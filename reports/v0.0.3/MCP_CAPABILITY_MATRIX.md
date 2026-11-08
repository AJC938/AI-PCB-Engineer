# MCP Capability Matrix — V0.0.3

Status legend: **VERIFIED** = invocation PASS + independent verification PASS ·
**PARTIAL** = works with limitations or needs a workaround · **FAILED** = produced an incorrect or no result ·
**BLOCKED** = not run because of a documented constraint · **UNSUPPORTED** = no capability in the toolset.
V0.0.2 rows (SWIG design flow) are carried over unchanged and re-confirmed by the V0.0.3 SWIG suite where noted.

## Backend layer
| Capability | SWIG | IPC (KiCad 10.0.8, kipy 0.8.0) |
|---|---|---|
| Connect / state / open project | VERIFIED (re-confirmed) | VERIFIED |
| Read components | VERIFIED | **FAILED** (silent: 0 components, D-16) |
| Read nets | VERIFIED | VERIFIED |
| Read layers / traces | VERIFIED | **FAILED** (numeric layer IDs, malformed trace ids, D-19) |
| Place footprint | VERIFIED | PARTIAL (persists, library nickname lost, D-18) |
| Rotate / edit / read back a component | VERIFIED (re-confirmed) | **FAILED** (D-17) |
| Board text | VERIFIED (V0.0.2) | VERIFIED |
| Zone refill | PARTIAL (works, triggers D-1) | VERIFIED (real fill, no desync) |
| Save / reopen | VERIFIED (D-1 reload rule) | save VERIFIED / MCP read-back FAILED |
| DRC / export (kicad-cli, file-based) | VERIFIED (`run_drc` does not refill zones: D-10) | same (backend-independent) |

## Library creation
| Capability | Tool(s) | Status | Limitation |
|---|---|---|---|
| Create symbol from scratch | create_symbol | VERIFIED | no pin-name hide/offset (cosmetic). Misleading angle doc (D-15) |
| Register symbol library (project) | register_symbol_library | PARTIAL | absolute, user-specific URI (D-11) |
| Look up a new symbol | get_symbol_info, search_symbols | PARTIAL | same-session cache miss (D-12). search timeout (D-13) |
| Place / wire / ERC / netlist with a custom symbol | add_schematic_component, add_schematic_wire, run_erc, generate_netlist | VERIFIED | — |
| Create footprint | create_footprint | PARTIAL | rectangles only, no `attr` type (D-14) |
| Edit footprint pads | edit_footprint_pad | VERIFIED | — |
| Attach 3D model | add_footprint_3d_model | VERIFIED | — |
| Register footprint library (project) | register_footprint_library | PARTIAL | absolute URI (D-11) |
| Footprint lookup after registration | get_footprint_info | FAILED (same session) | D-12 |
| Custom footprint on PCB: sync, place, route, DRC, Gerber, drill | sync_schematic_to_board, move_component, route_pad_to_pad, run_drc, export_* | VERIFIED | D-1 reload after sync |

## GUI driver (Windows)
| Capability | Tool | Status |
|---|---|---|
| Install helper | install_gui_driver | **FAILED** (wrong folder, D-20). Manual workaround works |
| Detect window | kicad_gui_wait_for | VERIFIED (after workaround) |
| Enumerate UI | kicad_gui_tree | PARTIAL (menus yes, toolbars 0. Exposes recent files) |
| Click / activate | kicad_gui_click | **FAILED** (`processed:false`, D-21) |
| Save via GUI | kicad_gui_click "Save" | **FAILED** (file unchanged) |
| Screenshot / snapshot | kicad_gui_screenshot, kicad_pcb_snapshot | **FAILED** (captures screen pixels incl. other apps: privacy, D-22) |
| GUI DRC | kicad_run_drc | **BLOCKED** (modal dialog on the user's active desktop) |
| AT-SPI tools | kicad_gui_tree_atspi, kicad_gui_click_atspi | **UNSUPPORTED** on Windows (Linux-only by design) |

## V0.0.2 SWIG design flow (carried over)
Schematic generation, wiring, ERC, netlist, footprint assignment, sync (with D-1/D-2/D-3), placement,
routing (straight segments), zones, DRC (no parity: D-6), Gerber, drill, BOM (`export_sch_bom`; D-5),
and CPL are all VERIFIED with the documented workarounds. See `reports/v0.0.2/MCP_CAPABILITY_MATRIX.md`.

**Overall:** the usable surface is SWIG plus file-based tools, now including custom symbol and footprint
creation. IPC and the GUI driver are not usable in this environment.
