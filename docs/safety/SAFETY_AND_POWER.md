# Safety and Power Requirements — Rev A

**This is a low-voltage (5 V DC) board. It has not been fabricated or tested; all protection behaviour below is
a design statement from datasheets and calculations, not a measured result.**

## 1. Supply requirements
| Requirement | Value |
|---|---|
| Voltage | 5.0 V DC ±5 % (4.75–5.25 V) |
| Current capability | ≥ 0.7 A recommended (above the eFuse limit, as TI recommends), so that the limit, not the supply, acts first |
| Type | **Isolated (floating) supply recommended**, e.g. a class II wall adapter with screw-terminal lead or an isolated bench supply |
| Connection | J1 screw terminal: pin 1 = +5 V (triangle marker), pin 2 = GND |
| Not allowed | Mains voltage of any kind; supplies above 5.25 V in normal use; any supply above 50 V (input capacitor rating), even reversed |

## 2. What the board protects against (design, NOT TESTED)
| Event | Behaviour | Source |
|---|---|---|
| Input above 5.39–5.82 V (slow rise) | eFuse turns off; restarts automatically below 5.0–5.35 V | TPS26600 OVP, CALCULATED thresholds |
| Input below 4.25–4.56 V (rising) | board stays off (UVLO) | CALCULATED |
| Reversed input, **isolated** supply, no other earthed equipment | blocked (no current flows) | TPS26600 reverse protection to −60 V; C12 limits J1 to ±50 V |
| Overload or short on +5 V | current limited to 0.51–0.69 A, thermal shutdown, auto-retry | TPS26600 MODE = RTN |
| Short on +3.3 V | LDO current limit and thermal shutdown | TLV1117LV |
| Plug-in inrush | soft start ≈ 2 ms, ≈ 89 mA inrush | dVdT capacitor |

## 3. What the board does NOT protect against
1. **Reversed supply with earthed equipment on the common ground.** If the supply's negative terminal is earthed
   and the ESP32 USB host (desktop PC, earthed USB charger) or an earthed peripheral is connected, a reversed J1
   creates a short-circuit loop through the board GND, J2, the DevKit and the USB cable. **The eFuse is not in
   that loop.** Only the supply's own current limit restricts the current, and damage to the cable, the DevKit or
   the PC USB port is possible.
2. **Surge or fast transients** (IEC 61000-4-5, inductive kick-back, hot-plugging long cables into a live
   supply). There is no TVS. Overvoltage that rises faster than about 24 V/ms while the board is powered can
   reach the loads before the 6 µs OVP response completes.
3. **ESD** on the headers: no dedicated ESD protection. Handle the board with ESD precautions.
4. **5 V on 3.3 V pins:** J6-3/J6-4 and all J2 signals are 3.3 V only.
5. **Overheating the LDO** above the +3V3_P rating (250 mA at ≤ 50 °C ambient).

## 4. Mandatory power-up order (rule R-31)
1. Check J1 polarity with a meter.
2. Power the board (J1) first, current limit ≤ 0.3 A for the first power-up. LED1 red must light (it lights only
   when the eFuse turned on with correct polarity).
3. Then connect the ESP32 USB cable.
4. Power-down: disconnect the ESP32 USB first, or both together.

## 5. Bench and test safety
- Use a current-limited bench supply for all first tests. Never test reverse polarity with the ESP32 or any
  earthed instrument connected to the board GND (see the controlled procedure in
  [PHYSICAL_VALIDATION_STATUS.md](../validation/PHYSICAL_VALIDATION_STATUS.md)).
- U1 (LDO) can reach about 95 °C (CALCULATED) at the full 250 mA rating and 50 °C ambient. Do not touch it during operation.
- Do not power the board while it lies on a conductive surface.
