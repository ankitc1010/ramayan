"""One arm for close inserts.  ARM.variant(pal={1: (base, shadow, 1)}, u=dict(side=1, band=1, old=0.)).  place_tip() puts a fingertip on a world point with the hand pointing along a direction."""
import numpy as np, math
from lau.stage import Fig
from lau.rig import V, nz
from .rama import PAL, BLUE
ARM = Fig('arm', 'armonly.glsl', PAL, u=dict(side=1, band=2, old=0., fur=0., fore=0., furB=(.76, .25, .035), furS=(.25, .045, .012)))
RAMA_ARM = ARM
HANUMAN_ARM = ARM.variant(pal={1: ('#d8683c', '#7c2c1c', 1)}, u=dict(side=1, band=1, fur=1.), build=dict(arm=1.42, hand=1.38))
SKIN = dict(rama=BLUE, gold=('#d9a066', '#86502f', 1), sita=('#dca070', '#8f5236', 1), old=('#b87f56', '#5f3626', 1), child=('#d49468', '#8a4e34', 1), hanuman=('#d8683c', '#7c2c1c', 1))


def align(a, b):
    """rotation taking unit a to unit b"""
    v = np.cross(a, b); s = np.linalg.norm(v); c = float(a @ b); K = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    if s < 1e-8: return np.eye(3) if c > 0 else np.diag([1., -1., -1.])
    return np.eye(3) + K + K @ K * ((1 - c) / (s * s))


def about(ax, deg):
    K = np.cross(nz(ax), np.eye(3)).T; t = math.radians(deg)
    return np.eye(3) + math.sin(t) * K + (1 - math.cos(t)) * K @ K


def frame_to(y0, z0, y1, z1):
    """rotation taking the frame (y0,z0) to (y1,z1)"""
    def F(y, z): y = nz(y); z = np.asarray(z, float); z = nz(z - y * (z @ y)); return np.stack([np.cross(y, z), y, z], 1)
    return F(y1, z1) @ F(y0, z0).T


def place_hand(S, side, at, fingers, palm, scale=1., anchor='palm'):
    """matrix for st.fig(M=...) so that the hand of solved pose S has its palm (or finger tip 'tip1'..) at `at`, fingers along `fingers`, palm facing `palm`"""
    B = S.u['BR' if side == 'R' else 'BL']; R = frame_to(B[1], B[2], fingers, palm); k = 20 if side == 'R' else 0
    if anchor.startswith('tip'): p = S.u['HF'][k + int(anchor[3:]) * 4 + 3, :3]
    elif anchor == 'wrist': p = S.J[9 if side == 'R' else 6]
    else:
        from lau.rig import palm_point
        p = palm_point(S.u, side)
    M = np.eye(4); M[:3, :3] = R * scale; M[:3, 3] = np.asarray(at, float) - R @ p * scale
    return M
