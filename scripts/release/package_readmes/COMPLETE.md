# Sensor Interface PCB — Rev A — Complete Manufacturing Package

Everything needed to request a quotation for **bare-board fabrication + full turnkey assembly (SMT + THT)**.
Release v1.0.0, board revision **A**. **Fabrication-ready digital design — NOT yet fabricated, assembled or
physically tested.**

| Folder | Content |
|---|---|
| `fabrication/` | Gerber X2 + job file, Excellon PTH/NPTH + drill maps, IPC-D-356, FABRICATION_NOTES.md |
| `assembly/` | BOM, CPL, assembly drawings, schematic PDF, layer plots, ASSEMBLY_NOTES.md, CONNECTOR_PINOUT.md |
| `3d/` | STEP model (mechanical review aid built from KiCad library models) |
| `MANIFEST-SHA256.txt` | SHA-256 of every file in this package |

Board: 90.0 × 64.0 mm, 2 layers, FR-4 1.6 mm, 1 oz, ENIG preferred. Assembly: top side only, 44 SMT + 8 THT, lead-free.
The quote must confirm: THT soldering method, availability of every exact MPN (especially TPS26600PWPR),
CPL rotation convention, finish, price, lead time and shipping. No substitution without written approval.

Licence: CERN-OHL-P-2.0 (LICENSE-HARDWARE.txt in this package). Copyright, acknowledgements, third-party
attribution, disclaimer and design limitations: NOTICE.md. Commercial manufacturing is permitted; recipients of
boards must have access to NOTICE.md (CERN-OHL-P §4).
