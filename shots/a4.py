"""a4 (108): Mithila.  Shiva's bow before rows of kings.  The prince lifts it with one hand (f0-29); grip and string, close (f30-53); the draw (f54-83), Sita watching (f66-71); it BREAKS (f84)."""
from lau.shot import *
from lau.look import *
from chars import rama, sita, people as PE
from chars.armonly import ARM, place_hand
from worlds import palace as PL
GREAT = dict(pal={9: ('#5a2a14', '#220c08', 1), 12: ('#b3202a', '#54081c', 1), 13: ('#fff0c8', '#b8864a', 1)})


def great_bow(st, M, pull, half=5.6, cut=0, string=.05):
    return st.fig(PR.BOW.variant(**GREAT, u=dict(pr=np.array([pull, half, cut, string] + [0] * 12, 'f4'), bound=(0, 0, -1.4, half + 1.8))), M=M)


class Shot(ShotBase):
    id = 'a4'; n = 108
    EVENTS = [(0, 'court murmur', dict(dur=30)), (8, 'hand on bow', {}), (14, 'bow lifted', {}), (22, 'court gasps', {}), (34, 'grip creaks', {}), (44, 'string hum', {}), (54, 'bow creak', dict(dur=30)), (84, 'BOW BREAKS', {}), (90, 'petals', dict(dur=18)), (96, 'court roars', dict(dur=12))]

    def setup(self, st):
        c = [((7, '#b3202a', '#54081c'), (8, '#e8a83a', '#8e5620'), .2), ((7, '#1f6a52', '#0a302c'), (8, '#f0e0b8', '#a4866c'), .6), ((7, '#4a2f8a', '#1c1040'), (8, '#e8a83a', '#8e5620'), 0.), ((7, '#d8882a', '#7a3a14'), (8, '#b3202a', '#54081c'), .9), ((7, '#2f5a9a', '#122248'), (8, '#f2c24a', '#8a5a14'), .35)]
        I = []
        for k, (a, b, bd) in enumerate(c):
            fig = PE.DASHARATHA.variant(pal={7: (a[1], a[2], 8), 8: (b[1], b[2], 8), 2: ('#241a16', '#0e0a0a', 5), 1: (['#b8804e', '#8a5636', '#c89060', '#a06a40', '#7a4a30'][k], ['#6a3e28', '#4a2a1c', '#744a30', '#5a3622', '#40241a'][k], 1)}, u=dict(beard=bd, old=0.), face=lambda F, k=k: PE.man_face(F, 0, beard=bd > .3, brow='#1a1010'))
            I.append((fig, [PZ.STAND.set(lh=(1.5, 9.0, 1.8), rh=(-1.5, 9.0, 1.8)), PZ.STAND.set(lh=(.6, 10.6, 1.9), rh=(-.9, 10.2, 2.0), lel=(1, -.4, 0), rel=(-1, -.4, 0)), PZ.CONTRA, PZ.STAND.set(lh=(2.2, 8.6, -.6), rh=(-2.2, 8.6, -.6), lel=(1, 0, -1), rel=(-1, 0, -1))][k % 4], Face(frown=.2, smile=-.1), 62)); I.append((fig, PZ.STAND.set(lh=(2.4, 16.6, .9), rh=(-2.6, 15.6, 1.2), lhand='open', rhand='open', lpalm=(0, 0, 1), rpalm=(0, 0, 1), lel=(1, .2, -.2), rel=(-1, .2, -.2), hedr=(0, -8, 0)), Face(brow=.8, mouth=.5, lid=1.1), 62))
        self.cr = Crowd(st, I, px=340, pitch=4.); r = np.random.default_rng(2); P, T, F = [], [], []
        for z in np.arange(-190, 60, 9.):
            for s in (-1, 1):
                for k in range(3): P.append((s * (27 + 9 * k + r.uniform(-1, 1)), 1.4 * k, z + r.uniform(-2, 2))); T.append(2 * r.integers(0, 5)); F.append(1. if s < 0 else -1.)
        self.P, self.T, self.F = np.array(P), np.array(T), np.array(F)

    def kings(self, st, t, shock=0.):
        tl = self.T + (shock > .5); self.cr.draw(self.P, scale=1. + .012 * np.sin(t * 5 + self.P[:, 2]), tile=tl, flip=self.F, lean=.03 * np.sin(t * 2 + self.P[:, 2]) - .12 * shock * 0, tint=.95)

    def frame(self, f, st):
        st.clear('#000', f=f); t = st.t
        if f < 30: return self.lift(f, st, t)
        if f < 54: return self.close_(f, st, t)
        if 66 <= f < 72: return self.sita(f, st, t)
        if f < 84: return self.draw(f, st, t)
        return self.broken(f, st, t)

    def dais(self, st):
        """a low lotus stand for the bow"""
        st.world('''
#define TMAX 120.
vec2 map(vec3 p){float bd=length(p-vec3(0,1,0))-9.;if(bd>1.) return vec2(bd,1.);float a=atan(p.z,p.x),r=length(p.xz*vec2(.62,1.));float d=max(r-3.6,abs(p.y-.45)-.45);float pt=abs(fract(a*14./TAU)-.5);d=min(d,max(r-4.2+.5*pt,abs(p.y-.18)-.18));vec2 m=vec2(d*.8,1.);for(int s=-1;s<=1;s+=2){vec3 q=p-vec3(float(s)*4.4,1.5,0);m=U(m,vec2(max(abs(length(q.xy)-.62)-.20,max(abs(q.z)-.35,q.y-.1)),2.));m=U(m,vec2(sCap(p,vec3(float(s)*4.4,0,0),vec3(float(s)*4.4,.95,0),.30),2.));}return m;}
void surf(vec3 p,vec3 n,int m,inout Surf s){if(m==2){s.cls=2.;s.base=vec3(1);s.sh=hex(0x5a2a10);}else{float a=atan(p.z,p.x);float pt=abs(fract(a*14./TAU)-.5);s.base=mix(hex(0xc8283a),hex(0xf2a0a0),smoothstep(.1,.5,pt));s.base=mix(s.base,hex(0xe8b040),step(.78,p.y));s.sh=hex(0x4a0c1c);}}
''')

    def lift(self, f, st, t):
        u = f / 29.; g = on2(f); cam = Cam(V(13 - 4 * u, 5.0 + .6 * u, 34 - 4 * u), V(0, 9.0, -2), 34, roll=-2); st.cam = cam; st.paint('sky.frag', **PL.sky('mithila'))
        up = keys(g, [(0, 0.), (9, 0.), (12, -.04), (22, 1.05, 'io'), (26, .98), (29, 1.)]); L = PL.light('mithila', at=(0, 40, 0)); st.open(cam, L); PL.draw(st, 'mithila'); self.kings(st, t, smooth(21, 24, f)); self.dais(st)
        # bow: from lying across its stand to upright in his left hand
        grip = lerp(V(0, 2.0, 1.2), V(3.2, 12.2, 1.6), up); ang = math.radians(90 * (1 - min(up, 1.02))); yv = V(math.sin(ang), math.cos(ang), 0); zv = nz(V(math.cos(ang) * .9 + .0, -math.sin(ang) * .9, .35 + .0))
        zv = lerp(V(0, 0, 1), nz(V(.95, 0, .3)), up); M = PR.place(grip, yv, zv, 1.62); great_bow(st, M, 1.05)
        rp = keys(g, [(0, 0.), (8, 1., 'io'), (12, 1.)]); lhand = np.array(lerp(V(2.3, 7.6, 1.2), grip, rp)); at = V(-.4, 0, -1.6)
        P = PZ.STAND.set(pel=(0, 8.3 - 1.9 * (rp - min(up, 1)) * (rp > 0), 0), pelr=(0, 16 * (rp - min(up, 1)), 0), cher=(0, 14 * (rp - min(up, 1)), 0), hedr=(18 * up, 8 * (1 - up), 0), lh=tuple(lhand - at - V(0, .62, .1)), lel=(1, -.3, -.6), lhand='grip' if rp > .9 else 'open', lfing=(.2, .2, 1) if rp > .5 else None, lpalm=(1, 0, 0) if up > .5 else (0, -1, .2), rh=(-2.4, 7.7, .5), lf=(1.2, .75, .6), rf=(-1.2, .75, -.5))
        st.fig(rama.PRINCE, P, at=tuple(at), yaw=0, face=Face(smile=.15, lid=.85, gx=.4 * up)); st.close(); PL.flames(st, 'mithila')
        FX.drift(st, 30, ((-20, 0, -20), (20, 30, 18)), t, kind='petal', size=.16, col='#f2a03a', col2='#e8506a', fall=1.2, seed=3)
        return st.finish(bloom=.45, thr=.95, vig=.42, contrast=1.05, fade=1 - smooth(0, 4, f), fadeCol='#f8e0b0')

    BK = '''
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform vec2 res;uniform float fT,hot;
void main(){vec2 p=uv*vec2(res.x/res.y,1.);vec3 c=mix(hex(0xd89a52),hex(0x6a2c22),smoothstep(.0,1.2,length(p-vec2(1.25,.75))));for(int i=0;i<7;i++){float f=float(i);vec2 q=p-vec2(h11(f*3.1)*1.78,h11(f*7.7)+.02*sin(fT+f));c+=hex(0xffc870)*smoothstep(.10+.06*h11(f),.07+.05*h11(f),length(q))*.16;}c*=.9+.2*fbm(p*4.);c+=hex(0xffa040)*hot*.25;o=vec4(c,1);}
'''

    def close_(self, f, st, t):
        g = on2(f)
        if f < 42:
            u = (f - 30) / 11.; cam = Cam(V(-3.2 + .5 * u, .6, 6.0 - .4 * u), V(.1, .15, 0), 34, roll=4 - 3 * u); st.cam = cam; st.paint(self.BK, hot=float(.2 * u))
            L = Light(key=(-.5, .6, .6), keyCol='#ffd8a0', amb='#7a5a7a', rim=(.8, .3, -.5), rimCol=(1.2, .8, .4), bounceCol=(.2, .1, .05), envT='#ffe0a0', envM='#ffc060', envB='#8a4a2a', ink=3.6, inkRef=.6)
            st.open(cam, L); great_bow(st, PR.place(V(0, 0, 0), V(.10, 1, 0), V(.9, 0, .45), 1.62), 1.4)
            dx = keys(g, [(30, 2.4), (34, .02, 'io'), (35, .0)]); Ph = PZ.STAND.set(rh=(-2.2, 11.5, 2.0), rel=(-.6, -1, -.3), rhand='grip' if g >= 34 else 'open', rpalm=(0, -.3, 1)); A = ARM.variant(u=dict(side=1, band=1, fore=1.)); S = st.fig(A, Ph, draw=False)
            st.fig(A, Ph, M=place_hand(S, 'R', V(-.22 - dx, .0, .34 + .25 * dx), (.62, -.10, -.45), (.45, 0, .9) if g < 34 else (.40, -.05, .9), 1.12)); st.close()
            gx = smooth(34, 41, f); x, y, z = cam.project(V(0, -3.4 + 8.0 * gx, 0)); FX.particles(st, np.array([[x, y]]), 120 * math.sin(gx * math.pi) + 1, '#ffe8b0', 'glint', alpha=.9)
            sx, sy = shake(f, 5 * impulse((f - 34) / 24., 10), .9, 3); IM.whip(st, sx, sy)
            return st.finish(bloom=.5, thr=.9, vig=.5, contrast=1.06)
        u = (f - 42) / 11.; pull = keys(g, [(42, 1.0), (46, 1.0), (53, 2.3, 'io')]); cam = Cam(V(-6.6 - .6 * u, .5, 4.6 + .4 * u), V(-2.0 - 1.1 * u, .0, 0), 34, roll=-5 + 3 * u); st.cam = cam; st.paint(self.BK, hot=float(.3 + .3 * u))
        L = Light(key=(-.5, .5, .7), keyCol='#ffd8a0', amb='#7a5a7a', rim=(.8, .3, -.5), rimCol=(1.2, .8, .4), bounceCol=(.2, .1, .05), envT='#ffe0a0', envM='#ffc060', envB='#8a4a2a', ink=3.6, inkRef=.6); vib = .02 * math.sin(f * 2.6) * u
        st.open(cam, L); great_bow(st, PR.place(V(0, vib, 0), V(0, 1, 0), V(1, 0, .05), 1.62), pull, string=.062)
        nk = V(-pull * 1.62, vib, -.02); A = ARM.variant(u=dict(side=1, band=1, fore=1.)); Ph = PZ.STAND.set(rh=(-2.2, 11.5, 2.0), rel=(-.6, -1, -.3), rhand='draw', rpalm=(0, -.3, 1)); S = st.fig(A, Ph, draw=False); st.fig(A, Ph, M=place_hand(S, 'R', nk + V(-.55, -.35, .05), (.86, .42, .25), (.30, -.15, -.94), 1.1)); st.close()
        return st.finish(bloom=.5, thr=.9, vig=.5, contrast=1.06)

    def hero(self, st, f, t, draw, at=(0, 0, 0)):
        P = PZ.archer(draw); S = st.fig(rama.PRINCE, P, at=at, yaw=14, face=Face(frown=.25, smile=.05, lid=.9, gx=.2), draw=True); g = S.palm('L', .0, .62, .30); nk = S.palm('R', .22, .95, .34); aim = nz(g - nk); pull = float(np.linalg.norm(g - nk))
        return S, g, nk, aim, pull

    def draw(self, f, st, t):
        u = (f - 54) / 29.; g = on2(f); d = keys(g, [(54, .05), (64, .35, 'io'), (72, .60, 'io'), (80, .98, 'io'), (84, 1.05)]); cam = Cam(V(8.5 - 2.5 * u, 2.4 + .6 * u, 27 - 6.5 * ease_io(u)), V(2.6, 11.4, 0), 36, roll=-6 + 3 * u); st.cam = cam; st.paint('sky.frag', **PL.sky('mithila'))
        L = PL.light('mithila', at=(0, 40, 0)); L.keyCol = tuple(np.array(hexc('#f2c088')) * (1 + .25 * u)); st.open(cam, L); PL.draw(st, 'mithila'); self.kings(st, t, 0.)
        S, gp, nk, aim, pull = self.hero(st, f, t, d); tr = .05 * u * u * math.sin(f * 2.9); up = S.d((0, 1, 0)); great_bow(st, PR.place(gp + V(0, tr, 0), up - aim * (up @ aim), aim, 1.62), pull / 1.62, string=.055); st.close(); PL.flames(st, 'mithila')
        x, y, z = cam.project(gp); st.paint('''
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform vec2 res,c;uniform float a,fT;void main(){vec2 p=vec2(uv.x*res.x,(1.-uv.y)*res.y)-c;float r=length(p)/res.y,an=atan(p.y,p.x);float ray=smoothstep(.0,.5,sin(an*18.+fT))*.6+smoothstep(.2,.6,sin(an*7.-fT*.8))*.6;o=vec4(hex(0xffc060)*(ray*exp(-r*2.6)*.35+exp(-r*r*18.)*.22)*a,0);}
''', 'over', c=(float(x), float(y)), a=float(smooth(62, 84, f)))
        FX.drift(st, 40, ((-20, 0, -20), (20, 30, 18)), t, kind='petal', size=.16, col='#f2a03a', col2='#e8506a', fall=1.2 - .8 * u, seed=3)
        sx, sy = shake(f, 3 * u * u, .9, 5); IM.whip(st, sx, sy)
        return st.finish(bloom=.5, thr=.92, vig=.45, contrast=1.06)

    def sita(self, f, st, t):
        u = (f - 66) / 5.; P = sita.fit(sita.S_STAND).set(lh=(.8, 10.2, 2.4), rh=(-.8, 10.2, 2.4), lhand='cup', rhand='cup', lfing=(-.2, 1, .2), rfing=(.2, 1, .2), lpalm=(0, 0, 1), rpalm=(0, 0, 1), hedr=(0, 2, 2)); S = st.fig(sita.BRIDE, P, draw=False); h = S.head((0, 0, .5)); cam = Cam(h + V(1.6, -.3, 9.0 - .4 * u), h + V(.1, -.2, 0), 24, roll=-2); st.cam = cam; st.paint(self.BK, hot=.3)
        L = Light(key=(.5, .3, .8), keyCol='#ffd8a0', amb='#7a4a6a', rim=(-.8, .4, -.5), rimCol=(1.2, .7, .35), bounceCol=(.25, .12, .06), envT='#ffe0a0', envM='#ffc060', envB='#8a4a2a', shadow=False, ink=3.4)
        st.open(cam, L); st.fig(sita.BRIDE, P, face=Face(lid=lerp(.85, 1.1, u), brow=.3 + .4 * u, smile=.05, gx=.35, gy=.1)); st.close()
        return st.finish(bloom=.5, thr=.92, vig=.5, contrast=1.06)

    def print_(self, f, st, t):
        """two frames as a three-colour print: only him, the bow in two, and the burst"""
        k = f - 84; cam = Cam(V(6.0, 3.2, 20.5), V(2.6, 11.4, 0), 36, roll=-3 + 4 * k); st.cam = cam; g0 = st.fig(rama.PRINCE, PZ.archer(1.05), yaw=14, draw=False) if False else None
        st.open(cam, Light(shadow=False)); S = st.fig(rama.PRINCE, PZ.archer(1.05), yaw=14, draw=False); gp = S.palm('L', .0, .62, .30); x, y, z = cam.project(gp)
        st.paint('''
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform vec2 res,c;uniform float k;void main(){vec2 p=vec2(uv.x*res.x,(1.-uv.y)*res.y)-c;float r=length(p)/res.y,a=atan(p.y,p.x);float st=.16+.22*pow(abs(sin(a*7.+k)),3.)+.16*pow(abs(sin(a*13.+2.*k)),6.);vec3 q=mix(hex(0xfff3dc),hex(0xc8281c)*.55,smoothstep(st,st+.02,r));q=mix(q,hex(0x140608),smoothstep(.62,.64,r+.18*sin(a*9.+k*3.)));o=vec4(q,1);}
''', c=(float(x), float(y)), k=float(k))
        L = Light(key=(.8, .4, .5), keyCol=(1.5, 1.4, 1.2), amb=(.05, .03, .05), rim=(.9, .3, -.3), rimCol=(3, 3, 3), shadow=False, stip=0., air=0., ink=6.0); st.open(cam, L); S = st.fig(rama.PRINCE, PZ.archer(1.05), yaw=14, face=Face(frown=.4, lid=1.0)); up = S.d((0, 1, 0)); aim = S.d((1, 0, .1))
        for s in (1, -1): great_bow(st, PR.place(gp + V(.5 * s * (k + 1) * .6, .9 * s * (k + 1), 0), nz(up + aim * .35 * s * (k + 1)), aim, 1.62), 3.2, cut=s)
        st.close(); FX.burst(st, 90, gp, (k + 1) / 24., speed=30, grav=0, size=.14, seed=3, col='#fff8e8', life=.5)
        IM.speedlines(st, (float(x), float(y)), .85, col=(.02, .01, .01) if k == 0 else '#fff3dc', seed=f, inner=.30, dens=7); IM.inkflash(st, '#140608', '#c8281c', '#fff3dc', lo=.26, hi=.60, invert=k == 1)
        return st.finish(bloom=.2, vig=.2)

    def broken(self, f, st, t):
        if f < 86: return self.print_(f, st, t)
        a = (f - 84) / 24.; cam = Cam(V(6.0 + .8 * a, 3.0, 20.5 + 5.5 * ease_out(min(1, a), 2.2)), V(2.4 - 1.2 * smooth(84, 100, f), 11.4 - 1.0 * smooth(84, 100, f), 0), 36, roll=-3); st.cam = cam; st.paint('sky.frag', **PL.sky('mithila'))
        L = PL.light('mithila', at=(0, 40, 0)); st.open(cam, L); PL.draw(st, 'mithila'); self.kings(st, t, 1.)
        P = PZ.archer(1.0).mix(PZ.STAND.set(lh=(4.6, 9.6, 1.6), rh=(-3.6, 8.8, .8), lhand='grip', rhand='open', hedr=(20, 0, 0), cher=(0, -4, 0), lel=(1, -.5, -.2), rel=(-1, -.4, -.4), lf=(2.0, .75, .5), rf=(-2.0, .75, -.3)), smooth(86, 96, on2(f)))
        S = st.fig(rama.PRINCE, P, yaw=14, face=Face(lid=.95, smile=.2 * smooth(92, 104, f), gx=.2)); gp = S.palm('L', .0, .62, .30); up = S.d((0, 1, 0)); aim = S.d((1, 0, .1))
        for s in (1, -1):                                                           # upper half flies, lower half stays in his hand
            if s > 0: pos = gp + V(1.5 * a * 9, 2.2 + 13 * a - 9 * a * a, 3 * a); yv = nz(V(math.sin(a * 6.5), math.cos(a * 6.5), .3))
            else: pos = gp; yv = nz(V(-.10 - .25 * smooth(86, 98, f), 1, .05))
            great_bow(st, PR.place(pos, yv, aim, 1.62), 1.6, cut=s)
        st.close(); PL.flames(st, 'mithila'); hit = S.w(S.J[6]) + V(0, 1, 0)
        x, y, z = cam.project(gp)
        FX.burst(st, 150, gp, a, speed=24, grav=7, size=.10, seed=3, col='#ffd890', life=.9); FX.burst(st, 60, gp, a, speed=17, grav=10, size=.22, seed=8, col='#8a5a2a', kind='leaf', life=1.4)
        r = np.random.default_rng(7); n = 260; d = r.normal(size=(n, 3)); d /= np.linalg.norm(d, axis=1, keepdims=True); k = r.uniform(.3, 1., n)[:, None]; P3 = V(0, 12, -1) + d * 22 * k * (1 - math.exp(-2.6 * a)) + V(0, -2.4, 0) * a * a + np.c_[.6 * np.sin(t * 2 + k[:, 0] * 30), np.zeros(n), np.zeros(n)]
        FX.particles(st, P3, .20 * r.uniform(.6, 1.3, n), np.where(r.uniform(0, 1, (n, 1)) > .5, np.array(hexc('#f2a03a')), np.array(hexc('#e8506a'))), 'petal', rot=r.uniform(0, 6, n) + t * 3 * (k[:, 0] - .5), alpha=min(1., a * 10))
        ray = 1 - smooth(84, 106, f); st.paint('''
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform vec2 res,c;uniform float a,fT;void main(){vec2 p=vec2(uv.x*res.x,(1.-uv.y)*res.y)-c;float r=length(p)/res.y,an=atan(p.y,p.x);float ray=smoothstep(.0,.5,sin(an*22.))*.6+smoothstep(.2,.6,sin(an*9.+1.))*.6;o=vec4(hex(0xffd890)*(ray*exp(-r*1.8)*.6+exp(-r*r*10.)*.5)*a,0);}
''', 'over', c=(float(x), float(y)), a=float(ray))
        if f < 94: IM.shock(st, (float(x), float(y)), 40 + 1900 * a, 110, 70 * (1 - a))
        if f == 86: IM.speedlines(st, (float(x), float(y)), .9, col=(.02, .01, .01), seed=f, inner=.18)
        sx, sy = shake(f, 46 * math.exp(-5 * a), .8, 4); IM.whip(st, sx, sy)
        return st.finish(bloom=.55, thr=.92, vig=.4, contrast=1.06, flash=.5 * (f == 86) + .22 * (f == 87), flashCol='#fff3d8')
