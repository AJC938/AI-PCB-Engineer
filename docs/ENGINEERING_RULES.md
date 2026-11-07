# Engineering Rules (mandatory)

These rules apply to every design step, whether performed by a human or an AI agent.
**Passing ERC and DRC is necessary but never sufficient.**

## 1. Datasheet verification
- Every active component and every non-trivial passive must have its manufacturer
  datasheet stored in `datasheets/` and indexed (part number, revision/date, source URL).
- Specifications (ratings, pinout, package, recommended layout) are taken from the
  datasheet only. Distributor pages and memory are not sources.
- Each specification used in the design cites the datasheet page/table.

## 2. Pinout verification
- Symbol pin numbers, names and electrical types are checked pin-by-pin against
  the datasheet pin table for the **exact package** used.
- Multi-unit, exposed-pad and NC pins are handled explicitly.
- Custom symbols are reviewed before first use and the review is recorded.

## 3. Footprint verification
- Pad size, pitch, courtyard, pin-1 location and body outline are checked against
  the datasheet mechanical drawing and recommended land pattern.
- Library footprints are verified, not trusted blindly. Record the check.
- 3D model alignment is inspected where a model exists.

## 4. Electrical calculations
- Current per net, voltage levels and logic-level compatibility are documented in
  `calculations/`.
- Trace widths are sized for the expected current and temperature rise (IPC-2152
  or a documented calculator) for the chosen copper weight.
- Resistor/LED/divider/regulator values are calculated, not guessed.

## 5. Power integrity
- Decoupling per datasheet recommendations, placed close to power pins.
- Regulator input/output capacitance, stability (ESR) and dropout are verified.
- Return paths and ground strategy are deliberate; avoid splitting reference planes
  under high-speed signals.

## 6. Thermal considerations
- Power dissipation estimated for regulators, drivers and power resistors.
- Thermal pads, vias and copper area follow datasheet guidance.
- Component temperature ratings checked against expected operating conditions.

## 7. Manufacturing constraints
- Board setup (trace/space, drill, annular ring, via size, solder mask, silkscreen,
  layer stack, board thickness) matches the selected manufacturer's published
  capabilities, recorded with the source and date.
- DFM/DFA concerns (polarity marks, fiducials, test points, tooling holes) are reviewed.

## 8. ERC and DRC
- ERC and DRC are run with `kicad-cli` and reports are saved in `reports/erc/` and
  `reports/drc/`. Every remaining violation or exclusion is justified in writing.

## 9. BOM verification
- Each BOM line: reference, value, footprint, manufacturer part number, supplier
  part number, quantity — cross-checked against the schematic and stock availability.
- Alternate parts must be verified to the same standard.

## 10. Manufacturing output inspection
- Gerbers, drill files, BOM and CPL are opened and visually inspected in a viewer
  before any submission. Layer count, outline, drill sizes and rotation/offsets of the
  CPL are checked.
- Outputs are stored per revision in `manufacturing/<rev>/` and never overwritten.

## 11. Physical testing
- A written test plan exists before boards arrive.
- Bring-up is incremental (visual inspection → continuity/short check → current-limited
  power-up → functional tests).
- Results, measurements and photos are stored in `testing/`.
- **No claim of working hardware without recorded test evidence.**

## 12. Traceability
- Decisions are logged with date, rationale and source in `docs/design-reviews/`.
- Every revision has a changelog entry and a git tag.
