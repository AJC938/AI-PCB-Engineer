"""Independent cross-check of the V0.2.0 critical numbers (different method from design_calcs_v020.py).

Method: Monte Carlo (uniform distributions over the datasheet min..max and +-1 % resistors). Trip points
are found by bisection on the pin voltage, not by the closed-form divider equations, so a formula
error in design_calcs_v020.py would show up as a disagreement.
"""
import random

random.seed(20261109)
N = 100_000

def bisect(f, lo, hi, it=60):
    for _ in range(it):
        mid = 0.5 * (lo + hi)
        if f(mid):
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)

def r(nom, tol=0.01):
    return nom * random.uniform(1 - tol, 1 + tol)

viol = {"ovp_below_vin_max": 0, "ovp_above_6v": 0, "uv_above_vin_min": 0, "uv_below_4v2": 0, "ldo_tj_over_110": 0}
ovp_rng = [9, 0]; uv_rng = [9, 0]; tj_rng = [999, 0]
for _ in range(N):
    rt, rm, rb = r(73.2e3), r(5.90e3), r(21.5e3)
    v_ovp_th = random.uniform(1.17, 1.225)
    v_uv_th = random.uniform(1.175, 1.225)
    # pin voltages as a function of VIN (series string, leakage ignored: 100 nA << 50 uA)
    ovp_pin = lambda vin: vin * rb / (rt + rm + rb)
    uv_pin = lambda vin: vin * (rm + rb) / (rt + rm + rb)
    v_ovp = bisect(lambda v: ovp_pin(v) >= v_ovp_th, 0.0, 20.0)
    v_uv = bisect(lambda v: uv_pin(v) >= v_uv_th, 0.0, 20.0)
    ovp_rng = [min(ovp_rng[0], v_ovp), max(ovp_rng[1], v_ovp)]
    uv_rng = [min(uv_rng[0], v_uv), max(uv_rng[1], v_uv)]
    viol["ovp_below_vin_max"] += v_ovp <= 5.25
    viol["ovp_above_6v"] += v_ovp >= 6.0
    viol["uv_above_vin_min"] += v_uv >= 4.75
    viol["uv_below_4v2"] += v_uv < 4.2
    # LDO: VIN uniform within supply spec, load uniform 0..worst, Vout within +-1.5 %, RthJA 84 (+0..10 %)
    vin = random.uniform(4.75, 5.25); iload = random.uniform(0.0, 0.2524); vout = 3.3 * random.uniform(0.985, 1.015)
    p = (vin - vout) * iload + vin * 100e-6
    tj = 50.0 + p * 84.0 * random.uniform(1.0, 1.10)
    tj_rng = [min(tj_rng[0], tj), max(tj_rng[1], tj)]
    viol["ldo_tj_over_110"] += tj > 110.0

print(f"samples {N}, seed 20261109")
print(f"OVP rising trip  : {ovp_rng[0]:.3f} .. {ovp_rng[1]:.3f} V (must stay in 5.25 .. 6.00 V)")
print(f"UVLO rising trip : {uv_rng[0]:.3f} .. {uv_rng[1]:.3f} V (must stay in 4.20 .. 4.75 V)")
print(f"LDO Tj (top copper >= 0.3 in2): {tj_rng[0]:.1f} .. {tj_rng[1]:.1f} C (limit 110 C design target)")
for k, v in viol.items():
    print(f"  {k:20s}: {v} violations -> {'PASS' if v == 0 else 'FAIL'}")
print("RESULT:", "PASS" if not any(viol.values()) else "FAIL")
