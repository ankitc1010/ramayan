"""c7 (84): the empty place.  Rain, almost no colour.  The raw ring where the hut stood, cold ash and one last thread of smoke; Lakshmana with his bow lowered; Rama walks in, finds an anklet, kneels (f24), his hand closes on wet earth (f34), his face (f40-66); the thread of smoke ends (f72)."""
from .c_kit import *
from chars import rama
from chars.armonly import ARM, SKIN, place_hand

ASH = V(16, .9, 20)                                       # the dead hearth
SPOT = V(-3.6, 0, 30.4)                                   # where the anklet lies
GREY = dict(cZen='#39444f', cMid='#55626e', cHor='#93a1aa', cLow='#6a7882', sunGlow=0., sunR=0., rays=0., halo=0., cov=.95, cy0=.05, cy1=.6, cLit='#8b99a3', cCM='#64727d', cSh='#3f4a55', cInk='#252e38', cink=.35, cdrift=.004)
RAINL = dict(key=(-.35, .85, .3), keyCol='#7d8c96', amb='#4c5a68', rim=(.35, .6, -.7), rimCol=(.26, .32, .37), bounceCol=(.03, .04, .05), envT='#b0c0c8', envM='#7a8a94', envB='#39434b', fogCol='#93a1ab', fog=(.0075, 24., .006, 0.), inkRef=1.1, inkCol='#10161c', shadow=False)
EARTH = dict(gA='#6e7074', gB='#42484e', leafA='#5c6658', leafB='#343c3e', rockA='#5c666e', rockB='#333c45')


class Shot(ShotBase):
    id = 'c7'; n = 84
    EVENTS = [(0, 'rain', dict(dur=80)), (2, 'wet footstep', {}), (13, 'wet footstep', {}), (22, 'he stops', {}), (27, 'knee on wet earth', {}), (35, 'hand closes on earth', {}), (40, 'one breath', dict(dur=12)), (54, 'breath breaks', {}), (66, 'rain on ash', dict(dur=12)), (72, 'the smoke ends', {}), (80, 'silence', dict(dur=4))]

    def frame(self, f, st):
        st.clear('#000', f=f); t = st.t
        return self.wide(f, st, t) if f < 32 else self.hand(f, st, t) if f < 40 else self.face(f, st, t) if f < 66 else self.ash(f, st, t)

    def place(self, st, defs='#define NOHUT\n#define NOISLE\n#define NOROCK', **k):
        place.draw(st, TORN.replace('m=U(m,hearth(p));', 'm=U(m,hearth(p));').replace('#ifndef NOHUT\n m=U(m,hearth(p));\n#endif', 'm=U(m,hearth(p));'), u={**tornu(gap=1., depth=13., wet=1., **EARTH), 'tone': .55, **k}, defs=defs, sun=0.)

    def anklet(self, st, at, r=.40):
        th = np.linspace(0, 2 * math.pi, 30); P = at + np.c_[r * np.cos(th), .10 + .10 * np.sin(th + .6), r * np.sin(th)]; st.mesh(*CL.tube(P, .065, 8), kind=0, col=('#c9cdd0', '#4a5056', '#fff'), cls=7, ink=.8)
        B = [CL.sheet(lambda u, v: P[i] + V(0, -.02, 0) + .10 * V(math.cos(u * 6.283) * math.sin(v * 3.1416), math.cos(v * 3.1416), math.sin(u * 6.283) * math.sin(v * 3.1416)), 8, 6) for i in range(0, 30, 3)]
        from chars.jatayu import join
        st.mesh(*join(B), kind=0, col=('#d4c8a8', '#5a544a', '#fff'), cls=7, ink=.7)

    def smoke(self, st, t, at, top, f, w=.10, amt=.9):
        """one thread; after f66 it thins, lets go of the ash and is gone at f72"""
        end = keys(f, [(62, 0.), (69, .35, 'in'), (72, 1.0, 'linear')]); k = np.linspace(end, 1, 46)
        if end >= .99: return
        for j, (aw, sh_) in enumerate(((1., 0.), (.55, .5))):
            P = at + np.c_[((.05 + .75 * k ** 1.2) * np.sin(k * 8.5 - t * 1.5 + sh_) + .30 * k * np.sin(k * 19 - t * 2.6 + sh_ * 3)) * top * .085 * (1 + .6 * k) + .06 * top * k ** 2, top * k, (.4 * k) * np.cos(k * 6 - t * 1.3) * top * .06]; a = amt * aw * (1 - smooth(66, 72, f) * .7)
            FX.ribbon(st, P, w * (.30 + 1.5 * k ** 1.3) * aw, 'smoke', '#c8d2d9', '#7a8892', seed=1.7 + j, amt=a)

    def wide(self, f, st, t):
        g = on2(f); u = f / 31.; cam = Cam(V(30 - 1.0 * u, 4.3 + .1 * u, 28 + .3 * u), V(-14, 7.0, 16.5), 43, roll=0); st.cam = cam
        st.paint('sky.frag', **SKY(None, **GREY)); L = Light(**{**RAINL, 'pts': [(V(10, 13, 32), 16., (.26, .31, .35))]}); st.open(cam, L); self.place(st)
        r = np.random.default_rng(4); k = dict(hazeCol='#9aa8b2', wind=.25, tint=(.50, .55, .60), season='monsoon')
        a = np.r_[np.linspace(3.6, 6.0, 15)]; R = r.uniform(120, 170, 15); FL.scatter(st, 'pahari_round', np.c_[np.sin(a) * R, 0 * a - .3, np.cos(a) * R + 10], 66, seed=1, haze=.62, **k); R = r.uniform(78, 104, 15); FL.scatter(st, 'banyan', np.c_[np.sin(a) * R, 0 * a - .3, np.cos(a) * R + 10][::4], 62, seed=2, haze=.40, **k); FL.scatter(st, 'mango', np.c_[np.sin(a) * R, 0 * a - .3, np.cos(a) * R + 10][1::2], 52, seed=3, haze=.42, **k)
        FL.scatter(st, 'shrub', [(-62, 0, 40), (-66, 0, 8), (-58, 0, -20), (-40, 0, -34), (-50, 0, 62)], 10, seed=5, haze=.22, **k); FL.scatter(st, 'grass', [(-44, 0, 34), (-36, 0, -12), (-40, 0, 2), (-30, 0, 44), (6, 0, 40), (-12, 0, 42)], 5, seed=6, haze=.05, **k)
        # Lakshmana, his back to us
        P = PZ.STAND.set(pel=(.1, 8.2, 0), cher=(0, 9, 0), hedr=(0, 22, 0), lh=(3.0, 7.9, .6), lhand='grip', lfing=(.1, -.5, .85), lpalm=(-1, -.1, 0), rh=(-2.0, 7.7, .4)); SL = st.fig(rama.LAKSHMANA, P, at=(-25.5, 0, 11), yaw=-112)
        st.fig(PR.BOW.variant(u=dict(pr=np.array([1.0, 4.6] + [0] * 14, 'f4'))), M=PR.place(SL.palm('L', .0, .62, .28) + V(0, -1.2, 0), (.10, 1, .30), (0, -.3, 1), 1.)); st.fig(PR.QUIVER, M=PR.place(SL.chest((-.4, -.9, -1.2)), SL.d((.35, 1, -.12)), SL.d((0, 0, -1)), 1.))
        # Rama
        way = V(9.5, 0, -3.2); way = way / np.linalg.norm(way); stand = SPOT - way * 2.6; ph = .10 + g / 24.; at = stand - way * 6.6 * (1 - clamp(g / 22.)) if g < 22 else stand; yaw = math.degrees(math.atan2(way[0], way[2]))
        walk = PZ.walk(ph if g < 22 else .10 + 22 / 24., stride=1.55, lift=.7).set(cher=(0, 8, 0), hedr=(0, 18, 0)); still = PZ.STAND.set(cher=(0, 12, 0), hedr=(0, 30, 0), rf=(-.55, .75, .5), lf=(.55, .75, -.2)); kneel = PZ.KNEEL.set(cher=(0, 24, 0), hedr=(0, 26, 0), lh=(1.2, 5.4, 2.6), rh=(-.9, 2.6, 4.2), rhand='open', rfing=(.1, -.5, .85), rpalm=(0, -1, -.2))
        pose = walk if g < 18 else keys(g, [(18, walk), (22, still), (23, still), (28, kneel.set(pel=(0, 4.5, 0)), 'io'), (30, kneel)])
        S = st.fig(rama.EXILE, pose, at=at, yaw=yaw, face=Face(lid=.6, gy=-.5, sad=.4, smile=-.1)); self.anklet(st, SPOT, .42)
        Q = CL.lag(lambda tt: S.chest((-1.2, 1.2, -.8)), t, n=14, length=6.5, wind=(-.06, 0, 0), grav=1.1, wave=.15, freq=.5); st.mesh(*CL.strip(Q, np.linspace(.6, 1.2, 14), up=(0, .2, 1), m=5, curl=.12, n=30), kind=1, col=('#7a4a3a', '#34242a', '#8a7a5a'), cls=1)
        st.close()
        self.smoke(st, t, ASH + V(0, .6, 0), 17, f, .12)
        rain(st, t, 520, ((-40, 0, -24), (27, 34, 46)), 3, size=.022, length=.9, a=.34); rain(st, t, 60, ((14, 0, 14), (29, 10, 30)), 5, size=.014, length=.6, a=.45)
        self.splash(st, t, 70, ((-30, -2), (24, 44)))
        return st.finish(bloom=.25, thr=.9, vig=.5, contrast=1.04, satu=.50, expo=1.22, sh=(.94, 1., 1.08), fade=.7 * (1 - smooth(0, 4, f)), fadeCol='#10161c')

    def splash(self, st, t, n, box, y=.08, size=.28, seed=2, a=.4):
        r = np.random.default_rng(seed); lo, hi = np.array(box[0], float), np.array(box[1], float)
        ph = r.uniform(0, 1, n) + t * r.uniform(1.6, 2.6, n); c = np.floor(ph); q = ph - c; X = np.modf(np.sin((np.arange(n) * 12.9 + c * 78.2)) * 43758.5)[0]; Z = np.modf(np.sin((np.arange(n) * 39.3 + c * 11.7)) * 24634.6)[0]; P = np.c_[lo[0] + abs(X) * (hi[0] - lo[0]), np.full(n, y), lo[1] + abs(Z) * (hi[1] - lo[1])]
        rr = np.hypot(P[:, 0], P[:, 2] - 4); ok = (rr > 26)
        FX.particles(st, P[ok], (size * (.25 + q))[ok], '#c8d6de', 'ring', alpha=(a * (1 - q))[ok]); FX.particles(st, (P + np.c_[0 * q, .35 * np.sin(q * 3.14), 0 * q])[ok], .045, '#d8e4ea', 'dot', alpha=(a * (1 - q) * 1.4)[ok])

    def hand(self, f, st, t):
        """the hand finds the anklet and closes on wet earth"""
        u = (f - 32) / 7.; g = on2(f); cam = Cam(V(1.0, 4.4 - .2 * u, 5.8 - .3 * u), V(-.1, .55, -.1), 31, roll=-5 + 2 * u); st.cam = cam
        st.paint(MUD, lo=0.)
        L = Light(**{**RAINL, 'key': (-.5, .75, .35), 'fog': (0, 0, 0, 0), 'inkRef': .5, 'ink': 3.4, 'shadow': True, 'keyCol': '#94a2ac'}); st.open(cam, L)
        st.world(MUDW, u=dict(hk=float(smooth(34, 37, f))))
        self.anklet(st, V(-1.25, .12, .15), .62)
        y = keys(g, [(32, 1.15), (34, .46, 'out'), (36, .40), (40, .40)]); hd = 'open' if g < 34 else 'relax' if g < 36 else 'fist'
        P = PZ.STAND.set(rh=(-3.0, 8.4, 3.4), rel=(-1, -.3, 0), rhand=hd, rfing=(0, 0, 1), rpalm=(0, -1, 0)); A = ARM.variant(pal={1: SKIN['rama']}, u=dict(side=1, band=2)); S = st.fig(A, P, draw=False); st.fig(A, P, M=place_hand(S, 'R', V(.35, y + .12 * smooth(35, 37, f), .05), (-.80, -.20 - .30 * smooth(34, 36, f), .42), (-.12, -1, .05), 1.0))
        st.close()
        if f >= 34: FX.burst(st, 16, (.1, .25, .3), (f - 35) / 24., speed=2.2, grav=8, size=.06, seed=4, col='#4a5056', kind='dot', life=.5, up=.6)
        for i in range(9):
            ph = t * 2.1 + i * .37; c, q = math.floor(ph), ph % 1.; p = V(3.6 * math.sin(i * 5.1 + c * 3.3), .06, 2.4 * math.cos(i * 3.3 + c * 2.1)); FX.particles(st, np.array([p]), .10 + .5 * q, '#b8c8d2', 'ring', alpha=.5 * (1 - q))
        rain(st, t, 90, ((-6, 0, -5), (6, 7, 5)), 4, v=(-1.6, -26, 0), size=.010, length=.55, a=.5)
        IM.dof(st, float((V(0, .4, 0) - cam.eye) @ cam.R[2]), 4., 5.)
        return st.finish(bloom=.25, thr=.9, vig=.55, contrast=1.06, satu=.52, expo=1.15, sh=(.94, 1., 1.08))

    def face(self, f, st, t):
        u = (f - 40) / 25.; g = on2(f); brk = smooth(53, 55, f)
        P = PZ.KNEEL.set(pelr=(0, 2, 0), cher=(0, 8, 0), hedr=keys(g, [(40, (4, 13, 0)), (46, (4, 11, 0)), (52, (3, 4, 1), 'io'), (54, (3, 5, 2)), (58, (3, 9, 3)), (66, (3, 13, 3))])); S = st.fig(rama.EXILE, P, yaw=0, draw=False); h0 = st.fig(rama.EXILE, P.set(hedr=(3, 10, 1)), yaw=0, draw=False).head((0, 0, 0))
        cam = Cam(h0 + V(3.0 - .3 * u, -.2, 11.4 - .9 * u), h0 + V(.05, -.02, .3), 17.5, roll=-1.5); st.cam = cam
        st.paint('sky.frag', **SKY(None, **{**GREY, 'cHor': '#7c8a94', 'cov': .7})); st.paint(VEIL, 'over')
        L = Light(**{**RAINL, 'key': (-.45, .6, .65), 'keyCol': '#b0c0ca', 'amb': '#586878', 'rimCol': (.10, .12, .14), 'fog': (0, 0, 0, 0), 'ink': 4., 'inkRef': 1.})
        lid = keys(f, [(40, .42), (46, .46), (51, .80, 'io'), (54, .80), (56, .58), (61, .50), (63, .10, 'io'), (66, .06)]); F = Face(lid=lid, gy=keys(f, [(40, -.7), (46, -.6), (51, .15, 'io'), (56, .10), (66, -.4)]), gx=keys(f, [(40, -.2), (48, .0), (66, 0.)]), sad=.45 + .5 * brk, brow=.15 * brk, smile=-.35 - .20 * brk, mouth=0., tear=0., squint=.25 * brk, frown=0.)
        st.open(cam, L); st.fig(rama.EXILE, P, face=F); st.close()
        # water on the face: drops run down; after f54 one of them starts at the eye
        Rh = S.u['Bh']; fw = S.d(np.array([0, 0, 1.]) @ Rh)
        if f >= 55:
            q = (f - 55) / 11.; x, yy = .37 + .07 * q, -.0 - .74 * ease_in(q, 1.5); w = S.head((x, yy, 1.22 - .12 * q)); tr = np.array([S.head((.37 + .07 * a, -.0 - .74 * ease_in(a, 1.5), 1.22 - .12 * a)) for a in np.linspace(0, q, 14)]); FX.ribbon(st, tr, np.linspace(.004, .020, 14), 'light', '#c8d8e2', '#f4f8fc', amt=1.1); FX.particles(st, np.array([w]), .030, '#e4eef4', 'drop')
        rain(st, t, 110, (tuple(h0 - V(5, 4, 3)), tuple(h0 + V(5, 4, 6))), 5, v=(-1.2, -22, 0), size=.010, length=.5, a=.42); rain(st, t, 160, (tuple(h0 - V(14, 8, 24)), tuple(h0 + V(14, 9, -4))), 6, v=(-1.2, -24, 0), size=.02, length=.8, a=.30)
        IM.dof(st, float((h0 - cam.eye) @ cam.R[2]), 4., 5.)
        return st.finish(bloom=.25, thr=.9, vig=.5, contrast=1.05, satu=.55, expo=1.12, sh=(.94, 1., 1.08))

    def ash(self, f, st, t):
        """cold ash; the thread lets go"""
        u = (f - 66) / 17.; cam = Cam(ASH + V(8.6 - .4 * ease_out(u), 4.4, 6.6 - .3 * ease_out(u)), ASH + V(-.1, 1.35, .5), 36, roll=0); st.cam = cam
        st.paint('sky.frag', **SKY(None, **GREY)); L = Light(**{**RAINL, 'fog': (.030, 12., .0, 0.), 'ink': 3.4, 'inkRef': .6, 'rimCol': (.12, .15, .17)}); st.open(cam, L)
        self.place(st, rockA='#a4b0b8', rockB='#5a656e')
        st.mesh(*CL.sheet(lambda a, b: ASH + V(0, -.9, 0) + V(3.1 * b * math.cos(a * 6.283), 1.05 * (1 - b * b) ** 1.1 + .10 * math.sin(a * 31 + b * 9) * b * (1 - b) + .06 * math.sin(a * 13 - b * 17), 2.7 * b * math.sin(a * 6.283)), 40, 18), kind=0, col=('#c4cacd', '#7a838a', '#fff'), cls=1, ink=.2)
        st.close()
        wet = 1 - smooth(75, 81, f)
        self.smoke(st, t, ASH + V(.3, .30, .4), 4.6, f, .10, 1.2)
        if wet > .01:
            rain(st, t, int(170), (tuple(ASH - V(9, 1, 8)), tuple(ASH + V(9, 10, 8))), 4, v=(-1.6, -26, 0), size=.011, length=.6, a=.42 * wet)
            n = 16
            for i in range(n):
                ph = t * 1.9 + i * .41; c, q = math.floor(ph), ph % 1.; a = i * 2.4 + c * 1.7; rr = 5.2 + 2.8 * abs(math.sin(i * 3.3 + c)); FX.particles(st, np.array([ASH + V(rr * math.sin(a), -.82, rr * math.cos(a))]), .08 + .42 * q, '#b8c8d2', 'ring', alpha=.45 * (1 - q) * wet)
                if i < 6: FX.burst(st, 4, ASH + V(1.6 * math.sin(a * 3), .1, 1.4 * math.cos(a * 5)), q * .35, speed=1.4, grav=6, size=.05, seed=i + int(c) * 7, col='#8a9298', kind='dot', life=.25, up=.8)
        IM.dof(st, float((ASH - cam.eye) @ cam.R[2]), 7., 6.)
        return st.finish(bloom=.2, thr=.9, vig=.55, contrast=1.04, satu=.45, expo=1.15, sh=(.94, 1., 1.08), fade=.25 * smooth(74, 84, f), fadeCol='#0c1216')


MUD = """
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform vec2 res;uniform float lo;void main(){o=vec4(mix(hex(0x2c3238),hex(0x565e66),fbm(uv*vec2(9.,5.))),1);}
"""
MUDW = """
#define TMAX 60.
#define STEPS 100
uniform float hk;
float h(vec2 q){float f=.18*fbm(q*.8+2.)+.07*fbm(q*3.1)-.10;f-=.10*hk*exp(-dot(q-vec2(-.1,.25),q-vec2(-.1,.25))*1.6);f-=.16*smoothstep(.16,.0,abs(length(q-vec2(-1.25,.15))-.62));return f;}
vec2 map(vec3 p){return vec2((p.y-h(p.xz))*.75,1.);}
void surf(vec3 p,vec3 n,int m,inout Surf s){float t=fbm(p.xz*2.2);s.base=mix(hex(0x6c7074),hex(0x3c4248),smoothstep(.3,.7,t));s.sh=s.base*.34;float w=smoothstep(.02,-.015,h(p.xz)-.012);if(w>.5){float rp=.5+.5*sin(length(p.xz-vec2(1.6,-1.2))*9.-fT*10.);s.base=mix(hex(0x5c6c78),hex(0x98a8b2),.35*rp);s.sh=s.base*.6;s.cls=8.;}s.ink=.3;}
"""
VEIL = """
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform vec2 res;uniform float fT;
void main(){vec2 p=uv*vec2(res.x/res.y,1.);float q=0.;vec3 c=vec3(0);float a=0.;for(int i=0;i<3;i++){float f=float(i);float x=p.x*(1.6+f*.7)+f*3.1;float hh=.92-.16*f+.10*fbm(vec2(x*2.,f*3.));float tr=smoothstep(.34,.0,abs(fract(x*1.4)-.5)-.10-.08*f)*.6;float m=smoothstep(.10,-.10,uv.y-hh);vec3 t=mix(hex(0x58656f),hex(0x2c3740),f*.4)*(1.-.25*tr);c=mix(c,t,m*.6);a=max(a,m*.8);}c=mix(c,hex(0x7d8b96),smoothstep(.45,.0,uv.y)*.35);o=vec4(c*a,a);}
"""
