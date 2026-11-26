"""Forests: layered painted planes with mist between.

    from worlds import forest as FO
    FO.SEASONS 'spring' 'summer' 'monsoon' 'autumn' 'winter'
b3, lateral track: the walkers go toward +x on the path z = 0 (ground y = 0); camera looks along -z from z about +62, x moving.
    st.paint('sky.frag', **FO.sky(s)); st.open(cam, FO.light(s)); FO.track(st, s, x0, x1, seed=); <figures at z = 0>; st.close(); FO.near(st, s, x0, x1); FO.drift(st, s)
    track draws ground, far hills, three planes of trees (z -40..-260), undergrowth, the near bank; near() lays the front plane (z = +18..+40, blurred leaves and grass) in its own layer over the figures.
    FO.wipe(st, season, u) -> a huge trunk crossing the frame, u 0..1 from the right edge to the left (put the season cut at u = .5 when it fills the frame).
clearing (b4, c1..c5, c7): FO.clearing(st, mood='day'|'night'|'rain'|'evening', season=, fire=0..1, line=0..1) = hut.glsl + trees round it.  Cameras: (26,9,62)->(4,12,0) fov 36 ; (0,14,90)->(0,16,0) ; from the door (4,12,14)->(-10,8,70).
grove (d6): FO.grove(st) : ashoka trees by moonlight, seat of Sita under the great tree at (0,0,0).  Cameras: (30,16,70)->(2,22,0) fov 36 ; (-18,9,34)->(2,10,0).
All take st inside open/close and use FL.scatter; every placement is a fixed function of seed, so any frame renders alone."""
import numpy as np, math
from lau.stage import Light, hexc
from lau.look import *
from lau import fx as FX, cloth as CL
from . import place, flora as FL

S = dict(
    spring=dict(sky=dict(cZen='#5c9ac0', cMid='#a8d4cc', cHor='#fbe6c8', cLow='#f0dcc0', sunDir=(-.5, .5, -1.), sunCol='#fff2d0', sunR=.0, rays=.5, halo=0., cov=.35, cLit='#fffaf0', cCM='#f6d4cc', cSh='#c8a0b4', cInk='#6a5470', cink=.4), haze='#f2dcc8', gA='#c8c878', gB='#7f9a52', mist='#f8e8d0', kinds=('pahari_round', 'mango', 'bare'), under=('shrub', 'grass', 'fern'), key='#fff0d0', amb='#b8b0c8', tr=(1, .97, .95)),
    summer=dict(sky=dict(cZen='#3f86c0', cMid='#8cc8d8', cHor='#f4ecc0', cLow='#e0dca8', sunDir=(-.5, .6, -1.), sunR=0., rays=.5, halo=0., cov=.3), haze='#dce8c0', gA='#c8b068', gB='#86883e', mist='#eef0cc', kinds=('mango', 'banyan', 'ashoka', 'palm'), under=('shrub', 'grass', 'fern'), key='#fff0c0', amb='#9fb0c0', tr=(1, 1, 1)),
    monsoon=dict(sky=dict(cZen='#24343f', cMid='#3f5c62', cHor='#a8c8bc', cLow='#6a8c80', sunGlow=.0, sunR=0., rays=0., halo=0., cov=.95, cLit='#9ab4ac', cCM='#5f7f80', cSh='#33505a', cInk='#14262c', cink=.6), haze='#7fa298', gA='#4f7a44', gB='#21503a', mist='#bcd6ca', kinds=('kadamba', 'banyan', 'bamboo', 'plantain'), under=('fern', 'grass', 'shrub'), key='#e4f2e8', amb='#8cb0aa', tr=(1.08, 1.12, 1.08)),
    autumn=dict(sky=dict(cZen='#7a6a9a', cMid='#e8b088', cHor='#ffe0a0', cLow='#f2c078', sunDir=(-.6, .22, -1.), sunCol='#fff0c0', sunR=.06, rays=.6, halo=.6, cov=.4, cLit='#fff0d0', cCM='#f0b890', cSh='#b8808a', cInk='#5a2c34'), haze='#f6cf90', gA='#d8a050', gB='#a0602c', mist='#ffe4b0', kinds=('pahari_round', 'bare', 'mango'), under=('reed', 'grass', 'shrub'), key='#ffe0a0', amb='#b08c90', tr=(1, .96, .92)),
    winter=dict(sky=dict(cZen='#8a9ab8', cMid='#b8c4d4', cHor='#eae6e4', cLow='#dcdce0', sunDir=(-.5, .3, -1.), sunCol='#fff6ee', sunR=.05, rays=.2, halo=.3, cov=.5, cLit='#f8f8fa', cCM='#ccd0dc', cSh='#9aa4ba', cInk='#4c5468', cink=.5), haze='#d8dce4', gA='#eceef2', gB='#b0b8c8', mist='#eef0f4', kinds=('bare', 'deodar', 'pahari_round'), under=('grass', 'shrub', 'grass', 'shrub', 'rock'), key='#fff6ee', amb='#b0b8d0', tr=(1, 1, 1)))
H = dict(pahari_round=62, mango=58, bare=64, banyan=74, ashoka=56, palm=76, kadamba=62, bamboo=66, plantain=30, deodar=88, shrub=10, grass=7, fern=8, reed=11, rock=16, ashoka_weep=60)


def sky(s, **k): return SKY(None, **{**S[s]['sky'], **k})


def light(s, **k):
    d = S[s]; return Light(**{**dict(key=(-.55, .65, .45), keyCol=d['key'], amb=d['amb'], rim=(.5, .5, -.8), rimCol=tuple(.5 * v for v in hexc(d['key'])), bounceCol=tuple(.15 * v for v in hexc(d['gA'])), envT='#ffffff', envM=d['key'], envB=d['gB'], fogCol=d['haze'], fog=(.0016, 90., .004, 0.), inkRef=1.2, inkCol='#1a1014'), **k})


def card_rows(st, s, z, x0, x1, step, kinds, seed, hscale=1., haze=0., y=0., jz=10., vary=.22, tint=None, pick=None, **k):
    """a row of trees along x at depth z, stable in world x (cells), any window x0..x1"""
    d = S[s]; i0, i1 = int(math.floor(x0 / step)) - 1, int(math.ceil(x1 / step)) + 1; B = {}
    for i in range(i0, i1):
        r = np.random.default_rng([seed & 0xffff, i & 0xffff, abs(int(z)) & 0xffff]); q = kinds[int(r.integers(len(kinds)))]; B.setdefault(q, []).append(((i + r.uniform(.1, .9)) * step, y, z + r.uniform(-jz, jz), r.uniform(1 - vary, 1 + vary), int(r.integers(0, 6)), r.uniform(0, 6.28)))
    for q, L in B.items():
        A = np.array(L); nv = FL.KINDS[q][6]
        for v in range(nv):
            m = (A[:, 4].astype(int) % nv) == v
            if m.any(): FL.cards(st, FL.plate_of(q, s, v), A[m, :3], H[q] * hscale * A[m, 3], np.where(A[m, 5] > 3.14, 1., -1.), phase=A[m, 5], haze=haze, hazeCol=d['mist'], tint=tint or d['tr'], **k)


GROUND = """
#define TMAX 1200.
#define STEPS 90
#define NOAO
#include "arch.glsl"
#include "paint.glsl"
uniform vec3 gA,gB,leafA,mist;uniform float snow,wet,river;
float gyF(vec2 q){float b=smoothstep(-16.,-46.,q.y);return b*(3.2*(vn(vec2(q.x*.02,q.y*.03))-.2))+smoothstep(14.,40.,q.y)*-1.5*vn(q*.05)+.25*vn(q*.18);}
vec2 map(vec3 p){return vec2((p.y-gyF(p.xz))*.8,M_GROUND);}
void surf(vec3 p,vec3 n,int m,inout Surf s){float t=fbm(p.xz*vec2(.05,.10));vec3 c=mix(gA,gB,smoothstep(.36,.64,t)*.7);float pth=smoothstep(8.5,5.5,abs(p.z+1.2*sin(p.x*.05))+1.6*(vn(p.xz*.4)-.5));c=mix(c,mix(gA,vec3(1.,.86,.66),.45),pth*(1.-.6*wet));
 vec2 cc=floor(p.xz/vec2(5.,3.2)),f=fract(p.xz/vec2(5.,3.2))-.5;vec2 h=h22(cc);vec2 o=(f-(h-.5)*.6)*vec2(5.,3.2);oAA=gPx;float tu=0.;for(int i=-2;i<=2;i++){vec2 q=vec2(o.x-float(i)*.32,-o.y);q.x-=float(i)*.22*q.y;tu=max(tu,oE(max(abs(q.x)-.10*(1.-q.y*.6),max(-q.y,q.y-1.5))));}
 c=mix(c,mix(gB*.55,leafA,h.x),tu*step(.35,h.y)*(1.-pth)*pLod(1.6));float pb=oE(length(o*vec2(1.,1.8))-.35-.3*h.x);c=mix(c,vec3(.45,.40,.40),pb*step(h.y,.12)*pLod(1.));
 c=mix(c,vec3(.92,.94,.99),snow*smoothstep(.30,.52,t+.15*n.y));s.base=c;s.sh=c*vec3(.50,.46,.62);s.ink=.2;s.cls=1.;
 if(wet>0.){float pd=smoothstep(.60,.63,vn(p.xz*vec2(.06,.14)+7.))*wet;if(pd>.5){s.base=mix(mist,gB,.35);s.sh=s.base*.7;s.cls=8.;float rp=abs(fract(length(fract(p.xz/6.)-.5)*3.-fT*1.5)-.5);s.base=mix(s.base,mist,smoothstep(.08,.0,rp)*.5);}}
 if(river>0.){float w=smoothstep(.0,.6,river)*step(abs(p.z+70.-6.*sin(p.x*.02)),16.);if(w>.5){oAA=gPx/9.;s.base=mix(hex(0x3a8a96),mist,.35+.4*oWater(p.xz/vec2(16.,7.)+vec2(fT*.2,0)));s.sh=s.base*.7;s.cls=8.;s.ink=.5;s.part+=8.;}}}
"""


def track(st, s, x0, x1, seed=1, river=0., mist=None):
    """everything behind and under the walkers between x0 and x1 (give the visible range plus about 120 each side)"""
    d = S[s]; mist = (1.3 if s == 'monsoon' else 1.) if mist is None else mist; place.draw(st, GROUND, u=dict(gA=d['gA'], gB=d['gB'], leafA=FL.GREEN[s][3], mist=d['mist'], snow=1. if s == 'winter' else 0., wet=1. if s == 'monsoon' else 0., river=float(river)), sun=0.)
    xc = (x0 + x1) / 2; w = (x1 - x0)
    X = np.arange(math.floor((xc - 1100) / 560) * 560, xc + 1100, 560); fl = np.where(np.round(X / 560).astype(int) % 2 == 0, 1., -1.)
    FL.cards(st, FL.plate_of('hill', s, 0), np.c_[X, 0 * X - 4, 0 * X - 620], 190, fl, haze=.62, hazeCol=d['mist'], wind=0.); FL.cards(st, FL.plate_of('hill', s, 1), np.c_[X + 260, 0 * X - 6, 0 * X - 420], 105, -fl, haze=.48, hazeCol=d['mist'], wind=0.)
    K = d['kinds']
    card_rows(st, s, -270, xc - w * .5 - 420, xc + w * .5 + 420, 44, K, seed + 5, 1.15, .52 * mist, wind=.2); card_rows(st, s, -170, xc - w * .5 - 260, xc + w * .5 + 260, 46, K, seed + 4, 1.1, .34 * mist, wind=.3)
    card_rows(st, s, -92, xc - w * .5 - 130, xc + w * .5 + 130, 46, K, seed + 3, 1.05, .16 * mist, wind=.4); card_rows(st, s, -40, x0 - 60, x1 + 60, 74, K, seed + 2, 1.1, .0, jz=5., wind=.5)
    for z, st_, hz in ((-120, 16, .2), (-60, 13, .08), (-30, 12, 0.), (-15, 11, 0.)): card_rows(st, s, z, x0 - 80, x1 + 80, st_, d['under'], seed + int(z), 1. if z < -20 else .62, hz * mist, jz=5., vary=.35, wind=.6, foot=.25, footCol=FL.GREEN[s][0])


def near(st, s, x0, x1, seed=9, blur=1.5, z=(30., 40.)):
    """after close: leaves and grass between the lens and the walkers, in pixels from their world x"""
    d = S[s]
    for zz, kind, step, sc in ((z[0], 'fg_grass', 46, 1.), (z[1], 'fg_leaves', 120, 1.)):
        for i in range(int(math.floor(x0 / step)) - 1, int(math.ceil(x1 / step)) + 2):
            r = np.random.default_rng([seed, i & 0xffff]); X = (i + r.uniform(0, 1)) * step
            if kind == 'fg_grass': P = (X, -2., zz); hgt = 9. * r.uniform(.8, 1.4); pl = FL.plate_of(kind, s, int(r.integers(2))); k = hgt * st.cam.px(P) / (pl.h * .8); x, y, _ = st.cam.project(P); FL.frame(st, kind, x, y + 10, k, s, int(r.integers(2)), lod=blur)
            else:
                if s == 'winter' or r.uniform() < .35: continue
                P = (X, 30., zz); k = 18 * st.cam.px(P) / 1000; x, y, _ = st.cam.project(P); FL.frame(st, kind, x, min(y, -20), k * r.uniform(.8, 1.2), s, int(r.integers(2)), lod=blur, flip=bool(r.integers(2)))


def wipe(st, s, u, scale=1.6, var=0, blur=1.2):
    """after close: a trunk that crosses the frame right to left as u goes 0..1; it covers the whole frame around u = .5"""
    pl = FL.plate_of('trunk_wide', s, var); w = pl.w * scale; x = 1920 + w * .5 - u * (1920 + w); st.plate(pl.tex, x, 540, scale, lod=blur)


def drift(st, s, n=90, box=None, t=None):
    """after close: what falls in the season: petals, rain, leaves, snow"""
    e = st.cam.eye; b = box or (e + [-70, -18, -120], e + [70, 45, -14]); t = st.t if t is None else t
    if s == 'spring': FX.drift(st, n, b, t, 'petal', .7, '#f2a8b8', 3.2, 2., col2='#fff0f0')
    elif s == 'monsoon': r = np.random.default_rng(3); P = r.uniform(0, 1, (n * 5, 3)); P[:, 1] = (P[:, 1] - t * 2.6 * (.8 + .4 * r.uniform(0, 1, n * 5))) % 1; P = np.asarray(b[0]) + P * (np.asarray(b[1]) - np.asarray(b[0])); FX.particles(st, P, .07, (.75, .85, .88), 'rain', vel=np.tile([[.6, -5., 0]], (len(P), 1)), alpha=.45)
    elif s == 'autumn': FX.drift(st, n, b, t, 'leaf', .9, '#d8741c', 4., 2.5, col2='#f6c84a')
    elif s == 'winter': FX.drift(st, n * 2, b, t, 'dot', .18, '#ffffff', 2.4, 1.2, alpha=.85)
    else: FX.drift(st, n // 3, b, t, 'leaf', .6, '#8aa84a', 2., 2., col2='#d8d070')


# ------------------------------------------------------------------ the clearing
CLR = dict(
    day=dict(sky=dict(**{**DAY, 'sunR': 0., 'cov': .3, 'cHor': '#f2eecc', 'cLow': '#c8d4a0', 'rays': .4, 'halo': 0.}), light=dict(key=(-.5, .7, .5), keyCol='#fff0c8', amb='#8fa8a8', rim=(.5, .5, -.8), rimCol=(.6, .55, .35), bounceCol=(.12, .14, .06), envT='#f4ffe8', envM='#ffe8a8', envB='#6a8a4a', fogCol='#cfe0b0', fog=(.0022, 70., .006, 0.)), season='summer', gA='#d0b070', gB='#94884a', mist='#dcebc4', tint=(1, 1, 1), hz=1.),
    evening=dict(sky=SAFFRON, light=dict(key=(-.8, .30, .35), keyCol='#ffc078', amb='#8a6a94', rim=(.6, .3, -.8), rimCol=(1.1, .6, .25), bounceCol=(.2, .1, .04), envT='#ffd8a0', envM='#ff9a5a', envB='#6a3a4a', fogCol='#e8a060', fog=(.0024, 70., .006, 0.)), season='summer', gA='#d8a060', gB='#8a5a3c', mist='#f0b070', tint=(1, .85, .72), hz=1.),
    night=dict(sky=dict(**{**NIGHT, 'sunDir': (.45, .5, -1.), 'sunR': .05, 'cov': .3, 'cHor': '#24406a', 'cLow': '#0c1a34'}), light=dict(key=(.4, .7, -.35), keyCol='#5f78c0', amb='#26346a', rim=(.45, .5, -.8), rimCol=(.30, .42, .8), bounceCol=(.04, .03, .02), envT='#6a84d8', envM='#ffa04a', envB='#1c2450', fogCol='#18305a', fog=(.0026, 60., .005, 0.), inkCol='#03040c'), season='night', gA='#6a7a6a', gB='#2c4448', mist='#203a66', tint=(1., 1., 1.05), hz=.9),
    rain=dict(sky=RAIN, light=dict(key=(-.3, .85, .3), keyCol='#8fa0a8', amb='#5c6c78', rim=(.4, .6, -.7), rimCol=(.20, .24, .28), bounceCol=(.04, .05, .05), envT='#b0c0c8', envM='#8094a0', envB='#404c54', fogCol='#8496a0', fog=(.0034, 60., .004, 0.), inkCol='#10161c'), season='monsoon', gA='#7c8478', gB='#4a5654', mist='#8a9ca6', tint=(.72, .76, .80), hz=1.4))


def csky(mood='day', **k): return SKY(None, **{**CLR[mood]['sky'], **k})


def clight(mood='day', fire=0., **k):
    L = Light(**{**dict(inkRef=1.2), **CLR[mood]['light'], **k})
    if fire > 0: L.pts = [((16., 4.5, 20.), 12., tuple(fire * v for v in (2.0, .80, .20)))]
    return L


def clearing(st, mood='day', season=None, fire=0., line=0., lineR=24., hut=True, rock=True, trees=True, seed=3):
    """the hut place.  fire = cooking fire glow (b4 1, c7 0); line = Lakshmana's burning line, drawn 0..1 round the hut at radius lineR"""
    m = CLR[mood]; s = season or m['season']; g = FL.GREEN[s]
    rk = dict(rain=('#6a747c', '#39434c'), night=('#6a78a0', '#242e54'), evening=('#d89a78', '#7a4a54')).get(mood, ('#cfae90', '#86706c')); lf = dict(night=('#7a7a58', '#2c3438'), rain=('#8a8460', '#4a4c3c')).get(mood, ('#c8a850', '#7a6428'))
    place.draw(st, 'hut.glsl', u=dict(fireK=float(fire), tone=1. if mood == 'rain' else 0., line=float(line), lineR=float(lineR), gA=m['gA'], gB=m['gB'], leafA=lf[0], leafB=lf[1], rockA=rk[0], rockB=rk[1]), defs=('' if hut else '#define NOHUT\n') + ('' if rock else '#define NOROCK\n'), sun=1. if mood in ('day', 'evening') else 0.)
    if not trees: return
    r = np.random.default_rng(seed); k = dict(hazeCol=m['mist'], tint=m['tint'], wind=.5); hz = m['hz']
    def ring(kind, n, r0, r1, a0, a1, hh, haze, sd, **q):
        a = np.linspace(a0, a1, n) + r.uniform(-.06, .06, n); R = r.uniform(r0, r1, n); P = np.c_[np.sin(a) * R, np.zeros(n) - .3, np.cos(a) * R]; FL.scatter(st, kind, P, hh, season=s, seed=sd, haze=np.clip(haze * hz, 0, .85), **{**k, **q})
    b0, b1 = 1.9, 4.4                                            # behind, from right to left
    FL.cards(st, FL.plate_of('hill', s, 0), [(x, -6, -420) for x in (-620, -200, 220, 640)], 130, [1, -1, 1, -1], haze=min(.8, .6 * hz), **{**k, 'wind': 0.})
    ring('pahari_round', 16, 150, 230, b0 - .3, b1 + .3, 74, .42, 1); ring('mango', 12, 100, 150, b0 - .2, b1 + .2, 62, .24, 2); ring('palm', 7, 96, 150, b0, b1, 74, .22, 3)
    ring('plantain', 5, 40, 58, 1.7, 2.3, 24, .03, 4); ring('plantain', 4, 42, 60, 4.0, 4.6, 26, .03, 5); ring('banyan', 1, 74, 78, 4.28, 4.3, 78, .06, 6); ring('ashoka', 2, 64, 80, 1.75, 2.0, 50, .06, 7); ring('bamboo', 4, 66, 90, 1.5, 2.1, 56, .10, 8)
    ring('shrub', 22, 56, 110, 1.3, 5.0, 10, .06, 9); ring('grass', 40, 34, 90, 0, 6.28, 6, .03, 10); ring('fern', 14, 44, 80, 1.2, 5.1, 8, .04, 11)
    if mood != 'rain': ring('lotus_clump', 2, 60, 66, .9, 1.15, 10, .0, 12)


GROVE = """
#define TMAX 900.
#define STEPS 100
#define AOK .8
#include "arch.glsl"
#include "paint.glsl"
uniform vec3 gA,gB;uniform float warm;
vec2 map(vec3 p){float g=.35*vn(p.xz*.05)+2.*smoothstep(60.,200.,length(p.xz))*vn(p.xz*.02);vec2 m=vec2((p.y-g)*.85,M_GROUND);float d=max(aOct(p.xz*.924+p.zx*vec2(.38,-.38))-15.,abs(p.y-.9)-1.1);d=min(d,max(aOct(p.xz*.924+p.zx*vec2(.38,-.38))-16.4,abs(p.y-.3)-.6));m=U(m,vec2(d-.1,M_STEP));
 vec3 q=p-vec3(0,0,-96);float w=max(abs(q.z)-2.5,p.y-13.);float k=abs(fract(p.x/5.)-.5)*5.;w=min(w,max(abs(q.z)-.8,p.y-13.-2.6*smoothstep(1.9,1.1,k)))*.8;m=U(m,vec2(w,M_WALL));m=U(m,aChhatri(vec3(abs(p.x)-70.,p.y-13.,p.z+96.),8.));return m;}
void surf(vec3 p,vec3 n,int m,inout Surf s){if(m==10){float t=fbm(p.xz*.05);s.base=mix(gA,gB,smoothstep(.35,.62,t)*.8);vec2 c=floor(p.xz/2.2),f=fract(p.xz/2.2)-.5;vec2 h=h22(c);oAA=gPx/2.2;float fl=oE(length(f-(h-.5)*.6)-.10-.05*h.x);float near=smoothstep(60.,14.,length(p.xz));s.base=mix(s.base,mix(hex(0xb8322a),hex(0xe8702a),h.x),fl*step(1.-.55*near,h.y)*pLod(.5));
  // moonlight through leaves
  float dp=smoothstep(.52,.60,vn(p.xz*.16+3.)*.6+vn(p.xz*.4)*.4);s.ns=mix(normalize(n-keyDir*.9),n,dp);s.sh=gB*.45;s.ink=.2;}
 else if(m==4){s.base=hex(0xc8c0d0);s.sh=hex(0x50527c);float a=atan(p.x,p.z);oAA=gPx/1.4;if(n.y<.5) s.base=mix(s.base,hex(0x8a6a9a),oLotus(vec2(a*10.,fract(p.y*.6))));else{oAA=gPx/13.;s.base=mix(s.base,hex(0x9a86b0),oLotusM(p.xz/13.)*.6);}}
 else if(m==1){s.base=hex(0xb8a8b8);s.sh=hex(0x484a78);pPave(s,p.xy,vec2(7.,3.4),s.base,s.sh,.5);}else if(m==2){s.cls=2.;s.base=vec3(1);s.sh=vec3(.5);}else{s.base=hex(0xa8a0c0);s.sh=hex(0x484a78);}
 if(warm>0.){float r=length(p-vec3(0,6,4));emit(s,s.base*vec3(1.4,.6,.15)*warm/(1.+r*r/60.));}}
"""


def grove_sky(**k): return SKY(NIGHT, **{**dict(sunDir=(.42, .55, -1.), sunR=.05, cov=.35, cHor='#2a4a86', cLow='#0c1838'), **k})


def grove_light(warm=0., **k):
    L = Light(**{**dict(key=(.45, .75, -.15), keyCol='#a8bcf0', amb='#2c3a78', rim=(.42, .5, -.8), rimCol=(.5, .65, 1.1), bounceCol=(.02, .03, .06), envT='#a0b4ff', envM='#5a6ab8', envB='#20264f', fogCol='#1c3468', fog=(.0030, 50., .004, 0.), inkRef=1.2, inkCol='#03040e'), **k})
    if warm > 0: L.pts = [((0., 8., 5.), 7., tuple(warm * v for v in (1.8, .85, .25)))]
    return L


def grove(st, warm=0., trees=True, seed=5):
    """the ashoka grove: a paved octagonal seat round the great tree at the origin, red flowers on the ground, rows of trees, a palace wall at z = -96.  warm = the ring's light"""
    place.draw(st, GROVE, u=dict(gA='#6a7a78', gB='#2c4258', warm=float(warm)), sun=0.)
    if not trees: return
    k = dict(hazeCol='#1e3a70', wind=.35); T = (.66, .74, 1.0); r = np.random.default_rng(seed)
    FL.tree(st, 'ashoka', (0, 1.6, -3), 58, season='monsoon', seed=0, tint=(.72, .74, .92), **k)
    P = np.array([(-58, 0, -34), (56, 0, -40), (-92, 0, -10), (94, 0, -6), (-30, 0, -70), (30, 0, -74)], float); FL.scatter(st, 'ashoka', P, 52, season='monsoon', seed=2, tint=T, haze=.10, **k)
    X = np.arange(-260, 261, 40.); FL.scatter(st, 'ashoka', np.c_[X + r.uniform(-9, 9, len(X)), 0 * X, -122 + r.uniform(-12, 12, len(X))], 58, season='night', seed=3, tint=(1.3, 1.1, 1.2), haze=.35, **k); X = np.arange(-340, 341, 36.); FL.scatter(st, 'ashoka_weep', np.c_[X, 0 * X, 0 * X - 160], 80, season='night', seed=4, tint=(1.2, 1.2, 1.3), haze=.5, **k)
    X = np.arange(-120, 121, 15.); FL.scatter(st, 'shrub', np.c_[X, 0 * X, -88 + r.uniform(-4, 4, len(X))], 10, season='night', seed=5, tint=(1.4, 1.3, 1.4), haze=.14, **k)
    A = r.uniform(0, 6.28, 34); R = r.uniform(20, 80, 34); FL.scatter(st, 'grass', np.c_[np.sin(A) * R, 0 * A, np.cos(A) * R - 12], 5, season='night', seed=6, tint=(1.5, 1.5, 1.5), **k)
