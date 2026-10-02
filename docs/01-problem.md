---
doc_id: TWK-PRB-001
title: TwinKit problem statement
project: TwinKit
doc_type: Problem statement
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
  change: Populate to TRL 2 (users, context, constraints, prior work)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record TRL 2 review items adopted for TRL 3 (TWK-DDR-001) and the items still open
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002). Budget constraint raised to $300; open questions closed except the co-design partner
- version: "0.5"
  date: '2026-10-02'
  author: Amish Chadha
  change: Budget worded as a value-engineering target; cost of the constructable design (TWK-DDR-003)
---

# TwinKit problem statement

Digital twins are sold as enterprise software, out of reach for small builders, small utilities and cities, yet the core idea is simple: a model, live data and a comparison between them. There is no open, low-cost kit that lets a small team link the model and calculations it already has to readings from the field.

## The problem

A digital twin, in the sense introduced by Grieves and Vickers, pairs a physical system with a virtual model that is updated from the physical one, so that the two can be compared and deviations caught early ([Grieves and Vickers, 2017](https://link.springer.com/chapter/10.1007/978-3-319-38756-7_4)). Standards now describe the reference architecture for manufacturing twins ([ISO 23247-2:2021](https://www.iso.org/standard/78743.html); [NIST analysis of ISO 23247](https://www.nist.gov/publications/analysis-new-iso-23247-series-standards-digital-twin-framework-manufacturing)). In practice the capability is delivered through large vendor platforms and cloud subscriptions sized for large operators.

Small operators have the most to gain from early fault detection and the least access to it:

- Water utilities lose an estimated 126 billion m³ of treated water a year to leaks and unbilled use, worth nearly $40 billion ([World Bank, 2018](https://blogs.worldbank.org/en/ppps/what-do-private-companies-look-performance-based-non-revenue-water-project)). Kenya's utilities report a national average non-revenue water of 44 % ([WASREB Impact Report 17, 2025](https://wasreb.go.ke/wp-content/uploads/2025/06/IMPACT-REPORT-17.pdf)).
- About one in four handpumps in sub-Saharan Africa is non-functional at any time, roughly 175,000 water points in 2015 ([Foster et al., 2019, via IRC](https://www.ircwash.org/resources/functionality-handpump-water-supplies-review-data-sub-saharan-africa-and-asia-pacific)). Faults are found when people report them, not when the data shows them.
- Small and medium enterprises make up about 90 % of businesses and more than half of employment worldwide ([World Bank](https://www.worldbank.org/en/topic/smefinance)), yet enterprise twin platforms are priced for the largest firms.

Within the Design Molecule lab the same gap appears on a small scale. Every project has a build123d model and design calculations, and several (FieldNode, WaterWatch, PowerBox, the smart city nodes) will produce live readings. Nothing yet ties those readings back to the model and the calculation that predicted them, so the lab cannot show whether a design performs as calculated.

## Prior work

- **Open-source twin frameworks.** [Eclipse Ditto](https://eclipse.dev/ditto/) manages twin state for IoT devices through an API. It is powerful but assumes a server cluster and does not link to CAD or design calculations.
- **Open IoT stacks.** LoRaWAN network servers, MQTT brokers, time-series databases and dashboards are mature open-source tools and run on a single-board computer. They show data as charts, not against a model or an expected value.
- **City twins.** [Virtual Singapore](https://oecd-opsi.org/innovations/virtual-twin-singapore/) shows what a national 3D twin can do for planning, at a scale and cost no small city can match.

TwinKit's contribution is the thin layer between these: a mapping from each sensor channel to a part of the project's model and to the calculation that predicts its value, running offline on one small gateway.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Design Molecule lab (first user) | See each prototype's live readings on its model and against its design calculation | Lab bench and first field pilots |
| Small builder or maker team | A twin of their own device without a cloud contract | Workshop, garage, school lab |
| Small utility or facility operator | Early warning when a pump, tank, store or battery drifts from expected behavior | Village water scheme, clinic, small factory |
| City team (via CityTwin) | A gateway and data layer for street sensors | Municipal pilot |
| Students and researchers | An inspectable, reproducible twin pipeline to learn from and extend | University lab, makerspace |

## Constraints

- Garage-buildable prototype from off-the-shelf modules with no custom PCB. Value-engineering target for the parts: USD 300 (raised from USD 200 by Amish on 2026-09-25, TWK-DDR-002); a hypothetical control target, not a limit (Amish, 2026-10-01).
- Runs on one gateway with no internet connection and no vendor cloud account.
- Open licenses throughout: hardware CERN-OHL-S-2.0, TwinKit code MIT, and open-source third-party software.
- Low voltage only (12 V DC input).
- Monitoring only: TwinKit reads and compares; it does not control equipment.
- Secure by default, because an edge gateway on a network is an attack surface.

## Out of scope

- Closed-loop control or actuation of the monitored system.
- Physics simulation beyond the project's own calculations (TwinKit compares measured values with expected values; it does not run finite element or CFD models).
- Hosted cloud services. Upstream sync to a server the owner controls is optional.
- Camera or audio data.

## Open questions

- First example twin: FieldNode (battery state of charge against its power-budget calculation). Decided by Amish, 2026-09-25: go with recommendation (TWK-DDR-002).
- Radio: a full LoRaWAN concentrator rather than a point-to-point LoRa receiver. Decided by Amish, 2026-09-25: go with recommendation (TWK-DDR-002).
- Budget: decided by Amish, 2026-09-25: go with recommendation, `budget_usd` raised from $200 to $300 (TWK-DDR-002). Value-engineering target: USD 300. Estimated cost of the constructable design: USD 334 (USD 34 over the target; TWK-CAL-001 v0.3, TWK-DDR-003).
- Who outside the lab should co-design the operator view (a small water utility, a makerspace, a municipal team)? No recommendation; proposed, awaiting Amish.
