# Board Architecture — Sensor Interface & Power Management Board

The board sits between an **ESP32 DevKit** and 5 V / 3.3 V peripherals. It provides protected power from an
external 5 V supply, a 3.3 V peripheral rail, 3.3 V ↔ 5 V signal conditioning for an HC-SR04-style ultrasonic
sensor, and labelled I²C, UART and GPIO headers. The ESP32 is **not** on the board.

> The AI toolchain used to design the board (Claude Code → MCP → KiCad) is described separately in
> [`docs/SYSTEM_ARCHITECTURE.md`](../SYSTEM_ARCHITECTURE.md) and [`docs/ai-workflow/`](../ai-workflow/).

## 1. System view (Architecture B)
```mermaid
flowchart TB
  subgraph EXT[External]
    PSU[5 V DC supply]
    PC[USB host / charger]
    US[Ultrasonic module 5 V]
    I2CDEV[I²C module 3.3 V]
    UARTDEV[UART device]
    GPDEV[3.3 V GPIO device]
  end
  subgraph DK[ESP32 DevKit - separate board]
    ESP[ESP32-WROOM-32E<br/>own 3.3 V regulator]
  end
  subgraph BOARD[This board - Rev A]
    J1[J1 power in] --> U5[U5 TPS26600 eFuse]
    U5 -->|+5V_P| U1[U1 TLV1117LV33 LDO]
    U1 -->|+3V3_P| PERIPH[J4 / J5 / J6 supply pins]
    U5 -->|+5V_P| J3[J3 ultrasonic]
    J2[J2 ESP32 interface] --> COND[Signal conditioning<br/>U2 · U3 · U4 · series R]
    COND --> J3
    COND --> J4[J4 UART]
    J2 --> J5[J5 I²C]
    J2 --> J6[J6 GPIO]
  end
  PSU --> J1
  PC -->|USB| ESP
  ESP <-->|12 wires| J2
  J3 <--> US
  J5 <--> I2CDEV
  J4 <--> UARTDEV
  J6 <--> GPDEV
```

## 2. Power domains
| Domain | Source | Supplies | Notes |
|---|---|---|---|
| VIN_RAW | J1 (5 V ±5 %) | U5 input only | Unprotected side of the eFuse |
| +5V_P | U5 OUT | U1 input, J3 VCC, U3 VCCB (5 V side), LED1 | Protected 5 V |
| +3V3_P | U1 | J4 VCC (JP1 default), J5-2, J6-2, LED2 | ≤ 250 mA at ≤ 50 °C |
| 3V3_ESP | DevKit 3V3 pin via J2-1 | U2, U4, U3 VCCA, I²C pull-ups, UART RX pull-up | Logic reference only, ≤ 3.4 mA |
| EF_RTN | U5 RTN | UVLO/OVP divider, ILIM, dVdT, U5 PowerPAD | Isolated island, **not GND** |
| GND | J1-2, J2-2/11/12 | everything else | Common with the DevKit and USB host |

`+3V3_P` and `3V3_ESP` never share a node (checked by the netlist verifier).

## 3. Signal conditioning
```mermaid
flowchart LR
  G26[GPIO26 3.3 V] --> U3["U3 SN74LVC1T45<br/>A: VCCA = 3V3_ESP<br/>B: VCCB = +5V_P<br/>DIR = A→B"] --> R15[R15 1 kΩ] --> TRIG[J3-2 TRIG 5 V]
  ECHO[J3-3 ECHO 0–5 V] --> R6[R6 1 kΩ<br/>R7 100 kΩ to GND] --> U2["U2 SN74LVC1G17<br/>VCC = 3V3_ESP<br/>5.5 V-tolerant input"] --> G34[GPIO34]
  G17[GPIO17 TX] --> R10[R10 220 Ω] --> J43[J4-3 TX]
  J44[J4-4 RX 3.3/5 V] --> R11[R11 1 kΩ<br/>R12 100 kΩ to 3V3_ESP] --> U4[U4 SN74LVC1G17] --> G16[GPIO16 RX]
  G21[GPIO21/22] ---|2.2 kΩ pull-ups via JP2| J5S[J5 SDA/SCL]
  G32[GPIO32/33] ---|R13/R14 1 kΩ| J6S[J6 IO1/IO2 3.3 V only]
```
R4 and R5 (100 kΩ) hold TRIG low on both sides of U3 while the ESP32 is in reset or unpowered.
