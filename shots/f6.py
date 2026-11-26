"""f6 (48): macro.  A drop swells on a glowing leaf between Hanuman's fingers and falls on Lakshmana's lips (f12); his eyes open (f24), the dawn in them; his hand closes on Rama's (f34) and sunrise floods the frame with gold."""
from lau.shot import *
from lau.look import *
from lau.rig import HANDS
from chars import rama
from chars.armonly import ARM, HANUMAN_ARM, SKIN, place_hand

LEAF = '''#include "noise.glsl"
in vec3 vp,vn_;in vec2 vuv;
layout(location=0) out vec4 g0;layout(location=1) out vec4 g1;layout(location=2) out vec4 g2;layout(location=3) out vec4 g3;
uniform vec3 ro;uniform mat3 CamR;uniform float far,objId,cls,inkw,part,fT,glow;uniform vec3 cA,cB,cC;
void main(){vec3 n=normalize(vn_),v=vp-ro;if(dot(n,v)>0.) n=-n;float vz=dot(v,transpose(CamR)[2]);gl_FragDepth=clamp(vz/far,0.,1.);
 float u=vuv.x,w=vuv.y*2.-1.;float mid=smoothstep(.085,.03,abs(w));float s=u*9.-abs(w)*2.4;float vein=smoothstep(.16,.04,abs(fract(s)-.5))*smoothstep(1.,.75,abs(w));float net=smoothstep(.05,.01,voro(vec2(u*34.,w*9.)).y);
 float pulse=.5+.5*sin(u*7.-fT*6.);vec3 c=mix(cB,cA,smoothstep(.0,.9,u)*.6+.4*(1.-abs(w)));c=mix(c,cC,clamp(mid+vein*.8+net*.22,0.,1.)*(.65+.35*pulse));c=mix(c,cB*.45,smoothstep(.90,.99,abs(w))*.8);
 g0=vec4(n,vz);g1=vec4(c*(.45+.75*glow),4.+clamp(inkw,0.,.98)*.98);g2=vec4(cB,1);g3=vec4(n,objId*64.+part);}
'''
DROP = '''
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform vec2 res,c;uniform float r,st,amt,fT;
void main(){vec2 p=vec2(uv.x*res.x,(1.-uv.y)*res.y)-c;p.y=-p.y;vec2 q=p/r;float up=max(q.y,0.);float w=1.-.62*smoothstep(0.,1.2+st*1.6,up)*step(0.,q.y);q.y/=mix(1.,1.+st,step(0.,q.y));q.x/=max(w,.12);float d=length(q)-1.;float a=smoothstep(2./r,-2./r,d);
 float h=sqrt(max(0.,1.-dot(q,q)));vec3 n=vec3(q,h);float f=pow(1.-h,2.);vec3 k=mix(hex(0x86c850),hex(0xf4ffb0),smoothstep(-.8,.8,-q.y+.25*q.x));k=mix(k,hex(0xfffbd0)*1.5,smoothstep(.55,.05,length(q-vec2(.10,-.38)))*.9);k=mix(k,hex(0x4a8a3c),f*.6);k+=vec3(1.3)*smoothstep(.20,.12,length((q-vec2(-.36,.40))*vec2(1.,1.5)));k+=vec3(.8)*smoothstep(.09,.05,length(q-vec2(-.10,.62)));
 float g=exp(-dot(p,p)/(r*r*9.))*.55+exp(-length(p)/(r*5.))*.30;vec3 gl=hex(0xd8e070)*g*.7;o=vec4(k*a+gl*(1.-a),a)*amt;}
'''
BACK = '''
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform vec2 res,sun;uniform float fT,dawn,disc,hor;
void main(){vec2 p=vec2(uv.x*res.x,(1.-uv.y)*res.y);vec2 s=(p-sun)/res.y;s.y=-s.y;float r=length(s),a=atan(s.y,s.x);float y=(hor-p.y)/res.y;
 vec3 nt=mix(hex(0x3a3a78),hex(0x0c1034),smoothstep(-.1,.7,y));vec3 gd=mix(hex(0xffc060),hex(0xc85a4a),smoothstep(.0,.7,y));vec3 c=mix(nt,gd,dawn);c*=.90+.16*fbm(uv*vec2(7.,4.));
 float cl=smoothstep(.50,.62,fbm(vec2(uv.x*4.+fT*.05,uv.y*16.)))*smoothstep(0.,.1,y);c=mix(c,mix(hex(0x4a4a90),hex(0xffe0a0),dawn),cl*.45);
 float ray=smoothstep(-.1,.3,sin(a*20.+fT*.5))*.6+smoothstep(.2,.6,sin(a*9.-fT*.3))*.5;c+=hex(0xffb040)*(ray*exp(-r*1.6)*.55+exp(-r*r*7.)*.8)*dawn;c=mix(c,hex(0xfff4d0)*1.4,smoothstep(.215,.205,r)*disc);c+=hex(0xffd070)*disc*(smoothstep(.012,.0,abs(r-.25))+smoothstep(.008,.0,abs(r-.29)))*.7;
 if(y<0.){vec3 g=mix(hex(0x1a1638),hex(0xb04a2c),dawn);g=mix(g,hex(0xffb050),exp(-abs(s.x)*2.2)*exp(y*5.)*dawn*.8);g*=.85+.3*fbm(vec2(uv.x*30.,y*90.));c=g;}
 o=vec4(c,1);}
'''
LAP = '''
#define TMAX 60.
vec2 map(vec3 p){float y=p.y+1.15+.30*sin(p.x*.55+.6)+.10*p.z*step(p.z,0.)*-.0+.16*sin(p.x*1.1+p.z*.9+1.2*sin(p.x*.5-p.z*.6))+.06*sin(p.x*2.3-p.z*2.1);return vec2(y*.6,1.);}
void surf(vec3 p,vec3 n,int m,inout Surf s){s.base=hex(0xd9772a);s.sh=hex(0x5a2420);float st=smoothstep(.08,.04,abs(fract(p.z*.22+.3)-.5));s.base=mix(s.base,hex(0xf0c060),st*.7);s.ink=.2;}
'''


def hand_mix(a, b, t):
    A, B = HANDS[a], HANDS[b]; m = lambda x, y: (np.array(x, float) * (1 - t) + np.array(y, float) * t).tolist()
    return dict(c=m(A['c'], B['c']), sp=m(A['sp'], B['sp']), th=m(A['th'], B['th']))


PINCH = dict(HANDS['pinch'], th=(34, 40), c=[(30, 30, 16), (60, 68, 28), (22, 26, 14), (16, 20, 12), (16, 20, 12)])


class Shot(ShotBase):
    id = 'f6'; n = 48
    EVENTS = [(0, 'drop swells', dict(dur=10)), (10, 'drop falls', {}), (12, 'drop on lips, a bell', {}), (24, 'eyes open, breath', {}), (36, 'hand closes on hand', {}), (34, 'sunrise swell', dict(dur=14))]

    def frame(self, f, st):
        st.clear('#000', f=f); t = st.t
        if f < 15: return self.leaf(f, st, t)
        if f < 30: return self.eyes(f, st, t)
        return self.hands(f, st, t)

    def leaf_mesh(self, st, stem, tip, side, width, t, glow):
        d = tip - stem; L = np.linalg.norm(d); d = d / L; side = nz(side - d * (side @ d)); nn = np.cross(d, side)

        def fn(u, v):
            w = width * math.sin(math.pi * min(1, u ** .8)) ** .8 * (1 - .25 * u); s = v * 2 - 1; c = stem + d * L * u + nn * (.16 * L * math.sin(u * 2.6)); return c + side * w * s + nn * (.35 * w * s * s + .03 * math.sin(u * 22 + s * 3))
        st.mesh(*CL.sheet(fn, 40, 17), kind=0, col=('#b8e858', '#2a7a38', '#fff4b0'), cls=4, ink=.8, frag=LEAF, u=dict(glow=float(glow)))
        return tip

    def leaf(self, f, st, t):
        u = ease_io(f / 14., 1.4); g = on2(f); P = PZ.STAND; kw = dict(at=V(-14.45, 0, 0), yaw=-90, pitch=-90); S = st.fig(rama.LAKSHMANA, P, draw=False, **kw); lips = S.head((0, -.60, .93)); hc = S.head((0, 0, 0))
        tip = lips + V(-.05, .88 + .03 * math.sin(t * 4), .05); cam = Cam(hc + V(-2.2 + .5 * u, 2.0, 8.4 - .6 * u), lips + V(.74, .60, -.1), 27, roll=-3); st.cam = cam
        fall = clamp((f - 10) / 2.); dp = lerp(tip - V(0, .10, 0), lips + V(0, .06, 0), fall ** 2); hit = smooth(12, 14, f)
        st.paint(BACK, sun=(300., 900.), dawn=.10 + .10 * hit, disc=0., hor=1400.); IM.defocus(st, 6)
        gl_ = 1.0 - .25 * smooth(10, 13, f); pts = [(tip + V(.2, .5, .7), 1.9, tuple(np.array([.46, .52, .20]) * gl_)), (dp + V(0, .05, .35), 1.2, tuple(np.array([.62, .62, .28]) * (.35 + .8 * hit)))]
        L = Light(key=(-.55, .45, .55), keyCol=(.26, .25, .42), amb=(.14, .13, .26), rim=(.5, .7, -.4), rimCol=(.75, .65, .75), bounceCol=(.10, .05, .03), envT='#c8e0a0', envM='#8a8a9a', envB='#4a2a3a', pts=pts, shadow=False, ink=3.6, inkRef=.5, inkCol='#080612')
        st.open(cam, L); st.world(LAP); st.fig(rama.LAKSHMANA, P, face=Face(lid=.0, smile=.05, sad=.1), **kw)
        stem = tip + V(.62, .66, .05); self.leaf_mesh(st, stem, tip, V(.35, -.45, .85), .36, t, gl_)
        Q = CL.spline(np.array([stem + V(.24, .34, 0), stem + V(.12, .17, 0), stem, stem + (tip - stem) * .25]), 16); st.mesh(*CL.tube(Q, np.linspace(.06, .03, 16), m=8), kind=0, col=('#7ac850', '#1c5a30', '#7ac850'), cls=1)
        Ph = PZ.STAND.set(rh=(-3.2, 8.6, 3.4), rel=(-1, -.2, 0), rhand=PINCH, rfing=(0, .1, 1), rpalm=(0, -1, 0)); Sh = st.fig(HANUMAN_ARM, Ph, draw=False); tr = .02 * math.sin(f * 1.1)
        grip = stem + V(.12, .16 + tr, .0); M = place_hand(Sh, 'R', grip, (-.90, -.10, .34), (.22, -.90, .36), .92, 'tip1'); T = [(M @ np.append(Sh.u['HF'][20 + k * 4 + 3, :3], 1))[:3] for k in (0, 1)]; M[:3, 3] += grip - (T[0] + T[1]) / 2; st.fig(HANUMAN_ARM, Ph, M=M); st.close()
        FX.particles(st, (tip + V(.4, .5, .1))[None], 2.0, '#d8e878', 'ember', alpha=.22 * gl_)
        x, y, z = cam.project(dp); rr = cam.px(dp) * (.06 + .115 * smooth(0, 10, f)) * (1 - .2 * fall)
        if f <= 12: st.paint(DROP, 'over', c=(float(x), float(y)), r=float(rr), st=float(.55 * smooth(5, 10, f) if fall == 0 else 1.3 * (1 - hit)), amt=1.)
        if f >= 12:
            k = (f - 12) / 24.; FX.particles(st, (lips + V(0, .1, .1))[None], (.5 + 12 * k), '#f4f0b0', 'ring', alpha=max(0., .40 - 2.6 * k)); FX.particles(st, (lips + V(0, .1, .1))[None], 1.5, '#f0f0a0', 'glint', alpha=.8 - 3 * k); FX.burst(st, 22, lips + V(0, .12, 0), k, speed=2.4, grav=4, size=.035, seed=3, col='#e8ffb8', kind='ember', life=.5, up=.9)
        FX.embers(st, 26, (tuple(tip - V(1.5, .6, .6)), tuple(tip + V(2., 1.2, .8))), t, rise=.5, size=.035, seed=4, life=2.2, col='#c8ff8a', swirl=.3)
        IM.dof(st, float((lips - cam.eye) @ cam.R[2]), 4.5, 6.)
        return st.finish(bloom=.55, thr=.8, vig=.55, contrast=1.06, satu=1.02)

    def eyes(self, f, st, t):
        """close on the face: the light runs up it from the lips, and the eyes open with the dawn in them"""
        u = ease_io((f - 15) / 14., 1.3); P = PZ.STAND.set(hedr=(0, 0, 0)); S = st.fig(rama.LAKSHMANA, P, draw=False); h = S.head((0, 0, .4)); lips = S.head((0, -.60, .95))
        cam = Cam(h + V(-1.5 + .3 * u, .55, 6.9 - .8 * u), h + V(.10, -.02 + .04 * u, 0), 24, roll=-24 + 3 * u); st.cam = cam; dn = smooth(18, 29, f); up = smooth(15, 22, f)
        st.paint(BACK, sun=(1750., 300.), dawn=.22 + .78 * dn, disc=0., hor=1500.); IM.defocus(st, 14)
        wv = h + V(0, -1.2 + 2.1 * up, 1.6); k = 1 - .55 * smooth(22, 29, f)
        L = Light(key=(.75, .42, .55), keyCol=tuple(lerp(np.array([.20, .20, .36]), np.array([1.15, .80, .46]), dn)), amb=tuple(lerp(np.array([.16, .15, .30]), np.array([.34, .22, .24]), dn)), rim=(.8, .5, -.4), rimCol=tuple(np.array([1.2, .75, .35]) * (.15 + .9 * dn)), bounceCol=(.14, .06, .03), envT='#ffe0a0', envM='#ffb060', envB='#7a3a2a', pts=[(wv, 1.5, tuple(np.array([.62, .58, .24]) * k))], shadow=False, ink=4.0, inkCol='#0c0508')
        lid = keys(f, [(15, 0.), (21, 0.), (23, .10), (26, .92, 'out'), (27, .80), (29, .96)]); sk = smooth(24, 28, f)
        st.open(cam, L); st.fig(rama.LAKSHMANA, P, face=Face(lid=lid, spark=sk, smile=.10 + .25 * smooth(25, 29, f), sad=.15 * (1 - dn), gx=.35 * smooth(26, 29, f), gy=.1))
        # Rama's hand under his head
        Pr = PZ.STAND.set(rh=(-3.0, 8.4, 3.4), rel=(-1, -.3, 0), rhand='cup', rfing=(0, .1, 1), rpalm=(0, 1, 0)); Sr = st.fig(ARM, Pr, draw=False); M = place_hand(Sr, 'R', h + V(-1.30, -.95, -1.55), (.10, .92, .30), (.90, .05, .40), 1.15); st.fig(ARM, Pr, M=M, u=dict(side=1, band=2)); st.close()
        for i in range(3):                                                  # the drop's light climbing
            q = (f - 13 - 2.2 * i) / 9.
            if 0 < q < 1: FX.particles(st, (lips + V(0, .9 * q, .25))[None], .3 + 2.0 * q, '#f4f0a0', 'ring', alpha=.16 * (1 - q))
        if sk > 0:
            for sd in (-1, 1): FX.particles(st, S.head((.36 * sd, .02, .98))[None], .55 * sk, '#ffc860', 'glint', alpha=.55 * sk * (1 - .4 * smooth(27, 29, f)))
        FX.drift(st, 40, (tuple(h - V(4, 3, 4)), tuple(h + V(4, 3, -.6))), t, kind='ember', size=.040, col='#ffd890', fall=-.5, sway=.4, seed=3, alpha=.35 + .5 * dn)
        IM.dof(st, float((S.head((0, 0, .8)) - cam.eye) @ cam.R[2]), 3.2, 6.)
        return st.finish(bloom=.5 + .2 * dn, thr=.85, vig=.5, contrast=1.06, satu=1.04)

    def hands(self, f, st, t):
        """his hand closes on his brother's; behind them the sun comes over the plain until there is nothing but gold"""
        u = (f - 30) / 17.; g = on2(f); rise = ease_out(u, 1.5); cl = keys(g, [(30, 0.), (32, -.12), (36, 1.12, 'in'), (38, 1., 'out')]); sq = .05 * impulse((f - 36) / 24., 9)
        cam = Cam(V(-1.1 + .3 * u, 2.1 - .2 * u, 9.6 - .9 * ease_io(u)), V(.05, .55, 0), 25, roll=2); st.cam = cam; sun = (980., 560. - 190. * rise); st.paint(BACK, sun=sun, dawn=1., disc=1., hor=640.)
        L = Light(key=(.10, .75, -.35), keyCol=(1.25, .88, .50), amb=(.40, .24, .26), rim=(.05, .7, -.7), rimCol=(2.0, 1.3, .55), bounceCol=(.25, .11, .05), envT='#fff0c8', envM='#ffc060', envB='#a85030', pts=[(V(0, 1.6, 2.6), 3.2, (.34, .22, .10))], shadow=True, ink=3.8, inkRef=.6, inkCol='#12060a')
        st.open(cam, L)
        Pa = PZ.STAND.set(lh=(3.2, 8.4, 3.4), lel=(1, -.3, 0), lhand=hand_mix('flat', 'cup', .25 + .85 * clamp(cl)), lfing=(0, .1, 1), lpalm=(0, 1, 0)); Sa = st.fig(ARM, Pa, draw=False); Ma = place_hand(Sa, 'L', V(.10, .05 - sq, 0), (.95, .12, .10), (-.10, .92, .36), 1.12); st.fig(ARM, Pa, M=Ma, u=dict(side=0, band=2))
        Pb = PZ.STAND.set(rh=(-3.2, 8.4, 3.4), rel=(-1, -.3, 0), rhand=hand_mix('relax', 'hold', max(-.35, min(1.15, cl)) * .95), rfing=(0, .1, 1), rpalm=(0, -1, 0)); Sb = st.fig(ARM, Pb, draw=False); down = lerp(.62, .30, clamp(cl)); Mb = place_hand(Sb, 'R', V(.02, .22 + down, .20), (-.92, -.10 - .10 * clamp(cl), .30), (.05, -.95, -.20), 1.12); st.fig(ARM.variant(pal={1: SKIN['gold']}), Pb, M=Mb, u=dict(side=1, band=1)); st.close()
        if f >= 36: FX.burst(st, 34, (.2, .7, .4), (f - 36) / 24., speed=3.2, grav=-.6, size=.05, seed=4, col='#ffe0a0', kind='ember', life=.8, up=.6)
        FX.embers(st, 60, ((-4, -1.5, -2), (4, .5, 2)), t, rise=1.5, size=.035, seed=6, life=2.4, col='#ffd070')
        x, y = sun; IM.zoomblur(st, (x, y), .03 + .12 * smooth(41, 47, f)); fl = ease_in((f - 37) / 9.5, 1.25)
        st.paint('''
in vec2 uv;out vec4 o;uniform vec2 res,c;uniform float k;void main(){vec2 p=(vec2(uv.x*res.x,(1.-uv.y)*res.y)-c)/res.y;float r=length(p);float R=-.5+2.3*k;float a=1.-smoothstep(R-.35,R+.45,r);vec3 q=mix(vec3(1.,.56,.12),vec3(1.,.80,.36),smoothstep(.9,0.,r));o=vec4(q*a,a);}
''', 'over', c=tuple(map(float, sun)), k=float(fl))
        return st.finish(bloom=.55 + .2 * fl, thr=.85, vig=.45 * (1 - fl), contrast=1.05, satu=1.05)
