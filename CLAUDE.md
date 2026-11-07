# CLAUDE.md — AI-PCB-Engineer

Instructions for every Claude Code session in this repository. Read this file,
`docs/ENGINEERING_RULES.md` and `ai/AI_AGENT_INSTRUCTIONS.md` before changing anything.

## What this project is
An AI-assisted PCB engineering workflow (Claude Code → MCP → KiCad 10) whose real
deliverable is a manufactured, assembled and physically tested PCB. The AI tooling
is a means, not the product.

## Before making changes
1. Understand the current state: read `README.md`, `CHANGELOG.md`, and the
   relevant files under `docs/` and `hardware/`.
2. State what you intend to change and why. Large or irreversible steps need
   the user's approval first.
3. Check that the KiCad file you will touch is **not open in KiCad**
   (look for a `~*.lck` / `*.lck` file next to it). Never edit an open project.

## Hard rules
- Follow `docs/ENGINEERING_RULES.md`. ERC/DRC passing does not mean the design is correct.
- **Datasheets are the authority** for component specifications. Never invent
  pinouts, ratings, dimensions or part numbers. If a value is not verified,
  mark it `UNVERIFIED` and say so.
- Never claim physical functionality, successful fabrication, or a passed test
  without recorded evidence in `testing/`.
- Work only inside this repository. MCP experiments go in `hardware/sandbox/`.
  Do not modify global KiCad libraries or the user's personal libraries
  (e.g. `Buzzer_a1`) or any project outside this repository.
- Preserve previous revisions: commit before each MCP editing session, never
  overwrite a released revision under `manufacturing/<rev>/`, bump the revision instead.
- Record design decisions with their source (datasheet page, calculation file,
  or user decision) so every choice is traceable.
- Never expose secrets. Credentials live only in local `.env` files.
- No pushes, public uploads, manufacturer submissions or purchases without
  explicit user approval for that specific action.

## Evidence labels used in reports
`VERIFIED (datasheet/measurement)` · `CALCULATED` · `TOOL-CHECKED (ERC/DRC)` ·
`ASSUMED` · `NOT TESTED`

## Environment quick reference
- KiCad 10.0.8, bundled Python 3.11 (`%LOCALAPPDATA%\Programs\KiCad\10.0\bin\python.exe`)
- `kicad-cli` is not on PATH; call it by full path.
- MCP server: `%USERPROFILE%\dev\tools\KiCAD-MCP-Server` (v2.8.3, stable), configured in
  the local `.mcp.json` (gitignored; template in `.mcp.example.json`).
- Initial MCP toolbox: `core`. Open further toolboxes only when a task needs them.
