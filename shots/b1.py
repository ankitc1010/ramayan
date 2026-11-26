"""b1 (72): the coronation.  The crown comes down toward Rama (f0-35), stops (f36).  Colour drains; above, in the dark, Kaikeyi's eyes open; one finger (f42), two (f54): two boons.  The crown goes back up."""
from lau.shot import *
from lau.look import *
from chars import rama, people as PE
from chars.armonly import ARM, place_hand

BACK = '''
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform vec2 res,c;uniform float fT,beat;
void main(){vec2 p=vec2(uv.x*res.x,(1.-uv.y)*res.y);vec2 q=(p-c)/res.y;float r=length(q),a=atan(q.y,q.x);
 vec3 b=mix(hex(0xf2b23a),hex(0xa8281c),smoothstep(.10,.95,r));b=mix(b,hex(0x4a0a18),smoothstep(.7,1.25,r));
 float ray=smoothstep(-.12,.12,sin(a*24.));b=mix(b,b*1.28+hex(0x2a1004),ray*.55);
 for(int i=0;i<3;i++){float R=.43+.17*float(i);float n=26.+10.*float(i);float w=abs(fract(a*n/TAU)-.5);float e=r-R-.020*sqrt(max(0.,1.-w*w*4.))-.006*beat;b=mix(b,hex(0x5a0c14),smoothstep(.0035,.0,abs(e)-.002));b=mix(b,hex(0xffe09a),smoothstep(.0030,.0,abs(e+.012)-.0015));float bd=length(vec2(w*TAU/n*R,r-R-.048));b=mix(b,hex(0xfff0c0),smoothstep(.010,.006,bd));}
 b*=.90+.20*fbm(p/70.);
 // red and gold cloth swags at the top corners
 float sw=p.y-150.-130.*cos(p.x/res.x*TAU*1.)-22.*sin(p.x/58.);float k=smoothstep(3.,-3.,sw);vec3 cl=mix(hex(0x8a1420),hex(0xc83028),.5+.5*sin(p.x/34.+p.y/90.));cl=mix(cl,hex(0xf0b840),smoothstep(26.,22.,abs(sw+30.))*.9);b=mix(b,cl,k);b=mix(b,hex(0x2a0610),smoothstep(4.,0.,abs(sw))*.8);
 o=vec4(b,1);}
'''
DRAIN = '''
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform vec2 res;uniform sampler2D tF;uniform float k,dim,sh;
void main(){vec2 u=(uv-vec2(.5,.42))*(1.+.10*k)+vec2(.5,.42);u.y+=.085*k;vec3 c=texture(tF,u).rgb;float l=lum(min(c,vec3(1.2)));vec3 g=mix(c,mix(hex(0x0a0c1c),hex(0x7f86a8),l*.75),k);g*=mix(1.,dim,k);float m=mix(1.,smoothstep(.62,.30,uv.y)*smoothstep(.62,.30,abs(uv.x-.5)),k);o=vec4(g*m,0.);}
'''


class Shot(ShotBase):
    id = 'b1'; n = 72
    EVENTS = [(0, 'coronation drums', dict(dur=36)), (0, 'conch', dict(dur=30)), (12, 'crown metal', dict(soft=1)), (36, 'everything stops', {}), (39, 'eyes open', {}), (42, 'first boon', {}), (54, 'second boon', {}), (60, 'crown goes up', {})]

    def scene(self, f, st, t, crown_y):
        g = on2(f); u = f / 35.; cam = Cam(V(0, 13.6 + .2 * u, 17.5 - 2.2 * u), V(0, 14.15, 0), 34); st.cam = cam; x, y, z = cam.project(V(0, 14.6, -2)); beat = impulse((f % 6) / 24., 14)
        st.paint(BACK, c=(float(x), float(y)), beat=float(beat))
        L = Light(key=(.15, .85, .55), keyCol=(1.0, .86, .62), amb=(.34, .20, .24), rim=(0, .7, -.8), rimCol=(1.3, .85, .4), bounceCol=(.22, .10, .05), envT='#ffe0a0', envM='#ffb050', envB='#8a2a20', ink=3.4, pts=[(V(0, crown_y - .3, .6), 2.0, (.40, .26, .10))])
        st.open(cam, L); st.fig(rama.BAREHEAD, PZ.STAND.set(hedr=(0, 9, 0), lh=(.35, 10.6, 2.4), rh=(-.35, 10.6, 2.4), lhand='anjali', rhand='anjali', lfing=(0, 1, .3), rfing=(0, 1, .3), lpalm=(-1, 0, 0), rpalm=(1, 0, 0), lel=(1, -.6, -.2), rel=(-1, -.6, -.2)), face=Face(lid=.32, gy=-.3, smile=.22))
        c = V(0, crown_y, -.05); st.fig(PR.CROWN, M=PR.place(c, (0, 1, 0), (0, 0, 1), 1.04))
        P = PZ.STAND.set(rh=(-3.2, 8.6, 3.2), rel=(-1, -.6, 0), rhand='hold', rfing=(0, 0, 1), rpalm=(1, 0, 0), lh=(3.2, 8.6, 3.2), lel=(1, -.6, 0), lhand='hold', lfing=(0, 0, 1), lpalm=(-1, 0, 0))
        for sd, sg, col in (('R', -1, ('#d8a06a', '#86502f', 1)), ('L', 1, ('#c88a58', '#784426', 1))):
            A = ARM.variant(pal={1: col}, u=dict(side=1 if sd == 'R' else 0, band=1)); S = st.fig(A, P, draw=False)
            st.fig(A, P, M=place_hand(S, sd, c + V(1.12 * sg, .02, .12), (-.30 * sg, .62, .20), (-1 * sg, -.15, .12), 1.0), u=dict(side=1 if sd == 'R' else 0))
        st.close()
        # marigold petals jump on the drum
        r = np.random.default_rng(3); n = 90; p = r.uniform(0, 1, (n, 3)); k = r.uniform(.6, 1.3, n); P3 = np.c_[(p[:, 0] - .5) * 24 + .5 * np.sin(t * 1.7 * k + p[:, 1] * 30), 5 + np.mod(p[:, 1] * 17 - t * 2.1 * k + .25 * beat * k, 17), (p[:, 2] - .55) * 14]
        FX.particles(st, P3, .15 * k, np.where(p[:, :1] > .5, np.array(hexc('#ffb02a')), np.array(hexc('#f2643a'))), 'petal', rot=p[:, 0] * 6 + t * (k - .9) * 5, alpha=1.)

    def setup(self, st):
        st.clear('#000', f=35); self.scene(35, st, 35 / 24., 16.15); self.still = gl.ctx().texture((st.pw, st.ph), 4, dtype='f2'); fb = gl.ctx().framebuffer([self.still]); gl.ctx().copy_framebuffer(fb, st.C.fbo)
        self.tmp = gl.ctx().texture((st.pw, st.ph), 4, dtype='f2'); self.tmpf = gl.ctx().framebuffer([self.tmp])

    def frame(self, f, st):
        st.clear('#000', f=f); t = st.t
        cy = keys(f, [(0, 18.1), (24, 16.75, 'io'), (33, 16.25, 'out'), (35, 16.15)])
        if f < 36:
            self.scene(f, st, t, cy); return st.finish(bloom=.5, thr=.9, vig=.4, contrast=1.05, expo=1 + .16 * impulse((f % 6) / 24., 14), fade=1 - smooth(0, 4, f), fadeCol='#1a0608')
        k = smooth(36, 40, f); u = (f - 36) / 35.; g = on2(f); base = self.still
        if f >= 57:                                                                        # the crown is taken back up out of the frozen picture
            self.scene(35, st, 35 / 24., 16.15 + 7.5 * ease_in((f - 57) / 14., 1.7)); gl.ctx().copy_framebuffer(self.tmpf, st.C.fbo); base = self.tmp; st.clear('#000', f=f)
        # her eyes, huge, in the upper dark
        lid = keys(f, [(37, .0), (40, .95, 'out'), (46, .80), (56, .86), (60, .62, 'io'), (72, .50)]); P = PE.K_TWO.set(hedr=(0, 4, 0)); S = st.fig(PE.KAIKEYI_EYES, P, draw=False); h = S.head((0, .06, .6)); fw = S.d((0, 0, 1)); cam = Cam(h + fw * (6.0 - .35 * u) + V(0, -.02, 0), h + V(0, -.78, 0), 22); st.cam = cam
        fl = 1 + .10 * noise1(t * 8, 2); L = Light(key=(.35, -.25, .9), keyCol=(.30, .17, .11), amb=(.030, .016, .040), rim=(-.8, .3, -.4), rimCol=(.35, .12, .20), bounceCol=(0, 0, 0), envT='#ff9a50', envM='#b8401c', envB='#1a0818', pts=[(h + V(.9, -1.3, 2.0), 1.8, tuple(np.array([.34, .16, .07]) * fl))], shadow=False, ink=3.6)
        st.open(cam, L); st.fig(PE.KAIKEYI_EYES, P, face=Face(lid=lid, gy=-.75, gx=.0, frown=.30, spark=.95 * smooth(40, 46, f), squint=.2)); st.close()
        st.paint('''
in vec2 uv;out vec4 o;uniform float k;void main(){float y=uv.y;float band=smoothstep(.60,.765,y)*smoothstep(1.02,.86,y);float s=smoothstep(.56,.36,abs(uv.x-.5));float a=1.-band*s*k;o=vec4(vec3(.004,.003,.008)*a,a);}
''', 'over', k=float(smooth(37, 41, f)))
        st.paint(DRAIN, 'add', k=float(k), dim=float(.50 - .34 * smooth(58, 70, f)), sh=0., texs=dict(tF=base))
        # the hand
        if f >= 40:
            up = keys(g, [(40, -3.6), (42, -.35, 'out'), (44, -.5), (52, -.5), (54, -.10, 'out'), (56, -.30), (72, -.36)]); hand = 'point' if f < 53 else 'two'
            A = ARM.variant(pal={1: ('#cf9a68', '#7c4830', 1)}, u=dict(side=1, band=1, fore=1.)); Ph = PZ.STAND.set(rh=(-2.2, 11.5, 2.0), rel=(-.6, -1, -.3), rhand=hand, rpalm=(.1, -.6, 1)); cam2 = Cam(V(0, 0, 14), V(0, 0, 0), 30); st.cam = cam2
            hit = impulse((f - 42) / 24., 9) + impulse((f - 54) / 24., 9); L2 = Light(key=(.6, .5, .5), keyCol=tuple(np.array([.22, .13, .12]) * (1 + 1.6 * hit)), amb=(.035, .022, .05), rim=(-.7, .5, -.5), rimCol=tuple(np.array([.9, .42, .25]) * (1 + .8 * hit)), bounceCol=(0, 0, 0), envT='#ffb060', envM='#c8501c', envB='#1a0818', shadow=False, ink=3.4)
            st.open(cam2, L2); Sh = st.fig(A, Ph, draw=False); st.fig(A, Ph, M=place_hand(Sh, 'R', V(2.1, -2.0 + up, 0), (-.10, 1, .0), (-.14, 0, 1), 1.22)); st.close()
            for q in (42, 54):
                if 0 <= f - q < 8: FX.burst(st, 16, V(2.22, -.40 + up, .6) if q == 42 else V(2.36, -.42 + up, .6), (f - q) / 24., speed=3.2, grav=0, size=.035, seed=q, col='#ffc060', life=.35)
        return st.finish(bloom=.45, thr=.8, vig=.5, contrast=1.06, expo=1 + .45 * (f in (42, 54)) + .2 * (f in (43, 55)), flash=.55 if f == 36 else .18 if f == 37 else 0., flashCol='#fff0d0', fade=smooth(66, 72, f), fadeCol='#040308')
