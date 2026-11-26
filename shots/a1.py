"""a1 (72): black, one breath, a spark falls on a wick (f24), the flame stands up (f36)."""
from lau.shot import *

WICK = V(3.05, .92, 0)


def lamp_light(amt, t, seed=0.):
    """flicker of one flame: multiplier"""
    return amt * (1 + .06 * noise1(t * 9, seed) + .05 * noise1(t * 21, seed + 3))


class Shot(ShotBase):
    id = 'a1'; n = 72
    EVENTS = [(2, 'breath in', dict(soft=1)), (13, 'spark falls', {}), (24, 'spark lands', {}), (33, 'flame catches', {}), (36, 'flame stands', {}), (40, 'lamp bed', dict(dur=32))]

    def frame(self, f, st):
        st.clear('#000000', f=f); t = st.t
        k = smoother(0, 72, f); e = ease_io(f / 71, 1.6)
        eye = np.array(lerp(V(4.3, 1.75, 6.6), V(1.2, 3.35, 15.2), e)); at = np.array(lerp(V(2.75, 1.25, 0), V(.9, 1.75, 0), e))
        cam = Cam(eye, at, lerp(19, 25, e)); st.cam = cam
        up = keys(f, [(32, 0.), (36, 1.22, 'out'), (40, .88), (45, 1.06), (50, 1.)]) if f >= 32 else 0.
        ember = keys(f, [(23, 0.), (24, 1.), (32, .75), (38, .15), (44, 0.)]) if f >= 23 else 0.
        I = lamp_light(up, t, 2.) * 1.0 + .10 * ember + .5 * decay((f - 24) / 24., 9) * (f >= 24)
        # the falling spark lights the brass a little as it comes
        fall = clamp((f - 10) / 14.); sp = V(3.05 - .9 * (1 - fall) ** 1.5 + .10 * math.sin(f * .9) * (1 - fall), .98 + 5.2 * (1 - fall ** 1.7), .3 * (1 - fall))
        pts = []
        if I > .004: pts.append((WICK + V(.05, 1.15 * max(up, .25), .1), 3.0, tuple(np.array([1.25, .62, .24]) * I)))
        if 10 <= f < 24: pts.append((sp, 1.1, (.9, .36, .10)))
        if pts:
            L = Light(key=(0, 1, 0), keyCol=(0, 0, 0), amb=(.006, .005, .010), rim=(.2, .2, -1), rimCol=(0, 0, 0), bounceCol=(0, 0, 0), pts=pts, shadow=False, envT='#ffb060', envM='#ff9a40', envB='#6a2a14', ink=2.6, inkRef=.35, inkCol='#060204', hi=.2, stip=.1)
            st.open(cam, L, far=200.); st.world('lamp.glsl', u=dict(clothZ=-13., glowW=float(max(ember, .8 * (up > 0))), glowL=float(max(I, .12 * ember + .05))))
            st.close()
        if up > .02:
            FX.flame(st, WICK + V(.02, -.06, 0), 2.35 * up, seed=1.3, glow=.75 * min(1, up), calm=1.2 - .5 * k)
            FX.embers(st, 10, ((2.9, 1.6, -.1), (3.2, 2.2, .1)), t, rise=1.6, size=.035, seed=4, life=2., swirl=.25)
        if 9 <= f < 25:
            tr = np.array([V(3.05 - .9 * (1 - u) ** 1.5 + .10 * math.sin((10 + 14 * u) * .9) * (1 - u), .98 + 5.2 * (1 - u ** 1.7), .3 * (1 - u)) for u in np.linspace(max(0, fall - .16), fall, 12)])
            FX.ribbon(st, tr, np.linspace(.004, .03, 12), 'light', '#ff7a2a', '#ffe0a0'); FX.particles(st, sp[None], .16, '#ffb050', 'glint')
        if 24 <= f < 44: FX.burst(st, 26, WICK + V(0, .05, 0), (f - 24) / 24., speed=2.6, grav=4., size=.022, seed=3, col='#ffb050', life=.6, up=.5)
        if f > 40: IM.dof(st, float((WICK - eye) @ cam.R[2]), 7., 7.)
        return st.finish(bloom=.42, thr=.95, vig=.55, grain=.018, contrast=1.06, fade=1 - smooth(0, 10, f) if f < 10 else 0.)
