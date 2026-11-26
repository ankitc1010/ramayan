"""Garlands: string(st, points (k,3), r=flower radius, cols=(even, odd, every ninth))."""
import numpy as np
from lau.stage import Fig
from lau.cloth import spline
COL = dict(marigold=('#f28a14', '#f7b52a', '#e8e0c8'), rose=('#d8304a', '#f0657a', '#fff0e0'), jasmine=('#fff6e6', '#f2e2cc', '#f28a14'))
_F = {}


def string(st, P, r=.28, col='marigold', gap=1.55, M=None):
    P = np.asarray(P, float); d = np.linalg.norm(np.diff(P, axis=0), axis=1).sum(); n = int(min(64, max(3, d / (r * gap)))); Q = spline(P, 240); s = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(Q, axis=0), axis=1))]); u = np.linspace(0, s[-1], n); G = np.stack([np.interp(u, s, Q[:, k]) for k in range(3)], 1)
    if col not in _F:
        a, b, c = COL[col]; dk = lambda h: '#' + ''.join('%02x' % int(int(h[i:i + 2], 16) * k) for i, k in ((1, .52), (3, .40), (5, .45))); _F[col] = Fig('garland', 'garland.glsl', {11: (a, dk(a), 1), 12: (b, dk(b), 1), 13: (c, dk(c), 1)}, human=False, step=.9, bound=(0, 0, 0, 5))
    ctr = G.mean(0); R = np.linalg.norm(G - ctr, axis=1).max() + r * 1.4; pr = np.zeros(16, 'f4'); pr[0], pr[1] = r, n
    return st.fig(_F[col], M=M, u=dict(G=np.vstack([G, np.zeros((64 - n, 3))]).astype('f4'), pr=pr, bound=(*ctr, R)))
