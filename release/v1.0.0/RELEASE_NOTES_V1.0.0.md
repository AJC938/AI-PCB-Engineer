# Release Notes — v1.0.0 (board Rev A)

**Sensor Interface & Power Management Board for ESP32**, released 2026-11-09.

> **v1.0.0 = fabrication-ready open hardware design release.** The design passed every digital check. It has
> **NOT been physically fabricated, assembled or tested.** Build a small first batch and follow the physical test plan.

## Download
| File | Use |
|---|---|
| `manufacturing/Sensor_Interface_Power_Board/RevA/packages/Sensor_Interface_PCB_RevA_Fabrication.zip` | Bare PCB order |
| `…/packages/Sensor_Interface_PCB_RevA_Assembly.zip` | BOM, CPL, assembly drawings |
| `…/packages/Sensor_Interface_PCB_RevA_Complete_Manufacturing.zip` | Fabrication + full turnkey assembly quote |
| `…/checksums/SHA256SUMS.txt` | Integrity check (`sha256sum -c`) |
| `hardware/kicad/Sensor_Interface_Power_Board/` | KiCad 10 source |

SHA-256 of the packages:
```
09a6932a98d854e3110cbb7bd1512aad493aca96dc5361b0a697ad747015996b  Sensor_Interface_PCB_RevA_Fabrication.zip
6683502f8018e1416aadc79c326ec78c94f8d8e3a567abd1bce131658ba6a57b  Sensor_Interface_PCB_RevA_Assembly.zip
008feec3bc17f058fed57db5eefe5c57230cbffb453ca897742e9256fbcc2c08  Sensor_Interface_PCB_RevA_Complete_Manufacturing.zip
```

## Highlights
- 90 × 64 mm, 2-layer FR-4, top-side assembly (44 SMT + 8 THT), 4 × M3.
- TPS26600 eFuse input: OVP 5.39–5.82 V, UVLO 4.25–4.56 V, reverse-polarity blocking, 0.51–0.69 A current limit.
- 3.3 V / 250 mA peripheral LDO with 251 mm² thermal copper.
- HC-SR04-style ultrasonic interface (3.3 ↔ 5 V), I²C, UART (3.3/5 V device supply), 2 GPIO.
- ESP32 DevKit stays on its own USB power. No connection between the board's 3.3 V rail and the ESP32's.

## Changes since V0.2.0
- Final engineering audit of the complete design. **No electrical or layout correction was needed.**
- Board revision label: title block rev **A**; silkscreen "REV A v1.0" (DDR-22). Copper, drills, BOM and CPL unchanged.
- Manufacturing outputs regenerated and independently audited (19/19). Three tested ZIP packages and SHA-256 checksums.
- BOM: engineering descriptions, dated sourcing notes, verified alternatives (carrier variants only).
- New documentation: README, quick start, connection guide, safety, architecture, electrical design, layout,
  manufacturing, assembly, validation status, visual review, licensing. KiCad-generated renders.
- Licences: CERN-OHL-S-2.0 (hardware), MIT (scripts).

## Validation
ERC 0 · DRC 0 errors / 0 warnings (zones refilled, all severities, no exclusions) · 0 unconnected · schematic parity
0 · netlist/power-domain verifier PASS · package audit 19/19 · ZIP extraction tests PASS · fresh-process reopen PASS.

## Known limitations
1. Not fabricated, not tested.
2. Reverse-polarity protection does not cover ground loops when the supply and the ESP32 USB host are earthed.
3. No surge protection; fast overvoltage steps while powered are not covered.
4. +3V3_P limited to 250 mA at ≤ 50 °C (calculated).
5. Power-up rule R-31: power the board before or together with the ESP32.
6. Ultrasonic module pin order and mating connectors not verified; wire J3 by labels.
7. TPS26600PWPR stock not confirmed on 2026-11-09 (DigiKey 0 in stock, 26-week lead time; TI store out of stock).
