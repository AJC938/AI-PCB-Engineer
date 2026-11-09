# Documentation Map

| Folder | Read this for |
|---|---|
| [getting-started/QUICK_START.md](getting-started/QUICK_START.md) | Find the KiCad files and manufacturing ZIPs in two minutes |
| [system-architecture/BOARD_ARCHITECTURE.md](system-architecture/BOARD_ARCHITECTURE.md) | Block diagram, power domains, signal conditioning |
| [electrical-design/ELECTRICAL_DESIGN.md](electrical-design/ELECTRICAL_DESIGN.md) | Circuit details, values, design decision record |
| [pinout/CONNECTION_GUIDE.md](pinout/CONNECTION_GUIDE.md) | Every connector pin, wiring diagram, GPIO map, power-up order |
| [pcb-layout/PCB_LAYOUT.md](pcb-layout/PCB_LAYOUT.md) | Board specifications, placement, zones |
| [manufacturing/HOW_TO_MANUFACTURE.md](manufacturing/HOW_TO_MANUFACTURE.md) | Ordering PCBs and assembly |
| [assembly/FULL_ASSEMBLY_REQUIREMENTS.md](assembly/FULL_ASSEMBLY_REQUIREMENTS.md) | Turnkey SMT + THT requirements |
| [safety/SAFETY_AND_POWER.md](safety/SAFETY_AND_POWER.md) | Supply requirements, protection limits |
| [validation/DIGITAL_VALIDATION.md](validation/DIGITAL_VALIDATION.md) | ERC/DRC/audit evidence |
| [validation/PHYSICAL_VALIDATION_STATUS.md](validation/PHYSICAL_VALIDATION_STATUS.md) | Physical status (not tested) and test plan |
| [visual-review/VISUAL_REVIEW.md](visual-review/VISUAL_REVIEW.md) | All renders and plots |
| [LICENSING.md](LICENSING.md) | Licence scope and third-party material |
| [ai-workflow/AI_TOOLCHAIN_SETUP.md](ai-workflow/AI_TOOLCHAIN_SETUP.md) | The Claude Code → MCP → KiCad toolchain |
| [requirements/v0.1.0/](requirements/v0.1.0/) | Original requirements, risk register, open questions |
| [ENGINEERING_RULES.md](ENGINEERING_RULES.md), [SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md), [DEVELOPMENT_ROADMAP.md](DEVELOPMENT_ROADMAP.md) | Project rules and toolchain architecture |

## Repository layout
| Path | Contents |
|---|---|
| `hardware/kicad/Sensor_Interface_Power_Board/` | **KiCad source** (schematic, PCB, project, project footprint library) and `build/` generator/verifier scripts |
| `manufacturing/Sensor_Interface_Power_Board/RevA/` | **Release Rev A**: fabrication, assembly, 3D, ZIP packages, checksums |
| `manufacturing/Sensor_Interface_Power_Board/manufacturer-profiles/` | Supplier candidate profiles (none confirmed) |
| `manufacturing/v0.2.0/` | Historical V0.2.0 package (kept unchanged) |
| `media/renders/` | KiCad-generated images |
| `reports/<version>/` | Design, audit and validation reports with evidence |
| `calculations/<version>/` | Engineering calculations (Python) with outputs |
| `datasheets/` | Datasheet indexes (links and revisions; PDFs are not redistributed) |
| `scripts/release/` | Release build, audit, packaging scripts |
| `release/v1.0.0/` | Release notes and checklist |
| `ai/`, `env/` | AI agent instructions, MCP harness, environment records |
| `testing/` | Physical test evidence (empty: not tested yet) |
