"""Armies and city crowds: figures baked once into a tile atlas (with normals, so they are lit and inked like everyone else), then drawn by the thousand."""
import numpy as np, math
import moderngl as mgl
from . import gl
from .cam import Cam
from .rig import V, eul


class Crowd:
    """Crowd(st, [(fig, pose, face[, yaw[, props]])...], box=(x0,y0,x1,y1) figure units, px=tile height, pitch=camera pitch in degrees).  props(st, Solved) may draw weapons into the tile."""

    def __init__(s, st, items, box=(-7, -.6, 7, 19), px=420, pitch=8., cols=8):
        s.st, s.box = st, box; c = gl.ctx(); px *= st.k; h = int(px); w = int(round(px * (box[2] - box[0]) / (box[3] - box[1]))); n = len(items); cols = min(cols, n); rows = (n + cols - 1) // cols
        s.grid = (cols, rows); s.tw, s.th = w, h; s.n = n
        s.at = [c.texture((w * cols, h * rows), 4, dtype='f2') for _ in range(4)]
        for t in s.at: t.filter = (mgl.NEAREST, mgl.NEAREST); t.repeat_x = t.repeat_y = False
        fb = c.framebuffer(s.at); keep = (st.cam, getattr(st, 'light', None), st.far); ss, sw, sh = st.ss, st.sw, st.sh
        from .stage import Light
        for k, it in enumerate(items):
            fig, pose, face = it[0], it[1], it[2]; yaw = it[3] if len(it) > 3 else 0.; props = it[4] if len(it) > 4 else None
            ctr = V((box[0] + box[2]) / 2, (box[1] + box[3]) / 2, 0); D = 60.; a = math.radians(pitch); eye = ctr + D * V(0, math.sin(a), math.cos(a)); cam = Cam(eye, ctr, 30)
            st.open(cam, Light(), far=200.); st.ortho_bake = ((box[3] - box[1]) / 2, w, h)
            S = st.fig(fig, pose, yaw=yaw, face=face, shadow=False)
            if props: props(st, S)
            st.ortho_bake = None
            p = gl.program('blit4.frag'); fb.use(); c.viewport = ((k % cols) * w, (k // cols) * h, w, h); c.disable(mgl.BLEND); c.disable(mgl.DEPTH_TEST)
            gl.set_uniforms(p, dict(tile=(w, h), dist=D)); gl.bind(p, dict(zip(('g0', 'g1', 'g2', 'g3'), st.gt))); gl.quad(p).render(mgl.TRIANGLE_STRIP)
        st.cam, st.light, st.far = keep
        # normals were written in world axes of the bake camera: rotate into view axes once
        s.bakeR = Cam(V(0, math.sin(math.radians(pitch)), math.cos(math.radians(pitch))) * 60, (0, 0, 0)).R
        s._fix(fb, w * cols, h * rows)

    def _fix(s, fb, w, h):
        src = 'in vec2 uv;layout(location=0) out vec4 o0;layout(location=1) out vec4 o1;layout(location=2) out vec4 o2;layout(location=3) out vec4 o3;uniform sampler2D t0,t1,t2,t3;uniform mat3 Rr;\nvoid main(){ivec2 q=ivec2(gl_FragCoord.xy);vec4 a=texelFetch(t0,q,0),d=texelFetch(t3,q,0);o0=vec4(Rr*a.xyz,a.w);o1=texelFetch(t1,q,0);o2=texelFetch(t2,q,0);o3=vec4(Rr*d.xyz,d.w);}\n'
        c = gl.ctx(); new = [c.texture((w, h), 4, dtype='f2') for _ in range(4)]
        for t in new: t.filter = (mgl.NEAREST, mgl.NEAREST); t.repeat_x = t.repeat_y = False
        f2 = c.framebuffer(new); f2.use(); c.viewport = (0, 0, w, h); p = gl.program(src); gl.set_uniforms(p, dict(Rr=s.bakeR)); gl.bind(p, dict(zip(('t0', 't1', 't2', 't3'), s.at))); gl.quad(p).render(mgl.TRIANGLE_STRIP)
        for t in s.at: t.release()
        s.at = new

    def draw(s, pos, scale=1., tile=0, flip=1., lean=0., tint=(1, 1, 1), upright=1.):
        """inside open()/close(): pos Nx3 = feet in world space; scale, tile, flip (+1/-1), lean scalar or N; tint rgb or Nx3"""
        st = s.st; c = gl.ctx(); p = gl.program('crowd.frag', vs='crowd.vert'); pos = np.asarray(pos, float); n = len(pos)
        if n == 0: return
        o = np.argsort(((pos - st.cam.eye) ** 2).sum(1)); D = np.zeros((n, 11), 'f4'); D[:, :3] = pos; D[:, 3] = scale; D[:, 4] = tile; D[:, 5] = flip; D[:, 6] = lean; D[:, 7:10] = tint; D = D[o]
        q = c.buffer(np.array([-1, -1, 1, -1, -1, 1, 1, 1], 'f4').tobytes()); vb = c.buffer(D.tobytes()); vao = c.vertex_array(p, [(q, '2f', 'q'), (vb, '3f 4f 4f/i', 'pos', 'a', 'tint')]); st.oid += 1
        u = dict(box=tuple(float(x) for x in s.box), grid=tuple(float(x) for x in s.grid), upright=float(upright), objId=float(st.oid)); tx = dict(zip(('a0', 'a1', 'a2', 'a3'), s.at)); st.oid += 97
        st._gdraw(p, u, tx, vao, mgl.TRIANGLE_STRIP, inst=n); vao.release(); vb.release(); q.release()
