"""V0.1.0 Phase 1 planning calculations (no components selected).

Run: python calculations/v0.1.0/phase1_calcs.py
Every input carries an evidence tag:
  VERIFIED  = read from an official document (see datasheets/index_v0.1.0.md)
  SECONDARY = third-party source only, not a manufacturer datasheet
  ASSUMED   = planning placeholder, must be replaced before design freeze
Outputs are CALCULATED planning values, not design approvals.
"""

# ---------------- Inputs ----------------
VIN_NOM, VIN_TOL = 5.0, 0.05      # ASSUMED: 5 V +/-5 % input (input source not yet defined)
VDD_IO_MIN, VDD_IO_NOM, VDD_IO_MAX = 3.0, 3.3, 3.6   # VERIFIED: WROOM-32E v2.1 Table 14 (VDD33 3.0-3.6 V)
VIH_FRAC, VIL_FRAC, VOH_FRAC = 0.75, 0.25, 0.80      # VERIFIED: ESP32 DS v5.3 Table 5-3 / WROOM Table 15
VIH_MAX_OFFSET = 0.3                                  # VERIFIED: VIH max = VDD + 0.3 V (same tables)
ESP_SUPPLY_MIN_A = 0.5            # VERIFIED: WROOM-32E Table 14 "current delivered by external supply" >= 0.5 A
ESP_TX_PEAK_A = 0.379             # VERIFIED: WROOM-32E Table 16, 802.11b 1 Mbps @19.5 dBm peak
ESP_TX_AVG_A = 0.239              # VERIFIED: same table, average
HCSR04_I_A = 0.015                # SECONDARY: "classic" HC-SR04 working current 15 mA (third-party sources)
HCSR04_I_ALLOC_A = 0.020          # ASSUMED allocation (15 mA + margin) until the module is chosen and measured
I2C_3V3_BUDGET_A = 0.100          # ASSUMED budget for 3.3 V I2C peripherals (sensor list TBD)
UART_DEV_BUDGET_A = 0.100         # ASSUMED budget for the UART device (device TBD; rail TBD)
GP_SENSOR_BUDGET_A = 0.050        # ASSUMED budget for optional general-purpose connector
LED_BUDGET_A = 0.004              # ASSUMED: two indicator LEDs at ~2 mA
I2C_VOL, I2C_IOL = 0.4, 0.003     # VERIFIED: UM10204 Rev 7.0 Table 9 (Std/Fast-mode, VDD > 2 V)
I2C_TR = {"Standard-mode (100 kHz)": 1000e-9, "Fast-mode (400 kHz)": 300e-9}  # VERIFIED: UM10204 Table 10
I2C_CB_MAX = 400e-12              # VERIFIED: UM10204 Table 10 (Std/Fast)
E24 = [1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0, 3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1]


def header(t):
    print("\n" + "=" * 78 + "\n" + t + "\n" + "=" * 78)


# ---------------- 1. ESP32 input thresholds ----------------
header("1. ESP32 GPIO limits across the allowed supply range (VERIFIED table formulas)")
for vdd in (VDD_IO_MIN, VDD_IO_NOM, VDD_IO_MAX):
    print(f"VDD={vdd:.2f} V: VIH(min)={VIH_FRAC*vdd:.3f} V  VIL(max)={VIL_FRAC*vdd:.3f} V  "
          f"VIH(max)={vdd+VIH_MAX_OFFSET:.2f} V  VOH(min)={VOH_FRAC*vdd:.3f} V")
print("Note: the datasheets give no 5 V tolerance; VIH(max)=VDD+0.3 V -> a 5 V signal must never reach a GPIO.")

# ---------------- 2. Echo divider ----------------
header("2. HC-SR04 Echo -> ESP32: resistor-divider candidates (1 % resistors)")
print("Echo HIGH level is SECONDARY/UNVERIFIED: 'classic' modules reportedly output 5 V TTL (~= sensor VCC);")
print("'modern' modules reportedly output ~VCC. The swept range below is a planning assumption.")
v_echo_hi = VIN_NOM * (1 + VIN_TOL)          # worst-case high if Echo ~= VCC(max)
v_echo_lo_case = VIN_NOM * (1 - VIN_TOL)     # Echo ~= VCC(min)
vih_worst = VIH_FRAC * VDD_IO_MAX            # highest threshold
vmax_worst = VDD_IO_MIN + VIH_MAX_OFFSET     # lowest absolute input limit (if VDD at its minimum)
print(f"Constraints: Vout(max) <= {vmax_worst:.2f} V (VDD_min+0.3, conservative) and "
      f"Vout(min) >= {vih_worst:.3f} V (0.75*VDD_max)")
cands = []
for top in E24:
    for bot in E24:
        for scale in (1, 10):
            rt, rb = top * 1000, bot * 1000 * scale
            if not (1000 <= rt + rb <= 50000):
                continue
            k_nom = rb / (rt + rb)
            k_max = rb * 1.01 / (rb * 1.01 + rt * 0.99)
            k_min = rb * 0.99 / (rb * 0.99 + rt * 1.01)
            vmax, vmin = v_echo_hi * k_max, v_echo_lo_case * k_min
            if vmax <= vmax_worst and vmin >= vih_worst:
                cands.append((rt + rb, rt, rb, k_nom, vmin, vmax))
cands.sort(key=lambda c: (-(min(c[4] - vih_worst, vmax_worst - c[5])), c[0]))
print(f"{'Rtop':>7} {'Rbot':>7} {'ratio':>6} {'Vout_min':>9} {'Vout_max':>9} {'margin_lo':>9} {'margin_hi':>9} {'I@5V25 mA':>9}")
for tot, rt, rb, k, vmin, vmax in cands[:8]:
    print(f"{rt:7.0f} {rb:7.0f} {k:6.3f} {vmin:9.3f} {vmax:9.3f} {vmin - vih_worst:9.3f} {vmax_worst - vmax:9.3f} {v_echo_hi/(tot)*1e3:9.3f}")
print(f"({len(cands)} E24 pairs satisfy both limits; best-margin pairs shown. Margins are thin: "
      f"window is {vmax_worst - vih_worst:.3f} V wide.)")
rt, rb = 2000.0, 3000.0
k = rb / (rt + rb)
print(f"\nSensitivity of example 2.0k/3.0k (ratio {k:.3f}) to the UNVERIFIED Echo level:")
for v in (5.25, 5.0, 4.75, 4.5, 4.0, 3.3):
    vo = v * k
    ok = "OK" if vih_worst <= vo <= vmax_worst else ("TOO LOW (no valid HIGH at VDD=3.6)" if vo < vih_worst else "TOO HIGH")
    ok_nom = "OK@3.3" if VIH_FRAC * VDD_IO_NOM <= vo <= VDD_IO_NOM + VIH_MAX_OFFSET else "fails@3.3"
    print(f"  Echo HIGH = {v:4.2f} V -> GPIO {vo:5.3f} V : {ok}; {ok_nom}")
print("Conclusion: a passive divider only works if Echo HIGH is close to 5 V. A 3.3 V-output ('modern') module")
print("powered from 3.3 V must NOT get a divider. Echo level must be measured on the chosen module.")
tau = (rt * rb / (rt + rb)) * (2e-12 + 10e-12)   # 2 pF pin (VERIFIED CIN) + 10 pF trace/connector (ASSUMED)
print(f"Divider RC (Thevenin {rt*rb/(rt+rb):.0f} ohm x 12 pF) = {tau*1e9:.1f} ns -> negligible vs echo pulse widths (us-ms).")

# ---------------- 3. Trigger ----------------
header("3. ESP32 -> HC-SR04 Trigger")
voh = VOH_FRAC * VDD_IO_NOM
print(f"ESP32 VOH(min) at 3.3 V = {voh:.2f} V (VERIFIED formula).")
for name, vih in (("TTL-type input, VIH=2.0 V (illustrative)", 2.0),
                  ("CMOS input at 5 V, VIH=0.7*VCC (illustrative)", 0.7 * 5.0)):
    print(f"  vs {name}: {'meets' if voh >= vih else 'DOES NOT meet'} threshold")
print("The sensor's actual trigger threshold is UNVERIFIED (no manufacturer datasheet): Trigger compatibility is TBD.")

# ---------------- 4. Power budget ----------------
header("4. Preliminary power budget (planning allocations)")
loads_5v = {"ESP32 DevKit via 5V pin (Arch. A only)": ESP_SUPPLY_MIN_A,
            "HC-SR04 (5 V)": HCSR04_I_ALLOC_A,
            "UART device (rail TBD; counted on 5 V)": UART_DEV_BUDGET_A,
            "Indicator LEDs": LED_BUDGET_A}
loads_3v3 = {"I2C peripherals": I2C_3V3_BUDGET_A, "General-purpose sensor": GP_SENSOR_BUDGET_A}
i3 = sum(loads_3v3.values())
for arch, include_esp in (("A: board powers DevKit through its 5V pin", True), ("B: DevKit powered by its own USB", False)):
    i5 = sum(v for k2, v in loads_5v.items() if include_esp or "DevKit" not in k2)
    iin = i5 + i3     # linear 3.3 V regulator: input current ~= output current (+ quiescent, ignored)
    print(f"\nArchitecture {arch}")
    print(f"  5 V loads {i5*1e3:6.0f} mA + 3.3 V loads (via linear reg.) {i3*1e3:4.0f} mA = input {iin*1e3:6.0f} mA")
    print(f"  Suggested protection/connector rating basis: >= {iin*1.25*1e3:.0f} mA continuous (+25 % margin, ASSUMED policy)")
print(f"\nESP32 transient: WROOM-32E TX peak {ESP_TX_PEAK_A*1e3:.0f} mA, average {ESP_TX_AVG_A*1e3:.0f} mA (VERIFIED);"
      f" Espressif requires >= {ESP_SUPPLY_MIN_A:.1f} A supply capability (VERIFIED).")

# ---------------- 5. 3.3 V regulator ----------------
header("5. 3.3 V regulator: linear dissipation vs load (VIN max 5.25 V)")
print(f"{'I_out mA':>9} {'P_LDO W':>8} {'P_buck W (eta=0.85, ASSUMED)':>30}")
for ma in (50, 100, 150, 200, 300, 500):
    i = ma / 1000
    p_ldo = (VIN_NOM * (1 + VIN_TOL) - VDD_IO_NOM) * i
    p_buck = VDD_IO_NOM * i * (1 / 0.85 - 1)
    print(f"{ma:9d} {p_ldo:8.3f} {p_buck:30.3f}")
print("Junction rise = P x RthJA of the chosen package (from its datasheet, TBD). At the 150 mA planning budget a")
print("linear regulator dissipates ~0.29 W; confirm against the selected part's RthJA and max Tj before selection.")

# ---------------- 6. Reverse-polarity element drop ----------------
header("6. Reverse-polarity element: voltage drop at planning current (illustrative parameters, NOT parts)")
i_in = sum(v for k2, v in loads_5v.items()) + i3
for name, drop in (("Series Schottky, Vf 0.3 V (illustrative)", 0.3),
                   ("Series Schottky, Vf 0.5 V (illustrative)", 0.5),
                   ("P-MOSFET, Rds(on) 50 mOhm (illustrative)", 0.05 * i_in),
                   ("P-MOSFET, Rds(on) 100 mOhm (illustrative)", 0.10 * i_in)):
    v5 = VIN_NOM * (1 - VIN_TOL) - drop
    print(f"  {name:45} drop {drop:5.3f} V -> 5 V rail min {v5:5.2f} V at {i_in*1e3:.0f} mA")
print("A Schottky drop pushes the 5 V rail toward 4.25-4.45 V at minimum input: check DevKit 5 V-pin regulator")
print("dropout and HC-SR04 minimum supply (both TBD) before choosing the topology.")

# ---------------- 7. I2C pull-ups ----------------
header("7. I2C pull-up range (UM10204 Rev 7.0, VDD = 3.3 V)")
rp_min = (VDD_IO_NOM - I2C_VOL) / I2C_IOL
print(f"Rp(min) = (VDD - VOL)/IOL = ({VDD_IO_NOM} - {I2C_VOL})/{I2C_IOL*1e3:.0f} mA = {rp_min:.0f} ohm (VERIFIED formula)")
for mode, tr in I2C_TR.items():
    for cb in (50e-12, 100e-12, 200e-12, I2C_CB_MAX):
        print(f"  {mode:24} Cb={cb*1e12:4.0f} pF -> Rp(max) = tr/(0.8473*Cb) = {tr/(0.8473*cb):8.0f} ohm")
print("Bus capacitance depends on cable length and connected modules (TBD). Many breakout modules already carry")
print("pull-ups; the parallel combination must stay >= Rp(min). ESP32 internal pull-ups (45 kohm typ.) are too weak.")
