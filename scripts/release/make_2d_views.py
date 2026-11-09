"""Rasterize genuine KiCad plots into review images (no artwork is drawn by this script).

Inputs are PDFs exported by kicad-cli (see build_release.sh): the board top/bottom plots and the schematic PDF.
The board region is located from the vector drawings on the page (union of drawing rectangles), so the crop
does not depend on the drawing-sheet placement. Close-ups are cut from the same top plot using the board's
real 90 x 64 mm geometry (local mm, origin top-left, as in build/build_pcb.py).
Usage: python -I make_2d_views.py <top.pdf> <bottom.pdf> <schematic.pdf> <out_dir>
"""
import os
import sys

import pymupdf

top_pdf, bot_pdf, sch_pdf, out = sys.argv[1:5]
BOARD_W, BOARD_H = 90.0, 64.0
DPI_BOARD = 600
os.makedirs(out, exist_ok=True)


def board_rect(page):
    """Union of the plotted items, ignoring the full-page background fill written by --bg-color."""
    r = None
    pw, ph = page.rect.width, page.rect.height
    for d in page.get_drawings():
        rr = d["rect"]
        if rr.width > 0.9 * pw and rr.height > 0.9 * ph:
            continue
        r = rr if r is None else r | rr
    return r


def save_board(pdf, name, crops=None):
    page = pymupdf.open(pdf)[0]
    r = board_rect(page)
    m = 2.0 * 72 / 25.4  # 2 mm margin
    clip = pymupdf.Rect(r.x0 - m, r.y0 - m, r.x1 + m, r.y1 + m)
    zoom = DPI_BOARD / 72
    pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), clip=clip, alpha=False)
    pix.save(os.path.join(out, name))
    print(name, pix.width, "x", pix.height, "board rect pt", [round(v, 1) for v in r])
    sx, sy = r.width / BOARD_W, r.height / BOARD_H
    for cname, (x0, y0, x1, y1) in (crops or {}).items():
        c = pymupdf.Rect(r.x0 + x0 * sx, r.y0 + y0 * sy, r.x0 + x1 * sx, r.y0 + y1 * sy)
        p = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), clip=c, alpha=False)
        p.save(os.path.join(out, cname))
        print(cname, p.width, "x", p.height)


save_board(top_pdf, "pcb_top_2d.png", {
    "closeup_power_input_J1_U5_U1.png": (0.0, 0.0, 54.0, 28.0),
    "closeup_esp32_header_J2.png": (10.0, 46.0, 56.0, 64.0),
    "closeup_peripheral_headers_J3-J6.png": (62.0, 0.0, 90.0, 56.0),
})
save_board(bot_pdf, "pcb_bottom_2d.png")

sch = pymupdf.open(sch_pdf)[0]
pix = sch.get_pixmap(matrix=pymupdf.Matrix(200 / 72, 200 / 72), alpha=False)
pix.save(os.path.join(out, "schematic_overview.png"))
print("schematic_overview.png", pix.width, "x", pix.height)
# eFuse / power-entry block (schematic mm coordinates of J1..C13 area, A3 sheet)
mm = 72 / 25.4
clip = pymupdf.Rect(40 * mm, 40 * mm, 140 * mm, 116 * mm)
pix = sch.get_pixmap(matrix=pymupdf.Matrix(300 / 72, 300 / 72), clip=clip, alpha=False)
pix.save(os.path.join(out, "schematic_power_entry_efuse.png"))
print("schematic_power_entry_efuse.png", pix.width, "x", pix.height)
