# Review note: TwinKit

## Session 2026-09-25: /populate to a strong TRL 2

### What was done

- `docs/01-problem.md` (TWK-PRB-001 v0.2): problem with cited figures, prior work (Grieves and Vickers, ISO 23247, Eclipse Ditto, Virtual Singapore), users and context, constraints, out of scope, open questions.
- `docs/03-requirements.md` (TWK-REQ-001 v0.2): 16 measurable requirements (R1 to R16) with targets, status and planned verification.
- `docs/02-concept.md` (TWK-PRC-001 v0.2): how it works, main components, first-order numbers with assumptions, design choices, relation to FieldNode, CityTwin, CellGuard and CalRig, safety, open questions.
- `cad/src/concept_media.py`: massing model of the DIN rail gateway (13 BOM-numbered parts) with a desk and 14-inch laptop for scale, since the gateway is too small to read beside a 1.75 m figure.
- `media/`: `hero.png`, `concept-blueprint.png`/`.pdf`/`.svg`, `exploded.png`, `cutaway.png`, `flow.png` (data flow, values marked as estimates), `model.glb` and `viewer.html`.
- `bom/bom.csv`: 16 rows with indicative USD costs; rows 1 to 13 match the exploded view. `bom/bom-notes.md` updated.
- `README.md`: hero, links line, concept rationale, burning platform, use tables by industry and region, origin, concept, components and safety updated.
- `docs/pdf/`: branded PDFs of the three controlled documents.
- `project.yaml`: unchanged. The pitch and problem remain accurate.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Nodes served | 50 at 1 reading per 5 min, under 0.3 % loss at SF7 | R1 met |
| Storage | about 1.6 GB per year on a 64 GB card | R3 met |
| Reading to dashboard | under 5 s | R5 met |
| Average power | about 6 W at 12 V | R8 met |
| Backup | about 2 h | R9 met |
| Enclosure air rise | about 20 K above ambient | R12 not yet shown |
| Parts cost | about $285 | R14 **not met** ($200) |

Requirements not met or not shown: R14 (cost, about $285 against $200), R12 (thermal margin at 40 °C ambient, not yet shown), R13 (60 min setup, can only be shown by a timed trial at TRL 4).

### Proposed, awaiting Amish

Update 2026-09-25: items 1 to 8 are now **Decided by Amish, 2026-09-25: go with recommendation** (TWK-DDR-002). Item 9 had no recommendation and stays Proposed, awaiting Amish.

1. **Budget.** Parts cost about $285 against `budget_usd: 200`. Options: (a) raise the budget to $300; (b) keep $200 with a "lite" gateway using a point-to-point LoRa USB receiver instead of the LoRaWAN concentrator and a UPS HAT instead of the DIN UPS and pack (about $197, but no third-party LoRaWAN sensors); (c) keep $200 and drop the backup (about $235, still over). Recommendation: (a), because LoRaWAN compatibility is what lets CityTwin and third-party sensors use the kit.
2. **Radio.** 8-channel LoRaWAN concentrator (recommended) or point-to-point LoRa receiver. Must match FieldNode's radio choice.
3. **Computer.** 4 GB Raspberry Pi 5 class board (recommended) or a 2 GB board to save cost (tighter memory for the database).
4. **Database.** TimescaleDB (recommended, SQL and compression), InfluxDB, or SQLite (lightest).
5. **Twin platform.** Lightweight stack plus a small TwinKit service (recommended) or Eclipse Ditto (richer, heavier).
6. **First example twin.** FieldNode battery and solar charge (recommended), WaterWatch, or ThermaBrick.
7. **Twin file schema.** The YAML fields sketched in the precis (part by BOM number, expected value from the calculation note, tolerance, hold time).
8. **Backup pack.** Off-the-shelf 12.8 V LiFePO4 pack with built-in BMS (recommended) or a CellGuard-protected pack later.
9. **Co-design partner** outside the lab: a small water utility, a makerspace or a municipal team.

### Safety concerns

- LiFePO4 backup pack: use a pack with a built-in BMS and fuse; charge only through the UPS module.
- 12 V supply: certified mains adapter; any cabinet or mains-side wiring by a qualified electrician.
- Cybersecurity: default credentials, open ports and unpatched software are the main real-world risk for an edge gateway.
- Over-reliance: the twin is a monitoring aid and must not replace required alarms or protection.
- Thermal: a closed enclosure at 40 °C ambient may throttle the computer; not a fire risk at 6 W, but a reliability risk.

### Gaps against the brief

- The Pi and concentrator prices are indicative retail figures, not supplier quotes.
- `flow.png` shows the data path without loss branches, because the kit's loss arrows scale against numeric stage values and this flow uses text labels; uplink loss is given in the precis instead.

### Recommended next step

Review this note and the media, and decide the budget and radio questions first, since both change the BOM. If approved, run `/advance-trl3` to write the calculation note (airtime and loss, storage and card wear, power and backup, enclosure thermal check), a working build123d model with STEP export, a drawing sheet and a fully priced BOM.

## Session 2026-09-25: TRL 3

On 2026-09-25 Amish asked for this batch of repos to be taken through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed this repo's TRL 2 items one by one. This session ran `/advance-trl3` on that instruction and stopped at TRL 3.

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (TWK-DDR-001 v0.1, status proposed): seven recommendations adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review (D1 to D7), and two items left open (O1 budget, O2 co-design partner).
- `docs/04-calcs/01-sizing.md` (TWK-CAL-001 v0.1) and `docs/04-calcs/sizing.py`: LoRa airtime and ALOHA collision loss, storage and card wear, latency and flag timing, power, peak current and fuse, backup, enclosure and processor temperature, memory, rail length and cost, with a status for every requirement. The script imports the model's parameters and reads the BOM and `project.yaml`; every number in the note is printed by it with a tag.
- `cad/src/model.py`: parametric build123d model (plate, TS35 rail, 9-module enclosure base and cover with end vents, board, cooler, concentrator HAT, card, antenna on a bulkhead, DC-DC converter, UPS module with pack, terminals and fuse). Exports `cad/step/` and `cad/stl/` for `twinkit-assembly` and `gateway-enclosure`.
- `cad/src/sheets.py` and `cad/drawings/TWK-DWG-001.svg`, `.pdf`, `.png`: general arrangement at Rev P1, 1:5, marked "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION". TWK-DWG-001 was free because the concept blueprint is TWK-DWG-010.
- `bom/bom.csv` (16 lines, all priced with a supplier type, $290.00) and `bom/bom-notes.md`.
- `cad/src/concept_media.py` now builds from the model; all of `media/` was re-rendered and every image checked. The kit's default cutaway works for this model because it is centered near the origin; no workaround was needed. Temporary `media/_views*` folders were removed.
- TWK-PRB-001, TWK-PRC-001 and TWK-REQ-001 revised to v0.3; `README.md` (TRL badge, concept numbers, components, links) and `project.yaml` (`trl: 3`, `trl_target: 3`, evidence list) updated. PDFs rebuilt in `docs/pdf/`.

Design changes found necessary by the calculations, within the adopted choices: the input fuse rises from 2 A to 3.15 A time-delay (peak 2.29 A at 9 V), and the UPS module must have a buck-boost charger to charge the 12.8 V pack to 14.6 V from a 9 to 12 V input ($25 to $30). Batched database commits every 10 s are adopted in the twin service design to limit card wear.

### Requirement status (TWK-CAL-001, Table 2)

2 not met, 1 at risk, 5 met by calculation, 7 met by design, 1 not verifiable at TRL 3.

| ID | Status | Key number |
| --- | --- | --- |
| R1 Uplink loss | **Not met** (marginal) | 1.02 % at SF9 with all 50 nodes at 5 min (target under 1 %); 0.30 % at SF7, 0.56 % at SF8, 0.21 % for an SF7 to SF9 mix; 48 nodes meet it at SF9. The TRL 2 "met" claim rested on a low airtime figure |
| R14 Cost | **Not met** | $290.00 against $200 `budget_usd`; $10 within the recommended $300, awaiting Amish |
| R12 Thermal | At risk | Processor 69.1 °C at light load (15.9 K margin), 96.9 °C at sustained full load, vented, at 40 °C ambient; throttle point and thermal resistance assumed |
| R13 Setup time | Not verifiable at TRL 3 | Needs a timed trial |
| R3, R5, R8, R9, R10 | Met by calculation | 4.73 GB/yr on 56 GB free; 4.7 s worst latency; 6.41 W average; 2.40 h backup (1.63 h worst); 294 mm of rail |
| R2, R4, R6, R7, R11, R15, R16 | Met by design | R6 frame rate on a phone not verifiable at TRL 3; 7-day buffer 91 MB |

Key numbers: airtime 71.9 ms (SF7) to 1810.4 ms (SF12) for a 20-byte reading; 20.6 W peak input; 2.42 GB of 4 GB memory in use; card writes 35 to 53 GB a year.

### Decisions recorded (TWK-DDR-001)

Decided by Amish, 2026-09-25: go with recommendation (previously adopted for TRL 3 and open for his review): D1 8-channel LoRaWAN concentrator; D2 4 GB Pi 5 class board; D3 TimescaleDB; D4 lightweight stack plus a TwinKit service; D5 FieldNode battery and solar charge as the first example twin; D6 the YAML twin file fields sketched in the precis; D7 off-the-shelf LiFePO4 pack with built-in BMS. No reworded pitch or problem line was recommended, so `project.yaml` and `README.md` keep the existing wording.

### Still awaiting Amish

1. **O1, budget.** Decided by Amish, 2026-09-25: go with recommendation. `budget_usd` raised from $200 to $300 (TWK-DDR-002). The design ($290) is costed for the recommended option, since D1 keeps LoRaWAN.
2. **O2, co-design partner** outside the lab. No recommendation was made. Proposed, awaiting Amish.
3. **New, R1 at SF9.** Options: (a) keep the target and require adaptive data rate so near nodes use SF7 or SF8 (0.21 % for an even mix); (b) state the design point as 48 nodes at SF9 and 5 min, or 50 nodes at FieldNode's 15 min default (0.34 %); (c) relax the target to 1.5 %. Recommendation: (a), since it needs no hardware change. Decided by Amish, 2026-09-25: go with recommendation (TWK-DDR-002).
4. **New, R12 load profile.** Recommendation: define R12 at the normal light load and require heavy database jobs to run in cool hours, with a larger or metal enclosure as the fallback if tests show throttling. Decided by Amish, 2026-09-25: go with recommendation (TWK-DDR-002).

### Cross-repo consistency

- FieldNode (FND REVIEW): LoRaWAN radio, STM32WL-class module, 20-byte payload, 15 min default interval, TwinKit as the default gateway. TwinKit's airtime figures now match FieldNode's Table 3 (72 ms at SF7, 247 ms at SF9, 1.8 s at SF12). TwinKit is sized for 5 min, which is conservative. No conflict. Note: a FieldNode at SF9 and 5 min would exceed The Things Network's 30 s fair-use limit if moved to that public network; on a private TwinKit gateway only the EU868 1 % duty cycle applies (0.08 % used).
- CellGuard: not used at this size (D7); no interface assumed.
- CalRig: calibration records could set channel tolerances later; no interface assumed at TRL 3.
- CityTwin (not in the shared set, but it depends on TwinKit): its review recommends costing the gateway in TwinKit, which matches O1. Its sealed street cabinet in sun is hotter than the 40 °C case here, so R12 and the pack temperature need a separate check there.

### Safety concerns

- LiFePO4 pack: built-in BMS and fuse; charge only through the UPS module; the buck-boost charger must be set for LiFePO4 (14.6 V) and must not charge below 0 °C or above 45 °C.
- Input protection: the 3.15 A time-delay fuse sits at the supply input; wire sized for at least 3 A.
- 12 V supply: certified mains adapter; any cabinet or mains-side wiring by a qualified electrician.
- Thermal: a sealed or sun-exposed enclosure at 40 °C can drive the processor past its throttle point under heavy load; this is a reliability risk rather than a fire risk at these powers.
- Cybersecurity and over-reliance: default credentials, open ports and unpatched software remain the main real-world risk; the twin is a monitoring aid and does not replace required alarms or protection.

### Gaps and notes

- Prices are indicative, not supplier quotes. A WebFetch check of the Raspberry Pi 5 price was not approved in time, and a supplier page for a concentrator module returned a clearance price that did not look representative, so no price was changed on web evidence. No citations were flagged as unchecked in the TRL 2 note; none were added.
- Assumptions that only tests can settle: processor thermal resistance and throttle point, board and concentrator power, card write amplification and endurance, and the latency of each software stage.
- The GA sheet is at 1:5 because the antenna sets the height; the views are small but legible.
- Existing material beyond TRL 3: `build-log/README.md` (scaffold) is present, untouched and not extended. `firmware/` and `electronics/` hold only placeholders. No test, build or firmware material was created.

### Recommended next step

TRL 4 is on hold by Amish's instruction; this repo stops at TRL 3. Amish's review is needed on the budget (O1), the co-design partner (O2), and the new R1 and R12 proposals above. For the record only, TRL 4 would need: a bench build of the gateway; a lab test report (TST, `environment: lab`) covering packet loss with real FieldNodes at several spreading factors, measured power and backup time, processor temperature at 40 °C under light and heavy load, database size and card writes over a sustained run, and a timed setup trial for R13; and build log entries. None of this has been started.

## Session 2026-09-25: recommendations accepted

On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." Every TwinKit item with a recommendation is now **Decided by Amish, 2026-09-25: go with recommendation**, recorded in `docs/decisions/0002-recommendations-accepted.md` (TWK-DDR-002 v0.1). TWK-DDR-001 is revised to v0.2 with the new status.

### Decisions applied and what changed

| Item | Decision | Before | After |
| --- | --- | --- | --- |
| O1 Budget | Raise the budget (option a) | `budget_usd` $200; R14 not met ($290 against $200) | `budget_usd` $300; R14 target $300, met ($10 margin) |
| N1 R1 at SF9 | Require adaptive data rate (option a) | R1 not met: 1.02 % loss with all 50 nodes at SF9 | R1 restated with adaptive data rate; 0.21 % for an SF7 to SF9 mix, met [A6] |
| N2 R12 load profile | Define R12 at light load; heavy jobs in cool hours | R12 at risk (96.9 °C at sustained full load) | R12 restated; 69.1 °C at light load, 15.9 K margin, met [F6] |
| D1 to D7 | LoRaWAN concentrator, 4 GB board, TimescaleDB, lightweight stack, FieldNode example twin, twin file schema, off-the-shelf LiFePO4 pack | Adopted for TRL 3, open for review | Decided; status wording updated in TWK-PRB-001, TWK-PRC-001, TWK-DDR-001 and `bom/bom.csv` |

Files changed: `project.yaml` (`budget_usd` 300, DDR-002 added to evidence), `README.md` (budget, concept numbers, new "What sparked the idea"), TWK-PRB-001 v0.4, TWK-PRC-001 v0.4 (adaptive data rate and cool-hours rules added to the design), TWK-REQ-001 v0.4 (R1, R12, R14 restated), TWK-CAL-001 v0.2 and `docs/04-calcs/sizing.py` (new tags A6 and F6; R14 read against the $300 budget), `bom/bom-notes.md`, `bom/bom.csv` (status notes only, prices unchanged at $290.00), `cad/src/concept_media.py` (two key figures). No geometry changed, so TWK-DWG-001 stays at Rev P1; the model, drawing, media and PDFs were regenerated so that every generated file shows the designmolecule.com address. The "What sparked the idea" section now cites Apollo 13's ground simulator work (NASA) instead of a portfolio review.

### Requirement status (TWK-CAL-001 v0.2)

0 not met, 0 at risk, 8 met by calculation, 7 met by design, 1 not verifiable at TRL 3.

| ID | Status | Key number |
| --- | --- | --- |
| R13 Setup time | Not verifiable at TRL 3 | Needs a timed trial |
| R1, R3, R5, R8, R9, R10, R12, R14 | Met by calculation | 0.21 % loss with ADR; 4.73 GB/yr on 56 GB; 4.7 s latency; 6.41 W; 2.40 h backup; 294 mm rail; 69.1 °C processor at light load; $290 of $300 |
| R2, R4, R6, R7, R11, R15, R16 | Met by design | R6 frame rate not verifiable at TRL 3 |

R12 and R14 are met on thin evidence: R12 on an assumed thermal resistance and throttle point, R14 on indicative prices with a $10 margin.

### Still awaiting Amish

- **O2, co-design partner** outside the lab (small water utility, makerspace or municipal team). No recommendation was made. Proposed, awaiting Amish.

### Cross-repo actions

- **FieldNode:** nodes must accept LoRaWAN adaptive data rate commands so that R1 holds (TWK-REQ-001 v0.4, R1). Raise with FieldNode; FieldNode was not edited.
- **CityTwin:** its gateway now costs up to $300 in parts (TwinKit budget), and a sealed street cabinet in sun remains outside TwinKit's 40 °C light-load case for R12. Raise with CityTwin; CityTwin was not edited.

### TRL 4

TRL 4 remains on hold by Amish's instruction. Decided work that needs TRL 4 (timed setup trial for R13, thermal test to confirm R12, packet-loss test with adaptive data rate, supplier quotes for R14, and the larger or metal enclosure fallback) is recorded as decided but on hold. `trl` and `trl_target` stay at 3.

## Session 2026-09-26: photoreal renders

Amish asked on 2026-09-26 for photoreal renders across the portfolio, starting with the software and playbook repos (Group C). This repo has no new product model: the existing concept scene from `cad/src/concept_media.py` was rendered with Blender Cycles (`.kit/scene_export.py`, `.kit/photoreal.py`) on Amish's Mac and captioned with the project, repository and viewing direction.

- New: `media/render-hero.png`, `media/render-detail.png`. The README now leads with `media/render-hero.png`.
- Geometry, BOM, calculations and drawings are unchanged. `trl` stays 3; TRL 4 remains on hold.

## Session 2026-09-27: kit 1.5.0 and image quality

- Kit 1.5.0 synced: STANDARDS v1.5 (sections 12 to 15: product renders, storefront images and image quality, public release, authorship and signing), `.kit/cards.py`, `.kit/image_qc.py`, `.kit/release_gate.py`, issue templates, and the `/render-product` and `/release` commands. `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- Every `media/render-*.png` recaptioned from its original render with the new layout: the title, concept label and repository sit in a band above the render and the view note in a band below it, each line wrapped to the image width, so no text overlaps other text or the render or runs off the image. `media/card.png` and `media/social-preview.png` regenerated with the same rules.
- `python .kit/image_qc.py` and `python .kit/release_gate.py` pass. trl stays 3.

## Session 2026-10-02: design for construction and prototype build plan (kit 1.7.0)

Amish approved the build plan format on 2026-09-30 and asked for it across all repos, with outstanding decisions kept in a separate design decisions register. He also wrote on 2026-09-30: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." This session installed kit 1.7.0 and did that for TwinKit.

### What was done

- Kit 1.7.0 installed (`.kit/`, `.claude/commands/`); `CLAUDE.md` replaced by `.kit/CLAUDE.md`.
- `cad/src/model.py`: constructable model with 274 build123d checks (`python cad/src/model.py --check`, all pass): no overlaps, every part touching what holds it, clearances kept. STEP and STL regenerated.
- `docs/decisions/0003-design-for-construction.md` (TWK-DDR-003 v0.1, status proposed): every change, made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review.
- `cad/src/build_plan_media.py`: overview, 5 making sketches (TWK-DWG-101 to 105), 2 hole layouts, 7 joint close-ups, 17 assembly step pictures and a wiring diagram, all drawn from the model.
- `docs/05-build-plan.md` (TWK-BLD-001 v0.1) and `docs/06-design-decisions.md` (TWK-DEC-001 v0.1).
- `cad/drawings/TWK-DWG-001` Rev P3; concept media regenerated (`media/hero.png`, `exploded.png`, `cutaway.png`, `concept-blueprint.*`, `model.glb`, `viewer.html`).
- `bom/bom.csv` (lines 1, 2, 3, 11, 12 respecified; lines 17 to 21 added) and `bom/bom-notes.md`; `docs/04-calcs/sizing.py` and TWK-CAL-001 v0.3 (new tag [F7]; cost against the value-engineering target); TWK-REQ-001 v0.5, TWK-PRC-001 v0.5, TWK-PRB-001 v0.5; `README.md` (links line, "Building the prototype"); `project.yaml` (`design_state: constructable`, new evidence). PDFs rebuilt in `docs/pdf/`.

### Design changes made for construction (TWK-DDR-003)

| # | Change | Reason |
| --- | --- | --- |
| P1 | Backup pack moved out of the UPS module into its own 3-module battery box; UPS module 3 modules wide with no internal battery | Two bought parts cannot nest |
| P2 | Vent slots moved from the end walls to the long walls, same area and spacing | The end walls face neighbouring modules 2 mm away |
| P3 | Computer and HAT on 6 mm and 16 mm brass standoffs with a header extender | Both boards floated |
| P4 | SMA bulkhead through a 6.5 mm hole in the cover, pigtail to the HAT | The antenna sat on the cover with no hole |
| P5 | RJ45 feed-through coupler and an M16 two-hole gland in the front wall | No path for the network or power leads |
| P6 | True TS35 top-hat rail, 350 mm, on three M4 screws into tapped holes | U channel with no fixing |
| P7 | DIN clip hooks modelled on every module; two end stops | Modules could slide off |
| P8 | 6 mm aluminium plate, tapped, on four rubber feet, with corner holes | "Plywood or aluminium" could not hold the rail |
| P9 | USB-C power lead and a power-fail pair to the computer | No power or power-fail path into the enclosure |

### Key results

- Rail: 331 mm of modules (18.9 modules), 345 mm with end stops, on a 350 mm rail; R10 met.
- Thermal: unchanged design case (69.1 °C at light load); with the end walls counted as shielded, 72.8 °C, 12.2 K margin [F7]; R12 met.
- Cost: value-engineering target USD 300; estimated cost of the constructable design USD 334 (USD 34 over the target). The concept was USD 290.
- Requirements: none not met, none at risk, 7 met by calculation, 7 met by design, R13 not verifiable at TRL 3, R14 reported against its target.

### Proposed, awaiting Amish

All in TWK-DEC-001: accept the TWK-DDR-003 changes (recommended); the region and radio band, to match FieldNode's pilot region; the co-design partner (no recommendation). Eight purchase checks are listed there.

### Stale media

The photoreal renders (`media/render-hero.png`, `media/render-detail.png`), `media/card.png` and `media/social-preview.png` show the concept: the pack inside the UPS, vents in the end walls, no battery box or end stops. They need regenerating on Amish's Mac; `media/render-hero.png` and `media/render-detail.png` are also absent from this cloud copy.

### Safety

No change to the safety case. The pack, its BMS and fuse, and the charge path through the UPS module are unchanged; the build plan adds safety stops before the adapter is plugged in, before the pack is connected, for the first charge, before the radio transmits and before the gateway joins a wider network.

### Recommended next step

Amish to review TWK-DDR-003 and the register. TRL 4 (building and testing to TWK-BLD-001) remains on hold.

## Session 2026-10-02: open decisions decided

Amish, 2026-10-02: "APPROVED: The open decisions from the last wave (TremorTrace to ZeerBox) came in after the review and aren't on the page either." This approves the recommendation written for each open decision in the design decisions register (TWK-DEC-001), as he did for the other 555 open decisions ("i approve your recommendations for all 555 open decisions."). trl stays 3; no build or test work was done, and the model, BOM quantities and prices, and pictures are unchanged.

### Decisions recorded

Three decisions, all moved to Decisions made in TWK-DEC-001, dated 2026-10-02:

1. Design for construction accepted: the changes P1 to P9 of TWK-DDR-003, as made.
2. Region and radio band of the first build: US915, with the US915 concentrator HAT and a 915 MHz antenna, to match FieldNode's decided first variant.
3. Co-design partner outside the lab: the first candidate to approach for the operator view is a small municipal water utility in the Dallas and Fort Worth area, found through the Texas Water Utilities Association, with Dallas Makerspace as the build and test partner.

### Documents changed

- `docs/06-design-decisions.md` (TWK-DEC-001 v0.2): open decisions moved to Decisions made.
- `docs/decisions/0003-design-for-construction.md` (TWK-DDR-003 v0.2): acceptance recorded in the status line (record stays Draft).
- `docs/decisions/0001-trl2-review-decisions.md` (TWK-DDR-001 v0.3) and `docs/decisions/0002-recommendations-accepted.md` (TWK-DDR-002 v0.2): O2 recorded as decided.
- `docs/01-problem.md` (TWK-PRB-001 v0.6): co-design partner question answered.
- `docs/02-concept.md` (TWK-PRC-001 v0.6): concentrator row names US915 for the first build; partner open question answered.
- `bom/bom.csv` (line 7 specification text only, no quantity or price change) and `bom/bom-notes.md`: US915 for the first build.

### Follow-up actions to carry approved decisions into the design

1. Decision 2 (calculations): Restate the regulatory air-time check in TWK-CAL-001 for US915 (400 ms dwell time per channel, no 1 % duty cycle) alongside the EU868 figure, and confirm the result for nodes at SF9 every 5 min.
2. Decision 2 (BOM): Price the US915 concentrator HAT and a 915 MHz antenna from a named supplier for lines 7 and 9.
3. Decision 2 (docs): Name US915 in the build plan's concentrator and antenna descriptions and in safety stop S5 when the build plan is next revised.
4. Decision 3 (docs): Approach a small municipal water utility in the Dallas and Fort Worth area through the Texas Water Utilities Association, and Dallas Makerspace for the build.

### Points found in the review

- Item 2 depends on FND-DDR-001 O1, which is no longer open: FieldNode decided US915 as its default first variant on 2026-10-02.
- BOM line 7 still reads 'EU868 or US915 version to suit region'; with item 2 decided it should name US915 (text only, price unchanged).

## Session 2026-10-02: approved follow-ups carried out

Amish approved all follow-up actions from the open-decision sign-off on 2026-10-02. No CAD model, drawing or picture changed. TwinKit is a scene-render repo with no `cad/src/product_model.py`, and none was created: the hero is the scene render, as before. The model is unchanged, so the scene was exported from `cad/src/concept_media.py` with `.kit/scene_export.py` (`export_views.py` needs a product model).

### Approved follow-ups carried out

1. Decision 2, calculations: done. `docs/04-calcs/sizing.py` prints a new tag [A7] and TWK-CAL-001 v0.4 restates the air-time check for US915: a 246.8 ms frame at SF9 every 5 min is 62 % of the 400 ms dwell time per channel and 71 s of air per day, with no duty-cycle limit; SF10 (452.6 ms) would exceed the dwell time, so the SF7 to SF9 range used for R1 is inside the limit. The EU868 figure stays alongside. R1 is unchanged.
2. Decision 2, BOM: partly done. Line 7 is priced from the Seeed Studio WM1302 SPI US915 module and Seeed WM1302 Raspberry Pi HAT (HAT USD 20.79 at RobotShop; module USD 39 list at a reseller, about USD 60 for the parts) and kept at USD 80 for shipping from two sellers and a HAT that fits the Pi 5 class computer (Seeed lists the HAT for boards up to the Pi 4B). Line 9 stays at USD 12: a named supplier price for the 915 MHz antenna was not found. Both are indicative, not quoted.
3. Decision 2, docs: done. TWK-BLD-001 v0.2 names US915 and the 915 MHz band in the concentrator and antenna descriptions and in safety stop S5.
4. Decision 3, approach the municipal water utility and Dallas Makerspace: not done, outreach by Amish.
5. Render scene: exported to `/home/claude/renders/twinkit` (view hero: `twinkit__hero.npz` and `.json`, plus `twinkit__jobs.json`). Photoreal render, card and social preview are made on Amish's Mac.

### Results

- Requirement status changes: none.
- Value-engineering target: USD 300. Estimated cost of the constructable design: USD 334 (USD 34 over the target). `budget_usd` is unchanged. Mass is not tracked in this repo.

### Documents changed

- `docs/04-calcs/01-sizing.md` (TWK-CAL-001 v0.4), `docs/05-build-plan.md` (TWK-BLD-001 v0.2)
- `bom/bom.csv` and `bom/bom-notes.md`, `docs/04-calcs/sizing.py`

### Cross-repo actions

None.

## 2026-10-02: photoreal renders redone on the constructable design

Rendered with Blender Cycles on Amish's Mac from the updated appearance model; captioned with `.kit/photo_caption.py`; `media/card.png` and `media/social-preview.png` regenerated with `.kit/cards.py`. Views: hero. image_qc passes. Appearance deviations are those logged above as proposed, awaiting Amish.
