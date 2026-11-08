# Requirements Matrix — V0.1.0

Priority: **Must / Should / Could** · Status: **Proposed** (engineering proposal, awaiting owner review) ·
**Confirmed** (accepted by the owner, none yet) · **TBD** (cannot be written until an open question is answered).
Verification: **I** = inspection (design files, BOM, silkscreen) · **A** = analysis or calculation ·
**T** = bench test with a recorded measurement · **D** = demonstration.
References: REF-xx = `datasheets/index_v0.1.0.md`, OQ-xx = `OPEN_QUESTIONS.md`.

## 1. Electrical: power
| ID | Requirement | Rationale | Pri | Verif. | Status |
|---|---|---|---|---|---|
| PWR-01 | The board shall accept a 5 V DC input. Nominal 5.0 V. Operating tolerance to be defined (planning assumption ±5 %) | Product concept. Tolerance drives every downstream margin | Must | T | Proposed (tolerance TBD, OQ-05) |
| PWR-02 | The input connector shall be polarised or keyed, with polarity marked on the silkscreen | Prevents the most likely wiring error | Must | I | Proposed |
| PWR-03 | A reversed input up to the maximum input voltage shall cause no damage, and no reversed voltage shall appear on any rail or connector | Concept requirement. Bench supplies get reversed | Must | T (current-limited reversed input) | Proposed |
| PWR-04 | The input shall have overcurrent protection rated from the final power budget (planning basis about 0.35 A for Arch. B, about 1.0 A for Arch. A) | Limits damage from shorted peripheral cables | Must | A + T | Proposed (rating TBD, OQ-04) |
| PWR-05 | The input should have transient/ESD protection appropriate for an external DC lead | External cables carry ESD and hot-plug transients | Should | A + I | Proposed (level TBD) |
| PWR-06 | The board shall provide a protected 5 V peripheral rail (`+5V_P`) downstream of all input protection | Concept requirement | Must | T | Proposed |
| PWR-07 | The board shall provide a regulated 3.3 V peripheral rail (`+3V3_P`) generated on the board from `+5V_P` | Concept requirement. Keeps peripheral load off the DevKit regulator | Must | T | Proposed |
| PWR-08 | `+3V3_P` shall **not** be connected to the DevKit 3V3 pin. Any shared reference (e.g. I2C pull-ups) requires a documented analysis | Avoids two regulators driving one node and back-feeding the DevKit (REF-03) | Must | I + A | Proposed |
| PWR-09 | The power design shall comply with REF-03: the DevKit receives power from **one source only** at any time | Espressif warns of damage otherwise | Must | I + A + T | Proposed |
| PWR-10 | The power architecture (A, B, or selectable) shall be chosen and documented before schematic capture | Determines current budget, protection ratings and back-feed risks | Must | I | **TBD (OQ-06)** |
| PWR-11 | `+3V3_P` regulator: steady-state dissipation and junction temperature at maximum load and maximum ambient shall be within the selected part's ratings with documented margin | Thermal safety | Must | A + T | Proposed |
| PWR-12 | `+3V3_P` shall supply at least the 3.3 V load budget (planning 150 mA) | I2C and GP sensors | Must | A + T | Proposed (value TBD, OQ-07/OQ-08) |
| PWR-13 | Rail accuracy and ripple targets for `+5V_P` and `+3V3_P` shall be defined from the connected devices' requirements | Sensor supply limits | Should | T | TBD |
| PWR-14 | A power-good indicator LED for `+5V_P`, and preferably for `+3V3_P` | Concept requirement | Must (5V) / Should (3V3) | D | Proposed |
| PWR-15 | Test points: `VIN` (before protection), `+5V_P`, `+3V3_P`, and at least two `GND` points | Concept requirement. Enables bring-up measurements | Must | I + T | Proposed |
| PWR-16 | A single ground reference shared by board and DevKit, with a defined return path for sensor currents (no signal returns through thin or shared high-current paths) | Signal integrity and threshold margins | Must | I (layout review) | Proposed |

## 2. Electrical: ESP32 interface
| ID | Requirement | Rationale | Pri | Verif. | Status |
|---|---|---|---|---|---|
| ESP-01 | One exact ESP32 development board (vendor, model, revision, module variant) shall be selected and its official pinout document recorded | Pinouts differ between DevKits | Must | I | **TBD (OQ-01)** |
| ESP-02 | The mechanical connection method (DevKit plugged into board sockets, or cable/harness) shall be defined | Drives connectors, size and antenna keep-out | Must | I | TBD (OQ-10) |
| ESP-03 | No ESP32 GPIO shall see a voltage above VDD + 0.3 V or below −0.3 V in any supported configuration, including power-up and power-down sequences | REF-01 Table 5-3 / REF-02 Table 15 | Must | A + T | Proposed |
| ESP-04 | Signals shall not be assigned to flash pins (GPIO6–11). Strapping pins shall be avoided or analysed against the boot-mode table | REF-03. Boot reliability | Must | I | Proposed (strapping table extraction pending) |
| ESP-05 | Input-only pins (GPIO34/35/36/39 on ESP32-DevKitC) shall be used only for inputs | REF-03 | Must | I | Proposed |
| ESP-06 | A pin-assignment table (function → GPIO → DevKit header pin) shall be published and cross-checked against the official pinout | Traceability | Must | I | TBD (after ESP-01) |
| ESP-07 | Per-pin and cumulative GPIO source/sink currents shall stay within REF-01 Table 5-1/5-3 | Device limits | Must | A | Proposed |

## 3. Electrical: ultrasonic interface
| ID | Requirement | Rationale | Pri | Verif. | Status |
|---|---|---|---|---|---|
| US-01 | A dedicated 4-position connector `VCC, TRIG, ECHO, GND`, each pin labelled on the silkscreen with the supply voltage | Concept requirement | Must | I | Proposed |
| US-02 | The exact sensor module (vendor/variant) shall be selected, and its supply range, Echo HIGH level and Trigger threshold obtained from its vendor document **or measured** | Variants differ. Only secondary data exists (REF-06) | Must | I + T | **TBD (OQ-11)** |
| US-03 | The sensor shall be supplied from the rail its variant requires (5 V for "classic" types per secondary data) | Range and function | Must | A + T | TBD (after US-02) |
| US-04 | Echo conditioning shall keep the GPIO voltage within [0.75·VDD, VDD + 0.3 V] for a HIGH and ≤ 0.25·VDD for a LOW, across sensor-supply and resistor tolerances | ESP-03. Valid logic levels | Must | A + T (scope at GPIO) | Proposed |
| US-05 | Trigger drive shall exceed the sensor's VIH with margin, or a level translator shall be used | 2.64 V VOH(min) may be below a 5 V CMOS threshold | Must | A + T | TBD (after US-02) |
| US-06 | Echo conditioning shall not inject current into an unpowered ESP32 beyond what its documentation allows (relevant to Arch. B) | Back-powering through IO protection structures | Should | A | Proposed (ESP32 injection limit not found yet, OQ-14) |

## 4. Electrical: I2C, UART, general-purpose
| ID | Requirement | Rationale | Pri | Verif. | Status |
|---|---|---|---|---|---|
| I2C-01 | A 4-position I2C connector `GND, VCC, SDA, SCL` (order proposed, see INTERFACE_SPEC), labelled with its supply voltage | Concept requirement | Must | I | Proposed |
| I2C-02 | I2C logic level 3.3 V and connector supply `+3V3_P`. 5 V-logic I2C devices are unsupported without a translator | ESP-03 | Must | I + A | Proposed |
| I2C-03 | On-board pull-ups on SDA/SCL, sized within UM10204 limits for the chosen mode and bus capacitance, disconnectable (e.g. solder jumper) | REF-04. Modules often carry their own pull-ups | Should | A + T (rise time) | Proposed |
| I2C-04 | The pull-up reference rail shall be chosen so that no GPIO is pulled above VDD + 0.3 V when the ESP32 is unpowered | ESP-03 with independent supplies | Must | A | TBD (OQ-12) |
| UART-01 | A 4-position UART connector `GND, VCC, TX, RX`. TX/RX named from the ESP32 side and stated on the silkscreen | Avoids crossed-line ambiguity | Must | I | Proposed |
| UART-02 | UART logic level 3.3 V. Connector supply `+3V3_P` by default, with `+5V_P` optional only when the device accepts 3.3 V logic | ESP-03 | Must | I + A | Proposed (device TBD, OQ-08) |
| UART-03 | Series resistors on UART lines for fault limiting | Robustness on external cables | Could | A | Proposed |
| GP-01 | Optional general-purpose connector: `GND, +3V3_P, 1–2 GPIO` (at least one ADC-capable) | Adds value only if a concrete sensor needs it | Could | I | TBD (OQ-13) |

## 5. Mechanical
| ID | Requirement | Rationale | Pri | Verif. | Status |
|---|---|---|---|---|---|
| MECH-01 | Board outline defined only after the DevKit, connection method and connector set are fixed | Concept constraint | Must | I | TBD |
| MECH-02 | Connectors placed on board edges, with documented clearance for mating plugs and cable bend | Usability | Should | I (3D review) | Proposed |
| MECH-03 | If the DevKit is mounted over the board, no copper or tall parts under its antenna region (keep-out per the DevKit or module documentation) | RF performance | Must (if stacked) | I | TBD (OQ-10, OQ-03) |
| MECH-04 | Mounting holes (M3 planning assumption) away from copper and connectors | Mounting | Should | I | Proposed |
| MECH-05 | Through-hole connectors for anything mated by hand | Mechanical robustness | Should | I | Proposed |

## 6. Manufacturing
| ID | Requirement | Rationale | Pri | Verif. | Status |
|---|---|---|---|---|---|
| MFG-01 | 2-layer FR-4. Thickness and copper weight chosen after manufacturer review (planning 1.6 mm, 1 oz) | Cost, availability | Must | I | Proposed |
| MFG-02 | The selected manufacturer's design rules recorded (source, date) and applied before layout release | ENGINEERING_RULES §7 | Must | I | TBD (OQ-16) |
| MFG-03 | SMD passives in a hand-solderable size unless PCBA is chosen | Assembly method | Should | I | TBD (OQ-16) |
| MFG-04 | Reference designators, polarity marks (LEDs, input, diodes) and pin-1 marks on the silkscreen | Assembly correctness | Must | I | Proposed |
| MFG-05 | Every BOM line has an MPN with a traceable datasheet and an approval justification before release | ENGINEERING_RULES §1, §9 | Must | I | Proposed |
| MFG-06 | ERC 0 and DRC 0 (with schematic parity) via kicad-cli. Every exclusion justified in writing | Workflow rules | Must | T (tool) | Proposed |

## 7. Usability and documentation
| ID | Requirement | Rationale | Pri | Verif. | Status |
|---|---|---|---|---|---|
| USE-01 | Every connector labelled with its signal names and supply voltage | Concept requirement | Must | I | Proposed |
| USE-02 | Test points reachable with standard probes while the DevKit and cables are fitted | Bring-up | Must | I (3D review) | Proposed |
| USE-03 | A printed or README pin-map card for the board ↔ DevKit ↔ sensor wiring | Usability | Should | I | Proposed |
| USE-04 | Visible power indicator(s), not hidden under the DevKit | Usability | Should | I | Proposed |

**Assumptions (not requirements):** ±5 % input tolerance, 150 mA 3.3 V budget, 100 mA UART budget,
20 mA HC-SR04 allocation, M3 holes, 1.6 mm / 1 oz board. Each is tagged ASSUMED in
`calculations/v0.1.0/phase1_calcs.py` and listed in OPEN_QUESTIONS.
