---
doc_id: TWK-REQ-001
title: TwinKit requirements
project: TwinKit
doc_type: Requirements
version: "0.2"
status: Draft
date: '2026-09-25'
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
---

# TwinKit requirements

These are first-pass requirements for the concept. Targets are proposals for review. Status is judged from the first-order estimates in TWK-PRC-001 and will be checked by calculation at TRL 3. One requirement (R14, cost) is not met, and two (R12, thermal; R13, setup time) are not yet shown.

Table 1. Requirements.

| ID | Requirement | Target | Status at TRL 2 | Verification (TRL 3 or later) |
| --- | --- | --- | --- | --- |
| R1 | Receive readings from lab sensor nodes | 50 nodes at 1 reading per 5 min each, under 1 % of uplinks lost at SF7 to SF9 | Met by estimate | Airtime and collision calculation |
| R2 | Accept common inputs | LoRaWAN (EU868 or US915), MQTT over Ethernet or Wi-Fi, HTTP POST | Met by design | Design review |
| R3 | Store history on the gateway | 1 year for 50 nodes x 10 fields at 5 min intervals | Met by estimate (about 1.6 GB of 64 GB) | Storage calculation |
| R4 | Link data to the model | Every sensor channel mapped to a named part (BOM number) of the project's build123d model and to an expected value or calculation, in a validated schema | Met by design | Schema review on the example twin |
| R5 | Compare measured and expected | Residual and pass or flag state shown within 60 s of a reading arriving; flag when outside a stated tolerance for a stated time | Met by estimate (under 5 s) | Latency estimate; later bench run |
| R6 | Show the twin in 3D | The project's glTF model, colored by live values, in a current browser on a mid-range laptop or phone | Met by design | Design review |
| R7 | Work offline | All functions run with no internet; optional upstream sync buffers at least 7 days | Met by design | Design review |
| R8 | Low-voltage power | 9 to 30 V DC input, 12 V nominal; average draw 8 W or less | Met by estimate (about 6 W) | Power budget |
| R9 | Ride through outages | At least 30 min on backup and a clean shutdown before the pack is empty | Met by estimate (about 2 h) | Backup energy calculation |
| R10 | Compact mounting | Fits a TS35 DIN rail; gateway, converter and backup within 20 modules (350 mm) of rail | Met (about 17 modules in the massing model) | Massing model |
| R11 | Secure by default | Unique credentials set at first boot, TLS on the dashboard, no ports open beyond the local network by default | Met by design | Design review; later configuration audit |
| R12 | Operate in a lab or equipment room | Ambient 0 to 40 °C without CPU throttling | Not yet shown (enclosure air about 20 K above ambient, estimate) | Thermal calculation |
| R13 | Quick setup | From a flashed card to the first live reading on the dashboard in 60 min or less, following the guide | Not yet shown | Timed trial at TRL 4 |
| R14 | Low cost and buildable | Parts $200 or less; no custom PCB | Not met (about $285; no custom PCB is met) | Priced BOM |
| R15 | Open and exportable | All software open source; data exportable as CSV and through an open API | Met by design | Design review |
| R16 | Monitoring only | No control outputs; the gateway cannot actuate the monitored system | Met by design | Design review |

## Assumptions

- A sensor reading is a LoRaWAN uplink of about 20 bytes of payload. Airtime is about 60 ms at SF7 and about 1.3 s at SF12, both at 125 kHz bandwidth.
- Uplinks spread evenly over 8 channels and arrive at random (pure ALOHA).
- A stored value takes about 30 bytes including index overhead, before any database compression.
- The gateway draws about 6 W: single-board computer about 4 W under light load, concentrator about 1 W, converter and UPS losses about 1 W.
- The backup pack delivers 80 % of its 19.2 Wh rating.
