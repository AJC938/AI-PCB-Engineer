"""V0.2.0 PCB build: board outline, design rules, placement (single source of truth for the layout).

Usage:
  python -I build_pcb.py check <fp_geom.json>          offline legality check (courtyards, edge, holes)
  python -I build_pcb.py steps <out_dir>               write MCP step files p1 (sync) and p2 (rules+outline+placement)

Coordinates: local mm with origin at the board's top-left corner; KiCad absolute = local + ORIGIN.
Rotation: KiCad degrees, counter-clockwise on screen (y axis down).
Rationale for the arrangement: reports/v0.2.0/PCB_PLACEMENT_REVIEW.md.
"""
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_schematic as B  # noqa: E402

ORIGIN = (100.0, 100.0)
W, H = 90.0, 64.0
EDGE_KEEPOUT = 0.5            # copper/courtyard to board edge (DFM profile, strictest shortlisted value +)
PCB = os.path.join(B.PROJ_DIR, B.NAME + ".kicad_pcb")

# Design rules (provisional, vendor-independent; see manufacturing/v0.2.0/manufacturer_profiles/)
RULES = dict(clearance=0.2, trackWidth=0.25, viaDiameter=0.6, viaDrill=0.3, minTrackWidth=0.2,
             minViaDiameter=0.6, minViaDrill=0.3, minHoleDiameter=0.3, requireCourtyard=True, courtyardClearance=0.0)

# ref: (x, y, rotation)
P = {
    # --- power entry (top-left), eFuse, divider, RTN island
    "J1": (5.6, 11.0, 270), "TP1": (14.5, 5.0, 0), "C12": (16.0, 9.5, 270),
    "U5": (22.0, 12.0, 0),
    "R16": (13.2, 14.0, 270), "R17": (15.2, 14.0, 270), "R18": (17.2, 16.7, 270),
    "R19": (27.5, 13.6, 270), "C13": (29.5, 13.6, 270),
    # --- +5V_P bulk, LDO, +3V3_P thermal copper area (x 42..56)
    "C1": (32.5, 9.5, 270), "C2": (34.5, 9.5, 270), "TP2": (31.0, 22.5, 0),
    "U1": (40.5, 12.0, 0), "C5": (36.0, 18.2, 270),
    "C3": (47.5, 19.3, 270), "C4": (49.5, 19.3, 270), "TP3": (52.5, 6.5, 0),
    # --- indicators
    "LED1": (59.5, 8.0, 0), "R2": (59.0, 13.0, 0), "LED2": (59.5, 18.0, 0), "R3": (59.0, 22.8, 0),
    # --- ultrasonic (J3 right edge, top)
    "J3": (86.5, 9.5, 0), "C8": (81.5, 10.5, 270), "C9": (79.5, 10.5, 270),
    "U3": (71.5, 12.0, 0), "C6": (67.5, 10.0, 270), "C7": (75.5, 10.5, 270), "R4": (67.5, 14.5, 270),
    "R15": (77.5, 14.0, 0), "R5": (81.0, 14.5, 270), "TP8": (78.5, 6.0, 0),
    "U2": (72.0, 20.0, 0), "C10": (67.5, 19.5, 270), "R6": (81.5, 18.5, 180), "R7": (76.5, 19.5, 270),
    "TP7": (72.0, 25.0, 0),
    # --- UART (J4)
    "J4": (86.5, 21.5, 0), "JP1": (80.5, 24.0, 0), "R10": (81.0, 27.0, 0), "R11": (81.0, 29.5, 180),
    "U4": (75.5, 30.0, 0), "R12": (76.5, 26.0, 0), "C11": (71.0, 29.5, 270),
    # --- I2C (J5)
    "J5": (86.5, 33.5, 0), "R8": (81.0, 37.5, 0), "R9": (81.0, 40.5, 0), "JP2": (76.5, 39.0, 0),
    # --- GP (J6)
    "J6": (86.5, 45.5, 0), "R13": (81.0, 50.5, 180), "R14": (81.0, 53.0, 180),
    # --- ESP32 cable header (bottom edge), test points
    "J2": (32.0, 60.0, 90), "TP4": (26.0, 57.5, 0), "TP5": (20.0, 57.5, 0), "TP6": (64.0, 36.0, 0),
    # --- mechanical
    "H1": (3.5, 3.5, 0), "H2": (86.5, 3.5, 0), "H3": (3.5, 60.5, 0), "H4": (86.5, 60.5, 0),
    "FID1": (9.0, 25.0, 0), "FID2": (60.0, 50.0, 0), "FID3": (12.0, 50.0, 0),
}


def rot(x, y, deg):
    t = math.radians(deg)
    return x * math.cos(t) + y * math.sin(t), -x * math.sin(t) + y * math.cos(t)


def courtyard_abs(ref, geom):
    x0, y0, x1, y1 = geom[ref]["crtyd"]
    px, py, r = P[ref]
    pts = [rot(a, b, r) for a, b in ((x0, y0), (x1, y0), (x1, y1), (x0, y1))]
    xs, ys = [p[0] + px for p in pts], [p[1] + py for p in pts]
    return min(xs), min(ys), max(xs), max(ys)


def check(geom_path):
    geom = json.load(open(geom_path))
    # mounting holes / fiducials are not in fp_geom.json (no MPN) -> fixed keep-outs
    keep = {"H": 3.45, "FID": 1.5}
    boxes, errs = {}, []
    for ref in P:
        if ref.startswith(("H", "FID")) and not ref.startswith("HT"):
            r = keep["FID" if ref.startswith("FID") else "H"]
            x, y, _ = P[ref]
            boxes[ref] = (x - r, y - r, x + r, y + r)
        else:
            boxes[ref] = courtyard_abs(ref, geom)
    missing = set(B.PARTS) - set(P)
    if missing:
        errs.append(f"unplaced: {sorted(missing)}")
    for ref, (a, b, c, d) in boxes.items():
        if a < EDGE_KEEPOUT - 1e-6 or b < EDGE_KEEPOUT - 1e-6 or c > W - EDGE_KEEPOUT + 1e-6 or d > H - EDGE_KEEPOUT + 1e-6:
            if not ref.startswith("H"):
                errs.append(f"edge: {ref} {tuple(round(v, 2) for v in (a, b, c, d))}")
    refs = list(boxes)
    for i, r1 in enumerate(refs):
        for r2 in refs[i + 1:]:
            a, b = boxes[r1], boxes[r2]
            ox, oy = min(a[2], b[2]) - max(a[0], b[0]), min(a[3], b[3]) - max(a[1], b[1])
            if ox > 1e-6 and oy > 1e-6:
                errs.append(f"overlap: {r1} x {r2} ({ox:.2f} x {oy:.2f})")
    print(f"placed {len(P)} / parts {len(B.PARTS)}; board {W} x {H} mm")
    print("RESULT:", "PASS" if not errs else "FAIL")
    for e in errs:
        print("  -", e)
    return not errs


def steps(out):
    os.makedirs(out, exist_ok=True)
    sch = os.path.join(B.PROJ_DIR, B.NAME + ".kicad_sch")
    pro = os.path.join(B.PROJ_DIR, B.NAME + ".kicad_pro")
    p1 = [{"label": "open", "name": "open_project", "arguments": {"filename": pro}},
          {"label": "sync", "name": "sync_schematic_to_board", "arguments": {"schematicPath": sch, "boardPath": PCB}}]
    p2 = [{"label": "open", "name": "open_project", "arguments": {"filename": pro}},
          {"label": "rules", "name": "set_design_rules", "arguments": RULES},
          {"label": "outline", "name": "add_board_outline", "arguments": {
              "shape": "rectangle", "params": {"x": ORIGIN[0], "y": ORIGIN[1], "width": W, "height": H, "unit": "mm"}}}]
    for ref, (x, y, r) in P.items():
        p2.append({"label": f"mv_{ref}", "name": "move_component", "arguments": {
            "reference": ref, "position": {"x": round(ORIGIN[0] + x, 4), "y": round(ORIGIN[1] + y, 4), "unit": "mm"},
            "rotation": r}})
    p2.append({"label": "save", "name": "save_project", "arguments": {}})
    json.dump(p1, open(os.path.join(out, "p1_sync.json"), "w"), indent=1)
    json.dump(p2, open(os.path.join(out, "p2_place.json"), "w"), indent=1)
    print(f"p1 {len(p1)} steps, p2 {len(p2)} steps -> {out}")


if __name__ == "__main__":
    if sys.argv[1] == "check":
        sys.exit(0 if check(sys.argv[2]) else 1)
    steps(sys.argv[2])
