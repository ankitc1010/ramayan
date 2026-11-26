"""HANUMAN, and the painter of vanara faces."""
import numpy as np, math, cairo
from dataclasses import dataclass
from lau.stage import Fig, hexc
from lau.rig import Pose, V, nz
from lau.face import Face, Pen, INK, rgb
from lau import cloth as CL
DIM = dict(chest=3.15, shx=2.32, shy=.86, shz=-.12, neck=1.46, nz=-.02, head=1.46, hz=.36, up=2.75, fore=2.65, hipx=.70, hipy=-.30, th=3.35, sh=3.28, hand=1.0, foot=1.2)
BUILD = dict(chest=1.17, depth=1.18, rib=1.05, waist=1.04, hips=1.06, arm=1.58, leg=1.36, hand=1.42, neck=1.2, shoulder=1.)
FUR, SKIN, LIGHT, DARK = ('#da7a1e', '#83361a', 1), ('#e25f42', '#8a2636', 1), ('#f4b663', '#a8552e', 1), ('#7a3318', '#34120e', 1)
PAL = {1: FUR, 2: ('#f3bd6a', '#a6582c', 1), 3: ('#ffe9bc', '#805030', 2), 4: ('#c4142c', '#54081c', 3), 5: ('#0f7a58', '#063a34', 3), 6: ('#f7efdc', '#c0a090', 1), 7: ('#c4222c', '#660f22', 1), 8: ('#c4222c', '#660f22', 1), 9: ('#fbf0d6', '#b08a78', 1), 11: SKIN, 12: FUR, 13: FUR, 14: LIGHT}
HS = [1.17, 1.10, 1.05, 1.05, 1.10, 1.1, 1., 1.05]


@dataclass(frozen=True)
class VFace(Face):
    """Face plus a lid multiplier per eye (lidL = his own left eye), for a single opening eye"""
    lidL: float = 1.
    lidR: float = 1.

    def mix(s, o, t): return VFace(**{k: round((1 - t) * getattr(s, k) + t * getattr(o, k, 1.), 3) for k in s.__dataclass_fields__})


STY = dict(iris='#f0a41e', iris2='#8a3c08', ring='#3a1206', sclera='#fff3da', brow='#3a1410', browt=1.15, line='#4a0f18', muzzle='#f3a47c', socket='#a82c34', lip='#9c2c34', lip2='#b5443f', liphi='#f6b48c', kohl='#25070f', mouthw=1., tilak=True, cheek='#d8402a', nosepad=None, old=0., eye=1.06, mouthin='#3a0612')


def vface(F, st=None, box=(-1.1, -1.25, 1.1, .95), S=1280):
    """paint a vanara's face for expression F; st overrides STY"""
    k = {**STY, **(st or {})}; P = Pen(S, box); c = P.c; L = k['line']

    def glow(x, y, rx, ry, col, a):
        c.save(); c.translate(x, y); c.scale(rx, ry); g = cairo.RadialGradient(0, 0, .35, 0, 0, 1); r = rgb(col); g.add_color_stop_rgba(0, *r, a); g.add_color_stop_rgba(.75, *r, a * .75); g.add_color_stop_rgba(1, *r, 0); c.set_source(g); c.arc(0, 0, 1, 0, 7); c.fill(); c.restore()
    jd = F.mouth * .26
    glow(0, -.60 - jd * .4, .50, .36 + jd * .5, k['muzzle'], .95)
    for sd in (1, -1): glow(sd * .34, .04, .34, .24, k['socket'], .38); glow(sd * .52, -.24, .24, .20, k['cheek'], .30)
    eyes(P, F, k); nose(P, F, k); vmouth(P, F, k)
    if k['tilak']:
        P.line([(-.088, .60), (-.088, .36, -.055, .22, 0, .165), (.055, .22, .088, .36, .088, .60)], .038, '#fff3cf'); P.fill([(-.024, .60), (-.032, .42, -.022, .30, 0, .235), (.022, .30, .032, .42, .024, .60)], '#c8102a')
    return P.out()


def eyes(P, F, k):
    c = P.c; L = k['line']
    for sd in (1, -1):
        lid = min(1.25, max(0., F.lid * (getattr(F, 'lidL', 1.) if sd > 0 else getattr(F, 'lidR', 1.))))
        up = -.045 + .205 * lid; lo = -.070 + .025 * max(F.smile, 0) * (lid > .2) + .055 * F.squint
        c.save(); c.scale(sd, 1); c.translate(.335, .03); c.scale(k['eye'], k['eye']); c.rotate(.04); c.translate(-.335, -.03)
        wy = .125 * (.15 + .85 * lid) - .02 * (1 - lid)
        eye = [(.115, -.045), (.18, up * .72 - .005, .26, up + .012, .345, up), (.43, up - .015, .49, wy - .03, .555, wy - .05), (.48, lo + .035, .41, lo, .31, lo - .004), (.24, lo, .17, -.062, .115, -.045)]
        for w, a in ((.13, .10), (.09, .14), (.055, .22), (.03, .35)): P.path(eye, True); P.col(k['kohl'], a); c.set_line_width(w); c.stroke()
        if lid > .05:
            P.fill(eye, k['sclera']); c.save(); P.path(eye, True); c.clip()
            ix, iy = .335 + F.gx * .10 * sd, .040 + F.gy * .07; r = .124
            P.col(k['ring']); c.arc(ix, iy, r, 0, 7); c.fill()
            g = cairo.RadialGradient(ix, iy - .05, .01, ix, iy, r * .92); a, b = rgb(k['iris']), rgb(k['iris2']); g.add_color_stop_rgba(0, *a, 1); g.add_color_stop_rgba(.55, *[a[i] * .75 + b[i] * .25 for i in range(3)], 1); g.add_color_stop_rgba(1, *b, 1); c.set_source(g); c.arc(ix, iy, r * .88, 0, 7); c.fill()
            for i in range(22):                                    # the fibres of the iris
                q = i / 22 * 6.2832; u = .6 + .25 * ((i * 7) % 5) / 4; P.line([(ix + math.cos(q) * r * .42, iy + math.sin(q) * r * .42), (ix + math.cos(q) * r * u, iy + math.sin(q) * r * u)], .006, '#ffd468' if i % 2 else k['iris2'], .5)
            P.col('#0a0406'); c.arc(ix, iy, .056 * F.pupil, 0, 7); c.fill()
            if F.glow > 0:
                g = cairo.RadialGradient(ix, iy, .0, ix, iy, r); g.add_color_stop_rgba(0, 1, .96, .65, F.glow); g.add_color_stop_rgba(.5, 1, .62, .15, F.glow); g.add_color_stop_rgba(1, 1, .3, .05, F.glow * .6); c.set_source(g); c.arc(ix, iy, r, 0, 7); c.fill()
            P.col('#ffffff'); c.arc(ix - .040 * sd, iy + .050, .030, 0, 7); c.fill(); P.col('#ffdca0', .9); c.arc(ix + .042 * sd, iy - .052, .017, 0, 7); c.fill()
            if F.spark > 0:                                         # a flame reflected in the eye
                for h, col in ((1., '#ff7a1a'), (.74, '#ffb638'), (.46, '#fff6cc')):
                    b = iy - .078; P.fill([(ix, b), (ix + .062 * h, b + .012 * h, ix + .050 * h, b + .085 * h, ix + .004, b + .190 * h), (ix - .040 * h, b + .11 * h, ix - .066 * h, b + .012 * h, ix, b)], col, F.spark)
            g = cairo.LinearGradient(0, up + .02, 0, up - .10); g.add_color_stop_rgba(0, .14, .03, .06, .80); g.add_color_stop_rgba(1, .14, .03, .06, 0); c.set_source(g); c.paint(); c.restore()
        # upper lid: a heavy painted line with a tail
        P.fill([(.095, -.065), (.16, up * .78, .26, up + .045, .35, up + .038), (.46, up + .012, .53, wy - .01, .665, wy + .035), (.56, wy - .045, .50, wy - .055, .44, up - .050 * max(.25, lid)), (.36, up - .012, .27, up - .014, .20, up * .55 - .015), (.16, .02 * lid - .04, .13, -.03, .095, -.065)], INK)
        P.line([(.10, -.06), (.22, lo - .016, .33, lo - .020, .42, lo + .022), (.48, lo + .05, .52, wy - .075, .57, wy - .04)], .018, INK)
        if lid > .15: P.line([(.17, up * .9 + .045), (.26, up + .090, .38, up + .090, .52, wy + .035)], .013, L, .85)
        P.line([(.15, lo - .055), (.26, lo - .085, .36, lo - .080, .46, lo - .030)], .012, L, .55)
        if F.squint > .3 or F.smile > .6: P.line([(.22, lo - .10), (.30, lo - .115, .38, lo - .10, .45, lo - .06)], .010, L, .5)
        for i in range(3): P.line([(.60, .00 - .05 * i), (.64, .01 - .06 * i, .66, .01 - .07 * i, .69, .02 - .085 * i)], .010, L, .35 + .4 * k['old'])
        if F.tear > 0: P.fill([(.30, lo - .02), (.36, lo - .02, .385, lo - .10 - .3 * F.tear, .345, lo - .16 - .42 * F.tear), (.305, lo - .20 - .42 * F.tear, .265, lo - .14 - .42 * F.tear, .30, lo - .02)], '#e8f6ff', .8); P.col('#ffffff', .9); c.arc(.328, lo - .10 - .40 * F.tear, .012, 0, 7); c.fill()
        c.restore()
        # brow: one strong brushed shape with a few hairs lifting from it
        c.save(); c.scale(sd, 1); t = k['browt']
        i0 = -F.frown * .115 + F.sad * .10 + F.brow * .06; i1 = F.brow * .10 - F.frown * .02; i2 = F.brow * .05 + F.frown * .07 - F.sad * .09
        P.fill([(.075, .215 + i0), (.16, .34 + i0 * .6 + i1 * .4, .38, .415 + i1, .68, .255 + i2), (.46, .335 + i1 - .03 * (t - 1), .25, .285 + i0 * .5 + i1 * .5 - .06 * (t - 1), .085, .150 + i0 - .06 * (t - 1))], k['brow'])
        B4 = np.array([(.075, .215 + i0), (.16, .34 + i0 * .6 + i1 * .4), (.38, .415 + i1), (.68, .255 + i2)])
        for i in range(9):                                          # hairs that lift from its upper edge
            q = .06 + .80 * i / 8; w3 = np.array([(1 - q) ** 3, 3 * q * (1 - q) ** 2, 3 * q * q * (1 - q), q ** 3]); d3 = np.array([-3 * (1 - q) ** 2, 3 * (1 - q) ** 2 - 6 * q * (1 - q), 6 * q * (1 - q) - 3 * q * q, 3 * q * q])
            p = w3 @ B4; d = nz(d3 @ B4); m = np.array((-d[1], d[0])); a, b, e = p - d * .030 - m * .020, p + d * .050 - m * .022, p + d * .085 + m * (.036 - .020 * q); P.fill([tuple(a), (*(p - d * .01 + m * .016), *(p + d * .04 + m * .030), *e), (*(p + d * .07 + m * .008), *b, *b)], k['brow'])
        if F.frown > .2: P.line([(.045, .08 + i0 * .4), (.055, .14, .06, .19, .045, .245 + i0 * .3)], .016, L, .8); P.line([(.0, .30), (.02, .27, .02, .22, .0, .20)], .012, L, .4)
        if F.brow > .4 or F.sad > .4: P.line([(.12, .46), (.25, .50, .38, .50, .50, .45)], .011, L, .45)
        c.restore()


def nose(P, F, k):
    c = P.c; L = k['line']
    if k['nosepad']: P.fill([(-.20, -.19), (-.10, -.14, .10, -.14, .20, -.19), (.27, -.26, .20, -.35, 0, -.365), (-.20, -.35, -.27, -.26, -.20, -.19)], k['nosepad'])
    for sd in (1, -1):
        c.save(); c.scale(sd, 1); w = .02 * F.frown + .015 * F.teeth
        P.line([(.085, .06), (.10, -.04, .10, -.12, .16, -.20)], .012, L, .45)
        P.line([(.15, -.185), (.235 + w, -.20, .245 + w, -.30, .185 + w, -.335)], .017, L, .9)
        P.fill([(.035, -.335), (.055, -.295, .125 + w, -.290, .160 + w, -.325), (.125 + w, -.320, .07, -.330, .035, -.335)], INK, .95)
        P.line([(.0, -.365), (.06, -.355, .12, -.35, .185 + w, -.335)], .014, L, .8)
        P.line([(.24, -.335), (.36, -.36, .42 + .02 * max(F.smile, 0), -.46, .415 + .02 * max(F.smile, 0), -.57 + .03 * max(F.smile, 0) - .05 * F.mouth)], .012, L, .35 + .35 * max(F.smile, F.teeth, 0))
        if k['old']: P.line([(.50, -.32), (.53, -.42, .52, -.52, .49, -.60)], .011, L, .5 * k['old'])
        if F.frown > .4 or F.teeth > .4: [P.line([(.03, .02 - .055 * i), (.05, .03 - .055 * i, .07, .03 - .055 * i, .09, .01 - .055 * i)], .010, L, .5) for i in range(3)]
        for x, y in ((.20, -.47), (.265, -.50), (.235, -.425), (.31, -.455)): P.col(L, .55); c.arc(x, y, .011, 0, 7); c.fill()
        c.restore()
    P.line([(-.035, -.38), (-.02, -.42, -.004, -.44, 0, -.535)], .011, L, .55); P.line([(.035, -.38), (.02, -.42, .004, -.44, 0, -.535)], .011, L, .55)


def vmouth(P, F, k):
    c = P.c; s = F.smile; w = k['mouthw']; o = F.mouth * .30; L = k['line']; cy = -.655 + .085 * s - .04 * F.sad; y0 = -.632
    if o < .012 and F.teeth < .2:
        line = [(-.385 * w, cy + .02), (-.28 * w, y0 - .035 - .02 * s, -.13 * w, y0 + .014, 0, y0 - .012), (.13 * w, y0 + .014, .28 * w, y0 - .035 - .02 * s, .385 * w, cy + .02)]
        P.fill([(-.36 * w, cy + .014), (-.24 * w, y0 + .006, -.10 * w, y0 + .046, 0, y0 + .026), (.10 * w, y0 + .046, .24 * w, y0 + .006, .36 * w, cy + .014), (.28 * w, y0 - .035 - .02 * s, .13 * w, y0 + .014, 0, y0 - .012), (-.13 * w, y0 + .014, -.28 * w, y0 - .035 - .02 * s, -.36 * w, cy + .014)], k['lip'])
        P.fill([(-.31 * w, cy - .006), (-.24 * w, y0 - .03 - .02 * s, -.13 * w, y0 + .008, 0, y0 - .016), (.13 * w, y0 + .008, .24 * w, y0 - .03 - .02 * s, .31 * w, cy - .006), (.21 * w, y0 - .088, .11 * w, y0 - .108, 0, y0 - .108), (-.11 * w, y0 - .108, -.21 * w, y0 - .088, -.31 * w, cy - .006)], k['lip2'])
        P.col(k['liphi'], .30); c.save(); c.translate(-.02, y0 - .062); c.scale(.10 * w, .015); c.arc(0, 0, 1, 0, 7); c.restore(); c.fill()
        P.line(line, .020, '#2a0610')
        for sd in (1, -1): c.save(); c.scale(sd, 1); P.line([(.385 * w, cy + .055), (.415 * w, cy + .035, .415 * w, cy - .005, .385 * w, cy - .025)], .013, L, .7); c.restore()
        P.line([(-.13, y0 - .185), (-.06, y0 - .20, .06, y0 - .20, .13, y0 - .185)], .011, L, .4)
    else:
        bot = y0 - .05 - o; g = .40 * w - .04 * F.mouth * (s < .3)
        outer = [(-g - .015, cy), (-.26 * w, y0 + .015, -.11 * w, y0 + .055, 0, y0 + .030), (.11 * w, y0 + .055, .26 * w, y0 + .015, g + .015, cy), (g * .95, bot - .02, .20 * w, bot - .100, 0, bot - .100), (-.20 * w, bot - .100, -g * .95, bot - .02, -g - .015, cy)]
        P.fill(outer, k['lip2'])
        inner = [(-g + .025, cy - .008), (-.22 * w, y0 - .030, -.09 * w, y0 - .006, 0, y0 - .020), (.09 * w, y0 - .006, .22 * w, y0 - .030, g - .025, cy - .008), (g * .86, bot + .015, .17 * w, bot - .030, 0, bot - .030), (-.17 * w, bot - .030, -g * .86, bot + .015, -g + .025, cy - .008)]
        P.fill(inner, k['mouthin']); c.save(); P.path(inner, True); c.clip()
        if o > .06 and F.teeth < .8: P.col('#c2515a'); c.save(); c.translate(0, bot + .01); c.scale(.20 * w, .085); c.arc(0, 0, 1, 0, 7); c.restore(); c.fill(); P.line([(0, bot + .08), (0, bot - .04)], .010, '#8a2a3a', .8)
        if F.teeth > .05 or o > .05:
            d = .035 + .035 * F.teeth
            P.fill([(-g, y0 + .03), (g, y0 + .03), (g * .9, y0 - .05 - d * .4, .10 * w, y0 - .025 - d, 0, y0 - .025 - d), (-.10 * w, y0 - .025 - d, -g * .9, y0 - .05 - d * .4, -g, y0 + .03)], '#fdf4e0')
            [P.line([(x * w, y0 + .02), (x * w, y0 - .03 - d)], .006, '#8a5a4a', .55) for x in np.linspace(-.24, .24, 9)]
            if F.teeth > .4:
                for sd in (1, -1): P.fill([(sd * .235 * w, y0), (sd * .31 * w, y0), (sd * .275 * w, y0 - .095 - .09 * F.teeth)], '#fff8e6')
            if F.teeth > .5: P.fill([(-.3 * w, bot - .08), (.3 * w, bot - .08), (.24 * w, bot + .045), (-.24 * w, bot + .045)], '#f3e6cc'); [P.line([(x * w, bot + .04), (x * w, bot - .05)], .006, '#8a5a4a', .55) for x in np.linspace(-.18, .18, 7)]
        c.restore(); P.path(outer, True); P.col('#2a0610'); c.set_line_width(.014); c.stroke(); P.path(inner, True); c.set_line_width(.011); c.stroke()
        P.line([(-.16, bot - .16), (-.07, bot - .175, .07, bot - .175, .16, bot - .16)], .012, L, .4)


def face(F): return vface(F)


HANUMAN = Fig('hanuman', 'hanuman.glsl', PAL, dim=DIM, build=BUILD, hs=HS, face=face, bound=(0, 8, 0, 11.5), step=.80)
HANUMAN_CU = HANUMAN.variant(face=lambda F: vface(F, S=2304))      # the same figure with a finer painted face, for eyes that fill the frame

# ------------------------------------------------------------------ poses (figure units; they suit any figure with DIM's proportions)
GY = .93                                     # ankle height of a planted foot
H_STAND = Pose(pel=(0, 7.42, 0), cher=(0, -3, 0), hedr=(0, 3, 0), lf=(1.15, GY, .1), rf=(-1.15, GY, .3), lft=(18, 0), rft=(-18, 0), lh=(3.5, 6.7, .9), rh=(-3.5, 6.7, .9), lel=(1, 0, -.7), rel=(-1, 0, -.7), lhand='relax', rhand='relax', lkn=(.25, 0, 1), rkn=(-.25, 0, 1))
H_ANJALI = H_STAND.set(cher=(0, 4, 0), hedr=(0, 12, 0), lh=(.34, 8.7, 2.75), rh=(-.34, 8.7, 2.75), lhand='anjali', rhand='anjali', lfing=(-.06, 1, .22), rfing=(.06, 1, .22), lpalm=(-1, 0, 0), rpalm=(1, 0, 0), lel=(1, -.55, -.1), rel=(-1, -.55, -.1))
_KN = Pose(pel=(0, 4.15, 0), pelr=(0, 6, 0), lf=(1.1, GY, 2.5), rf=(-.95, .80, -3.0), lkn=(.35, .4, 1), rkn=(-.25, -.5, 1), lft=(12, 0), rft=(-4, 62))
H_BOW = _KN.set(cher=(0, 26, 0), hedr=(0, 24, 0), lh=(.34, 6.5, 3.9), rh=(-.34, 6.5, 3.9), lhand='anjali', rhand='anjali', lfing=(-.06, .92, .5), rfing=(.06, .92, .5), lpalm=(-1, 0, 0), rpalm=(1, 0, 0), lel=(1, -.5, 0), rel=(-1, -.5, 0))
H_KNEEL_PALM = _KN.set(cher=(0, 16, 0), hedr=(0, 24, 0), lh=(.62, 6.4, 4.7), rh=(-.62, 6.4, 4.7), lhand='cup', rhand='cup', lfing=(-.16, .10, 1), rfing=(.16, .10, 1), lpalm=(-.30, 1, -.1), rpalm=(.30, 1, -.1), lel=(1, -.7, -.2), rel=(-1, -.7, -.2))
H_CROUCH = Pose(pel=(0, 3.0, -1.5), pelr=(0, 34, 0), cher=(0, 26, 0), hedr=(0, -46, 0), lf=(1.9, GY, -.9), rf=(-1.9, GY, -.9), lkn=(.75, .5, 1), rkn=(-.75, .5, 1), lft=(30, 14), rft=(-30, 14), lh=(2.7, 1.42, 3.4), rh=(-2.7, 1.42, 3.4), lel=(1, .3, -.5), rel=(-1, .3, -.5), lhand='fist', rhand='fist', lfing=(0, -1, .12), rfing=(0, -1, .12), lpalm=(0, -.1, -1), rpalm=(0, -.1, -1), shrug=(.5, .5))
H_LEAP = Pose(pel=(0, 9.0, 0), pelr=(0, 4, 0), cher=(14, -14, -6), hedr=(-8, -16, 0), rh=(-2.1, 18.6, 1.2), lh=(4.6, 9.6, -2.2), rel=(-1, 0, -.4), lel=(.6, .2, -1), rhand='fist', lhand='fist', rfing=(.05, 1, .1), rpalm=(.2, 0, 1), lfing=(.4, -.7, -.6), lpalm=(-.3, .2, 1), lf=(1.0, 6.0, 1.0), rf=(-.9, 2.3, -1.5), lkn=(.25, .4, 1), rkn=(-.1, 0, 1), lft=(8, 46), rft=(-6, 74))
H_FLY = Pose(pel=(0, 8.0, 0), pelr=(8, 62, 0), cher=(8, -14, 4), hedr=(-12, -46, 0), rh=(-1.9, 12.0, 8.7), lh=(4.6, 8.0, -.4), rel=(-.7, -.6, .3), lel=(.7, .6, -.3), rhand='open', lhand='fist', rfing=(.02, .30, 1), rpalm=(.1, -1, .30), lfing=(.1, -.2, -1), lpalm=(-.3, 1, 0), lf=(.9, 5.9, -6.4), rf=(-1.15, 4.1, -1.5), lkn=(.1, 0, 1), rkn=(-.3, .5, 1), lft=(0, 126), rft=(0, 108))
H_FLY2 = Pose(pel=(0, 8.0, 0), pelr=(0, 100, 0), cher=(0, -14, 0), hedr=(0, -60, 0), lh=(5.0, 9.4, -.9), rh=(-5.0, 9.4, -.9), lel=(.8, .7, 0), rel=(-.8, .7, 0), lhand='flat', rhand='flat', lfing=(.25, .3, -1), rfing=(-.25, .3, -1), lpalm=(.1, -1, -.3), rpalm=(-.1, -1, -.3), lf=(.75, 9.6, -6.2), rf=(-.75, 8.0, -5.6), lft=(0, 152), rft=(0, 134), lkn=(.1, 0, 1), rkn=(-.1, 0, 1))
H_CARRY = Pose(pel=(0, 8.0, 0), pelr=(-10, 44, 0), cher=(-8, -20, -14), hedr=(4, -20, 12), shrug=(1.4, 0), lh=(2.9, 17.6, 3.9), rh=(-4.0, 7.2, -.8), lel=(1, 0, -.6), rel=(-.8, .3, -.4), lhand='flat', rhand='fist', lfing=(.55, .18, -.8), lpalm=(0, 1, .1), rfing=(-.3, -.5, -.9), rpalm=(.4, 1, -.2), lf=(1.1, 4.6, -1.6), rf=(-.9, 4.4, -5.4), lkn=(.25, 0, 1), rkn=(-.1, 0, 1), lft=(0, 96), rft=(0, 118))
H_LAND = Pose(pel=(0, 3.5, -.6), pelr=(-8, 30, 0), cher=(-12, 26, 0), hedr=(10, -12, 0), lf=(2.0, GY, 1.5), rf=(-1.5, .95, -3.2), lkn=(.7, .5, 1), rkn=(-.6, -.25, 1), lft=(24, 0), rft=(-12, 56), rh=(-1.5, 1.42, 3.9), lh=(5.6, 6.6, -1.6), rel=(-1, .3, -.4), lel=(.2, .8, -1), rhand='fist', lhand='open', rfing=(0, -1, .1), rpalm=(.2, 0, -1), lfing=(.8, .35, -.5), lpalm=(0, -.9, -.2), shrug=(.2, .4))
H_PERCH = Pose(pel=(0, 2.75, -.8), pelr=(0, 26, 0), cher=(6, 18, 0), hedr=(-8, -22, 0), lf=(1.25, GY, .3), rf=(-1.25, GY, .3), lkn=(.8, .5, 1), rkn=(-.8, .5, 1), lft=(26, 4), rft=(-26, 4), rh=(-.8, 1.40, 2.9), lh=(2.7, 4.2, 2.6), rel=(-1, .4, -.2), lel=(1, .2, -.5), rhand='fist', lhand='relax', rfing=(.1, -1, .15), rpalm=(.5, 0, -1), lfing=(-.4, -.5, .8), lpalm=(-.3, -1, -.2))
H_BOUND = Pose(pel=(0, 2.9, -.7), pelr=(0, 4, 0), cher=(0, 10, 0), hedr=(0, 30, 0), lf=(.95, .75, -1.6), rf=(-.95, .75, -1.6), lkn=(.32, -.3, 1), rkn=(-.32, -.3, 1), lft=(-6, 84), rft=(6, 84), lh=(.48, 4.35, -2.05), rh=(-.48, 4.35, -2.05), lel=(1, -.1, -.6), rel=(-1, -.1, -.6), lhand='fist', rhand='fist', lfing=(-.45, -.8, -.1), rfing=(.45, -.8, -.1), lpalm=(0, .1, -1), rpalm=(0, .1, -1), shrug=(.25, .25))
H_ROAR = Pose(pel=(0, 6.9, 0), pelr=(0, -4, 0), cher=(0, -14, 0), hedr=(0, -14, 0), lf=(2.1, GY, .6), rf=(-2.1, GY, -.1), lkn=(.6, 0, 1), rkn=(-.6, 0, 1), lft=(30, 0), rft=(-30, 0), lh=(6.4, 11.4, 1.4), rh=(-6.4, 11.4, 1.4), lel=(.3, -1, -.5), rel=(-.3, -1, -.5), lhand='claw', rhand='claw', lfing=(.45, 1, .2), rfing=(-.45, 1, .2), lpalm=(-.5, .1, 1), rpalm=(.5, .1, 1), shrug=(.3, .3))


def mirror(p):
    """the same pose with left and right exchanged"""
    f = lambda q: None if q is None else (-q[0], q[1], q[2]); g = lambda q: (-q[0], q[1], -q[2])
    return Pose(pel=f(p.pel), pelr=g(p.pelr), cher=g(p.cher), hedr=g(p.hedr), lh=f(p.rh), rh=f(p.lh), lel=f(p.rel), rel=f(p.lel), lhand=p.rhand, rhand=p.lhand, lfing=f(p.rfing), rfing=f(p.lfing), lpalm=f(p.rpalm), rpalm=f(p.lpalm), lf=f(p.rf), rf=f(p.lf), lkn=f(p.rkn), rkn=f(p.lkn), lft=(-p.rft[0], p.rft[1]), rft=(-p.lft[0], p.lft[1]), shrug=(p.shrug[1], p.shrug[0]))


H_FLY_L = mirror(H_FLY)                      # left arm forward: flying toward screen right (yaw 90) it leaves the face clear


def H_WALK(ph, stride=1.75, lift=1.0):
    """walk cycle, ph in 0..1, toward +z"""
    a = 2 * math.pi * ph; c, s = math.cos(a), math.sin(a)

    def foot(p):
        p %= 1.
        if p < .5: return stride * (1 - 4 * p), 0., (-14 * (1 - p / .1) if p < .1 else (34 * ((p - .35) / .15) if p > .35 else 0))
        q = (p - .5) / .5; return -stride + 2 * stride * (q * q * (3 - 2 * q)), lift * math.sin(math.pi * q), (34 * (1 - q * 2) if q < .5 else -14 * (q - .5) * 2)
    lz, ly, lp = foot(ph); rz, ry, rp = foot(ph + .5)
    return Pose(pel=(0, 7.25 - .22 * abs(c), 0), pelr=(9 * c, 4, 2 * s), cher=(-16 * c, 0, -2 * s), hedr=(7 * c, 0, 0), lf=(.95, GY + ly, lz), rf=(-.95, GY + ry, rz), lft=(12, lp), rft=(-12, rp), lh=(3.4, 6.9 + .25 * abs(c), .6 - 1.6 * c), rh=(-3.4, 6.9 + .25 * abs(c), .6 + 1.6 * c), lel=(.8, 0, -1), rel=(-.8, 0, -1), lkn=(.2, 0, 1), rkn=(-.2, 0, 1))


def H_RUN(ph, stride=3.3, lift=2.4, lean=26):
    """a bounding run, ph in 0..1, toward +z"""
    a = 2 * math.pi * ph; c = math.cos(a)

    def foot(p):
        p %= 1.
        if p < .36: q = p / .36; return stride * .75 * (1 - 2 * q) - .3, 0., 34 * q
        q = (p - .36) / .64; return -stride * .75 - .3 + 1.5 * stride * (q * q * (3 - 2 * q)), lift * math.sin(math.pi * q) ** .8, 66 * (1 - q)
    lz, ly, lp = foot(ph); rz, ry, rp = foot(ph + .5)
    return Pose(pel=(0, 6.85 + .5 * math.sin(2 * a + .6), 0), pelr=(13 * c, lean * .6, 0), cher=(-28 * c, lean * .5, 0), hedr=(13 * c, -lean * .75, 0), lf=(.75, GY + ly, lz), rf=(-.75, GY + ry, rz), lft=(6, lp), rft=(-6, rp), lh=(3.0, 8.4 - .9 * c, 1.9 - 2.9 * c), rh=(-3.0, 8.4 + .9 * c, 1.9 + 2.9 * c), lel=(.8, -.3, -1), rel=(-.8, -.3, -1), lhand='fist', rhand='fist', lkn=(.2, 0, 1), rkn=(-.2, 0, 1))


def _club(d, palm):
    """finger and palm directions of the right hand that make a held shaft point along d"""
    d = nz(d); z = np.asarray(palm, float); z = nz(z - d * (z @ d)); return dict(rfing=tuple(np.cross(z, d)), rpalm=tuple(z), rhand='grip')


_SW = [Pose(pel=(-.3, 6.9, -.3), pelr=(-34, 0, 0), cher=(-34, -6, 6), hedr=(52, 4, 0), rh=(-3.6, 13.2, -2.0), lh=(1.6, 11.2, 3.2), lf=(1.5, GY, 1.9), rf=(-1.9, GY, -1.5), lft=(10, 0), rft=(-50, 0), rel=(-1, .2, -.3), lel=(.9, -.5, .3), lhand='open', lfing=(-.3, .6, .8), lpalm=(-.6, -.2, .7), lkn=(.3, 0, 1), rkn=(-.8, 0, .6), **_club((.35, .35, -.9), (.9, .1, .5))),
       Pose(pel=(.1, 6.7, .5), pelr=(8, 8, 0), cher=(16, 12, -4), hedr=(-20, -8, 0), rh=(-2.2, 11.6, 5.0), lh=(4.2, 8.4, -.6), lf=(1.5, GY, 2.6), rf=(-1.8, GY + .1, -1.9), lft=(10, 0), rft=(-40, 18), rel=(-1, -.2, .2), lel=(.8, 0, -1), lhand='fist', lkn=(.3, 0, 1), rkn=(-.5, 0, .9), **_club((.15, .55, .85), (1, -.1, 0))),
       Pose(pel=(.3, 6.2, 1.0), pelr=(26, 16, 0), cher=(28, 20, -6), hedr=(-36, -22, 0), rh=(1.6, 6.6, 6.0), lh=(4.8, 8.4, -1.6), lf=(1.6, GY, 3.0), rf=(-1.8, GY + .3, -2.4), lft=(10, 0), rft=(-30, 34), rel=(-.8, .6, .3), lel=(.6, .3, -1), lhand='fist', lkn=(.4, 0, 1), rkn=(-.4, 0, 1), **_club((.85, -.25, .55), (.2, -.4, -.9)))]


def H_SWING(t):
    """gada swing, t 0 wound up over the right shoulder, .5 strike, 1 followed through across the body"""
    t = max(0., min(1., t)); return _SW[0].mix(_SW[1], t * 2) if t < .5 else _SW[1].mix(_SW[2], t * 2 - 1)


def fit(p, dim=DIM):
    """a lau.poses pose made for the human proportions, brought to these (shorter legs, wider shoulders)"""
    k = (dim['th'] + dim['sh'] + GY) / 8.05; d = {}
    f = lambda q: None if q is None else (q[0] * 1.25, GY + (q[1] - .75) * k, q[2])
    h = lambda q: None if q is None else (q[0] * 1.25, q[1] * k, q[2] * 1.1)
    return p.set(pel=(p.pel[0], p.pel[1] * k + .02, p.pel[2]), lf=f(p.lf), rf=f(p.rf), lh=h(p.lh), rh=h(p.rh))


# ------------------------------------------------------------------ tail, sash, gada
_TAIL = """#include "noise.glsl"
in vec3 vp,vn_;in vec2 vuv;
layout(location=0) out vec4 g0;layout(location=1) out vec4 g1;layout(location=2) out vec4 g2;layout(location=3) out vec4 g3;
uniform vec3 ro;uniform mat3 CamR;uniform float far,objId,cls,inkw,part,fT,Lr;uniform int kind;uniform vec3 cA,cB,cC;
void main(){
  vec3 n=normalize(vn_),v=vp-ro;if(dot(n,v)>0.) n=-n;vec3 f=transpose(CamR)[2];float vz=dot(v,f);gl_FragDepth=clamp(vz/far,0.,1.);
  vec3 b=cA,s=cB,ns=n;float ik=inkw;vec2 u=vuv;
  vec3 T=dFdx(vp)*dFdy(u.y)-dFdy(vp)*dFdx(u.y);float dt=dFdx(u.x)*dFdy(u.y)-dFdy(u.x)*dFdx(u.y);T=normalize(T*sign(dt)+1e-5);
  if(kind==0||kind==2){
    float ink=0.,tl=0.;for(int L=0;L<2;L++){float nc=kind==0?10.:7.;vec2 g=vec2(u.y*nc,u.x*Lr*(kind==0?1.9:1.2));for(int i=-1;i<=1;i++){float c=floor(g.x)+float(i);float cm=mod(c,nc)+float(L)*31.;float y=g.y+h11(cm*1.7)*7.;float r=floor(y);float h=h21(vec2(cm,r));float q=fract(y);float x=g.x-c-.5+(h-.5)*.7+(fract(h*7.)-.5)*.5*q;float tp=min(q*6.,1.)*(1.-q);ink=max(ink,(1.-smoothstep(.04*tp,.10*tp+.01,abs(x)))*step(.25,fract(h*5.)));tl+=(fract(h*3.7)-.5)*(1.-smoothstep(.1,.5*(1.-q)+.1,abs(x)));}}
    b=mix(b,s*1.35,ink*.65);s=mix(s,s*.5,ink*.8);ns=normalize(n+T*tl*.45);
    b=mix(b,cC,kind==0?smoothstep(.72,.97,u.x+.05*sin(u.y*44.)):0.);}
  else{float w=u.x*Lr*1.15+u.y*1.0;float q=fract(w),k=floor(w);b=mix(cA,cA*vec3(.86,.82,.74),h11(k)*.7);s=mix(cB,cB*.8,h11(k+9.));float e=smoothstep(.07,.0,q)+smoothstep(.95,1.,q)*.6;b=mix(b,cB*.55,e*.9);s=mix(s,cB*.3,e*.9);
    float th=smoothstep(.75,.95,vn(vec2(u.x*Lr*16.,u.y*9.)));b=mix(b,cC,th*.5);float st=smoothstep(.52,.60,fbm(vec2(u.x*Lr*.9,u.y*4.)));b=mix(b,cC,st*.55);}
  g0=vec4(n,vz);g1=vec4(b,cls+clamp(ik,0.,.98)*.98);g2=vec4(s,1);g3=vec4(ns,objId*64.+part);
}
"""


def _join(M):
    P, N, U, I, k = [], [], [], [], 0
    for p, n, u, i in M: P.append(p); N.append(n); U.append(u); I.append(i + k); k += len(p)
    return np.vstack(P), np.vstack(N), np.vstack(U), np.vstack(I)


def _key(u, K):
    """smooth interpolation through (u, value) keys"""
    x = np.array([a for a, _ in K], float); y = np.array([b for _, b in K], float); m = np.gradient(y, x); i = np.clip(np.searchsorted(x, u, 'right') - 1, 0, len(x) - 2); h = x[i + 1] - x[i]; t = (u - x[i]) / h
    return (2 * t ** 3 - 3 * t ** 2 + 1) * y[i] + (t ** 3 - 2 * t ** 2 + t) * h * m[i] + (-2 * t ** 3 + 3 * t ** 2) * y[i + 1] + (t ** 3 - t ** 2) * h * m[i + 1]


_ELEV = dict(calm=[(0, -38), (.14, -46), (.30, -2), (.46, 52), (.62, 84), (.76, 104), (.88, 92), (1, 20)], up=[(0, 0), (.14, 34), (.30, 70), (.48, 90), (.62, 108), (.76, 124), (.88, 104), (1, 30)],
             fly=[(0, 8), (.3, 4), (.7, 10), (.86, 46), (1, 132)], whip=[(0, -8), (.3, 22), (.6, 44), (.8, 40), (1, 90)])


def tail_curve(S, t, style='calm', length=13., seed=0, path=None, vel=(0, 0, 0), ground=None, n=72):
    """the tail's centre line in world space (n,3), root to tip.  path(t) = world displacement of the figure over time, or vel = its world velocity (units/s): either makes the tail lag behind"""
    sc = S.Sc; u = np.linspace(0, 1, n); pel = lambda v: S.d(np.asarray(v, float) @ S.u['Bp']); root = S.pelvis((0, .02, -.74)); out = pel((0, -.10, -1)); w = seed * 1.7
    if style == 'fly': bk = nz(S.joint(0) - S.joint(1)); fu = S.d((0, 1, .25)); up = nz(fu - bk * (fu @ bk))
    else: bk, up = S.d((0, 0, -1)), S.d((0, 1, 0))
    lf = nz(np.cross(up, bk)); lf = lf if lf @ S.d((1, 0, 0)) > 0 else -lf
    e = _key(u, _ELEV[style]); a = np.zeros(n)
    if style in ('calm', 'up'): e = e + 7 * u * np.sin(1.9 * t - 4.2 * u + w) * (1.2 if style == 'up' else 1.); a = 20 * u ** .8 * np.sin(1.45 * t - 3.4 * u + w) + 24 * np.sin(u * 3.3 + w * .6 + .4) * u
    elif style == 'fly': e = e + 24 * np.minimum(1, u * 2.2) * np.sin(7.5 * u - 6.4 * t + w); a = 20 * np.minimum(1, u * 2) * np.sin(6.2 * u - 5.1 * t + 1.3 + w)
    else: g = np.minimum(1, u * 2.6); e = e + 46 * g * np.sin(8.6 * u - 9.5 * t + w); a = 62 * g * np.sin(7.4 * u - 8.3 * t + w * 1.3)
    e, a = np.radians(e), np.radians(a); D = (np.cos(e) * np.cos(a))[:, None] * bk + (np.sin(e))[:, None] * up + (np.cos(e) * np.sin(a))[:, None] * lf
    k = np.clip(1 - u / .16, 0, 1)[:, None] ** 2; D = D * (1 - k) + out * k; D /= np.linalg.norm(D, axis=1, keepdims=True); ds = length * sc / (n - 1)
    P = root + np.vstack([np.zeros(3), np.cumsum((D[1:] + D[:-1]) / 2 * ds, axis=0)])
    if path is not None: o = np.asarray(path(t), float); P = P + np.array([np.asarray(path(t - .42 * q ** 1.2), float) - o for q in u])
    else: P = P - np.asarray(vel, float)[None] * (.16 * u ** 1.3)[:, None]
    if path is not None or np.any(vel):                  # keep its length
        d = np.diff(P, axis=0); d = d / (np.linalg.norm(d, axis=1, keepdims=True) + 1e-9) * ds; P = np.vstack([P[0], P[0] + np.cumsum(d, axis=0)])
    if ground is not None: g = ground + .34 * sc; h = P[:, 1] - g; P[:, 1] = g + .5 * (h + np.sqrt(h * h + (.30 * sc) ** 2)) * (1 - k[:, 0]) + h * k[:, 0]
    return P


def tail(st, S, t, style='calm', length=13., wrap=0, seed=0, path=None, vel=(0, 0, 0), ground='auto', r=.30, draw=True, col=FUR, tuft=DARK):
    """draw the tail of the solved figure S (between open and close) and return its centre line (72,3) in world space, root to tip.
    style calm | up | fly | whip; wrap=1 winds it in pale oiled cloth.  ground: a world height it may not sink under ('auto' = the figure's origin for calm, up and whip; None = free)"""
    if ground == 'auto': ground = float(S.w((0, 0, 0))[1]) if style != 'fly' and abs(S.Mf[1, 1]) > .8 * S.Sc else None
    P = tail_curve(S, t, style, length, seed, path, vel, ground); sc = S.Sc
    if not draw: return P
    Lr = length / .9; u = np.linspace(0, 1, len(P))
    if wrap:
        Q = CL.spline(P, 260); v = np.linspace(0, 1, 260); R = np.interp(v, [0, .06, .12, .55, .93, .985, 1], [r * .95, r, r * 1.45, r * 1.30, r * 1.35, r * .9, .02]) * (1 + .085 * np.abs(np.sin(v * Lr * 1.15 * math.pi)) - .03)
        st.mesh(*CL.tube(Q, R * sc, m=18), kind=1, col=('#efe0bd', '#8a7064', '#c79a54'), cls=1, ink=.85, frag=_TAIL, u=dict(Lr=Lr), part=3.)
        return P
    Q = CL.spline(P, 150); R = np.interp(np.linspace(0, 1, 150), [0, .05, .4, .8, .93, 1], [r * 1.25, r * 1.08, r * .90, r * .80, r * .85, r * .35])
    st.mesh(*CL.tube(Q, R * sc, m=16), kind=0, col=(col[0], col[1], tuft[0]), cls=1, ink=.85, frag=_TAIL, u=dict(Lr=Lr), part=3.)
    # the tuft: locks that leave the last part of the tail, swell and close to a point like a brush
    i0 = int(len(P) * .895); base = P[i0:]; T = np.gradient(P, axis=0); T /= np.linalg.norm(T, axis=1, keepdims=True); end = P[-1]; te = T[-1]; a = nz(np.cross(te, S.d((.3, .9, .2)))); b = np.cross(te, a); M = []; Lf = 1.55 * sc * (r / .30)
    M.append(CL.tube(CL.spline(np.vstack([base, end + te * Lf * .55, end + te * Lf * 1.05]), 30), np.array([.6, .95, 1.5, 1.7, 1.25, .55, .03]) * r * sc, m=12))
    for j in range(13):
        q = j / 13 * 6.2832 + (j % 2) * .25; dr = a * math.cos(q) + b * math.sin(q); k = .75 + .30 * ((j * 5) % 7) / 6; m = int((j % 3) * len(base) // 5)
        p0 = base[m] + dr * r * .30 * sc; tm = T[i0 + m]; p1 = p0 * .25 + (base[-1] if m < len(base) - 1 else p0) * .75 + dr * r * 1.05 * sc; p2 = end + te * Lf * .42 * k + dr * r * (1.30 - .25 * k) * sc; p3 = end + te * Lf * k + dr * r * .55 * sc + a * math.sin(t * 2.3 + j) * .05 * sc
        M.append(CL.tube(CL.spline(np.array([p0, p1, p2, p3]), 16), np.array([.35, .62, .55, .02]) * r * sc, m=7))
    st.mesh(*_join(M), kind=2, col=(tuft[0], tuft[1], col[0]), cls=1, ink=.8, frag=_TAIL, u=dict(Lr=6.), part=4.)
    return P


def sash(st, S, t, length=4.6, wind=(0, 0, 0), vel=(0, 0, 0), col=('#c4222c', '#660f22', '#f2b23a')):
    """two ends of the waist sash hanging (or streaming, with wind or the figure's world velocity vel) from his left hip"""
    sc = S.Sc; a0 = S.pelvis((.98, .42, .30)); v = np.asarray(vel, float); w = np.asarray(wind, float) - v * .05; g = .95 / (1 + float(np.linalg.norm(w)) * 1.2)
    for k, (dx, ph) in enumerate(((0., 0.), (.12, 1.4))):
        P = CL.lag(lambda q: a0 + v * (q - t) * .35, t, 14, (length - .9 * k) * sc, delay=.03, wind=w, grav=g, wave=.30, freq=1.1, phase=ph + k, dirn=S.d(S.u['Bp'].T @ V(.28 + dx, -.1, .12 - .3 * k)) * .5)
        st.mesh(*CL.strip(P, np.array([.30, .52, .62, .66]) * sc, up=S.d((1, .1, .5 - .9 * k)), n=40, curl=.18), kind=1, col=col, cls=8, ink=.85, part=5.)


def gada(st, S, side='R', scale=1., flip=False):
    """put PR.GADA in the hand; returns the world position of its head"""
    from lau import props as PR
    y = S.hand(side, (1, 0, 0)) * (-1 if flip else 1); o = S.palm(side, 0, .62, .34) - y * .55 * S.Sc * scale; st.fig(PR.GADA, M=PR.place(o, y, S.hand(side, (0, 0, 1)), S.Sc * scale)); return o + y * 5.6 * S.Sc * scale


def tail_fire(st, P, t, a=0., b=1., k=1., scale=1., seed=0):
    """after close(): set the part a..b (0 root, 1 tip) of a tail curve alight; k = strength, scale = the figure's scale"""
    from lau import fx as FX
    n = len(P); Q = CL.spline(P, 160)[int(a * 159):max(int(a * 159) + 4, int(b * 159) + 1)]; m = len(Q); r = np.random.default_rng(seed); s = scale * k; u = np.linspace(0, 1, m)
    up = np.array((0, 1., 0)); N = int(150 * k * (b - a)) + 12; q = r.uniform(0, 1, N); ph = r.uniform(0, 1, N); lf = (t * r.uniform(1.6, 2.8, N) + ph) % 1.; B = Q[(q * (m - 1)).astype(int)]; w = .55 + .75 * q
    FX.ribbon(st, Q + up * .30 * s, np.interp(u, [0, .12, .8, 1], [.12, .75, 1.05, .5]) * s, mode='fire', amt=1.1, seed=seed, blend='add')
    R = B + up * (lf * 1.9 * w * s)[:, None] + np.c_[np.sin(ph * 40 + t * 5), np.zeros(N), np.cos(ph * 31 + t * 4)] * (.22 * s * lf)[:, None]
    FX.particles(st, R, .95 * s * w * (1 - .65 * lf), '#ff9a3a', 'tongue', seed=ph, alpha=np.minimum(1, lf * 6) * (1 - lf) ** .8, blend='add')
    g = r.uniform(0, 1, N // 2); l2 = (t * .9 * (.6 + g) + g * 7) % 1.; E = Q[(r.uniform(0, 1, N // 2) * (m - 1)).astype(int)] + up * (l2 * 5.5 * s)[:, None] + np.c_[np.sin(g * 50 + t * 3), np.zeros(N // 2), np.cos(g * 37 + t * 2.4)] * (1.1 * s * l2)[:, None]
    FX.particles(st, E, .085 * s * (1 - l2) ** .5, '#ffc060', 'ember', seed=g, alpha=(1 - l2) ** .7)
