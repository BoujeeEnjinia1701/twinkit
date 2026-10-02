---
doc_id: TWK-REQ-001
title: TwinKit requirements
project: TwinKit
doc_type: Requirements
version: "0.5"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: First measurable requirements for TRL 2
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Status from the TRL 3 calculations (TWK-CAL-001); R1 found not met at SF9; decisions per TWK-DDR-001
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002). R1 restated with adaptive data rate, R12 restated at light load, R14 target raised to $300
- version: "0.5"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Constructable design (TWK-DDR-003): R10 with the battery box and end stops; R14 reported against the value-engineering target"
---

# TwinKit requirements

Status is judged from the TRL 3 calculation note TWK-CAL-001 v0.3 and the constructable model of TWK-DDR-003. No requirement is shown as not met or at risk; R13 (setup time) can only be shown by a timed trial. At v0.5, R14 is reported against its value-engineering target (Amish, 2026-10-01: the budget is "a hypothethical control target"): the constructable design is USD 34 over it. R10 still holds with the battery box and end stops added. Three requirements were changed at this revision by Amish's decisions of 2026-09-25 (TWK-DDR-002): R1 now requires adaptive data rate (was: under 1 % at SF7 to SF9, which failed at 1.02 % with every node on SF9); R12 now applies at the normal light load, with heavy jobs scheduled for cool hours (was: at any load, at risk); and R14's parts limit rises from $200 to $300 (was not met at $290).

Table 1. Requirements.

| ID | Requirement | Target | Status at TRL 3 (TWK-CAL-001) | Verification (TRL 4 or later) |
| --- | --- | --- | --- | --- |
| R1 | Receive readings from lab sensor nodes | 50 nodes at 1 reading per 5 min each, under 1 % of uplinks lost, with adaptive data rate enabled on the network server so each node uses the fastest spreading factor (SF7 to SF9) its link allows | Met: 0.21 % for an SF7 to SF9 mix [A3, A6]; for information, 1.02 % if all nodes were forced to SF9 [A2] | Bench and field packet counts |
| R2 | Accept common inputs | LoRaWAN (EU868 or US915), MQTT over Ethernet or Wi-Fi, HTTP POST | Met by design | Configuration check |
| R3 | Store history on the gateway | 1 year for 50 nodes x 10 fields at 5 min intervals | Met: 4.73 GB per year uncompressed on 56 GB free [B1, B2]; card wear 5.5 to 8.2 card cycles per year, to watch [B4] | Measured database size |
| R4 | Link data to the model | Every sensor channel mapped to a named part (BOM number) of the project's build123d model and to an expected value or calculation, in a validated schema | Met by design (schema fields adopted, TWK-DDR-001) | Schema review on the FieldNode example twin |
| R5 | Compare measured and expected | Residual and pass or flag state shown within 60 s of a reading arriving; flag when outside a stated tolerance for a stated time | Met: 0.9 to 4.7 s [C1] | Bench run |
| R6 | Show the twin in 3D | The project's glTF model, colored by live values, in a current browser on a mid-range laptop or phone | Met by design; frame rate not verifiable at TRL 3 | Browser trial |
| R7 | Work offline | All functions run with no internet; optional upstream sync buffers at least 7 days | Met by design; 7-day buffer 91 MB [B3] | Offline run |
| R8 | Low-voltage power | 9 to 30 V DC input, 12 V nominal; average draw 8 W or less | Met: 6.41 W average; 20.6 W peak, 2.29 A at 9 V, 3.15 A T fuse [D1 to D3] | Power measurement |
| R9 | Ride through outages | At least 30 min on backup and a clean shutdown before the pack is empty | Met: 2.40 h new, 1.63 h aged pack at 0 °C [E1] | Timed outage |
| R10 | Compact mounting | Fits a TS35 DIN rail; gateway, converter and backup within 20 modules (350 mm) of rail | Met: 331 mm, 18.9 modules; 345 mm with the end stops on a 350 mm rail [H1] | Fit check |
| R11 | Secure by default | Unique credentials set at first boot, TLS on the dashboard, no ports open beyond the local network by default | Met by design | Configuration audit |
| R12 | Operate in a lab or equipment room | Ambient 0 to 40 °C without CPU throttling at the normal light load; heavy jobs (database recompression, backups, rebuilds) scheduled for cool hours | Met: processor 69.1 °C at light load, vented, 15.9 K below an assumed 85 °C throttle point [F6]; 96.9 °C if a heavy job ran at 40 °C [F2] | Thermal test at 40 °C |
| R13 | Quick setup | From a flashed card to the first live reading on the dashboard in 60 min or less, following the guide | Not verifiable at TRL 3 | Timed trial |
| R14 | Low cost and buildable | Parts cost against a USD 300 value-engineering target (raised from $200, TWK-DDR-002; a control target, not a limit); no custom PCB | USD 334.00, USD 34 over the target [I1, I2]; no custom PCB | Supplier quotes |
| R15 | Open and exportable | All software open source; data exportable as CSV and through an open API | Met by design | Design review |
| R16 | Monitoring only | No control outputs; the gateway cannot actuate the monitored system | Met by design | Design review |

## Assumptions

The assumptions behind each status are listed in TWK-CAL-001, Table 1. The main ones are:

- A sensor reading is a LoRaWAN uplink of 20 bytes of payload plus 13 bytes of overhead, at 125 kHz and coding rate 4/5 (71.9 ms at SF7, 246.8 ms at SF9, 1810.4 ms at SF12).
- Uplinks spread evenly over 8 channels and arrive at random (pure ALOHA), with no capture effect.
- A stored value takes 90 bytes including index overhead, before compression.
- The gateway draws 6.41 W on average: board 4 W, fan 0.5 W, concentrator 1 W, converter at 90 % and UPS loss 0.3 W.
- The backup pack delivers 80 % of its 19.2 Wh rating when new.
- The processor throttles at 85 °C and sits 4 K/W above the enclosure air with its fan running; both are assumptions to be measured.
