"""Devanagari drawn as brush strokes (no fonts).  Each glyph: strokes of points in a box 1 unit high, head-line (shirorekha) at y=0, y down; width = advance."""
import numpy as np, math
from .cloth import spline
G = {
    # र
    'ra': (.62, [[(.14, .02), (.36, .06), (.44, .20), (.34, .34), (.16, .37)], [(.16, .37), (.28, .48), (.40, .66), (.52, .88)]]),
    # ा (aa matra)
    'aa': (.30, [[(.15, 0), (.15, .5), (.15, .92)]]),
    # म
    'ma': (.80, [[(.14, .0), (.14, .28), (.14, .56)], [(.14, .56), (.06, .60), (.05, .70), (.14, .72), (.22, .64), (.24, .55), (.42, .56), (.62, .56)], [(.62, 0), (.62, .5), (.62, .92)]]),
    # य
    'ya': (.80, [[(.12, .06), (.26, .10), (.28, .26), (.16, .36), (.10, .48), (.22, .62), (.42, .60), (.62, .42)], [(.62, 0), (.62, .5), (.62, .92)]]),
    # ण
    'nna': (.92, [[(.12, 0), (.12, .28), (.16, .46), (.26, .52), (.36, .44), (.40, .28), (.40, 0)], [(.40, .0), (.40, .30), (.40, .50)], [(.74, 0), (.74, .5), (.74, .92)]]),
    # ल
    'la': (.86, [[(.215, .63), (.13, .66), (.055, .55), (.075, .37), (.20, .275), (.32, .345), (.365, .50), (.335, .70), (.245, .87)], [(.355, .46), (.43, .325), (.54, .285), (.63, .33), (.68, .43)], [(.68, 0), (.68, .5), (.68, .92)]]),
    # ौ (au matra): bar with two flags above the head line
    'au': (.34, [[(.15, 0), (.15, .5), (.15, .92)], [(.15, 0), (.10, -.16), (-.04, -.30), (-.22, -.36)], [(.15, 0), (.20, -.20), (.10, -.42), (-.10, -.52)]]),
    # ी not needed; श्री kept out on purpose
    'ii': (.30, [[(.15, 0), (.15, .5), (.15, .92)], [(.15, 0), (.10, -.26), (-.12, -.34), (-.32, -.22), (-.36, 0)]]),
    'da': (.60, [[(.36, 0), (.36, .14), (.20, .18), (.10, .34), (.18, .52), (.34, .54), (.42, .46)], [(.34, .54), (.40, .70), (.54, .86)]]),
    'pa': (.80, [[(.14, 0), (.14, .30), (.20, .46), (.38, .50), (.62, .42)], [(.62, 0), (.62, .5), (.62, .92)]]),
}
WORDS = dict(ram=['ra', 'aa', 'ma'], ramayan=['ra', 'aa', 'ma', 'aa', 'ya', 'nna'], lau=['la', 'au'], dip=['da', 'ii', 'pa'])


def strokes(word, n=28, headline=True):
    """-> list of (k,2) polylines in units of letter height, plus total width; head line last"""
    out, x = [], 0.
    for g in WORDS.get(word, word):
        w, S = G[g]
        for s in S: out.append(spline(np.array(s, float), n) + [x, 0])
        x += w
    if headline: out.append(np.stack([np.linspace(-.02, x - .08, n), np.zeros(n)], 1))
    return out, x


def points(word, spacing=.05):
    """evenly spaced points along all strokes (for lamps, stars, stones)"""
    S, w = strokes(word, 120); P = []
    for s in S:
        d = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(s, axis=0), axis=1))]); m = max(2, int(d[-1] / spacing)); q = np.linspace(0, d[-1], m); P.append(np.stack([np.interp(q, d, s[:, 0]), np.interp(q, d, s[:, 1])], 1))
    return np.vstack(P), w


def draw(c, word, x, y, h, col=(1, 1, 1), w=.11, upto=1., alpha=1., nib=-47.):
    """a broad reed pen held at a constant angle; upto 0..1 writes the word progressively.  (x, y) = left end of the head line, h = letter height in user units"""
    S, tot = strokes(word, 64); L = [np.linalg.norm(np.diff(s, axis=0), axis=1).sum() for s in S]; T = sum(L) * upto; c.set_source_rgba(*col, alpha)
    n = np.array([math.cos(math.radians(nib)), math.sin(math.radians(nib))]) * w * h * .56; acc = 0; c.push_group(); c.set_line_cap(0); c.set_line_join(1); c.set_source_rgba(*col, 1.)
    for s, l in zip(S, L):
        if acc >= T: break
        k = min(1., (T - acc) / l); acc += l; P = s[:max(2, int(len(s) * k))] * h + [x, y]; c.new_path()
        for p, q in zip(P, P[1:]):
            A = [p - n, p + n, q + n, q - n]; d = sum(A[i][0] * A[(i + 1) % 4][1] - A[(i + 1) % 4][0] * A[i][1] for i in range(4))
            if d < 0: A = A[::-1]
            c.move_to(*A[0]); [c.line_to(*v) for v in A[1:]]; c.close_path()
        c.fill(); c.set_line_width(w * h * .34); c.move_to(*P[0]); [c.line_to(*v) for v in P[1:]]; c.stroke()
    c.pop_group_to_source(); c.paint_with_alpha(alpha)
    return tot * h
