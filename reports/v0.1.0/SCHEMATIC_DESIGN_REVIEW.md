# Schematic Design Review — V0.1.0

Project: [`hardware/kicad/Sensor_Interface_Power_Board/`](../../hardware/kicad/Sensor_Interface_Power_Board/)
(`Sensor_Interface_Power_Board.kicad_sch`, A3, single sheet; PDF in
[`evidence/validation/`](evidence/validation/Sensor_Interface_Power_Board_schematic.pdf)).

## How it was built (reproducible)
| Step | Method | Tool |
|---|---|---|
| 1 | `create_project` | MCP (SWIG), harness run s1 |
| 2 | Paper A3 + title block (no MCP tool exists for this) | controlled script `build/set_page_a3.py` (one token + title block, paren balance asserted, then MCP `validate_schematic` incl. kicad-cli load) |
| 3 | 53 symbols, 124 pin-snapped global labels, 2 no-connects, 144 properties (Manufacturer/MPN/Datasheet), validate, ERC, netlist | MCP, 326 calls, 0 failures (run s2) |
| 4 | Header MPNs TSW → HTSW (DDR-16) | MCP `set_schematic_component_property` (run s3) |
| 5 | Capacitor values shortened (text overlap) | MCP `edit_schematic_component` (run s4) |
| 6 | Re-open in a fresh server process: components, netlist, ERC | MCP (run s5) |
Single source of truth: `build/build_schematic.py` (PARTS, NETS). Re-running it on an empty project
reproduces the schematic.

## Sheet organisation
Hierarchical sheets were **not** used. The design has about 50 parts in 6 functional groups, and one A3 sheet
in three rows is clearer: **row 1** power entry, protection, regulation, indicators, power test points. **Row 2** ESP32
interface, TRIG translator, ultrasonic connector, Echo buffer. **Row 3** I2C, UART (VCC select, TX series,
RX buffer), GP connector. **Row 4** ground test points and PWR_FLAGs.
Connectivity is **pin-snapped global labels** (DDR-15): every pin carries its net name, and there are no wires that only look connected.

## Review checklist
| Item | Result | Evidence |
|---|---|---|
| Pin connectivity | 27 design nets match the design table exactly (no missing or extra node) | `verify_output.txt` [1] |
| Unconnected pins | Only U2-1 and U4-1 (datasheet "NC"), flagged no-connect | netlist `unconnected-(U2-NC-Pad1)`, `(U4-NC-Pad1)` |
| Power flags | `+5V_P` (driven through passive Q1), `GND`, `3V3_ESP` (from passive J2). `+3V3_P` is driven by U1's power_out pin, so no flag needed | ERC 0 |
| Pin types | Logic inputs (A, DIR) all driven or pulled. Power-in pins on flagged or power_out nets. No output-to-output conflicts | ERC 0 (all severities) |
| Signal direction | GPIO26 → U3 A → B → TRIG. ECHO → U2 A → Y → GPIO34. RX → U4 → GPIO16. GPIO17 → R10 → TX. DIR on 3V3_ESP = A→B (DS-08 function table) | netlist + DS-08 p.14 |
| Power domains | ESP32 nets touch only allowed 3.3 V-domain parts. `+3V3_P` ∩ `3V3_ESP` = ∅. U2/U4/U3-A powered from 3V3_ESP. U3-B from `+5V_P` | `verify_output.txt` [2] |
| Footprint mapping | 50 footprints exist. Every symbol pin number has a pad | `verify_output.txt` [3] |
| Symbol ↔ datasheet pinout | AO3401A, TLV1117LV (AMS1117 symbol), LVC1G17, LVC1T45 checked pin-by-pin | DATASHEET_VERIFICATION.md |
| Metadata | 48/48 BOM parts have Manufacturer + MPN (+ Datasheet URL). JP1/JP2 are PCB features | BOM `bom_cli.csv` |
| Reference designators | Sequential by class: C1–11, D1, F1, J1–6, JP1–2, LED1–2, Q1, R1–14, TP1–8, U1–4 | BOM |

## Findings
| # | Severity | Finding | Disposition |
|---|---|---|---|
| F-1 | Cosmetic | TP1–TP4 value/reference text overlaps their labels. The U1 value overlaps its GND pin label | Accept for V0.1.0. Tidy in KiCad GUI or V0.2.0 |
| F-2 | Info | Regulator uses the `AMS1117-3.3` symbol as a pin-identical carrier for TLV1117LV33 (value and MPN set correctly) | Accepted (verified pin map). Optional custom symbol later |
| F-3 | Info | TVS drawn with `D_Zener` (unidirectional K/A) because KiCad's `D_TVS` is bidirectional | Accepted |
| F-4 | Process | MCP `create_footprint`/`create_symbol` not needed. All library parts exist | — |
| F-5 | Process | No MCP tool sets paper size or title block, so a controlled script was used, then validated | Documented (new MCP limitation) |

**Not production-ready:** the electrical design is validated digitally. Physical dependencies are listed in
OPEN_QUESTIONS.md (ultrasonic pin order, DevKit mechanics, measurements).
