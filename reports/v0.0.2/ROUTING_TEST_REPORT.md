# Routing and Copper Zone Report — V0.0.2

## Before routing
`get_ratsnest` reported 3 nets and 3 airwires, totalling 50.15 mm:
+5V J1.1–R1.1 (9.72 mm), LED_A R1.2–D1.2 (11.04 mm), GND J1.2–D1.1 (29.40 mm).

## Tracks (route_pad_to_pad)
| Net | From → To | Layer | Width | Length | Source |
|---|---|---|---|---|---|
| +5V | J1.1 → R1.1 | F.Cu | 0.5 mm | 9.717 mm | query_traces |
| LED_A | R1.2 → D1.2 (A) | F.Cu | 0.5 mm | 11.037 mm | query_traces |
| GND | D1.1 (K) → J1.2 | B.Cu | 0.5 mm | 29.400 mm | query_traces |

No vias. Every pad is THT, so a B.Cu track reaches the pads directly.

Tool behaviour: `route_pad_to_pad` draws **one straight segment** between pad centres and
detects the net from the pad. It does **not** avoid obstacles and takes no waypoints.
Placement was chosen so that every straight path was clear. Collision-free routing was then
confirmed by DRC, not assumed. For denser boards, the waypoint tool (`route_trace`, not tested
here) or an autorouter is needed.

Width: 0.5 mm carries about 6 mA with negligible temperature rise. This is a design choice
(CALCULATED current, see `calculations/v0.0.2/`), not an IPC-2152 sizing.

## Copper zone
| Item | Value |
|---|---|
| Tool | `add_copper_pour` (layer B.Cu, net GND, clearance 0.3 mm) |
| Outline | board outline (default) |
| Fill | `refill_zones`: 1 zone, `isFilled true`, filled area 1341.4 mm² (`query_zones`) |
| Purpose | Exercise the zone workflow. A low-impedance return. Not electrically necessary at 6 mA |
| Pad connection | GND pads thermal-relieved (visible in the 2D view). +5V/LED_A pads cleared |

`refill_zones` carries a server warning about SWIG segfault risk. It ran twice without crashing,
but each fill caused the save desynchronisation D-1, so a reload was needed.

## Connectivity verification
| Check | Result |
|---|---|
| MCP `run_drc`: unconnected items | 0 |
| `kicad-cli pcb drc --refill-zones`: unconnected items | 0 |
| Gerber X2 `TO.N` net attributes on F.Cu / B.Cu | +5V, GND, LED_A only |
| `get_nets_list` after reload | 3 nets, 1 track each, 0 vias |

**No airwires remain and DRC is clean.** That shows the copper matches the netlist. It does
**not** show that the circuit works physically, which is NOT TESTED.
