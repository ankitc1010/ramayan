"""c3 (48): the line.  Extreme low: an arrow point ploughs a furrow in the red earth, feet stepping back with it, the hut behind (f0-17).  f18: the line takes fire and runs both ways round the hut, lighting Sita in the doorway.
f30: Lakshmana looks at her, at the forest; f36 he turns and runs out past the lens.  Hold on Sita inside the ring of fire, small."""
from shots.forest_kit import *

CTR, R0 = V(0, 0, 4.), 24.                                  # the ring of worlds/hut.glsl
SKY3 = SKY(DUSK, cHor='#e8703a', cMid='#7a2c4a', cov=.5, sunR=0., sunDir=(-.7, .12, -1.))
LIGHT3 = dict(key=(-.75, .32, .40), keyCol=(.62, .30, .20), amb='#3c3472', rim=(.5, .4, -.8), rimCol=(.0, .0, .0), bounceCol=(.12, .05, .03), envT='#9a6a80', envM='#ff8a4a', envB='#3a1c34', fogCol='#5a2c48', fog=(.0026, 70., .006, 0.), inkRef=1.2)


def light3(**k): return Light(**{**LIGHT3, **k})


def place3(st):
    """worlds/forest.clearing at dusk, with red earth, and no grass between the lens and the line"""
    FO.place.draw(st, 'hut.glsl', u=dict(fireK=0., tone=0., line=0., lineR=R0, gA='#b4562f', gB='#5e2626', leafA='#b0823c', leafB='#4a3430', rockA='#8a5264', rockB='#3c2446'), sun=1.)
    r = np.random.default_rng(3); k = dict(hazeCol='#3a2450', wind=.5)
    def put(kind, n, r0, r1, a0, a1, hh, haze, sd, tint=(.42, .42, .56)):
        a = np.linspace(a0, a1, n) + r.uniform(-.06, .06, n); R = r.uniform(r0, r1, n); P = np.c_[np.sin(a) * R, np.zeros(n) - .3, np.cos(a) * R]; P = P[~((P[:, 2] > 12) & (np.abs(P[:, 0]) < 40))]; FL.scatter(st, kind, P, hh, season='summer', seed=sd, haze=haze, tint=tint, **k)
    put('pahari_round', 16, 150, 230, 1.6, 4.7, 74, .55, 1); put('mango', 12, 100, 150, 1.7, 4.6, 62, .34, 2); put('palm', 7, 96, 150, 1.9, 4.4, 74, .30, 3); put('plantain', 5, 44, 60, 1.7, 2.3, 24, .06, 4); put('plantain', 4, 44, 60, 4.0, 4.6, 26, .06, 5); put('banyan', 1, 76, 80, 4.28, 4.3, 78, .10, 6); put('ashoka', 2, 66, 80, 1.75, 2.0, 50, .10, 7); put('bamboo', 4, 66, 90, 1.5, 2.1, 56, .14, 8); put('shrub', 22, 56, 110, 1.3, 5.0, 10, .10, 9); put('grass', 34, 44, 90, .9, 5.4, 6, .06, 10); put('fern', 14, 46, 80, 1.2, 5.1, 8, .06, 11)


def ring(a, y=.12, r=R0): a = np.asarray(a, float); rr = r + .22 * np.sin(a * 23) + .14 * np.sin(a * 61 + 1); return np.stack([CTR[0] + np.sin(a) * rr, np.full_like(a, y), CTR[2] + np.cos(a) * rr], -1)


A0, AV = -.80, .0185                                        # where the tip is at f0, radians a frame


def tip_a(f): return A0 + AV * f


AC = tip_a(17)                                             # where the fire starts


class Shot(ShotBase):
    id = 'c3'; n = 48
    EVENTS = [(0, 'arrow scratches earth', dict(dur=18)), (0, 'step back', {}), (6, 'step back', {}), (12, 'step back', {}), (18, 'line takes fire', {}), (19, 'fire runs', dict(dur=12)), (30, 'ring of fire', dict(dur=18)), (30, 'he looks at her', {}), (33, 'far cry', dict(soft=1)), (36, 'he turns and runs', {}), (38, 'run footstep', {}), (41, 'run footstep', {})]

    # -------------------------------------------------------------- the furrow
    def furrow(self, st, a0, a1, hot=0.):
        a = np.linspace(a0, a1, max(8, int(abs(a1 - a0) * 90))); rad = np.stack([np.sin(a), 0 * a, np.cos(a)], 1)
        j = .10 * np.sin(a * 190) + .07 * np.sin(a * 331 + 2)
        for s, w, y, col in ((0, .62, .17, ('#2a0c0c', '#140608', '#2a0c0c')), (1, .40, .30, ('#d87a4a', '#6a2a22', '#d87a4a')), (-1, .40, .28, ('#a84c30', '#4a1c1c', '#a84c30'))):
            P = ring(a, y) + rad * (s * (.50 + j))[:, None]; m = CL.strip(P, w * (1 + (j if s else 0 * j) * 2), up=rad, m=5, curl=-.35 if s else .0); m = (m[0], np.tile(V(0, 1, 0) + 0., (len(m[0]), 1)) + (rad.repeat(5, 0) * .4 * s), m[2], m[3]); st.mesh(*m, kind=0, col=col, cls=1, ink=.5 if s else .2, part=20. + s)

    def lak_back(self, f):
        """walking backward along the line, bent, the arrow point down: pose, at, yaw, tip"""
        a = tip_a(f); tip = ring(np.array([a]), .22)[0]; b = a + .262; at = ring(np.array([b]), 0., R0 + 1.9)[0]; tang = V(math.cos(b), 0, -math.sin(b)); yaw = math.degrees(math.atan2(-tang[0], -tang[2]))
        ph = -f / 12. * 1.0; D = AV * R0 * 12; P = stride_pose(ph, dist=D, duty=.62, pel=6.55, drop=.12, yaw=5, lean=20, hip=.95, lift=.9)
        M = np.linalg.inv(np.block([[eul(yaw, 0, 0), at[:, None]], [np.zeros((1, 3)), np.ones((1, 1))]])); q = lambda w: tuple((M @ np.append(w, 1))[:3])
        shaft = nz(V(0, 1, 0) * 1.35 + tang * 1.0 + V(0, 0, .12)); hand = tip + shaft * 5.0; sway = .05 * math.sin(f * 1.9)
        P = P.set(cher=(P.cher[0] * .3 + 8, 34, 0), hedr=(0, -6, 0), rh=tuple(np.array(q(hand)) + V(-.15, -.35 + sway, -.2)), rhand='grip', rfing=(.3, -.5, .8), rpalm=(.9, 0, -.3), rel=(-.9, .2, -.5), lh=(2.2, 5.6, 1.8), lel=(1, .2, -.6), lhand='relax')
        return P, at, yaw, tip, shaft

    def scratch(self, f, st, t):
        a = tip_a(f); P, at, yaw, tip, shaft = self.lak_back(f); u = f / 17.; sx, sy = shake(f, .035, .7, 4)
        c0 = ring(np.array([lerp(tip_a(0), tip_a(17), .12 + .80 * u)]), 0.)[0]; cam = Cam(c0 + V(-.9 + 1.0 * u + sx, 1.05 + .25 * u + sy, 9.9 - .5 * u), c0 + V(1.9, 2.75 + .25 * u, -2.), 45, roll=lerp(-4, 0, u)); st.cam = cam
        st.paint('sky.frag', **SKY3); L = light3(inkRef=.8, pts=[(tuple(tip + V(-.3, .5, .3)), 1.6, tuple(np.array([.55, .26, .08]) * smooth(6, 17, f)))]); st.open(cam, L); place3(st)
        self.furrow(st, a - 1.3, a)
        S = st.fig(rama.LAKSHMANA, P, at=at, yaw=yaw, face=Face(frown=.4, smile=-.1)); quiver(st, S); h = S.palm('R', 0, .6, .25); d = nz(tip - h); Ln = float(np.linalg.norm(tip - h)) + .02; st.fig(PR.arrow_of(Ln + 1.2, 1.35), M=PR.place(h - d * 1.2, V(0, .3, 1) - d * (V(0, .3, 1) @ d), d, 1.))
        st.fig(sita.FOREST, sita.S_STAND.set(hedr=(0, 4, 0)), at=(-1.2, 0, 18.6), yaw=6, face=Face(sad=.3, smile=-.05))
        solve = lambda tt: (lambda q: st.fig(rama.LAKSHMANA, q[0], at=q[1], yaw=q[2], draw=False))(self.lak_back(tt * 24)); sashes(st, solve, t, 'lak', wind=(-.45, -.35, .15), wave=.5, grav=.8, k=.9)
        st.close()
        # earth thrown by the point
        for k in range(6):
            f0 = f - k; tp = ring(np.array([tip_a(f0)]), .25)[0]
            if f0 >= -4: FX.burst(st, 16, tp, k / 24., speed=4.6, grav=15, size=.10, seed=f0 + 40, col='#8a3a22', kind='ash', life=.42, up=1.0, spread=(1, .7, .9)); FX.burst(st, 7, tp, k / 24., speed=5.2, grav=15, size=.07, seed=f0 + 80, col='#d8804e', kind='dot', life=.40, up=1.1)
        Q = np.array([tip + V(-1.2 * q, .3 + 1.3 * q + .2 * math.sin(q * 5 - t * 6), .2) for q in np.linspace(0, 2.2, 14)]); FX.ribbon(st, Q, np.linspace(.15, .9, 14), 'smoke', '#c87a50', '#6a2e22', seed=2, amt=.30)
        if f >= 8: FX.particles(st, tip[None] + V(0, .1, 0), .25 + .3 * smooth(8, 17, f) * (1 + .3 * math.sin(f * 2.3)), '#ffb050', 'glint', alpha=smooth(8, 14, f)); FX.embers(st, int(16 * smooth(8, 17, f)) + 1, (tuple(tip - V(.3, .1, .3)), tuple(tip + V(.2, .1, .3))), t, rise=2.2, size=.05, seed=3, life=.8)
        FL.frame(st, 'fg_grass', 60, 1170, .55, 'autumn', 0, lod=3., tint=(.5, .4, .45)); FL.frame(st, 'fg_grass', 2060, 1190, .5, 'autumn', 1, lod=3., tint=(.5, .4, .45))
        IM.dof(st, float((tip - cam.eye) @ cam.R[2]), 9., 6.)
        return st.finish(bloom=.42, thr=.9, vig=.5, contrast=1.08, fade=.5 * (1 - smooth(0, 4, f)), fadeCol='#080a14')

    # -------------------------------------------------------------- the fire
    def prog(self, f): return .012 + ease_io(clamp((f - 18) / 12.5), 1.35) * math.pi

    def lights(self, f, t, k=1.):
        u = self.prog(f); fl = 1 + .08 * noise1(t * 8, 3); n = 9; a = np.linspace(max(-1.5, AC - u), min(1.35, AC + u), n); P = ring(a, 2.2)
        amt = min(1., u / 1.0) * .34 + .22; pts = [(tuple(p), 5.5, tuple(np.array([1.5, .62, .16]) * amt * fl)) for p in P]
        pts.append(((0., 4., 22.), 12., tuple(np.array([1.0, .46, .16]) * .75 * smooth(.3, 1.6, u) * fl))); return light3(pts=pts, keyCol=tuple(np.array([.62, .30, .20]) * (1 - .55 * k * smooth(18, 34, f))), amb=tuple(np.array(hexc('#3c3472')) * (1 - .40 * k * smooth(18, 34, f))))

    def fire(self, f, st, t, big=1.):
        """after close: the burning line, front at +-u"""
        u = self.prog(f); r = np.random.default_rng(7); n = 520; a = r.uniform(-math.pi, math.pi, n); on = np.abs(a) < u; age = np.clip((u - np.abs(a)) / .25, 0, 1); near = np.exp(-((u - np.abs(a)) / .22) ** 2) * (u < 3.0)
        s = (1.0 + 1.3 * r.uniform(0, 1, n)) * (.35 + .65 * age + .9 * near) * (1 + .16 * np.sin(t * 9 + a * 40)) * big; P = ring(AC + a, 0.); P[:, 1] = s * .80 - .05; o = np.argsort(((P - st.cam.eye) ** 2).sum(1))[::-1]; o = o[on[o]]
        FX.particles(st, P[o], s[o], (1, .95, .9), 'tongue', seed=r.uniform(0, 1, n)[o])
        for sg in (1, -1):
            q = np.linspace(0, u, 60) * sg; FX.ribbon(st, ring(AC + q, .25), .22, 'light', '#ff7a20', '#fff0c0', amt=.9)
            if u < 3.05:
                h = ring(np.array([AC + u * sg]), 1.)[0]; FX.particles(st, h[None], 3.4, '#ffc060', 'lamp'); FX.burst(st, 40, h, ((f % 3) + 1) / 24., speed=11, grav=8, size=.11, seed=f * 2 + sg, col='#ffc060', life=.4, up=.8)
                trail = ring(AC + np.linspace(max(0, u - .55), u, 30) * sg, 1.1); FX.ribbon(st, trail + V(0, 1, 0) * np.linspace(0, .5, 30)[:, None], np.linspace(.1, 1.25, 30), 'fire', (1, .9, .8), seed=sg, amt=.8)
        m = 120; ae = AC + r.uniform(-u, u, m); lf = (t * .8 * r.uniform(.6, 1.3, m) + r.uniform(0, 1, m)) % 1.; Pe = ring(ae, .6); Pe[:, 1] += lf * 9; Pe[:, 0] += .9 * np.sin(lf * 7 + ae * 9); FX.particles(st, Pe, .13 * (1 - lf) ** .5, '#ffa040', 'ember', alpha=np.minimum(1, lf * 8) * (1 - lf))

    def sita_door(self, st, f, t):
        k = smooth(19, 25, f); br = .04 * math.sin(t * 2.4); P = sita.S_STAND.mix(sita.S_HEART, keys(on2(f), [(18, 0.), (24, 1.03, 'io'), (28, 1.)])).set(hedr=(keys(on2(f), [(18, 0), (22, -10, 'io'), (28, 4, 'io'), (34, 10), (40, 6), (48, 6)]), lerp(6, 2, k), 3))
        return st.fig(sita.FOREST, P.set(pel=(P.pel[0], P.pel[1] + br, P.pel[2])), at=(0, 0, 18.4), yaw=4, face=Face(lid=1., sad=.45, smile=-.1, brow=.2, spark=.8 * round(k, 1)))

    def lak_heat(self, f):
        """the fire wakes: an arm goes up against the heat, he gives back one step, turns to the hut; feet stay where they stand until they step"""
        g = on2(f); P0, at0, yaw0, _, _ = self.lak_back(17); out = nz((at0 - CTR) * V(1, 0, 1)); back = out * 3.6; tw = lambda a, b: ease_io(clamp((f - a) / (b - a)), 1.8)
        k = clamp(keys(g, [(18, 0.), (20, -.05), (25, 1.04, 'io'), (28, 1.)])); yaw1 = math.degrees(math.atan2(-out[0], -out[2])); y0 = yaw0 + 360 * round((yaw1 - yaw0) / 360); yaw = lerp(y0, yaw1, clamp(k)); at = at0 + back * tw(19, 26)
        shield = keys(g, [(18, 0.), (21, 1.05, 'out'), (25, 1.), (29, .25, 'io')]); R = eul(yaw, 0, 0)
        def foot(p0, p1, a, b): u = tw(a, b); return p0 + (p1 - p0) * u + V(0, 1.1 * math.sin(math.pi * u), 0)
        w0 = lambda q: at0 + eul(yaw0, 0, 0) @ np.asarray(q, float); w1 = lambda q: at0 + back + eul(yaw1, 0, 0) @ np.asarray(q, float)
        lf, rf = foot(w0(P0.lf), w1((.9, .75, .5)), 21, 26), foot(w0(P0.rf), w1((-.9, .75, -.6)), 18, 22); inv = lambda q: tuple(R.T @ (q - at))
        E = PZ.STAND.set(pel=(0, 8.0, 0), lh=(2.3, 8.2, 1.5), lhand='grip', lfing=(-.2, .1, 1), lpalm=(-1, 0, 0), rh=(-2.2, 7.8, 1.0), hedr=(0, 2, 0)); P = P0.mix(E, clamp(k))
        P = P.mix(P.set(rh=(-.9, 13.6, 2.4), rel=(-1, -.2, .2), rhand='open', rfing=(.6, .8, .1), rpalm=(0, 0, 1), cher=(P.cher[0] - 10, P.cher[1] - 8, 0)), clamp(shield)).set(lf=inv(lf), rf=inv(rf), lft=(8, 0), rft=(-8, 0)); return None, (P, at, yaw)

    def runs(self, f, st, t):
        e = ease_io(clamp((f - 18) / 12.), 1.7); sx, sy = shake(f, .25 * decay((f - 18) / 24., 6.), 1., 4); start = ring(np.array([tip_a(17)]), 0.)[0]
        cam = Cam(lerp(start + V(4.5, 1.5, 12.5), V(5., 15.5, 82), e) + V(sx, sy, 0), lerp(start + V(1.5, 4.2, -6), V(0, 9.5, 2), e), lerp(46, 38, e), roll=lerp(4, 0, e)); st.cam = cam
        st.paint('sky.frag', **SKY3); L = self.lights(f, t); st.open(cam, L); place3(st); u = self.prog(f); self.furrow(st, AC - max(1.2, min(u, math.pi)), AC + max(.05, min(u, math.pi)))
        self.sita_door(st, f, t)
        # he straightens up and steps back from the heat
        S, sol = self.lak_heat(f); P, at, yaw = sol; S = st.fig(rama.LAKSHMANA, P, at=at, yaw=yaw, face=Face(frown=.4)); quiver(st, S); held_bow(st, S, 'L', up=S.d((.05, 1, .05)), fwd=S.d((0, 0, 1)), half=4.3) if f >= 22 else None
        if f < 22: h = S.palm('R', 0, .6, .25); d = nz(S.d((.1, -.75, .6))); st.fig(PR.arrow_of(6.2, 1.35), M=PR.place(h - d * 1.2, S.d((1, 0, 0)), d, 1.))
        solve = lambda tt: (lambda q: st.fig(rama.LAKSHMANA, q[0], at=q[1], yaw=q[2], draw=False))(self.lak_heat(max(18., tt * 24))[1]); sashes(st, solve, t, 'lak', wind=(-.30, .12, .62), wave=.8, grav=.5, k=.95)
        st.close(); self.fire(f, st, t, 1.0)
        if f < 22: IM.zoomblur(st, tuple(cam.project(start)[:2]), .03 * (1 - (f - 18) / 4.))
        FL.frame(st, 'fg_grass', 160, 1120 + 60 * e, .62, 'autumn', 0, lod=2.6, tint=(.35, .22, .28)); FL.frame(st, 'fg_grass', 1800, 1120 + 60 * e, .66, 'autumn', 1, lod=2.6, tint=(.35, .22, .28)); FL.frame(st, 'fg_leaves', -120, -150, .50, 'autumn', 0, lod=2.6, tint=(.3, .22, .3))
        return st.finish(bloom=.55, thr=.88, vig=.5, contrast=1.08, flash=.07 if f == 18 else 0., flashCol='#ffc070')

    # -------------------------------------------------------------- he goes
    def goes(self, f, st, t):
        pull = ease_io(clamp((f - 37.5) / 10.5), 1.6); u = (f - 30) / 17.
        cam = Cam(lerp(V(3.6, 9.8 - .1 * u, 69 - 2.4 * u), V(1.5, 15.0, 92), pull), lerp(V(1.4, 10.0, 8), V(0, 9.4, 2), pull), lerp(34, 33, pull)); st.cam = cam; st.paint('sky.frag', **SKY3); L = self.lights(f, t)
        at0 = V(-1.6, 0, 46.5); P, at, yaw, face, seen = self.lak_goes(f, at0)
        L.pts = L.pts[:8] + [(tuple(V(at[0] + .5, 9., at[2] - 5.)), 5., (1.2, .5, .14))] + L.pts[-1:]
        st.open(cam, L); place3(st); self.furrow(st, -math.pi, math.pi); self.sita_door(st, f, t); st.close(); self.fire(f, st, t, 1.0)
        if seen:
            L2 = light3(keyCol=(.46, .25, .20), amb='#2c2656', key=(.70, .22, .40), rim=(.25, .30, -.9), rimCol=(2.2, .85, .22), pts=[(tuple(V(at[0] + 4.5, 10.5, at[2] + .5)), 5., (.85, .36, .10))], ink=3.6)
            st.open(cam, L2); S = st.fig(rama.LAKSHMANA, P, at=at, yaw=yaw, face=face); quiver(st, S); held_bow(st, S, 'L', up=S.d((.08, 1, .10)), fwd=S.d((.1, -.1, 1)))
            solve = lambda tt: (lambda q: st.fig(rama.LAKSHMANA, q[0], at=q[1], yaw=q[2], draw=False))(self.lak_goes(max(30., tt * 24), at0)); sashes(st, solve, t, 'lak', wind=(.30, -.10, -.75 if f > 36 else -.25), wave=.6, grav=.6, k=.95); st.close()
        if f == 40: IM.zoomblur(st, (760, 500), .07)
        for f0, p in ((38, V(1.4, .2, 52.)), (41, V(4., .2, 64.))): FX.burst(st, 24, p, (f - f0) / 24., speed=6, grav=9, size=.32, seed=f0, col='#8a4430', kind='ash', life=.5, up=.7)
        FL.frame(st, 'fg_grass', 160, 1180, .62, 'autumn', 0, lod=2.6, tint=(.35, .22, .28)); FL.frame(st, 'fg_grass', 1800, 1180, .66, 'autumn', 1, lod=2.6, tint=(.35, .22, .28)); FL.frame(st, 'fg_leaves', -120, -150, .50, 'autumn', 0, lod=2.6, tint=(.3, .22, .3)); FL.frame(st, 'fg_leaves', 2040, -170, .46, 'autumn', 1, lod=2.6, tint=(.3, .22, .3), flip=True)
        return st.finish(bloom=.55, thr=.88, vig=.52, contrast=1.08)

    def lak_goes(self, f, at0):
        g = on2(f) if f < 37 else f; B = PZ.CONTRA.set(lh=(1.95, 8.6, 1.5), lhand='grip', lfing=(-.2, .1, 1), lpalm=(-1, 0, 0), rh=(-1.9, 8.4, 1.2), rhand='relax', lel=(.8, -.4, -.8))
        if f < 37:
            k = keys(g, [(30, 1.), (32, 1.), (36, -.02, 'io'), (37, 0.)]); w = keys(g, [(34, 0.), (36, 1., 'io')])
            P = B.set(pelr=(lerp(4, 16, k), 0, 3), cher=(lerp(0, 30, k), 3 * k, -4 - 3 * k), hedr=(lerp(-16, 50, k), lerp(-3, 4, k), 3 * k), rh=tuple(lerp(V(-1.9, 8.4, 1.2), V(-1.2, 9.6, 2.0), k)), pel=(.25, 8.2 - .8 * w, .1 - .5 * w)); face = Face(frown=.25, sad=.5, lid=.95, gx=.3, smile=-.25) if f < 33 else Face(frown=.45, sad=.35, lid=1., gx=-.35, smile=-.3, brow=.1)
            return P, at0, 12., face, True
        s = f - 37; ph = .0 + s / 8.; d = 1.6 * s + .95 * s * s; dirn = nz(V(2.4, 0, 22)); P = run_pose(ph, dist=24, lean=26).set(lh=(1.7, 9.0, 2.2), lhand='grip', lfing=(-.3, .2, .9), lpalm=(-.9, 0, -.2), lel=(.8, -.6, -.4)); P = B.mix(P, smooth(37, 39, f)); at = at0 + dirn * d
        return P, at, math.degrees(math.atan2(dirn[0], dirn[2])), Face(frown=.5, lid=.95, smile=-.2), at[2] < 67

    def frame(self, f, st):
        st.clear('#000', f=f); t = st.t
        return self.scratch(f, st, t) if f < 18 else self.runs(f, st, t) if f < 30 else self.goes(f, st, t)
