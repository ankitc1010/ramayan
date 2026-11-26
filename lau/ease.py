"""Timing: keyframes, easings, springs, deterministic noise."""
import numpy as np, math


def clamp(x, a=0., b=1.): return max(a, min(b, x))
def lerp(a, b, t): return a + (b - a) * t
def smooth(a, b, x): t = clamp((x - a) / (b - a) if b != a else float(x >= b)); return t * t * (3 - 2 * t)
def smoother(a, b, x): t = clamp((x - a) / (b - a)); return t * t * t * (t * (6 * t - 15) + 10)
def ease_in(t, p=2.): return clamp(t) ** p
def ease_out(t, p=2.): return 1 - (1 - clamp(t)) ** p
def ease_io(t, p=2.): t = clamp(t); return .5 * (2 * t) ** p if t < .5 else 1 - .5 * (2 - 2 * t) ** p
def back_out(t, s=1.7): t = clamp(t) - 1; return t * t * ((s + 1) * t + s) + 1
def elastic(t, k=3.2, f=2.4): t = clamp(t); return 1 - math.exp(-k * 2 * t) * math.cos(f * 6.283 * t)
def impulse(t, k=8.): return 0. if t < 0 else k * t * math.exp(1 - k * t)
def decay(t, k=6.): return 0. if t < 0 else math.exp(-k * t)
def on2(f): return f // 2 * 2
def on3(f): return f // 3 * 3


def keys(f, K, mode='smooth'):
    """K: [(frame, value[, ease])]; values: number, tuple, or anything with .mix(other, t) (Pose, Face).  ease: smooth, linear, in, out, io, back, step, snap"""
    if f <= K[0][0]: return K[0][1]
    if f >= K[-1][0]: return K[-1][1]
    for a, b in zip(K, K[1:]):
        if a[0] <= f < b[0]:
            t = (f - a[0]) / (b[0] - a[0]); e = b[2] if len(b) > 2 else mode
            t = {'smooth': lambda t: t * t * (3 - 2 * t), 'linear': lambda t: t, 'in': lambda t: t ** 2.2, 'out': lambda t: 1 - (1 - t) ** 2.2, 'io': lambda t: ease_io(t, 2.6), 'back': back_out, 'step': lambda t: 0., 'snap': lambda t: 1 - (1 - t) ** 5}[e](t)
            x, y = a[1], b[1]
            if isinstance(x, str) or e == 'step': return x if t < 1 else y
            if hasattr(x, 'mix'): return x.mix(y, t)
            if isinstance(x, (tuple, list, np.ndarray)): return tuple((1 - t) * np.asarray(x, float) + t * np.asarray(y, float))
            return x + (y - x) * t


def noise1(x, seed=0):
    i = math.floor(x); f = x - i; f = f * f * (3 - 2 * f)
    h = lambda n: math.modf(abs(math.sin((n + seed * 57.31) * 127.1) * 43758.5453))[0] * 2 - 1
    return h(i) * (1 - f) + h(i + 1) * f


def shake(f, amt=1., freq=.5, seed=0):
    """camera shake offset (x, y) for frame f"""
    return amt * noise1(f * freq, seed), amt * noise1(f * freq, seed + 9)
