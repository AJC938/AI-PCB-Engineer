# Visual Review — Rev A

Every image on this page was generated from the actual Rev A design files by KiCad 10.0.8
(`kicad-cli pcb render` for 3D, `kicad-cli pcb/sch export pdf` rasterized by `scripts/release/make_2d_views.py`).
No photograph exists, because no board has been manufactured. 3D component bodies are KiCad library models and
**represent shape only, not the exact purchased parts.** For example, LED2 is green in the BOM but uses the generic red LED model.

## 3D
| Isometric | Isometric (rear) |
|---|---|
| ![3D isometric](../../media/renders/3d_isometric.png) | ![3D isometric rear](../../media/renders/3d_isometric_rear.png) |

| Top | Bottom |
|---|---|
| ![3D top](../../media/renders/3d_top.png) | ![3D bottom](../../media/renders/3d_bottom.png) |

## 2D PCB
Top (copper, mask, silkscreen, outline):

![PCB top](../../media/renders/pcb_top_2d.png)

Bottom (copper, mirrored, as seen from below):

![PCB bottom](../../media/renders/pcb_bottom_2d.png)

## Connector close-ups (from the top plot)
| Power input: J1, U5 eFuse, U1 LDO | Peripheral headers J3–J6 |
|---|---|
| ![power](../../media/renders/closeup_power_input_J1_U5_U1.png) | ![headers](../../media/renders/closeup_peripheral_headers_J3-J6.png) |

ESP32 interface J2:

![J2](../../media/renders/closeup_esp32_header_J2.png)

## Schematic
![Schematic overview](../../media/renders/schematic_overview.png)

Power entry (J1, U5 eFuse, divider, RILIM, dVdT):

![eFuse](../../media/renders/schematic_power_entry_efuse.png)

## Diagrams
Power-architecture and signal-conditioning diagrams are drawn in Mermaid (rendered by GitHub) in
[BOARD_ARCHITECTURE.md](../system-architecture/BOARD_ARCHITECTURE.md) and
[CONNECTION_GUIDE.md](../pinout/CONNECTION_GUIDE.md). They are based on the netlist.

## Owner review checklist (before publishing)
- [ ] Renders match expectations (board outline, connector positions, silkscreen legend readable)
- [ ] Silkscreen label shows "REV A v1.0"
- [ ] No image contains personal information
