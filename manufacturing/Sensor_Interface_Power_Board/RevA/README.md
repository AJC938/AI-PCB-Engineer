# Rev A — Manufacturing Release (v1.0.0)

**Fabrication-ready digital design. NOT yet fabricated, assembled or physically tested. Not submitted to any
manufacturer.** Generated 2026-11-09 with KiCad 10.0.8 by
[`scripts/release/build_release.sh`](../../../scripts/release/build_release.sh) from
[`hardware/kicad/Sensor_Interface_Power_Board/`](../../../hardware/kicad/Sensor_Interface_Power_Board/).

| Folder | Content |
|---|---|
| [`packages/`](packages/) | **Start here.** `Sensor_Interface_PCB_RevA_Fabrication.zip`, `…_Assembly.zip`, `…_Complete_Manufacturing.zip` |
| [`fabrication/`](fabrication/) | Gerber X2 (9 layers) + job file, Excellon PTH/NPTH + drill maps, IPC-D-356, [FABRICATION_NOTES.md](fabrication/FABRICATION_NOTES.md) |
| [`assembly/`](assembly/) | BOM (33 lines / 52 parts), CPL (55 rows incl. 3 fiducials), assembly drawings, schematic PDF, layer plots, [ASSEMBLY_NOTES.md](assembly/ASSEMBLY_NOTES.md), [CONNECTOR_PINOUT.md](assembly/CONNECTOR_PINOUT.md) |
| [`3d/`](3d/) | STEP model (place origin = board bottom-left) |
| [`checksums/SHA256SUMS.txt`](checksums/SHA256SUMS.txt) | SHA-256 of the ZIPs and every file above. Verify from this folder: `sha256sum -c checksums/SHA256SUMS.txt` |

Independent audit of these files: [`reports/v0.3.0/evidence/validation/release_audit.txt`](../../../reports/v0.3.0/evidence/validation/release_audit.txt)
and [`reports/v0.3.0/MANUFACTURING_PACKAGE_AUDIT.md`](../../../reports/v0.3.0/MANUFACTURING_PACKAGE_AUDIT.md).
