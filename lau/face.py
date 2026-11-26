"""Painted faces: a decal drawn flat from the front (head units: x right, y up) that the head shader projects onto the skull."""
import cairo, numpy as np, math
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Face:
    """expression.  lid 1 open 0 shut; gaze -1..1; brow + up / - down; frown 0..1 (inner ends down, angry); sad 0..1 (inner ends up); smile -1..1; mouth 0..1 open; teeth; tear 0..1"""
    lid: float = 1.; gx: float = 0.; gy: float = 0.; brow: float = 0.; frown: float = 0.; sad: float = 0.; smile: float = .25; mouth: float = 0.; teeth: float = 0.; tear: float = 0.
    squint: float = 0.; pupil: float = 1.; glow: float = 0.; spark: float = 0.

    def mix(s, o, t):
        return Face(**{k: round((1 - t) * getattr(s, k) + t * getattr(o, k), 3) for k in s.__dataclass_fields__})

    def set(s, **k): return replace(s, **k)


def rgb(h): h = h.lstrip('#'); return [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]


INK = '#150a14'


class Pen:
    def __init__(s, S, box):
        s.sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, S, S); s.S = S; c = s.c = cairo.Context(s.sf); x0, y0, x1, y1 = box
        c.scale(S / (x1 - x0), -S / (y1 - y0)); c.translate(-x0, -y1); c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND)

    def col(s, h, a=1.): r, g, b = rgb(h); s.c.set_source_rgba(r, g, b, a)

    def path(s, pts, close=False):
        """pts: start point then 6-tuples (curve) or 2-tuples (line)"""
        c = s.c; c.move_to(*pts[0])
        for p in pts[1:]: c.curve_to(*p) if len(p) == 6 else c.line_to(*p)
        if close: c.close_path()

    def fill(s, pts, col, a=1.): s.path(pts, True); s.col(col, a); s.c.fill()

    def line(s, pts, w, col=INK, a=1.): s.path(pts); s.col(col, a); s.c.set_line_width(w); s.c.stroke()

    def out(s): s.sf.flush(); return np.ndarray((s.S, s.S, 4), np.uint8, s.sf.get_data()).copy()


DEF = dict(iris='#7a3a16', iris2='#3a1608', sclera='#fbf3e4', lip='#9c3f5c', lip2='#b8506a', liphi='#f2a8a8', kohl='#1a0c22', kohlk=1., brow=INK, browt=1., browy=0., tilak='U', size=1., lash=0., nose='#1a1830', mouthy=0., mouthw=1., skinsh='#1c2c58',
           blush=None, lidcol='#4f7fb0', eyex=.0, tilt=0.)


def human(F, st=None, box=(-1.1, -1.25, 1.1, .95), S=1024, extra=None, under=None):
    """F: Face, st: style overrides of DEF; extra(pen, F, st) draws on top (moustache, paint), under(...) below"""
    k = {**DEF, **(st or {})}; P = Pen(S, box); c = P.c; kh = k['kohlk']
    if under: under(P, F, k)
    if k['blush']:
        for sd in (1, -1):
            g = cairo.RadialGradient(sd * .42, -.30, .02, sd * .42, -.30, .26); r = rgb(k['blush']); g.add_color_stop_rgba(0, *r, .45); g.add_color_stop_rgba(1, *r, 0); c.set_source(g); c.arc(sd * .42, -.30, .26, 0, 7); c.fill()
    up = -.035 + .20 * F.lid; lo = -.062 + .03 * max(F.smile, 0) + .05 * F.squint
    for sd in (1, -1):
        c.save(); c.scale(sd, 1); c.translate(k['eyex'], 0); c.translate(.33, .03); c.scale(k['size'], k['size']); c.rotate(k['tilt']); c.translate(-.33, -.03)
        eye = [(.125, -.02), (.19, up * .75 - .005, .27, up + .015, .345, up), (.43, up - .02, .49, .085 * (.3 + .7 * F.lid), .545, .075 * (.3 + .7 * F.lid)), (.47, .005, .40, lo, .31, lo - .004), (.24, lo, .18, -.035, .125, -.02)]
        for w, a in ((.12, .07), (.085, .10), (.055, .16), (.03, .25)):
            P.path(eye, True); P.col(k['kohl'], a * kh); c.set_line_width(w); c.stroke()
        if F.lid > .06:
            P.fill(eye, k['sclera']); c.save(); P.path(eye, True); c.clip()
            ix, iy = .325 + F.gx * .10 * sd, .045 + F.gy * .07; r = .108
            P.col(k['iris2']); c.arc(ix, iy, r, 0, 7); c.fill()
            g = cairo.RadialGradient(ix, iy - .04, .01, ix, iy, r * .9); a, b = rgb(k['iris']), rgb(k['iris2']); g.add_color_stop_rgba(0, *a, 1); g.add_color_stop_rgba(1, *b, 1); c.set_source(g); c.arc(ix, iy, r * .86, 0, 7); c.fill()
            P.col('#0a0508'); c.arc(ix, iy, .050 * F.pupil, 0, 7); c.fill()
            if F.glow > 0:
                g = cairo.RadialGradient(ix, iy, .0, ix, iy, r); g.add_color_stop_rgba(0, 1, .95, .6, F.glow); g.add_color_stop_rgba(.5, 1, .6, .15, F.glow); g.add_color_stop_rgba(1, 1, .3, .05, F.glow * .6); c.set_source(g); c.arc(ix, iy, r, 0, 7); c.fill()
            P.col('#ffffff'); c.arc(ix - .035 * sd, iy + .042, .026, 0, 7); c.fill(); P.col('#ffd9a0', .9); c.arc(ix + .035 * sd, iy - .045, .015, 0, 7); c.fill()
            if F.spark > 0:                                     # a flame reflected in the eye
                P.fill([(ix, iy - .07), (ix + .05, iy - .05, ix + .045, iy + .0, ix + .0, iy + .085), (ix - .045, iy + .0, ix - .05, iy - .05, ix, iy - .07)], '#ff9a2a', F.spark)
                P.fill([(ix, iy - .055), (ix + .03, iy - .04, ix + .025, iy - .0, ix, iy + .045), (ix - .025, iy + .0, ix - .03, iy - .04, ix, iy - .055)], '#fff0b0', F.spark)
            g = cairo.LinearGradient(0, up + .02, 0, up - .09); g.add_color_stop_rgba(0, .10, .04, .16, .75); g.add_color_stop_rgba(1, .1, .04, .16, 0); c.set_source(g); c.paint(); c.restore()
        wy = .135 * (.25 + .75 * F.lid)
        P.fill([(.11, -.03), (.18, up * .82, .27, up + .04, .35, up + .030), (.45, up + .005, .52, wy - .025, .655, wy), (.55, wy - .06, .49, wy - .06, .43, up - .055 * max(.25, F.lid)), (.36, up - .012, .27, up - .014, .21, up * .55 - .01), (.17, .02 * F.lid - .02, .14, -.01, .11, -.03)], INK)
        P.line([(.16, -.035), (.24, lo - .006, .33, lo - .016, .42, lo + .03), (.47, lo + .055, .51, .04 * F.lid, .555, .075 * F.lid)], .014)
        if F.lid > .2: P.line([(.20, up * .95 + .035), (.28, up + .075, .38, up + .075, .50, wy + .02)], .012, INK, .8)
        for i in range(int(k['lash'])):
            u = .35 + .6 * i / max(1, k['lash'] - 1); x = .12 + .48 * u; y = up + .03 - .10 * (u - .5) ** 2 * 2; P.line([(x, y), (x + .05, y + .04, x + .07, y + .06, x + .085 + .03 * u, y + .075)], .011)
        if F.tear > 0:
            P.fill([(.30, lo - .02), (.36, lo - .02, .38, lo - .10 - .3 * F.tear, .345, lo - .16 - .42 * F.tear), (.31, lo - .20 - .42 * F.tear, .27, lo - .14 - .42 * F.tear, .30, lo - .02)], '#dff2ff', .75)
        c.restore()
        c.save(); c.scale(sd, 1); c.translate(k['eyex'], 0); t = k['browt']
        i0 = k['browy'] - F.frown * .115 + F.sad * .10 + F.brow * .06; i1 = k['browy'] + F.brow * .10 - F.frown * .02; i2 = k['browy'] + F.brow * .05 + F.frown * .07 - F.sad * .09
        P.fill([(.085, .205 + i0), (.20, .31 + i0 * .6 + i1 * .4, .36, .375 + i1, .62, .235 + i2), (.40, .315 + i1 - .02 * (t - 1), .24, .275 + i0 * .5 + i1 * .5 - .05 * (t - 1), .10, .165 + i0 - .05 * (t - 1))], k['brow'])
        if F.frown > .25: P.line([(.045, .10 + i0 * .4), (.05, .16, .055, .19, .045, .235 + i0 * .3)], .014, k['nose'], .7)
        P.line([(.045, -.395), (.075, -.375, .10, -.38, .12, -.40)], .018, k['nose'], .9); P.line([(.155, -.28), (.185, -.32, .175, -.38, .14, -.395)], .012, k['nose'], .7)
        if F.smile > .45 or F.teeth > .4: P.line([(.22, -.40), (.28, -.47, .30, -.52, .285, -.60)], .011, k['nose'], .55)
        c.restore()
    mouth(P, F, k)
    if k['tilak'] == 'U':
        P.line([(-.085, .56), (-.085, .33, -.05, .19, 0, .145), (.05, .19, .085, .33, .085, .56)], .036, '#fff3cf'); P.fill([(-.022, .55), (-.03, .40, -.02, .27, 0, .215), (.02, .27, .03, .40, .022, .55)], '#c8202a')
    elif k['tilak'] == 'bindi': P.col('#b3122a'); c.arc(0, .245, .045, 0, 7); c.fill(); P.col('#ffd27a'); c.arc(0, .245, .016, 0, 7); c.fill()
    elif k['tilak'] == 'bars':
        for i in range(3): P.line([(-.20, .36 + .07 * i), (-.07, .345 + .07 * i, .07, .345 + .07 * i, .20, .36 + .07 * i)], .032, '#f2ead8', .95)
        P.col('#c8202a'); c.arc(0, .40, .05, 0, 7); c.fill()
    elif k['tilak'] == 'line': P.fill([(-.03, .56), (-.035, .38, -.02, .2, 0, .15), (.02, .2, .035, .38, .03, .56)], '#e8632a')
    if extra: extra(P, F, k)
    return P.out()


def mouth(P, F, k):
    c = P.c; s = F.smile; w = k['mouthw']; y = k['mouthy']; o = F.mouth * .24; cy = y - .585 + .07 * s - .03 * F.sad
    c.save()
    if o < .012 and F.teeth < .2:
        P.fill([(-.205 * w, cy), (-.12 * w, y - .545, -.05 * w, y - .522, 0, y - .540), (.05 * w, y - .522, .12 * w, y - .545, .205 * w, cy), (.12 * w, y - .60, .05 * w, y - .600, 0, y - .603), (-.05 * w, y - .600, -.12 * w, y - .60, -.205 * w, cy)], k['lip'])
        P.fill([(-.19 * w, cy - .003), (-.10 * w, y - .602, -.05 * w, y - .602, 0, y - .604), (.05 * w, y - .602, .10 * w, y - .602, .19 * w, cy - .003), (.12 * w, y - .675, .06 * w, y - .698, 0, y - .698), (-.06 * w, y - .698, -.12 * w, y - .675, -.19 * w, cy - .003)], k['lip2'])
        P.col(k['liphi'], .55); c.save(); c.translate(0, y - .648); c.scale(.075 * w, .02); c.arc(0, 0, 1, 0, 7); c.restore(); c.fill()
        P.line([(-.225 * w, cy + .007 + .01 * s), (-.12 * w, y - .606, -.04 * w, y - .592, 0, y - .606), (.04 * w, y - .592, .12 * w, y - .606, .225 * w, cy + .007 + .01 * s)], .016, '#2a0a1c')
    else:
        bot = y - .625 - o; g = max(o, .05 * F.teeth)
        outer = [(-.215 * w, cy), (-.12 * w, y - .545, -.05 * w, y - .520, 0, y - .538), (.05 * w, y - .520, .12 * w, y - .545, .215 * w, cy), (.19 * w, bot - .04, .09 * w, bot - .085, 0, bot - .085), (-.09 * w, bot - .085, -.19 * w, bot - .04, -.215 * w, cy)]
        P.fill(outer, k['lip2'])
        inner = [(-.185 * w, cy - .006), (-.10 * w, y - .590, -.04 * w, y - .583, 0, y - .590), (.04 * w, y - .583, .10 * w, y - .590, .185 * w, cy - .006), (.15 * w, bot + .005, .08 * w, bot - .018, 0, bot - .018), (-.08 * w, bot - .018, -.15 * w, bot + .005, -.185 * w, cy - .006)]
        P.fill(inner, '#2a0612'); c.save(); P.path(inner, True); c.clip()
        if F.teeth > .05 or o > .05:
            P.fill([(-.2 * w, y - .53), (.2 * w, y - .53), (.17 * w, y - .615 - .02 * F.teeth, .06 * w, y - .635 - .03 * F.teeth, 0, y - .635 - .03 * F.teeth), (-.06 * w, y - .635 - .03 * F.teeth, -.17 * w, y - .615 - .02 * F.teeth, -.2 * w, y - .53)], '#fdf6e6')
            if F.teeth > .6: P.fill([(-.2 * w, bot - .06), (.2 * w, bot - .06), (.15 * w, bot + .045), (-.15 * w, bot + .045)], '#f3e8d2'); [P.line([(x * w, y - .50), (x * w, bot - .05)], .006, '#8a6a5a', .5) for x in np.linspace(-.15, .15, 7)]
        if o > .06 and F.teeth < .7: P.col('#b8485a'); c.save(); c.translate(0, bot + .0); c.scale(.11 * w, .06); c.arc(0, 0, 1, 0, 7); c.restore(); c.fill()
        c.restore(); P.path(outer, True); P.col('#2a0a1c'); c.set_line_width(.012); c.stroke(); P.path(inner, True); c.set_line_width(.010); c.stroke()
    c.restore()
