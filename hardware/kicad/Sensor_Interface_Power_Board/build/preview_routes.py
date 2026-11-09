"""Render a quick PNG preview of pads + planned routes (before they are written through MCP).
Usage: python -I preview_routes.py <pcb_state.json> <routes.json> <out.png>"""
import json
import math
import sys

import pymupdf

st, rt, out = json.load(open(sys.argv[1])), json.load(open(sys.argv[2])), sys.argv[3]
S = 10.0
doc = pymupdf.open()
pg = doc.new_page(width=92 * S, height=66 * S)
off = 1 * S
def P(x, y): return pymupdf.Point(off + x * S, off + y * S)
pg.draw_rect(pymupdf.Rect(off, off, off + 90 * S, off + 64 * S), color=(0.8, 0.8, 0), width=1.5)
for z in rt["zones"]:
    if z["net"] != "GND":
        for x0, y0, x1, y1 in z["keepout"]:
            pg.draw_rect(pymupdf.Rect(P(x0, y0), P(x1, y1)), color=None, fill=(1, 0.9, 0.75) if z["net"] == "+3V3_P" else (0.85, 0.9, 1))
for s in rt["segments"]:
    col = (0.85, 0.1, 0.1) if s["layer"] == "F.Cu" else (0.1, 0.3, 0.9)
    pg.draw_line(P(s["x1"], s["y1"]), P(s["x2"], s["y2"]), color=col, width=max(1, s["w"] * S))
for p in st["pads"]:
    if not p["layers"]:
        continue
    a = math.radians(-p["angle"]); c, s_ = math.cos(a), math.sin(a)
    hw, hh = p["w"] / 2, p["h"] / 2
    pts = [P(p["x"] + u * c - v * s_, p["y"] + u * s_ + v * c) for u, v in ((-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh), (-hw, -hh))]
    pg.draw_polyline(pts, color=(0.2, 0.2, 0.2), fill=(0.7, 0.7, 0.7) if p["net"] else (1, 1, 1), width=0.5)
for v in rt["vias"]:
    pg.draw_circle(P(v["x"], v["y"]), 0.3 * S, color=(0, 0.5, 0), fill=(0.6, 0.9, 0.6), width=0.5)
pg.get_pixmap(dpi=90).save(out)
print("preview", out)
