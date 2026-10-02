"""TwinKit prototype build plan pictures (TWK-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|layouts|joints|steps|wiring ...]
With no argument it draws everything. Every picture is drawn from cad/src/model.py
(build_parts and standoff_pieces), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/TWK-DWG-101 to 105        making sketches for the made and drilled components
    docs/05-build-plan/plate-holes.png     hole layout of the bench plate
    docs/05-build-plan/enclosure-holes.png cut-outs in the enclosure base, cover and battery box
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
    docs/05-build-plan/wiring.png          block-level wiring with wire sizes (matplotlib)
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from model import PARAMS as P, build_parts, derived, standoff_pieces, board_holes, box  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-02"
D = derived(P)
C = build_parts(P)
SP = standoff_pieces(P)
Z0, T = P["rail"][2], P["enc_wall"]
XG, ED = P["x_gw"], P["enc_d"]

COL = {"plate": "#A8A29E", "feet": "#1F2937", "rail": "#9CA3AF", "screws": "#111827", "enc_base": "#D1D5DB",
       "enc_cover": "#7DD3C8", "entries": "#1F2937", "standoffs": "#B45309", "sbc": "#15803D", "sd": "#1F2937",
       "cooler": "#4B5563", "hat": "#0F766E", "header": "#7C3AED", "antenna": "#374151", "terminals": "#D4A017",
       "psu": "#6B7280", "ups": "#64748B", "box_base": "#D1D5DB", "pad": "#57534E", "pack": "#C2410C",
       "box_cover": "#7DD3C8", "stops": "#1E3A8A", "bolt": "#111827"}


def _fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def mv(p, e):
    return Part(p.name, p.shape, p.color, None, tuple(e), p.alpha)


# ----------------------------------------------------------------- named parts, in build order
def made():
    return {
        "plate": part("Bench plate", C["plate"], COL["plate"]),
        "feet": part("Rubber feet (4)", C["feet"], COL["feet"]),
        "rail": part("DIN rail and 3 M4 screws", C["rail"] + C["rail_screws"], COL["rail"]),
        "enc_base": part("Enclosure base, cut and drilled", C["enc_base"], COL["enc_base"]),
        "entries": part("Network coupler and power gland", C["entries"], COL["entries"]),
        "lower": part("Lower standoffs (4) and screws", SP["lower"] + SP["heads_low"], COL["standoffs"]),
        "sbc": part("Computer with microSD card", C["sbc"] + C["sd"], COL["sbc"]),
        "cooler": part("Active cooler", C["cooler"], COL["cooler"]),
        "upper": part("Upper standoffs (4) and header extender", SP["upper"] + SP["header"], COL["header"]),
        "hat": part("Concentrator HAT and screws", C["hat"] + SP["heads_top"], COL["hat"]),
        "enc_cover": part("Enclosure cover, drilled", C["enc_cover"], COL["enc_cover"]),
        "antenna": part("Antenna and SMA bulkhead", C["antenna"], COL["antenna"]),
        "terminals": part("Terminal blocks and fuse holder", C["terminals"], COL["terminals"]),
        "psu": part("DC-DC converter", C["psu"], COL["psu"]),
        "ups": part("UPS module", C["ups"], COL["ups"]),
        "box_base": part("Battery box base and gland", C["box_base"] + C["box_gland"], COL["box_base"]),
        "pad": part("Hook-and-loop pad", C["pad"], COL["pad"]),
        "pack": part("Backup pack", C["pack"], COL["pack"]),
        "box_cover": part("Battery box cover", C["box_cover"], COL["box_cover"]),
        "stops": part("End stops (2)", C["stops"], COL["stops"]),
    }


ORDER = ["plate", "feet", "rail", "enc_base", "entries", "lower", "sbc", "cooler", "upper", "hat", "enc_cover",
         "antenna", "terminals", "psu", "ups", "box_base", "pad", "pack", "box_cover", "stops"]


# ----------------------------------------------------------------- overview
def overview():
    M = made()
    off = {"plate": (0, 0, -40), "feet": (0, 0, -120), "rail": (0, 0, 0), "enc_base": (0, 0, 60),
           "entries": (0, -120, 60), "lower": (0, 0, 130), "sbc": (0, 0, 175), "cooler": (0, 0, 220),
           "upper": (0, 0, 265), "hat": (0, 0, 310), "enc_cover": (0, 0, 370), "antenna": (0, 0, 440),
           "terminals": (-50, 0, 60), "psu": (20, 0, 60), "ups": (45, 0, 60), "box_base": (110, 0, 60),
           "pad": (110, 0, 150), "pack": (110, 0, 200), "box_cover": (110, 0, 290)}
    parts = []
    for k in ORDER[:-1]:
        p = M[k]
        p.explode = off[k]
        parts.append(p)
    # the two end stops are pulled out along the rail, each its own way
    import build123d as b
    left = C["stops"] & b.Pos(D["stop_l"], 0, 0) * b.Box(30, 200, 200)
    right = C["stops"] & b.Pos(D["stop_r"], 0, 0) * b.Box(30, 200, 200)
    parts.append(part("End stops (2)", b.Pos(-110, 0, 30) * left + b.Pos(150, 0, 30) * right, COL["stops"]))
    return bv.overview(parts, OUT / "overview.png", "TwinKit prototype: every component, pulled apart",
                       subtitle="Numbered in build order. Seen from the front right and above; the front is the side with the cable entries",
                       elev=22, azim=-62, size=(12, 8.5), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches
def sheets():
    import build123d as b
    M = made()
    base = dict(project="TwinKit", date=DATE)
    out = []
    xr = D["x_rail"]
    pl = P["plate"]
    ins = P["plate_hole_inset"]

    # 101 bench plate
    out.append(bv.component_sheet(
        Part("Bench plate", C["plate"], COL["plate"]), [M["rail"], M["enc_base"], M["psu"], M["ups"], M["box_base"], M["terminals"]],
        dwg_no="TWK-DWG-101", title="TwinKit bench plate: making sketch", material="Aluminium sheet 6 mm, 5083, 6082 or 6061 class",
        view_shape=b.Pos(-xr, 0, 0) * C["plate"], inset_view=(30, -60),
        notes=["Blank 360 x 180 x 6 mm. Cut square, file the edges, round the",
               "  corners to about 3 mm. Scribe a centre line along the long side.",
               "Rail holes: three on the centre line, at the middle and 150 mm",
               "  each side of it. Drill 3.3 mm right through and tap M4.",
               f"Corner holes: four 5.5 mm holes, {ins:.0f} mm in from each long and short",
               "  edge, for screwing the plate to a wall or cabinet later.",
               "Deburr every hole on both faces.",
               "Underneath: four stick-on rubber feet, 20 mm across, centred",
               "  150 mm each side of the middle and 60 mm each side of the centre line.",
               "Fit: the rail lies on the centre line, held by three M4 x 6 mm",
               "  pan-head screws through its base into the tapped holes.",
               "Check: an M4 screw runs into each hole by hand; the plate rocks",
               "  on none of its feet on a flat bench."], **base))

    # 102 DIN rail
    rail = C["rail"]
    out.append(bv.component_sheet(
        Part("DIN rail", rail, COL["rail"]), [M["plate"]],
        dwg_no="TWK-DWG-102", title="TwinKit DIN rail: making sketch", material="TS35 x 7.5 top-hat rail, slotted, steel or aluminium",
        view_shape=b.Pos(-xr, 0, 0) * rail, inset_view=(35, -70),
        notes=["Cut a 350 mm length of TS35 x 7.5 slotted top-hat rail with a",
               "  hacksaw; file the cut ends square and remove every burr.",
               "The rail is 35 mm wide across its top flanges, 7.5 mm high, with",
               "  a 27 mm wide base that lies on the plate.",
               "Holes: three, on the rail's centre line, at the middle and 150 mm",
               "  each side. Where a slot already falls within 3 mm of a mark, use",
               "  the slot; otherwise drill 4.5 mm through the base.",
               "Fit: lay the rail on the plate's centre line, ends 5 mm in from the",
               "  plate's short edges. Three M4 x 6 mm pan-head screws, snug.",
               "Every module clips over the two top flanges; the screw heads sit",
               "  3.9 mm below the modules, so nothing rubs.",
               "Check: the rail lies flat along its length; a module clips on and",
               "  slides along it from end to end without catching on a screw."], **base))

    # 103 enclosure base
    eb = C["enc_base"]
    out.append(bv.component_sheet(
        Part("Enclosure base", eb, COL["enc_base"]), [M["rail"], M["entries"], M["lower"], M["sbc"], M["plate"]],
        dwg_no="TWK-DWG-103", title="TwinKit gateway enclosure base: cutting and drilling sketch",
        material="Bought 9-module DIN enclosure base, polycarbonate, 157.5 x 90 x 44 mm",
        view_shape=b.Pos(-XG, 0, -Z0) * eb, inset_view=(25, -60),
        notes=["The front is the long wall that will face you on the bench; the",
               "  antenna sits toward the back. Mark the front before cutting.",
               "Vent slots: two slots 40 x 4 mm in each long wall, centred 32 mm",
               "  left of the middle, 2.5 to 6.5 and 9.5 to 13.5 mm above the",
               "  outside of the floor. Chain drill 3.5 mm and file to the line.",
               "Front wall, 26 mm above the outside of the floor: a 20 mm hole",
               "  50 mm right of the middle (network coupler) and a 16.2 mm hole",
               "  20 mm right of the middle (power gland). Step drill, light pressure.",
               "Floor: four 2.7 mm holes for the computer: 58 mm apart along the",
               "  base and 49 mm apart across it, the left pair 59 mm and the right",
               "  pair 1 mm left of the middle. Use the maker's bosses if it has them.",
               "Tape the faces first; no solvents; deburr inside and out.",
               "Check: lay the computer on the floor; its holes line up with yours."], **base))

    # 104 enclosure cover
    ec = C["enc_cover"]
    out.append(bv.component_sheet(
        Part("Enclosure cover", ec, COL["enc_cover"]), [M["enc_base"], M["antenna"], M["hat"]],
        dwg_no="TWK-DWG-104", title="TwinKit gateway enclosure cover: drilling sketch",
        material="Bought cover for the 9-module enclosure, clear or tinted polycarbonate",
        view_shape=b.Pos(-XG, 0, -(Z0 + P["tray_h"])) * ec, inset_view=(35, -60),
        notes=["Antenna hole: 6.5 mm through the top, 30 mm left of the middle",
               "  and 20 mm behind the centre line (toward the back wall).",
               "  Pilot 3 mm, then step drill; check the size on the bulkhead's",
               "  datasheet before the last step.",
               "Vent slots: two slots 40 x 4 mm in each long wall, in line with the",
               "  base's slots, 1.5 to 5.5 and 6.5 to 10.5 mm above the cover's",
               "  lower edge. Skip any the maker has already moulded.",
               "Deburr; clean with water and mild soap only.",
               "Fit: the bulkhead goes in from above, flange and washer on the",
               "  outside, nut inside. The cover then closes onto the base with",
               "  the maker's clips or screws.",
               "Check: the bulkhead nut clears the concentrator HAT by 20 mm when",
               "  the cover is closed."], **base))

    # 105 battery box base
    bb_ = C["box_base"]
    out.append(bv.component_sheet(
        Part("Battery box base", bb_, COL["box_base"]), [M["rail"], M["pack"], M["pad"], M["ups"],
                                                         part("Gland", C["box_gland"], COL["entries"])],
        dwg_no="TWK-DWG-105", title="TwinKit battery box base: drilling sketch",
        material="Bought 3-module DIN enclosure base, polycarbonate, 52.5 x 90 x 44 mm",
        view_shape=b.Pos(-D["x_box"], 0, -Z0) * bb_, inset_view=(25, -60),
        notes=["One 12.2 mm hole in the front wall, on the middle of the wall,",
               "  26 mm above the outside of the floor, for the M12 gland that",
               "  the pack lead passes through. Pilot 3 mm, then step drill.",
               "Deburr inside and out.",
               "Inside: a hook-and-loop pad 38 x 60 mm stuck to the middle of the",
               "  floor; its mate goes on the pack's underside.",
               "The pack (38 x 70 x 38 mm at most) lies on the pad, long side",
               "  front to back, 3.5 mm clear of the gland nut.",
               "Fit: the gland goes in from outside, seal outside, nut inside.",
               "Check: the pack sits on the pad with its lead reaching the gland",
               "  without strain, and the cover closes without touching it."], **base))
    return out


# ----------------------------------------------------------------- joints
def _win(sh, x0, x1, y0, y1, z0, z1):
    import build123d as b
    return sh & (b.Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * b.Box(x1 - x0, y1 - y0, z1 - z0))


def joints():
    out = []
    xr = D["x_rail"]
    # 01 rail on the plate, cut through the middle screw
    w = (xr - 25, xr + 0.01, -40, 40, -8, 12)
    out.append(bv.joint([
        part("Bench plate (tapped M4)", _win(C["plate"], *w), COL["plate"]),
        part("DIN rail base on the plate", _win(C["rail"], *w), COL["rail"]),
        part("M4 x 6 pan-head screw", _win(C["rail_screws"], *w), COL["bolt"])],
        OUT / "joint-01.png", "Joint 1: DIN rail on the bench plate (cut through the middle screw)",
        subtitle="Seen from the front right. The rail's base lies flat on the plate; the screw goes into a tapped hole",
        elev=25, azim=-35, size=(8, 6)))
    # 02 module clip on the rail, cut across the rail
    x0 = D["x_psu"]
    w = (x0 - 6, x0 + 0.01, -26, 26, -3, 14)
    out.append(bv.joint([
        part("Bench plate", _win(C["plate"], *w), COL["plate"]),
        part("DIN rail (top-hat section)", _win(C["rail"], *w), "#374151"),
        part("Module base with its clip hooks", _win(C["psu"], *w), "#93C5FD")],
        OUT / "joint-02.png", "Joint 2: how every module clips onto the rail (cut across the rail)",
        subtitle="Seen along the rail. A hook each side reaches under the rail's flange; the base sits on top of it",
        elev=6, azim=-6, size=(8, 6)))
    # 03 board stack at one corner, cut open
    hx, hy = board_holes(P)[1]
    w = (hx - 10, hx + 14, hy - 4, hy + 5, Z0 - 3, Z0 + 37)
    out.append(bv.joint([
        part("Enclosure floor", _win(C["enc_base"], *w), COL["enc_base"]),
        part("Lower standoff, 6 mm, screw from below", _win(SP["lower"] + SP["heads_low"], *w), COL["standoffs"]),
        part("Computer board", _win(C["sbc"], *w), COL["sbc"]),
        part("Upper standoff, 16 mm", _win(SP["upper"], *w), COL["header"]),
        part("Header extender", _win(SP["header"], *w), "#A78BFA"),
        part("Concentrator HAT, screw on top", _win(C["hat"] + SP["heads_top"], *w), COL["hat"])],
        OUT / "joint-03.png", "Joint 3: the board stack at one corner (enclosure cut away)",
        subtitle="Back left corner, seen from the front. Floor, 6 mm standoff, computer, 16 mm standoff, HAT; the header extender joins the boards",
        elev=14, azim=-72, size=(8, 6)))
    # 04 cable entries through the front wall, cut through their centres
    ze = Z0 + P["entry_z"]
    w = (XG + 5, XG + 70, -62, -20, ze - 25, ze + 0.01)
    out.append(bv.joint([
        part("Enclosure front wall", _win(C["enc_base"], *w), COL["enc_base"]),
        part("Network coupler: flange outside, nut inside", _win(C["entries"] & _right_of(XG + 35), *w), COL["entries"]),
        part("Power gland: dome outside, nut inside", _win(C["entries"] & _left_of(XG + 35), *w), "#475569")],
        OUT / "joint-04.png", "Joint 4: network coupler and power gland in the front wall (cut through their centres)",
        subtitle="Lower halves, seen from above and the front. Each clamps the wall between its outside flange and its inside nut",
        elev=50, azim=-70, size=(8, 6)))
    # 05 antenna bulkhead through the cover
    ax_, ay_ = D["bx"] - 10, 20
    zt = Z0 + P["enc_h"]
    w = (ax_ - 22, ax_ + 22, ay_ - 0.01, ay_ + 22, zt - 12, zt + 22)
    out.append(bv.joint([
        part("Enclosure cover top", _win(C["enc_cover"], *w), COL["enc_cover"]),
        part("SMA bulkhead, nut inside", _win(C["antenna"], *w), COL["antenna"])],
        OUT / "joint-05.png", "Joint 5: antenna bulkhead through the cover (cut through its centre)",
        subtitle="Back half, seen from the front. Flange and washer on top, nut underneath; the whip screws onto the top",
        elev=12, azim=-90, size=(8, 6)))
    # 06 pack in the battery box, cut in half along the rail
    xb = D["x_box"]
    w = (xb - 30, xb + 0.01, -70, 50, Z0 - 1, Z0 + 61)
    out.append(bv.joint([
        part("Battery box base", _win(C["box_base"], *w), COL["box_base"]),
        part("Hook-and-loop pad", _win(C["pad"], *w), COL["pad"]),
        part("Backup pack", _win(C["pack"], *w), COL["pack"]),
        part("M12 gland for the pack lead", _win(C["box_gland"], *w), COL["entries"]),
        part("Battery box cover", _win(C["box_cover"], *w), COL["box_cover"])],
        OUT / "joint-06.png", "Joint 6: backup pack in its battery box (box cut in half)",
        subtitle="Seen from the right. The pack sits on the pad, 3.5 mm clear of the gland nut and clear of the cover",
        elev=15, azim=-10, size=(8, 6)))
    # 07 end stop against the fuse holder
    xs = D["stop_l"]
    w = (xs - 10, xs + 30, -35, 35, -6, 60)
    out.append(bv.joint([
        part("Bench plate", _win(C["plate"], *w), COL["plate"]),
        part("DIN rail", _win(C["rail"], *w), COL["rail"]),
        part("End stop, screw-clamped to the rail", _win(C["stops"], *w), COL["stops"]),
        part("Fuse holder and terminal blocks", _win(C["terminals"], *w), COL["terminals"])],
        OUT / "joint-07.png", "Joint 7: left end stop pressed against the fuse holder",
        subtitle="Seen from the front left. The stop clamps to the rail touching the last module, so nothing can slide",
        elev=22, azim=-130, size=(8, 6)))
    return out


def _right_of(x):
    import build123d as b
    return b.Pos(x + 100, 0, 0) * b.Box(200, 400, 400)


def _left_of(x):
    import build123d as b
    return b.Pos(x - 100, 0, 0) * b.Box(200, 400, 400)


# ----------------------------------------------------------------- assembly steps
def steps():
    M = made()
    out = []

    def st(n, done, new, title, sub, **kw):
        out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))

    pl, ft, rl = M["plate"], M["feet"], M["rail"]
    st(1, [pl], [mv(ft, (0, 0, -50))], "rubber feet under the bench plate",
       "Seen from below. Clean the underside; press one foot on at each mark, 150 mm and 60 mm from the middle",
       elev=-30, azim=-60, label_done=True)
    st(2, [pl, ft], [mv(part("DIN rail", C["rail"], COL["rail"]), (0, 0, 50)),
                     mv(part("M4 x 6 pan-head screws (3)", C["rail_screws"], COL["screws"]), (0, 0, 90))],
       "DIN rail onto the bench plate", "On the centre line, 5 mm in from each end; three M4 screws into the tapped holes, snug",
       elev=30, azim=-60, label_done=False)
    eb = M["enc_base"]
    st(3, [eb], [mv(M["entries"], (0, -60, 0))], "network coupler and power gland into the enclosure base",
       "From outside: flange and seal outside, nut inside, maker's torque. Seen from the front left",
       elev=25, azim=-125, label_done=True)
    st(4, [eb, M["entries"]], [mv(M["lower"], (0, 0, 50))], "lower standoffs into the enclosure floor",
       "Four 6 mm brass standoffs on the four floor holes; an M2.5 pan-head screw into each from underneath",
       elev=40, azim=-55, label_done=False)
    st(5, [part("Computer", C["sbc"], COL["sbc"])], [mv(part("Active cooler", C["cooler"], COL["cooler"]), (0, 0, 40)),
                                                      mv(part("microSD card (flashed)", C["sd"], COL["sd"]), (-40, 0, 0))],
       "cooler and microSD card onto the computer", "Cooler clips into its two board holes; plug its fan lead in. Card into its slot, contacts up",
       elev=30, azim=-60, label_done=True)
    done6 = [eb, M["entries"], M["lower"]]
    st(6, done6, [mv(part("Computer with cooler and card", C["sbc"] + C["sd"] + C["cooler"], COL["sbc"]), (0, 0, 70))],
       "computer onto the lower standoffs", "Lay it on the standoffs, network socket toward the coupler; plug in the coupler's patch lead now",
       elev=35, azim=-55, label_done=False)
    done7 = done6 + [part("Computer", C["sbc"] + C["sd"] + C["cooler"], COL["sbc"])]
    st(7, done7, [mv(M["upper"], (0, 0, 50))], "upper standoffs and header extender",
       "Screw a 16 mm standoff into each lower one through the board's holes; push the extender onto the 40-pin header",
       elev=35, azim=-55, label_done=False)
    done8 = done7 + [M["upper"]]
    st(8, done8, [mv(M["hat"], (0, 0, 60))], "concentrator HAT onto the stack",
       "Line its socket up with the extender and press down evenly; four M2.5 screws on top. Antenna pigtail onto its U.FL socket",
       elev=35, azim=-55, label_done=False)
    st(9, [M["enc_cover"]], [mv(M["antenna"], (0, 0, 80))], "antenna bulkhead into the cover",
       "From above: flange and washer outside, nut inside, snug; then screw the whip on finger tight",
       elev=30, azim=-60, label_done=True)
    done10 = done8 + [M["hat"]]
    st(10, done10, [mv(part("Cover with antenna", C["enc_cover"] + C["antenna"], COL["enc_cover"]), (0, 0, 90))],
       "close the gateway enclosure", "Pigtail onto the bulkhead first. Then close the cover with the maker's clips or screws, no wire pinched",
       elev=25, azim=-55, label_done=False)
    rail_done = [pl, ft, rl]
    st(11, rail_done, [mv(M["terminals"], (0, 0, 60))], "terminal blocks and fuse holder onto the rail",
       "At the left end, fuse holder outermost. Hook the back edge over the rail, then press the front down until it clicks",
       elev=28, azim=-60, label_done=False)
    gw = part("Gateway enclosure", C["enc_base"] + C["enc_cover"] + C["antenna"] + C["entries"], COL["enc_base"])
    done12 = rail_done + [M["terminals"]]
    st(12, done12, [mv(gw, (0, 0, 60))], "gateway enclosure onto the rail",
       "2 mm right of the terminal blocks, cable entries to the front; it clips on the same way",
       elev=28, azim=-60, label_done=False)
    done13 = done12 + [gw]
    st(13, done13, [mv(M["psu"], (0, 0, 60)), mv(M["ups"], (0, 0, 120))], "DC-DC converter and UPS module onto the rail",
       "Each 2 mm right of the one before; terminals to the top",
       elev=28, azim=-60, label_done=False)
    done14 = done13 + [M["psu"], M["ups"]]
    st(14, done14, [mv(M["box_base"], (0, 0, 60))], "battery box base onto the rail",
       "2 mm right of the UPS module, gland to the front",
       elev=28, azim=-60, label_done=False)
    done15 = done14 + [M["box_base"]]
    st(15, done15, [mv(M["pad"], (0, 0, 60)), mv(part("Backup pack (lead through the gland)", C["pack"], COL["pack"]), (0, 0, 110))],
       "backup pack into the battery box", "Pad on the floor, pack pressed onto it; lead out through the gland, gland nut tight. Do not connect it yet",
       elev=40, azim=-60, label_done=False)
    done16 = done15 + [M["pad"], M["pack"]]
    st(16, done16, [mv(M["box_cover"], (0, 0, 70))], "close the battery box",
       "Cover on with the maker's clips or screws", elev=28, azim=-60, label_done=False)
    import build123d as b
    left = C["stops"] & b.Pos(D["stop_l"], 0, 0) * b.Box(30, 200, 200)
    right = C["stops"] & b.Pos(D["stop_r"], 0, 0) * b.Box(30, 200, 200)
    done17 = done16 + [M["box_cover"]]
    st(17, done17, [mv(part("Left end stop", left, COL["stops"]), (-60, 0, 0)), mv(part("Right end stop", right, COL["stops"]), (60, 0, 0))],
       "end stops at both ends", "Slide each stop against the last module and tighten its screw; the modules can no longer slide",
       elev=28, azim=-60, label_done=False)
    return out


# ----------------------------------------------------------------- layouts
def layouts():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle, Circle
    INK, MUT, AC = "#111827", "#4B5563", "#0F766E"
    res = []
    # plate holes, seen from above
    L, Wd, _ = P["plate"]
    ins = P["plate_hole_inset"]
    fig = plt.figure(figsize=(11, 6.6), dpi=150)
    ax = fig.add_axes([0.05, 0.1, 0.9, 0.74]); ax.set_aspect("equal"); ax.set_axis_off()
    ax.add_patch(Rectangle((-L / 2, -Wd / 2), L, Wd, fc="#F5F5F4", ec=INK, lw=1.2))
    ax.add_patch(Rectangle((-175, -P["rail"][1] / 2), 350, P["rail"][1], fc="none", ec=MUT, lw=0.8, ls="--"))
    ax.text(-100, P["rail"][1] / 2 + 3, "rail goes here (350 x 35)", fontsize=8, color=MUT, va="bottom")
    ax.axhline(0, color=MUT, lw=0.5, ls=(0, (8, 3, 2, 3)))
    for dx in P["rail_screw_dx"]:
        ax.add_patch(Circle((dx, 0), 1.65, fc="white", ec=INK, lw=1))
        ax.plot([dx - 5, dx + 5], [0, 0], color=MUT, lw=0.4); ax.plot([dx, dx], [-5, 5], color=MUT, lw=0.4)
        ax.text(dx, -8, f"M4 tapped\n{dx:+g}" if dx else "M4 tapped\nmiddle", ha="center", va="top", fontsize=7.5, color=INK)
    fd, fh, fx, fy = P["feet"]
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = sx * (L / 2 - ins), sy * (Wd / 2 - ins)
            ax.add_patch(Circle((x, y), 2.75, fc="white", ec=INK, lw=1))
            ax.add_patch(Circle((sx * fx, sy * fy), fd / 2, fc="none", ec=AC, lw=0.8, ls=":"))
    ax.text(L / 2 - ins - 6, -Wd / 2 + ins, "5.5 corner hole, 12 in from both edges", ha="right", va="center", fontsize=7.5, color=INK)
    ax.text(fx - fd / 2 - 4, fy, "rubber foot (underneath),\n150 and 60 from the middle", ha="right", va="center", fontsize=7.5, color=AC)
    for x in (-150, 0, 150):
        ax.plot([x, x], [-Wd / 2 - 2, -Wd / 2 - 12], color=AC, lw=0.4, ls=":")
    ax.text(0, -Wd / 2 - 16, "rail screws at the middle and 150 mm each side of it, on the centre line", ha="center", va="top", fontsize=8, color=AC)
    ax.set_xlim(-L / 2 - 8, L / 2 + 8); ax.set_ylim(-Wd / 2 - 30, Wd / 2 + 8)
    fig.text(0.03, 0.97, "Bench plate: hole layout", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.03, 0.925, "Seen from above, 360 x 180 x 6 mm aluminium. Sizes in mm from the middle of the plate, taken from the model.",
             fontsize=8.5, color=MUT, va="top")
    fig.text(0.03, 0.015, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    fig.text(0.97, 0.015, "github.com/BoujeeEnjinia1701/twinkit", fontsize=7, color=AC, ha="right", family="monospace")
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / "plate-holes.png", facecolor="white"); plt.close(fig); res.append(OUT / "plate-holes.png")

    # enclosure base front wall (elevation) and floor (plan)
    ew, eh = D["enc_w"], P["tray_h"]
    sw, sh = P["vent_slot"]
    fig = plt.figure(figsize=(11, 8.6), dpi=150)
    ax = fig.add_axes([0.05, 0.47, 0.9, 0.38]); ax.set_aspect("equal"); ax.set_axis_off()
    ax.add_patch(Rectangle((-ew / 2, 0), ew, eh, fc="#F3F4F6", ec=INK, lw=1.2))
    for zc in (P["vent_z_low"] - 3.5, P["vent_z_low"] + 3.5):
        ax.add_patch(Rectangle((P["vent_dx"] - sw / 2, zc - sh / 2), sw, sh, fc="white", ec=INK, lw=1))
    ax.text(P["vent_dx"], 17, "vent slots 40 x 4, centred 32 left;\n2.5 to 6.5 and 9.5 to 13.5 up", ha="center", va="bottom", fontsize=7.5, color=INK)
    ze = P["entry_z"]
    for dx, d, fl, name in ((P["rj45"][2], P["rj45"][0], P["rj45"][1], "network coupler\n20 hole, 50 right"),
                            (P["gland"][2], P["gland"][0], P["gland"][1], "power gland\n16.2 hole, 20 right")):
        ax.add_patch(Circle((dx, ze), fl / 2, fc="none", ec=MUT, lw=0.6, ls="--"))
        ax.add_patch(Circle((dx, ze), d / 2, fc="white", ec=INK, lw=1.1))
        ax.plot([dx - fl / 2 - 2, dx + fl / 2 + 2], [ze, ze], color=MUT, lw=0.4); ax.plot([dx, dx], [ze - fl / 2 - 2, ze + fl / 2 + 2], color=MUT, lw=0.4)
        ax.plot([dx, dx], [ze + fl / 2, eh + 3], color=MUT, lw=0.5)
        ax.text(dx, eh + 3.5, name, ha="center", va="bottom", fontsize=7.5, color=INK)
    ax.plot([0, 0], [-1, eh + 1], color=MUT, lw=0.5, ls=(0, (8, 3, 2, 3)))
    ax.plot([ew / 2, ew / 2 + 10], [ze, ze], color=AC, lw=0.5, ls=":"); ax.text(ew / 2 + 11, ze, "26 up", va="center", fontsize=8, color=AC)
    ax.text(-ew / 2, -3, "outside of the floor (rail side)", va="top", fontsize=7.5, color=MUT)
    ax.text(0, -3, "middle", ha="center", va="top", fontsize=7.5, color=MUT)
    ax.set_xlim(-ew / 2 - 6, ew / 2 + 30); ax.set_ylim(-10, eh + 16)
    fig.text(0.04, 0.88, "A. Front wall, seen from the front. The back wall has the same two vent slots and nothing else.", fontsize=9, fontweight="bold", color=INK)
    ax2 = fig.add_axes([0.05, 0.07, 0.9, 0.34]); ax2.set_aspect("equal"); ax2.set_axis_off()
    ax2.add_patch(Rectangle((-ew / 2, -ED / 2), ew, ED, fc="#F3F4F6", ec=INK, lw=1.2))
    ax2.add_patch(Rectangle((-ew / 2, -P["rail"][1] / 2), ew, P["rail"][1], fc="none", ec=MUT, lw=0.6, ls="--"))
    ax2.text(ew / 2 - 2, P["rail"][1] / 2 - 2, "DIN clip under the floor", ha="right", va="top", fontsize=7, color=MUT)
    holes = [(x - XG, y) for x, y in board_holes(P)]
    for x, y in holes:
        ax2.add_patch(Circle((x, y), 1.35, fc="white", ec=INK, lw=1))
        ax2.add_patch(Circle((x, y), 2.5, fc="none", ec=COL["standoffs"], lw=0.8, ls=":"))
    xs = sorted({round(x, 1) for x, _ in holes})
    for x in xs:
        ax2.plot([x, x], [-ED / 2 - 2, -ED / 2 - 8], color=AC, lw=0.4, ls=":")
        ax2.text(x, -ED / 2 - 9, f"{x:+g}", ha="center", va="top", fontsize=7.5, color=AC)
    for y in (-24.5, 24.5):
        ax2.plot([ew / 2 + 2, ew / 2 + 10], [y, y], color=AC, lw=0.4, ls=":")
        ax2.text(ew / 2 + 11, y, f"{y:+g}", va="center", fontsize=7.5, color=AC)
    ax2.text(xs[0] + 29, 0, "four 2.7 holes for the computer,\n58 apart along, 49 apart across", ha="center", va="center", fontsize=7.5, color=INK)
    ax2.text(0, ED / 2 + 2, "back wall", ha="center", va="bottom", fontsize=7.5, color=MUT)
    ax2.text(0, -ED / 2 - 15, "front wall (cable entries)", ha="center", va="top", fontsize=7.5, color=MUT)
    ax2.set_xlim(-ew / 2 - 6, ew / 2 + 30); ax2.set_ylim(-ED / 2 - 22, ED / 2 + 8)
    fig.text(0.04, 0.43, "B. Floor, seen from above (inside). Positions from the middle of the base.", fontsize=9, fontweight="bold", color=INK)
    fig.text(0.03, 0.975, "Gateway enclosure base: cut-outs", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.03, 0.94, "Sizes in mm, taken from the model. Solid outline: the hole to cut. Dashed: the flange of the part that goes in it. "
             "Left and right as seen from the front.", fontsize=8.2, color=MUT, va="top")
    fig.text(0.03, 0.015, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    fig.text(0.97, 0.015, "github.com/BoujeeEnjinia1701/twinkit", fontsize=7, color=AC, ha="right", family="monospace")
    fig.savefig(OUT / "enclosure-holes.png", facecolor="white"); plt.close(fig); res.append(OUT / "enclosure-holes.png")
    return res


# ----------------------------------------------------------------- wiring
def wiring():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
    fig = plt.figure(figsize=(12, 7.2), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 120); ax.set_ylim(0, 72); ax.set_axis_off()
    INK, MUT = "#111827", "#4B5563"
    ax.text(2, 70, "TwinKit prototype: block-level wiring", fontsize=13, fontweight="bold", color=INK, va="top")
    ax.text(2, 66.6, "Bought modules wired at their screw terminals, left to right along the rail. Stranded copper; a ferrule on every screw terminal.",
            fontsize=8.5, color=MUT, va="top")
    ax.text(2, 1.5, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    ax.text(118, 1.5, "github.com/BoujeeEnjinia1701/twinkit", fontsize=7, color="#0F766E", ha="right", family="monospace")

    def blk(x, y, w, h, title, sub, color):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3", fc="white", ec=color, lw=1.8))
        ax.text(x + w / 2, y + h - 1.4, title, ha="center", va="top", fontsize=9, fontweight="bold", color=INK)
        ax.text(x + w / 2, y + h - 4.3, sub, ha="center", va="top", fontsize=7.2, color=MUT, linespacing=1.3)

    def wire(pts, color, lw=2.0):
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round", zorder=1)

    def lab(x, y, text, color, ha="left"):
        ax.text(x, y, text, fontsize=7.2, color=color, ha=ha, va="center", zorder=3,
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))
    RED, BLU, GRY, RF = "#B91C1C", "#1D4ED8", "#6B7280", "#374151"
    blk(2, 44, 14, 12, "12 V adapter", "certified, double\ninsulated, 9 to 30 V", "#111827")
    blk(22, 44, 15, 12, "Fuse and terminals", "3.15 A time-delay\nfuse; + and - blocks", "#D4A017")
    blk(44, 44, 15, 12, "UPS module", "IN, OUT, BAT,\npower-fail contact", "#64748B")
    blk(66, 44, 15, 12, "DC-DC converter", "9 to 30 V in,\n5.1 V 5 A out", "#6B7280")
    blk(44, 18, 15, 12, "Backup pack", "12.8 V 1.5 Ah LiFePO4,\nBMS and fuse inside", "#C2410C")
    ax.add_patch(FancyBboxPatch((86, 12), 30, 46, boxstyle="round,pad=0.4", fc="#F8FAFC", ec="#94A3B8", lw=1, ls="--"))
    ax.text(87.5, 13.2, "Inside the gateway enclosure", fontsize=8, color=MUT, va="bottom")
    blk(89, 36, 24, 14, "Computer", "USB-C power in, GPIO\nthrough the HAT's header,\nnetwork socket", "#15803D")
    blk(89, 16, 24, 10, "Concentrator HAT", "on the 40-pin header,\nU.FL antenna socket", "#0F766E")
    # adapter to fuse to terminals
    wire([(16, 50), (22, 50)], RED); lab(19, 52.5, "0.75 mm²", RED, "center")
    wire([(37, 50), (44, 50)], RED); lab(40.5, 52.5, "0.75 mm²", RED, "center")
    ax.text(40.5, 48.2, "to UPS IN", fontsize=6.8, color=MUT, ha="center")
    wire([(59, 50), (66, 50)], RED); lab(62.5, 52.5, "0.75 mm²", RED, "center")
    ax.text(62.5, 48.2, "UPS OUT", fontsize=6.8, color=MUT, ha="center")
    wire([(51.5, 44), (51.5, 30)], RED); lab(50.8, 34, "BAT, 0.75 mm², through\nthe battery box gland", RED, "right")
    wire([(81, 47), (89, 47)], RED); lab(85, 53, "USB-C lead,\n5 A rated", RED, "center")
    wire([(56, 44), (56, 39), (89, 39)], BLU, 1.4); lab(72.5, 41.2, "power-fail contact to a free GPIO and ground, 0.25 mm²", BLU, "center")
    wire([(101, 36), (101, 26)], GRY, 1.4); lab(101.8, 31, "header", GRY)
    wire([(113, 21), (117, 21), (117, 62), (101, 62)], RF, 1.2); lab(116.5, 54, "U.FL pigtail to\nthe antenna bulkhead", RF, "right")
    ax.text(109, 62.6, "antenna on the cover", fontsize=7, color=RF, ha="center", va="bottom")
    wire([(95, 50), (95, 62), (66, 62)], "#0E7490", 1.4); lab(66, 64, "patch lead to the network coupler and site network", "#0E7490")
    ax.text(3, 9.6, "Safety: the pack lead stays unplugged from the UPS BAT terminals until stop S3 of the plan. The adapter stays unplugged until stop S2.",
            fontsize=7.6, color="#B45309", fontweight="bold")
    ax.text(3, 6.2, "Red: power. Blue: signal. Grey: board header. Teal: Ethernet. The USB-C lead and power-fail wires enter through the power gland. "
            "All circuits are extra-low voltage: 14.6 V highest (pack charging).",
            fontsize=7.2, color=MUT)
    out = OUT / "wiring.png"
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


if __name__ == "__main__":
    what = sys.argv[1:] or ["overview", "sheets", "layouts", "joints", "steps", "wiring"]
    fns = {"overview": overview, "sheets": sheets, "layouts": layouts, "joints": joints, "steps": steps, "wiring": wiring}
    for w in what:
        r = fns[w]()
        print(w, "->", r)
