"""d6 (84): the ashoka grove by moonlight.  Sita alone, the guards asleep (f0-30); the ring drops from the leaves into her palm (f36) and its spark lights her face,
the first warm light since the rain (f48-70); she looks up (f70); in the leaves two kind amber eyes hold the same spark (f76-84)."""
from lau.shot import *
from lau.look import *
from lau.stage import hexc
from worlds import forest as FO, flora as FL
from chars import sita, hanuman as HM, rakshasa as RK
from chars.armonly import ARM, SKIN, place_hand

DARK = {k: ('#1a2148', '#080b22', 1) for k in range(1, 22) if k not in (3,)}; DARK[3] = ('#39427a', '#12173a', 1)
GUARDS = [k.variant(u=dict(hold=0, shield=0), pal=DARK) for k in (RK.HULK, RK.TUSK, RK.HORN)]
SLUMP = Pose(pel=(0, 1.5, -.6), pelr=(0, -8, 4), cher=(0, 26, -8), hedr=(10, 46, 14), lf=(1.5, .75, 4.6), rf=(-1.9, .75, 3.0), lkn=(.3, 1, .4), rkn=(-.5, 1, .3), lft=(20, -20), rft=(-30, -10), lh=(2.6, 1.6, 2.2), rh=(-1.6, 3.6, 3.0), lel=(1, 0, -.5), rel=(-1, .1, -.3), lhand='relax', rhand='relax', lfing=(.3, -.5, .8), rfing=(.3, -.6, .7), lpalm=(0, -1, 0), rpalm=(0, -1, 0))
CURLED = Pose(pel=(0, 1.3, 0), pelr=(0, 10, 10), cher=(0, 30, 12), hedr=(-14, 30, 20), lf=(1.2, .75, 3.0), rf=(-1.4, .75, 2.6), lkn=(.4, 1, .5), rkn=(-.4, 1, .5), lh=(1.6, 5.0, 2.6), rh=(-1.2, 5.2, 2.6), lel=(1, 0, 0), rel=(-1, 0, 0), lhand='relax', rhand='relax', lfing=(-.7, 0, .6), rfing=(.7, 0, .6), lpalm=(0, -1, 0), rpalm=(0, -1, 0))
SEAT = V(1.2, 2.0, 8.2)

RAYS = '''
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform vec2 res,src;uniform float fT,amt;uniform vec3 col;
void main(){vec2 p=vec2(uv.x*res.x,(1.-uv.y)*res.y);vec2 d=p-src;float a=atan(d.x,d.y);float r=length(d)/res.y;float s=0.;for(int i=0;i<3;i++){float f=7.+9.*float(i);s+=smoothstep(.52,.86,vn(vec2(a*f+float(i)*7.,fT*.10+float(i)*3.)))*(.5-.1*float(i));}
 s*=smoothstep(1.75,.35,r)*smoothstep(.0,.25,r);o=vec4(col*s*amt,0.);}
'''
BOKEH = '''
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform vec2 res,c;uniform float fT,warm,lift;
void main(){vec2 p=uv*vec2(res.x/res.y,1.);vec3 q=mix(hex(0x050a22),hex(0x1c3468),smoothstep(-.1,1.1,uv.y+.35*(fbm(p*1.3+3.)-.5)+lift));
 for(int i=0;i<2;i++){float f=float(i);float tr=smoothstep(.10,.02,abs(fract(p.x*(1.1+.7*f)+.3*f+.05*fbm(vec2(uv.y*2.,f)))-.5)-.10-.05*uv.y*f);q=mix(q,hex(0x060a1e)*(1.+.8*f),tr*.55);}
 float m=smoothstep(.46,.60,fbm(p*2.2+vec2(0,7.)))*smoothstep(.35,.85,uv.y);q=mix(q,hex(0x081a30),m*.8);
 for(int L=0;L<2;L++){float f=float(L);vec2 g=p*(5.+4.*f)+vec2(f*3.7,fT*.03);vec2 id=floor(g);vec2 h=h22(id+f*31.);vec2 e=fract(g)-.5-(h-.5)*.55;float r=.07+.13*h.x;float k=smoothstep(r,r-.05,length(e)+.05*(vn(e*9.+id)-.5))*step(.74,h.y);vec3 cc=h.x>.55?hex(0x9c2430)*.55:hex(0x7fa0e0)*.40;q=mix(q,q+cc*(.35+.25*smoothstep(r-.10,r,length(e))),k*(.36-.12*f));}
 vec2 d=vec2(uv.x*res.x,(1.-uv.y)*res.y)-c;float rr=length(d)/res.y;q+=hex(0xff8a3a)*(exp(-rr*rr*8.)*.30+exp(-rr*2.4)*.06)*warm;o=vec4(q*(.93+.12*fbm(uv*vec2(9.,6.))),1);}
'''


def motes(st, t, box, n=40, seed=5): FX.drift(st, n, box, t, kind='ember', size=.05, col='#8fb0ff', fall=.12, sway=.5, seed=seed, spin=0, alpha=.45)


class Shot(ShotBase):
    id = 'd6'; n = 84
    EVENTS = [(0, 'night insects', dict(dur=84)), (0, 'guards breathe', dict(dur=30)), (10, 'leaf falls', dict(dur=18)), (30, 'ring falls', dict(dur=6)), (33, 'ring glint', {}), (36, 'ring in palm', {}), (40, 'spark wakes', {}), (50, 'breath in', {}), (58, 'eyes see', {}), (62, 'tear', {}), (70, 'looks up', {}), (77, 'eyes open in leaves', {})]

    def frame(self, f, st):
        st.clear('#000', f=f)
        return self.wide(f, st, st.t) if f < 30 else self.palm(f, st, st.t) if f < 48 else self.face(f, st, st.t) if f < 76 else self.eyes(f, st, st.t)

    def wide(self, f, st, t):
        g = on2(f); e = ease_io(f / 31., 1.7); cam = Cam(lerp(V(32, 10, 72), V(15, 8.2, 38), e), lerp(V(1, 19, 0), V(2.2, 10.2, 4), e), lerp(38, 32, e)); st.cam = cam
        st.paint('sky.frag', **FO.grove_sky()); L = FO.grove_light(key=(.40, .75, .52), keyCol='#7f93d0', amb='#1c2758', fogCol='#0c1a42', fog=(.0075, 62., .002, 0.), pts=[(tuple(SEAT + V(5, 15, 9)), 13., (.42, .52, .85))]); st.open(cam, L, far=2000.); FO.grove(st)
        br = .25 * math.sin(t * 2.2); P = sita.S_SIT.set(hedr=(10, 24 + br, 6), cher=(8, 8 + br, -7))
        st.fig(sita.GROVE, P, at=SEAT, yaw=16, face=Face(lid=.30, gy=-.5, sad=.45, smile=0), u=dict(Wind=(.05 * math.sin(t * 1.3), 0, .03)))
        for k, (fig, pose, at, yaw) in enumerate([(GUARDS[0], SLUMP, V(24, 0, 33), -150), (GUARDS[1], CURLED, V(-19, 0, 13), 60), (GUARDS[2], SLUMP, V(20, 0, -2), -20)]):
            b = .5 * math.sin(t * 1.9 + k * 2); st.fig(fig, pose.set(cher=(pose.cher[0], pose.cher[1] + b * 2, pose.cher[2])), at=at, yaw=yaw, face=Face(lid=0, frown=0))
        st.fig(PR.SPEAR, M=PR.place(V(27.5, .2, 30), (-.12, 1, .10), (0, 0, 1), 1.5)); st.fig(PR.SPEAR, M=PR.place(V(-22, .2, 10), (.16, 1, -.1), (0, 0, 1), 1.5))
        st.close(); st.paint(RAYS, 'over', src=(1380., -260.), amt=.075, col=hexc('#8fb0ff'))
        motes(st, t, ((-20, 2, -10), (26, 30, 40)), 60)
        # one leaf falls
        u = clamp((f - 4) / 26.); q = V(9 - 5 * u + 2.2 * math.sin(u * 9), 27 - 23 * u + .8 * math.cos(u * 9), 11); FX.particles(st, q[None], .55, '#7a3020', 'leaf', rot=.6 + 1.1 * math.sin(u * 9 + .7)); FX.drift(st, 14, ((-22, 1, -14), (26, 34, 20)), t, 'petal', .24, '#8a1f1a', .9, 1.6, seed=3)
        FL.frame(st, 'fg_leaves', -160 - 120 * e, -150 - 60 * e, .62 + .12 * e, 'night', 0, rot=4 + math.sin(t), lod=2.4, tint=(.40, .46, .7)); FL.frame(st, 'fg_leaves', 2080 + 120 * e, -170 - 60 * e, .50 + .12 * e, 'night', 0, rot=-10 + math.sin(t * 1.2), flip=True, lod=2.6, tint=(.36, .42, .64)); FL.frame(st, 'fg_grass', 260 - 80 * e, 1130 + 60 * e, .8, 'night', 0, lod=2.6, tint=(.4, .46, .7))
        return st.finish(bloom=.35, thr=.8, vig=.6, satu=.95, contrast=1.12)

    def hand(self, st, palm, sink=0.):
        P = PZ.STAND.set(rh=(-3.0, 8.2, 3.4), rel=(-1, -.3, 0), rhand='cup', rfing=(0, .1, 1), rpalm=(0, 1, 0), lh=(3.0, 8.2, 3.4)); A = ARM.variant(pal={1: SKIN['sita']}, u=dict(side=1, band=1, old=0.))
        S = st.fig(A, P, draw=False); M = place_hand(S, 'R', palm + V(0, sink - .02, 0), (.97, .05, .26), (-.10, 1, .22), 1.12); st.fig(A, P, M=M); return S

    def palm(self, f, st, t):
        g = on2(f); push = ease_io((f - 37) / 11., 1.8) if f > 37 else 0.; palm = V(.25, 0, .2); rest = palm + V(0, .34, .05); hit = 36
        sp = keys(f, [(38, 0.), (41, 1.35, 'out'), (45, .9), (48, 1.15)]) if f > 38 else 0.
        u = (f - 30) / 6.; fall = rest + V(.5 * (1 - u), 3.3 * (1 - u ** 1.7), -.2 * (1 - u)) if f < hit else rest + V(.06, .55 * max(0., math.sin((f - 36) / 4. * math.pi)) if f < 40 else 0, 0); spin = (30 - f) * 1.15 if f < hit else 0.; sink = -.12 * impulse((f - 36) / 24., 7)
        eye = lerp(V(1.4, 6.8 - .03 * (f - 30), 9.6), rest + V(.35, 1.75, 2.9), push); at = lerp(V(.35, .55, .1), rest + V(0, .10, 0), push); cam = Cam(eye, at, lerp(24, 27, push), roll=lerp(-4, 2, push)); st.cam = cam
        x, y, z = cam.project(rest); st.paint(BOKEH, warm=float(sp), c=(float(x), float(y)), lift=0.)
        L = Light(key=(.35, .85, .15), keyCol=(.42, .50, .78), amb=(.10, .14, .28), rim=(.7, .5, -.6), rimCol=(.45, .6, 1.0), bounceCol=(.02, .03, .06), envT='#c8d8ff', envM='#5a70b0', envB='#141c3a', pts=[(rest + V(0, .55, .2), 1.25, tuple(np.array([1.7, .76, .25]) * sp))] if sp > 0 else [], shadow=True, ink=3.4, inkRef=.6)
        st.open(cam, L); self.hand(st, palm, sink); a = spin
        yv = nz(V(math.sin(a) * .9, math.cos(a) * .9 + .1, .5 + .5 * math.sin(a * .7))) if f < hit else nz(V(.10 + .35 * decay((f - 36) / 24., 9) * math.sin(f * 2.1), .80, .62))
        zv = nz(V(.96, -.10 + .5 * math.sin(a), -.2)) if f < hit else V(.96, -.10, -.2)
        rp = fall + V(0, sink, 0); st.fig(PR.RING, M=PR.place(rp, yv, zv, .36)); st.close(); gem = rp + yv * .36 * 1.42
        if 31 <= f <= 35: FX.particles(st, gem[None], (.0, 0, .35, .95, 1.3, .6)[f - 30] * .9, '#eaf2ff', 'glint', rot=.3)
        if sp > 0:
            FX.flame(st, gem - V(0, .10, 0), .32 * min(sp, 1.15), seed=1.3, glow=.9 * sp, calm=1.2); FX.particles(st, gem[None], .5 * sp, '#ffb050', 'glint', alpha=.7); FX.burst(st, 16, gem, (f - 40) / 24., speed=1.6, grav=1., size=.018, seed=4, col='#ffc060', life=.5, up=.5)
        motes(st, t, ((-5, -2, -4), (6, 6, 5)), 40, 8)
        FX.drift(st, 5, ((-4, -2, -3), (5, 5, 3)), t, 'petal', .16, '#b02a24', .9, .5, seed=9)
        IM.dof(st, float((rest - cam.eye) @ cam.R[2]), 4.5, 5.)
        return st.finish(bloom=.45, thr=.9, vig=.55, satu=.9 + .2 * min(sp, 1), contrast=1.06)

    def face(self, f, st, t):
        u = (f - 48) / 27.; g = on2(f); up = keys(g, [(69, 0.), (74, 1., 'io')]); P = sita.S_PALM.set(hedr=(lerp(-3, 2, up), lerp(keys(g, [(48, 24.), (60, 18.), (69, 20.)]), -16, up), lerp(-2, 0, up)), cher=(0, lerp(6, 0, up), -4))
        S = st.fig(sita.GROVE, P, draw=False); h = S.head((0, .05, .45)); S0 = st.fig(sita.GROVE, sita.S_PALM, draw=False); h0 = S0.head((0, .05, .45)); pw = S.palm('R', 0, .62, .3)
        tg = lerp(h0 + V(-.15, lerp(-.45, -.22, smooth(50, 67, f)), 0), h + V(0, .0, 0), ease_io(up)); cam = Cam(h0 + V(-1.9 + .6 * u, -.9 - .5 * up, 9.4 - 2.9 * ease_io(clamp((f - 50) / 17.)) + 1.2 * up), tg, 23, roll=2); st.cam = cam
        fk = 1 + .08 * noise1(t * 8, 4); on = keys(f, [(48, .18), (53, .30), (59, 1.0, 'io')]); src = h + V(-.4, -2.5, 1.9); x, y, z = cam.project(src + V(0, -.5, 0)); st.paint(BOKEH, warm=.65 * on, c=(float(x), float(y)), lift=.25 * up)
        L = Light(key=(.75, .55, -.45), keyCol=(.30, .38, .66), amb=(.11, .14, .30), rim=(.7, .5, -.6), rimCol=(.5, .7, 1.2), bounceCol=tuple(np.array([.20, .08, .02]) * on), envT='#a8c0ff', envM='#8a6a70', envB='#ff9a4a', pts=[(src, 2.7, tuple(np.array([1.10, .50, .17]) * fk * on))], shadow=False, ink=3.4)
        lid = keys(f, [(48, .42), (54, .42), (57, .20, 'in'), (60, .72, 'out'), (66, .68), (69, .62), (74, 1.0, 'out'), (76, 1.0)]); gy = keys(f, [(48, -.75), (56, -.7), (60, -.6), (69, -.5), (73, .5, 'io')]); sk = smooth(56, 61, f)
        F = Face(lid=lid, gy=gy, gx=keys(f, [(48, -.15), (70, -.1), (74, .15)]), spark=sk, sad=keys(f, [(48, .6), (58, .5), (68, .30), (76, .15)]), smile=keys(f, [(48, -.05), (60, 0.), (69, .34), (76, .42)]), tear=keys(f, [(60, 0.), (63, .2), (72, .5, 'smooth')]), mouth=keys(f, [(57, 0.), (60, .05), (64, .02), (69, 0.)]), brow=.3 * smooth(57, 61, f))
        st.open(cam, L); st.fig(sita.GROVE, P, face=F, u=dict(Wind=(.05 * math.sin(t * 1.3), 0, .02)))
        st.fig(PR.RING, M=PR.place(pw + V(0, .22, 0), V(.06, 1, .12), V(.25, -.12, 1), .25)); st.close()
        gem = pw + V(0, .22, 0) + nz(V(.06, 1, .12)) * .36; FX.flame(st, gem, .34, seed=1.3, glow=.8 * on, calm=1.2)
        FX.embers(st, 14, (tuple(gem - V(.5, .1, .3)), tuple(gem + V(.5, .4, .3))), t, rise=1.0, size=.018, seed=3, life=1.8); motes(st, t, (tuple(h - V(5, 4, 3)), tuple(h + V(5, 4, 4))), 40, 3)
        FX.drift(st, 8, (tuple(h + V(-5, -3, -6)), tuple(h + V(5, 4, -1.5))), t, 'petal', .13, '#b02a24', .7, .5, seed=12)
        IM.dof(st, float((h - cam.eye) @ cam.R[2]), 6., 5.)
        return st.finish(bloom=.45, thr=.9, vig=.55, satu=1.0, contrast=1.06)

    def eyes(self, f, st, t):
        g = on2(f); u = (f - 76) / 7.; P = HM.H_PERCH.set(hedr=(0, -2, 5)); S = st.fig(HM.HANUMAN_CU, P, draw=False); h = S.head((0, .05, .5)); fw = S.d((0, 0, 1)); cam = Cam(h + fw * (9.4 - .6 * u) + V(.2, -2.0, 0), h + V(0, .0, 0), 21, roll=-3); st.cam = cam
        st.paint(BOKEH, warm=.10, c=(960., 700.), lift=.1); lid = keys(f, [(75, .0), (79, .95, 'out'), (82, 1.0)]); fk = 1 + .1 * noise1(t * 8, 4); g = smooth(76, 79, f)
        L = Light(key=(.6, .7, -.1), keyCol=(.07, .10, .22), amb=(.030, .040, .095), rim=(.7, .6, -.6), rimCol=(.35, .5, .9), bounceCol=(0, 0, 0), envT='#8fa8ff', envM='#3a4a80', envB='#8a4a24', pts=[(h + fw * 1.1 + V(0, -.25, 0), .75, tuple(np.array([.95, .42, .13]) * fk * g))], shadow=False, ink=3.4)
        st.open(cam, L); st.fig(HM.HANUMAN_CU, P, face=Face(lid=lid, spark=g, glow=.75 * g, smile=.5, gy=-.35, brow=.35)); st.close()
        for x, y, sc, r, fl, ld, tn in ((-120, -330, .95, 14, False, .6, 1.), (2060, -360, .95, -16, True, .6, 1.), (240, -600, .85, 6, False, 1.2, .8), (1700, -600, .85, -4, True, 1.2, .8), (-420, 1640, .95, -60, False, .8, .9), (2360, 1660, .95, 60, True, .8, .9), (150, 1800, .85, -84, False, 1.6, .7), (1800, 1820, .85, 84, True, 1.6, .7)): FL.frame(st, 'fg_leaves', x - 10 * u * (1 if x < 960 else -1), y, sc, 'night', 0, rot=r + 1.2 * math.sin(t * 2 + x), flip=fl, lod=ld, tint=(.62 * tn, .70 * tn, .95 * tn))
        for sx in (1, -1):
            q = S.head((.358 if sx > 0 else -.41, .11, .98)); FX.flame(st, q - V(0, .06, 0), .15 * g, seed=2.1 + sx, glow=.10 * g, calm=1.3)
        motes(st, t, (tuple(h - V(4, 3, 2)), tuple(h + V(4, 3, 5))), 24, 3)
        return st.finish(bloom=.5, thr=.85, vig=.6, contrast=1.06)
