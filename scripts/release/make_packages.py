"""Build, test and checksum the three Rev A manufacturing ZIP packages.

1. Builds deterministic ZIPs (sorted entries, fixed timestamp, POSIX paths, one top-level folder):
     Sensor_Interface_PCB_RevA_Fabrication.zip            bare-board fabrication only
     Sensor_Interface_PCB_RevA_Assembly.zip               BOM, CPL, drawings, notes
     Sensor_Interface_PCB_RevA_Complete_Manufacturing.zip fabrication + assembly + 3D
   Each ZIP contains README.md (from scripts/release/package_readmes/) and MANIFEST-SHA256.txt.
2. Tests every ZIP: CRC test, extraction into a fresh temporary directory, byte-identical comparison with the
   source files, no absolute/parent/backslash paths, no machine-specific strings in any member.
3. Writes <rev>/checksums/SHA256SUMS.txt for the ZIPs and every file of the release folder.
Usage: python -I make_packages.py <manufacturing/<board>/RevA>
"""
import hashlib
import os
import re
import sys
import tempfile
import zipfile

rev_dir = os.path.abspath(sys.argv[1])
here = os.path.dirname(os.path.abspath(__file__))
readmes = os.path.join(here, "package_readmes")
pkg_dir = os.path.join(rev_dir, "packages")
sum_dir = os.path.join(rev_dir, "checksums")
os.makedirs(pkg_dir, exist_ok=True)
os.makedirs(sum_dir, exist_ok=True)
DATE = (2026, 11, 9, 0, 0, 0)
# strings that must never appear in a public package (machine-specific)
FORBIDDEN = [re.compile(rb"(?i)[A-Z]:[\\/]+Users[\\/]+"), re.compile(rb"(?i)/home/[a-z]"),
             re.compile(rb"(?i)AppData[\\/]")]
for var in ("USERNAME", "USER", "COMPUTERNAME", "HOSTNAME"):  # the local account/host name, read at run time
    val = os.environ.get(var, "")
    if len(val) >= 3:
        FORBIDDEN.append(re.compile(re.escape(val.encode()), re.I))


def sha(path_or_bytes):
    h = hashlib.sha256()
    if isinstance(path_or_bytes, bytes):
        h.update(path_or_bytes)
    else:
        with open(path_or_bytes, "rb") as fh:
            h.update(fh.read())
    return h.hexdigest()


def listdir(sub):
    d = os.path.join(rev_dir, sub)
    return sorted(os.path.join(d, f) for f in os.listdir(d) if os.path.isfile(os.path.join(d, f)))


fab = listdir("fabrication")
asm = listdir("assembly")
m3d = listdir("3d")
PACKAGES = {
    "Sensor_Interface_PCB_RevA_Fabrication": ("FABRICATION.md", [("", f) for f in fab]),
    "Sensor_Interface_PCB_RevA_Assembly": ("ASSEMBLY.md", [("", f) for f in asm]),
    "Sensor_Interface_PCB_RevA_Complete_Manufacturing": (
        "COMPLETE.md", [("fabrication/", f) for f in fab] + [("assembly/", f) for f in asm] + [("3d/", f) for f in m3d]),
}

fails = []
for name, (readme, members) in PACKAGES.items():
    zpath = os.path.join(pkg_dir, name + ".zip")
    entries = [(f"{name}/README.md", open(os.path.join(readmes, readme), "rb").read())]
    for sub, src in members:
        entries.append((f"{name}/{sub}{os.path.basename(src)}", open(src, "rb").read()))
    manifest = "".join(f"{sha(b)}  {arc[len(name) + 1:]}\n" for arc, b in sorted(entries))
    entries.append((f"{name}/MANIFEST-SHA256.txt", manifest.encode()))
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for arc, data in sorted(entries):
            zi = zipfile.ZipInfo(arc, DATE)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, data)
    # ---- test
    with zipfile.ZipFile(zpath) as z:
        bad = z.testzip()
        names = z.namelist()
        with tempfile.TemporaryDirectory() as tmp:
            z.extractall(tmp)
            for arc, data in entries:
                got = open(os.path.join(tmp, *arc.split("/")), "rb").read()
                if got != data:
                    fails.append(f"{name}: {arc} differs after extraction")
                for pat in FORBIDDEN:
                    if pat.search(got):
                        fails.append(f"{name}: {arc} contains machine-specific text {pat.pattern!r}")
    if bad:
        fails.append(f"{name}: CRC error in {bad}")
    for n in names:
        if n.startswith("/") or ".." in n.split("/") or "\\" in n or re.match(r"^[A-Za-z]:", n) or not n.startswith(name + "/"):
            fails.append(f"{name}: unsafe member path {n}")
    if len(names) != len(entries):
        fails.append(f"{name}: {len(names)} members vs {len(entries)} expected")
    print(f"{name}.zip: {len(names)} files, {os.path.getsize(zpath)} bytes, sha256 {sha(zpath)[:16]}..., test "
          f"{'PASS' if not [f for f in fails if f.startswith(name)] else 'FAIL'}")

lines = []
for sub in ("packages", "fabrication", "assembly", "3d"):
    for f in listdir(sub):
        lines.append(f"{sha(f)}  {sub}/{os.path.basename(f)}\n")
open(os.path.join(sum_dir, "SHA256SUMS.txt"), "w", newline="\n").write("".join(lines))
print(f"checksums/SHA256SUMS.txt: {len(lines)} entries")
for f in fails:
    print("FAIL:", f)
print("RESULT:", "PASS" if not fails else "FAIL")
sys.exit(1 if fails else 0)
