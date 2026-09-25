"""TwinKit concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

The physical part of TwinKit is a small edge gateway on a DIN rail, mounted on a
bench plate. The rest of the kit is software; its data flow is shown in media/flow.png.
Coordinates in mm: X along the DIN rail, Y across it, Z up. The plate top is at z = 0.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Pos, Rot
from concept import Part, render_all

MOD = 17.5                      # DIN module width (mm)
RAIL_H = 7.5                    # TS35 rail height
ENC_W, ENC_D, ENC_H = 9 * MOD, 90.0, 60.0   # 9-module gateway enclosure
WALL = 2.5
Z0 = RAIL_H                     # enclosures sit on the rail
X_GW = -40.0                    # gateway enclosure center (X)
X_PSU = X_GW + ENC_W / 2 + 2 + MOD            # 2-module DC-DC converter
X_UPS = X_PSU + MOD + 2 + 2 * MOD             # 4-module UPS with LiFePO4 pack
X_TB = X_GW - ENC_W / 2 - 14.0                # terminal blocks and fuse


def box_at(x, y, z0, w, d, h):
    """Box with its base at z0."""
    return Pos(x, y, z0 + h / 2) * Box(w, d, h)


# 1 Bench mounting plate and 2 DIN rail
plate = Pos(5, 0, -3) * Box(360, 180, 6)
rail = box_at(5, 0, 0, 320, 35, RAIL_H)

# 3 Gateway enclosure: base tray and 4 clear cover
tray_h = 44.0
tray = box_at(X_GW, 0, Z0, ENC_W, ENC_D, tray_h) - box_at(X_GW, 0, Z0 + WALL, ENC_W - 2 * WALL, ENC_D - 2 * WALL, tray_h)
cover_h = ENC_H - tray_h
cover = (box_at(X_GW, 0, Z0 + tray_h, ENC_W, ENC_D, cover_h)
         - box_at(X_GW, 0, Z0 + tray_h - 1, ENC_W - 2 * WALL, ENC_D - 2 * WALL, cover_h - WALL + 1))

# 5 Single-board computer (85 x 56 mm) with 6 active cooler, 7 LoRaWAN concentrator HAT
sbc_z = Z0 + WALL + 6.0
sbc = box_at(X_GW - 20, 0, sbc_z, 85, 56, 1.6) + box_at(X_GW - 20 + 30, 0, sbc_z + 1.6, 18, 50, 14)   # board plus USB/Ethernet block
cooler = box_at(X_GW - 20 - 12, 0, sbc_z + 1.6, 40, 40, 8)
hat_z = sbc_z + 1.6 + 16.0
hat = box_at(X_GW - 20 - 10, 0, hat_z, 65, 56, 1.6) + box_at(X_GW - 20 - 10, 0, hat_z + 1.6, 52, 30, 5)
# 8 microSD card sits in the SBC edge: shown as a small block
sd = box_at(X_GW - 20 - 45, 0, sbc_z - 1.2, 15, 11, 1.2)

# 9 Antenna on an SMA bulkhead through the cover
ant_x = X_GW - 20 - 10
antenna = Pos(ant_x, 20, Z0 + ENC_H + 95) * Cylinder(6, 190) + Pos(ant_x, 20, Z0 + ENC_H + 3) * Cylinder(7, 6)

# 10 12 V to 5 V DC-DC converter (2 modules)
psu = box_at(X_PSU, 0, Z0, 2 * MOD, ENC_D, ENC_H - 5) + box_at(X_PSU, 0, Z0 + ENC_H - 5, 2 * MOD - 6, 45, 5)

# 11 DIN UPS module and 12 LiFePO4 backup pack (4 modules together)
ups_shell = (box_at(X_UPS, 0, Z0, 4 * MOD, ENC_D, ENC_H)
             - box_at(X_UPS, 0, Z0 + WALL, 4 * MOD - 2 * WALL, ENC_D - 2 * WALL, ENC_H))
pack = box_at(X_UPS, -8, Z0 + WALL, 4 * MOD - 10, 60, 40)
ups_board = box_at(X_UPS, 34, Z0 + WALL, 4 * MOD - 10, 12, 45)

# 13 Terminal blocks and fuse holder
tb = (box_at(X_TB, 0, Z0, 6.2, 45, 40) + box_at(X_TB - 7, 0, Z0, 6.2, 45, 40)
      + box_at(X_TB - 16, 0, Z0, 9, 60, 50))

parts = [
    Part("Bench mounting plate", plate, "#C8A97E", 1, (0, 0, -60)),
    Part("DIN rail, TS35", rail, "#A8AFB7", 2, (0, 0, -30)),
    Part("Gateway enclosure base", tray, "#E5E7EB", 3, (0, 0, 0)),
    Part("Gateway enclosure cover", cover, "#BFE3DE", 4, (0, 0, 190)),
    Part("Single-board computer, 4 GB", sbc, "#15803D", 5, (0, 0, 55)),
    Part("Active cooler", cooler, "#4B5563", 6, (0, -70, 80)),
    Part("LoRaWAN concentrator HAT", hat, "#0F766E", 7, (0, 0, 120)),
    Part("microSD card, high endurance", sd, "#1F2937", 8, (0, -110, 20)),
    Part("LoRa antenna and SMA bulkhead", antenna, "#374151", 9, (0, 0, 190)),
    Part("DC-DC converter, 12 V to 5 V", psu, "#6B7280", 10, (40, 0, 0)),
    Part("DIN UPS module", ups_shell, "#D1D5DB", 11, (90, 0, 0)),
    Part("LiFePO4 backup pack, 12.8 V", pack + ups_board, "#C2410C", 12, (90, 0, 110)),
    Part("Terminal blocks and fuse", tb, "#D4A017", 13, (-50, 0, 0)),
]

# Context for scale: desk and a 14-inch laptop showing the twin dashboard
desk = Pos(130, 60, -6 - 12.5) * Box(760, 420, 25)
lap_x, lap_y = 360, 90
lap_base = Pos(lap_x, lap_y, -6 + 9) * Box(320, 220, 18)
lap_screen = Pos(lap_x, lap_y + 110 + 25, -6 + 18 + 100) * Rot(-15, 0, 0) * Box(320, 7, 210)
context = [Part("Desk", desk, "#D6D9DE"), Part("14-inch laptop", lap_base + lap_screen, "#8B929B")]

render_all(
    parts, project="TwinKit", title="Edge gateway concept", dwg_no="TWK-DWG-010",
    key_figures=["Up to 50 sensor nodes at 1 reading per 5 min (target)",
                 "About 6 W average at 12 V (estimate)",
                 "About 2 h backup on a 12.8 V, 1.5 Ah LiFePO4 pack (estimate)",
                 "About 1.6 GB per year for 50 nodes (estimate)",
                 "About $285 in parts vs $200 budget (indicative)",
                 "Works offline; no vendor cloud account"],
    scale_figure=False, context=context,
    cut_exclude=("LoRa antenna and SMA bulkhead", "Bench mounting plate"),
    flow={"title": "data flow from sensor to twin (values are estimates)", "unit": "",
          "stages": [("Sensor nodes", "50 x 1 per 5 min"), ("Concentrator", "8 ch LoRaWAN"),
                     ("Network server", "MQTT, under 1 s"), ("Time-series DB", "about 1.6 GB/yr"),
                     ("Twin service", "model + calc"), ("Dashboard, 3D", "residual flags")]},
)
