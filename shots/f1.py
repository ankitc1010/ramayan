"""f1 (96): Lanka's gate in the dark.  Ten pairs of eyes open from the edges inward, one on every pulse (f12 .. f66); the main head is the last.  Nothing moves (f66-71).
f72: ten mouths laugh, twenty arms open like a wheel inside a ring of fire, the gate is thrown wide and the host pours out past him."""
from .f_kit import *
from chars import ravana as RV, rakshasa as RK, vehicles as VH
from worlds import lanka as LK

ORDER = [0, 9, 1, 8, 2, 7, 3, 6, 5, 4]                   # the order in which f10 will put them out
OPEN = {h: 12 + 6 * i for i, h in enumerate(ORDER)}
AT, SC, HIT = V(0, 260., 1184.), 5., 72

GLOW = '''
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform vec2 res,ctr;uniform float fT,amt,rad,rays,wheel;
void main(){vec2 p=(vec2(uv.x*res.x,(1.-uv.y)*res.y)-ctr)/rad;float r=length(p),a=atan(p.y,p.x);float ry=smoothstep(-.2,.3,sin(a*24.+fT*.8))*.6+smoothstep(.2,.5,sin(a*10.-fT*.5))*.6;
 vec3 c=hex(0xff6a1c)*(exp(-r*r*2.2)*.75+exp(-r*2.6)*.20)+hex(0xffa03a)*ry*rays*exp(-r*1.7)*.55;
 for(int i=0;i<3;i++){float R=.92+.15*float(i);float n=40.+12.*float(i);float w=abs(fract(a*n/TAU+.5*float(i)+fT*.05*(float(i)-1.))-.5);float d=abs(r-R-.035*cos(w*PI))-.004;c+=hex(0xffc46a)*smoothstep(.006,.0,d)*.55*wheel;float b=length(vec2(w*TAU/n*R,r-R-.075));c+=hex(0xffd890)*smoothstep(.011,.004,b)*.6*wheel;}
 o=vec4(c*amt,0.);}
'''


def stair_y(z): return np.where(z < 1180, 260., 260. - .27 * (z - 1180)) + .6


LAUGH = RV.R_STAND.set(pelr=(0, -4, 0), cher=(0, -8, 0), hedr=(0, 8, 0), shrug=(.4, .4))


class Shot(ShotBase):
    id = 'f1'; n = 96
    EVENTS = [(0, 'deep fire drone', dict(dur=72))] + [(OPEN[h], 'eye opens', dict(k=i)) for i, h in enumerate(ORDER)] + [(66, 'silence', dict(dur=6)), (72, 'ten mouths laugh', dict(dur=24)), (72, 'gate thrown open', {}), (72, 'fire bursts up', {}), (74, 'arms and weapons unfold', dict(dur=8)), (78, 'host roars out', dict(dur=18))]

    def setup(self, st):
        K = [RK.TUSK, RK.HORN, RK.SPEARMAN, RK.HULK, RK.HORN_SPEAR, RK.SWORDSMAN]
        self.cr = Crowd(st, [(g, RK.K_RUN(p / 4 + k * .17), ROAR, y) for k, (g, y) in enumerate(zip(K, (14, -14, 8, -8, 18, -18))) for p in range(4)], px=420, pitch=2., box=(-7, -.6, 7, 19)); self.cr.kinds, self.cr.ph = 6, 4
        r = np.random.default_rng(5); n = 330; x = np.sign(r.uniform(-1, 1, n)) * (5 + 62 * r.uniform(0, 1, n) ** .8); z = 1330 - 230 * r.uniform(0, 1, n)
        self.host = Host(self.cr, np.c_[x, 0 * x, z], 3, scale=(1.15, 1.5))

    # ---------------------------------------------------------------- how awake he is
    def eyes(self, f):
        lids, glow, flare = np.zeros(10), np.zeros(10), np.zeros(10)
        for h, k in OPEN.items():
            lids[h] = keys(f, [(k - 1, 0.), (k, .55), (k + 1, 1.08), (k + 4, 1.)]); glow[h] = smooth(k - 1, k + 1, f) * (1. + .06 * noise1(f * .4, h)); flare[h] = 0. if f < k else .26 + 1.5 * decay((f - k) / 24., 7.)
        return lids, glow, flare

    def frame(self, f, st):
        st.clear('#000', f=f); t = st.t; hit = f >= HIT; a = (f - HIT) / 24.; lids, glow, flare = self.eyes(f)
        u = f / 71.; pu = ease_io(min(u, 1.), 1.5); dist = 206 - 126 * pu
        k = keys(f, [(HIT - 1, 0.), (HIT, 0.), (HIT + 1, .40), (HIT + 3, .95), (HIT + 5, 1.05), (HIT + 9, 1.), (95, 1.0)]) if hit else 0.
        eye = lerp(V(0, 318 + 16 * pu, AT[2] + dist), V(0, 270, AT[2] + 124 - 5 * smooth(80, 95, f)), k); at = lerp(V(0, 325 + 15.5 * pu, AT[2]), V(0, 317, AT[2]), k)
        cam = Cam(eye, at, lerp(34., 50., k))
        if f > HIT: cam = shaken(cam, f, 3.6 * decay(a, 5.) + .35, .9)
        st.cam = cam
        wake = sum(smooth(k, k + 6, f) for k in OPEN.values()) / 10.; fire = .25 * wake ** 2 + (1.1 if hit else 0.)
        # ---- Lanka
        st.paint('sky.frag', **SKY(BLOOD, sunDir=(0, .02, -1), sunR=0., sunGlow=.0 + .9 * hit, rays=.5 * hit, cov=.72, cy0=.0, cy1=.42, **{c: tuple(np.array(hexc(v)) * (.16 + .9 * hit + .5 * wake ** 2 * (not hit))) for c, v in dict(cZen='#14040c', cMid='#5a0c14', cHor='#d8481c', cLow='#3a0a10', cLit='#e85a2a', cCM='#8a1c20', cSh='#3a0a18', cInk='#0c0206').items()}))
        g = .55 * wake + .3 * hit
        L0 = LK.light('dark', inkRef=3., key=(0, .5, .6), keyCol=tuple(np.array([.16, .06, .05]) * g * (1 + .5 * hit)), amb=tuple(np.array([.035, .018, .035]) * g * (1 + .5 * hit)), rimCol=tuple(np.array([1.1, .30, .06]) * (wake ** 2 * .5 + .7 * hit)), envM=tuple(np.array([.8, .22, .06]) * g * (1 + .8 * hit)), envB=tuple(np.array([1., .4, .1]) * g * (1 + .8 * hit)), envT=(.06, .02, .05), fogCol='#2a0810', fog=(.0007, 220, .001, 0), pts=[(V(0, 300, 1120), 34., (2.6 * hit, .95 * hit, .24 * hit)), *[(V(sx * 74, 300, 1216), 20., tuple(np.array([1.4, .42, .09]) * sum(smooth(OPEN[h], OPEN[h] + 3, f) for h in ORDER[i::2]) / 5.)) for i, sx in ((0, -1), (1, 1))]])
        st.open(cam, L0, far=6000); LK.draw(st, 'dark', night=.6 * wake, doors=float(1 - smooth(HIT - 1, HIT + 5, f))); st.close()
        # fires along the wall wake with the eyes, from both ends inward
        P, S, Q = [], [], []
        for i, h in enumerate(ORDER):
            ag = max(0., (f - OPEN[h]) / 24.)
            if ag <= 0: continue
            sx = -1 if i % 2 == 0 else 1; q = np.random.default_rng(20 + i); m = 5
            for j in range(m):
                an = (j - 2) * .62; r_ = 6.6 * (.4 + .15 * (i // 2)); y = 304.5 - 8.3 * (i // 2); s = (4.2 + 1.6 * q.uniform()) * smooth(0, .35, ag) * (1 + .5 * hit) * (1 + .8 * decay(ag, 6.)); P.append((sx * 74 + r_ * math.sin(an), y + s * .7, 1204 + r_ * math.cos(an))); S.append(s); Q.append(q.uniform())
        if P: FX.particles(st, np.array(P), np.array(S), (.40, .26, .20) if not hit else (.62, .40, .30), 'tongue', seed=np.array(Q)); FX.particles(st, np.array(P), np.array(S) * (3.2 if not hit else 1.7), (.5, .10, .02), 'ember', alpha=.035 if not hit else .10)
        if hit: IM.grade(st, (.82, .52, .46))
        cx, cy, _ = cam.project(AT + V(0, 62, -6)); px = cam.px(AT)
        if hit: st.paint(GLOW, 'add', ctr=(float(cx), float(cy)), amt=float(.42 * smooth(HIT, HIT + 3, f)), rad=float(px * 62), rays=1., wheel=0.)
        else: st.paint(GLOW, 'add', ctr=(float(cx), float(cy + 240)), amt=float(.16 * wake ** 1.6), rad=900., rays=.0, wheel=0.)
        haze(st, 8 + 10 * wake)
        # ---- him
        arms = keys(f, [(HIT, 0.), (HIT + 2, .12), (HIT + 8, 1.06, 'out'), (HIT + 13, 1.0)]); laugh = .86 + .14 * math.sin((f - HIT) * 2.1) if hit else 0.
        mouths = np.array([laugh * (.72 + .28 * math.sin(f * 1.3 + i * 1.9)) for i in range(10)]) if hit else np.zeros(10)
        pose = keys(on2(f), [(0, RV.R_STAND), (HIT - 2, RV.R_STAND), (HIT - 1, RV.R_STAND.set(pelr=(0, 3, 0), cher=(0, 5, 0), hedr=(0, 5, 0))), (HIT + 4, LAUGH, 'back'), (95, LAUGH.set(hedr=(0, 3, 0)))])
        if hit: b = math.sin((on2(f) - HIT) * 1.05); pose = pose.set(cher=(0, pose.cher[1] + 2.2 * b, 0), hedr=(0, pose.hedr[1] + 1.5 * b, 0), shrug=(.3 + .25 * b, .3 + .25 * b))
        S = RV.fig(st, pose, at=AT, scale=SC, fan=1., draw=False); E = RV.heads(S, 1.); pts = []
        for h in range(10):
            c, s, R = E[h]
            if flare[h] > 0 and not hit: pts.append((c + V(0, .5, 1.7) * s, .62 * s, tuple(np.array([3.2, 1.1, .22]) * flare[h])))
        up = smooth(HIT - 1, HIT + 2, f)
        if hit: pts = [(AT + V(-30, 2, 34), 46., (2.0 * up, .75 * up, .18 * up)), (AT + V(30, 2, 34), 46., (2.0 * up, .75 * up, .18 * up)), (AT + V(0, 4, 48), 40., (1.5 * up, .6 * up, .15 * up))]
        base = .016 * wake ** 1.5
        L = Light(key=(0, -.45, .9), keyCol=tuple(np.array([1.25, .58, .24]) * up + base * np.array([1., .5, .5])), amb=tuple(np.array([.05, .022, .06]) * (.01 + .30 * wake ** 1.5) * (1 - up) + np.array([.16, .06, .12]) * up), rim=(.0, .55, -.85), rimCol=tuple(np.array([.55, .13, .03]) * wake ** 2 * (1 - up) + np.array([2.4, .95, .28]) * up), bounceCol=tuple(np.array([.5, .18, .04]) * up), envT=tuple(np.array([.10, .03, .03]) * (1.3 * wake ** 1.5) * (1 - up) + np.array([.6, .2, .14]) * up), envM=tuple(np.array([.13, .045, .015]) * (.01 + 1.5 * wake ** 1.6) * (1 - up) + np.array([1., .5, .2]) * up), envB=tuple(np.array([.18, .06, .02]) * (.01 + 1.5 * wake ** 1.6) * (1 - up) + np.array([1.3, .75, .32]) * up), pts=pts, shadow=False, ink=3.2, inkRef=SC * .9, inkCol=(.004, .001, .002), fogCol='#8a2410', fog=(.0006 * up, 60, 0, 0))
        st.open(cam, L, far=3000)
        S = RV.fig(st, pose, at=AT, scale=SC, fan=1., arms=float(arms), lids=lids, eyeglow=glow * (1. - .25 * hit), mouths=mouths, face=Face(frown=.5, smile=.1 + .5 * hit, mouth=float(mouths[4]), teeth=.4 * hit))
        RV.cape(st, S, t, wind=(0, .10 + .25 * up, -.2))
        if hit:
            go = (f - HIT) * 2.9; P = self.host.pos + V(0, 0, go - 60); z = P[:, 2]; m = (z > 1166) & (z < eye[2] - 14)
            self.host.draw((f - HIT) * .55, off=(0, 0, go - 60), mask=m, y=lambda p: stair_y(p[:, 2]))
            for sx in (-1, 1):
                for j, (bx, bz, bh, bl) in enumerate(((62, 1186, 74, 46), (104, 1150, 120, 60))):
                    rise = ease_out((f - HIT - j * 2) / 7., 3.); root = V(sx * bx, 255 + bh * rise, bz); st.mesh(*CL.tube(np.array([V(sx * bx, 250, bz), root]), .8, 8, 4), kind=0, col=('#5a2a14', '#1c0a08', '#fff'), cls=2, ink=.9)
                    if rise > .3: VH.banner(st, 'ravana', root - V(0, 1.5, 0), t * 1.1 + j, bl * rise, 22 * rise, (sx * 1., .04, .22), amp=1.5, seed=sx + j)
            for sx, z0, ph, g_, s_ in ((-1, 1290, 0., RK.HORN, 1.7), (1, 1294, .4, RK.HULK, 1.6), (-1, 1262, .7, RK.SPEARMAN, 1.5), (1, 1258, .2, RK.HORN_SPEAR, 1.5)):
                z = z0 - 70 + min(go, 64) + .35 * max(0, go - 64)
                if f >= HIT + 2: st.fig(g_, RK.K_RUN(on2(f - HIT) / 14. + ph), at=(sx * (49 if z0 > 1280 else 37), float(stair_y(z)), z), yaw=-sx * 14, scale=s_, face=ROAR)
        st.close()
        # ---- fire round the wheel, sparks, smoke
        if hit:
            c = S.chest((0, .8, -1.)); n = 64; an = np.arange(n) / n * 6.283; s = 12. * smooth(HIT + 1, HIT + 6, f) * (1 + .18 * np.sin(an * 5 + t * 9)); R = 57 * ease_out((f - HIT - 1) / 6., 3.)
            q = np.stack([np.sin(an) * R, np.cos(an) * R * .97, 0 * an], 1) + c; keep = q[:, 1] > AT[1] - 2
            FX.particles(st, q[keep] + np.stack([np.sin(an * 1.) * .35, .35 + .2 * np.cos(an), 0 * an], 1)[keep] * s[keep][:, None], s[keep], (.85, .60, .45), 'tongue', rot=-.62 * np.where(an > 3.1416, an - 6.2832, an)[keep], seed=(np.arange(n) * .618 % 1)[keep])
            FX.embers(st, 260, ((-110, 190, 1160), (110, 300, 1300)), t * 1.5, rise=44., size=.9, seed=5, life=1.6, swirl=8)
            FX.burst(st, 120, AT + V(0, 0, 40), a, speed=110, grav=-20, size=1.0, seed=3, spread=(1.3, 1.1, .5), up=.9, life=1.)
            footdust(st, 40, ((-60, 225, 1190), (60, 250, 1290)), t, size=13, col=('#c8602a', '#5a1c14'), alpha=.45, rise=9, seed=4)
        else:
            eo = RV.eye_points(S, 1.)
            for h, kf in OPEN.items():
                if f >= kf:
                    for p in eo[h]: x, y, _ = cam.project(p); FX.particles(st, np.array([[x, y]]), cam.px(p) * E[h][1] * .62, (1., .34, .04), 'ember', alpha=.16)
                if kf <= f < kf + 10:
                    ag = (f - kf) / 24.; e = RV.eye_points(S, 1.)[h]; s = E[h][1]
                    for p in e: x, y, _ = cam.project(p); FX.particles(st, np.array([[x, y]]), cam.px(p) * s * (.85 * decay(ag, 6.) + .25), '#ffb040', 'glint', alpha=.8 * decay(ag, 6.))
                    FX.burst(st, 14, e.mean(0), ag, speed=2.6 * s, grav=-3, size=.05 * s, seed=h, col='#ffb050', life=.5, kind='ember')
            FX.embers(st, 40 + int(70 * wake), ((-60, 285, 1170), (60, 300, 1235)), t, rise=24., size=.42, seed=5, life=3.2, swirl=3)
        if f == HIT: IM.inkflash(st, '#0a0206', '#c8281a', '#ffe6b0', lo=.24, hi=.60)
        elif hit and f < HIT + 6: IM.zoomblur(st, (float(cx), 560.), .045 * (1 - (f - HIT) / 6.)); IM.shock(st, (float(cx), 600.), 200 + 2600 * a * 2.2, 120, 50)
        return st.finish(bloom=.55, thr=.85, vig=.5, contrast=1.1, satu=1.05, flash=.10 * (f == HIT + 1), flashCol="#ff9a30", grain=.017)
