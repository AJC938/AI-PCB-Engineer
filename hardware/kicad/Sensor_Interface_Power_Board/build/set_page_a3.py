"""Controlled non-MCP edit: set paper to A3 and fill the title block of a freshly created schematic.

Why: no MCP tool sets paper size or title block (V0.1.0 finding). The edit touches only the
(paper ...) token and inserts/replaces (title_block ...); the result is verified by re-parsing and by
kicad-cli loading the file (validate step in the MCP build sequence).
Usage: python -I set_page_a3.py <file.kicad_sch> <title> <rev> <date>
"""
import re
import sys

path, title, rev, date = sys.argv[1:5]
s = open(path, encoding="utf-8").read()
n_paper = len(re.findall(r'\(paper "[^"]+"\)', s))
assert n_paper == 1, f"expected one paper token, found {n_paper}"
s = re.sub(r'\(paper "[^"]+"\)', '(paper "A3")', s)
tb = (f'(title_block\n\t\t(title "{title}")\n\t\t(date "{date}")\n\t\t(rev "{rev}")\n'
      f'\t\t(company "AI-PCB-Engineer")\n\t\t(comment 1 "Architecture B: ESP32 DevKit on its own USB; board powers peripherals")\n'
      f'\t\t(comment 2 "V0.2.0: eFuse power entry (DDR-17), TRIG series R15 (DDR-18)")\n\t)')
if "(title_block" in s:
    s = re.sub(r"\(title_block.*?\n\t\)", tb, s, count=1, flags=re.S)
else:
    s = s.replace('(paper "A3")', '(paper "A3")\n\t' + tb, 1)
assert s.count("(") == s.count(")"), "unbalanced parentheses after edit"
open(path, "w", encoding="utf-8", newline="\n").write(s)
print("paper A3 + title block set:", path)
