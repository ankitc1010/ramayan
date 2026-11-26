"""Jatayu, the old king of vultures.  Wingspan about 62 units; flies toward +z, y up, origin between the shoulders.

    from chars import jatayu as JT
    S = JT.draw(st, JT.flap(ph), at=(0, 40, 0), yaw=.., pitch=.., roll=..)      # or M=4x4
    S.p('beak'), S.p('head'), S.p('talonL'), S.p('tipL'), S.p('wristR'), S.p('back')      world points
Poses: flap(ph) glide(t) dive(t) brake(t) strike(t) wing_lost(t, side) lying(t).  JPose.mix blends any two."""
import numpy as np, math, cairo
from dataclasses import dataclass, replace, fields
from lau.stage import Fig, model, hexc
from lau.rig import V, nz, Rx, Ry, Rz, eul
from lau.face import Face, Pen, rgb
from lau import cloth as CL
from chars.deer import track


# ------------------------------------------------------------------ feathers
FEATHER = '''#include "noise.glsl"
in vec3 vp,vn_;in vec2 vuv;
layout(location=0) out vec4 g0;layout(location=1) out vec4 g1;layout(location=2) out vec4 g2;layout(location=3) out vec4 g3;
uniform vec3 ro;uniform mat3 CamR;uniform float far,objId,inkw,gild,bars,ragged,asp;uniform int shape;uniform vec3 cA,cB,cC,cE;uniform float tipAt,burnF;
void main(){
  vec3 n=normalize(vn_),v=vp-ro;if(dot(n,v)>0.) n=-n;vec3 f=transpose(CamR)[2];float vz=dot(v,f);gl_FragDepth=clamp(vz/far,0.,1.);
  float id=floor(vuv.x),u=fract(vuv.x)/.98,sd=vuv.y*2.-1.,q=abs(sd);float r=h11(id+3.1),r2=h11(id*1.7+9.2);
  float w;                                                             // half width of the vane at u
  if(shape==0){w=mix(1.,sd>0.?.46:.60,smoothstep(.34,.56,u))*mix(.35,1.,smoothstep(0.,.12,u));w*=sqrt(max(0.,1.-pow(max(0.,(u-.80)/.20),2.)));}
  else if(shape==1){w=mix(.4,1.,smoothstep(0.,.15,u))*sqrt(max(0.,1.-pow(max(0.,(u-.78)/.22),2.2)));}
  else if(shape==2){w=mix(.75,1.,smoothstep(0.,.3,u))*sqrt(max(0.,1.-pow(max(0.,(u-.58)/.42),2.)));}
  else {w=mix(.9,1.,u)*sqrt(max(0.,1.-pow(max(0.,(u-.35)/.65),1.7)));}
  w+=.03*sin(u*60.+r*40.)*ragged*smoothstep(.3,.8,u);
  if(ragged>0.){float sl=.25+.5*r2;float at=abs(u-sl-.18*q*(1.+r));if(q>.25&&at<.012*ragged*step(.45,r)) discard;}
  if(q>w) discard;
  float L=asp;float e=w-q;                                             // distance to the edge in half widths
  float tip=smoothstep(tipAt,tipAt+.26,u+.06*sin(q*9.+r*9.));
  vec3 b=mix(cA,cC,tip)*(.86+.26*r);vec3 s=mix(cB,cC*.45,tip);
  float barb=sin(u*L*9.-q*7.+r*6.);b*=1.+.055*barb;
  if(bars>0.){float k=smoothstep(.15,.5,sin(u*26.+q*2.5+r*3.));b=mix(b,b*.55,k*bars*(1.-tip));}
  b=mix(b,b*.62,smoothstep(.55,.0,u)*.45);                             // shade where the next row lies over it
  float rim=smoothstep(.20,.13,e)*smoothstep(.02,.07,e);float cl=1.;
  b=mix(b,cE,rim*.85);s=mix(s,cE*.5,rim*.85);if(gild>0.&&rim>.5&&u>.35){cl=2.;b=vec3(1.1,.95,.7);}
  float rk=smoothstep(.075,.045,q)*smoothstep(1.,.82,u);b=mix(b,cE*.9,rk*.7);b=mix(b,b*.4,smoothstep(.03,.0,abs(q-.11))*.5*smoothstep(1.,.8,u));
  if(burnF>0.){float k=burnF*1.5-(1.-u)*.6-.3*vn(vuv*vec2(1.,4.)*3.+r*9.);if(k>.25) discard;if(k>.12){cl=4.;b=vec3(2.4,.8,.12);}else if(k>0.)b*=.3;}
  g0=vec4(n,vz);g1=vec4(b,cl+clamp(inkw,0.,.98)*.98);g2=vec4(s,1);g3=vec4(n,objId*64.+mod(id,61.)+1.);
}'''


SCALY = '''#include "noise.glsl"
in vec3 vp,vn_;in vec2 vuv;
layout(location=0) out vec4 g0;layout(location=1) out vec4 g1;layout(location=2) out vec4 g2;layout(location=3) out vec4 g3;
uniform vec3 ro;uniform mat3 CamR;uniform float far,objId,inkw;uniform vec2 rep;uniform vec3 cA,cB,cC,cE;
void main(){
  vec3 n=normalize(vn_),v=vp-ro;if(dot(n,v)>0.) n=-n;vec3 f=transpose(CamR)[2];float vz=dot(v,f);gl_FragDepth=clamp(vz/far,0.,1.);
  vec2 u=vuv.yx*rep.yx;float e=0.,vv=0.,id=0.;float row=floor(u.y);
  for(int k=1;k>=-1;k--){float r=row+float(k);vec2 q=vec2(u.x+.5*mod(r,2.),u.y-r);float c=floor(q.x);q.x=fract(q.x)-.5;float y=q.y-.35;float d=length(vec2(q.x*1.05,max(y,0.)*.78))-.52;if(d<0.&&q.y>-.2){e=d;vv=clamp((q.y+.1)/1.15,0.,1.);id=h21(vec2(c,r));break;}}
  float tip=smoothstep(.5,.95,vv),ed=smoothstep(-.10,-.02,e);vec3 b=mix(cA*.75,cA*1.1,tip)*(.86+.28*id),s=cB;b=mix(b,cE,smoothstep(-.22,-.16,e)*(1.-ed)*.7);b=mix(b,cC*.5,ed);
  g0=vec4(n,vz);g1=vec4(b,1.+clamp(inkw,0.,.98)*.98);g2=vec4(s,1);g3=vec4(n,objId*64.+1.);
}'''


def feathers(root, d, nor, L, W, bend=0., curl=.12, twist=0., id0=0, nl=8, nv=4):
    """n feathers: roots, directions, up normals (n,3); length, half width, bend (+ along the normal), twist per feather"""
    n = len(root); d = d / (np.linalg.norm(d, axis=1, keepdims=True) + 1e-9); nor = nor - d * (nor * d).sum(1, keepdims=True); nor = nor / (np.linalg.norm(nor, axis=1, keepdims=True) + 1e-9); sd = np.cross(nor, d)
    f = lambda x: np.broadcast_to(np.asarray(x, float), (n,))[:, None]
    L, W, bend, tw = f(L), f(W), f(bend), np.radians(f(twist)); sd, nor = sd * np.cos(tw) + nor * np.sin(tw), nor * np.cos(tw) - sd * np.sin(tw)
    u = np.linspace(0, 1, nl)[None, :, None]; v = np.linspace(-1, 1, nv)[None, None, :, None]; Lx, bx = L[:, :, None], bend[:, :, None]
    P = root[:, None] + d[:, None] * Lx * u * (1 - .25 * np.abs(bx) * u) + nor[:, None] * bx * Lx * u ** 2; T = d[:, None] + nor[:, None] * 2 * bx * u; N = nor[:, None] - d[:, None] * 2 * bx * u; N /= np.linalg.norm(N, axis=2, keepdims=True)
    Wx = W[:, :, None, None]; pos = P[:, :, None] + sd[:, None, None] * Wx * v - N[:, :, None] * curl * Wx * v ** 2; nr = N[:, :, None] + sd[:, None, None] * 2 * curl * v; nr = nr / np.linalg.norm(nr, axis=3, keepdims=True)
    uv = np.zeros((n, nl, nv, 2)); uv[..., 0] = (np.arange(n) + id0)[:, None, None] + u.reshape(1, nl, 1) * .98; uv[..., 1] = (v[..., 0] + 1) / 2
    i = (np.arange(nl - 1)[:, None] * nv + np.arange(nv - 1)[None]).reshape(-1); q = np.concatenate([np.stack([i, i + 1, i + nv], 1), np.stack([i + 1, i + nv + 1, i + nv], 1)]); idx = (q[None] + (np.arange(n) * nl * nv)[:, None, None]).reshape(-1, 3)
    return pos.reshape(-1, 3), nr.reshape(-1, 3), uv.reshape(-1, 2), idx


def join(parts):
    """several meshes -> one"""
    off = 0; P, N, U, I = [], [], [], []
    for p, n, u, i in parts: P.append(p); N.append(n); U.append(u); I.append(i + off); off += len(p)
    return np.vstack(P), np.vstack(N), np.vstack(U), np.vstack(I)


def xform(m, M):
    """mesh -> world by a 4x4 (uniform scale)"""
    p, n, u, i = m; R = M[:3, :3] / np.linalg.norm(M[:3, 0]); return p @ M[:3, :3].T + M[:3, 3], n @ R.T, u, i


# ------------------------------------------------------------------ pose
@dataclass
class Wing:
    """degrees; fold 0 spread .. 1 closed, spread = fan of the hand 0..1, bend of the primaries (+ up), hand/ulna raise the outer parts"""
    elev: float = 8.; sweep: float = 0.; twist: float = 0.; fold: float = 0.; ulna: float = 3.; hand: float = 4.; spread: float = 1.; bend: float = .14

    def mix(s, o, t): return Wing(**{f.name: (1 - t) * getattr(s, f.name) + t * getattr(o, f.name) for f in fields(s)})


@dataclass
class JPose:
    L: Wing = None; R: Wing = None
    neck: tuple = (14., 18., 0.)          # rise of the neck base, rise of its end, yaw
    head: tuple = (0., 14., 0.)           # yaw, pitch (down), roll
    reach: float = .85                    # neck length factor
    tail: tuple = (-4., .55, 0.)          # pitch (up), spread 0..1, roll
    legs: tuple = (0., 0.)                # 0 tucked back under the tail .. 1 thrown forward
    claw: tuple = (.25, .25)              # 0 closed .. 1 wide open
    jaw: float = 0.
    lost: int = 0                         # +1 left wing gone, -1 right wing gone
    heave: float = 0.

    def mix(s, o, t):
        d = {}
        for f in fields(s):
            a, b = getattr(s, f.name), getattr(o, f.name)
            d[f.name] = a.mix(b, t) if isinstance(a, Wing) else tuple((1 - t) * np.asarray(a, float) + t * np.asarray(b, float)) if isinstance(a, tuple) else (a if t < .5 else b) if f.name == 'lost' else (1 - t) * a + t * b
        return JPose(**d)

    def set(s, **k): return replace(s, **k)


def both(**k): return dict(L=Wing(**k), R=Wing(**k))


GLIDE = JPose(**both())
_FL = dict(elev=[(0, 52), (.08, 50), (.30, 8), (.50, -34), (.56, -36), (.75, 4), (.92, 46)], sweep=[(0, 2), (.25, 12), (.52, 10), (.75, -10), (.95, -4)], twist=[(0, 8), (.15, -10), (.45, -8), (.6, 14), (.85, 20)], fold=[(0, .12), (.12, 0), (.48, .02), (.62, .34), (.78, .50), (.92, .26)],
           ulna=[(0, 2), (.2, 10), (.5, 0), (.7, -22), (.9, -10)], hand=[(0, -22), (.12, -4), (.28, 22), (.50, 16), (.60, -12), (.76, -42), (.92, -36)], spread=[(0, .85), (.2, 1), (.5, 1), (.7, .45), (.9, .55)], bend=[(0, .0), (.16, .22), (.35, .34), (.52, .20), (.64, -.08), (.8, -.16), (.94, -.10)], heave=[(0, -.9), (.3, .1), (.55, 1.1), (.8, .2)])


def flap(ph, amp=1.):
    """one wing stroke per unit of phase: 0 wings high, .55 bottom of the down stroke, then the folded recovery"""
    k = {a: track(ph % 1., K, 1.) for a, K in _FL.items()}; h = k.pop('heave') * amp; k['elev'] = 6 + (k['elev'] - 6) * amp
    b = math.sin(2 * math.pi * ph)
    return JPose(**both(**k), neck=(16 - 5 * b, 18 - 4 * b, 0.), head=(0., 14 + 3 * b, 0.), tail=(-4 + 7 * b, .5 + .12 * b, 0.), heave=h)


def glide(t=0., bank=0.):
    """soaring, with the small restless motions of the hand; bank -1..1 tips one wing up"""
    a, b = math.sin(1.9 * t), math.sin(2.7 * t + 1)
    return JPose(L=Wing(elev=8 + 1.5 * a - 8 * bank, hand=4 + 3 * b, bend=.15 + .02 * b, twist=2 * a), R=Wing(elev=8 + 1.5 * a + 8 * bank, hand=4 + 3 * a, bend=.15 + .02 * a, twist=2 * b), tail=(-4, .55, 14 * bank), head=(20 * bank, 14 + 2 * a, 0.))


def dive(t=1.):
    """t 0 glide .. 1 the closed stoop, an arrowhead"""
    return GLIDE.mix(JPose(**both(elev=24, sweep=-16, twist=-4, fold=.82, ulna=-6, hand=-8, spread=.25, bend=-.04), neck=(2, 2, 0.), head=(0., 2., 0.), reach=1.05, tail=(0., .08, 0.), legs=(.05, .05), claw=(.1, .1)), min(1., t))


def brake(t=1.):
    """t 0 stoop .. 1 wings thrown forward and high, tail fanned, talons out"""
    return dive(1.).mix(JPose(**both(elev=40, sweep=26, twist=32, fold=.06, ulna=8, hand=14, spread=1.1, bend=.36), neck=(40, 6, 0.), head=(0., 22., 0.), reach=.9, tail=(-38, 1., 0.), legs=(1., 1.), claw=(1., 1.), jaw=.8), min(1., t))


def strike(t):
    """the blow: brake (0), talons close (.35), wings beat down and forward (.6), recover (1)"""
    a = brake(1.)
    b = JPose(**both(elev=-20, sweep=30, twist=6, fold=.04, ulna=-4, hand=6, spread=1., bend=.22), neck=(6, -16, 0.), head=(0., 30., 0.), reach=1.15, tail=(-50, .9, 0.), legs=(1.05, .85), claw=(.15, .15), jaw=.35)
    return a.mix(a.set(claw=(.2, .2), jaw=1.), track(t, [(0, 0.), (.35, 1.)])).mix(b, track(t, [(.25, 0.), (.65, 1.)])).mix(GLIDE, track(t, [(.75, 0.), (1., 1.)]))


def wing_lost(t, side=1):
    """falling, one wing gone (side +1 its left, -1 its right); the other beats wildly; t seconds"""
    s = math.sin(9 * t); w = Wing(elev=34 + 26 * s, sweep=6, twist=10 - 14 * s, fold=.18 + .18 * math.sin(9 * t + 1.6), ulna=6 * s, hand=-22 * math.sin(9 * t + .9), bend=.22 * math.sin(9 * t + .6)); st = Wing(elev=10 + 12 * s, fold=.55)
    return JPose(L=st if side > 0 else w, R=w if side > 0 else st, neck=(30 + 8 * s, 26, 24 * side), head=(30. * side, -6., 12 * s), tail=(-10 + 12 * s, .8, 20 * side), legs=(.45 + .2 * s, .35 - .2 * s), claw=(.7, .9), jaw=.9, lost=side)


def lying(t=0., lost=0):
    """on the ground (put the origin about 2.3 units above it), head sunk, the wings let go; a slow breath in t seconds"""
    b = math.sin(1.6 * t)
    return JPose(L=Wing(elev=-9 + .6 * b, sweep=-14, twist=-6, fold=.30, ulna=3, hand=3, spread=.8, bend=.03), R=Wing(elev=-9 + .6 * b, sweep=-20, twist=-6, fold=.42, ulna=3, hand=3, spread=.6, bend=.03), neck=(4 + b, -30 + b, 28.), head=(48., 24., 14.), reach=1., tail=(4., .35, 6.), legs=(.12, .25), claw=(.35, .5), lost=lost, heave=0.)


# ------------------------------------------------------------------ solve
H_, U_, C_ = 7.2, 9.2, 5.4                # bones of the wing
SH = V(2.05, .95, 1.6)


def _dir(a): a = np.radians(a); return np.stack([np.cos(a), np.zeros_like(a), np.sin(a)], -1)


def wing_geo(w, stub=False):
    """left wing: points and a frame field; returns dict of feather sets"""
    q = w.fold; a1, a2, a3 = -14 - 62 * q, 20 + 78 * q, -10 - 74 * q
    R1 = Rz(w.elev) @ Ry(-w.sweep) @ Rx(-w.twist); R2 = R1 @ Rz(w.ulna) @ Rx(-w.twist * .25); R3 = R2 @ Rz(w.hand)
    sh = SH; el = sh + R1 @ _dir(a1) * H_; wr = el + R2 @ _dir(a2) * U_; tp = wr + R3 @ _dir(a3) * C_
    JT = np.array([sh, el, wr, tp]); Rs = np.array([R1, R2, R3]); front = sh + R1 @ V(.5, .1, 2.2)

    def at(s):
        """bone point, frame (n,3,3) for s in 0..3"""
        s = np.atleast_1d(s); i = np.clip(s.astype(int), 0, 2); f = s - i; P = JT[i] * (1 - f)[:, None] + JT[i + 1] * f[:, None]
        x = s - .5; j = np.clip(np.floor(x).astype(int), 0, 1); k = np.clip(x - j, 0, 1); k = k * k * (3 - 2 * k); return P, Rs[j] * (1 - k)[:, None, None] + Rs[j + 1] * k[:, None, None]

    def ang(s):
        sp = w.spread; in_ = -86 - 4 * q; out = a3 - 6 - 60 * (1 - sp) * (1 - q) * .5
        k = np.clip((s - 2) / 1., 0, 1); t = np.interp(s, [0, 1, 2], [-112, -98, in_]); return np.where(s > 2, in_ + (out - in_) * k ** .9, t)

    def lead(s):                          # leading edge: skin stretched from the shoulder to the wrist, then the hand
        P, _ = at(s); s = np.atleast_1d(s); k = np.clip(s / 2, 0, 1)[:, None]; web = front * (1 - k) + (wr + R2 @ V(0, 0, .55)) * k + (R2 @ V(0, 0, 1.)) * (np.sin(k * np.pi) * (-.75))
        hand = P + (Rs[2] @ V(0, 0, .6))[None] * (1 - .6 * np.clip(s - 2, 0, 1))[:, None]; m = np.clip((s - 1.9) / .2, 0, 1)[:, None]; return web * (1 - m) + hand * m
    def Lr(s): return np.interp(s, [0, .5, 1, 1.5, 2, 2.35, 2.7, 3.], [6.4, 7.6, 8.6, 9.2, 10.2, 13.2, 14.4, 11.6])
    S = {}

    def row(name, s, k, fr, wd, h, side=1, twist=7., bend=0., curl=.12, nl=6, tilt=0., jit=0.):
        s = np.asarray(s, float); P, R = at(s); E = lead(s); n = np.einsum('nij,j->ni', R, V(0, 1, 0)); n /= np.linalg.norm(n, axis=1, keepdims=True); d = np.einsum('nij,nj->ni', R, _dir(ang(s)))
        root = P * (1 - k) + E * k + n * h * side
        d = d - n * tilt * side; j = np.sin(s * 91.7) * jit
        S[name] = feathers(root, d, n * side, Lr(s) * fr * (1 + j), wd, bend, curl, twist * side, nl=nl)
    if stub:
        row('cov0', np.linspace(.1, .75, 7), .2, .5, .9, .10, tilt=.05); row('cov1', np.linspace(.05, .7, 8), .55, .32, .8, .35); row('cov2', np.linspace(.0, .65, 9), .85, .22, .7, .5); row('und0', np.linspace(.1, .75, 7), .2, .5, .9, .1, -1)
        S['tube'] = CL.tube(np.array([sh - R1 @ V(1.2, 0, 0), sh + (el - sh) * .35, sh + (el - sh) * .72]), [1.2, .95, .45], 12); return S, JT
    sp = np.linspace(2.06, 3., 10); ks = (sp - 2) ** 1.
    row('prim', sp, 0., 1., np.linspace(1.25, .95, 10), 0., twist=-9., bend=w.bend * (.35 + .75 * ks), nl=12, curl=.10, jit=.03)
    ss = np.concatenate([np.linspace(.22, .92, 5), np.linspace(1.02, 1.99, 13)]); row('sec', ss, 0., 1., 1.12, -.03, twist=-7., bend=.02 + w.bend * .25, nl=8, jit=.05)
    for nm, side, hs in (('cov', 1, 1.), ('und', -1, .75)):
        row(nm + '0', np.concatenate([np.linspace(.18, 1.98, 22), np.linspace(2.06, 2.96, 9)]), .10, .50, .95, .16 * hs, side, 7., bend=-.05 + w.bend * .1, nl=6, tilt=.015, jit=.06)
        row(nm + '1', np.linspace(.10, 2.9, 32), .34, .34, .88, .34 * hs, side, 7., bend=-.09, nl=5, jit=.07)
        row(nm + '2', np.linspace(.05, 2.85, 36), .58, .23, .80, .50 * hs, side, 8., bend=-.12, nl=5, jit=.07)
        row(nm + '3', np.linspace(.0, 2.8, 40), .78, .17, .70, .56 * hs, side, 8., bend=-.2, nl=4, jit=.08)
    row('cov4', np.linspace(.0, 2.8, 44), .94, .135, .62, .52, 1, 8., bend=-.3, nl=4, jit=.08)
    s = np.array([0., .35, .8, 1.25, 1.7, 2.08, 2.4, 2.7, 3.]); E = CL.spline(np.vstack([[sh - R1 @ V(1.3, .1, -.6)], lead(s)]), 40); S['tube'] = CL.tube(E, np.interp(np.linspace(0, 1, 40), [0, .06, .18, .6, .75, 1], [1.0, .95, .66, .44, .36, .10]), 14)
    return S, JT


def solve(p):
    Rn = Ry(p.neck[2]); n0 = V(0, .35, 3.6); P = [n0]; seg = 1.22 * p.reach
    for i in range(5):
        a = math.radians(p.neck[0] + (p.neck[1] - p.neck[0]) * i / 4 + 26 * math.sin(i / 4 * math.pi) * (1.1 - p.reach)); yaw = Ry(p.neck[2] * (i + 1) / 5); P.append(P[-1] + yaw @ V(0, math.sin(a), math.cos(a)) * seg)
    Bh = (Ry(p.neck[2] * .7 + p.head[0]) @ Rx(p.head[1]) @ Rz(-p.head[2])); HD = P[-1] + Bh @ V(0, .28, .35); LG = np.zeros((40, 3))
    for k, sg in enumerate((1, -1)):
        e = p.legs[k]; c = p.claw[k]; hip = V(sg * 1.25, -1.35, -1.2 + .9 * e); th = math.radians(-150 + 112 * e); sh = math.radians(-166 + 124 * e); tr = math.radians(-172 + 150 * min(e, 1.05))
        d = lambda a: V(0, math.sin(a), math.cos(a)); lean = V(sg * .16, 0, 0)
        kn = hip + nz(d(th) + lean) * 2.3; an = kn + nz(d(sh) + lean * .5) * 2.4; ft = an + nz(d(tr)) * 2.2; LG[20 * k: 20 * k + 4] = hip, kn, an, ft
        f = nz(d(tr)); up = nz(np.cross(f, V(1, 0, 0))); sd = V(1, 0, 0)          # foot frame: f along the tarsus, toes fan round it
        for t, (ang, ln) in enumerate(((0, 1.15), (46, 1.), (-46, 1.), (180, .9))):
            a = math.radians(ang); o = nz(up * -math.cos(a) * -1 + sd * math.sin(a)); op = math.radians(20 + 70 * c); b = 20 * k + 4 + 4 * t; q = ft.copy(); LG[b] = q; aa = op
            for j, (l, cv) in enumerate(((.95, 0.), (.85, 30 + 22 * (1 - c)), (.95, 46))):
                aa -= math.radians(cv); q = q + nz(f * math.cos(aa) + o * math.sin(aa)) * l * ln; LG[b + 1 + j] = q
    return dict(Bh=Bh.T, NK=np.array(P), HD=HD, LG=LG)


# ------------------------------------------------------------------ eye and palette
def _eye(F):
    P = Pen(1024, (-1.5, -1.5, 1.5, 1.5)); c = P.c; k = F.lid; up = -.12 + .42 * k
    eye = [(.80, -.20), (.60, .06, .34, up - .04, .0, up), (-.34, up, -.62, .22 * k, -.82, .08), (-.62, -.22, -.36, -.36, .0, -.36), (.34, -.36, .62, -.32, .80, -.20)]
    for w, a, h in ((.62, .28, '#5a1a2a'), (.42, .45, '#4a1424'), (.24, .9, '#2a0a16')): P.path(eye, True); P.col(h, a); c.set_line_width(w); c.stroke()
    for i in range(5):                                                   # the wrinkles of age
        a = 2.75 + i * .22; r0, r1 = .98, 1.36 - .05 * i; P.line([(r0 * math.cos(a), r0 * math.sin(a) * .62 + .05), (1.15 * math.cos(a + .06), 1.15 * math.sin(a + .06) * .62 + .02, r1 * math.cos(a + .12), r1 * math.sin(a + .12) * .66, (r1 + .05) * math.cos(a + .2), (r1 + .05) * math.sin(a + .2) * .68)], .035, '#3a1220', .85)
    for i in range(3): y = -.52 - .17 * i; P.line([(.55 - .1 * i, y + .06), (.2, y - .08, -.3, y - .08, -.75 + .1 * i, y + .12)], .032, '#3a1220', .8 - .15 * i)
    if k > .06:
        P.fill(eye, '#f6dfae'); c.save(); P.path(eye, True); c.clip(); ix, iy = .04 + F.gx * .18, -.01 + F.gy * .1
        g = cairo.RadialGradient(ix, iy, .05, ix, iy, .40); g.add_color_stop_rgba(0, *rgb('#ffd24a'), 1); g.add_color_stop_rgba(.55, *rgb('#f08a1c'), 1); g.add_color_stop_rgba(.85, *rgb('#b03014'), 1); g.add_color_stop_rgba(1, *rgb('#3a0c0c'), 1); c.set_source(g); c.arc(ix, iy, .40, 0, 7); c.fill()
        for i in range(30): a = i / 30 * 6.283; P.line([(ix + .19 * math.cos(a), iy + .19 * math.sin(a)), (ix + .34 * math.cos(a), iy + .34 * math.sin(a))], .012, '#7a2408', .5)
        P.col('#0a0406'); c.arc(ix, iy, .165 * F.pupil, 0, 7); c.fill()
        g = cairo.LinearGradient(0, up, 0, up - .30); g.add_color_stop_rgba(0, .05, 0, .03, .8); g.add_color_stop_rgba(1, .05, 0, .03, 0); c.set_source(g); c.rectangle(-1, -1, 2, 2); c.fill()
        P.col('#ffffff'); c.arc(ix + .12, iy + .14, .075, 0, 7); c.fill(); P.col('#ffe8b0', .9); c.arc(ix - .12, iy - .14, .035, 0, 7); c.fill()
        if F.spark > 0: P.fill([(ix - .05, iy - .14), (ix - .12, iy, ix - .02, iy + .06, ix, iy + .2), (ix + .06, iy + .06, ix + .12, iy, ix + .05, iy - .14)], '#fff0b0', F.spark)
        c.restore()
    P.path(eye, True); P.col('#14060e'); c.set_line_width(.06); c.stroke()
    f = F.frown
    P.fill([(.98, -.34), (.66, .04, .4, up + .02, .02, up + .04), (-.38, up + .04, -.72, .28, -1.1, .16), (-.8, .5, -.3, up + .34, .1, up + .28), (.5, up + .20 - .1 * f, .8, .2 - .2 * f, .98, -.34)], '#1c0812')         # the heavy lid
    P.line([(.95, -.2), (1.05, -.5, 1.0, -.7, .9, -.9)], .05, '#2a0a16', .8)
    return P.out()


PAL = {1: ('#d89a86', '#7a3c48', 1), 2: ('#fbf6ea', '#a8a0b8', 1), 3: ('#ffffff', '#805030', 2), 4: ('#8a5230', '#3c2028', 1), 5: ('#e0a83c', '#8a4a1c', 1), 6: ('#f6f0e0', '#a8a0b8', 8), 7: ('#2a2028', '#0c0810', 7), 8: ('#c4142c', '#54081c', 3), 9: ('#0f8a66', '#063a34', 3), 10: ('#b02a30', '#5a0c18', 1), 11: ('#e0b060', '#8a5020', 8), 12: ('#d8a050', '#7a4018', 8), 13: ('#d9a866', '#7a4a3a', 1)}
BODY = Fig('jatayu', 'jatayu.glsl', PAL, face=_eye, human=False, step=.85, bound=(0, 0, 2, 12), u=dict(brow=0., jaw=0., dust=0.))
# feather layers: shape, base, shadow, tip, edge, tipAt, gild, bars, ink
KINGLY = dict(prim=(0, '#4a3036', '#1e1420', '#120c18', '#c89a5a', .30, 0., 0., .95), sec=(1, '#744630', '#341a22', '#1c1018', '#e0b070', .62, 0., .55, .9), cov0=(1, '#96592e', '#46222a', '#4a2620', '#f2cf8c', .66, 0., 0., .85), cov1=(2, '#b4702e', '#5c2c24', '#7a421e', '#f8dc9c', .70, 1., 0., .8), cov2=(2, '#c88436', '#6c3822', '#96591f', '#ffe6ac', .74, 1., 0., .75), cov3=(2, '#d89a44', '#7c4424', '#a86a26', '#ffecbc', .76, 1., 0., .7), cov4=(2, '#e4b060', '#8a5230', '#b87c34', '#fff2cc', .78, 1., 0., .65),
              und0=(1, '#c8a078', '#6a4648', '#6a4034', '#f2dcb4', .62, 0., .3, .8), und1=(2, '#dcb88c', '#7c5450', '#a87c54', '#fbeccb', .7, 0., 0., .7), und2=(2, '#e8caa0', '#8a6058', '#bc9064', '#fff4da', .74, 0., 0., .65), und3=(2, '#f0d8b4', '#987064', '#cca67a', '#fff8e6', .76, 0., 0., .6),
              tail=(1, '#553424', '#24141c', '#160e16', '#d8a866', .52, 0., .5, .9), tcov=(2, '#a8662e', '#50281f', '#6a381c', '#f6d898', .7, 1., 0., .8), ruff=(3, '#fffaf0', '#a89cb4', '#f4e4cc', '#ffffff', .8, 0., 0., .7))


def _mesh(st, name, m, pal, burn):
    sh, a, b, t, e, ta, gild, bars, ink = pal[name]
    st.mesh(*m, col=(a, b, t), ink=ink, frag=FEATHER, u=dict(shape=sh, cE=hexc(e), tipAt=ta, gild=gild, bars=bars, ragged=1., asp=8. if sh < 2 else 3., burnF=float(burn)))


class JS:
    """placed Jatayu: w(point), p(name)"""

    def __init__(s, M, q, jl, jr): s.M, s.q, s.jl, s.jr = M, q, jl, jr; s.Sc = float(np.linalg.norm(M[:3, 0]))

    def w(s, p): return s.M[:3, :3] @ np.asarray(p, float) + s.M[:3, 3]

    def d(s, v): return nz(s.M[:3, :3] @ np.asarray(v, float))

    def head(s, p=(0, 0, 0)): return s.w(s.q['HD'] + np.asarray(p, float) @ s.q['Bh'])

    def p(s, n):
        mir = V(-1, 1, 1); q = s.q
        return {'head': lambda: s.head(), 'beak': lambda: s.head((0, -1., 2.8)), 'eyeL': lambda: s.head((.95, .22, .75)), 'eyeR': lambda: s.head((-.95, .22, .75)), 'back': lambda: s.w((0, 2., 0)), 'breast': lambda: s.w((0, -2., 2.5)), 'torque': lambda: s.w(q['NK'][0] + V(0, -1.4, .8)), 'talonL': lambda: s.w(q['LG'][3]), 'talonR': lambda: s.w(q['LG'][23]),
                'shoulderL': lambda: s.w(s.jl[0]), 'wristL': lambda: s.w(s.jl[2]), 'tipL': lambda: s.w(s.jl[3] + (s.jl[3] - s.jl[2]) / C_ * 11), 'shoulderR': lambda: s.w(s.jr[0] * mir), 'wristR': lambda: s.w(s.jr[2] * mir), 'tipR': lambda: s.w((s.jr[3] + (s.jr[3] - s.jr[2]) / C_ * 11) * mir), 'tail': lambda: s.w((0, 0, -14))}[n]()


def _mirror(m): p, n, u, i = m; s = np.array([-1, 1, 1]); return p * s, n * s, u, i[:, ::-1]


def draw(st, pose=None, at=(0, 0, 0), yaw=0., pitch=0., roll=0., scale=1., M=None, face=None, pal=None, parts=('body', 'wingL', 'wingR', 'tail'), burn=0., dust=0., shadow=True, draw=True):
    """draw him; parts=('wingL',) draws a severed left wing alone; burn 0..1 singes the feathers; dust greys him"""
    p = pose or GLIDE; M = model(at, yaw, pitch, roll, scale) if M is None else np.asarray(M, float); Sc = np.linalg.norm(M[:3, 0])
    if p.heave: M = M.copy(); M[:3, 3] += M[:3, 1] * p.heave
    q = solve(p); pal = pal or KINGLY; gl_, jl = wing_geo(p.L, p.lost > 0); gr_, jr = wing_geo(p.R, p.lost < 0); S = JS(M, q, jl, jr)
    if not draw: return S
    if 'body' in parts:
        pts = np.vstack([q['HD'][None], q['LG'][[0, 1, 2, 3, 23]], [[0, 0, 5], [0, 0, -5]]]); c = (pts.max(0) + pts.min(0)) / 2; R = np.linalg.norm(pts - c, axis=1).max() + 3.6
        st.fig(BODY, M=M, face=face or Face(frown=.3), u=dict(Bh=q['Bh'], NK=q['NK'], HD=q['HD'], LG=q['LG'], jaw=float(p.jaw), dust=float(dust), bound=np.append(c, R)), shadow=shadow)
        ax = nz(q['NK'][1] - q['NK'][0]); c0 = q['NK'][0] + ax * .35; xx = nz(np.cross(V(0, 1, 0), ax)); yy = np.cross(ax, xx); R_ = []
        for k, (n, r, L, up) in enumerate(((26, 1.35, 2.3, .55), (30, 1.40, 1.8, .85), (30, 1.30, 1.3, 1.3))):
            a = np.linspace(0, 2 * np.pi, n, endpoint=False) + k * .1; rad = np.cos(a)[:, None] * xx + np.sin(a)[:, None] * yy; d = rad * up - ax * 1.; R_.append(feathers(c0 + rad * r + ax * .24 * k, d, rad + ax * .5, L * (1 + .12 * np.sin(a * 7)), .42, -.12, .2, 6., id0=k * 37, nl=5))
        _mesh(st, 'ruff', xform(join(R_), M), pal, burn)
        sc = []
        for k in range(4):
            n = 13; u = np.linspace(0, 1, n)
            for sg in (1, -1): sc.append(feathers(np.stack([sg * (.35 + .55 * k + .25 * np.sin(u * 3)), 2.18 - .16 * k ** 1.5 - .75 * u ** 1.6, 3.0 - .3 * k - 6.6 * u], 1), np.stack([sg * (.10 + .10 * k) * (1 - u * .6), -.02 - .05 * u, -np.ones(n)], 1), np.stack([sg * .22 * k * np.ones(n), np.ones(n), np.full(n, .25)], 1), 2.1 + .5 * u, .62, -.06, .16, 5., id0=14 * (2 * k + (sg > 0)), nl=5))
        _mesh(st, 'cov1', xform(join(sc), M), pal, burn)
    if 'tail' in parts:
        Rt = Rz(p.tail[2]) @ Rx(-p.tail[0]); n = 12; s = np.linspace(-1, 1, n); sp = 8 + 44 * p.tail[1]; a = np.radians(s * sp); d = np.stack([np.sin(a), -.02 - .05 * np.abs(s), -np.cos(a)], 1); r = np.stack([s * .95, .05 - .12 * np.abs(s) - .03 * (np.arange(n) % 2), np.full(n, -5.6)], 1); up = np.stack([s * .25, np.ones(n), np.zeros(n)], 1); T = V(0, .2, -5.)
        fx = lambda v: (v - T) @ Rt.T + T
        m1 = feathers(fx(r), d @ Rt.T, up @ Rt.T, 9.2 - 1.8 * np.abs(s) ** 2, .92, -.04, .1, -6 * s, nl=8)
        n2 = 16; s2 = np.linspace(-1, 1, n2); a2 = np.radians(s2 * sp * .9); d2 = np.stack([np.sin(a2), -.06 + 0 * s2, -np.cos(a2)], 1); rows = []
        for k in range(3):
            for sg in (1, -1): rows.append(feathers(fx(np.stack([s2 * (1.1 + .12 * k), sg * (.32 + .24 * k) - .1 * np.abs(s2) * sg, np.full(n2, -5.4 + 1.0 * k)], 1)), d2 @ Rt.T, (np.stack([s2 * .4, np.full(n2, sg * 1.), 0 * s2], 1)) @ Rt.T, (3.6 - .5 * k), .72, -.06, .14, 6 * sg, id0=20 * (2 * k + (sg > 0)), nl=5))
        _mesh(st, 'tail', xform(m1, M), pal, burn); _mesh(st, 'tcov', xform(join(rows), M), pal, burn)
    W_ = []
    if 'wingL' in parts: W_.append(gl_)
    if 'wingR' in parts: W_.append({k: _mirror(m) for k, m in gr_.items()})
    for nm in ('prim', 'sec', 'cov0', 'cov1', 'cov2', 'cov3', 'cov4', 'und0', 'und1', 'und2', 'und3'):
        ms = [g[nm] for g in W_ if nm in g]
        if ms: _mesh(st, nm, xform(join(ms), M), pal, burn)
    for g in W_: a = pal['cov4']; st.mesh(*xform(g['tube'], M), col=(a[1], a[2], a[3]), ink=.8, frag=SCALY, u=dict(cE=hexc(a[4]), rep=(44., 9.)))
    return S


def shed(st, S, t, n=60, seed=3, where='shoulderL', speed=14., life=3.2, size=.9, fall=5., col='#b4702e', col2='#3a2430', spread=3.):
    """feathers that scatter from a named point at t = 0 (seconds), after close()"""
    from lau import fx as FX
    if t < 0: return
    r = np.random.default_rng(seed); d = r.normal(size=(n, 3)); d /= np.linalg.norm(d, axis=1, keepdims=True); k = r.uniform(.3, 1., (n, 1)); at = S.p(where) if isinstance(where, str) else np.asarray(where, float)
    g = (1 - math.exp(-2.1 * t)) / 2.1; P = at + r.normal(size=(n, 3)) * spread * S.Sc + d * speed * k * g * S.Sc + V(0, -1, 0) * fall * k * max(t - .15, 0) * S.Sc; ph = r.uniform(0, 6.28, n); P[:, 0] += 1.6 * S.Sc * np.sin(2.6 * t + ph) * min(t, 1.); P[:, 2] += 1.1 * S.Sc * np.cos(2.1 * t + ph * 2) * min(t, 1.)
    a, b = np.array(hexc(col)), np.array(hexc(col2)); c = a * k + b * (1 - k); FX.particles(st, P, size * S.Sc * r.uniform(.5, 1.5, n), c, 'feather', rot=ph + 1.2 * np.sin(2.6 * t + ph) + t * r.uniform(-1.5, 1.5, n), seed=r.uniform(0, 1, n), alpha=np.clip((life - t) / .8, 0, 1) * np.ones(n))
