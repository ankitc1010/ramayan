"""VANARAS: the army, and the named kings.  One shader, many looks (see vanara.glsl for the uniforms look, orn, hold, tailW, tailL)."""
import numpy as np, math
from lau.stage import Fig
from lau.rig import Pose, V, nz
from lau.face import Face
from .hanuman import vface, VFace, tail, tail_curve, mirror

DIM = dict(chest=2.85, shx=1.86, shy=.86, shz=-.12, neck=1.22, nz=-.02, head=1.32, hz=.42, up=2.62, fore=2.60, hipx=.60, hipy=-.30, th=2.90, sh=2.80, hand=1.0, foot=1.1)
BUILD = dict(chest=1.02, depth=1.08, rib=.98, waist=1., hips=.96, arm=1.26, leg=1.16, hand=1.24, neck=1.05, shoulder=1.)
WARRIOR_ST = dict(iris='#e8a02a', muzzle='#d99a78', socket='#7a2c28', line='#3a1210', lip='#7a2c2c', lip2='#934038', liphi='#d89a80', tilak=False, brow='#2a1410', cheek='#b8503c')


def _hs(head=1.14, mz=1.2, mw=1.0, ruff=1.0, ear=1.1, brow=1.25, beard=1., nose=1.15): return np.array([head, mz, mw, ruff, ear, brow, beard, nose], 'f4')


def _pal(fur, ruff, skin, light, cloth, band, trim=('#e0a83a', '#7a4418', 1)):
    f = (*fur, 1); return {1: f, 12: f, 13: f, 2: (*ruff, 1), 11: (*skin, 1), 14: (*light, 1), 7: (*cloth, 1), 8: (*band, 1), 16: trim, 3: ('#ffe9bc', '#805030', 2), 4: ('#c4142c', '#54081c', 3), 6: ('#f3e8cf', '#b49a88', 1), 9: ('#6f4423', '#30190d', 1), 10: ('#a39a94', '#544c5c', 1), 15: ('#5d9a3a', '#1f4a34', 1)}


def _fig(name, pal, st, hs, look, orn=0, build=None, dim=None, u=None):
    return Fig(name, 'vanara.glsl', pal, dim={**DIM, **(dim or {})}, build={**BUILD, **(build or {})}, face=lambda F, k=st: vface(F, k, S=640 if look < 4 else 1280), bound=(0, 8, 0, 16.), step=.78, u={**dict(HS=hs, look=look, orn=orn, hold=0, tailW=0., tailL=7.0), **(u or {})})


WARRIOR = _fig('vwarrior', _pal(('#8a5a34', '#43261c'), ('#a8743f', '#553222'), ('#c8705a', '#6c2c34'), ('#c49a68', '#6e4a36'), ('#b0552a', '#561f18'), ('#a82a2a', '#521020')), WARRIOR_ST, _hs(), 0, orn=1 | 4)
LANGUR = _fig('vlangur', _pal(('#a9a7a6', '#565468'), ('#ece6da', '#8e8798'), ('#3a3136', '#15111c'), ('#d2cdc6', '#7a7688'), ('#3f6f8a', '#1c3550'), ('#d8a23a', '#7a4a1c'), ('#f0e2c0', '#8a7a68', 1)),
              dict(WARRIOR_ST, muzzle='#4c4148', cheek='#2a2226', socket='#1a1418', line='#0c080c', lip='#2a1c22', lip2='#5a4448', liphi='#8a747a', brow='#e8e2d6', iris='#f0b43a', kohl='#0a0608', mouthin='#5a1a24'), _hs(1.12, 1.12, .92, 1.25, 1.0, 1.15, 1.2, .95), 1, orn=2, build=dict(arm=1.10, leg=1.02, chest=.94, waist=.92), u=dict(tailL=9.5))
YOUTH = _fig('vyouth', _pal(('#e0a23e', '#8e5124'), ('#f3cf80', '#ad7434'), ('#e58a64', '#934038'), ('#f6d892', '#b07c48'), ('#3f8a5a', '#17423a'), ('#c4222c', '#660f22')),
             dict(WARRIOR_ST, muzzle='#f3b48a', socket='#b8503a', line='#5a2018', lip='#a8443c', lip2='#bf5a4a', brow='#7a4a1c', browt=.8, eye=1.14), _hs(1.14, 1.0, .95, .85, 1.2, .9, .7, 1.), 2, orn=8, build=dict(arm=1.06, leg=1.0, chest=.92, waist=.9, neck=.95), dim=dict(shx=1.66, up=2.5, fore=2.5), u=dict(tailL=8.0))
JAMBAVAN = _fig('jambavan', _pal(('#4a3a34', '#1d1620'), ('#63504a', '#2a2026'), ('#5a463c', '#261c22'), ('#6d584c', '#2f242c'), ('#8a2a2a', '#42101c'), ('#8a2a2a', '#42101c')),
                dict(WARRIOR_ST, muzzle='#c9a884', cheek='#4a362e', nosepad='#1c1216', eye=.88, socket='#2a1c1e', line='#1c0f12', lip='#3a2224', lip2='#6a4640', brow='#d8d2c6', browt=1.5, iris='#c87a2a', old=1.), _hs(1.28, 1.52, .84, 1.4, .80, 1.15, 1.7, 1.05), 3, orn=2, build=dict(chest=1.26, depth=1.24, waist=1.30, hips=1.18, rib=1.22, arm=1.62, leg=1.46, belly=.85, hand=1.44, neck=1.35), dim=dict(shx=2.18, hipx=.78), u=dict(tailL=0.))
SUGRIVA = _fig('sugriva', _pal(('#c8662c', '#6e2c1c'), ('#e8a85c', '#95502a'), ('#e08058', '#8c3a38'), ('#eab872', '#995a38'), ('#6a2a7a', '#2c1040'), ('#e0a83a', '#7a4418'), ('#e8a42c', '#8a4214', 1)),
               dict(WARRIOR_ST, muzzle='#f0ac82', socket='#a03c30', line='#4a1614', lip='#983434', lip2='#b04c44', brow='#3a1a12', tilak=True), _hs(1.18, 1.18, 1.0, 1.1, 1.1, 1.15, 1.2, 1.05), 4, build=dict(chest=1.12, depth=1.14, arm=1.42, leg=1.26, hand=1.32, neck=1.12), dim=dict(shx=2.06, th=3.0, sh=2.95))
ANGADA = _fig('angada', _pal(('#eab03a', '#95581e'), ('#fadf94', '#b8823c'), ('#ea8f6a', '#98443c'), ('#fbe3a0', '#b98a50'), ('#1f7a8a', '#0c3448'), ('#e0a83a', '#7a4418'), ('#e8a42c', '#8a4214', 1)),
              dict(WARRIOR_ST, muzzle='#f7bd94', socket='#c05a40', line='#5a2018', lip='#a8443c', lip2='#bf5a4a', brow='#6a3a16', eye=1.12, tilak=True), _hs(1.16, 1.04, .96, .95, 1.15, 1., .7, 1.), 5, build=dict(chest=1.04, arm=1.28, leg=1.16, neck=1.02), dim=dict(th=3.0, sh=2.95))
# cloth, band and ornament variants for the ranks
WARRIOR2 = WARRIOR.variant(pal={1: ('#6e4a38', '#33201e', 1), 12: ('#6e4a38', '#33201e', 1), 13: ('#6e4a38', '#33201e', 1), 2: ('#8d6446', '#452a22', 1), 7: ('#8a8a3a', '#42421c', 1), 8: ('#d8a23a', '#7a4a1c', 1)}, u=dict(orn=2))
YOUTH2 = YOUTH.variant(pal={1: ('#cf7a3a', '#7a3820', 1), 12: ('#cf7a3a', '#7a3820', 1), 13: ('#cf7a3a', '#7a3820', 1), 2: ('#e8b070', '#9a5c34', 1), 7: ('#c4382c', '#661422', 1)}, u=dict(orn=1 | 8))
LANGUR2 = LANGUR.variant(pal={7: ('#b0552a', '#561f18', 1), 8: ('#a82a2a', '#521020', 1)}, u=dict(orn=1 | 4))
KINDS = [WARRIOR, LANGUR, YOUTH, WARRIOR2, YOUTH2, LANGUR2, JAMBAVAN]


def arm(fig, hold=0, tailw=0.): return fig.variant(u=dict(hold=int(hold), tailW=float(tailw)))


# ------------------------------------------------------------------ poses
GY = .86
V_STAND = Pose(pel=(0, 6.45, 0), pelr=(0, 8, 0), cher=(0, 10, 0), hedr=(0, -16, 0), lf=(1.0, GY, .2), rf=(-1.0, GY, .2), lkn=(.3, 0, 1), rkn=(-.3, 0, 1), lft=(20, 0), rft=(-20, 0), lh=(2.9, 5.6, 1.4), rh=(-2.9, 5.6, 1.4), lel=(1, 0, -.6), rel=(-1, 0, -.6))


def V_RUN(ph, stride=3.0, lift=2.2):
    """a loping run, ph 0..1"""
    a = 2 * math.pi * ph; c = math.cos(a)

    def foot(p):
        p %= 1.
        if p < .36: q = p / .36; return stride * .75 * (1 - 2 * q) - .3, 0., 34 * q
        q = (p - .36) / .64; return -stride * .75 - .3 + 1.5 * stride * (q * q * (3 - 2 * q)), lift * math.sin(math.pi * q) ** .8, 66 * (1 - q)
    lz, ly, lp = foot(ph); rz, ry, rp = foot(ph + .5)
    return Pose(pel=(0, 5.85 + .45 * math.sin(2 * a + .6), 0), pelr=(12 * c, 20, 0), cher=(-26 * c, 18, 0), hedr=(12 * c, -28, 0), lf=(.65, GY + ly, lz), rf=(-.65, GY + ry, rz), lft=(6, lp), rft=(-6, rp), lh=(2.7, 6.8 - .8 * c, 2.2 - 2.7 * c), rh=(-2.7, 6.8 + .8 * c, 2.2 + 2.7 * c), lel=(.8, -.2, -1), rel=(-.8, -.2, -1), lhand='fist', rhand='grip', rfing=(.25, -.5, .8), rpalm=(1, 0, 0), lkn=(.25, 0, 1), rkn=(-.25, 0, 1))


def V_CHARGE(ph):
    """the run with the right arm raised, for a weapon in the hand"""
    c = math.cos(2 * math.pi * ph); return V_RUN(ph).set(rh=(-2.6, 11.6 + .4 * c, 1.2 + .5 * c), rel=(-1, .1, -.2), rfing=(.1, .6, .8), rpalm=(.9, .1, -.3), hedr=(4 * c, -30, 0))


def V_CHEER(ph):
    """jumping with both arms up"""
    q = ph % 1.; h = max(0., math.sin(math.pi * min(1., max(0., (q - .25) / .6)))); k = 1 - min(1, abs(q - .12) / .14) if q < .26 else 0.; w = math.sin(2 * math.pi * q)
    return Pose(pel=(0, 6.35 + 1.5 * h - 1.0 * k, 0), pelr=(0, 6 + 10 * k, 4 * w), cher=(0, -8 * h + 10 * k, -4 * w), hedr=(0, -18, 6 * w), lf=(1.0 + .2 * h, GY + 1.35 * h, .2 - .4 * h), rf=(-1.0 - .2 * h, GY + 1.25 * h, .2 - .7 * h), lft=(18, 40 * h), rft=(-18, 46 * h), lkn=(.4, 0, 1), rkn=(-.4, 0, 1),
                lh=(3.0 - .4 * h + .3 * w, 12.4 + 1.9 * h - 2.2 * k, 1.0), rh=(-3.0 + .4 * h + .3 * w, 12.4 + 1.9 * h - 2.2 * k, 1.0), lel=(1, -.2, -.3), rel=(-1, -.2, -.3), lhand='open', rhand='fist', lfing=(.2, 1, .1), rfing=(-.1, 1, .1), lpalm=(-.2, 0, 1), rpalm=(.3, 0, 1))


_TH = [V_STAND.set(pel=(-.4, 5.9, -.5), pelr=(-24, -2, -6), cher=(-30, -10, -6), hedr=(44, -2, 0), rh=(-3.4, 11.2, -2.2), lh=(2.2, 9.6, 3.4), lf=(.9, GY + 1.4, 2.4), rf=(-1.2, GY, -1.2), lft=(8, -10), rft=(-40, 0), rel=(-1, .2, -.3), lel=(.8, -.6, .2), rhand='claw', lhand='open', rfing=(-.1, .7, -.7), rpalm=(.2, .7, .7), lfing=(0, .5, .9), lpalm=(-.5, -.4, .6)),
       V_STAND.set(pel=(0, 6.1, .5), pelr=(14, 12, 4), cher=(22, 8, 4), hedr=(-28, -10, 0), rh=(-1.6, 12.4, 3.4), lh=(3.2, 7.0, -.6), lf=(1.0, GY, 2.5), rf=(-1.1, GY + .1, -1.8), lft=(8, 0), rft=(-30, 20), rel=(-1, .1, 0), lel=(.8, 0, -1), rhand='claw', lhand='fist', rfing=(.1, .75, .65), rpalm=(0, -.4, .9)),
       V_STAND.set(pel=(.2, 5.4, 1.1), pelr=(24, 22, 4), cher=(26, 26, 4), hedr=(-34, -28, 0), rh=(.9, 5.6, 4.8), lh=(3.6, 7.0, -2.0), lf=(1.0, GY, 2.9), rf=(-1.1, GY + .4, -2.3), lft=(8, 0), rft=(-24, 40), rel=(-.8, .6, .2), lel=(.6, .3, -1), rhand='open', lhand='fist', rfing=(.5, -.5, .7), rpalm=(0, -.6, -.6))]


def V_THROW(t):
    """a throw, t 0 wound up, .5 release, 1 followed through"""
    t = max(0., min(1., t)); return _TH[0].mix(_TH[1], t * 2) if t < .5 else _TH[1].mix(_TH[2], t * 2 - 1)


_UP = dict(lh=(1.75, 13.2, .9), rh=(-1.75, 13.2, .9), lel=(1, -.3, .1), rel=(-1, -.3, .1), lhand='open', rhand='open', lfing=(.25, .30, -.9), rfing=(-.25, .30, -.9), lpalm=(-.35, .95, .2), rpalm=(.35, .95, .2), hedr=(0, -14, 0))
V_CARRY = V_STAND.set(cher=(0, -4, 0), pelr=(0, 2, 0), **_UP)


def V_WALK(ph, stride=1.6, lift=.9):
    a = 2 * math.pi * ph; c, s = math.cos(a), math.sin(a)

    def foot(p):
        p %= 1.
        if p < .5: return stride * (1 - 4 * p), 0., (-14 * (1 - p / .1) if p < .1 else (34 * ((p - .35) / .15) if p > .35 else 0))
        q = (p - .5) / .5; return -stride + 2 * stride * (q * q * (3 - 2 * q)), lift * math.sin(math.pi * q), (34 * (1 - q * 2) if q < .5 else -14 * (q - .5) * 2)
    lz, ly, lp = foot(ph); rz, ry, rp = foot(ph + .5)
    return Pose(pel=(0, 6.2 - .2 * abs(c), 0), pelr=(9 * c, 8, 2 * s), cher=(-16 * c, 8, -2 * s), hedr=(7 * c, -14, 0), lf=(.85, GY + ly, lz), rf=(-.85, GY + ry, rz), lft=(14, lp), rft=(-14, rp), lh=(2.8, 5.9 + .2 * abs(c), 1.3 - 1.5 * c), rh=(-2.8, 5.9 + .2 * abs(c), 1.3 + 1.5 * c), lel=(.8, 0, -1), rel=(-.8, 0, -1), rhand='grip', lkn=(.25, 0, 1), rkn=(-.25, 0, 1))


def V_CARRY_WALK(ph):
    """walking under a stone held on both hands"""
    return V_WALK(ph, stride=1.35).set(cher=(0, -4, 0), **_UP)


V_CLIMB = Pose(pel=(0, 6.2, -.6), pelr=(-6, 4, 6), cher=(10, -2, -10), hedr=(0, -24, 0), lf=(1.5, 4.0, .9), rf=(-1.1, 1.4, .7), lkn=(.9, .4, .6), rkn=(-.8, 0, .7), lft=(20, 30), rft=(-20, 40), lh=(2.2, 9.6, 1.7), rh=(-2.0, 13.0, 1.4), lel=(1, -.4, -.2), rel=(-1, -.2, -.2), lhand='claw', rhand='claw', lfing=(0, 1, .3), rfing=(0, 1, .3), lpalm=(0, -.2, 1), rpalm=(0, -.2, 1))


V_CLIMB2 = mirror(V_CLIMB)
