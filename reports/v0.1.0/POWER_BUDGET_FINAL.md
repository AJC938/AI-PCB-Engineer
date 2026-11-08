# Power Budget (final, V0.1.0, Architecture B)

Supersedes the planning budget in `docs/requirements/v0.1.0/POWER_BUDGET.md`. Source:
`calculations/v0.1.0/design_calcs.py` §1–5 and §13. Tags: VERIFIED / VENDOR / DESIGN (rating) / ASSUMED.

## Loads
| Load | Rail | Typical | Worst case used | Tag / source |
|---|---|---|---|---|
| ESP32 DevKit | own USB | — | **0 on this board** (Arch. B) | design decision |
| Ultrasonic (Adafruit 4007) | +5V_P | 2.2 mA | 20 mA allocation (covers a classic HC-SR04 at about 15 mA) | VENDOR / DESIGN |
| SN74LVC1T45 VCCB | +5V_P | — | 4 µA | VERIFIED DS-08 |
| TVS leakage | +5V_P | — | 0.8 mA (value at 6.0 V VWM, so conservative at ≤ 5.25 V) | VERIFIED DS-05 |
| LED1 red | +5V_P | about 2 mA | 2.46 mA | CALCULATED |
| I2C devices | +3V3_P | — | 100 mA | DESIGN rating |
| GP sensor | +3V3_P | — | 50 mA | DESIGN rating |
| UART device | +3V3_P (or +5V_P via JP1) | — | 100 mA | DESIGN rating |
| LED2 green | +3V3_P | about 1.6 mA | 2.35 mA | CALCULATED |
| TLV1117LV IQ | +5V_P | 50 µA | 100 µA | VERIFIED DS-06 |
| U2 + U4 + U3(A) + pull-ups + RX pull-up | 3V3_ESP (DevKit) | µA | 3.37 mA | VERIFIED ICC + CALCULATED |

## Totals
| Quantity | Value |
|---|---|
| `+3V3_P` worst | **252.4 mA** |
| `+5V_P` direct worst | 23.3 mA |
| **Input current worst** | **275.7 mA** (unchanged if the UART is moved to 5 V) |
| Draw from the DevKit 3V3 pin | ≤ 3.4 mA (reference loads only) |
| Margin policy | Polyfuse hold at max ambient ≥ 1.2 × worst: actual ×1.45 at 50 °C |

## Per rail: voltage, current, dissipation, thermal
| Rail / element | Vmin | Vnom | Vmax | Imax | Dissipation | Thermal margin |
|---|---|---|---|---|---|---|
| `+5V_P` | 4.439 V | 4.818 V | 5.250 V | 276 mA | — | — |
| `+3V3_P` | 3.215 V | 3.300 V | 3.349 V | 252 mA | — | — |
| U1 TLV1117LV33 | — | — | — | 252 mA | **0.505 W** | Tj 81.8 °C at 50 °C ambient, 43 °C below the 125 °C limit (RθJA 62.9) |
| F1 MF-MSMF050 | — | — | — | 276 mA | ≤ 76 mW (R1max) | hold ×1.45 at 50 °C |
| Q1 AO3401A | — | — | — | 276 mA | 9.7 mW | +1.2 °C |
| R10 220 Ω (TX short) | — | — | — | 16 mA | 59 mW | 0.1 W rating |
| LED resistors | — | — | — | 2.5 mA | ≤ 9.1 mW | — |

## Assumptions that remain (to be confirmed by measurement)
- MLCC DC-bias retention ≥ 40 % (no Samsung curve). Only affects the stability margin (×8 shown).
- AO3401A RDS(on) +50 % hot (conservative).
- Ambient ≤ 50 °C (DESIGN).
- The DevKit 3V3 pin can source 3.4 mA. Plausible, because the ESP32 module itself needs ≥ 0.5 A from that regulator, but the clone's regulator is unverified.
