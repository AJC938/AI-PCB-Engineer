# Final Engineering Audit — V0.3.0 (release Rev A / v1.0.0)

Date 2026-11-09 · branch `release/v0.3.0-finalization` · base: V0.2.0 commit `d859317` (verified: present,
clean, author date 2026-11-09). Every result below was re-derived from the **saved design files** and the
**datasheets**, not copied from V0.2.0 reports. Labels: `VERIFIED (datasheet/board read-back)` · `CALCULATED` ·
`TOOL-CHECKED (ERC/DRC)` · `ASSUMED` · `NOT TESTED`.

**Result: no electrical or layout correction is required.** One non-electrical change was made: the board
revision label (DDR-22, §8). Six limitations are classified and documented (§9). None blocks a digital release.

## 1. Sources
| ID | Document | Revision read |
|---|---|---|
| DS-17 | TI TPS2660x datasheet SLVSDG2G | Rev. G, Dec 2019 (PDF metadata 2026-09-04) |
| DS-06 | TI TLV1117LV datasheet SBVS160C | Rev. C, Jan 2023 |
| DS-07/08 | TI SN74LVC1G17 / SN74LVC1T45 | as indexed in `datasheets/v0.1.0/DATASHEET_INDEX.md` |
| — | Board read-back | `pcbnew.LoadBoard()` on the saved `.kicad_pcb` (read-only) |
| — | Calculations | `calculations/v0.3.0/release_audit_calcs.py` (+ output), V0.2.0 calcs and Monte Carlo |

## 2. TPS26600 eFuse input protection (U5)
### 2.1 Schematic vs datasheet
| Pin (PWP) | Datasheet function (DS-17 p.4–5) | Design net | Verdict |
|---|---|---|---|
| 1, 2 IN | power input | VIN_RAW (J1-1, C12 1 µF 50 V, R16) | PASS |
| 3 UVLO | divider IN→UVLO→RTN; "must not be left floating" | EF_UVLO (R16/R17 node) | PASS |
| 5 OVP | divider IN→OVP→RTN | EF_OVP (R17/R18 node) | PASS |
| 6 MODE | RTN = current limit with auto-retry (Table 2) | EF_RTN | PASS: current-limit, auto-retry |
| 7 SHDN | low = shutdown | not connected (internally pulled up, device enabled) | PASS (TI minimal configuration) |
| 8 RTN | "reference for internal control circuits" | EF_RTN island | PASS |
| 9 GND | "connect GND to system ground" | GND | PASS |
| 10 IMON / 14 FLT | "if unused, leave floating" | not connected | PASS |
| 11 ILIM | resistor to RTN, 5.36–120 kΩ recommended | R19 20 kΩ → RTN | PASS |
| 12 dVdT | capacitor to RTN, ≥ 10 nF recommended | C13 47 nF → RTN | PASS |
| 15, 16 OUT | power output | +5V_P | PASS |
| 4, 13 N.C. | no connect | not connected | PASS |
| PowerPAD (17) | "must be connected to RTN plane"; RTN ≠ GND when reverse protection is needed (§12.1) | EF_RTN | PASS |

Board read-back: U5 pad 17 (3.4 × 5.0 mm) and pads 6/8 are on `EF_RTN`; pad 9 is on `GND`; the EF_RTN zone is a
38.0 mm² top-copper island. No via connects EF_RTN to any other layer. `VERIFIED (board read-back)`.

### 2.2 Thresholds and behaviour
| Item | Value | Label |
|---|---|---|
| Operating input range (device) | 4.2–60 V; abs max −60…62 V (DS-17 p.6) | VERIFIED |
| OVP trip, rising | 5.389–5.823 V worst case (Monte Carlo 5.395–5.817 V) | CALCULATED |
| UVLO, rising | 4.252–4.564 V | CALCULATED |
| Current limit | 0.51–0.69 A (RILIM 20 kΩ, I_OL = 12/RILIM) | CALCULATED |
| Inrush | 1.97 ms ramp, ≈ 89 mA into 33.6 µF | CALCULATED |
| Overload | current limited at I_OL; thermal shutdown; auto-retry ~540 ms after cooling (MODE = RTN, Table 2) | VERIFIED (datasheet) |
| Output short | fast trip at 1.8 × I_OL, then current-limited restart | VERIFIED (datasheet) |
| Normal dissipation | 19 mW at 0.28 A (RON 250 mΩ max) | CALCULATED |
| Start-up sequence | UVLO released → dVdT-controlled ramp → +5V_P → LDO → +3V3_P | VERIFIED (datasheet) / NOT TESTED |
| Input capacitor | C12 1 µF 50 V ≥ the 1 µF that TI recommends to keep input falling slew ≤ 20 V/µs (§11.1) | PASS |

### 2.3 Reverse-polarity topology and every conductive path
The TPS2660 blocks reverse input with integrated back-to-back FETs and a protected GND/RTN reference (DS-17
§9.3.3, block diagram p.18). **The eFuse protects only the path that goes through it.** All nodes that can carry
current between the external source and other equipment were traced from the netlist:

| Path from J1 | Through | Inside the eFuse protection? |
|---|---|---|
| J1-1 VIN_RAW → U5 IN → OUT → +5V_P → U1, J3-1, LEDs, U3 VCCB | U5 FETs | **Yes**: blocked to −60 V |
| J1-1 VIN_RAW → C12, TP1, R16-R17-R18 → EF_RTN | divider/RTN island (internal GND↔RTN blocking) | Yes: RTN abs max −60 V wrt GND |
| J1-2 GND → board GND plane → J2-2/11/12 → ESP32 DevKit GND → USB cable → USB host | **no series element** | **No** |
| J1-2 GND → J3-4, J4-1, J5-1, J6-1 → external peripherals and their own supplies | **no series element** | **No** |
| Signals (TRIG/ECHO/I²C/UART/GPIO) | series resistors 220 Ω–1 kΩ and buffers | not power paths; referenced to GND |

| Scenario | Result |
|---|---|
| Floating source (battery, isolated adapter) connected reversed | VIN_RAW = −V wrt GND; U5 blocks; the only other path (GND) does not close a loop. **Protected** (design statement, NOT TESTED) |
| Reversed source, ESP32 USB host floating (laptop on battery) | Same as above: **protected** |
| Reversed source whose **negative terminal is earthed** (e.g. bench supply with − linked to earth), while the ESP32 USB host is earthed (desktop PC) | Source + reaches board GND through J1-2. Board GND = USB GND = host earth = source −. **The source is short-circuited through board GND, J2, the DevKit and the USB cable. The eFuse is not in this loop.** Current is limited only by the source's current limit. **NOT protected** |
| Reversed source while an externally powered, earthed peripheral is on J3–J6 | Same loop through the peripheral's ground. **NOT protected** |
| Correct polarity, any source | No bypass path. The eFuse is in series with every load as intended |

**Classification:** inherent to any design whose ground is common with another earthed system (Architecture B
requires the common ground for the signal interface). It cannot be removed on this board without isolating the
ESP32 interface, which is a functional change. **Mitigations (documented, no hardware change):**
1. Use an isolated (floating) 5 V source, or check the polarity at J1 before connecting any other equipment.
2. Power-up order (rule R-31): connect and switch on J1 first, confirm LED1 (red, +5V_P) is on — it lights only
   when the eFuse has turned on with correct polarity — then connect the ESP32 USB cable.
3. Bench work: set the supply current limit low (≤ 0.3 A) for the first power-up.

### 2.4 Transients and surge
- Overvoltage that rises faster than ≈ 24–30 V/ms while the board is powered can reach the loads during the
  ≤ 6 µs OVP response (CALCULATED in V0.2.0). Normal adapters and bench supplies ramp far slower. **Not covered.**
- **No surge (IEC 61000-4-5) protection is claimed.** There is no input TVS and no output Schottky (both optional
  in TI §11.1). A hard output short can produce a negative spike at OUT through output inductance. With 10 µF + 100 nF
  directly at the eFuse output and short on-board traces this is ASSUMED low risk, and NOT TESTED.
- ESD at J1 is absorbed by C12 (≈ 1.2 V step for an 8 kV / 150 pF model, ASSUMED model). No ESD rating is claimed.

### 2.5 Thermal (U5)
TI recommends vias from the PowerPAD to an RTN plane "for enhanced thermal performance" and "to operate at rated
power" (2 A class). This board uses a 38 mm² top-only RTN island and no RTN vias. Normal dissipation is 19 mW, so
the deviation has no effect in normal operation. In overload, a smaller copper area makes thermal shutdown happen
sooner, which is the intended self-protection. **Accepted deviation** (documented, NOT TESTED).

## 3. LDO thermal review (U1 TLV1117LV33DCYR, SOT-223)
| Item | Value | Label |
|---|---|---|
| Package / pinout | DCY SOT-223: 1 GND, 2 OUT + tab, 3 IN | VERIFIED (DS-06) |
| Footprint | `SOT-223-3_TabPin2`: tab pad 2.0 × 3.8 mm on +3V3_P | VERIFIED (board) |
| Thermal copper | **251.2 mm² solid +3V3_P top copper** (zone outline 252.0 mm², pad connection = solid) | VERIFIED (board) |
| Bottom copper / thermal vias | none on +3V3_P (bottom is the GND plane) | VERIFIED (board) |
| RθJA model | TI LM1117 SOT-223 2-layer data (same package) interpolated at 0.389 in² × 1.10 = **88.6 °C/W** | ASSUMED proxy + CALCULATED |
| Power | (5.25 − 3.25 V) × 252.4 mA = 0.505 W | CALCULATED |
| Tj at 50 °C ambient | **94.7 °C** (target ≤ 110 °C; TI: limit Tj to 125 °C, TSD 165 °C) | CALCULATED, NOT measured |
| TLV1117LV JEDEC RθJA 62.9 °C/W | 4-layer high-K value, **not used** for this 2-layer board | VERIFIED (DS-06 p.4) |

**Output rating (new, documented in the README and connection guide):** +3V3_P ≤ **250 mA continuous at
Ta ≤ 50 °C**. CALCULATED limits for Tj ≤ 110 °C: 480 mA at 25 °C, 395 mA at 40 °C, 339 mA at 50 °C, 282 mA at 60 °C.
A +3V3_P short drives U1 into its own current limit and thermal shutdown (TLV1117LV: "output short-circuit
duration: indefinite"). The 0.51–0.69 A eFuse limit applies first on the 5 V side.

## 4. Signal review
| Interface | Implementation | Check | Verdict |
|---|---|---|---|
| TRIG | ESP32 GPIO26 → U3 SN74LVC1T45 A (VCCA = 3V3_ESP) → B (VCCB = +5V_P) → R15 1 kΩ → J3-2; DIR tied to VCCA (A→B) | TRIG high ≥ 4.535 V (96.9 % of sensor VCC); R4/R5 100 kΩ pull-downs keep TRIG low at reset or when unpowered | PASS |
| ECHO | J3-3 → R6 1 kΩ → U2 SN74LVC1G17 (VCC = 3V3_ESP, input tolerant to 5.5 V) → GPIO34 | ECHO high 4.63 V vs VT+ max 2.25 V; input ≤ 5.25 V ≤ 5.5 V; R7 100 kΩ pull-down | PASS |
| I²C | GPIO21/22, 2.2 kΩ pull-ups to 3V3_ESP through JP2 | Rp(min) 1067 Ω < 2.2 kΩ; 3 mA sink; 159 pF budget in Fast-mode | PASS |
| UART TX | GPIO17 → R10 220 Ω → J4-3 | 3.3 V CMOS. The device RX must accept 3.3 V logic (also when JP1 selects 5 V) | PASS (documented) |
| UART RX | J4-4 → R11 1 kΩ → U4 SN74LVC1G17 → GPIO16; R12 100 kΩ pull-up to 3V3_ESP | accepts 3.3 V or 5 V device TX | PASS |
| GPIO | GPIO32/33 ↔ R13/R14 1 kΩ ↔ J6-3/4 | **3.3 V only, not 5 V tolerant** (documented) | PASS (documented) |
| Power domains | +3V3_P (board LDO) and 3V3_ESP (DevKit) share no node; the DevKit 5V pin is not used | netlist verifier [2] | PASS (TOOL-CHECKED) |
| Sequencing | U2/U3/U4 are powered from 3V3_ESP. With the ESP32 off, their inputs are Ioff-protected. With the board off and the ESP32 on, back-feed ≤ 2.5 mA (I²C) and ≤ 12 mA (UART TX into an unpowered device) | rule R-31 (board first or together) | Documented |
| Test points | TP1 VIN_RAW, TP2 +5V_P, TP3 +3V3_P, TP4 3V3_ESP, TP5/TP6 GND, TP7 ECHO_ESP, TP8 TRIG_5V | net names match silk labels | PASS |

## 5. Connector interface review
Every connector, pin, net, voltage and direction was re-read from the netlist and is published in
[`docs/pinout/CONNECTION_GUIDE.md`](../../docs/pinout/CONNECTION_GUIDE.md) and the package file `CONNECTOR_PINOUT.md`.
J3 keeps its explicit labels (1 +5V, 2 TRIG, 3 ECHO, 4 GND). The physical pin order of HC-SR04-style modules is
**not universal and not verified**, so the guide tells users to wire J3 with four individual jumpers by label. No
universal module pin order is claimed. Mating connectors are not specified and not verified (§6).

## 6. Footprint and mechanical audit
Re-read from the saved board: 61 footprints, all on top. 3D models resolve through `${KICAD10_3DMODEL_DIR}`
(KiCad 10 standard library).

| Ref(s) | Footprint | Evidence | Verdict |
|---|---|---|---|
| U5 | project `TI_PWP0016A_HTSSOP-16-1EP…` (in `Sensor_Interface_Power_Board.pretty`, `${KIPRJMOD}` lib table) | 16 × 1.5 × 0.45 mm, 0.65 mm pitch, EP 3.4 × 5.0, mask/paste 3.3 × 3.3 = TI PWP0016A | PASS. The 3D model is KiCad's HTSSOP-16 body (same 4.4 × 5 mm body, different EP mask variant): visual only |
| U1 | SOT-223-3_TabPin2 | IPC-7351 pattern; TI note allows alternatives | PASS |
| U2/U4, U3 | SOT-23-5 / SOT-23-6 | IPC-7351 | PASS |
| R/C | 0603 IPC-7351 nominal | body 1.6 × 0.8 verified; the Panasonic land-pattern document was not compared | PASS (low-risk note) |
| J1 Phoenix 1715721 | MKDS-1,5-2-5.08 horizontal, Ø1.3 mm drill, Ø2.6 mm pad, 5.08 mm pitch | Phoenix data (V0.2.0); wire entry faces the left edge, body inside the outline (3D render) | PASS. Overhang/edge distance from the 3D view only, not measured |
| J2–J6 Samtec HTSW | 2.54 mm, Ø1.0 mm drill, Ø1.7 mm pad | Samtec recommends 1.02 ± 0.03 mm; the 1.0 mm finished hole fits a 0.64 mm square post (diagonal 0.9 mm) | PASS (note: tight against the post diagonal with −0.08 mm hole tolerance; still ≥ 0.82 mm) |
| LED1/LED2 | LED_D5.0mm, Ø0.9 mm drill | Kingbright 0.5 mm square leads (diagonal 0.71 mm) | PASS. LED2's 3D model is the generic red body (colour only) |
| TP1–TP8 | Keystone 5015 | 3.4 × 1.8 mm pad = datasheet | PASS |
| H1–H4 | NPTH Ø3.2 mm, 3.5 mm from each edge | M3 clearance | PASS |
| FID1–FID3 | 1.0 mm copper, 2.0 mm mask | — | PASS |
| Courtyards / edge clearance / silkscreen | kicad-cli DRC, all severities | 0 violations | TOOL-CHECKED |

**Independent reopening:** no file in the KiCad project contains an absolute path (`grep` = 0). The project
footprint library uses `${KIPRJMOD}`. Symbols are embedded in the schematic. Requirement: **KiCad 10.0.x** with
its standard footprint and 3D libraries. A KiCad 9 install cannot open the files.

**Not verified (no dimensional evidence):** mating housings for J2–J6; physical fit of the ultrasonic module and
ESP32 DevKit (connected by wires, so no board-to-board mechanical interface exists); enclosure.

## 7. Validation (this audit's re-run, `scripts/release/build_release.sh`)
| Check | Result |
|---|---|
| ERC (kicad-cli, all severities) | **0** |
| Netlist verifier (31 nets, domain rules, 61 footprints, 52 MPNs) | **PASS** |
| DRC, zones refilled (D-10), all severities, schematic parity | **0 violations, 0 unconnected, 0 parity** |
| DRC, stored zones | **0 / 0 / 0** (refill makes no difference) |
| Release package audit | see `MANUFACTURING_PACKAGE_AUDIT.md` |

## 8. Engineering change DDR-22 (non-electrical)
| Field | Content |
|---|---|
| Change | Title block `rev` 0.2.0 → **A** (schematic and PCB); comment 3 "Release v1.0.0 (Rev A) - fabrication-ready design, NOT physically tested"; top silkscreen "SENSOR IF + PWR BOARD  REV 0.2.0" → "SENSOR IF + PWR BOARD REV A v1.0" |
| Reason | The released hardware revision must be identifiable on the physical board and in the job file (Gerber job `Revision: A`) |
| Impact | Silkscreen and title block only. Compared with `manufacturing/v0.2.0/` after removing header and date lines: F.Cu, B.Cu, both masks, both pastes, Edge.Cuts, PTH, NPTH, IPC-D-356, BOM and CPL are **identical**. B.Silkscreen is identical. F.Silkscreen differs only at Y 36.1–37.1 mm, which is the revision label |
| Method | `scripts/release/set_release_revision.py`: exact-match edits with expected counts; refuses to run if a KiCad lock exists for the edited file |
| Preservation | V0.2.0 design = git `d859317`; `manufacturing/v0.2.0/` untouched |
| Verification | ERC 0, DRC 0/0/0 with parity, after the change |

## 9. Classified limitations (documented, not blocking a digital release)
| # | Limitation | Class | Where documented |
|---|---|---|---|
| L-1 | Reverse polarity is **not** protected when the source is earth-referenced and the ESP32 USB host (or a peripheral) is earthed | Inherent (common ground) | README, safety guide, connection guide |
| L-2 | No surge / fast-overvoltage protection (dV/dt > ~24 V/ms while powered) | Design scope | README, safety guide |
| L-3 | +3V3_P rating 250 mA at ≤ 50 °C (thermal, CALCULATED, not measured) | Rating | README, connection guide |
| L-4 | Power-sequencing rule R-31 (board first or together with the ESP32) | Architecture B | silkscreen, README, guides |
| L-5 | Ultrasonic module pin order and mating connectors not verified | Mechanical | connection guide |
| L-6 | TPS26600PWPR availability limited (2026-11-09) | Sourcing | BOM_SOURCING_AUDIT.md |
| L-7 | Everything is NOT physically fabricated or tested | Status | everywhere |
