# NOTICE — Sensor Interface & Power Management Board

**Hardware design: Sensor Interface & Power Management Board for ESP32, board revision A, release v1.0.0.**

Copyright 2026 AI-PCB-Engineer contributors.

The original hardware design source and documentation of this project (schematic, PCB layout, manufacturing
data, drawings and hardware documentation) are licensed under the **CERN Open Hardware Licence Version 2 –
Permissive** (SPDX: `CERN-OHL-P-2.0`). The licence text is in `LICENSE-HARDWARE`
(also at https://ohwr.org/cern_ohl_p_v2.txt). The original software (scripts) in the source repository is
licensed under the MIT License (`LICENSE-CODE`). The exact scope of each licence is in `LICENSE_SCOPE.md`.

## Disclaimer
The hardware design is provided "as is", without any warranty, as stated in section 5 (Disclaimer and Liability)
of CERN-OHL-P-2.0. **This design is DIGITALLY VALIDATED ONLY. It has NOT been fabricated, assembled or physically
tested.** No electrical safety, EMC, reliability or regulatory certification has been performed or is claimed.
Use of the CERN-OHL-P licence does not imply any endorsement by CERN or any involvement of CERN in this design.

## Design limitations (summary)
- Input 5.0 V DC ±5 % only. An isolated supply is recommended. Never exceed 50 V at J1, even reversed.
- Reverse-polarity protection does **not** cover ground loops when the supply and the ESP32 USB host (or a peripheral) are earthed.
- No surge or ESD protection is claimed.
- +3V3_P is limited to 250 mA at ≤ 50 °C (calculated).
- Power the board before or together with the ESP32 (rule R-31).
- The ESP32-facing signals and J6 are 3.3 V only.

Full text: `docs/safety/SAFETY_AND_POWER.md` in the source repository.

## Acknowledgements and third-party material
- KiCad library data (symbols and footprints in the design files, 3D model geometry in the STEP file and renders)
  comes from the KiCad libraries (KiCad Library contributors, https://gitlab.com/kicad/libraries).
  Licence: `CC-BY-SA-4.0 WITH KiCad-libraries-exception`. The exception waives article 3 for designs and
  generated files that use the library data.
- The project footprint for U5 is a **modified** KiCad library footprint. It remains under
  `CC-BY-SA-4.0 WITH KiCad-libraries-exception`. See `THIRD_PARTY_NOTICES.md`.
- Component names, manufacturer names and trademarks (e.g. Texas Instruments, Espressif/ESP32, Samtec, Phoenix
  Contact, Kingbright, Keystone, Samsung, Murata, Panasonic) belong to their owners and are used only to identify parts.
  This licence grants no rights to third-party patents, trademarks, datasheets or products.

## Modification notices
The modification history of the covered source is in `MODIFICATIONS.md`. If you modify and convey this design,
CERN-OHL-P-2.0 §3.3 requires you to keep these notices and to add a notice that you modified it, with the date and a
brief description (see `docs/licensing/CONTRIBUTOR_NOTICES.md`). Products made from the design must give their
recipients access to these notices (§4).

Source repository: AI-PCB-Engineer, `hardware/kicad/Sensor_Interface_Power_Board/` (release tag `v1.0.0`).
