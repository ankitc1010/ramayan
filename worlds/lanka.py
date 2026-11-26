"""Lanka: setup and helpers for lanka.glsl.

    from worlds import lanka as LK
    st.paint('sky.frag', **LK.sky('moon')); LK.moon(st); st.open(cam, LK.light('moon')); LK.draw(st, 'moon'); st.close(); LK.lamps(st)
    burning: st.open(cam, LK.light('fire')); LK.draw(st, 'fire', fire=.6, fireAt=(x, y, z)); st.close(); P, S = LK.fires(.6, fireAt, cam, n=400); FX.particles(st, P, S, (.95, .86, .80), 'tongue', seed=Q)
Far views: st.open(cam, light, far=20000).
Moods: 'moon' (d5), 'fire' (d8), 'dark' (f1), 'day' (e2 horizon, e1).
LK.roofs() -> list of dict(x, y, z, w, kind): flat landing places; LK.path(n) -> n roof points that climb from the front wall to the palace (for Hanuman's leaps); LK.fire_points() -> Nx4 (x, y, z, size) where flames sit.
LK.ground(x, z) -> terrace height.  Gate sill at (0, 260, 1190); sea stair foot at (0, 0, 1560)."""
import numpy as np, math
from lau import gl
from lau.stage import Light, hexc
from lau.look import *
from lau import fx as FX
from . import place

CW, NC, RIM, PK0, PK1, PK2 = 100., 24, 260., 640., 550., 510.
PEAKS = [((0., -60.), 380., 660., 1.12, 180.), ((-560., 60.), 290., 330., 1.1, 80.), ((580., 0.), 250., 320., 1.1, 80.)]
_C = {}


def _rimR(a): return 1180 + 26 * np.sin(a * 5 + 1) + 18 * np.sin(a * 9)


def _hill(x, z):
    h = 0.
    for (cx, cz), a, R, p, d0 in PEAKS: h = max(h, a * min(1., max(0., 1 - (math.hypot(x - cx, z - cz) - d0) / R)) ** p)
    return h


def layout():
    if 'A' in _C: return _C['A'], _C['B']
    rng = np.random.default_rng(11); A = np.zeros((NC, NC, 4)); B = np.zeros((NC, NC, 4))
    for j in range(NC):
        for i in range(NC):
            x, z = (i - NC / 2 + .5) * CW, (j - NC / 2 + .5) * CW; l = math.hypot(x, z)
            if l + 71 > _rimR(math.atan2(x, z)) - 40: continue
            top = RIM + 36 * round(_hill(x, z) / 36); t = rng.choice([1, 2, 3, 4, 0], p=[.20, .28, .22, .24, .06]); n = rng.integers(1, 4); hx, hz = rng.uniform(33, 43), rng.uniform(33, 43); H = 30. * (n + 1); s = rng.uniform(.02, .98); dx, dz = rng.uniform(-4, 4, 2)
            if t == 1: H = rng.uniform(120, 210); hx, hz = rng.uniform(30, 40), rng.uniform(22, 30)
            if t == 2: H = 60. * rng.integers(1, 3)
            if t == 3: H = rng.uniform(120, 200); hx = hz = rng.uniform(32, 42)
            if t == 4: H = 30. * rng.integers(1, 4)
            if abs(x) < 60 and z > 100: t = 0 if z < 1000 else t          # the processional way
            if z > 960 and abs(x) < 190: t = 0
            if max(abs(x), abs(z + 60)) < 225: top, t = PK0, 0
            if max(abs(x + 560), abs(z - 60)) < 115: top, t = PK1, 0
            if max(abs(x - 580), abs(z)) < 115: top, t = PK2, 0
            A[j, i] = (t, hx, H, hz); B[j, i] = (dx, dz, top, s)
    _C['A'], _C['B'] = A, B; return A, B


def tex():
    if 't' not in _C:
        A, B = layout(); T = np.zeros((NC * 2, NC, 4), 'f4'); T[0::2] = A; T[1::2] = B; t = gl.ctx().texture((NC, NC * 2), 4, T.tobytes(), dtype='f4'); t.filter = (0x2600, 0x2600); _C['t'] = t
    return _C['t']


def ground(x, z):
    A, B = layout(); i, j = int(math.floor(x / CW)) + NC // 2, int(math.floor(z / CW)) + NC // 2
    return float(B[j, i, 2]) if 0 <= i < NC and 0 <= j < NC else 0.


def roofs():
    """flat roofs and ledges: dict(x, y, z, w half width, kind 1 gopura 2 dome 3 spire 4 terrace)"""
    A, B = layout(); R = []
    for j in range(NC):
        for i in range(NC):
            t, hx, H, hz = A[j, i]; dx, dz, top, s = B[j, i]
            if t == 0: continue
            x, z = (i - NC / 2 + .5) * CW + dx, (j - NC / 2 + .5) * CW + dz; y = top + (H * .82 + min(hx, hz) * .5 if t == 1 else math.floor(H * .5 / 30 + .5) * 30 if t == 2 else H if t == 3 else H)
            R.append(dict(x=x, y=y, z=z, w=min(hx, hz), kind=int(t), top=top, H=H))
    return R


def path(n=12, side=1, seed=0):
    """n landing points on terrace edges and domed blocks, winding up from the front wall round the middle peak"""
    R = [r for r in roofs() if r['kind'] in (2, 4)]; out = []
    for k in range(n):
        u = k / max(1, n - 1); a = side * (.15 + 2.2 * u); rad = 1000 * (1 - .68 * u); t = np.array([math.sin(a) * rad, math.cos(a) * rad - 30 * u]); b = min((r for r in R if r not in out), key=lambda r: (r['x'] - t[0]) ** 2 + (r['z'] - t[1]) ** 2); out.append(b)
    return [np.array([r['x'] + r['w'] * .72 * (1 if r['kind'] == 2 else .85), r['y'] + .8, r['z'] + r['w'] * .72 * (1 if r['kind'] == 2 else .85)]) for r in out]


def fire_points():
    """(x, y, z, size): roof edges, tower tops, terrace corners where flames sit (N,4)"""
    if 'fp' in _C: return _C['fp']
    A, B = layout(); r = np.random.default_rng(4); P = []
    for j in range(NC):
        for i in range(NC):
            t, hx, H, hz = A[j, i]; dx, dz, top, s = B[j, i]; x, z = (i - NC / 2 + .5) * CW + dx, (j - NC / 2 + .5) * CW + dz
            if t == 0: continue
            if t == 1: P += [(x + u * hx * .4, top + H * (.82 + .1), z, 26.) for u in (-.8, 0, .8)] + [(x + sx * hx * .8, top + H * .45, z + sz * hz * .8, 18.) for sx in (-1, 1) for sz in (-1, 1)]
            elif t == 2: y = top + math.floor(H * .5 / 30 + .5) * 30; P += [(x + sx * (hx - 4), y + 4, z + sz * (hz - 4), 22.) for sx in (-1, 0, 1) for sz in (-1, 0, 1) if (sx, sz) != (0, 0)] + [(x, y + min(hx, hz) * 1.6, z, 30.)]
            elif t == 3: P += [(x, top + H * .9, z, 30.)] + [(x + sx * hx * .8, top + 10 + H * .30, z + sz * hz * .8, 18.) for sx in (-1, 1) for sz in (-1, 1)]
            else: P += [(x + sx * (hx - 4), top + H + 4, z + sz * (hz - 4), 22.) for sx in (-1, 0, 1) for sz in (-1, 0, 1) if (sx, sz) != (0, 0)] + [(x, top + H + 60, z, 26.)]
    for k in range(44): a = k / 44 * 6.283; R = _rimR(a) - 24; P.append((math.sin(a) * R, RIM + 92, math.cos(a) * R, 26.))
    P += [(u * 80, PK0 + 110 + 330 + 40, -60, 70.) for u in (-.5, 0, .5)] + [(sx * 138, PK0 + 58 + 130, -60 + sz * 138, 46.) for sx in (-1, 0, 1) for sz in (-1, 0, 1) if (sx, sz) != (0, 0)] + [(sx * 110, PK0 + 112, -60 + sz * 110, 40.) for sx in (-1, 1) for sz in (-1, 1)] + [(-560, PK1 + 290, 60, 60.), (580, PK2 + 190, 0, 60.)]
    _C['fp'] = np.array(P); return _C['fp']


def burn(P, fire, at):
    """0..1 how far each point burns (same rule as the shader, without its noise)"""
    P = np.asarray(P, float)[:, :3]; d = np.linalg.norm((P - np.asarray(at)) * [1, .7, 1], axis=1); return np.clip((fire * 2700 - d - 120) / 170, 0, 1)


def fires(fire, at, cam, n=900, per=2, rise=1.0, near=90.):
    """positions and sizes of flame particles (kind 'tongue') for the visible burning points: returns P (M,3), size (M,), seed (M,)"""
    F = fire_points(); b = burn(F, fire, at); c = (F[:, :3] - cam.eye) @ cam.R.T; m = (b > .05) & (c[:, 2] > 5) & (np.abs(c[:, 0]) * cam.fl < c[:, 2] * 2.1) & (np.abs(c[:, 1]) * cam.fl < c[:, 2] * 1.6); F, b, z = F[m], b[m], c[m, 2]
    m = z > near; F, b, z = F[m], b[m], z[m]; r = np.random.default_rng(6); k_ = n // per; o = np.arange(len(F)) if len(F) <= k_ else np.sort(np.random.default_rng(5).permutation(len(F))[:k_]); F, b = F[o], b[o]; P, S, Q = [], [], []
    for k in range(per): j = r.uniform(-1, 1, (len(F), 3)); s = F[:, 3] * b * (1.5 - .3 * k) * rise; P.append(F[:, :3] + j * F[:, 3:4] * [.5, .12, .5] + np.c_[0 * s, s * .72, 0 * s]); S.append(s); Q.append((np.arange(len(F)) * .618 + k * .37) % 1)
    P, S, Q = np.vstack(P), np.hstack(S), np.hstack(Q); o = np.argsort(-((P - cam.eye) ** 2).sum(1)); return P[o], S[o], Q[o]


MOOD = dict(
    moon=dict(sky={**NIGHT, 'cZen': '#040720', 'cMid': '#0f1a4c', 'cHor': '#33509a', 'cLow': '#0c1440', 'sunDir': (.10, .235, -1.), 'sunR': 0., 'sunCol': '#c8d0f0', 'sunGlow': .35, 'halo': 0., 'cov': .50, 'cy0': .015, 'cy1': .16, 'cLit': '#b8c6ee', 'cCM': '#5a6cb0', 'cSh': '#232e66', 'cInk': '#0a0e2a', 'cink': .6},
              light=dict(key=(.45, .55, .25), keyCol='#8c9ce0', amb='#3c4488', rim=(.10, .25, -1.), rimCol=(.75, .85, 1.25), bounceCol=(.18, .08, .02), envT='#8fa8ff', envM='#ffd284', envB='#e88a34', fogCol='#2c4488', fog=(.00016, 900., .0012, 0.), ink=3., inkRef=12., inkCol='#05040f'), w=('#3a56a0', '#070b2a', (1.1, 1.05, .9))),
    fire=dict(sky={**BLOOD, 'cZen': '#05030a', 'cMid': '#140714', 'cHor': '#4a150e', 'cLow': '#0a0308', 'sunR': 0., 'sunGlow': 0., 'rays': 0., 'cov': .55, 'cy0': .03, 'cy1': .4, 'cLit': '#7a2c14', 'cCM': '#30101a', 'cSh': '#12060e', 'starAmt': .4},
              light=dict(key=(.4, -.1, .6), keyCol='#c0602c', amb='#321838', rim=(.1, .4, -1.), rimCol=(1.5, .55, .15), bounceCol=(.5, .18, .04), envT='#5a1c3a', envM='#ff8a3a', envB='#ffc05a', fogCol='#2c0a0c', fog=(.00024, 500., .0010, 0.), ink=3., inkRef=10., inkCol='#080206'), w=('#2a0a0a', '#040106', (1.2, .45, .12))),
    dark=dict(sky={**BLOOD, 'cZen': '#040208', 'cMid': '#16060e', 'cHor': '#4a1010', 'cLow': '#0a0306', 'sunR': 0., 'sunGlow': 0., 'rays': 0., 'cov': .7, 'cLit': '#5a1a1a', 'cCM': '#2a0c14', 'cSh': '#10050c'},
              light=dict(key=(-.5, .5, .4), keyCol='#5a3040', amb='#2c1830', rim=(.3, .4, -.8), rimCol=(.75, .20, .04), bounceCol=(.12, .03, .01), envT='#4a1c3a', envM='#c8502a', envB='#ff8a3a', fogCol='#1c0810', fog=(.0005, 200., .001, 0.), ink=3., inkRef=4., inkCol='#040104'), w=('#3a0c0c', '#050106', (.6, .2, .06))),
    day=dict(sky=DAY, light=dict(key=(.45, .6, .4), keyCol='#fff0d0', amb='#8fa0c8', rimCol=(.5, .5, .5), envT='#ffffff', envM='#ffe6b0', envB='#a88a5a', fogCol='#cfe6ea', fog=(.00010, 900., .0012, 0.), inkRef=12.), w=('#cfe8ea', '#2a8aa8', (.8, .8, .7))))


def sky(mood='moon', **k): return SKY(MOOD[mood]['sky'], **k)


MOON = (.02, .235, -1.)


def moon(st, R=.30, dir=MOON, amt=1., glow=1., cA='#fbf3dc', cB='#a9b4cc', cG='#6f8ad8'):
    """the enormous moon: after paint('sky.frag'), before open"""
    st.paint('moon.frag', 'over', dir=tuple(dir), R=float(R), amt=float(amt), glow=float(glow), cA=tuple(amt * .84 * v for v in hexc(cA)), cB=hexc(cB), cG=hexc(cG))


def light(mood='moon', **k): return Light(**{**MOOD[mood]['light'], **k})


def draw(st, mood='moon', night=None, fire=0., fireAt=(0, 300, 1100), doors=0., defs='', **u):
    w = MOOD[mood]['w']; n = dict(moon=1., fire=1., dark=.6, day=0.)[mood] if night is None else night
    place.draw(st, 'lanka.glsl', u=dict(night=float(n), fire=float(fire), fireAt=tuple(float(v) for v in fireAt), doors=float(doors), skyA=hexc(w[0]), skyB=hexc(w[1]), skyC=w[2], **u), texs=dict(tLanka=tex()), defs=defs, sun=0.)


def lamp_points():
    """lights along terraces, rampart and stair"""
    if 'lp' in _C: return _C['lp']
    A, B = layout(); P = []
    a = np.linspace(0, 6.283, 420, endpoint=False); R = _rimR(a) - 12; P.append(np.c_[np.sin(a) * R, np.full(420, RIM + 60), np.cos(a) * R])
    for j in range(NC):
        for i in range(NC):
            t, hx, H, hz = A[j, i]; dx, dz, top, s = B[j, i]
            if top < 1: continue
            x, z = (i - NC / 2 + .5) * CW, (j - NC / 2 + .5) * CW; u = np.arange(-48, 49, 12.)
            for (di, dj) in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                q = B[j + dj, i + di, 2] if 0 <= j + dj < NC and 0 <= i + di < NC else 0
                if q < top: P.append(np.c_[x + (di * 50.5 + (0 if di else u)) * np.ones(len(u)), np.full(len(u), top + 1.5), z + (dj * 50.5 + (0 if dj else u)) * np.ones(len(u))])
            if t in (2, 4):
                y = top + (math.floor(H * .5 / 30 + .5) * 30 if t == 2 else H) + 5; v = np.arange(-hx, hx + 1, 11.); P.append(np.c_[x + dx + v, np.full(len(v), y), np.full(len(v), z + dz + hz + 1)]); v = np.arange(-hz, hz + 1, 11.); [P.append(np.c_[np.full(len(v), x + dx + sg * (hx + 1)), np.full(len(v), y), z + dz + v]) for sg in (-1, 1)]
    k = np.arange(7); [P.append(np.c_[np.full(7, sg * 68.), RIM * np.clip((378 - 63. * k) / 378, 0, 1) + 30, 1180 + 63. * k]) for sg in (-1, 1)]
    _C['lp'] = np.vstack(P); return _C['lp']


def lamps(st, amount=1., size=1.6, gain=1., col='#ff9a3a', minpx=1.1, mirror=True):
    """after close: the small lights of the city and their streaks on the sea"""
    P = lamp_points(); c = (P - st.cam.eye) @ st.cam.R.T; z = np.maximum(c[:, 2], 1.); px = st.cam.fl * 540 / z; m = c[:, 2] > 4; P, px = P[m], px[m]; n = len(P); ph = np.random.default_rng(2).uniform(0, 6.28, n); fl = .8 + .2 * np.sin(st.t * 7 + ph); s = np.maximum(size * 2, minpx * 2.2 / px); dim = np.clip(size * 2 * px / (minpx * 2.2), .3, 1) ** .6
    FX.particles(st, P, s, np.array(hexc(col)) * 1.4 * gain, 'lamp', seed=ph, alpha=amount * fl * dim)
    if mirror:
        e = st.cam.eye; A = lamp_points(); A = A[np.random.default_rng(8).permutation(len(A))[:900]]; A = A[(A[:, 0] * (e[0] - A[:, 0]) + A[:, 2] * (e[2] - A[:, 2])) > 0]; A = A[(A[:, 1] < 420)]; k = e[1] / (e[1] + A[:, 1]); Q = e + (A * [1, -1, 1] - e) * k[:, None]; Q[:, 1] = .5; w = np.sin(st.t * 3 + np.arange(len(Q)) * 1.7); zz = ((Q - e) @ st.cam.R.T)[:, 2]; m = (zz > 5) & (np.hypot(Q[:, 0], Q[:, 2]) > 830); Q, w, zz = Q[m], w[m], zz[m]; p2 = st.cam.fl * 540 / zz
        if len(Q): FX.particles(st, Q, 1.4 / p2, np.array(hexc(col)) * 1.2, 'ember', vel=np.c_[0 * w, (30 + 18 * w) / p2, 0 * w], alpha=amount * (.22 + .18 * w) * gain)
