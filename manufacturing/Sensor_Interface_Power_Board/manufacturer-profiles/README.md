# Manufacturer Profiles — Rev A

**No manufacturer is confirmed for this design.** Nothing has been uploaded, quoted or ordered. The standard
package in `../RevA/` works with any qualified PCB + PCBA manufacturer. These profiles only help someone who
chooses one of the researched suppliers.

| Profile | Status | Basis |
|---|---|---|
| [GENERIC_DFM_PROFILE.md](GENERIC_DFM_PROFILE.md) | **Applied to the design** (vendor-independent rules) | Strictest published standard capability of the shortlisted vendors |
| [PCBWAY_PROFILE.md](PCBWAY_PROFILE.md) | Candidate (recommended in V0.2.0, **not approved**) | Official pages read 2026-11-09 |
| [NEXTPCB_PROFILE.md](NEXTPCB_PROFILE.md) | Candidate (alternate, **not approved**) | Official pages read 2026-11-09 |
| [OTHER_CANDIDATES.md](OTHER_CANDIDATES.md) | Seeed Fusion, Eurocircuits (researched, lower score) | Official pages read 2026-11-09 |

Full comparison, weighting and sources: [`reports/v0.2.0/MANUFACTURER_COMPARISON.md`](../../../reports/v0.2.0/MANUFACTURER_COMPARISON.md)
and [`reports/v0.2.0/MANUFACTURER_SELECTION_RECOMMENDATION.md`](../../../reports/v0.2.0/MANUFACTURER_SELECTION_RECOMMENDATION.md).

## What every quote must confirm (any supplier)
1. Full turnkey **SMT + THT** assembly, top side, lead-free, and the THT soldering method (wave, selective or hand).
2. Sourcing of every exact MPN, especially **TPS26600PWPR** (limited stock on 2026-11-09). No substitution without
   written approval.
3. CPL rotation convention and polarity check against the assembly drawing.
4. Finish (ENIG preferred), board thickness 1.6 mm, 1 oz copper.
5. Shipping to the destination country, duties, price and lead time. **None of these are claimed here.**
