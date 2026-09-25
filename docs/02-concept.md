---
doc_id: TWK-PRC-001
title: TwinKit design precis
project: TwinKit
doc_type: Design precis
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
  change: Populate to TRL 2 (architecture, first-order numbers, safety, media)
---

# TwinKit design precis

TwinKit is a small DIN rail edge gateway plus open software that receives sensor readings, stores them, and shows each reading on the project's own build123d model next to the value the design calculation predicted. First-order numbers suggest one single-board computer with a LoRaWAN concentrator can serve 50 sensor nodes, store a year of data and ride through a 2 h outage on about 6 W. Parts cost about $285, above the $200 budget; options are listed below and in REVIEW.md.

![Hero render](../media/hero.png)

Figure 1. Gateway on a DIN rail and bench plate, with a desk and 14-inch laptop for scale.

## How it works

1. **Sense.** Sensor nodes such as FieldNode (a sibling lab project) send small readings over LoRa radio. Other devices can post over MQTT or HTTP on the local network.
2. **Receive.** An 8-channel LoRaWAN concentrator on the gateway hears all nodes in range; an open-source network server decodes the packets and publishes them to a local MQTT broker.
3. **Store.** A time-series database on the gateway keeps every reading with its node, channel, unit and time.
4. **Map.** A mapping file for each project (the twin file) links every channel to a named part of the project's build123d model, using the same part names and BOM numbers the concept media already use, and to an expected value: a constant, a curve, or a function from the project's calculation note.
5. **Compare.** The TwinKit twin service computes the residual (measured minus expected) for each reading and raises a flag when it stays outside the stated tolerance for the stated time.
6. **Show.** A browser dashboard shows trends and flags, and a 3D view loads the project's `model.glb` and colors each mapped part by its live value or residual.

![Data flow](../media/flow.png)

Figure 2. Data flow from sensor to twin. Values are estimates.

An illustrative twin file for the proposed first example (FieldNode) might read:

```yaml
project: fieldnode
model: media/model.glb
channels:
  - id: battery_v
    node: fieldnode-01
    part: 4            # BOM number of the LiFePO4 cell in FieldNode's model
    unit: V
    expected: calc.power_budget.soc_to_voltage   # from FieldNode's calculation note
    tolerance: 0.1
    hold: 30 min
```

The schema is a concept sketch; its fields are proposed, awaiting Amish.

## Main components

Table 1. Main components (numbers match `bom/bom.csv` and Figure 3).

| # | Component | Proposed choice | Notes |
| --- | --- | --- | --- |
| 1, 2 | Bench plate and DIN rail | 6 mm plate, TS35 rail | Plate optional when an equipment cabinet exists |
| 3, 4 | Gateway enclosure | 9-module DIN enclosure, vented, clear cover | Holds the computer and concentrator |
| 5, 6 | Single-board computer and cooler | 4 GB quad-core Arm board (Raspberry Pi 5 class) | Runs all software. Proposed, awaiting Amish |
| 7 | LoRaWAN concentrator | SX1302 or SX1303 8-channel HAT | Region version (EU868 or US915). Proposed, awaiting Amish |
| 8 | Storage | 64 GB high-endurance microSD | SSD upgrade is an option |
| 9 | Antenna | 3 dBi whip on an SMA bulkhead | Mounted on the cover or outside a cabinet |
| 10 | DC-DC converter | 9 to 30 V in, 5.1 V 5 A out | Accepts a 12 V adapter or an existing 12 V system |
| 11, 12 | Backup | DIN 12 V UPS module with a 12.8 V, 1.5 Ah LiFePO4 pack | Power-fail signal triggers a clean shutdown |
| 13 | Terminals and fuse | DIN terminal blocks, 2 A fuse | Fuse at the supply input |
| 14 | Open-source stack | LoRaWAN network server, MQTT broker, time-series database, dashboard | All open source, no cloud account |
| 15 | Twin service and schema | Python service and YAML twin file | TwinKit's own code, MIT |
| 16 | Example twin | FieldNode battery and solar charge | Proposed, awaiting Amish |

![Exploded view](../media/exploded.png)

Figure 3. Exploded view with BOM numbers.

![Cutaway](../media/cutaway.png)

Figure 4. Cutaway through the gateway enclosure (left), converter (center) and UPS with backup pack (right).

## First-order numbers

All values are estimates for concept review and will be checked at TRL 3.

Table 2. First-order numbers.

| Quantity | Estimate | Basis | Requirement |
| --- | --- | --- | --- |
| Uplinks handled | 600 per hour | 50 nodes x 12 readings per hour | R1 |
| Uplink loss from collisions | under 0.3 % at SF7; about 5 % if all nodes use SF12 | Pure ALOHA, 75 uplinks per channel per hour, 60 ms or 1.3 s airtime | R1 met at SF7 to SF9 |
| Stored values per year | about 53 million | 50 nodes x 10 fields x 288 per day x 365 | R3 |
| Storage per year | about 1.6 GB | 30 bytes per value before compression | R3 met (64 GB card) |
| Reading to dashboard | under 5 s | MQTT and database writes in well under 1 s each; dashboard refresh 2 s | R5 met (60 s) |
| Average power | about 6 W (0.5 A at 12 V) | Computer about 4 W, concentrator about 1 W, losses about 1 W | R8 met (8 W) |
| Backup time | about 2 h | 19.2 Wh x 80 % usable, 90 % converter efficiency, 6 W load gives 2.3 h | R9 met (30 min) |
| Enclosure air temperature rise | about 20 K | 6 W over about 0.059 m² of enclosure surface at 5 W/(m²·K) | R12 not yet shown |
| Rail length used | about 300 mm (17 modules) | 9 + 2 + 4 modules plus terminals | R10 met |
| Parts cost | about $285 | Indicative prices, see `bom/bom.csv` | R14 not met ($200) |

The thermal estimate is the main technical risk: at 40 °C ambient, enclosure air near 60 °C leaves little margin before the processor throttles. Vents, the active cooler and a light software load are expected to be enough, but this must be checked at TRL 3.

## Key design choices

- **Compare with the calculation, not only with thresholds.** Most dashboards alarm on fixed limits. TwinKit compares each reading with what the design said it should be at that moment, so a battery that charges more slowly than the power budget predicted is caught before it goes flat.
- **Reuse the portfolio's own model outputs.** Every lab repo already exports a `model.glb` with named, BOM-numbered parts. The twin file points at those names, so no separate 3D model is built for the twin.
- **Edge first.** Everything runs on the gateway. An upstream server is optional, which keeps the kit usable where connectivity is poor and keeps data with its owner.
- **LoRaWAN rather than a single-channel receiver.** An 8-channel concentrator follows the open standard and accepts third-party sensors, at about $55 more than a point-to-point receiver. Proposed, awaiting Amish.
- **Lightweight stack over a twin platform.** Frameworks such as Eclipse Ditto assume a server cluster; a single-board computer running a network server, MQTT, a time-series database and a small Python service fits in 4 GB. Proposed, awaiting Amish.
- **Monitoring only.** No control outputs, so a software fault cannot move a pump or switch a load.

## Relation to other lab projects

- **FieldNode** is the primary data source and the proposed first example twin.
- **CityTwin** builds its public map and kiosk on TwinKit's gateway and software.
- **CellGuard** could protect a larger backup pack in a later version; at this size an off-the-shelf pack with a built-in BMS is proposed.
- **CalRig** calibration records could feed each channel's tolerance in the twin file.

## Safety

> **Safety:** The backup pack is a lithium (LiFePO4) battery. Use a pack with a built-in BMS and fuse, charge it only through the UPS module within the maker's limits, keep it away from heat, and never leave a first build charging unattended.

> **Safety:** The gateway runs from 12 V DC. Use a certified, double-insulated mains adapter; any wiring to an existing 12 V system or into a mains cabinet must be done or checked by a qualified electrician under local code.

> **Safety:** A network gateway is an attack surface. Change every default credential, keep it off the public internet until it is hardened, apply updates, and treat sensor data as the owner's data.

> **Safety:** TwinKit is a monitoring aid. It must not be relied on as a safety system, and it does not replace alarms, protection devices or inspections that a regulation or the equipment maker requires.

## Open questions for TRL 3

- Thermal check of the enclosure at 40 °C ambient; do vents suffice or is a larger enclosure needed?
- Confirm airtime and loss figures for the chosen spreading factors and FieldNode's payload format.
- Choose the time-series database (TimescaleDB, InfluxDB or SQLite) against memory use and card wear. Proposed: TimescaleDB, awaiting Amish.
- Define the twin file schema and how expected values are imported from a project's calculation note.
- microSD wear over a year of writes, or move to an SSD.

Concept media: [blueprint sheet](../media/concept-blueprint.pdf), [interactive 3D model](../media/viewer.html).
