"""g5 (168): the lamp of the beginning.  A child's new wick is lit at the flame, an old hand under the small one (f30-48); the small flame comes to us (f48-84); a breath, out (f84).
Black.  लौ is written in embers (f90-120), holds, and fades (f144-168)."""
from lau.shot import *
from chars.armonly import ARM, SKIN, place_hand
from chars import people as PE
from .a1 import WICK, lamp_light

OLD = ARM.variant(pal={1: SKIN['old']}, u=dict(side=0, band=2, old=1.)); CHILD = ARM.variant(pal={1: SKIN['child']}, u=dict(side=1, band=1, old=0.), build=dict(arm=1.12, hand=1.0), dim=dict(up=2.2, fore=1.75))
CUP = PZ.STAND.set(rh=(-2.2, 8.6, 3.4), rel=(-1, -.6, -.1), rhand='cup', rfing=(.2, .1, 1), rpalm=(0, 1, .1), lh=(2.2, 8.6, 3.4), lel=(1, -.6, -.1), lhand='cup', lfing=(-.2, .1, 1), lpalm=(0, 1, .1))
DIYA = PR.DIYA.variant(pal={3: ('#b0643a', '#4a2416', 1), 6: ('#f7efdc', '#a08070', 1), 14: ('#8a4a1c', '#3a1a0c', 3)})

EMBER = '''
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform vec2 res;uniform sampler2D tW,tE;uniform float fT,fade_,age;
void main(){vec2 p=vec2(uv.x*res.x,(1.-uv.y)*res.y);vec2 dq=(vec2(vn(p/9.),vn(p/9.+7.))-.5)*5./res;float a=texture(tW,uv+dq).a;float soft=textureLod(tW,uv,4.5).a,glow=textureLod(tE,uv,6.).a+.6*textureLod(tE,uv,7.5).a;
 float n=fbm(p/14.)*.6+fbm(p/46.+3.)*.4;float cr=smoothstep(.40,.62,fbm(p/7.+vec2(0,fT*.25)));float e=texture(tE,uv+dq).a;
 float heat=clamp(e*1.2+a*(.55+.35*sin(fT*2.2+n*14.))*(1.-.25*cr),0.,1.6)*fade_;
 vec3 c=mix(hex(0x140404),hex(0x8a1a08),smoothstep(.05,.40,heat));c=mix(c,hex(0xff5a14),smoothstep(.35,.72,heat));c=mix(c,hex(0xffc860),smoothstep(.75,1.15,heat)*(1.-cr*.6));c=mix(c,hex(0x0c0405),cr*.55*a*(1.-e));
 float dry=smoothstep(.16,.42,n+.25*soft);float k=a*dry;vec3 g=hex(0xff6a1c)*(soft*.10+glow*.16)*fade_;o=vec4(c*k*fade_+g,1);}
'''


class Shot(ShotBase):
    id = 'g5'; n = 168
    EVENTS = [(0, 'lamp bed', dict(dur=84)), (30, 'wick to wick', {}), (42, 'small flame catches', {}), (56, 'flame comes near', {}), (80, 'breath', {}), (84, 'flame out', {}), (90, 'title embers', dict(dur=30)), (120, 'title done', {})]

    def frame(self, f, st):
        st.clear('#000', f=f)
        if f < 54: return self.pass_on(f, st, st.t)
        if f < 90: return self.near(f, st, st.t)
        return self.title(f, st, st.t)

    def diya(self, st, at, sc, yaw, tiltx=0., lit=0., t=0.):
        """a small clay lamp whose wick tip is at local (1.28, .34, 0); returns the wick point"""
        M = np.eye(4); M[:3, :3] = eul(yaw, 0, tiltx) * sc; M[:3, 3] = at; st.fig(DIYA, M=M)
        return M[:3, :3] @ V(1.30, .42, 0) + M[:3, 3]

    def pass_on(self, f, st, t):
        e = ease_io(f / 53., 1.5); cam = Cam(lerp(V(1.6, 3.0, 15.0), V(3.4, 2.2, 10.6), e), lerp(V(1.1, 1.7, 0), V(3.7, 1.55, 0), e), 26); st.cam = cam
        g = on2(f); go = keys(g, [(0, 0.), (30, 1., 'io'), (44, 1.), (54, .86, 'io')]); lit = keys(f, [(36, 0.), (40, .35), (43, 1.15, 'out'), (48, 1.)]) if f >= 36 else 0.
        touch = WICK + V(.62, .62, .35); wick = lerp(V(11.2, .2, 3.4), touch, go) + V(0, .04 * math.sin(t * 3), 0); sc = .86; yaw = 180 + 8
        base = wick - eul(yaw, 0, -8) * sc @ V(1.30, .42, 0)
        I = lamp_light(1., t, 2.); bow = .9 * smooth(26, 34, f) * (1 - smooth(44, 52, f))
        pts = [(WICK + V(.05 + .3 * bow, 1.1, .1), 3.0, tuple(np.array([1.25, .62, .24]) * I))]
        if lit > .02: pts.append((wick + V(0, .7, .2), 2.2, tuple(np.array([.95, .46, .17]) * lit * lamp_light(1., t, 9.))))
        L = Light(key=(0, 1, 0), keyCol=(.02, .012, .01), amb=(.016, .010, .016), rim=(-.6, .4, -.5), rimCol=(.30, .12, .04), bounceCol=(.05, .02, .01), pts=pts, shadow=False, envT='#ffb060', envM='#ff9a40', envB='#6a2a14', ink=2.8, inkRef=.4, inkCol='#060204', hi=.3, stip=.15)
        st.open(cam, L, far=200.); st.world('lamp.glsl', u=dict(clothZ=-13., glowW=.8, glowL=float(I)))
        self.diya(st, base, sc, yaw, -8)
        S = st.fig(CHILD, CUP, draw=False); M = place_hand(S, 'R', base + V(.25, -.62, .1), (-.96, .10, -.25), (.05, 1, .10), .82); st.fig(CHILD, CUP, M=M)
        So = st.fig(OLD, CUP, draw=False); Mo = place_hand(So, 'L', base + V(.55, -1.20, .15), (-.92, .22, -.30), (.10, 1, .15), 1.06); st.fig(OLD, CUP, M=Mo, u=dict(side=0))
        st.close()
        FX.flame(st, WICK + V(.02, -.06, 0), 2.35, seed=1.3, glow=.7, lean=.62 * bow, calm=.9)
        if 34 <= f: FX.flame(st, wick + V(0, -.02, 0), 1.35 * lit, seed=7.1, glow=.55 * min(lit, 1), lean=-.35 * bow, calm=1.0)
        if 36 <= f < 60: FX.burst(st, 18, wick, (f - 38) / 24., speed=1.8, grav=2, size=.02, seed=3, col='#ffb050', life=.6, up=.8)
        FX.embers(st, 10, ((2.9, 1.8, -.1), (3.2, 2.4, .1)), t, rise=1.6, size=.03, seed=4, life=2., swirl=.25)
        IM.dof(st, float((WICK - cam.eye) @ cam.R[2]), 7., 6.)
        return st.finish(bloom=.42, thr=.95, vig=.55, grain=.018, contrast=1.06, fade=1 - smooth(0, 8, f))

    def near(self, f, st, t):
        """the child brings the new flame to us; at the storyteller's last breath it bows and is gone"""
        u = (f - 54) / 29.; k = ease_io(clamp(u), 1.8); out = keys(f, [(80, 1.), (82, .82), (83, .55), (84, 0., 'snap')]) if f >= 80 else 1.; lean = keys(f, [(74, 0.), (80, .18), (83, 1.5, 'in')]) if f >= 74 else 0.; g = on2(f)
        P0 = PE.C_LAMP; h0 = (np.array(P0.lh) + np.array(P0.rh)) / 2; d = np.array(keys(g, [(54, (0, -.5, -.4)), (64, (0, .35, .9), 'io'), (84, (0, .55, 1.25), 'io')])); P = P0.set(lh=tuple(np.array(P0.lh) + d), rh=tuple(np.array(P0.rh) + d), hedr=keys(g, [(54, (0, 16, 0)), (70, (0, 8, 0)), (84, (0, 10, 0))]))
        S = st.fig(PE.CHILD, P, draw=False); mid = (S.palm('L') + S.palm('R')) / 2; base = mid + V(0, .42, .12); wick = base + V(0, .30, .72)
        cam = Cam(lerp(V(.5, 8.6, 10.6), V(.10, 7.7, 7.4), k), lerp(V(0, 6.7, 0), wick + V(0, .55, -.6), k), 27); st.cam = cam; I = lamp_light(1., t, 9.) * out + .05 * max(0., 1 - abs(f - 85) / 6.); wall = .42 * (1 - .4 * k) * (out > .5)
        st.paint('''
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform vec2 res;uniform float amt,fT;void main(){vec2 p=(uv-.5)*vec2(res.x/res.y,1.);vec3 c=hex(0x0a0506);vec2 q=p-vec2(-.58,.14);float r=length(q);c+=hex(0xc8641a)*(exp(-r*r*9.)*.9+exp(-r*3.)*.3)*amt*(.95+.05*sin(fT*9.));float d=length(q*vec2(1.,.45));c+=hex(0xffc870)*smoothstep(.09,.02,d)*amt*.8;c*=.92+.12*fbm(uv*vec2(8.,5.));o=vec4(c,1);}
''', amt=float(wall))
        L = Light(key=(0, -.2, 1), keyCol=(.012, .007, .006), amb=(.014, .009, .014), rim=(-.8, .3, -.4), rimCol=(.35 * wall, .15 * wall, .04), bounceCol=(0, 0, 0), pts=[(wick + V(0, .55, .35), 2.1, tuple(np.array([1.15, .56, .21]) * I))], shadow=False, envT='#ffb060', envM='#ff9a40', envB='#6a2a14', ink=3.2, inkRef=.5, inkCol='#060204', hi=.35, stip=.15)
        lid = keys(f, [(54, .62), (62, .62), (68, 1.0, 'out'), (78, .95), (82, .02, 'io')])
        st.open(cam, L, far=200.); st.fig(PE.CHILD, P, face=Face(lid=lid, spark=.9 * out * smooth(60, 68, f), smile=.35 + .2 * k, gy=-.5 * (1 - smooth(64, 70, f)))); M = np.eye(4); M[:3, :3] = eul(-90, 0, 0) * .62; M[:3, 3] = base + V(0, .08, 0); st.fig(DIYA, M=M); st.close()
        wick = M[:3, :3] @ V(1.30, .42, 0) + M[:3, 3]
        if out > .02: FX.flame(st, wick + V(0, -.02, 0), 1.15 * (.4 + .6 * out), seed=7.1, glow=.26 * out, lean=lean, calm=.8 + lean)
        else:
            a = (f - 84) / 24.; Q = np.array([wick + V(.12 * math.sin(q * 5 + a * 5) * q, 1.6 * q * min(1., .35 + a * 2), .0) for q in np.linspace(0, 1, 24)]); FX.ribbon(st, Q, np.linspace(.02, .17, 24), 'smoke', '#6a6470', '#2a262e', seed=3, amt=.55 * (1 - a * 2.2)); FX.particles(st, wick[None] + V(0, .02, 0), .08 * max(.1, 1 - a * 3.4), '#ff6a24', 'ember')
        IM.dof(st, float((wick - cam.eye) @ cam.R[2]), 5., 4.)
        return st.finish(bloom=.42, thr=.95, vig=.6, grain=.018, contrast=1.06, fade=smooth(86, 90, f))

    def title(self, f, st, t):
        up = ease_io((f - 90) / 30., 1.7); w, h = W, H; x0, y0, hh = 720, 455, 430

        def tex(a, b):
            sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h); c = cairo.Context(sf); LT.draw(c, 'lau', x0, y0, hh, col=(1, 1, 1), w=.135, upto=b)
            if a > 0: c.set_operator(cairo.OPERATOR_DEST_OUT); LT.draw(c, 'lau', x0, y0, hh, col=(1, 1, 1), w=.145, upto=a)
            sf.flush(); return gl.tex_from(np.ndarray((h, w, 4), np.uint8, sf.get_data()).copy())
        A = tex(0, max(up, .004)); E = tex(max(0, up - .10), max(up, .004)) if f < 124 else tex(.999, 1.); age = max(0, f - 120) / 24.
        fade = 1 - smooth(144, 166, f)
        st.paint(EMBER, texs=dict(tW=A, tE=E), fade_=float(fade * (1 - .15 * smooth(120, 140, f))), age=float(age))
        S, tot = LT.strokes('lau', 60); Ls = np.array([np.linalg.norm(np.diff(s, axis=0), axis=1).sum() for s in S]); r = np.random.default_rng(3); n = 220; born = r.uniform(0, 1, n); P = []
        for q in born:
            T = Ls.sum() * q; a = 0
            for s, l in zip(S, Ls):
                if T <= a + l: i = (T - a) / l * 59; j = int(min(i, 58)); P.append(s[j] + (s[j + 1] - s[j]) * (i - j)); break
                a += l
            else: P.append(S[-1][-1])
        P = np.array(P) * hh + [x0, y0]; lf = (f - 90 - 30 * born ** .8) / 24. / r.uniform(.8, 2.2, n); ok = (lf > 0) & (lf < 1); Q = P + np.c_[26 * np.sin(lf * 5 + born * 40), -150 * lf * r.uniform(.4, 1.2, n)]
        FX.particles(st, Q[ok], (r.uniform(1.6, 4.2, n) * (1 - np.clip(lf, 0, 1)) ** .5)[ok], '#ffa040', 'ember', alpha=(1 - np.clip(lf, 0, 1))[ok] * fade)
        A.release(); E.release()
        return st.finish(bloom=.55, thr=.55, vig=.45, grain=.015, fade=smooth(160, 167, f))
