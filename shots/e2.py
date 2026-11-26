"""e2 (96): the bridge builds itself.  Stones rain in on every pulse, each with the glowing name; they splash, sink a little, bob and lock, and the causeway runs ahead of the flying camera to Lanka (f0-35).  A squirrel with a pebble (f36-47).  Again the flying camera (f48-59); Rama and Lakshmana and the army march (f60), the camera swings round them, up and back: one line of small glowing names across the sea (f84-96)."""
from lau.shot import *
from lau.look import *
from chars import rama, hanuman as HM, vanara as VN, birds as BD
from worlds import lanka as LK
from shots import d_kit as K

Z0, DZ, NX, HW = 7000., 11.2, 4, 24.                            # shore, row spacing, stones across, half width; Lanka's sea stair is at z = 1560
NR = int((Z0 - 1580) / DZ)
R0 = 70                                                          # rows already there at f0
PER = 5                                                          # rows that land on each pulse
R72 = R0 + PER * 12 + PER
SUN = nz(V(-.30, .30, -1.))
DIRS = 8


def rowz(r): return Z0 - DZ * np.asarray(r, float)


def landing(r):
    """frame on which row r locks"""
    r = np.asarray(r, float); a = 6. * np.floor((r - R0) / PER); b = 73 + 17 * np.clip((r - R72) / (NR - R72), 0, 1) ** .62; return np.where(r < R72, a, b)


class Shot(ShotBase):
    id = 'e2'; n = 96
    EVENTS = [(0, 'sea', dict(dur=96)), (0, 'work song', dict(dur=96))] + [(q, 'stones splash', dict(big=int(q % 24 == 0))) for q in range(0, 36, 6)] + [(3 + q, 'stones thrown', {}) for q in range(0, 36, 12)] + [(36, 'squirrel feet', dict(dur=9)), (45, 'pebble set', {})] + [(q, 'stones splash', dict(big=int(q % 24 == 0))) for q in range(48, 60, 6)] + [(q, 'army footsteps', {}) for q in range(60, 96, 6)] + [(60, 'conch', dict(dur=14)), (74, 'names run to Lanka', dict(dur=16)), (90, 'bridge complete', {})]

    def setup(self, st):
        W_, H_ = 760, 500; sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W_, H_); c = cairo.Context(sf); LT.draw(c, 'ram', 130, 120, 285, col=(1, 1, 1), w=.17); sf.flush(); self.name = gl.tex_from(np.ndarray((H_, W_, 4), np.uint8, sf.get_data()).copy()); self.name.swizzle = 'BGRA'
        r = np.random.default_rng(2); N = NR * NX; self.sx = (np.arange(N) % NX - (NX - 1) / 2) * 11.9 + r.normal(0, .75, N); self.row = np.arange(N) // NX; self.sz = rowz(self.row) + r.normal(0, 1.0, N) + 1.6 * (self.row % 2) * 0 + (np.arange(N) % NX - 1.5) ** 2 * .6; self.sz = self.sz + np.where(np.arange(N) % 2, 3.0, -2.6); self.size = r.uniform(6.7, 7.9, N); self.ang = r.normal(0, 1, (3, N)) * np.array([[.20], [.055], [.055]]); self.sy = .95 + r.normal(0, .22, N); self.lt = landing(self.row) + r.choice([0, 0, 0, 1, 2], N); self.shp = r.integers(0, 6, N)
        self.fr = np.c_[r.choice([-1, 1], N) * r.uniform(60, 170, N), r.uniform(0, 8, N), r.uniform(-60, 130, N)]; self.hgt = r.uniform(16, 56, N); self.spin = r.uniform(-5, 5, (3, N)); self.D = r.uniform(14, 21, N); self.ph = r.uniform(0, 1, N)
        a = VN.arm; kk = [VN.YOUTH, VN.LANGUR2, VN.WARRIOR]
        self.cw = Crowd(st, [(a(fg, 4, p / 4), VN.V_CARRY_WALK(p / 4), Face(), 168) for fg in kk for p in range(4)] + [(fg, VN.V_THROW(p / 3), Face(mouth=.3), 150) for fg in kk for p in range(4)], px=420, pitch=8.)
        self.cm = Crowd(st, [(a(fg, h), VN.V_WALK(p / 4 + .13 * i), Face(mouth=.15), 360. * d / DIRS) for i, (fg, h) in enumerate(((VN.WARRIOR, 3), (VN.LANGUR, 0), (VN.YOUTH2, 2))) for d in range(DIRS) for p in range(4)], px=440, pitch=14.)
        # the marching column
        n = 900; self.mz = np.sort(r.uniform(0, 520, n)) ** 1.0; self.mx = r.uniform(-19, 19, n); self.mk = r.integers(0, 3, n); self.mp = r.uniform(0, 1, n); self.ms = r.uniform(.84, 1.0, n); self.mt = np.clip(r.normal(1, .1, (n, 1)) + r.normal(0, .035, (n, 3)), .72, 1.2)
        # builders
        n = 46; self.bx = r.choice([-1, 1], n) * r.uniform(15.5, 21.5, n); self.bz = r.uniform(-60, 330, n); self.bk = r.integers(0, 3, n); self.bp = r.uniform(0, 1, n); self.bs = r.uniform(.84, 1., n); self.bt = np.clip(r.normal(1, .1, (n, 1)) + r.normal(0, .03, (n, 3)), .72, 1.2)

    # ---- the stones
    def stones(self, st, f, cam, near=420., far=1500., boost=0.):
        zc = (np.c_[self.sx, self.sx * 0, self.sz] - cam.eye) @ cam.R[2]; born = self.lt - self.D; vis = (zc > -30) & (zc < far) & (f >= born); i = np.nonzero(vis)[0]; u = np.clip((f - born[i]) / self.D[i], 0, 1); T = np.maximum(0, (f - self.lt[i]) / 24.); done = u >= 1
        slot = np.c_[self.sx[i], self.sy[i], self.sz[i]]; P = slot + self.fr[i] * (1 - u)[:, None] ** 1.15; P[:, 1] += 4 * self.hgt[i] * u * (1 - u) * (1 - .25 * u); bob = np.where(done, -3.4 * np.exp(-4.2 * T) * np.cos(13 * T) + .16 * np.sin(1.7 * f / 24 + self.ph[i] * 6.28), 0); P[:, 1] += bob
        sp = np.where(done, 0., 1 - u); A = self.ang[:, i] + self.spin[:, i] * sp + np.where(done, np.exp(-3.6 * T) * .22 * np.sin(12 * T), 0)[None] * np.array([[.3], [1.], [1.]]); R = K.rotmats(*A); beat = impulse((f % 6) / 24., 12); gl_ = np.where(done, np.clip(T * 5, 0, 1) * (.55 + .25 * beat + .6 * np.exp(-3. * T) + boost), .45); z = zc[i]; st_col = ('#c8b49c', '#6a5a78', '#8f8474')
        for m, sub in ((z < near, 2), ((z >= near) & (z < 1100), 1), (z >= 1100, 0)):
            if m.any(): K.rocks(st, P[m], self.size[i[m]], R[m], shape=self.shp[i[m]], glow=gl_[m], sub=sub, col=st_col, name=self.name, wetY=2.2, ids=i[m], flat=(1., .60, .78), cuts=6, top=.50, ink=(.2, .5, .85)[sub])
        return i, P, u, T, done

    def splashes(self, st, f, cam, big=1.):
        m = (f - self.lt >= -.5) & (f - self.lt < 15) & (np.abs(self.sz - cam.eye[2]) < 700) & (self.lt > -20); i = np.nonzero(m)[0]
        if not len(i): return
        i = i[np.argsort(np.abs(self.sz[i] - cam.eye[2]))][:60]
        T = (f - self.lt[i]) / 24.; r = np.random.default_rng(4); k = 22; th = r.uniform(0, 6.283, (len(i), k)); v = r.uniform(.4, 1., th.shape); up = r.uniform(.5, 1., th.shape); TT = T[:, None]; R = self.size[i][:, None] * .85 + 13 * v * TT; P = np.stack([self.sx[i][:, None] + np.cos(th) * R, .5 + 30 * up * TT - 42 * TT * TT, self.sz[i][:, None] + np.sin(th) * R * .9], -1).reshape(-1, 3); al = np.clip(1.4 - TT / .42, 0, 1) * np.ones_like(th); ok = (P[:, 1] > 0)
        FX.particles(st, P, (r.uniform(.22, .62, th.shape) * big).ravel(), '#f8fffa', 'drop', alpha=al.ravel() * ok)
        n = 3; th = r.uniform(0, 6.283, (len(i), n)); R = self.size[i][:, None] * .9 + 7 * TT; Q = np.stack([self.sx[i][:, None] + np.cos(th) * R, .6 + 13 * TT * r.uniform(.5, 1., th.shape) - 20 * TT * TT, self.sz[i][:, None] + np.sin(th) * R], -1).reshape(-1, 3); s = (1.2 + 5.5 * TT * np.ones_like(th)).ravel() * big; K.sprites(st, Q, s * K.CW / K.CH, s, var=r.integers(0, 8, len(s)), rot=r.uniform(-1, 1, len(s)), alpha=(np.clip(1.3 - TT / .40, 0, 1) * np.ones_like(th)).ravel() * .9, puff=True, cLit='#ffffff', cMid='#e2f6f0', cSh='#93c8c4', cInk='#2a7a80', cRim=(.2, .2, .15), soft=2., near=10., ink=.5)

    def glows(self, st, i, P, T, done, cam, k=1.):
        """halo of each name, and far names as points of light"""
        m = done; z = (P - cam.eye) @ cam.R[2]; m = m & (z > 4); Q = P[m] + V(0, 3.0, 0); FX.particles(st, Q, 3.4, '#ff8a2a', 'ember', alpha=np.clip(k * (.16 + .5 * np.exp(-3 * T[m])), 0, 1))

    def far_names(self, st, f, cam, start, k=1., size=1.):
        r = np.arange(0, NR); L = landing(r); z = rowz(r); on = np.clip((f - L) / 3., 0, 1); x = np.array([-9., 9.]); P = np.stack([np.broadcast_to(x, (NR, 2)), np.full((NR, 2), 3.), np.broadcast_to(z[:, None], (NR, 2))], -1).reshape(-1, 3); on = np.repeat(on, 2); d = (P - cam.eye) @ cam.R[2]; m = (d > start) & (on > 0); P, on, d = P[m], on[m], d[m]
        if not len(P): return
        px = cam.fl * 540 / d; s = np.maximum(3.4, 3.4 / px) * size; fl = .75 + .25 * np.sin(f * .5 + np.arange(len(P)) * 1.7); new = np.exp(-np.maximum(0, f - np.repeat(L, 2)[m]) / 5.); FX.particles(st, P, s * (1 + 1.6 * new), np.array(hexc('#ff9a3a')) * 1.25, 'lamp', alpha=k * np.clip((d - start) / 160, 0, 1) * on * fl * np.clip(.62 + 500 / d + new, 0, 1))

    def sky(self, st, **k): st.paint('sky.frag', **SKY(None, **{**dict(cZen='#1f5a7a', cMid='#5fb0b0', cHor='#f7d9a0', cLow='#8fc4b4', sunDir=tuple(SUN), sunR=.045, sunCol='#fff0c0', sunGlow=.8, rays=.45, cov=.55, cy0=.03, cy1=.24, cscale=1.6, cLit='#fffaf0', cCM='#d8efe6', cSh='#8fc4c0', cInk='#2a6a70'), **k}))

    def light(self, **k): return Light(**{**dict(key=tuple(nz(V(-.45, .65, .25))), keyCol='#fff0d0', amb='#6f9ab0', rim=(-.2, .5, -1), rimCol=(1.1, .9, .55), bounceCol=(.06, .20, .20), envT='#e8fff8', envM='#ffdc9a', envB='#2a7a80', fogCol='#e8dcb4', fog=(.00008, 900, .0012, 0), ink=3.2), **k})

    def world(self, st, f, front, near=520., lanka=True, **k):
        K.ocean(st, **{**dict(amp=1.5, fr=.14, spd=1.2, near=near, lvl=.8, sun=SUN, glit=.22, unfog=3.2, seaW=.34, bridge=(HW - 2, front, Z0 + 40, 1.), cDeep='#07505e', cMid='#158a8c', cLite='#66ccb8', cFoam='#fbf8ea', cFar='#cfe0c0'), **k})
        if lanka: LK.draw(st, 'day')

    def gild(self, st, cam, k=1.):
        """the far island: small and dark gold"""
        w = cam.project(V(0, 1.6, 1500)); 
        if w[2] < 100: return
        z0 = float(w[2]); st.post_paint('''
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform sampler2D tex,tZ;uniform vec2 res;uniform float z0,yw,k,xc,xw,fl;uniform vec3 ro;uniform mat3 CamR;
void main(){vec3 c=texture(tex,uv).rgb;float z=texelFetch(tZ,ivec2(gl_FragCoord.xy),0).x;float y=(1.-uv.y)*res.y;float m=step(z0*.93,z)*step(z,z0+3400.)*smoothstep(yw+1.,yw-1.,y)*step(abs(uv.x*res.x-xc),xw);vec3 rd=transpose(CamR)*vec3((uv*2.-1.)*vec2(res.x/res.y,1.),fl);float zs=rd.y<0.?(.8-ro.y)/rd.y*fl:1e9;m*=step(.012,abs(z/zs-1.));float l=lum(min(c,vec3(1.2)));vec3 g=mix(hex(0x3a2010),hex(0xb8741e),smoothstep(.18,.60,l));g=mix(g,hex(0xf6c65a),smoothstep(.55,.95,l));o=vec4(mix(c,g,m*.82*k),1);}
''', z0=z0, yw=float(w[1]), k=float(k), xc=float(w[0]), xw=float(1500. * cam.fl * 540 / max(z0 + 1500, 1.)))

    def front(self, f):
        r = np.arange(NR); L = landing(r); return float(rowz(r[L <= f].max()) - DZ * .5) if (L <= f).any() else Z0

    # ---- pictures
    def frame(self, f, st):
        st.clear('#000', f=f)
        if 36 <= f < 48: return self.squirrel(f, st, st.t)
        if f < 60: return self.fly(f, st, st.t)
        return self.march(f, st, st.t)

    def fly(self, f, st, t):
        g = f if f < 36 else f - 12; v = PER * DZ / 6.; beat = impulse((f % 6) / 24., 10); s2 = f >= 48
        zc = rowz(R0) + 128 - v * f + (0 if not s2 else -14); sw = math.sin(g * .13)
        cam = Cam(V(5.5 * sw + (6 if s2 else 0), keys(f, [(0, 30.), (12, 15.), (24, 18.), (35, 26.), (47, 10.), (59, 22.)]) - .5 * beat, zc), V(-3 * sw, keys(f, [(0, 12.), (12, 9.), (35, 8.), (47, 12.), (59, 4.)]), zc - 150), keys(f, [(0, 46.), (20, 52.), (35, 54.), (47, 60.), (59, 56.)]), roll=7 * math.sin(g * .13 + .8) - 1.2 * beat); st.cam = cam
        self.sky(st); st.open(cam, self.light(), far=30000.); self.world(st, f, self.front(f)); i, P, u, T, done = self.stones(st, f, cam)
        # builders: carriers on both edges, throwers near the end of the road
        fr = self.front(f); z = fr + 24 + (self.bz + 60 - 22. * t) % 330; thr = z < fr + 84; ph = ((t * 1.0 + self.bp) * 4).astype(int) % 4; th = np.clip((((f - 3) % 12) / 12. * 4 + (self.bp > .5) * 2) % 4, 0, 3.9).astype(int); tl = np.where(thr, 12 + self.bk * 4 + th, self.bk * 4 + ph); B = np.c_[self.bx, 3.3 + .2 * np.sin(t * 3 + self.bp * 6), z]; m = ((B - cam.eye) @ cam.R[2]) > 7; self.cw.draw(B[m], scale=self.bs[m], tile=tl[m], tint=self.bt[m], flip=np.where(self.bx[m] > 0, -1., 1.))
        st.close(); self.gild(st, cam); self.splashes(st, f, cam); self.glows(st, i, P, T, done, cam); self.far_names(st, f, cam, 700.)
        # drips from the stones in the air
        m = ~done & (u > .05); Q = P[m]
        if len(Q): r = np.random.default_rng(6); k = 5; off = r.uniform(0, 1, (len(Q), k)); D = (Q[:, None] + np.stack([r.normal(0, 2.5, off.shape), -14 * off ** 1.5 - 3, 6 * off + r.normal(0, 2, off.shape)], -1)).reshape(-1, 3); FX.particles(st, D, .28, '#f0fff8', 'drop', alpha=np.tile(.8 * (1 - off), 1).ravel())
        BD.specks(st, np.c_[np.linspace(-900, 900, 14) + 60 * t, 260 + 60 * np.sin(np.arange(14) * 2.1), np.full(14, zc - 2200)], t, size=5, col='#1f4a58', seed=2)
        IM.zoomblur(st, cam.project(V(0, 10, zc - 2000))[:2], .008 + .012 * beat)
        return st.finish(bloom=.45, thr=.95, vig=.35, flash=.15 * (f == 0) + .10 * (f == 48), flashCol='#f4fff8')

    def squirrel(self, f, st, t):
        g = f - 36; zb = rowz(40); run = g < 9; x = keys(f, [(35, -8.6), (45, 1.6, 'linear'), (46, 2.0, 'out')]); sc = 1.15; top = 3.75; zs = zb + 4.2; y = top - .04 + (.35 * abs(math.sin(g * 1.1)) if run else 0)
        cam = Cam(V(-1.0 + .16 * g, 7.6 - .03 * g, zb + 17.5 - .12 * g), V(.1 + .14 * g, 4.5, zb - 2), 34, roll=-2); st.cam = cam; self.sky(st)
        st.open(cam, self.light(inkRef=.6, shadow=True, bounceCol=(.10, .07, .04), amb='#8a90a8', key=tuple(nz(V(-.55, .62, .55)))), far=30000.); self.world(st, f, rowz(R0 + 40), near=260., lanka=True); i, P, u, T, done = self.still_stones(st, f, cam)
        k = ('slab',); kk = (2, (1., .60, .78), 6, .50); hh = float(K._SH[kk][0][0][:, 1].max()); K.rocks(st, np.array([[-.6, top - hh * 12.5, zs]]), np.array([[12.5, 12.5, 8.6]]), np.eye(3)[None], shape=np.array([0]), glow=.95, sub=2, col=('#c8b49c', '#6a5a78', '#8f8474'), name=self.name, wetY=1.6, ids=np.array([2999]), flat=kk[1], cuts=6, top=.50)
        pose = 'run' if run else ('bow' if f < 47 else 'sit'); BD.squirrel(st, (x, y, zs), yaw=90 if run else 62, scale=sc, pose=pose, ph=g * .36, carry=False); q = np.array([x + (2.0 if run else 1.55), y + (1.25 if run else .22), zs + (.15 if run else .7)]); K.rocks(st, q[None], np.array([.40]), K.rotmats(np.array([.4]), np.array([.1]), np.array([.1])), sub=2, ink=.8, col=('#e8d8b8', '#8a7a88', '#b8a888'))
        n = 7; xs = np.linspace(-30, 34, n) + 19 * t; self.cw.draw(np.c_[(xs + 40) % 80 - 40, np.full(n, 3.2), np.full(n, zb - 20.)], scale=1., tile=(np.arange(n) % 3) * 4 + ((t * 4 + np.arange(n) * 1.3).astype(int) % 4), flip=1.)
        st.close(); self.gild(st, cam, .8); self.glows(st, i, P, T, done, cam, .8); IM.dof(st, float((V(x, 4, zs) - cam.eye) @ cam.R[2]), 9., 7.)
        if f >= 45: FX.burst(st, 14, q, (f - 45) / 24., speed=2.2, grav=2, size=.07, seed=3, col='#ffc060', life=.5, up=.5); FX.particles(st, q[None] + V(0, .2, .2), 1.6 * smooth(45, 46, f), '#ffb050', 'glint', alpha=.8)
        return st.finish(bloom=.40, thr=1.0, vig=.4)

    def still_stones(self, st, f, cam): return self.stones(st, f + 40, cam, near=160., far=900.)

    def march(self, f, st, t):
        g = on2(f); zr = Z0 - 340. - 7.2 * (f - 60) / 24.; C = V(0, 10, zr); sw = smoother(66, 90, f); az = keys(f, [(60, 187.), (68, 183.), (90, 2., 'io'), (96, 0.)]); rad = keys(f, [(60, 27.), (68, 31.), (78, 130.), (90, 330., 'out'), (96, 352.)]); hgt = keys(f, [(60, 6.), (68, 9.), (79, 70.), (91, 168., 'out'), (96, 178.)]); a = math.radians(az); eye = C * [1, 0, 1] + V(math.sin(a) * rad, hgt, math.cos(a) * rad); at = lerp(C + V(0, 1.6, 0), V(0, 0, zr - 560), smoother(76, 92, f)); cam = Cam(eye, at, lerp(38, 44, sw), roll=keys(f, [(60, 2.), (76, -7.), (92, 0.)])); st.cam = cam
        fr = self.front(f); e = smooth(74, 91, f); mx = lambda a, b: tuple(np.array(hexc(a)) * (1 - e) + np.array(hexc(b)) * e); self.sky(st, cZen=mx('#1f5a7a', '#0e2f4c'), cMid=mx('#5fb0b0', '#2f6a7c'), cHor=mx('#f7d9a0', '#e8a262'), cLow=mx('#8fc4b4', '#8a9a88'), cLit=mx('#fffaf0', '#ffe2b0'), cCM=mx('#d8efe6', '#d8a884'), cSh=mx('#8fc4c0', '#6f7f88'), sunCol=mx('#fff0c0', '#ffc878')); back = cam.R[2][2] > 0; kz = lerp(-.75, .10, sw); st.open(cam, self.light(key=tuple(nz(V(-.5, .55, kz))), keyCol=mx('#fff0d0', '#e8b27a'), amb=mx('#6f9ab0', '#3f5f78')), far=30000.); self.world(st, f, fr, lanka=not back, cDeep=mx('#07505e', '#032c3a'), cMid=mx('#158a8c', '#0a5058'), cLite=mx('#66ccb8', '#2f8480'), cFoam=mx('#fbf8ea', '#d8d8c8'), cFar=mx('#cfe0c0', '#a87e60'))
        # the shore behind them
        if cam.R[2][2] > -.5:
            r = np.random.default_rng(8); n = 26; H = np.c_[np.linspace(-2200, 2200, n) + r.normal(0, 60, n), np.full(n, -4.), Z0 + r.uniform(260, 900, n)]; K.FL.scatter(st, 'hill', H, 210, season='summer', seed=3, vary=.35, haze=.35, hazeCol=hexc('#d8dcb8')); n = 60; PZ_ = np.c_[r.normal(0, 260, n), np.full(n, 0.), Z0 + r.uniform(60, 240, n)]; K.FL.scatter(st, 'palm', PZ_, 70, season='summer', seed=5, haze=.15, hazeCol=hexc('#d8dcb8'))
        i, P, u, T, done = self.stones(st, f, cam, near=330., far=2600., boost=.6 * e); ph = (g - 60) / 24. * 1.06; wy = 3.35
        pr = PZ.walk(ph).set(hedr=(0, -2, 0), lh=(2.3, 8.4, .9), lhand='grip', lfing=(0, -.2, 1), lpalm=(-1, 0, 0)); pl = PZ.walk(ph + .5).set(hedr=(6, 0, 0))
        S = st.fig(rama.EXILE, pr, at=(-4.6, wy, zr), yaw=180, face=Face(frown=.25, smile=.1, spark=.4, lid=.95)); st.fig(PR.QUIVER, M=PR.place(S.chest((.5, .5, -1.2)), S.d((-.35, 1, -.12)), S.d((0, 0, -1)), 1.)); gp = S.palm('L', .0, .62, .30); st.fig(PR.BOW.variant(u=dict(pr=np.array([1.0, 4.6] + [0] * 14, 'f4'))), M=PR.place(gp, S.d((.12, 1, .10)), S.d((.2, 0, 1)), 1.))
        S2 = st.fig(rama.LAKSHMANA, pl, at=(4.6, wy, zr + 2.4), yaw=180, face=Face(frown=.35, lid=.95)); st.fig(PR.QUIVER, M=PR.place(S2.chest((.5, .5, -1.2)), S2.d((-.35, 1, -.12)), S2.d((0, 0, -1)), 1.))
        S3, TP, _ = K.giant(st, HM.H_WALK(ph + .2), at=(-12.6, wy, zr + 10.), yaw=178, face=HM.VFace(smile=.3, lid=.95), tail='calm', ring=None, wind=(.1, 0, .2)); st.fig(VN.arm(VN.SUGRIVA, 3), VN.V_WALK(ph + .7), at=(12.4, wy, zr + 10.5), yaw=182, face=Face(frown=.3)); st.fig(VN.arm(VN.ANGADA, 3), VN.V_WALK(ph + .3), at=(1., wy, zr + 17.), yaw=180, face=Face(frown=.3))
        mz = zr + 24 + self.mz; B = np.c_[self.mx, np.full(len(mz), wy), mz]; m = (mz < Z0 + 10) & (((B - cam.eye) @ cam.R[2]) > 5); rel = np.degrees(np.arctan2(cam.eye[0] - B[m][:, 0], cam.eye[2] - B[m][:, 2])); d = np.round((180. - rel) / (360. / DIRS)).astype(int) % DIRS; tl = self.mk[m] * DIRS * 4 + d * 4 + ((g / 24. * 1.06 + self.mp[m]) * 4).astype(int) % 4; self.cm.draw(B[m], scale=self.ms[m], tile=tl, tint=self.mt[m])
        # banners over the column
        for k in range(6):
            zb = zr + 40 + 62 * k; x = 15 * (-1) ** k; p0 = V(x, 31, zb); st.mesh(*CL.tube(np.array([V(x, 3, zb), V(x, 33, zb)]), .28, 8, 8), kind=0, col=('#6a3a20', '#2a1410', '#6a3a20'), cls=1); Q = CL.lag(lambda q: p0, t, 12, 13, wind=(.9, .05, .25), grav=.15, wave=.5, freq=1.3, phase=k); st.mesh(*CL.strip(Q, np.linspace(6.5, 3.5, 12), up=(0, 1, 0), n=24), kind=4, col=('#d8341e', '#7a1418', '#ffd060'), cls=8)
        st.close()
        if not back: self.gild(st, cam)
        self.glows(st, i, P, T, done, cam, 1 + 2.4 * e); self.far_names(st, f, cam, 260. if not back else 5000., k=1., size=lerp(1., 1.5, e)); self.splashes(st, f, cam)
        # the line running out to the island
        if f >= 73 and not back:
            x, yy, z = cam.project(V(0, 4, fr)); FX.particles(st, V(0, 6, fr)[None], max(8., 9. / (cam.fl * 540 / max(z, 1.))), '#ffb050', 'glint', alpha=1 - smooth(89, 94, f))
        if f >= 89 and not back: k = impulse((f - 89) / 24., 8); FX.particles(st, V(0, 60, 1500)[None], 200., '#ffb050', 'glint', alpha=.6 * k)
        FX.drift(st, 70, (tuple(C - V(40, 8, 60)), tuple(C + V(40, 40, 80))), t, kind='petal', size=.4, col='#e8421e', col2='#f2b23a', fall=2., sway=.8, seed=4, wind=(6, 0, 3), alpha=1 - smooth(74, 84, f))
        return st.finish(bloom=.5, thr=.93, vig=.38, flash=.10 * (f == 60), flashCol='#fff4dc')
