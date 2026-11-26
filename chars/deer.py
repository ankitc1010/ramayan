"""The golden deer of Maricha, and the four-legged rig (Quad) that the horses share.

    from chars import deer
    S = deer.draw(st, deer.STAND, at=(0, 0, 0), yaw=90)                  # faces +x
    S = deer.draw(st, deer.leap(t), at=..., yaw=90, burn=.4)             # t 0..1, travels deer.LEAP_DIST units forward on its own
    S.p('head'), S.p('eyeL'), S.p('chest'), S.w((x, y, z))               # world points for effects

Figure space as everywhere: y up, faces +z, its left is +x, hooves at y = 0.  Height at the crown about 11 units, antler tips about 14."""
import numpy as np, math, cairo
from dataclasses import dataclass, replace, fields
from lau.stage import Fig, hexc
from lau.rig import V, nz, Rx, Ry, Rz, eul, ik2
from lau.face import Face, Pen, rgb


# ------------------------------------------------------------------ interpolation
def track(x, K, period=None):
    """monotone cubic through K = [(x, v)] (v number or tuple); with `period` the track is cyclic.  Never overshoots its keys."""
    X = np.array([k[0] for k in K], float); Y = np.array([np.atleast_1d(k[1]) for k in K], float)
    if period:
        X = np.concatenate([X[-2:] - period, X, X[:2] + period]); Y = np.vstack([Y[-2:], Y, Y[:2]]); x = x % period
    x = min(max(x, X[0]), X[-1]); h = np.diff(X); d = np.diff(Y, axis=0) / h[:, None]; m = np.zeros_like(Y)
    m[0], m[-1] = d[0], d[-1]
    if len(X) > 2:
        a, b = d[:-1], d[1:]; w1, w2 = (2 * h[1:] + h[:-1])[:, None], (h[1:] + 2 * h[:-1])[:, None]
        with np.errstate(divide='ignore', invalid='ignore'): hm = (w1 + w2) / (w1 / a + w2 / b)
        m[1:-1] = np.where(a * b > 0, hm, 0)
    i = int(np.clip(np.searchsorted(X, x, 'right') - 1, 0, len(h) - 1)); t = (x - X[i]) / h[i]
    v = (2 * t ** 3 - 3 * t * t + 1) * Y[i] + (t ** 3 - 2 * t * t + t) * h[i] * m[i] + (3 * t * t - 2 * t ** 3) * Y[i + 1] + (t ** 3 - t * t) * h[i] * m[i + 1]
    return float(v[0]) if np.ndim(K[0][1]) == 0 else v


# ------------------------------------------------------------------ the four-legged rig
@dataclass
class QPose:
    """positions in the animal's rest units (scaled by the species), angles in degrees"""
    pos: tuple = (0, 0, 0)               # shift of the trunk from its standing place
    pitch: float = 0.                    # nose of the trunk up
    roll: float = 0.
    bend: float = 0.                     # + arches the back (hind quarters tucked under)
    turn: float = 0.                     # trunk bends sideways, head end to its left
    neck: tuple = (34., 66., 0.)         # rise of the lower neck, rise of the upper neck, yaw of the neck
    head: tuple = (0., 22., 0.)          # yaw (absolute, from the neck's 0), pitch (nose down), roll
    fl: tuple = (0, 0, 0)                # hoof offsets from the standing place: side, up, forward
    fr: tuple = (0, 0, 0)
    hl: tuple = (0, 0, 0)
    hr: tuple = (0, 0, 0)
    fold: tuple = (0., 0., 0., 0.)       # flexion of the pasterns (fl fr hl hr), 0 = standing on the hoof
    tail: tuple = (-35., 0.)             # rise of the tail, side swing
    ears: tuple = (0., 0.)               # + forward for each ear, - pinned back
    jaw: float = 0.
    travel: float = 0.                   # forward displacement of the whole figure

    def mix(s, o, t):
        d = {}
        for f in fields(s):
            a, b = getattr(s, f.name), getattr(o, f.name)
            d[f.name] = tuple((1 - t) * np.asarray(a, float) + t * np.asarray(b, float)) if isinstance(a, tuple) else (1 - t) * a + t * b
        return QPose(**d)

    def set(s, **k): return replace(s, **k)


@dataclass
class Build:
    """bone lengths and stations of a species"""
    hb: float = 6.05                     # height of the trunk axis
    L: float = 4.0                       # hip to chest station
    hip: tuple = (.56, .10, -.30)        # hip joint in the pelvis frame
    sh: tuple = (.58, -.75, .75)         # point of the shoulder in the chest frame
    el: tuple = (.02, -.62, -.95)        # shoulder -> elbow
    fore: float = 2.05; can: float = 1.72
    fem: float = 1.75; tib: float = 2.15; met: float = 2.15
    past: float = .62
    pa: float = 34.                      # pastern angle from the vertical, standing
    hoof: float = .16                    # height of the hoof's centre
    stF: tuple = (.56, .60)              # standing hoof x, z from the chest / hip station
    stH: tuple = (.62, -.75)
    n0: tuple = (0, .62, .62)            # neck root in the chest frame
    nl: tuple = (1.75, 1.80)             # neck segment lengths
    hd: tuple = (0, .12, .22)            # head centre from the end of the neck, head frame
    tl: tuple = (.75, .75)               # tail segments
    t0: tuple = (0, .62, -1.05)


LEGS = ('fl', 'fr', 'hl', 'hr')


def solve(P, B):
    """QPose -> joints J (40x3) and frames.  0 pelvis 1 chest 2 neck root 3 neck mid 4 neck top 5 head; legs from 6: shoulder elbow carpus fetlock hoof (hip stifle hock fetlock hoof), order fl fr hl hr; 26..28 tail; 29 withers"""
    J = np.zeros((40, 3)); R0 = Rz(-P.roll) @ np.eye(3)
    Rp = Ry(-P.turn * .5) @ Rx(-(P.pitch + P.bend)) @ R0; Rc = Ry(P.turn * .5) @ Rx(-(P.pitch - P.bend)) @ R0
    c = V(0, B.hb, 0) + np.asarray(P.pos, float) + V(0, 0, P.travel)
    J[0] = c + Rp @ V(0, 0, -B.L / 2); J[1] = c + Rc @ V(0, 0, B.L / 2)
    Rn = Ry(P.turn * .5 + P.neck[2]); g = lambda a: Rn @ V(0, math.sin(math.radians(a)), math.cos(math.radians(a)))
    J[2] = J[1] + Rc @ np.asarray(B.n0, float); J[3] = J[2] + g(P.neck[0] + P.pitch * .5) * B.nl[0]; J[4] = J[3] + g(P.neck[1] + P.pitch * .5) * B.nl[1]
    Rh = Ry(P.turn * .5 + P.neck[2] * .6 + P.head[0]) @ Rx(P.head[1]) @ Rz(-P.head[2]); J[5] = J[4] + Rh @ np.asarray(B.hd, float)
    for k, nm in enumerate(LEGS):
        sg = 1 if nm[1] == 'l' else -1; off = np.asarray(getattr(P, nm), float); b = 6 + 5 * k; fo = P.fold[k]
        fr = nm[0] == 'f'; st = B.stF if fr else B.stH
        H = V(sg * st[0], B.hoof, (B.L / 2 if fr else -B.L / 2) + st[1] + P.travel) + off * V(sg if False else 1, 1, 1)
        a = math.radians(B.pa - fo); pd = V(0, -math.cos(a), math.sin(a))          # direction fetlock -> hoof; folding swings it back
        F = H - pd * B.past
        if fr:
            gl = np.clip((H[2] - (J[1][2] + st[1])) / 4., -1, 1)                   # the shoulder blade glides with the reach
            s = J[1] + Rc @ (np.asarray(B.sh, float) * V(sg, 1, 1) + V(0, .22 * abs(gl), .42 * gl)); e = s + Rc @ Rx(-26 * gl) @ (np.asarray(B.el, float) * V(sg, 1, 1))
            m, F2 = ik2(e, F, B.fore, B.can, Rc @ V(sg * .04, .25, 1.)); J[b:b + 4] = s, e, m, F2
        else:                                                                       # femur and cannon stay parallel (stay apparatus): a 2-bone chain
            h = J[0] + Rp @ (np.asarray(B.hip, float) * V(sg, 1, 1)); m, F2 = ik2(h, F, B.fem + B.met, B.tib, Rp @ V(sg * .06, .1, 1.))
            u = nz(m - h); stf = h + u * B.fem; hk = stf + (F2 - m); J[b:b + 4] = h, stf, hk, F2
        J[b + 4] = F2 + pd * B.past
    t0 = J[0] + Rp @ np.asarray(B.t0, float); ta = P.tail[0] + P.pitch + P.bend
    for i in range(2):
        a = math.radians(180 - ta + 22 * i); J[26 + i] = t0 if i == 0 else J[27 + i - 1]
        J[27 + i] = J[26 + i] + Ry(P.tail[1]) @ V(0, math.sin(a), math.cos(a)) * B.tl[i]
    J[29] = J[1] + Rc @ V(0, 1., -.1)
    return dict(J=J, Bp=Rp.T, Bc=Rc.T, Bh=Rh.T)


class Beast:
    """what draw() returns: joints and world points"""

    def __init__(s, S, u, names, hs=1.16): s.S, s.u, s.Mf, s.Sc, s.names, s.J, s.hs = S, u, S.Mf, S.Sc, names, u['J'], hs

    def w(s, p): return s.S.w(p)

    def joint(s, i): return s.S.w(s.J[i])

    def head(s, p=(0, 0, 0)): return s.S.w(s.J[5] + np.asarray(p, float) * s.hs @ s.u['Bh'])

    def chest(s, p=(0, 0, 0)): return s.S.w(s.J[1] + np.asarray(p, float) @ s.u['Bc'])

    def pelvis(s, p=(0, 0, 0)): return s.S.w(s.J[0] + np.asarray(p, float) @ s.u['Bp'])

    def p(s, name):
        """named world point"""
        fr, q = s.names[name]; return {'h': s.head, 'c': s.chest, 'p': s.pelvis}[fr](q) if fr in 'hcp' else s.joint(fr)


# ------------------------------------------------------------------ gaits (offsets in deer units; a horse scales them)
STAND = QPose(fl=(0, 0, .18), fr=(0, 0, -.12), hl=(0, 0, -.20), hr=(0, 0, .25), ears=(.2, .2))
ALERT = STAND.set(neck=(44., 76., 0.), head=(0., 14., 0.), ears=(1., 1.), tail=(10., 0.))


def look(side=1, amt=1.):
    """standing, head turned to the watcher on its left (side=1) or right (-1)"""
    return STAND.mix(STAND.set(neck=(40., 74., 16. * side), head=(58. * side, 12., 4. * side), ears=(.9, .9), turn=4. * side), amt)


def graze(amt=1.):
    return STAND.mix(STAND.set(neck=(-48., -62., 8.), head=(0., 62., 0.), ears=(-.2, .3), pitch=-4., pos=(0, -.12, .05)), amt)


def _foot(ph, duty, stride, lift, fold):
    """(up, forward, fold) of one hoof; phase 0 = touch down"""
    ph %= 1.
    if ph < duty: q = ph / duty; return 0., stride * (.5 - q), 10. * max(0., q - .7) / .3
    q = (ph - duty) / (1 - duty); e = q * q * (3 - 2 * q)
    return lift * math.sin(math.pi * min(1., q * 1.05)) ** 1.2 * (1. - .25 * q), stride * (e - .5), fold * math.sin(math.pi * q ** .75)


def step(ph, stride=2.3, lift=.85):
    """a dainty four-beat walk (hl fl hr fr), one cycle per unit of phase; ground speed = stride / .62 per cycle (STEP_DIST)"""
    f = {n: _foot(ph - o, .62, stride, lift * (1.15 if n[0] == 'f' else .8), 75 if n[0] == 'f' else 55) for n, o in dict(hl=0., fl=.25, hr=.5, fr=.75).items()}
    s = math.sin(2 * math.pi * ph); b = math.cos(4 * math.pi * ph)
    return QPose(pos=(.10 * s, .05 * b, 0), roll=1.6 * s, turn=2.5 * s, neck=(36 + 3 * b, 66 + 3 * b, -2 * s), head=(0., 20 - 4 * b, 0.), tail=(-20 + 6 * b, 10 * s), ears=(.4, .1),
                 **{n: (0, v[0], v[1]) for n, v in f.items()}, fold=tuple(f[n][2] for n in LEGS))


STEP_DIST = 2.3 / .62


def _pose(x, T, period=None):
    """pose from a table of tracks"""
    k = {a: track(x, K, period) for a, K in T.items()}; d = dict(pos=(0, k.get('y', 0.), k.get('z', 0.)), pitch=k.get('pitch', 0.), bend=k.get('bend', 0.), neck=(*k['neck'], 0.), head=(0., k.get('head', 20.), 0.), tail=(k.get('tail', 0.), 0.), travel=k.get('travel', 0.))
    fo = []
    for n in LEGS: u, f, o = k[n]; d[n] = (0, u, f); fo.append(o)
    e = k.get('ears', 0.); return QPose(**d, fold=tuple(fo), ears=(e, e))


# the bounding gallop of a deer: hind pair together, a long extended flight, fore pair, a short gathered flight
_RUN = dict(
    y=[(0., -.30), (.12, -.35), (.30, .75), (.40, .62), (.52, -.25), (.62, -.30), (.80, .30), (.92, .10)], pitch=[(0., 5), (.16, 13), (.34, 4), (.50, -10), (.66, -9), (.85, -1)], bend=[(.02, 15), (.18, -4), (.34, -10), (.52, -4), (.78, 14), (.9, 19)],
    neck=[(0., (42, 66)), (.2, (26, 46)), (.36, (30, 50)), (.55, (46, 70)), (.75, (44, 68))], head=[(0., 24), (.3, 12), (.55, 30), (.8, 26)], tail=[(0., 40), (.3, 62), (.6, 34), (.85, 48)], ears=[(0., -.5), (.5, -.3)],
    hl=[(.0, (0, 2.3, 0)), (.11, (0, .4, 0)), (.22, (.05, -2.0, 18)), (.34, (1.5, -2.9, 82)), (.48, (1.7, -2.0, 100)), (.66, (1.5, .2, 84)), (.84, (1.2, 2.9, 30)), (.95, (.4, 2.8, 0))],
    hr=[(.03, (0, 2.6, 0)), (.14, (0, .6, 0)), (.25, (.05, -1.8, 18)), (.37, (1.5, -2.7, 82)), (.51, (1.7, -1.8, 100)), (.69, (1.5, .4, 84)), (.87, (1.2, 3.1, 30)), (.98, (.4, 3.0, 0))],
    fl=[(.42, (.2, 2.3, 0)), (.46, (0, 1.9, 0)), (.55, (0, .1, 0)), (.65, (.05, -2.0, 25)), (.76, (1.0, -2.3, 100)), (.92, (2.2, -.3, 125)), (.10, (2.4, .9, 118)), (.24, (2.1, 2.2, 62)), (.35, (1.4, 2.9, 12))],
    fr=[(.47, (.2, 2.7, 0)), (.51, (0, 2.3, 0)), (.60, (0, .4, 0)), (.70, (.05, -1.7, 25)), (.81, (1.0, -2.1, 100)), (.96, (2.2, .0, 125)), (.14, (2.4, 1.1, 118)), (.28, (2.1, 2.4, 62)), (.39, (1.4, 3.1, 12))])
_RUN['fl'].sort(); _RUN['fr'].sort()
RUN_DIST = 19.8


def run(ph): return _pose(ph % 1., _RUN, 1.)


LEAP_DIST, LEAP_H = 26., 6.2
_LEAP = dict(
    y=[(0., 0), (.10, -1.15), (.16, -1.25), (.24, .15), (.36, 4.1), (.50, 6.2), (.64, 4.2), (.75, .5), (.82, -.75), (.90, -.4), (1., 0)],
    travel=[(0., 0), (.12, -.35), (.18, .2), (.26, 3.2), (.50, 13.4), (.74, 22.8), (.84, 24.9), (1., 26.)],
    pitch=[(0., 0), (.12, -7), (.18, 6), (.26, 30), (.36, 23), (.50, 0), (.64, -22), (.74, -24), (.83, -5), (1., 0)],
    bend=[(0., 0), (.14, 16), (.22, 4), (.30, -7), (.50, -11), (.66, -2), (.80, 12), (1., 0)],
    neck=[(0., (40, 72)), (.12, (24, 46)), (.22, (46, 70)), (.36, (34, 58)), (.52, (30, 52)), (.70, (52, 74)), (.84, (34, 56)), (1., (40, 72))], head=[(0., 18), (.12, 30), (.24, 4), (.50, 14), (.70, 34), (.84, 22), (1., 18)],
    tail=[(0., 0), (.14, -20), (.26, 70), (.5, 50), (.75, 75), (1., 10)], ears=[(0., .8), (.15, -.4), (.5, -.6), (.8, .2), (1., .8)],
    hl=[(0., (0, -.2, 0)), (.05, (.35, .25, 24)), (.10, (0, .75, 0)), (.18, (0, .25, 0)), (.25, (.0, -2.25, 26)), (.33, (1.9, -3.2, 70)), (.42, (4.6, -3.9, 78)), (.52, (6.5, -4.6, 92)), (.62, (5.6, -3.0, 108)), (.72, (1.9, 1.0, 84)), (.79, (.5, 2.3, 24)), (.83, (0, 2.2, 0)), (.90, (0, 1.25, 0)), (.95, (.35, .5, 22)), (1., (0, -.2, 0))],
    hr=[(0., (0, .25, 0)), (.06, (.35, .65, 24)), (.10, (0, 1.05, 0)), (.18, (0, .55, 0)), (.26, (.0, -2.4, 26)), (.34, (2.0, -3.0, 70)), (.43, (4.8, -3.6, 80)), (.53, (6.9, -4.2, 96)), (.63, (5.9, -2.6, 110)), (.73, (2.0, 1.4, 84)), (.81, (.5, 2.5, 24)), (.85, (0, 2.3, 0)), (.92, (0, 1.6, 0)), (.965, (.3, .9, 18)), (1., (0, .25, 0))],
    fl=[(0., (0, .18, 0)), (.12, (0, .55, 0)), (.16, (.4, .9, 30)), (.23, (3.2, 1.3, 120)), (.32, (6.4, 1.6, 128)), (.42, (8.2, 2.8, 92)), (.52, (8.6, 3.6, 46)), (.62, (4.6, 3.1, 12)), (.71, (.3, 1.6, 0)), (.76, (0, .9, 0)), (.82, (0, -.6, 8)), (.87, (1.2, -1.2, 96)), (.94, (.6, .2, 50)), (1., (0, .18, 0))],
    fr=[(0., (0, -.12, 0)), (.12, (0, .25, 0)), (.16, (.5, .6, 34)), (.24, (3.6, 1.6, 124)), (.33, (6.8, 2.0, 130)), (.43, (8.6, 2.4, 118)), (.53, (9.0, 3.2, 70)), (.63, (4.9, 3.4, 16)), (.73, (.3, 1.9, 0)), (.78, (0, 1.2, 0)), (.85, (0, -.4, 8)), (.91, (1.1, -.8, 90)), (.97, (.3, .2, 30)), (1., (0, -.12, 0))])


def leap(t):
    """the full leap: gather (0-.18), launch (.18-.3), stretched apex (.5), fore landing (.72), recovery (1).  Moves LEAP_DIST forward and LEAP_H up on its own."""
    return _pose(min(max(t, 0.), 1.), _LEAP)


def struck(t):
    """hit in mid stride: rears and arches, knees fold, sinks"""
    t = min(max(t, 0.), 1.)
    return QPose(pos=(0, track(t, [(0, .2), (.25, 1.3), (.6, -.6), (1., -2.9)]), track(t, [(0, 0), (.3, -.7), (1., -.2)])), pitch=track(t, [(0, 4), (.25, 34), (.6, 6), (1., -10)]), bend=track(t, [(0, 0), (.25, -15), (.6, 6), (1., 9)]), roll=track(t, [(0, 0), (.4, -6), (1., -16)]),
                 neck=(*track(t, [(0, (40, 70)), (.25, (78, 112)), (.6, (40, 60)), (1., (2, 10))]), track(t, [(0, 0), (.3, -18), (1., 26)])), head=(track(t, [(0, 0), (.3, -20), (1., 20)]), track(t, [(0, 15), (.25, -34), (.6, 12), (1., 26)]), track(t, [(0, 0), (1., 18)])), ears=(-.8, -.9), tail=(track(t, [(0, 20), (.25, 70), (1., -50)]), 0), jaw=track(t, [(0, 0), (.2, .8), (.7, .5), (1., .2)]),
                 fl=(0, *track(t, [(0, (.0, .6)), (.25, (4.0, 2.0)), (.6, (.6, .4)), (1., (.0, -1.2))])), fr=(0, *track(t, [(0, (.6, .2)), (.25, (4.9, 1.4)), (.6, (.2, .6)), (1., (.0, 1.6))])), hl=(0, 0, track(t, [(0, 0), (.25, .9), (1., 1.9)])), hr=(0, 0, track(t, [(0, .4), (.25, .3), (1., 2.4)])),
                 fold=(track(t, [(0, 10), (.25, 120), (.6, 60), (1., 112)]), track(t, [(0, 40), (.25, 128), (.6, 30), (1., 70)]), track(t, [(0, 0), (1., 10)]), track(t, [(0, 0), (1., 20)])))


# ------------------------------------------------------------------ the deer itself
def _eye(F):
    """eye decal: eye-plane units (x toward the nose, y up), box -1..1; the same for both eyes"""
    P = Pen(1024, (-1.25, -1.25, 1.25, 1.25)); c = P.c; k = F.lid
    up = -.16 + .62 * k; eye = [(.74, -.14), (.52, .18 * k + up * .45 - .05, .30, up, -.02, up), (-.40, up, -.66, .16 + .12 * k, -.80, .10), (-.62, -.22, -.34, -.40, .02, -.40), (.34, -.40, .56, -.30, .74, -.14)]
    for w, a in ((.46, .35), (.36, .5), (.26, 1.)): P.path(eye, True); P.col('#fff3da', a); c.set_line_width(w); c.stroke()
    for w, a in ((.17, .35), (.12, .8), (.085, 1.)): P.path(eye, True); P.col('#1a0a12', a); c.set_line_width(w); c.stroke()
    # tear line and painted flick, as on a temple mural
    P.line([(.72, -.14), (.92, -.26, .98, -.40, 1.02, -.60)], .085, '#1a0a12'); P.line([(-.78, .12), (-.95, .20, -1.05, .26, -1.18, .24)], .07, '#1a0a12')
    if k > .08:
        P.fill(eye, '#2a1008'); c.save(); P.path(eye, True); c.clip(); ix, iy = F.gx * .24, .02 + F.gy * .14
        P.fill([(.80, -.2), (.66, .0, .60, .02, .57, -.04), (.60, -.16, .66, -.22, .80, -.2)], '#f7e6d0'); P.fill([(-.85, .12), (-.76, .16, -.70, .10, -.69, .04), (-.70, -.04, -.76, -.02, -.85, .12)], '#e8cdb8')
        g = cairo.RadialGradient(ix, iy - .22, .02, ix, iy, .56); g.add_color_stop_rgba(0, *rgb('#e8902c'), 1); g.add_color_stop_rgba(.45, *rgb('#8a3c12'), 1); g.add_color_stop_rgba(.8, *rgb('#3a1408'), 1); g.add_color_stop_rgba(1, *rgb('#140608'), 1); c.set_source(g); c.arc(ix, iy, .56, 0, 7); c.fill()
        for i in range(26):
            a = i / 26 * 6.283; P.line([(ix + .27 * math.cos(a), iy + .25 * math.sin(a)), (ix + .48 * math.cos(a), iy + .46 * math.sin(a))], .014, '#ffc46a', .35 if math.sin(a) < .3 else .08)
        P.col('#080306'); c.save(); c.translate(ix, iy + .02); c.scale(1.25, .95); c.arc(0, 0, .25 * F.pupil, 0, 7); c.fill(); c.restore()
        g = cairo.LinearGradient(0, up, 0, up - .46); g.add_color_stop_rgba(0, .04, .0, .05, .85); g.add_color_stop_rgba(1, .04, 0, .05, 0); c.set_source(g); c.rectangle(-1, -1, 2, 2); c.fill()
        if F.glow > 0:
            g = cairo.RadialGradient(ix, iy, 0, ix, iy, .56); g.add_color_stop_rgba(0, 1, .9, .5, F.glow); g.add_color_stop_rgba(.5, 1, .5, .1, F.glow); g.add_color_stop_rgba(1, 1, .2, .02, F.glow * .5); c.set_source(g); c.arc(ix, iy, .56, 0, 7); c.fill()
        P.col('#ffffff'); c.save(); c.translate(ix + .17, iy + .20); c.rotate(.5); c.scale(1.35, 1); c.arc(0, 0, .105, 0, 7); c.fill(); c.restore(); P.col('#ffe6b8', .95); c.arc(ix - .20, iy - .20, .055, 0, 7); c.fill(); P.col('#ffffff', .9); c.arc(ix + .02, iy + .30, .035, 0, 7); c.fill()
        c.restore()
    P.path(eye, True); P.col('#12060e'); c.set_line_width(.05); c.stroke()
    P.line([eye[0], eye[1], eye[2]], .115, '#12060e')                                 # heavy upper lid
    for i in range(11):                                                                # lashes sweep back
        u = i / 10; x = .30 - 1.06 * u; y = up * (1 - abs((x + .05) / .86) ** 2.4) * (1 if k > .3 else .6) + .02 + .10 * max(0., u - .6); L = .13 + .24 * u ** .8; w = .05
        a = math.radians(96 + 62 * u); P.path([(x + .03, y - .02), (x + .03 + math.cos(a - .5) * L * .6, y + math.sin(a - .5) * L * .6, x + math.cos(a) * L, y + math.sin(a) * L, x + math.cos(a + .25) * L * 1.5, y + math.sin(a + .25) * L * 1.35), (x + math.cos(a) * L * .7, y + math.sin(a) * L * .7, x, y + .05, x - w, y - .02)], True); P.col('#12060e'); c.fill()
    P.line([(.50, .34 + .2 * k + .10 * F.brow), (.2, .62 + .22 * k + .1 * F.brow, -.4, .62 + .2 * k, -.82, .36 + .14 * k)], .035, '#7a3a10', .8)
    return P.out()


def _antler():
    """main beam (8 points) and tines of the right antler, head space; x out"""
    from lau.cloth import spline
    beam = spline(np.array([(.17, .40, -.08), (.38, .85, -.45), (.86, 1.45, -.95), (1.16, 2.25, -.95), (.98, 3.05, -.42)]), 8)
    t1 = spline(np.array([beam[1] + V(.0, -.02, 0), (.40, .92, .14), (.40, 1.30, .48), (.36, 1.72, .52)]), 4)
    t2 = spline(np.array([beam[5], (1.34, 2.5, -1.2), (1.42, 2.85, -1.28), (1.36, 3.2, -1.2)]), 4)
    t3 = spline(np.array([beam[3], (1.02, 1.62, -.62), (1.16, 1.9, -.34), (1.20, 2.2, -.22)]), 4)
    return np.vstack([beam, t1, t2, t3])                                              # 8 + 4 + 4 + 4 = 20


PAL = {1: ('#fff0c8', '#8a4a1a', 2), 2: ('#fff8ea', '#c8a89a', 1), 3: ('#ffffff', '#805030', 2), 4: ('#d81838', '#54081c', 3), 5: ('#12a074', '#063a34', 3), 6: ('#f6f4ff', '#a8a2c8', 8), 7: ('#2e1c18', '#120a0c', 7), 8: ('#ffe9b4', '#8a5a2a', 2), 9: ('#e89a86', '#9a4a4a', 1), 10: ('#1a0e12', '#0a0508', 8), 11: ('#2456c8', '#0c1c5a', 3)}
DEER = Fig('deer', 'deer.glsl', PAL, face=_eye, human=False, step=.86, bound=(0, 6.5, .8, 8.8), u=dict(AT=_antler(), burn=0., burnAt=np.zeros(4), dark=0.))
BUILD = Build()
NAMES = dict(head=('h', (0, 0, 0)), nose=('h', (0, -.26, 1.75)), eyeL=('h', (.46, .06, .40)), eyeR=('h', (-.46, .06, .40)), crown=('h', (0, .6, 0)), antlerL=('h', (1.0, 3.05, -.4)), antlerR=('h', (-1.0, 3.05, -.4)), chest=('c', (0, -.4, 0)), heart=('c', (.8, -.5, -.2)), back=('c', (0, 1.2, -1.6)), rump=('p', (0, .8, -.6)), hfl=(10, 0), hfr=(15, 0), hhl=(20, 0), hhr=(25, 0))


def draw(st, pose=None, at=(0, 0, 0), yaw=0., pitch=0., roll=0., scale=1., face=None, burn=0., burn_at=None, dark=0., M=None, fig=None, u=None, shadow=True, draw=True):
    """draw the deer; burn 0..1 eats the gold away from figure-space point burn_at (x, y, z) outward (default: everywhere at once); dark 0..1 chars what is left"""
    p = pose or STAND; q = solve(p, BUILD); J = q['J']; c = (J[0] + J[1]) / 2 * .55 + J[5] * .45 * .6 + (J[0] + J[1]) / 2 * .18; R = max(np.linalg.norm(J[:29] - c, axis=1).max() + .6, np.linalg.norm(J[5] - c) + 4.3)
    ba = np.array([*(burn_at if burn_at is not None else (0, 0, 0)), 0. if burn_at is None else 1.]) + (np.zeros(4) if burn_at is None else np.array([0, 0, p.travel, 0]))
    U = dict(J=q['J'], Bp=q['Bp'], Bc=q['Bc'], Bh=q['Bh'], ear=np.array(p.ears, 'f4'), jaw=float(p.jaw), burn=float(burn), burnAt=ba, dark=float(dark), bound=np.append(c, R), **(u or {}))
    S = st.fig(fig or DEER, at=at, yaw=yaw, pitch=pitch, roll=roll, scale=scale, M=M, face=face or Face(), u=U, shadow=shadow, draw=draw)
    return Beast(S, q, NAMES)


def leaf(st, S, t, n=260, seed=5, speed=7., size=.16, life=1.3, col='#ffcf5a'):
    """gold leaf that bursts off the body at t = 0 (seconds), after close()"""
    from lau import fx as FX
    if t < 0: return
    r = np.random.default_rng(seed); k = r.uniform(0, 1, n)[:, None]; a = np.array([S.pelvis(), S.chest(), S.joint(3), S.head()]); i = np.minimum((k[:, 0] * 3).astype(int), 2); f = k * 3 - i[:, None]
    d = r.normal(size=(n, 3)); d /= np.linalg.norm(d, axis=1, keepdims=True); P = a[i] * (1 - f) + a[i + 1] * f + d * r.uniform(.5, 1.3, (n, 1)) * S.Sc
    sp = speed * r.uniform(.15, 1., (n, 1)); dl = r.uniform(0, .35, (n, 1)); tt = np.maximum(t - dl, 0); P = P + (d + V(0, .5, 0)) * sp * (1 - np.exp(-2.2 * tt)) / 2.2 * S.Sc + V(0, -1, 0) * 1.6 * tt ** 2 * S.Sc; P[:, 0] += .4 * np.sin(5 * tt[:, 0] + k[:, 0] * 30) * tt[:, 0] * S.Sc
    al = np.clip(1.6 - tt[:, 0] / life * 1.6, 0, 1); FX.particles(st, P, size * S.Sc * r.uniform(.4, 1.4, n), col, 'flake', rot=r.uniform(0, 6, n) + tt[:, 0] * r.uniform(-9, 9, n), seed=k[:, 0], alpha=al)
