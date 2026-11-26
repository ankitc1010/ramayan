"""Birds and the squirrel.

    from chars import birds as BD
    BD.flock(st, 'egret'|'goose'|'parrot'|'crow', P, vel, t, size=1.)          # between open and close: one mesh for the whole flock
    BD.vee(n, at, dirn, gap) -> positions of a flying wedge ;  BD.swarm(n, box, t, vel) -> positions wrapped in a box
    BD.specks(st, P, t, size)                                                     # far birds as tiny ink strokes
    BD.peacock(st, at, yaw, fan=0..1, t=...)      BD.squirrel(st, at, yaw, pose='sit'|'run'|'carry', ph)
Flapping meshes face +z in their own space."""
import numpy as np, math
from lau.stage import Fig, model, hexc
from lau.rig import V, nz, Rx, Ry, Rz
from lau.face import Face
from lau import cloth as CL
from chars.jatayu import feathers, FEATHER, join, xform

BIRD = '''#include "noise.glsl"
in vec3 vp,vn_;in vec2 vuv;
layout(location=0) out vec4 g0;layout(location=1) out vec4 g1;layout(location=2) out vec4 g2;layout(location=3) out vec4 g3;
uniform vec3 ro;uniform mat3 CamR;uniform float far,objId,inkw;uniform vec3 cA,cB,cC,cE,cF;uniform int species;
// uv.x = id + part*.1 + u*.1 (part 0 body 1 wing 2 beak 3 leg 4 tail), uv.y = v
void main(){
  vec3 n=normalize(vn_),v=vp-ro;if(dot(n,v)>0.) n=-n;vec3 f=transpose(CamR)[2];float vz=dot(v,f);gl_FragDepth=clamp(vz/far,0.,1.);
  float id=floor(vuv.x),x=fract(vuv.x)*10.;float pt=floor(x),u=(x-pt)/.98;vec3 b=cA,s=cB;float q=abs(vuv.y-.5)*2.;float ik=inkw;
  if(pt<.5){b=mix(cA,cF,smoothstep(.25,.0,vuv.y)*0.);if(species==2){b=mix(cA,cE,smoothstep(.28,.0,u)*0.);float rg=smoothstep(.02,.0,abs(u-.80)-.025);b=mix(b,cE,rg);}}
  else if(pt<1.5){                                                                   // wing: u shoulder..tip, v leading..trailing edge
    float fin=abs(fract(u*9.+.5)-.5);float tr=smoothstep(.45,.75,vuv.y);float cut=.80+.20*sqrt(max(0.,1.-pow(fin*2.,2.)))-(u>.6?.16*smoothstep(.25,.5,fin)*(u-.6)*4.:0.);if(vuv.y>cut) discard;
    b=mix(cA,cC,tr*smoothstep(.2,.7,u)+smoothstep(.72,.95,u)*.9);b=mix(b,b*.55,smoothstep(.08,.0,.5-fin)*step(.42,vuv.y)*.8);float ln=smoothstep(.03,.0,abs(vuv.y-.42));b=mix(b,b*.6,ln*.7);if(species==2)b=mix(b,cE,smoothstep(.3,.1,vuv.y)*smoothstep(.3,.1,u));}
  else if(pt<2.5){b=cE;s=cE*.45;} else if(pt<3.5){b=cE*.8;s=cE*.35;} else {b=mix(cA,cC,u);}
  g0=vec4(n,vz);g1=vec4(b,1.+clamp(ik,0.,.98)*.98);g2=vec4(s,1);g3=vec4(n,objId*64.+mod(id*5.+pt,61.)+1.);
}'''
# species: body, shadow, wing tip, beak/leg, extra; proportions: body length, neck, wing span (each), chord, leg trail
SPEC = dict(egret=(0, '#fffdf6', '#a6a8cc', '#f4f0e4', '#e0a030', '#ffffff', dict(neck=1.5, span=2.3, chord=.95, leg=1.5, beak=.6, curl=.6)), goose=(1, '#c8b8a0', '#5a5068', '#4a3a3e', '#e07a2c', '#f4ead8', dict(neck=1.7, span=2.5, chord=.85, leg=0., beak=.35, curl=.0)), parrot=(2, '#3fae4a', '#14505a', '#1f6ab0', '#d82c3a', '#e8c030', dict(neck=.25, span=1.6, chord=.72, leg=0., beak=.22, curl=0., tail=1.7)), crow=(3, '#2a2630', '#0c0a14', '#14121a', '#1a1418', '#000000', dict(neck=.35, span=1.7, chord=.9, leg=0., beak=.35, curl=0., tail=.7)), swan=(0, '#ffffff', '#9aa0cc', '#fff6ea', '#e0802c', '#ffffff', dict(neck=2.4, span=2.7, chord=1.1, leg=0., beak=.4, curl=0.)))


def _bird(flapv, kind, glide=0.):
    """one bird in its own space; flapv = phase 0..1"""
    sp = SPEC[kind][6]; a = 2 * math.pi * flapv; el = 34 * math.sin(a) + 6; tip = 30 * math.sin(a - 1.15); fold = .22 * max(0, -math.cos(a)); parts = []; bob = -.16 * math.sin(a)
    if glide: el, tip, fold = el * (1 - glide) + 8 * glide, tip * (1 - glide) + 3 * glide, fold * (1 - glide)
    def tag(m, part, flip=False): p, n, u, i = m; u = u.copy(); u[:, 0] = part * .1 + u[:, 0] * .098; return p, n, u, i
    nk = sp['neck']; c = sp['curl']
    body = np.array([(0, .02, -1.15), (0, .05, -.6), (0, 0, .1), (0, .08, .7)] + [(0, .14 + .55 * c * math.sin(k * 3.0) + .10 * k, .7 + nk * k * (1 - .45 * c)) for k in (.35, .7, 1.)] + [(0, .22 + .12 * 1 + 0 * c, .7 + nk * (1 - .45 * c) + .28)]); body[:, 1] += bob
    parts.append(tag(CL.tube(body, [.04, .28, .42, .33, .15, .12, .14, .20, .05], 8, 18), 0)); hd = body[-1]
    parts.append(tag(CL.tube(np.array([hd + V(0, 0, -.06), hd + V(0, -.02, sp['beak'] * .5), hd + V(0, -.06 - (.12 if kind == 'parrot' else 0), sp['beak'])]), [.10, .07, .01], 6), 2))
    if sp['leg']: parts.append(tag(CL.tube(np.array([(0, -.1 + bob, -.7), (0, -.05 + bob, -1.4), (0, -.12 + bob, -1.1 - sp['leg'])]), [.06, .05, .04], 5), 3))
    tl = sp.get('tail', .55); parts.append(tag(CL.strip(np.array([(0, .04 + bob, -.8), (0, .02 + bob, -1.1 - tl * .5), (0, -.06 + bob, -1.1 - tl)]), [.28, .46 if tl < 1 else .24, .34 if tl < 1 else .05], up=(1, 0, 0), m=3, n=6), 4))
    nu, nv = 8, 4
    for sg in (1, -1):
        G = np.zeros((nu, nv, 3)); x = y = 0.; e = math.radians(el)
        for k in range(nu):
            u = k / (nu - 1); s = sp['span'] * (1 - fold * u); ang = math.radians(el + tip * u * 1.1); ds = s / (nu - 1)
            if k: x += math.cos(ang) * ds; y += math.sin(ang) * ds
            ch = sp['chord'] * (1 - .30 * u) ; sw = .35 * math.sin(u * 2.6) - .55 * u * u - fold * 1.2 * u
            for j in range(nv): v = j / (nv - 1); G[k, j] = (sg * (.16 + x), .16 + y + bob - .10 * v * v - .06 * math.sin(v * 3), .42 + sw - ch * v)
        du = np.gradient(G, axis=0); dv = np.gradient(G, axis=1); N = np.cross(du, dv); N /= np.linalg.norm(N, axis=2, keepdims=True) + 1e-9; uv = np.stack(np.meshgrid(np.linspace(0, 1, nu), np.linspace(0, 1, nv), indexing='ij'), -1); i = (np.arange(nu - 1)[:, None] * nv + np.arange(nv - 1)[None]).reshape(-1)
        parts.append(tag((G.reshape(-1, 3), N.reshape(-1, 3), uv.reshape(-1, 2), np.concatenate([np.stack([i, i + nv, i + 1], 1), np.stack([i + 1, i + nv, i + nv + 1], 1)])), 1))
    return join(parts)


_CACHE = {}


def flock(st, kind, P, vel, t, size=1., rate=2.2, phase=None, glide=0., bank=0., seed=0, ink=.85, col=None):
    """P (n,3) world positions, vel (3,) or (n,3) flight direction; size = half the body length in world units"""
    P = np.atleast_2d(np.asarray(P, float)); n = len(P); r = np.random.default_rng(seed); ph = r.uniform(0, 1, n) if phase is None else np.broadcast_to(phase, (n,)); rt = rate * r.uniform(.9, 1.1, n); vel = np.broadcast_to(np.asarray(vel, float), (n, 3)); size = np.broadcast_to(size, (n,)); gl_ = np.broadcast_to(glide, (n,)); out = []
    for i in range(n):
        k = int(((t * rt[i] + ph[i]) % 1.) * 16); key = (kind, k, round(float(gl_[i]), 1))
        if key not in _CACHE: _CACHE[key] = _bird(k / 16, kind, key[2])
        p, nn, u, ix = _CACHE[key]; z = nz(vel[i]); x = nz(np.cross(V(0, 1, 0), z)); y = np.cross(z, x); a = math.radians(bank * (.6 + .4 * ph[i])); x, y = x * math.cos(a) + y * math.sin(a), y * math.cos(a) - x * math.sin(a); R = np.stack([x, y, z])
        u2 = u.copy(); u2[:, 0] += i; out.append((p @ R * size[i] + P[i], nn @ R, u2, ix))
    s = SPEC[kind]; c = col or s[1:6]; st.mesh(*join(out), col=c[:3], ink=ink, frag=BIRD, u=dict(species=s[0], cE=hexc(c[3]), cF=hexc(c[4])))


def vee(n, at, dirn, gap=4., spread=.8, t=0., seed=0):
    """a flying wedge, leader at `at`"""
    z = nz(dirn); x = nz(np.cross(V(0, 1, 0), z)); r = np.random.default_rng(seed); k = (np.arange(n) + 1) // 2; sg = np.where(np.arange(n) % 2, 1, -1); ph = r.uniform(0, 6, n)
    return np.asarray(at, float) - z * (gap * k)[:, None] + x * (sg * gap * spread * k)[:, None] + V(0, 1, 0) * (.25 * gap * np.sin(1.3 * t + ph))[:, None] + r.normal(size=(n, 3)) * .12 * gap


def swarm(n, box, t, vel=(6, 0, 0), seed=0, sway=1.):
    r = np.random.default_rng(seed); a, b = np.array(box, float); p = r.uniform(0, 1, (n, 3)) * (b - a) + np.asarray(vel, float) * t * r.uniform(.8, 1.2, (n, 1)); p = a + np.mod(p - 0, b - a); ph = r.uniform(0, 6.28, (n, 2)); p[:, 1] += sway * np.sin(1.4 * t + ph[:, 0]); p[:, 2] += sway * np.cos(1.1 * t + ph[:, 1]); return p


def specks(st, P, t, size=6., col='#2a1a24', rate=1.8, seed=0, alpha=1.):
    """far birds: two-stroke ink marks, size in pixels; P world (n,3) or pixels (n,2)"""
    P = np.asarray(P, float); r = np.random.default_rng(seed); ph = r.uniform(0, 1, len(P)); X = P if P.shape[1] == 2 else st.cam.project(P)[:, :2]; q = hexc(col, lin=False)
    def fn(c):
        c.set_source_rgba(*q, alpha); c.set_line_cap(1)
        for (x, y), p in zip(X, ph):
            s = size * (.7 + .6 * p); f = math.sin((t * rate + p) * 6.283); c.set_line_width(max(1.2, s * .22)); c.move_to(x - s, y - s * .55 * f); c.curve_to(x - s * .55, y - s * .5 - s * .2 * f, x - s * .2, y - s * .1, x, y); c.curve_to(x + s * .2, y - s * .1, x + s * .55, y - s * .5 - s * .2 * f, x + s, y - s * .55 * f); c.stroke()
    st.vector(fn)


# ------------------------------------------------------------------ small beasts as SDF (KIND 0 peacock, 1 squirrel)
SMALL = '''
#if KIND==0
uniform vec3 NK[8];
vec2 map(vec3 p){
  vec3 q=vec3(abs(p.x),p.yz);
  float d=sEll(p-vec3(0,4.1,0),vec3(1.05,1.15,1.75));d=smin(d,sEll(p-vec3(0,4.5,-1.4),vec3(.7,.7,1.1)),.5);d=smin(d,sEll(q-vec3(.75,4.25,-.2),vec3(.5,.85,1.5)),.3);
  float nk=1e3;for(int i=0;i<7;i++)nk=smin(nk,sCone(p,NK[i],NK[i+1],mix(.78,.26,sqrt(float(i)/7.)),mix(.78,.26,sqrt((float(i)+1.)/7.))),.1);
  vec3 H=NK[7];nk=smin(nk,sEll(p-H-vec3(0,.05,.1),vec3(.30,.32,.42)),.1);
  float all=smin(d,nk,.4);vec2 m=vec2(all,1.);
  m=U(m,vec2(sCone(p-H,vec3(0,.02,.42),vec3(0,-.10,.95),.13,.02),5.));vec3 he=vec3(abs(p.x),p.yz)-H-vec3(.24,.10,.22);m=U(m,vec2(length(he)-.085,7.));
  for(int i=0;i<5;i++){float a=(float(i)-2.)*.24;vec3 b=H+vec3(0,.28,-.05),e=b+vec3(sin(a)*.95,.95*cos(a),-.25);m=U(m,vec2(sCap(p,b,e,.018),5.));m=U(m,vec2(sEll(p-e,vec3(.10,.13,.06)),2.));}
  m=U(m,vec2(min(sCone(q,vec3(.42,3.2,-.1),vec3(.45,1.8,.05),.42,.16),min(sCone(q,vec3(.45,1.8,.05),vec3(.45,.12,-.05),.12,.10),min(sCone(q,vec3(.45,.10,-.05),vec3(.45,.06,.75),.09,.05),min(sCone(q,vec3(.45,.10,0),vec3(.85,.06,.55),.08,.04),sCone(q,vec3(.45,.10,0),vec3(.12,.06,.55),.08,.04))))),5.));
  return m;}
void surf(vec3 p,vec3 n,int m,inout Surf s){
  if(m==1){float nkk=smoothstep(4.5,5.3,p.y+.5*p.z);vec3 u3=p;vec2 u=vec2(atan(p.x,p.z-.2)*3.2,-p.y*2.6);float e=0.,id=0.;float row=floor(u.y);
    for(int k=1;k>=-1;k--){float r=row+float(k);vec2 f=vec2(u.x+.5*mod(r,2.),u.y-r);float c=floor(f.x);f.x=fract(f.x)-.5;float y=f.y-.35;float d=length(vec2(f.x*1.05,max(y,0.)*.78))-.52;if(d<0.&&f.y>-.2){e=d;id=h21(vec2(c,r));break;}}
    vec3 nb=mix(hex(0x0f3fb0),hex(0x1a8ad0),smoothstep(.2,.8,n.y*.5+.5));vec3 bd=mix(hex(0x0c6a6a),hex(0x2aa050),id);vec3 wg=mix(hex(0xc8884a),hex(0x8a5a3a),step(.5,fract(p.z*2.+p.y)));
    float wing=step(.80,abs(p.x))*step(abs(p.y-4.2),.8)*step(p.z,.9);s.base=mix(bd,nb,nkk);s.base=mix(s.base,wg,wing);s.sh=s.base*vec3(.30,.26,.46);s.base=mix(s.base,hex(0xe8d27a),smoothstep(-.24,-.17,e)*.4);s.base=mix(s.base,s.base*.4,smoothstep(-.10,-.03,e));s.cls=8.;
    vec3 h=p-NK[7];if(length(h)<.62){float pa=smoothstep(.03,-.0,abs(length(vec2(h.y-.10,h.z-.22))-.20)-.05);s.base=mix(s.base,hex(0xf6f2e4),pa*step(.1,abs(h.x)));float ln=smoothstep(.03,.0,abs(h.y-.12-.1*(h.z-.2))-.025);s.base=mix(s.base,hex(0x0c0a18),ln);s.ink=.6;}}
}
#else
uniform vec3 JQ[16];uniform float carry;
vec2 map(vec3 p){
  // JQ 0 rump 1 chest 2 head 3..6 fore paws (elbow, hand) L R  7..10 hind (knee, foot) L R  11..15 tail
  float d=sCone(p,JQ[0],JQ[1],.62,.46);d=smin(d,length(p-JQ[0])-.66,.2);d=smin(d,sCone(p,JQ[1],JQ[2],.40,.36),.2);
  vec3 h=p-JQ[2];vec3 q=vec3(abs(h.x),h.yz);d=smin(d,sEll(h,vec3(.40,.40,.46)),.12);d=smin(d,sCone(h,vec3(0,-.08,.3),vec3(0,-.14,.62),.24,.12),.12);
  for(int i=0;i<2;i++){d=smin(d,min(sCone(p,JQ[1]+vec3(i==0?.3:-.3,-.1,.1),JQ[3+2*i],.20,.14),sCone(p,JQ[3+2*i],JQ[4+2*i],.14,.12)),.1);d=smin(d,min(sCone(p,JQ[0]+vec3(i==0?.3:-.3,-.1,.1),JQ[7+2*i],.40,.28),sCone(p,JQ[7+2*i],JQ[8+2*i],.22,.14)),.14);}
  vec2 m=vec2(d,1.);float tl=1e3;for(int i=0;i<4;i++){float k=float(i)/4.;tl=smin(tl,sCone(p,JQ[11+i],JQ[12+i],.13+.27*sin(k*2.75),.13+.27*sin((k+.25)*2.75)),.15);}tl-=.07*pow(vn3(p*vec3(9.,9.,9.)),1.6)+.035*vn3(p*26.);m=U(m,vec2(tl*.62,2.));
  m=U(m,vec2(min(sEll(q-vec3(.26,.40,-.10),vec3(.10,.19,.08)),1e3),1.));m=U(m,vec2(length(q-vec3(.30,.08,.24))-.105,7.));m=U(m,vec2(length(h-vec3(0,-.10,.72))-.07,7.));
  if(carry>.5)m=U(m,vec2(sBox(p-.5*(JQ[4]+JQ[6])-vec3(0,.05,.12),vec3(.30,.24,.26),.14)+.04*vn3(p*6.),9.));
  return m;}
void surf(vec3 p,vec3 n,int m,inout Surf s){
  if(m==1||m==2){float f=sin(p.y*30.+p.z*22.+5.*vn3(p*5.))*.5+.5;s.base*=.86+.2*f;
    if(m==1){vec3 ax=normalize(JQ[1]-JQ[0]),o=p-JQ[0];float al=dot(o,ax);vec3 r=o-ax*al,up=normalize(vec3(0,1,0)-ax*ax.y);float ph=abs(atan(r.x,dot(r,up))),inb=smoothstep(-.55,-.2,al)*smoothstep(length(JQ[1]-JQ[0])+.30,length(JQ[1]-JQ[0])-.05,al);
      s.base=mix(s.base,hex(0x6a3a24),inb*.75*smoothstep(.20,.08,abs(ph-.33)));s.base=mix(s.base,hex(0xfff2d4),inb*clamp(smoothstep(.12,.07,ph)+smoothstep(.12,.07,abs(ph-.66)),0.,1.));s.base=mix(s.base,hex(0xfbeed6),smoothstep(.35,.75,dot(n,vec3(0,-.5,.8))+.15*sin(p.y*40.+p.x*20.))*smoothstep(.1,.5,JQ[2].y-p.y+.2*JQ[2].z));}
    if(m==2){float f2=sin(p.y*46.+p.z*30.+6.*vn3(p*7.))*.5+.5;s.base=mix(s.base*.72,hex(0xe8cfa6),smoothstep(.35,.95,f2)*.55);}}
  if(m==7){vec3 h=p-JQ[2];s.base=hex(0x140a10);if(length(vec3(abs(h.x),h.yz)-vec3(.36,.14,.30))<.06)s.base=vec3(1.3);s.cls=6.;}
  s.ink=.8;
}
#endif
'''
_P = {1: ('#1a6ab0', '#0c2050', 8), 2: ('#2a8ad8', '#0c2060', 8), 5: ('#8a6a5a', '#3c2830', 1), 7: ('#140a10', '#08040a', 8), 9: ('#b8aa98', '#5c5266', 1)}
PEA = Fig('peacock', SMALL, _P, human=False, bound=(0, 4.4, 0, 5.6), defs='#define KIND 0')
SQ = Fig('squirrel', SMALL, {**_P, 1: ('#b87a4a', '#5a3434', 1), 2: ('#a87050', '#4a2c30', 1)}, human=False, bound=(0, 1.6, 0, 3.2), defs='#define KIND 1')

EYE = '''#include "noise.glsl"
in vec3 vp,vn_;in vec2 vuv;
layout(location=0) out vec4 g0;layout(location=1) out vec4 g1;layout(location=2) out vec4 g2;layout(location=3) out vec4 g3;
uniform vec3 ro;uniform mat3 CamR;uniform float far,objId,inkw,shimmer;
void main(){
  vec3 n=normalize(vn_),v=vp-ro;bool back=dot(n,v)>0.;if(back) n=-n;vec3 f=transpose(CamR)[2];float vz=dot(v,f);gl_FragDepth=clamp(vz/far,0.,1.);
  float id=floor(vuv.x),u=fract(vuv.x)/.98,s0=vuv.y*2.-1.,q=abs(s0);float r=h11(id+2.3);
  vec2 e=vec2(s0,(u-.86)/.115);float eye=length(e*vec2(1.,.95));bool vane=eye<1.;
  float w=mix(.10,.55,smoothstep(.05,.75,u))*(.65+.35*sin(u*150.+q*9.));float shaft=step(q,.07);
  if(!vane){if(u>.97||q>w) {if(shaft<.5||u>.88) discard;}if(shaft<.5&&sin(u*150.-q*16.+r*6.)<-.15) discard;}
  vec3 b=mix(hex(0x2a7a3a),hex(0x7ab040),smoothstep(.3,.8,u))*(.8+.3*r);float cl=8.,ik=inkw*.5;vec3 s;
  b=mix(b,hex(0xc89a4a),shaft);
  if(vane){float a=.05*sin(atan(e.y,e.x)*26.);b=mix(hex(0x8ab83a),hex(0xb87a2a),smoothstep(.98,.86,eye+a));b=mix(b,hex(0xe8b850),smoothstep(.74,.70,eye));b=mix(b,hex(0x14a08a),smoothstep(.62,.57,eye));vec2 h=e-vec2(0,-.06);float ht=length(h*vec2(1.,1.1))+.10*smoothstep(.2,.0,abs(h.x))*step(0.,h.y)*1.6;b=mix(b,hex(0x10206a),smoothstep(.38,.33,ht));ik=inkw;if(eye>.60&&eye<.66){cl=2.;b=vec3(1.,.9,.6);}}
  if(back){b*=vec3(.55,.50,.48);cl=1.;}
  s=b*vec3(.30,.28,.44);
  g0=vec4(n,vz);g1=vec4(b,cl+clamp(ik,0.,.98)*.98);g2=vec4(s,1);g3=vec4(n,objId*64.+mod(id,61.)+1.);
}'''


def peacock(st, at=(0, 0, 0), yaw=0., scale=1., M=None, fan=0., t=None, head=(0., 0.), step=0., pitch=0.):
    """standing about 9 units tall; fan 0 train trailing .. 1 the full wheel; head = (yaw, up) degrees"""
    t = st.t if t is None else t; M = model(at, yaw, pitch, 0, scale) if M is None else np.asarray(M, float); Rh = Ry(head[0]); P = [V(0, 4.5, .9)]
    for i in range(7):
        u = (i + 1) / 7; P.append(V(0, 4.5, .9) + Ry(head[0] * u) @ V(0, 4.3 * u + .10 * math.sin(t * 1.3) * u, 1.15 * math.sin(u * 2.5) * (1 - .35 * u) + .30 * u))
    st.fig(PEA, M=M, u=dict(NK=np.array(P), bound=np.array([0, 4.6, .3, 5.6])))
    n = 74; g = (np.arange(n) * .61803) % 1.; ring = np.sqrt((np.arange(n) + 1) / n); r0 = np.tile(V(0, 4.7, -1.9), (n, 1)); e = fan * fan * (3 - 2 * fan); side = g * 2 - 1
    ang = side * 118 * e + side * 9 * (1 - e); sh = .6 * np.sin(t * 11 + np.arange(n)) * e; a = np.radians(ang + sh); L = (7.2 + 5.2 * ring) * (1 + .08 * (1 - e)); L = L * (1 - .10 * np.abs(side) * e)
    up = np.stack([np.sin(a), np.cos(a), np.full(n, -.22) - .10 * (1 - ring)], 1); dn = np.stack([np.sin(a) * 1.0, -.30 - .05 * ring, -np.ones(n)], 1); d = up * e + dn * (1 - e); d[:, 2] += -.4 * e * (1 - e) * 2
    nor = np.stack([np.zeros(n), (1 - e) * np.ones(n), e * np.ones(n) + .05], 1); r0 = r0 + np.stack([.55 * side, .25 * (1 - e) * (1 - np.abs(side)) - .02 * np.arange(n) / n * 8 * (1 - e) * 0, -.012 * np.arange(n)], 1)
    off = nor * (.012 * (n - np.arange(n)))[:, None]; bd = np.where(e > .5, -.10 * e, .10 * (1 - e)); L2 = L
    k = np.argsort(-ring); m = feathers(r0 + off, d, nor, L2, np.full(n, .80), bd, .06, 0., nl=12)
    pts = m[0]; gy = .12
    if e < .95: pts[:, 1] = np.maximum(pts[:, 1], gy + .25 * (pts[:, 1] - gy) * (pts[:, 1] < gy))
    st.mesh(*xform((pts, *m[1:]), M), col=('#2a7a3a', '#0c2a2a', '#c89a4a'), ink=.8, frag=EYE, u=dict(shimmer=t))
    # short brown tail that props the fan, and green scale feathers over the root
    n2 = 11; a2 = np.radians(np.linspace(-62, 62, n2) * (.15 + .85 * e)); d2 = np.stack([np.sin(a2), np.cos(a2) * e - .15 * (1 - e), -(1 - e) - .25 * np.ones(n2)], 1); st.mesh(*xform(feathers(np.tile(V(0, 4.6, -2.1), (n2, 1)), d2, nor[:n2], 4.2, .5, 0., .1, 0.), M), col=('#8a5230', '#3c2028', '#5a3020'), ink=.8, frag=FEATHER, u=dict(shape=1, cE=hexc('#e0b070'), tipAt=.6, gild=0., bars=0., ragged=1., asp=6., burnF=0.))
    rows = []
    for j in range(4):
        n3 = 9 + 3 * j; s3 = np.linspace(-1, 1, n3); a3 = np.radians(s3 * (100 * e + 12)); d3 = np.stack([np.sin(a3), np.cos(a3) * e - .1 * (1 - e), -(1 - e) * np.ones(n3) - .12], 1); rows.append(feathers(V(0, 4.75, -1.7) + d3 * (.25 + .55 * j) + (nor[:1] * (.95 - .08 * j)), d3, np.tile(nor[:1], (n3, 1)), 1.5, .48, 0., .15, 0., id0=j * 20, nl=5))
    st.mesh(*xform(join(rows), M), col=('#2aa058', '#0c3a3a', '#1a6a9a'), ink=.8, frag=FEATHER, u=dict(shape=2, cE=hexc('#e8d27a'), tipAt=.7, gild=1., bars=0., ragged=0., asp=3., burnF=0.))
    return M


def squirrel(st, at=(0, 0, 0), yaw=0., scale=.55, M=None, pose='sit', ph=0., t=None, carry=True, roll=0., pitch=0.):
    """the three-striped palm squirrel of the bridge; at scale 1 it sits 2.8 units high (use about .4 to .6); pose sit (holds the pebble), run(ph), bow"""
    t = st.t if t is None else t; M = model(at, yaw, pitch, roll, scale) if M is None else np.asarray(M, float); J = np.zeros((16, 3)); tw = .05 * math.sin(t * 9)
    if pose == 'run':
        a = 2 * math.pi * ph; s, c = math.sin(a), math.cos(a); y = .25 * max(0, s); J[0] = (0, .85 + y, -.75); J[1] = (0, .95 + y - .15 * c, .55); J[2] = (0, 1.35 + y - .1 * c, 1.15); rch = .55 * c
        for k, sg in enumerate((1, -1)):
            J[3 + 2 * k] = (sg * .36, .62 + y * .6, .75 + rch * .5); J[4 + 2 * k] = (sg * .34, .12 + max(0, s) * .4, 1.0 + rch + .1 * sg); J[7 + 2 * k] = (sg * .42, .62 + y * .6, -.45 - rch * .4); J[8 + 2 * k] = (sg * .40, .14 + max(0, s) * .4, -.75 - rch + .1 * sg)
        for i in range(5): u = i / 4; J[11 + i] = (.10 * math.sin(a - 2 * u) * u, .90 + y + .95 * math.sin(2.5 * u) + .28 * math.sin(a - u * 2.5) * u, -1.2 - 2.3 * u)
    else:
        b = 1. if pose == 'bow' else 0.; J[0] = (0, .75, -.35); J[1] = (0, 1.75 - .35 * b, .12 + .3 * b); J[2] = (0, 2.45 - .6 * b + tw * .3, .38 + .35 * b)
        for k, sg in enumerate((1, -1)): J[3 + 2 * k] = (sg * .46, 1.45 - .3 * b, .50 + .2 * b); J[4 + 2 * k] = (sg * .20, 1.55 - .45 * b, .86 + .25 * b); J[7 + 2 * k] = (sg * .60, .92, .22); J[8 + 2 * k] = (sg * .52, .16, .62)
        for i in range(5): u = i / 4; J[11 + i] = (.25 * math.sin(t * 2.2 - u * 2) * u, .35 + 2.6 * u - .2 * u * u, -.95 - .75 * math.sin(u * 2.6) + .35 * max(0, u - .7))
    st.fig(SQ, M=M, u=dict(JQ=J, carry=1. if carry and pose != 'run' else 0., bound=np.array([0, 1.6, -.4, 3.3])))
    return M
