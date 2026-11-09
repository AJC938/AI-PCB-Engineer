"""Controlled non-MCP edit: PCB title block (title, revision, date, company, comments).

Why: no MCP tool writes the board title block; the revision appears in the drawing PDFs and in the Gerber X2
%TF.ProjectId attribute, so fabrication files carry the revision. Only the title block is changed.
Usage: python -I set_pcb_title.py <board.kicad_pcb> <rev> <date>   (KiCad's bundled Python)
"""
import sys

import pcbnew

path, rev, date = sys.argv[1:4]
board = pcbnew.LoadBoard(path)
tb = board.GetTitleBlock()
tb.SetTitle("Sensor Interface & Power Management Board for ESP32")
tb.SetRevision(rev)
tb.SetDate(date)
tb.SetCompany("AI-PCB-Engineer")
tb.SetComment(0, "2 layers FR-4 1.6 mm, 1 oz Cu, ENIG preferred, green mask, white silk")
tb.SetComment(1, "Architecture B: ESP32 DevKit on its own USB; board powers peripherals")
board.SetTitleBlock(tb)
pcbnew.SaveBoard(path, board)
t = pcbnew.LoadBoard(path).GetTitleBlock()
print("title block:", t.GetTitle(), "| rev", t.GetRevision(), "|", t.GetDate())
