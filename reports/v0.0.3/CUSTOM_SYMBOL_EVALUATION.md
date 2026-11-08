# Custom Symbol Evaluation — V0.0.3

**Verdict: native MCP can create, register, place, wire and verify a custom symbol end-to-end.
No external scripting was needed.** Limitations are cosmetic or concern portability.

## Test object
Symbol `AIPCB_Symbols:LED_WP7113ID`, created from scratch with `create_symbol`. Every pin and
graphic coordinate was supplied by the test (`tests/make_custom_part_suite.py`), and no library
symbol was copied. Part: Kingbright WP7113ID (datasheet V.14A, see `datasheets/index.md`).

| Field | Value |
|---|---|
| Reference prefix / value | `D` / `LED_WP7113ID` |
| Pins | 1 = **K**, passive, at (−3.81, 0), angle 0, length 1.27. 2 = **A**, passive, at (3.81, 0), angle 180, length 1.27 |
| Graphics | triangle (apex toward K), cathode bar, lead line, two emission arrows (5 polylines) |
| Properties | datasheet URL, description, keywords, default footprint `AIPCB_Footprints:LED_D5.0mm_WP7113ID`, in BOM, on board |

Library: `hardware/sandbox/v0.0.3/custom_symbols/AIPCB_Symbols.kicad_sym` (copy: `evidence/libraries/`).

## Workflow and results
| Step | Tool | Result | Verification |
|---|---|---|---|
| Create symbol | create_symbol | **PASS** | File parsed. 2 pins, 5 polylines, 6 properties. KiCad 9 format `20241209`, loads in KiCad 10 |
| List / validate library | list_symbols_in_library, validate_symbol_library | **PASS** | 1 symbol, valid |
| Create project | create_project | **PASS** | `sym_test.*` |
| Register library (project scope) | register_symbol_library `scope=project` | **WARNING** | project `sym-lib-table` written. The global table was **not** touched. **URI is absolute and contains the user name** (D-11) |
| Read pins | batch_list_symbol_pins | **PASS** | output identical to `Device:LED` (K at −3.81/0°, A at 3.81/180°) |
| Symbol info | get_symbol_info | **WARNING** | failed in the same session right after registration ("Symbol not found"). Succeeded in a fresh server process with any path form (D-12) |
| Search | search_symbols with projectPath | **WARNING** | timed out after 30 s (D-13). `list_library_symbols` works |
| Place in schematic | add_schematic_component | **PASS** | `lib_id "AIPCB_Symbols:LED_WP7113ID"`, embedded `lib_symbols` cache present |
| Pin orientation | get_schematic_pin_locations | **PASS** | at 90°: A (pin 2) at (60.96, 88.90) on top, K (pin 1) at (60.96, 96.52) on the bottom |
| Connect | add_schematic_wire ×7, global label | **PASS** | every endpoint snapped to a pin |
| Structure | validate_schematic | **PASS** | valid, kicad-cli load OK |
| ERC | run_erc / `kicad-cli sch erc --severity-all` | **PASS** | 0 / 0 |
| Netlist | generate_netlist, export_netlist / `kicad-cli sch export netlist` | **PASS** | +5V: J1/1–R1/1. LED_A: R1/2–**D1/2 (A)**. GND: **D1/1 (K)**–J1/2. `libsource lib=AIPCB_Symbols part=LED_WP7113ID`. MCP and CLI `<nets>` identical |
| Persistence (fresh process) | list_schematic_components, get_schematic_pin_locations, run_erc, generate_netlist | **PASS** | same lib_id, pins, ERC 0, nets |

## Visual check
[`images/custom_symbol.png`](evidence/images/custom_symbol.png) (kicad-cli `sym export svg`):
the triangle points to K, the bar is on the K side, pin 1 is left, pin 2 is right.
[`images/sym_test_schematic_crop.png`](evidence/images/sym_test_schematic_crop.png): polarity is correct in the circuit.

**Cosmetic WARNING:** pin names `K`/`A` and the reference text overlap the body. `create_symbol`
has no option to hide pin names or set their offset. The `LED_A` global label overlaps D1.

## Schema note
The tool schema describes `pin.at.angle` as "direction the pin wire extends FROM the symbol body".
The test shows the value is written verbatim with **KiCad's file meaning** (direction from the
connection point toward the body): angle 0 on a left-hand pin gives a correct symbol. The
description is misleading. Rely on the KiCad convention.

## Native vs external
All steps used MCP tools. Independent checks used kicad-cli and file inspection only.
