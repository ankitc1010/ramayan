"""Time, pitch, filters, rooms, loudness and the layer/part machinery everything else is built on.

A Part is one stem of one act. It holds Layers (one instrument line each). A layer is levelled by measured
K-weighted loudness, not by guessed gains, then placed in synthetic rooms."""
import os
for _k in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMBA_NUM_THREADS'): os.environ.setdefault(_k, '1')
import re, sys, pathlib, functools
import numpy as np
from numba import njit
from scipy import signal

ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))
import film

SR = 48000
FR = SR // 24
TOTAL = film.N * FR
PULSE = film.PULSE
ACT0 = {a: film.START[a.lower() + '1'] for a in film.ACTS}
ACT1 = {a: min([v for v in list(ACT0.values()) + [film.N] if v > ACT0[a]]) for a in ACT0}


def fr(shot, f=0):
    """Film frame of frame f of a shot."""
    return film.START[shot] + f


def sec(frame): return frame / 24.


def rng(*seed):
    h = 2166136261
    for c in repr(seed).encode(): h = ((h ^ c) * 16777619) & 0xffffffff
    return np.random.default_rng(h)


# ---- pitch ---------------------------------------------------------------------------------------------
SA = 293.6648
JUST = dict(S=1., r=16/15, R=9/8, g=6/5, G=5/4, m=4/3, M=45/32, P=3/2, d=8/5, D=5/3, n=9/5, N=15/8)


def hz(deg, sa=SA):
    """'P' 'D,' 'S'' -> Hz.  A comma lowers, an apostrophe raises an octave."""
    return sa * JUST[deg[0]] * 2. ** (deg.count("'") - deg.count(','))


def cents(a, b): return 1200 * np.log2(np.maximum(a, 1e-9) / b)


_TOK = re.compile(r"^(?P<d>[SrRgGmMPdDnN_][',]*)(?P<f>[~^vw]*)(?::(?P<l>[\d.]+))?(?:@(?P<v>[\d.]+))?$")


def notes(text, start, pulse=PULSE, sa=SA):
    """'S:1 G:1 P~:2 _:1' -> [(t0, t1, hz, flags, vel)] in seconds; start is a film frame, lengths are pulses.
    Flags: ~ long slow shake, ^ touched from above, v touched from below, w gamak."""
    out, f = [], float(start)
    for tok in text.replace('|', ' ').split():
        m = _TOK.match(tok)
        if not m: raise ValueError(tok)
        n = float(m['l'] or 1) * pulse
        if m['d'][0] != '_': out.append((sec(f), sec(f + n), hz(m['d'], sa), m['f'] or '', float(m['v'] or 1)))
        f += n
    return out


# ---- small signal tools ----------------------------------------------------------------------------------
def ns(t): return int(round(t * SR))
def db(x): return 10. ** (x / 20.)
def white(n, r): return r.standard_normal(int(n)).astype(np.float64)


def env(pts, n):
    """Piecewise-linear envelope; pts = [(seconds, value)]."""
    t, v = zip(*pts)
    return np.interp(np.arange(n) / SR, t, v)


def expenv(n, tau, attack=.001):
    t = np.arange(n) / SR
    return np.exp(-t / tau) * np.minimum(1, t / max(attack, 1e-5))


def fades(x, a=.005, b=.02):
    x = np.array(x, dtype=np.float64)
    na, nb = min(ns(a), len(x)), min(ns(b), len(x))
    s = (slice(None),) + (None,) * (x.ndim - 1)
    if na: x[:na] *= (.5 - .5 * np.cos(np.pi * np.arange(na) / na))[s]
    if nb: x[-nb:] *= (.5 + .5 * np.cos(np.pi * np.arange(nb) / nb))[s]
    return x


def hp(x, f, o=2): return signal.sosfilt(signal.butter(o, f, 'high', fs=SR, output='sos'), x, axis=0)
def lp(x, f, o=2): return signal.sosfilt(signal.butter(o, min(f, SR * .49), 'low', fs=SR, output='sos'), x, axis=0)
def bp(x, a, b, o=2): return signal.sosfilt(signal.butter(o, (a, min(b, SR * .49)), 'band', fs=SR, output='sos'), x, axis=0)


def peq(x, f, g, q=.8, kind='peak'):
    """One parametric biquad: peak, low shelf or high shelf, g in dB."""
    A, w = 10 ** (g / 40), 2 * np.pi * f / SR
    al, c = np.sin(w) / (2 * q), np.cos(w)
    if kind == 'peak': b, a = [1 + al * A, -2 * c, 1 - al * A], [1 + al / A, -2 * c, 1 - al / A]
    else:
        s, k = (1 if kind == 'low' else -1), 2 * np.sqrt(A) * al
        b = [A * ((A + 1) - s * (A - 1) * c + k), s * 2 * A * ((A - 1) - s * (A + 1) * c), A * ((A + 1) - s * (A - 1) * c - k)]
        a = [(A + 1) + s * (A - 1) * c + k, -s * 2 * ((A - 1) + s * (A + 1) * c), (A + 1) + s * (A - 1) * c - k]
    return signal.lfilter(np.array(b) / a[0], np.array(a) / a[0], x, axis=0)


def smooth(x, t):
    """Two-pass one-pole smoothing of a control signal, t seconds."""
    a = np.exp(-1 / max(t * SR, 1e-9))
    y = signal.lfilter([1 - a], [1, -a], x, zi=[x[0] * a])[0]
    return signal.lfilter([1 - a], [1, -a], y[::-1], zi=[y[-1] * a])[0][::-1]


def wander(n, rate, r, octaves=2):
    """Smooth random signal, unit-ish amplitude, `rate` turns per second."""
    y = np.zeros(n)
    for k in range(octaves):
        m = int(n / SR * rate * 2 ** k) + 4
        y += np.interp(np.linspace(0, m - 3.001, n), np.arange(m), r.standard_normal(m)) / 2 ** k
    w = max(3, int(SR / rate / 6))
    return signal.lfilter([1 - np.exp(-1 / w)], [1, -np.exp(-1 / w)], y)


@njit(cache=True, fastmath=True)
def modal(f, a, tau, ph, n, g):
    """Sum of decaying partials.  g: per-sample pitch factor (length n) or length 1 for none."""
    y = np.zeros(n)
    w0 = 2 * np.pi / 48000.
    for k in range(len(f)):
        if f[k] >= 21000 or a[k] == 0: continue
        d = np.exp(-1. / (tau[k] * 48000.)); A = a[k]
        if len(g) < n:
            c, s = np.cos(w0 * f[k]), np.sin(w0 * f[k])
            x, z = np.sin(ph[k]), np.cos(ph[k])
            for i in range(n):
                y[i] += A * x
                x, z = (x * c + z * s) * d, (z * c - x * s) * d
                if A * (abs(x) + abs(z)) < 1e-7: break
        else:
            p, e = ph[k], A
            for i in range(n):
                y[i] += e * np.sin(p)
                p += w0 * f[k] * g[i]; e *= d
                if e < 1e-7: break
    return y


@njit(cache=True, fastmath=True)
def svf_sweep(x, f, q, mode):
    """State-variable filter with per-sample cutoff. mode 0 low, 1 band, 2 high."""
    y = np.empty_like(x)
    a = b = 0.
    for i in range(len(x)):
        g = np.tan(np.pi * min(f[i], 22000.) / 48000.)
        k = 1. / q
        h = 1. / (1. + g * (g + k))
        v3 = x[i] - b
        v1 = h * a + g * h * v3
        v2 = b + g * v1
        a = 2 * v1 - a; b = 2 * v2 - b
        y[i] = v2 if mode == 0 else (v1 * k if mode == 1 else x[i] - k * v1 - v2)
    return y


def sweep(x, f, q=1., mode='band'):
    f = np.broadcast_to(np.asarray(f, dtype=np.float64), x.shape).copy()
    return svf_sweep(np.asarray(x, dtype=np.float64), f, float(q), dict(low=0, band=1, high=2)[mode])


def pan(x, p):
    """Mono to stereo, equal power, p in -1..1."""
    a = (np.clip(p, -1, 1) + 1) * np.pi / 4
    return np.stack([x * np.cos(a), x * np.sin(a)], 1) * 1.0


def wide(x, r, amt=.5, spread=.012):
    """Mono to decorrelated stereo with short diffuse tails (early reflections of a big source)."""
    n = ns(spread)
    h = np.stack([r.standard_normal(n) * np.exp(-np.arange(n) / (n / 4)) for _ in range(2)], 1)
    h /= np.sqrt((h ** 2).sum(0))
    w = np.stack([signal.fftconvolve(x, h[:, c])[:len(x)] for c in (0, 1)], 1)
    return (1 - amt) * x[:, None] + amt * w


# ---- rooms -------------------------------------------------------------------------------------------------
# name: (seconds at 125 500 2k 8k, predelay ms, early reflections, early level, high cut)
ROOMS = dict(
    close=((.25, .25, .22, .15), 2, 10, .9, 12000),
    theatre=((.7, .75, .65, .4), 7, 14, .8, 9000),
    hall=((2.6, 2.4, 1.9, .9), 24, 18, .45, 9000),
    cathedral=((5.2, 4.8, 3.4, 1.3), 42, 16, .25, 7500),
    open=((.9, 1.3, 1.1, .5), 60, 7, .5, 6000),
    stone=((1.6, 1.7, 1.4, .7), 14, 20, .7, 9000),
    cave=((4.2, 3.6, 2.2, .7), 30, 14, .35, 5000),
)


@functools.lru_cache(None)
def room_ir(name):
    t60, pre, ne, el, hc = ROOMS[name]
    r = rng('room', name)
    n = ns(max(t60) * 1.1)
    t = np.arange(n) / SR
    fb = np.array([62, 125, 250, 500, 1000, 2000, 4000, 8000, 16000.])
    T = np.interp(np.log2(fb), np.log2([125, 500, 2000, 8000]), t60)
    h = np.zeros((n, 2))
    F = np.fft.rfftfreq(n, 1 / SR)
    lf = np.log2(np.maximum(F, 20) / fb[0])
    for k in range(len(fb)):
        w = np.clip(1 - abs(lf - k), 0, 1)
        if k == 0: w = np.where(lf < 0, 1, w)
        w = np.sin(w * np.pi / 2)
        for c in (0, 1):
            x = np.fft.irfft(np.fft.rfft(r.standard_normal(n)) * w, n)
            h[:, c] += x * np.exp(-6.91 * t / T[k])
    h *= (1 - np.exp(-t / (.004 + pre * 3e-4)))[:, None]
    e = np.zeros((n, 2))
    for k in range(ne):
        d = ns((.15 + (k + r.random()) / ne) * (pre + 9) * 2.2e-3)
        g = r.choice([-1, 1]) * np.exp(-2.2 * k / ne)
        p = r.uniform(-.95, .95)
        e[d, 0] += g * np.cos((p + 1) * np.pi / 4); e[d, 1] += g * np.sin((p + 1) * np.pi / 4)
    e = lp(e, 7000, 1)
    h /= np.sqrt((h ** 2).sum() / 2); e /= np.sqrt((e ** 2).sum() / 2)
    h = np.concatenate([np.zeros((ns(pre / 1000), 2)), h]); e = np.pad(e, ((0, len(h) - n), (0, 0)))
    h = h * np.sqrt(1 - el ** 2) + e * el
    h = lp(hp(h, 90, 2), hc, 1)
    return h / np.sqrt((h ** 2).sum() / 2)


def reverb(x, name):
    h = room_ir(name)
    return np.stack([signal.oaconvolve(x[:, c], h[:, c]) for c in (0, 1)], 1)


# ---- loudness (ITU-R BS.1770) -----------------------------------------------------------------------------------
_K1 = signal.tf2sos([1.53512485958697, -2.69169618940638, 1.19839281085285], [1, -1.69065929318241, .73248077421585])
_K2 = signal.tf2sos([1., -2., 1.], [1, -1.99004745483398, .99007225036621])
_KS = np.concatenate([_K1, _K2])


def kpower(x, win=.4, hop=.1):
    """Mean K-weighted power (both channels summed) per window."""
    x = x if x.ndim == 2 else np.stack([x, x], 1) * .7071
    y = signal.sosfilt(_KS, x, axis=0)
    c = np.concatenate([[0], np.cumsum((y ** 2).sum(1))])
    w, h = ns(win), ns(hop)
    i = np.arange(0, max(1, len(x) - w + 1), h)
    return (c[np.minimum(i + w, len(x))] - c[i]) / w


def lu(p): return -.691 + 10 * np.log10(np.maximum(p, 1e-12))


def integrated(x):
    p = kpower(x)
    p = p[lu(p) > -70]
    if not len(p): return -120.
    g = p[lu(p) > lu(p.mean()) - 10]
    return float(lu(g.mean()))


def momentary_max(x):
    if len(x) < ns(.4): x = np.concatenate([x, np.zeros((ns(.4) - len(x),) + x.shape[1:])])
    return float(lu(kpower(x, .4, .02).max()))


# ---- dead stops: whatever began before the frame is cut there, reverberation included (seconds of fade) ------------------
CUTS = [(fr('a4', 79), .08), (fr('b1', 36), .03), (fr('c4', 91.5), .06), (fr('c7', 72), .2), (fr('d3', 37), .12), (fr('f1', 70.5), .04), (fr('f4', 42), .35), (fr('f8', 96), .03), (fr('f9', 95), .01), (fr('g5', 88), .1)]


def cut(x, start):
    """Truncate audio x beginning at sample `start` at the first dead stop it would cross."""
    for f, d in CUTS:
        c = int(f * FR) - start
        if 1.3 * FR < c < len(x):
            m = min(ns(d), len(x) - c)
            y = np.array(x[:c + m]); y[c:] *= (.5 + .5 * np.cos(np.pi * np.arange(m) / m)).reshape((-1,) + (1,) * (x.ndim - 1))
            return y
    return x


# ---- layers and parts -----------------------------------------------------------------------------------------------
class Layer:
    """One instrument line. lufs: gated loudness of the dry layer; mom: max momentary instead. sends: {room: amount}."""
    def __init__(self, part, name, lufs=None, mom=None, sends=None, p=0., low=None, high=None, eq=(), dry=1., fx=None):
        self.part, self.name, self.lufs, self.mom, self.sends, self.p = part, name, lufs, mom, sends or {}, p
        self.low, self.high, self.eq, self.dry, self.fx = low, high, eq, dry, fx
        self.b = np.zeros((part.n, 2))

    def add(self, x, t, g=1., p=None):
        """Add mono or stereo x starting at absolute second t."""
        x = cut(np.asarray(x), ns(t))
        if x.ndim == 1: x = pan(x, self.p if p is None else p)
        i = ns(t) - self.part.s0
        a, b = max(i, 0), min(i + len(x), self.part.n)
        if b > a: self.b[a:b] += g * x[a - i:b - i]
        return self

    def at(self, x, frame, g=1., p=None): return self.add(x, sec(frame), g, p)

    def render(self):
        b = self.b
        if self.low: b = hp(b, self.low)
        if self.high: b = lp(b, self.high)
        for e in self.eq: b = peq(b, *e)
        if self.fx: b = self.fx(b)
        if self.lufs is not None: b = b * db(np.clip(self.lufs - integrated(b), -80, 80))
        elif self.mom is not None: b = b * db(np.clip(self.mom - momentary_max(b), -80, 80))
        return b


class Part:
    """One stem over frames f0..f1 plus a tail."""
    def __init__(self, f0, f1, tail=7., pre=0):
        self.s0 = max(0, (f0 - pre) * FR)
        self.n = min(TOTAL, f1 * FR + ns(tail)) - self.s0
        self.layers = []

    def layer(self, name, **k):
        self.layers.append(Layer(self, name, **k)); return self.layers[-1]

    def stops(self): return [(int(f * FR) - self.s0, d) for f, d in CUTS if 0 < int(f * FR) - self.s0 < self.n]

    def finish(self):
        out, sends, info = np.zeros((self.n, 2)), {}, {}
        for L in self.layers:
            b = L.render()
            info[L.name] = round(integrated(b), 1)
            out += b * L.dry
            for k, g in L.sends.items(): sends[k] = sends.get(k, 0) + b * g
        stops = [0] + [c + ns(d) for c, d in self.stops()] + [self.n]          # what is fading out must not feed the room afterwards
        for k, s in sends.items():
            for a, b in zip(stops[:-1], stops[1:]):
                if not s[a:b].any(): continue
                w = cut(reverb(s[a:b], k), self.s0 + a)[:self.n - a]
                out[a:a + len(w)] += w
        return out.astype(np.float32), info


def write_wav(path, x, bits=24):
    import wave
    x = np.clip(x, -1, 1 - 2 ** -23)
    d = np.round(x * (2 ** 23 - 1)).astype('<i4')
    raw = np.frombuffer(d.tobytes(), np.uint8).reshape(-1, 4)[:, :3].tobytes()
    with wave.open(str(path), 'wb') as w:
        w.setnchannels(x.shape[1]); w.setsampwidth(3); w.setframerate(SR); w.writeframes(raw)


def read_wav(path):
    import wave
    with wave.open(str(path), 'rb') as w:
        assert w.getsampwidth() == 3
        raw = np.frombuffer(w.readframes(w.getnframes()), np.uint8).reshape(-1, 3)
        d = np.zeros((len(raw), 4), np.uint8); d[:, 1:] = raw
        return (d.view('<i4').reshape(-1, w.getnchannels()) / 2 ** 31)
