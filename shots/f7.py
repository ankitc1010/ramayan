"""f7 (96): the duel.  Two chariots wheel round each other inside a ring of fire.  On f12 24 36 42 48 54 58 62 66 69 72 an arrow takes a head; it bursts into gold leaf, and grows again out of its own ember.
From f72 the ten heads leave him and wheel round one still point, faster and faster.  f90: one calm eye, which has seen where the wheel turns."""
from .f_kit import *
from .f8 import BG
from chars import ravana as RV, rama, vehicles as VH, vanara as VN, rakshasa as RK, horse as HR

HITS = (12, 24, 36, 42, 48, 54, 58, 62, 66, 69, 72)
HEADS = (7, 2, 4, 8, 1, 6, 3, 9, 0, 5, 4)               # which head each arrow takes (screen left 0 .. 9)
CUTS = [(0, 'wide'), (10, 'hit', 0), (18, 'draw'), (22, 'hit', 1), (30, 'passing'), (35, 'hit', 2), (39, 'hoof'), (41, 'hit', 3), (45, 'wheel'), (47, 'hit', 4), (51, 'string'), (53, 'hit', 5), (56, 'glare'), (57, 'hit', 6), (60, 'beast'), (61, 'hit', 7), (64, 'string'), (65, 'hit', 8), (68, 'hit', 9), (71, 'hit', 10), (73, 'discus'), (90, 'calm')]
# camera of each hit: yaw round the head, height, distance (in units of 10), fov, roll, side the arrow comes from
VIEW = [(16, -.10, 3.3, 30, -6, 1), (-22, -.12, 2.5, 28, 5, -1), (0, -.12, 2.0, 28, 0, 1), (28, .12, 1.9, 26, -8, -1), (-24, -.2, 1.7, 28, 9, 1), (12, .18, 1.6, 26, -5, -1), (-18, 0., 1.45, 26, 7, 1), (30, -.1, 1.35, 26, -9, -1), (-30, .1, 1.3, 26, 8, 1), (6, -.15, 1.2, 26, -4, -1), (0, 0., 2.3, 30, 0, 1)]

DISC = '''
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform vec2 res,ctr;uniform float fT,heat,spin,scale;
void main(){vec2 p=(vec2(uv.x*res.x,(1.-uv.y)*res.y)-ctr)/res.y/scale;float r=length(p),a0=atan(p.y,p.x);
 vec3 c=mix(hex(0x4a0c14),hex(0x090308),smoothstep(.05,1.2,r));
 float a=a0+spin*.55+2.2*exp(-r*1.6);float sw=fbm(vec2(a*2.2,r*3.-spin*.3))*.6+fbm(vec2(a*5.,r*7.-spin*.5))*.4;c=mix(c,hex(0x8a1c14),smoothstep(.42,.66,sw)*smoothstep(1.3,.1,r)*heat);c=mix(c,hex(0xd8521a),smoothstep(.56,.74,sw)*smoothstep(1.1,.15,r)*heat);
 float ray=smoothstep(-.2,.25,sin(a0*22.+spin))*.6+smoothstep(.2,.5,sin(a0*9.-spin*.6))*.6;c+=hex(0xff8a2a)*ray*exp(-r*2.)*.28*heat;
 for(int i=0;i<4;i++){float R=.20+.15*float(i);float n=20.+8.*float(i);float s=spin*(mod(float(i),2.)<.5?1.:-.7);float w=abs(fract((a0+s)*n/TAU)-.5);float d=abs(r-R-.028*cos(w*PI))-.004;c+=hex(0xffc46a)*smoothstep(.005,.0,d)*.45*heat;float b=length(vec2(w*TAU/n*R,r-R-.055));c+=hex(0xffd890)*smoothstep(.009,.003,b)*.5*heat;}
 c+=hex(0xffb45a)*(exp(-r*r*60.)*.7+exp(-r*5.)*.30)*heat;c*=.9+.16*fbm(uv*vec2(30.,17.));o=vec4(c,1);}
'''


class Shot(ShotBase):
    id = 'f7'; n = 96
    EVENTS = [(0, 'two chariots gallop', dict(dur=12)), (0, 'ring of fire', dict(dur=72)), (18, 'bow drawn', dict(dur=4)), (22, 'bow release', {}), (30, 'chariots pass', dict(dur=5)), (39, 'hoof', {}), (45, 'wheel', dict(dur=2)), (51, 'bow release', dict(k=1)), (56, 'glare', {}), (60, 'demon horse', {}), (64, 'bow release', dict(k=2))] + \
             [(f, 'head struck', dict(k=i)) for i, f in enumerate(HITS)] + [(f + (4 if i < 2 else 2), 'head grows again', dict(k=i)) for i, f in enumerate(HITS[:10])] + [(73, 'burning discus', dict(dur=17)), (90, 'silence', dict(dur=6))]

    def setup(self, st):
        F = ROAR; it = [(VN.arm(VN.WARRIOR, 3), VN.V_CHEER(p / 3.), F, 10) for p in range(3)] + [(VN.arm(VN.LANGUR, 2), VN.V_CHEER(p / 3. + .2), F, -10) for p in range(2)] + [(RK.SPEARMAN, RK.K_RUN(p / 3.), F, 10) for p in range(3)] + [(RK.HORN, RK.K_GUARD, F, -20), (RK.HULK, RK.K_RUN(.4), F, 15)]
        self.cr = Crowd(st, it, px=240, pitch=8., box=(-7, -.6, 7, 19)); r = np.random.default_rng(2); n = 520; a = r.uniform(0, 6.283, n); R = 184 + 70 * r.uniform(0, 1, n) ** 1.5; self.hp = np.c_[np.sin(a) * R, 0 * a, np.cos(a) * R]; self.ht = np.where(np.sin(a) > 0, r.integers(5, 10, n), r.integers(0, 5, n)); self.hs = r.uniform(1.0, 1.3, n)
        n = 230; a = np.arange(n) / n * 6.283 + r.uniform(-.01, .01, n); R = 168 + r.uniform(-4, 6, n); self.fp = np.c_[np.sin(a) * R, 0 * a, np.cos(a) * R]; self.fs = r.uniform(9, 17, n); self.fq = r.uniform(0, 1, n)

    # ---------------------------------------------------------------- the field
    def sky(self, st, **k): st.paint('sky.frag', **SKY(WAR, **{**dict(sunDir=(-.4, .12, -1.), sunR=.12, sunGlow=.5, rays=.35, cov=.6, cy0=.02, cy1=.36, cZen='#1c0510', cMid='#7a1018', cHor='#e0521c', cLit='#f07a3a', cCM='#9a2424', cSh='#460c1c'), **k}))

    def light(self, **k): return war_light(**{**dict(key=(-.5, .45, .6), keyCol=(.95, .66, .42), amb='#5a2c5a', rim=(.45, .35, -.8), rimCol=(2.0, .85, .26), bounceCol=(.45, .16, .04), envT='#ff9a5a', envM='#ff7a30', envB='#8a2a14', fogCol='#c8481c', fog=(.0026, 90., .006, 0.)), **k})

    def field(self, st, f):
        ground(st, gA='#8a3a20', gB='#5c1a18', gC='#2a0a10'); self.cr.draw(self.hp + np.c_[0 * self.hs, 1.6 * np.abs(np.sin(f * .5 + self.ht * 1.9 + self.hs * 40)), 0 * self.hs], scale=self.hs, tile=self.ht, tint=(.16, .07, .08))

    def fire(self, st, f, near=20.):
        z = (self.fp - st.cam.eye) @ st.cam.R[2]; m = z > near; P, s, q = self.fp[m], self.fs[m], self.fq[m]; o = np.argsort(-z[m]); s = s * (1 + .15 * np.sin(f * .7 + q * 40)); FX.particles(st, (P + V(0, 1, 0) * (s * .72)[:, None])[o], s[o], (.80, .52, .38), 'tongue', seed=q[o], fog=.0006, fogCol='#c8481c')

    def orbit(self, f):
        """where the two chariots are: angle of Rama's on the circle"""
        return -1.50 + f * .058

    def chariots(self, st, f, R=50., only=None, team=2):
        """both cars on their circle; returns {kind: (Chariot, yaw)}"""
        a = self.orbit(f); out = {}
        for k, off in (('rama', 0.), ('ravana', math.pi)):
            if only and k != only: continue
            b = a + off; out[k] = (VH.chariot(st, k, at=(math.sin(b) * R, 0, math.cos(b) * R), yaw=math.degrees(b) + 90, t=f / 24., speed=1., horses=team, roll=-3., canopy=k == 'rama'), math.degrees(b) + 90)
        return out

    def on(self, C, aim_yaw, k=1.):
        """platform matrix turned so that the figure's own +x (an archer's bow arm) points along aim_yaw"""
        M = C.stand.copy(); s = float(np.linalg.norm(M[:3, 0])); M[:3, :3] = eul(aim_yaw - 90, 0, 0) * s * k; return M

    def rama_on(self, st, M, draw, face=None, arrow=True, rel=0.):
        P = PZ.archer(draw).set(hedr=(74, 0, -2)); S = st.fig(rama.EXILE, P, M=M, face=face or Face(frown=.45, squint=.3, lid=.9, smile=-.05)); r = PR.bow_and_arrow(st, S, half=5.2, arrow=arrow, release=rel); st.fig(PR.QUIVER, M=PR.place(S.chest((.5, .5, -1.2)), S.d((-.35, 1, -.12)), S.d((0, 0, -1)), 1.)); t = st.t
        for an, ln, wd, col in ((lambda tt: S.chest((-1.2, 1.2, -.8)), 10., 1.4, ('#c8431f', '#4a1020', '#f2c24a')), (lambda tt: S.pelvis((-.6, .5, -.9)), 7., 1., ('#e8a22c', '#7a3a14', '#b3202a'))):
            Q = CL.lag(an, t, n=16, length=ln, wind=S.d((-1., .12, -.5)), grav=.10, wave=1.2); st.mesh(*CL.strip(Q, np.linspace(wd * .6, wd, 16), up=(0, 1, .3), m=6, curl=.12, n=36), kind=1, col=col, cls=8)
        return S, r

    def frame(self, f, st):
        st.clear('#000', f=f)
        for c in reversed(CUTS):
            if f >= c[0]: return getattr(self, c[1])(f, st, st.t, *c[2:])

    # ---------------------------------------------------------------- the circle
    def wide(self, f, st, t):
        u = f / 10.; b = -.66 + .36 * u; D = 120 - 16 * u; cam = Cam(V(math.sin(b) * D, 20 - 6 * u, math.cos(b) * D), V(0, 15 + 2 * u, 0), 46, roll=-6 + 7 * u); cam = shaken(cam, f, .25, .9); st.cam = cam; self.sky(st)
        st.open(cam, self.light(inkRef=2.2)); self.field(st, f); C = self.chariots(st, f); ar, av = C['rama'][0].stand[:3, 3], C['ravana'][0].stand[:3, 3]; y = math.degrees(math.atan2(*(av - ar)[[0, 2]]))
        self.rama_on(st, self.on(C['rama'][0], y), .9); S = RV.fig(st, RV.R_ARCHER(.8), M=self.on(C['ravana'][0], y + 180, 1.35), fan=1., arms=1., face=Face(frown=.8, mouth=.5, teeth=.6)); PR.bow_and_arrow(st, S, half=5.6); st.close(); self.fire(st, f)
        for k in C: p = C[k][0].w((0, 0, -4)); footdust(st, 30, (tuple(p - V(9, -1, 9)), tuple(p + V(9, 3, 9))), t, size=6, rise=5, alpha=.5, seed=3, col=('#d87a3a', '#6a2418'))
        FX.embers(st, 120, ((-120, 0, -120), (120, 8, 120)), t, rise=14, size=.35, seed=5, life=2.6, swirl=4); dustbank(st, .3, .7, 1.1, colA='#d87a3a', colB='#5a1a14', seed=2.)
        if f == 6: pass
        return st.finish(bloom=.5, thr=.9, vig=.55, contrast=1.12)

    def ravana(self, st, f, struck, hf, grow, at=V(0, 8.6, 0), yaw=0., mouth=0., eyes=.55, pose=None):
        al = np.ones(10); al[struck] = 1. if f < hf else (0. if f < hf + grow - 1 else keys(f, [(hf + grow - 1, 0.), (hf + grow, .55), (hf + grow + 1, 1.12), (hf + grow + 3, 1.)]))
        ml = float(mouth); return RV.fig(st, pose or RV.R_ARCHER(.9), at=at, yaw=yaw, fan=1., arms=1., alive=al, eyeglow=eyes, mouths=ml * (.5 + .5 * np.sin(np.arange(10) * 2.3 + f)), face=Face(frown=.9, smile=-.2, mouth=.5 * ml, teeth=.6))

    def hit(self, f, st, t, k):
        hf, h = HITS[k], HEADS[k]; s = f - hf; yw, el, D, fov, roll, side = VIEW[k]; a = s / 24.; grow = 4 if k < 2 else 2; rec = decay(a, 9.) if s >= 0 else 0.
        at = V(0, 8.6, 0); pose = RV.R_LOOM if k % 3 == 1 else RV.R_STAND.set(cher=(0, 6 - 16 * rec, 0)); S0 = RV.fig(st, pose, at=at, yaw=0, fan=1., arms=1., draw=False); hd = RV.heads(S0, 1.)[h]; c = hd[0] + V(0, .5 * hd[1], 0); cy = math.radians(yw)
        wide_ = D * 10; foc = lerp(c, S0.head((0, .6, 0)), .55 if k in (0, 1) else .30 if k == 10 else .18); eye = foc + wide_ * V(math.sin(cy), el, math.cos(cy)) + V(0, 0, -.6 * max(s, 0)); cam = Cam(eye, foc, fov, roll=roll); cam = shaken(cam, f, .06 * wide_ * .1 + .5 * rec, .9, k); st.cam = cam
        self.sky(st, sunDir=(math.sin(-cy + .25 * side) * 1., .16, -math.cos(cy)), sunR=.16, cov=.45)
        lit = (c + V(0, .6, 2.2) * hd[1], 2.2 * hd[1], tuple(np.array([2.4, 1.05, .30]) * rec)); L = self.light(pts=[lit], inkRef=1., key=(.55 * -side, .35, .75), fog=(.0016, 60., .004, 0.))
        st.open(cam, L, far=2000); self.field(st, f); C = VH.chariot(st, 'ravana', at=(0, 0, 0), yaw=0, t=t, speed=1., horses=2, canopy=False) if k in (0, 1) else None; S = self.ravana(st, f, h, hf, grow, mouth=.8 if s >= 0 else .25, pose=pose); RV.cape(st, S, t, wind=(.3 * side, .15, -.35))
        # the arrow: two frames in the air
        dr = nz(c - (eye - cam.R[0] * side * .62 * wide_ - cam.R[1] * .16 * wide_)); ln = .24 * wide_ + 2.
        if -3 < s < 0: tip = c - dr * ((-s - .55) * .42 * wide_); st.fig(PR.arrow_of(ln, 1.3 + .03 * wide_), M=PR.place(tip - dr * ln, cam.R[1] - dr * (cam.R[1] @ dr), dr, 1.))
        st.close(); self.fire(st, f, 40.)
        if -3 < s < 0: FX.ribbon(st, np.array([tip - dr * 1.5 * wide_, tip - dr * .25 * wide_, tip]), np.array([.0, .62, .26]) * wide_ * .022, 'fire', (1.1, .9, .6), seed=k); FX.ribbon(st, np.array([tip - dr * 1.5 * wide_, tip]), .010 * wide_, 'light', '#ffb050', '#fff6dc')
        if s >= 0:
            sc = hd[1]; FX.ribbon(st, np.array([c - dr * 40, c + dr * 30]), .30 * sc * max(0., 1 - s / 4.) + .001, 'light', '#ffb050', '#fff6dc', amt=max(0, 1 - s / 4.)); leafburst(st, c, a, speed=11 * sc, n=150, size=.17 * sc, seed=30 + k, grav=7, life=1.0); FX.burst(st, 60, c, a, speed=7 * sc, grav=-3, size=.10 * sc, seed=60 + k, col='#ff7a24', kind='ember', life=.9)
            if s < grow + 2: b = c - V(0, 1.0 * sc, 0); FX.particles(st, b[None], (1.2 + .35 * math.sin(f * 3.)) * sc, '#ff8a2a', 'ember', alpha=.8); FX.flame(st, b, .9 * sc + .5 * sc * smooth(0, grow, s), seed=k, glow=.5, calm=1.6)
            x, y, _ = cam.project(c); IM.shock(st, (float(x), float(y)), 30 + 2600 * a, 60, 46 * max(0., 1 - a * 4)); IM.zoomblur(st, (float(x), float(y)), .028 * rec)
            if s == 0: IM.speedlines(st, (x, y), col='#1a0408', seed=k, inner=.36, dens=7, amt=.75)
            if s == 0 and k in (0, 1, 10): IM.inkflash(st, '#12040a', '#d8301a', '#fff0cc', lo=.24, hi=.56)
        FX.embers(st, 50, (tuple(foc - V(16, 14, 10)), tuple(foc + V(16, 2, 14))), t, rise=6., size=.09, seed=k, life=2., swirl=1.5)
        return st.finish(bloom=.55, thr=.9, vig=.55, contrast=1.12, satu=1.05)

    # ---------------------------------------------------------------- between the blows
    def draw(self, f, st, t):
        u = (f - 18) / 3.; cam = Cam(V(4.5, 18.2, 22 - 2.5 * u), V(1.6, 19.6, 0), 34, roll=-6 + 2 * u); cam = shaken(cam, f, .18, .9); st.cam = cam; self.sky(st, sunDir=(.25, .16, -1))
        st.open(cam, self.light(key=(.6, .4, .7), fog=(.002, 60, .004, 0))); self.field(st, f); C = VH.chariot(st, 'rama', at=(0, 0, 0), yaw=70, t=t, speed=1., horses=2, canopy=False); self.rama_on(st, self.on(C, 92), keys(f, [(18, .55), (21, 1.04, 'out')])); st.close(); self.fire(st, f, 40.); FX.embers(st, 60, ((-18, 6, -10), (18, 12, 14)), t, rise=7, size=.08, seed=3, life=2.)
        return st.finish(bloom=.5, thr=.9, vig=.55, contrast=1.12)

    def string(self, f, st, t):
        """the string hand, and the string"""
        k = f - (51 if f < 60 else 64); rel = k >= 1; M = np.eye(4); M[:3, 3] = (0, 8.6, 0); P = PZ.archer(1.05).set(hedr=(74, 0, -2)); S0 = st.fig(rama.EXILE, P, M=M, draw=False); h = S0.palm('R', .22, .95, .34); sd = -1 if f > 60 else 1; cam = Cam(h + V(2.2, .4 * sd, 6.4 - .5 * k), h + V(.9, .05, 0), 34, roll=8 * sd); cam = shaken(cam, f, .10 + .25 * rel, .9); st.cam = cam; self.sky(st, sunDir=(.1, .3, -1))
        st.open(cam, self.light(key=(.6, .3, .75), inkRef=.8, pts=[(h + V(3, .5, 2), 3., (.9, .42, .14))])); S = st.fig(rama.EXILE, P, M=M, face=Face(frown=.45, squint=.4, lid=.85)); PR.bow_and_arrow(st, S, half=5.2, arrow=not rel, release=float(rel)); st.close()
        if rel: g = S.palm('L', 0, .62, .3); d = nz(g - h); FX.ribbon(st, np.array([h - d * 1, h + d * 30]), [.02, .5], 'light', '#ffb050', '#fff6dc', amt=1. if k == 1 else .5); FX.burst(st, 40, h, (k - .5) / 24., speed=16, grav=2, size=.06, seed=4, life=.4); IM.whip(st, 22, 0)
        return st.finish(bloom=.6, thr=.9, vig=.55, contrast=1.12)

    def passing(self, f, st, t):
        """broadside, low: the two cars cross in front of us"""
        u = (f - 30) / 4.; cam = Cam(V(0, 3.2, 64), V(0, 15, 0), 50, roll=-3 + 6 * u); cam = shaken(cam, f, .5, .9); st.cam = cam; self.sky(st, sunDir=(0, .17, -1), sunR=.15)
        st.open(cam, self.light(inkRef=1.6, key=(0, .45, .8), keyCol=(.75, .5, .34), fog=(.0020, 70., .004, 0.))); self.field(st, f); x = -44 + 52 * u
        A = VH.chariot(st, 'rama', at=(x - 6, 0, 8), yaw=90, t=t, speed=1.1, horses=2, pitch=-2); B = VH.chariot(st, 'ravana', at=(-x + 6, 0, -26), yaw=-90, t=t, speed=1.1, horses=2, pitch=-2)
        self.rama_on(st, self.on(A, 60 + 70 * u), 1.); S = RV.fig(st, RV.R_ARCHER(.9), M=self.on(B, 240 - 60 * u), fan=1., arms=1., face=Face(frown=.9, mouth=.6, teeth=.6)); PR.bow_and_arrow(st, S, half=5.6); st.close(); self.fire(st, f, 30.)
        for C in (A, B): p = C.w((0, 0, 0)); footdust(st, 34, (tuple(p - V(16, -1.5, 5)), tuple(p + V(16, 3, 5))), t, size=4.5, rise=5, alpha=.5, seed=3, col=('#d87a3a', '#6a2418'))
        FX.embers(st, 90, ((-50, 0, -40), (50, 10, 40)), t, rise=10, size=.2, seed=5, life=2.)
        return st.finish(bloom=.5, thr=.9, vig=.55, contrast=1.12)

    def hoof(self, f, st, t):
        s = f - 39; cam = Cam(V(13, 1.5, 47 - .8 * s), V(2.5, 4.8, 26), 48, roll=9); cam = shaken(cam, f, .5 if s else .15, .9); st.cam = cam; self.sky(st, sunDir=(-.3, .14, -1), sunR=.15)
        st.open(cam, self.light(inkRef=1., key=(.5, .4, .7), fog=(.002, 60, .004, 0))); self.field(st, f); VH.chariot(st, 'rama', at=(0, 0, 0), yaw=0, t=t, speed=1., horses=2, phase=.22 + .10 * s, flags=False); st.close(); self.fire(st, f, 40.); ring_burst(st, V(5, .2, 34), (s + 1.2) / 24., speed=26, n=30, size=2.4, col=('#d87a3a', '#6a2418'), life=.6); FX.burst(st, 50, V(5, .3, 34), (s + .6) / 24., speed=26, grav=20, size=.12, seed=5, up=.6, life=.5); IM.zoomblur(st, (960, 620), .05)
        return st.finish(bloom=.5, thr=.9, vig=.55, contrast=1.12)

    def wheel(self, f, st, t):
        s = f - 45; st.cam = Cam(V(0, 5, 10), V(0, 5, 0), 40); cam = Cam(V(20 - s, 4.2, 11), V(7.4, 6.2, -.4), 46, roll=-11); cam = shaken(cam, f, .5, .9); st.cam = cam; self.sky(st, sunDir=(-1, .14, -.5), sunR=.15)
        st.open(cam, self.light(inkRef=1., key=(.8, .35, .4), fog=(.002, 60, .004, 0))); self.field(st, f); C = VH.chariot(st, 'ravana', at=(0, 0, 0), yaw=0, t=t, speed=1.2, horses=2, flags=False); st.close(); self.fire(st, f, 40.); p = C.w((7.0, .2, 0)); FX.burst(st, 70, p, .05 + s / 24., speed=36, grav=10, size=.14, seed=f, up=.5, spread=(.6, 1, 1), life=.5); footdust(st, 24, (tuple(p - V(3, -.5, 14)), tuple(p + V(3, 2, 2))), t, size=3, rise=4, alpha=.5, seed=4, col=('#d87a3a', '#6a2418'))
        x, y, _ = cam.project(C.w((6.5, 5, 0))); IM.zoomblur(st, (float(x), float(y)), .0, spin=.16)
        return st.finish(bloom=.5, thr=.9, vig=.55, contrast=1.12)

    def glare(self, f, st, t):
        S0 = RV.fig(st, RV.R_STAND, draw=False); e = RV.eye_points(S0, 1.)[4].mean(0); cam = Cam(e + V(.5, -.1, 5.2), e + V(.1, .15, 0), 25, roll=-5); cam = shaken(cam, f, .05, .9); st.cam = cam; st.clear('#1a0408', f=f); self.sky(st, sunDir=(0, .3, -1))
        st.open(cam, self.light(key=(-.6, .1, .75), inkRef=.8, pts=[(e + V(-2, -1.5, 2.2), 2.4, (1.4, .55, .16))])); RV.fig(st, RV.R_STAND, fan=1., eyeglow=.8, face=Face(frown=1.1, lid=.85, smile=-.4, glow=.8)); st.close(); FX.embers(st, 40, (tuple(e - V(4, 3, 3)), tuple(e + V(4, 0, 4))), t, rise=3, size=.03, seed=3, life=1.2)
        return st.finish(bloom=.7, thr=.85, vig=.6, contrast=1.14)

    def beast(self, f, st, t):
        cam = Cam(V(23, 12.0, 43), V(4.6, 13.8, 34.5), 27, roll=-8); cam = shaken(cam, f, .3, .9); st.cam = cam; self.sky(st, sunDir=(-1., .16, -.35), sunR=.17)
        st.open(cam, self.light(inkRef=1., key=(.8, .25, .5), keyCol=(.80, .5, .32), amb='#5a2c5a', fog=(.002, 60, .004, 0))); self.field(st, f); VH.chariot(st, 'ravana', at=(0, 0, 0), yaw=0, t=t, speed=1., horses=2, phase=.05, flags=False); st.close(); self.fire(st, f, 40.); FX.embers(st, 60, ((-8, 4, 36), (16, 8, 50)), t, rise=9, size=.10, seed=3, life=1.2)
        return st.finish(bloom=.6, thr=.88, vig=.55, contrast=1.14)

    # ---------------------------------------------------------------- the wheel
    def discus(self, f, st, t):
        """the heads leave their row and turn about the one point that does not move"""
        u = (f - 73) / 16.; out = ease_out((f - 73) / 5., 2.2); sp = .10 * (f - 73) + 5.4 * max(0., u) ** 2.6; S0 = RV.fig(st, RV.R_STAND, draw=False); nav = S0.pelvis((0, 1.35, 1.5)); D = lerp(38, 17., ease_io(max(0, (f - 76) / 13.), 2.)); cam = Cam(nav + V(0, .2 + 1.8 * (1 - out), D), nav + V(0, 2.8 * (1 - out), 0), 40, roll=0); cam = shaken(cam, f, .10 + .25 * u, .9); st.cam = cam; x, y, _ = cam.project(nav); ppu = cam.px(nav)
        st.paint(DISC, ctr=(float(x), float(y)), heat=float(.55 + .55 * u), spin=float(sp * .6), scale=float(1.0 + .5 * u))
        L = Light(key=(0, -.1, 1), keyCol=tuple(np.array([1.05, .60, .34]) * (1 - .25 * u)), amb=(.10, .04, .09), rim=(0, .4, -.9), rimCol=(2.0, .8, .22), envT='#ff8a3a', envM='#d8501c', envB='#4a1018', bounceCol=(.2, .06, .02), pts=[(nav + V(0, 0, 2.5), 5., (1.2 + 1.2 * u, .55 + .5 * u, .16 + .12 * u))], shadow=False, ink=3.2)
        st.open(cam, L, far=2000); S = RV.fig(st, RV.R_STAND, fan=1., arms=1., alive=0., hair=0., navel=float(smooth(76, 84, f)), armT=t * (1 + 3 * u), face=Face(lid=0.)) if f < 88 else S0
        hh = math.tan(math.radians(20)) * D; row = RV.heads(S0, 1.); Rr = hh * lerp(.70, .80, u); hs = hh * lerp(.150, .205, u); c3 = nav + V(0, 0, 3.); tips = []
        for ring in (0, 1):                                                     # the wheel, and after f79 a smaller one inside it that turns the other way
            k2 = smooth(79, 83, f)
            if ring and k2 <= 0: continue
            for h in range(10):
                an = math.pi / 2 - (h - 4) / 10. * 6.2832 + (-sp if not ring else sp * .8 + .31)
                if ring: p = nav + V(math.cos(an), math.sin(an), 0) * Rr * .47 + V(0, 0, 2.2); up, sc = V(math.cos(an), math.sin(an), 0), hs * .52 * k2
                else: p = lerp(row[h][0] + V(0, 0, 1.2), c3 + V(math.cos(an), math.sin(an), 0) * Rr, out); up = nz(lerp(V(0, 1, 0), V(math.cos(an), math.sin(an), 0), out)); sc = lerp(row[h][1], hs, out); tips.append((an, p))
                st.fig(RV.HEAD, M=PR.place(p, up, V(0, 0, 1), sc), face=Face(frown=1., mouth=.75, teeth=.6, smile=.4, glow=1., lid=1.1), u=dict(eyeglow=np.full(10, .85, 'f4')))
        st.close()
        for h, (an, p) in enumerate(tips):                                      # each head drags its fire round the circle
            q = np.linspace(.10, .12 + .50 * out, 24); rr = Rr + hs * (1.1 + .35 * np.sin(q * 11 + t * 11 + h)); arc = c3 + np.stack([np.cos(an + q) * rr, np.sin(an + q) * rr, 0 * q - .8], 1); FX.ribbon(st, arc, np.linspace(.75, .10, 24) * hs * out + .001, 'fire', (1., .75, .5), seed=h * 2.7, amt=.9)
        n = 54; a = np.arange(n) / n * 6.283 - sp * 1.15; R2 = Rr + 2.9 * hs; s = (1.15 + .25 * np.sin(a * 7 + t * 9)) * out * hs; FX.particles(st, c3 + np.stack([np.cos(a) * R2, np.sin(a) * R2, 0 * a - 1.], 1), s, (.85, .55, .38), 'tongue', rot=a - math.pi / 2 + .5, seed=np.arange(n) * .618 % 1)
        g = smooth(77, 86, f); FX.particles(st, (nav + V(0, 0, .4))[None], 1.0 + 1.6 * g, '#ffd070', 'ember', alpha=g); FX.particles(st, (nav + V(0, 0, .5))[None], .9 * g + .01, '#fff4d0', 'glint', alpha=g)
        FX.embers(st, 120, (tuple(c3 - V(18, 14, 6)), tuple(c3 + V(18, 10, 8))), t, rise=6, size=.09, seed=5, life=1.6, swirl=3)
        rate = sp - (.10 * (f - 74) + 5.4 * max(0., (f - 74) / 16.) ** 2.6 if f > 73 else 0); IM.zoomblur(st, (float(x), float(y)), .012 * u, spin=min(.20 * rate, .025 + .03 * u + .28 * smooth(86.5, 90, f)))
        if f > 80: FX.particles(st, np.array([[x, y]]), ppu * (.35 + .5 * g) + 260 * smooth(85, 90, f), '#fff0c0', 'glint', alpha=g); FX.particles(st, np.array([[x, y]]), 30 + 900 * smooth(85, 90.5, f) ** 2, '#ffb84a', 'ember', alpha=.9 * smooth(85, 88, f))
        return st.finish(bloom=.55 + .15 * u, thr=.88, vig=.5, contrast=1.12, satu=1.06, flash=.10 * smooth(87, 90, f), flashCol='#fff0d0')

    def calm(self, f, st, t):
        """he has seen it"""
        P = PZ.archer(1.04).set(hedr=(72, 2, -2)); S = st.fig(rama.EXILE, P, yaw=0, draw=False); h = S.head((.16, .02, .7)); fw = S.d(np.array([0, 0, 1.]) @ S.u['Bh']); sd = S.d(np.array([1., 0, 0]) @ S.u['Bh']); e = S.head((.50, .10, 1.2)); cam = Cam(e + fw * 1.15 + sd * .12 + V(0, .0, 0), e + V(-.02, -.01, 0), 25, roll=-3); st.cam = cam
        st.paint(BG, sun=(1700., 420.), heat=.55, silent=1.)
        L = Light(key=tuple(fw * .6 + sd * .5 + V(0, -.1, 0)), keyCol=(.60, .58, .62), amb=(.12, .12, .24), rim=tuple(-fw * .3 - sd + V(0, .3, 0)), rimCol=(.9, .35, .16), envT='#ffb060', envM='#d8601c', envB='#2a1030', pts=[(h + fw * 3.2 + sd * 1.6 + V(0, -.2, 0), 3., (.34, .15, .05))], shadow=False, ink=4.2)
        st.open(cam, L); st.fig(rama.EXILE, P, face=Face(lid=.92, frown=.12, squint=.1, smile=.10, spark=.9)); st.close()
        # in the iris: the wheel, ten points of gold, and the flame that stands still in the middle of it
        a = np.arange(10) / 10 * 6.283 + .2; Q = np.c_[806 + 122 * np.cos(a), 636 + 92 * np.sin(a)]; Q = Q[(Q[:, 1] > 570) & (Q[:, 1] < 722)]; FX.particles(st, Q, 13., '#ffb84a', 'ember', alpha=.9)
        FX.particles(st, np.array([[810., 630.]]), 150., '#ff8a2a', 'ember', alpha=.16); FX.particles(st, np.array([[812., 655.]]), 34., '#ffe9b0', 'ember', alpha=.55)
        FX.embers(st, 16, (tuple(h - V(2.5, 2, 2.5)), tuple(h + V(2.5, 0, 2.5))), 3.7 + (f - 90) / 60., rise=1., size=.016, seed=2, life=2.4)
        return st.finish(bloom=.45, thr=.95, vig=.6, contrast=1.10)
