# Power Budget — V0.1.0 (initial, planning)

Source of all numbers: [`calculations/v0.1.0/phase1_calcs.py`](../../../calculations/v0.1.0/phase1_calcs.py)
and its [output](../../../calculations/v0.1.0/phase1_calcs_output.txt). Tags: **VERIFIED** (official
document) · **SECONDARY** · **ASSUMED** (placeholder) · **CALCULATED**.

## Load allocations
| Load | Rail | Current | Tag | Basis |
|---|---|---|---|---|
| ESP32 DevKit (Arch. A only) | 5 V → DevKit regulator | 500 mA allocation | VERIFIED requirement | REF-02 Table 14: external supply must deliver ≥ 0.5 A. TX peak 379 mA, average 239 mA (Table 16) |
| HC-SR04 (classic) | 5 V | 20 mA allocation | SECONDARY + ASSUMED margin | about 15 mA per third-party sources (REF-06/07) |
| UART device | 5 V or 3.3 V (TBD) | 100 mA | ASSUMED | device unknown (OQ-08). Counted on 5 V (conservative for input) |
| I2C peripherals | 3.3 V | 100 mA | ASSUMED | sensor list unknown (OQ-07) |
| General-purpose sensor | 3.3 V | 50 mA | ASSUMED | Could item (OQ-13) |
| Indicator LEDs | 5 V | 4 mA | ASSUMED | 2 × about 2 mA |

## Totals (CALCULATED; linear 3.3 V regulator, so input current ≈ output current)
| Architecture | 5 V loads | 3.3 V loads | Input current | Rating basis (+25 %, ASSUMED policy) |
|---|---|---|---|---|
| A: board powers DevKit via 5 V pin | 624 mA | 150 mA | **774 mA** | ≥ 968 mA |
| B: DevKit on its own USB | 124 mA | 150 mA | **274 mA** | ≥ 342 mA |

ESP32 transients: in Arch. A the 379 mA TX peaks flow through the input connector, protection and
`+5V_P` copper. The DevKit regulator input needs its decoupling (DevKit design, OQ-02). Board-side
bulk capacitance on `+5V_P` must be sized after the DevKit schematic is reviewed.

## 3.3 V regulator: LDO vs buck (CALCULATED; VIN max 5.25 V)
| I_out | LDO loss | Buck loss (η = 0.85, ASSUMED) |
|---|---|---|
| 50 mA | 0.098 W | 0.029 W |
| 100 mA | 0.195 W | 0.058 W |
| **150 mA (budget)** | **0.293 W** | 0.087 W |
| 200 mA | 0.390 W | 0.116 W |
| 300 mA | 0.585 W | 0.175 W |
| 500 mA | 0.975 W | 0.291 W |
Junction rise = P × RthJA of the chosen package (TBD). **Preliminary direction (not a selection):** at
≤ 150–200 mA a linear regulator is favoured (no switching noise near sensor signals, fewer parts), provided
its package RthJA keeps Tj within rating at the maximum ambient (OQ-15). Above about 300 mA, or at high
ambient, re-evaluate a buck.

## Reverse-polarity element drop (illustrative parameters, NOT parts; Arch. A current)
| Element | Drop at 774 mA | `+5V_P` at minimum input (4.75 V) |
|---|---|---|
| Schottky, Vf 0.3 V | 0.300 V | 4.45 V |
| Schottky, Vf 0.5 V | 0.500 V | 4.25 V |
| P-MOSFET, 50 mΩ | 0.039 V | 4.71 V |
| P-MOSFET, 100 mΩ | 0.077 V | 4.67 V |
A diode drop may break the 5 V-only ultrasonic module's supply range and the DevKit regulator headroom
(both TBD). A P-MOSFET (or ideal-diode controller) is favoured at Arch. A current. At Arch. B current a
Schottky may be acceptable. Decision after OQ-06 and the HC-SR04 supply minimum.

## Grounding and return paths
- A single GND net. Board-to-DevKit GND through all available DevKit GND pins (REF-03 lists three on DevKitC V4).
- In Arch. A the DevKit's return current (up to the 379 mA peaks) shares the input GND path, so it needs a
  low-impedance GND pour and short input loop.
- Sensor returns (HC-SR04 bursts, I2C) should not share narrow traces with the DevKit supply return.

## Back-feed analysis (summary)
| Path | Risk | Mitigation direction |
|---|---|---|
| DevKit USB VBUS ↔ board `+5V_P` (Arch. A) | Two sources on the DevKit 5 V node. Espressif warns of damage (REF-03) | Enforced one-source rule: removable link and labelling, or OR-ing / ideal-diode path. Needs the DevKit schematic (OQ-02) |
| `+3V3_P` ↔ DevKit 3V3 | Two regulators fighting | Never connected (PWR-08) |
| Signal lines into an unpowered ESP32 (Arch. B) | Current through IO protection structures back-powers the chip | Buffers with power-off protection, series resistance, or power-sequencing rule. Limit TBD (OQ-14) |
| I2C pull-ups to `+3V3_P` while the ESP32 is off | Same as above | Pull-ups referenced to the ESP32's own 3.3 V, or a translator (OQ-12) |

## Unresolved values
Input tolerance (OQ-05), connector/protection rating (OQ-04), DevKit regulator type and dropout (OQ-02),
HC-SR04 supply range (OQ-11), I2C/UART/GP loads (OQ-07/08/13), maximum ambient (OQ-15),
regulator RthJA (after selection).
