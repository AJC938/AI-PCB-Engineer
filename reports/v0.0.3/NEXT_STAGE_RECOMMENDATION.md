# Next Stage Recommendation (after V0.0.3)

## Recommended architecture
```
Claude Code ─MCP─▶ KiCAD-MCP-Server v2.8.3 (SWIG backend, core + task toolboxes)
                       ├─ schematic / symbol_library / footprint / board / routing / drc / export
                       └─ files on disk ◀── kicad-cli (independent ERC, DRC + parity, exports)
                                         ◀── pcbnew API scripts (field sync, readback)
```
- Backend: **SWIG only** (`KICAD_BACKEND=swig`, as configured). KiCad GUI closed while the agent edits.
- IPC: **do not enable** in the workflow (D-16 to D-19).
- GUI driver: **do not use** (D-20 to D-22).

## Workflow rules to add (on top of the V0.0.2 rules)
1. `run_drc` does not refill zones. Refill (or run `kicad-cli pcb drc --refill-zones`) before judging zone-related errors (D-10).
2. After `register_symbol_library` / `register_footprint_library`, rewrite the project table URI to
   `${KIPRJMOD}/…` before committing (D-11). Then restart the MCP session before any lookup tool (D-12).
3. Prefer `list_library_symbols` over `search_symbols` for project libraries (D-13).
4. After `create_footprint`: set the footprint type (THT/SMD) and add any non-rectangular graphics
   (outline circles, polarity marks) with a reviewed pcbnew script or a careful file edit. Re-check with
   `kicad-cli fp export svg` and DRC (D-14).
5. Symbol pin `angle` uses KiCad's file convention (toward the body). Verify every new symbol with a
   `kicad-cli sym export svg` render (D-15).
6. Never use GUI screenshot tools on a shared desktop.

## Remaining gaps
| Gap | Impact | Suggested handling |
|---|---|---|
| IPC unusable with kicad-python 0.8.0 on KiCad 10.0.8 | no live GUI sync | re-test when kicad-python supports KiCad 10 board types. Start with a direct kipy `get_footprints()` probe |
| `create_footprint` graphics | footprints need a post-edit | small pcbnew helper (to be reviewed) or manual KiCad footprint editor work |
| Absolute library URIs | repo not portable | URI fix-up step (script) |
| Single-run latency data | no statistical comparison | not needed while IPC is unusable |
| Routing is straight-line only (V0.0.2) | dense boards need waypoints or an autorouter | evaluate `route_trace` with waypoints in V0.1.x. Freerouting only if the net count justifies it |
| No manufacturer rule set | DRC rules are generic | pick the fab in V0.1.0 and encode its capabilities |

## Readiness for V0.1.0
**Ready**, on the SWIG-based workflow with the documented rules. V0.1.0 is requirements and component
selection, which does not depend on IPC or the GUI driver. Custom symbol and footprint creation, which
real boards will need, is verified as workable, with the post-edit step above. No further evaluation
stage is required before V0.1.0. IPC can be re-evaluated in parallel when a compatible kicad-python exists.

V0.1.0 entry requirements:
1. Approved target-board requirements (function, power, interfaces, size, environment, budget, fab).
2. Manufacturer chosen, and its design rules recorded with source and date.
3. Datasheets collected and indexed for the candidate parts (manufacturer sources only).
4. The workflow rules above added to `ai/AI_AGENT_INSTRUCTIONS.md` (done in this branch).
