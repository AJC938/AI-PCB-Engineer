# V0.1.0 Phase 1 Summary — Requirements & Design Planning

Date: 2026-11-08 · Branch: `design/v0.1.0-phase1` (from `v0.0.3-rc1`) · No schematic, PCB, MPN or order.

## Completed
| Item | Where |
|---|---|
| Product scope, users, out-of-scope list | DESIGN_BRIEF.md |
| 52 requirements (PWR 16, ESP 7, US 6, I2C 4, UART 3, GP 1, MECH 5, MFG 6, USE 4), with priority and verification method | REQUIREMENTS_MATRIX.md |
| System, power and signal block diagrams (voltage domains separated) | BLOCK_DIAGRAM.md |
| Interface tables for power, DevKit, ultrasonic, I2C, UART, GP and test points. Echo/Trigger option analysis | INTERFACE_SPEC.md |
| Power budget for two architectures. LDO vs buck losses. Reverse-polarity drop. Back-feed analysis | POWER_BUDGET.md |
| 22 risks with scores and mitigations | RISK_REGISTER.md |
| Component categories with datasheet verification items and criteria (no MPNs) | COMPONENT_SELECTION_PLAN.md |
| Design, assembly, power and signal verification with acceptance criteria | VERIFICATION_PLAN.md |
| 18 open questions: 13 blocking (3 of them only for a given architecture), 1 partly, 4 non-blocking | OPEN_QUESTIONS.md |
| Reproducible calculations | `calculations/v0.1.0/phase1_calcs.py` (+ output) |
| Reference index (official vs secondary) | `datasheets/index_v0.1.0.md` |

## Key engineering findings
1. **ESP32 GPIOs are not 5 V tolerant** (VIH max = VDD + 0.3 V, Espressif REF-01/REF-02). Every
   sensor-side signal needs a defined conditioning path.
2. **The Echo divider is fragile.** It satisfies the limits only if Echo HIGH ≈ 4.75–5.25 V. The window is 0.6 V
   at the VDD extremes, and it fails for 3.3 V-output modules. A 5 V-tolerant buffer is the robust alternative.
3. **Trigger compatibility is unknown.** The ESP32's VOH(min) of 2.64 V passes a TTL threshold but would fail a
   5 V-CMOS threshold. HC-SR04 data exists only from secondary sources, and variants differ.
4. **Espressif mandates a single power source for the DevKitC** (REF-03). This drives the architecture choice:
   Architecture B (DevKit on USB) is safe by construction at about 274 mA input. Architecture A (board powers
   DevKit) needs about 774 mA and an enforced exclusivity mechanism.
5. **ESP32 supply capability ≥ 0.5 A with 379 mA TX peaks** (REF-02) dominates Arch. A sizing.
6. At the 150 mA 3.3 V planning budget a linear regulator dissipates about 0.29 W (VIN 5.25 V). This is acceptable
   in principle, pending the real RthJA and ambient.
7. **I2C:** Rp(min) 967 Ω at 3.3 V. Fast-mode is infeasible at 400 pF. Bus capacitance must be estimated.

## Unresolved
Blocking open questions: OQ-01 (exact DevKit), OQ-02 (DevKit power path), OQ-03 (dimensions),
OQ-04/05 (input source and tolerance), OQ-06 (architecture), OQ-07 (I2C devices), OQ-10 (mounting),
OQ-11 (ultrasonic module), OQ-12/14 (back-power analysis), OQ-15 (ambient), OQ-16 (fab and assembly).
No requirement is yet **Confirmed** by the owner.

## Design-freeze readiness
**Not ready for design freeze.** Phase 1 is **ready for review**: every completion criterion in the brief
is met in planning form, with no unsupported assumption presented as fact. Every ASSUMED or SECONDARY
value is tagged. Freeze requires the owner's answers to the blocking questions, then component
selection with official datasheets (Phase 2).

## Recommended next steps
1. Owner review: answer OQ-01, OQ-04, OQ-06, OQ-10, OQ-11 first. These unblock most of the others.
2. Retrieve the chosen DevKit's schematic and dimension drawing (OQ-02/03).
3. Obtain the ultrasonic module sample and characterise Echo HIGH and Trigger threshold on the bench
   (current-limited, DevKit not connected).
4. Then Phase 2: component shortlists and selection per COMPONENT_SELECTION_PLAN.
