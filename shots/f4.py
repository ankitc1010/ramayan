"""f4 (96): violet night.  The camp looks up; a face of shadow swells in the cloud (f10) and Indrajit stands rim-lit in it with the serpent bow (f18-28); a serpent of lightning strikes Lakshmana (f30).
Then no sound and almost no colour: he falls, Rama turns and catches him (f36-60); Rama holds him; the lamp behind them gutters to a blue bead (f60-96)."""
from pathlib import Path
from lau.shot import *
from lau.look import *
from chars import rama, rakshasa as RK, vanara as VN

CLOUD = '''
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform vec2 res,fc;uniform float fT,face,flash,hor,zoom,fs,front,grey;
// a storm cloud as a mural painter lays it: overlapping discs like scales, each with contour lines, lit from the upper left
vec4 scales(vec2 p,float seed,float ymax){vec2 n=floor(p);float best=-1e3;vec4 r=vec4(0,0,0,0);for(int j=-2;j<=2;j++)for(int i=-2;i<=2;i++){vec2 g=n+vec2(i,j);vec2 h=h22(g+seed);vec2 c=g+.15+.7*h;if(c.y>ymax) continue;float R=.62+.42*h21(g+seed+5.);vec2 d=(p-c)/R;float an=atan(d.y,d.x);float l=length(d)*(1.+.055*sin(an*7.+h.x*30.)+.04*sin(an*13.+h.y*30.));if(l<1.){float pr=-c.y+.6*h.x;if(pr>best){best=pr;r=vec4(d,l,h21(g+seed+9.));}}}return r;}
float puf(vec2 p){return .5+.5*(vn(p*1.2)-.5)+.3*(vn(p*2.6)-.5);}
float el(vec2 p,vec2 r){return (length(p/r)-1.)*min(r.x,r.y);}
// depth of a face pressed out of the cloud (0 outside): q in face units, height about 2
float faceM(vec2 q,out float eye){vec2 a=vec2(abs(q.x),q.y);float head=smoothstep(.12,-.30,el(q-vec2(0,-.02),vec2(.80,1.06)));float s=0.;
 s-=.95*smoothstep(.16,-.10,el((a-vec2(.34,.16))*mat2(.95,-.30,.30,.95),vec2(.27,.13)));          // sockets
 s+=.65*smoothstep(.10,-.08,el((a-vec2(.36,.38))*mat2(.95,.36,-.36,.95),vec2(.34,.08)));           // brow
 s+=.55*smoothstep(.10,-.05,el(q-vec2(0,-.05),vec2(.10,.34)));                                      // nose
 s+=.45*smoothstep(.16,-.05,el(a-vec2(.46,-.12),vec2(.20,.16)));                                    // cheek
 s-=.95*smoothstep(.10,-.06,el(q-vec2(0,-.55+.14*a.x*a.x*3.),vec2(.40,.09)));                       // mouth
 s+=.35*smoothstep(.10,-.05,el(q-vec2(0,-.84),vec2(.22,.12)));
 float e=el((a-vec2(.34,.15))*mat2(.95,-.25,.25,.95),vec2(.17,.055));eye=smoothstep(.02,-.02,e);return s*head+.20*head;}
void main(){vec2 p=vec2(uv.x*res.x,(1.-uv.y)*res.y);vec2 q=(p-vec2(960.,hor))/1080.*zoom;q.y=-q.y;
 vec3 c=mix(hex(0x4a3476),hex(0x150c34),smoothstep(-.05,.95,q.y));c=mix(c,hex(0x7a4a86),smoothstep(.22,.0,q.y)*.55);
 float dr=fT*.05;float eye;vec2 f=(p-fc)/fs;f.y=-f.y;vec2 wb=vec2(fbm(f*2.2+dr*3.),fbm(f*2.2+7.-dr*3.))-.5;f+=.09*wb;float e0;float fm=faceM(f,e0)*face;vec2 f2=f-.075*wb;faceM(f2,eye);
 vec2 w=q*vec2(1.6,2.1)+vec2(dr,-.4*dr);float n=fbm(w*1.1);vec2 sw=q*vec2(4.6,5.6)+vec2(dr*3.,0.)+.55*(vec2(fbm(w*1.6),fbm(w*1.6+9.))-.5);
 // the swelling: scales slide outward from the face
 sw-=.9*face*(q-vec2((fc.x-960.)/1080.,(hor-fc.y)/1080.)*zoom)*exp(-dot(f,f)*.8)*4.*.35;
 vec4 s1=scales(sw,3.,1e3),s2=scales(sw*2.3+4.,11.,1e3);float pf=n;
 float bank=smoothstep(.13,.19,q.y+.22*(n-.5)+.05*(1.-s1.z)-.02*s2.z);
 vec2 ld=normalize(vec2(-.5,.75));vec3 l3=normalize(vec3(-.45,.72,.42));float l1=dot(vec3(s1.xy,sqrt(max(0.,1.-dot(s1.xy,s1.xy)))),l3),l2=dot(vec3(s2.xy,sqrt(max(0.,1.-dot(s2.xy,s2.xy)))),l3);
 float tone=.02+.50*l1+.16*l2*(1.-.5*s1.z)+.55*(fbm(w*.8+3.)-.5)+.16*(s1.w-.5)+fm*.60;tone=mix(tone,tone*.8+.06,smoothstep(.2,.9,q.y));
 vec3 k=mix(hex(0x0a051c),hex(0x1c113c),smoothstep(.18,.24,tone));k=mix(k,hex(0x33245c),smoothstep(.38,.44,tone));k=mix(k,hex(0x57447f),smoothstep(.58,.64,tone));k=mix(k,hex(0x8f7cb0),smoothstep(.76,.82,tone)*.8);
 float ln=smoothstep(.045,.015,abs(s1.z-.975))*.75+smoothstep(.030,.010,abs(s1.z-.82))*.45+smoothstep(.025,.008,abs(s1.z-.66))*.28+smoothstep(.05,.02,abs(s2.z-.96))*.16;k=mix(k,hex(0x080418),clamp(ln,0.,1.)*.75*step(.01,s1.z));
 float dk=smoothstep(-.06,-.34,fm);k=mix(k,hex(0x05030e),dk*.93);
 float rr=length(p-fc)/1080.;k=k*(1.+flash*(2.6*exp(-rr*rr*3.)+.5))+hex(0x8ab4f4)*flash*exp(-rr*rr*6.)*.55*(.45+.55*smoothstep(.2,.7,tone));
 c=mix(c,k,bank);c+=hex(0x58f0b8)*eye*smoothstep(.6,1.,face)*1.2;c+=hex(0x3ac890)*exp(-pow(length((vec2(abs(f.x),f.y)-vec2(.34,.15))*vec2(1.,1.6)),2.)*26.)*smoothstep(.6,1.,face)*.35;
 if(front>.5){float h=q.y;vec2 fw=vec2(q.x*5.2+dr*5.,h*6.6);float top=.02+.10*(fbm(vec2(q.x*1.6+dr,3.))-.5);fw.y=(h-top)*6.6;vec4 a1=scales(fw,21.,-.45);float a=a1.z>0.?1.:smoothstep(.004,-.004,h-top+.16);float dp=top-h;float tn=.12+.62*dot(vec3(a1.xy,sqrt(max(0.,1.-dot(a1.xy,a1.xy)))),normalize(vec3(-.45,.8,.3)))-1.1*dp+.14*(a1.w-.5);vec3 m=mix(hex(0x080418),hex(0x1c1140),smoothstep(.14,.22,tn));m=mix(m,hex(0x382866),smoothstep(.36,.44,tn));m=mix(m,hex(0x6a58a0),smoothstep(.58,.66,tn));float l=smoothstep(.045,.015,abs(a1.z-.97))*.8+smoothstep(.03,.01,abs(a1.z-.80))*.45+smoothstep(.025,.008,abs(a1.z-.62))*.3;m=mix(m,hex(0x070316),l*.75*step(.01,a1.z));m+=hex(0x88b0ff)*flash*smoothstep(.40,.85,tn)*.35;m=mix(m,hex(0x05030e),smoothstep(.10,.45,dp)*.75);o=vec4(m*a,a);return;}
 vec3 g=vec3(lum(c))*vec3(.92,.88,1.12);c=mix(c,g,grey);o=vec4(c,1);}
'''
GROUND = '''
#define TMAX 420.
#define STEPS 90
#define NOAO
float H(vec2 p){return .9*fbm(p*.045)+.22*vn(p*.45)+.07*vn(p*1.9);}
vec2 map(vec3 p){float d=p.y-H(p.xz)+.55;float m=1.;vec3 q=p-vec3(STX,0.,STZ);
 if(length(q.xz)<9.){float s=sBox(q-vec3(0,.4,0),vec3(1.5,.8,1.3),.15);s=min(s,sCyl(q-vec3(0,2.6,0),.62-.10*smoothstep(1.,4.,q.y)+.05*abs(sin(atan(q.x,q.z)*4.)),2.2,.05));s=min(s,sCyl(q-vec3(0,2.6,0),.78,.16,.06));s=min(s,sCyl(q-vec3(0,4.55,0),1.0,.22,.08));s=min(s,sCyl(q-vec3(0,4.95,0),1.25,.16,.08));if(s<d){d=s;m=2.;}float pl=sCyl(q-vec3(3.4,9.,-1.),.17,9.5,.02);pl=min(pl,length(q-vec3(3.4,18.6,-1.))-.35);if(pl<d){d=pl;m=3.;}}
 return vec2(d*.85,m);}
void surf(vec3 p,vec3 n,int m,inout Surf s){
 if(m==1){float g=fbm(p.xz*.6);s.base=mix(hex(0x3a2c58),hex(0x5a4a72),g);s.sh=mix(hex(0x120a2a),hex(0x1c1238),g);float tuft=smoothstep(.72,.80,vn(p.xz*vec2(5.,1.6)));s.base=mix(s.base,hex(0x2a1f48),tuft*.6);s.ink=.16;}
 if(m==2){s.base=mix(hex(0x6a5c74),hex(0x8a7c8c),fbm(p.xz*2.+p.y*2.));s.sh=hex(0x241a3a);}
 if(m==3){s.cls=2.;s.base=vec3(.9,.8,.7);}}
'''
LAMP = V(7.4, 5.15, -7.0)                                       # the lamp by the standard

# the engine's lamp flame, hidden by whatever stands in front of it
FLAME = (Path(gl.__file__).parent / 'glsl/flame.frag').read_text().replace('uniform vec3 tint;', 'uniform vec3 tint;uniform sampler2D tZ;uniform float fz;').replace(' vec2 g=p-vec2(0,ht*.45);', ' float kz=step(fz,texture(tZ,uv).x+.4);body*=kz;vec2 g=p-vec2(0,ht*.45);').replace('*glow*(', '*glow*mix(.35,1.,kz)*(')


class Shot(ShotBase):
    id = 'f4'; n = 96
    EVENTS = [(0, 'night wind, distant camp', dict(dur=30)), (10, 'cloud swells, low rumble', dict(dur=18)), (18, 'thunder far', {}), (22, 'serpent bow drawn', dict(dur=6)), (28, 'hiss falling', dict(dur=2)), (30, 'lightning strikes', {}), (31, 'silence', dict(dur=65)), (46, 'bow drops, muffled', dict(soft=1)), (50, 'he is caught', dict(soft=1)), (52, 'second bow drops, muffled', dict(soft=1)), (84, 'lamp gutters', dict(dur=12))]

    def setup(self, st):
        sit = VN.V_STAND.set(pel=(0, 2.6, -.4), lf=(1.1, .93, .9), rf=(-1.1, .93, .9), lkn=(.6, .6, 1), rkn=(-.6, .6, 1), lh=(1.6, 3.6, 2.2), rh=(-1.6, 3.6, 2.2)); up = VN.V_STAND.set(hedr=(0, -24, 0))
        self.crowd = Crowd(st, [(VN.KINDS[i % 7], up if i % 2 else sit, Face(), (30, -40, 160, -150)[i % 4]) for i in range(8)], px=620, pitch=4.)

    # ------------------------------------------------------------------ shared
    def cloud(self, st, cam, fc, fs, face=0., flash=0., front=0., grey=0., zoom=1., hor=None):
        h = cam.project(cam.eye + V(0, 0, -1.) * 9000)[1] if hor is None else hor
        st.paint(CLOUD, 'over' if front else None, fc=tuple(map(float, fc)), fs=float(fs), face=float(face), flash=float(flash), hor=float(h), zoom=float(zoom), front=float(front), grey=float(grey))

    def ground(self, st): st.world(GROUND, defs='#define STX 7.4\n#define STZ -7.0\n')

    def standard(self, st, t, blow=1.):
        top = LAMP + V(3.4, 13.0, -1.); Q = CL.lag(lambda q: top, t * .8, n=16, length=9.5, wind=(1., .02, .25), grav=.18 + .5 * (1 - blow), wave=.9 * blow, freq=.8)
        st.mesh(*CL.strip(Q, np.linspace(3.6, 1.2, 16), up=(0, 1, 0), m=7, curl=.06, n=40), kind=1, col=('#8a2a2c', '#2a0c24', '#d8a040'), cls=8)
        st.fig(PR.DIYA, at=LAMP, yaw=180, scale=.62)

    def camp(self, st, t, grey=0.):
        """the host in the dark behind: rows of vanaras, small fires"""
        r = np.random.default_rng(5); n = 120; P = np.c_[r.uniform(-120, 120, n), np.full(n, -.2), -r.uniform(28, 120, n)]; P = P[(np.abs(P[:, 0] - 3) > 6) | (P[:, 2] < -60)]
        self.crowd.draw(P, scale=r.uniform(.85, 1.1, len(P)), tile=r.integers(0, 8, len(P)), flip=r.choice([-1, 1], len(P)), tint=(.55, .48, .62))

    FIRES = [(-34, 0, -46), (-62, 0, -80), (30, 0, -58), (58, 0, -90), (-16, 0, -100), (84, 0, -70), (6, 0, -118)]

    def fires(self, st, t, k=1.):
        for i, q in enumerate(self.FIRES): FX.flame(st, V(*q) + V(0, .7, 0), 3.2 * (.6 + .4 * k), seed=i * 2.3, glow=.55 * k, amt=.4 + .6 * k)

    def light(self, t, lamp=1., grey=0., fl=0., extra=(), **k):
        fk = 1 + .08 * noise1(t * 8, 3); g = lambda c: tuple(lerp(np.array(c), np.array([.92, .88, 1.1]) * float(np.dot(c, [.3, .5, .2])), grey))
        d = dict(key=(-.35, .75, .35), keyCol=g((.26, .22, .50)), amb=g((.15, .11, .28)), rim=(-.6, .65, -.5), rimCol=g((.45, .50, .95)), bounceCol=g((.05, .03, .06)), envT='#7a70c8', envM='#6a4a78', envB='#2a1830', fogCol=g((.055, .030, .13)), fog=(.010, 30, 0, 0), inkCol='#05020c',
                 pts=[(LAMP + V(0, 1.6, .4), 5.5, tuple(np.array([1.0, .46, .15]) * lamp * fk))] + list(extra))
        return Light(**{**d, **k})

    def frame(self, f, st):
        st.clear('#000', f=f); t = st.t
        if f < 18: return self.watch(f, st, t)
        if f < 28: return self.shadow(f, st, t)
        if f < 36: return self.strike(f, st, t)
        if f < 60: return self.fall(f, st, t)
        return self.pieta(f, st, t)

    # ------------------------------------------------------------------ back to back
    @staticmethod
    def ready(look=0., g=0): 
        return PZ.STAND.set(pel=(0, 7.9, 0), pelr=(-14, 0, 0), cher=(-10, -8, 0), hedr=(6 + look, -16, 0), lf=(1.3, .75, 1.1), rf=(-1.2, .75, -1.0), lft=(18, 0), rft=(-40, 0), lkn=(.4, 0, 1), rkn=(-.5, 0, 1), lh=(2.5, 13.2, 4.5), rh=(.9, 11.7, 1.7), lel=(.6, -.8, 0), rel=(-1, .1, -.2), lhand='grip', rhand='draw', lfing=(-.5, .1, .8), lpalm=(.5, .2, .85), rfing=(.5, .5, .5), rpalm=(.2, .3, -.9))

    def pair(self, st, f, look=0., faceR=None, faceL=None, hit=0.):
        g = on2(f); br = .05 * math.sin(f / 24. * 5)
        PR_ = self.ready(look); PR_ = PR_.set(pel=(0, 7.9 + br, 0)); SR = st.fig(rama.EXILE, PR_, at=(1.55, 0, 0), yaw=52, face=faceR or Face(frown=.45, gy=.6, lid=1., smile=-.1)); PR.bow_and_arrow(st, SR, half=4.4)
        P = self.ready(-look).set(pel=(0, 7.9 - br, 0)); SL = st.fig(rama.LAKSHMANA, P, at=(-1.75, 0, .5), yaw=-66, face=faceL or Face(frown=.5, gy=.6, lid=1., smile=-.1)); PR.bow_and_arrow(st, SL, half=4.4)
        for S in (SR, SL): st.fig(PR.QUIVER, M=PR.place(S.chest((.5, .5, -1.2)), S.d((-.35, 1, -.12)), S.d((0, 0, -1)), 1.))
        t = f / 24.
        for S, col, ph in ((SR, ('#b0502a', '#42181c', '#e0a848'), 0.), (SL, ('#b5303a', '#4a1020', '#e8c870'), 2.)):
            Q = CL.lag(lambda q: S.pelvis((-.6, .5, -.9)), t, n=16, length=6., wind=(.75, .12, .1), grav=.4, wave=.9, freq=.9, phase=ph); st.mesh(*CL.strip(Q, np.linspace(.6, 1.1, 16), up=(0, 1, .2), m=7, curl=.12, n=40), kind=1, col=col, cls=8)
        return SR, SL

    def watch(self, f, st, t):
        u = ease_io(f / 17., 1.4); cam = Cam(lerp(V(-2.6, 2.4, 34), V(-1.2, 1.9, 30), u), lerp(V(.4, 9.6, 0), V(.4, 11.6, 0), u), 46); st.cam = cam
        fa = smooth(6, 16, f); fl = .5 * decay((f - 13) / 24., 9) if f >= 13 else 0.; fc = (960 - 40 + 20 * u, 285 - 10 * u)
        self.cloud(st, cam, fc, 300 + 36 * fa, face=fa, flash=.15 * fa + fl)
        st.open(cam, self.light(t, rimCol=(.04, .04, .09))); self.camp(st, t); st.close(); self.fires(st, t)
        lit = .8 * fa; L = self.light(t, lamp=1.1, extra=[(V(-3, 4, 12), 7., (.16, .10, .14))], rim=(-.1, .95, -.25), rimCol=tuple(np.array([.35, .60, .75]) * (.8 + 1.6 * fl + .5 * fa)))
        st.open(cam, L); self.ground(st); self.standard(st, t); self.pair(st, f, look=keys(on2(f), [(0, 12.), (6, 4., 'io'), (12, -4., 'io')])); st.close()
        self.lamp_flame(st, f, 1.)
        FX.drift(st, 60, ((-20, 0, -14), (20, 26, 16)), t, kind='ash', size=.08, col='#6a5a94', fall=-.4, sway=.8, seed=2, wind=(4, 0, 0)); FX.embers(st, 24, ((5.6, 6, -7.5), (6.4, 6.6, -6.6)), t, rise=1.6, size=.05, seed=3, wind=(.6, 0, 0))
        return st.finish(bloom=.45, thr=.85, vig=.5, contrast=1.08, satu=1.02)

    # ------------------------------------------------------------------ Indrajit
    def shadow(self, f, st, t):
        u = (f - 18) / 9.; g = on2(f); dr = keys(f, [(18, .35), (25, 1., 'io'), (27, 1.04)]); fl = keys(f, [(18, 0.), (21, .05), (22, 1.1, 'snap'), (24, .85), (25, 1.0, 'snap'), (28, .30)])
        cam = Cam(V(1.6, 6.2 - .6 * u, 27 - 2.2 * u), V(1.4, 11.0, 0), 34, roll=-5 + 2 * u); st.cam = cam
        self.cloud(st, cam, (900., 420.), 520., face=.35 * (1 - smooth(20, 23, f)), flash=.10 + 1.0 * fl, hor=1500., zoom=1.0)
        L = Light(key=(-.75, .62, -.05), keyCol=tuple(np.array([.50, .95, 1.1]) * (.05 + 2.0 * fl)), amb=(.05 + .03 * fl, .045 + .05 * fl, .11 + .08 * fl), rim=(-.8, .55, .1), rimCol=tuple(np.array([.9, 1.5, 1.8]) * (.06 + 1.1 * fl)), bounceCol=(0, 0, 0), envT=tuple(np.array([.5, .8, 1.]) * (.10 + .8 * fl)), envM=tuple(np.array([.10, .14, .22]) * (.3 + fl)), envB='#080414', shadow=False, ink=3.2, inkCol='#020108', stip=.1)
        L.pts = [(V(5.0, 12.6, 3.0), 4.5, tuple(np.array([.30, 1.0, .75]) * (.25 + .6 * fl)))]
        st.open(cam, L); P = PZ.archer(dr); P = P.set(hedr=(46, 6, 0), rh=(P.rh[0] - .5, P.rh[1] - .75, P.rh[2] - .2)); S = st.fig(RK.INDRAJIT, P, yaw=20, face=Face(frown=.55, smile=.25, lid=.9, glow=1., gx=.5, gy=-.3)); nk, tip, aim = RK.serpent_bow(st, S, tint=('#d8fff0', '#58c8a8', 4))
        Q = CL.lag(lambda q: S.chest((-.5, 1.0, -1.0)), t, n=16, length=9., wind=(-.9, .1, -.2), grav=.2, wave=1.2, freq=1.1); st.mesh(*CL.strip(Q, np.linspace(1.2, 2.6, 16), up=(0, 1, .2), m=7, curl=.14, n=40), kind=1, col=('#1c4a48', '#061a20', '#58a890'), cls=8); st.close()
        FX.particles(st, tip[None], .9 + .9 * smooth(22, 27, f), '#7affd8', 'glint', alpha=.9 * smooth(20, 25, f)); FX.ribbon(st, np.linspace(nk, tip, 12), .10, 'light', '#58e8c0', '#f0fff8', amt=.7 * smooth(21, 26, f))
        self.cloud(st, cam, (900., 420.), 520., flash=fl, front=1., hor=900. - 10 * u, zoom=.8)
        return st.finish(bloom=.5, thr=.85, vig=.6, contrast=1.10)

    # ------------------------------------------------------------------ the serpent of lightning
    def serpent(self, st, a, b, p, amt=1., t=0.):
        """a snake of light from pixel a to pixel b, grown to p (0..1): zigzag body with scales, spread hood, fangs"""
        a, b = np.array(a, float), np.array(b, float); d = b - a; L = np.linalg.norm(d); u = d / L; nrm = np.array([-u[1], u[0]]); q = np.linspace(0, p, 150)
        env = np.clip((p - q - .22) / .22, 0, 1); env = env * env * (3 - 2 * env); zz = np.sin(q * 14.5 + 2.2) + .22 * np.sin(q * 29 + 1.)
        C = a + d * q[:, None] + nrm * (zz * 118 * env)[:, None]
        T = np.gradient(C, axis=0); T /= np.linalg.norm(T, axis=1, keepdims=True); N = np.c_[-T[:, 1], T[:, 0]]; s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(C, axis=0), axis=1))]; left = s[-1] - s
        W = np.interp(q, [0, .1, 1], [16, 27, 27]) + 66 * np.exp(-((left - 112) / 58) ** 2)                        # the hood behind the head
        W = np.where(left < 42, np.minimum(W, 30 * np.sqrt(np.maximum(left, 0) / 42) + 4), W)
        FX.ribbon(st, C, np.maximum(W * 4.2, 60), 'bolt', '#3a6cff', '#bfe0ff', amt=.75 * amt); FX.ribbon(st, C, W * 1.9, 'light', '#4af0d0', '#eafff8', amt=.55 * amt)

        def draw(c):
            A, B = C + N * W[:, None], C - N * W[:, None]
            poly(c, np.vstack([A, B[::-1]])); g = cairo.LinearGradient(*C[0], *C[-1]); g.add_color_stop_rgb(0, .55, .78, 1.); g.add_color_stop_rgb(.6, .80, 1., .97); g.add_color_stop_rgb(1, 1., 1., .96); c.set_source(g); c.fill_preserve(); c.set_source_rgb(.10, .05, .32); c.set_line_width(4.); c.stroke()
            # scales
            c.set_line_width(2.2); S = np.arange(8, s[-1] - 46, 19.)
            for m, ss in enumerate(S):
                x, y = np.interp(ss, s, C[:, 0]), np.interp(ss, s, C[:, 1]); tx, ty = np.interp(ss, s, T[:, 0]), np.interp(ss, s, T[:, 1]); w = np.interp(ss, s, W); n = max(2, int(w / 11)); nx, ny = -ty, tx
                for h in range(-n, n + 1):
                    o = (h + .5 * (m % 2)) / (n + .5) * w
                    if abs(o) > w - 3: continue
                    e = w / (n + .5) * .55; px, py = x + nx * o, y + ny * o; c.move_to(px + nx * e, py + ny * e); c.curve_to(px + nx * e + tx * 13, py + ny * e + ty * 13, px - nx * e + tx * 13, py - ny * e + ty * 13, px - nx * e, py - ny * e); c.set_source_rgba(.20, .34, .86, .62); c.stroke()
            # hood marks, eyes, jaws, fangs of light
            h = C[-1]; tt = T[-6:].mean(0); tt /= np.linalg.norm(tt); nn = np.array([-tt[1], tt[0]]); P = lambda f_, g_: tuple(h + tt * f_ * (1.55 if f_ > -60 else 1.) + nn * g_ * (1.55 if f_ > -60 else 1.))
            if p > .3:
                for sg in (-1, 1):
                    c.save(); c.translate(*P(-118, sg * 44)); c.rotate(math.atan2(tt[1], tt[0])); c.scale(1.5, 1.); c.arc(0, 0, 13, 0, 6.3); c.restore(); c.set_source_rgb(.10, .10, .45); c.set_line_width(5); c.stroke()
                    c.move_to(*P(-34, sg * 26)); c.curve_to(*P(-4, sg * 34), *P(26, sg * 30), *P(44, sg * 15)); c.curve_to(*P(24, sg * 12), *P(8, sg * 10), *P(-6, sg * 6)); c.close_path(); c.set_source_rgb(.93, 1., .98); c.fill_preserve(); c.set_source_rgb(.10, .05, .32); c.set_line_width(3.2); c.stroke()
                    c.move_to(*P(34, sg * 16)); c.curve_to(*P(50, sg * 18), *P(66, sg * 10), *P(82, sg * 4)); c.curve_to(*P(64, sg * 3), *P(48, sg * 6), *P(30, sg * 8)); c.close_path(); c.set_source_rgb(1, 1, 1); c.fill()
                    c.move_to(*P(-18, sg * 20)); c.curve_to(*P(-10, sg * 25), *P(0, sg * 24), *P(6, sg * 17)); c.curve_to(*P(-2, sg * 15), *P(-12, sg * 15), *P(-18, sg * 20)); c.set_source_rgb(.85, .10, .20); c.fill()
                c.move_to(*P(8, 0)); c.line_to(*P(52, 0)); c.line_to(*P(66, 9)); c.move_to(*P(52, 0)); c.line_to(*P(66, -9)); c.set_source_rgb(.85, .15, .30); c.set_line_width(3); c.stroke()
        st.vector(draw, alpha=min(1., amt))
        # forks of lightning off its back
        r = np.random.default_rng(int(p * 100) + int(t * 24)); F = []
        for m in range(7):
            i = int(r.integers(4, 145)); sg = r.choice([-1, 1]); w = C[i] + N[i] * sg * W[i]; pts = [w]
            for z in range(7): w = w + (N[i] * sg * r.uniform(14, 40) + T[i] * r.uniform(-20, 45) + r.normal(size=2) * 14); pts.append(w)
            FX.ribbon(st, np.array(pts), np.linspace(7, 1., 8), 'bolt', '#6aa0ff', '#f0f8ff', amt=.8 * amt)
        return C

    HIT = PZ.STAND.set(pel=(0, 7.7, -.5), pelr=(-14, -8, 2), cher=(-6, -20, 2), hedr=(4, -22, 4), lf=(1.2, .75, 1.2), rf=(-1.1, .75, -1.2), lft=(18, 0), rft=(-34, 6), lkn=(.4, 0, 1), rkn=(-.5, 0, 1), lh=(4.4, 11.6, 2.4), rh=(-4.2, 11.0, 1.4), lel=(.5, -.6, -.6), rel=(-.5, -.6, -.6), lhand='open', rhand='open', lfing=(.8, .4, .4), rfing=(-.8, .3, .4))
    AT, YAW = V(-1.75, 0, .5), -72                         # where Lakshmana stands, and which way he faces

    def sashes(self, st, SR, SL, t, w=1.):
        for S, col, ph in ((SR, ('#b0502a', '#42181c', '#e0a848'), 0.), (SL, ('#b5303a', '#4a1020', '#e8c870'), 2.)):
            Q = CL.lag(lambda q: S.pelvis((-.6, .5, -.9)), t, n=16, length=6., wind=(.75 * w, .12 * w, .1), grav=.4 + .4 * (1 - w), wave=.9 * w, freq=.9, phase=ph); st.mesh(*CL.strip(Q, np.linspace(.6, 1.1, 16), up=(0, 1, .2), m=7, curl=.12, n=40), kind=1, col=col, cls=8)

    def strike(self, f, st, t):
        u = (f - 28) / 7.; g = f; hit = f >= 30; cam = Cam(V(-3.4, 2.6, 31 - .5 * u), V(-.4, 11.2, 0), 46, roll=-3); st.cam = cam
        if hit: dx, dy = shake(f, .55 * decay((f - 30) / 24., 7), 1.3, 4); cam = Cam(cam.eye, cam.at + V(dx, dy, 0), 46, roll=-3); st.cam = cam
        fl = [.55, .9, 1.2, 1.0, .6, .3, .14, .05][f - 28]; grey = .55 * smooth(31, 36, f)
        self.cloud(st, cam, (1240., 130.), 330., face=1 - smooth(30, 33, f), flash=fl * .8, grey=grey)
        st.open(cam, self.light(t, rimCol=(.05, .05, .10), grey=grey)); self.camp(st, t); st.close(); self.fires(st, t, 1 - .5 * grey)
        cold = np.array([.75, 1.0, 1.25]); L = self.light(t, lamp=1. - .2 * grey, grey=grey, extra=[(V(-1.6, 13.5, 2.4), 6., tuple(cold * 1.0 * fl))], key=(.15, .9, .35), keyCol=tuple(np.array([.26, .22, .50]) * (1 - .5 * grey) + cold * .55 * fl), rim=(.2, .9, -.3), rimCol=tuple(cold * (.4 + 1.1 * fl)))
        st.open(cam, L); self.ground(st); self.standard(st, t, 1 - .4 * smooth(31, 36, f))
        PR_ = self.ready(0).set(hedr=(keys(g, [(28, 6.), (30, -10.), (34, -44., 'out')]), -8, 0), cher=(keys(g, [(30, -10.), (35, -26., 'out')]), -6, 0)); SR = st.fig(rama.EXILE, PR_, at=(1.55, 0, 0), yaw=52, face=Face(frown=.2, sad=.5 * hit, lid=1., mouth=.25 * hit, gx=-.6 * hit)); PR.bow_and_arrow(st, SR, half=4.4)
        PL = self.ready(0).mix(self.HIT, keys(f, [(29, 0.), (30, .8, 'out'), (32, 1.08, 'out'), (36, 1.)]))
        SL = st.fig(rama.LAKSHMANA, PL, at=self.AT, yaw=lerp(-66, self.YAW, smooth(29, 32, f)), face=Face(lid=1. if not hit else .85, mouth=.35 * hit, sad=.6 * hit, frown=.4 * (not hit), gy=.4))
        if not hit: PR.bow_and_arrow(st, SL, half=4.4)
        else: self.bow(st, f, SL)
        self.sashes(st, SR, SL, t); st.close(); self.lamp_flame(st, f, 1. - .25 * smooth(31, 36, f))
        x, y, z = cam.project(SL.chest((0, .4, .9)) if hit else SL.head((-.6, 1.5, 1.5)))
        pr = {28: .60, 29: .84}.get(f, 1.); am = 1. if f <= 30 else max(0., 1 - (f - 30) / 3.6)
        if am > .02: self.serpent(st, (1500, -330), (x, y - 40 * (f < 30)), pr, am, t)
        if hit:
            at = SL.chest((0, .4, .9)); FX.particles(st, at[None], 4.5 * am + .2, '#bfe8ff', 'spark', alpha=am); FX.burst(st, 60, at, (f - 30) / 24., speed=15, grav=5, size=.09, seed=2, col='#a8dcff', life=.6); FX.burst(st, 24, at, (f - 30) / 24., speed=7, grav=2, size=.16, seed=5, col='#e0f4ff', kind='glint', life=.8)
        if f == 30: IM.inkflash(st, dark='#0a0418', mid='#4a2f9a', light='#eafcff', lo=.24, hi=.60)
        return st.finish(bloom=.55, thr=.85, vig=.5 + .1 * grey, contrast=1.08, satu=1.02 - .4 * grey)

    def bow(self, st, f, SL):
        """the bow leaves Lakshmana's hand (f30), turns over and lies down (f46)"""
        k = (f - 30) / 16.; p0 = self.AT + V(-2.6, 11.0, 2.2); q = clamp(k); y = p0[1] + 2.0 * q - (p0[1] + 1.85) * q ** 2.0; p = V(p0[0] - 2.6 * q, max(.28, y), p0[2] + 2.2 * q); a = min(1., q) * 1.0
        up = lerp(V(.1, 1, .1), V(.93, .02, -.35), ease_io(a)); z = lerp(V(-.9, .3, .3), V(.1, .15, .9), ease_io(a))
        st.fig(PR.BOW.variant(u=dict(pr=np.array([1.0, 4.4] + [0] * 14, 'f4'))), M=PR.place(p, up, z, 1.))

    def fall(self, f, st, t):
        """no sound: he goes down slowly and his brother is there"""
        g = on2(f); u = ease_io((f - 36) / 23., 1.3); lk = self.lampk(f); ts = 1.5 + (f - 36) / 24. * .45                                # everything but the brothers moves at less than half speed
        cam = Cam(lerp(V(-1.5, 6.2, 33), V(.4, 6.0, 29), u), lerp(V(.5, 7.2, 0), V(1.2, 5.8, 0), u), 30); st.cam = cam; grey = .55
        self.cloud(st, cam, (1240., -200.), 400., flash=.10 * (1 - u), grey=.62)
        st.open(cam, self.light(ts, grey=grey, rimCol=(.02, .02, .03))); self.camp(st, ts); st.close(); self.fires(st, ts, .35); IM.defocus(st, 2.5)
        L = self.light(ts, lamp=.9 * lk, grey=.5, key=(.10, .30, .92), keyCol=(.36, .34, .52), rim=(.6, .7, -.4), rimCol=(.5, .52, .85))
        st.open(cam, L); self.ground(st); self.standard(st, ts, .45)
        K1 = self.HIT.set(lhand='relax', rhand='relax', lfing=(.5, -.5, .4), rfing=(-.5, -.5, .4), pel=(0, 7.1, -.9), pelr=(-10, -20, 2), cher=(-4, -18, 0), hedr=(10, -18, 6), lh=(4.0, 8.2, 1.0), rh=(-3.6, 8.6, .2))
        K2 = self.HIT.set(pel=(0, 5.4, -2.4), pelr=(-6, -36, 0), cher=(2, -14, 2), hedr=(20, -14, 8), lh=(3.0, 4.0, -2.0), rh=(-2.2, 5.6, -2.0), lhand='relax', rhand='relax', lfing=(.3, -.9, .2), rfing=(-.2, -.8, .3), lpalm=(-.6, 0, .6), lf=(.9, .75, 1.6), rf=(-.9, .75, .4), lft=(18, -6), rft=(-20, 0), lkn=(.3, .5, 1), rkn=(-.3, .5, 1))
        K3 = self.HIT.set(pel=(0, 2.9, -3.3), pelr=(0, -50, 0), cher=(6, -9, 3), hedr=(36, -8, 12), lh=(2.4, 1.4, -4.2), rh=(.2, 4.6, -4.3), lhand='relax', rhand='relax', lfing=(.4, -.5, .5), lpalm=(0, .6, .8), rfing=(.75, -.3, -.2), rpalm=(0, -.8, -.5), lf=(.6, .75, 1.7), rf=(-.6, .75, .6), lft=(24, -20), rft=(-18, -10), lkn=(.25, 1, .1), rkn=(-.1, 1, .1), lel=(1, -.1, -.4), rel=(-.8, .5, .4))
        PL = keys(g, [(36, self.HIT), (42, K1, 'io'), (50, K2, 'io'), (57, K3, 'io'), (60, K3)])
        SL = st.fig(rama.LAKSHMANA, PL, at=self.AT, yaw=-84 + 12 * (1 - smooth(36, 44, g)), face=Face(lid=keys(f, [(36, .8), (44, .45), (52, 0., 'io')]), mouth=.3 * (1 - smooth(38, 48, f)), sad=.45, smile=0.))
        hl, ch = SL.head((0, 0, 0)), SL.chest((0, 0, -.6))
        # Rama: lets his own bow go, turns, steps in under him, goes down on one knee
        A = self.ready(0).set(hedr=(-44, -6, 0), cher=(-26, -6, 0)); w = keys(g, [(38, 0.), (52, 1., 'io')])
        R1 = PZ.STAND.set(pel=(0, 7.7, 0), pelr=(0, 4, 0), cher=(0, 8, 0), hedr=(14, 33, 6), lf=(1.4, .75, .8), rf=(-1.3, .75, -.6), lhand='open', rhand='open')
        R2 = Pose(pel=(0, 4.1, 0), pelr=(0, 4, 0), cher=(4, 14, 5), hedr=(20, 19, 7), lf=(2.5, .75, 2.1), rf=(-1.5, 1.2, -2.6), lkn=(.5, .5, 1), rkn=(-.4, -.5, 1), lft=(20, 0), rft=(-20, 70), lhand='cup', rhand='open')
        base = keys(g, [(36, A), (42, R1.set(lh=(2.6, 10.6, 2.4), rh=(-2.4, 10.6, 2.2)), 'io'), (48, R1.set(pel=(0, 6.6, 0)), 'io'), (56, R2, 'io'), (60, R2)])
        at = np.array(keys(g, [(36, (1.55, 0, 0)), (46, (2.2, 0, -2.0), 'io'), (60, (2.3, 0, -2.9), 'io')])); yaw = keys(g, [(36, 52.), (46, -14., 'io'), (56, -10., 'io'), (60, -6.)])
        MI = np.linalg.inv(np.vstack([np.c_[eul(yaw, 0, 0), at], [0, 0, 0, 1]])); loc = lambda p: (MI @ np.append(p, 1))[:3]
        if g >= 44:
            k = smooth(43, 50, g); lt = loc(hl + V(.2, -.9, -.8)); rt = loc(ch + V(-.4, .2, .9) if g < 52 else SL.chest((-.2, .3, 1.0)) + V(0, .2, .1))
            bl, br = (np.array(base.lh) if base.lh else lt), (np.array(base.rh) if base.rh else rt); base = base.set(lh=tuple(lerp(bl, lt, k)), rh=tuple(lerp(br, rt, k)), lel=(1, -.2, -.2), rel=(-1, -.4, .1), lfing=(.15, .25, .95), lpalm=(-.5, .85, .2), rfing=(.6, .1, .7), rpalm=(.2, -.7, -.5), lhand='cup', rhand='open')
        SR = st.fig(rama.EXILE, base, at=at, yaw=yaw, face=Face(lid=keys(f, [(36, 1.), (42, .8), (58, .55)]), sad=.8, mouth=.18 * (1 - smooth(48, 56, f)), smile=-.3, gx=.2, gy=-.75 * smooth(38, 44, f)))
        self.bow(st, f, SL)
        kb = clamp((f - 37) / 15.); pb = lerp(V(5.6, 12.2, 1.6), V(7.6, .3, 3.4), kb); pb[1] = max(.28, 12.2 - 11.9 * kb ** 2.); st.fig(PR.BOW.variant(u=dict(pr=np.array([1.0, 4.4] + [0] * 14, 'f4'))), M=PR.place(pb, lerp(V(.1, 1, 0), V(.8, .05, .5), ease_io(kb)), lerp(V(.8, .3, .5), V(-.3, .9, .4), ease_io(kb)), 1.))
        self.sashes(st, SR, SL, ts, .55); st.close(); self.lamp_flame(st, f, lk)
        FX.burst(st, 20, V(-4.4, .2, 2.7), (f - 46) / 24. * .5, speed=2.5, grav=.5, size=.7, seed=4, col='#4a4466', kind='smoke', life=.9, spread=(1, .2, 1))
        FX.drift(st, 70, ((-16, 0, -8), (16, 18, 12)), ts, kind='ash', size=.09, col='#8a84a8', fall=.8, sway=.8, seed=4, wind=(1., 0, 0), alpha=.6)
        return st.finish(bloom=.45, thr=.85, vig=.58, contrast=1.05, satu=.62)

    # ------------------------------------------------------------------ pieta
    def lampk(self, f): return keys(f, [(30, 1.), (36, .75), (60, .62), (74, .5), (84, .30), (91, .10), (96, .07)])

    def lamp_flame(self, st, f, lk, big=1.):
        """the lamp by the standard; as it fails the flame shrinks to a blue bead"""
        w = LAMP + V(-.82, .30, 0); gone = 1 - smooth(.08, .42, lk)
        tint = tuple(lerp(np.array([1., 1., 1.]), np.array([.34, .55, 1.5]), gone)); fl = 1 + .22 * gone * noise1(f * .9, 7)
        x, y, z = st.cam.project(w); h = (.35 + 1.75 * lk) * fl * big * st.cam.px(w)
        st.paint(FLAME, 'over', base=(float(x), float(y)), ht=float(h), wd=float(h * .42), lean=float(.35 * gone * noise1(f * .3, 3)), seed=2.2, amt=1., glow=.25 + .7 * lk, calm=1. + 1.4 * gone, tint=tint, fz=float(z))

    def pieta(self, f, st, t):
        u = ease_io((f - 60) / 35., 1.3); g = on2(f); lk = self.lampk(f)
        cam = Cam(lerp(V(-4.5, 7.6, 38), V(-2.0, 8.6, 33), u), lerp(V(1.3, 6.3, 1.5), V(2.0, 8.0, 1.8), u), lerp(21, 13.5, u), roll=0); st.cam = cam
        self.cloud(st, cam, (500., -200.), 700., grey=.66)
        st.open(cam, self.light(t, grey=.6, shadow=False, rimCol=(0, 0, 0))); self.camp(st, t); st.close(); self.fires(st, t, .25); IM.defocus(st, 5.)
        L = self.light(t, lamp=.85 * lk + .05, grey=.55, key=(.25, .42, .85), keyCol=(.36, .34, .50), rim=(.75, .55, -.4), rimCol=(.55, .55, .85))
        st.open(cam, L); self.ground(st); self.standard(st, t * .6, .35); br = .05 * math.sin(t * 1.6)
        PL = Pose(pel=(0, 1.75, 2.4), pelr=(0, -46, 0), cher=(8, -6, 4), hedr=(44, -8, 14), lf=(.75, .55, 9.15), rf=(-.75, .60, 8.0), lkn=(.35, 1, .1), rkn=(-.25, 1, .1), lft=(34, -62), rft=(-30, -52), lh=(1.9, .95, .4), lel=(1, -.1, -.4), lhand='relax', lfing=(.4, -.5, .5), lpalm=(0, .6, .8), rh=(.55, 4.25, 1.3), rel=(-.8, .5, .4), rhand='relax', rfing=(.75, -.35, -.2), rpalm=(0, -.8, -.5))
        SL = st.fig(rama.LAKSHMANA, PL, at=(0, 0, 3.0), yaw=-90, face=Face(lid=.0, smile=.05, sad=.15))
        hl = SL.head((0, 0, 0)); self.hl = hl
        PRm = Pose(pel=(-.3, 4.0, -.2), pelr=(6, 4, 0), cher=(8, 17 + br, 7), hedr=(keys(g, [(60, 16.), (74, 12., 'io')]), 15 + 2 * smooth(66, 84, g), 7), lf=(2.6, .75, 2.0), rf=(-1.5, 1.2, -2.6), lkn=(.5, .5, 1), rkn=(-.4, -.5, 1), lft=(20, 0), rft=(-20, 70),
                   lh=tuple(hl + V(.45, -.75, -.75)), lel=(1, -.2, -.2), lhand='cup', lfing=(.15, .25, .95), lpalm=(-.5, .85, .2), rh=(-.75, 5.15, 3.5), rel=(-1, -.4, .1), rhand='relax', rfing=(.80, .05, .5), rpalm=(.1, -.85, -.4))
        S = st.fig(rama.EXILE, PRm, face=Face(lid=keys(f, [(60, .5), (70, .5), (76, .34), (84, .42)]), sad=.9, smile=-.35, gx=.35, gy=-.6, tear=0.))
        w = .35 + .65 * smooth(62, 76, f)
        Q = CL.lag(lambda q: S.chest((1.1, 1.0, -.75)), t * .7, n=18, length=8.5, wind=(-.95 * w, .05, -.15), grav=.95 - .62 * w, wave=.9 * w, freq=.8, phase=1.); st.mesh(*CL.strip(Q, np.linspace(.7, 1.5, 18), up=(0, 1, .25), m=7, curl=.12, n=44), kind=1, col=('#b0502a', '#42181c', '#e0a848'), cls=8)
        # the bow he let fall
        st.fig(PR.BOW.variant(u=dict(pr=np.array([1.0, 4.6] + [0] * 14, 'f4'))), M=PR.place(V(-3.4, .22, 7.2), V(.93, .02, -.35), V(.1, .15, .9), 1.)); st.close()
        self.lamp_flame(st, f, lk)
        # one tear: it wells, runs down the cheek, and falls
        a = np.array([0.]); 
        if f >= 74:
            q = smooth(74, 88, f); e0, e1 = S.head((.30, -.16, .93)), S.head((.36, -.78, .84)); P = e0 + (e1 - e0) * q
            if f < 90: FX.particles(st, (P + S.d((0, 0, .06)))[None], .085, '#dff0ff', 'ember', alpha=.95 * smooth(74, 77, f)); FX.ribbon(st, np.array([e0 + (P - e0) * k for k in np.linspace(0, 1, 8)]), .022, 'light', '#a8c4f0', '#f4faff', amt=.8)
            else: FX.particles(st, (e1 + V(.05, -.5 * ((f - 89) / 24. * 6) ** 2 * .5, .1))[None], .07, '#e8f4ff', 'drop')
        FX.particles(st, np.array([LAMP + V(-.82, .45, 0)]), .5 * (1 - lk) + .2, '#7aa8ff', 'ember', alpha=.55 * smooth(80, 92, f))
        FX.drift(st, 36, ((-14, 0, -8), (14, 16, 10)), t * .6, kind='ash', size=.07, col='#8a84a8', fall=.5, sway=.6, seed=4, wind=(.8, 0, 0), alpha=.5)
        IM.dof(st, float((S.head() - cam.eye) @ cam.R[2]), 8., 6.)
        return st.finish(bloom=.45, thr=.8, vig=.62, contrast=1.06, satu=.66)
