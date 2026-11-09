"""V0.3.0 final engineering audit calculations (release Rev A / V1.0.0).

Every input is labelled: VERIFIED (datasheet / board read-back), CALCULATED, or ASSUMED.
Run: python -I release_audit_calcs.py   (any Python 3.8+, no packages)
"""

def hdr(t):
    print("\n" + "=" * 88 + "\n" + t + "\n" + "=" * 88)


# ---- Inputs
VIN_MAX = 5.25          # supply spec 5 V +-5 % (requirements; ASSUMED supply compliance)
VOUT_MIN = 3.25         # TLV1117LV33 output low limit used in V0.2.0 calcs (CALCULATED worst case)
AREA_MM2 = 251.2        # +3V3_P solid top copper, pcbnew read-back of saved board (VERIFIED, board)
AREA_IN2 = AREA_MM2 / 645.16
# TI LM1117 SNOS412 Table 9-2 (SOT-223, 2-layer, top copper only) used as a proxy for the same SOT-223 package
# (ASSUMED proxy, +10 % margin applied as in V0.2.0)
TABLE = [(0.30, 84.0), (0.53, 75.0)]
(a0, r0), (a1, r1) = TABLE
RTH = (r0 + (AREA_IN2 - a0) * (r1 - r0) / (a1 - a0)) * 1.10
TJ_TARGET, TJ_REC_MAX = 110.0, 125.0   # design target / TLV1117LV operating TJ max (VERIFIED SBVS160C p.13-14: -40..+125 C, "limit junction temperature to 125 C")
I_OL_MIN, I_OL_MAX = 0.51, 0.69       # TPS26600 current limit with RILIM 20k (V0.2.0 CALCULATED range)
I_5V_DIRECT = 0.02246                  # +5V_P loads other than the LDO (V0.2.0 budget, CALCULATED)

hdr("1. LDO thermal model (independent re-derivation)")
print(f"+3V3_P copper {AREA_MM2} mm2 = {AREA_IN2:.3f} in2 -> RthJA (interp. x1.10) = {RTH:.1f} C/W")
for i in (0.2524,):
    p = (VIN_MAX - VOUT_MIN) * i
    print(f"Design load {i*1000:.1f} mA: P = {p:.3f} W -> Tj @50C = {50 + RTH * p:.1f} C (V0.2.0 reported 94.7 C)")

hdr("2. Continuous +3V3_P output rating vs ambient (VIN = 5.25 V worst case)")
print(" Ta[C]  Imax for Tj<=110C   Imax for Tj<=125C")
for ta in (25, 40, 50, 60):
    i110 = (TJ_TARGET - ta) / RTH / (VIN_MAX - VOUT_MIN)
    i125 = (TJ_REC_MAX - ta) / RTH / (VIN_MAX - VOUT_MIN)
    print(f" {ta:5d}  {i110*1000:8.0f} mA          {i125*1000:8.0f} mA")
print("Published rating (docs): +3V3_P <= 250 mA continuous at Ta <= 50 C (Tj ~95 C CALCULATED).")

hdr("3. Fault cases")
p_short_ldo = VIN_MAX * I_OL_MAX
print(f"+3V3_P shorted: eFuse limits input to <= {I_OL_MAX} A -> LDO P <= {p_short_ldo:.2f} W -> Tj reaches")
print("  TSD 165 C (SBVS160C p.5): TLV1117LV thermal shutdown cycles (current limit 1.1 A typ p.1; short duration 'Indefinite' p.4).")
print(f"+5V_P shorted: TPS26600 current limit {I_OL_MIN}-{I_OL_MAX} A, P = VIN x I <= {VIN_MAX*I_OL_MAX:.2f} W ->")
print("  thermal shutdown, auto-retry (MODE = RTN, TI SLVSDG2G Table 2). Board-level: self-protecting, NOT TESTED.")
budget = I_OL_MIN - I_5V_DIRECT
print(f"Total +5V_P budget before current limit (min): {I_OL_MIN*1000:.0f} mA; available for LDO + J3 sensor: {budget*1000:.0f} mA")

hdr("4. Reverse polarity: which paths are inside the eFuse protection")
print("Floating (isolated) source reversed: VIN_RAW = -V vs board GND; TPS26600 blocks to -60 V; no other path -> PROTECTED (design).")
print("Earth-referenced source (negative terminal earthed) reversed while the ESP32 USB host is earthed:")
print("  source +  -> J1-2 (board GND) -> J2-2/11/12 -> DevKit GND -> USB GND -> host earth -> source -  (loop)")
print("  The eFuse is NOT in this loop. Current is limited only by the source current limit and the cable/USB path.")
print("  -> NOT PROTECTED. Mitigation: isolated supply, polarity check before USB connection (power-up order R-31).")
