# Component Selection — V0.1.0 (BOM)

Status: **SELECTED** = official datasheet read and checked against the design (DATASHEET_VERIFICATION.md).
**PROVISIONAL** = selected, but one listed item must be confirmed at order or layout time. Nothing was purchased.

| Ref | Qty | Function | Manufacturer | MPN | Package / footprint | Status | Alternatives |
|---|---|---|---|---|---|---|---|
| J1 | 1 | 5 V input terminal | Phoenix Contact | 1715721 | MKDS 1,5/2-5,08 / `TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal` | SELECTED | any 5.08 mm 2-pos terminal ≥ 1 A |
| F1 | 1 | Polyfuse 0.5 A hold | Bourns | MF-MSMF050-2 | 1812 / `Fuse_1812_4532Metric` | SELECTED | MF-MSMF050/16X-2 (16 V rated) |
| Q1 | 1 | Reverse-polarity P-MOSFET | Alpha & Omega Semiconductor | AO3401A | SOT-23 / `SOT-23` | SELECTED | any −20/−30 V P-FET, VGS ±12 V, RDS(on) ≤ 85 mΩ at −2.5 V, G-S-D pinout |
| R1 | 1 | Q1 gate 10 kΩ | Panasonic | ERJ-3EKF1002V | 0603 | SELECTED | Yageo RC0603FR-0710KL (datasheet not retrieved) |
| D1 | 1 | TVS 6.0 V VWM | Vishay | SMAJ6.0A-E3/61 | SMA / `D_SMA` | PROVISIONAL (cathode-band ↔ pad 1 check in V0.2.0) | Littelfuse SMAJ6.0A |
| U1 | 1 | 3.3 V LDO 1 A | Texas Instruments | TLV1117LV33DCYR | SOT-223 / `SOT-223-3_TabPin2` (symbol AMS1117-3.3, pin-identical) | SELECTED | TLV761 (TI-suggested upgrade, not evaluated) |
| U2, U4 | 2 | 5 V-tolerant Schmitt buffer | Texas Instruments | SN74LVC1G17DBVR | SOT-23-5 | SELECTED | SN74LVC1G34 (no hysteresis; not preferred) |
| U3 | 1 | 3.3→5 V translator | Texas Instruments | SN74LVC1T45DBVR | SOT-23-6 | SELECTED | SN74LV1T34 (not evaluated) |
| C1, C3, C8 | 3 | 10 µF 10 V X5R | Samsung Electro-Mechanics | CL10A106KP8NNNC | 0603 | PROVISIONAL (DC-bias curve unavailable; suffix C at order) | Murata GRM188R61A106KE69D (datasheet fetch failed) |
| C2, C4, C5, C6, C7, C9, C10, C11 | 8 | 100 nF 16 V X7R | Murata | GRM188R71C104KA01D | 0603 | SELECTED | — |
| R2 | 1 | LED1 1.5 kΩ | Panasonic | ERJ-3EKF1501V | 0603 | SELECTED | — |
| R3 | 1 | LED2 680 Ω | Panasonic | ERJ-3EKF6800V | 0603 | SELECTED | — |
| R4, R5, R7, R12 | 4 | 100 kΩ pull-down/up | Panasonic | ERJ-3EKF1003V | 0603 | SELECTED | — |
| R6, R11, R13, R14 | 4 | 1 kΩ series | Panasonic | ERJ-3EKF1001V | 0603 | SELECTED | — |
| R8, R9 | 2 | I2C pull-up 2.2 kΩ | Panasonic | ERJ-3EKF2201V | 0603 | SELECTED | — |
| R10 | 1 | UART TX series 220 Ω | Panasonic | ERJ-3EKF2200V | 0603 | SELECTED | — |
| LED1 | 1 | 5 V indicator, red | Kingbright | WP7113ID | T-1¾ 5 mm / `LED_D5.0mm` | SELECTED | — |
| LED2 | 1 | 3.3 V indicator, green | Kingbright | WP7113SGD | T-1¾ 5 mm / `LED_D5.0mm` | SELECTED | — |
| J2 | 1 | ESP32 interface 1×12 | Samtec | **HTSW-112-07-T-S** | 2.54 mm / `PinHeader_1x12_P2.54mm_Vertical` | PROVISIONAL (mechanical interface Option B) | — |
| J3, J4, J5, J6 | 4 | Ultrasonic / UART / I2C / GP 1×4 | Samtec | **HTSW-104-07-T-S** | 2.54 mm / `PinHeader_1x04_P2.54mm_Vertical` | SELECTED | — |
| TP1–TP8 | 8 | SMT test points | Keystone Electronics | 5015 | `TestPoint_Keystone_5015_Micro_Mini` | SELECTED | Keystone 5017 |
| JP1 | 1 | UART VCC select (3-pad, 1-2 bridged) | — | PCB feature | `SolderJumper-3_P1.3mm_Bridged12_RoundedPad1.0x1.5mm` | n/a | — |
| JP2 | 1 | I2C pull-up enable (bridged) | — | PCB feature | `SolderJumper-2_P1.3mm_Bridged_RoundedPad1.0x1.5mm` | n/a | — |
| — | 1 | Ultrasonic module (off-board, recommended) | Adafruit | 4007 | module | VENDOR-documented | Adafruit 3942 (HC-SR04) |

## Notable selection corrections made during verification
| Item | Initial choice | Problem found in the datasheet | Correction |
|---|---|---|---|
| Header MPN | TSW-1xx-07-**G**-S | Samtec plating options are −F/−GF/−L/−T. "−G" does not exist (DS-15) | −T (matte tin) |
| Header series | TSW | "TSW: Lead-Free Solderable: No, Lead Wave Only" (DS-15) | **HTSW** (Hi-Temp LCP, lead-free solderable: Yes), same pin layout |
| LDO | MCP1826S (Microchip) | official datasheet not retrievable from the manufacturer domain | TLV1117LV33 (TI, official datasheet read) |
| TVS symbol | `Device:D_TVS` | KiCad's D_TVS is bidirectional (A1/A2). The part is unidirectional | `Device:D_Zener` (K/A) |
| Test points | Keystone 5000/5001 THT | the retrieved Keystone sheet covers SMT parts (5015 …) | Keystone 5015 SMT |
| 10 µF MLCC | Murata GRM188R61A106KE69 | Murata server reset the connection (3 attempts). KEMET certificate expired. TDK 403 | Samsung CL10A106KP8NNNC (official online sheet) |
