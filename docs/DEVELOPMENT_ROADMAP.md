# Development Roadmap

Each phase has an exit criterion and ends with a user review before the next begins.

| Version | Phase | Exit criterion |
|---|---|---|
| **0.0.1** | Environment setup & MCP integration | Toolchain verified, MCP server built, one real MCP→KiCad round trip in sandbox, docs in place |
| 0.0.2 | MCP capability evaluation | Each core/schematic/board/DRC toolbox exercised in sandbox; known limitations documented; decide on IPC backend |
| 0.1.0 | Requirements | Approved `docs/requirements/` for the target board (function, power, interfaces, size, cost, manufacturer) |
| 0.2.0 | Component selection | Parts chosen with datasheets stored, key specs cited, availability checked |
| 0.3.0 | Symbols & footprints | Custom/library symbols and footprints verified against datasheets (review recorded) |
| 0.4.0 | Schematic | Complete schematic, calculations in `calculations/`, ERC clean or justified, schematic review |
| 0.5.0 | Board setup & placement | Manufacturer rules applied, outline, stack-up, placement reviewed (mechanical + thermal + power) |
| 0.6.0 | Routing & zones | Routed board, copper zones, DRC clean or justified, layout review |
| 0.7.0 | Manufacturing outputs | Gerber/drill/BOM/CPL generated and visually inspected, DFM review |
| 1.0.0 | Fabrication & assembly | Boards ordered (with explicit approval), received, assembled |
| 1.1.0 | Bring-up & testing | Test plan executed, measurements and photos recorded, issues logged |
| 1.2.0 | Documentation & publication | Public GitHub repository with sources, outputs and test evidence |

Optional integrations evaluated when a phase needs them: Freerouting (Java),
JLCPCB/LCSC parts data, Digi-Key API, LTspice/ngspice simulation, KiCad IPC API.
