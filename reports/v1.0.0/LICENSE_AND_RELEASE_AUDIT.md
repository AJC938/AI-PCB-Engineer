# Licence Finalization and Stable Release Audit — v1.0.0

Date 2026-11-09 · branch `release/v0.3.0-finalization` · base `v1.0.0-rc1` (`60714d2`, annotated tag object `c1e3ad1`)
· **DIGITALLY VALIDATED — NOT FABRICATED OR PHYSICALLY TESTED.**

## 1. Licence decision (owner-approved)
| Material | Licence | File |
|---|---|---|
| Original hardware design source and hardware documentation | `CERN-OHL-P-2.0` | `LICENSE-HARDWARE` |
| Original software and scripts | `MIT` | `LICENSE-CODE` |

## 2. Licence text verification
| Text | Source | Verification |
|---|---|---|
| CERN-OHL-P-2.0 | `https://ohwr.org/cern_ohl_p_v2.txt` → 301 → OHWR canonical file `gitlab.com/ohwr/project/cernohl/-/wikis/uploads/3eff4154d05e7a0459f3ddbf0674cae4/cern_ohl_p_v2.txt` | `LICENSE-HARDWARE` is byte-identical (SHA-256 `6e471d647db50527d0c75ee5f1a55a74012ab177c73282bef0bdc7f6562b7ded`, 199 lines). The SPDX-list copy used for the rc differs in wording, for example §3.4 "provided that You:" vs "provided that:", so the **official OHWR text** was used |
| MIT | `https://opensource.org/license/mit/` (OSI) | Body identical to the OSI text. Only the line `Copyright <YEAR> <COPYRIGHT HOLDER>` was filled in |
| CC-BY-SA-4.0 (third-party footprint) | `creativecommons.org/licenses/by-sa/4.0/legalcode.txt` | `LICENSES/CC-BY-SA-4.0.txt`, unmodified |
| KiCad-libraries-exception | SPDX license-list-data; identical to the exception in the KiCad libraries' `LICENSE.md` | `LICENSES/KiCad-libraries-exception.txt` |

The TLS certificate revocation server for ohwr.org was offline from this network. The download used curl's
`--ssl-revoke-best-effort` (the certificate chain is still validated) and followed the site's own redirect.

## 3. Copyright attribution
No project record named a copyright holder, and git author metadata was not treated as proof. The owner
explicitly approved **"AI-PCB-Engineer contributors"** (2026-11-09) for public attribution. It is used in:
- `LICENSE-CODE`, `NOTICE.md`, `MODIFICATIONS.md`, `LICENSE_SCOPE.md`, `REUSE.toml`;
- the SPDX headers of the new scripts.

No personal name or e-mail address is published.

## 4. Licence scope audit (`LICENSE_SCOPE.md`, `REUSE.toml`, `scripts/release/audit_licensing.py`)
| Result | Count |
|---|---|
| Files resolved to a licence (all committable files except the licence texts) | 404 |
| `CERN-OHL-P-2.0` | 349: KiCad design, manufacturing data and packages, renders, hardware docs, reports, calculation outputs, BOM data |
| `MIT` | 54: all `*.py`/`*.sh`, AI toolchain docs, environment records, configuration |
| `CC-BY-SA-4.0 WITH KiCad-libraries-exception` | 1: U5 project footprint (third-party derived) |

- **Mixed documents:** README, CHANGELOG, CONTRIBUTING and the V0.0.x reports were classified explicitly (§5 of the scope map).
- **Code that generates or checks the hardware:** licensed directly under MIT by the same holder, so CERN-OHL-P §3.4 is
  not needed. If it were treated as Covered Source, §3.4 would still be satisfied, because the repository always
  includes `LICENSE-HARDWARE` and §3.3 notices are kept.

## 5. Third-party audit (`THIRD_PARTY_NOTICES.md`)
| Item | Finding | Action |
|---|---|---|
| U5 project footprint | **Derived from a KiCad library footprint** (descr, `KiLib_Generator` property). Earlier drafts wrongly called it project-original | Kept under `CC-BY-SA-4.0 WITH KiCad-libraries-exception`, with attribution, change notice (`MODIFICATIONS.md`) and licence texts. **Excluded from the CERN-OHL-P grant** |
| KiCad symbols and footprints embedded in `.kicad_sch` / `.kicad_pcb`; 3D geometry in STEP and renders | Covered by the KiCad library exception (designs and generated files) | Documented. Design files remain CERN-OHL-P-2.0 |
| KiCad 3D model files | Referenced through `${KICAD10_3DMODEL_DIR}`, not included | — |
| Datasheets | 18 PDFs in the repository, **all KiCad exports** (L7). No manufacturer PDF is included | URLs and revisions kept in `datasheets/` |
| Tools: KiCad / pcbnew (GPL-3.0-or-later), PyMuPDF 2.1 (AGPL-3.0 or commercial), KiCAD-MCP-Server (MIT) | Not distributed. Imported or used at run time | Documented, with a note on combined distribution |
| Logos, product photographs | none in the repository | — |
| Unverified licences | none | — |

## 6. Manufacturing packages
All three ZIPs now include `NOTICE.md` and `LICENSE-HARDWARE.txt`, identical to the repository root (L8).
`NOTICE.md` contains:
- copyright and licence references;
- the "as is" disclaimer (§5) and the NOT TESTED status;
- design limitations;
- KiCad acknowledgement and third-party footprint notice;
- a trademark and no-patent-grant statement;
- modification-notice and §4 product-notice instructions.

It says that commercial manufacturing is permitted and that CERN does not endorse the design.

| Package | Files | SHA-256 |
|---|---|---|
| `Sensor_Interface_PCB_RevA_Fabrication.zip` | 20 | `80e270fb082e33fba018466a3b9a1c215885a0ab98d3f98470e457ab32f46033` |
| `Sensor_Interface_PCB_RevA_Assembly.zip` | 12 | `9c3c876b633df825f17ef1379bb1196cdc2a62668cd49f2bf7db18d2376fe584` |
| `Sensor_Interface_PCB_RevA_Complete_Manufacturing.zip` | 29 | `618a06f370de7f01433c91ea8d132d1203f51e3a5f4ecc199ac507ae165f138b` |

ZIP tests: CRC, extraction into a fresh directory, byte comparison, path and privacy scan: PASS.
`sha256sum -c checksums/SHA256SUMS.txt`: 28/28 OK.

## 7. Engineering integrity
| Check | Result |
|---|---|
| `git diff v1.0.0-rc1` on `hardware/kicad/`, `RevA/fabrication`, `RevA/assembly`, `RevA/3d`, `media/renders`, `manufacturing/v0.2.0` | **empty**: design, Gerber, drill, IPC-D-356, BOM, CPL, drawings and STEP are byte-identical to the candidate |
| Board revision | Rev A (title block and silkscreen) |
| ERC (all severities) | 0 |
| DRC (all severities, zones refilled, parity) | 0 violations, 0 unconnected, 0 parity |
| Netlist / power-domain verifier | PASS |
| Package audit | 19/19 PASS |
| Licence audit | 9/9 PASS |

Evidence: `reports/v1.0.0/evidence/` (erc.json, drc_refilled.json, netlist.xml, release_audit.txt,
licence_audit.txt; paths sanitized).

## 8. Historical integrity
Tags `v0.0.1-baseline`, `v0.0.2`, `v0.0.3-rc1` and `v1.0.0-rc1` are unchanged. `v1.0.0-rc1` still points to
`60714d2` (tag object `c1e3ad1`). `manufacturing/v0.2.0/` is unchanged.
`reports/v0.3.0/FINAL_V0.3.0_REPORT.md` received only a dated "superseded licence" note at the top. Its original
text is kept.
