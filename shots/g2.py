"""g2 (96): the flower chariot goes home over the night map of India.  Under its petals (f0-18); up behind it (f18-60); high over the dark land with the river of lamps it has woken, and the glow of Ayodhya on the edge of the world."""
from lau.shot import *
from lau.look import *
from chars import vehicles as VH, hanuman as HM
from worlds import flora as FLO
from .g_kit import *

ALT = 250.                                                      # how high the craft flies
TIP = 260.                                                      # z of the southern point of the land (north is -z)
AYO = V(500, 0, -42000)


def cz(f): return 1330 - 18 * f - .10 * f * f                     # where the craft is
def cx(z): return 150 * math.sin(z * .0036 + 1.0) * min(1., max(0., (900 - z) / 900)) + 40 * math.sin(z * .0011)
def when(z): return (-18 + np.sqrt(324 + .40 * np.maximum(1330 - z, 0))) / .20      # the frame it passes over z


MAP = '''
#include "orn.glsl"
float coastW(float z){return z>260.?-(z-260.):sqrt((260.-z)*26.)*2.2+(260.-z)*.20;}
float landD(vec2 p){float w=coastW(p.y);float d=w-abs(p.x-90.*sin(p.y*.0009));d+=130.*(fbm(p*.0042)-.5)+46.*(fbm(p*.016)-.5);vec2 q=(p-vec2(330.,1290.))/vec2(300.,470.);float l=(1.-length(q))*300.+60.*(fbm(p*.008+4.)-.5);return max(d,l);}   // > 0 on land
float riverD(vec2 p,out float w){float d=1e5;w=10.;for(int i=0;i<8;i++){float k=float(i);float z0=-150.-430.*k-90.*h11(k);float s=sin(p.x*.0034+k*2.1),z=z0+110.*s+46.*sin(p.x*.0098+k*4.)+.12*p.x*(h11(k+3.)-.5)*2.;float sl=cos(p.x*.0034+k*2.1)*110.*.0034+cos(p.x*.0098+k*4.)*46.*.0098;float e=abs(p.y-z)/sqrt(1.+sl*sl);if(e<d){d=e;w=3.2+2.2*h11(k+9.)+.002*abs(p.x);}
  float x2=-260.+520.*h11(k+5.);float zz=p.y-z0;if(zz<0.&&zz>-330.){float x=x2+(90.*sin(zz*.011+k)+.4*zz*(h11(k+7.)-.5));float t=abs(p.x-x)*.93;if(t<d){d=t;w=1.8+.002*(330.+zz);}}}return d;}
'''
GROUND = '''
#include "noise.glsl"
''' + MAP + '''
in vec2 uv;out vec4 o;uniform vec2 res,moon;uniform vec3 ro,ayo;uniform mat3 CamR;uniform float fl,fT,haze,bx0,bx1;
uniform sampler2D tL;uniform vec4 lbox;
void main(){vec2 s=(uv*2.-1.)*vec2(res.x/res.y,1.);vec3 d=normalize(transpose(CamR)*vec3(s,fl));
 if(d.y>-.0015){discard;}
 float t=-ro.y/d.y;vec3 P=ro+d*t;vec2 p=P.xz;float px=t*2./(fl*1080.)/max(-d.y,.05);
 float L=landD(p),aa=max(px,.6);float land=smoothstep(-aa,aa,L);
 // sea: scalloped waves in rows
 vec3 sea=mix(hex(0x062830),hex(0x0b4650),fbm(p*.003+3.)*.9+.25*smoothstep(-260.,0.,L));oAA=px/34.;float wv=oWater(p/vec2(34.,17.)+vec2(fT*.25,0.))*smoothstep(8.,2.,px);sea+=hex(0x2c8a88)*wv*.22*(.4+.6*fbm(p*.006+9.));
 float rip=0.;for(int i=0;i<3;i++){float r=-9.-11.*float(i);rip+=smoothstep(1.2+px,0.,abs(L-r-2.*sin(p.x*.05+p.y*.04)))*(.5-.13*float(i));}sea=mix(sea,hex(0x6fb4ac),rip*.6);
 // land: deep indigo green, fields, dry brush
 float n=fbm(p*.0045),m=fbm(p*.021+5.);vec3 g=mix(hex(0x0b1a38),hex(0x16383e),smoothstep(.3,.7,n));g=mix(g,hex(0x2b3350),smoothstep(.55,.75,m)*.5);
 vec2 f=rot(.5*floor(n*6.))*p/46.;vec2 fi=floor(f),ff=fract(f);float fd=step(.62,h21(fi))*smoothstep(.52,.46,max(abs(ff.x-.5),abs(ff.y-.5)));float rows=.5+.5*sin(f.y*38.*step(.5,h21(fi+3.))+f.x*38.*step(h21(fi+3.),.5));g=mix(g,mix(hex(0x1f4a44),hex(0x3a4a5c),h21(fi+7.)),fd*(.30+.35*rows*smoothstep(1.2,.3,px))*smoothstep(10.,2.,px));
 float w;float rd=riverD(p,w);float rv=smoothstep(w+aa,w-aa,rd);vec3 sil=mix(hex(0x3f6488),hex(0xa8c8e0),smoothstep(.35,.7,fbm(vec2(p.x*.02,p.y*.05)+fT*.3)));g=mix(g,hex(0x050b1c),smoothstep(w+4.+aa,w+1.,rd)*.7);g=mix(g,sil*.72,rv);
 float cst=smoothstep(3.5+aa,1.,abs(L-1.));g=mix(g,hex(0xd8c08a)*.5,smoothstep(16.,2.,L)*.55);
 vec3 c=mix(sea,g,land);c=mix(c,hex(0xe8d8a8)*.55,cst*.8);
 // the bridge of stones
 {float u=clamp((p.y-210.)/(930.-210.),0.,1.);float bx=mix(bx0,bx1,u)+16.*sin(u*9.);float a=(p.y-210.)/17.;float k=floor(a);vec2 q=vec2(p.x-bx-3.*(h11(k)-.5),(fract(a)-.5)*17.);float st=smoothstep(6.5+aa,6.5-aa,length(q*vec2(1.,.95)))*step(215.,p.y)*step(p.y,930.);c=mix(c,hex(0x061a22),smoothstep(11.,6.,length(q))*step(215.,p.y)*step(p.y,930.)*.6);c=mix(c,mix(hex(0x9a8a78),hex(0xe8d8b8),h11(k+4.))*.75,st);}
 // warm light of the lamps that are awake
 vec2 lq=(p-lbox.xy)/(lbox.zw-lbox.xy);if(min(lq.x,lq.y)>0.&&max(lq.x,lq.y)<1.){float g2=textureLod(tL,lq,0.).r;c+=(c*2.2+hex(0x3a1405)*.35)*vec3(1.6,.66,.20)*g2;}
 vec2 mg=P.xz-ro.xz;float moonp=exp(-pow(dot(normalize(mg),normalize(vec2(moon.x,moon.y)))-1.,2.)*60.);c+=hex(0x6f8ac8)*moonp*(.05+.10*(1.-land))*exp(-t*.0003);
 float fg=1.-exp(-max(0.,t-500.)*haze);vec3 hz=mix(hex(0x0c1440),hex(0x3a3566),smoothstep(.12,.0,-d.y));vec3 ad=normalize(ayo-ro);float gl=exp(-pow(length((d.xz/length(d.xz)-ad.xz/length(ad.xz)))*9.,2.));hz+=hex(0xe0742a)*gl*smoothstep(.10,.0,-d.y)*.30;c=mix(c,hz,fg);
 o=vec4(c,1);}
'''
SKYG = '''
#include "sky.glsl"
in vec2 uv;out vec4 o;uniform vec2 res;uniform vec3 ro,ayo;uniform mat3 CamR;uniform float fl,fT,amt;
void main(){vec2 s=(uv*2.-1.)*vec2(res.x/res.y,1.);vec3 d=normalize(transpose(CamR)*vec3(s,fl));vec3 a=normalize(ayo-ro);vec2 q=skyUV(d)-vec2(skyUV(a).x,0.);q.y=max(q.y,0.);
 float g=exp(-q.x*q.x*26.-q.y*15.)*.42+exp(-q.x*q.x*190.-q.y*60.)*1.1;float ray=1.;vec3 c=mix(hex(0xd85a1c),hex(0xffc070),exp(-q.y*30.))*g*ray;o=vec4(c*amt*step(0.,d.y+.002),0.);}
'''
def cloud(c, seed):
    """a thin mural cloud, 1500 x 360: scallops over a drifting foot, with the painter's contour lines"""
    r = np.random.default_rng(seed); n = 15; x = np.linspace(150, 1350, n); env = np.sin(np.linspace(.12, 3.0, n)) ** .7; rad = (40 + 78 * env) * r.uniform(.72, 1.12, n); y = 215 - rad * .30 - 26 * env * r.uniform(0, 1, n); C = list(zip(x, y, rad)) + [(q + 34, 226, 30 + 20 * e) for q, e in zip(x[:-1], env)]
    c.push_group()
    for k, (a, col) in enumerate(((7, '#0a1140'), (0, '#8f9fe0'), (-9, '#5a6ab4'), (-13, '#7f90d4'), (-34, '#54649e'), (-38, '#7384c8'))):
        for X, Y, R in C:
            if R + a > 4: c.new_path(); c.save(); c.translate(X, Y); c.scale(1, .86); c.arc(0, 0, R + a, 0, 7); c.restore(); c.set_source_rgb(*rgb(col)); c.fill()
    g = cairo.LinearGradient(0, 70, 0, 300); g.add_color_stop_rgba(0, 1, 1, 1, .28); g.add_color_stop_rgba(.5, .6, .7, 1, .05); g.add_color_stop_rgba(1, .05, .08, .3, .55); c.set_operator(cairo.OPERATOR_ATOP); c.set_source(g); c.paint(); c.set_operator(cairo.OPERATOR_OVER); c.pop_group_to_source()
    m = cairo.LinearGradient(0, 205, 0, 272); m.add_color_stop_rgba(0, 0, 0, 0, 1); m.add_color_stop_rgba(1, 0, 0, 0, 0); c.mask(m)


def hillock(c, seed):
    """a hill of the miniature painters, 640 x 380: humps of wash edged with light, a few round trees"""
    r = np.random.default_rng(seed)
    for k in range(5):
        cx_, w, h = 110 + 105 * k + r.uniform(-30, 30), r.uniform(120, 170), r.uniform(150, 300) * (1 - .12 * abs(k - 2)); y0 = 372; x = np.linspace(-1, 1, 40); P = np.c_[cx_ + x * w, y0 - h * np.maximum(np.cos(x * 1.571), 0) ** .8 * (1 + .05 * np.sin(x * 17 + k))]
        g = cairo.LinearGradient(0, y0 - h, 0, y0); a, b = [('#4a5a9a', '#14224a'), ('#3f6a86', '#10283e'), ('#5a528c', '#181c44')][(k + seed) % 3]; g.add_color_stop_rgb(0, *rgb(a)); g.add_color_stop_rgb(1, *rgb(b)); poly(c, P); c.set_source(g); c.fill_preserve(); c.set_source_rgb(*rgb('#080c26')); c.set_line_width(6); c.stroke()
        Q = P * [1, 1] + [0, 9]; c.move_to(*Q[4]); [c.line_to(*q) for q in Q[5:26]]; c.set_source_rgba(*rgb('#b4c4ec'), .55); c.set_line_width(5); c.stroke()
        for _ in range(5):
            j = r.integers(6, 34); X, Y = P[j]; Y += r.uniform(14, h * .5); R = r.uniform(11, 19); c.arc(X, Y, R, 0, 7); c.set_source_rgb(*rgb('#12304a')); c.fill_preserve(); c.set_source_rgb(*rgb('#060a20')); c.set_line_width(4); c.stroke(); c.arc(X - R * .3, Y - R * .3, R * .4, 0, 7); c.set_source_rgb(*rgb('#3a7088')); c.fill()


def temple(c, w=256, h=420):
    """a little white temple, as miniature painters put them on hills"""
    c.scale(w / 256, h / 420); INK = '#0a0c24'
    def P(q, col, lw=5): poly(c, q); c.set_source_rgb(*rgb(col)); c.fill_preserve(); c.set_source_rgb(*rgb(INK)); c.set_line_width(lw); c.set_line_join(1); c.stroke()
    P([(20, 410), (20, 372), (236, 372), (236, 410)], '#8a90b8'); P([(40, 372), (40, 270), (216, 270), (216, 372)], '#d8dcf0'); P([(30, 270), (30, 252), (226, 252), (226, 270)], '#a8aed0')
    L = [(128 - x, y) for x, y in ((84, 252), (80, 190), (64, 120), (40, 66), (20, 44))]; P(L + [(256 - x, y) for x, y in L[::-1]], '#eef0fa')
    for y in (222, 192, 162, 132, 104, 80): k = np.interp(y, [44, 66, 120, 190, 252], [20, 40, 64, 80, 84]); c.move_to(128 - k, y); c.line_to(128 + k, y); c.set_source_rgba(*rgb('#6a74a8'), .8); c.set_line_width(4); c.stroke()
    P([(112, 44), (112, 34), (144, 34), (144, 44)], '#e8b04a', 4); c.arc(128, 24, 12, 0, 7); c.set_source_rgb(*rgb('#f0c860')); c.fill(); c.move_to(128, 12); c.line_to(128, 2); c.set_source_rgb(*rgb(INK)); c.set_line_width(4); c.stroke()
    c.move_to(108, 372); c.line_to(108, 320); c.arc(128, 320, 20, math.pi, 0); c.line_to(148, 372); c.close_path(); c.set_source_rgb(*rgb('#ffb04a')); c.fill_preserve(); c.set_source_rgb(*rgb(INK)); c.set_line_width(4); c.stroke()


def hash_land(x, z):
    """rough test that a place is on the mainland, away from the coast"""
    w = np.where(z > 260, -1e3, np.sqrt(np.maximum(260 - z, 0) * 26) * 2.2 + (260 - z) * .20); return w - np.abs(x - 90 * np.sin(z * .0009)) - 110


class Shot(ShotBase):
    id = 'g2'; n = 96
    EVENTS = [(0, 'flower chariot overhead', dict(dur=30)), (4, 'bells on the chariot', dict(dur=60)), (18, 'wind', dict(dur=78)), (30, 'villages wake', dict(dur=66)), (48, 'temple bell far', dict(soft=1)), (72, 'temple bell far', dict(soft=1)), (88, 'city glow', {})]

    def setup(self, st):
        r = np.random.default_rng(21); V_, Lz = [], []
        # villages: close beside the path, then farther and later
        z = 180.
        while z > -2300:
            for _ in range(3): V_.append((cx(z) + r.normal(0, 85), z + r.uniform(-60, 60), r.uniform(26, 62), 0.))
            if r.uniform() < .8: V_.append((cx(z) + r.choice([-1, 1]) * r.uniform(180, 480), z + r.uniform(-60, 60), r.uniform(20, 46), r.uniform(8, 22)))
            z -= 62
        V_ = np.array(V_); V_ = V_[hash_land(V_[:, 0], V_[:, 1]) > 0]; self.vil = V_; P, w, big = [], [], []
        for x, z, rad, late in V_:
            n = int(8 + rad * .62); a = r.uniform(0, 6.28, n); q = rad * np.sqrt(r.uniform(0, 1, n)); P.append(np.c_[x + q * np.cos(a), np.full(n, 3.), z + q * np.sin(a) * .8]); w.append(when(z) - 3 + late + 6 * q / rad + r.uniform(0, 4, n) + abs(x - cx(z)) * .02); big.append(r.uniform(.6, 1.5, n))
        # a thread of lamps under the path itself: the boats and the road
        zz = np.arange(170, -2300, -6.); P.append(np.c_[[cx(q) for q in zz] + r.normal(0, 10, len(zz)), np.full(len(zz), 3.), zz]); w.append(when(zz) - 4 + r.uniform(0, 4, len(zz))); big.append(r.uniform(.5, 1.1, len(zz)))
        self.P, self.w, self.big = np.vstack(P), np.concatenate(w), np.concatenate(big); self.vw = when(V_[:, 1]) + V_[:, 3] + np.abs(V_[:, 0] - np.array([cx(q) for q in V_[:, 1]])) * .02
        # trees, hills, temples
        n = 9000; x = r.uniform(-1300, 1300, n); z = r.uniform(-4300, 240, n); cl = np.sin(x * .017 + 1) * np.sin(z * .014) + .7 * np.sin(x * .037 - z * .029); m = (hash_land(x, z) > -60) & (cl > .30); self.trees = np.c_[x, 0 * x, z][m]
        n = 150; x = r.uniform(-1000, 1000, n); z = r.uniform(-4200, 100, n); m = (hash_land(x, z) > 20) & (np.abs(x - np.array([cx(q) for q in z])) > 150) & (np.sin(x * .004 + z * .003) > -.1); self.hills = np.c_[x, 0 * x - 2, z][m]
        n = 64; x = np.r_[r.uniform(-700, 700, n)]; z = r.uniform(-3800, 150, n); m = hash_land(x, z) > 0; self.temples = np.c_[x, 0 * x, z][m]
        mk = lambda q, w, h, top: FLO.Plate(q, w, h, .5, .97, top)
        self.tpl = mk(plate('g2_temple', 256, 420, temple, ver=1), 256, 420, .01); self.hp = [mk(plate('g2_hill%d' % k, 640, 380, lambda c, k=k: hillock(c, k), ver=2), 640, 380, .2) for k in range(3)]
        self.cp = [plate('g2_cloud%d' % k, 1500, 360, lambda c, k=k: cloud(c, k + 4), ver=5) for k in range(3)]
        # clouds: (x, y, z, length)
        g = np.random.default_rng(14); self.low = [(g.uniform(-1100, 1100), 130 + g.uniform(-20, 30), z_, g.uniform(260, 460), int(g.integers(0, 3))) for z_ in np.linspace(900, -3200, 19)]; self.high = [(g.choice([-1, 1]) * g.uniform(160, 900), 470 + g.uniform(-60, 80), z_, g.uniform(330, 560), int(g.integers(0, 3))) for z_ in np.linspace(900, -2400, 14)]

    def clouds(self, st, C, L, alpha, part=0):
        """part -1: only what is beyond the craft, +1: only what is between it and us"""
        cam = st.cam; zC = float((C - cam.eye) @ cam.R[2]); D = sorted(((float((V(*c[:3]) - cam.eye) @ cam.R[2]), c) for c in L), key=lambda q: -q[0])
        for z, (x, y, zz, ln, k) in D:
            if z < 40 or z > 5200 or (z - zC) * part > 0: continue
            X, Y, _ = cam.project(V(x + 9 * st.t, y, zz)); w = ln * cam.fl * H / 2 / z
            if X < -w or X > W + w or Y < -w * .3 or Y > H + w * .3: continue
            warm = math.exp(-np.sum((V(x, y, zz) - C) ** 2) / (2 * 260. ** 2)); st.plate(self.cp[k], X, Y, sx=w / 1500., sy=w / 1500. * (.75 + .5 * abs(cam.R[2][1])), alpha=float(alpha * smooth(40, 420, z) * math.exp(-z * .00030)), tint=(.62 + .5 * warm, .62 + .16 * warm, .74 - .1 * warm), flip=bool(k % 2), lod=0.)

    def lightmap(self, f):
        """where the ground is lit by woken villages: a small texture over the land"""
        x0, x1, z0, z1 = -1000., 1000., -2400., 400.; w, h = 300, 420; a = np.zeros((h, w), 'f4'); k = np.clip((f - self.vw) / 8., 0, 1)
        X = np.linspace(x0, x1, w); Z = np.linspace(z0, z1, h)
        for (x, z, rad, _), q in zip(self.vil, k):
            if q <= 0: continue
            i0, i1 = np.searchsorted(X, [x - 3 * rad, x + 3 * rad]); j0, j1 = np.searchsorted(Z, [z - 3 * rad, z + 3 * rad])
            a[j0:j1, i0:i1] += q * np.exp(-((X[i0:i1][None] - x) ** 2 + (Z[j0:j1][:, None] - z) ** 2) / (2 * (.8 * rad) ** 2))
        t = gl.ctx().texture((w, h), 1, np.ascontiguousarray(np.minimum(a, 1.4)).tobytes(), dtype='f4'); t.filter = (gl.mgl.LINEAR, gl.mgl.LINEAR); t.repeat_x = t.repeat_y = False
        return t, (x0, z0, x1, z1)

    def craft(self, f):
        z = cz(f); x = cx(z); dx = (cx(z - 5) - cx(z + 5)); yaw = math.degrees(math.atan2(dx, -10)); t = f / 24.
        return V(x, lerp(ALT, 120., smooth(30, 80, f)) + 5 * math.sin(t * 1.7), z), yaw, 4 * math.sin(t * 1.2) + dx * 1.5

    def cam(self, f, C):
        # relative to the craft: from under its petals, round its stern, up and far behind
        rel = glide(f, [(0, (8, -50, -50)), (17, (18, -50, 60)), (27, (38, -4, 150)), (42, (58, 100, 340)), (64, (20, 310, 780)), (95, (-40, 600, 1420))])
        at = glide(f, [(0, (-2, 60, 34)), (16, (2, 60, 10)), (27, (2, 18, -60)), (42, (2, -30, -160)), (64, (4, -110, -260)), (95, (20, -60, -230))])
        d = at - rel; p = math.atan2(d[1], -d[2])                                      # up is kept in the plane of flight, so passing overhead never spins the picture
        return Cam(C + rel, C + at, glide(f, [(0, 74.), (18, 66.), (42, 54.), (64, 51.), (95, 55.)]), roll=glide(f, [(0, -10.), (30, 4.), (62, 0.), (95, 0.)]), up=(0, math.cos(p), math.sin(p)))

    def frame(self, f, st):
        st.clear('#05071e', f=f); t = st.t; C, yaw, roll = self.craft(f); cam = self.cam(f, C); st.cam = cam; far = 12000.
        moon = nz(V(-.42, .30, -1.))
        st.paint('sky.frag', **SKY(NIGHT, cZen='#04061c', cMid='#0f1742', cHor='#3a3566', cLow='#1a1c48', sunR=0., sunGlow=0., halo=0., cov=.46, cy0=.0, cy1=.10, cscale=3.2, cLit='#6f7fc0', cCM='#39468a', cSh='#1c2560', cInk='#05081c', starAmt=1.))
        st.paint('moon.frag', 'over', dir=tuple(moon), R=.115, amt=1., glow=.8, cA=hexc('#fbf3dc'), cB=hexc('#a9b4cc'), cG=hexc('#6f8ad8'))
        st.paint(SKYG, 'over', ayo=tuple(AYO), amt=float(.25 + .75 * smooth(40, 90, f)))
        tl, box = self.lightmap(f); st.paint(GROUND, 'over', moon=(float(moon[0]), float(moon[2])), ayo=tuple(AYO), haze=.00042, bx0=float(cx(210.)), bx1=float(300.), texs=dict(tL=tl), lbox=box)
        L = Light(key=tuple(moon), keyCol='#8090d0', amb='#333c7c', rim=tuple(moon), rimCol=(.4, .5, .9), bounceCol=(.22, .10, .03), envT='#8fa4ff', envM='#ffb45a', envB='#c86a2a', fogCol='#1a1f52', fog=(.00040, 700., 0, 0), ink=3., inkRef=6., inkCol='#05040f', shadow=False)
        st.open(cam, L, far=far)
        FLO.scatter(st, 'pahari_round', self.trees, 23, season='night', seed=2, vary=.3, tint=(1.15, 1.2, 1.2), wind=.2)
        [FLO.cards(st, hp, self.hills[k::3], 58., wind=0., tint=(.9, .9, 1.), flip=np.resize([1., -1.], len(self.hills[k::3]))) for k, hp in enumerate(self.hp)]; FLO.cards(st, self.tpl, self.temples, 30., wind=0., tint=(1.15, 1.1, 1.15))
        st.close()
        self.clouds(st, C, self.low, .62); self.clouds(st, C, self.high, .55, -1)
        # lamps of the land
        k = np.clip((f - self.w) / 3., 0, 1); pop = 1 + .9 * np.exp(-np.maximum(f - self.w, 0) / 4.) * (f > self.w); m = k > 0
        if m.any(): glows(st, self.P[m], 2.6, 2.4 * self.big[m] * pop[m], k[m], col='#ff9a3a', gain=1.9, seed=3, tw=.2)
        m = f > self.vw
        if m.any(): FX.particles(st, np.c_[self.vil[m, 0], np.full(m.sum(), 6.), self.vil[m, 1]], self.vil[m, 2] * 2.4, '#ff7a20', 'ember', alpha=.075 * np.clip((f - self.vw[m]) / 10., 0, 1))
        # Ayodhya, far off: a seam of light on the rim of the world
        g = np.random.default_rng(8); n = 420; A = AYO + np.c_[g.normal(0, 2600, n), 60 + 900 * g.uniform(0, 1, n) ** 2 * np.exp(-np.linspace(-1, 1, n) ** 2), g.normal(0, 120, n)]; glows(st, A, 6., 1.5 * g.uniform(.6, 1.4, n), smooth(30, 80, f) * g.uniform(.4, 1, n), gain=1.8, tw=.3)
        # the chariot and those who ride it
        st.open(cam, Light(key=tuple(moon), keyCol='#8f9ce0', amb='#3f4688', rim=tuple(moon), rimCol=(.5, .6, 1.1), bounceCol=(.30, .13, .04), envT='#8fa4ff', envM='#ffb45a', envB='#d8742a', pts=[(C + V(0, 40, 0), 60., (.6, .32, .12)), (C + V(0, 24, 56), 20., (2.2, 1.2, .5))], ink=3.2, inkRef=6., inkCol='#05040f', shadow=False), far=far)
        K = VH.pushpaka(st, at=tuple(C), yaw=yaw, pitch=2 * math.sin(t * 1.3), roll=roll, scale=float(lerp(6., 11., smooth(40, 95, f))), lamps=1.1, glow=float(lerp(.42, .85, smooth(14, 40, f))), t=t)
        kk = K.Sc / 6.
        if f > 20:
            for fig, x, z, p, ya in ((RAMA, 4., 4., PZ.STAND, 60), (SITA_JEWEL, -4.5, 4., sita.S_STAND, -50), (rama.LAKSHMANA, 12., 4., PZ.STAND, 90), (HM.HANUMAN, -13., 4., HM.H_ANJALI, -100)): st.fig(fig, p, M=K.aft @ model((x * kk, 0, z * kk), ya, scale=kk * 1.25), face=Face(smile=.4), shadow=False)
        st.close()
        q = K.lamps(22); glows(st, q, 2.4, 2.0, 1., gain=1.6, tw=.2); FX.particles(st, (C + V(0, 10, 0))[None], 90., '#ff8a34', 'ember', alpha=.14 * smooth(40, 60, f))
        FX.drift(st, 60, (tuple(C + V(-160, -160, -40)), tuple(C + V(160, 30, 420))), t, size=2.6, col='#f2a0b0', col2='#ffd080', fall=26., sway=10., seed=3, wind=(0, 0, 60))
        self.clouds(st, C, self.high, .55, 1)
        tl.release()
        return st.finish(bloom=.55, thr=.85, vig=.42, contrast=1.06, satu=1.08, fade=0.)
