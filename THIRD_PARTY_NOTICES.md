# Third-Party Notices

Third-party material keeps its own licence. **This project does not relicense it.** Audit date: 2026-11-09.
Licence texts were checked at the sources listed. "Distributed here" means the material, or data derived from
it, is included in this repository or its release packages.

## 1. Material included in the repository or packages
| # | Material | Creator / supplier | Source | Licence | Attribution / conditions | Redistribution | Status |
|---|---|---|---|---|---|---|---|
| T-1 | KiCad library **symbols** copied into `Sensor_Interface_Power_Board.kicad_sch` (and the V0.0.2/V0.0.3 test schematics) | KiCad Library contributors | https://gitlab.com/kicad/libraries/kicad-symbols | `CC-BY-SA-4.0 WITH KiCad-libraries-exception` (`LICENSE.md` of the library, read 2026-11-09) | Article 3 (attribution/ShareAlike) is waived for designs and generated files that use the library data | Permitted | May remain. The design files are CERN-OHL-P-2.0 |
| T-2 | KiCad library **footprints** copied into `Sensor_Interface_Power_Board.kicad_pcb` and the test boards | KiCad Library contributors | https://gitlab.com/kicad/libraries/kicad-footprints | same (identical `LICENSE.md`) | same | Permitted | May remain |
| T-3 | KiCad **3D model** geometry in `RevA/3d/*.step`, `manufacturing/v0.2.0/3d/*.step` and the renders in `media/renders/`, `reports/*/evidence/images/` | KiCad Library contributors | https://gitlab.com/kicad/libraries/kicad-packages3D | same (identical `LICENSE.md`) | Generated files: article 3 waived. The model files themselves are **not** included; the design references `${KICAD10_3DMODEL_DIR}` | Permitted | May remain |
| T-4 | **U5 project footprint** `hardware/kicad/Sensor_Interface_Power_Board/Sensor_Interface_Power_Board.pretty/TI_PWP0016A_HTSSOP-16-1EP_4.4x5mm_P0.65mm_EP3.4x5mm.kicad_mod` | KiCad Library contributors (original `Package_SO:HTSSOP-16-1EP_4.4x5mm_P0.65mm_EP3.4x5mm_Mask2.66x2.46mm`); modified by this project | https://gitlab.com/kicad/libraries/kicad-footprints | `CC-BY-SA-4.0 WITH KiCad-libraries-exception` | This file is library material in its own right. Attribution (this entry); ShareAlike (the file stays under the same licence); changes indicated (`MODIFICATIONS.md`, footprint `descr`); licence text in `LICENSES/CC-BY-SA-4.0.txt` and `LICENSES/KiCad-libraries-exception.txt` | Permitted under CC-BY-SA-4.0 | May remain, **excluded from the CERN-OHL-P grant** |
| T-5 | Licence texts in `LICENSE-HARDWARE`, `LICENSES/CERN-OHL-P-2.0.txt` | CERN | https://ohwr.org/cern_ohl_p_v2.txt (redirects to the OHWR CERN-OHL repository) | Text © CERN 2020, "Anyone is welcome to use it, in unmodified form only" | Unmodified | Permitted (unmodified) | Byte-identical to the official text |
| T-6 | MIT licence text in `LICENSE-CODE`, `LICENSES/MIT.txt` | Open Source Initiative template | https://opensource.org/license/mit/ | — | Only the year/holder line is filled in | Permitted | OK |
| T-7 | CC-BY-SA-4.0 legal code and the KiCad exception text in `LICENSES/` | Creative Commons; SPDX License List | https://creativecommons.org/licenses/by-sa/4.0/legalcode.txt ; https://github.com/spdx/license-list-data (`KiCad-libraries-exception`) | licence texts | Unmodified | Permitted | OK |

## 2. Material NOT included (referenced only)
| # | Material | Owner | How it is used | Status |
|---|---|---|---|---|
| T-10 | Component datasheets (TI TPS2660, TLV1117LV, LM1117, SN74LVC1G17, SN74LVC1T45; Samsung, Murata and Panasonic passives; Phoenix Contact 1715721; Samtec HTSW; Kingbright WP7113; Keystone 5015; Espressif ESP32 / DevKitC; NXP UM10204; Adafruit 4007 guide) | Their publishers | **No datasheet PDF is in the repository or packages** (checked: the only PDFs are KiCad exports of this design). `datasheets/` lists URL, document revision and the short facts used, with page numbers | OK: not redistributed |
| T-11 | TI PWP0016A land-pattern drawing | Texas Instruments | Dimensions (facts) used to modify T-4. The drawing is not reproduced | OK |
| T-12 | Trademarks and product names (ESP32, Texas Instruments, Samtec, Phoenix Contact, KiCad, …) | Their owners | Identification only. No logos are included | OK |
| T-13 | Supplier web pages (PCBWay, NextPCB, Seeed, Eurocircuits, DigiKey, Mouser, LCSC, TI store) | Their owners | Short facts, dates and URLs in the profiles and reports. No page content is copied | OK |

## 3. Tools and software dependencies (not distributed with this project)
| # | Tool / library | Licence (as checked) | Used by | Note |
|---|---|---|---|---|
| T-20 | KiCad 10.0.8 (EDA suite, `kicad-cli`) | GPL-3.0-or-later, with third-party components under other licences (KiCad `LICENSE.README`) | Design, exports, ERC/DRC | Not distributed. The repository contains only files created with KiCad, not KiCad itself |
| T-21 | KiCad Python module `pcbnew` | GPL-3.0-or-later (part of KiCad) | `import pcbnew` in `scripts/release/audit_release.py`, `hardware/kicad/*/build/*.py`, `ai/workflows/sync_footprint_fields.py`, `reports/v0.0.3/tests/read_board_state.py` | Not distributed. Anyone distributing these scripts **together with** KiCad must follow KiCad's licence |
| T-22 | PyMuPDF 2.1 (bundled in the KiCad Python used here) | Dual: AGPL-3.0 or Artifex commercial licence (package metadata) | `import pymupdf` in `scripts/release/make_2d_views.py`, `hardware/kicad/*/build/preview_routes.py` | Not distributed. Only needed to regenerate PNG previews. Its licence applies to whoever distributes PyMuPDF |
| T-23 | KiCAD-MCP-Server v2.8.3 (`1d204fe`) | MIT, "Copyright (c) 2024 mixelpixx" (its `LICENSE`) | Design automation through MCP (stdio) | Not distributed. Only `.mcp.example.json` (project-written) references it |
| T-24 | Python 3.11 standard library, Node.js 24, Git, Claude Code | their own licences | Runtime / tooling | Not distributed |

## 4. Unresolved items
None. No material with an unverified licence is included in the repository or the release packages.
