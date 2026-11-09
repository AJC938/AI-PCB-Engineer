# Physical Validation Status

## Status: **DIGITALLY VALIDATED DESIGN — NOT PHYSICALLY FABRICATED OR TESTED**

As of release v1.0.0 (2026-11-09): no board has been manufactured, assembled, powered or measured. The
`testing/` folder contains no test records. Every "PASS" in this repository is a digital result (ERC, DRC,
netlist checks, calculations, file audits). **No physical test below has been performed, and none is marked PASS.**

## Future test plan (bring-up order)
Equipment: current-limited bench supply (isolated outputs), DMM, oscilloscope (≥ 20 MHz), thermocouple or
IR thermometer, ESP32 DevKit with USB, an HC-SR04-style 5 V module, an I²C module and a UART device.
Record every result with date, board serial, instrument and photos in `testing/v1.0.0/`.

| # | Test | Procedure (summary) | Pass criterion (design value) | Status |
|---|---|---|---|---|
| T1 | Visual inspection | Check every part against the BOM, polarity of U1–U5, LEDs and pin 1 of J1–J6 against the assembly drawing; check solder joints of THT parts and the U5 exposed pad (X-ray if available) | No missing, misplaced or reversed parts | NOT TESTED |
| T2 | Short-circuit inspection | Unpowered: resistance VIN_RAW–GND, +5V_P–GND, +3V3_P–GND, 3V3_ESP–GND | No low-ohm path (expect ≥ kΩ class after capacitor charge) | NOT TESTED |
| T3 | Input voltage verification | Supply 5.00 V, limit 0.3 A, nothing connected. Measure TP1, TP2, TP3; input current | TP2 ≈ VIN − ≤ 0.07 V; TP3 3.3 V ±2 %; quiescent current a few mA; LED1 and LED2 on | NOT TESTED |
| T4 | OVP threshold | Slowly raise VIN (≤ 0.1 V/s) from 5.0 V until TP2 drops; then lower until it returns | Trip 5.39–5.82 V; release 5.00–5.35 V | NOT TESTED |
| T5 | UVLO threshold | Raise VIN slowly from 0 V; note turn-on; lower to note turn-off | On 4.25–4.56 V; off 3.91–4.19 V | NOT TESTED |
| T6 | Current-limit behaviour | Electronic load on TP2/GND (or on J3 +5V), step 0.3 → 0.8 A with supply limit 1 A | Output current limited at 0.51–0.69 A; thermal shutdown and auto-retry; no damage | NOT TESTED |
| T7 | Reverse polarity (controlled) | **Isolated** supply, nothing else connected to the board (no ESP32, no USB, no earthed probe ground), limit 0.1 A, apply −5 V to J1 for ≤ 10 s | Supply current ≈ 0 (leakage only); TP2 = 0 V; board works normally afterwards (repeat T3) | NOT TESTED |
| T8 | 3.3 V LDO output | Load +3V3_P with 0, 100, 250 mA | 3.3 V within regulator tolerance at all loads | NOT TESTED |
| T9 | LDO temperature | 250 mA on +3V3_P, VIN 5.25 V, 30 min, note ambient | Tab temperature consistent with Tj ≤ 110 °C at 50 °C ambient (CALCULATED 94.7 °C) | NOT TESTED |
| T10 | TRIG output | ESP32 on; drive GPIO26 with 10 µs pulses; probe TP8 and J3-2 | 0 V / ≥ 4.5 V levels, clean edges, low at ESP32 reset | NOT TESTED |
| T11 | ECHO input | Feed 0/5 V pulses into J3-3 from a generator through 1 kΩ; probe TP7 | TP7 0 / 3.3 V, delay < 1 µs class | NOT TESTED |
| T12 | I²C | Connect a 3.3 V I²C module on J5; run an I²C scan at 100 and 400 kHz | Device found; rise time within the I²C limit for the mode | NOT TESTED |
| T13 | UART | Loop back J4-3 to J4-4; send and receive at 115200 baud | Error-free loop-back | NOT TESTED |
| T14 | ESP32 integration | Full wiring per the connection guide; power-up order R-31; check no back-feed with the board off (measure +3V3_P) | All functions work; back-feed within the documented bounds | NOT TESTED |
| T15 | Ultrasonic functionality | HC-SR04-style module wired by labels; measure known distances 10–200 cm | Distance readings consistent with the module's specification | NOT TESTED |

**Do not perform uncontrolled destructive tests.** In particular: never apply reverse polarity with the ESP32,
a USB host or an earthed oscilloscope ground connected to the board GND (see
[SAFETY_AND_POWER.md](../safety/SAFETY_AND_POWER.md) §3). Never exceed 50 V at J1. Always use a current-limited supply.

When a test is done, update this table with the result and a link to the evidence in `testing/`. Only results
with recorded evidence may be marked PASS.
