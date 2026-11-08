# Changelog

All notable changes to this project are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning: SemVer.

## [Unreleased] — 0.1.0 Phase 1: Requirements & design planning (branch `design/v0.1.0-phase1`)
- Product: Sensor Interface & Power Management Board for ESP32 (planning only. No schematic, PCB, MPN or order).
- `docs/requirements/v0.1.0/`: design brief, 52 requirements, block diagrams, interface spec, power budget
  (Arch. A 774 mA / Arch. B 274 mA), 22 risks, component selection plan, verification plan, 18 open
  questions, Phase 1 summary.
- `calculations/v0.1.0/phase1_calcs.py`: ESP32 thresholds, Echo divider window, trigger margin, power budget,
  LDO vs buck, reverse-polarity drop, I2C pull-up limits. Every input tagged VERIFIED/SECONDARY/ASSUMED.
- `datasheets/index_v0.1.0.md`: Espressif ESP32 DS v5.3, WROOM-32E DS v2.1, DevKitC V4 guide, NXP UM10204 Rev 7.0.
  HC-SR04 data is secondary only.
- Status: ready for review. **Not ready for design freeze** (13 blocking open questions).

## [0.0.3-rc1] — 2026-11-08 — MCP advanced capability evaluation (branch `evaluation/v0.0.3-mcp-capabilities`)

### Added
- Reports in `reports/v0.0.3/`: IPC, custom symbol, custom footprint, GUI driver, SWIG vs IPC, capability
  matrix, test log, evidence index, next-stage recommendation, final report. Sanitized evidence.
- `ai/workflows/mcp_harness.py` (reproducible MCP stdio test client). Test generators and readers in `reports/v0.0.3/tests/`.
- MCP workflow rules 10–14 in `ai/AI_AGENT_INSTRUCTIONS.md`.

### Results
- SWIG 12/12 PASS. IPC tested and not usable (kicad-python 0.8.0 vs KiCad 10.0.8, silent wrong reads).
- Custom symbol creation PASS (native MCP). Custom footprint creation PASS with limitations.
- GUI driver not usable on Windows (install path, unprocessed clicks, screenshot privacy). GUI DRC BLOCKED.
- New defects D-10 to D-22. KiCad global config restored byte-identical after the temporary, approved changes.

## [0.0.2] — 2026-11-07 — MCP capability evaluation

### Added
- LED indicator test board (5 V, 620 Ω, red 5 mm LED, Phoenix terminal): schematic, PCB 50×30 mm
  two-layer, routing, GND zone, fab outputs. Built in `hardware/sandbox/v0.0.2-led-test/`,
  snapshot and outputs in `reports/v0.0.2/evidence/`.
- Datasheet index (`datasheets/index.md`) and circuit calculations (`calculations/v0.0.2/`).
- Ten evaluation reports in `reports/v0.0.2/`, including the capability matrix and the final report.
- `ai/workflows/sync_footprint_fields.py` (non-MCP field-copy workaround) and
  `ai/workflows/inspect_fab_outputs.py` (independent Gerber/drill/BOM/CPL inspection).
- MCP workflow rules in `ai/AI_AGENT_INSTRUCTIONS.md`.

### Verified
- ERC 0, DRC 0 errors / 0 warnings, 0 unconnected, schematic parity 0 (kicad-cli). MCP and CLI agree.
- 56 MCP tools invoked: 48 PASS, 7 WARNING, 1 FAILED (`add_mounting_hole`).

### Known issues (KiCAD-MCP-Server v2.8.3)
- D-1 save desync after sync/refill. D-2 net-name prefix lost. D-3 fields not synced.
  D-4 invalid mounting-hole lib ID. D-5 PCB BOM ignores exclusions/attributes. D-6 no parity in `run_drc`.
- Design warning: no reverse-polarity protection (LED VR 5 V).
- Digital validation only. No hardware built or tested.

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
