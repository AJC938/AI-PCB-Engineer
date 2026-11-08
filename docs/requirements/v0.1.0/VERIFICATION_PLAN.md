# Verification Plan — V0.1.0

Evidence is stored in `reports/` (design checks) and `testing/` (physical results), with the instrument,
conditions, date and photos. Nothing is claimed as passed without a recorded measurement.
Numeric limits marked TBD are fixed at design freeze from the selected parts and the answered open questions.

## 1. Design verification (before fabrication)
| Check | Method | Acceptance |
|---|---|---|
| ERC | `kicad-cli sch erc --severity-all` | 0 violations. Any exclusion justified in writing |
| DRC + parity | `kicad-cli pcb drc --severity-all --schematic-parity --refill-zones` | 0 violations, 0 unconnected, 0 parity issues |
| Fab rules | DRC rule set = recorded manufacturer capabilities | rules file referenced to its source and date (MFG-02) |
| Netlist review | CLI netlist vs INTERFACE_SPEC pin tables | every connector pin and GPIO matches. No 5 V net touches a GPIO net (ESP-03) |
| Calculations | `calculations/v0.1.x/` re-run with selected-part values | margins documented for US-04, PWR-11, I2C-03, PWR-03 |
| Footprints | Datasheet land patterns vs `.kicad_mod` (pads, pitch, drill, pin 1) | recorded per part |
| 3D/mechanical | 3D render with DevKit and connectors | MECH-02/03, USE-02 satisfied |
| Fab outputs | Gerber/drill/BOM/CPL inspection (`ai/workflows/inspect_fab_outputs.py`) | dimensions, drills and references correct |

## 2. Assembly inspection
Visual inspection under magnification: polarity of LEDs, diodes and the input connector. Solder joints. No
bridges. Pin-1 orientation. Photos recorded. Unpowered resistance checks `VIN`–`GND`, `+5V_P`–`GND`,
`+3V3_P`–`GND` are each > TBD Ω (no shorts).

## 3. Power tests (DevKit NOT fitted first)
| Test | Setup | Acceptance |
|---|---|---|
| P1 First power-up | Bench supply 5.0 V, current limit 100 mA | Input current < TBD mA idle. LEDs on |
| P2 Rail voltages | DMM at TP_5V, TP_3V3, no load and with dummy loads up to budget | `+5V_P` ≥ TBD V at full load. `+3V3_P` within the regulator tolerance |
| P3 Reverse polarity | Reversed 5.25 V (OQ-05), current limit 200 mA, 60 s | No damage. Rails ≥ −0.3 V (or the documented safe value). Board works after re-polarising |
| P4 Overcurrent | Short `+5V_P` through the load (planned procedure) | Protection acts within the datasheet trip time. Recovers (PTC/eFuse) |
| P5 Ripple/noise | Scope at TP_5V/TP_3V3, 20 MHz BW, short ground spring | ≤ TBD mVpp (from device requirements) |
| P6 Thermal | Maximum load, 30 min, thermocouple/IR on the regulator and protection parts | Tj estimate within rating with margin (PWR-11) |
| P7 Arch. A only: Wi-Fi TX transient | DevKit fitted, continuous TX, scope on `+5V_P` | Rail stays ≥ TBD V. No brown-out resets |
| P8 Back-feed checks | Arch. A: USB present + link rule. Arch. B: DevKit off while board on | No current into the USB host. GPIO voltages within ESP-03 |

## 4. Signal tests
| Test | Method | Acceptance |
|---|---|---|
| S1 Echo level | Sensor fitted, scope at the GPIO side of the conditioning (DevKit absent, then present) | HIGH within [0.75·VDD, VDD+0.3] V. LOW ≤ 0.25·VDD (US-04) |
| S2 Trigger | Scope at J_US TRIG under firmware toggle. Sensor responds (Echo pulse present) | Sensor responds 100/100 triggers (US-05) |
| S3 Ranging sanity | Target at known distances (e.g. 20/50/100 cm) | Readings consistent with expected time of flight. Tolerance TBD |
| S4 I2C | Bus scan with the intended device(s). Scope rise time on SDA/SCL | Devices ACK. tr ≤ 1000 ns (Std) / 300 ns (Fast) (REF-04) |
| S5 UART | Loopback at J_UART, then the intended device | Error-free at the intended baud rate. Levels within ESP-03 |
| S6 GPIO safety | Scope or DMM on every board-driven GPIO net during power-up and power-down | Never above VDD + 0.3 V |

## 5. Acceptance criteria for V0.1.0 hardware
All Must requirements verified per their method. P1–P6, S1, S2, S4 and S5 passed with recorded evidence. No open
R-score-6 risk without mitigation evidence. Deviations listed with justification. Until then, the board
status is **"not validated"**.
