# ERC and Netlist Report — V0.0.2

## ERC
| Run | Tool | Result |
|---|---|---|
| After wiring | MCP `run_erc` | 0 errors, 0 warnings, 0 info |
| After wiring | `kicad-cli sch erc --severity-all` | 0 violations |
| After switching to global label `LED_A` | MCP `run_erc` | 0 |
| Final | `kicad-cli sch erc --severity-all` | 0. Evidence: [`evidence/checks/erc_cli.json`](evidence/checks/erc_cli.json) |

MCP and CLI agree on every run. No warning was suppressed or excluded.

### PWR_FLAG justification (experiment, not assumption)
The PWR_FLAG symbols were removed from a **temporary copy** of the schematic (outside the
repository) and ERC was re-run with kicad-cli:

| Violation | Item |
|---|---|
| error `power_pin_not_driven` | #PWR01 (+5V) |
| error `power_pin_not_driven` | #PWR03 (GND) |
| 2× warning `unconnected_wire_endpoint` | caused only by deleting the flag symbols and leaving their wires |

Both nets are fed only by J1's **passive** pins, so KiCad's ERC has no power-output source.
One PWR_FLAG per net (+5V, GND) is therefore required, and only those two are used.

## Netlist
MCP `generate_netlist` and `kicad-cli sch export netlist --format kicadxml`
([`evidence/checks/led_test_cli.net`](evidence/checks/led_test_cli.net)) give identical results:

| Net | Nodes | Expected | Check |
|---|---|---|---|
| +5V | J1/1 (Pin_1), R1/1 | supply to resistor | PASS |
| LED_A | R1/2, D1/2 (**A**) | resistor to anode | PASS |
| GND | D1/1 (**K**), J1/2 (Pin_2) | cathode to return | PASS |

| Component | Value | Footprint | MPN | Manufacturer |
|---|---|---|---|---|
| D1 | Red | LED_THT:LED_D5.0mm | WP7113ID | Kingbright |
| J1 | 5V_IN | TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal | 1715721 | Phoenix Contact |
| R1 | 620 | R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal | MFR-25FBF52-620R | Yageo |

- No unconnected pins, references are correct, LED polarity is correct, and the connector numbering matches the silkscreen.
- Every pin type is passive. The power symbols are `power_in`, and the PWR_FLAG pins are `power_out`.

**Evidence label:** TOOL-CHECKED (ERC) + netlist cross-check. This does not by itself prove the
circuit works. See the calculations for the electrical design.
