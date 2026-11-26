"""c6 (96): out of the low sun the old vulture king falls on them (f0-24).  Three exchanges on the beat: beak on the dark dome (f30), the wing that throws Ravana back (f42), talon on sword (f54).  f60 the blade passes.
f72 from the floating earth Sita lets her ornaments go, a spark in a scrap of yellow cloth; on a dark hill five small figures look up (f84-96)."""
from .c_kit import *
from chars import sita as SI, ravana as RV, vehicles as VH, jatayu as JT, birds as BD, vanara as VA, hanuman as HM
from chars.armonly import ARM, SKIN, place_hand

JT.SCALY = JT.SCALY.replace('uniform vec2 rep;', 'uniform vec4 rep;')                    # st.mesh pads rep to four numbers

RED = dict(cZen='#2a0a20', cMid='#8a1420', cHor='#f2642a', cLow='#a82a1c', cLit='#ffb060', cCM='#c83a24', cSh='#5a1024', cInk='#1a0610', rays=.5, halo=0., sunGlow=1., cov=.7, cy0=.02, cy1=.45, sunDir=(.0, .12, -1.), sunR=.085, sunCol='#ffd890', cdrift=.06)
SUNL = dict(key=(-.45, .35, .75), keyCol='#d8704a', amb='#5a2a4c', rim=(.15, .35, -.95), rimCol=(2.0, .95, .34), bounceCol=(.22, .07, .03), envT='#a83a3a', envM='#ff9a50', envB='#3a1028', fogCol='#b8401c', fog=(.0012, 120., .0, 0.), inkRef=1.6, inkCol='#0a0308', shadow=False)


def clouds(st, t, n=9, seed=3, y=(0, 70), z=-40, v=-260, L=90, w=4., col='#ff9a50', col2='#7a1a24', amt=.5, span=260):
    """torn strips of cloud flying through the fight"""
    r = np.random.default_rng(seed)
    for i in range(n):
        x = np.mod(r.uniform(0, span) + v * t * r.uniform(.8, 1.25), span + L) - (span + L) / 2; yy = r.uniform(*y); k = np.linspace(0, 1, 24); ph = r.uniform(0, 6); P = np.c_[x + (k - .5) * L * r.uniform(.6, 1.3), yy + 2.2 * np.sin(k * 5 + ph + t * 3), np.full(24, z + r.uniform(-12, 12))]
        FX.ribbon(st, P, np.interp(k, [0, .3, .7, 1], [.1, 1., .7, .05]) * w * r.uniform(.5, 1.3), 'smoke', col, col2, seed=i * 2.7, amt=amt)


PLUME = JT.FEATHER.replace('w+=.03*sin(', 'w=mix(.07,(sd>0.?1.:.62),smoothstep(.10,.36,u))*sqrt(max(0.,1.-pow(max(0.,(u-.50)/.50),2.4)));w+=.03*sin(', 1)      # a whole feather: bare quill, uneven vane, round tip


def plume(st, m, pal):
    a, b, t, e = pal[1:5]; st.mesh(*m, col=(a, b, t), ink=.8, frag=PLUME, u=dict(shape=2, cE=hexc('#ffd88a'), tipAt=.6, gild=1., bars=.35, ragged=.7, asp=8., burnF=0.))


class Shot(ShotBase):
    id = 'c6'; n = 96
    EVENTS = [(0, 'wind', dict(dur=24)), (4, 'far cry of an old bird', {}), (12, 'stoop, rising rush', dict(dur=8)), (20, 'wings open like sails', {}), (30, 'beak on the dome', {}), (36, 'wing beat', {}), (42, 'wing buffet', {}), (44, 'Ravana slides back', dict(dur=3)), (48, 'wing beat', {}), (54, 'talon on sword', {}), (60, 'the blade passes', {}), (61, 'held breath', dict(dur=10)), (66, 'feathers', dict(dur=6)), (72, 'ornaments let go', {}), (74, 'small bells falling away', dict(dur=10)), (86, 'five heads turn up', {}), (92, 'jewels on rock', dict(soft=1))]

    def frame(self, f, st):
        st.clear('#000', f=f); t = st.t
        for a, fn in ((24, self.stoop), (36, self.beak), (48, self.buffet), (60, self.talon), (72, self.fall), (84, self.letgo), (96, self.hill)):
            if f < a: return fn(f, st, t)

    def stoop(self, f, st, t):
        u = f / 23.; d = keys(f, [(0, 1500.), (15, 230., 'out'), (20, 60., 'linear'), (23, 12.)]); g = f if f > 12 else on2(f)
        dx, dy = shake(f, .25 * smooth(12, 22, f), 1., 2); cam = Cam(V(1.5 + dx, 17.5 + dy, 27), V(0, 23.0, -20), 42, roll=-5 + 7 * smooth(8, 23, f)); st.cam = cam
        st.paint('sky.frag', **SKY(None, **{**RED, 'sunDir': (.02, .17, -1.), 'sunR': .15, 'cov': .5, 'cy0': -.02, 'cy1': .16, 'rays': .4}))
        L = Light(**{**SUNL, 'key': (-.3, .2, .9), 'keyCol': '#b8603c', 'amb': '#4c2440'})
        c = V(1, 27.5, -18); sun = nz(V(.02, .16, -1.)); p = cam.eye + nz(V(.02, .17, -1.)) * (d + 27) + V(0, 1.5 * smooth(17, 23, f), 0)
        op = smooth(17, 22, f); P = JT.dive(1.).mix(JT.brake(.74).set(neck=(22, -4, 0.), head=(0., 18., 0.)), op)
        st.open(cam, L)
        S = JT.draw(st, P, at=p, yaw=3, pitch=lerp(16, -14, op), roll=-8 * (1 - op), face=Face(frown=.6, spark=1.))
        st.close()
        turn = smooth(13, 19, f)
        st.open(cam, RV.silhouette('#12040c', inkRef=1.2)); Pr = RV.R_STAND.set(hedr=(0, 4 - 20 * turn, 0), cher=(0, -3 - 9 * turn, 0), lh=lerp(np.array(RV.R_STAND.lh), V(4.6, 12.6, 1.), turn), lhand='claw' if turn > .5 else 'fist'); S2 = RV.fig(st, Pr, at=(-3.5, -1.5, 4), yaw=180, scale=.92, fan=1., arms=.0, u=None); RV.cape(st, S2, t, wind=(.25, 0, .25)); st.close()
        if f >= 18: IM.speedlines(st, tuple(cam.project(S.p('breast'))[:2].astype(float)), .55 * smooth(18, 23, f), (.05, .01, .03), seed=f // 2, inner=.55, dens=11)
        if f >= 20: IM.zoomblur(st, (960, 470), .02)
        return st.finish(bloom=.6, thr=.85, vig=.5, contrast=1.1, satu=1.08)

    def sky(self, st, t, sun, **k):
        st.paint('sky.frag', **SKY(None, **{**RED, 'sunDir': sun, 'sunR': .12, 'cov': .85, 'cy0': -.12, 'cy1': .55, 'cdrift': .25, 'cLit': '#ff9a50', 'cCM': '#b02a20', 'cSh': '#4a0c20', **k}))

    def sparks(self, st, at, q, n=120, sp=60, size=.5, seed=3):
        if q < 0: return
        FX.burst(st, n, at, q, speed=sp, grav=26, size=size, seed=seed, col='#ffd070', kind='streak', life=.55, drag=2.2, stretch=.06); FX.burst(st, n // 3, at, q, speed=sp * .6, grav=14, size=size * 1.8, seed=seed + 1, col='#f2b040', kind='flake', life=.8, drag=1.8)
        if q < .17: FX.particles(st, np.array([at]), size * 30 * (1 - q * 4.5), '#ffe0a0', 'spark', seed=[.3]); FX.particles(st, np.array([at]), size * 9 * (1 - q * 4), '#ffc060', 'glint')

    def beak(self, f, st, t):
        """f30: the old beak comes down on the dark dome"""
        g = f; u = (f - 24) / 11.; hit = impulse((f - 30) / 24., 10); dx, dy = shake(f, 1.6 * hit, 1.3, 3); push = 7 * ease_out((f - 30) / 5.) if f >= 30 else 0.
        cam = Cam(V(-40 + 14 * u + dx, 50 + dy, 60 - 6 * u), V(0, 51 - .3 * push, 2), 47, roll=-14 + 22 * u); st.cam = cam; self.sky(st, t, (.5, .16, -1.))
        L = Light(**{**SUNL, 'inkRef': 3., 'key': (-.5, .4, .7)}); dome = V(-1.5, 44.5, 4.5)
        pose = keys(f, [(24, JT.brake(1.)), (27, JT.brake(.8).set(neck=(52, 30, 0.), head=(0., -14., 0.), reach=1.0, jaw=.9)), (30, JT.strike(.62).set(neck=(-16, -48, 0.), head=(0., 34., 0.), reach=1.3, jaw=.3), 'in'), (32, JT.strike(.62).set(neck=(-10, -40, 0.), head=(0., 30., 0.), reach=1.25, jaw=.5)), (36, JT.flap(.0).set(jaw=.8), 'out')])
        J = dict(yaw=-58, pitch=keys(f, [(24, -10.), (28, -20.), (30, 30., 'in'), (33, 22.), (36, 0.)]), roll=keys(f, [(24, -16.), (30, 10., 'in'), (36, -6.)])); bk = JT.draw(st, pose, draw=False, **J).p('beak')
        at = dome - bk + V(*keys(f, [(24, (26, 34, -16)), (28, (12, 20, -6)), (30, (0, 0, 0), 'in'), (32, (0, .6, 0)), (36, (10, 16, -6))]))
        st.open(cam, L, far=3000.)
        P = VH.pushpaka(st, at=(0, 0 - .5 * push, 0), yaw=64, pitch=2 * hit, roll=-6 + 7 * hit, scale=6, mood=1., lamps=1.3, t=t * 1.5)
        S = JT.draw(st, pose, at=at, **J, face=Face(frown=.8, spark=.8))
        st.close()
        if f >= 30:
            q = (f - 30) / 24.; self.sparks(st, dome + V(0, 1, 3), q, 170, 70, .5); FX.burst(st, 60, dome, q, speed=44, grav=40, size=1.5, seed=9, col='#8a4a20', kind='flake', life=1.1, up=.5)
            JT.shed(st, S, q, 18, where='breast', speed=12, size=1.0)
        clouds(st, t, 9, 5, (20, 100), -40)
        if f in (30, 31): IM.shock(st, tuple(cam.project(dome)[:2].astype(float)), 90 + 200 * (f - 30), 60, 34)
        if f == 24: IM.whip(st, 90, 20)
        return st.finish(bloom=.55, thr=.85, vig=.5, contrast=1.1, satu=1.08, flash=.015 * (f == 30), flashCol='#ffd0a0')

    def buffet(self, f, st, t):
        """f42: seen over the great wings, the king is thrown back"""
        u = (f - 36) / 11.; hit = impulse((f - 42) / 24., 8); dx, dy = shake(f, 1.0 * hit, 1.2, 5); back = keys(f, [(42, 0.), (45, 22., 'out'), (47, 24.)])
        cam = Cam(V(5 - 8 * u + dx, 22 + dy, 70 - 3 * u), V(1, 23., -10), 54, roll=10 - 18 * u); st.cam = cam; self.sky(st, t, (-.30, .14, -1.))
        L = Light(**{**SUNL, 'inkRef': 2., 'rim': (-.4, .35, -.9), 'keyCol': '#b8563c'})
        ph = keys(f, [(36, .78), (40, 1.06), (43, 1.46, 'in'), (45, 1.56), (47, 1.72)]); pose = JT.flap(ph, 1.2).set(neck=(22, 4, 0.), head=(0., 14., 0.), legs=(.8, .7), claw=(.8, .9), jaw=.8 if f >= 40 else .3, tail=(-20, .9, 0.))
        st.open(cam, L, far=3000.)
        VH.pushpaka(st, at=(-95, 2 + 2 * math.sin(t), -190), yaw=70, pitch=-2, roll=3, scale=4.2, mood=1., lamps=1.2, t=t * 1.5)
        Pr = keys(f, [(36, RV.R_SWORD(0.)), (41, RV.R_SWORD(.15)), (43, RV.R_STRUCK, 'out'), (47, RV.R_STRUCK.set(pel=(0, 7.4, .2)))])
        S2 = RV.fig(st, Pr, at=(8 + 1.5 * back, -4 + .50 * back, -2 - 2.6 * back), yaw=-8, pitch=-22 * smooth(41, 45, f), roll=8 * smooth(42, 47, f), scale=1.75, fan=1., arms=.9, eyeglow=1., face=Face(frown=.6, mouth=.5 * smooth(41, 43, f), teeth=.4)); RV.cape(st, S2, t * 2, wind=(0, .1 + .3 * hit, -.5 - .7 * hit))
        S = JT.draw(st, pose, at=(-7, 31. + 3 * smooth(36, 40, f) - 6 * smooth(40, 43, f), 31), yaw=170, pitch=-20, roll=-5 + 6 * u, face=Face(frown=.8, spark=.8))
        st.close()
        clouds(st, t, 8, 8, (0, 70), -70, v=180)
        if f >= 41:
            q = (f - 41) / 24.; r = np.random.default_rng(7)
            for k in range(12):
                a = r.uniform(0, 6.28); rr = r.uniform(9, 26); s_ = np.linspace(0, 1, 26); z0 = 20 - 210 * q; Pw = np.c_[(rr + 6 * s_) * np.cos(a + .9 * s_), 20 + (rr + 6 * s_) * .62 * np.sin(a + .9 * s_), z0 - 50 + 60 * s_]; FX.ribbon(st, Pw, np.interp(s_, [0, .4, 1], [.05, .8, .1]), 'wind', '#fff0d0', '#ffb060', seed=k, amt=.9 * (1 - smooth(.14, .26, q)))
            FX.burst(st, 60, (3, 0, -22), q, speed=40, grav=6, size=.5, seed=4, col='#ffc070', kind='streak', life=.5, spread=(1., .6, .6)); JT.shed(st, S, q, 16, where='wristL', speed=22, size=1.0); JT.shed(st, S, q, 16, where='wristR', speed=22, size=1.0, seed=9)
        if 42 <= f < 45: IM.zoomblur(st, tuple(cam.project(V(3, 16, -30))[:2].astype(float)), .07 * (45 - f) / 3)
        IM.speedlines(st, (960, 560), .45 * hit, (.05, .01, .03), seed=f // 2, inner=.45)
        return st.finish(bloom=.55, thr=.85, vig=.5, contrast=1.1, satu=1.08)

    def talon(self, f, st, t):
        """f54: talon on sword, a star of sparks; then he draws back for the last cut"""
        u = (f - 48) / 11.; hit = impulse((f - 54) / 24., 9); dx, dy = shake(f, 1.0 * hit, 1.3, 7)
        cam = Cam(V(-8 + 12 * u + dx, 14 + dy, 60 - 5 * u), V(6, 28.5, 0), 52, roll=-14 + 24 * u); st.cam = cam; self.sky(st, t, (.1, .22, -1.), sunR=.14)
        L = Light(**{**SUNL, 'inkRef': 1.8, 'pts': [(V(3, 27, 5), 12., tuple(np.array([2.2, 1.2, .45]) * hit))] if hit > .02 else []})
        Pr = keys(f, [(48, RV.R_STAND.set(rh=(-3.4, 11.6, 3.4), rel=(-1, -.4, -.2), rhand='grip', rfing=(.5, .3, .8), rpalm=(.7, -.2, -.5), pel=(0, 7.8, 0), cher=(-4, 6, 0), hedr=(0, -6, 0), lh=(5., 10.5, 2.), lhand='claw')), (52, RV.R_STAND.set(rh=(-2.6, 15.6, 3.0), rel=(-1, -.4, -.2), rhand='grip', rfing=(.5, .3, .8), rpalm=(.7, -.2, -.5), cher=(-10, -8, 0), hedr=(0, -18, 0), lh=(5., 11., 2.), lhand='claw'), 'out'), (54, RV.R_STAND.set(rh=(-2.2, 15.0, 3.0), rel=(-1, -.4, -.2), rhand='grip', rfing=(.5, .3, .8), rpalm=(.7, -.2, -.5), pel=(0, 7.9, 0), cher=(-6, -2, 0), hedr=(0, -14, 0), lh=(5., 10., 2.), lhand='claw')), (56, RV.R_STAND.set(rh=(-2.2, 15.0, 3.0), rel=(-1, -.4, -.2), rhand='grip', rfing=(.5, .3, .8), rpalm=(.7, -.2, -.5), pel=(0, 7.9, 0), cher=(-6, -2, 0), hedr=(0, -14, 0), lh=(5., 10., 2.), lhand='claw')), (59, RV.R_SWORD(0.), 'out')])
        st.open(cam, L, far=3000.)
        S2 = RV.fig(st, Pr, at=(-9, -2, 0), yaw=38, scale=1.6, fan=1., arms=.9, eyeglow=1., face=Face(frown=.7, mouth=.3, teeth=.4)); RV.cape(st, S2, t * 2, wind=(-.4, .1, -.3))
        up = S2.d((.25, 1, .1)); hand = S2.palm('R', 0., .62, .28)
        if f < 57: st.fig(PR.SWORD, M=PR.place(hand, up, S2.d((0, 0, 1)), 2.5)); edge = hand + nz(up) * 8.
        else: RV.hold(st, S2, PR.SWORD, scale=1.6); edge = hand
        op = keys(f, [(48, .5), (53, 1., 'out'), (59, 1.)]); pose = JT.brake(op).set(legs=(1.05, 1.0), claw=(.9, .9) if f < 54 else (.15, .7), neck=(46, 10, 0.), head=(0., 24., 0.), jaw=.9)
        S0 = JT.draw(st, pose, at=(0, 0, 0), yaw=-74, pitch=-20, roll=6, draw=False); tl = S0.p('talonL'); d = keys(f, [(48, (27, 13, -8)), (53, (3, 4, -1), 'in'), (54, (0, 0, 0)), (56, (0, .4, 0)), (59, (7, 8, -3), 'out')]); anchor = edge if f < 57 else V(2, 30, 3)
        S = JT.draw(st, pose, at=anchor - tl + V(*d) + V(0, .8, 0), yaw=-74, pitch=-20, roll=6, face=Face(frown=.8, spark=.8))
        st.close()
        if f >= 54: self.sparks(st, edge if f < 57 else V(2, 30, 3), (f - 54) / 24., 200, 46, .34, 5)
        clouds(st, t, 9, 11, (0, 70), -50)
        if f >= 54: JT.shed(st, S, (f - 54) / 24., 14, where='breast', speed=10, size=.8)
        if f in (54, 55): IM.shock(st, tuple(cam.project(edge)[:2].astype(float)), 80 + 220 * (f - 54), 70, 30)
        return st.finish(bloom=.6, thr=.85, vig=.5, contrast=1.1, satu=1.08, flash=.02 * (f == 54), flashCol='#fff0c0')

    def fall(self, f, st, t):
        """f60 the blade; then no sound: one wing, the feathers, and the old eye still on her as he goes down"""
        q = (f - 61) / 24.; slow = 1 - .30 * smooth(61, 66, f); tt = max(0., q)
        if f < 62:                                                                          # the cut itself, seen from below, and its print
            cam = Cam(V(-4, 16, 46), V(4, 25, 0), 44, roll=12); st.cam = cam; self.sky(st, t, (.1, .2, -1.), sunR=.14); L = Light(**{**SUNL, 'inkRef': 1.8})
            st.open(cam, L, far=3000.); S2 = RV.fig(st, RV.R_SWORD(.55), at=(-14, 2, 2), yaw=52, scale=1.5, fan=1., arms=.9, eyeglow=1., face=Face(frown=.8, mouth=.4, teeth=.5)); RV.hold(st, S2, PR.SWORD, scale=2.2)
            S = JT.draw(st, JT.flap(.12).set(neck=(40, 8, 0.), jaw=1., legs=(.8, .6)), at=(13, 28, -4), yaw=-62, pitch=-22, roll=-18, face=Face(frown=.2, sad=.5)); st.close()
            w = cam.project(S.p('wristL') * .35 + S.p('shoulderL') * .65)[:2]; k = np.linspace(-1, 1, 40); A = np.c_[w[0] + 1150 * k, w[1] + 420 * k - 110 * (1 - k * k) + 60]
            FX.ribbon(st, A, np.interp(k, [-1, 0, 1], [0, 34, 0]), 'light', '#fff0d0', '#ffffff', amt=2.); FX.ribbon(st, A + 0., np.interp(k, [-1, 0, 1], [0, 70, 0]), 'brush', '#fff4e0', amt=1.)
            if f == 60: IM.inkflash(st, dark='#0a0408', mid='#b0141c', light='#fff2dc', lo=.36, hi=.60)
            return st.finish(bloom=.4, thr=.9, vig=.5, contrast=1.1, satu=1.05)
        u = (f - 62) / 9.; e = ease_in((f - 65) / 6.5, 1.8); sl = (f - 62) / 24. * (1 - .45 * smooth(62, 64, f) * (1 - smooth(66, 69, f)))
        cam = Cam(V(0, 0, 0), V(.0, -60, -16), 40, roll=5 - 8 * u, up=(0, 0, -1)); st.cam = cam
        self.below(st, cam, f, V(300 + 30 * u, 0, 900))
        L = Light(**{**SUNL, 'key': (.45, .85, -.2), 'keyCol': '#f09a64', 'amb': '#6a4474', 'rim': (.8, -.2, -.5), 'rimCol': (1.6, .8, .35), 'fogCol': '#2a1436', 'fog': (.0030, 50., 0., 0.), 'inkRef': 1.2, 'pts': [(V(6, -12, -14), 16., (.9, .42, .16))]})
        d = 27.5 + 2.5 * u + 95 * e; at = V(-3.2 + 1.6 * u + 4 * e, -d, -1.2 - .10 * d + 23 * e)
        pose = JT.wing_lost(.35 + 1.1 * sl, side=1); pose = pose.set(R=pose.R.mix(JT.Wing(elev=34, sweep=8, twist=6, fold=.10, hand=10, bend=.3), .6), neck=(44, 34, 10.), head=(42 - 6 * u, -30 + 6 * u, 4.), jaw=.22, legs=(.35, .25))
        st.open(cam, L, far=2000.)
        S = JT.draw(st, pose, at=at, yaw=6 + 10 * u, pitch=-82 - 16 * e, roll=-4 + 10 * u + 18 * e, face=Face(frown=0., sad=.5, lid=.92, gy=.45, gx=.2, spark=.8))
        wp = JT.Wing(elev=20 + 8 * math.sin(5 * sl), twist=10, fold=.10, ulna=4, hand=-8, bend=.25)
        W_ = JT.draw(st, JT.GLIDE.set(L=wp, R=wp), at=V(6 + 7 * u, -27 - 5 * u, -9 - 5 * u), yaw=-20 + 46 * u, pitch=-64 + 22 * u, roll=24 - 30 * u, parts=('wingL',)); rr = np.random.default_rng(8); m_ = 34; rt = W_.p('shoulderL') + rr.normal(size=(m_, 3)) * .75; dd_ = nz(W_.p('shoulderL') - W_.p('wristL')) + rr.normal(size=(m_, 3)) * .55; plume(st, JT.feathers(rt, dd_, np.tile([[0., 1., .1]], (m_, 1)) + rr.normal(size=(m_, 3)) * .5, rr.uniform(1.6, 3.2, m_), .42, .15, .25, 6., nl=12, nv=5), JT.KINGLY['cov2'])
        r = np.random.default_rng(5); n = 190; dr = r.normal(size=(n, 3)) * V(1.25, .75, 1.); dr /= np.linalg.norm(dr, axis=1, keepdims=True); k = r.uniform(.2, 1., (n, 1)); g = (1 - math.exp(-2.6 * (sl + .16))) / 2.6; org = V(4, -26, -8); ph = r.uniform(0, 6.28, n)
        P = org + dr * (.35 + k) * 62 * g + V(0, -1, .1) * 10 * k * sl; P[:, 0] += 1.1 * np.sin(2.4 * t + ph); P[:, 2] += .8 * np.cos(2. * t + ph)
        hx, hy, hz = cam.project(S.p('head')); X = cam.project(P); far_ = np.hypot(X[:, 0] - hx, X[:, 1] - hy) > 290 - 130 * e; ok = (X[:, 2] > 14) & (far_ | (X[:, 2] > hz + 6)); gust = 1.6 * np.sin(2.1 * sl * 6 + ph)
        th = ph + gust; D = np.stack([np.cos(th), .5 * np.sin(th * 1.3 + ph), np.sin(th)], 1); N_ = np.stack([.5 * np.sin(ph * 3 + t), np.ones(n), .5 * np.cos(ph * 2 + t * .8)], 1); Lf = r.uniform(.9, 2.6, n)
        for nm, sel in (('cov1', np.arange(n) % 3 == 0), ('cov2', np.arange(n) % 3 == 1), ('sec', np.arange(n) % 3 == 2)):
            q_ = ok & sel; kk = 1.5 if nm == 'sec' else 1.; plume(st, JT.feathers(P[q_], D[q_], N_[q_], Lf[q_] * 1.5 * kk, Lf[q_] * .24 * kk, .30 * np.sin(ph[q_] * 2), .25, 6., nl=12, nv=5), JT.KINGLY[nm])
        st.close()
        FX.particles(st, (org + dr * k * 74 * g)[:80], .16, '#ffd27a', 'flake', rot=ph[:80] + t * 3, seed=r.uniform(0, 1, 80))
        return st.finish(bloom=.5, thr=.85, vig=.6, contrast=1.08, satu=.95, flash=.02 * (f == 62), flashCol='#fff0d8')

    def below(self, st, cam, f, at, h=250.):
        """the night forest far down, seen along the same lens"""
        c2 = Cam(V(at[0], h, at[2]), V(at[0], h, at[2]) + cam.R[2], cam.fov); c2.R = cam.R
        L = Light(key=(.6, .45, -.5), keyCol='#d0605a', amb='#34346e', rimCol=(0, 0, 0), bounceCol=(0, 0, 0), shadow=False, ink=2.4, inkCol='#05060f', inkRef=6., fogCol='#3a1838', fog=(.0010, 120., 0., 0.)); st.cam = c2
        st.open(c2, L, far=3000.); place.draw(st, TORN, u=tornu(leafA='#56607a', leafB='#1c2448', gA='#50304a', gB='#1a1430'), defs='#define CANOPY\n#define NOROCK\n#define NOISLE\n#define NOHUT', sun=0.); st.close(); st.cam = cam
        st.L.color_attachments[1].write(np.full((st.ph, st.pw), 6e4, 'f4').tobytes()); st.paint(MIST, 'over')

    def letgo(self, f, st, t):
        """her hand over the edge of the floating earth; a scrap of yellow cloth, and in it a spark"""
        u = (f - 72) / 11.; q = max(0., (f - 73.5) / 24.); g = on2(f)
        cam = Cam(V(1.3, 6.6, 3.0), V(1.3, 6.6, 3.0) + V(-.06 + .03 * u, -.80, -.58) * 10, 46, roll=-8 + 5 * u); st.cam = cam
        self.below(st, cam, f, V(620 + 16 * u, 0, 780 - 20 * u))
        hand = V(.9, 3.0, .6); L = Light(key=(.4, .8, .2), keyCol='#e8845c', amb='#4a2c58', rim=(-.7, .2, -.6), rimCol=(1.5, .65, .25), bounceCol=(.10, .03, .06), envT='#ffb070', envM='#d8502c', envB='#3a1030', shadow=False, ink=3.6, inkRef=.7)
        fall_ = .5 * 13 * q * q + .6 * q; bp = V(.1 + .5 * q, 2.15 - min(fall_, 2.) - max(0., fall_ - 2.) * 1.6, -1.2 - 1.5 * q)
        dd = 90 * ease_in(clamp((q - .10) / .33), 1.9); c0 = Cam(V(1.3, 6.6, 3.0), V(1.3, 6.6, 3.0) + V(-.045, -.80, -.58) * 10, 46, roll=-5); palm = c0.eye + c0.ray(690, 640) * 4.9; bp = palm + c0.ray(880, 600) * .95 + V(.1, 0, -.35) + V(0, -5 * min(q, .16) ** 2, 0) + c0.ray(1010, 600) * dd
        st.open(cam, L)
        Ph = PZ.STAND.set(rh=(-3.2, 8.1, 3.6), rel=(-1, -.2, .2), rhand='pinch' if f < 73 else 'relax' if f < 75 else 'open', rfing=(0, 0, 1), rpalm=(0, -1, 0)); A = ARM.variant(pal={1: SKIN['sita']}, u=dict(side=1, band=0), build=dict(arm=.60, hand=.84)); S0 = st.fig(A, Ph, draw=False); st.fig(A, Ph, M=place_hand(S0, 'R', palm + V(-.12 * smooth(73, 76, f), .22 * smooth(73, 76, f), .12 * smooth(74, 82, f)), (.36, .02 + .16 * smooth(73, 77, f), -.93), (-.25, -.88, -.28), 1.0))
        if dd < 40:
            s0 = 1. ; bund = CL.sheet(lambda a, b: bp + V(.42 * math.sin(b * 3.14) * math.cos(a * 6.283) * (1 + .12 * math.sin(a * 25)), -.42 + .84 * b - .10, .42 * math.sin(b * 3.14) * math.sin(a * 6.283) * (1 + .12 * math.cos(a * 19))), 20, 12); st.mesh(*bund, kind=1, col=('#f2b428', '#9a5a1c', '#a83a1c'), cls=1, ink=.85)
            for sg in (-1, 1):
                Q = CL.lag(lambda tt: bp + V(.05 * sg, .30, 0), t, n=10, length=1.5, wind=(.45 * sg, .9 * smooth(0, .2, q) - .2, -.2), grav=.1, wave=1.2, freq=3., phase=sg); st.mesh(*CL.strip(Q, [.16, .5, .34], up=(.2, .2, 1), m=5, curl=.15, n=20, twist=.8 * sg), kind=1, col=('#f2b428', '#9a5a1c', '#a83a1c'), cls=1, ink=.85)
            st.fig(PR.RING, M=PR.place(bp + V(.14, .22, .34), (.3, .7, .6), (1, 0, 0), .22)); th = np.linspace(0, 4.6, 24); st.mesh(*CL.tube(bp + np.c_[.36 * np.cos(th) - .05, -.18 + .16 * np.sin(th * .7), .36 * np.sin(th) + .12], .05, 7), kind=0, col=('#ffffff', '#805030', '#fff'), cls=2, ink=.7)
        st.close()
        tw = .8 + .2 * math.sin(t * 23); FX.particles(st, np.array([bp + V(.1, .2, .3)]), (.9 + .022 * dd) * tw, '#ffd070', 'glint'); FX.particles(st, np.array([bp + V(.1, .2, .3)]), .30 + .020 * dd, '#fff0c0', 'lamp')
        if dd > .5:
            k = np.linspace(0, 1, 20)[:, None]; tail = bp + (V(.0, 1, .12)) * k * min(dd * .55, 14); FX.ribbon(st, tail, np.linspace(.03 + .004 * dd, .0, 20), 'light', '#ffc060', '#fff0c0', amt=.8)
        r = np.random.default_rng(4); n = 26; Pf = np.c_[r.uniform(-6, 6, n), np.mod(r.uniform(0, 1, n) * 20 - 5 * t * r.uniform(.6, 1.3, n), 20) - 15, r.uniform(-9, 1, n)]; FX.particles(st, Pf, .26 * r.uniform(.6, 1.3, n), '#b0743a', 'feather', rot=r.uniform(0, 6, n) + t, seed=r.uniform(0, 1, n), alpha=.95)
        return st.finish(bloom=.6, thr=.85, vig=.6, contrast=1.08, satu=1.0)

    def hill(self, f, st, t):
        """a dark hill; five of the forest people look up"""
        g = on2(f); u = (f - 84) / 11.
        cam = Cam(V(-3 + 1.2 * u, 9.5, 66 - 2 * u), V(0, 25 - 1.5 * u, 0), 40, roll=0); st.cam = cam
        st.paint('sky.frag', **SKY(None, **{**RED, 'cZen': '#140a2a', 'cMid': '#4a1436', 'cHor': '#d84a24', 'cLow': '#3a1024', 'sunR': 0., 'sunDir': (.55, .03, -1.), 'cov': .55, 'cy0': .03, 'cy1': .22, 'starAmt': .5, 'rays': .06, 'sunGlow': .35, 'cLit': '#e8602c', 'cCM': '#7a1c34', 'cSh': '#2a0c28', 'cdrift': .02}))
        L = Light(key=(.6, .25, -.6), keyCol='#a8442c', amb='#1c1638', rim=(.55, .2, -.8), rimCol=(1.6, .6, .22), bounceCol=(0, 0, 0), envT='#4a1c3a', envM='#d8502c', envB='#100818', shadow=False, ink=3., inkCol='#05030a')
        st.open(cam, L)
        st.world(HILL)
        up = keys(g, [(84, 0.), (85, 0.), (88, 1., 'back'), (96, 1.)])
        G = [(VA.SUGRIVA, -13., 0., 1.0, 160), (HM.HANUMAN, -1.5, .0, 1.06, 172), (VA.KINDS[0], -7.6, -1.2, .92, 190), (VA.KINDS[2], 5.2, -.8, .95, 200), (VA.KINDS[4], 11.4, -.2, .90, 205)]
        for i, (fig, x, z, sc, yaw) in enumerate(G):
            k = clamp(up * 1.25 - .06 * i); y = 8.4 - .030 * x * x + .0 * x; base = HM.H_STAND if fig is HM.HANUMAN else VA.V_STAND; pose = base.set(hedr=(0, 14 - 44 * k, 0), cher=(0, 8 - 13 * k, 0))
            st.fig(fig, pose, at=(x, hillh(x, z) - .1, z), yaw=yaw, scale=sc)
        st.close()
        # the chariot, a red coal going away, and the spark it has dropped
        c = V(-58 + 22 * u, 80 + 3 * u, -190); FX.particles(st, np.array([c + V(0, 1, 0)]), 9., '#c8301c', 'ember', alpha=.5)
        st.open(cam, Light(**{**SUNL, 'inkRef': 3., 'ink': 2.})); VH.pushpaka(st, at=c, yaw=78, pitch=-4, scale=1.5, mood=1., lamps=2.); st.close()
        A, B = V(-40, 74, -150), V(33, 13, -52); q = ease_in((f - 84) / 8., 1.25); p = lerp(A, B, min(q, 1.)) + V(0, 9 * math.sin(math.pi * min(q, 1.)), 0)
        k = np.linspace(0, 1, 30); Q = np.array([lerp(A, B, max(0., min(q, 1.) - .16 * v)) + V(0, 9 * math.sin(math.pi * max(0., min(q, 1.) - .16 * v)), 0) for v in k])
        if f < 92: FX.ribbon(st, Q, np.linspace(.8, .0, 30), 'light', '#ffb050', '#fff0c0', amt=1.2); FX.particles(st, np.array([p]), 9. * (.8 + .2 * math.sin(t * 24)), '#ffd070', 'glint'); FX.particles(st, np.array([p]), 3.2, '#fff0c0', 'lamp')
        else:
            h = (f - 92) / 24.; FX.particles(st, np.array([B]), 9 * (1 - h * 2.), '#ffc060', 'glint'); FX.burst(st, 30, B, h, speed=16, grav=16, size=.5, seed=3, col='#ffd070', kind='ember', life=.6, up=.8); FX.particles(st, np.array([B]), 2.2, '#ffb050', 'lamp', alpha=.9)
        FX.embers(st, 12, ((-20, 4, -8), (20, 10, 6)), t, rise=1.2, size=.06, seed=3, col='#8aa0ff', life=3.)
        return st.finish(bloom=.6, thr=.85, vig=.5, contrast=1.1, satu=1.0, fade=.85 * smooth(93, 96, f), fadeCol='#0c1018')


def hillh(x, z): return 7.6 - .020 * x * x - .006 * z * z + .5 * math.sin(x * .33 + 1.)


HILL = """
#define TMAX 400.
#define STEPS 90
#define NOAO
float hh(vec2 q){return 7.6-.020*q.x*q.x-.006*q.y*q.y+.5*sin(q.x*.33+1.);}
vec2 map(vec3 p){float d=(p.y-max(hh(p.xz),-20.)-.25*vn(p.xz*1.1)*smoothstep(2.,9.,length(p.xz*vec2(.5,1.))))*.55;float far_=(p.y+4.-10.*vn(p.xz*vec2(.03,.01)+3.)-5.*vn(p.xz*.11))*.5;far_=max(far_,p.z+34.);return d<far_?vec2(d,1.):vec2(far_,2.);}
void surf(vec3 p,vec3 n,int m,inout Surf s){s.cls=1.;float t=fbm(p.xz*.5);s.base=m==1?mix(hex(0x241a34),hex(0x4a2634),t):mix(hex(0x1a1430),hex(0x30183a),t);s.sh=s.base*.35;s.ink=m==1?.6:.3;}
"""
MIST = """
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform vec2 res;uniform float fT;
void main(){vec2 p=uv*vec2(res.x/res.y,1.);float m=fbm(p*vec2(2.2,2.8)+vec2(fT*.6,fT*.14));float a=smoothstep(.46,.82,m)*.55+.12;vec3 c=mix(hex(0x3a1438),hex(0xc04a30),smoothstep(.60,.90,m)*.7);float r=length(uv-vec2(1.05,1.05));c+=hex(0xff6a30)*exp(-r*r*5.)*.35;a=max(a,exp(-r*r*5.)*.6);o=vec4(c*a,a);}
"""
