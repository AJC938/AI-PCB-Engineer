# Licensing Guide (plain language)

This is a summary to help you. **It is not legal advice.** The binding terms are in
[LICENSE-HARDWARE](../../LICENSE-HARDWARE) (CERN-OHL-P-2.0) and [LICENSE-CODE](../../LICENSE-CODE) (MIT).
Which file is under which licence: [LICENSE_SCOPE.md](../../LICENSE_SCOPE.md).

## The short version
| You want to … | Hardware (CERN-OHL-P-2.0) | Scripts (MIT) |
|---|---|---|
| Build boards for yourself | Yes | — |
| Sell boards made from the design | Yes. Buyers must have access to the notices (§4) | — |
| Modify the design | Yes | Yes |
| Share your modified design | Yes. Keep the notices and add a modification notice (§3.3) | Yes. Keep the copyright and permission notice |
| Keep your modified design private or closed | Yes. CERN-OHL-P is permissive and does not require you to publish your changes | Yes |
| Share it under a different licence | Yes, if you meet §3.3 and include a copy of CERN-OHL-P (§3.4) | Yes (keep the MIT notice) |

CERN-OHL-P-2.0 is the **permissive** variant. Unlike CERN-OHL-S, it does **not** require modified designs or
products to be released as open source.

## Reusing the hardware
1. **Copying the source unchanged (§3.1):** keep all notices: `NOTICE.md`, `MODIFICATIONS.md`, copyright lines,
   licence references and the disclaimer.
2. **Modifying (§3.2):** you may change anything except the notices. Delete a notice only if it no longer applies
   to your version. You may add notices for your changes.
3. **Conveying your modified source (§3.3):** keep the notices and add one stating **that** you modified the design,
   **when**, and **briefly how**. Add a row to `MODIFICATIONS.md` (see [CONTRIBUTOR_NOTICES.md](CONTRIBUTOR_NOTICES.md)).
4. **Different licence terms (§3.4):** allowed, provided you comply with §3.3 and give recipients a copy of CERN-OHL-P.
5. **Making and selling products (§4):** make sure that recipients of the board can access the applicable notices.
   For example, ship or link `NOTICE.md` (it is inside every manufacturing ZIP) or print a URL to it.
6. The licence gives **no rights** to third-party patents, trademarks or products. CERN does not endorse this design.
   Do not imply that CERN or the original authors endorse your product.

## Using the software
The Python and shell scripts are MIT-licensed. You can use, copy, modify, merge, publish, distribute, sublicense
and sell them. Keep the copyright notice and the permission notice in all copies or substantial portions. The
scripts call KiCad's `pcbnew` (GPL-3.0-or-later) and PyMuPDF (AGPL-3.0 or commercial). Those tools are not part
of this project. If you distribute them, their own licences apply.

## Third-party material inside the project
- The U5 footprint in `Sensor_Interface_Power_Board.pretty` is a modified KiCad library footprint. It stays under
  **CC-BY-SA-4.0 WITH KiCad-libraries-exception**. If you redistribute it as a library footprint, keep the attribution
  and the licence, and mark your changes.
- KiCad library symbols, footprints and 3D geometry embedded in the design or generated files are covered by the
  KiCad library exception, so no extra obligations apply to the design files.
- Datasheets are not included; follow the links in `datasheets/`.

Details: [THIRD_PARTY_NOTICES.md](../../THIRD_PARTY_NOTICES.md).
