"""V0.2.0 grid router (A*, 2 layers, 8 directions) producing MCP route_trace / add_via / add_zone steps.

Why a project router: MCP route_pad_to_pad draws straight pad-to-pad segments only (V0.0.2 finding D-9) and
Freerouting is not pre-approved. This script only computes geometry; all copper is written through the
MCP server, and KiCad's own DRC (kicad-cli, zones refilled, schematic parity) is the acceptance check.

Input : pcb_state.json from pcb_extract.py (pads in local mm, read from the saved board with pcbnew).
Output: routes.json (segments, vias, zones) and p3_route.json (MCP steps).
Usage : python -I route_pcb.py <pcb_state.json> <out_dir>

Rules mirrored from build_pcb.RULES: clearance 0.20 mm (router uses 0.24 to cover grid/diagonal effects),
edge clearance 0.5 mm, via 0.6/0.3 mm, no via inside SMD pads.
"""
import heapq
import json
import math
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_pcb as L  # noqa: E402

G = 0.1                     # grid pitch (mm)
CLR = 0.24                  # router clearance (DRC rule 0.20 + margin)
EDGE = 0.5 + 0.05           # copper-to-edge
VIA_D, VIA_DRILL = 0.6, 0.3
HOLE_CLR = 0.3              # drill-to-drill (KiCad default min 0.25)
LAYERS = ("F.Cu", "B.Cu")
LAYER_COST = (1.0, 2.5)     # keep the bottom GND plane as intact as possible
VIA_COST, BEND_COST = 2.0, 0.05

WIDTH = defaultdict(lambda: 0.25)
WIDTH.update({"VIN_RAW": 0.5, "+5V_P": 0.5, "+3V3_P": 0.5, "GND": 0.4, "EF_RTN": 0.3, "3V3_ESP": 0.3})

# Zones (local mm). Region rectangles also act as keep-outs on their layer for foreign-net tracks.
ZONES = [
    dict(net="+3V3_P", layer="F.Cu", conn="solid",
         pts=[(42.0, 4.0), (57.0, 4.0), (57.0, 22.5), (51.0, 22.5), (51.0, 17.4), (46.0, 17.4), (46.0, 22.5), (42.0, 22.5)],
         keepout=[(42.0, 4.0, 57.0, 17.4), (42.0, 17.4, 46.0, 22.5), (51.0, 17.4, 57.0, 22.5)],
         why="TLV1117LV tab thermal copper (>= 194 mm2), notch for C3/C4 and their GND vias"),
    dict(net="EF_RTN", layer="F.Cu", conn="solid", pts=[(16.2, 16.9), (31.0, 16.9), (31.0, 19.6), (16.2, 19.6)],
         keepout=[(16.2, 16.9, 31.0, 19.6)],
         why="TPS2660 RTN island (SLVSDG2G 12.1: RTN must be a copper plane or island)"),
    dict(net="GND", layer="F.Cu", pts=[(0, 0), (12.0, 0), (12.0, 24.0), (57.5, 24.0), (57.5, 0), (L.W, 0), (L.W, L.H), (0, L.H)],
         conn="thermal", keepout=[], why="top GND pour outside the power-entry/thermal area"),
    dict(net="GND", layer="B.Cu", pts=[(0, 0), (L.W, 0), (L.W, L.H), (0, L.H)], conn="thermal", keepout=[],
         why="bottom GND plane (return path for all signals)"),
]
# Pre-routes: pins of one net inside a fine-pitch package, joined before routing (exact geometry).
PREROUTES = [("U5", "1", "U5", "2", "VIN_RAW", 0.4), ("U5", "16", "U5", "15", "+5V_P", 0.4)]
NET_ORDER = ["VIN_RAW", "EF_RTN", "EF_UVLO", "EF_OVP", "EF_ILIM", "EF_DVDT", "+5V_P", "+3V3_P", "3V3_ESP"]


# ------------------------------------------------------------------ geometry
def seg_dist(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    L2 = dx * dx + dy * dy
    t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / L2))
    return math.hypot(px - ax - t * dx, py - ay - t * dy)


class Shape:
    __slots__ = ("net", "layer", "kind", "g", "bbox", "smd", "hole")

    def __init__(self, net, layer, kind, g, smd=False, hole=0.0):
        self.net, self.layer, self.kind, self.g, self.smd, self.hole = net, layer, kind, g, smd, hole
        if kind == "rect":
            cx, cy, hw, hh, a = g
            r = math.hypot(hw, hh)
            self.bbox = (cx - r, cy - r, cx + r, cy + r)
        elif kind == "circle":
            cx, cy, r = g
            self.bbox = (cx - r, cy - r, cx + r, cy + r)
        elif kind == "seg":
            ax, ay, bx, by, r = g
            self.bbox = (min(ax, bx) - r, min(ay, by) - r, max(ax, bx) + r, max(ay, by) + r)
        elif kind == "poly":   # zone keep-out region (axis-aligned rectangle list)
            xs, ys = [p[0] for p in g], [p[1] for p in g]
            self.bbox = (min(xs), min(ys), max(xs), max(ys))

    def dist(self, x, y):
        k, g = self.kind, self.g
        if k == "rect":
            cx, cy, hw, hh, a = g
            c, s = math.cos(a), math.sin(a)
            u, v = (x - cx) * c + (y - cy) * s, -(x - cx) * s + (y - cy) * c
            return math.hypot(max(abs(u) - hw, 0.0), max(abs(v) - hh, 0.0))
        if k == "circle":
            return math.hypot(x - g[0], y - g[1]) - g[2]
        if k == "seg":
            return seg_dist(x, y, g[0], g[1], g[2], g[3]) - g[4]
        x0, y0, x1, y1 = self.bbox
        return math.hypot(max(x0 - x, 0, x - x1), max(y0 - y, 0, y - y1))

    def contains(self, x, y):
        return self.dist(x, y) <= 1e-9


class World:
    BUCKET = 1.0

    def __init__(self):
        self.idx = [defaultdict(list), defaultdict(list)]
        self.holes = []

    def add(self, sh, pad=None):
        li = LAYERS.index(sh.layer)
        x0, y0, x1, y1 = sh.bbox
        m = 0.8
        for bx in range(int((x0 - m) // self.BUCKET), int((x1 + m) // self.BUCKET) + 1):
            for by in range(int((y0 - m) // self.BUCKET), int((y1 + m) // self.BUCKET) + 1):
                self.idx[li][(bx, by)].append(sh)

    def near(self, li, x, y):
        return self.idx[li].get((int(x // self.BUCKET), int(y // self.BUCKET)), ())

    def free(self, li, x, y, net, need, smd_block=False):
        if min(x, L.W - x, y, L.H - y) < need - CLR + EDGE:
            return False
        for sh in self.near(li, x, y):
            if sh.net != net or (smd_block and sh.smd):
                if sh.dist(x, y) < need - (0.0 if sh.net != net else CLR - 0.1):
                    return False
        return True

    def via_ok(self, x, y, net):
        r = VIA_D / 2
        for li in (0, 1):
            if not self.free(li, x, y, net, r + CLR, smd_block=True):
                return False
        for hx, hy, hr in self.holes:
            if math.hypot(x - hx, y - hy) < hr + VIA_DRILL / 2 + HOLE_CLR:
                return False
        return True


def pad_shapes(p):
    a = math.radians(-p["angle"])          # KiCad CCW (y down) -> math frame
    out = []
    if p["ref"].startswith("FID"):         # fiducial: keep tracks outside the 2 mm mask opening and its 0.6 mm local clearance
        return [Shape(None, lay, "circle", (p["x"], p["y"], max(1.0, p["w"] / 2 + 0.6) + 0.05)) for lay in p["layers"]]
    for lay in p["layers"]:
        if p["shape"] == "0" or p["shape"].lower().startswith("circle"):     # pcbnew PAD_SHAPE_CIRCLE = 0
            out.append(Shape(p["net"] or None, lay, "circle", (p["x"], p["y"], p["w"] / 2), smd=not p["drill"]))
        else:
            out.append(Shape(p["net"] or None, lay, "rect", (p["x"], p["y"], p["w"] / 2, p["h"] / 2, a),
                             smd=not p["drill"]))
    return out


# ------------------------------------------------------------------ router
def snap(v):
    return round(v / G)


DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]


def astar(world, net, w, sources, target_pads, max_exp=400000):
    """sources: set of (li, ix, iy). target_pads: list of Shape (own net). Returns node path or None."""
    need = w / 2 + CLR
    tx = sum(s.g[0] for s in target_pads) / len(target_pads)
    ty = sum(s.g[1] for s in target_pads) / len(target_pads)
    tlay = {LAYERS.index(s.layer) for s in target_pads}
    memo = {}

    def ok(li, ix, iy):
        k = (li, ix, iy)
        v = memo.get(k)
        if v is None:
            v = memo[k] = world.free(li, ix * G, iy * G, net, need)
        return v

    def is_target(li, ix, iy):
        if li not in tlay:
            return False
        x, y = ix * G, iy * G
        return any(LAYERS.index(s.layer) == li and s.contains(x, y) for s in target_pads)

    def h(ix, iy):
        dx, dy = abs(ix * G - tx), abs(iy * G - ty)
        return max(dx, dy) + 0.4142 * min(dx, dy)

    openq, best, parent = [], {}, {}
    for s in sources:
        best[s] = 0.0
        parent[s] = None
        heapq.heappush(openq, (h(s[1], s[2]), 0.0, s, None))
    exp = 0
    while openq:
        f, g, node, d = heapq.heappop(openq)
        if g > best.get(node, 1e18) + 1e-9:
            continue
        li, ix, iy = node
        if is_target(li, ix, iy):
            path = []
            while node is not None:
                path.append(node)
                node = parent[node]
            return path[::-1]
        exp += 1
        if exp > max_exp:
            return None
        for k, (dx, dy) in enumerate(DIRS):
            nx, ny = ix + dx, iy + dy
            if not ok(li, nx, ny):
                continue
            step = G * (1.4142 if dx and dy else 1.0) * LAYER_COST[li]
            ng = g + step + (BEND_COST if d is not None and d != k else 0.0)
            nn = (li, nx, ny)
            if ng < best.get(nn, 1e18) - 1e-9:
                best[nn], parent[nn] = ng, node
                heapq.heappush(openq, (ng + h(nx, ny), ng, nn, k))
        oli = 1 - li
        nn = (oli, ix, iy)
        if ok(oli, ix, iy) and world.via_ok(ix * G, iy * G, net):
            ng = g + VIA_COST
            if ng < best.get(nn, 1e18) - 1e-9:
                best[nn], parent[nn] = ng, node
                heapq.heappush(openq, (ng + h(ix, iy), ng, nn, None))
    return None


def path_to_copper(path, net, w):
    segs, vias = [], []
    run = [path[0]]
    for a, b in zip(path, path[1:]):
        if a[0] != b[0]:
            if len(run) > 1:
                segs.append((run[0], run[-1]))
            vias.append((a[1] * G, a[2] * G))
            run = [b]
            continue
        if len(run) >= 2:
            d0 = (run[-1][1] - run[-2][1], run[-1][2] - run[-2][2])
            d1 = (b[1] - a[1], b[2] - a[2])
            if d0 != d1:
                segs.append((run[0], run[-1]))
                run = [run[-1]]
        run.append(b)
    if len(run) > 1:
        segs.append((run[0], run[-1]))
    out = [dict(net=net, w=w, layer=LAYERS[s[0][0]], x1=s[0][1] * G, y1=s[0][2] * G, x2=s[1][1] * G, y2=s[1][2] * G)
           for s in segs]
    return out, [dict(net=net, x=x, y=y) for x, y in vias]


def nodes_inside(shape, li, net, world, w):
    x0, y0, x1, y1 = shape.bbox
    res = []
    for ix in range(snap(x0) - 1, snap(x1) + 2):
        for iy in range(snap(y0) - 1, snap(y1) + 2):
            if shape.contains(ix * G, iy * G) and world.free(li, ix * G, iy * G, net, w / 2 + CLR):
                res.append((li, ix, iy))
    return res


def build_world(st):
    world = World()
    pads_by_net, pad_index = defaultdict(list), {}
    for p in st["pads"]:
        shapes = pad_shapes(p)
        for sh in shapes:
            world.add(sh)
        if p["drill"]:
            world.holes.append((p["x"], p["y"], p["drill"] / 2))
        if p["net"]:
            pads_by_net[p["net"]].append((p, shapes))
        pad_index[(p["ref"], p["num"])] = (p, shapes)
    for z in ZONES:
        for (x0, y0, x1, y1) in z["keepout"]:
            world.add(Shape(z["net"], z["layer"], "poly", [(x0, y0), (x1, y1)]))
    # THT GND pads: keep a ring free so the zone thermal-relief spokes are not starved (DRC starved_thermal)
    for p, shapes in pads_by_net.get("GND", []):
        if p["drill"]:
            for lay in p["layers"]:
                world.add(Shape("__SPOKES__", lay, "circle", (p["x"], p["y"], max(p["w"], p["h"]) / 2 + 0.7)))
    return world, pads_by_net, pad_index


def run(st, priority):
    """Route everything once. priority: list of job ids routed first (from failures of a previous pass)."""
    world, pads_by_net, pad_index = build_world(st)
    segs, vias, report = [], [], []

    def commit(new_segs, new_vias):
        for s in new_segs:
            segs.append(s)
            world.add(Shape(s["net"], s["layer"], "seg", (s["x1"], s["y1"], s["x2"], s["y2"], s["w"] / 2)))
        for v in new_vias:
            vias.append(v)
            for lay in LAYERS:
                world.add(Shape(v["net"], lay, "circle", (v["x"], v["y"], VIA_D / 2)))
            world.holes.append((v["x"], v["y"], VIA_DRILL / 2))

    connected = defaultdict(set)
    for r1, n1, r2, n2, net, w in PREROUTES:
        a, b = pad_index[(r1, n1)][0], pad_index[(r2, n2)][0]
        commit([dict(net=net, w=w, layer="F.Cu", x1=a["x"], y1=a["y"], x2=b["x"], y2=b["y"])], [])
        connected[net] |= {id(a), id(b)}

    def gnd_escape(p, shapes):
        w = WIDTH["GND"]
        sh = shapes[0]
        best = None
        for rad in range(3, 40):
            for ix in range(snap(p["x"]) - rad, snap(p["x"]) + rad + 1):
                for iy in range(snap(p["y"]) - rad, snap(p["y"]) + rad + 1):
                    if max(abs(ix - snap(p["x"])), abs(iy - snap(p["y"]))) != rad:
                        continue
                    x, y = ix * G, iy * G
                    if sh.dist(x, y) < VIA_D / 2 + 0.15:
                        continue
                    if world.via_ok(x, y, "GND") and world.free(0, x, y, "GND", w / 2 + CLR):
                        d = math.hypot(x - p["x"], y - p["y"])
                        if best is None or d < best[0]:
                            best = (d, ix, iy)
            if best:
                break
        if not best:
            return False
        _, ix, iy = best
        path = astar(world, "GND", w, {(0, ix, iy)}, shapes, max_exp=20000)
        if path is None:
            return False
        ns, _ = path_to_copper(path, "GND", w)
        end = path[-1]
        ns.append(dict(net="GND", w=min(w, p["w"], p["h"]), layer="F.Cu", x1=end[1] * G, y1=end[2] * G,
                       x2=p["x"], y2=p["y"]))
        commit([s for s in ns if (s["x1"], s["y1"]) != (s["x2"], s["y2"])], [dict(net="GND", x=ix * G, y=iy * G)])
        return True

    def route_net(net):
        w = WIDTH[net]
        items = pads_by_net[net]
        done_ids = set(connected[net]) or {id(items[0][0])}
        tree_nodes = set()
        for p, shapes in items:
            if id(p) in done_ids:
                for sh in shapes:
                    tree_nodes |= set(nodes_inside(sh, LAYERS.index(sh.layer), net, world, w))
        todo = [(p, s) for p, s in items if id(p) not in done_ids]
        fails = []
        while todo:
            todo.sort(key=lambda it: min((math.hypot(it[0]["x"] - n[1] * G, it[0]["y"] - n[2] * G)
                                          for n in tree_nodes), default=0))
            p, shapes = todo.pop(0)
            path = astar(world, net, w, tree_nodes, shapes) if tree_nodes else None
            if path is None:
                fails.append(f"{p['ref']}.{p['num']}")
                continue
            ns, nv = path_to_copper(path, net, w)
            end = path[-1]
            ns.append(dict(net=net, w=min(w, p["w"], p["h"]) if not p["drill"] else w, layer=LAYERS[end[0]],
                           x1=end[1] * G, y1=end[2] * G, x2=p["x"], y2=p["y"]))
            commit([s for s in ns if (s["x1"], s["y1"]) != (s["x2"], s["y2"])], nv)
            tree_nodes |= set(path)
            for sh in shapes:
                tree_nodes |= set(nodes_inside(sh, LAYERS.index(sh.layer), net, world, w))
        return fails

    gnd_jobs = [f"GND:{p['ref']}.{p['num']}" for p, _ in pads_by_net["GND"] if not p["drill"]]
    net_jobs = [n for n in NET_ORDER if n in pads_by_net] + sorted(
        n for n in pads_by_net if n not in NET_ORDER and n != "GND")
    jobs = [j for j in priority] + [j for j in gnd_jobs + net_jobs if j not in priority]
    failed = []
    for job in jobs:
        if job.startswith("GND:"):
            ref, num = job[4:].rsplit(".", 1)
            p, shapes = pad_index[(ref, num)]
            if not gnd_escape(p, shapes):
                failed.append(job)
                report.append(f"FAIL {job}")
        else:
            f = route_net(job)
            if f:
                failed.append(job)
                report.append(f"FAIL {job}: {f}")
    return segs, vias, report, failed


def main():
    st = json.load(open(sys.argv[1]))
    out_dir = sys.argv[2]
    priority = []
    for attempt in range(1, 7):
        segs, vias, report, failed = run(st, priority)
        print(f"pass {attempt}: segments {len(segs)}, vias {len(vias)}, failed {failed}")
        if not failed:
            break
        priority = failed + [p for p in priority if p not in failed]
    total_fail = len(failed)
    res = dict(segments=segs, vias=vias, zones=ZONES, report=report, failures=total_fail, priority=priority)
    os.makedirs(out_dir, exist_ok=True)
    json.dump(res, open(os.path.join(out_dir, "routes.json"), "w"), indent=1)
    steps = [{"label": "open", "name": "open_project", "arguments": {"filename": os.path.join(L.B.PROJ_DIR, L.B.NAME + ".kicad_pro")}}]
    ox, oy = L.ORIGIN
    for i, s in enumerate(segs):
        steps.append({"label": f"t{i}", "name": "route_trace", "arguments": {
            "start": {"x": round(ox + s["x1"], 4), "y": round(oy + s["y1"], 4), "unit": "mm"},
            "end": {"x": round(ox + s["x2"], 4), "y": round(oy + s["y2"], 4), "unit": "mm"},
            "layer": s["layer"], "width": s["w"], "net": s["net"]}})
    for i, v in enumerate(vias):
        steps.append({"label": f"v{i}", "name": "add_via", "arguments": {
            "position": {"x": round(ox + v["x"], 4), "y": round(oy + v["y"], 4), "unit": "mm"}, "net": v["net"]}})
    for i, z in enumerate(ZONES):
        steps.append({"label": f"z{i}", "name": "add_zone", "arguments": {
            "layer": z["layer"], "net": z["net"], "unit": "mm", "clearance": 0.3, "minWidth": 0.25,
            "padConnection": z["conn"], "points": [{"x": round(ox + x, 4), "y": round(oy + y, 4)} for x, y in z["pts"]]}})
    steps.append({"label": "save", "name": "save_project", "arguments": {}})
    json.dump(steps, open(os.path.join(out_dir, "p3_route.json"), "w"), indent=1)
    print(f"segments {len(segs)}, vias {len(vias)}, zones {len(ZONES)}, failures {total_fail}")
    for r in report:
        if "FAIL" in r:
            print(" ", r)


if __name__ == "__main__":
    main()
