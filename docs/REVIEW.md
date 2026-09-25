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
