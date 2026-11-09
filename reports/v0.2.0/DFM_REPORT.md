# DFM Report — V0.2.0

Rule sets:
- **Generic profile (applied)**: `manufacturing/v0.2.0/manufacturer_profiles/GENERIC_DFM_PROFILE.md`, strictest common values of PCBWay, NextPCB and Seeed.
- **PCBWay provisional** and **NextPCB alternate** profiles: documented, not approved.

| Check | Design | Strictest published | Status |
|---|---|---|---|
| Track / space | 0.25 / 0.20 mm (rule 0.20/0.20) | 0.10 / 0.10 mm | PASS (×2) |
| Via drill / pad / ring | 0.30 / 0.60 / 0.15 mm | drill 0.20 (Seeed), ring 0.15 (PCBWay std) | PASS (ring = limit, drill ×1.5) |
| Smallest PTH | 0.9 mm (LED leads) | — | PASS |
| Hole-to-hole | KiCad DRC min hole clearance 0.25 mm: 0 violations | 0.30 mm different nets (NextPCB) | PASS (DRC checked at 0.25 mm; the router enforces ≥ 0.30 mm drill edge-to-edge for every via) |
| Copper to edge | ≥ 0.5 mm (DRC rule) | 0.30 mm (Seeed) | PASS |
| Annular ring THT | J1 (2.6−1.3)/2 = 0.65; headers 0.35; LEDs 0.45 mm | 0.15 mm | PASS |
| Solder mask | expansion 0 (pad-defined), U5 EP mask-defined 3.3 × 3.3; DRC solder_mask_bridge: 0 | dam ≥ 0.10 mm | PASS |
| Silkscreen | 1.0 mm / 0.15 mm; DRC silk_overlap and silk_over_copper: 0 | ≥ 0.8 / 0.15 mm | PASS |
| Board size / outline | 90 × 64 mm rectangle, Edge.Cuts 0.05 mm line | ≥ 10 × 10 mm | PASS |
| Copper balance | top 3419 + 251 + 38 mm² of zones; bottom 5342 mm² plane | — | PASS (both layers heavily copper-filled; low warp risk) |
| Acid traps / slivers | zone min width 0.2 mm, island removal default; DRC 0 | — | PASS |
| Impedance | none required | — | N/A |
| Finish | ENIG preferred (0.65 mm pitch + PowerPAD), HASL LF acceptable | both offered | PASS |

**Conflicts between vendors**: the PCBWay standard page gives min drill 0.15 mm and the advanced page 0.20 mm.
The design uses 0.30 mm, so there is no impact. NextPCB requires 0.30 mm hole-to-hole between different nets
(PCBWay ≥ 16 mil = 0.41 mm for component holes, advanced). The design's closest different-net drill pair is
LED pads at 2.54 mm pitch (drill edge-to-edge 1.64 mm), and the router keeps every via drill ≥ 0.30 mm edge-to-edge from any other drill, so the stricter value is met.

**Manufacturer-specific DFM**: still PROVISIONAL until the owner approves a supplier. The vendor's own DFM review
(free at NextPCB and Seeed; engineering check at PCBWay) will be the final step before production.
