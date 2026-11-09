# AI Toolchain Setup (Claude Code → MCP → KiCad)

> Moved from the repository README in V0.3.0. This page documents the AI-assisted design workflow used to
> create the board. It is **not** needed to open, manufacture or use the hardware. Statements about versions
> below describe the state at V0.0.2 and are kept for history; current status is in the root README.

An AI-assisted PCB engineering workflow, using **Claude Code → MCP → KiCad 10**, aimed at
designing, manufacturing, assembling and physically testing a real PCB.

**Current version:** `0.0.2`: MCP capability evaluation completed on a full LED test board
(schematic → ERC → PCB → routing → DRC → Gerber/drill/BOM/CPL), digitally validated only.
Results: [reports/v0.0.2/FINAL_V0.0.2_REPORT.md](../../reports/v0.0.2/FINAL_V0.0.2_REPORT.md).
`0.0.1` (environment setup and MCP integration) is complete.
The MCP connection was verified inside Claude Code: `kicad` server connected, backend SWIG,
37 core tools, `get_backend_state` OK.

## Architecture
```
Claude Code ─MCP/stdio─▶ KiCad MCP Server v2.8.3 (Node 24 LTS)
                              └─▶ Python bridge (KiCad 10 bundled Python 3.11)
                                     ├─ pcbnew (SWIG backend, active)
                                     ├─ kicad-skip / sexpdata (schematics)
                                     └─ kipy (IPC API, installed, not yet used)
                                            ▼
                                       KiCad 10.0.8 files ◀── kicad-cli (independent ERC/DRC/exports)
```
Details: [docs/SYSTEM_ARCHITECTURE.md](../../docs/SYSTEM_ARCHITECTURE.md)

## Installed requirements (verified)
KiCad 10.0.8 · KiCad Python 3.11.5 + pcbnew · Node.js 24.22.2 LTS (portable) ·
KiCAD-MCP-Server v2.8.3 · Git 2.55. Full list with statuses:
[env/ENVIRONMENT_REPORT.md](../../env/ENVIRONMENT_REPORT.md) and [env/DEPENDENCIES.md](../../env/DEPENDENCIES.md).

## Setup (Windows 11, reproducing on another machine)
1. Install KiCad 10.x (per-user is fine).
2. Get Node.js 24 LTS. A portable zip under `%USERPROFILE%\dev\tools\` works.
3. Install the MCP server:
   ```powershell
   cd $env:USERPROFILE\dev\tools
   git clone --branch stable https://github.com/mixelpixx/KiCAD-MCP-Server.git
   cd KiCAD-MCP-Server
   git checkout 1d204fe3            # v2.8.3
   $env:Path = "$env:USERPROFILE\dev\tools\node-v24.22.2;$env:Path"   # this shell only
   npm ci                           # also runs the TypeScript build
   & "$env:LOCALAPPDATA\Programs\KiCad\10.0\bin\python.exe" -I -m pip install -r requirements.txt
   ```
4. Copy `.mcp.example.json` to `.mcp.json` in this repo and replace `<USERPROFILE>` and
   `<LOCALAPPDATA>` with real absolute paths. `.mcp.json` is gitignored.

## Connecting Claude Code
1. Open a **new** Claude Code session with this folder as the working directory.
2. Claude Code asks whether to trust the project MCP server `kicad` from `.mcp.json`.
   Approve it. In the CLI, `/mcp` shows its status.
3. Check: the session should list `kicad` tools (37 with the `core` toolbox). Ask, for
   example, "call get_backend_state". The expected answer is `backend: swig`.
   (Verified 2026-11-07.) Note: the bundled CLI `claude mcp get kicad` may still print
   "Pending approval" after approving in the desktop app. This is a known, non-blocking
   inconsistency; the in-session tool calls are the authoritative check.
4. Open more toolboxes only when needed (`list_toolboxes`, `open_toolbox`).

Rules for every session: [CLAUDE.md](../../CLAUDE.md), [docs/ENGINEERING_RULES.md](../../docs/ENGINEERING_RULES.md).

## Repository layout
| Path | Contents |
|---|---|
| `docs/` | Architecture, roadmap, engineering rules, requirements, design reviews |
| `env/` | Environment report, dependencies, package snapshots |
| `ai/` | Agent instructions, prompts, workflows |
| `hardware/kicad/` | Real KiCad designs (version controlled) |
| `hardware/libraries/` | Project-local symbols, footprints, 3D models |
| `hardware/sandbox/` | Throwaway MCP experiments (gitignored) |
| `datasheets/`, `calculations/` | Sources and engineering math |
| `reports/` | ERC/DRC and validation reports |
| `manufacturing/`, `testing/`, `media/` | Fab outputs per revision, test evidence, images |

## Future capabilities
Requirements → component selection → schematic → footprints → placement → routing →
ERC/DRC → Gerber/BOM/CPL → fabrication → assembly → testing. See
[docs/DEVELOPMENT_ROADMAP.md](../../docs/DEVELOPMENT_ROADMAP.md).

## Current limitations
- Only sandbox test boards exist: V0.0.1 smoke test and the V0.0.2 LED test board
  ([capability matrix](../../reports/v0.0.2/MCP_CAPABILITY_MATRIX.md)). No real product design yet.
- Known MCP server defects and the required workarounds are listed in
  [FINAL_V0.0.2_REPORT.md](../../reports/v0.0.2/FINAL_V0.0.2_REPORT.md#defects-and-limitations) and
  [ai/AI_AGENT_INSTRUCTIONS.md](../../ai/AI_AGENT_INSTRUCTIONS.md).
- SWIG backend: KiCad must not have the edited file open and must reload after changes.
- IPC API, Freerouting, part sourcing and simulation are not configured.
- **No hardware has been designed, fabricated or tested.**

