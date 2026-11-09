"""V0.2.0 design calculations (Sensor Interface & Power Management Board).

Revision of the V0.1.0 power-entry stage (DDR-17): the AO3401A / MF-MSMF050 / SMAJ6.0A chain is
replaced by a TI TPS26600 eFuse (reverse polarity, OVP cut-off, current limit, inrush control).
Also: LDO thermal model for a 2-layer board, trace widths, I2C recheck, TRIG series resistor.

Input tags: VERIFIED (datasheet, page/table cited) | DESIGN (owner/design choice) | ASSUMED.
Run: python design_calcs_v020.py  (pure Python 3, no dependencies)
"""
import itertools
import math

def h(t):
    print("\n" + "=" * 88 + "\n" + t + "\n" + "=" * 88)

# ---------------------------------------------------------------- inputs
VIN_MIN, VIN_NOM, VIN_MAX = 4.75, 5.00, 5.25          # DESIGN: regulated 5 V +-5 % (OQ-05)
T_AMB_MAX = 50.0                                      # DESIGN (OQ-15)

# TPS2660x, TI SLVSDG2G (Dec 2019) = DS-17
EF_VIN_ABS, EF_VIN_REV_ABS = 62.0, -60.0              # VERIFIED p.6 7.1
EF_VIN_OP_MIN = 4.2                                   # VERIFIED p.7
EF_UVLOR = (1.175, 1.19, 1.225)                       # VERIFIED p.7 V(UVLOR) min/typ/max
EF_UVLOF = (1.08, 1.10, 1.125)                        # VERIFIED p.7
EF_OVPR = (1.17, 1.19, 1.225)                         # VERIFIED p.7
EF_OVPF = (1.085, 1.10, 1.125)                        # VERIFIED p.7
EF_PIN_LEAK = 100e-9                                  # VERIFIED p.7 UVLO/OVP leakage max
EF_RON_MAX = 0.250                                    # VERIFIED p.8 (-40..125 C)
EF_RON_TYP = 0.150                                    # VERIFIED p.8 (25 C)
EF_IQ_MAX = 390e-6                                    # VERIFIED p.7
EF_OVP_DLY = 6e-6                                     # VERIFIED p.9 OVP disable delay
EF_DVDT_I, EF_DVDT_GAIN = 4.7e-6, 24.6                # VERIFIED p.7/p.21
EF_RTHJA = 38.6                                       # VERIFIED p.6 (JEDEC; 2-layer is worse, see below)
EF_TJ_MAX = 125.0                                     # VERIFIED p.6 ROC
ILIM_TOL = 0.15                                       # ASSUMED: +-15 % (table gives +-15 % at 0.1 A, +-5 % at 1 A)

# Divider (E96, Panasonic ERJ-3EKF +-1 %, DS-09)
R_TOP, R_MID, R_BOT = 73.2e3, 5.90e3, 21.5e3          # DESIGN (R_MID 6.49k -> 5.90k: UVLO min must stay >= 4.2 V)
R_TOL = 0.01
R_ILIM = 20.0e3                                       # DESIGN -> 0.6 A nominal
C_DVDT = 47e-9                                        # DESIGN (Samsung CL10B473KB8NNNC, DS-19)
C_IN_EF = 1.0e-6                                      # DESIGN (Samsung CL10A105KB8NNNC 50 V, DS-18)

# Downstream (from V0.1.0, DS-06/07/08)
LDO_VIN_ROC, LDO_VIN_ABS = 5.5, 6.0                   # VERIFIED DS-06 p.4
LVC_VCC_ROC, LVC_ABS = 5.5, 6.5                       # VERIFIED DS-07/08
US_VCC_MAX = 5.5                                      # VENDOR DS-13 (no abs max published)
I_3V3 = 0.2524                                        # CALCULATED V0.1.0 (I2C 100 + GP 50 + UART 100 + LED2)
I_5V_DIRECT = 0.020 + 0.00246 + 4e-6                  # US 20 mA alloc + LED1 + LVC1T45 VCCB (V0.1.0)
LDO_IQ = 100e-6                                       # VERIFIED DS-06 p.5
LDO_VOUT_MIN = 3.3 * (1 - 0.015)                      # VERIFIED +-1.5 %
C_5V = [10e-6, 10e-6, 0.1e-6, 0.1e-6, 0.1e-6, 0.1e-6] # C1, C8, C2, C5, C7, C9 on +5V_P
C_3V3 = [10e-6, 0.1e-6]                               # C3, C4 behind the LDO (charged during the ramp)
C_TOL = 0.10

# ---------------------------------------------------------------- 1. load and input current
h("1. Load budget (Architecture B) and input current")
r_string = R_TOP + R_MID + R_BOT
i_div = VIN_MAX / (r_string * (1 - R_TOL))
i_in = I_3V3 + LDO_IQ + I_5V_DIRECT + EF_IQ_MAX + i_div
print(f"+3V3_P {I_3V3*1e3:.1f} mA + LDO Iq + +5V_P direct {I_5V_DIRECT*1e3:.2f} mA + eFuse Iq {EF_IQ_MAX*1e6:.0f} uA"
      f" + divider {i_div*1e6:.0f} uA")
print(f"Input current worst: {i_in*1e3:.1f} mA  (V0.1.0: 275.7 mA incl. 0.8 mA TVS leakage, now removed)")

# ---------------------------------------------------------------- 2. UVLO / OVP window (worst-case corners)
h("2. TPS26600 UVLO / OVP thresholds - worst-case corners (thresholds x resistor +-1 %)")
def corners():
    for kt, km, kb in itertools.product((1 - R_TOL, 1 + R_TOL), repeat=3):
        yield R_TOP * kt, R_MID * km, R_BOT * kb

def vin_ovp(vth, rt, rm, rb):  return vth * (rt + rm + rb) / rb
def vin_uv(vth, rt, rm, rb):   return vth * (rt + rm + rb) / (rm + rb)

ovp_r = [vin_ovp(v, *c) for v in (EF_OVPR[0], EF_OVPR[2]) for c in corners()]
ovp_f = [vin_ovp(v, *c) for v in (EF_OVPF[0], EF_OVPF[2]) for c in corners()]
uv_r = [vin_uv(v, *c) for v in (EF_UVLOR[0], EF_UVLOR[2]) for c in corners()]
uv_f = [vin_uv(v, *c) for v in (EF_UVLOF[0], EF_UVLOF[2]) for c in corners()]
ovp_nom = vin_ovp(EF_OVPR[1], R_TOP, R_MID, R_BOT)
uv_nom = vin_uv(EF_UVLOR[1], R_TOP, R_MID, R_BOT)
print(f"Divider {R_TOP/1e3:.1f}k / {R_MID/1e3:.2f}k / {R_BOT/1e3:.1f}k, string current {VIN_NOM/r_string*1e6:.0f} uA "
      f"(>= 20 x pin leakage {20*EF_PIN_LEAK*1e6:.0f} uA: PASS)")
print(f"OVP rising : nom {ovp_nom:.3f} V, range {min(ovp_r):.3f} .. {max(ovp_r):.3f} V")
print(f"OVP falling: range {min(ovp_f):.3f} .. {max(ovp_f):.3f} V (output re-enables below this)")
print(f"UVLO rising: nom {uv_nom:.3f} V, range {min(uv_r):.3f} .. {max(uv_r):.3f} V")
print(f"UVLO falling: range {min(uv_f):.3f} .. {max(uv_f):.3f} V (POR falling ~3.72 V also applies)")
chk = [
    ("OVP rising min > VIN_max (no nuisance trip)", min(ovp_r) - VIN_MAX),
    ("OVP rising max < TLV1117LV VIN abs max 6.0 V", LDO_VIN_ABS - max(ovp_r)),
    ("OVP rising max < LVC VCC abs max 6.5 V", LVC_ABS - max(ovp_r)),
    ("UVLO rising max < VIN_min (always starts in spec)", VIN_MIN - max(uv_r)),
    ("UVLO rising min > TPS2660 VIN op min 4.2 V", min(uv_r) - EF_VIN_OP_MIN),
]
for name, m in chk:
    print(f"  {name}: margin {m:+.3f} V -> {'PASS' if m > 0 else 'FAIL'}")
print(f"Note: between {LDO_VIN_ROC} V (LDO/LVC/sensor ROC max) and OVP max {max(ovp_r):.2f} V the board is outside the")
print("recommended range but below every absolute maximum; this only happens with an out-of-spec (> 5.25 V) supply.")

# ---------------------------------------------------------------- 3. RON drop, rails
h("3. Rails with the eFuse (RON max 250 mOhm over temperature)")
v5_min = VIN_MIN - i_in * EF_RON_MAX
v5_max = VIN_MAX
print(f"+5V_P: {v5_min:.3f} .. {v5_max:.3f} V (V0.1.0: 4.439 .. 5.250 V); eFuse P = {i_in**2*EF_RON_MAX*1e3:.1f} mW")
vdo_est = 0.090 * I_3V3 / 0.200 * 1.5   # VERIFIED 90 mV @ 200 mA typ, x1.5 ASSUMED worst
print(f"LDO headroom at +5V_P min: {v5_min - 3.3:.3f} V vs dropout estimate {vdo_est:.3f} V -> "
      f"{'PASS' if v5_min - 3.3 > vdo_est else 'FAIL'}")

# ---------------------------------------------------------------- 4. current limit, inrush, start-up
h("4. Current limit (RILIM) and inrush (dVdT)")
i_ol = 12.0 / (R_ILIM / 1e3)                          # VERIFIED Eq.9: ILIM = 12 / RILIM(kOhm)
i_ol_min, i_ol_max = i_ol * (1 - ILIM_TOL), i_ol * (1 + ILIM_TOL)
i_fast = 1.87 * i_ol_max + 0.015                      # VERIFIED p.8 fast-trip
print(f"RILIM {R_ILIM/1e3:.1f}k -> I_OL nom {i_ol:.3f} A, assumed range {i_ol_min:.3f} .. {i_ol_max:.3f} A; fast-trip <= {i_fast:.2f} A")
print(f"Steady load {i_in:.3f} A -> margin x{i_ol_min/i_in:.2f} to I_OL min ({'PASS' if i_ol_min > 1.5*i_in else 'CHECK'})")
c_out = sum(C_5V + C_3V3) * (1 + C_TOL)
t_ramp = 8e3 * VIN_MAX * C_DVDT                       # VERIFIED Eq.2
i_inrush = c_out * VIN_MAX / t_ramp
print(f"C_out (incl. LDO output, +10 %) {c_out*1e6:.1f} uF; C(dVdT) {C_DVDT*1e9:.0f} nF -> ramp {t_ramp*1e3:.2f} ms, inrush {i_inrush*1e3:.0f} mA")
print(f"Inrush + full load {i_inrush + i_in:.3f} A vs I_OL min {i_ol_min:.3f} A -> {'PASS' if i_inrush + i_in < i_ol_min else 'FAIL'}")
p_start = 0.5 * VIN_MAX * i_inrush + VIN_MAX**2 / 6 * (i_in / VIN_MAX)  # Eq.16 + Eq.17 (resistive-load approx)
print(f"Start-up average dissipation ~{p_start*1e3:.0f} mW for {t_ramp*1e3:.1f} ms (negligible)")
p_short = VIN_MAX * i_ol_max
print(f"Output short (current-limit mode, MODE=RTN): P = {p_short:.2f} W until thermal shutdown (157 C), auto-retry 512 ms")
print(f"  -> device self-protects; with ~{EF_RTHJA} C/W (JEDEC) or worse on 2 layers, TSD within seconds (by design).")

# ---------------------------------------------------------------- 5. transients
h("5. Input transients and OVP response")
L_cable = 1e-6                                        # ASSUMED: ~1 m two-wire supply lead
c_in_eff = C_IN_EF * 0.8                              # ASSUMED 20 % DC-bias loss at 5 V on a 50 V part
z0 = math.sqrt(L_cable / c_in_eff)
v_spike = VIN_MAX + i_fast * z0                       # TI Eq.25 form: V = VIN + I*sqrt(L/C)
print(f"Hot-short interruption spike: {VIN_MAX} + {i_fast:.2f} A x {z0:.2f} Ohm = {v_spike:.2f} V << 62 V abs max (PASS)")
v_ring = 2 * VIN_MAX
print(f"Hot-plug ringing (undamped worst, 2 x VIN) {v_ring:.1f} V at IN: < 62 V; FET is OFF during plug-in")
print("  (UVLO turn-on delay >= 250 us + dVdT ramp), so the ringing does not reach +5V_P.")
slew_ok = (LDO_VIN_ABS - max(ovp_r)) / EF_OVP_DLY
print(f"Overvoltage arriving while ON: output follows input for <= {EF_OVP_DLY*1e6:.0f} us -> abs max respected for")
print(f"  input slew <= {slew_ok/1e3:.1f} V/ms (bench supplies and adapters ramp in ms; a fast step while ON is NOT covered).")
print("Reverse polarity: TPS2660 blocks down to -60 V (VERIFIED p.19); C_IN rated 50 V -> board survives -50 .. +50 V at J1")
print("  (limited by C_IN rating; DESIGN statement, NOT TESTED).")
print("ESD at J1 (IEC 61000-4-2 8 kV contact, 150 pF): dV on C_IN = 1.2 uC / 1 uF = 1.2 V (ASSUMED model) -> no TVS needed.")

# ---------------------------------------------------------------- 6. LDO thermal, 2-layer board
h("6. TLV1117LV33 thermal on a 2-layer, 1 oz board")
p_ldo = (VIN_MAX - LDO_VOUT_MIN) * I_3V3 + VIN_MAX * LDO_IQ
print(f"P_LDO worst = ({VIN_MAX} - {LDO_VOUT_MIN:.3f}) x {I_3V3:.4f} + Iq = {p_ldo:.3f} W")
print("RthJA 62.9 C/W (DS-06) is a JEDEC 2s2p (4-layer) value -> NOT used for this 2-layer board.")
# TI LM1117 SNOS412Q Table 9-2: SOT-223 (DCY) on 1 oz copper, same TI package (DS-20)
table = [("min pad top 0.0123 in2", 136), ("top 0.066 in2", 123), ("top 0.3 in2", 84), ("top 0.53 in2", 75),
         ("top 1.0 in2", 66), ("top+bottom 0.284 in2 each", 83), ("top+bottom 0.5 in2 each", 70)]
UNCERT = 1.10                                         # ASSUMED +10 % (die/leadframe differs from LM1117)
for name, rth in table:
    tj = T_AMB_MAX + p_ldo * rth * UNCERT
    print(f"  {name:28s} RthJA {rth:3d} x1.10 -> Tj {tj:6.1f} C  {'PASS' if tj <= 110 else 'FAIL (target <= 110 C)'}")
print("Design requirement: >= 0.30 in2 (194 mm2) of 1 oz top copper on the tab (OUT, +3V3_P), plus a bottom +3V3_P")
print("  copper area joined by vias where layout allows. Target Tj <= 110 C (15 C below TJ max) at 50 C ambient.")

# ---------------------------------------------------------------- 7. trace widths
h("7. Trace widths (IPC-2221 external-layer formula, 1 oz = 35 um, dT = 10 C)")
def ipc2221_width_mm(i, dt=10.0, oz=1.0, k=0.048):
    area_mil2 = (i / (k * dt ** 0.44)) ** (1 / 0.725)
    return area_mil2 / (oz * 1.378) * 0.0254
for net, i, chosen in [("VIN_RAW / +5V_P main", i_ol_max, 0.80), ("+3V3_P main", I_3V3 * 1.5, 0.60),
                       ("+5V_P branch (sensor, LEDs, LVC)", 0.05, 0.40), ("signals", 0.025, 0.25)]:
    w = ipc2221_width_mm(i)
    r_per_mm = 1.72e-8 / (chosen * 1e-3 * 35e-6) * 1e-3
    print(f"  {net:34s} I {i*1e3:5.0f} mA -> min {w:.3f} mm; chosen {chosen:.2f} mm "
          f"(x{chosen/w:.1f}); {r_per_mm*1e3:.3f} mOhm/mm")
print("Voltage drop: 60 mm of 0.8 mm track at 0.28 A = "
      f"{0.28 * 60e-3 * 1.72e-8 / (0.8e-3 * 35e-6) * 1e3:.1f} mV (negligible)")

# ---------------------------------------------------------------- 8. I2C recheck
h("8. I2C pull-up recheck (UM10204 Rev 7.0, DS-I2C)")
RP, RP_TOL = 2.2e3, 0.01
for vdd in (3.0, 3.3, 3.6):
    rp_min = (vdd - 0.4) / 3e-3
    print(f"  VDD {vdd}: Rp(min) {rp_min:.0f} Ohm vs {RP*(1-RP_TOL):.0f} Ohm -> {'PASS' if RP*(1-RP_TOL) >= rp_min else 'FAIL'};"
          f" sink {vdd/(RP*(1-RP_TOL))*1e3:.2f} mA")
cb_fm = 300e-9 / (0.8473 * RP * (1 + RP_TOL))
cb_sm = min(1000e-9 / (0.8473 * RP * (1 + RP_TOL)), 400e-12)
print(f"Max bus capacitance: Fast-mode {cb_fm*1e12:.0f} pF, Standard-mode {cb_sm*1e12:.0f} pF")
c_board = 10e-12                                      # ASSUMED: J2+J5 traces + 2 headers
print(f"Board contribution ~{c_board*1e12:.0f} pF (ASSUMED) -> cable + devices may add {cb_fm*1e12 - c_board*1e12:.0f} pF in Fast-mode")

# ---------------------------------------------------------------- 9. ultrasonic levels with new +5V_P range
h("9. Ultrasonic levels with +5V_P = %.3f .. %.3f V and new 1 k TRIG series resistor (R15)" % (v5_min, v5_max))
R15, R_PD = 1e3, 100e3
voh_b = v5_min - 0.1                                  # VERIFIED DS-08 VOH = VCCO - 0.1 V @ -100 uA
trig_hi = voh_b * R_PD * (1 - R_TOL) / (R_PD * (1 - R_TOL) + R15 * (1 + R_TOL))
print(f"TRIG HIGH at J3 >= {trig_hi:.3f} V = {trig_hi/v5_min*100:.1f} % of sensor VCC (PASS: >= 90 %)")
echo_hi = v5_min * R_PD * (1 - R_TOL) / (R_PD * (1 - R_TOL) + 1e3 * (1 + R_TOL))
print(f"ECHO HIGH at U2 input >= {echo_hi:.3f} V vs VT+ max 2.25 V -> margin {echo_hi-2.25:.2f} V; max {v5_max} V <= 5.5 V (PASS)")
print(f"Mis-wired TRIG<->ECHO (output vs output): contention current <= {v5_max/R15*1e3:.1f} mA (limited by R15) -> no damage")
print("End of V0.2.0 calculations.")
