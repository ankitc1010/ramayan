"""f8 (120): the last draw.  Every flame of the film comes to the arrow point: a flash of each on the beat (f6 lamp, f14 wedding fire, f22 line, f30 ring, f38 tail, f46 city).
Close on the point (f48), the eye with the flame in it (f72), then silence (f96-120): one still silhouette against the fire."""
import importlib
from lau.shot import *
from lau.look import *
from chars import rama

# which earlier flame flashes when: (frame here, shot, frame there)
FLASH = [(6, 'a1', 56), (14, 'a5', 20), (22, 'c3', 26), (30, 'd1', 52), (38, 'd7', 45), (46, 'd8', 158)]

BG = '''
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform vec2 res,sun;uniform float fT,heat,silent;
void main(){vec2 p=vec2(uv.x*res.x,(1.-uv.y)*res.y)/res.y;vec2 s=sun/res.y;vec2 q=p-s;float r=length(q),a=atan(q.y,q.x);
 vec3 c=mix(hex(0x2a0812),hex(0x070309),smoothstep(.05,1.15,r));
 float sm=fbm(p*vec2(2.2,3.4)+vec2(fT*.10,-fT*.05))*.65+fbm(p*vec2(6.,9.)-fT*.12)*.35;c=mix(c,hex(0x4a0f14),smoothstep(.42,.75,sm)*smoothstep(1.2,.1,r)*.9);c=mix(c,hex(0x9a2a12),smoothstep(.58,.80,sm)*smoothstep(.95,.05,r)*heat);
 float ray=smoothstep(-.2,.25,sin(a*22.+fT*.25*(1.-silent)))*.6+smoothstep(.2,.5,sin(a*9.-fT*.18*(1.-silent)))*.6;c+=hex(0xff9a3a)*ray*exp(-r*2.3)*.32*heat;
 c+=hex(0xffb45a)*(exp(-r*r*14.)*.55+exp(-r*3.2)*.22)*heat;
 // three rings of petals round the fire, like a mural halo
 for(int i=0;i<3;i++){float R=.36+.105*float(i);float n=28.+10.*float(i);float w=abs(fract(a*n/TAU+.5*float(i)+(1.-silent)*fT*.02*(float(i)-1.))-.5);float d=abs(r-R-.028*cos(w*PI))-.004;c+=hex(0xffc46a)*smoothstep(.004,.0,d)*.42*heat;float b=length(vec2(w*TAU/n*R,r-R-.055));c+=hex(0xffd890)*smoothstep(.008,.003,b)*.55*heat;}
 c*=.9+.16*fbm(uv*vec2(30.,17.));o=vec4(c,1);}
'''


class Shot(ShotBase):
    id = 'f8'; n = 120
    EVENTS = [(0, 'bow drawn', dict(dur=48))] + [(f, 'flame gathers', dict(k=i)) for i, (f, _, _) in enumerate(FLASH)] + [(48, 'point burns', {}), (72, 'eye', {}), (84, 'string creak', {}), (96, 'silence', dict(dur=24)), (108, 'string creak', dict(soft=1))]

    def setup(self, st):
        self.past = {}
        for f, s, g in FLASH:
            try:
                m = importlib.import_module('shots.' + s).Shot(); m.setup(st); m.frame(g, st); t = gl.ctx().texture((st.pw, st.ph), 4, dtype='f2'); fb = gl.ctx().framebuffer([t]); gl.ctx().copy_framebuffer(fb, st.C.fbo); self.past[f] = t
            except Exception as e: print('f8: no flame from', s, repr(e)[:100])

    def hero(self, st, f, cam, light, draw, face, yaw=26, low=0., fire=1.):
        t = f / 24.; st.open(cam, light)
        P = PZ.archer(draw, low); P = P.set(hedr=(72, 2 + 3 * draw, -2))
        S = st.fig(rama.EXILE, P, yaw=yaw, face=face)
        nk, tip, aim = PR.bow_and_arrow(st, S, half=5.2)
        st.fig(PR.QUIVER, M=PR.place(S.chest((.5, .5, -1.2)), S.d((-.35, 1, -.12)), S.d((0, 0, -1)), 1.))
        w = 1 - smooth(92, 100, f)
        for k, (an, ln, wd, col, ph) in enumerate(((lambda tt: S.chest((-1.2, 1.2, -.8)), 10., 1.5, ('#c8431f', '#4a1020', '#f2c24a'), 0.), (lambda tt: S.pelvis((-.6, .5, -.9)), 7.5, 1.1, ('#e8a22c', '#7a3a14', '#b3202a'), 2.), (lambda tt: S.head((-.2, 1.0, -.8)), 4.5, .55, ('#f2ead2', '#a8806a', '#c8431f'), 4.))):
            Q = CL.lag(an, t * w + 3.3 * (1 - w), n=18, length=ln, wind=(-.9, .20 + .06 * k, -.35), grav=.12, wave=1.3 * w + .25, freq=1.0, phase=ph); st.mesh(*CL.strip(Q, np.linspace(wd * .6, wd, 18), up=(0, 1, .3), m=7, curl=.12, n=42), kind=2 if k == 0 else 1, col=col, cls=8, u=dict(rep=(28., 3., 0, 0)))
        st.close()
        return S, nk, tip, aim

    def frame(self, f, st):
        st.clear('#000', f=f); t = st.t
        if f < 48:
            for (g, s, k) in FLASH:
                if g <= f < g + 3 and g in self.past:                                  # three frames of an older flame
                    st.plate(self.past[g], srgb=False, blend=None, scale=1.02 + .02 * (f - g)); IM.zoomblur(st, (960, 540), .05 + .05 * (f - g)); return st.finish(bloom=.6, vig=.5, contrast=1.1)
            return self.wide(f, st, t)
        if f < 72: return self.point(f, st, t)
        if f < 96: return self.eye(f, st, t)
        return self.still(f, st, t)

    def line(self, S):
        nk = S.palm('R', .22, .95, .34); g = S.palm('L', 0, .62, .30); d = np.linalg.norm(g - nk); aim = (g - nk) / d
        return nk, aim, nk + aim * max(5., d + 1.5)

    def tip(self, S): return self.line(S)[2]

    def gathered(self, f): return sum(1. for g, _, _ in FLASH if f >= g) / len(FLASH)

    def wide(self, f, st, t):
        u = f / 47.; G = self.gathered(f); cam = Cam(V(11.5 - 4.2 * ease_io(u), 3.2 + .8 * u, 25 - 5.5 * ease_io(u)), V(2.1, 10.2, 0), 36, roll=-7 + 5 * u); st.cam = cam
        draw = keys(f, [(0, .15), (40, 1., 'io'), (48, 1.04)])
        S = st.fig(rama.EXILE, PZ.archer(draw), yaw=26, draw=False); tipw = self.tip(S); x, y, z = cam.project(tipw)
        st.paint(BG, sun=(float(x), float(y)), heat=float(.12 + .80 * G), silent=0.)
        L = Light(key=(.75, .35, .35), keyCol=tuple(np.array([1.1, .62, .28]) * (.35 + .75 * G)), amb=(.10, .07, .14), rim=(-.7, .5, -.6), rimCol=(1.2, .35, .15), bounceCol=(.2, .06, .03), envT='#ff9a4a', envM='#c8501c', envB='#3a0f1c', pts=[(tipw + V(0, .4, .6), 4.5, tuple(np.array([1.5, .72, .24]) * (.25 + 1.1 * G)))], ink=3.4)
        S, nk, tip, aim = self.hero(st, f, cam, L, draw, Face(frown=.55, smile=-.15, squint=.35, lid=.9, gx=.3, spark=.8 * G))
        # streams of fire from the past: each comes in from the edge it was flashed from
        ang = [2.5, -.5, 1.2, -2.2, .4, 3.6]
        for i, (g, _, _) in enumerate(FLASH):
            if f < g + 2: continue
            a = ang[i] + .25 * math.sin(t + i); far = tip + cam.R.T @ V(math.cos(a) * 20, math.sin(a) * 13 + 2, 8 - 3 * i % 5); age = (f - g - 2) / 24.; k = smooth(0, .28, age)
            c1 = lerp(far, tip, .45) + cam.R.T @ V(-math.sin(a) * 5.5, math.cos(a) * 5.5, 0); P = np.array([(1 - q) ** 2 * far + 2 * q * (1 - q) * c1 + q * q * tip for q in np.linspace(0, k, 40)])
            P += np.c_[.25 * np.sin(np.linspace(0, 9, 40) + t * 9 + i), .25 * np.cos(np.linspace(0, 8, 40) + t * 8 + i), np.zeros(40)] * (1 - np.linspace(0, 1, 40))[:, None]
            FX.ribbon(st, P, np.interp(np.linspace(0, 1, 40), [0, .12, .5, 1], [.05, 1.15, .75, .12]), 'fire', [(1., .9, .7), (1., .8, .6), (1., .55, .4), (1., .5, .6), (1., .75, .4), (1., .7, .35)][i], seed=i * 3.1, amt=.95); FX.ribbon(st, P, np.linspace(.22, .03, 40), 'light', '#ff9a4a', '#fff0c0', amt=.8)
        FX.flame(st, tip, .9 + 1.5 * G, seed=1.3, glow=.5 + 1.0 * G, lean=-.45, calm=1.2)
        FX.embers(st, 120, ((-16, -2, -8), (16, 6, 10)), t, rise=3.4, size=.06, seed=5, life=3., swirl=1.4, wind=(-1.6, 0, 0))
        return st.finish(bloom=.55, thr=.9, vig=.5, contrast=1.10, satu=1.05)

    def point(self, f, st, t):
        u = (f - 48) / 23.; draw = 1.04; S = st.fig(rama.EXILE, PZ.archer(draw), yaw=26, draw=False); nkw, aim, tipw = self.line(S)
        cam = Cam(tipw + V(5.2 - 1.2 * u, -.9 + .4 * u, 6.4 - 1.8 * ease_io(u)), tipw + V(-1.9 + .9 * u, .55, 0), 36, roll=6 - 4 * u); st.cam = cam; x, y, z = cam.project(tipw)
        st.paint(BG, sun=(float(x), float(y)), heat=.75, silent=0.)
        L = Light(key=(.6, .3, .6), keyCol=(.62, .36, .17), amb=(.09, .05, .10), rim=(-.6, .5, -.6), rimCol=(1.0, .4, .15), envT='#ffb060', envM='#d8601c', envB='#4a1420', pts=[(tipw + V(0, .5, .5), 3.2, (.95, .46, .17))], ink=3.6, inkRef=.8)
        S, nk, tip, aim = self.hero(st, f, cam, L, draw, Face(frown=.55, smile=-.15, squint=.35, lid=.9))
        # fire winds round the shaft into the point
        for i in range(3):
            q = np.linspace(0, 1, 60); ph = t * 7 + i * 2.1; Ln = np.linalg.norm(tip - nk); c = nk + aim[None] * (2.2 + (Ln - 2.2) * q)[:, None]; e1 = nz(np.cross(aim, V(0, 1, 0))); e2 = np.cross(e1, aim); r = (.62 * (1 - q) ** .7 + .04)[:, None]
            FX.ribbon(st, c + (np.cos(q * 13 + ph)[:, None] * e1 + np.sin(q * 13 + ph)[:, None] * e2) * r, np.linspace(.04, .16, 60), 'fire', (1., .85, .6), seed=i * 5., amt=.9); FX.ribbon(st, c + (np.cos(q * 13 + ph)[:, None] * e1 + np.sin(q * 13 + ph)[:, None] * e2) * r, .022, 'light', '#ff9a4a', '#fff4d0', amt=.6)
        FX.flame(st, tip - aim * .3, 1.35 + .35 * u, seed=1.3, glow=.8, lean=-.40, calm=1.3)
        FX.embers(st, 60, (tuple(tipw - V(5, 3, 3)), tuple(tipw + V(5, 1, 3))), t, rise=3.0, size=.035, seed=9, life=1.6, swirl=.8)
        return st.finish(bloom=.6, thr=.9, vig=.45, contrast=1.10)

    def eye(self, f, st, t):
        u = (f - 72) / 23.; P = PZ.archer(1.04).set(hedr=(72, 2, -2)); S = st.fig(rama.EXILE, P, yaw=0, draw=False); h = S.head((.16, .02, .7)); fw = S.d(np.array([0, 0, 1.]) @ S.u['Bh']); sd = S.d(np.array([1., 0, 0]) @ S.u['Bh'])
        eye = h + fw * (4.6 - .5 * ease_io(u)) + sd * .9 + V(0, .12, 0); cam = Cam(eye, h + V(0, .05, 0), 21 - 2.2 * u, roll=-3); st.cam = cam
        st.paint(BG, sun=(1700., 420.), heat=.9, silent=0.)
        fk = .85 + .12 * noise1(t * 9, 3)
        L = Light(key=tuple(fw * .6 + sd * .5 + V(0, -.15, 0)), keyCol=(1.0 * fk, .58 * fk, .26 * fk), amb=(.10, .09, .22), rim=tuple(-fw * .3 - sd + V(0, .3, 0)), rimCol=(1.1, .4, .2), envT='#ffb060', envM='#d8601c', envB='#2a1030', pts=[(h + fw * 3.4 + sd * 1.6 + V(0, -.2, 0), 3.2, (1.1 * fk, .5 * fk, .16 * fk))], shadow=False, ink=4.2)
        lid = keys(f, [(72, .95), (80, .92), (84, .70, 'out'), (95, .74)])
        st.open(cam, L); st.fig(rama.EXILE, P, face=Face(lid=lid, frown=.55, squint=.45, smile=-.1, spark=1., gx=.0, gy=.05)); st.close()
        FX.embers(st, 34, (tuple(h - V(2.5, 2, 2.5)), tuple(h + V(2.5, 0, 2.5))), t, rise=1.6, size=.018, seed=2, life=2.)
        IM.shock(st, (960, 540), 0, 1, 0)
        return st.finish(bloom=.5, thr=.95, vig=.6, contrast=1.10)

    def still(self, f, st, t):
        """nothing moves but the flame"""
        u = (f - 96) / 23.; cam = Cam(V(2.6, 6.8, 38 - .6 * u), V(2.4, 8.4, 0), 27); st.cam = cam
        S = st.fig(rama.EXILE, PZ.archer(1.06), yaw=8, draw=False); nkw, aim, tipw = self.line(S); x, y, z = cam.project(tipw)
        st.paint(BG, sun=(float(x), float(y)), heat=1.15, silent=1.)
        L = Light(key=(.9, .2, -.5), keyCol=(.28, .10, .05), amb=(.018, .008, .016), rim=(.9, .25, -.3), rimCol=(2.6, 1.1, .35), bounceCol=(0, 0, 0), envT='#ff8a3a', envM='#8a2a0c', envB='#14050a', pts=[(tipw, 2.2, (1.2, .5, .15))], shadow=False, ink=3.0, air=.0, stip=0.)
        st.open(cam, L); S = st.fig(rama.EXILE, PZ.archer(1.06).set(hedr=(74, 4, -2)), yaw=8, face=Face(frown=.5, squint=.4, lid=.7)); nk, tip, aim = PR.bow_and_arrow(st, S, half=5.4)
        Q = CL.lag(lambda tt: S.chest((-1.2, 1.2, -.8)), 3.3, n=18, length=9., wind=(-.80, -.05, -.25), grav=.30, wave=.7, freq=.25); st.mesh(*CL.strip(Q, np.linspace(.9, 1.7, 18), up=(0, 1, .2), m=7, curl=.12, n=40), kind=1, col=('#c8431f', '#4a1020', '#f2c24a'), cls=8)
        st.close()
        # ground line: a hill of ink
        st.vector(lambda c: (c.set_source_rgb(.012, .004, .008), c.move_to(-10, 1100), c.line_to(-10, 985), c.curve_to(400, 935, 900, 925, 1200, 945), c.curve_to(1500, 962, 1750, 990, 1930, 975), c.line_to(1930, 1100), c.fill()))
        FX.flame(st, tip, 1.9, seed=1.3, glow=1.25, lean=-.05, calm=.55 - .3 * u)
        return st.finish(bloom=.55, thr=.9, vig=.55, contrast=1.12, satu=1.0)
