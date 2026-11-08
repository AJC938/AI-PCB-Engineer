# Block Diagram — V0.1.0 (planning)

Voltage domains are kept separate. No line connects a 5 V signal directly to an ESP32 GPIO.
The dashed link `L_DEVKIT_5V` exists **only** in Architecture A and is open in Architecture B.

## System and power architecture
```mermaid
flowchart LR
  subgraph IN["Input (external 5 V DC)"]
    VIN["5V DC input<br/>keyed connector"]
  end
  subgraph PROT["Input protection"]
    RP["Reverse-polarity<br/>protection"] --> OCP["Overcurrent<br/>protection"] --> TVS["Transient / ESD<br/>clamp (Should)"]
  end
  VIN --> RP
  TVS --> P5["+5V_P<br/>protected 5 V rail"]
  P5 --> LDO["3.3 V regulator<br/>(topology TBD)"] --> P33["+3V3_P<br/>3.3 V peripheral rail"]
  P5 --> LED5["PWR LED 5V"]
  P33 --> LED3["PWR LED 3V3"]
  P5 --> USVCC["Ultrasonic VCC<br/>(if 5 V variant)"]
  P5 -. "UART VCC option<br/>(3.3 V-logic devices only)" .-> UVCC["UART connector VCC"]
  P33 --> UVCC
  P33 --> I2CVCC["I2C connector VCC"]
  P33 --> GPVCC["GP connector VCC (Could)"]

  subgraph DK["ESP32 development board (exact model TBD, OQ-01)"]
    DK5["DevKit 5V pin"] --> DKLDO["DevKit on-board<br/>3.3 V regulator"] --> DK33["ESP32 VDD 3.3 V<br/>(GPIO domain)"]
    USB["DevKit USB"] --> DK5
  end
  P5 -. "L_DEVKIT_5V (Arch. A only)<br/>one-source rule REF-03" .-> DK5

  GND(("Common GND"))
```
Notes:
- `+3V3_P` and the DevKit's 3.3 V are **different rails**. They are never tied together (PWR-08).
- In Architecture A, the DevKit's USB and `L_DEVKIT_5V` must never supply the DevKit at the same time.
  How this is enforced is an open design decision (OQ-06, R-03).

## Signal paths
```mermaid
flowchart LR
  subgraph S5["Sensor domain (5 V if 'classic' module)"]
    ECHO["HC-SR04 ECHO<br/>(HIGH level UNVERIFIED)"]
    TRIGIN["HC-SR04 TRIG input<br/>(threshold UNVERIFIED)"]
  end
  subgraph LV["Level conditioning (board)"]
    ECHOCOND["Echo conditioning<br/>divider or 5V-tolerant buffer"]
    TRIGCOND["Trigger drive<br/>direct or 3.3→5 V translator (TBD)"]
  end
  subgraph G33["ESP32 GPIO domain (VDD 3.0–3.6 V)"]
    GECHO["GPIO (input) ECHO"]
    GTRIG["GPIO (output) TRIG"]
    GSDA["GPIO SDA"]
    GSCL["GPIO SCL"]
    GTX["GPIO UART TX"]
    GRX["GPIO UART RX"]
  end
  ECHO --> ECHOCOND --> GECHO
  GTRIG --> TRIGCOND --> TRIGIN
  subgraph B33["3.3 V external buses"]
    I2C["I2C connector<br/>SDA/SCL 3.3 V, pull-ups to TBD rail"]
    UART["UART connector<br/>TX/RX 3.3 V logic"]
  end
  GSDA <--> I2C
  GSCL <--> I2C
  GTX --> UART
  UART --> GRX
```
- Echo conditioning options are evaluated in INTERFACE_SPEC §2 (divider math in
  `calculations/v0.1.0/phase1_calcs_output.txt` §2).
- I2C and UART are 3.3 V logic only (I2C-02, UART-02). 5 V-logic devices are out of scope unless a
  translator is added.

## Power architecture options (summary; detail in POWER_BUDGET)
| Option | Description | Verdict (Phase 1) |
|---|---|---|
| **A** | Board powers the DevKit through its 5 V pin (`L_DEVKIT_5V` fitted). One supply for everything | Viable only with an enforced one-source rule (no simultaneous USB). Input path rated about 1 A |
| **B** | DevKit powered by its own USB. Board powers peripherals only. Common GND | Complies with REF-03 by construction. Lower input current (about 0.35 A). Back-powering risk on signal lines when the ESP32 is off (R-04) |
| C | Board 3.3 V feeds the DevKit 3V3 pin | **Rejected**: bypasses and conflicts with the DevKit regulator, violates the one-source rule whenever USB is connected |
| A/B selectable | Removable link (`L_DEVKIT_5V`) with B as default | Candidate. Needs an unambiguous label and a USB-presence rule. Decision OQ-06 |
