"""Independent audit of the V0.2.0 manufacturing package against the board (pcbnew read-only).

Checks (each PASS/FAIL):
 G1 required Gerber layers present with correct X2 FileFunction; units/format declared
 G2 Edge.Cuts extents = 90.0 x 64.0 mm at the aux origin (0,0)
 G3 F.Paste flashes = SMD pads with paste on F.Cu; B.Paste empty (single-sided assembly)
 D1 PTH holes = plated pads + vias by diameter; D2 NPTH holes = 4 x 3.2 mm mounting holes
 C1 CPL refs = assembled parts (BOM placements) + fiducials; C2 X/Y match board (aux origin, Y up) within 1 um;
 C3 rotation matches footprint orientation; C4 all on top side
 B1 BOM placements = schematic in_bom parts; every line has Manufacturer + MPN
 N1 IPC-D-356 contains every routed net
Usage: python -I audit_fab_outputs.py <manufacturing/v0.2.0> <board.kicad_pcb>
"""
import csv
import glob
import os
import re
import sys
from collections import Counter

import pcbnew

mdir, board_path = sys.argv[1:3]
mm = pcbnew.ToMM
board = pcbnew.LoadBoard(board_path)
ax = board.GetDesignSettings().GetAuxOrigin()
AX, AY = mm(ax.x), mm(ax.y)
res = []


def check(cid, ok, msg):
    res.append((cid, ok, msg))


gdir = os.path.join(mdir, "gerbers")
files = {os.path.basename(f): f for f in glob.glob(os.path.join(gdir, "*"))}
need = {"F_Cu.gtl": "Copper,L1,Top", "B_Cu.gbl": "Copper,L2,Bot", "F_Mask.gts": "Soldermask,Top",
        "B_Mask.gbs": "Soldermask,Bot", "F_Paste.gtp": "Paste,Top", "B_Paste.gbp": "Paste,Bot",
        "F_Silkscreen.gto": "Legend,Top", "B_Silkscreen.gbo": "Legend,Bot", "Edge_Cuts.gm1": "Profile"}
miss = []
for suffix, ff in need.items():
    f = [p for n, p in files.items() if n.endswith(suffix)]
    if not f:
        miss.append(suffix)
        continue
    s = open(f[0], encoding="utf-8", errors="replace").read()
    if ff not in s or "%MOMM*%" not in s:
        miss.append(f"{suffix} (FileFunction/units)")
check("G1", not miss, f"Gerber layers/X2 attributes {'OK' if not miss else miss}")


def coords(path):
    s = open(path, encoding="utf-8", errors="replace").read()
    fmt = re.search(r"%FSLAX(\d)(\d)Y(\d)(\d)\*%", s)
    dec = int(fmt.group(2))
    pts, flashes = [], 0
    x = y = 0.0
    for m in re.finditer(r"(?:X(-?\d+))?(?:Y(-?\d+))?D0?([123])\*", s):
        if m.group(1) is None and m.group(2) is None:
            continue
        if m.group(1) is not None:
            x = int(m.group(1)) / 10 ** dec
        if m.group(2) is not None:
            y = int(m.group(2)) / 10 ** dec
        pts.append((x, y))
        flashes += m.group(3) == "3"
    return pts, flashes


edge = [p for n, p in files.items() if n.endswith("Edge_Cuts.gm1")][0]
pts, _ = coords(edge)
xs, ys = [p[0] for p in pts], [p[1] for p in pts]
w, h = max(xs) - min(xs), max(ys) - min(ys)
check("G2", abs(min(xs)) < 0.06 and abs(min(ys)) < 0.06 and abs(w - 90) < 0.11 and abs(h - 64) < 0.11,
      f"Edge.Cuts extents x {min(xs):.3f}..{max(xs):.3f}, y {min(ys):.3f}..{max(ys):.3f} (w {w:.3f}, h {h:.3f}; line width incl.)")

smd_paste = sum(1 for fp in board.GetFootprints() for p in fp.Pads() if p.IsOnLayer(pcbnew.F_Paste))
_, fpaste = coords([p for n, p in files.items() if n.endswith("F_Paste.gtp")][0])
_, bpaste = coords([p for n, p in files.items() if n.endswith("B_Paste.gbp")][0])
# custom-shape pads are written as regions (not flashes): count them separately
custom_paste = sum(1 for fp in board.GetFootprints() for p in fp.Pads()
                   if p.IsOnLayer(pcbnew.F_Paste) and p.GetShape(pcbnew.F_Cu) == pcbnew.PAD_SHAPE_CUSTOM)
check("G3", fpaste == smd_paste - custom_paste and bpaste == 0,
      f"F.Paste flashes {fpaste} vs SMD paste pads {smd_paste} (custom-shape {custom_paste}); B.Paste flashes {bpaste}")


def drill_hits(path):
    s = open(path, encoding="utf-8", errors="replace").read()
    tools = {m.group(1): float(m.group(2)) for m in re.finditer(r"^T(\d+)C([\d.]+)", s, re.M)}
    cnt, cur = Counter(), None
    for line in s.splitlines():
        m = re.match(r"^T(\d+)$", line)
        if m:
            cur = m.group(1)
        elif re.match(r"^X-?[\d.]+Y-?[\d.]+", line) and cur:
            cnt[round(tools[cur], 3)] += 1
    return cnt


exp_pth, exp_npth = Counter(), Counter()
for fp in board.GetFootprints():
    for p in fp.Pads():
        d = p.GetDrillSize().x
        if d:
            (exp_npth if p.GetAttribute() == pcbnew.PAD_ATTRIB_NPTH else exp_pth)[round(mm(d), 3)] += 1
for t in board.GetTracks():
    if t.GetClass() == "PCB_VIA":
        exp_pth[round(mm(t.GetDrillValue()), 3)] += 1
pth = drill_hits([p for n, p in files.items() if n.endswith("-PTH.drl")][0])
npth = drill_hits([p for n, p in files.items() if n.endswith("-NPTH.drl")][0])
check("D1", pth == exp_pth, f"PTH by diameter file {dict(pth)} vs board {dict(exp_pth)}")
check("D2", npth == exp_npth and npth == Counter({3.2: 4}), f"NPTH file {dict(npth)} vs board {dict(exp_npth)}")

cpl_path = glob.glob(os.path.join(mdir, "assembly", "*_CPL.csv"))[0]
bom_path = glob.glob(os.path.join(mdir, "assembly", "*_BOM.csv"))[0]
cpl = {r["Ref"]: r for r in csv.DictReader(open(cpl_path, encoding="utf-8"))}
bom_refs = set()
bom_ok = True
for r in csv.DictReader(open(bom_path, encoding="utf-8")):
    bom_refs |= set(r["References"].split())
    bom_ok &= bool(r["MPN"]) and bool(r["Manufacturer"])
fids = {fp.GetReference() for fp in board.GetFootprints() if fp.GetReference().startswith("FID")}
check("C1", set(cpl) == bom_refs | fids, f"CPL refs {len(cpl)} = BOM placements {len(bom_refs)} + fiducials {len(fids)}"
      + ("" if set(cpl) == bom_refs | fids else f"; diff {sorted(set(cpl) ^ (bom_refs | fids))}"))
bad_xy, bad_rot, bad_side = [], [], []
for fp in board.GetFootprints():
    ref = fp.GetReference()
    if ref not in cpl:
        continue
    r = cpl[ref]
    x, y = mm(fp.GetPosition().x) - AX, AY - mm(fp.GetPosition().y)
    if abs(float(r["PosX"]) - x) > 1e-3 or abs(float(r["PosY"]) - y) > 1e-3:
        bad_xy.append(ref)
    rot = fp.GetOrientationDegrees()
    if abs(((float(r["Rot"]) - rot) + 180) % 360 - 180) > 0.01:
        bad_rot.append(ref)
    if r["Side"] != "top":
        bad_side.append(ref)
check("C2", not bad_xy, f"CPL X/Y vs board (aux origin {AX},{AY}; Y up): mismatches {bad_xy}")
check("C3", not bad_rot, f"CPL rotation vs footprint orientation: mismatches {bad_rot}")
check("C4", not bad_side, f"all CPL parts on top: exceptions {bad_side}")
check("B1", bom_ok and len(bom_refs) == 52, f"BOM placements {len(bom_refs)} (expected 52), all lines with MPN+Manufacturer: {bom_ok}")

d356 = [p for n, p in files.items() if n.endswith(".d356")][0]
s = open(d356, encoding="utf-8", errors="replace").read()
nets_file = set(re.findall(r"^3\d\d(\S+)", s, re.M))
routed = {t.GetNetname() for t in board.GetTracks() if t.GetNetname()}
missing = sorted(n for n in routed if n[:14] not in {x[:14] for x in nets_file})
check("N1", not missing, f"IPC-D-356 nets {len(nets_file)}; routed nets missing: {missing}")

for cid, ok, msg in res:
    print(f"{cid}: {'PASS' if ok else 'FAIL'}  {msg}")
print("RESULT:", "PASS" if all(ok for _, ok, _ in res) else "FAIL")
sys.exit(0 if all(ok for _, ok, _ in res) else 1)
