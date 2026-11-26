"""Hand props.  Every prop returns a Fig; place() builds the world matrix from an origin and two axes."""
import numpy as np, math
from .stage import Fig
from .rig import V, nz
PAL = {3: ('#ffffff', '#805030', 2), 4: ('#c4142c', '#54081c', 3), 5: ('#0f7a58', '#063a34', 3), 6: ('#f7efdc', '#c0a090', 1), 9: ('#7a3d1a', '#34160b', 1), 10: ('#a9b6c6', '#4a5464', 7), 11: ('#f4e7cf', '#b08a7a', 1), 12: ('#8a2a1e', '#3c1010', 1), 13: ('#f2e6c8', '#8a6a50', 1), 14: ('#e8a838', '#8a4a14', 3)}


def _p(kind, bound, step=.8, pal=None, pr=()):
    q = list(pr) + [0.] * (16 - len(pr))
    return Fig('prop%d' % kind, 'props.glsl', {**PAL, **(pal or {})}, bound=bound, step=step, defs='#define KIND %d' % kind, human=False, u=dict(pr=np.array(q, 'f4')))


BOW = _p(0, (0, 0, -1.2, 6.0), pr=(1.0, 4.6)); ARROW = _p(1, (0, 0, 2.6, 3.4), pr=(5.0, 1.)); GADA = _p(2, (0, 2.6, 0, 5.0)); SWORD = _p(3, (0, 2.3, 0, 4.2)); RING = _p(4, (0, .2, 0, 1.9)); DIYA = _p(5, (0, 0, 0, 2.0))
SANDAL = _p(6, (0, 0, 0, 1.7)); SPEAR = _p(7, (0, .8, 0, 7.2)); QUIVER = _p(9, (0, .4, 0, 3.6)); STONE = _p(10, (0, 0, 0, 2.1), pal={9: ('#b8aa98', '#5c5266', 1)}); CROWN = _p(11, (0, .7, 0, 2.0))


def place(origin, y, z, scale=1.):
    """matrix whose local y axis points along y and local z along z (z is made orthogonal)"""
    y = nz(y); z = np.asarray(z, float); z = nz(z - y * (z @ y)); x = np.cross(y, z)
    M = np.eye(4); M[:3, :3] = np.stack([x, y, z], 1) * scale; M[:3, 3] = origin
    return M


def arrow_of(length=5., head=1.15):
    """an arrow of a given length (nock at the origin, flies +z)"""
    return ARROW.variant(u=dict(pr=np.array([length, head] + [0] * 14, 'f4'), bound=(0, 0, length / 2, length / 2 + 1.2)))


def bow_and_arrow(st, S, side='L', arrow=True, up=None, tint=None, fire=0., half=4.6, release=0.):
    """draw a bow in hand `side` of the solved figure S with the string drawn to the other hand.  returns (nock, tip, aim) in world space"""
    o = 'R' if side == 'L' else 'L'; g = S.palm(side, .0, .62, .30); nk = S.palm(o, .22, .95, .34)
    aim = nz(g - nk); pull = float(np.linalg.norm(g - nk)) / S.Sc
    if release > 0: pull = 1. + (pull - 1.) * max(0, 1 - release)
    u = np.asarray(up if up is not None else S.d(V(0, 1, 0)), float)
    b = BOW if tint is None else BOW.variant(pal={9: tint}); b = b.variant(u=dict(pr=np.array([pull, half] + [0] * 14, 'f4')))
    st.fig(b, M=place(g, u - aim * (u @ aim), aim, S.Sc))
    L = max(5., pull + 1.5); tip = nk + aim * L * S.Sc                       # the arrow reaches past the grip
    if arrow: st.fig(arrow_of(L), M=place(nk, u - aim * (u @ aim), aim, S.Sc))
    return nk, tip, aim
