# Evidence Index — V0.2.0

Paths relative to the repository root. Machine paths in logs were replaced with `%USERPROFILE%` / `<user>`.

## Sources and calculations
| ID | Item | Path | Label |
|---|---|---|---|
| E2-01 | Datasheet additions DS-17…DS-20 (+ addenda) | `datasheets/v0.2.0/DATASHEET_INDEX.md` | VERIFIED (datasheet) |
| E2-02 | Design calculations V0.2.0 + output | `calculations/v0.2.0/design_calcs_v020.py`, `_output.txt` | CALCULATED |
| E2-03 | Independent Monte Carlo (100 000, seed 20261109) + output | `calculations/v0.2.0/independent_checks_v020.py`, `_output.txt` | CALCULATED (independent) |
| E2-04 | Manufacturer facts (official pages, 2026-11-09) | `reports/v0.2.0/MANUFACTURER_COMPARISON.md` | VERIFIED (vendor page) / NOT FOUND marked |

## Design sources (reproducible build)
| ID | Item | Path |
|---|---|---|
| E2-10 | KiCad project (schematic, PCB, project, fp-lib-table, project footprint library) | `hardware/kicad/Sensor_Interface_Power_Board/` |
| E2-11 | Schematic generator (PARTS/NETS), BOM flags, page setup | `build/build_schematic.py`, `set_bom_flags.py`, `set_page_a3.py` |
| E2-12 | U5 footprint generator (TI PWP0016A) | `build/make_footprints.py` |
| E2-13 | Placement plan + checker + MCP steps | `build/build_pcb.py` |
| E2-14 | Router (geometry) | `build/route_pcb.py`, preview `build/preview_routes.py` |
| E2-15 | Silkscreen placer | `build/place_silk.py` |
| E2-16 | Workarounds: NC pad nets (D-24), zone connection, PCB title | `build/fix_nc_pad_nets.py`, `set_zone_connection.py`, `set_pcb_title.py` |
| E2-17 | Verifiers: netlist/domains, pcbnew read-back, fab audit, BOM builder | `build/verify_schematic.py`, `pcb_extract.py`, `audit_fab_outputs.py`, `make_bom.py`, `fp_report.py` |

## Validation (`reports/v0.2.0/evidence/`)
| ID | Item | File | Shows |
|---|---|---|---|
| E2-20 | ERC kicad-cli (json + report) | `validation/erc_cli.json`, `.rpt`; `reports/erc/v0.2.0-erc.json` | 0 violations |
| E2-21 | DRC kicad-cli, refilled zones | `validation/drc_cli_refilled.json`, `.rpt`; `reports/drc/v0.2.0-drc.json` | 0 / 0 / 0 |
| E2-22 | DRC kicad-cli, stored zones | `validation/drc_cli_stored_zones.json` | 0 / 0 / 0 |
| E2-23 | Netlist + verifier | `validation/netlist_cli.xml`, `verify_output.txt` | PASS |
| E2-24 | Manufacturing audit | `validation/fab_audit_output.txt` | 11/11 PASS |
| E2-25 | Schematic PDF (gate A state) | `validation/Sensor_Interface_Power_Board_schematic_v0.2.0.pdf` | — |
| E2-26 | MCP runs: schematic s1/s2/s2inc; PCB p1 sync, p2/p2b/p2c placement, p3/p3b/p3b2 routing + pours, del (rip-up), p4 silk, p5 refill, p6 origin, p7 reopen | `mcp_runs/*.json` | every call and response |
| E2-27 | Router plan, silk plan, pre-route board state | `layout/routes.json`, `silk_plan.json`, `pcb_state_before_routing.json` | — |
| E2-28 | Images: 3D top/bottom/iso/left, copper/silk plots, assembly drawing, schematic, route preview | `images/*.png` | visual review |

## Manufacturing package
`manufacturing/v0.2.0/` (README.md): Gerbers, drill, IPC-D-356, BOM, CPL, drawings, STEP, notes, profiles.

## Not available (by nature of this milestone)
Fabricated boards, assembly, any measurement: **NOT TESTED** (`testing/` has no V0.2.0 records). Manufacturer
quotes, stock confirmations and shipping terms: not requested (no external commitment without approval).
