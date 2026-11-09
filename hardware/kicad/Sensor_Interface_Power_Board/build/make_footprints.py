"""Create the project-local footprint for U5 (TPS26600PWPR) from the KiCad library footprint.

Why: the KiCad footprint HTSSOP-16-1EP_4.4x5mm_P0.65mm_EP3.4x5mm_Mask2.66x2.46mm follows TI package
PWP0016H (its descr points to an older TPS2660 datasheet page 48). The current datasheet
TI SLVSDG2G (Dec 2019) specifies package PWP0016A with this land pattern (p.53) and stencil (p.54):
  - 16 signal pads 1.5 x 0.45 mm, pitch 0.65 mm, pad-centre span 5.8 mm
  - exposed metal 3.4 x 5.0 mm, solder-mask-defined opening 3.3 x 3.3 mm
  - paste 3.3 x 3.3 mm (100 % at 0.125 mm stencil)
The KiCad library file is only read, never modified. Output goes to the project library
../Sensor_Interface_Power_Board.pretty/. Every change is asserted.
Usage: python -I make_footprints.py <kicad_footprint_dir>
"""
import os
import re
import sys

SRC_NAME = "HTSSOP-16-1EP_4.4x5mm_P0.65mm_EP3.4x5mm_Mask2.66x2.46mm"
NEW_NAME = "TI_PWP0016A_HTSSOP-16-1EP_4.4x5mm_P0.65mm_EP3.4x5mm"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.abspath(os.path.join(HERE, "..", "Sensor_Interface_Power_Board.pretty"))

src = os.path.join(sys.argv[1], "Package_SO.pretty", SRC_NAME + ".kicad_mod")
s = open(src, encoding="utf-8").read()

# 1. name, descr, tags
s = s.replace(f'(footprint "{SRC_NAME}"', f'(footprint "{NEW_NAME}"', 1)
s = s.replace(f'(property "Value" "{SRC_NAME}"', f'(property "Value" "{NEW_NAME}"', 1)
s, n = re.subn(r'\(descr "[^"]*"\)',
               '(descr "TI PWP0016A PowerPAD HTSSOP-16 per TPS2660 datasheet SLVSDG2G p.53 land pattern, p.54 stencil; '
               'derived from KiCad ' + SRC_NAME + '")', s, count=1)
assert n == 1
s, n = re.subn(r'\(tags "[^"]*"\)', '(tags "HTSSOP SO Texas_PWP0016A TPS2660")', s, count=1)
assert n == 1

# 2. signal pads 1..16: size 1.575x0.4 -> 1.5x0.45, x +-2.8625 -> +-2.9
cnt = 0
def fix_pad(m):
    global cnt
    cnt += 1
    body = m.group(0)
    body = re.sub(r"\(at (-?)2\.8625 ", lambda a: f"(at {a.group(1)}2.9 ", body)
    body = body.replace("(size 1.575 0.4)", "(size 1.5 0.45)")
    assert "(size 1.5 0.45)" in body and "2.9 " in body, body
    return body
s = re.sub(r'\(pad "(?:[1-9]|1[0-6])" smd roundrect\s*\(at [^)]*\)\s*\(size 1\.575 0\.4\)', fix_pad, s)
assert cnt == 16, cnt

# 3. mask opening 2.66x2.46 -> 3.3x3.3 (solder-mask-defined, TI p.53)
s, n = re.subn(r'(\(pad "" smd rect\s*\(at 0 0\)\s*)\(size 2\.66 2\.46\)(\s*\(layers "F\.Mask"\))',
               r"\1(size 3.3 3.3)\2", s)
assert n == 1

# 4. paste: replace the two 2.14x0.99 segments by one 3.3x3.3 aperture (TI p.54, 0.125 mm stencil)
pat = r'\t\(pad "" smd roundrect\s*\(at 0 -?0\.615\)\s*\(size 2\.14 0\.99\)\s*\(layers "F\.Paste"\)[^)]*\)\s*\)\n'
s, n = re.subn(pat, "", s)
assert n == 2, n
paste = '\t(pad "" smd rect\n\t\t(at 0 0)\n\t\t(size 3.3 3.3)\n\t\t(layers "F.Paste")\n\t)\n'
s = s.replace('\t(pad "1" smd roundrect', paste + '\t(pad "1" smd roundrect', 1)

# 5. exposed copper unchanged (3.4 x 5.0 = TI metal), check it
assert re.search(r'\(pad "17" smd rect\s*\(at 0 0\)\s*\(size 3\.4 5\)', s)
assert s.count("(") == s.count(")")

os.makedirs(OUT_DIR, exist_ok=True)
dst = os.path.join(OUT_DIR, NEW_NAME + ".kicad_mod")
open(dst, "w", encoding="utf-8", newline="\n").write(s)
print("written", os.path.basename(dst), "pads fixed:", cnt)
