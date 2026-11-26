"""f2 (96): the hosts meet.  f0-35 the camera runs down the closing gap between two armies toward the sun (f30-35 one held breath); f36 they meet and the sun goes out.
f41-71 the camera rips along the line, a blow on every pulse (f42 48 54 60 66); f72-96 it looks up: two storms of arrows, and under the sun Rama and Lakshmana shooting (f82, f90)."""
from .f_kit import *
from chars import hanuman as HM, vanara as VN, rakshasa as RK, rama, vehicles as VH

SUN = (.0, .155, -1.)
BLOWS = (42, 48, 54, 60, 66)
X = [0., 46., 92., 138., 184.]                          # where each duel stands along the line


def gap(f):
    """half the distance between the two fronts"""
    tau = f if f < 30 else 30 + (f - 30) * .10
    return 36 - .55 * tau - .0125 * tau * tau


def tau(f): return f if f < 30 else 30 + (f - 30) * .10


class Shot(ShotBase):
    id = 'f2'; n = 96
    EVENTS = [(0, 'two hosts run', dict(dur=30)), (0, 'war drums', dict(dur=30)), (30, 'held breath', dict(dur=6)), (36, 'hosts collide', {}), (37, 'dust wall', dict(dur=6))] + \
             [(42, 'mace breaks shield', {}), (48, 'tree sweeps two away', {}), (54, 'club on helm', {}), (60, 'rock bursts', {}), (66, 'club meets sword', {})] + \
             [(44, 'camera whip', {}), (50, 'camera whip', {}), (56, 'camera whip', {}), (62, 'camera whip', {}), (72, 'arrow storm', dict(dur=24)), (82, 'bow release', {}), (90, 'bow release', dict(k=1))] + [(f, 'arrows meet', dict(k=i)) for i, f in enumerate((76, 79, 82, 84, 87, 89, 91, 94))]

    def setup(self, st):
        self.va, self.rk = vanara_host(st, 66, 5., px=480), rakshasa_host(st, -60, 5., px=480)
        F = ROAR
        fight = [(VN.arm(VN.WARRIOR, 3), VN.V_THROW(.1), F, 70), (VN.arm(VN.WARRIOR2, 3), VN.V_THROW(.55), F, 70), (VN.arm(VN.LANGUR, 2), VN.V_THROW(.2), F, 60), (VN.arm(VN.LANGUR2, 1), VN.V_THROW(.45), F, 75), (VN.arm(VN.YOUTH, 1), VN.V_CHEER(.5), F, 40), (VN.arm(VN.JAMBAVAN, 4), VN.V_CARRY, F, 60),
                 (RK.SPEARMAN, RK.K_STAB(.1), F, -70), (RK.SPEARMAN, RK.K_STAB(.5), F, -70), (RK.HORN, RK.K_GUARD, F, -60), (RK.HULK, RK.K_RUN(.2), F, -60), (RK.HORN, RK.K_FALL, F, -50), (RK.TUSK, RK.K_FALL, F, -70)]
        self.fc = Crowd(st, fight, px=620, pitch=6., box=(-7, -.6, 7, 19))
        r = np.random.default_rng(8)
        n = 420; self.L = Host(self.va, np.c_[-r.uniform(0, 1, n) ** 1.25 * 150 - 7, np.zeros(n), r.uniform(-330, 40, n)], 1)
        n = 420; self.R = Host(self.rk, np.c_[r.uniform(0, 1, n) ** 1.25 * 150 + 7, np.zeros(n), r.uniform(-330, 40, n)], 2)
        n = 520; self.M = np.c_[r.uniform(-70, 260, n), np.zeros(n), -14 - 150 * r.uniform(0, 1, n) ** 1.3]; self.Mt = r.integers(0, 12, n); self.Ms = r.uniform(.9, 1.15, n); self.Mc = np.clip(r.normal(1, .1, (n, 1)), .7, 1.25) * np.ones((1, 3))
        # arrows of the storm: two flocks, start, velocity, launch time (s from f72)
        n = 230; self.A = []
        for side, seed in ((-1, 3), (1, 4)):
            q = np.random.default_rng(seed); p0 = np.c_[side * q.uniform(60, 190, n), q.uniform(4, 22, n), q.uniform(-170, -58, n)]; v = np.c_[-side * q.uniform(62, 96, n), q.uniform(46, 108, n), q.uniform(-6, 6, n)]; self.A.append((p0, v, q.uniform(-2.2, 1.0, n), q.uniform(0, 1, n) < .42))
        self.meet = [(f, V(X[4] + x, y, z)) for f, x, y, z in ((76, -26, 52, -60), (79, 24, 62, -70), (82, -8, 70, -70), (84, 40, 50, -60), (87, -40, 64, -70), (89, 12, 66, -60), (91, -20, 60, -80), (94, 30, 68, -70))]

    def frame(self, f, st):
        st.clear('#000', f=f)
        return self.charge(f, st) if f < 41 else self.line(f, st)

    def sky(self, st, **k): st.paint('sky.frag', **SKY(WAR, **{**dict(sunDir=SUN, sunR=.105, sunGlow=.55, rays=.45, cy0=.03, cy1=.30, cov=.5), **k}))

    # ---------------------------------------------------------------- the two fronts
    def charge(self, f, st):
        t = st.t; T = tau(f); G = gap(f); hit = f >= 36; a = (f - 36) / 24.; u = min(f, 36) / 36.
        zc = 70 - .80 * T; hold = smooth(29, 31, f) * (not hit)
        eye = V(0, lerp(2.6, 7.0, u), zc + (9 * (1 - math.exp(-a * 9)) if hit else 0)); cam = Cam(eye, eye + V(0, lerp(2.0, 1.6, u), -10), lerp(44, 42, ease_io(u)), roll=(3. * math.sin(T * .16)) * (1 - hold))
        cam = shaken(cam, f, (.16 * (1 - hold) if not hit else 1.6 * decay(a, 7.)), .8); st.cam = cam
        self.sky(st, sunGlow=.5 + .2 * u)
        L = war_light(key=(.15, .55, .8), keyCol=(.92, .66, .42), amb='#7a4a6a', rim=(0, .35, -.95), rimCol=(2.1, 1.05, .36), fogCol='#d8662c', fog=(.0048, 40., .006, 0.))
        st.open(cam, L); ground(st)
        far = lambda h: h.pos[:, 2] < zc - 50
        step = T * .5; dx = 46 - G
        self.L.draw(step, off=(-G + 3, 0, 0), mask=far(self.L)); self.R.draw(step + .5, off=(G - 3, 0, 0), mask=far(self.R))
        self.leads(f, st, T, G, zc, hold, hit)
        st.close()
        # dust under the feet
        zz = (zc - 120, zc - 10)
        for s in (-1, 1): footdust(st, 60, ((s * (G + 3), 1., zz[0]), (s * (G + 46), 3., zz[1])), T / 24. + 5, size=3.6, rise=3.8, alpha=.50 * (1 - .0 * hold), seed=5 + s, wind=(-s * 2, 0, 0))
        footdust(st, 26, ((-G, .6, zc - 70), (G, 1.4, zc - 16)), T / 24. + 5, size=1.7, rise=2.2, alpha=.20, seed=11, col=('#f0b870', '#c87a40'))
        FX.drift(st, 60, ((-30, 0, zc - 60), (30, 22, zc - 16)), T / 24. + 3, 'ash', size=.13, col='#5a2a1a', fall=-1.2, sway=1.2, seed=4, wind=(1.5, 0, 2))
        dustbank(st, .35, .62, 1.05, seed=2., speed=.2)
        x, y, _ = cam.project(V(0, 11, zc - 32))
        if hold: FX.particles(st, np.array([[960., 380.]]), 40 + 4 * (f - 30), '#fff0c0', 'glint', alpha=.25 * hold)
        if f > 37:
            leafburst(st, V(0, 12, zc - 31), a, speed=34, n=160, size=.30, seed=3, life=.8)
            r = np.random.default_rng(9); n = 90; z = zc - 34 - 190 * r.uniform(0, 1, n) ** 1.6; g = 1 - math.exp(-a * 7); px = r.normal(0, 1, n) * (3 + 16 * g); P = np.c_[px, r.uniform(0, 1, n) * 30 * g, z + 8 * g]; puffs(st, P, (4 + 15 * g) * r.uniform(.6, 1.2, n), col=('#f2bc74', '#a8562c'), alpha=min(1, .9 * a * 14), seed=6, soft=6)
            IM.zoomblur(st, (float(x), float(y)), .12 * decay(a, 9))
            dustbank(st, smooth(37, 40., f) * 1.1, -.7, .4, colA='#f2bc74', colB='#a8562c', seed=4., speed=1.)
        if f == 36: IM.inkflash(st, '#14040a', '#d8361c', '#ffeec8', lo=.36, hi=.74)
        if f == 37: IM.inkflash(st, '#14040a', '#fff0cc', '#f08a2a', lo=.36, hi=.74)
        return st.finish(bloom=.5, thr=.9, vig=.5, contrast=1.10, satu=1.06, flash=.12 * (f == 38), flashCol='#ffe0a0')

    def leads(self, f, st, T, G, zc, hold, hit):
        ph = on2(int(T)) / 13.; F = ROAR; q = smooth(24, 31, f); up = q * 2.2 + hold * .10 * (f - 30); z0 = -31 + 2.0 * T * .0
        zl = lambda d: 70 - .80 * 30 - d                                   # where the leaders are when the breath is held
        # Hanuman and the hulk are the two who leap
        sw = keys(on2(f), [(22, 0.), (29, .0), (35, .20), (36, .44), (40, .5)])
        tuck = dict(lf=(1.0, 4.6, 1.8), rf=(-.9, 2.4, -2.0), lft=(8, 40), rft=(-6, 74), lkn=(.3, .3, 1), rkn=(-.1, 0, 1))
        P = HM.H_RUN(ph).mix(HM.H_SWING(sw).set(**tuck), q)
        xh = -G * (1 - .30 * q) - .4 if not hit else -4.2
        S = st.fig(HM.HANUMAN, P, at=(xh, up, zl(33)), yaw=lerp(80, 66, q), roll=0, face=HM.VFace(frown=.9, mouth=.5, teeth=.9, spark=.6)); vel = V(34 * (1 - hold * .9), 0, 0)
        HM.tail(st, S, T / 24., 'fly' if q < .5 else 'up', vel=vel, ground=None); HM.sash(st, S, T / 24., vel=vel)
        if q > .05 or f > 12: HM.gada(st, S, scale=1.15)
        P2 = RK.K_RUN(ph + .3).mix(RK.K_RUN(.3).set(**{**tuck, 'rh': (-2.8, 16.2, -1.4), 'rfing': (.2, .5, -.8)}), q); xk = G * (1 - .30 * q) + .4 if not hit else 4.4
        st.fig(RK.HULK, P2, at=(xk, up * .85, zl(34)), yaw=lerp(-80, -64, q), scale=1.08, face=F)
        rows = [(VN.arm(VN.SUGRIVA, 3, T / 20.), VN.V_CHARGE, -1, 44, .2, 72), (VN.arm(VN.ANGADA, 3, T / 22.), VN.V_CHARGE, -1, 62, .6, 70), (VN.arm(VN.LANGUR, 2, T / 22.), VN.V_CHARGE, -1, 25, .45, 78), (VN.arm(VN.YOUTH, 1, T / 22.), VN.V_CHARGE, -1, 50, .85, 74),
                (RK.HORN, RK.K_RUN, 1, 42, .7, -72), (RK.HORN_SPEAR, RK.K_RUN, 1, 60, .1, -70), (RK.SPEARMAN, RK.K_RUN, 1, 25, .5, -78), (RK.TUSK, RK.K_RUN, 1, 50, .35, -74)]
        for g, p, s, d, o, y in rows:
            x = s * (G + (7. if d < 30 else 1.5 + .06 * d)) if not hit else s * (13.5 if d < 30 else 6.5 + .05 * d); st.fig(g, p(ph + o), at=(x, 0, zl(d)), yaw=y, face=F)

    # ---------------------------------------------------------------- along the line
    def camx(self, f):
        K = [(40, X[0] - 12)]
        for i, b in enumerate(BLOWS): K += [(b - 2.5, X[i] - 1.6, 'io' if i else 'out'), (b + 2.5, X[i] + 1.6, 'linear')] if i < 4 else [(b - 2.5, X[i] - 1.2, 'io'), (72, X[i] + .8, 'linear')]
        return keys(f, K, 'io')

    def line(self, f, st):
        t = st.t; cx = self.camx(f); vx = self.camx(f + .5) - self.camx(f - .5); up = ease_io(smooth(70, 80, f), 1.6); i = int(np.argmin([abs(cx - x) for x in X])); tb = f - BLOWS[i]; hitk = decay(tb / 24., 8.) if tb >= 0 else 0.
        zoom = [0, 7.5, 2.5, 3.0, 1.0][i]; lift = [0, 2.2, 1.0, 1.2, 2.0][i]; rl = [-5, 4, -4, 5, -2][i]
        eye = V(cx, 6.2 + 11 * up, 27 + zoom * (1 - up) - 1.6 * hitk * (1 - up) + 8 * up - 15. * smooth(76, 104, f)); at = V(cx + .6 * (1 - up), lerp(8.4 + lift, 34, up), lerp(0, -40, up))
        cam = Cam(eye, at, lerp(38, 48, up), roll=rl * (1 - up) * clamp(1 - abs(vx) * .2)); cam = shaken(cam, f, .55 * hitk * (1 - up), .9); st.cam = cam
        self.sky(st, sunDir=(.02 + .0 * up, .20, -1.), sunR=.14, sunGlow=.42, sunCol='#f08436', cov=.5, cy0=.0, cy1=.22)
        if f > 66: self.storm(st, f, cam)
        L = war_light(key=(-.25, .6, .75), keyCol=(1.0, .72, .45), amb='#7a4a6a', rim=(.15, .4, -.9), rimCol=(2.0, 1.0, .34), fogCol='#d4642c', fog=(.0060, 42., .004, 0.))
        st.open(cam, L)
        ground(st, hills=[(X[4] - 2., -46., 46., 24.)] if up > 0 else ())
        # the press behind: hundreds
        d = np.abs(self.M[:, 0] - cx) < 120 + 60 * up; wob = np.floor((f + self.Mt * 1.7) / 4.) % 2; tile = np.where(self.Mt < 6, (self.Mt + 0 * wob), self.Mt); tile = np.where((self.Mt == 0) | (self.Mt == 1), wob, tile); tile = np.where((self.Mt == 6) | (self.Mt == 7), 6 + wob, tile); P = self.M + np.c_[np.where(self.Mt < 6, 1, -1) * .10 * (f - 56), np.maximum(0, np.sin(f * .9 + self.Mt * 2.1)) * .7, 0 * self.Ms]
        if up > 0: P = P.copy(); q = np.hypot((P[:, 0] - X[4] + 2) / 46, (P[:, 2] + 46) / 17); d &= q > 1.1
        self.fc.draw(P[d], scale=self.Ms[d], tile=tile[d], tint=self.Mc[d])
        fx = []
        if f < 80:
            for k, fn in enumerate((self.v1, self.v2, self.v3, self.v4, self.v5)):
                if abs(X[k] - cx) < 34: fx.append((k, fn(st, f - BLOWS[k], V(X[k], 0, 0))))
        if up > 0: S1, S2 = self.archers(st, f)
        for bx, k, L_ in ((24, 0, 16), (70, 1, 18), (118, 0, 16), (162, 1, 18)):                                  # standards that cross the lens
            if abs(bx - cx) < 22: r_ = V(bx, 15., 14.); st.mesh(*CL.tube(np.array([V(bx, -1, 14), r_]), .22, 8, 4), kind=0, col=('#4a2412', '#1c0a08', '#fff'), cls=1); VH.banner(st, 'rama' if k else 'ravana', r_, t, 10, 5, (-1 if k else 1, 0, -.1), seed=bx)
        st.close()
        footdust(st, 46, ((cx - 34, -.4, -16), (cx + 34, 1.0, 10)), t, size=3.0, rise=3.0, alpha=.42 * (1 - up * .7), seed=3)
        footdust(st, 24, ((cx - 60, 0, -80), (cx + 60, 6, -24)), t, size=9, rise=5.0, alpha=.35 * (1 - up), seed=7)
        for k, at_ in fx: self.impact(st, k, f, at_)
        FX.embers(st, 60, ((cx - 30, 0, -20), (cx + 30, 6, 14)), t, rise=4., size=.10, seed=5, life=2.)
        if up > 0: self.meets(st, f)
        dustbank(st, .55 * (1 - smooth(40, 43, f)) + .25 * (1 - up), .60 - .9 * (1 - smooth(40, 42.5, f)), 1.1, seed=4., speed=.5)
        sp = cam.px(V(cx, 8, 0)) * vx
        if abs(sp) > 110 and f not in BLOWS: whip2(st, -math.copysign(min(620., (abs(sp) - 90) * .42), sp))
        if f == BLOWS[4]: IM.inkflash(st, '#14040a', '#d8361c', '#fff0cc', lo=.24, hi=.52)
        return st.finish(bloom=.5, thr=.9, vig=.5, contrast=1.10, satu=1.06, flash=max(.45 * (1 - smooth(40.5, 42, f)), .03 * (f in BLOWS[:4])), flashCol='#f0b468')

    # five duels.  s = frames from the blow, o = where it stands; each returns the point of the blow
    def v1(self, st, s, o):
        """Hanuman's mace breaks a shield"""
        s2 = s // 2 * 2 if abs(s) > 1 else s; t = st.t; sw = keys(s2, [(-5, 0.), (-2, .06), (0, .5, 'in'), (3, .86, 'out'), (8, 1.)]); S = st.fig(HM.HANUMAN, HM.H_SWING(sw), at=o + V(-6.4, 0, 1), yaw=78, face=HM.VFace(frown=.9, mouth=.6, teeth=.9)); HM.tail(st, S, t, 'whip'); HM.sash(st, S, t, vel=V(14, 0, 0)); HM.gada(st, S, scale=1.15)
        k = ease_out(max(0, s2) / 8., 2.); P = RK.K_GUARD.mix(RK.K_FALL, smooth(-1, 2, s2)); st.fig(RK.HORN.variant(u=dict(shield=0 if s >= 0 else 1)), P, at=o + V(5.6 + 7 * k, 3.6 * math.sin(math.pi * min(1, k)) , 0), yaw=-82, roll=10 * k, face=Face(frown=.4, mouth=.9, teeth=.5) if s >= 0 else ROAR)
        st.fig(RK.SPEARMAN, RK.K_STAB(.1 + .2 * smooth(-4, 4, s2)), at=o + V(13.5, 0, -6.5), yaw=-74, face=ROAR); st.fig(VN.arm(VN.YOUTH, 1, t), VN.V_THROW(keys(s2, [(-3, 0.), (3, .6)])), at=o + V(-14.5, 0, -5), yaw=72, face=ROAR)
        return o + V(3.4, 11.2, 2.6)

    def v2(self, st, s, o):
        """a langur sweeps two away with a whole tree"""
        s2 = s // 2 * 2 if abs(s) > 1 else s; t = st.t; q = keys(s2, [(-6, 0.), (-2, .02), (0, .5, 'in'), (2, .72, 'out'), (8, .9)]); st.fig(VN.arm(VN.LANGUR, 2, t), vswing(q), at=o + V(-7.4, 0, 2.0), yaw=78, scale=1.2, face=ROAR); k = ease_out(max(0, s2) / 9., 1.8)
        for j, (dx, dz, g) in enumerate(((4.2, 1.5, RK.SWORDSMAN), (8.0, -2.5, RK.TUSK))):
            P = RK.K_GUARD.mix(RK.K_FALL, smooth(-1, 2, s2 - j)); st.fig(g, P, at=o + V(dx + 10 * k, (9 - 3 * j) * k * (1.35 - .5 * k), dz), yaw=-70 - 20 * j, roll=26 * k + 16 * j * k, pitch=-14 * k, face=Face(mouth=.9, frown=.3, teeth=.4) if s >= 0 else ROAR)
        st.fig(VN.arm(VN.WARRIOR, 3, t), VN.V_CHARGE(st.f / 13.), at=o + V(-15.5, 0, -6), yaw=72, face=ROAR)
        return o + V(1.6, 9.5, 4.)

    def v3(self, st, s, o):
        """Angada in the air above a spear"""
        s2 = s // 2 * 2 if abs(s) > 1 else s; t = st.t; a = keys(s2, [(-6, (-11., 3.0)), (-2, (-6.8, 5.4), 'out'), (0, (-4.2, 4.2), 'in'), (3, (-3.0, 1.6), 'in'), (8, (-2.4, 0.), 'in')]); q = keys(s2, [(-6, 0.), (-2, .05), (0, .55, 'in'), (3, .95), (8, 1.)]); P = vswing(q).set(lf=(1.2, 3.4, 1.6), rf=(-1.2, 1.6, -2.2), lft=(8, 40), rft=(-10, 60)) if s < 3 else vswing(q)
        st.fig(VN.arm(VN.ANGADA, 3, t), P, at=o + V(a[0], a[1], 1), yaw=76, pitch=8, face=ROAR); k = smooth(0, 6, s2)
        st.fig(RK.SPEARMAN, RK.K_STAB(keys(s2, [(-6, 0.), (-1, .5), (2, .55)])).mix(RK.K_FALL, .85 * smooth(0, 3, s2)), at=o + V(5.2 + 2.4 * k, -1.2 * k, 0), yaw=-80, face=Face(mouth=.9, frown=.3, teeth=.4) if s >= 0 else ROAR); st.fig(RK.HORN, RK.K_RUN(st.f / 14.), at=o + V(14, 0, -6), yaw=-70, face=ROAR)
        st.fig(VN.arm(VN.YOUTH2, 3, t), VN.V_CHARGE(st.f / 13. + .4), at=o + V(-14, 0, -7), yaw=70, face=ROAR)
        return o + V(3.4, 13.6, 2.2)

    def v4(self, st, s, o):
        """Jambavan throws a boulder; it bursts on the hulk's chest"""
        s2 = s // 2 * 2 if abs(s) > 1 else s; thrown = s >= -3; A = VN.V_CARRY; B = VN.V_THROW(.5).set(lh=(1.9, 11.8, 3.6), rh=(-1.9, 11.8, 3.6), pelr=(0, 18, 0), cher=(0, 16, 0), lhand='open', rhand='open'); st.fig(VN.arm(VN.JAMBAVAN, 0 if thrown else 4), A.mix(B, smooth(-5, -2, s2)), at=o + V(-9, 0, 1), yaw=78, scale=1.12, face=ROAR); hit = o + V(4.4, 11.4, 1.4)
        if s >= 0:
            for j in range(8): d_ = np.random.default_rng(j).normal(size=3) * V(1, .8, .5) + V(-.1, .5, .3); a_ = (s + .6) / 24.; boulder(st, hit + d_ * 13 * a_ - V(0, 16 * a_ * a_, 0), .95 - .09 * j, 5 + j, spin=s * .5 + j)
        if thrown and s < 0: p = lerp(o + V(-7.5, 16.5, 1.5), hit, (s + 3) / 3.); boulder(st, p, 2.3, 3, spin=s * .7)
        k = ease_out(max(0, s2) / 9., 2.); st.fig(RK.HULK, RK.K_RUN(st.f / 16.).mix(RK.K_FALL, smooth(-1, 2, s2)), at=o + V(6.6 + 5 * k, 0, 0), yaw=-78, scale=1.15, face=Face(mouth=1., frown=.2, teeth=.3) if s >= 0 else ROAR); st.fig(RK.HORN_SPEAR, RK.K_STAB(.2), at=o + V(16, 0, -6), yaw=-72, face=ROAR); st.fig(VN.arm(VN.LANGUR2, 1), VN.V_THROW(.1), at=o + V(-17, 0, -5), yaw=66, face=ROAR)
        return hit

    def v5(self, st, s, o):
        """Sugriva's club and a sword meet and lock"""
        s2 = s // 2 * 2 if abs(s) > 1 else s; t = st.t; q = keys(s2, [(-6, 0.), (-2, .02), (0, .36, 'in'), (2, .40), (6, .38)]); jit = .05 * math.sin(s2 * 2.3) if s > 0 else 0.; st.fig(VN.arm(VN.SUGRIVA, 3, t), vswing(q), at=o + V(-6.2 + jit, 0, 1.6), yaw=76, scale=1.06, face=ROAR)
        P = RK.K_RUN(.2).set(rh=(-2.2, 15.5, -1.2), rfing=(.2, .6, -.7), lf=(.9, .75, 2.1), rf=(-1.1, .75, -1.7)); Q = RK.K_STAB(.45).set(rh=(-1.4, 13.2, 4.6), rfing=(.1, .75, .6)); st.fig(RK.HORN, P.mix(Q, keys(s2, [(-6, 0.), (-2, .02), (0, 1., 'in'), (6, .96)])), at=o + V(5.6 - jit, 0, 0), yaw=-76, face=ROAR)
        st.fig(RK.SWORDSMAN, RK.K_GUARD, at=o + V(15.5, 0, -6), yaw=-70, face=ROAR); st.fig(VN.arm(VN.WARRIOR2, 3, t), VN.V_CHARGE(st.f / 13.), at=o + V(-16, 0, -6), yaw=72, face=ROAR)
        return o + V(.2, 14.2, 2.8)

    def impact(self, st, k, f, p):
        a = (f - BLOWS[k]) / 24.
        if a < 0: return
        if k == 3:
            FX.burst(st, 46, p, a, speed=26, grav=26, size=.5, seed=4, col='#7a6a5a', kind='ash', life=.9, drag=1.2)
        if k == 1: FX.burst(st, 70, p, a, speed=24, grav=8, size=.34, seed=8, col='#5a8a2a', kind='leaf', life=1.0, drag=1.4)
        leafburst(st, p, a, speed=30 if k != 4 else 22, n=110, size=.22, seed=20 + k, life=.8, spread=(1, 1, .6))
        if k == 4 and f < 80: FX.particles(st, p[None], 2.2 + .5 * math.sin(f * 2.1), '#ffe0a0', 'spark', alpha=.9 * decay(a, 3.)); FX.burst(st, 60, p, (a * 24 % 5) / 24., speed=20, grav=-14, size=.10, seed=f // 5, life=.5, up=.8)
        x, y, _ = st.cam.project(p)
        if a < .3: IM.shock(st, (float(x), float(y)), 40 + 2600 * a, 60, 34 * (1 - a / .3))

    # ---------------------------------------------------------------- under the sun
    def archers(self, st, f):
        t = st.t; b = V(X[4] - 2., 24., -46.); rel = [82, 90]; out = []
        for k, (g, dx, dz, r0) in enumerate(((rama.EXILE, -7.5, 1.5, 82), (rama.LAKSHMANA, 7.5, -1.5, 90))):
            d = keys(f, [(r0 - 14, .0), (r0 - 4, 1., 'io'), (r0, 1.05), (r0 + 2, 1.12, 'out'), (r0 + 9, .95)]); P = PZ.archer(d, .25 * k); P = P.set(lh=(P.lh[0] - .55, P.lh[1] + 2.3, P.lh[2]), rh=(P.rh[0] + .1, P.rh[1] - .25, P.rh[2]), cher=(-20, 0, -9), hedr=(76, 0, 2), lel=(0, -1, -.2))
            S = st.fig(g, P, at=b + V(dx, 0, dz), yaw=14 - 4 * k, face=Face(frown=.5, squint=.3, lid=.9)); PR.bow_and_arrow(st, S, half=5., arrow=f < r0 or f > r0 + 8, release=float(r0 <= f <= r0 + 8)); st.fig(PR.QUIVER, M=PR.place(S.chest((.5, .5, -1.2)), S.d((-.35, 1, -.12)), S.d((0, 0, -1)), 1.))
            for j, (an, ln, wd, col) in enumerate(((lambda tt: S.chest((-1.2, 1.2, -.8)), 9., 1.3, ('#c8431f', '#4a1020', '#f2c24a')), (lambda tt: S.pelvis((-.6, .5, -.9)), 6.5, 1., ('#e8a22c', '#7a3a14', '#b3202a')))):
                Q = CL.lag(an, t, n=16, length=ln, wind=(-.95, .16 + .08 * j, -.1), grav=.10, wave=1.0, phase=j * 2 + k); st.mesh(*CL.strip(Q, np.linspace(wd * .6, wd, 16), up=(0, 1, .3), m=6, curl=.12, n=36), kind=1, col=col, cls=8)
            out.append(S)
        for j, (bx, bz, h, l) in enumerate(((-21, -3, 23, 15), (19, -4, 26, 16), (-13, -8, 28, 14))):
            r_ = b + V(bx, h, bz); st.mesh(*CL.tube(np.array([b + V(bx, -8, bz), r_]), .26, 8, 4), kind=0, col=('#6a3416', '#2c120a', '#fff'), cls=1); VH.banner(st, 'rama', r_ - V(0, .4, 0), t + j, l, 6.5, (-1, .06, -.15), seed=j * 2.)
        self.rel = [(82, out[0]), (90, out[1])]; return out

    def storm(self, st, f, cam):
        T = (f - 72) / 24.; g = 50.; cx = X[4]
        for side, (p0, v, t0, lit) in zip((0, 1), self.A):
            a = T - t0; m = (a > 0) & (a < 3.2); p = p0[m] + V(cx, 0, 0) + v[m] * a[m][:, None] - V(0, .5 * g, 0) * (a[m] ** 2)[:, None]; vv = v[m] - V(0, g, 0) * a[m][:, None]; l = lit[m]; k = p[:, 1] > 14; p, vv, l = p[k], vv[k], l[k]
            if not len(p): continue
            d = vv / np.linalg.norm(vv, axis=1, keepdims=True); A, B = cam.project(p - d * 4.2), cam.project(p + d * 1.2); ok = (A[:, 2] > 8) & (B[:, 2] > 8); o = np.argsort(-B[ok, 2]); w = np.clip(cam.fl * 540 / B[ok, 2] * .14, 1., 4.5)[o]
            col = (.10, .03, .05) if side == 0 else (.05, .02, .03)
            st.vector(lambda c: arrow_lines(c, A[ok][o][:, :2], B[ok][o][:, :2], w, col, head=(.95, .75, .42), fletch=((.96, .85, .6) if side == 0 else (.6, .1, .1))))
            if l.any():
                q, dd, vv2 = p[l] + d[l] * 1.0, d[l], vv[l]; FX.particles(st, q - dd * 2.4, .42, '#ff8a2c', 'streak', vel=dd * 7.0, alpha=.85); FX.particles(st, q, 1.15, '#ffb050', 'ember', alpha=.9); FX.particles(st, q + V(0, .5, 0), 1.0, (.9, .7, .5), 'tongue', seed=np.arange(len(q)) * .618 % 1, rot=.0)

    def meets(self, st, f):
        # a few that pass close to the lens
        r = np.random.default_rng(12); A, B, wd = [], [], []
        for k in range(13):
            s_ = -1 if k % 2 else 1; f0 = 72 + 1.9 * k; q = (f - f0) / 5.; z = r.uniform(-14, 4); y = r.uniform(27, 44); x = X[4] - s_ * 46 + s_ * 92 * q
            if -.1 < q < 1.1: p = V(x, y + 14 * q * (1 - q), z); d = nz(V(s_, .16 * (1 - 2 * q), 0)); a, b = st.cam.project(p - d * 5), st.cam.project(p); A.append(a[:2]); B.append(b[:2]); wd.append(float(np.clip(st.cam.px(p) * .16, 2, 9)))
        if A: st.vector(lambda c: arrow_lines(c, A, B, np.array(wd), (.08, .025, .04), head=(.95, .78, .45), fletch=(.94, .84, .62)))
        for r0, S in (self.rel if f >= 72 else ()):
            a = f - r0
            if 0 <= a < 5: g_ = S.palm('L', 0, .62, .30); dr = nz(g_ - S.palm('R', .22, .95, .34) + V(0, .6, 0)) if a < 1 else nz(V(.94, .34, -.1)); FX.ribbon(st, np.array([g_ + dr * (a * 26 - 8 if a else 0), g_ + dr * (30 + a * 46)]), [.2, 1.1], 'light', '#ff9a3a', '#fff6dc', amt=1 - a / 5.); FX.particles(st, g_[None], 3.2 - .5 * a, '#fff0c8', 'spark', alpha=1 - a / 5.)
        for k, (mf, p) in enumerate(self.meet):
            a = (f - mf) / 24.
            if 0 <= a < .6: FX.particles(st, p[None], 7.5 * (1 - a * 1.2), '#fff0c8', 'spark', alpha=1 - a / .6); FX.burst(st, 36, p, a, speed=22, grav=14, size=.26, seed=40 + k, life=.6); FX.burst(st, 20, p, a, speed=12, grav=12, size=.24, seed=60 + k, col='#ffcf6a', kind='flake', life=.8)
