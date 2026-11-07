# Environment Report — V0.0.1

Verified on 2026-11-07 by running each tool (not from memory).
Status: `PASS` · `WARNING` · `FAILED` · `NOT TESTED`

| Component | Status | Version | Location | Notes |
|---|---|---|---|---|
| Windows | PASS | 11 Home 23H2, build 22631, x64 | — | Native Windows workflow |
| KiCad | PASS | 10.0.8 (release build, 2026-10-29) | `%LOCALAPPDATA%\Programs\KiCad\10.0` | Per-user install. IPC API built in (`KICAD_IPC_API=ON`) |
| kicad-cli | PASS | 10.0.8 | `...\KiCad\10.0\bin\kicad-cli.exe` | Not on PATH; called by full path (PATH intentionally unchanged) |
| KiCad Python | PASS | 3.11.5 | `...\KiCad\10.0\bin\python.exe` | Used for all MCP Python work |
| pcbnew | PASS | 10.0.8 | `...\KiCad\10.0\bin\Lib\site-packages` | The README's `lib\python3\dist-packages` path does not apply to KiCad 10 on Windows |
| kipy | PASS (import) | kicad-python 0.8.0 | KiCad site-packages | IPC backend not exercised |
| KiCad IPC API server | WARNING | disabled | `%APPDATA%\kicad\10.0\kicad_common.json` | Deliberately left disabled for V0.0.1 |
| Node.js (MCP runtime) | PASS | 24.22.2 LTS | `%USERPROFILE%\dev\tools\node-v24.22.2` (portable) | Authenticode signature valid (OpenJS Foundation). LTS until 2028-04-30 |
| Node.js (system) | WARNING | 25.6.1 | `C:\Program Files\nodejs` | Odd-numbered line, end-of-life 2026-06-01 (nodejs/Release schedule). Left installed, not used by MCP |
| npm | PASS | 11.19.1 (with Node 24) / 11.9.0 (system) | — | |
| System Python | PASS | 3.11.5 | `%LOCALAPPDATA%\Programs\Python\Python311` | Not used for KiCad (no pcbnew). `python3` resolves to a WindowsApps stub |
| Git | PASS | 2.55.0.windows.4 | `C:\Program Files\Git` | Global identity configured. `core.longpaths` unset (OS long paths enabled) |
| GitHub CLI | PASS | 2.96.0 | — | Authenticated. Not used in V0.0.1 (no push) |
| Claude Code | PASS | 2.1.317 | Bundled with the Claude desktop app | Not on PATH. Reads this project's `.mcp.json` |
| KiCad MCP Server | PASS | v2.8.3 (`stable`, commit `1d204fe3`) | `%USERPROFILE%\dev\tools\KiCAD-MCP-Server` | Built and validated over stdio |
| Symbol libraries | PASS | KiCad 10 stock (224 files) | `...\share\kicad\symbols` | `Device:R` resolved by MCP |
| Footprint libraries | PASS | KiCad 10 stock (155 `.pretty`) | `...\share\kicad\footprints` | `Resistor_SMD:R_0603_1608Metric` placed by MCP |
| 3D models | PASS | 3.14 GB | `...\share\kicad\3dmodels` | Not exercised |
| Free disk (C:) | WARNING | ~32 GB | — | Enough for now. Do not download the JLCPCB catalogue without checking space |
| Workspace | PASS | — | `%USERPROFILE%\dev\AI-PCB-Engineer` | ASCII path, outside OneDrive, full control |
| WSL2 | NOT TESTED | Ubuntu 24.04 present | — | Fallback only |

## Known warnings
1. **Claude Code project-server approval pending.** `claude mcp get kicad` shows
   *Scope: Project config, Status: Pending approval*. The user must approve the
   `kicad` server once (Claude Code security gate) and start a new session.
2. **False "No KiCAD installations found" log warning.** This comes from a legacy
   diagnostic in `python/kicad_interface.py` that only checks KiCad 9's
   `lib\python3\dist-packages` layout. The real discovery in
   `utils/platform_helper.py` handles KiCad 10, and every tool call worked.
3. **`cairosvg` cannot import on its own.** It needs `cairo-2.dll` from KiCad's
   `bin` directory on PATH. The server adds that directory to its own process PATH
   (`ensure_cairo_on_path`). Verified working under that condition. pymupdf is the
   primary SVG rasterizer anyway.
4. **esbuild postinstall blocked** by npm 11.19 `allowScripts`. esbuild is a
   dev-only dependency (vitest), so it does not affect the runtime or the build (`tsc`).
5. **SWIG backend**: edits are written to disk and KiCad must reload. Never edit an
   open project.
6. **Personal library untouched.** The global `sym-lib-table` references the user's
   personal `Buzzer_a1` library on the OneDrive Desktop. It was not modified.
