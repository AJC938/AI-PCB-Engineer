# Design Brief — Sensor Interface & Power Management Board for ESP32 (V0.1.0)

Status: **Phase 1 draft: requirements and planning only.** No schematic, PCB or component selection exists.

## Product concept
An external companion PCB that sits between an ESP32 development board and common hobby or lab sensors.
It provides:
- a protected 5 V input with reverse-polarity and overcurrent protection,
- organised 5 V and 3.3 V peripheral power rails with status indication and test points,
- a dedicated, level-safe interface for an HC-SR04-class ultrasonic sensor,
- labelled I2C and UART connectors (and optionally one general-purpose sensor connector),
- a clearly documented, pin-exact mapping to one specific ESP32 development board.

## Intended users and use cases
| User | Use case |
|---|---|
| Engineering student / maker (primary) | Build sensor prototypes without breadboard wiring errors, back-feeding, or 5 V-into-3.3 V damage |
| The project owner (portfolio) | Demonstrate a full, traceable PCB engineering cycle from requirements to tested hardware |
| Lab / teaching bench | Repeatable sensor set-ups with known power limits and measurable test points |

Typical scenarios: distance measurement (HC-SR04), environmental sensing over I2C, a GPS or
serial sensor over UART, and logging or Wi-Fi telemetry on the ESP32.

## Scope (V0.1.0)
- Requirements, architecture options, power budget, interface specification, risk register,
  component selection plan, verification plan, open questions (this phase).
- Later V0.1.x phases: component selection with datasheets, schematic, layout, fabrication outputs,
  assembly, bring-up and measured validation.

## Out of scope (V0.1.0)
- Firmware beyond simple bring-up and test sketches.
- Battery power, charging and power-path management for batteries.
- Wireless design (the ESP32 module and its antenna belong to the development board).
- Mains-powered or > 5 V inputs. Isolated interfaces. Automotive or industrial ratings.
- 5 V-logic I2C/UART devices without an explicit level translator (decision pending, see OQ-09).
- Enclosure design (only mechanical clearances are considered).
- Certification (EMC/CE/FCC) testing.
- Purchasing, fabrication orders and assembly services (each needs separate approval).

## Key constraints
- The ESP32 GPIOs are **not 5 V tolerant**: VIH(max) = VDD + 0.3 V, per Espressif REF-01/REF-02.
- The ESP32-DevKitC accepts **one and only one** power source at a time (REF-03).
- ESP32 module supply capability ≥ 0.5 A with 379 mA TX peaks (REF-02).
- HC-SR04 electrical data is **secondary-source only**. Module variants differ (REF-06).
- The exact ESP32 development board is **not yet chosen** (OQ-01). No pin assignment is final.

Related documents: [REQUIREMENTS_MATRIX](REQUIREMENTS_MATRIX.md), [BLOCK_DIAGRAM](BLOCK_DIAGRAM.md),
[INTERFACE_SPEC](INTERFACE_SPEC.md), [POWER_BUDGET](POWER_BUDGET.md), [RISK_REGISTER](RISK_REGISTER.md),
[COMPONENT_SELECTION_PLAN](COMPONENT_SELECTION_PLAN.md), [VERIFICATION_PLAN](VERIFICATION_PLAN.md),
[OPEN_QUESTIONS](OPEN_QUESTIONS.md), [PHASE_1_SUMMARY](PHASE_1_SUMMARY.md).
