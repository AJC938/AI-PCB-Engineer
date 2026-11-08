# SWIG vs IPC Comparison — V0.0.3

**Equivalence of conditions:** both backends ran the *same generated 20-step sequence*
(`tests/make_backend_suite.py`) on *byte-identical* copies of the V0.0.2 board (sha256 `bd10786d…`),
through the same MCP server build (v2.8.3, `1d204fe3`) and the same harness (`ai/workflows/mcp_harness.py`).
The differences were the backend variable and, for IPC, a running pcbnew with the board open.
Each run was performed once (n = 1).

## Results per dimension
| Dimension | SWIG | IPC | Notes |
|---|---|---|---|
| Connection reliability | PASS | PASS | IPC needs the GUI and a global preference (temporarily enabled). Direct kipy connect 18 ms |
| Project state reading | PASS | PASS | IPC session pinned correctly |
| Schematic inspection | PASS | PASS (n/a) | file-based in both. Not backend-dependent |
| PCB inspection | PASS | **FAIL** | IPC: 0 components (silent), numeric layer IDs, malformed trace uuid/netCode |
| Component placement | PASS | **WARNING** | IPC places and persists, but drops the footprint's library nickname |
| Property modification | PASS (rotate 180°, value → 1k) | **FAIL** | IPC cannot find the component it just placed |
| Save persistence | PASS (independent pcbnew read) | PASS | IPC save is done by KiCad itself |
| Reopen consistency | PASS (R2 read back after reopen) | **FAIL** | IPC cannot read R2 back. The file holds R2 unmodified |
| DRC availability | PASS (kicad-cli). WARNING: stale zone gives 6 errors until refill (D-10) | PASS (kicad-cli, same) | `run_drc` is file-based for both |
| Export capability | PASS | PASS | kicad-cli for both |
| Zone refill | PASS with D-1 (V0.0.2) | **PASS**, no desync | the one area where IPC was better |
| Error recovery | Known reload rule (D-1). Failures are explicit | Silent wrong reads are **not recoverable by the caller** | worst property of the IPC path here |
| Latency (n = 1) | faster on every read | slower on every read | see table |

## Latency and outcome by step (seconds, n = 1)
| Step | Tool | SWIG | IPC | IPC outcome |
|---|---|---|---|---|
| T1a | check_kicad_ui | 2.758 | 2.363 | ok |
| T1b | get_backend_state | 0.698 | 0.551 | ok |
| T3 | open_project | 2.848 | 2.123 | ok |
| T2 | get_backend_state | 0.760 | 1.091 | ok |
| T4 | list_schematic_components | 4.121 | 4.177 | ok (file-based) |
| T5a | get_component_list | 0.193 | 0.204 | **wrong: 0 components** |
| T5b | get_nets_list | 0.083 | 0.203 | ok |
| T6a | get_board_info | 0.075 | 1.030 | **wrong componentCount** |
| T6b | get_layer_list | 0.087 | 0.283 | numeric IDs |
| T6c | query_traces | 0.096 | 0.279 | malformed uuid/netCode |
| T7 | place_component | 0.625 | 3.537 | placed, nickname lost |
| T8a | rotate_component | 0.291 | 0.248 | FAIL |
| T8b | edit_component | 0.049 | 0.186 | FAIL (SWIG fallback) |
| T8c | get_component_properties | 0.080 | 0.626 | FAIL |
| T9 | save_project | 0.388 | 0.481 | ok |
| T10a | open_project | 0.437 | 1.432 | ok |
| T10b | get_component_properties | 0.076 | 0.719 | FAIL |
| T10c | get_backend_state | 0.874 | 0.218 | ok |
| T11 | run_drc | 24.420 | 9.255 | ok (kicad-cli) |
| T12 | export_gerbers | 1.836 | 0.622 | ok (kicad-cli) |

`run_drc` and `export_gerbers` call kicad-cli, so their timing difference reflects system load and
caching, not the backend.

## Recommendation
**SWIG remains the only backend fit for use** in this environment (KiCad 10.0.8, kicad-python 0.8.0,
server v2.8.3), with the V0.0.2 workflow rules. IPC should be re-evaluated only after a
kicad-python release that decodes KiCad 10 footprint messages. The first test then is the direct
kipy probe `get_board().get_footprints()`, before any MCP test.
