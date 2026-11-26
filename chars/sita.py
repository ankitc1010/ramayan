"""Sita: BRIDE (crimson and gold), FOREST (ochre cotton and jasmine), GROVE (worn pale yellow, loose hair, the hair jewel).
Poses: S_STAND S_WALK(phase) S_GARLAND S_SIT S_PALM S_LOOKUP S_HEART S_STEP, and fit(pose) for poses of lau.poses."""
from lau.stage import Fig
from lau.rig import Pose
from lau.face import human, Face
from lau import poses as PZ

SKIN = ('#dca070', '#8f5236', 1)
DIM = dict(chest=2.55, shx=1.66, shy=.93, shz=-.13, neck=1.34, nz=-.14, head=1.50, hz=.13, up=2.46, fore=2.26, hipx=.58, hipy=-.30, th=3.68, sh=3.47, hand=1.08, foot=.84)
BUILD = dict(chest=.80, depth=.88, rib=.80, waist=.74, hips=1.06, arm=.66, leg=.86, hand=.84, bust=.75, neck=.84, shoulder=.80)
HS = [.95, .86, .90, .78, 1.0, .55, 1.02, .95]
PAL = {1: SKIN, 2: ('#2a1a14', '#100908', 5), 3: ('#ffffff', '#805030', 2), 4: ('#c4142c', '#54081c', 3), 5: ('#0f7a58', '#063a34', 3), 6: ('#fff4e0', '#c8a098', 1), 7: ('#c01828', '#5c0a20', 8), 8: ('#c81c2a', '#600c22', 8), 9: ('#5a1038', '#2a0820', 8),
       10: ('#d0222c', '#6a0e24', 8), 11: ('#fff0d8', '#d08a7a', 1), 14: ('#e8a838', '#8a4a14', 1), 15: ('#ffffff', '#805030', 2), 16: ('#fff4e0', '#c8a098', 1),
       17: ('#6a0f3a', '#340820', 8), 18: ('#a2301c', '#4a1410', 1), 19: ('#e0a040', '#7a4a1c', 1), 20: ((2.4, 1.2, .3), (2.4, 1.2, .3), 4), 21: ('#c8822a', '#6a3a12', 1)}


def lashes(P, F, k, col='#150a14', n=3, lower=True):
    """fine outer lashes and a soft line down the nose"""
    c = P.c; up = -.035 + .20 * F.lid; lo = -.062 + .03 * max(F.smile, 0) + .05 * F.squint; wy = .135 * (.25 + .75 * F.lid)
    for sd in (1, -1):
        c.save(); c.scale(sd, 1); c.translate(k['eyex'], 0); c.translate(.33, .03); c.scale(k['size'], k['size']); c.rotate(k['tilt']); c.translate(-.33, -.03)
        for i in range(n):
            u = i / max(1, n - 1); x = .46 + .13 * u; y = (up + .012) * (1 - u) + (wy - .01) * u; P.line([(x, y - .01), (x + .03, y + .004, x + .052, y + .018, x + .060 + .022 * u, y + .030 - .008 * u)], .014, col)
        if F.lid < .3:
            for i in range(6):
                u = i / 5; x = .20 + .30 * u; y = lo - .01 + .05 * u * u; P.line([(x, y), (x + .01, y - .025, x + .02 + .02 * u, y - .045, x + .035 + .035 * u, y - .052 + .015 * u)], .010, col)
        elif lower:
            for i in range(4):
                u = i / 3; x = .42 + .10 * u; y = lo + .02 + .06 * u; P.line([(x, y), (x + .010, y - .008, x + .016, y - .010, x + .026, y - .012)], .008, col, .7)
        c.restore()
    P.line([(-.045, .10), (-.065, -.02, -.060, -.14, -.085, -.235)], .012, k['nose'], .45)


def face(F, **k):
    st = dict(iris='#6a3416', iris2='#1e0c06', lip='#b03a4a', lip2='#c9545e', liphi='#f8c0b0', blush='#e05a48', brow='#2a1610', browt=.75, browy=.025, tilak='bindi', size=1.10, nose='#9a5236', kohl='#2a1210', mouthw=.86, tilt=.02)
    return human(F, {**st, **k}, extra=lashes, S=1536)


BRIDE = Fig('sita', 'sita.glsl', PAL, dim=DIM, build=BUILD, hs=HS, face=face, u=dict(look=0, hairm=0, veil=1., lamp=0., old=0.))
FOREST = BRIDE.variant(pal={7: ('#e0922c', '#8a4a1c', 1), 8: ('#e89e38', '#94501e', 1), 9: ('#a83a1c', '#5c1c14', 1), 14: ('#f0b83a', '#9a5a1c', 1)}, u=dict(look=1, veil=0.))
GROVE = BRIDE.variant(pal={7: ('#ecd794', '#a08a5a', 1), 8: ('#f0dca2', '#a48e60', 1), 9: ('#c9a45e', '#7a5a36', 1), 14: ('#8a5a2a', '#4a2a14', 1), 18: ('#a8762a', '#5a3c18', 1), 19: ('#a8762a', '#5a3c18', 1)}, u=dict(look=2, hairm=1, veil=0.), face=lambda F: face(F, tilak=None, blush='#d87a5a'))


def fit(pose, k=.965):
    """a pose of lau.poses scaled to her height"""
    f = lambda v: None if v is None else tuple(k * x for x in v)
    return pose.set(pel=(pose.pel[0] * k, min(pose.pel[1] * .981, 8.2), pose.pel[2] * k), lh=f(pose.lh), rh=f(pose.rh))


_ARMS = dict(lel=(.5, -.2, -1), rel=(-.5, -.2, -1))
S_STAND = Pose(pel=(.24, 8.22, 0), pelr=(8, 0, 5), cher=(-6, -1, -11), hedr=(-6, 4, 8), lf=(.62, .75, .0), rf=(-.40, .84, .42), lkn=(.1, 0, 1), rkn=(-.15, 0, 1), lft=(16, 0), rft=(-16, 8), lh=(1.95, 7.6, .15), rh=(-.30, 9.25, 1.45), rhand='pinch', rfing=(.8, .35, .25), rpalm=(.1, -.2, -1), rel=(-1, -1.2, -.2), lel=(.5, -.2, -1))


def S_WALK(ph):
    p = PZ.walk(ph, stride=1.05, lift=.45, bounce=.10, swing=.7)
    return p.set(pel=(0, 8.19 - .085 * abs(p.pelr[0]) / 9, 0), cher=(p.cher[0] * .5, 1, p.cher[2]), hedr=(p.hedr[0], 3, 0), lf=(.36, p.lf[1], p.lf[2]), rf=(-.36, p.rf[1], p.rf[2]), lh=(1.75, 7.5, p.lh[2] - .1), rh=(-1.55, 8.9, 1.2 + .25 * p.rh[2]), rhand='pinch', rfing=(.6, .3, .7), rpalm=(.4, -.4, -.8), rel=(-1, -1, -.4), lel=(.6, -.1, -1))


S_GARLAND = Pose(pel=(0, 8.18, .2), pelr=(0, 0, 2), cher=(0, -3, -3), hedr=(0, 2, 2), lf=(.42, .75, .0), rf=(-.40, .75, .55), lft=(12, 0), rft=(-10, 0), lh=(1.30, 11.75, 3.35), rh=(-1.30, 11.75, 3.35), lel=(.9, -1, .1), rel=(-.9, -1, .1), lhand='hold', rhand='hold', lfing=(-.35, .35, .85), rfing=(.35, .35, .85), lpalm=(-.45, .85, -.1), rpalm=(.45, .85, -.1))
S_SIT = Pose(pel=(.25, 1.0, -.2), pelr=(-6, 4, 5), cher=(8, 2, -7), hedr=(6, 6, 4), lf=(-2.1, .42, .6), rf=(-2.9, .42, -.5), lkn=(.25, .25, 1), rkn=(-.4, .25, 1), lft=(-80, 30), rft=(-80, 30), lh=(1.9, 1.35, .9), rh=(-.5, 2.05, 2.3), lhand='flat', rhand='relax', lfing=(.4, -.35, .8), lpalm=(0, -1, -.1), rfing=(.4, -.1, .8), rpalm=(0, -1, .1), lel=(1, 0, -.8), rel=(-1, .1, -.3))
S_PALM = S_SIT.set(pelr=(0, 4, 3), cher=(0, 6, -4), hedr=(-3, 24, -2), rh=(-.75, 3.75, 2.55), rhand='open', rfing=(.80, .05, .55), rpalm=(-.1, .92, .25), rel=(-1, -.8, -.2), lh=(1.35, 1.6, 1.5), lel=(1, .1, -.6))
S_LOOKUP = S_STAND.set(hedr=(8, -26, 0), cher=(-2, -8, -5), rh=(-.25, 9.75, 1.45), rfing=(.75, .6, .2), rhand='relax')
S_HEART = S_STAND.set(pelr=(3, 0, 3), cher=(-2, 3, -5), hedr=(-5, 10, 6), rh=(-.62, 10.75, 1.25), rhand='flat', rfing=(.86, .42, .20), rpalm=(0, -.1, -1), rel=(-1, -.9, -.1))
S_STEP = Pose(pel=(0, 8.08, .5), pelr=(-4, 2, 1), cher=(4, 2, -2), hedr=(0, 8, 3), lf=(.28, .82, 1.75), rf=(-.36, .75, -.55), lft=(4, -6), rft=(-14, 10), lkn=(.05, 0, 1), rkn=(-.1, 0, 1), lh=(1.6, 7.6, 1.2), rh=(-.9, 8.6, 2.1), rhand='open', rfing=(.3, .2, 1), rpalm=(.2, .9, 0), rel=(-.8, -.9, -.6), lel=(.7, -.2, -1))
