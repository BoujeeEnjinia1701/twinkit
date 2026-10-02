---
doc_id: TWK-DEC-001
title: TwinKit design decisions register
project: TwinKit
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-02'
    author: Amish Chadha
    change: Register opened with the open decisions, purchase checks and value engineering from the constructable design (TWK-DDR-003)
---

# TwinKit design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`, TWK-BLD-001) describes the design as it stands and does not list open decisions.

## Open decisions

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Accept the design-for-construction changes (P1 to P9): battery box beside a 3-module UPS module, vents in the long walls, board standoffs, antenna bulkhead, cable entries, top-hat rail on screws, end stops, aluminium plate on feet, power and power-fail wiring | (a) accept as made; (b) accept with changes; (c) reject a change and say what replaces it | (a): none changes what the gateway does, its pitch or its safety case | The whole build plan follows them | TWK-DDR-003 |
| 2 | Region and radio band of the first build (EU868 or US915) | The band of the region where the first FieldNodes are used | Match FieldNode's pilot region, which is itself still open (FND-DDR-001, O1) | Which concentrator HAT and antenna to buy (BOM lines 7 and 9) | `bom/bom.csv` line 7; FND-DDR-001 |
| 3 | Co-design partner outside the lab | A small water utility, a makerspace or a municipal team | None made | Not part of the TRL 3 build; shapes the first field twin | TWK-DDR-002, O2 |

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The 9-module enclosure: whether it has moulded bosses for the computer, moulded vents, a flat front wall where the 20 mm and 16.2 mm holes go, and how its cover is held | Sets whether the floor holes and vent slots are cut or already there (build plan section 3.3) | TWK-DDR-003, P2, P3, P5 |
| 2 | The concentrator HAT passes the 40-pin header through, or names free GPIO and ground pins, and sits on the computer's 58 x 49 hole pattern | The power-fail pair connects there; the 16 mm standoffs and header extender assume that pattern and height | TWK-DDR-003, P3, P9 |
| 3 | The active cooler is no taller than 8 mm above the board | It must clear the HAT on 16 mm standoffs | TWK-DDR-003, P3 |
| 4 | The UPS module: 3 modules wide, no internal battery, a LiFePO4 setting at 14.6 V and 0.5 A or less, a 0 to 45 °C charge window, and a power-fail output that is a dry contact or open collector | Width sets the rail length; the output type decides whether the pair can go straight to a GPIO pin (safety stop S3) | `bom/bom.csv` line 11; TWK-DDR-003, P1, P9 |
| 5 | The backup pack is no larger than 38 x 70 x 38 mm with a lead of about 300 mm and its own BMS and fuse | It must fit the 3-module battery box with 3.5 mm to the gland nut | `bom/bom.csv` line 12; TWK-DDR-003, P1 |
| 6 | The DC-DC converter is 2 modules wide | Sets the rail length (345 mm of 350 mm used with end stops) | `bom/bom.csv` line 10 |
| 7 | The computer runs from the converter's 5.1 V through its USB-C socket without power negotiation | It then limits its USB sockets to low power, which the gateway does not use; if it refuses to boot, power it through its header pins instead | TWK-DDR-003, P9 |
| 8 | The network coupler's panel hole (20 mm assumed) and the rail's factory slot positions | Hole sizes in build plan sections 3.2 and 3.3 | TWK-DDR-003, P5, P6 |

## Value engineering

Value-engineering target: USD 300 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 334 (USD 34 over the target). Main cost drivers and savings worth trying:

- The largest lines are the concentrator HAT (USD 80), the computer (USD 65), the UPS module (USD 30), the backup pack (USD 25), the gateway enclosure and the DC-DC converter (USD 18 each) and the aluminium plate (USD 15).
- Making the design constructable added USD 44 against the concept's USD 290: the battery box (USD 8), end stops (USD 3), board mounting kit (USD 5), cable entries (USD 10), fixings and wiring (USD 9) and the aluminium plate in place of plywood (USD 9 more).
- Savings worth trying: a 9 mm plywood plate with threaded inserts in place of tapped aluminium (about USD 6 saved); an enclosure that already has bosses and vents for the computer (saves the standoff kit, about USD 3, and the cutting time); a DIN UPS module with a built-in LiFePO4 pack, if one meeting line 11 exists, which would remove the battery box (about USD 8); and a single supplier for the computer, cooler, card and standoffs. None of these changes what the gateway does.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 items D1 to D7: 8-channel LoRaWAN concentrator, 4 GB Pi 5 class computer, TimescaleDB, lightweight open-source stack with a TwinKit twin service, FieldNode battery and solar charge as the first example twin, the YAML twin file fields, an off-the-shelf LiFePO4 pack with built-in BMS | Amish: "i accept all your recommendations, go with them across all repos." | TWK-DDR-001, TWK-DDR-002 |
| 2026-09-25 | Budget raised from USD 200 to USD 300 to keep LoRaWAN compatibility (O1) | Amish, same instruction | TWK-DDR-002 |
| 2026-09-25 | R1 judged with adaptive data rate required (N1); R12 defined at light load with heavy jobs in cool hours, a larger or metal enclosure as the fallback (N2) | Amish, same instruction | TWK-DDR-002 |
| 2026-10-01 | `budget_usd` is a value-engineering target, not a spending limit | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens. its ok to ensure wording reflects that the hypothesis budget was x - the real cost being accrued is y" | `.kit/STANDARDS.md` section 18 |
