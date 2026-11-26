"""What the shots of act G share: Sita without (or with) the hair jewel, the jewel itself, a small standing brass lamp, night colours, flicker."""
import copy
from lau.shot import *
from lau.face import human
from chars import sita, rama

INDIGO = '#0b1030'
BRASS_PAL = {3: ('#ffffff', '#805030', 2), 4: ('#c4142c', '#54081c', 3), 5: ('#12a878', '#04382e', 3), 6: ('#fff6e6', '#b09a9c', 1), 9: ('#7a3d1a', '#34160b', 1), 14: ('#8a4a1c', '#3a1a0c', 3), 13: ('#f2e6c8', '#8a6a50', 1)}


class Jewelled(Fig):
    """Sita's shader with one more uniform: jewel 0 = the hair jewel is gone, 1 = it is worn"""

    def program(self):
        src = gl.source('sita.glsl').replace('#version 430\n', '').replace('if(look==2){vec3 g=h-vec3(-.43', 'if(look==2&&jewel>.5){vec3 g=h-vec3(-.43')
        return gl.program('#include "fig_head.glsl"\nuniform float jewel;\n' + src + '\n#include "fig_main.glsl"\n', defs=self.defs)


def one_tear(F, S=2048, lash=True):
    """Sita's grove face, painted finer, with at most one tear: it wells at the rim of her left eye (screen right) and runs down the cheek"""
    k = min(1., max(0., F.tear)); G = F.set(tear=0.)

    def extra(P, F_, st):
        if lash: sita.lashes(P, F_, st)
        if k > 0:
            lo = -.062 + .03 * max(F.smile, 0) + .05 * F.squint; x = .315; run = max(0., (k - .25) / .75); y = lo - .045 - .55 * run ** 1.3; r = .030 + .012 * min(1., k * 3)
            if run > .03:
                P.fill([(x - .004, lo - .03), (x + .012, lo - .2 * run, x + .016, y + .12, x + r * .55, y + .03), (x, y + .01), (x - r * .55, y + .03), (x - .012, y + .12, x - .010, lo - .2 * run, x - .004, lo - .03)], '#ffe6c0', .38)
            P.fill([(x, y + r * 2.0), (x + r * .4, y + r, x + r, y + r * .5, x + r, y - r * .1), (x + r, y - r * .85, x - r, y - r * .85, x - r, y - r * .1), (x - r, y + r * .5, x - r * .4, y + r, x, y + r * 2.0)], '#ffdca8', .85)
            P.fill([(x - r * .45, y + r * .2), (x - r * .3, y + r * .5, x, y + r * .5, x + r * .1, y + r * .2), (x, y - r * .1, x - r * .3, y - r * .1, x - r * .45, y + r * .2)], '#fffaf0', .95)
            P.line([(x - r * .8, y - r * .2), (x - r * .7, y - r * .9, x + r * .7, y - r * .9, x + r * .8, y - r * .2)], .010, '#b0623a', .8)
    st = dict(iris='#6a3416', iris2='#1e0c06', lip='#b03a4a', lip2='#c9545e', liphi='#f8c0b0', blush='#d87a5a', brow='#2a1610', browt=.75, browy=.025, tilak=None, size=1.10, nose='#9a5236', kohl='#2a1210', mouthw=.86, tilt=.02)
    return human(G, st, extra=extra, S=S)


def _jewelled(v):
    o = copy.copy(sita.GROVE); o.__class__ = Jewelled
    return o.variant(u=dict(jewel=v), face=one_tear)


SITA, SITA_JEWEL = _jewelled(0.), _jewelled(1.)
SITA_P = SITA.variant(face=lambda F: one_tear(F, 1536, False))          # for profiles: no drawn lashes on the turn of the cheek
RAMA = rama.EXILE.variant(pal={1: ('#2f78cc', '#1c3f88', 1)}, face=lambda F: human(F, dict(skinsh='#1c2c58'), S=2048))

# the chudamani: face toward +z, about 2 across; local y = up the hair
JEWEL = Fig('chudamani', '''vec2 map(vec3 p){
 vec3 q=p;float a=atan(q.y,q.x);float r=length(q.xy*vec2(1.,.82));
 vec2 m=vec2(sEll(q,vec3(.92+.05*cos(a*12.),1.12+.05*cos(a*12.),.26)),3.);
 m=U(m,vec2(length(vec2(r-.66,q.z-.16))-.085,3.));
 m=U(m,vec2(sEll(q-vec3(0,0,.17),vec3(.50,.66,.30)),5.));
 float n=12.,s=TAU/n;float b=mod(a+s*.5,s)-s*.5;m=U(m,vec2(length(vec3(r*cos(b)-.92,r*sin(b),q.z-.05))-.165,6.));
 m=U(m,vec2(sEll(q-vec3(0,-1.60,.02),vec3(.17,.30,.17)),6.));m=U(m,vec2(length(q-vec3(0,-1.26,.02))-.10,3.));
 m=U(m,vec2(length(q-vec3(0,1.30,.02))-.15,4.));m=U(m,vec2(length(vec2(length(q.xy-vec2(0,1.30))-.17,q.z-.0))-.06,3.));
 m=U(m,vec2(sCap(q,vec3(0,1.,-.2),vec3(0,-.9,-.28),.05),3.));return m;}
void surf(vec3 p,vec3 n,int m,inout Surf s){if(m==6){s.ink=.6;}}
''', BRASS_PAL, bound=(0, -.2, 0, 2.2), human=False)

# a small standing lamp (samai): dish centre at the origin, radius 1, rim at y=.28, wick tip at (0, .48, .0); foot at y=-5
LAMP = Fig('samai', '''vec2 map(vec3 p){
 float a=atan(p.z,p.x),r=length(p.xz);float prof=.26*r*r;float d=max(abs(p.y-prof)-.05,r-1.);d=min(d,length(vec2(r-1.,p.y-.27))-.075);vec2 m=vec2(d*.7,3.);
 float n=24.,s=TAU/n;float b=mod(a+s*.5,s)-s*.5;m=U(m,vec2(length(vec3(r*cos(b)-.99,p.y-.13,r*sin(b)))-.07,3.));
 float st=r-(.17+.10*exp(-pow((p.y+.35)*4.,2.))+.16*exp(-pow((p.y+1.5)*3.2,2.))+.09*exp(-pow((p.y+2.7)*4.,2.))+.10*exp(-pow((p.y+3.6)*4.,2.)));st=max(st,max(p.y-.02,-5.-p.y));m=U(m,vec2(st*.6,3.));
 float ft=max(r-mix(1.15,.28,smoothstep(-5.,-4.25,p.y)),max(-5.-p.y,p.y+4.));m=U(m,vec2(ft*.6,3.));
 m=U(m,vec2(max(abs(p.y-.17)-.015,r-.9),14.));m=U(m,vec2(sCap(p,vec3(0,.16,.25),vec3(0,.44,.0),.06),13.));return m;}
void surf(vec3 p,vec3 n,int m,inout Surf s){}
''', BRASS_PAL, bound=(0, -2.4, 0, 3.4), human=False)


def flick(t, seed=0., k=1.):
    """a lamp's flicker, round 1"""
    return 1 + k * (.06 * noise1(t * 9, seed) + .04 * noise1(t * 19, seed + 3))


def curl(a, b, k):
    """a hand shape between two of rig.HANDS"""
    A, B = HANDS[a], HANDS[b]; m = lambda x, y: tuple((1 - k) * np.array(x, float) + k * np.array(y, float))
    return dict(c=[m(x, y) for x, y in zip(A['c'], B['c'])], sp=list(m(A['sp'], B['sp'])), th=m(A['th'], B['th']))


# ------------------------------------------------------------------ Ayodhya at night
from worlds import ayodhya as AY, flora as FLO, place
from chars import people as PP


def city(st, night=1., fill=.6, trees=1., upright=None, tint=(.9, .8, .75), tall=1.):
    """Ayodhya between open and close, without the sun's cast shadows; trees can lean back toward a camera above"""
    w = AY.MOOD['night']['w']; b = np.zeros((8, 4), 'f4')
    for i, q in enumerate(AY.BOATS[:8]): b[i] = q[:4]
    place.draw(st, 'ayodhya.glsl', u=dict(night=float(night), fill=float(fill), boats=b, skyA=hexc(w[0]), skyB=hexc(w[1]), skyC=(0., 0., 0.)), texs=dict(tCity=AY.tex()), sun=0.)
    if trees > 0 and tall > .05:
        for k, P in AY._trees().items(): FLO.scatter(st, k, P, AY.HGT[k] * tall, season='summer', seed=len(k), tint=tint, wind=.4, foot=.8, footCol=(2.6 * trees, .50 * trees, .06 * trees), upright=upright)


AMBER = '''
in vec2 uv;out vec4 o;uniform sampler2D tex;uniform float amt;
void main(){vec3 c=texture(tex,uv).rgb;float y=smoothstep(.25,.75,(min(c.r,c.g)-c.b)/max(max(c.r,c.g),.02));float m=max(c.r,c.g);vec3 a=vec3(m,m*.50,m*.10);o=vec4(mix(c,a,y*amt*smoothstep(.45,.95,c.g/max(c.r,.02))),1);}
'''


def amber(st, amt=1.):
    """the windows of the city come out lemon yellow: bring pure yellows back to lamp amber"""
    st.post_paint(AMBER, amt=float(amt))


def glows(st, P, size, minpx, alpha, col='#ffa64a', gain=1.5, seed=1, tw=.14, kind='lamp', soft=0.):
    """flames as points: size in world units, never smaller than minpx pixels; alpha scalar or N"""
    P = np.asarray(P, float); n = len(P); c = (P - st.cam.eye) @ st.cam.R.T; z = np.maximum(c[:, 2], 1.); px = st.cam.fl * 540 / z; al = np.broadcast_to(np.asarray(alpha, float), (n,))
    ph = np.random.default_rng(seed).uniform(0, 6.28, n); m = (c[:, 2] > 2) & (np.abs(c[:, 0]) * st.cam.fl < z * 1.85) & (np.abs(c[:, 1]) * st.cam.fl < z * 1.1) & (al > .004)
    fl = 1 - tw + tw * np.sin(st.t * 9 + ph) * np.sin(st.t * 5.3 + ph * 2); s = np.maximum(size * 2., np.asarray(minpx) * 2.2 / px); dim = np.clip(size * 2. * px / (np.asarray(minpx) * 2.2), .30, 1.) ** .55 if kind == 'lamp' else 1.
    if m.any(): FX.particles(st, P[m], s[m], np.array(hexc(col)) * gain, kind, seed=ph[m], alpha=(al * fl * dim)[m], soft=soft)


NIGHT_L = dict(inkRef=4.)
_LAMPERS = None


def people_tiles(bow=True):
    """(figure, pose, face) of the townspeople with lamps: 3 women, 3 men, 2 children; the same again half bowed and fully bowed"""
    F, M, K = PP.CITIZEN_F_LAMP, PP.CITIZEN_M_LAMP, [PP.CHILD_LAMP, PP.CHILD_B_LAMP]; joy = Face(smile=.7, lid=.9); out = []
    for lv in range(3 if bow else 1):
        for k, fig in enumerate(F + M + K):
            p = PP.P_LAMP.set(hedr=(0, 4, (k % 3 - 1) * 4), cher=(0, 0, (k % 2) * 4 - 2), lh=(.98, 10.0 + .35 * (k % 3), 2.0), rh=(-.98, 10.0 + .35 * (k % 3), 2.0))
            if lv: a = (12., 27.)[lv - 1]; d = (.5, 1.3)[lv - 1]; p = p.set(pel=(0, 8.3, -.35 * lv), pelr=(0, a * .7, 0), cher=(0, a, 0), hedr=(0, a * .9, 0), lh=(.98, 10. - 1.1 * lv, 2. + d), rh=(-.98, 10. - 1.1 * lv, 2. + d))
            p = sita.fit(p) if k < 3 else PP.child_pose(p) if k > 5 else p
            out.append((fig, p, joy if lv == 0 else Face(smile=.5, lid=.35)))
    return out


def flame_offset(fig, pose, yaw=0.):
    """where the diya's flame of a tile is, relative to the feet (figure units)"""
    from lau.stage import Solved
    S = Solved(solve(pose, fig.dim, fig.build), model(yaw=yaw), 1.); return PP.flame(S)


def glide(f, K):
    """a smooth curve through [(frame, value)], without the stops that keys() makes at every key"""
    T = np.array([k[0] for k in K], float); Y = np.array([np.atleast_1d(np.asarray(k[1], float)) for k in K]); n = len(T)
    if f <= T[0]: v = Y[0]
    elif f >= T[-1]: v = Y[-1]
    else:
        M = np.zeros_like(Y); s = np.diff(Y, axis=0) / np.diff(T)[:, None]
        for i in range(1, n - 1): a, b = T[i] - T[i - 1], T[i + 1] - T[i]; M[i] = (s[i - 1] * b + s[i] * a) / (a + b)
        M[0] = s[0] * .6; M[-1] = s[-1] * .35; i = int(np.searchsorted(T, f, 'right') - 1); h = T[i + 1] - T[i]; u = (f - T[i]) / h
        v = (2 * u ** 3 - 3 * u ** 2 + 1) * Y[i] + (u ** 3 - 2 * u ** 2 + u) * h * M[i] + (3 * u ** 2 - 2 * u ** 3) * Y[i + 1] + (u ** 3 - u ** 2) * h * M[i + 1]
    return v if len(v) > 1 else float(v[0])
