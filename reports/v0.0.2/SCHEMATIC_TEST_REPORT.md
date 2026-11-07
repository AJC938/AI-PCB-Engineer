# Schematic Test Report — V0.0.2

Project: `hardware/sandbox/v0.0.2-led-test/led_test.kicad_sch` (sandbox, gitignored).
Snapshot: [`evidence/kicad/led_test.kicad_sch`](evidence/kicad/led_test.kicad_sch). Rendering:
[`evidence/images/schematic_view_mcp.png`](evidence/images/schematic_view_mcp.png) and
[`evidence/fab/led_test-schematic.pdf`](evidence/fab/led_test-schematic.pdf).

## Circuit
`J1.1 (+5V) → R1 620 Ω → D1 anode | D1 cathode → J1.2 (GND)`. Calculations in
[`calculations/v0.0.2/led_current.md`](../../calculations/v0.0.2/led_current.md).

## Symbols placed (add_schematic_component)
| Ref | Symbol | Value | Footprint | MPN / Manufacturer | Position, angle |
|---|---|---|---|---|---|
| J1 | Connector:Screw_Terminal_01x02 | 5V_IN | TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal | 1715721 / Phoenix Contact | (40.64, 80.01), 0° |
| R1 | Device:R | 620 | R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal | MFR-25FBF52-620R / Yageo | (60.96, 80.01), 0° |
| D1 | Device:LED | Red | LED_THT:LED_D5.0mm | WP7113ID / Kingbright | (60.96, 92.71), 90° |
| #PWR01–02 | power:+5V | +5V | — | — | at J1 side and above R1 |
| #PWR03–04 | power:GND | GND | — | — | at J1 side and below D1 |
| #FLG01–02 | power:PWR_FLAG | — | — | — | on +5V (via R1.1) and GND (via D1.K) |

## Pin numbering and polarity (VERIFIED)
| Symbol | Pins from `batch_list_symbol_pins` | Placed pin location (`get_schematic_pin_locations`) | Datasheet check |
|---|---|---|---|
| Device:LED | 1 = K, 2 = A | A (pin 2) at (60.96, 88.90) on top, K (pin 1) at (60.96, 96.52) on the bottom | Current flows R1 → A → K → GND. Footprint pad 1 (square) = K = flat side, per Kingbright p.1 |
| Device:R | 1, 2 (passive) | 1 at y 76.20, 2 at y 83.82 | non-polar |
| Screw_Terminal_01x02 | 1 = Pin_1, 2 = Pin_2 | 1 at (35.56, 80.01), 2 at (35.56, 82.55) | Pin 1 = +5V, pin 2 = GND, also marked on silkscreen |

## Wiring (add_schematic_wire, snapToPins on)
7 wires. The tool's response confirmed that **every start and end point snapped to a pin**:
J1/1→#PWR01, J1/2→#PWR03, #PWR02→R1/1, R1/1→#FLG01, R1/2→D1/2, D1/1→#PWR04, D1/1→#FLG02.
No wire ends in the middle of another wire, so no junctions are needed.

Net naming: a **global label `LED_A`** on R1 pin 2 (see D-2 for why it is global, not local).

## Results
| Check | Tool | Result |
|---|---|---|
| File structure | validate_schematic (+ kicad-cli load on a copy) | PASS: valid, 0 errors, 9 components |
| ERC | run_erc / kicad-cli | PASS: 0 (see ERC_REPORT.md) |
| Netlist | generate_netlist / kicad-cli | PASS: identical (see ERC_REPORT.md) |
| Readability | get_schematic_view | WARNING (cosmetic): PWR_FLAG value text overlaps the +5V/GND symbol text near R1/D1. No electrical impact. Fixable later with the `schematic_layout` toolbox (not tested) |

## Tool behaviour notes
- Angles follow KiCad's CCW convention. `angle 90` on Device:LED put the anode on top, as predicted.
- Coordinates come back with floating-point noise (`82.55000000000001`). KiCad loads and saves the file normally.
- Custom fields added with `set_schematic_component_property` are hidden by default.
