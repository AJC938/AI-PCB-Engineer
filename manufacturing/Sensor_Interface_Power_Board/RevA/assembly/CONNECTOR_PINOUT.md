# Connector Pinout — Rev A

Pin 1 of every header is the **square pad**. Voltages are nominal. Direction is seen from this board.
The full user guide with wiring diagrams is `docs/pinout/CONNECTION_GUIDE.md`.

## J1 — Power input (Phoenix Contact 1715721, MKDS 1,5/2-5,08, 2-pos screw terminal, 5.08 mm)
| Pin | Net | Voltage | Direction | Function |
|---|---|---|---|---|
| 1 | VIN_RAW | +5 V ±5 % | in | Supply input to the TPS26600 eFuse |
| 2 | GND | 0 V | — | Supply return / board ground |

## J2 — ESP32 interface (Samtec HTSW-112-07-T-S, 1×12, 2.54 mm)
| Pin | Net | Voltage | Direction | ESP32 DevKit pin (by label) |
|---|---|---|---|---|
| 1 | 3V3_ESP | 3.3 V | in (logic reference only, ≤ 3.4 mA) | 3V3 |
| 2 | GND | 0 V | — | GND |
| 3 | US_TRIG_ESP | 3.3 V | in from ESP32 | GPIO26 |
| 4 | US_ECHO_ESP | 3.3 V | out to ESP32 | GPIO34 (input-only) |
| 5 | I2C_SDA | 3.3 V | bidirectional (open-drain) | GPIO21 |
| 6 | I2C_SCL | 3.3 V | bidirectional (open-drain) | GPIO22 |
| 7 | UART_TX_ESP | 3.3 V | in from ESP32 | GPIO17 (TX2) |
| 8 | UART_RX_ESP | 3.3 V | out to ESP32 | GPIO16 (RX2) |
| 9 | GP_IO1_ESP | 3.3 V | bidirectional via 1 kΩ | GPIO32 |
| 10 | GP_IO2_ESP | 3.3 V | bidirectional via 1 kΩ | GPIO33 |
| 11 | GND | 0 V | — | GND |
| 12 | GND | 0 V | — | GND |

**The DevKit 5V/VIN pin is not wired to this board.**

## J3 — Ultrasonic sensor (Samtec HTSW-104-07-T-S, 1×4, 2.54 mm)
| Pin | Net | Voltage | Direction | Function |
|---|---|---|---|---|
| 1 | +5V_P | +5 V | out | Sensor VCC |
| 2 | US_TRIG_5V | 5 V CMOS | out | TRIG (via 1 kΩ R15) |
| 3 | US_ECHO_5V | 0–5 V | in | ECHO (5 V tolerant input via 1 kΩ, 100 kΩ pull-down) |
| 4 | GND | 0 V | — | Sensor GND |

## J4 — UART (Samtec HTSW-104-07-T-S)
| Pin | Net | Voltage | Direction | Function |
|---|---|---|---|---|
| 1 | GND | 0 V | — | GND |
| 2 | UART_VCC | 3.3 V (JP1 1-2, default) or 5 V (JP1 2-3) | out | Device supply |
| 3 | UART_TX | 3.3 V | out | ESP32 GPIO17 via 220 Ω (connect to device RX) |
| 4 | UART_RX | 3.3 V or 5 V | in | Buffered to ESP32 GPIO16 (connect to device TX); 100 kΩ pull-up to 3V3_ESP |

## J5 — I²C (Samtec HTSW-104-07-T-S)
| Pin | Net | Voltage | Direction | Function |
|---|---|---|---|---|
| 1 | GND | 0 V | — | GND |
| 2 | +3V3_P | 3.3 V | out | Peripheral supply (board LDO) |
| 3 | I2C_SDA | 3.3 V | bidirectional | SDA, 2.2 kΩ pull-up to 3V3_ESP (JP2) |
| 4 | I2C_SCL | 3.3 V | bidirectional | SCL, 2.2 kΩ pull-up to 3V3_ESP (JP2) |

## J6 — General-purpose GPIO (Samtec HTSW-104-07-T-S)
| Pin | Net | Voltage | Direction | Function |
|---|---|---|---|---|
| 1 | GND | 0 V | — | GND |
| 2 | +3V3_P | 3.3 V | out | Peripheral supply |
| 3 | GP_IO1 | **3.3 V only** | bidirectional | ESP32 GPIO32 via 1 kΩ (not 5 V tolerant) |
| 4 | GP_IO2 | **3.3 V only** | bidirectional | ESP32 GPIO33 via 1 kΩ (not 5 V tolerant) |

## Mating connectors
Not specified by this design and **not verified**. J1 takes stripped wire. J2–J6 are standard 0.64 mm square-post,
2.54 mm male headers that accept common 2.54 mm female jumper wires or housings. Check the mating part against
the Samtec HTSW datasheet before relying on a specific housing.
