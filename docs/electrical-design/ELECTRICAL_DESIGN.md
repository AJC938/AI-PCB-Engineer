# Electrical Design — Rev A

Summary of the circuit and the reasons behind each choice. Every value links to its source. Full calculations:
[`calculations/`](../../calculations/). Datasheet index: [`datasheets/`](../../datasheets/).

## 1. Input protection — U5 TPS26600PWPR eFuse (TI SLVSDG2G Rev. G)
| Function | Implementation | Value | Source |
|---|---|---|---|
| Overvoltage cut-off | R16 73.2 kΩ / R17 5.90 kΩ / R18 21.5 kΩ (1 %) from IN to RTN | OVP trip 5.39–5.82 V rising (worst case) | `calculations/v0.2.0/design_calcs_v020_output.txt` §2; Monte Carlo `independent_checks_v020_output.txt` |
| Undervoltage lockout | same divider | 4.25–4.56 V rising | same |
| Reverse polarity | integrated back-to-back FETs, GND/RTN separation | blocks to −60 V (board limited to −50 V by C12) | DS p.19; limitation for earthed setups: [SAFETY_AND_POWER.md](../safety/SAFETY_AND_POWER.md) |
| Current limit | R19 20 kΩ ILIM → RTN; MODE → RTN | 0.51–0.69 A, current limit with auto-retry | DS Table 2; calcs §4 |
| Soft start | C13 47 nF dVdT → RTN | 1.97 ms ramp, ≈ 89 mA inrush | calcs §4 |
| Input capacitor | C12 1 µF 50 V X5R | ≥ 1 µF per TI §11.1 | DS p.38 |
| Unused pins | SHDN, IMON, FLT, NC left open | per the TI pin table | DS p.4–5 |

Why an eFuse: V0.1.0 used a fuse, a P-MOSFET and an SMAJ6.0A TVS. The TVS breakdown (≥ 6.67 V) is above the
LDO's 6.0 V absolute maximum, so it could not protect it (DDR-17,
[`reports/v0.2.0/TVS_LDO_PROTECTION_ANALYSIS.md`](../../reports/v0.2.0/TVS_LDO_PROTECTION_ANALYSIS.md)).

## 2. 3.3 V peripheral rail — U1 TLV1117LV33DCYR (TI SBVS160C)
- Input +5V_P (4.68–5.25 V), output +3V3_P, C1/C3 10 µF + 100 nF decoupling.
- Dissipation 0.505 W at the 252 mA design load. **251 mm² solid top copper** on the tab gives an estimated
  Tj ≈ 94.7 °C at 50 °C ambient (CALCULATED from TI's 2-layer SOT-223 copper-area data, +10 % margin).
- **Rating: ≤ 250 mA continuous on +3V3_P at ≤ 50 °C** ([`calculations/v0.3.0/`](../../calculations/v0.3.0/)).

## 3. Ultrasonic interface
| Path | Parts | Key numbers |
|---|---|---|
| TRIG (ESP32 → sensor) | U3 SN74LVC1T45 (3.3 → 5 V), R15 1 kΩ, R4/R5 100 kΩ pull-downs | TRIG high ≥ 4.54 V (≥ 96.9 % of sensor VCC); mis-wiring current ≤ 5.2 mA |
| ECHO (sensor → ESP32) | R6 1 kΩ, R7 100 kΩ, U2 SN74LVC1G17 on 3V3_ESP | input ≤ 5.25 V < 5.5 V tolerance; VT+ max 2.25 V |

## 4. I²C, UART, GPIO
- I²C: 2.2 kΩ ±1 % pull-ups to 3V3_ESP (JP2, cuttable). Passes UM10204 Rp(min) at 3.6 V; Fast-mode bus budget ≈ 149 pF for cable and devices.
- UART: TX via 220 Ω; RX via U4 buffer (accepts 3.3 V or 5 V) with 100 kΩ pull-up; device supply 3.3 V or 5 V (JP1).
- GPIO32/33 via 1 kΩ series resistors to J6 (3.3 V only).

## 5. Design decision record (traceability)
| ID | Decision | Source |
|---|---|---|
| Arch. B | ESP32 on its own USB; board powers peripherals; 3V3_ESP used as logic reference | `docs/requirements/v0.1.0/`, user decision V0.1.0 |
| DDR-17 | TPS26600 eFuse replaces fuse/P-FET/TVS | TVS_LDO_PROTECTION_ANALYSIS.md |
| DDR-18 | R15 1 kΩ TRIG series resistor | design_calcs_v020 §9 |
| DDR-19 | Mounting holes and fiducials in the schematic (parity) | reports/v0.2.0/DRC_VALIDATION.md |
| DDR-20 | Project footprint for TI PWP0016A | reports/v0.2.0/FOOTPRINT_VERIFICATION.md |
| DDR-21 | ≥ 194 mm² +3V3_P copper for U1 | reports/v0.2.0/POWER_AND_THERMAL_REVIEW.md |
| DDR-22 | Revision label Rev A / v1.0.0 (non-electrical) | reports/v0.3.0/FINAL_ENGINEERING_AUDIT.md §8 |
| R-31 | Power the board before or together with the ESP32 | reports/v0.2.0/ELECTRICAL_DESIGN_REVIEW.md |
