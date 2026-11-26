"""c1 (60): morning, emerald and gold.  The golden deer steps into the shafts of light, turns its jewelled head and looks at us (f18-30), leaps (f36) across the frame shedding gold dust.  f42: Sita, close: the gold passes over her face and stays in her eyes."""
from shots.forest_kit import *
from chars import deer


class Shot(ShotBase):
    id = 'c1'; n = 60
    EVENTS = [(0, 'forest morning', dict(dur=60)), (1, 'hoof', dict(soft=1)), (5, 'hoof', dict(soft=1)), (10, 'hoof', dict(soft=1)), (14, 'hoof', dict(soft=1)), (18, 'jewels chime', {}), (24, 'it looks at us', {}), (33, 'hooves gather', {}), (36, 'leap', dict(dur=6)), (36, 'gold dust', dict(dur=24)), (48, 'she sees it', {}), (50, 'gold shimmer', dict(dur=10))]

    # ------------------------------------------------------------ the deer
    X0, STOP = -11.2, 18

    def deer_at(self, f):
        """pose and place at frame f (whole or between)"""
        if f < 18:
            c = 7.6 / deer.STEP_DIST; u = f / 18.; e = u - .04 * math.sin(2 * math.pi * u); P = deer.step(.12 + c * e, lift=1.0); x = -7.2 - 7.6 * (1 - e)
            return P.mix(deer.ALERT, smooth(14, 18, f)), x
        g = on2(f) if f < 33 else f
        k = keys(g, [(18, 0.), (20, -.10), (25, 1.05, 'io'), (28, 1.)]); P = deer.ALERT.mix(deer.look(-1, 1.).set(head=(-66., 12., -6.), neck=(42., 76., -20.), ears=(1., 1.)), k).set(tail=(10 + 26 * max(0., math.sin((f - 18) * 1.15)) * (f < 30), 0.))
        P = P.set(ears=(1. - .7 * (f in (27, 28)), 1.))
        if f >= 30:
            t = keys(f, [(30, 0.), (34, .155, 'io'), (35, .18, 'linear'), (36, .235, 'linear'), (42, .70, 'linear')]); Q = deer.leap(t); P = P.mix(Q, smooth(30, 33, f)) if f < 33 else Q
        return P, -7.2

    def stage1(self, f, st, t):
        push = ease_io(clamp((f - 2) / 28.), 1.9); run = smooth(31, 40, f)
        eye = lerp(lerp(V(-4.5, 6.2, 43), V(-2.2, 5.6, 27.5), push), V(4.6, 5.4, 41), run); at = lerp(lerp(V(-6.5, 8.4, 0), V(-3.4, 7.5, 0), push), V(5.8, 10.6, 0), run); cam = Cam(eye, at, lerp(32, 35, run), roll=-2.5 * run); st.cam = cam
        st.paint('sky.frag', **SKY(None, **WOOD['sky'])); hop = V(-9, 17, -70); x, y, z = cam.project(hop)
        st.paint('in vec2 uv;out vec4 o;uniform vec2 res,c;void main(){vec2 p=(vec2(uv.x*res.x,(1.-uv.y)*res.y)-c)/res.y;float r=length(p*vec2(1.,.8));o=vec4(vec3(1.,.86,.42)*(exp(-r*r*7.)*.36+exp(-r*2.2)*.22),0.);}', 'add', c=(float(x), float(y)))
        L = wood_light(); st.open(cam, L); wood(st, -70, 80, seed=5, clear=(-27., 24.))
        P, dx = self.deer_at(f); yaw = 78; SD = deer.draw(st, P, at=(dx, 0, 0), yaw=yaw, face=Face(gx=0., lid=.0 if f in (21, 22) else 1.), scale=1.)
        FL.tree(st, 'banyan', (-33, -.4, -13), 64, season='summer', seed=1, tint=(.30, .42, .36)); FL.tree(st, 'mango', (36, -.4, -10), 60, season='summer', seed=0, tint=(.34, .46, .38))
        for x_, z_, h_, s_, k_ in ((-17, 7, 4.6, 0, 'fern'), (14, 8, 5.0, 1, 'fern'), (23, 4, 5.5, 0, 'shrub'), (-24, 3, 6.5, 1, 'shrub')): FL.tree(st, k_, (x_, -.3, z_), h_, season='summer', seed=s_, tint=(.62, .78, .66))
        st.close()
        shafts(st, (x - 420, -760), .62 * (1 + .04 * math.sin(t * 2)), '#ffe08a', 34, 70, dens=10., seed=3., wid=1.1)
        # a glow under the gold: it lights the grass
        h = SD.chest(); a, b, _ = cam.project(h); st.paint('in vec2 uv;out vec4 o;uniform vec2 res,c;uniform float k;void main(){vec2 p=(vec2(uv.x*res.x,(1.-uv.y)*res.y)-c)/res.y;float r=length(p);o=vec4(vec3(1.,.70,.20)*(exp(-r*r*9.)*.16+exp(-r*3.)*.06)*k,0.);}', 'add', c=(float(a), float(b)), k=1.)
        r = np.random.default_rng(2); n = 130; p0 = r.uniform((-22, 0, -18), (24, 20, 14), (n, 3)); ph = r.uniform(0, 6.28, n); Pm = p0 + np.c_[1.0 * np.sin(t * .7 + ph), .8 * np.sin(t * .5 + ph * 2) + .35 * t, .8 * np.cos(t * .6 + ph)]; FX.particles(st, Pm, r.uniform(.05, .13, n), '#ffe9a0', 'lamp', alpha=.35 + .5 * np.clip(np.sin(t * 2 + ph * 3), 0, 1))
        pts = [SD.p('antlerL'), SD.p('antlerR'), SD.p('crown'), SD.p('heart'), SD.p('back'), SD.chest((.3, .9, .4))]; tw = np.array([max(0., math.sin(t * 5 + i * 2.1)) ** 4 for i in range(len(pts))]); tw[2] += 2.2 * decay((f - 24) / 24., 7.) * (f >= 24); FX.particles(st, np.array(pts), .9 + .9 * tw, '#fff0b0', 'glint', alpha=np.clip(tw, 0, 1))
        if f >= 31:                                                              # gold dust left hanging along the arc
            self.dust(f, st, yaw)
        FX.burst(st, 26, V(-9.6, .3, .4), (f - 35) / 24., speed=7, grav=12, size=.16, seed=5, col='#b89a50', kind='ash', life=.6, up=.9, spread=(1.4, .5, .8))
        FL.frame(st, 'fg_leaves', -90 - 240 * run, -110 - 60 * run, .56, 'summer', 0, lod=3.0, rot=1.5 * math.sin(t * 1.3)); FL.frame(st, 'fg_leaves', 2010 + 120 * run, -150 - 160 * run, .56, 'summer', 1, lod=3.0, flip=True, rot=1.5 * math.sin(t * 1.1 + 2)); FL.frame(st, 'fg_grass', 260 - 60 * run, 1150, .66, 'summer', 0, lod=3.0); FL.frame(st, 'fg_grass', 1760 - 60 * run, 1160, .70, 'summer', 1, lod=3.0)
        if f >= 36: IM.whip(st, 10 * run, 0)
        return st.finish(bloom=.50, thr=.88, vig=.42, contrast=1.05, fade=.6 * (1 - smooth(0, 4, f)), fadeCol='#0c2018')

    def dust(self, f, st, yaw):
        r = np.random.default_rng(8); n = 900; te = 33.5 + 8.5 * r.uniform(0, 1, n) ** .9; age = (f - te) / 24.; ok = age > 0; B = {}
        for q in range(33, 43):
            P, dx = self.deer_at(q); B[q] = deer.draw(st, P, at=(dx, 0, 0), yaw=yaw, draw=False)
        a = np.array([[B[q].pelvis(), B[q].chest(), B[q].head()] for q in range(33, 43)]); i = np.clip(np.floor(te).astype(int) - 33, 0, 8); fr = (te - 33 - i)[:, None]; k = r.uniform(0, 2, n); j = np.minimum(k.astype(int), 1); w = (k - j)[:, None]
        lo = a[i, j] * (1 - w) + a[i, j + 1] * w; hi = a[i + 1, j] * (1 - w) + a[i + 1, j + 1] * w; body = lo * (1 - fr) + hi * fr; vel = (hi - lo) * 24
        ag = np.maximum(age, 0)[:, None]; P = body + r.normal(0, 1., (n, 3)) * (.8 + 2.0 * ag) + vel * .10 * (1 - np.exp(-3 * ag)) - V(0, 1.8, 0) * ag + np.c_[.4 * np.sin(5 * ag[:, 0] + k * 9), 0 * k, 0 * k]
        FX.particles(st, P[ok], ((.07 + .26 * r.uniform(0, 1, n) ** 2.2) * np.clip(1 - age * .5, 0, 1))[ok], '#ffce4a', 'flake', rot=(r.uniform(0, 6, n) + age * r.uniform(-8, 8, n))[ok], seed=(k / 2)[ok]); m = ok & (r.uniform(0, 1, n) > .55); FX.particles(st, (P + r.normal(0, .5, (n, 3)))[m], .22, '#ffd870', 'lamp', alpha=np.clip(1 - age, 0, 1)[m])
        if f >= 36:
            path = [B[q].chest((0, .2, 0)) for q in range(34, min(f, 42) + 1)]
            if len(path) > 2: Q = CL.spline(path, 40); FX.ribbon(st, Q, np.linspace(.05, 1.5, 40), 'light', '#e08a18', '#ffdc80', amt=.42); FX.ribbon(st, Q + V(0, 1.0, 0), np.linspace(.02, .34, 40), 'light', '#ffc040', '#fff2c0', amt=.55); FX.ribbon(st, Q - V(0, 1.2, .5), np.linspace(.02, .22, 40), 'light', '#ffb030', '#fff0b0', amt=.45)

    # ------------------------------------------------------------ Sita
    def stage2(self, f, st, t):
        u = (f - 42) / 17.; g = on2(f); sweep = (f - 43) / 16.
        turn = keys(g, [(42, 0.), (46, -.06), (50, 1.04, 'io'), (52, 1.)])
        P = sita.S_STAND.set(pelr=(0, 0, 0), cher=(-4 + 4 * turn, 2, -3), hedr=(lerp(-22, 6, turn), lerp(10, -2, turn), lerp(5, -3, turn)), rh=(-.5, 10.7 + .2 * turn, 2.2), rhand='relax', rfing=(.5, .85, .2), rpalm=(.2, -.1, -1), rel=(-1, -.9, 0))
        S = st.fig(sita.FOREST, P, draw=False); h = S.head((0, 0, .4))
        cam = Cam(h + V(1.5 - .25 * u, -.25, 9.6 - 1.3 * ease_io(u)), h + V(.30, -.35 + .2 * u, 0), 21, roll=1.5); st.cam = cam
        st.paint('sky.frag', **SKY(None, **WOOD['sky']))
        st.paint('#include "noise.glsl"\nin vec2 uv;out vec4 o;uniform vec2 res;uniform float fT;void main(){vec2 p=uv*vec2(res.x/res.y,1.);vec3 c=mix(hex(0x0b3a2c),hex(0x2f7a46),smoothstep(.25,.75,fbm(p*1.7+3.)));c=mix(c,hex(0xe8d880),smoothstep(.75,.0,length(p-vec2(.30,.95)))*.75);for(int i=0;i<26;i++){vec2 q=vec2(h11(float(i)*3.1),h11(float(i)*7.7+1.))*vec2(res.x/res.y,1.);q+=.012*vec2(sin(fT+float(i)),cos(fT*.8+float(i)*2.));float R=.025+.05*h11(float(i)+9.);float d=length(p-q);vec3 k=mix(hex(0x7ac060),hex(0xffe89a),h11(float(i)*1.7));c+=k*smoothstep(R,R-.006,d)*(.10+.16*h11(float(i)*5.));c+=k*smoothstep(.004,.0,abs(d-R+.003))*.12;}o=vec4(c,1);}')
        gx_ = lerp(-5.5, 6.5, sweep); near = h + V(gx_, .6 * math.sin(sweep * 3.1), 4.2); ga = smooth(42, 46, f) * 1.0
        L = wood_light(key=(-.35, .75, .55), keyCol=(.62, .58, .40), amb='#3c7a66', rim=(-.7, .5, -.5), rimCol=(1.2, 1.0, .45), bounceCol=(.22, .18, .04), envM='#ffd45a', pts=[(tuple(near), 3.2, tuple(np.array([1.35, .92, .28]) * ga * (1 - .35 * smooth(54, 60, f))))], shadow=False, ink=3.6)
        fc = Face(lid=.80, smile=.15, gx=-.35, gy=-.25) if f < 46 else Face(lid=.45, smile=.15, gx=0.) if f == 46 else Face(lid=1., brow=.30, smile=.15, mouth=.05, gx=round(clamp(.9 * (sweep - .5), -.4, .45) * 5) / 5, spark=round(smooth(46, 52, f), 1)) if f < 53 else Face(lid=.98, brow=.28, smile=.42, mouth=.0, gx=.35, spark=1.)
        st.open(cam, L); st.fig(sita.FOREST, P, face=fc, u=dict(Wind=(-.3 * sweep, 0, 0))); st.close()
        # the gold thrown on her: bright flecks that slide over skin and cloth
        st.post_paint('''
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform sampler2D tex,tZ;uniform vec2 res;uniform float fT,cx,k;
void main(){vec3 c=texture(tex,uv).rgb;float z=texture(tZ,uv).x;vec2 p=vec2(uv.x*res.x,uv.y*res.y)/res.y;float x=p.x-cx/res.y;
 vec2 w=vec2(p.x*2.6-cx/res.y*2.2,p.y*2.6+.4*sin(fT*2.));w+=.35*vec2(vn(w*1.7+fT*.7),vn(w*1.7-fT*.6+5.));float v=voro(w).x;float ca=smoothstep(.34,.06,v);float lines=smoothstep(.10,.0,abs(v-.30));
 float band=exp(-x*x*3.2)+.45*exp(-pow(x+.55,2.)*7.);float m=step(z,60.)*band*k;c*=1.+vec3(1.0,.72,.18)*m*(.40+1.25*lines+.7*ca);o=vec4(c,1);}
''', texs=dict(tZ=st.L.color_attachments[1]), fT=float(t), cx=float(lerp(260, 1560, sweep)), k=float(ga))
        r = np.random.default_rng(4); n = 90; p0 = r.uniform((-5, -4, -2), (5, 4.5, 5), (n, 3)); ph = r.uniform(0, 6.28, n); v = V(5.5, .0, 0); Pm = h + p0 + v * (1 - math.exp(-(f - 42) / 24. * 2.5)) * .6 + np.c_[.3 * np.sin(t * 2 + ph), -.9 * (f - 42) / 24. * r.uniform(.4, 1.4, n), .2 * np.cos(t * 2 + ph)] - V(1.6, -.6, 0); FX.particles(st, Pm, r.uniform(.015, .055, n), '#ffce4a', 'flake', rot=ph + t * 4, seed=ph / 6.28, alpha=ga); FX.particles(st, Pm[::3] + V(.4, .3, .3), .07, '#ffd870', 'lamp', alpha=.8 * ga)
        IM.dof(st, float((h - cam.eye) @ cam.R[2]), 4.5, 4.)
        return st.finish(bloom=.5, thr=.9, vig=.48, contrast=1.06)

    def frame(self, f, st):
        st.clear('#000', f=f); return self.stage1(f, st, st.t) if f < 42 else self.stage2(f, st, st.t)
