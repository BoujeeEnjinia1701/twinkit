---
doc_id: TWK-DDR-003
title: TwinKit design for construction
project: TwinKit
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-02'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: Accepted by Amish on 2026-10-02 (TWK-DEC-001, item 1)
---

# 0003: Design for construction

- **Date:** 2026-10-02
- **Status:** accepted. Amish, 2026-10-02: "APPROVED: The open decisions from the last wave (TremorTrace to ZeerBox) came in after the review and aren't on the page either." This approves the recommendation written for each open decision in the design decisions register (TWK-DEC-001 v0.1), including acceptance of every change below (P1 to P9), as made. The record stays Draft. Nothing here changes what TwinKit does, its pitch or its safety case.

## Context

On 2026-09-30 Amish asked for every repo to have an illustrated prototype build plan, and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The TRL 3 model of TWK-DDR-002 was a massing model: it showed the gateway's modules at the right sizes on a DIN rail, but several parts could not be made, fitted or held as drawn. Checking the model part by part found nine problems (P1 to P9 below).

The changes keep what the gateway does: the same computer, cooler, concentrator, card, antenna, converter, UPS, pack, fuse and terminals, the same 9-module enclosure and its vent area, the same 12 V input and the same software. Every change is in `cad/src/model.py`, which now also runs 274 constructability checks (`python cad/src/model.py --check`): no two parts overlap, every part touches the part that holds it, and neighbours keep their stated clearances. All 274 pass.

## Options considered

For each problem the simplest physically sound fix that uses bought parts or plain workshop operations (saw, drill, tap, file) was chosen. The alternatives considered are given in the "Why this way" column.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | The backup pack was drawn inside the UPS module's shell. The UPS module and the pack are both bought parts, so one cannot be put inside the other. | The UPS module (line 11) is now a 3-module unit with no battery inside it. The pack (line 12, no larger than 38 x 70 x 38 mm, a 4S block of 18650 cells) sits in its own empty 3-module DIN enclosure, the battery box (new line 17), on a hook-and-loop pad, with its lead out through an M12 gland in the box's front wall. | Keeps everything on the rail, as the concept intended, and keeps the pack away from the charger's 0.81 W of heat [E3]. The pack, its BMS, its fuse and the charge path through the UPS are unchanged, so the safety case stands. |
| P2 | The vents were slots in the two end walls of the enclosure, which face the neighbouring terminal blocks and converter only 2 mm away, so almost no air could pass. | The same slots (two rows of 40 x 4 mm, low in the base and high in the cover, 42 mm apart vertically) move to the two long walls. | Same vent area (640 mm² low and high) and the same stack height, so the thermal results of TWK-CAL-001 stand. On a vertical cabinet plate the long walls face up and down, which makes the vents a chimney. A cautious check with the end walls counted as shielded gives 72.8 °C at light load, still 12.2 K below the assumed throttle point [F7]. |
| P3 | The computer floated 6 mm above the enclosure floor, and the HAT 16 mm above the computer, with nothing holding either. | Four 6 mm brass standoffs on four 2.7 mm floor holes (M2.5 screws from underneath), four 16 mm standoffs on top of them through the computer's holes, the HAT screwed on top, and a 2 x 20 header extender to carry the 40-pin header up to the HAT (new line 19). | The computer's own four-hole pattern (58 x 49 mm) carries both boards. The screw heads under the floor sit 4.75 mm outside the rail's flanges, clear of the DIN clip. The header extender sits between the standoffs with 1.1 mm to spare at each end. |
| P4 | The antenna bulkhead sat on top of the cover with no hole, and nothing connected it to the HAT. | A 6.5 mm hole in the cover, 30 mm left of the middle and 20 mm toward the back; the SMA bulkhead goes through it with its nut inside, and a U.FL pigtail runs to the HAT. | How an SMA bulkhead is fitted. The inside nut clears the HAT by about 22 mm. |
| P5 | No way for the network cable or the power and power-fail wires to enter the enclosure; the computer's network socket was inside a closed box, although R2 relies on Ethernet. | Two entries in the enclosure's front long wall, 26 mm above the floor: a round RJ45 feed-through coupler (20 mm hole) with a short patch lead to the computer, and an M16 gland with a two-hole insert for the USB-C power lead and the power-fail pair (new line 20). | A plug cannot pass through a sealing gland, so the network goes through a coupler. Both sit clear of the vents and of the boards (13.5 mm or more). On a cabinet plate the front wall faces down, so water cannot sit on the entries. |
| P6 | The DIN rail was drawn as a U channel lying on the plate, with no fixing. | A true TS35 x 7.5 top-hat section, 350 mm long, held to the plate by three M4 x 6 pan-head screws into tapped holes at the middle and 150 mm each side. | Every module's DIN clip needs the top-hat flanges to hook under. The screw heads sit 3.9 mm below the modules. |
| P7 | The modules stood on the rail with no clip and nothing stopped them sliding off its ends. | Each module's DIN clip is modelled (a hook under each flange), and two screw-clamped end stops (new line 18) press against the fuse holder and the battery box. | How DIN equipment is held. |
| P8 | The plate was "plywood or aluminium" with "4 screw holes", so the rail had nothing firm to screw into and the plate had nothing under it. | 6 mm aluminium sheet (line 1), three tapped M4 holes for the rail, four 5.5 mm corner holes for a wall or cabinet, and four stick-on rubber feet. | Tapped aluminium holds the rail without nuts underneath, so the plate can still lie flat on a wall. Plywood remains a saving worth trying (TWK-DEC-001, value engineering). |
| P9 | Power had no path from the converter to the computer, and the UPS power-fail signal had no path to the computer. | A 5 A USB-C power lead with bare ends from the converter's 5.1 V terminals to the computer, and a 0.25 mm² pair from the UPS power-fail contact to a free GPIO pin and ground, both through the power gland (line 21 and the wiring diagram in TWK-BLD-001). | Uses the computer's normal power socket. Without a power negotiation the computer limits its USB sockets to low power, which this gateway does not use. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Rail | Modules take 331 mm (18.9 modules), 345 mm with end stops, on a 350 mm rail (was 294 mm on 320 mm) [H1]. R10 (350 mm, 20 modules) is still met. | Battery box and end stops added; UPS module narrowed from 4 to 3 modules. |
| Cost | BOM lines 1, 2, 3, 11 and 12 respecified (line 1 repriced from USD 6 to USD 15), lines 17 to 21 added. Value-engineering target: USD 300. Estimated cost of the constructable design: USD 334 (USD 34 over the target) [I1, I2]. | Parts added for construction. `budget_usd` is unchanged; savings worth trying are in TWK-DEC-001. |
| Thermal | Unchanged in the design case (69.1 °C at light load [F6]); new sensitivity [F7] with the end walls counted as shielded: 72.8 °C, 12.2 K margin. | Vents moved, same area and spacing. |
| Power and backup | Unchanged (6.41 W, 2.40 h). | No electrical part changed. |
| Drawings and media | TWK-DWG-001 Rev P3; making sketches TWK-DWG-101 to 105 added; concept media regenerated from the model. | Follows the model. |
| Documents | TWK-CAL-001 v0.3, TWK-REQ-001 v0.5, TWK-PRC-001 v0.5, `bom/bom-notes.md`. | Follows the model. |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan TWK-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`).
- Requirement status: none not met, none at risk, 7 met by calculation, 7 met by design, 1 not verifiable at TRL 3 (R13), and R14 reported against its value-engineering target (USD 34 over).
- The photoreal renders (`media/render-hero.png`, `media/render-detail.png`), `media/card.png` and `media/social-preview.png` still show the concept: no end stops or battery box, vents in the end walls, the pack inside the UPS. They need regenerating on Amish's Mac, where Blender is.
- The enclosure, UPS module, pack and HAT are chosen when parts are bought; the items to confirm then are listed in TWK-DEC-001.
