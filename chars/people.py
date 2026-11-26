"""The people of the story.  See the bottom of the file for names; every figure takes u=dict(lamp=1.) (a lit diya in both hands)."""
import cairo, math, numpy as np
from lau.stage import Fig
from lau.rig import Pose, V, palm_point
from lau.face import human, Face, rgb
from lau import poses as PZ
from . import sita
from .sita import lashes

LAMPPAL = {20: ((2.4, 1.2, .3), (2.4, 1.2, .3), 4), 21: ('#c8822a', '#6a3a12', 1)}
W_PAL = {**sita.PAL, 22: ('#0f7a58', '#063a34', 3), 23: ('#6a2aa8', '#2a0a54', 3)}
WU = dict(look=3, hairm=2, veil=0., lamp=0., old=0., crownk=0.)


def eyes_fine(P, F, k, lid=('#5a2a86', '#1f7a5c'), iris=('#c98a2e', '#6a3210', '#1a0804'), ink='#120712'):
    """eyes redrawn for a full-screen close-up: iris fibres, limbal ring, kohl, painted lids, lashes, a glint"""
    c = P.c; up = -.035 + .20 * F.lid; lo = -.062 + .03 * max(F.smile, 0) + .05 * F.squint; wy = .135 * (.25 + .75 * F.lid) + .015
    rnd = np.random.RandomState(7)
    for sd in (1, -1):
        c.save(); c.scale(sd, 1); c.translate(k['eyex'], 0); c.translate(.33, .03); c.scale(k['size'], k['size']); c.rotate(k['tilt']); c.translate(-.33, -.03)
        eye = [(.125, -.02), (.19, up * .75 - .005, .27, up + .015, .345, up), (.43, up - .02, .49, .085 * (.3 + .7 * F.lid), .545, .075 * (.3 + .7 * F.lid)), (.47, .005, .40, lo, .31, lo - .004), (.24, lo, .18, -.035, .125, -.02)]
        # painted lid: a soft wash up to the crease
        lidp = [(.10, -.03), (.17, up * .9 + .03, .27, up + .115, .38, up + .105), (.48, up + .085, .58, wy + .06, .72, wy + .085), (.60, wy - .01, .50, wy - .02, .43, up - .03), (.33, up - .005, .20, up * .6, .10, -.03)]
        g = cairo.LinearGradient(0, up, 0, up + .11); a, b = rgb(lid[0]), rgb(lid[1]); g.add_color_stop_rgba(0, *a, .95); g.add_color_stop_rgba(.55, *b, .75); g.add_color_stop_rgba(1, *b, 0); P.path(lidp, True); c.set_source(g); c.fill()
        for w, al in ((.10, .10), (.07, .16), (.045, .30), (.028, .5)): P.path(eye, True); P.col(k['kohl'], al); c.set_line_width(w); c.stroke()
        if F.lid > .06:
            g = cairo.LinearGradient(0, up, 0, lo); g.add_color_stop_rgba(0, .80, .74, .78, 1); g.add_color_stop_rgba(.45, 1, .97, .92, 1); g.add_color_stop_rgba(1, .95, .88, .86, 1); P.path(eye, True); c.set_source(g); c.fill()
            c.save(); P.path(eye, True); c.clip()
            P.col('#c9605a', .55); c.arc(.135, -.018, .022, 0, 7); c.fill()
            ix, iy = .325 + F.gx * .10 * sd, .045 + F.gy * .07; r = .112; a, b, d = [rgb(q) for q in iris]
            P.col(iris[2]); c.arc(ix, iy, r, 0, 7); c.fill()
            g = cairo.RadialGradient(ix, iy, .03, ix, iy, r * .93); g.add_color_stop_rgba(0, *b, 1); g.add_color_stop_rgba(.45, *a, 1); g.add_color_stop_rgba(.8, *b, 1); g.add_color_stop_rgba(1, *d, 1); c.set_source(g); c.arc(ix, iy, r * .93, 0, 7); c.fill()
            for i in range(84):                                   # fibres of the iris
                t = i / 84 * 6.2832 + rnd.uniform(-.03, .03); r0, r1 = .045 + .012 * rnd.rand(), r * (.70 + .20 * rnd.rand()); m = t + rnd.uniform(-.05, .05)
                P.line([(ix + math.cos(t) * r0, iy + math.sin(t) * r0), (ix + math.cos(m) * r1, iy + math.sin(m) * r1)], .0022 + .002 * rnd.rand(), '#ffd98a' if i % 3 == 0 else iris[2], .55 if i % 3 == 0 else .40)
            g = cairo.RadialGradient(ix, iy - .05, .005, ix, iy - .045, .07); g.add_color_stop_rgba(0, 1, .82, .40, .75); g.add_color_stop_rgba(1, 1, .6, .2, 0); c.set_source(g); c.arc(ix, iy, r * .9, 0, 7); c.fill()
            P.col('#050208'); c.arc(ix, iy, .048 * F.pupil, 0, 7); c.fill()
            if F.spark > 0:
                P.fill([(ix, iy - .07), (ix + .05, iy - .05, ix + .045, iy + .0, ix + .0, iy + .085), (ix - .045, iy + .0, ix - .05, iy - .05, ix, iy - .07)], '#ff9a2a', F.spark); P.fill([(ix, iy - .055), (ix + .03, iy - .04, ix + .025, iy - .0, ix, iy + .045), (ix - .025, iy + .0, ix - .03, iy - .04, ix, iy - .055)], '#fff0b0', F.spark)
            if F.glow > 0:
                g = cairo.RadialGradient(ix, iy, 0, ix, iy, r); g.add_color_stop_rgba(0, 1, .95, .6, F.glow); g.add_color_stop_rgba(.5, 1, .6, .15, F.glow); g.add_color_stop_rgba(1, 1, .3, .05, F.glow * .6); c.set_source(g); c.arc(ix, iy, r, 0, 7); c.fill()
            x, y = ix - .038 * sd, iy + .042                      # the glint: a small window and its echo
            P.fill([(x - .026, y - .014), (x - .022, y + .010, x - .010, y + .022, x + .012, y + .024), (x + .020, y + .006, x + .018, y - .012, x + .004, y - .024), (x - .010, y - .026, x - .020, y - .022, x - .026, y - .014)], '#ffffff'); P.col('#ffe2b0', .95); c.arc(ix + .042 * sd, iy - .048, .013, 0, 7); c.fill(); P.col('#ffffff', .8); c.arc(ix + .058 * sd, iy + .02, .006, 0, 7); c.fill()
            g = cairo.LinearGradient(0, up + .02, 0, up - .10); g.add_color_stop_rgba(0, .06, .01, .12, .88); g.add_color_stop_rgba(1, .06, .01, .12, 0); c.set_source(g); c.paint(); c.restore()
        # kohl: upper line and wing, lower line, lashes
        P.fill([(.095, -.045), (.17, up * .78, .27, up + .035, .35, up + .030), (.45, up + .010, .53, wy - .03, .70, wy + .045), (.58, wy - .055, .50, wy - .065, .43, up - .060 * max(.25, F.lid)), (.36, up - .016, .27, up - .018, .21, up * .55 - .012), (.17, .02 * F.lid - .02, .14, -.008, .095, -.045)], ink)
        P.fill([(.13, -.035), (.22, lo - .012, .32, lo - .022, .42, lo + .022), (.48, lo + .05, .52, .035 * F.lid, .60, wy - .035), (.50, lo + .055, .44, lo + .052, .41, lo + .040), (.32, lo - .004, .22, lo + .004, .13, -.035)], ink)
        if F.lid > .2: P.line([(.17, up * .9 + .05), (.26, up + .105, .38, up + .105, .56, wy + .045)], .009, '#2a0f22', .85)
        for i in range(11):
            u = i / 10; x = .27 + .35 * u; y = up + .022 - .60 * (u - .34) ** 2 * (.30 if u > .34 else .9) * (up + .04) * 1.2; y = y * (1 - u * .35) + (wy + .0) * u * .35; l = .020 + .036 * u
            P.fill([(x - .008, y - .012), (x + .014 + .014 * u, y + l * .30, x + .026 + .040 * u, y + l * .6, x + .036 + .072 * u, y + l), (x + .022 + .046 * u, y + l * .35, x + .018 + .02 * u, y + l * .05, x + .008, y - .012)], ink)
        for i in range(9):
            u = i / 8; x = .28 + .23 * u; y = lo - .010 + .085 * u * u; P.line([(x, y), (x + .008, y - .012, x + .014 + .01 * u, y - .020, x + .022 + .014 * u, y - .022)], .006, ink, .85)
        if F.tear > 0: P.fill([(.30, lo - .02), (.36, lo - .02, .38, lo - .10 - .3 * F.tear, .345, lo - .16 - .42 * F.tear), (.31, lo - .20 - .42 * F.tear, .27, lo - .14 - .42 * F.tear, .30, lo - .02)], '#dff2ff', .75)
        c.restore()


def wrinkles(P, F, k, col=None, beard=False):
    """age: brow furrows, crow's feet, bags, folds beside the mouth"""
    c = P.c; w = col or k['nose']
    for i in range(3): P.line([(-.30, .46 + .085 * i), (-.12, .435 + .085 * i + .02, .12, .435 + .085 * i + .02, .30, .46 + .085 * i)], .013, w, .55 - .08 * i)
    for sd in (1, -1):
        c.save(); c.scale(sd, 1)
        for i in range(3): P.line([(.60, .06 - .05 * i), (.64, .07 - .065 * i, .67, .07 - .08 * i, .71, .08 - .10 * i)], .011, w, .6)
        P.line([(.17, -.12), (.25, -.175, .37, -.175, .46, -.11)], .012, w, .6); P.line([(.22, -.175), (.28, -.205, .35, -.205, .41, -.175)], .009, w, .4)
        P.line([(.125, -.36), (.22, -.43, .27, -.50, .275, -.60)], .015, w, .75)
        if not beard: P.line([(.25, -.66), (.27, -.71, .27, -.75, .25, -.80)], .011, w, .5)
        P.line([(.04, .13), (.045, .17, .045, .20, .04, .235)], .010, w, .55)
        c.restore()


def kaikeyi_face(F, S=2048, box=(-1.1, -1.25, 1.1, .95)):
    st = dict(iris='#c98a2e', iris2='#1a0804', lip='#8a1838', lip2='#a82a48', liphi='#f0a0a0', blush='#c84a5a', brow='#150a12', browt=1.15, browy=.01, tilak=None, size=1.12, nose='#8a4632', kohl='#180818', mouthw=.84, tilt=.075)

    def extra(P, F, k):
        eyes_fine(P, F, k); P.line([(-.045, .10), (-.065, -.02, -.060, -.14, -.085, -.235)], .012, k['nose'], .45)
        P.fill([(0, .41), (.028, .33, .030, .27, 0, .215), (-.030, .27, -.028, .33, 0, .41)], '#0f7a58'); P.col('#ffd27a'); P.c.arc(0, .20, .018, 0, 7); P.c.fill(); P.col('#1a0810'); P.c.arc(.30, -.60, .016, 0, 7); P.c.fill()
    G = F.set(frown=min(1., F.frown + .15), brow=F.brow + .12, lid=F.lid * .90, squint=min(1., F.squint + .25))
    if box[3] < .9: st['blush'] = None
    return human(G, st, box=box, S=S, extra=extra)


KAIKEYI = Fig('kaikeyi', 'people.glsl', {**W_PAL, 1: ('#e0a878', '#94563c', 1), 2: ('#1c1218', '#0a060a', 5), 7: ('#0f7a56', '#063430', 8), 8: ('#6a2a9a', '#2c0c50', 8), 9: ('#4a1470', '#200838', 8), 10: ('#7a34aa', '#320e58', 8), 4: ('#0f8a5c', '#063a34', 3), 5: ('#6a2aa8', '#2a0a54', 3), 17: ('#34105a', '#180628', 8), 18: ('#e8a838', '#8a4a14', 1)},
              dim={**sita.DIM, 'chest': 2.62, 'neck': 1.40}, build={**sita.BUILD, 'shoulder': .83}, hs=[.92, .80, .95, .76, 1.05, .6, 1.05, .98], face=kaikeyi_face, u=dict(WU, look=0, hairm=1, veil=2., crownk=1.), defs='#define KIND 0')
EYEBOX = (-.80, -.32, .80, .58)
KAIKEYI_EYES = KAIKEYI.variant(face=lambda F: kaikeyi_face(F, S=3072, box=EYEBOX)); KAIKEYI_EYES.box = EYEBOX


def woman_face(F, age=0, **k):
    st = dict(iris='#5a3018', iris2='#1a0c06', lip='#a84848', lip2='#bf5f58', liphi='#f0b8a8', blush='#d06a50', brow='#24140f', browt=.85, browy=.015, tilak='bindi', size=1.02, nose='#8a4a34', kohl='#2a1412', mouthw=.86)

    def ex(P, F, k):
        (wrinkles if age else lashes)(P, F, k)
    return human(F, {**st, **k}, S=768, extra=ex)


KAUSHALYA = KAIKEYI.variant(pal={1: ('#d8a27c', '#8a5844', 1), 2: ('#c9c6cc', '#74707e', 5), 7: ('#f4efe2', '#a69aa6', 1), 8: ('#f8f3e6', '#aca0aa', 1), 9: ('#d8cdb8', '#8c8088', 1), 10: ('#f8f3e6', '#aaa0ac', 1), 18: ('#c8963a', '#7a5428', 1), 19: ('#c8963a', '#7a5428', 1), 4: ('#c4142c', '#54081c', 3)}, build=dict(arm=.64, waist=.82, bust=.65), u=dict(WU, look=3, hairm=2, veil=1., old=.8),
                            face=lambda F: woman_face(F, 1, brow='#9a949c', lip='#a0605c', lip2='#b4736a', blush=None, size=.98, tilak='line', browt=.9, nose='#7a4c40'))
_CF = KAUSHALYA.variant(pal={1: ('#c98a5c', '#7e4a34', 1), 2: ('#241812', '#0e0808', 5), 7: ('#2f7f9a', '#173c5c', 1), 8: ('#f0b84a', '#9a6426', 1), 9: ('#c23a3a', '#641824', 1), 10: ('#f0b84a', '#9a6426', 1), 18: ('#c23a3a', '#641824', 1), 19: ('#f0c860', '#9a6a2a', 1)}, build=dict(arm=.68, waist=.78, bust=.75), u=dict(WU), face=lambda F: woman_face(F))
CITIZEN_F = [_CF,
             _CF.variant(pal={1: ('#b87a4e', '#70402c', 1), 7: ('#c8467a', '#64204c', 1), 8: ('#e87a3a', '#8c3a22', 1), 9: ('#3a7a4a', '#1c4030', 1), 10: ('#e87a3a', '#8c3a22', 1), 18: ('#f8d068', '#a0702c', 1), 19: ('#f8d068', '#a0702c', 1)}, u=dict(WU, veil=1.)),
             _CF.variant(pal={1: ('#d8a070', '#8a5438', 1), 7: ('#7a9a3a', '#3c5424', 1), 8: ('#f2e6c8', '#a4947e', 1), 9: ('#8a3a6a', '#481c40', 1), 18: ('#8a3a6a', '#481c40', 1), 19: ('#f2e6c8', '#a4947e', 1)}, u=dict(WU, hairm=0))]

# ---------------------------------------------------------------- men
MU = dict(look=0, hairm=2, veil=0., lamp=0., old=0., beard=0., hairk=3, robe=.55, shawl=0, tunic=0, beads=0., staff=0., bowl=0., kid=0.)
M_PAL = {1: ('#c08654', '#744630', 1), 2: ('#20140f', '#0c0706', 5), 3: ('#ffffff', '#805030', 2), 4: ('#b3122a', '#54081c', 3), 5: ('#0f7a58', '#063a34', 3), 6: ('#fbf1dc', '#bfa898', 1), 7: ('#f2e6cc', '#a2908a', 1), 8: ('#d8662a', '#7c3018', 1), 9: ('#f2e6c8', '#a8947a', 1), 12: ('#c83a2a', '#661820', 1), 13: ('#7a4a22', '#3a1e0c', 1), 14: ('#f0b83a', '#9a5a1c', 1), 17: ('#8a1a2a', '#420a1a', 8), 18: ('#c83a2a', '#661820', 1), 19: ('#c83a2a', '#661820', 1), 22: ('#6b3416', '#2e130a', 1), **LAMPPAL}
M_HS = [1.10, 1.25, 1.06, 1.08, .92, 1.05, .95, 1.02]
M_BUILD = dict(chest=.90, depth=.94, rib=.92, waist=.96, hips=.94, arm=.86, leg=.92, hand=.94, neck=.94, shoulder=.90)


def moustache(P, w=1., col='#1a100c'):
    for sd in (1, -1):
        P.c.save(); P.c.scale(sd, 1); P.fill([(0, -.455), (.08, -.43, .18, -.46, .31 * w, -.565), (.36 * w, -.60, .38 * w, -.57, .39 * w, -.53), (.38 * w, -.64, .30 * w, -.655, .22 * w, -.59), (.14, -.545, .06, -.515, 0, -.515)], col); P.c.restore()


def man_face(F, age=0, mous=0, beard=False, **k):
    st = dict(iris='#5a3018', iris2='#1a0c06', lip='#9a5240', lip2='#ad6450', liphi='#e0a890', brow='#1c1210', browt=1.25, tilak='line', size=.94, nose='#6a3a24', kohl='#1a0c10', kohlk=.6, mouthw=.92)

    def ex(P, F, k):
        if age: wrinkles(P, F, k, beard=beard)
        if mous: moustache(P, mous)
    return human(F, {**st, **k}, S=768, extra=ex)


_M = Fig('men', 'people.glsl', M_PAL, build=M_BUILD, hs=M_HS, face=lambda F: man_face(F, mous=1.), u=MU, defs='#define KIND 1')
DASHARATHA = _M.variant(pal={1: ('#cf9a6c', '#80523c', 1), 2: ('#f2eee8', '#a39aa6', 5), 7: ('#f4e8cc', '#a8907a', 8), 8: ('#e8a83a', '#8e5620', 8), 9: ('#f0dfb8', '#a4866c', 8), 17: ('#a8641e', '#5a2c14', 8), 4: ('#c4142c', '#54081c', 3)}, build=dict(belly=.7, waist=1.05, arm=.84), u=dict(beard=1.25, hairk=1, robe=2., shawl=1, tunic=2, beads=2., old=.8),
                        face=lambda F: man_face(F, 1, beard=True, brow='#e6e0da', browt=1.5, nose='#7a4a34', size=.95))
SAGE = _M.variant(pal={1: ('#c08a5a', '#744a34', 1), 2: ('#eee9e0', '#9a92a0', 5), 7: ('#e0822a', '#8a441c', 1), 8: ('#e8923a', '#924c20', 1), 18: ('#a83a1c', '#5a1c14', 1)}, build=dict(chest=.84, waist=.88, arm=.76, belly=.0), u=dict(beard=1.5, hairk=0, robe=2., shawl=2, beads=1., old=.9),
                  face=lambda F: man_face(F, 1, beard=True, brow='#ddd6cc', browt=1.4, tilak='bars', nose='#6e4028'))
MENDICANT = _M.variant(pal={1: ('#b27a4c', '#6a3e2a', 1), 2: ('#3a2a22', '#160e0c', 5), 7: ('#c8742a', '#743a1a', 1), 8: ('#d2802e', '#7c421c', 1), 18: ('#7e3516', '#40180c', 1)}, u=dict(beard=.55, hairk=0, robe=2., shawl=2, beads=1., staff=1., bowl=1.),
                       face=lambda F: man_face(F.set(lid=min(F.lid, 1.)), 0, beard=True, tilak='bars', nose='#5e3420', size=.98))
_CM = _M.variant(u=dict(hairk=2))
CITIZEN_M = [_CM,
             _CM.variant(pal={1: ('#a87044', '#64392a', 1), 7: ('#e8c070', '#94703c', 1), 8: ('#2f7f7a', '#173c44', 1), 12: ('#f0c24a', '#98682a', 1), 14: ('#c83a2a', '#661820', 1), 18: ('#2f7f7a', '#173c44', 1), 2: ('#8a8684', '#44404a', 5)}, u=dict(hairk=2, beard=.35, shawl=1), face=lambda F: man_face(F, 0, beard=True, brow='#4a4440')),
             _CM.variant(pal={1: ('#cf9868', '#80503a', 1), 7: ('#8aa0b8', '#445470', 1), 8: ('#f2e6c8', '#a4947e', 1), 9: ('#a8382e', '#5a1820', 1), 18: ('#f2e6c8', '#a4947e', 1), 19: ('#f0c24a', '#98682a', 1)}, u=dict(hairk=3, tunic=1, shawl=3), face=lambda F: man_face(F, mous=.85))]
BHARATA = _M.variant(pal={1: ('#e6bd84', '#94683f', 1), 2: ('#241812', '#0e0808', 5), 7: ('#dcebd2', '#7e9484', 1), 8: ('#4a8a5a', '#1f4a38', 1), 18: ('#4a8a5a', '#1f4a38', 1)}, build=dict(chest=1., depth=1., rib=.98, waist=.96, hips=.98, arm=.95, leg=.98, neck=.98, shoulder=.98), u=dict(hairk=0, robe=.40, beads=1.),
                     face=lambda F: man_face(F, tilak='U', lip='#a8483c', lip2='#c0604c', nose='#8a5a34', size=1.0, browt=1.05))
OLD_HAND = SAGE.variant(u=dict(old=1., hairk=3, beads=0., shawl=1))

# ---------------------------------------------------------------- children
C_DIM = dict(chest=1.45, shx=.80, shy=.48, shz=-.06, neck=.74, nz=-.06, head=1.10, hz=.10, up=1.36, fore=1.24, hipx=.36, hipy=-.20, th=1.98, sh=1.82, hand=.66, foot=.62)
C_BUILD = dict(chest=.6, depth=.6, rib=.6, waist=.6, hips=.66, arm=.60, leg=.66, hand=1., neck=.6, shoulder=.80)
C_HS = [1.02, .80, .72, .88, 1.16, .5, .95, .88]


def child_face(F, **k):
    st = dict(iris='#6a3a1c', iris2='#1e0e06', lip='#b85a52', lip2='#cc7468', liphi='#f8c8b8', blush='#e8705a', brow='#24140f', browt=.8, browy=.03, tilak='bindi', size=1.14, nose='#9a5a3c', kohl='#2a1412', mouthw=.74)
    return human(F, {**st, **k}, S=768, extra=lambda P, F, k: lashes(P, F, k, n=2))


CHILD = _M.variant(pal={1: ('#d09a68', '#845238', 1), 7: ('#f2e6cc', '#a2908a', 1), 8: ('#d83a2e', '#701c20', 1), 9: ('#f0a83a', '#98602a', 1), 18: ('#d83a2e', '#701c20', 1), 19: ('#d83a2e', '#701c20', 1)}, u=dict(hairk=4, robe=.5, shawl=3, tunic=1, kid=1.), face=child_face)
CHILD.dim, CHILD.build, CHILD.hs = C_DIM, C_BUILD, C_HS
CHILD_B = CHILD.variant(pal={1: ('#b87c4e', '#70422c', 1), 9: ('#2f8f8a', '#174a50', 1), 8: ('#e8c24a', '#94702a', 1), 18: ('#e8c24a', '#94702a', 1), 19: ('#f8e0a0', '#a4885a', 1)})
CHILD_HAND = CHILD


def lit(fig, hands=1.):
    """the same figure holding a lit diya: hands 1 both, 2 right, 3 left"""
    return fig.variant(u=dict(lamp=float(hands)))


CITIZEN_M_LAMP = [lit(f) for f in CITIZEN_M]; CITIZEN_F_LAMP = [lit(f) for f in CITIZEN_F]; CHILD_LAMP = lit(CHILD); CHILD_B_LAMP = lit(CHILD_B); KAUSHALYA_LAMP = lit(KAUSHALYA)


def flame(S, hands=1):
    """world point of the diya's flame for a Solved figure (light it with Light.pts, or add FX.flame there)"""
    a, b = palm_point(S.u, 'L'), palm_point(S.u, 'R'); k = S.u['B'][7]; o = (.5 * (a + b) if hands == 1 else b if hands == 2 else a) + V(0, .18 if hands == 1 else .24, 0) * k
    return S.w(o + V(0, .95, .76) * .50 * k)


# ---------------------------------------------------------------- poses.  men = full height, women use sita.fit, children child_pose
P_LAMP = Pose(hedr=(0, 8, 0), lh=(.98, 10.0, 2.0), rh=(-.98, 10.0, 2.0), lhand='open', rhand='open', lfing=(-.62, -.02, .78), rfing=(.62, -.02, .78), lpalm=(-.22, 1, -.05), rpalm=(.22, 1, -.05), lel=(1, -1, -.2), rel=(-1, -1, -.2))
P_WAVE = Pose(pelr=(0, 0, -3), cher=(0, -3, 5), hedr=(0, -6, -4), rh=(-2.9, 14.2, .9), rhand='open', rfing=(-.25, 1, .1), rpalm=(0, 0, 1), rel=(-1, -.5, .0), lh=(2.0, 7.9, .5))
P_BOW = Pose(pel=(0, 8.3, -.7), pelr=(0, 22, 0), cher=(0, 22, 0), hedr=(0, 16, 0), lh=(.26, 9.2, 4.1), rh=(-.26, 9.2, 4.1), lhand='anjali', rhand='anjali', lfing=(0, .7, .7), rfing=(0, .7, .7), lpalm=(-1, 0, 0), rpalm=(1, 0, 0), lel=(1, -.4, -.4), rel=(-1, -.4, -.4))
P_NAMASTE = PZ.ANJALI.set(hedr=(0, 10, 0))
P_WALK = lambda ph: PZ.walk(ph, stride=1.35, lift=.6, bounce=.14, swing=1.)
K_TWO = Pose(pel=(.2, 8.22, 0), pelr=(8, 0, 5), cher=(-6, -2, -8), hedr=(-6, 2, 4), lf=(.62, .75, .05), rf=(-.42, .84, .42), rft=(-16, 8), rh=(-1.75, 11.9, 2.1), rhand='two', rfing=(.05, 1, .12), rpalm=(.1, 0, 1), rel=(-1, -1, -.1), lh=(1.35, 8.5, .9), lhand='relax', lfing=(-.5, -.2, .8), lpalm=(-.4, -.6, -.5), lel=(1, .0, -.9))
D_KING = Pose(pel=(0, 4.75, -.4), pelr=(0, -4, 0), cher=(0, 2, 0), hedr=(0, 2, 0), lf=(1.15, .75, 2.7), rf=(-1.15, .75, 2.5), lkn=(.35, .4, 1), rkn=(-.35, .4, 1), lh=(1.85, 5.35, 2.7), rh=(-1.85, 5.35, 2.7), lhand='relax', rhand='relax', lfing=(0, -.35, .95), rfing=(0, -.35, .95), lpalm=(0, -1, -.2), rpalm=(0, -1, -.2), lel=(1, -.1, -.6), rel=(-1, -.1, -.6))
B_SANDALS = PZ.KNEEL.set(cher=(0, 14, 0), hedr=(0, 12, 0), lh=(.75, 6.4, 3.0), rh=(-.75, 6.4, 3.0), lhand='open', rhand='open', lfing=(-.35, .1, .9), rfing=(.35, .1, .9), lpalm=(0, 1, -.1), rpalm=(0, 1, -.1), lel=(1, -.6, -.3), rel=(-1, -.6, -.3))
P_STAFF = Pose(hedr=(0, 12, 0), rh=(-2.0, 9.0, 1.5), rhand='grip', rfing=(.45, .1, .85), rpalm=(.9, .1, -.4), rel=(-.8, -.8, -.5), lh=(1.0, 9.5, 2.2), lhand='cup', lfing=(-.5, .05, .85), lpalm=(0, 1, 0), lel=(1, -1, -.2))
P_GIVE = P_LAMP.set(cher=(0, 12, 0), hedr=(0, 14, 0), rh=(-.4, 9.2, 3.6), rhand='open', rfing=(.25, -.05, .97), rpalm=(.2, 1, 0), lh=(1.7, 8.0, 1.0), lhand='relax', lfing=None, lpalm=None)


def child_pose(pose):
    """any adult pose brought down to the child's height"""
    k, kl = .54, .545
    f = lambda v, o=0.: None if v is None else tuple(k * x for x in v)
    up = lambda v: None if v is None else (v[0] * .62, (v[1] - 8.35) * .56 + 4.55, v[2] * .56)
    leg = lambda v: (v[0] * .58, .48 + (v[1] - .75) * kl, v[2] * kl)
    return pose.set(pel=(pose.pel[0] * k, (pose.pel[1] - 8.35) * kl + 4.48, pose.pel[2] * k), lh=up(pose.lh), rh=up(pose.rh), lf=leg(pose.lf), rf=leg(pose.rf))


C_STAND, C_LAMP, C_WAVE = child_pose(PZ.STAND), child_pose(P_LAMP), child_pose(P_WAVE)
F_LAMP, F_WAVE, F_NAMASTE, F_STAND = [sita.fit(p) for p in (P_LAMP, P_WAVE, P_NAMASTE, PZ.STAND)]
