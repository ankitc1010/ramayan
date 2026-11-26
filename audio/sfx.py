"""Sound effects.  Every function returns audio whose named instant is at index 0, or (audio, seconds before the instant).
p holds the cue's parameters; n is a length in frames for beds.  S(name, level, words...) registers: level is max momentary LUFS."""
import re
import numpy as np
from numba import njit
from scipy import signal
from core import SR, ns, sec, db, hp, lp, bp, peq, rng, white, env, wander, smooth, sweep, modal, fades, pan, wide, expenv
import perc, inst

REG = {}


def S(name, level=-24, room=None, words=''):
    def deco(fn):
        REG[name] = dict(fn=fn, level=level, room=room or {'open': .25}, words=[name.replace('_', ' ')] + [w.strip() for w in words.split(',') if w.strip()])
        return fn
    return deco


def T(n): return np.arange(n) / SR
def dur(p, d): return p['n'] / 24. if 'n' in p else p.get('dur', d)


def swell(n, a, b): return env([(0, 0), (a, 1), (n / SR - b, 1), (n / SR, 0)], n)


def st(fn, r, *a):
    """Two independent renderings make a wide stereo source."""
    return np.stack([fn(r), fn(r)], 1)


# ---- air --------------------------------------------------------------------------------------------------------------------


def wind(n, r, lo=200, hi=900, rate=.5, q=1.2, whistle=.0):
    x = white(n, r)
    f = np.exp(np.log(lo) + (np.log(hi) - np.log(lo)) * np.clip(.5 + .33 * wander(n, rate, r), 0, 1))
    y = sweep(x, f, q) * (.6 + .4 * np.clip(1 + .6 * wander(n, rate * 1.4, r), 0, 2)) + .35 * lp(x, lo, 1)
    if whistle: y += whistle * sweep(x, f * 2.6, 14.)
    return y


def whoosh(n, r, peak=.5, lo=250, hi=2800, q=1., sharp=2.):
    """Something passes: rises to `peak` (0..1) then falls, in pitch and loudness."""
    u = np.arange(n) / n
    e = np.where(u < peak, (u / peak) ** sharp, ((1 - u) / (1 - peak)) ** (sharp * .8))
    f = lo * (hi / lo) ** e
    return sweep(white(n, r), f, q) * e + .4 * sweep(white(n, r), f * .4, .8) * e


@S('breath', -33, {'close': .4}, 'breath, inhale, exhale')
def _(p, r):
    n = ns(1.1); x = white(n, r)
    e = env([(0, 0), (.28, 1), (.5, .25), (.56, 0), (.62, 0), (.75, .7), (1.1, 0)], n) ** 1.3
    y = (bp(x, 700, 1700) + .6 * bp(x, 2400, 5200) * env([(0, 1), (.5, .9), (.62, .35), (1.1, .2)], n) + .5 * bp(x, 250, 600)) * e
    return fades(y, .02, .05), 0


@S('breath_out', -30, {'close': .5}, 'blows out, blown out')
def _(p, r):
    n = ns(.9); x = white(n, r)
    e = env([(0, 0), (.05, 1), (.2, .7), (.9, 0)], n) ** 1.2
    return fades((bp(x, 350, 1300) + .5 * bp(x, 1800, 4200) * np.exp(-T(n) / .15)) * e, .003, .1)


@S('wind', -30, {'open': .2}, 'wind, gust')
def _(p, r):
    n = ns(dur(p, 3)); return swell(n, .5, .8)[:, None] * st(lambda q: wind(n, q, p.get('lo', 180), p.get('hi', 800), whistle=p.get('whistle', .05)), r)


@S('wind_rush', -22, {'open': .2}, 'rush, flight, flying, speed')
def _(p, r):
    n = ns(dur(p, 3)); y = st(lambda q: wind(n, q, 350, 1700, 1.2, .8), r)
    return swell(n, min(.12, n / SR / 4), .5)[:, None] * y * (1 + .25 * np.clip(wander(n, 3, r), -1.5, 1.5))[:, None]


@S('mountain_wind', -27, {'open': .4})
def _(p, r):
    n = ns(dur(p, 4)); return swell(n, .8, 1.)[:, None] * st(lambda q: wind(n, q, 130, 520, .35, 1.6, .12), r)


@S('whoosh', -23, {'open': .3}, 'whoosh, through cloud, through clouds, swish, sweep, passes, wipe, pass by, dart, swing')
def _(p, r):
    d = dur(p, .7); pk = p.get('peak', .55); n = ns(d)
    x = whoosh(n, r, pk, p.get('lo', 220), p.get('hi', 2400), .9)
    a = p.get('pan0', -.7); b = p.get('pan1', .7)
    q = np.linspace(a, b, n)
    return np.stack([x * np.cos((q + 1) * np.pi / 4), x * np.sin((q + 1) * np.pi / 4)], 1), d * pk


@S('whoom', -20, {'hall': .3}, 'push through, bloom, dive, surge, rises')
def _(p, r):
    """Low swelling rush that arrives on the instant."""
    d = dur(p, 1.0); n = ns(d + .8)
    e = env([(0, 0), (d * .6, .25), (d, 1), (d + .15, .5), (d + .8, 0)], n) ** 1.6
    f = 70 + 900 * env([(0, 0), (d, 1), (d + .8, .15)], n) ** 2
    return st(lambda q: sweep(white(n, q), f, .8, 'low') * e, r), d


@S('cloth', -34, {'theatre': .3}, 'cloth, tail settles, robe, sash, garland, curtain, banner')
def _(p, r):
    n = ns(dur(p, .6)); x = white(n, r)
    g = np.clip(wander(n, 9, r), 0, 3) * np.sin(np.pi * np.arange(n) / n)
    return bp(x, 500, 4200, 1) * g


# ---- fire ---------------------------------------------------------------------------------------------------------------


def crackle(n, r, rate=9, lo=1200, hi=6500, size=1.):
    y = np.zeros(n)
    for t in np.cumsum(r.exponential(1 / rate, int(n / SR * rate * 1.6) + 3)):
        i = ns(t); m = ns(.012 + .03 * r.random() * size)
        if i + m >= n: continue
        f = np.exp(r.uniform(np.log(lo), np.log(hi)))
        k = modal(np.array([f, f * 1.7]), np.array([1., .5]), np.array([.0015, .001]) * (1 + 2 * size * r.random()), np.zeros(2), m, np.ones(1))
        y[i:i + m] += k * r.pareto(2.2) * .25 * (1 if r.random() > .1 else 2.5)
        if size > 1 and r.random() < .25:
            m2 = min(ns(.12), n - i); y[i:i + m2] += bp(r.standard_normal(m2 + 64), 250, 1400)[64:] * np.exp(-np.arange(m2) / SR / .018) * r.random() * 1.2
    return np.tanh(y)


def fire(n, r, size=1.):
    """size .2 a lamp, 1 a hearth, 3 a burning hall, 6 a city."""
    x = white(n, r)
    flut = np.clip(1 + .45 * wander(n, 7 / size ** .4, r, 3), .1, 2.5)
    roar = lp(x, 160 + 60 * size, 2) * 2.2 * min(size, 4) ** .7 * flut
    hiss = bp(x, 900, 3500, 1) * .05 * flut * min(1, .5 + size / 3)
    c = crackle(n, r, 4 + 7 * size ** .6, 1000 / size ** .25, 6000, size) * (.35 + .25 / max(size, .5))
    return .35 * roar + hiss + c * .9


@S('lamp', -40, {'close': .3}, 'lamp burns, lamp bed')
def _(p, r):
    n = ns(dur(p, 3)); return swell(n, .3, .4)[:, None] * st(lambda q: fire(n, q, .2), r)


@S('fire', -26, {'open': .2}, 'fire, burning, blaze, burns')
def _(p, r):
    n = ns(dur(p, 3)); s = p.get('size', 1.); return swell(n, p.get('a', .2), p.get('b', .5))[:, None] * st(lambda q: fire(n, q, s), r)


@S('far_fire', -31, {'hall': .8, 'open': .5}, 'distant fire, far fire')
def _(p, r):
    n = ns(dur(p, 3)); return lp(swell(n, .4, .8)[:, None] * st(lambda q: fire(n, q, 5.), r), 900, 2)


@S('embers', -34, {'hall': .4}, 'embers, ember, crackle, title')
def _(p, r):
    n = ns(dur(p, 1.6)); return swell(n, .05, .7)[:, None] * st(lambda q: crackle(n, q, 11, 1500, 5500, .7) + .02 * bp(white(n, q), 1500, 5000), r)


@S('spark', -28, {'theatre': .5}, 'spark, glint, wakes')
def _(p, r):
    n = ns(.5); y = np.zeros(n)
    for k in range(9):
        i = ns(.0 if k == 0 else r.exponential(.05)); m = ns(.02)
        if i + m < n: y[i:i + m] += modal(np.array([r.uniform(3000, 8500)]), np.array([1. if k == 0 else r.uniform(.1, .5)]), np.array([.0022]), np.zeros(1), m, np.ones(1))
    m = ns(.12); y[:m] += bp(white(m, r), 2500, 8000) * np.exp(-T(m) / .02) * .25
    return y


@S('flame_up', -26, {'theatre': .4}, 'flame stands, flame up, catches, ignites, lights, kindle, takes fire, torch')
def _(p, r):
    s = p.get('size', .6); n = ns(.9 + .3 * s); t = T(n)
    f = (180 + 900 * np.exp(-t / .12)) * (1 / s ** .2)
    y = sweep(white(n, r), f, .8, 'low') * np.minimum(1, t / .012) * np.exp(-t / (.16 + .12 * s))
    y2 = fire(n, r, s) * .5 * np.minimum(1, t / .05) * np.exp(-t / .5)
    return np.stack([y + y2, y + np.roll(y2, 300)], 1)


@S('fire_run', -23, {'open': .3}, 'runs round, line of fire, fire runs, flame gathers, flames stream')
def _(p, r):
    d = dur(p, 1.2); n = ns(d + .3); u = np.linspace(0, 1, n)
    y = whoosh(n, r, .7, 300, 1500, .7, 1.2) * 1.2 + fire(n, r, 1.5) * np.sin(np.pi * u) ** .5
    q = np.sin(2 * np.pi * u * 1.1 - 1.4) * .85
    return np.stack([y * np.cos((q + 1) * np.pi / 4), y * np.sin((q + 1) * np.pi / 4)], 1)


@S('puff', -31, {'hall': .5}, 'goes out, go out, light out, flame out, lamp out, puff, snuffed, extinguished, line out')
def _(p, r):
    n = ns(.6); t = T(n); x = white(n, r)
    f = 900 * np.exp(-t / .07) + 120
    y = sweep(x, f, .8, 'low') * np.minimum(1, t / .004) * np.exp(-t / .06) * 2 + bp(x, 2500, 6000) * .10 * np.minimum(1, t / .05) * np.exp(-t / .15)
    return y


@S('ash_hiss', -38, {'open': .3}, 'ash, smoke, hiss, steam')
def _(p, r):
    n = ns(dur(p, 2)); return swell(n, .1, .6) * bp(white(n, r), 2200, 7000, 1) * np.clip(.5 + .5 * wander(n, 5, r), 0, 2)


@S('gold', -27, {'hall': .6}, 'gold, shimmer, gold dust, glitter, gold leaf, glow, glows, jewel')
def _(p, r):
    d = dur(p, 1.4); n = ns(d + .6); y = np.zeros((n, 2))
    for k in range(int(38 * d)):
        i = ns(min(abs(r.normal(0, d * .4)), d)); f = np.exp(r.uniform(np.log(2200), np.log(6800))); m = ns(.35)
        if i + m >= n: continue
        y[i:i + m] += pan(modal(np.array([f, f * 1.503]), np.array([1., .3]) * r.uniform(.1, 1), np.array([.09, .05]), np.zeros(2), m, np.ones(1)), r.uniform(-.9, .9))
    return lp(y, 8000, 1) * .5


# ---- water -----------------------------------------------------------------------------------------------------------------


def bubbles(n, r, rate=20, lo=400, hi=2400, rise=.25):
    """Minnaert bubbles: each a sine that rises as it nears the surface."""
    y = np.zeros(n)
    for t in np.cumsum(r.exponential(1 / rate, int(n / SR * rate * 1.5) + 3)):
        i = ns(t); f = np.exp(r.uniform(np.log(lo), np.log(hi))); tau = .012 + 18 / f * .6; m = ns(tau * 5)
        if i + m >= n: continue
        u = T(m); y[i:i + m] += np.sin(2 * np.pi * f * (u + rise * u * u / (2 * tau * 3))) * np.exp(-u / tau) * np.minimum(1, u / .001) * r.uniform(.1, 1) * (500 / f) ** .4
    return y


@S('river', -34, {'open': .2}, 'river, stream, water')
def _(p, r):
    n = ns(dur(p, 3)); return swell(n, .6, .8)[:, None] * st(lambda q: bubbles(n, q, 70, 500, 3200) * .35 + bp(white(n, q), 500, 3500, 1) * .12 * (1 + .3 * wander(n, 2, q)), r)


@S('waves', -28, {'open': .3}, 'waves, sea, surf, ocean, shore')
def _(p, r):
    n = ns(dur(p, 4)); t = T(n)
    def w(q):
        ph = q.uniform(0, 6); e = np.clip(.45 + .55 * np.sin(2 * np.pi * t / p.get('period', 2.6) + ph), 0, 1) ** 1.6
        return sweep(white(n, q), 250 + 2200 * e, .7, 'low') * (.2 + e) + .1 * bubbles(n, q, 40, 600, 3000)
    return swell(n, .4, .7)[:, None] * st(w, r)


@S('splash', -21, {'open': .4}, 'splash, spray, breaks the surface, breaks surface, hits water, hits the water, into the water, dropped, surfaces, plunge')
def _(p, r):
    s = p.get('size', 1.); n = ns(1.1 + .5 * s); t = T(n)
    f = 500 + 4200 * np.exp(-t / .09)
    def w(q):
        y = sweep(white(n, q), f, .7, 'low') * np.minimum(1, t / .002) * (np.exp(-t / .07) + .35 * np.exp(-t / (.3 * s)))
        y += .5 * bubbles(n, q, 60, 300, 2000) * np.exp(-t / .35) + bp(white(n, q), 2500, 7000) * .12 * np.exp(-np.maximum(t - .1, 0) / .3) * np.minimum(1, t / .15)
        return y
    z = modal(np.array([70., 110.]), np.array([1., .6]) * s, np.array([.09, .05]), np.zeros(2), n, 1 + .8 * np.exp(-t / .03))
    return st(w, r) + z[:, None] * .6


@S('underwater', -29, {'cave': .4}, 'under water, underwater, sinks, green water')
def _(p, r):
    n = ns(dur(p, 1.6)); e = swell(n, .05, .12)
    def w(q): return lp(white(n, q), 220, 2) * 2.2 * (1 + .3 * wander(n, 1.5, q)) + lp(bubbles(n, q, 16, 180, 900), 1200) * .8
    return e[:, None] * st(w, r)


@S('drop', -30, {'cave': .7, 'hall': .3}, 'drop, drip')
def _(p, r):
    n = ns(.5); t = T(n); f = p.get('f', 1050)
    y = np.sin(2 * np.pi * f * (t + 1.1 * t * t)) * np.exp(-t / .045) * np.minimum(1, t / .0012)
    i = ns(.055); u = t[:n - i]; y[i:] += .5 * np.sin(2 * np.pi * f * 1.45 * (u + 2.2 * u * u)) * np.exp(-u / .03)
    m = ns(.01); y[:m] += .3 * bp(white(m, r), 2000, 7000) * np.exp(-T(m) / .002)
    return y


def rainbed(n, r, dens=1., hard=0.):
    x = white(n, r)
    y = bp(x, 900, 7000, 1) * .10 * dens * (1 + .15 * wander(n, 1, r)) + lp(x, 400, 1) * .05 * dens
    for t in np.cumsum(r.exponential(1 / (45 * dens), int(n / SR * 45 * dens * 1.4) + 3)):
        i = ns(t); m = ns(.03)
        if i + m >= n: continue
        f = np.exp(r.uniform(np.log(900), np.log(5200)))
        y[i:i + m] += modal(np.array([f]), np.array([r.pareto(2.5) * .06]), np.array([.0025 + .006 * r.random()]), np.zeros(1), m, np.ones(1))
    return y


@S('rain', -30, {'open': .25}, 'rain, monsoon, rainy')
def _(p, r):
    n = ns(dur(p, 3)); return swell(n, p.get('a', .4), p.get('b', .6))[:, None] * lp(st(lambda q: rainbed(n, q, p.get('dens', 1.)), r), 7500, 1)


@S('thunder', -22, {'open': .6, 'hall': .4}, 'thunder')
def _(p, r):
    n = ns(3.2); t = T(n); near = p.get('near', .4)
    y = lp(white(n, r), 90 + 120 * near, 2) * 3 * np.exp(-t / .9) * np.clip(.6 + .7 * wander(n, 5, r, 3), 0, 3)
    y += near * sweep(white(n, r), 300 + 3500 * np.exp(-t / .05), .7, 'low') * np.exp(-t / .12) * 1.4
    return np.tanh(y * .8) * np.minimum(1, t / .003)


# ---- things struck, snapped, worn ----------------------------------------------------------------------------------------


@S('clack', -27, {'theatre': .6}, 'clack, puppet, rod, wooden, prince')
def _(p, r): return perc.wood(p.get('f', 620 + 260 * r.random()), 1., int(r.integers(5)), .022) + 0


@S('creak', -27, {'theatre': .4}, 'creak, creaks, bow drawn, draw, draws, drawn, bowstring, string creak, string creaks, lifts, weight')
def _(p, r):
    """Stick-slip: a train of small releases whose rate climbs with tension."""
    d = dur(p, 1.); n = ns(d); u = np.arange(n) / n
    rate = p.get('r0', 14) * (p.get('r1', 70) / p.get('r0', 14)) ** u * (1 + .3 * wander(n, 6, r))
    ph = np.cumsum(np.maximum(rate, 2)) / SR
    k = np.where(np.diff(np.floor(ph)) > 0)[0]
    x = np.zeros(n); x[k] = r.uniform(.3, 1, len(k)); x = lp(signal.lfilter([1], [1, -.93], x), 2600, 2)
    b = p.get('f', 420)
    f = np.array([1., 1.63, 2.41, 3.8, 5.3]) * b; y = np.zeros(n)
    for ff, a in zip(f, (1, .8, .7, .4, .25)): y += a * sweep(x, ff * (1 + .25 * u), 22.)
    y += .25 * bp(x, 1200, 4000)
    y = np.tanh(y / (1.8 * np.sqrt((y ** 2).mean()) + 1e-9))
    e = (.25 + .75 * u ** 1.4) * np.minimum(1, u * n / ns(.05)) * np.minimum(1, (n - np.arange(n)) / ns(.012))
    return y * e


@S('bow_break', -10.5, {'hall': .5, 'cathedral': .35}, 'bow breaks, bow break, bow snaps, it breaks')
def _(p, r):
    """Shiva's bow: the crack, the two limbs, the earth under it."""
    n = ns(4.5); t = T(n)
    cr = bp(white(n, r), 700, 6500, 1) * (np.exp(-t / .006) * 1.8 + .8 * np.exp(-np.abs(t - .021) / .007) + .6 * np.exp(-np.abs(t - .047) / .01))
    sp = np.zeros(n)
    for k in range(60):
        i = ns(abs(r.normal(0, .09))); m = ns(.05); f = np.exp(r.uniform(np.log(500), np.log(4200)))
        sp[i:i + m] += modal(np.array([f, f * 2.3]), np.array([1., .5]) * r.random(), np.array([.006, .003]), np.zeros(2), m, np.ones(1))
    wd = modal(np.array([88., 141., 233., 317., 480., 690., 960.]), np.array([1.2, 1.2, 1., .9, .7, .6, .4]), np.array([.25, .2, .14, .1, .07, .05, .04]), np.zeros(7), n, 1 + .25 * np.exp(-t / .05))
    bm = modal(np.array([33., 47., 61.]), np.array([2.2, 1.6, 1.]), np.array([.7, .5, .35]), np.zeros(3), n, 1 + .9 * np.exp(-t / .07))
    tw = modal(np.array([110., 221., 333., 446., 560.]), np.array([.8, .6, .5, .4, .3]), np.full(5, .5), np.zeros(5), n, 1 + .06 * np.sin(2 * np.pi * 17 * t) * np.exp(-t / .3))
    rb = lp(white(n, r), 180, 2) * 2.4 * np.exp(-t / .55) * np.clip(.8 + .5 * wander(n, 8, r), 0, 3)
    y = np.tanh(1.6 * cr + .5 * sp + .7 * wd + bm + .22 * tw + .5 * rb)
    z = wide(y, r, .35); z[:ns(.004)] = y[:ns(.004), None]
    return fades(z, .0001, .8)


@S('crack', -20, {'open': .5}, 'cracks, crack, rock cracks, rocks roll, rubble')
def _(p, r):
    n = ns(.9); t = T(n); s = p.get('size', 1.)
    y = bp(white(n, r), 500, 4500, 1) * np.exp(-t / .008)
    for k in range(int(10 * s)):
        i = ns(abs(r.normal(0, .12))); m = ns(.12); z = perc.stone(r.uniform(180, 600), 1., k)[:m]; y[i:i + len(z)] += z * r.uniform(.2, .8)
    y += modal(np.array([62., 97.]), np.array([1., .6]) * s, np.array([.15, .1]), np.zeros(2), n, 1 + .5 * np.exp(-t / .03))
    return np.tanh(y)


@S('petals', -34, {'hall': .4}, 'petals, flowers, blossom')
def _(p, r):
    d = dur(p, 1.5); n = ns(d); u = np.arange(n) / n
    y = np.zeros((n, 2))
    for k in range(int(40 * d)):
        i = int(r.uniform(0, .9) * n); m = min(ns(.06), n - i)
        y[i:i + m] += pan(bp(r.standard_normal(m + 64), 1500, 5500)[64:] * np.hanning(m) * r.random(), r.uniform(-1, 1))
    return y * (np.exp(-u * 2.2))[:, None]


@S('crown', -24, {'stone': .8}, 'crown, thunk, metal, set down')
def _(p, r):
    n = ns(1.6); t = T(n)
    y = modal(np.array([418., 655., 1130., 1722., 2410., 3180.]), np.array([.7, .8, .6, .45, .3, .15]), np.array([.35, .28, .2, .14, .1, .07]), r.uniform(0, 1, 6), n, np.ones(1))
    th = modal(np.array([92., 150., 236.]), np.array([1.6, .9, .5]), np.array([.07, .05, .03]), np.zeros(3), n, 1 + .4 * np.exp(-t / .015))
    i = ns(.085); y[i:] += .35 * y[:-i].copy(); i = ns(.135); y[i:] += .15 * y[:-i].copy()
    return y * .55 + th + bp(white(n, r), 600, 3500) * np.exp(-t / .006) * .6


@S('foot', -33, {'stone': .5}, 'footstep, bare foot, bare foot on stone, bare foot on earth, foot, feet, steps, step, walk')
def _(p, r):
    n = ns(.3); t = T(n); k = p.get('on', 'stone')
    th = modal(np.array([85., 130., 210.]), np.array([1., .6, .3]), np.array([.03, .025, .015]), np.zeros(3), n, 1 + .4 * np.exp(-t / .01))
    if k == 'leaves': x = bp(white(n, r), 1200, 6000) * np.clip(wander(n, 40, r), 0, 3) * np.exp(-t / .07) * .8
    elif k == 'wet': x = bp(white(n, r), 400, 2500) * np.exp(-t / .04) + .5 * bubbles(n, r, 40, 500, 1800) * np.exp(-t / .1)
    else: x = bp(white(n, r), 500, 2600) * (np.exp(-t / .012) + .25 * np.exp(-np.abs(t - .07) / .012))
    return th * .8 + x * .6


@S('steps', -33, {'open': .3}, 'running, footsteps, runs')
def _(p, r):
    """A run or walk: every = frames between steps, n = frames long."""
    n = ns(dur(p, 2.)); y = np.zeros((n + ns(.4), 2)); f = 0.; k = 0
    while f < dur(p, 2.) * 24 - 1:
        x = REG['foot']['fn'](p, r) * r.uniform(.7, 1.); i = ns(sec(f) + abs(r.normal(0, .006)))
        y[i:i + len(x)] += pan(x, p.get('pan', 0) + .12 * (-1) ** k); f += p.get('every', 6); k += 1
    return y


@S('march', -26, {'open': .5}, 'march, marching, army, host, armies')
def _(p, r):
    n = ns(dur(p, 4.)); y = np.zeros((n, 2)); t = 0.
    while t < n / SR - .3:
        for k in range(14):
            i = ns(t + abs(r.normal(0, .022))); m = ns(.16)
            x = (lp(r.standard_normal(m), 420, 2) * 2 + .12 * r.standard_normal(m)) * np.exp(-T(m) / .03)
            if i + m < n: y[i:i + m] += pan(x, r.uniform(-1, 1)) * r.uniform(.3, 1)
        t += .25 * p.get('every', 6) / 6
    return lp(y, 3500, 1) * swell(n, .4, .4)[:, None]


@S('crowd', -32, {'open': .4, 'hall': .3}, 'crowd, murmur, people, kings, court, cheer, cheers')
def _(p, r):
    """A murmuring crowd: many unsteady formant voices, no words."""
    n = ns(dur(p, 3)); y = np.zeros((n, 2)); t = T(n)
    for k in range(int(p.get('voices', 26))):
        f0 = r.choice([r.uniform(95, 150), r.uniform(180, 260)]) * p.get('pitch', 1.)
        f = f0 * 2 ** (.16 * wander(n, 2.2, r) + p.get('excite', 0.) * .3 * np.sin(np.pi * np.linspace(0, 1, n)))
        src = signal.sawtooth(2 * np.pi * np.cumsum(f) / SR) * np.clip(wander(n, 3.2, r) + .1, 0, 2) * np.clip(wander(n, .6, r) + .7, 0, 2) + .04 * r.standard_normal(n)
        z = sweep(src, 480 * 2 ** (.35 * wander(n, 3, r)), 5.) + .6 * sweep(src, 1350 * 2 ** (.3 * wander(n, 3, r)), 7.) + .25 * sweep(src, np.full(n, 2600.), 6.)
        y += pan(z, r.uniform(-1, 1)) * r.uniform(.4, 1)
    return lp(y, 3500, 1) * swell(n, p.get('a', .5), p.get('b', .6))[:, None]


@S('gate', -22, {'stone': .6}, 'gate, door, hinge')
def _(p, r):
    n = ns(2.); y = REG['creak']['fn'](dict(dur=1.6, f=140, r0=10, r1=34), r); z = np.zeros(n); z[:len(y)] = y * .5
    z += lp(white(n, r), 110, 2) * 2 * swell(n, .3, .6); return z


@S('temple_bell', -27, {'hall': .7}, 'temple bell, bells, sunrise bell, bell')
def _(p, r): return inst.bell(p.get('f', 659.), 3.5, 4., .4, 3)


@S('ring', -27, {'hall': .7}, 'ring, ornament, anklet, bangles, bangle, jewel on palm')
def _(p, r):
    n = ns(1.8); f = p.get('f', 2349.3)
    return modal(f * np.array([1., 1.003, 1.51, 2.32, 2.76]), np.array([.7, .6, .35, .25, .12]), np.array([.35, .4, .2, .12, .08]), np.zeros(5), n, np.ones(1)) * .5


@S('ring_skin', -30, {'hall': .6}, 'ring drops, into her palm, palm, ring falls')
def _(p, r):
    n = ns(1.6); t = T(n); y = REG['ring']['fn'](dict(f=1975.5), r)[:n] * .6
    return y + modal(np.array([150., 230.]), np.array([.5, .3]), np.array([.02, .015]), np.zeros(2), n, np.ones(1))


# ---- arrows, blades, blows ------------------------------------------------------------------------------------------------------


@S('loose', -22, {'open': .3}, 'release, looses, loose, shoots, shot, arrow flies')
def _(p, r):
    n = ns(.9); t = T(n); s = p.get('size', 1.)
    f = p.get('f', 128.)
    tw = modal(f * np.array([1, 2.01, 3.03, 4.06, 5.1, 6.2]), np.array([1., .8, .6, .4, .25, .15]), np.array([.16, .12, .09, .07, .05, .04]), np.zeros(6), n, 1 + .12 * np.exp(-t / .03))
    sn = bp(white(n, r), 900, 5200) * np.exp(-t / .006)
    wh = sweep(white(n, r), 3200 * np.exp(-t / .35) + 500, 1.4) * np.minimum(1, t / .015) * np.exp(-t / .16)
    return tw * .7 + sn * .8 + wh * .8 * s


@S('arrow_fly', -26, {'open': .3}, 'arrow of light, arrow, flight of the arrow')
def _(p, r):
    d = dur(p, .6); n = ns(d); u = np.arange(n) / n
    x = sweep(white(n, r), 2600 * (1 - .5 * u), 5.) * np.sin(np.pi * u ** .5) + .4 * whoosh(n, r, .4, 500, 3200)
    q = np.linspace(-.8, .8, n) * p.get('dir', 1); return np.stack([x * np.cos((q + 1) * np.pi / 4), x * np.sin((q + 1) * np.pi / 4)], 1)


@S('hit', -19, {'open': .4}, 'hit, struck, strikes, strike, blow, impact, lands, landing')
def _(p, r):
    s = p.get('size', 1.); n = ns(1.2); t = T(n)
    y = bp(white(n, r), 400, 3800, 1) * np.exp(-t / .012) * 1.2 + modal(np.array([58., 96., 171., 290.]) / s ** .4, np.array([1.6, 1.1, .6, .4]), np.array([.2, .13, .07, .04]) * s ** .5, np.zeros(4), n, 1 + .6 * np.exp(-t / .03))
    return np.tanh(y + lp(white(n, r), 500) * np.exp(-t / .1) * .8)


@S('steel', -22, {'open': .4}, 'sword, blade, steel, clash of steel, talons, blade takes')
def _(p, r):
    n = ns(1.1); f = p.get('f', r.uniform(700, 1100)); K = 12
    ff = f * np.cumsum(r.uniform(.5, 1.1, K)) * .9 + f * .2
    y = modal(ff, np.exp(-np.arange(K) * .16) * r.uniform(.4, 1, K), .16 / (1 + ff / 2500) + .02, r.uniform(0, 6, K), n, np.ones(1))
    return lp(y + bp(white(n, r), 2000, 6500) * np.exp(-T(n) / .008) * 1.5, 7000, 1) * .5


@S('clash', -13, {'open': .5, 'hall': .3}, 'clash, collide, collision, hosts meet, armies meet')
def _(p, r):
    n = ns(2.6); t = T(n); y = np.zeros((n, 2))
    b = REG['hit']['fn'](dict(size=2.5), r); y[:len(b)] += 1.6 * b[:, None]
    for k in range(34):
        i = 0 if k < 3 else ns(r.exponential(.28)); x = REG['steel']['fn']({}, r) * r.uniform(.15, .6) if k % 2 else perc.wood(r.uniform(250, 700), 1., k % 5) * 1.5
        m = min(len(x), n - i)
        if m > 0: y[i:i + m] += pan(x[:m], r.uniform(-1, 1))
    y += st(lambda q: lp(white(n, q), 260, 2) * 2.2 * np.exp(-t / .6), r)
    return np.tanh(y)


@S('arrow_storm', -22, {'open': .4}, 'storm of arrows, arrows, volley')
def _(p, r):
    n = ns(dur(p, 2.5)); y = np.zeros((n, 2))
    for k in range(int(26 * n / SR)):
        d = r.uniform(.2, .5); m = ns(d); i = int(r.uniform(0, n - m)); u = np.arange(m) / m
        x = sweep(white(m, r), r.uniform(1400, 3400) * (1.2 - .5 * u), 6.) * np.sin(np.pi * u); q = np.linspace(-1, 1, m) * r.choice([-1, 1]) * r.uniform(.3, 1)
        y[i:i + m] += np.stack([x * np.cos((q + 1) * np.pi / 4), x * np.sin((q + 1) * np.pi / 4)], 1) * r.uniform(.2, 1)
    return y * swell(n, .3, .3)[:, None]


@S('rope', -22, {'stone': .5}, 'rope, ropes, bonds, ropes burst')
def _(p, r):
    n = ns(1.); y = np.zeros(n)
    for d in (0., .012, .03, .041, .07):
        i = ns(d); m = n - i; u = T(m)
        y[i:] += (bp(white(m, r), 700, 4500, 1) * np.exp(-u / .010) + modal(np.array([r.uniform(120, 240), r.uniform(300, 500)]), np.array([1., .6]), np.array([.05, .03]), np.zeros(2), m, 1 + .3 * np.exp(-u / .03))) * r.uniform(.5, 1)
    return np.tanh(y)


# ---- earth, wings, giants, storms ---------------------------------------------------------------------------------------------------


@S('earth_tear', -14, {'open': .5, 'hall': .3}, 'earth tears, earth tearing, earth torn, earth rips, rips loose')
def _(p, r):
    d = dur(p, 1.8); n = ns(d + 1); t = T(n); e = np.minimum(1, t / .004) * np.clip((d + 1 - t) / 1.2, 0, 1)
    def w(q):
        y = lp(white(n, q), 130, 2) * 3.4 * np.clip(.7 + .6 * wander(n, 9, q, 3), 0, 3) + bp(white(n, q), 250, 1500, 1) * np.clip(wander(n, 16, q, 2) - .2, 0, 3) * .9
        for k in range(24):
            i = int(q.uniform(0, .75) ** 1.5 * n); z = perc.stone(q.uniform(90, 380), 1., k % 6, 1.); m = min(len(z), n - i); y[i:i + m] += z[:m] * q.uniform(.3, 1.4)
        return np.tanh(y + bp(white(n, q), 300, 3500, 1) * np.exp(-t / .03) * 2)
    b = modal(np.array([36., 54., 79.]), np.array([2., 1.4, .8]), np.array([.5, .35, .2]), np.zeros(3), n, 1 + .5 * np.exp(-t / .08))
    return (st(w, r) + b[:, None] * .7) * e[:, None]


@S('rumble', -25, {'hall': .3}, 'rumble, tremble, quake, chariot wheels, flying chariot')
def _(p, r):
    n = ns(dur(p, 3)); return swell(n, p.get('a', .4), .6)[:, None] * st(lambda q: lp(white(n, q), p.get('f', 95), 2) * np.clip(.8 + .4 * wander(n, 6, q), 0, 3), r)


@S('wings', -20, {'open': .4}, 'wing, wings, flap, vulture, wingbeat')
def _(p, r):
    """Huge wings: beats every `every` frames."""
    d = dur(p, 1.5); n = ns(d + .5); y = np.zeros((n, 2)); f = 0.
    while f < d * 24:
        m = ns(.42); x = whoosh(m, r, .28, 70, 750, .7, 1.5) * 2 + bp(white(m, r), 900, 3000, 1) * np.hanning(m) ** 2 * .18; i = ns(sec(f)); k = min(m, n - i)
        if k > 0: y[i:i + k] += wide(x, r, .6)[:k]
        f += p.get('every', 9)
    return y


@S('feathers', -32, {'open': .4}, 'feather, feathers')
def _(p, r):
    n = ns(dur(p, 1.5)); return np.stack([bp(white(n, r), 900, 4200, 1) * np.clip(wander(n, 12, r), 0, 3) for _ in (0, 1)], 1) * (np.linspace(1, 0, n) ** 1.5 * np.minimum(1, T(n) / .02))[:, None]


@S('giant_grow', -24, {'cave': .4, 'open': .3}, 'grows, growing, stands up, swells, unfolds')
def _(p, r):
    d = dur(p, 3); n = ns(d); u = np.arange(n) / n
    y = REG['creak']['fn'](dict(dur=d, f=95, r0=7, r1=16), r) * .6 + sweep(white(n, r), 45 + 70 * u, 2.5) * 2.5 * (.2 + u)
    return y * swell(n, .3, .3)


@S('footfall', -14, {'open': .6, 'hall': .3}, 'footfall, giant step, giant foot, stamp')
def _(p, r):
    n = ns(2.4); t = T(n)
    y = modal(np.array([29., 41., 58., 83., 130.]), np.array([2.4, 1.8, 1.2, .8, .5]), np.array([.5, .35, .22, .14, .08]), np.zeros(5), n, 1 + .8 * np.exp(-t / .05))
    y += lp(white(n, r), 170, 2) * 3 * np.exp(-t / .35) + bp(white(n, r), 250, 2400, 1) * np.exp(-t / .025) * 1.1
    for k in range(14):
        i = ns(.05 + r.exponential(.2)); z = perc.stone(r.uniform(200, 600), 1., k % 6)
        if i + len(z) < n: y[i:i + len(z)] += z * r.uniform(.1, .5)
    return np.tanh(y * .9)


@S('giant_fall', -11.5, {'open': .5, 'cathedral': .3}, 'falls like a mountain, giant falls, crash, collapse, topples')
def _(p, r):
    n = ns(4.); t = T(n); y = np.zeros(n)
    for d, g in ((0, 1.), (.11, .6), (.27, .45), (.5, .3)):
        x = REG['footfall']['fn'](p, r) * g; i = ns(d); m = min(len(x), n - i); y[i:i + m] += x[:m]
    y += lp(white(n, r), 300, 2) * 2. * np.exp(-t / .8) * np.clip(.7 + .6 * wander(n, 10, r, 2), 0, 3)
    return np.tanh(wide(y, r, .4))


@S('roar', -17, {'cave': .4, 'open': .4}, 'roar, serpent, demon, growl, bellow')
def _(p, r):
    """A throat the size of a harbour: rough low source, two sliding formants."""
    d = dur(p, 1.6); n = ns(d); t = T(n); u = t / d; b = p.get('f', 62.)
    f = b * (1 + .5 * np.sin(np.pi * u ** .6)) * (1 + .04 * wander(n, 24, r))
    ph = 2 * np.pi * np.cumsum(f) / SR
    src = signal.sawtooth(ph) + .8 * signal.sawtooth(ph * .5 + .7) * (1 + .5 * np.sin(ph * .25)) + .5 * white(n, r) * np.clip(.6 + wander(n, 40, r), 0, 2)
    o = np.sin(np.pi * u ** .7)
    y = sweep(src, 180 + 420 * o, 3.) + .8 * sweep(src, 620 + 900 * o, 4.) + .4 * sweep(src, 2000 + 500 * o, 4.)
    return np.tanh(wide(y, r, .5) * 1.4) * (np.minimum(1, t / .06) * np.clip((d - t) / .5, 0, 1) ** .8)[:, None]


@S('leap_blast', -11, {'open': .6, 'cathedral': .25}, 'leap, the leap, blast, peak bursts, explodes, explosion')
def _(p, r):
    n = ns(4.); t = T(n)
    y = np.zeros(n)
    x = REG['footfall']['fn'](p, r); y[:len(x)] += 1.3 * x
    y += bp(white(n, r), 300, 5000, 1) * (np.exp(-t / .02) * 1.5 + .35 * np.exp(-t / .35)) + lp(white(n, r), 130, 2) * 3 * np.exp(-t / .9)
    for k in range(40):
        i = ns(r.exponential(.35)); z = perc.stone(r.uniform(90, 500), 1., k % 6, .6)
        if i + len(z) < n: y[i:i + len(z)] += z * r.uniform(.2, .9)
    wh = sweep(white(n, r), 500 + 2600 * np.exp(-t / .5), .8) * np.exp(-t / .6) * np.minimum(1, t / .05)
    return np.tanh(wide(y, r, .4) + .7 * wide(wh, r, .9))


@S('lightning', -12, {'open': .6, 'hall': .3}, 'lightning, bolt')
def _(p, r):
    n = ns(2.8); t = T(n)
    g = np.clip(.4 + wander(n, 30, r, 3), 0, 4)
    y = bp(white(n, r), 400, 7000, 1) * (np.exp(-t / .012) * 2.2 + .6 * np.exp(-t / .10) * g) + lp(white(n, r), 150, 2) * 3 * np.exp(-t / .5) * np.clip(.7 + .5 * wander(n, 7, r), 0, 3)
    z = signal.sawtooth(2 * np.pi * np.cumsum(900 * np.exp(-t / .07) + 70) / SR) * np.exp(-t / .12)
    return np.tanh(lp(wide(y, r, .5), 8000, 1) + .4 * lp(z, 3000)[:, None])


@S('heartbeat', -30, {}, 'heartbeat, heart')
def _(p, r):
    """every = frames per beat, n = frames."""
    d = dur(p, 2.); n = ns(d + .6); y = np.zeros(n); f = 0.
    m = ns(.3); u = T(m)
    k = lambda a, ff: a * np.sin(2 * np.pi * ff * (u - .25 * .02 * (1 - np.exp(-u / .02)))) * np.exp(-u / .06) * np.minimum(1, u / .004)
    while f < d * 24 - .5:
        i = ns(sec(f)); y[i:i + m] += k(1., 52) + .25 * k(1, 104)
        j = i + ns(p.get('gap', .26))
        if j + m < n: y[j:j + m] += k(.65, 60) + .15 * k(1, 120)
        f += p.get('every', 24)
    return y


@S('stone_drop', -22, {'open': .4}, 'stone, stones, pebble, rock')
def _(p, r):
    x = perc.stone(p.get('f', r.uniform(160, 300)), 1., int(r.integers(6)), p.get('big', 1.)) * 1.
    s = REG['splash']['fn'](dict(size=.5), r) * p.get('wet', .5); s[:len(x)] += x[:, None]; return s


@S('write', -36, {'close': .4}, 'writes, finger, finger on stone, scratch, scratches, draws a line')
def _(p, r):
    d = dur(p, 1.4); n = ns(d); e = np.clip(.4 + wander(n, 4, r), 0, 2) * swell(n, .05, .1)
    return (bp(white(n, r), 700, 3200, 1) * (1 + .5 * np.clip(wander(n, 60, r), -1, 3)) + .5 * lp(white(n, r), 300)) * e


@S('eye_open', -22, {'cave': .5}, 'eye opens, eyes open, giant eye, ravana eye')
def _(p, r):
    n = ns(.9); t = T(n); y = sweep(white(n, r), 110 + 600 * np.exp(-t / .09), .9, 'low') * np.minimum(1, t / .008) * np.exp(-t / .22) * 2 + fire(n, r, 1.2) * .5 * np.exp(-t / .35)
    return y


@S('chariot', -25, {'open': .3}, 'chariot, chariots, horses, hooves, wheels')
def _(p, r):
    n = ns(dur(p, 3)); y = np.zeros((n, 2))
    for who, (pn, off) in enumerate(((-.5, 0.), (.5, .07))):
        t = off
        while t < n / SR - .3:
            for d in (0, .085, .16):
                i = ns(t + d + r.normal(0, .004)); x = perc.wood(r.uniform(180, 300), 1., int(r.integers(5)), .02)
                if i >= 0 and i + len(x) < n: y[i:i + len(x)] += pan(x, pn) * r.uniform(.5, 1)
            t += .25
        y += pan(lp(white(n, r), 260, 2) * np.clip(.8 + .6 * wander(n, 11, r), 0, 3) * .7, pn)
    return y * swell(n, .3, .4)[:, None]


@S('tunnel', -13, {'hall': .4}, 'tunnel, enormous rush, flies through')
def _(p, r):
    """The arrow through every memory: a rush that rises until the strike."""
    d = dur(p, 3.); n = ns(d); u = np.arange(n) / n
    f = 300 + 2400 * u ** 1.6
    y = st(lambda q: sweep(white(n, q), f * (1 + .25 * wander(n, 5, q)), 1.1) * (.35 + .65 * u) + sweep(white(n, q), 120 + 200 * u, .8, 'low') * 1.6, r)
    ph = np.cumsum(5 + 9 * u) / SR
    return np.tanh(y * (.7 + .45 * np.cos(2 * np.pi * ph))[:, None]) * np.minimum(1, T(n) / .003)[:, None] * np.minimum(1, (n - np.arange(n)) / ns(.02))[:, None]


# ---- living places ---------------------------------------------------------------------------------------------------------------


def chirp(r, f, d, shape='up'):
    n = ns(d); u = np.arange(n) / n
    k = dict(up=1 + .25 * u, down=1.25 - .3 * u, arc=1 + .3 * np.sin(np.pi * u), trill=1 + .10 * np.sin(2 * np.pi * 26 * u * d))[shape]
    return np.sin(2 * np.pi * np.cumsum(f * k) / SR) * np.sin(np.pi * u) ** .8


@S('birds', -36, {'open': .6}, 'birds, dawn, peacock, koel, forest')
def _(p, r):
    n = ns(dur(p, 4)); y = np.zeros((n, 2)); D = n / SR
    for b in range(p.get('k', 5)):
        f = r.uniform(1700, 4300); pn = r.uniform(-.9, .9); sh = [['up', 'arc'], ['down', 'down'], ['trill', 'up'], ['arc', 'arc', 'down']][b % 4]; t = r.uniform(0, .5); g = r.uniform(.2, 1)
        while t < D - .6:
            for s in sh:
                x = chirp(r, f * r.uniform(.94, 1.06), r.uniform(.05, .16), s) * g; i = ns(t)
                if i + len(x) < n: y[i:i + len(x)] += pan(x, pn)
                t += r.uniform(.1, .2)
            t += r.exponential(.8) + .2
    return y * swell(n, p.get('a', .6), .6)[:, None]


@S('crickets', -38, {'open': .4}, 'crickets, night, insects')
def _(p, r):
    n = ns(dur(p, 3)); t = T(n); y = np.zeros((n, 2))
    for k in range(6):
        f = r.uniform(3600, 5200); rate = r.uniform(26, 38); ch = r.uniform(1.2, 2.4)
        g = np.clip(np.sin(2 * np.pi * rate * t), 0, 1) ** 2 * (np.sin(2 * np.pi * ch * t + r.uniform(0, 6)) > r.uniform(-.2, .4))
        y += pan(np.sin(2 * np.pi * f * t + .3 * wander(n, 2, r)) * smooth(g * 1., .003), r.uniform(-1, 1)) * r.uniform(.3, 1)
    return lp(y, 6500, 1) * swell(n, .5, .6)[:, None]


@S('night_city', -35, {'open': .5}, 'night city, city, lanka')
def _(p, r):
    n = ns(dur(p, 3)); y = REG['wind']['fn'](dict(n=n / 2000, lo=120, hi=380), r)[:n] * .6
    for k in range(5):
        i = int(r.uniform(.05, .8) * n); b = inst.bell(r.choice([392., 523., 659.]), 1.6, 1.6, .2, k) * .06; m = min(len(b), n - i); y[i:i + m] += pan(b[:m], r.uniform(-.8, .8))
    return y


@S('lamps', -30, {'hall': .6}, 'lamps, villages wake, lamp wakes, lamps wake, ten thousand')
def _(p, r):
    """Lamp after lamp: tiny tuned ticks of light, pentatonic, gathering."""
    d = dur(p, 3); n = ns(d + 1.); y = np.zeros((n, 2)); sc = np.array([1, 9/8, 5/4, 3/2, 5/3, 2, 9/4, 5/2, 3]) * 587.33
    for k in range(int(d * p.get('rate', 11))):
        i = ns(r.uniform(0, 1) ** p.get('curve', .6) * d); f = r.choice(sc) * r.choice([1, 2]); m = ns(.7)
        x = modal(f * np.array([1, 2.01, 3.9]), np.array([1., .25, .1]), np.array([.14, .07, .03]), np.zeros(3), m, np.ones(1)) * r.uniform(.2, .8) * (700 / f) ** .5
        if i + m < n: y[i:i + m] += pan(x, r.uniform(-1, 1))
    return y


@S('leaves', -34, {'open': .3}, 'leaves, dry leaves, autumn, trees')
def _(p, r):
    n = ns(dur(p, 1.2)); y = np.zeros((n, 2))
    for k in range(int(70 * n / SR)):
        m = ns(r.uniform(.01, .05)); i = int(r.uniform(0, max(1, n - m)))
        y[i:i + m] += pan(bp(r.standard_normal(m + 64), 1800, 6500)[64:] * np.exp(-T(m) / .01) * r.pareto(2) * .5, r.uniform(-1, 1))[:n - i]
    return np.tanh(y) * swell(n, .15, .25)[:, None]


@S('hoof', -33, {'open': .4}, 'hoof, hooves')
def _(p, r):
    """k light hooves, a frame and a half apart."""
    n = ns(.5 + .0625 * p.get('k', 1)); y = np.zeros(n)
    for k in range(p.get('k', 1)):
        x = perc.wood(r.uniform(260, 340), 1., int(r.integers(5)), .018); i = ns(.0625 * k); y[i:i + len(x)] += x * r.uniform(.7, 1)
        m = ns(.09); y[i:i + m] += bp(white(m, r), 900, 4200) * np.exp(-T(m) / .03) * .25
    return y


@S('bird_cry', -27, {'cave': .5, 'open': .6}, 'bird cry, old bird')
def _(p, r):
    """An old vulture, far off: a rasp that climbs, breaks and falls."""
    n = ns(1.3); t = T(n); u = t / 1.3
    f = (620 + 420 * np.sin(np.pi * np.minimum(1, u * 1.5)) - 260 * u) * (1 + .03 * wander(n, 30, r))
    src = signal.sawtooth(2 * np.pi * np.cumsum(f) / SR) * (1 + .7 * np.sin(2 * np.pi * 58 * t)) + .35 * white(n, r)
    return lp(sweep(src, f * 1.6, 3.) + .6 * sweep(src, f * 3.1, 4.), 5200, 1) * np.minimum(1, t / .05) * (1 - u) ** .7


@S('shatter', -20, {'hall': .4, 'open': .3}, 'shatter, lattice, window breaks')
def _(p, r):
    """A carved screen going to pieces: one blow, then wood and small metal raining down."""
    n = ns(1.5); y = np.zeros((n, 2)); b = REG['hit']['fn'](dict(size=.7), r)[:n]; y[:len(b)] += .8 * b[:, None]
    for k in range(46):
        x = perc.wood(r.uniform(500, 1700), 1., k % 5, .02) if k % 3 else REG['ring']['fn'](dict(f=r.uniform(2000, 4200)), r)[:ns(.3)] * .5
        i = ns(min(1.1, r.exponential(.22))); x = x[:n - i]; y[i:i + len(x)] += pan(x, r.uniform(-.9, .9)) * r.uniform(.15, .7)
    return y


@S('squirrel', -34, {'open': .4}, 'squirrel')
def _(p, r):
    y = np.zeros(ns(.6))
    for k in range(5): x = chirp(r, 2900 * (1 + .06 * k), .045, 'down'); i = ns(.075 * k); y[i:i + len(x)] += x
    return y * .6


@S('boat', -36, {'open': .4}, 'boat, boats, oar')
def _(p, r):
    n = ns(dur(p, 2)); return (REG['creak']['fn'](dict(dur=n / SR, f=230, r0=8, r1=12), r)[:n] * .3 + bubbles(n, r, 14, 350, 1200) * .4) * swell(n, .2, .4)


def find(text):
    """Effect for a free-text event name: exact key, else the longest matching keyword."""
    t = str(text).lower().replace('_', ' ')
    k = t.strip().replace(' ', '_')
    if k in REG: return k
    best, L = None, 0
    for name, e in REG.items():
        for w in e['words']:
            if len(w) > L and re.search(r'\b' + re.escape(w) + r'\b', t): best, L = name, len(w)
    return best

