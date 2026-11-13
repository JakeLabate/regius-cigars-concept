"""Original, generic cigar drawings to one scale. No Regius artwork is reproduced:
bands are plain colour fields with rules, wrappers are flat leaf tones from palette tokens.

Scale: 100 SVG units = 1 inch. Ring gauge is diameter in 64ths of an inch.
Every colour comes from a CSS class that resolves to a :root token.
"""
import math

S = 100.0          # units per inch
VB_W = 860         # shared viewBox width, so every drawing is at one scale
X0 = 20            # head of the cigar starts here

_uid = [0]


def uid():
    _uid[0] += 1
    return f"g{_uid[0]}"


def parse_in(s):
    """'4 7/8' -> 4.875"""
    total = 0.0
    for part in str(s).split():
        if "/" in part:
            a, b = part.split("/")
            total += float(a) / float(b)
        else:
            total += float(part)
    return total


def mm_len(s):
    return round(parse_in(s) * 25.4)


def mm_dia(ring):
    return round(ring / 64 * 25.4, 1)


def f(n):
    return f"{n:.1f}"


def body_path(L, T, cy, shape, T2=None):
    x0, x1 = X0, X0 + L
    top, bot = cy - T / 2, cy + T / 2
    if shape == "parejo":
        r = T * 0.5
        return (f"M{f(x0 + r)},{f(top)} L{f(x1)},{f(top)} L{f(x1)},{f(bot)} L{f(x0 + r)},{f(bot)} "
                f"C{f(x0 + r * .3)},{f(bot)} {f(x0)},{f(cy + T * .3)} {f(x0)},{f(cy)} "
                f"C{f(x0)},{f(cy - T * .3)} {f(x0 + r * .3)},{f(top)} {f(x0 + r)},{f(top)} Z")
    if shape == "torpedo":
        tl = min(1.3 * S, L * 0.28)
        return (f"M{f(x0 + tl)},{f(top)} L{f(x1)},{f(top)} L{f(x1)},{f(bot)} L{f(x0 + tl)},{f(bot)} "
                f"C{f(x0 + tl * .55)},{f(bot)} {f(x0 + tl * .16)},{f(cy + T * .15)} {f(x0)},{f(cy)} "
                f"C{f(x0 + tl * .16)},{f(cy - T * .15)} {f(x0 + tl * .55)},{f(top)} {f(x0 + tl)},{f(top)} Z")
    if shape == "perfecto":
        hl, fl = 1.15 * S, 0.85 * S
        t0, f0 = T * 0.13, T * 0.2
        return (f"M{f(x0)},{f(cy - t0)} C{f(x0 + hl * .3)},{f(cy - T * .34)} {f(x0 + hl * .6)},{f(top)} {f(x0 + hl)},{f(top)} "
                f"L{f(x1 - fl)},{f(top)} C{f(x1 - fl * .45)},{f(top)} {f(x1 - fl * .15)},{f(cy - T * .36)} {f(x1)},{f(cy - f0)} "
                f"L{f(x1)},{f(cy + f0)} C{f(x1 - fl * .15)},{f(cy + T * .36)} {f(x1 - fl * .45)},{f(bot)} {f(x1 - fl)},{f(bot)} "
                f"L{f(x0 + hl)},{f(bot)} C{f(x0 + hl * .6)},{f(bot)} {f(x0 + hl * .3)},{f(cy + T * .34)} {f(x0)},{f(cy + t0)} Z")
    if shape == "fatperfecto":
        # T is the ring at the shoulder, T2 the widest point, near the foot third.
        hl, fl = 1.1 * S, 0.8 * S
        t0, f0 = T * 0.13, T2 * 0.2
        xm = x0 + L * 0.66
        return (f"M{f(x0)},{f(cy - t0)} C{f(x0 + hl * .3)},{f(cy - T * .34)} {f(x0 + hl * .6)},{f(cy - T / 2)} {f(x0 + hl)},{f(cy - T / 2)} "
                f"C{f(x0 + L * .4)},{f(cy - T / 2)} {f(xm - L * .12)},{f(cy - T2 / 2)} {f(xm)},{f(cy - T2 / 2)} "
                f"C{f(x1 - fl * .5)},{f(cy - T2 / 2)} {f(x1 - fl * .12)},{f(cy - T2 * .38)} {f(x1)},{f(cy - f0)} "
                f"L{f(x1)},{f(cy + f0)} C{f(x1 - fl * .12)},{f(cy + T2 * .38)} {f(x1 - fl * .5)},{f(cy + T2 / 2)} {f(xm)},{f(cy + T2 / 2)} "
                f"C{f(xm - L * .12)},{f(cy + T2 / 2)} {f(x0 + L * .4)},{f(cy + T / 2)} {f(x0 + hl)},{f(cy + T / 2)} "
                f"C{f(x0 + hl * .6)},{f(cy + T / 2)} {f(x0 + hl * .3)},{f(cy + T * .34)} {f(x0)},{f(cy + t0)} Z")
    raise ValueError(shape)


def veins(L, T, cy, seed):
    """A few leaf veins, clipped to the body. Deterministic."""
    out = []
    n = max(3, int(L / 115))
    for i in range(n):
        x = X0 + L * (0.12 + 0.8 * (i + 0.5) / n) + ((seed * 37 + i * 53) % 40) - 20
        lean = 26 + ((seed * 11 + i * 29) % 22)
        out.append(f'<path class="vein" d="M{f(x)},{f(cy - T / 2 - 2)} q{f(lean * .35)},{f(T * .5)} {f(lean)},{f(T + 4)}"/>')
    return "".join(out)


def band_group(kind, bx, T, cy, second=None):
    if not kind:
        return ""
    bw = 0.6 * S
    y, h = cy - T / 2 - 3, T + 6
    g = [f'<rect class="band b-{kind}" x="{f(bx)}" y="{f(y)}" width="{f(bw)}" height="{f(h)}"/>',
         f'<rect class="rule r-{kind}" x="{f(bx + 5)}" y="{f(y)}" width="2.2" height="{f(h)}"/>',
         f'<rect class="rule r-{kind}" x="{f(bx + bw - 7.2)}" y="{f(y)}" width="2.2" height="{f(h)}"/>']
    if second:
        sx, sw = bx + bw + 7, 0.2 * S
        g.append(f'<rect class="band b-{second}" x="{f(sx)}" y="{f(y)}" width="{f(sw)}" height="{f(h)}"/>')
    return "".join(g)


def cigar(length, ring, leaf, shape="parejo", band="black", second=None, ring2=None,
          label="", pad=14, extra="", show_ring=False, cy=None, H=None):
    """One cigar, head to the left, on the shared scale. Returns an <svg> string."""
    L = parse_in(length) * S
    T = ring / 64 * S
    Tmax = (ring2 or ring) / 64 * S
    if H is None:
        H = Tmax + pad * 2
    if cy is None:
        cy = pad + Tmax / 2
    cid = uid()
    seed = int(L) + ring
    if shape == "fatperfecto":
        d = body_path(L, T, cy, shape, T2=Tmax)
    else:
        d = body_path(L, T, cy, shape)
    head = {"parejo": 0.92, "torpedo": 1.45, "perfecto": 1.3, "fatperfecto": 1.25}[shape] * S
    bx = X0 + min(head, L * 0.3)
    foot = ""
    if shape in ("parejo", "torpedo"):
        foot = f'<ellipse class="foot" cx="{f(X0 + L)}" cy="{f(cy)}" rx="{f(max(2.2, T * .045))}" ry="{f(T / 2)}"/>'
    ringmark = ""
    if show_ring:
        rx = VB_W - 14 - T / 2
        ringmark = (f'<circle class="leaf-{leaf} ringedge" cx="{f(rx)}" cy="{f(cy)}" r="{f(T / 2)}"/>'
                    f'<circle class="foot-in" cx="{f(rx)}" cy="{f(cy)}" r="{f(T / 2 * .82)}"/>'
                    f'<path class="vein" d="M{f(rx - T * .28)},{f(cy)} q{f(T * .14)},{f(-T * .2)} {f(T * .28)},0 t{f(T * .28)},0"/>')
    title = ""
    aria = f'role="img" aria-label="{label}"' if label else 'aria-hidden="true"'
    return (f'<svg class="cigar" viewBox="0 0 {VB_W} {f(H)}" {aria} focusable="false">{title}'
            f'<defs><clipPath id="{cid}"><path d="{d}"/></clipPath></defs>'
            f'<g class="shadowed">'
            f'<path class="leaf-{leaf}" d="{d}"/>'
            f'<g clip-path="url(#{cid})">{veins(L, Tmax, cy, seed)}{band_group(band, bx, Tmax, cy, second)}'
            f'<rect class="shade" x="0" y="{f(cy - Tmax / 2)}" width="{VB_W}" height="{f(Tmax)}"/></g>'
            f'{foot}<path class="outline" d="{d}"/></g>{ringmark}{extra}</svg>')


def culebra(length, ring, leaves, label=""):
    """Three cigars twisted together, as a culebra is sold."""
    L = parse_in(length) * S
    T = ring / 64 * S
    amp = T * 0.62
    wave = 1.95 * S
    H = T + amp * 2 + 30
    cy = H / 2
    strands = []
    for k, leaf in enumerate(leaves):
        pts = []
        steps = 90
        for i in range(steps + 1):
            x = X0 + T / 2 + (L - T) * i / steps
            y = cy + amp * math.sin(2 * math.pi * (x - X0) / wave + k * 2 * math.pi / 3)
            pts.append(f"{f(x)},{f(y)}")
        d = "M" + " L".join(pts)
        strands.append(f'<path class="strand-edge" d="{d}" stroke-width="{f(T + 2.6)}"/>'
                       f'<path class="strand st-{leaf}" d="{d}" stroke-width="{f(T)}"/>')
    ties = "".join(
        f'<rect class="band b-gold" x="{f(x)}" y="{f(cy - amp - T / 2 - 2)}" width="9" height="{f(amp * 2 + T + 4)}" rx="2"/>'
        for x in (X0 + 0.55 * S, X0 + L - 0.55 * S - 9))
    title = ""
    aria = f'role="img" aria-label="{label}"' if label else 'aria-hidden="true"'
    return (f'<svg class="cigar" viewBox="0 0 {VB_W} {f(H)}" {aria} focusable="false">{title}'
            f'<g class="shadowed">{"".join(strands)}{ties}</g></svg>')


def ruler(inches=8, y0=6, numerals=True):
    """An inch ruler on the same scale as the drawings."""
    parts = [f'<line class="tick" x1="{X0}" y1="{y0}" x2="{f(X0 + inches * S)}" y2="{y0}"/>']
    for q in range(inches * 4 + 1):
        x = X0 + q * S / 4
        h = 18 if q % 4 == 0 else (11 if q % 2 == 0 else 6)
        parts.append(f'<line class="tick" x1="{f(x)}" y1="{y0}" x2="{f(x)}" y2="{y0 + h}"/>')
        if numerals and q % 4 == 0:
            parts.append(f'<text class="num" x="{f(x)}" y="{y0 + 38}" text-anchor="middle">{q // 4}</text>')
    return "".join(parts)


def ruler_svg(inches=8):
    return (f'<svg class="ruler" viewBox="0 0 {VB_W} 52" aria-hidden="true" focusable="false">'
            f'{ruler(inches)}<text class="num unit" x="{f(X0 + inches * S + 14)}" y="44">in</text></svg>')


def plate(length, ring, leaf, label, band="black"):
    """Hero plate: the cigar, its ring seen end on, and the ruler beneath.
    Height and centre line are fixed so the plate does not jump when sizes are switched."""
    pad = 18
    tmax = 60 / 64 * S
    cy = pad + tmax / 2
    ry = pad * 2 + tmax + 4
    extra = (f'<g transform="translate(0,{f(ry)})">{ruler(8, 0)}'
             f'<text class="num unit" x="{f(X0 + 8 * S + 14)}" y="38">in</text></g>')
    return cigar(length, ring, leaf, band=band, label=label, extra=extra,
                 show_ring=True, cy=cy, H=ry + 52)


DEFS = ('<svg class="svg-defs" aria-hidden="true" focusable="false"><defs>'
        '<linearGradient id="cyl" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" class="s-hi" stop-opacity=".04"/>'
        '<stop offset=".2" class="s-hi" stop-opacity=".3"/>'
        '<stop offset=".48" class="s-lo" stop-opacity="0"/>'
        '<stop offset="1" class="s-lo" stop-opacity=".58"/>'
        '</linearGradient></defs></svg>')
