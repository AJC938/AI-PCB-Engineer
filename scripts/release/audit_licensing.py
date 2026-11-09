# SPDX-FileCopyrightText: 2026 AI-PCB-Engineer contributors
# SPDX-License-Identifier: MIT
"""Licence-compliance audit of the repository and the release packages (read-only).

 L1 LICENSE-HARDWARE is byte-identical to the official CERN-OHL-P-2.0 text (SHA-256 recorded below) and to LICENSES/
 L2 LICENSE-CODE = the OSI MIT text with only the copyright line filled in; LICENSES/MIT.txt = the OSI template
 L3 no copyright-holder placeholder left in any committable file
 L4 every committable file resolves to a licence through REUSE.toml (last matching annotation, or in-file SPDX header)
 L5 scope rules: *.py/*.sh -> MIT; KiCad design/manufacturing/renders -> CERN-OHL-P-2.0;
    U5 project footprint -> CC-BY-SA-4.0 WITH KiCad-libraries-exception; no other licence id used
 L6 no SPDX header or manifest entry names CERN-OHL-S/W (the superseded or unused variants)
 L7 every PDF in the repository is a KiCad export (no redistributed datasheet)
 L8 every release ZIP contains NOTICE.md and LICENSE-HARDWARE.txt identical to the repository root
 L9 the derived U5 footprint states its KiCad origin (descr) and is listed in THIRD_PARTY_NOTICES.md and MODIFICATIONS.md
Usage: python -I audit_licensing.py <repo_root>
"""
import glob
import hashlib
import os
import re
import subprocess
import sys
import tomllib
import zipfile

root = os.path.abspath(sys.argv[1])
os.chdir(root)
OFFICIAL_CERN_OHL_P_SHA256 = "6e471d647db50527d0c75ee5f1a55a74012ab177c73282bef0bdc7f6562b7ded"
res = []
PLACEHOLDER = "@@" + "HOLDER@@"  # split so that the holder substitution never rewrites this check


def check(cid, ok, msg):
    res.append((cid, ok, msg))


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


files = sorted(set(subprocess.run(["git", "ls-files", "-c", "-o", "--exclude-standard"], capture_output=True,
                                  text=True, check=True).stdout.split("\n")) - {""})
files = [f for f in files if os.path.isfile(f)]

hw = open("LICENSE-HARDWARE", "rb").read()
check("L1", sha("LICENSE-HARDWARE") == OFFICIAL_CERN_OHL_P_SHA256 and hw == open("LICENSES/CERN-OHL-P-2.0.txt", "rb").read()
      and hw.startswith(b"CERN Open Hardware Licence Version 2 - Permissive"),
      f"LICENSE-HARDWARE sha256 {sha('LICENSE-HARDWARE')[:16]}… = official; identical to LICENSES/CERN-OHL-P-2.0.txt")

code = open("LICENSE-CODE", encoding="utf-8").read().split("\n")
tmpl = open("LICENSES/MIT.txt", encoding="utf-8").read().split("\n")
first_ok = re.fullmatch(r"Copyright 2026 \S.*", code[0]) is not None and PLACEHOLDER not in code[0]
check("L2", first_ok and code[1:] == tmpl[1:] and tmpl[0] == "Copyright <YEAR> <COPYRIGHT HOLDER>",
      f"LICENSE-CODE line 1 = {code[0]!r}; body identical to the OSI MIT text: {code[1:] == tmpl[1:]}")

ph = [f for f in files if not f.endswith((".png", ".zip", ".pdf", ".step"))
      and PLACEHOLDER in open(f, encoding="utf-8", errors="replace").read()]
check("L3", not ph, f"files with the holder placeholder: {ph[:8]}{' …' if len(ph) > 8 else ''}")


def glob_re(p):
    out, i = "", 0
    while i < len(p):
        if p.startswith("**/", i):
            out += "(?:.*/)?"
            i += 3
        elif p.startswith("**", i):
            out += ".*"
            i += 2
        elif p[i] == "*":
            out += "[^/]*"
            i += 1
        else:
            out += re.escape(p[i])
            i += 1
    return re.compile(out + r"\Z")


ann = tomllib.load(open("REUSE.toml", "rb"))["annotations"]
rules = [([glob_re(p) for p in ([a["path"]] if isinstance(a["path"], str) else a["path"])],
          a["SPDX-License-Identifier"]) for a in ann]
IGNORED = re.compile(r"^(LICENSES/|LICEN[CS]E([-.].*)?$|\.git/)")


def licence_of(f):
    head = open(f, encoding="utf-8", errors="replace").read(400) if not f.endswith((".png", ".zip", ".pdf", ".step")) else ""
    m = re.search(r"SPDX-License-Identifier:\s*([^\n\"]+)", head)
    if m and not f.endswith("REUSE.toml"):
        return m.group(1).strip()
    lic = None
    for pats, ident in rules:
        if any(p.match(f) for p in pats):
            lic = ident
    return lic


lic = {f: licence_of(f) for f in files if not IGNORED.match(f)}
unmapped = [f for f, l in lic.items() if not l]
check("L4", not unmapped, f"{len(lic)} files resolved to a licence; unmapped {unmapped[:5]}")

ALLOWED = {"CERN-OHL-P-2.0", "MIT", "CC-BY-SA-4.0 WITH KiCad-libraries-exception"}
bad = []
for f, l in lic.items():
    if l not in ALLOWED:
        bad.append((f, l))
    if f.endswith((".py", ".sh")) and l != "MIT":
        bad.append((f, l))
    if re.search(r"\.(kicad_pcb|kicad_sch|kicad_pro|gtl|gbl|drl|d356|step|zip)$", f) and l != "CERN-OHL-P-2.0":
        bad.append((f, l))
    if f.startswith("media/renders/") and l != "CERN-OHL-P-2.0":
        bad.append((f, l))
u5 = "hardware/kicad/Sensor_Interface_Power_Board/Sensor_Interface_Power_Board.pretty/" \
     "TI_PWP0016A_HTSSOP-16-1EP_4.4x5mm_P0.65mm_EP3.4x5mm.kicad_mod"
if lic.get(u5) != "CC-BY-SA-4.0 WITH KiCad-libraries-exception":
    bad.append((u5, lic.get(u5)))
counts = {}
for l in lic.values():
    counts[l] = counts.get(l, 0) + 1
check("L5", not bad, f"scope rules; licence counts {counts}; violations {bad[:5]}")

sw = []
for f in files:
    if f.endswith((".png", ".zip", ".pdf", ".step")):
        continue
    for line in open(f, encoding="utf-8", errors="replace"):
        if re.search(r"SPDX-License-Identifier\s*[:=]\s*\"?CERN-OHL-[SW]", line):
            sw.append(f)
check("L6", not sw, f"SPDX identifiers naming CERN-OHL-S/W: {sw}")

nonkicad = []
for f in [f for f in files if f.endswith(".pdf")]:
    head = open(f, "rb").read()
    if b"KiCad PDF" not in head and b"KiCad" not in head[:200000]:
        nonkicad.append(f)
check("L7", not nonkicad, f"{sum(f.endswith('.pdf') for f in files)} PDFs, all KiCad exports; others: {nonkicad}")

zbad = []
for z in glob.glob("manufacturing/Sensor_Interface_Power_Board/RevA/packages/*.zip"):
    name = os.path.splitext(os.path.basename(z))[0]
    with zipfile.ZipFile(z) as zz:
        for arc, src in (("NOTICE.md", "NOTICE.md"), ("LICENSE-HARDWARE.txt", "LICENSE-HARDWARE")):
            try:
                if zz.read(f"{name}/{arc}") != open(src, "rb").read():
                    zbad.append(f"{name}: {arc} differs")
            except KeyError:
                zbad.append(f"{name}: {arc} missing")
check("L8", not zbad and len(glob.glob("manufacturing/Sensor_Interface_Power_Board/RevA/packages/*.zip")) == 3,
      f"3 ZIPs carry NOTICE.md + LICENSE-HARDWARE.txt: {zbad or 'OK'}")

descr = open(u5, encoding="utf-8").read()
tpn = open("THIRD_PARTY_NOTICES.md", encoding="utf-8").read()
mods = open("MODIFICATIONS.md", encoding="utf-8").read()
check("L9", "derived from KiCad" in descr and os.path.basename(u5) in tpn and os.path.basename(u5) in mods,
      "U5 footprint provenance recorded (descr, THIRD_PARTY_NOTICES.md, MODIFICATIONS.md)")

for cid, ok, msg in res:
    print(f"{cid}: {'PASS' if ok else 'FAIL'}  {msg}")
print(f"RESULT: {'PASS' if all(ok for _, ok, _ in res) else 'FAIL'} ({sum(ok for _, ok, _ in res)}/{len(res)})")
sys.exit(0 if all(ok for _, ok, _ in res) else 1)
