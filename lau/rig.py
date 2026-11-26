"""Skeleton, poses, inverse kinematics, hands.  Figure space: y up, z forward, +x = the figure's own left; 1 unit = half a head."""
import numpy as np, math, copy
from dataclasses import dataclass, field, replace, fields
V = lambda *a: np.array(a, float)


def nz(v):
    v = np.asarray(v, float); n = np.linalg.norm(v)
    return v / n if n > 1e-9 else V(0, 1, 0)


def Rx(d): c, s = math.cos(math.radians(d)), math.sin(math.radians(d)); return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
def Ry(d): c, s = math.cos(math.radians(d)), math.sin(math.radians(d)); return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
def Rz(d): c, s = math.cos(math.radians(d)), math.sin(math.radians(d)); return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


def eul(yaw=0, pitch=0, roll=0):
    """yaw turns to the figure's left, pitch bows forward, roll leans to the figure's left"""
    return Ry(yaw) @ Rx(pitch) @ Rz(-roll)


def ik2(a, c, l1, l2, pole):
    """two-bone IK: elbow and reached end"""
    d = c - a; L = np.linalg.norm(d); m = l1 + l2
    if L > m * .9995: d = d * (m * .9995 / L); L = m * .9995; c = a + d
    if L < abs(l1 - l2) + 1e-3: L = abs(l1 - l2) + 1e-3; d = nz(d) * L; c = a + d
    u = d / L; x = (l1 * l1 - l2 * l2 + L * L) / (2 * L); h = math.sqrt(max(l1 * l1 - x * x, 0))
    p = np.asarray(pole, float); p = p - u * (p @ u); p = nz(p) if np.linalg.norm(p) > 1e-6 else nz(np.cross(u, V(.3, .2, 1)))
    return a + u * x + p * h, c


# ------------------------------------------------------------------ hands
# finger: (curl at base, middle, tip in degrees ; spread)   order thumb, index, middle, ring, little
HANDS = dict(
    open=dict(c=[(12, 10, 5), (4, 6, 4), (3, 5, 4), (4, 6, 4), (6, 8, 5)], sp=[0, 6, 1, -5, -11], th=(48, 10)),
    relax=dict(c=[(20, 18, 12), (22, 28, 14), (28, 32, 16), (32, 36, 18), (36, 40, 20)], sp=[0, 4, 1, -3, -7], th=(40, 22)),
    fist=dict(c=[(40, 45, 35), (82, 95, 60), (84, 98, 62), (86, 98, 62), (88, 98, 60)], sp=[0, 2, 0, -2, -4], th=(20, 52)),
    grip=dict(c=[(38, 36, 28), (66, 78, 46), (68, 80, 48), (70, 82, 50), (72, 84, 50)], sp=[0, 3, 0, -2, -5], th=(28, 50)),
    hold=dict(c=[(30, 28, 18), (48, 52, 28), (50, 54, 30), (52, 56, 32), (54, 58, 32)], sp=[0, 3, 0, -2, -5], th=(34, 46)),
    point=dict(c=[(40, 40, 30), (2, 4, 2), (84, 96, 60), (86, 98, 60), (88, 98, 60)], sp=[0, 2, 0, -2, -4], th=(22, 50)),
    two=dict(c=[(44, 44, 30), (2, 3, 2), (2, 3, 2), (86, 98, 60), (88, 98, 60)], sp=[0, 8, -6, -2, -4], th=(18, 56)),
    draw=dict(c=[(30, 36, 20), (54, 72, 30), (56, 74, 30), (60, 78, 36), (84, 96, 60)], sp=[0, 2, 0, -1, -4], th=(26, 40)),
    anjali=dict(c=[(6, 4, 2), (2, 2, 1), (1, 2, 1), (2, 2, 1), (3, 3, 2)], sp=[0, 1, 0, -1, -2], th=(26, 4)),
    abhaya=dict(c=[(10, 8, 4), (-4, 4, 2), (-5, 3, 2), (-4, 4, 2), (-2, 5, 3)], sp=[0, 3, 0, -3, -7], th=(40, 4)),
    cup=dict(c=[(26, 20, 10), (26, 30, 22), (28, 32, 24), (30, 34, 24), (32, 36, 26)], sp=[0, 2, 0, -2, -4], th=(38, 34)),
    claw=dict(c=[(26, 30, 30), (18, 52, 46), (18, 54, 46), (20, 54, 46), (22, 54, 46)], sp=[0, 14, 3, -9, -18], th=(52, 20)),
    flat=dict(c=[(8, 8, 4), (0, 2, 1), (0, 2, 1), (0, 2, 1), (0, 3, 2)], sp=[0, 2, 0, -2, -4], th=(34, 4)),
    pinch=dict(c=[(34, 34, 18), (46, 54, 28), (14, 20, 12), (12, 18, 10), (14, 18, 10)], sp=[0, 2, -2, -7, -12], th=(34, 44)),
    katak=dict(c=[(30, 34, 22), (52, 56, 24), (54, 58, 26), (12, 14, 8), (8, 10, 6)], sp=[0, 2, 0, -10, -18], th=(30, 46)),
)
_MCP = [V(.24, .12, .05), V(.255, .80, .0), V(.085, .84, .01), V(-.09, .81, .0), V(-.25, .73, -.01)]
_LEN = [(.40, .32, .26), (.42, .28, .22), (.46, .31, .23), (.42, .29, .22), (.33, .22, .19)]
_RAD = [(.15, .125, .115, .085), (.118, .105, .096, .075), (.122, .108, .098, .076), (.116, .103, .094, .074), (.102, .090, .082, .064)]


def hand_points(kind, side):
    """finger joints in the hand frame (x toward the thumb for the RIGHT hand seen from the palm .. mirrored for left), y along the fingers, z out of the palm"""
    h = HANDS[kind] if isinstance(kind, str) else kind
    out = []
    for f in range(5):
        p = _MCP[f].copy(); c = h['c'][f]; sp = h['sp'][f]
        if f == 0:
            sw, opp = h['th']            # thumb: swing out of the palm plane, opposition across it
            d = nz(V(math.sin(math.radians(sw)), math.cos(math.radians(sw)), math.sin(math.radians(opp)) * .9)); bend = nz(np.cross(d, V(.35, .1, 1)))
            pts = [p]
            for k in range(3):
                a = math.radians(c[k] * (.5 if k == 0 else 1)); d = nz(d * math.cos(a) + nz(V(-.75, .25, .55) - d * (V(-.75, .25, .55) @ d)) * math.sin(a)); p = p + d * _LEN[f][k]; pts.append(p)
        else:
            s = math.radians(sp); d = V(math.sin(s), math.cos(s), 0); pts = [p]; ang = 0
            for k in range(3):
                ang += math.radians(c[k]); dd = nz(d * math.cos(ang) + V(0, 0, 1) * math.sin(ang)); p = p + dd * _LEN[f][k]; pts.append(p)
        out.append(pts)
    P = np.array(out)                    # 5,4,3
    return P


# ------------------------------------------------------------------ pose
@dataclass
class Pose:
    """All angles in degrees (yaw, pitch, roll), all positions in figure units relative to the figure origin (ground between the feet)."""
    pel: tuple = (0, 8.35, 0)            # pelvis position
    pelr: tuple = (0, 0, 0)              # pelvis yaw, pitch, roll
    cher: tuple = (0, 0, 0)              # chest relative to the pelvis
    hedr: tuple = (0, 0, 0)              # head relative to the chest
    lh: tuple = None                     # left hand (wrist) target in figure space; None = hangs
    rh: tuple = None
    lel: tuple = (.6, -.35, -.8)         # elbow pole directions, figure space
    rel: tuple = (-.6, -.35, -.8)
    lhand: str = 'relax'                 # name in rig.HANDS
    rhand: str = 'relax'
    lfing: tuple = None                  # direction of the fingers (figure space); None = along the forearm
    rfing: tuple = None
    lpalm: tuple = None                  # direction the palm faces; None = toward the body
    rpalm: tuple = None
    lf: tuple = (.75, .75, .1)           # ankle targets
    rf: tuple = (-.75, .75, .1)
    lkn: tuple = (.12, 0, 1)             # knee poles
    rkn: tuple = (-.12, 0, 1)
    lft: tuple = (14, 0)                 # foot yaw, pitch (pitch>0 = toes down)
    rft: tuple = (-14, 0)
    shrug: tuple = (0, 0)                # raise of left/right shoulder
    ext: dict = field(default_factory=dict)   # character extras (tail, jaw ...)

    def mix(self, o, t):
        """blend toward another pose"""
        d = {}
        for f in fields(self):
            a, b = getattr(self, f.name), getattr(o, f.name)
            if f.name == 'ext': d[f.name] = {**a, **b}; continue
            if isinstance(a, str) or isinstance(b, str): d[f.name] = a if t < .5 else b; continue
            if a is None or b is None: d[f.name] = a if t < .5 else b; continue
            d[f.name] = tuple((1 - t) * np.asarray(a, float) + t * np.asarray(b, float))
        return Pose(**d)

    def set(self, **k): return replace(self, **k)


DIM = dict(chest=3.0, shx=1.66, shy=1.08, shz=-.12, neck=1.38, nz=-.16, head=1.56, hz=.14, up=2.70, fore=2.45, hipx=.62, hipy=-.30, th=3.75, sh=3.55, hand=1.08, foot=1.0, heady=1.0)
BUILD = dict(chest=1., depth=1., rib=1., waist=1., hips=1., arm=1., leg=1., hand=1., bust=0., belly=0., neck=1., shoulder=1.)


def solve(pose, dim=DIM, build=BUILD):
    """Pose -> dict of shader uniforms (joints, frames, finger joints) plus named joints"""
    D = {**DIM, **dim}; pr = eul(*pose.pelr); pel = np.asarray(pose.pel, float)
    cr = pr @ eul(*pose.cher); mid = nz(pr @ V(0, 1, 0) + cr @ V(0, 1, 0))
    che = pel + pr @ V(0, 1, 0) * D['chest'] * .42 + mid * D['chest'] * .20 + cr @ V(0, 1, 0) * D['chest'] * .38
    hr = cr @ eul(*pose.hedr)
    neck = che + cr @ V(0, D['neck'], D['nz']); head = neck + (cr @ V(0, 1, 0) * .45 + hr @ V(0, 1, 0) * .55) * D['head'] + hr @ V(0, 0, D['hz'])
    J = np.zeros((20, 3)); J[0], J[1], J[2], J[3] = pel, che, neck, head
    up = dict(L=1, R=-1); HFp = np.zeros((40, 4)); frames = {}
    for k, (nm, sg) in enumerate(up.items()):
        sh = che + cr @ V(sg * D['shx'] * build.get('shoulder', 1.), D['shy'] + pose.shrug[k] * .3, D['shz'])
        tgt = pose.lh if nm == 'L' else pose.rh; pole = pose.lel if nm == 'L' else pose.rel
        if tgt is None: tgt = sh + cr @ V(sg * .55, -(D['up'] + D['fore']) * .965, .45)
        el, wr = ik2(sh, np.asarray(tgt, float), D['up'], D['fore'], pole)
        b = 4 + k * 3; J[b], J[b + 1], J[b + 2] = sh, el, wr
        fg = pose.lfing if nm == 'L' else pose.rfing; pm = pose.lpalm if nm == 'L' else pose.rpalm
        y = nz(fg) if fg is not None else nz(wr - el)
        z = np.asarray(pm, float) if pm is not None else cr @ V(-sg, 0, .25)
        z = z - y * (z @ y); z = nz(z) if np.linalg.norm(z) > 1e-6 else nz(np.cross(y, V(.1, .2, 1)))
        # thumb side: for the right hand, palm facing z, fingers y -> thumb at +x = y cross z ; mirrored for the left
        x = np.cross(y, z) if nm == 'R' else -np.cross(y, z)
        M = np.stack([x, y, z]); frames[nm] = M
        hs = D['hand'] * build.get('hand', 1.)
        P = hand_points(pose.lhand if nm == 'L' else pose.rhand, nm) * hs
        Pw = P.reshape(-1, 3) @ M + wr
        HFp[k * 20:k * 20 + 20, :3] = Pw; HFp[k * 20:k * 20 + 20, 3] = np.array(_RAD).reshape(-1) * hs
    for k, (nm, sg) in enumerate(up.items()):
        hp = pel + pr @ V(sg * D['hipx'], D['hipy'], 0); tgt = pose.lf if nm == 'L' else pose.rf; pole = pose.lkn if nm == 'L' else pose.rkn
        kn, an = ik2(hp, np.asarray(tgt, float), D['th'], D['sh'], pr @ np.asarray(pole, float)); b = 10 + k * 4
        fy, fp = pose.lft if nm == 'L' else pose.rft
        Rf = Ry(fy) @ Rx(fp); s = D['foot']
        J[b], J[b + 1], J[b + 2] = hp, kn, an; J[b + 3] = an + Rf @ V(0, -.52 * s, 1.42 * s); J[18 + k] = an + Rf @ V(0, -.50 * s, -.34 * s)
    bl = [build.get(k, d) for k, d in (('chest', 1.), ('depth', 1.), ('rib', 1.), ('waist', 1.), ('hips', 1.), ('arm', 1.), ('leg', 1.), ('hand', 1.), ('bust', 0.), ('belly', 0.), ('neck', 1.), ('shoulder', 1.))]
    bl[7] = D['hand'] * build.get('hand', 1.)
    return dict(J=J, Bp=pr.T, Bc=cr.T, Bh=hr.T, BL=frames['L'], BR=frames['R'], HF=HFp, B=np.array(bl))


def palm_point(S, side, x=0., y=.62, z=.16):
    """a point on the palm (figure space) for props: side 'L' or 'R'"""
    M = S['BL'] if side == 'L' else S['BR']; w = S['J'][6 if side == 'L' else 9]; hs = S['B'][7]
    return w + (V(x, y, z) * hs) @ M
