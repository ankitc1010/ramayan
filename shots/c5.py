"""c5 (60): Ravana unfolds.  The mendicant's cloth blows off like smoke and the king stands up out of it in three accents (f0, f6, f12).  f24 he takes the very ground she stands on; it rises with the hut and with her, behind the dark flower chariot."""
from .c_kit import *
from chars import people as PE, sita as SI, ravana as RV, vehicles as VH, birds as BD

BLOODSKY = dict(cZen='#16061a', cMid='#6a0e1c', cHor='#e0481c', cLow='#7a1a18', cLit='#ff7a3a', cCM='#8a1c26', cSh='#3a0a1c', cInk='#0c0408', rays=.35, halo=0., sunGlow=.7, cov=.75, cy0=.05, cy1=.55, sunDir=(.0, .10, 1.), sunR=.0, sunCol='#ff9a50', cdrift=.05)
BLOODL = dict(key=(-.5, .45, .55), keyCol='#c85038', amb='#4a1c38', rim=(.3, .5, -.85), rimCol=(1.5, .42, .12), bounceCol=(.20, .05, .03), envT='#8a2030', envM='#ff7a3a', envB='#2a0a1c', fogCol='#7a1c1c', fog=(.0022, 60., .004, 0.), inkRef=1.3, inkCol='#080206')


class Shot(ShotBase):
    id = 'c5'; n = 60
    EVENTS = [(0, 'cloth tears away', dict(dur=10)), (0, 'first accent', {}), (6, 'second accent, arms', {}), (12, 'third accent, ten heads', {}), (14, 'crowns and gold settle', dict(dur=6)), (18, 'he breathes', dict(dur=5)), (24, 'the earth cracks', {}), (26, 'stones and roots tear', dict(dur=14)), (30, 'the ground comes loose', {}), (34, 'flying chariot passes over', dict(dur=14)), (38, 'wind', dict(dur=22)), (47, 'birds scatter', dict(dur=10)), (50, 'the sky swallows them', dict(dur=10))]

    def frame(self, f, st):
        st.clear('#000', f=f); t = st.t
        return self.unfold(f, st, t) if f < 24 else self.tear(f, st, t) if f < 38 else self.her(f, st, t) if f < 47 else self.away(f, st, t)

    def unfold(self, f, st, t):
        g = on2(f); acc = [keys(f, [(a - 1, 0.), (a + 2, 1.10, 'out'), (a + 5, 1.)]) for a in (1, 6, 12)]; tot = sum(acc) / 3; hit = sum(impulse((f - a) / 24., 12) for a in (1, 6, 12) if f >= a)
        dx, dy = shake(f, .35 * hit, 1.1, 2); cam = Cam(V(1.5 + dx, 2.4 + dy, 25.5 - 4.2 * smooth(0, 23, f)), V(.2, 8.5 + 7.2 * (.15 * acc[0] + .35 * acc[1] + .5 * acc[2]), 0), 58, roll=-4 + 3 * tot); st.cam = cam
        st.paint('sky.frag', **SKY(None, **{**BLOODSKY, 'sunDir': (.0, .22, -1.), 'cov': .8}))
        st.paint(HALO, 'over', c=tuple(cam.project(V(0, 15, -3))[:2].astype(float)), k=float(.35 * tot + .25 * hit))
        self.column(st, f, False)
        sc = .88 + .14 * acc[0] + .16 * acc[1] + .24 * acc[2]; fan = .05 * acc[0] + .45 * acc[1] + .52 * acc[2]; arms = .12 * acc[0] + .50 * acc[1] + .38 * acc[2]
        L = Light(**{**BLOODL, 'pts': [(V(0, 1.5, 11), 8., tuple(np.array([1.3, .34, .10]) * (.10 + .7 * hit))), (V(3, 14 + 8 * tot, 13), 11., (1.1 * tot, .42 * tot, .16 * tot)), (V(-9, 12, 6), 10., (.55, .12, .08))], 'shadow': True})
        st.open(cam, L)
        place.draw(st, TORN, u=tornu(gA='#4a2838', gB='#1c1228'), defs='#define NOHUT\n#define NOROCK\n#define NOISLE', sun=0.)
        FL.scatter(st, 'pahari_round', [(x, 0, -95 + 12 * math.sin(x)) for x in np.arange(-150, 151, 22.)], 36, season='summer', seed=3, tint=(.08, .05, .12), hazeCol='#5a1424', haze=.12, wind=.6); FL.scatter(st, 'shrub', [(x, 0, -50) for x in np.arange(-90, 91, 17.)], 10, season='summer', seed=4, tint=(.06, .04, .10), hazeCol='#5a1424', haze=.03, wind=.6)
        pose = keys(g, [(0, RV.R_STAND.set(cher=(0, 30, 0), hedr=(0, 30, 0), lh=(-1.2, 11.2, 3.0), rh=(1.2, 10.6, 3.2))), (5, RV.R_STAND.set(cher=(0, 22, 0), hedr=(0, 20, 0), lh=(-.6, 11.2, 3.0), rh=(.6, 10.6, 3.2))), (8, RV.R_STAND.set(cher=(0, 4, 0), hedr=(0, 12, 0)), 'back'), (12, RV.R_STAND.set(cher=(0, -2, 0), hedr=(0, 8, 0)), 'back'), (17, RV.R_STAND.set(cher=(0, -6, 0), hedr=(0, 10, 0)))])
        if f >= 2:
            S = RV.fig(st, pose, scale=sc, yaw=0, fan=fan, arms=arms, mantle=smooth(2, 10, f), eyeglow=.95 * smooth(6, 10, f), lids=np.array([1. if f >= 13 + abs(k - 4) else .3 for k in range(10)]) if f >= 12 else 1., face=Face(frown=.55, smile=-.15 + .1 * smooth(16, 20, f), lid=.9))
            RV.cape(st, S, t * 1.6, wind=(.10 + .5 * hit, .05 + .25 * hit, -.45), length=10.2 * smooth(2, 8, f) + .1)
        else: S = st.fig(PE.MENDICANT, PE.P_STAFF.set(hedr=(0, 8, 0)), face=Face(lid=1., frown=.6), yaw=0)
        # the cloth goes off him in rags
        r = np.random.default_rng(5); k = (f - 1) / 24.
        if 0 <= f < 15:
            for i in range(9):
                a = r.uniform(-1, 1); y = r.uniform(4, 13); dirn = nz(V(a * 1.3, r.uniform(.1, .9), r.uniform(.1, .7))); sp = r.uniform(16, 30); root = V(a * 1.8, y, 1.2)
                tr = lambda tt: root + dirn * sp * max(0., tt) * (1 - .35 * max(0., tt)) + V(0, 1.2 * math.sin(6 * tt + i), 0)
                if f >= 1:
                    P = CL.lag(tr, k, n=12, length=3. + 4 * r.uniform(), delay=.022, wind=tuple(-dirn * .5), grav=.1, wave=1.2, freq=1.6, phase=i); w = 1.6 * (1 - smooth(7, 15, f)) * r.uniform(.6, 1.2)
                    st.mesh(*CL.strip(P, [w * .5, w, w * .3], up=(.3, 1, .2), m=5, curl=.2, twist=2., n=26), kind=0, col=('#c8742a', '#5a2416', '#f0b050'), cls=1, ink=.85)
        st.close()
        self.column(st, f, True)
        for j, a in enumerate((1, 6, 12)):
            q = (f - a) / 24.
            if 0 <= q < .9:
                FX.burst(st, 60, (0, .6, 2), q, speed=30, grav=9, size=.17, seed=17 + j, col='#ffae50', kind='streak', life=.6, spread=(1.3, .6, .7), up=.6, drag=2.); FX.burst(st, 44, (0, .4, 1), q, speed=26, grav=0, size=1.7, seed=27 + j, col='#5a2420', kind='smoke', life=.6, spread=(1.6, .10, .8), up=.04, drag=3.2)
                if j: FX.burst(st, 90, (0, 11 + 2 * j, 3), q, speed=34, grav=3, size=.15, seed=47 + j, col='#ffc060', kind='flake', life=.7, spread=(1.3, .9, .5), drag=2.6)
        FX.embers(st, 90, ((-26, 0, -10), (26, 4, 14)), t, rise=6., size=.11, seed=4, life=2.6, swirl=2., wind=(2, 0, 0), col='#ff7a30')
        if f in (12, 13): IM.zoomblur(st, (960, 520), .05)
        if f == 12: IM.speedlines(st, (960, 470), .8, col=(.02, .0, .01), seed=5, inner=.46, dens=6); IM.inkflash(st, '#10030a', '#d8261c', '#ffdf9c', lo=.34, hi=.60); return st.finish(bloom=.2, vig=.3)          # ten heads, as a print
        return st.finish(bloom=.55, thr=.85, vig=.5, contrast=1.10, satu=1.1, flash=.16 * (f == 1) + .05 * (f == 6) + .07 * (f == 12), flashCol='#ff5a28')

    def column(self, st, f, front):
        """fire and torn smoke going up round him, f1-13; the half behind him is painted before he is"""
        if not 1 <= f < 14: return
        q = (f - 1) / 24.; r = np.random.default_rng(31); n = 190; h0, a0, sp = r.uniform(0, 1, n), r.uniform(0, 6.283, n), r.uniform(.6, 1.4, n); go = smooth(-1.5, 2.5, f - .5)
        H = 21. * np.clip(h0 * .75 * go + q * 1.3 * sp, 0, 1.2); R = (1.0 + 4.2 * go * (.45 + .55 * H / 21.) + 5. * q) * r.uniform(.6, 1.25, n); A = a0 + 11. * q * sp + H * .18; P = np.c_[np.cos(A) * R, H, np.sin(A) * R * .7 + .8]; al = np.clip(1.5 - q / .30, 0, 1) * np.clip(H / 1.2, 0, 1) * np.clip((25 - H) / 6, 0, 1); m = (P[:, 2] > .8) == front
        c = np.where(r.uniform(0, 1, (n, 1)) > .5, np.array(hexc('#3c1024')), np.array(hexc('#7a2616'))); FX.particles(st, P[m], (r.uniform(.45, 1.25, n) * (1 + 1.6 * q))[m], c[m], 'smoke', seed=r.uniform(0, 1, n)[m], alpha=(.85 * al)[m], rot=A[m])
        for i in range(9):
            u = np.linspace(0, 1, 64); an = i * .698 + 13. * q + u * (4.4 + .9 * (i % 3)); rad = (1.0 + 3.6 * go) * (.55 + .62 * u) * (1 + .10 * math.sin(7 * q + i)); C = np.c_[np.cos(an) * rad, (17.5 + 2.5 * (i % 3)) * u ** 1.1 * go, np.sin(an) * rad * .7 + .8]; w = np.interp(u, [0, .2, .75, 1], [.25, .62, .46, .03]) * (1.2 - .9 * smooth(6, 14, f)); k = (C[:, 2] > .8) == front
            for run in np.split(np.arange(64), np.nonzero(np.diff(k.astype(int)))[0] + 1):
                if k[run[0]] and len(run) > 3: FX.ribbon(st, C[run], w[run], 'fire', (1., .72, .45), seed=i * 3.1 + run[0] * .07, amt=1 - smooth(7, 13.5, f))

    def lift(self, f):
        """the piece of earth: translation, rotation, how far it is cut, how deep the wound"""
        up = keys(f, [(29, 0.), (31, 3.5, 'out'), (33, 5.), (38, 19., 'in')]); tl = keys(f, [(29, 0.), (31, 9., 'back'), (34, 6.), (38, -5.)]); w = impulse((f - 30) / 24., 8)
        return V(0, up, 0), eul(0, .4 * tl + 1.2 * math.sin(f * 1.7) * w, tl), keys(f, [(24, 0.), (26, .35, 'out'), (30, .8), (38, 1.2)]), keys(f, [(24, 0.), (26, 3., 'out'), (30, 9.), (34, 15.)])

    def tear(self, f, st, t):
        g = on2(f); T, R, gap, dep = self.lift(f); hit = impulse((f - 24) / 24., 9) + .8 * impulse((f - 30) / 24., 7); u = (f - 24) / 13.; dx, dy = shake(f, 1.1 * hit + .15, 1.2, 3)
        cam = Cam(V(-13 + 3 * u + dx, 7.5 + dy, 88 - 4 * u), V(1.5, 31 + 2.5 * u, 0), 52, roll=3 - 3 * u); st.cam = cam
        st.paint('sky.frag', **SKY(None, **{**BLOODSKY, 'sunDir': (.25, .22, -1.)})); st.paint(HALO, 'over', c=tuple(cam.project(V(0, 52, -30))[:2].astype(float)), k=.40 + .2 * hit)
        L = Light(**{**BLOODL, 'pts': [(V(0, 1, 30), 14., tuple(np.array([1.6, .42, .10]) * (.1 + .9 * hit))), (V(0, 52, 4), 22., (1.0, .34, .12))], 'inkRef': 1.6, 'amb': '#30204e', 'keyCol': '#a84038', 'fogCol': '#4a1428'})
        st.open(cam, L)
        place.draw(st, TORN, u=tornu(T, R, gap, dep, gA='#6a3c44', gB='#221630', rockA='#5a2434', rockB='#1c1030', rockH=46., leafA='#a87838', leafB='#4a3020', red=.06 + .12 * hit), sun=0.)
        trees(st, far=False, near=False, right=False, tint=(.15, .10, .20), mist='#4a1428')
        pose = keys(g, [(24, RV.R_STAND.set(lh=(6.2, 15.5, 1.), rh=(-6.2, 15.5, 1.), lhand='claw', rhand='claw', cher=(0, -10, 0))), (25, RV.R_LOOM, 'in'), (29, RV.R_LOOM.set(cher=(0, 30, 0), pel=(0, 7.7, -.4))), (32, RV.R_LOOM.set(cher=(0, 14, 0), pel=(0, 8.3, -.8), lh=(6.6, 14.4, 2.2), rh=(-6.6, 14.4, 2.2)), 'out'), (37, RV.R_LOOM.set(cher=(0, 8, 0), pel=(0, 8.4, -1.), lh=(6.9, 15.6, 1.6), rh=(-6.9, 15.6, 1.6)))])
        S = RV.fig(st, pose, at=(2, 4., -30), scale=3.9, fan=1., arms=1., eyeglow=1., spread=1.1, face=Face(frown=.6, smile=-.1), mouths=.25 * smooth(28, 32, f) * np.ones(10)); RV.cape(st, S, t * 1.5, wind=(.2, .1, -.2))
        if f >= 33: k = (f - 33) / 4.; VH.pushpaka(st, at=(64 - 54 * ease_out(k, 1.5), 80 - 11 * k, 22), yaw=-62, pitch=-6, roll=10 - 8 * k, scale=3.6, mood=1., lamps=1.5)
        roots(st, T, R, t, 22)
        stones(st, (f - 24) / 24., (0, 0, 4), 60, up=30., grav=34., size=1.3, seed=3); stones(st, (f - 30) / 24., (0, 0, 4), 80, up=36., grav=30., size=1.8, seed=9)
        p = isle((4.0, 1.1, 15.0), T, R); SI_ = self.kneel(st, M=self.on(T, R, (2.2, 1.1, 13.5), 0.), wind=.4)
        st.close()
        ring = np.array([line_point(a, 24.) for a in np.linspace(0, 1, 90)]); q = (f - 24) / 24.; r = np.random.default_rng(2)
        if f >= 24:
            h = 16 * (1 - math.exp(-4. * q)) * r.uniform(.25, 1., 90); al = np.clip(1.1 - q * 2.4, 0, 1)
            for k in (.35, .7, 1.): FX.particles(st, ring + np.c_[0 * h, h * k, 0 * h], (1.4 + 2.2 * q) * r.uniform(.6, 1.2, 90), '#7a4030', 'smoke', seed=r.uniform(0, 1, 90), alpha=.85 * al)
            FX.particles(st, ring + np.c_[0 * h, h * .5, 0 * h], .5, '#ffb050', 'ember', alpha=al * .8)
        if f >= 30:
            q = (f - 30) / 24.; FX.burst(st, 70, (0, 0, 27), q, speed=40, grav=14, size=1.9, seed=6, col='#6a3428', kind='smoke', life=.45, spread=(1.5, .35, .4), up=.35, drag=2.5); FX.burst(st, 90, (0, 1, 20), q, speed=40, grav=20, size=.4, seed=7, col='#ffae60', kind='streak', life=.7, spread=(1.3, .7, .6), up=.6)
            P = np.array([isle((x, -3., z), T, R) for x, z in r.uniform(-20, 20, (70, 2))]); fall = np.mod(r.uniform(0, 1, 70) + q * 2., 1.); P[:, 1] -= fall * 13; FX.particles(st, P, .6 * r.uniform(.4, 1.3, 70), '#5a3020', 'ash', seed=r.uniform(0, 1, 70), alpha=.9 * (1 - fall))
        FX.embers(st, 70, ((-60, 0, -20), (60, 8, 40)), t, rise=9., size=.18, seed=4, life=2.6, swirl=3., wind=(3, 0, 0), col='#ff7a30')
        if f == 24: IM.zoomblur(st, (960, 760), .03)
        return st.finish(bloom=.5, thr=.85, vig=.5, contrast=1.10, satu=1.1, flash=.05 * (f == 24) + .03 * (f == 30), flashCol='#ff6a30')

    def on(self, T, R, p, yaw):
        M = np.eye(4); M[:3, :3] = R @ eul(yaw, 0, 0); M[:3, 3] = isle(p, T, R); return M

    def kneel(self, st, M, wind=1., draw=True, face=None):
        P = SI.S_SIT.set(pelr=(0, 4, 2), cher=(8, 2, -3), hedr=(4, 13, 4), lh=(2.15, 5.2, -1.2), lel=(.8, -.8, -.1), lhand='grip', lfing=(.95, .25, -.2), lpalm=(.25, 0, -.95), rh=(-.5, 3.4, 1.7), rhand='flat', rfing=(.85, .45, .25), rpalm=(0, -.1, -1), rel=(-1, -.8, -.1))
        return st.fig(SI.FOREST, P, M=M, face=face or Face(lid=0., smile=.02, sad=.22), u=dict(Wind=(-.5 * wind, .0, -.4 * wind)), draw=draw)

    def her(self, f, st, t):
        """on the rising earth: she has closed her eyes"""
        u = (f - 38) / 8.; T = V(0, 14 + 30 * u + 14 * u * u, 0); R = eul(-3 + 5 * u, 2 - 4 * u, -5 + 3 * u); dx, dy = shake(f, .10, .9, 5); S0 = None
        M = self.on(T, R, (2.2, 1.1, 13.5), -25.); S = self.kneel(st, M, draw=False); h = S.head((0, 0, 0)); Re = R
        cam = Cam(isle((-12 + dx, 4.2 + dy, 35 - 2. * u), T, R), isle((4.6, 5.8, 13.), T, R), 26, roll=-4 + 3 * u, up=tuple(R @ V(0, 1, 0))); st.cam = cam
        st.paint('sky.frag', **SKY(None, **{**BLOODSKY, 'sunDir': (.4, .16, -1.), 'cy0': .10 - .30 * u, 'cy1': .6 - .2 * u})); fk = .9 + .1 * noise1(t * 6, 2)
        L = Light(**{**BLOODL, 'key': (-.55, .35, .65), 'keyCol': '#f0845a', 'amb': '#5c2c48', 'pts': [], 'rimCol': (1.6, .55, .2), 'inkRef': 1.})
        st.open(cam, L)
        place.draw(st, TORN, u=tornu(T, R, 1.2, 15., gA='#a06444', gB='#50282e', rockA='#7a3830', rockB='#341626', rockH=96., leafA='#c08a44', leafB='#5a3824', red=.12), defs='#define NOROCK', sun=0.)
        self.kneel(st, M, wind=1.1 + .4 * math.sin(t * 7))
        st.close()
        r = np.random.default_rng(6); n = 130; lo, hi = np.array([-22., -8, -6]), np.array([24., 26, 24]); P = r.uniform(0, 1, (n, 3)) * (hi - lo); v = V(2, -38, 0); P = lo + np.mod(P + v * t * r.uniform(.7, 1.3, (n, 1)), hi - lo); P = np.array([isle(q, T, R) for q in P])
        FX.particles(st, P[:70], .10 * r.uniform(.5, 2.4, 70), '#4a2418', 'ash', seed=r.uniform(0, 1, 70), alpha=.95); FX.particles(st, P[70:], .04, '#ffb070', 'streak', vel=np.tile(-v * .035, (60, 1)), alpha=.5)
        FX.drift(st, 20, (tuple(h + V(3, -8, -6)), tuple(h + V(16, 9, 7))), t * 2, 'leaf', .30, '#a86a2c', 9., 1.5, col2='#5a2a1c', wind=(-4, 0, 0), seed=3)
        IM.dof(st, float((h - cam.eye) @ cam.R[2]), 9., 6.)
        return st.finish(bloom=.5, thr=.9, vig=.55, contrast=1.08, satu=1.05)

    def away(self, f, st, t):
        """the forest falls away, a round raw wound in it; the dark chariot draws the torn earth into the red"""
        u = (f - 47) / 12.; e = ease_in(u, 1.5); T = V(4 + 84 * e, 46 + 120 * e, -8 - 260 * e); R = eul(-20 + 30 * u, 6 - 10 * u, -9 + 4 * u); vel = nz(V(74, 108, -250))
        cam = Cam(V(-30 - 10 * u, 150 + 34 * u, 170 + 10 * u), lerp(V(6, 50, -10), T + V(4, 34, 0), ease_io(u, 1.6)), 50 - 14 * ease_io(u), roll=9 - 9 * u); st.cam = cam
        st.paint('sky.frag', **SKY(None, **{**BLOODSKY, 'sunDir': (.40, .10, -1.), 'sunR': .055, 'sunCol': '#ffd08a', 'cov': .6, 'sunGlow': 1.}))
        L = Light(**{**BLOODL, 'key': (.4, .35, -.75), 'keyCol': '#e06038', 'amb': '#4a2040', 'rim': (.4, .3, -.9), 'rimCol': (1.6, .6, .2), 'inkRef': 4., 'fogCol': '#8a2a24', 'fog': (.0013, 200., .002, 0.)})
        st.open(cam, L, far=6000.)
        place.draw(st, TORN, u=tornu(T, R, 1.2, 15., gA='#8a5448', gB='#30202e', leafA='#4a4250', leafB='#12142c', red=.05), defs='#define CANOPY\n#define NOROCK\n#define NOISLE', sun=0.)
        st.world(*self.isle_src(), u=dict(uAmb=hexc(L.amb), uKey=hexc(L.keyCol), sunSh=0., **{k: (hexc(v) if isinstance(v, str) else v) for k, v in tornu(T, R, 1.2, 15., gA='#a06848', gB='#50282e', leafA='#a87838', leafB='#4a3020', red=.10).items()}), head='place_head.glsl', main='place_main.glsl')
        roots(st, T, R, t, 22, vel=vel * 16)
        self.kneel(st, self.on(T, R, (2.2, 1.1, 13.5), 0.), wind=1.)
        pt = T + V(0, 54, -14) + vel * 10; P = VH.pushpaka(st, at=pt, yaw=163 - 12 * u, pitch=-12 + 4 * u, roll=-10 + 16 * u, scale=4.2, mood=1., lamps=1.4)
        Md = P.deck.copy(); Md[:3, :3] *= 1.7; RV.fig(st, RV.R_STAND, M=Md, fan=1., arms=1., eyeglow=1., face=Face(frown=.5))
        r = np.random.default_rng(3); n = 46; b0 = np.c_[r.uniform(-70, 70, n), r.uniform(34, 62, n), r.uniform(-70, 60, n)]; out_ = b0 * V(1, 0, 1); out_ /= np.linalg.norm(out_, axis=1, keepdims=True); v = out_ * r.uniform(40, 75, (n, 1)) + V(0, 22, 0); BD.flock(st, 'crow', b0 + v * (.1 + t - 47 / 24.), v, t, size=2.2, rate=3.2, seed=4)
        st.close()
        for k, (x, z) in enumerate(((-19, 14), (19, 14), (-17, -12), (17, -12))):        # cords of red fire, chariot to earth
            A, B = P.w((.22 * x, -1.6, .25 * z)), isle((x, 12 if z < 0 else 1, z), T, R); q = np.linspace(0, 1, 26)[:, None]; C = A * (1 - q) + B * q + V(0, -1, 0) * 14 * q * (1 - q) + np.c_[.8 * np.sin(q[:, 0] * 9 + t * 12 + k), 0 * q[:, 0], 0 * q[:, 0]] * q * (1 - q) * 4
            FX.ribbon(st, C, .55, 'light', '#ff3a1a', '#ffc070', amt=.9); FX.ribbon(st, C, 1.3, 'fire', (1., .5, .35), seed=k * 3., amt=.5)
        w = r.uniform(0, 1, (60, 3)); Q = np.array([isle((a * 40 - 20, -6, c * 40 - 16), T, R) for a, b, c in w]); lf = np.mod(w[:, 1] + t * .9, 1.); FX.particles(st, Q + np.c_[0 * lf, -60 * lf ** 1.4, 0 * lf], 1.1 * (1 - .5 * lf), '#4a2418', 'ash', alpha=.9 * (1 - lf))
        FX.burst(st, 70, (0, 2, 4), (f - 40) / 24., speed=40, grav=-2, size=9, seed=8, col='#6a3428', kind='smoke', life=1.3, spread=(1., .35, 1.), up=.25, drag=2.6)
        return st.finish(bloom=.55, thr=.85, vig=.45, contrast=1.08, satu=1.08)

    def isle_src(self): return (TORN.replace('vec2 q=p.xz-IC.xz;float r=length(q),a=atan(q.x,q.y);float hole', 'return island(p);vec2 q=p.xz-IC.xz;float r=length(q),a=atan(q.x,q.y);float hole'),)


HALO = '''
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform vec2 res,c;uniform float k,fT;
void main(){vec2 p=(vec2(uv.x*res.x,(1.-uv.y)*res.y)-c)/res.y;float r=length(p),a=atan(p.y,p.x);float ry=smoothstep(-.1,.3,sin(a*20.+fT*.6))*.6+smoothstep(.2,.6,sin(a*9.-fT*.4))*.5;vec3 q=hex(0xff5a20)*(exp(-r*r*5.)*.9+ry*exp(-r*2.2)*.5);o=vec4(q*k,0.);}
'''
