# Licensing

## What is open
| Material | Licence (SPDX) | Licence file |
|---|---|---|
| Hardware source: KiCad schematic, PCB, project file, project footprint library (`Sensor_Interface_Power_Board.pretty`) | `CERN-OHL-S-2.0` | [LICENSE-HARDWARE](../LICENSE-HARDWARE) |
| Manufacturing outputs: Gerber, drill, IPC-D-356, BOM, CPL, drawings, STEP, ZIP packages | `CERN-OHL-S-2.0` | [LICENSE-HARDWARE](../LICENSE-HARDWARE) |
| Hardware documentation: `docs/`, `reports/`, design notes, renders in `media/` | `CERN-OHL-S-2.0` | [LICENSE-HARDWARE](../LICENSE-HARDWARE) |
| Scripts and code: `scripts/`, `ai/workflows/`, `hardware/kicad/*/build/*.py`, `calculations/**/*.py`, `reports/**/tests/` | `MIT` | [LICENSE-CODE](../LICENSE-CODE) |

The licence texts are the unmodified texts from the SPDX License List data
(`github.com/spdx/license-list-data`, `text/CERN-OHL-S-2.0.txt` and `text/MIT.txt`, retrieved 2026-11-09).
Copyright: "AI-PCB-Engineer contributors" (neutral author metadata; no personal data is published).

## What CERN-OHL-S-2.0 means in practice (summary, not legal advice)
You may use, study, modify, make and sell boards from this design. If you **convey** (distribute) the design, a
modified design or products made from it, you must make the complete source of your version available under
CERN-OHL-S-2.0, keep the notices, and say what you changed. Read the licence text for the binding terms.

## Third-party material
| Item | Licence / status |
|---|---|
| KiCad standard footprints and 3D models used by the board (`${KICAD10_3DMODEL_DIR}` and the standard footprint libraries) | CC-BY-SA 4.0 with the KiCad library exception: designs and generated files that use the library data are not affected (KiCad libraries `LICENSE.md`). The libraries are not redistributed here |
| U5 project footprint | Created for this project from TI's published PWP0016A land-pattern drawing (dimensions are facts from the datasheet); covered by CERN-OHL-S-2.0 |
| Datasheets | **Not redistributed.** Only links and revision identifiers are listed in `datasheets/` |
| Manufacturer and part names | Trademarks of their owners; used only to identify parts |

## Certification
This project is **not** certified by the Open Source Hardware Association (OSHWA), and no such compliance is claimed.

## Licence choice (owner decision)
CERN-OHL-S-2.0 (strongly reciprocal) was prepared as the recommended default. The alternatives with materially
different redistribution terms are CERN-OHL-W-2.0 (weakly reciprocal: obligations apply to the licensed design
itself but not to a larger design that only uses it as an external component) and CERN-OHL-P-2.0 (permissive).
The owner confirms the variant before the `v1.0.0` tag (see `release/v1.0.0/RELEASE_CHECKLIST.md`).
