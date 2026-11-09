# ERC Validation — V0.2.0

| Check | Tool | Result | Evidence |
|---|---|---|---|
| Schematic build | MCP (SWIG): 364/364 calls (full build) + 10/10 (incremental H1–H4, FID1–FID3) | OK | `evidence/mcp_runs/run_s2.json`, `run_s2inc.json` |
| validate_schematic | MCP | valid, 0 errors | run_s2 |
| ERC | MCP `run_erc` | **0** (errors 0, warnings 0, info 0) | run_s2, run_s2inc |
| ERC | `kicad-cli sch erc --severity-all` (KiCad 10.0.8), after every schematic edit including the BOM-flag edit | **0 violations** | `evidence/validation/erc_cli.json`, `erc_cli.rpt`, `reports/erc/v0.2.0-erc.json` |
| Netlist vs design table | `build/verify_schematic.py` on the kicad-cli netlist | **PASS**: 31 nets exact, domain rules, eFuse RTN/GND/IN/OUT rules, TRIG series R, 61 footprints exist (54 electrical with every pin padded + 4 holes + 3 fiducials), 52 parts with MPN | `evidence/validation/verify_output.txt` |

**No exclusions, severity changes or waivers.** The no-connect flags (U2-1, U4-1, U5-4/13 NC, U5-7 SHDN, U5-10
IMON, U5-14 FLT) each follow the TI pin tables. SHDN has an internal pull-up (2.7 V). IMON and FLT: "if unused,
leave floating".

Controlled non-MCP schematic edits (each re-validated with ERC 0):
1. `set_page_a3.py`: paper and title block (no MCP tool).
2. `set_bom_flags.py`: `in_bom no` on H1–H4, FID1–FID3, JP1, JP2 (MCP always writes `in_bom yes`).
