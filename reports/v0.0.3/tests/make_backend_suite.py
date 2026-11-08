"""Generate the V0.0.3 backend comparison sequence (identical steps for SWIG and IPC).

Usage: python -I make_backend_suite.py <backend: swig|ipc> <out.json>
The test project is hardware/sandbox/v0.0.3/<backend>/led_test.* , a byte-identical copy
of the V0.0.2 evidence snapshot. Paths are resolved at run time (none stored in git).
"""
import json
import os
import sys

backend, out = sys.argv[1], sys.argv[2]
repo = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
d = os.path.join(repo, "hardware", "sandbox", "v0.0.3", backend)
pro, sch, pcb = (os.path.join(d, f"led_test.{e}") for e in ("kicad_pro", "kicad_sch", "kicad_pcb"))
fp = "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal"

steps = [
    {"label": "T1a", "name": "check_kicad_ui"},
    {"label": "T1b", "name": "get_backend_state"},
    {"label": "T3", "name": "open_project", "arguments": {"filename": pro}},
    {"label": "T2", "name": "get_backend_state"},
    {"label": "T4", "name": "list_schematic_components", "arguments": {"schematicPath": sch}},
    {"label": "T5a", "name": "get_component_list"},
    {"label": "T5b", "name": "get_nets_list", "arguments": {"includeStats": True}},
    {"label": "T6a", "name": "get_board_info"},
    {"label": "T6b", "name": "get_layer_list"},
    {"label": "T6c", "name": "query_traces"},
    {"label": "T7", "name": "place_component",
     "arguments": {"componentId": fp, "footprint": fp, "reference": "R2", "value": "TEST",
                   "position": {"x": 125, "y": 122, "unit": "mm"}, "rotation": 0}},
    {"label": "T8a", "name": "rotate_component", "arguments": {"reference": "R2", "angle": 180}},
    {"label": "T8b", "name": "edit_component", "arguments": {"reference": "R2", "value": "1k"}},
    {"label": "T8c", "name": "get_component_properties", "arguments": {"reference": "R2"}},
    {"label": "T9", "name": "save_project"},
    {"label": "T10a", "name": "open_project", "arguments": {"filename": pro}},
    {"label": "T10b", "name": "get_component_properties", "arguments": {"reference": "R2"}},
    {"label": "T10c", "name": "get_backend_state"},
    {"label": "T11", "name": "run_drc", "arguments": {"reportPath": os.path.join(d, "out", "drc_mcp.rpt")}},
    {"label": "T12", "name": "export_gerbers",
     "arguments": {"boardPath": pcb, "outputDir": os.path.join(d, "out", "gerber"),
                   "layers": ["F.Cu", "B.Cu", "F.SilkS", "Edge.Cuts"]}},
]
os.makedirs(os.path.join(d, "out"), exist_ok=True)
json.dump(steps, open(out, "w", encoding="utf-8"), indent=1)
print("wrote", out, len(steps), "steps for", d)
