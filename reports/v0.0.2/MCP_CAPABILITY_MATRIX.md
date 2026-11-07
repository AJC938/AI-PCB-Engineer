# MCP Capability Matrix — V0.0.2

Two separate questions per feature:
- **Invocation:** did the MCP tool run and do what it claims?
- **Engineering validation:** was the result checked independently (kicad-cli, file
  inspection, datasheet) and found correct?

| Feature | MCP tool(s) | Tested | Invocation | Engineering validation | Limitation |
|---|---|---|---|---|---|
| Schematic generation | create_project, add_schematic_component | Yes | PASS | PASS: `validate_schematic` + kicad-cli load. 9 symbols | Field text can overlap (cosmetic). No auto-layout used |
| Symbol selection | search_symbols, batch_list_symbol_pins | Yes | PASS | PASS: pin numbers/names checked against datasheets (LED 1=K, 2=A) | Library symbols only. No MPN-specific symbols |
| Electrical wiring | add_schematic_wire, add_schematic_net_label, get_schematic_pin_locations | Yes | PASS | PASS: all 7 wire endpoints snapped to pins. CLI netlist shows 3 correct nets | Caller must compute coordinates. Snapping makes this reliable |
| ERC | run_erc | Yes | PASS | PASS: 0 violations, same as `kicad-cli sch erc --severity-all`. PWR_FLAG necessity proven by experiment | — |
| Netlist | generate_netlist, export_netlist | Yes | PASS | PASS: identical to `kicad-cli sch export netlist` | — |
| Footprint assignment | add_schematic_component (footprint field), get_footprint_info | Yes | PASS | PASS: pads/drills/pitch checked against datasheets from `.kicad_mod` files and Gerbers | `get_footprint_info` lacks pad geometry and drill sizes |
| Board synchronization | sync_schematic_to_board | Yes | **WARNING** | PASS after workarounds: CLI schematic parity 0 | D-1 false "external change" save refusal. D-2 local-label net names lose the `/` prefix. D-3 custom fields not copied (non-MCP script used) |
| Placement | move_component, place_component, check_courtyard_overlaps | Yes | PASS | PASS: DRC courtyard rules 0. 3D render reviewed (terminal-block wire entry faces the edge) | Courtyard checker false positives for holes (D-8). Mounting-hole tool defective (D-4) |
| Routing | route_pad_to_pad | Yes | PASS | PASS: DRC 0, unconnected 0, clearance by DRC | Straight segment only, no obstacle avoidance or waypoints. Layout had to be planned for straight routes |
| Copper zones | add_copper_pour, refill_zones, query_zones | Yes | PASS (with WARNING) | PASS: zone filled (1341 mm²), DRC 0 | refill triggers D-1. Server documents SWIG segfault risk (not observed) |
| DRC | run_drc, get_drc_violations, set_design_rules | Yes | PASS | PASS: final 0 errors / 0 warnings, same as kicad-cli | No schematic-parity check (D-6). Default clearance was 0 until set |
| Gerber | export_gerbers | Yes | PASS | PASS: Edge 50.000 × 30.000 mm, 6 pad flashes per copper layer at the right coordinates, X2 net attributes | Reads the saved file only |
| Drill | export_drill | Yes | PASS | PASS: PTH 0.8×2, 0.9×2, 1.3×2 and NPTH 3.2×4, metric. Drill map PDF | — |
| BOM | export_sch_bom, export_bom | Yes | PASS / **WARNING** | Schematic BOM PASS (MPN, Manufacturer, Qty). PCB BOM includes excluded holes, omits MPN | Use `export_sch_bom` (D-5) |
| CPL | export_pos | Yes | PASS | PASS: 3 parts, holes excluded, positions/rotations match the board | KiCad CPL is Y-negated (standard). Fab-specific rotation offsets not applied |
| 3D / PDF docs | export_3d, export_pcb_pdf, export_sch_pdf | Yes | PASS | PASS: STEP 848 KB with models, PDFs 4 + 1 pages | — |

**Overall:** the MCP server can carry a simple two-layer THT board from an empty project to
inspected fabrication files without the KiCad GUI. It needs three workarounds (reload after
sync/refill, global labels for named nets, a pcbnew field-copy script) and one replaced tool
(mounting holes). This is a **digital** validation only. **No hardware was built or tested.**
