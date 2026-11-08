# IPC Backend Evaluation — V0.0.3

## Activation requirements (from the server docs and source, then verified)
| Requirement | Source | Status during test |
|---|---|---|
| KiCad 9.0+ running with a board open in the PCB editor | `docs/IPC_BACKEND_STATUS.md` | pcbnew.exe 10.0.8 launched by the test on the sandbox board |
| KiCad preference *Enable IPC API Server* | docs / `kicad_common.json` → `api.enable_server` | was `false`. **Temporarily set `true` with the user's approval**, then restored byte-identical |
| `kicad-python` (kipy) | `requirements.txt` | 0.8.0 installed in V0.0.1 |
| MCP backend selection | `KICAD_BACKEND=auto|ipc|swig` | `ipc`, set **only for the test harness process**. `.mcp.json` is unchanged |
| Session pinning | docs (§Session Pinning) | `open_project` pins to IPC only when the GUI has the same `.kicad_pcb` open |

Windows transport: kipy uses `ipc://%TEMP%\kicad\api.sock`, which NNG implements as a **named pipe**,
so no socket file appears. A file-existence check is not a valid readiness test. A direct kipy
`get_version()` is.

## Procedure
1. Closed all KiCad instances (the user closed their own session; it was not terminated by the test).
2. Backed up `%APPDATA%\kicad\10.0` (18 files, sha256 manifest).
3. Set `api.enable_server=true` and launched `pcbnew.exe ipc/led_test.kicad_pcb`.
4. Direct kipy probe. Then the identical 20-step suite used for SWIG (`tests/make_backend_suite.py ipc`), then an extra zone/text test.
5. Closed the launched pcbnew gracefully. Restored the config, verified byte-identical, removed the empty `%TEMP%\kicad`.

Input: `hardware/sandbox/v0.0.3/ipc/led_test.*`, byte-identical (sha256 `bd10786d…`) to the SWIG input and the V0.0.2 snapshot.

## Direct kipy probe (independent of MCP)
| Call | Result |
|---|---|
| `KiCad().get_version()` | `10.0.8`, 18 ms. **Connection works** |
| `get_open_documents(PCB)` | `['led_test.kicad_pcb']` |
| `get_board().get_footprints()` | **NotImplementedError: Missing type mapping for `kiapi.board.types.ReferencePoint`** |

Root cause of most IPC failures below: **kicad-python 0.8.0 cannot decode a message type that KiCad
10.0.8 sends for footprints.** A newer kicad-python was **not** tested, because no dependency was changed.

## Test cases (MCP, `KICAD_BACKEND=ipc`)
| # | Operation | Tool(s) | Result | Evidence / observation |
|---|---|---|---|---|
| 1 | Connect | check_kicad_ui, get_backend_state | **PASS** | `ipc_connected: true`, `realtime: true` |
| 2 | Read project state | get_backend_state | **PASS** | `sessionBackend: ipc` after open |
| 3 | Open test project | open_project | **PASS** | pinned to IPC (GUI had the same board) |
| 4 | Read schematic | list_schematic_components | PASS (n/a) | file-based (kicad-skip). Not an IPC operation, so the result is identical to SWIG |
| 5 | Components and nets | get_component_list, get_nets_list | **FAIL** | components: `success:true, count:0` on a board with 7 footprints (**silent wrong result**). Nets: correct |
| 6 | PCB structure | get_board_info, get_layer_list, query_traces | **FAIL** | `componentCount: 0` (wrong). Layers returned as numeric IDs (`"3","42",…`). Trace `uuid` is a raw protobuf string, `netCode: 0`, layer `"3"`. Size and track count correct |
| 7 | Place component | place_component | **WARNING** | R2 placed and visible in the GUI, persisted after save. **The footprint's library nickname was lost** (`R_Axial_…` instead of `Resistor_THT:R_Axial_…`). 3.5 s |
| 8 | Modify property | rotate_component, edit_component, get_component_properties | **FAIL** | "Component R2 not found" (IPC). `edit_component` fell back to SWIG, whose board copy does not contain the IPC-placed R2 |
| 9 | Save | save_project | **PASS** | KiCad wrote the file. R2 present on disk (independent pcbnew read) |
| 10 | Reopen and verify | open_project, get_component_properties | **FAIL** (MCP) / PASS (disk) | MCP still cannot find R2. On disk: R2 at (125, 122), rot 0, value `TEST`, so the rotation and value changes never applied |
| 11 | DRC | run_drc | PASS (n/a) | runs kicad-cli on the saved file (backend `swig`). 6 errors from a stale zone, same as SWIG (D-10) |
| 12 | Export | export_gerbers | PASS (n/a) | kicad-cli on the saved file (backend `swig`) |
| X1 | Text | add_board_text | **PASS** | `IPC TEST` in the saved file |
| X2 | Zone refill | refill_zones | **PASS** | 0.65 s. Real fill: CLI DRC **without** refill reports 0. **No D-1 save desync** |
| X3 | Save after X1/X2 | save_project | **PASS** | persisted |

Independent comparison of the final boards (CLI DRC `--severity-all --schematic-parity --refill-zones`):
IPC board and SWIG board both give 0 violations, 0 unconnected, 1 expected parity item (R2 is PCB-only).

## Latency (single run, n = 1: indicative only)
Reads were slower over IPC (`get_board_info` 1.03 s vs 0.08 s, `get_layer_list` 0.28 vs 0.09 s,
`query_traces` 0.28 vs 0.10 s). `place_component` took 3.54 vs 0.63 s. Full table in SWIG_VS_IPC_COMPARISON.md.

## Conclusion
IPC **connects and can write** (place, text, zone refill, save). Zone refill over IPC fixes two SWIG
weaknesses (stale fills, D-1 desync). But with KiCad 10.0.8 + kicad-python 0.8.0, **every footprint
read fails**, and some fail **silently** with `success:true`. Component-level editing is therefore
impossible and verification is unreliable. **IPC is not usable for the design workflow in this
environment.** It is not "more reliable" just because it connects.

Defects: D-16 to D-19 (see FINAL_V0.0.3_REPORT.md).
