"""TwinKit concept media (TRL 3), built from the parametric model in cad/src/model.py.

Run from the repo root:  python cad/src/concept_media.py
Geometry comes from model.py (PARAMS); not for fabrication.

The physical part of TwinKit is a small edge gateway on a DIN rail, mounted on a
bench plate. The rest of the kit is software; its data flow is shown in media/flow.png.
Coordinates in mm: X along the DIN rail, Y across it, Z up. The plate top is at z = 0.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build123d import Box, Pos, Rot  # noqa: E402
from concept import Part, render_all  # noqa: E402

from model import PARAMS, BOM_ORDER, build_parts  # noqa: E402

COLORS = {"plate": "#C8A97E", "rail": "#A8AFB7", "enc_base": "#E5E7EB", "enc_cover": "#BFE3DE",
          "sbc": "#15803D", "cooler": "#4B5563", "hat": "#0F766E", "sd": "#1F2937", "antenna": "#374151",
          "psu": "#6B7280", "ups": "#D1D5DB", "pack": "#C2410C", "terminals": "#D4A017"}
EXPLODE = {"plate": (0, 0, -60), "rail": (0, 0, -30), "enc_base": (0, 0, 0), "enc_cover": (0, 0, 190),
           "sbc": (0, 0, 55), "cooler": (0, -70, 80), "hat": (0, 0, 120), "sd": (0, -110, 20),
           "antenna": (0, 0, 190), "psu": (40, 0, 0), "ups": (90, 0, 0), "pack": (90, 0, 110),
           "terminals": (-50, 0, 0)}

P = build_parts(PARAMS)
parts = [Part(name, P[key], COLORS[key], n, EXPLODE[key]) for key, n, name in BOM_ORDER]

# Context for scale: desk and a 14-inch laptop showing the twin dashboard
desk = Pos(130, 60, -6 - 12.5) * Box(760, 420, 25)
lap_x, lap_y = 360, 90
lap_base = Pos(lap_x, lap_y, -6 + 9) * Box(320, 220, 18)
lap_screen = Pos(lap_x, lap_y + 110 + 25, -6 + 18 + 100) * Rot(-15, 0, 0) * Box(320, 7, 210)
context = [Part("Desk", desk, "#D6D9DE"), Part("14-inch laptop", lap_base + lap_screen, "#8B929B")]

render_all(
    parts, project="TwinKit", title="Edge gateway concept", dwg_no="TWK-DWG-010",
    key_figures=["50 nodes at 1 reading per 5 min; 0.21 % loss with ADR (TWK-CAL-001)",
                 "6.4 W average at 12 V; 20.6 W peak; 3.15 A T fuse",
                 "2.4 h backup on a 12.8 V, 1.5 Ah LiFePO4 pack",
                 "4.7 GB per year for 50 nodes, uncompressed",
                 "$290 in parts within the $300 budget",
                 "Works offline; no vendor cloud account"],
    scale_figure=False, context=context,
    cut_exclude=("LoRa antenna and SMA bulkhead", "Bench mounting plate"),
    flow={"title": "data flow from sensor to twin (values are TRL 3 estimates, TWK-CAL-001)", "unit": "",
          "stages": [("Sensor nodes", "50 x 1 per 5 min"), ("Concentrator", "8 ch LoRaWAN"),
                     ("Network server", "MQTT, under 5 s"), ("TimescaleDB", "4.7 GB/yr (calc)"),
                     ("Twin service", "model + calc"), ("Dashboard, 3D", "residual flags")]},
)
