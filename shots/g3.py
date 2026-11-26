"""g3 (108): Bharata by the empty throne with the sandals lifts his head (f0); old Kaushalya raises her lamp (f24); the streets, every hand a lamp (f44); they come, and the people bow in a wave (f76)."""
from lau.shot import *
from lau.look import *
from worlds import palace as PL
from chars import hanuman as HM
from .g_kit import *

SEAT = V(0, 14.75, 163.)
SPEED = 5.2                                                     # the walkers, units a second
TIER2 = float(AY.tier(2))


def run_lamp(ph, kid=True):
    """a child running with a lamp held before it"""
    p = PZ.run(ph, stride=2.6, lift=1.7, lean=10); L = PP.P_LAMP
    return PP.child_pose(p.set(lh=(.98, 10.3 + .3 * math.sin(ph * 12.57), 2.5), rh=(-.98, 10.3 + .3 * math.sin(ph * 12.57), 2.5), lhand=L.lhand, rhand=L.rhand, lfing=L.lfing, rfing=L.rfing, lpalm=L.lpalm, rpalm=L.rpalm, lel=L.lel, rel=L.rel, cher=(p.cher[0] * .4, p.cher[1], 0), hedr=(0, -8, 0)))


class Shot(ShotBase):
    id = 'g3'; n = 108
    EVENTS = [(0, 'quiet hall', dict(dur=24)), (8, 'crowd far', dict(dur=36)), (10, 'head lifts', dict(soft=1)), (30, 'lamp raised', {}), (44, 'crowd', dict(dur=64)), (48, 'children running', dict(dur=26)), (52, 'conch', {}), (60, 'temple bell', {}), (76, 'crowd joy', dict(dur=32)), (76, 'footsteps', dict(dur=32)), (84, 'crowd bows', dict(dur=24)), (90, 'temple bell', {})]

    def setup(self, st):
        T = people_tiles(True); nT = len(T) // 3                                        # 8 people x 3 bows
        self.nT = nT; self.yaws = (52., -52.); items = [(a, b, c, y) for y in self.yaws for a, b, c in T]
        self.cr = Crowd(st, items, px=560, pitch=0., cols=8); self.off = np.array([flame_offset(a, b, y) for a, b, c, y in items])
        self.run = Crowd(st, [(k, run_lamp(i / 6.), Face(smile=.9), y) for y in (138., -138., 50., -50.) for k in (PP.CHILD_LAMP, PP.CHILD_B_LAMP) for i in range(6)], px=420, pitch=0., box=(-4.5, -.5, 4.5, 9.5), cols=12)
        r = np.random.default_rng(17); P, Y = [], []
        # beat 3: both sides of the avenue, flat and stairs, three tiers deep
        for z in np.arange(-158, -500, -3.6):
            for s in (-1, 1):
                for x in (12.5, 17., 21.5, 26.5):
                    if r.uniform() < .80: P.append((s * (x + r.uniform(-1.6, 1.6)), z + r.uniform(-1.2, 1.2))); Y.append(s)
        P = np.array(P); self.A = np.c_[P[:, 0], AY.ground(P[:, 0], P[:, 1]), P[:, 1]]; self.As = np.array(Y); self.Ak = r.integers(0, nT, len(P))
        # beat 4: along the landing and up the stairs behind
        P, Y = [], []
        for z in np.arange(-392, -500, -3.4):
            for s in (-1, 1):
                for x in (15.5, 19.5, 23.5, 27.5):
                    if r.uniform() < .88: P.append((s * (x + r.uniform(-1.3, 1.3)), z + r.uniform(-1., 1.))); Y.append(s)
        P = np.array(P); self.B = np.c_[P[:, 0], AY.ground(P[:, 0], P[:, 1]), P[:, 1]]; self.Bs = np.array(Y); self.Bk = r.integers(0, nT, len(P)); self.lamps = AY.lamp_points()

    def frame(self, f, st):
        st.clear('#05071e', f=f)
        return (self.hall if f < 24 else self.mother if f < 44 else self.street if f < 76 else self.come)(f, st, st.t)

    # ---------------------------------------------------------------- Bharata
    def hall(self, f, st, t):
        u = f / 23.; g = on2(f); cam = Cam(lerp(V(-15, 20.5, 133), V(-13, 20.0, 136.5), ease_io(u, 1.5)), lerp(V(6.6, 17.4, 163), V(7.0, 17.6, 163), u), 34); st.cam = cam; lamp = V(-7.4, 17.8, 156.); I = flick(t, 4.)
        out = smooth(6, 18, f)                                                          # light from outside
        L = Light(key=(-.55, .25, -.80), keyCol=tuple(np.array([.030, .034, .085]) * (1 - out) + np.array([.17, .10, .06]) * out), amb=tuple(np.array([.050, .050, .125]) + np.array([.05, .02, .0]) * out), rim=(.6, .3, .7), rimCol=(.14, .16, .40), bounceCol=(.03, .015, .01), envT='#2a2a5a', envM='#ffa650', envB='#6a2c14', fogCol='#080a22', fog=(.002, 30, 0, 0), ink=3., inkRef=1.6, inkCol='#04030c', shadow=True,
                  pts=[(lamp + V(0, 1.2, -.4), 6.5, tuple(np.array([1.35, .66, .24]) * I)), (V(8.5, 20.5, 144.), 6.5, tuple(np.array([2.1, 1.25, .62]) * out))])
        st.open(cam, L, far=2000.); PL.draw(st, 'crown', lamps=0., dusk=0.)
        for sx in (-1, 1): st.fig(PR.SANDAL, M=PR.place(SEAT + V(2.6 + 1.2 * sx, .72, -.6), (0, 1, 0), (.10 * sx, 0, -1), 1.5))
        st.fig(LAMP, M=model(lamp - V(0, .75, 0), scale=1.55))
        lift = keys(g, [(0, 0.), (8, 0.), (10, -.10), (18, 1., 'io'), (24, 1.02)]); br = .4 * math.sin(t * 3)
        P = PP.B_SANDALS.set(pel=(0, 4.7, 0), pelr=(0, 4, 0), cher=(0, lerp(20, 2, lift) + br, 0), hedr=(lerp(0, 30, lift), lerp(34, -10, lift), lerp(4, -4, lift)), lh=(.34, lerp(6.5, 8.1, lift), 3.1), rh=(-.34, lerp(6.5, 8.1, lift), 3.1), lhand='anjali', rhand='anjali', lfing=(0, 1, .35), rfing=(0, 1, .35), lpalm=(-1, 0, 0), rpalm=(1, 0, 0))
        st.fig(PP.BHARATA, P, at=(13.4, 9, 154.), yaw=-160, face=Face(lid=keys(g, [(0, .12), (8, .12), (16, 1.02, 'out')]), gx=.25 * out, gy=.25 * out, sad=.35 * (1 - out) + .1, smile=.05 + .30 * smooth(14, 22, f), brow=.3 * out, spark=out)); st.close()
        FX.flame(st, lamp - V(0, 0, 0), 1.75, seed=1.3, glow=.55 * I, calm=.8)
        FX.embers(st, 12, (tuple(lamp + V(-.5, 1, -.5)), tuple(lamp + V(.5, 2, .5))), t, rise=1.4, size=.06, seed=4, life=2.)
        # dust in the light from the door
        if out > 0: FX.drift(st, 50, ((-12, 9, 138), (22, 32, 160)), t, kind='ember', size=.10, col='#ffc070', fall=.25, sway=.5, seed=8, spin=0, alpha=.45 * out)
        IM.dof(st, float((V(8, 16, 157) - cam.eye) @ cam.R[2]), 16., 5.)
        return st.finish(bloom=.45, thr=.9, vig=.55, contrast=1.06, fade=.6 * (1 - smooth(0, 3, f)), fadeCol='#04051a')

    # ---------------------------------------------------------------- Kaushalya
    def mother(self, f, st, t):
        u = (f - 24) / 19.; g = on2(f); cam0 = Cam((3, 66, -88), (0, 74, -300), 40); st.cam = cam0; st.paint('sky.frag', **AY.sky('night', sunGlow=0.)); st.open(cam0, AY.light('night', inkRef=2.), far=20000.); city(st, 1., .42); st.close(); amber(st, .9); glows(st, self.lamps, 1.1, 2.2, 1.); IM.defocus(st, 15.); IM.grade(st, (.62, .60, .66))
        up = keys(g, [(24, 0.), (28, -.06), (36, 1., 'io'), (40, 1.03), (44, 1.)]); I = flick(t, 5.)
        P = sita.fit(PP.P_LAMP.set(cher=(0, lerp(4, -3, up), 0), hedr=(0, lerp(16, -3, up), 2), lh=(.98, lerp(9.75, 11.15, up), lerp(1.9, 2.9, up)), rh=(-.98, lerp(9.75, 11.15, up), lerp(1.9, 2.9, up)), lel=(1, -1, .1), rel=(-1, -1, .1)))
        S = st.fig(PP.KAUSHALYA_LAMP, P, yaw=-10, draw=False); fl = PP.flame(S); e = S.head((0, 0, .8))
        cam = Cam(V(1.9 - .5 * u, 12.6 - .2 * u, 15.6 - 1.6 * ease_io(u, 1.5)), V(-.1, 12.15, 0), 21); st.cam = cam
        L = Light(key=(.2, -.1, .9), keyCol=(.16, .11, .09), amb=(.085, .080, .175), rim=(-.5, .5, -.8), rimCol=(.75, .42, .18), bounceCol=(.12, .05, .02), envT='#3a3a80', envM='#ffa650', envB='#c8641c', pts=[(fl + V(0, .5, .6), 2.6, tuple(np.array([2.1, 1.24, .62]) * I)), (fl + V(.4, 1.2, 2.2), 2.2, tuple(np.array([.55, .36, .22]) * I * up))], shadow=False, ink=3.4, inkCol='#06040c', hi=.3)
        st.open(cam, L); st.fig(PP.KAUSHALYA_LAMP, P, yaw=-10, face=Face(lid=keys(g, [(24, .35), (34, .95, 'io')]), gy=-.1 + .2 * up, sad=.22, smile=.12 + .42 * smooth(34, 42, f), spark=smooth(30, 36, f), tear=0., brow=.25 * up)); st.close()
        FX.flame(st, fl - V(0, .30, 0), .95, seed=2.2, glow=.75 * I, calm=.9); FX.embers(st, 12, (tuple(fl - V(.2, .1, .2)), tuple(fl + V(.2, .4, .2))), t, rise=1.2, size=.018, seed=5, life=1.8)
        FX.drift(st, 26, ((-6, 7, -3), (6, 18, 8)), t, size=.17, col='#f2a0b0', col2='#ffd080', fall=2., sway=.8, seed=9, alpha=.9)
        return st.finish(bloom=.5, thr=.9, vig=.5, contrast=1.06)

    # ---------------------------------------------------------------- the street
    def people(self, f, P, side, kind, level, st, near=15.):
        """crowd tiles for people standing on both sides (side -1 left, +1 right) turned toward the middle, with their bow level 0..2"""
        m = (P - st.cam.eye) @ st.cam.R[2] > near; P, side, kind, level = P[m], side[m], kind[m], level[m]; yi = np.where(side < 0, 0, 1); tile = yi * 3 * self.nT + np.clip(level, 0, 2).astype(int) * self.nT + kind
        bob = .12 * np.abs(np.sin(f / 24. * 4 + np.arange(len(P)) * 1.7)) * (level < .5); Q = P + np.c_[0 * bob, bob, 0 * bob]; self.cr.draw(Q, scale=1., tile=tile, tint=(1.35, 1.12, .95))
        return Q + self.off[tile]

    def street(self, f, st, t):
        u = (f - 44) / 31.; k = ease_io(u, 1.25); cam = Cam(lerp(V(-5.0, 58.0, -128), V(1.5, 62.0, -166), k), lerp(V(5, 67, -250), V(0, 86, -370), k), lerp(45, 49, k), roll=1.5 * math.sin(u * 3.6)); st.cam = cam
        st.paint('sky.frag', **AY.sky('night', sunGlow=0.)); e = cam.eye; pts = [((s * 10., float(AY.ground(0, e[2] - dz)) + 11., e[2] - dz), 9., (.30, .15, .06)) for dz in (38, 62, 90, 120, 150) for s in (-1, 1)] + [((s * 5., float(AY.ground(0, e[2] - 9)) + 11.5, e[2] - 9.), 7., (.85, .50, .26)) for s in (-1, 1)]
        st.open(cam, AY.light('night', inkRef=2., keyCol=(.22, .18, .20), key=(.2, .3, .9), fogCol='#171648', fog=(.0032, 70., 0, 0), pts=pts), far=20000.); city(st, 1., .34, trees=.35)
        fl = self.people(f, self.A, self.As, self.Ak, np.zeros(len(self.A)), st)
        # children run up the middle with their lamps
        kids, tt = [], t - 44 / 24.
        for i in range(12):                                                             # the even ones run up ahead of us, the odd ones come down toward us
            away = i % 2 == 0; z = -157. - 9 * i - 27. * tt if away else -226. - 11 * i + 15. * tt; w = i * 2.3 + t * 1.1; x = 5.0 * math.sin(w); yw = (0 if away else 2) + (0 if math.cos(w) > 0 else 1)
            kids.append((x, float(AY.ground(x, z)), z, yw * 12 + (i // 2 % 2) * 6 + int(t * 13 + i * 2) % 6, -1. if away else 1.))
        kids = np.array(kids); self.run.draw(kids[:, :3], scale=1.05, tile=kids[:, 3], tint=(1.5, 1.15, .92))
        # near the lens
        big = []
        for fig, x, z, yaw, seed in ((PP.CITIZEN_F_LAMP[1], -9.8, -152., 38, 0), (PP.CITIZEN_M_LAMP[1], 11.0, -160., -40, 1), (PP.CITIZEN_F_LAMP[0], 11.2, -184., -34, 2), (PP.CITIZEN_M_LAMP[0], -11.6, -178., 46, 3), (PP.CHILD_LAMP, -7.4, -183., 22, 4), (PP.CITIZEN_F_LAMP[2], -10.0, -206., 30, 5)):
            if z > e[2] - 4: continue
            y = float(AY.ground(x, z)); kid = fig is PP.CHILD_LAMP; p = PP.P_LAMP.set(hedr=(0, -2 + 3 * math.sin(t * 2 + seed), 3 * math.sin(t * 1.5 + seed)), lh=(.98, 10.4 + .2 * math.sin(t * 2.4 + seed), 2.1), rh=(-.98, 10.4 + .2 * math.sin(t * 2.4 + seed), 2.1)); p = PP.child_pose(p) if kid else sita.fit(p) if seed in (0, 2, 5) else p
            S = st.fig(fig, p, at=(x, y, z), yaw=yaw, face=Face(smile=.75, lid=.95, spark=.6), shadow=False); big.append(PP.flame(S))
        st.close(); amber(st, .9); glows(st, self.lamps, 1.1, 2.0, 1.); glows(st, fl, .55, 2.0, .95, seed=4); glows(st, kids[:, :3] + np.c_[0 * kids[:, 4], 6.3 + 0 * kids[:, 4], 1.3 * kids[:, 4]], .6, 2.0, 1., seed=6)
        for i, p in enumerate(big): FX.flame(st, p - V(0, .28, 0), .95, seed=i * 2., glow=.6)
        FX.drift(st, 170, (tuple(e + V(-32, -8, -70)), tuple(e + V(32, 34, 2))), t, size=.36, col='#f2a0b0', col2='#ffd080', fall=5.5, sway=1.6, seed=3, wind=(1.2, 0, 2.))
        IM.dof(st, 40., 60., 4.)
        return st.finish(bloom=.5, thr=.9, vig=.42, contrast=1.10, satu=1.14)

    # ---------------------------------------------------------------- they come
    def come(self, f, st, t):
        u = (f - 76) / 31.; g = on2(f); tw = (g - 76) / 24.; dz = SPEED * tw; e = ease_io(u, 1.3); cam = Cam(V(1.0 - 1.4 * e, TIER2 + 3.6 + .6 * e, -352 + 2.0 * u), V(.2, TIER2 + lerp(12.6, 10.4, e), -420), lerp(26.5, 20.5, e)); st.cam = cam; z0 = -427.
        wave = lerp(-455, -376, u) - 4
        st.paint('sky.frag', **AY.sky('night', sunGlow=0.)); zw = z0 + dz
        pts = [((s * 11.5, TIER2 + 9., z), 8., (.34, .17, .07)) for z in (-394, -440, -462) for s in (-1, 1)] + [((s * 8.5, TIER2 + 9.5, zw + a), 5.0, (1.75, 1.25, .86)) for s in (-1, 1) for a in (6, 15)] + [((-9.5, TIER2 + 6, -381), 5., (.5, .25, .1)), ((11., TIER2 + 6, -381), 5., (.5, .25, .1))]
        st.open(cam, AY.light('night', inkRef=1.6, key=(-.3, .35, .9), keyCol=(.20, .17, .19), amb='#232a66', rim=(0, .45, -1), rimCol=(.9, .50, .22), fogCol='#171648', fog=(.0075, 76., 0, 0), pts=pts), far=20000.); city(st, 1., .30, trees=.35)
        lv = np.clip((wave - self.B[:, 2]) / 4.5 + .6 * np.sin(np.arange(len(self.B)) * 2.4), 0, 2.4); fl = self.people(f, self.B, self.Bs, self.Bk, np.round(lv), st, 40.)
        calm = Face(smile=.42, lid=.86, spark=.5)
        ph = lambda stride: (tw * SPEED / (4 * stride)) % 1.
        bless = smooth(84, 92, f)
        Pr = PZ.walk(ph(1.35) + .06, stride=1.35, lift=.55, bounce=.14, swing=.8); Pr = Pr.set(hedr=(Pr.hedr[0] * .5 - 4, 3, 0)); Pb = Pr.set(rh=(-2.3, 11.2, 2.0), rhand='abhaya', rfing=(-.05, 1, .1), rpalm=(0, 0, 1), rel=(-.7, -1, -.3)); Pr = Pr.set(rhand=Pb.rhand if bless > .4 else 'relax', rh=tuple(lerp(np.array(Pr.rh), np.array(Pb.rh), bless)), rel=(-.7, -1, -.4), rfing=Pb.rfing if bless > .4 else None, rpalm=Pb.rpalm if bless > .4 else None)
        Sr = st.fig(RAMA, Pr, at=(-2.6, TIER2, z0 + dz), yaw=1, face=calm); Ss = st.fig(SITA_JEWEL, sita.S_WALK(ph(1.05) + .3), at=(3.4, TIER2, z0 + dz - .3), yaw=-2, face=calm.set(smile=.5))
        Pl = PZ.walk(ph(1.35) + .45, stride=1.35, lift=.55, bounce=.14, swing=.9); Sl = st.fig(rama.LAKSHMANA, Pl.set(hedr=(6, 2, 0)), at=(9.6, TIER2, z0 + dz - 4.5), yaw=-3, face=calm)
        Ph = HM.H_WALK(ph(1.35) + .25, stride=1.35, lift=.7); Ph = Ph.set(lh=(.34, 8.7, 2.75), rh=(-.34, 8.7, 2.75), lhand='anjali', rhand='anjali', lfing=(-.06, 1, .22), rfing=(.06, 1, .22), lpalm=(-1, 0, 0), rpalm=(1, 0, 0), lel=(1, -.55, -.1), rel=(-1, -.55, -.1), hedr=(-6, 12, 0))
        Sh = st.fig(HM.HANUMAN, Ph, at=(-9.6, TIER2, z0 + dz - 4.8), yaw=3, face=HM.VFace(smile=.5, lid=.8)); HM.tail(st, Sh, t, 'calm')
        # two citizens by the lens, bowing as they pass
        big = []
        for fig, x, z, yaw, at_, wm in ((PP.CITIZEN_F_LAMP[1], -11.8, -387., 158, 94, 1), (PP.CHILD_LAMP, 9.8, -385., -160, 98, 2)):
            b = keys(g, [(at_, 0.), (at_ + 10, 1., 'io')]); p = PP.P_LAMP.set(pel=(0, 8.3, -.7 * b), pelr=(0, 18 * b, 0), cher=(0, 24 * b, 0), hedr=(0, 4 + 20 * b, 0), lh=(.98, 10.3 - 2.0 * b, 2.1 + 1.3 * b), rh=(-.98, 10.3 - 2.0 * b, 2.1 + 1.3 * b)); p = [lambda q: q, sita.fit, PP.child_pose][wm](p); S = st.fig(fig, p, at=(x, TIER2, z), yaw=yaw, face=Face(smile=.7)); big.append(PP.flame(S))
        st.close()
        amber(st, .9); glows(st, self.lamps, 1.1, 2.0, 1.); glows(st, fl, .55, 2.0, .95, seed=4); IM.dof(st, float((V(0, TIER2 + 8, zw) - cam.eye) @ cam.R[2]), 36., 5.)
        kw = dict(size=.30, col='#f2a0b0', col2='#ffd080', fall=4.5, sway=1.0, wind=(.3, 0, 1.0))              # petals fall beside and behind the four, never across their faces
        for sd, n, lo, hi in ((3, 60, (-24, TIER2 - 2, -438), (-11.5, TIER2 + 26, -356)), (4, 60, (13.5, TIER2 - 2, -438), (25, TIER2 + 26, -356)), (5, 80, (-13, TIER2 - 1, -452), (14, TIER2 + 30, -434))): FX.drift(st, n, (lo, hi), t, seed=sd, **kw)
        return st.finish(bloom=.5, thr=.9, vig=.42, contrast=1.10, satu=1.14)
