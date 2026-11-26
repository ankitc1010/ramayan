"""War horses (and Ravana's donkey-faced demon team).  Drawn at scale 1.9 by default: withers about 13.5 units, crown about 21.

    from chars import horse as HR
    S = HR.draw(st, HR.gallop(ph), at=.., yaw=.., kind='white'|'dawn'|'demon')
    S.p('bit'), S.p('collar'), S.p('back'), S.p('girthL') ...       world points for reins and traces
Poses: STAND gallop(ph) trot(ph) walk(ph) rear(t) halt(t).  GALLOP_DIST = ground covered per cycle at the default scale."""
import numpy as np, math
from dataclasses import replace
from lau.stage import Fig, model, hexc
from lau.rig import V, nz, Rx, Ry, Rz
from lau.face import Face
from lau import cloth as CL
from chars import deer as D
from chars.deer import QPose, Build, Beast, track, LEGS, _pose, _foot
from chars.jatayu import feathers, FEATHER, join, xform

SCALE = 1.9
BUILD = Build(hb=5.75, L=4.3, hip=(.70, .15, -.30), sh=(.78, -.90, .95), el=(.0, -.55, -1.0), fore=2.1, can=1.62, fem=1.8, tib=2.1, met=1.95, past=.62, pa=36., hoof=.20, stF=(.72, .55), stH=(.78, -.85), n0=(0, .55, .75), nl=(2.0, 1.75), hd=(0, .10, .30), tl=(.6, .5), t0=(0, .85, -1.45))
STAND = QPose(neck=(62., 52., 0.), head=(0., 44., 0.), fl=(0, 0, .1), fr=(0, 0, -.1), hl=(0, 0, -.2), hr=(0, 0, .25), tail=(-30., 0.), ears=(.3, .3))
_H = [(0., (0, 2.9, 0)), (.11, (0, .1, 0)), (.22, (.1, -2.8, 20)), (.33, (1.2, -3.3, 85)), (.50, (1.8, -1.2, 102)), (.70, (1.9, 1.9, 70)), (.86, (1.2, 3.6, 18)), (.95, (.4, 3.5, 0))]
_F = [(0., (0, 2.7, 0)), (.11, (0, .0, 0)), (.22, (.1, -2.8, 25)), (.33, (1.5, -3.0, 108)), (.52, (2.9, -.4, 128)), (.70, (3.1, 2.0, 98)), (.84, (2.1, 3.4, 30)), (.94, (.6, 3.3, 0))]
_T = dict(y=[(0., -.10), (.12, -.28), (.30, .0), (.46, -.22), (.62, -.05), (.80, .55), (.92, .30)], pitch=[(0., 3), (.14, 8), (.30, 2), (.46, -6), (.60, -7), (.80, 0)], bend=[(.0, 9), (.18, -2), (.38, -5), (.58, 0), (.84, 11)],
          neck=[(0., (56, 44)), (.18, (50, 36)), (.44, (40, 24)), (.62, (48, 34)), (.84, (60, 50))], head=[(0., 42), (.2, 34), (.46, 26), (.7, 38), (.86, 46)], tail=[(0., 10), (.3, 26), (.6, 4), (.85, 18)], ears=[(0., -.3), (.5, -.1)])
GALLOP_DIST = 5.7 / .22 * SCALE


def gallop(ph, lead=1):
    """transverse gallop: off hind, near hind, off fore, leading fore, then the gathered flight; lead +1 = its left fore leads"""
    a, b = ('r', 'l') if lead > 0 else ('l', 'r'); off = {'h' + a: 0., 'h' + b: .10, 'f' + a: .30, 'f' + b: .46}; T = dict(_T)
    k = {n: track(ph, K, 1.) for n, K in _T.items()}; d = {}; fo = []
    for n in LEGS: u, f, o = track(ph - off[n], _H if n[0] == 'h' else _F, 1.); d[n] = (0, u, f); fo.append(o)
    return QPose(pos=(0, k['y'], 0), pitch=k['pitch'], bend=k['bend'], neck=(*k['neck'], 0.), head=(0., k['head'], 0.), tail=(k['tail'], 0.), ears=(k['ears'],) * 2, fold=tuple(fo), **d, jaw=.25)


def trot(ph):
    """two-beat trot on the diagonals, high knees"""
    f = {n: _foot(ph - o, .42, 2.9, 1.5 if n[0] == 'f' else 1.1, 105 if n[0] == 'f' else 80) for n, o in dict(fl=0., hr=.02, fr=.5, hl=.52).items()}; b = math.cos(4 * math.pi * ph + .6)
    return QPose(pos=(0, -.1 - .16 * b, 0), neck=(64 + 2 * b, 50, 0.), head=(0., 48 - 2 * b, 0.), tail=(-5, 0), ears=(.2, .2), **{n: (0, v[0], v[1]) for n, v in f.items()}, fold=tuple(f[n][2] for n in LEGS))


def walk(ph): p = D.step(ph, 2.6, .8); return replace(p, neck=(p.neck[0] + 24, p.neck[1] - 14, 0.), head=(0., p.head[1] + 22, 0.))


def rear(t):
    """rears up: t 0 standing, .5 high with pawing fores, 1 down"""
    h = math.sin(math.pi * min(max(t, 0), 1)) ** .7; s = math.sin(t * 18)
    return STAND.mix(QPose(pos=(0, 1.1, -1.4), pitch=44., bend=-4., neck=(54, 44, 0.), head=(0., 52., 0.), fl=(0, 4.8 + .5 * s, 1.3), fr=(0, 4.1 - .5 * s, 2.0), hl=(0, 0, .6), hr=(0, 0, 1.0), fold=(112, 88, 0, 0), tail=(-30, 0), ears=(-.7, -.7), jaw=.6), h)


def halt(t): return gallop(.2).mix(STAND.set(pitch=5., pos=(0, -.3, -.4), hl=(0, 0, 1.2), hr=(0, 0, .9), neck=(74, 60, 0.), head=(0., 56., 0.)), min(1., t))


PAL = {1: ('#f6f1e8', '#8f93b8', 1), 3: ('#ffffff', '#805030', 2), 4: ('#d81838', '#54081c', 3), 5: ('#12a074', '#063a34', 3), 6: ('#f6f4ea', '#a8a2c8', 8), 7: ('#4a3a36', '#1a1418', 8), 8: ('#d8c8a8', '#6a5a4a', 8), 9: ('#d8a49a', '#8a5058', 1), 10: ('#a8a6b4', '#50506c', 1), 11: ('#fff6e0', '#a89ab0', 8), 12: ('#b3202a', '#4a0c1c', 8)}
HORSE = Fig('horse', 'horse.glsl', PAL, face=D._eye, human=False, step=.86, bound=(0, 5.5, 1, 8), u=dict(demon=0., harness=1., plain=0., clothA=hexc('#b3202a'), clothB=hexc('#1f5a9a')))
DAWN = HORSE.variant(pal={1: ('#e8c99a', '#8a5a4a', 1), 10: ('#8a5a3a', '#3c2028', 1)}, u=dict(clothA=hexc('#0f6a5a'), clothB=hexc('#b3202a')))
DEMON = HORSE.variant(pal={1: ('#3a3236', '#0e0a14', 1), 3: ('#f6dcae', '#805030', 2), 7: ('#1a1216', '#080508', 7), 9: ('#8a2a2a', '#3c0c14', 1), 10: ('#1c161c', '#08060c', 1), 12: ('#5a0c16', '#1c040a', 8)}, u=dict(demon=1., clothA=hexc('#6a0c16'), clothB=hexc('#1a1018')))
KINDS = dict(white=(HORSE, ('#f4e6c4', '#9a7f96', '#d8743a'), ('#d81838', '#6a0a1c', '#f0b040')), dawn=(DAWN, ('#3a2020', '#140a10', '#5a3020'), ('#12a074', '#063a34', '#f0c040')), demon=(DEMON, ('#1c1014', '#080408', '#b03014'), ('#e05018', '#5a0c0c', '#1a0a0e')))
NAMES = dict(head=('h', (0, 0, 0)), bitL=('h', (.46, -.34, 1.56)), bitR=('h', (-.46, -.34, 1.56)), nose=('h', (0, -.2, 2.4)), poll=('h', (0, 1.1, -.1)), eyeL=('h', (.5, .14, .7)), chest=('c', (0, -.5, 1.4)), collarL=('c', (1.2, -.1, .4)), collarR=('c', (-1.2, -.1, .4)), back=('c', (0, 1.0, -2.0)), withers=('c', (0, 1.25, -.2)), girthL=('c', (1.4, -.2, -1.1)), girthR=('c', (-1.4, -.2, -1.1)), rump=('p', (0, 1.2, -.6)))


def draw(st, pose=None, at=(0, 0, 0), yaw=0., pitch=0., roll=0., scale=SCALE, M=None, kind='white', t=None, speed=0., face=None, harness=1., plume=True, u=None, shadow=True, draw=True, hair=True):
    """speed 0..1 blows mane and tail back; t seconds drives their waves (default st.t)"""
    p = pose or STAND; q = D.solve(p, BUILD); J = q['J']; fig, hc, pc = KINDS[kind]; t = st.t if t is None else t; M = model(at, yaw, pitch, roll, scale) if M is None else np.asarray(M, float)
    c = (J[0] + J[1]) / 2 * .72 + J[5] * .28; R = np.linalg.norm(J[:29] - c, axis=1).max() + 1.0
    if face is None: face = Face(glow=.9) if kind == 'demon' else Face()
    S = st.fig(fig, M=M, face=face, u=dict(J=J, Bp=q['Bp'], Bc=q['Bc'], Bh=q['Bh'], ear=np.array(p.ears, 'f4'), jaw=float(p.jaw), harness=float(harness), bound=np.append(c, max(R, np.linalg.norm(J[5] - c) + 2.8)), **(u or {})), shadow=shadow, draw=draw)
    S = Beast(S, q, NAMES, 1.13)
    if not draw or not hair: return S
    HD = lambda x: J[5] + np.asarray(x, float) * 1.13 @ q['Bh']
    # mane along the crest
    fw = nz(q['Bh'][2] * 0 + (J[4] - J[2])); side = nz(np.cross(V(0, 1, 0), V(0, 0, 1))); n = 26; crest = CL.spline(np.array([J[2] + V(0, 1.12, -.55), J[3] + V(0, .55, -.62), J[4] + V(0, .18, -.62), HD((0, .62, -.35)), HD((0, .62, .30))]), n); T = np.gradient(crest, axis=0); T /= np.linalg.norm(T, axis=1, keepdims=True)
    back = nz(V(0, .25, -1.)); k = np.arange(n); parts = []
    for s in (0, 1):
        w = np.sin(t * 9 - k * .55 + s * 2.) * (.25 + .5 * speed); out = np.where((k + s) % 2, 1., -1.)[:, None]
        if kind == 'demon': d = np.cross(T, V(1, 0, 0)) * -1. + back * (.4 + .8 * speed) + V(0, .25, 0) + out * V(.12, 0, 0) + w[:, None] * V(.2, .15, 0); L = 1.15 + .25 * np.sin(k * 2.3 + s)
        else: d = V(0, -1, 0) * (.62 - .40 * speed) + back * (.25 + 1.35 * speed) + out * V(1.15 - .95 * speed, 0, 0) + w[:, None] * V(.35, .35, 0); L = 1.7 + .35 * np.sin(k * 1.7 + s)
        L = L * np.where(k > n - 4, .62, 1.); parts.append(feathers(crest + V(0, -.05, 0), d, np.tile(V(1, 0, 0), (n, 1)) * out, L, .26, (.18 * np.sin(t * 7 - k * .8 + s)) * (.3 + .7 * speed) - .55 * (1 - speed), .1, 0., id0=s * n, nl=8))
    hu = dict(shape=3, cE=hexc(hc[2]), tipAt=.6, gild=0., bars=0., ragged=1., asp=6., burnF=0.); st.mesh(*xform(join(parts), M), col=hc, ink=.8, frag=FEATHER, u=hu)
    # tail: locks that lift and stream
    r0 = J[27]; d0 = nz(J[27] - J[26]); parts = []
    for i in range(9):
        a = (i - 4) / 4; L = 4.0 + .5 * math.sin(i * 2.1); P = []
        for j in range(9):
            uu = j / 8; P.append(r0 + d0 * .35 * math.sin(min(1, uu * 2) * 1.57) + V(a * .30 * uu * (1 + .6 * speed), -L * uu * uu * (1 - .72 * speed) - .25 * uu, -L * uu * (.22 + .78 * speed)) + V(.35 * math.sin(t * 8 - uu * 4.5 + i * .5), .45 * math.sin(t * 9 - uu * 5 + i * .35) * (.3 + speed), 0) * uu)
        parts.append(CL.strip(np.array(P), [.40, .62, .55, .10], up=nz(V(.5 if i % 2 else -.5, .15 + speed, 1.05 - speed)), m=4, n=16))
        pz = parts[-1]; pz[2][:, 0] = pz[2][:, 0] * .98 + i + 70; 
    st.mesh(*xform(join(parts), M), col=hc, ink=.8, frag=FEATHER, u=dict(hu, shape=3))
    if plume and harness:
        b = HD((0, 1.1, -.08)); n = 7; a = np.linspace(-1, 1, n); up = q['Bh'][1]; bk = -q['Bh'][2]; d = up * 1. + np.outer(a, q['Bh'][0]) * .42 + bk * (.25 + .5 * speed)
        st.mesh(*xform(feathers(np.tile(b, (n, 1)) + np.outer(a, q['Bh'][0]) * .08, d, np.tile(q['Bh'][2], (n, 1)) + np.outer(a, q['Bh'][0]) * .3, 1.55 - .35 * np.abs(a), .24, -.35 - .25 * speed + .08 * np.sin(t * 8 + a * 2), .2, 8 * a, nl=9), M), col=pc, ink=.85, frag=FEATHER, u=dict(shape=1, cE=hexc('#ffe8b0'), tipAt=.7, gild=0., bars=0., ragged=1., asp=6., burnF=0.))
    return S
