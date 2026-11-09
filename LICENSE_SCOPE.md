# Licence Scope

This repository contains material under **different licences**. Neither licence covers the whole repository.
The machine-readable version of this map is [`REUSE.toml`](REUSE.toml) (SPDX identifiers).

| Licence | SPDX | Text |
|---|---|---|
| CERN Open Hardware Licence Version 2 – Permissive | `CERN-OHL-P-2.0` | [LICENSE-HARDWARE](LICENSE-HARDWARE) (official text, unmodified) |
| MIT License | `MIT` | [LICENSE-CODE](LICENSE-CODE) |
| Third-party material | per item | [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) |

Copyright holder of the project's original material: **AI-PCB-Engineer contributors** (2026).

## 1. Hardware source and hardware documentation — `CERN-OHL-P-2.0`
Original material created by this project that is used to make, assemble or test the board. Unless a later
row in this document says otherwise, this covers:

| Path | Content |
|---|---|
| `hardware/kicad/Sensor_Interface_Power_Board/*.kicad_pro`, `*.kicad_sch`, `*.kicad_pcb`, `fp-lib-table` | KiCad project, schematic and PCB (see §4 for the KiCad library data embedded in them) |
| `manufacturing/**` | Gerber, Excellon, IPC-D-356, BOM, CPL, assembly drawings, schematic PDF, STEP, ZIP packages, fabrication/assembly notes, manufacturer profiles, checksums |
| `media/renders/**` | KiCad-generated images of the board |
| `docs/**` (except the software rows below) | Architecture, electrical design, pinout and connection guide, layout, manufacturing, assembly, safety, validation, visual review, requirements, engineering rules, licensing guides |
| `reports/**` (except `*.py`) | Design, audit and validation reports and their evidence, including the V0.0.2/V0.0.3 test designs |
| `calculations/**` outputs (`*.txt`, `*.md`) | Calculation results used to choose component values |
| `datasheets/*.md`, `datasheets/*/*.md` | Datasheet indexes (links and facts; no datasheet is redistributed) |
| `release/**`, `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `PROJECT_SCOPE.md`, `NOTICE.md`, `MODIFICATIONS.md`, `LICENSE_SCOPE.md`, `THIRD_PARTY_NOTICES.md` | Release and project documentation |
| `scripts/release/package_readmes/*.md`, `scripts/release/bom_enrichment.csv` | Package READMEs and BOM data (hardware data, stored next to the scripts that use it) |

## 2. Software — `MIT`
| Path | Content |
|---|---|
| `**/*.py`, `**/*.sh` | All original Python and shell code: `scripts/release/`, `hardware/kicad/*/build/`, `ai/workflows/`, `calculations/**/*.py`, `reports/v0.0.3/tests/` |
| `ai/**`, `env/**`, `docs/ai-workflow/**`, `docs/SYSTEM_ARCHITECTURE.md`, `CLAUDE.md` | AI toolchain instructions, environment records and toolchain documentation |
| `.mcp.example.json`, `.env.example`, `.gitignore`, `.gitattributes`, `REUSE.toml` | Repository and tool configuration |

New files in `scripts/release/` and `calculations/v0.3.0/` also carry `SPDX-License-Identifier: MIT` headers.
Historical files are not edited to add headers; this map and `REUSE.toml` cover them.

## 3. Code that generates or checks the hardware (decision record)
Some MIT files contain hardware design information:
- `hardware/kicad/*/build/build_schematic.py` holds the part list and netlist;
- `build_pcb.py` holds the placement;
- `route_pcb.py` computes the routing;
- the audit and calculation scripts check the design.

Decision:
1. These files are **original works of the same copyright holder** and are licensed **directly under MIT**. They
   are not CERN-OHL-P Covered Source being relicensed, so CERN-OHL-P §3.4 does not need to be invoked.
2. If any of them were treated as CERN-OHL-P Covered Source, §3.4 would still allow conveying them under MIT,
   provided that §3.3 is met (keep notices; add a modification notice when modified) and a copy of CERN-OHL-P is
   provided. Every copy of this repository includes [LICENSE-HARDWARE](LICENSE-HARDWARE), and the
   modification-notice rule is in [MODIFICATIONS.md](MODIFICATIONS.md) and
   [docs/licensing/CONTRIBUTOR_NOTICES.md](docs/licensing/CONTRIBUTOR_NOTICES.md).
3. The hardware data they produce (KiCad files, manufacturing outputs) is licensed under CERN-OHL-P-2.0 (§1).
   File extension alone does not decide the licence: `bom_enrichment.csv` sits in `scripts/` but is BOM data,
   so it is CERN-OHL-P-2.0.

## 4. Third-party material (NOT relicensed by this project)
| Material | Licence | Note |
|---|---|---|
| `hardware/kicad/Sensor_Interface_Power_Board/Sensor_Interface_Power_Board.pretty/TI_PWP0016A_…kicad_mod` | `CC-BY-SA-4.0 WITH KiCad-libraries-exception` | Modified from a KiCad library footprint. Stays under the upstream licence (ShareAlike), [LICENSES/CC-BY-SA-4.0.txt](LICENSES/CC-BY-SA-4.0.txt) + [exception](LICENSES/KiCad-libraries-exception.txt) |
| KiCad library symbols and footprints copied into the `.kicad_sch` / `.kicad_pcb`; KiCad 3D model geometry in the STEP file and renders | `CC-BY-SA-4.0 WITH KiCad-libraries-exception` | The exception waives article 3 for designs and generated files that use the library data, so these design files can be distributed under CERN-OHL-P-2.0 |
| Datasheets, manufacturer names and trademarks, tools (KiCad, PyMuPDF, KiCAD-MCP-Server) | their own terms | Not included in the repository; see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) |

## 5. Mixed documents
| File | Treatment |
|---|---|
| `README.md` | CERN-OHL-P-2.0 (hardware documentation). Its "About the design process" paragraph only links to the MIT toolchain documents |
| `CHANGELOG.md`, `reports/v0.0.1`–`v0.0.3` | CERN-OHL-P-2.0 as project documentation. The code inside `reports/v0.0.3/tests/` is MIT (§2) |
| `CONTRIBUTING.md` | CERN-OHL-P-2.0; states which licence applies to each kind of contribution |
| Release-candidate documents written before the licence decision (`reports/v0.3.0/FINAL_V0.3.0_REPORT.md`, tag `v1.0.0-rc1`) | They record that CERN-OHL-S-2.0 was the prepared default at the time. **Superseded:** the final release `v1.0.0` uses CERN-OHL-P-2.0 for hardware |
