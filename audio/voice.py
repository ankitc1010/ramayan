"""A singing voice: Liljencrants-Fant glottal pulses with jitter, shimmer and aspiration, through a cascade of twelve
time-varying formants (the open tract up to about 12 kHz), two nasal pole-zero pairs, and a frication/burst branch.
Hindi syllables are placed so that the vowel, not the consonant, lands on the beat."""
import numpy as np
from numba import njit
from scipy import signal
from scipy.ndimage import gaussian_filter1d
from core import SR, PULSE, hz, sec, rng, ns, db, hp, lp, bp, pan, fades, wander, cents, _TOK
import functools

OS = 2
CT = .001                     # control step, seconds
NF = 12

# ---- glottal source: LF pulse parameters from Rd (Fant 1995), solved once ------------------------------------------------
RD = np.linspace(.35, 2.7, 64)


def _lf(rd):
    Ra, Rk = (-1 + 4.8 * rd) / 100, (22.4 + 11.8 * rd) / 100
    Rg = 1 / (4 * ((.11 * rd / (.5 + 1.2 * Rk)) - Ra) / Rk)
    tp = 1 / (2 * Rg); te = tp * (1 + Rk); ta = max(Ra, .003)
    if te > .97: te = .97; tp = te / (1 + Rk)
    eps = 1 / ta
    for _ in range(80): eps = (1 - np.exp(-eps * (1 - te))) / ta
    w = np.pi / tp
    t = np.linspace(0, te, 4000); u = np.linspace(te, 1, 4000)
    ret = np.trapezoid(-(np.exp(-eps * (u - te)) - np.exp(-eps * (1 - te))) / (eps * ta), u)
    lo, hi = -60., 200.
    for _ in range(70):
        al = (lo + hi) / 2
        e = np.exp(al * (t - te)) * np.sin(w * t) * (-1 / np.sin(w * te))
        if np.trapezoid(e, t) + ret > 0: lo = al
        else: hi = al
    return tp, te, ta, eps, al


LF = np.array([_lf(r) for r in RD])


@njit(cache=True, fastmath=True)
def _cascade(n, f0, ee, rdt, asp, F, B, z1, p1, z2, p2, vlp, jit, shim, seed, LF, fs, step):
    """Render n samples at fs.  Control arrays advance one row every `step` samples and are interpolated."""
    np.random.seed(seed)
    out = np.empty(n)
    nf = F.shape[1]
    A_, B_, C_ = np.zeros(nf), np.zeros(nf), np.zeros(nf)
    y1, y2 = np.zeros(nf), np.zeros(nf)
    ph, Tj, Aj = 0., 1., 1.
    tp = te = ta = eps = al = 0.5
    E0 = 1.
    zA = np.zeros(2); zB = np.zeros(2); zC = np.zeros(2); x1 = np.zeros(2); x2 = np.zeros(2)
    pA = np.zeros(2); pB = np.zeros(2); pC = np.zeros(2); w1 = np.zeros(2); w2 = np.zeros(2)
    lpv = 0.; alp = 0.; asl = 0.
    op = 0.; T = 1. / fs
    nc = len(f0)
    new = True
    for i in range(n):
        c = i / step
        k = int(c); fk = c - k
        if k >= nc - 1: k = nc - 2; fk = 1.
        if i % 16 == 0:
            for j in range(nf):
                ff = F[k, j] + fk * (F[k + 1, j] - F[k, j])
                bb = B[k, j] + fk * (B[k + 1, j] - B[k, j])
                if j == 0: bb = bb * (1. + .55 * op); ff = ff * (1. + .025 * op)
                r = np.exp(-np.pi * bb * T)
                C_[j] = -r * r; B_[j] = 2 * r * np.cos(2 * np.pi * ff * T); A_[j] = 1 - B_[j] - C_[j]
            for q in range(2):
                fz = (z1[k] + fk * (z1[k + 1] - z1[k])) if q == 0 else (z2[k] + fk * (z2[k + 1] - z2[k]))
                fp = (p1[k] + fk * (p1[k + 1] - p1[k])) if q == 0 else (p2[k] + fk * (p2[k + 1] - p2[k]))
                bz = 90. if q == 0 else 160.
                r = np.exp(-np.pi * bz * T)
                cc = -r * r; b_ = 2 * r * np.cos(2 * np.pi * fz * T); a_ = 1 - b_ - cc
                zA[q] = 1 / a_; zB[q] = -b_ / a_; zC[q] = -cc / a_
                cc = -r * r; b_ = 2 * r * np.cos(2 * np.pi * fp * T); a_ = 1 - b_ - cc
                pA[q] = a_; pB[q] = b_; pC[q] = cc
            alp = 1 - np.exp(-2 * np.pi * (vlp[k] + fk * (vlp[k + 1] - vlp[k])) * T)
        f = f0[k] + fk * (f0[k + 1] - f0[k])
        if new:
            rd = rdt[k]
            u = (rd - .35) / (2.7 - .35) * 63
            if u < 0: u = 0.
            if u > 62.999: u = 62.999
            m = int(u); g = u - m
            tp = LF[m, 0] + g * (LF[m + 1, 0] - LF[m, 0]); te = LF[m, 1] + g * (LF[m + 1, 1] - LF[m, 1])
            ta = LF[m, 2] + g * (LF[m + 1, 2] - LF[m, 2]); eps = LF[m, 3] + g * (LF[m + 1, 3] - LF[m, 3])
            al = LF[m, 4] + g * (LF[m + 1, 4] - LF[m, 4])
            Tj = 1. + jit * np.random.standard_normal(); Aj = 1. + shim * np.random.standard_normal()
            new = False
        if ph < te:
            s = -np.exp(al * (ph - te)) * np.sin(np.pi * ph / tp) / np.sin(np.pi * te / tp)
            op = np.sin(np.pi * ph / te)
        else:
            s = -(np.exp(-eps * (ph - te)) - np.exp(-eps * (1 - te))) / (eps * ta)
            op = 0.
        s = s * (ee[k] + fk * (ee[k + 1] - ee[k])) * Aj
        ph += f * T * Tj
        if ph >= 1.: ph -= 1.; new = True
        lpv += alp * (s - lpv)
        nz = np.random.standard_normal()
        asl += .35 * (nz - asl)
        x = lpv + (nz - .6 * asl) * (asp[k] + fk * (asp[k + 1] - asp[k])) * (.35 + .65 * op)
        for q in range(2):
            v = zA[q] * x + zB[q] * x1[q] + zC[q] * x2[q]
            x2[q] = x1[q]; x1[q] = x
            y = pA[q] * v + pB[q] * w1[q] + pC[q] * w2[q]
            w2[q] = w1[q]; w1[q] = y
            x = y
        for j in range(nf):
            y = A_[j] * x + B_[j] * y1[j] + C_[j] * y2[j]
            y2[j] = y1[j]; y1[j] = y
            x = y
        out[i] = x
    return out


# ---- phones --------------------------------------------------------------------------------------------------------------
# female F1 F2 F3, then male.  Standard Hindi: a is a short central vowel, au a long open o, ai an open e.
VOWELS = dict(
    a=((720, 1560, 2850), (600, 1370, 2450)), aa=((880, 1400, 2850), (720, 1220, 2500)),
    i=((440, 2350, 3050), (390, 2000, 2600)), ii=((340, 2700, 3300), (290, 2280, 2950)),
    u=((440, 1050, 2750), (390, 980, 2350)), uu=((370, 900, 2700), (310, 830, 2300)),
    e=((460, 2450, 3050), (405, 2100, 2650)), ai=((690, 2080, 2850), (590, 1800, 2480)),
    o=((480, 950, 2750), (430, 880, 2400)), au=((720, 1110, 2780), (600, 960, 2420)),
)
# consonants: dur, voicing, aspiration, frication (gain, lo, hi), F1 and F2 locus (female Hz, pull), F3, nasal zeros, low-pass of the voice bar
CONS = dict(
    k=dict(d=.08, av=0, burst=(1.1, 1300, 2700, .028), asp=.035, loc=(250, None, .0), stop=1),
    g=dict(d=.075, av=.22, burst=(.9, 1200, 2400, .022), loc=(250, None, 0), vlp=350, stop=1),
    gh=dict(d=.085, av=.24, burst=(1.0, 1200, 2400, .026), asp=.085, breathy=1, loc=(250, None, 0), vlp=350, stop=1),
    b=dict(d=.065, av=.22, burst=(.22, 400, 1800, .01), loc=(250, 900, .55), vlp=350, stop=1),
    d=dict(d=.06, av=.22, burst=(.3, 2800, 6000, .012), loc=(250, 1850, .45), vlp=350, stop=1),
    j=dict(d=.09, av=.22, burst=(.85, 2300, 5800, .052), loc=(260, 2300, .3), vlp=380, stop=1),
    jh=dict(d=.095, av=.22, burst=(.85, 2300, 5800, .055), asp=.06, breathy=1, loc=(260, 2300, .3), vlp=380, stop=1),
    ch=dict(d=.115, av=0, burst=(1.15, 2400, 6000, .072), asp=.015, loc=(260, 2300, .3), stop=1),
    s=dict(d=.12, av=0, fric=(.36, 5200, 9500), loc=(320, 1850, .45)),
    h=dict(d=.07, av=.25, asp=.02, aspc=.10, loc=None),
    m=dict(d=.10, av=.7, loc=(290, 1000, .3), nz=(520, 1050), nas=1, tt=.035),
    n=dict(d=.09, av=.65, loc=(290, 1700, .3), nz=(560, 1750), nas=1, tt=.035),
    ng=dict(d=.09, av=.5, loc=(300, 2100, .5), nz=(540, 3200), nas=1),
    l=dict(d=.10, av=.5, loc=(340, 1550, .25), F3=3000, nz=(None, 2150), tt=.03),
    r=dict(d=.038, av=.45, loc=(420, 1600, .55), F3=2150, tt=.03),
    v=dict(d=.07, av=.45, loc=(310, 900, .3), vlp=1800),
    y=dict(d=.08, av=.65, loc=(310, 2500, .1)),
)
SYL = dict(
    ek='- e k', lau='l au -', ja='j a -', lii='l ii -', mi='m i -', van='v a n', cha='ch a -', sang='s a ng', bu='b u -', jhii='jh ii -',
    jaa='j aa -', gii='g ii -', raa='r aa -', ma='m a -', raam='r aa m', naam='n aa m', si='s i -', yaa='y aa -', ghar='gh a r', man='m a n',
    aa='- aa -', ii='- ii -', hum='m a m', oo='- o -', uu='- uu -', au='- au -', e='- e -', a='- a -', haa='h aa -', ha='h a -', ho='h o -', he='h e -', hau='h au -', mm='m m -',
)


class Singer:
    """kind f (woman), m (man), c (child). tract scales every formant; rd is the resting glottal shape (low = pressed)."""
    def __init__(s, kind='f', tract=1., rd=1.15, breath=.012, vib=(5.2, 26), jit=.0035, shim=.025, drift=5., glide=1., ring=0., seed=0):
        s.__dict__.update(locals()); del s.__dict__['s']
        s.mi = 1 if kind == 'm' else 0
        s.sc = tract * (1.17 if kind == 'c' else 1.)

    def vowel(s, v): return np.array(VOWELS[v][s.mi], float) * s.sc

    def high(s):
        if s.kind == 'm': f = [3250, 3800, 4650, 5600, 6600, 7650, 8700, 9800, 10900]
        else: f = [3950, 4800, 5750, 6900, 8050, 9200, 10400, 11600, 12800]
        f = np.array(f, float)
        if s.ring: f[0] -= s.ring * 400; f[1] -= s.ring * 550
        return f * s.sc

    # -- pitch ------------------------------------------------------------------------------------------
    def pitch(s, nts, t0, n, r, scale=(0, 204, 386, 702, 884)):
        """Cents above 100 Hz on the control grid, from [(t0, t1, hz, flags, vel, newsyllable)]."""
        t = t0 + np.arange(n) * CT
        c = [cents(x[2], 100.) for x in nts]
        y = np.full(n, c[0])
        add = np.zeros(n)
        for i, (a, b, _, fl, vel, syl) in enumerate(nts):
            m = t >= a - .4 if i == 0 else t >= a
            y[m] = c[i]
        for i in range(1, len(nts)):
            a = nts[i][0]; gap = a - nts[i - 1][1]
            d = abs(c[i] - c[i - 1]) / 100
            L = np.clip(.07 + .016 * d, .06, .24) * s.glide * (1. if not nts[i][5] else .8)
            L = min(L, .7 * (nts[i][1] - a), .7 * (nts[i - 1][1] - nts[i - 1][0]))
            if gap > .2: L = min(L, .09)
            lead = .75 if nts[i][5] else .5
            u = np.clip((t - (a - lead * L)) / L, 0, 1)
            m = (t > a - lead * L - 1e-9) & (t < a + (1 - lead) * L)
            y[m] = c[i - 1] + (c[i] - c[i - 1]) * (.5 - .5 * np.cos(np.pi * u[m]))
        for i, (a, b, f, fl, vel, syl) in enumerate(nts):
            u = t - a
            D = b - a
            if '^' in fl or 'v' in fl:
                from_sa = cents(f, 293.6648) % 1200
                sc = [x + o for o in (-1200, 0, 1200) for x in scale]
                k = min([x for x in sc if x > from_sa + 60]) if '^' in fl else max([x for x in sc if x < from_sa - 60])
                add += (k - from_sa) * np.exp(-.5 * ((u - .035) / .034) ** 2) * (u > -.15)
            if '~' in fl: add += 45 * np.sin(2 * np.pi * 3.1 * u) * np.clip(u / .25, 0, 1) * np.clip((b - t) / .15, 0, 1) * (u > 0) * (t < b)
            if 'w' in fl: add += 130 * np.sin(2 * np.pi * 5.6 * u) * np.clip(u / .12, 0, 1) * np.clip((b - t) / .1, 0, 1) * (u > 0) * (t < b)
            if D > .45 and '~' not in fl and 'w' not in fl:
                w = np.clip((u - .28) / .5, 0, 1) * np.clip((b - t) / .12, 0, 1) * (t < b)
                rate = s.vib[0] * (1 + .04 * r.standard_normal())
                add += s.vib[1] * w * np.sin(2 * np.pi * rate * u + r.uniform(0, 1.))
        a = nts[0][0]
        add -= 90 * np.exp(-np.clip(t - a + .03, 0, 9) / .045)
        m = int(n * CT * 3) + 4
        dr = np.interp(np.linspace(0, m - 2, n), np.arange(m), r.standard_normal(m)) * s.drift
        for i in range(1, len(nts)):                # a note reached by leap overshoots a little, then settles
            u = t - nts[i][0]
            add += .07 * np.clip(c[i] - c[i - 1], -500, 500) * np.where(u > 0, np.exp(-u / .06) * np.sin(2 * np.pi * np.clip(u, 0, 1) / .22), 0)
        return gaussian_filter1d(y, 6) + add + gaussian_filter1d(dr, 40)

    # -- one phrase ----------------------------------------------------------------------------------------
    def sing(s, syls, seed=0, attack=.07, release=.16, gain=1., breathin=0., raga=(0, 204, 386, 702, 884), cons=1., raw=False):
        """syls = [(name, [(t0, t1, hz, flags, vel), ...])] contiguous notes inside a syllable -> (mono, start second)."""
        r = rng('sing', s.kind, s.seed, seed)
        ph = []                                  # (start, end, kind, name, vowel of the syllable)
        for i, (name, nt) in enumerate(syls):
            on, v, co = SYL[name].split()
            a, b = nt[0][0], nt[-1][1]
            nxt = syls[i + 1] if i + 1 < len(syls) else None
            end = b
            if nxt is not None and nxt[1][0][0] - b < .03:
                o2 = SYL[nxt[0]].split()[0]
                if o2 != '-': end = nxt[1][0][0] - CONS[o2]['d'] * cons
            if on != '-': ph.append((a - CONS[on]['d'] * cons, a, 'C', on, v, 1))
            if co != '-':
                d = CONS[co]['d'] * cons * (1.25 if co in ('m', 'n', 'ng') else 1)
                if co in ('m', 'n', 'ng') and end - a > .5: d = min(.28, .35 * (end - a))
                ph.append((a, end - d, 'V', v, v, 0)); ph.append((end - d, end, 'C', co, v, 0))
            else: ph.append((a, end, 'V', v, v, 0))
        t0 = ph[0][0] - .25; t1 = ph[-1][1] + .45
        n = int((t1 - t0) / CT) + 2
        t = t0 + np.arange(n) * CT
        nts = [x[:5] + (j == 0,) for _, nt in syls for j, x in enumerate(nt)]
        f0 = 100 * 2 ** (s.pitch(nts, t0, n, r, raga) / 1200)
        # formants
        kt, kF = [], []
        kz1, kz2 = [], []
        av = np.zeros(n); asp = np.full(n, 0.); brd = np.zeros(n); vlp = np.full(n, 20000.)
        fric = []
        zp1, zp2 = 270. * s.sc, 2000. * s.sc
        def key(tt, F): kt.append(tt); kF.append(F)
        msc = .86 if s.mi else 1.
        for i, (a, b, kd, p, v, onset) in enumerate(ph):
            Fv = s.vowel(v if v in VOWELS else 'a')
            prev_gap = i == 0 or a - ph[i - 1][1] > .02
            next_gap = i == len(ph) - 1 or ph[i + 1][0] - b > .02
            mk = (t >= a) & (t < b)
            if kd == 'V' and p in VOWELS:
                L = min(CONS[ph[i - 1][3]].get('tt', .055) if i and ph[i - 1][2] == 'C' else .055, (b - a) * .35)
                L2 = min(CONS[ph[i + 1][3]].get('tt', .055) if i + 1 < len(ph) and ph[i + 1][2] == 'C' else .055, (b - a) * .35)
                F0_, F1_ = Fv, Fv
                if p == 'au': F0_, F1_ = Fv * np.array([1.04, 1.06, 1]), Fv * np.array([.93, .95, 1])
                if p == 'e': F1_ = Fv * np.array([.96, 1.02, 1])
                key(a + L, F0_); key(max(b - L2, a + L + .001), F1_)
                av[mk] = 1.
                if prev_gap: av[(t > a - .02) & (t <= a)] = 1.
            else:
                q = CONS[p if p in CONS else 'm']
                loc = q.get('loc')
                if loc is None: Fc = Fv.copy()
                else:
                    f1 = loc[0] * msc * s.sc
                    f2 = Fv[1] * 1.12 if loc[1] is None else loc[1] * msc * s.sc + loc[2] * (Fv[1] - loc[1] * msc * s.sc)
                    f3 = q.get('F3', 0) * msc * s.sc or (f2 + 340 if loc[1] is None else Fv[2])
                    if q.get('stop'): f1 = f1 + .12 * (Fv[0] - f1)
                    Fc = np.array([f1, f2, f3])
                key(a + .004, Fc); key(b - .002, Fc)
                av[mk] = q['av']
                vlp[mk] = q.get('vlp', 20000.)
                if 'nz' in q:
                    z = q['nz']
                    if z[0]: kz1.append((a, b, z[0] * s.sc))
                    if z[1]: kz2.append((a, b, z[1] * s.sc * (msc if s.mi else 1)))
                if 'fric' in q: fric.append((a + .005, b + .005, q['fric'], 'f'))
                if 'burst' in q:
                    g, lo, hi, d = q['burst']
                    if q.get('stop') and d > .03: fric.append((b - d, b, (g, lo, hi), 'b'))
                    else: fric.append((b - .012, b - .012 + d, (g, lo, hi), 'b'))
                if 'asp' in q:
                    m = (t >= b - .01) & (t < b + q['asp'])
                    asp[m] = .10 if not q.get('breathy') else .14
                    if not q['av']: av[(t >= b - .004) & (t < b + q['asp'] * .6)] = 0.
                    if q.get('breathy'): brd[(t >= b - .01) & (t < b + q['asp'] + .05)] = .9
                if 'aspc' in q: asp[mk] = q['aspc']; brd[mk] = 1.
        kt = np.array(kt); kF = np.array(kF)
        o = np.argsort(kt, kind='stable'); kt, kF = kt[o], kF[o]
        F = np.empty((n, NF)); B = np.empty((n, NF))
        for j in range(3): F[:, j] = gaussian_filter1d(np.interp(t, kt, kF[:, j]), 5)
        hi = s.high()
        for j in range(3, NF): F[:, j] = hi[j - 3]
        wob = [wander(n * 48, 2.2, r)[::48][:n] for _ in range(3)]
        for j in range(3): F[:, j] *= 1 + .008 * wob[j]
        F[:, 0] = np.maximum(F[:, 0], f0 * 1.04)
        F[:, 1] = np.maximum(F[:, 1], F[:, 0] + 220)
        F[:, 2] = np.maximum(F[:, 2], F[:, 1] + 320)
        F[:, 3] = np.maximum(F[:, 3], F[:, 2] + 300); F[:, 4] = np.maximum(F[:, 4], F[:, 3] + 300); F[:, 5] = np.maximum(F[:, 5], F[:, 4] + 300)
        nas = np.zeros(n)
        z1 = np.full(n, zp1); z2 = np.full(n, zp2); p2 = np.full(n, zp2)
        for a, b, z in kz1:
            z1[(t >= a) & (t < b)] = z; nas[(t >= a) & (t < b)] = 1
        for a, b, z in kz2:
            m = (t >= a - .03) & (t < b + .03); p2[m] = z * 1.0
            z2[m] = z * 1.0
            m = (t >= a) & (t < b); p2[m] = z * 1.45
        z1 = gaussian_filter1d(z1, 14); z2 = gaussian_filter1d(z2, 5); p2 = gaussian_filter1d(p2, 9)
        nas = gaussian_filter1d(nas, 20)
        B[:, 0] = 60 + .10 * f0 + 60 * nas + 60 * (asp > .05)
        B[:, 1] = 75 + .02 * F[:, 1] + 90 * nas
        B[:, 2] = 110 + .02 * F[:, 2] + 90 * nas
        for j in range(3, NF): B[:, j] = 140 + 55 * (j - 3) + .03 * hi[j - 3]
        # loudness: phrase arc, note velocity, swells on long notes
        vel = np.full(n, nts[0][4] * 1.)
        sw = np.zeros(n)
        for a, b, f, fl, ve, ns_ in nts:
            m = (t >= a - .03) & (t < b)
            vel[m] = ve
            if b - a > .4:
                u = np.clip((t[m] - a) / (b - a), 0, 1)
                sw[m] = 1.6 * np.sin(np.pi * u ** .8) - 1.2 * np.clip(u - .8, 0, 1) * 5 * .6
        vel = gaussian_filter1d(vel, 45); sw = gaussian_filter1d(sw, 60)
        a0, b1 = ph[0][0], ph[-1][1]
        ramp = np.clip((t - a0) / attack, 0, 1) if not CONS.get(ph[0][3], {}).get('stop') else np.clip((t - a0 + .02) / .02, 0, 1)
        gate = ramp * np.clip((b1 + release * .3 - t) / release, 0, 1) ** 1.3
        for i in range(1, len(ph)):               # rests inside the phrase
            g0, g1 = ph[i - 1][1], ph[i][0]
            if g1 - g0 > .02:
                d = min(.1, (g1 - g0) * .7)
                m = (t >= g0) & (t < g1)
                at = min(attack, .09) if ph[i][2] == 'V' else .02
                gate[m] *= np.maximum(np.clip(1 - (t[m] - g0) / d, 0, 1), np.clip(1 - (g1 - t[m]) / at, 0, 1))
                av[m] = np.maximum(av[m], 1.)
        av[t < a0] = av[min(max(int((a0 - t0) / CT) + 1, 0), n - 1)]; av[t >= b1] = 1.
        av = gaussian_filter1d(av, 5)
        ee = av * vel * db(sw) * gaussian_filter1d(gate, 8)
        rd = s.rd + .55 * (1 - vel) + brd + .5 * (1 - np.clip(gate, 0, 1)) - .03 * sw
        rd = np.clip(gaussian_filter1d(rd, 8), .36, 2.65)
        vg = np.clip(gaussian_filter1d(gate, 8), 0, 1)
        asp = gaussian_filter1d(asp, 5) * np.clip(vel, .3, 1) + s.breath * vel ** .5 * vg * (av > .4) + .25 * s.breath * vg
        vlp = np.exp(gaussian_filter1d(np.log(vlp), 6))
        N = int(n * CT * SR) * OS
        y = _cascade(N, f0, ee, rd, asp, F, B, z1, np.full(n, zp1), z2, p2, vlp, s.jit, s.shim, int(r.integers(1 << 30)), LF, SR * OS * 1., SR * OS * CT)
        y = signal.resample_poly(y, 1, OS) * .30
        for a, b, (g, lo, hi_), kd in fric:
            m = ns(b - a)
            x = bp(r.standard_normal(m + 400), lo * (1 if not s.mi else .9), hi_)[400:]
            e = np.ones(m)
            if kd == 'f': e = np.minimum(1, np.minimum(np.arange(m) / ns(.03), (m - np.arange(m)) / ns(.03)))
            else: e = np.minimum(1, np.arange(m) / ns(.0015)) * np.exp(-np.arange(m) / (m * .45)) * np.clip((m - np.arange(m)) / ns(.006), 0, 1)
            i = ns(a - t0); j = min(i + m, len(y))
            k = int((b - t0) / CT)
            y[i:j] += (.28 * g * e * x)[:j - i] * vel[min(k, n - 1)]
        y = hp(y, 70)
        if breathin:
            m = ns(.42); x = r.standard_normal(m)
            e = np.sin(np.pi * np.linspace(0, 1, m) ** 1.6) ** 2
            b = (bp(x, 900, 2200) + .7 * bp(x, 3200, 6500) + .3 * bp(x, 300, 700)) * e * .05 * breathin
            i = ns(a0 - t0 - .46)
            if i < 0: y = np.concatenate([np.zeros(-i), y]); t0 += i / SR; i = 0
            y[i:i + m] += b
        y = y * gain
        return (y, t0, f0, t) if raw else (y, t0)


def lyric(text, start, sa=293.6648, pulse=PULSE):
    """'ek=S:1+G:1 lau=P:2 _:1' from a film frame -> syllables for Singer.sing. A token without '=' continues the last syllable."""
    out, f = [], float(start)
    for tok in text.replace('|', ' ').split():
        name, _, body = tok.partition('=')
        if not body: name, body = None, tok
        nt = []
        for p in body.split('+'):
            m = _TOK.match(p)
            if not m: raise ValueError(p)
            L = float(m['l'] or 1) * pulse
            if m['d'][0] != '_': nt.append((sec(f), sec(f + L), hz(m['d'], sa), m['f'] or '', float(m['v'] or 1)))
            f += L
        if name: out.append((name, nt))
        elif nt: out[-1][1].extend(nt)
    return out


LEAD = Singer('f', 1.0, rd=1.15, breath=.016, vib=(5.3, 38), glide=1.25, drift=7, seed=1)
LEADM = Singer('m', 1.0, rd=1.0, breath=.010, vib=(5.0, 26), ring=.6, glide=1.1, seed=2)
CHOIR = 1.5                   # scales every choir's head count
CHILD = Singer('c', 1.0, rd=1.3, breath=.022, vib=(5.6, 8), jit=.006, drift=9, glide=.8, seed=3)


def solo(L, singer, syls, g=1., p=0., **k):
    y, t0 = singer.sing(syls, **k)
    L.add(y, t0, g, p)


def phrases(syls, gap=.12):
    """Split at rests so long lines render as separate breaths."""
    out, cur = [], []
    for s in syls:
        if cur and s[1][0][0] - cur[-1][1][-1][1] > gap: out.append(cur); cur = []
        cur.append(s)
    return out + [cur] if cur else out


def choir(L, syls, kind='m', n=10, seed=0, octave=0, spread=.9, loose=.018, rd=1.0, g=1., vib=20, tune=8., scoop=0, **k):
    """n separate singers: own tract, timing, tuning, vibrato and place on the stage."""
    n = int(round(n * CHOIR))
    r = rng('choir', kind, n, seed)
    for i in range(n):
        s = Singer(kind, float(np.clip(1 + .035 * r.standard_normal(), .92, 1.08)), rd=rd + .18 * r.standard_normal(), breath=.014, vib=(5.2 + .45 * r.standard_normal(), vib * r.uniform(.5, 1.5)),
                   jit=.004, shim=.03, drift=8, ring=.5 if kind == 'm' else 0, glide=r.uniform(.8, 1.2), seed=1000 + i + 100 * seed)
        c = 2 ** (tune * r.standard_normal() / 1200 + octave)
        dt = loose * r.standard_normal() + .004
        sy = [(nm, [(a + dt, b + dt, f * c, fl, v) for a, b, f, fl, v in nt]) for nm, nt in syls]
        for j, part in enumerate(phrases(sy)):
            y, t0 = s.sing(part, seed=j, **k)
            L.add(y, t0, g * r.uniform(.75, 1.1) / np.sqrt(n), spread * (2 * (i + .5) / n - 1))


def warm():
    Singer().sing([('lau', [(0, .3, 300., '', 1.)])])
