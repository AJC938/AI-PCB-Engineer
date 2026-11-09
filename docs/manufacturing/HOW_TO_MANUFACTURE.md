# How to Manufacture and Assemble the Board

> The design is fabrication-ready but **has never been manufactured**. Order a small first batch, inspect it,
> and follow the bring-up plan in [PHYSICAL_VALIDATION_STATUS.md](../validation/PHYSICAL_VALIDATION_STATUS.md)
> before relying on it.

## 1. Pick the package
All packages are in [`manufacturing/Sensor_Interface_Power_Board/RevA/packages/`](../../manufacturing/Sensor_Interface_Power_Board/RevA/packages/).
Check them against [`checksums/SHA256SUMS.txt`](../../manufacturing/Sensor_Interface_Power_Board/RevA/checksums/SHA256SUMS.txt).

| You want | Upload |
|---|---|
| Bare PCBs only | `Sensor_Interface_PCB_RevA_Fabrication.zip` |
| PCBs + full assembly (recommended) | `Sensor_Interface_PCB_RevA_Fabrication.zip` as the "Gerber" file, and the BOM/CPL from `Sensor_Interface_PCB_RevA_Assembly.zip`, or `Sensor_Interface_PCB_RevA_Complete_Manufacturing.zip` where the service accepts a single archive |

## 2. Bare-board order parameters
| Parameter | Value |
|---|---|
| Layers | 2 |
| Size | 90 × 64 mm |
| Material / thickness | FR-4, 1.6 mm |
| Copper | 1 oz outer |
| Finish | **ENIG** (preferred; lead-free HASL acceptable) |
| Min track / space | 0.25 / 0.20 mm (standard process) |
| Min hole | 0.3 mm |
| Solder mask / silkscreen | both sides mask, top silkscreen (green / white suggested) |
| Electrical test | yes (IPC-D-356 netlist included) |
| Panel | not needed (single boards) |

Do not accept a DFM change that connects the U5 exposed pad (EF_RTN island) to GND, or that reduces the
+3V3_P copper around U1. See [FABRICATION_NOTES.md](../../manufacturing/Sensor_Interface_Power_Board/RevA/fabrication/FABRICATION_NOTES.md) §6.

## 3. Requesting full assembly (turnkey SMT + THT)
1. Choose **turnkey** (the factory buys all parts) and **top side** assembly, **lead-free**.
2. Upload the BOM (`..._BOM.csv`) and the pick-and-place file (`..._CPL.csv`, mm, origin bottom-left).
3. Ask the factory to confirm **in writing**:
   - THT soldering of J1 (terminal block), J2–J6 (pin headers) and LED1/LED2. The method may be wave, selective or hand. All 8 THT parts are on the top side.
   - That every **exact MPN** is sourced, especially **TPS26600PWPR**. Its stock was limited on 2026-11-09 (see
     [`reports/v0.3.0/BOM_SOURCING_AUDIT.md`](../../reports/v0.3.0/BOM_SOURCING_AUDIT.md)). Allowed fallback:
     the TPS26600PWPT reel variant, with your approval.
   - **No substitutions without your written approval** (every BOM line says so).
   - CPL rotation and polarity check against the assembly drawing (first-article inspection).
4. Supplier-specific notes for the researched candidates are in
   [`manufacturing/Sensor_Interface_Power_Board/manufacturer-profiles/`](../../manufacturing/Sensor_Interface_Power_Board/manufacturer-profiles/).
   None of them is confirmed. Any qualified PCBA manufacturer can use the standard package.

## 4. If you prefer to solder the THT parts yourself
Order SMT-only assembly (exclude J1–J6 and LED1/LED2 from the BOM/CPL in the factory's web tool) and hand-solder the 8
THT parts: lead-free solder, parts flush on the top side, square pad = pin 1, LED square pad = cathode.

## 5. After delivery
Inspect against [ASSEMBLY_NOTES.md](../../manufacturing/Sensor_Interface_Power_Board/RevA/assembly/ASSEMBLY_NOTES.md)
§4 (polarity), then run tests T1–T3 of the physical test plan before connecting an ESP32.
