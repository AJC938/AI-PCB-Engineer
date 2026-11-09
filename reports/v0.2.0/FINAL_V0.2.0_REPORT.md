# Final Report — V0.2.0: PCB Layout, DFM, DFA and Manufacturing Package
Sensor Interface & Power Management Board for ESP32 · 2026-11-09 · branch `design/v0.2.0-pcb-layout`

## 1. Status
**Digital design: COMPLETE. Manufacturer: PROVISIONAL (owner approval pending). Physical: NOT FABRICATED,
NOT TESTED.** No order, upload, account, purchase or push was made.

## 2. Electrical design review (Gate A)
- **TVS/LDO:** the V0.1.0 protection was not valid. SMAJ6.0A breakdown is ≥ 6.67 V, above the TLV1117LV's 6.0 V
  absolute maximum. **TPS26600 eFuse** replaces F1/Q1/R1/D1 (DDR-17):
  - OVP trip 5.39–5.82 V worst case (Monte Carlo 5.395–5.817 V);
  - reverse polarity blocked to −60 V;
  - 0.51–0.69 A current limit;
  - 1.97 ms soft start.

  Documented limits: overvoltage stepping faster than 23.8 V/ms while powered; no surge rating; earth-loop
  reverse-polarity path.
- **Architecture B preserved.** +3V3_P and 3V3_ESP share no node, and the DevKit 5V is not connected. Back-feed
  paths are quantified (≤ 2.5 mA I2C, ≤ 12 mA UART TX into an unpowered device). **R-31: power the board first or
  together with the ESP32.**
- **Thermal:** the V0.1.0 81.8 °C used a JEDEC 4-layer RθJA and is withdrawn. TI LM1117 2-layer copper data
  (+10 %) with 251 mm² solid +3V3_P copper gives **Tj ≈ 94.7 °C at 50 °C ambient** (target ≤ 110 °C).
- **Other schematic changes:**
  - R15 1 kΩ TRIG series resistor (DDR-18);
  - H1–H4 and FID1–FID3 added to the schematic for parity (DDR-19);
  - TI PWP0016A footprint (DDR-20);
  - thermal copper requirement (DDR-21).
- **J3:** signal names verified (Adafruit). Physical module pin order unpublished → board interface uses
  labelled individual jumpers (order-independent). Mechanical mating NOT VERIFIED.

## 3. Manufacturer research (Gate B)
| Vendor | Score | Full SMT+THT | Sourcing | KSA shipping |
|---|---|---|---|---|
| **PCBWay (recommended)** | 4.50 | yes (SMT, THT, hybrid; lead/lead-free) | turnkey/partial/consigned, approval before decisions | Saudi Arabia in DHL country list (INDICATED) |
| NextPCB (alternate) | 4.40 | yes (wave line; lead-free) | full/partial/consigned, global distributors | 166 countries via DHL/FedEx; KSA not named |
| Seeed Fusion | 3.70 | yes (method not found) | OPL + BOM procurement | not found |
| Eurocircuits | 3.45 | yes (≤ 50 pcs) | sourced + customer-supplied | not found |
Remaining commercial items:
- THT soldering method;
- **TPS26600PWPR stock** (TI store out of stock 2026-11-09);
- KSA shipping/duties;
- price, lead time, quantity.

## 4. PCB layout
| Item | Value |
|---|---|
| Board | 90.0 × 64.0 mm, 2 layers FR-4 1.6 mm, 1 oz, ENIG preferred |
| Placement | 61 footprints (52 assembled, 4 M3 holes, 3 fiducials, 2 solder jumpers), all top side |
| Routing | 31/31 nets, 331 tracks (F.Cu 776 mm, B.Cu 46 mm), 57 vias; widths 0.5/0.4/0.3/0.25 mm |
| Zones | +3V3_P thermal 251.2 mm² (solid), EF_RTN island 38 mm², GND top 3419 mm², GND bottom plane 5342 mm² |
| Silkscreen | 54 references placed legally plus a full connector/GPIO pin-map legend and the R-31 rule |

## 5. Validation
| Check | Result |
|---|---|
| ERC (MCP + kicad-cli, all severities) | **0** |
| DRC (kicad-cli, all severities, refilled and stored zones) | **0 errors, 0 warnings** |
| Unconnected items | **0** |
| Schematic parity | **0** |
| Netlist/domain verifier | PASS |
| Manufacturing audit | 11/11 PASS |
| Reopen in a fresh MCP process | PASS |
| DFM / DFA | PASS on the generic profile; vendor confirmation pending |

## 6. Manufacturing package (`manufacturing/v0.2.0/`)
- `gerbers/`:
  - Sensor_Interface_Power_Board-F_Cu.gtl, -B_Cu.gbl, -F_Mask.gts, -B_Mask.gbs, -F_Paste.gtp, -B_Paste.gbp,
    -F_Silkscreen.gto, -B_Silkscreen.gbo, -Edge_Cuts.gm1, -job.gbrjob
  - -PTH.drl, -NPTH.drl and drill-map PDFs
  - Sensor_Interface_Power_Board_v0.2.0.d356
- `assembly/`: …_BOM.csv, …_CPL.csv, …_assembly_drawing_top.pdf, …_assembly_drawing_bottom.pdf, …_layers.pdf,
  …_schematic.pdf
- `3d/`: …_v0.2.0.step
- `docs/`: FABRICATION_NOTES.md, ASSEMBLY_NOTES.md
- `manufacturer_profiles/`: GENERIC_DFM_PROFILE.md (applied), PCBWAY_PROVISIONAL_PROFILE.md,
  NEXTPCB_ALTERNATE_PROFILE.md

## 7. MCP findings (V0.2.0)
**New defects:**
- **D-23:** `add_zone` → "Unknown command" (SWIG). Workaround: `add_copper_pour`.
- **D-24:** `sync_schematic_to_board` leaves no-connect pads without nets.

**Other limitations:**
- `add_schematic_component` writes `in_bom yes` in a compact format.
- `refill_zones` refuses its own save.
- No MCP tool for the PCB title block, zone pad connection or BOM flags.

Each workaround is a small documented script verified by kicad-cli. All copper, placement, outline, origin
and silkscreen changes went through MCP:
- schematic: full build 364/364, incremental H/FID 10/10;
- PCB:
  - sync 2/2;
  - placement 65/65 + 3/3 + 4/4;
  - first routing pass 396/400 (the 4 failures are `add_zone`, D-23; this pass was later ripped up);
  - copper pours 6/6;
  - rip-up 33/33;
  - final routing 390/390;
  - silkscreen 77/77;
  - refill 4/5 (save refused, D-1 pattern);
  - origin 2/2;
  - reopen 7/7.

## 8. Risk status (summary)
| Status | Risks |
|---|---|
| Closed by design | R-01, R-02, R-03, R-05, R-10, R-19 (generic rules applied), R-30, R-32 |
| Mitigated | R-04, R-08, R-09, R-11, R-12, R-21, R-40 |
| Open (test / vendor) | R-06/R-15/R-41 thermal measurement; R-13 burst noise; R-31 sequencing (rule documented); R-34 sensor pin order; R-35; R-36 TPS26600 stock; R-39 vendor CPL/substitution |
| Accepted | R-33, R-37, R-38 |

## 9. Remaining dependencies (real items only)
1. Owner approves the manufacturer, then obtains a quote with THT method, TPS26600PWPR stock, KSA shipping and price.
2. Owner decides quantity, budget and finish.
3. Physical checks in V0.3.0:
   - ultrasonic pin order;
   - DevKit labels;
   - OVP/UVLO/ILIM thresholds;
   - LDO temperature;
   - transient response.

## 10. Next milestone
**V0.3.0 (fabrication and physical validation) can begin as soon as the owner approves the supplier and the quote
confirms THT assembly and TPS26600PWPR availability.** The design files need no change for either the
recommended or the alternate vendor. Bring-up follows docs/ENGINEERING_RULES.md §11:
1. visual inspection;
2. continuity checks;
3. current-limited power-up;
4. OVP/UVLO/reverse tests;
5. functional tests with the ESP32.
