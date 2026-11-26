"""Pitched instruments: strings with a wrapping bridge (tanpura, sitar, veena, sarod), struck and plucked courses,
jet-driven flute, bowed strings, lip-reed horns and conch, drones."""
import functools
import numpy as np
from numba import njit
from scipy import signal
from scipy.ndimage import gaussian_filter1d
from core import SR, ns, db, hp, lp, bp, peq, rng, wander, smooth, sweep, modal, expenv, pan, fades, cents, sec, hz, wide

# ---- the string that buzzes on a curved bridge -------------------------------------------------------------------------


@njit(cache=True, fastmath=True)
def _jawari(q0, f0, xk, hk, K, dmp, s0, s1, inh, n, fs, mute, mtau):
    """Modal string with unilateral contact at points xk (fractions of length) against a bridge of height hk below rest.
    f0: fundamental per control block of 32 samples.  Returns the force on the bridge."""
    M = len(q0)
    P = len(xk)
    phi = np.empty((P, M))
    for p in range(P):
        for m in range(M): phi[p, m] = np.sin((m + 1) * np.pi * xk[p])
    q = q0.copy(); qp = q0.copy()
    a1 = np.zeros(M); a2 = np.zeros(M); b = np.zeros(M)
    out = np.empty(n)
    F = np.zeros(P)
    yo = np.zeros(P)
    T = 1. / fs
    for i in range(n):
        if i % 32 == 0:
            f1 = f0[min(i // 32, len(f0) - 1)]
            for m in range(M):
                h = m + 1.
                f = f1 * h * np.sqrt(1 + inh * h * h)
                sg = s0 + s1 * (f / 1000.) ** 1.7
                if i > mute: sg += mtau
                R = np.exp(-sg * T)
                if f > fs * .45: R = 0.
                a1[m] = 2 * R * np.cos(2 * np.pi * f * T); a2[m] = -R * R; b[m] = 1.
            if i == 0:
                for m in range(M): qp[m] = q[m]
        tot = 0.
        for p in range(P):
            y = 0.
            for m in range(M): y += phi[p, m] * q[m]
            pen = hk[p] - y
            F[p] = 0.
            if pen > 0:
                F[p] = K * pen * (1. + dmp * min(max((yo[p] - y) / (pen + 1e-9), -.9), 1.))
                tot += F[p]
            yo[p] = y
        s = 0.
        if tot > 0:
            for m in range(M):
                f = 0.
                for p in range(P): f += phi[p, m] * F[p]
                x = a1[m] * q[m] + a2[m] * qp[m] + f
                qp[m] = q[m]; q[m] = x
                s += (m + 1) * x
        else:
            for m in range(M):
                x = a1[m] * q[m] + a2[m] * qp[m]
                qp[m] = q[m]; q[m] = x
                s += (m + 1) * x
        out[i] = s
    return out


def jawari(f, dur, pluck=.13, bright=.6, curve=.55, t60=6., hf=.9, contact=1., amp=1., bend=None, mute=None, inh=2e-5, reach=.016, thread=None, seed=0):
    """f: Hz (start). bend: function of time array -> pitch factor. curve: bridge steepness (smaller buzzes longer)."""
    r = rng('jaw', seed)
    fs = 96000
    n = int(dur * fs)
    nb = n // 32 + 2
    t = np.arange(nb) * 32 / fs
    f0 = np.full(nb, f) if bend is None else f * bend(t)
    M = int(min(90, 15000 / f0.max()))
    m = np.arange(1, M + 1)
    q = amp * np.sin(m * np.pi * pluck) / (m * m) * 2.2 * np.exp(-(m / (M * bright * .9 + 4)) ** 2)
    if thread: xk = np.array([thread, thread * 1.06]); hk = np.array([.0, -.0004])
    else:
        xk = np.linspace(reach / 6, reach, 6)
        hk = -curve * .035 * (xk / reach) ** 2
    K = .22 * contact / (len(xk) * M) * 2
    out = _jawari(q, f0, xk, hk, K, .25, 3.45 / t60, hf, inh, n, float(fs), int((mute if mute else dur * 2) * fs), 60.)
    return signal.resample_poly(out, 1, 2) * .25


@functools.lru_cache(None)
def body_ir(kind):
    """Short modal body response."""
    r = rng('body', kind)
    P = dict(gourd=[(95, .05, .8), (180, .06, 1.), (290, .05, .9), (430, .04, .8), (640, .03, .6), (1150, .02, .5), (2100, .012, .4), (3400, .008, .25)],
             sarod=[(140, .05, .9), (260, .05, 1.), (420, .04, .9), (780, .025, .8), (1400, .015, .6), (2600, .01, .4)],
             box=[(210, .03, .7), (420, .03, .9), (800, .02, .8), (1500, .012, .7), (3000, .008, .5)],
             violin=[(275, .035, 1.), (460, .03, 1.), (540, .028, 1.1), (700, .02, .7), (850, .018, .7), (1000, .016, .9), (1300, .012, .6), (2000, .008, .7), (2500, .007, 1.), (2900, .006, .9), (3600, .005, .45)],
             cello=[(100, .06, 1.), (185, .05, 1.1), (220, .05, 1.), (330, .03, .6), (470, .025, .7), (600, .02, .6), (1000, .012, .6), (1600, .008, .6), (2300, .006, .5)])[kind]
    n = ns(.18)
    f = np.array([p[0] for p in P]) * (1 + .02 * r.standard_normal(len(P))); tau = np.array([p[1] for p in P]); a = np.array([p[2] for p in P]) / tau / SR * 2
    h = modal(f, a, tau, r.uniform(0, 6, len(P)), n, np.ones(1))
    h[0] += .35
    return h / np.sqrt((h ** 2).sum())


def body(x, kind): return signal.oaconvolve(x, body_ir(kind))[:len(x)]


@functools.lru_cache(None)
def _tanpura_string(f, var, dur):
    x = jawari(f, dur, pluck=.28 + .04 * var, bright=.5, curve=.16, t60=11., hf=.28, reach=.011, amp=.8 + .1 * var, contact=1., seed=var)
    return fades(hp(x, 60), .006, 1.2)


def tanpura(L, f0, f1, cycle=4.5, sa=146.8324, g=1., first='P,', r=None, start=0):
    """Four strings, Pa Sa Sa Sa(low), slow and unhurried, over film frames f0..f1."""
    r = r or rng('tanpura', f0)
    seq = [(first, 0., .75), ('S', .24, .85), ('S', .47, .85), ('S,', .70, 1.)]
    t, k = sec(f0), start
    while t < sec(f1):
        d, off, v = seq[k % 4]
        x = _tanpura_string(hz(d, sa) * (1 + (.0006 if k % 4 == 2 else 0)), k % 3, 6.5)
        L.add(body(x, 'gourd'), t, g * v * r.uniform(.9, 1.05), [-.35, -.1, .12, .35][k % 4])
        step = [.24, .23, .23, .30][k % 4] * cycle
        t += step + r.normal(0, .012); k += 1


def _bendcurve(nts, i0, t0, lag=.05, over=True):
    """Pitch factor function for one pluck that slides through the notes nts (meend)."""
    base = nts[0][2]
    def fn(t):
        y = np.zeros_like(t) + 0.
        for j in range(1, len(nts)):
            a = nts[j][0] - t0
            L = min(.16, .5 * (nts[j][0] - nts[j - 1][0]) + .02)
            u = np.clip((t - (a - .6 * L)) / L, 0, 1)
            y += (np.log2(nts[j][2] / nts[j - 1][2])) * (.5 - .5 * np.cos(np.pi * u))
        for j, x in enumerate(nts):
            a = x[0] - t0
            if 'w' in x[3]: y += .085 * np.sin(2 * np.pi * 5.4 * (t - a)) * ((t > a) & (t < x[1] - t0)) * np.clip((t - a) / .1, 0, 1)
            if '~' in x[3]: y += .03 * np.sin(2 * np.pi * 3.2 * (t - a)) * ((t > a) & (t < x[1] - t0)) * np.clip((t - a) / .2, 0, 1)
            if '^' in x[3] : y += .16 * np.exp(-.5 * ((t - a - .03) / .03) ** 2)
        return 2 ** y
    return fn


KIND = dict(
    sitar=dict(pluck=.1, bright=.75, curve=.35, t60=4.5, hf=.5, reach=.015, bod='gourd', low=90),
    veena=dict(pluck=.17, bright=.5, curve=.6, t60=6., hf=.55, reach=.012, bod='gourd', low=60),
    sarod=dict(pluck=.12, bright=.65, curve=2.5, t60=3., hf=.8, reach=.006, bod='sarod', low=70),
    toy=dict(pluck=.09, bright=.6, curve=3., t60=1.1, hf=2.4, reach=.005, bod='box', low=110),
    tumbi=dict(pluck=.07, bright=.8, curve=.7, t60=1.4, hf=1.2, reach=.012, bod='box', low=140),
)


def pluck(f, dur, kind='sitar', vel=1., seed=0, bend=None, mute=None):
    k = dict(KIND[kind]); bod = k.pop('bod'); low = k.pop('low')
    r = rng('pl', kind, seed)
    k['bright'] = k['bright'] * (.55 + .45 * vel); k['pluck'] *= 1 + .12 * r.standard_normal()
    x = jawari(f, dur, amp=.55 + .5 * vel, bend=bend, mute=mute, seed=seed, **k)
    m = ns(.012); c = r.standard_normal(m) * np.exp(-np.arange(m) / (m * .2))          # the plectrum
    x[:m] += .05 * bp(c, 900, 6000) * np.abs(x[:ns(.1)]).max() * 4
    return fades(hp(body(x, bod), low), .0006, min(.25, dur * .3)) * (.5 + .5 * vel)


def line(L, nts, kind='sitar', g=1., p=0., ring=1.2, seed=0, human=.006, slur=True):
    """Notes flagged '~', 'w', '^' ornament; a run whose later notes carry flag 'v' is one pluck bent through them."""
    r = rng('line', kind, seed, len(nts))
    i = 0
    while i < len(nts):
        j = i + 1
        while slur and j < len(nts) and 'v' in nts[j][3]: j += 1
        grp = nts[i:j]
        a, b = grp[0][0], grp[-1][1]
        d = b - a + ring
        x = pluck(grp[0][2], d, kind, grp[0][4], seed + i, _bendcurve(grp, 0, a), mute=b - a + ring * .6)
        L.add(x, a + abs(r.normal(0, human)), g * r.uniform(.9, 1.05), p)
        i = j


# ---- struck and swept courses -------------------------------------------------------------------------------------------


def course(f, dur, hard=.6, pos=.13, t60=3., strings=3, seed=0, spread=1.6, inh=6e-5):
    """Santoor or swarmandal: several strings per note, struck or plucked, no bridge contact."""
    r = rng('course', seed)
    n = ns(dur)
    y = np.zeros(n)
    K = int(min(42, 13000 / f))
    k = np.arange(1, K + 1)
    for s in range(strings):
        ff = f * k * np.sqrt(1 + inh * k * k) * 2 ** ((s - (strings - 1) / 2) * spread * r.uniform(.6, 1.4) / 1200)
        a = np.sin(k * np.pi * pos) / k ** .75 * np.exp(-(k * f / (1500 + 6500 * hard)) ** 1.3)
        tau = t60 / 6.91 / (1 + (k * f / 2600) ** 1.1) * (1 + .2 * r.standard_normal(K)) * (1.25 if s % 2 else .8)
        y += modal(ff, a / strings, np.maximum(tau, .01), r.uniform(-.3, .3, K), n, np.ones(1))
    m = ns(.02); c = modal(np.array([2300., 3900., 5600.]), np.array([.2, .16, .1]) * hard, np.array([.004, .003, .002]), np.zeros(3), m, np.ones(1))
    y[:m] += c * .6
    return fades(body(y, 'box'), .0005, min(.3, dur * .3))


def santoor(L, nts, g=1., p=0., seed=0, hard=.6, ring=1.6, roll=0, human=.005):
    """roll > 0: repeat long notes at that interval (seconds), the santoor's shimmer."""
    r = rng('san', seed)
    for i, (a, b, f, fl, v) in enumerate(nts):
        hits = [a] if not roll or b - a < 2 * roll else list(np.arange(a, b - roll * .4, roll))
        for j, h in enumerate(hits):
            vv = v * (1. if j == 0 else .45 + .25 * r.random() + .25 * np.sin(np.pi * j / len(hits)))
            L.add(course(f, ring, hard * (.6 + .4 * vv), seed=seed + 31 * i + j % 4, t60=2.4), h + (abs(r.normal(0, human)) if j else 0), g * vv, p + .1 * (-1) ** j)


def swarmandal(L, degs, frame, dt=.045, g=1., sa=293.6648, p0=-.5, p1=.5, ring=3., seed=0, down=False):
    d = degs.split()
    if down: d = d[::-1]
    for i, x in enumerate(d):
        L.add(course(hz(x, sa), ring, .35, pos=.22, t60=4.5, strings=2, seed=seed + i), sec(frame) + i * dt * (1 + .06 * np.sin(i * 1.7)), g * (.7 + .3 * i / len(d)), p0 + (p1 - p0) * i / max(1, len(d) - 1))


# ---- bells, plates, gongs ---------------------------------------------------------------------------------------------------
BELL = [(.5, .5, 1.6), (1., 1., 1.), (1.19, .55, .8), (1.5, .35, .7), (2.0, .7, .55), (2.52, .28, .4), (2.66, .22, .35), (3.01, .3, .3), (4.1, .2, .2), (5.4, .13, .13), (6.8, .09, .1)]


def bell(f, dur=4., t60=4., hard=.6, seed=0, beat=.0016):
    r = rng('bell', seed)
    q = np.array(BELL); K = len(q)
    fr_ = np.concatenate([q[:, 0] * (1 - beat * r.uniform(.4, 1, K)), q[:, 0] * (1 + beat * r.uniform(.4, 1, K))]) * f
    a = np.concatenate([q[:, 1]] * 2) * np.exp(-np.maximum(fr_ / f - 1, 0) * (1.1 - hard) * .6) * .5
    tau = np.concatenate([q[:, 2]] * 2) * t60 / 6.91 * np.clip((900 / f) ** .15, .6, 1.4)
    y = modal(fr_, a, tau, r.uniform(0, 6, 2 * K), ns(dur), np.ones(1))
    return fades(y, .0006, min(.5, dur * .3))


def manjira(f=3100., dur=.9, open_=1., seed=0):
    r = rng('manj', seed)
    q = np.array([1., 1.004, 1.47, 1.476, 2.09, 2.1, 2.76, 3.4, 4.2])
    a = np.array([.8, .8, .6, .6, .5, .4, .25, .12, .06])
    return fades(modal(f * q, a, np.array([.5, .55, .4, .42, .3, .3, .2, .12, .08]) * .55 * open_ + .012, r.uniform(0, 6, 9), ns(dur), np.ones(1)), .0005, .05) * .4


def gong(f=62., dur=7., bloom=.35, bright=.6, seed=0, t60=7.):
    """Large bronze: a low cluster, with energy climbing into the upper modes after the blow."""
    r = rng('gong', seed)
    K = 90
    ff = f * (1 + np.cumsum(r.gamma(2., .16, K)))
    ff[:4] = f * np.array([1, 1.006, 1.52, 2.03])
    n = ns(dur)
    y = np.zeros(n)
    t = np.arange(n) / SR
    for lo, hi, rise in ((0, 6, .004), (6, 22, .05), (22, 50, .5), (50, K, 1.)):
        a = np.exp(-ff[lo:hi] / f / (6 + 16 * bright)) * r.uniform(.4, 1, hi - lo)
        tau = t60 / 6.91 / (1 + (ff[lo:hi] / 900) ** .8)
        z = modal(ff[lo:hi], a, tau, r.uniform(0, 6, hi - lo), n, 1 + .012 * np.exp(-t / .25))
        y += z * (1 - np.exp(-t / (rise * bloom + .0008))) * (1 if rise < .1 else 1.6)
    return fades(y * .5, .0008, .8)


# ---- bansuri --------------------------------------------------------------------------------------------------------------


@njit(cache=True, fastmath=True)
def _flute(f, pr, noise, n, fs, jr, refl, lpc, gain, off):
    """Jet-driven open tube: breath crosses the mouth hole, the jet arrives late, saturates, feeds the bore."""
    N = 8192
    bore = np.zeros(N); jet = np.zeros(N)
    out = np.empty(n)
    w = 0; l1 = 0.; dc = 0.; nz = 0.
    for i in range(n):
        D = fs / f[i] - 1.35 / lpc * .5
        x = w - D
        k = int(np.floor(x)); fk = x - k
        b = 0.
        # third-order Lagrange read
        c0 = -fk * (fk - 1) * (fk - 2) / 6; c1 = (fk + 1) * (fk - 1) * (fk - 2) / 2; c2 = -(fk + 1) * fk * (fk - 2) / 2; c3 = (fk + 1) * fk * (fk - 1) / 6
        b = c0 * bore[(k - 1) % N] + c1 * bore[k % N] + c2 * bore[(k + 1) % N] + c3 * bore[(k + 2) % N]
        l1 += lpc * (b - l1)
        r_ = l1 - dc
        dc += .0008 * r_
        nz += .25 * (noise[i] - nz)
        u = pr[i] * (1. + nz)
        jet[w % N] = u - .55 * r_
        x = w - D * jr
        k = int(np.floor(x)); fk = x - k
        j = jet[k % N] * (1 - fk) + jet[(k + 1) % N] * fk
        v = np.tanh(gain * (j - off * 1.0))
        bore[w % N] = .48 * v * (pr[i] > 0) * min(1., pr[i] * 3) + refl * r_
        out[i] = bore[w % N]
        w += 1
    return out


def _flute_raw(f, pr, r, **k):
    up = 2
    n = len(f) * up
    F = np.repeat(f, up); P = np.repeat(pr, up)
    return F, P, n


@functools.lru_cache(None)
def flute_cal():
    """Measured pitch of the raw flute against its nominal pitch, so playing can be corrected."""
    fs_ = np.geomspace(180, 1300, 22)
    out = []
    for f in fs_:
        n = 48000
        r = rng('cal')
        y = _flute(np.full(n, f * 1.), np.full(n, .7), np.zeros(n), n, 96000., .42, .62, .32, 2.2, .7)
        y = y[n // 2:] - y[n // 2:].mean()
        Y = abs(np.fft.rfft(y * np.hanning(len(y)), 8 * len(y)))
        k = int(np.argmax(Y)); a, b, c = np.log(Y[k - 1:k + 2])
        out.append((k + .5 * (a - c) / (a - 2 * b + c)) * 96000 / (8 * len(y)))
    return fs_, np.array(out)


_BAN = dict(jr=.42, refl=.62, lpc=.32, gain=2.2, off=.7)


def bansuri_phrase(nts, seed=0, breath=.10, vib=(4.9, 16), glide=1.5, attack=.06, release=.14, raga=(0, 204, 386, 702, 884), flutter=0.):
    """One breath of legato notes -> (mono, start)."""
    from voice import Singer
    r = rng('ban', seed, len(nts))
    t0, t1 = nts[0][0] - .06, nts[-1][1] + .25
    n = ns(t1 - t0)
    nc = int((t1 - t0) * 1000) + 2
    P = Singer('f', vib=vib, glide=glide, drift=4).pitch([x[:5] + (j == 0,) for j, x in enumerate(nts)], t0, nc, r, raga)
    P = P + 55 * np.exp(-np.clip(t0 + np.arange(nc) * .001 - nts[0][0] + .03, 0, 9) / .045)      # a flute speaks a little flat, a voice more so
    f = 100 * 2 ** (np.interp(np.arange(n) / SR, np.arange(nc) / 1000, P) / 1200)
    nom, act = flute_cal()
    f = f / np.interp(f, nom, act / nom)
    t = t0 + np.arange(n) / SR
    pr = np.zeros(n)
    for j, (a, b, _, fl, v) in enumerate(nts):
        m = (t >= a - (.0 if j else .02)) & (t < b)
        u = np.clip((t[m] - a) / (b - a), 0, 1)
        pr[m] = (.46 + .26 * v) * (1 + (.07 * np.sin(np.pi * u) if b - a > .4 else 0))
        if j and t[m].size and nts[j - 1][1] > a - .02: pr[m] *= 1 - .22 * np.exp(-(t[m] - a) / .03)
    pr = smooth(pr, .012)
    a0, b1 = nts[0][0], nts[-1][1]
    g = np.clip((t - a0 + .035) / attack, 0, 1) ** .7 * np.clip((b1 + .06 - t) / release, 0, 1)
    pr = pr * g * (1 + .035 * wander(n, 5, r)) * (1 + flutter * np.sin(2 * np.pi * 22 * t) * np.exp(-np.clip(t - a0, 0, 9) / .12))
    pr = pr + .25 * np.exp(-np.clip(t - a0 + .02, 0, 9) / .018) * (t > a0 - .02) * g                # chiff
    F, Q = np.repeat(f, 2), np.repeat(pr, 2)
    nz = r.standard_normal(2 * n) * (breath + .22 * np.repeat(np.exp(-np.clip(t - a0 + .02, 0, 9) / .03), 2))
    y = signal.resample_poly(_flute(F, Q, nz, 2 * n, 96000., **_BAN), 1, 2)
    air = bp(r.standard_normal(n), 1800, 7000) * pr * .010
    return fades(hp(y, 150) * .5 + air, .004, .03), t0


def bansuri(L, nts, g=1., p=0., seed=0, **k):
    cur = []
    k0 = 0
    for x in nts + [None]:
        if x is None or (cur and x[0] - cur[-1][1] > .1):
            y, t0 = bansuri_phrase(cur, seed=seed + k0, **k)
            L.add(y, t0, g, p); k0 += 1; cur = []
        if x is not None: cur.append(x)


# ---- bowed strings -----------------------------------------------------------------------------------------------------------


@njit(cache=True, fastmath=True)
def _bow(f, vb, fb, n, fs, beta, lp1, loss, seed, rough):
    """Bowed string: two travelling waves meet a stick-slip friction curve at the bow."""
    np.random.seed(seed)
    N = 8192
    nk = np.zeros(N); br = np.zeros(N)
    out = np.empty(n)
    l = 0.; ln = 0.
    for i in range(n):
        D = fs / f[i]
        Db = D * beta; Dn = D - Db - (1. / lp1 - 1.) - 1.0
        x = i - Db; k = int(np.floor(x)); fk = x - k
        b = br[k % N] * (1 - fk) + br[(k + 1) % N] * fk
        x = i - Dn; k = int(np.floor(x)); fk = x - k
        c0 = -fk * (fk - 1) * (fk - 2) / 6; c1 = (fk + 1) * (fk - 1) * (fk - 2) / 2; c2 = -(fk + 1) * fk * (fk - 2) / 2; c3 = (fk + 1) * fk * (fk - 1) / 6
        a = c0 * nk[(k - 1) % N] + c1 * nk[k % N] + c2 * nk[(k + 1) % N] + c3 * nk[(k + 2) % N]
        l += lp1 * (b - l)
        rb = -loss * l
        rn = -a
        v = vb[i] * (1 + rough * np.random.standard_normal())
        dv = v - (rb + rn)
        s = abs(dv * fb[i]) + .75
        s = s * s; s = s * s
        g = 1. / s
        if g > .98: g = .98
        nv = dv * g
        nk[i % N] = rb + nv
        br[i % N] = rn + nv
        out[i] = b
    return out


@functools.lru_cache(None)
def bow_cal(kind):
    fs_ = np.geomspace(*((60, 420) if kind == 'cello' else (170, 1250)), 14)
    out = []
    for f in fs_:
        n = 48000
        y = _bow(np.full(n, f * 1.), np.full(n, .2), np.full(n, 3.), n, 96000., .115, _BOWLP[kind], .985, 1, 0.)
        y = y[n // 2:]; y = y - y.mean()
        Y = abs(np.fft.rfft(y * np.hanning(len(y)), 8 * len(y)))
        h = sum(np.interp(np.arange(len(Y) // 6) * m, np.arange(len(Y)), Y) for m in (1, 2, 3))          # harmonic sum, so a weak fundamental does not fool it
        lo, hi = int(f * .9 * 8 * len(y) / 96000), int(f * 1.1 * 8 * len(y) / 96000)
        k = lo + int(np.argmax(h[lo:hi])); out.append(k * 96000 / (8 * len(y)))
    return fs_, np.array(out)


_BOWLP = dict(violin=.55, cello=.4)


def bowed(nts, kind='violin', seed=0, cent=0., vib=(5.6, 20), press=1., glide=.7, attack=.07, release=.15, trem=0., raga=(0, 204, 386, 702, 884), swell=0.):
    from voice import Singer
    r = rng('bow', kind, seed)
    t0, t1 = nts[0][0] - .05, nts[-1][1] + release + .25
    n = ns(t1 - t0); nc = int((t1 - t0) * 1000) + 2
    P = Singer('f', vib=(vib[0] + .4 * r.standard_normal(), vib[1]), glide=glide, drift=4).pitch([x[:5] + (j == 0,) for j, x in enumerate(nts)], t0, nc, r, raga) + cent
    f = 100 * 2 ** (np.interp(np.arange(n) / SR, np.arange(nc) / 1000, P) / 1200)
    nom, act = bow_cal(kind); f = f / np.interp(f, nom, act / nom)
    t = t0 + np.arange(n) / SR
    vb = np.zeros(n)
    for j, (a, b, _, fl, v) in enumerate(nts):
        m = (t >= a) & (t < b)
        u = (t[m] - a) / (b - a)
        vb[m] = v * (1 + (swell * np.sin(np.pi * u) if b - a > .5 else 0))
        if j: vb[m] *= 1 - .35 * np.exp(-(t[m] - a) / .03)
    vb = smooth(vb, .02)
    if trem:
        ph = np.cumsum(trem * (1 + .1 * wander(n, 3, r))) / SR
        vb = vb * (.25 + .75 * abs(np.sin(np.pi * ph)))
    g = np.clip((t - nts[0][0] + .02) / attack, 0, 1) * np.clip((nts[-1][1] + release - t) / release, 0, 1)
    vb = .04 + .2 * vb * g * (1 + .05 * wander(n, 4, r))
    y = _bow(np.repeat(f, 2), np.repeat(vb, 2), np.full(2 * n, 3.3 / press), 2 * n, 96000., .115 + .02 * r.uniform(-1, 1), _BOWLP[kind], .985, int(r.integers(1 << 30)), .05)
    y = body(hp(signal.resample_poly(y, 1, 2), 45), kind)
    return y * g ** 1.2 * np.interp(vb, [.04, .25], [.25, 1.]), t0


def strings(L, nts, kind='violin', n=8, g=1., p=0., width=.5, seed=0, loose=.012, tune=6., **k):
    """A section: n players, each with own bow, body, tuning and timing."""
    r = rng('sec', kind, seed)
    bows = []
    cur = []
    for x in nts + [None]:
        if x is None or (cur and x[0] - cur[-1][1] > .04): bows.append(cur); cur = []
        if x is not None: cur.append(x)
    for i in range(n):
        dt, c, pp = loose * r.standard_normal(), tune * r.standard_normal(), p + width * (2 * (i + .5) / n - 1)
        for j, b in enumerate(bows):
            y, t0 = bowed(b, kind, seed=seed * 97 + i * 13 + j, cent=c, vib=(5.5, 20 * r.uniform(.6, 1.4)), **k)
            L.add(y, t0 + dt, g / np.sqrt(n), pp)


def chord(L, degs, f0, f1, kind='violin', sa=293.6648, v=.8, **k):
    for j, d in enumerate(degs.split()):
        strings(L, [(sec(f0), sec(f1), hz(d, sa), '', v)], kind, seed=k.pop('seed', 0) + j if False else j + int(f0), **k)


# ---- lip reeds ---------------------------------------------------------------------------------------------------------------


@njit(cache=True, fastmath=True)
def _steepen(x, k, n):
    """Wave steepening in a long bore: loud parts of the wave travel faster."""
    N = 4096
    buf = np.zeros(N); out = np.empty(n)
    for i in range(n):
        buf[i % N] = x[i]
        d = 60. - k[i] * x[i]
        if d < 1: d = 1.
        z = i - d; j = int(np.floor(z)); f = z - j
        out[i] = buf[j % N] * (1 - f) + buf[(j + 1) % N] * f if j >= 0 else 0.
    return out


def brass_note(nts, seed=0, kind='horn', cent=0., attack=.05, release=.1, growl=0., blare=1., glide=.5, scoop=0., vib=(5., 10)):
    """Lip pulses, brighter as they get louder, through bore steepening and a bell."""
    from voice import Singer
    r = rng('brass', kind, seed)
    t0, t1 = nts[0][0] - .05, nts[-1][1] + release + .1
    n = ns(t1 - t0); nc = int((t1 - t0) * 1000) + 2
    P = Singer('f', vib=vib, glide=glide, drift=5).pitch([x[:5] + (j == 0,) for j, x in enumerate(nts)], t0, nc, r) + cent
    t = t0 + np.arange(n) / SR
    P = np.interp(np.arange(n) / SR, np.arange(nc) / 1000, P)
    if scoop: P = P - scoop * np.exp(-np.clip(t - nts[0][0], 0, 99) / .16)
    f = 100 * 2 ** (P / 1200) * (1 + .004 * wander(n, 30, r) * np.exp(-np.clip(t - nts[0][0], 0, 9) / .08)) 
    v = np.zeros(n)
    for j, (a, b, _, fl, ve) in enumerate(nts):
        m = (t >= a) & (t < b); u = t[m] - a
        v[m] = ve * (.82 + .18 * np.exp(-u / .12))
        if j: v[m] *= 1 - .4 * np.exp(-u / .03)
    v = smooth(v, .008)
    g = np.clip((t - nts[0][0] + .012) / attack, 0, 1) ** 1.2 * np.clip((nts[-1][1] + release - t) / release, 0, 1)
    v = v * g * (1 + .03 * wander(n, 7, r))
    if growl: v = v * (1 + growl * np.sin(2 * np.pi * 27 * t + wander(n, 3, r)))
    ph = 2 * np.pi * np.cumsum(f) / SR
    lip = np.sin(ph + .5 * np.sin(ph)) + .35 * np.sin(2 * ph + .6)
    lip = lip * v + .02 * v * r.standard_normal(n)
    up = signal.resample_poly(lip, 2, 1)
    y = _steepen(up, np.repeat(v, 2)[:len(up)] * 96000 / np.repeat(f, 2)[:len(up)] * .115 * blare, len(up))
    y = signal.resample_poly(y, 1, 2)[:n]
    y = hp(y, f.mean() * .6, 1)
    if kind == 'horn': y = peq(peq(hp(y, 110, 1), 450, 4, .8), 1400, 3, 1.2)
    if kind == 'low': y = peq(peq(y, 250, 3, .7), 900, 3, 1.)
    y = lp(y, 5200 if kind != 'low' else 3600, 1)
    return y * .4, t0


def horns(L, nts, n=4, g=1., p=0., width=.5, seed=0, kind='horn', loose=.008, tune=6, **k):
    r = rng('horns', seed)
    for i in range(n):
        y, t0 = brass_note(nts, seed * 31 + i, kind, tune * r.standard_normal(), **k)
        L.add(y, t0 + loose * r.standard_normal(), g / np.sqrt(n), p + width * (2 * (i + .5) / n - 1))


def conch(f=233., dur=2.2, seed=0, vel=1., rise=.16):
    """Shankha: lips find the note from below, the shell's throat opens, the first formant rises."""
    r = rng('conch', seed)
    n = ns(dur); t = np.arange(n) / SR
    P = f * 2 ** ((-5.0 * np.exp(-t / (rise * .6)) + .18 * np.sin(2 * np.pi * 4.6 * t) * np.clip((t - .5) / .8, 0, 1) - 1.2 * np.clip((t - dur + .25) / .25, 0, 1) + .06 * wander(n, 6, r)) / 12)
    v = np.clip(t / (rise * .8), 0, 1) ** 1.3 * np.clip((dur - t) / .22, 0, 1) * (1 + .06 * wander(n, 5, r)) * vel
    ph = 2 * np.pi * np.cumsum(P) / SR
    lip = (np.sin(ph + .7 * np.sin(ph)) + .25 * np.sin(2 * ph)) * v + .035 * v * r.standard_normal(n)
    y = _steepen(lip, v * SR / P * .10, n)
    F = 330 + 430 * np.clip(t / (rise * 2.2), 0, 1)
    z = .55 * y + 1.5 * sweep(y, F, 3.) + .8 * sweep(y, F * 2.35, 4.) + .22 * sweep(y, np.full(n, 2300.), 4.)
    z += bp(r.standard_normal(n), 900, 4200) * v * .03 * (1 + 3 * np.exp(-t / .08))
    return fades(lp(hp(z, 120), 5500, 2), .004, .05) * .4


def drone(f, dur, seed=0, bright=.4, n=3):
    """Low bowed-string cluster that breathes."""
    r = rng('drone', seed)
    N = ns(dur); t = np.arange(N) / SR
    y = np.zeros(N)
    for i in range(n):
        ph = 2 * np.pi * np.cumsum(f * 2 ** ((5 * r.standard_normal() + 3 * wander(N, .3, r)) / 1200)) / SR
        s = np.zeros(N)
        K = int(min(24, 2400 * bright / f + 3))
        for k in range(1, K + 1):
            s += np.sin(k * ph + r.uniform(0, 6)) / k ** 1.15 * (1 + .5 * wander(N, .35 + .06 * k, r)) * (1 if k < 4 else np.exp(-k * f / (900 * bright + 200)))
        y += s
    return y / n * .3
