"""Set the board revision label for the V1.0.0 release (Rev A). Non-electrical change (DDR-22).

Edits, by exact string match with expected counts (the script aborts without writing if any count differs):
  .kicad_pcb  title_block rev "0.2.0" -> "A", comment 3 added, silkscreen "...REV 0.2.0" -> "...REV A v1.0"
  .kicad_sch  title_block rev "0.2.0" -> "A", comment 3 added
The line ending of each file is preserved (the MCP-saved .kicad_pcb uses CRLF, the .kicad_sch uses LF).
Refuses to run if a KiCad lock file exists for the file being edited.
Usage: python -I set_release_revision.py <project_dir>
"""
import os
import sys

NL = "\n"
proj = sys.argv[1]
name = "Sensor_Interface_Power_Board"
COMMENT3 = '\t\t(comment 3 "Release v1.0.0 (Rev A) - fabrication-ready design, NOT physically tested")' + NL
EDITS = {
    name + ".kicad_pcb": [
        ('\t\t(rev "0.2.0")' + NL, '\t\t(rev "A")' + NL, 1),
        ('"SENSOR IF + PWR BOARD  REV 0.2.0"', '"SENSOR IF + PWR BOARD REV A v1.0"', 1),
        ('\t\t(comment 2 "Architecture B: ESP32 DevKit on its own USB; board powers peripherals")' + NL,
         '\t\t(comment 2 "Architecture B: ESP32 DevKit on its own USB; board powers peripherals")' + NL + COMMENT3, 1),
    ],
    name + ".kicad_sch": [
        ('\t\t(rev "0.2.0")' + NL, '\t\t(rev "A")' + NL, 1),
        ('\t\t(comment 2 "V0.2.0: eFuse power entry (DDR-17), TRIG series R15 (DDR-18)")' + NL,
         '\t\t(comment 2 "V0.2.0: eFuse power entry (DDR-17), TRIG series R15 (DDR-18)")' + NL + COMMENT3, 1),
    ],
}
plans = {}
for fn, edits in EDITS.items():
    path = os.path.join(proj, fn)
    if os.path.exists(os.path.join(proj, "~" + fn + ".lck")):
        sys.exit(f"ABORT: {fn} is open in KiCad")
    txt = open(path, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in txt else "\n"
    for old, new, n in edits:
        old, new = old.replace(NL, nl), new.replace(NL, nl)
        c = txt.count(old)
        if c != n:
            sys.exit(f"ABORT: {fn}: expected {n} x {old!r}, found {c}")
        txt = txt.replace(old, new)
    plans[path] = txt
for path, txt in plans.items():
    open(path, "w", encoding="utf-8", newline="").write(txt)
    print("updated", os.path.basename(path))
