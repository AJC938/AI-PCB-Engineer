# V0.0.1 Sandbox Smoke Test

Date: 2026-11-07. Project: `hardware/sandbox/mcp_smoke_test` (gitignored, throwaway).
Client: a minimal stdio MCP client that launches the server exactly as configured in
`.mcp.json` (same command, args and env). Raw sanitized responses: `mcp_tool_calls.json`.

## MCP calls (real tool calls, KiCAD-MCP-Server v2.8.3, backend `swig`)
| # | Tool | Result | Evidence |
|---|---|---|---|
| 1 | initialize | PASS | serverInfo `kicad-mcp-server 2.8.3`, 1.3 s |
| 2 | tools/list | PASS | 37 tools (core toolbox), see `mcp_core_tools.json` |
| 3 | get_backend_state | PASS | `backend: swig`, Python worker up |
| 4 | list_toolboxes | PASS | 20 toolboxes, 215 additional tools |
| 5 | check_kicad_ui | PASS | Detected the running KiCad without interacting with it |
| 6 | create_project | PASS | `.kicad_pro`, `.kicad_pcb`, `.kicad_sch` created |
| 7 | add_board_outline | PASS | rectangle 50 × 30 mm |
| 8 | place_component | PASS | R1 `Resistor_SMD:R_0603_1608Metric`, 10k, at (25, 15) mm, F.Cu |
| 9 | save_project | PASS | board saved |
| 10 | get_board_info | PASS | size 50 × 30 mm reported back |
| 11 | add_schematic_component | PASS | R1 `Device:R` 10k with footprint field |
| 12 | list_schematic_components | PASS | `R1: Device:R = "10k"`, 2 pins |
| 13 | get_project_info / get_backend_state | PASS | board loaded, not dirty |

## Independent verification (not via MCP)
| Check | Tool | Result |
|---|---|---|
| Board file is valid KiCad 10 | `kicad-cli pcb drc` | PASS: parsed, version `20260206` |
| DRC | `kicad-cli pcb drc --severity-all` | PASS: 0 violations, 0 unconnected (`reports/drc/v0.0.1-sandbox-drc.json`) |
| ERC | `kicad-cli sch erc --severity-all` | 2 errors, **expected**: `pin_not_connected` on R1 pins 1 and 2 (fixture has no nets) |
| Edge.Cuts | Gerber `-Edge_Cuts.gm1` | PASS: closed rectangle (0,0) to (50,30) mm |
| Footprint pads | Gerber `-F_Cu.gtl` vs library `.kicad_mod` | PASS: 2 pads at x = 24.175 / 25.825 mm (library ±0.825 mm), roundrect 0.8 × 0.95 mm (library 0.8 × 0.95) |
| Schematic | file inspection | PASS: `lib_id "Device:R"`, Reference R1, Value 10k, Footprint set |
| Exports | `kicad-cli pcb export gerbers / svg` | PASS: 24 Gerber layers + job file, SVG render |

## In-session verification (Claude Code, after user approval, 2026-11-07)
The 13 calls above used a stand-alone stdio client. After the user approved the project
server, the connection was re-verified from inside a Claude Code session (read-only, no
files changed):

| Call | Result |
|---|---|
| Tool discovery | PASS: 37 `kicad` tools exposed to the session (33 core + 4 toolbox-management) |
| `get_backend_state` | PASS: `backend: swig`, no board loaded |
| `check_kicad_ui` | PASS: reported KiCad not running at that time |
| `is_dirty` | PASS: no board loaded |
| `list_toolboxes` / `search_tools("drc")` | PASS: 20 toolboxes, 9 DRC-related matches |

Previous sandbox DRC result (unchanged): 0 violations, 0 unconnected.
Known non-blocking inconsistency: CLI `claude mcp get kicad` still says "Pending approval".

## Limitations of this test
- No nets, wiring or routing. Schematic and board are not linked (no
  `sync_schematic_to_board`), so it is not a functional circuit.
- Only the `core` toolbox was exercised.
- IPC backend, GUI driver, Freerouting and part sourcing were not tested.
- The 13 build-and-check calls used a stand-alone stdio client. In-session use was
  verified afterwards with read-only calls only (see above).
- No physical hardware involved. Nothing here says anything about a real board.
