"""V0.2.0 silkscreen: legal reference positions + connector pin-map legend (written through MCP).

Reads the saved board with pcbnew (read-only), measures the real text boxes, and for every footprint picks
the first candidate position around its courtyard whose box stays clear of: pad/mask openings (+0.15 mm),
other footprints' silkscreen (+0.15 mm), already placed texts, holes, fiducial mask openings and the board
edge. Mounting-hole and fiducial references are hidden (mechanical items). The legend gives every connector
pin unambiguously (J2 GPIO map, J3-J6 pin order, solder jumpers, power-sequencing rule R-31).
Output: MCP steps (move_footprint_text, add_board_text) in <out_dir>/p4_silk.json and a plan JSON.
Usage: python -I place_silk.py <out_dir>   (KiCad's bundled Python)
"""
import json
import os
import sys

import pcbnew

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_pcb as L  # noqa: E402

mm, FM = pcbnew.ToMM, pcbnew.FromMM
OX, OY = L.ORIGIN
TXT_H, TXT_T = 1.0, 0.15          # >= 0.8 mm height / 0.15 mm stroke (strictest shortlisted fab: PCBWay)
CLR_SILK, CLR_MASK, EDGE = 0.15, 0.15, 0.5

board = pcbnew.LoadBoard(L.PCB)


def bb_local(bb, grow=0.0):
    return (mm(bb.GetX()) - OX - grow, mm(bb.GetY()) - OY - grow,
            mm(bb.GetRight()) - OX + grow, mm(bb.GetBottom()) - OY + grow)


obst = []                                   # (box, owner, kind)
for fp in board.GetFootprints():
    ref = fp.GetReference()
    for pad in fp.Pads():
        if pad.IsOnLayer(pcbnew.F_Mask) or pad.IsOnLayer(pcbnew.F_Cu):
            g = 1.0 if ref.startswith("FID") else CLR_MASK
            obst.append((bb_local(pad.GetBoundingBox(), g), ref, "pad"))
        if pad.GetDrillSize().x:
            obst.append((bb_local(pad.GetBoundingBox(), 0.4), ref, "hole"))
    for item in fp.GraphicalItems():
        if item.GetLayer() == pcbnew.F_SilkS and item.GetClass() != "PCB_FIELD":
            obst.append((bb_local(item.GetBoundingBox(), CLR_SILK), ref, "silk"))


def text_box(text, cx, cy, rot=0):
    t = pcbnew.PCB_TEXT(board)
    t.SetText(text)
    t.SetTextSize(pcbnew.VECTOR2I(FM(TXT_H), FM(TXT_H)))
    t.SetTextThickness(FM(TXT_T))
    t.SetTextAngleDegrees(rot)
    t.SetPosition(pcbnew.VECTOR2I(FM(OX + cx), FM(OY + cy)))
    return bb_local(t.GetBoundingBox())


def hit(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def legal(box, owner=None):
    if box[0] < EDGE or box[1] < EDGE or box[2] > L.W - EDGE or box[3] > L.H - EDGE:
        return False
    for ob, own, kind in obst:
        if hit(box, ob):
            return False
    return True


placed = []
steps = [{"label": "open", "name": "open_project",
          "arguments": {"filename": os.path.join(L.B.PROJ_DIR, L.B.NAME + ".kicad_pro")}}]
plan = {"refs": {}, "texts": [], "hidden": [], "unplaced": []}

fps = sorted(board.GetFootprints(), key=lambda f: -mm(f.GetBoundingBox().GetWidth()) * mm(f.GetBoundingBox().GetHeight()))
for fp in fps:
    ref = fp.GetReference()
    if ref.startswith(("H", "FID")):
        steps.append({"label": f"hide_{ref}", "name": "move_footprint_text", "arguments": {
            "reference": ref, "field": "Reference", "visible": False}})
        plan["hidden"].append(ref)
        continue
    cy = fp.GetCourtyard(pcbnew.F_CrtYd).BBox()
    x0, y0, x1, y1 = bb_local(cy)
    cx, cyy = (x0 + x1) / 2, (y0 + y1) / 2
    w0 = text_box(ref, 0, 0)
    tw, th = w0[2] - w0[0], w0[3] - w0[1]
    cands = []
    for dx in (0, -1.0, 1.0, -2.0, 2.0):
        cands += [(cx + dx, y0 - th / 2 - 0.05, 0), (cx + dx, y1 + th / 2 + 0.05, 0)]
    for dy in (0, -1.0, 1.0, -2.0, 2.0):
        cands += [(x0 - tw / 2 - 0.05, cyy + dy, 0), (x1 + tw / 2 + 0.05, cyy + dy, 0)]
    for dy in (0, -1.5, 1.5):
        cands += [(x0 - th / 2 - 0.05, cyy + dy, 90), (x1 + th / 2 + 0.05, cyy + dy, 90)]
    for gap in (0.6, 1.2, 2.0):
        cands += [(cx, y0 - th / 2 - gap, 0), (cx, y1 + th / 2 + gap, 0)]
    own_silk = [ob for ob in obst if ob[1] == ref]
    choice = None
    for (x, y, r) in cands:
        box = text_box(ref, x, y, r)
        if legal(box):
            choice = (x, y, r, box)
            break
    if not choice:
        plan["unplaced"].append(ref)
        steps.append({"label": f"hide_{ref}", "name": "move_footprint_text", "arguments": {
            "reference": ref, "field": "Reference", "visible": False}})
        continue
    x, y, r, box = choice
    obst.append((tuple(v for v in box), ref, "text"))
    plan["refs"][ref] = dict(x=round(x, 3), y=round(y, 3), rot=r)
    steps.append({"label": f"ref_{ref}", "name": "move_footprint_text", "arguments": {
        "reference": ref, "field": "Reference", "x": round(OX + x, 3), "y": round(OY + y, 3), "unit": "mm",
        "rotation": r, "layer": "F.SilkS", "visible": True}})

LEGEND = [
    "SENSOR IF + PWR BOARD  REV 0.2.0",
    "J1: 1=+5V IN  2=GND  (5V +-5%)",
    "J2 ESP32: 1=3V3  2=GND",
    " 3=IO26 TRIG   4=IO34 ECHO",
    " 5=IO21 SDA    6=IO22 SCL",
    " 7=IO17 TX     8=IO16 RX",
    " 9=IO32  10=IO33  11,12=GND",
    "J3 SONAR: 1=+5V 2=TRIG 3=ECHO 4=GND",
    "J4 UART: 1=GND 2=VCC 3=TX 4=RX",
    "J5 I2C: 1=GND 2=3V3 3=SDA 4=SCL",
    "J6 GP: 1=GND 2=3V3 3=IO32 4=IO33",
    "JP1 UART VCC: 1-2=3V3  2-3=5V",
    "JP2 I2C PULL-UP: CUT=OFF",
    "POWER THIS BOARD BEFORE/WITH ESP32",
]
x_left, y = 1.2, 27.4
for line in LEGEND:
    w = text_box(line, 0, 0)
    tw = w[2] - w[0]
    xl = None
    for attempt in range(8):
        for xc in (x_left, 14.0):
            box = text_box(line, xc + tw / 2, y)
            if legal(box):
                xl = xc
                break
        if xl is not None:
            break
        y += 0.5
    if xl is None:
        plan["unplaced"].append(line)
        continue
    obst.append((box, "legend", "text"))
    plan["texts"].append(dict(text=line, x=round(xl + tw / 2, 3), y=round(y, 3)))
    steps.append({"label": f"txt{len(plan['texts'])}", "name": "add_board_text", "arguments": {
        "text": line, "position": {"x": round(OX + xl + tw / 2, 3), "y": round(OY + y, 3), "unit": "mm"},
        "layer": "F.SilkS", "size": TXT_H, "thickness": TXT_T, "rotation": 0}})
    y += 1.75

# short functional labels next to parts (only where legal)
EXTRA = [("+5V", "J1", 1), ("GND", "J1", 2)]
for text, ref, pin in EXTRA:
    fp = board.FindFootprintByReference(ref)
    pad = [p for p in fp.Pads() if p.GetNumber() == str(pin)][0]
    px, py = mm(pad.GetPosition().x) - OX, mm(pad.GetPosition().y) - OY
    for dx in (7.5, 8.5, 9.5):
        box = text_box(text, px + dx, py)
        if legal(box):
            obst.append((box, "label", "text"))
            plan["texts"].append(dict(text=text, x=round(px + dx, 3), y=round(py, 3)))
            steps.append({"label": f"lbl_{text}", "name": "add_board_text", "arguments": {
                "text": text, "position": {"x": round(OX + px + dx, 3), "y": round(OY + py, 3), "unit": "mm"},
                "layer": "F.SilkS", "size": TXT_H, "thickness": TXT_T, "rotation": 0}})
            break

steps.append({"label": "save", "name": "save_project", "arguments": {}})
out = sys.argv[1]
os.makedirs(out, exist_ok=True)
json.dump(steps, open(os.path.join(out, "p4_silk.json"), "w"), indent=1)
json.dump(plan, open(os.path.join(out, "silk_plan.json"), "w"), indent=1)
print(f"refs placed {len(plan['refs'])}, hidden {plan['hidden']}, legend/labels {len(plan['texts'])}, "
      f"unplaced {plan['unplaced']}, steps {len(steps)}")
