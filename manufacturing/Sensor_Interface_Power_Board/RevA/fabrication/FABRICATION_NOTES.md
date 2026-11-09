# Fabrication Notes — Sensor Interface & Power Management Board, Rev A (release v1.0.0)

**Status: fabrication-ready digital design. NOT yet fabricated, NOT physically tested.**
These notes are manufacturer-independent. Supplier-specific instructions are in
`manufacturing/Sensor_Interface_Power_Board/manufacturer-profiles/` and are not part of this standard data.

Generated with KiCad 10.0.8 (`kicad-cli`) from `hardware/kicad/Sensor_Interface_Power_Board/` by
`scripts/release/build_release.sh`. Independent audit: `reports/v0.3.0/evidence/validation/release_audit.txt`.

## 1. Board summary
| Item | Requirement |
|---|---|
| Outline | Rectangle **90.0 × 64.0 mm**, square corners. Outline on `Edge_Cuts.gm1`. Tolerance ±0.2 mm |
| Layers | 2 copper layers (rigid, double-sided, plated through-holes) |
| Base material | FR-4, Tg ≥ 130 °C (standard FR-4 is acceptable) |
| Finished thickness | 1.6 mm ±10 % |
| Copper | 1 oz (35 µm) finished, both outer layers |
| Surface finish | **ENIG preferred** (0.65 mm pitch HTSSOP with exposed pad, U5). Lead-free HASL acceptable |
| Solder mask | Both sides, LPI, green preferred (colour is not functional) |
| Silkscreen | Top only, white preferred. The bottom silkscreen file is intentionally empty |
| Impedance control | None required |
| Electrical test | Flying-probe (or fixture) test against `Sensor_Interface_Power_Board_RevA.d356` (IPC-D-356) |
| Quantity / panel | Set by the orderer. No panel is required by the design; if the factory panelizes, keep ≥ 0.5 mm from copper to any V-score or tab |
| Markings | The factory may add an order number only where it does not overlap copper features or the silkscreen legend |

> Note: the Gerber job file lists `"Finish": "None"` because no finish is set in the KiCad stack-up. **This
> document governs the surface finish (ENIG preferred).**

## 2. Layer map (Gerber X2, coordinates in mm, format 4.6, origin = board bottom-left corner)
| Order | File | Layer | X2 FileFunction |
|---|---|---|---|
| 1 | `Sensor_Interface_Power_Board-F_Silkscreen.gto` | Top silkscreen | Legend,Top |
| 2 | `Sensor_Interface_Power_Board-F_Paste.gtp` | Top paste (stencil) | Paste,Top |
| 3 | `Sensor_Interface_Power_Board-F_Mask.gts` | Top solder mask | Soldermask,Top |
| 4 | `Sensor_Interface_Power_Board-F_Cu.gtl` | **L1 top copper** | Copper,L1,Top |
| 5 | `Sensor_Interface_Power_Board-B_Cu.gbl` | **L2 bottom copper** | Copper,L2,Bot |
| 6 | `Sensor_Interface_Power_Board-B_Mask.gbs` | Bottom solder mask | Soldermask,Bot |
| 7 | `Sensor_Interface_Power_Board-B_Paste.gbp` | Bottom paste (empty, no bottom components) | Paste,Bot |
| 8 | `Sensor_Interface_Power_Board-B_Silkscreen.gbo` | Bottom silkscreen (empty) | Legend,Bot |
| — | `Sensor_Interface_Power_Board-Edge_Cuts.gm1` | Board outline | Profile |
| — | `Sensor_Interface_Power_Board-job.gbrjob` | Gerber job file (stack-up, layer list) | — |

## 3. Stack-up (from the Gerber job file)
| Layer | Material | Thickness |
|---|---|---|
| Top solder mask | LPI | 0.01 mm |
| F.Cu | Copper | 0.035 mm |
| Core | FR-4 | 1.51 mm |
| B.Cu | Copper | 0.035 mm |
| Bottom solder mask | LPI | 0.01 mm |
| **Total** | | **1.60 mm** |

## 4. Drilling (Excellon, metric, decimal format, absolute, origin = board bottom-left)
| File | Diameter (finished) | Count | Use |
|---|---|---|---|
| `-PTH.drl` | 0.30 mm | 57 | Vias (0.6 mm pad) |
| `-PTH.drl` | 0.90 mm | 4 | LED1, LED2 leads |
| `-PTH.drl` | 1.00 mm | 28 | 2.54 mm pin headers J2–J6 |
| `-PTH.drl` | 1.30 mm | 2 | Terminal block J1 |
| `-NPTH.drl` | 3.20 mm | 4 | M3 mounting holes H1–H4 (non-plated) |

Drill drawings: `-PTH-drl_map.pdf`, `-NPTH-drl_map.pdf`. Hole tolerance: standard fabrication tolerance
(±0.08 mm typical) is acceptable. No slots, no castellations, no blind/buried vias, no back-drilling.

## 5. Design rules used (minimums in the design)
| Rule | Value |
|---|---|
| Track width | 0.25 mm minimum (signal); 0.3 / 0.4 / 0.5 mm power |
| Clearance | 0.20 mm (copper to copper); 0.30 mm zone clearance |
| Via | 0.6 mm pad / 0.3 mm drill |
| Annular ring | ≥ 0.15 mm |
| Copper to board edge | ≥ 0.5 mm |
| Silkscreen | min text height 1.0 mm, stroke 0.15 mm |

All are within the capability tables of common prototype manufacturers. Confirm against the chosen factory's
own DFM check.

## 6. Critical notes (do not change without an engineering review)
1. **U5 exposed pad (TPS26600) is NOT ground.** It sits on an isolated `EF_RTN` copper island. It must stay isolated
   from the GND plane (TI SLVSDG2G, Layout Guidelines). Do not let a "DFM fix" merge it into GND.
2. **+3V3_P thermal copper** around U1 (251 mm² solid top copper on the tab) is a thermal requirement
   (≥ 194 mm²). Do not reduce or hatch it.
3. Solder jumpers JP1 (pads 1–2) and JP2 are **bridged in copper** by design. They are not open pads.
4. Zones are stored filled. If Gerbers are regenerated, use KiCad 10.0.8 and run DRC with zone refill first.
5. Fiducials FID1–FID3: 1.0 mm copper with a 2.0 mm mask opening. Keep them free of silkscreen.
