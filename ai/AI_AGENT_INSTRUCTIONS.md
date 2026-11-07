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
