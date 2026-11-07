"""Independent inspection of KiCad fabrication outputs (Gerber X2, Excellon, BOM, CPL).

Usage: python -I inspect_fab_outputs.py <fab_dir> <project_name>
Parses the files directly (no KiCad, no MCP) and prints board extents, pad flashes,
drill tools/hit counts, BOM rows and CPL rows so they can be checked against the design.
"""
import csv
import os
import re
import sys
from collections import Counter

fab, name = sys.argv[1], sys.argv[2]
g = os.path.join(fab, "gerber")


def gerber_coords(path):
    s = open(path, encoding="utf-8", errors="replace").read()
    fmt = re.search(r"%FSLAX(\d)(\d)Y", s)
    dec = int(fmt.group(2)) if fmt else 6
    pts, flashes, ap, aps = [], [], None, {}
    for m in re.finditer(r"%ADD(\d+)([A-Za-z0-9_]+),?([^*]*)\*%", s):
        aps[m.group(1)] = (m.group(2), m.group(3))
    x = y = 0.0
    for line in s.split("*"):
        line = line.strip().lstrip("%").strip()
        m = re.match(r"^D(\d{2,})$", line)
        if m and int(m.group(1)) >= 10:
            ap = m.group(1)
            continue
        m = re.match(r"^(?:X(-?\d+))?(?:Y(-?\d+))?(?:I-?\d+J-?\d+)?D0([123])$", line)
        if m:
            if m.group(1) is not None:
                x = int(m.group(1)) / 10 ** dec
            if m.group(2) is not None:
                y = int(m.group(2)) / 10 ** dec
            pts.append((x, y))
            if m.group(3) == "3":
                flashes.append((round(x, 3), round(-y, 3), aps.get(ap, ("?", ""))))
    return pts, flashes, s


print("== Gerber files")
for f in sorted(os.listdir(g)):
    print("  ", f, os.path.getsize(os.path.join(g, f)), "bytes")

pts, _, s = gerber_coords(os.path.join(g, f"{name}-Edge_Cuts.gm1"))
xs, ys = [p[0] for p in pts], [p[1] for p in pts]
print(f"\n== Edge.Cuts extents: X {min(xs):.3f}..{max(xs):.3f}  Y {-max(ys):.3f}..{-min(ys):.3f}"
      f"  -> {max(xs) - min(xs):.3f} x {max(ys) - min(ys):.3f} mm")
print("   file function:", re.findall(r"%TF\.FileFunction,([^*]*)\*%", s))

for layer in ("F_Cu.gtl", "B_Cu.gbl"):
    _, fl, s = gerber_coords(os.path.join(g, f"{name}-{layer}"))
    print(f"\n== {layer}: {len(fl)} pad flashes  (FileFunction {re.findall(r'%TF.FileFunction,([^*]*)', s)})")
    for x, y, a in sorted(fl):
        print(f"   ({x:8.3f}, {y:8.3f})  aperture {a[0]} {a[1]}")
    print("   TO.N nets referenced:", sorted(set(re.findall(r"%TO\.N,([^*]*)\*%", s))))

print("\n== Drill files")
for f in sorted(os.listdir(g)):
    if f.endswith(".drl"):
        s = open(os.path.join(g, f)).read()
        tools = dict(re.findall(r"^(T\d+)C([\d.]+)", s, re.M))
        hits, cur = Counter(), None
        for line in s.splitlines():
            if re.match(r"^T\d+$", line):
                cur = line
            elif line.startswith("X") and cur:
                hits[cur] += 1
        print(f"   {f}: units={'METRIC' if 'METRIC' in s else 'INCH?'} " +
              ", ".join(f"{t} Ø{tools[t]} mm x{hits[t]}" for t in tools))

for label, fn in (("BOM (schematic)", f"{name}-bom.csv"), ("BOM (from PCB, MCP export_bom)", f"{name}-bom-from-pcb.csv"),
                  ("CPL", f"{name}-cpl.csv")):
    p = os.path.join(fab, fn)
    print(f"\n== {label}: {fn}")
    for row in csv.reader(open(p, encoding="utf-8")):
        print("   ", row)
