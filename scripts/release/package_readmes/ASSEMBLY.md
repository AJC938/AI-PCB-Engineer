# Sensor Interface PCB — Rev A — Assembly Package

Release v1.0.0, board revision **A**. Intended service: **full turnkey, SMT + THT, top side only, lead-free.**
**NOT yet assembled or tested.**

Contents: BOM (33 lines, 52 placements: 44 SMT + 8 THT, no DNP), CPL / pick-and-place (52 parts + 3 fiducials,
mm, origin bottom-left), top and bottom assembly drawings (bottom has no parts), schematic PDF, layer plots,
ASSEMBLY_NOTES.md (polarity, fiducials, THT, MSL, rotations), CONNECTOR_PINOUT.md.

Rules for the assembler:
- Use the exact manufacturer part numbers. **No substitution without written approval** from the orderer.
- Confirm the THT soldering method (wave, selective or hand) for J1–J6 and LED1/LED2.
- Confirm polarity of U1–U5, LED1/LED2 and pin 1 of J1–J6 against the assembly drawing at first article.
- Apply your own package zero-orientation offsets to the CPL rotations (KiCad library orientation).
Combine this package with the Fabrication package, or use the Complete Manufacturing package.
