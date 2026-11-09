# Release Notes — v1.0.0 (board Rev A)

**Sensor Interface & Power Management Board for ESP32**, released 2026-11-09.

> **DIGITALLY VALIDATED — NOT FABRICATED OR PHYSICALLY TESTED.**
> v1.0.0 is a fabrication-ready open hardware **design** release. No board has been manufactured, assembled,
> powered or measured. No reliability, safety, EMC or production testing, and no certification, is claimed.

## Licences
| Material | Licence |
|---|---|
| Original hardware design source and hardware documentation | **CERN-OHL-P-2.0** (`LICENSE-HARDWARE`, official text) |
| Original software and scripts | **MIT** (`LICENSE-CODE`) |
| Third-party material | its own terms (`THIRD_PARTY_NOTICES.md`). The U5 project footprint is derived from the KiCad library and stays `CC-BY-SA-4.0 WITH KiCad-libraries-exception` |

Scope map: `LICENSE_SCOPE.md` / `REUSE.toml`. Notices: `NOTICE.md`. Modification notices: `MODIFICATIONS.md`.
Commercial manufacturing and sale are permitted. Recipients of boards must have access to `NOTICE.md`
(CERN-OHL-P §4). It is included in every manufacturing ZIP.

## Download
| File | Use |
|---|---|
| `manufacturing/Sensor_Interface_Power_Board/RevA/packages/Sensor_Interface_PCB_RevA_Fabrication.zip` | Bare PCB order |
| `…/packages/Sensor_Interface_PCB_RevA_Assembly.zip` | BOM, CPL, assembly drawings |
| `…/packages/Sensor_Interface_PCB_RevA_Complete_Manufacturing.zip` | Fabrication + full turnkey assembly quote |
| `…/checksums/SHA256SUMS.txt` | Integrity check (`sha256sum -c`, run from `RevA/`) |
| `hardware/kicad/Sensor_Interface_Power_Board/` | KiCad 10 source |

SHA-256 of the packages:
```
9c3c876b633df825f17ef1379bb1196cdc2a62668cd49f2bf7db18d2376fe584  Sensor_Interface_PCB_RevA_Assembly.zip
618a06f370de7f01433c91ea8d132d1203f51e3a5f4ecc199ac507ae165f138b  Sensor_Interface_PCB_RevA_Complete_Manufacturing.zip
80e270fb082e33fba018466a3b9a1c215885a0ab98d3f98470e457ab32f46033  Sensor_Interface_PCB_RevA_Fabrication.zip
```

## Highlights
- 90 × 64 mm, 2-layer FR-4 1.6 mm, 1 oz, top-side assembly (44 SMT + 8 THT), 4 × M3.
- TPS26600 eFuse input: OVP 5.39–5.82 V, UVLO 4.25–4.56 V, reverse-polarity blocking, 0.51–0.69 A current limit.
- 3.3 V / 250 mA peripheral LDO with 251 mm² thermal copper.
- HC-SR04-style ultrasonic interface (3.3 ↔ 5 V), I²C, UART (3.3/5 V device supply), 2 GPIO.
- The ESP32 DevKit stays on its own USB power; the board's 3.3 V rail never connects to the ESP32's.

## Changes since V0.2.0
- Final engineering audit. **No electrical or layout correction was needed.**
- Board revision label Rev A (DDR-22). Copper, drills, BOM parts and CPL are unchanged.
- Regenerated and audited manufacturing outputs (19/19); three tested ZIP packages; SHA-256 checksums.
- Full documentation set and KiCad-generated renders.
- Final licensing: CERN-OHL-P-2.0 + MIT, scope map, notices, third-party audit. The packages now carry
  `NOTICE.md` and `LICENSE-HARDWARE.txt`.
- From `v1.0.0-rc1` to `v1.0.0`: licensing and documentation only. Engineering files are byte-identical.

## Validation (digital only)
ERC 0 · DRC 0 errors / 0 warnings (zones refilled, all severities, no exclusions) · 0 unconnected · schematic parity 0
· netlist/power-domain verifier PASS · package audit 19/19 · licence audit 9/9 · ZIP extraction tests PASS ·
`sha256sum -c` PASS · clean-clone validation PASS.

## Known limitations
1. **Not fabricated, not physically tested.**
2. Reverse-polarity protection does not cover ground loops when the supply and the ESP32 USB host are earthed.
3. No surge protection; fast overvoltage steps while powered are not covered.
4. +3V3_P limited to 250 mA at ≤ 50 °C (calculated).
5. Power-up rule R-31: power the board before or together with the ESP32.
6. Ultrasonic module pin order and mating connectors not verified; wire J3 by labels.
7. TPS26600PWPR stock not confirmed on 2026-11-09 (DigiKey 0 in stock, 26-week lead time; TI store out of stock).
