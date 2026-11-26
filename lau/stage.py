"""The stage: canvas + G-buffer.  Order of a frame:
   st.clear(); st.paint(sky shader); st.open(cam, light); st.fig(...)/st.world(...)/st.mesh(...)/st.crowd(...); st.close(); st.paint/plate/particles/vector ...; st.finish() -> uint8 image"""
import numpy as np, math, cairo
import moderngl as mgl
from dataclasses import dataclass, field, replace
from . import W, H, gl
from .cam import Cam
from .rig import Pose, solve, eul, V, nz


def hexc(h, lin=True):
    if not isinstance(h, str): return tuple(h)
    h = h.lstrip('#'); h = ''.join(x * 2 for x in h) if len(h) == 3 else h; c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(x ** 2.2 for x in c) if lin else tuple(c)


@dataclass
class Light:
    """Directions point TOWARD the light (world space).  Colours: hex strings or linear rgb tuples; k = multiplier in the tuple form."""
    key: tuple = (-.7, .5, .6)
    keyCol: object = (1.0, .96, .88)
    amb: object = (.72, .74, .86)
    rim: tuple = (.8, .4, -.5)
    rimCol: object = (.55, .42, .30)
    bounce: tuple = (0, -1, .2)
    bounceCol: object = (.10, .08, .06)
    envT: object = (1.0, 1.0, 1.0)          # what gold reflects from above / the horizon / below
    envM: object = (1.0, .95, .85)
    envB: object = (.75, .60, .55)
    pts: list = field(default_factory=list)  # [(xyz, radius, rgb)], up to 12 flames
    shadow: bool = True
    edge: float = .47                       # toon terminator position
    soft: float = .03
    hi: float = .55                         # highlight tone strength on skin and cloth
    stip: float = .30                       # stippled terminator
    air: float = 1.0                        # airbrushed edge shading, as in mural painting
    pig: float = 1.0                        # pigment granulation
    ink: float = 3.2                        # line width in px at 1080p
    inkCol: object = (.0075, .0035, .0065)
    inkRef: float = 1.0                     # world size of the figures' unit, scales line detection
    fogCol: object = (0, 0, 0)
    fog: tuple = (0, 0, 0, 0)               # density, start, height falloff, base height


class Solved:
    """a placed figure: joints in figure space (J), frames, and figure -> world"""

    def __init__(s, u, Mf, Sc): s.u = u; s.J = u['J']; s.Mf = Mf; s.Sc = Sc

    def w(s, p): return (s.Mf @ np.append(np.asarray(p, float), 1))[:3]

    def d(s, v): return nz(s.Mf[:3, :3] @ np.asarray(v, float))

    def joint(s, i): return s.w(s.J[i])

    def palm(s, side, x=0., y=.62, z=.16):
        from .rig import palm_point
        return s.w(palm_point(s.u, side, x, y, z))

    def head(s, p=(0, 0, 0)): return s.w(s.J[3] + np.asarray(p, float) @ s.u['Bh'])

    def chest(s, p=(0, 0, 0)): return s.w(s.J[1] + np.asarray(p, float) @ s.u['Bc'])

    def pelvis(s, p=(0, 0, 0)): return s.w(s.J[0] + np.asarray(p, float) @ s.u['Bp'])

    def hand(s, side, v):
        """direction v of the hand frame (x thumb side, y fingers, z palm) in world space"""
        return s.d(np.asarray(v, float) @ s.u['BL' if side == 'L' else 'BR'])


class Fig:
    """a character or prop: GLSL with map()/surf(), palette, proportions, face painter"""

    def __init__(self, name, glsl, pal, dim=None, build=None, hs=None, face=None, box=(-1.1, -1.25, 1.1, .95), bound=(0, 8, 0, 10.5), step=.82, defs='', human=True, u=None):
        self.name, self.glsl, self.human, self.defs = name, glsl, human, defs
        self.dim, self.build = dim or {}, build or {}; self.hs = list(hs or [1] * 8); self.facefn = face; self.box = box
        self.bound, self.step = bound, step; self.u = u or {}
        n = 24; self.Pb = np.zeros((n, 3), 'f4'); self.Ps = np.zeros((n, 3), 'f4'); self.Pc = np.zeros(n, 'f4')
        for k, (b, s, c) in pal.items(): self.Pb[k] = hexc(b); self.Ps[k] = hexc(s); self.Pc[k] = c
        self._ftex = {}

    def program(self):
        src = '#include "%s"\n#include "%s"\n#include "fig_main.glsl"\n' % ('fig_head.glsl' if self.human else 'prop_head.glsl', self.glsl)
        return gl.program(src, defs=self.defs)

    def facetex(self, face):
        if self.facefn is None: return None
        k = repr(face)
        if k not in self._ftex:
            if len(self._ftex) > 40: self._ftex.clear()
            a = self.facefn(face); t = gl.tex_from(a); t.swizzle = 'BGRA'; self._ftex[k] = t
        return self._ftex[k]

    def variant(self, **k):
        """same character with other palette entries: variant(pal={7:(..)}) / u={...}"""
        import copy
        o = copy.copy(self); o.Pb, o.Ps, o.Pc = self.Pb.copy(), self.Ps.copy(), self.Pc.copy(); o._ftex = {} if 'face' in k else self._ftex
        for i, (b, s, c) in k.get('pal', {}).items(): o.Pb[i] = hexc(b); o.Ps[i] = hexc(s); o.Pc[i] = c
        o.u = {**self.u, **k.get('u', {})}
        for n in ('build', 'dim'):
            if n in k: setattr(o, n, {**getattr(self, n), **k[n]})
        if 'face' in k: o.facefn = k['face']
        if 'defs' in k: o.defs = k['defs']
        return o


def model(at=(0, 0, 0), yaw=0., pitch=0., roll=0., scale=1.):
    M = np.eye(4); M[:3, :3] = eul(yaw, pitch, roll) * scale; M[:3, 3] = at
    return M


class Stage:
    def __init__(s, ss=2, w=W, h=H, k=1):
        """shots draw in w x h picture pixels; the output has k x k pixels for each of them (k=2 makes 3840x2160 of the same shot)"""
        s.ss, s.k, s.wd, s.ht = ss, k, w, h; c = gl.ctx(); s.pw, s.ph = w * k, h * k; sw, sh = s.pw * ss, s.ph * ss; s.sw, s.sh = sw, sh
        s.gt = [c.texture((sw, sh), 4, dtype=d) for d in ('f4', 'f2', 'f2', 'f4')]          # depth and ids need full floats
        for t in s.gt: t.filter = (mgl.NEAREST, mgl.NEAREST); t.repeat_x = t.repeat_y = False
        s.gz = c.depth_texture((sw, sh)); s.G = c.framebuffer(s.gt, s.gz)
        s.S = gl.RT(sw, sh, 1, 'f2', filt='nearest')
        s.L = c.framebuffer([c.texture((s.pw, s.ph), 4, dtype='f2'), c.texture((s.pw, s.ph), 1, dtype='f4')])
        for t in s.L.color_attachments: t.repeat_x = t.repeat_y = False
        s.C = gl.RT(s.pw, s.ph); s.C2 = gl.RT(s.pw, s.ph); s.out = gl.RT(s.pw, s.ph, 1, 'f1', comps=4)
        s.sh_n = 1400; s.sht = c.texture((s.sh_n, s.sh_n), 1, dtype='f4'); s.shz = c.depth_texture((s.sh_n, s.sh_n)); s.Sh = c.framebuffer([s.sht], s.shz)
        s.bl = []
        q = 2
        while min(w // q, h // q) > 8 and len(s.bl) < 6: s.bl.append(gl.RT(w // q, h // q)); q *= 2
        s.cam = Cam((0, 0, 10), (0, 0, 0)); s.t = 0.; s.f = 0; s.calls = []; s.far = 4000.
        s.ortho_bake = None
        s._white = gl.tex_from(np.full((2, 2, 4), 255, np.uint8), mip=False); s.has3d = False

    # ---------------------------------------------------------------- canvas
    def clear(s, col=(0, 0, 0), f=0):
        s.f = f; s.t = f / 24.; c = hexc(col); s.C.clear(*c, 1); s.has3d = False
        s.L.use(); s.L.clear(0, 0, 0, 0)
        gl.ctx().copy_framebuffer  # noqa (kept simple: depth cleared below)
        s.L.color_attachments[1].write(np.full((s.ph, s.pw), 6e4, 'f4').tobytes())

    def base_u(s):
        return dict(res=(s.wd, s.ht), fT=s.t, frame=float(s.f), far=s.far, **s.cam.u())

    def paint(s, frag, blend=None, texs=None, defs='', **u):
        """full-screen shader over the canvas: frag = file name or source (in: uv; out: o premultiplied linear)"""
        p = gl.program(frag, defs=defs); gl.draw(p, s.C, {**s.base_u(), **u}, {**(texs or {}), 'tZ': s.L.color_attachments[1]}, blend)

    def post_paint(s, frag, texs=None, defs='', **u):
        """shader that reads the canvas (sampler tex) and replaces it"""
        p = gl.program(frag, defs=defs); gl.draw(p, s.C2, {**s.base_u(), **u}, {'tex': s.C[0], 'tZ': s.L.color_attachments[1], **(texs or {})}); s.C, s.C2 = s.C2, s.C

    def plate(s, tex, x=W / 2, y=H / 2, scale=1., rot=0., alpha=1., tint=(1, 1, 1), srgb=True, blend='over', lod=0., flip=False, sx=None, sy=None):
        """draw a texture so that its centre lands at pixel (x, y); scale 1 = one texel per pixel"""
        p = gl.program('copy.frag'); tw, th = tex.size; a = math.radians(rot); c, sn = math.cos(a), math.sin(a)
        kx, ky = (sx or scale) * (-1 if flip else 1), (sy or scale)
        # uv (0..1, y up) -> texture uv
        T1 = np.array([[s.wd, 0, -x], [0, s.ht, -(s.ht - y)], [0, 0, 1.]]); R_ = np.array([[c, sn, 0], [-sn, c, 0], [0, 0, 1.]])
        S_ = np.array([[1 / (tw * kx), 0, .5], [0, 1 / (th * ky), .5], [0, 0, 1.]])
        gl.draw(p, s.C, dict(M=S_ @ R_ @ T1, tint=(*hexc(tint), alpha), srgb=1. if srgb else 0., blurLod=float(lod)), dict(tex=tex), blend)

    def vector(s, fn, blend='over', alpha=1., tint=(1, 1, 1), scale=1.):
        """fn(cairo context, 1920x1080, y down) drawn over the canvas"""
        scale *= s.k; w, h = int(s.wd * scale), int(s.ht * scale)
        sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h); c = cairo.Context(sf); c.scale(scale, scale); fn(c); sf.flush()
        a = np.ndarray((h, w, 4), np.uint8, sf.get_data()); t = gl.tex_from(a.copy(), mip=False); t.swizzle = 'BGRA'
        s.plate(t, s.wd / 2, s.ht / 2, 1 / scale, alpha=alpha, tint=tint, blend=blend); t.release()

    # ---------------------------------------------------------------- 3D
    def open(s, cam, light, far=4000.):
        s.cam, s.light, s.far = cam, light, far; s.calls = []; s.oid = 0
        s.G.use(); s.G.clear(0, 0, 0, 0, depth=1.0)

    def _gdraw(s, prog, u, texs=None, vao=None, mode=mgl.TRIANGLE_STRIP, inst=-1, scissor=None, cull=False):
        c = gl.ctx(); s.G.use(); c.viewport = (0, 0, s.sw, s.sh); s.G.scissor = scissor or (0, 0, s.sw, s.sh)
        c.enable(mgl.DEPTH_TEST); c.depth_func = '<'; c.disable(mgl.BLEND)
        rs, oth = (s.sw, s.sh), 0.
        if s.ortho_bake: oth, bw, bh = s.ortho_bake; rs = (bw, bh); c.viewport = (0, 0, bw, bh); s.G.scissor = (0, 0, bw, bh)
        gl.set_uniforms(prog, u); gl.set_uniforms(prog, dict(res=rs, far=s.far, ortho=float(oth), bake=1. if s.ortho_bake else 0., fT=s.t, **s.cam.u()))
        if texs: gl.bind(prog, texs)
        (vao or gl.quad(prog)).render(mode, instances=inst) if inst >= 0 else (vao or gl.quad(prog)).render(mode)
        s.G.scissor = (0, 0, s.sw, s.sh); c.disable(mgl.DEPTH_TEST)

    def _scissor(s, P, R):
        """pixel rectangle of a bounding sphere"""
        x, y, z = s.cam.project(P)
        if z < R * 1.05: return None
        r = R / math.sqrt(max(z * z - R * R, 1e-6)) * s.cam.fl * s.ht / 2 * 1.15 + 6
        x0, x1 = max(0, x - r), min(s.wd, x + r); y0, y1 = max(0, y - r), min(s.ht, y + r)
        if x1 <= x0 or y1 <= y0: return 'out'
        g = s.ss * s.k
        return (int(x0 * g), int((s.ht - y1) * g), int((x1 - x0) * g) + 1, int((y1 - y0) * g) + 1)

    def fig(s, fig, pose=None, at=(0, 0, 0), yaw=0., pitch=0., roll=0., scale=1., face=None, M=None, u=None, texs=None, shadow=True, draw=True):
        """draw a figure; returns a Solved (joints -> world) for props, ribbons and effects"""
        Mf = model(at, yaw, pitch, roll, scale) if M is None else np.asarray(M, float); Sc = float(np.linalg.norm(Mf[:3, 0]))
        us = solve(pose or Pose(), fig.dim, fig.build) if fig.human else dict(J=np.zeros((20, 3)))
        S = Solved(us, Mf, Sc)
        if not draw: return S
        if fig.human:
            c = us['J'][:20].mean(0); bc = (us['J'][0] + us['J'][3]) / 2 * .6 + c * .4; R = np.linalg.norm(us['J'] - bc, axis=1).max() + fig.bound[3] * .24
            bnd = np.append(bc, R)
        else: bnd = np.array(fig.bound, float)
        for src in (fig.u, u or {}):                                           # a call's own bound wins over the figure's
            if 'bound' in src: bnd = np.array(src['bound'], float)
        s.oid += 1
        fu = dict(Mf=Mf, Mi=np.linalg.inv(Mf), Sc=Sc, bnd=bnd, objId=float(s.oid), Pb=fig.Pb, Ps=fig.Ps, Pc=fig.Pc, stepK=fig.step, HS=np.array(fig.hs, 'f4'), faceBox=fig.box, Wind=(0, 0, 0), jaw=0., **us)
        fu.update(fig.u); fu.update(u or {}); fu.pop('bound', None)
        if face is not None and hasattr(face, 'mouth'): fu.setdefault('jaw', 0.); fu['jaw'] = float(getattr(face, 'mouth', 0.))
        prog = fig.program(); tx = dict(texs or {})
        if fig.facefn is not None:
            from .face import Face
            tx['tFace'] = fig.facetex(face if face is not None else Face())
        sc = None if s.ortho_bake else s._scissor(S.w(bnd[:3]), bnd[3] * Sc)
        if sc != 'out': s._gdraw(prog, fu, tx, scissor=sc)
        if shadow: s.calls.append((prog, fu, tx, S.w(bnd[:3]), bnd[3] * Sc))
        return S

    def world(s, src, u=None, texs=None, defs='', shadow=False, head='world_head.glsl', main='world_main.glsl'):
        """ray-marched scenery: src supplies  vec2 map(vec3 p)  and  void surf(vec3 p, vec3 n, int m, inout Surf s)  in world space"""
        full = '#include "%s"\n%s\n#include "%s"\n' % (head, src if '\n' in src else '#include "%s"' % src, main)
        p = gl.program(full, defs=defs); s.oid += 1
        uu = dict(objId=float(s.oid), keyDir=tuple(nz(s.light.key)), **(u or {})); s._gdraw(p, uu, texs)
        if shadow: s.calls.append((p, uu, texs, V(0, 0, 0), None))

    def mesh(s, pos, nrm, uv, idx, kind=0, col=('#c03020', '#601010', '#e0b040'), cls=1., ink=.9, u=None, texs=None, part=1., frag='mesh.frag', twosided=True):
        """triangle mesh into the G-buffer: pos/nrm Nx3, uv Nx2, idx Mx3; frag colours by `kind` pattern"""
        c = gl.ctx(); p = gl.program(frag, vs='mesh.vert'); s.oid += 1
        data = np.hstack([pos, nrm, uv]).astype('f4'); vb = c.buffer(data.tobytes()); ib = c.buffer(np.asarray(idx, 'i4').tobytes())
        vao = c.vertex_array(p, [(vb, '3f 3f 2f', 'ip', 'in_', 'iuv')], ib)
        uu = dict(objId=float(s.oid), kind=int(kind), cA=hexc(col[0]), cB=hexc(col[1]), cC=hexc(col[2]), cls=float(cls), inkw=float(ink), part=float(part), **(u or {}))
        if 'rep' in uu and 'rep' in p: uu['rep'] = tuple(list(uu['rep']) + [0] * 4)[:p['rep'].dimension]      # as many numbers as this shader wants
        s._gdraw(p, uu, texs, vao, mgl.TRIANGLES); vao.release(); vb.release(); ib.release()

    def _shadow(s):
        c = gl.ctx(); L = s.light; d = nz(L.key); cs = [q for q in s.calls if q[4] is not None]
        if not cs: return None
        P = np.array([q[3] for q in cs]); R = np.array([q[4] for q in cs]); ctr = (P.min(0) + P.max(0)) / 2; rad = float((np.linalg.norm(P - ctr, axis=1) + R).max())
        eye = ctr + d * rad * 2.2; cam = Cam(eye, ctr, 30); far = rad * 4.4
        s.Sh.use(); s.Sh.clear(0, 0, 0, 0, depth=1.0); c.viewport = (0, 0, s.sh_n, s.sh_n); c.enable(mgl.DEPTH_TEST); c.depth_func = '<'; c.disable(mgl.BLEND)
        for prog, u, tx, sc_at, sc_r in s.calls:
            q = cam.R @ (np.asarray(sc_at, float) - cam.eye)
            if sc_r is not None:
                k = s.sh_n / 2 / rad; x0, y0 = (q[0] - sc_r) * k + s.sh_n / 2 - 2, (q[1] - sc_r) * k + s.sh_n / 2 - 2; x0, y0 = max(0, int(x0)), max(0, int(y0)); w = min(s.sh_n - x0, int(2 * sc_r * k) + 5); s.Sh.scissor = (x0, y0, max(1, w), max(1, min(s.sh_n - y0, int(2 * sc_r * k) + 5)))
            else: s.Sh.scissor = (0, 0, s.sh_n, s.sh_n)
            gl.set_uniforms(prog, u); gl.set_uniforms(prog, dict(res=(s.sh_n, s.sh_n), far=far, ortho=rad, bake=0., fT=s.t, **cam.u()))
            if tx: gl.bind(prog, tx)
            gl.quad(prog).render(mgl.TRIANGLE_STRIP)
        s.Sh.scissor = (0, 0, s.sh_n, s.sh_n); c.disable(mgl.DEPTH_TEST)
        M = np.eye(4); M[:3, :3] = cam.R; M[:3, 3] = -cam.R @ cam.eye; M[0] /= rad; M[1] /= rad
        return M

    def close(s, blend='over', alpha=1.):
        """shade + ink the G-buffer, composite over the canvas"""
        L = s.light; Mx = s._shadow() if L.shadow else None
        u = dict(res=(s.sw, s.sh), far=s.far, fT=s.t, keyDir=tuple(nz(L.key)), keyCol=hexc(L.keyCol), ambCol=hexc(L.amb), rimDir=tuple(nz(L.rim)), rimCol=hexc(L.rimCol), bounceDir=tuple(nz(L.bounce)), bounceCol=hexc(L.bounceCol),
                 envT=hexc(L.envT), envM=hexc(L.envM), envB=hexc(L.envB), fogCol=hexc(L.fogCol), fog=tuple(L.fog), inkCol=hexc(L.inkCol), inkW=L.ink, inkRef=L.inkRef, toonEdge=L.edge, toonSoft=L.soft, pig=L.pig, hiAmt=L.hi, stip=L.stip, air=L.air,
                 shOn=1. if Mx is not None else 0., shM=Mx if Mx is not None else np.eye(4), shFar=1., **s.cam.u())
        pp = np.zeros((12, 4), 'f4'); pc = np.zeros((12, 4), 'f4')
        for i, (p, r, c) in enumerate(L.pts[:12]): pp[i] = (*p, r); pc[i, :3] = hexc(c)
        u.update(nPt=min(12, len(L.pts)), ptPos=pp, ptCol=pc)
        gl.draw(gl.program('shade.frag'), s.S, u, dict(g0=s.gt[0], g1=s.gt[1], g2=s.gt[2], g3=s.gt[3], tSh=s.sht))
        gl.draw(gl.program('resolve.frag'), s.L_rt(), dict(sres=(s.sw, s.sh), ss=float(s.ss)), dict(tex=s.S[0], g0=s.gt[0], g1=s.gt[1]))
        gl.draw(gl.program('copy.frag'), s.C, dict(M=np.eye(3), tint=(1, 1, 1, alpha), srgb=0., blurLod=0.), dict(tex=s.L.color_attachments[0]), blend)
        s.has3d = True

    def L_rt(s):
        class _T: pass
        t = _T(); t.use = s.L.use; t.width, t.height = s.pw, s.ph
        return t

    def depth(s):
        """distance to what the last close() drew, one value per picture pixel, top row first"""
        D = np.frombuffer(s.L.color_attachments[1].read(), 'f4').reshape(s.ph, s.pw)[::-1]
        return D[::s.k, ::s.k]

    # ---------------------------------------------------------------- finish
    def finish(s, bloom=.35, thr=.85, expo=1., contrast=1.04, satu=1.06, vig=.35, grain=.014, paper=.05, ca=.6, sh=(1, 1, 1), hi=(1, 1, 1), flash=0., flashCol=(1, 1, 1), fade=0., fadeCol=(0, 0, 0)):
        src = s.C[0]; p = gl.program('bloom.frag')
        for i, b in enumerate(s.bl):
            t = src if i == 0 else s.bl[i - 1][0]; q = s.k if i == 0 else 1; gl.draw(p, b, dict(mode=0 if i == 0 else 1, px=(q / t.width, q / t.height), thr=float(thr), amt=1.), dict(tex=t))
        for i in range(len(s.bl) - 1, 0, -1):
            t = s.bl[i][0]; gl.draw(p, s.bl[i - 1], dict(mode=2, px=(1 / t.width, 1 / t.height), thr=0., amt=.85), dict(tex=t), 'add')
        gl.draw(gl.program('post.frag'), s.out, dict(res=(s.wd, s.ht), gres=(s.pw, s.ph), frame=float(s.f % 1000), bloom=bloom, expo=expo, contrast=contrast, satu=satu, vig=vig, grain=grain, paper=paper, ca=ca, flash=flash, fade=fade,
                 shTint=hexc(sh) if isinstance(sh, str) else tuple(sh), hiTint=hexc(hi) if isinstance(hi, str) else tuple(hi), flashCol=hexc(flashCol), fadeCol=hexc(fadeCol)), dict(tex=src, tBloom=s.bl[0][0]))
        return np.frombuffer(s.out.fbo.read(components=3), np.uint8).reshape(s.ph, s.pw, 3)[::-1].copy()
