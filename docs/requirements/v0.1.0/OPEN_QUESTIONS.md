# Open Questions — V0.1.0

**Blocking** = must be answered before design freeze (schematic capture).

| ID | Question | Why it matters | Information needed to resolve | Blocking |
|---|---|---|---|---|
| OQ-01 | Which exact ESP32 development board (vendor, model, revision, module: WROOM-32E/UE, WROVER-E, or another chip family such as S3/C3)? | Pinout, available GPIOs, power pins, dimensions, regulator. "ESP32 DevKit" is not one pinout | Owner's choice. Its official user guide, schematic and dimension drawing | **Yes** |
| OQ-02 | On the chosen DevKit: how are USB VBUS and the 5V header pin connected (diode? direct?), and which regulator (dropout, current) feeds 3.3 V? | Determines Arch. A safety, minimum `+5V_P`, and back-feed into a USB host | DevKit schematic (e.g. the Espressif DevKitC V4 schematic, not yet retrieved) | **Yes** (for Arch. A) |
| OQ-03 | DevKit dimensions and antenna position | Board size, connector placement, antenna keep-out | Official dimension drawing (DevKitC V4: linked PDF/DXF, not yet retrieved) | **Yes** |
| OQ-04 | What is the 5 V source and connector (bench supply, wall adapter, USB-C power)? Its current capability? | Connector type, protection rating, input transient environment | Owner's intended use. Adapter specification | **Yes** |
| OQ-05 | What input voltage tolerance and maximum (including adapter overshoot) must be survived? | Reverse-polarity, TVS standoff and clamp, regulator max input | Adapter specification or chosen standard (e.g. ±5 %) | **Yes** |
| OQ-06 | Power architecture: A (board powers DevKit), B (DevKit on USB), or A/B selectable with B as default? | Current budget (774 vs 274 mA), back-feed risk R-03/R-04, protection sizing | Owner's use case (tethered to a PC vs standalone). OQ-02 answer | **Yes** |
| OQ-07 | Which I2C devices: supply voltage, logic level, current, on-module pull-ups, bus speed, cable length? | Pull-up values, Cb, 3.3 V budget, connector pin order | Device list and their datasheets | **Yes** (budget, pin order) |
| OQ-08 | Which UART device(s): logic level, supply voltage and current, baud rate? | UART supply option, translator need, budget | Device list and datasheets | Partly |
| OQ-09 | Are 5 V-logic I2C/UART devices required? | Would add translators (scope change) | Owner decision | No (default: unsupported) |
| OQ-10 | Is the DevKit plugged onto the board (stacked) or connected by cable? | Mechanical design, antenna keep-out, connector type | Owner decision | **Yes** |
| OQ-11 | Which exact ultrasonic module (vendor, variant: classic 5 V vs 3.3 V-capable)? Its supply range, Echo HIGH level, Trigger VIH? | Echo conditioning choice, trigger translation, supply rail | Vendor document for that module, or bench measurement of a sample | **Yes** |
| OQ-12 | Pull-up reference for I2C: ESP32's own 3.3 V (via DevKit 3V3 pin as reference only) or `+3V3_P`? | Back-powering an unpowered ESP32. PWR-08 compliance | Arch. decision (OQ-06) and analysis | Yes (for Arch. B) |
| OQ-13 | Is the general-purpose connector needed, and for which sensor? | Avoid unjustified complexity | Owner's sensor plans | No |
| OQ-14 | What injection current or voltage may an unpowered ESP32 GPIO tolerate? | Arch. B signal-line safety (US-06) | Espressif documentation (not found in REF-01 sections read) or a design that avoids injection entirely | Yes (for Arch. B with a divider) |
| OQ-15 | Maximum ambient temperature and environment (indoor bench vs enclosure) | Regulator and PTC derating, thermal margin | Owner's use case | Yes |
| OQ-16 | Which PCB manufacturer, and hand assembly or PCBA? | Design rules, part sizes, BOM format | Owner decision (no order is placed) | Yes (before layout) |
| OQ-17 | Quantity and budget targets | Part choices (cost vs margin), assembly method | Owner decision | No |
| OQ-18 | Should the board carry ESD arrays on external signal connectors? | Robustness vs cost and capacitance (I2C) | OQ-07 cable lengths, use environment | No |
