"""d4 (126): flight.  Joy over a turquoise sea, his hand cutting a line of spray (f0-41); up through the cloud bank (f42), a moment of calm gold (f48-60); a shadow under the water (f60); Surasa's mouth, big as a harbour (f66); he shrinks in three pops (f74 76 78), a spark darts in between the teeth and is out again as the jaws clap (f90); then low and fast over a darkening sea to a golden glimmer (f96-126)."""
from lau.shot import *
from lau.look import *
from chars import hanuman as HM, serpent as SP, birds as BD
from shots import d_kit as K

SP.SCALE = SP.SCALE.replace('uniform vec2 rep;', 'uniform vec4 rep;')           # st.mesh pads `rep` to four numbers
SUN = nz(V(.90, .20, -.28))                                      # ahead of him: he flies along +x


def az(a): a = math.radians(a); return V(math.sin(a), 0, math.cos(a))


class Shot(ShotBase):
    id = 'd4'; n = 126
    EVENTS = [(0, 'wind rush', dict(dur=60)), (0, 'sea', dict(dur=42)), (10, 'joyful cry', {}), (16, 'hand cuts water', dict(dur=20)), (20, 'sea birds', dict(dur=16)), (36, 'whoosh up', {}), (42, 'bursts through cloud', {}), (48, 'calm', dict(dur=12)), (60, 'deep rumble', dict(dur=8)), (66, 'serpent rises', dict(dur=10)), (66, 'water pours', dict(dur=20)), (74, 'shrinks', {}), (76, 'shrinks', {}), (78, 'shrinks', {}), (79, 'spark darts in', {}), (82, 'spark circles', dict(dur=6)), (88, 'spark darts out', {}), (90, 'jaws clap', {}), (90, 'spray', dict(dur=10)), (96, 'low flight', dict(dur=30)), (108, 'glimmer', {})]

    def setup(self, st):
        r = np.random.default_rng(3); n = 190; self.c0 = np.c_[r.uniform(-160, 420, n), r.uniform(0, 60, n) * 0, r.uniform(-260, 260, n)]; self.cw = r.uniform(26, 64, n); self.cv = r.integers(0, 8, n); self.cf = r.choice([-1., 1.], n); self.cj = r.normal(0, 1, (n, 3))
        self.k46 = r.uniform(.6, 1.3, 46)
        n = 330; q = 40 + 1500 * r.uniform(0, 1, n) ** 1.5; a = r.uniform(0, 6.283, n); self.f0 = np.c_[np.cos(a) * q, r.normal(0, 5, n), np.sin(a) * q]; self.fw = r.uniform(26, 56, n) * (1 + q / 260); self.fv = r.integers(0, 8, n); self.ff = r.choice([-1., 1.], n)

    def frame(self, f, st):
        st.clear('#000', f=f)
        if f < 48: return self.skim(f, st, st.t)
        if f < 60: return self.gold(f, st, st.t)
        if f < 66: return self.shadow(f, st, st.t)
        if f < 79: return self.mouth(f, st, st.t)
        if f < 88: return self.inside(f, st, st.t)
        if f < 96: return self.clap(f, st, st.t)
        return self.low(f, st, st.t)

    def sky(self, st, **k): K.sky(st, **{**dict(sunDir=tuple(SUN), sunR=.05, cZen='#2f8fa4', cMid='#8fc4b0', cHor='#ffe0a2', cLow='#f2cf9a', cov=.5, cy0=.03, cy1=.26, cscale=1.5, cLit='#fffaf0', cCM='#f6dcb4', cSh='#b8b8a8', cInk='#3a6a70', rays=.45), **k})

    def golden(self, k):
        mix = lambda a, b: tuple(np.array(hexc(a)) * (1 - k) + np.array(hexc(b)) * k); return dict(cZen=mix('#2f8fa4', '#d8784a'), cMid=mix('#8fc4b0', '#f6ac5c'), cHor=mix('#ffe0a2', '#ffe4a6'), cLow=mix('#f2cf9a', '#ffdc9a'), cLit=mix('#fffaf0', '#fff6dc'), cCM=mix('#f6dcb4', '#ffd8a0'), cSh=mix('#b8b8a8', '#f0a878'), cInk=mix('#3a6a70', '#a85a3a'))

    def light(self, **k): return K.light(**{**dict(key=tuple(nz(V(.75, .55, .42))), keyCol='#fff0d2', amb='#7f9cb8', rim=(.5, .5, -.7), rimCol=(1.2, .9, .5), bounceCol=(.06, .22, .22), envT='#fff0d0', envM='#ffd89a', envB='#2a9aa0', fog=(0, 0, 0, 0)), **k})

    # ------------------------------------------------ f0-47 over the sea, then up into the cloud
    def skim(self, f, st, t):
        g = on2(f); sp = 84.; off = V(sp * t, 0); up = smooth(35, 47, f); rise = 26 * smoother(35, 46, f) + 60 * ease_in((f - 38) / 10., 2.) * (f > 38)
        dip = keys(f, [(0, 3.2), (14, .9, 'io'), (17, .0, 'out'), (33, .15), (37, 1.0)]); bob = .22 * math.sin(t * 7); base = keys(f, [(0, -2.6), (10, -2.9), (17, -1.0, 'io'), (33, -1.0), (37, -2.2)]) + dip + bob + rise
        SK = HM.H_FLY2.set(pelr=(-6, 94, 0), cher=(-8, -16, -8), hedr=(20, -56, 6), lh=(2.0, 10.0, 8.8), lel=(.7, -.5, .2), lhand='open', lfing=(0, .2, 1), lpalm=(0, -1, .2), rh=(-2.9, 3.4, 4.2), rel=(-1, .3, -.6), rhand='open', rfing=(-.05, -.92, -.30), rpalm=(.25, -.3, .9), lf=(.8, 8.6, -6.4), rf=(-.8, 8.0, -6.0))
        A0 = HM.H_FLY_L.set(hedr=(18, -42, 4)); JOY = A0.set(lh=(4.4, 13.6, 6.6), rh=(-5.0, 10.6, 1.0), rhand='open', lhand='open', cher=(-6, -22, -6), hedr=(26, -44, 6), rel=(-.7, .6, -.3))
        LOOK = A0.set(hedr=(6, -62, 0), lh=(1.6, 14.4, 7.6), pelr=(-4, 48, 0), rh=(-3.4, 7.0, -.6))
        pose = keys(g, [(0, JOY), (6, JOY.set(cher=(-8, -26, -10))), (13, A0, 'io'), (17, SK, 'out'), (24, SK.set(hedr=(30, -54, 8), cher=(-12, -18, -12))), (32, SK), (36, A0.set(pelr=(-4, 74, 0), cher=(0, 8, 0), hedr=(0, -30, 0)), 'io'), (41, LOOK, 'out'), (48, LOOK.set(lh=(1.0, 15.2, 6.6)))])
        a = keys(f, [(0, 58.), (12, 34.), (24, 2.), (34, -28., 'io'), (41, -44.), (47, -52.)]); dist = keys(f, [(0, 19.5), (10, 21.), (20, 24.), (30, 23.), (40, 30.), (47, 36.)]); ey = keys(f, [(0, 5.4), (12, 3.8), (22, 2.6), (32, 2.9), (40, 8.), (44, 16.), (47, 30.)]) + .35 * rise
        tgt = V(1.4, 5.0 + dip + rise * .92, 0) + V(keys(f, [(0, 1.2), (12, 1.8), (24, 1.2), (36, 2.6)]), keys(f, [(0, 2.0), (12, .8), (20, -.2), (40, 2.)]), 0); cam = Cam(tgt * [1, 0, 1] + az(a) * dist + V(0, ey, 0), tgt, keys(f, [(0, 42.), (20, 40.), (40, 50.), (47, 56.)]), roll=keys(f, [(0, -8.), (14, 3.), (26, -4.), (36, 6.), (47, -10.)])); st.cam = cam
        self.sky(st, **({} if f < 38 else self.golden(smooth(38, 45, f)))); L = self.light()
        # birds that keep him company, then peel away
        u = f / 24.; n = 12; r = np.random.default_rng(6); B0 = np.c_[np.linspace(-13, 9, n) + r.normal(0, 1.2, n), 5.5 + r.uniform(0, 5.5, n), -r.uniform(7, 17, n)]; peel = np.clip((f - 20 - np.arange(n) * 1.1) / 18., 0, 1.4)[:, None]; B = B0 + V(0, 0, 0) + np.c_[np.sin(u * 2 + np.arange(n)), .6 * np.sin(u * 3 + np.arange(n) * 2), 0 * np.arange(n)] + peel ** 1.8 * np.array([-14, 15, -26.]); vel = np.tile(V(1, .05, 0), (n, 1)) + peel * np.array([-.2, .6, -1.3])
        st.open(cam, self.light(inkRef=.7), far=20000.); BD.flock(st, 'egret', B[::2], vel[::2], t, size=.95, rate=3.0, bank=34 * float(peel.mean()), seed=2); BD.flock(st, 'goose', B[1::2], vel[1::2], t, size=.85, rate=3.4, bank=34 * float(peel.mean()), seed=4); st.close()
        st.open(cam, L, far=20000.); S, TP, gem = K.giant(st, pose, at=(0, base, 0), yaw=90, pitch=-38 * up, roll=keys(f, [(0, -14.), (8, 10., 'io'), (16, -4.), (30, 3.), (36, -8.), (42, 6.)]), face=HM.VFace(smile=.85, lid=.95, mouth=keys(f, [(4, .1), (8, .55, 'out'), (14, .5), (18, .2)]), teeth=.5, gx=.2, spark=.8), tail='fly', tlen=15., vel=(30, 0, 0), wind=(-1.1, .06, .0), ring='L', gem=cam.eye, sashlen=5.6)
        hand = S.palm('R', 0, 1.9, 0); wet = smooth(15.5, 17.5, f) * (1 - smooth(33, 36, f)); K.ocean(st, off=off, wake=(hand[0], hand[2], 26., wet), wakeDir=(1, 0), sun=SUN, amp=.55, fr=.34); st.close()
        if wet > .01: self.spray(st, hand * [1, 0, 1] + V(0, .45, 0), t, wet)
        # speed: streaks of wind and drops past the lens
        r = np.random.default_rng(9); m = 60; P = np.c_[(r.uniform(0, 60, m) - sp * 1.4 * t * r.uniform(.8, 1.2, m)) % 60 - 30, r.uniform(.3, 9, m) + rise * .9, r.uniform(-9, 14, m)]; FX.particles(st, P, .035, '#fffaf0', 'streak', vel=np.tile(V(-3.4, 0, 0), (m, 1)), alpha=.45)
        if f >= 35: self.bank(f, st, t, base)
        w = smooth(42, 46.5, f); IM.zoomblur(st, (960, 480), .10 * w)
        return st.finish(bloom=.4, thr=.97, vig=.32, fade=.0, flash=.45 * smooth(45, 48, f), flashCol='#fff4dc', satu=1.08)

    def spray(self, st, at, t, k, n=620):
        """two curtains of water that stand up behind the hand, and everything they throw"""
        for sg in (-1, 1):
            for j in range(3):
                u = np.linspace(0, 1, 26); L, hh, w = (30, 23, 16)[j], (2.1, 3.0, 2.2)[j], (1.0, 1.25, .9)[j]; Q = at + np.c_[-u * L, hh * np.sin(math.pi * u ** .62) * (1 + .15 * np.sin(u * 30 - t * 40 + j * 2)) - .2, sg * (.15 + u * (1.4 + 1.5 * j))]; FX.ribbon(st, Q, np.r_[.12, np.linspace(.5, 1.2, 12), np.linspace(1.15, .1, 13)] * w, mode='wind', col=('#ffffff', '#e8fff8', '#c8f4ee')[j], amt=.95 * k, seed=j * 3.1 + sg)
        r = np.random.default_rng(1); ph = r.uniform(0, 1, n); lf = (t * r.uniform(1.6, 2.4, n) + ph) % 1.; T = lf * .62; sg = r.choice([-1, 1], n); v = np.c_[-r.uniform(16, 44, n), r.uniform(2.5, 11.5, n), sg * r.uniform(.5, 6.0, n)]; P = at + v * T[:, None] + V(0, -14, 0) * (T * T)[:, None]; al = np.clip((1 - lf) * 2.4, 0, 1) * k * (P[:, 1] > .1); FX.particles(st, P, r.uniform(.05, .19, n) * (1 - .4 * lf), '#f6fffa', 'drop', vel=None, alpha=al); m = n // 2; FX.particles(st, P[:m], .05, '#ffffff', 'streak', vel=v[:m] * .035, alpha=al[:m] * .8)

    def bank(self, f, st, t, y):
        """the cloud bank he goes up into: it comes down at us, opens round him, tears"""
        u = (f - 42) / 24.; top = 62.; C = self.c0.copy(); C[:, 0] = (C[:, 0] - 84 * t + 160) % 580 - 160; C[:, 1] = top - 26 + self.cj[:, 1] * 7; d = np.hypot(C[:, 0] - 4, C[:, 2]); push = np.clip(u * 3.2, 0, 1) * np.exp(-d / 42.) * 46
        C[:, 0] += (C[:, 0] - 4) / (d + 4) * push; C[:, 2] += C[:, 2] / (d + 4) * push; K.sprites(st, C, self.cw, var=self.cv, flip=self.cf, rot=self.cj[:, 0] * .25 * np.clip(u * 2, 0, 1) * np.exp(-d / 60), alpha=smooth(35, 39, f), cLit='#fffaf0', cMid='#ffe2b4', cSh='#d8a890', cInk='#8a5a4a', soft=8., near=8.)

    # ------------------------------------------------ f48-59 calm gold
    def gold(self, f, st, t):
        u = (f - 48) / 12.; g = on2(f); burst = 1 - ease_out((f - 48) / 6., 2.); p = V(-4 + 8 * ease_out(u, 2.), 27 - 14 * burst + .5 * math.sin(t * 3), 0)
        cam = Cam(V(24 - 3 * u, 22.5 + 2.0 * u, 46 - 4 * u), V(-3, 25.0, -8), 36, roll=-3 + 2 * u); st.cam = cam; sd = nz(V(-.80, .20, -.80))
        K.sky(st, sunDir=tuple(sd), sunR=.12, sunCol='#ffbe62', sunGlow=.55, rays=.55, halo=.8, cZen='#b85430', cMid='#e88a44', cHor='#ffcf84', cLow='#f2b674', cov=.35, cy0=.01, cy1=.10, cLit='#ffe9bc', cCM='#f6b672', cSh='#c8745a', cInk='#7a3a2c')
        L = K.light(key=tuple(nz(V(.25, .45, .60))), keyCol='#ffd49a', amb='#8a6a9a', rim=tuple(sd), rimCol=(2.6, 1.5, .65), bounceCol=(.45, .26, .12), fog=(0, 0, 0, 0))
        C = self.f0 + V(-13 * t, 0, 0); C[:, 0] = (C[:, 0] + 1500) % 3000 - 1500; R_ = np.hypot(C[:, 0], C[:, 2]); C[:, 1] += 4 - .0040 * R_; hole = np.hypot(C[:, 0] - p[0] + 8, C[:, 2]); C[:, 1] -= 16 * np.exp(-hole / 16.); zg = float((p - cam.eye) @ cam.R[2]); z = (C - cam.eye) @ cam.R[2]; w = self.fw * np.clip(.34 + R_ / 420, .34, 1.)
        cl = lambda m: K.sprites(st, C[m], w[m], var=self.fv[m], flip=self.ff[m], cLit='#ffe9bc', cMid='#f2ab68', cSh='#a8584e', cInk='#5a2622', cRim=(.75, .48, .16), fog=.0008, fogS=170., fogCol='#ffca86', soft=5., near=14., ink=.75)
        cl(z >= zg); AR = HM.H_FLY_L.set(lh=(3.4, 12.2, 7.4), rh=(-5.9, 8.6, .4), lhand='open', rhand='open', lel=(.6, -.5, -.4), rel=(-.3, .9, -.2), cher=(4, -20, 0), hedr=(6, -38, 2), lfing=(.4, .25, .9), rfing=(-.8, -.25, -.4), lpalm=(0, -1, .2), rpalm=(0, -1, .2)); UP = HM.H_FLY_L.set(lh=(1.0, 15.0, 6.6), pelr=(-4, 44, 0), hedr=(8, -56, 0))
        st.open(cam, L, far=20000.); S, TP, gem = K.giant(st, keys(g, [(48, UP), (54, AR, 'io'), (60, AR.set(hedr=(2, -34, 2)))]), at=p - V(0, 8, 0), yaw=84, pitch=-44 * burst - 4, roll=-10 * (1 - u), face=HM.VFace(smile=.6, lid=keys(f, [(50, .9), (54, .35, 'io'), (60, .42)]), spark=.6), tail='fly', tlen=15., vel=(16, 0, 0), wind=(-.8, .05, 0), ring='L', gem=cam.eye, sashlen=5.2, slow=.7); st.close(); cl(z < zg)
        r = np.random.default_rng(5); n = 30; T = (f - 47) / 24.; a = r.uniform(0, 6.283, n); e = 1 - math.exp(-3.4 * T); R = p * [1, 0, 1] + V(-6, 6, 0) + np.c_[np.cos(a) * 20 * r.uniform(.3, 1.2, n), r.uniform(4, 22, n), np.sin(a) * 14 * r.uniform(.3, 1, n)] * e - V(0, 16, 0) * T * T; sz = r.uniform(.8, 2.6, n) * max(0., 1 - .9 * u); K.sprites(st, R, sz * K.CW / K.CH, sz, var=r.integers(0, 8, n), rot=r.uniform(-.8, .8, n) + T * r.uniform(-2, 2, n), alpha=clamp(1.4 - 1.8 * u), puff=True, cLit='#ffe9bc', cMid='#f2b070', cSh='#b8645a', cInk='#6a2e28', cRim=(.8, .5, .18), soft=1., near=6.)
        FX.drift(st, 60, ((-30, 10, -20), (40, 50, 30)), t, kind='ember', size=.22, col='#ffe6b0', fall=-.6, sway=1.2, seed=2, wind=(-9, 0, 0), alpha=.7)
        return st.finish(bloom=.45, thr=.96, vig=.38, flash=.25 * (1 - smooth(48, 51, f)), flashCol='#fff4dc')

    # ------------------------------------------------ f60-65 the shadow
    def shadow(self, f, st, t):
        u = (f - 60) / 5.; cam = Cam(V(-8, 150 - 10 * u, 26), V(0, 0, -4), 46, roll=14 - 3 * u); st.cam = cam; sp = 84.
        st.paint('in vec2 uv;out vec4 o;\nvoid main(){o=vec4(.05,.4,.45,1);}')
        L = self.light(key=tuple(nz(V(.5, .8, .2))), inkRef=2.); st.open(cam, L, far=4000.); k = ease_io(u, 1.6)
        st.mesh(*CL.sheet(lambda a, b: ((a - .5) * 2, -999, b), 2, 2), kind=0); S, TP, _ = K.giant(st, HM.H_FLY_L.set(hedr=(0, -20, 0)), at=(-9 + 9 * u, 30, 4), yaw=90, scale=1.35, face=HM.VFace(), tail='fly', tlen=15., vel=(24, 0, 0), wind=(-1., 0, 0), ring=None)
        K.ocean(st, off=(sp * t, 0), amp=.9, fr=.16, near=420., seaW=.28, sun=nz(V(.4, .8, .2)), glit=.0, shade=(6 - 10 * u, -2, 22 + 44 * k, .25 + .72 * k), cFar='#169aa0', unfog=9.); st.close()
        # his own small shadow, broken gulls of foam
        FX.drift(st, 40, ((-110, 1, -70), (110, 2, 70)), t, kind='dot', size=.35, col='#fff8e6', fall=0, sway=.3, seed=4, wind=(-sp, 0, 0), alpha=.6)
        return st.finish(bloom=.3, thr=.97, vig=.45, satu=1.05)

    # ------------------------------------------------ f66-78 the mouth
    def serp(self, f):
        """(y of the head, gape, hood, pitch)"""
        u = (f - 64.5) / 10.; h, gp, hd = SP.rise(clamp(u)); y = lerp(-95, 78, h); gape = gp if f < 86 else keys(f, [(86, 1.), (89.2, .02, 'in'), (92, .10), (96, .0)]); return y, gape, hd, lerp(16, -5, smooth(66, 74, f))

    def serpent(self, st, f, t, **k):
        y, gp, hd, pt = self.serp(f); y += 1.2 * math.sin(t * 2.4); return SP.draw(st, gp, at=(0, y, 0), yaw=keys(f, [(66, 5.), (74, 0.)]) , pitch=pt, scale=10, hood=hd, wet=.75, face=Face(frown=.7, pupil=.8), **k)

    def pour(self, st, S, t, k=1., n=90, floor=0.):
        """water running off the jaws"""
        r = np.random.default_rng(2)
        for i in range(26):
            x = -5.4 + 10.8 * i / 25 + r.normal(0, .12); zz = 6.4 - .19 * x * x; top = i % 3 != 0; q = (S.up if top else S.low)((x, -1.7 if top else -2.4, zz)); L = max(4., q[1] - floor) * r.uniform(.55, 1.); u = np.linspace(0, 1, 9); w = r.uniform(.8, 2.4) * k
            FX.ribbon(st, q - V(0, 1, 0) * (u * L)[:, None] + np.c_[np.sin(u * 5 + i + t * 4) * 1.2 * u, 0 * u, np.cos(u * 4 + i) * .8 * u], np.linspace(w * .55, w * 1.5, 9), mode='wind', col='#eafff8', amt=.85 * k, seed=i * 1.7)
        m = n * 5; x = r.uniform(-6, 6, m); top = r.uniform(0, 1, m) < .65; base = np.array([(S.up if tt else S.low)((xx, -1.6, 6.3 - .19 * xx * xx)) for xx, tt in zip(x, top)]); T = ((t * r.uniform(.6, 1.1, m) + r.uniform(0, 1, m)) % 1.) * 2.2; P = base + r.normal(0, 1.4, (m, 3)) - V(0, 22, 0) * (T * T)[:, None] - V(0, 3, 0) * T[:, None]; FX.particles(st, P, r.uniform(.35, 1.1, m), '#f2fffa', 'drop', alpha=np.where(P[:, 1] > floor, .9 * k, 0.))

    def mouth(self, f, st, t):
        u = (f - 66) / 12.; g = on2(f); sh = 2.6 * decay((f - 66) / 24., 3.); jx, jy = shake(f, sh, .9, 4); push = ease_io((f - 66) / 9., 1.8)
        cam = Cam(V(10 - 8 * push + jx, lerp(20, 46, push) + jy, lerp(206, 130, push) - 8 * u), V(jx, lerp(34, 76, push) + jy, 0), lerp(52, 66, push), roll=-5 + 4 * push); st.cam = cam
        self.sky(st, sunDir=(-.5, .5, -.6), cZen='#1f7a94', cMid='#6fb4b0', cHor='#ffe6b4', cov=.6, cy1=.4)
        L = self.light(key=tuple(nz(V(-.55, .62, .55))), inkRef=9., keyCol='#fff0d0', amb='#6f8cb0', rim=(.6, .5, -.6), rimCol=(.8, .9, .8), fog=(.0009, 190, .004, 0), fogCol='#bfe0d4', pts=[(V(0, 60, 40), 60., (.10, .20, .18))])
        st.open(cam, L, far=20000.); S = self.serpent(st, f, t); K.ocean(st, off=(0, -30 * t), amp=3.2, fr=.055, near=900., sun=nz(V(-.5, .5, -.6)), glit=.35, churn=(0, 4, 66, 1 - .35 * smooth(70, 78, f)), unfog=2., cFar='#e6dcb4', seaW=1.); st.close()
        pk = [1., .46, .20, .07]; k = sum(f >= q for q in (74, 76, 78)); sc = pk[k] * 1.55; pop = 1 + .55 * (f in (74, 76, 78)); hp = V(0, lerp(40, 66, push) + 1.2 * math.sin(t * 5), lerp(128, 82, push)); st.open(cam, self.light(key=tuple(nz(V(-.55, .62, .55))), inkRef=sc), far=20000.)
        BR = HM.H_LEAP.set(pel=(0, 8, 0), pelr=(0, -8, 0), cher=(0, -10, 0), hedr=(0, -10, 0), lh=(5.6, 12.6, -1.0), rh=(-5.6, 12.6, -1.0), lhand='open', rhand='open', lfing=(.5, .8, 0), rfing=(-.5, .8, 0), lpalm=(0, 0, 1), rpalm=(0, 0, 1), lel=(.5, -.6, -.5), rel=(-.5, -.6, -.5), lf=(1.6, 3.4, -1.6), rf=(-1.4, 2.4, -2.2)); TK = BR.set(lh=(1.2, 9.6, 2.2), rh=(-1.2, 9.6, 2.2), lhand='fist', rhand='fist', cher=(0, 22, 0), hedr=(0, 10, 0), lf=(1.1, 5.4, 1.4), rf=(-1.1, 4.8, .8))
        S2, TP, _ = K.giant(st, keys(g, [(66, HM.H_FLY), (70, BR, 'out'), (73, BR), (75, TK, 'out')]), at=hp - V(0, 8 * sc * pop, 0), yaw=176, pitch=keys(f, [(66, -30.), (70, 8.)]), scale=sc * pop, face=HM.VFace(), tail='whip', tlen=14., ring=None, wind=(0, .4, 1.)); st.close()
        self.pour(st, S, t, smooth(66, 69, f))
        r = np.random.default_rng(7); n = 46; T = (f - 65) / 24.; a = np.pi / 2 + np.tile([-1, 1], n // 2) * r.uniform(.5, 2.6, n); Q = np.c_[np.cos(a) * (58 + 60 * T), 4 + r.uniform(20, 70, n) * T - 46 * T * T, np.sin(a) * (58 + 60 * T)]; K.sprites(st, Q, 9 * self.k46 * K.CW / K.CH, 9 * self.k46, var=r.integers(0, 8, n), rot=r.uniform(-1, 1, n), alpha=np.clip(1.7 - T * 2.2, 0, 1), puff=True, cLit='#ffffff', cMid='#dff6ee', cSh='#8fc4c4', cInk='#2a7a88', cRim=(.2, .2, .15), soft=8., near=20., ink=.6)
        FX.burst(st, 260, (0, 6, 30), (f - 65) / 24., speed=150, grav=120, size=1.1, seed=8, col='#f4fffa', kind='drop', life=1.2, spread=(1, .7, .8), up=.8, drag=1.2)
        for q in (74, 76, 78):
            if 0 <= f - q < 5: v = (f - q) / 5.; x, y, _ = cam.project(hp); rr = (150 - 40 * (q - 74) / 2) * (.3 + v); st.vector(lambda c: (c.set_source_rgba(1, .86, .5, .9 * (1 - v)), c.set_line_width(10 * (1 - v) + 1), c.arc(x, y, rr, 0, 7), c.stroke())); FX.burst(st, 22, hp, v * .2, speed=40, grav=0, size=.5, seed=q, col='#ffd070', life=.22)
        if k: FX.particles(st, hp[None], 5 + 3 * k, '#ffb050', 'glint', alpha=.35 * k)
        return st.finish(bloom=.4, thr=.97, vig=.45, flash=.35 * (f == 66), flashCol='#eafff6', contrast=1.05)

    # ------------------------------------------------ f79-87 from the throat
    def spark_path(self, S, f):
        K_ = [(78, (0, 1.0, 26)), (80, (.6, .6, 8.5)), (81.5, (2.6, -.2, 3.)), (83, (1.2, 1.8, -1.2)), (84.5, (-2.6, 1.0, .6)), (86, (-1.6, -.6, 4.)), (87.3, (.2, -.1, 8.)), (89, (.6, 1.2, 22))]; t = np.array([k for k, _ in K_]); P = np.array([p for _, p in K_]); from lau.cloth import spline
        Q = spline(P, 120); u = np.interp(f, t, np.linspace(0, 119, len(t))); i = int(min(118, u)); q = Q[i] + (Q[i + 1] - Q[i]) * (u - i); return S.w(q)

    def spark(self, st, S, f, size=1., n=16, dt=.22):
        P = np.array([self.spark_path(S, max(78., f - dt * k)) for k in range(n)]); FX.ribbon(st, P, np.linspace(3.6, .2, n) * size, mode='light', col='#ff8a2a', col2='#fff2c0', amt=.95, blend='add'); FX.particles(st, P[:1], 17. * size, '#ff9a3a', 'ember', alpha=.8); FX.particles(st, P[:1], 15. * size, '#ffb050', 'glint', alpha=1.); FX.particles(st, P[:1], 1.3 * size, '#fff6d8', 'dot', alpha=1.); FX.particles(st, P[1:], np.linspace(1.2, .2, n - 1) * size, '#ffc060', 'ember', alpha=np.linspace(.9, .1, n - 1)); return P[0]

    def inside(self, f, st, t):
        u = (f - 79) / 8.; cl = keys(f, [(79, 1.), (84, .98), (88, .52, 'in')]); M = None; y = 78 + 1.2 * math.sin(t * 2.4)
        tmp = SP.SS(SP.model((0, y, 0), 180, -5, 0, 10), cl); jx, jy = shake(f, .25 + 1.2 * smooth(84, 88, f), .8, 2); cam = Cam(tmp.w((.4 * math.sin(f * .4) + jx * .1, -.5 + jy * .1, -6.4 + .5 * u)), tmp.w((jx * .1, -.1, 8)), 68, roll=4 * math.sin(f * .5)); st.cam = cam; sp = self.spark_path(tmp, f)
        self.sky(st, sunDir=(.15, .90, -.35), cZen='#0f4a62', cMid='#1f7484', cHor='#5fb0a4', cLow='#2a8a90', cov=.7, cy1=.34, sunR=0., sunGlow=.15, rays=0., halo=0., cLit='#a8d4c4', cCM='#5fa09c', cSh='#2a6470', cInk='#0c3444')
        L = self.light(key=(-.2, .5, -.85), keyCol=(.55, .42, .36), amb=(.16, .07, .09), inkRef=8., rim=(0, .4, -1), rimCol=(.8, .6, .4), bounceCol=(.05, .02, .02), pts=[(sp, 26., (1.9, .85, .28))], shadow=False)
        st.open(cam, L, far=20000.); S = SP.draw(st, cl, at=(0, y, 0), yaw=180, pitch=-5, scale=10, hood=0., wet=.8, face=Face(), barbels=False); K.ocean(st, off=(0, -40 * t), amp=3., fr=.055, near=900., sun=nz(V(.15, .9, -.35)), glit=0., unfog=2., cFar='#4f9c98', cDeep='#07405a', cMid='#0f7480', cLite='#4fb4a4'); st.close()
        # threads of water and spittle between the teeth catch the light
        for i in range(9): x = -4.5 + i * 1.1; a, b = S.up((x, -1.9, 6.2 - .17 * x * x)), S.low((x + .2, -1.4, 6.2 - .17 * x * x)); q = np.linspace(0, 1, 12)[:, None]; s = np.sin(q * math.pi); FX.ribbon(st, a * (1 - q) + b * q - V(0, 0, 3) * s * math.sin(t * 6 + i), .28, mode='wind', col='#fff4e0', amt=.8, seed=i)
        self.spark(st, S, f, .62); FX.embers(st, 30, (tuple(sp - 4), tuple(sp + 4)), t, rise=6, size=.35, seed=3, life=.8)
        st.paint('in vec2 uv;out vec4 o;uniform float k;\nvoid main(){vec2 p=(uv-.5)*vec2(1.78,1.);float v=smoothstep(.42,1.05,length(p));o=vec4(vec3(.05,.005,.012)*v,v*k);}', 'over', k=.9)
        if f < 81: IM.whip(st, 0, 60 * (81 - f))
        return st.finish(bloom=.6, thr=.9, vig=.5, contrast=1.06)

    # ------------------------------------------------ f88-95 the jaws clap
    def clap(self, f, st, t):
        g = f; y, gp, hd, pt = self.serp(f); gp = keys(f, [(86, .85), (88, .62, 'linear'), (90, .0, 'in'), (91, .07), (93, .0)]); hit = max(0., (f - 90) / 24.); sh = 5. * decay(hit, 7.) * (f >= 90); jx, jy = shake(f, sh, 1., 6); cam = Cam(V(150 + jx, 64 + jy, 168), V(16 + jx, 70 + jy, 22), 46, roll=5 - 6 * smooth(88, 95, f)); st.cam = cam
        self.sky(st, sunDir=(-.6, .24, -.75), sunR=0., halo=0., sunGlow=.3, cZen='#1f6a8a', cMid='#6fa8a8', cHor='#ffdca0', cov=.6, cy1=.4); L = self.light(key=tuple(nz(V(.35, .6, .6))), inkRef=9., rim=(-.6, .4, -.7), rimCol=(1.3, 1., .6), fog=(.0009, 200, .004, 0), fogCol='#cfe0cc')
        st.open(cam, L, far=20000.); S = SP.draw(st, gp, at=(0, 78 - 5 * decay(hit, 5) * (f >= 90), 0), yaw=6, pitch=-5 + 9 * decay(hit, 6) * (f >= 90), scale=10, hood=1., wet=.8, face=Face(frown=.8 if f < 90 else .2, pupil=.8 if f < 90 else 1.5, lid=1.)); K.ocean(st, off=(0, -20 * t), amp=3.2, fr=.055, near=900., sun=nz(V(-.6, .3, -.75)), glit=.35, churn=(0, 4, 66, .8), unfog=2., cFar='#e6dcb4'); st.close(); self.pour(st, S, t, .8)
        # out between the last teeth, past the lens
        a, b = S.w((.1, -.3, 5.)), V(58, 78, 142); e = (f - 87.4) / 4.6; P = [lerp(a, b, ease_out(clamp(e - .035 * k), 1.3)) + V(0, 20 * math.sin(math.pi * clamp(e - .035 * k)), 0) for k in range(22)]
        P = np.array(P); FX.ribbon(st, P, np.linspace(3.6, .2, 22), mode='light', col='#ff8a2a', col2='#fff2c0', amt=1., blend='add'); FX.particles(st, P[:1], 22., '#ffb050', 'glint', alpha=1.); FX.particles(st, P[:1], 12., '#ff9a3a', 'lamp', alpha=1.); FX.particles(st, P[1:], np.linspace(1.6, .3, 21), '#ffc060', 'ember', alpha=np.linspace(.9, .1, 21))
        if f >= 90:
            for k, x in enumerate(np.linspace(-5, 5, 9)): FX.burst(st, 60, S.up((x, -2., 6.3 - .19 * x * x)), hit, speed=120, grav=110, size=1.9, seed=20 + k, col='#f4fffa', kind='drop', life=.8, spread=(1, .5, 1), up=.35, drag=1.5)
            r = np.random.default_rng(3); n = 34; x = r.uniform(-6, 6, n); B = np.array([S.up((v, -2., 6.6 - .19 * v * v)) for v in x]); d = nz(S.d if False else V(.3, .2, 1)); Q = B + np.c_[x * 3.5, r.uniform(-8, 16, n), r.uniform(12, 34, n)] * (1 - math.exp(-5 * hit)) - V(0, 40, 0) * hit * hit; K.sprites(st, Q, (7 + 34 * hit) * self.k46[:n] * K.CW / K.CH, (7 + 34 * hit) * self.k46[:n], var=r.integers(0, 8, n), rot=r.uniform(-1, 1, n), alpha=np.clip(1.5 - hit * 5, 0, 1), puff=True, cLit='#ffffff', cMid='#dff6ee', cSh='#8fc4c4', cInk='#2a7a88', cRim=(.2, .2, .15), soft=6., near=20., ink=.6)
        if f == 90: IM.inkflash(st, dark='#06121a', mid='#0f8a94', light='#fff6dc', lo=.32, hi=.60)
        return st.finish(bloom=.45, thr=.95, vig=.42, flash=.14 * (f == 91) + smooth(94, 96, f) * .35, flashCol='#ffe6b0')

    # ------------------------------------------------ f96-125 low and fast to the glimmer
    def low(self, f, st, t):
        u = (f - 96) / 29.; g = on2(f); d = ease_io(u, 1.5); mix = lambda a, b: tuple(np.array(hexc(a)) * (1 - d) + np.array(hexc(b)) * d); sp = 120.; gl = V(0, 0, -1)
        hp = V(-2.5 + 2.0 * math.sin(u * 3.4), 4.8 + .7 * math.sin(u * 6) - .9 * u, lerp(-4, -15, ease_io(u, 1.4))); cam = Cam(V(lerp(11.5, 8.5, u), 5.6 - .9 * u + .12 * math.sin(f * .6), 13.5), V(lerp(-4.5, -1.5, u), 5.4 + .3 * u, -18), lerp(46, 40, u), roll=keys(f, [(96, 10.), (106, -4.), (116, 3.), (126, 0.)])); st.cam = cam
        st.paint('sky.frag', **SKY(DUSK, cZen=mix('#2a6a90', '#0c1136'), cMid=mix('#c88a6a', '#2c2358'), cHor=mix('#ffd08a', '#8a4a50'), cLow=mix('#d8a070', '#3a2444'), sunDir=(0, .004, -1.), sunR=0., sunGlow=.22, sunCol=mix('#ffdc9a', '#ff9a3a'), rays=0., halo=0., cov=.5, cy0=.02, cy1=.16, cscale=1.6, cdrift=.02, starAmt=.9 * smooth(.35, 1., u), cLit=mix('#ffe8c0', '#b8604a'), cCM=mix('#e0a888', '#5a3458'), cSh=mix('#9a7080', '#221a42'), cInk=mix('#5a3a4a', '#0c0820')))
        L = Light(key=(-.4, .5, .3), keyCol=mix('#ffe6bc', '#5a6aa8'), amb=mix('#7f8cb0', '#28305e'), rim=(0, .25, -1), rimCol=tuple(np.array((1.5, 1.0, .5)) * (1 - d) + np.array((1.7, .85, .30)) * d), bounceCol=mix('#1a5a5a', '#10204a'), envT='#a0a8d0', envM='#ffb060', envB='#1a3a5a', ink=3.2)
        st.open(cam, L, far=30000.); S, TP, _ = K.giant(st, HM.H_FLY_L.set(hedr=(4, -50, 0), pelr=(-8, 74, 0), lh=(1.7, 11.4, 9.0)), at=hp - V(0, 8, 0), yaw=176 + 7 * math.sin(u * 3), roll=12 * math.sin(u * 5.), pitch=2, face=HM.VFace(), tail='fly', tlen=16., vel=(0, 6, -34), wind=(.1, .02, 1.), ring=None, sashlen=5.5)
        K.ocean(st, off=(0, -sp * t), amp=.6, fr=.30, spd=1.1, near=340., sun=gl, glit=.35 + .55 * d, unfog=lerp(1.2, 2.4, d), wake=(hp[0], hp[2] - 2, 20., .75), wakeDir=(0, -1), cDeep=mix('#0a5d78', '#0a1230'), cMid=mix('#169aa0', '#1a2c5c'), cLite=mix('#6fdcc4', '#4a5c94'), cFoam=mix('#fff8e6', '#c8b8c8'), cFar=mix('#e8b87a', '#6a3a48'), cSun=mix('#ffc878', '#ff8a30')); st.close()
        x, y, z = cam.project(cam.eye + V(0, -.0, -1) * 9000 - V(0, cam.eye[1], 0)); k = smooth(100, 112, f)
        st.paint('''
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform vec2 res,c;uniform float k,fT,sc;uniform sampler2D tZ;
void main(){vec2 p=(vec2(uv.x*res.x,(1.-uv.y)*res.y)-c)/res.y;float z=texelFetch(tZ,ivec2(gl_FragCoord.xy),0).x;float open=step(400.,z);vec2 q=p/sc;float r=length(q*vec2(1.,1.2));vec3 a=hex(0xff9a34)*(exp(-dot(q*vec2(5.,13.),q*vec2(5.,13.)))*.34+exp(-r*11.)*.22)+hex(0xffc060)*exp(-dot(q*vec2(9.,60.),q*vec2(9.,60.)))*.7;
 // a far city: three peaks of points of light
 float h=0.;h=max(h,.046-abs(q.x)*.75);h=max(h,.030-abs(q.x+.038)*.8);h=max(h,.026-abs(q.x-.040)*.8);h=max(h,.010*step(abs(q.x),.075));float y=-q.y;float body=smoothstep(.0012,-.0012,y-h)*step(-.001,y);a=mix(a,hex(0xf08a1c)*(.75+12.*max(y,0.)),body);vec2 g=q*620.;vec2 id=floor(g);float tw=step(.60,h21(id))*(.6+.4*sin(fT*8.+h21(id+3.)*40.));a+=hex(0xfff0c0)*body*tw*2.2*smoothstep(.5,.1,length(fract(g)-.5));
 float ray=pow(max(0.,cos(atan(q.y,q.x)*8.)),30.)*exp(-r*16.);a+=hex(0xffc060)*ray*.22;o=vec4(a*k*open,0.);}
''', 'over', c=(float(x), float(y)), k=float(k * (.85 + .15 * math.sin(t * 5))), sc=float(lerp(.9, 1.7, u)))
        r = np.random.default_rng(9); m = 90; P = np.c_[r.uniform(-16, 16, m), r.uniform(.3, 10, m), (r.uniform(0, 60, m) + sp * t * r.uniform(.8, 1.2, m)) % 60 - 40]; FX.particles(st, P, .03, '#fff4e0', 'streak', vel=np.tile(V(0, 0, 3.2), (m, 1)), alpha=.4); self.spray_back(st, hp, t)
        IM.zoomblur(st, (float(x), float(y)), .05 * (1 - smooth(96, 104, f)))
        return st.finish(bloom=.5, thr=.9, vig=.42, flash=.5 * (1 - smooth(96, 99, f)), flashCol='#ffe6b0', contrast=1.05)

    def spray_back(self, st, hp, t, n=160):
        r = np.random.default_rng(4); ph = r.uniform(0, 1, n); lf = (t * 2.0 + ph) % 1.; T = lf * .6; sg = r.choice([-1, 1], n); P = np.c_[hp[0] + sg * (.6 + r.uniform(1, 7, n) * T), .3 + r.uniform(2, 7, n) * T - 11 * T * T, hp[2] + 4 + r.uniform(16, 44, n) * T]; FX.particles(st, P, r.uniform(.04, .12, n), '#f4f0ea', 'drop', alpha=np.clip((1 - lf) * 2, 0, 1) * .8 * (P[:, 1] > .1))
