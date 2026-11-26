"""d1 (84): a rainy hill.  Rama's hand lays a ring in Hanuman's great palm (f24); deep in the ruby a spark wakes (f42); Hanuman's lowered eyes open with it (f54-84)."""
from lau.shot import *
from lau.look import *
from chars.armonly import ARM, HANUMAN_ARM, place_hand
from chars import hanuman as HM

RAIN_BG = '''
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform vec2 res;uniform float fT,warm;uniform vec2 c;
void main(){vec2 p=uv*vec2(res.x/res.y,1.);vec3 q=mix(hex(0x1c2832),hex(0x5a6e78),smoothstep(.0,1.15,uv.y+.25*(fbm(p*1.6)-.5)));
 float tr=0.;for(int i=0;i<3;i++){float f=float(i);float x=p.x*(1.3+f*.6)+f*3.7;float h=.30+.24*f+.20*fbm(vec2(x*1.2,f))+.05*fbm(vec2(x*7.,f));float m=smoothstep(.06,-.06,uv.y-h*.62-.02);vec3 t=mix(hex(0x0f1f1e),hex(0x2f4644),f*.42);q=mix(q,t,m*(1.-.28*f));}
 float s=0.;for(int i=0;i<3;i++){float f=float(i);vec2 r=p*vec2(34.+22.*f,1.5+.5*f);r.x+=r.y*1.3;r.y+=fT*(3.2+f*1.1);vec2 id=floor(r);float h=h21(id+f*17.);float w=fract(r.x)-.5;s+=step(.86,h)*smoothstep(.16,.0,abs(w))*smoothstep(0.,.3,fract(r.y))*smoothstep(1.,.5,fract(r.y))*(.34-.07*f);}
 q+=hex(0xb8d0da)*s*.55;vec2 d=vec2(uv.x*res.x,(1.-uv.y)*res.y)-c;float rr=length(d)/res.y;q+=hex(0xff8a3a)*exp(-rr*rr*9.)*.30*warm;o=vec4(q,1);}
'''


def rain(st, t, n=150, seed=3, box=((-9, -3, -6), (9, 8, 6)), col='#c8dce6', a=.5):
    r = np.random.default_rng(seed); lo, hi = np.array(box, float); P = r.uniform(0, 1, (n, 3)) * (hi - lo); v = V(-2.0, -15.5, 0); P = lo + np.mod(P + v * t * r.uniform(.8, 1.2, (n, 1)), hi - lo)
    FX.particles(st, P, r.uniform(.006, .014, n), col, 'rain', vel=np.tile(nz(v) * .62, (n, 1)), alpha=a)


class Shot(ShotBase):
    id = 'd1'; n = 84
    EVENTS = [(0, 'rain', dict(dur=84)), (24, 'ring on palm', {}), (42, 'spark wakes', {}), (58, 'eyes open', {}), (60, 'heartbeat', {}), (72, 'heartbeat', {}), (78, 'fist closes', {})]

    def frame(self, f, st):
        st.clear('#000', f=f)
        return self.hands(f, st, st.t) if f < 54 else self.face(f, st, st.t)

    def hands(self, f, st, t):
        g = on2(f); push = ease_io((f - 30) / 23., 2.0) if f > 30 else 0.
        palm = V(.25, 0, .2); ring = palm + V(.0, .42, .05); sp = keys(f, [(41, 0.), (43, 1.35, 'out'), (47, .85), (54, 1.1)]) if f > 41 else 0.
        eye = lerp(V(1.4 - .010 * f, 6.8 - .012 * f, 9.6), ring + V(.35, 1.55, 2.35), push); at = lerp(V(.35, .35, .1), ring + V(0, .12, 0), push); cam = Cam(eye, at, lerp(23, 27, push), roll=lerp(-4, 2, push)); st.cam = cam
        x, y, z = cam.project(ring); st.paint(RAIN_BG, warm=float(sp), c=(float(x), float(y)))
        L = Light(key=(-.35, .85, .25), keyCol=(.50, .60, .68), amb=(.16, .21, .27), rim=(.7, .5, -.6), rimCol=(.45, .62, .75), bounceCol=(.03, .04, .05), envT='#c8dce8', envM='#6a7f8c', envB='#1c262e', pts=[(ring + V(0, .55, .2), 1.25, tuple(np.array([1.6, .72, .24]) * sp))] if sp > 0 else [], shadow=True, ink=3.4, inkRef=.6)
        st.open(cam, L)
        P = PZ.STAND.set(rh=(-3.0, 8.2, 3.4), rel=(-1, -.3, 0), rhand='cup', rfing=(0, .1, 1), rpalm=(0, 1, 0), lh=(3.0, 8.2, 3.4))
        S = st.fig(HANUMAN_ARM, P, draw=False); sink = -.10 * impulse((g - 24) / 24., 6); M = place_hand(S, 'R', palm + V(0, sink - .22, 0), (.97, .05, .26), (-.10, 1, .22), 1.32); st.fig(HANUMAN_ARM, P, M=M)
        # the giving hand
        d = keys(g, [(0, (4.6, 5.2, -1.2)), (20, (1.05, 1.75, -.35), 'io'), (24, (.80, 1.28, -.22), 'io'), (28, (.95, 1.55, -.25)), (40, (5.6, 5.6, -2.2), 'in')])
        hand = 'pinch' if g < 25 else 'open'; Pr = PZ.STAND.set(rh=(-3.0, 8.4, 3.2), rel=(-1, -.3, 0), rhand=hand, rfing=(0, 0, 1), rpalm=(0, -1, 0)); Sr = st.fig(ARM, Pr, draw=False); fing = nz(V(-.72, -.58, .38)); pw = palm + np.array(d)
        Mr = place_hand(Sr, 'R', pw, fing, (-.45, -.55, .70) if g < 25 else (-.30, -.80, .5), 1.0); st.fig(ARM, Pr, M=Mr)
        rp = ring + V(0, sink, 0) if g >= 24 else pw + V(-.72, -.52, .55); spin = 0 if g >= 24 else .3 * math.sin(g * .4)
        yv = nz(V(.10 + spin, .80, .62)) if g >= 24 else nz(V(.2 + spin, .9, .4))
        st.fig(PR.RING, M=PR.place(rp, yv, V(.96, -.10, -.2), .40)); st.close()
        gem = rp + yv * .40 * 1.42
        if sp > 0:
            FX.flame(st, gem - V(0, .10, 0), .34 * min(sp, 1.15), seed=1.3, glow=.9 * sp, calm=1.2); FX.particles(st, gem[None], .55 * sp, '#ffb050', 'glint', alpha=.7)
            if f < 60: FX.burst(st, 16, gem, (f - 42) / 24., speed=1.6, grav=1., size=.018, seed=4, col='#ffc060', life=.5, up=.5)
        if 24 <= f < 40: FX.burst(st, 18, ring, (f - 24) / 24., speed=2.0, grav=5, size=.03, seed=6, col='#d8e8f0', kind='drop', life=.5, up=.8)
        # drops striking the palm
        for k in range(7):
            ph = (t * 1.6 + k * .37) % 1.; q = palm + V(1.7 * math.sin(k * 5.1 + math.floor(t * 1.6 + k * .37) * 3.3), .42, 1.0 * math.cos(k * 3.3 + math.floor(t * 1.6 + k * .37) * 2.1))
            if ph < .35: FX.burst(st, 6, q, ph * .6, speed=1.5, grav=7, size=.022, seed=k, col='#cfe2ec', kind='dot', life=.25, up=.9)
        rain(st, t, 130, 3, ((-7, -2, -4), (7, 7, 7)))
        IM.dof(st, float((ring - cam.eye) @ cam.R[2]), 4.5, 6.)
        return st.finish(bloom=.45, thr=.9, vig=.5, satu=.85 + .25 * min(sp, 1), contrast=1.06, fade=.9 * (1 - smooth(0, 5, f)), fadeCol='#0a1016')

    def face(self, f, st, t):
        u = (f - 54) / 29.; g = on2(f); P = HM.H_KNEEL_PALM.set(hedr=keys(g, [(54, (0, 30, 0)), (62, (0, 26, 0)), (74, (0, 4, 0), 'io'), (84, (0, 2, 0))])); S = st.fig(HM.HANUMAN, P, draw=False); h = S.head((0, .05, .5)); fw = S.d((0, 0, 1))
        eye = S.head((0, 0, 0)) + fw * (9.2 - .9 * ease_io(u)) + V(1.0 - .3 * u, -.35, 0); cam = Cam(eye, S.head((0, 0, 0)) + V(0, .10, .2), 22, roll=-2); st.cam = cam; st.paint(RAIN_BG, warm=.55, c=(960., 1000.))
        fk = 1 + .10 * noise1(t * 8, 4); src = h + fw * 1.6 + V(0, -2.3, 0)
        L = Light(key=(-.35, .85, .25), keyCol=(.42, .50, .58), amb=(.15, .19, .26), rim=(.7, .5, -.6), rimCol=(.55, .75, .9), bounceCol=(.22, .08, .02), envT='#c8dce8', envM='#8a6a50', envB='#ff9a4a', pts=[(src, 2.6, (1.0 * fk, .46 * fk, .16 * fk))], shadow=False, ink=3.6)
        lid = keys(f, [(54, .05), (58, .08), (63, .62, 'out'), (66, .55), (72, 1.0, 'io'), (84, 1.0)]); sk = smooth(60, 70, f)
        st.open(cam, L); st.fig(HM.HANUMAN, P, face=Face(lid=lid, spark=sk, smile=.15 + .25 * smooth(72, 82, f), frown=.15 * smooth(70, 80, f), gy=-.35 * (1 - smooth(64, 74, f)))); st.close()
        # drops run from the brow and catch the warm light
        rain(st, t, 120, 5, (tuple(h + V(-4, -4, -2)), tuple(h + V(4, 4, 5))), a=.45); FX.embers(st, 16, (tuple(src - V(1, .2, .6)), tuple(src + V(1, .4, .6))), t, rise=1.3, size=.02, seed=3, life=1.8)
        IM.dof(st, float((h - cam.eye) @ cam.R[2]), 6., 6.)
        return st.finish(bloom=.5, thr=.9, vig=.55, satu=1.0, contrast=1.08)
