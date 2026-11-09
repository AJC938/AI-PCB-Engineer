"""Controlled non-MCP edit: solid (full) pad connection for the +3V3_P thermal zone, then refill and save.

Why: the LDO (TLV1117LV, SOT-223) tab must join its thermal copper without thermal-relief spokes
(POWER_AND_THERMAL_REVIEW). MCP add_zone is not implemented in the SWIG backend (D-23) and
add_copper_pour has no pad-connection parameter, so this one property is set with KiCad's own API.
Only the +3V3_P zone's pad-connection mode changes; all zones are refilled with KiCad's ZONE_FILLER.
Usage: python -I set_zone_connection.py <board.kicad_pcb>   (KiCad's bundled Python)
"""
import sys

import pcbnew

path = sys.argv[1]
board = pcbnew.LoadBoard(path)
zones = [z for z in board.Zones() if z.GetNetname() == "+3V3_P"]
assert len(zones) == 1, len(zones)
zones[0].SetPadConnection(pcbnew.ZONE_CONNECTION_FULL)
filler = pcbnew.ZONE_FILLER(board)
filler.Fill(board.Zones())
pcbnew.SaveBoard(path, board)
for z in pcbnew.LoadBoard(path).Zones():
    print(z.GetNetname(), z.GetLayerName(), "connection", z.GetPadConnection(), "filled", z.IsFilled(),
          "area mm2", round(z.GetFilledArea() / 1e12, 1))
