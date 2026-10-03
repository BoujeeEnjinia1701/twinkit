---
doc_id: TWK-DDR-001
title: TwinKit TRL 2 review decisions
project: TwinKit
doc_type: Design decision record
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record the TRL 2 review recommendations adopted for TRL 3 work and the items that remain open
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: O2 recorded as decided by Amish on 2026-10-02
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted in part. On 2026-09-25 Amish accepted all recommendations ("i accept all your recommendations, go with them across all repos"). Items D1 to D7 and O1 are decided by Amish, 2026-09-25: go with recommendation (see TWK-DDR-002). O2 had no recommendation on 2026-09-25; Amish decided it on 2026-10-02 (TWK-DEC-001).

## Context

The TRL 2 review note (`docs/REVIEW.md`, session 2026-09-25, /populate) listed nine items as "Proposed, awaiting Amish", most with a recommendation. On 2026-09-25 Amish asked for this batch of repos to be taken through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed this repo's items one by one. Under that instruction, every item that carries a recommendation is adopted as recommended for TRL 3 work, open for his review. Items without a recommendation stay open. A recommended change to `budget_usd` is not applied: the figure is recorded here and in `docs/REVIEW.md` as awaiting Amish.

## Options considered

The options for each item are those listed in `docs/REVIEW.md` (session 2026-09-25, /populate) and in TWK-PRC-001 v0.2, Key design choices.

## Decision

*Table 1. Items adopted for TRL 3 work, now decided by Amish (TWK-DDR-002).*

| # | Item | Adopted choice | Status |
| --- | --- | --- | --- |
| D1 | Radio | 8-channel LoRaWAN concentrator (SX1302 or SX1303 class), not a point-to-point LoRa receiver. Consistent with FieldNode's recommended LoRaWAN radio (FND REVIEW, item 1). | Decided by Amish, 2026-09-25: go with recommendation |
| D2 | Computer | 4 GB Raspberry Pi 5 class board, not a 2 GB board. TWK-CAL-001 [G1, G2] shows the stack needs about 2.4 GB. | Decided by Amish, 2026-09-25: go with recommendation |
| D3 | Database | TimescaleDB, rather than InfluxDB or SQLite. | Decided by Amish, 2026-09-25: go with recommendation |
| D4 | Twin platform | Lightweight open-source stack plus a small TwinKit twin service, not Eclipse Ditto. | Decided by Amish, 2026-09-25: go with recommendation |
| D5 | First example twin | FieldNode battery and solar charge. | Decided by Amish, 2026-09-25: go with recommendation |
| D6 | Twin file schema | The YAML fields sketched in the precis: project, model, and per channel an id, node, part (BOM number), unit, expected value (constant, curve or calculation reference), tolerance and hold time. | Decided by Amish, 2026-09-25: go with recommendation |
| D7 | Backup pack | Off-the-shelf 12.8 V LiFePO4 pack with a built-in BMS and fuse; a CellGuard-protected pack only in a later, larger version. | Decided by Amish, 2026-09-25: go with recommendation |

*Table 2. Items left open by v0.1. O1 was decided on 2026-09-25 and O2 on 2026-10-02.*

| # | Item | Status |
| --- | --- | --- |
| O1 | Budget. The TRL 2 review recommended raising `budget_usd` from $200 to $300 (option a), to keep LoRaWAN compatibility. Under the session instruction the budget is not changed: `budget_usd` stays at $200, and $300 is recorded as the recommended figure. TWK-CAL-001 [I2] states the $290 parts cost against both figures. The design is costed for option (a) because D1 (LoRaWAN) is adopted. | Decided by Amish, 2026-09-25: go with recommendation; `budget_usd` raised to $300 (TWK-DDR-002) |
| O2 | Co-design partner outside the lab (a small water utility, a makerspace or a municipal team). No recommendation was made on 2026-09-25. | Decided by Amish, 2026-10-02 (TWK-DEC-001): the first candidate to approach is a small municipal water utility in the Dallas and Fort Worth area, found through the Texas Water Utilities Association, with Dallas Makerspace as the build and test partner |

No reworded pitch or problem line was recommended, so `project.yaml` and `README.md` keep the existing wording.

## Consequences

- `project.yaml`: only the TRL fields change. `budget_usd` stays at $200.
- TWK-PRB-001, TWK-PRC-001 and TWK-REQ-001 are revised to v0.3. The design choices in D1 to D7 are no longer described as "proposed" but as adopted for TRL 3 pending Amish's review. No requirement target is relaxed or redefined as a result of these items; R14 keeps its $200 target until Amish decides O1.
- TWK-CAL-001 led to two changes within these choices: a 3.15 A time-delay input fuse in place of 2 A, and a UPS module with a buck-boost charger for the 12.8 V pack (parts cost now $290).
- Cross-repo: FieldNode sends 20-byte LoRaWAN uplinks every 15 min by default; TwinKit is sized for 5 min, which is conservative. CityTwin recommends costing the gateway in TwinKit, which matches this record. No conflict was found; see `docs/REVIEW.md`.
- TRL 4 is on hold by Amish's instruction. Nothing in this record authorizes building or testing.
- Update at v0.2: the consequences above describe the state at v0.1. After Amish's decision of 2026-09-25, `budget_usd` is $300 and R14's target is $300; R1 and R12 were also restated. See TWK-DDR-002.
