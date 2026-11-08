# ERC and Netlist Validation — V0.1.0

| Check | Tool | Result | Evidence |
|---|---|---|---|
| Structural validity | MCP `validate_schematic` (+ kicad-cli load on a copy) | valid, 0 errors / 0 warnings, 53 symbols | `mcp_runs/run_s2.json`, `run_s3.json`, `run_s4.json` |
| ERC (MCP) | `run_erc` | **0 violations** (errors 0, warnings 0, info 0) after build, after MPN change, after value change, and after re-open | runs s2–s5 |
| ERC (independent) | `kicad-cli sch erc --format json --severity-all` (KiCad 10.0.8) | **0 violations** | `validation/erc_cli.json` |
| Netlist (independent) | `kicad-cli sch export netlist --format kicadxml` | 50 components, 29 nets (27 design + 2 NC singles) | `validation/netlist_cli.xml` |
| Netlist vs design table | `build/verify_schematic.py` | **PASS**: nets exact, domain rules, 50 footprints, metadata | `validation/verify_output.txt` |
| MCP vs CLI netlist | `generate_netlist` (MCP) vs CLI | same 50 components and net membership | run s5 vs `netlist_cli.xml` |
| BOM | `kicad-cli sch export bom` | 32 grouped lines, MPNs present | `validation/bom_cli.csv` |

**No ERC exclusions, severity changes or suppressions were used.** The only no-connect flags are on the
two pins the TI datasheet defines as "NC – no internal connection" (SN74LVC1G17 pin 1).

## Power-flag justification
| Net | Why a PWR_FLAG is needed |
|---|---|
| `+5V_P` | Fed from J1 through passive F1/Q1 pins. It has power_in consumers (U1 VI, U3 VCCB) |
| `GND` | Ground reference for power_in pins. Source is the passive J1/J2 pins |
| `3V3_ESP` | Supplied from the DevKit through passive J2-1. Power_in consumers U2/U3/U4 |
| `+3V3_P` | none: driven by U1 VO (power_out) |

## Netlist inspection summary (from the CLI netlist)
| Net | Nodes |
|---|---|
| `US_TRIG_ESP` | J2-3, U3-3 (A), R4 |
| `US_TRIG_5V` | U3-4 (B), R5, J3-2, TP8 |
| `US_ECHO_5V` → `US_ECHO_IN` | J3-3 → R6 → U2-2 (A), R7 |
| `US_ECHO_ESP` | U2-4 (Y), J2-4, TP7 |
| `UART_RX` → `UART_RX_IN` → `UART_RX_ESP` | J4-4 → R11 → U4-2 (+R12 to 3V3_ESP) → U4-4 → J2-8 |
| `UART_TX_ESP` → `UART_TX` | J2-7 → R10 → J4-3 |
| `I2C_SDA` / `I2C_SCL` | J2-5/J5-3/R8, J2-6/J5-4/R9. Pull-up common `I2C_PU` via JP2 to 3V3_ESP |
| `GP_IO1/2` ↔ `GP_IO1/2_ESP` | J6-3/4 ↔ R13/R14 ↔ J2-9/10 |
| `+3V3_P` | U1-2, C3, C4, R3, TP3, J5-2, J6-2, JP1-1 |
| `3V3_ESP` | J2-1, TP4, U3-1, U3-5, C6, U2-5, C10, JP2-1, R12, U4-5, C11 |
| `+5V_P` | Q1-2 (S), D1-K, C1, C2, C5, U1-3, R2, TP2, U3-6, C7, J3-1, C8, C9, JP1-3 |
