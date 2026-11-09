# Datasheets

Datasheet PDFs are **not redistributed** (copyright of their publishers). The indexes list each official URL,
the document revision read, and the exact facts (with page numbers) used in the design.

| Index | Content |
|---|---|
| [v0.1.0/DATASHEET_INDEX.md](v0.1.0/DATASHEET_INDEX.md) | DS-01…DS-16: ESP32/DevKitC, LDO, logic, passives, connectors, LEDs, test points (some parts later removed) |
| [v0.2.0/DATASHEET_INDEX.md](v0.2.0/DATASHEET_INDEX.md) | DS-17…DS-20: TPS26600 eFuse, eFuse capacitors, LM1117 thermal data, land-pattern addenda |
| [index_v0.1.0.md](index_v0.1.0.md), [index.md](index.md) | Phase 1 and V0.0.2 indexes (history) |

## Parts in Rev A → datasheet
| Ref | MPN | Index ID |
|---|---|---|
| U5 | TPS26600PWPR | DS-17 (TI SLVSDG2G Rev. G) |
| U1 | TLV1117LV33DCYR | DS-06 (TI SBVS160C) + DS-20 thermal proxy |
| U2, U4 / U3 | SN74LVC1G17DBVR / SN74LVC1T45DBVR | DS-07 / DS-08 |
| C12, C13 | CL10A105KB8NNNC, CL10B473KB8NNNC | DS-18, DS-19 |
| Other passives, J1–J6, LEDs, TPs | see the v0.1.0 index | DS-09…DS-16 |

## V0.3.0 re-checks (2026-11-09, same documents)
| Doc | Facts re-read for the final audit |
|---|---|
| DS-17 TPS2660 SLVSDG2G Rev. G | p.4–5 pin functions incl. "PowerPad must be connected to RTN plane"; p.6 abs max (RTN −60…0.3 V wrt GND); p.18 block diagram (reverse-polarity circuit on GND, fast trip 1.8 × I_OL); p.19 reverse input protection to −60 V; p.27 Table 2 MODE→RTN = current limit with auto-retry, restart 540 ms after cooling; p.38 transient protection (C_IN ≥ 1 µF, optional TVS/Schottky); p.39 layout: RTN must be a plane or island, RTN/GND/PowerPAD joined only when reverse protection is not needed |
| DS-06 TLV1117LV SBVS160C | p.4 abs max VIN 6 V, output short "Indefinite", RθJA 62.9 °C/W (JEDEC); p.5 TSD 165 °C; p.13–14 operating TJ −40…+125 °C, "limit junction temperature to 125 °C"; p.1 current limit 1.1 A |
