# V0.0.2 Final Report — MCP Capability Evaluation

Date: 2026-11-07 · Baseline: tag `v0.0.1-baseline` (`c42075b`) · KiCad 10.0.8 · KiCAD-MCP-Server
v2.8.3 (SWIG) · Claude Code 2.1.317 · Test project: `hardware/sandbox/v0.0.2-led-test/`
(snapshot in [`evidence/kicad/`](evidence/kicad/)).

## Result
A complete digital workflow was executed for a 5 V / ≈5 mA LED indicator on a 50 × 30 mm two-layer
THT board, almost entirely through MCP tool calls from Claude Code:

datasheets → calculations → schematic → ERC → netlist → footprints → board sync → placement →
routing → GND zone → DRC → Gerber / drill / BOM / CPL / PDF / STEP → independent inspection.

**Final state:** ERC 0 · DRC 0 errors, 0 warnings · 0 unconnected · schematic parity 0 (kicad-cli).
The MCP and CLI results agree.

**This is a digital engineering validation only. No board was fabricated, assembled or tested.**

## Acceptance criteria
| Criterion | Status | Evidence |
|---|---|---|
| Functional schematic exists | PASS | SCHEMATIC_TEST_REPORT |
| Actual electrical connections | PASS | 7 snapped wires, netlist 3 nets, MCP = CLI |
| ERC executed | PASS | ERC_REPORT (0, PWR_FLAG need proven) |
| Netlist verified | PASS | ERC_REPORT |
| Footprints assigned and checked | PASS (1 WARNING: LED lead tolerance vs Ø0.9 hole) | FOOTPRINT_TEST_REPORT |
| PCB layout exists | PASS | PCB_LAYOUT_REPORT |
| All nets routed | PASS | ROUTING_TEST_REPORT (0 unconnected) |
| DRC executed | PASS | DRC_REPORT |
| CLI validation compared | PASS | DRC_REPORT, ERC_REPORT |
| Gerber and drill exported and inspected | PASS | MANUFACTURING_EXPORT_REPORT |
| BOM generated and checked | PASS (schematic BOM). WARNING (MCP PCB BOM) | MANUFACTURING_EXPORT_REPORT |
| Capability reports exist | PASS | this folder |
| Limitations documented | PASS | below |
| Baseline preserved | PASS | tag `v0.0.1-baseline`, no history rewritten |

## Component selection (datasheet-verified)
| Ref | Part | Key verified facts |
|---|---|---|
| D1 | Kingbright WP7113ID (5 mm red diffused) | VF 1.9 typ / 2.3 max @10 mA, IF 30 mA, VR 5 V, hole Ø0.9 @ 2.54 mm |
| R1 | Yageo MFR-25FBF52-620R (620 Ω 1 % ¼ W) | 0.25 W @70 °C, 250 V, L 6.3 / D 2.4 / d 0.55 mm |
| J1 | Phoenix Contact MKDS 1,5/ 2-5,08 (1715721) | 5.08 mm, 17.5 A, pins 0.9×0.9, hole Ø1.3 |

Calculated current: 5.16 mA nominal, 3.91–5.78 mA worst case. R1 dissipates at most 20.5 mW (8 % of rating).
**Design WARNING:** a reversed supply would put about 5.25 V reverse across D1, which exceeds VR 5 V.
There is no reverse protection, only polarity marking on the silkscreen.

## Defects and limitations
| ID | Area | Observation | Impact | Workaround used |
|---|---|---|---|---|
| D-1 | sync_schematic_to_board, refill_zones | They write the board through a separate path. The in-memory session then sees "on-disk contents changed externally" and **refuses auto-save**. The on-disk file was correct each time | Stale in-memory state (e.g. `get_nets_list` showed a removed net) | **Always `open_project` after sync or refill**, then verify on disk |
| D-2 | sync_schematic_to_board | Local-label nets lose KiCad's sheet prefix (`/LED_A` becomes `LED_A`). Auto-named nets differ too (`Net-(D1-Pad2)` vs `Net-(D1-A)`) | Schematic-parity `net_conflict` | Name every net with a **global label** (or power symbol) |
| D-3 | sync_schematic_to_board | Custom/standard fields (MPN, Manufacturer, Description) are not copied to footprints. No MCP tool can write them | Parity `footprint_symbol_field_mismatch`. PCB-side BOM has no MPN | Non-MCP script [`ai/workflows/sync_footprint_fields.py`](../../ai/workflows/sync_footprint_fields.py) (KiCad pcbnew API) |
| D-4 | add_mounting_hole | Writes lib ID `MountingHole:MountingHole_3.2mm`, which doesn't exist, plus silkscreen inside the mask opening | DRC `lib_footprint_issues` + `silk_over_copper` | `place_component` with `MountingHole:MountingHole_3.2mm_M3` |
| D-5 | export_bom (PCB) | Ignores `exclude_from_bom` and `includeAttributes` | Wrong BOM if used for ordering | Use `export_sch_bom` |
| D-6 | run_drc | No schematic-parity check | Parity errors invisible to MCP | `kicad-cli pcb drc --schematic-parity` |
| D-7 | get_footprint_info | No pad coordinates or drill sizes | Cannot verify a footprint through MCP alone | Read `.kicad_mod`, then `get_component_pads` after placement |
| D-8 | check_courtyard_overlaps | Hole "courtyard" bounding box about 20 mm wide (seems to include text) | False boundary violations | Trust KiCad DRC courtyard rules |
| D-9 | get_board_2d_view | Monochrome render, unusable once a zone is filled | Weak visual review | `kicad-cli pcb render` (3D) |
| L-1 | route_pad_to_pad | Single straight segment, no obstacle avoidance | Needs placement planned for straight routes | Fine here. Denser boards need waypoints or an autorouter |
| L-2 | set_design_rules | Board default clearance read back as 0 | DRC would miss clearance errors | Always set rules explicitly first |
| L-3 | Server note vs client | Toolbox tools usable in the same turn in Claude Code (the note says next message) | None | — |
| L-4 | Schematic aesthetics | PWR_FLAG text overlaps power symbol text | Cosmetic | `schematic_layout` toolbox (not tested) |

## IPC and Freerouting assessment (from the findings above)
| Question | Finding |
|---|---|
| 1. Is SWIG reliable enough? | **Yes for this scale.** 0 crashes in about 140 MCP tool calls, including 2 zone refills. Reliability depends on the reload discipline (D-1) |
| 2. Are files saved correctly? | Yes, **on disk**. Each write was verified by file inspection or kicad-cli. 20 automatic pre-write backups in `.mcp-backups/`. The in-memory state can go stale (D-1) |
| 3. Does synchronization work? | Partially. Footprints, pads, nets and net renames on existing tracks work. Naming (D-2) and fields (D-3) do not |
| 4. Does MCP routing work for this circuit? | Yes: 3 nets, 0 unconnected, DRC clean, but only with straight-line routes (L-1) |
| 5. Are GUI interactions necessary? | **No.** The whole flow ran headless with KiCad closed. The GUI would only help with human visual review |
| 6. Would IPC materially improve reliability? | Probably for D-1, because it edits the live board instead of files. It would also enable `add_component_3d_model` and avoid the SWIG refill crash risk. Costs: KiCad must be open, which changes the "never edit an open project" rule, and the IPC path was not tested here. **Not proven, so not recommended as default yet** |
| 7. Is Freerouting needed? | **Not for this board.** It becomes relevant for boards with many nets or tight layouts. Requires Java. Not installed |

**Recommendation:** keep SWIG as the default for V0.0.x, with the mandatory workflow rules below.
Evaluate IPC in a dedicated sandbox milestone (enable the API server in KiCad, compare D-1 behaviour).
Defer Freerouting until the first real board's net count justifies it. Nothing was enabled or installed.

## Mandatory MCP workflow rules (added to `ai/AI_AGENT_INSTRUCTIONS.md`)
1. `check_kicad_ui` before writing. Never write while the project is open in KiCad.
2. `set_design_rules` explicitly before placement or routing.
3. After `sync_schematic_to_board` or `refill_zones`: `open_project`, then verify on disk.
4. Name nets with global labels or power symbols.
5. After sync, copy fields with `sync_footprint_fields.py` until D-3 is fixed upstream.
6. Final DRC with `kicad-cli pcb drc --severity-all --schematic-parity --refill-zones`.
7. BOM from `export_sch_bom`. Inspect fab outputs with `inspect_fab_outputs.py`.

## What is NOT tested
Physical fit of parts, soldering, power-up, LED current measurement, IPC backend, GUI driver,
Freerouting, part sourcing (JLCPCB / Digi-Key / parts-registry), custom symbol/footprint creation,
hierarchical schematics, multi-layer (>2) boards, and about 190 discovered tools.

## Next phase (proposed)
V0.0.3: IPC backend evaluation in the sandbox and a test of custom symbol/footprint creation
(`symbol_library`, `footprint` toolboxes). Then V0.1.0: requirements for the first real board.
