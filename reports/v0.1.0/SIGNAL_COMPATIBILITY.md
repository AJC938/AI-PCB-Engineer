# Signal Compatibility — V0.1.0

All limits are from manufacturer datasheets (DS-xx). Margins are CALCULATED worst case and confirmed by
Monte Carlo (`independent_checks_output.txt`). ESP32 VDD range 3.0–3.6 V throughout.

## Ultrasonic module selection
| Candidate | Supply | Echo level | Trigger threshold | Documentation | Verdict |
|---|---|---|---|---|---|
| **Adafruit 4007** (RCWL-1601) | 3–5.5 V, 2.2 mA (VENDOR) | equals supply ("logic level will be the same", VENDOR) | not published | vendor product page + dimension drawing | **Selected** (best documented, low current, in stock per vendor page 2026-11-08) |
| Adafruit 3942 (HC-SR04, 5 V only) | 5 V (VENDOR) | not checked | not published | vendor page (not read in detail) | Alternate. The interface also works (see "variant independence") |
| Generic HC-SR04 clones | 5 V, about 15 mA (SECONDARY) | about 5 V TTL (SECONDARY) | unknown | none from a manufacturer | Not selected |
| Price/availability | Adafruit page: in stock, USD 3.95 (2026-11-08) | | | | No purchase made |

**Design choice that removes the unknowns:** the sensor is always powered from `+5V_P` (4.44–5.25 V). TRIG is
driven at a full 5 V CMOS level by the translator, and ECHO is received by a 5 V-tolerant buffer. The
interface therefore works for Echo HIGH levels from about 2.3 V up to 5.5 V, and for any trigger input
threshold ≤ about 0.9 × sensor VCC.

## ECHO path: J3-3 → R6 1 kΩ → U2 SN74LVC1G17 (VCC = 3V3_ESP) → GPIO34
| Check | Limit (source) | Worst case | Margin |
|---|---|---|---|
| Echo HIGH at buffer input | ≥ VT+ max 2.25 V (DS-07, interpolated at VCC 3.6 V) | 4.39 V (+5V_P min, 1k/100k divider) | **+2.15 V** |
| Echo HIGH max | ≤ 5.5 V VI (DS-07, independent of VCC) | 5.25 V | +0.25 V |
| Echo LOW | ≤ VT− min 0.89 V (DS-07 at 3 V) | module VOL not published | **Measure (S1)** |
| Buffer → GPIO HIGH | ≥ 0.75·VDD (DS-01) | VOH ≥ VDD − 0.1 V | +0.65 V (VDD 3.0) … +0.80 V (3.6) |
| Buffer → GPIO max | ≤ VDD + 0.3 V | ≤ VCC = VDD | **+0.30 V** by construction |
| ESP32 off | no back-drive | Ioff ≤ 10 µA, output high-Z (DS-07) | PASS |
| Timing | echo pulse µs–ms | tpd < 5 ns. RC 1 kΩ × 4.5 pF ≈ 5 ns | negligible |

## TRIG path: GPIO26 → U3 SN74LVC1T45 A (VCCA = 3V3_ESP, DIR = H) → B (VCCB = +5V_P) → J3-2
| Check | Limit | Worst case | Margin |
|---|---|---|---|
| GPIO HIGH into translator | VIH 2.0 V (DS-08, VCCI 3–3.6 V) | VOH 0.8·VDD = 2.40 V at VDD 3.0 | **+0.40 V** |
| TRIG HIGH at sensor | sensor VIH (not published) | ≥ 4.34 V = 98 % of sensor VCC | covers any threshold ≤ 0.9·VCC. Verify S2 |
| Defined state at ESP32 boot | — | R4 100 kΩ pull-down (A side), R5 100 kΩ (B side, active when VCCA off) | no spurious trigger |
| Supply isolation | either VCC = 0 → both ports high-Z (DS-08) | — | PASS |
| Pulse | ≥ 10 µs (module convention, SECONDARY) | tpd < 10 ns | unaffected |

## I2C: GPIO21/22 ↔ J5, devices on `+3V3_P`, pull-ups 2.2 kΩ to 3V3_ESP (JP2, bridged by default)
| Check | Limit (UM10204 Rev 7.0) | Value | Result |
|---|---|---|---|
| Rp(min) at VDD 3.6 V | 1067 Ω | 2178 Ω (2.2 k −1 %). 1803 Ω with a 10 k module pull-up | PASS |
| Standard-mode | Cb ≤ 400 pF | supported to 400 pF | PASS |
| Fast-mode | tr ≤ 300 ns | supported to **159 pF** bus capacitance | PASS if cable + devices ≤ 159 pF (measure tr, S4) |
| Sink current | ≤ 3 mA | 1.64 mA | PASS |
| Level shifting | — | none: 3.3 V devices only (I2C-02). 5 V-logic I2C devices unsupported | by design |
| Disabling on-board pull-ups | — | cut JP2 if modules already provide pull-ups | provided |

## UART: J4 (pin 3 TX = ESP32 → device, pin 4 RX = device → ESP32)
Signal direction is named from the **ESP32 side**. The connector pin order is `1 GND, 2 VCC, 3 TX, 4 RX`.
| Path | Design | Check | Result |
|---|---|---|---|
| RX (device → ESP32) | J4-4 → 1 kΩ → U4 SN74LVC1G17 → GPIO16. 100 kΩ pull-up to 3V3_ESP | accepts 3.3 V and **5 V** device TX (VI ≤ 5.5 V). Output ≤ VDD | PASS |
| TX (ESP32 → device) | GPIO17 → 220 Ω → J4-3 | VOH ≥ 2.64 V vs 3.3 V-device VIH 2.31 V. Short-circuit current ≤ 16.4 mA | PASS for 3.3 V devices. **5 V CMOS-input devices unsupported** |
| VCC | JP1 selects `+3V3_P` (default) or `+5V_P` | — | label on silkscreen (V0.2.0) |

## GP connector J6 (3.3 V only)
GPIO32/33 through 1 kΩ series resistors. Inputs must stay ≤ VDD + 0.3 V, so **5 V sensors are not allowed**
(silkscreen label). Back-power ≤ 2.75 mA if driven while the ESP32 is off (R-04, residual).

## Summary of compatibility status
| Interface | Status |
|---|---|
| ECHO | VERIFIED by calculation + datasheets. LOW level to be measured |
| TRIG | VERIFIED translator margins. Sensor threshold to be confirmed by S2 |
| I2C | VERIFIED for 3.3 V devices. Bus capacitance to measure |
| UART | VERIFIED for 3.3 V devices and 5 V device TX. 5 V CMOS RX unsupported |
| GP | 3.3 V only, residual back-power risk documented |
