# Full Assembly Requirements (Turnkey SMT + THT)

The owner's intended assembly method is **FULL FACTORY ASSEMBLY / FULL TURNKEY**: the factory solders every
part, including the through-hole connectors. **No manufacturer has confirmed this for this board yet.**

| Requirement | Detail | Confirmed by a supplier? |
|---|---|---|
| Single-sided assembly | All 52 parts on top; no bottom paste | Design fact |
| SMT | 44 placements, smallest 0603, finest pitch 0.65 mm (U5 HTSSOP with PowerPAD) | Standard capability of every candidate (published) |
| THT | J1 Phoenix 1715721 (5.08 mm), J2 HTSW-112, J3–J6 HTSW-104 (2.54 mm), LED1/LED2 5 mm | THT assembly is published by PCBWay, NextPCB, Seeed and Eurocircuits. **The method for this board is NOT confirmed** |
| Lead-free | All parts lead-free solderable (Samtec HTSW is the lead-free version) | Supplier-dependent |
| Sourcing | Exact MPNs; TPS26600PWPR has limited stock | **Supplier-dependent** |
| Substitution | Not allowed without written approval | Must be agreed per order |
| Inspection | AOI; X-ray of the U5 PowerPAD recommended; first-article polarity check | Supplier-dependent |

## Possible approved assembly approaches
1. **Full turnkey with THT** (preferred): the factory does SMT reflow, then wave, selective or hand soldering of the 8 THT parts.
2. **Turnkey SMT + consigned THT parts:** the owner supplies J1–J6/LEDs, and the factory solders them.
3. **Turnkey SMT only + owner hand-solders THT:** a fallback if a supplier cannot do THT.
4. **Consigned U5:** if the factory cannot source TPS26600PWPR, the owner buys and ships it (partial turnkey).

No approach is claimed to be universally supported. The supplier's written quote decides.
