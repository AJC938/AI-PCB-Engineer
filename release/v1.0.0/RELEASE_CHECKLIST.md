# Release Checklist — v1.0.0 (Rev A)

Legend: ✅ done and verified · ❌ not done. Status: **DIGITALLY VALIDATED — NOT FABRICATED OR PHYSICALLY TESTED.**

## A. Engineering and package criteria
| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | Final electrical audit | ✅ | `reports/v0.3.0/FINAL_ENGINEERING_AUDIT.md` |
| 2 | Protection limitations classified | ✅ L-1…L-7 | same, §9 |
| 3 | Connector interfaces documented | ✅ | `docs/pinout/CONNECTION_GUIDE.md` |
| 4 | Footprints and mechanics reviewed | ✅ | audit §6 |
| 5 | Gerber/drill verified | ✅ 19/19 | `reports/v1.0.0/evidence/release_audit.txt` |
| 6 | BOM/CPL verified | ✅ | same |
| 7 | ZIPs extracted and checked; checksums | ✅ | `make_packages.py` output, `sha256sum -c` |
| 8 | KiCad sources reopen independently | ✅ | clean clone ERC/DRC; fresh MCP reopen (V0.3.0) |
| 9 | ERC / DRC / parity | ✅ 0 / 0 / 0 | `reports/v1.0.0/evidence/` |
| 10 | Engineering files identical to `v1.0.0-rc1` | ✅ | `git diff v1.0.0-rc1` on design, manufacturing data, renders: empty |

## B. Licensing criteria (V1.0.0 prompt §16)
| # | Criterion | Status | Evidence |
|---|---|---|---|
| 11 | CERN-OHL-P-2.0 text exact and official | ✅ | `audit_licensing.py` L1 (SHA-256 of the OHWR text) |
| 12 | MIT text exact; holder filled | ✅ | L2 |
| 13 | Copyright attribution approved by the owner | ✅ | `reports/v1.0.0/LICENSE_AND_RELEASE_AUDIT.md` §3 |
| 14 | Hardware and software scope explicit; mixed docs classified | ✅ | `LICENSE_SCOPE.md`, `REUSE.toml`, L4/L5 |
| 15 | Third-party material audited, nothing relicensed | ✅ | `THIRD_PARTY_NOTICES.md`, L5/L7/L9 |
| 16 | README explains the licence split | ✅ | `README.md` §22 |
| 17 | Packages contain the notices | ✅ | L8 |
| 18 | Historical releases intact; `v1.0.0-rc1` untouched | ✅ | git checks in the audit report |
| 19 | No private data or machine paths | ✅ | repository scan |

## C. Tag
- [x] Local annotated tag `v1.0.0` on the final reviewed commit (never force-moved; `v1.0.0-rc1` kept).

## D. Manual GitHub publication (owner only; nothing was pushed)
1. Create the GitHub repository (no remote is configured locally) and add it: `git remote add origin <url>`.
2. Merge `release/v0.3.0-finalization` into `main` locally (fast-forward).
3. `git push origin main` and `git push origin v1.0.0` (optionally `v1.0.0-rc1` and the older tags).
4. Create a GitHub release from `v1.0.0`. Use `RELEASE_NOTES_V1.0.0.md` and attach the three ZIPs and `SHA256SUMS.txt`.
5. Check that the README renders correctly (images, Mermaid diagrams, links).

## E. After the first physical build (future)
- [ ] Tests T1–T15 with evidence in `testing/`; update `docs/validation/PHYSICAL_VALIDATION_STATUS.md`.
