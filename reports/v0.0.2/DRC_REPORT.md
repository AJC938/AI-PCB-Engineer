# DRC Report — V0.0.2

Final evidence: [`evidence/checks/drc_cli.json`](evidence/checks/drc_cli.json) (kicad-cli, all
severities, schematic parity, zones refilled), [`evidence/checks/drc_mcp.rpt`](evidence/checks/drc_mcp.rpt).

## Iterations
| # | State | MCP `run_drc` | kicad-cli DRC (`--severity-all --schematic-parity`) | Action |
|---|---|---|---|---|
| 1 | Routed + zone + MCP-generated holes | 0 err, 8 warn: 4 `lib_footprint_issues`, 4 `silk_over_copper` | — | Holes replaced with the library footprint (D-4) |
| 2 | Library holes | 0 err, 2 warn: `silk_edge_clearance` (H1/H2 refs) | 2 violations, 0 unconnected, **9 parity**: 2 net_conflict `Net-(D1-Pad2)` vs `Net-(D1-A)`, 3 MPN missing, 4 extra footprint | Hide hole refs. Holes marked board-only. Net named |
| 3 | Local label `LED_A` | — | 0 violations, 0 unconnected, 5 parity: 2 net_conflict `LED_A` vs `/LED_A`, 3 MPN missing | Global label instead (D-2) |
| 4 | Global label + field-copy script | — | 0 / 0 / 3 parity: `Description` differs | Script re-run for Description |
| 5 | **Final** | **0 errors, 0 warnings** | **0 violations, 0 unconnected, 0 parity** | — |

## MCP vs CLI discrepancies
| Item | Explanation |
|---|---|
| Schematic parity | MCP `run_drc` does not run it, so 9 real issues were invisible to MCP (D-6). Always run `kicad-cli pcb drc --schematic-parity` |
| Violation counts | Identical whenever both ran on the same saved board (iteration 2: 2 = 2. Final: 0 = 0) |
| Side effect | MCP `run_drc` writes `led_test_drc_violations.json` next to the board file |

## Checks covered
| Check | How | Result |
|---|---|---|
| Clearance (copper, hole, edge) | DRC rules (0.25 / 0.25 / 0.5 mm) | PASS |
| Board connectivity / unrouted nets | DRC unconnected items | PASS: 0 |
| Board outline | DRC (closed Edge.Cuts) + Gerber extents 50 × 30 mm | PASS |
| Courtyards | DRC + `check_courtyard_overlaps` (components) | PASS |
| Footprint-to-pad mapping | schematic parity 0 + pad/net table (FOOTPRINT_TEST_REPORT) | PASS |
| Drill | drill file vs datasheet holes (0.8 / 0.9 / 1.3 / 3.2) | PASS (with the LED lead-tolerance WARNING in the footprint report) |
| Manufacturing rules | Generic conservative rules. **No specific fab profile** | WARNING: to verify against the chosen manufacturer |
| Silkscreen | DRC silk checks | PASS (after hiding hole refs) |

No rule exclusions or severity overrides were used to reach zero.
