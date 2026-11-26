"""Fire, sparks, smoke, petals, rain, trails of light.  All deterministic functions of time."""
import numpy as np, math
import moderngl as mgl
from . import gl, W, H
from .stage import hexc
from .rig import V, nz
KIND = dict(ember=0, streak=1, petal=2, leaf=3, ash=4, glint=5, smoke=6, tongue=7, rain=8, feather=9, ring=10, dot=11, spark=12, flake=13, drop=14, lamp=15)
_q = None


def particles(st, pos, size, col, kind='ember', rot=0., seed=None, vel=None, alpha=1., space='world', soft=0., blend='over', fog=0., fogCol=(0, 0, 0)):
    """instanced billboards over the canvas (depth-tested against the last close()).  pos Nx3 world, or Nx2 pixels with space='px'.  col: hex / rgb / Nx3.  vel (Nx3): stretches the quad along it"""
    global _q
    c = gl.ctx(); p = gl.program('part.frag', vs='part.vert'); pos = np.asarray(pos, float); n = len(pos)
    if n == 0: return
    if pos.shape[1] == 2: pos = np.c_[pos, np.zeros(n)]; space = 'px'
    D = np.zeros((n, 14), 'f4'); D[:, 0:3] = pos; D[:, 3] = size; D[:, 4] = rot; D[:, 5] = KIND[kind] if isinstance(kind, str) else kind; D[:, 6] = np.arange(n) * .6180 % 1 if seed is None else seed
    col = np.asarray(hexc(col) if isinstance(col, (str, tuple)) else col, float); D[:, 7:10] = col; D[:, 10] = alpha
    if vel is not None: v = np.asarray(vel, float); D[:, 11:11 + v.shape[-1]] = v
    if _q is None: _q = c.buffer(np.array([-1, -1, 1, -1, -1, 1, 1, 1], 'f4').tobytes())
    vb = c.buffer(D.tobytes()); vao = c.vertex_array(p, [(_q, '2f', 'q'), (vb, '3f 4f 4f 3f/i', 'pos', 'a', 'col', 'vel')])
    st.C.use(); c.viewport = (0, 0, st.pw, st.ph); gl.set_uniforms(p, {**st.base_u(), 'space': 1 if space == 'px' else 0, 'soft': float(soft), 'fogD': float(fog), 'fogC': hexc(fogCol)}); gl.bind(p, dict(tZ=st.L.color_attachments[1]))
    c.enable(mgl.BLEND); c.blend_func = (mgl.ONE, mgl.ONE_MINUS_SRC_ALPHA) if blend == 'over' else (mgl.ONE, mgl.ONE)
    vao.render(mgl.TRIANGLE_STRIP, vertices=4, instances=n); c.disable(mgl.BLEND); vao.release(); vb.release()


def ribbon(st, P, width, mode='fire', col=(1, 1, 1), col2=(1, 1, 1), seed=0., amt=1., space='world', soft=0., blend='over'):
    """camera-facing strip along P (world Nx3 or pixel Nx2): mode fire, light, smoke, brush, wind, gold, bolt.  width = half width (world units or px), scalar or per point"""
    c = gl.ctx(); p = gl.program('strip.frag', vs='strip.vert'); P = np.asarray(P, float); k = len(P)
    if k < 2: return
    if P.shape[1] == 2: space = 'px'; P = np.c_[P, np.zeros(k)]
    w = np.broadcast_to(np.interp(np.linspace(0, 1, k), np.linspace(0, 1, np.size(width)), np.atleast_1d(width)) if np.size(width) > 1 else float(width), (k,)); T = np.gradient(P, axis=0)
    if space == 'px': N = np.stack([-T[:, 1], T[:, 0], np.zeros(k)], 1); wpx = w
    else:
        E = st.cam.eye - P; N = np.cross(T, E); wpx = w * np.array([st.cam.px(q) for q in P])
    N /= np.linalg.norm(N, axis=1, keepdims=True) + 1e-9; s = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))]); Lw = s[-1] / max(1e-6, float(np.mean(w)))
    A = np.zeros((k * 2, 7), 'f4'); A[0::2, :3] = P - N * w[:, None]; A[1::2, :3] = P + N * w[:, None]; u = s / max(s[-1], 1e-9)
    A[0::2, 3] = u; A[1::2, 3] = u; A[0::2, 4] = -1; A[1::2, 4] = 1; A[0::2, 5] = wpx; A[1::2, 5] = wpx; A[:, 6] = Lw
    vb = c.buffer(A.tobytes()); vao = c.vertex_array(p, [(vb, '3f 4f', 'ip', 'iuv')]); st.C.use(); c.viewport = (0, 0, st.pw, st.ph)
    m = dict(fire=0, light=1, smoke=2, brush=3, wind=4, gold=5, bolt=6)[mode]
    gl.set_uniforms(p, {**st.base_u(), 'space': 1 if space == 'px' else 0, 'mode': m, 'seed': float(seed), 'amt': float(amt), 'soft': float(soft), 'colA': hexc(col), 'colB': hexc(col2)}); gl.bind(p, dict(tZ=st.L.color_attachments[1]))
    c.enable(mgl.BLEND); c.blend_func = (mgl.ONE, mgl.ONE_MINUS_SRC_ALPHA) if blend == 'over' else (mgl.ONE, mgl.ONE); vao.render(mgl.TRIANGLE_STRIP); c.disable(mgl.BLEND); vao.release(); vb.release()


def flame(st, at, h, w=None, lean=0., seed=0., amt=1., glow=1., calm=1., tint=(1, 1, 1)):
    """a lamp flame; at = world point (3) or pixel (2) of the wick; h = height in world units or pixels"""
    if len(at) == 3: x, y, z = st.cam.project(at); h = h * st.cam.px(at)
    else: x, y = at
    st.paint('flame.frag', 'over', base=(float(x), float(y)), ht=float(h), wd=float(w if w else h * .42), lean=float(lean), seed=float(seed), amt=float(amt), glow=float(glow), calm=float(calm), tint=hexc(tint))
    return x, y, h


def embers(st, n, box, t, rise=2.2, size=.06, seed=0, col='#ffb04a', life=2.6, swirl=.6, wind=(0, 0, 0), kind='ember'):
    """a steady stream of sparks inside box = ((x0,y0,z0),(x1,y1,z1))"""
    r = np.random.default_rng(seed); a, b = np.array(box, float); p0 = r.uniform(a, b, (n, 3)); ph = r.uniform(0, 1, n); k = r.uniform(.5, 1.4, n); lf = (t / life * k + ph) % 1.
    P = p0 + np.c_[swirl * np.sin(lf * 7 + ph * 40) * lf, lf * rise * life * k, swirl * np.cos(lf * 6 + ph * 33) * lf] + np.asarray(wind, float) * (lf * life)[:, None]
    particles(st, P, size * k * (1 - lf) ** .5, col, kind, seed=ph, alpha=np.minimum(1, lf * 8) * (1 - lf) ** .7)


def burst(st, n, at, t, speed=6., grav=5., size=.08, seed=0, col='#ffd27a', life=1.1, kind='streak', spread=(1, 1, 1), up=0., stretch=.09, drag=1.4):
    """particles thrown from a point at t=0"""
    if t < 0 or t > life * 1.4: return
    r = np.random.default_rng(seed); d = r.normal(size=(n, 3)); d /= np.linalg.norm(d, axis=1, keepdims=True); d = d * np.asarray(spread, float) + V(0, up, 0); sp = speed * r.uniform(.25, 1., n)[:, None]; lf = life * r.uniform(.5, 1.3, n)
    g = (1 - math.exp(-drag * t)) / drag; P = np.asarray(at, float) + d * sp * g + V(0, -grav, 0) * t * t * .5; v = d * sp * math.exp(-drag * t) + V(0, -grav, 0) * t; al = np.clip(1 - t / lf, 0, 1)
    particles(st, P, size * (.5 + .5 * al), col, kind, seed=r.uniform(0, 1, n), vel=v * stretch if kind in ('streak', 'rain') else None, alpha=al, rot=r.uniform(0, 6, n) + t * r.uniform(-5, 5, n))


def drift(st, n, box, t, kind='petal', size=.2, col='#f2a0b0', fall=1., sway=.8, seed=0, spin=2., wind=(0, 0, 0), col2=None, alpha=1.):
    """things that fall for ever: petals, leaves, ash, feathers, snow"""
    r = np.random.default_rng(seed); a, b = np.array(box, float); ext = b - a; p0 = r.uniform(0, 1, (n, 3)); k = r.uniform(.6, 1.4, n); ph = r.uniform(0, 6.28, n)
    P = p0 * ext + np.asarray(wind, float) * t * k[:, None]; P[:, 1] -= fall * t * k; P[:, 0] += sway * np.sin(t * 1.7 * k + ph); P[:, 2] += sway * .6 * np.cos(t * 1.3 * k + ph * 2); P = a + np.mod(P, ext)
    c = np.array(hexc(col)) if col2 is None else np.array(hexc(col)) * (1 - p0[:, :1]) + np.array(hexc(col2)) * p0[:, :1]
    particles(st, P, size * k, c, kind, rot=ph + t * spin * (k - 1) * 3, seed=ph, alpha=alpha)
