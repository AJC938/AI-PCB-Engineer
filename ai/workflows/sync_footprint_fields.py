"""Copy custom symbol fields (e.g. MPN, Manufacturer) from a KiCad XML netlist into PCB footprints.

Why: KiCAD-MCP-Server v2.8.3 `sync_schematic_to_board` does not transfer custom fields, and
no MCP tool writes custom footprint fields. KiCad's DRC schematic-parity check then reports
`footprint_symbol_field_mismatch`. This is a NON-MCP workaround using KiCad's own pcbnew API.

Usage (KiCad's bundled Python; the board must NOT be open in KiCad):
  "%LOCALAPPDATA%\\Programs\\KiCad\\10.0\\bin\\python.exe" -I sync_footprint_fields.py \
      <board.kicad_pcb> <netlist.xml from `kicad-cli sch export netlist --format kicadxml`> \
      [FIELD ...]            (default fields: MPN Manufacturer)
After running, reload the board in any open MCP session (open_project).
"""
import sys
import xml.etree.ElementTree as ET

import pcbnew


def main():
    board_path, netlist_path = sys.argv[1], sys.argv[2]
    fields = sys.argv[3:] or ["MPN", "Manufacturer"]
    comps = {}
    for comp in ET.parse(netlist_path).getroot().iter("comp"):
        vals = {f.get("name"): (f.text or "") for f in comp.iter("field")}
        comps[comp.get("ref")] = {k: vals[k] for k in fields if k in vals}

    board = pcbnew.LoadBoard(board_path)
    changed = 0
    for fp in board.GetFootprints():
        ref = fp.GetReference()
        for name, value in comps.get(ref, {}).items():
            if fp.HasField(name) and fp.GetFieldText(name) == value:
                continue
            fp.SetField(name, value)
            fld = fp.GetField(name)
            fld.SetVisible(False)
            fld.SetLayer(pcbnew.F_Fab)
            changed += 1
            print(f"{ref}: {name} = {value}")
    if changed:
        pcbnew.SaveBoard(board_path, board)
    print(f"fields written: {changed}")


if __name__ == "__main__":
    main()
