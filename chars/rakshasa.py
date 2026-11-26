"""Rakshasas: four kinds of soldier, Maricha (the demon under the golden deer) and Indrajit (Ravana's son)."""
import numpy as np, math
from lau.stage import Fig
from lau.face import human, Face
from lau.rig import Pose, V, nz
from lau import poses as PZ, props as PR


def _fierce(**st):
    paint = st.pop('paint', '#c8a03a'); pk = st.pop('pk', 0)
    S = {**dict(iris='#e0a01c', iris2='#7a1606', sclera='#f6e2a8', lip='#4a1a1c', lip2='#5e2424', liphi='#9a5a50', kohl='#0c0408', brow='#100808', browt=2.6, tilak='none', size=1.16, nose='#140a0c', mouthw=1.45, tilt=.16), **st}

    def extra(P, F, k):
        for sd in (1, -1):
            P.c.save(); P.c.scale(sd, 1)
            P.line([(.20, -.36), (.30, -.42, .36, -.52, .36, -.64)], .018, k['nose'], .8); P.line([(.05, .12), (.06, .18, .05, .24, .09, .30)], .018, k['nose'], .8); P.line([(.07, -.18), (.12, -.14, .16, -.16, .18, -.22)], .012, k['nose'], .6)
            P.line([(.56, -.08), (.62, -.10, .66, -.14, .70, -.2)], .012, k['nose'], .6)
            if pk == 0: [P.line([(.24 + .12 * i, -.22), (.25 + .12 * i, -.30, .27 + .12 * i, -.38, .30 + .12 * i, -.44)], .035, paint, .9) for i in range(3)]
            if pk == 1: P.fill([(.10, .40), (.30, .48, .48, .44, .62, .30), (.50, .52, .25, .62, .06, .60)], paint, .85)
            if pk == 2: P.fill([(.0, .62), (.05, .4, .03, .2, 0, .16), (-.03, .2, -.05, .4, 0, .62)], paint); P.line([(.62, .02), (.5, -.15, .5, -.3, .44, -.5)], .028, paint, .9)
            if pk == 3: [P.line([(.0, .34 + .09 * i), (.12, .33 + .09 * i, .22, .30 + .09 * i, .34, .28 + .09 * i)], .03, paint, .9) for i in range(3)]
            P.c.restore()
    return lambda F: human(F.set(frown=min(1.3, .55 + .5 * F.frown)), S, extra=extra)


def _pal(skin, sh, hair='#14100f', cloth=('#5a1c1a', '#240a10', 1), sash=('#8a1c1c', '#3a0a12', 1), iron=('#4a4c58', '#22242e', 7), shield=('#6a1a1a', '#2a0a10', 1)):
    return {1: (skin, sh, 1), 2: (hair, '#070506', 5), 3: ('#c99a5a', '#60381c', 2), 4: ('#b3222a', '#4a0818', 3), 5: iron, 6: ('#eadfc2', '#8f7a68', 1), 7: cloth, 8: sash, 9: ('#4a2c1a', '#1f120c', 1), 10: ('#a4adbb', '#444c5a', 7), 11: ('#5a3620', '#26140c', 1), 12: shield, 13: ('#f2e6c8', '#8a6a50', 1)}


_U = dict(hold=0, shield=0, gild=0.)
TUSK = Fig('rk0', 'rakshasa.glsl', _pal('#6f8038', '#2c3a20'), dim=dict(chest=3.05, up=2.75, fore=2.5, th=3.5, sh=3.3, hand=1.15, foot=1.1), build=dict(chest=1.2, depth=1.22, rib=1.35, waist=1.42, hips=1.2, arm=1.22, leg=1.2, belly=.7, neck=1.35, shoulder=1.1), hs=[1.25, 1.3, .9, 1.5, 1.15, 1.5, 1.1, 1.02], face=_fierce(), bound=(0, 8, 0, 24), defs='#define KIND 0\n#define HSC 1.08', u={**_U, 'hold': 3})
HORN = Fig('rk1', 'rakshasa.glsl', _pal('#8e3430', '#3c1420', hair='#1a0d0c', cloth=('#2c2a3a', '#121020', 1), sash=('#c8862a', '#6a3412', 1)), dim=dict(chest=3.1, up=2.8, fore=2.5, th=3.75, sh=3.55, hand=1.12), build=dict(chest=1.18, depth=1.1, rib=1.18, waist=1.08, hips=1.05, arm=1.18, leg=1.1, neck=1.25, shoulder=1.1), hs=[1.1, 1.15, 1., 1.3, 1.1, 1.5, 1., 1.05], face=_fierce(paint='#1a0c10', pk=1, iris='#e8c83a', iris2='#8a2a06'), bound=(0, 8, 0, 24), defs='#define KIND 1\n#define HSC 1.06', u={**_U, 'hold': 2, 'shield': 1})
ARCHER = Fig('rk2', 'rakshasa.glsl', _pal('#8d8a90', '#403c50', hair='#22202a', cloth=('#3a4a3a', '#161e1c', 1), sash=('#6a2a4a', '#2a0f24', 1)), dim=dict(chest=3.1, up=2.85, fore=2.6, th=3.95, sh=3.7), build=dict(chest=.95, depth=.92, rib=.92, waist=.86, hips=.92, arm=.92, leg=.92, neck=1.0), hs=[.95, 1., 1.1, 1.15, 1.2, 1.3, .9, 1.1], face=_fierce(paint='#b3262a', pk=2, iris='#b8d04a', iris2='#3a5a12'), bound=(0, 8, 0, 24), defs='#define KIND 2\n#define HSC 1.02', u={**_U, 'hold': 4})
HULK = Fig('rk3', 'rakshasa.glsl', _pal('#4a6a94', '#1e2c52', cloth=('#6a3a1c', '#2a140c', 1), sash=('#b08a2a', '#4a3010', 1)), dim=dict(chest=3.4, up=3.1, fore=2.9, th=3.6, sh=3.4, hand=1.45, foot=1.25, shx=1.8), build=dict(chest=1.55, depth=1.45, rib=1.6, waist=1.6, hips=1.35, arm=1.62, leg=1.42, belly=.9, neck=1.7, shoulder=1.35), hs=[1.4, 1.5, .85, 1.6, 1.1, 1.6, 1.15, .98], face=_fierce(paint='#e8e0d0', pk=3, iris='#f0b02a', iris2='#8a2a06'), bound=(0, 8, 0, 26), defs='#define KIND 3\n#define HSC 1.08', u={**_U, 'hold': 3})
KINDS = [TUSK, HORN, ARCHER, HULK]
SPEARMAN = TUSK.variant(u=dict(hold=1, shield=1)); SWORDSMAN = TUSK.variant(u=dict(hold=2, shield=1)); HORN_SPEAR = HORN.variant(u=dict(hold=1, shield=0))


def _maricha(P, F, k):
    for sd in (1, -1):
        P.c.save(); P.c.scale(sd, 1)
        P.line([(.14, -.10), (.26, -.20, .40, -.18, .52, -.06)], .02, k['nose'], .75); P.line([(.18, -.16), (.28, -.26, .40, -.25, .50, -.14)], .012, k['nose'], .6)
        P.line([(.22, -.34), (.34, -.44, .36, -.60, .30, -.80)], .018, k['nose'], .8); P.line([(.60, -.05), (.64, -.2, .60, -.4, .52, -.55)], .014, k['nose'], .6)
        [P.line([(.04 + .02 * i, .36 + .075 * i), (.15, .40 + .075 * i, .28, .41 + .075 * i, .42, .34 + .075 * i)], .012, k['nose'], .6) for i in range(3)]
        P.c.restore()


MARICHA = Fig('maricha', 'rakshasa.glsl', {**_pal('#7a6a4e', '#352a38', hair='#2a2220', cloth=('#4a3a2a', '#1e1614', 1), sash=('#5a4a36', '#241a18', 1)), 3: ('#d8a860', '#60381c', 2)}, dim=dict(chest=3.0, up=2.95, fore=2.8, th=3.8, sh=3.7, hand=1.28, foot=1.1), build=dict(chest=.92, depth=.80, rib=.80, waist=.60, hips=.80, arm=.74, leg=.72, neck=.85, shoulder=1.0), hs=[.95, .95, 1.2, 1.25, 1.3, 1.5, 1., 1.1],
              face=lambda F: human(F, dict(iris='#d8a02a', iris2='#5a2a08', sclera='#f8ecc8', lip='#5a2a28', lip2='#6e3430', liphi='#a86a58', kohl='#120812', brow='#16100e', browt=1.7, tilak='none', size=1.30, nose='#22141a', mouthw=1.35), extra=_maricha), bound=(0, 8, 0, 14), defs='#define KIND 4\n#define HSC 1.32', u={**_U})


def _indrajit(P, F, k):
    for sd in (1, -1):
        P.c.save(); P.c.scale(sd, 1)
        P.fill([(0, -.455), (.08, -.43, .20, -.47, .30, -.40), (.22, -.50, .10, -.50, 0, -.485)], '#0a0810')                                        # thin moustache
        P.fill([(.50, .08), (.58, .12, .66, .20, .70, .30), (.64, .22, .58, .18, .52, .13)], '#0e3a34'); P.c.restore()
    P.line([(0, .16), (.05, .22, .06, .27, 0, .32), (-.06, .37, -.05, .43, 0, .50)], .03, '#e8c85a'); P.col('#1fae8a'); P.c.arc(0, .135, .03, 0, 7); P.c.fill()


INDRAJIT = Fig('indrajit', 'rakshasa.glsl', {**_pal('#5e5078', '#221a40', hair='#0e0c14', cloth=('#16403c', '#071c20', 8), sash=('#1f5a50', '#0a2824', 8), iron=('#33404c', '#12181f', 7)), 3: ('#e6cc94', '#7a5428', 2), 4: ('#12a078', '#06403a', 3), 8: ('#1c5a4e', '#0a2a2a', 8)}, dim=dict(chest=3.1, up=2.8, fore=2.55, th=4.0, sh=3.75), build=dict(chest=1.05, depth=.98, rib=1.0, waist=.92, hips=.96, arm=1.02, leg=1.0, neck=1.0, shoulder=1.05), hs=[1.02, 1.05, 1.1, 1., 1.1, 1.2, 1., 1.06],
               face=lambda F: human(F, dict(iris='#2fae7a', iris2='#0c4030', sclera='#f6f0dc', lip='#5a2a44', lip2='#7a3a54', liphi='#c08a92', kohl='#050a10', kohlk=1.2, brow='#080810', browt=1.5, tilak='none', size=1.04, nose='#101828', tilt=.10), extra=_indrajit), bound=(0, 8, 0, 14), defs='#define KIND 5\n#define HSC 1.02', u={**_U})
SERPENT_BOW = Fig('serpent_bow', 'rakshasa.glsl', {**PR.PAL, 9: ('#2f7a62', '#0c2a2c', 8), 3: ('#e6cc94', '#7a5428', 2), 4: ('#ffb02a', '#a0300c', 4), 5: ('#e8c84a', '#6a4a10', 3), 12: ('#33404c', '#12181f', 7), 13: ('#bfe8d0', '#4a8a7a', 1)}, bound=(0, 0, -1.2, 6.6), step=.75, defs='#define SBOW', human=False, u=dict(pr=np.array([1.0, 4.8] + [0.] * 14, 'f4')))


def serpent_bow(st, S, side='L', arrow=True, half=4.8, release=0., tint=('#cfe8d8', '#4a7a6a', 4)):
    """Indrajit's bow between his two hands, like PR.bow_and_arrow; returns (nock, tip, aim)"""
    o = 'R' if side == 'L' else 'L'; g = S.palm(side, .0, .62, .30); nk = S.palm(o, .22, .95, .34); aim = nz(g - nk); pull = float(np.linalg.norm(g - nk)) / S.Sc
    if release > 0: pull = 1. + (pull - 1.) * max(0, 1 - release)
    u = S.d(V(0, 1, 0)); st.fig(SERPENT_BOW.variant(u=dict(pr=np.array([pull, half] + [0] * 14, 'f4'))), M=PR.place(g, u - aim * (u @ aim), aim, S.Sc))
    if arrow: st.fig(PR.ARROW.variant(pal={10: tint}), M=PR.place(nk, u - aim * (u @ aim), aim, S.Sc))
    return nk, nk + aim * 5. * S.Sc, aim


# ------------------------------------------------------------------ poses
def K_RUN(ph):
    """charge, weapon arm high"""
    P = PZ.run(ph, stride=2.8, lift=2.0, lean=20); c = math.cos(2 * math.pi * ph); s = math.sin(4 * math.pi * ph)
    return P.set(rh=(-2.6, 12.6 + .35 * s, 1.6 + .5 * c), rel=(-1, -.5, -.4), rhand='grip', rfing=(.3, -.25, .9), rpalm=(.95, 0, -.3), lh=(1.9, 10.4 + .2 * s, 2.3 - .6 * c), lel=(.9, -.5, -.3), lhand='fist', lfing=(-.6, .2, .75), lpalm=(-.35, 0, -.95))


_ST = [(0., Pose(pel=(0, 7.6, -.4), pelr=(-24, 0, 0), cher=(-16, 2, 0), hedr=(36, 0, 0), rh=(-2.4, 10.8, -1.6), rel=(-.6, .6, -.8), rhand='grip', rfing=(.3, -.3, .9), rpalm=(.3, .9, .1), lh=(1.7, 10.6, 2.8), lel=(.8, -.5, -.2), lhand='fist', lf=(.9, .75, 2.1), rf=(-1.1, .75, -1.7), rft=(-40, 0))),
       (.5, Pose(pel=(0, 7.1, 1.1), pelr=(14, 8, 0), cher=(22, 10, 0), hedr=(-30, -6, 0), rh=(-.7, 10.6, 5.4), rel=(-1, .3, 0), rhand='grip', rfing=(.3, -.2, .9), rpalm=(.3, .9, .1), lh=(2.4, 10.0, 1.0), lel=(.8, -.5, -.6), lhand='fist', lf=(.9, .75, 2.9), rf=(-1.1, .85, -2.0), rft=(-40, 20))),
       (1., Pose(pel=(0, 7.4, .4), pelr=(0, 4, 0), cher=(4, 4, 0), hedr=(-4, -4, 0), rh=(-1.8, 10.3, 2.6), rel=(-1, .1, -.4), rhand='grip', rfing=(.3, -.2, .9), rpalm=(.3, .9, .1), lh=(2.0, 10.4, 2.2), lel=(.8, -.5, -.4), lhand='fist', lf=(.9, .75, 2.1), rf=(-1.1, .75, -1.7), rft=(-40, 0)))]


def K_STAB(t):
    """0 drawn back, .5 thrust home, 1 recovered (spear points along the thumb side of the hand)"""
    for (a, A), (b, B) in zip(_ST, _ST[1:]):
        if t <= b: return A.mix(B, max(0., (t - a) / (b - a)))
    return _ST[-1][1]


K_STAB_POSES = _ST
K_GUARD = Pose(pel=(0, 7.75, 0), pelr=(-12, 3, 0), cher=(-8, 5, 0), hedr=(18, -4, 0), rh=(-2.7, 9.6, 1.9), rel=(-1, -.1, -.5), rhand='grip', rfing=(.1, .0, 1), rpalm=(1, 0, 0), lh=(1.5, 11.0, 2.6), lel=(1, -.6, 0), lhand='fist', lfing=(-.75, .25, .55), lpalm=(-.5, 0, -.85), lf=(1.1, .75, 1.1), rf=(-1.3, .75, -.9), lft=(10, 0), rft=(-44, 0))
K_FALL = Pose(pel=(0, 6.4, -1.2), pelr=(10, -34, 8), cher=(10, -26, 6), hedr=(0, -18, 0), lh=(4.0, 12.6, -1.8), rh=(-4.2, 11.6, -2.6), lel=(.6, -.4, -.8), rel=(-.6, -.4, -.8), lhand='open', rhand='open', lf=(1.0, 1.2, 2.2), rf=(-.9, .85, 1.2), lft=(10, -30), rft=(-20, -14))
K_DOWN = Pose(pel=(0, 1.25, 0), pelr=(0, -86, 0), cher=(0, -6, 0), hedr=(18, -4, 0), lh=(4.4, .9, -2.2), rh=(-4.6, 1.0, -3.6), lel=(.5, .6, 0), rel=(-.5, .6, 0), lhand='open', rhand='relax', lpalm=(0, 1, 0), rpalm=(0, 1, 0), lf=(1.4, .8, 6.6), rf=(-1.2, .8, 6.0), lkn=(.6, 1, 0), rkn=(-.4, 1, 0), lft=(20, -60), rft=(-30, -60))
K_CROWD = [K_RUN(i / 6) for i in range(6)]


def K_SHOOT(d=1.): return PZ.archer(d)


M_CRY = Pose(pel=(0, 7.6, 0), pelr=(0, -6, 0), cher=(0, -16, 4), hedr=(0, -16, 6), lh=(4.6, 12.4, 2.0), rh=(-4.2, 13.6, 1.2), lel=(.8, -.6, -.4), rel=(-.8, -.6, -.4), lhand='claw', rhand='claw', lfing=(.4, .8, .3), rfing=(-.4, .8, .3), lpalm=(-.3, .2, 1), rpalm=(.3, .2, 1), lf=(1.0, .75, 1.6), rf=(-1.0, .9, -1.4), rft=(-20, 16), lft=(10, 0))
M_FALLING = M_CRY.set(pel=(0, 6.2, -.8), pelr=(0, -26, 8), cher=(0, -20, 6), lf=(1.2, 1.6, 2.6), rf=(-1.0, .9, 1.0))
CRY = Face(mouth=1., teeth=.3, sad=.9, frown=.1, brow=.4, smile=-.3, lid=1., pupil=.6)
I_STAND = PZ.CONTRA.set(pel=(.25, 8.45, 0))
