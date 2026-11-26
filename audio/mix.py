"""Stems -> soundtrack.  Level riding by measured loudness per passage, real silences, ducking, limiter, 24-bit files.
Every gain is applied to the stems, so the five stems add up exactly to the soundtrack."""
import numpy as np
from numba import njit
from scipy import signal
from scipy.ndimage import minimum_filter1d, maximum_filter1d
from core import *

STEMS = ('voice', 'melodic', 'drums', 'pads', 'sfx')
TRIM = dict(voice=0., melodic=0., drums=-.5, pads=3., sfx=2.)             # overall stem balance, dB
EQ = dict(voice=((5500, 2.5, .7, 'high'),), melodic=((4200, 3., .7, 'high'), (250, -1., .8)), drums=((75, -2., .7, 'low'), (3600, 4., .7, 'high')), pads=((300, -1.5, .8), (3800, 3., .7, 'high')), sfx=((3500, 2., .7, 'high'), (60, -1., .7, 'low')))
TARGET = -15.                                                             # integrated LUFS
CEIL = -2.0                                                               # dBTP

# (shot, frame, LUFS): how loud each passage should sit before mastering. Each holds until the next entry.
LEVELS = [
    ('a1', 0, -32), ('a1', 24, -27), ('a2', 0, -23), ('a3', 0, -20), ('a3', 24, -16.5), ('a4', 0, -20), ('a4', 48, -17), ('a4', 84, -13), ('a5', 6, -21),
    ('b1', 0, -15), ('b1', 36, -27), ('b2', 0, -25), ('b3', 0, -19), ('b4', 0, -26),
    ('c1', 0, -22), ('c2', 0, -18), ('c2', 36, -20), ('c3', 0, -23), ('c3', 18, -19), ('c4', 0, -22), ('c4', 36, -17.5), ('c5', 0, -18), ('c5', 24, -13.5), ('c6', 0, -14.5), ('c6', 60, -17), ('c6', 72, -22), ('c7', 0, -26),
    ('d1', 0, -33), ('d1', 42, -28), ('d2', 0, -21), ('d2', 42, -17.5), ('d3', 0, -16.5), ('d3', 42, -11.5), ('d4', 0, -12.5), ('d4', 108, -15), ('d5', 0, -25), ('d6', 0, -23), ('d7', 0, -21), ('d7', 30, -18), ('d7', 66, -15), ('d8', 0, -11.8), ('d8', 126, -17), ('d8', 147, -21),
    ('e1', 0, -19), ('e1', 42, -23), ('e1', 84, -15), ('e2', 0, -13.5),
    ('f1', 0, -21), ('f1', 36, -18), ('f1', 72, -14.5), ('f2', 0, -14), ('f2', 36, -11), ('f3', 0, -15), ('f3', 48, -13.5), ('f3', 66, -13), ('f3', 78, -11.5), ('f4', 0, -19), ('f4', 30, -12.5), ('f4', 46, -29), ('f5', 0, -17), ('f5', 48, -14), ('f6', 0, -26), ('f7', 0, -14), ('f7', 48, -12), ('f8', 0, -19), ('f8', 48, -14.5), ('f8', 78, -11.5), ('f8', 96, -33), ('f9', 0, -11.5), ('f9', 72, -10.5), ('f9', 88, -14), ('f10', 4, -29),
    ('g1', 0, -24), ('g2', 0, -20), ('g3', 0, -16.5), ('g4', 0, -15), ('g4', 60, -13.5), ('g4', 84, -12.5), ('g4', 108, -15), ('g5', 0, -23), ('g5', 48, -25), ('g5', 90, -27), ('g5', 120, -27),
]
# (shot, first silent frame, shot, first sounding frame, fade-out frames, stems that stay)
HUSH = [
    ('a1', 0, 'a1', 1, .1, ()),
    ('a4', 79, 'a4', 84, 3., ()),
    ('c4', 91.5, 'c5', 0, 2., ('sfx',)),
    ('c7', 72, 'd1', 1, 26., ()),
    ('f8', 96, 'f8', 104, 1.2, ()), ('f8', 104, 'f9', 0, .02, ('sfx',)),
    ('f9', 95, 'f10', 1, 10., ()),
]


def tf(shot, f): return (film.START[shot] + f) * FR


def riding(mix):
    """Gain curve in dB, and a report [(frame, target, measured, gain)]."""
    pts, rep = [], []
    seg = [(tf(s, f), t) for s, f, t in LEVELS] + [(TOTAL, None)]
    for (a, t), (b, _) in zip(seg[:-1], seg[1:]):
        x = mix[a:b]
        m = integrated(x) if b - a >= ns(.45) else float(lu(kpower(x, (b - a) / SR, 1)[0]))
        g = float(np.clip(t - m, -14, 8 if t > -30 else 2)) if m > -60 else 0.
        rep.append((a / FR, t, round(m, 1), round(g, 1)))
        w = min(ns(.08), (b - a) // 3)
        if pts: pts.append((a - w, pts[-1][1]))
        pts.append((a, g)); pts.append((b - 1, g))
    x, y = zip(*sorted(pts))
    g = np.interp(np.arange(TOTAL), x, y)
    k = np.hanning(ns(.05)); k /= k.sum()
    return signal.oaconvolve(np.pad(g, ns(.025), 'edge'), k, 'same')[ns(.025):-ns(.025)], rep


def hush_curves():
    out = {s: np.ones(TOTAL, np.float32) for s in STEMS}
    for s0, f0, s1, f1, fade, keep in HUSH:
        a, b = int(tf(s0, f0)), int(tf(s1, f1)); w = max(16, int(fade * FR))
        u = np.arange(w) / w
        for s in STEMS:
            if s in keep: continue
            c = out[s]
            i = max(a - w, 0)
            c[i:a] *= (.5 + .5 * np.cos(np.pi * u))[w - (a - i):]
            c[a:b] = 0
            c[b:b + 144] *= np.linspace(0, 1, 144)
    e = np.ones(TOTAL, np.float32)
    a, b = tf('g5', 144), tf('g5', 167)
    e[a:b] = (.5 + .5 * np.cos(np.pi * np.arange(b - a) / (b - a))) ** 2; e[b:] = 0
    for s in STEMS: out[s] *= e
    return out


def envelope(x, att=.02, rel=.25):
    p = np.sqrt(np.maximum((x ** 2).sum(1), 1e-12))
    p = maximum_filter1d(p, ns(.01))
    d = 96
    q = p[::d]
    q = smooth_ar(q, att * SR / d, rel * SR / d)
    return np.interp(np.arange(len(p)), np.arange(len(q)) * d, q)


@njit(cache=True)
def smooth_ar(x, a, r):
    y = np.empty_like(x); s = 0.
    ka, kr = 1 - np.exp(-1 / a), 1 - np.exp(-1 / r)
    for i in range(len(x)):
        s += (ka if x[i] > s else kr) * (x[i] - s); y[i] = s
    return y


@njit(cache=True)
def _release(g, k):
    s = 1.
    for i in range(len(g)):
        s = g[i] if g[i] < s else s + k * (g[i] - s)
        g[i] = s
    return g


def truepeak(x):
    """Per-sample true peak (4x oversampled), worst channel."""
    h = signal.firwin(96, 1 / 4, window=('kaiser', 8.)) * 4
    pk = np.abs(x).max(1)
    for c in range(x.shape[1]):
        for ph in range(4):
            y = signal.oaconvolve(x[:, c], h[ph::4])[12:12 + len(x)]
            pk = np.maximum(pk, np.abs(y))
    return pk


def limiter(x, ceil):
    pk = truepeak(x)
    g = np.minimum(1, db(ceil) / np.maximum(pk, 1e-9))
    L = ns(.004)
    g = minimum_filter1d(g, 2 * L + 1)
    g = _release(g.copy(), 1 - np.exp(-1 / (.09 * SR)))
    g = minimum_filter1d(g, L)
    k = np.hanning(L + 2)[1:-1]; k /= k.sum()
    g = np.minimum(signal.oaconvolve(np.pad(g, L, 'edge'), k, 'same')[L:-L], 1)
    return g


def master(stems, quiet=False):
    """stems: dict of full-length stereo arrays -> (dict of final stems, mix, report)."""
    for s in STEMS:
        x = stems[s] * db(TRIM[s])
        for e in EQ[s]: x = peq(x, *e)
        m, d = (x[:, 0] + x[:, 1]) / 2, hp((x[:, 0] - x[:, 1]) / 2, 110, 2)          # one low end, in the middle
        stems[s] = hp(np.stack([m + d, m - d], 1), 24, 2)
    v = envelope(stems['voice']); ref = np.percentile(v[v > v.max() * .05], 60) if v.max() > 0 else 1
    duck = np.clip(v / ref, 0, 1) ** .7
    dr = envelope(stems['drums'], .004, .18); dref = np.percentile(dr, 97) + 1e-9
    dd = np.clip(dr / dref, 0, 1) ** 1.2
    stems['melodic'] = stems['melodic'] * db(-2.2 * duck)[:, None]
    stems['pads'] = stems['pads'] * db(-2.8 * duck - 1.5 * dd)[:, None]
    stems['sfx'] = stems['sfx'] * db(-1.5 * duck)[:, None]
    hc = hush_curves()
    g, rep = riding(sum(stems[s] * hc[s][:, None] for s in STEMS))
    for s in STEMS:
        stems[s] = stems[s] * (db(g) * hc[s])[:, None]
    mix = sum(stems[s] for s in STEMS)
    G = db(TARGET - integrated(mix))
    for _ in range(5):
        lg = limiter(mix * G, CEIL)
        out = mix * G * lg[:, None]
        e = TARGET - integrated(out)
        if abs(e) < .05: break
        G *= db(e)
    for s in STEMS: stems[s] = (stems[s] * G * lg[:, None])
    return stems, out, dict(riding=rep, gain=20 * np.log10(G), limit=20 * np.log10(lg.min()), lg=lg)
