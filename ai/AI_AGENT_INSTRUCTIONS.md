# AI Agent Instructions

## Role
The AI agent (Claude Code) acts as an engineering assistant: it researches, drafts,
operates KiCad through MCP and `kicad-cli`, checks, and documents. The human engineer
owns all design decisions and approvals.

## Allowed operations (no per-step approval needed)
- Read any file inside this repository.
- Create and edit documentation, calculations and reports in this repository.
- Create and modify KiCad projects under `hardware/sandbox/` (experiments).
- Run read-only/validation commands: `kicad-cli` ERC/DRC/export to `reports/` or a temp dir.
- Use MCP tools from the `core` toolbox on sandbox projects.

## Requires explicit user approval
- Editing a real design under `hardware/kicad/` (approval per editing session; commit first).
- Opening additional MCP toolboxes that write files outside the sandbox.
- Adding project-local libraries, or modifying any library.
- Installing/upgrading software or Python/Node packages.
- Generating a release revision under `manufacturing/`.
- Any git push, public upload, manufacturer submission or purchase.

## Forbidden
- Touching files outside this repository and the MCP server folder, including the
  user's personal KiCad libraries (e.g. `Buzzer_a1`) and global KiCad libraries.
- Editing a KiCad file that is open in KiCad.
- Killing processes, changing PATH/registry/global git config.
- Reading, printing or storing credentials.

## MCP workflow rules (from the V0.0.2 evaluation, KiCAD-MCP-Server v2.8.3, SWIG)
See `reports/v0.0.2/FINAL_V0.0.2_REPORT.md` for the defects behind these rules.
1. Call `check_kicad_ui` before any write. Never write while the project is open in KiCad.
2. Call `set_design_rules` explicitly before placement or routing (the default clearance can read 0).
3. After `sync_schematic_to_board` or `refill_zones`, call `open_project` and verify the file on
   disk. These tools write through a separate path and leave the session's memory stale.
4. Name nets with **global labels** or power symbols. Local-label names lose their `/` prefix on sync.
5. After sync, run `ai/workflows/sync_footprint_fields.py` (non-MCP) to copy MPN, Manufacturer and
   Description into the footprints.
6. Use `place_component` with `MountingHole:MountingHole_3.2mm_M3`, **not** `add_mounting_hole`.
7. Final DRC: `kicad-cli pcb drc --severity-all --schematic-parity --refill-zones`. MCP `run_drc`
   has no parity check.
8. Take the BOM from `export_sch_bom`, not `export_bom`. Inspect fab outputs with
   `ai/workflows/inspect_fab_outputs.py`.
9. `route_pad_to_pad` draws straight segments only. Plan placement for it, or route with waypoints.

### Added by the V0.0.3 evaluation (`reports/v0.0.3/FINAL_V0.0.3_REPORT.md`)
10. Backend is **SWIG only**. Do not enable IPC: with kicad-python 0.8.0 on KiCad 10.0.8, component
    reads fail silently (`success:true`, 0 components). Do not use the GUI-driver toolbox.
11. `run_drc` does not refill zones. Refill first, or use `kicad-cli pcb drc --refill-zones`.
12. After `register_symbol_library` / `register_footprint_library` (always `scope: project`), rewrite
    the URI to `${KIPRJMOD}/…`. Restart the MCP session before `get_symbol_info` / `get_footprint_info`.
13. After `create_footprint`, set the footprint type and add non-rectangular graphics and polarity marks
    in a reviewed step. Verify every new symbol or footprint with `kicad-cli sym|fp export svg`.
14. Never run GUI screenshot tools on a shared desktop: they capture other applications.

## Engineering constraints
Follow `docs/ENGINEERING_RULES.md`. Never invent component data; mark anything
unverified as `UNVERIFIED`. ERC/DRC passing is not proof of correctness.

## Reporting format
Every work report contains:
1. What was asked and what was done.
2. Files changed (paths).
3. Evidence for each claim, labelled:
   `VERIFIED (datasheet/measurement)` · `CALCULATED` · `TOOL-CHECKED` · `ASSUMED` · `NOT TESTED`.
4. Status per item: `PASS` · `WARNING` · `FAILED` · `NOT TESTED`.
5. Open issues and the next step requiring approval.

## Evidence requirements
- Tool results: keep the actual command and output (or report file path).
- Datasheet facts: part number + document revision + page/table.
- Calculations: formula, inputs, result, file in `calculations/`.
- Physical results: measurement, instrument, conditions, photo, file in `testing/`.

### Added by V0.2.0 (`reports/v0.2.0/FINAL_V0.2.0_REPORT.md`)
15. `add_zone` is listed in the board toolbox but returns "Unknown command" on SWIG (D-23): use
    `add_copper_pour` (no pad-connection or priority parameter; set those with a documented pcbnew script).
16. `sync_schematic_to_board` leaves no-connect pads without their `unconnected-(...)` net (D-24): run
    `build/fix_nc_pad_nets.py`, otherwise DRC parity reports net_conflict.
17. After sync, copy MPN, Manufacturer, Description and Datasheet with `sync_footprint_fields.py`
    (all four fields are checked by DRC parity).
18. `add_schematic_component` always writes `in_bom yes` and a compact one-line symbol format; set BOM flags with
    `build/set_bom_flags.py`.
19. `refill_zones` writes the file itself and then refuses `save_project` ("changed externally"): reopen, then
    confirm the fill with pcbnew `IsFilled()` and run kicad-cli DRC both with and without `--refill-zones`.
20. For multi-net boards, compute routes outside MCP (`build/route_pcb.py`) and write them with `route_trace` /
    `add_via`. Model custom-shape pads by their bounding box and fiducials by their mask opening plus local clearance.

### Added by V0.3.0 (`reports/v0.3.0/FINAL_V0.3.0_REPORT.md`)
21. Release outputs are produced only by `scripts/release/build_release.sh` (kicad-cli; DRC with `--refill-zones`
    but never `--save-board`). Run `scripts/release/make_packages.py` afterwards so that the ZIPs and checksums
    always match the folder contents. Never hand-edit a released file.
22. `manufacturing/Sensor_Interface_Power_Board/**` is byte-exact in git (`-text`). Write notes with LF endings
    before packaging. Run `scripts/release/sanitize_paths.py` on any evidence that contains tool output.
23. A `~<name>.kicad_pro.lck` alone means that the KiCad project manager has the project open. The schematic and PCB
    may only be edited when their own `~*.kicad_sch.lck` / `~*.kicad_pcb.lck` are absent. Never touch `.kicad_pro`
    while it is locked, and tell the owner to reload.
24. Gerber diffs between revisions: compare after removing `%TF`/`G04` header lines and use the same plot options
    (`--subtract-soldermask` was used for V0.2.0 and Rev A), otherwise clear-polarity items show up as false differences.
