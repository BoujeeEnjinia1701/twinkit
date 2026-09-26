"""TwinKit parametric model (build123d), TRL 3, massing-plus level of detail.

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl:
    twinkit-assembly.step / .stl    bench plate, DIN rail and every gateway module
    gateway-enclosure.step / .stl   9-module enclosure with the computer, cooler, HAT, card and antenna

Axes: X along the TS35 DIN rail, Y across it, Z up, with the top of the bench plate at z = 0.
The same layout fits a vertical cabinet back plate; the bench case is the worst case for
natural ventilation (shortest vertical distance between the low and high vents).
Main dimensions and interfaces only: rail, module widths, enclosure envelope and vents,
board stack, antenna bulkhead, UPS and pack, terminals and fuse. Not fabrication detail;
not for fabrication. The same PARAMS feed docs/04-calcs/sizing.py (TWK-CAL-001) and the
drawing TWK-DWG-001 (cad/src/sheets.py).
"""
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    "module": 17.5,                     # DIN module pitch
    "rail": (320.0, 35.0, 7.5),         # 2 TS35 x 7.5 rail: length, width, height
    "plate": (360.0, 180.0, 6.0),       # 1 bench plate
    "gap": 2.0,                         # clearance between modules on the rail
    # 3, 4 gateway enclosure: modules, depth across the rail (Y), height above the rail (Z)
    "enc_modules": 9, "enc_d": 90.0, "enc_h": 60.0, "enc_wall": 2.5, "tray_h": 44.0,
    # vents: slots in both end walls, low row in the base and high row in the cover
    "vent_slot": (40.0, 4.0), "vent_rows_low": 2, "vent_rows_high": 2,
    "vent_z_low": 8.0, "vent_z_high": 50.0,          # slot centers above the rail top
    # 5 computer (85 x 56 board), 6 cooler, 7 HAT, 8 card
    "sbc": (85.0, 56.0, 1.6), "sbc_standoff": 6.0, "cooler": (40.0, 40.0, 8.0),
    "hat": (65.0, 56.0, 1.6), "hat_standoff": 16.0,
    # 9 antenna on an SMA bulkhead through the cover: whip length and diameter
    "antenna": (190.0, 12.0),
    # 10 DC-DC converter, 11 UPS module with 12 LiFePO4 pack inside it
    "psu_modules": 2, "ups_modules": 4, "pack": (60.0, 60.0, 40.0),
    # 13 terminal blocks (2 x 6.2 mm) and fuse holder (9 mm)
    "tb_w": 6.2, "fuse_w": 9.0, "tb_h": 40.0, "fuse_h": 50.0,
    "x_gw": -40.0,                      # enclosure center along the rail
}


def derived(p=PARAMS):
    """Dimensions the calc note and drawing quote, computed from PARAMS."""
    m = p["module"]
    enc_w = p["enc_modules"] * m
    rail_l, rail_w, rail_h = p["rail"]
    x_psu = p["x_gw"] + enc_w / 2 + p["gap"] + p["psu_modules"] * m / 2
    x_ups = x_psu + p["psu_modules"] * m / 2 + p["gap"] + p["ups_modules"] * m / 2
    x_tb0 = p["x_gw"] - enc_w / 2 - p["gap"]              # right edge of the terminal group
    tb_len = 2 * p["tb_w"] + p["fuse_w"] + 2 * p["gap"]
    used_l = (x_ups + p["ups_modules"] * m / 2) - (x_tb0 - tb_len)
    sw, sh = p["vent_slot"]
    vents = sw * sh * 2                                      # both end walls, one row
    d, h = p["enc_d"], p["enc_h"]
    return {
        "enc_w": enc_w, "x_psu": x_psu, "x_ups": x_ups, "x_tb0": x_tb0, "tb_len": tb_len,
        "rail_used_mm": used_l, "rail_used_modules": used_l / m,
        "rail_left": x_tb0 - tb_len, "rail_right": x_ups + p["ups_modules"] * m / 2,
        "vent_low_mm2": vents * p["vent_rows_low"], "vent_high_mm2": vents * p["vent_rows_high"],
        "vent_stack_mm": p["vent_z_high"] - p["vent_z_low"],
        # enclosure outer area without the face that sits on the rail
        "enc_area_m2": (2 * (enc_w * d + enc_w * h + d * h) - enc_w * d) / 1e6,
        "enc_top_z": rail_h + h,
        "antenna_top_z": rail_h + h + 6 + p["antenna"][0],
        "rail_z": rail_h,
    }


def _b():
    import build123d as b
    return b


def box(cx, cy, z0, sx, sy, sz):
    """Box with its base at z0."""
    b = _b()
    return b.Pos(cx, cy, z0 + sz / 2) * b.Box(sx, sy, sz)


def zcyl(x, y, z0, r, h):
    b = _b()
    return b.Pos(x, y, z0 + h / 2) * b.Cylinder(r, h)


def build_parts(p=PARAMS):
    """Return {key: solid} for BOM items 1 to 13."""
    D = derived(p)
    m, gap = p["module"], p["gap"]
    rl, rw, rh = p["rail"]
    pl, pw, pt = p["plate"]
    Z0 = rh
    xg, ew, ed, eh, t = p["x_gw"], D["enc_w"], p["enc_d"], p["enc_h"], p["enc_wall"]
    xc = (D["rail_left"] + D["rail_right"]) / 2
    parts = {}
    parts["plate"] = box(xc, 0, -pt, pl, pw, pt)
    parts["rail"] = box(xc, 0, 0, rl, rw, rh) - box(xc, 0, 1.0, rl + 1, rw - 10, rh)   # hat section

    # 3 enclosure base tray with low vents, 4 cover with high vents and the antenna bulkhead
    th = p["tray_h"]
    tray = box(xg, 0, Z0, ew, ed, th) - box(xg, 0, Z0 + t, ew - 2 * t, ed - 2 * t, th)
    cover = box(xg, 0, Z0 + th, ew, ed, eh - th) - box(xg, 0, Z0 + th - 1, ew - 2 * t, ed - 2 * t, eh - th - t + 1)
    sw, sh = p["vent_slot"]
    for side in (-1, 1):
        xw = xg + side * (ew / 2 - t / 2)
        for i in range(p["vent_rows_low"]):
            tray = tray - box(xw, 0, Z0 + p["vent_z_low"] - sh / 2 + (i - (p["vent_rows_low"] - 1) / 2) * 7, t + 2, sw, sh)
        for i in range(p["vent_rows_high"]):
            cover = cover - box(xw, 0, Z0 + p["vent_z_high"] - sh / 2 + (i - (p["vent_rows_high"] - 1) / 2) * 5, t + 2, sw, sh)
    parts["enc_base"] = tray
    parts["enc_cover"] = cover

    # 5 computer, 6 cooler, 7 concentrator HAT, 8 microSD
    bx = xg - 20
    sbc_z = Z0 + t + p["sbc_standoff"]
    sx, sy, sz = p["sbc"]
    parts["sbc"] = box(bx, 0, sbc_z, sx, sy, sz) + box(bx + 30, 0, sbc_z + sz, 18, 50, 14)
    cx_, cy_, cz_ = p["cooler"]
    parts["cooler"] = box(bx - 12, 0, sbc_z + sz, cx_, cy_, cz_)
    hat_z = sbc_z + sz + p["hat_standoff"]
    hx, hy, hz = p["hat"]
    parts["hat"] = box(bx - 10, 0, hat_z, hx, hy, hz) + box(bx - 10, 0, hat_z + hz, 52, 30, 5)
    parts["sd"] = box(bx - sx / 2 - 2.5, 0, sbc_z - 1.2, 15, 11, 1.2)

    # 9 antenna whip on an SMA bulkhead in the cover
    al, ad = p["antenna"]
    ax = bx - 10
    parts["antenna"] = zcyl(ax, 20, Z0 + eh, 7, 6) + zcyl(ax, 20, Z0 + eh + 6, ad / 2, al)

    # 10 DC-DC converter
    pw_ = p["psu_modules"] * m
    parts["psu"] = box(D["x_psu"], 0, Z0, pw_, ed, eh - 5) + box(D["x_psu"], 0, Z0 + eh - 5, pw_ - 6, 45, 5)

    # 11 UPS module shell and board, 12 LiFePO4 pack inside it
    uw = p["ups_modules"] * m
    xu = D["x_ups"]
    parts["ups"] = (box(xu, 0, Z0, uw, ed, eh) - box(xu, 0, Z0 + t, uw - 2 * t, ed - 2 * t, eh)
                    + box(xu, 34, Z0 + t, uw - 10, 12, 45))
    kx, ky, kz = p["pack"]
    parts["pack"] = box(xu, -8, Z0 + t, kx, ky, kz)

    # 13 terminal blocks and fuse holder, left of the enclosure
    x0 = D["x_tb0"]
    tw, fw = p["tb_w"], p["fuse_w"]
    parts["terminals"] = (box(x0 - tw / 2, 0, Z0, tw, 45, p["tb_h"])
                          + box(x0 - tw - gap / 2 - tw / 2, 0, Z0, tw, 45, p["tb_h"])
                          + box(x0 - 2 * tw - gap - fw / 2, 0, Z0, fw, 60, p["fuse_h"]))
    return parts


BOM_ORDER = [("plate", 1, "Bench mounting plate"), ("rail", 2, "DIN rail, TS35"),
             ("enc_base", 3, "Gateway enclosure base"), ("enc_cover", 4, "Gateway enclosure cover"),
             ("sbc", 5, "Single-board computer, 4 GB"), ("cooler", 6, "Active cooler"),
             ("hat", 7, "LoRaWAN concentrator HAT"), ("sd", 8, "microSD card, high endurance"),
             ("antenna", 9, "LoRa antenna and SMA bulkhead"), ("psu", 10, "DC-DC converter, 12 V to 5 V"),
             ("ups", 11, "DIN UPS module"), ("pack", 12, "LiFePO4 backup pack, 12.8 V"),
             ("terminals", 13, "Terminal blocks and fuse")]

ENCLOSURE_KEYS = ("enc_base", "enc_cover", "sbc", "cooler", "hat", "sd", "antenna")


def assembly(p=PARAMS):
    b = _b()
    return b.Compound(children=list(build_parts(p).values()))


if __name__ == "__main__":
    from build123d import Compound, export_step, export_stl
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True)
    (out / "stl").mkdir(exist_ok=True)
    P = build_parts()
    groups = {"twinkit-assembly": list(P.values()),
              "gateway-enclosure": [P[k] for k in ENCLOSURE_KEYS]}
    for name, shapes in groups.items():
        c = Compound(children=shapes)
        export_step(c, str(out / "step" / f"{name}.step"))
        export_stl(c, str(out / "stl" / f"{name}.stl"))
        bb = c.bounding_box()
        print(f"{name}: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm")
    D = derived()
    print(f"rail used {D['rail_used_mm']:.0f} mm ({D['rail_used_modules']:.1f} modules); enclosure "
          f"{D['enc_w']:.1f} x {PARAMS['enc_d']:.0f} x {PARAMS['enc_h']:.0f} mm, area {D['enc_area_m2']:.4f} m2; "
          f"vents {D['vent_low_mm2']:.0f} mm2 low, {D['vent_high_mm2']:.0f} mm2 high, {D['vent_stack_mm']:.0f} mm apart")
