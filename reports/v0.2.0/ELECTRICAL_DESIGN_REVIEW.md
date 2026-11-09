# Electrical Design Review — V0.2.0 (Gate A)

Gate A was completed before any placement or routing. The schematic changed **only** as documented below (V0.1.0
remains intact at git `06f223c`; its PDF is in `reports/v0.1.0/evidence/`).

## 1. Schematic revisions
| ID | Change | Reason | Evidence |
|---|---|---|---|
| DDR-17 | F1, Q1, R1, D1 removed. U5 TPS26600PWPR + C12, C13, R16–R19 added | TVS could not protect the LDO (VBR 6.67 V > 6.0 V abs max); OVP eFuse protects the whole 5 V rail | TVS_LDO_PROTECTION_ANALYSIS.md |
| DDR-18 | R15 1 kΩ in series with TRIG (U3-B → J3-2) | Limits contention if TRIG/ECHO are mis-wired (≤ 5.2 mA) and ESD current into U3. TRIG still ≥ 96.9 % of sensor VCC | design_calcs_v020 §9 |
| DDR-19 | H1–H4 (M3) and FID1–FID3 added to the schematic, not in BOM | Keeps DRC schematic parity exact; mechanical features | DRC_VALIDATION.md |
| DDR-20 | Project footprint for U5 per TI PWP0016A | KiCad library footprint follows the older PWP0016H pattern | FOOTPRINT_VERIFICATION.md |
| DDR-21 | +3V3_P copper ≥ 194 mm² on U1 tab, solid connection | JEDEC RθJA not valid on 2 layers | POWER_AND_THERMAL_REVIEW.md |

ERC after the revision: 0 (MCP and kicad-cli, all severities). The netlist verifier passes (31 nets, eFuse RTN ≠ GND,
TRIG series R present).

## 2. Power-domain review (§5.3)
| Check | Result | Evidence |
|---|---|---|
| +3V3_P ∩ 3V3_ESP | none (no shared node) | verify_output.txt [2] |
| +5V_P to DevKit 5V | not connected (J2 has 3V3_ESP, GND and signals only) | netlist |
| ESP32-facing nets touch only 3.3 V-domain parts | PASS (8 nets) | verify_output.txt [2] |
| Translator supplies | U3 VCCA = 3V3_ESP, VCCB = +5V_P, DIR = VCCA (A→B). U2/U4 VCC = 3V3_ESP | netlist + DS-07/08 |
| I2C pull-ups | 2.2 kΩ to 3V3_ESP via JP2 (bridged) | netlist |
| UART logic | TX 3.3 V CMOS via 220 Ω. RX via LVC1G17 (accepts 3.3/5 V). VCC 3.3 V (JP1 1-2 default) or 5 V | netlist |
| eFuse RTN | separate island EF_RTN. GND pin 9 on GND | verify_output.txt |

### Back-feed paths and power-sequencing rule R-31
| Condition | Path | Current bound | Effect |
|---|---|---|---|
| Board OFF, ESP32 ON | 3V3_ESP → R8/R9 2.2 kΩ → I2C device clamps → +3V3_P → U1 body diode → +5V_P | ≤ 2 × (3.3 − 0.6)/2.2 k ≈ 2.5 mA | +5V_P rises to ~2 V. eFuse reverse blocking stops it at VIN_RAW. No damage, but unpowered peripherals are back-fed |
| Board OFF, ESP32 ON | GPIO17 TX → R10 220 Ω → UART device clamp | ≤ 12 mA (device dependent) | possible stress on an unpowered UART device |
| Board OFF, ESP32 ON | GPIO32/33 → 1 kΩ → GP device | ≤ 2.7 mA | low |
| Board ON, ESP32 OFF | U2/U4 VCC = 3V3_ESP = 0 V; inputs Ioff-protected. U3 A side Ioff | ≤ 10 µA | none (no drive into the ESP32) |
**Rule R-31 (silk legend and docs): power this board before or together with the ESP32.** Routing adds no
other paths: the netlist is identical to the schematic (DRC parity 0).

## 3. Ultrasonic interface (§5.4)
- U3 SN74LVC1T45: pin 3 A ← GPIO26, pin 4 B → R15 → J3-2, DIR (pin 5) = VCCA → A→B (DS-08 function table).
  100 k pull-downs on A (R4) and on the connector side (R5) keep TRIG low when the ESP32 is unpowered or reset.
- U2 SN74LVC1G17: pin 2 A ← R6 1 k ← J3-3 (R7 100 k pull-down), pin 4 Y → GPIO34. VI ≤ 5.5 V independent of VCC.
- Decoupling: C6/C7 3.2–3.4 mm, C10 5.6 mm, C8/C9 at J3.
- **J3 pin order:** Adafruit documents the signal names "VCC, trig, echo, GND" (learn.adafruit.com
  ultrasonic-sonar-distance-sensors, read 2026-11-09). The **physical pin order of the 4007 module is not
  published** (the dimension drawing has no labels). The board interface is therefore defined as one labelled
  2.54 mm header (1 +5V, 2 TRIG, 3 ECHO, 4 GND, printed on silk). The module connects with four individual
  female–female jumper wires, matched by label. The board works for any module pin order. Status: **mechanical
  mating NOT VERIFIED until the module is in hand (NQ-01)**.

## 4. DevKit interface (§5.5) — J2 wiring table (also on silkscreen)
| J2 pin | Net | DevKit pin (by label) | Direction | Level |
|---|---|---|---|---|
| 1 | 3V3_ESP | 3V3 | DevKit → board (reference only, ≤ 3.4 mA) | 3.3 V |
| 2, 11, 12 | GND | GND | — | — |
| 3 | US_TRIG_ESP | GPIO26 | out | 3.3 V |
| 4 | US_ECHO_ESP | GPIO34 (input-only) | in | ≤ VDD |
| 5 / 6 | I2C_SDA / SCL | GPIO21 / GPIO22 | bidir (open-drain) | 3.3 V |
| 7 | UART_TX_ESP | GPIO17 (TX2) | out | 3.3 V |
| 8 | UART_RX_ESP | GPIO16 (RX2) | in | ≤ VDD |
| 9 / 10 | GP_IO1/2_ESP | GPIO32 / GPIO33 | bidir via 1 kΩ | 3.3 V |
The DevKit **5V/VIN pin must not be wired** (Architecture B). No DevKit dimensions are used; the cable is
wired by DevKit pin labels.

## 5. I2C (§5.6)
Rp 2.2 kΩ ±1 % to 3V3_ESP. Rp(min) is 1067 Ω at 3.6 V (3 mA sink), so it passes. Allowed bus capacitance is 159 pF
(Fast-mode, 300 ns) and 400 pF (Standard-mode). Board contribution ≈ 10 pF (ASSUMED, ~45 mm tracks + 2 headers),
leaving ≈ 149 pF for cable and devices in Fast-mode. Device pull-ups in parallel lower Rp: cut JP2 if the modules
already have ≤ 4.7 kΩ. Start-up: the pull-ups are powered from the ESP32 rail, so R-31 applies.

## 6. Gate A verdict
**PASS.** Every absolute maximum is respected under the defined protection conditions, the remaining
limitations are documented, and nothing unsafe was routed.
