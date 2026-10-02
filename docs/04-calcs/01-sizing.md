---
doc_id: TWK-CAL-001
title: TwinKit sizing calculations
project: TwinKit
doc_type: Calculation
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First issue for TRL 3 (airtime and collisions, storage and card wear, latency, power and fuse, backup, enclosure and processor temperature, memory, rail, cost)
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002). R1 judged with adaptive data rate, R12 at light load with heavy jobs in cool hours, R14 against the $300 budget
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: Constructable design (TWK-DDR-003). Vents in the long walls, battery box, 350 mm rail, new fittings costed; shielded end-wall sensitivity [F7]; budget treated as a value-engineering target
---

# TwinKit sizing calculations

On paper, TwinKit meets fourteen of its sixteen requirements (seven by calculation, seven by design); R13 (setup time) cannot be checked at TRL 3 and needs a timed trial, and R14 (cost) is reported against a value-engineering target rather than as met or not met. Version 0.3 follows the constructable design of TWK-DDR-003: the vents move from the end walls to the two long walls (same area and spacing, so the thermal results stand), the backup pack moves out of the UPS module into its own battery box, the rail grows to 350 mm, and the fittings that hold everything together are now in the BOM. Value-engineering target: USD 300. Estimated cost of the constructable design: USD 334 (USD 34 over the target) [I1, I2]. Version 0.2 applied the decisions Amish made on 2026-09-25 (TWK-DDR-002), which changed three results from v0.1. R1 (uplink loss) is now judged with adaptive data rate required, which spreads nodes over SF7 to SF9 and loses 0.21 % of uplinks against 1 %; with every node forced to SF9 the loss would be 1.02 % (v0.1 reported R1 as not met on that case). R12 (no processor throttling at 40 °C) is now defined at the normal light load, where the processor stays 15.9 K below its assumed throttle point, with heavy jobs scheduled for cool hours (v0.1: at risk). The calculations changed two parts of the TRL 2 concept: the input fuse rises from 2 A to 3.15 A time-delay, and the UPS module is specified with a buck-boost charger so that it can charge the 12.8 V pack from a 9 V to 12 V input. Several TRL 2 figures were corrected (see the last section). Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [A2], is the line of that script's output that carries it.

> **Safety:** These are first-principles estimates for a paper proof of concept. They are not a substitute for electrical safety checks of the 12 V wiring and the LiFePO4 pack, or for a security audit of the gateway. See TWK-PRC-001, Safety.

## Scope and method

The note checks every requirement in TWK-REQ-001 v0.4 against the design in TWK-PRC-001 v0.4, the decisions in TWK-DDR-001 and TWK-DDR-002 and the parametric model `cad/src/model.py`. The script imports the model's `PARAMS` and derived dimensions, so the enclosure size, vent areas and rail length used here are the ones in the STEP files and in drawing TWK-DWG-001. It also reads `bom/bom.csv` and `budget_usd` in `project.yaml`. Run it from the repo root with `python docs/04-calcs/sizing.py`.

The design case is the R1 design point: 50 sensor nodes, each sending a 20-byte reading every 5 min, to one gateway on a bench or in an equipment room at up to 40 °C. FieldNode's default interval is 15 min (FND-PRC-001 v0.2), so the 5 min case is conservative for FieldNode fleets.

## Assumptions

*Table 1. Main assumptions.*

| Area | Assumption | Basis |
| --- | --- | --- |
| Radio | 20-byte payload plus 13 bytes of LoRaWAN overhead; 125 kHz, coding rate 4/5, 8-symbol preamble, explicit header, CRC on, low data rate optimization at SF11 and SF12; unconfirmed uplinks | FieldNode payload convention; Semtech time-on-air formula |
| Traffic | Uplinks spread evenly over 8 channels, random arrival (pure ALOHA); spreading factors treated as orthogonal; no capture effect | Conservative screening model |
| Storage | 10 values per reading; 90 bytes per stored value in a narrow table with index, uncompressed; compressed chunks keep 10 % of that after 7 days; 8 GB for the system | Conservative for PostgreSQL rows; compression ratio assumed |
| Card wear | One 8 kB write-ahead log page per commit plus heap and index writes at twice the data size; write amplification inside the card of 10 | Assumed; card endurance data not available |
| Latency | Forwarder 0.1 s, network server 0.3 s, MQTT 0.05 s, twin service 0.2 s, database 0.2 s, dashboard refresh 2 s | Typical figures for these tools on a Pi 5 class board, to be measured |
| Power | Board 4 W light load, 8 W sustained full load; fan 0.5 W; concentrator 1.0 W receiving, 2.5 W during a downlink; converter 90 %; UPS 0.3 W; charger 14.6 V at 0.5 A, 90 % | Typical figures, to confirm from datasheets and measurement |
| Backup | 12.8 V, 1.5 Ah pack; 80 % usable; 85 % capacity at 0 °C; 80 % at end of life | Typical LiFePO4 data |
| Thermal | 40 °C ambient; combined convection and radiation 5 W/m²K (8 W/m²K as a check); vent discharge coefficient 0.6; bench mounting, so the vents are only 42 mm apart vertically; processor dissipates 2.5 W at light load and 6.5 W at full load; 4 K/W from processor to enclosure air with the fan running; throttling at 85 °C | Handbook ranges; thermal resistance and throttle point assumed for a Pi 5 class board, to be measured |

## A. Airtime and collisions (R1)

- **Traffic.** 50 nodes at 5 min give 600 uplinks per hour, 75 per channel per hour [A1].
- **Time on air.** A 33-byte frame takes 71.9 ms at SF7, 133.6 ms at SF8, 246.8 ms at SF9, 452.6 ms at SF10 and 1810.4 ms at SF12 [A2]. These agree with FieldNode's airtime table (FND-PRC-001 v0.2, Table 3).
- **Loss.** With every node on one spreading factor, collisions lose 0.30 % at SF7, 0.56 % at SF8, 1.02 % at SF9, 1.87 % at SF10 and 7.27 % at SF12 [A2]. An even mix of SF7, SF8 and SF9 loses 0.21 % [A3]. At FieldNode's 15 min default every case up to SF10 stays under 1 % (0.34 % at SF9) [A2].
- **Verdict.** R1, as restated in TWK-REQ-001 v0.4, requires adaptive data rate so that each node uses the fastest spreading factor its link allows. For an even SF7 to SF9 mix the loss is 0.21 % against 1 % [A6], so R1 is met. For information: if all 50 nodes were forced to SF9 at 5 min the loss would be 1.02 %, and the largest fleet under 1 % in that case is 48 nodes [A5]. FieldNode's 15 min default keeps every case up to SF10 under 1 % [A2].
- **Regulatory duty cycle.** At SF9 and 5 min each node uses 0.08 % of air time, well inside the 1 % EU868 sub-band limit [A4]. The Things Network's 30 s per day fair-use limit does not apply on a private TwinKit gateway, but a node at SF9 and 5 min would exceed it (71 s per day) if moved to that public network [A2].

## B. Storage and card wear (R3, R7)

- **Volume.** R3's case stores 52.6 million values a year. At the TRL 2 figure of 30 bytes that is 1.58 GB; at a conservative 90 bytes uncompressed it is 4.73 GB, and 0.55 GB with compression after 7 days [B1].
- **Capacity.** With 56 GB free on the 64 GB card, the data fits for 11.8 years uncompressed [B2]. R3 is met.
- **Sync buffer.** Seven days of readings for upstream sync take 91 MB [B3]. R7's buffer is met.
- **Wear.** Committing each uplink writes about 53 GB a year; batching commits every 10 s writes about 35 GB. At an assumed card write amplification of 10, that is 8.2 or 5.5 full-card program cycles a year [B4]. This is modest for a high-endurance card, but the card's own endurance and amplification are unknown. Batched commits are adopted in the twin service design, and an SSD remains the upgrade path.

## C. Latency and flag timing (R5)

- **Reading to dashboard.** 0.9 s at SF7 with a pushed update, up to 4.7 s at SF12 with a 2 s dashboard refresh [C1]. R5 (60 s) is met with a wide margin.
- **Fault to flag.** A flag is raised only after the residual stays out of tolerance for the hold time. With the example 30 min hold, a step fault is flagged within 35 min at 5 min readings, or 45 min at FieldNode's 15 min default [C2]. The hold time is therefore the design lever for early warning, not the data path.

## D. Power, peak current and fuse (R8)

- **Average.** 5.5 W on the 5 V rail becomes 6.41 W at the 12 V input, 0.53 A, or 56 kWh a year [D1]. R8 (8 W) is met. The TRL 2 figure of about 6 W was slightly low.
- **Peak.** With the board at full load, a downlink in progress and the pack charging, the input peaks at 20.6 W: 1.72 A at 12 V and 2.29 A at the 9 V lower limit of R8. The 5 V rail carries 2.16 A of the converter's 5 A [D2].
- **Fuse.** A 2 A fuse run at no more than 75 % of rating allows 1.50 A, too little at 9 V. A 3.15 A time-delay fuse allows 2.36 A [D3]. The BOM (line 13) is changed to 3.15 A T.
- **Charger interface.** The pack charges to 14.6 V, above a 12 V input. The UPS module (line 11) must therefore have a buck-boost charger that works from 9 V to 30 V. The BOM specification is changed accordingly; the price rises from $25 to $30 (indicative).

## E. Backup (R9)

- **Runtime.** On battery the gateway draws 6.41 W. The pack gives 15.36 Wh usable, which lasts 2.40 h when new and 1.63 h for an aged pack at 0 °C [E1]. R9 (30 min) is met in every case.
- **Shutdown and recharge.** A clean shutdown needs 0.13 Wh; the pack refills from its cut-off in about 2.4 h at 0.5 A [E2].

## F. Enclosure and processor temperature (R12)

- **Geometry.** The 157.5 x 90 x 60 mm enclosure exposes 0.0439 m². Two slot rows in each long wall give 640 mm² of low and of high vent, 42 mm apart vertically in the bench case. The constructable design (TWK-DDR-003) moved the slots from the end walls, which face the neighbouring modules only 2 mm away, to the long walls; area and spacing are unchanged. It holds 5.5 W at light load and 9.5 W at full load [F1].
- **Light load.** Vented, the enclosure air rises 19.1 K to 59.1 °C at 40 °C ambient and the processor reaches 69.1 °C, 15.9 K below throttling. Sealed, the air rises 25.1 K and the processor reaches 75.1 °C [F2].
- **Full load.** Sustained full load raises the processor to 96.9 °C vented and 109.3 °C sealed, so it would throttle [F2]. At the more typical 8 W/m²K it still reaches 88.3 °C [F3]. Doubling the vent area only brings it to 91.1 °C [F5].
- **Shielded end walls.** With modules 2 mm away on both sides, the end walls shed little heat. Leaving them out of the exposed area (0.0331 m² instead of 0.0439 m²) raises the processor to 72.8 °C at light load, still 12.2 K below the assumed throttle point, and 102.4 °C at full load [F7]. R12 is met in this more cautious case too.
- **Verdict.** R12, as restated in TWK-REQ-001 v0.4, applies at the normal light load (0.17 uplinks per second [G3]), with heavy jobs such as a full database recompression or backup scheduled for cool hours. In that case the processor reaches 69.1 °C, 15.9 K below the assumed throttle point [F6], so R12 is met on paper. A sustained heavy job at 40 °C would still throttle (96.9 °C), which is why the schedule rule is part of the design. The thermal resistance and throttle point are assumptions to be measured at TRL 4 (on hold); a larger or metal enclosure remains the hardware fallback if tests show throttling.
- **Pack.** The LiFePO4 pack sits in its own battery box beside the UPS module (TWK-DDR-003), away from the charger's 0.81 W of loss while charging [E3], so it stays within a few kelvin of ambient and inside the usual 45 °C charge limit at 40 °C. A sealed street cabinet in sun (CityTwin) is a different case and is not covered here.

## G. Memory

- **Budget.** At light load the stack uses about 2.42 GB of 4 GB: system 0.40, network server and Redis 0.25, MQTT 0.02, PostgreSQL with TimescaleDB 0.90, dashboard 0.20, twin service 0.15 and 0.50 GB of file cache headroom [G1]. A 2 GB board would be short by 0.42 GB [G2], which supports the 4 GB board adopted in TWK-DDR-001.
- **Load.** 0.17 uplinks per second, or 1.7 values per second, is a very light database load [G3].

## H. Rail and mounting (R10)

- **Rail.** Terminals, enclosure, converter, UPS and battery box take 331 mm (18.9 modules); with the two end stops they occupy 345 mm of a 350 mm rail [H1]. R10 (350 mm, 20 modules) is met. Before the constructable design the four modules took 294 mm (16.8 modules) of a 320 mm rail, with the pack drawn inside the UPS module.
- **Height.** The enclosure top is 67.5 mm above the plate and the antenna tip 264 mm [H2].

## I. Cost (R14)

- **Total.** All 21 BOM lines are priced; the total is $334.00: computer, cooler and card $85, radio and antenna $92, power and backup $85, enclosure, rail and plate $37, battery box and fittings for construction $35 [I1].
- **Against the target.** `budget_usd` is a hypothetical value-engineering target, not a limit (Amish, 2026-10-01). Value-engineering target: USD 300. Estimated cost of the constructable design: USD 334 (USD 34 over the target) [I2]. The concept was USD 290; the battery box, end stops, board mounting kit, cable entries, fixings and the aluminium plate added USD 44 (TWK-DDR-003). No custom PCB is used. Prices are indicative, not supplier quotes. Savings worth trying are listed in the design decisions register (TWK-DEC-001).

## J. Results against every requirement

*Table 2. Requirement status at TRL 3 [J1, J2].*

| ID | Requirement | Value | Target | Status |
| --- | --- | --- | --- | --- |
| R1 | Receive readings | 0.21 % loss with adaptive data rate (SF7 to SF9 mix); 1.02 % if all forced to SF9 | Under 1 %, 50 nodes at 5 min, adaptive data rate | Met |
| R2 | Common inputs | LoRaWAN concentrator, MQTT, HTTP | LoRaWAN, MQTT, HTTP | Met by design |
| R3 | Store history | 4.73 GB per year uncompressed on 56 GB free | 1 year | Met |
| R4 | Link data to model | Twin file schema, TWK-PRC-001 | Every channel mapped to a part and an expected value | Met by design |
| R5 | Compare measured and expected | 4.7 s worst case | 60 s | Met |
| R6 | 3D twin | glTF in a standard web viewer | Current browser, laptop or phone | Met by design; frame rate not verifiable at TRL 3 |
| R7 | Work offline | All local; 91 MB for 7 days | 7-day buffer | Met by design |
| R8 | Low-voltage power | 6.41 W average; 20.6 W peak | 9 to 30 V; 8 W average | Met |
| R9 | Ride through outages | 2.40 h new, 1.63 h worst | 30 min and clean shutdown | Met |
| R10 | Compact mounting | 331 mm, 18.9 modules (345 mm with end stops) | 350 mm, 20 modules | Met |
| R11 | Secure by default | First-boot credentials, TLS, no WAN ports | As stated | Met by design |
| R12 | Operate at 0 to 40 °C | Processor 69.1 °C at light load (72.8 °C with the end walls shielded); heavy jobs in cool hours (96.9 °C if run at 40 °C) | No throttling at light load (85 °C assumed) | Met |
| R13 | Quick setup | Not calculable | 60 min | Not verifiable at TRL 3 |
| R14 | Low cost | $334.00 | Value-engineering target $300 | $34 over the target |
| R15 | Open and exportable | Open-source stack, CSV and API | As stated | Met by design |
| R16 | Monitoring only | No control outputs | As stated | Met by design |

Summary: 0 not met, 0 at risk, 7 met by calculation, 7 met by design, 1 not verifiable at TRL 3 (R13), and R14 reported against its value-engineering target (USD 34 over). In v0.2: 8 met by calculation, with R14 met at $290. In v0.1: 2 not met (R1, R14), 1 at risk (R12).

## Checks against earlier figures

*Table 3. Earlier figures corrected by this note (TRL 2, and TRL 3 v0.2 where marked).*

| Quantity | TRL 2 (TWK-PRC-001 v0.2) | TRL 3 | Change |
| --- | --- | --- | --- |
| Airtime, 20-byte reading | about 60 ms (SF7), 1.3 s (SF12) | 71.9 ms, 1810.4 ms | Overhead bytes and low data rate optimization now counted |
| Loss at SF12, all nodes | about 5 % | 7.27 % | Follows the airtime |
| R1 status | Met at SF7 to SF9 | Not met at SF9 (1.02 %) | TRL 2 claim was wrong |
| Storage per year | about 1.6 GB | 4.73 GB uncompressed (0.55 GB compressed) | 90 bytes per value instead of 30 |
| Average power | about 6 W | 6.41 W | UPS loss counted |
| Backup time | about 2 h (2.3 h) | 2.40 h new, 1.63 h worst | Load and derating recomputed |
| Enclosure air rise | about 20 K | 19.1 K vented, 25.1 K sealed | Mounting face excluded, vents modeled |
| Rail used | about 300 mm (17 modules) | 294 mm (16.8 modules) | From the model |
| Parts cost | about $285 | $290.00 | UPS with buck-boost charger |
| Input fuse | 2 A | 3.15 A time-delay | Peak current at 9 V |
| Rail used | 294 mm (TRL 3 v0.2) | 331 mm, 345 mm with end stops | Battery box and end stops added (TWK-DDR-003) |
| Parts cost | $290.00 (TRL 3 v0.2) | $334.00 | Fittings for construction added (TWK-DDR-003) |
