"""Surasa, mother of serpents.  Drawn at scale 10 her open jaws are about 120 units across.

    from chars import serpent as SP
    S = SP.draw(st, gape=1., at=(0, 60, 0), yaw=0, pitch=-10, scale=10, neck=[(x, y, z), ...])
    S.w((x, y, z))        head units (see below) -> world;  S.p('throat'), S.p('tongue'), S.p('eyeL'), S.p('fangL'), S.p('centre')
Head units: the mouth opens toward +z; hinge at (0, 0, -4.5); rim of teeth about 5 wide and 6.5 forward; throat tunnel from z = -7 back.
A camera at S.w((0, -.3, -6)) looking to S.w((0, 0, 8)) sees the sea between the teeth."""
import numpy as np, math, cairo
from lau.stage import Fig, model, hexc
from lau.rig import V, nz, Rx, Ry, Rz
from lau.face import Face, Pen, rgb
from lau import cloth as CL
from chars.jatayu import xform, join


def _eye(F):
    P = Pen(1024, (-1.1, -1.1, 1.1, 1.1)); c = P.c
    g = cairo.RadialGradient(0, .1, .05, 0, 0, 1.); g.add_color_stop_rgba(0, *rgb('#fff0a0'), 1); g.add_color_stop_rgba(.35, *rgb('#f6b02c'), 1); g.add_color_stop_rgba(.7, *rgb('#c8501a'), 1); g.add_color_stop_rgba(1, *rgb('#4a0c14'), 1); c.set_source(g); c.rectangle(-2, -2, 4, 4); c.fill()
    for i in range(60): a = i / 60 * 6.283; P.line([(.22 * math.cos(a), .35 * math.sin(a)), (.80 * math.cos(a + .05), .80 * math.sin(a + .05))], .014, '#8a2c08' if i % 2 else '#ffe08a', .5)
    w = .17 * F.pupil; x = F.gx * .25; P.fill([(x, .86), (x + w * 1.3, .3, x + w * 1.3, -.3, x, -.86), (x - w * 1.3, -.3, x - w * 1.3, .3, x, .86)], '#0a0206')
    P.col('#ffffff'); c.arc(x + .26, .34, .12, 0, 7); c.fill(); P.col('#fff0c0', .8); c.arc(x - .24, -.36, .06, 0, 7); c.fill()
    y = -1.1 + 2.2 * max(0., 1 - F.lid * .80)
    P.fill([(-1.2, 1.2), (-1.2, .62 - y * .1), (-.5, 1.0 - 2.2 * (1 - F.lid) - .16, .4, .95 - 2.2 * (1 - F.lid) - .3 * F.frown - .2, 1.2, .30 - 1.6 * (1 - F.lid) - .3 * F.frown), (1.2, 1.2)], '#12324a'); P.line([(-1.2, .62 - y * .1), (-.5, 1.0 - 2.2 * (1 - F.lid) - .16, .4, .95 - 2.2 * (1 - F.lid) - .3 * F.frown - .2, 1.2, .30 - 1.6 * (1 - F.lid) - .3 * F.frown)], .10, '#12060e')
    c.arc(0, 0, 1.0, 0, 7); P.col('#12060e'); c.set_line_width(.14); c.stroke()
    return P.out()


PAL = {1: ('#1f7a78', '#0c2a4a', 8), 2: ('#d85a5e', '#5a0c24', 8), 3: ('#ffffff', '#805030', 2), 4: ('#8a2038', '#2a0614', 1), 5: ('#fff4dc', '#9a8ab0', 8), 6: ('#d8344a', '#4a0820', 8), 7: ('#f6b02c', '#8a3a14', 6), 8: ('#f6f2e4', '#a8a0c0', 8), 9: ('#f2e2b8', '#8a6a4a', 8), 10: ('#ff3048', '#7a0a1c', 3), 11: ('#12a074', '#063a34', 3), 12: ('#f0d89a', '#9a6a4a', 8), 13: ('#d85a5e', '#5a0c24', 8)}
HEAD = Fig('surasa', 'serpent.glsl', PAL, face=_eye, human=False, step=.8, bound=(0, 0, -2., 15.), u=dict(gape=0., wet=.6, tongueIn=0.))

SCALE = '''#include "noise.glsl"
in vec3 vp,vn_;in vec2 vuv;
layout(location=0) out vec4 g0;layout(location=1) out vec4 g1;layout(location=2) out vec4 g2;layout(location=3) out vec4 g3;
uniform vec3 ro;uniform mat3 CamR;uniform float far,objId,inkw,fT,seaY,wet;uniform vec2 rep;uniform vec3 cA,cB,cC,cE,cF;uniform int mode;
// mode 0 neck (v = angle, .25 belly .75 spine), 1 hood (u across -1..1 packed 0..1, v up)
void main(){
  vec3 n=normalize(vn_),v=vp-ro;bool back=dot(n,v)>0.;if(back) n=-n;vec3 f=transpose(CamR)[2];float vz=dot(v,f);gl_FragDepth=clamp(vz/far,0.,1.);
  float part=1.;vec3 b,s;float cl=8.,ik=inkw;
  vec2 u=vuv.yx*rep.yx;float e=0.,vv=0.,id=0.;float row=floor(u.y);
  for(int k=1;k>=-1;k--){float r=row+float(k);vec2 q=vec2(u.x+.5*mod(r,2.),u.y-r);float c=floor(q.x);q.x=fract(q.x)-.5;float y=q.y-.35;float d=length(vec2(q.x*1.05,max(y,0.)*.78))-.52;if(d<0.&&q.y>-.2){e=d;vv=clamp((q.y+.1)/1.15,0.,1.);id=h21(vec2(c,r));break;}}
  float tip=smoothstep(.5,.95,vv),ed=smoothstep(-.11,-.03,e);
  if(mode==0){float bel=abs(vuv.y-.25);bel=min(bel,1.-bel);float sp=abs(vuv.y-.75);sp=min(sp,1.-sp);
    vec3 a=mix(cA,cC,smoothstep(.22,.05,sp));b=mix(a*.72,a*1.16,tip)*(.86+.28*id);s=cB*(.75+.4*tip);b=mix(b,cE,smoothstep(-.24,-.17,e)*(1.-ed)*.5);b=mix(b,b*.35,ed);s=mix(s,s*.4,ed);
    float band=step(.5,fract(vuv.x*rep.x/14.))*0.;
    float dia=abs(fract(vuv.x*rep.x/12.)-.5)*2.;float dm=smoothstep(.02,-.02,sp-.16*dia);if(dm>.5&&ed<.5){b=mix(b,cC*.9,.6);}
    if(bel<.105){float y=fract(vuv.x*rep.x*.62+.8*pow(bel/.105,2.)*.4);float ln=smoothstep(.10,.02,abs(y-.5)-.40);b=cF*(.78+.30*y);s=cF*vec3(.42,.36,.52);b=mix(cF*.35,b,ln);part=2.;}
    else if(bel<.125){b=cE;s=cE*.4;cl=2.;b=vec3(1.1,.95,.7);part=3.;}
  }else{
    vec2 h=vec2(vuv.x*2.-1.,vuv.y);float k=abs(h.x);vec3 a=mix(cA,cC,smoothstep(.25,1.,k));b=mix(a*.72,a*1.16,tip)*(.86+.28*id);s=cB*(.75+.4*tip);b=mix(b,cE,smoothstep(-.24,-.17,e)*(1.-ed)*.5);b=mix(b,b*.35,ed);s=mix(s,s*.4,ed);
    if(!back){                                                   // the inner face: ribs, eye spots, gold hem
      float rib=abs(fract(h.x*4.5*(1.4-.4*h.y)+.5)-.5);b=mix(b,b*.55,smoothstep(.10,.03,rib));
      vec2 q=vec2(k-.52,(h.y-.60)*1.25);float d=length(q);float c0=smoothstep(.02,-.02,d-.30);b=mix(b,cE,c0);b=mix(b,hex(0x0c2c5e),smoothstep(.02,-.02,d-.25));b=mix(b,hex(0x1aa08a),smoothstep(.02,-.02,length(q-vec2(0,-.02))-.18));b=mix(b,hex(0xf6d060),smoothstep(.02,-.02,length(q-vec2(0,-.03))-.11));b=mix(b,hex(0xb0122a),smoothstep(.015,-.015,length(q-vec2(0,-.03))-.07));
      if(abs(d-.275)<.018){cl=2.;b=vec3(1.1,.95,.7);}
      if(k<.13){float y=fract(h.y*20.);b=cF*(.8+.3*y);b=mix(cF*.35,b,smoothstep(.02,.12,y));s=cF*.4;}
    }}
  float wetk=smoothstep(.62,.72,fbm(vec2(vuv.y*26.,vuv.x*rep.x*.18+fT*1.2)));b=mix(b,hex(0xeaf6f0),wetk*wet*.5);
  g0=vec4(n,vz);g1=vec4(b,cl+clamp(ik,0.,.98)*.98);g2=vec4(s,1);g3=vec4(n,objId*64.+part);
}'''


def tube_ref(P, r, side=(1, 0, 0), m=40, n=60):
    """tube whose angle coordinate starts at `side` (kept constant along the curve): v=.25 lies toward cross(tangent, side)"""
    P = CL.spline(np.asarray(P, float), n); r = np.interp(np.linspace(0, 1, n), np.linspace(0, 1, np.size(r)), np.atleast_1d(r)); T = np.gradient(P, axis=0); T /= np.linalg.norm(T, axis=1, keepdims=True); s = np.asarray(side, float); s = s / np.linalg.norm(s)
    X = s - T * (T @ s)[:, None]; X /= np.linalg.norm(X, axis=1, keepdims=True); Y = np.cross(T, X); a = np.linspace(0, 2 * np.pi, m); ring = np.cos(a)[None, :, None] * X[:, None] + np.sin(a)[None, :, None] * Y[:, None]; pos = P[:, None] + ring * r[:, None, None]
    L = np.r_[0, np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))]; uv = np.stack(np.broadcast_arrays((L / L[-1])[:, None], (a / (2 * np.pi))[None]), -1); i = (np.arange(n - 1)[:, None] * m + np.arange(m - 1)[None]).reshape(-1)
    return (pos.reshape(-1, 3), ring.reshape(-1, 3), uv.reshape(-1, 2), np.concatenate([np.stack([i, i + m, i + 1], 1), np.stack([i + 1, i + m, i + m + 1], 1)])), L[-1]


def _tongue(t, gape, wave=1.):
    P = [];
    for i in range(8):
        u = i / 7; P.append(V(.5 * wave * math.sin(2.2 * t - 3 * u) * u, -1.4 - 1.0 * gape * u * (1 - u) * 2. - (.6 + 2.6 * gape) * u + .5 * wave * math.sin(3.1 * t - 4.5 * u) * u * gape, -7.2 + (9.2 + 3.2 * gape) * u))
    d = nz(P[7] - P[6]); T = P[:]
    for s in (1, -1): T += [P[7] + d * 1.1 + V(s * .45, .05, 0), P[7] + d * 2.0 + V(s * 1.15, .45 + .3 * math.sin(6 * t + s), 0), P[7] + d * 2.6 + V(s * 1.6, .9, 0)]
    return np.array(T)


NAMES = dict(centre=(0, 0, 0), throat=(0, -.3, -8.), tongue=(0, -2, 5), jewel=(0, 3.9, 2.2))


class SS:
    def __init__(s, M, gape): s.M, s.gape = M, gape; s.Sc = float(np.linalg.norm(M[:3, 0]))

    def w(s, p): return s.M[:3, :3] @ np.asarray(p, float) + s.M[:3, 3]

    def up(s, p):
        """a point of the upper jaw (closed position) -> world, with the gape"""
        a = s.gape * .66; q = np.asarray(p, float) - V(0, 0, -4.5); return s.w(Rx(-math.degrees(a)) @ q + V(0, 0, -4.5))

    def low(s, p):
        a = s.gape * .70; q = np.asarray(p, float) - V(0, 0, -4.5); return s.w(Rx(math.degrees(a)) @ q + V(0, 0, -4.5))

    def p(s, n):
        if n in NAMES: return s.up(NAMES[n]) if n == 'jewel' else s.w(NAMES[n])
        sg = 1 if n[-1] == 'L' else -1
        return s.up(dict(eye=(sg * 4.6, 2.6, 2.), fang=(sg * 2.1, -2., 6.4), horn=(sg * 5.2, 7.9, -6.6))[n[:-1]])


def draw(st, gape=1., at=(0, 0, 0), yaw=0., pitch=0., roll=0., scale=10., M=None, t=None, face=None, neck=None, hood=1., wet=.6, neck_r=(5.2, 4.6, 4.2, 4.6, 5.4), barbels=True, u=None):
    """head + hood + neck.  neck: list of world points from the head's back down into the water (default: a thick S going down behind); hood 0..1 spreads the cobra hood"""
    M = model(at, yaw, pitch, roll, scale) if M is None else np.asarray(M, float); t = st.t if t is None else t; S = SS(M, gape); Sc = S.Sc
    st.fig(HEAD, M=M, face=face or Face(frown=.5), u=dict(gape=float(gape), wet=float(wet), TG=_tongue(t, gape), bound=np.array([0, .3, -2.2, 14.8]), **(u or {})))
    col = ('#1f7a78', '#0c2a4a', '#12405e'); cu = dict(cE=hexc('#e8d27a'), cF=hexc('#f0d89a'), wet=float(wet), seaY=-1e4)
    if neck is None: P = np.array([(0, .6, -5.5), (0, .2, -9.5), (0, -5, -14.), (0, -13, -14.5), (0, -22, -11.), (0, -34, -10.)]) @ M[:3, :3].T + M[:3, 3]
    else: P = np.vstack([S.w((0, .6, -5.5)), S.w((0, .2, -9.5)), np.asarray(neck, float)])
    m, L = tube_ref(P, np.asarray(neck_r) * Sc, side=M[:3, 0] / Sc); st.mesh(*m, col=col, ink=.95, frag=SCALE, u=dict(mode=0, rep=(L / Sc / 1.15, 26.), **cu))
    # dorsal fins: a row of gold-edged leaves along the neck
    from chars.jatayu import feathers, FEATHER
    Q = CL.spline(P, 60)[8:]; T = np.gradient(Q, axis=0); T /= np.linalg.norm(T, axis=1, keepdims=True); X = M[:3, 0] / Sc; N = -np.cross(T, X); N /= np.linalg.norm(N, axis=1, keepdims=True); r = np.interp(np.linspace(0, 1, 52), np.linspace(0, 1, 5), neck_r) * Sc
    k = np.linspace(0, 51, 30).astype(int); fin = feathers(Q[k] + N[k] * (r[k] * .9)[:, None], N[k] + T[k] * .75, np.tile(X, (30, 1)), 3.4 * Sc * (1 + .15 * np.sin(np.arange(30) * 1.9)), 1.0 * Sc, .04 * math.sin(t), .0, nl=7)
    fu = dict(shape=2, cE=hexc('#f6d070'), tipAt=.3, gild=1., bars=0., ragged=0., asp=3., burnF=0.); st.mesh(*fin, col=('#d8563a', '#6a1224', '#f0a050'), ink=.9, frag=FEATHER, u=fu)
    if hood > 0:
        W_ = 14.5 * hood
        def sh(a, b):                                                  # a across 0..1, b up 0..1 (head units)
            x = a * 2 - 1; pr = math.sin(min(1., b * .86 + .14) * math.pi) ** .75; lobe = 1 + .05 * abs(math.sin(x * 2.5 * math.pi)) * b
            y = -13 + 29.5 * b * lobe - 6.0 * x * x * b; return (x * W_ * (pr * .96 + .04) * lobe, y, -10.5 + 4.2 * b * b - 1.0 * (1 - abs(x)) + 3.4 * x * x * (.4 + b * .6))
        m = CL.sheet(sh, 49, 30); st.mesh(*xform(m, M), col=('#1a6a74', '#0a2444', '#0f3c5c'), ink=.95, frag=SCALE, u=dict(mode=1, rep=(40., 32.), **cu))
        rim = np.array([sh(a, 1.) for a in np.linspace(0, 1, 70)]); side = [np.array([sh(a, b) for b in np.linspace(.25, 1, 24)]) for a in (0., 1.)]
        g = [CL.tube(rim, .26, 8)] + [CL.tube(q, .26, 8) for q in side]; st.mesh(*xform(join(g), M), col=('#ffffff', '#805030', '#ffffff'), cls=2, ink=.8)
        from lau.props import STONE  # noqa  (jewels on the lobes are drawn as meshes)
        j = []
        for a in np.linspace(.1, .9, 5):
            c = np.array(sh(a, 1.)); th = np.linspace(0, np.pi, 9); pr = np.stack([np.zeros(9), -np.cos(th) * 1.1, np.zeros(9)], 1) + c + V(0, .9, .2); j.append(CL.tube(pr, np.maximum(np.sin(th), .02) * .62, 12))
        st.mesh(*xform(join(j), M), col=('#ff3048', '#7a0a1c', '#ffffff'), cls=3, ink=.8)
    if barbels:
        b = []
        for sg in (1, -1):
            for i, (x, z, ln) in enumerate(((4.2, 4.6, 9.), (5.6, 1.4, 11.), (6.2, -2., 8.))):
                a = math.radians(38 * gape + 6); r0 = V(sg * x, -1.1, z); r0 = Rx(math.degrees(gape * .70)) @ (r0 - V(0, 0, -4.5)) + V(0, 0, -4.5)
                q = [r0 + V(sg * (u * 2.2 + .7 * math.sin(2 * t + i * 2 - u * 4) * u), -ln * (u * .25 + .5 * u * u) + 1.2 * math.sin(1.6 * t + i - 3 * u) * u, -ln * u * u * .45) for u in np.linspace(0, 1, 9)]; b.append(CL.tube(np.array(q), [.30, .22, .15, .04], 8, 24))
        st.mesh(*xform(join(b), M), col=('#d8a24a', '#6a3a24', '#ffffff'), cls=8, ink=.85)
    return S


def rise(t):
    """helper for the surge out of the sea: t 0..1 -> (height factor, gape, hood)"""
    from lau.ease import smooth, back_out
    return back_out(min(1., t / .7), 1.2), smooth(.25, .8, t), smooth(.1, .6, t)
