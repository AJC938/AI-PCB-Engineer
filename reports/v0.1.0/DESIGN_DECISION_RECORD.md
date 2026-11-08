# Design Decision Record — V0.1.0

| ID | Decision | Alternatives | Evidence | Calculations | Risks | Reason |
|---|---|---|---|---|---|---|
| DDR-01 | **Architecture B**: DevKit on its own USB. Board powers peripherals only. DevKit 5V pin not wired | A (board powers DevKit), C (board 3V3 into DevKit) | DS-02b one-source rule. Clone VBUS path unknown | Input 0.28 A (B) vs about 0.8–1.0 A (A) | two supplies. Power-sequencing rule (R-31) | Compliant by construction, independent of clone internals |
| DDR-02 | ESP32-facing logic powered from **3V3_ESP** (DevKit 3V3 used as a ≤ 3.4 mA reference) | power buffers from `+3V3_P` | DS-07/08 Ioff and VCC isolation. DS-01 VIH max = VDD + 0.3 | VOH ≤ VDD by construction. Margins +0.65…0.80 V | the clone regulator must source 3.4 mA (plausible) | Logic levels track the ESP32's VDD. No back-drive when the ESP32 is off |
| DDR-03 | ECHO via **SN74LVC1G17** (5 V-tolerant Schmitt buffer) + 1 kΩ series + 100 kΩ pull-down | resistor divider (Phase 1 E1), MOSFET shifter | DS-07 VI ≤ 5.5 V independent of VCC, VT+ ≤ 2.25 V | Echo margin +2.15 V, any variant | needs VCC from 3V3_ESP | Divider window was only 0.6 V and failed for 3.3 V-output modules |
| DDR-04 | TRIG via **SN74LVC1T45** A→B (DIR = VCCA), VCCB = `+5V_P` | direct GPIO drive | DS-08 VIH 2.0 V. VOH = VCCO − 0.1 | +0.40 V input margin. TRIG ≥ 98 % of sensor VCC | none significant | Sensor VIH unpublished. Driving at the sensor's own rail removes the unknown |
| DDR-05 | Sensor VCC fixed at **+5V_P** | selectable 3.3/5 V | DS-13 3–5.5 V. Classic modules are 5 V-only (SECONDARY) | 4.44–5.25 V in range | — | Works for both module families. Echo stays inside the buffer's VI ≤ 5.5 V |
| DDR-06 | **Adafruit 4007** recommended module | Adafruit 3942, generic HC-SR04 | DS-13 (vendor-documented) | 2.2 mA | pin order unpublished (verify on receipt) | Best-documented candidate. Interface is variant-independent |
| DDR-07 | Reverse polarity by **P-MOSFET AO3401A** | series Schottky, ideal-diode controller | DS-03 | 35 mV / 9.7 mW worst vs 0.3–0.5 V for a Schottky | — | Keeps `+5V_P` ≥ 4.44 V for the 5 V sensor and the LDO |
| DDR-08 | Overcurrent by **MF-MSMF050-2** polyfuse | fuse, eFuse | DS-04 derating | hold ×1.45 at 50 °C. Drop ≤ 0.28 V | slow trip (s at low overload) | Resettable. Sized for the 0.28 A budget |
| DDR-09 | **SMAJ6.0A** TVS on `+5V_P` | SMAJ5.0A (VWM below 5.25 V), none | DS-05 | VWM 6.0 > 5.25 V | clamp 10.3 V > downstream abs max (R-32) | ESD/hot-plug aid. Not surge or overvoltage protection |
| DDR-10 | **TLV1117LV33** LDO | buck, MCP1826S | DS-06 | 0.505 W, Tj 81.8 °C at 50 °C | needs tab copper (V0.2.0) | Low noise, simple. Official datasheet available |
| DDR-11 | I2C pull-ups **2.2 kΩ to 3V3_ESP**, disconnectable (JP2) | 4.7 kΩ, pull-ups to `+3V3_P` | UM10204 | Fast-mode to 159 pF. Rp(min) margin | unpowered I2C devices back-fed when the board is off (R-31) | No back-power into the ESP32. Fast-mode capable |
| DDR-12 | UART RX buffered (SN74LVC1G17), TX 220 Ω series. VCC selectable (JP1, default 3V3) | direct lines | DS-07 | 5 V device TX accepted. Short ≤ 16 mA | 5 V CMOS RX devices unsupported | Robust RX, simple TX |
| DDR-13 | GPIO map: ECHO 34, TRIG 26, SDA 21, SCL 22, TX 17, RX 16, GP 32/33 | others | DS-01 strapping/input-only/ADC1 tables | — | GPIO16/17 unavailable on WROVER boards | Avoids strapping, flash and UART0 pins |
| DDR-14 | Mechanical interface **Option B** (1×12 header + wires) for V0.1.0 | Option A female sockets | no verified clone drawing | — | wiring errors (labels mitigate) | Electrical design completes without mechanical guesses |
| DDR-15 | Connectivity by **global labels on pin endpoints** | wires, local labels | V0.0.2 D-2 | — | readability is lower than with drawn wires | Robust MCP construction, net names stable through sync |
| DDR-16 | Headers **HTSW** instead of TSW | TSW | DS-15 lead-free note | — | — | Lead-free solderable |
