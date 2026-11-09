# Modification Notices (CERN-OHL-P-2.0 §3.3(b))

This file records modifications of the Covered Source. **Never delete or rewrite earlier entries.** Add new
entries at the end. Downstream modifiers who convey a modified version must add their own entry with the date and
a brief description of how they modified the design (see `docs/licensing/CONTRIBUTOR_NOTICES.md`).

## Original licensor's revision history (before and at first public release)
| Date | Version / board rev | Modified by | Description |
|---|---|---|---|
| 2026-11-08 | 0.1.0 / — | AI-PCB-Engineer contributors | Initial schematic (Architecture B, ultrasonic interface, I²C/UART/GPIO) |
| 2026-11-09 | 0.2.0 / 0.2.0 | AI-PCB-Engineer contributors | Input protection redesigned: TPS26600 eFuse replaces fuse/P-FET/TVS (DDR-17); R15 TRIG series resistor; complete 2-layer PCB layout; manufacturing package |
| 2026-11-09 | 1.0.0-rc1 / A | AI-PCB-Engineer contributors | Board revision label "REV A v1.0" and title block rev A (DDR-22); no electrical or copper change |
| 2026-11-09 | 1.0.0 / A | AI-PCB-Engineer contributors | First public release under CERN-OHL-P-2.0 (hardware) and MIT (code). No design change from 1.0.0-rc1 |

## Third-party material modified by this project
| Date | Material | Upstream | Modification |
|---|---|---|---|
| 2026-11-09 | `Sensor_Interface_Power_Board.pretty/TI_PWP0016A_HTSSOP-16-1EP_4.4x5mm_P0.65mm_EP3.4x5mm.kicad_mod` | KiCad library footprint `Package_SO:HTSSOP-16-1EP_4.4x5mm_P0.65mm_EP3.4x5mm_Mask2.66x2.46mm` (CC-BY-SA-4.0 WITH KiCad-libraries-exception) | Pads changed to 1.5 × 0.45 mm on a 5.8 mm span, exposed pad 3.4 × 5.0 mm, mask and paste openings 3.3 × 3.3 mm, per the TI PWP0016A land pattern (TPS2660 datasheet SLVSDG2G p.53–54). The result stays under the upstream licence |

## Downstream modifications
| Date | Modified by | Description |
|---|---|---|
| | | |
