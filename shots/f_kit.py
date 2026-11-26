"""The war: what f1, f2, f3 and f7 share.  Sky and ground of the red plain, dust, heat, gold leaf, storms of arrows, baked hosts."""
from lau.shot import *
from lau.look import *
import moderngl as mgl

# ------------------------------------------------------------------ sky, light, ground
WAR = {**BLOOD, 'cZen': '#2c0714', 'cMid': '#94161a', 'cHor': '#e8742a', 'cLow': '#b0601f', 'sunCol': '#ff9a44', 'cLit': '#ff9a4a', 'cCM': '#b8342a', 'cSh': '#581226', 'cInk': '#240610', 'cov': .55, 'cy0': .02, 'cy1': .34, 'rays': .28, 'sunGlow': .55, 'halo': 1., 'sunR': .10}


def war_light(**k):
    return Light(**{**dict(key=(-.45, .55, .55), keyCol='#ffdca0', amb='#8a5a78', rim=(.3, .4, -.9), rimCol=(1.5, .75, .28), bounceCol=(.30, .13, .04), envT='#ffc890', envM='#ff9a50', envB='#8a3a20', fogCol='#e0803a', fog=(.0050, 50., .004, 0.), ink=3.2), **k})


GROUND = '''
#define TMAX 6000.
#define STEPS 90
#define RELAX 1.
#define NOAO
uniform vec3 gA,gB,gC;uniform vec4 hill[3];            // hill: x, z, radius, height (up to three mounds)
float hillH(vec2 q){float h=0.;for(int i=0;i<3;i++) if(hill[i].w>0.){float r=length((q-hill[i].xy)/vec2(hill[i].z,hill[i].z*.42))+.07*sin(q.x*.31)+.05*sin(q.y*.5);h=max(h,hill[i].w*smoothstep(1.2,.22,r));}return h;}
vec2 map(vec3 p){vec3 d=normalize(p-ro+vec3(0,-1e-5,0));float t=d.y<-1e-4?max(p.y,0.)/(-d.y):(p.y<.001?0.:1e4);float m=t;bool any_=hill[0].w>0.;
 if(any_){float h=hillH(p.xz)+.35*fbm(p.xz*.3)*smoothstep(.5,3.,hillH(p.xz));float dh=h>.05?(p.y-h)*.45:1e4;float bd=1e4;for(int i=0;i<3;i++) if(hill[i].w>0.){vec3 q=abs(p-vec3(hill[i].x,0.,hill[i].y))-vec3(hill[i].z*1.3,hill[i].w*1.1,hill[i].z*.6);bd=min(bd,max(q.x,max(q.y,q.z)));}m=min(m,bd>2.?bd:min(dh,max(1.5,bd)+1.5));}
 return vec2(m,1.);}
void surf(vec3 p,vec3 n,int m,inout Surf s){float v=fbm(p.xz*.045),w=fbm(p.xz*.35),d=length(p-ro);float H=hill[0].w>0.?hillH(p.xz):0.;
 vec3 c=mix(gA,gB,smoothstep(.30,.70,v));c*=.86+.34*w;
 vec4 vo=voro(p.xz*.22);float cr=smoothstep(.05,.0,vo.y)*smoothstep(.45,.62,fbm(p.xz*.03+9.))*smoothstep(260.,60.,d);c=mix(c,gC*.5,cr*.75);
 float st=smoothstep(.62,.70,vn(p.xz*vec2(1.7,.9)))*smoothstep(110.,20.,d);c=mix(c,gC,st*.35);
 s.base=c;s.sh=gC*.55;s.cls=1.;s.ink=0.;s.ns=vec3(0,1,0);
 if(H>.4){float e=.4;vec3 g=normalize(vec3(hillH(p.xz-vec2(e,0))-hillH(p.xz+vec2(e,0)),2.*e,hillH(p.xz-vec2(0,e))-hillH(p.xz+vec2(0,e))));s.ns=g;s.ink=.5;s.base*=.8;}}
'''


def ground(st, gA='#a85a28', gB='#7a3018', gC='#421416', hills=()):
    h = np.zeros((3, 4), 'f4')
    for i, q in enumerate(hills): h[i] = q
    st.world(GROUND, u=dict(gA=hexc(gA), gB=hexc(gB), gC=hexc(gC), hill=h))


def shaken(cam, f, amt, freq=.9, seed=0):
    """the same camera, shaken (world units)"""
    if amt <= 0: return cam
    x, y = shake(f, amt, freq, seed); o = cam.R[0] * x + cam.R[1] * y; c = Cam(cam.eye + o, cam.at + o, cam.fov); c.R = cam.R; return c


# ------------------------------------------------------------------ air
_HAZE = '''
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform sampler2D tex;uniform vec2 res,ctr;uniform float fT,amt,rad;
void main(){vec2 p=vec2(uv.x*res.x,(1.-uv.y)*res.y);float k=rad>0.?exp(-dot(p-ctr,p-ctr)/(rad*rad)):1.;vec2 q=p/res.y;
 vec2 d=vec2(fbm(q*vec2(9.,5.)+vec2(0.,fT*1.4))-.5,fbm(q*vec2(8.,5.)+vec2(5.,fT*1.6))-.5);o=texture(tex,uv+d*amt*k/res);}
'''


def haze(st, amt=8., at=(W / 2, H / 2), rad=0.):
    """hot air: the canvas shimmers"""
    if amt > .1: st.post_paint(_HAZE, amt=float(amt), ctr=tuple(map(float, at)), rad=float(rad))


_FOGBANK = '''
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform vec2 res;uniform float fT,amt,y0,y1,seed,speed;uniform vec3 cA,cB;
void main(){vec2 p=vec2(uv.x*res.x,(1.-uv.y)*res.y)/res.y;vec2 q=p*vec2(1.9,3.0)+vec2(seed-fT*speed,seed*.7+fT*.12);float n=fbm(q+.8*fbm(q*1.3+3.));n=n*.75+.25*fbm(q*3.1-fT*speed);
 float y=p.y;float prof=smoothstep(y0,y1,y+.42*(n-.5));float a=amt*prof*smoothstep(.18,.62,n+.35*prof);float l=smoothstep(.30,.72,fbm(q+vec2(.06,.10)));o=vec4(mix(cB,cA,l)*a,a);}
'''


def whip2(st, dx, dy=0.):
    """a whip without banding"""
    IM.whip(st, dx, dy); IM.whip(st, dx / 14., dy / 14.)


def vswing(t):
    """Hanuman's swing on a vanara's shorter legs"""
    from chars import hanuman as HM
    P = HM.H_SWING(t); k = -.62; return P.set(pel=(P.pel[0], P.pel[1] + k, P.pel[2]), lh=(P.lh[0], P.lh[1] + k, P.lh[2]), rh=(P.rh[0], P.rh[1] + k, P.rh[2]))


def dustbank(st, amt, y0=.55, y1=1.0, colA='#f0b060', colB='#8a3c1e', seed=0., speed=.25):
    """painted dust rising from the bottom of the frame: y0 clear .. y1 thick (fractions of the height, 0 top)"""
    if amt > .004: st.paint(_FOGBANK, 'over', amt=float(amt), y0=float(y0), y1=float(y1), seed=float(seed), speed=float(speed), cA=hexc(colA), cB=hexc(colB))


def puffs(st, P, size, age=0., col=('#d89a56', '#a85a2c'), alpha=.8, seed=0, soft=3.):
    """billows of dust at points P (N,3)"""
    P = np.asarray(P, float); n = len(P); r = np.random.default_rng(seed); k = r.uniform(0, 1, n)[:, None]; c = np.array(hexc(col[0])) * k + np.array(hexc(col[1])) * (1 - k)
    o = np.argsort(-((P - st.cam.eye) ** 2).sum(1)); s = np.broadcast_to(size, (n,)); a = np.broadcast_to(alpha, (n,))
    FX.particles(st, P[o], s[o], c[o], 'smoke', rot=r.uniform(-.5, .5, n)[o], seed=r.uniform(0, 1, n)[o], alpha=a[o], soft=soft)


def footdust(st, n, box, t, size=2.4, life=.9, col=('#d89a56', '#a85a2c'), alpha=.55, seed=0, rise=2.2, wind=(0, 0, 0)):
    """puffs that keep being kicked up inside a box"""
    r = np.random.default_rng(seed); a, b = np.array(box, float); ph = r.uniform(0, 1, n); u = t / life + ph; lf = u % 1.; k = np.floor(u); h = lambda s: np.modf(np.abs(np.sin(k * 12.9898 + ph * 78.2 + s) * 43758.5453))[0]
    P = a + (b - a) * np.stack([h(1.), h(2.), h(3.)], 1); P = P + np.asarray(wind, float) * (lf * life)[:, None]; P[:, 1] += rise * lf ** .7
    puffs(st, P, size * (.35 + .9 * lf ** .6), col=col, alpha=alpha * np.minimum(1, lf * 7) * (1 - lf) ** 1.2, seed=seed)


def ring_burst(st, at, t, speed=40., n=46, size=5., col=('#e8b070', '#a85a2c'), life=1.0, seed=0, up=.25, drag=2.2):
    """dust thrown out along the ground in a ring"""
    if t < 0 or t > life: return
    r = np.random.default_rng(seed); an = r.uniform(0, 6.283, n); sp = speed * r.uniform(.5, 1., n); g = (1 - math.exp(-drag * t)) / drag; P = np.asarray(at, float) + np.stack([np.cos(an) * sp * g, up * sp * g * r.uniform(.2, 1, n) + .3, np.sin(an) * sp * g], 1)
    puffs(st, P, size * (.5 + 1.4 * (t / life) ** .5) * r.uniform(.6, 1.3, n), col=col, alpha=.9 * (1 - t / life) ** .8, seed=seed)


def leafburst(st, at, t, speed=14., n=90, size=.16, seed=0, grav=9., life=1.1, sparks=True, spread=(1, 1, 1), up=.2):
    """what a blow looks like in this film: gold leaf and sparks"""
    if t < 0: return
    FX.burst(st, n, at, t, speed=speed, grav=grav, size=size, seed=seed, col='#ffcf6a', kind='flake', life=life, spread=spread, up=up, drag=2.0)
    if sparks: FX.burst(st, n // 2, at, t, speed=speed * 1.8, grav=grav * .6, size=size * .6, seed=seed + 1, col='#ffb050', kind='streak', life=life * .55, spread=spread, up=up)
    if t < .13: FX.particles(st, np.asarray(at, float)[None], speed * (.28 - 1.2 * t), '#fff0c8', 'spark', alpha=1 - t / .13)


_ROCK = {}


def boulder(st, at, r, seed=0, spin=0., axis=(.3, 1., .2), col=('#a08a78', '#4a3a40', '#2a1c1c')):
    """a facetted stone"""
    if seed not in _ROCK:
        q = np.random.default_rng(seed); D = q.normal(size=(15, 3)); D /= np.linalg.norm(D, axis=1, keepdims=True); d = q.uniform(.74, 1., 15)

        def fn(u, v):
            a, b = u * 6.28319, (v - .5) * 3.14159; n = V(math.cos(a) * math.cos(b), math.sin(b), math.sin(a) * math.cos(b)); k = D @ n; return n * min(1.12, float(np.where(k > .05, d / np.maximum(k, 1e-3), 9.).min()))
        _ROCK[seed] = CL.sheet(fn, 40, 22)
    p, n, uv, ix = _ROCK[seed]; a = np.asarray(axis, float); a /= np.linalg.norm(a); c, s_ = math.cos(spin), math.sin(spin); K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]]); R = np.eye(3) + s_ * K + (1 - c) * K @ K
    st.mesh(p @ R.T * r + np.asarray(at, float), -n @ R.T, uv, ix, kind=0, col=col, cls=1, ink=.9)


_SUN = '''
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform vec2 res,ctr;uniform float fT,R,amt,rays,ring;uniform vec3 col;
void main(){vec2 p=(vec2(uv.x*res.x,(1.-uv.y)*res.y)-ctr)/R;float r=length(p),a=atan(p.y,p.x);vec3 c=col*(exp(-max(r-1.,0.)*1.6)*.30+exp(-max(r-1.,0.)*.45)*.14);
 float ry=smoothstep(-.1,.2,sin(a*20.+fT*.15))*.6+smoothstep(.3,.5,sin(a*9.-fT*.1))*.5;c+=col*ry*rays*exp(-r*.28)*smoothstep(1.,1.6,r)*.30;
 float d=smoothstep(1.02,.985,r);float hb=smoothstep(.025,.0,abs(r-1.35))+smoothstep(.018,.0,abs(r-1.58));float n=26.;float bd=smoothstep(.055,.03,length(vec2((fract(a*n/TAU)-.5)*TAU/n*r,r-1.465)));
 float pt=abs(fract(a*36./TAU)-.5);float pe=smoothstep(.02,.0,abs(r-1.78-.10*cos(pt*PI))-.006);c+=col*(hb+bd+pe*.7)*ring*.55;o=vec4(mix(c,col*1.45,d)*amt,d*amt);}
'''


def sun(st, at, r, amt=1., rays=.6, ring=1., col='#ff9a44'):
    """a round painted sun with its mural ring at a pixel, for high suns that the sky's own map would stretch"""
    st.paint(_SUN, 'over', ctr=tuple(map(float, at)), R=float(r), amt=float(amt), rays=float(rays), ring=float(ring), col=hexc(col))


# ------------------------------------------------------------------ silhouettes baked to a texture
def silhouette(st, draw, cam, w=512, h=512):
    """white-on-alpha texture of draw(st) seen from cam (in setup only: every texture is new)"""
    from chars import ravana as RV
    st.clear('#000'); st.open(cam, RV.silhouette('#ffffff')); draw(st); st.close(alpha=0.)
    c = gl.ctx(); t = c.texture((w, h), 4, dtype='f1'); t.repeat_x = t.repeat_y = False; fb = c.framebuffer([t])

    class T: width, height = w, h; use = staticmethod(fb.use)
    gl.draw(gl.program('in vec2 uv;out vec4 o;uniform sampler2D tex;uniform float asp;\nvoid main(){vec2 u=vec2((uv.x-.5)*asp+.5,uv.y);o=vec4(texture(tex,u).a);}\n'), T, dict(asp=float(w / h * H / W)), dict(tex=st.L.color_attachments[0]))
    t.build_mipmaps(); t.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR); return t


# ------------------------------------------------------------------ hosts
ROAR = Face(frown=.8, mouth=.45, teeth=.8, smile=0)


def vanara_host(st, yaw=68, pitch=8., px=360, phases=4):
    from chars import vanara as VN
    K = [(VN.WARRIOR, 3), (VN.LANGUR, 2), (VN.YOUTH, 1), (VN.WARRIOR2, 2), (VN.YOUTH2, 3), (VN.LANGUR2, 1), (VN.JAMBAVAN, 0)]
    it = [(VN.arm(g, h, p / phases), (VN.V_CHARGE if h else VN.V_RUN)(p / phases + k * .07), ROAR, yaw) for k, (g, h) in enumerate(K) for p in range(phases)]
    c = Crowd(st, it, px=px, pitch=pitch, box=(-7, -.6, 7, 19)); c.kinds, c.ph = len(K), phases; return c


def rakshasa_host(st, yaw=-62, pitch=8., px=360, phases=4):
    from chars import rakshasa as RK
    K = [RK.TUSK, RK.HORN, RK.SPEARMAN, RK.HULK, RK.HORN_SPEAR, RK.SWORDSMAN]
    it = [(g, RK.K_RUN(p / phases + k * .17), ROAR, yaw) for k, g in enumerate(K) for p in range(phases)]
    c = Crowd(st, it, px=px, pitch=pitch, box=(-7, -.6, 7, 19)); c.kinds, c.ph = len(K), phases; return c


class Host:
    """a scattered army: pos (N,3), and what each one is"""

    def __init__(s, crowd, pos, seed=0, scale=(.9, 1.15)):
        r = np.random.default_rng(seed); s.cr, s.pos, s.n = crowd, np.asarray(pos, float), len(pos); s.kind = r.integers(0, crowd.kinds, s.n); s.phase = r.uniform(0, crowd.ph, s.n); s.sc = r.uniform(*scale, s.n); s.tint = np.clip(r.normal(1, .10, (s.n, 1)) + r.normal(0, .035, (s.n, 3)), .7, 1.25)

    def draw(s, steps, off=(0, 0, 0), flip=1., mask=None, tint=1., y=None):
        """steps = run phase in tiles (advance about .5 per frame)"""
        m = slice(None) if mask is None else mask; P = s.pos + np.asarray(off, float)
        if y is not None: P = P.copy(); P[:, 1] = y(P)
        s.cr.draw(P[m], scale=s.sc[m], tile=(s.kind * s.cr.ph + np.floor(s.phase + steps).astype(int) % s.cr.ph)[m], tint=(s.tint * np.asarray(tint))[m], flip=flip)


# ------------------------------------------------------------------ arrows
def arrow_lines(c, A, B, w=2.2, col=(.06, .02, .03), head=None, fletch=None, alpha=1.):
    """many arrows on a cairo context: A tails, B tips (N,2) px, w = shaft width (scalar or N)"""
    A, B = np.asarray(A, float), np.asarray(B, float); d = B - A; L = np.linalg.norm(d, axis=1, keepdims=True) + 1e-6; d = d / L; nrm = np.c_[-d[:, 1], d[:, 0]]; w = np.broadcast_to(w, (len(A),))
    head, fletch = head or col, fletch or col
    for a, b, u, m, k, l in zip(A, B, d, nrm, w, L[:, 0]):
        if l < 2: continue
        c.set_source_rgba(*col, alpha); c.set_line_width(k); c.move_to(*a); c.line_to(*(b - u * k * 2)); c.stroke()
        c.set_source_rgba(*head, alpha); q = b - u * k * 5.2; c.move_to(*b); c.line_to(*(q + m * k * 1.9)); c.line_to(*(q + u * k * 1.2)); c.line_to(*(q - m * k * 1.9)); c.close_path(); c.fill()
        c.set_source_rgba(*fletch, alpha)
        for s in (1, -1): e = a + u * min(l * .24, k * 9); c.move_to(*(a + u * k)); c.line_to(*(a - u * k * 1.5 + m * s * k * 2.4)); c.line_to(*(e - u * k * 2 + m * s * k * 2.1)); c.line_to(*e); c.close_path(); c.fill()
