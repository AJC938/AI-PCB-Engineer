"""Controlled non-MCP edit: mark PCB-feature symbols (mounting holes, fiducials, solder jumpers) as not in BOM.

Why: MCP add_schematic_component always writes (in_bom yes); no MCP tool sets the flag (V0.2.0 finding).
The footprints of these parts already carry exclude_from_bom, so KiCad's DRC schematic parity reports
"Exclude from bill of materials settings differ". Only the (in_bom ...) token inside the named symbol
instances is changed; counts and parenthesis balance are asserted; the result is validated by MCP
validate_schematic and kicad-cli ERC afterwards.
Usage: python -I set_bom_flags.py <file.kicad_sch>
"""
import re
import sys

REFS = {"H1", "H2", "H3", "H4", "FID1", "FID2", "FID3", "JP1", "JP2"}
path = sys.argv[1]
s = open(path, encoding="utf-8").read()   # text mode: CRLF read as LF; written back as LF


def blocks(text):
    # placed-symbol instances in both writer styles: "\t(symbol\n\t\t(lib_id" (KiCad) and "\t  (symbol (lib_id" (MCP)
    for m in re.finditer(r"\n[\t ]+\(symbol\s+\(lib_id", text):
        i = text.index("(symbol", m.start())
        j, d = i, 0
        while True:
            c = text[j]
            if c == "(":
                d += 1
            elif c == ")":
                d -= 1
                if d == 0:
                    break
            j += 1
        yield i, j + 1


changed, out, last = set(), [], 0
for a, b in blocks(s):
    blk = s[a:b]
    m = re.search(r'\(property "Reference" "([^"]+)"', blk)
    if m and m.group(1) in REFS:
        n = blk.count("(in_bom yes)")
        assert n == 1, (m.group(1), n)
        blk = blk.replace("(in_bom yes)", "(in_bom no)", 1)
        changed.add(m.group(1))
    out.append(s[last:a])
    out.append(blk)
    last = b
out.append(s[last:])
new = "".join(out)
assert changed == REFS, f"not found: {sorted(REFS - changed)}"
assert new.count("(") == new.count(")")
open(path, "w", encoding="utf-8", newline="\n").write(new)
print("in_bom no set for:", sorted(changed))
