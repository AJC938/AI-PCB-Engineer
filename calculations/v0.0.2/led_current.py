"""V0.0.2 LED indicator: current, power and tolerance analysis.

Run:  python calculations/v0.0.2/led_current.py
Inputs are tagged with their evidence source (see led_current.md).
"""

# ---- Inputs -----------------------------------------------------------------
VS_NOM = 5.00            # V   requirement (user spec)
VS_TOL = 0.05            # +/-5 % supply tolerance            -> ASSUMED (no supply specified)
R_NOM = 620.0            # ohm   requirement (user spec), E24 value
R_TOL = 0.01             # +/-1 %  Yageo MFR-25 'F' code       -> VERIFIED (Yageo MFR datasheet p.2)
R_RATED_W = 0.25         # W at 70 degC                        -> VERIFIED (Yageo MFR p.3)
R_VMAX = 250.0           # V max working voltage MFR-25      -> VERIFIED (Yageo MFR p.3)

VF_TYP_5MA = 1.80        # V  read from IF-VF curve (~4-5 mA) -> GRAPH-READ, typical (Kingbright WP7113ID p.3)
VF_TYP_10MA = 1.90       # V  table, IF=10 mA                -> VERIFIED (Kingbright p.2)
VF_MAX_10MA = 2.30       # V  table, IF=10 mA                -> VERIFIED (Kingbright p.2)
VF_LOW = 1.70            # V  lower bound = graph typ - 0.1 V (datasheet note: VF tolerance +/-0.1 V)
                         #    -> ASSUMED bound (no VF min in datasheet)
LED_IF_MAX = 0.030       # A  DC forward current             -> VERIFIED (Kingbright p.2)
LED_PD_MAX = 0.075       # W                                  -> VERIFIED (Kingbright p.2)
LED_VR_MAX = 5.0         # V  reverse voltage                 -> VERIFIED (Kingbright p.2)
LED_TC_VF = -1.9e-3      # V/degC                               -> VERIFIED (Kingbright p.2)
J_RATED_A = 17.5         # A  Phoenix MKDS 1,5/2-5,08         -> VERIFIED (Phoenix 1715721 product page)


def current(vs, vf, r):
    return (vs - vf) / r


def main():
    rows = []
    cases = {
        "Nominal (Vs 5.00, VF 1.80 graph, R 620)": (VS_NOM, VF_TYP_5MA, R_NOM),
        "Nominal w/ table VF (VF 1.90 @10 mA)":    (VS_NOM, VF_TYP_10MA, R_NOM),
        "Max current (Vs +5 %, VF low, R -1 %)":   (VS_NOM * (1 + VS_TOL), VF_LOW, R_NOM * (1 - R_TOL)),
        "Min current (Vs -5 %, VF max, R +1 %)":   (VS_NOM * (1 - VS_TOL), VF_MAX_10MA, R_NOM * (1 + R_TOL)),
    }
    print(f"{'Case':44} {'I (mA)':>7} {'P_R (mW)':>9} {'P_LED (mW)':>10} {'V_R (V)':>8}")
    for name, (vs, vf, r) in cases.items():
        i = current(vs, vf, r)
        pr, pled = i * i * r, i * vf
        rows.append((name, i, pr, pled, vs - vf))
        print(f"{name:44} {i*1e3:7.2f} {pr*1e3:9.2f} {pled*1e3:10.2f} {vs - vf:8.2f}")

    i_nom = current(VS_NOM, VF_TYP_5MA, R_NOM)
    i_max = max(r[1] for r in rows)
    pr_max = max(r[2] for r in rows)
    pled_max = max(r[3] for r in rows)
    print("\nSensitivities")
    print(f"  dI/dVF            = {-1/R_NOM*1e3:.3f} mA/V  -> +/-0.1 V VF tolerance = +/-{0.1/R_NOM*1e3:.3f} mA")
    print(f"  R tolerance +/-1 %  -> dI ~ -/+{i_nom*R_TOL*1e3:.3f} mA (~ -/+1 %)")
    print(f"  VF tempco 0..50 degC (ref 25 degC): dVF = +/-{abs(LED_TC_VF)*25*1e3:.1f} mV -> dI = -/+{abs(LED_TC_VF)*25/R_NOM*1e3:.3f} mA")
    print("\nMargins")
    print(f"  Resistor power  : worst {pr_max*1e3:.1f} mW vs {R_RATED_W*1e3:.0f} mW rating -> {pr_max/R_RATED_W*100:.1f} % of rating")
    print(f"  Resistor voltage: worst {max(r[4] for r in rows):.2f} V vs {R_VMAX:.0f} V max")
    print(f"  LED current     : worst {i_max*1e3:.2f} mA vs {LED_IF_MAX*1e3:.0f} mA max -> {i_max/LED_IF_MAX*100:.1f} %")
    print(f"  LED dissipation : worst {pled_max*1e3:.1f} mW vs {LED_PD_MAX*1e3:.0f} mW max")
    print(f"  Connector       : {i_max*1e3:.2f} mA vs {J_RATED_A} A rating")
    vs_rev = VS_NOM * (1 + VS_TOL)
    print(f"  Reverse polarity: LED would see up to ~{vs_rev:.2f} V reverse vs VR max {LED_VR_MAX} V "
          f"-> {'EXCEEDS' if vs_rev > LED_VR_MAX else 'within'} rating (no reverse protection in this test circuit)")


if __name__ == "__main__":
    main()
