"""War chariots and Pushpaka.

    from chars import vehicles as VH
    C = VH.chariot(st, 'rama'|'ravana', at=(0, 0, 0), yaw=90, t=f / 24, speed=1.)      # horses, chariot, umbrella, banners, reins
    st.fig(rama.PRINCE, PZ.archer(1.), M=C.stand)                                       # C.stand = world matrix of the platform (figure units, faces forward)
    C.w((x, y, z)) ...  C.reins()  C.p('banner'|'driver'|'prow')
    P = VH.pushpaka(st, at=(0, 80, 0), yaw=.., pitch=.., roll=.., mood=0., lamps=1.)      # P.deck = matrix of the fore deck, P.w(..) in vehicle units (1 unit = 6)"""
import numpy as np, math, cairo
from lau.stage import Fig, model, hexc
from lau.rig import V, nz, Rx, Ry, Rz
from lau import cloth as CL
from lau.plates import plate, rgb, blob, ink, smooth_path
from chars import horse as HR
from chars.jatayu import xform, join

GOLD = ('#ffffff', '#805030', 2)
RAMA = Fig('chariot_rama', 'vehicles.glsl', {3: GOLD, 4: ('#c4142c', '#54081c', 3), 5: ('#0f8a66', '#063a34', 3), 6: ('#f6f2e4', '#a8a2c0', 8), 7: ('#8a96a8', '#2c3444', 7), 9: ('#8a4a22', '#3c1c12', 1), 10: ('#f6e2d0', '#a87a86', 8), 11: ('#f6efe0', '#a89aa8', 8), 12: ('#ff8030', '#ff8030', 4), 13: ('#fff6e0', '#a89ab0', 8), 14: ('#fdf8ec', '#b0a6c0', 8)}, human=False, step=.82, bound=(0, 13.5, 5.5, 22.5), defs='#define KIND 0', u=dict(wheel=0., canopy=1., mood=0., lamps=1., glow=0.))
RAVANA = Fig('chariot_ravana', 'vehicles.glsl', {3: ('#f6d6a0', '#6a3c20', 2), 4: ('#e01c28', '#5a0412', 3), 5: ('#0f6a5a', '#04282a', 3), 6: ('#c8b8a0', '#5a4a5a', 8), 7: ('#4a4650', '#101018', 7), 9: ('#2a1c22', '#0c080e', 1), 10: ('#3c1420', '#14060e', 8), 11: ('#221620', '#0a060c', 8), 12: ('#ff6020', '#ff6020', 4), 13: ('#f0e0c0', '#8a7a8a', 8), 14: ('#1c1018', '#080408', 8)}, human=False, step=.82, bound=(0, 14.5, 5.5, 23.5), defs='#define KIND 1', u=dict(wheel=0., canopy=1., mood=0., lamps=1., glow=0.))
PUSH = Fig('pushpaka', 'vehicles.glsl', {3: GOLD, 4: ('#d81838', '#54081c', 3), 5: ('#12a074', '#063a34', 3), 6: ('#f6f2e4', '#a8a2c0', 8), 9: ('#b5482a', '#4a1820', 1), 10: ('#fff6e4', '#8a5a40', 2), 11: ('#f6ead2', '#a08498', 1), 12: ('#ffb050', '#ffb050', 4), 13: ('#f0a0a8', '#7a3048', 8), 14: ('#fbe4d0', '#a86a78', 8), 15: ('#fbf6ec', '#9a9ac0', 8), 16: ('#f0802c', '#8a3214', 8), 17: ('#f2dcc0', '#94708a', 1), 18: ('#f6e4c8', '#94708a', 1)}, human=False, step=.85, bound=(0, 2.6, .6, 11.2), defs='#define KIND 2', u=dict(wheel=0., canopy=1., mood=0., lamps=1., glow=0.))


# ------------------------------------------------------------------ banners (painted once)
def _banner(kind):
    def fn(c):
        W, H = 1024, 512; base, edge, art = dict(rama=('#e8862a', '#b3202a', '#fff0c0'), ravana=('#1c0e16', '#8a1220', '#f0b040'), saffron=('#e8862a', '#b3202a', '#ffe6a0'))[kind]
        c.set_source_rgb(*rgb(base)); c.rectangle(0, 0, W, H); c.fill(); c.set_source_rgb(*rgb(edge))
        for y in (0, H - 62): c.rectangle(0, y, W, 62); c.fill()
        c.set_source_rgb(*rgb(art))
        for y in (70, H - 78): c.rectangle(0, y, W, 8); c.fill()
        for i in range(26):
            for y in (31, H - 31): c.arc(20 + i * 40, y, 11, 0, 7); c.fill()
        cx, cy = 400, 256
        if kind == 'rama':                                               # the sun of the solar house, with an eagle's wings
            for i in range(20):
                a = i / 20 * 6.283; r0, r1 = 92, 150 if i % 2 == 0 else 124; c.move_to(cx + r0 * math.cos(a - .10), cy + r0 * math.sin(a - .10)); c.line_to(cx + r1 * math.cos(a), cy + r1 * math.sin(a)); c.line_to(cx + r0 * math.cos(a + .10), cy + r0 * math.sin(a + .10)); c.fill()
            c.arc(cx, cy, 86, 0, 7); c.fill(); c.set_source_rgb(*rgb(edge)); c.arc(cx, cy, 72, 0, 7); c.set_line_width(5); c.stroke()
            for s in (1, -1):
                c.arc(cx + s * 26, cy - 12, 9, 0, 7); c.fill()
                for k in range(6):
                    y = cy - 40 + k * 26; blob(c, [(cx + s * 150, y), (cx + s * 260, y - 62 + k * 10), (cx + s * (400 - k * 34), y - 70 + k * 16), (cx + s * (330 - k * 24), y - 12 + k * 6), (cx + s * 200, y + 16)], art if k % 2 == 0 else '#ffd27a', line=4, lcol=edge)
            blob(c, [(cx - 14, cy + 4), (cx + 14, cy + 4), (cx + 4, cy + 34), (cx - 4, cy + 34)], edge)
        elif kind == 'ravana':                                           # the veena
            c.save(); c.translate(cx + 40, cy); c.rotate(-.32); c.set_source_rgb(*rgb(art)); c.rectangle(-260, -12, 520, 24); c.fill()
            for x, r in ((-200, 84), (190, 70)): c.arc(x, 46, r, 0, 7); c.fill(); c.set_source_rgb(*rgb(edge)); c.arc(x, 46, r - 16, 0, 7); c.set_line_width(5); c.stroke(); c.set_source_rgb(*rgb(art))
            for i in range(18): c.set_source_rgb(*rgb(edge)); c.rectangle(-210 + i * 24, -18, 6, 36); c.fill()
            c.set_source_rgb(*rgb(art)); c.arc(285, -10, 34, 0, 7); c.fill(); c.set_line_width(3)
            for k in range(4): c.move_to(-250, -20 - 5 * k); c.line_to(270, -20 - 5 * k); c.stroke()
            c.restore()
            for i in range(9): x = 740 + (i % 3) * 70; y = 160 + (i // 3) * 96; c.set_source_rgb(*rgb('#c01c24')); c.arc(x, y, 18, 0, 7); c.fill()
        else:
            c.arc(cx, cy, 90, 0, 7); c.fill()
    return plate('banner_' + kind, 1024, 512, fn, ver=3)


def banner(st, kind, root, t, L=12., H=5., dirn=(0, 0, -1), amp=1., seed=0., tails=True):
    """a painted banner flying from a staff: root = top of the hoist (world), dirn = where it streams"""
    d = nz(dirn); s = nz(np.cross(d, V(0, 1, .001))); n = 26; u = np.linspace(0, 1, n); P = np.asarray(root, float) + d * (u * L)[:, None] * 1. + s * (amp * .085 * L * np.sin(u * 7. - t * 8. + seed) * u ** .8)[:, None] + V(0, 1, 0) * (-.06 * L * u ** 2 + .035 * L * np.sin(u * 5 - t * 6 + seed) * u)[:, None]
    q = []
    for j in range(7): v = j / 6; q.append(P + V(0, -1, 0) * (H * v * (1 - .45 * u))[:, None] + s * (amp * .03 * L * np.sin(u * 9 - t * 8 + v * 2.2 + seed) * u)[:, None])
    G = np.array(q); pos = G.transpose(1, 0, 2); du = np.gradient(pos, axis=0); dv = np.gradient(pos, axis=1); N = np.cross(du, dv); N /= np.linalg.norm(N, axis=2, keepdims=True); uv = np.stack(np.meshgrid(u, 1 - np.arange(7) / 6, indexing='ij'), -1); i = (np.arange(n - 1)[:, None] * 7 + np.arange(6)[None]).reshape(-1)
    st.mesh(pos.reshape(-1, 3), N.reshape(-1, 3), uv.reshape(-1, 2), np.concatenate([np.stack([i, i + 7, i + 1], 1), np.stack([i + 1, i + 7, i + 8], 1)]), kind=3, col=('#ffffff', '#8a6a86', '#ffffff'), cls=8, ink=.9, texs=dict(tCard=_banner(kind)))


def pennon(st, root, t, L=3., w=.6, dirn=(0, 0, -1), col=('#c42a2a', '#6a0f22', '#f2c24a'), seed=0.):
    d = nz(dirn); s = nz(np.cross(d, V(0, 1, .001))); u = np.linspace(0, 1, 12); P = np.asarray(root, float) + d * (u * L)[:, None] + (s + V(0, .5, 0)) * (.12 * L * np.sin(u * 6 - t * 9 + seed) * u)[:, None]
    st.mesh(*CL.strip(P, [w, w * .7, .03], up=(0, 1, 0), m=3), kind=1, col=col, cls=8, ink=.85)


# ------------------------------------------------------------------ chariots
class Chariot:
    def __init__(s, M, stand, horses): s.M, s.stand, s.horses = M, stand, horses; s.Sc = float(np.linalg.norm(M[:3, 0]))

    def w(s, p):
        """a point of the car (modelled units: floor at y = 6.6, wheels radius 5) -> world"""
        return s.M[:3, :3] @ (np.asarray(p, float) * CAR) + s.M[:3, 3]

    def d(s, v): return nz(s.M[:3, :3] @ np.asarray(v, float))

    def p(s, n): return s.w(dict(prow=(0, 12, 5.6), driver=(0, 6.6, 3.2), banner=(3.6, 28, -5.2), axleL=(7.5, 5, 0), axleR=(-7.5, 5, 0), wheelL=(6.1, 0, 0), wheelR=(-6.1, 0, 0), umbrella=(0, 23, -4.8))[n])


WHEEL_R, CAR = 5., 1.3              # the car is modelled at 1 and drawn at 1.3
_OFF = {2: (-4.8, 4.8), 3: (-9., 0., 9.), 4: (-13.6, -4.8, 4.8, 13.6)}


def chariot(st, kind='rama', at=(0, 0, 0), yaw=0., t=None, speed=1., pitch=0., roll=0., scale=1., M=None, horses=2, canopy=True, phase=None, reins_to=None, gait=None, bump=1., flags=True, dist=None, team=True):
    """draws the team, the chariot, umbrella, banners and traces; returns a Chariot.
    speed 0..1.2 (1 = full gallop, 2.2 strides a second); dist = ground covered in world units (turns the wheels; default from t and speed); phase = gallop phase of the first horse"""
    t = st.t if t is None else t; Mb = model(at, yaw, pitch, roll, scale) if M is None else np.asarray(M, float); rate = 2.2; ph = t * rate if phase is None else phase; v = HR.GALLOP_DIST * rate * speed
    dist = v * t if dist is None else dist / scale; b = bump * min(1., speed); M0 = Mb; J = np.eye(4); J[:3, :3] = Rx(.9 * b * math.sin(ph * 12.6 + .5)) @ Rz(.7 * b * math.sin(ph * 9.1)); J[1, 3] = .16 * b * abs(math.sin(ph * 12.6)); Mc = M0 @ J
    fig = RAMA if kind == 'rama' else RAVANA; Kc = np.diag([CAR, CAR, CAR, 1.]); st.fig(fig, M=Mc @ Kc, u=dict(wheel=-dist / (WHEEL_R * CAR), canopy=1. if canopy else 0.))
    out = []; hk = {'rama': ('white',), 'ravana': ('demon',)}[kind]
    if team:
        for i, x in enumerate(_OFF[horses]):
            p = gait(i) if gait else HR.gallop(ph + .13 * i + (.5 if kind == 'ravana' else 0.) * (i % 2) * .3, 1 if x >= 0 else -1) if speed > .05 else HR.STAND.set(head=(8. * math.sin(t * .9 + i * 2), 44., 0.), ears=(.3, .1))
            H = HR.draw(st, p, M=M0 @ model((x, 0, 25. - .12 * abs(x)), 0, 0, 0, HR.SCALE), kind=hk[0], t=t + i * .21, speed=.15 + .75 * min(1., speed)); out.append(H)
        # yoke, traces and reins
        c = ('#8a4a22', '#3c1c12', '#f2c24a') if kind == 'rama' else ('#2a1c22', '#0c080e', '#b08040'); xs = _OFF[horses]; yk = np.array([M0[:3, :3] @ V(x, 12.6 - .008 * x * x, 30. - .05 * abs(x)) + M0[:3, 3] for x in np.linspace(min(xs) - 1.8, max(xs) + 1.8, 14)]); st.mesh(*CL.tube(yk, [.22, .38, .46, .38, .22], 10, 30), kind=0, col=c, cls=1, ink=.85)
        tr, rn = [], []; S = Chariot(Mc, None, out); hands = reins_to if reins_to is not None else [S.w((-.7, 11.4, 4.4)), S.w((.7, 11.4, 4.4))]
        for i, H in enumerate(out):
            for s in ('L', 'R'):
                a = H.p('girth' + s); tr.append(CL.tube(np.array([a, a * .5 + S.w((xs[i] * .3, 6., 8)) * .5 + V(0, -.5, 0), S.w((max(-3.8, min(3.8, xs[i] * .5)), 6., 5.2))]), .11 * scale, 6, 10))
                m = H.p('bit' + s); w = H.w((.75 if s == 'L' else -.75, 7.8, 1.2)); h = np.asarray(hands[0 if xs[i] < 0 else 1], float); rn.append(CL.tube(np.array([m, w, w * .45 + h * .55 + V(0, -1.2 * scale, 0), h]), .07 * scale, 5, 22))
        st.mesh(*join(tr), kind=0, col=c, cls=1, ink=.8); st.mesh(*join(rn), kind=0, col=('#c42a2a', '#5a0f1c', '#fff') if kind == 'rama' else ('#8a1420', '#2a0610', '#fff'), cls=8, ink=.7)
    C = Chariot(Mc, Mc @ model((0, 6.62 * CAR, -.6)), out)
    if flags:
        back = C.d((0, 0, -1)); wd = nz(back * (.25 + speed) + V(0, -.12, 0) + C.d((.35, 0, 0)) * (1 - min(1, speed)))
        banner(st, kind, C.w((3.6, 28.2, -5.2)), t, 15. * scale, 7. * scale, wd); pennon(st, C.w((0, 26.6 if kind == 'rama' else 29.6, -4.8)), t, 8. * scale, 1.8 * scale, wd, col=('#c42a2a', '#6a0f22', '#f2c24a') if kind == 'rama' else ('#1c0e16', '#08040a', '#b02020'), seed=2.)
        # tassels of the wall
        for i, x in enumerate((-3.2, 3.2)): pennon(st, C.w((x, 10.6, -3.8)), t, 3.2 * scale, .8 * scale, wd, col=('#1f5a9a', '#0c2a5a', '#f2c24a') if kind == 'rama' else ('#6a0c16', '#24040a', '#b08040'), seed=i + .5)
    return C


# ------------------------------------------------------------------ Pushpaka
class Push:
    def __init__(s, M): s.M = M; s.Sc = float(np.linalg.norm(M[:3, 0])); k = np.eye(4); k[:3, :3] /= s.Sc; s.deck = M @ model((0, .26, 4.9)) @ k; s.aft = M @ model((0, .26, -5.4)) @ k

    def w(s, p): return s.M[:3, :3] @ np.asarray(p, float) + s.M[:3, 3]

    def d(s, v): return nz(s.M[:3, :3] @ np.asarray(v, float))

    def p(s, n): return s.w(dict(prow=(0, 3.4, 9.4), dome=(0, 8.3, -.4), keel=(0, -4.2, 0), stern=(0, 3, -8.5), gate=(0, 1.5, 4.4), deck=(0, .26, 5.2))[n])

    def lamps(s, n=22):
        """world points of the lamps at the waist, for FX.flame / particles / Light.pts"""
        a = (np.arange(n) + .5) / n * 2 * np.pi; return np.array([s.w((4.2 * math.sin(x), -.55, 4.2 * 1.72 * math.cos(x))) for x in a])


def pushpaka(st, at=(0, 0, 0), yaw=0., pitch=0., roll=0., scale=6., M=None, mood=0., lamps=1., glow=0., t=None, flags=True, wind=1., u=None):
    """the flower chariot; about 20 x 10 x 13 units at scale 1 (120 long at 6).  mood 0 benign .. 1 Ravana's; lamps = brightness of windows and lamps, glow 0..1 = how much their light warms the vessel (use 1 at night)"""
    M = model(at, yaw, pitch, roll, scale) if M is None else np.asarray(M, float); t = st.t if t is None else t; P = Push(M); Sc = P.Sc
    st.fig(PUSH, M=M, u=dict(mood=float(mood), lamps=float(lamps), glow=float(glow), **(u or {})))
    if flags:
        wd = nz(P.d((0, 0, -1)) * wind + V(0, -.1, 0) + P.d((.3, 0, 0)) * .2); cs = [('#e8862a', '#8a3a1a', '#fff0c0'), ('#c42a2a', '#6a0f22', '#f2c24a')] if mood < .5 else [('#5a0c16', '#1c040a', '#c86a2a'), ('#1c1018', '#08040a', '#a01c1c')]
        k = 0
        for x, z in ((1.72, 2.75), (-1.72, 2.75), (1.72, -3.55), (-1.72, -3.55)): pennon(st, P.w((x, 6.2, z)), t, 2.6 * Sc, .55 * Sc, wd, cs[k % 2], k * 1.3); k += 1
        pennon(st, P.w((0, 8.6, -.4)), t, 4.2 * Sc, .85 * Sc, wd, cs[0], .7)
        for sg in (1, -1):                                        # long streamers from the stern
            for i in range(2):
                r = P.w((sg * (1.2 + 1.1 * i), .3, -6.5 + .5 * i)); uu = np.linspace(0, 1, 18); L = (7. - 1.2 * i) * Sc; q = r + wd * (uu * L)[:, None] + P.d((1, 0, 0)) * (sg * .10 * L * uu * np.sin(uu * 4 - t * 4 + i + sg))[:, None] + V(0, 1, 0) * (.09 * L * np.sin(uu * 5 - t * 5 + i * 2 + sg) * uu - .12 * L * uu ** 2)[:, None]
                st.mesh(*CL.strip(q, [.5 * Sc, .62 * Sc, .5 * Sc, .1 * Sc], up=P.d((0, 1, .2)), m=4, twist=1.2 * sg), kind=2, col=cs[(i + 1) % 2], cls=8, ink=.85, u=dict(rep=(26., 5., 0., 0.)))
    return P


def garland(st, A, B, sag=1., n=40, r=.2, col=('#f0a030', '#8a4a14', '#fff0c0'), cls=1):
    """a swag of marigolds between two world points"""
    u = np.linspace(0, 1, n)[:, None]; P = np.asarray(A, float) * (1 - u) + np.asarray(B, float) * u + V(0, -1, 0) * sag * 4 * u * (1 - u); st.mesh(*CL.tube(P, r * (1 + .25 * np.sin(np.arange(n) * 2.2)), 8), kind=0, col=col, cls=cls, ink=.8)
