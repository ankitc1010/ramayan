"""b2 (72): the crown is set down (thunk f12); bare feet turn and go; three silhouettes walk out through the great gate into a red dusk and behind them the lamps go out one by one (f36-66)."""
from lau.shot import *
from lau.look import *
from chars import rama, sita, people as PE
from chars.armonly import ARM, place_hand
from worlds import palace as PL


class Shot(ShotBase):
    id = 'b2'; n = 72
    EVENTS = [(12, 'crown set down', {}), (20, 'bare foot on stone', {}), (23, 'bare foot on stone', {}), (28, 'wind in the hall', dict(dur=44))] + [(36 + int(i * 1.7), 'lamp goes out', dict(k=i)) for i in range(18)] + [(30, 'bare foot on stone', dict(soft=1)), (38, 'bare foot on stone', dict(soft=1)), (46, 'bare foot on stone', dict(soft=1)), (54, 'bare foot on stone', dict(soft=1))]

    def setup(self, st):
        I = []
        for k, (m, p, y) in enumerate(((PE.CITIZEN_M[0], PE.P_BOW, 70), (PE.CITIZEN_M[1], PE.P_NAMASTE, 75), (PE.CITIZEN_F[0], PE.F_NAMASTE, 75), (PE.CITIZEN_F[1], PE.F_WAVE, 70), (PE.CITIZEN_M[2], PE.P_BOW, 80), (PE.CITIZEN_F[2], PE.F_NAMASTE, 65))): I.append((m, p, Face(sad=.8, lid=.6, smile=-.4), y))
        self.cr = Crowd(st, I, px=300, pitch=3.); r = np.random.default_rng(4); P, T, F = [], [], []
        for z in np.arange(-70, -400, -7.5):
            for s in (-1, 1):
                for k in range(2): P.append((s * (42 + 7 * k + r.uniform(-2, 2)), 0, z + r.uniform(-3, 3))); T.append(r.integers(0, 6)); F.append(1. if s < 0 else -1.)
        self.P, self.T, self.F = np.array(P), np.array(T), np.array(F)

    def frame(self, f, st):
        st.clear('#000', f=f); t = st.t
        return self.crown(f, st, t) if f < 25 else self.gate(f, st, t)

    def crown(self, f, st, t):
        g = on2(f); u = f / 24.; cam = Cam(V(-2.6 + .6 * u, 1.55, 9.2 - .5 * u), V(.9 + .2 * u, 2.1, 0), 33, roll=-2); st.cam = cam; st.paint('sky.frag', **PL.sky('ayodhya'))
        cy = keys(g, [(0, 2.9), (10, .45, 'io'), (12, .16, 'in'), (13, .22), (14, .16)]); hit = impulse((f - 12) / 24., 14)
        L = PL.light('ayodhya', at=(0, 8, -20), gain=.16, keyCol=(.30, .13, .07), shadow=True); L.inkRef = .6; L.ink = 3.4; L.pts = L.pts[:4] + [(V(-3.5, 4.5, 5.5), 4.5, (.42, .24, .11))]; L.hi = .25
        st.open(cam, L); PL.draw(st, 'ayodhya', lamps=18., dusk=1.)
        c = V(.2, cy, 2.2); st.fig(PR.CROWN, M=PR.place(c, (0, 1, 0), (.25, 0, 1), 1.12))
        # his feet and legs behind it: he stands, turns, goes
        turn = keys(g, [(0, 12.), (14, 12.), (19, 150., 'io'), (24, 176.)]); go = max(0., (g - 18) / 24.) * 8.; ph = .25 + max(0, (g - 18)) / 24. * 1.15
        P = PZ.STAND if g < 18 else PZ.walk(ph, stride=1.6)
        st.fig(rama.EXILE, P, at=(1.9, 0, -1.6 - go), yaw=turn)
        if g < 20:
            wd = keys(g, [(0, 0.), (13, 0.), (20, 5.5, 'in')]); Ph = PZ.STAND.set(rh=(-2.6, 7.2, .9), rel=(-1, -.2, -.6), rhand='hold', rpalm=(1, 0, .1), lh=(2.6, 7.2, .9), lel=(1, -.2, -.6), lhand='hold', lpalm=(-1, 0, .1))
            for sd, sg in (('R', -1), ('L', 1)):
                A = ARM.variant(u=dict(side=1 if sd == 'R' else 0, band=0, fore=0.)); S = st.fig(A, Ph, draw=False)
                st.fig(A, Ph, M=place_hand(S, sd, c + V((1.22 + .35 * min(wd, 1)) * sg, .10 + wd, -.15 - wd * .6), (-.22 * sg, -.95, .16), (-1 * sg, -.20, .10), 1.0), u=dict(side=1 if sd == 'R' else 0))
        st.close(); PL.flames(st, 'ayodhya', lamps=18.)
        if 12 <= f < 24: FX.burst(st, 22, (.2, .05, 2.2), (f - 12) / 24., speed=3.2, grav=2.5, size=.05, seed=2, col='#c8906a', kind='ash', life=.6, spread=(1.4, .25, 1.0), up=.15)
        IM.dof(st, float((c - cam.eye) @ cam.R[2]), 7., 8.); sx, sy = shake(f, 7 * hit, .9, 2); IM.whip(st, sx, sy)
        return st.finish(bloom=.35, thr=1.0, vig=.5, contrast=1.06, expo=.92)

    def gate(self, f, st, t):
        u = (f - 25) / 46.; lamps = keys(f, [(35, 18.), (66, 0., 'linear')]); cam = Cam(V(0, 5.4 + .5 * u, 34 - 8 * u), V(0, 27 - 1.0 * u, -430), 23); st.cam = cam; gl_ = lamps / 18.
        st.paint('sky.frag', **PL.sky('ayodhya')); L = PL.light('ayodhya', at=(0, 8, -150), lamps=lamps, order='far', gain=.45, keyCol=(.42, .16, .08), amb=tuple(np.array(hexc('#4a2436')) * (.22 + .50 * gl_))); L.ink = 2.8; L.hi = .2
        st.open(cam, L); PL.draw(st, 'ayodhya', lamps=float(lamps), dusk=1., order='far')
        st.fig(PR.CROWN, M=PR.place(V(-4.6, .16, 8.0), (0, 1, 0), (.25, 0, 1), 1.12))
        ph = (f - 25) / 18.; d = (f - 25) / 24. * 7.6; z0 = -96.
        sw = lambda a, x, z, dx: (x, 0, z0 + z - d)
        st.fig(rama.EXILE, PZ.walk(ph, stride=1.7), at=sw(0, 0, 0, 0), yaw=180); st.fig(sita.FOREST, sita.S_WALK(ph + .5), at=sw(1, 5.4, 2.5, 0), yaw=180); st.fig(rama.LAKSHMANA, PZ.walk(ph + .25, stride=1.7), at=sw(2, -5.6, 4.5, 0), yaw=180)
        lean = .05 * np.sin(t * 2 + self.P[:, 2] * .3); self.cr.draw(self.P, scale=1., tile=self.T, flip=self.F, lean=lean, tint=.75)
        st.close(); PL.flames(st, 'ayodhya', lamps=float(lamps), order='far')
        # a thread of smoke from every lamp that has just gone out
        Q = PL.flame_points('ayodhya', 'far'); tin = [35 + 31 * (18 - i) / 18. for i in range(len(Q))]
        for i, q in enumerate(Q):
            j = len(Q) - 1 - i; a = (f - (35 + 31. * (j + .5) / 18.)) / 24.; q = Q[len(Q) - 1 - j]
            if 0 < a < 1.1: FX.ribbon(st, np.array([q + V(.8 * math.sin(k * 5 + a * 4 + i) * k * 2, 1 + 13 * k * min(1, .3 + a), 0) for k in np.linspace(0, 1, 16)]), np.linspace(.25, 1.5, 16), 'smoke', '#8a6a6a', '#3a2028', seed=i, amt=.5 * (1 - a / 1.1))
        return st.finish(bloom=.35, thr=1.0, vig=.5 + .2 * u, contrast=1.06, expo=.95, fade=smooth(66, 72, f), fadeCol='#0a0306')
