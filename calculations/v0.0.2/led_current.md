# V0.0.2 LED Indicator — Circuit Calculations

Script: [`led_current.py`](led_current.py) · Output: [`led_current_output.txt`](led_current_output.txt)

## Topology
`J1.1 (+5V) → R1 (620 Ω) → D1 anode → D1 cathode → J1.2 (GND)`

## Inputs and evidence
| Input | Value | Evidence |
|---|---|---|
| Supply | 5.00 V | User requirement |
| Supply tolerance | ±5 % | **ASSUMED**: no supply has been specified |
| R1 | 620 Ω, ±1 %, 0.25 W @70 °C, 250 V max | **VERIFIED**: Yageo MFR datasheet (Aug 17 2021 V.0) p.2 ordering code, p.3 electrical table |
| D1 VF @ 10 mA | 1.9 V typ / 2.3 V max (±0.1 V) | **VERIFIED**: Kingbright WP7113ID V.14A p.2 |
| D1 VF @ ~5 mA | ≈1.80 V typ | **GRAPH-READ**: Kingbright p.3 IF–VF curve (~1.78 V at 4 mA, ~1.9 V at 8 mA) |
| D1 VF lower bound | 1.70 V | **ASSUMED**: graph typ − 0.1 V. The datasheet gives no VF min |
| D1 limits | IF 30 mA, PD 75 mW, VR 5 V, TC(VF) −1.9 mV/°C | **VERIFIED**: Kingbright p.2 |
| J1 rating | 17.5 A, 400 V (III/2) | **VERIFIED**: Phoenix 1715721 product page |

The 2 V forward voltage in the brief was a preliminary assumption. It is replaced by the
datasheet values above.

## Results (CALCULATED)
| Case | I (mA) | P_R1 (mW) | P_D1 (mW) |
|---|---|---|---|
| Nominal (5.00 V, VF 1.80 V, 620 Ω) | **5.16** | 16.5 | 9.3 |
| Nominal with table VF 1.90 V | 5.00 | 15.5 | 9.5 |
| Max (5.25 V, VF 1.70 V, 613.8 Ω) | 5.78 | 20.5 | 9.8 |
| Min (4.75 V, VF 2.30 V, 626.2 Ω) | 3.91 | 9.6 | 9.0 |

- Target of about 5 mA is met. Worst-case spread is 3.9–5.8 mA, dominated by supply tolerance and VF spread.
- VF sensitivity: −1.61 mA/V, so the ±0.1 V VF tolerance gives ±0.16 mA.
- Resistor tolerance ±1 % gives about ∓0.05 mA (∓1 %).
- VF temperature drift over 0–50 °C: ±47.5 mV, giving about ∓0.08 mA.

## Margins
| Check | Worst case | Limit | Result |
|---|---|---|---|
| R1 power | 20.5 mW | 250 mW (to 70 °C ambient, derated to 0 at 155 °C) | PASS (8 %) |
| R1 voltage | 3.55 V | 250 V | PASS |
| D1 current | 5.78 mA | 30 mA | PASS (19 %) |
| D1 dissipation | 9.8 mW | 75 mW | PASS |
| J1 current | 5.8 mA | 17.5 A | PASS |
| **Reverse polarity** | ≈5.25 V reverse across D1 | VR 5 V | **WARNING**: exceeds the rating if the supply is reversed. The test circuit has no reverse protection. Mark polarity on the silkscreen. A series diode is a future-revision option |

## PCB implications
- Current is under 6 mA, so track width is not current-limited. 0.5 mm tracks are used for robustness and manufacturability. This is a design choice, not an IPC-2152 requirement.
- All parts are THT. The board is two-layer, 1.6 mm thick (KiCad default stack-up).
