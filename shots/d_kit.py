"""Things the flight and the bridge share: mount Mahendra and its sea, mural cloud sprites, broken rocks, the giant Hanuman."""
import numpy as np, math, cairo
import moderngl as mgl
from lau import gl, cloth as CL, props as PR, fx as FX
from lau.stage import hexc, Light
from lau.rig import V, nz, eul
from lau.ease import *
from lau.look import SKY, SAFFRON
from lau.plates import plate
from chars import hanuman as HM
from worlds import place, flora as FL

SEA_Y = -300.
CX, CZ = 24., 7.                               # middle of the bare top; he stands at the origin, near its seaward edge
SEAWARD = V(.77, 0, -.64)                       # the way he faces: over the water
GOLD_FOG = '#f7c27e'
SUN = nz(V(.62, .16, -.77))

# ------------------------------------------------------------------ the mountain (same formula in python and GLSL)


def ground(x, z):
    x, z = np.asarray(x, float) - CX, np.asarray(z, float) - CZ; r = np.hypot(x, z) + 1e-6; a = np.arctan2(x, z); s = x * .77 - z * .64; rd = r + 7 * np.sin(3 * a + 1) + 4 * np.sin(7 * a); q = np.maximum(rd - 50, 0); w = np.clip((s / r + .86) / .56, 0, 1); w = w * w * (3 - 2 * w)
    inn = -128 * (1 - np.exp(-q * .0060)); sea = -345 * (1 - np.exp(-q * .0046)); u = np.clip(q / 160, 0, 1); u = u * u * (3 - 2 * u)
    return inn * (1 - w) + sea * w + u * (20 * np.sin(x * .0170 + 1) * np.sin(z * .0150 + 2) + 9 * np.sin(x * .041 + z * .033))


_H = '''
float ground(vec2 p){p-=vec2(CXZ);float r=length(p)+1e-6,a=atan(p.x,p.y),s=p.x*.77-p.y*.64;float rd=r+7.*sin(3.*a+1.)+4.*sin(7.*a);float q=max(rd-50.,0.);float w=smoothstep(-.86,-.30,s/r);
 float inn=-128.*(1.-exp(-q*.0060)),sea=-345.*(1.-exp(-q*.0046));float u=smoothstep(0.,160.,q);return mix(inn,sea,w)+u*(20.*sin(p.x*.0170+1.)*sin(p.y*.0150+2.)+9.*sin(p.x*.041+p.y*.033));}
'''
_H = _H.replace('CXZ', '%g,%g' % (CX, CZ))
MOUNT = '''
#define TMAX 2600.
#define STEPS 130
#define RELAX .80
#define PLANES
#define BOUND
uniform float seaY,crackR,crackK,crater,scorch,waveR;uniform vec3 cDeep,cMid,cLite,cFoam,cFar,uPaint;uniform vec2 sunAz;
''' + _H + '''
vec2 bound(vec3 o,vec3 d){float t0=0.,t1=TMAX;if(o.y>30.){if(d.y>=0.) return vec2(1,0);t0=(30.-o.y)/d.y;}else if(d.y>0.) t1=min(t1,(30.-o.y)/d.y+1.);return vec2(t0,max(t1,t0+.1));}
float planes(vec3 o,vec3 d,out float m,out vec3 n){m=9.;n=vec3(0,1,0);return d.y<0.?(seaY-o.y)/d.y:1e9;}
float rocky(vec3 p,float q){return 0.;}
float rim(vec2 p){p-=vec2(CXZ);float r=length(p),a=atan(p.x,p.y);return r+7.*sin(3.*a+1.)+4.*sin(7.*a);}
vec2 map(vec3 p){float h=ground(p.xz);float r=length(p.xz);
 float rd=rim(p.xz);if(r<230.){float edge=smoothstep(38.,60.,rd)*smoothstep(230.,120.,r);if(edge>0.){vec4 v=voro(p.xz*.052);vec4 v2=voro(p.xz*.16+3.);h+=edge*(9.*(v.z-.45)+3.*(v2.z-.5)-1.2*smoothstep(.12,.0,v.y));}}
 if(crater>0.&&r<110.){float c=crater*smoothstep(64.,12.,r+9.*sin(atan(p.x,p.z)*5.));vec4 v=voro(p.xz*.075+9.);h-=c*26.*(.6+.7*v.z);}
 return vec2((p.y-h)*.72,1.);}
void surf(vec3 p,vec3 n,int m,inout Surf s){
 vec3 unl=1./max(mix(uAmb,uKey,.55),vec3(.02));
 if(m==9){ // painted water
   float h=ground(p.xz)-seaY;float far=smoothstep(900.,9000.,gT);
   vec3 c=mix(cDeep,cMid,smoothstep(.35,.65,fbm(p.xz*.0032+vec2(fT*.02,0))));
   c=mix(c,cLite,smoothstep(-46.,-4.,h)*.85);
   // rows of painted wave scallops, three sizes, each fading out as it gets too fine
   for(int i=0;i<3;i++){float S=i==0?16.:i==1?46.:130.;float lod=smoothstep(.16,.05,gPx/S);if(lod<=0.) continue;vec2 u=p.xz/S;u.y+=.10*sin(u.x*1.7+fT*.6);u+=vec2(fT*(.10+.05*float(i)),fT*.16);float row=floor(u.y*1.6);vec2 f=vec2(fract(u.x+.5*mod(row,2.))-.5,fract(u.y*1.6));float hh=h21(vec2(floor(u.x+.5*mod(row,2.)),row));float d=length(vec2(f.x*1.1,f.y-.02))-.52;float ln=smoothstep(.07,.02,abs(d))+.55*smoothstep(.05,.015,abs(d+.14))+.3*smoothstep(.04,.01,abs(d+.26));c=mix(c,cDeep*.62,ln*lod*(.30+.2*hh));c=mix(c,cFoam,smoothstep(.07,.0,abs(d+.05))*step(.80,hh)*lod*.75);}
   // swell toward the shore: rings of foam
   if(h>-70.&&h<14.){float k=h*.085-fT*.55+.9*fbm(p.xz*.02);float b=abs(fract(k)-.5);float w=.06+.16*smoothstep(-50.,0.,h);float fo=smoothstep(w,w-.06,b)*smoothstep(-70.,-18.,h)*smoothstep(.30,.48,fbm(p.xz*.05+fT*.1)+.16*smoothstep(-30.,0.,h));c=mix(c,cFoam,fo*.9);c=mix(c,cFoam,smoothstep(-5.,-1.5,h+2.*fbm(p.xz*.09)));}
   // waves that race out from the mountain's foot
   if(waveR>0.){float rr=length(p.xz)+26.*(fbm(p.xz*.006)-.5);for(int i=0;i<4;i++){float R=waveR*(1.-.17*float(i));float w=(22.+.050*R);float x=(rr-R)/w;float k=smoothstep(1.,0.,abs(x))*smoothstep(200.,420.,R)*(1.-.12*float(i));float crest=smoothstep(.42,.60,k-.50+.95*fbm(p.xz*.6/w+vec2(fT,0)));c=mix(c,cLite,k*.55);c=mix(c,cFoam,crest);c=mix(c,cDeep*.7,smoothstep(.5,.0,abs(x+1.15))*.5*smoothstep(200.,420.,R));}}
   // sun path
   vec2 vd=normalize(p.xz-ro.xz);float al=dot(vd,sunAz);float path=smoothstep(.80,1.,al);float gl=smoothstep(.56,.70,vn(p.xz*vec2(.05,.05)/max(1.,gPx*.35)+fT*vec2(1.1,.7))*.6+vn(p.xz*.13/max(1.,gPx*.35)-fT*1.4)*.5);
   c=mix(c,cFar,far*.75);c+=vec3(1.,.72,.34)*path*(.10+.62*gl*smoothstep(.86,1.,al)*smoothstep(.42,.10,-gRd.y))*smoothstep(60.,900.,gT);
   c=mix(c,cFar*1.06,smoothstep(6000.,18000.,gT));
   s.cls=6.;s.base=c*unl;s.sh=s.base;s.ink=0.;s.part=2.;return;}
 float h=p.y,r=length(p.xz);float rd=rim(p.xz);float st=n.y;float v=fbm(p.xz*.05),v2=fbm(p.xz*.014+4.);
 vec3 rock=mix(hex(0xb87a4c),hex(0xe6bd86),v),rsh=mix(hex(0x573049),hex(0x7a4a5e),v);
 vec3 grass=mix(hex(0x5f8a3a),hex(0xb4b854),smoothstep(.35,.7,v2)),gsh=mix(hex(0x1c4248),hex(0x2f5648),v2);
 float gk=smoothstep(.80,.90,st+.10*(v-.5))*smoothstep(36.,64.,rd);
 s.base=mix(rock,grass,gk);s.sh=mix(rsh,gsh,gk);
 // tufts: the mural painter's little arcs
 float l=pLodQ(9.);vec2 u=p.xz/9.;float row=floor(u.y);vec2 f=vec2(fract(u.x+.5*mod(row,2.))-.5,fract(u.y));float d=abs(length(vec2(f.x,f.y-.1))-.40);s.base=mix(s.base,s.base*.70,smoothstep(.07,.02,d)*gk*l*.6*step(.4,h21(vec2(floor(u.x+.5*mod(row,2.)),row))));
 // beach
 float b=h-seaY;float bk=smoothstep(26.,12.,b+10.*fbm(p.xz*.03));s.base=mix(s.base,hex(0xf2d9a2),bk);s.sh=mix(s.sh,hex(0xa8788a),bk);s.base=mix(s.base,hex(0xc89a6a),smoothstep(7.,3.,b)*.6);
 // bare top: fractured slabs
 float top=smoothstep(62.,40.,rd);{vec4 q=voro(p.xz*.085);float e=smoothstep(.055,.015,q.y)*pLodQ(2.);s.base*=1.-.30*top*(q.z-.5);s.base=mix(s.base,s.sh*.8,e*top*.75);s.base=mix(s.base,hex(0xf0d29a),top*.25*smoothstep(.4,.7,v));}
 // cracks that run out from under his feet
 if(crackR>0.){float a=atan(p.x,p.z);float w=0.;for(int i=0;i<2;i++){float n_=i==0?9.:17.;float aa=a*n_/TAU+.35*(fbm(vec2(r*.06,float(i)*7.))-.5)*2.*n_/9.+.12*sin(r*.35+float(i));float id=floor(aa);float hh=h21(vec2(id,float(i)+3.));float L=crackR*(.45+.75*hh)*(i==0?1.:.7);float wd=(i==0?1.35:.8)*crackK*smoothstep(L,L*.15,r);float dd=abs(fract(aa)-.5)*TAU/n_*r;w=max(w,smoothstep(wd,wd*.55,dd)*step(r,L));s.base=mix(s.base,hex(0xffe2a8),smoothstep(wd*2.2,wd*1.1,dd)*step(r,L)*.35);}
   s.base=mix(s.base,hex(0x2a0c16),w);s.sh=mix(s.sh,hex(0x14060e),w);}
 s.base=mix(s.base,hex(0x6a3424),scorch*smoothstep(70.,20.,r));
 s.ink=mix(.75,.35,smoothstep(150.,700.,gT))*mix(1.,.45,gk);if(gk>.5) s.ink=.22;
}
'''.replace('CXZ', '%g,%g' % (CX, CZ)).replace('vec2 bound(', 'float pLodQ(float size){return smoothstep(.42,.12,gPx/size);}\nvec2 bound(')

SEACOL = dict(cDeep='#0b5a74', cMid='#17929a', cLite='#5fd0b8', cFoam='#fff3da', cFar='#e8c694')


def mount(st, crackR=0., crackK=1., crater=0., scorch=0., waveR=0., sun=SUN, **k):
    u = dict(seaY=SEA_Y, crackR=float(crackR), crackK=float(crackK), crater=float(crater), scorch=float(scorch), waveR=float(waveR), uPaint=(1, 1, 1), sunAz=tuple(nz(V(sun[0], sun[2]))), **{a: hexc(v) for a, v in {**SEACOL, **k}.items()})
    place.draw(st, MOUNT, u=u, sun=0.)


def trees(st, near=70., far=640., n=1500, seed=3, season='spring', haze0=200., bend=None, lo=34., hi=62., skip=None):
    """the forest on his slopes: fixed places, sizes and kinds"""
    r = np.random.default_rng(seed); a = r.uniform(0, 6.283, n); q = near + (far - near) * r.uniform(0, 1, n) ** .75; x, z = np.sin(a) * q, np.cos(a) * q; y = ground(x, z); m = y > SEA_Y + 34
    if skip is not None: m &= ~skip(x, z)
    x, y, z = x[m], y[m], z[m]; P = np.c_[x, y - 1.5, z]; k = r.integers(0, 4, len(P)); D = np.linalg.norm(P - st.cam.eye, axis=1); hz = np.clip((D - haze0) / 1500., 0, .62)
    front = ((P - st.cam.eye) @ st.cam.R[2]) > 2.; kinds = ('pahari_round', 'mango', 'ashoka', 'kadamba')
    for j, kd in enumerate(kinds):
        s = (k == j) & front
        if s.any():
            lean = 0. if bend is None else bend(P[s])
            FL.scatter(st, kd, P[s], (lo + hi) / 2, season=season if kd != 'ashoka' else 'summer', seed=seed + j, vary=.28, haze=hz[s], hazeCol=hexc(GOLD_FOG), tint=(.92, .84, .74), lean=lean) if bend is None else _bent(st, kd, P[s], (lo + hi) / 2, season if kd != 'ashoka' else 'summer', seed + j, hz[s], lean)


def _bent(st, kind, pos, height, season, seed, haze, lean):
    n = len(pos); nv = FL.KINDS[kind][6]; r = np.random.default_rng(seed); v = r.integers(0, nv, n); hh = height * (1 + .28 * r.uniform(-1, 1, n)); fl = r.choice([-1., 1.], n); ph = r.uniform(0, 6.28, n); ti = np.array((.92, .84, .74)) * (1 + .1 * r.uniform(-1, 1, (n, 1)) + .05 * r.uniform(-1, 1, (n, 3))); lean = np.broadcast_to(lean, (n,))
    for j in range(nv):
        m = v == j
        if m.any(): FL.cards(st, FL.plate_of(kind, season, j), pos[m], hh[m], fl[m], lean=lean[m], phase=ph[m], tint=ti[m], haze=haze[m], hazeCol=hexc(GOLD_FOG))


def sky(st, **k):
    st.paint('sky.frag', **SKY(SAFFRON, **{**dict(cZen='#b8502c', cMid='#f09a48', cHor='#ffdc92', cLow='#f2bd7c', sunDir=tuple(SUN), sunR=.062, sunCol='#fff2c0', sunGlow=.85, rays=.5, cov=.45, cy0=.02, cy1=.16, cscale=1.8, cLit='#fff4d0', cCM='#ffce8c', cSh='#e08a5a', cInk='#7a3020', cink=.65), **k}))


def light(**k):
    return Light(**{**dict(key=(.80, .42, .30), keyCol='#ffe6bc', amb='#8478b4', rim=(.75, .35, -.75), rimCol=(1.5, .95, .42), bounceCol=(.22, .12, .06), envT='#ffe2b0', envM='#ffb868', envB='#5a7a8a', fogCol=GOLD_FOG, fog=(.00026, 260., .0012, SEA_Y), ink=3.2), **k})


# ------------------------------------------------------------------ mural clouds: painted once, flown as sprites
CW, CH, NVAR = 1024, 576, 8


_BAKE = '''
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform float seed;uniform int mode;
float sm2(float a,float b,float k){float h=max(k-abs(a-b),0.)/k;return min(a,b)-h*h*k*.25;}
float topAt(float x){float e=pow(max(0.,1.-pow(abs((x-.22*(h11(seed+3.)-.5))/.86),2.6)),.75);return .16+.78*e*(.22+.95*fbm(vec2(x*1.55+seed*3.17,seed*1.3)));}
float bank(vec2 p,out float tp){const float cs=.235;float xi=floor(p.x/cs),d=1e3;tp=0.;float ws=0.;
 for(int i=-2;i<=2;i++){float id=xi+float(i);vec2 h=h22(vec2(id,seed*7.3)),g=h22(vec2(id+.5,seed*3.1));float cx=(id+.5+(h.x-.5)*.5)*cs;if(abs(cx)>.82) continue;float top=topAt(cx);float w=exp(-pow((p.x-cx)/cs,2.)*1.6);tp+=w*top;ws+=w;float r=min(cs*(.40+.42*h.y),top*.75);
  d=min(d,length(p-vec2(cx,top-r))-r);d=min(d,length(p-vec2(cx+cs*(.6*(g.x-.5)+.32),top-r*1.85))-r*(.70+.35*g.y));d=min(d,length(p-vec2(cx-cs*.40,top-r*2.1-cs*.1*g.y))-r*(.78+.3*g.x));}
 tp/=max(ws,.3);float cur=max(p.y-(tp-cs*.60),abs(p.x)-.80);return sm2(d,cur*.8,cs*.25);}
float puff(vec2 p,out float tp){float d=length(p-vec2(0,-.04))-.46;for(int i=0;i<9;i++){vec2 h=h22(vec2(float(i),seed*5.1));float a=(float(i)+.5*h.x)/9.*TAU;float r=.20+.15*h.y;d=min(d,length(p-vec2(cos(a),sin(a)*.94)*(.46+.10*h.x))-r);}tp=.6;return d;}
float sd(vec2 p){float tp;p+=(vec2(vn(p*9.+seed),vn(p*9.+7.))-.5)*.035+(vec2(vn(p*26.+seed),vn(p*26.+7.))-.5)*.012;return mode==0?bank(p,tp):puff(p,tp);}
void main(){vec2 p=mode==0?vec2(uv.x*2.-1.,uv.y*1.125):(uv*2.-1.)*vec2(1.78,1.);float tp;float dm=mode==0?bank(p,tp):puff(p,tp);float d=sd(p);
 float al=smoothstep(.004,-.004,d);float u=-d;float hy=mode==0?smoothstep(.10,max(tp,.3),p.y):smoothstep(-.75,.75,p.y+.25*p.x);
 float shd=sd(p+vec2(.055,.085));float lite=smoothstep(-.02,.06,shd-d);
 float tone=.18+.62*hy+.22*lite+.20*(fbm(p*vec2(4.,6.)+seed)-.5);
 float ink=0.;float pr=.5+.5*smoothstep(.25,.65,vn(p*9.+seed));float S=mode==0?1.:1.25;
 ink+=smoothstep(.015,.006,abs(u-.005))*.95;ink+=smoothstep(.0075,.0028,abs(u-.050*S))*.62*pr;ink+=smoothstep(.0068,.0024,abs(u-.098*S))*.50*pr;ink+=smoothstep(.0062,.0022,abs(u-.150*S))*.40*pr;ink+=smoothstep(.0056,.0020,abs(u-.215*S))*.30*pr;
 if(mode==0) ink*=smoothstep(.10,.34,p.y+.10*(fbm(p*6.+seed)-.5))*.9+.1;
 float rim=smoothstep(.046,.014,u)*smoothstep(.010,.018,u)*smoothstep(.15,.6,hy+.5*lite);
 if(mode==0){float ft=smoothstep(.02,.30,p.y+.13*(fbm(p*vec2(4.,9.)+seed)-.5));al*=ft*smoothstep(1.,.86,abs(p.x));}
 o=vec4(clamp(tone,0.,1.),clamp(ink,0.,1.),rim,1.)*al;}
'''
_AT = {}


def _atlas(mode):
    if mode not in _AT:
        c = gl.ctx(); t = c.texture((CW * 2, CH * 4), 4, dtype='f1'); fb = c.framebuffer([t]); p = gl.program(_BAKE); fb.use(); c.disable(mgl.BLEND)
        for k in range(NVAR): c.viewport = ((k % 2) * CW, (3 - k // 2) * CH, CW, CH); gl.set_uniforms(p, dict(seed=float(3.7 * k + 1.3 + 40 * mode), mode=mode)); gl.quad(p).render(mgl.TRIANGLE_STRIP)
        t.build_mipmaps(); t.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR); t.anisotropy = 8.; t.repeat_x = t.repeat_y = False; _AT[mode] = t
    return _AT[mode]


_SV = '''#version 430
in vec2 q;in vec3 pos;in vec4 a;in vec4 col;in vec2 b;
uniform vec3 ro;uniform mat3 CamR;uniform float fl;uniform vec2 res;
out vec2 vuv;out vec4 vc;out float vz;out float vq;flat out float lit;
void main(){vec3 c=CamR*(pos-ro);float k=cos(a.z),s=sin(a.z);vec2 l=q*a.xy;l=vec2(k*l.x-s*l.y,s*l.x+k*l.y);c.xy+=l;vz=c.z;vc=col;lit=b.y;vq=q.y*.5+.5;
 float v=mod(a.w,8.);float f=b.x<0.?-1.:1.;vec2 t=vec2(f*q.x*.5+.5,q.y*.5+.5)*.992+.004;float cx=mod(v,2.),cy=floor(v/2.);vuv=vec2((t.x+cx)*.5,1.-((1.-t.y)+cy)*.25);
 gl_Position=c.z<.05?vec4(2,2,2,1):vec4(c.x*fl*res.y/res.x,c.y*fl,0,c.z);}
'''
_SF = '''#include "noise.glsl"
in vec2 vuv;in vec4 vc;in float vz;in float vq;flat in float lit;out vec4 o;
uniform sampler2D tA,tZ;uniform vec3 cLit,cMid,cSh,cInk,cRim,fogCol;uniform float fogD,fogS,soft,nearF,inkK;
void main(){vec4 t=texture(tA,vuv);if(t.a<.004) discard;vec3 k=t.rgb/max(t.a,.01);float tone=clamp(k.r*.86+.18*(vq-.5)+.10*(lit-.5),0.,1.);
 vec3 c=mix(cSh,cMid,smoothstep(.30,.62,tone));c=mix(c,cLit,smoothstep(.60,.92,tone));c+=cRim*k.b*lit;c=mix(c,cInk,clamp(k.g,0.,1.)*inkK);c*=vc.rgb;
 float f=1.-exp(-max(0.,vz-fogS)*fogD);c=mix(c,fogCol,f);float z=texelFetch(tZ,ivec2(gl_FragCoord.xy),0).x;float al=t.a*vc.a*clamp((z-vz)/soft,0.,1.)*smoothstep(nearF*.35,nearF,vz);o=vec4(c*al,al);}
'''
_Q = None


def sprites(st, P, w, h=None, var=0, rot=0., flip=1., alpha=1., tint=(1, 1, 1), lit=1., puff=False, cLit='#fff4d2', cMid='#ffcf92', cSh='#c87a62', cInk='#6a2a24', cRim=(.5, .36, .16), fogCol=GOLD_FOG, fog=0., fogS=200., soft=6., near=4., ink=.8):
    """after close(): mural clouds (or dust puffs) at world points, sorted, depth-tested.  w = half width in world units; var 0..7"""
    global _Q
    P = np.atleast_2d(np.asarray(P, float)); n = len(P)
    if n == 0: return
    tex = _atlas(1 if puff else 0); c = gl.ctx(); p = gl.program(_SF, vs=_SV)
    if _Q is None: _Q = c.buffer(np.array([-1, -1, 1, -1, -1, 1, 1, 1], 'f4').tobytes())
    D = np.zeros((n, 13), 'f4'); D[:, :3] = P; D[:, 3] = w; D[:, 4] = np.broadcast_to(w, (n,)) * CH / CW if h is None else h; D[:, 5] = rot; D[:, 6] = var; D[:, 7:10] = tint; D[:, 10] = alpha; D[:, 11] = flip; D[:, 12] = lit
    D = D[np.argsort(-((P - st.cam.eye) @ st.cam.R[2]))]; vb = c.buffer(D.tobytes()); vao = c.vertex_array(p, [(_Q, '2f', 'q'), (vb, '3f 4f 4f 2f/i', 'pos', 'a', 'col', 'b')]); st.C.use(); c.viewport = (0, 0, st.pw, st.ph)
    gl.set_uniforms(p, {**st.base_u(), 'cLit': hexc(cLit), 'cMid': hexc(cMid), 'cSh': hexc(cSh), 'cInk': hexc(cInk), 'cRim': hexc(cRim), 'fogCol': hexc(fogCol), 'fogD': float(fog), 'fogS': float(fogS), 'soft': float(soft), 'nearF': float(near), 'inkK': float(ink)}); gl.bind(p, dict(tA=tex, tZ=st.L.color_attachments[1]))
    c.enable(mgl.BLEND); c.blend_func = (mgl.ONE, mgl.ONE_MINUS_SRC_ALPHA); vao.render(mgl.TRIANGLE_STRIP, vertices=4, instances=n); c.disable(mgl.BLEND); vao.release(); vb.release()


DUST = dict(cLit='#fbdcae', cMid='#dfa878', cSh='#9c6250', cInk='#5a2c22', cRim=(.35, .22, .08))


def dust(st, at, t, n=34, R=30., speed=60., size=9., life=1.3, seed=0, rise=10., flat=.22, squash=1., spread=6.283, yaw=0., alpha=.95, **k):
    """a ring of mural dust thrown out from a point at t=0 (seconds)"""
    if t < 0 or t > life * 1.2: return
    r = np.random.default_rng(seed); a = yaw + r.uniform(-.5, .5, n) * spread; d = np.c_[np.sin(a), r.uniform(0, 1, n) * flat * 3, np.cos(a)]; sp = speed * r.uniform(.45, 1.1, n); lf = life * r.uniform(.6, 1.15, n); g = (1 - np.exp(-2.6 * t)) / 2.6
    P = np.asarray(at, float) + np.c_[np.sin(a), 0 * a, np.cos(a)] * R * r.uniform(.6, 1.1, n)[:, None] + d * (sp * g)[:, None] + V(0, 1, 0) * rise * t * r.uniform(.3, 1.2, n)[:, None]; u = np.clip(t / lf, 0, 1); s = size * r.uniform(.6, 1.3, n) * (.35 + .95 * (1 - (1 - u) ** 3)) * (1 - .55 * u ** 2); al = np.clip((1 - u) * 2.2, 0, 1) * alpha
    sprites(st, P, s * CW / CH, s, var=r.integers(0, 8, n), rot=r.uniform(-.4, .4, n) + t * r.uniform(-.8, .8, n), flip=r.choice([-1, 1], n), alpha=al, puff=True, **{**DUST, **k})


# ------------------------------------------------------------------ rocks: a handful of shapes, any number of them in one mesh
def _ico(sub):
    g = (1 + 5 ** .5) / 2; v = np.array([(-1, g, 0), (1, g, 0), (-1, -g, 0), (1, -g, 0), (0, -1, g), (0, 1, g), (0, -1, -g), (0, 1, -g), (g, 0, -1), (g, 0, 1), (-g, 0, -1), (-g, 0, 1)], float); f = np.array([(0, 11, 5), (0, 5, 1), (0, 1, 7), (0, 7, 10), (0, 10, 11), (1, 5, 9), (5, 11, 4), (11, 10, 2), (10, 7, 6), (7, 1, 8), (3, 9, 4), (3, 4, 2), (3, 2, 6), (3, 6, 8), (3, 8, 9), (4, 9, 5), (2, 4, 11), (6, 2, 10), (8, 6, 7), (9, 8, 1)]); v /= np.linalg.norm(v, axis=1, keepdims=True)
    for _ in range(sub):
        v = list(map(tuple, v)); m = {}; nf = []
        def mid(a, b):
            k = (min(a, b), max(a, b))
            if k not in m: p = np.array(v[a]) + np.array(v[b]); v.append(tuple(p / np.linalg.norm(p))); m[k] = len(v) - 1
            return m[k]
        for a, b, c_ in f: x, y, z = mid(a, b), mid(b, c_), mid(c_, a); nf += [(a, x, z), (b, y, x), (c_, z, y), (x, y, z)]
        v, f = np.array(v), np.array(nf)
    return v, f


def rock_shapes(n=6, sub=2, seed=5, flat=(1., .62, .8), cuts=7, top=None):
    """faceted boulders: sphere cut by random planes"""
    r = np.random.default_rng(seed); out = []
    for k in range(n):
        v, f = _ico(sub); p = v.copy()
        for _ in range(cuts):
            d = r.normal(size=3); d /= np.linalg.norm(d); h = r.uniform(.60, .86); e = p @ d; p = p - np.outer(np.maximum(e - h, 0), d)
        if top is not None: p[:, 1] = np.minimum(p[:, 1], top)
        p = p * (np.array(flat) * r.uniform(.85, 1.15, 3)); P = p[f].reshape(-1, 3); a = np.cross(P[1::3] - P[::3], P[2::3] - P[::3]); a /= np.linalg.norm(a, axis=1, keepdims=True) + 1e-9
        nv = np.zeros_like(p); np.add.at(nv, f.ravel(), np.repeat(a, 3, 0)); nv /= np.linalg.norm(nv, axis=1, keepdims=True) + 1e-9
        out.append((p, nv, f))
    return out


def rotmats(a, b, c):
    """N rotations about y, x, z"""
    ca, sa, cb, sb, cc, sc = np.cos(a), np.sin(a), np.cos(b), np.sin(b), np.cos(c), np.sin(c); o, l = np.zeros_like(a), np.ones_like(a)
    Ry = np.stack([ca, o, sa, o, l, o, -sa, o, ca], 1).reshape(-1, 3, 3); Rx = np.stack([l, o, o, o, cb, -sb, o, sb, cb], 1).reshape(-1, 3, 3); Rz = np.stack([cc, -sc, o, sc, cc, o, o, o, l], 1).reshape(-1, 3, 3); return Ry @ Rx @ Rz


ROCK = '''#include "noise.glsl"
in vec3 vp,vn_;in vec2 vuv;
layout(location=0) out vec4 g0;layout(location=1) out vec4 g1;layout(location=2) out vec4 g2;layout(location=3) out vec4 g3;
uniform vec3 ro;uniform mat3 CamR;uniform float far,objId,inkw,wetY,haze;uniform vec3 cA,cB,cC;uniform sampler2D tName;uniform float name_;uniform vec2 nbox;
void main(){vec3 n=normalize(vn_),v=vp-ro;vec3 fn=normalize(cross(dFdx(vp),dFdy(vp)));if(dot(fn,v)>0.) fn=-fn;vec3 f=transpose(CamR)[2];float vz=dot(v,f);gl_FragDepth=clamp(vz/far,0.,1.);
 float id=floor(vuv.x/8.),glw=floor(vuv.y/8.)/32.;vec2 l=vec2(vuv.x-id*8.-4.,vuv.y-floor(vuv.y/8.)*8.-4.);float h=h11(id+3.);
 float m=fbm(l*1.7+h*31.),m2=vn(l*6.+h*9.);vec3 b=cA*(.80+.34*m)*(.90+.22*h),s=cB*(.85+.3*m);b=mix(b,cC,smoothstep(.55,.72,fbm(l*.9+h*17.))*.45);float ck=smoothstep(.025,.0,abs(fbm(l*.8+h*5.)-.5));b=mix(b,s,ck*.6);
 float wet=smoothstep(.9,-.2,vp.y-wetY-.5*m2)*step(-1e3,wetY);b*=1.-.42*wet;float cls=1.;vec3 nn=normalize(mix(fn,n,.35));
 if(name_>.5&&n.y>.30){vec2 u=l/nbox*.5+.5;if(u.x>0.&&u.x<1.&&u.y>0.&&u.y<1.){float px=length(fwidth(u));float a=texture(tName,u).a;a*=smoothstep(.30,.55,n.y);b=mix(b,vec3(.60,.018,.012),a);s=mix(s,vec3(.20,.010,.02),a);if(glw>.02&&a>.06){float g=a*min(glw,1.);if(g>.22) cls=4.;b=mix(b,vec3(1.7,.50,.07)*(.7+.9*glw),g);}}}
 g0=vec4(nn,vz);g1=vec4(b,cls+clamp(inkw,0.,.98)*.98);g2=vec4(s,1);g3=vec4(nn,objId*64.+mod(id,60.)+1.);}
'''
_SH = {}


def rocks(st, pos, size, R, shape=None, glow=0., sub=2, col=('#c9a27c', '#6a4058', '#8a5a48'), name=None, wetY=-1e4, ink=.85, flat=(1., .62, .8), ids=None, cuts=7, top=None, box=(.70, .46)):
    """N boulders in one draw: pos Nx3, size N (or Nx3), R Nx3x3.  name = texture of the painted name laid on their tops; glow 0..1"""
    pos = np.atleast_2d(pos); n = len(pos)
    if n == 0: return
    key = (sub, flat, cuts, top)
    if key not in _SH: _SH[key] = rock_shapes(6, sub, 5, flat, cuts, top)
    sh = _SH[key]; shape = (np.arange(n) * 7) % 6 if shape is None else np.asarray(shape); size = np.asarray(size, float); size = np.broadcast_to(size[:, None] if size.ndim == 1 else size, (n, 3)); glow = np.broadcast_to(glow, (n,)); ids = np.arange(n) if ids is None else np.asarray(ids); A, B, C, I, o = [], [], [], [], 0
    for k in range(6):
        m = np.nonzero(shape % 6 == k)[0]
        if not len(m): continue
        p, nv, f = sh[k]; q = p[None] * size[m][:, None]; w = np.einsum('nij,nvj->nvi', R[m], q) + pos[m][:, None]; nn = np.einsum('nij,vj->nvi', R[m], nv); uu = np.empty((len(m), len(p), 2)); uu[..., 0] = ((ids[m] % 3000) * 8 + 4)[:, None] + np.clip(p[:, 0], -3, 3); uu[..., 1] = (np.floor(np.clip(glow[m], 0, 1.5) * 32) * 8 + 4)[:, None] - np.clip(p[:, 2], -3, 3)
        A.append(w.reshape(-1, 3)); B.append(nn.reshape(-1, 3)); C.append(uu.reshape(-1, 2)); I.append((f[None] + (np.arange(len(m)) * len(p))[:, None, None] + o).reshape(-1, 3)); o += len(m) * len(p)
    st.mesh(np.vstack(A), np.vstack(B), np.vstack(C), np.vstack(I), col=col, ink=ink, frag=ROCK, texs=dict(tName=name if name is not None else st._white), u=dict(name_=1. if name is not None else 0., wetY=float(wetY), haze=0., nbox=tuple(box)))


# ------------------------------------------------------------------ the giant
def giant(st, pose, at=(0, 0, 0), yaw=0., scale=1., face=None, t=None, tail='up', vel=(0, 0, 0), wind=(.35, .05, .1), tail_ground='auto', ring='R', fig=None, pitch=0., roll=0., M=None, tlen=13., path=None, slow=1., cloth=True, draw=True, gem=None, sashlen=4.6):
    """Hanuman with tail, sash and Rama's ring; slow = how slowly cloth and tail move (big things move slowly)"""
    t = st.t if t is None else t; S = st.fig(fig or HM.HANUMAN, pose, at=at, yaw=yaw, pitch=pitch, roll=roll, scale=scale, M=M, face=face, draw=draw); P = None
    if cloth and draw: P = HM.tail(st, S, t * slow, tail, length=tlen, vel=vel, path=path, ground=tail_ground); HM.sash(st, S, t * slow, length=sashlen, wind=wind, vel=vel)
    g = None
    if ring and draw: g = ring_on(st, S, ring, gem)
    return S, P, g


def ring_on(st, S, side='R', toward=None, finger=3, size=.20, draw=True):
    """Rama's ring on a finger; toward = world point the gem looks at (default: away from the palm).  returns the gem's world point"""
    F = S.u['HF'][(0 if side == 'L' else 20) + finger * 4:][:2, :3]; a, b = S.w(F[0]), S.w(F[1]); o = a * .42 + b * .58; z = nz(b - a); y = -S.hand(side, (0, 0, 1)) if toward is None else np.asarray(toward, float) - o; y = nz(y - z * (y @ z)); sc = size * S.Sc
    if draw: st.fig(PR.RING, M=PR.place(o, y, z, sc))
    return o + y * sc * 1.5


def tree_cards(st, kind, P, axis, height, season='spring', var=0, tint=(1, 1, 1), spin=None):
    """whole trees in any attitude: foot at P, trunk along axis (N,3), turned to face the lens"""
    pl = FL.plate_of(kind, season, var); P = np.atleast_2d(np.asarray(P, float)); a = np.asarray(axis, float); a = a / np.linalg.norm(a, axis=1, keepdims=True); n = len(P)
    if n == 0: return
    k = np.broadcast_to(height, (n,)) / (abs(pl.ay - pl.top) * pl.h); w, h = pl.w * k, pl.h * k; x = np.cross(a, st.cam.eye - P); x /= np.linalg.norm(x, axis=1, keepdims=True) + 1e-9; nn = np.cross(x, a); uv = np.array([(0, 0), (1, 0), (0, 1), (1, 1.)]); pos = P[:, None] + x[:, None] * ((uv[None, :, 0] - pl.ax) * w[:, None])[..., None] + a[:, None] * ((uv[None, :, 1] - (1 - pl.ay)) * h[:, None])[..., None]
    idx = (np.array([(0, 1, 2), (1, 3, 2)])[None] + (np.arange(n) * 4)[:, None, None]).reshape(-1, 3); st.mesh(pos.reshape(-1, 3), np.repeat(nn, 4, 0), np.tile(uv, (n, 1)), idx, kind=3, col=(tint, '#8a7a9a', '#ffffff'), cls=6, ink=0., texs=dict(tCard=pl.tex), u=dict(cutoff=.45))


def smear(st, dx, dy):
    """a whip blur without the beads of one long pass"""
    from lau import impact as IM
    IM.whip(st, dx, dy); IM.whip(st, dx / 20, dy / 20)


# ------------------------------------------------------------------ the open sea, near and far
OCEAN = '''
#define SEA_IT 4
#define TMAX 8000.
#define STEPS 84
#define RELAX .82
#define NOAO
#define PLANES
#define BOUND
#include "sea.glsl"
uniform vec2 off,sunAz,wkD;uniform float amp,fr,spd,near_,glit,unfog;uniform vec4 wake,churn,shade,brg;uniform float lvl;uniform vec3 cDeep,cMid,cLite,cFoam,cFar,cSun,sunD;uniform float seaW;
float H(vec2 p){float r=length(p-ro.xz);float k=smoothstep(near_,near_*.35,r);float h=k<=0.?0.:k*seaH(p+off,fT*spd,amp,fr);if(churn.w>0.){float q=length(p-churn.xy);h+=churn.w*amp*2.2*exp(-pow((q-churn.z)/(churn.z*.22+2.),2.))*(.6+.6*vn(p*.14+fT));}if(brg.w>0.){float dz=max(brg.y-p.y,p.y-brg.z);float b=max(abs(p.x)-brg.x,dz);h*=mix(1.,smoothstep(-3.,20.,b),brg.w);}return h;}
vec2 bound(vec3 o,vec3 d){float top=lvl+amp*(2.+churn.w*3.);float t0=0.,t1=near_*1.1;if(o.y>top){if(d.y>=0.) return vec2(1,0);t0=(top-o.y)/d.y;}return vec2(t0,max(t1,t0+.1));}
float planes(vec3 o,vec3 d,out float m,out vec3 n){m=9.;n=vec3(0,1,0);return d.y<0.?(lvl-o.y)/d.y:1e9;}
vec2 map(vec3 p){return vec2((p.y-lvl-H(p.xz))*.66,1.);}
void surf(vec3 p,vec3 n,int m,inout Surf s){vec3 unl=1./max(mix(uAmb,uKey,.55),vec3(.02));vec2 w=p.xz+off;float hf=.62+.5*(fbm(w*fr*.9+fT*.2)-.5);float hh=m==9?hf:mix(hf,(p.y-lvl)/max(amp,1e-3),smoothstep(near_,near_*.35,length(p.xz-ro.xz)));
 float fine=smoothstep(.5,.06,gPx*fr);vec3 c=mix(cDeep,cMid,smoothstep(.10,.80,hh+.45*(fbm(w*fr*.55)-.5)+.25*(fbm(w*.012)-.5)));float fre=pow(1.-max(0.,dot(n,-gRd)),4.);c=mix(c,cLite,smoothstep(.80,1.5,hh)*.8);c=mix(c,cLite,fre*.45);
 float lit=smoothstep(-.10,.45,dot(n,sunD));if(m!=9) c*=mix(.74,1.06,lit);
 float ph=hh*2.3+.35*vn(w*fr*2.);float ln=smoothstep(.10,.03,abs(fract(ph*1.5)-.5))*smoothstep(.25,.6,hh);c=mix(c,cDeep*.62,ln*.42*fine);
 for(int i=0;i<3;i++){float S=(i==0?5.:i==1?17.:60.)/max(fr*2.4,.2)*seaW;float lod=smoothstep(.16,.05,gPx/S)*(i==0?.5:1.);if(lod<=0.) continue;vec2 u=w/S;u.y+=.10*sin(u.x*1.7+fT*.6);u+=vec2(fT*(.10+.05*float(i)),fT*.16);float row=floor(u.y*1.6);vec2 f=vec2(fract(u.x+.5*mod(row,2.))-.5,fract(u.y*1.6));float q=h21(vec2(floor(u.x+.5*mod(row,2.)),row));float d=length(vec2(f.x*1.1,f.y-.02))-.52;float l=smoothstep(.07,.02,abs(d))+.5*smoothstep(.05,.015,abs(d+.14));c=mix(c,cDeep*.66,l*lod*(.26+.2*q));c=mix(c,cFoam,smoothstep(.07,.0,abs(d+.05))*step(.84,q)*lod*.65);}
 float fo=smoothstep(1.18,1.34,hh+.30*(fbm(w*fr*4.+fT*.2)-.5))*(m==9?0.:1.);c=mix(c,cFoam,fo*.9);
 if(shade.w>0.){vec2 q=p.xz-shade.xy;q+=2.*vec2(sin(q.y*.11+fT*2.),cos(q.x*.10+fT*1.6));float R=shade.z;float d=length(q/vec2(1.,1.15))-R;d=min(d,length(vec2(q.x-R*.22*sin((q.y+R)*.020),max(-(q.y+R*.4),0.)*0.+q.y+R*3.2)/vec2(.52,2.9))-R);float k=smoothstep(R*.16,-R*.10,d+R*.10*(fbm(w*.05+fT*.3)-.5));c=mix(c,cDeep*.22,k*shade.w);
  vec2 e=vec2(abs(q.x)-R*.46,q.y-R*.18);float ey=smoothstep(R*.16,R*.05,length(e/vec2(1.,.7)));c=mix(c,vec3(1.,.55,.10),ey*smoothstep(.75,1.,shade.w)*.85);}
 if(wake.w>0.){vec2 q=p.xz-wake.xy;float a=dot(q,wkD),b=dot(q,vec2(-wkD.y,wkD.x));if(a<1.){float L=max(-a,0.);float w0=.22+L*.055;float nz=fbm(vec2(a*.35+off.x*.0-fT*9.,b*1.3));float core=smoothstep(w0*1.25,w0*.4,abs(b)+w0*.5*(nz-.5))*exp(-L/wake.z);float arm=smoothstep(.5+L*.02,.1,abs(abs(b)-L*.19-.2))*exp(-L/(wake.z*1.3))*smoothstep(.30,.55,nz+.15);c=mix(c,cFoam,clamp(core*(.55+.6*nz)+arm*.9,0.,1.)*wake.w);}}
 if(churn.w>0.){float q=length(p.xz-churn.xy);float nz=fbm(p.xz*.10+vec2(fT*.8,-fT*.5));float k=smoothstep(churn.z*1.35,churn.z*.75,q+churn.z*.5*(nz-.5));float rg=smoothstep(.25,.05,abs(fract(q/(churn.z*.30)-fT*1.1)-.5)-.12*nz)*smoothstep(churn.z*3.2,churn.z*1.1,q);c=mix(c,cFoam,clamp(k*(.5+.8*nz)+rg*.55*smoothstep(.35,.6,nz+.1),0.,1.)*churn.w);}
 if(brg.w>0.){float dz=max(brg.y-p.z,p.z-brg.z);float b=length(max(vec2(abs(p.x)-brg.x,dz),0.))+min(max(abs(p.x)-brg.x,dz),0.);float nz=fbm(p.xz*.16+vec2(fT*.5,fT*.8));float lod=smoothstep(900.,120.,gT);float k=smoothstep(7.,1.,b+9.*(nz-.5));float rg=smoothstep(.16,.04,abs(fract(b*.085-fT*.8+.6*nz)-.5))*smoothstep(34.,4.,b)*smoothstep(.40,.56,nz)*lod;c=mix(c,cFoam,clamp(k*(.35+.9*nz)*smoothstep(-8.,0.,b)+rg*.8,0.,1.)*brg.w);c=mix(c,cDeep*.55,smoothstep(0.,-5.,b)*.8*brg.w);}
 vec2 vd=normalize(p.xz-ro.xz);float al=dot(vd,sunAz);float g0_=gPx*fr;float gl=smoothstep(.56,.68,vn(w*fr*1.7/max(1.,g0_*3.)+fT*vec2(1.5,.9))*.6+vn(w*fr*4./max(1.,g0_*5.)-fT*1.9)*.5);c+=cSun*glit*smoothstep(.72,1.,al)*(.10+.85*gl*smoothstep(.84,1.,al)*smoothstep(.55,.12,-gRd.y));c=mix(c,cFar,smoothstep(150.*unfog,2600.*unfog,gT)*.62);c=mix(c,cFar,smoothstep(1800.*unfog,9000.*unfog,gT));
 s.cls=6.;s.base=c*unl;s.sh=s.base;s.ink=.1;s.part=1.;s.ns=vec3(0,1,0);}
'''
TURQ = dict(cDeep='#0a5d78', cMid='#169aa0', cLite='#6fdcc4', cFoam='#fff8e6', cFar='#f2cf9a', cSun='#ffc878')


def ocean(st, off=(0, 0), amp=.5, fr=.35, spd=1.1, near=360., wake=None, wakeDir=(1, 0), churn=None, shade=None, sun=SUN, glit=.8, unfog=1., seaW=1., bridge=None, lvl=0., **k):
    """wake = (x, z, length, strength) foam line behind a point that moves along wakeDir; churn = (x, z, radius, strength) boiling water; shade = (x, z, radius, strength) a dark shape below"""
    u = dict(off=tuple(map(float, off)), amp=float(amp), fr=float(fr), spd=float(spd), near_=float(near), glit=float(glit), unfog=float(unfog), seaW=float(seaW), wkD=tuple(map(float, wakeDir)), sunAz=tuple(nz(V(sun[0], sun[2]))), sunD=tuple(nz(sun)))
    u['lvl'] = float(lvl)
    for n, v in (('wake', wake), ('churn', churn), ('shade', shade), ('brg', bridge)): u[n] = tuple(map(float, v)) if v is not None else (0., 0., 1., 0.)
    place.draw(st, OCEAN, u={**u, **{a: hexc(v) for a, v in {**TURQ, **k}.items()}}, sun=0.)
