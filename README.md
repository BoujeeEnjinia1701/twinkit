# TwinKit

![TRL 2](https://img.shields.io/badge/TRL-2%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Digital Twins · **TRL:** 2 of 9 (concept formulated) · **Prototype budget:** about $200 USD · **Difficulty:** 3 of 5

An open digital twin starter kit: a small edge gateway that collects readings from lab sensors (FieldNode and others), plus software that ties live data to each project's build123d model so it can be seen and compared with the design calculations.

## Concept rationale

Every lab project already has a parametric model and calculated targets; linking those to live readings closes the loop between design and reality at low cost.

## Burning platform

Operators of small infrastructure (village water, clinics, small factories) lack the monitoring that large operators take for granted, so faults are found late.

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| _To be developed_ | |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| _To be developed_ | |

## What sparked the idea

It came out of a September 2026 review of Design Molecule's applied research areas against the open projects already in the lab. Digital twins are a Design Molecule research area with no open project yet.

## Problem

Digital twins are sold as enterprise software, out of reach for small builders and cities, yet the idea is simple: a model, live data and a comparison between them.

## Concept

An open digital twin starter kit: a small edge gateway that collects readings from lab sensors (FieldNode and others), plus software that ties live data to each project's build123d model so it can be seen and compared with the design calculations.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Single-board computer gateway in DIN rail enclosure
- LoRa concentrator and Wi-Fi or cellular modem
- 12 V power input and backup cell
- Open-source time series database and dashboard stack
- Model-to-data mapping schema
- Example twin of one lab project

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> Low voltage only. Secure the gateway: change default credentials and keep it off public networks until it is hardened.

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (TWK-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `TWK-PRC-001/v1.0`.

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

A project of the [Design Molecule](https://designmolecule.com) lab. Shared components set.
