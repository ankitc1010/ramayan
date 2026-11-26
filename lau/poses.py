"""A library of poses (figure units, y up, z forward, +x = figure's left)."""
import math
from .rig import Pose, V

STAND = Pose()
CONTRA = Pose(pel=(.25, 8.25, 0), pelr=(8, 0, 4), cher=(-6, 0, -7), hedr=(-6, 2, 4), lf=(.85, .75, .1), rf=(-.75, .75, .55), lh=(2.3, 7.9, .9), rh=(-1.7, 9.2, 1.4), lhand='relax', rhand='relax')


def archer(draw=1., low=0.):
    """side-on archer: bow in the LEFT hand toward +x, string hand at the chin.  draw 0..1"""
    d = draw
    return Pose(pel=(-.1, 7.75 - low, 0), pelr=(18, 0, 0), cher=(-20, 0, 1), hedr=(74, 2, 0), shrug=(.1, .35),
                lh=(6.95, 12.10 - low, .75), rh=(1.15 - 2.35 * d, 12.25 - low, 1.25), lel=(0, -1, -.35), rel=(-1, .35, -.25),
                lhand='grip', rhand='draw', lfing=(.35, .1, .95), lpalm=(.9, -.1, -.4), rfing=(.80, .05, .55), rpalm=(.25, -.1, -1),
                lf=(2.5, .75, .5), rf=(-2.5, .75, -.3), lft=(72, 0), rft=(-8, 0), lkn=(.9, 0, .6), rkn=(-.5, 0, 1))


def walk(ph, stride=1.7, lift=.9, bounce=.22, swing=1.4):
    """walk cycle, ph in 0..1; walks toward +z"""
    a = 2 * math.pi * ph; s, c = math.sin(a), math.cos(a)

    def foot(p):
        p %= 1.
        if p < .5: z = stride * (1 - 4 * p); y = 0.; pt = -14 * (1 - p / .1) if p < .1 else (34 * ((p - .35) / .15) if p > .35 else 0)
        else: q = (p - .5) / .5; z = -stride + 2 * stride * (q * q * (3 - 2 * q)); y = lift * math.sin(math.pi * q) ; pt = 34 * (1 - q * 2) if q < .5 else -14 * (q - .5) * 2
        return z, y, pt
    lz, ly, lp = foot(ph); rz, ry, rp = foot(ph + .5)
    return Pose(pel=(0, 8.1 - bounce * abs(math.cos(a)) * .9, 0), pelr=(9 * math.cos(a), 3, 2 * s), cher=(-15 * math.cos(a), 2, -2 * s), hedr=(6 * math.cos(a), -2, 0),
                lf=(.55, .75 + ly, lz), rf=(-.55, .75 + ry, rz), lft=(6, lp), rft=(-6, rp),
                lh=(2.1, 7.9 + .25 * abs(c), .4 - swing * c), rh=(-2.1, 7.9 + .25 * abs(c), .4 + swing * c), lel=(.4, 0, -1), rel=(-.4, 0, -1))


def run(ph, stride=2.9, lift=2.2, lean=18):
    a = 2 * math.pi * ph; s, c = math.sin(a), math.cos(a)

    def foot(p):
        p %= 1.
        if p < .38: q = p / .38; z = stride * .75 * (1 - 2 * q) - .2; y = .0; pt = 30 * q
        else: q = (p - .38) / .62; z = -stride * .75 - .2 + 1.5 * stride * (q * q * (3 - 2 * q)); y = lift * math.sin(math.pi * q) ** .8; pt = 60 * (1 - q)
        return z, y, pt
    lz, ly, lp = foot(ph); rz, ry, rp = foot(ph + .5)
    return Pose(pel=(0, 7.9 + .45 * math.sin(2 * a + .6), 0), pelr=(12 * c, lean * .6, 0), cher=(-26 * c, lean * .5, 0), hedr=(12 * c, -lean * .7, 0), lf=(.5, .75 + ly, lz), rf=(-.5, .75 + ry, rz), lft=(4, lp), rft=(-4, rp),
                lh=(1.9, 10.0 - .6 * c, 1.0 - 2.1 * c), rh=(-1.9, 10.0 + .6 * c, 1.0 + 2.1 * c), lel=(.5, -.3, -1), rel=(-.5, -.3, -1), lhand='fist', rhand='fist')


KNEEL = Pose(pel=(0, 4.7, 0), pelr=(0, 4, 0), cher=(0, 4, 0), lf=(.8, .75, 2.1), rf=(-.8, 1.5, -3.0), lkn=(.15, .4, 1), rkn=(-.2, -.5, 1), rft=(0, 72), lh=(1.6, 5.6, 2.7), rh=(-1.9, 6.1, 1.4))
BOW_DOWN = KNEEL.set(cher=(0, 24, 0), hedr=(0, 22, 0), lh=(.30, 6.6, 3.9), rh=(-.30, 6.6, 3.9), lhand='anjali', rhand='anjali', lfing=(0, 1, .25), rfing=(0, 1, .25), lpalm=(-1, 0, 0), rpalm=(1, 0, 0))
ANJALI = Pose(lh=(.30, 11.0, 2.2), rh=(-.30, 11.0, 2.2), lhand='anjali', rhand='anjali', lfing=(0, 1, .3), rfing=(0, 1, .3), lpalm=(-1, 0, 0), rpalm=(1, 0, 0), lel=(1, -.6, -.2), rel=(-1, -.6, -.2))
SIT = Pose(pel=(0, 1.35, 0), cher=(0, 2, 0), lf=(-.9, .55, 2.3), rf=(.9, .75, 2.0), lkn=(1, .25, .5), rkn=(-1, .25, .5), lft=(-80, 20), rft=(80, 20), lh=(2.2, 2.0, 2.7), rh=(-2.2, 2.0, 2.7), lel=(1, .2, -.4), rel=(-1, .2, -.4))
BLESS = STAND.set(rh=(-2.2, 11.3, 2.0), rhand='abhaya', rfing=(-.05, 1, .05), rpalm=(0, 0, 1), rel=(-.7, -1, -.3))
