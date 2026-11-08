"""Independent check of the critical V0.1.0 calculations by Monte Carlo sampling (different method from
design_calcs.py, which uses closed-form worst-case corners). Same tagged inputs; 200 000 samples, fixed seed.

Run: python calculations/v0.1.0/independent_checks.py
A check FAILS if any sample violates its limit. Margins reported are the worst sample found.
"""
import random

random.seed(20261108)
N = 200_000
U = random.uniform

worst = {k: float("inf") for k in ("echo_hi_margin", "esp_vih_margin", "esp_vmax_margin", "trig_margin",
                                    "ldo_tj_margin", "ptc_margin", "ldo_headroom", "us_supply_lo", "us_supply_hi",
                                    "i2c_rpmin_margin")}
fails = {k: 0 for k in worst}

for _ in range(N):
    vin = U(4.75, 5.25)                     # DESIGN input spec
    t_amb = U(0.0, 50.0)                    # DESIGN ambient range
    vdd = U(3.0, 3.6)                       # ESP32 VDD (DevKit 3V3), VERIFIED range
    i3 = U(0.0, 0.2524)                     # +3V3_P load (0..rated)
    i5 = U(0.0, 0.0233)                     # +5V_P direct loads (0..allocation)
    iin = i3 + i5 + 100e-6
    r_ptc = U(0.15, 1.0)                    # VERIFIED Rmin..R1max
    rds = U(0.0, 0.085 * 1.5)               # VERIFIED max @2.5 V, x1.5 hot (ASSUMED)
    v5 = vin - iin * (r_ptc + rds)
    # PTC hold at ambient: linear interpolation of the VERIFIED table between 23 and 50 C (0.50 -> 0.40 A)
    ihold = 0.50 if t_amb <= 23 else 0.50 - (0.10 * (t_amb - 23) / 27)
    m = ihold - iin;                               worst["ptc_margin"] = min(worst["ptc_margin"], m); fails["ptc_margin"] += m < 0
    # LDO
    v33 = 3.3 * U(1 - 0.015, 1 + 0.015) - U(0, 0.035)
    m = (v5 - v33) - 0.700 * i3;                   worst["ldo_headroom"] = min(worst["ldo_headroom"], m); fails["ldo_headroom"] += m < 0
    p = (v5 - v33) * i3 + v5 * 100e-6
    tj = t_amb + p * 62.9
    m = 125 - tj;                                  worst["ldo_tj_margin"] = min(worst["ldo_tj_margin"], m); fails["ldo_tj_margin"] += m < 0
    # Ultrasonic supply window (VENDOR 3.0..5.5 V)
    worst["us_supply_lo"] = min(worst["us_supply_lo"], v5 - 3.0); fails["us_supply_lo"] += v5 < 3.0
    worst["us_supply_hi"] = min(worst["us_supply_hi"], 5.5 - v5); fails["us_supply_hi"] += v5 > 5.5
    # Echo: module output = its VCC (VENDOR) through 1k (+-1 %) into 100k (+-1 %) || buffer input
    r6, r7 = 1000 * U(0.99, 1.01), 100e3 * U(0.99, 1.01)
    v_in = v5 * r7 / (r6 + r7)
    vtp_max = 1.92 + (2.74 - 1.92) * (vdd - 3.0) / 1.5          # VERIFIED corners, linear interpolation
    m = v_in - vtp_max;                            worst["echo_hi_margin"] = min(worst["echo_hi_margin"], m); fails["echo_hi_margin"] += m < 0
    m = 5.5 - v5;                                  fails["echo_hi_margin"] += m < 0       # VI <= 5.5 V
    # Buffer output into GPIO: VOH >= VCC-0.1 (VERIFIED, light load), VOH <= VCC
    voh = U(vdd - 0.1, vdd)
    m = voh - 0.75 * vdd;                          worst["esp_vih_margin"] = min(worst["esp_vih_margin"], m); fails["esp_vih_margin"] += m < 0
    m = (vdd + 0.3) - voh;                         worst["esp_vmax_margin"] = min(worst["esp_vmax_margin"], m); fails["esp_vmax_margin"] += m < 0
    # Trigger: ESP32 VOH >= 0.8*VDD vs LVC1T45 VIH 2.0 V (VCCA 3..3.6)
    m = 0.8 * vdd - 2.0;                           worst["trig_margin"] = min(worst["trig_margin"], m); fails["trig_margin"] += m < 0
    # I2C Rp(min) with 2.2k -1 % at VDD
    m = 2200 * 0.99 - (vdd - 0.4) / 3e-3;          worst["i2c_rpmin_margin"] = min(worst["i2c_rpmin_margin"], m); fails["i2c_rpmin_margin"] += m < 0

units = {"echo_hi_margin": "V", "esp_vih_margin": "V", "esp_vmax_margin": "V", "trig_margin": "V", "ldo_tj_margin": "C",
         "ptc_margin": "A", "ldo_headroom": "V", "us_supply_lo": "V", "us_supply_hi": "V", "i2c_rpmin_margin": "ohm"}
print(f"Monte Carlo, {N} samples, seed 20261108")
print(f"{'check':20} {'worst margin':>14} {'violations':>11}  result")
for k in worst:
    print(f"{k:20} {worst[k]:14.3f} {units[k]:3} {fails[k]:7d}  {'PASS' if fails[k] == 0 else 'FAIL'}")
