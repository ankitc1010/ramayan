"""Act C, the dark half (c4 to c7): the hut place with a fire that throws a shadow, the shadow theatre of Ravana, the earth torn out along the line, bowls and roots."""
import os
from lau.shot import *
from lau.look import *
from lau import ROOT
from worlds import place, flora as FL, forest as FO

# ------------------------------------------------------------------ the place
def _hut():
    """worlds/hut.glsl with a longer, higher rock, fainter cracks, and a line that can die outward from a point"""
    s = open(os.path.join(ROOT, 'worlds/hut.glsl')).read()
    for a, b in (('uniform float fireK,tone,line,lineR;', 'uniform float line,lineLo,lineC,lineK,rockH,lineG;bool burn(float a){return a<line&&a>lineLo&&abs(a-lineC)>lineK;}\nuniform float fireK,tone,lineR;'),
                 ('if(a<line){s.cls=4.', 'if(burn(a)){s.cls=4.'), ('if(a<line) emit(s,vec3(1.2,.4,.07)*.8*', 'if(burn(a)) emit(s,vec3(1.2,.4,.07)*lineG*'),
                 ('float h=62.+22.*vn(vec2(p.x*.02,2.))-.0035*p.x*p.x;', 'float h=rockH*(.74+.26*vn(vec2(p.x*.02,2.)))-.0010*p.x*p.x;'), ('if(d0>30.||abs(p.x)>170.) return vec2(max(d0-20.,abs(p.x)-150.)*.5+4.,0.);', 'if(d0>30.||abs(p.x)>230.) return vec2(max(d0-20.,abs(p.x)-210.)*.5+4.,0.);'),
                 ('abs(cr-.5))*.7)', 'abs(cr-.5))*.20)'), ('vec2 map(vec3 p){float g=', 'vec2 map0(vec3 p){float g='), ('void surf(vec3 p,vec3 n,int m,inout Surf s){', 'void surf0(vec3 p,vec3 n,int m,inout Surf s){')):
        if a not in s: raise SystemExit('c_kit: worlds/hut.glsl changed, not found: ' + a)
        s = s.replace(a, b)
    return s


_HUT = _hut()
# everything lit by a fire at fireP that throws the painted shadow tShad, standing in the plane through shO (facing the fire), over the ground, the hut and the rock
LITBY = _HUT + '''
uniform sampler2D tShad;uniform vec3 fireP,shO,shX,shN;uniform vec4 shBox;uniform vec3 hot;uniform float fireI,shK,dusk,eyes,hutK,lean;uniform vec3 fireC,shTint;
vec2 map(vec3 p){return map0(p);}
vec2 shadow(vec3 p){vec3 d=p-fireP;float a=dot(d,shN),b=dot(shO-fireP,shN);if(a<b+.8) return vec2(0.);vec3 h=fireP+d*(b/a);h.x+=lean*pow(max(h.y-6.,0.)/10.,1.6);float fl=fT*5.;vec2 w=vec2(vn(vec2(p.x*.035+3.,p.y*.05-fl))-.5,vn(vec2(p.y*.045+9.,p.x*.03-fl*.8))-.5)+.4*vec2(vn(vec2(p.x*.14,p.y*.12-fl*2.))-.5,0.);float far_=smoothstep(0.,60.,a-b);
 h.xy+=w*(.10+.26*far_);vec2 u=(vec2(dot(h-shO,shX),h.y-shO.y)-shBox.xy)/shBox.zw;if(u.x<0.||u.x>1.||u.y<0.||u.y>1.) return vec2(0.);float l=1.+.9*far_;vec4 t=textureLod(tShad,u,l);float s=smoothstep(.22,.78,t.r+.08*w.x);return vec2(s*smoothstep(0.,.02,u.x)*smoothstep(1.,.98,u.x),textureLod(tShad,u,0.6).g);}
void surf(vec3 p,vec3 n,int m,inout Surf s){surf0(p,n,m,s);if(s.cls>3.5&&s.cls<4.5) return;
 vec3 d=fireP-p;float r=length(d);d/=r;vec2 S=shadow(p);float sh=S.x*shK*(m==6||m==10?1.:hutK);sh=mix(max(sh,dusk*(m==6?.62:.85)),max(sh,dusk*.85),0.);if(m==6) s.base*=1.+.9*dusk*(1.-S.x);float fall=1./(1.+r*r/(130.*130.));float nl=.30+.70*smoothstep(-.1,.65,dot(n,d));
 float fl=.90+.10*vn(vec2(fT*7.,1.))+.06*(vn(vec2(p.y*.02-fT*5.,p.x*.015))-.5);
 float gy_=smoothstep(130.,8.,p.y);vec3 b=s.base;
 s.base*=mix(vec3(1.),shTint,sh*.9)*(1.-.0*dusk);s.sh*=mix(vec3(1.),shTint,sh*.9);
 float mk=m==10?.10:m==6?mix(.30,1.15,exp(-dot(p.xy-hot.xy,(p.xy-hot.xy)*vec2(1.,1.3))/(hot.z*hot.z))):.30;emit(s,b*fireC*fireI*fall*nl*fl*(1.-sh)*mk);
 if(eyes>0.&&m==6) emit(s,vec3(1.6,.34,.05)*S.y*eyes);}
'''
DUSKL = dict(key=(-.7, .55, .45), keyCol='#5a4a7a', amb='#3a2c58', rim=(.5, .5, -.8), rimCol=(.10, .06, .12), bounceCol=(.05, .03, .04), envT='#8a6aa8', envM='#ff9a4a', envB='#2a1838', fogCol='#3a2448', fog=(.0030, 80., .004, 0.), inkRef=1.2, inkCol='#0a0410')
DUSKSKY = dict(cZen='#140c30', cMid='#5a1c3c', cHor='#d8541c', cLow='#7a2420', sunR=0., rays=.0, halo=0., sunGlow=.4, cov=.65, cLit='#e8703a', cCM='#7a2c40', cSh='#341638', cInk='#12081c', sunDir=(-.9, .10, -.6))


def placeu(**k):
    return {**dict(fireK=0., tone=0., line=0., lineLo=-1., lineC=.5, lineK=-1., lineR=24., rockH=84., lineG=.30, gA='#a8784c', gB='#5c3a34', leafA='#c8a850', leafB='#6a5428', rockA='#c08a6c', rockB='#5c3c48'), **k}


def trees(st, tint=(.50, .40, .46), mist='#3a2448', hz=1.1, season='summer', seed=3, near=True, far=True, back=True, right=True):
    """the ring of trees of worlds/forest.clearing, darker"""
    r = np.random.default_rng(seed); k = dict(hazeCol=mist, tint=tint, wind=.5)

    def ring(kind, n, r0, r1, a0, a1, hh, haze, sd, **q):
        a = np.linspace(a0, a1, n) + r.uniform(-.06, .06, n); R = r.uniform(r0, r1, n); P = np.c_[np.sin(a) * R, np.zeros(n) - .3, np.cos(a) * R]; FL.scatter(st, kind, P, hh, season=season, seed=sd, haze=min(.85, haze * hz), **{**k, **q})
    b0, b1 = 1.9, 4.4
    if far: ring('pahari_round', 16, 150, 230, b0 - .3, b1 + .3, 74, .42, 1); ring('mango', 12, 100, 150, b0 - .2, b1 + .2, 62, .24, 2); ring('palm', 7, 96, 150, b0, b1, 74, .22, 3)
    if back: ring('plantain', 5, 40, 58, 1.7, 2.3, 24, .03, 4); ring('plantain', 4, 42, 60, 4.0, 4.6, 26, .03, 5); ring('banyan', 1, 74, 78, 4.28, 4.3, 78, .06, 6); right and (ring('ashoka', 2, 64, 80, 1.75, 2.0, 50, .06, 7), ring('bamboo', 4, 66, 90, 1.5, 2.1, 56, .10, 8))
    if near: ring('shrub', 22, 56, 110, 1.3, 5.0, 10, .06, 9); ring('grass', 40, 34, 90, 0, 6.28, 6, .03, 10); ring('fern', 14, 44, 80, 1.2, 5.1, 8, .04, 11)


def line_point(a, R=24., y=.1):
    """the burning line at fraction a (0 behind the hut, .25 at -x, .5 at the front, .75 at +x)"""
    th = (a - .5) * 2 * math.pi
    return V(math.sin(th) * R, y, 4 + math.cos(th) * R)


def line_fire(st, t, lo=0., hi=1., h=2.4, n=220, R=24., seed=1, amt=1.):
    """standing flames along the line from fraction lo to hi, after close"""
    if hi <= lo: return
    r = np.random.default_rng(seed); a = np.sort(r.uniform(0, 1, n)); a = a[(a > lo) & (a < hi)]
    if not len(a): return
    edge = np.clip(np.minimum((a - lo) / .02 if lo > 0 else 1., (hi - a) / .02 if hi < 1 else 1.), 0, 1); s = np.array([h * (.55 + .75 * ((i * .618) % 1)) for i in range(len(a))]) * edge; s = s * (1 + .18 * np.sin(t * 11 + a * 400))
    P = np.array([line_point(x, R) for x in a]) + np.c_[np.zeros(len(a)), s * .8, np.zeros(len(a))]
    FX.particles(st, P, s, (1.0 * amt, .92 * amt, .85 * amt), 'tongue', seed=(a * 37) % 1)


def bowl(st, at, r=.8, rice=True, col=('#8a4a24', '#3a1a12', '#c87a3a'), up=(0, 1, 0)):
    """a wooden bowl of rice, opening upward, centre of its rim at `at`"""
    at = np.asarray(at, float); B = PR.place((0, 0, 0), up, (0, 0, 1))[:3, :3]
    prof = [(0., -.72), (.42, -.72), (.80, -.48), (1.0, -.10), (1.02, 0.), (.93, 0.), (.88, -.10)]
    def fn(u, v):
        q = CL.spline(np.array([(*p, 0.) for p in prof]), 60)[min(59, int(v * 59.99))]; th = u * 2 * math.pi
        return at + B @ V(q[0] * math.cos(th), q[1], q[0] * math.sin(th)) * r
    st.mesh(*CL.sheet(fn, 22, 16), kind=0, col=col, cls=1, ink=.85)
    if rice: st.mesh(*CL.sheet(lambda u, v: at + B @ V(.90 * v * math.cos(u * 6.2832), .34 * (1 - v * v) - .06, .90 * v * math.sin(u * 6.2832)) * r, 18, 8), kind=0, col=('#fff6e0', '#a890a0', '#fff'), cls=1, ink=.6)


# ------------------------------------------------------------------ the shadow theatre
UX, UY, UW, UH, PPU = -21., -1., 42., 33., 34      # the mask in figure units (a man is 16 tall)


def _stroke(c, P, w):
    d = np.gradient(P, axis=0); n = np.stack([-d[:, 1], d[:, 0]], 1); n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-9; k = (w * np.sin(np.linspace(.25, math.pi - .1, len(P))))[:, None] * .5; _path(c, np.vstack([P + n * k, (P - n * k)[::-1]]))


def _path(c, P): c.move_to(*P[0]); [c.line_to(*q) for q in P[1:]]; c.close_path()


_PROF = [(-.50, -2.1), (-.62, -1.35), (-.92, -.55), (-1.0, .15), (-.92, .70), (-1.22, .80), (-1.16, 1.02), (-.92, 1.10), (-.98, 1.45), (-.74, 1.62), (-.78, 2.0), (-.54, 2.15), (-.56, 2.5), (-.33, 2.62), (-.34, 2.95), (-.10, 3.06), (0., 3.75), (.10, 3.06), (.34, 2.95), (.33, 2.62), (.56, 2.5), (.54, 2.15), (.78, 2.0), (.74, 1.62), (.98, 1.45), (.92, 1.10), (1.16, 1.02), (1.16, .78), (.84, .66), (.80, .42), (.92, .26), (.80, .12), (1.05, -.12), (1.30, -.34), (1.18, -.46), (.90, -.44),
         (1.16, -.54), (1.50, -.46), (1.72, -.14), (1.62, -.56), (1.30, -.72), (.92, -.66), (1.0, -.80), (.86, -.92), (1.02, -1.20), (.80, -1.48), (.36, -1.52), (.30, -2.1)]
_PROF_S = smooth_path(np.array(_PROF[:6]), 5).tolist() + _PROF[6:31] + smooth_path(np.array(_PROF[31:]), 4).tolist()


def _eye(c, x, y, w, h, tilt):
    c.save(); c.translate(x, y); c.rotate(tilt); c.move_to(-w, 0); c.curve_to(-w * .4, h, w * .4, h, w, 0); c.curve_to(w * .4, -h * .7, -w * .4, -h * .7, -w, 0); c.restore()


class Theatre:
    """paints the shadow as a puppet-cutter would: r = the shadow, g = the eyes cut through it"""

    def __init__(s, st, figs):
        """figs: {'man': fn()} drawn black once with the stage, seen from the fire"""
        s.w, s.h = int(UW * PPU), int(UH * PPU); s.man = {}
        cam = Cam((UX + UW / 2, UY + UH / 2, 400), (UX + UW / 2, UY + UH / 2, 0), 2 * math.degrees(math.atan(UH / 2 / 400)))
        for k, fn in figs.items():
            st.clear('#000', f=0); st.cam = cam; L = Light(keyCol=(0, 0, 0), amb=(0, 0, 0), rimCol=(0, 0, 0), shadow=False, ink=0., inkRef=8., inkCol='#ffffff', fogCol='#ffffff', fog=(1e4, 0, 0, 0)); st.open(cam, L); fn(); st.close()
            a = np.frombuffer(st.L.fbo.read(components=4, attachment=0, dtype='f2') if hasattr(st.L, 'fbo') else st.L.read(components=4, attachment=0, dtype='f2'), np.float16).reshape(st.ph, st.pw, 4)[::-1, :, 3].astype(np.float32)
            import cv2
            sc = H / UH; x0 = W / 2 - UW / 2 * sc; a = np.clip(a, 0, 1); b = np.zeros((s.h, s.w), np.float32); M = np.array([[PPU / sc / st.k, 0, -x0 * PPU / sc], [0, PPU / sc / st.k, 0]]); b = cv2.warpAffine(a, M, (s.w, s.h), flags=cv2.INTER_AREA); b = (np.clip(b, 0, 1) * 255).astype(np.uint8); rgba = np.dstack([np.zeros_like(b)] * 3 + [b]).copy()
            s.man[k] = (rgba, cairo.ImageSurface.create_for_data(rgba, cairo.FORMAT_ARGB32, s.w, s.h))
        s.tex = gl.ctx().texture((s.w, s.h), 4, dtype='f1'); s.tex.swizzle = 'BGRA'; s.tex.repeat_x = s.tex.repeat_y = False; import moderngl as mgl; s.tex.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR); s.tex.anisotropy = 8.

    def _piece(s, c, draw, gap=.20):
        """a part laid over the others with a thin line of light round it"""
        if gap > 0:
            c.save(); c.set_operator(cairo.OPERATOR_DEST_OUT); c.set_source_rgba(0, 0, 0, .95); c.set_line_width(gap * 2); c.set_line_join(cairo.LINE_JOIN_ROUND); draw(c); c.stroke(); c.restore()
        c.set_source_rgba(1, 0, 0, 1); draw(c); c.fill()

    def _cut(s, c, draw, eye=0.):
        """cut light through the shadow; eye > 0 also writes the eye channel"""
        c.save(); c.set_operator(cairo.OPERATOR_DEST_OUT); c.set_source_rgba(0, 0, 0, 1); draw(c); c.fill(); c.restore()
        if eye > 0: c.save(); c.set_operator(cairo.OPERATOR_ADD); c.set_source_rgba(0, eye, 0, 1); draw(c); c.fill(); c.restore()

    def head(s, c, x, y, sc, side, tilt, eye, gap=.11):
        """a profile head looking toward side (+1 right, -1 left)"""
        c.save(); c.translate(x, y); c.rotate(tilt); c.scale(sc * side, sc)
        s._piece(c, lambda c: _path(c, _PROF_S), gap)
        for q in ((-.55, .92), (-.18, .92), (.20, .92), (.58, .92)): s._cut(c, lambda c: c.arc(q[0], q[1], .085, 0, 7))
        for q in ((0, 1.36, .15), (0, 2.02, .12), (0, 2.55, .09)): s._cut(c, lambda c: c.arc(q[0], q[1], q[2], 0, 7))
        s._cut(c, lambda c: (c.arc(-.42, -.86, .30, 0, 7), c.new_sub_path(), c.arc_negative(-.42, -.86, .17, 7, 0)))
        if eye > 0: s._cut(c, lambda c: _eye(c, .50, .10, .30, .20 * eye, .16), eye)
        c.restore()

    def front(s, c, x, y, sc, crown, eye, hd=1., gap=.12):
        """the main head, full face, his crown rising out of the topknot"""
        c.save(); c.translate(x, y); c.scale(sc, sc)

        def shape(c):
            c.move_to(-.95, .75); c.curve_to(-1.02, .0, -.95, -.6, -.55, -1.2); c.curve_to(-.3, -1.5, .3, -1.5, .55, -1.2); c.curve_to(.95, -.6, 1.02, .0, .95, .75); c.curve_to(.6, 1.2, -.6, 1.2, -.95, .75); c.close_path()
        s._piece(c, shape, gap * hd)
        if crown > .01:
            R = [(1.22, .70), (1.30, .95), (1.02, 1.05), (1.10, 1.50), (.84, 1.66), (.88, 2.08), (.62, 2.22), (.64, 2.62), (.38, 2.74), (.40, 3.10), (.12, 3.20), (0., 4.1)]; P = [(a, .70 + (b - .70) * crown) for a, b in R]; P = P + [(-a, b) for a, b in P[::-1][1:]]
            s._piece(c, lambda c: _path(c, P), gap)
            for k in (-1, 1):      # side plumes, moustache ends, ear rings
                s._piece(c, lambda c: _path(c, smooth_path(np.array([(.95 * k, -.45), (1.35 * k, -.62 + .0 * crown), (1.72 * k, -.36), (1.86 * k, .06), (1.62 * k, -.68), (1.1 * k, -.80)]) * np.array([crown, 1.]), 5, True)), 0.)
            for q in ((-.66, .95), (-.33, .97), (.33, .97), (.66, .95)): s._cut(c, lambda c: c.arc(q[0], .70 + (q[1] - .70) * crown, .09 * crown, 0, 7))
            s._cut(c, lambda c: _eye(c, 0, .70 + .80 * crown, .20 * crown, .30 * crown, 0))
            for q in (1.9, 2.5): s._cut(c, lambda c: c.arc(0, .70 + (q - .70) * crown, .12 * crown, 0, 7))
        if eye > 0:
            for k in (-1, 1):
                s._cut(c, lambda c: _eye(c, .42 * k, .12, .30, .19 * eye, .20 * k), eye)
                for P, w in (([(.16, .30), (.42, .47), (.76, .58)], .10),): s._cut(c, lambda c: _stroke(c, smooth_path(np.array(P) * np.array([k, 1.]), 8), w * eye))
        c.restore()

    def arm(s, c, x, y, a0, a1, l0, l1, weapon, wl, w=1., gap=.11):
        """upper arm at angle a0, fore-arm at a1 (degrees, 0 = out to the right); weapon along its own angle"""
        a, b = math.radians(a0), math.radians(a1); ex, ey = x + l0 * math.cos(a), y + l0 * math.sin(a); hx, hy = ex + l1 * math.cos(b), ey + l1 * math.sin(b)

        def limb(c):
            for (px, py, qx, qy, r0, r1) in ((x, y, ex, ey, .62 * w, .46 * w), (ex, ey, hx, hy, .48 * w, .30 * w)):
                d = math.hypot(qx - px, qy - py) or 1.; nx, ny = -(qy - py) / d, (qx - px) / d
                c.move_to(px + nx * r0, py + ny * r0); c.line_to(qx + nx * r1, qy + ny * r1); c.line_to(qx - nx * r1, qy - ny * r1); c.line_to(px - nx * r0, py - ny * r0); c.close_path(); c.new_sub_path(); c.arc(qx, qy, r1, 0, 7); c.new_sub_path()
            c.arc(hx, hy, .50 * w, 0, 7)
        if wl > .01:
            c.save(); c.translate(hx, hy); c.rotate(b); s._piece(c, lambda c: s.weapon(c, weapon, wl), gap); c.restore()
        s._piece(c, limb, gap)
        for u in (.55, .62): s._cut(c, lambda c: c.arc(x + (ex - x) * u, y + (ey - y) * u, .07, 0, 7))
        return hx, hy

    def weapon(s, c, k, L):
        """along +x from the fist; L 0..1"""
        if k == 0:                       # curved sword
            n = 4.6 * L; c.move_to(-.8, -.14); c.line_to(.35, -.14); c.line_to(.35, -.55); c.line_to(.6, -.55); c.line_to(.6, -.2); c.curve_to(n * .5, -.15, n * .8, .0, n, .95); c.curve_to(n * .75, .72, n * .5, .58, .6, .34); c.line_to(.6, .60); c.line_to(.35, .60); c.line_to(.35, .14); c.line_to(-.8, .14); c.close_path()
        elif k == 1:                     # mace
            n = 3.6 * L; c.rectangle(-.9, -.13, n + .9, .26); c.new_sub_path(); c.arc(n, 0, .95 * L, 0, 7); c.new_sub_path(); c.arc(n + .95 * L, 0, .25, 0, 7)
        elif k == 2:                     # trident
            n = 4.4 * L; c.rectangle(-1.2, -.11, n + 1.2, .22); c.new_sub_path(); _path(c, [(n - .2, -.95), (n + 1.7 * L, -.85), (n + .2, -.62), (n + .2, -.16), (n + 2.1 * L, 0), (n + .2, .16), (n + .2, .62), (n + 1.7 * L, .85), (n - .2, .95)])
        elif k == 3:                     # discus
            for i in range(24):
                a = i / 24 * 6.2832; r = (1.25 if i % 2 else .95) * L; (c.move_to if i == 0 else c.line_to)(1.2 * L + r * math.cos(a), r * math.sin(a))
            c.close_path(); c.new_sub_path(); c.arc_negative(1.2 * L, 0, .5 * L, 7, 0)
        elif k == 4:                     # spear
            n = 5.2 * L; c.rectangle(-2., -.10, n + 2., .20); c.new_sub_path(); _path(c, [(n, -.42), (n + 1.7 * L, 0), (n, .42), (n - .25, 0)])
        elif k == 5:                     # axe
            n = 3.6 * L; c.rectangle(-.8, -.12, n + .8, .24); c.new_sub_path(); c.move_to(n - 1., .1); c.curve_to(n - 1., .9, n - 1.2, 1.2, n - 1.5, 1.5); c.curve_to(n - .4, 1.75, n + .5, 1.6, n + .9, 1.2); c.curve_to(n + .4, .9, n + .1, .6, n + .1, .1); c.close_path()

    def paint(s, fn):
        sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, s.w, s.h); c = cairo.Context(sf); c.scale(PPU, -PPU); c.translate(-UX, -(UY + UH)); fn(c); sf.flush()
        s.tex.write(np.ndarray((s.h, s.w, 4), np.uint8, sf.get_data())[::-1].copy().tobytes()); s.tex.build_mipmaps(); return s.tex

    def person(s, c, k='man', alpha=1.):
        c.save(); c.identity_matrix(); c.set_source_rgba(1, 0, 0, alpha); c.mask_surface(s.man[k][1], 0, 0); c.restore()

    def king(s, c, b):
        """the body: from a thread inside the man's outline (b 0) to the king (b 1)"""
        if b <= 0: return
        R = [(.0, 12.9), (1.0, 12.75), (2.5, 12.5), (3.5, 11.9), (3.6, 11.0), (2.5, 10.2), (2.0, 8.9), (1.75, 7.9), (2.5, 6.6), (3.3, 4.2), (3.9, 1.5), (4.4, -.5)]; P = [(x * (.25 + .75 * b), y) for x, y in R]; P = P + [(-x, y) for x, y in P[::-1]]
        s._piece(c, lambda c: _path(c, smooth_path(np.array(P), 5)), .16 * b)
        for i in range(7): s._cut(c, lambda c: c.arc((i - 3) * .55 * b, 11.2 - .12 * (9 - (i - 3) ** 2) * .5, .11 * b, 0, 7))
        for i in range(5): s._cut(c, lambda c: c.arc((i - 2) * .55 * b, 7.6, .10 * b, 0, 7))


# arms of the wheel: (angle of the upper arm, of the fore-arm, weapon), from the top down; mirrored
WHEEL = [(84, 92, 4), (68, 78, 0), (52, 64, 2), (37, 50, 1), (22, 36, 0), (7, 20, 3), (-9, 4, 5), (-25, -12, 4), (-42, -30, 0)]
HEADS = [(1, 1), (-1, 1), (1, 2), (-1, 2), (1, 3), (-1, 3), (1, 4), (-1, 4), (1, 5)]                        # the order in which the nine come
BEATS = [36, 42, 48, 54, 60, 66, 66, 72, 72]


def shadow_at(T, f):
    """paint the shadow of frame f (c4): the man, then the nine heads on their beats, the wheel of arms from f54, crowns, swords"""
    t = f / 24.; b = smooth(50, 72, f); tr = lambda k, a=.06: a * math.sin(t * 5.1 + k * 2.3)

    def fn(c):
        wheel = smooth(52, 60, f)
        # the arms, from behind: the fan opens like a peacock's train
        for j, (a0, a1, w) in enumerate(WHEEL):
            for sd in (1, -1):
                st_ = 54 + (len(WHEEL) - 1 - j) * 1.6 + (0 if sd > 0 else .8); k = back_out((f - st_) / 8., 1.2) if f > st_ else 0.
                if k <= 0: continue
                wob = 2.2 * math.sin(t * 2.6 + j * 1.3 + sd); A0, A1 = lerp(-76, a0, k) + wob, lerp(-84, a1, k) + wob * 1.8; wl = smooth(st_ + 4, st_ + 11, f); L = 5.0 * (.35 + .65 * min(1, k))
                c.save(); c.scale(sd, 1); T.arm(c, 2.2, 11.6, A0, A1, L, 4.6 * (.35 + .65 * min(1, k)), w, wl * (1 if not (j == 1 and sd > 0) else 1), 1.0); c.restore()
        T.person(c, 'man'); T.king(c, b)
        # the staff: lifted, turned, a sword
        u = smooth(48, 58, f)
        c.save(); c.translate(lerp(2.0, 2.4, u), lerp(9.0, 11.0, u)); c.rotate(math.radians(lerp(91., 112, u) - 18 * smooth(58, 64, f))); c.set_source_rgba(1, 0, 0, 1); c.set_line_width(.34); c.move_to(-8.6 * (1 - u * .9), 0); c.line_to(5.2, .12 * math.sin(t)); c.stroke()
        if u > .05: T._piece(c, lambda c: (c.save(), c.translate(2.5, 0), T.weapon(c, 0, 1.25 * u), c.restore()), .12)
        c.restore()
        # heads
        for (sd, n), f0 in list(zip(HEADS, BEATS))[::-1]:
            if f < f0: continue
            k = back_out((f - f0) / 6., 1.9); e = min(1., (f - f0) / 4.); x1, y1 = sd * (1.95 * n + .25 - .02 * n * n), 14.75 - .155 * n * n + .25 * n; y1 += .16 * math.sin(t * 3.1 + n * 1.7 + sd); x = x1 * k; y = lerp(13.7, y1, k) + 1.1 * math.sin(math.pi * min(1., k)) * (1 - min(1, k)); sc = lerp(.75, 1.10 - .055 * n, min(1, e))
            # the neck
            q = np.array([(sd * .3, 12.3), (sd * (.35 + .45 * abs(x)), 12.55 - .05 * n), (x - sd * .35 * sc, y - 2.0 * sc), (x - sd * .25 * sc, y - 1. * sc)]); N = smooth_path(q, 10); wd = np.linspace(.62, .42, len(N)) * sc; d = np.gradient(N, axis=0); nn = np.stack([-d[:, 1], d[:, 0]], 1); nn /= np.linalg.norm(nn, axis=1, keepdims=True) + 1e-9; A = np.vstack([N + nn * wd[:, None], (N - nn * wd[:, None])[::-1]])
            T._piece(c, lambda c: _path(c, A), .05)
            T.head(c, x, y, sc * (1 + .12 * math.sin(math.pi * e)), sd, sd * (-.02 - .045 * n) * 1 + .05 * math.sin(t * 2.3 + n), smooth(f0 + 2, f0 + 7, f))
        T.front(c, 0, lerp(13.75, 14.35, b), lerp(.96, 1.28, b), smooth(50, 64, f), smooth(62, 68, f), hd=smooth(36, 44, f))
    return T.paint(fn)


# ------------------------------------------------------------------ light on a lens
VIGN = '''
in vec2 uv;out vec4 o;uniform vec3 col;uniform float a0,a1;uniform vec2 c;
void main(){float r=length((uv-c)*vec2(1.6,1.));float k=smoothstep(a0,a1,r);o=vec4(col*k,k);}
'''


def rain(st, t, n=220, box=((-30, 0, -30), (30, 40, 30)), seed=3, v=(-2.2, -46, 0), size=.02, length=.55, col='#b8ccd8', a=.4):
    r = np.random.default_rng(seed); lo, hi = np.array(box, float); v = np.asarray(v, float); P = r.uniform(0, 1, (n, 3)) * (hi - lo); P = lo + np.mod(P + v * t * r.uniform(.85, 1.15, (n, 1)), hi - lo)
    FX.particles(st, P, size * r.uniform(.6, 1.4, n), col, 'rain', vel=np.tile(nz(v) * length, (n, 1)), alpha=a)


# ------------------------------------------------------------------ the earth torn out along the line
TORN = _HUT.replace('#define TMAX 900.', '#define TMAX 1600.') + '''
uniform vec3 islT;uniform mat3 islR;uniform float gap,depth,canopy,redK,wetK;
const vec3 IC=vec3(0.,0.,4.);
float ringR(float a,float y){float r=23.4+.9*sin(a*5.+1.)+.5*sin(a*13.+y*.3)+.35*sin(a*29.);float h=abs(a-.64);return r-4.6*exp(-h*h*38.);}
vec3 isl(vec3 p){return transpose(islR)*(p-IC-islT)+IC;}
vec2 island(vec3 p){vec3 q=isl(p);vec3 c=q-IC;float bb=max(length(c.xz)-30.,max(c.y-34.,-c.y-24.));if(bb>6.) return vec2(bb,0.);float r=length(c.xz),a=atan(c.x,c.z);float R=ringR(a,0.)-gap;float n=vn3(q*.22);
 float lo=-(4.+15.*pow(max(0.,1.-r/(R+.5)),.55)*(.75+.5*vn(vec2(a*2.5,3.))))-2.2*n-1.4*abs(sin(a*7.+q.y*.7));float top=q.y-.12*vn(q.xz*.5);float side=r-R-(.8*vn3(q*.55)-.4)-.10*q.y;
 float d=max(max(top,side),lo-q.y)*.50;vec2 m=vec2(d,20.);if(top>-.35&&side<-.3) m.y=M_GROUND;
#ifndef NOHUT
 m=U(m,hut(q));
#endif
 return m;}
float canopyH(vec2 q){float l=length(q-vec2(0,12.));float k=smoothstep(58.,74.,l);if(k<=0.) return -3.;vec4 v=voro(q*.036);vec4 v2=voro(q*.13+3.);return k*(8.+26.*sqrt(max(0.,1.-1.2*v.x*v.x))*(.55+.45*v.z)+3.*(1.-v2.x)+16.*vn(q*.006)+smoothstep(160.,800.,l)*(90.*vn(q*.0045+2.)*vn(q*.0019)));}
vec2 map(vec3 p){vec2 q=p.xz-IC.xz;float r=length(q),a=atan(q.x,q.y);float hole=smoothstep(ringR(a,p.y)+.5,ringR(a,p.y)-2.2-.25*depth,r);float g=gy(p.xz)-depth*hole*(.72+.28*vn(p.xz*.16)+.10*vn(p.xz*.7));float lip=1.5*exp(-pow((r-ringR(a,0.)-1.6)/1.3,2.))*min(1.,depth*.2)*vn(p.xz*.5+3.);
 vec2 m=vec2((p.y-g-lip-.12*vn(p.xz*.5))*(hole>.01&&hole<.99?.42:.8),hole*depth>.06?21.:M_GROUND);
#ifdef CANOPY
 if(p.y<130.){float h=canopyH(p.xz);m=U(m,vec2((p.y-h)*.5,22.));}else m=U(m,vec2((p.y-118.)*.9,22.));
#endif
#ifndef NOHUT
 m=U(m,hearth(p));
#endif
#ifndef NOROCK
 m=U(m,rockf(p));
#endif
#ifndef NOISLE
 m=U(m,island(p));
#endif
 return m;}
void surf(vec3 p,vec3 n,int m,inout Surf s){vec3 q=p;bool is=false;
#ifndef NOISLE
 is=island(p).x<.05+.6*gPx;if(is) q=isl(p);
#endif
 if(m==20||m==21){vec3 c=q-IC;float a=atan(c.x,c.z);float ly=q.y+.9*vn(vec2(a*6.,q.y*.4));float st=fract(ly*.34),id=floor(ly*.34);vec3 b=mix(hex(0x8a4a30),hex(0x4a2420),h11(id+3.)*.8);b=mix(b,hex(0xb87848),step(.82,st)*.5);b*=.82+.34*vn3(q*.9);float stn=voro(vec2(a*7.,q.y*.45)).x;b=mix(b,hex(0x9a8a80)*.7,smoothstep(.22,.15,stn)*step(.5,h11(id+9.)));
  float rt=abs(fbm(vec2(a*9.+q.y*.05,q.y*.16))-.5);b=mix(b,hex(0x2a1610),smoothstep(.035,.015,rt)*.8);if(m==21) b*=mix(1.,.62,smoothstep(-2.,-12.,p.y));s.base=b*(1.-.45*tone);s.sh=b*vec3(.30,.24,.34)*(1.-.3*tone);s.ink=.75;s.part=float(m);if(m==21){s.part=10.;s.ink=mix(.24,.6,0.);}
  if(wetK>0.&&m==21){float w=smoothstep(-depth*.80,-depth*.86,p.y+.6*vn(p.xz*.4));s.base=mix(s.base,mix(uAmb,uKey,.35),w*wetK);s.cls=w*wetK>.5?8.:1.;}}
 else if(m==22){vec4 v=voro(p.xz*.036);vec4 v2=voro(p.xz*.13+3.);vec4 v3=voro(p.xz*.42);float t=.5+.5*n.y;vec3 b=mix(leafB,leafA,smoothstep(.35,.95,t)*(.4+.6*v.z));b*=.78+.35*v2.z;b=mix(b,b*.55,smoothstep(.45,.60,v3.x));s.base=b;s.sh=b*vec3(.30,.26,.50);s.ink=.2;s.part=22.+mod(floor(v.z*40.),38.);}
 else {if(is){s.ns=n;}surf0(q,n,m,s);}
 if(redK>0.) emit(s,s.base*vec3(1.,.16,.06)*redK*max(0.,.3+.7*dot(n,normalize(vec3(-.2,1.,.3)))));}
'''


def tornu(T=(0, 0, 0), R=None, gap=.0, depth=0., canopy=0., red=0., wet=0., **k):
    return {**placeu(lineG=0.), **dict(islT=tuple(T), islR=(np.eye(3) if R is None else R), gap=float(gap), depth=float(depth), canopy=float(canopy), redK=float(red), wetK=float(wet)), **k}


def isle(p, T, R): return V(0, 0, 4) + np.asarray(T, float) + R @ (np.asarray(p, float) - V(0, 0, 4))


def roots(st, T, R, t, n=26, seed=4, vel=(0, 0, 0)):
    """roots and creepers that hang from the torn edge, trailing behind the motion"""
    r = np.random.default_rng(seed); A, B = [], []
    from chars.jatayu import join
    for i in range(n):
        a = r.uniform(0, 6.28); rr = r.uniform(12, 22.); y0 = -2. - (23 - rr) * r.uniform(.3, .75); p = isle((math.sin(a) * rr, y0, 4 + math.cos(a) * rr), T, R); L = r.uniform(5, 13); k = np.linspace(0, 1, 9)[:, None]; w = r.uniform(-1, 1, 3)
        P = p + k * L * V(.25 * w[0], -1, .25 * w[2]) - k ** 2 * np.asarray(vel, float) * L * .05 + np.c_[np.sin(k[:, 0] * 4 + t * 3 + i), 0 * k[:, 0], np.cos(k[:, 0] * 3.4 + t * 2.6 + i * 2)] * k * 1.3; (A if i % 3 else B).append(CL.tube(P, [.42 * (.6 + r.uniform()), .25, .05], 6, 14))
    st.mesh(*join(A), kind=0, col=('#5a3424', '#20101a', '#000'), cls=1, ink=.8); st.mesh(*join(B), kind=0, col=('#4a4a2a', '#1a1a1c', '#000'), cls=1, ink=.8)


def _clod(r, seed):
    q = np.random.default_rng(seed); ph = q.uniform(0, 6.28, 9)
    def fn(u, v):
        a, b = u * 6.28318, (v - .5) * math.pi; d = V(math.cos(a) * math.cos(b), math.sin(b), math.sin(a) * math.cos(b)); k = 1 + .22 * math.sin(2.3 * d[0] + ph[0] + 1.7 * d[1]) + .18 * math.sin(3.7 * d[1] + ph[1]) + .16 * math.sin(4.1 * d[2] + ph[2] + d[0] * 2); d = np.round(d * 2.6 + .25 * np.sin(ph[3:6])) / 2.6 * .45 + d * .55
        return d * k * r
    return CL.sheet(fn, 13, 9)


_CL = [_clod(1., k) for k in range(6)]


def stones(st, t, at, n=40, seed=3, up=14., spread=24., size=1.2, grav=5., col=('#8a5a44', '#34202a', '#000')):
    """clods of earth flung up from the ring (world), t seconds since the tear"""
    if t <= 0: return
    from chars.jatayu import join, xform
    r = np.random.default_rng(seed); at = np.asarray(at, float); A = []
    for i in range(n):
        a = r.uniform(0, 6.28); rr = spread * r.uniform(.85, 1.12); sp = up * r.uniform(.3, 1.2); o = r.uniform(-.5, 4.); p = at + V(math.sin(a) * (rr + o * t), sp * t - grav * t * t * .5, math.cos(a) * (rr + o * t)); s = size * (.25 + r.uniform() ** 2.2); w = r.uniform(-1, 1, 5)
        if p[1] > -3: A.append(xform(_CL[i % 6], model(p, 360 * w[0] + 260 * t * w[1], 360 * w[2] + 220 * t * w[3], 0, s)))
    if A: st.mesh(*join(A), kind=0, col=col, cls=1, ink=.8)
