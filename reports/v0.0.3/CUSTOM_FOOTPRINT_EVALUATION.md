# Custom Footprint Evaluation — V0.0.3

**Verdict: native MCP can create, edit, attach a 3D model to, register, place and verify a custom
THT footprint.** Graphics are limited to rectangles and the footprint-type attribute is not set,
so a production-quality footprint still needs a follow-up edit.

## Geometry specification
Footprint `AIPCB_Footprints:LED_D5.0mm_WP7113ID` for Kingbright WP7113ID.

| Item | Value | Basis |
|---|---|---|
| Lead pitch | 2.54 mm | **VERIFIED** (datasheet V.14A p.1) |
| Hole | Ø0.9 mm ×2 | **VERIFIED** (recommended PCB layout, p.1) |
| Body / flange | Ø5.0 / Ø5.9 mm | **VERIFIED** (p.1) |
| Cathode | pad 1, square, on the flange-flat side | **VERIFIED** (p.1) |
| Pad size | 1.8 mm (created at 1.7, edited to 1.8) | design choice (annular ring 0.45 mm) |
| Origin / orientation | pad 1 at (0,0), anode at +X | design choice (KiCad convention) |
| Fab rect | x −1.68…4.22, y −2.95…2.95 (box around the Ø5.9 flange) | derived |
| Silk rect | x −1.80…4.34, y −3.07…3.07 | derived |
| Courtyard | x −1.93…4.47, y −3.20…3.20 (+0.25 mm) | design choice |
| 3D model | `${KICAD10_3DMODEL_DIR}/LED_THT.3dshapes/LED_D5.0mm.step` | KiCad's generic 5 mm LED model, **not** a Kingbright-specific model |

This tests the **creation workflow** with datasheet-backed pitch, hole and body dimensions.
Pad size and courtyard are design choices, not datasheet values.

## Workflow and results
| Step | Tool | Result | Verification |
|---|---|---|---|
| Create | create_footprint | **PASS** | `.kicad_mod` written (format `20241229`). 2 pads, 3 rectangles, ref/value fields |
| Edit pads | edit_footprint_pad ×2 | **PASS** | file shows `(size 1.8 1.8)` for both pads |
| 3D model | add_footprint_3d_model | **PASS** | `(model …LED_D5.0mm.step)`. Model appears on the pads in the 3D render |
| Register (project scope) | register_footprint_library | **WARNING** | project `fp-lib-table` written, global table untouched. **Absolute URI with user name** (D-11) |
| Info lookup | get_footprint_info | **FAIL** (same session) | "Failed to get footprint info" right after registration (D-12, same pattern as symbols) |
| Assign to symbol | create_symbol `footprint` + add_schematic_component `footprint` | **PASS** | netlist footprint `AIPCB_Footprints:LED_D5.0mm_WP7113ID` |
| Sync to board | sync_schematic_to_board | **PASS with D-1** | 3 footprints, 3 nets. Save refused (D-1), file correct. `open_project` reload |
| Place / route | move_component, route_pad_to_pad ×3 | **PASS** | same layout as V0.0.2 |
| Save | save_project | **PASS** | |
| Reopen (fresh process) | open_project, get_component_properties, get_component_pads | **PASS** | D1 = custom footprint at (135, 117.54), rot 90, pads 1.8 mm, pad 1 rect (GND), pad 2 circle (LED_A) |
| DRC (MCP) | run_drc | **PASS** | 0 |
| DRC (CLI) | `kicad-cli pcb drc --severity-all --schematic-parity` | **PASS** | 0 violations, 0 unconnected, **no `lib_footprint_issues`** (kicad-cli resolves the custom library through the project table). 3 parity items = MPN field (known D-3) |
| Fab outputs | export_gerbers, export_drill | **PASS** | PTH drill: T2 Ø0.900 at (135.0, 115.0) and (135.0, 117.54) |

## Independent geometry check
`.kicad_mod` pads (file read) compared with KiCad's `LED_THT:LED_D5.0mm`:

| Pad | Custom | KiCad library |
|---|---|---|
| 1 | thru_hole **rect**, (0, 0), 1.8 × 1.8, drill 0.9, `*.Cu *.Mask` | identical |
| 2 | thru_hole **circle**, (2.54, 0), 1.8 × 1.8, drill 0.9, `*.Cu *.Mask` | identical |

Graphics differ by design: rectangles here versus circle and arc outlines in the library.

Visuals: [`custom_footprint.png`](evidence/images/custom_footprint.png) (kicad-cli `fp export svg`),
[`fp_test_2d_view_mcp.png`](evidence/images/fp_test_2d_view_mcp.png) (MCP `get_board_2d_view`),
[`fp_test_3d.png`](evidence/images/fp_test_3d.png) (kicad-cli 3D render).

## Limitations (D-14)
- `create_footprint` accepts only **one rectangle** each for silkscreen, fab and courtyard. No circles, arcs, lines or polygons. The Ø5.9 flange outline and the cathode-flat marking cannot be drawn.
- No footprint-type attribute is written (`attr through_hole` missing). On the board the footprint reports `type: unspecified`, which affects pick-and-place classification. It can be fixed per placement with `set_footprint_type`, but not in the library.
- `kicad-cli fp export svg` requires the output directory to exist ("Error creating svg file" otherwise). This is a CLI behaviour, not MCP.

## Native vs external
All creation, editing and placement steps used MCP tools. Verification used kicad-cli and file
inspection. No pcbnew scripting was needed for this test. Richer graphics would need pcbnew
scripting or direct file edits, which were not tested.
