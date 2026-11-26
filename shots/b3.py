"""b3 (108): fourteen years in one tracking shot.  Rama, Sita and Lakshmana walk left to right, a step every nine frames; great near trunks cross the lens and the season changes behind them:
spring (f0: she touches a blossom), monsoon (f27: one leaf for two, Lakshmana looks back), autumn (f54: gold light, the river, a moored boat), winter (f81: shawls, breath, his hand steadies hers) and at the end a lamp-warm glow ahead."""
from shots.forest_kit import *
from chars import deer, birds

STEP = 4.2; V_ = STEP / 9.                                  # units per step, per frame
CUT = (27, 54, 81); SEASON = ('spring', 'monsoon', 'autumn', 'winter')
OFF = dict(spring=(6.9, -.2, -6.9), monsoon=(3.0, -.9, -8.2), autumn=(6.6, .2, -6.2), winter=(4.2, -.6, -7.2))   # Rama, Sita, Lakshmana ahead of the group's centre
PLAIN = deer.DEER.variant(pal={1: ('#b27a44', '#5c3524', 1), 8: ('#c89460', '#6e4630', 1), 2: ('#e8d8bc', '#8a7a70', 1), 3: ('#7a5238', '#3a2418', 1), 4: ('#7a5238', '#3a2418', 1), 5: ('#7a5238', '#3a2418', 1), 6: ('#e8dcc4', '#9a8878', 1), 11: ('#7a5238', '#3a2418', 1)})
LEAD = (1.6, -1.0)                                          # the group gains on the frame


def gx(f): return V_ * f


def figspace(at, p):
    """world point -> figure space of a walker (yaw 90, feet at `at`)"""
    d = np.asarray(p, float) - np.asarray(at, float); return (-d[2], d[1], d[0])


def boat_plate(c):
    """a moored dugout, 900 x 300, waterline at the bottom"""
    P = smooth_path([(20, 92), (120, 150), (450, 182), (760, 150), (880, 60), (868, 130), (800, 250), (700, 296), (200, 296), (90, 240)], 10, True); poly(c, P); c.set_source_rgb(*rgb('#5c2c1c')); c.fill_preserve(); c.set_source_rgb(*rgb('#1c0a0a')); c.set_line_width(6); c.stroke()
    for k, col in ((0, '#8a4a28'), (1, '#6e3620'), (2, '#8a4a28')):
        q = smooth_path([(70 + 12 * k, 168 + 34 * k), (440, 214 + 30 * k), (820 - 14 * k, 160 + 38 * k)], 14); ink(c, q, 20, col, (.2, .2)); ink(c, q + [0, 13], 4, '#2a1010', (.1, .1))
    q = smooth_path([(24, 94), (120, 152), (450, 184), (760, 152), (878, 64)], 12); ink(c, q, 16, '#c07a3c', (.1, .1)); ink(c, q + [0, 8], 4, '#2a1010', (.1, .1))
    for x in (250, 450, 640): c.rectangle(x, 168, 56, 14); c.set_source_rgb(*rgb('#a8662f')); c.fill_preserve(); c.set_source_rgb(*rgb('#1c0a0a')); c.set_line_width(4); c.stroke()
    c.arc(842, 112, 17, 0, 7); c.set_source_rgb(*rgb('#fff0d0')); c.fill_preserve(); c.set_source_rgb(*rgb('#1c0a0a')); c.set_line_width(4); c.stroke(); c.arc(846, 112, 8, 0, 7); c.fill()


class Shot(ShotBase):
    id = 'b3'; n = 108
    EVENTS = ([(f, 'footstep', dict(who='three', on='grass')) for f in range(0, 27, 9)] + [(f, 'footstep splash', dict(who='three')) for f in range(27, 54, 9)] + [(f, 'footstep', dict(who='three', on='dry leaves')) for f in range(54, 81, 9)] + [(f, 'footstep', dict(who='three', on='snow')) for f in range(81, 108, 9)]
              + [(0, 'spring birds', dict(dur=27)), (3, 'peacock', {}), (12, 'blossom shakes', {}), (24, 'trunk passes', dict(dur=6)), (27, 'rain', dict(dur=27)), (30, 'rain on leaf', dict(dur=24)), (36, 'thunder far', dict(soft=1)), (51, 'trunk passes', dict(dur=6)), (54, 'river', dict(dur=27)), (54, 'dry leaves', dict(dur=27)), (78, 'trunk passes', dict(dur=6)), (81, 'cold wind', dict(dur=27)), (90, 'bangles', dict(soft=1)), (98, 'lamp warmth', dict(dur=10))])

    def setup(self, st):
        self.a, self.old = {}, {}; self.boat = plate('b3_boat', 900, 300, boat_plate, 3)
        for s in SEASON: FL.plate_of('trunk_wide', s, 0)

    # -------------------------------------------------------------- one season
    def poses(self, f, s):
        """the three poses at frame f in season s, with their places"""
        ph = f / 18.; X = gx(f); at = [(X + o, 0, z) for o, z in zip(OFF[s], (0., .35, -.2))]
        look = -20.
        R = stride_pose(ph, arms=.9).set(hedr=(look, 0, 0)); S = stride_pose(ph + .5, pel=8.24, drop=.36, yaw=6, fs=.84, lift=.40, arms=.6, hip=.34).set(hedr=(look, 1, 0)); K = stride_pose(ph, arms=.8).set(hedr=(look, 0, 0))
        S = S.set(rh=(-1.5, 8.9, 1.2 + .2 * math.cos(2 * math.pi * ph)), rhand='pinch', rfing=(.6, .3, .7), rpalm=(.4, -.4, -.8), rel=(-1, -1, -.4), lh=(1.7, 7.6, S.lh[2] - .1))
        K = K.set(rh=(-2.35, 8.35, 1.25 + .25 * math.cos(2 * math.pi * ph)), rhand='grip', rfing=(.1, -.25, 1), rpalm=(1, 0, 0), rel=(-.8, -.3, -1))
        fr, fs_, fk = Face(smile=.25, lid=.92), Face(smile=.25, lid=.9), Face(smile=.05, lid=.95)
        if s == 'spring':
            k = keys(f, [(2, 0.), (4, -.08), (11, 1.04, 'io'), (13, 1.), (17, 1.), (24, .25, 'io')]); p = figspace(at[1], (at[1][0] + 1.15, 14.9, 1.1)); S = S.mix(S.set(rh=p, rhand='relax', rfing=(.1, .95, .35), rpalm=(.3, .1, 1), rel=(-1, -.5, .2)), k); S = S.set(hedr=(lerp(look, -26, k), lerp(1, -20, k), lerp(0, 4, k)), cher=(S.cher[0] - 8 * k, S.cher[1] - 4 * k, S.cher[2]))
            fs_ = Face(smile=.25, lid=.9) if f < 9 else Face(smile=.65, lid=.95, gy=.5, gx=.1, brow=.2)
            g = keys(f, [(12, 0.), (18, 1., 'io')]); R = R.set(hedr=(lerp(look, -58, g), 4 * g, 0), cher=(R.cher[0] - 16 * g, R.cher[1], R.cher[2])); fr = Face(smile=.25, lid=.92) if f < 15 else Face(smile=.5, lid=.85, gx=-.5)
        if s == 'monsoon':
            k = keys(f, [(24, 0.), (28, -.06), (35, 1.06, 'io'), (38, 1.)]); c = math.cos(4 * math.pi * ph) * .12
            R = R.set(lh=(1.55, lerp(9.4, 13.1, k) + c, lerp(1.4, .25, k)), lhand='grip', lfing=(-.6, .3, .6), lpalm=(-.3, 0, 1), lel=(1, -.6, .3), cher=(R.cher[0] - 10 * k, R.cher[1], R.cher[2]), hedr=(look - 34 * k, 5 * k, 0), shrug=(.7 * k, 0)); fr = Face(smile=.35, lid=.82, gx=-.5, gy=-.15)
            S = S.set(hedr=(look - 4, -8 * k, 3), rh=(-1.2, 10.4, 1.5), rhand='relax', rfing=(.8, .5, .3), rpalm=(0, -.2, -1)); fs_ = Face(smile=.35, lid=.85) if f < 36 else Face(smile=.5, lid=.92, gy=.45, gx=.2)
            q = keys(f, [(34, 0.), (36, -.05), (40, 1.05, 'io'), (42, 1.), (49, 1.), (54, .1, 'io')]); K = K.set(cher=(K.cher[0] - 46 * q, K.cher[1], K.cher[2]), hedr=(lerp(look, -74, q), -2 * q, 0), lh=(1.6, lerp(8.0, 10.4, q), lerp(.4, 1.3, q)), lhand='relax'); fk = Face(smile=.05, lid=.95) if f < 38 else Face(frown=.4, smile=-.1, lid=.9, squint=.2, gx=-.5)
        if s == 'autumn':
            K = K.set(hedr=(look - 6, -4, 0)); g = keys(f, [(60, 0.), (66, 1., 'io'), (76, 1.), (81, .3)]); S = S.set(hedr=(look - 22 * g, 10 * g, 0)); fs_ = Face(smile=.3, lid=.9) if f < 64 else Face(smile=.45, lid=.72, gy=-.5, gx=-.4)
            fr = Face(smile=.22, lid=.9, gx=.1); R = R.set(hedr=(look, -3, 0))
        if s == 'winter':
            dip = impulse((f - 86) / 24., 9) if f > 86 else 0.; k = keys(f, [(82, .15), (84, .10), (88, 1.05, 'out'), (90, 1.)]); hold = (at[1][0] + 2.25, 8.55 - .35 * dip + .08 * math.cos(4 * math.pi * ph), 1.75)
            R = R.mix(R.set(rh=figspace(at[0], hold), rhand='cup', rfing=(.25, -.25, -1), rpalm=(.2, 1, -.2), rel=(-1, -.8, -.5)), k); R = R.set(cher=(R.cher[0] - 18 * k, R.cher[1] + 3, R.cher[2]), hedr=(look - 34 * k, 10 * k, 0)); fr = Face(smile=.3, lid=.8, gx=-.4, gy=-.3) if f < 98 else Face(smile=.3, lid=.95)
            S = S.mix(S.set(rh=figspace(at[1], (hold[0] - .55, hold[1] + .42, hold[2] + .05)), rhand='relax', rfing=(.2, -.15, 1), rpalm=(0, -1, 0), rel=(-1, -.6, -.4)), k); S = S.set(pel=(S.pel[0], S.pel[1] - .55 * dip, S.pel[2] + .25 * dip), cher=(S.cher[0], S.cher[1] + 4 + 12 * dip, S.cher[2] + 4 * dip), hedr=(look, 9 + 6 * dip - 8 * smooth(94, 102, f), 0)); fs_ = Face(smile=.1, lid=.7, gy=-.5) if f < 94 else Face(smile=.4, lid=.95, gy=.1)
            g = smooth(94, 101, f); R = R.set(hedr=(lerp(R.hedr[0], look, g), lerp(R.hedr[1], -2, g), 0)); K = K.set(cher=(K.cher[0], K.cher[1] + 5, 0), lh=(.4, 10.0, 1.5), lhand='fist', lel=(1, -.8, 0))
        return (R, fr, at[0]), (S, fs_, at[1]), (K, fk, at[2])

    def season(self, st, s, f):
        t = f / 24.; X = gx(f); cx = X + lerp(*LEAD, f / 107.); au = s == 'autumn'
        cam = Cam((cx, 8.6, 66), (cx, 9.75 if not au else 7.9, 0), 22.5); st.cam = cam
        warm = smooth(95, 106, f) if s == 'winter' else 0.
        st.paint('sky.frag', **FO.sky(s))
        kw = dict(spring=dict(key=(-.6, .62, .5), rim=(.6, .5, -.6), rimCol=(.55, .5, .36)), monsoon=dict(key=(-.3, .8, .5)), autumn=dict(key=(-.88, .27, .34), keyCol=(1.55, 1.12, .66), rim=(-.8, .35, -.6), rimCol=(1.5, .85, .3), amb='#a88a9c'), winter=dict(key=(-.5, .5, .6), amb='#a4aed0'))[s]
        L = FO.light(s, **kw)
        if warm: L.pts = [((cx + 15.5, 7.5, 6.), 15., tuple(warm * v for v in (1.15, .52, .16)))]; L.keyCol = tuple(np.array(hexc(L.keyCol)) * (1 - .28 * warm)); L.rim = (.9, .2, -.2); L.rimCol = tuple(np.array([1.6, .72, .22]) * warm + np.array(hexc(L.rimCol)) * (1 - warm))
        st.open(cam, L); FO.track(st, s, cx - 30, cx + 30, seed=dict(spring=1, monsoon=4, autumn=2, winter=1)[s])
        if s == 'spring':
            FL.tree(st, 'pahari_round', (30.5, 0, -24), 50, season='spring', seed=1); pz = (21.0, 0, -8.5); birds.peacock(st, at=pz, yaw=-62, scale=.86, fan=.25 + .75 * smooth(0, 16, f), t=t, head=(-18 + 20 * math.sin(t * 2), 0))
        if s == 'monsoon':
            FL.tree(st, 'banyan', (35., -.4, -17), 46, season='monsoon', seed=0); w = math.sin(t * 2.2)
            deer.draw(st, deer.ALERT.set(head=(38., 12., 0), neck=(40., 74., 12.), ears=(1, .4 + .5 * w)), at=(32.5, 0, -11), yaw=-62, scale=.80, fig=PLAIN); deer.draw(st, deer.graze(.9 + .1 * w), at=(38.5, 0, -13), yaw=70, scale=.74, fig=PLAIN)
        if au: quad(st, self.boat, (46.0, .9, 3.6), 10.5, 3.5)
        W3 = self.poses(f, s); wind = dict(spring=(-.45, .0, .1), monsoon=(-.25, -.2, 0), autumn=(-.85, .10, .1), winter=(-.75, -.05, 0))[s]; out = []
        for (P, face, at), fig in zip(W3, (rama.EXILE, sita.FOREST, rama.LAKSHMANA)): out.append(st.fig(fig, P, at=at, yaw=90, face=face, u=dict(Wind=(0, 0, wind[0] * .9))))
        SR, SS, SK = out; quiver(st, SR); back_bow(st, SR); quiver(st, SK); held_bow(st, SK, 'R', up=(.10, 1, .1), fwd=(1, -.1, .25))
        if s != 'winter':
            for who, i, fig in (('rama', 0, rama.EXILE), ('lak', 2, rama.LAKSHMANA)):
                base = W3[i][0]
                def at_time(tt, i=i, fig=fig, base=base): g = tt * 24; P = stride_pose(g / 18.); return st.fig(fig, base.set(pel=P.pel, pelr=P.pelr, cher=(base.cher[0], P.cher[1], P.cher[2])), at=(gx(g) + OFF[s][i], 0, W3[i][2][2]), yaw=90, draw=False)
                sashes(st, at_time, t, who, wind=wind, wave=.55 if s != 'autumn' else .9, k=.8 if s == 'monsoon' else 1., grav=.75 if s == 'monsoon' else .5)
        else:
            shawl(st, SS, t, r=1.62, length=5.6, col=('#a8343c', '#4c1424', '#f0c46a'), wind=wind, open_=40., kind=1); shawl(st, SR, t, r=2.05, length=4.6, col=('#c88a3c', '#6a3a1c', '#7a2a1c'), wind=wind, open_=66., top=1.15); shawl(st, SK, t + .4, r=2.05, length=4.9, col=('#e4dccb', '#8a829a', '#8a2430'), wind=wind, open_=58., top=1.15)
        leafc = None
        if s == 'monsoon':                                                       # one great leaf on its stalk, over the two of them
            h = SR.palm('L', 0, .6, .3); k = keys(f, [(24, 0.), (28, -.06), (35, 1.06, 'io'), (38, 1.)]); tip = h + V(lerp(-2.6, -2.1, k), lerp(1.2, 4.1, k), 1.3); tilt = lerp(-.75, .05, k) + .05 * math.sin(t * 9); tx = V(math.cos(tilt), math.sin(tilt), 0); up = V(-math.sin(tilt), math.cos(tilt), .0); leafc = (tip, tx, up)
            st.mesh(*CL.tube(CL.spline([h - V(.15, 1.1, 0), h, h + (tip - h) * .55 + V(.35, .2, 0), tip], 16), [.13, .10], m=8), kind=0, col=('#5a8a3a', '#24481e', '#c0d070'), cls=1)
            fl = lambda u, v: tip + tx * ((u - .5) * 10.4) + V(0, 0, 1) * ((v - .5) * 6.4) + up * (.55 - 2.3 * (u - .5) ** 2 * 1.9 - 1.9 * (v - .5) ** 2 + .10 * math.sin(t * 15 + u * 9) * abs(u - .5))
            P, N, UV, I = CL.sheet(fl, 22, 14); st.mesh(P, N, UV, I, kind=3, col=((1.9, 1.9, 1.3), (.5, .5, .55), (1, 1, 1)), cls=6, ink=.6, texs=dict(tCard=FL.plate_of('lotus_leaf', 'monsoon', 0).tex), u=dict(cutoff=.4))
        st.close()
        # ------------------------------------ light and weather
        if s == 'spring': shafts(st, (260, -420), .34, '#ffe9b0', 62, 150, dens=8., seed=2., wid=1.1)
        if au: shafts(st, (-500, 60), .60, '#ffcf70', 60, 160, dens=10., seed=5., wid=1.2)
        e = cam.eye; box = (e + V(-24, -10, -84), e + V(24, 16, -46))
        if s == 'monsoon':
            FO.drift(st, s, 150, (e + V(-26, -10, -120), e + V(26, 18, -24)))
            for i, (P, _, at) in enumerate(W3):                                 # a splash where each foot comes down
                for k in range(3, 6):
                    f0 = 9 * k
                    if 0 <= f - f0 < 9: left = (k % 2 == 0) != (i == 1); FX.burst(st, 30, V(gx(f0) + OFF[s][i] + 3.3, .25, at[2] + .9), (f - f0) / 24., speed=9.5, grav=34, size=.19, seed=k * 3 + i, col='#cfe6e0', kind='drop', life=.40, up=1.0, spread=(1.1, .7, .5))
            tip, tx, up = leafc; r = np.random.default_rng(4); n = 26; u = r.uniform(-1, 1, n); ph = (t * 1.9 + r.uniform(0, 1, n)) % 1.; Pd = tip + np.outer(u * 4.6, tx) + np.outer(np.where(r.uniform(0, 1, n) > .5, 1, -.6) * 2.4 * np.sqrt(np.maximum(.1, 1 - u * u)), V(0, 0, 1)); Pd[:, 1] -= .5 + 1.2 * np.abs(u) ** 2 + 12. * ph * ph; FX.particles(st, Pd, .13, '#dff0ea', 'drop', alpha=np.clip(1.4 - ph * 1.4, 0, 1))
            sp = tip + up * .5 + np.outer(r.uniform(-4.4, 4.4, 14), tx) + V(0, .2, .6); q = (t * 4 + r.uniform(0, 1, 14)) % 1.; FX.particles(st, sp + np.c_[0 * q, q * .7, 0 * q], .16 * (1 - q), '#e8f6f0', 'dot', alpha=.7 * (1 - q))
        elif s == 'winter':
            FO.drift(st, s, 90, box)
            for i, S in enumerate((SR, SS, SK)):                                # breath, once a step pair
                for b in range(4):
                    age = (f - (80 + 18 * b + 5 * i)) / 24.
                    if 0 < age < .85: m = S.head((0, 0, 0)) + V(1.55 + 1.6 * ease_out(age / .85) - V_ * 24 * age * .16, -.45 + .7 * age, .3); FX.particles(st, np.array([m, m + V(.35, .15, 0), m - V(.3, -.1, 0)]), np.array([.30, .23, .19]) * (1 + 2.0 * age), (1.5, 1.55, 1.7), 'smoke', alpha=.42 * (1 - age / .85))
        else: FO.drift(st, s, 46 if au else 60, box)
        if s == 'spring':                                                        # the blossom bough she reaches for
            hit = decay((f - 12) / 24., 4.) * math.sin((f - 12) * .9) * (f >= 12); B = V(21.2, 20.1, 1.2); x, y, _ = cam.project(B); FL.frame(st, 'blossom_branch', x, y, .44, 'spring', 0, rot=-17 + 1.8 * hit + .6 * math.sin(t * 2), flip=True)
            for q, a in ((12, V(gx(12) + .9, 15.2, 1.4)), (15, V(gx(15) + .9, 15.3, 1.4))):
                if f >= q: tt = (f - q) / 24.; FX.burst(st, 14, a, tt, speed=2.4, grav=1.7, size=.19, seed=q, col='#f6b0c0', kind='petal', life=1.6, up=.2, drag=2.)
        if au:
            _, y0, _ = cam.project(V(cx, 0, 3.4)); water(st, y0, cx * cam.px(V(cx, 0, 9)), deep='#4a5a58', sheen='#ffd890', sq=1.9)
            for i in range(5): r = np.random.default_rng(i); xw = 8 + 11.5 * i + r.uniform(-2, 2) + 10; x, y, _ = cam.project(V(xw, -.6, 8.4 + 1.6 * r.uniform())); FL.frame(st, 'rock', x, y, .13 + .05 * r.uniform(), 'autumn', i, tint=(.75, .62, .55))
        foreground(st, s, cx - 40, cx + 40, seed=dict(spring=9, monsoon=11, autumn=14, winter=9)[s], keep_=.4 if au else .6, low=-7.3 if au else -6.2)
        if warm: st.post_paint('in vec2 uv;out vec4 o;uniform sampler2D tex;uniform float k;void main(){vec3 c=texture(tex,uv).rgb;float l=smoothstep(1.15,.35,uv.x+.15*uv.y);o=vec4(c*mix(vec3(1.),mix(vec3(.78,.64,.60),vec3(.33,.34,.52),l),k),1);}', k=float(warm)); st.paint('in vec2 uv;out vec4 o;uniform vec2 res;uniform float k;void main(){vec2 q=(uv-vec2(1.03,.40))*vec2(res.x/res.y,1.);float r=length(q);o=vec4(vec3(1.,.50,.14)*(exp(-r*r*3.6)*1.0+exp(-r*2.6)*.22)*k,0.);}', 'add', k=float(warm * (.72 + .05 * noise1(t * 8, 2))))

    def frame(self, f, st):
        st.clear('#000', f=f); i = sum(f >= c for c in CUT); s = SEASON[i]
        near = next((c for c in CUT if abs(f + .5 - c) < 8), None); vpx = 225.
        if near is None: self.season(st, s, f)
        else:
            cx = 960 - (f + .5 - near) * vpx; j = CUT.index(near); a, b = SEASON[j], SEASON[j + 1]; lean = .05 * (-1) ** j
            if cx >= 1920 + 60: self.season(st, a, f)
            elif cx <= -60: self.season(st, b, f)
            else: self.season(st, a, f); tex = keep(st, self.old); st.clear('#000', f=f); self.season(st, b, f); join(st, tex, cx, lean)
            rim = dict(monsoon='#5a7a6c', autumn='#c87828', winter='#aab4cc')[b]; trunk(st, cx, b, wide=1380., blur=vpx * .5, lean=lean, shade=.95, rim=rim, y=200. * j)
        ex = dict(spring=1.0, monsoon=1.05, autumn=1.0, winter=.92)[s]
        return st.finish(bloom=.38, thr=.92, vig=.36, contrast=1.05, expo=ex, fade=1 - smooth(-1, 4, f), fadeCol='#0a0506')
