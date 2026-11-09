# DFA Report — V0.2.0 (full factory assembly)

| Topic | Implementation | Status |
|---|---|---|
| Assembly sides | top only (B.Paste empty, no bottom parts) → one reflow pass + THT step | PASS |
| SMT packages | 0603 R/C, SOT-23-5/6, SOT-223, HTSSOP-16 0.65 mm with exposed pad, Keystone 5015 on tape | PASS (all ≥ 0603, pitch ≥ 0.65 mm; within every shortlisted vendor's capability) |
| THT parts | J1 terminal block, J2–J6 Samtec HTSW (lead-free solderable), LED1/2 | PASS; **THT method to be confirmed by the vendor** |
| THT access | all THT on the top side, at board edges, no SMT parts within 1.5 mm of THT pins on the bottom (bottom is bare) | PASS (wave or selective soldering possible) |
| Lead-free | all parts RoHS / lead-free solderable (TSW → HTSW change V0.1.0) | PASS |
| Orientation | ICs share a consistent orientation (pin 1 top-left for U2/U3/U4/U5); passives at 0°/90°/180°/270° only | PASS |
| Polarity marks | silk pin-1 marks on U1–U5, J1–J6; LED flat + square cathode pad; assembly drawing page 2 | PASS |
| Silkscreen under parts | no reference text under bodies (DRC silk_over_copper 0, placer avoids courtyards) | PASS |
| Courtyard spacing | no overlaps (offline check + KiCad DRC courtyard rules: 0) | PASS |
| Fiducials | 3 global, 1 mm copper / 2 mm mask, non-collinear, listed in CPL | PASS |
| Tooling holes | 4 × M3 NPTH (usable as tooling holes); no panel requested | PASS (vendor may add a panel with rails) |
| Paste / stencil | U5 EP paste 3.3 × 3.3 (TI 100 % at 0.125 mm stencil); no via-in-pad anywhere | PASS |
| Thermal relief | GND THT pads use thermal reliefs (zones), no starved spokes (DRC 0); U1 tab solid by design (thermal), it is SMD so it reflows fine | PASS |
| Test access | 8 SMT test points top side, ≥ 2.6 mm pads, probe-friendly; IPC-D-356 for flying probe | PASS |
| Pick-and-place data | CPL: 55 rows (52 parts + 3 fiducials), origin bottom-left, rotations = KiCad orientation | PASS (vendor to confirm rotation convention) |
| BOM integrity | 33 lines: Ref, Qty, Manufacturer, MPN, Description, Value, Package, Mount, Side, DNP, "NO SUBSTITUTION without written approval" | PASS |
| Solder jumpers | JP1 (1-2 bridged = 3.3 V UART VCC), JP2 (bridged = I2C pull-ups on): copper bridges, no assembly step | PASS |
| Moisture sensitivity | U5 MSL 2 (TI) | note for vendor |

**Not proven by the BOM/CPL alone:** that the vendor will actually solder every THT part. This depends on the
vendor's confirmed THT process (see MANUFACTURER_SELECTION_RECOMMENDATION.md). Status: **PROVISIONAL until the
quote confirms it.**
