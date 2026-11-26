"""d3 (84): the crouch and the leap.  He gathers himself on the peak (f0-30): rock cracks (f12 f18 f24), trees bow inward, dust runs to his feet.  The hold: his eyes (f30-41).  f42 LEAP over the lens; the peak bursts; the camera whips round after him: a comet rising against the sun, trees torn after him like arrows and falling away one by one."""
from lau.shot import *
from lau.look import *
from chars import hanuman as HM, vanara as VN
from shots import d_kit as K

G = 12.                                                          # his size
YAW = 130.
SW = nz(K.SEAWARD)
KINDS = ('pahari_round', 'ashoka', 'mango', 'kadamba')


def az(a, e=0.): a, e = math.radians(a), math.radians(e); return V(math.sin(a) * math.cos(e), math.sin(e), math.cos(a) * math.cos(e))


SUND = az(135., 17.5)


def path(T):
    """where he is, T seconds after the leap"""
    T = max(T, 0.); return SW * (900 * (1 - math.exp(-1.6 * T)) + 200 * T) + V(0, 470 * (1 - math.exp(-2.2 * T)) + 70 * T, 0) + az(45.) * 90 * T ** 1.6


def da_sign(a, b): return float(a.R[0] @ b.R[2])


class Shot(ShotBase):
    id = 'd3'; n = 84
    EVENTS = [(0, 'wind', dict(dur=41)), (4, 'giant crouches', dict(dur=20)), (12, 'rock cracks', {}), (18, 'rock cracks', {}), (24, 'rock cracks', dict(big=1)), (14, 'trees groan', dict(dur=16)), (30, 'everything stops', dict(dur=11)), (33, 'eyes open wide', {}), (36, 'heartbeat', {}), (42, 'LEAP', {}), (42, 'mountain bursts', dict(dur=20)), (44, 'passes overhead', {}), (46, 'whip', {}), (48, 'trees torn up', dict(dur=20)), (50, 'boulders', dict(dur=14)), (54, 'shock wave on the sea', dict(dur=30)), (60, 'flight roar', dict(dur=24)), (64, 'tree falls away', {}), (70, 'tree falls away', {}), (76, 'tree falls away', {})]

    def setup(self, st):
        S = st.fig(HM.HANUMAN, self.pose(34), yaw=YAW, scale=G, draw=False); self.headp = S.head((0, -.05, .3))
        a = VN.arm; k5 = [VN.WARRIOR, VN.LANGUR, VN.YOUTH, VN.WARRIOR2, VN.YOUTH2]; low = VN.V_STAND.set(pel=(0, 3.4, -.6), pelr=(0, 34, 0), cher=(0, 22, 0), hedr=(0, -30, 0), lh=(1.8, 4.4, 3.2), rh=(-1.8, 4.4, 3.2), lhand='claw', rhand='claw', lf=(1.3, VN.GY, .6), rf=(-1.3, VN.GY, -.8))
        self.cr = Crowd(st, [(fg, low, Face(mouth=.25), y + 12 * (i - 2)) for y in (200, 20) for i, fg in enumerate(k5)], px=380, pitch=6.); self.low = low
        r = np.random.default_rng(4); n = 110; th = np.radians(r.uniform(40, 330, n)); q = r.uniform(30, 54, n); P = np.c_[np.sin(th) * q + K.CX, 0 * q, np.cos(th) * q + K.CZ]; cd = az(100); sd_ = V(cd[2], 0, -cd[0]); P = P[(np.hypot(P[:, 0], P[:, 2]) > 38) & (np.abs(P @ sd_ - 4) > 17)]; P[:, 1] = K.ground(P[:, 0], P[:, 2]); self.P = P; n = len(self.P); self.kind = r.integers(0, 5, n); self.sc = r.uniform(.72, .9, n); self.tint = np.clip(r.normal(1, .1, (n, 1)) + r.normal(0, .03, (n, 3)), .72, 1.2)
        # rocks lying on the top, boulders of the burst
        n = 46; th = r.uniform(0, 6.283, n); q = r.uniform(34, 60, n); self.lie = np.c_[np.sin(th) * q + K.CX, 0 * q, np.cos(th) * q + K.CZ]; self.lie[:, 1] = K.ground(self.lie[:, 0], self.lie[:, 2]); self.lies = r.uniform(1.4, 4.6, n); self.lieR = K.rotmats(*r.uniform(-1, 1, (3, n)) * np.array([[3.], [.5], [.5]]))
        n = 260; th = r.uniform(0, 6.283, n); q = 46 * r.uniform(0, 1, n) ** .5; self.b0 = np.c_[np.sin(th) * q, r.uniform(-12, 2, n), np.cos(th) * q]; self.bv = np.c_[np.sin(th), 0 * th, np.cos(th)] * r.uniform(20, 120, n)[:, None] + V(0, 1, 0) * r.uniform(60, 250, n)[:, None] + SW * r.uniform(0, 150, n)[:, None]; self.bs = 1.6 + 9.5 * r.uniform(0, 1, n) ** 2.4; self.ba, self.bw = r.uniform(-3, 3, (3, n)), r.uniform(-5, 5, (3, n))
        # trees: standing ones on the slopes, and those he takes with him
        n = 320; th = r.uniform(0, 6.283, n); q = 74 + 190 * r.uniform(0, 1, n) ** 1.1; P = np.c_[np.sin(th) * q + K.CX, 0 * q, np.cos(th) * q + K.CZ]; cd = az(100); sd_ = V(cd[2], 0, -cd[0]); dep, sid = P @ cd, P @ sd_; ok = ~((dep > -14) & (np.abs(sid) < 80 + .22 * (dep - 20))) & ~((dep > 120) & (np.abs(sid) < 130)); P = P[ok]; P[:, 1] = K.ground(P[:, 0], P[:, 2]) - 1.5; self.T, self.Th, self.Tk = P, r.uniform(38, 66, len(P)), r.integers(0, 4, len(P))
        n = 90; th = np.radians(100 + np.tile([-1, 1], 45) * r.uniform(48, 170, n)); q = r.uniform(58, 150, n); P = np.c_[np.sin(th) * q, 0 * q, np.cos(th) * q]; P[:, 1] = K.ground(P[:, 0], P[:, 2]); self.f0, self.fk, self.fh = P, r.integers(0, 4, n), r.uniform(34, 58, n); self.flag = np.sort(r.uniform(.16, .80, n)); fa, fr = r.uniform(0, 6.283, n), r.uniform(120, 300, n); e1 = az(45); self.foff = e1[None] * (np.cos(fa) * fr * 1.25)[:, None] + V(0, 1, 0)[None] * (np.sin(fa) * fr * .8 - 20)[:, None]; self.ffall = np.linspace(1.75, .62, n) + r.normal(0, .05, n); self.fph = r.uniform(0, 6.28, n)

        # nothing may cross between the lens and him
        okT, okB = np.ones(len(self.f0), bool), np.ones(len(self.b0), bool)
        for f in range(52, 84):
            c = self.camera(f); h = c.project(path((f - 42) / 24.)); Pt, At = self.flying(f); X = c.project(Pt + At * self.fh[:, None] * .5); r_ = self.fh * .8 * c.fl * 540 / np.maximum(X[:, 2], 1.); okT &= ~((X[:, 2] > 0) & (X[:, 2] < h[2] + 60) & (np.hypot(X[:, 0] - h[0], X[:, 1] - h[1]) < 150 + r_)); X = c.project(self.debris(f)[0]); r_ = self.bs * c.fl * 540 / np.maximum(X[:, 2], 1.); okB &= ~((X[:, 2] > 0) & (X[:, 2] < h[2] + 60) & (np.hypot(X[:, 0] - h[0], X[:, 1] - h[1]) < 130 + r_))
        for k in ('f0', 'fk', 'fh', 'flag', 'foff', 'ffall', 'fph'): setattr(self, k, getattr(self, k)[okT])
        for k in ('b0', 'bv', 'bs'): setattr(self, k, getattr(self, k)[okB])
        self.ba, self.bw = self.ba[:, okB], self.bw[:, okB]; print('d3: trees', okT.sum(), 'boulders', okB.sum())

    # ---- acting
    def pose(self, f):
        g = on2(f); C = HM.H_CROUCH; ST = HM.H_STAND.set(lf=(1.7, HM.GY, .2), rf=(-1.7, HM.GY, -.2), lft=(26, 0), rft=(-26, 0), hedr=(0, 4, 0), cher=(0, 6, 0)); RE = ST.set(cher=(0, -14, 0), hedr=(0, -16, 0), lh=(4.7, 8.3, -1.4), rh=(-4.7, 8.3, -1.4), lel=(1, .5, -.6), rel=(-1, .5, -.6), lhand='fist', rhand='fist', pel=(0, 7.5, -.1))
        D = C.set(pel=(0, 2.75, -1.9), pelr=(0, 40, 0), hedr=(0, -52, 0)); D2 = C.set(pel=(0, 2.55, -2.2), pelr=(0, 44, 0), cher=(0, 30, 0), hedr=(0, -58, 0))
        return keys(g, [(0, ST), (6, RE, 'io'), (12, C.set(pel=(0, 3.4, -1.2)), 'in'), (14, D, 'out'), (18, C), (24, D, 'io'), (27, C), (30, D, 'io'), (38, D), (41, D2, 'in')])

    def shaken(self, f):
        a = sum(k * decay((f - q) / 24., 8.) * (f >= q) for q, k in ((12, 1.6), (18, 1.4), (24, 2.2), (42, 9.))); return a

    def camera(self, f):
        d = az(100.); s = V(d[2], 0, -d[0]); H = self.headp
        base = d * keys(f, [(0, 176.), (27, 158.), (31, 120., 'io'), (41, 117.), (43, 132., 'out'), (50, 172., 'out')]) + V(0, keys(f, [(0, 46.), (27, 40.), (31, 40., 'io'), (41, 39.), (44, 36.), (50, 46.), (55, 150., 'io'), (62, 270., 'out'), (84, 430., 'linear')]), 0) + s * keys(f, [(0, -6.), (27, 2.), (31, 18., 'io'), (41, 18.), (44, 4.)])
        if f >= 50: base = lerp(base + SW * 20 * smooth(50, 56, f), path((f - 42) / 24.) - SUND * keys(f, [(50, 400.), (62, 455.), (84, 640.)]) + az(45.) * -14 + V(0, 10, 0), smoother(51, 60, f))
        at = V(*keys(f, [(0, (0, 90, 0)), (9, (0, 84, 0)), (14, (0, 48, 0), 'io'), (27, tuple(V(0, 52, 0) + s * 6)), (31, tuple(H), 'io'), (41, tuple(H + V(0, -2, 0))), (42, (0, 104, 0), 'step'), (44, (0, 96, 0)), (45, (0, 60, 0), 'out'), (47, (0, 66, 0))])); fov = keys(f, [(0, 58.), (10, 57.), (14, 50., 'io'), (27, 47.), (31, 17.5, 'io'), (41, 16.), (42, 84., 'step'), (44, 82.), (45, 58., 'out'), (47, 60.), (62, 50.), (84, 47.)])
        if f == 42: at = V(0, 104, 0)
        # the whip: from looking in at him to looking out after him
        if f >= 47:
            k = smoother(47, 51.5, f); dirA = nz(V(0, 66, 0) - base); him = path((f - 42) / 24.); dirB = nz(him - base); dirB = nz(lerp(dirB, az(136, 3.), smooth(54, 68, f)))
            aA, aB = math.atan2(dirA[0], dirA[2]), math.atan2(dirB[0], dirB[2]); da = (aB - aA) % (2 * math.pi) - 2 * math.pi * ((aB - aA) % (2 * math.pi) > math.pi); a = aA + da * k; e = lerp(math.asin(dirA[1]), math.asin(dirB[1]), k) + .75 * math.sin(math.pi * k); at = base + 100 * V(math.sin(a) * math.cos(e), math.sin(e), math.cos(a) * math.cos(e))
        jx, jy = shake(f, self.shaken(f) * (1 - .8 * smooth(54, 64, f)), .95, 5); roll = keys(f, [(0, -2.), (27, -2.), (31, 3.), (41, 3.), (42, -5., 'step'), (47, -7., 'out'), (50, 9.), (57, -4.), (84, 0.)])
        return Cam(base + s * jx * .3 + V(0, jy * .3, 0), at + s * jx + V(0, jy, 0), fov, roll=roll)

    # ---- things the shot throws about
    def debris(self, f):
        T = (f - 42) / 24.; g = (1 - np.exp(-.9 * T)) / .9; P = self.b0 + self.bv * g * 1.35 + V(0, -60, 0) * T * T; W = path(T * .9) * np.clip(self.bv @ SW / 300., 0, .7)[:, None]; return P + W * smooth(0, .5, T), K.rotmats(*(self.ba + self.bw * T))

    def flying(self, f):
        """trees streaming after him: foot, axis"""
        T = (f - 42) / 24.; n = len(self.f0); P, A = np.zeros((n, 3)), np.zeros((n, 3))
        for i in range(n):
            def at(t):
                q = max(0., t - self.flag[i] * .55); e = q * (1 - .25 * self.flag[i]); s = smooth(0., .35, q); p = lerp(self.f0[i], path(e) * 1.0 + self.foff[i] * (1 + .3 * q), s) if q > 0 else self.f0[i]
                if t > self.ffall[i] + .35: u = t - self.ffall[i] - .35; p = p - SW * 130 * u - V(0, 150 * u * u + 60 * u, 0)
                return np.asarray(p, float)
            P[i] = at(T); v = at(T) - at(T - .06); v = nz(v) if np.linalg.norm(v) > .5 else V(0, 1, 0); w = .22 * math.sin(T * 5 + self.fph[i]); A[i] = nz(lerp(V(0, 1, 0), v, smooth(0., .3, T - self.flag[i] * .55)) + V(w, 0, w))
        return P, A

    def frame(self, f, st):
        st.clear('#000', f=f); t = st.t; g = on2(f); cam = self.camera(f); st.cam = cam; T = (f - 42) / 24.; air = f >= 42; out = f >= 46
        K.sky(st, sunDir=tuple(SUND), sunR=.165 if out else .06, sunCol='#ffc566' if out else '#fff2c0', sunGlow=lerp(.8, .62, float(out)), rays=.75, halo=1., cy1=.30 if not out else .20, cov=.6, cscale=1.3 if not out else 1.7, cZen='#b8502c' if not out else '#c85a30')
        kl = dict(key=tuple(nz(az(118, 34))), rim=(.5, .4, -.8)) if not out else dict(key=tuple(SUND), rim=tuple(SUND), rimCol=(2.4, 1.35, .55), fog=(.00010, 300., .0010, K.SEA_Y)); L = K.light(inkRef=2.2, **kl); Lb = K.light(inkRef=G * .8, **kl)
        crackR = keys(f, [(11, 0.), (13, 26., 'out'), (17, 28.), (19, 46., 'out'), (23, 48.), (25, 82., 'out'), (41, 88.), (43, 120.)]); crackK = keys(f, [(11, .7), (13, 1.5), (19, 1.9), (25, 2.6), (40, 2.8), (42, 5.)])
        hop = sum(2.2 * max(0., math.sin(min(1., max(0., (f - q) / 8.)) * math.pi)) for q in (12, 18, 24)); zg = float((V(0, 30, 0) - cam.eye) @ cam.R[2]); fwd = lambda P: (P - cam.eye) @ cam.R[2]
        # trees bow to the centre, then are blown flat
        pull = keys(f, [(8, 0.), (13, .5, 'out'), (17, .38), (20, .70, 'out'), (23, .58), (26, 1.02, 'out'), (30, .92), (41, 1.0), (43, -1.5, 'out'), (54, -.7), (66, -.2)])
        def standing(m):
            m = m & (fwd(self.T) > 4)
            if air: m = m & (np.linalg.norm(self.T, axis=1) > 135)
            if not m.any(): return
            P = self.T[m]; v = P - cam.eye; R = np.c_[-v[:, 2], 0 * v[:, 0], v[:, 0]]; R /= np.linalg.norm(R, axis=1, keepdims=True); c = V(K.CX * .3, 0, K.CZ * .3) - P; c[:, 1] = 0; c /= np.linalg.norm(c, axis=1, keepdims=True); q_ = np.linalg.norm(P, axis=1); ln = pull * (c * R).sum(1) * np.clip(1.5 - q_ / 170, .15, 1.2) + .05 * np.sin(t * 5 + P[:, 0]) * abs(pull); D = np.linalg.norm(v, axis=1); hz = np.clip((D - 160) / 1500, 0, .6); h = self.Th[m]; kd = self.Tk[m]
            for j, nm in enumerate(KINDS):
                q = kd == j
                if q.any(): K.FL.cards(st, K.FL.plate_of(nm, 'spring' if nm != 'ashoka' else 'summer', j), P[q], h[q] * (1 - .12 * abs(pull)), np.where(P[q][:, 0] * 7 % 2 > 1, 1., -1.), lean=ln[q], phase=P[q][:, 0], tint=(.94, .86, .76), haze=hz[q], hazeCol=hexc(K.GOLD_FOG))
        def giant():
            if f < 42:
                lid = keys(f, [(0, .9), (8, .7), (28, .55), (31, .40), (33, .42), (35, 1.0, 'snap'), (41, 1.)]); sk = .6 + .4 * smooth(32, 36, f)
                return K.giant(st, self.pose(f), yaw=YAW, scale=G, face=HM.VFace(lid=lid, frown=.35 + .4 * smooth(10, 32, f), squint=.2, spark=sk, smile=.12, gy=.12, gx=.1), slow=1., t=min(t, 1.25) * 1.3 + max(0., t - 1.25) * .12, tail='up', wind=(-.3, .02, .1), gem=cam.eye, ring='L')
            if f < 47:
                p = path(T * .8) + V(0, (-34, -46, -74, -30, 0)[f - 42], 0); M = model(p, YAW, pitch=lerp(6, 26, smooth(0, .12, T)), scale=G) @ np.diag([.86, (1.12, 1.35, 1.5, 1.4, 1.3)[f - 42], .86, 1.]); return K.giant(st, HM.H_LEAP.set(hedr=(0, -22, 0)), M=M, face=HM.VFace(frown=.8, spark=1., mouth=.4, teeth=.6), tail='whip', vel=SW * 300 + V(0, 600, 0), ring=None)
            return self.comet(f, st, cam, T)
        st.open(cam, L, far=20000.); K.mount(st, crackR=crackR, crackK=crackK, crater=float(air), sun=SUND, waveR=keys(f, [(44, 0.), (52, 900.), (62, 2100., 'linear'), (84, 4300., 'linear')]), cMid='#0f9aa6', cDeep='#086084', cLite='#58d6bc', cFar='#f0c488'); zc = float(fwd(path(T))) if f >= 47 else zg; standing(fwd(self.T) >= zg)
        if not air: K.rocks(st, self.lie + np.c_[0 * self.lies, hop * (1 + .5 * np.sin(np.arange(len(self.lies)) * 2.4)), 0 * self.lies], self.lies, self.lieR, sub=1)
        else: BP, BR = self.debris(f); q = fwd(BP) >= zc; K.rocks(st, BP[q], self.bs[q], BR[q], sub=2, col=('#c9a27c', '#8a5a5c', '#8a5a48'))
        if air: TP_, TA_ = self.flying(f)
        def fly(m):
            for j, nm in enumerate(KINDS): q = m & (self.fk == j) & (fwd(TP_) > 70); K.tree_cards(st, nm, TP_[q], TA_[q], self.fh[q], season='spring' if nm != 'ashoka' else 'summer', var=j, tint=(.80, .62, .50) if out else (.95, .86, .72))
        if f >= 47: fly(fwd(TP_) >= zc)
        elif f < 42: giant()
        if not air: m = (fwd(self.P) > 3) & (fwd(self.P) >= zg); self.vanaras(m, hop)
        st.close(); st.open(cam, Lb, far=20000.); S, TP, gem = giant(); self.Slast = S; st.close(); self.fx(f, st, cam, T, S)
        st.open(cam, K.light(inkRef=1.2, **kl), far=20000.)
        if f < 47: standing(fwd(self.T) < zg)
        if air:
            q = (fwd(BP) < zc) & (fwd(BP) > 80); K.rocks(st, BP[q], self.bs[q], BR[q], sub=2, ink=.7, col=('#c9a27c', '#8a5a5c', '#8a5a48')); fly(fwd(TP_) < zc)
        elif f < 29:
            self.vanaras((fwd(self.P) > 3) & (fwd(self.P) < zg), hop); d0 = az(100); s0 = V(d0[2], 0, -d0[0])
            for k, (x, dd, fg, y) in enumerate(((-34, 62, VN.YOUTH, 200), (-44, 56, VN.LANGUR2, 190), (37, 60, VN.WARRIOR, 160), (47, 66, VN.YOUTH2, 170))):
                q = d0 * dd + s0 * x; q[1] = float(K.ground(q[0], q[2])) + 1.; st.fig(fg, self.low.set(hedr=(0, -34, 8 * math.sin(k + f * .2)), lh=(2.0, 4.0 + .5 * hop, 3.4)), at=q + V(0, hop * .8, 0), yaw=100 + y, scale=.95, face=Face(mouth=.3))
        st.close(); self.fx2(f, st, cam, T)
        if 28 < f < 32: IM.zoomblur(st, (960, 520), .06 * (2 - abs(f - 30)))
        if f in (42, 43): IM.speedlines(st, cam.project(V(0, 40, 0))[:2], amt=.8, col='#fff0d0', seed=f, inner=.25); IM.inkflash(st, dark='#1a0410', mid='#e0501c' if f == 42 else '#b8242a', light='#fff3dc', lo=.30, hi=.60, invert=(f == 43))
        if f == 44: K.smear(st, 30, -90)
        if 46 < f < 52:
            c0, c1 = self.camera(f), self.camera(f + 1); q = c0.project(c1.eye + c1.R[2] * 100); z = q[2]; K.smear(st, float(np.clip(q[0] - 960 if z > 5 else 400 * np.sign(da_sign(c0, c1)), -380, 380)) * .8, float(np.clip(q[1] - 540 if z > 5 else 0, -260, 260)) * .8)
        return st.finish(bloom=.42, thr=.98, vig=.38, contrast=1.05, flash=.12 * (f == 44), flashCol='#fff0d0')

    def vanaras(self, m, hop):
        if m.any(): self.cr.draw(self.P[m] + V(0, hop * .7, 0), scale=self.sc[m], tile=self.kind[m] + np.where((self.P[m] @ az(100)) > 0, 0, 5), tint=self.tint[m])

    def comet(self, f, st, cam, T):
        p = path(T); sway = 6 * math.sin(T * 5.); P_ = HM.H_FLY_L; k = smooth(47, 54, f); pose = keys(on2(f), [(47, HM.H_LEAP), (54, P_.set(hedr=(10, -40, 0)), 'io'), (62, P_), (72, P_.set(lh=(1.9, 12.4, 8.5))), (84, P_)]); fw = az(74.)
        S, _, _ = K.giant(st, pose, at=p - V(0, 8 * G, 0), yaw=lerp(100, 74, k), pitch=-30 * k + 4 * math.sin(T * 4), roll=sway, scale=G, face=HM.VFace(spark=1., frown=.3), cloth=False, ring=None)
        TP = HM.tail(st, S, T * .9, 'fly', length=17., vel=fw * 60 + V(0, 25, 0)); up = cam.R[1]
        for j, (ln, ph, wd) in enumerate(((8.5, 0., 1.5), (7., 2., 1.15))):
            Q = CL.lag(lambda q: S.pelvis((.6, .4, -.4 - .3 * j)), T, 16, ln * G, wind=tuple(-fw * 1.1 + V(0, -.35 - .25 * j, 0)), grav=.15, wave=.55, freq=1.1, phase=ph); st.mesh(*CL.strip(Q, np.linspace(.9, wd, 16) * G, up=up, n=44, curl=.12), kind=1, col=('#e0342a', '#8a1c24', '#f6c24a'), cls=8, u=dict())
        return S, TP, None

    def fx(self, f, st, cam, T, S):
        t = st.t; s0 = V(0, 1.5, 0)
        if 6 <= f < 42:
            # dust and leaves run to his feet
            n = 120; r = np.random.default_rng(2); ph = r.uniform(0, 1, n); u = ((f / 24. * r.uniform(.8, 1.3, n)) + ph) % 1. if f < 30 else ((30 / 24. * r.uniform(.8, 1.3, n)) + ph) % 1.; a = r.uniform(0, 6.28, n) + 1.1 * u; R = 100 * (1 - u) ** 1.5 + 16; P = np.c_[np.sin(a) * R, 3 + r.uniform(0, 8, n) * (1 - u) + 2 * u, np.cos(a) * R]; k = smooth(6, 14, f); FX.particles(st, P, r.uniform(.5, 1.5, n), '#f2c088', 'petal', rot=a * 3, alpha=k * np.minimum(1, u * 6))
            n = 30; r = np.random.default_rng(3); ph = r.uniform(0, 1, n); tt = min(f, 30) / 24.; u = (tt * r.uniform(.7, 1.1, n) + ph) % 1.; a = r.uniform(0, 6.28, n) + .8 * u; R = 92 * (1 - u) ** 1.3 + 20; P = np.c_[np.sin(a) * R, 3 + 0 * a, np.cos(a) * R]; P[:, 1] += np.maximum(K.ground(P[:, 0], P[:, 2]), -20); K.sprites(st, P, 9 * (1 - .55 * u) * K.CW / K.CH, 9 * (1 - .55 * u), var=r.integers(0, 8, n), rot=a * .3, alpha=.8 * k * np.sin(math.pi * u), puff=True, near=14., **K.DUST)
        for q, k in ((12, .8), (18, .9), (24, 1.3)):
            if f < 42: K.dust(st, (0, 1, 0), (f - q) / 24., n=22, R=26, speed=80 * k, size=3.6 * k, rise=8, seed=q, near=18., life=.8)
            if 0 <= f - q < 14: FX.burst(st, 50, V(0, 2, 0) + SW * 14, (f - q) / 24., speed=70 * k, grav=90, size=.8, seed=q, col='#e8b480', kind='dot', life=.6, spread=(1, .4, 1), up=.6, drag=2.5)
        if f >= 42:
            for k, (n, R, sp, sz) in enumerate(((46, 30, 330, 22), (40, 16, 160, 24), (34, 50, 420, 15))): K.dust(st, (0, -4, 0), T + .05 - .02 * k, n=n, R=R, speed=sp, size=sz, rise=(90, 230, 60)[k], seed=60 + k, near=24., life=1.5, flat=.35)
            # shock rings in the air
            for k in range(3):
                u = T - .05 * k
                if 0 < u < .6 and f < 50:
                    c = path(.12 + .12 * k); a = np.linspace(0, 6.283, 64); ax = nz(SW + V(0, .9, 0)); e1 = nz(np.cross(ax, V(0, 1, 0))); e2 = np.cross(ax, e1); R = 60 + 420 * ease_out(u / .6, 2.); Q = c + (np.cos(a)[:, None] * e1 + np.sin(a)[:, None] * e2) * R; FX.ribbon(st, Q, 9 * (1 - u / .6), mode='light', col='#ffd890', col2='#fffbe8', amt=1 - u / .6)
    def fx2(self, f, st, cam, T):
        t = st.t
        if 29 <= f < 42: FX.drift(st, 46, (tuple(self.headp + az(100) * 10 - 34), tuple(self.headp + az(100) * 90 + 34)), 2. + (f - 29) * .004, kind='petal', size=.75, col='#ffd9a0', col2='#f2a0a0', fall=.4, sway=.4, seed=5)
        if 46 <= f < 54: Q = np.array([path(T - .016 * k) for k in range(34)]); FX.ribbon(st, Q[2:], np.linspace(24, 2, 32), mode='light', col='#ff9a3a', col2='#fff0c0', amt=.55 * (1 - smooth(50, 54, f)), blend='add')
        if f >= 47:
            S = self.Slast; bk = nz(S.joint(0) - S.joint(1)); side = nz(np.cross(bk, cam.R[2])); feet = (S.joint(12) + S.joint(16)) / 2; k = smooth(50, 56, f)
            u = np.linspace(0, 1, 40)
            def arc(o, L, bend, j): return feet + o + bk * (u * L)[:, None] - cam.R[0] * (u ** 2 * L * bend)[:, None] - V(0, 1, 0) * (u ** 1.7 * L * .35)[:, None] + side * (np.sin(u * 4 - T * 7 + j * 1.7) * 7 * u)[:, None]
            FX.ribbon(st, arc(V(0, 0, 0), 420, .35, 0), np.linspace(58, 6, 40), mode='light', col='#ff9a4a', col2='#ffe2a0', amt=.34 * k, blend='add')
            for j in range(9): FX.ribbon(st, arc(side * (j - 4) * 10, (430, 260, 340, 210, 380, 240, 310, 200, 360)[j], .30 + .03 * ((j * 5) % 7), j), np.linspace(2.6 + (j % 3) * 1.3, .4, 40), mode='light', col='#ffd080', col2='#fffbe8', amt=.75 * k, blend='add')
            P, A = self.flying(f); n = 700; r = np.random.default_rng(9); i = r.integers(0, len(P), n); lf = r.uniform(0, 1, n); v = path(T) - path(T - .1); Z = P[i] + A[i] * (self.fh[i] * .7)[:, None] + r.normal(0, 13, (n, 3)) * (1 + 1.5 * lf[:, None]) - nz(v) * (lf * 110)[:, None] - V(0, 1, 0) * (lf * lf * 22)[:, None]; col = np.array([hexc('#f2a0b8'), hexc('#ff7a4a'), hexc('#ffd27a'), hexc('#c8e08a')])[self.fk[i]]; FX.particles(st, Z, r.uniform(1.3, 2.8, n), col, 'petal', rot=r.uniform(0, 6, n) + t * r.uniform(-6, 6, n), alpha=(1 - lf) ** .5)
            FX.embers(st, 60, (tuple(path(T) - 40), tuple(path(T) + 30)), t, rise=-20, size=2.2, seed=4, life=.8, swirl=12)
