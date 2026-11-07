# System Architecture

## Layered view

```
Claude Code (agent, runs in the Claude desktop app)
   │  reads project-scoped .mcp.json (local, gitignored)
   ▼
MCP protocol — JSON-RPC 2.0 over stdio
   ▼
KiCad MCP Server v2.8.3  (TypeScript, dist/index.js)
   │  tool registry, toolboxes (core = 37 tools), input validation (zod)
   ▼
Node.js 24.22.2 LTS  (portable, %USERPROFILE%\dev\tools\node-v24.22.2)
   │  spawns a long-lived Python worker; JSON commands over its stdin/stdout
   ▼
Python bridge  (python/kicad_interface.py + commands/*)
   │  runs on KiCad's bundled interpreter (KICAD_PYTHON)
   ▼
KiCad Python APIs
   ├── pcbnew (SWIG)  — in-process board load/edit/save          ← active backend
   ├── kicad-skip / sexpdata — direct .kicad_sch S-expression edits
   └── kipy (kicad-python) — IPC API client to a running KiCad   ← installed, not used yet
   ▼
KiCad 10.0.8  (files on disk: .kicad_pro / .kicad_sch / .kicad_pcb)
   └── kicad-cli — independent ERC/DRC/export used for verification
```

## Backends: pcbnew, kipy and the IPC API

| | pcbnew (SWIG) | kipy → IPC API |
|---|---|---|
| What it is | KiCad's legacy Python bindings, loaded *inside* the Python process | Official client library that talks to a **running** KiCad over a local socket (protobuf/NNG) |
| Needs KiCad GUI running | No | Yes, with *Preferences → Plugins → Enable IPC API server* |
| Edits | Files on disk; KiCad must reload to see them | Live objects in the open editor (real-time) |
| Status upstream | Deprecated long-term, still shipped in KiCad 10 | KiCad's supported path going forward |
| Here | **Active** (`KICAD_BACKEND=swig`) | Installed (`kicad-python 0.8.0`), IPC server disabled — evaluated in a later version |

Schematic tools do not use pcbnew; they edit `.kicad_sch` files through
kicad-skip/sexpdata and KiCad's own library tables.

## Data and safety boundaries
- The server runs with the user's permissions and can write anywhere the user can.
  Project policy (`CLAUDE.md`, `ai/AI_AGENT_INSTRUCTIONS.md`) restricts writes to this
  repository, and experiments to `hardware/sandbox/`.
- Before writing a board the server saves a copy in `<project>/.mcp-backups/` (gitignored).
- Server logs: `%USERPROFILE%\.kicad-mcp\logs\` (outside the repo).
- With the SWIG backend, never edit a file that is open in KiCad — KiCad will not
  see the change and may overwrite it on save.
- Verification is independent of the MCP server: `kicad-cli` ERC/DRC/exports.

## Configuration
`.mcp.json` (local) — template: `.mcp.example.json`

| Variable | Value | Purpose (from server source/README) |
|---|---|---|
| `KICAD_PYTHON` | `%LOCALAPPDATA%\Programs\KiCad\10.0\bin\python.exe` | Interpreter for the Python worker |
| `PYTHONPATH` | `%LOCALAPPDATA%\Programs\KiCad\10.0\bin\Lib\site-packages` | Location of `pcbnew` on KiCad 10 Windows |
| `KICAD_BACKEND` | `swig` | `auto` / `ipc` / `swig` |
| `KICAD_MCP_TOOLBOXES` | `core` | Start with 37 core tools; others opened on demand |
| `LOG_LEVEL` | `info` | `error`/`warn`/`info`/`debug` |
