# Open Questions — V0.2.0

Only real unresolved items are listed. V0.1.0 items closed by this milestone are at the end.

## Owner decisions / external actions (nothing has been done externally)
| ID | Question | Blocks | Next step |
|---|---|---|---|
| OQ2-01 | **Approve the manufacturer** (recommended PCBWay, alternate NextPCB) | ordering; final vendor DFM profile | owner approval, then request a quote (owner action) |
| OQ2-02 | **TPS26600PWPR availability** (TI store "Out of stock" 2026-11-09; no drop-in alternate) | assembly | vendor turnkey quote. If unavailable: consign, wait, or authorise a design revision |
| OQ2-03 | Vendor THT method (selective, wave or hand) and lead-free process for J1–J6 and LEDs | full-assembly claim | written vendor confirmation |
| OQ2-04 | Shipping to Saudi Arabia: service, cost, duties, lead time | delivery | vendor quote |
| OQ2-05 | Quantity / budget (OQ-17) | quote | owner |
| OQ2-06 | Finish: ENIG (preferred) or lead-free HASL | order form | owner/vendor |
| OQ2-07 | CPL rotation convention of the chosen vendor | first-article placement | vendor engineering check |

## Physical verification (V0.3.0)
| ID | Item | Method |
|---|---|---|
| NQ-01 | Adafruit 4007 physical pin order and jumper-wire mating to J3 | inspect the module; wire by label |
| NQ-02 | Real Echo/Trigger levels | oscilloscope |
| NQ-03 | DevKit clone pin labels for the J2 harness | read the clone silkscreen |
| NQ-04 | 3V3_ESP with the board attached | DMM |
| NQ2-08 | OVP trip (5.39–5.82 V), UVLO (4.25–4.56 V), current limit (0.51–0.69 A), reverse polarity | bench supply ramp, electronic load. Current-limited supply for the reverse test |
| NQ2-09 | LDO tab temperature at full DESIGN load (CALCULATED ≈ 94.7 °C Tj at 50 °C) | thermocouple / IR |
| NQ2-10 | +3V3_P load-transient response with C3/C4 at 7.6–8.8 mm | oscilloscope |

## Low-risk documentation items
| ID | Item |
|---|---|
| NQ-06 | 10 µF X5R DC-bias derating (Samsung page has no curve) |
| NQ2-11 | Panasonic ERJ-3 vendor land pattern not obtained (IPC-7351 nominal used) |
| NQ2-12 | Vendor STEP models (LED2 shown with a red generic model) |

## Closed by V0.2.0
| Item | Closure |
|---|---|
| OQ-16 Fab and assembly choice | researched; provisional recommendation (approval pending, OQ2-01) |
| R-32 TVS clamp above abs max | **closed by design**: eFuse OVP (TVS_LDO_PROTECTION_ANALYSIS.md) |
| NQ-05 SMAJ6.0A band vs pad 1 | obsolete (TVS removed) |
| NQ-07 Fabrication design rules | generic DFM profile applied |
| V0.1.0 F-1 schematic cosmetic overlaps | references re-placed on the PCB; schematic overlaps remain cosmetic |
