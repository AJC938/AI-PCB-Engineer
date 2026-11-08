"""Generate V0.0.3 custom symbol / footprint MCP test sequences.

Usage: python -I make_custom_part_suite.py <out_dir>
Writes: sym_create.json, sym_reopen.json, fp_create.json, fp_reopen.json
Part: Kingbright WP7113ID (datasheet Spec DSAF0012 Rev V.14A, p.1-2; see datasheets/index.md).
  Datasheet-backed: lead pitch 2.54 mm, recommended hole 0.9 mm x2, body dia 5.0, flange dia 5.9,
  cathode = flat side. Design choices (not from the datasheet): pad 1.8 mm, courtyard +0.25 mm.
Paths are resolved at run time (none stored in git).
"""
import json
import os
import sys

out = sys.argv[1]
repo = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
base = os.path.join(repo, "hardware", "sandbox", "v0.0.3")
sym_dir, fp_dir = os.path.join(base, "custom_symbols"), os.path.join(base, "custom_footprints")
SYMLIB = os.path.join(sym_dir, "AIPCB_Symbols.kicad_sym")
FPLIB = os.path.join(fp_dir, "AIPCB_Footprints.pretty")
FPNAME = "LED_D5.0mm_WP7113ID"
FP_ID = f"AIPCB_Footprints:{FPNAME}"
SYM_ID = "AIPCB_Symbols:LED_WP7113ID"
DS = "https://www.kingbrightusa.com/images/catalog/SPEC/WP7113ID.pdf"

symbol = {
    "libraryPath": SYMLIB, "name": "LED_WP7113ID", "referencePrefix": "D",
    "description": "Red 5 mm THT LED, Kingbright WP7113ID (V0.0.3 custom test symbol)",
    "keywords": "LED red THT 5mm", "datasheet": DS, "footprint": FP_ID, "inBom": True, "onBoard": True,
    "pins": [  # KiCad file convention: angle = direction from the connection point toward the body
        {"name": "K", "number": "1", "type": "passive", "at": {"x": -3.81, "y": 0, "angle": 0}, "length": 1.27},
        {"name": "A", "number": "2", "type": "passive", "at": {"x": 3.81, "y": 0, "angle": 180}, "length": 1.27},
    ],
    "polylines": [  # drawn from scratch: triangle (apex toward K), cathode bar, lead line, two emission arrows
        {"points": [{"x": 1.27, "y": 1.27}, {"x": 1.27, "y": -1.27}, {"x": -1.27, "y": 0}, {"x": 1.27, "y": 1.27}],
         "width": 0.254, "fill": "none"},
        {"points": [{"x": -1.27, "y": 1.27}, {"x": -1.27, "y": -1.27}], "width": 0.254, "fill": "none"},
        {"points": [{"x": -2.54, "y": 0}, {"x": 2.54, "y": 0}], "width": 0, "fill": "none"},
        {"points": [{"x": -0.5, "y": 1.8}, {"x": 0.5, "y": 2.8}], "width": 0, "fill": "none"},
        {"points": [{"x": 0.5, "y": 1.8}, {"x": 1.5, "y": 2.8}], "width": 0, "fill": "none"},
    ],
}

footprint = {
    "libraryPath": FPLIB, "name": FPNAME,
    "description": "Kingbright WP7113ID 5 mm THT LED: pitch 2.54, hole 0.9 (datasheet V.14A p.1); pad 1.7 (edited to 1.8 in test)",
    "tags": "LED THT 5mm WP7113ID",
    "pads": [  # origin = pad 1 (cathode), +X toward the anode, matching KiCad convention
        {"number": "1", "type": "thru_hole", "shape": "rect", "at": {"x": 0, "y": 0}, "size": {"w": 1.7, "h": 1.7}, "drill": 0.9},
        {"number": "2", "type": "thru_hole", "shape": "circle", "at": {"x": 2.54, "y": 0}, "size": {"w": 1.7, "h": 1.7}, "drill": 0.9},
    ],
    # flange dia 5.9 centred at (1.27, 0) -> bounding box x -1.68..4.22, y -2.95..2.95
    "fabLayer": {"x1": -1.68, "y1": -2.95, "x2": 4.22, "y2": 2.95, "width": 0.1},
    "silkscreen": {"x1": -1.8, "y1": -3.07, "x2": 4.34, "y2": 3.07, "width": 0.12},
    "courtyard": {"x1": -1.93, "y1": -3.2, "x2": 4.47, "y2": 3.2, "width": 0.05},
    "refPosition": {"x": 1.27, "y": -4.2}, "valuePosition": {"x": 1.27, "y": 4.2},
}


def circuit(sch, d1_symbol, d1_fp):
    """Same LED circuit and coordinates as V0.0.2, with D1 replaced."""
    S = []
    add = lambda sym, ref, val, x, y, fp=None, ang=0: S.append(
        {"label": f"add_{ref}", "name": "add_schematic_component",
         "arguments": {k: v for k, v in {"schematicPath": sch, "symbol": sym, "reference": ref, "value": val,
                                          "footprint": fp, "position": {"x": x, "y": y}, "angle": ang}.items() if v is not None}})
    add("Connector:Screw_Terminal_01x02", "J1", "5V_IN", 40.64, 80.01,
        "TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal")
    add("Device:R", "R1", "620", 60.96, 80.01, "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal")
    add(d1_symbol, "D1", "WP7113ID", 60.96, 92.71, d1_fp, 90)
    add("power:+5V", "#PWR01", "+5V", 30.48, 74.93)
    add("power:+5V", "#PWR02", "+5V", 60.96, 73.66)
    add("power:GND", "#PWR03", "GND", 33.02, 88.9)
    add("power:GND", "#PWR04", "GND", 60.96, 100.33)
    add("power:PWR_FLAG", "#FLG01", "PWR_FLAG", 66.04, 73.66)
    add("power:PWR_FLAG", "#FLG02", "PWR_FLAG", 66.04, 99.06, None, 180)
    S.append({"label": "pins_D1", "name": "get_schematic_pin_locations", "arguments": {"schematicPath": sch, "reference": "D1"}})
    for i, w in enumerate([[[35.56, 80.01], [30.48, 80.01], [30.48, 74.93]], [[35.56, 82.55], [33.02, 82.55], [33.02, 88.9]],
                           [[60.96, 73.66], [60.96, 76.2]], [[60.96, 76.2], [66.04, 76.2], [66.04, 73.66]],
                           [[60.96, 83.82], [60.96, 88.9]], [[60.96, 96.52], [60.96, 100.33]],
                           [[60.96, 96.52], [66.04, 96.52], [66.04, 99.06]]], 1):
        S.append({"label": f"W{i}", "name": "add_schematic_wire", "arguments": {"schematicPath": sch, "waypoints": w}})
    S.append({"label": "lbl", "name": "add_schematic_net_label", "arguments": {
        "schematicPath": sch, "netName": "LED_A", "labelType": "global_label", "componentRef": "R1", "pinNumber": "2"}})
    for ref, mpn, mfr in (("D1", "WP7113ID", "Kingbright"), ("R1", "MFR-25FBF52-620R", "Yageo"), ("J1", "1715721", "Phoenix Contact")):
        S.append({"label": f"mpn_{ref}", "name": "set_schematic_component_property",
                  "arguments": {"schematicPath": sch, "reference": ref, "name": "MPN", "value": mpn}})
        S.append({"label": f"mfr_{ref}", "name": "set_schematic_component_property",
                  "arguments": {"schematicPath": sch, "reference": ref, "name": "Manufacturer", "value": mfr}})
    return S


def write(name, steps):
    json.dump(steps, open(os.path.join(out, name), "w", encoding="utf-8"), indent=1)
    print("wrote", name, len(steps), "steps")


# ---- Symbol suite (project custom_symbols/sym_test) ----
sp = os.path.join(sym_dir, "sym_test")
s_pro, s_sch = sp + ".kicad_pro", sp + ".kicad_sch"
sym = [
    {"label": "S1", "name": "create_symbol", "arguments": symbol},
    {"label": "S2", "name": "list_symbols_in_library", "arguments": {"libraryPath": SYMLIB}},
    {"label": "S3", "name": "validate_symbol_library", "arguments": {"libraryPath": SYMLIB}},
    {"label": "S4", "name": "create_project", "arguments": {"path": sym_dir, "name": "sym_test"}},
    {"label": "S5", "name": "register_symbol_library", "arguments": {
        "libraryPath": SYMLIB, "libraryName": "AIPCB_Symbols", "scope": "project", "projectPath": s_pro,
        "description": "V0.0.3 custom symbol test library"}},
    {"label": "S6", "name": "batch_list_symbol_pins", "arguments": {"symbols": [SYM_ID, "Device:LED"], "schematicPath": s_sch}},
    {"label": "S7", "name": "get_symbol_info", "arguments": {"symbol": SYM_ID, "projectPath": s_pro}},
] + circuit(s_sch, SYM_ID, "LED_THT:LED_D5.0mm") + [
    {"label": "S8", "name": "validate_schematic", "arguments": {"schematicPath": s_sch}},
    {"label": "S9", "name": "run_erc", "arguments": {"schematicPath": s_sch}},
    {"label": "S10", "name": "generate_netlist", "arguments": {"schematicPath": s_sch}},
]
sym_reopen = [
    {"label": "R1", "name": "list_schematic_components", "arguments": {"schematicPath": s_sch, "filter": {"referencePrefix": "D"}}},
    {"label": "R2", "name": "get_schematic_pin_locations", "arguments": {"schematicPath": s_sch, "reference": "D1"}},
    {"label": "R3", "name": "run_erc", "arguments": {"schematicPath": s_sch}},
    {"label": "R4", "name": "generate_netlist", "arguments": {"schematicPath": s_sch}},
    {"label": "R5", "name": "export_netlist", "arguments": {"schematicPath": s_sch, "outputPath": os.path.join(sym_dir, "out", "sym_test_mcp.net")}},
]

# ---- Footprint suite (project custom_footprints/fp_test) ----
fpp = os.path.join(fp_dir, "fp_test")
f_pro, f_sch, f_pcb = fpp + ".kicad_pro", fpp + ".kicad_sch", fpp + ".kicad_pcb"
FPFILE = os.path.join(FPLIB, FPNAME + ".kicad_mod")
fpsteps = [
    {"label": "F1", "name": "create_footprint", "arguments": footprint},
    {"label": "F2a", "name": "edit_footprint_pad", "arguments": {"footprintPath": FPFILE, "padNumber": "1", "size": {"w": 1.8, "h": 1.8}}},
    {"label": "F2b", "name": "edit_footprint_pad", "arguments": {"footprintPath": FPFILE, "padNumber": "2", "size": {"w": 1.8, "h": 1.8}}},
    {"label": "F3", "name": "add_footprint_3d_model", "arguments": {
        "footprintPath": FPFILE, "modelPath": "${KICAD10_3DMODEL_DIR}/LED_THT.3dshapes/LED_D5.0mm.step"}},
    {"label": "F4", "name": "create_project", "arguments": {"path": fp_dir, "name": "fp_test"}},
    {"label": "F5a", "name": "register_footprint_library", "arguments": {
        "libraryPath": FPLIB, "libraryName": "AIPCB_Footprints", "scope": "project", "projectPath": f_pro,
        "description": "V0.0.3 custom footprint test library"}},
    {"label": "F5b", "name": "register_symbol_library", "arguments": {
        "libraryPath": SYMLIB, "libraryName": "AIPCB_Symbols", "scope": "project", "projectPath": f_pro}},
    {"label": "F6", "name": "get_footprint_info", "arguments": {"library_name": "AIPCB_Footprints", "footprint_name": FPNAME}},
] + circuit(f_sch, SYM_ID, FP_ID) + [
    {"label": "F7", "name": "run_erc", "arguments": {"schematicPath": f_sch}},
    {"label": "F8", "name": "sync_schematic_to_board", "arguments": {"schematicPath": f_sch, "boardPath": f_pcb}},
    {"label": "F9", "name": "open_project", "arguments": {"filename": f_pro}},
    {"label": "F10", "name": "set_design_rules", "arguments": {"clearance": 0.25, "minTrackWidth": 0.25, "trackWidth": 0.5,
                                                               "minHoleDiameter": 0.3, "courtyardClearance": 0.25}},
    {"label": "F11", "name": "add_board_outline", "arguments": {"shape": "rounded_rectangle", "params": {
        "x": 100, "y": 100, "width": 50, "height": 30, "cornerRadius": 1, "unit": "mm"}}},
    {"label": "F12a", "name": "move_component", "arguments": {"reference": "J1", "position": {"x": 105.6, "y": 112.46, "unit": "mm"}, "rotation": 270}},
    {"label": "F12b", "name": "move_component", "arguments": {"reference": "R1", "position": {"x": 115, "y": 110, "unit": "mm"}, "rotation": 0}},
    {"label": "F12c", "name": "move_component", "arguments": {"reference": "D1", "position": {"x": 135, "y": 117.54, "unit": "mm"}, "rotation": 90}},
    {"label": "F13", "name": "get_component_pads", "arguments": {"reference": "D1"}},
    {"label": "F14a", "name": "route_pad_to_pad", "arguments": {"fromRef": "J1", "fromPad": "1", "toRef": "R1", "toPad": "1", "layer": "F.Cu", "width": 0.5}},
    {"label": "F14b", "name": "route_pad_to_pad", "arguments": {"fromRef": "R1", "fromPad": "2", "toRef": "D1", "toPad": "2", "layer": "F.Cu", "width": 0.5}},
    {"label": "F14c", "name": "route_pad_to_pad", "arguments": {"fromRef": "D1", "fromPad": "1", "toRef": "J1", "toPad": "2", "layer": "B.Cu", "width": 0.5}},
    {"label": "F15", "name": "save_project"},
    {"label": "F16", "name": "run_drc", "arguments": {"reportPath": os.path.join(fp_dir, "out", "drc_mcp.rpt")}},
]
fp_reopen = [
    {"label": "P1", "name": "open_project", "arguments": {"filename": f_pro}},
    {"label": "P2", "name": "get_component_properties", "arguments": {"reference": "D1"}},
    {"label": "P3", "name": "get_component_pads", "arguments": {"reference": "D1"}},
    {"label": "P4", "name": "get_ratsnest"},
    {"label": "P5", "name": "export_gerbers", "arguments": {"boardPath": f_pcb, "outputDir": os.path.join(fp_dir, "out", "gerber"),
                                                            "layers": ["F.Cu", "B.Cu", "F.SilkS", "F.Mask", "Edge.Cuts"]}},
    {"label": "P6", "name": "export_drill", "arguments": {"boardPath": f_pcb, "outputDir": os.path.join(fp_dir, "out", "gerber"),
                                                          "excellonUnits": "mm", "excellonSeparateTh": True}},
    {"label": "P7", "name": "get_board_2d_view", "arguments": {"pcbPath": f_pcb, "responseMode": "file", "format": "png"}},
]
for d in (sym_dir, fp_dir):
    os.makedirs(os.path.join(d, "out"), exist_ok=True)
write("sym_create.json", sym)
write("sym_reopen.json", sym_reopen)
write("fp_create.json", fpsteps)
write("fp_reopen.json", fp_reopen)
