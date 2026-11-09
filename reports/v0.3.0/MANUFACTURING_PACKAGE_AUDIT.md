# Manufacturing Package Audit — Rev A (v1.0.0)

Outputs were regenerated (not copied) from the final design by `scripts/release/build_release.sh` with KiCad
10.0.8 `kicad-cli`. Only options listed by `kicad-cli <command> --help` were used. A successful export was not
treated as proof: every file was inspected by `scripts/release/audit_release.py` (pcbnew read-back of the board,
parsing of the Gerber, Excellon, CSV, IPC-D-356 and job files).

## 1. Independent audit — 19/19 PASS (`evidence/validation/release_audit.txt`)
| ID | Check | Result |
|---|---|---|
| G1 | 9 Gerber layers, X2 FileFunction, mm, format 4.6 | PASS |
| G2 | Edge.Cuts extents 0…90.000 × 0…64.000 mm (origin bottom-left) | PASS |
| G3 | F.Paste flashes 107 = SMD paste pads 107; B.Paste empty | PASS |
| G4 | every coordinate of every Gerber inside the outline | PASS |
| G5 | job file: 2 layers, 1.6 mm, 90.1 × 64.1 mm (incl. outline line width) | PASS |
| G6 | B.Silkscreen prints nothing; F.Silkscreen 8446 printing operations; "REV A v1.0" label present | PASS |
| D1 | PTH by diameter: 0.3 × 57, 0.9 × 4, 1.0 × 28, 1.3 × 2 = board | PASS |
| D2 | NPTH 3.2 × 4 = board | PASS |
| D3 | Excellon METRIC/decimal; 95 hits = 95 board holes, each at the same X/Y (± 5 µm) and diameter | PASS |
| C1–C4 | CPL: 55 rows = 52 placements + 3 fiducials; X/Y (± 1 µm) and rotation = board; all top | PASS |
| B1–B4 | BOM: 52 placements, 33 lines, Qty = reference count, Mount/Side set, all required columns, no generic descriptions | PASS |
| N1 | IPC-D-356 contains every routed net (39 net records) | PASS |
| F1 | STEP, drawings, schematic, layer plots, drill maps, notes present | PASS |

## 2. Change against the V0.2.0 release (header and date lines removed)
F.Cu, B.Cu, F.Mask, B.Mask, F.Paste, B.Paste, B.Silkscreen, Edge.Cuts, PTH, NPTH, CPL and IPC-D-356 are
**identical** to `manufacturing/v0.2.0/`. F.Silkscreen differs only in the Y 36.1–37.1 mm band, which is the
"REV A v1.0" label (DDR-22). The BOM has the same parts. Only the description, sourcing and alternative columns
were added.

## 3. ZIP packages (`scripts/release/make_packages.py`) — PASS
| Package | Files | Bytes | SHA-256 |
|---|---|---|---|
| `Sensor_Interface_PCB_RevA_Fabrication.zip` | 18 | 126 933 | `09a6932a98d854e3110cbb7bd1512aad493aca96dc5361b0a697ad747015996b` |
| `Sensor_Interface_PCB_RevA_Assembly.zip` | 10 | 324 819 | `6683502f8018e1416aadc79c326ec78c94f8d8e3a567abd1bce131658ba6a57b` |
| `Sensor_Interface_PCB_RevA_Complete_Manufacturing.zip` | 27 | 808 988 | `008feec3bc17f058fed57db5eefe5c57230cbffb453ca897742e9256fbcc2c08` |

Tests on each archive:
- CRC test passed.
- Extracted into a fresh temporary directory, and every member is byte-identical to its source file.
- One top-level folder per ZIP; no absolute, parent (`..`), drive-letter or backslash paths.
- No machine-specific text in any member: drive-letter user paths, `AppData`, `/home/` and the local account
  name were all scanned for. PDFs were also checked after decompressing every stream: no hit. PDF metadata holds
  only the title, "PCBNEW"/"Eeschema-PDF" and "KiCad PDF". The STEP header has the file name and KiCad only.
- Each ZIP has its own `README.md` and `MANIFEST-SHA256.txt`.
- Deterministic build: sorted entries and a fixed timestamp (2026-11-09 00:00).

`RevA/checksums/SHA256SUMS.txt` (28 entries: 3 ZIPs + every fabrication, assembly and 3D file) was verified with
`sha256sum -c`: 28/28 OK. The release folder is marked `-text` in `.gitattributes`, so git stores the files
byte-exact and the checksums hold on every platform.

## 4. Renders and plots (`media/renders/`)
3D: top, bottom, isometric, rear isometric (`kicad-cli pcb render`, high quality, 2400 × 1600). 2D: top and bottom
plots, three connector close-ups, schematic overview and eFuse detail (KiCad PDF → PNG). All generated from the
Rev A files; nothing was drawn or edited by hand.
