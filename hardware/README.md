# Hardware Sources

| Path | Contents |
|---|---|
| [`kicad/Sensor_Interface_Power_Board/`](kicad/Sensor_Interface_Power_Board/) | The board: `.kicad_pro`, `.kicad_sch`, `.kicad_pcb`, `fp-lib-table`, project footprint library `Sensor_Interface_Power_Board.pretty/` (U5, TI PWP0016A) |
| `kicad/Sensor_Interface_Power_Board/build/` | Scripts that generated and verified the design (schematic generator, placement plan, router, silkscreen, verifiers, BOM builder) |
| `libraries/` | Reserved for shared project libraries (currently empty; the only custom footprint lives with the project) |
| `sandbox/` | Throwaway MCP experiments (gitignored) |

**Requirements to open:** KiCad 10.0.x with its standard libraries. No absolute paths are used. Custom symbols:
none (all symbols are embedded in the schematic). Custom 3D models: none (U5 uses the KiCad HTSSOP-16 model).

The KiCad project folder stays at `hardware/kicad/` (rather than being moved) so that the build scripts, report
links and git history remain valid.
