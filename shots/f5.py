"""f5 (120): Hanuman with the herb mountain on his palm.  He crosses an enormous moon, black then rim-lit (f0-40); the camera swings up and over him, sleeping India below (f40-80); the horizon ahead goes rose, then gold, and he drops toward the camp, herbs blazing (f80-120)."""
from lau.shot import *
from lau.look import *
from lau.stage import hexc
from worlds import lanka as LK, flora as FL
from chars import hanuman as HM, deer as DE

PEAKS = [(-2., -4., 33., 22., 1.25), (-15., 5., 19., 13., 1.2), (12., -9., 23., 14., 1.2), (3., 12., 10., 10., 1.1)]
LEDGE = (15., 11., 5.5)
FALLS = [2.4, 3.3, -.50, -1.5, -2.2]                          # azimuths where water leaves the rim (0 = +z, the side we see first)
BASE = -24.5


def rim(a): return 28 + 2.6 * np.sin(3 * a + 1) + 1.6 * np.sin(7 * a)


def height(x, z):
    x, z = np.asarray(x, float), np.asarray(z, float); h = np.full(np.broadcast(x, z).shape, 3.)
    for cx, cz, H_, R, p in PEAKS: h = np.maximum(h, 3 + H_ * np.clip(1 - np.hypot(x - cx, z - cz) / R, 0, 1) ** p)
    k = np.clip((9.5 - np.hypot(x - LEDGE[0], z - LEDGE[1])) / 3.5, 0, 1); k = k * k * (3 - 2 * k); return h * (1 - k) + LEDGE[2] * k


MOUNT = '''
#define TMAX 900.
#define STEPS 150
#define RELAX .8
#define EPS .0006
uniform mat3 mR;uniform vec3 mO;uniform float mS,flow,dawn;uniform float fa[5];
float rimR(float a){return 28.+2.6*sin(3.*a+1.)+1.6*sin(7.*a);}
float top(vec2 p){float h=3.;PK
 float k=smoothstep(9.5,6.,length(p-vec2(15.,11.)));return mix(h,5.5,k);}
vec2 map(vec3 P){vec3 p=mR*(P-mO)/mS;float bb=length(p-vec3(0,6,0))-38.;if(bb>4.) return vec2(bb*mS,0.);
 float l=length(p.xz),a=atan(p.x,p.z);float R=rimR(a);
 float u=a*6.;vec4 v=voro(vec2(u*1.1,p.y*.16+.5*sin(u)));float rock=v.x*2.6+1.1*vn3(p*.55)+.5*vn3(p*1.4);
 float h=top(p.xz);float dt=(p.y-h-.9*(vn3(p*.45)-.5)-.35*(vn3(p*1.3)-.5))*.55;
 float q=clamp(l/R,0.,1.2);float yl=-25.*(1.-pow(q,.95))-2.5;float dl=(yl-p.y)*.50+1.0*(rock-2.)*smoothstep(1.,-4.,p.y)*smoothstep(-24.,-16.,p.y);
 float dr=(l-R)*.8+.45*(rock-2.);
 float d=max(max(dt,dl),dr);d=max(d,BASEY-p.y);
 return vec2(d*mS*.85,1.);}
void surf(vec3 P,vec3 n,int m,inout Surf s){vec3 p=mR*(P-mO)/mS;vec3 nl=mR*n;float l=length(p.xz),a=atan(p.x,p.z);float h=top(p.xz);
 float f=fbm3(p*.5),g=smoothstep(.42,.66,nl.y+.25*(f-.5))*smoothstep(.0,2.5,p.y);g*=smoothstep(30.,20.,p.y+8.*f);
 float st=fbm(vec2(a*14.,p.y*.35));vec3 rk=mix(hex(0x4e4660),hex(0xa08c86),smoothstep(.3,.7,st));float cr=smoothstep(.03,.0,abs(fbm3(p*.7)-.5)-.012);rk=mix(rk,hex(0x2a2238),cr*.6);
 s.base=rk;s.sh=mix(hex(0x1c1a38),hex(0x2e2848),st);
 vec3 ea=mix(hex(0x4a2c24),hex(0x9a6a48),fbm3(p*1.1));float vr=abs(sin(a*17.+3.*fbm3(p*.4)+p.y*.15));ea=mix(ea,hex(0x2a1620),smoothstep(.25,.08,vr)*.8);ea=mix(ea,hex(0xb08a60),smoothstep(.90,.97,vr)*.5);float e=smoothstep(1.5,-2.,p.y+3.*(f-.5));s.base=mix(s.base,ea,e);s.sh=mix(s.sh,mix(hex(0x1a0f18),hex(0x3a2430),fbm3(p*.8)),e);
 vec3 gr=mix(hex(0x1f4a38),hex(0x6f9a4a),fbm(p.xz*.45));s.base=mix(s.base,gr,g);s.sh=mix(s.sh,hex(0x0a1c30),g);
 float sn=smoothstep(24.,30.,p.y+6.*(f-.5))*smoothstep(.15,.5,nl.y);s.base=mix(s.base,hex(0xdfe4f0),sn);s.sh=mix(s.sh,hex(0x5a6aa8),sn);
 for(int i=0;i<5;i++){float da=a-fa[i];da-=TAU*round(da/TAU);float w=1.5+.5*sin(p.y*.8+float(i));float k=smoothstep(w,w-.35,abs(da)*l)*smoothstep(-6.,-1.,p.y)*smoothstep(16.,11.,p.y)*smoothstep(8.,12.,l);if(k>0.){float sk=fbm(vec2(da*l*3.2,p.y*.35+flow*5.));vec3 wc=mix(hex(0x5a8ad0),hex(0xf2f8ff),smoothstep(.35,.62,sk));s.base=mix(s.base,wc,k);s.sh=mix(s.sh,wc*.45,k);s.cls=k>.5?8.:s.cls;}}
 s.ink=.85;}
'''.replace('BASEY', f'({BASE:.1f})').replace('PK', ''.join(f'h=max(h,3.+{H_:.1f}*pow(max(0.,1.-length(p-vec2({cx:.1f},{cz:.1f}))/{R:.1f}),{p:.2f}));' for cx, cz, H_, R, p in PEAKS))

LAND = '''
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform vec2 res;uniform vec3 ro,hazeC,sunD,moonD,shP;uniform mat3 CamR;uniform float fl,fT,alt,scroll,dawn,cloud;
float riv(vec2 p,float k){float c=150.*sin(p.x*.0026+k*2.)+70.*sin(p.x*.0071+k)+26.*sin(p.x*.019+k*3.);return abs(p.y-c-k*900.);}
void main(){vec2 s=(uv*2.-1.)*vec2(res.x/res.y,1.);vec3 d=normalize(transpose(CamR)*vec3(s,fl));if(d.y>-.0005){o=vec4(0);return;}
 float t=(-alt-ro.y)/d.y;vec2 w=ro.xz+d.xz*t;vec2 p=w+vec2(scroll,0.);float px=t/(fl*res.y*.5)/max(-d.y,.05);
 float lod=smoothstep(26.,4.,px);float n=fbm(p*.0016),n2=fbm(p*.006+4.);
 vec4 v=voro(p/vec2(120.,84.));vec2 fd=rot(v.z*3.14)*p;float fur=smoothstep(.25,.0,abs(fract(fd.x/9.)-.5)-.18)*smoothstep(5.,1.4,px);
 vec3 fn=mix(hex(0x1a3350),hex(0x335a64),v.w);fn=mix(fn,hex(0x46604e),step(.72,v.z));vec3 fdn=mix(hex(0xd88a4a),hex(0xb8b04c),v.w);fdn=mix(fdn,hex(0x7a9a4c),step(.6,v.z));
 vec3 c=mix(fn,fdn,dawn);c*=1.-.18*fur;c=mix(c,c*.55,smoothstep(.05,.015,v.y)*lod*.8);
 float fo=smoothstep(.46,.54,n+.25*(n2-.5));float tr=smoothstep(.55,.2,voro(p/17.).x)*lod;vec3 fc=mix(mix(hex(0x07182c),hex(0x12304a),tr),mix(hex(0x2c3a26),hex(0x7a7a34),tr),dawn);c=mix(c,fc,fo);
 // hills: shaded ridges
 float hb=smoothstep(.50,.72,fbm(p*.0009+9.));float r0=ridge(p*.0035),r1=ridge((p+vec2(16.,-10.))*.0035);float sh=clamp((r0-r1)*5.+.5,0.,1.);c=mix(c,mix(mix(hex(0x0c1a38),hex(0x3a5684),sh),mix(hex(0x5a3448),hex(0xf0a060),sh),dawn),hb*.85);
 // rivers like thread
 vec3 rf=reflect(d,vec3(0,1,0));float gm=pow(max(0.,dot(rf,normalize(moonD))),3.),gs=pow(max(0.,dot(rf,normalize(sunD))),4.);float wv=.75+.5*vn(p*.05+fT);
 for(int i=0;i<3;i++){float k=float(i)-1.;float wd=(i==1?8.5:4.5)*(1.+.4*sin(p.x*.004+k));float rv=riv(p,k);float m=smoothstep(wd+px,wd-px,rv);vec3 rc=mix(hex(0x7f9ad8)*(.55+.9*gm),hex(0xffd890)*(.6+1.1*gs),dawn)*wv;c=mix(c,mix(hex(0x0a1830),hex(0x6a4a3a),dawn),smoothstep(wd*1.9+px,wd+px,rv)*.5);c=mix(c,rc,m);
  float tb=abs(p.x-k*700.-430.-90.*sin(p.y*.006+k)-34.*sin(p.y*.021));tb=mod(p.x+2000.*0.,1e9)<0.?tb:tb;float m2=smoothstep(2.5+px,2.5-px,tb)*step(0.,p.y-(150.*sin(p.x*.0026))-0.);c=mix(c,rc*.9,m2*.8);}
 // his shadow crossing the fields
 vec2 q=(w-shP.xy)/shP.z;float a=atan(q.x,q.y);float sd=length(q)-(28.+2.6*sin(3.*a+1.)+1.6*sin(7.*a));sd=min(sd,length(vec2(q.x-2.,q.y-clamp(q.y,-44.,-26.)))-2.4);vec2 b=rot(.5)*(q-vec2(-2.,-47.));sd=min(sd,length(vec2(b.x-clamp(b.x,-12.,7.),b.y))-4.2);sd=min(sd,length(q-vec2(8.,-43.))-3.6);sd=min(sd,length(vec2(q.x-clamp(q.x,-40.,-12.),q.y+52.+3.*sin(q.x*.2+fT*6.)))-1.4);c*=1.-.78*smoothstep(3.,-2.,sd)*(1.-.6*dawn);
 float light=.85+.2*n2;c*=light;
 // thin cloud between him and the land
 if(cloud>0.){float tc=(-alt*.45-ro.y)/d.y;if(tc>0.){vec2 cp=ro.xz+d.xz*tc+vec2(scroll,0.);float cn=fbm(cp*vec2(.0022,.0045))+.35*(fbm(cp*vec2(.010,.018))-.5);float cm=smoothstep(.56,.66,cn)*cloud;float ce=smoothstep(.56,.80,cn);vec3 cc=mix(mix(hex(0x2a3c78),hex(0x9fb0e0),ce),mix(hex(0xc86a7a),hex(0xffe0a8),ce),dawn);c=mix(c,cc,cm*.85);}}
 float fg=1.-exp(-max(0.,t-300.)*.00024);c=mix(c,hazeC,fg);c*=.95+.10*fbm(uv*vec2(60.,34.));o=vec4(c,1);}
'''


def mixd(a, b, k):
    v = lambda x: np.array(hexc(x) if isinstance(x, str) else x, float)
    return {n: (1 - k) * v(a[n]) + k * v(b[n]) for n in a}


NSKY = dict(cZen='#040720', cMid='#101c52', cHor='#2c4690', cLow='#101a4a', sunCol='#ffd890', sunGlow=0., rays=0., halo=0., sunR=.001, cov=.45, cy0=.012, cy1=.13, cLit='#aab8e8', cCM='#5466ac', cSh='#222d66', cInk='#0a0e2c', starAmt=1.)
RSKY = dict(cZen='#2c3f86', cMid='#c8688a', cHor='#ffb070', cLow='#e88a6a', sunCol='#ffd890', sunGlow=.7, rays=.5, halo=.5, sunR=.045, cov=.5, cy0=.012, cy1=.16, cLit='#ffd8b0', cCM='#e88a80', cSh='#8a5084', cInk='#3a1a3c', starAmt=.25)
GSKY = dict(cZen='#5a78b0', cMid='#f0a070', cHor='#ffcf92', cLow='#f2ac68', sunCol='#fff0b8', sunGlow=1.1, rays=.8, halo=1., sunR=.06, cov=.5, cy0=.012, cy1=.18, cLit='#fff0c8', cCM='#f5b080', cSh='#b87a80', cInk='#5a2a3a', starAmt=0.)
NL = dict(keyCol=(.30, .34, .62), amb=(.10, .12, .30), rimCol=(.9, 1.05, 1.5), bounceCol=(.04, .06, .10), envT='#8fa4ff', envM='#5868b8', envB='#182048', fogCol=hexc('#2c4690'))
RL = dict(keyCol=(1.0, .62, .46), amb=(.26, .19, .34), rimCol=(1.3, .75, .5), bounceCol=(.10, .06, .08), envT='#e8a0b0', envM='#ff9a6a', envB='#4a305a', fogCol=hexc('#e08a7a'))
GL = dict(keyCol=(1.25, .92, .58), amb=(.40, .30, .36), rimCol=(1.4, 1.0, .5), bounceCol=(.20, .12, .06), envT='#ffe8c0', envM='#ffc060', envB='#a8683a', fogCol=hexc('#ffd090'))
SPEED = 620.


class Shot(ShotBase):
    id = 'f5'; n = 120
    EVENTS = [(0, 'great flight, wind', dict(dur=120)), (2, 'waterfalls in the air', dict(dur=60)), (12, 'conch far off', {}), (40, 'camera whoosh over', dict(dur=20)), (52, 'night land below, crickets', dict(dur=28)), (66, 'temple bell below', {}), (80, 'first birds', dict(dur=40)), (88, 'dawn swell', dict(dur=32)), (109, 'dive', dict(dur=11)), (112, 'herbs blaze', {})]

    def setup(self, st):
        r = np.random.default_rng(8)

        def on(n, lo=0., hi=26.5, ymax=30, seed=0):
            q = np.random.default_rng(seed); a, l = q.uniform(0, 6.283, n * 4), hi * np.sqrt(q.uniform((lo / hi) ** 2, 1, n * 4)); x, z = np.sin(a) * l, np.cos(a) * l; y = height(x, z); m = (y < ymax) & (l < rim(a) - 1.6); return np.c_[x, y, z][m][:n]
        led = lambda P, d: P[np.hypot(P[:, 0] - LEDGE[0], P[:, 2] - LEDGE[1]) > d]
        self.trees = {k: led(on(n, lo, 27, ym, s), 6.5) for k, n, lo, ym, s in (('deodar', 60, 4, 22, 1), ('pahari_round', 26, 12, 9, 2), ('shrub', 46, 12, 9, 3), ('mango', 12, 14, 7, 5))}
        H = np.vstack([on(330, 0, 27.6, 34, 11), np.array([[LEDGE[0] + 5 * math.sin(k * 2.4) * (k / 14) ** .5, LEDGE[2], LEDGE[1] + 5 * math.cos(k * 2.4) * (k / 14) ** .5] for k in range(14)])]); a = r.uniform(0, 6.283, 90); R = rim(a) + .2
        self.herbs = np.vstack([H + [0, .7, 0], np.c_[np.sin(a) * R, r.uniform(-3, 3.4, 90), np.cos(a) * R]]); n = len(self.herbs); self.hp = r.uniform(0, 6.28, n); self.hs = r.uniform(.5, 1.25, n)
        self.hc = np.where(r.uniform(0, 1, (n, 1)) < .72, np.array([hexc('#b8ff7a')]), np.where(r.uniform(0, 1, (n, 1)) < .6, np.array([hexc('#7affd8')]), np.array([hexc('#ffe08a')])))
        self.roots = [(a, l, L) for a, l, L in zip(r.uniform(0, 6.283, 34), r.uniform(8, 24, 34), r.uniform(6, 17, 34))]
        # village lamps: clusters on a strip of land that repeats
        C = np.c_[r.uniform(0, 5200, 120), r.normal(0, 900, 120)]; self.lamps = np.vstack([c + r.normal(size=(int(k), 2)) * [26, 18] for c, k in zip(C, r.integers(6, 26, 120))]); self.lp = r.uniform(0, 6.28, len(self.lamps))

    # ------------------------------------------------------------------ what time of night
    def dawn(self, f): return smooth(72, 96, f), smooth(92, 112, f)

    def flight(self, f):
        """his place in the moving frame: a long swell, then the dive"""
        t = f / 24.; dv = ease_in((f - 109) / 11., 1.6) if f > 109 else 0.; up = -3.0 * smooth(102, 109, f) * (1 - smooth(109, 114, f))
        return V(16 * dv, 1.5 * math.sin(t * 2.1) - 36 * dv - up, 6 * math.sin(t * .9) + 14 * dv), dv

    def solved(self, f):
        g = on2(f); t = g / 24.; at, dv = self.flight(g); P = HM.H_CARRY.set(lf=(1.1, 4.6 + .3 * math.sin(t * 3), -1.6), hedr=(4 + 22 * smooth(92, 102, g), -20 + 14 * dv, 12)); return dict(pose=P, at=at, yaw=90, pitch=8 + 3 * math.sin(t * 2.1 + 1) + 26 * dv, roll=2 * math.sin(t * 1.3))

    def frame(self, f, st):
        st.clear('#000', f=f); t = st.t; kr, kg = self.dawn(f); sky = mixd(mixd(NSKY, RSKY, kr), GSKY, kg); Ld = mixd(mixd(NL, RL, kr), GL, kg)
        at, dv = self.flight(f); F = V(1, 24, 0)
        # ---- camera: across, over, behind, round to the front
        az = keys(f, [(0, 4.), (34, -4., 'linear'), (58, -62., 'io'), (84, -78., 'io'), (104, 30., 'io'), (112, 36.), (120, 40.)]); el = keys(f, [(0, -15.), (34, -13.5), (58, 46., 'io'), (70, 41.), (90, 11., 'io'), (104, -4., 'io'), (112, 4.), (120, 20., 'in')])
        dist = keys(f, [(0, 132.), (34, 104.), (58, 100., 'io'), (84, 90., 'io'), (104, 60., 'io'), (112, 57.), (120, 92., 'in')]); fov = keys(f, [(0, 30.), (34, 31.), (60, 40., 'io'), (90, 38.), (120, 36.)])
        off = keys(f, [(0, 36.), (30, 5., 'linear'), (40, 0.), (120, 0.)]); a, e = math.radians(az), math.radians(el); d = V(math.sin(a) * math.cos(e), math.sin(e), math.cos(a) * math.cos(e))
        tgt = F + V(off, 0, 0) + V(at[0] * .6, 0, at[2] * .6 * (f > 109)) + V(0, keys(f, [(0, 6.), (40, 2.), (60, 8.), (84, 8., 'io'), (104, -8., 'io'), (109, -8.), (115, -24., 'linear'), (120, -42., 'linear')]), 0); cam = Cam(tgt + d * dist, tgt, fov, roll=keys(f, [(0, 0.), (34, 2.), (58, -14., 'io'), (84, 4., 'io'), (104, 6., 'io'), (120, -3.)])); st.cam = cam
        sd = nz(V(1, .045 + .07 * kg, .10)); md = nz(V(.02, .25, -1)); ms = 1 - smooth(78, 100, f); scroll = SPEED * (t - .6 * max(0., t - 104 / 24.))
        st.paint('sky.frag', **SKY(None, **{k: (tuple(v) if np.ndim(v) else float(v)) for k, v in sky.items()}, sunDir=tuple(sd), cdrift=.05, cseed=5.))
        if ms > 0: LK.moon(st, R=.35, dir=tuple(md), amt=float(ms), glow=.8 * ms)
        hz = np.array(sky['cHor']) * .85
        st.paint(LAND, 'over', hazeC=tuple(hz), sunD=tuple(sd), moonD=tuple(md), shP=(290., 105., 1.45), alt=420., scroll=float(scroll), dawn=float(.45 * kr + .55 * kg), cloud=.9)
        # ---- village lamps far down
        P = self.lamps - [scroll, 0]; P = np.c_[(P[:, 0] + 2600) % 5200 - 2600, np.full(len(P), -419.), P[:, 1]]; z = (P - cam.eye) @ cam.R[2]; m = z > 60; dm = (1 - .8 * kr) * (1 - kg)
        if m.any() and dm > .02: FX.particles(st, P[m], np.maximum(4.4, 3.4 / (cam.fl * 540 / z[m])), np.array(hexc('#ffa84a')) * 1.7, 'lamp', seed=self.lp[m], alpha=dm * np.clip(1.5 - z[m] / 2600, 0, 1) * (.75 + .25 * np.sin(t * 5 + self.lp[m])))
        if f >= 96:                                                     # the camp: fires on the plain
            r = np.random.default_rng(21); Q = np.c_[r.normal(0, 150, 60), np.full(60, -418.), r.normal(0, 90, 60)] + V(-470 + SPEED * .4 * (120 - f) / 24., 0, -350); FX.particles(st, Q, r.uniform(5, 9, 60), np.array(hexc('#ff8a34')) * 1.5, 'lamp', alpha=.9 * smooth(96, 104, f))
            for q in Q[:9]: u = np.linspace(0, 1, 14); FX.ribbon(st, q + np.c_[-34 * u ** 1.6 + 4 * np.sin(u * 6 + t * 2), 60 * u, 0 * u], np.linspace(1., 8., 14), 'smoke', '#c8909a', '#8a5a70', amt=.35)
        # ---- light: black against the moon, then its rim, then the sun from ahead
        lift = smooth(10, 34, f); sil = .18 + .82 * lift; key = nz(lerp(V(-.15, .75, .45), V(.95, .30, .30), kr)); Lk = {k: tuple(np.array(v)) for k, v in Ld.items()}
        for n in ('keyCol', 'amb', 'bounceCol', 'envM', 'envB', 'envT'): Lk[n] = tuple(np.array(Lk[n]) * lerp(sil, 1., kr))
        Lk['rimCol'] = tuple(np.array(Lk['rimCol']) * (.35 + .75 * lift)); blaze = 1 + .9 * smooth(106, 116, f)
        s = self.solved(f); S = st.fig(HM.HANUMAN, s['pose'], draw=False, **{k: s[k] for k in ('at', 'yaw', 'pitch', 'roll')}); palm = S.palm('L', 0, .62, .30)
        tl = t - .12; Mr = eul(0, 0, 0) @ eul(90, 4 * math.sin(tl * 2.1) + 10 * dv, -5 - 3 * math.sin(tl * 1.6) - 10 * dv) @ eul(-90, 0, 0); mS = .64; mO = palm - Mr @ V(0, BASE + .3, 0) * mS; w = lambda q: mO + (np.atleast_2d(q) * mS) @ Mr.T
        glow = np.array([.55, .95, .40]); pts = [(w(V(x, y, z))[0], 8., tuple(glow * k * lerp(.50, .18, kg) * blaze)) for x, y, z, k in ((-12, 14, 14, .9), (14, 12, 16, 1.), (2, 26, 8, .7), (-20, 8, -6, .7), (16, 14, -14, .8))]
        pts.append((palm + V(0, 7, 6), 8., tuple(glow * .35 * lift * (1 - kg))))
        L = Light(key=tuple(key), rim=tuple(nz(lerp(V(.1, .75, -.5), V(.8, .45, -.3), kr))), shadow=True, pts=pts, ink=2.8, inkRef=1.3, inkCol=(.006, .004, .014), fog=(.0010 * kr, 140, 0, 0), **Lk)
        st.open(cam, L, far=6000.)
        st.world(MOUNT, u=dict(mR=Mr.T, mO=tuple(mO), mS=mS, flow=t, dawn=kg, fa=np.array(FALLS, 'f4')), shadow=False)
        for kind, Q in self.trees.items():
            hgt = dict(deodar=5.0, pahari_round=4.4, shrub=1.8, mango=4.4)[kind]; FL.scatter(st, kind, w(Q - [0, .5, 0]), height=hgt, season='summer', seed=3, tint=tuple(lerp(np.array([.62, .80, 1.25]) * (.55 + .5 * lift), np.array([1.15, 1.05, .9]) * (1 - kg) + np.array([1.75, 1.35, .8]) * kg, kr)), inkw=.3)
        for (x, z, yw, ps, sc) in ((15, 13.2, 150, DE.graze(.5 + .5 * math.sin(t * 1.3)), .27), (18.2, 9.4, 60, DE.ALERT if 84 < f < 110 else DE.look(1, .6), .28), (11.6, 11.4, 210, DE.graze(1.), .23), (15.2, 8.0, 100, DE.STAND, .18)): DE.draw(st, ps, at=w(V(x, LEDGE[2] + .15, z))[0], yaw=yw, scale=sc, shadow=False)
        for k, (ra, rl, RL_) in enumerate(self.roots):                 # roots torn out of the ground, trailing behind
            q = min(1., rl / rim(ra)); p0 = V(math.sin(ra) * rl, -25 * (1 - q ** .95) - 1.2, math.cos(ra) * rl); Q = CL.lag(lambda tt: w(p0)[0], t, n=12, length=RL_ * .42, wind=(-.55, 0, .05 * math.sin(k)), grav=.85, wave=.9, freq=.9, phase=k * 1.7); st.mesh(*CL.tube(Q, np.linspace(.40, .04, 12) * (.6 + .5 * (k % 3) / 2), m=7, n=26), kind=0, col=('#7a4e34', '#24141c', '#7a4e34'), cls=1, ink=.8)
        st.fig(HM.HANUMAN, s['pose'], face=Face(lid=.9, frown=.25, smile=.25, gx=.1, gy=lerp(.05, -.3, smooth(96, 106, f)), spark=.8 * smooth(86, 96, f)), **{k: s[k] for k in ('at', 'yaw', 'pitch', 'roll')})
        HM.tail(st, S, t, 'fly', vel=(60, 0, 0), ground=None, length=15); HM.sash(st, S, t, vel=(70, 4, 0), length=6.5)
        Q = CL.lag(lambda q: S.chest((0, 1.2, -1.3)), t, n=18, length=11., wind=(-1.1, .12, .1), grav=.05, wave=1.0, freq=1.5); st.mesh(*CL.strip(Q, np.linspace(1.0, 2.4, 18), up=(0, .35, 1), m=7, curl=.14, n=44), kind=1, col=('#c4222c', '#660f22', '#f2b23a'), cls=8); st.close()
        self.effects(f, st, t, cam, w, kr, kg, lift, blaze)
        return st.finish(bloom=.5, thr=.85, vig=.45, contrast=1.06, satu=1.04, flash=.0)

    def effects(self, f, st, t, cam, w, kr, kg, lift, blaze):
        # falls that leave the rim and blow back into spray
        wc = (np.array(hexc('#cfe0ff')) * (1 - kg) + np.array(hexc('#ffe6c0')) * kg) * (.35 + .65 * lift)
        for k, fa in enumerate(FALLS):
            R = rim(fa) + .4; p0 = w(V(math.sin(fa) * R, 1.0, math.cos(fa) * R))[0]; tg = V(math.cos(fa), 0, -math.sin(fa)); u = np.linspace(0, 1, 24)
            for b in range(7):
                q = np.random.default_rng(k * 10 + b); o = (b - 3) * .28; ln = q.uniform(.6, 1.1); Q = p0 + tg * o + np.c_[(-17 * u ** 1.7 - 2.5 * u * q.uniform(-1, 1)) * ln, -20 * u ** 1.35 * ln, .5 * np.sin(u * 7 - t * 6 + k + b)] + tg * (o * 2.2 * u)[:, None]; FX.ribbon(st, Q, np.linspace(.16, .34, 24) * (1 + .5 * (b % 2)), 'wind' if b % 2 else 'light', tuple(wc * .8), tuple(wc), seed=k * 3.3 + b, amt=.50)
            q = np.random.default_rng(k + 50); n = 60; lf = (t * q.uniform(.8, 1.3, n) + q.uniform(0, 1, n)) % 1.; FX.particles(st, p0 + np.c_[-20 * lf ** 1.6 + q.normal(size=n) * 2.2 * lf, -22 * lf ** 1.3 + q.normal(size=n) * 1.4 * lf, q.normal(size=n) * 1.6 * lf], .10 + .22 * lf, tuple(wc), 'ember', alpha=.55 * (1 - lf))
        # herbs: hundreds of small lamps, each leaving a thread of light
        H = w(self.herbs); tw = .8 + .2 * np.sin(t * 4 + self.hp); FX.particles(st, H, .62 * self.hs * tw * blaze ** .7, self.hc * 1.15, 'lamp', seed=self.hp, alpha=np.clip(tw, 0, 1)); FX.particles(st, H[::7], 1.2 * self.hs[::7] * blaze, self.hc[::7], 'glint', alpha=.55 * tw[::7])
        for i in range(0, len(H), 13):
            u = np.linspace(0, 1, 16); Q = H[i] + np.c_[-u * (18 + 7 * math.sin(i)), 1.4 * np.sin(u * 6 - t * 7 + i) * u + 1.5 * u, 1.2 * np.cos(u * 5 - t * 6 + i) * u]; FX.ribbon(st, Q, np.linspace(.20, .03, 16), 'light', tuple(self.hc[i]), '#f4ffe0', amt=.40 * blaze)
        # motes shed from the herbs
        r = np.random.default_rng(4); n = 170; j = r.integers(0, len(H), n); lf = (t * r.uniform(.5, 1.1, n) + r.uniform(0, 1, n)) % 1.; P = H[j] + np.c_[-70 * lf, -6 * lf + 3 * np.sin(lf * 6 + j), 3 * np.cos(lf * 5 + j)]; FX.particles(st, P, .38 * (1 - lf), self.hc[j], 'ember', alpha=(1 - lf) ** .8)
        # earth and pebbles falling from the torn base
        n = 110; lf = (t * r.uniform(.7, 1.2, n) + r.uniform(0, 1, n)) % 1.; a = r.uniform(0, 6.283, n); l = r.uniform(2, 24, n); q = np.clip(l / 28, 0, 1); p0 = w(np.c_[np.sin(a) * l, -25 * (1 - q ** .95) - 3, np.cos(a) * l]); P = p0 + np.c_[-26 * lf, -38 * lf ** 1.8, np.zeros(n)]; c = np.array([.10, .07, .07]) * (.5 + lift) + np.array([.35, .20, .10]) * kg; FX.particles(st, P, r.uniform(.08, .36, n), c, 'ash', seed=r.uniform(0, 1, n), alpha=np.minimum(1, (1 - lf) * 3), rot=t * 5 + a)
        # wind: streaks of cloud torn past
        for k in range(16):
            q = np.random.default_rng(90 + k); ph = (t * q.uniform(.75, 1.25) + q.uniform()) % 1.; x = 190 - 420 * ph; y, z = q.uniform(-34, 66), q.choice([-1, 1]) * q.uniform(22, 75); y = y if z < 0 else q.uniform(-34, -2); L = q.uniform(40, 90); u = np.linspace(0, 1, 14); Q = np.c_[x + L * u, y + 1.5 * np.sin(u * 3 + k), np.full(14, z)]; col = np.array(hexc('#b8c8f4')) * (1 - kr) + np.array(hexc('#ffe0b8')) * kr; FX.ribbon(st, Q, q.uniform(.5, 1.8), 'wind', tuple(col), seed=k, amt=.30 * math.sin(ph * 3.14))
