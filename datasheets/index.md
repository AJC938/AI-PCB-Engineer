# Datasheet Index

PDFs are not committed: they are third-party copyrighted documents, and this repo is meant
to become public. Each entry records the source, the revision and the facts used.

| Ref | Part | Manufacturer / MPN | Document | Source (accessed 2026-11-07) | Facts used |
|---|---|---|---|---|---|
| D1 | 5 mm red diffused LED, T-1 3/4 | Kingbright **WP7113ID** | Spec DSAF0012, Rev V.14A, 01/08/2026, 5 pages | https://www.kingbrightusa.com/images/catalog/SPEC/WP7113ID.pdf | p.1: Ø5.0 body, Ø5.9 flange, lead □0.5 (+0.25/−0.1), pitch 2.54, cathode lead on the flat side and 1.5±1 mm shorter, recommended PCB hole Ø0.9 ×2. p.2: VF 1.9 typ / 2.3 max @10 mA (±0.1 V), IF 30 mA, IFP 160 mA, PD 75 mW, VR 5 V, TC(VF) −1.9 mV/°C. p.3: IF–VF curve, wave solder 260 °C |
| R1 | 620 Ω metal film, 1/4 W, 1 % | Yageo **MFR-25FBF52-620R** | "Metal Film Resistors, MFR Series", Product specification Aug 17 2021 V.0, 16 pages | Manufacturer PDF mirrored by Octopart: https://datasheet.octopart.com/MFR-25FRF52-620R-Yageo-datasheet-155367622.pdf (the yageo.com link returned 404) | p.2: part-number decoding (‑25 = 1/4 W, F = ±1 %, B = bulk, F = ±100 ppm/°C, 52 = 52.4 mm forming). p.3: MFR-25 L 6.3±0.5, ØD 2.4±0.2, H 28±2, Ød 0.55±0.05 mm. 1/4 W @70 °C, 250 V max working, −55…+155 °C, derating |
| J1 | 2-pos PCB screw terminal, 5.08 mm | Phoenix Contact **MKDS 1,5/ 2-5,08**, item **1715721** | Official product page, technical data | https://www.phoenixcontact.com/en-us/products/printed-circuit-board-terminal-mkds-15-2-508-1715721 | 2 positions, pitch 5.08 mm, 17.5 A, 400 V (III/2), pins 0.9×0.9 mm, solder pin 3.5 mm, **hole Ø1.3 mm**, W 10.16 × L 9.8 × H 17.3 mm, −40…+105 °C, wave soldering |

Notes:
- Distributor availability and pricing were **not checked**. No purchase was made.
- Yageo MPN suffix `FBF52` (bulk, ±100 ppm) was decoded from the datasheet ordering table.
  Its stock availability is not verified. `FTF52` (box pack) is an equivalent alternative.
