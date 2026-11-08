# Interface Specification — V0.1.0 (planning)

Connector part numbers, pitch and orientation are **not selected** (COMPONENT_SELECTION_PLAN). Pin orders
below are proposals for review. GPIO numbers are **placeholders** until ESP-01 (exact DevKit) is resolved.

## 1. Power input (J_PWR)
| Pin | Signal | Level | Notes |
|---|---|---|---|
| 1 | VIN+ | 5.0 V nominal (tolerance TBD, OQ-05) | Keyed connector, polarity on silkscreen (PWR-02) |
| 2 | GND | 0 V | |
Connector type (terminal block, barrel jack, or USB-C power-only) is TBD (OQ-04). Its current rating
must exceed the final input budget with margin.

## 2. ESP32 development board interface (J_ESP)
Reference candidate for documentation only: **ESP32-DevKitC V4** (REF-03), 2 × 19-pin headers J2/J3.
**Not selected**: OQ-01.

| Board signal | DevKit pin (DevKitC V4 reference) | Direction | Domain | Notes |
|---|---|---|---|---|
| GND | J2-14, J3-1, J3-7 (REF-03) | — | GND | Use all available GND pins for low impedance |
| DevKit 5V | J2-19 (REF-03) | power in to DevKit | 5 V | Connected only in Arch. A (`L_DEVKIT_5V`) |
| DevKit 3V3 | J2-1 (REF-03) | — | 3.3 V | **Not connected to `+3V3_P`** (PWR-08). Possible use as a reference only (OQ-12) |
| US_ECHO | GPIO TBD (input-only pins 34/35/36/39 suitable, ESP-05) | in | 3.3 V after conditioning | ESP-03, US-04 |
| US_TRIG | GPIO TBD (not strapping, not input-only) | out | 3.3 V | US-05 |
| I2C_SDA / I2C_SCL | GPIO TBD | bidir / out (open-drain) | 3.3 V | ESP32 I2C pins are routable via the GPIO matrix. Choose non-strapping pins |
| UART_TX / UART_RX | GPIO TBD (avoid UART0, used by the USB bridge on DevKits) | out / in | 3.3 V | |
| GP_IO1/IO2 | GPIO TBD (≥1 ADC-capable) | in/out | 3.3 V | Could (GP-01) |
Excluded: GPIO6–11 (flash, REF-03). GPIO16/17 if a WROVER variant is chosen (REF-03). Strapping pins
are analysed against REF-01's strapping table before assignment (ESP-04).

## 3. Ultrasonic connector (J_US): HC-SR04 class
| Pin | Signal | Level | Notes |
|---|---|---|---|
| 1 | VCC | `+5V_P` (classic variant) or `+3V3_P` (if a 3.3 V-capable variant is chosen) | US-03. Rail selection TBD (OQ-11) |
| 2 | TRIG | ESP32 output, VOH ≥ 0.8·VDD = 2.64 V at 3.3 V (REF-01) | Sensor VIH UNVERIFIED. Translator may be needed (US-05) |
| 3 | ECHO | sensor output, HIGH level UNVERIFIED (secondary: about 5 V TTL on classic types) | Conditioned before the GPIO (US-04) |
| 4 | GND | 0 V | |
Pin order follows the common module header order VCC-TRIG-ECHO-GND (secondary sources). Confirm on the chosen module.

### Echo conditioning options
| Option | Principle | Pros | Cons / conditions |
|---|---|---|---|
| E1 Resistor divider (ratio about 0.60) | Passive attenuation | Simple, no supply needed | Works only if Echo HIGH ≈ 4.75–5.25 V. Window 0.6 V wide at the VDD extremes. Wrong for 3.3 V-output modules. Can back-power an unpowered ESP32 |
| E2 5 V-tolerant-input logic buffer powered from the ESP32's 3.3 V | Active translation | Defined output levels, independent of Echo amplitude above its VIH | One IC. Input tolerance and power-off (Ioff) behaviour must be confirmed in its datasheet |
| E3 Bidirectional MOSFET or translator IC | Translation | Common in modules | Overkill for a unidirectional signal |
Calculated example (E1): 2.0 kΩ / 3.0 kΩ at 1 % gives 2.827–3.175 V for Echo 4.75–5.25 V,
inside [2.70, 3.30] V (the conservative window) (`phase1_calcs_output.txt` §2). **Selection is deferred until the
module's Echo level is known (OQ-11).**

### Trigger options
| Option | Condition |
|---|---|
| T1 Direct GPIO drive | Acceptable only if the sensor's VIH ≤ about 2.3 V with margin (to be measured or documented) |
| T2 3.3→5 V translator with TTL-compatible input, powered from `+5V_P` | Required if the sensor input is CMOS-at-5 V (VIH about 3.5 V would fail) |

## 4. I2C connector (J_I2C)
| Pin | Signal | Level |
|---|---|---|
| 1 | GND | 0 V |
| 2 | VCC | `+3V3_P` |
| 3 | SDA | 3.3 V open-drain |
| 4 | SCL | 3.3 V open-drain |
Order proposal: GND-VCC-SDA-SCL. Final order is chosen to match the intended sensor modules (OQ-07).
Several incompatible conventions exist, so the silkscreen is mandatory.
Pull-ups (I2C-03): Rp(min) = 967 Ω at 3.3 V / 3 mA. Rp(max) = 3.5 kΩ (Fast-mode, Cb 100 pF) to 11.8 kΩ
(Standard-mode, Cb 100 pF) per REF-04. Fast-mode is infeasible at the 400 pF limit (885 Ω < 967 Ω).
Cb must be estimated from cable length and devices (OQ-07). Pull-up reference rail: OQ-12.

## 5. UART connector (J_UART)
| Pin | Signal | Direction | Level |
|---|---|---|---|
| 1 | GND | — | 0 V |
| 2 | VCC | out | `+3V3_P` default. `+5V_P` option (UART-02) |
| 3 | TX | ESP32 → device | 3.3 V |
| 4 | RX | device → ESP32 | must stay ≤ VDD + 0.3 V |
"TX" and "RX" are named from the ESP32 side, so the device's RX connects to pin 3.

## 6. General-purpose connector (J_GP, Could)
`GND, +3V3_P, GP_IO1 (ADC-capable), GP_IO2`. Included only if a concrete sensor justifies it (OQ-13).

## 7. Test points
`TP_VIN`, `TP_5V`, `TP_3V3`, `TP_GND1`, `TP_GND2`, and optionally `TP_ECHO_GPIO` (post-conditioning) and `TP_TRIG`.
