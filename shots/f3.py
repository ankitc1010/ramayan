"""f3 (96): Kumbhakarna.  f0 dunes at dusk, a file of small runners; f12 the dune opens, it is the lid of an eye.  f30-59 he stands up and puts out the sun.
f60-65 Rama, small, at full draw.  f66 one arrow, a line of light across the whole frame; f70-73 his chest breaks like a kintsugi bowl; f74 he falls on us; f78 he lands; dust."""
from .f_kit import *
from chars import kumbha as KB, vanara as VN, rama

Z = 12.
RUN = ('V_RUN',)

DUNE = '''
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform vec2 res;uniform float fT,amt,lift;
float ridge(float x,float s){return .5+.13*sin(x*1.7+s)+.06*sin(x*4.1+s*2.)+.02*sin(x*9.+s);}
void main(){vec2 p=vec2(uv.x*res.x,(1.-uv.y)*res.y)/res.y;vec3 c=mix(hex(0x3a0a18),hex(0xb8301c),smoothstep(0.,.30,p.y));c=mix(c,hex(0xff9a3c),smoothstep(.20,.46,p.y));
 vec2 s=p-vec2(1.28,.30+lift*.2);float r=length(s),a=atan(s.y,s.x);c+=hex(0xff9a3c)*(exp(-r*4.)*.5+smoothstep(-.1,.3,sin(a*18.))*exp(-r*3.)*.16);c=mix(c,hex(0xffc060)*1.3,smoothstep(.105,.100,r));
 float y=p.y+lift;float k=0.;
 float r1=ridge(p.x*.9,4.)-.20;vec3 d1=mix(hex(0xc8582a),hex(0x8a2c20),smoothstep(r1,r1+.25,y));c=mix(c,d1,smoothstep(-.002,.002,y-r1));
 float r2=ridge(p.x*.8,1.3)-.06;float bl=smoothstep(r2-.004,r2+.03,y+.03*(fbm(p*7.)-.5));
 o=vec4(c,1.)*amt*(1.-bl);}
'''


class Shot(ShotBase):
    id = 'f3'; n = 96
    EVENTS = [(0, 'desert wind', dict(dur=12)), (2, 'small feet running', dict(dur=14)), (12, 'eye opens', {}), (18, 'eye widens', {}), (30, 'mountain stands up', dict(dur=26)), (30, 'crowd flees', dict(dur=28))] + [(f, 'rock bursts', dict(k=i)) for i, f in enumerate((36, 41, 45, 49))] + \
             [(51, 'giant hand sweeps', dict(dur=5)), (56, 'sun goes out', {}), (60, 'bow drawn, quiet', dict(dur=6)), (66, 'release of light', {}), (67, 'arrow strikes jewel', {}), (70, 'armour cracks', dict(dur=5)), (74, 'giant falls', dict(dur=4)), (78, 'giant hits the ground', {}), (80, 'ground wave', dict(dur=10)), (84, 'dust swallows', dict(dur=12))]

    def setup(self, st):
        cam = Cam((0, 7, 34), (0, 7, 0), 34)
        self.runner = [silhouette(st, lambda s, p=p, g=g: s.fig(g, VN.V_RUN(p / 4.), yaw=80), cam, 256, 256) for p, g in enumerate((VN.WARRIOR, VN.YOUTH, VN.WARRIOR, VN.YOUTH))]
        r = np.random.default_rng(3); n = 26; self.climb = r.uniform(0, 1, n)

    def frame(self, f, st):
        st.clear('#000', f=f)
        for a, fn in ((78, self.land), (74, self.topple), (70, self.crack), (66, self.ray), (60, self.small), (30, self.rise), (0, self.eye)):
            if f >= a: return fn(f, st, st.t)

    # ---------------------------------------------------------------- a landscape that is a lid
    def eye(self, f, st, t):
        k = ease_io(f / 29., 1.6); zoom = keys(f, [(0, 1.95), (11, 1.85), (19, 1.02, 'io'), (29, 1.13, 'in')]); at = keys(f, [(0, (-.25, -.12)), (11, (-.22, -.10)), (19, (0., -.02), 'io'), (29, (-.02, -.05))])
        op = keys(f, [(11, 0.), (12, .17), (13, .25), (16, .30), (19, 1.12, 'out'), (22, 1.0), (25, .98), (28, .74, 'io'), (29, .72)]); pu = keys(f, [(12, .95), (18, .9), (22, .12, 'out'), (29, .22)]); gz = keys(f, [(15, (-.5, -.4)), (20, (-.45, -.2)), (22, (.30, .05), 'snap'), (25, (.30, .05)), (27, (0., -.02), 'snap'), (29, (0., 0.))])
        if 17 <= f: x, y = shake(f, .006 + .02 * decay((f - 18) / 24., 6.), .9); at = (at[0] + x, at[1] + y)
        fl = .9 * smooth(16, 21, f)
        KB.eye(st, open=op, gaze=gz, pupil=pu, flame=fl, zoom=zoom, at=at, roll=keys(f, [(0, -5.), (19, -1.5), (29, 0.)]), key='#ffa860', dark=.35 + .3 * k, skin=('#a8623a', '#4a2022'), iris=('#e8961c', '#5a1406'), t=t)
        dune = 1 - smooth(9, 15, f)
        if dune > 0: st.paint(DUNE, 'over', amt=float(dune), lift=float(.16 * smooth(9, 15, f) - .0016 * f))
        rr = math.radians(-5 if f < 12 else -1.5); S = lambda x, y: (960 + (x * zoom + at[0]) * 540, 540 - (y * zoom + at[1]) * 540)
        # the runners: on the slope, then in the eye
        if f < 17:
            for i in range(13):
                x = -1.15 + .15 * i + .0085 * f + .03 * math.sin(i * 5.1); y = .10 - .10 * x * x + .05 * x + .012 * math.sin(i * 3.3); j = max(0, f - 11); y += .16 * op + (.030 * j - .0052 * j * j) * (1 if j else 0); px, py = S(x, y); h = abs(math.sin((f * .55 + i) * 1.6)); sz = .30 + .05 * math.sin(i * 2.7)
                st.plate(self.runner[(f // 2 + i) % 4], px, py - 34 - 9 * h, sz * 1.15, rot=-2 + 22 * math.sin(i * 2 + f) * (j > 0), tint=(.055, .015, .02), srgb=False, alpha=1 - smooth(14, 17, f))
        if f >= 17:
            g = np.array([gz[0] * .42, gz[1] * .22 + .06])
            for i in range(7):
                a = -2.42 + .23 * i + .018 * (f - 17) + .03 * math.sin(i * 4.); R = .335; x, y = g[0] + R * math.cos(a), g[1] + R * math.sin(a); px, py = S(x, y); sz = (.20 + .02 * math.sin(i * 3)) * zoom * .9; h = abs(math.sin((f * .6 + i) * 1.6))
                st.plate(self.runner[(f // 2 + i) % 4], px, py - 4 * h, sz * 1.0, rot=math.degrees(-a - math.pi / 2) * .75, tint=(.02, .006, .008), srgb=False, alpha=.85 * smooth(17, 20, f))
            px, py = S(g[0] + .02, g[1] - .23); FX.particles(st, np.array([[px + 20 * math.sin(i * 2.2 + t * 2) * zoom, py - ((t * 60 * (1 + .2 * i) + 37 * i) % 130) * zoom] for i in range(7)]), 3.2 * zoom, '#ffc060', 'ember', alpha=.8 * smooth(18, 21, f))
        FX.drift(st, 26, ((0, 0, 0), (1920, 1080, 1)), t, 'ash', size=3.2, col='#c8783a', fall=-30, sway=40, seed=3, wind=(160, 0, 0)) if 0 else None
        r = np.random.default_rng(5); n = 70; P = np.c_[np.mod(r.uniform(0, 2100, n) + t * r.uniform(120, 380, n), 2100) - 90, r.uniform(120, 1080, n) + 14 * np.sin(t * 3 + r.uniform(0, 6, n))]; FX.particles(st, P, r.uniform(1.5, 4.2, n), '#e8a050', 'ash', alpha=.55 * (1 - .6 * smooth(12, 18, f)))
        dustbank(st, .55 * (1 - smooth(8, 16, f)) + .10, .5, 1.1, colA='#e89a50', colB='#7a301c', seed=1., speed=.35)
        # sand running off the lid as it opens
        if 12 <= f < 26:
            n = 130; q = np.random.default_rng(8); x = q.uniform(-1.2, 1.2, n); a = (f - 12 - q.uniform(0, 5, n)) / 24.; m = a > 0; up = .60 * np.maximum(0, 1 - (x / 1.24) ** 2) ** .62 * op; px = 960 + (x * zoom + at[0]) * 540; py = 540 - ((up - .02) * zoom + at[1]) * 540 + 1500 * a * a + 30 * a; FX.particles(st, np.c_[px, py][m], q.uniform(2, 6, n)[m], '#e8a864', 'streak', vel=np.c_[0 * a, 26 + 130 * a][m], alpha=np.clip(1 - a * 2.6, 0, 1)[m])
        return st.finish(bloom=.45, thr=.9, vig=.55, contrast=1.12, satu=1.05)

    # ---------------------------------------------------------------- the giant
    def lit(self, **k): return war_light(**{**dict(key=(-.4, .5, .75), keyCol=(.80, .50, .32), amb='#6a3a58', rim=(.1, .45, -.9), rimCol=(2.3, 1.1, .36), fogCol='#c85a2a', fog=(.0018, 70., .010, 0.), inkRef=9., ink=3.4), **k})

    def giant(self, st, pose, at, yaw, face, L, cam, hang=1.0, f=0, scale=Z, thrash=1.):
        """him, and (in a second layer) those who hang on him.  returns the solved figure and the perches that can be seen"""
        st.open(cam, L, far=3000); ground(st); S = st.fig(KB.KUMBHA, pose, at=at, yaw=yaw, scale=scale, face=face); st.close()
        pr = [(p, n) for k, (p, n) in KB.perches(S).items() if k != 'helm' and (cam.eye - p) @ n > .15 * np.linalg.norm(cam.eye - p)]
        return S, pr

    def hangers(self, st, pr, f, L, cam, amount=1., scale=.95):
        from dataclasses import replace as rep
        if amount <= 0: return
        st.open(cam, rep(L, inkRef=1.4, ink=2.4, shadow=False, rimCol=(1.2, .6, .22)), far=3000)
        K = [VN.WARRIOR, VN.YOUTH, VN.LANGUR, VN.YOUTH2, VN.WARRIOR2, VN.LANGUR2]
        for i, (p, n) in enumerate(pr):
            if i / max(1, len(pr)) > amount: continue
            h = (f // 2 + i) % 2; sw = V(math.sin(i * 2.1 + f * .25), 0, math.cos(i * 1.7 + f * .2)) * .25; st.fig(K[i % 6], (VN.V_CLIMB if h else VN.V_CLIMB2), M=PR.place(p + n * .4 * scale - V(0, 7.5, 0) * scale, V(0, 1, 0) + sw, -n + V(0, .01, 0), scale), face=ROAR)
        st.close()

    def rise(self, f, st, t):
        T = keys(f, [(30, .26), (32, .24), (38, .56, 'io'), (40, .60), (47, .97, 'io'), (49, 1.0)]); pose = KB.KB_RISE(T); dark = smooth(55.5, 57, f)
        low = dict(pel=(0, 5.0, .6), lf=(2.5, 1.15, 2.0), rf=(-2.4, 1.1, -2.0), lkn=(.8, .3, 1), rkn=(-.8, 0, 1), lft=(30, 0), rft=(-34, 16), lh=(5.0, 4.0, -.8), lel=(.8, .4, -.6), lhand='claw', rhand='claw')
        A = KB.KB_STAND.set(pelr=(-20, -2, 0), cher=(-30, 18, 0), hedr=(44, 18, 0), rh=(-7.6, 10.5, -1.0), rel=(-1, .4, -.2), rhand='open', rfing=(-.4, .5, .6), rpalm=(.8, -.2, .5), lh=(4.2, 9.0, 3.4))
        LEAN = KB.KB_STAND.set(cher=(0, 24, 0), hedr=(0, 14, 0))
        B = Pose(**{**KB.KB_STAND.__dict__, **low, 'pelr': (-8, 22, 0), 'cher': (-14, 34, 0), 'hedr': (16, -46, 0), 'rh': (-4.4, 2.2, 6.0), 'rel': (-1, .2, 0), 'rhand': 'open', 'rfing': (.5, .25, .8), 'rpalm': (.9, -.1, .2)}); C = B.set(pelr=(8, 22, 0), cher=(22, 36, 0), hedr=(-18, -44, 0), rh=(4.2, 1.9, 6.4), rfing=(.95, .15, .2), rpalm=(.2, -.2, .95))
        BIG = KB.KB_STAND.set(cher=(0, 22, 0), hedr=(0, 12, 0), lh=(7.0, 9.6, 3.6), rh=(-7.0, 9.6, 3.6), lel=(.7, .7, -.5), rel=(-.7, .7, -.5), lhand='claw', rhand='claw', lfing=(.1, -.35, .9), rfing=(-.1, -.35, .9), lpalm=(-.4, -.8, .3), rpalm=(.4, -.8, .3), shrug=(.6, .6), lf=(2.4, 1.15, .9), rf=(-2.4, 1.15, .3))
        if f >= 40: pose = pose.mix(LEAN, smooth(41, 47, f))
        if f >= 46: pose = keys(on2(f) if f < 52 else f, [(46, pose), (50, A, 'io'), (51, A), (53, B, 'in'), (54, B.set(pelr=(0, 22, 0), cher=(4, 35, 0), hedr=(0, -46, 0), rh=(.4, 1.7, 7.3), rfing=(.25, .12, .95), rpalm=(.9, -.1, -.2)), 'linear'), (55, C, 'linear')])
        if f >= 56: pose = BIG
        G = V(6, 0, -4); e0 = smooth(30, 55, f); cam = Cam(V(-4 + 4 * e0, 1.7, 118 - 3 * e0), V(3, lerp(44, 78, ease_io(smooth(30, 48, f))), -14), 64, roll=-3 + 5 * e0)
        if f >= 56: cam = Cam(V(0, 1.7, 122 - .5 * (f - 56)), V(5, 92, -4), 68, roll=-1)
        stomp = max(decay((f - 38) / 24., 7.) if f >= 38 else 0, decay((f - 47) / 24., 7.) if f >= 47 else 0, .8 * decay((f - 56) / 24., 7.) if f >= 56 else 0); cam = shaken(cam, f, .10 + 1.0 * stomp, .9); st.cam = cam
        S0 = st.fig(KB.KUMBHA, BIG if f >= 56 else LEAN, at=G, scale=Z, draw=False)
        st.paint('sky.frag', **SKY(WAR, sunDir=(0, .3, -1), sunR=0., sunGlow=.15, rays=0., halo=0., cov=.55, cy0=.03, cy1=.45, cHor='#d8682a'))
        sx, sy, _ = cam.project(S0.head((0, .5, 0))); sun(st, (sx, sy), 150 + 14 * dark, rays=.8)
        L = self.lit(keyCol=tuple(np.array([.80, .50, .32]) * (1 - .72 * dark)), amb=tuple(np.array(hexc('#6a3a58')) * (1 - .6 * dark)), fog=(.0018 * (1 - .6 * dark), 70., .010, 0.)); lid = smooth(30, 36, f)
        S, pr = self.giant(st, pose, G, -4, Face(frown=1., smile=-.5, mouth=.25 + .65 * smooth(44, 50, f), teeth=.6, lid=lid, gy=-.5, glow=.35 + .5 * dark), L, cam)
        self.hangers(st, pr[:10], f, L, cam, .4 + .6 * smooth(34, 44, f) if f < 52 or f >= 56 else .5, scale=1.15)
        # dust sheets off him; he stands up out of it
        e = smooth(30, 58, f); r = np.random.default_rng(4)
        pts = np.array([S.chest((x, y, z)) for x, y, z in ((2.6, 1.8, .4), (-2.6, 1.8, .4), (1.2, .4, 2.), (-1.2, .4, 2.), (0, -1.4, 2.4))] + [S.joint(5), S.joint(8), S.joint(6), S.joint(9)]); n = 420; b = r.integers(0, len(pts), n); ph = np.mod(r.uniform(0, 1, n) + t * 1.3, 1.); P = pts[b] + r.normal(0, 4.0, (n, 3)) * V(1, .3, 1) - np.c_[0 * ph, 70 * ph ** 1.7, 0 * ph]; FX.particles(st, P, .32, '#e8a860', 'streak', vel=np.c_[0 * ph, -(3 + 12 * ph), 0 * ph], alpha=.7 * (1 - ph) * (1 - .7 * e))
        n = 70; a = r.uniform(0, 6.28, n); R = r.uniform(14, 66, n); ph = np.mod(r.uniform(0, 1, n) + t * .55, 1.); P = np.c_[G[0] + np.cos(a) * R, 2 + 26 * ph * (1 - .55 * e), G[2] + np.sin(a) * R]; puffs(st, P, 10 + 16 * ph, col=('#d8924c', '#7a3820'), alpha=.6 * (1 - ph) ** .8 * np.minimum(1, ph * 6) * (1 - .55 * e), seed=6, soft=10)
        # rocks thrown from below
        for i, (hf, tgt) in enumerate(((36, (1.2, .3, 2.2)), (41, (-2.4, 1.4, 1.2)), (45, (.4, -1.2, 2.6)), (49, (2.4, 1.2, 1.4)))):
            p1 = S.chest(tgt); p0 = V(-40 + 26 * i, 2, 60 - 6 * i); q = (f - hf + 8) / 8.
            if 0 <= q < 1:
                p = lerp(p0, p1, q) + V(0, 30 * q * (1 - q), 0); st.open(cam, self.lit(inkRef=2., shadow=False)); boulder(st, p, 2.6, i, spin=q * 6); st.close()
            a_ = (f - hf) / 24.
            if 0 <= a_ < .6: FX.burst(st, 40, p1, a_, speed=34, grav=44, size=.9, seed=i, col='#5a3a2a', kind='ash', life=.6); puffs(st, p1 + r.normal(0, 1, (14, 3)) * (2 + 18 * (1 - math.exp(-a_ * 6))), 3.5 + 16 * a_, col=('#d89a60', '#8a4a2a'), alpha=max(0, .55 - 1.1 * a_), seed=i, soft=3); FX.burst(st, 24, p1, a_, speed=40, grav=20, size=.35, seed=i + 9, life=.4)
        # those who flee past us
        from dataclasses import replace as rep
        st.open(cam, rep(L, inkRef=1., fog=(0, 0, 0, 0), keyCol=(.34, .20, .13), amb='#3a1c30', rimCol=(2.2, 1.0, .34)))
        K = [(VN.arm(VN.WARRIOR, 3), -7.5, 74, 0., 10), (VN.LANGUR2, 10.5, 66, .4, -10), (VN.YOUTH, -17, 50, .2, 14), (VN.JAMBAVAN, 22, 44, .7, -16), (VN.YOUTH2, 5.5, 36, .55, 4)]
        for g, x, z, ph, y in K:
            for k in (0, 1):
                z2 = z + 2.3 * (f - 30) - 62 * k
                if 1.5 < cam.eye[2] - z2 < 90 and z2 > 24 and f < 56: st.fig(g, VN.V_RUN(on2(f) / 11. + ph + k * .3), at=(x, 0, z2), yaw=y, face=Face(frown=.4, mouth=.4, lid=1.1))
        st.close()
        footdust(st, 26, ((-24, .5, 60), (24, 1.5, 110)), t, size=2.0, rise=2.4, alpha=.40, seed=3)
        FX.embers(st, 50, ((-30, 0, 40), (30, 10, 112)), t, rise=5., size=.10, seed=5, life=2.)
        dustbank(st, .75 * (1 - smooth(30, 46, f)) + .22, .30 + .3 * e, 1.05, seed=3., speed=.3)
        if 52 <= f <= 55: IM.whip(st, [20, 46, 60, 40][f - 52], 0)
        return st.finish(bloom=.5, thr=.9, vig=.55, contrast=1.12, satu=1.05)

    # ---------------------------------------------------------------- one small man
    def rama_(self, st, f, at, yaw, draw, arrow=True, cloth=.35):
        t = st.t; P = PZ.archer(draw); P = P.set(lh=(P.lh[0] - .9, P.lh[1] + 2.9, P.lh[2]), rh=(P.rh[0] + .1, P.rh[1] - .4, P.rh[2]), cher=(-20, 0, -12), hedr=(74, 0, 4), lel=(0, -1, -.2))
        S = st.fig(rama.EXILE, P, at=at, yaw=yaw, face=Face(frown=.3, smile=.05, lid=.85, gx=.2)); nk, tip, aim = PR.bow_and_arrow(st, S, half=5., arrow=arrow, release=0. if arrow else 1.); st.fig(PR.QUIVER, M=PR.place(S.chest((.5, .5, -1.2)), S.d((-.35, 1, -.12)), S.d((0, 0, -1)), 1.))
        for an, ln, wd, col in ((lambda tt: S.chest((-1.2, 1.2, -.8)), 9., 1.3, ('#c8431f', '#4a1020', '#f2c24a')), (lambda tt: S.pelvis((-.6, .5, -.9)), 6.5, 1., ('#e8a22c', '#7a3a14', '#b3202a'))):
            Q = CL.lag(an, t, n=16, length=ln, wind=(-.8, -.02, -.1), grav=.22, wave=cloth, freq=.7); st.mesh(*CL.strip(Q, np.linspace(wd * .6, wd, 16), up=(0, 1, .3), m=6, curl=.12, n=36), kind=1, col=col, cls=8)
        return S, nk, tip, aim

    def small(self, f, st, t):
        cam = Cam(V(12, 5.5, 92 - .35 * (f - 60)), V(17, 23, 0), 40); st.cam = cam
        st.paint('sky.frag', **SKY(WAR, sunDir=(-.16, .17, -1), sunR=.10, sunGlow=.5, rays=.25, cov=.4, cHor='#c85a28', cMid='#7a1418'))
        L = self.lit(fog=(.0040, 60., .006, 0.), rim=(-.5, .4, -.7), key=(-.6, .45, .6)); step = keys(f, [(60, 0.), (65, 1., 'io')]); P = KB.KB_STAND.set(lf=(1.75, 1.15 + 2.2 * math.sin(math.pi * .5 * step), .5 + 2.6 * step), lft=(28, 20 * step))
        S, pr = self.giant(st, P, V(56, 0, -42), -38, Face(frown=.9), L, cam); self.hangers(st, [(p, n) for p, n in pr if p[1] < 110], f, L, cam, 1.)
        footdust(st, 40, ((20, 3, -70), (95, 8, -10)), t, size=14, rise=7, alpha=.30, seed=5)
        st.open(cam, war_light(fog=(0, 0, 0, 0), keyCol=(1.1, .85, .62), rim=(-.5, .4, -.7), rimCol=(1.6, .9, .4))); R, nk, tip, aim = self.rama_(st, f, (-19, 0, 14), 6, 1.0 + .03 * smooth(60, 65, f)); st.close()
        FX.particles(st, tip[None], .9 + .5 * smooth(61, 65, f), '#fff0c8', 'glint', alpha=.9)
        FX.drift(st, 40, ((-70, 0, -60), (90, 60, 30)), t, 'ash', size=.22, col='#c87a3a', fall=.8, sway=1., seed=4, wind=(3, 0, 0)); dustbank(st, .30, .78, 1.1, seed=5.)
        return st.finish(bloom=.45, thr=.9, vig=.55, contrast=1.1)

    def ray(self, f, st, t):
        a = f - 66; cam = Cam(V(24, 36, 300 - 2 * a), V(24, 88, 0), 42); cam = shaken(cam, f, 2.2 * decay(a / 24., 9.) if a >= 1 else 0, .9); st.cam = cam
        st.paint('sky.frag', **SKY(WAR, sunDir=(.36, .36, -1), sunR=.15, sunGlow=.5, rays=.4, cov=.5, cy1=.3, cHor='#c85a28', cMid='#7a1418'))
        L = self.lit(fog=(.0010, 120., .010, 0.)); pose = KB.KB_FALL(keys(f, [(66, .02), (67, .03), (69, .20, 'out')])); G = V(104, 0, -30); S, pr = self.giant(st, pose, G, -62, Face(frown=.9, mouth=.5 if a < 1 else 1., sad=.5 * (a >= 1), lid=1.2), L, cam); self.hangers(st, pr, f, L, cam, 1., scale=1.3)
        J = S.chest((0, -.2, 2.35)); R0 = V(-112, 0, 22)
        st.open(cam, war_light(fog=(0, 0, 0, 0), inkRef=1.5, keyCol=(1.3, 1., .7))); R, nk, tip, aim = self.rama_(st, f, R0, 6, 1. if a < 1 else 1.06, arrow=False); st.close()
        g = R.palm('L', 0, .62, .3); d = nz(J - g); far = np.linalg.norm(J - g); q = min(1., (a + .75) / 1.4)
        footdust(st, 60, ((30, 4, -70), (170, 14, 0)), t, size=24, rise=12, alpha=.26, seed=5); dustbank(st, .4, .72, 1.1, seed=5.)
        fade = 1 - .28 * max(0, a - 1)
        # the line: from past the left edge, through his bow, to the jewel
        s0 = g - d * (0 if a == 0 else 8); e = g + d * far * q; FX.ribbon(st, np.array([s0, lerp(s0, e, .5), e]), [1.2, 4.2, 1.8], 'light', '#ff9a30', '#fff8e0', amt=fade); FX.ribbon(st, np.array([s0, e]), 9., 'light', (1., .42, .10), (1., .7, .3), amt=.30 * fade); FX.particles(st, g[None], 14 - 3 * a, '#fff0c8', 'spark', alpha=fade)
        if a >= 2: FX.ribbon(st, np.array([J - d * 6, J + d * 220]), [3., .8], 'light', '#ff9a30', '#fff0c8', amt=.75 * fade)
        if q >= 1: FX.particles(st, J[None], 40 - 4 * a, '#fff4d0', 'spark', alpha=fade); FX.burst(st, 120, J, (a - .5) / 24., speed=150, grav=30, size=1.2, seed=4, col='#ffcf6a', kind='flake', life=.8); FX.burst(st, 70, J, (a - .5) / 24., speed=190, grav=0, size=.8, seed=5, life=.4); x, y, _ = cam.project(J); IM.shock(st, (float(x), float(y)), 40 + 330 * a, 60, 40)
        if f == 67: IM.inkflash(st, '#12040a', '#c8281a', '#fff6dc', lo=.26, hi=.66)
        return st.finish(bloom=.75, thr=.85, vig=.5, contrast=1.1)

    def crack(self, f, st, t):
        a = f - 70; pose = KB.KB_FALL(.2); G = V(0, 0, 0); S = st.fig(KB.KUMBHA, pose, at=G, scale=Z, draw=False); J = S.chest((0, -.2, 2.4)); fw = S.d(S.u['Bc'].T @ V(0, 0, 1)); fw = S.d(np.array([0, 0, 1.]) @ S.u['Bc']); cam = Cam(J + fw * (64 - 5 * a) + V(10, -14, 0), J + V(0, 1, 0), 44, roll=8 - 2 * a); cam = shaken(cam, f, .9, .9, 3); st.cam = cam
        st.paint('sky.frag', **SKY(WAR, sunDir=(.1, .5, -1), sunR=0., sunGlow=.3, rays=.3, cov=.4, cMid='#5a1016', cHor='#8a2c18'))
        lk = .5 + .5 * a / 3.; L = self.lit(keyCol=(.30, .17, .12), amb='#34182e', pts=[(J + V(0, 0, 8), 16., tuple(np.array([.8, .36, .10]) * lk))], fog=(0, 0, 0, 0), shadow=False)
        st.open(cam, L, far=2000); S = st.fig(KB.KUMBHA, pose, at=G, scale=Z, face=Face(mouth=1., sad=.7, lid=1.25)); st.close()
        jx, jy, jz = cam.project(J); ppu = cam.px(J)
        r = np.random.default_rng(11); grow = [.34, .62, .86, 1.][min(a, 3)]
        zb = st.depth()

        def on_him(P):                                                     # a seam ends where his body ends
            P = np.asarray(P); xi, yi = np.clip(P[:, 0].astype(int), 0, W - 1), np.clip(P[:, 1].astype(int), 0, H - 1); bad = np.nonzero(zb[yi, xi] > jz + 90)[0]; return P[:bad[0]] if len(bad) else P
        for b in range(15):                                              # the gold seams, branching from the jewel, as a mended bowl
            an = b / 15 * 6.283 + r.uniform(-.16, .16); Ln = r.uniform(24, 46) * grow; n = 15; P = [np.array([jx, jy])]; h = an
            for i in range(n): k = an + r.uniform(-.75, .75); P.append(P[-1] + np.array([math.cos(k), math.sin(k) * .86]) * Ln / n * ppu)
            P = on_him(P); w = np.linspace(1.0, .10, 16)[:len(P)] * ppu * .42
            if len(P) < 3: continue
            FX.ribbon(st, P, w * 2.6, 'light', (1., .40, .06), (1., .55, .15), amt=.30); FX.ribbon(st, P, w * 1.1, 'light', '#ff9a20', '#fff2c0'); FX.ribbon(st, P, w * .35, 'bolt', '#ffe6a0', '#ffffff')
            for k in (4, 7, 10):
                if k >= len(P): continue
                q = [P[k]]; hh = an + r.choice([-1, 1]) * r.uniform(.6, 1.1)
                for i in range(5): g = hh + r.uniform(-.7, .7); q.append(q[-1] + np.array([math.cos(g), math.sin(g)]) * Ln * .06 * ppu)
                FX.ribbon(st, on_him(q), np.linspace(.6, .06, 6)[:max(2, len(on_him(q)))] * ppu * .34, 'light', '#ff9a20', '#fff0c0')
        FX.particles(st, np.array([[jx, jy]]), ppu * (5 + 3 * a), '#fff6dc', 'spark'); FX.particles(st, np.array([[jx, jy]]), ppu * (6 + 3 * a), '#ffb050', 'ember', alpha=.5)
        leafburst(st, J + V(0, 0, 3), .04 + a / 24., speed=90, n=70, size=.6, seed=6, grav=30)
        IM.zoomblur(st, (float(jx), float(jy)), .012 + .018 * a)
        return st.finish(bloom=.6, thr=.9, vig=.5, contrast=1.1)

    def topple(self, f, st, t):
        """from behind and below: he comes down on us"""
        a = f - 74; T = [.28, .46, .62, .78][a]; G = V(0, 0, 0); S0 = st.fig(KB.KUMBHA, KB.KB_FALL(T), at=G, scale=Z, draw=False); hd = S0.head((0, 0, 0)); cam = Cam(V(14, 2.2, -142), V(0, hd[1] * .62 + 8, hd[2] * .5 - 30), 62, roll=-6 + 3 * a); cam = shaken(cam, f, .5, .9); st.cam = cam
        st.paint('sky.frag', **SKY(WAR, sunDir=(.25, .5, 1), sunR=.14, sunGlow=.7, rays=.7, cov=.4, cHor='#c85a28'))
        L = self.lit(key=(.4, .5, -.75), rim=(0, .45, .9), keyCol=tuple(np.array([.6, .36, .24]) * (1 - .2 * a)), fog=(.0010, 60., .01, 0.)); S, pr = self.giant(st, KB.KB_FALL(T), V(0, 0, 0), 0, Face(mouth=1.), L, cam); self.hangers(st, pr, f, L, cam, .6)
        from dataclasses import replace as rep
        st.open(cam, rep(L, inkRef=1., fog=(0, 0, 0, 0), keyCol=(.4, .24, .16), amb='#3a1c30'))
        for g, x, z, ph, y in ((VN.WARRIOR, -5, -112, 0., 172), (VN.LANGUR2, 30, -104, .4, 190), (VN.YOUTH, 22, -92, .2, 200), (VN.YOUTH2, -24, -96, .7, 165)): st.fig(g, VN.V_RUN(f / 9. + ph), at=(x, 0, z - 2.4 * a), yaw=y, face=Face(sad=.6, mouth=.8, lid=1.2))
        st.close()
        r = np.random.default_rng(6); n = 60; P = np.c_[r.uniform(-50, 50, n), r.uniform(20, 150, n) - 18 * a, r.uniform(-80, 0, n)]; FX.particles(st, P, .5, '#ffcf6a', 'flake', rot=r.uniform(0, 6, n) + a, seed=r.uniform(0, 1, n)); footdust(st, 30, ((-30, .5, -90), (30, 2, -40)), t, size=3, rise=3, alpha=.4, seed=3); IM.whip(st, 0, 10 + 9 * a); dustbank(st, .25 + .06 * a, .55, 1.05, seed=3.)
        return st.finish(bloom=.5, thr=.9, vig=.5, contrast=1.14, fade=.07 * a)

    # ---------------------------------------------------------------- the ground
    def land(self, f, st, t):
        a = (f - 78) / 24.; cam = Cam(V(0, 5.0, 150), V(0, lerp(18, 20, a), 0), 42, roll=2.5 * math.sin(a * 9) * decay(a, 3.)); cam = shaken(cam, f, 5.0 * decay(a, 4.5) + .3, .9); st.cam = cam
        st.paint('sky.frag', **SKY(WAR, sunDir=(-.22, .20, -1), sunR=.13, sunGlow=.6, rays=.45, cov=.45, cHor='#d8682a'))
        L = self.lit(rim=(-.4, .4, -.8), fog=(.0016, 120., .010, 0.)); bounce = 6 * max(0, math.sin(a * 11)) * decay(a, 7.); S, pr = self.giant(st, KB.KB_FALL(1.), V(74, bounce - 3, -30), 82, Face(lid=0., mouth=.5), L, cam)
        # the wave in the ground, and everyone it throws up
        rad = 22 + 190 * (1 - math.exp(-a * 2.6)); n = 110; an = np.linspace(0, 6.283, n, endpoint=False); r = np.random.default_rng(7); jit = r.uniform(.9, 1.06, n); W_ = np.c_[np.cos(an) * rad * jit * 1.5, r.uniform(2, 9, n), -24 + np.sin(an) * rad * jit]; W_ = W_[W_[:, 2] > -60]
        from dataclasses import replace as rep
        st.open(cam, rep(L, inkRef=1.2, shadow=False, keyCol=(.62, .40, .26)))
        q = np.random.default_rng(12); K = [VN.WARRIOR, VN.YOUTH, VN.LANGUR, VN.YOUTH2, VN.LANGUR2, VN.WARRIOR2]
        for i in range(16):
            x, z = q.uniform(-58, 58), q.uniform(40, 104); d = math.hypot(x / 1.5, z + 24); ta = -math.log(max(.03, 1 - (d - 22) / 190)) / 2.6; b = a - ta + .085
            if b < 0 and f < 91: st.fig(K[i % 6], VN.V_RUN(on2(f) / 11. + i * .17), at=(x, 0, z + 14 * a), yaw=q.uniform(-30, 30), face=Face(sad=.5, mouth=.6))
            elif b >= 0:
                v = q.uniform(70, 112); y = v * b - 95 * b * b; w = q.choice([-1, 1]) * q.uniform(380, 720)
                if f < 91: st.fig(K[i % 6], VN.V_CHEER(.5) if i % 2 else VN.V_CLIMB, at=(x * (1 + .6 * b), max(0, y), z + 14 * a + 70 * b), yaw=40 * i, pitch=w * b * .6, roll=20 + w * b, face=Face(sad=.4, mouth=.8, lid=1.1))
        for i in range(16):
            x, z = q.uniform(-70, 70), q.uniform(10, 100); d = math.hypot(x / 1.5, z + 24); b = a + math.log(max(.03, 1 - (d - 22) / 190)) / 2.6
            if b > 0 and f < 90: v = q.uniform(40, 80); y = v * b - 52 * b * b; boulder(st, V(x * (1 + b), max(.5, y), z + 60 * b), q.uniform(.8, 2.6), i % 5, spin=b * q.uniform(4, 12))
        st.close()
        g = 1 - math.exp(-a * 3.2); n = 130; x = r.normal(0, 1, n); P = np.c_[8 + x * (54 + 60 * g), r.uniform(0, 1, n) ** 1.4 * (8 + 62 * g), -30 + r.uniform(-26, 10, n) + 60 * g * r.uniform(0, 1, n)]; puffs(st, P, (7 + 15 * g) * r.uniform(.6, 1.2, n), col=('#eab26a', '#8a4426'), alpha=min(1., a * 20) * .9 * (1 - .3 * g), seed=8, soft=12)
        puffs(st, W_, (2.6 + 5.5 * g) * r.uniform(.6, 1.2, n)[:len(W_)] if len(W_) <= n else 8., col=('#eab26a', '#9a502a'), alpha=.9 * (1 - .4 * a), seed=9, soft=5)
        FX.drift(st, 60, ((-60, 0, 20), (60, 60, 130)), t, 'flake', size=.4, col='#ffcf6a', fall=9, sway=2, seed=4)
        x, y, _ = cam.project(V(30, 10, -20))
        if f > 79: IM.shock(st, (float(x), float(y)), 60 + 2600 * a, 160, 90 * decay(a, 3), squash=.42); IM.zoomblur(st, (float(x), float(y)), .10 * decay(a, 10))
        dustbank(st, 1.25 * smooth(85, 94, f), lerp(1.0, -.9, smooth(84, 94, f)), lerp(1.4, .15, smooth(84, 94, f)), colA='#e8a458', colB='#7a3a20', seed=7., speed=.8)
        dustbank(st, .9 * smooth(89, 94, f), -1., -.5, colA='#d8924a', colB='#6a2e1a', seed=3.3, speed=.5)
        if f == 78: IM.inkflash(st, '#0e0408', '#d8301a', '#fff0cc', lo=.30, hi=.60)
        if f == 79: IM.inkflash(st, '#0e0408', '#fff0cc', '#e8842a', lo=.30, hi=.62)
        return st.finish(bloom=.5, thr=.9, vig=.5, contrast=1.12, fade=.8 * smooth(91, 97, f), fadeCol='#2a0e0a')
