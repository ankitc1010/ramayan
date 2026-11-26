"""The halls: HALL 0 'mithila' (a4), 1 'ayodhya' (b2, toward the gate) and 'crown' (b1, same hall, gold light, toward the throne), 2 'ravana' (d7).  Geometry, cameras and uniforms: top of palace.glsl.

    from worlds import palace as PL
    st.paint('sky.frag', **PL.sky('ayodhya'));  st.open(cam, PL.light('ayodhya', at=(0, 10, -60)));  PL.draw(st, 'ayodhya', lamps=18, dusk=1.);  st.close();  PL.flames(st, 'ayodhya', lamps=18)
lamps: how many of the 18 stands of the coronation hall burn, counted from the gate (stand j is at x = -34 / +34 alternately); animate it down (or pass order='far' to put out the ones near the throne first: stands are then counted from the throne).
PL.flame_points(hall) -> Nx3.  PL.light(hall, at=) puts the 6 flames nearest `at` into Light.pts so figures are lit by them."""
import numpy as np, math
from lau.stage import Light, hexc
from lau.look import *
from lau import fx as FX
from . import place
HALLS = dict(mithila=0, ayodhya=1, crown=1, ravana=2)
BZ, GZ = 48., -430.
MOOD = dict(
    mithila=dict(sky=DAWN, light=dict(key=(-.75, .42, .38), keyCol='#f2c088', amb='#7a5a74', rim=(.7, .3, -.6), rimCol=(.9, .6, .3), bounceCol=(.14, .08, .03), envT='#ffe6b0', envM='#ffc070', envB='#8a4a2a', fogCol='#d08a4a', fog=(.0011, 150., .0, 0.), ink=3., inkRef=2.2, inkCol='#1c0c10'), pts=(1.5, .75, .25)),
    ayodhya=dict(sky=dict(**{**DUSK, 'cZen': '#2a1038', 'cMid': '#8a1f34', 'cHor': '#ff6a34', 'cLow': '#a0301c', 'sunDir': (0., .055, -1.), 'sunR': .055, 'sunCol': '#ff9a5a', 'sunGlow': .5, 'rays': .35, 'cov': .5, 'cy0': .10, 'cy1': .4}), light=dict(key=(.12, .24, -1.), keyCol='#b04026', amb='#42284e', rim=(0., .25, -1.), rimCol=(1.3, .40, .14), bounceCol=(.22, .06, .02), envT='#8a3a44', envM='#ffb054', envB='#c8542a', fogCol='#4a1626', fog=(.0007, 160., .0, 0.), ink=3., inkRef=2.2, inkCol='#0c0408'), pts=(1.5, .62, .16)),
    crown=dict(sky=DUSK, light=dict(key=(-.5, .55, -.65), keyCol='#ffc078', amb='#6a4668', rim=(.4, .4, .8), rimCol=(1.1, .6, .2), bounceCol=(.25, .10, .03), envT='#ffe0a0', envM='#ffc060', envB='#a8502a', fogCol='#7a3024', fog=(.0008, 160., .0, 0.), ink=3., inkRef=2.2, inkCol='#14060a'), pts=(1.4, .62, .18)),
    ravana=dict(sky=BLOOD, light=dict(key=(-.4, .5, .5), keyCol='#b0563a', amb='#30162c', rim=(.3, .3, -.9), rimCol=(1.1, .22, .06), bounceCol=(.35, .06, .01), envT='#5a1c30', envM='#ffb060', envB='#ff6a2a', fogCol='#2c060c', fog=(.0016, 120., .0, 0.), ink=3., inkRef=2.2, inkCol='#050204'), pts=(1.8, .42, .08)))


def flame_points(hall, order='gate'):
    if HALLS[hall] == 1:
        P = [(sx * 34., 34.8, GZ + 46 + k * BZ) for k in range(9) for sx in (-1, 1)]; return np.array(P if order == 'gate' else P[::-1])
    if hall == 'mithila': return np.array([(0., 64.6, BZ * .5 + BZ * k) for k in range(-6, 9)])
    return np.array([(sx * 34., 14.4, BZ * .5 + BZ * k) for k in range(-4, 4) for sx in (-1, 1)])


def sky(hall, **k): return SKY(MOOD[hall]['sky'], **k)


def light(hall, at=None, lamps=18., order='gate', gain=1., **k):
    L = Light(**{**MOOD[hall]['light'], **k})
    if at is not None:
        P = flame_points(hall, order); on = np.clip(lamps - np.arange(len(P)), 0, 1) if HALLS[hall] == 1 else np.ones(len(P)); o = np.argsort(np.linalg.norm(P - np.asarray(at, float), axis=1) + 1e4 * (on <= 0))[:6]; c = MOOD[hall]['pts']
        L.pts = [(tuple(P[i]), 20., tuple(v * on[i] * gain for v in c)) for i in o if on[i] > 0]
    return L


def draw(st, hall, lamps=18., dusk=1., lit=1., order='gate', polish=True, defs=''):
    """lamps / dusk for 'ayodhya'; lit 0..1 for the others"""
    d = '#define HALL %d\n' % HALLS[hall] + ('#define POLISH\n' if polish else '') + defs
    if order != 'gate': d += '#define LAMPREV\n'
    place.draw(st, 'palace.glsl', u=dict(lamps=float(lamps), dusk=float(dusk), lit=float(lit)), defs=d, sun=0.)


def flames(st, hall, lamps=18., lit=1., h=None, order='gate', glow=.5):
    """after close: the flames themselves (particles far, true lamp flames near)"""
    P = flame_points(hall, order); on = np.clip(lamps - np.arange(len(P)), 0, 1) if HALLS[hall] == 1 else np.full(len(P), lit); m = on > .01; P, on = P[m], on[m]; c = (P - st.cam.eye) @ st.cam.R.T; h = h or dict(mithila=3.4, ayodhya=4.2, crown=4.2, ravana=9.)[hall]
    for i in np.argsort(-c[:, 2]):
        if c[i, 2] < 2: continue
        px = h * on[i] * st.cam.px(P[i]); x, y, _ = st.cam.project(P[i])
        if not (-200 < x < 2120 and -200 < y < 1400): continue
        if hall == 'ravana': FX.particles(st, P[i:i + 1] + [[0, h * .55, 0]], h * .8, (.9, .55, .35), 'tongue', seed=np.array([i * .37 % 1]))
        else: FX.particles(st, P[i:i + 1] + [[0, h * .3, 0]], max(h * .62, 4. / st.cam.px(P[i])) * on[i], '#ffa64a', 'lamp', alpha=on[i])
        if px > 14 and hall != 'ravana': FX.flame(st, P[i], h * on[i], glow=glow * on[i], seed=i * 1.7)
