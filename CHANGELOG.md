# Changelog

All notable changes to this project are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning: SemVer.

## [Unreleased] — 0.0.2 MCP capability evaluation
- In progress: complete LED test board (schematic → ERC → netlist → PCB → routing →
  DRC → fabrication outputs) in `hardware/sandbox/v0.0.2-led-test/`.

## [0.0.1] — 2026-11-07 — Initial environment setup

### Verified after release (2026-11-07)
- MCP connection verified **inside Claude Code**: `kicad` server connected after the user
  approved it, backend `swig`, 37 core tools exposed, `get_backend_state`,
  `check_kicad_ui`, `is_dirty`, `list_toolboxes`, `search_tools` all succeeded (read-only).
- Non-blocking inconsistency: the bundled CLI `claude mcp get kicad` still reports
  "Pending approval" although the desktop session has the server approved and connected.

### Added
- Workspace structure for docs, environment, AI instructions, hardware, datasheets,
  calculations, reports, manufacturing, testing and media.
- `CLAUDE.md`, `ai/AI_AGENT_INSTRUCTIONS.md`, `docs/ENGINEERING_RULES.md`,
  `docs/SYSTEM_ARCHITECTURE.md`, `docs/DEVELOPMENT_ROADMAP.md`, `PROJECT_SCOPE.md`.
- `env/ENVIRONMENT_REPORT.md`, `env/DEPENDENCIES.md`, package snapshots.
- KiCAD-MCP-Server v2.8.3 (`stable`, `1d204fe3`) installed outside the repo, built
  with Node 24.22.2 LTS.
- MCP Python dependencies installed into KiCad 10.0.8's bundled Python.
- Project-scoped MCP config (`.mcp.json`, local only) and `.mcp.example.json` template.
- Sandbox smoke test with sanitized evidence in `reports/v0.0.1/`, `reports/drc/`, `reports/erc/`.

### Decided
- KiCad 10.0.8 instead of 9.0. SWIG backend first, IPC deferred.
- Node 24 LTS (portable) for the MCP runtime. The system Node 25 is end-of-life and is not used.

### Known issues
- ~~Project MCP server needs one-time approval in Claude Code.~~ Approved and verified.
- Cosmetic "No KiCAD installations found" log warning from the upstream server on KiCad 10.
