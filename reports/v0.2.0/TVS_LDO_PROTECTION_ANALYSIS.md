# TVS / LDO Protection Analysis — V0.2.0 (Gate A §5.1)

**Decision (DDR-17): the V0.1.0 input chain F1 (MF-MSMF050) → Q1 (AO3401A) → D1 (SMAJ6.0A) is replaced by a
TI TPS26600 eFuse with an external OVP cut-off, integrated reverse-polarity blocking, current limit and inrush
control. The TVS is removed.** Status: **RESOLVED (CALCULATED + independent check). NOT TESTED physically.**

## 1. Why the V0.1.0 combination was not valid protection
| Parameter | Value | Source |
|---|---|---|
| SMAJ6.0A stand-off VWM | 6.0 V | DS-05 Vishay 88390 p.2 |
| SMAJ6.0A breakdown VBR | **6.67 V min** – 7.37 V max @ 10 mA | DS-05 p.2 |
| SMAJ6.0A clamping VC | **10.3 V @ IPP 38.8 A**, 10/1000 µs waveform | DS-05 p.1-2 |
| SMAJ6.0A leakage at VWM | ≤ 800 µA | DS-05 p.2 |
| TLV1117LV VIN recommended | 2.0 – **5.5 V** | DS-06 TI SBVS160C p.4 §6.3 |
| TLV1117LV VIN absolute max | **6.0 V** | DS-06 p.4 §6.1 |
| SN74LVC1T45 VCCB abs max / ROC | 6.5 V / 5.5 V | DS-08 |
| Ultrasonic module supply | 3–5.5 V (vendor; no abs max published) | DS-13 |

The TVS does not even begin to conduct (VBR min 6.67 V) before the LDO's absolute maximum (6.0 V) is exceeded.
It therefore protects the LDO against **no** overvoltage event, and at its rated clamp (10.3 V) every 5 V-rail
load is beyond its absolute maximum. The claim "TVS protects the board" was unsupported and is withdrawn.

## 2. Options evaluated
| Option | Result | Reason |
|---|---|---|
| A. Other TVS (e.g. SMAJ5.0A, VWM 5.0 V) | Rejected | VWM < VIN max 5.25 V (leakage/conduction in normal operation) and VBR min (≈ 6.4 V) is still > 6.0 V. No TVS with VWM ≥ 5.25 V has VBR < 6.0 V. |
| B. Series impedance + clamp (PTC/TVS or Zener crowbar) | Rejected | Clamp voltage plus tolerance and dynamic resistance reaches ≈ 6 V. There is no margin to the 6.0 V abs max, and the PTC trip time (seconds) is too slow for the regulator. |
| C. Regulator with higher VIN rating only | Insufficient alone | Protects U1 only. LVC1T45 (6.5 V abs), the sensor (5.5 V) and the LVC1G17 echo input (6.5 V abs) remain exposed on +5V_P. |
| **D. OVP cut-off eFuse TPS26600 (selected)** | **Accepted** | Disconnects the whole +5V_P rail above 5.39–5.82 V. Also covers reverse polarity (−60 V), current limit, inrush and reverse current. IN abs max 62 V. |
| E. Remove TVS, no replacement | Rejected | Leaves the wrong-adapter case (9/12 V) destructive. |

## 3. Selected circuit (schematic V0.2.0)
J1 → VIN_RAW → U5 TPS26600PWPR (IN 1/2 → OUT 15/16 = +5V_P). Support parts (TI SLVSDG2G):
- C12 1 µF 50 V (IN–GND, §12.1).
- Divider R16 73.2 k / R17 5.90 k / R18 21.5 k (UVLO and OVP, Eq.10/11).
- R19 20.0 k (ILIM, Eq.9).
- C13 47 nF (dVdT, Eq.1/2).
- MODE tied to RTN (current limit, auto-retry, p.8).
- SHDN, IMON and FLT left open (pin table p.4–5, Fig. 69).
- RTN is a separate copper island; GND pin 9 goes to GND (§9.3.5.5, §10.4).

## 4. Results (`calculations/v0.2.0/design_calcs_v020.py`, worst-case corners)
| Quantity | Result | Limit | Margin | Status |
|---|---|---|---|---|
| OVP rising trip | 5.389 – 5.823 V | > 5.25 V (no nuisance trip) | +0.139 V | PASS |
| OVP rising trip | ≤ 5.823 V | < 6.0 V LDO abs max | +0.177 V | PASS |
| OVP rising trip | ≤ 5.823 V | < 6.5 V LVC abs max | +0.677 V | PASS |
| UVLO rising | 4.252 – 4.564 V | 4.2 V device min … 4.75 V supply min | +0.052 / +0.186 V | PASS |
| +5V_P in operation | 4.681 – 5.250 V | sensor 3–5.5 V, LDO ≤ 5.5 V | — | PASS |
| Current limit | 0.51 – 0.69 A (±15 % ASSUMED) | ≥ 1.5 × load 0.275 A | ×1.85 | PASS |
| Inrush (C_out 33.6 µF, ramp 1.97 ms) | 89 mA | + load < I_OL min | 0.365 < 0.51 A | PASS |
| eFuse steady dissipation | 19 mW (RON 250 mΩ max) | — | — | PASS |
| Hot-short spike at IN | 6.71 V | 62 V abs max | — | PASS |
| Hot-plug ringing (2 × VIN) | ≤ 10.5 V at IN; FET off during plug-in | 62 V | — | PASS |
| ESD 8 kV/150 pF into C12 | +1.2 V (ASSUMED model) | — | — | PASS |
| Reverse polarity | blocked to −60 V; board limited by C12 50 V rating | — | — | PASS (DESIGN) |
Independent Monte Carlo (`independent_checks_v020.py`, 100 000 samples, different method: bisection on the pin
voltage) gives OVP 5.395–5.817 V and UVLO 4.257–4.556 V, with 0 violations.

## 5. Documented limitations (no unsupported claims)
1. **Overvoltage arriving while the board is ON.** The output follows the input for up to the 6 µs OVP delay
   (SLVSDG2G p.9). Absolute maxima are respected only for input slew ≤ 23.8 V/ms. Bench supplies and adapters
   ramp in milliseconds, but a fast step while powered is NOT covered.
2. **5.5 – 5.82 V input band.** Between the recommended maxima (5.5 V) and the OVP trip the board stays below every
   absolute maximum but outside recommended operation. This happens only with an out-of-spec supply.
3. **No surge (IEC 61000-4-5) rating claimed.** The input is specified for a regulated SELV 5 V supply with a
   short lead. TI §11.1 recommends a TVS only when transients exceed 62 V, which this case does not reach.
4. **Earthed-supply reverse-polarity loop.** If the supply's negative and the ESP32 host PC are both earth-referenced, a
   reversed J1 can drive current through the shared GND (Architecture B). The eFuse cannot block a GND path
   (R-37). Rule: use a floating (isolated) 5 V adapter or observe polarity.
5. **Sourcing.** TPS26600PWPR showed "Out of stock" on TI's store on 2026-11-09 (R-36). There is no
   drop-in alternate: TPS26601PWPR is not in the addendum, and TPS26602 has a fixed 38 V clamp.
