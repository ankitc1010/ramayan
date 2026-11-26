"""g1 (72): Rama and Sita in profile, and the dark between their faces is a lamp (f0-20).  His hand lays the jewel in her palm (f24).  Her eyes, one tear (f40); his (f54); the lamp again (f62)."""
from lau.shot import *
from lau.look import *
from chars.armonly import ARM, SKIN, place_hand
from .g_kit import *

FL_AT = V(0., 14.05, 0.)

BG = '''
#include "noise.glsl"
#include "orn.glsl"
in vec2 uv;out vec4 o;uniform vec2 res,c;uniform float fT,warm,u_;      // c = the wick, u_ = pixels per unit of the figures
float band(vec2 q,float y,float w,float cv){return smoothstep(w+.006,w,abs(q.y-y+cv*(1.-q.x*q.x*2.2)));}
void main(){vec2 p=vec2(uv.x*res.x,(1.-uv.y)*res.y);vec2 q=(p-c)/u_;q.y=-q.y;float r=length(q);          // figure units round the wick, y up
 vec3 b=mix(hex(0x101a48),hex(0x04061a),smoothstep(.8,6.2,length(q*vec2(.8,1.1)+vec2(0,.9))));b*=.72+.5*fbm(p/210.+3.);
 b+=hex(0xff8a34)*(exp(-r*r*.9)*.13+exp(-r*1.05)*.07)*warm;
 // the body of the lamp: everything under the rim, between the faces
 float sag=.085*(1.-q.x*q.x*1.6);float body=smoothstep(.02,-.02,q.y+sag+.05)*smoothstep(2.1,1.5,abs(q.x));
 vec3 v=hex(0x010106);float lite=exp(q.y*.9)*.85+.16;vec3 gold=mix(hex(0xb8641c),hex(0xffd27a),smoothstep(-.6,.5,q.x+.35*sin(q.y*2.)))*lite;
 float x=q.x/ max(.2,1.),k=0.;
 k+=band(q,-.30,.014,.06)*.8+band(q,-.40,.010,.06)*.5;
 vec2 e=vec2(q.x*8.5,(q.y+.86+.05*(1.-q.x*q.x*2.))/.28);oAA=.05;k+=oLotus(e)*step(0.,e.y)*step(e.y,1.)*.42;
 k+=band(q,-.90,.010,.05)*.6+band(q,-.53,.008,.05)*.5;
 e=vec2(q.x*5.2,(q.y+1.98+.07*(1.-q.x*q.x))/.60);k+=oLotus(e)*step(0.,e.y)*step(e.y,1.)*.40;
 k+=band(q,-1.32,.012,.06)*.6+band(q,-2.02,.012,.07)*.6;float bd=length(vec2(fract(q.x*7.)-.5,(q.y+2.14+.07*(1.-q.x*q.x))*7.));k+=smoothstep(.30,.22,bd)*.5;k+=band(q,-2.26,.010,.07)*.5;
 e=vec2(q.x*6.,(q.y+3.1+.06*(1.-q.x*q.x*2.))/.5);k+=oLotus(e)*step(0.,e.y)*step(e.y,1.)*.30+band(q,-3.14,.012,.06)*.4+band(q,-2.56,.010,.06)*.4;
 v+=gold*min(k,1.)*.26;
 b=mix(b,v,body);
 // the rim: a brass dish seen edge-on, oil in it
 vec2 rq=vec2(q.x/.80,(q.y+.06)/.085);float el=length(rq);vec3 rim=mix(hex(0x5a2a0c),hex(0xffc860),smoothstep(-.5,.9,-rq.y*.6+.5*exp(-rq.x*rq.x*9.)+.25*sin(rq.x*9.)));
 float lip=smoothstep(1.06,1.02,el);vec3 in_=mix(hex(0x6a2a0a),hex(0xffb040),exp(-q.x*q.x*7.));b=mix(b,rim*1.1,lip);b=mix(b,in_,smoothstep(.90,.84,length(rq*vec2(1.,1.15)-vec2(0,.12))));
 o=vec4(b,1);}
'''


BOKEH = '''
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform vec2 res,c;uniform float fT,warm,rad;
void main(){vec2 p=vec2(uv.x*res.x,(1.-uv.y)*res.y);vec2 q=(p-c)/res.y;float r=length(q);vec3 b=mix(hex(0x101a48),hex(0x04061a),smoothstep(.1,1.1,r));b*=.72+.5*fbm(p/210.+3.);
 b+=hex(0xff8a34)*(exp(-r*r*16.)*.22+exp(-r*3.4)*.14)*warm;
 vec2 e=q;e.y*=e.y>0.?1.25:.62;float d=length(e)-rad;float fl=smoothstep(.022,-.022,d);vec3 f=mix(hex(0xff8a24),hex(0xffd890)*1.15,smoothstep(.0,-.05,d));b=mix(b,f,fl*.95);o=vec4(b,1);}
'''
HER = ARM.variant(pal={1: SKIN['sita']}, u=dict(side=1, band=0), build=dict(arm=.70, hand=.90)); HIS = ARM.variant(pal={1: ('#2f78cc', '#1c3f88', 1)}, u=dict(side=1, band=2))


class Shot(ShotBase):
    id = 'g1'; n = 72
    EVENTS = [(0, 'lamp bed', dict(dur=72)), (2, 'breath', dict(soft=1)), (24, 'jewel on palm', {}), (30, 'hand withdraws', dict(soft=1)), (46, 'tear', {}), (54, 'breath', dict(soft=1)), (62, 'two breaths', dict(soft=1))]

    def frame(self, f, st):
        st.clear('#000', f=f)
        if 20 <= f < 40: return self.hands(f, st, st.t)
        if 40 <= f < 62: return self.eyes(f, st, st.t)
        return self.vase(f, st, st.t)

    def hands(self, f, st, t):
        g = on2(f); u = (f - 20) / 19.; palm = V(.0, 0, 0); top = palm + V(-.05, .24, .02)
        cam = Cam(lerp(V(-.5, 4.1, 8.4), V(-.2, 3.4, 7.3), ease_io(u, 1.5)), lerp(V(-.15, .75, 0), V(.0, .55, 0), ease_io(u, 1.5)), 21.5); st.cam = cam; I = flick(t, 2.)
        st.paint(BOKEH, c=(900. - 20 * u, 150.), warm=float(I), rad=.085)
        dip = -.10 * impulse((g - 24) / 24., 5); gem = top + V(0, dip, 0)
        L = Light(key=(-.1, .6, -.8), keyCol=(.16, .12, .12), amb=(.05, .055, .13), rim=(0, .5, -.9), rimCol=(1.3, .62, .22), bounceCol=(0, 0, 0), envT='#ffb060', envM='#c8641c', envB='#1a1a4a', pts=[(V(.3, 2.0, -1.1), 2.1, tuple(np.array([1.5, .95, .55]) * I)), (V(-1.5, 2.6, 3.0), 2.6, (.34, .30, .30))], shadow=False, ink=3.6, inkRef=.5, inkCol='#04030c', hi=.35)
        st.open(cam, L)
        Ph = PZ.STAND.set(rh=(-2.6, 9.9, 3.9), rel=(-.5, -1, -.2), rhand=curl('open', 'cup', keys(g, [(28, .25), (38, .85, 'io')])), rfing=(0, 0, 1), rpalm=(0, 1, 0)); Sh = st.fig(HER, Ph, draw=False)
        st.fig(HER, Ph, M=place_hand(Sh, 'R', palm + V(0, dip - .10, 0), (-.95, .06, .10), (.03, 1, .18), 1.0))
        d = keys(g, [(20, (-1.05, 1.75, -.25)), (24, (-.62, 1.02, -.02), 'io'), (27, (-.70, 1.14, -.04)), (30, (-.95, 1.45, -.12), 'io'), (40, (-3.6, 2.6, -.5), 'io')])
        Pr = PZ.STAND.set(rh=(-2.6, 9.6, 3.7), rel=(-.6, -.5, -.2), rhand=curl('pinch', 'relax', keys(g, [(24, 0.), (30, 1., 'io')])), rfing=(0, 0, 1), rpalm=(0, -1, 0)); Sr = st.fig(HIS, Pr, draw=False); pw = palm + V(*d)
        st.fig(HIS, Pr, M=place_hand(Sr, 'R', pw, (.80, -.58, .10), (-.35, -.75, .55), 1.06))
        carry = pw + V(.60, -.58, .06); jp = gem if g >= 24 else carry; yv = nz(V(-.75, .25, -.2)) if g >= 24 else nz(V(-.55, .75, 0)); zv = V(.10, .92, .42) if g >= 24 else V(.55, .55, .70)
        st.fig(JEWEL, M=PR.place(jp, yv, zv, .31)); st.close()
        if g >= 24:
            k = .55 + .45 * math.sin(t * 8) ** 2; FX.particles(st, (gem + V(-.06, .12, .10))[None], .22 * k, '#fff0c8', 'glint', alpha=.8)
            FX.flame(st, gem + V(.05, .06, .12), .13, seed=1.3, glow=.0, amt=.75 * smooth(24, 30, f))
        FX.embers(st, 10, ((-.8, 1.2, -2.5), (1., 1.8, -2.0)), t, rise=1.2, size=.02, seed=4, life=2., swirl=.25)
        IM.dof(st, float((gem - cam.eye) @ cam.R[2]), 3.4, 5.)
        return st.finish(bloom=.42, thr=.95, vig=.55, contrast=1.06)

    def eyes(self, f, st, t):
        her = f < 54; a, n = (40, 14) if her else (54, 8); u = (f - a) / n; g = on2(f); I = flick(t, 2.)
        fig, P = (SITA, sita.S_STAND.set(pelr=(0, 0, 0), cher=(0, -1, 0), hedr=(0, -5, 1.5), pel=(0, 8.22, 0))) if her else (RAMA, PZ.STAND.set(hedr=(0, 6, -1.5)))
        S = st.fig(fig, P, draw=False); fw = S.d(V(0, 0, 1) @ S.u['Bh']); sd = S.d(V(1, 0, 0) @ S.u['Bh']); up = np.cross(fw, sd); e = S.head((0, .0, .75)); s = 1. if her else -1.
        cam = Cam(e + fw * (9.0 - .5 * u) + sd * (1.5 * s) - up * .5, e + up * (-.16 - .04 * u) + sd * .02 * s, (9.6 - .7 * u) if her else (9.4 - .5 * u), roll=1.2 * s); st.cam = cam
        st.paint(BOKEH, c=(150. if her else 1770., 760.), warm=.7 * float(I), rad=.075)
        src = e + fw * 2.6 - up * 1.5 + sd * .5 * s
        L = Light(key=tuple(fw * .4 + sd * s * .8 - up * .25), keyCol=(.30, .17, .085) if her else (.17, .15, .16), amb=(.055, .05, .105), rim=tuple(-fw * .3 - sd * s + up * .3), rimCol=(.10, .16, .42), bounceCol=(.10, .04, .015) if her else (.05, .04, .05), envT='#24305a', envM='#ff9a40', envB='#5a2414',
                  pts=[(src, 1.9, tuple(np.array([1.45, .84, .42] if her else [1.55, 1.18, .92]) * I))], shadow=False, ink=4., inkCol='#05040c', hi=.3)
        if her: fc = Face(lid=keys(g, [(40, .80), (44, .86), (48, .80), (54, .84)]), gy=.12, smile=keys(g, [(44, .02), (52, .22, 'io')]), sad=keys(g, [(40, .30), (50, .16)]), spark=1., tear=round(keys(f, [(40, .10), (45, .30), (53, 1.0, 'in')]), 3))
        else: fc = Face(lid=keys(g, [(54, .66), (58, .80, 'io')]), gy=-.10, smile=.26, sad=.08, spark=1.)
        st.open(cam, L); st.fig(fig, P, face=fc); st.close()
        FX.embers(st, 8, (tuple(e - V(2, 1.4, 0) + fw), tuple(e + V(2, -.8, 0) + fw * 1.5)), t, rise=.9, size=.014, seed=6 + her, life=2.)
        return st.finish(bloom=.42, thr=.95, vig=.6, contrast=1.06)

    def vase(self, f, st, t):
        g = on2(f); br = .05 * math.sin(g / 24. * 2.4); br2 = .05 * math.sin(g / 24. * 2.4 + 1.1)
        k = ease_in((f - 62) / 10., 1.35) if f >= 62 else 0.; c0 = V(0, 12.95, 0); at = lerp(c0, FL_AT + V(0, .12, 0), ease_io(clamp((f - 62) / 10.), 1.6)) if f >= 62 else c0
        cam = Cam(at + V(0, 0, 46), at, (6.9 - .012 * f) if f < 20 else lerp(6.6, 3.2, k)); st.cam = cam; d = 1.58
        I = flick(t, 2.); x, y, z = cam.project(FL_AT); st.paint(BG, c=(float(x), float(y)), warm=float(I), u_=float(cam.px(FL_AT)))
        for who in (0, 1):
            sg = 1 if who else -1
            L = Light(key=(sg * .6, .3, -1), keyCol=(.03, .045, .12), amb=(.026, .032, .085), rim=(-sg, .15, -.15), rimCol=(1.5, .72, .24) if who else (.28, .34, .46), bounceCol=(0, 0, 0), envT='#24305a', envM='#ff9a40', envB='#5a2414',
                      pts=[(FL_AT + V(0, -.5, .55), 1.35, tuple(np.array([1.9, .98, .42] if who else [1.55, 1.30, 1.10]) * I))], shadow=False, ink=3.2, inkCol='#03030a')
            st.open(cam, L)
            if who: st.fig(SITA_P, sita.S_STAND.set(pelr=(0, 0, 0), pel=(0, 8.22, 0), cher=(0, -1 + br2 * 12, 0), hedr=(0, -3, 0), lh=(1.4, 7.5, .9), rh=(-1.4, 7.5, .9)), at=(d, .46, 0), yaw=-90, face=Face(lid=.85, smile=.15, spark=.9))
            else: st.fig(RAMA, PZ.STAND.set(cher=(0, br * 12, 0), hedr=(0, 7, 0)), at=(-1.46, 0, 0), yaw=90, face=Face(lid=.82, smile=.22, spark=.9))
            st.close()
        FX.flame(st, FL_AT, .95, seed=1.3, glow=.40 * I, calm=.8)
        return st.finish(bloom=.42, thr=.95, vig=.5, contrast=1.06)
