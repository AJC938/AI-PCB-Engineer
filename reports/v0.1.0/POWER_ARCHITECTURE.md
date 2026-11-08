# Power Architecture — V0.1.0

Numbers come from [`calculations/v0.1.0/design_calcs.py`](../../calculations/v0.1.0/design_calcs.py)
([output](../../calculations/v0.1.0/design_calcs_output.txt)) and were checked independently by
[`independent_checks.py`](../../calculations/v0.1.0/independent_checks.py) (Monte Carlo, 0 violations).

## Candidates
### Architecture A: the board supplies the ESP32 DevKit (via its 5V pin)
| Aspect | Finding |
|---|---|
| ESP32 demand | Supply must deliver ≥ 0.5 A. TX peaks 379 mA (DS-02) |
| Input current | about 0.78 A worst (Phase 1 budget) + DevKit regulator and USB bridge (unknown for the clone) |
| Distribution losses | PTC R1max 1 Ω at 0.78 A gives 0.78 V, which would drop `+5V_P` to about 3.9 V. A larger PTC is needed, increasing fault energy |
| USB back-feed | DevKit allows **one and only one** power source (DS-02b). The clone's VBUS↔5V-pin path (diode or not) is **unknown**, so plugging USB while the board powers the DevKit risks damage to the board, DevKit or PC port |
| Simultaneous-source prevention | Would need ideal-diode OR-ing or a hard interlock, plus verification on the real clone |

### Architecture B (selected): DevKit on its own USB, board powers peripherals
| Aspect | Finding |
|---|---|
| Separate domains | `+5V_P`/`+3V3_P` (board) and the DevKit's own 3.3 V (`3V3_ESP`). No supply connection between them. The DevKit 5V pin is **not wired** |
| Shared ground | Required for signal reference. Three GND pins on J2 |
| Signal references | Every ESP32-facing driver/receiver is powered from **3V3_ESP** (U2, U4, U3-A side, pull-ups), so its levels track the ESP32's VDD by construction |
| Back-power paths | ESP32 off and board on: U2/U4/U3 lose VCC, become high-Z with Ioff ≤ 10 µA (DS-07/08), so no drive into the GPIOs. I2C pull-ups follow 3V3_ESP. **Residual:** GP_IO inputs through 1 kΩ (≤ 2.75 mA, injection limit not published) and the UART TX line into an unpowered device |
| Board off, ESP32 on | I2C pull-ups (3V3_ESP) can pull SDA/SCL of unpowered I2C devices high through their protection diodes (≤ 1.6 mA per line). Operating rule: power the board before or with the ESP32 (R-31) |
| Sensor supply capacity | `+5V_P` ≥ 4.44 V at the worst-case 276 mA total. `+3V3_P` rated 250 mA (I2C 100, GP 50, UART 100) |

### Architecture C: board 3.3 V into the DevKit 3V3 pin
Rejected. It bypasses and fights the DevKit regulator, and violates the one-source rule whenever USB is connected.

## Comparison
| Criterion | A | B |
|---|---|---|
| Compliance with Espressif one-source rule | Only with extra OR-ing hardware + clone verification | **By construction** |
| Input current / protection sizing | about 0.8–1.0 A | **0.28 A** |
| Dependence on unknown clone internals | High (VBUS path, regulator) | **None** (3V3 pin used as a ≤ 3.4 mA reference) |
| Supplies needed in use | One | Two (USB + 5 V input) |
| Back-power risks | Lower (single source) | Mitigated by Ioff buffers. Residual GP/I2C items documented |
| Programming/debug convenience | USB must be unplugged or OR-ed | USB always available |
**Selected: B.** It is the safest practical architecture for the first board. Its consequences (two supplies,
a power-sequencing rule) are operational, not hazards. A remains a candidate for V0.2.x once the physical
DevKit is characterised.

## Rails (CALCULATED, worst case)
| Rail | Min | Nom | Max | Expected / max current | Notes |
|---|---|---|---|---|---|
| VIN (spec) | 4.75 V | 5.00 V | 5.25 V | — / 276 mA | DESIGN input specification |
| `+5V_P` | **4.44 V** | 4.82 V | 5.25 V | about 30 mA direct + LDO input / 276 mA total | PTC R1max and hot RDS(on) included |
| `+3V3_P` | **3.215 V** | 3.300 V | 3.349 V | — / 252 mA | TLV1117LV ±1.5 %, load reg ≤ 35 mV |
| `3V3_ESP` | DevKit regulator (3.0–3.6 V assumed per ESP32 range) | — | — | ≤ 3.4 mA drawn | not generated on this board |

## Protection chain (J1 → F1 → Q1 → +5V_P, D1 on +5V_P)
| Element | Check | Result |
|---|---|---|
| F1 MF-MSMF050-2 | Ihold 0.40 A at 50 °C vs 0.276 A | PASS ×1.45 (×1.20 at 70 °C) |
| F1 | Vmax 15 V vs 5.25 V. Dissipation ≤ 76 mW | PASS |
| Q1 AO3401A | VGS −4.47 V at VIN min, so RDS(on) bound 85 mΩ (2.5 V spec) ×1.5 hot = 35 mV, 9.7 mW | PASS |
| Q1 reverse | −5.25 V input: VGS ≈ 0 (off), body diode reverse-biased, |VDS| 5.25 V < 30 V | PASS (rails see no negative voltage) |
| Q1 gate | VGS ≤ 10.3 V during TVS clamp < ±12 V rating | PASS |
| D1 SMAJ6.0A | VWM 6.0 V > 5.25 V (no conduction), leakage ≤ 0.8 mA | PASS |
| D1 clamp | 10.3 V at 38.8 A > LDO abs max 6 V and LVC 6.5 V | **Limitation**: transient/ESD aid only, not surge-proof or overvoltage protection (R-32) |

## 3.3 V regulator selection
| Option | Dissipation at 252 mA | Assessment |
|---|---|---|
| **LDO TLV1117LV33 (SOT-223)** | 0.505 W, giving Tj 81.8 °C at 50 °C ambient (RθJA 62.9) | **Selected**: no switching noise near sensor lines, few parts, 43 °C margin. Sensitivity: RθJA 120 °C/W still gives Tj 110.6 °C < 125 °C |
| Buck converter | about 0.15 W | Not needed at this load. Adds inductor, EMI and layout risk |
The LDO's RθJA assumes a JEDEC high-K board. **V0.2.0 must give the SOT-223 tab (OUT) a copper area.**
