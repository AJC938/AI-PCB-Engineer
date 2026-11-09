"""Workaround for MCP defect D-24 (V0.2.0): sync_schematic_to_board leaves pads of no-connect pins without a net.

KiCad's own "Update PCB from Schematic" gives each such pad its single-pin net "unconnected-(REF-PIN-PadN)";
without it, DRC schematic parity reports net_conflict for every NC pin. This script copies exactly those
nets from the kicad-cli XML netlist onto the matching pads (nothing else is touched) and saves the board.
Usage: python -I fix_nc_pad_nets.py <board.kicad_pcb> <netlist.xml>   (KiCad's bundled Python)
"""
import sys
import xml.etree.ElementTree as ET

import pcbnew

board_path, net_xml = sys.argv[1:3]
want = {}
for n in ET.parse(net_xml).getroot().iter("net"):
    name = n.get("name")
    if name.startswith("unconnected-"):
        nodes = list(n.iter("node"))
        assert len(nodes) == 1, name
        want[(nodes[0].get("ref"), nodes[0].get("pin"))] = name

board = pcbnew.LoadBoard(board_path)
done = 0
for fp in board.GetFootprints():
    for pad in fp.Pads():
        key = (fp.GetReference(), pad.GetNumber())
        if key in want:
            assert pad.GetNetname() in ("", want[key]), (key, pad.GetNetname())
            if pad.GetNetname() != want[key]:
                net = board.FindNet(want[key])
                if net is None:
                    net = pcbnew.NETINFO_ITEM(board, want[key])
                    board.Add(net)
                pad.SetNet(net)
                done += 1
                print(f"{key[0]}.{key[1]} -> {want[key]}")
assert done + sum(1 for fp in board.GetFootprints() for p in fp.Pads()
                  if (fp.GetReference(), p.GetNumber()) in want and p.GetNetname() == want[(fp.GetReference(), p.GetNumber())]) >= len(want)
if done:
    pcbnew.SaveBoard(board_path, board)
print(f"NC pad nets set: {done} (expected {len(want)})")
