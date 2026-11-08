# Datasheet Verification — V0.1.0

Index of documents: [`datasheets/v0.1.0/DATASHEET_INDEX.md`](../../datasheets/v0.1.0/DATASHEET_INDEX.md).
Legend: ✔ verified from the official document · ◐ verified with a stated limitation · ✖ not available.

| Part | Electrical limits | Operating conditions | Package / dimensions | Pinout ↔ symbol ↔ footprint | Thermal | Temperature range |
|---|---|---|---|---|---|---|
| AO3401A | ✔ VDS −30, VGS ±12, RDS(on) | ✔ | ✔ SOT-23 | ✔ 1 G / 2 S / 3 D = `Transistor_FET:AO3401A` = SOT-23 pads 1/2/3 (drawing p.1) | ✔ RθJA 125 max | ✔ −55…150 °C |
| MF-MSMF050-2 | ✔ Vmax, Ihold, Itrip, R | ✔ derating table | ✔ 1812 | ✔ 2-terminal non-polar | ✔ Pd 0.8 W | ✔ −40…85 °C derating |
| SMAJ6.0A-E3/61 | ✔ VWM, VBR, VC, IPP | ✔ | ✔ SMA | ◐ unidirectional K/A = `D_Zener` 1 K / 2 A. Footprint pad 1 = cathode by KiCad convention, band orientation to confirm against Vishay drawing in V0.2.0 | ✔ PD | ✔ −55…150 °C |
| TLV1117LV33DCYR | ✔ VIN abs 6 V, ROC 5.5 V | ✔ | ✔ SOT-223 (DCY) | ✔ 1 GND / 2 OUT+tab / 3 IN = AMS1117-3.3 symbol (1 GND, 2 VO, 3 VI) = SOT-223-3_TabPin2 (tab = pin 2) | ✔ RθJA 62.9 | ✔ TJ −40…125 °C |
| SN74LVC1G17DBVR | ✔ VI 5.5 V indep. of VCC, Ioff | ✔ | ✔ SOT-23-5 | ✔ 1 NC / 2 A / 3 GND / 4 Y / 5 VCC = `74xGxx:74LVC1G17` (NC pin flagged no-connect) | ✔ RθJA 357 (negligible power) | ✔ −40…125 °C |
| SN74LVC1T45DBVR | ✔ VIH, VOH, Ioff, VCC isolation | ✔ | ✔ SOT-23-6 | ✔ 1 VCCA / 2 GND / 3 A / 4 B / 5 DIR / 6 VCCB = `SN74LVC1T45DBV` | ✔ | ✔ −40…85 °C |
| ERJ-3EKF (all values) | ✔ 0.1 W, ±1 % | ✔ | ✔ 0603 | ✔ 2-terminal | — | ✔ −55…155 °C |
| CL10A106KP8NNNC | ◐ 10 V X5R. **No DC-bias curve** | ◐ | ✔ 1.6 × 0.8 × 0.8 mm | ✔ | — | ◐ X5R class (−55…85 °C by EIA definition, not stated on page) |
| GRM188R71C104KA01D | ✔ 16 V X7R | ✔ | ✔ 0603 | ✔ | — | ✔ −55…125 °C |
| WP7113ID / WP7113SGD | ✔ VF, IF | ✔ | ✔ T-1¾ (ID drawing verified in V0.0.2. SGD drawing to compare) | ✔ pad 1 = K (flat side) | ✔ | ✔ |
| 1715721 | ✔ 17.5 A, 400 V | ✔ | ✔ pitch 5.08, hole 1.3 | ✔ | — | ✔ −40…105 °C |
| HTSW-1xx-07-T-S | ◐ current rating not extracted (signal-level use, ≤ 0.1 A) | ✔ −55…105 °C (tin) | ✔ .100" pitch, lead style −07 | ✔ pins 1…n = PinHeader pads 1…n | — | ✔ |
| Keystone 5015 | ✔ material | — | ✔ pad layout drawing | ✔ 1 pad | — | — |
| Adafruit 4007 (off-board) | ◐ VENDOR: 3–5.5 V, 2.2 mA, logic = supply | ◐ | ✔ 40 × 18 mm, 4-pin header | ✖ **pin names not published**, so verify on the physical module | — | ◐ −10…90 °C (probe) |
| ESP32 / DevKit | ✔ (REF-01/02/03) | ✔ | ✖ clone drawing unavailable | ✔ GPIO numbers. Header positions wired by label | — | — |

## Verification method
Each PDF was downloaded straight from the manufacturer URL into an isolated scratch folder and parsed
locally with pymupdf (KiCad's Python). Pinout drawings that are graphics (AO3401A, Adafruit diagram) were
rendered and inspected visually. Values were then copied into `design_calcs.py` with their source tag.
Access controls were never bypassed: Würth (403), KEMET (expired certificate) and TDK (403) were skipped.
