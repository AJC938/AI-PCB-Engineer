# Evidence Index — V0.0.3

All files are under [`evidence/`](evidence/). User-profile paths are replaced with `%USERPROFILE%`.
Personal project paths and the GUI recent-files list are redacted. Total about 0.75 MB, 39 files.
Reproduction scripts are in [`tests/`](tests/) and [`ai/workflows/mcp_harness.py`](../../ai/workflows/mcp_harness.py).

| File | Proves |
|---|---|
| `runs/run_swig.json` | SWIG suite: 20 calls, responses, latency |
| `runs/run_ipc.json` | IPC suite: same 20 calls. Silent wrong reads (0 components), "R2 not found" failures, latency |
| `runs/run_ipc_extra.json` | IPC text, zone refill and save succeeded |
| `runs/run_sym_create.json`, `run_sym_reopen.json` | Custom symbol creation, registration, placement, wiring, ERC, netlist. Persistence in a fresh process |
| `runs/run_symlookup.json`, `run_symlookup2.json` | D-12 (stale library cache) and D-13 (search timeout) |
| `runs/run_fp_create.json`, `run_fp_reopen.json` | Custom footprint create/edit/3D/register, board integration, D-1 recurrence, persistence |
| `runs/run_gui_install.json` | `install_gui_driver` target folder (D-20) |
| `runs/run_gui1.json` | GUI `wait_for`, `tree` (recent files redacted), snapshot call (image deleted, D-22) |
| `runs/run_gui2.json`, `run_gui3.json` | `kicad_gui_click` → `processed:false` for Zoom and Save (D-21) |
| `checks/swig_drc_cli_norefill.json` / `_refill.json` | 6 errors come from the stale zone only (D-10) |
| `checks/swig_drc_cli_final.json`, `ipc_drc_cli_final.json` | Final SWIG and IPC boards equivalent under CLI DRC |
| `checks/ipc_drc_cli_norefill_after_ipcfill.json` | IPC `refill_zones` really refilled (0 violations without CLI refill) |
| `checks/sym_test_erc_cli.json`, `sym_test_cli.net`, `sym_test_mcp.net` | ERC 0. Nets identical between MCP and CLI. Custom libsource |
| `checks/fp_test_drc_cli.json` | Custom-footprint board: 0 violations, 0 unconnected, no library issues, parity = MPN only |
| `checks/fp_test-PTH.drl` | Ø0.9 holes at the custom-footprint pad positions |
| `libraries/AIPCB_Symbols.kicad_sym` | The symbol as written by `create_symbol` |
| `libraries/AIPCB_Footprints.pretty/LED_D5.0mm_WP7113ID.kicad_mod` | The footprint after `create_footprint` + `edit_footprint_pad` + `add_footprint_3d_model` |
| `libraries/*.sanitized` | Project lib tables. The originals hold absolute user paths (D-11) |
| `kicad/sym_test.kicad_sch`, `fp_test.kicad_sch`, `fp_test.kicad_pcb` | Final test designs |
| `kicad/swig_after_suite.kicad_pcb`, `ipc_after_suite.kicad_pcb` | Persistence comparison. IPC R2 lacks the library nickname (D-18) and keeps rot 0 / value TEST |
| `images/custom_symbol.png`, `sym_test_schematic_crop.png` | Symbol graphics and polarity. Cosmetic overlap |
| `images/custom_footprint.png`, `fp_test_2d_view_mcp.png`, `fp_test_3d.png` | Footprint geometry, board view, 3D model alignment |
| `config_restore/kicad_cfg_manifest_before.txt`, `_final.txt` | Identical sha256 manifests of 18 KiCad config files: the global configuration was restored |

Deliberately **not** kept: the GUI snapshot image (it captured another application), raw unsanitized
logs, and large generated files (STEP, full Gerber sets) that can be regenerated from the evidence boards.
