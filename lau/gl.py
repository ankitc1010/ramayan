"""OpenGL plumbing: one headless context, shader loading with #include, full-screen passes, render targets."""
import os, re, hashlib, numpy as np
from . import ROOT, W, H
import moderngl as mgl

_ctx = None
VS = '#version 430\nin vec2 p; out vec2 uv; void main(){uv=p*.5+.5; gl_Position=vec4(p,0,1);}'
DIRS = ['lau/glsl', 'chars', 'worlds', 'shots']


def ctx():
    global _ctx
    if _ctx is None:
        _ctx = mgl.create_context(standalone=True, require=430, backend='egl')
        _ctx.gc_mode = 'auto'
    return _ctx


def source(name):
    """GLSL text of a file name (searched in DIRS) or of literal source, with #include expanded once each"""
    seen = set()

    def load(n):
        if '\n' in n or '{' in n: return n
        for d in DIRS:
            p = os.path.join(ROOT, d, n)
            if os.path.exists(p): return open(p).read()
        raise FileNotFoundError(n)

    def expand(s):
        def sub(m):
            n = m.group(1)
            if n in seen: return ''
            seen.add(n)
            return expand(load(n))
        return re.sub(r'^[ \t]*#include[ \t]+"([^"]+)"[^\n]*$', sub, s, flags=re.M)
    s = expand(load(name))
    s = re.sub(r'^\s*#version[^\n]*\n', '', s, flags=re.M)
    return '#version 430\n' + s


_progs = {}


def program(fs, vs=VS, defs=''):
    key = hashlib.md5((vs + '|' + fs + '|' + defs).encode()).hexdigest()
    if key not in _progs:
        src = source(fs)
        if defs: src = src.replace('#version 430\n', '#version 430\n' + defs + '\n', 1)
        v = vs if '\n' in vs else source(vs)
        try:
            _progs[key] = ctx().program(vertex_shader=v, fragment_shader=src)
        except mgl.Error as e:
            lines = src.split('\n'); msg = str(e)
            for m in sorted({int(x) for x in re.findall(r'0\((\d+)\)', msg)})[:6]:
                msg += '\n' + '\n'.join('%4d %s' % (i + 1, lines[i]) for i in range(max(0, m - 2), min(len(lines), m + 1)))
            raise RuntimeError((fs if '\n' not in fs else 'inline') + '\n' + msg) from None
    return _progs[key]


_quad = None
_vaos = {}


def quad(prog):
    global _quad
    if _quad is None: _quad = ctx().buffer(np.array([-1, -1, 1, -1, -1, 1, 1, 1], 'f4'))
    k = id(prog)
    if k not in _vaos: _vaos[k] = ctx().vertex_array(prog, [(_quad, '2f', 'p')])
    return _vaos[k]


def set_uniforms(prog, u):
    for k, v in u.items():
        if k not in prog: continue
        m = prog[k]
        if isinstance(v, np.ndarray):
            if v.ndim >= 2 and m.dimension in (9, 16): v = np.swapaxes(v, -1, -2)      # numpy rows -> GLSL columns
            b = np.ascontiguousarray(v, 'f4').tobytes(); need = m.dimension * m.array_length * 4
            m.write(b[:need] if len(b) > need else b + bytes(need - len(b)))
        elif isinstance(v, (list, tuple)): m.value = tuple(float(x) for x in v) if not isinstance(v[0], (list, tuple, np.ndarray)) else [tuple(float(y) for y in x) for x in v]
        else: m.value = v


def bind(prog, texs, start=0):
    """texs: {'uniform': texture}"""
    for i, (k, t) in enumerate(texs.items()):
        if k in prog and t is not None:
            t.use(start + i); prog[k].value = start + i


def draw(prog, target, u=None, texs=None, blend=None, viewport=None):
    c = ctx(); target.use()
    c.viewport = viewport or (0, 0, target.width, target.height)
    if u: set_uniforms(prog, u)
    if texs: bind(prog, texs)
    if blend == 'over': c.enable(mgl.BLEND); c.blend_func = (mgl.ONE, mgl.ONE_MINUS_SRC_ALPHA)
    elif blend == 'add': c.enable(mgl.BLEND); c.blend_func = (mgl.ONE, mgl.ONE)
    else: c.disable(mgl.BLEND)
    quad(prog).render(mgl.TRIANGLE_STRIP)
    c.disable(mgl.BLEND)


class RT:
    """a colour target (one or several textures, optional depth)"""

    def __init__(self, w, h, n=1, dtype='f2', comps=4, depth=False, filt='linear'):
        c = ctx(); self.w, self.h = w, h; self.width, self.height = w, h
        self.tex = [c.texture((w, h), comps, dtype=dtype) for _ in range(n)]
        for t in self.tex:
            t.repeat_x = t.repeat_y = False
            t.filter = (mgl.LINEAR, mgl.LINEAR) if filt == 'linear' else (mgl.NEAREST, mgl.NEAREST)
        self.depth = c.depth_texture((w, h)) if depth else None
        self.fbo = c.framebuffer(self.tex, self.depth)

    def use(self): self.fbo.use()

    def clear(self, *v, depth=1.0):
        self.fbo.use(); self.fbo.clear(*(v or (0, 0, 0, 0)), depth=depth)

    def __getitem__(self, i): return self.tex[i]

    def read(self, comps=3, dtype='f2', i=0):
        a = np.frombuffer(self.fbo.read(components=comps, attachment=i, dtype=dtype), {'f1': np.uint8, 'f2': np.float16, 'f4': np.float32}[dtype])
        return a.reshape(self.h, self.w, comps)[::-1]


def tex_from(a, mip=True, srgb_premul=False):
    """numpy HxWxC (top row first; uint8 or float) -> texture (bottom row first)"""
    a = np.ascontiguousarray(a[::-1]); c = ctx()
    dt = 'f1' if a.dtype == np.uint8 else 'f2' if a.dtype == np.float16 else 'f4'
    if a.ndim == 2: a = a[..., None]
    t = c.texture((a.shape[1], a.shape[0]), a.shape[2], a.tobytes(), dtype=dt, alignment=1)
    if mip: t.build_mipmaps(); t.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR); t.anisotropy = 8.0
    else: t.filter = (mgl.LINEAR, mgl.LINEAR)
    t.repeat_x = t.repeat_y = False
    return t
