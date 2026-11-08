"""Independent board reader (KiCad pcbnew API, not MCP): print footprints, nets, tracks, zones.

Usage: "%LOCALAPPDATA%\\Programs\\KiCad\\10.0\\bin\\python.exe" -I read_board_state.py <board.kicad_pcb> [REF ...]
"""
import sys

import pcbnew

b = pcbnew.LoadBoard(sys.argv[1])
refs = set(sys.argv[2:])
mm = pcbnew.ToMM
print("footprints:", len(b.GetFootprints()), "| tracks:", len(b.GetTracks()), "| zones:", b.GetAreaCount(),
      "| nets:", sorted(str(n) for n in b.GetNetsByName().keys() if str(n)))
for fp in b.GetFootprints():
    if refs and fp.GetReference() not in refs:
        continue
    p = fp.GetPosition()
    pads = [(pd.GetNumber(), round(mm(pd.GetPosition().x), 3), round(mm(pd.GetPosition().y), 3), pd.GetNetname())
            for pd in fp.Pads()]
    print(f"{fp.GetReference():4} {fp.GetValue():10} {fp.GetFPIDAsString():60} at ({mm(p.x):.3f},{mm(p.y):.3f}) "
          f"rot {fp.GetOrientationDegrees():.1f} layer {fp.GetLayerName()} pads {pads}")
for i in range(b.GetAreaCount()):
    z = b.GetArea(i)
    layers = [b.GetLayerName(l) for l in z.GetLayerSet().Seq()]
    print("zone", z.GetNetname(), layers, "filled:", z.IsFilled())
