# V0.0.3 Final Report — MCP Advanced Capability Evaluation

Date: 2026-11-08 · Branch: `evaluation/v0.0.3-mcp-capabilities` (from `v0.0.2` / `0195a8d`) ·
KiCad 10.0.8 · KiCAD-MCP-Server v2.8.3 (`1d204fe3`) · kicad-python 0.8.0 · Node 24.22.2

## Executive summary
| Area | Result |
|---|---|
| SWIG baseline (12 operations) | **12/12 PASS**, independently verified (pcbnew readback, CLI DRC) |
| IPC backend (same 12 operations) | **Tested, not usable.** Connects and saves, but all footprint reads fail (some silently) because kicad-python 0.8.0 cannot decode KiCad 10.0.8 footprint data. Rotate, edit and read-back fail. Zone refill over IPC works and avoids the SWIG desync |
| Custom symbol | **PASS**, fully native MCP. Created from scratch, registered (project scope), placed, wired, ERC 0, netlist verified, persistent |
| Custom footprint | **PASS with limitations**, native MCP. Created, pad-edited, 3D model attached, placed, DRC 0, persistent. Rectangle-only graphics, no type attribute |
| GUI driver | **Not usable on Windows.** Installer targets the wrong folder. Clicks are not processed. Screenshots capture other applications. Read-only UI introspection works after a manual workaround |
| SWIG vs IPC | SWIG recommended. IPC re-test deferred until a compatible kicad-python exists |

**Status: COMPLETE as an evaluation, with one BLOCKED sub-test** (GUI DRC dialog not run on the
user's active desktop) and several NOT TESTED items listed below. Release candidate tag: `v0.0.3-rc1`.

## Environment and test conditions
- All tests ran in `hardware/sandbox/v0.0.3/{swig,ipc,custom_symbols,custom_footprints,gui_driver}` (gitignored).
  The SWIG, IPC and GUI inputs are byte-identical copies of the V0.0.2 evidence board.
- **MCP client:** the Claude Code in-session `kicad` connection was disconnected in this session. Every
  MCP call went through `ai/workflows/mcp_harness.py`, which launches the same server binary with the same
  `.mcp.json` configuration over the same protocol, with per-process overrides (`KICAD_BACKEND`,
  `KICAD_MCP_TOOLBOXES`). `.mcp.json` was not changed.
- **Global changes (user-approved, temporary, reverted):**
  - KiCad `api.enable_server` toggled for the IPC test.
  - GUI-driver helper installed for the GUI test.
  - The KiCad config folder was verified **byte-identical** to the pre-test backup afterwards (18-file sha256 manifest).
  - The user closed their own KiCad session before the tests. No user process was terminated.
- No dependency was installed, upgraded or downgraded. Nothing was pushed, ordered or uploaded.

## Defects and limitations found (continuing V0.0.2 numbering)
| ID | Area | Finding | Severity |
|---|---|---|---|
| D-10 | run_drc | Does not refill zones. A stale fill produced 6 false errors after a placement (0 after refill) | Medium |
| D-11 | register_*_library | Writes **absolute, user-specific URIs** into project lib tables | Medium (portability, privacy) |
| D-12 | library lookup | `get_symbol_info` / `get_footprint_info` fail in the same session right after registration. They work in a fresh process | Low |
| D-13 | search_symbols | 30 s timeout with `projectPath` | Low |
| D-14 | create_footprint | One rectangle per layer for silk, fab and courtyard. No circles, arcs or lines. No `attr` (type = unspecified) | Medium |
| D-15 | create_symbol | No pin-name hide/offset (text overlaps the body). Schema description of pin angle is misleading | Low |
| D-16 | IPC / kipy | `kiapi.board.types.ReferencePoint` cannot be decoded by kicad-python 0.8.0 with KiCad 10.0.8, so footprint enumeration fails. MCP returns `success:true, 0 components` | **High (silent wrong data)** |
| D-17 | IPC | rotate, get_properties and read-back cannot find components. `edit_component` falls back to a SWIG board copy without the IPC changes | High |
| D-18 | IPC place_component | Placed footprint loses its library nickname (`R_Axial…` instead of `Resistor_THT:R_Axial…`) | Medium |
| D-19 | IPC reads | Numeric layer IDs. Trace `uuid` is a raw protobuf string. `netCode: 0` | Medium |
| D-20 | install_gui_driver | Windows target `%APPDATA%\kicad\<ver>\3rdparty\plugins` is not on KiCad 10's plugin search path | High (feature dead on arrival) |
| D-21 | kicad_gui_click | `processed:false`. No effect (Save did not write) | High |
| D-22 | GUI screenshots | Capture a screen rectangle, including any foreground application | **High (privacy)** |

V0.0.2 defects D-1 to D-9 remain. D-1 recurred after `sync_schematic_to_board` in the footprint test.

## Not tested
- A newer kicad-python (no upgrades allowed).
- GUI-driver `kicad_run_drc` (BLOCKED, modal dialog), `kicad_run_action_plugin`, `kicad_reload_and_open_plugin`.
- Opening a project through the GUI driver.
- Pcbnew-script footprint creation as an alternative path.
- Repeated latency runs (n = 1).
- Physical anything.

## Engineering recommendation
Adopt the **SWIG + kicad-cli** architecture for V0.1.0. Use native MCP for custom symbols and footprints,
with the post-edit and URI rules in NEXT_STAGE_RECOMMENDATION.md. Keep IPC disabled until a
kicad-python release decodes KiCad 10 board types (re-test starting with a direct kipy probe). Do not
use the GUI driver. None of these capabilities is production-ready on the strength of this evaluation.
They are suitable for supervised, verified use in the sandbox and for the first real design.

## Reports
`IPC_BACKEND_EVALUATION.md` · `CUSTOM_SYMBOL_EVALUATION.md` · `CUSTOM_FOOTPRINT_EVALUATION.md` ·
`GUI_DRIVER_EVALUATION.md` · `SWIG_VS_IPC_COMPARISON.md` · `MCP_CAPABILITY_MATRIX.md` · `TEST_LOG.md` ·
`EVIDENCE_INDEX.md` · `NEXT_STAGE_RECOMMENDATION.md`
