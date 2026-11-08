# Component Selection Plan — V0.1.0

**No MPN is selected in Phase 1.** Every category below lists candidate *technologies* (not parts), the
datasheet items that must be verified, and the selection criteria. A component becomes **APPROVED** only
with:
1. a manufacturer datasheet (revision and date) indexed in `datasheets/`,
2. every "must verify" item cited by page or table,
3. a written engineering justification linked to requirement IDs,
4. a footprint verified against the package drawing (ENGINEERING_RULES §3).

Library availability is **not** a selection criterion.

## Common checklist (all parts)
Absolute maximum ratings · recommended operating conditions · electrical characteristics at our
conditions · package drawing and recommended land pattern · pinout for the exact package · thermal data
(RthJA/RthJC, derating) · operating temperature range · lifecycle status (active/NRND/EOL) · RoHS.

## Categories
| Category | Candidate technologies | Must verify in datasheet | Selection criteria | Depends on |
|---|---|---|---|---|
| Input connector | Pluggable/screw terminal block, barrel jack, USB-C power-only receptacle | Rated current and voltage, contact resistance, wire range, mating cycles, footprint, keying | ≥ input rating basis (POWER_BUDGET), keyed, hand-mateable | OQ-04, OQ-06 |
| Reverse-polarity protection | Series Schottky, P-channel MOSFET (gate-clamped), ideal-diode controller | VDS/VR max, Rds(on) or Vf at load current and temperature, VGS max and threshold at 4.75 V input, reverse leakage, power dissipation | Drop small enough to keep `+5V_P` above every 5 V load's minimum (TBD). Survives reversed input | OQ-05, OQ-11 |
| Overcurrent protection | PTC resettable fuse, eFuse/load switch, fast fuse | Hold/trip current vs ambient (derating), max voltage, trip time, R at hold. For an eFuse: current-limit accuracy, UVLO, fault behaviour | Holds the budget current at the maximum ambient. Trips below the connector or copper ratings | OQ-04, OQ-15 |
| Transient/ESD protection | TVS diode on VIN, ESD arrays on external signal lines | Working standoff voltage ≥ max VIN, clamping voltage vs downstream abs max, capacitance (signal lines), IEC 61000-4-2 level | Standoff above the input tolerance. Clamp below the most sensitive downstream rating | OQ-05 |
| 3.3 V regulation | LDO (fixed 3.3 V) or synchronous buck | Dropout at load, max input, output tolerance, PSRR, quiescent current, stability vs output capacitor (ESR), RthJA, current limit, thermal shutdown | Dissipation within rating at the maximum ambient (POWER_BUDGET). Output tolerance compatible with ESP32 VDD+0.3 rules where applicable | OQ-07, OQ-08, OQ-15 |
| Echo level conditioning | Resistor divider, single-gate buffer with 5 V-tolerant input and power-off protection | (buffer) input voltage tolerance at VCC = 0 and 3.3 V, VIH/VIL at 3.3 V, Ioff, propagation delay. (resistors) tolerance, TCR, power | Guarantees US-04 over all tolerances. Satisfies US-06 | OQ-11, OQ-14 |
| Trigger translation (if needed) | Single-gate buffer with TTL-compatible input powered at 5 V | VIH at VCC = 5 V ≤ 2.0 V (to accept 2.64 V with margin), VOH, supply range | Needed only if the sensor's VIH > about 2.3 V | OQ-11 |
| I2C pull-ups | Resistors with solder jumpers | Tolerance, power | Within Rp(min…max) for the chosen mode and Cb (INTERFACE_SPEC §4) | OQ-07, OQ-12 |
| UART protection | Series resistors | Tolerance, power | Limits fault current within ESP32 IO limits without breaking timing | OQ-08 |
| Signal and power connectors | 2.54 mm keyed headers, JST-style wire-to-board, terminal blocks | Current per contact, pitch, keying, mating parts, footprint | Keyed where feasible. Common sensor-cable compatibility | OQ-07, OQ-10 |
| ESP32 interface | Female socket headers (for a plug-in DevKit) or cable connector | Pitch, row spacing, height (antenna clearance), contact current | Matches the exact DevKit drawing | OQ-01, OQ-03, OQ-10 |
| Bulk and decoupling capacitors | MLCC (X7R/X5R), possibly electrolytic or polymer bulk | Capacitance vs DC bias, voltage rating, ESR (regulator stability), temperature | Meets regulator stability requirements. Bias derating applied | Regulator choice |
| Resistors | Thick-film chip or THT | Tolerance (1 % for dividers), power, TCR | Tolerances used in the calculations | — |
| LEDs | Indicator LEDs with series resistors | VF at test current, IF max, intensity, viewing angle, polarity marking | Visible at 1–2 mA. Current calculated per rail | — |
| Test points | THT loops or SMD test pads | Probe compatibility, current | Reachable with fitted cables (USE-02) | — |

## Process
1. Resolve the blocking open questions (OQ-01, OQ-04, OQ-05, OQ-06, OQ-11).
2. For each category: shortlist 2–3 parts, obtain official datasheets, fill a comparison table
   (in `docs/design-reviews/`), then choose one and document the justification.
3. Index the datasheets (`datasheets/`) and create or verify the symbols and footprints. Custom parts follow the
   V0.0.3 rules (`ai/AI_AGENT_INSTRUCTIONS.md` 12–13).
4. Mark each part APPROVED only after review. Never purchase without the owner's explicit approval.
