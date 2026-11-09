"""Footprint geometry report (pads, drills, courtyard, body) for every footprint used by the design.

Usage: python -I fp_report.py <kicad_footprints_dir> [out.json]
Reads build_schematic.PARTS; resolves the project-local library from the project folder.
Used by FOOTPRINT_VERIFICATION.md (comparison against datasheet land patterns) and the placement script.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_schematic as B  # noqa: E402


def sexp_blocks(s, head):
    out, i = [], 0
    while True:
        i = s.find("(" + head, i)
        if i < 0:
            return out
        d, j = 0, i
        while True:
            if s[j] == "(":
                d += 1
            elif s[j] == ")":
                d -= 1
                if d == 0:
                    break
            j += 1
        out.append(s[i:j + 1])
        i = j + 1


def parse(path):
    s = open(path, encoding="utf-8").read()
    pads = []
    for blk in sexp_blocks(s, "pad "):
        m = re.match(r'\(pad "([^"]*)" (\w+) (\w+)', blk)
        at = re.search(r"\(at (-?[\d.]+) (-?[\d.]+)(?: (-?[\d.]+))?\)", blk)
        size = re.search(r"\(size (-?[\d.]+) (-?[\d.]+)\)", blk)
        drill = re.search(r"\(drill (?:oval )?([\d.]+)(?: ([\d.]+))?", blk)
        layers = re.search(r"\(layers ([^)]*)\)", blk).group(1)
        pads.append(dict(num=m.group(1), type=m.group(2), shape=m.group(3), x=float(at.group(1)), y=float(at.group(2)),
                         w=float(size.group(1)), h=float(size.group(2)),
                         drill=float(drill.group(1)) if drill else None, layers=layers))
    crt = []
    for blk in sexp_blocks(s, "fp_"):
        if '"F.CrtYd"' in blk or '"B.CrtYd"' in blk:
            crt += [(float(a), float(b)) for a, b in re.findall(r"\((?:start|end|xy|center) (-?[\d.]+) (-?[\d.]+)\)", blk)]
    attr = re.search(r"\(attr ([^)]*)\)", s)
    model = re.search(r'\(model "([^"]+)"', s)
    return dict(pads=pads, crtyd=[min(p[0] for p in crt), min(p[1] for p in crt), max(p[0] for p in crt),
                                  max(p[1] for p in crt)] if crt else None,
                attr=attr.group(1) if attr else None, model=model.group(1) if model else None)


def main():
    fp_dir = sys.argv[1]
    rep = {}
    for ref, p in B.PARTS.items():
        lib, name = p["fp"].split(":", 1)
        base = B.PROJ_DIR if lib == B.NAME else fp_dir
        rep[ref] = dict(fp=p["fp"], mpn=p["mpn"], **parse(os.path.join(base, lib + ".pretty", name + ".kicad_mod")))
    if len(sys.argv) > 2:
        json.dump(rep, open(sys.argv[2], "w"), indent=1)
    seen = set()
    for ref, r in rep.items():
        if r["fp"] in seen:
            continue
        seen.add(r["fp"])
        cy = r["crtyd"]
        print(f"{r['fp']}  [{r['mpn']}]  attr={r['attr']}  crtyd={cy[2]-cy[0]:.2f}x{cy[3]-cy[1]:.2f}  model={'yes' if r['model'] else 'NO'}")
        sig = {}
        for pd in r["pads"]:
            k = (pd["shape"], pd["w"], pd["h"], pd["drill"])
            sig.setdefault(k, []).append(pd["num"])
        for (shape, w, h, dr), nums in sig.items():
            print(f"    pads {','.join(n or '-' for n in nums[:8])}{'...' if len(nums) > 8 else ''}: {shape} {w}x{h}"
                  + (f" drill {dr}" if dr else ""))
        xs = sorted({pd["x"] for pd in r["pads"] if pd["num"]}); ys = sorted({pd["y"] for pd in r["pads"] if pd["num"]})
        if len(xs) > 1 or len(ys) > 1:
            print(f"    pad-centre spans x {xs[-1]-xs[0]:.3f} y {ys[-1]-ys[0]:.3f}")


if __name__ == "__main__":
    main()
