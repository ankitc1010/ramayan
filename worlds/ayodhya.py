"""Ayodhya: setup and helpers for ayodhya.glsl.

    from worlds import ayodhya as AY
    st.paint('sky.frag', **AY.sky('dawn'));  st.open(cam, AY.light('dawn'));  AY.draw(st, 'dawn');  AY.trees(st, 'dawn');  st.close();  AY.birds / FX ...
    night:  AY.draw(st, 'night', night=1.);  AY.trees(st, 'night');  st.close();  AY.lamps(st, amount=0..1)      # after close: thousands of flames
Moods: 'dawn' (a3), 'day', 'night' (g3, g4), 'dusk'.  night=0..1 may be animated; lamps(amount) wakes them outward from the river.
AY.ground(x, z) -> y of the pavement (ghat, promenade, terraces) for standing figures and lamps; AY.lamp_points() -> Nx3 of every lamp, ordered from the river up."""
import numpy as np, math
from lau import gl
from lau.stage import Light, hexc
from lau.look import *
from lau import fx as FX
from . import place, flora as FL

CW, CD, Z0, TIER, GH, TOP, NC, NR = 120., 120., -140., 36., 48., 300., 44, 14
BOATS = [(-190, 130, .25, 1.0, 0), (120, 210, -.2, 1.25, 1), (330, 110, .1, .9, 0), (-420, 260, .4, 1.1, 1), (560, 300, -.35, 1.2, 0), (-40, 64, .05, .8, 0), (-700, 170, .1, 1.1, 1), (820, 160, .2, 1., 0)]


def tier(r): return GH + TIER * np.clip(r, 0, 7)


def ground(x, z):
    """height of the pavement at x, z (numpy ok)"""
    x, z = np.asarray(x, float), np.asarray(z, float); u = -z; gh = np.clip((np.floor(u / 4.75) + 1) * 2.4, 0, GH); gh = np.where(z > 0, 0., gh); r = np.floor((Z0 - z) / CD); y = np.where(z > Z0, gh, tier(r))
    zb = Z0 - (r + 1) * CD; st = np.clip(np.floor((zb + 64.8 - z) / 3.6) + 1, 0, 18) * 2.; return np.where((z < Z0) & (np.abs(x) < 30) & (r < 7), tier(r) + st, y)


_C = {}


def layout():
    """A (type, hx, H, hz), B (dx, dz, storey, seed) per cell"""
    if 'A' in _C: return _C['A'], _C['B']
    rng = np.random.default_rng(7); A = np.zeros((NR, NC, 4)); B = np.zeros((NR, NC, 4))
    for r in range(NR):
        for k in range(NC):
            x = (k - NC / 2 + .5) * CW; cx = abs(x); s = rng.uniform(.01, .999); t = rng.choice([1, 2, 3, 4, 5, 6, 0], p=[.24, .21, .17, .15, .04, .06, .13]); fh = rng.choice([27., 29., 31.])
            if cx > 2000 and rng.uniform() < .5: t = 0
            if r >= 7 and cx < 600: t = 0
            if cx < 70 and r < 7: t = [4, 1, 2, 3, 4, 1, 4][r]
            if r == 0 and cx < 400: t = {1: 3, 2: 2, 3: 4}.get(int(cx // 120) + (1 if cx > 70 else 0), t)
            hx, hz = rng.uniform(38, 50), rng.uniform(36, 48); n = rng.integers(1, 4); peak = 1 + .45 * math.exp(-(x / 800) ** 2) * (.4 + r / 12); H = fh * n
            if t == 1: H = fh * int(max(1, round(n * peak)))
            if t == 2: H = rng.uniform(105, 160) * peak; hx, hz = rng.uniform(34, 46), rng.uniform(46, 53)
            if t == 3: H = fh * int(max(2, round((n + .4) * peak)))
            if t == 4: H = round(rng.choice([2, 2, 3]) * fh) / .46
            if t == 5: hx = rng.uniform(14, 18); hz = hx * 1.7 + 2; H = fh * rng.integers(3, 5)
            if t == 6: H = rng.uniform(90, 120)
            dx = dz = 0.
            if cx < 70: hx = min(hx, 38.); dx = 18. * np.sign(x); hz = min(hz, 46.)
            if t in (1, 3, 4) : dx += rng.uniform(-1, 1) * (54 - hx) * (cx > 70); dz = rng.uniform(-1, 1) * (54 - hz)
            if r == 0: dz = 0.
            A[r, k] = (t, hx, H, hz); B[r, k] = (dx, dz, fh, s)
    _C['A'], _C['B'] = A, B; return A, B


def tex():
    if 't' not in _C:
        A, B = layout(); T = np.zeros((NR * 2, NC, 4), 'f4'); T[0::2] = A; T[1::2] = B; t = gl.ctx().texture((NC, NR * 2), 4, T.tobytes(), dtype='f4'); t.filter = (0x2600, 0x2600); _C['t'] = t
    return _C['t']


MOOD = dict(
    dawn=dict(sky=dict(cZen='#5a6ab0', cMid='#e89a86', cHor='#ffd88a', cLow='#f7b878', sunDir=(-.30, .105, -1.), sunR=.075, rays=.75, halo=1., cov=.62, cy0=.07, cy1=.34, cLit='#fff0c8', cCM='#f2a890', cSh='#b87a94', cInk='#5a2a44'),
              light=dict(key=(-.62, .42, .30), keyCol='#ffdcae', amb='#a89ad0', rim=(-.5, .3, -.9), rimCol=(1.3, .9, .5), bounceCol=(.25, .15, .10), envT='#ffe0b8', envM='#ffc07a', envB='#8a5a7a', fogCol='#f8c49a', fog=(.00048, 560., .0012, 0.), ink=3., inkRef=4., edge=.49, inkCol='#2c1220'),
              w=('#ffcf8a', '#b79ac0', (1.5, .95, .45)), ck=.7),
    day=dict(sky=DAY, light=dict(key=(.5, .7, .45), keyCol='#fff4dc', amb='#9fb0d0', rimCol=(.4, .4, .4), envT='#ffffff', envM='#ffeccc', envB='#8a9a8a', fogCol='#cfe0e4', fog=(.00035, 250., .0016, 0.), inkRef=4.), w=('#dcecf0', '#6aa8d0', (.5, .5, .4)), ck=1.),
    dusk=dict(sky=DUSK, light=dict(key=(-.6, .25, -.2), keyCol='#ff9a5a', amb='#6a4a8a', rim=(-.5, .2, -.8), rimCol=(1.4, .6, .3), envT='#8a4a7a', envM='#ff8a4a', envB='#4a2450', fogCol='#b8503e', fog=(.0005, 200., .0016, 0.), inkRef=4.), w=('#f08a4a', '#4a2a5a', (1.2, .5, .2)), ck=.6),
    night=dict(sky=dict(**{**NIGHT, 'cZen': '#05071e', 'cMid': '#131a4a', 'cHor': '#3a3268', 'cLow': '#141440', 'cov': .40, 'sunDir': (.5, .55, -1.), 'cCM': '#3c4684', 'sunR': .0, 'sunGlow': .15, 'halo': 0.}),
               light=dict(key=(.5, .7, .25), keyCol='#3e4c96', amb='#2a3270', rim=(.4, .4, -.8), rimCol=(.22, .24, .45), bounceCol=(.25, .10, .03), envT='#5a5aa0', envM='#ffb45a', envB='#c86a2a', fogCol='#201c4c', fog=(.00036, 300., .0016, 0.), inkRef=4., ink=3., inkCol='#05040f'),
               w=('#2c2a5c', '#0a0e30', (.1, .1, .2)), ck=.32))


def sky(mood='dawn', **k): return SKY(MOOD[mood]['sky'], **k)


def light(mood='dawn', **k): return Light(**{**MOOD[mood]['light'], **k})


def draw(st, mood='dawn', night=None, fill=1., boats=None, defs='', **u):
    w = MOOD[mood]['w']; b = np.zeros((8, 4), 'f4')
    for i, q in enumerate((BOATS if boats is None else boats)[:8]): b[i] = q[:4]
    n = (1. if mood == 'night' else 0.) if night is None else night
    place.draw(st, 'ayodhya.glsl', u=dict(night=float(n), fill=float(fill), boats=b, skyA=hexc(w[0]), skyB=hexc(w[1]), skyC=hexc(w[2]), **u), texs=dict(tCity=tex()), defs=defs, sun=0. if n > .5 else 1.)


def _trees():
    if 'tr' in _C: return _C['tr']
    A, B = layout(); r_ = np.random.default_rng(3); T = {k: [] for k in ('pahari_round', 'mango', 'ashoka_weep', 'palm', 'kadamba', 'plantain', 'shrub', 'ashoka')}
    for r in range(NR):
        for k in range(NC):
            x, z = (k - NC / 2 + .5) * CW, Z0 - (r + .5) * CD; t, hx, H, hz = A[r, k]; y = tier(r)
            if t in (0, 6) and not (r >= 7 and abs(x) < 620):
                for _ in range(7 if t == 0 else 3): T[r_.choice(['pahari_round', 'mango', 'palm', 'kadamba', 'ashoka'])].append((x + r_.uniform(-50, 50), y, z + r_.uniform(-50, 50)))
            elif t in (2, 5) or r_.uniform() < .5:
                for s in (-1, 1): T[r_.choice(['ashoka_weep', 'palm', 'mango', 'pahari_round'])].append((x + s * 56, y, z + r_.uniform(30, 57)))
    for x in np.r_[np.arange(-1500, -380, 300), np.arange(450, 1500, 300)]: T['banyan' if False else 'pahari_round'].append((x + r_.uniform(-40, 40), GH, -118.)); T['mango'].append((x + 90, GH, -122.))
    for x in (-250, -110, 108, 255): T['ashoka_weep'].append((x, GH, -124.))
    for r in range(7):                                             # the avenue
        for s in (-1, 1): T['ashoka_weep'].append((s * 37., tier(r), Z0 - r * CD - 24))
    for x in (-250, -190, 190, 250, -120, 120): T['ashoka_weep'].append((x * 1.4, TOP, -985.)); T['mango'].append((x * 2.1, TOP, -990.))
    T['palm'] += [(x, TOP, -1130. + (i % 2) * 40) for i, x in enumerate(np.linspace(-820, 820, 24)) if abs(x) > 545]
    for x in np.arange(-2400, 2500, 70): T[r_.choice(['pahari_round', 'mango', 'palm', 'kadamba'])].append((x + r_.uniform(-30, 30), TOP, -1840 + r_.uniform(-60, 40)))
    T = {k: [q for q in v if not (abs(q[0]) < 42 and q[2] > -1000 and k != 'ashoka_weep') and not (abs(q[0]) < 34 and q[2] > -1000)] for k, v in T.items()}; _C['tr'] = {k: np.array(v) for k, v in T.items() if v}; return _C['tr']


HGT = dict(pahari_round=62, mango=54, ashoka_weep=66, palm=80, kadamba=60, plantain=26, shrub=12, ashoka=54)


def trees(st, mood='dawn', season='summer', hills=True, wind=.4):
    tint = dict(dawn=(1.0, .86, .86), day=(1, 1, 1), dusk=(.8, .6, .7), night=(.9, .8, .75))[mood]; fog = hexc(MOOD[mood]['light']['fogCol'])
    for k, P in _trees().items(): FL.scatter(st, k, P, HGT[k], season=season, seed=len(k), tint=tint, wind=wind, foot=.35 if mood != 'night' else .8, footCol='#2c1c30' if mood != 'night' else (2.6, .50, .06))
    if hills:
        for z, s, hz in ((-2500, 520, .55), (-3300, 760, .74)): FL.cards(st, FL.plate_of('hill', 'summer', 1 if z < -3000 else 0), [(x * 1.0, 200, z) for x in np.arange(-5200, 5300, 800 if s == 520 else 1200)], s, flip=np.resize([1., -1.], len(np.arange(-5200, 5300, 800 if s == 520 else 1200))), haze=hz if mood != 'night' else .9, hazeCol=fog, wind=0., tint=tint)


def lamp_points(step=9.):
    """every lamp of the city (N,3), ordered from the river upward"""
    if 'lp' in _C: return _C['lp']
    A, B = layout(); P = []; add = P.append
    for i in range(1, 20, 1):                                       # ghats
        z, y = -i * 4.75 + 2., i * 2.4 + .6; sp = 14. if i % 2 else 21.; x = np.arange(-1500, 1500, sp) + (i * 5 % 14); m = np.abs(x) > 0; add(np.c_[x[m], np.full(m.sum(), y), np.full(m.sum(), z)])
    x = np.arange(-2600, 2600, 10.); add(np.c_[x, np.full(len(x), GH + 5.), np.full(len(x), -95.)])
    for r in range(1, 8): x = np.arange(-2600, 2600, 12.); x = x[np.abs(x) > 36]; add(np.c_[x, np.full(len(x), tier(r) + 1.2), np.full(len(x), Z0 - r * CD + 1.2)])
    for r in range(7):                                              # avenue
        z = np.arange(Z0 - r * CD, Z0 - (r + 1) * CD, -9.); [add(np.c_[np.full(len(z), s * 31.), ground(0 * z, z) + 1.5, z]) for s in (-1, 1)]
        for j in range(1, 19, 2): x = np.arange(-27, 28, 9.); add(np.c_[x, np.full(len(x), tier(r) + j * 2 + .6), np.full(len(x), Z0 - (r + 1) * CD + 64.8 - (j - .5) * 3.6)])
    def ring(cx, y, cz, hx, hz, sp):
        x = np.arange(-hx, hx + .1, sp); z = np.arange(-hz, hz + .1, sp); o = 1.4
        add(np.c_[cx + x, np.full(len(x), y), np.full(len(x), cz + hz + o)]); add(np.c_[cx + x, np.full(len(x), y), np.full(len(x), cz - hz - o)]); add(np.c_[np.full(len(z), cx + hx + o), np.full(len(z), y), cz + z]); add(np.c_[np.full(len(z), cx - hx - o), np.full(len(z), y), cz + z])
    for r in range(NR):
        for k in range(NC):
            t, hx, H, hz = A[r, k]; dx, dz, fh, s = B[r, k]; cx, cz = (k - NC / 2 + .5) * CW + dx, Z0 - (r + .5) * CD + dz; y = tier(r)
            if t == 0 or abs(cx) > 2500: continue
            if t in (1, 4, 5):
                Ht = H * .46 if t == 4 else H; w, d = (hx, hx) if t == 5 else (hx, hz)
                for j in range(1, int(round(Ht / fh)) + 1): ring(cx, y + j * fh + 1.2, cz, w + .6, d + .6, step)
                if t == 4: R = min(hx, hz) * .66; a = np.linspace(0, 6.283, 22); add(np.c_[cx + R * np.cos(a), np.full(22, y + Ht + R * .62), cz + R * np.sin(a)])
            elif t == 3:
                H1 = math.floor(H * .62 / fh + .5) * fh
                for j in range(1, int(H1 / fh) + 1): ring(cx, y + j * fh + 1.2, cz + hz * .36, hx + .6, hz * .64 + .6, step)
                sg = 1 if s > .5 else -1
                for j in range(int(H1 / fh) + 1, int(H / fh) + 1): ring(cx - hx * .22 * sg, y + j * fh + 1.2, cz - hz * .45, hx * .72 + .6, hz * .52 + .6, step)
            elif t == 2:
                for j in range(1, 8): yy = .22 * H + .07 * H * j; q = min(1, max(0, (yy - .22 * H) / (.6 * H))); rr = hx * .62 * (1 - .8 * q ** 1.55) * 1.14; ring(cx, y + yy, cz - hz * .3, rr, rr, max(4., step * .7))
                ring(cx, y + 5, cz, hx, hz, step)
            elif t == 6: ring(cx, y + 6, cz, hx, hz, step)
    S = 1.5
    for hx, H, hz in ((250, 74, 84), (168, 148, 66), (92, 222, 52)): [ring(0, TOP + S * yy + 1.5, -1190, S * hx + 1, S * hz + 1, step) for yy in np.arange(37 if hx > 200 else H - 37, H + 1, 37)]
    for yy, rr in ((252, 50), (268, 57), (292, 58), (312, 44)): a = np.linspace(0, 6.283, 90); add(np.c_[S * rr * np.cos(a), np.full(90, TOP + S * yy), -1190 + S * rr * np.sin(a)])
    for cx, cy, w, h in ((306, 0, 34, 262), (222, 74, 18, 110)):
        for s in (-1, 1):
            for j in range(1, 10): yy = h * (.22 + .065 * j); q = min(1, (yy / h - .22) / .6); rr = w * (1 - .8 * q ** 1.55) * 1.14; ring(s * S * cx, TOP + S * (cy + yy), -1190, S * rr, S * rr, 8.)
    P = np.vstack(P); d = -P[:, 2] + np.abs(P[:, 0]) * .25; _C['lp'] = P[np.argsort(d, kind='stable')]; return _C['lp']


def lamps(st, amount=1., size=1.1, gain=1., seed=0, col='#ffa64a', water=220, minpx=1.5, every=1, mirror=2600):
    """after st.close(): the flames.  amount wakes them from the river up; size in world units (grows to `minpx` pixels when far)"""
    P = lamp_points()[::every]; n = len(P); r = np.random.default_rng(seed); j = np.clip(np.arange(n) / n + r.normal(0, .03, n), 0, 1); al = np.clip((amount * 1.1 - j) * 14, 0, 1)
    if water:
        g = np.random.default_rng(5); W_ = np.c_[g.uniform(-900, 900, water), np.full(water, .9), 8 + 500 * g.uniform(0, 1, water) ** 1.7]; W_[:, 0] += st.t * g.uniform(3, 9, water); P = np.vstack([P, W_]); al = np.r_[al, np.full(water, min(1., amount * 2))]
    c = (P - st.cam.eye) @ st.cam.R.T; z = np.maximum(c[:, 2], 1.); px = st.cam.fl * 540 / z; m = (c[:, 2] > 2) & (np.abs(c[:, 0]) * st.cam.fl < z * 1.85) & (np.abs(c[:, 1]) * st.cam.fl < z * 1.1) & (al > 0)
    P, z, px, al = P[m], z[m], px[m], al[m]; ph = np.random.default_rng(seed + 1).uniform(0, 6.28, len(m))[m]; fl = .86 + .14 * np.sin(st.t * 9 + ph) * np.sin(st.t * 5.3 + ph * 2)
    s = np.maximum(size * 2.0, minpx * 2.2 / px); dim = np.clip((size * 2.0) * px / (minpx * 2.2), .30, 1.) ** .55
    FX.particles(st, P, s, np.array(hexc(col)) * 1.5 * gain, 'lamp', seed=ph, alpha=al * fl * dim)
    if mirror and st.cam.eye[1] > 1:                                # the lights lie on the river as broken streaks
        A = lamp_points(); g = np.random.default_rng(9); A = A[(np.abs(A[:, 0]) < 1300)]; A = A[g.permutation(len(A))[:mirror]]; n2 = len(A); e = st.cam.eye; k = e[1] / (e[1] + A[:, 1]); Q = e + (A * [1, -1, 1] - e) * k[:, None]
        w = np.sin(st.t * g.uniform(2, 5, n2) + g.uniform(0, 6.28, n2)); Q[:, 0] += w * 1.5; Q[:, 1] = .15; m = (Q[:, 2] > 3) & (((Q - e) @ st.cam.R.T)[:, 2] > 5); Q, w = Q[m], w[m]; zz = ((Q - e) @ st.cam.R.T)[:, 2]; p2 = st.cam.fl * 540 / zz
        FX.particles(st, Q, 1.7 / p2, np.array(hexc('#ff9a3a')) * 1.3, 'ember', vel=np.c_[0 * w, (34 + 18 * w) / p2, 0 * w], alpha=min(1., amount * 1.5) * (.30 + .25 * w) * gain)


def birds(st, n=14, at=(-300, 330, -500), spread=(300, 60, 200), size=9., seed=1, col='#4a2a3c'):
    """after close: a loose flock, inked"""
    r = np.random.default_rng(seed)
    P = np.asarray(at, float) + r.uniform(-1, 1, (n, 3)) * spread + np.array([st.t * 26, st.t * 3, 0]); ph = r.uniform(0, 6.28, n)
    def fn(c):
        for p, a in zip(P, ph):
            x, y, z = st.cam.project(p)
            if z < 5: continue
            k = size * st.cam.px(p); f = math.sin(st.t * 9 + a) * .5; c.set_line_width(max(1., k * .16)); c.set_source_rgb(*hexc(col, False)); c.move_to(x - k, y - k * (.2 + f)); c.curve_to(x - k * .5, y - k * (.5 + f * .4), x - k * .2, y - k * .1, x, y); c.curve_to(x + k * .2, y - k * .1, x + k * .5, y - k * (.5 + f * .4), x + k, y - k * (.2 + f)); c.stroke()
    st.vector(fn)
