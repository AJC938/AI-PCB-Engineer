# GUI Driver Evaluation — V0.0.3

## Support status (from source and docs)
- Present in v2.8.3 as the opt-in `gui-driver` toolbox (11 tools): `install_gui_driver`,
  `kicad_gui_tree`, `kicad_gui_click`, `kicad_run_action_plugin`, `kicad_gui_wait_for`,
  `kicad_gui_screenshot`, `kicad_pcb_snapshot`, `kicad_reload_and_open_plugin`, `kicad_run_drc`,
  `kicad_gui_tree_atspi`, `kicad_gui_click_atspi`.
- Two backends (`docs/GUI_DRIVER_SPEC.md`): **A**, an in-process wx helper plugin (cross-platform), and
  **B**, AT-SPI, which is **Linux-only**. On Windows only backend A applies.
- Helper metadata: status `development`, declared `kicad_version 9.0`, GPL-3.0. Listens on
  127.0.0.1:8770 (default) with a per-session token file.
- Requirements: the helper is copied into KiCad's plugin tree, and `KICAD_GUI_DRIVER_ENABLE=1` is set in KiCad's environment.

## Safety conditions applied
The user approved a temporary install. The user closed their own KiCad first. The test launched
its own `pcbnew.exe` on an identical sandbox copy, with the enable variable set for that process only.
After the test the plugin, the token file and the created `3rdparty/` and `scripting/` folders were
removed, and the KiCad config folder was verified byte-identical to the pre-test backup.

## Results
| # | Capability | Tool | Result | Evidence / observation |
|---|---|---|---|---|
| 0 | Install helper | install_gui_driver | **FAIL (Windows)** | installed to `%APPDATA%\kicad\10.0\3rdparty\plugins\…`. KiCad 10's `pcbnew.LoadPlugins` does **not** search that folder (it searches `<config>\scripting\plugins`, the user scripting path, and `KICAD_3RD_PARTY\plugins`, which is under *Documents*). Result: no token or listener after 60 s (D-20) |
| 0b | Workaround | manual copy to `%APPDATA%\kicad\10.0\scripting\plugins\…` (searched path) | **PASS** | token written after 5.2 s. Listener on **127.0.0.1:8770** owned by the test's pcbnew |
| 1 | Detect UI state | kicad_gui_wait_for (+ core check_kicad_ui) | **PASS** | found "led_test — PCB Editor" in 4.3 s |
| 2 | Interact with the intended window | kicad_gui_tree | **PASS / WARNING** | `PcbFrame` menus enumerated with wx IDs, destructive items flagged `⚠`. **0 AUI toolbars** returned. The tree **exposes the recent-files list** (user paths), so it was redacted in the evidence |
| 3 | Open the isolated project | (not through the driver) | **NOT TESTED** | the board was opened by the launch argument. Opening via File→Open would show a dialog in the user's active desktop session |
| 4 | Inspect PCB content | kicad_pcb_snapshot | **FAIL (privacy)** | the image captured **a different application that was in the foreground** in the same screen rectangle. It was deleted immediately and is not in the evidence. The tool grabs screen pixels, not the window's contents (D-22) |
| 4b | Inspect via GUI DRC | kicad_run_drc | **BLOCKED** | opens a modal dialog. Not run because the user was actively using another application in the foreground |
| 5 | Simple reversible UI action | kicad_gui_click "Zoom to Fit", "Zoom In" (id 20504) | **FAIL** | `success: true` but **`processed: false`**. In `driver.py`, `processed = frame.ProcessEvent(evt)`, so no handler handled the event. No observable effect could be verified without screenshots (D-21) |
| 6 | Save and verify | kicad_gui_click "Save" (id 20414) | **FAIL** | `processed: false`. Board file sha256 and mtime **unchanged** |

## Assessment
On Windows with KiCad 10.0.8 the GUI driver is **not usable**:
- The installer targets the wrong folder.
- Menu activation is not handled.
- Screenshots are a privacy hazard on a shared desktop.

Only read-only UI introspection (`wait_for`, `tree`) worked, after a manual install workaround.
It adds nothing the design workflow needs, because the SWIG and kicad-cli path already covers design
content headlessly.

**Recommendation:** do not use the GUI driver in this project. If it is ever re-evaluated, use a
dedicated or locked desktop session, never on the user's active desktop.
