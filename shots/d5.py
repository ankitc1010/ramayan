"""d5 (84): hush.  Lanka under an enormous moon over a still sea (f0-40); a small shape crosses the moon (f24) and drops; f48 it lands on a parapet and lifts its head (f60-70).  Far below, a dark grove and one faint figure (f70-84)."""
from lau.shot import *
from lau.look import *
from lau.stage import hexc
from worlds import lanka as LK, place
from chars import hanuman as HM, sita

CLOUDS = '''
#include "sky.glsl"
in vec2 uv;out vec4 o;uniform vec2 res;uniform mat3 CamR;uniform float fl,fT,amt,drift;
// thin mural clouds: long tapering bands with a scalloped upper edge and the painter's contour lines
float band(vec2 q,float L,float th,float seed){float x=q.x/L;float k=1.-x*x;if(k<=0.) return 1.;float s=.013;float u=q.x/s;float id=floor(u);float d=1.;
 for(int i=-1;i<=1;i++){float h=h21(vec2(id+float(i),seed));float cx=(id+float(i)+.5+.4*(h-.5))*s;float kk=1.-pow(cx/L,2.);if(kk<=0.) continue;float r=s*(.55+.45*h)*(.35+.65*kk);float cy=th*kk*(.35+.65*vn(vec2(cx*26.,seed)))-r*.6;d=min(d,length((q-vec2(cx,cy))*vec2(.8,1.))-r);}
 float body=max(q.y-th*k*(.2+.5*vn(vec2(q.x*26.,seed))),-q.y-.0035*k);d=smin2(d,body,.006);return max(d,-q.y-.0035*k-.0015*sin(q.x*90.+seed));}
void main(){vec2 s=(uv*2.-1.)*vec2(res.x/res.y,1.);vec3 d=normalize(transpose(CamR)*vec3(s,fl));vec2 p=skyUV(d);vec3 c=vec3(0);float a=0.;
 for(int i=0;i<7;i++){float f=float(i);vec2 h=h22(vec2(f,5.));float y=.085+.062*f+.02*h.x;float sp=(.6+.9*h.y);float x=mod(h.x*1.9+drift*sp+f*.53,1.9)-.95;float L=.12+.17*h.y;vec2 q=p-vec2(x,y);float e=band(q,L,.010+.016*h.x,f*3.1);
  float aa=.0012;float k=smoothstep(aa,-aa,e);float u=-e;vec3 m=mix(hex(0x26347a),hex(0x7f92d6),smoothstep(-.004,.028,q.y));m=mix(m,hex(0xe8e4e0),smoothstep(.007,.001,u)*.75);float ln=smoothstep(.0012,.0004,abs(u-.0055))*.6+smoothstep(.0011,.0004,abs(u-.010))*.45+smoothstep(.0010,.0003,abs(u-.015))*.3;m=mix(m,hex(0x10164a),ln);m=mix(m,hex(0x0c1038),smoothstep(.0018,.0006,u)*.7);k*=.92;c=c*(1.-k)+m*k;a=a*(1.-k)+k;}
 o=vec4(c,a)*amt;}
'''

PARA = '''
#include "orn.glsl"
#define TMAX 160.
#define STEPS 110
#define RELAX .8
uniform mat3 wR;uniform vec3 wO;uniform float lampK;
float merlon(vec2 q,float h){q.x=abs(q.x);float w=1.18;float b=max(q.x-w,q.y-h*.45);vec2 c=vec2(-.55,h*.45);float r=length((q-c)*vec2(1.,.82))-1.73;b=min(b,max(r,h*.45-q.y));float notch=length(q-vec2(1.28,h*.36))-.26;return max(max(b,-notch),-q.y-2.);}
float makara(vec3 p){ // a sea beast with a curled trunk, jaws open; +z out of the wall, 1 unit = its head
 vec3 a=vec3(abs(p.x),p.yz);float d=sCone(p,vec3(0,-.5,-3.2),vec3(0,.1,.3),1.5,1.15);d=max(d,-1.75-p.z);d=smin(d,sEll(p-vec3(0,.45,.7),vec3(1.05,.95,1.5)),.5);
 d=smin(d,sCone(p,vec3(0,.55,1.6),vec3(0,.75,3.3),.72,.52),.4);d=smin(d,sCone(p,vec3(0,.75,3.3),vec3(0,1.6,4.2),.50,.40),.25);d=smin(d,sCone(p,vec3(0,1.6,4.2),vec3(0,2.5,3.9),.40,.30),.2);d=smin(d,sCone(p,vec3(0,2.5,3.9),vec3(0,2.6,3.2),.30,.22),.2);d=smin(d,sCone(p,vec3(0,2.6,3.2),vec3(0,2.1,3.2),.22,.16),.15);
 float jaw=sCone(p,vec3(0,-.55,.4),vec3(0,-1.35,2.7),.70,.30);jaw=smin(jaw,sCone(p,vec3(0,-1.35,2.7),vec3(0,-1.05,3.2),.30,.18),.2);d=smin(d,jaw,.25);
 d=max(d,-sEll(p-vec3(0,-.28,2.3),vec3(.55,.52,1.5)));
 d=min(d,sCone(a,vec3(.42,.35,2.9),vec3(.5,-.55,3.0),.15,.02));d=min(d,sCone(a,vec3(.30,-1.1,2.5),vec3(.34,-.4,2.6),.12,.02));for(int i=0;i<3;i++){float f=float(i);d=min(d,sCone(a,vec3(.50,.25,1.3+.5*f),vec3(.52,-.20,1.3+.5*f),.12,.03));}
 d=smin(d,sEll(a-vec3(.72,.95,.9),vec3(.42,.36,.5)),.12);d=min(d,length(a-vec3(.92,.98,1.08))-.30);
 d=smin(d,sCone(a,vec3(.55,1.2,.1),vec3(.95,2.4,-.9),.30,.08),.15);d=smin(d,sCone(a,vec3(.95,2.4,-.9),vec3(1.0,2.5,-1.8),.10,.03),.1);
 for(int i=0;i<3;i++){float f=float(i);d=smin(d,sEll(a-vec3(1.12-.05*f,.15-.45*f,-.35-.45*f),vec3(.16,.42,.75)),.1);}
 d=min(d,sTor(p.xzy-vec3(0,-1.6,0).xyz,1.45,.18));
 return d*.85;}
vec2 map(vec3 P){vec3 p=wR*(P-wO);vec2 m=vec2(1e3,0.);
 float ty=p.y;vec3 w=p;float per=3.3;                                              // the wall: top at y 0, outside is -z
 float wall=max(abs(p.z)-1.5,p.y);wall=min(wall,sBox(p-vec3(0,-.55,0),vec3(1e3,.38,1.9),.12));wall=min(wall,sBox(p-vec3(0,-5.2,0),vec3(1e3,.45,1.85),.12));
 float u=p.x-per*round(p.x/per);float ml=max(merlon(vec2(u,p.y),3.6),abs(p.z)-.62);float mi=max(merlon(vec2(u*1.22,(p.y-.2)*1.22),3.6),abs(p.z)-.80);ml=min(ml,mi);ml=max(ml,5.1-length(p.xz));ml=max(ml,3.4-abs(p.x+16.2));
 // the bastion he lands on
 float l=length(p.xz),an=atan(p.x,p.z);float b=max(l-5.0,p.y-3.4);b=min(b,max(l-5.5-.16*abs(sin(an*12.)),abs(p.y-2.9)-.42));b=min(b,max(l-5.35,abs(p.y-1.75)-.22));b=min(b,max(l-5.3,abs(p.y+.9)-.35));
 m=U(vec2(min(wall,b),1.),vec2(ml*.8,2.));
 float bead=length(vec2(length(vec2(l-5.15,p.y-2.25))-.0,(fract(an*24./TAU)-.5)*TAU/24.*5.15))-.24;m=U(m,vec2(bead,2.));
 ml=0.;{vec3 g=(p-vec3(-16.2,2.7,1.0))/1.55;g.xz=rot(-.35)*g.xz;float gb=length(g-vec3(0,.4,.4))-4.9;if(gb<.6) m=U(m,vec2(makara(g)*1.55,3.));else m=U(m,vec2(gb*1.55,0.));m=U(m,vec2(sBox(p-vec3(-16.2,.3,0),vec3(2.6,.6,2.),.15),1.));}
 {vec3 g=(p-vec3(23.2,-1.4,1.3))/1.3;float gb=length(g-vec3(0,.4,.4))-4.9;if(gb<.6) m=U(m,vec2(makara(g)*1.3,3.));else m=U(m,vec2(gb*1.3,0.));}
 if(m.y<.5) m.x=max(m.x,.2);
 return m;}
void surf(vec3 P,vec3 n,int mi,inout Surf s){vec3 p=wR*(P-wO);vec3 nl=wR*n;oAA=.012;
 s.cls=2.;s.base=vec3(1.,.93,.82);s.sh=vec3(.4,.3,.25);s.ink=.85;
 if(mi==1){s.cls=1.;s.base=hex(0x4a3560);s.sh=hex(0x1a1238);float l=length(p.xz);float an=atan(p.x,p.z);vec2 q=l<5.6?vec2(an*5.2,p.y):vec2(p.x,p.y);
   float row=floor(p.y/1.35);float jx=abs(fract(q.x/2.6+.5*mod(row,2.))-.5)*2.6,jy=abs(fract(p.y/1.35)-.5)*1.35;float bev=step(.62,jy)+step(1.27,jx);s.base=mix(s.base,hex(0x2c1f4a),clamp(bev,0.,1.)*.8*step(abs(nl.y),.5));
   if(abs(nl.y)<.5&&p.y<-1.1&&p.y>-4.6&&l>5.6){float o=oLotus(vec2(q.x*.55,(p.y+4.4)/3.1));s.base=mix(s.base,hex(0xd8a23c),o);s.sh=mix(s.sh,hex(0x6a3a1c),o);if(o>.6) s.cls=2.,s.base=vec3(.9,.8,.7);}
   if(p.y>-1.||p.y<-4.7&&p.y>-5.7){s.cls=2.;s.base=vec3(.95,.86,.74);if(nl.y>.6){s.ink=.2;s.cls=1.;s.base=hex(0x8a6a4a);s.sh=hex(0x2c1c34);}}
   if(l<5.6&&p.y>1.&&abs(nl.y)<.7){s.cls=2.;s.base=vec3(1.,.92,.8);}
   if(nl.y>.6&&l<5.2){s.cls=1.;float o=oLotusM(p.xz/4.4);s.base=mix(hex(0x55406a),hex(0xd8a94a),o*.8);s.sh=hex(0x1c143a);s.ink=.25;}
   if(nl.y>.6&&l>5.2){s.ink=.4;}}
 if(mi==2){float u=p.x-3.3*round(p.x/3.3);vec2 q=vec2(u,p.y);float e=merlon(q*1.5-vec2(0,.35),3.6);if(abs(nl.z)>.7&&length(p.xz)>5.3){float f=oEll(q-vec2(0,1.35),vec2(.22,.30));float lo=oPet(q-vec2(0,.35),.62,2.0);float l2=oPet(q-vec2(0,.35),.40,1.5);s.base*=1.-.6*clamp(oL(lo,.05)+oL(l2,.035),0.,1.);if(f<0.){s.cls=3.;s.base=hex(0xc4142c);s.sh=hex(0x4a0616);}else if(f<.07) s.base*=.4;}}
 if(nl.z<-.08&&mi<3){s.ink=.22;s.cls=1.;s.base=mix(hex(0x5a4a7a),hex(0xb88a50),mi==2?.6:.0);s.sh=hex(0x241c44);}
 if(mi==3){vec3 g=p.x<0.?(p-vec3(-16.2,2.7,1.0))/1.55:(p-vec3(23.2,-1.4,1.3))/1.3;if(p.x<0.) g.xz=rot(-.35)*g.xz;vec3 a=vec3(abs(g.x),g.yz);if(length(a-vec3(.92,.98,1.08))<.31){s.cls=3.;s.base=hex(0xd82030);s.sh=hex(0x500818);}
   else{float sc=oScale(vec2(atan(g.x,g.y)*2.4,g.z*1.7));s.base*=1.-.55*sc*smoothstep(.7,.1,g.z);float w=abs(fract(g.z*2.2+.5*g.y)-.5);s.base*=1.-.45*smoothstep(.10,.04,w)*step(1.3,g.z)*step(.4,g.y);}
   float mo=max(abs(g.x)-.60,max(abs(g.y+.30+.10*(g.z-1.))-.50,1.-g.z));if(mo<0.){s.cls=1.;s.base=hex(0x8a2030);s.sh=hex(0x300818);}}
}
'''
CUT = '''
#define map mapL
#include "lanka.glsl"
#undef map
vec2 map(vec3 p){vec2 m=mapL(p);float c=p.z+712.;if(c>m.x) m=vec2(c,c>.5?0.:m.y);return m;}
'''
GROVE = '''
#define map mapL
#define surf surfLk
#include "lanka.glsl"
#undef map
#undef surf
#define M_LEAF 60
#define M_LAWN 61
#define M_WALLG 62
uniform vec3 gO,cO;uniform float gR;
#define M_ARC 63
float canopy(vec3 p){float d=1e3;vec2 id0=round(p.xz/26.);for(int j=-1;j<=1;j++)for(int i=-1;i<=1;i++){vec2 id=id0+vec2(i,j);vec2 c=id*26.+(h22(id)-.5)*13.;float lc=length(c);if(lc>gR-13.||lc<36.) continue;float h=h21(id+3.);float H=20.+9.*h;vec3 q=p-vec3(c.x,0.,c.y);float r=9.5+4.*h;d=min(d,sEll(q-vec3(0,H,0),vec3(r,r*.78,r)));d=min(d,sCap(q,vec3(0),vec3(0,H,0),1.1));}
 float b=1.5*vn3(p*.30)+.5*vn3(p*.8);return (d-1.8*b+.6)*.7;}
vec2 map(vec3 p){vec2 m=mapL(p);vec3 q=p-gO;float l=length(q.xz);vec3 kq=abs(p-cO)-vec3(190.,300.,62.);float cut=min(max(l-gR,-q.y-40.),max(kq.x,max(kq.y,kq.z)));m.x=max(m.x,-cut);if(m.x<=-cut+1e-4&&m.x>.01&&cut<0.) m.y=0.;
 float g=max(l-gR-3.,abs(q.y+60.)-60.);float w=max(abs(l-gR)-3.,abs(q.y-50.)-64.);w=min(w,max(abs(l-gR)-4.6,abs(q.y-112.)-3.));w=min(w,max(abs(l-gR+2.)-4.,abs(q.y-38.)-2.));vec2 r=vec2(g,M_LAWN);r=U(r,vec2(w,M_WALLG));
 float top=max(l-gR-6.,q.y-46.);if(top<4.){r=U(r,vec2(max(canopy(q),-q.y-1.),M_LEAF));}else r=U(r,vec2(top+1.,0.));
 return U(m,r);}
void surf(vec3 p,vec3 n,int m,inout Surf s){vec3 q=p-gO;float l=length(q.xz);
 if(m==M_LAWN){s.cls=1.;s.base=mix(hex(0x1d3a44),hex(0x2c5050),fbm(q.xz*.12));s.sh=hex(0x0b1630);s.ink=.15;float a=atan(q.x,q.z);float path=smoothstep(1.,.0,abs(l-30.)-3.)+smoothstep(1.,.0,abs(abs(q.x)-0.)-2.6)*step(30.,l);s.base=mix(s.base,hex(0x7a80a8),clamp(path,0.,1.)*.55);float gl=exp(-l*l/260.);s.base+=hex(0x8fb0e8)*gl*.5;}
 else if(m==M_WALLG){float a=atan(q.x,q.z)*gR;oAA=max(gPx,.05);s.cls=2.;s.base=vec3(.72,.62,.52);s.ink=.6;if(n.y<.6){for(int k=0;k<2;k++){vec2 w=vec2(mod(a,22.)-11.,q.y-(k==0?3.:46.));float ar=oArch(w,6.4,k==0?14.:30.,5.);if(ar<0.){s.cls=4.;s.base=mix(hex(0x1c0c1e),hex(0xd07420),smoothstep(-.5,-6.,ar)*(k==0?.35:.8));s.ink=.2;}else if(ar<1.2) s.base*=.45;}}}
 else if(m==M_LEAF){s.cls=1.;float v=fbm3(p*.35);s.base=mix(hex(0x10303c),hex(0x3a7a6a),smoothstep(.35,.62,v));s.sh=mix(hex(0x040a1c),hex(0x0a1c34),v);float f=smoothstep(.80,.84,vn3(p*.75+3.));s.base=mix(s.base,hex(0xc83430),f);s.sh=mix(s.sh,hex(0x4a0c1c),f);s.ink=.20;}
 else surfLk(p,n,m,s);}
'''


class Shot(ShotBase):
    id = 'd5'; n = 84
    EVENTS = [(0, 'still sea at night', dict(dur=84)), (2, 'temple bell far off', {}), (24, 'wind of flight, small', dict(dur=12)), (44, 'air rush', dict(dur=4)), (48, 'soft landing on gold', {}), (54, 'tail settles', {}), (62, 'eyes lift', {}), (70, 'look down', {}), (74, 'leaves far below', dict(dur=10))]

    O = V(-50, 396, -690)                              # the parapet, high on the north side of the middle peak: the city falls away toward the moon

    def frame(self, f, st):
        st.clear('#000', f=f); t = st.t
        if f < 42: return self.wide(f, st, t)
        if f < 70: return self.perch(f, st, t)
        return self.down(f, st, t)

    def sky(self, st, t, drift=0., md=(.02, .235, -1.), R=.30, clouds=1., **k):
        st.paint('sky.frag', **LK.sky('moon', **{**dict(cZen='#03051a', cMid='#0b123e', cHor='#22357c'), **k})); LK.moon(st, R=R, dir=md, glow=.62, cG='#5f78cc')
        if clouds: st.paint(CLOUDS, 'over', amt=float(clouds), drift=float(drift))

    def wide(self, f, st, t):
        u = ease_io(f / 41., 1.6); cam = Cam(lerp(V(-420, 46, 3900), V(-330, 150, 3120), u), lerp(V(60, 470, 0), V(40, 500, 0), u), 33); st.cam = cam
        self.sky(st, t, .10 + .020 * t, cov=.34)
        st.open(cam, LK.light('moon'), far=20000.); LK.draw(st, 'moon'); st.close(); LK.lamps(st, minpx=1.25)
        if 23 <= f < 41:
            # a small shape crosses the disc, hangs, and drops behind the towers
            q = on2(f) if f < 33 else f; a = (q - 23) / 24.
            x = keys(q, [(23, -.30), (31, .02, 'out'), (34, .075), (40, .10)]); y = keys(q, [(23, .30), (30, .345, 'out'), (33, .335), (40, .10, 'in')])
            d = nz(cam.R[2] * 0 + V(x + .02, y, -1.)); at = cam.eye + d * 700.; drop = smooth(32, 36, f)
            L = Light(key=(0, .4, 1), keyCol=(.05, .06, .13), amb=(.03, .035, .09), rim=(0, .3, -1), rimCol=(.5, .6, .9), shadow=False, ink=2.2, inkRef=4., envT='#202a60', envM='#1a2050', envB='#0a0e28', stip=0.)
            st.open(cam, L); P = HM.H_FLY_L.mix(HM.H_LAND, drop); S = st.fig(HM.HANUMAN, P, at=at - V(0, 8, 0) * 1.5, yaw=84 - 30 * drop, pitch=0, scale=1.5); HM.tail(st, S, t, 'fly', vel=(60, 0, 0), ground=None); HM.sash(st, S, t, vel=(60, 10, 0)); st.close()
        return st.finish(bloom=.42, thr=.82, vig=.45, contrast=1.06, fade=0 * f)

    def city(self, st, src, **u):
        w = LK.MOOD['moon']['w']; place.draw(st, src, u=dict(night=1., fire=0., fireAt=(0., 300., 1100.), doors=0., skyA=hexc(w[0]), skyB=hexc(w[1]), skyC=w[2], **u), texs=dict(tLanka=LK.tex()), sun=0.)

    def lamps(self, st, keep=lambda P: P[:, 2] < -712, minpx=1.6, gain=.9):
        P = LK.lamp_points(); P = P[keep(P)]; z = (P - st.cam.eye) @ st.cam.R[2]; P, z = P[z > 4], z[z > 4]; px = st.cam.fl * 540 / z; ph = np.random.default_rng(2).uniform(0, 6.28, len(P))
        FX.particles(st, P, np.maximum(3.2, minpx * 2.2 / px), np.array(hexc('#ff9a3a')) * 1.4 * gain, 'lamp', seed=ph, alpha=.8 + .2 * np.sin(st.t * 7 + ph))

    @staticmethod
    def height(f): return keys(f, [(42, 27.), (43, 22.5, 'linear'), (48, 0., 'linear')])

    def hero(self, f):
        """pose, height above the bastion and face at frame f"""
        g = on2(f)
        fall = HM.H_LAND.set(pel=(0, 6.2, -.4), pelr=(-8, 16, 0), cher=(-10, 8, 0), lf=(1.6, 2.6, .6), rf=(-1.4, 3.0, -1.6), lft=(20, 40), rft=(-12, 60), rh=(-3.2, 9.0, 2.6), lh=(5.6, 10.4, -.4), rhand='open', rfing=(-.3, -.6, .7))
        squash = HM.H_LAND.set(pel=(0, 3.0, -.7), cher=(-12, 32, 0), hedr=(8, 4, 0)); bow = HM.H_PERCH.set(hedr=(6, -2, 0), cher=(10, 22, 0)); up = HM.H_PERCH.set(hedr=(14, -24, 0), cher=(14, 10, 0)); look = HM.H_PERCH.set(hedr=(8, 4, 0), cher=(12, 20, 0))
        P = keys(g, [(46, fall), (48, squash, 'in'), (52, HM.H_LAND.set(hedr=(8, -4, 0)), 'out'), (58, bow, 'io'), (60, bow.set(hedr=(6, 1, 0))), (66, up, 'out'), (68, up.set(hedr=(14, -20, 0))), (70, look, 'io')])
        y = self.height(f)
        face = Face(lid=keys(f, [(58, .30), (62, .35), (66, 1.0, 'out')]), spark=.0 + .9 * smooth(62, 68, f), glow=.0, smile=.2, frown=.15, gy=keys(f, [(62, -.4), (66, .15, 'out')]))
        return P, y, face

    def perch(self, f, st, t):
        O = self.O; u = ease_io((f - 42) / 27., 1.4); v = smooth(56, 70, f); top = O + V(0, 3.4, 0); h = top + V(.3, 7.4, 1.)
        eye = O + lerp(lerp(V(-15.0, 8.6, 41.0), V(-12.5, 8.1, 36.5), u), V(-5.2, 9.4, 21.5), v); cam = Cam(eye, lerp(O + V(-1.4, 8.5, 0), h + V(.1, -.1, 0), v), lerp(38, 31, v), roll=-1.5)
        dx, dy = shake(f, .5 * decay((f - 48) / 24., 8), .9, 3) if f >= 48 else (0., 0.); cam = Cam(eye, cam.at + cam.R[0] * dx + cam.R[1] * dy, cam.fov, roll=-1.5); st.cam = cam
        S = st.fig(HM.HANUMAN, self.hero(68)[0], at=top + V(0, 0, .4), yaw=-40, draw=False); md = nz(S.head((0, .6, 0)) - eye)
        self.sky(st, t, .34 + .02 * t, md=tuple(md), R=.275, cov=.30)
        st.open(cam, LK.light('moon', inkRef=5., fog=(.00055, 300., .0010, 0.)), far=20000.); self.city(st, CUT); st.close(); self.lamps(st)
        wr = eul(24, 0, 0).T
        fk = 1 + .06 * noise1(t * 6, 2); gl_ = (.34 * fk, .16 * fk, .045 * fk)
        L = Light(key=(-.2, -.25, .95), keyCol=(.20, .15, .19), amb=(.10, .11, .26), rim=(.45, .85, -.35), rimCol=(1.25, 1.4, 1.9), bounceCol=(.22, .09, .02), envT='#6a80d8', envM='#c8904e', envB='#8a4a1c', pts=[(O + V(-6, -2.5, 9), 7., gl_), (O + V(7, -3., 8), 7., gl_), (h + V(-1.6, -1.6, 3.4), 2.4, tuple(np.array([.55, .28, .09]) * fk * smooth(60, 67, f)))], ink=3.2, inkRef=1., inkCol='#06040f')
        P, y, face = self.hero(f)
        st.open(cam, L); st.world(PARA, u=dict(wR=wr, wO=tuple(O), lampK=1.))
        S = st.fig(HM.HANUMAN, P, at=top + V(0, y, .4), yaw=-40, face=face)
        vy = 0 if f >= 48 else -110.; path = (lambda q: V(0, self.height(q * 24), 0))
        HM.tail(st, S, t, 'calm', path=path, ground=float(top[1])); HM.sash(st, S, t, wind=(.25, 0, .1), vel=(0, vy, 0)); st.close()
        if f >= 48: FX.burst(st, 46, top + V(0, .2, .6), (f - 48) / 24., speed=7.5, grav=2.5, size=.15, seed=3, col='#ffcf7a', kind='flake', life=.9, spread=(1, .15, 1), up=.25, drag=2.6); FX.burst(st, 16, top + V(0, .3, .6), (f - 48) / 24., speed=6., grav=.2, size=.75, seed=5, col='#58609a', kind='smoke', life=.8, spread=(1, .05, 1), drag=3.)
        FX.embers(st, 26, (tuple(O + V(-18, -8, 2)), tuple(O + V(18, -4, 12))), t, rise=2.2, size=.05, seed=8, life=4., col='#ffb860')
        IM.dof(st, float((h - cam.eye) @ cam.R[2]), 16, 7.)
        return st.finish(bloom=.45, thr=.85, vig=.5, contrast=1.08)

    def down(self, f, st, t):
        O = self.O; u = ease_io((f - 70) / 13., 1.5); top = O + V(0, 3.4, 0); G = O + V(28, -136, 108)
        eye = O + lerp(V(-7.5, 33, -9.5), V(-5.5, 29, -5.5), u); cam = Cam(eye, lerp(O + V(1.5, -8, 12), O + V(4.5, -20, 21), u), 46, roll=-8); st.cam = cam
        st.paint('sky.frag', **LK.sky('moon', cov=.0))
        st.open(cam, LK.light('moon', inkRef=3., key=(-.25, .75, -.5), keyCol='#6f84d8', amb='#262e66', rimCol=(.2, .25, .5), bounceCol=(.05, .03, .02), fog=(.0011, 120., .0, 0.), fogCol='#141f52', pts=[(G + V(0, 9, 4), 13., (.22, .30, .52))]), far=20000.); self.city(st, GROVE, gO=tuple(G), cO=tuple(O), gR=112.)
        st.fig(sita.GROVE, sita.S_SIT, at=G + V(0, .3, 0), yaw=165, face=Face(lid=.4), scale=1.5); st.close()
        self.lamps(st, lambda P: np.hypot(P[:, 0] - G[0], P[:, 2] - G[2]) > 116, minpx=1.4, gain=.8)
        FX.drift(st, 40, (tuple(G + V(-60, 4, -60)), tuple(G + V(60, 60, 60))), t, kind='petal', size=.8, col='#e8503a', fall=3., sway=2., seed=3); FX.particles(st, (G + V(0, 6, 0))[None], 16., '#7f9ae0', 'ember', alpha=.30)
        P = HM.H_PERCH.set(cher=(10, 26, 0), hedr=keys(on2(f), [(70, (-4, 6, 0)), (78, (-14, 24, 0), 'io'), (84, (-14, 25, 0))]))
        L = Light(key=(-.4, .8, -.5), keyCol='#8f9ee0', amb=(.10, .11, .26), rim=(-.75, .5, -.4), rimCol=(.75, .85, 1.25), bounceCol=(.14, .06, .02), envT='#8a9cf0', envM='#c8904e', envB='#8a4a1c', pts=[(O + V(2, -2., 9), 7., (.30, .14, .04))], ink=3.2, inkCol='#06040f')
        st.open(cam, L); st.world(PARA, u=dict(wR=eul(24, 0, 0).T, wO=tuple(O), lampK=1.)); S = st.fig(HM.HANUMAN, P, at=top + V(0, 0, .4), yaw=-40 + 48, face=Face()); HM.tail(st, S, t, 'calm', ground=float(top[1])); HM.sash(st, S, t, wind=(.25, 0, .1)); st.close()
        IM.dof(st, 30., 60, 3.)
        return st.finish(bloom=.45, thr=.85, vig=.6, contrast=1.08, satu=1.0)
