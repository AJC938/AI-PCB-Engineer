# Routing Review — V0.2.0

## Method (reproducible)
1. **Geometry computed** by `build/route_pcb.py`: an A* grid router on a 0.1 mm grid with 8 directions over 2 layers.
   It uses the exact pad, track and via shapes of all other nets (clearance 0.24 mm in the router, 0.20 mm DRC rule),
   0.55 mm to the edge, vias 0.6/0.3 mm, and no vias in SMD pads. Zone areas are keep-outs for other nets, and THT
   GND pads keep a spoke ring. Bottom-layer cost is ×2.5 so the GND plane stays whole. Freerouting was not used
   (not pre-approved).
2. **Copper written** only through MCP: `route_trace` (331 segments) and `add_via` (57), 390/390 calls OK. Zones
   used `add_copper_pour` (4) because `add_zone` returns "Unknown command" (new defect D-23).
3. **Checked** by KiCad itself (`kicad-cli pcb drc --severity-all --schematic-parity --refill-zones`).

## Iterations (failures were fixed, not hidden)
| Pass | Result | Root cause | Fix |
|---|---|---|---|
| 1 | 6 failures (EF_OVP R18, TRIG U3.3, 4 GND escapes) | RTN keep-out covered the R18 OVP pad; thermal keep-out blocked C3/C4 GND vias; routing order trapped pins | rectangle keep-outs with a notch, GND escapes first, retry loop |
| 2 | all routed; DRC: 5 shorts, 4 clearance, 1 starved thermal | **router input error**: custom-shape solder-jumper pads read as 1.0×0.5 (real 1.0×1.5); fiducial 0.6 mm local clearance and 2 mm mask not modelled; tracks crowded LED1 GND thermal | real bounding box for custom pads, fiducial keep-out, spoke rings on THT GND pads; all copper deleted through MCP (`delete_trace`) and rerouted |
| 3 | **DRC 0 / 0 / 0** | — | — |

## Result
| Item | Value |
|---|---|
| Nets routed | 31/31 (+7 single-pin NC nets), **0 unconnected items** |
| Track length | F.Cu 776 mm, **B.Cu 46 mm** (12 short crossings, ≤ 11 mm each) |
| Widths | 0.50 mm power (81 seg), 0.40 GND stubs/necks (46), 0.30 RTN/3V3_ESP (50), 0.25 signals (154) |
| Vias | 57: 22 GND stitch/escape, 35 signal layer changes |
| Zones | +3V3_P top 251.2 mm² (solid), EF_RTN top 38.0 mm² (isolated), GND top 3419 mm², GND bottom 5342 mm² |
| Clearance | min 0.20 mm (DRC rule), router ≥ 0.24 mm |

## Engineering review
- **Return paths.** The bottom GND plane is continuous except for 12 short crossings (≤ 11 mm). Each of the 22 SMD GND pads
  has its own via, at most 1.6 mm from the pad centre (measured). All signals are slow (≤ 1 MHz class), so no impedance control is needed.
- **Protection path.** J1 → C12 → U5 is short (J1 pin 1 to U5 IN is 13.6 mm straight-line). The ILIM/dVdT traces are 2.6/4.6 mm, with no coupling to
  switching nodes (there are none on this board).
- **High current.** The VIN/+5V_P path is 0.5 mm wide, necked to the pad width only at U5's 0.65 mm pins. No narrow
  necks elsewhere.
- **Thermal.** The thermal copper is kept free of other nets (keep-out during routing).
- **Domains.** No routed copper joins +3V3_P and 3V3_ESP (DRC parity 0, netlist identical).
- The router's planned geometry and a preview are kept as evidence (`evidence/layout/routes.json`,
  `images/route_preview_planned.png`).
