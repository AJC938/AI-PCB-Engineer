# Sensor Interface PCB — Rev A — Fabrication Package (bare board)

Sensor Interface & Power Management Board for ESP32, release v1.0.0, board revision **A**.
**Fabrication-ready digital design. NOT yet fabricated or physically tested.**

Contents: Gerber X2 layers (9) + Gerber job file, Excellon drill files (PTH and NPTH, metric) with drill maps,
IPC-D-356 netlist for electrical test, FABRICATION_NOTES.md (stack-up, layer map, drill table, critical notes).

Quick order parameters: 2 layers · FR-4 · 1.6 mm · 1 oz copper · 90.0 × 64.0 mm · ENIG preferred (lead-free HASL
acceptable) · solder mask both sides · white silkscreen top only · flying-probe test with the .d356 file.

Origin of all coordinates: board bottom-left corner, mm. Read FABRICATION_NOTES.md §6 before accepting any
manufacturer DFM change (the U5 exposed pad must stay isolated from GND).
Source and documentation: the AI-PCB-Engineer repository, `hardware/kicad/Sensor_Interface_Power_Board/`.
Licence: CERN-OHL-S-2.0 (see LICENSE-HARDWARE in the repository).
