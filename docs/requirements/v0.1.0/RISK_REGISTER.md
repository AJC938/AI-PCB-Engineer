# Risk Register — V0.1.0 (Phase 1)

Likelihood (L) and Impact (I): 1 (low) – 3 (high). Score = L × I. Owner for all items: design phase lead.

## Electrical
| ID | Risk | L | I | Score | Mitigation | Linked |
|---|---|---|---|---|---|---|
| R-01 | 5 V Echo signal reaches an ESP32 GPIO (no 5 V tolerance, VIH max VDD + 0.3 V) | 2 | 3 | 6 | Mandatory Echo conditioning. Analysis over tolerances. Scope test at the GPIO before connecting the DevKit | US-04, ESP-03 |
| R-02 | Trigger not recognised because the 3.3 V VOH is below the sensor's VIH | 2 | 2 | 4 | Measure the chosen module's threshold. Translator footprint option | US-05 |
| R-03 | Two supplies feed the DevKit (USB + board 5 V) → damage (REF-03) | 2 | 3 | 6 | Arch. B default. If A: enforced exclusivity (link, OR-ing) after DevKit schematic review | PWR-09, OQ-06 |
| R-04 | Back-powering an unpowered ESP32 through Echo divider, pull-ups or UART lines | 2 | 2 | 4 | Power-off-protected buffers or reference pull-ups to the ESP32's 3.3 V. Sequencing rule | US-06, I2C-04 |
| R-05 | Reverse-polarity element drop starves the 5 V-only sensor or the DevKit regulator | 2 | 2 | 4 | Low-drop topology (P-MOSFET) at Arch. A currents. Verify minimum supplies | PWR-03 |
| R-06 | 3.3 V regulator overheats if loads exceed the budget or ambient is high | 2 | 2 | 4 | Thermal calculation with real RthJA. Load budget enforced in documentation. Thermal test | PWR-11 |
| R-07 | ESP32 TX peaks cause brown-out through connector, protection or trace resistance (Arch. A) | 2 | 2 | 4 | Rated input path. Bulk capacitance. Measure the rail during Wi-Fi TX | PWR-04 |
| R-08 | I2C pull-up mismatch (modules' own pull-ups) or excessive bus capacitance | 2 | 1 | 2 | Disconnectable pull-ups. Rise-time measurement | I2C-03 |
| R-09 | Wrong pinout assumed (DevKit variants differ, WROVER reserves GPIO16/17) | 2 | 3 | 6 | Lock one exact board (ESP-01). Pin table checked against the official doc | ESP-06 |
| R-10 | Strapping-pin use causes boot failure | 1 | 2 | 2 | Avoid strapping pins or analyse them against the strapping table | ESP-04 |
| R-11 | ESD and hot-plug events on external sensor/power cables | 2 | 2 | 4 | Transient clamp on input. Series resistors on lines. Consider ESD arrays (Should) | PWR-05, UART-03 |
| R-12 | HC-SR04 variant electrical data differs from secondary sources | 3 | 2 | 6 | Treat every value as UNVERIFIED. Characterise the purchased module before freeze | US-02 |
| R-13 | Classic HC-SR04 transmit bursts inject supply noise into shared rails | 1 | 2 | 2 | Local decoupling at J_US. Separate return path. Measure ripple during ranging | PWR-16 |

## Thermal
| ID | Risk | L | I | Score | Mitigation |
|---|---|---|---|---|---|
| R-14 | Resettable fuse trips early at high ambient (derating) or late at low ambient | 2 | 1 | 2 | Use the derating curves from the datasheet at the maximum ambient (OQ-15) |
| R-15 | LDO copper area insufficient for the required RthJA | 2 | 2 | 4 | Size copper from the datasheet guidance. Thermal measurement at maximum load |

## Mechanical
| ID | Risk | L | I | Score | Mitigation |
|---|---|---|---|---|---|
| R-16 | Stacked DevKit antenna over copper degrades Wi-Fi | 2 | 2 | 4 | Antenna keep-out or cable/off-board mounting (MECH-03, OQ-10) |
| R-17 | Connectors blocked by the DevKit or each other. Probes cannot reach test points | 2 | 1 | 2 | 3D review before layout freeze (MECH-02, USE-02) |
| R-18 | Reversed or offset sensor cable on unkeyed headers | 3 | 2 | 6 | Keyed connectors where possible. Silkscreen pin names. Echo conditioning tolerant of miswiring analysed |

## Manufacturing
| ID | Risk | L | I | Score | Mitigation |
|---|---|---|---|---|---|
| R-19 | Generic DRC rules differ from the chosen fab's capability | 2 | 2 | 4 | Record the fab rules before layout (MFG-02) |
| R-20 | Part availability or obsolescence at order time | 2 | 1 | 2 | Approved alternates with datasheets. Check lifecycle at selection |
| R-21 | MCP tool defects (V0.0.2/V0.0.3, D-1…D-22) silently corrupt design files | 2 | 3 | 6 | SWIG-only workflow. Reload after sync/refill. kicad-cli ERC/DRC with parity. Field-sync script. Review every diff |
| R-22 | Silkscreen/polarity errors lead to mis-assembly | 2 | 2 | 4 | Assembly drawing. 3D review. First-article inspection |

**Highest-score risks (6):** R-01, R-03, R-09, R-12, R-18, R-21. All six depend on open questions
OQ-01, OQ-06 and OQ-11 or on established workflow rules.

## V0.1.0 design-phase additions (2026-11-08)
| ID | Risk | L | I | Score | Mitigation | Status |
|---|---|---|---|---|---|---|
| R-30 | Samtec TSW headers are not lead-free solderable ("Lead Wave Only") | 3 | 1 | 3 | HTSW series selected (DDR-16, DS-15) | CLOSED by design |
| R-31 | Power sequencing: with the board unpowered and the ESP32 on, the I2C pull-ups (3V3_ESP) back-feed unpowered I2C devices through their SDA/SCL clamps; the converse direction is blocked by Ioff buffers | 2 | 2 | 4 | Rule: power the board first or together with the DevKit. JP2 opens the pull-ups. Measure in V0.3.0 | OPEN (documented) |
| R-32 | SMAJ6.0A clamp (≤ 10.3 V at IPP) exceeds the TLV1117LV (6 V) and LVC (6.5 V) abs max; the input is not overvoltage-protected | 1 | 3 | 3 | Regulated 5 V supply only (OQ-05). TVS is an ESD/hot-plug aid. Consider OVP in a later revision | ACCEPTED |
| R-33 | GPIO16/17 (UART) are unavailable on WROVER-based boards | 1 | 2 | 2 | Reference is WROOM-32(E) (DDR-13). Remap required if a WROVER board is used | ACCEPTED |
| R-34 | Ultrasonic module pin order is not published (Adafruit 4007) | 2 | 2 | 4 | Verify on receipt (NQ-01) before wiring. J3 order VCC/TRIG/ECHO/GND | OPEN |
| R-35 | Clone 3V3 pin regulator behaviour unknown (sources 3V3_ESP, ≤ 3.4 mA) | 1 | 1 | 1 | Measure 3V3_ESP with the board attached (NQ-04) | OPEN |

Resolution status of R-01…R-22 after the V0.1.0 design: see
[`reports/v0.1.0/FINAL_V0.1.0_DESIGN_REPORT.md`](../../../reports/v0.1.0/FINAL_V0.1.0_DESIGN_REPORT.md).
