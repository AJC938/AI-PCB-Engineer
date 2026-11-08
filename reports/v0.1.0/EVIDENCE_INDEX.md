# Evidence Index — V0.1.0

Every claim in the V0.1.0 reports traces to one of the items below. Paths are relative to the repository root.
Machine-specific paths in evidence files were replaced with `%USERPROFILE%` / `<user>`.

## Design sources
| ID | Item | Path | Label |
|---|---|---|---|
| E-01 | Datasheet index (DS-01…DS-16: URL, revision, extracted facts) | `datasheets/v0.1.0/DATASHEET_INDEX.md` | VERIFIED (datasheet) |
| E-02 | Phase 1 requirements, interface spec, risks, open questions | `docs/requirements/v0.1.0/` | baseline |
| E-03 | Design calculations (tagged inputs) + output | `calculations/v0.1.0/design_calcs.py`, `design_calcs_output.txt` | CALCULATED |
| E-04 | Independent Monte Carlo checks (200 000 samples, seed 20261108) + output | `calculations/v0.1.0/independent_checks.py`, `independent_checks_output.txt` | CALCULATED (independent) |

## Schematic and build
| ID | Item | Path | Label |
|---|---|---|---|
| E-10 | KiCad project (schematic, project, empty PCB) | `hardware/kicad/Sensor_Interface_Power_Board/` | design file |
| E-11 | Schematic generator: PARTS and NETS tables = single source of truth | `hardware/kicad/Sensor_Interface_Power_Board/build/build_schematic.py` | reproducible |
| E-12 | Controlled paper/title-block edit | `.../build/set_page_a3.py` | documented non-MCP edit |
| E-13 | Independent netlist verifier | `.../build/verify_schematic.py` | TOOL-CHECKED |
| E-14 | MCP harness used for all MCP calls | `ai/workflows/mcp_harness.py` | tool |

## Validation evidence (`reports/v0.1.0/evidence/`)
| ID | Item | File | Shows |
|---|---|---|---|
| E-20 | MCP run: create project | `mcp_runs/run_s1.json` | project created via SWIG |
| E-21 | MCP run: full build (326 calls, 0 failed) + validate + ERC + netlist | `mcp_runs/run_s2.json` | ERC 0 |
| E-22 | MCP run: header MPN change to HTSW | `mcp_runs/run_s3.json` | ERC 0 |
| E-23 | MCP run: capacitor value text change | `mcp_runs/run_s4.json` | ERC 0 |
| E-24 | MCP run: re-open in a fresh process | `mcp_runs/run_s5.json` | persisted, ERC 0 |
| E-25 | kicad-cli ERC, all severities | `validation/erc_cli.json` | 0 violations, no exclusions |
| E-26 | kicad-cli netlist (kicadxml) | `validation/netlist_cli.xml` | 50 components, 29 nets |
| E-27 | Verifier output | `validation/verify_output.txt` | PASS (nets, domains, footprints, metadata) |
| E-28 | kicad-cli BOM | `validation/bom_cli.csv` | 32 lines with MPNs |
| E-29 | Schematic PDF | `validation/Sensor_Interface_Power_Board_schematic.pdf` | review copy |
| E-30 | Schematic renders | `images/sch_overview.png`, `images/sch_rail_right.png` | visual review |

## Not available (by nature of this milestone)
| Item | Label |
|---|---|
| PCB layout, DRC, Gerbers | NOT STARTED (V0.2.0) |
| Fabrication, assembly | NOT DONE |
| Any physical measurement | **NOT TESTED** (`testing/` has no V0.1.0 records) |
