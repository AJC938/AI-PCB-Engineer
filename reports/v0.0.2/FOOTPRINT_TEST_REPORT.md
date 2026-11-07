# Footprint Test Report — V0.0.2

All footprints come from the KiCad 10.0.8 official libraries. No custom footprint was needed,
and the `footprint` toolbox (create/edit) was **NOT TESTED**. Pad data was read from the library
`.kicad_mod` files because MCP `get_footprint_info` returns only pad numbers and shapes (D-7).
The values were then confirmed in the generated Gerbers and drill files.

## J1: Phoenix Contact MKDS 1,5/ 2-5,08 (1715721)
Footprint: `TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal`

| Parameter | Datasheet (Phoenix product page) | Footprint | Check |
|---|---|---|---|
| Positions / pitch | 2 / 5.08 mm | pads 1, 2 at x = 0, 5.08 | PASS |
| PCB hole | Ø1.3 mm | drill 1.3 | PASS |
| Pin section | 0.9 × 0.9 mm (diagonal 1.27 mm) | — | PASS: fits Ø1.3 (diametral clearance 0.03 mm on the diagonal, as Phoenix specifies) |
| Pad | — | 2.6 mm (pad 1 roundrect, pad 2 circle). Annular ring 0.65 mm | OK |
| Body W × L | 10.16 × 9.8 mm | Fab outline 10.16 × 9.8 mm | PASS |
| Wire entry | — | +Y side of the footprint. Rotated 270° on the board, it faces the left edge | VERIFIED by 3D render ([`from_left.png`](evidence/images/from_left.png)) |
| 3D model | — | KiCad STEP present | PASS |

## R1: Yageo MFR-25FBF52-620R
Footprint: `Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal`

| Parameter | Datasheet (Yageo MFR, p.3) | Footprint | Check |
|---|---|---|---|
| Body L × ØD | 6.3±0.5 × 2.4±0.2 mm (max 6.8 × 2.6) | 6.3 × 2.5 mm body | PASS (nominal match. Max body leaves 1.68 mm per side to the pad centre for the lead bend) |
| Lead Ød | 0.55±0.05 (max 0.60) | drill 0.8 | PASS: 0.20 mm diametral clearance |
| Pitch | not specified (axial) | 10.16 mm | OK, standard for DIN0207 |
| Pad | — | Ø1.6. Annular ring 0.4 mm | OK |
| 3D model | — | present | PASS |

## D1: Kingbright WP7113ID
Footprint: `LED_THT:LED_D5.0mm`

| Parameter | Datasheet (Kingbright V.14A p.1) | Footprint | Check |
|---|---|---|---|
| Pitch | 2.54 mm | 2.54 mm | PASS |
| PCB hole | recommended Ø0.9 ×2 | drill 0.9 | PASS (matches the manufacturer's recommendation) |
| Lead | □0.5 (+0.25 / −0.1) mm | — | **WARNING**: at the maximum tolerance (□0.75, diagonal 1.06 mm) a lead would not pass a Ø0.9 hole. The manufacturer still recommends Ø0.9, so it is kept. Physical fit is **NOT TESTED** |
| Body / flange | Ø5.0 / Ø5.9 mm | Fab circle Ø5.0. Silkscreen arc about Ø5.98 | PASS |
| Polarity | cathode lead on the flange's flat side, shorter by 1.5±1 mm | pad 1 = square = K. Silkscreen flat at x = −1.29 mm, on the pad 1 side | PASS |

## Schematic pin to PCB pad mapping
| Ref | Schematic pin | Pad | Net (board, `get_component_pads`) | Gerber flash |
|---|---|---|---|---|
| J1 | 1 (Pin_1) | 1 (roundrect 2.6) | +5V | (105.60, 112.46) |
| J1 | 2 (Pin_2) | 2 (circle 2.6) | GND | (105.60, 117.54) |
| R1 | 1 | 1 (Ø1.6) | +5V | (115.00, 110.00) |
| R1 | 2 | 2 (Ø1.6) | LED_A | (125.16, 110.00) |
| D1 | 1 (K) | 1 (square 1.8) | GND | (135.00, 117.54) |
| D1 | 2 (A) | 2 (Ø1.8) | LED_A | (135.00, 115.00) |

KiCad DRC schematic parity: **0 issues** (final), which confirms the mapping.

## Mounting holes
`MountingHole:MountingHole_3.2mm_M3`: NPTH Ø3.2, no annular ring, board-only, excluded from
the BOM and CPL. The MCP `add_mounting_hole` tool was not used for the final design (D-4).
