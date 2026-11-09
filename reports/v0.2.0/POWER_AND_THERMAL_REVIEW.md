# Power and Thermal Review — V0.2.0 (Gate A §5.2, §11)

Status: **PASS (CALCULATED from TI data + drawn copper measured in the layout). NOT a physical measurement.**

## 1. Power budget (Architecture B, unchanged loads)
| Rail | Source | Worst load | Range | Evidence |
|---|---|---|---|---|
| VIN_RAW | external regulated 5 V ±5 % | 275.4 mA | 4.75 – 5.25 V | design_calcs_v020 §1 |
| +5V_P | U5 OUT (RON ≤ 250 mΩ) | 275.4 mA through U5 | 4.681 – 5.250 V | §3 |
| +3V3_P | U1 TLV1117LV33 | 252.4 mA (I2C 100 + GP 50 + UART 100 DESIGN ratings + LED2) | 3.250 – 3.349 V | V0.1.0 |
| 3V3_ESP | DevKit 3V3 pin (reference only) | ≤ 3.4 mA | DevKit | V0.1.0 |

## 2. LDO junction temperature (re-derived, not reused)
- P_LDO = (5.25 − 3.250) × 0.2524 A + 5.25 V × 100 µA = **0.505 W** (worst: VIN max, VOUT min, full DESIGN load).
- The V0.1.0 value of 81.8 °C used **RθJA 62.9 °C/W, a JEDEC 4-layer (2s2p) figure** (DS-06 p.4). It does not
  apply to this 2-layer board and is withdrawn.
- 2-layer source: TI LM1117 datasheet SNOS412Q, Table 9-2 (DS-20). This is the same TI SOT-223 (DCY) package on 1 oz
  copper. Values: 136 °C/W (minimum pad), 84 °C/W (0.30 in² top), 75 °C/W (0.53 in² top). A +10 % uncertainty
  factor is applied (ASSUMED) because the TLV1117LV die and lead-frame differ.

| Case | Copper on tab | RθJA used | Tj at 50 °C ambient | Result |
|---|---|---|---|---|
| Minimum pad | 0.012 in² | 136 × 1.1 | 125.6 °C | FAIL (why copper is mandatory) |
| Design requirement | ≥ 0.30 in² (194 mm²) top | 84 × 1.1 | 96.7 °C | PASS |
| **As drawn** | **251.2 mm² (0.389 in²) top, solid connection** | ≈ 80.5 × 1.1 (interpolated) | **≈ 94.7 °C** | **PASS (target ≤ 110 °C, max 125 °C)** |
| As drawn, 70 °C ambient (beyond spec) | same | same | ≈ 114.7 °C | below 125 °C; outside design ambient |

The copper area comes from pcbnew `ZONE::GetFilledArea()` after refill (evidence: DRC_VALIDATION.md). The tab
connects to the zone with a **solid** connection, not thermal-relief spokes (`build/set_zone_connection.py`).
Thermal vias were **not** added: the bottom layer is the continuous GND plane, so a bottom +3V3_P area would split
the return plane. The top-only rows of Table 9-2 already meet the target. Thermal verification: V0.3.0 (IR or
thermocouple on the tab at full DESIGN load).

## 3. eFuse thermal
19 mW steady (I² × RON max). During an output short in current-limit mode, 3.6 W flows until TI's internal thermal
shutdown (157 °C) with 512 ms auto-retry. This is protective behaviour, and no extra copper is needed. The PowerPAD
sits on the RTN island (38 mm², separate from GND per TI).

## 4. Trace widths (IPC-2221 external, 1 oz, ΔT 10 °C)
| Net class | Max current | Minimum | Used | Note |
|---|---|---|---|---|
| VIN_RAW / +5V_P | 0.69 A (I_OL max) | 0.18 mm | **0.50 mm** | necks to 0.40–0.45 mm only at U5 fine-pitch pins |
| +3V3_P | 0.38 A | 0.08 mm | **0.50 mm** + 251 mm² zone | — |
| GND stubs to plane | — | — | 0.40 mm | bottom plane 5342 mm², top pour 3419 mm² |
| EF_RTN, 3V3_ESP | < 5 mA | — | 0.30 mm | — |
| Signals | < 25 mA | — | 0.25 mm | — |
Voltage drop on 60 mm of 0.5 mm track at 0.28 A ≈ 17 mV (negligible).

## 5. Decoupling placement (pad-centre distances measured on the board with pcbnew)
| Capacitor | Pin | Distance | Assessment |
|---|---|---|---|
| C12 1 µF | U5 IN (1) | 3.3 mm | good (TI §12.1: close to IN/GND) |
| C13 47 nF / R19 20 k | U5 dVdT / ILIM | 4.6 / 2.6 mm | good (TI: short ILIM trace) |
| C1 / C2 | U5 OUT (16) | 7.7 / 9.7 mm | acceptable (bulk on the 5 V rail) |
| C5 100 nF | U1 IN (3) | 3.4 mm | good |
| C3 10 µF / C4 100 nF | U1 OUT (2) | 7.6 / 8.8 mm, joined through the 251 mm² +3V3_P zone | **WARNING (accepted)**: farther than ideal. TLV1117LV is stable with 0 Ω ESR ceramics (DS-06 p.1), and the zone path has very low inductance. Check the transient response in V0.3.0 |
| C6 / C7 100 nF | U3 VCCA / VCCB | 3.4 / 3.2 mm | good |
| C10 / C11 100 nF | U2 / U4 VCC | 5.6 / 5.6 mm | acceptable (logic at kHz rates) |
| C8 10 µF / C9 100 nF | J3 pin 1 | 5.0 / 7.0 mm | good (sensor burst current) |
