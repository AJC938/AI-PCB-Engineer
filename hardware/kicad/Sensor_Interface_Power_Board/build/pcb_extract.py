"""Read the saved .kicad_pcb with KiCad's own pcbnew API (read-only) and export pad/track/zone data.

Independent of the MCP server: used to verify placement against build_pcb.P and as router input.
Usage: python -I pcb_extract.py <out.json>   (run with KiCad's bundled Python)
"""
import json
import math
import os
import sys

import pcbnew

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_pcb as L  # noqa: E402

mm = pcbnew.ToMM
board = pcbnew.LoadBoard(L.PCB)
out = {"footprints": {}, "pads": [], "tracks": [], "vias": [], "zones": [], "outline": None}
errs = []
for fp in board.GetFootprints():
    ref = fp.GetReference()
    pos = fp.GetPosition()
    x, y, r = mm(pos.x) - L.ORIGIN[0], mm(pos.y) - L.ORIGIN[1], fp.GetOrientationDegrees()
    out["footprints"][ref] = dict(x=round(x, 4), y=round(y, 4), rot=r, layer=fp.GetLayerName(),
                                  fpid=fp.GetFPIDAsString(), attrs=fp.GetAttributes())
    if ref in L.P:
        px, py, pr = L.P[ref]
        if abs(px - x) > 1e-3 or abs(py - y) > 1e-3 or (pr - r) % 360 not in (0,) and abs(((pr - r) + 180) % 360 - 180) > 0.01:
            errs.append(f"{ref}: file ({x:.3f},{y:.3f},{r}) != plan ({px},{py},{pr})")
    else:
        errs.append(f"{ref}: not in placement plan")
    for pad in fp.Pads():
        p = pad.GetPosition()
        sz = pad.GetSize(pcbnew.F_Cu) if hasattr(pad, "GetSize") else pad.GetSize()
        custom = pad.GetShape(pcbnew.F_Cu) == pcbnew.PAD_SHAPE_CUSTOM if hasattr(pcbnew, "PAD_SHAPE_CUSTOM") else False
        if custom:  # custom pads (solder jumpers): use the real copper bounding box, not the anchor size
            bb = pad.GetBoundingBox()
            sz = pcbnew.VECTOR2I(bb.GetWidth(), bb.GetHeight())
        lset = pad.GetLayerSet()
        layers = [n for n, lid in (("F.Cu", pcbnew.F_Cu), ("B.Cu", pcbnew.B_Cu)) if lset.Contains(lid)]
        drill = pad.GetDrillSize()
        out["pads"].append(dict(
            ref=ref, num=pad.GetNumber(), net=pad.GetNetname(), x=round(mm(p.x) - L.ORIGIN[0], 4),
            y=round(mm(p.y) - L.ORIGIN[1], 4), w=round(mm(sz.x), 4), h=round(mm(sz.y), 4),
            angle=0.0 if custom else pad.GetOrientationDegrees(), custom=custom,
            local_clearance=round(mm(pad.GetLocalClearance() or 0), 4) if hasattr(pad, "GetLocalClearance") else 0.0, shape=pad.ShapeType(pad.GetShape()) if hasattr(pad, "ShapeType") else str(pad.GetShape()),
            layers=layers, drill=round(mm(drill.x), 4) if drill.x else 0.0,
            npth=pad.GetAttribute() == pcbnew.PAD_ATTRIB_NPTH))
for t in board.GetTracks():
    if t.GetClass() == "PCB_VIA":
        p = t.GetPosition()
        out["vias"].append(dict(x=mm(p.x) - L.ORIGIN[0], y=mm(p.y) - L.ORIGIN[1], d=mm(t.GetWidth(pcbnew.F_Cu)) if hasattr(t, "GetWidth") else 0,
                                net=t.GetNetname()))
    else:
        s, e = t.GetStart(), t.GetEnd()
        out["tracks"].append(dict(x1=mm(s.x) - L.ORIGIN[0], y1=mm(s.y) - L.ORIGIN[1], x2=mm(e.x) - L.ORIGIN[0],
                                  y2=mm(e.y) - L.ORIGIN[1], w=mm(t.GetWidth()), layer=t.GetLayerName(), net=t.GetNetname()))
for z in board.Zones():
    out["zones"].append(dict(net=z.GetNetname(), layer=z.GetLayerName(), priority=z.GetAssignedPriority(),
                             filled_area_mm2=round(z.GetFilledArea() / 1e12, 2) if z.IsFilled() else None))
bb = board.GetBoardEdgesBoundingBox()
out["outline"] = [mm(bb.GetX()) - L.ORIGIN[0], mm(bb.GetY()) - L.ORIGIN[1], mm(bb.GetWidth()), mm(bb.GetHeight())]
ds = board.GetDesignSettings()
out["rules"] = dict(clearance=mm(ds.m_MinClearance) if hasattr(ds, "m_MinClearance") else None,
                    track_min=mm(ds.m_TrackMinWidth), via_min=mm(ds.m_ViasMinSize), hole_min=mm(ds.m_MinThroughDrill),
                    edge_clearance=mm(ds.m_CopperEdgeClearance))
json.dump(out, open(sys.argv[1], "w"), indent=1)
nets = {p["net"] for p in out["pads"] if p["net"]}
print(f"footprints {len(out['footprints'])}, pads {len(out['pads'])} ({sum(1 for p in out['pads'] if p['net'])} with net), "
      f"nets {len(nets)}, tracks {len(out['tracks'])}, vias {len(out['vias'])}, zones {len(out['zones'])}")
print("outline (local x, y, w, h):", [round(v, 3) for v in out["outline"]], "rules:", out["rules"])
print("placement vs plan:", "PASS" if not errs else "FAIL")
for e in errs:
    print("  -", e)
