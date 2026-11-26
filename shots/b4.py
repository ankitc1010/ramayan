"""b4 (36): Panchavati at night.  A leaf hut, a small fire (the flame of the film), three faces lit from below, fireflies, stars through leaves.  Lakshmana finishes a story; Sita smiles."""
from shots.forest_kit import *

F0 = V(16., .0, 20.)                                        # the hearth of worlds/hut.glsl


def seat(side=1, lean=8., knee=1.0):
    """cross-legged on the ground"""
    return Pose(pel=(0, 1.22, -.1), pelr=(0, -4, 0), cher=(0, lean, 0), hedr=(0, 2, 0), lf=(-1.15, .58, 1.55), rf=(1.15, .74, 1.9), lkn=(1, .16, .42), rkn=(-1, .16, .42), lft=(-84, 34), rft=(84, 34),
                lh=(1.9, 2.1, 2.5), rh=(-1.9, 2.1, 2.5), lel=(1, .1, -.5), rel=(-1, .1, -.5), lfing=(.2, -.5, 1), rfing=(-.2, -.5, 1), lpalm=(0, -1, -.3), rpalm=(0, -1, -.3))


class Shot(ShotBase):
    id = 'b4'; n = 36
    EVENTS = [(0, 'small fire', dict(dur=36)), (0, 'crickets', dict(dur=36)), (2, 'quiet words', dict(who='Lakshmana', dur=8)), (14, 'she laughs softly', dict(soft=1)), (20, 'ember pops', {})]

    def frame(self, f, st):
        st.clear('#000', f=f); t = st.t; u = f / 35.; g = on2(f); e = ease_io(u, 1.5)
        cam = Cam(lerp(V(27, 6.6, 66), V(20.6, 6.0, 46.5), e), lerp(V(12.6, 13.0, 10), V(15.2, 7.9, 16.5), e), lerp(37, 32, e)); st.cam = cam
        st.paint('sky.frag', **FO.csky('night', starAmt=1.3))
        fl = 1 + .09 * noise1(t * 8, 3) + .05 * noise1(t * 19, 5)
        L = FO.clight('night', key=(.35, .7, -.2), keyCol='#4a62ac', amb='#1e2a5a', rim=(-.2, .6, -.8), rimCol=(0., 0., 0.), pts=[(tuple(F0 + V(0, 2.2, .3)), 8.2, tuple(np.array([1.95, 1.10, .58]) * fl)), (tuple(F0 + V(0, 5., 5)), 7., tuple(np.array([.50, .23, .08]) * fl)), (tuple(F0 + V(-8, 5., -10)), 9., tuple(np.array([.35, .13, .04]) * fl))], shadow=True, ink=3.0, inkRef=1.)
        st.open(cam, L); FO.clearing(st, 'night', fire=.40 * fl, hut=True, rock=False)
        FL.scatter(st, 'shrub', [(x, -.3, -62 - 6 * (i % 2)) for i, x in enumerate(range(14, 120, 8))], 19, season='night', seed=4, tint=(1.0, 1.0, 1.15)); FL.tree(st, 'shrub', (37.5, 0, -9), 13, season='night', seed=1, tint=(1.3, 1.3, 1.4)); FL.tree(st, 'shrub', (47, 0, -16), 12, season='night', seed=0, tint=(1.2, 1.2, 1.3))
        # ------------------------------------ three round the fire
        talk = keys(g, [(0, .2), (4, 1., 'out'), (8, .8), (12, 1.), (18, .0, 'io')]); br = .05 * math.sin(t * 2.2)
        K = seat(lean=10).set(hedr=(-6, -2 + 2 * math.sin(g * .9) * (g < 12), 2), rh=tuple(lerp(V(-1.9, 2.1, 2.5), V(-1.7, 5.2, 2.9), talk)), rhand='open', rfing=tuple(lerp(V(-.2, -.5, 1), V(.1, .6, .8), talk)), rpalm=tuple(lerp(V(0, -1, -.3), V(.4, .9, .1), talk)), rel=(-1, -.7, 0))
        mouth = 0. if g >= 12 else (.0, .35, .12, .4, .15, .3)[(g // 2) % 6]
        fk = Face(lid=.85, smile=.35, mouth=mouth, gx=-.3) if g < 14 else Face(lid=.72, smile=.5, gx=-.3)
        SK = st.fig(rama.LAKSHMANA, K.set(pel=(0, 1.22 + br, -.1)), at=F0 + V(7.6, 0, -1.2), yaw=-72, face=fk)
        a = keys(g, [(10, 0.), (12, -.05), (18, 1.04, 'io'), (22, 1.)])
        P = sita.S_SIT.set(pelr=(-4, 4, 3), cher=(6, 4 + br * 20 - 4 * a, -4), hedr=(lerp(-2, 20, a), lerp(16, 2, a), lerp(0, -5, a)), rh=(-1.0, 2.4, 2.4), lh=(1.5, 2.2, 2.0))
        fs = Face(lid=.55, smile=.2, gy=-.6) if g < 12 else (Face(lid=.8, smile=.45, gx=.45) if g < 18 else Face(lid=.82, smile=.85, gx=.35, squint=.15))
        SS = st.fig(sita.FOREST, P, at=F0 + V(.9, 0, -7.4), yaw=-2, face=fs)
        b = keys(g, [(16, 0.), (18, -.04), (26, 1.03, 'io'), (30, 1.)]); R = seat(lean=12).set(pel=(0, 1.24 - br, -.1), hedr=(lerp(4, 26, b), lerp(10, 4, b), 0), lh=(1.7, 2.3, 2.5), rh=(-.4, 3.4 , 3.2), rhand='hold', rfing=(.3, -.2, 1), rpalm=(0, -.5, .6), rel=(-1, -.2, -.4))
        fr = Face(lid=.6, smile=.3, gy=-.5) if g < 20 else Face(lid=.85, smile=.5, gx=.4)
        SR = st.fig(rama.EXILE.variant(pal={1: ('#3a78d8', '#1c3c90', 1)}), R, at=F0 + V(-7.6, 0, -.6), yaw=74, face=fr)
        stick = SR.palm('R', 0, .7, .2); st.mesh(*CL.tube([stick - V(1.4, -.9, .1), stick, stick + V(2.6, -1.35, .05)], [.10, .09, .07], m=7), kind=0, col=('#5a3420', '#2a140c', '#80502c'), cls=1)
        bow = PR.BOW.variant(u=dict(pr=np.array([1., 4.4] + [0] * 14, 'f4'))); st.fig(bow, M=PR.place(V(6.4, 5.0, 16.6), (.22, 1, -.16), (.9, 0, .5), 1.)); st.fig(PR.QUIVER, M=PR.place(V(4.2, 1.4, 17.4), (-.12, 1, -.2), (0, 0, 1), 1.))
        st.close()
        fx, fy, fh = FX.flame(st, F0 + V(0, .9, 0), 4.6, w=None, seed=1.3, glow=.40 * fl, calm=.85, lean=.05 * math.sin(t * 3))
        r = np.random.default_rng(2); n = 9; an = r.uniform(0, 6.28, n); s = r.uniform(.7, 1.35, n) * (1 + .15 * np.sin(t * 9 + an * 4)); Pf = F0 + np.c_[np.cos(an) * 1.25, .55 + s * .75, np.sin(an) * .7]; FX.particles(st, Pf, s * .8, (1, .95, .9), 'tongue', seed=r.uniform(0, 1, n))
        FX.embers(st, 34, (tuple(F0 + V(-1, 1, -.6)), tuple(F0 + V(1, 2.4, .6))), t, rise=4.2, size=.075, seed=2, life=2.4, swirl=1.1)
        FX.burst(st, 14, F0 + V(.2, 2., .3), (f - 20) / 24., speed=5, grav=4, size=.07, seed=8, col='#ffb050', life=.6, up=1.2)
        # smoke that goes up straight: nothing troubles the air
        Q = np.array([F0 + V(.5 * math.sin(q * 5 - t * 1.6) * q, 5. + 26 * q, -.5 * q) for q in np.linspace(0, 1, 26)]); FX.ribbon(st, Q, np.linspace(.15, 1.5, 26), 'smoke', '#6a7090', '#242c50', seed=3, amt=.20)
        r = np.random.default_rng(5); n = 34; p0 = r.uniform((-16, 2., 2), (46, 17, 38), (n, 3)); ph = r.uniform(0, 6.28, n); P = p0 + np.c_[2.2 * np.sin(t * .8 + ph), 1.1 * np.sin(t * 1.1 + ph * 2), 1.6 * np.cos(t * .7 + ph * 3)]; gl_ = np.clip(np.sin(t * 2.6 + ph * 5) * 1.4 + .3, 0, 1); FX.particles(st, P, .40, '#c8f06a', 'lamp', alpha=gl_ * .9)
        FL.frame(st, 'fg_leaves', -60, -130, .62, 'night', 0, lod=2.2, rot=1.2 * math.sin(t * 1.1)); FL.frame(st, 'fg_leaves', 1990, -110, .66, 'night', 1, lod=2.2, flip=True, rot=-1.2 * math.sin(t * 1.3 + 1)); FL.frame(st, 'fg_grass', 120, 1150, .62, 'night', 0, lod=2.4); FL.frame(st, 'fg_grass', 1800, 1180, .7, 'night', 1, lod=2.4)
        IM.dof(st, float((F0 + V(0, 5, -4) - cam.eye) @ cam.R[2]), 26., 4.)
        return st.finish(bloom=.45, thr=.9, vig=.5, contrast=1.06)
