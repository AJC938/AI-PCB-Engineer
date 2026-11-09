# Manufacturer Selection Recommendation — V0.2.0

**Recommended provisional target: PCBWay (score 4.50). Alternate: NextPCB (4.40).** Status: **PROVISIONAL — awaits
the owner's explicit approval.** No account, upload, quote or order was made.

## Why PCBWay
1. It explicitly publishes **THT and hybrid SMT+THT assembly**, single or double sided, with leaded or lead-free
   solder. This is a full-assembly service, not just SMT.
2. Its turnkey sourcing states that it **asks the customer's approval before parts decisions**. That matches the
   "no substitution without approval" requirement. NextPCB's policy was not found.
3. Its standard capabilities cover the board with at least ×2 margin (GENERIC_DFM_PROFILE.md).
4. Saudi Arabia appears in its DHL country list. This is **INDICATED only**, because the shipping page was not
   readable from here.

## Why NextPCB remains a close alternate
It offers free DFM and DFA on every order, no MOQ, a wave-soldering line and broad distributor sourcing. Choose it
if PCBWay cannot source TPS26600PWPR or HTSW headers, or if its quote/shipping to KSA is unfavourable.

## Not recommended
- **Seeed Fusion.** THT is stated, but the soldering method, lead-free assembly, consigned parts and shipping
  were not found.
- **Eurocircuits.** EU-based, limited to 50 pcs, and its PCB pool data and shipping outside Europe could not be
  verified.

## What the owner must confirm with the chosen vendor (before any commitment)
- THT method for J1–J6/LEDs (selective, wave or hand) and lead-free compatibility.
- Turnkey stock of **TPS26600PWPR** (TI store "Out of stock" 2026-11-09). If the vendor cannot source it:
  consignment, or a design revision (no drop-in alternate exists).
- Shipping service, cost and duties to Saudi Arabia; payment method; lead time for this BOM.
- CPL rotation convention and polarity, confirmed against ASSEMBLY_NOTES.md.
- Requested finish ENIG, or acceptance of lead-free HASL.

The manufacturer-specific profile (`manufacturing/v0.2.0/manufacturer_profiles/PCBWAY_PROVISIONAL_PROFILE.md`)
is **not** final until the supplier is approved. The layout uses only the generic (strictest common) rules, so
it stays valid for either vendor.
