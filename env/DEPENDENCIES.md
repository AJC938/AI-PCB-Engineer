# Dependencies

## Runtime toolchain
| Dependency | Version | Why | Installed by V0.0.1? | Removal |
|---|---|---|---|---|
| KiCad | 10.0.8 | EDA environment, pcbnew, kicad-cli, libraries | No (pre-existing) | — |
| Node.js (portable) | 24.22.2 LTS | Runs the MCP server | No (pre-existing portable copy, signature verified) | Delete folder |
| KiCAD-MCP-Server | v2.8.3 @ `1d204fe3` | MCP ↔ KiCad bridge | **Yes**: `git clone --branch stable` | Delete `%USERPROFILE%\dev\tools\KiCAD-MCP-Server` |

## Node packages (MCP server, `npm ci` from `package-lock.json`, lockfile v3)
261 packages installed. Production dependencies: see `node-packages.txt`.
- `@modelcontextprotocol/sdk` 1.31.0, `express` 5.2.1, `zod` 3.25.76, `dotenv` 17.2.3
- All packages resolve from `registry.npmjs.org`.
- Install scripts: `esbuild` (blocked by npm `allowScripts`, dev only) and `fsevents` (macOS only, skipped).

## Python packages (installed into KiCad's bundled Python 3.11.5)
Command: `"%LOCALAPPDATA%\Programs\KiCad\10.0\bin\python.exe" -I -m pip install -r requirements.txt`
(run from the MCP server root, exit code 0, `pip check`: no broken requirements).

Snapshots:
- before: `python-packages-before.txt` (12 packages)
- after: `python-packages.txt` (48 packages)

No pre-existing package was upgraded or downgraded (confirmed by `--dry-run` first).

| Required by v2.8.3 | Installed |
|---|---|
| kicad-python (kipy) >= 0.5.0 | 0.8.0 |
| sexpdata >= 1.0.2 | 1.0.2 |
| kicad-skip >= 0.1.0 | 0.2.5 |
| Pillow >= 9.0.0 | 13.0.0 (pre-existing) |
| pymupdf >= 1.24 | 2.1 (brings pymupdf4llm, pymupdf_layout, onnxruntime 1.31.1) |
| cairosvg >= 2.7.0 | 2.9.1 (needs KiCad `bin` on process PATH, see ENVIRONMENT_REPORT) |
| colorlog >= 6.7.0 | 6.12.0 |
| pydantic >= 2.5.0 | 2.14.3 |
| requests >= 2.32.5 | 2.34.2 (pre-existing) |
| python-dotenv >= 1.0.0 | 1.2.4 |

**Rollback:** `python.exe -I -m pip uninstall` the packages that appear only in
`python-packages.txt`, or reinstall KiCad. A KiCad reinstall or upgrade will
remove these packages, so re-run the install afterwards.

## Optional (not installed)
| Integration | Status | Notes |
|---|---|---|
| Freerouting | Deferred | Needs Java (`JAVA_HOME`). `autoroute` toolbox |
| JLCPCB / LCSC catalogue | Deferred | Large local DB download. API keys optional (`.env` in server root) |
| Digi-Key API | Deferred | Production app credentials, `.env` only |
| LTspice / ngspice | Deferred | KiCad 10 ships ngspice 46 internally |
| KiCad IPC API | Deferred | kipy installed. Enable in KiCad when evaluated |
