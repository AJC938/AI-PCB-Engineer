# Manufacturer Comparison — V0.2.0 (Gate B)

Requirement: **full factory assembly / full turnkey** of a 2-layer FR-4 board with 44 SMT and 8 THT placements
(2.54 mm headers, 5.08 mm terminal block, 5 mm LEDs), shipped to Saudi Arabia. JLCPCB was excluded by
instruction. All sources are official manufacturer pages, **checked 2026-11-09**. Pages were read through a fetch
tool. Pages that could not be read are stated as such, and nothing was inferred from memory.

## Sources
| Vendor | Read | Not readable (reason) |
|---|---|---|
| PCBWay | pcbway.com/capabilities.html, /assembly-capabilities.html | shipping_method_guide.aspx, helpcenter shipping page (fetch refused / connection reset) |
| NextPCB | nextpcb.com/pcb-capabilities, /pcb-assembly-services | /pcb-assembly-capabilities, PCBA guide PDF, /shipment (refused / reset) |
| Seeed Fusion | wiki.seeedstudio.com/Service_for_Fusion_PCB (updated 2026-09-16), seeedstudio.com/pcb-assembly.html, /fusion_pcb.html | PCBA service PDF (compressed, unreadable), shipping help page (empty) |
| Eurocircuits | eurocircuits.com/services/pcb-assembly-capabilities/ | standard-pool, technical guidelines, classification (fetch refused) |

## Capability facts
| Criterion | PCBWay | NextPCB | Seeed Fusion | Eurocircuits |
|---|---|---|---|---|
| 2 L FR-4 1.6 mm 1 oz | yes (std list) | yes | yes | NOT RETRIEVED (pool page refused) |
| Min track/space | 0.10/0.10 mm (4 mil) | 3/3 mil (1 oz) | 4/4 mil | NOT RETRIEVED |
| Min drill | 0.15 mm std / 0.20 mm adv (conflict) | 0.15 mm (≤1.2 mm board) | 0.2 mm | NOT RETRIEVED |
| Annular ring | 0.15 mm (std) | 3.5 mil | NOT FOUND | NOT RETRIEVED |
| Copper to edge | 0.25 mm (adv, CNC) | 0.2 mm | 0.3 mm | NOT RETRIEVED |
| Silkscreen | ≥ 0.8 mm / 0.15 mm | ≥ 0.76 / 0.12 mm | ≥ 23 mil / 4 mil | NOT RETRIEVED |
| Finishes | HASL (lead/LF), immersion gold, OSP, ENIG (adv)… | "multiple finishes" (list on another page) | HASL LF, ENIG, OSP, hard gold | NOT RETRIEVED |
| SMT + **THT** + mixed | "SMT, Thru-Hole (THT) and hybrid of both"; single/double side | SMT, THT, mixed; single/double; wave-soldering line in factory photos; "Automated/Manual soldering" | SMT, THT, mixed; single/double (wiki) | SMT/THT single or double sided; max 800 THT placements |
| THT soldering method named | NOT FOUND (sub-page not read) | wave (photos); selective/hand not named | NOT FOUND | NOT FOUND |
| Lead-free assembly | leaded and lead-free | lead-free RoHS (and standard) | NOT FOUND | SAC305 lead-free |
| Sourcing | turnkey / partial / consigned; "we will always ask for your approval"; no parts markup | full / partial turnkey / consigned; HQ Online + Digikey/Mouser/… | turnkey via OPL (150k) + BOM procurement; consigned NOT FOUND | all parts sourced; customer may supply unsourceable parts |
| Substitution approval | **explicit: approval before decisions** | NOT FOUND | NOT FOUND | NOT FOUND |
| Assembly MOQ | 5 pcs | none (1 pc) | 1 pc (wiki) / "no minimum" | 1–50 pcs |
| DFM/DFA review | capability check vs specs | free DFM + DFA every order | free DFA every order | NOT FOUND |
| Testing | AOI, X-ray, ICT, functional; flying probe free | AOI, X-ray, ICT, FCT | AOI, X-ray, ICT, functional | SPI, X-ray, visual |
| Shipping carriers | FedEx, UPS, DHL, TNT, EMS… (footer). Saudi Arabia appears in the DHL quote country list (search result; INDICATED, not confirmed on a readable page) | DHL/FedEx "to 166 countries"; Saudi not named | NOT FOUND | NOT FOUND (EU-based) |
| Lead time (published) | "24 hours to a few weeks" | conflicting: 5–7 / 7 / 14+ / ~20 business days | 7 working days (OPL parts only) | 3/5/7/10 WD after bare boards |
| Pricing transparency | online quote; no parts markup | online quote; promotions | online quote | online price ≤ 200 BOM lines |

## Weighted evaluation (weights from the V0.2.0 prompt; scores 1–5 from the facts above)
| Criterion (weight) | PCBWay | NextPCB | Seeed | Eurocircuits |
|---|---|---|---|---|
| Full SMT/THT assembly (30 %) | 5 | 5 | 4 (THT stated, method/lead-free not found) | 4 (THT yes, ≤ 50 pcs) |
| Component sourcing (20 %) | 5 (all models + explicit approval policy) | 4 (broad sourcing; approval policy not found) | 3 (OPL-centric; consigned not found) | 4 |
| PCB capability (15 %) | 5 | 5 | 5 | 3 (values not retrievable) |
| DFM/engineering support (10 %) | 3 | 5 | 5 | 3 |
| Shipping to Saudi Arabia (10 %) | 4 (country listed, INDICATED) | 3 (166 countries, KSA not named) | 2 (not found) | 1 (not found) |
| Cost transparency (10 %) | 4 | 4 | 3 | 4 |
| Lead time / reliability (5 %) | 3 | 3 | 3 | 4 |
| **Weighted score** | **4.50** | **4.40** | **3.70** | **3.45** |

Scores separate published evidence from assumptions. No price, shipping cost or turnaround is claimed for this
board, because no quote was requested.
