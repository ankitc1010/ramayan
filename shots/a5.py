"""a5 (72): the wedding.  Across the sacred fire Sita raises the garland; their eyes meet (f30); the garland comes down over the lens (f60-72)."""
from lau.shot import *
from lau.look import *
from chars import rama, sita, garland as GL

MANDAP = '''
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform vec2 res,fire;uniform float fT,zoom,close_;
void main(){vec2 p=vec2(uv.x*res.x,(1.-uv.y)*res.y);vec2 c=vec2(960.,fire.y);vec2 q=(p-c)/zoom;float r=length(q-vec2(0,-260.))/540.,a=atan(q.y+260.,q.x);
 vec3 b=mix(hex(0x7a1420),hex(0x2a0614),smoothstep(.15,1.7,r));b*=.86+.24*fbm(p/210.);
 // a mandala of lotus petals behind the fire
 for(int i=0;i<4;i++){float R=.30+.19*float(i);float n=12.+6.*float(i);float w=abs(fract(a*n/TAU+.5*float(i))-.5);float e=r-R-.075*sqrt(max(0.,1.-w*w*4.));float k=smoothstep(.006,-.006,abs(e)-.004);b=mix(b,hex(0xe8a83c)*.75,k*(.85-.14*float(i)));float f=smoothstep(.0,-.05,e)*smoothstep(-.075,-.02,e);b+=hex(0xc8501c)*f*.14;}
 float gl=exp(-dot(q-vec2(0,-60.),q-vec2(0,-60.))/(330.*330.));b+=hex(0xff8a2c)*gl*.55*(1.+.06*sin(fT*9.));
 // hanging strings of marigold, three depths
 for(int i=2;i>=0;i--){float fi=float(i);float sp=(74.+26.*fi)*1.;float sway=6.*sin(fT*1.1+p.y*.004+fi*2.);float x=q.x*(1.-.10*fi)+sway+fi*31.;float id=floor(x/sp);float L=380.+170.*h11(id+fi*9.)+120.*fi-360.*smoothstep(900.,120.,abs((id+.5)*sp))*(.55+.2*fi);float y=q.y+760.;if(y<L){float s=15.-2.5*fi;vec2 u=vec2(x-(id+.5)*sp,mod(y,s*1.7)-s*.85);float d=length(u)-s*.8*(.9+.12*sin(atan(u.y,u.x)*7.));float odd=mod(floor(y/(s*1.7)),2.);vec3 m=mix(hex(0xd8640c),hex(0xf2a51e),odd);m*=.62+.5*smoothstep(s,-s,u.y);m=mix(hex(0x3a0c10),m,smoothstep(2.,-2.,d+2.5));m*=1.-.24*fi;b=mix(b,m,smoothstep(1.,-1.,d));}}
 // pillars wrapped in flowers, near the edges
 for(int s=-1;s<=1;s+=2){float x=abs(q.x-float(s)*860.);float w=70.;if(x<w){float u=(q.x-float(s)*860.)/w;vec3 m=mix(hex(0x5a0f1a),hex(0xb8641c),smoothstep(-1.,.2,-u*float(s)));float band=step(.5,fract((q.y+u*38.)/66.));vec3 f=mix(hex(0xd8640c),hex(0xf2a51e),step(.5,fract((q.y+u*38.)/33.)));float dot_=length(vec2(fract(u*3.)-.5,fract((q.y+u*38.)/22.)-.5));m=mix(m,f*(.5+.5*smoothstep(.5,.1,dot_)),band*smoothstep(.5,.42,dot_));m*=1.-.5*abs(u);b=mix(b,m,smoothstep(w,w-3.,x));}}
 o=vec4(b,1);}
'''


def kund(st, at, t, amt=1., seed=0):
    """the sacred fire in its brick altar: flames only (altar drawn by the world)"""
    r = np.random.default_rng(seed); n = 34; a = r.uniform(0, 6.28, n); rr = r.uniform(0, .85, n) ** .7; s = r.uniform(.9, 2.2, n) * (1.15 - .5 * rr) * amt * (1 + .12 * np.sin(t * 8 + a * 5)); P = np.asarray(at) + np.c_[np.cos(a) * rr * 1.5, s * .92, np.sin(a) * rr * 1.1]; o = np.argsort(P[:, 2])
    FX.particles(st, P[o], s[o], (1, 1, 1), 'tongue', seed=r.uniform(0, 1, n)[o])


ALTAR = '''
#define TMAX 90.
vec2 map(vec3 p){vec2 m=vec2(p.y+.0,1.);vec3 q=p-vec3(0,0,1.2);float d=1e3;for(int i=0;i<3;i++){float f=float(i);float y=.35+.62*f;d=min(d,sBox(q-vec3(0,y,0),vec3(2.9-.42*f,.31,2.3-.36*f),.06));}d=max(d,-sBox(q-vec3(0,2.1,0),vec3(1.55,.9,1.15),.05));m=U(m,vec2(d,2.));vec3 k=q-vec3(0,2.2,0);k.xz=rot(.5)*k.xz;m=U(m,vec2(sCap(k,vec3(-1.5,-.3,0),vec3(1.5,.1,.2),.16),3.));k.xz=rot(1.2)*k.xz;m=U(m,vec2(sCap(k,vec3(-1.4,-.3,0),vec3(1.4,.15,0),.15),3.));return m;}
void surf(vec3 p,vec3 n,int m,inout Surf s){if(m==1){vec2 u=p.xz;float r=length(u-vec2(0,1.2));float a=atan(u.y-1.2,u.x);float pt=smoothstep(.06,.02,abs(r-5.2-.5*abs(sin(a*9.))))+smoothstep(.05,.02,abs(r-7.4-.35*cos(a*16.)))+smoothstep(.20,.12,length(vec2(fract(a*24./TAU)-.5,(r-6.4)*.9)));s.base=mix(hex(0x6a1a20),hex(0xf2e6cc),clamp(pt,0.,1.)*.85);s.sh=hex(0x1c060e);s.ink=.2;}
 if(m==2){float b=step(.94,fract((p.x+floor(p.y/.62)*.4)*.8));s.base=mix(hex(0xb8502c),hex(0x8a2f22),b);float d=length(vec2(fract(p.x*1.1)-.5,fract(p.y/.62)-.5)*vec2(1.,.6));s.base=mix(s.base,hex(0xfff0d0),smoothstep(.12,.07,d)*step(.5,abs(n.z)+abs(n.x)));s.sh=hex(0x3a0c14);}
 if(m==3){s.base=hex(0x4a2416);s.sh=hex(0x1a0a08);float g=smoothstep(.9,.2,abs(p.x));s.cls=4.;s.base=mix(hex(0x2a1008),hex(0xff6a1c),g*.8);}}
'''


class Shot(ShotBase):
    id = 'a5'; n = 72
    EVENTS = [(0, 'sacred fire', dict(dur=72)), (0, 'petals', dict(dur=72)), (6, 'bangles', {}), (30, 'eyes meet', {}), (60, 'garland falls', {})]

    def lights(self, t, k=1.):
        fl = k * (1 + .07 * noise1(t * 8, 3) + .05 * noise1(t * 19, 5))
        return Light(key=(0, .30, .95), keyCol=(.62, .40, .25), amb=(.20, .10, .14), rim=(0, .5, -.9), rimCol=(1.0, .5, .2), bounceCol=(.30, .12, .04), envT='#ffb060', envM='#e8641c', envB='#6a1420', pts=[(V(0, 4.6, 1.6), 6.5, tuple(np.array([1.15, .56, .20]) * fl))], ink=3.2)

    def two(self, st, raise_, rf, sf, blink=0.):
        Pr = PZ.STAND.set(pel=(0, 8.3, 0), cher=(0, 4, 0), hedr=(0, 9, 0), lh=(1.6, 8.9, 1.9), rh=(-1.6, 8.9, 1.9), lhand='relax', rhand='relax')
        Sr = st.fig(rama.PRINCE, Pr, at=(-4.7, 0, 0), yaw=78, face=rf)
        A = sita.fit(sita.S_STAND).set(lh=(1.1, 8.0, 2.2), rh=(-1.1, 8.0, 2.2), lhand='cup', rhand='cup', lpalm=(0, 1, .2), rpalm=(0, 1, .2)) if hasattr(sita, 'fit') else sita.S_STAND
        P = A.mix(sita.S_GARLAND, raise_).set(hedr=(0, lerp(16, 2, raise_), 0)); Ss = st.fig(sita.BRIDE, P, at=(4.5, 0, 0), yaw=-78, face=sf)
        L, R = Ss.palm('L'), Ss.palm('R'); lo = (L + R) / 2 + V(-.5, -3.2, 0); GL.string(st, [L + V(0, .25, 0), L * .6 + lo * .4 + V(-.3, -.9, .4), lo, R * .6 + lo * .4 + V(-.3, -.9, -.4), R + V(0, .25, 0)], r=.27)
        return Sr, Ss

    def frame(self, f, st):
        st.clear('#000', f=f); t = st.t; g = on2(f)
        petals = lambda: FX.drift(st, 70, ((-13, 0, -6), (13, 19, 9)), t, kind='petal', size=.17, col='#f2a03a', col2='#e8506a', fall=1.5, sway=.6, seed=4)
        if f < 30:
            u = f / 29.; up = keys(g, [(2, 0.), (18, 1.04, 'io'), (24, 1.)]); cam = Cam(V(0, 8.2 + .5 * u, 31 - 4.0 * ease_io(u)), V(0, 8.3 + .4 * u, 0), 32); st.cam = cam; x, y, z = cam.project(V(0, 3, 0)); st.paint(MANDAP, fire=(float(x), float(y)), zoom=float(1 + .10 * u), close_=0.)
            st.open(cam, self.lights(t)); st.world(ALTAR); self.two(st, up, Face(smile=.3, gx=0, lid=.95), Face(lid=lerp(.35, .62, u), smile=.25, gy=-.4)); st.close()
            kund(st, (0, 2.0, 1.2), t); FX.embers(st, 60, ((-1.6, 2.4, .2), (1.6, 3.4, 2.2)), t, rise=4.2, size=.06, seed=2, life=2.2, swirl=.8); petals()
            return st.finish(bloom=.5, thr=.9, vig=.5, contrast=1.06)
        if f < 47:
            u = (f - 30) / 16.; lid = keys(f, [(30, .55), (36, 1.0, 'out'), (46, .96)]); P = sita.fit(sita.S_STAND).set(lh=(1.4, 8.6, 2.2), rh=(-1.4, 8.6, 2.2), pelr=(0, 0, 0), cher=(0, 2, 0), hedr=(0, keys(g, [(30, 12.), (38, 2., 'io')]), 4)); S = st.fig(sita.BRIDE, P, at=(0, 0, 0), yaw=0, draw=False); h = S.head((0, 0, .5))
            cam = Cam(h + V(-2.6 + .3 * u, -.5, 8.6 - .5 * u), h + V(-.15, .12, 0), 22, roll=2); st.cam = cam; st.paint(MANDAP, fire=(960., 1500.), zoom=2.6, close_=1.)
            fl = 1 + .08 * noise1(t * 8, 3); L = Light(key=(-.45, -.10, .9), keyCol=(.85, .52, .30), amb=(.24, .12, .16), rim=(.8, .4, -.6), rimCol=(1.1, .55, .25), bounceCol=(.30, .12, .04), envT='#ffb060', envM='#e8641c', envB='#8a2420', pts=[(h + V(-1.6, -2.8, 2.6), 4.2, tuple(np.array([.8, .4, .15]) * fl))], shadow=False, ink=3.4)
            st.open(cam, L); st.fig(sita.BRIDE, P, face=Face(lid=lid, gx=-.35, gy=.15, smile=keys(f, [(34, .2), (44, .55)]), spark=.75 * smooth(33, 38, f), brow=.2)); st.close(); FX.drift(st, 26, (tuple(h - V(5, 4, 2)), tuple(h + V(5, 4, 5))), t, kind='petal', size=.12, col='#f2a03a', col2='#e8506a', fall=1.3, sway=.5, seed=7); IM.dof(st, float((h - cam.eye) @ cam.R[2]), 7, 5)
            return st.finish(bloom=.5, thr=.9, vig=.5, contrast=1.06)
        if f < 60:
            u = (f - 47) / 12.; P = PZ.STAND.set(hedr=(0, 7, -3)); S = st.fig(rama.PRINCE, P, draw=False); h = S.head((0, 0, .5)); cam = Cam(h + V(2.6 - .3 * u, -.5, 9.0 - .5 * u), h + V(.15, .28, 0), 23, roll=-2); st.cam = cam; st.paint(MANDAP, fire=(960., 1500.), zoom=2.6, close_=1.)
            fl = 1 + .08 * noise1(t * 8, 3); L = Light(key=(.45, -.10, .9), keyCol=(.85, .55, .34), amb=(.22, .13, .20), rim=(-.8, .4, -.6), rimCol=(1.1, .55, .25), bounceCol=(.30, .12, .04), envT='#ffb060', envM='#e8641c', envB='#8a2420', pts=[(h + V(1.6, -2.8, 2.6), 4.2, tuple(np.array([.8, .4, .15]) * fl))], shadow=False, ink=3.4)
            st.open(cam, L); st.fig(rama.PRINCE, P, face=Face(lid=.92, gx=.35, gy=-.1, smile=keys(f, [(47, .25), (56, .5)]), spark=.75)); st.close(); FX.drift(st, 26, (tuple(h - V(5, 4, 2)), tuple(h + V(5, 4, 5))), t, kind='petal', size=.12, col='#f2a03a', col2='#e8506a', fall=1.3, sway=.5, seed=9); IM.dof(st, float((h - cam.eye) @ cam.R[2]), 7, 5)
            return st.finish(bloom=.5, thr=.9, vig=.5, contrast=1.06)
        # through his eyes: the garland comes over
        u = (f - 60) / 11.; e = ease_io(u, 1.6); P = sita.S_GARLAND.set(hedr=(0, 6, 0)); S = st.fig(sita.BRIDE, P, at=(0, 0, -7.5 + 3.0 * e), draw=False); h = S.head((0, 0, .3)); cam = Cam(V(0, 12.6, 6.0), V(0, 12.5, -6), 40); st.cam = cam; st.paint(MANDAP, fire=(960., 900.), zoom=1.6, close_=1.)
        st.open(cam, self.lights(t, 1.1)); st.world(ALTAR); st.fig(sita.BRIDE, P, at=(0, 0, -7.5 + 3.0 * e), face=Face(lid=.95, smile=.55, spark=.8, gy=.1))
        L, R = S.palm('L'), S.palm('R'); zc = lerp(-1.5, 5.2, e); w = lerp(1.6, 1.35, e); top = lerp(13.4, 13.75, e); Q = np.array([V(math.sin(a) * w * (1. if abs(a) < 2.6 else .8), top - 1.35 + 1.42 * math.cos(a), zc - .35 * math.cos(a)) for a in np.linspace(-math.pi, math.pi, 25)]); GL.string(st, Q, r=.22, gap=1.42)
        st.close(); petals()
        return st.finish(bloom=.5, thr=.9, vig=.5, contrast=1.06, fade=smooth(68, 72, f), fadeCol='#1a0608')
