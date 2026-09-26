---
doc_id: TWK-DDR-002
title: TwinKit recommendations accepted
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
  change: Recommendations accepted by Amish (DDR-002)
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted

## Context

TWK-DDR-001 and `docs/REVIEW.md` (sessions of 2026-09-25) listed items that were adopted for TRL 3 pending Amish's review, or proposed and awaiting Amish, each with a recommendation. On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." Every item that carried a recommendation is therefore decided as recommended. Where a recommendation named one of several options, that option is the decision. Items with no recommendation stay open. TRL 4 remains on hold by Amish's instruction, and `trl` and `trl_target` stay at 3.

## Options considered

The options for each item are those listed in `docs/REVIEW.md` (TRL 2 and TRL 3 sessions) and in TWK-DDR-001.

## Decision

*Table 1. Items decided by Amish, 2026-09-25: go with recommendation.*

| # | Item | Decision | What changed in the repo |
| --- | --- | --- | --- |
| D1 | Radio | 8-channel LoRaWAN concentrator (SX1302 or SX1303 class) | Status wording only in TWK-PRC-001, TWK-PRB-001, TWK-DDR-001 and `bom/bom.csv`; no design change |
| D2 | Computer | 4 GB Raspberry Pi 5 class board | Status wording only |
| D3 | Database | TimescaleDB | Status wording only |
| D4 | Twin platform | Lightweight open-source stack plus a TwinKit twin service | Status wording only |
| D5 | First example twin | FieldNode battery and solar charge | Status wording only; cross-repo action for FieldNode (adaptive data rate, below) |
| D6 | Twin file schema | Project, model, and per channel an id, node, part (BOM number), unit, expected value, tolerance and hold time | Status wording only |
| D7 | Backup pack | Off-the-shelf 12.8 V LiFePO4 pack with built-in BMS and fuse | Status wording only |
| O1 | Budget | Option (a): raise the budget to $300 to keep LoRaWAN compatibility | `project.yaml` `budget_usd` 200 to 300; R14 target $200 to $300 (TWK-REQ-001 v0.4); R14 not met to met ($290); README budget line; TWK-PRB-001 constraint; `bom/bom-notes.md`; concept blueprint key figure |
| N1 | R1 at SF9 | Option (a): keep the 1 % target and require adaptive data rate so near nodes use SF7 or SF8 | R1 restated in TWK-REQ-001 v0.4; adaptive data rate added as a design rule in TWK-PRC-001 v0.4; TWK-CAL-001 v0.2 judges R1 on the SF7 to SF9 mix: 1.02 % (not met) to 0.21 % (met) [A6]; blueprint key figure updated |
| N2 | R12 load profile | Define R12 at the normal light load and schedule heavy database jobs for cool hours; a larger or metal enclosure is the fallback if tests show throttling | R12 restated in TWK-REQ-001 v0.4; cool-hours scheduling added as a design rule in TWK-PRC-001 v0.4; TWK-CAL-001 v0.2 [F6]: at risk to met (69.1 °C, 15.9 K margin at light load). The enclosure fallback depends on TRL 4 tests and is on hold |

No geometry changed, so `cad/src/model.py`, `bom/bom.csv` prices and drawing TWK-DWG-001 (Rev P1) are unchanged in content; the model, drawing and media were regenerated only for the site address change. No reworded pitch or problem line was recommended, so the `pitch` and `problem` text in `project.yaml` and `README.md` stay as they were.

*Table 2. Items still open.*

| # | Item | Status |
| --- | --- | --- |
| O2 | Co-design partner outside the lab (a small water utility, a makerspace or a municipal team). No recommendation was made. | Proposed, awaiting Amish |

## Consequences

- Requirement status (TWK-CAL-001 v0.2, Table 2): 0 not met, 0 at risk, 8 met by calculation, 7 met by design, 1 not verifiable at TRL 3 (R13, setup time). Before: 2 not met (R1, R14), 1 at risk (R12).
- The R14 margin is small ($10) and rests on indicative prices, not supplier quotes.
- R12 is met on assumed values for the processor's thermal resistance and throttle point; only a TRL 4 thermal test can confirm them.
- Cross-repo: FieldNode nodes must accept LoRaWAN adaptive data rate commands for R1 to hold. This is listed under "Cross-repo actions" in `docs/REVIEW.md`; no other repo was edited.
- TRL 4 work implied by these decisions (a timed setup trial, thermal and packet-loss tests, supplier quotes, a trial of the enclosure fallback) is decided in principle but on hold, because TRL 4 is on hold by Amish's instruction.
