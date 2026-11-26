"""Leather shadow puppets (tholu bommalata), drawn flat in cairo as what they let through: dyed translucent hide, black cut edges, punched holes that shine.  Heights in units of one puppet = 1."""
import cairo, math, numpy as np
from lau.plates import smooth_path, poly
BK = (.05, .015, .012); HOLE = (1., .93, .70)
DYE = dict(ochre=(.86, .50, .20), blue=(.13, .33, .40), red=(.66, .09, .05), green=(.15, .36, .13), yellow=(.95, .66, .18), rose=(.80, .34, .24), brown=(.36, .15, .07), white=(.95, .86, .66), violet=(.36, .13, .28))


def hide(c, P, col, lw=.010, n=8, close=True, smooth=True):
    """a piece of dyed leather with a cut black edge"""
    Q = smooth_path(P, n, close) if smooth else np.asarray(P, float); poly(c, Q, close); c.set_source_rgb(*(DYE[col] if isinstance(col, str) else col)); c.fill_preserve(); c.set_source_rgb(*BK); c.set_line_width(lw); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke()


def holes(c, P, step=.018, r=.005, col=HOLE, n=10):
    """a row of punched holes along a curve"""
    Q = smooth_path(P, n); d = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(Q, axis=0), axis=1))]); k = max(2, int(d[-1] / step)); s = np.linspace(0, d[-1], k); c.set_source_rgb(*col)
    for x, y in zip(np.interp(s, d, Q[:, 0]), np.interp(s, d, Q[:, 1])): c.new_sub_path(); c.arc(x, y, r, 0, 7)
    c.fill()


def rosette(c, x, y, r, n=8, col=HOLE, core=True):
    c.set_source_rgb(*col)
    for i in range(n): a = i * 2 * math.pi / n; c.save(); c.translate(x + math.cos(a) * r * .62, y + math.sin(a) * r * .62); c.rotate(a); c.scale(r * .34, r * .17); c.new_sub_path(); c.arc(0, 0, 1, 0, 7); c.restore()
    c.fill()
    if core: c.new_sub_path(); c.arc(x, y, r * .20, 0, 7); c.fill()


def slits(c, x0, x1, y0, y1, n, col=HOLE, w=.004):
    c.set_source_rgb(*col); c.set_line_width(w); c.set_line_cap(cairo.LINE_CAP_ROUND)
    for i in range(n): u = (i + .5) / n; x = x0 + (x1 - x0) * u; c.move_to(x, y0); c.line_to(x + (x - (x0 + x1) / 2) * .18, y1)
    c.stroke()


def head(c, skin='ochre', crown='king', beard=False, eye=1., smile=.2):
    """profile facing +x; origin at the neck, chin about (.07,-.03); head height about .17"""
    if crown in ('king', 'prince', 'rishi'):                        # hair bun or back hair
        hide(c, [(-.01, -.03), (-.085, -.02), (-.115, -.075), (-.085, -.14), (-.02, -.165), (.02, -.12)], (.06, .03, .04))
    hide(c, [(-.035, .03), (.030, .025), (.028, -.012), (.062, -.010), (.082, -.030), (.078, -.046), (.092, -.054), (.084, -.066), (.094, -.076), (.088, -.088), (.112, -.098), (.092, -.128), (.084, -.150), (.070, -.176), (.030, -.192), (-.030, -.186), (-.062, -.150), (-.060, -.090), (-.048, -.040)], skin, n=6)
    if beard: hide(c, [(-.02, -.04), (.02, -.02), (.06, -.035), (.085, -.05), (.10, -.01), (.085, .06), (.05, .125), (.02, .06), (-.01, .02)], (.93, .88, .78)); slits(c, .01, .085, -.005, .085, 6, BK, .003)
    # eye: a big fish-shaped cut
    c.save(); c.translate(.052, -.122); c.move_to(-.040, .004); c.curve_to(-.015, -.026, .015, -.024, .034, -.004); c.curve_to(.014, .014, -.016, .016, -.040, .004); c.set_source_rgb(*HOLE); c.fill_preserve(); c.set_source_rgb(*BK); c.set_line_width(.006); c.stroke(); c.arc(.004, -.004, .0105 * eye, 0, 7); c.fill()
    c.set_line_width(.008); c.move_to(-.042, -.030); c.curve_to(-.012, -.050, .022, -.046, .042, -.030); c.stroke(); c.restore()
    c.set_source_rgb(*BK); c.set_line_width(.005); c.move_to(.086, -.062); c.line_to(.060, -.058 - .012 * smile); c.stroke()
    c.set_line_width(.012); c.set_source_rgb(*DYE['red']); c.move_to(.084, -.150); c.line_to(.078, -.176); c.stroke()
    hide(c, [(-.030, -.085), (-.012, -.105), (-.004, -.085), (-.014, -.050), (-.032, -.055)], skin, .006); hide(c, [(-.020, -.052), (.006, -.030), (-.018, -.004), (-.044, -.028)], 'yellow', .006); rosette(c, -.019, -.028, .017, 6)
    if crown == 'king':
        hide(c, [(-.070, -.160), (.088, -.168), (.094, -.200), (.050, -.215), (.062, -.262), (.036, -.262), (.036, -.318), (.010, -.306), (.004, -.372), (-.004, -.306), (-.030, -.318), (-.032, -.262), (-.062, -.258), (-.052, -.212), (-.082, -.196)], 'yellow', .009, smooth=False)
        holes(c, [(-.062, -.176), (.010, -.184), (.086, -.182)], .018, .0050); rosette(c, .006, -.232, .030, 8); rosette(c, .004, -.285, .016, 6); hide(c, [(.075, -.185), (.135, -.215), (.100, -.165)], 'red', .006)
    elif crown == 'prince':
        hide(c, [(-.066, -.160), (.086, -.166), (.080, -.205), (.046, -.200), (.040, -.250), (.008, -.232), (-.016, -.252), (-.028, -.202), (-.064, -.200)], 'yellow', .009, smooth=False); holes(c, [(-.056, -.176), (.010, -.184), (.078, -.180)], .018, .0048); rosette(c, .010, -.208, .018, 6)
        hide(c, [(.004, -.250), (.02, -.300), (.056, -.316), (.044, -.280), (.016, -.246)], 'green', .006)
    elif crown == 'rishi':
        hide(c, [(-.05, -.172), (.06, -.185), (.05, -.215), (.03, -.262), (.0, -.285), (-.03, -.262), (-.04, -.212)], (.30, .17, .10)); holes(c, [(-.04, -.190), (.005, -.198), (.05, -.196)], .016, .0042); slits(c, -.03, .035, -.265, -.21, 5, HOLE, .003)


def arm(c, x, y, a1, a2, skin, l1=.17, l2=.15, hand='open', band='yellow'):
    """shoulder at (x,y); angles in degrees, 0 = hanging down, + = forward (+x)"""
    c.save(); c.translate(x, y); c.rotate(math.radians(-a1)); hide(c, [(-.030, -.012), (.030, -.012), (.026, l1 * .55), (.022, l1), (-.022, l1), (-.026, l1 * .55)], skin, .008); hide(c, [(-.034, l1 * .42), (.034, l1 * .42), (.032, l1 * .60), (-.032, l1 * .60)], band, .006, smooth=False); holes(c, [(-.024, l1 * .51), (.024, l1 * .51)], .014, .004)
    c.translate(0, l1); c.rotate(math.radians(-a2)); hide(c, [(-.022, -.01), (.022, -.01), (.018, l2 * .9), (-.018, l2 * .9)], skin, .008); hide(c, [(-.026, l2 * .74), (.026, l2 * .74), (.024, l2 * .90), (-.024, l2 * .90)], band, .006, smooth=False)
    c.translate(0, l2 * .9)
    if hand == 'fist': hide(c, [(-.022, 0), (.024, 0), (.032, .028), (.018, .050), (-.020, .046)], skin, .007)
    elif hand == 'point': hide(c, [(-.018, 0), (.020, 0), (.024, .030), (.010, .095), (.002, .040), (-.016, .042)], skin, .007)
    else: hide(c, [(-.018, 0), (.018, 0), (.034, .030), (.020, .034), (.022, .078), (.008, .046), (.002, .084), (-.008, .046), (-.020, .074), (-.018, .034)], skin, .007)
    c.restore()
    c.save(); c.translate(x, y); c.set_source_rgb(*BK); c.arc(0, 0, .011, 0, 7); c.fill(); c.set_source_rgb(*HOLE); c.arc(0, 0, .004, 0, 7); c.fill(); c.restore()


def figure(c, x, y, s, skin='ochre', cloth='red', sash='green', crown='king', beard=False, flip=False, near=(20, 60, 'open'), far=(10, 40, 'open'), lean=0., bob=0., seated=False, extra=None, smile=.2):
    """a whole puppet standing with its feet at (x, y) px, s px tall"""
    c.save(); c.translate(x, y); c.scale(-s if flip else s, s); c.rotate(math.radians(lean)); c.translate(0, bob)
    c.set_source_rgba(.04, .015, .01, .75); c.set_line_width(.010); c.move_to(0, -.30); c.line_to(.02, .6); c.stroke()                          # rod
    arm(c, -.035, -.655, *far[:2], skin, hand=far[2])
    if extra: extra(c, 'back')
    if not seated:
        for k, (dx, f) in enumerate(((-.055, 1), (.055, 1))):
            hide(c, [(dx - .030, -.20), (dx + .030, -.20), (dx + .022, -.045), (dx + .085, -.018), (dx + .090, 0), (dx - .028, 0)], skin, .008, smooth=False); hide(c, [(dx - .030, -.075), (dx + .028, -.075), (dx + .026, -.050), (dx - .028, -.050)], 'yellow', .006, smooth=False)
        hide(c, [(-.085, -.470), (.085, -.470), (.130, -.300), (.150, -.110), (.085, -.085), (.030, -.105), (0, -.085), (-.040, -.105), (-.100, -.085), (-.135, -.115), (-.118, -.300)], cloth, .010)
        holes(c, [(-.128, -.135), (-.06, -.118), (0, -.118), (.07, -.118), (.140, -.130)], .020, .0060); holes(c, [(-.126, -.168), (0, -.150), (.138, -.164)], .030, .0045); slits(c, -.075, .080, -.430, -.200, 9, HOLE, .004)
        for u in (-.07, .0, .07): rosette(c, u * 1.2, -.195, .020, 6)
        hide(c, [(-.022, -.470), (.030, -.470), (.050, -.150), (.004, -.120), (-.030, -.160)], sash, .008); holes(c, [(.004, -.44), (.010, -.17)], .022, .0055)
    else:
        hide(c, [(-.11, -.30), (.10, -.31), (.22, -.22), (.23, -.10), (.10, -.06), (-.14, -.07), (-.17, -.16)], cloth, .010); holes(c, [(-.13, -.11), (.0, -.10), (.19, -.12)], .020, .0058); slits(c, -.08, .14, -.28, -.15, 9)
    k = 0 if not seated else .18
    c.translate(0, k)
    hide(c, [(-.080, -.480), (.080, -.480), (.072, -.560), (.104, -.660), (.060, -.700), (0, -.706), (-.060, -.700), (-.104, -.660), (-.072, -.560)], skin, .010)
    hide(c, [(-.090, -.500), (.090, -.500), (.094, -.462), (-.094, -.462)], 'yellow', .007, smooth=False); holes(c, [(-.080, -.481), (.080, -.481)], .020, .0058)
    for r in (.050, .078): holes(c, [(-r, -.690), (-r * .72, -.690 + r * .85), (0, -.690 + r * 1.2), (r * .72, -.690 + r * .85), (r, -.690)], .014, .0046)
    rosette(c, 0, -.575, .026, 8)
    hide(c, [(-.100, -.680), (-.060, -.705), (.090, -.500), (.060, -.486)], sash, .007, smooth=False); holes(c, [(-.078, -.686), (.074, -.498)], .022, .0045)
    c.save(); c.translate(0, -.715); head(c, skin, crown, beard, smile=smile); c.restore()
    if extra: extra(c, 'front')
    arm(c, .045, -.655, *near[:2], skin, hand=near[2]); c.restore()


def bow(c, x, y, r, pull, ang=0.):
    """a toy bow whose grip is at (x,y), pointing +x"""
    c.save(); c.translate(x, y); c.rotate(ang); c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_source_rgb(*BK); c.set_line_width(.030); c.move_to(-r * .35, -r); c.curve_to(r * .28, -r * .55, r * .28, r * .55, -r * .35, r); c.stroke(); c.set_source_rgb(*DYE['yellow']); c.set_line_width(.016); c.move_to(-r * .35, -r); c.curve_to(r * .28, -r * .55, r * .28, r * .55, -r * .35, r); c.stroke()
    c.set_source_rgb(*BK); c.set_line_width(.006); c.move_to(-r * .35, -r); c.line_to(-r * .35 - pull, 0); c.line_to(-r * .35, r); c.stroke(); c.restore()


def fire(c, x, y, s, t, seed=0):
    """a leather fire: three dyed tongues that jerk on twos"""
    for k, (col, h, w) in enumerate((('red', 1., .55), ('rose', .74, .40), ('yellow', .48, .26))):
        a = .10 * math.sin(t * 9 + k + seed) + .06 * math.sin(t * 17 + k * 2); P = [(-w, 0), (-w * .85, -h * .35), (-w * .30 + a, -h * .55), (-w * .42 + a, -h * .82), (a * 1.6, -h), (w * .22 + a, -h * .70), (w * .62, -h * .52), (w * .88, -h * .24), (w, 0)]
        hide(c, [(x + px * s, y + py * s) for px, py in P], col, s * .022)
    holes(c, [(x - .18 * s, y - .12 * s), (x, y - .20 * s), (x + .18 * s, y - .12 * s)], s * .06, s * .018)


def altar(c, x, y, s):
    hide(c, [(x - .62 * s, y), (x + .62 * s, y), (x + .48 * s, y - .12 * s), (x + .58 * s, y - .22 * s), (x - .58 * s, y - .22 * s), (x - .48 * s, y - .12 * s)], 'brown', s * .022, smooth=False); holes(c, [(x - .5 * s, y - .17 * s), (x + .5 * s, y - .17 * s)], s * .075, s * .020); rosette(c, x, y - .07 * s, s * .05, 8)
