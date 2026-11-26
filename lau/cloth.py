"""Ribbons, sashes, capes, banners: follow-through without simulation (deterministic, any frame on its own), or a Verlet strip simulated in setup()."""
import numpy as np, math
from .rig import V, nz


def spline(P, n):
    """Catmull-Rom through points P (k,3) -> (n,3)"""
    P = np.asarray(P, float); k = len(P); Q = np.vstack([2 * P[0] - P[1], P, 2 * P[-1] - P[-2]])
    t = np.linspace(0, k - 1 - 1e-6, n); i = np.floor(t).astype(int); u = (t - i)[:, None]; a, b, c, d = Q[i], Q[i + 1], Q[i + 2], Q[i + 3]
    return .5 * (2 * b + (c - a) * u + (2 * a - 5 * b + 4 * c - d) * u ** 2 + (-a + 3 * b - 3 * c + d) * u ** 3)


def lag(anchor, t, n=14, length=6., delay=.05, wind=(0, 0, 0), grav=.9, wave=.35, freq=2.2, phase=0., stiff=.0, dirn=(0, 0, 0)):
    """points of a ribbon whose root is anchor(t) (world): each point remembers where the root was a little earlier, falls, blows and waves"""
    seg = length / (n - 1); P = []; wind = np.asarray(wind, float); dirn = np.asarray(dirn, float)
    side = nz(np.cross(wind + dirn + V(0, -1e-3, 0), V(0, 1, .01)))
    for i in range(n):
        u = i / (n - 1); a = np.asarray(anchor(t - i * delay), float)
        P.append(a + (wind * u + dirn * u * (1 - stiff * u)) * length + V(0, -1, 0) * grav * length * u ** 1.25 + side * wave * u * length * .22 * math.sin(freq * 6.283 * t - u * 5.2 + phase) + V(0, 1, 0) * wave * u * length * .10 * math.sin(freq * 5.1 * t - u * 6.5 + phase * 1.7))
    P = np.array(P); Q = [P[0]]                     # keep the length
    for i in range(1, n): d = P[i] - Q[-1]; Q.append(Q[-1] + nz(d) * seg)
    return np.array(Q)


def strip(P, width, up=(0, 1, 0), m=5, curl=.0, twist=0., n=None):
    """surface along the curve P (k,3): width scalar or per-point array, `up` = direction the cloth's width runs (per curve or per point)"""
    P = np.asarray(P, float)
    if n: P = spline(P, n)
    k = len(P); T = np.gradient(P, axis=0); T /= np.linalg.norm(T, axis=1, keepdims=True) + 1e-9
    U = np.broadcast_to(np.asarray(up, float), (k, 3)).copy(); U -= T * (U * T).sum(1, keepdims=True); U /= np.linalg.norm(U, axis=1, keepdims=True) + 1e-9
    N = np.cross(T, U)
    if np.ndim(twist) or twist:
        a = (np.linspace(0, 1, k) * twist if not np.ndim(twist) else np.asarray(twist))[:, None]; U, N = U * np.cos(a) + N * np.sin(a), N * np.cos(a) - U * np.sin(a)
    w = (np.interp(np.linspace(0, 1, k), np.linspace(0, 1, np.size(width)), np.atleast_1d(width)) if np.size(width) > 1 else np.full(k, float(width)))[:, None]; v = np.linspace(-1, 1, m); pos = []; nrm = []; uv = []
    for j, s in enumerate(v):
        pos.append(P + U * w * s * .5 + N * w * curl * (s * s - .4)); nn = N - U * 2 * curl * s * 2; nrm.append(nn / np.linalg.norm(nn, axis=1, keepdims=True)); uv.append(np.stack([np.linspace(0, 1, k), np.full(k, s * .5 + .5)], 1))
    pos = np.array(pos).transpose(1, 0, 2).reshape(-1, 3); nrm = np.array(nrm).transpose(1, 0, 2).reshape(-1, 3); uv = np.array(uv).transpose(1, 0, 2).reshape(-1, 2)
    i = np.arange(k - 1)[:, None] * m + np.arange(m - 1)[None]; a = i.reshape(-1); idx = np.concatenate([np.stack([a, a + 1, a + m], 1), np.stack([a + 1, a + m + 1, a + m], 1)])
    return pos, nrm, uv, idx


def tube(P, r, m=10, n=None):
    """round rope / tail along P; r scalar or per point"""
    P = np.asarray(P, float)
    if n: P = spline(P, n)
    k = len(P); r = np.broadcast_to(np.interp(np.linspace(0, 1, k), np.linspace(0, 1, np.size(r)), np.atleast_1d(r)) if np.size(r) > 1 else r, (k,))
    T = np.gradient(P, axis=0); T /= np.linalg.norm(T, axis=1, keepdims=True) + 1e-9; u = nz(np.cross(T[0], V(.31, .95, .12))); pos, nrm, uv = [], [], []
    for i in range(k):
        u = u - T[i] * (u @ T[i]); u = nz(u); v = np.cross(T[i], u); a = np.linspace(0, 2 * math.pi, m); ring = np.cos(a)[:, None] * u + np.sin(a)[:, None] * v
        pos.append(P[i] + ring * r[i]); nrm.append(ring); uv.append(np.stack([np.full(m, i / (k - 1)), a / (2 * math.pi)], 1))
    i = np.arange(k - 1)[:, None] * m + np.arange(m - 1)[None]; a = i.reshape(-1); idx = np.concatenate([np.stack([a, a + m, a + 1], 1), np.stack([a + 1, a + m, a + m + 1], 1)])
    return np.array(pos).reshape(-1, 3), np.array(nrm).reshape(-1, 3), np.array(uv).reshape(-1, 2), idx


def sheet(fn, nu=24, nv=16):
    """surface from fn(u,v)->xyz on the unit square"""
    u = np.linspace(0, 1, nu); v = np.linspace(0, 1, nv); G = np.array([[fn(a, b) for b in v] for a in u], float)
    du = np.gradient(G, axis=0); dv = np.gradient(G, axis=1); N = np.cross(du, dv); N /= np.linalg.norm(N, axis=2, keepdims=True) + 1e-9
    uv = np.stack(np.meshgrid(u, v, indexing='ij'), -1); i = np.arange(nu - 1)[:, None] * nv + np.arange(nv - 1)[None]; a = i.reshape(-1)
    return G.reshape(-1, 3), N.reshape(-1, 3), uv.reshape(-1, 2), np.concatenate([np.stack([a, a + nv, a + 1], 1), np.stack([a + 1, a + nv, a + nv + 1], 1)])
