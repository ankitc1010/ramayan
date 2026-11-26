"""Painted plates: cairo paintings cached on disk and uploaded once."""
import os, hashlib, numpy as np, cairo, math
from . import CACHE, gl
_T = {}


def plate(key, w, h, fn, ver=1, mip=True):
    """texture of a w x h painting fn(cairo context); cached in cache/<key>.npy (bump ver to repaint)"""
    k = f'{key}_{w}x{h}_v{ver}'
    if k in _T: return _T[k]
    p = os.path.join(CACHE, k + '.npy')
    if os.path.exists(p): a = np.load(p)
    else:
        sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h); fn(cairo.Context(sf)); sf.flush(); a = np.ndarray((h, w, 4), np.uint8, sf.get_data()).copy()
        tmp = p + '.%d.npy' % os.getpid(); np.save(tmp, a); os.replace(tmp, p)
    t = gl.tex_from(a, mip=mip); t.swizzle = 'BGRA'; _T[k] = t
    return t


def rgb(h, a=None):
    h = h.lstrip('#'); c = tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return c if a is None else (*c, a)


def poly(c, P, close=True):
    c.move_to(*P[0]); [c.line_to(*q) for q in P[1:]]
    if close: c.close_path()


def smooth_path(P, n=10, close=False):
    """Catmull-Rom through P"""
    P = np.asarray(P, float); Q = np.vstack([P[-1], P, P[0], P[1]]) if close else np.vstack([2 * P[0] - P[1], P, 2 * P[-1] - P[-2]]); m = len(P) if close else len(P) - 1; out = []
    for i in range(m):
        a, b, c, d = Q[i], Q[i + 1], Q[i + 2], Q[i + 3]; u = np.linspace(0, 1, n, endpoint=False)[:, None]; out.append(.5 * (2 * b + (c - a) * u + (2 * a - 5 * b + 4 * c - d) * u ** 2 + (-a + 3 * b - 3 * c + d) * u ** 3))
    if not close: out.append(P[-1:])
    return np.vstack(out)


def ink(c, P, w, col='#140a12', taper=(.3, .4), alpha=1., seed=0):
    """a pen stroke with swelling width along P (k,2)"""
    P = np.asarray(P, float); d = np.gradient(P, axis=0); n = np.stack([-d[:, 1], d[:, 0]], 1); n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-9; u = np.linspace(0, 1, len(P)); k = np.ones(len(P))
    if taper[0] > 0: k = np.minimum(k, (u / taper[0]) ** .6)
    if taper[1] > 0: k = np.minimum(k, ((1 - u) / taper[1]) ** .6)
    r = np.random.default_rng(seed); wob = np.interp(u, np.linspace(0, 1, 7), r.uniform(.75, 1.2, 7)); ww = (w * .5 * np.clip(k, .08, 1) * wob)[:, None]
    A = np.vstack([P + n * ww, (P - n * ww)[::-1]]); c.set_source_rgba(*rgb(col), alpha); poly(c, A); c.fill()


def blob(c, P, col, alpha=1., line=0., lcol='#140a12', n=8):
    Q = smooth_path(P, n, True); poly(c, Q); c.set_source_rgba(*rgb(col), alpha)
    if line > 0: c.fill_preserve(); c.set_source_rgba(*rgb(lcol), 1); c.set_line_width(line); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke()
    else: c.fill()
