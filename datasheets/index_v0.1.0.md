# Reference Document Index — V0.1.0 Phase 1

Planning references only. **No component has been selected.** PDFs are not committed (copyright).
Accessed 2026-11-08. Evidence class: **OFFICIAL** = issued by the device or standard owner.
**SECONDARY** = third-party, not usable as a verified limit.

| ID | Document | Issuer / revision | Source | Class | Facts used (section/table/page) |
|---|---|---|---|---|---|
| REF-01 | ESP32 Series Datasheet | Espressif, **v5.3** | https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf (redirects to documentation.espressif.com) | OFFICIAL | Table 5-1 (p.51): VDD abs max −0.3…3.6 V, cumulative IO output 1200 mA. Table 5-2 (p.51): VDD3P3 3.0/2.3–3.6 V, **external supply ≥ 0.5 A**. Table 5-3 (p.52): VIH 0.75×VDD…VDD+0.3, VIL −0.3…0.25×VDD, VOH ≥ 0.8×VDD, VOL ≤ 0.1×VDD, IOH 40 mA typ, IOL 28 mA typ, internal pull-up/down 45 kΩ typ. Table 5-4 (p.52): TX 802.11b 240 mA typ (50 % duty), RX 95–100 mA. **No 5 V tolerance stated** |
| REF-02 | ESP32-WROOM-32E / -32UE Datasheet | Espressif, **v2.1** | https://www.espressif.com/sites/default/files/documentation/esp32-wroom-32e_esp32-wroom-32ue_datasheet_en.pdf | OFFICIAL | Table 13 (p.28): VDD33 abs max 3.6 V. Table 14: VDD33 3.0–3.6 V, **IVDD ≥ 0.5 A**, −40…85/105 °C. Table 15 (p.28–29): same IO thresholds as REF-01. Table 16 (p.29): TX 802.11b @19.5 dBm **avg 239 mA, peak 379 mA** (100 % duty). RX 112–118 mA |
| REF-03 | ESP32-DevKitC V4 User Guide | Espressif docs (latest, no revision date shown) | https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/esp32-devkitc/user_guide.html | OFFICIAL | Three **mutually exclusive** power options (Micro-USB, 5V/GND pins, 3V3/GND pins). "one and only one of the options… otherwise the board and/or the power supply source can be damaged". J2/J3 2×19-pin headers. 5V = J2-19, 3V3 = J2-1, GND = J2-14, J3-1, J3-7. GPIO34/35/36/39 marked input (I). GPIO6–11 (flash): avoid. GPIO16/17 not available on WROVER variants. Variants: -32E, -32UE, -VE, -VIE |
| REF-04 | UM10204 I2C-bus specification and user manual | NXP, **Rev. 7.0, 1 Oct 2021** | https://www.nxp.com/docs/en/user-guide/UM10204.pdf | OFFICIAL | Table 9 (p.43): VOL ≤ 0.4 V at 3 mA (Std/Fast). Table 10 (p.44): tr ≤ 1000 ns (Std) / 300 ns (Fast). Cb ≤ 400 pF. §7.1 (p.50): Rp(max) = tr/(0.8473·Cb). Rp(min) from VOL and 3 mA sink |
| REF-05 | HC-SR04 "ElecFreaks" datasheet | ElecFreaks (via third-party mirror listing) | radiolocman.com listing di=168043 (**PDF not retrieved**) | SECONDARY | Listing text only: "2cm–400cm non-contact measurement" |
| REF-06 | "HC-SR04 Ultrasonic Sensor: pinout, datasheet, specs" | R. Mischianti (article, 2026-07-13) | https://mischianti.org/hc-sr04-ultrasonic-sensor-high-resolution-pinout-datasheet-pinout-and-specs/ | SECONDARY | Variant families "Classic" (LM324 + MAX232 + MCU, 5 V only, Echo "5V TTL", ~15 mA), "Clone" (5 V only, Echo "5V TTL"), "Modern" (single IC e.g. RCWL-9200, 2.8–5.5 V, Echo Vcc-dependent, ~2–3.6 mA). No trigger threshold given for any variant |
| REF-07 | Search summary of further HC-SR04 sources | various | web search 2026-11-08 | SECONDARY | Several sources repeat 15 mA, 10 µs TTL trigger and TTL echo. One lists 16 mA. Some describe 3.3 V-capable second-generation modules |

Not retrieved (blocked or not attempted): SparkFun-hosted HC-SR04 PDFs (fetch proxy refused the domain),
the ESP32-DevKitC V4 schematic and dimension drawing (needed, see OPEN_QUESTIONS OQ-02/OQ-03).
**HC-SR04 has no single original manufacturer. Every value for it is SECONDARY until the exact module
is chosen and its vendor document is obtained, or the value is measured.**
