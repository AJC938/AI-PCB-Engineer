# MCP Tool Inventory — V0.0.2

Server: KiCAD-MCP-Server v2.8.3 (`stable`, `1d204fe3`), backend SWIG, KiCad 10.0.8.
Client: Claude Code 2.1.317 inside the Claude desktop app. Date: 2026-11-07.

## Discovery method
1. `list_toolboxes` and `search_tools` (run in this session during the V0.0.1 in-session verification) list
   20 toolboxes with 215 tools, plus the core set (33 core tools + 4 toolbox-management tools = 37).
2. `open_toolbox` opened `schematic, symbol_library, symbol_pins, library, footprint, board, component, routing, drc, export, validation`.
   The response returned every tool name and description.
3. Each tool's JSON schema was loaded and read before its first call.
4. `close_toolbox` closed `symbol_library, symbol_pins, footprint, validation` after use.

**Finding (client behaviour):** the server's note says new toolbox tools are callable "from the
user's next message". In Claude Code they became callable **in the same turn**, and closing a
toolbox removed its tools immediately.

## Toolboxes
| Toolbox | Tools | Opened in V0.0.2 | Tools invoked |
|---|---|---|---|
| core (always on) | 37 | — | 16 |
| schematic | 36 | yes | 9 (+3 shared with core) |
| symbol_library | 17 | yes | 1 |
| symbol_pins | 3 | yes | 1 |
| library | 9 | yes | 1 |
| footprint | 5 | yes | 0 |
| board | 15 | yes | 3 |
| component | 24 | yes | 6 |
| routing | 14 | yes | 6 |
| drc | 8 | yes | 4 |
| export | 27 | yes | 8 |
| validation | 2 | yes | 1 |
| schematic_hierarchy / schematic_layout / schematic_batch / autoroute / import / jlcpcb / parts-registry / digikey / gui-driver | 7/12/6/4/2/7/3/3/11 | no | 0 |

## Tools invoked (56 distinct)
Legend: R = read-only, W = writes project/output files. "PASS" requires a successful call **and**
independent verification of the intended effect.

| Tool | Toolbox | R/W | Result | Note |
|---|---|---|---|---|
| list_toolboxes | core | R | PASS | 20 toolboxes |
| search_tools | core | R | PASS | `drc` gives 9 matches |
| open_toolbox | core | config | PASS | tools usable in the same turn |
| close_toolbox | core | config | PASS | tools removed immediately |
| get_backend_state | core | R | PASS | `swig` (V0.0.1 in-session) |
| is_dirty | core | R | PASS | (V0.0.1 in-session) |
| check_kicad_ui | core | R | PASS | detects whether kicad.exe is running |
| create_project | core | W | PASS | .kicad_pro/.kicad_sch/.kicad_pcb created |
| open_project | core | R | PASS | needed to resync memory after sync/refill (see defects) |
| save_project | core | W | PASS | |
| add_schematic_component | core | W | PASS | 9 symbols incl. power and PWR_FLAG |
| add_schematic_net_label | core | W | PASS | local and global labels, pin snapping |
| sync_schematic_to_board | core | W | **WARNING** | works, but see D-1, D-2, D-3 |
| add_board_outline | core | W | PASS | 50 × 30 mm, R1 corners |
| move_component | core | W | PASS | position and rotation |
| place_component | core | W | PASS | library footprint by `lib:name` |
| get_schematic_pin_locations | schematic | R | PASS | correct after rotation |
| add_schematic_wire | schematic | W | PASS | 7 wires, all endpoints snapped to pins |
| set_schematic_component_property | schematic | W | PASS | MPN / Manufacturer |
| run_erc | schematic | R | PASS | equals `kicad-cli sch erc` |
| generate_netlist | schematic | R | PASS | equals `kicad-cli` XML netlist |
| export_netlist | schematic/export | W | PASS | |
| get_schematic_view | schematic | R | PASS | image usable for review |
| delete_schematic_net_label | schematic | W | PASS | |
| list_schematic_labels | schematic | R | PASS | |
| validate_schematic | validation | R | PASS | structural + kicad-cli load check |
| batch_list_symbol_pins | symbol_pins | R | PASS | pin numbers/names/types |
| search_symbols | symbol_library | R | PASS | |
| get_footprint_info | library | R | **WARNING** | no pad positions or drill sizes (D-7) |
| get_design_rules | drc | R | PASS | default clearance was 0 |
| set_design_rules | drc | W | PASS | |
| run_drc | drc | R* | PASS | no schematic-parity check (D-6); writes `<board>_drc_violations.json` next to the board |
| get_drc_violations | drc | R | PASS | |
| get_component_pads | component | R | PASS | positions, nets, sizes, drill |
| check_courtyard_overlaps | component | R | **WARNING** | false boundary violations for holes (D-8) |
| get_ratsnest | component | R | PASS | |
| delete_component | component | W | PASS | |
| set_footprint_type | component | W | PASS | board-only, BOM/POS exclusion |
| move_footprint_text | component | W | PASS | hide reference |
| add_mounting_hole | board | W | **FAILED** | invalid lib ID, silk/mask warnings (D-4). Replaced by `place_component` |
| add_board_text | board | W | PASS | silkscreen labels |
| get_board_2d_view | board | R | **WARNING** | monochrome render, not useful with a filled zone (D-9) |
| route_pad_to_pad | routing | W | PASS | straight segment only, no obstacle avoidance |
| add_copper_pour | routing | W | PASS | GND, B.Cu |
| refill_zones | routing | W | **WARNING** | fills correctly but triggers D-1. No crash in 2 runs |
| query_zones | routing | R | PASS | |
| query_traces | routing | R | PASS | |
| get_nets_list | routing | R | **WARNING** | stale net shown until reload (D-1) |
| export_gerbers | export | W | PASS | |
| export_drill | export | W | PASS | |
| export_pos | export | W | PASS | |
| export_sch_bom | export | W | PASS | |
| export_bom | export | W | **WARNING** | ignores `exclude_from_bom` and `includeAttributes` (D-5) |
| export_pcb_pdf | export | W | PASS | 4 pages |
| export_sch_pdf | export | W | PASS | |
| export_3d | export | W | PASS | STEP with component models |

Totals: **48 PASS · 7 WARNING · 1 FAILED** of 56 invoked. The remaining ~190 discovered tools are
**NOT TESTED**. Discovery alone is not counted as PASS.

Defect IDs (D-n) are described in [FINAL_V0.0.2_REPORT.md](FINAL_V0.0.2_REPORT.md#defects-and-limitations).
