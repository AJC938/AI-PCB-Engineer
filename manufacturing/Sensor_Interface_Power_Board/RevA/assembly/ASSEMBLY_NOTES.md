# Assembly Notes — Sensor Interface & Power Management Board, Rev A (release v1.0.0)

**Intended assembly: FULL FACTORY ASSEMBLY / FULL TURNKEY (SMT + THT), top side only.**
**Status: NOT yet assembled or tested.** No supplier has confirmed this assembly; see §6.

## 1. Files
| File | Content |
|---|---|
| `Sensor_Interface_Power_Board_RevA_BOM.csv` | 33 lines, 52 placements (44 SMT + 8 THT): Item, Qty, References, Value, Description, Manufacturer, MPN, Package, Mount, Side, DNP, Substitution |
| `Sensor_Interface_Power_Board_RevA_CPL.csv` | 55 rows: 52 placements + 3 fiducials. Ref, Val, Package, PosX, PosY (mm), Rot (deg), Side |
| `..._assembly_drawing_top.pdf` | Top assembly drawing (fab outlines, reference designators, polarity marks, silkscreen, outline) |
| `..._assembly_drawing_bottom.pdf` | Bottom side (mirrored): **no components** |
| `..._schematic.pdf` | Full schematic |
| `..._layers.pdf` | Layer plots (copper, mask, silkscreen, fab) for reference |
| `CONNECTOR_PINOUT.md` | Pin-1 location and function of every connector |
| `../3d/Sensor_Interface_Power_Board_RevA.step` | 3D model (review aid; library models, not measured parts) |

## 2. Assembly requirements
| Item | Requirement |
|---|---|
| Sides | **Top only.** No bottom components, no bottom paste |
| SMT | 44 placements: 0603 R/C, SOT-23-5/6, SOT-223, HTSSOP-16 with exposed pad (U5), SMT test points |
| THT | 8 parts: J1 (Phoenix 1715721 terminal block), J2 (Samtec HTSW-112-07-T-S), J3–J6 (Samtec HTSW-104-07-T-S), LED1/LED2 (Kingbright 5 mm) |
| Solder | Lead-free (RoHS). The headers are Samtec **HTSW**, the lead-free-process version (TSW is lead-only wave) |
| Stencil | Top only, 0.12–0.125 mm. U5 exposed-pad paste aperture 3.3 × 3.3 mm (as in the paste Gerber) |
| THT soldering | Factory method: wave, selective wave or hand. All THT parts sit flush, perpendicular to the board, on top |
| Moisture | TPS26600PWPR: MSL 2 (TI package addendum). Handle and bake per J-STD-033 |
| Cleaning | Standard no-clean process acceptable. No conformal coating is required |
| Inspection | AOI recommended. First-article check of all polarities in §4 |
| Substitution | **No substitution of any MPN without written approval from the orderer** |
| DNP | **None.** Every BOM line is fitted |

## 3. Not placed (PCB features, not in BOM)
H1–H4 (M3 non-plated holes), FID1–FID3 (fiducials), JP1/JP2 (solder jumpers, already bridged in copper:
JP1 pads 1-2 → UART VCC = 3.3 V; JP2 closed → I²C pull-ups on).

## 4. Polarity and orientation (verify at first-article inspection)
| Ref | Marking | Rule |
|---|---|---|
| U5 TPS26600PWPR | pin-1 marker on silk | pin 1 (IN) on the side facing J1 (top-left of U5) |
| U1 TLV1117LV33DCYR | large tab pad | tab (pin 2, OUT) to the right, inside the +3V3 copper area |
| U2, U4 SN74LVC1G17DBVR; U3 SN74LVC1T45DBVR | pin-1 marker on silk | per assembly drawing |
| LED1 red (+5V present), LED2 green (+3.3V present) | square pad = cathode (pin 1), flat side on silk outline | cathode on the left |
| J1 terminal block | wire entries face the left board edge | pin 1 (+5V IN) = upper position, marked with a triangle |
| J2 1×12 header | square pad = pin 1 | pin 1 (3V3_ESP reference) at the left end |
| J3–J6 1×4 headers | square pad = pin 1 | pin 1 at the top (J3 pin 1 = +5V, J4/J5/J6 pin 1 = GND) |

## 5. Fiducials and coordinates
- Origin (0, 0) = board **bottom-left** corner; X to the right, Y up; units mm. Gerbers, drill files and CPL use
  the same origin.
- Global fiducials (1.0 mm copper, 2.0 mm mask opening): **FID1 (9.0, 39.0) · FID2 (60.0, 14.0) · FID3 (12.0, 14.0)**.
- CPL rotation = KiCad footprint orientation (KiCad library zero orientation). The factory must apply its own
  package zero-orientation offsets and confirm polarity against the assembly drawing before placement.

## 6. Supplier-dependent items (not confirmed by any manufacturer)
1. Factory THT soldering method for the terminal block, 2.54 mm headers and 5 mm LEDs.
2. Turnkey availability of **TPS26600PWPR** (stock is limited; see `reports/v0.3.0/BOM_SOURCING_AUDIT.md`).
3. CPL rotation convention for the factory's machine library.
4. Whether the factory needs local fiducials (three global fiducials are provided).
