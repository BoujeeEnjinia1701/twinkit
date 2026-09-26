---
doc_id: TWK-DDR-001
title: TwinKit TRL 2 review decisions
project: TwinKit
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record the TRL 2 review recommendations adopted for TRL 3 work and the items that remain open
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** proposed. The recommendations in items D1 to D7 are adopted for TRL 3 work pending Amish's review; items O1 and O2 remain "Proposed, awaiting Amish".

## Context

The TRL 2 review note (`docs/REVIEW.md`, session 2026-09-25, /populate) listed nine items as "Proposed, awaiting Amish", most with a recommendation. On 2026-09-25 Amish asked for this batch of repos to be taken through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed this repo's items one by one. Under that instruction, every item that carries a recommendation is adopted as recommended for TRL 3 work, open for his review. Items without a recommendation stay open. A recommended change to `budget_usd` is not applied: the figure is recorded here and in `docs/REVIEW.md` as awaiting Amish.

## Options considered

The options for each item are those listed in `docs/REVIEW.md` (session 2026-09-25, /populate) and in TWK-PRC-001 v0.2, Key design choices.

## Decision

*Table 1. Items adopted for TRL 3 work.*

| # | Item | Adopted choice | Status |
| --- | --- | --- | --- |
| D1 | Radio | 8-channel LoRaWAN concentrator (SX1302 or SX1303 class), not a point-to-point LoRa receiver. Consistent with FieldNode's recommended LoRaWAN radio (FND REVIEW, item 1). | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |
| D2 | Computer | 4 GB Raspberry Pi 5 class board, not a 2 GB board. TWK-CAL-001 [G1, G2] shows the stack needs about 2.4 GB. | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |
| D3 | Database | TimescaleDB, rather than InfluxDB or SQLite. | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |
| D4 | Twin platform | Lightweight open-source stack plus a small TwinKit twin service, not Eclipse Ditto. | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |
| D5 | First example twin | FieldNode battery and solar charge. | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |
| D6 | Twin file schema | The YAML fields sketched in the precis: project, model, and per channel an id, node, part (BOM number), unit, expected value (constant, curve or calculation reference), tolerance and hold time. | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |
| D7 | Backup pack | Off-the-shelf 12.8 V LiFePO4 pack with a built-in BMS and fuse; a CellGuard-protected pack only in a later, larger version. | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |

*Table 2. Items that remain open.*

| # | Item | Status |
| --- | --- | --- |
| O1 | Budget. The TRL 2 review recommended raising `budget_usd` from $200 to $300 (option a), to keep LoRaWAN compatibility. Under the session instruction the budget is not changed: `budget_usd` stays at $200, and $300 is recorded as the recommended figure. TWK-CAL-001 [I2] states the $290 parts cost against both figures. The design is costed for option (a) because D1 (LoRaWAN) is adopted. | Proposed, awaiting Amish |
| O2 | Co-design partner outside the lab (a small water utility, a makerspace or a municipal team). No recommendation was made. | Proposed, awaiting Amish |

No reworded pitch or problem line was recommended, so `project.yaml` and `README.md` keep the existing wording.

## Consequences

- `project.yaml`: only the TRL fields change. `budget_usd` stays at $200.
- TWK-PRB-001, TWK-PRC-001 and TWK-REQ-001 are revised to v0.3. The design choices in D1 to D7 are no longer described as "proposed" but as adopted for TRL 3 pending Amish's review. No requirement target is relaxed or redefined as a result of these items; R14 keeps its $200 target until Amish decides O1.
- TWK-CAL-001 led to two changes within these choices: a 3.15 A time-delay input fuse in place of 2 A, and a UPS module with a buck-boost charger for the 12.8 V pack (parts cost now $290).
- Cross-repo: FieldNode sends 20-byte LoRaWAN uplinks every 15 min by default; TwinKit is sized for 5 min, which is conservative. CityTwin recommends costing the gateway in TwinKit, which matches this record. No conflict was found; see `docs/REVIEW.md`.
- TRL 4 is on hold by Amish's instruction. Nothing in this record authorizes building or testing.
