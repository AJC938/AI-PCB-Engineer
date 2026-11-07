# PCB Layout Report — V0.0.2

Board snapshot: [`evidence/kicad/led_test.kicad_pcb`](evidence/kicad/led_test.kicad_pcb).
Renders: [`final_top.png`](evidence/images/final_top.png), [`final_iso.png`](evidence/images/final_iso.png),
[`final_bottom.png`](evidence/images/final_bottom.png), [`from_left.png`](evidence/images/from_left.png).

## Board
| Item | Value | Tool | Verified by |
|---|---|---|---|
| Layers | 2 copper (F.Cu, B.Cu), 1.6 mm (KiCad default stack-up) | create_project | Gerber job file: `LayerNumber 2`, `BoardThickness 1.6` |
| Outline | 50 × 30 mm rounded rectangle, R1 mm, origin (100, 100) | add_board_outline | Edge.Cuts Gerber: 100.000–150.000 × 100.000–130.000 mm |
| Mounting | 4 × M3 NPTH Ø3.2 at 4 mm from each edge | place_component (`MountingHole_3.2mm_M3`) | NPTH drill file: T1 Ø3.2 ×4 |

## Design rules (set_design_rules)
| Rule | Value | Basis |
|---|---|---|
| Copper clearance | 0.25 mm | **ASSUMED** conservative value. The KiCad default read back as **0** |
| Track width (default / min) | 0.5 / 0.25 mm | Design choice. Current is under 6 mA (see calculations) |
| Min hole | 0.3 mm | Generic |
| Hole clearance / hole-to-hole | 0.25 / 0.25 mm | KiCad default |
| Copper-to-edge | 0.5 mm | KiCad default |
| Courtyard clearance | 0.25 mm | set |

No manufacturer is selected yet. These rules are generic and have **not** been checked against a
specific fab's published capabilities (ENGINEERING_RULES §7). That check comes before any real order.

## Placement (move_component)
| Ref | Position (mm) | Rotation | Rationale |
|---|---|---|---|
| J1 | (105.60, 112.46) pad 1 | 270° | Wire entry faces the left board edge, as seen in the 3D render. Screws face up |
| R1 | (115.00, 110.00) pad 1 | 0° | Between the connector and the LED. Straight route to J1.1 |
| D1 | (135.00, 117.54) pad 1 (K) | 90° | Right side, unobstructed, easy to see |

Steps and checks:
1. `sync_schematic_to_board` imported 3 footprints and 3 nets (6 pads assigned, 0 unmatched).
2. `check_courtyard_overlaps` found J1 0.065 mm past the left edge. J1 was moved +0.52 mm in X and re-checked: no component overlaps.
3. The checker then reported the mounting holes as out of bounds. That is a false positive (D-8). KiCad DRC courtyard rules report 0.
4. `get_component_pads` was used after every move to confirm pad positions and nets.

## Silkscreen
Labels `+5V` and `GND` sit beside the two terminal screws (pad 1 = +5V on top, pad 2 = GND below).
The title reads `LED TEST v0.0.2  5V DC`. The LED outline shows the cathode flat. The mounting-hole
references are hidden (`move_footprint_text visible=false`) because they were clipped by the board
edge. Final DRC has no silkscreen warnings.

## Issues found during layout
| Issue | Resolution |
|---|---|
| `add_mounting_hole` used a non-existent lib ID and caused silk-over-mask warnings (D-4) | Deleted, replaced with the library footprint through `place_component` |
| Holes flagged "extra footprint" in schematic parity | `set_footprint_type not_in_schematic=true`, excluded from BOM and POS |
| Two save refusals after sync and refill (D-1) | `open_project` reload. On-disk state verified each time |

Placement is functional and deliberate, not arbitrary, and it was checked visually with 3D renders.
Mechanical fit with real parts is **NOT TESTED**.
