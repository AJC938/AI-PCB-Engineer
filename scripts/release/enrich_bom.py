"""Add release columns to the generated BOM without changing any part data.

Replaces the generic KiCad library 'Description' with an engineering description and adds
'Sourcing notes (checked 2026-11-09)' and 'Verified alternative' from scripts/release/bom_enrichment.csv
(keyed by MPN). References, quantities, values, manufacturers, MPNs, packages and mount types are untouched;
the script fails if any MPN has no enrichment row.
Usage: python -I enrich_bom.py <BOM.csv>   (rewrites the file in place)
"""
import csv
import os
import sys

bom_path = sys.argv[1]
src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bom_enrichment.csv")
data = {r["MPN"]: r for r in csv.DictReader(open(src, encoding="utf-8"))}
rows = list(csv.DictReader(open(bom_path, encoding="utf-8")))
NOTE, ALT = "Sourcing notes (checked 2026-11-09)", "Verified alternative"
cols = ["Item", "Qty", "References", "Value", "Description", "Manufacturer", "MPN", "Package", "Mount", "Side", "DNP",
        NOTE, ALT, "Substitution"]
missing = sorted({r["MPN"] for r in rows} - set(data))
if missing:
    sys.exit(f"ABORT: no enrichment for {missing}")
with open(bom_path, "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=cols)
    w.writeheader()
    for r in rows:
        e = data[r["MPN"]]
        r["Description"] = e["Description"]
        r[NOTE], r[ALT] = e[NOTE], e[ALT]
        w.writerow({c: r[c] for c in cols})
print(f"BOM enriched: {len(rows)} lines, {sum(int(r['Qty']) for r in rows)} placements")
