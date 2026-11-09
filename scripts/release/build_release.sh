#!/usr/bin/env bash
# Rebuild the V1.0.0 (Rev A) validation evidence and manufacturing outputs from the KiCad sources.
#
# Usage (from the repository root, Git Bash on Windows or any POSIX shell):
#   KICAD_CLI=/path/to/kicad-cli KICAD_PY=/path/to/kicad/python scripts/release/build_release.sh
# Defaults point at a per-user KiCad 10 install on Windows (%LOCALAPPDATA%\Programs\KiCad\10.0\bin).
# Only kicad-cli options listed by `kicad-cli <cmd> --help` (KiCad 10.0.8) are used.
# The script never writes to the KiCad design files (DRC runs with --refill-zones but WITHOUT --save-board).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
KBIN_DEFAULT="${LOCALAPPDATA:-}/Programs/KiCad/10.0/bin"
CLI="${KICAD_CLI:-$KBIN_DEFAULT/kicad-cli.exe}"
PY="${KICAD_PY:-$KBIN_DEFAULT/python.exe}"
FPDIR="${KICAD_FOOTPRINT_DIR:-$KBIN_DEFAULT/../share/kicad/footprints}"

NAME=Sensor_Interface_Power_Board
PROJ=hardware/kicad/$NAME
PCB=$PROJ/$NAME.kicad_pcb
SCH=$PROJ/$NAME.kicad_sch
REV=RevA
OUT=manufacturing/$NAME/$REV
FAB=$OUT/fabrication
ASM=$OUT/assembly
M3D=$OUT/3d
EVD=reports/v0.3.0/evidence/validation
RND=media/renders

for f in "$PROJ"/~*.lck; do
  case "$f" in *"$NAME.kicad_pcb.lck"|*"$NAME.kicad_sch.lck") echo "ABORT: $f exists (design file open in KiCad)"; exit 1;; esac
done
mkdir -p "$FAB" "$ASM" "$M3D" "$EVD" "$RND"
rm -f "$FAB"/*.g?? "$FAB"/*.gm1 "$FAB"/*.gbrjob "$FAB"/*.drl "$FAB"/*drl_map.pdf "$FAB"/*.d356

echo "== 1. ERC (all severities)"
"$CLI" sch erc --format json --severity-all --units mm -o "$EVD/erc.json" "$SCH"
"$CLI" sch erc --format report --severity-all --units mm -o "$EVD/erc.rpt" "$SCH"

echo "== 2. Netlist + independent schematic verifier"
"$CLI" sch export netlist --format kicadxml -o "$EVD/netlist.xml" "$SCH"
"$PY" -I "$PROJ/build/verify_schematic.py" "$EVD/netlist.xml" "$FPDIR" > "$EVD/verify_schematic.txt"

echo "== 3. DRC (all severities, schematic parity): zones refilled in memory (D-10), and as stored"
"$CLI" pcb drc --format json --severity-all --schematic-parity --refill-zones --units mm -o "$EVD/drc_refilled.json" "$PCB"
"$CLI" pcb drc --format report --severity-all --schematic-parity --refill-zones --units mm -o "$EVD/drc_refilled.rpt" "$PCB"
"$CLI" pcb drc --format json --severity-all --schematic-parity --units mm -o "$EVD/drc_stored_zones.json" "$PCB"

echo "== 4. Fabrication: Gerber X2 (drill/place origin = board bottom-left), Excellon mm, drill maps, IPC-D-356"
"$CLI" pcb export gerbers -o "$FAB" --use-drill-file-origin --subtract-soldermask \
  -l F.Cu,B.Cu,F.Mask,B.Mask,F.Paste,B.Paste,F.SilkS,B.SilkS,Edge.Cuts "$PCB"
"$CLI" pcb export drill -o "$FAB/" --format excellon --drill-origin plot --excellon-units mm \
  --excellon-zeros-format decimal --excellon-separate-th --generate-map --map-format pdf "$PCB"
"$CLI" pcb export ipcd356 -o "$FAB/${NAME}_${REV}.d356" "$PCB"

echo "== 5. Assembly: CPL (mm, top, place origin), BOM, drawings, schematic"
"$CLI" pcb export pos -o "$ASM/${NAME}_${REV}_CPL.csv" --format csv --units mm --side front --use-drill-file-origin "$PCB"
"$PY" -I "$PROJ/build/make_bom.py" "$EVD/netlist.xml" "$PCB" "$ASM/${NAME}_${REV}_BOM.csv"
"$PY" -I scripts/release/enrich_bom.py "$ASM/${NAME}_${REV}_BOM.csv"
"$CLI" pcb export pdf -o "$ASM/${NAME}_${REV}_assembly_drawing_top.pdf" --mode-single --ibt --scale 1.8 --ev \
  --black-and-white -l F.Fab,F.SilkS,Edge.Cuts "$PCB"
"$CLI" pcb export pdf -o "$ASM/${NAME}_${REV}_assembly_drawing_bottom.pdf" --mode-single --ibt --scale 1.8 -m \
  --black-and-white -l B.Fab,B.SilkS,Edge.Cuts "$PCB"
"$CLI" pcb export pdf -o "$ASM/${NAME}_${REV}_layers.pdf" --mode-multipage --ibt \
  -l F.Cu,B.Cu,F.SilkS,F.Mask,B.Mask,F.Fab,Edge.Cuts --cl Edge.Cuts "$PCB"
"$CLI" sch export pdf -o "$ASM/${NAME}_${REV}_schematic.pdf" "$SCH"

echo "== 6. STEP (place origin) and renders"
"$CLI" pcb export step -f --drill-origin -o "$M3D/${NAME}_${REV}.step" "$PCB"
R() { "$CLI" pcb render -o "$RND/$1" --width 2400 --height 1600 --quality high --background opaque "${@:2}" "$PCB"; }
R 3d_top.png --side top
R 3d_bottom.png --side bottom
R 3d_isometric.png --side top --perspective --rotate '-45,0,45' --zoom 0.85
R 3d_isometric_rear.png --side top --perspective --rotate '-45,0,-135' --zoom 0.85
TMPV="$(mktemp -d)"
"$CLI" pcb export pdf -o "$TMPV/top.pdf" --mode-single --bg-color '#ffffff' \
  -l F.Cu,F.Mask,F.SilkS,Edge.Cuts "$PCB"
"$CLI" pcb export pdf -o "$TMPV/bottom.pdf" --mode-single -m --bg-color '#ffffff' \
  -l B.Cu,B.Mask,B.SilkS,Edge.Cuts "$PCB"
"$PY" -I scripts/release/make_2d_views.py "$TMPV/top.pdf" "$TMPV/bottom.pdf" "$ASM/${NAME}_${REV}_schematic.pdf" "$RND"
rm -rf "$TMPV"

echo "== 6b. Remove machine-specific paths from text evidence"
"$PY" -I scripts/release/sanitize_paths.py "$ROOT" "$EVD"/*.json "$EVD"/*.rpt "$EVD"/netlist.xml

echo "== 7. Independent audit of the generated package"
"$PY" -I scripts/release/audit_release.py "$OUT" "$PCB" | tee "$EVD/release_audit.txt"
echo "DONE"
