"""c4 (96): the great shadow.  A mendicant at the burning line; the fire throws his shadow up the rock and the shadow tells the truth: a head on every beat from f36, the wheel of arms from f54.
Sita looks up (f78); her foot crosses (f84); the line dies along its length (f90) and the shadow is everywhere."""
from .c_kit import *
from chars import people as PE, sita as SI

MAN = V(13.0, 0, 30.6)                 # the mendicant, just outside the line
WALL = V(29., 0, -48.)                 # where his shadow stands on the rock
CROSS = .545                           # where her foot crosses, as a fraction of the line
WALK = [(0, (1.0, 0., 18.4)), (72, (5.2, 0., 24.9))]
HOLD = dict(lh=(.62, 9.35, 2.15), rh=(-.62, 9.35, 2.15), lel=(1, -.6, -.5), rel=(-1, -.6, -.5), lhand='cup', rhand='cup', lfing=(-.75, .05, .65), rfing=(.75, .05, .65), lpalm=(-.15, 1, -.1), rpalm=(.15, 1, -.1))

EYE = (.327, .041, .65, .112)            # her irises in head units: out, up, forward, radius
INTERIOR = '''
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform vec2 res;uniform float fT,fk;
void main(){vec2 p=uv*vec2(res.x/res.y,1.);vec2 q=p*7.;float k=step(.5,fract(q.x*.5+.5*step(.5,fract(q.y*.25))));float w=.5+.5*sin(q.y*9.+3.14*k);vec3 c=mix(hex(0x2a0e14),hex(0x6a2c18),w*.35+.3*fbm(p*2.));c*=mix(1.5,.35,smoothstep(0.,1.05,uv.y))*fk;c+=hex(0xff7a24)*.22*exp(-uv.y*4.)*fk;o=vec4(c,1);}
'''
REFLECT = '''
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform sampler2D tS;uniform vec2 res,c;uniform float r,k,fT,lidy;
void main(){vec2 p=(vec2(uv.x*res.x,(1.-uv.y)*res.y)-c)/r;float d=length(p);vec2 q=vec2(p.x,-p.y);vec2 u=vec2(.5,.52)+vec2(q.x*.46,q.y*.44)*(1.+.22*d*d);float s=smoothstep(.2,.8,textureLod(tS,u,2.).r);
 vec3 w=mix(hex(0xd8501a),hex(0xff9a3a),smoothstep(.7,-.5,q.y));vec3 b=mix(w,vec3(.015,.006,.012),s);float f=smoothstep(.05,.0,q.y+.62+.12*vn(vec2(q.x*7.,fT*6.)));b=mix(b,vec3(1.7,1.1,.4),f);b*=.45+.75*smoothstep(1.,.2,d);
 b+=vec3(.9)*smoothstep(.17,.12,length(p-vec2(-.36,-.42)));float a=smoothstep(.96,.88,d)*k*smoothstep(-.62,-.50,p.y);o=vec4(b*a,a);}
'''


class Shot(ShotBase):
    id = 'c4'; n = 96
    EVENTS = [(0, 'fire burns low', dict(dur=90)), (0, 'evening insects', dict(dur=36))] + [(f, 'soft footstep', {}) for f in (12, 36, 60)] + [(f, 'a head slides out of the shadow', dict(k=i)) for i, f in enumerate((36, 42, 48, 54, 60, 66, 72))] + \
             [(54, 'twenty arms open', dict(dur=22)), (58, 'shadow swords ring', {}), (78, 'she looks up', {}), (86, 'bare foot on earth', {}), (87, 'flames shiver', {}), (90, 'the line goes out', dict(dur=5)), (91, 'ten pairs of eyes kindle', {}), (93, 'silence', dict(dur=3))]

    def setup(self, st):
        self.T = Theatre(st, dict(man=lambda: st.fig(PE.MENDICANT, PE.P_STAFF, yaw=172, u=dict(staff=0.))))

    def frame(self, f, st):
        st.clear('#000', f=f)
        return self.wide(f, st, st.t) if f < 78 else self.eyes(f, st, st.t) if f < 84 else self.foot(f, st, st.t) if f < 90 else self.wide(f, st, st.t)

    def sita(self, st, f, g, t):
        at = V(*keys(g, WALK, 'linear')); ph = min(g, 72) / 48.; stop = smooth(66, 74, g)
        P = SI.S_WALK(ph).mix(SI.S_STAND.set(rf=(-.4, .75, .2), lf=(.45, .75, .1)), stop).set(hedr=(0, 20, 0), **HOLD)
        F = Face(lid=.32, gy=-.5, smile=.22)
        if f >= 90: at = V(6.2, 0, 27.0); P = SI.S_STEP.set(hedr=(0, -14, 0), **HOLD); F = Face(lid=1., gy=.5, smile=-.1, sad=.5, brow=.4)
        S = st.fig(SI.FOREST, P, at=at, yaw=24, face=F); bowl(st, (S.palm('L') + S.palm('R')) / 2 + V(0, .62, 0), .82); return S

    def wide(self, f, st, t):
        g = on2(f); after = f >= 90; u = min(f, 78) / 78.; w = max(0., (f - 90) / 5.); tex = shadow_at(self.T, g if not after else 90)
        out = ease_out((f - 90) / 4.5, 1.6) if after else 0.; loom = smooth(50, 76, f)
        cam = Cam(V(26 - 2.5 * u, 7 - .6 * u, 101 - 6.5 * u - 2 * w), V(11 + 1. * u, 32 + 1.5 * u, -30), 40, roll=-1.2 * loom); st.cam = cam
        st.paint('sky.frag', **SKY(None, **{**DUSKSKY, 'cHor': tuple(np.array(hexc('#d8541c')) * (1 - .6 * out))}))
        fk = (.92 + .08 * noise1(t * 9, 2) + .05 * noise1(t * 21, 5)) * (1 - out)
        N = nz((WALL - MAN) * V(1, 0, 1)); X = np.cross(N, V(0, 1, 0)); fire = MAN - N * (28. - 5.5 * loom) + V(.5 * noise1(t * 6, 1), 1.6 + .25 * noise1(t * 5, 7), 0)
        L = Light(**{**DUSKL, 'pts': [(MAN + V(-1.5, 2.0, -3.2), 7., (1.1 * fk, .44 * fk, .12 * fk)), (line_point(.48, y=2.), 8., (1.0 * fk, .40 * fk, .11 * fk))]})
        st.open(cam, L)
        place.draw(st, LITBY, u=placeu(line=1., lineC=CROSS, lineK=.56 * out if after else -1., rockH=112., lineG=.30, fireP=tuple(fire), shO=tuple(MAN), shX=tuple(X), shN=tuple(N), shBox=(UX, UY, UW, UH), fireI=1.65 * fk, shK=1., hutK=lerp(1., .30, smooth(38, 56, f)), lean=2.9 * loom, dusk=float(out), eyes=float(.9 * smooth(90, 93, f)), fireC=(1., .40, .10), shTint=lerp(np.array((.30, .20, .34)), np.array((.22, .20, .42)), out), hot=(28., 52., 92.)), texs=dict(tShad=tex), sun=0.)
        trees(st, far=False, right=False, near=False, tint=tuple(np.array((.50, .40, .46)) * (1 - .45 * out)))
        FL.scatter(st, 'shrub', [(-58, 0, -6), (70, 0, -14), (96, 0, -22), (62, 0, -30)], 10, season='summer', seed=9, tint=(.42, .34, .42), hazeCol='#3a2448', haze=.05, wind=.5); FL.scatter(st, 'grass', [(-40, 0, 24), (-34, 0, 40), (58, 0, 26), (47, 0, 38), (64, 0, 44)], 6, season='summer', seed=10, tint=(.36, .28, .36), hazeCol='#3a2448', haze=0., wind=.5)
        d = V(3, 0, 20) - MAN; yaw = math.degrees(math.atan2(d[0], d[2]))
        st.fig(PE.MENDICANT, PE.P_STAFF, at=MAN, yaw=yaw, face=Face(lid=.3))
        self.sita(st, f, min(g, 78), t)
        st.close()
        if out < 1: line_fire(st, t, 0., CROSS - .56 * out if after else 1., h=2.1 * (1 - .5 * out))
        if after and out < 1: line_fire(st, t, CROSS + .56 * out, 1., h=2.1 * (1 - .5 * out), seed=2)
        FX.embers(st, 70, ((-24, 0, 14), (24, 2, 30)), t, rise=5., size=.09 * (1 - .6 * out), seed=4, life=2.8, swirl=1.4)
        if after:                                                                         # threads of smoke where the line was
            for i in range(13):
                x = (CROSS + (i - 6) * .052); q = clamp((out * .56 - abs(x - CROSS)) * 8)
                if q > 0: p0 = line_point(x); k = np.linspace(0, 1, 18)[:, None]; FX.ribbon(st, p0 + k * V(.6, 5. * q + (i % 3), 0) + np.c_[.5 * np.sin(k[:, 0] * 5 - t * 6 + i), 0 * k[:, 0], 0 * k[:, 0]] * k, np.linspace(.10, .55, 18), 'smoke', '#8a7a9a', '#40304a', seed=i * 3., amt=.5 * q)
        beat = sum(impulse((f - q) / 24., 14) for q in set((36, 42, 48, 54, 60, 66, 72)) if 0 <= f - q < 8)
        return st.finish(bloom=.5, thr=.9, vig=.5 + .12 * beat, contrast=1.08, expo=1. - .05 * beat, satu=1.06 - .2 * out, flash=0., fade=.5 * (1 - smooth(0, 4, f)) if f < 5 else 0., fadeCol='#140810')

    def eyes(self, f, st, t):
        """what she sees, in her eyes"""
        g = on2(f); u = (f - 78) / 5.; P = SI.S_STAND.set(hedr=keys(g, [(78, (0, 14, 0)), (82, (0, -5, 0), 'out')]), cher=(0, 0, 0), pelr=(0, 0, 0)); S = st.fig(SI.FOREST, P, draw=False); h = S.head((0, .04, .6)); fw = S.d(np.array([0, 0, 1.]) @ S.u['Bh'])
        cam = Cam(S.head((0, 0, 0)) + V(.35, -.15, 6.6 - .5 * u), h + V(.04, -.04, 0), 10.2 - .5 * u, roll=-2); st.cam = cam
        st.paint(INTERIOR, fk=float(.9 + .1 * noise1(t * 9, 3)))
        fk = .9 + .12 * noise1(t * 9, 3)
        L = Light(key=(.35, -.25, .9), keyCol=(.95 * fk, .50 * fk, .22 * fk), amb=(.12, .07, .15), rim=(-.7, .4, -.5), rimCol=(.6, .22, .16), envT='#ffb060', envM='#d8601c', envB='#2a1030', pts=[(h + V(.5, -2.2, 2.6), 2.6, (.8 * fk, .34 * fk, .09 * fk))], shadow=False, ink=4.)
        lid = keys(f, [(78, .30), (80, 1.02, 'out'), (83, .96)]); gy = keys(f, [(78, -.6), (81, .35, 'out')])
        F = Face(lid=lid, gy=gy, gx=0., brow=.55 * smooth(79, 82, f), sad=.25 + .15 * smooth(79, 82, f), smile=-.05, pupil=1.25 - .5 * smooth(80, 83, f))
        st.open(cam, L); st.fig(SI.FOREST, P, face=F); st.close()
        k = smooth(79, 82, f)
        if k > 0:
            tex = shadow_at(self.T, 76 + (f - 78))
            for sx in (-1, 1):
                x, y, z = cam.project(S.head((sx * EYE[0], EYE[1] + .077 * gy, EYE[2]))); r = cam.px(S.head((0, 0, .65))) * EYE[3]
                st.paint(REFLECT, 'over', texs=dict(tS=tex), c=(float(x), float(y)), r=float(r), k=float(k), lidy=float(y - r * 1.2))
        FX.embers(st, 26, (tuple(h - V(2.6, 2, 1.)), tuple(h + V(2.6, 0, 2.))), t, rise=1.8, size=.022, seed=2, life=1.8)
        return st.finish(bloom=.5, thr=.9, vig=.55, contrast=1.08)

    def foot(self, f, st, t):
        """her foot comes over the line and down; the fire shivers away from it"""
        g = on2(f); u = (f - 84) / 5.; a0 = CROSS; c = line_point(a0, y=0.); out_ = nz((c - V(0, 0, 4)) * V(1, 0, 1)); side = V(out_[2], 0, -out_[0])
        cam = Cam(c + side * 7.0 + out_ * (2.8 - .2 * u) + V(0, 1.5 + .1 * u, 0), c + out_ * .35 + V(0, 1.45, 0), 33, roll=4 - u); st.cam = cam
        st.paint('sky.frag', **SKY(None, **DUSKSKY))
        gone = smooth(87, 90, f); fk = (.9 + .1 * noise1(t * 12, 3)); yaw = math.degrees(math.atan2(out_[0], out_[2]))
        L = Light(**{**DUSKL, 'pts': [(c + side * 2.5 + V(0, 1.4, 0), 4., tuple(np.array([.80, .33, .09]) * fk)), (c - side * 2.5 + V(0, 1.4, 0), 4., tuple(np.array([.62, .25, .07]) * fk))], 'rimCol': (.9, .34, .12), 'inkRef': .8, 'ink': 3.4})
        st.open(cam, L)
        place.draw(st, LITBY, u=placeu(line=1., lineC=a0, lineK=.016 * gone if f >= 87 else -1., rockH=112., lineG=0., fireP=(13., 1.6, 58.), shO=(0, -900., 0), shX=(1., 0, 0), shN=(0, 0, -1.), shBox=(UX, UY, UW, UH), fireI=.9 * fk, shK=0., hutK=0., lean=0., dusk=0., eyes=0., fireC=(1., .40, .10), shTint=(1., 1., 1.), hot=(28., 52., 92.)), texs=dict(tShad=self.T.tex), sun=0.)
        z = keys(f, [(84, -.5), (86, 1.6, 'io'), (87, 2.35, 'out'), (90, 2.35)]); y = keys(f, [(84, 1.25), (85, 1.9, 'out'), (86, 1.6), (87, .82, 'in'), (90, .80)]); pt = keys(f, [(84, 30.), (86, -14.), (87, -10.), (88, 0.)])
        P = SI.S_STEP.set(pel=(0, 8.05, .1 + .45 * smooth(84, 88, f)), lf=(.25, y, z), lft=(4, pt), **HOLD); at = c - out_ * .95
        S = st.fig(SI.FOREST, P, at=at, yaw=yaw, face=Face(), u=dict(Wind=(0, .12, -.5 - .25 * (1 - u))))
        an = S.joint(12); th = np.linspace(0, 2 * math.pi, 20)
        st.mesh(*CL.tube(an + np.c_[.40 * np.cos(th), .10 + 0 * th, .40 * np.sin(th)], .075, 8), kind=0, col=('#fff0d0', '#805030', '#fff'), cls=2, ink=.8)
        st.close()
        k = a0 + np.r_[np.linspace(-.075, .075, 44)]; near = np.clip(1 - np.abs(k - a0) / .030, 0, 1); h = 1.15 * (.6 + .5 * np.modf(np.arange(44) * .618)[0]) * (1 - near * (.55 + .45 * gone)) * (1 + .18 * np.sin(t * 13 + k * 900)); Q = np.array([line_point(q) for q in k]); lean = np.sign(k - a0) * near * 1.4
        Q = Q + np.c_[0 * h, h * .8, 0 * h] + side * (-.9 * lean * h * 0)[:, None]; w = h > .08
        FX.particles(st, Q[w], h[w], (1., .92, .85), 'tongue', seed=(k[w] * 91) % 1, rot=(lean * .5)[w])
        if f >= 87: FX.burst(st, 30, c + out_ * 1.2, (f - 87) / 24., speed=4., grav=3., size=.05, seed=5, col='#ffb050', life=.6, spread=(1, .3, 1), up=.5); FX.burst(st, 24, c + out_ * 1.2, (f - 87) / 24., speed=3., grav=1., size=.16, seed=6, col='#8a5a40', kind='ash', life=.6, spread=(1, .15, 1), up=.15)
        FX.embers(st, 40, (tuple(c - V(7, 0, 5)), tuple(c + V(7, .6, 5))), t, rise=3., size=.035, seed=4, life=1.6)
        return st.finish(bloom=.5, thr=.9, vig=.5, contrast=1.08)
