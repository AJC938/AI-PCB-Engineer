# Digital Validation Summary — Rev A (v1.0.0)

All checks were run with KiCad 10.0.8 `kicad-cli` on the saved design files by
[`scripts/release/build_release.sh`](../../scripts/release/build_release.sh). Evidence:
[`reports/v0.3.0/evidence/validation/`](../../reports/v0.3.0/evidence/validation/). No DRC/ERC exclusions exist.

| Check | Tool | Result |
|---|---|---|
| ERC, all severities | `kicad-cli sch erc --severity-all` | **0 violations** |
| Netlist / power-domain verifier | `hardware/kicad/.../build/verify_schematic.py` | **PASS** (31 design nets, `+3V3_P` ∩ `3V3_ESP` = ∅, eFuse RTN ≠ GND, 61 footprints, 52 MPNs) |
| DRC, all severities, zones refilled before the check (MCP defect D-10) | `kicad-cli pcb drc --refill-zones --schematic-parity --severity-all` | **0 violations, 0 unconnected, 0 parity errors** |
| DRC with the stored zone fills | same, no refill | **0 / 0 / 0** |
| Manufacturing package audit | `scripts/release/audit_release.py` | see `release_audit.txt` |
| ZIP package test (extraction, byte compare, path and privacy scan) | `scripts/release/make_packages.py` | see `MANUFACTURING_PACKAGE_AUDIT.md` |
| Fresh-process reopen | KiCAD-MCP-Server (SWIG) in a new process + kicad-cli + pcbnew | see `reports/v0.3.0/FINAL_V0.3.0_REPORT.md` |

What this does **not** prove: correct behaviour of real parts, solder quality, thermal behaviour, signal
integrity on real cables, or sensor compatibility. See
[PHYSICAL_VALIDATION_STATUS.md](PHYSICAL_VALIDATION_STATUS.md).
