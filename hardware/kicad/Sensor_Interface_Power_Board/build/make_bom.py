"""Assembly BOM for V0.2.0: schematic fields (kicad-cli netlist) + PCB mount type/side (pcbnew, read-only).

Columns: Item, Qty, References, Value, Description, Manufacturer, MPN, Package, Mount (SMT/THT), Side, DNP,
Substitution. Parts with in_bom=no (mounting holes, fiducials, solder jumpers) are excluded and listed as
PCB features. Every line carries "NO SUBSTITUTION without written approval" (DFA requirement).
Usage: python -I make_bom.py <netlist.xml> <board.kicad_pcb> <out.csv>   (KiCad's bundled Python)
"""
import csv
import sys
import xml.etree.ElementTree as ET
from collections import OrderedDict

import pcbnew

net_xml, board_path, out = sys.argv[1:4]
board = pcbnew.LoadBoard(board_path)
fpinfo = {}
for fp in board.GetFootprints():
    a = fp.GetAttributes()
    mount = "THT" if a & pcbnew.FP_THROUGH_HOLE else ("SMT" if a & pcbnew.FP_SMD else "OTHER")
    fpinfo[fp.GetReference()] = dict(mount=mount, side="Top" if fp.GetLayer() == pcbnew.F_Cu else "Bottom",
                                     pkg=fp.GetFPID().GetLibItemName().wx_str(),
                                     dnp=bool(fp.IsDNP()) if hasattr(fp, "IsDNP") else False,
                                     no_bom=bool(a & pcbnew.FP_EXCLUDE_FROM_BOM))

groups = OrderedDict()
features = []
for comp in ET.parse(net_xml).getroot().iter("comp"):
    ref = comp.get("ref")
    f = {x.get("name"): (x.text or "") for x in comp.iter("field")}
    props = {p.get("name"): p.get("value") for p in comp.iter("property")}
    if "exclude_from_bom" in props or fpinfo[ref]["no_bom"]:
        features.append(ref)
        continue
    key = (f.get("MPN", ""), comp.findtext("value"), fpinfo[ref]["pkg"])
    g = groups.setdefault(key, dict(refs=[], value=comp.findtext("value"), desc=f.get("Description", ""),
                                    mfr=f.get("Manufacturer", ""), mpn=f.get("MPN", ""), **fpinfo[ref]))
    g["refs"].append(ref)


def natural(r):
    import re
    m = re.match(r"([A-Z]+)(\d+)", r)
    return (m.group(1), int(m.group(2))) if m else (r, 0)


rows = sorted(groups.values(), key=lambda g: natural(sorted(g["refs"], key=natural)[0]))
with open(out, "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["Item", "Qty", "References", "Value", "Description", "Manufacturer", "MPN", "Package", "Mount",
                "Side", "DNP", "Substitution"])
    for i, g in enumerate(rows, 1):
        refs = sorted(g["refs"], key=natural)
        assert g["mpn"] and g["mfr"], refs
        w.writerow([i, len(refs), " ".join(refs), g["value"], g["desc"], g["mfr"], g["mpn"], g["pkg"], g["mount"],
                    g["side"], "No" if not g["dnp"] else "Yes", "NO SUBSTITUTION without written approval"])
n = sum(len(g["refs"]) for g in rows)
print(f"BOM lines {len(rows)}, placements {n} (SMT {sum(len(g['refs']) for g in rows if g['mount']=='SMT')}, "
      f"THT {sum(len(g['refs']) for g in rows if g['mount']=='THT')}); PCB features excluded: {sorted(features, key=natural)}")
