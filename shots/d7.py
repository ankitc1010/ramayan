"""d7 (84): Ravana's hall.  Hanuman bound, his tail wound in oiled cloth and laid across the floor to the lens; a torch touches its tip (f30) and the fire runs up it toward him, lighting the hall as it comes;
close: one eye opens, a small smile (f48-66); the ropes burst (f66), he goes over the lens trailing fire; guards are thrown back, the ceiling burns gold, and he leaves by the great window (f72-84)."""
from lau.shot import *
from lau.look import *
from lau.stage import hexc
from worlds import palace as PL
from .lanka_kit import hx
from chars import hanuman as HM, rakshasa as RK, ravana as RV
from chars.armonly import ARM, place_hand
from chars.hanuman import VFace

WINDOW = '''
#define TMAX 900.
#define STEPS 110
#define NOAO
#include "arch.glsl"
#include "paint.glsl"
uniform float brk,fire_;
const vec3 WP=vec3(0.,0.,254.);
float lat(vec2 q){vec2 u=mat2(.7071,-.7071,.7071,.7071)*q/9.;vec2 g=abs(fract(u)-.5);float d=min(g.x,g.y)*9.-.9;float r=abs(length(q-vec2(0,46.))-19.)-1.6;return min(d,r);}
vec2 map(vec3 p){vec3 q=p-WP;if(q.z<-30.) return vec2(-q.z-14.,0.);float ar=oArch(q.xy-vec2(0,4.),37.,48.,5.);float d=max(abs(q.z)-6.,-ar);d=min(d,max(abs(abs(ar)-2.6)-1.3,abs(q.z+5.)-3.));float hole=length((q.xy-vec2(0,44.)))-brk-3.*vn(q.xy*.3);
 float l=max(max(lat(q.xy),abs(q.z)-.9),max(ar,-hole));vec2 m=vec2(d,M_COL);m=U(m,vec2(l*.8,M_DARK));m=U(m,vec2(max(abs(q.z-14.)-.4,ar-9.),M_CLOTH));
 m=U(m,vec2(sBox(q-vec3(0,2,-10),vec3(46,2,10),.3),M_STEP));return m;}
void surf(vec3 p,vec3 n,int m,inout Surf s){vec3 q=p-WP;if(m==9){vec2 u=q.xy;vec3 c=mix(hex(0x0c1844),hex(0x03051c),smoothstep(10.,90.,u.y));vec2 w=u-vec2(0.,44.);float r=length(w);c=mix(c,hex(0x2a4488),exp(-max(r-17.,0.)*.06)*.8);
  if(r<17.) c=hex(0xf2ead2)*(1.05-.25*smoothstep(.50,.60,fbm(w*.11+3.)));vec2 id=floor(u/3.);float st=step(.965,h21(id));c+=vec3(.8)*st*smoothstep(.9,.2,length(fract(u/3.)-.5)*4.)*step(17.5,r);
float sk=0.;for(int L=0;L<2;L++){float W=L==0?8.:13.;float k=floor(u.x/W+.5*float(L));float x=u.x-(k+.5-.5*float(L))*W;float hh=7.+11.*h11(k*3.1+float(L)*17.)*(L==0?1.:.7);float r=W*.34;float t=step(abs(x),W*.42)*hh;t=max(t,step(abs(x),r)*(hh+sqrt(max(0.,r*r-x*x))*1.15));t=max(t,step(abs(x),.5)*(hh+r*1.15+3.5*(1.-abs(x)*1.6)));sk=max(sk,t);}if(u.y<sk){c=hex(0x060820);vec2 wi=abs(fract(u/vec2(2.7,4.1))-.5);if(h21(floor(u/vec2(2.7,4.1)))>.84&&max(wi.x*1.4,wi.y)<.16&&u.y<sk-3.) c=vec3(1.2,.55,.14);}
  s.cls=4.;s.base=c;s.ink=0.;return;}
 if(m==12){s.base=hex(0x3a2420);s.sh=hex(0x180c14);s.cls=2.;s.base=vec3(.8,.6,.45);s.ink=.8;return;}
 vec3 w=hex(0x2a1a26),sh=hex(0x140a18);pPave(s,q.xy,vec2(16.,9.),w,sh,.6);oAA=gPx;float ar=oArch(q.xy-vec2(0,4.),37.,48.,5.);if(ar>1.&&ar<4.4){s.cls=2.;s.base=vec3(1.1,1.,.9);}else if(ar>7.&&ar<8.4){s.cls=2.;s.base=vec3(.9);}else{oAA=gPx/12.;float by=(ar-9.)/10.;if(by>0.&&by<1.&&oVine(vec2((q.x+q.y)/12.,by))>.5){s.cls=2.;s.base=vec3(.9,.75,.6);}}
 if(s.cls<1.5) emit(s,vec3(.9,.26,.04)*fire_*.20);s.ink=.7;}
'''
SCH = dict(hold=1)
JEER = RK.K_GUARD.set(rh=(-3.2, 15.2, 1.4), rel=(-1, 0, -.3), rfing=(0, 1, .2), rpalm=(0, 0, 1), rhand='fist', lh=(3.0, 13.8, 2.0), lhand='open', lfing=(.4, .8, .5), lpalm=(-.3, -.2, 1), hedr=(0, -6, 0))
LAUGH = RK.K_GUARD.set(cher=(0, -14, 0), hedr=(0, -14, 0), lh=(1.0, 9.6, 2.2), lhand='flat')
POINT = RK.K_GUARD.set(lh=(2.6, 11.4, 5.4), lhand='point', lfing=(-.2, -.15, 1), lpalm=(0, -1, 0), cher=(-6, 12, 0))
TIP = V(1.6, .5, 28.)
BOUND = HM.H_BOUND
TAILW = [V(0, 2.4, -1.4), V(.4, .9, -3.2), V(5, .5, -5.0), V(9.2, .5, -2.0), V(8.6, .5, 4.0), V(1, .5, 7.0), V(-6.6, .5, 10), V(-7.6, .5, 15.5), V(-1.5, .5, 18.5), V(5.0, .5, 20.5), V(5.6, .5, 24.5), TIP]


def on_floor(P0, Q):
    """displacement that makes hanuman.tail follow the polyline Q"""
    s = CL.spline(Q, 400); L = np.r_[0, np.cumsum(np.linalg.norm(np.diff(s, axis=0), axis=1))]

    def path(T0): return lambda tt: (lambda q: 30. * np.array([np.interp(q * L[-1], L, s[:, i]) for i in range(3)]))(clamp((T0 - tt) / .42) ** (1 / 1.2))
    return path, L[-1]


class Shot(ShotBase):
    id = 'd7'; n = 84
    EVENTS = [(0, 'jeering crowd', dict(dur=66)), (0, 'hall fire', dict(dur=84)), (8, 'ravana chuckles', {}), (18, 'torch comes', dict(dur=12)), (30, 'torch touches tail', {}), (31, 'fire runs', dict(dur=30)), (48, 'silence falls', {}), (54, 'eye opens', {}), (58, 'small smile', {}), (60, 'fire reaches him', {}), (63, 'ropes creak', {}), (66, 'ropes burst', {}), (69, 'leap over the lens', {}), (72, 'guards thrown back', {}), (74, 'roar of fire', dict(dur=10)), (81, 'window breaks', {})]

    def setup(self, st):
        st.cam = Cam((0, 5, 40), (0, 5, 0), 30); F = Face(mouth=.7, teeth=.6, frown=.6)
        self.cr = Crowd(st, [(k, p, F, y) for y in (62, 20) for k, p in ((RK.TUSK, JEER), (RK.HORN, LAUGH), (RK.HULK, POINT), (RK.TUSK, RK.K_GUARD), (RK.HORN, JEER), (RK.ARCHER, LAUGH))], px=330, pitch=4)
        r = np.random.default_rng(7); n = 70; sd = r.choice([-1., 1.], n); self.crp = np.c_[sd * r.uniform(19, 58, n), 0 * sd, r.uniform(-190, -4, n)]; self.crs = r.uniform(0, 1, (n, 3)); self.path, self.tl = on_floor(None, TAILW)

    def frame(self, f, st):
        st.clear('#000', f=f)
        return self.floor(f, st, st.t) if f < 48 else self.close(f, st, st.t) if f < 66 else self.burst(f, st, st.t) if f < 72 else self.out(f, st, st.t)

    def ropes(self, st, S, brk=0., t=0., fine=False):
        """coils of rope round arms and chest; brk > 0 = seconds since they burst"""
        col = ('#a8845a', '#4a3426', '#d8b888'); r = np.random.default_rng(4); c0 = S.chest((0, 0, 0)); X, Y, Z = (S.chest(tuple(e)) - c0 for e in np.eye(3))
        tw = .125 * (1 + .16 * np.sin(np.linspace(0, 2 * math.pi * 34, 193)))
        for k in range(9):
            y = -1.35 + .30 * k; a = np.linspace(0, 2 * math.pi, 193); rx = 3.0 + .10 * math.sin(k * 2.1); rz = 1.95 + .12 * math.cos(k * 1.7); tilt = .10 * math.sin(k * 1.9); R = np.array([c0 + X * math.cos(q) * rx + Z * (math.sin(q) * rz - .25) + Y * (y + tilt * math.cos(q) + .05 * math.sin(3 * q + k)) for q in a])
            if fine:
                T = np.gradient(R, axis=0); T /= np.linalg.norm(T, axis=1, keepdims=True); Nn = np.cross(T, S.d((0, 1, 0))); Nn /= np.linalg.norm(Nn, axis=1, keepdims=True); Bn = np.cross(T, Nn); w = np.linspace(0, 2 * math.pi * 15, len(R))[:, None]
                for q in range(3): st.mesh(*CL.tube(R + .085 * (Nn * np.cos(w + q * 2.094) + Bn * np.sin(w + q * 2.094)), .095, m=8), kind=0, col=col, cls=1, ink=.8, part=float(q + 1))
                continue
            if brk <= 0: st.mesh(*CL.tube(R, tw, m=8), kind=0, col=col, cls=1, ink=.85); continue
            for j in range(4):
                seg = R[j * 48:j * 48 + 49:4]; m = seg.mean(0); d = nz(m - c0 + V(0, .6 * r.normal(), 0) + r.normal(size=3) * .3); ax = nz(r.normal(size=3)); an = brk * r.uniform(8, 20); K = np.cross(ax, np.eye(3)).T; Ro = np.eye(3) + math.sin(an) * K + (1 - math.cos(an)) * K @ K
                g = (1 - math.exp(-2.2 * brk)) / 2.2; st.mesh(*CL.tube((seg - m) @ Ro.T * 1.1 + m + d * r.uniform(34, 70) * g + V(0, 6, 0) * brk - V(0, 26, 0) * brk * brk, .14, m=7), kind=0, col=col, cls=1, ink=.85)

    def glow(self, st, cam, k):
        x, y, z = cam.project(V(0, 66, -300)); st.paint('in vec2 uv;out vec4 o;uniform vec2 res,c;uniform float k;void main(){vec2 d=vec2(uv.x*res.x,(1.-uv.y)*res.y)-c;d/=res.y;d.y*=1.15;float r=dot(d,d);o=vec4((vec3(.75,.10,.015)*exp(-r*26.)+vec3(.35,.05,.01)*exp(-r*7.))*k,0.);}', 'over', c=(float(x), float(y)), k=float(k))

    def ravana(self, st, cam, f, t):
        """the king on his throne, a black shape against the burning wheel, ten pairs of dull eyes"""
        st.open(cam, RV.silhouette('#080207', ink=2., inkRef=6.), far=2000.); b = .5 * math.sin(t * 1.6)
        S = RV.fig(st, RV.R_THRONE, at=(0, 9, -262), scale=7.2, fan=1., arms=.0, eyeglow=.85 + .12 * math.sin(t * 2.2), lids=.6, spread=1.15, mouths=.25 * max(0., math.sin(t * 5)) if f < 30 else 0.); st.close(); return S

    def floor(self, f, st, t):
        g = on2(f); u = f / 47.; burn = clamp((f - 30) / 30.) ** .9; run = 1 - burn; e = ease_io(u, 1.4); cam = Cam(lerp(V(-1.6, 8.2, 46.5), V(-.9, 7.8, 43), e) + V(*shake(f, .04, .9), 0), lerp(V(.2, 7.8, 0), V(.2, 7.4, 0), e), 43, roll=1.5); st.cam = cam
        st.paint('sky.frag', **PL.sky('ravana')); Lk = smooth(30, 48, f); st.open(cam, PL.light('ravana', at=(0, 10, -40), keyCol=tuple(np.array([.075, .022, .020]) * (1 + 3.6 * Lk)), amb=hx('#0c050e', '#26101c', Lk), gain=.30 + .55 * Lk, rimCol=(.55, .10, .03)), far=2000.); st.light.pts = [((0., 7., 24. - 18. * burn), 34., tuple(np.array([1.5, .50, .09]) * Lk))] + st.light.pts; PL.draw(st, 'ravana', lit=.35, polish=False); st.close(); PL.flames(st, 'ravana', lit=.55); self.glow(st, cam, .5 + .3 * Lk); self.ravana(st, cam, f, t)
        # the front of the fire along the tail
        S = st.fig(HM.HANUMAN, BOUND, draw=False); P = HM.tail(st, S, 10., 'calm', length=self.tl, wrap=1, path=self.path(10.), draw=False); fr = P[int(clamp(run) * 71)]; fk = 1 + .12 * noise1(t * 9, 3) + .06 * noise1(t * 21, 5)
        tp = keys(f, [(6, (14, 12, 28)), (20, (6.4, 6.4, 28.5), 'io'), (26, (4.8, 4.2, 28.3)), (30, (2.2, 1.25, 28.2), 'in'), (34, (2.5, 1.6, 28)), (43, (15, 10, 28), 'in')]); th = np.array(tp) + V(.06 * math.sin(f * .9), .05 * math.cos(f * .7), 0)
        pts = [(tuple(th + V(0, .8, 0)), 5., (1.5 * fk, .62 * fk, .18 * fk))]
        if f >= 30: pts = [(tuple(fr + V(0, 2.4, 0)), 8., tuple(np.array([1.6, .62, .16]) * fk * smooth(29, 33, f)))] + ([(tuple(P[int(lerp(run, 1, q) * 71)] + V(0, 2.4, 0)), 9., tuple(np.array([.9, .32, .07]) * fk)) for q in (.35, .75)] if burn > .1 else []) + pts
        pts += [((0., 13., 11.), 6., (.34, .15, .07))]
        pts += [((sx * 34., 15., z), 14., (.45, .11, .02)) for sx in (-1, 1) for z in (-24., 24.)]
        L = Light(key=(-.3, .5, -.7), keyCol=(.16, .05, .035), amb=(.030, .014, .030), rim=(.2, .5, -.9), rimCol=(.95, .22, .05), bounceCol=(.14, .03, .01), envT='#4a1420', envM='#c8541c', envB='#ff7a2a', pts=pts, shadow=False, ink=3., inkCol='#050204', inkRef=1.2, fogCol='#240408', fog=(.0022, 80., 0, 0))
        st.open(cam, L, far=2000.)
        bt = ((t * 5.2 * (.7 + .6 * self.crs[:, 0]) + self.crs[:, 1] * 6).astype(int) % 3 == 0) * 1. if f < 40 else 0 * self.crs[:, 0]
        self.cr.draw(self.crp + np.c_[0 * bt, 1.0 * bt, 0 * bt], 1.05 + .2 * self.crs[:, 2], (self.crs[:, 1] * 6).astype(int), -np.sign(self.crp[:, 0]) * -1., tint=(.30, .24, .27))
        S = st.fig(HM.HANUMAN, BOUND.set(hedr=(0, 30 + .8 * math.sin(t * 1.5), 0)), face=Face(lid=.0, smile=.1)); self.ropes(st, S); HM.tail(st, S, 10., 'calm', length=self.tl, wrap=1, path=self.path(10.))
        for k, (fig, pose, at, yaw) in enumerate([(RK.HULK, LAUGH, V(-14, 0, 20), 120), (RK.HORN, POINT, V(15.0, 0, 13), -118), (RK.TUSK, JEER, V(-17, 0, 2), 105), (RK.TUSK, POINT, V(18, 0, -4), -100)]):
            h_ = math.sin(g * .55 + k * 1.9); pose = pose.set(cher=(pose.cher[0], pose.cher[1] - 9 * max(0., h_), pose.cher[2]), hedr=(pose.hedr[0], pose.hedr[1] - 8 * max(0., h_), 0), rh=(pose.rh[0], pose.rh[1] + 1.1 * h_, pose.rh[2]), lh=(pose.lh[0], pose.lh[1] + .8 * math.sin(g * .55 + k * 1.9 + 1.2), pose.lh[2]), pel=(pose.pel[0], pose.pel[1] - .25 * abs(h_), pose.pel[2])); st.fig(fig.variant(u=dict(hold=0, shield=0)), pose, at=at, yaw=yaw, face=Face(mouth=.35 + .4 * max(0., h_), teeth=.7, frown=.5))
        # the torch and the arm that brings it
        ax = nz(V(.50, .86, .12)); grip = th + ax * 3.4
        A = ARM.variant(pal={1: ('#7a4434', '#2c1018', 1)}, u=dict(side=1, band=2, old=0., fur=0.)); Pa = PZ.STAND.set(rh=(-3.0, 8.4, 3.2), rel=(-1, -.3, 0), rhand='grip', rfing=(0, 0, 1), rpalm=(0, -1, 0)); Sa = st.fig(A, Pa, draw=False)
        if f < 44: st.mesh(*CL.tube(np.array([th - ax * .2, th + ax * 2., th + ax * 5.2]), np.array([.42, .26, .20]), m=12), kind=0, col=('#4a2c1c', '#1c0e0c', '#8a5a34'), cls=1); st.mesh(*CL.tube(np.array([th - ax * .35, th + ax * .9]), np.array([.40, .52]), m=12), kind=0, col=('#2a1410', '#100608', '#5a2c1c'), cls=1); st.fig(A, Pa, M=place_hand(Sa, 'R', grip, nz(V(-.80, .46, -.20)), nz(V(.15, .1, -1.)), 1.35))
        st.close()
        if f < 46: r = np.random.default_rng(5); n = 9; q = r.uniform(0, 1, n); FX.particles(st, th + np.c_[r.normal(0, .18, n), .55 + .55 * q, r.normal(0, .18, n)], .55 + .75 * q, (.95, .82, .66), 'tongue', seed=r.uniform(0, 1, n)); FX.embers(st, 16, (tuple(th - V(.4, 0, .4)), tuple(th + V(.4, .6, .4))), t, rise=3.2, size=.05, seed=4, life=1.4)
        if f >= 29:
            k = smooth(29, 34, f); HM.tail_fire(st, P, t, run, 1., .85 * k, 1.15)
            if f < 42: FX.burst(st, 70, TIP, (f - 30) / 24., speed=9, grav=9, size=.07, seed=8, col='#ffc060', life=.8, up=.9, spread=(1, .7, 1))
            if f >= 30: FX.burst(st, 40, fr, ((f - 30) % 8) / 24., speed=6, grav=8, size=.05, seed=max(0, (f - 30) // 8), col='#ffb050', life=.5, up=.9)
        FX.embers(st, 50, ((-30, 2, -60), (30, 10, 30)), t, rise=5., size=.09, seed=14, life=3.)
        return st.finish(bloom=.45, thr=.9, vig=.55, contrast=1.08)

    def close(self, f, st, t):
        u = (f - 48) / 17.; g = on2(f); strain = smooth(60, 66, f); lift = keys(g, [(48, 30.), (53, 30.), (57, 22., 'out'), (62, 20.), (66, 10., 'in')]); P = BOUND.set(hedr=(-4, lift, 2), cher=(0, 10 + 2 * math.sin(t * 1.6) - 6 * strain, 0), shrug=(.25 + .3 * strain, .25 + .3 * strain)); S = st.fig(HM.HANUMAN_CU, P, draw=False); h = S.head((0, 0, .4)); fw = S.d((0, 0, 1))
        cam = Cam(h + fw * (8.6 - 1.5 * ease_io(u)) + V(-1.6 + .4 * u, -2.4, 0) + V(*shake(f, .06 * strain, 1.), 0), h + V(.1, -.30, 0), 25, roll=-2); st.cam = cam; arrive = smooth(50, 62, f); fk = 1 + .12 * noise1(t * 10, 4) + .06 * noise1(t * 23, 2)
        st.paint('''
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform vec2 res;uniform float fT,k;
void main(){vec2 p=(uv-.5)*vec2(res.x/res.y,1.);vec3 q=mix(hex(0x0c0308),hex(0x2c080a),smoothstep(-.5,.5,uv.y-.4+.4*(fbm(p*2.)-.5)));for(int i=0;i<6;i++){float x=(float(i)-2.5)*.42+.06*sin(float(i)*3.);float w=.07;float c=smoothstep(w,w-.02,abs(p.x-x-.015*sin(p.y*26.+float(i))));q=mix(q,hex(0x180609)*(1.+.8*k),c*.7);}
 vec2 d=p-vec2(.75,-.62);float r=length(d*vec2(1.,.8));float fl=.85+.15*vn(vec2(fT*7.,1.));q+=(hex(0xff5a14)*exp(-r*r*2.6)*.75+hex(0xffa040)*exp(-r*r*9.)*.55)*k*fl;d=p-vec2(-.9,.55);q+=hex(0x7a1408)*exp(-dot(d,d)*3.)*.35;o=vec4(q*(.92+.14*fbm(uv*vec2(9.,6.))),1);}
''', k=float(arrive))
        L = Light(key=(-.5, .5, .5), keyCol=(.16, .055, .05), amb=(.050, .026, .048), rim=(.75, .25, -.6), rimCol=tuple(np.array([1.9, .70, .16]) * (.15 + .85 * arrive) * fk), bounceCol=tuple(np.array([.32, .10, .02]) * arrive), envT='#5a1420', envM='#ff8a3a', envB='#ffb04a', pts=[(h + V(3.2, -1.2, 2.2), 3.4, tuple(np.array([1.15, .46, .13]) * arrive * fk)), (h + V(-2.6, -2.5, 3.5), 3., (.22, .05, .03))], shadow=False, ink=3.4)
        e1 = keys(f, [(53, 0.), (54, .55, 'out'), (56, 1.0, 'out')]) if f > 53 else 0.; sm = keys(f, [(48, 0.), (56, .05), (60, .55, 'out')])
        st.open(cam, L); S = st.fig(HM.HANUMAN_CU, P, face=VFace(lid=.95 if e1 > 0 else .02, lidL=e1 if e1 > 0 else 1., lidR=.03 if e1 > 0 else 1., smile=sm, spark=e1 * smooth(54, 57, f), gx=.05, gy=.15, brow=.25 * smooth(54, 58, f), frown=.15 + .25 * strain)); self.ropes(st, S, fine=True); st.close()
        # the fire arrives behind him
        r = np.random.default_rng(8); n = 46; x = r.uniform(-2, 7, n); s = r.uniform(.8, 2.4, n) * smooth(52, 62, f); Q = h + np.c_[x + 1.0, -3.6 + s * .7, -3.5 - r.uniform(0, 3, n)]; o = np.argsort(Q[:, 2]); FX.particles(st, Q[o], s[o], (.95, .80, .62), 'tongue', seed=r.uniform(0, 1, n)[o], alpha=.95)
        FX.embers(st, 60, (tuple(h + V(-3, -4, -4)), tuple(h + V(6, -1, 3))), t, rise=3.4, size=.045, seed=3, life=1.8)
        IM.dof(st, float((h - cam.eye) @ cam.R[2]), 6., 5.)
        return st.finish(bloom=.5, thr=.9, vig=.55, contrast=1.08)

    def burst(self, f, st, t):
        """the ropes fly; he rises and goes over the lens"""
        a = (f - 66) / 24.; up = keys(f, [(66, 0.), (67, .8, 'out'), (68, 1.0), (69, 1.08), (72, 2.35, 'linear')]); ROAR = HM.H_ROAR; LEAP = HM.H_LEAP.set(hedr=(0, -4, 0)); P = BOUND.mix(ROAR, min(1, up)) if up <= 1 else ROAR.mix(HM.H_FLY2.set(pelr=(0, 60, 0), hedr=(0, -34, 0)), min(1., up - 1))
        k = max(0., up - 1); at = V(.6 * k, 2.0 * min(up, 1) + 1.0 * k, 19 * k ** 1.4); cam = Cam(V(-1.5, 3.0, 29), V(0, 9.5 + 3.5 * k, 0), 46, roll=3); st.cam = cam; fk = 1 + .1 * noise1(t * 12, 4)
        st.paint('sky.frag', **PL.sky('ravana')); st.open(cam, PL.light('ravana', at=(0, 20, -30), keyCol=(.50, .20, .10), amb='#3a1a24', rimCol=(1.4, .45, .12)), far=2000.); PL.draw(st, 'ravana', lit=.6, polish=False); st.close(); PL.flames(st, 'ravana'); self.ravana(st, cam, f, t)
        S = st.fig(HM.HANUMAN, P, at=at, draw=False); ch = S.chest((0, 0, 0)); L = Light(key=(.3, .7, -.6), keyCol=(.55, .24, .12), amb=(.12, .05, .07), rim=(.1, .5, -1.), rimCol=(2.2, .85, .2), bounceCol=(.45, .15, .03), envT='#8a2c20', envM='#ff9a40', envB='#ffc060', pts=[(tuple(ch + V(-6, 5, -5)), 10., tuple(np.array([2.0, .80, .22]) * fk)), (tuple(ch + V(7, -2, 4)), 9., tuple(np.array([1.2, .48, .14]) * fk))], shadow=False, ink=3.4, inkCol='#050204')
        st.open(cam, L, far=2000.); S = st.fig(HM.HANUMAN, P, at=at, face=Face(mouth=.75, teeth=.8, frown=.9, spark=1.) if f < 70 else Face(mouth=.5, teeth=.8, frown=.6, spark=1.))
        Q = [V(0, 0, 0), V(-3, 2, -4), V(-9, 7, -6), V(-12, 14, -3), V(-6, 19, -1), V(3, 18, -3), V(10, 13, -4), V(13, 6, -2), V(9, 1, 1)]; pth, tl = on_floor(None, Q); w = math.sin(f * 1.3); P2 = HM.tail(st, S, 10., 'whip', length=tl * (.8 + .06 * w), wrap=1, path=pth(10.), ground=None)
        self.ropes(st, st.fig(HM.HANUMAN, BOUND, draw=False), max(.02, a), t); r = np.random.default_rng(3)
        for j in range(6): sd = -1 if j % 2 else 1; st.fig(RK.KINDS[j % 4].variant(u=dict(hold=0, shield=0)), RK.K_FALL, at=V(sd * (12 + 3 * j + 34 * a), 8 * a - 10 * a * a, -8 - 5 * j - 20 * a), yaw=-sd * 70, pitch=-30 * a * 3, face=Face(mouth=1., teeth=.8, frown=-.2))
        st.close(); HM.tail_fire(st, P2, t, .08, 1., 1.8, 1.35); c = V(0, 6.5, 0)
        FX.burst(st, 160, c, a, speed=42, grav=20, size=.12, seed=5, col='#ffb850', life=.5); FX.burst(st, 40, c, a, speed=30, grav=24, size=.16, seed=6, col='#b08a5a', kind='flake', life=.6)
        x, y, z = cam.project(c); IM.shock(st, (x, y), 120 + 2600 * a, 110, 46 * (1 - a * 3.2)) if a < .3 else None; IM.speedlines(st, (x, y), .30 * (1 - smooth(66, 71, f)), (1.0, .55, .18), seed=f, inner=.42); IM.zoomblur(st, (x, y), .012 + .07 * k)
        if f in (66, 67): IM.inkflash(st, dark='#12040a', mid='#d8321a' if f == 66 else '#ff9a2a', light='#fff0c8', lo=.22, hi=.50, amt=1. if f == 66 else .55)
        return st.finish(bloom=.5, thr=.9, vig=.45, contrast=1.08, flash=.0)

    def out(self, f, st, t):
        """from the throne's side: he crosses the hall like a comet and takes the window with him"""
        a = (f - 71) / 24.; u = clamp((f - 72) / 9.5); p = lambda q: V(6 * (1 - q) * math.cos(q * 5), 14 + 26 * q + 12 * math.sin(math.pi * q), -26 + 278 * q ** 1.15); hp = p(u); dirn = nz(p(min(1., u + .02)) - p(max(0., u - .02)))
        cam = Cam(V(-4 + 3 * u, 9 + 14 * u, -52 + 150 * u ** 1.2), lerp(V(0, 30, 120), V(0, 41, 254), smooth(72, 80, f)), lerp(54, 40, ease_io(clamp((f - 72) / 11.))), roll=lerp(-5, 0, u)); st.cam = cam; fk = 1 + .1 * noise1(t * 12, 4); gone = smooth(81, 83, f)
        pts = [(tuple(hp), 34., tuple(np.array([2.6, .95, .22]) * fk * (1 - .6 * gone))), (tuple(p(max(0, u - .22))), 30., (1.7, .55, .10)), (tuple(p(max(0, u - .45)) + V(0, 10, 0)), 30., (1.2, .38, .07)), (tuple(p(max(0, u - .7)) + V(0, 16, 0)), 30., (.9, .28, .05)), ((0, 80, hp[2] - 10), 40., (1.0, .40, .08))]
        st.paint('sky.frag', **PL.sky('ravana')); L = PL.light('ravana', keyCol=(.20, .08, .06), amb='#26101c', rimCol=(1.2, .35, .10), bounceCol=(.6, .2, .04)); L.pts = pts; st.open(cam, L, far=2000.); PL.draw(st, 'ravana', lit=.6, polish=False); st.world(WINDOW, u=dict(brk=float(2 + 34 * ease_out(clamp((f - 80) / 3.), 2)) if f >= 80 else 0., fire_=float(smooth(74, 81, f)), uAmb=hexc(L.amb), uKey=hexc(L.keyCol), sunSh=0.), head='place_head.glsl', main='place_main.glsl')
        for j in range(10):
            sd = -1 if j % 2 else 1; r = np.random.default_rng(j); z0 = -14 + 11 * j; ta = max(0., a - .035 * j * .7); v = V(sd * r.uniform(26, 44), r.uniform(18, 30), r.uniform(-8, 10)); q = V(sd * r.uniform(9, 13), 0, z0) + v * ta - V(0, 34, 0) * ta * ta; q[1] = max(q[1], 0)
            st.fig(RK.KINDS[j % 4].variant(u=dict(hold=0, shield=0)), RK.K_GUARD.mix(RK.K_FALL, clamp(ta * 9)), at=q, yaw=-sd * 90, pitch=-70 * clamp(ta * 3), roll=sd * 25 * ta, face=Face(mouth=1., teeth=.8, brow=.5))
        if f < 82:
            P = HM.H_FLY; yaw = math.degrees(math.atan2(dirn[0], dirn[2])); S = st.fig(HM.HANUMAN, P, at=hp - V(0, 12, 0), yaw=yaw, scale=1.9, face=Face(frown=.4))
            T0 = t; P2 = HM.tail(st, S, t, 'fly', length=30, wrap=1, ground=None, path=lambda tt: .22 * (p(clamp((tt * 24 - 72) / 9.5)) - hp) + V(math.sin((T0 - tt) * 16 - T0 * 14) * 14, math.cos((T0 - tt) * 13 - T0 * 14) * 9, 0) * clamp((T0 - tt) / .3))
        st.close(); PL.flames(st, 'ravana')
        Q = np.array([p(q) + V(0, 2 + 10 * (u - q), 0) + V(math.sin(q * 30) * 2.2, math.cos(q * 26) * 2, 0) for q in np.linspace(max(0, u - .75), max(.02, u - .10), 60)]); FX.ribbon(st, Q, np.interp(np.linspace(0, 1, 60), [0, .5, .9, 1], [.4, 4.5, 3.4, 1.0]), 'fire', amt=1.1, seed=3, blend='add')
        if f < 82: HM.tail_fire(st, P2, t, .10, 1., 1.0, 1.9)
        n = 70; r = np.random.default_rng(9); q = r.uniform(0, 1, n) * max(0, u - .12); age = np.clip((u - q) * 1.6, 0, 1); B = np.array([p(x) for x in q]) + np.c_[r.normal(0, 3, n), 6 + 46 * age, r.normal(0, 3, n)]; o = np.argsort(-((B - cam.eye) ** 2).sum(1)); FX.particles(st, B[o], (3.5 + 6 * r.uniform(0, 1, n) * np.sin(math.pi * np.clip(age + .12, 0, 1)))[o], (.95, .78, .58), 'tongue', seed=r.uniform(0, 1, n)[o], alpha=(1 - age)[o] ** .6 * .9)
        for w in (-1, 1): FX.embers(st, 60, ((min(w * 8, w * 50), 3, -30), (max(w * 8, w * 50), 40, 200)), t, rise=14, size=.35, seed=20 + w, life=1.6, swirl=3.)
        if f >= 80: FX.burst(st, 120, V(0, 44, 250), (f - 80) / 24., speed=90, grav=30, size=.9, seed=5, col='#ffc060', life=.6); FX.burst(st, 60, V(0, 44, 246), (f - 80) / 24., speed=80, grav=60, size=2.4, seed=6, col='#5a3018', kind='flake', life=.9); FX.particles(st, np.array([[0, 44, 249.]]), 46 * (1 - smooth(81, 84, f)), '#ffd890', 'glint', alpha=.9)
        x, y, z = cam.project(hp); IM.zoomblur(st, (x, y), .05 * (1 - smooth(72, 76, f)) + .01)
        return st.finish(bloom=.5, thr=.9, vig=.5, contrast=1.08)
