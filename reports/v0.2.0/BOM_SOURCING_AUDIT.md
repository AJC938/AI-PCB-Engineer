# BOM Sourcing Audit — V0.2.0 (Gate B §6.2)

BOM: `manufacturing/v0.2.0/assembly/Sensor_Interface_Power_Board_v0.2.0_BOM.csv`, 33 lines, 52 placements
(44 SMT, 8 THT). Changes since V0.1.0: −F1, −Q1, −R1, −D1; +U5, +C12, +C13, +R15–R19.

Evidence column:
- **TI-ADD**: the TI datasheet package addendum states the orderable MPN is "Active / Production".
- **TI-WEB**: TI product page read 2026-11-09.
- **SAMTEC-WEB**: samtec.com product page read 2026-11-09.
- **NOT VERIFIED**: no readable official stock source from this environment. It must be confirmed in the vendor's turnkey quote.

Distributor pages were not used as authority.

| Ref | MPN | Package | Mount | Stock / lifecycle evidence | Assembly support | Alternative (requires approval) |
|---|---|---|---|---|---|---|
| U5 | TPS26600PWPR | HTSSOP-16 PWP | SMT | TI-ADD Active (addendum 10-Nov-2025). **TI-WEB: ACTIVE, "Out of stock" (TI store)** | standard SMT, MSL 2 | none drop-in: TPS26600PWPT (250-reel, same die, also out of stock at TI). Redesign if unavailable (R-36) |
| U1 | TLV1117LV33DCYR | SOT-223 DCY | SMT | TI-ADD Active Production (addendum 14-Jun-2026). TI-WEB not readable | standard | none listed (no DCYT variant in the TI addendum; checked) |
| U2, U4 | SN74LVC1G17DBVR | SOT-23-5 | SMT | TI-ADD Active Production | standard | SN74LVC1G17DBVT (TI-ADD Active Production, small reel, same device) |
| U3 | SN74LVC1T45DBVR | SOT-23-6 | SMT | TI-ADD Active Production. **TI-WEB: ACTIVE, "Out of stock" (TI store)** | standard | SN74LVC1T45DBVT (TI-ADD Active Production; TI-WEB also out of stock) |
| J1 | Phoenix 1715721 | THT 2-pos 5.08 mm | THT | NOT VERIFIED (phoenixcontact.com 403) | THT soldering required | none without approval |
| J2 | Samtec HTSW-112-07-T-S | THT 1×12 2.54 | THT | NOT VERIFIED (samtec page refused) | THT | — |
| J3–J6 | Samtec HTSW-104-07-T-S | THT 1×4 2.54 | THT | SAMTEC-WEB: "Ships Tomorrow: 3268 pieces" | THT | — |
| LED1 | Kingbright WP7113ID | 5 mm THT | THT | NOT VERIFIED (kingbrightusa.com redirect) | THT | — |
| LED2 | Kingbright WP7113SGD | 5 mm THT | THT | NOT VERIFIED | THT | — |
| TP1–TP8 | Keystone 5015 | SMT test point | SMT | NOT VERIFIED (keyelco.com 403) | SMT (tape and reel) | — |
| R2–R19 (14 values) | Panasonic ERJ-3EKF…V | 0603 | SMT | NOT VERIFIED (high-volume family) | standard | 1 % 0603 thick film of the same value (approval needed) |
| C1, C3, C8 | Samsung CL10A106KP8NNNC | 0603 | SMT | NOT VERIFIED | standard | 10 µF ≥ 10 V X5R/X7R 0603 (approval) |
| C2, C4–C7, C9–C11 | Murata GRM188R71C104KA01D | 0603 | SMT | NOT VERIFIED | standard | 100 nF ≥ 16 V X7R 0603 |
| C12 | Samsung CL10A105KB8NNNC | 0603 | SMT | Samsung spec page read (1.0 µF ±10 % 50 V X5R) | standard | 1 µF ≥ 50 V X5R/X7R |
| C13 | Samsung CL10B473KB8NNNC | 0603 | SMT | Samsung spec page read (47 nF ±10 % 50 V X7R) | standard | 47 nF ≥ 16 V X7R |

## Findings
1. **Highest sourcing risk: U5 TPS26600PWPR** (TI store out of stock on 2026-11-09). The vendor quote must
   confirm it before approval. If it is unavailable: consign it, wait for stock, or start a design revision
   (an alternative OVP eFuse with re-verified thresholds). This is a human decision.
2. THT parts need factory THT soldering. Every recommended vendor publishes THT assembly, but the method must be
   confirmed (MANUFACTURER_SELECTION_RECOMMENDATION.md).
3. Every BOM line carries "NO SUBSTITUTION without written approval". Alternatives above are candidates only and
   would need datasheet re-verification and recalculation if used.
4. Lead-free compatibility: HTSW (lead-free solderable) replaced TSW in V0.1.0. TI parts are NiPdAu/Sn,
   RoHS "Yes" (TI-ADD).
