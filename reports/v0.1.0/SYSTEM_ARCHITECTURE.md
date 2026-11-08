# System Architecture — V0.1.0 (Sensor Interface & Power Management Board for ESP32)

## Context
An external companion board. The ESP32 development board stays on its own USB supply
(**Architecture B**, see POWER_ARCHITECTURE.md). The board takes a separate 5 V input and powers,
protects and level-conditions the external peripherals.

## Platform
| Item | Value | Evidence |
|---|---|---|
| User's board (provisional description) | ESP32 with ESP-WROOM-32 module, USB-C, CP2102 USB-UART, 2 header rows, likely 38-pin | user description, not verified physically |
| Closest documented board | Espressif **ESP32-DevKitC V4** (38-pin, 2 × 19 headers) | DS-02b |
| Chip-level electrical limits | ESP32 Series Datasheet v5.3 + WROOM-32E v2.1 (same IO electrical class) | DS-01/02 |
| Mechanical interface | **Provisional**: 1×12 header (J2) wired to the DevKit (Option B below). No DevKit dimensions assumed | — |

## Voltage domains
| Domain | Net | Source | Consumers |
|---|---|---|---|
| Raw input | `VIN_RAW`, `VIN_FUSED` | J1 (5 V ±5 % spec) | polyfuse, reverse-polarity FET |
| Protected 5 V | `+5V_P` | after F1 + Q1, clamped by D1 | ultrasonic VCC (J3), LVC1T45 VCCB, LDO input, LED1, UART VCC option |
| Board 3.3 V | `+3V3_P` | U1 TLV1117LV33 | I2C VCC (J5), GP VCC (J6), UART VCC default, LED2 |
| ESP32 reference 3.3 V | `3V3_ESP` | DevKit 3V3 pin via J2-1 (**sinks no power into the DevKit**) | U2/U4 VCC, U3 VCCA and DIR, I2C pull-ups (via JP2), UART RX pull-up. About 3.4 mA max |
| Ground | `GND` | common (J1-2, J2-2/11/12) | all |

`+3V3_P` and `3V3_ESP` are separate nets with no common node, which the verifier checks automatically.

## Block diagram
```mermaid
flowchart LR
  J1["J1 5V in<br/>Phoenix 1715721"] --> F1["F1 polyfuse<br/>MF-MSMF050-2"] --> Q1["Q1 P-MOSFET<br/>AO3401A (rev. polarity)"] --> P5["+5V_P"]
  P5 --- D1["D1 TVS SMAJ6.0A"]
  P5 --> U1["U1 TLV1117LV33"] --> P33["+3V3_P"]
  P5 --> J3V["J3 ultrasonic VCC"]
  P33 --> J5V["J5 I2C VCC"] & J6V["J6 GP VCC"]
  P5 & P33 --> JP1["JP1 UART VCC select (default 3V3)"] --> J4V["J4 UART VCC"]
  subgraph ESPDOM["ESP32 domain (3V3_ESP from DevKit, J2)"]
    U3A["U3 A side"]
    U2["U2 SN74LVC1G17 (Echo)"]
    U4["U4 SN74LVC1G17 (UART RX)"]
    PU["I2C pull-ups 2.2k (JP2)"]
  end
  GPIO26["GPIO26 TRIG"] --> U3A --> U3B["U3 B side (VCCB=+5V_P)"] --> TRIG["J3 TRIG (5 V CMOS)"]
  ECHO["J3 ECHO (≈ sensor VCC)"] --> R6["1k"] --> U2 --> GPIO34["GPIO34 ECHO"]
  RXC["J4 RX (3.3/5 V)"] --> R11["1k"] --> U4 --> GPIO16["GPIO16 RX"]
  GPIO17["GPIO17 TX"] --> R10["220R"] --> TXC["J4 TX (3.3 V logic)"]
  SDA["GPIO21 SDA / GPIO22 SCL"] <--> J5S["J5 SDA/SCL"]
  PU --- J5S
  GP["GPIO32/33"] <--> R1314["1k series"] <--> J6S["J6 GP_IO1/2 (3.3 V only)"]
```

## GPIO assignment (ESP32 GPIO numbers; DevKit header positions are wired by label)
| Function | GPIO | Direction | Why this pin (DS-01) |
|---|---|---|---|
| US_ECHO_ESP | **34** | in | input-only pin (no output driver needed), not strapping, ADC1_CH6 |
| US_TRIG_ESP | **26** | out | general-purpose output, not strapping, not flash |
| I2C_SDA / I2C_SCL | **21 / 22** | open-drain | not strapping/flash. The common ESP32 Arduino defaults (convention, not a hardware restriction) |
| UART_TX_ESP / UART_RX_ESP | **17 / 16** | out / in | UART2 (UART0 GPIO1/3 is used by the CP2102 bridge). Available on WROOM modules (not WROVER, DS-02b) |
| GP_IO1 / GP_IO2 | **32 / 33** | in/out | ADC1_CH4/CH5, not strapping |
Excluded: GPIO0, 2, 5, 12, 15 (strapping, DS-01 Table 3-1). GPIO6–11 (flash). GPIO1/3 (USB-UART).

## Mechanical integration: options
| Criterion | A. Female headers on the PCB (DevKit plugs in) | B. Header + cable/jumper wires (chosen for V0.1.0) |
|---|---|---|
| Electrical reliability | Very good (short, fixed) | Good for signal levels. Loose-wire risk mitigated by labels |
| Assembly | Needs 2 × 19 sockets at exact pitch and row spacing | One 1×12 header |
| Mechanical compatibility | **Requires a verified drawing** of the user's clone (row spacing, length, USB-C overhang). Not available | Independent of the DevKit variant |
| Usability | Plug-and-play, but the antenna sits over the board (keep-out needed) | Flexible placement. Wiring step required |
| Decision | Deferred to V0.2.0 after measuring the physical board | **Selected now**: electrical design complete without mechanical assumptions |
