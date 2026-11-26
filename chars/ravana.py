"""Ravana: king, scholar, tyrant.  Ten heads (uniform fan), twenty arms (uniform arms)."""
import numpy as np, math
from lau.stage import Fig, Light
from lau.face import human, Face, Pen
from lau.rig import Pose, V, nz
from lau import gl

MAIN = 4                                # index of the main head in alive / eyeglow / lids / mouths; 0 = his far right (screen left), 9 = his far left
SKIN = ('#5f4374', '#26143e', 1)
PAL = {1: SKIN, 2: ('#120c16', '#060409', 5), 3: ('#f2dcb4', '#805030', 2), 4: ('#c4142c', '#54081c', 3), 5: ('#0f7a58', '#063a34', 3), 6: ('#f5ead2', '#a88a8c', 1), 7: ('#a3121f', '#420616', 8), 8: ('#c01c24', '#520a1a', 8), 9: ('#d6a868', '#805030', 2),
       10: ('#b4bccb', '#4a5464', 7), 11: ('#5a2a18', '#24100c', 1), 12: ('#ff9030', '#ff9030', 4), 13: SKIN, 15: ('#dcb070', '#805030', 2), 16: ('#7a1420', '#300812', 1), 17: ('#140c14', '#070408', 5)}
BOX = (-1.1, -1.25, 1.1, .95)
STYLE = dict(iris='#c87a1c', iris2='#4a1006', sclera='#fff0d2', lip='#6e2036', lip2='#8c3044', liphi='#d88a86', kohl='#0c0414', kohlk=1.2, brow='#0c0610', browt=2.3, browy=.015, tilak='none', size=1.10, nose='#150a22', mouthw=1.3, tilt=.07)


def _paint(P, F, k):
    """three ash bars and the third-eye mark, lines of age and rule"""
    for i in range(3):
        y = .425 + .088 * i; w = .40 - .03 * i
        P.line([(-w, y - .035), (-w * .4, y + .02, w * .4, y + .02, w, y - .035)], .05, '#efe6d6', .96)
        P.line([(-w * .9, y - .05), (-w * .4, y, w * .4, y, w * .9, y - .05)], .008, '#8a7a90', .6)
    P.fill([(0, .335), (.055, .40, .05, .47, 0, .575), (-.05, .47, -.055, .40, 0, .335)], '#c8141e'); P.fill([(0, .37), (.025, .41, .022, .45, 0, .50), (-.022, .45, -.025, .41, 0, .37)], '#ffb43a')
    P.c.save()
    for sd in (1, -1):
        P.c.save(); P.c.scale(sd, 1)
        P.line([(.20, -.115), (.29, -.165, .40, -.15, .49, -.07)], .012, k['nose'], .55)                # under the eye
        P.line([(.195, -.36), (.27, -.42, .32, -.50, .33, -.60)], .014, k['nose'], .65)                  # cheek fold
        if F.frown > .15: P.line([(.075, .14), (.07, .19, .075, .24, .10, .30)], .014, k['nose'], .7)
        P.c.restore()
    P.c.restore()


def face(F): return human(F.set(frown=min(1.2, .22 + .78 * F.frown)), STYLE, extra=_paint)


def _glow(lid):
    """burning eyes: fire inside the eye opening"""
    import cairo
    S = 400; P = Pen(S, BOX); c = P.c
    if lid > .06:
        up = -.035 + .20 * lid; lo = -.062
        for sd in (1, -1):
            c.save(); c.scale(sd, 1); c.translate(.33, .03); c.rotate(STYLE['tilt']); c.translate(-.33, -.03)
            eye = [(.125, -.02), (.19, up * .75 - .005, .27, up + .015, .345, up), (.43, up - .02, .49, .085 * (.3 + .7 * lid), .545, .075 * (.3 + .7 * lid)), (.47, .005, .40, lo, .31, lo - .004), (.24, lo, .18, -.035, .125, -.02)]
            P.path(eye, True); c.clip()
            g = cairo.RadialGradient(.335, .03, .0, .335, .03, .24); [g.add_color_stop_rgb(s, *q) for s, q in ((0, (1, .95, .66)), (.22, (1, .74, .24)), (.5, (1, .40, .07)), (1, (.66, .08, .02)))]; c.set_source(g); c.paint()
            
            c.restore()
    return P.out()


_cells = None


def cells():
    """atlas 5 x 4: columns lids 0 .25 .5 .75 1; top row mouth shut, then half, then laughing; bottom row the burning eyes"""
    global _cells
    if _cells is None:
        S = 400; A = np.zeros((4 * S, 5 * S, 4), np.uint8)
        for j in range(5):
            L = j / 4
            for i, (mo, te, sm, fr) in enumerate(((0, 0, -.05, .30), (.45, .3, .45, .35), (1., .55, .9, .45))):
                A[i * S:(i + 1) * S, j * S:(j + 1) * S] = human(Face(lid=L, mouth=mo, teeth=te, smile=sm, frown=fr), STYLE, S=S, extra=_paint)
            A[3 * S:, j * S:(j + 1) * S] = _glow(L)
        _cells = gl.tex_from(A); _cells.swizzle = 'BGRA'
    return _cells


class _RFig(Fig):
    def facetex(self, face):
        cells().use(15)                 # a texture unit the engine never binds
        return super().facetex(face)


_U = dict(tCells=15, fan=0., arms=0., armT=0., navel=0., hair=1., spread=1., mantle=1., armTop=1.3, alive=np.ones(10, 'f4'), eyeglow=np.zeros(10, 'f4'), lids=np.ones(10, 'f4'), mouths=np.zeros(10, 'f4'))
DIM = dict(chest=3.45, shx=1.75, shy=1.12, neck=1.46, head=1.84, up=3.0, fore=2.7, hipx=.80, th=4.05, sh=3.85, hand=1.18, foot=1.28)
BUILD = dict(chest=1.42, depth=1.32, rib=1.52, waist=1.42, hips=1.22, arm=1.40, leg=1.32, hand=1.08, belly=.35, neck=1.42, shoulder=1.30)
RAVANA = _RFig('ravana', 'ravana.glsl', PAL, dim=DIM, build=BUILD, hs=[1] * 8, face=face, bound=(0, 9, 0, 24), step=.82, u=_U)
HEAD = _RFig('ravana_head', 'ravana.glsl', PAL, dim=DIM, build=BUILD, hs=[1] * 8, face=face, step=.82, u={**_U, 'bound': (0, 1.1, 0, 2.6)}, defs='#define HEADONLY')      # one loose head, origin at the centre of the skull (faces +z); st.fig(HEAD, M=..., face=...)
S0 = 1.30


def _ten(v): return np.full(10, v, 'f4') if np.ndim(v) == 0 else np.asarray(v, 'f4')


def heads(S, fan=1., spread=1.):
    """[(world centre of the skull, scale, 3x3 world rotation whose rows are the head's x y z)] for the ten heads, the same layout the shader uses"""
    Bh, Bc = S.u['Bh'], S.u['Bc']; J3 = S.J[3]; rZ = nz(.45 * Bc[2] + .55 * Bh[2]); rX = nz(.6 * Bc[0] + .4 * Bh[0]); rY = nz(np.cross(rZ, rX)); rX = np.cross(rY, rZ); Rw = S.Mf[:3, :3] / S.Sc
    out = [None] * 10; out[MAIN] = (S.w(J3), S0 * S.Sc, Bh @ Rw.T); x = [0., 0.]; pv = [S0, S0]
    for n in range(1, 6):
        for s in (0, 1):
            k = MAIN + (n if s else -n)
            if k < 0: continue
            sc = (1.06 - .083 * n) if s else (1.08 - .085 * n); x[s] += (.725 if s else .785) * spread * (pv[s] + sc); pv[s] = sc; e = 1 - (1 - min(1., max(0., fan * 1.35 - .07 * n))) ** 2.2; sg = 1 if s else -1
            p = V(sg * x[s] * e, (.04 + .02 * n - .02 * n * n) * e - .25 * (1 - e), -.22 * n * e - .34); a = sg * (.05 + .080 * n) * e; c, d = math.cos(a), math.sin(a); B = np.stack([rX, rY, rZ]); R = np.array([[c, 0, -d], [0, 1, 0], [d, 0, c]]) @ B
            out[k] = (S.w(J3 + p @ B), sc * (.55 + .45 * e) * S.Sc, R @ Rw.T)
    return out


def eye_points(S, fan=1., out=.72, spread=1.):
    """10 x 2 x 3 world points just in front of every eye (his right eye first)"""
    return np.array([[c + sc * (V(sx * .345, .05, out + .12) @ R) for sx in (-1, 1)] for c, sc, R in heads(S, fan, spread)])


def bound(S, fan=0., arms=0., spread=1.):
    """sphere round the posed figure for u['bound'] (figure space)"""
    Bh, Bc = S.u['Bh'], S.u['Bc']; P = [S.J, S.J[3] + V(0, 4.6, 0) @ Bh]
    if fan > 0: P += [S.J[3] + np.array([(x * max(1., spread), y, -1.6) for x, y in ((7., -1.6), (-7., -1.6), (6.5, 2.2), (-6.5, 2.2))]) @ (.5 * Bh + .5 * Bc)]
    if arms > 0: a = np.radians(np.arange(0, 360, 30)); P += [S.J[1] + (np.stack([np.cos(a) * 11.6, np.sin(a) * 10.5 + .8, -.8 + 0 * a], 1)) @ Bc]
    P = np.vstack(P); P = P[P @ V(0, 1, 0) > -3]; c = (P.min(0) + P.max(0)) / 2; return (*c, float(np.linalg.norm(P - c, axis=1).max()) + 1.2)


def fig(st, pose, at=(0, 0, 0), yaw=0., fan=0., arms=0., armT=None, alive=1., eyeglow=0., lids=1., mouths=0., navel=0., hair=1., spread=1., mantle=1., armTop=1.3, face=None, fig=None, u=None, **k):
    """draw Ravana with the right bounding sphere.  alive, eyeglow, lids, mouths: a number or ten (index 4 = main head).  The main head shows `face`, with lids[4] and mouths[4] folded into it."""
    f = fig or RAVANA; face = face or Face(smile=0., frown=.2); L, M = _ten(lids).copy(), _ten(mouths).copy()
    face = face.set(lid=round(float(face.lid * L[MAIN]), 2), mouth=round(max(face.mouth, float(M[MAIN])), 2), teeth=max(face.teeth, round(.55 * float(M[MAIN]), 2)), smile=max(face.smile, round(.9 * float(M[MAIN]), 2)) if M[MAIN] > 0 else face.smile); L[MAIN] = 1.; M[MAIN] = 0.
    from lau.stage import model
    S = st.fig(f, pose, at=at, yaw=yaw, draw=False, **{q: k[q] for q in ('pitch', 'roll', 'scale', 'M') if q in k})
    U = dict(fan=float(fan), arms=float(arms), armT=float(st.t if armT is None else armT), alive=_ten(alive), eyeglow=_ten(eyeglow), lids=L, mouths=M, navel=float(navel), hair=float(hair), spread=float(spread), mantle=float(mantle), armTop=float(armTop), bound=bound(S, fan, arms, spread), **(u or {}))
    if face.lid < 1 and U['eyeglow'][MAIN] > 0: U['lids'][MAIN] = face.lid if face.mouth < .02 else 1.
    return st.fig(f, pose, at=at, yaw=yaw, face=face, u=U, **k)


SHADOW = dict(fan=1., arms=1., spread=1.5, mantle=0., armTop=.15)                      # the layout that reads as a pure shadow: heads wide apart on long necks, arms below them


def silhouette(col='#000000', ink=2.2, inkRef=1.):
    """a Light that turns everything drawn under it into one flat colour (fire-coloured eyes still burn): st.open(cam, RV.silhouette('#1a0608')) ... st.close(alpha=.85)"""
    return Light(keyCol=(0, 0, 0), amb=(0, 0, 0), rimCol=(0, 0, 0), bounceCol=(0, 0, 0), envT=(0, 0, 0), envM=(0, 0, 0), envB=(0, 0, 0), shadow=False, ink=ink, inkCol=col, fogCol=col, fog=(1e4, 0, 0, 0), pig=0., inkRef=inkRef)


def shadow_tex(st, draw, cam, key='ravana', w=1024, h=576):
    """bake the silhouette of draw(st) seen from cam into a texture (rgb 1, alpha = coverage) for a shadow painted on scenery: st.mesh(kind=3, texs=dict(tCard=tex), col=(shadow colour, ..), cls=6, ink=0) or a world shader.
    Call before st.clear() of the frame or in setup (it uses the stage's own buffers)."""
    import moderngl as mgl
    st.open(cam, silhouette('#ffffff')); draw(st); st.close(alpha=0.)
    t = _tex.get((key, w, h))
    if t is None: c = gl.ctx(); t = _tex[(key, w, h)] = c.texture((w, h), 4, dtype='f1'); t.repeat_x = t.repeat_y = False; _fbo[(key, w, h)] = c.framebuffer([t])
    fb = _fbo[(key, w, h)]

    class T: width, height = w, h; use = staticmethod(fb.use)
    gl.draw(gl.program('in vec2 uv;out vec4 o;uniform sampler2D tex;\nvoid main(){float a=0.;vec2 p=1./vec2(textureSize(tex,0));for(int j=0;j<2;j++)for(int i=0;i<2;i++)a+=texture(tex,uv+(vec2(i,j)-.5)*p).a*.25;o=vec4(a);}\n'), T, {}, dict(tex=st.L.color_attachments[0]))
    t.build_mipmaps(); t.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)
    return t


_tex, _fbo = {}, {}


def cape(st, S, t=0., length=10.2, wind=(0, 0, -.12), col=('#8e0f1e', '#380512', '#d8982c'), flow=1.):
    """a crimson cape with a gold border from the shoulders down his back; wind in world units of `length`"""
    from lau import cloth as CL
    A, B = S.chest((2.2, 1.42, -.95)), S.chest((-2.2, 1.42, -.95)); bk = -S.d(S.u['Bc'].T @ V(0, 0, 1)); sd = nz(B - A); L0 = length * S.Sc; w = np.asarray(wind, float); dn = V(0, -1, 0)

    def pt(v, u):
        c = u - .5; L = L0 * (.95 + .07 * math.cos(c * math.pi)); fold = math.sin(c * 21 + .7 * math.sin(t * 1.7 + v * 2.)) * (.10 + .34 * v) + .25 * v * math.sin(t * 2.6 - v * 4.2 + c * 3) * flow
        p = A + (B - A) * u + bk * S.Sc * (.55 * math.cos(c * math.pi) + .30 * v + fold) + sd * c * 3.2 * v ** 1.1 * S.Sc
        p = p + dn * L * v + w * L * v ** 1.5 + sd * .12 * L * v * v * math.sin(t * 1.9 - v * 3.) * flow * .4
        p[1] = max(p[1], S.Mf[1, 3] + .06 + .04 * abs(c)); return p
    st.mesh(*CL.sheet(pt, 30, 40), kind=2, col=col, cls=8, u=dict(rep=(11., 12., 0., 0.)))


def hold(st, S, prop, side='R', scale=1., tilt=0.):
    """put a sword, mace or spear (lau.props, long axis +y) in a hand"""
    from lau import props as PR
    y = S.hand(side, (1 if side == 'R' else 1, tilt, 0)); return st.fig(prop, M=PR.place(S.palm(side, .0, .62, .28), y, S.hand(side, (0, 1, 0)), S.Sc * scale))


# ------------------------------------------------------------------ poses
_FT = dict(lf=(1.5, .98, .5), rf=(-1.5, .98, .2), lft=(26, 0), rft=(-26, 0), lkn=(.25, 0, 1), rkn=(-.25, 0, 1))
R_STAND = Pose(pel=(0, 8.55, 0), pelr=(0, -2, 0), cher=(0, -3, 0), hedr=(0, 4, 0), lh=(2.62, 9.75, .75), rh=(-2.62, 9.75, .75), lel=(1, .1, -.45), rel=(-1, .1, -.45), lhand='fist', rhand='fist', lfing=(-.75, -.35, .55), rfing=(.75, -.35, .55), lpalm=(-.4, -.3, -.8), rpalm=(.4, -.3, -.8), **_FT)
R_EASE = Pose(pel=(.2, 8.45, 0), pelr=(6, 0, 3), cher=(-4, -3, -5), hedr=(-4, 4, 3), **{**_FT, 'rf': (-1.6, .98, 1.0)}, lh=(2.62, 9.75, .75), lel=(1, .1, -.45), lhand='fist', lfing=(-.75, -.35, .55), lpalm=(-.4, -.3, -.8), rh=(-4.5, 11.2, 2.6), rel=(-.7, -1, -.3), rhand='katak', rfing=(-.2, .8, .6), rpalm=(0, .5, 1))
R_LOOM = Pose(pel=(0, 8.1, -.5), pelr=(0, 8, 0), cher=(0, 24, 0), hedr=(0, -14, 0), lh=(6.6, 12.6, 3.0), rh=(-6.6, 12.6, 3.0), lel=(.6, .8, -.6), rel=(-.6, .8, -.6), lhand='claw', rhand='claw', lfing=(.35, -.35, .85), rfing=(-.35, -.35, .85), lpalm=(-.3, -.8, .35), rpalm=(.3, -.8, .35), **{**_FT, 'lf': (1.9, .98, 1.2), 'rf': (-1.9, .98, -.2)})
R_THRONE = Pose(pel=(0, 4.75, -.6), pelr=(0, -5, 0), cher=(0, -2, -3), hedr=(0, 6, 3), lf=(1.9, .98, 3.5), rf=(-1.9, .98, 3.1), lkn=(.35, .6, 1), rkn=(-.35, .6, 1), lft=(20, 0), rft=(-20, 0), lh=(3.7, 6.1, 2.2), rh=(-3.3, 5.75, 2.5), lel=(1, .2, -.5), rel=(-1, .2, -.5), lhand='fist', rhand='relax', lfing=(.1, -.1, 1), rfing=(.2, -.2, 1), lpalm=(-.2, -1, 0), rpalm=(.1, -1, 0))
R_LAUGH = R_STAND.set(pelr=(0, -6, 0), cher=(0, -9, 0), hedr=(0, -13, 0), shrug=(.35, .35))
R_STRUCK = Pose(pel=(0, 7.9, .9), pelr=(0, -14, 0), cher=(4, -18, 4), hedr=(4, -8, 5), lh=(6.4, 14.6, -2.4), rh=(-6.2, 13.6, -2.6), lel=(.3, -.6, -.8), rel=(-.3, -.6, -.8), lhand='open', rhand='open', lfing=(.7, .6, .2), rfing=(-.8, .4, .2), lpalm=(0, .1, 1), rpalm=(0, .1, 1), lf=(1.9, .98, 1.6), rf=(-1.8, 1.0, -1.6), lft=(24, 0), rft=(-34, 18), lkn=(.3, 0, 1), rkn=(-.4, 0, 1))


def R_ARCHER(draw=1.):
    d = draw
    return Pose(pel=(-.15, 8.0, 0), pelr=(18, 0, 0), cher=(-20, 0, 1), hedr=(72, 2, 0), shrug=(.1, .35), lh=(7.75, 13.35, .85), rh=(1.6 - 2.9 * d, 13.55, 1.75), lel=(0, -1, -.35), rel=(-1, .35, -.25), lhand='grip', rhand='draw',
                lfing=(.35, .1, .95), lpalm=(.9, -.1, -.4), rfing=(.80, .05, .55), rpalm=(.25, -.1, -1), lf=(2.7, .98, .6), rf=(-2.7, .98, -.3), lft=(72, 0), rft=(-8, 0), lkn=(.9, 0, .6), rkn=(-.5, 0, 1))


_SW = [(0., Pose(pel=(0, 8.2, 0), pelr=(-14, 0, 0), cher=(-24, -6, 0), hedr=(26, 4, 0), rh=(-3.6, 16.3, -1.2), rel=(-1, .2, -.4), rhand='grip', rfing=(-.2, .3, -.9), rpalm=(.4, .9, .2), lh=(4.2, 11.6, 2.4), lel=(.8, -.6, -.3), lhand='claw', **{**_FT, 'lf': (1.9, .98, 1.6), 'rf': (-1.9, .98, -1.4)})),
       (.45, Pose(pel=(0, 7.8, .5), pelr=(6, 6, 0), cher=(10, 12, 0), hedr=(-4, 0, 0), rh=(-1.6, 13.0, 5.4), rel=(-1, .1, -.3), rhand='grip', rfing=(.2, -.2, .95), rpalm=(.9, -.3, -.2), lh=(4.4, 10.6, -.6), lel=(.8, -.4, -.6), lhand='claw', **{**_FT, 'lf': (1.9, .98, 2.2), 'rf': (-1.9, .98, -1.4)})),
       (1., Pose(pel=(0, 7.5, .8), pelr=(20, 10, 0), cher=(26, 18, 0), hedr=(-18, -8, 0), rh=(3.6, 8.4, 4.2), rel=(-.8, .3, .2), rhand='grip', rfing=(.8, -.4, .3), rpalm=(.2, -.6, -.8), lh=(4.6, 10.4, -1.8), lel=(.8, -.2, -.8), lhand='claw', **{**_FT, 'lf': (1.9, .98, 2.4), 'rf': (-1.9, .98, -1.6)}))]


def R_SWORD(t):
    """0 wound up over the shoulder, .45 the blow, 1 follow-through"""
    for (a, A), (b, B) in zip(_SW, _SW[1:]):
        if t <= b: return A.mix(B, max(0., (t - a) / (b - a)))
    return _SW[-1][1]
