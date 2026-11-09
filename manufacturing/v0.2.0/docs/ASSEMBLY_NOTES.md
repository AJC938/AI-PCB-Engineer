# Assembly notes — Rev 0.2.0 (full factory assembly, turn-key)

| Item | Value |
|---|---|
| Assembly side | **Top only** (bottom: no components, no paste) |
| Placements | 52: 44 SMT + 8 THT (BOM `Sensor_Interface_Power_Board_v0.2.0_BOM.csv`, 33 lines) |
| Not placed (PCB features) | H1–H4 (NPTH M3 holes), FID1–FID3 (fiducials), JP1/JP2 (solder jumpers, factory-bridged in copper) |
| Solder | Lead-free (SAC/RoHS). All parts are lead-free solderable: Samtec **HTSW** chosen because TSW is "lead wave only" |
| Stencil | Top only, 0.12–0.125 mm; U5 exposed pad aperture 3.3 × 3.3 mm (TI SLVSDG2G p.54) |
| MSL | TPS26600PWPR: MSL 2 (260 °C, 1 year) per TI addendum — bake per J-STD-033 if exposure exceeded |
| THT parts | J1 (Phoenix 1715721), J2 (HTSW-112-07-T-S), J3–J6 (HTSW-104-07-T-S), LED1/LED2 (Kingbright 5 mm). All seated flush, perpendicular, on top |
| Substitution | **No substitution of any MPN without written approval from the owner** |

## Fiducials (bottom-left origin, mm)
FID1 (9.0, 39.0) · FID2 (60.0, 14.0) · FID3 (12.0, 14.0) — 1.0 mm copper, 2.0 mm mask opening.

## Polarity / orientation (verify at first-article inspection)
| Ref | Mark | Rule |
|---|---|---|
| U5 TPS26600 | pin-1 dot/triangle on silk, top-left | pin 1 (IN) toward J1 |
| U1 TLV1117LV33 | tab (pin 2) to the right | tab inside the +3V3 copper area |
| U2/U4 LVC1G17, U3 LVC1T45 | pin-1 triangle on silk | as drawn on assembly drawing p.2 |
| LED1 red (+5V), LED2 green (+3V3) | square pad = cathode (pin 1), flat side on silk | cathode to the left |
| J1 | wire entries face the **left board edge** | pin 1 (+5V) = upper position, marked ▸ |
| J2–J6 | square pad = pin 1 | J2 pin 1 = left end (3V3); J3–J6 pin 1 = top |

## CPL convention
`Sensor_Interface_Power_Board_v0.2.0_CPL.csv`: Ref, Val, Package, PosX, PosY (mm, origin = board bottom-left,
Y up), Rot (KiCad footprint orientation, degrees), Side. Rotations use KiCad library zero orientation; the
factory must apply its own package-orientation offsets and confirm polarity against the assembly drawing.
Fiducials are included in the CPL; H*, JP* are excluded.
