# Attribution and Modification Notices

## For contributors to this repository
- Hardware and hardware-documentation contributions are accepted under **CERN-OHL-P-2.0**, and code contributions
  under **MIT**, according to [LICENSE_SCOPE.md](../../LICENSE_SCOPE.md).
- Add yourself to the copyright line of new files you create, or state your copyright in the pull request.
  `SPDX-FileCopyrightText: <year> <name>` headers are welcome in code files.
- Every change to the hardware design gets a row in [`MODIFICATIONS.md`](../../MODIFICATIONS.md) (date, author,
  description) and, for electrical or layout changes, a new board revision. Never edit or delete earlier rows.
- Do not add third-party material without recording its source and licence in
  [`THIRD_PARTY_NOTICES.md`](../../THIRD_PARTY_NOTICES.md). Material with an unknown licence must not be added.

## For people who modify and share the design elsewhere (CERN-OHL-P-2.0 §3.3)
When you convey a modified version of the hardware source:
1. Keep `NOTICE.md`, `MODIFICATIONS.md`, `LICENSE-HARDWARE` and all copyright and licence references that still apply.
2. Add a modification notice. Recommended form, in `MODIFICATIONS.md` and in the KiCad title-block comment:

   ```text
   Modified by <name or organisation> on <YYYY-MM-DD>: <brief description of the change>.
   Based on "Sensor Interface & Power Management Board" Rev A (v1.0.0), CERN-OHL-P-2.0.
   ```
3. Change the board revision label (silkscreen and title block) so that your boards cannot be confused with Rev A.
4. If you use different licence terms for your version (§3.4), still include a copy of CERN-OHL-P-2.0.

## For people who make or sell boards (§4)
Give recipients access to `NOTICE.md` (included in every manufacturing ZIP). A printed URL or an included copy is
enough. Do not present the board as endorsed by CERN or by the original authors.
