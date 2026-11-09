# BOM and Sourcing Audit — V0.3.0 (release Rev A)

BOM: `manufacturing/Sensor_Interface_Power_Board/RevA/assembly/Sensor_Interface_Power_Board_RevA_BOM.csv`.
**33 lines, 52 placements (44 SMT + 8 THT), top side, no DNP.** Generated from the schematic netlist by
`build/make_bom.py`, then `scripts/release/enrich_bom.py` adds engineering descriptions, dated sourcing notes and
verified alternatives (`scripts/release/bom_enrichment.csv`). **No MPN was changed.** The BOM is identical to
V0.2.0 in references, quantities, manufacturers, MPNs and packages (diff checked).

## 1. Integrity checks (independent audit `scripts/release/audit_release.py`)
| Check | Result |
|---|---|
| Placements = schematic parts with `in_bom` | 52 = 52 |
| Lines | 33. Qty column = number of references on every line |
| Manufacturer + exact MPN on every line | yes |
| Required columns (Reference, Qty, Manufacturer, MPN, Description, Value, Package, SMT/THT, Side, DNP, Sourcing, Alternative) | present |
| BOM references ⊂ CPL; CPL = BOM + 3 fiducials | yes |
| Excluded PCB features | H1–H4, FID1–FID3, JP1, JP2 (not purchased parts) |

## 2. Availability evidence (checked 2026-11-09)
Rules followed: a part is not declared unavailable only because the manufacturer's store is out of stock, and it
is not declared available without the exact suffix and package. Search-engine summaries are **not** treated as
evidence of stock.

| MPN | Package | Evidence | Assessment |
|---|---|---|---|
| **TPS26600PWPR** | HTSSOP-16 PWP (TI page "PWP \| 16"; DigiKey "16-HTSSOP") | **TI product page:** lifecycle ACTIVE, inventory "Out of stock", no pricing shown. **DigiKey 6199305:** Part Status "Active", **In-Stock: 0**, "2,000 expected in stock on 14-Dec-2026", manufacturer standard lead time **26 weeks**, $3.79 at qty 1 (cut tape). The page was read through a fetch tool, and only part of it was verbatim. **LCSC C544399:** MPN and "HTSSOP-16-EP" listed; stock and price not readable. **Mouser:** page timed out | **ACTIVE but constrained.** No confirmed stock at the date checked. Main sourcing risk (L-6) |
| TPS26600PWPT | HTSSOP-16 PWP, 250-pc reel | TI: ACTIVE, out of stock | Same device and package (carrier variant only). Acceptable as a turnkey alternative **with written approval** |
| SN74LVC1T45DBVR | SOT-23-6 DBV | TI store: ACTIVE, out of stock (V0.2.0, 2026-11-09). DigiKey page blocked by the fetch tool. Search snapshots (undated) show distributor stock | **Not verified.** Confirm in the quote. Carrier variant DBVT is acceptable with approval |
| TLV1117LV33DCYR, SN74LVC1G17DBVR | SOT-223 / SOT-23-5 | TI addendum: Active / Production | Lifecycle verified; stock not verified |
| Samtec HTSW-104-07-T-S | THT 1×4 | samtec.com: "Ships Tomorrow: 3268 pieces" (V0.2.0, 2026-11-09) | Available at the date checked |
| Passives, Phoenix 1715721, HTSW-112, LEDs, Keystone 5015 | — | official pages not readable from the research network | Common catalogue parts; stock **not verified**. Must be confirmed in the quote |

## 3. Options if TPS26600PWPR is still unavailable when ordering (owner decision; nothing is changed now)
1. Wait for distributor stock (DigiKey showed an expected date of 2026-12-14; not guaranteed).
2. Ask the assembler to source or reserve it, or consign parts bought by the owner (partial turnkey).
3. Approve the TPS26600PWPT carrier variant (same silicon and package, no design change).
4. A different eFuse means a **design revision (Rev B)**: new datasheet verification, OVP/UVLO divider and
   current-limit recalculation, footprint check and full re-validation. It is **not** a BOM substitution.

## 4. Alternatives policy
Only carrier variants of the same TI device (DBVT/PWPT) are listed as verified alternatives, because they share
the datasheet, package and footprint. Every other line says "None verified". Each BOM line carries
"NO SUBSTITUTION without written approval".
