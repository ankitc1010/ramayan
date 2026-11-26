"""What the forest shots (b3 b4 c1 c2 c3) share: walks whose feet stay where they are put down, the exiles' dress and arms, painted shafts of light, reflections in water, a trunk that wipes the frame."""
from lau.shot import *
from lau.rig import Rx
from lau.look import *
from chars import rama, sita
from worlds import forest as FO, flora as FL

# ------------------------------------------------------------------ walking and running


def stance_foot(q, duty, dist, fs=1., roll=30., heel=-15., swing_lift=.75, swing_pitch=42.):
    """ankle (z, y) relative to the body and foot pitch at phase q of one foot (0 = heel down).  The body covers `dist` per cycle; while the foot is down its toe (or heel) does not move over the ground."""
    q %= 1.; z0 = dist * duty / 2; toe, ty, hl, hy = 1.42 * fs, -.52 * fs, -.34 * fs, -.50 * fs; base = .23 + .52 * fs
    flat = lambda zz: (zz, base)
    def on_toe(zz, p): c, s = math.cos(math.radians(p)), math.sin(math.radians(p)); return zz + toe - (ty * s + toe * c), base + ty - (ty * c - toe * s)
    def on_heel(zz, p): c, s = math.cos(math.radians(p)), math.sin(math.radians(p)); return zz + hl - (hy * s + hl * c), base + hy - (hy * c - hl * s)
    if q < duty:
        z = z0 - dist * q; u = q / duty
        if u < .16: p = heel * (1 - u / .16); return (*on_heel(z, p), p)
        if u > .62: p = roll * ((u - .62) / .38) ** 1.5; return (*on_toe(z, p), p)
        return (*flat(z), 0.)
    u = (q - duty) / (1 - duty); a = on_toe(-z0, roll); b = on_heel(z0, heel); e = u * u * (3 - 2 * u)
    p = keys(u, [(0., roll), (.22, swing_pitch), (.72, -2.), (1., heel)])
    return a[0] + (b[0] - a[0]) * e, a[1] + (b[1] - a[1]) * u + swing_lift * math.sin(math.pi * min(1., u ** .8)), p


def stride_pose(ph, dist=8.4, duty=.60, pel=8.30, drop=.40, yaw=9., sway=.12, lean=2., arms=1.25, hip=.42, fs=1., lift=.62):
    """a walk along +z; ph counts cycles (two steps), left heel comes down at whole numbers"""
    a = 2 * math.pi * ph; c, s = math.cos(a), math.sin(a); L = stance_foot(ph, duty, dist, fs, swing_lift=lift); R = stance_foot(ph + .5, duty, dist, fs, swing_lift=lift)
    y = pel - drop * (.5 + .5 * math.cos(2 * a - .55))
    return Pose(pel=(sway * math.sin(a - .4), y, 0), pelr=(-yaw * c, lean, 2.4 * math.sin(a - .4)), cher=(yaw * 1.55 * c, lean * .6, -2.4 * math.sin(a - .4)), hedr=(-yaw * .6 * c, -lean * 1.2 + 1.2 * math.cos(2 * a - 1.2), 0),
                lf=(hip, L[1], L[0]), rf=(-hip, R[1], R[0]), lft=(5, L[2]), rft=(-5, R[2]), lkn=(.10, 0, 1), rkn=(-.10, 0, 1),
                lh=(2.0, y + .0 + .22 * abs(c), .35 - arms * math.cos(a - .25)), rh=(-2.0, y + .0 + .22 * abs(c), .35 + arms * math.cos(a - .25)), lel=(.35, 0, -1), rel=(-.35, 0, -1))


def run_pose(ph, dist=26., lean=24.):
    """a sprint along +z; `dist` per cycle of two strides, left foot strikes at whole numbers; both feet leave the ground"""
    duty = .26; a = 2 * math.pi * ph; c, s = math.cos(a), math.sin(a)

    def foot(q):
        q %= 1.; z0 = dist * duty / 2 - .25
        if q < duty:
            u = q / duty; z = z0 - dist * q; p = 34 * max(0., (u - .45) / .55) ** 1.3; cc, ss = math.cos(math.radians(p)), math.sin(math.radians(p)); return z + 1.42 - (-.52 * ss + 1.42 * cc), .75 - .52 + .52 * cc + 1.42 * ss, p
        u = (q - duty) / (1 - duty); z1 = z0 - dist * duty; z = keys(u, [(0., z1), (.30, z1 - .3), (.72, z0 * .95), (.88, z0 + .55), (1., z0)]); y = keys(u, [(0., 1.5), (.26, 4.1), (.55, 3.4), (.82, 1.35), (1., .75)]); p = keys(u, [(0., 34.), (.25, 78.), (.6, 42.), (.9, -10.), (1., 0.)]); return z, y, p
    L, R = foot(ph), foot(ph + .5); b = math.cos(2 * (a - 2 * math.pi * (duty / 2)))        # low at mid stance
    return Pose(pel=(0, 7.55 - .42 * b, 0), pelr=(-15 * math.cos(a - .5), lean * .55, 0), cher=(30 * math.cos(a - .5), lean * .5, 0), hedr=(-15 * math.cos(a - .5), -lean * .8, 0), lf=(.42, L[1], L[0]), rf=(-.42, R[1], R[0]), lft=(3, L[2]), rft=(-3, R[2]), lkn=(.08, 0, 1), rkn=(-.08, 0, 1),
                lh=(1.55, 9.9 + .7 * c, 1.1 - 2.4 * math.cos(a - .3)), rh=(-1.55, 9.9 - .7 * c, 1.1 + 2.4 * math.cos(a - .3)), lel=(.5, -.3, -1), rel=(-.5, -.3, -1), lhand='fist', rhand='fist')


# ------------------------------------------------------------------ the exiles
SASH = dict(rama=(('#c8431f', '#4a1020', '#f2c24a'), ('#e8a22c', '#7a3a14', '#b3202a')), lak=(('#b5303a', '#4a0f1c', '#f2d28a'), ('#efe6d2', '#9a7f86', '#b5303a')))


def quiver(st, S, side=1): st.fig(PR.QUIVER, M=PR.place(S.chest((.5 * side, .45, -1.2)), S.d(V(-.35 * side, 1, -.12) @ S.u['Bc']), S.d(V(0, 0, -1) @ S.u['Bc']), S.Sc))


def back_bow(st, S, side=1, half=4.4, pull=1.0):
    """the bow slung across the back"""
    b = PR.BOW.variant(u=dict(pr=np.array([pull, half] + [0] * 14, 'f4'))); st.fig(b, M=PR.place(S.chest((-.1 * side, .1, -1.65)), S.d(V(.62 * side, 1, -.10) @ S.u['Bc']), S.d(V(0, -.05, -1) @ S.u['Bc']), S.Sc))


def held_bow(st, S, side='R', half=4.5, up=(0, 1, 0), fwd=None, pull=1.0):
    """the bow carried in one hand, unstrung from the shot"""
    g = S.palm(side, .0, .62, .30); b = PR.BOW.variant(u=dict(pr=np.array([pull, half] + [0] * 14, 'f4'))); st.fig(b, M=PR.place(g, np.asarray(up, float), np.asarray(fwd if fwd is not None else S.d((0, 0, 1)), float), S.Sc))


def sashes(st, solve_at, t, who='rama', wind=(-.55, -.05, 0), wave=.7, k=1., grav=.45, n=14):
    """two loose ends of cloth: from the shoulder and from the hip.  solve_at(t) -> Solved at an earlier time (they remember where the body was)"""
    memo = {}
    def S(tt):
        q = round(tt * 48); memo.setdefault(q, solve_at(q / 48.)); return memo[q]
    for j, (an, ln, wd, col) in enumerate(((lambda tt: S(tt).chest((1.05, 1.25, -.75)), 6.8 * k, 1.15, SASH[who][0]), (lambda tt: S(tt).pelvis((-.75, .45, -.75)), 5.6 * k, .85, SASH[who][1]))):
        Q = CL.lag(an, t, n=n, length=ln, delay=.028, wind=wind, grav=grav, wave=.15, freq=1.1, phase=j * 2.1); u = np.linspace(0, 1, n); T = np.gradient(Q, axis=0); T /= np.linalg.norm(T, axis=1, keepdims=True); N = np.cross(T, V(0, 0, 1)); ph = 6.283 * (1.25 * u - 1.35 * t) + j * 2.1
        Q = Q + N * (wave * ln * .13 * u * np.sin(ph))[:, None] + V(0, 0, 1) * (wave * ln * .10 * u * np.cos(ph * .8 + 1.))[:, None]
        st.mesh(*CL.strip(Q, np.interp(u, [0, .15, .75, 1], [wd * .45, wd * .8, wd, wd * .82]), up=(.1, 1, .5), m=7, curl=.10, twist=np.interp(np.linspace(0, 1, 40), [0, 1], [0., .9]) * math.sin(t * 3 + j), n=40), kind=1, col=col, cls=8)


def shawl(st, S, t, r=1.75, length=5.2, col=('#7a3a4a', '#3a1626', '#e0b060'), open_=62., wind=(-.5, 0, 0), flow=.5, kind=1, top=1.05, lean=0.):
    """a wool wrap round the shoulders, open in front, its hem lagging in the wind (wind in world space)"""
    C = S.u['Bc'].T; w = S.Mf[:3, :3].T @ np.asarray(wind, float) / S.Sc

    def fn(u, v):
        a = math.radians(open_ + u * (360 - 2 * open_)); e = v ** 1.1; sh = math.sin(a); cs = math.cos(a); rr = r * (.50 + .50 * min(1., v * 3.2) ** .6) * (1 + .18 * v); fold = .10 * math.sin(a * 9 + 2.) * v
        y = top + .62 * (1 - min(1., v * 3.)) ** 1.4 - length * max(0., v - .12) + .16 * math.sin(a * 5 + t * 5) * v
        p = V((rr + fold) * sh * 1.12, y, (rr * .86 + fold) * cs - .12) + w * length * flow * e * e * (1 + .35 * math.sin(t * 6.5 - v * 4 + a * 2)); return S.w(S.J[1] + (C @ p if v < .3 else (C @ p) * (1 - .0) ))
    st.mesh(*CL.sheet(fn, 44, 14), kind=kind, col=col, cls=1, u=dict(rep=(20., 3., 0, 0)))


# ------------------------------------------------------------------ things done to the picture
_SHAFT = '''
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform vec2 res,src;uniform float fT,amt,near_,far_,dens,seed,wid;uniform vec3 col;uniform sampler2D tZ;
void main(){vec2 p=vec2(uv.x*res.x,(1.-uv.y)*res.y);vec2 q=(p-src)/res.y;float a=atan(q.x,q.y),r=length(q);
 float k=0.;for(int i=0;i<3;i++){float f=dens*(1.+.9*float(i));float x=a*f+seed+float(i)*7.3;float id=floor(x);float h=h11(id+seed*3.);float w=abs(fract(x)-.5);float on=step(.46,h);float br=.75+.25*sin(fT*.9+h*20.);
   k+=on*smoothstep(wid*(.28+.2*h),wid*.02,w)*br*(.60-.14*float(i));}
 k*=smoothstep(.02,.45,r)*smoothstep(1.75,.55,r);k*=.78+.35*fbm(p/res.y*vec2(5.,3.)+vec2(fT*.10,-fT*.05));
 float z=texture(tZ,uv).x;k*=smoothstep(near_,far_,min(z,5e4));o=vec4(col*k*amt,0.);}
'''


def shafts(st, src, amt=.5, col='#ffd98a', near=20., far=90., dens=9., seed=1., wid=1.):
    """painted shafts of light falling from pixel `src`; far things get all of it, near things little"""
    st.paint(_SHAFT, 'add', src=tuple(map(float, src)), amt=float(amt), col=hexc(col), near_=float(near), far_=float(far), dens=float(dens), seed=float(seed), wid=float(wid))


_WATER = '''
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform sampler2D tex;uniform vec2 res;uniform float y0,fT,camx,amp,sq;uniform vec3 deep,sheen;
void main(){vec2 p=vec2(uv.x*res.x,(1.-uv.y)*res.y);vec3 c=texture(tex,uv).rgb;float edge=y0+5.*sin((p.x+camx)*.011)+3.*sin((p.x+camx)*.031+1.);float d=p.y-edge;
 if(d>0.){float u=d/(res.y-y0);vec2 w=vec2((p.x+camx)/mix(150.,420.,u),d/mix(9.,26.,u)-fT*1.4);float n=fbm(w)-.5,n2=vn(w*vec2(2.3,1.7)+fT*.8)-.5;
  vec2 q=vec2(p.x+n*amp*(8.+60.*u),edge-d*sq+n2*amp*(3.+16.*u));vec3 r=vec3(0.);for(int i=0;i<5;i++){r+=texture(tex,vec2((q.x+(float(i)-2.)*1.5*(1.+3.*u))/res.x,1.-clamp(q.y,2.,res.y)/res.y)).rgb;}r/=5.;
  float fr=mix(.82,.50,u);vec3 b=mix(deep,r,fr);float gl=smoothstep(.16,.30,n+.5*n2)*smoothstep(0.,.1,u);b+=sheen*gl*(.35+.4*u);b=mix(b,deep*.35,smoothstep(5.,0.,d)*.8);b+=sheen*smoothstep(2.5,0.,abs(d-9.-4.*n2))*.5;c=b;}
 o=vec4(c,1);}
'''


def water(st, y0, camx, deep='#1c4a56', sheen='#ffd890', amp=1., sq=1.):
    """below pixel row y0 the picture becomes water that mirrors what stands above the bank"""
    st.post_paint(_WATER, y0=float(y0), camx=float(camx), deep=hexc(deep), sheen=hexc(sheen), amp=float(amp), sq=float(sq))


_TRUNK = '''
in vec2 uv;out vec4 o;uniform sampler2D tex_;uniform vec2 res,sz;uniform float cx,blur,lean,shade,y;uniform vec3 tint,rimc;
void main(){vec2 p=vec2(uv.x*res.x,(1.-uv.y)*res.y);vec4 s=vec4(0);for(int i=0;i<27;i++){float k=(float(i)/26.-.5)*blur;vec2 q=vec2(p.x+k-cx-lean*(p.y-res.y*.5),p.y-res.y*.5+y)/sz+.5;vec4 t=(q.x<0.||q.x>1.)?vec4(0):texture(tex_,vec2(q.x,q.y));t.rgb=pow(t.rgb/max(t.a,.01),vec3(2.2))*t.a;float e=abs(q.x-.5)*2.5;t.rgb*=mix(1.,.30,smoothstep(.45,1.,e));t.rgb=mix(t.rgb,rimc*t.a,smoothstep(.80,.98,e)*step(q.x,.5)*.8);s+=t;}
 s/=27.;o=vec4(s.rgb*tint*shade,s.a);}
'''


def trunk(st, cx, season, wide=1300., blur=110., lean=.06, shade=.5, var=0, tint=(1, 1, 1), rim=(0, 0, 0), y=0.):
    """a great near trunk with its axis at pixel cx, smeared by its own speed"""
    pl = FL.plate_of('trunk_wide', season, var); st.paint(_TRUNK, 'over', texs=dict(tex_=pl.tex), cx=float(cx), sz=(float(wide), float(wide * pl.h / pl.w)), blur=float(blur), lean=float(lean), shade=float(shade), tint=hexc(tint), rimc=hexc(rim), y=float(y))


_JOIN = '''
in vec2 uv;out vec4 o;uniform sampler2D tex,tA;uniform vec2 res;uniform float cx,lean;
void main(){vec2 p=vec2(uv.x*res.x,(1.-uv.y)*res.y);float x=cx+lean*(p.y-res.y*.5);o=p.x<x?texture(tA,uv):texture(tex,uv);}
'''


def keep(st, slot):
    """copy the canvas into a texture held by `slot` (a dict)"""
    if 'tex' not in slot: slot['tex'] = gl.ctx().texture((st.pw, st.ph), 4, dtype='f2'); slot['fbo'] = gl.ctx().framebuffer([slot['tex']])
    gl.ctx().copy_framebuffer(slot['fbo'], st.C.fbo); return slot['tex']


def join(st, before, cx, lean=.06):
    """left of the line cx the older picture, right of it the canvas as it is"""
    st.post_paint(_JOIN, texs=dict(tA=before), cx=float(cx), lean=float(lean))


def quad(st, tex, at, w, h, right=(1, 0, 0), up=(0, 1, 0), col=((1, 1, 1), (.5, .5, .5)), part=1., cut=.4):
    """a painted plate standing in 3-D, centre at `at`"""
    r, u = np.asarray(right, float), np.asarray(up, float); at = np.asarray(at, float); P = np.array([at - r * w / 2 - u * h / 2, at + r * w / 2 - u * h / 2, at + r * w / 2 + u * h / 2, at - r * w / 2 + u * h / 2]); N = np.tile(nz(np.cross(r, u)), (4, 1)); st.mesh(P, N, np.array([[0, 0], [1, 0], [1, 1], [0, 1.]]), np.array([[0, 1, 2], [0, 2, 3]]), kind=3, col=(col[0], col[1], (1, 1, 1)), cls=6, ink=0, part=part, texs=dict(tCard=tex), u=dict(cutoff=float(cut)))


def foreground(st, s, x0, x1, seed=9, blur=1.6, zg=33., low=-6.2, hgt=8.5, step=34., keep_=.6, leaves=True, zl=36.):
    """after close: leaf and grass silhouettes between the lens and the walkers, kept low so that feet are seen"""
    for i in range(int(math.floor(x0 / step)) - 1, int(math.ceil(x1 / step)) + 2):
        r = np.random.default_rng([seed, i & 0xffff]); X = (i + r.uniform(0, 1)) * step
        if r.uniform() > keep_: continue
        P = (X, low, zg); k = hgt * r.uniform(.75, 1.25) * st.cam.px(P) / (560 * .8); x, y, _ = st.cam.project(P)
        if -900 < x < 2820: FL.frame(st, 'fg_grass', x, max(y, 1086), k, s, int(r.integers(2)), lod=blur)
    if leaves and s != 'winter':
        for i in range(int(math.floor(x0 / 22)) - 1, int(math.ceil(x1 / 22)) + 2):
            r = np.random.default_rng([seed + 77, i & 0xffff]); X = (i + r.uniform(0, 1)) * 22
            if r.uniform() > .62: continue
            x, y, _ = st.cam.project((X, 24., zl)); k = 5.6 * st.cam.px((X, 24., zl)) / 1000 * r.uniform(.8, 1.2)
            if -1400 < x < 2600: FL.frame(st, 'fg_leaves', x, -60 - 120 * r.uniform(), k, s, int(r.integers(2)), lod=blur + .5, flip=bool(r.integers(2)), rot=r.uniform(-6, 6) + 1.5 * math.sin(st.t * 2 + i))


# ------------------------------------------------------------------ the deep wood of c1 and c2
WOOD = dict(sky=dict(cZen='#0f5a48', cMid='#4fa468', cHor='#d2cf86', cLow='#8fb468', sunDir=(-.30, .22, -1.), sunCol='#fff4c0', sunR=0., sunGlow=.6, rays=0., halo=0., cov=0.), mist='#cfe08a', gA='#b8b04a', gB='#3f7a3a')


def wood_light(**k):
    return Light(**{**dict(key=(-.45, .72, .38), keyCol='#ffeab0', amb='#4f9078', rim=(-.35, .5, -.8), rimCol=(1.5, 1.15, .5), bounceCol=(.10, .16, .05), envT='#fff4c8', envM='#ffd45a', envB='#2a6a44', fogCol='#b8d488', fog=(.0026, 70., .004, 0.), inkRef=1.1, inkCol='#08140e'), **k})


def wood(st, x0, x1, seed=1, dark=1., clear=(-14., 16.), near=True, rows=((-150, 34, .58), (-95, 34, .36), (-58, 30, .16)), kinds=('banyan', 'mango', 'pahari_round', 'kadamba'), mist=None, ground=True, under=1.):
    """ground, three planes of great trees and undergrowth between x0 and x1, all a function of world x; `clear` = the x range kept open at the near plane"""
    m = mist or WOOD['mist']; T = tuple(dark * v for v in (.80, .96, .86)); d = FO.S['summer']
    if ground: FO.place.draw(st, FO.GROUND, u=dict(gA=WOOD['gA'], gB=WOOD['gB'], leafA=FL.GREEN['summer'][3], mist=m, snow=0., wet=0., river=0.), sun=0.)
    def row(z, step, kk, hh, haze, sd, jz=6., vary=.2, tint=T, skip=None, **q):
        for i in range(int(math.floor(x0 / step)) - 1, int(math.ceil(x1 / step)) + 2):
            r = np.random.default_rng([seed * 17 + sd, i & 0xffff]); X = (i + r.uniform(.1, .9)) * step
            if skip and skip[0] < X < skip[1]: continue
            k = kk[int(r.integers(len(kk)))]; yield k, (X, -.3, z + r.uniform(-jz, jz)), hh * r.uniform(1 - vary, 1 + vary), int(r.integers(6)), 1. if r.uniform() > .5 else -1., r.uniform(0, 6.28), haze, tint
    L = []
    for j, (z, step, hz) in enumerate(rows): L += list(row(z, step, kinds, 76 + 8 * (j == 0), hz, 3 + j, skip=(None if j < 2 else clear)))
    for z, step, hz in ((-72, 12, .20), (-44, 11, .07), (-24, 10, 0.), (-13, 11, 0.)): L += list(row(z, step, ('shrub', 'fern', 'fern', 'grass'), 9 if z < -20 else 5.2, hz, abs(z), jz=4., vary=.35, skip=None if z < -14 or not clear else (clear[0] * .4, clear[1] * .4), tint=tuple(under * v for v in T)))
    if near: L += list(row(-20, 46, ('banyan', 'mango'), 70, 0., 91, jz=3., skip=clear, tint=tuple(.62 * v for v in T)))
    B = {}
    for k, *q in L: B.setdefault((k, q[2] % FL.KINDS[k][6]), []).append(q)
    for (k, v), Q in B.items(): FL.cards(st, FL.plate_of(k, 'summer', v), [q[0] for q in Q], [q[1] for q in Q], np.array([q[3] for q in Q]), phase=np.array([q[4] for q in Q]), haze=np.array([q[5] for q in Q]), hazeCol=m, tint=np.array([q[6] for q in Q]), wind=.5)
