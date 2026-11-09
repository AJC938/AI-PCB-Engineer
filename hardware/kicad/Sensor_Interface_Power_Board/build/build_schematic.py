"""Generate the MCP call sequence that builds the schematic (V0.2.0 revision; V0.1.0 = git 06f223c) (SWIG backend, via ai/workflows/mcp_harness.py).

Usage: python -I build_schematic.py <out_dir>
Writes: s1_create.json (create_project) and s2_build.json (symbols, labels, no-connects, properties).
Between the two runs, set_page_a3.py performs one controlled, verified file edit (paper size and title block).
Single source of truth for the design: PARTS (symbol, value, footprint, MPN, position) and NETS (pin -> net).
Connectivity uses global labels placed exactly on pin endpoints (workaround D-2: no '/'-prefixed local nets).
V0.2.0 (DDR-17/18): F1/Q1/R1/D1 replaced by U5 TPS26600 eFuse (OVP, reverse polarity, current limit);
R15 1k series resistor added on TRIG. See reports/v0.2.0/TVS_LDO_PROTECTION_ANALYSIS.md.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ_DIR = os.path.abspath(os.path.join(HERE, ".."))
NAME = "Sensor_Interface_Power_Board"
SCH = os.path.join(PROJ_DIR, NAME + ".kicad_sch")

FP_R = "Resistor_SMD:R_0603_1608Metric"
FP_C = "Capacitor_SMD:C_0603_1608Metric"
FP_HDR4 = "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical"
FP_TP = "TestPoint:TestPoint_Keystone_5015_Micro_Mini"
DS = {
    "R": "https://industrial.panasonic.com/cdbs/www-data/pdf/RDA0000/AOA0000C304.pdf",
    "C10u": "https://weblib.samsungsem.com/mlcc/mlcc-ec-data-sheet.do?partNumber=CL10A106KP8NNN",
    "C100n": "https://search.murata.co.jp/Ceramy/image/img/A01X/G101/ENG/GRM188R71C104KA01-01.pdf",
    "HDR": "https://suddendocs.samtec.com/catalog_english/tsw_th.pdf",
    "TP": "https://www.keyelco.com/userAssets/file/M65p55.pdf",
    "C1u50": "https://weblib.samsungsem.com/mlcc/mlcc-ec-data-sheet.do?partNumber=CL10A105KB8NNN",
    "C47n": "https://weblib.samsungsem.com/mlcc/mlcc-ec-data-sheet.do?partNumber=CL10B473KB8NNN",
}
R_MPN = {"10k": "ERJ-3EKF1002V", "100k": "ERJ-3EKF1003V", "1k": "ERJ-3EKF1001V", "2.2k": "ERJ-3EKF2201V",
         "220": "ERJ-3EKF2200V", "1.5k": "ERJ-3EKF1501V", "680": "ERJ-3EKF6800V",
         "73.2k": "ERJ-3EKF7322V", "5.9k": "ERJ-3EKF5901V", "21.5k": "ERJ-3EKF2152V", "20k": "ERJ-3EKF2002V"}

# ref: (lib_id, value, footprint, (x, y), angle, manufacturer, mpn, datasheet)
PARTS = {}


def part(ref, sym, val, fp, x, y, ang=0, mfr=None, mpn=None, ds=None):
    PARTS[ref] = dict(sym=sym, val=val, fp=fp, x=x, y=y, ang=ang, mfr=mfr, mpn=mpn, ds=ds)


def res(ref, val, x, y):
    part(ref, "Device:R", val, FP_R, x, y, 0, "Panasonic", R_MPN[val], DS["R"])


def cap(ref, val, x, y):
    if val == "10u":
        part(ref, "Device:C", "10uF", FP_C, x, y, 0, "Samsung Electro-Mechanics", "CL10A106KP8NNNC", DS["C10u"])
    elif val == "1u50":
        part(ref, "Device:C", "1uF 50V", FP_C, x, y, 0, "Samsung Electro-Mechanics", "CL10A105KB8NNNC", DS["C1u50"])
    elif val == "47n":
        part(ref, "Device:C", "47nF", FP_C, x, y, 0, "Samsung Electro-Mechanics", "CL10B473KB8NNNC", DS["C47n"])
    else:
        part(ref, "Device:C", "100nF", FP_C, x, y, 0, "Murata", "GRM188R71C104KA01D", DS["C100n"])


# ---------------- Row 1: power input, protection, regulation, indicators (y = 60)
part("J1", "Connector:Screw_Terminal_01x02", "5V_IN",
     "TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal", 55.88, 60.96, 0,
     "Phoenix Contact", "1715721", "https://www.phoenixcontact.com/en-us/products/printed-circuit-board-terminal-mkds-15-2-508-1715721")
# V0.2.0: eFuse power entry (replaces F1/Q1/R1/D1 of V0.1.0)
cap("C12", "1u50", 76.2, 66.04)
part("U5", "Power_Management:TPS26600PWP", "TPS26600PWPR",
     "Sensor_Interface_Power_Board:TI_PWP0016A_HTSSOP-16-1EP_4.4x5mm_P0.65mm_EP3.4x5mm", 109.22, 66.04, 0,
     "Texas Instruments", "TPS26600PWPR", "https://www.ti.com/lit/ds/symlink/tps2660.pdf")
res("R16", "73.2k", 78.74, 99.06)
res("R17", "5.9k", 88.9, 99.06)
res("R18", "21.5k", 99.06, 99.06)
res("R19", "20k", 114.3, 99.06)
cap("C13", "47n", 127.0, 99.06)
cap("C1", "10u", 157.48, 60.96)
cap("C2", "100n", 170.18, 60.96)
cap("C5", "100n", 182.88, 60.96)
part("U1", "Regulator_Linear:AMS1117-3.3", "TLV1117LV33", "Package_TO_SOT_SMD:SOT-223-3_TabPin2", 215.9, 60.96, 0,
     "Texas Instruments", "TLV1117LV33DCYR", "https://www.ti.com/lit/ds/symlink/tlv1117lv.pdf")
cap("C3", "10u", 248.92, 60.96)
cap("C4", "100n", 261.62, 60.96)
res("R2", "1.5k", 279.4, 60.96)
part("LED1", "Device:LED", "RED 5V", "LED_THT:LED_D5.0mm", 294.64, 60.96, 90,
     "Kingbright", "WP7113ID", "https://www.kingbrightusa.com/images/catalog/SPEC/WP7113ID.pdf")
res("R3", "680", 312.42, 60.96)
part("LED2", "Device:LED", "GREEN 3V3", "LED_THT:LED_D5.0mm", 327.66, 60.96, 90,
     "Kingbright", "WP7113SGD", "https://www.kingbrightusa.com/images/catalog/SPEC/WP7113SGD.pdf")
for i, x in enumerate((350.52, 363.22, 375.92, 388.62), start=1):
    part(f"TP{i}", "Connector:TestPoint", ["VIN", "+5V", "+3V3", "3V3_ESP"][i - 1], FP_TP, x, 55.88, 0,
         "Keystone Electronics", "5015", DS["TP"])

# ---------------- Row 2: ESP32 interface and ultrasonic (y = 130)
part("J2", "Connector_Generic:Conn_01x12", "ESP32_IF", "Connector_PinHeader_2.54mm:PinHeader_1x12_P2.54mm_Vertical",
     60.96, 130.81, 0, "Samtec", "HTSW-112-07-T-S", DS["HDR"])
part("U3", "Logic_LevelTranslator:SN74LVC1T45DBV", "SN74LVC1T45DBVR", "Package_TO_SOT_SMD:SOT-23-6", 109.22, 130.81, 0,
     "Texas Instruments", "SN74LVC1T45DBVR", "https://www.ti.com/lit/ds/symlink/sn74lvc1t45.pdf")
res("R4", "100k", 137.16, 130.81)
res("R5", "100k", 149.86, 130.81)
res("R15", "1k", 190.5, 130.81)
cap("C6", "100n", 162.56, 130.81)
cap("C7", "100n", 175.26, 130.81)
part("J3", "Connector_Generic:Conn_01x04", "ULTRASONIC", FP_HDR4, 205.74, 130.81, 0, "Samtec", "HTSW-104-07-T-S", DS["HDR"])
cap("C8", "10u", 220.98, 130.81)
cap("C9", "100n", 233.68, 130.81)
res("R6", "1k", 248.92, 130.81)
res("R7", "100k", 261.62, 130.81)
part("U2", "74xGxx:74LVC1G17", "SN74LVC1G17DBVR", "Package_TO_SOT_SMD:SOT-23-5", 292.1, 130.81, 0,
     "Texas Instruments", "SN74LVC1G17DBVR", "https://www.ti.com/lit/ds/symlink/sn74lvc1g17.pdf")
cap("C10", "100n", 322.58, 130.81)
for i, x in ((7, 340.36), (8, 353.06)):
    part(f"TP{i}", "Connector:TestPoint", "ECHO_ESP" if i == 7 else "TRIG_5V", FP_TP, x, 125.73, 0,
         "Keystone Electronics", "5015", DS["TP"])

# ---------------- Row 3: I2C, UART, GP (y = 205)
part("J5", "Connector_Generic:Conn_01x04", "I2C", FP_HDR4, 60.96, 205.74, 0, "Samtec", "HTSW-104-07-T-S", DS["HDR"])
res("R8", "2.2k", 81.28, 205.74)
res("R9", "2.2k", 93.98, 205.74)
part("JP2", "Jumper:SolderJumper_2_Bridged", "I2C_PU_EN", "Jumper:SolderJumper-2_P1.3mm_Bridged_RoundedPad1.0x1.5mm",
     121.92, 205.74, 0)
part("J4", "Connector_Generic:Conn_01x04", "UART", FP_HDR4, 162.56, 205.74, 0, "Samtec", "HTSW-104-07-T-S", DS["HDR"])
part("JP1", "Jumper:SolderJumper_3_Bridged12", "UART_VCC_SEL", "Jumper:SolderJumper-3_P1.3mm_Bridged12_RoundedPad1.0x1.5mm",
     190.5, 205.74, 0)
res("R10", "220", 210.82, 205.74)
res("R11", "1k", 223.52, 205.74)
res("R12", "100k", 236.22, 205.74)
part("U4", "74xGxx:74LVC1G17", "SN74LVC1G17DBVR", "Package_TO_SOT_SMD:SOT-23-5", 279.4, 205.74, 0,
     "Texas Instruments", "SN74LVC1G17DBVR", "https://www.ti.com/lit/ds/symlink/sn74lvc1g17.pdf")
cap("C11", "100n", 309.88, 205.74)
part("J6", "Connector_Generic:Conn_01x04", "GP_3V3", FP_HDR4, 342.9, 205.74, 0, "Samtec", "HTSW-104-07-T-S", DS["HDR"])
res("R13", "1k", 360.68, 205.74)
res("R14", "1k", 373.38, 205.74)

# ---------------- Row 4: ground test points and power flags (y = 250)
part("TP5", "Connector:TestPoint", "GND", FP_TP, 45.72, 248.92, 0, "Keystone Electronics", "5015", DS["TP"])
part("TP6", "Connector:TestPoint", "GND", FP_TP, 58.42, 248.92, 0, "Keystone Electronics", "5015", DS["TP"])
FLAGS = {"#FLG01": ("VIN_RAW", 83.82), "#FLG02": ("GND", 99.06), "#FLG03": ("3V3_ESP", 114.3)}

# ---------------- Connectivity: (ref, pin) -> net
NETS = {
    "VIN_RAW": [("J1", 1), ("TP1", 1), ("U5", 1), ("U5", 2), ("C12", 1), ("R16", 1), ("#FLG01", 1)],
    "EF_UVLO": [("R16", 2), ("R17", 1), ("U5", 3)],
    "EF_OVP": [("R17", 2), ("R18", 1), ("U5", 5)],
    "EF_RTN": [("R18", 2), ("U5", 8), ("U5", 17), ("U5", 6), ("R19", 2), ("C13", 2)],
    "EF_ILIM": [("U5", 11), ("R19", 1)],
    "EF_DVDT": [("U5", 12), ("C13", 1)],
    "+5V_P": [("U5", 15), ("U5", 16), ("C1", 1), ("C2", 1), ("C5", 1), ("U1", 3), ("R2", 1), ("TP2", 1),
              ("U3", 6), ("C7", 1), ("J3", 1), ("C8", 1), ("C9", 1), ("JP1", 3)],
    "+3V3_P": [("U1", 2), ("C3", 1), ("C4", 1), ("R3", 1), ("TP3", 1), ("J5", 2), ("JP1", 1), ("J6", 2)],
    "3V3_ESP": [("J2", 1), ("TP4", 1), ("U3", 1), ("U3", 5), ("C6", 1), ("U2", 5), ("C10", 1), ("JP2", 1),
                ("R12", 2), ("U4", 5), ("C11", 1), ("#FLG03", 1)],
    "GND": [("J1", 2), ("U5", 9), ("C12", 2), ("C1", 2), ("C2", 2), ("C5", 2), ("U1", 1), ("C3", 2), ("C4", 2),
            ("LED1", 1), ("LED2", 1), ("J2", 2), ("J2", 11), ("J2", 12), ("U3", 2), ("R4", 2), ("R5", 2), ("C6", 2),
            ("C7", 2), ("J3", 4), ("C8", 2), ("C9", 2), ("R7", 2), ("U2", 3), ("C10", 2), ("J5", 1), ("J4", 1),
            ("U4", 3), ("C11", 2), ("J6", 1), ("TP5", 1), ("TP6", 1), ("#FLG02", 1)],
    "LED1_A": [("R2", 2), ("LED1", 2)],
    "LED2_A": [("R3", 2), ("LED2", 2)],
    "US_TRIG_ESP": [("J2", 3), ("U3", 3), ("R4", 1)],
    "US_TRIG_B": [("U3", 4), ("R15", 1)],
    "US_TRIG_5V": [("R15", 2), ("R5", 1), ("J3", 2), ("TP8", 1)],
    "US_ECHO_5V": [("J3", 3), ("R6", 1)],
    "US_ECHO_IN": [("R6", 2), ("R7", 1), ("U2", 2)],
    "US_ECHO_ESP": [("U2", 4), ("J2", 4), ("TP7", 1)],
    "I2C_SDA": [("J2", 5), ("J5", 3), ("R8", 2)],
    "I2C_SCL": [("J2", 6), ("J5", 4), ("R9", 2)],
    "I2C_PU": [("JP2", 2), ("R8", 1), ("R9", 1)],
    "UART_TX_ESP": [("J2", 7), ("R10", 1)],
    "UART_TX": [("R10", 2), ("J4", 3)],
    "UART_RX": [("J4", 4), ("R11", 1)],
    "UART_RX_IN": [("R11", 2), ("R12", 1), ("U4", 2)],
    "UART_RX_ESP": [("U4", 4), ("J2", 8)],
    "UART_VCC": [("JP1", 2), ("J4", 2)],
    "GP_IO1_ESP": [("J2", 9), ("R13", 2)],
    "GP_IO1": [("J6", 3), ("R13", 1)],
    "GP_IO2_ESP": [("J2", 10), ("R14", 2)],
    "GP_IO2": [("J6", 4), ("R14", 1)],
}
# U5: 4/13 NC (datasheet N.C); 7 SHDN floats high internally (enabled, TI Fig. 69 minimal configuration);
# 10 IMON and 14 FLT unused ("If unused, leave floating", TI pin table p.4).
NO_CONNECT = [("U2", 1), ("U4", 1), ("U5", 4), ("U5", 13), ("U5", 7), ("U5", 10), ("U5", 14)]


def main(out):
    s1 = [{"label": "create", "name": "create_project", "arguments": {"path": PROJ_DIR, "name": NAME}}]
    s2 = []
    for ref, p in PARTS.items():
        args = {"schematicPath": SCH, "symbol": p["sym"], "reference": ref, "value": p["val"],
                "position": {"x": p["x"], "y": p["y"]}, "angle": p["ang"]}
        if p["fp"]:
            args["footprint"] = p["fp"]
        s2.append({"label": f"add_{ref}", "name": "add_schematic_component", "arguments": args})
    for ref, (net, x) in FLAGS.items():
        s2.append({"label": f"add_{ref}", "name": "add_schematic_component", "arguments": {
            "schematicPath": SCH, "symbol": "power:PWR_FLAG", "reference": ref, "value": "PWR_FLAG",
            "position": {"x": x, "y": 248.92}, "angle": 0}})
    for net, pins in NETS.items():
        for ref, pin in pins:
            s2.append({"label": f"lbl_{ref}_{pin}", "name": "add_schematic_net_label", "arguments": {
                "schematicPath": SCH, "netName": net, "labelType": "global_label",
                "componentRef": ref, "pinNumber": str(pin)}})
    for ref, pin in NO_CONNECT:
        s2.append({"label": f"nc_{ref}_{pin}", "name": "add_no_connect", "arguments": {
            "schematicPath": SCH, "componentRef": ref, "pinNumber": str(pin)}})
    for ref, p in PARTS.items():
        for prop, key in (("Manufacturer", "mfr"), ("MPN", "mpn"), ("Datasheet", "ds")):
            if p[key]:
                s2.append({"label": f"prop_{ref}_{prop}", "name": "set_schematic_component_property", "arguments": {
                    "schematicPath": SCH, "reference": ref, "name": prop, "value": p[key]}})
    s2 += [{"label": "validate", "name": "validate_schematic", "arguments": {"schematicPath": SCH}},
           {"label": "erc", "name": "run_erc", "arguments": {"schematicPath": SCH}},
           {"label": "netlist", "name": "generate_netlist", "arguments": {"schematicPath": SCH}}]
    os.makedirs(out, exist_ok=True)
    json.dump(s1, open(os.path.join(out, "s1_create.json"), "w"), indent=1)
    json.dump(s2, open(os.path.join(out, "s2_build.json"), "w"), indent=1)
    npins = sum(len(v) for v in NETS.values())
    print(f"parts {len(PARTS)} + flags {len(FLAGS)}; nets {len(NETS)}; pin-labels {npins}; steps s2 {len(s2)}")
    # sanity: each (ref,pin) used once
    seen = {}
    for net, pins in NETS.items():
        for rp in pins:
            assert rp not in seen, f"pin {rp} on two nets: {seen[rp]} and {net}"
            seen[rp] = net
    print("pin uniqueness: OK")


if __name__ == "__main__":
    main(sys.argv[1])
