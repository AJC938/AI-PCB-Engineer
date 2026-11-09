# DRC Validation — V0.2.0

## Final result (KiCad 10.0.8, `kicad-cli pcb drc --severity-all --schematic-parity`)
| Run | Violations | Unconnected | Schematic parity | Evidence |
|---|---|---|---|---|
| Zones **refilled** by DRC (`--refill-zones`) | **0** | **0** | **0** | `evidence/validation/drc_cli_refilled.json` / `.rpt`, `reports/drc/v0.2.0-drc.json` |
| Zones **as stored** in the board file (no refill) | **0** | **0** | **0** | `evidence/validation/drc_cli_stored_zones.json` |

No exclusions, no severity changes and no rule relaxations (`drc_exclusions: []`). Rules: clearance 0.20, track ≥ 0.20,
via ≥ 0.6/0.3, hole ≥ 0.3, copper-edge 0.5, hole clearance 0.25, courtyards required (MCP `set_design_rules` +
board defaults, read back with pcbnew).

## D-10 zone procedure (as required)
1. Board saved (MCP).
2. Zones refilled by MCP `refill_zones`. It reported success but refused its own save ("file changed externally"):
   the refill writes through a separate path, the same pattern as D-1.
3. The project was reopened in a fresh MCP process, and the stored fill was confirmed with pcbnew (`IsFilled()`).
4. The +3V3_P pad connection was set to solid (`set_zone_connection.py`, pcbnew `ZONE_FILLER`, saved).
5. kicad-cli DRC was run both with and without refill: identical, 0/0/0.
6. Fill areas were independently read: +3V3_P 251.2 mm², EF_RTN 38.0, GND top 3419.2, GND bottom 5342.1 mm².

## History (problems found and fixed)
| Stage | Result | Fix |
|---|---|---|
| First routed board | 13 errors (5 shorts, 4 clearance, 1 hole clearance, 2 mask bridge, 1 starved thermal), 23 silk warnings, 77 parity warnings | router pad model corrected and rerouted; silkscreen placer; field sync (D-3); NC pad nets (D-24); BOM flags |
| After reroute | 0 errors, 23 silk warnings, 52 parity (Datasheet field) | Datasheet field sync, silkscreen placement |
| Final | 0 / 0 / 0 | — |

The independent check was run with KiCad's own engine, not MCP `run_drc` (no parity check, D-6; no refill, D-10).
