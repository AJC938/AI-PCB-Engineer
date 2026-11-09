# Contributing

Thank you for your interest. Issues and pull requests are welcome, especially **physical test results**.

## Reporting a problem
Open an issue with the board revision (silkscreen "REV A"), what you did, what you expected and what you measured.
Photos and measurements (with the instrument used) help a lot.

## Contributing test results
The design has not been physically tested by the maintainers. If you build one:
1. Follow [docs/validation/PHYSICAL_VALIDATION_STATUS.md](docs/validation/PHYSICAL_VALIDATION_STATUS.md).
2. Put raw evidence (CSV, photos, scope captures) in `testing/<version>/` and describe the setup.
3. Update the status table only for tests with recorded evidence.

## Changing the design
- Use **KiCad 10.0.x**. Do not edit a file while it is open in KiCad.
- Any electrical or layout change needs a **new board revision** (Rev B, …). Never overwrite a released revision
  under `manufacturing/`.
- Record the reason and the source (datasheet page, calculation or decision) for every change, following
  [docs/ENGINEERING_RULES.md](docs/ENGINEERING_RULES.md).
- Before a pull request, run `scripts/release/build_release.sh`. ERC and DRC (with zone refill and schematic
  parity) must report 0 with no exclusions, and the package audit must pass.
- Do not change a manufacturer part number without datasheet verification and recalculation.
- Never commit secrets, personal data or machine-specific absolute paths.

## Licensing of contributions
Hardware and hardware-documentation contributions are accepted under CERN-OHL-P-2.0, and code contributions under
MIT (see [LICENSE_SCOPE.md](LICENSE_SCOPE.md)). Record every hardware modification in
[MODIFICATIONS.md](MODIFICATIONS.md) as described in
[docs/licensing/CONTRIBUTOR_NOTICES.md](docs/licensing/CONTRIBUTOR_NOTICES.md).
