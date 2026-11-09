# PCB Placement Review — V0.2.0

Single source of truth: `hardware/kicad/Sensor_Interface_Power_Board/build/build_pcb.py` (dictionary `P`). It
was checked offline (`build_pcb.py check`: courtyards, edge ≥ 0.5 mm, hole keep-outs → PASS), written with MCP
`move_component` (65/65 OK), and read back with pcbnew (`pcb_extract.py`: 61/61 footprints at plan position and
rotation).

## Board
| Item | Value | Rationale |
|---|---|---|
| Outline | **90.0 × 64.0 mm** rectangle (MCP `add_board_outline`) | Fits the power chain across the top, four edge connectors on the right and the ESP32 header at the bottom. Not minimised at the expense of routing or thermal copper |
| Layers | 2 (F.Cu signals/power, B.Cu GND plane) | low-speed design; DFM profile |
| Assembly side | top only | single reflow pass; no bottom paste |
| Mounting | 4 × M3 NPTH (3.5 mm from each corner) | generic standoffs. **No DevKit dimensions used** (cable interface, Option B) |
| Fiducials | 3 global (9,25), (60,50), (12,50) mm from top-left | non-collinear triangle for the pick-and-place vision system |
| Origin | aux/drill origin at the bottom-left corner (MCP `set_board_origin`) | CPL/Gerber/drill coordinates start at (0,0) |

## Functional zones (local mm, origin top-left)
| Zone | Parts | Reasoning |
|---|---|---|
| Power entry (x 0–31, y 4–23) | J1 (left edge, wire entry outward), TP1, C12, U5, R16–R19, C13, RTN island | Input → eFuse in signal-flow order. C12 is 3.3 mm from U5 IN. ILIM/dVdT parts 2.6/4.6 mm from their pins (TI §12.1). The RTN island sits directly below U5 |
| 5 V distribution and LDO (x 31–57) | C1, C2, C5, TP2, U1, C3, C4, TP3 | U1's tab faces right into the 251 mm² +3V3_P thermal copper. Nothing else sits inside the thermal area except TP3 (same net) |
| Indicators (x 57–64) | LED1 (+5V), LED2 (+3V3), R2, R3 | visible, beside their rails |
| Ultrasonic (x 65–84, y 4–26) | J3, U3, U2, R4–R7, R15, C6–C10, TP7, TP8 | Conditioning sits next to J3, so the 5 V signals stay short (≤ 20 mm) and only 3.3 V signals run to J2 |
| UART / I2C / GP (x 70–84, y 22–56) | J4, J5, J6, U4, R8–R14, JP1, JP2, C11 | each group beside its connector. Solder jumpers reachable |
| ESP32 cable (bottom edge) | J2 (pin 1 left), TP4 (3V3_ESP), TP5 (GND) | cable leaves the board edge. Test points next to it |
| Free area (x 1–30, y 26–56) | silkscreen pin-map legend | unambiguous wiring without external documents |

## Clearances and access
- **Connectors.** All six sit at board edges, with pin 1 marked. Mating-housing gap between J3/J4/J5/J6 is ≥ 1.8 mm
  (12 mm pitch for 10.16 mm housings). J2 is 2.2 mm from the bottom edge.
- **Test points.** TP1 VIN, TP2 +5V, TP3 +3V3, TP4 3V3_ESP, TP5/TP6 GND, TP7 ECHO_ESP and TP8 TRIG_5V are all on
  top, none under connectors. Every rail has a nearby GND (TP5 bottom-left, TP6 centre). No test point exposes
  more than 5.25 V.
- **Heat.** U1 is the only significant heat source (0.5 W). The logic ICs are ≥ 25 mm away.
- **Courtyards.** No overlaps (offline check, plus KiCad DRC courtyard rules: 0 violations).

## Placement findings
| # | Finding | Disposition |
|---|---|---|
| P-1 | C3/C4 are 7.6–8.8 mm from U1 OUT (placed in a notch of the thermal zone for their GND vias) | WARNING accepted; low-inductance zone path. V0.3.0 transient check |
| P-2 | The left-centre area is used only for silkscreen | Accepted: it gives the board a self-documenting wiring legend |
| P-3 | The J1 horizontal terminal block overhangs nothing (front face 0.9 mm inside the edge) | PASS (3D left view) |
