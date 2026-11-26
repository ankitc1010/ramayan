"""Painted flora: every leaf drawn with cairo, light over dark, with ink; stood in 3-D as cards.

    from worlds import flora as FL
    FL.tree(st, 'pahari_round', (x, 0, z), 60, season='spring', seed=1)        # between st.open and st.close
    FL.scatter(st, 'shrub', P, height=6, season='monsoon', haze=.3, hazeCol='#c8d8c0')   # P Nx3, one call, any number
    FL.frame(st, 'fg_leaves', x, y, scale, rot=, flip=, lod=2, tint=)           # after st.close: a blurred leaf mass near the lens, pixels
    FL.plate_of('banyan', 'summer', 0) -> Plate(tex, w, h, ax, ay, top)         # the raw texture: ax, ay = foot in px (y down), top = y of the crown's top

Height is the painted height (foot to top) in world units; people are 15.5 tall, so trees are 45 to 160 high, shrubs 6 to 14, grass 4 to 10.
SEASONS spring summer monsoon autumn winter (gold = for the ashoka / festive).  All cards are class 6 (flat paint): they take the light's mix of key and ambient, the fog, and flame points.
KINDS is the registry (kind -> painter, size, variants)."""
import numpy as np, math, cairo, hashlib, inspect
import moderngl as mgl
from dataclasses import dataclass
from lau import gl
from lau.plates import plate, rgb, poly, smooth_path, ink
from lau.stage import hexc

VER = 1
TAU = 2 * math.pi
# dark, low, mid, light, high, ink
GREEN = dict(
    spring=('#1d4630', '#3c7538', '#7aa93f', '#b6d25a', '#ecf2a6', '#152a1c'),
    summer=('#10352a', '#1d5a36', '#3a8143', '#74aa4c', '#bfd676', '#0c1f1a'),
    monsoon=('#05211f', '#0b4034', '#14644a', '#2d8d5c', '#7cbf7c', '#031413'),
    autumn=('#561a14', '#943510', '#cb661c', '#e8a031', '#fbdb74', '#2b0c0c'),
    winter=('#4b5360', '#6d7a80', '#97a39e', '#c2c9bb', '#ecece0', '#252a38'),
    gold=('#4a1e12', '#8a4a14', '#c88a28', '#edc255', '#fff0b0', '#250d0a'),
    night=('#081428', '#10243f', '#1c3a58', '#33597a', '#6f9ab4', '#040818'))
BARK = dict(spring=('#7d5a4c', '#4b2f2e', '#b28c74'), summer=('#6b4c3e', '#3b2527', '#a07c62'), monsoon=('#3f3432', '#1c1719', '#75685c'), autumn=('#75503c', '#40251f', '#b58a62'), winter=('#6a6168', '#39333f', '#aaa5a6'),
            gold=('#6b4030', '#361b1a', '#a8764c'), night=('#252a40', '#101326', '#4c5878'))
FLOWER = dict(red=('#7a0d14', '#c5211c', '#ee5a24', '#ffa04a'), pink=('#b04a70', '#dd7d98', '#f5b4bc', '#fff0ee'), white=('#a8a8b8', '#dcdcd8', '#f8f6ea', '#ffffff'), gold=('#b06a10', '#e09a1c', '#f8c63c', '#fff0a0'), blue=('#2a3a86', '#4d64b8', '#8ba2e0', '#d8e4ff'))


def mixc(a, b, t):
    A, B = rgb(a), rgb(b); return tuple(x + (y - x) * t for x, y in zip(A, B))


def ramp(pal, v):
    """colour at 0..1 along the five pigments"""
    v = min(.9999, max(0., v)) * 4; i = int(v); return mixc(pal[i], pal[i + 1], v - i)


# ------------------------------------------------------------------ marks
def leaf(c, x, y, a, l, w, col, dark=None, line=None, lw=1., vein=None, curl=.0, tip=.1):
    """one leaf from its stalk at (x, y) pointing at angle a (radians, y down); two-tone if dark is given"""
    ca, sa = math.cos(a), math.sin(a)
    def P(u, v): v += curl * l * u * u; return x + ca * u * l - sa * v, y + sa * u * l + ca * v
    p = [P(0, 0), P(.18, -w * .62), P(.62, -w * .62), P(1, 0), P(.62, w * .62), P(.18, w * .62)]; m1, m2 = P(1 - tip, -w * .08), P(1 - tip, w * .08)
    c.move_to(*p[0]); c.curve_to(*p[1], *p[2], *m1); c.line_to(*p[3]); c.line_to(*m2); c.curve_to(*p[4], *p[5], *p[0]); c.close_path()
    c.set_source_rgb(*col)
    if line: c.fill_preserve(); c.set_source_rgb(*line); c.set_line_width(lw); c.stroke()
    else: c.fill()
    if dark:
        q = P(.5, w * .04); c.move_to(*p[0]); c.curve_to(*P(.3, w * .06), *q, *p[3]); c.curve_to(*P(.62, w * .52), *P(.18, w * .52), *p[0]); c.close_path(); c.set_source_rgb(*dark); c.fill()
    if vein: c.move_to(*P(.06, 0)); c.line_to(*P(.92, 0)); c.set_source_rgb(*vein); c.set_line_width(max(.6, lw * .9)); c.stroke()


def flower(c, x, y, r, pal, n=5, rot=0., line='#3a0a14', lw=1.):
    for k in range(n):
        a = rot + k * TAU / n; leaf(c, x, y, a, r, r * .9, rgb(pal[2]), rgb(pal[1]), rgb(line), lw, tip=.25)
    c.arc(x, y, r * .22, 0, TAU); c.set_source_rgb(*rgb(pal[3])); c.fill()


def rosette(c, x, y, r, n, a0, spread, pal, v, rng, wd=.42, lw=1., vein=True, curl=.12, two=True):
    """a spray of leaves from one twig, the near leaves last"""
    ang = a0 + np.linspace(-.5, .5, n) * spread; o = np.argsort(-np.abs(ang - a0))
    for i in o:
        s = r * rng.uniform(.78, 1.12); t = v + rng.uniform(-.10, .10) - .10 * abs(i - (n - 1) / 2) / n
        col = ramp(pal, t); leaf(c, x, y, ang[i] + rng.uniform(-.10, .10), s, s * wd, col, ramp(pal, t - .16) if two else None, rgb(pal[5]), lw, ramp(pal, t + .18) if vein else None, curl=rng.uniform(-curl, curl))


def scallop(cx, cy, rx, ry, rng, n=26, amp=.10):
    a = np.linspace(0, TAU, n, endpoint=False); k = 1 + amp * np.where(np.arange(n) % 2, 1, -1) * rng.uniform(.4, 1., n)
    return smooth_path(np.c_[cx + rx * k * np.cos(a), cy + ry * k * np.sin(a)], 6, True)


def clump(c, cx, cy, rx, ry, pal, rng, r=26, n=None, per=7, spread=2.6, wd=.42, lw=1.2, sun=(-.55, -.83), hang=.5, base=.0, gain=1., vein=True, flowers=None, fden=.0, frad=9, two=True, gap=1., ground=True):
    """one rounded mass of foliage: dark ground, then sprays laid like scales from the shaded side to the lit side, outermost ones breaking the outline"""
    if ground:
        poly(c, scallop(cx, cy, rx * .95, ry * .95, rng)); g = cairo.LinearGradient(cx - rx * .5, cy - ry, cx + rx * .4, cy + ry); g.add_color_stop_rgb(0, *ramp(pal, .16 + base)); g.add_color_stop_rgb(1, *ramp(pal, .0)); c.set_source(g); c.fill_preserve(); c.set_source_rgb(*rgb(pal[5])); c.set_line_width(lw * 2); c.stroke()
    n = n or int(rx * ry * 3.14 / (r * r * 1.05) * gap); k = np.arange(n) + .5; rr = np.sqrt(k / n) * 1.0; th = k * 2.399963 + rng.uniform(0, 6)
    X = cx + rx * rr * np.cos(th) + rng.normal(0, r * .16, n); Y = cy + ry * rr * np.sin(th) + rng.normal(0, r * .16, n)
    u = (X - cx) / rx; w = (Y - cy) / ry; z = np.sqrt(np.clip(1 - u * u - w * w, 0, 1)); L = u * sun[0] + w * sun[1]
    v = .34 + .50 * np.sign(L) * np.abs(L) ** 1.15 + .12 * z; o = np.argsort(L + rng.normal(0, .12, n))
    for i in o:
        out = math.atan2(w[i] + 1e-4, u[i] + 1e-4); a = out
        # leaves hang: turn the spray toward the ground
        d = np.array([math.cos(out) * (.25 + rr[i]), math.sin(out) * (.25 + rr[i]) + hang]); a = math.atan2(d[1], d[0]) + rng.normal(0, .25)
        rosette(c, X[i], Y[i], r * rng.uniform(.85, 1.12), per, a, spread, pal, base + gain * v[i], rng, wd, lw, vein, two=two)
        if flowers and rng.uniform() < fden: flower(c, X[i] + rng.normal(0, r * .4), Y[i] + rng.normal(0, r * .4), frad * rng.uniform(.8, 1.2), flowers, 5, rng.uniform(0, 6))


def limb(c, P, w, bark, inkc, rng, lw=2.4, n=14, rings=0., stroke=1., wob=1.):
    """a trunk or branch along P with widths w: flat pigment, lit left edge, shaded right edge, bark strokes, ink sides"""
    P = smooth_path(P, n); k = len(P); t = np.linspace(0, 1, k); W = np.interp(t, np.linspace(0, 1, len(w)), w) * (1 + wob * .05 * np.sin(t * 17 + rng.uniform(0, 6)) + wob * .03 * np.sin(t * 41 + rng.uniform(0, 6)))
    d = np.gradient(P, axis=0); N = np.stack([-d[:, 1], d[:, 0]], 1); N /= np.linalg.norm(N, axis=1, keepdims=True) + 1e-9
    if N[:, 0].mean() < 0: N = -N                                      # N points to screen right
    A, B = P - N * W[:, None] * .5, P + N * W[:, None] * .5
    poly(c, np.vstack([A, B[::-1]])); c.set_source_rgb(*rgb(bark[0])); c.fill()
    e = .10 + .12 * np.sin(t * 23 + rng.uniform(0, 6))
    poly(c, np.vstack([P + N * (W * (.06 + e))[:, None], B[::-1]])); c.set_source_rgba(*rgb(bark[1]), .80); c.fill()
    poly(c, np.vstack([A, (P - N * (W * (.30 + .5 * e))[:, None])[::-1]])); c.set_source_rgba(*rgb(bark[2]), .75); c.fill()
    L = np.linalg.norm(np.diff(P, axis=0), axis=1).sum()
    for _ in range(int(stroke * L * np.mean(W) / 900)):
        i0 = rng.integers(0, max(1, k - 6)); ln = rng.integers(4, max(6, k // 4)); i1 = min(k, i0 + ln)
        if i1 - i0 < 4: continue
        s = rng.uniform(-.46, .46); q = P[i0:i1] + N[i0:i1] * (W[i0:i1] * (s + .05 * np.sin(np.arange(i1 - i0) * .7 + rng.uniform(0, 6))))[:, None]
        dark = rng.uniform() < .68; ink(c, q, rng.uniform(1., 2.6) * lw * .5, bark[1] if dark else bark[2], alpha=.75, seed=int(rng.integers(1e6)))
    if rings:
        for s in np.arange(0, L, rings):
            i = min(k - 1, int(s / L * k)); a = np.linspace(-1, 1, 9); q = P[i] + N[i] * (W[i] * .5 * a)[:, None] + np.c_[np.zeros(9), (1 - a * a) * rings * .28]; ink(c, q, lw * 1.0, bark[1], alpha=.85, seed=i)
    ink(c, A, lw * 1.3, inkc, (.02, .25)); ink(c, B, lw * 1.8, inkc, (.02, .25))
    return P


def roots(c, x, y, w, bark, inkc, rng, n=5, spread=1.6, dy=30):
    for k in np.argsort(-np.abs(np.linspace(-1, 1, n))):
        s = np.linspace(-1, 1, n)[k]; limb(c, [(x + s * w * .30, y - w * .75), (x + s * w * .62, y - w * .16), (x + s * w * spread * rng.uniform(.8, 1.1), y + dy * rng.uniform(.0, .5))], [w * .34, w * .30, 4], bark, inkc, rng, stroke=.6)


def wash(c, w, h, rng, n=400, amt=.018):
    """gouache granulation inside what is already painted"""
    c.save(); c.set_operator(cairo.OPERATOR_ATOP)
    for _ in range(n):
        x, y, r = rng.uniform(0, w), rng.uniform(0, h), rng.uniform(.02, .12) * h; g = cairo.RadialGradient(x, y, 0, x, y, r); k = rng.choice([0., 1.]); g.add_color_stop_rgba(0, k, k, k * .9, amt); g.add_color_stop_rgba(1, k, k, k, 0); c.set_source(g); c.arc(x, y, r, 0, TAU); c.fill()
    c.restore()


def shade(c, w, h, top, bot, a):
    """a painter's glaze over the painted pixels: top colour to bottom colour"""
    c.save(); c.set_operator(cairo.OPERATOR_ATOP); g = cairo.LinearGradient(w * .3, 0, w * .62, h); g.add_color_stop_rgba(0, *rgb(top), a); g.add_color_stop_rgba(.45, *rgb(top), 0); g.add_color_stop_rgba(.55, *rgb(bot), 0); g.add_color_stop_rgba(1, *rgb(bot), a); c.set_source(g); c.paint(); c.restore()


# ------------------------------------------------------------------ trees.  each: fn(c, w, h, season, rng); foot at (ax, ay) of the registry
def pahari_round(c, w, h, s, rng):
    p, b = GREEN[s], BARK[s]; x, y = w / 2, h * .965; bend = rng.uniform(-40, 40)
    if s == 'winter': return bare(c, w, h, s, rng)
    fl = dict(spring=FLOWER['pink']).get(s)
    for k, (dx, dy) in enumerate(((-250, 560), (250, 590), (-60, 690), (120, 760))): limb(c, [(x + bend * .5, y - 360), (x + dx * .45, y - 360 - dy * .30), (x + dx, y - 360 - dy * .62)], [58, 38, 14], b, p[5], rng)
    roots(c, x, y, 120, b, p[5], rng); limb(c, [(x, y), (x - 8, y - 160), (x + bend, y - 420), (x + bend, y - 620)], [124, 92, 78, 44], b, p[5], rng)
    cl = [(-300, 620, 250, 190), (300, 640, 250, 190), (0, 690, 300, 210), (-330, 830, 220, 190), (340, 850, 220, 190), (-120, 880, 280, 220), (150, 930, 270, 220), (-210, 1050, 230, 180), (200, 1070, 230, 180), (0, 1170, 240, 180)]
    for k, (dx, dy, rx, ry) in enumerate(cl): clump(c, x + dx * 1.02 + rng.normal(0, 14), y - dy + rng.normal(0, 12), rx, ry, p, rng, r=34, per=6, wd=.48, base=.02 + .018 * k, flowers=fl, fden=.85 if fl else 0, frad=15)
    shade(c, w, h, p[4], p[0], .20); wash(c, w, h, rng)


def mango(c, w, h, s, rng):
    p, b = GREEN[s], BARK[s]; x, y = w / 2, h * .965
    for dx, dy in ((-330, 400), (330, 420), (-120, 560), (170, 600)): limb(c, [(x, y - 300), (x + dx * .5, y - 330 - dy * .25), (x + dx, y - 330 - dy * .5)], [70, 46, 18], b, p[5], rng)
    roots(c, x, y, 150, b, p[5], rng); limb(c, [(x, y), (x + 10, y - 180), (x - 10, y - 420)], [150, 120, 90], b, p[5], rng)
    cl = [(-420, 520, 250, 180), (420, 540, 250, 180), (0, 560, 320, 190), (-450, 720, 230, 190), (460, 740, 230, 190), (-190, 760, 290, 220), (210, 790, 290, 220), (-300, 940, 260, 180), (300, 950, 260, 180), (0, 1010, 320, 200), (-120, 1120, 230, 140), (140, 1130, 230, 140)]
    for k, (dx, dy, rx, ry) in enumerate(cl):
        clump(c, x + dx, y - dy, rx, ry, p, rng, r=48, per=8, spread=3.6, wd=.24, hang=.9, base=.015 * k, lw=1.2, gap=1.15)
        if s in ('spring', 'gold'):                               # blossom panicles, cream cones over the leaves
            for _ in range(9):
                a = rng.uniform(math.pi * 1.0, TAU); px, py = x + dx + rx * .8 * rng.uniform(-1, 1), y - dy - ry * rng.uniform(.0, .8)
                for j in range(34):
                    t = j / 34; q = rng.normal(0, 13 * (1 - t) + 2); c.arc(px + q, py - t * 58, rng.uniform(2.4, 4.6), 0, TAU); c.set_source_rgb(*rgb(('#8a5a1c', '#f0d890', '#fff6c8', '#e8a868')[int(rng.integers(4))])); c.fill()
        elif s == 'summer':
            for _ in range(5):
                px, py = x + dx + rx * .75 * rng.uniform(-1, 1), y - dy + ry * rng.uniform(-.3, .8); leaf(c, px, py, 1.5, 42, 34, rgb('#e8a02a'), rgb('#b8541a'), rgb(p[5]), 2, tip=.3)
    shade(c, w, h, p[4], p[0], .18); wash(c, w, h, rng)


def kadamba(c, w, h, s, rng):
    p, b = GREEN[s], BARK[s]; x, y = w / 2, h * .965
    for dx, dy in ((-270, 520), (280, 560), (-40, 760)): limb(c, [(x, y - 420), (x + dx * .5, y - 400 - dy * .3), (x + dx, y - 400 - dy * .6)], [60, 40, 14], b, p[5], rng)
    roots(c, x, y, 110, b, p[5], rng); limb(c, [(x, y), (x - 20, y - 240), (x + 16, y - 560)], [112, 88, 62], b, p[5], rng)
    cl = [(-260, 640, 230, 170), (270, 660, 230, 170), (0, 720, 270, 190), (-290, 850, 210, 170), (300, 870, 210, 170), (0, 930, 290, 200), (-170, 1060, 230, 170), (190, 1080, 220, 170), (0, 1190, 210, 150)]
    for k, (dx, dy, rx, ry) in enumerate(cl):
        clump(c, x + dx, y - dy, rx, ry, p, rng, r=50, per=5, spread=2.9, wd=.56, base=.02 * k, lw=1.4)
        for _ in range(11):                                        # the round golden flower heads, spiked like little suns
            px, py = x + dx + rx * .8 * rng.uniform(-1, 1), y - dy + ry * .8 * rng.uniform(-1, 1); R = rng.uniform(13, 19); c.set_line_width(1.6)
            for a in np.linspace(0, TAU, 22): c.move_to(px, py); c.line_to(px + math.cos(a) * R * 1.5, py + math.sin(a) * R * 1.5)
            c.set_source_rgb(*rgb('#fff0b8')); c.stroke(); g = cairo.RadialGradient(px - R * .35, py - R * .4, 1, px, py, R); g.add_color_stop_rgb(0, *rgb('#ffd860')); g.add_color_stop_rgb(1, *rgb('#d0701a')); c.set_source(g); c.arc(px, py, R, 0, TAU); c.fill_preserve(); c.set_source_rgb(*rgb('#5a2410')); c.set_line_width(1.4); c.stroke()
    shade(c, w, h, p[4], p[0], .18); wash(c, w, h, rng)


def ashoka(c, w, h, s, rng):
    """the red-flowering ashoka: long wavy hanging leaves, coppery young tassels, flower clusters on the twigs and the old wood"""
    p, b = GREEN[s], BARK[s]; x, y = w / 2, h * .965; F = FLOWER['red']
    def cluster(px, py, R):
        c.arc(px, py, R * .8, 0, TAU); c.set_source_rgb(*rgb(F[0])); c.fill()
        for q in range(int(R * 1.5)):
            a, rr = rng.uniform(0, TAU), R * math.sqrt(rng.uniform(0, 1)); t = .5 - .5 * math.sin(a) * rr / R; fx, fy = px + rr * math.cos(a), py + rr * math.sin(a) * .85
            for m in range(4): leaf(c, fx, fy, m * TAU / 4 + rng.uniform(0, 1), R * .24, R * .20, mixc(F[1], F[3], t * rng.uniform(.4, 1.)), None, rgb(F[0]), 1., tip=.3)
            if q % 3 == 0:
                for m in range(3): a2 = a + rng.normal(0, .5); c.move_to(fx, fy); c.line_to(fx + math.cos(a2) * R * .5, fy + math.sin(a2) * R * .5); c.set_source_rgb(*rgb('#ffd08a')); c.set_line_width(1.2); c.stroke()
    for dx, dy in ((-340, 420), (350, 460), (-110, 720), (150, 760)): limb(c, [(x, y - 300), (x + dx * .45, y - 340 - dy * .30), (x + dx, y - 360 - dy * .55)], [70, 46, 16], b, p[5], rng)
    roots(c, x, y, 124, b, p[5], rng); tr = limb(c, [(x, y), (x + 24, y - 200), (x - 24, y - 460), (x + 4, y - 640)], [130, 96, 84, 46], b, p[5], rng)
    cl = [(-400, 560, 210, 150), (410, 580, 210, 150), (-160, 640, 230, 160), (200, 660, 230, 160), (-420, 760, 200, 160), (430, 790, 200, 160), (0, 820, 280, 180), (-250, 930, 230, 170), (270, 950, 230, 170), (0, 1070, 260, 180), (-130, 1190, 190, 130), (140, 1190, 190, 130)]
    for k, (dx, dy, rx, ry) in enumerate(cl):
        clump(c, x + dx, y - dy, rx, ry, p, rng, r=68, per=6, spread=1.5, wd=.20, hang=1.6, base=.015 * k, lw=1.3, gap=1.5)
        for _ in range(3): cluster(x + dx + rx * .75 * rng.uniform(-1, 1), y - dy + ry * .7 * rng.uniform(-1, 1), rng.uniform(26, 44))
    for i in (12, 22, 33): q = tr[min(len(tr) - 1, i)]; cluster(q[0] + rng.uniform(-30, 30), q[1], rng.uniform(20, 28))
    shade(c, w, h, p[4], p[0], .16); wash(c, w, h, rng)


def ashoka_weep(c, w, h, s, rng):
    """the mast form: a tall spear whose branches all weep"""
    p, b = GREEN[s], BARK[s]; x, y = w / 2, h * .97; limb(c, [(x, y), (x + 4, y - 200), (x, y - 1500)], [46, 40, 10], b, p[5], rng); roots(c, x, y, 46, b, p[5], rng, 4)
    poly(c, smooth_path([(x, y - 1850), (x + 120, y - 1500), (x + 195, y - 900), (x + 175, y - 330), (x + 60, y - 190), (x - 60, y - 190), (x - 175, y - 330), (x - 195, y - 900), (x - 120, y - 1500)], 8, True)); c.set_source_rgb(*ramp(p, .04)); c.fill_preserve(); c.set_source_rgb(*rgb(p[5])); c.set_line_width(3); c.stroke()
    for yy in np.linspace(230, 1800, 60):
        hw = 215 * min(1, (1880 - yy) / 900) ** .75 * min(1, .55 + yy / 900)
        for q in rng.permutation(np.linspace(-1, 1, max(3, int(hw / 20)))):
            v = .42 - .30 * q + rng.normal(0, .08); rosette(c, x + q * hw * .92 + rng.normal(0, 5), y - yy + abs(q) * 40, 62 + 20 * abs(q), 4, math.pi / 2 - q * .45, .9, p, v, rng, .18, 1.2)
    wash(c, w, h, rng, 200)


def banyan(c, w, h, s, rng):
    p, b = GREEN[s], BARK[s]; x, y = w / 2, h * .96
    def hang(px, py, L, wd): limb(c, [(px, py), (px + rng.normal(0, 10), py + L * .5), (px + rng.normal(0, 14), py + L)], [wd * 1.3, wd, wd * .55], b, p[5], rng, lw=1.6, stroke=.5)
    arms = ((-560, 150), (580, 170), (-780, 250), (800, 270), (-330, 360), (340, 380))
    for dx, dy in arms: limb(c, [(x + dx * .06, y - 340), (x + dx * .35, y - 480 - dy * .4), (x + dx * .7, y - 540 - dy * .6), (x + dx, y - 530 - dy * .7)], [130, 92, 64, 26], b, p[5], rng)
    for dx in (-690, -430, -300, 330, 520, 720): hang(x + dx, y - 600, 600 + rng.uniform(-6, 22), rng.uniform(26, 48))     # roots that have become trunks
    for k in np.argsort(-np.abs(np.linspace(-1, 1, 11))):
        q = np.linspace(-1, 1, 11)[k]; limb(c, [(x + q * 90, y - 700), (x + q * 130, y - 260), (x + q * 170, y - 60), (x + q * 270 * rng.uniform(.8, 1.1), y + 20)], [70, 74, 80, 20], b, p[5], rng)
    for _ in range(54): px = x + rng.uniform(-820, 820); L = rng.uniform(120, 420); q = np.array([(px, y - 640), (px + rng.normal(0, 6), y - 640 + L * .5), (px + rng.normal(0, 14), y - 640 + L)]); ink(c, smooth_path(q, 8), rng.uniform(3, 7), b[1 if rng.uniform() < .6 else 0], (.02, .7), seed=int(rng.integers(1e6)))
    cl = [(-760, 660, 230, 150), (770, 680, 230, 150), (-480, 690, 260, 160), (500, 700, 260, 160), (-180, 720, 270, 160), (190, 720, 270, 160), (-800, 820, 200, 150), (810, 840, 200, 150), (-560, 870, 260, 180), (580, 880, 260, 180), (-240, 900, 290, 190), (260, 910, 290, 190), (-640, 1030, 230, 150), (650, 1040, 230, 150), (-360, 1070, 270, 170), (370, 1080, 270, 170), (0, 1070, 300, 180), (-470, 1180, 220, 130), (480, 1180, 220, 130), (-150, 1220, 260, 150), (170, 1230, 260, 150)]
    for k, (dx, dy, rx, ry) in enumerate(cl): clump(c, x + dx, y - dy, rx, ry, p, rng, r=40, per=5, spread=3.0, wd=.62, base=.008 * k, lw=1.3, hang=.4)
    for _ in range(26): px = x + rng.uniform(-780, 780); L = rng.uniform(80, 260); q = np.array([(px, y - 620), (px + rng.normal(0, 6), y - 620 + L * .6), (px + rng.normal(0, 12), y - 620 + L)]); ink(c, smooth_path(q, 8), rng.uniform(2, 5), b[2], (.02, .7), seed=int(rng.integers(1e6)))
    shade(c, w, h, p[4], p[0], .18); wash(c, w, h, rng)


def palm(c, w, h, s, rng):
    """coconut palm"""
    p, b = GREEN[s], BARK[s]; x, y = w * .5, h * .97; cx, cy = x + rng.choice([-1, 1]) * rng.uniform(20, 90), h * .30
    limb(c, [(x, y), (x + (cx - x) * .12, y - h * .25), (cx, cy + 10)], [74, 46, 38], (b[2], b[1], '#d8c8a8'), p[5], rng, rings=26, stroke=.4)
    fr = [(a, 1) for a in (-2.95, -.2, -2.6, -.55, -2.2, -.95, -1.85, -1.3)] + [(a, 0) for a in (2.75, .4, 2.2, .95, 3.05, .08)]
    def frond(a, lit):
        L = rng.uniform(430, 520) * (1 if lit else .9); dx, dy = math.cos(a), math.sin(a); R = smooth_path([(cx, cy), (cx + dx * L * .45, cy + dy * L * .45 - 30), (cx + dx * L * .85, cy + dy * L * .62 + 90), (cx + dx * L * .98, cy + dy * L * .55 + 260)], 18); T = np.gradient(R, axis=0); k = len(R)
        for side in (1, -1):
            for i in range(3, k):
                t = i / k; l = 150 * math.sin(math.pi * min(1, t * .86 + .14)) ** .7 + 14; A = math.atan2(T[i, 1], T[i, 0]) + side * (.95 - .35 * t); A = math.atan2(math.sin(A) + .55, math.cos(A)); v = (.34 + .22 * lit) + (.20 if side * dx < 0 else -.06) + rng.normal(0, .06); leaf(c, R[i, 0], R[i, 1], A, l, 13, ramp(p, v), None, rgb(p[5]), .9, curl=.06)
        ink(c, R, 8, p[3] if lit else p[2], (.0, .8))
    for a, l in fr[8:]: frond(a, l)
    for a in np.linspace(0, TAU, 7): px, py = cx + 34 * math.cos(a), cy + 30 + 26 * math.sin(a); g = cairo.RadialGradient(px - 8, py - 9, 2, px, py, 25); g.add_color_stop_rgb(0, *rgb('#e8b858')); g.add_color_stop_rgb(1, *rgb('#7a4a1c')); c.set_source(g); c.arc(px, py, 24, 0, TAU); c.fill_preserve(); c.set_source_rgb(*rgb(p[5])); c.set_line_width(2); c.stroke()
    for a, l in fr[:8]: frond(a, l)
    wash(c, w, h, rng, 150)


def tala(c, w, h, s, rng):
    """palmyra: great pleated fans on a black ringed trunk"""
    p, b = GREEN[s], BARK[s]; x, y = w / 2, h * .97; cx, cy = x + rng.uniform(-30, 30), h * .27
    limb(c, [(x, y), (x - 6, y - h * .34), (cx, cy + 40)], [104, 74, 70], (b[0], b[1], b[2]), p[5], rng, rings=30, stroke=.7)
    def fan(a, R, dist, v0):
        fx, fy = cx + math.cos(a) * dist, cy + math.sin(a) * dist * .9; ink(c, np.linspace((cx, cy + 20), (fx, fy), 12), 13, p[2], (0, .1)); n = 26
        for k in np.argsort(-np.abs(np.linspace(-1, 1, n))):
            q = np.linspace(-1, 1, n)[k]; A = a + q * 2.15; l = R * (1 - .22 * q * q) * rng.uniform(.95, 1.05); v = v0 + .20 * math.cos(A + 2.2) + (.10 if k % 2 else -.06); leaf(c, fx, fy, A, l, R * .21, ramp(p, v), ramp(p, v - .2), rgb(p[5]), 1.3, curl=.04 * q, tip=.04)
    for a in (2.3, .8, 1.57): fan(a, 190, 120, .20)                # old fans hang
    for a in (2.95, .2, 2.65, .5, 1.9, 1.2): fan(a, 220, 120, .30)
    for a in (-2.5, -.65, -1.57, 3.1, .05): fan(a, 190, 70, .36)
    for a in (-2.8, -.35, -2.3, -.85, -1.9, -1.25, -1.57): fan(a, 230, 190, .48)
    wash(c, w, h, rng, 150)


def plantain(c, w, h, s, rng):
    p, b = GREEN[s], ('#8fa45a', '#4b6a38', '#d2d48a'); x, y = w / 2, h * .97; cx, cy = x + rng.uniform(-10, 10), h * .50
    def bleaf(a, L, wd, v, droop):
        dx, dy = math.cos(a), math.sin(a); R = smooth_path([(cx, cy), (cx + dx * L * .4, cy + dy * L * .5), (cx + dx * L * .8, cy + dy * L * .75 + droop * .35), (cx + dx * L, cy + dy * L * .72 + droop)], 14); T = np.gradient(R, axis=0); N = np.stack([-T[:, 1], T[:, 0]], 1); N /= np.linalg.norm(N, axis=1, keepdims=True); k = len(R); t = np.linspace(0, 1, k)
        W = wd * np.clip(np.sin(math.pi * np.clip((t - .10) / .90, 0, 1)) ** .55, 0, 1)
        for sd in (1, -1):
            e = R + N * (sd * W * (1 + .05 * np.sin(t * 60 + sd)))[:, None]; vv = v + (.14 if sd * dx < 0 else -.08); poly(c, np.vstack([R, e[::-1]])); c.set_source_rgb(*ramp(p, vv)); c.fill_preserve(); c.set_source_rgb(*rgb(p[5])); c.set_line_width(2.2); c.stroke()
            for i in range(4, k - 1, 1):
                q = np.linspace(R[i], e[min(k - 1, i + 3)], 6); ink(c, q, 2., p[5] if i % 5 == 0 else (p[1] if i % 2 else p[3]), (.1, .2), alpha=.75 if i % 5 == 0 else .55, seed=i)
            for i in rng.integers(8, k - 4, 5): poly(c, [e[i], e[min(k - 1, i + 2)], R[i] + (e[i] - R[i]) * rng.uniform(.3, .6)]); c.set_operator(cairo.OPERATOR_CLEAR); c.fill(); c.set_operator(cairo.OPERATOR_OVER)
        ink(c, R, 11, p[4], (.0, .7))
    for a, L, wd, d in ((2.9, 480, 74, 300), (.25, 480, 74, 300), (-2.75, 560, 84, 190), (-.40, 560, 84, 190)): bleaf(a, L, wd, .32, d)
    for dx in (-60, 66, 0): limb(c, [(x + dx * 1.4, y), (x + dx * .5, y - h * .22), (cx, cy)], [86, 66, 46], b, p[5], rng, stroke=1.2)
    for a, L, wd, d in ((-2.4, 640, 92, 60), (-.75, 640, 92, 60), (-1.95, 640, 84, -40), (-1.2, 640, 84, -40), (-1.57, 560, 64, -90)): bleaf(a, L, wd, .52, d)
    q = smooth_path([(cx, cy), (cx + 70, cy - 40), (cx + 120, cy + 60), (cx + 118, cy + 170)], 8); ink(c, q, 14, p[2], (0, 0)); leaf(c, cx + 118, cy + 150, 1.57, 130, 84, rgb('#8a1c3a'), rgb('#4a0c24'), rgb('#1e0410'), 2.4)
    for k in range(7): leaf(c, cx + 100 + (k % 3) * 14, cy + 50 + k * 10, 2.4 - k * .2, 40, 20, rgb('#e6c040'), rgb('#9a7a1c'), rgb(p[5]), 1.4)
    wash(c, w, h, rng, 160)


def bamboo(c, w, h, s, rng):
    p = GREEN[s]; b = (p[2], p[1], p[4]) if s != 'winter' else ('#b8ae84', '#7d7458', '#e4dcb8'); x, y = w / 2, h * .97
    def spray(px, py, n, v):
        for _ in range(n):
            a = rng.choice([math.pi * .5 + rng.uniform(.2, 1.2), math.pi * .5 - rng.uniform(.2, 1.2)]); l = rng.uniform(70, 130); t = v + rng.uniform(-.14, .2); leaf(c, px + rng.normal(0, 20), py + rng.normal(0, 14), a, l, l * .16, ramp(p, t), ramp(p, t - .14), rgb(p[5]), 1., curl=rng.uniform(-.1, .1))
    K = []
    for k in range(13):
        bx = x + (k - 6) * 30 + rng.normal(0, 16); lean = (k - 6) * 17 + rng.normal(0, 46); H_ = h * rng.uniform(.72, .93); K.append((bx, lean, H_, rng.uniform(17, 30), k % 3))
    for bx, lean, H_, wd, lay in sorted(K, key=lambda q: q[4]):
        P = smooth_path([(bx, y), (bx + lean * .25, y - H_ * .4), (bx + lean * .7, y - H_ * .8), (bx + lean * 1.25 + rng.normal(0, 40), y - H_)], 14)
        bb = b if lay else (p[1], p[0], p[2]); limb(c, P[::8], [wd, wd * .85, wd * .55, wd * .2], bb, p[5], rng, lw=1.6, stroke=.3)
        for i in range(4, len(P) - 2, 5): q = P[i]; c.save(); c.translate(*q); c.rotate(rng.normal(0, .05)); c.rectangle(-wd * .55, -3, wd * 1.1, 6); c.set_source_rgb(*rgb(bb[2])); c.fill_preserve(); c.set_source_rgb(*rgb(p[5])); c.set_line_width(1.4); c.stroke(); c.restore()
        for i in range(int(len(P) * .36), len(P), 2): spray(*P[i], 6 + int(7 * i / len(P)), .26 + .14 * lay)
    shade(c, w, h, p[4], p[0], .18); wash(c, w, h, rng, 200)


def deodar(c, w, h, s, rng):
    p, b = GREEN['summer' if s in ('spring', 'autumn') else s], BARK[s]; x, y = w / 2, h * .97; snow = s == 'winter'; H_ = h * .91
    limb(c, [(x, y), (x + 4, y - 300), (x, h * .06)], [70, 52, 6], b, p[5], rng); roots(c, x, y, 70, b, p[5], rng, 4)
    for yy in np.linspace(230, H_, 25):
        u = (yy - 230) / (H_ - 230); hw = (w * .45) * (1 - u) ** .85 + 22
        for sd in rng.permutation([-1, 1]):
            for lay in range(2):
                r = hw * rng.uniform(.62, 1.04) * (1 if lay else .75); y0 = y - yy + rng.normal(0, 14) + (0 if lay else -14); dr = rng.uniform(.14, .34); n = max(4, int(r / 13)); R = smooth_path([(x, y0), (x + sd * r * .5, y0 + r * .02), (x + sd * r, y0 + r * dr)], max(3, n // 2)); t = np.linspace(0, 1, len(R))
                hang_ = (46 + 22 * (1 - u)) * np.sin(np.pi * np.clip(t * .9 + .12, 0, 1)) ** .6; poly(c, np.vstack([R, (R + np.c_[0 * t, hang_])[::-1]])); c.set_source_rgb(*ramp(p, .07)); c.fill_preserve(); c.set_source_rgb(*rgb(p[5])); c.set_line_width(2); c.stroke()
                for i, q in enumerate(R):
                    for j in range(8): a = math.pi / 2 - sd * .75 + rng.normal(0, .42); l = rng.uniform(22, 44); v = .26 - .20 * sd + .22 * t[i] + .10 * lay + rng.normal(0, .08); leaf(c, q[0] + rng.normal(0, 7), q[1] + rng.uniform(-4, .7 * hang_[i]), a, l, 8, ramp(p, v - .012 * j), None, rgb(p[5]), .8)
                    if snow and lay and i % 2: c.save(); c.translate(q[0], q[1] - 2); c.scale(1, .40); c.arc(0, 0, rng.uniform(14, 28), 0, TAU); c.restore(); c.set_source_rgb(*rgb('#f4f4f6')); c.fill_preserve(); c.set_source_rgba(*rgb('#8890a8'), .6); c.set_line_width(1.4); c.stroke()
    wash(c, w, h, rng, 160)


def bare(c, w, h, s, rng):
    b, p = BARK[s], GREEN[s]; x, y = w / 2, h * .965
    def grow(px, py, a, L, wd, d):
        bend = rng.normal(0, .22); x1, y1 = px + math.cos(a + bend) * L, py + math.sin(a + bend) * L; mx, my = px + math.cos(a) * L * .5, py + math.sin(a) * L * .5
        kids = [] if d == 0 else [(a + sg * rng.uniform(.25, .62) + rng.normal(0, .12), L * rng.uniform(.66, .84)) for sg in ((-1, 1) if rng.uniform() < .55 or d > 5 else (-1, .1, 1))]
        P = [(px, py), (mx, my), (x1, y1)]
        for ka, kl in kids:
            ka = math.atan2(math.sin(ka) - .02, math.cos(ka) * 1.06); grow(x1, y1, ka, kl, wd * .64, d - 1)
        if wd > 9: limb(c, P, [wd, wd * .82, wd * .68], b, p[5], rng, lw=1.7, n=8)
        else: ink(c, smooth_path(P, 6), wd + 2.2, p[5], (0, .25 if d == 0 else 0)); ink(c, smooth_path(P, 6), wd * .7, b[0], (0, .4 if d == 0 else 0))
        if d <= 2 and s in ('autumn', 'gold', 'spring') and rng.uniform() < .8:
            if s == 'spring':
                for _ in range(3): flower(c, x1 + rng.normal(0, 14), y1 + rng.normal(0, 14), rng.uniform(13, 21), FLOWER['pink'], 5, rng.uniform(0, 6))
            else: leaf(c, x1, y1, rng.uniform(.6, 2.4), rng.uniform(20, 32), 15, ramp(p, rng.uniform(.4, .8)), None, rgb(p[5]), 1.)
    roots(c, x, y, 110, b, p[5], rng); grow(x, y, -math.pi / 2 + rng.normal(0, .05), h * .225, 112, 7)
    wash(c, w, h, rng, 120)


# ------------------------------------------------------------------ low plants
def shrub(c, w, h, s, rng):
    p = GREEN[s]; x, y = w / 2, h * .96; fl = dict(spring=FLOWER['pink'], monsoon=FLOWER['white'], summer=FLOWER['red'], gold=FLOWER['red']).get(s)
    for dx, dy, rx, ry in ((-190, 120, 150, 120), (190, 120, 150, 120), (0, 130, 190, 140), (-110, 230, 150, 120), (120, 240, 150, 120), (0, 320, 140, 100)): clump(c, x + dx, y - dy, rx, ry, p, rng, r=40, per=6, wd=.42, hang=-.3, base=.03, flowers=fl, fden=.45 if fl else 0, frad=16, lw=1.4)
    for _ in range(60): bx = x + rng.uniform(-330, 330); lx = rng.normal(0, 30); ink(c, smooth_path([(bx, y + 14), (bx + lx * .3, y - 40), (bx + lx, y - rng.uniform(50, 100))], 6), 8, p[int(rng.integers(1, 4))], (.0, .9))
    wash(c, w, h, rng, 60)


def grass(c, w, h, s, rng):
    p = GREEN[s]; x, y = w / 2, h * .985
    for k in range(150):
        u = k / 150; bx = x + np.clip(rng.normal(0, w * .10), -w * .24, w * .24); L = h * rng.uniform(.45, .92) * (1 - .25 * u); lean = (bx - x) * rng.uniform(.4, 1.0) + rng.normal(0, w * .06); P = smooth_path([(bx, y), (bx + lean * .25, y - L * .55), (bx + lean * 1.0, y - L), (bx + lean * 1.45, y - L * .90)], 9); v = .10 + .62 * u + rng.normal(0, .07)
        wd = rng.uniform(8, 15); ink(c, P, wd + 3.0, p[5], (0., .9)); ink(c, P, wd, '#%02x%02x%02x' % tuple(int(q * 255) for q in ramp(p, v)), (0., .9))
        if k % 9 == 0:
            for i in range(12): q = P[-1 - i % 8]; c.arc(q[0] + rng.normal(0, 5), q[1] + rng.normal(0, 8), 3.4, 0, TAU); c.set_source_rgb(*rgb(p[4])); c.fill()


def reed(c, w, h, s, rng):
    """kusha and plume grass (kaans) with white feathers"""
    grass(c, w, h, s, rng); p = GREEN[s]; x, y = w / 2, h * .985
    for k in range(13):
        lean = rng.normal(0, w * .16); P = smooth_path([(x + lean * .2, y), (x + lean * .5, y - h * .5), (x + lean, y - h * rng.uniform(.78, .93))], 10); ink(c, P, 5, p[3], (0, .2)); d = P[-1] - P[-6]; a0 = math.atan2(d[1], d[0])
        for i in range(70): t = rng.uniform(0, 1); q = P[-1] + np.array([math.cos(a0), math.sin(a0)]) * (t - .7) * h * .14; leaf(c, q[0], q[1], a0 + rng.choice([-1, 1]) * rng.uniform(.2, .7), 28 * (1.1 - t), 4, mixc('#b8a88c', '#fffaf0', rng.uniform(.3, 1)), None, None)


def fern(c, w, h, s, rng):
    p = GREEN[s]; x, y = w / 2, h * .95
    for a in (-2.95, -.2, -2.6, -.5, -2.2, -.95, -1.8, -1.35):
        L = h * rng.uniform(.65, .85); R = smooth_path([(x, y), (x + math.cos(a) * L * .4, y + math.sin(a) * L * .6), (x + math.cos(a) * L * .85, y + math.sin(a) * L * .82), (x + math.cos(a) * L * 1.1, y + math.sin(a) * L * .55)], 14); T = np.gradient(R, axis=0)
        for i in range(3, len(R)):
            t = i / len(R); l = 92 * math.sin(math.pi * (t * .8 + .2)) + 6
            for sd in (-1, 1): A = math.atan2(T[i, 1], T[i, 0]) + sd * 1.05; v = .45 + .2 * (sd * math.cos(a) < 0) + rng.normal(0, .06); leaf(c, *R[i], A, l, 17, ramp(p, v), ramp(p, v - .18), rgb(p[5]), 1., curl=.1 * sd)
        ink(c, R, 5, p[4], (0, .8))


def creeper(c, w, h, s, rng):
    """hanging vines (foot of the plate = the top edge it hangs from)"""
    p = GREEN[s]; fl = FLOWER['white' if s == 'monsoon' else 'pink' if s == 'spring' else 'gold']
    for k in range(9):
        x = w * (.08 + .105 * k) + rng.normal(0, 12); L = h * rng.uniform(.45, .96); P = smooth_path([(x, -10), (x + rng.normal(0, 26), L * .35), (x + rng.normal(0, 30), L * .7), (x + rng.normal(0, 22), L)], 18); ink(c, P, 6, BARK[s][1], (0, .6))
        for i in range(2, len(P)):
            for sd in (-1, 1):
                A = math.pi / 2 + sd * rng.uniform(.5, 1.1); l = rng.uniform(30, 48) * (1.1 - .5 * i / len(P)); v = rng.uniform(.25, .75); leaf(c, *P[i], A, l, l * .62, ramp(p, v), ramp(p, v - .18), rgb(p[5]), 1.2, ramp(p, v + .2))
            if rng.uniform() < .12: flower(c, P[i, 0] + rng.normal(0, 10), P[i, 1], 13, fl, 5, rng.uniform(0, 6))


# ------------------------------------------------------------------ lotus pond
def _lotus(c, x, y, R, open_=1., pal=FLOWER['pink']):
    def pet(a, l, wd, v): leaf(c, x, y, a, l, wd, mixc(pal[2], pal[3], v), mixc(pal[1], pal[2], v), rgb('#6a1c3c'), 2., mixc(pal[1], pal[2], .5), tip=.12)
    for a in np.linspace(-2.85, -.29, 7): pet(a, R * 1.0, R * .46, .2)
    for a in np.linspace(-2.6, -.54, 6): pet(a, R * .95, R * .44, .55)
    c.save(); c.translate(x, y - R * .30); c.scale(1, .55); c.arc(0, 0, R * .26, 0, TAU); c.restore(); c.set_source_rgb(*rgb('#f0c040')); c.fill()
    for a in np.linspace(0, TAU, 16): c.move_to(x, y - R * .28); c.line_to(x + math.cos(a) * R * .36, y - R * .30 + math.sin(a) * R * .20); c.set_source_rgb(*rgb('#ffe890')); c.set_line_width(2); c.stroke()
    for a in (-2.95, -.19, -2.5, -.64, -2.05, -1.09, -1.57): pet(a, R * .78, R * .44, .9)
    for a in (3.05, .09): pet(a, R * .9, R * .34, .4)


def lotus_bloom(c, w, h, s, rng):
    p = GREEN[s]; x = w / 2; ink(c, smooth_path([(x + 10, h * .99), (x - 10, h * .75), (x, h * .5)], 10), 16, p[5], (0, 0)); ink(c, smooth_path([(x + 10, h * .99), (x - 10, h * .75), (x, h * .5)], 10), 11, p[3], (0, 0)); _lotus(c, x, h * .55, w * .46, 1., FLOWER['white'] if s == 'night' else FLOWER['pink'])


def lotus_bud(c, w, h, s, rng):
    p = GREEN[s]; x = w / 2; q = smooth_path([(x - 6, h * .99), (x + 8, h * .7), (x, h * .42)], 10); ink(c, q, 14, p[5], (0, 0)); ink(c, q, 9, p[3], (0, 0))
    for a, l, v in ((-1.85, .36, .2), (-1.29, .36, .2), (-1.72, .40, .5), (-1.42, .40, .5), (-1.57, .42, .85)): leaf(c, x, h * .44, a, h * l, w * .36, mixc('#e58aa4', '#fff0ee', v), mixc('#c25a80', '#f0aab8', v), rgb('#6a1c3c'), 2.2)
    for a in (-2.2, -.94): leaf(c, x, h * .46, a, h * .12, w * .14, ramp(p, .6), None, rgb(p[5]), 1.5)


def lotus_leaf(c, w, h, s, rng):
    """a floating pad seen at a low angle"""
    p = GREEN[s]; cx, cy = w / 2, h * .56; a = np.linspace(.25, TAU - .25, 60); k = 1 + .03 * np.sin(a * 9) + .02 * np.sin(a * 17); E = np.c_[cx + w * .47 * k * np.cos(a), cy + h * .38 * k * np.sin(a)]; E = np.vstack([E, [(cx + w * .04, cy)]])
    poly(c, E + [0, 10]); c.set_source_rgb(*rgb(p[0])); c.fill(); poly(c, E); g = cairo.LinearGradient(0, 0, w, h); g.add_color_stop_rgb(0, *ramp(p, .72)); g.add_color_stop_rgb(1, *ramp(p, .32)); c.set_source(g); c.fill_preserve(); c.set_source_rgb(*rgb(p[5])); c.set_line_width(4); c.stroke()
    for q in E[::4]: ink(c, np.linspace((cx, cy), (cx + (q[0] - cx) * .93, cy + (q[1] - cy) * .93), 8), 3.4, p[4], (.0, .6), alpha=.8)
    for _ in range(7): t = rng.uniform(0, TAU); r = rng.uniform(.2, .7); c.arc(cx + w * .45 * r * math.cos(t), cy + h * .35 * r * math.sin(t), rng.uniform(3, 8), 0, TAU); c.set_source_rgba(1, 1, 1, .7); c.fill()


def lotus_clump(c, w, h, s, rng):
    """a stand of raised leaves, buds and blooms"""
    p = GREEN[s]; y = h * .97
    def stem(x0, x1, y1, wd=11): q = smooth_path([(x0, y), ((x0 + x1) / 2 + rng.normal(0, 14), (y + y1) / 2), (x1, y1)], 10); ink(c, q, wd + 4, p[5], (0, 0)); ink(c, q, wd, p[2], (0, 0))
    def pad(x, yy, R, t): stem(x + rng.normal(0, 30), x, yy); c.save(); c.translate(x, yy); c.rotate(rng.normal(0, .12)); c.scale(1, t); c.translate(-R, -R * 1.1); c.scale(2 * R / 400, 2 * R / 400); lotus_leaf(c, 400, 400, s, rng); c.restore()
    for k in range(9): pad(w * (.08 + .105 * k) + rng.normal(0, 18), h * rng.uniform(.58, .80), rng.uniform(95, 140), rng.uniform(.34, .5))
    for x, yy, R in ((.22, .34, 120), (.55, .22, 140), (.82, .40, 115)): stem(w * x + 20, w * x, h * yy); _lotus(c, w * x, h * yy, R, 1., FLOWER['white'] if s == 'night' else FLOWER['pink'])
    for x, yy in ((.38, .30), (.70, .28), (.10, .46)):
        stem(w * x - 14, w * x, h * yy)
        for a, l, v in ((-1.8, 84, .3), (-1.34, 84, .3), (-1.57, 96, .8)): leaf(c, w * x, h * yy + 8, a, l, 44, mixc('#e58aa4', '#fff0ee', v), mixc('#c25a80', '#f0aab8', v), rgb('#6a1c3c'), 2.)
    for k in range(7): pad(w * (.10 + .135 * k) + rng.normal(0, 18), h * rng.uniform(.82, .92), rng.uniform(105, 150), rng.uniform(.32, .42))


# ------------------------------------------------------------------ rocks, trunk wipes, foreground
def rock(c, w, h, s, rng):
    """the crystalline boulders of Pahari and Mughal hills: leaning facets with pale crests and ink hatching"""
    base = dict(spring=('#5a4a66', '#8f7c8e', '#c8b0b0', '#f2e2d4'), summer=('#4f4650', '#857668', '#bda88c', '#ecdcba'), monsoon=('#232a36', '#465260', '#748488', '#aebcb4'), autumn=('#5a3434', '#96604a', '#d09a68', '#f4d8a0'), winter=('#4a5064', '#7c869a', '#b4bccc', '#f4f4f8'), gold=('#4a2a2a', '#86563a', '#c8925a', '#f4d49a'), night=('#101a30', '#22304e', '#3e5274', '#7c98b8'))[s]
    y = h * .95
    for k, cx in enumerate(rng.permutation(np.linspace(.14, .86, 11))):
        H_ = h * (.82 - 1.0 * abs(cx - .5)) * rng.uniform(.7, 1.05); x = w * cx; wd = w * rng.uniform(.10, .17); ln = rng.uniform(-.05, .16) * w
        P = np.array([(x - wd, y), (x - wd * .95 + ln * .3, y - H_ * .45), (x - wd * .55 + ln * .8, y - H_ * .85), (x + ln, y - H_), (x + wd * .5 + ln * .8, y - H_ * .88), (x + wd * .9 + ln * .3, y - H_ * .5), (x + wd, y)]) + rng.normal(0, 6, (7, 2))
        poly(c, P); g = cairo.LinearGradient(x - wd, y - H_, x + wd, y); g.add_color_stop_rgb(0, *rgb(base[2])); g.add_color_stop_rgb(1, *rgb(base[1])); c.set_source(g); c.fill_preserve(); c.set_source_rgb(*rgb(base[0])); c.set_line_width(3.4); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke()
        poly(c, [P[3], P[4], P[5], P[6], (x + wd * .25, y), (x + ln * .5 + wd * .15, y - H_ * .5)]); c.set_source_rgba(*rgb(base[0]), .62); c.fill()
        poly(c, [P[1], P[2], P[3], P[3] + [wd * .05, H_ * .10], P[2] + [wd * .16, H_ * .10], P[1] + [wd * .16, H_ * .06]]); c.set_source_rgb(*rgb(base[3])); c.fill()
        for j in range(9): t = rng.uniform(.1, .9); q0 = P[3] * (1 - t) + np.array([x + rng.uniform(-.6, .9) * wd, y]) * t; ink(c, np.array([q0, q0 + [rng.normal(0, 4) - 4, 14], q0 + [-ln * .12, rng.uniform(26, 70)]]), 3, base[0], (.1, .7), alpha=.7, seed=j)
    if s != 'winter':
        p = GREEN[s]
        for _ in range(40): x = w * rng.uniform(.06, .94); rosette(c, x, y - rng.uniform(0, h * .10), 30, 5, -1.57, 2.0, p, rng.uniform(.3, .8), rng, .3)


def trunk_wide(c, w, h, s, rng):
    """an old trunk as wide as the plate, for wiping the screen: hold it near the lens"""
    p, b = GREEN[s], BARK[s]; x = w / 2; W_ = w * .80
    limb(c, [(x, h + 20), (x - 10, h * .66), (x + 14, h * .33), (x, -20)], [W_, W_ * .94, W_ * .95, W_], b, p[5], rng, lw=5, stroke=0, n=40, wob=.35)
    for k in range(44):                                             # fluted ridges that run and fork
        u = rng.uniform(-.46, .46); q = smooth_path([(x + u * W_ + rng.normal(0, 8), yy) for yy in np.linspace(-20, h + 20, 9)], 10); q[:, 0] += 12 * np.sin(q[:, 1] * .013 + k * 1.7); wd = rng.uniform(10, 30); ink(c, q, wd, b[1] if u > -.1 else b[0], (.05, .05), alpha=.8, seed=k); ink(c, q - [wd * .5, 0], wd * .32, b[2], (.05, .05), alpha=.8, seed=k + 99)
    for k in range(5):
        kx, ky = x + rng.uniform(-.3, .3) * W_, rng.uniform(.1, .9) * h
        for r in (74, 56, 38, 20): c.save(); c.translate(kx, ky); c.scale(.62, 1); c.arc(0, 0, r, 0, TAU); c.restore(); c.set_source_rgb(*rgb(b[1] if r in (74, 38) else b[0])); c.fill_preserve(); c.set_source_rgb(*rgb(p[5])); c.set_line_width(3); c.stroke()
    if s in ('monsoon', 'spring', 'summer'):
        for _ in range(130): mx, my = x + np.clip(rng.normal(-.20, .13), -.44, .4) * W_, rng.uniform(0, h); c.save(); c.translate(mx, my); c.scale(1, rng.uniform(.3, .6)); c.arc(0, 0, rng.uniform(8, 34), 0, TAU); c.restore(); c.set_source_rgba(*ramp(p, rng.uniform(.25, .7)), .55); c.fill()
    vine = smooth_path([(x - W_ * .42, h + 10), (x + W_ * .22, h * .72), (x - W_ * .26, h * .44), (x + W_ * .30, h * .18), (x - W_ * .1, -30)], 26); ink(c, vine, 26, p[5], (0, 0)); ink(c, vine, 18, b[0] if s in ('winter', 'autumn') else p[1], (0, 0)); ink(c, vine - [4, 0], 6, b[2], (0, 0))
    if s != 'winter':
        for i in range(2, len(vine), 2):
            for sd in (-1, 1): l = rng.uniform(80, 140); v = rng.uniform(.3, .75); leaf(c, *vine[i], rng.uniform(.3, 1.0) if sd > 0 else math.pi - rng.uniform(.3, 1.0), l, l * .62, ramp(p, v), ramp(p, v - .2), rgb(p[5]), 3., ramp(p, v + .2))
            if s == 'spring' and i % 8 == 0: flower(c, *vine[i], 46, FLOWER['pink'], 5, 0, lw=2.4)


def _fgcol(s): return dict(spring=('#12301f', '#274f2c'), summer=('#0b241c', '#173f2a'), monsoon=('#031413', '#0a2c28'), autumn=('#2a0c0e', '#5c2212'), winter=('#20242e', '#3c424e'), gold=('#220d0a', '#4c2410'), night=('#03050f', '#0a1428'))[s]


def fg_leaves(c, w, h, s, rng):
    """dark leaf mass that hangs from the top left corner of the frame"""
    d, l = _fgcol(s)
    for k in range(9):
        u = k / 8; x0, y0 = (-20, h * (.02 + .40 * u * u)) if k % 2 else (w * .62 * u, -20); a = .10 + .75 * rng.uniform(.6, 1.1) * (1 - .4 * u) + (.35 if k % 2 == 0 else -.1); L = rng.uniform(.50, .72) * w * (1 - .25 * u)
        P = smooth_path([(x0, y0), (x0 + math.cos(a) * L * .4, y0 + math.sin(a) * L * .30), (x0 + math.cos(a) * L * .8, y0 + math.sin(a) * L * .62), (x0 + math.cos(a) * L, y0 + math.sin(a) * L * .95)], 8); ink(c, P, 14, d, (0, .6)); T = np.gradient(P, axis=0)
        for i in range(3, len(P), 2):
            for sd in (-1, 1): q = math.atan2(T[i, 1], T[i, 0]) + sd * rng.uniform(.35, .9); q = math.atan2(math.sin(q) + .45, math.cos(q)); ll = rng.uniform(150, 230) * (1.1 - .4 * i / len(P)); lit = rng.uniform() < .35; leaf(c, *P[i], q, ll, ll * .27, rgb(l if lit else d), rgb(d), mixc(d, '#000000', .5), 2.5, vein=mixc(d, l, 1.) if not lit else mixc(l, '#ffffff', .15), curl=.08 * sd)


def fg_grass(c, w, h, s, rng):
    d, l = _fgcol(s)
    for k in range(120): u = rng.beta(1.5, 1.5); bx = w * (.10 + .80 * u); L = h * rng.uniform(.35, .95) * (.35 + .65 * math.sin(math.pi * u) ** .6); ln = float(np.clip(rng.normal(0, w * .05), -w * .05, w * .05)); P = smooth_path([(bx, h + 10), (bx + ln * .3, h - L * .6), (bx + ln, h - L), (bx + ln * 1.8, h - L * .92)], 9); ink(c, P, rng.uniform(12, 30), d if k % 4 else l, (0, .9))


def fg_palm(c, w, h, s, rng):
    d, l = _fgcol(s)
    for y0, dy in ((-.05, .50), (.15, .30), (-.1, .16)):
        R = smooth_path([(-40, h * y0), (w * .35, h * (y0 + dy * .25)), (w * .70, h * (y0 + dy * .7)), (w * .92, h * (y0 + dy * 1.5))], 20); T = np.gradient(R, axis=0); ink(c, R, 18, d, (0, .7))
        for i in range(4, len(R)):
            for sd in (-1, 1): a = math.atan2(T[i, 1], T[i, 0]) + sd * .8; a = math.atan2(math.sin(a) + .3, math.cos(a)); leaf(c, *R[i], a, 260 * math.sin(math.pi * (i / len(R) * .8 + .2)), 26, rgb(d if i % 3 else l), None, None, curl=.08)


def blossom_branch(c, w, h, s, rng):
    """a flowering branch across the top of the frame"""
    b, p = BARK[s], GREEN[s]; fl = FLOWER['pink' if s in ('spring', 'winter') else 'red' if s == 'gold' else 'white']
    P = limb(c, [(-30, h * .30), (w * .28, h * .20), (w * .6, h * .34), (w * .96, h * .26)], [64, 46, 28, 8], b, p[5], rng, wob=.6); tw = []
    for i in range(5, len(P) - 1, 2):
        sd = rng.choice([-1, 1]); a = sd * rng.uniform(.5, 1.2); L = rng.uniform(110, 260) * (1 - .3 * i / len(P)); q = smooth_path([P[i], P[i] + [math.cos(a) * L * .5, math.sin(a) * L * .55], P[i] + [math.cos(a) * L, math.sin(a) * L * .8 + 24]], 8); ink(c, q, 13, p[5], (0, .7)); ink(c, q, 9, b[1], (0, .8)); tw.append(q)
    for q in tw:
        for j in range(9): z = q[rng.integers(3, len(q))] + rng.normal(0, 12, 2); leaf(c, *z, rng.uniform(.1, 3.0), rng.uniform(50, 86), 28, ramp(p, rng.uniform(.4, .8)), ramp(p, .3), rgb(p[5]), 1.6, ramp(p, .9))
    for q in tw:
        for j in range(9): z = q[rng.integers(3, len(q))] + rng.normal(0, 22, 2); r = rng.uniform(20, 34); flower(c, *z, r, fl, 5, rng.uniform(0, 6), lw=1.7)
        for j in range(4): z = q[-1] + rng.normal(0, 16, 2); c.arc(*z, rng.uniform(6, 10), 0, TAU); c.set_source_rgb(*rgb(fl[1])); c.fill_preserve(); c.set_source_rgb(*rgb(fl[0])); c.set_line_width(1.6); c.stroke()


def hill(c, w, h, s, rng):
    """a far ridge of rounded Pahari hills dotted with tiny trees (set far off, hazed)"""
    p = GREEN[s]
    for k in range(4):
        x = np.linspace(-20, w + 20, 60); y = h * 1.1 * np.abs(x / w * 2 - 1) ** 5 + h * (.30 + .16 * k) + h * .16 * np.sin(x / w * (5 + k) + k * 2.2 + rng.uniform(0, 6)) * (1 - .14 * k) + h * .03 * np.sin(x / w * 23 + k); P = np.r_[np.c_[x, y], [(w + 20, h + 10), (-20, h + 10)]]
        poly(c, P); g = cairo.LinearGradient(0, y.min(), 0, h); g.add_color_stop_rgb(0, *ramp(p, .62 - .08 * k)); g.add_color_stop_rgb(1, *ramp(p, .40 - .07 * k)); c.set_source(g); c.fill_preserve(); c.set_source_rgba(*rgb(p[5]), .8); c.set_line_width(2.6); c.stroke()
        for j in range(70):
            u = rng.uniform(0, 1); tx = u * w; ty = np.interp(tx, x, y) + rng.uniform(4, h * .13)
            if ty > h * .97: continue
            r = rng.uniform(8, 17) * (1 + .25 * k); c.rectangle(tx - 1.5, ty, 3, r); c.set_source_rgb(*rgb(p[5])); c.fill(); c.arc(tx, ty - r * .4, r, 0, TAU); c.set_source_rgb(*ramp(p, .25)); c.fill_preserve(); c.set_source_rgb(*rgb(p[5])); c.set_line_width(1.6); c.stroke(); c.arc(tx - r * .28, ty - r * .7, r * .55, 0, TAU); c.set_source_rgb(*ramp(p, .62)); c.fill()


# ------------------------------------------------------------------ registry: kind -> (painter, w, h, anchor x, anchor y, top, variants)
KINDS = dict(pahari_round=(pahari_round, 1408, 1500, .5, .965, .06, 3), mango=(mango, 1664, 1400, .5, .965, .06, 2), kadamba=(kadamba, 1280, 1500, .5, .965, .08, 2), ashoka=(ashoka, 1536, 1500, .5, .965, .06, 2), ashoka_weep=(ashoka_weep, 640, 2000, .5, .97, .04, 2), banyan=(banyan, 2048, 1500, .5, .96, .08, 2),
             palm=(palm, 1280, 1600, .5, .97, .08, 3), tala=(tala, 1180, 1500, .5, .97, .06, 2), plantain=(plantain, 1400, 1300, .5, .97, .06, 2), bamboo=(bamboo, 1280, 1600, .5, .97, .05, 2), deodar=(deodar, 1000, 1800, .5, .97, .04, 2), bare=(bare, 1600, 1600, .5, .965, .08, 3),
             shrub=(shrub, 900, 560, .5, .96, .1, 2), grass=(grass, 720, 560, .5, .985, .08, 3), reed=(reed, 720, 900, .5, .985, .08, 2), fern=(fern, 1100, 760, .5, .95, .1, 2), creeper=(creeper, 900, 1300, .5, .0, 1., 2),
             lotus_bloom=(lotus_bloom, 360, 520, .5, .99, .3, 1), lotus_bud=(lotus_bud, 180, 460, .5, .99, .06, 1), lotus_leaf=(lotus_leaf, 512, 256, .5, .62, .1, 2), lotus_clump=(lotus_clump, 1400, 900, .5, .97, .08, 2),
             rock=(rock, 1100, 800, .5, .95, .1, 3), trunk_wide=(trunk_wide, 1600, 2048, .5, 1., 0., 2), fg_leaves=(fg_leaves, 1400, 1000, 0., 0., 1., 2), fg_grass=(fg_grass, 1600, 560, .5, 1., .05, 2), fg_palm=(fg_palm, 1400, 1100, 0., 0., 1., 1), blossom_branch=(blossom_branch, 1600, 800, 0., .25, 0., 1), hill=(hill, 2048, 700, .5, 1., .1, 2))


@dataclass
class Plate:
    tex: object; w: int; h: int; ax: float; ay: float; top: float

    def size(s, height):
        """card width and height in world units so that foot to top measures `height`"""
        k = height / (abs(s.ay - s.top) * s.h); return s.w * k, s.h * k


_MARKS = ''.join(inspect.getsource(q) for q in (leaf, flower, rosette, scallop, clump, limb, roots, wash, shade, _lotus))
def _src(fn): return hashlib.md5((_MARKS + inspect.getsource(fn) + repr((GREEN, BARK, FLOWER))).encode()).hexdigest()[:6]


def plate_of(kind, season='summer', var=0):
    fn, w, h, ax, ay, top, nv = KINDS[kind]; var %= nv; seed = int(hashlib.md5(f'{kind}{season if season == "bare" else ""}{var}'.encode()).hexdigest()[:8], 16)
    t = plate(f'flora_{kind}_{season}_{var}_{_src(fn)}', w, h, lambda c: fn(c, w, h, season, np.random.default_rng(seed)), VER)
    return Plate(t, w, h, ax, ay, top)


_q = None


def cards(st, pl, pos, height, flip=1., lean=0., yaw=None, phase=0., tint=(1, 1, 1), haze=0., hazeCol=(.5, .5, .5), foot=0., footCol=(.05, .08, .08), wind=.5, upright=None, cutoff=.45, cls=6., inkw=0.):
    """draw one plate at many places (world feet Nx3); height, flip, lean, yaw, phase, tint, haze: scalar or per card"""
    global _q
    c = gl.ctx(); p = gl.program('flora.frag', vs='flora.vert'); pos = np.atleast_2d(np.asarray(pos, float)); n = len(pos)
    if n == 0: return
    o = np.argsort(((pos - st.cam.eye) ** 2).sum(1)); D = np.zeros((n, 15), 'f4'); D[:, :3] = pos; h = np.broadcast_to(np.asarray(height, float), (n,)); k = h / (abs(pl.ay - pl.top) * pl.h); D[:, 3] = pl.w * k; D[:, 4] = pl.h * k; D[:, 5] = flip; D[:, 6] = phase
    D[:, 7] = pl.ax; D[:, 8] = 1 - pl.ay; D[:, 9] = 99. if yaw is None else np.radians(yaw); D[:, 10] = lean; D[:, 11:14] = hexc(tint) if isinstance(tint, (str, tuple)) else tint; D[:, 14] = haze; D = D[o]
    if upright is None: d = float(np.clip((-st.cam.R[2][1] - .30) / .55, 0, 1)); upright = 1 - .72 * d * d * (3 - 2 * d)         # seen from above, cards lean back to face us as trees do in a miniature
    if _q is None: _q = c.buffer(np.array([0, 0, 1, 0, 0, 1, 1, 1], 'f4').tobytes())
    vb = c.buffer(D.tobytes()); vao = c.vertex_array(p, [(_q, '2f', 'q'), (vb, '3f 4f 4f 4f/i', 'pos', 'a', 'b', 'tint')]); st.oid += 1
    st._gdraw(p, dict(objId=float(st.oid), hazeCol=hexc(hazeCol), footCol=hexc(footCol), foot=float(foot), wind=float(wind), upright=float(upright), cutoff=float(cutoff), cls=float(cls), inkw=float(inkw)), dict(tCard=pl.tex), vao, mgl.TRIANGLE_STRIP, inst=n); vao.release(); vb.release()


def tree(st, kind, at, height, season='summer', seed=0, flip=None, yaw=None, crossed=False, **k):
    """one plant standing at `at`; crossed=True adds a second card at right angles (for cameras that swing round it)"""
    pl = plate_of(kind, season, seed); f = (1. if seed % 2 == 0 else -1.) if flip is None else (-1. if flip is True else 1. if flip is False else float(flip)); k.setdefault('phase', seed * 1.7)
    if crossed: cards(st, pl, [at, at], height, f, yaw=np.array([yaw or 0., (yaw or 0.) + 90.]), **k)
    else: cards(st, pl, [at], height, f, yaw=yaw, **k)


def scatter(st, kind, pos, height=10., season='summer', seed=0, vary=.25, tintvar=.10, **k):
    """many plants of one kind: variants, sizes, flips and tints drawn from `seed` (stable from frame to frame)"""
    pos = np.atleast_2d(np.asarray(pos, float)); n = len(pos); nv = KINDS[kind][6]; r = np.random.default_rng(seed); v = r.integers(0, nv, n); hh = np.broadcast_to(np.asarray(height, float), (n,)) * (1 + vary * r.uniform(-1, 1, n)); fl = r.choice([-1., 1.], n); ph = r.uniform(0, 6.28, n)
    base = np.asarray(hexc(k.pop('tint', (1, 1, 1)))); ti = base * (1 + tintvar * r.uniform(-1, 1, (n, 1)) + .5 * tintvar * r.uniform(-1, 1, (n, 3))); hz = np.broadcast_to(np.asarray(k.pop('haze', 0.), float), (n,))
    for j in range(nv):
        m = v == j
        if m.any(): cards(st, plate_of(kind, season, j), pos[m], hh[m], fl[m], phase=ph[m], tint=ti[m], haze=hz[m], **k)


def frame(st, kind, x, y, scale=1., season='summer', var=0, rot=0., flip=False, lod=0., tint=(1, 1, 1), alpha=1.):
    """after st.close(): a plate laid on the picture in pixels with its anchor (corner it hangs from / foot) at (x, y); lod blurs it like a near thing out of focus"""
    pl = plate_of(kind, season, var); ox, oy = (.5 - pl.ax) * pl.w * scale * (-1 if flip else 1), (.5 - pl.ay) * pl.h * scale; a = math.radians(rot)
    st.plate(pl.tex, x + ox * math.cos(a) - oy * math.sin(a), y + ox * math.sin(a) + oy * math.cos(a), scale, rot=-rot, alpha=alpha, tint=tint, lod=lod, flip=flip)
