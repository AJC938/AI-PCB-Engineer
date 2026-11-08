"""Collect and sanitize V0.0.3 evidence into reports/v0.0.3/evidence/.

Usage: python -I collect_evidence.py <scratchpad_dir_with_run_logs>
Sanitizing: user profile paths become %USERPROFILE%; any path to a non-sandbox personal
project is redacted; the GUI tree's "Open Recent" submenu (recent-file paths) is dropped.
"""
import json
import os
import re
import shutil
import sys

S = sys.argv[1]
repo = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sb = os.path.join(repo, "hardware", "sandbox", "v0.0.3")
ev = os.path.join(repo, "reports", "v0.0.3", "evidence")
user = os.path.basename(os.path.expanduser("~"))


def clean(text):
    for sep in ("\\\\\\\\", "\\\\", "\\", "/"):
        text = text.replace(f"C:{sep}Users{sep}{user}", "%USERPROFILE%")
    text = re.sub(r"%USERPROFILE%[\\/]+OneDrive[^\"'\n,\]]*", "<redacted personal path>", text)
    return text.replace(user, "<user>")


def drop_recent(obj):
    if isinstance(obj, dict):
        if obj.get("name") == "Open Recent":
            return {"name": "Open Recent", "children": "<redacted: recent-file list>"}
        return {k: drop_recent(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [drop_recent(x) for x in obj]
    return obj


def put(src, rel, text=True):
    dst = os.path.join(ev, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if text:
        open(dst, "w", encoding="utf-8", newline="\n").write(clean(open(src, encoding="utf-8").read()))
    else:
        shutil.copyfile(src, dst)
    print("  ", rel)


print("runs/")
for name in ["run_swig", "run_ipc", "run_ipc_extra", "run_sym_create", "run_sym_reopen", "run_symlookup",
             "run_symlookup2", "run_fp_create", "run_fp_reopen", "run_gui_install", "run_gui1", "run_gui2", "run_gui3"]:
    log = json.load(open(os.path.join(S, name + ".json"), encoding="utf-8"))
    log.pop("stderr_tail", None)
    for st in log.get("steps", []):
        if st["name"] == "kicad_gui_tree":
            try:
                st["text"] = json.dumps(drop_recent(json.loads(st["text"])), ensure_ascii=False, indent=1)
            except Exception:
                st["text"] = "<unparseable tree removed>"
        if st["name"] == "kicad_pcb_snapshot":
            st["text"] += "  [image deleted: it captured an unrelated foreground application; see GUI_DRIVER_EVALUATION.md]"
    dst = os.path.join(ev, "runs", name + ".json")
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    open(dst, "w", encoding="utf-8", newline="\n").write(clean(json.dumps(log, indent=1, ensure_ascii=False)))
    print("   runs/" + name + ".json")

print("checks/")
for rel_src, rel_dst in [
    ("swig/out/drc_cli_norefill.json", "checks/swig_drc_cli_norefill.json"),
    ("swig/out/drc_cli_refill.json", "checks/swig_drc_cli_refill.json"),
    ("swig/out/drc_cli_final.json", "checks/swig_drc_cli_final.json"),
    ("ipc/out/drc_cli_final.json", "checks/ipc_drc_cli_final.json"),
    ("ipc/out/drc_cli_norefill_after_ipcfill.json", "checks/ipc_drc_cli_norefill_after_ipcfill.json"),
    ("custom_symbols/out/erc_cli.json", "checks/sym_test_erc_cli.json"),
    ("custom_symbols/out/sym_test_cli.net", "checks/sym_test_cli.net"),
    ("custom_symbols/out/sym_test_mcp.net", "checks/sym_test_mcp.net"),
    ("custom_footprints/out/drc_cli.json", "checks/fp_test_drc_cli.json"),
    ("custom_footprints/out/gerber/fp_test-PTH.drl", "checks/fp_test-PTH.drl"),
]:
    put(os.path.join(sb, rel_src), rel_dst)

print("libraries/ and kicad/")
for rel_src, rel_dst in [
    ("custom_symbols/AIPCB_Symbols.kicad_sym", "libraries/AIPCB_Symbols.kicad_sym"),
    ("custom_footprints/AIPCB_Footprints.pretty/LED_D5.0mm_WP7113ID.kicad_mod",
     "libraries/AIPCB_Footprints.pretty/LED_D5.0mm_WP7113ID.kicad_mod"),
    ("custom_symbols/sym-lib-table", "libraries/sym_test.sym-lib-table.sanitized"),
    ("custom_footprints/fp-lib-table", "libraries/fp_test.fp-lib-table.sanitized"),
    ("custom_symbols/sym_test.kicad_sch", "kicad/sym_test.kicad_sch"),
    ("custom_footprints/fp_test.kicad_sch", "kicad/fp_test.kicad_sch"),
    ("custom_footprints/fp_test.kicad_pcb", "kicad/fp_test.kicad_pcb"),
    ("swig/led_test.kicad_pcb", "kicad/swig_after_suite.kicad_pcb"),
    ("ipc/led_test.kicad_pcb", "kicad/ipc_after_suite.kicad_pcb"),
]:
    put(os.path.join(sb, rel_src), rel_dst)

print("images/")
for rel_src, rel_dst in [
    ("custom_symbols/out/symbol_only.png", "images/custom_symbol.png"),
    ("custom_symbols/out/sym_test_crop.png", "images/sym_test_schematic_crop.png"),
    ("custom_footprints/out/footprint_only.png", "images/custom_footprint.png"),
    ("custom_footprints/out/fp_test_3d.png", "images/fp_test_3d.png"),
    ("custom_footprints/fp_test_2d_view.png", "images/fp_test_2d_view_mcp.png"),
]:
    put(os.path.join(sb, rel_src), rel_dst, text=False)

print("config_restore/")
for n in ("kicad_cfg_manifest_before.txt", "kicad_cfg_manifest_final.txt"):
    put(os.path.join(S, n), "config_restore/" + n)
