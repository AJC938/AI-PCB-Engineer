# Quick Start

**Sensor Interface & Power Management Board, Rev A (release v1.0.0).**
**Fabrication-ready digital design. NOT physically fabricated or tested.**

## I want to manufacture it
1. Download the ZIPs from [`manufacturing/Sensor_Interface_Power_Board/RevA/packages/`](../../manufacturing/Sensor_Interface_Power_Board/RevA/packages/):
   - `Sensor_Interface_PCB_RevA_Fabrication.zip`: bare PCB (Gerber X2, Excellon, IPC-D-356, notes)
   - `Sensor_Interface_PCB_RevA_Assembly.zip`: BOM, CPL, assembly drawings, notes
   - `Sensor_Interface_PCB_RevA_Complete_Manufacturing.zip`: everything, for a fabrication + assembly quote
2. Verify them: `sha256sum -c` against [`RevA/checksums/SHA256SUMS.txt`](../../manufacturing/Sensor_Interface_Power_Board/RevA/checksums/SHA256SUMS.txt)
   (run from the `RevA` folder).
3. Follow [HOW_TO_MANUFACTURE.md](../manufacturing/HOW_TO_MANUFACTURE.md).

## I want to open the design
1. Install **KiCad 10.0.x** (the files were saved by 10.0.8; KiCad 9 cannot open them).
2. Clone or download this repository.
3. Open `hardware/kicad/Sensor_Interface_Power_Board/Sensor_Interface_Power_Board.kicad_pro`.
   - The U5 footprint is in the project library `Sensor_Interface_Power_Board.pretty` (loaded through `${KIPRJMOD}`).
   - All other footprints and 3D models come from the standard KiCad 10 libraries.
   - Symbols are embedded in the schematic.
4. Optional: rebuild every output and re-run every check with `scripts/release/build_release.sh` (needs Bash and KiCad 10).

## I want to wire it up
Read [CONNECTION_GUIDE.md](../pinout/CONNECTION_GUIDE.md) and [SAFETY_AND_POWER.md](../safety/SAFETY_AND_POWER.md) first.
In short: 5 V into J1 (pin 1 = +). ESP32 DevKit on its own USB, wired to J2 by pin labels (12 wires, **not** the
DevKit 5V pin). Power the board first, then connect the ESP32 USB.
