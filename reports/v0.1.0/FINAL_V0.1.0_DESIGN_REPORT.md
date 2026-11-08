# Final Design Report — V0.1.0
**Sensor Interface & Power Management Board for ESP32** · 2026-11-08 · branch `design/v0.1.0-phase1`

## 1. Status
**COMPLETE (electrical design and schematic), with physical dependencies.**
- Digitally validated: ERC 0 (MCP and kicad-cli, all severities, no exclusions). Netlist matches the design table.
  Domain, footprint and metadata checks pass. Calculations and independent checks pass.
- **Not production-ready, NOT TESTED physically.** No PCB layout, fabrication or measurement exists yet.

## 2. What the board does
| Function | Implementation |
|---|---|
| Power input | 5 V ±5 % on J1 (Phoenix 1715721) → F1 PTC 0.5 A → Q1 P-MOSFET reverse protection → D1 TVS → `+5V_P` |
| 3.3 V peripheral rail | U1 TLV1117LV33 → `+3V3_P` (I2C, UART, GP connectors). LEDs on both rails |
| ESP32 interface | J2 1×12 header, cable to a DevKitC-compatible ESP32 (Architecture B: DevKit on its own USB) |
| Ultrasonic | J3 (VCC 5 V, TRIG, ECHO, GND). TRIG via SN74LVC1T45 (3.3 → 5 V). ECHO via SN74LVC1G17 (5.5 V-tolerant) |
| I2C | J5. 2.2 kΩ pull-ups to 3V3_ESP, disconnectable (JP2) |
| UART | J4. VCC 3.3/5 V (JP1). TX 220 Ω series. RX via SN74LVC1G17 |
| GP | J6. GPIO32/33 with 1 kΩ series |
| Test | TP1–TP8 (VIN, 5V, 3V3, 3V3_ESP, GND×2, ECHO_ESP, TRIG_5V) |

GPIO map: TRIG 26, ECHO 34, SDA 21, SCL 22, TX 17, RX 16, GP 32/33. No strapping, flash or UART0 pins (DDR-13).

## 3. Key engineering decisions
See [DESIGN_DECISION_RECORD.md](DESIGN_DECISION_RECORD.md) (DDR-01…16). In short:
- **Architecture B** ([POWER_ARCHITECTURE.md](POWER_ARCHITECTURE.md)). There is no path between the board rails and the DevKit 5V/3V3 outputs.
  `3V3_ESP` is used only as a ≤ 3.4 mA logic reference. `+3V3_P` ∩ `3V3_ESP` = ∅ (tool-checked).
- **Variant-independent ultrasonic interface.** The design does not depend on the unpublished sensor thresholds.
- **Mechanical Option B** (cable). Option A (stacked) is deferred until a verified clone drawing exists.

## 4. Calculations (CALCULATED, `calculations/v0.1.0/`)
| Quantity | Worst-case result | Limit / margin |
|---|---|---|
| Input current | 275.7 mA | PTC hold 0.40 A at 50 °C (×1.45) |
| `+5V_P` | 4.439–5.250 V | sensor 3–5.5 V. LDO headroom 1.139 V |
| `+3V3_P` | 3.215–3.349 V | 3.3 V ±5 % |
| LDO | 0.505 W, Tj 81.8 °C at 50 °C | 125 °C (43 °C margin). 110.6 °C even at RθJA 120 |
| Echo at buffer | 4.394 V vs VT+ 2.25 V | +2.15 V |
| Buffer VOH at ESP32 | margins +0.65/0.73/0.80 V | ≤ VDD by construction |
| TRIG | ≥ 4.34 V (98 % of sensor VCC) | input margin +0.40 V |
| I2C | Rp(min) 1067 Ω. 2.2 kΩ supports 159 pF (Fm) / 400 pF (Sm) | UM10204 |
Independent Monte Carlo check: 10/10 PASS, 0 violations ([POWER_BUDGET_FINAL.md](POWER_BUDGET_FINAL.md),
[SIGNAL_COMPATIBILITY.md](SIGNAL_COMPATIBILITY.md)).

## 5. Components
48 BOM parts, all with manufacturer MPN and an official datasheet (DS-01…16), except the off-board
ultrasonic module (vendor data only). See [COMPONENT_SELECTION.md](COMPONENT_SELECTION.md) and
[DATASHEET_VERIFICATION.md](DATASHEET_VERIFICATION.md).

## 6. Schematic
`hardware/kicad/Sensor_Interface_Power_Board/Sensor_Interface_Power_Board.kicad_sch`: A3, 50 parts + 3 PWR_FLAGs,
27 design nets. Built through the KiCAD-MCP-Server (SWIG), 326 calls with 0 failures. One documented non-MCP edit
(paper size and title block). Review: [SCHEMATIC_DESIGN_REVIEW.md](SCHEMATIC_DESIGN_REVIEW.md). Validation:
[ERC_VALIDATION.md](ERC_VALIDATION.md).

## 7. Phase 1 risk status after design
| Risk | Status |
|---|---|
| R-01 Echo 5 V into GPIO | Mitigated: 5.5 V-tolerant buffer at 3V3_ESP (calc + MC) |
| R-02 Trigger VIH unknown | Mitigated: TRIG at the sensor's own 5 V rail |
| R-03 Two supplies into DevKit | Eliminated by Architecture B (DevKit 5V not wired) |
| R-04 Back-powering ESP32 | Mitigated (Ioff buffers, pull-ups to 3V3_ESP). Residual GP ≤ 2.75 mA |
| R-05 Reverse-polarity drop | Mitigated: P-MOSFET, 35 mV worst |
| R-06 / R-15 LDO thermal | Calculated OK. Copper area set in V0.2.0. Thermal test in V0.3.0 |
| R-07 TX brown-out | Not applicable in Architecture B |
| R-08 I2C pull-up mismatch | Mitigated: JP2 |
| R-09 Wrong pinout | Mitigated: GPIO-number interface. Clone pinout read on receipt (NQ-03) |
| R-10 Strapping pins | Eliminated (none used) |
| R-11 ESD | Partially mitigated (TVS on input, series resistors). Arrays deferred (OQ-18) |
| R-12 HC-SR04 data | Mitigated (variant-independent). Measurement pending |
| R-13 Burst noise | Local decoupling C8/C9 at J3. Measure in V0.3.0 |
| R-14 PTC derating | Calculated (×1.20 at 70 °C) |
| R-16…R-18, R-22 | Layout phase (V0.2.0) |
| R-19 Fab rules | Open (OQ-16) |
| R-20 Availability | Checked at selection. Recheck before order |
| R-21 MCP defects | Mitigated: independent kicad-cli ERC + netlist verifier |
New risks R-30…R-35 are in `docs/requirements/v0.1.0/RISK_REGISTER.md`.

## 8. Remaining dependencies
See [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md):
- Ultrasonic pin order (NQ-01).
- Clone header pinout for the harness (NQ-03).
- Fab/assembly choice and rules (OQ-16, needed before V0.2.0 DRC).
- Physical measurements (NQ-02, NQ-04).
- Power-sequencing rule (R-31).

## 9. Readiness for V0.2.0 (PCB layout)
**Ready, with conditions:**
1. The owner selects the fab/assembly method (OQ-16), so its design rules can be entered.
2. The J3 pin order is confirmed or accepted as VCC/TRIG/ECHO/GND.
3. Layout gives U1 tab copper sized for RθJA ≤ about 90 °C/W, and keeps the TVS and decoupling close to their pins.
4. The mechanical interface stays Option B unless a verified DevKit drawing is provided.
