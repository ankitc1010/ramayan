"""a2 (108): the shadow theatre, seen from the seats.  Sacred fire (f0); four small princes (f36, 42, 48, 54); the eldest shoots a toy arrow across the cloth (draw f72, release f90)."""
from lau.shot import *
from . import puppets as PU

CLOTH = '''
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform vec2 res,hot;uniform float fT,flick,zoom;uniform sampler2D tA,tB;uniform float blurA,blurB;uniform vec2 ctr;
uniform float lk;
vec4 pup(sampler2D t,vec2 q,float l){vec4 c=textureLod(t,q,l+lk*min(l,1.));c.rgb=pow(c.rgb/max(c.a,1e-3),vec3(2.2));return c;}
void main(){vec2 p=vec2(uv.x*res.x,(1.-uv.y)*res.y);p=(p-ctr)/zoom+ctr;vec2 q=vec2(p.x/res.x,1.-p.y/res.y);
 float fold=.5+.5*sin(p.x*.0115+.6*sin(p.y*.004)+.4*sin(fT*.9));float f2=sin(p.x*.031+1.3+.3*sin(fT*1.3+p.y*.006));vec2 dq=vec2(.0016*cos(p.x*.0115)+.0007*f2,.0);
 float r=length((p-hot)/vec2(1.,.92));float lite=exp(-r*r/(2.*210.*210.))*.62+exp(-r/560.)*.86+.05;lite*=flick;
 vec3 c=mix(hex(0xa8480e),hex(0xffb24e),smoothstep(.15,1.1,lite))*lite;c=mix(c,hex(0xffe2a0)*1.12,smoothstep(1.02,1.75,lite));
 float wv=sin(p.x*1.55)*sin(p.y*1.55);c*=.94+.06*wv;c*=.90+.12*fold+.04*f2;c*=.93+.14*fbm(p/190.)+.05*(vn(p/3.)-.5);
 vec4 b=pup(tB,q+dq,blurB),a=pup(tA,q+dq,blurA);
 c*=mix(vec3(1.),b.rgb,b.a*.93);c*=mix(vec3(1.),a.rgb,a.a*.97);
 float ed=smoothstep(.010,.0,abs(a.a-.5))*0.;
 // hem and frame
 vec2 e=vec2(abs(p.x-960.)-880.,abs(p.y-500.)-470.);float fr=max(e.x,e.y);c*=1.-.55*smoothstep(-160.,0.,fr);
 float band=smoothstep(0.,3.,e.y)*step(p.y,500.);
 vec3 bd=hex(0x5a0f10)*.35;float bx=fract(p.x/90.)-.5;float tri=step(abs(bx)*1.4,(p.y-2.)/60.);bd=mix(bd,hex(0xd88a24)*.30,tri*step(p.y,26.));bd=mix(bd,hex(0xe8a030)*.22,smoothstep(7.,5.,length(vec2(bx*90.,p.y-14.))));
 c=mix(c,bd*(.35+lite*.6),band);float side=smoothstep(0.,4.,e.x);c=mix(c,hex(0x1a0a08)*.25,side);
 o=vec4(c,1);}
'''


class Shot(ShotBase):
    id = 'a2'; n = 108
    EVENTS = [(0, 'theatre begins', {}), (18, 'ghee on the fire', {}), (36, 'prince 1', {}), (42, 'prince 2', {}), (48, 'prince 3', {}), (54, 'prince 4', {}), (72, 'toy bow drawn', {}), (90, 'toy arrow', {}), (97, 'arrow passes lamp', {})]
    HOT = (1010., 430.)

    def setup(self, st):
        r = np.random.default_rng(5); self.heads = [(x, 1040 + 26 * math.sin(i * 2.3), 62 + 14 * r.uniform(-1, 1), r.integers(0, 4)) for i, x in enumerate(np.linspace(30, 1890, 13) + r.uniform(-30, 30, 13))]

    def layer(self, fn, k):
        sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W * k, H * k); c = cairo.Context(sf); c.scale(k, k); fn(c); sf.flush(); t = gl.tex_from(np.ndarray((H * k, W * k, 4), np.uint8, sf.get_data()).copy()); t.swizzle = 'BGRA'
        return t

    def frame(self, f, st):
        st.clear('#000000', f=f); t = st.t; g = on2(f); tg = g / 24.; GY = 905
        # ---- what hangs where
        out1 = ease_in((g - 62) / 14., 2.2)                                   # the court leaves to both sides
        in1 = back_out(clamp((g + 4) / 12.), 1.2)
        kx = lerp(-260, 470, in1) - 900 * out1; sx = lerp(2180, 1490, in1) + 900 * out1
        joy = impulse((g - 36) / 24., 5) + impulse((g - 48) / 24., 5)
        ladle = keys(g, [(6, 62.), (14, 40.), (18, 96.), (24, 70.), (36, 60.)])
        drops = [36, 42, 48, 54]; skins = ['blue', 'ochre', 'rose', 'ochre']; cl = ['yellow', 'red', 'green', 'violet']; sashs = ['red', 'green', 'red', 'yellow']
        gone = [0 if i == 0 else ease_in((g - 66 - 2 * i) / 10., 2) for i in range(4)]
        big = ease_io((g - 64) / 14., 2.4)

        def back(c):
            # sacred fire and altar sink away
            sink = 560 * ease_in((g - 31) / 8., 2)
            PU.altar(c, 985, GY + sink, 200); PU.fire(c, 985, GY - 42 + sink, 250 * (1 + .30 * impulse((g - 18) / 24., 6) + .75 * ease_in((g - 24) / 10., 2) + .06 * math.sin(tg * 11)), tg)

        def front(c):
            if kx > -330: PU.figure(c, kx, GY + 6, 640, 'ochre', 'red', 'green', 'king', True, near=(52 + 22 * joy + 3 * math.sin(tg * 5), 58 + 26 * joy, 'open'), far=(30 + 30 * joy, 66, 'open'), bob=-.020 * abs(math.sin(tg * 6.28)) * (g < 62) - .03 * joy, lean=2 * math.sin(tg * 3))

            def spoon(c, w):
                if w == 'front':
                    c.set_source_rgb(*PU.BK); c.set_line_width(.016); c.move_to(.20, -.52); c.line_to(.42, -.60 + .0016 * (96 - ladle)); c.stroke(); c.arc(.43, -.60 + .0016 * (96 - ladle), .020, 0, 7); c.fill()
            if sx < 2200: PU.figure(c, sx, GY + 6, 600, 'brown', 'yellow', 'red', 'rishi', True, flip=True, near=(ladle, 22, 'fist'), far=(34, 50, 'open'), bob=-.015 * abs(math.sin(tg * 6.28 + 1)), extra=spoon)
            for i in (3, 2, 1, 0):
                if g < drops[i] - 2: continue
                u = clamp((g - drops[i] + 2) / 8.); up = back_out(u, 2.6); x0 = 690 + 185 * i; s = 350.
                if i == 0: x = lerp(x0, 560, big); s = lerp(330, 780, big); y = GY + (1 - up) * 420
                else: x = x0 + 700 * gone[i] * (1 if i > 1 else -1.6); y = GY + (1 - up) * 420 + 260 * gone[i]
                wob = 5 * math.sin((g - drops[i]) * .7) * math.exp(-.12 * max(0, g - drops[i]))
                if i == 0 and g >= 64:
                    d = keys(g, [(70, 0.), (84, 1., 'io'), (89, 1.06), (90, 0., 'snap'), (94, -.06), (98, 0.)])
                    near = (86, 4, 'fist'); far = (lerp(60, -62, max(0, d)), lerp(40, 128, max(0, d)), 'fist')
                    PU.figure(c, x, y, s, skins[0], cl[0], sashs[0], 'prince', near=near, far=far, lean=-2.5 * max(d, 0) + 2 * impulse((g - 90) / 24., 7) + wob, smile=.8,
                              extra=lambda c, w, d=d: (PU.bow(c, .045 + .315, -.665, .17, .035 + .13 * max(0, d)), self.toy(c, .045 + .315 - .06 - .035 - .13 * max(0, d), -.665) if g < 90 else None) if w == 'back' else None)
                else: PU.figure(c, x, y, s, skins[i], cl[i], sashs[i], 'prince', near=(24 + 50 * impulse((g - drops[i] - 4) / 24., 5), 40, 'open'), far=(20, 46, 'open'), lean=wob, bob=-.03 * abs(math.sin(tg * 6.28 + i)), smile=.7)
            if g >= 90:                                                          # the arrow crosses the light
                ax = 560 + 780 * .36 + (g - 90) * 118; ay = GY - .665 * 780 - 26 * math.sin(min(1, (g - 90) / 12.) * 2.4)
                c.save(); c.translate(ax, ay); c.scale(780, 780); self.toy(c, 0, 0); c.restore()
        A = self.layer(front, st.k); B = self.layer(back, st.k)
        zoom = keys(f, [(0, 1.0), (60, 1.035, 'linear'), (88, 1.07), (108, 1.55, 'in')], 'linear'); hot = self.HOT
        fl = 1 + .05 * noise1(t * 8, 1) + .03 * noise1(t * 19, 2) + .10 * impulse((f - 18) / 24., 5) + (.5 * smooth(96, 108, f))
        st.paint(CLOTH, hot=hot, flick=float(fl), zoom=float(zoom), ctr=hot, blurA=float(keys(g, [(0, 2.4), (8, 0.), (62, 0.), (70, 1.6), (78, 0.)], 'linear')), blurB=.8, lk=math.log2(st.k), texs=dict(tA=A, tB=B))
        FX.flame(st, hot, 250 * zoom, 92 * zoom, seed=1.3, amt=.62 + .30 * smooth(92, 108, f), glow=.30, calm=.8)
        # heads of the people watching, dark against the cloth
        rise = 1 - ease_in((f - 84) / 22., 2) * 0; dy = 260 * ease_in((f - 80) / 26., 2)

        def crowd(c):
            for i, (x, y, r, k) in enumerate(self.heads):
                b = 4 * math.sin(t * 2.2 + i * 1.7) - 14 * impulse((f - 90 - i % 3) / 24., 5); x = 960 + (x - 960) * (1 + .25 * (zoom - 1)); y = y + dy + b; c.save(); c.translate(x, y); c.scale(r, r)
                for layer in (0, 1):                                              # a hair of lamp light, then the dark head on top
                    c.set_source_rgba(*((.55, .22, .05, .9) if layer == 0 else (.018, .008, .006, 1))); e = .045 if layer == 0 else 0.; oy = 0 if layer == 0 else .035
                    c.new_path(); c.save(); c.translate(0, oy); c.save(); c.scale(.78 + e, .92 + e); c.arc(0, 0, 1, 0, 7); c.restore(); c.fill(); c.new_path(); c.save(); c.translate(0, 1.95); c.scale(1.62 + e, 1.15 + e); c.arc(0, 0, 1, math.pi, 0); c.restore(); c.fill()
                    if k == 1: c.arc(.0, -1.02, .30 + e, 0, 7); c.fill()
                    if k == 2: c.save(); c.translate(0, -.48); c.scale(1.02 + e, .58 + e); c.arc(0, 0, 1, 0, 7); c.restore(); c.fill()
                    if k == 3: c.save(); c.translate(.0, -.1); c.scale(.92 + e, 1.05 + e); c.arc(0, 0, 1, 0, 7); c.restore(); c.fill(); c.save(); c.translate(0, 1.2); c.scale(1.1 + e, 1.1); c.arc(0, 0, 1, math.pi, 0); c.restore(); c.fill()
                    c.restore()
                c.restore()
        st.vector(crowd)
        for x in (A, B): x.release()
        fade = 0.
        return st.finish(bloom=.40, thr=.95, vig=.45, grain=.018, flash=smooth(102, 108, f) * .85, flashCol='#ffdf90')

    def toy(self, c, x, y):
        c.set_source_rgb(*PU.BK); c.set_line_width(.012); c.set_line_cap(cairo.LINE_CAP_ROUND); c.move_to(x, y); c.line_to(x + .26, y); c.stroke(); c.move_to(x + .30, y); c.line_to(x + .25, y - .018); c.line_to(x + .25, y + .018); c.close_path(); c.fill(); c.set_source_rgb(*PU.DYE['red'])
        for k in (-1, 1): c.move_to(x, y); c.line_to(x - .02, y + .022 * k); c.line_to(x + .03, y + .022 * k); c.line_to(x + .05, y); c.close_path(); c.fill()
