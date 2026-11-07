# Project Scope

## Overall goal
Design, manufacture, assemble and physically test a real, functional PCB using
an AI-assisted engineering workflow built on Claude Code, the Model Context
Protocol (MCP) and KiCad 10. The final public repository showcases the PCB
project itself: original KiCad sources, schematics, BOM, manufacturing outputs,
documentation and physical test evidence.

## V0.0.1 — Environment Setup & MCP Integration (this release)
Included:
- Verified local toolchain (KiCad 10.0.8, KiCad bundled Python, Node.js LTS, Git, Claude Code).
- KiCAD-MCP-Server v2.8.3 installed from the `stable` branch, built and validated.
- Project-scoped MCP configuration for Claude Code (local only, gitignored).
- Workspace structure, engineering rules, agent instructions and documentation.
- An isolated sandbox smoke test proving at least one real MCP → KiCad round trip.

Explicitly out of scope for V0.0.1:
- Designing the production PCB or selecting its components.
- KiCad IPC API backend (deferred; SWIG/pcbnew backend is used first).
- Freerouting, JLCPCB/LCSC database download, Digi-Key API, LTspice.
- Publishing to GitHub, contacting manufacturers, ordering parts or boards.

## Long-term capabilities (later versions)
Requirements analysis → component research → datasheet verification → schematic
→ custom symbols → footprint verification → board setup → placement → routing →
copper zones → ERC/DRC → Gerber/drill/BOM/CPL → design review → fabrication →
assembly → physical test and documentation. See `docs/DEVELOPMENT_ROADMAP.md`.

## Constraints
- Native Windows 11 workflow; WSL2 is a fallback only.
- Every engineering claim must be traceable to a datasheet, calculation, tool
  output or measurement (see `docs/ENGINEERING_RULES.md`).
