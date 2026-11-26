"""Drums.  Membranes as banks of modes: the loaded tabla head (Raman: modes fall into a harmonic series), the plain
circular head (Bessel ratios, air-loaded), tension that rises with the blow, shells, sticks, hands and jingles."""
import functools
import numpy as np
from core import SR, ns, hp, lp, bp, peq, rng, modal, fades, sec, db, sweep
from inst import bell, gong, manjira

BESSEL = np.array([1., 1.594, 2.136, 2.296, 2.653, 2.918, 3.156, 3.501, 3.600, 3.652, 4.060, 4.154, 4.602, 4.832, 4.903, 5.131, 5.412, 5.540, 5.977, 6.153, 6.528, 7.0, 7.6, 8.2, 9.0])
RAMAN = np.array([1., 2., 2.005, 3., 3.01, 4., 4.02, 5., 5.02, 5.05, 6.1, 7.15, 8.3])        # (01)(11)(21,02)(31,12)(41,03,22)...


def _click(n, lo, hi, tau, r):
    x = bp(r.standard_normal(n), lo, hi, 1) * np.exp(-np.arange(n) / SR / tau)
    return x


# ---- tabla family ---------------------------------------------------------------------------------------------------------


@functools.lru_cache(None)
def dayan(stroke='na', f=293.66, v=1., var=0):
    """Right-hand drum.  na: rim, fundamental damped.  tin: softer, long.  tun: open centre.  te, ti: dead slaps."""
    r = rng('dayan', stroke, var)
    n = ns(1.3)
    A = dict(na=[.06, 1., .8, .75, .6, .35, .25, .18, .12, .1, .05, .03, .02], tin=[.25, 1., .7, .3, .25, .1, .08, .05, .03, .02, .01, 0, 0],
             tun=[1., .25, .2, .06, .05, .02, .02, .01, 0, 0, 0, 0, 0], te=[.3, .4, .4, .4, .4, .4, .4, .4, .3, .3, .3, .25, .2])[stroke]
    T = dict(na=.30, tin=.42, tun=.5, te=.016)[stroke]
    a = np.array(A) * (1 + .12 * r.standard_normal(13)) * np.exp(-RAMAN * .10 * (1.2 - v))
    if stroke == 'te': ratio = RAMAN * (1 + .05 * r.standard_normal(13)) * .85
    else: ratio = RAMAN
    g = 1 + (.008 * np.exp(-np.arange(n) / SR / .03) if stroke != 'te' else 0)
    y = modal(f * ratio, a, T / (1 + .28 * (RAMAN - 1)) * (1 + .1 * r.standard_normal(13)), r.uniform(-.4, .4, 13), n, np.ones(n) * g)
    m = ns(.03)
    y[:m] += _click(m, 1500, 6500, .0022 if stroke != 'te' else .006, r) * (.7 if stroke in ('na', 'te') else .3) * v
    if stroke == 'te': y[:m] += _click(m, 500, 2200, .009, r) * .5
    return fades(y, .0003, .05) * .5 * (.35 + .65 * v)


@functools.lru_cache(None)
def bayan(stroke='ge', f=88., v=1., bend=.35, var=0, hold=.09):
    """Left-hand drum; the heel of the hand bends the note up after the blow.  ke: flat slap."""
    r = rng('bayan', stroke, var)
    n = ns(1.2); t = np.arange(n) / SR
    if stroke == 'ke':
        y = modal(f * np.array([2.1, 3.2, 4.4, 5.6, 7.]), np.array([.6, .6, .5, .4, .3]), np.full(5, .016), np.zeros(5), n, np.ones(1))
        m = ns(.03); y[:m] += _click(m, 400, 2600, .008, r) * .8
        return fades(y, .0003, .05) * .5 * (.35 + .65 * v)
    g = 1 + .05 * np.exp(-t / .02) + bend * (1 - np.exp(-np.maximum(t - .01, 0) / hold)) - bend * .25 * np.clip((t - .35) / .5, 0, 1)
    y = modal(f * np.array([1., 1.9, 2.75, 3.6, 4.5, 5.6]), np.array([1., .34, .16, .10, .06, .04]), np.array([.34, .16, .10, .06, .05, .04]), r.uniform(-.3, .3, 6), n, g)
    m = ns(.02); y[:m] += _click(m, 300, 1800, .004, r) * .35 * v
    return fades(y, .0005, .06) * .75 * (.35 + .65 * v)


@functools.lru_cache(None)
def pakhawaj(stroke='dha', f=196., v=1., var=0):
    """Barrel drum: deep dough-loaded bass head, open ringing treble."""
    r = rng('pak', stroke, var)
    n = ns(1.5)
    y = np.zeros(n)
    if stroke in ('dha', 'ta', 'din'):
        A = np.array([.35, 1., .7, .6, .5, .3, .2, .15, .1, .06, .03, .02, .01]) if stroke != 'din' else np.array([1., .4, .3, .12, .1, .05, .04, .02, .01, .01, 0, 0, 0])
        y += modal(f * RAMAN * np.r_[1, np.full(12, 1.01)], A, .34 / (1 + .3 * (RAMAN - 1)), r.uniform(-.4, .4, 13), n, np.ones(n))
        m = ns(.03); y[:m] += _click(m, 1200, 5000, .003, r) * .55 * v
    if stroke in ('dha', 'ge'):
        t = np.arange(n) / SR
        g = 1 + .28 * np.exp(-t / .03)
        y += modal(66. * np.array([1, 1.62, 2.2, 2.9, 3.7]), np.array([1.7, .6, .3, .2, .1]), np.array([.32, .14, .08, .05, .03]), np.zeros(5), n, g)
        m = ns(.02); y[:m] += _click(m, 200, 1200, .005, r) * .5 * v
    if stroke == 'ki':
        y += modal(f * np.array([1.4, 2.3, 3.3, 4.5, 5.9, 7.3]), np.full(6, .5), np.full(6, .013), np.zeros(6), n, np.ones(1))
        m = ns(.03); y[:m] += _click(m, 700, 4000, .008, r)
    return fades(y, .0003, .06) * .42 * (.35 + .65 * v)


@functools.lru_cache(None)
def dholak(stroke='dum', v=1., var=0, f=0.):
    r = rng('dholak', stroke, var)
    n = ns(.8); t = np.arange(n) / SR
    if stroke == 'dum':
        g = 1 + .5 * np.exp(-t / .035)
        y = modal((f or 82.) * np.array([1, 1.6, 2.2, 2.9]), np.array([1.5, .5, .25, .15]), np.array([.2, .09, .06, .04]), np.zeros(4), n, g)
        m = ns(.02); y[:m] += _click(m, 250, 1500, .005, r) * .5
    elif stroke == 'gum':
        g = 1 + .9 * (1 - np.exp(-t / .07))
        y = modal((f or 78.) * np.array([1, 1.6, 2.2]), np.array([1.5, .4, .2]), np.array([.22, .1, .06]), np.zeros(3), n, g)
        m = ns(.02); y[:m] += _click(m, 250, 1500, .005, r) * .4
    else:
        ff = (f or 330.) * (1 if stroke == 'na' else 1.05)
        y = modal(ff * BESSEL[:14], np.array([.5, 1, .8, .6, .6, .5, .4, .3, .3, .2, .2, .1, .1, .1]), (.11 if stroke == 'na' else .02) / (1 + .25 * (BESSEL[:14] - 1)), r.uniform(-.5, .5, 14), n, np.ones(1))
        m = ns(.02); y[:m] += _click(m, 1800, 7000, .003, r) * .6
    return fades(y, .0003, .05) * .45 * (.35 + .65 * v)


@functools.lru_cache(None)
def frame(stroke='doum', f=74., v=1., var=0, jingle=0.):
    r = rng('framed', stroke, var)
    n = ns(1.4)
    t = np.arange(n) / SR
    if stroke == 'doum':
        y = modal(f * BESSEL[:12] * (1 + .01 * r.standard_normal(12)), np.array([1.4, .8, .4, .4, .3, .2, .15, .1, .1, .08, .05, .05]), .34 / (1 + .7 * (BESSEL[:12] - 1)), r.uniform(-.4, .4, 12), n, 1 + .10 * v * np.exp(-t / .05))
        m = ns(.02); y[:m] += _click(m, 200, 1600, .004, r) * .4
    else:
        y = modal(f * 2.2 * BESSEL[:16], .5 * np.exp(-np.arange(16) * .07), .07 / (1 + .12 * np.arange(16)), r.uniform(-.5, .5, 16), n, np.ones(1))
        m = ns(.03); y[:m] += _click(m, 900, 5200, .006, r) * .55
    if jingle:
        for k in range(5):
            d = ns(.004 * k + .003 * r.random()); z = manjira(5200 + 700 * k, .25, .18, seed=k + var) * jingle * .25
            y[d:d + len(z)] += z
    return fades(y, .0003, .06) * .5 * (.35 + .65 * v)


# ---- big drums ----------------------------------------------------------------------------------------------------------


@functools.lru_cache(None)
def war(f=46., v=1., var=0, hard=.5, dur=2.6, rim=0.):
    """A head you could sleep on: tension modulation, air-loaded modes, a shell, a log of a beater."""
    r = rng('war', var, round(f))
    n = ns(dur); t = np.arange(n) / SR
    K = 22
    q = BESSEL[:K] * (1 + .012 * r.standard_normal(K)); q[0] *= .92
    a = np.exp(-(q - 1) * (.75 - .35 * hard * v)) * (1 + .25 * r.standard_normal(K)); a[0] = 1.25
    tau = .62 / (1 + .75 * (q - 1))
    g = 1 + (.16 * v) * np.exp(-t / .055) + .05 * v * np.exp(-t / .25)
    y = modal(f * q, a, tau, r.uniform(-.3, .3, K), n, g)
    y += modal(np.array([112., 187., 265., 410.]), np.array([.35, .3, .2, .12]) * v, np.array([.07, .05, .04, .03]), np.zeros(4), n, np.ones(1))
    m = ns(.12)
    y[:m] += _click(m, 120, 900, .016, r) * .9 * v + _click(m, 900, 4200, .006, r) * (.25 + .7 * hard) * v
    if rim: y[:m] += modal(np.array([620., 1130., 1710., 2600.]), np.array([.5, .5, .35, .2]) * rim, np.array([.02, .016, .012, .008]), np.zeros(4), m, np.ones(1))
    y = np.tanh(y * .9)
    return fades(y, .0004, .3) * .8 * (.3 + .7 * v)


@functools.lru_cache(None)
def dhol(stroke='dha', v=1., var=0):
    """Dhol: cane on the treble head, curved stick on the bass."""
    r = rng('dhol', stroke, var)
    n = ns(.9); t = np.arange(n) / SR
    y = np.zeros(n)
    if stroke in ('dha', 'ge'):
        y += modal(62. * np.array([1, 1.6, 2.2, 2.6, 3.4]), np.array([1.6, .8, .4, .3, .2]), np.array([.2, .1, .07, .05, .03]), np.zeros(5), n, 1 + .4 * np.exp(-t / .028))
        m = ns(.03); y[:m] += _click(m, 200, 1400, .006, r) * .8
    if stroke in ('dha', 'na'):
        y += modal(310. * BESSEL[:16], .45 * np.exp(-np.arange(16) * .06), .085 / (1 + .12 * np.arange(16)), r.uniform(-.5, .5, 16), n, np.ones(1))
        m = ns(.02); y[:m] += _click(m, 2200, 7500, .0025, r) * .8
    return fades(np.tanh(y), .0003, .05) * .55 * (.35 + .65 * v)


@functools.lru_cache(None)
def nagara(v=1., var=0, f=92., hard=.8):
    """Kettle drum pair, stick struck."""
    r = rng('nag', var, f)
    n = ns(1.3); t = np.arange(n) / SR
    q = np.array([1., 1.5, 1.98, 2.44, 2.9, 3.4, 4.2, 4.9, 5.7, 6.6])
    y = modal(f * q, np.array([1., .9, .7, .5, .35, .28, .2, .14, .1, .07]) * (1 + .15 * r.standard_normal(10)), .36 / (1 + .45 * (q - 1)), r.uniform(-.4, .4, 10), n, 1 + .06 * v * np.exp(-t / .03))
    m = ns(.04); y[:m] += _click(m, 900, 5500, .004, r) * hard * v + _click(m, 200, 800, .008, r) * .5
    return fades(np.tanh(y * .9), .0003, .1) * .6 * (.35 + .65 * v)


@functools.lru_cache(None)
def clap(v=1., var=0):
    r = rng('clap', var); n = ns(.25); y = np.zeros(n)
    for d in np.sort(r.uniform(0, .012, 4)):
        i = ns(d); m = n - i
        y[i:] += bp(r.standard_normal(m), 900, 3200, 1) * np.exp(-np.arange(m) / SR / .012) * r.uniform(.6, 1)
    return fades(y, .0003, .05) * .4 * v


@functools.lru_cache(None)
def wood(f=900., v=1., var=0, tau=.03):
    r = rng('wood', var, f)
    q = np.array([1., 2.57, 4.1, 5.6]) * (1 + .03 * r.standard_normal(4))
    n = ns(.35)
    y = modal(f * q, np.array([1., .5, .3, .15]), tau / q ** .7, np.zeros(4), n, np.ones(1))
    m = ns(.01); y[:m] += _click(m, 1500, 6000, .0015, r) * .5
    return fades(y, .0003, .03) * .4 * v


@functools.lru_cache(None)
def stone(f=420., v=1., var=0, big=0.):
    """A rock struck by a rock."""
    r = rng('stone', var, f)
    n = ns(.6); K = 18
    ff = f * np.sort(r.uniform(.6, 7, K)); a = r.uniform(.3, 1, K) / (1 + ff / f * .25); tau = .035 / (1 + ff / 2500) * r.uniform(.5, 1.5, K) * (1 + big)
    y = modal(ff, a, tau, r.uniform(0, 6, K), n, np.ones(1))
    m = ns(.08); y[:m] += _click(m, 500, 4500, .006, r) * .7
    if big:
        t = np.arange(n) / SR
        y += big * modal(np.array([58., 93., 140.]), np.array([2.2, 1.1, .5]), np.array([.13, .08, .05]), np.zeros(3), n, 1 + .4 * np.exp(-t / .02))
    return fades(np.tanh(y * .6), .0003, .05) * .5 * (.35 + .65 * v)


# ---- playing --------------------------------------------------------------------------------------------------------------
STROKES = {
    'D': lambda v, i: dayan('na', v=v, var=i) + 0, 'd': lambda v, i: dayan('tin', v=v, var=i), 'U': lambda v, i: dayan('tun', v=v, var=i), 't': lambda v, i: dayan('te', v=v, var=i),
    'G': lambda v, i: bayan('ge', v=v, var=i, bend=(.2, .38, .55)[i % 3]), 'k': lambda v, i: bayan('ke', v=v, var=i),
    'X': lambda v, i: _sum(dayan('na', v=v, var=i), bayan('ge', v=v, var=i, bend=(.25, .4, .3)[i % 3])), 'Y': lambda v, i: _sum(dayan('tin', v=v, var=i), bayan('ge', v=v, var=i, bend=.5)),
    'P': lambda v, i: pakhawaj('dha', v=v, var=i), 'q': lambda v, i: pakhawaj('ta', v=v, var=i), 'K': lambda v, i: pakhawaj('ki', v=v, var=i), 'g': lambda v, i: pakhawaj('ge', v=v, var=i), 'i': lambda v, i: pakhawaj('din', v=v, var=i),
    'm': lambda v, i: dholak('dum', v=v, var=i), 'u': lambda v, i: dholak('gum', v=v, var=i), 'n': lambda v, i: dholak('na', v=v, var=i), 'c': lambda v, i: dholak('te', v=v, var=i), 'M': lambda v, i: _sum(dholak('dum', v=v, var=i), dholak('na', v=v, var=i)),
    'F': lambda v, i: frame('doum', v=v, var=i, jingle=.3), 'f': lambda v, i: frame('tek', v=v, var=i, jingle=.4),
    'H': lambda v, i: dhol('dha', v=v, var=i), 'h': lambda v, i: dhol('na', v=v, var=i), 'B': lambda v, i: dhol('ge', v=v, var=i),
    'W': lambda v, i: war(v=v, var=i, hard=.5), 'w': lambda v, i: war(62., v=v, var=i, hard=.7, dur=1.6), 'R': lambda v, i: war(46., v=v, var=i, hard=.8, rim=.8),
    'N': lambda v, i: nagara(v, i, 92.), 'o': lambda v, i: nagara(v, i, 138.), 'C': lambda v, i: clap(v, i), 'T': lambda v, i: stone(520., v, i), 'S': lambda v, i: stone(260., v, i, .8),
    'j': lambda v, i: manjira(3300, .7, .9, i), 'J': lambda v, i: manjira(3300, .12, .1, i), 'O': lambda v, i: wood(700, v, i),
}


def _sum(a, b):
    y = np.zeros(max(len(a), len(b))); y[:len(a)] += a; y[:len(b)] += b
    return y


def beat(L, pat, frame, step=3, reps=1, g=1., p=0., human=.004, seed=0, vel=None, width=0., upto=None):
    """pat: one character per step (frames), '.' rest, a following '-' softens, '+' accents. Spaces and | ignored."""
    r = rng('beat', seed, pat, frame)
    ev = []
    for ch in pat.replace(' ', '').replace('|', ''):
        if ch == '-': ev[-1][1] = .42
        elif ch == '+': ev[-1][1] = 1.
        else: ev.append([ch, .74])
    for k in range(reps):
        for i, (ch, v) in enumerate(ev):
            f = frame + (k * len(ev) + i) * step
            if ch == '.' or (upto is not None and f >= upto): continue
            vv = v * (vel(f) if vel else 1.)
            vq = round(float(np.clip(vv * r.uniform(.92, 1.06), .1, 1)) * 12) / 12
            dt = r.normal(0, human) * (0 if i == 0 else 1)
            L.add(STROKES[ch](vq, int(r.integers(4))), sec(f) + dt, g * (.55 + .45 * vv) * (1 if vv > .12 else vv / .12), p + width * r.uniform(-1, 1))


def roll(L, ch, f0, f1, d0=3., d1=1., v0=.2, v1=1., g=1., p=0., seed=0):
    """Accelerating roll that arrives exactly on f1 (the last blow is not played)."""
    r = rng('roll', seed, f0)
    f = float(f1); hits = []
    while f > f0:
        u = (f - f0) / (f1 - f0)
        f -= d0 + (d1 - d0) * u; hits.append(f)
    for f in hits:
        if f < f0: continue
        u = (f - f0) / (f1 - f0); v = v0 + (v1 - v0) * u ** 1.3
        L.add(STROKES[ch](round(float(np.clip(v * r.uniform(.85, 1.1), .1, 1)) * 12) / 12, int(r.integers(4))), sec(f) + r.normal(0, .003), g * v, p + .2 * r.uniform(-1, 1))


def ensemble(L, fn, frame, n=6, spread=.010, g=1., width=.8, seed=0):
    """Many players on one blow: the first is exact, the rest follow within a few milliseconds."""
    r = rng('ens', seed, frame)
    for i in range(n):
        L.add(fn(i), sec(frame) + (0 if i == 0 else abs(r.normal(0, spread))), g * (1. if i == 0 else r.uniform(.4, .8)) / n ** .5, width * (2 * (i + .5) / n - 1) if n > 1 else 0)
