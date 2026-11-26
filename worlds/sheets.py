"""Contact sheets of the places: ./.mm/env/bin/python worlds/sheets.py flora trees_seasons orn ...  -> qa/places/"""
import sys, os, time
from pathlib import Path
HOME = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(HOME)); os.chdir(HOME)
import numpy as np, cv2, math
from lau.shot import *
from lau.look import *
from worlds import flora as FL
OUT = os.environ.get('OUT', 'qa/places'); os.makedirs(OUT, exist_ok=True)
SC = {}
_st = None


def stage():
    global _st
    if _st is None: _st = Stage(2)
    return _st


def scene(fn): SC[fn.__name__] = fn; return fn


def grid(ims, cols, w=960):
    h = w * 9 // 16; t = [cv2.resize(i, (w, h), interpolation=cv2.INTER_AREA) for i in ims]; n = cols; return np.vstack([np.hstack((t[i:i + n] + [np.zeros_like(t[0])] * n)[:n]) for i in range(0, len(t), n)])


def cells(kinds, cols, cw, ch, bg='#e6d6b4', label=True):
    """plates laid on a paper ground"""
    rows = (len(kinds) + cols - 1) // cols; sf = cairo.ImageSurface(cairo.FORMAT_RGB24, cols * cw, rows * ch); c = cairo.Context(sf); c.set_source_rgb(*rgb(bg)); c.paint()
    for i, (k, s, v) in enumerate(kinds):
        pl = FL.plate_of(k, s, v); a = np.frombuffer(pl.tex.read(), np.uint8).reshape(pl.h, pl.w, 4)[::-1].copy(); q = cairo.ImageSurface.create_for_data(a, cairo.FORMAT_ARGB32, pl.w, pl.h); z = min((cw - 16) / pl.w, (ch - 30) / pl.h); x, y = (i % cols) * cw, (i // cols) * ch
        c.save(); c.translate(x + (cw - pl.w * z) / 2, y + (ch - 24 - pl.h * z)); c.scale(z, z); c.set_source_surface(q, 0, 0); c.get_source().set_filter(cairo.FILTER_BEST); c.paint(); c.restore()
        c.set_source_rgb(.2, .1, .1); c.set_font_size(15); c.move_to(x + 8, y + ch - 7); c.show_text(f'{k} {s}')
    sf.flush(); return np.ndarray((rows * ch, cols * cw, 4), np.uint8, sf.get_data())[..., :3].copy()


@scene
def flora():
    ss = dict(pahari_round='spring', mango='spring', kadamba='monsoon', ashoka='summer', bare='winter', rock='summer', banyan='summer', deodar='summer', lotus_bloom='summer')
    return cells([(k, ss.get(k, 'summer'), 0) for k in FL.KINDS], 6, 420, 420)


@scene
def trees_seasons():
    K = []
    for k in ('pahari_round', 'banyan', 'mango', 'shrub', 'trunk_wide'): K += [(k, s, 0) for s in ('spring', 'summer', 'monsoon', 'autumn', 'winter')]
    return cells(K, 5, 500, 420)


ORN = """
#include "noise.glsl"
#include "orn.glsl"
in vec2 uv;out vec4 o;uniform vec2 res;
vec3 pap=hex(0xf0e0c0),red=hex(0xb02a1c),gld=hex(0xd89a2a),blu=hex(0x27407a),grn=hex(0x2c6a4a),ink_=hex(0x241016);
void main(){vec2 p=vec2(uv.x,1.-uv.y)*vec2(1920.,1080.);vec3 c=hex(0xe6d2a6);
 if(p.y<620.){float h=620./12.;int k=int(p.y/h)+(p.x>960.?12:0);float yy=1.-fract(p.y/h);vec2 q=vec2(p.x,(yy-.1)/.8);float x=p.x/(h*.8);oAA=1./(h*.8);vec3 bg=red,fg=hex(0xf6d27a);float v=0.;
  if(k==0||k==12){v=oLotus(q*vec2(0,1)+vec2(x,0));}else if(k==1){v=oLotusFill(vec2(x,q.y));bg=blu;}else if(k==2){v=oBead(vec2(x*1.6,q.y));bg=ink_;}else if(k==3){v=oWave(vec2(x*.8,q.y));bg=blu;fg=pap;}else if(k==4){v=oVine(vec2(x*.75,q.y));bg=grn;}else if(k==5){v=oKey(vec2(x,q.y));bg=ink_;}
  else if(k==6){v=oMerlon(vec2(x,q.y));bg=hex(0x6a86c8);fg=pap;}else if(k==7){v=oRope(vec2(x*1.5,q.y));bg=red;}else if(k==8){v=oLeafBand(vec2(x*1.5,q.y));bg=pap;fg=grn;}else if(k==9){v=oLotus(vec2(x,q.y));bg=pap;fg=red;}else if(k==10){v=oVine(vec2(x*.75,q.y));bg=pap;fg=blu;}else if(k==11){v=oBead(vec2(x*1.6,q.y));bg=gld;fg=red;}
  else if(k==13){v=oLotusFill(vec2(x*2.,q.y));bg=gld;fg=red;}else if(k==14){v=oScale(vec2(x*2.,q.y*2.));bg=grn;}else if(k==15){v=oWater(vec2(x,q.y*1.5));bg=blu;fg=pap;}else if(k==16){v=oJali(vec2(x*2.,q.y*2.));bg=ink_;fg=pap;}else if(k==17){v=oJaliSq(vec2(x*2.,q.y*2.));bg=ink_;fg=hex(0xe0a890);}
  else if(k==18){v=oDiaper(vec2(x,q.y));}else if(k==19){v=oFlorets(vec2(x*1.4,q.y*1.4));bg=pap;fg=red;}else if(k==20){v=oButa(vec2(x,q.y));bg=blu;}else v=oWave(vec2(x*1.3,q.y));
  c=mix(bg,fg,v);c=mix(c,ink_,step(q.y,-.04)+step(1.04,q.y));}
 else{float s=320.;vec2 g=vec2((p.x-40.)/s,(p.y-700.)/s);int k=int(g.x);vec2 q=vec2(fract(g.x)-.5,.5-g.y)*2.2;oAA=2.2/s;vec3 bg=hex(0x3a1420),fg=hex(0xf0c45a);float v=0.;if(g.y>0.&&g.y<1.&&p.x>40.&&k<6){if(k==0)v=oLotusM(q);else if(k==1)v=oSun(q);else if(k==2)v=oWheel(q);else if(k==3)v=oConch(q);else if(k==4)v=oEyeM(q);else{float d=oArch(q+vec2(0,.95),.62,.85,4.);v=oE(d)*.0+oL(d,.03)+oE(d)*.35;v+=oE(abs(d-.10)-.02)*.6;}c=mix(bg,fg,v);}}
 c*=.92+.14*fbm(p/7.);o=vec4(c,1);}
"""


@scene
def orn():
    st = stage(); st.clear(); st.paint(ORN); return st.finish(bloom=0, vig=0)[..., ::-1]


ARCH = """
#define SUNSH 24
#define TMAX 400.
#include "arch.glsl"
vec2 map(vec3 p){vec2 m=vec2(p.y,M_GROUND);
 m=U(m,vec2(aColumn(p-vec3(-92,0,0),30.,2.6),M_COL));m=U(m,aDome(p-vec3(-70,0,0),10.));m=U(m,aChhatri(p-vec3(-46,0,0),8.));
 vec3 q=p-vec3(-18,0,0);m=U(m,vec2(aBlock(q,vec3(13,28,10),14.),M_WALL));m=U(m,vec2(aParapet(q-vec3(0,28,0),vec2(13,10),3.4,3.2),M_WALL));m=U(m,aJharokha(q-vec3(0,12,10.),4.5));
 m=U(m,aShikhara(p-vec3(16,0,0),9.,62.));m=U(m,aGopura(p-vec3(50,0,0),16.,9.,52.,7.));m=U(m,aTorana(p-vec3(86,0,0),10.,26.,1.6));
 m=U(m,vec2(aRampart(p-vec3(0,0,-30),120.,24.,3.,5.),M_WALL));m=U(m,vec2(aTower(p-vec3(-60,0,-30),9.,32.,4.),M_WALL));m=U(m,aDeepa(p-vec3(-106,0,8),30.,3.4));m=U(m,vec2(aBaluster(p-vec3(0,0,26),30.,4.,1.6),M_WALL));
 vec2 s=vec2(p.z-34.,p.y+12.);m=U(m,vec2(max(aStairs(s,1.4,2.2),s.x-34.),M_STEP));return m;}
void surf(vec3 p,vec3 n,int m,inout Surf s){s.base=hex(0xf2e2cc);s.sh=hex(0xb07a80);if(m==2){s.base=vec3(1);s.sh=vec3(.5);s.cls=2.;}if(m==3){s.base=hex(0xf6ecd8);s.sh=hex(0xb48a9c);}if(m==10){s.base=hex(0xe0b080);s.sh=hex(0x9a6060);s.ink=0.;}}
"""


@scene
def arch():
    st = stage(); st.clear(f=0); from worlds import place; ims = []
    for cam in (Cam((0, 30, 150), (0, 24, 0), 40), Cam((-70, 22, 60), (-40, 16, 0), 40)):
        st.clear(); st.cam = cam; st.paint('sky.frag', **SKY(DAY)); st.open(cam, Light(**{**L_DAY.__dict__, 'inkRef': 2.})); t = time.time(); place.draw(st, ARCH); st.close(); im = st.finish()[..., ::-1]; print('%.2fs' % (time.time() - t)); ims.append(im)
    return grid(ims, 1, 1600)


def shoot(st, cam, sky_, light_, body, after=None, f=0, bg=None, **fin):
    st.clear(f=f); st.cam = cam; st.paint('sky.frag', **sky_); bg and bg(st); st.open(cam, light_, far=20000.); t = time.time(); body(st); gl.ctx().finish(); t2 = time.time(); st.close()
    if after: after(st)
    im = st.finish(**{**dict(bloom=.45), **fin})[..., ::-1]; print('   world %.2fs  frame %.2fs' % (t2 - t, time.time() - t)); return im


def AYim(mood, cam, night=None, after=True, f=0, fr=None, fill=1., gain=1., **kw):
    from worlds import ayodhya as AY
    def body(st): AY.draw(st, mood, night=night, fill=fill); AY.trees(st, mood)
    def aft(st):
        if mood == 'night': AY.lamps(st, gain=gain, minpx=1.5 * gain)
        else: AY.birds(st)
        if fr: fr(st)
    return shoot(stage(), cam, AY.sky(mood), AY.light(mood, **kw), body, aft if after else None, f, **(dict(bloom=.7) if mood == 'night' else {}))


def _frA(st):
    FL.frame(st, 'fg_leaves', -30, -40, .50, 'summer', 0, lod=.6); FL.frame(st, 'fg_leaves', 1950, -50, .42, 'summer', 1, flip=True, lod=.6); FL.frame(st, 'fg_grass', 1500, 1100, .36, 'summer', 0, lod=.8); FL.frame(st, 'fg_grass', 1800, 1110, .42, 'summer', 1, lod=.8)


@scene
def ayodhya_dawn(): return grid([AYim('dawn', Cam((-110, 90, 640), (20, 270, -900), 42), fr=_frA, inkRef=10.), AYim('dawn', Cam((40, 470, 520), (0, 260, -900), 42), inkRef=10.), AYim('dawn', Cam((-200, 30, 210), (40, 140, -300), 46)), AYim('dawn', Cam((420, 70, 60), (-100, 70, -150), 42))], 2)


@scene
def ayodhya_night(): return grid([AYim('night', Cam((-60, 60, 330), (0, 180, -600), 46), fill=.62, inkRef=8.), AYim('night', Cam((150, 62, -40), (-200, 56, -110), 48), fill=.7, inkRef=2.), AYim('night', Cam((4, 66, -150), (0, 150, -500), 50), inkRef=2.), AYim('night', Cam((-14, 230, -500), (10, 420, -1200), 50))], 2)


@scene
def ayodhya_above(): return grid([AYim('night', Cam((0, 820, 700), (0, 330, -560), 48), fill=.36, gain=1.25, inkRef=10., keyCol='#2a3474', amb='#1e2660'), AYim('night', Cam((0, 1500, 900), (0, 190, -620), 46), fill=.10, gain=1.5, inkRef=14., keyCol='#1e2760', amb='#171e50')], 1, 1600)


def LKim(mood, cam, fire=0., at=(0, 200, 1100), f=20, doors=0., rise=1., **kw):
    from worlds import lanka as LK
    def body(st): LK.draw(st, mood, fire=fire, fireAt=at, doors=doors)
    def aft(st):
        if mood != 'dark': LK.lamps(st, amount=1. if fire == 0 else .5)
        if fire > 0:
            P, S, Q = LK.fires(fire, at, cam, rise=rise); FX.particles(st, P, S, (.95, .86, .80), 'tongue', seed=Q, alpha=.95); FX.embers(st, 300, (cam.eye + [-400, -250, -700], cam.eye + [400, 250, -60]), st.t, size=2.5, rise=30) if rise < 1.5 else 0
    return shoot(stage(), cam, LK.sky(mood), LK.light(mood, **kw), body, aft, f, bg=LK.moon if mood == 'moon' else None, bloom=.5 if mood == 'moon' else .4)


@scene
def lanka_moon(): return grid([LKim('moon', Cam((-500, 120, 3300), (0, 420, 0), 34)), LKim('moon', Cam((520, 300, 1900), (-100, 380, 0), 40)), LKim('moon', Cam((-470, 420, 1060), (40, 620, 0), 46), inkRef=4.), LKim('dark', Cam((50, 292, 1500), (0, 345, 1100), 44), inkRef=3.)], 2)


@scene
def lanka_roofs(): return grid([LKim('fire', Cam((-330, 460, 800), (60, 500, 100), 52), fire=.36, at=(-200, 380, 400), inkRef=4.), LKim('fire', Cam((330, 640, 520), (-60, 640, -100), 55), fire=.42, inkRef=4.), LKim('fire', Cam((-740, 560, 560), (-100, 520, 100), 50), fire=.8, inkRef=4.), LKim('moon', Cam((330, 500, 660), (-40, 520, 60), 52), inkRef=4.)], 2)


@scene
def lanka_far(): return grid([LKim('fire', Cam((0, 130, 6200), (0, 240, 0), 34), fire=1., rise=2.2, inkRef=30.), LKim('fire', Cam((900, 420, 3800), (0, 300, 0), 40), fire=1., rise=1.6), LKim('moon', Cam((0, 60, 8000), (0, 330, 0), 24)), LKim('day', Cam((1200, 300, 3600), (0, 330, 0), 36))], 2)


def PLim(hall, cam, lamps=18, f=10, **kw):
    from worlds import palace as PL
    return shoot(stage(), cam, PL.sky(hall), PL.light(hall, **kw), lambda st: PL.draw(st, hall, lamps=lamps), lambda st: PL.flames(st, hall, lamps=lamps), f, bloom=.5)


@scene
def halls(): return grid([PLim('mithila', Cam((0, 24, 150), (0, 36, -240), 44)), PLim('mithila', Cam((-44, 18, 40), (40, 34, -160), 48)), PLim('ayodhya', Cam((0, 9, -40), (0, 46, -430), 46)), PLim('crown', Cam((-16, 22, 40), (4, 34, 200), 46)),
                           PLim('ayodhya', Cam((0, 9, -120), (0, 44, -430), 46), lamps=5.5), PLim('ravana', Cam((-12, 20, 120), (4, 40, -240), 44))], 2)


def TRim(s, x=0., f=20, **kw):
    from worlds import forest as FO
    cam = Cam((x, 12, 74), (x, 15, 0), 36)
    def aft(st): FO.drift(st, s); FO.near(st, s, x - 90, x + 90)
    return shoot(stage(), cam, FO.sky(s), FO.light(s, **kw), lambda st: FO.track(st, s, x - 80, x + 80, river=1. if s == 'summer' else 0.), aft, f, bloom=.4)


def CLim(mood, cam, f=20, fire=0., line=0.):
    from worlds import forest as FO
    def aft(st):
        if fire > 0: FX.flame(st, (16, 1.5, 20), 7 * fire, glow=.8)
        if mood == 'rain': FO.drift(st, 'monsoon')
    return shoot(stage(), cam, FO.csky(mood), FO.clight(mood, fire), lambda st: FO.clearing(st, mood, fire=fire, line=line), aft, f, bloom=.4)


@scene
def forest():
    from worlds import forest as FO
    ims = [TRim('spring', 0), TRim('monsoon', 400), TRim('autumn', 800), TRim('winter', 1200)]
    ims += [CLim('day', Cam((30, 10, 78), (2, 15, 0), 38)), CLim('night', Cam((34, 9, 62), (4, 13, 4), 38), fire=1.), CLim('rain', Cam((-26, 9, 70), (4, 13, 0), 38)), CLim('evening', Cam((0, 15, 100), (0, 20, 0), 40), line=.7)]
    ims.append(shoot(stage(), Cam((34, 12, 74), (2, 24, 0), 38), FO.grove_sky(), FO.grove_light(1.), lambda st: FO.grove(st, warm=1.), lambda st: FL.frame(st, 'fg_leaves', -30, -40, .6, 'night', 0, lod=1.5), 20, bloom=.4))
    st = stage(); cam = Cam((0, 12, 74), (0, 15, 0), 36); ims.append(shoot(st, cam, FO.sky('summer'), FO.light('summer'), lambda st: FO.track(st, 'summer', -80, 80, river=1.), lambda st: (FO.drift(st, 'summer'), FO.near(st, 'summer', -90, 90), FO.wipe(st, 'summer', .2)), 20, bloom=.4))
    return grid(ims, 2)


if __name__ == '__main__':
    for n in sys.argv[1:]:
        t = time.time(); im = SC[n](); cv2.imwrite(f'{OUT}/{n}.jpg', im if im.ndim == 3 else im, [1, 90]); print(n, im.shape, '%.1fs' % (time.time() - t))
