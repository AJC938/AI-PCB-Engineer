# Visual Review — Rev A

The generated renders below were produced from the Rev A design files using KiCad 10.0.8 command-line exports. The separate `images/screenshots/` gallery contains seven **actual GUI screenshots** captured from the released project in KiCad Schematic Editor, PCB Editor, and 3D Viewer.

No photograph exists because no board has been manufactured. 3D component bodies are KiCad library models and **represent shape only, not the exact purchased parts**. For example, LED2 is green in the BOM but uses the generic red LED model.

## Actual KiCad GUI screenshots

| Schematic | Power | PCB top | PCB bottom |
|---|---|---|---|
| ![Full schematic](images/screenshots/01-schematic-full.png) | ![Power management](images/screenshots/02-power-management.png) | ![PCB top](images/screenshots/03-pcb-top-layout.png) | ![PCB bottom](images/screenshots/04-pcb-bottom-layout.png) |

| 3D top | 3D bottom | Connector details |
|---|---|---|
| ![3D top](images/screenshots/05-pcb-3d-viewer.png) | ![3D bottom](images/screenshots/06-pcb-3d-bottom.png) | ![Connectors](images/screenshots/07-connectors.png) |
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

## Owner review checklist
- [x] Actual GUI captures reviewed for board outline, connector positions and silkscreen legibility
- [x] Silkscreen label shows "REV A v1.0"
- [x] No image contains personal information
