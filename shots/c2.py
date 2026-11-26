"""c2 (60): the chase.  Rama runs beside us through whipping leaves, the deer a flicker of gold ahead (f0-11); plants (f12), draws, holds (f18-23), release (f24); the arrow through leaf and light (f26-29);
f30 strike, a print flash; the gold burns off and Maricha is inside it: his face, the stolen cry (f36-60), and the wood goes dark."""
from shots.forest_kit import *
from chars import deer, rakshasa as RK

VR = 26. / 12.                                              # his speed, units a frame: a footfall on every pulse
PH0 = .0


def rx(f): return VR * f


XP = rx(12) + 26. * .26 / 2 - .25                           # where the left ankle comes down at f12
YAW1 = 14.


class Shot(ShotBase):
    id = 'c2'; n = 60
    EVENTS = [(0, 'run footstep', {}), (0, 'leaves whip', dict(dur=14)), (6, 'run footstep', {}), (3, 'deer bounds', {}), (9, 'deer bounds', {}), (12, 'foot plants', {}), (14, 'arrow drawn from quiver', {}), (16, 'bow draw', dict(dur=3)), (18, 'string creak', dict(dur=6)), (24, 'bow release', {}), (25, 'arrow flight', dict(dur=5)), (30, 'arrow strikes', {}), (31, 'gold burns', dict(dur=12)), (36, 'the stolen cry', dict(dur=20)), (38, 'birds burst up', dict(soft=1)), (48, 'wood darkens', dict(dur=12))]

    # -------------------------------------------------------------- Rama
    def rama(self, f):
        """pose, place, yaw, face, and what the hands do: ('run', 'nock', 'loose')"""
        if f < 12:
            ph = f / 12.; P = run_pose(ph + PH0); c = math.cos(2 * math.pi * ph)
            P = P.set(lh=(1.5, 9.2 - .5 * c, 2.6 - .8 * c), lel=(.8, -.6, -.4), lhand='grip', lfing=(-.3, .2, .9), lpalm=(-.9, 0, -.2), hedr=(P.hedr[0] - 14, P.hedr[1], 0)); return P, (rx(f), 0, 0), 90., Face(frown=.35, squint=.15, smile=-.1), 'run'
        e = keys(f, [(12, 0.), (16, 1.03, 'out'), (18, 1.)]); yaw = lerp(90., YAW1, e); ox = lerp(rx(12), XP - 2.45, keys(f, [(12, 0.), (14, 1.35, 'out'), (18, 1., 'io')]))
        d = keys(f, [(15, .12), (18, 1.08, 'out'), (20, 1.0), (24, 1.02)]); trem = .018 * math.sin(f * 2.4) * (18 <= f < 24)
        A = PZ.archer(d + trem, low=.55).set(hedr=(76, 3, -2))
        R0 = run_pose(1. + PH0).set(lh=(1.5, 9.2, 2.6), lel=(.8, -.6, -.4), lhand='grip', lfing=(-.3, .2, .9), lpalm=(-.9, 0, -.2))
        P = R0.mix(A, clamp(e)); back = keys(f, [(12, 0.), (14, 1., 'out'), (15, 1.), (16, .0, 'io')])                # the hand goes over the shoulder for an arrow
        if back > 0: P = P.mix(P.set(rh=(-1.1, 14.3, -1.3), rel=(-1, .5, .2), rhand='draw', rfing=(.2, -.9, -.3), rpalm=(0, -.3, 1)), back)
        low = impulse((f - 12) / 24., 10) * .9; P = P.set(pel=(P.pel[0], P.pel[1] - low, P.pel[2]))
        loose = 0.
        if f >= 24:
            loose = 1.; k = ease_out((f - 23) / 2.5, 2.6); P = P.set(rh=tuple(np.array(P.rh) + V(-1.9, .25, -.75) * k), rhand='open', rfing=(-.2, .7, .6), lh=tuple(np.array(P.lh) + V(.25, -.20, .05) * k), cher=(P.cher[0] - 5 * k, P.cher[1] - 3 * k, P.cher[2]))
        a = math.radians(yaw); d_ = V(XP - ox, .75, 0.0); lf = (math.cos(a) * d_[0] - math.sin(a) * d_[2], .75, math.sin(a) * d_[0] + math.cos(a) * d_[2]); P = P.set(lf=lf, lft=(90 - yaw, 0))
        face = Face(frown=.45, squint=.25, smile=-.15, lid=.95) if f < 24 else Face(frown=.3, squint=.1, smile=-.1, lid=1.)
        return P, (ox, 0, 0), yaw, face, 'run' if f < 15 else 'nock' if f < 24 else 'loose'

    def chase(self, f, st, t):
        P, at, yaw, face, hands = self.rama(f); run = 1 - smooth(11, 15, f); X = rx(f) if f < 12 else lerp(rx(12), XP - 1.0, ease_out((f - 12) / 4., 2.)); e = ease_io((f - 11) / 7., 2.2)
        sx, sy = shake(f, .22 * run + .03, .8, 3); sx2, sy2 = shake(f, .35 * decay((f - 24) / 24., 9.) * (f >= 24), 1., 8)
        eye = lerp(V(X + 7.5, 4.6, 27), V(X + 12.0, 4.0, 19.), e) + V(-.10, .03, -.16) * max(0, min(f, 24) - 17) + V(sx + sx2, sy + sy2, 0); tgt = lerp(V(X + 3.8, 8.6, 0), V(X + 2.9, 10.0, 0), e) + V(sx, sy, 0) * .6; cam = Cam(eye, tgt, lerp(38, 36, e), roll=lerp(-5, -3, e)); st.cam = cam
        st.paint('sky.frag', **SKY(None, **WOOD['sky'])); L = wood_light(key=(.35, .70, .55), rimCol=(1.7, 1.3, .55))
        far_ = V(X + 34 + 20 * e, 14, -80); x, y, z = cam.project(far_); st.paint('in vec2 uv;out vec4 o;uniform vec2 res,c;void main(){vec2 p=(vec2(uv.x*res.x,(1.-uv.y)*res.y)-c)/res.y;float r=length(p);o=vec4(vec3(1.,.86,.42)*(exp(-r*r*6.)*.40+exp(-r*2.2)*.22),0.);}', 'add', c=(float(x), float(y)))
        st.open(cam, L); wood(st, X - 60, X + 130, seed=9, clear=None, near=False, kinds=('mango', 'pahari_round', 'kadamba', 'palm'), rows=((-150, 34, .62), (-92, 36, .42), (-52, 34, .20)))
        # the deer, seen between the trunks
        dt = .10 + f / 13.; dx = X + 16.0 + 9. * ease_in((f - 10) / 14., 1.5) + 1.2 * math.sin(f * .3); deer.draw(st, deer.run(dt), at=(dx, 0, -13.5), yaw=84, scale=.86)
        for i in range(-2, 10):
            r = np.random.default_rng(i & 0xff); tx = i * 24. + r.uniform(-4, 4) + 10
            if tx < XP + 4: FL.tree(st, ('kadamba', 'ashoka', 'palm')[i % 3], (tx, -.3, -9.5 - 2 * r.uniform()), 62, season='summer', seed=i % 2, tint=(.46, .60, .52))
        # his shadow on the ground
        sh = CL.sheet(lambda u, v: V(at[0] + (u - .5) * 8.2 - 1.6, .28, (v - .5) * 2.4 - .8), 8, 4); st.close()
        shafts(st, (x - 200, -700), .50, '#ffe08a', 30, 70, dens=10., seed=3. + X * .0, wid=1.1)
        IM.whip(st, 46 * run, 0)
        st.open(cam, L); S = st.fig(rama.EXILE, P, at=at, yaw=yaw, face=face, u=dict(Wind=(0, 0, -1.5 * run))); quiver(st, S); aim = None
        if hands == 'run': held_bow(st, S, 'L', up=S.d((-.15, .95, .30)) if f < 13 else (0, 1, 0), fwd=S.d((0, -.3, 1)) if f < 13 else (1, 0, 0), half=5.0)
        elif hands == 'nock': nk, tip, aim = PR.bow_and_arrow(st, S, half=5.2)
        else: nk, tip, aim = PR.bow_and_arrow(st, S, half=5.2, arrow=False, release=1.)
        def solve_at(tt): g = tt * 24; P, at, yaw, _, _ = self.rama(min(g, 24)); return st.fig(rama.EXILE, P, at=at, yaw=yaw, draw=False)
        kick = decay((f - 24) / 24., 5.) * (f >= 24); w = lerp(.85, 1.25, run); sashes(st, solve_at, t, 'rama', wind=(-w + .5 * kick, .10 + .10 * run + .5 * kick, -.15 * (1 - run)), wave=.8, grav=lerp(.50, .28, run), k=1.1)
        st.close()
        if f < 12:                                                              # dust from each footfall
            pass
        for f0, x0 in ((0, rx(0) + 3.1), (6, rx(6) + 3.1), (12, XP)):
            FX.burst(st, 26, V(x0, .2, .3), (f - f0) / 24., speed=6, grav=10, size=.30, seed=f0, col='#a89858', kind='ash', life=.5, up=.8, spread=(1.2, .5, .6)); FX.burst(st, 8, V(x0, .3, .3), (f - f0) / 24., speed=9, grav=16, size=.28, seed=f0 + 1, col='#5a8a3a', kind='leaf', life=.7, up=1., spread=(1.2, .6, .6))
        if hands == 'nock' and f >= 18: FX.particles(st, tip[None], .8 + .25 * math.sin(f * 1.7), '#fff0b8', 'glint', alpha=.9)
        if f >= 24:
            o = S.palm('L', 0, .62, .3); u = (f - 23.4); a = o + aim * (6 + 17 * u); FX.ribbon(st, np.array([o + aim * max(0, 17 * u - 26), a]), np.array([.02, .16]), 'light', '#ffd070', '#fff8e0', amt=1.); FX.particles(st, a[None], 1.6, '#fff0c0', 'glint'); p = cam.project(o)
            IM.shock(st, (p[0], p[1]), 90 + 260 * u, 60, 26 * (1 - u / 3))
        # leaves between us and him
        r = np.random.default_rng(5); n = 60; p0 = r.uniform((0, 0, 4), (60, 15, 20), (n, 3)); ph = r.uniform(0, 6.28, n); P3 = p0.copy(); P3[:, 0] = X - 26 + np.mod(p0[:, 0] - X * 1.12, 60); P3[:, 1] += .5 * np.sin(t * 5 + ph); FX.particles(st, P3, r.uniform(.22, .5, n), np.where(p0[:, 1:2] > 7, np.array(hexc('#e8c84a')), np.array(hexc('#3f8a3a'))), 'leaf', rot=ph + t * 6, alpha=float(clamp(run * 2)))
        if run > .02:
            for i in range(13):
                q = np.random.default_rng([3, i]); X3 = i * 7. + q.uniform(-2, 2) - 8; xx, yy, zz = cam.project((X3, 22 if i % 2 else -5., 18.5))
                if -1200 < xx < 3000: FL.frame(st, 'fg_leaves' if i % 2 else 'fg_grass', xx - (500 if i % 2 else 0), -190 if i % 2 else 1160, .56 if i % 2 else .85, 'summer', i % 2, lod=4.)
        FL.frame(st, 'fg_leaves', -120 - 500 * run, -120, .62, 'summer', 1, lod=3.2, rot=2 * math.sin(t * 2))
        if run > .05: IM.speedlines(st, amt=.13 * run, col=(1., .85, .42), seed=f // 2, parallel=0., dens=9., inner=.58)
        return st.finish(bloom=.45, thr=.9, vig=.42 + .12 * e, contrast=1.06)

    # -------------------------------------------------------------- the arrow
    def flight(self, f, st, t):
        u = (f - 26) / 4.; X = 62. * u; a0 = V(X, 9.2, 0); D = X - X; head = V(66., 8.2, 0)
        cam = Cam(a0 + V(-8.2 - 1.5 * u, 1.9, 2.6), a0 + V(16, -.6, -.4), 46, roll=6 - 14 * u); st.cam = cam; st.paint('sky.frag', **SKY(None, **WOOD['sky'])); x, y, z = cam.project(head)
        st.paint('in vec2 uv;out vec4 o;uniform vec2 res,c;void main(){vec2 p=(vec2(uv.x*res.x,(1.-uv.y)*res.y)-c)/res.y;float r=length(p);o=vec4(vec3(1.,.86,.42)*(exp(-r*r*6.)*.6+exp(-r*2.2)*.30),0.);}', 'add', c=(float(x), float(y)))
        L = wood_light(key=(-.5, .7, .3), fog=(.006, 30., .002, 0.)); st.open(cam, L); FO.place.draw(st, FO.GROUND, u=dict(gA=WOOD['gA'], gB=WOOD['gB'], leafA=FL.GREEN['summer'][3], mist=WOOD['mist'], snow=0., wet=0., river=0.), sun=0.)
        r = np.random.default_rng(6); n = 46; Px = r.uniform(10, 260, n); s = np.where(np.arange(n) % 2 == 0, 1, -1); Pz = s * (17 + 36 * r.uniform(0, 1, n) ** 1.6 + Px * .05); A = np.c_[Px, 0 * Px - .3, Pz]; hz = np.clip((Px - X) / 420, 0, .6); FL.scatter(st, 'banyan', A[:16], 66, season='summer', seed=1, haze=hz[:16], hazeCol=WOOD['mist'], tint=(.5, .66, .56)); FL.scatter(st, 'mango', A[16:32], 60, season='summer', seed=2, haze=hz[16:32], hazeCol=WOOD['mist'], tint=(.5, .66, .56)); FL.scatter(st, 'pahari_round', A[32:], 62, season='summer', seed=3, haze=hz[32:], hazeCol=WOOD['mist'], tint=(.5, .66, .56))
        B = r.uniform((5, -.3, -26), (160, -.2, 26), (60, 3)); B[:, 2] += np.sign(B[:, 2]) * 4; FL.scatter(st, 'fern', B, 6.5, season='summer', seed=4, tint=(.7, .85, .7))
        deer.draw(st, deer.run(.30 + .09 * (f - 26)).set(head=(-64., 4., 0.), neck=(44., 72., -24.)), at=(66. + 1.6 * (f - 26), 0, -1.2), yaw=80, scale=1.05); st.close(); shafts(st, (x + 300, -600), .5, '#ffe08a', 30, 90, dens=9., seed=4.)
        IM.zoomblur(st, (x, y), .11)
        st.open(cam, L); d = nz(head - a0); spin = f * 1.1; upv = V(0, math.cos(spin), math.sin(spin)); M = PR.place(a0 - d * 3.0, upv - d * (upv @ d), d, 1.25); st.fig(PR.arrow_of(6.5, 1.3), M=M); st.close()
        tip = a0 + d * 5.1; FX.particles(st, tip[None], 1.5, '#fff0c0', 'glint'); e1 = V(0, 1, 0); Q = np.array([tip - d * q for q in np.linspace(0, 13, 20)]); FX.ribbon(st, Q + V(0, .28, 0), np.linspace(.02, .12, 20), 'wind', '#fff4d0', '#ffffff', amt=.7); FX.ribbon(st, Q - V(0, .25, .2), np.linspace(.02, .10, 20), 'wind', '#fff4d0', '#ffffff', amt=.6)
        n = 70; p0 = r.uniform((0, 2, -7), (40, 15, 7), (n, 3)); p0[:, 0] = X - 6 + np.mod(p0[:, 0] - X, 40); FX.particles(st, p0, r.uniform(.2, .5, n), np.where(p0[:, 1:2] > 8, np.array(hexc('#e8c84a')), np.array(hexc('#4a9a3a'))), 'leaf', rot=p0[:, 1] + t * 8)
        FL.frame(st, 'fg_leaves', -160 - 300 * u, -160 - 120 * u, .8 + .5 * u, 'summer', 0, lod=4.5); FL.frame(st, 'fg_leaves', 2080 + 300 * u, -160 - 120 * u, .8 + .5 * u, 'summer', 1, lod=4.5, flip=True)
        IM.speedlines(st, (x, y), amt=.12, col=(1., .80, .30), seed=f, inner=.50, dens=8.)
        return st.finish(bloom=.5, thr=.9, vig=.5, contrast=1.08)

    # -------------------------------------------------------------- the strike
    def strike(self, f, st, t):
        k = (f - 30) / 24.; sx, sy = shake(f, .8 * decay(k, 7.), 1., 2); cam = Cam(V(2.5 + sx, 4.6 + sy, 27 - .5 * (f - 30)), V(.6 + sx, 8.6 + sy, 0), 38, roll=4); st.cam = cam; st.paint('sky.frag', **SKY(None, **WOOD['sky'])); h0 = V(-1.4, 7.6, .8); x, y, z = cam.project(h0)
        dk = smooth(31, 36, f); L = wood_light(key=(-.4, .6, .6), keyCol=tuple(np.array(hexc('#ffeab0')) * (1 - .45 * dk)), amb=tuple(np.array(hexc('#4f9078')) * (1 - .5 * dk)), pts=[(tuple(h0 + V(0, .5, 2.5)), 7., (1.8, .9, .25))])
        st.open(cam, L); wood(st, -50, 60, seed=12, clear=(-24., 24.), dark=1 - .4 * dk)
        tt = keys(f, [(30, .05), (33, .24, 'out'), (36, .40)]); b = keys(f, [(30, 0.), (31, .06), (36, .80)]); SD = deer.draw(st, deer.struck(tt), at=(0, 0, 0), yaw=72, burn=b, burn_at=(0, 6.6, 1.6))
        if f >= 32: st.fig(RK.MARICHA, RK.M_CRY.set(pel=(0, 7.0, 0)), at=(.3, 0, -.6), yaw=38, face=RK.CRY, u=dict(gild=float(1 - .25 * smooth(32, 36, f))))
        if f < 33: d = nz(V(1, -.08, -.15)); st.fig(PR.arrow_of(6.5, 1.3), M=PR.place(h0 - d * (4.2 if f > 30 else 6.0), V(0, 1, 0), d, 1.))
        st.close(); deer.leaf(st, SD, (f - 30.5) / 24., n=520, speed=15., size=.22)
        FX.burst(st, 70, h0, (f - 30) / 24., speed=26, grav=6, size=.12, seed=4, col='#ffc050', life=.5, stretch=.07); FX.embers(st, 90, ((-5, 2, -2), (5, 12, 3)), t, rise=6., size=.13, seed=3, life=1.2, swirl=1.2)
        IM.shock(st, (x, y), 60 + 130 * (f - 30), 80, 46 * decay(k, 4.))
        if f in (30, 31): IM.zoomblur(st, (x, y), .10); IM.inkflash(st, dark='#0c1408', mid='#d8961c', light='#fff6dc', lo=.30, hi=.60, invert=f == 31)
        return st.finish(bloom=.55, thr=.9, vig=.5, contrast=1.08)

    # -------------------------------------------------------------- the cry
    def cry(self, f, st, t):
        u = (f - 36) / 23.; g = on2(f); dk = smooth(40, 58, f)
        rear = keys(g, [(36, -.3), (38, 0.), (44, 1.04, 'out'), (48, 1.), (54, .95), (60, .75)]); sh_ = .9 * math.sin(f * 2.1) * (1 - smooth(50, 58, f))
        P = RK.M_CRY.set(hedr=(lerp(-16, 6, rear) + sh_, lerp(10, -17, rear), lerp(-5, 7, rear)), cher=(0, lerp(-8, -14, rear), 4), lh=(4.0, 13.6 + .3 * rear, 3.2), rh=(-3.6, 12.4, 3.4))
        S = st.fig(RK.MARICHA, P, draw=False); h = S.head((0, .05, .4)); cam = Cam(h + V(-2.2 + .9 * u, -1.5 - .3 * u, 10.2 - 1.2 * ease_io(u)), h + V(.35, .30, 0), 27, roll=lerp(-5, 3, u)); st.cam = cam
        st.paint('''
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform vec2 res;uniform float fT,k;
void main(){vec2 p=uv*vec2(res.x/res.y,1.);vec3 c=mix(hex(0x12503a),hex(0x4a8a3c),smoothstep(.25,.75,fbm(p*1.5+2.)));c=mix(c,hex(0xe0c870),smoothstep(.8,.0,length(p-vec2(.35,1.)))*.6);
 vec3 d=mix(hex(0x04060e),hex(0x16203a),smoothstep(.2,.8,fbm(p*1.5+2.)));d=mix(d,hex(0x2a3a5c),smoothstep(.9,.0,length(p-vec2(.35,1.)))*.55);
 float edge=fbm(p*2.2+5.)*.5;float m=smoothstep(-.08,.08,k*1.35-edge-.35*distance(p,vec2(.35,1.))*.6);c=mix(c,d,m);
 for(int i=0;i<5;i++){float f=float(i);float x=(f+.5)/5.*2.1-.15+.1*h11(f);float w=.035+.05*h11(f+3.);float tr=smoothstep(w,w-.02,abs(p.x-x+.03*sin(p.y*4.+f)));c=mix(c,mix(hex(0x0c2c20),hex(0x04060c),m),tr*.75);}
 o=vec4(c,1);}
''', k=float(dk))
        gild = keys(f, [(36, 1.), (37, .96), (48, .10), (54, 0.)]); fl = 1 + .12 * noise1(t * 9, 3); gk = gild * (1 - .5 * dk) + .12
        L = wood_light(key=(-.5, .55, .6), keyCol=tuple(lerp(np.array([.95, .80, .50]), np.array([.22, .27, .40]), dk)), amb=tuple(lerp(np.array([.10, .24, .17]), np.array([.035, .045, .10]), dk)), rim=(.7, .4, -.5), rimCol=tuple(lerp(np.array([1.3, 1.0, .4]), np.array([.35, .48, .85]), dk)), bounceCol=(.1, .06, .02), envT='#ffe8a0', envM='#ffb84a', envB='#3a1a14', pts=[(tuple(h + V(.4, -2.6, 2.6)), 4.2, tuple(np.array([1.1, .52, .16]) * gk * fl))], shadow=False, ink=3.8)
        face = RK.CRY.set(lid=1.) if f < 54 else RK.CRY.set(lid=.8, mouth=.85)
        if f < 38: face = RK.CRY.set(mouth=.55)
        st.open(cam, L); st.fig(RK.MARICHA, P, face=face, u=dict(gild=float(gild))); st.close()
        # the gold goes by: flakes torn off him toward the wood behind us
        r = np.random.default_rng(9); n = 420; born = 34 + 20 * r.uniform(0, 1, n) ** 1.1; age = (f - born) / 24.; ok = (age > 0) & (age < 1.1); d = r.normal(size=(n, 3)); d /= np.linalg.norm(d, axis=1, keepdims=True); p0 = h + d * V(1.0, 1.2, .9) + V(0, -.6, .2); v = V(5.2, 1.6, 3.6) * r.uniform(.5, 1.5, (n, 1)); a = np.maximum(age, 0)[:, None]; Pp = p0 + v * a + v * .6 * a ** 2 + np.c_[.35 * np.sin(a[:, 0] * 7 + d[:, 0] * 9), .3 * np.cos(a[:, 0] * 6 + d[:, 1] * 9), 0 * a[:, 0]]
        FX.particles(st, Pp[ok], (r.uniform(.04, .15, n) * np.clip(1.1 - age, .2, 1))[ok], '#ffc24a', 'flake', rot=(d[:, 0] * 6 + age * r.uniform(-9, 9, n))[ok], seed=r.uniform(0, 1, n)[ok]); m = ok & (r.uniform(0, 1, n) > .6); FX.particles(st, (Pp + V(.3, .2, 0))[m], .07, '#ff9a3a', 'ember', alpha=np.clip(1 - age, 0, 1)[m])
        # the cry itself: rings of air from the mouth
        mth = S.head((0, -.65, .95)); mx, my, _ = cam.project(mth)
        for f0 in (40, 44, 48):
            if f0 <= f < f0 + 9: q = (f - f0) / 9.; IM.shock(st, (mx, my), 40 + 950 * q, 70, 26 * (1 - q) ** 1.4)
        if 38 <= f < 50: IM.zoomblur(st, (mx, my), .022 * (1 - (f - 38) / 12.))
        return st.finish(bloom=.5, thr=.9, vig=.5 + .15 * dk, contrast=1.08, satu=1.04 - .2 * dk)

    def frame(self, f, st):
        st.clear('#000', f=f); t = st.t
        return self.chase(f, st, t) if f < 26 else self.flight(f, st, t) if f < 30 else self.strike(f, st, t) if f < 36 else self.cry(f, st, t)
