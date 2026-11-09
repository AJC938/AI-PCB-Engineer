# Repository Release Audit — V0.3.0

| Check (prompt §20) | Method | Result |
|---|---|---|
| Changed files reviewed | `git status`, `git diff d859317` | Design files: 2 (title block rev, silk label, comment 3). All other changes are new documentation, scripts, outputs and images |
| Previous release integrity | `git diff --stat d859317 -- reports/v0.0.* reports/v0.1.0 reports/v0.2.0 reports/drc reports/erc manufacturing/v0.2.0 calculations/v0.0.2 calculations/v0.1.0 calculations/v0.2.0 datasheets/v0.1.0 datasheets/v0.2.0 hardware/kicad/*/build` | **no diff**. Tags `v0.0.1-baseline`, `v0.0.2`, `v0.0.3-rc1` untouched |
| Machine-specific absolute paths | grep of every committable text file for drive-letter user paths, `/c/Users/`, the local account name, host name, owner e-mail and personal name | **none** in new files. Historical V0.0.3 evidence already uses `<user>`. Generated evidence is passed through `scripts/release/sanitize_paths.py` |
| KiCad project paths | grep of `.kicad_pro/.kicad_sch/.kicad_pcb/fp-lib-table` | no absolute paths; `${KIPRJMOD}` and `${KICAD10_3DMODEL_DIR}` only |
| Secrets | grep for key/secret/password/token assignments | none. `.mcp.json` and `.env*` remain gitignored |
| Package privacy | member-by-member scan in `make_packages.py`, PDF stream decompression scan, STEP header | none |
| Duplicated binaries | ZIPs repeat the files of `RevA/` (≈ 1.3 MB): intentional release assets, so users can download a package without git. Renders ≈ 4.2 MB. No other duplicates | accepted |
| Temporary files | `.gitignore` excludes `*.lck`, `.kicad_prl`, `.mcp-backups/`, `__pycache__/`, `fp-info-cache`, logs | clean |
| Line endings | `.gitattributes`: KiCad and Markdown normalized to LF; release folder `-text` (byte-exact); `*.zip` binary | checksums hold after clone |
| Reopen in a clean process | KiCAD-MCP-Server (SWIG) in a new process: `open_project`, `get_board_info`, `query_zones`, `get_nets_list`, `validate_schematic`, `run_erc`, `is_dirty` | 7/7 OK; ERC 0; board not dirty; design files byte-unchanged (SHA-256 before/after) |
| Links | relative-link checker over every new or changed Markdown file | 0 broken |
| Working tree | `git status` after the release commit | clean (see final report) |

## Structure decisions
- The KiCad project stays at `hardware/kicad/Sensor_Interface_Power_Board/` (not moved to a new tree). Moving it
  would break the generator scripts' relative paths, links in the V0.1.0/V0.2.0 reports and the reproducible history, and the project was open in
  the KiCad project manager during this session. `hardware/README.md` explains the layout.
- Release outputs live in `manufacturing/Sensor_Interface_Power_Board/RevA/`. The V0.2.0 package stays in
  `manufacturing/v0.2.0/` as history.
- Images live in `media/renders/` (the existing media folder). New scripts are in `scripts/release/`. Existing
  generator and verifier scripts stay with the project (`build/`) and in `ai/workflows/`.

## KiCad session note
During this milestone the KiCad **project manager** held `~Sensor_Interface_Power_Board.kicad_pro.lck`. No
`.kicad_sch`/`.kicad_pcb` lock existed, so the schematic and PCB editors were closed. `.kicad_pro` was never written.
`set_release_revision.py` refuses to run if an editor lock exists. If the owner opens the editors from the
already-running project manager, they load the updated files from disk.
