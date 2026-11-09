# Changelog

All notable changes to this project are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning: SemVer.

## [1.0.0] — 2026-11-09 — Fabrication-ready open hardware design release, board Rev A (V0.3.0 finalization, branch `release/v0.3.0-finalization`)
**Status: DIGITALLY VALIDATED DESIGN — NOT PHYSICALLY FABRICATED OR TESTED.**

### Audited
- Final engineering audit (`reports/v0.3.0/FINAL_ENGINEERING_AUDIT.md`):
  - TPS26600 pin-by-pin against SLVSDG2G Rev. G;
  - reverse-polarity path tracing, including the earth-referenced ground-loop limitation;
  - LDO thermal re-derived from the board read-back (Tj ≈ 94.7 °C at 50 °C; new +3V3_P rating 250 mA at ≤ 50 °C);
  - signals, connectors, footprints, portability.
- No electrical or layout correction was required.
- BOM sourcing re-checked on 2026-11-09: TPS26600PWPR active, but TI store out of stock and DigiKey 0 in stock with a 26-week lead time.

### Changed
- DDR-22: board revision label Rev A (title blocks, silkscreen "REV A v1.0"). Copper, drills, BOM and CPL are identical to V0.2.0.
- README rewritten for the hardware. The former toolchain README moved to `docs/ai-workflow/AI_TOOLCHAIN_SETUP.md`.

### Added
- `manufacturing/Sensor_Interface_Power_Board/RevA/`:
  - regenerated Gerber X2, Excellon, IPC-D-356, BOM (with sourcing columns), CPL, drawings, STEP;
  - three tested ZIP packages and SHA-256 checksums;
  - reviewed manufacturer profiles.
- `scripts/release/`: build, audit (19 checks), BOM enrichment, packaging, path sanitizer and revision scripts.
- `docs/`: quick start, architecture, electrical design, connection guide, layout, manufacturing, assembly, safety, validation status, visual review, licensing.
- `media/renders/`: KiCad-generated 3D and 2D images.
- `CONTRIBUTING.md`, `release/v1.0.0/` notes and checklist. (The release candidate `v1.0.0-rc1` carried a
  CERN-OHL-S-2.0 draft licence; it was superseded before the stable release, see Licensing.)
- `.gitattributes`: release folder byte-exact, so the published checksums match on every platform.

### Licensing (final, owner-approved 2026-11-09)
- Hardware: **CERN-OHL-P-2.0**. `LICENSE-HARDWARE` is the official OHWR text, byte-identical.
- Software: **MIT**. `LICENSE-CODE` is the OSI text.
- Added `LICENSE_SCOPE.md` (file and directory scope map, decision for hardware-generating code), `REUSE.toml` and
  `LICENSES/`, `NOTICE.md`, `MODIFICATIONS.md` (CERN-OHL-P §3.3 modification notices), `THIRD_PARTY_NOTICES.md`,
  `docs/licensing/`.
- Third-party audit: the U5 project footprint is derived from a KiCad library footprint and stays under
  `CC-BY-SA-4.0 WITH KiCad-libraries-exception`. No datasheet PDF is redistributed.
- Manufacturing ZIPs now include `NOTICE.md` and `LICENSE-HARDWARE.txt`. Engineering files are byte-identical to `v1.0.0-rc1`.
- `scripts/release/audit_licensing.py` (9 checks).

### Validation
ERC 0. DRC 0/0 with zone refill and parity. Verifier PASS. Package audit 19/19. ZIP tests PASS. `sha256sum -c` 28/28. Fresh MCP reopen 7/7.

## [Unreleased] — 0.2.0 PCB layout, DFM/DFA and manufacturing package (branch `design/v0.2.0-pcb-layout`)
- Gate A: TVS/LDO analysis showed that SMAJ6.0A (VBR ≥ 6.67 V) cannot protect the TLV1117LV (6 V abs max).
  F1/Q1/R1/D1 were replaced by a TPS26600 eFuse: OVP 5.39–5.82 V worst case, reverse polarity −60 V, 0.6 A
  limit, inrush control. TRIG series 1 kΩ (R15) added. LDO thermal re-derived for a 2-layer board
  (251 mm² copper, Tj ≈ 94.7 °C at 50 °C).
- Gate B: PCBWay, NextPCB, Seeed Fusion and Eurocircuits compared from official pages. PCBWay is the provisional
  recommendation and NextPCB the alternate. Supplier approval is pending. BOM sourcing audit done
  (TPS26600PWPR stock risk).
- Gate C: footprint verification. Project footprint for TI PWP0016A.
- Layout: 90 × 64 mm, 2 layers, top-side assembly, 331 tracks, 57 vias, 4 zones. kicad-cli DRC (all
  severities, parity, refilled and stored zones): 0 violations, 0 unconnected, 0 parity. ERC 0.
- `manufacturing/v0.2.0/`: Gerber X2, Excellon, IPC-D-356, BOM, CPL, assembly drawings, STEP, notes, DFM
  profiles. Independent audit 11/11 PASS.
- New MCP findings D-23 (add_zone unsupported) and D-24 (NC pad nets); workarounds added to AI_AGENT_INSTRUCTIONS.
- Status: digital design complete. **NOT fabricated, NOT TESTED. Supplier approval pending.**

## [Unreleased] — 0.1.0 Engineering design, component selection & schematic (branch `design/v0.1.0-phase1`)
- Architecture B selected (DevKit on its own USB. The board powers peripherals only). Variant-independent ultrasonic
  interface (SN74LVC1T45 TRIG, SN74LVC1G17 ECHO/RX, logic referenced to 3V3_ESP).
- `calculations/v0.1.0/design_calcs.py` + `independent_checks.py` (Monte Carlo, 10/10 PASS).
- `datasheets/v0.1.0/DATASHEET_INDEX.md`: DS-01…DS-16 official sources with revisions.
- `hardware/kicad/Sensor_Interface_Power_Board/`: complete A3 schematic built via KiCAD-MCP-Server (SWIG),
  48 BOM parts with MPNs. ERC 0 (MCP and kicad-cli, no exclusions). Netlist verified by `build/verify_schematic.py`.
- `reports/v0.1.0/`: 13 design reports + sanitized validation evidence.
- Phase 1 docs: status pointer in OPEN_QUESTIONS. Risks R-30…R-35 added.
- `.gitignore`: re-include `hardware/kicad/*/build/` (schematic generator scripts are design sources).
- Status: schematic complete and digitally validated. **NOT TESTED physically. Not production-ready.**

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
