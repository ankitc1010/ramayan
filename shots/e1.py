"""e1 (96): a vermilion finger writes the name on a stone (f0-36); it is dropped (f42), sinks, the name glows (f60), it rises, breaks the surface and floats (f84)."""
from lau.shot import *
from lau.look import *
from chars import rama
from chars.armonly import ARM, SKIN, place_hand

STONE = '''
#define STEPS 110
uniform sampler2D tName;uniform vec3 sPos;uniform mat3 sRot;uniform float glowN,wet,sScale;
float stoneD(vec3 p){vec3 q=sRot*(p-sPos)/sScale;float d=sBox(q,vec3(2.6,.95,1.75),.55);d=smin(d,sEll(q-vec3(.8,-.2,.4),vec3(1.9,1.0,1.5)),.6);d-=.16*fbm3(q*.9)+.05*vn3(q*3.1);return (d+.12)*sScale*.8;}
vec2 map(vec3 p){return vec2(stoneD(p),1.);}
void surf(vec3 p,vec3 n,int m,inout Surf s){
  vec3 q=sRot*(p-sPos)/sScale;vec3 nl=sRot*n;float v=fbm3(q*1.5),cr=smoothstep(.02,.0,abs(fbm3(q*.8+3.)-.5)-.01);
  s.base=mix(hex(0x8d8378),hex(0xc9bda8),v);s.base=mix(s.base,hex(0x5a5048),smoothstep(.55,.75,fbm3(q*3.+7.))*.6);s.base*=1.-.5*cr;s.sh=mix(hex(0x3a3440),hex(0x5c5560),v);s.base*=mix(1.,.62,wet);s.cls=wet>.5?8.:1.;s.ink=.9;
  if(nl.y>.35){vec2 u=vec2(q.x/4.6+.5,q.z/2.9+.5);if(u.x>0.&&u.x<1.&&u.y>0.&&u.y<1.){vec4 t=texture(tName,vec2(u.x,1.-u.y));float a=t.a*smoothstep(.35,.6,nl.y);a*=.86+.14*vn(q.xz*14.);
    s.base=mix(s.base,hex(0xc81e14)*(wet>.5?.85:1.),a);s.sh=mix(s.sh,hex(0x6a0c12),a);
    if(glowN>0.&&a>.05){float g=a*glowN;s.cls=g>.2?4.:s.cls;s.base=mix(s.base,hex(0xff8020)*(1.25+.35*glowN),g);}}}
}
'''
BELOW = '''
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform vec2 res;uniform float fT,depth,open_;
float ca(vec2 p,float t){float c=0.;mat2 m=mat2(.8,.6,-.6,.8);for(int i=0;i<4;i++){p=m*p*1.35+vec2(t*.35,-t*.22);float n=abs(vn(p)-.5);c+=smoothstep(.10,.0,n);}return c*.35;}
void main(){vec2 p=(uv-.5)*vec2(res.x/res.y,1.);float y=uv.y;
 vec3 c=mix(hex(0x03222e),hex(0x0d5a62),smoothstep(0.,.75,y-depth*.35+.18));c=mix(c,hex(0x4fc0a8),smoothstep(.55,1.15,y-depth*.5+.1));
 vec2 s=vec2(p.x+.10,1.25-y);float a=atan(p.x-.05,1.5-y+.2);float ray=0.;for(int i=0;i<3;i++){float f=9.+float(i)*7.;ray+=smoothstep(.45,1.,vn(vec2(a*f+float(i)*3.,fT*.35+float(i))))*.4;}
 c+=hex(0x9fe8c8)*ray*smoothstep(-.1,.9,y)*.38*(1.-depth*.5);
 c+=hex(0x7fe0c0)*ca(p*vec2(7.,3.)+vec2(0,depth*6.),fT*1.6)*smoothstep(.62,1.05,y-depth*.45)*.75;
 float fl=smoothstep(.10,-.05,y-.10-.06*fbm(vec2(p.x*3.+1.,2.)))*smoothstep(.2,.9,depth);c=mix(c,hex(0x02141c),fl);
 c*=.92+.14*fbm(uv*vec2(9.,6.)+fT*.05);o=vec4(c,1);}
'''


class Shot(ShotBase):
    id = 'e1'; n = 96
    EVENTS = [(4, 'finger on stone', dict(dur=30)), (36, 'last stroke', {}), (42, 'stone hits water', {}), (46, 'underwater', dict(dur=36)), (60, 'name glows', {}), (72, 'stone rises', {}), (84, 'stone breaks surface', {})]

    def name_tex(self, up):
        k = round(up, 3)
        if k in self.tx: return self.tx[k]
        w, h = 1400, 880; sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h); c = cairo.Context(sf); LT.draw(c, 'ram', 330, 250, 430, col=(1, 1, 1), w=.15, upto=up); sf.flush(); t = gl.tex_from(np.ndarray((h, w, 4), np.uint8, sf.get_data()).copy()); t.swizzle = 'BGRA'
        if len(self.tx) > 60: self.tx.clear()
        self.tx[k] = t
        return t

    def setup(self, st):
        self.tx = {}; S, tot = LT.strokes('ram', 60); L = np.array([np.linalg.norm(np.diff(s, axis=0), axis=1).sum() for s in S]); self.S, self.L = S, L

    def tip(self, up):
        """pen position on the plate (pixels of the 1400x880 name) for progress up, and whether the pen is down"""
        T = self.L.sum() * up; a = 0
        for s, l in zip(self.S, self.L):
            if T <= a + l or s is self.S[-1]:
                u = clamp((T - a) / l); i = u * (len(s) - 1); j = min(int(i), len(s) - 2); q = s[j] + (s[j + 1] - s[j]) * (i - j); return V(330 + q[0] * 430, 250 + q[1] * 430)
            a += l

    def glow(self, st, cam, at, g):
        x, y, z = cam.project(at); st.paint('''
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform vec2 res,c;uniform float g,fT;void main(){vec2 p=vec2(uv.x*res.x,(1.-uv.y)*res.y)-c;float r=length(p)/res.y;float a=atan(p.y,p.x);float ray=.5+.5*sin(a*14.+fT*1.2)*sin(a*5.-fT*.7);vec3 q=hex(0xff9a34)*(exp(-r*r*16.)*.30+exp(-r*3.6)*.16*(.7+.5*ray))*g;o=vec4(q,0);}
''', 'over', c=(float(x), float(y)), g=float(g))

    def stone(self, st, pos, rot, sc, up, glow=0., wet=0.):
        st.world(STONE, u=dict(sPos=tuple(pos), sRot=rot.T, sScale=float(sc), glowN=float(glow), wet=float(wet)), texs=dict(tName=self.name_tex(up)))

    def frame(self, f, st):
        st.clear('#000', f=f); t = st.t
        if f < 40: return self.write(f, st, t)
        return self.water(f, st, t)

    def write(self, f, st, t):
        up = keys(f, [(3, 0.), (14, .30, 'io'), (20, .52, 'io'), (30, .86, 'io'), (36, 1., 'io')]); lift = smooth(36, 40, f)
        cam = Cam(V(.2 + .010 * f, 7.6 - .02 * f, 4.4 - .012 * f), (.15, 1.0, .05), 34, roll=-6 + .06 * f); st.cam = cam
        st.paint('''
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform vec2 res;uniform float fT;
void main(){vec2 p=uv*vec2(res.x/res.y,1.);vec3 c=mix(hex(0xe0b878),hex(0xb9824e),fbm(p*3.));c*=.82+.3*fbm(p*vec2(22.,14.));float r=sin(p.y*46.+3.*fbm(p*4.)+p.x*8.);c*=1.-.14*smoothstep(.4,.9,r);c=mix(c,hex(0x5a3a3a),smoothstep(.75,.2,uv.y)*.25);o=vec4(c,1);}
''')
        L = Light(key=(-.5, .75, -.35), keyCol='#ffe0b0', amb='#7f86b8', rim=(.6, .4, -.7), rimCol=(.9, .7, .4), fogCol='#d0a060', fog=(0, 0, 0, 0), inkRef=.5)
        st.open(cam, L)
        R = eul(6, 0, 0); self.stone(st, V(0, .25, 0), R, 1., up)
        # contact shadow of the stone
        q = self.tip(up); lx = (q[0] / 1400 - .5) * 4.6; lz = (q[1] / 880 - .5) * 2.9; top = R @ V(lx, 1.0, lz) + V(0, .25, 0)
        hover = .10 * abs(math.sin(f * .9)) * (0 < up < 1) * 0 + 1.4 * lift + (.8 * (1 - smooth(0, 4, f)))
        tip = top + V(0, .10 + hover, 0)
        # a right arm with one finger out, reaching in from the upper right
        P = PZ.STAND.set(rh=(-3.2, 8.1, 3.6), rel=(-1, -.2, .2), rhand='point', rfing=(-.2, -.5, .8), rpalm=(.1, -.85, -.5)); sc = 1.0
        S0 = st.fig(ARM, P, draw=False); M = place_hand(S0, 'R', tip, (-.66, -.60, -.30), (-.30, -.45, .85), sc, 'tip1')
        st.fig(ARM, P, M=M, u=dict(side=1, band=2))
        st.close()
        # wet pigment on the finger
        FX.particles(st, np.array([tip + V(0, .04, 0)]), .085, '#c81e14', 'dot')
        if 36 <= f: FX.burst(st, 14, tip - V(0, hover, 0), (f - 36) / 24., speed=1.6, grav=3, size=.03, col='#e0301c', kind='dot', life=.5, up=.6)
        fl = smooth(37, 40, f)
        IM.whip(st, 0, -220 * fl ** 2)
        return st.finish(bloom=.3, vig=.45)

    def water(self, f, st, t):
        u = f - 40
        y = keys(f, [(40, 9.0), (43, 5.4, 'in'), (58, -.6, 'out'), (64, -.95, 'smooth'), (70, -.6, 'smooth'), (84, 7.0, 'in'), (89, 6.15, 'out'), (96, 6.35)])
        surf_y = 5.9; under = 1 - smooth(80, 85, f); glow = keys(f, [(54, 0.), (60, 1.15, 'back'), (70, .85), (84, 1.25), (96, 1.)])
        rollx = keys(f, [(40, -20.), (48, 30., 'out'), (62, 6., 'smooth'), (84, 0.), (90, -6.), (96, 2.)]); rz = keys(f, [(40, 16.), (50, -18., 'out'), (64, -4.), (84, 0.), (89, 8.), (96, -3.)])
        R = eul(-14 + .5 * u, 46 + .8 * rollx, rz)
        depth = smooth(43, 60, f) * (1 - smooth(72, 86, f))
        cy = lerp(2.4, 2.4, 0) + .25 * y; sub = f < 85
        if sub:
            cam = Cam((0.4 * math.sin(f * .05), .25 * y + 1.0, 11.5 - 1.6 * smooth(52, 66, f)), (0, .55 * y + .6, 0), 38, roll=2 * math.sin(f * .07)); st.cam = cam
            st.paint(BELOW, depth=float(depth), open_=0.)
            L = Light(key=(.15, 1, .25), keyCol=(.55, .95, .85), amb=(.06, .20, .24), rim=(-.2, 1, -.3), rimCol=(.6, 1.2, 1.0), envT='#9ff0d8', envM='#2a8a88', envB='#062a34', pts=[((0, y + 1.6, 1.4), 2.4, (.70 * glow, .30 * glow, .08 * glow))] if glow > .02 else [], shadow=False, fogCol='#0b4a52', fog=(.012, 6, 0, 0), inkRef=.5, inkCol='#02141a')
            st.open(cam, L, far=300.); self.stone(st, V(0, y, 0), R, 1., 1., glow, .0); st.close()
            # bubbles: a burst at the plunge, strings after it
            r = np.random.default_rng(2); n = 170; p0 = r.normal(size=(n, 3)) * [1.5, .7, 1.1]; ph = r.uniform(0, 1.3, n); lf = (u / 24. - .10 - ph * .55)
            k = lf > 0; yb = 5.4 - 4.6 * np.minimum(1, ph * 1.0) + np.minimum(lf, 9) * r.uniform(2.2, 4.4, n)
            P = np.c_[p0[:, 0] + .25 * np.sin(lf * 7 + ph * 20), np.minimum(yb, 8.5), p0[:, 2]][k]
            FX.particles(st, P, (r.uniform(.03, .13, n))[k], '#c8fff0', 'ring', alpha=.75); FX.particles(st, P, (r.uniform(.015, .05, n))[k], '#e8fff8', 'ember', alpha=.6)
            if f < 52: FX.burst(st, 120, (0, 5.2, 0), (f - 42) / 24., speed=9, grav=-5, size=.10, seed=8, col='#d8fff4', kind='dot', life=.6, spread=(1.2, .8, .6), drag=4)
            if glow > .05:
                self.glow(st, cam, (0, y + 1., 0), glow)
            # drifting motes
            FX.drift(st, 70, ((-8, -4, -6), (8, 9, 8)), t, kind='ember', size=.05, col='#8fe0c8', fall=-.15, sway=.4, seed=3, spin=0, alpha=.5)
            if f < 46: IM.whip(st, 0, 160 * (1 - smooth(40, 46, f)))
            white = smooth(82, 85, f)
            return st.finish(bloom=.55, thr=.8, vig=.6, contrast=1.08, flash=.75 * white + .35 * (1 - smooth(42, 46, f)) * (f >= 42), flashCol='#dffff4', grain=.015)
        # above the surface: teal morning sea, the stone bobbing with its name alight
        cam = Cam((2.2, surf_y + 3.1, 10.8 - .05 * (f - 85)), (0, surf_y + .35, 0), 36, roll=-2 + 1.2 * math.sin(f * .2)); st.cam = cam
        st.paint('sky.frag', **SKY(None, cZen='#1f5a7a', cMid='#5fb0b0', cHor='#f7d9a0', cLow='#5fa8a0', sunDir=(-.25, .30, -1), sunR=.05, sunCol='#fff4cc', cov=.5, cy0=.03, cy1=.22, cscale=2.2, cLit='#fffaf0', cCM='#d8efe6', cSh='#8fc4c0', cInk='#2a6a70'))
        L = Light(key=(-.35, .6, -.4), keyCol=(.80, .72, .56), amb=(.14, .30, .34), rim=(-.2, .5, -1), rimCol=(.8, .75, .5), envT='#e8fff8', envM='#9fd8cc', envB='#2a7a80', pts=[((0, y + 1.6, 1.4), 2.4, (1.1 * glow, .42 * glow, .10 * glow))], shadow=False, fogCol='#dff2e0', fog=(.006, 30, 0, 0), inkRef=.5)
        st.open(cam, L, far=900.)
        st.world('''
#include "sea.glsl"
#define TMAX 420.
#define STEPS 90
#define RELAX .75
#define NOAO
uniform float sy;uniform float ring;
vec2 map(vec3 p){float r=length(p.xz);float h=seaH(p.xz*1.0,fT*1.1,.30,.62)+.20*sin(r*2.4-ring*9.)*exp(-r*.16)*exp(-ring*1.2)*smoothstep(2.,4.,r);return vec2((p.y-sy-h+.30),1.);}
void surf(vec3 p,vec3 n,int m,inout Surf s){vec3 rd=normalize(p-ro);float r=length(p.xz);float h=p.y-sy+.30;seaPaint(p,n,rd,h,.30,fT,hex(0x07424e),hex(0x167f84),hex(0x5cc0b0),hex(0xf4f4e6),s.base,s.sh);float fo=smoothstep(.45,.15,abs(r-3.3-.30*sin(atan(p.x,p.z)*5.+fT*3.)))*smoothstep(.50,.62,fbm(p.xz*2.5+fT));s.base=mix(s.base,hex(0xf4f2e4),fo*.8);s.cls=8.;s.ink=.5;}
''', u=dict(sy=surf_y - .0, ring=float((f - 85) / 24.)))
        self.stone(st, V(0, y - .62, 0), eul(8 + .1 * u, 34 + .7 * rollx, .7 * rz), 1., 1., glow, 1.)
        st.close()
        self.glow(st, cam, (0, y + .8, .8), glow * .8)
        FX.burst(st, 160, (0, surf_y, 0), (f - 84.5) / 24., speed=8.5, grav=13, size=.12, seed=5, col='#f4fffa', kind='drop', life=.9, spread=(1, .35, 1), up=.9, drag=.7)
        FX.burst(st, 90, (0, surf_y, 0), (f - 84.5) / 24., speed=6.5, grav=12, size=.07, seed=6, col='#fff4d8', kind='dot', life=.8, spread=(1, .3, 1), up=1.1, drag=.7)
        return st.finish(bloom=.45, thr=.95, vig=.35, flash=.6 * (1 - smooth(85, 88, f)), flashCol='#f4fff8')
