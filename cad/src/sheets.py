"""TwinKit general arrangement sheet TWK-DWG-001, Rev P3 (TRL 3, constructable design).

Run from the repo root:  python cad/src/sheets.py
Writes cad/drawings/TWK-DWG-001.svg, .pdf and .png from the parametric model in
cad/src/model.py with .kit/drawing.py. Dimensions are taken from PARAMS and derived(), so
they follow any parameter change. The concept blueprint in media/ is TWK-DWG-010.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from drawing import Sheet, _viewbox, _t, M, TB_Y, INK, MUTED  # noqa: E402
from model import PARAMS as P, assembly, derived  # noqa: E402

DATE = "2026-09-25"
DATE_P3 = "2026-10-02"


def safe_project_views(part, workdir, line_weight=0.35):
    """Same views as drawing.project_views, edge by edge, so a degenerate edge is skipped."""
    from build123d import ExportSVG, LineType, Unit
    workdir = Path(workdir); workdir.mkdir(parents=True, exist_ok=True)
    bb = part.bounding_box()
    c = bb.center(); d = max(bb.size.X, bb.size.Y, bb.size.Z) * 10
    setups = {"front": ((c.X, c.Y - d, c.Z), (0, 0, 1)), "top": ((c.X, c.Y, c.Z + d), (0, 1, 0)),
              "right": ((c.X + d, c.Y, c.Z), (0, 0, 1)), "iso": ((c.X + d, c.Y - d, c.Z + d * 0.8), (0, 0, 1))}
    out, skipped = {}, 0
    for name, (origin, up) in setups.items():
        visible, hidden = part.project_to_viewport(origin, up, (c.X, c.Y, c.Z))
        ex = ExportSVG(unit=Unit.MM, line_weight=line_weight)
        ex.add_layer("Visible", line_color=0x111827)
        ex.add_layer("Hidden", line_color=0x6B7280, line_type=LineType.ISO_DASH, line_weight=line_weight / 2)
        for layer, edges in (("Visible", visible), ("Hidden", hidden if name != "iso" else [])):
            for e in edges:
                try:
                    ex.add_shape(e, layer=layer)
                except (AssertionError, ValueError, ZeroDivisionError):
                    skipped += 1
        p = workdir / f"{name}.svg"
        ex.write(str(p))
        out[name] = p
    print(f"projected views; skipped {skipped} degenerate edges")
    return out


def ortho_cells(sheet, views, names=("front", "top", "right")):
    """Repeat Sheet.add_ortho's layout arithmetic to find where each view lands (x, y, w, h)."""
    ax, ay, aw, ah = M + 10, M + 16, 245, TB_Y - M - 20
    gap, lab, dl = 14, 12, 11
    dims = {n: _viewbox(Path(views[n]).read_text())[2:] for n in names}
    fw, fh = dims["front"]; tw, th = dims["top"]; rw, rh = dims["right"]
    k = sheet.scale
    ax += (aw - (k * (max(fw, tw) + rw) + gap + dl)) / 2 + dl
    ay += (ah - (k * (th + max(fh, rh)) + gap + 2 * lab + dl)) / 2 + dl
    colw = k * max(fw, tw)
    front_y = ay + k * th + lab + gap
    row_h = k * max(fh, rh)
    return {"top": (ax, ay, colw, k * th), "front": (ax, front_y, colw, row_h),
            "right": (ax + colw + gap, front_y, k * rw, row_h)}


def dim_h(x1, x2, y, text):
    a = 1.4
    return [f'<line x1="{x1:.2f}" y1="{y:.2f}" x2="{x2:.2f}" y2="{y:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x1:.2f} {y:.2f} l{a} -0.5 l0 1 Z" fill="{INK}"/>',
            f'<path d="M{x2:.2f} {y:.2f} l{-a} -0.5 l0 1 Z" fill="{INK}"/>',
            _t((x1 + x2) / 2, y - 1.0, text, 2.3, 400, INK, "middle", mono=True)]


def dim_v(x, y1, y2, text, side=-1):
    a = 1.4
    cx, cy = x + side * 1.0, (y1 + y2) / 2
    return [f'<line x1="{x:.2f}" y1="{y1:.2f}" x2="{x:.2f}" y2="{y2:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x:.2f} {y1:.2f} l-0.5 {a} l1 0 Z" fill="{INK}"/>',
            f'<path d="M{x:.2f} {y2:.2f} l-0.5 {-a} l1 0 Z" fill="{INK}"/>',
            f'<g transform="rotate(-90 {cx:.2f} {cy:.2f})">{_t(cx, cy, text, 2.3, 400, INK, "middle", mono=True)}</g>']


def ext(x1, y1, x2, y2):
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{MUTED}" stroke-width="0.13"/>'


def leader(x1, y1, x2, y2, text, anchor="start"):
    return [f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{MUTED}" stroke-width="0.15"/>',
            f'<circle cx="{x1:.2f}" cy="{y1:.2f}" r="0.5" fill="{INK}"/>',
            _t(x2 + (1 if anchor == "start" else -1), y2 + 0.8, text, 2.1, 400, INK, anchor)]


def main():
    D = derived(P)
    work = ROOT / "cad" / "drawings" / "_views"
    asm = assembly()
    views = safe_project_views(asm, work)
    bb = asm.bounding_box()
    s = Sheet(project="TwinKit", title="General arrangement, edge gateway", dwg_no="TWK-DWG-001", rev="P3",
              author="Amish Chadha", date=DATE_P3, scale=None, theme="technical",
              material="Bought-in DIN modules per bom/bom.csv. PRELIMINARY, NOT FOR FABRICATION",
              revisions=[("P1", "Preliminary GA for TRL 3 (from cad/src/model.py)", DATE, "AC"),
                         ("P2", "Layout and labels tidied", DATE, "AC"),
                         ("P3", "Constructable design: vents in long walls, battery box, end stops, fixings (TWK-DDR-003)", DATE_P3, "AC")])
    s.add_ortho(views)
    k = s.scale
    c = ortho_cells(s, views)
    L = []
    ew, ed, eh = D["enc_w"], P["enc_d"], P["enc_h"]
    xg = P["x_gw"]
    zr = D["rail_z"]

    # front view (from -Y): X right, Z up
    x, y, w, h = c["front"]
    X = lambda mx: x + (mx - bb.min.X) * k
    Z = lambda mz: y + h - (mz - bb.min.Z) * k
    xr = X(bb.max.X) + 5
    for i, (zz, label) in enumerate(((D["enc_top_z"], f"{D['enc_top_z']:.1f}"),
                                     (D["antenna_top_z"], f"{D['antenna_top_z']:.0f} ANTENNA TIP"))):
        xd = xr + 7 * i
        L.append(ext(X(xg + ew / 2 if i == 0 else xg - 30), Z(zz), xd + 1, Z(zz)))
        L += dim_v(xd, Z(zz), Z(0), label, side=3)
    L.append(ext(X(D["rail_right"]), Z(0), xr + 8, Z(0)))
    L += leader(X(xg - 30), Z(D["antenna_top_z"] - 60), X(xg - 30) + 8, Z(D["antenna_top_z"] - 40), "9 ANTENNA, SMA BULKHEAD")
    L += leader(X(xg + P["vent_dx"] - 15), Z(zr + P["vent_z_high"]), X(xg + 40), Z(zr + P["vent_z_high"] + 45), "VENTS IN BOTH LONG WALLS")
    L.append(_t(X(bb.max.X), Z(0) + 4, "PLATE TOP Z = 0", 1.9, 400, MUTED, "end"))

    # top view (from +Z): X right, Y up
    x, y, w, h = c["top"]
    Xt = lambda mx: x + (mx - bb.min.X) * k
    Yt = lambda my: y + h - (my - bb.min.Y) * k
    ya = Yt(bb.max.Y) - 12
    L += [ext(Xt(D["rail_left"]), Yt(ed / 2), Xt(D["rail_left"]), ya - 1),
          ext(Xt(D["rail_right"]), Yt(ed / 2), Xt(D["rail_right"]), ya - 1)]
    L += dim_h(Xt(D["rail_left"]), Xt(D["rail_right"]), ya, f"{D['rail_used_mm']:.0f} RAIL USED ({D['rail_used_modules']:.1f} MODULES)")
    yb = ya - 7
    L += [ext(Xt(xg - ew / 2), Yt(ed / 2), Xt(xg - ew / 2), yb - 1), ext(Xt(xg + ew / 2), Yt(ed / 2), Xt(xg + ew / 2), yb - 1)]
    L += dim_h(Xt(xg - ew / 2), Xt(xg + ew / 2), yb, f"{ew:.1f} (9 MODULES)")

    # right view (from +X): Y right, Z up
    x, y, w, h = c["right"]
    Yr = lambda my: x + (my - bb.min.Y) * k
    Zr = lambda mz: y + h - (mz - bb.min.Z) * k
    zt = D["enc_top_z"] + 30
    L += [ext(Yr(-ed / 2), Zr(D["enc_top_z"]), Yr(-ed / 2), Zr(zt) - 1), ext(Yr(ed / 2), Zr(D["enc_top_z"]), Yr(ed / 2), Zr(zt) - 1)]
    L += dim_h(Yr(-ed / 2), Yr(ed / 2), Zr(zt), f"{ed:.0f}")

    s._layers += L
    s.add_svg(views["iso"], 276, 34, 140, 98, label="Isometric view", sublabel="Not to scale")
    m = P["module"]
    s.add_notes("Main dimensions and interfaces (mm)", [
        f"TS35 x 7.5 rail, {P['rail'][0]:.0f} long, on 3 M4 screws; module pitch {m}",
        f"13 terminals, fuse | 3, 4 enclosure {P['enc_modules']} mod | 10 DC-DC {P['psu_modules']} mod | 11 UPS {P['ups_modules']} mod",
        f"17 battery box {P['box_modules']} mod holding 12 pack (12.8 V, 1.5 Ah) | 18 end stops",
        f"Enclosure {ew:.1f} x {ed:.0f} x {eh:.0f} above the rail; top {D['enc_top_z']:.1f} above the plate",
        f"Vents {D['vent_low_mm2']:.0f} mm2 low and high, {D['vent_stack_mm']:.0f} apart (TWK-CAL-001 F)",
        f"5 board {P['sbc'][0]:.0f} x {P['sbc'][1]:.0f} on {P['sbc_standoff']:.0f} standoffs; 7 HAT on {P['hat_standoff']:.0f} standoffs",
        "20 RJ45 coupler and cable glands in the -Y walls; 9 to 30 V DC in",
        f"Plate {P['plate'][0]:.0f} x {P['plate'][1]:.0f} x {P['plate'][2]:.0f} aluminium; omit in a cabinet",
        "Third-angle; front view from -Y; X along the rail",
    ], x=276, y=158, width=140)
    out = s.save(ROOT / "cad" / "drawings" / "TWK-DWG-001")
    shutil.rmtree(work, ignore_errors=True)
    print(f"wrote {out} and .pdf, .png at scale 1:{1 / k:g}")


if __name__ == "__main__":
    main()
