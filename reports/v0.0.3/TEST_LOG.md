# V0.0.3 Test Log (chronological, 2026-11-08, local time)

Client for all MCP runs: `ai/workflows/mcp_harness.py` (JSON-RPC over stdio, same command, args
and env as `.mcp.json`, plus per-process overrides). The Claude Code in-session `kicad` connection was
disconnected at the start of this session, so all calls went through the harness. Raw logs:
`evidence/runs/*.json` (sanitized). The harness flags only *explicit* failures. Silent failures
(marked †) were found by independent verification.

| Time | Run / action | Steps | Outcome | Notes |
|---|---|---|---|---|
| — | Git checks | — | OK | HEAD = `v0.0.2` (`0195a8d`), clean, no v0.0.3 refs, no remote. Branch `evaluation/v0.0.3-mcp-capabilities` created |
| — | Server inspection | — | OK | IPC_BACKEND_STATUS.md, GUI_DRIVER_SPEC.md, FOOTPRINT_SYMBOL_CREATOR_GUIDE.md, KNOWN_ISSUES.md, ipc_backend.py, gui_driver.py |
| — | User decisions | — | approved | temporary IPC preference toggle with restore. Temporary GUI-driver install with removal |
| — | Schema dump | 21 schemas | OK | all tools present with the 12 toolboxes opened (201 tools) |
| 01:24 | `run_swig` (backend suite, SWIG) | 20 | 20/20 OK | KiCad project manager (user's session) was running, untouched. DRC 6 errors traced to a stale zone (D-10) |
| — | Independent SWIG check | — | PASS | pcbnew read R2 (125, 122), rot 180, value 1k. CLI DRC no-refill 6 / refill 0 |
| 01:28 | `run_sym_create` | 34 | 33 OK, S7 fail | S7 `get_symbol_info` "Symbol not found" right after registration (D-12) |
| — | Independent symbol check | — | PASS | CLI ERC 0, CLI netlist nets correct, `libsource AIPCB_Symbols`. Symbol and schematic renders |
| 01:29 | `run_sym_reopen` (fresh process) | 5 | 5/5 OK | MCP `export_netlist` nets == CLI nets |
| 01:29 | `run_symlookup` | 5 | G3 timeout | `search_symbols` 30 s timeout (D-13). `get_symbol_info` OK with dir / .kicad_sch |
| 01:30 | `run_symlookup2` | 1 | OK | `get_symbol_info` OK with .kicad_pro in a fresh process, confirming D-12 is a same-session cache issue |
| 01:30 | `run_fp_create` | 46 | 45 OK, F6 fail | F6 `get_footprint_info` fail (D-12). F8 sync save refused (D-1), handled by F9 reopen |
| — | Independent footprint check | — | PASS | pcbnew: D1 = `AIPCB_Footprints:LED_D5.0mm_WP7113ID`. File pads equal KiCad `LED_D5.0mm`. CLI DRC 0/0, parity = MPN only |
| 01:32 | `run_fp_reopen` (fresh process) | 7 | 7/7 OK | D1 persisted. Gerber and drill exported. 2D view |
| — | User closed their KiCad | — | — | confirmed no KiCad process |
| ~03:00 | Config backup + `api.enable_server=true` | — | — | 18-file manifest |
| ~03:01 | Launch pcbnew (IPC board) | — | OK | named-pipe socket. Direct kipy: version OK, open docs OK, **get_footprints → ReferencePoint decode error** (D-16) |
| 03:02 | `run_ipc` (same suite, IPC) | 20 | 16 OK†, 4 explicit FAIL | † T5a 0 components, T6a componentCount 0, T6b numeric layers, T6c malformed trace ids. T8a–c and T10b "R2 not found" |
| — | Independent IPC check | — | mixed | file: R2 present, rot 0, value TEST, **no library nickname** (D-18) |
| 03:04 | `run_ipc_extra` | 5 | 5/5 OK | text + refill + save persisted. CLI DRC without refill = 0 (real fill) |
| — | Close pcbnew, restore `kicad_common.json` | — | OK | byte-identical. `pcbnew.json` recent-files changed (restored later) |
| 03:05 | `run_gui_install` | 1 | OK† | † installed to an unsearched folder (D-20). Helper never started (60 s) |
| — | Manual copy to `<config>\scripting\plugins` | — | OK | token after 5.2 s. Listener 127.0.0.1:8770 |
| 03:08 | `run_gui1` | 3 | 3 OK† | wait_for, tree OK. † snapshot captured a different foreground application. **Image deleted** (D-22) |
| 03:09 | `run_gui2` | 3 | 3 OK† | † all clicks `processed: false`, no effect (D-21) |
| 03:09 | `run_gui3` | 1 | OK† | † Save: `processed: false`, file unchanged |
| ~03:10 | Cleanup | — | OK | pcbnew closed. Plugin, token and created folders removed. `pcbnew.json` restored. **Config byte-identical to backup (18 files)**. Empty `%TEMP%\kicad` removed |

Not run on purpose: `kicad_run_drc` (opens a modal dialog on the user's active desktop) and any
further screenshot tool.
