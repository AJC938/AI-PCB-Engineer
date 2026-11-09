# Fabrication notes — Sensor Interface & Power Management Board, Rev 0.2.0

**Status: DIGITAL RELEASE CANDIDATE — not ordered, not approved for a specific manufacturer.**

| Item | Requirement |
|---|---|
| Board | 90.0 × 64.0 mm rectangle, outline on `Edge_Cuts.gm1`, tolerance ±0.2 mm |
| Layers | 2 copper (L1 = top `F_Cu.gtl`, L2 = bottom `B_Cu.gbl`) |
| Stack-up | FR-4, Tg ≥ 130 °C, finished thickness 1.6 mm ±10 %, 1 oz (35 µm) finished copper both sides (job file `-job.gbrjob`) |
| Surface finish | ENIG preferred; lead-free HASL acceptable (0.65 mm pitch HTSSOP with exposed pad U5) |
| Solder mask | Green both sides, LPI; mask-defined opening on U5 exposed pad 3.3 × 3.3 mm |
| Silkscreen | White, top only (bottom silkscreen file is empty); min text 1.0 mm, stroke 0.15 mm |
| Min track / space | 0.25 mm / 0.20 mm (rule minimum 0.20 / 0.20) |
| Vias | 0.6 mm pad / 0.3 mm finished drill, 57 vias, tented not required (not in pads) |
| Holes | PTH: 0.3 (57), 0.9 (4), 1.0 (28), 1.3 (2) mm; NPTH: 3.2 mm (4 mounting holes) — `PTH.drl`, `NPTH.drl` (Excellon, mm) |
| Copper to edge | ≥ 0.5 mm |
| Impedance control | **None required** (all signals ≤ 1 MHz class; no controlled-impedance nets) |
| Electrical test | Flying probe against `Sensor_Interface_Power_Board_v0.2.0.d356` (IPC-D-356) |
| Origin | All Gerber/drill/CPL coordinates use the board's bottom-left corner as (0, 0) |
| Panelization | Not required by the design; if the factory panelizes, keep ≥ 0.5 mm from copper to any V-score/tab |
| Markings | No UL/date marking required; the factory may add its order number only outside copper features |

## Critical notes
- Zones are stored filled in the design; regenerate Gerbers only with KiCad 10.0.8 and run DRC with
  `--refill-zones` first (MCP defect D-10).
- The +3V3_P copper area around U1 (≥ 194 mm² required, 251 mm² drawn) is a thermal requirement — do not reduce.
- RTN copper island under/below U5 must stay isolated from GND (TI SLVSDG2G §10.4).
