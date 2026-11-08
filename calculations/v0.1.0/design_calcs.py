"""V0.1.0 design calculations: Sensor Interface & Power Management Board (Architecture B).

Run: python calculations/v0.1.0/design_calcs.py
Evidence tags on every input:
  VERIFIED  = manufacturer document (see datasheets/v0.1.0/DATASHEET_INDEX.md, IDs DS-xx)
  VENDOR    = product vendor documentation (module level, not a component datasheet)
  SECONDARY = third-party only
  DESIGN    = a design rating chosen for this board (a specification, not a measured fact)
  ASSUMED   = engineering assumption to be confirmed by measurement
Units: V, A, ohm, W, degC unless stated. Outputs are CALCULATED.
"""
import math

# ------------------------------------------------------------------ inputs
VIN_NOM, VIN_TOL = 5.0, 0.05               # DESIGN: 5 V +/-5 % input specification (adapter/bench supply)
VIN_MIN, VIN_MAX = VIN_NOM * (1 - VIN_TOL), VIN_NOM * (1 + VIN_TOL)
T_AMB_MAX = 50.0                            # DESIGN: max ambient for the board (indoor bench/enclosure)

# Polyfuse Bourns MF-MSMF050 (DS-04)
PTC_IHOLD = {23: 0.50, 40: 0.44, 50: 0.40, 60: 0.37, 70: 0.33, 85: 0.29}   # VERIFIED derating table
PTC_ITRIP_23C, PTC_RMIN, PTC_R1MAX, PTC_VMAX = 1.00, 0.15, 1.0, 15.0       # VERIFIED
# P-MOSFET AOS AO3401A (DS-03)
Q_RDS_4V5_MAX, Q_RDS_2V5_MAX, Q_VGS_MAX, Q_VDS_MAX = 0.060, 0.085, 12.0, 30.0   # VERIFIED (25 degC)
Q_VGSTH_MAX = 1.3                            # VERIFIED |VGS(th)| max
Q_RTHJA_MAX = 125.0                          # VERIFIED steady-state max (1 in2 2 oz Cu)
# TVS Vishay SMAJ6.0A (DS-05)
TVS_VWM, TVS_VBR_MIN, TVS_VC, TVS_IPP, TVS_ID_MAX = 6.0, 6.67, 10.3, 38.8, 800e-6   # VERIFIED
# LDO TI TLV1117LV33 (DS-06)
LDO_VIN_MAX_ROC, LDO_VIN_ABS, LDO_ACC, LDO_IQ_MAX = 5.5, 6.0, 0.015, 100e-6         # VERIFIED
LDO_LOADREG_MAX = 0.035                     # VERIFIED 0..1 A
LDO_VDO_1A_MAX = 0.700                      # VERIFIED (VOUT >= 3.3 V, 1 A)
LDO_RTHJA, LDO_TJ_MAX = 62.9, 125.0         # VERIFIED (JEDEC board) / recommended Tj max
LDO_COUT_EFF_MIN = 0.5e-6                   # VERIFIED effective output capacitance for stability
# Logic: TI SN74LVC1G17 (DS-07), SN74LVC1T45 (DS-08)
G17_VI_MAX_ROC, G17_VI_ABS = 5.5, 6.5       # VERIFIED (independent of VCC)
G17_VTP_MAX_3V0, G17_VTP_MAX_4V5 = 1.92, 2.74   # VERIFIED VT+ max
G17_VTN_MIN_3V0 = 0.89                      # VERIFIED VT- min
G17_IOFF, G17_ICC = 10e-6, 10e-6            # VERIFIED
T45_VIH_A_3V = 2.0                          # VERIFIED VIH (VCCI 3-3.6 V)
T45_IOFF, T45_ICC = 2e-6, 4e-6              # VERIFIED
# ESP32 (REF-01/02 of Phase 1; DS-01/02 here)
ESP_VDD_MIN, ESP_VDD_NOM, ESP_VDD_MAX = 3.0, 3.3, 3.6   # VERIFIED module operating range
ESP_VIH_K, ESP_VIL_K, ESP_VOH_K, ESP_VIH_MAX_OFS = 0.75, 0.25, 0.80, 0.3  # VERIFIED
# Ultrasonic module Adafruit 4007 (RCWL-1601) (DS-13)
US_VCC_MIN, US_VCC_MAX, US_I_TYP = 3.0, 5.5, 2.2e-3      # VENDOR
US_I_ALLOC = 0.020                          # DESIGN allocation (also covers a classic HC-SR04, ~15 mA SECONDARY)
# Connector supply ratings (board specification)
I2C_RATING, GP_RATING, UART_RATING = 0.100, 0.050, 0.100  # DESIGN
# LEDs Kingbright WP7113ID red (DS-11), WP7113SGD green (DS-12)
LED_R_VF_RANGE = (1.6, 2.3)                 # VF 1.9 typ/2.3 max @10 mA VERIFIED; 1.6 V lower bound at ~2 mA ASSUMED (curve-read ~1.7 V)
LED_G_VF_RANGE = (1.8, 2.5)                 # VF 2.2 typ/2.5 max @20 mA VERIFIED; 1.8 V lower bound at ~1.5 mA ASSUMED
R_TOL = 0.01                                # VERIFIED Panasonic ERJ-3EKF (F = +/-1 %) (DS-09)
# I2C (UM10204 Rev 7.0, Phase 1 REF-04)
I2C_VOL, I2C_IOL = 0.4, 3e-3
I2C_TR = {"Standard (100 kHz)": 1000e-9, "Fast (400 kHz)": 300e-9}

# ------------------------------------------------------------------ chosen component values
R_LED_R, R_LED_G = 1500.0, 680.0
R_PULLUP = 2200.0
R_ECHO_SER, R_PD = 1000.0, 100e3
R_UART_TX, R_UART_RX_SER, R_UART_RX_PU = 220.0, 1000.0, 100e3
R_GP_SER = 1000.0
R_GATE = 10e3


def h(t):
    print("\n" + "=" * 80 + "\n" + t + "\n" + "=" * 80)


out = {}

# ------------------------------------------------------------------ 1. load budget
h("1. Load budget (Architecture B: ESP32 DevKit powered by its own USB; board powers peripherals)")
led_r_max = (VIN_MAX - LED_R_VF_RANGE[0]) / (R_LED_R * (1 - R_TOL))
led_g_max = (3.3 * (1 + LDO_ACC) + LDO_LOADREG_MAX - LED_G_VF_RANGE[0]) / (R_LED_G * (1 - R_TOL))
i_3v3 = I2C_RATING + GP_RATING + UART_RATING + led_g_max          # worst: UART jumper on 3V3
i_5v_direct = US_I_ALLOC + led_r_max + T45_ICC + TVS_ID_MAX
i_in = i_5v_direct + i_3v3 + LDO_IQ_MAX
esp_ref = 2 * (3.6 / R_PULLUP) + 2 * G17_ICC + T45_ICC + 3.6 / R_UART_RX_PU + 3.6 / R_PD
print(f"+3V3_P worst load  : I2C {I2C_RATING*1e3:.0f} + GP {GP_RATING*1e3:.0f} + UART {UART_RATING*1e3:.0f} + LED2 {led_g_max*1e3:.2f} = {i_3v3*1e3:.1f} mA")
print(f"+5V_P direct loads : US {US_I_ALLOC*1e3:.0f} + LED1 {led_r_max*1e3:.2f} + LVC1T45 VCCB {T45_ICC*1e6:.0f} uA + TVS leakage {TVS_ID_MAX*1e3:.1f} mA (max at VWM)")
print(f"Input current (worst): {i_in*1e3:.1f} mA   (UART on 5 V moves 100 mA from 3V3 to 5V; total unchanged)")
print(f"3V3_ESP draw from DevKit (reference supply for U2/U3/U4 + pull-ups, worst): {esp_ref*1e3:.2f} mA")
out["i_in"] = i_in

# ------------------------------------------------------------------ 2. PTC
h("2. Overcurrent protection: MF-MSMF050 at T_amb max")
ihold = PTC_IHOLD[50]
print(f"Ihold @50 C = {ihold:.2f} A vs worst load {i_in:.3f} A -> margin x{ihold/i_in:.2f}  ({'PASS' if ihold >= 1.2*i_in else 'CHECK'})")
print(f"Ihold @70 C = {PTC_IHOLD[70]:.2f} A -> margin x{PTC_IHOLD[70]/i_in:.2f} (beyond design ambient)")
print(f"Itrip @23 C = {PTC_ITRIP_23C:.2f} A; Vmax {PTC_VMAX:.0f} V >= {VIN_MAX:.2f} V input (PASS)")
p_ptc = i_in**2 * PTC_R1MAX
print(f"Dissipation at worst load with R1max: {p_ptc*1e3:.0f} mW")

# ------------------------------------------------------------------ 3. reverse-polarity MOSFET
h("3. Reverse-polarity P-MOSFET AO3401A (drain = input side, source = +5V_P, gate -> 10k -> GND)")
vgs = VIN_MIN - i_in * PTC_R1MAX      # gate at 0 V, source ~ +5V_P
print(f"|VGS| at VIN_min with PTC R1max drop: {vgs:.2f} V >= 4.5 V spec point? {'yes' if vgs >= 4.5 else 'no -> use 2.5 V spec (85 mOhm)'}")
rds = Q_RDS_4V5_MAX if vgs >= 4.5 else Q_RDS_2V5_MAX
rds_hot = rds * 1.5                    # ASSUMED +50 % at elevated Tj (datasheet shows ~+25..50 % at 125 C)
v_q = i_in * rds_hot
p_q = i_in**2 * rds_hot
print(f"RDS(on) used {rds*1e3:.0f} mOhm x1.5 (hot, ASSUMED) -> drop {v_q*1e3:.1f} mV, P {p_q*1e3:.2f} mW, dT {p_q*Q_RTHJA_MAX:.2f} C")
print(f"|VGS| max in operation = VIN_max {VIN_MAX:.2f} V; during TVS clamp {TVS_VC} V -> < {Q_VGS_MAX} V rating (PASS)")
print(f"Reverse input -{VIN_MAX:.2f} V: VGS ~ 0 V (< VGS(th) {Q_VGSTH_MAX} V) -> OFF; body diode reverse-biased; |VDS| {VIN_MAX:.2f} V << {Q_VDS_MAX} V (PASS)")

# ------------------------------------------------------------------ 4. rails
h("4. Rail voltages (min / nom / max)")
v5_min = VIN_MIN - i_in * PTC_R1MAX - v_q
v5_nom = VIN_NOM - i_in * 0.5 * (PTC_RMIN + PTC_R1MAX) - i_in * rds
v5_max = VIN_MAX
v33_min = 3.3 * (1 - LDO_ACC) - LDO_LOADREG_MAX
v33_max = 3.3 * (1 + LDO_ACC)
vdo_needed = LDO_VDO_1A_MAX * (i_3v3 / 1.0)   # linear scaling of the 1 A max (conservative upper estimate, ASSUMED shape)
print(f"+5V_P : min {v5_min:.3f}  nom {v5_nom:.3f}  max {v5_max:.3f} V  (current {i_in*1e3:.0f} mA worst)")
print(f"+3V3_P: min {v33_min:.3f}  nom 3.300  max {v33_max:.3f} V  (current {i_3v3*1e3:.0f} mA max)")
print(f"LDO headroom at +5V_P min: {v5_min - 3.3:.3f} V vs dropout estimate {vdo_needed:.3f} V -> {'PASS' if v5_min - 3.3 > vdo_needed else 'FAIL'}")
print(f"LDO VIN max {v5_max:.2f} V <= {LDO_VIN_MAX_ROC} V recommended (PASS); abs max {LDO_VIN_ABS} V")
print(f"Ultrasonic supply {v5_min:.2f}..{v5_max:.2f} V within vendor 3.0..5.5 V (PASS)")
out.update(v5_min=v5_min, v5_max=v5_max)

# ------------------------------------------------------------------ 5. LDO thermal
h("5. LDO thermal (TLV1117LV33, SOT-223)")
p_ldo = (v5_max - 3.3 * (1 - LDO_ACC)) * i_3v3 + v5_max * LDO_IQ_MAX
tj = T_AMB_MAX + p_ldo * LDO_RTHJA
print(f"P_LDO worst = ({v5_max:.2f} - {3.3*(1-LDO_ACC):.3f}) x {i_3v3:.3f} + Iq = {p_ldo:.3f} W")
print(f"Tj = {T_AMB_MAX:.0f} + {p_ldo:.3f} x {LDO_RTHJA} = {tj:.1f} C vs {LDO_TJ_MAX:.0f} C max -> margin {LDO_TJ_MAX - tj:.1f} C")
print("RthJA is the JEDEC high-K value; a 2-layer board with a copper pour on the tab is required to approach it (layout V0.2.0).")
for ra in (90.0, 120.0):
    print(f"  sensitivity: RthJA {ra:.0f} C/W -> Tj {T_AMB_MAX + p_ldo*ra:.1f} C")

# ------------------------------------------------------------------ 6. TVS
h("6. TVS SMAJ6.0A")
print(f"VWM {TVS_VWM} V >= VIN_max {VIN_MAX:.2f} V (PASS: no conduction in normal operation; VBR min {TVS_VBR_MIN} V)")
print(f"Clamp {TVS_VC} V @ {TVS_IPP} A exceeds TLV1117LV abs max {LDO_VIN_ABS} V and LVC abs max 6.5 V at full surge current:")
print("  protects against ESD/short transients; NOT a guarantee for high-energy surges or sustained overvoltage (documented risk).")

# ------------------------------------------------------------------ 7. Echo path
h("7. Ultrasonic ECHO -> SN74LVC1G17 (VCC = 3V3_ESP) -> GPIO34")
vtp_max_36 = G17_VTP_MAX_3V0 + (G17_VTP_MAX_4V5 - G17_VTP_MAX_3V0) * (3.6 - 3.0) / 1.5   # linear interpolation, ASSUMED
echo_hi_min = v5_min * R_PD * (1 - R_TOL) / (R_PD * (1 - R_TOL) + R_ECHO_SER * (1 + R_TOL))   # Echo = VCC (VENDOR) into 1k/100k
print(f"Echo HIGH at buffer input (min): {echo_hi_min:.3f} V vs VT+ max {vtp_max_36:.2f} V (VCC=3.6, interpolated) -> margin {echo_hi_min - vtp_max_36:.2f} V")
print(f"Echo HIGH max {VIN_MAX:.2f} V <= VI max {G17_VI_MAX_ROC} V recommended (independent of VCC) (PASS)")
print(f"Echo LOW must be < VT- min {G17_VTN_MIN_3V0} V (at VCC 3 V); module VOL not specified -> verify by measurement (S1)")
for vdd in (ESP_VDD_MIN, ESP_VDD_NOM, ESP_VDD_MAX):
    voh = vdd - 0.1      # VERIFIED VOH = VCC-0.1 @ -100 uA; GPIO input current 50 nA
    print(f"  VDD={vdd:.1f}: buffer VOH >= {voh:.2f} V vs ESP32 VIH {ESP_VIH_K*vdd:.3f} V (margin {voh-ESP_VIH_K*vdd:.2f}); "
          f"VOH <= VCC = VDD < VDD+0.3 (PASS)")
print(f"Back-power with ESP32 off: buffer Ioff <= {G17_IOFF*1e6:.0f} uA (VERIFIED), output high-Z -> no drive into GPIO (PASS)")
print("Variant independence: a classic 5 V HC-SR04 (Echo ~5 V, SECONDARY) and the RCWL-1601 (Echo = VCC, VENDOR) both satisfy the window.")

# ------------------------------------------------------------------ 8. Trigger path
h("8. GPIO26 -> SN74LVC1T45 (A: VCCA=3V3_ESP, B: VCCB=+5V_P, DIR=H) -> TRIG")
for vdd in (ESP_VDD_MIN, ESP_VDD_NOM, ESP_VDD_MAX):
    print(f"  VDD={vdd:.1f}: ESP32 VOH min {ESP_VOH_K*vdd:.2f} V vs LVC1T45 VIH {T45_VIH_A_3V} V -> margin {ESP_VOH_K*vdd - T45_VIH_A_3V:.2f} V")
trig_hi = v5_min - 0.1
print(f"TRIG HIGH at sensor >= {trig_hi:.2f} V (VCCB-0.1 @100 uA; 100k pull-down = {v5_max/R_PD*1e6:.0f} uA). Sensor VCC = same rail,")
print(f"so TRIG HIGH = {trig_hi/v5_min*100:.0f} % of sensor VCC: meets any CMOS/TTL threshold <= 0.9*VCC (sensor VIH not published: S2 test)")
print("10 us trigger pulse vs tpd < 10 ns: timing unaffected.")

# ------------------------------------------------------------------ 9. UART
h("9. UART")
print(f"RX: device TX (3.3 V or 5 V) -> 1k -> SN74LVC1G17 (VI <= 5.5 V) -> GPIO16: 5 V-logic TX accepted; output <= VDD (PASS)")
print(f"RX idle pull-up 100k to 3V3_ESP; when ESP32 off the buffer is unpowered and Ioff-protected (PASS)")
print(f"TX: GPIO17 -> {R_UART_TX:.0f} ohm -> connector. VOH min {ESP_VOH_K*ESP_VDD_NOM:.2f} V at 3.3 V: OK for 3.3 V devices "
      f"(VIH 0.7*3.3 = {0.7*3.3:.2f} V); 5 V CMOS inputs (VIH 3.5 V) NOT supported")
i_short = ESP_VDD_MAX / R_UART_TX
print(f"TX short-to-GND current limited to {i_short*1e3:.1f} mA (< 40 mA IOH typical) ")
rc = R_UART_TX * 50e-12
print(f"TX RC with 50 pF cable (ASSUMED): {rc*1e9:.1f} ns -> fine up to >1 Mbaud")

# ------------------------------------------------------------------ 10. I2C
h("10. I2C pull-ups 2.2 k to 3V3_ESP (via bridged JP2)")
rpmin = (ESP_VDD_MAX - I2C_VOL) / I2C_IOL
print(f"Rp(min) at VDD 3.6 V = {rpmin:.0f} ohm; 2.2k -1% = {R_PULLUP*(1-R_TOL):.0f} ohm (PASS); with a 10k module pull-up in parallel = {1/(1/2200+1/10000):.0f} ohm (PASS)")
for mode, tr in I2C_TR.items():
    cb_max = tr / (0.8473 * R_PULLUP * (1 + R_TOL))
    print(f"  {mode}: max bus capacitance with 2.2k = {min(cb_max, 400e-12)*1e12:.0f} pF")
print(f"Sink current when low: {(ESP_VDD_MAX-0)/R_PULLUP*1e3:.2f} mA per line (< 3 mA spec)")

# ------------------------------------------------------------------ 11. GP / back-power
h("11. GP inputs and back-power with ESP32 unpowered (board powered)")
i_inj = (3.3 * (1 + LDO_ACC) - 0.6) / R_GP_SER    # 0.6 V ASSUMED protection-diode drop
print(f"GP sensor output 3.3 V into unpowered ESP32 through {R_GP_SER:.0f} ohm: <= {i_inj*1e3:.2f} mA (ESP32 injection limit NOT published: residual risk, R-04)")
print("I2C: pull-ups follow 3V3_ESP, devices are open-drain -> no injection into ESP32. ECHO/RX: Ioff buffers -> none. TRIG: ESP32 is the source.")

# ------------------------------------------------------------------ 12. capacitors
h("12. Capacitors")
dc_bias_keep = 0.40      # ASSUMED fraction of 10 uF (X5R 0603 10 V) retained at 5 V bias (Samsung page gives no DC-bias curve)
print(f"LDO output: 10 uF X5R at 3.3 V, assumed >= {dc_bias_keep*100:.0f} % retained -> {10*dc_bias_keep:.1f} uF effective vs >= 0.5 uF required (PASS, margin x{10*dc_bias_keep/0.5:.0f})")
print("Input/+5V_P: 2 x 10 uF + 100 nF; 10 uF + 100 nF at J3 (sensor burst currents); 100 nF at every logic VCC pin (TI recommendation).")
print(f"Rated voltage: 10 V (10 uF) and 16 V (100 nF) >= {VIN_MAX:.2f} V; TVS clamp {TVS_VC} V transients slightly exceed 10 V rating (short events; documented)")

# ------------------------------------------------------------------ 13. LEDs
h("13. LED currents")
for name, rail_lo, rail_hi, r, vf in (("LED1 red / +5V_P", v5_min, v5_max, R_LED_R, LED_R_VF_RANGE),
                                     ("LED2 green / +3V3_P", v33_min, v33_max, R_LED_G, LED_G_VF_RANGE)):
    imin = (rail_lo - vf[1]) / (r * (1 + R_TOL))
    imax = (rail_hi - vf[0]) / (r * (1 - R_TOL))
    print(f"{name}: R {r:.0f} ohm -> {imin*1e3:.2f} .. {imax*1e3:.2f} mA; P_R max {imax**2*r*1e3:.1f} mW (0.1 W rating)")

# ------------------------------------------------------------------ 14. resistor power
h("14. Resistor dissipation (worst case, 0.1 W ERJ-3EKF)")
for name, v, r in (("R1 gate", VIN_MAX, R_GATE), ("Pull-up 2.2k (line low)", ESP_VDD_MAX, R_PULLUP),
                   ("UART TX 220 (short)", ESP_VDD_MAX, R_UART_TX), ("100k pull-downs", VIN_MAX, R_PD)):
    print(f"  {name}: {v*v/r*1e3:.2f} mW")
print("\nAll outputs CALCULATED from the tagged inputs above.")
