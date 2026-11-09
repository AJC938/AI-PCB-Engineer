# Generic (vendor-independent) DFM profile — V0.2.0

Status: **APPLIED** to the V0.2.0 layout. Every value is at least as strict as the strictest of the shortlisted
manufacturers' published standard capabilities (sources checked 2026-11-09, see
[`reports/v0.2.0/MANUFACTURER_COMPARISON.md`](../../../reports/v0.2.0/MANUFACTURER_COMPARISON.md)).

| Rule | Design value | PCBWay (std) | NextPCB | Seeed Fusion | Margin vs strictest |
|---|---|---|---|---|---|
| Layers / material | 2 / FR-4 | 1–14, FR-4 | 1–32, FR-4 Tg130/150/170 | FR-4 Tg130/150/170 | — |
| Thickness | 1.6 mm | 0.2–3.2 (1.6 listed) | 0.6–3.2 (1.6 listed) | 0.6–3.0 (1.6 listed) | standard |
| Copper (outer) | 1 oz | 1–8 oz | 1/2 oz | 1/2/3 oz | standard |
| Min track | **0.25 mm** signals (0.20 rule) | 0.10 mm | 0.08 mm (1 oz) | 0.10 mm (1 oz) | ×2.0 |
| Min clearance | **0.20 mm** | 0.10 mm | 0.08 mm | 0.10 mm | ×2.0 |
| Via | **0.6 / 0.3 mm** (annular 0.15) | drill ≥ 0.15 (0.20 adv.), ring ≥ 0.15 | drill ≥ 0.15, ring ≥ 0.09 | drill ≥ 0.20 | = PCBWay ring, drill ×1.5 |
| Min mechanical hole | 0.3 mm (vias) | 0.15 / 0.20 mm | 0.15 mm | 0.20 mm | ×1.5 |
| PTH hole tolerance | design assumes ±0.08 mm | ±0.08 mm | ±0.075 mm | NOT FOUND | — |
| Copper to board edge | **0.5 mm** | 0.25 mm (adv., CNC) | 0.20 mm | 0.30 mm | ×1.7 |
| Solder-mask web | KiCad 0 expansion; min web ≥ 0.1 mm (pads ≥ 0.2 mm apart) | 4 mil (0.10) green | 3.5 mil green | 0.10 mm | = |
| Silkscreen | **1.0 mm** text, 0.15 mm stroke | ≥ 0.8 mm / ≥ 0.15 mm | ≥ 0.76 mm / ≥ 0.12 mm | ≥ 0.58 mm / ≥ 0.10 mm | ×1.25 height |
| Outline tolerance | 90 × 64 mm ±0.2 | ±0.2 mm CNC | ±0.15 mm | ±0.2 mm | — |
| Surface finish | **ENIG preferred** (0.65 mm HTSSOP + PowerPAD coplanarity); lead-free HASL acceptable | both | listed generically | both | — |
| Board size | 90 × 64 mm (single board, no panel required by the design) | min 10 × 10 | min 10 × 10 | min 10 × 10 | — |

Conflicts between vendors (documented, not silently resolved): PCBWay's standard page lists 0.15 mm min drill
while its advanced page lists 0.20 mm; the design uses 0.30 mm, so the conflict has no impact.
