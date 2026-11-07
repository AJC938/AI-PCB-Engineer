# Manufacturing Export Report — V0.0.2

**Test outputs only. Nothing was uploaded, quoted or ordered.**
Files: [`evidence/fab/`](evidence/fab/). Independent parse: [`evidence/checks/fab_inspection.txt`](evidence/checks/fab_inspection.txt),
produced by [`ai/workflows/inspect_fab_outputs.py`](../../ai/workflows/inspect_fab_outputs.py) (no KiCad, no MCP).

## Generated files (all via MCP)
| Output | Tool | Files |
|---|---|---|
| Gerber (X2, Protel ext., soldermask subtracted from silk) | export_gerbers | F_Cu.gtl, B_Cu.gbl, F_Mask.gts, B_Mask.gbs, F_Silkscreen.gto, B_Silkscreen.gbo, Edge_Cuts.gm1, job.gbrjob |
| Drill (Excellon, mm, separate PTH/NPTH, PDF map) | export_drill | PTH.drl, NPTH.drl, PTH-drl_map.pdf, NPTH-drl_map.pdf |
| BOM from schematic | export_sch_bom | led_test-bom.csv |
| BOM from PCB | export_bom | led_test-bom-from-pcb.csv (for comparison, see D-5) |
| CPL (CSV, mm, both sides) | export_pos | led_test-cpl.csv |
| PCB PDF (F.Cu, B.Cu, F.SilkS, F.Fab + Edge) | export_pcb_pdf | led_test-pcb.pdf (4 pages) |
| Schematic PDF | export_sch_pdf | led_test-schematic.pdf (1 page) |
| 3D | export_3d | led_test.step (848 KB, kept in the sandbox, not committed) |

No paste layers were exported because the board is all THT.

## Inspection results
| Check | Expected | Found | Result |
|---|---|---|---|
| Board outline | 50 × 30 mm | Edge.Cuts 100.000–150.000 × 100.000–130.000 mm (`Profile,NP`) | PASS |
| Copper layers | 2 | `Copper,L1,Top` / `Copper,L2,Bot`. Job: `LayerNumber 2`, 1.6 mm | PASS |
| Pad flashes | 6 per side at the designed coordinates | 6 per side. J1 (105.60,112.46) roundrect 2.6 / (105.60,117.54) Ø2.6. R1 (115.00,110.00), (125.16,110.00) Ø1.6. D1 (135.00,115.00) Ø1.8, (135.00,117.54) square 1.8 | PASS |
| Net attributes | +5V, GND, LED_A | `TO.N` on both copper layers: +5V, GND, LED_A | PASS |
| PTH drills | 0.8 ×2, 0.9 ×2, 1.3 ×2 | T1 0.800 ×2, T2 0.900 ×2, T3 1.300 ×2 (METRIC) | PASS |
| NPTH drills | 3.2 ×4 | T1 3.200 ×4 | PASS |
| Drill map | readable | PDF lists 0.8 / 0.9 / 1.3 mm, 2 holes each | PASS |
| BOM (schematic) | 3 lines with value, footprint, manufacturer, MPN, qty | D1 Red WP7113ID Kingbright. J1 5V_IN 1715721 Phoenix Contact. R1 620 MFR-25FBF52-620R Yageo. Qty 1 each | PASS |
| BOM (PCB, MCP `export_bom`) | same 3 parts | 7 rows (includes H1–H4 despite `exclude_from_bom`). No MPN/Manufacturer despite `includeAttributes` | **WARNING (D-5)**: do not use for ordering |
| CPL | R1, D1, J1 only | D1 (135.000, −117.540, 90°). J1 (105.600, −112.460, −90°). R1 (115.000, −110.000, 0°). Holes excluded | PASS: matches the board (KiCad convention: Y negated) |
| Schematic PDF | 1 page, KiCad 10.0.8 title block | 1 page | PASS |
| STEP | board + component bodies | 848 KB, contains the component model references | PASS (not opened in a MCAD tool: NOT TESTED) |

## Not done (by design)
- No fab-specific output profile (e.g. JLCPCB layer naming or CPL rotation offsets). A manufacturer has not been chosen.
- Gerbers were parsed and checked numerically, not opened in an external Gerber viewer.
- No upload, quotation or order.
