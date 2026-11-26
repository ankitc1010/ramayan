"""d8 (168): Lanka burning, one take.  The tail is a brush and the city the page: out of the window (f0), roof to roof beside him (lands f12 24 30 42), under the bridge he leaps (f48),
straight down on the curl he writes (f54-84), behind him up the palace as the towers catch (f84-108), the spring against the moon (f110-126), and back over black water until the island is a lamp (hiss f150)."""
from .lanka_kit import *
from chars import hanuman as HM, rakshasa as RK

BRIDGE = '''
#define TMAX 1400.
#define STEPS 110
#define NOAO
#include "arch.glsl"
#include "paint.glsl"
uniform float burn;
const vec3 BP=vec3(0.,296.,648.);
vec2 map(vec3 p){vec3 q=p-BP;float bb=sBox(q-vec3(0,66,0),vec3(124,84,24),0.);if(bb>12.) return vec2(bb,0.);vec3 a=vec3(abs(q.x),q.yz);
 float d=sBox(q-vec3(0,58,0),vec3(118,58,14),.4);d=max(d,-oArch(q.xy,62.,44.,5.));float s=oArch(vec2(abs(q.x)-93.,q.y),16.,62.,3.);d=max(d,-s);
 vec2 m=vec2(d,M_COL);float rb=max(abs(oArch(q.xy,62.,44.,5.)+3.)-2.2,abs(abs(q.z)-14.)-1.2);m=U(m,vec2(max(rb,-q.y),M_GOLD));
 m=U(m,vec2(min(sBox(q-vec3(0,116,0),vec3(122,2.2,17),.3),sBox(q-vec3(0,108,0),vec3(119,1.2,15.5),.2)),M_GOLD));
 vec3 c=vec3(q.x-11.*round(q.x/11.),q.y-118.,abs(q.z)-15.);float bl=max(sCyl(c-vec3(0,5,0),1.1+.7*sin(c.y*.9),5.,.1),abs(q.x)-118.);m=U(m,vec2(min(bl*.8,sBox(vec3(q.x,q.y-129.,abs(q.z)-15.),vec3(119,1.3,1.8),.2)),M_GOLD));
 m=U(m,aChhatri(a-vec3(96,118,0),13.));
return m;}
void surf(vec3 p,vec3 n,int m,inout Surf s){pNight=1.;vec3 q=p-BP;if(m==2||m==3||m==8){s.cls=2.;s.base=vec3(1.05,.95,.85);s.sh=s.base*.5;s.ink=.7;return;}if(m==11){s.cls=4.;s.base=vec3(1.6,.75,.2);return;}
 vec3 w=hex(0x4f3642),sh=hex(0x2a1d34);if(abs(n.z)>.6){pPave(s,q.xy,vec2(15.,8.),w,sh,.6);oAA=gPx;float d=oArch(q.xy,62.,44.,5.);if(d>6.&&d<8.){s.cls=2.;s.base=vec3(1);}oAA=gPx/9.;float by=(q.y-98.)/9.;if(by>0.&&by<1.&&oVine(vec2(q.x/11.,by))>.5){s.cls=2.;s.base=vec3(1.1);}}else{pPave(s,q.xz,vec2(9.,9.),w*.9,sh,.6);}
 s.ink=.7;float u=q.x;float g=exp(-max(q.y,0.)*.016);emit(s,vec3(.9,.26,.05)*(.10+burn*(.5*g+.35*smoothstep(0.,-1.,n.y))));}
'''


MIRROR = """
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform sampler2D tex;uniform vec2 res;uniform float y0,amt,fT;
void main(){vec3 c=texture(tex,uv).rgb;float y=(1.-uv.y)*res.y,d=y-y0;if(d>0.){float k=d/res.y;float w=vn(vec2(uv.x*res.x*.012+3.*sin(fT*.7),d*.16/(.35+k)-fT*3.))-.5,w2=vn(vec2(uv.x*res.x*.05,d*.42/(.4+k)-fT*5.))-.5;vec2 u=vec2(uv.x+(w*26.+w2*12.)*(.25+2.2*k)/res.x,1.-(y0-d*1.0+w*30.*k)/res.y);
 vec3 m=textureLod(tex,u,1.).rgb;m=max(m-.22,0.)*1.15;float br=smoothstep(.30,.62,vn(vec2(uv.x*res.x*.010+w*2.,d*.20/(.30+k)-fT*2.2))+.22-.55*k);c+=m*vec3(1.,.72,.55)*amt*br*smoothstep(0.,14.,d)*(1.-.55*k/.35);}o=vec4(c,1);}
"""


def spline_keys(f, K):
    """smooth curve through (frame, tuple) keys, without overshoot"""
    x = np.array([k[0] for k in K], float); Y = np.array([k[1] for k in K], float); f = clamp(f, x[0], x[-1]); h = np.diff(x); d = np.diff(Y, axis=0) / h[:, None]; m = np.zeros_like(Y); m[0], m[-1] = d[0], d[-1]
    for i in range(1, len(x) - 1): s = d[i - 1] * d[i]; m[i] = np.where(s > 0, 2 * s / (d[i - 1] + d[i] + 1e-12 * np.sign(d[i - 1] + d[i] + 1e-30)), 0.)
    i = min(int(np.searchsorted(x, f, 'right')) - 1, len(h) - 1); t = (f - x[i]) / h[i]
    return (2 * t ** 3 - 3 * t ** 2 + 1) * Y[i] + (t ** 3 - 2 * t ** 2 + t) * h[i] * m[i] + (3 * t ** 2 - 2 * t ** 3) * Y[i + 1] + (t ** 3 - t ** 2) * h[i] * m[i + 1]


# frame: (yaw of the eye round him, its pitch, distance, height of the target over his feet, fov)
CAM = [(0, (-36, 3, 46, 11, 42)), (10, (-70, 2, 50, 11, 42)), (24, (-90, 0, 56, 11, 42)), (33, (-112, -2, 60, 10, 44)), (42, (-150, -14, 76, 10, 52)), (50, (-186, -30, 100, 12, 55)), (57, (-224, 20, 190, 8, 56)), (64, (-262, 66, 340, 0, 50)), (72, (-298, 84, 470, 0, 48)), (79, (-328, 82, 470, 0, 48)),
       (87, (-350, 40, 310, 6, 46)), (95, (-362, 22, 250, 10, 46)), (101, (-366, 2, 135, 14, 48)), (108, (-361, -15, 50, 13, 50)), (118, (-360, -9, 62, 15, 46)), (126, (-360, -5, 92, 10, 42))]
UNDER = [(36, (66, 532, 446)), (42, (58, 482, 508)), (46, (38, 412, 572)), (49, (12, 366, 618)), (52, (-2, 345, 655)), (55, (-18, 362, 696)), (58, (-44, 430, 724)), (62, (-110, 560, 700)), (66, (-190, 660, 600))]      # through the arch of the bridge


H = HM
RISE = H.H_LEAP.set(hedr=(-6, -8, 0))
GLIDE = H.H_FLY_L
REACH = H.H_LEAP.set(pel=(0, 7.4, 0), pelr=(0, -24, 0), cher=(0, 34, 0), hedr=(0, -10, 0), lh=(5.4, 11.8, -1.6), rh=(-5.2, 12.4, -.6), lel=(.6, .2, -1), rel=(-.6, .2, -1), lhand='open', rhand='open', lfing=(.8, .5, -.2), rfing=(-.8, .5, -.2), lf=(1.1, 3.2, 4.6), rf=(-1.0, 4.6, 2.6), lkn=(.3, .8, 1), rkn=(-.3, .8, 1), lft=(6, -24), rft=(-6, -8))
TUCK = H.H_CROUCH.set(pel=(0, 7.4, 0), pelr=(0, 48, 0), cher=(0, 40, 0), hedr=(0, 20, 0), lf=(1., 5.4, 2.4), rf=(-1., 5.4, 2.4), lh=(2.2, 6.4, 3.4), rh=(-2.2, 6.4, 3.4))
HANG = H.H_LEAP.set(pel=(0, 8.6, 0), pelr=(0, -6, 0), cher=(0, -10, 0), hedr=(0, 14, 0), lh=(5.6, 14.6, 1.2), rh=(-5.6, 14.6, 1.2), lel=(.5, -.6, -.8), rel=(-.5, -.6, -.8), lhand='open', rhand='open', lfing=(.55, .8, .2), rfing=(-.55, .8, .2), lpalm=(-.3, 0, 1), rpalm=(.3, 0, 1), lf=(1.5, 4.4, 1.6), rf=(-1.2, 2.4, -1.4), lkn=(.6, .4, 1), rkn=(-.3, 0, 1), lft=(14, 30), rft=(-10, 70))
CLIMB = H.H_LEAP.set(lh=(2.4, 17.2, 2.0), lel=(1, 0, -.4), lhand='claw', lfing=(0, 1, .2), lpalm=(0, 0, 1), rhand='claw')


def act(f):
    """pose and pitch of his flight at frame f"""
    if f < 108:
        a = max(k for k in LF if k <= f); b = min(k for k in LF if k > f); u = (f - a) / (b - a); end = H.H_LAND if b < 96 else H.H_CROUCH; fly = GLIDE if a < 54 else H.H_FLY2 if a < 84 else CLIMB
        if a == 0: return keys(f, [(0, GLIDE), (6, GLIDE), (9, REACH), (12, H.H_LAND, 'in')]), 0.
        if b - a == 6 and a < 60: return keys(f, [(a, H.H_LAND), (a + 2, H.H_CROUCH, 'out'), (a + 3, RISE, 'out'), (a + 4, REACH), (b, end, 'in')]), 0.
        if a == 42: return keys(f, [(a, H.H_LAND), (a + 2, H.H_CROUCH, 'out'), (a + 4, RISE, 'out'), (a + 6, TUCK), (a + 8, TUCK), (a + 10, REACH, 'out'), (b, end, 'in')]), 360 * ease_io(clamp((f - 45) / 6.), 1.4)
        if b - a == 6: return keys(f, [(a, H.H_CROUCH if a >= 84 else H.H_LAND), (a + 2, H.H_CROUCH, 'out'), (a + 4, CLIMB, 'out'), (b - 1, CLIMB), (b, end, 'in')]), 0.
        return keys(f, [(a, H.H_LAND), (a + 2, H.H_CROUCH, 'out'), (a + 4, RISE, 'out'), (a + 6, fly), (b - 4, fly), (b - 2, REACH), (b, end, 'in')]), 0.
    if f < 126: return keys(f, [(108, H.H_CROUCH), (110, H.H_CROUCH.set(pel=(0, 2.6, -1.6))), (112, H.H_LEAP, 'out'), (116, H.H_LEAP), (120, HANG, 'out'), (126, HANG)]), 0.
    return keys(f, [(126, HANG), (131, H.H_FLY, 'io')]), 78 * smooth(126, 134, f)


YAW = [(0, 40.), (12, 10.), (24, 0.), (42, 0.), (46, -50.), (54, -62.)]


def yaw_of(f):
    if f < 54: return keys(f, YAW)
    if f < 84: v = heading(f, 3.); return math.degrees(math.atan2(v[0], v[2]))
    if f < 108: return keys(f, [(84, 150.), (88, 162.), (96, 172.), (108, 180.)])
    return keys(f, [(108, 180.), (112, 180.), (119, 360., 'io')]) if f < 126 else 360. - 12 * smooth(126, 134, f)


def scale_of(f): return SC * (1 + .75 * smooth(57, 66, f) * (1 - smooth(99, 107, f)))


class Shot(ShotBase):
    id = 'd8'; n = 168
    EVENTS = [(0, 'lattice bursts', {}), (0, 'tail fire', dict(dur=150)), (2, 'city wind', dict(dur=165)), (12, 'land on roof', {}), (15, 'leap', {}), (16, 'roof catches', {}), (24, 'land on roof', {}), (27, 'leap', {}), (28, 'roof catches', {}), (30, 'land on roof', {}), (33, 'leap', {}), (36, 'roof catches', {}), (42, 'land on roof', {}), (45, 'leap', {}), (48, 'somersault whoosh', {}), (51, 'under the bridge', dict(dur=5)), (54, 'land on roof', {}), (56, 'fire stroke', dict(dur=30)), (60, 'camera up', dict(dur=10)), (66, 'land on roof', {}), (72, 'land on roof', {}), (70, 'crowd cries', dict(dur=34)), (84, 'land on roof', {}), (87, 'great leap', {}), (90, 'land on terrace', {}), (91, 'towers catch', {}), (96, 'land on palace', {}), (97, 'towers catch', {}), (102, 'land on tower', {}), (108, 'land on the top', {}), (110, 'spring', {}), (112, 'city goes up', dict(dur=40)), (118, 'hang', dict(dur=8)), (127, 'dive', dict(dur=23)), (138, 'wall of fire', dict(dur=30)), (150, 'hiss in the sea', {}), (152, 'steam', dict(dur=10)), (156, 'lamp picture', {})]

    def setup(self, st):
        self.sm = np.array([self._smooth(f) for f in range(-2, 172)]); self.s2 = np.array([self._smooth(f, 2.) for f in range(-2, 172)]); self.moon = nz(V(.02, .40, -1)); arrival(); fire_points(); folk(); st.cam = Cam((0, 5, 40), (0, 5, 0), 30)
        self.cr = Crowd(st, [(k, RK.K_RUN(i / 4), Face(mouth=.5), 80) for k in (RK.SPEARMAN, RK.HORN) for i in range(4)], px=150, pitch=30)

    def _smooth(self, f, sg=4.2):
        w = [(k, math.exp(-(k / sg) ** 2)) for k in range(-9, 10)]; return sum(hero(clamp(f + k, -2, 126)) * a for k, a in w) / sum(a for _, a in w)

    def cam(self, f):
        g = min(f, 126); yaw, pit, dist, up, fov = spline_keys(g, CAM); tg = self.sm[int(round(g)) + 2] + V(0, up, 0); tg[1] += lerp(.80, .92, smooth(90, 98, g)) * (self.s2[int(round(g)) + 2][1] - tg[1] + up); tg = lerp(tg, CURL + V(0, 360, 0), .62 * smooth(60, 70, g) * (1 - smooth(80, 87, g))); a, b = math.radians(yaw), math.radians(pit); eye = tg + dist * V(math.sin(a) * math.cos(b), math.sin(b), math.cos(a) * math.cos(b))
        if f > 120:
            e = ease_io((f - 124) / 34., 1.7); d = 120 * (5050 / 120.) ** e * (1 + .035 * smooth(150, 168, f)); e2 = V(0, lerp(1330, 165, smooth(.38, 1., e)), d - 20); pt = math.radians(keys(f, [(120, 5.), (126, 4.), (134, -21.), (140, -17.), (151, 3.6), (158, 4.9)])); home = e2 + d * V(0, math.sin(pt), -math.cos(pt)); k = smooth(124, 130, f)
            return Cam(lerp(eye, e2, k), lerp(tg, home, k), lerp(fov, 35, smooth(.0, .7, e)))
        if 36 < f < 66: k = smooth(36, 43, f) * (1 - smooth(57, 66, f)); eye = lerp(eye, spline_keys(f, UNDER), k); tg = lerp(tg, LAND[54] + V(0, 12, 0), smooth(48, 53, f) * (1 - smooth(55, 60, f)))
        return Cam(eye, tg, fov)

    def man(self, st, f, draw=True):
        g = on2(f) if 54 > f or 108 <= f < 126 else f; P, pit = act(g); hp = hero(f); sc = scale_of(f); R = eul(yaw_of(f), pit, 0) * sc; M = np.eye(4); M[:3, :3] = R; M[:3, 3] = hp + V(0, 8 * sc, 0) - R @ V(0, 8, 0)
        F = Face(smile=.35, frown=.35) if f < 112 else Face(smile=.5, spark=1., gy=-.3)
        if draw and 108 < f < 126: HM.sash
        return st.fig(HM.HANUMAN, P, M=M, face=F, draw=draw)

    def tailpath(self, f):
        """what his tail does: it streams along his way and lashes; at the spring it winds into a spiral"""
        t = f / 24.; sp = smooth(111, 119, f) * (1 - smooth(126, 131, f)); hd = heading(f); n = nz(np.cross(hd + V(0, 1e-3, 0), V(0, 1, 0))); cr = self.camR

        def fn(tt):
            q = clamp((t - tt) / .42) ** (1 / 1.2); d_ = hero(tt * 24) - hero(f); s = d_ * min(.5, 34. / (np.linalg.norm(hero(f - 8.) - hero(f)) + 1e-6))
            s = s + (n * math.sin(q * 7.5 - t * 15) * 11 + V(0, 1, 0) * math.cos(q * 6.0 - t * 13) * 8) * q ** 1.2
            if sp > 0: Ln = 108.; r0, bb = 9., 2.0; th = (-r0 + math.sqrt(r0 * r0 + 2 * bb * q * Ln)) / bb; a = -1.57 - th; r = r0 + bb * th; s = s * (1 - sp) + sp * 5 * (cr[0] * math.cos(a) * r + V(0, 1, 0) * (math.sin(a) * r) + V(0, 0, -1) * 5 * min(1, q * 4))
            return s
        return fn

    def taillen(self, f): return lerp(20, 72, smooth(111, 119, f) * (1 - smooth(127, 134, f)))

    def brush(self, f, P):
        """the stroke in the air behind the tail"""
        n = 26 if f < 54 else 34 if f < 84 else 7; a = max(1., f - n); F = np.linspace(a, f - 2.5, 40); Q = np.array([trail(q) + V(0, 13 + 12 * smooth(55, 62, q) * (1 - smooth(80, 86, q)), 0) + V(0, .34, 0) * (f - q) + 3.2 * V(math.sin(q * 1.3), math.cos(q * 1.1) * .8, math.sin(q * .9 + 2)) for q in F]); Q = np.vstack([Q, P[-8:]]); return CL.spline(Q[::2], 150)

    def frame(self, f, st):
        st.clear('#000', f=f); t = st.t; cam = self.cam(f); st.cam = cam; self.camR = cam.R; hp = hero(f); w = smooth(105, 118, f)
        m = smooth(128, 150, f); st.paint('sky.frag', **sky(w)); LK.moon(st, R=lerp(.25, .150, m), dir=nz(V(.0, lerp(.27, .185, m), -1)), cA=hx(hx('#dfe0e8', '#ffb868', w), '#a83a16', m), cB=hx(hx('#8d9ac0', '#c8582c', w), '#6a1a12', m), cG=hx('#5a6cc8', '#d04c1c', w), glow=.6)
        S = self.man(st, f, False); fd = heading(f); tl = hp + V(0, 10, 0) - nz(fd + V(0, 1e-3, 0)) * 13; fl = .9 + .1 * noise1(t * 9, 3); zc = float(np.linalg.norm(cam.eye - hp))
        pts = [(tuple(tl + V(0, 4, 0)), 13., (1.5 * fl, .58 * fl, .13 * fl)), (tuple(hp + V(0, 2, 0) - nz(fd + V(0, 1e-3, 0)) * 40), 22., (.8, .26, .05)), (tuple(hp + V(0, 14, 0) + nz(cam.eye - hp) * 16 - cam.R[0] * 12), 13., (1.5, .72, .26))]
        st.open(cam, light(w, pts=pts, inkRef=float(clamp(zc / 60., 1.5, 14.))), far=16000.)
        city(st, t, w)
        if f < 90: st.world(BRIDGE, u=dict(burn=float(smooth(1.6, 2.6, t)), uAmb=hexc(st.light.amb), uKey=hexc(st.light.keyCol), sunSh=0.), head='place_head.glsl', main='place_main.glsl')
        top = smooth(56, 66, f) * (1 - smooth(82, 92, f))
        if f < 120:
            Q, D, run, R, T = folk_at(t); side = np.sign(D @ cam.R[0] + 1e-6); self.cr.draw(Q, 1.15, ((t * 9 * (.8 + .4 * R[:, 1]) + R[:, 2] * 4).astype(int) % 4 + 4 * (R[:, 0] > .5)) * run + 1 * (~run), side, tint=np.array([.42, .34, .40]) + 0 * Q, upright=1 - .8 * top)
        if f < 150: S = self.man(st, f)
        if f < 140: P = HM.tail(st, S, t, 'fly', length=self.taillen(f), wrap=1, path=self.tailpath(f), ground=None)
        st.close()
        if f < 110:
            Q, D, run, R, T = folk_at(t); m = R[:, 0] > .62; FX.particles(st, Q[m] + V(0, 15, 0), 4.5, (1.0, .42, .10), 'lamp', seed=R[m, 1], alpha=.9 * np.minimum(1, np.linalg.norm(Q[m] - cam.eye, axis=1) / 90 - .4).clip(0, 1))
        if f < 12: self.window(st, f)
        if f < 112 or f > 146: smoke(st, t, cam)
        self.nf = flames(st, t, cam, 1700, near=14. if f < 58 else 36.)
        if f > 122: self.great(st, f, cam)
        if 4 < f < 110: FX.ribbon(st, self.brush(f, P), np.array([.2, 3.4, 4.6, 3.6, 1.2]) * (1 + 2.2 * top + 1.2 * (f > 84)), 'fire', amt=1.0, seed=2., blend='add')
        if f < 140: HM.tail_fire(st, P, t, .12, 1., 1.7, S.Sc)
        if f < 130: c0 = cam.at * .75 + cam.eye * .25; FX.embers(st, 150, (tuple(c0 - V(70, 60, 70)), tuple(c0 + V(70, 20, 70))), t, rise=26, size=.42 if not top else .9, seed=9, life=2.2, swirl=8.)
        if f >= 126: self.dive(st, f, cam, hp)
        if f > 141: st.post_paint(MIRROR, y0=float(cam.project(V(0, 0, 250))[1]), amt=.55 * smooth(141, 154, f))
        IM.zoomblur(st, (960, 520), .016 * sum(math.exp(-((f - q) / 1.8) ** 2) for q in (87, 93, 99, 105)))
        return st.finish(bloom=.42, thr=.95, vig=.4, contrast=1.07)

    def window(self, st, f):
        """he has come through the stone lattice: pieces, a breath of fire in the arch behind him"""
        a = (f + 1) / 24.; w = V(32, 664, 107); FX.burst(st, 46, w, a, speed=52, grav=60, size=1.1, seed=3, col='#3a2430', kind='flake', life=1.1, spread=(1, .7, .4)); FX.burst(st, 60, w + V(0, 0, 4), a, speed=70, grav=10, size=.5, seed=4, col='#ffb050', life=.7, stretch=.05)
        k = 1 - smooth(5, 12, f); r = np.random.default_rng(2); P = w + r.uniform(-1, 1, (9, 3)) * [6, 5, 2]; FX.particles(st, P + V(0, 2, 2), 4.2 * k * r.uniform(.6, 1.2, 9), (.95, .80, .66), 'tongue', seed=r.uniform(0, 1, 9), vel=np.tile([[9., 10., 10.]], (9, 1)) * k * r.uniform(.7, 1.3, (9, 1)))

    def great(self, st, f, cam):
        """far away the fires of the city draw together into one flame, and the sea holds it upside down"""
        g = smooth(141, 155, f); br = 1 + .03 * math.sin(f * .42); r = np.random.default_rng(21); n = 120; a = r.uniform(0, 6.283, n); rad = 1050 * np.sqrt(r.uniform(0, 1, n)); x, zz = rad * np.sin(a), rad * np.cos(a) * .55; e = np.clip(1 - np.abs(x) / 1130., 0, 1)
        h = (150 + 730 * e ** 1.6) * g * (.8 + .4 * r.uniform(0, 1, n)) * br; y = np.array([LK.RIM + 36 * round(LK._hill(p, q) / 36) for p, q in zip(x, zz)]) + 90 * e; d = np.c_[-x * .30 * e, h, 0 * x]; P = np.c_[x, y, zz] + d * .46; o = np.argsort(zz)
        sd = r.uniform(0, 1, n); FX.particles(st, P[o], (h * .34)[o], (.95, .82, .70), 'tongue', seed=sd[o], vel=d[o], alpha=.92 * g * np.clip(((P[o] - cam.eye) @ cam.R[2] - 700) / 600, 0, 1))
        q = r.uniform(0, 1, (260, 4)); lf = (f / 24. * (.22 + .25 * q[:, 0]) + q[:, 1]) % 1.; xx = (q[:, 2] - .5) * 1900 * (1 - lf) ** 1.6; FX.particles(st, np.c_[xx + 40 * np.sin(lf * 9 + q[:, 3] * 30), 420 + 1500 * lf + 200 * q[:, 3], 60 + 0 * lf], 8 * (1 - lf) ** .5, '#ffb050', 'ember', alpha=g * np.minimum(1, lf * 6) * (1 - lf))

    def dive(self, st, f, cam, hp):
        z = max(1., float((hp - cam.eye) @ cam.R[2]))
        if f < 150:
            F = np.linspace(max(126, f - 9), f, 30); Q = np.array([hero(q) + V(0, 10, 0) for q in F]); px = 540 * cam.fl / z; wd = np.linspace(.0, max(3.2, 3.4 / px), 30); FX.ribbon(st, Q, wd, 'fire', amt=1.1, seed=4., blend='add'); FX.particles(st, (hp + V(0, 9, 0))[None], max(9., 30. / px), (1.2, .62, .22), 'lamp')
        else:
            a = (f - 150) / 24.; f < 161 and FX.burst(st, 80, SEA, a, speed=150, grav=170, size=5, seed=6, col='#ffd8a0', kind='drop', life=1.1, spread=(.6, .3, .6), up=.9, drag=.6); r = np.random.default_rng(3); u = r.normal(size=(16, 3)) * [1, .5, .4]; FX.particles(st, SEA + u * (14 + 60 * a) + V(0, 1, 0) * (14 + 70 * a * (1 + u[:, :1])), (16 + 46 * a) * r.uniform(.6, 1.2, 16), (.26, .13, .09), 'smoke', seed=r.uniform(0, 1, 16), alpha=.5 * max(0, 1 - a * 1.7) * smooth(149, 152, f)); FX.particles(st, (SEA + V(0, 20, 0))[None], 90 * max(0, 1 - a * 3), '#ffe8c0', 'glint')
