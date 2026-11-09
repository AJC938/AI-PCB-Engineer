# SPDX-FileCopyrightText: 2026 AI-PCB-Engineer contributors
# SPDX-License-Identifier: MIT
"""Independent audit of the Rev A (V1.0.0) manufacturing outputs against the saved board (pcbnew, read-only).

Derived from hardware/kicad/<board>/build/audit_fab_outputs.py (V0.2.0, 11 checks) with extra checks.
 G1 required Gerber layers present, X2 FileFunction, mm units, format 4.6
 G2 Edge.Cuts extents = 90.0 x 64.0 mm with (0,0) at the board bottom-left
 G3 F.Paste flashes = SMD pads with paste; B.Paste empty (single-sided assembly)
 G4 every coordinate in every Gerber lies inside the outline (+0.1 mm)
 G5 Gerber job file: 2 copper layers, 1.6 mm, board size 90 x 64 mm
 G6 B.Silkscreen empty; F.Silkscreen contains the Rev A label
 D1 PTH holes = plated pads + vias by diameter;  D2 NPTH = 4 x 3.2 mm mounting holes
 D3 Excellon files METRIC; every board hole has a drill hit at the same X/Y (0.005 mm)
 C1 CPL refs = BOM placements + fiducials;  C2 X/Y match board;  C3 rotation matches;  C4 all top side
 B1 52 BOM placements, every line has Manufacturer + MPN;  B2 Qty column = reference count, 33 lines,
 B3 every BOM line has Mount SMT/THT and Side Top
 N1 IPC-D-356 contains every routed net
 F1 required package files present (STEP, drawings, schematic, notes)
Usage: python -I audit_release.py <manufacturing/<board>/RevA> <board.kicad_pcb>
"""
import csv
import glob
import json
import os
import re
import sys
from collections import Counter

import pcbnew

out_dir, board_path = sys.argv[1:3]
fab, asm = os.path.join(out_dir, "fabrication"), os.path.join(out_dir, "assembly")
mm = pcbnew.ToMM
board = pcbnew.LoadBoard(board_path)
ax = board.GetDesignSettings().GetAuxOrigin()
AX, AY = mm(ax.x), mm(ax.y)
res = []


def check(cid, ok, msg):
    res.append((cid, ok, msg))


def one(pattern):
    f = glob.glob(os.path.join(pattern))
    return f[0] if len(f) == 1 else None


files = {os.path.basename(f): f for f in glob.glob(os.path.join(fab, "*"))}
need = {"F_Cu.gtl": "Copper,L1,Top", "B_Cu.gbl": "Copper,L2,Bot", "F_Mask.gts": "Soldermask,Top",
        "B_Mask.gbs": "Soldermask,Bot", "F_Paste.gtp": "Paste,Top", "B_Paste.gbp": "Paste,Bot",
        "F_Silkscreen.gto": "Legend,Top", "B_Silkscreen.gbo": "Legend,Bot", "Edge_Cuts.gm1": "Profile"}
gpath, miss = {}, []
for suffix, ff in need.items():
    f = [p for n, p in files.items() if n.endswith(suffix)]
    if len(f) != 1:
        miss.append(suffix)
        continue
    gpath[suffix] = f[0]
    s = open(f[0], encoding="utf-8", errors="replace").read()
    if ff not in s or "%MOMM*%" not in s or "%FSLAX46Y46*%" not in s:
        miss.append(f"{suffix} (FileFunction/units/format)")
check("G1", not miss, f"9 Gerber layers, X2 FileFunction, mm, 4.6: {'OK' if not miss else miss}")


def coords(path):
    s = open(path, encoding="utf-8", errors="replace").read()
    dec = int(re.search(r"%FSLAX(\d)(\d)Y(\d)(\d)\*%", s).group(2))
    pts, flashes, x, y = [], 0, 0.0, 0.0
    for m in re.finditer(r"(?:X(-?\d+))?(?:Y(-?\d+))?(?:I-?\d+)?(?:J-?\d+)?D0?([123])\*", s):
        if m.group(1) is None and m.group(2) is None:
            continue
        if m.group(1) is not None:
            x = int(m.group(1)) / 10 ** dec
        if m.group(2) is not None:
            y = int(m.group(2)) / 10 ** dec
        pts.append((x, y))
        flashes += m.group(3) == "3"
    return pts, flashes


pts, _ = coords(gpath["Edge_Cuts.gm1"])
xs, ys = [p[0] for p in pts], [p[1] for p in pts]
w, h = max(xs) - min(xs), max(ys) - min(ys)
check("G2", abs(min(xs)) < 0.06 and abs(min(ys)) < 0.06 and abs(w - 90) < 0.11 and abs(h - 64) < 0.11,
      f"Edge.Cuts x {min(xs):.3f}..{max(xs):.3f}, y {min(ys):.3f}..{max(ys):.3f} (w {w:.3f}, h {h:.3f})")

smd_paste = sum(1 for fp in board.GetFootprints() for p in fp.Pads() if p.IsOnLayer(pcbnew.F_Paste))
custom_paste = sum(1 for fp in board.GetFootprints() for p in fp.Pads()
                   if p.IsOnLayer(pcbnew.F_Paste) and p.GetShape(pcbnew.F_Cu) == pcbnew.PAD_SHAPE_CUSTOM)
_, fpaste = coords(gpath["F_Paste.gtp"])
bpts, bpaste = coords(gpath["B_Paste.gbp"])
check("G3", fpaste == smd_paste - custom_paste and bpaste == 0 and not bpts,
      f"F.Paste flashes {fpaste} vs SMD paste pads {smd_paste} (custom {custom_paste}); B.Paste items {len(bpts)}")

outside = {}
for suffix, p in gpath.items():
    q = [(x, y) for x, y in coords(p)[0] if not (-0.1 <= x <= 90.1 and -0.1 <= y <= 64.1)]
    if q:
        outside[suffix] = q[:3]
check("G4", not outside, f"all Gerber coordinates inside 90x64 outline: {'OK' if not outside else outside}")

job = one(os.path.join(fab, "*-job.gbrjob"))
jd = json.load(open(job, encoding="utf-8")) if job else {}
gs = jd.get("GeneralSpecs", {})
size = gs.get("Size", {})
check("G5", gs.get("LayerNumber") == 2 and abs(gs.get("BoardThickness", 0) - 1.6) < 1e-6
      and abs(size.get("X", 0) - 90) < 0.11 and abs(size.get("Y", 0) - 64) < 0.11,
      f"job file: layers {gs.get('LayerNumber')}, thickness {gs.get('BoardThickness')}, size {size}")

def dark_ops(path):
    """Drawing operations with dark polarity (LPD). Clear-polarity (LPC) items written by
    --subtract-soldermask only erase and print nothing on an otherwise empty layer."""
    pol, n = "D", 0
    for line in open(path, encoding="utf-8", errors="replace"):
        if line.startswith("%LPC"):
            pol = "C"
        elif line.startswith("%LPD"):
            pol = "D"
        elif re.search(r"D0?[123]\*$", line.strip()) and re.match(r"^[XYIJ]", line) and pol == "D":
            n += 1
    return n


bsilk = dark_ops(gpath["B_Silkscreen.gbo"])
fsilk = dark_ops(gpath["F_Silkscreen.gto"])
pcb_txt = open(board_path, encoding="utf-8").read()
check("G6", bsilk == 0 and fsilk > 1000 and '"SENSOR IF + PWR BOARD REV A v1.0"' in pcb_txt and "REV 0.2.0" not in pcb_txt,
      f"B.Silkscreen printing ops {bsilk}; F.Silkscreen printing ops {fsilk}; silk label 'REV A v1.0' present")


def drill(path):
    s = open(path, encoding="utf-8", errors="replace").read()
    tools = {m.group(1): float(m.group(2)) for m in re.finditer(r"^T(\d+)C([\d.]+)", s, re.M)}
    cnt, hits, cur = Counter(), [], None
    for line in s.splitlines():
        m = re.match(r"^T(\d+)$", line)
        if m:
            cur = m.group(1)
            continue
        m = re.match(r"^X(-?[\d.]+)Y(-?[\d.]+)", line)
        if m and cur:
            cnt[round(tools[cur], 3)] += 1
            hits.append((float(m.group(1)), float(m.group(2)), round(tools[cur], 3)))
    return cnt, hits, ("METRIC" in s and "FMAT,2" in s)


exp_pth, exp_npth, holes = Counter(), Counter(), []
for fp in board.GetFootprints():
    for p in fp.Pads():
        d = p.GetDrillSize().x
        if d:
            (exp_npth if p.GetAttribute() == pcbnew.PAD_ATTRIB_NPTH else exp_pth)[round(mm(d), 3)] += 1
            holes.append((mm(p.GetPosition().x) - AX, AY - mm(p.GetPosition().y), round(mm(d), 3)))
for t in board.GetTracks():
    if t.GetClass() == "PCB_VIA":
        exp_pth[round(mm(t.GetDrillValue()), 3)] += 1
        holes.append((mm(t.GetPosition().x) - AX, AY - mm(t.GetPosition().y), round(mm(t.GetDrillValue()), 3)))
pth, ph, pm = drill([p for n, p in files.items() if n.endswith("-PTH.drl")][0])
npth, nh, nm = drill([p for n, p in files.items() if n.endswith("-NPTH.drl")][0])
check("D1", pth == exp_pth, f"PTH by diameter file {dict(pth)} vs board {dict(exp_pth)}")
check("D2", npth == exp_npth == Counter({3.2: 4}), f"NPTH file {dict(npth)} vs board {dict(exp_npth)}")
allhits = ph + nh
unmatched = [h for h in holes if not any(abs(h[0] - x) < 0.005 and abs(h[1] - y) < 0.005 and h[2] == d
                                         for x, y, d in allhits)]
check("D3", pm and nm and not unmatched and len(allhits) == len(holes),
      f"Excellon METRIC/decimal {pm and nm}; hits {len(allhits)} vs board holes {len(holes)}; unmatched {unmatched[:3]}")

cpl_path = one(os.path.join(asm, "*_CPL.csv"))
bom_path = one(os.path.join(asm, "*_BOM.csv"))
cpl = {r["Ref"]: r for r in csv.DictReader(open(cpl_path, encoding="utf-8"))}
bom = list(csv.DictReader(open(bom_path, encoding="utf-8")))
bom_refs, bom_ok, qty_ok, mount_ok = set(), True, True, True
for r in bom:
    refs = r["References"].split()
    bom_refs |= set(refs)
    bom_ok &= bool(r["MPN"]) and bool(r["Manufacturer"])
    qty_ok &= int(r["Qty"]) == len(refs)
    mount_ok &= r["Mount"] in ("SMT", "THT") and r["Side"] == "Top"
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
    if abs(((float(r["Rot"]) - fp.GetOrientationDegrees()) + 180) % 360 - 180) > 0.01:
        bad_rot.append(ref)
    if r["Side"] != "top":
        bad_side.append(ref)
check("C2", not bad_xy, f"CPL X/Y vs board (origin bottom-left, Y up): mismatches {bad_xy}")
check("C3", not bad_rot, f"CPL rotation vs footprint orientation: mismatches {bad_rot}")
check("C4", not bad_side, f"all CPL parts on top: exceptions {bad_side}")
check("B1", bom_ok and len(bom_refs) == 52, f"BOM placements {len(bom_refs)} (expected 52); MPN+Manufacturer on all lines: {bom_ok}")
check("B2", qty_ok and len(bom) == 33, f"BOM lines {len(bom)} (expected 33); Qty = reference count: {qty_ok}")
check("B3", mount_ok, f"every BOM line Mount SMT/THT and Side Top: {mount_ok}")
need_cols = {"Reference": "References", "Qty": "Qty", "Manufacturer": "Manufacturer", "MPN": "MPN",
             "Description": "Description", "Value": "Value", "Package": "Package", "Mount": "Mount", "Side": "Side",
             "DNP": "DNP", "Sourcing": "Sourcing notes (checked 2026-11-09)", "Alternative": "Verified alternative"}
absent_cols = [k for k, c in need_cols.items() if c not in bom[0]]
generic = [r["MPN"] for r in bom if "script generated" in r["Description"] or not r.get(need_cols["Sourcing"])]
check("B4", not absent_cols and not generic,
      f"BOM release columns present (missing {absent_cols}); lines with generic/empty description or notes {generic}")

d356 = one(os.path.join(fab, "*.d356"))
s = open(d356, encoding="utf-8", errors="replace").read()
nets_file = set(re.findall(r"^3\d\d(\S+)", s, re.M))
routed = {t.GetNetname() for t in board.GetTracks() if t.GetNetname()}
missing = sorted(n for n in routed if n[:14] not in {x[:14] for x in nets_file})
check("N1", not missing, f"IPC-D-356 nets {len(nets_file)}; routed nets missing: {missing}")

req = ["3d/*_RevA.step", "assembly/*_assembly_drawing_top.pdf", "assembly/*_assembly_drawing_bottom.pdf",
       "assembly/*_schematic.pdf", "assembly/*_layers.pdf", "fabrication/*-PTH-drl_map.pdf",
       "fabrication/*-NPTH-drl_map.pdf", "fabrication/FABRICATION_NOTES.md", "assembly/ASSEMBLY_NOTES.md"]
absent = [r for r in req if not glob.glob(os.path.join(out_dir, r))]
check("F1", not absent, f"package files present: {'OK' if not absent else absent}")

for cid, ok, msg in res:
    print(f"{cid}: {'PASS' if ok else 'FAIL'}  {msg}")
print(f"RESULT: {'PASS' if all(ok for _, ok, _ in res) else 'FAIL'} ({sum(ok for _, ok, _ in res)}/{len(res)})")
sys.exit(0 if all(ok for _, ok, _ in res) else 1)
