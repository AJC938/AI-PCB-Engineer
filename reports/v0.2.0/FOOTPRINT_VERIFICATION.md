# Footprint Verification — V0.2.0 (Gate C)

Method: pad geometry was extracted from every footprint used (`build/fp_report.py`) and compared with the
manufacturer land pattern or mechanical data. Pin numbering and symbol↔footprint mapping are checked by
`verify_schematic.py` ([3] 54 footprints, every symbol pin has a pad). Placement orientation and polarity were
checked in the 3D review and on the assembly drawing.

| Ref(s) | Footprint | Mfr data | Pads / drill (footprint) | Datasheet value | Verdict |
|---|---|---|---|---|---|
| U5 | **project** `TI_PWP0016A_HTSSOP-16-1EP…` | TI SLVSDG2G p.52-54 (PWP0016A) | 16 × 1.5×0.45, pitch 0.65, span 5.8; EP 3.4×5.0; mask 3.3×3.3; paste 3.3×3.3 | identical | **PASS**. Replaces the KiCad footprint, which follows the older PWP0016H (mask 2.66×2.46, pads 1.575×0.4) |
| U1 | `SOT-223-3_TabPin2` | TI DCY0004A p.23 | 3 × 2.0×1.5 + tab 2.0×3.8, pitch 2.3, span 6.3 | 3 × 2.15×0.95 + tab 3.25×2.15, span 5.8 | **PASS (IPC-7351 alternative, TI note 4 allows)**. Pin map 1 GND / 2 OUT+tab / 3 IN verified (V0.1.0) |
| U2, U4 | `SOT-23-5` | TI DBV0005A p.24 | 1.325×0.6, pitch 0.95, span 2.275 | 1.1×0.6, span 2.6 | **PASS (IPC-7351 alternative, TI note 6)** |
| U3 | `SOT-23-6` | TI DBV0006A p.32 | 1.325×0.6, span 2.275 | 1.1×0.6, span 2.6 | **PASS (IPC-7351 alternative)** |
| R*, C* | `R_0603_1608Metric` 0.8×0.95 / `C_0603_1608Metric` 0.9×0.95, span 1.65/1.55 | Panasonic ERJ-3 (land pattern in a separate document, not obtained); Samsung/Murata 0603 1.6×0.8 body | IPC-7351 nominal | body 1.6×0.8 verified | **PASS (IPC-7351; vendor land pattern not compared)** |
| J1 | `TerminalBlock_Phoenix_MKDS-1,5-2-5.08…Horizontal` | Phoenix 1715721 (DS-14) | 2 × Ø2.6 pad / Ø1.3 drill, pitch 5.08 | pitch 5.08, hole Ø1.3 | **PASS**. Wire entry faces the board edge (3D left view) |
| J2 | `PinHeader_1x12_P2.54mm_Vertical` | Samtec TSW/HTSW catalog p.2 | Ø1.7 pad / Ø1.0 drill | recommended hole 1.02 ± 0.03 mm | **PASS (note)**. 1.0 mm finished hole with fab tolerance ±0.08 fits a 0.64 mm square post (diagonal 0.9 mm) |
| J3–J6 | `PinHeader_1x04_P2.54mm_Vertical` | same | same | same | **PASS (note)** |
| LED1, LED2 | `LED_D5.0mm` | Kingbright WP7113ID/SGD (DS-11/12) | Ø1.8 pad / Ø0.9 drill, pitch 2.54, pad 1 = cathode (square) | pitch 2.54, lead 0.5 mm square | **PASS**. Cathode marked on silk (flat) and pad shape |
| TP1–TP8 | `TestPoint_Keystone_5015_Micro_Mini` | Keystone M65p55 | 3.4 × 1.8 | pad layout .135 × .070 in = 3.4 × 1.8 mm | **PASS** |
| JP1, JP2 | `SolderJumper-3/2_P1.3mm_Bridged…` | PCB feature | 1.0×1.5 rounded pads, copper bridge | — | **PASS** (bridged in copper: JP1 1-2, JP2 closed) |
| H1–H4 | `MountingHole_3.2mm_M3` | ISO M3 clearance | NPTH Ø3.2 | — | **PASS** |
| FID1–3 | `Fiducial_1mm_Mask2mm` | — | Ø1.0 copper, Ø2.0 mask | — | **PASS** |

## Footprint attributes and 3D models
- Type attributes: all SMD parts are `smd`, connectors/LEDs are `through_hole`. Jumpers, holes and fiducials are
  excluded from the BOM (CPL includes fiducials only).
- Every footprint has a KiCad 3D model; the STEP export used the substituted models. LED2's model is the generic
  red 5 mm LED (colour only), with no mechanical impact.
- Courtyard checks: KiCad DRC with courtyard rules shows 0 violations.

**No unverified footprint is treated as production-ready.** The IPC-7351 alternatives are explicitly allowed by
the TI notes. The passive land patterns are IPC-7351 nominal and were not compared against the Panasonic document
(listed in OPEN_QUESTIONS as low risk).
