"""d2 (84): on the shore mountain he remembers what he is.  Eyes closed, one breath (f0-12); three surges of growth (f18, f30, f42-72) and the camera rides up him, past treetops and birds and through the cloud, to his opening eyes (f70)."""
from lau.shot import *
from lau.look import *
from chars import hanuman as HM, vanara as VN, birds as BD
from shots import d_kit as K

YAW = 118.
CLOUD_Y = 285.
NECK = -K.SEAWARD                                                # the land side, where the army stands


def az(a): a = math.radians(a); return V(math.sin(a), 0, math.cos(a))


class Shot(ShotBase):
    id = 'd2'; n = 84
    EVENTS = [(0, 'sea wind', dict(dur=84)), (0, 'vanara murmur', dict(dur=18)), (4, 'breath', {}), (18, 'first surge', {}), (19, 'ground hit', {}), (22, 'crowd gasps', dict(dur=10)), (30, 'second surge', {}), (31, 'ground hit', {}), (33, 'rocks roll', dict(dur=8)), (42, 'third surge', dict(dur=30)), (45, 'anklet bells', {}), (49, 'birds scatter', {}), (52, 'cloth', dict(dur=20)), (56, 'through cloud', dict(dur=10)), (62, 'crowd cheers far below', dict(dur=22)), (70, 'eyes open', {}), (74, 'ring glints', {})]

    def setup(self, st):
        a = VN.arm; k5 = [VN.WARRIOR, VN.LANGUR, VN.YOUTH, VN.WARRIOR2, VN.YOUTH2]; look = VN.V_STAND.set(hedr=(0, -34, 0), cher=(0, -2, 0))
        items = [(fg, VN.V_CHEER(p / 4 + .1 * i), Face(mouth=.5, smile=1), 180 + 14 * (i - 2)) for i, fg in enumerate(k5) for p in range(4)] + [(fg, VN.V_CHEER(p / 4 + .1 * i), Face(mouth=.5, smile=1), 24 * (i - 2)) for i, fg in enumerate(k5) for p in range(4)] + [(fg, look, Face(mouth=.15), y + 10 * (i - 2)) for y in (180, 0) for i, fg in enumerate(k5)]
        self.cr = Crowd(st, items, px=420, pitch=4.); r = np.random.default_rng(5); cd = az(74); sd = V(cd[2], 0, -cd[0])
        n = 300; th = r.uniform(0, 6.283, n); q = 15 + 50 * r.uniform(0, 1, n) ** .8; P = np.c_[np.sin(th) * q, 0 * q, np.cos(th) * q]; side, dep = P @ sd, P @ cd; m = ~((np.abs(side) < 7 + .30 * np.maximum(dep, 0)) & (dep > 2)) & ~((side > -4) & (dep < -6)) & ~((dep > 12) & (dep < 60)); P = P[m]
        # the army on the neck of land: grains
        n = 2600; q = 60 + 1900 * r.uniform(0, 1, n) ** .9; th = math.atan2(NECK[0], NECK[2]) + r.normal(0, .17, n) * (1 + 60 / q); G = np.c_[np.sin(th) * q + K.CX, 0 * q, np.cos(th) * q + K.CZ]; P = np.vstack([P, G]); P[:, 1] = K.ground(P[:, 0], P[:, 2]); P = P[P[:, 1] > K.SEA_Y + 20]; n = len(P)
        self.P, self.dep, self.q, self.kind, self.ph, self.sc = P, P @ cd, np.hypot(P[:, 0], P[:, 2]), r.integers(0, 5, n), r.uniform(0, 1, n), r.uniform(.70, .92, n)
        self.tint = np.clip(r.normal(1, .10, (n, 1)) + r.normal(0, .035, (n, 3)), .72, 1.2); self.flip = r.choice([-1., 1.], n)
        # vanaras near the lens, drawn whole: (side, depth, kind, scale, yaw)
        self.near = [(sd * s + cd * d, fg, sc, math.degrees(math.atan2(-cd[0], -cd[2])) + y, p) for s, d, fg, sc, y, p in ((-5.4, 17.6, VN.YOUTH, .66, 12, 0.), (-9.4, 13.6, VN.LANGUR2, .72, 20, .3), (8.8, 16.6, VN.WARRIOR, .70, -16, .5), (12.4, 11.4, VN.YOUTH2, .70, -28, .8), (6.2, 11.6, VN.LANGUR, .62, -14, .2))]
        rb = np.random.default_rng(8); m = 90; a_ = rb.uniform(0, 6.28, m); d_ = rb.uniform(30, 140, m); self.bird0 = np.c_[np.sin(a_) * d_, rb.uniform(-6, 40, m), np.cos(a_) * d_]; self.birdv = np.c_[np.cos(a_), rb.uniform(.5, 1.1, m), -np.sin(a_)] * rb.uniform(26, 60, (m, 1))
        rt = np.random.default_rng(21); m = 16; sg = np.tile([-1, 1], 8); a_ = np.radians(74 + sg * rt.uniform(30, 50, m)); d_ = rt.uniform(56, 78, m); self.rt = np.c_[np.sin(a_) * d_, 0 * d_, np.cos(a_) * d_]; self.rt[:, 1] = K.ground(self.rt[:, 0], self.rt[:, 2]) - 2; self.rth = rt.uniform(56, 84, m)
        near = np.min([np.linalg.norm(self.birds(q) - self.camera(q).eye, axis=1) for q in range(43, 64)], axis=0); self.bird0, self.birdv = self.bird0[near > 30], self.birdv[near > 30]
        # cloud layer: a ring round him and a sea of them beyond, with a window over the army
        rc = np.random.default_rng(12); N = 260; a_ = rc.uniform(0, 6.28, N); d_ = np.r_[rc.uniform(95, 420, 70), 420 + 3600 * rc.uniform(0, 1, N - 70) ** 1.5]; C = np.c_[np.sin(a_) * d_, CLOUD_Y + rc.normal(0, 10, N) + .006 * d_, np.cos(a_) * d_]; w = rc.uniform(60, 120, N) * (1 + d_ / 700)
        cam = self.camera(80); X = cam.project(C); pp = cam.fl * 540 / np.maximum(X[:, 2], 1.); win = (((X[:, 0] - 280) / (330 + .62 * w * pp)) ** 2 + ((X[:, 1] - 830) / (270 + .30 * w * pp)) ** 2 < 1) & (X[:, 2] > 0); keep = ~win; self.cl, self.clw, self.cld = C[keep], w[keep], d_[keep]; m = len(self.cl); self.clv = rc.integers(0, 8, m); self.clf = rc.choice([-1., 1.], m)

    def birds(self, f): return self.bird0 + V(0, 42 - 46 * decay((f - 43) / 24., 7), 0) + self.birdv * (f - 45) / 24.

    # ---- his size, his pose
    def size(self, f):
        l = math.log; return math.exp(keys(f, [(0, l(1.15)), (13, l(1.15)), (17, l(1.06)), (22, l(3.35), 'out'), (26, l(2.95)), (29, l(2.72)), (36, l(10.6), 'out'), (40, l(9.5)), (42, l(9.2)), (71, l(37.2), 'io'), (77, l(36.0)), (84, l(36.2))]))

    def pose(self, f):
        g = on2(f); A = HM.H_ANJALI.set(hedr=(-16, 10, 0)); IN = HM.H_STAND.set(pel=(0, 7.1, -.1), cher=(0, 10, 0), hedr=(0, 22, 0), lh=(3.0, 7.2, 1.2), rh=(-3.0, 7.2, 1.2), lhand='fist', rhand='fist')
        UP = HM.H_STAND.set(pel=(0, 7.5, 0), cher=(0, -12, 0), hedr=(-10, -6, 0), lh=(4.6, 6.9, .2), rh=(-4.6, 6.9, .2), lhand='fist', rhand='fist', lf=(1.7, HM.GY, .4), rf=(-1.7, HM.GY, -.1), lft=(26, 0), rft=(-26, 0))
        ST = HM.H_STAND.set(cher=(0, -6, 0), hedr=(-10, 6, 0), lh=(4.2, 6.7, .5), rh=(-4.2, 6.7, .5), lhand='fist', rhand='fist', lf=(1.7, HM.GY, .4), rf=(-1.7, HM.GY, -.1), lft=(26, 0), rft=(-26, 0))
        RING = ST.set(lh=(3.7, 11.6, 3.0), lel=(.8, -1, -.1), lhand='relax', lfing=(-.06, 1, .16), lpalm=(-.62, .05, -.78), cher=(-8, -5, 0), hedr=(-14, 2, -4), pel=(0, 7.42, 0))
        return keys(g, [(0, A), (4, A), (10, A.set(cher=(0, -3, 0), hedr=(-16, 14, 0), pel=(0, 7.5, 0))), (17, IN, 'io'), (22, UP, 'out'), (26, ST), (29, IN), (35, UP, 'out'), (40, ST), (43, IN.set(hedr=(0, 14, 0))), (52, UP), (60, ST), (68, RING, 'io'), (71, RING.set(lh=(3.7, 11.95, 3.0), hedr=(-14, -3, -4)), 'out'), (76, RING)])

    def camera(self, f):
        G = self.size(f); sh = 0.; h = keys(f, [(38, .85), (45, 1.6, 'io'), (58, 8.0, 'linear'), (68, 12.9, 'out'), (84, 13.1)]); d = az(74); s = V(d[2], 0, -d[0])
        # low among the vanaras, thrown back by the surges, then in to his foot for the ride
        lowE = d * keys(f, [(0, 28.5), (17, 26.5), (21, 30., 'out'), (30, 33.), (34, 64., 'out'), (39, 60.)]) + V(0, 4.4, 0) + s * 1.4; lowA = V(0, keys(f, [(0, 8.0), (17, 8.3), (22, 23., 'out'), (28, 21.), (30, 21.), (36, 52., 'out'), (39, 54.)]), 0) + s * 1.2; lowF = keys(f, [(0, 41.), (17, 39.), (22, 60., 'out'), (30, 58.), (36, 70., 'out')])
        a2 = az(keys(f, [(38, 58.), (58, 80., 'linear'), (84, 101., 'out')])); rid = keys(f, [(38, 5.0), (46, 5.6), (60, 7.4), (68, 8.8), (84, 11.6, 'io')]); rideE = a2 * rid * G + V(0, h * G, 0); up = keys(f, [(38, 2.6), (50, 1.8), (62, .2), (70, -.95), (84, -1.6)]); s2 = V(a2[2], 0, -a2[0]); rideA = V(0, (h + up) * G, 0) + s2 * G * keys(f, [(38, .2), (60, .2), (70, -.35), (84, -.30)]); k = smoother(36, 42, f)
        for q in (18, 30): sh += 1.0 * decay((f - q) / 24., 7.) * (f >= q) * (1 + (q - 18) / 12)
        jx, jy = shake(f, sh, .9, 3); return Cam(lerp(lowE, rideE, k) + V(0, jy * .5, 0), lerp(lowA, rideA, k) + s * jx + V(0, jy, 0), lerp(lowF, keys(f, [(40, 62.), (60, 56.), (84, 42.)]), k), roll=lerp(-3., 2 * math.sin(f * .07), k))

    def frame(self, f, st):
        st.clear('#000', f=f); t = st.t; g = on2(f); G = self.size(f); cam = self.camera(f); st.cam = cam; eyeY = cam.eye[1]; hi = smooth(40, 160, eyeY)
        K.sky(st, cy1=lerp(.34, .13, hi), cov=lerp(.62, .5, hi), cscale=lerp(1.2, 1.8, hi), cdrift=0.)
        kl = dict(key=(.66, .46, -.34), rim=(.5, .4, -.8)); L = K.light(inkRef=1.6, fog=(lerp(.00026, .00017, hi), 260., .0012, K.SEA_Y), **kl)
        lid = keys(f, [(0, .75), (5, .6), (10, .02, 'io'), (69, .02), (72, 1.0, 'out'), (84, .95)]); sk = smooth(69, 73, f); face = HM.VFace(lid=lid, spark=sk, smile=.18 + .2 * smooth(72, 80, f), frown=.12 * smooth(68, 74, f), gx=keys(f, [(76, -.25), (79, .45, 'out')]), gy=.05)
        big = f >= 20; pose = self.pose(f); n = len(self.P)
        fig = lambda **k: K.giant(st, pose, yaw=YAW, scale=G, face=face, slow=lerp(1., .5, hi), tail='calm', wind=(.22, .03, -.10), ring='L' if f >= 58 else 'R', gem=cam.eye, sashlen=4.2, **k)
        cheer = f >= 36; away = self.dep > 4
        tl = self.kind * 4 + ((t * 2.2 + self.ph) * 4).astype(int) % 4 + np.where(away, 0, 20) if cheer else 40 + self.kind + np.where(away, 0, 5)
        hop = np.zeros(n)
        for q in (18, 30): u = (f - q) / 24. - self.q * .0025; hop += np.where((u > 0) & (u < .5), 2.6 * np.sin(np.clip(u / .5, 0, 1) * math.pi), 0)
        foot = V(0, 0, 0); keep = (np.hypot(self.P[:, 0], self.P[:, 2]) > 2.0 * G ** .9 + 3) & (((self.P - cam.eye) @ cam.R[2]) > 4); front = keep & (((self.P - cam.eye) @ cam.R[2]) < ((foot - cam.eye) @ cam.R[2]) - .5 * G); back = keep & ~front
        crowd = lambda m: self.cr.draw(self.P[m] + V(0, 1, 0) * hop[m, None], scale=self.sc[m], tile=tl[m], tint=self.tint[m], flip=self.flip[m])
        st.open(cam, L, far=20000.); K.mount(st, cMid='#129aa2', cDeep='#0a6280', cLite='#58d6bc'); K.trees(st, far=720, n=900 if eyeY < 60 else 1500, skip=lambda x, z: ((x * NECK[0] + z * NECK[2]) > .86 * np.hypot(x, z)) & (np.hypot(x, z) < 2000)); fig(); crowd(back if big else keep)
        st.close()
        C = self.cl + V(5, 0, -4) * t; X = cam.project(C); al = np.clip((np.abs(C[:, 1] - 0) - 0) / 1, 0, 1) * smooth(40, 150, eyeY); zg = float((-cam.eye) @ cam.R[2]); cloud = lambda m: K.sprites(st, C[m], self.clw[m], var=self.clv[m], flip=self.clf[m], alpha=al[m], fog=.00022, fogS=300., soft=40., near=40.)
        if big:
            cloud(X[:, 2] >= zg); st.open(cam, K.light(inkRef=max(1., G * .75), **kl), far=20000.); fig(); st.close()
        for q, R0, k, nn in ((18, 3.6, 1., 30), (30, 10., 1.9, 34), (43, 30., 2.6, 26)):
            K.dust(st, (0, 0, 0), (f - q) / 24., n=nn, R=R0, speed=52 * k, size=2.6 * k, rise=7 * k, seed=q, near=14., life=1.0)
        if big:
            if 43 <= f < 64:
                B = self.birds(f); st.open(cam, K.light(inkRef=1., **kl), far=4000.); BD.flock(st, 'parrot', B[::2], self.birdv[::2], t, size=2.6, rate=4.5, seed=3); BD.flock(st, 'swan', B[1::2], self.birdv[1::2], t, size=3.2, rate=3.2, seed=5); st.close()
            if 26 <= f < 62:
                st.open(cam, K.light(inkRef=1., **kl), far=4000.)
                for kd, m in (('palm', slice(0, 11)), ('tala', slice(11, 16))): K.FL.scatter(st, kd, self.rt[m], self.rth[m], season='summer', seed=4, vary=.1, tint=(.95, .86, .74))
                st.close()
            if front.any() and f < 60: st.open(cam, K.light(inkRef=1., **kl), far=20000.); crowd(front); self.close_ones(st, f, t); st.close()
            cloud(X[:, 2] < zg)
        else: st.open(cam, K.light(inkRef=1., **kl), far=4000.); self.close_ones(st, f, t); st.close()
        if f >= 66:
            gem = K.ring_on(st, K.giant(st, pose, yaw=YAW, scale=G, draw=False)[0], 'L', cam.eye, draw=False); k = smooth(70, 74, f); tw = .75 + .25 * math.sin(t * 9) + 1.6 * impulse((f - 73) / 24., 9); FX.particles(st, (gem + cam.R[2] * -.3 * G)[None], .62 * G * k * tw, '#ffb050', 'glint', alpha=.9 * k); FX.particles(st, (gem - cam.R[2] * .3 * G)[None], .26 * G * k, '#ff9a3a', 'lamp', alpha=k)
        return st.finish(bloom=.4, thr=.95, vig=.35)

    def close_ones(self, st, f, t):
        g = on2(f); 
        if f >= 36: return
        for P, fg, sc, yaw, ph in self.near:
            hop = sum(2.2 * math.sin(clamp((g - q - 1) / 9.) * math.pi) for q in (18, 30)); duck = sum(smooth(q, q + 3, g) * (1 - smooth(q + 8, q + 14, g)) for q in (18, 30))
            p = VN.V_STAND.set(hedr=(0, -36, 0), cher=(0, 2 + 10 * duck, 0), pel=(0, 6.45 - .9 * duck, 0), lh=(2.9 + .8 * duck, 5.6 + 5.0 * duck, 1.4 + 1.0 * duck), rh=(-2.9 - .4 * duck, 5.6 + 2.0 * duck, 1.4 + .6 * duck)); st.fig(fg, p, at=P + V(0, hop, 0), yaw=yaw, scale=sc, face=Face(mouth=.2))
