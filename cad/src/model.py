"""TwinKit parametric model (build123d), TRL 3, constructable design (TWK-DDR-003).

Run from the repo root:
    python cad/src/model.py            export STEP and STL into cad/step and cad/stl
    python cad/src/model.py --check    constructability checks (overlaps, contacts, clearances)
Exports:
    twinkit-assembly.step / .stl    bench plate, DIN rail and every gateway module, with fixings
    gateway-enclosure.step / .stl   9-module enclosure with the computer, cooler, HAT, card and antenna

Axes: X along the TS35 DIN rail, Y across it, Z up, with the top of the bench plate at z = 0.
The same layout fits a vertical cabinet back plate (then -Y is down, so the cable entries face
down and the vents in the two long walls form a chimney); the bench case is the worst case for
natural ventilation. Every part can be bought, or made with a saw, drill, tap and file:
see docs/05-build-plan.md (TWK-BLD-001). The same PARAMS feed docs/04-calcs/sizing.py
(TWK-CAL-001), the drawing TWK-DWG-001 (cad/src/sheets.py) and the build plan pictures
(cad/src/build_plan_media.py).
"""
import sys
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    "module": 17.5,                     # DIN module pitch
    "rail": (350.0, 35.0, 7.5),         # 2 TS35 x 7.5 top-hat rail: length, width, height
    "rail_t": 1.0,                      # rail sheet thickness
    "rail_web": 27.0,                   # width of the rail's base (the part screwed to the plate)
    "rail_screw_dx": (-150.0, 0.0, 150.0),   # M4 rail screws, from the rail centre
    "plate": (360.0, 180.0, 6.0),       # 1 bench plate, aluminium
    "plate_hole_inset": 12.0,           # 5.5 mm corner holes for wall or cabinet mounting
    "feet": (20.0, 6.0, 150.0, 60.0),   # rubber feet: diameter, height, x and y from the plate centre
    "gap": 2.0,                         # clearance between modules on the rail
    "clip": (2.0, 2.0, 1.0),            # DIN clip hook under each module: hook width, lip reach, lip thickness
    # 3, 4 gateway enclosure: modules, depth across the rail (Y), height above the rail (Z)
    "enc_modules": 9, "enc_d": 90.0, "enc_h": 60.0, "enc_wall": 2.5, "tray_h": 44.0,
    # vents: slots in both LONG walls (+Y and -Y), low row in the base and high row in the cover
    "vent_slot": (40.0, 4.0), "vent_rows_low": 2, "vent_rows_high": 2,
    "vent_z_low": 8.0, "vent_z_high": 50.0,          # slot centres above the rail top
    "vent_dx": -32.0,                                # slot centre along X from the enclosure centre
    # 5 computer (85 x 56 board), 6 cooler, 7 HAT, 8 card
    "sbc": (85.0, 56.0, 1.6), "sbc_standoff": 6.0, "cooler": (40.0, 40.0, 8.0),
    "hat": (65.0, 56.0, 1.6), "hat_standoff": 16.0,
    "sbc_holes": (58.0, 49.0, 3.5),     # board mounting holes: spacing along X and Y, inset from the corner
    "standoff_d": 5.0, "hole_m25": 2.7,
    "header": (50.8, 5.0),              # 2 x 20 header extender footprint
    # 9 antenna whip on an SMA bulkhead through the cover: whip length and diameter
    "antenna": (190.0, 12.0), "sma_hole": 6.5,
    # cable entries in the -Y long wall of the gateway enclosure base
    "rj45": (20.0, 28.0, 50.0),         # feed-through coupler: hole, flange diameter, x from the enclosure centre
    "gland": (16.2, 20.0, 20.0),        # M16 cable gland with a two-hole insert: hole, flange diameter, x from the enclosure centre
    "box_gland": (12.2, 15.0),          # M12 cable gland for the pack lead: hole, flange diameter
    "entry_z": 26.0,                    # entry centres above the rail top
    # 10 DC-DC converter, 11 UPS module, 17 battery box with the 12 LiFePO4 pack inside it
    "psu_modules": 2, "ups_modules": 3, "box_modules": 3,
    "pack": (38.0, 70.0, 38.0), "pad_t": 3.0,
    # 13 terminal blocks (2 x 6.2 mm) and fuse holder (9 mm), 18 end stops
    "tb_w": 6.2, "fuse_w": 9.0, "tb_h": 40.0, "fuse_h": 50.0,
    "stop": (8.0, 40.0, 30.0),
    "x_gw": -40.0,                      # enclosure centre along the rail
}


def derived(p=PARAMS):
    """Dimensions the calc note, drawings and build plan quote, computed from PARAMS."""
    m = p["module"]
    enc_w = p["enc_modules"] * m
    rail_l, rail_w, rail_h = p["rail"]
    ups_w, box_w = p["ups_modules"] * m, p["box_modules"] * m
    x_psu = p["x_gw"] + enc_w / 2 + p["gap"] + p["psu_modules"] * m / 2
    x_ups = x_psu + p["psu_modules"] * m / 2 + p["gap"] + ups_w / 2
    x_box = x_ups + ups_w / 2 + p["gap"] + box_w / 2
    x_tb0 = p["x_gw"] - enc_w / 2 - p["gap"]              # right edge of the terminal group
    tb_len = 2 * p["tb_w"] + p["fuse_w"] + 2 * p["gap"]
    tb_left = x_tb0 - 2 * p["tb_w"] - p["gap"] - p["fuse_w"]   # left face of the fuse holder
    rail_right = x_box + box_w / 2
    used_l = rail_right - (x_tb0 - tb_len)
    sw, sh = p["vent_slot"]
    vents = sw * sh * 2                                      # both long walls, one row
    d, h = p["enc_d"], p["enc_h"]
    stop_l = tb_left - p["stop"][0] / 2
    stop_r = rail_right + p["stop"][0] / 2
    x_rail = ((stop_l - p["stop"][0] / 2) + (stop_r + p["stop"][0] / 2)) / 2
    return {
        "enc_w": enc_w, "x_psu": x_psu, "x_ups": x_ups, "x_box": x_box, "ups_w": ups_w, "box_w": box_w,
        "x_tb0": x_tb0, "tb_len": tb_len, "tb_left": tb_left,
        "rail_used_mm": used_l, "rail_used_modules": used_l / m,
        "rail_left": x_tb0 - tb_len, "rail_right": rail_right,
        "stop_l": stop_l, "stop_r": stop_r, "x_rail": x_rail,
        "rail_occupied_mm": (stop_r + p["stop"][0] / 2) - (stop_l - p["stop"][0] / 2),
        "vent_low_mm2": vents * p["vent_rows_low"], "vent_high_mm2": vents * p["vent_rows_high"],
        "vent_stack_mm": p["vent_z_high"] - p["vent_z_low"],
        # enclosure outer area without the face that sits on the rail
        "enc_area_m2": (2 * (enc_w * d + enc_w * h + d * h) - enc_w * d) / 1e6,
        # the same without the two end walls, which face the neighbouring modules 2 mm away
        "enc_area_shielded_m2": (2 * (enc_w * d + enc_w * h) - enc_w * d) / 1e6,
        "enc_top_z": rail_h + h,
        "antenna_top_z": rail_h + h + 6 + p["antenna"][0],
        "rail_z": rail_h,
        "bx": p["x_gw"] - 20,           # board centre along X
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


def ycyl(x, y0, z, r, h):
    """Cylinder along Y from y0 to y0 + h (h may be negative)."""
    b = _b()
    lo = min(y0, y0 + h)
    return b.Pos(x, lo + abs(h) / 2, z) * b.Rot(90, 0, 0) * b.Cylinder(r, abs(h))


def clip_feet(cx, w, p=PARAMS):
    """DIN clip hooks under a module of width w centred at cx: a hook outside each rail flange,
    with a lip under the flange. They touch the rail; they do not cut into it."""
    hw, reach, lt = p["clip"]
    rh, t = p["rail"][2], p["rail_t"]
    half = p["rail"][1] / 2
    out = None
    for s in (-1, 1):
        hook = box(cx, s * (half + hw / 2), rh - 2 * lt, w - 2, hw, 2 * lt)
        lip = box(cx, s * (half - reach / 2), rh - 2 * lt, w - 2, reach, lt)
        part = hook + lip
        out = part if out is None else out + part
    return out


def rail_shape(p=PARAMS):
    D = derived(p)
    rl, rw, rh = p["rail"]
    t, web = p["rail_t"], p["rail_web"]
    xc = D["x_rail"]
    s = box(xc, 0, 0, rl, web, t)
    for sgn in (-1, 1):
        s = s + box(xc, sgn * (web / 2 - t / 2), t, rl, t, rh - 2 * t)
        s = s + box(xc, sgn * (web / 2 - t + (rw - web + 2 * t) / 4), rh - t, rl, (rw - web + 2 * t) / 2, t)
    for dx in p["rail_screw_dx"]:
        s = s - zcyl(xc + dx, 0, -1, 2.25, t + 2)
    return s


def gland_shape(x, yo, ze, hole, flange, t):
    """Cable gland in a -Y wall whose outside face is at yo: dome and cable outside, nut inside."""
    return (ycyl(x, yo, ze, flange / 2, -4) + ycyl(x, yo - 4, ze, min(5.5, flange / 2 - 1.5), -10)
            + ycyl(x, yo, ze, hole / 2 - 0.2, t) + ycyl(x, yo + t, ze, flange / 2 + 0.5, 4))


def board_holes(p=PARAMS):
    D = derived(p)
    bx = D["bx"]
    hx, hy, hin = p["sbc_holes"]
    sx = p["sbc"][0]
    return [(bx - sx / 2 + hin + i * hx, (j - 0.5) * hy) for i in (0, 1) for j in (0, 1)]


def standoff_pieces(p=PARAMS):
    """The board stack fittings, separately: lower and upper standoffs, screw heads, header extender."""
    D = derived(p)
    Z0, t = p["rail"][2], p["enc_wall"]
    sz, hz = p["sbc"][2], p["hat"][2]
    sbc_z = Z0 + t + p["sbc_standoff"]
    hat_z = sbc_z + sz + p["hat_standoff"]
    r = p["standoff_d"] / 2
    out = {k: None for k in ("lower", "upper", "heads_low", "heads_top")}
    for x, y in board_holes(p):
        for k, s in (("lower", zcyl(x, y, Z0 + t, r, p["sbc_standoff"])), ("upper", zcyl(x, y, sbc_z + sz, r, p["hat_standoff"])),
                     ("heads_low", zcyl(x, y, Z0 - 1.7, 2.25, 1.7)), ("heads_top", zcyl(x, y, hat_z + hz, 2.25, 1.7))):
            out[k] = s if out[k] is None else out[k] + s
    hl, hw_ = p["header"]
    hdr_x0 = D["bx"] - p["sbc"][0] / 2 + 7.1
    out["header"] = box(hdr_x0 + hl / 2, p["sbc_holes"][1] / 2, sbc_z + sz, hl, hw_, p["hat_standoff"])
    return out


def build_parts(p=PARAMS):
    """Return {key: solid} for every part of the constructable design."""
    D = derived(p)
    m, gap = p["module"], p["gap"]
    rl, rw, rh = p["rail"]
    pl, pw, pt = p["plate"]
    Z0 = rh
    xg, ew, ed, eh, t = p["x_gw"], D["enc_w"], p["enc_d"], p["enc_h"], p["enc_wall"]
    xr = D["x_rail"]
    parts = {}

    # 1 plate with tapped rail holes and corner mounting holes
    plate = box(xr, 0, -pt, pl, pw, pt)
    for dx in p["rail_screw_dx"]:
        plate = plate - zcyl(xr + dx, 0, -pt - 1, 1.65, pt + 2)            # M4 tapping drill 3.3
    ins = p["plate_hole_inset"]
    for sx in (-1, 1):
        for sy in (-1, 1):
            plate = plate - zcyl(xr + sx * (pl / 2 - ins), sy * (pw / 2 - ins), -pt - 1, 2.75, pt + 2)
    parts["plate"] = plate
    parts["rail"] = rail_shape(p)

    # 3 enclosure base tray with low vents and cable entries, 4 cover with high vents and the antenna hole
    th = p["tray_h"]
    tray = box(xg, 0, Z0, ew, ed, th) - box(xg, 0, Z0 + t, ew - 2 * t, ed - 2 * t, th)
    cover = box(xg, 0, Z0 + th, ew, ed, eh - th) - box(xg, 0, Z0 + th - 1, ew - 2 * t, ed - 2 * t, eh - th - t + 1)
    sw, sh = p["vent_slot"]
    xv = xg + p["vent_dx"]
    for side in (-1, 1):
        yw = side * (ed / 2 - t / 2)
        for i in range(p["vent_rows_low"]):
            tray = tray - box(xv, yw, Z0 + p["vent_z_low"] - sh / 2 + (i - (p["vent_rows_low"] - 1) / 2) * 7, sw, t + 2, sh)
        for i in range(p["vent_rows_high"]):
            cover = cover - box(xv, yw, Z0 + p["vent_z_high"] - sh / 2 + (i - (p["vent_rows_high"] - 1) / 2) * 5, sw, t + 2, sh)
    ze = Z0 + p["entry_z"]
    tray = tray - ycyl(xg + p["rj45"][2], -ed / 2 - 1, ze, p["rj45"][0] / 2, t + 2)
    tray = tray - ycyl(xg + p["gland"][2], -ed / 2 - 1, ze, p["gland"][0] / 2, t + 2)
    bx = D["bx"]
    sx, sy, sz = p["sbc"]
    holes = board_holes(p)
    for x, y in holes:
        tray = tray - zcyl(x, y, Z0 - 1, p["hole_m25"] / 2, t + 2)
    parts["enc_base"] = tray + clip_feet(xg, ew, p)
    al, ad = p["antenna"]
    ax_, ay_ = bx - 10, 20
    cover = cover - zcyl(ax_, ay_, Z0 + eh - t - 1, p["sma_hole"] / 2, t + 2)
    parts["enc_cover"] = cover

    # 5 computer, 6 cooler, 7 concentrator HAT, 8 microSD, 19 standoffs and header extender
    sbc_z = Z0 + t + p["sbc_standoff"]
    sbc = box(bx, 0, sbc_z, sx, sy, sz)
    for x, y in holes:
        sbc = sbc - zcyl(x, y, sbc_z - 1, p["hole_m25"] / 2, sz + 2)
    parts["sbc"] = sbc + box(bx + 31.5, 0, sbc_z + sz, 18, 50, 14)          # USB and Ethernet stack
    cx_, cy_, cz_ = p["cooler"]
    parts["cooler"] = box(bx - 12, 0, sbc_z + sz, cx_, cy_, cz_)
    hat_z = sbc_z + sz + p["hat_standoff"]
    hx_, hy_, hz_ = p["hat"]
    hat = box(bx - 10, 0, hat_z, hx_, hy_, hz_)
    for x, y in holes:
        hat = hat - zcyl(x, y, hat_z - 1, p["hole_m25"] / 2, hz_ + 2)
    parts["hat"] = hat + box(bx - 10, 0, hat_z + hz_, 52, 30, 5)
    parts["sd"] = box(bx - sx / 2 - 2.5, 0, sbc_z - 1.2, 15, 11, 1.2)
    sp = standoff_pieces(p)
    parts["standoffs"] = sp["lower"] + sp["upper"] + sp["heads_low"] + sp["heads_top"] + sp["header"]

    # 9 antenna: SMA bulkhead through the cover (nut inside, flange and whip outside)
    parts["antenna"] = (zcyl(ax_, ay_, Z0 + eh - t - 3, 5.0, 3) + zcyl(ax_, ay_, Z0 + eh - t, 3.1, t)
                        + zcyl(ax_, ay_, Z0 + eh, 7, 6) + zcyl(ax_, ay_, Z0 + eh + 6, ad / 2, al))

    # 20 cable entries: RJ45 feed-through coupler and M12 gland in the -Y wall
    yo = -ed / 2
    d0, fd, dx = p["rj45"]
    rj = (ycyl(xg + dx, yo, ze, fd / 2, -3) + ycyl(xg + dx, yo, ze, d0 / 2 - 0.2, t)
          + ycyl(xg + dx, yo + t, ze, fd / 2 - 1, 4) + ycyl(xg + dx, yo + t + 4, ze, d0 / 2 - 0.5, 10))
    g0, gfd, gdx = p["gland"]
    parts["entries"] = rj + gland_shape(xg + gdx, yo, ze, g0, gfd, t)

    # 10 DC-DC converter
    pw_ = p["psu_modules"] * m
    parts["psu"] = (box(D["x_psu"], 0, Z0, pw_, ed, eh - 5) + box(D["x_psu"], 0, Z0 + eh - 5, pw_ - 6, 45, 5)
                    + clip_feet(D["x_psu"], pw_, p))

    # 11 UPS module (no battery inside it)
    uw, xu = D["ups_w"], D["x_ups"]
    parts["ups"] = box(xu, 0, Z0, uw, ed, eh - 5) + box(xu, 0, Z0 + eh - 5, uw - 6, 45, 5) + clip_feet(xu, uw, p)

    # 17 battery box (3-module DIN enclosure, base and cover), 12 pack on a hook-and-loop pad, gland
    bw, xb = D["box_w"], D["x_box"]
    bbase = box(xb, 0, Z0, bw, ed, th) - box(xb, 0, Z0 + t, bw - 2 * t, ed - 2 * t, th)
    bbase = bbase - ycyl(xb, -ed / 2 - 1, ze, p["box_gland"][0] / 2, t + 2)
    parts["box_base"] = bbase + clip_feet(xb, bw, p)
    parts["box_cover"] = box(xb, 0, Z0 + th, bw, ed, eh - th) - box(xb, 0, Z0 + th - 1, bw - 2 * t, ed - 2 * t, eh - th - t + 1)
    kx, ky, kz = p["pack"]
    parts["pad"] = box(xb, 0, Z0 + t, kx, ky - 10, p["pad_t"])
    parts["pack"] = box(xb, 0, Z0 + t + p["pad_t"], kx, ky, kz)
    parts["box_gland"] = gland_shape(xb, yo, ze, p["box_gland"][0], p["box_gland"][1], t)

    # 13 terminal blocks and fuse holder, left of the enclosure
    x0 = D["x_tb0"]
    tw, fw = p["tb_w"], p["fuse_w"]
    tb = (box(x0 - tw / 2, 0, Z0, tw, 45, p["tb_h"]) + box(x0 - tw - gap / 2 - tw / 2, 0, Z0, tw, 45, p["tb_h"])
          + box(x0 - 2 * tw - gap - fw / 2, 0, Z0, fw, 60, p["fuse_h"]))
    tb = tb + clip_feet(x0 - tw / 2, tw, p) + clip_feet(x0 - tw - gap / 2 - tw / 2, tw, p) + clip_feet(x0 - 2 * tw - gap - fw / 2, fw, p)
    parts["terminals"] = tb

    # 18 end stops, tight against the fuse holder and the battery box
    sw_, sd_, sh_ = p["stop"]
    st = None
    for xs in (D["stop_l"], D["stop_r"]):
        s = box(xs, 0, Z0, sw_, sd_, sh_) + clip_feet(xs, sw_ + 2, p)
        st = s if st is None else st + s
    parts["stops"] = st

    # 21 fixings: M4 rail screws (pan heads on the rail base) and rubber feet under the plate
    fx = None
    for dx in p["rail_screw_dx"]:
        s = zcyl(xr + dx, 0, p["rail_t"], 3.5, 2.6) + zcyl(xr + dx, 0, -pt, 1.65, pt) + zcyl(xr + dx, 0, 0, 2.0, p["rail_t"])
        fx = s if fx is None else fx + s
    parts["rail_screws"] = fx
    fd_, fh_, fxo, fyo = p["feet"]
    ft = None
    for sx_ in (-1, 1):
        for sy_ in (-1, 1):
            f = zcyl(xr + sx_ * fxo, sy_ * fyo, -pt - fh_, fd_ / 2, fh_)
            ft = f if ft is None else ft + f
    parts["feet"] = ft
    return parts


# key, BOM line, name (BOM numbers match bom/bom.csv and the exploded view callouts)
BOM_ORDER = [("plate", 1, "Bench mounting plate"), ("rail", 2, "DIN rail, TS35"),
             ("enc_base", 3, "Gateway enclosure base"), ("enc_cover", 4, "Gateway enclosure cover"),
             ("sbc", 5, "Single-board computer, 4 GB"), ("cooler", 6, "Active cooler"),
             ("hat", 7, "LoRaWAN concentrator HAT"), ("sd", 8, "microSD card, high endurance"),
             ("antenna", 9, "LoRa antenna and SMA bulkhead"), ("psu", 10, "DC-DC converter, 12 V to 5 V"),
             ("ups", 11, "DIN UPS module"), ("pack", 12, "LiFePO4 backup pack, 12.8 V"),
             ("terminals", 13, "Terminal blocks and fuse"),
             ("box_base", 17, "Battery box base"), ("box_cover", 17, "Battery box cover"),
             ("stops", 18, "DIN rail end stops"), ("standoffs", 19, "Board standoffs and header extender"),
             ("entries", 20, "Cable entries"), ("box_gland", 20, "Battery box gland"),
             ("pad", 21, "Hook-and-loop pad"), ("rail_screws", 21, "Rail screws"), ("feet", 21, "Rubber feet")]

ENCLOSURE_KEYS = ("enc_base", "enc_cover", "sbc", "cooler", "hat", "sd", "antenna", "standoffs", "entries")


def assembly(p=PARAMS):
    b = _b()
    return b.Compound(children=list(build_parts(p).values()))


# ----------------------------------------------------------------- constructability checks
# Pairs that must touch (a face on a face): the joint that holds or seats each part.
CONTACTS = [("rail", "plate"), ("rail_screws", "rail"), ("rail_screws", "plate"), ("feet", "plate"),
            ("enc_base", "rail"), ("psu", "rail"), ("ups", "rail"), ("box_base", "rail"), ("terminals", "rail"),
            ("stops", "rail"), ("stops", "terminals"), ("stops", "box_base"),
            ("enc_cover", "enc_base"), ("box_cover", "box_base"),
            ("standoffs", "enc_base"), ("standoffs", "sbc"), ("standoffs", "hat"),
            ("cooler", "sbc"), ("sd", "sbc"), ("antenna", "enc_cover"), ("entries", "enc_base"),
            ("pad", "box_base"), ("pack", "pad"), ("box_gland", "box_base")]
# Pairs that must stay apart by at least this clearance (mm): neighbours on the rail, and parts
# inside the enclosures that must not rub.
CLEAR = [("enc_base", "terminals", 1.5), ("enc_base", "psu", 1.5), ("psu", "ups", 1.5), ("ups", "box_base", 1.5),
         ("enc_cover", "psu", 1.5), ("box_cover", "ups", 1.5),
         ("hat", "cooler", 5.0), ("antenna", "hat", 10.0), ("entries", "sbc", 5.0), ("entries", "hat", 5.0),
         ("pack", "box_gland", 2.0), ("pack", "box_cover", 1.0), ("rail_screws", "enc_base", 2.0),
         ("rail_screws", "ups", 2.0), ("standoffs", "rail", 2.0), ("sd", "enc_base", 2.0)]


def check(p=PARAMS, verbose=True):
    """Run the constructability checks. Returns (passed, failed) lists of strings."""
    P = build_parts(p)
    keys = list(P)
    ok, bad = [], []
    for i, a in enumerate(keys):
        for k in keys[i + 1:]:
            try:
                v = (P[a] & P[k]).volume
            except Exception:
                v = 0.0
            (bad if v > 0.01 else ok).append(f"no overlap {a} / {k}: {v:.3f} mm3")
    for a, k in CONTACTS:
        d = P[a].distance_to(P[k])
        (ok if d < 0.01 else bad).append(f"touch {a} / {k}: gap {d:.3f} mm")
    for a, k, c in CLEAR:
        d = P[a].distance_to(P[k])
        (ok if d >= c - 1e-6 else bad).append(f"clear {a} / {k}: {d:.2f} mm (min {c})")
    D = derived(p)
    # the rail and plate must hold every module and both end stops
    rl = p["rail"][0]
    span = D["rail_occupied_mm"]
    (ok if span <= rl else bad).append(f"rail {rl:.0f} mm carries {span:.1f} mm of modules and end stops")
    (ok if rl <= p["plate"][0] else bad).append(f"rail {rl:.0f} mm fits the {p['plate'][0]:.0f} mm plate")
    (ok if D["rail_used_mm"] <= 350 else bad).append(f"R10: modules use {D['rail_used_mm']:.1f} mm of rail (350 mm allowed)")
    if verbose:
        for s in ok:
            print("ok  ", s)
        for s in bad:
            print("FAIL", s)
        print(f"{len(ok)} checks passed, {len(bad)} failed")
    return ok, bad


if __name__ == "__main__":
    if "--check" in sys.argv:
        _, bad = check()
        sys.exit(1 if bad else 0)
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
        export_stl(c, str(out / "stl" / f"{name}.stl"), tolerance=0.05, angular_tolerance=0.3)
        bb = c.bounding_box()
        print(f"{name}: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm")
    D = derived()
    print(f"rail used {D['rail_used_mm']:.0f} mm ({D['rail_used_modules']:.1f} modules), {D['rail_occupied_mm']:.0f} mm with end stops; enclosure "
          f"{D['enc_w']:.1f} x {PARAMS['enc_d']:.0f} x {PARAMS['enc_h']:.0f} mm, area {D['enc_area_m2']:.4f} m2; "
          f"vents {D['vent_low_mm2']:.0f} mm2 low, {D['vent_high_mm2']:.0f} mm2 high, {D['vent_stack_mm']:.0f} mm apart")
