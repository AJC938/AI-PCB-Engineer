# Datasheet Index — V0.2.0 additions

Continues [`datasheets/v0.1.0/DATASHEET_INDEX.md`](../v0.1.0/DATASHEET_INDEX.md) (DS-01…DS-16). DS-03 (AO3401A),
DS-04 (MF-MSMF050) and DS-05 (SMAJ6.0A) remain as V0.1.0 history; those parts are **removed** in V0.2.0.
PDFs were downloaded to a scratch folder and parsed locally; they are not redistributed. Checked 2026-11-09.

| ID | Part | Mfr | Document / revision | URL | Facts used (page) |
|---|---|---|---|---|---|
| DS-17 | TPS26600PWPR | Texas Instruments | SLVSDG2G, Dec 2019; package addendum 10-Nov-2025 | https://www.ti.com/lit/ds/symlink/tps2660.pdf | p.4-5 pinout (HTSSOP 1/2 IN, 3 UVLO, 5 OVP, 6 MODE, 7 SHDN, 8 RTN, 9 GND, 10 IMON, 11 ILIM, 12 dVdT, 14 FLT, 15/16 OUT, PowerPAD = RTN). p.6 abs max IN −60…62 V, OVP/dVdT/ILIM ≤ 5 V; ROC dVdT ≥ 10 nF; RθJA 38.6 °C/W. p.7 UVLOR 1.175/1.19/1.225, OVPR 1.17/1.19/1.225, OVPF 1.085–1.125, POR 3.9–4.1 V, op 4.2–60 V, dVdT 4.7 µA × 24.6. p.7-8 I_OL table, RON 150 typ / 250 max. p.9 OVP disable 6 µs. p.19-21 OVP/UVLO divider, reverse polarity, dVdT Eq.1/2. p.26 RTN ≠ GND. p.29 Eq.9-11. p.38 transient protection. p.39-40 layout. p.43 TPS26600PWPR Active, MSL2-260C. p.52-54 PWP0016A outline, land pattern, stencil |
| DS-18 | CL10A105KB8NNNC | Samsung Electro-Mechanics | online spec (weblib) | https://weblib.samsungsem.com/mlcc/mlcc-ec-data-sheet.do?partNumber=CL10A105KB8NNN | 1.0 µF ±10 %, 50 Vdc, X5R, 0603, 1.6 × 0.8 × 0.8 mm |
| DS-19 | CL10B473KB8NNNC | Samsung Electro-Mechanics | online spec (weblib) | https://weblib.samsungsem.com/mlcc/mlcc-ec-data-sheet.do?partNumber=CL10B473KB8NNN | 47 nF ±10 %, 50 Vdc, X7R, 0603 |
| DS-20 | LM1117 (thermal data only) | Texas Instruments | SNOS412Q, Jan 2023 | https://www.ti.com/lit/ds/symlink/lm1117.pdf | p.18-19 Table 9-2: SOT-223 RθJA vs 1 oz copper area (136/123/84/75/69/66 top; 115/98/89/82/79 bottom; 125/93/83/75/70 both). Applied to TLV1117LV (same TI DCY package) with a +10 % uncertainty |
| DS-06 (add.) | TLV1117LV33DCYR | Texas Instruments | SBVS160C | (V0.1.0) | p.23 DCY0004A land pattern (3 × 2.15 × 0.95, tab 3.25 × 2.15, pitch 2.3). Addendum 14-Jun-2026: Active Production |
| DS-07/08 (add.) | SN74LVC1G17DBVR / SN74LVC1T45DBVR | Texas Instruments | (V0.1.0) | (V0.1.0) | DBV land pattern 1.1 × 0.6, span 2.6 (p.24 / p.32). Addenda: Active Production (DBVR and DBVT) |
| DS-15 (add.) | Samtec HTSW | Samtec | TSW/HTSW catalog | (V0.1.0) | recommended PCB hole 1.02 ± 0.03 mm; .025" square post; current per pin 4.3–6.3 A (by mate) |
| DS-16 (add.) | Keystone 5015 | Keystone | M65p55 | (V0.1.0) | pad layout .135 × .070 in (3.4 × 1.8 mm) |
| WEB-1 | Adafruit 4007 wiring | Adafruit | learn.adafruit.com/ultrasonic-sonar-distance-sensors/python-circuitpython | — | signal names VCC / trig / echo / GND (functional); physical pin order not given |
