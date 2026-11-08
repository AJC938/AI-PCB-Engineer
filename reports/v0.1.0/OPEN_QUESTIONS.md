# Open Questions — V0.1.0 resolution register

Source list: [`docs/requirements/v0.1.0/OPEN_QUESTIONS.md`](../../docs/requirements/v0.1.0/OPEN_QUESTIONS.md)
(Phase 1, OQ-01…OQ-18). This file records how each one was handled in the V0.1.0 design, plus the
new questions that came up during design (NQ-xx).

Status: **RESOLVED** (evidence-based) · **RESOLVED-DESIGN** (a stated design limit the owner can change) ·
**MITIGATED** (design no longer depends on the answer, a residual remains) · **OPEN**.

## Phase 1 questions
| ID | Topic | Status | Resolution | Source |
|---|---|---|---|---|
| OQ-01 | Exact ESP32 board | RESOLVED (reference) | ESP32-DevKitC V4 with ESP32-WROOM-32(E) is the documented reference. The user's 38-pin USB-C/CP2102 clone is treated as "DevKitC-compatible". The interface uses only GPIO numbers + 3V3 + GND, so clone pin **positions** do not affect the schematic | DDR-13, DS-01/02 |
| OQ-02 | DevKit VBUS / 5V pin / regulator | MITIGATED | Architecture B: the DevKit 5V pin is **not wired**, so the VBUS path no longer matters. Residual: the clone 3V3 pin must source ≤ 3.4 mA (NQ-04) | DDR-01, POWER_ARCHITECTURE.md |
| OQ-03 | DevKit dimensions / antenna | OPEN (non-blocking for V0.1.0) | Option B (cable) chosen, so no outline is needed now. Needed only for future Option A (stacked) | DDR-14 |
| OQ-04 | 5 V source and connector | RESOLVED-DESIGN | Regulated 5 V supply ≥ 0.5 A, screw terminal Phoenix 1715721 (5.08 mm) | DS-14, POWER_BUDGET_FINAL.md |
| OQ-05 | Input tolerance | RESOLVED-DESIGN | 5 V ±5 % (4.75–5.25 V). Reverse polarity blocked (Q1). TVS VWM 6.0 V. **Not** an overvoltage-protected input (R-32) | DS-03/05 |
| OQ-06 | Power architecture | RESOLVED | **B** (DevKit on its own USB) | DDR-01 |
| OQ-07 | I2C devices | RESOLVED-DESIGN | Connector rating 100 mA from `+3V3_P`. 2.2 kΩ pull-ups to 3V3_ESP (JP2 disconnectable). Fast-mode to 159 pF, Standard-mode to 400 pF | DDR-11, `design_calcs.py` |
| OQ-08 | UART devices | RESOLVED-DESIGN | 100 mA. VCC 3.3 V (default) or 5 V via JP1. RX accepts 3.3 V or 5 V logic. TX is 3.3 V CMOS through 220 Ω | DDR-12 |
| OQ-09 | 5 V logic I2C/UART | RESOLVED | Unsupported, except UART RX, which accepts 5 V | DDR-12 |
| OQ-10 | Stacked vs cable | RESOLVED | Cable (Option B) for V0.1.0 | DDR-14 |
| OQ-11 | Ultrasonic module | RESOLVED | Adafruit 4007 recommended. The interface (5 V supply, 5 V TRIG, 5.5 V-tolerant ECHO buffer) also works with classic 5 V HC-SR04 modules | DDR-03…06 |
| OQ-12 | I2C pull-up reference | RESOLVED | 3V3_ESP | DDR-11 |
| OQ-13 | GP connector | RESOLVED | Included: 1×4 (+3V3_P, GND, GPIO32, GPIO33) with 1 kΩ series resistors | DDR-13 |
| OQ-14 | Unpowered ESP32 injection limit | MITIGATED | Echo/RX via Ioff buffers powered from 3V3_ESP. TRIG translator A side Ioff. Residual on GP lines ≤ 2.75 mA through 1 kΩ (R-04). Espressif publishes no limit | DS-07/08, calc |
| OQ-15 | Ambient / environment | RESOLVED-DESIGN | 50 °C max indoor bench (LDO Tj 81.8 °C. Sensitivity in POWER_BUDGET_FINAL) | `design_calcs.py` |
| OQ-16 | Fab and assembly | **OPEN — needed before V0.2.0 layout rules** | Owner decision. No order is placed | — |
| OQ-17 | Quantity / budget | OPEN (non-blocking) | Owner decision | — |
| OQ-18 | ESD arrays on signal connectors | RESOLVED-DESIGN (deferred) | Not fitted in V0.1.0. Series resistors (ECHO 1 kΩ, RX 1 kΩ, TX 220 Ω, GP 1 kΩ) limit injected current. TRIG is a translator output. Revisit in V0.2.0 if space allows | R-11 |

## New questions raised during design
| ID | Question | Blocks | How to resolve |
|---|---|---|---|
| NQ-01 | Pin order of the purchased ultrasonic module (Adafruit does not publish pin names) | Wiring/silkscreen of J3 (VCC/TRIG/ECHO/GND assumed) | Inspect the physical module. Adjust J3 silkscreen in V0.2.0 if needed |
| NQ-02 | Real Echo HIGH / Trigger threshold of the purchased module | Nothing (variant-independent design). Verification only | Scope measurement (VERIFICATION_PLAN) |
| NQ-03 | Exact clone pinout (which header pin is GPIO26, 34, 21, 22, 17, 16, 32, 33, 3V3, GND) | Wiring harness only | Read the clone's silkscreen. Fill the wiring table in V0.2.0 |
| NQ-04 | Can the clone 3V3 pin source 3.4 mA extra? | Low risk (AMS1117-class regulators, ≥ 500 mA typical) | Measure the 3V3_ESP voltage with the board attached |
| NQ-05 | SMAJ6.0A band vs footprint pad 1 | Assembly drawing | Compare with the Vishay package drawing during V0.2.0 |
| NQ-06 | 10 µF X5R DC-bias derating (Samsung page has no curve) | Confirm the effective capacitance still meets the DS-06 output-capacitor requirement (ASSUMED met: 10 µF nominal) | Use the Samsung characterisation tool or a part with a published curve |
| NQ-07 | Fabrication design rules (track/space, drill, mask) | V0.2.0 DRC setup | = OQ-16 |
