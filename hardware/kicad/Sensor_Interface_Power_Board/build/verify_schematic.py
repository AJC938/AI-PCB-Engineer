"""Independent schematic verification from the kicad-cli XML netlist (no MCP involved).

Usage: python -I verify_schematic.py <netlist.xml> <kicad_footprints_dir>
Checks:
 1. Every design net (build_schematic.NETS) exists with exactly the intended pins; no extra nets with >1 node.
 2. Power-domain rules: ESP32 GPIO nets touch only 3.3 V-domain parts; +3V3_P and 3V3_ESP never share a node;
    no 5 V-capable node (+5V_P, J3 signals, UART RX connector) is on any ESP32 net.
 3. Footprints: every assigned footprint exists, and every symbol pin number has a matching pad.
 4. BOM metadata: Manufacturer and MPN present on every non-virtual part.
 V0.2.0: eFuse rules (RTN island never on GND, IN on VIN_RAW, OUT on +5V_P), TRIG series resistor,
         project-local footprint library resolved from the project folder.
Exit code 1 on any failure.
"""
import os
import re
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_schematic as B  # noqa: E402

net_xml, fp_dir = sys.argv[1], sys.argv[2]
root = ET.parse(net_xml).getroot()
fails = []

# ---- 1. nets
actual = {}
for n in root.iter("net"):
    nodes = {(x.get("ref"), int(x.get("pin"))) for x in n.iter("node") if x.get("pin").isdigit()}
    actual[n.get("name")] = nodes
for net, pins in B.NETS.items():
    exp = {(r, p) for r, p in pins if not r.startswith("#")}
    got = actual.get(net)
    if got is None:
        fails.append(f"net {net} missing")
    elif got != exp:
        fails.append(f"net {net} mismatch: missing {sorted(exp - got)} extra {sorted(got - exp)}")
design_names = set(B.NETS)
for name, nodes in actual.items():
    if name not in design_names and len(nodes) > 1:
        fails.append(f"unexpected multi-node net {name}: {sorted(nodes)}")
unconnected = sorted(n for n, nodes in actual.items() if n.startswith("unconnected-"))
print(f"[1] nets checked: {len(B.NETS)} design nets; actual nets {len(actual)}; single-pin 'unconnected-' nets: {unconnected}")

# ---- 2. domains
ESP_NETS = ["US_TRIG_ESP", "US_ECHO_ESP", "I2C_SDA", "I2C_SCL", "UART_TX_ESP", "UART_RX_ESP", "GP_IO1_ESP", "GP_IO2_ESP"]
FIVE_V_NODES = set(map(tuple, B.NETS["+5V_P"])) | {("J3", 2), ("J3", 3), ("J4", 4), ("J1", 1)}
ALLOWED = {  # parts allowed on each ESP32 net (all 3.3 V-domain or series/pull elements)
    "US_TRIG_ESP": {"J2", "U3", "R4"}, "US_ECHO_ESP": {"J2", "U2", "TP7"}, "I2C_SDA": {"J2", "J5", "R8"},
    "I2C_SCL": {"J2", "J5", "R9"}, "UART_TX_ESP": {"J2", "R10"}, "UART_RX_ESP": {"J2", "U4"},
    "GP_IO1_ESP": {"J2", "R13"}, "GP_IO2_ESP": {"J2", "R14"}}
for net in ESP_NETS:
    nodes = actual.get(net, set())
    refs = {r for r, _ in nodes}
    if refs - ALLOWED[net]:
        fails.append(f"domain: {net} touches {sorted(refs - ALLOWED[net])}")
    if nodes & FIVE_V_NODES:
        fails.append(f"domain: 5 V node on ESP32 net {net}: {sorted(nodes & FIVE_V_NODES)}")
if actual.get("+3V3_P", set()) & actual.get("3V3_ESP", set()):
    fails.append("domain: +3V3_P and 3V3_ESP share a node")
# buffers powered from the ESP32 rail
for ref, pin in (("U2", 5), ("U4", 5), ("U3", 1), ("U3", 5)):
    if (ref, pin) not in actual.get("3V3_ESP", set()):
        fails.append(f"domain: {ref} pin {pin} not on 3V3_ESP")
if ("U3", 6) not in actual.get("+5V_P", set()):
    fails.append("domain: U3 VCCB not on +5V_P")
# eFuse (TI SLVSDG2G 9.3.5.5 / 10.4: never connect RTN to GND; support parts referenced to RTN)
rtn, gnd = actual.get("EF_RTN", set()), actual.get("GND", set())
if not rtn or ("U5", 8) in gnd or ("U5", 17) in gnd:
    fails.append("efuse: RTN net missing or RTN pin on GND")
for ref, pin in (("U5", 8), ("U5", 17), ("U5", 6)):
    if (ref, pin) not in rtn:
        fails.append(f"efuse: U5 pin {pin} not on EF_RTN")
if ("U5", 9) not in gnd:
    fails.append("efuse: U5 GND pin 9 not on GND")
if not {("U5", 1), ("U5", 2)} <= actual.get("VIN_RAW", set()):
    fails.append("efuse: U5 IN not on VIN_RAW")
if not {("U5", 15), ("U5", 16)} <= actual.get("+5V_P", set()):
    fails.append("efuse: U5 OUT not on +5V_P")
if ("J3", 2) in actual.get("US_TRIG_B", set()) or ("R15", 1) not in actual.get("US_TRIG_B", set()):
    fails.append("trig: R15 series resistor missing between U3-B and J3")
print(f"[2] domain rules checked on {len(ESP_NETS)} ESP32 nets")

# ---- 3. footprints vs pins
libparts = {(lp.get("lib"), lp.get("part")): {p.get("num") for p in lp.iter("pin")} for lp in root.iter("libpart")}
n_fp = 0
for comp in root.iter("comp"):
    ref, fp = comp.get("ref"), comp.findtext("footprint")
    ls = comp.find("libsource")
    pins = libparts.get((ls.get("lib"), ls.get("part")), set())
    if not fp:
        fails.append(f"fp: {ref} has no footprint")
        continue
    lib, name = fp.split(":", 1)
    base = B.PROJ_DIR if lib == B.NAME else fp_dir
    path = os.path.join(base, lib + ".pretty", name + ".kicad_mod")
    if not os.path.isfile(path):
        fails.append(f"fp: {ref} footprint not found {fp}")
        continue
    pads = set(re.findall(r'\(pad "([^"]*)"', open(path, encoding="utf-8").read()))
    if pins - pads:
        fails.append(f"fp: {ref} pins {sorted(pins - pads)} have no pad in {fp}")
    n_fp += 1
print(f"[3] footprints verified: {n_fp}")

# ---- 4. metadata
n_meta = 0
for comp in root.iter("comp"):
    ref = comp.get("ref")
    if ref.startswith("JP"):
        continue  # PCB solder jumpers: no part
    f = {x.get("name"): (x.text or "") for x in comp.iter("field")}
    if not f.get("MPN") or not f.get("Manufacturer"):
        fails.append(f"meta: {ref} lacks MPN/Manufacturer")
    else:
        n_meta += 1
print(f"[4] parts with Manufacturer+MPN: {n_meta}")

print("\nRESULT:", "PASS" if not fails else "FAIL")
for f in fails:
    print("  -", f)
sys.exit(1 if fails else 0)
