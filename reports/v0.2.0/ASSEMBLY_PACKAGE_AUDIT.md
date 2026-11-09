# Assembly Package Audit — V0.2.0

| Item | File | Check | Result |
|---|---|---|---|
| BOM | `assembly/Sensor_Interface_Power_Board_v0.2.0_BOM.csv` | 33 lines, 52 placements = schematic in_bom parts. Columns: Item, Qty, References, Value, Description, Manufacturer, MPN, Package, Mount (SMT/THT), Side, DNP, Substitution policy. Every line has Manufacturer + MPN | PASS (B1) |
| CPL | `assembly/Sensor_Interface_Power_Board_v0.2.0_CPL.csv` | 55 rows = 52 parts + 3 fiducials. X/Y within 1 µm of the board (origin bottom-left, Y up). Rotation = footprint orientation. All top side | PASS (C1–C4) |
| Assembly drawing top | `assembly/…_assembly_drawing_top.pdf` | p.1 fab layer (bodies, pin-1 chamfers, refs, pads sketched); p.2 silkscreen (refs, polarity, legend). Scale 1.8:1, rev 0.2.0 title block | PASS (visual) |
| Assembly drawing bottom | `assembly/…_assembly_drawing_bottom.pdf` | no components (confirms single-sided assembly) | PASS |
| Layer plots | `assembly/…_layers.pdf` | F.Cu, B.Cu, F.Silkscreen, F.Mask with outline | PASS |
| Schematic | `assembly/…_schematic.pdf` | rev 0.2.0, A3 | PASS |
| Notes | `docs/ASSEMBLY_NOTES.md` | side, solder, stencil, MSL, THT list, fiducial coordinates, polarity table, CPL convention, no-substitution rule | PASS |
| 3D | `3d/…step` | full assembly incl. connectors | PASS (review aid) |

## Integrity checks performed
- BOM references ∪ fiducials = CPL references exactly. H*/JP* are excluded consistently in both, with in_bom = no
  in the schematic and exclude_from_bom/pos on the footprints.
- DNP: none. All 52 placements are fitted.
- Values in CPL = values in BOM (same netlist source).
- Polarity-sensitive parts (U1–U5, LED1/2, J1–J6) are listed with their marks in ASSEMBLY_NOTES.md.

## Limits
- **CPL rotations are in KiCad's convention.** Vendors often apply their own per-package offsets, so the vendor
  must confirm orientation against the assembly drawing (DFA_REPORT.md).
- The package proves the data is consistent. It does not prove the vendor will assemble every THT part; that
  needs the vendor's written confirmation.
