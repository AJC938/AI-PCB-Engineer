# PCBWay — PROVISIONAL manufacturer profile (not approved)

Status: **PROVISIONAL**. Recommended target pending the owner's explicit approval. No account, upload, quote
or order has been made. Sources read 2026-11-09: https://www.pcbway.com/capabilities.html,
https://www.pcbway.com/assembly-capabilities.html (shipping pages could not be fetched from this network).

## Order parameters to request (when the owner approves)
| Item | Value |
|---|---|
| Service | PCB + PCB Assembly, **Turn-key** (PCBWay sources all parts), quantity per owner (min. 5 for assembly) |
| Board | 2 layers, FR-4 (Tg ≥ 130), 1.6 mm, 1 oz outer copper, 90 × 64 mm, single board (no panel requested) |
| Finish / mask / silk | ENIG preferred (HASL lead-free acceptable), green mask, white silkscreen |
| Assembly | Top side only: 44 SMT placements + 8 THT parts (J1, J2–J6, LED1, LED2), lead-free (RoHS) |
| THT soldering | Factory to confirm method (wave, selective or hand) for 2.54 mm headers, 5.08 mm terminal block, 5 mm LEDs |
| Files | Gerber X2 + Excellon (`gerbers/`), BOM and CPL (`assembly/`), assembly drawing PDF |
| Substitution | **No substitution without written approval** (PCBWay states it asks approval before parts decisions) |
| Testing | Flying probe (free per capability page), AOI; IPC-D-356 netlist provided |

## Items the owner must confirm with PCBWay before ordering
1. THT soldering method and lead-free compatibility for Samtec HTSW and Phoenix 1715721.
2. Turn-key availability of **TPS26600PWPR** (TI shows "Out of stock" 2026-11-09) and SN74LVC1T45DBVR.
3. CPL rotation convention (file uses KiCad footprint orientation; see `docs/ASSEMBLY_NOTES.md`).
4. Shipping service to Saudi Arabia, cost and import duties (not readable on the official pages from here).
5. Whether fiducials are required (3 global fiducials are provided).
