"""Kumbhakarna, the sleeping giant, and the painter of his one enormous eye."""
import numpy as np, math
from lau.stage import Fig, hexc
from lau.face import human, Face
from lau.rig import Pose, V, nz

BOX = (-1.1, -1.25, 1.1, .95)
PAL = {1: ('#80544a', '#2e1a2a', 1), 2: ('#2a1a18', '#120a0c', 5), 3: ('#e2bd84', '#70481f', 2), 4: ('#b3121f', '#4a0818', 3), 5: ('#0f7a58', '#063a34', 3), 6: ('#eadcb8', '#8a7060', 1), 7: ('#a8702e', '#482612', 1), 8: ('#8f1722', '#3a0812', 1), 9: ('#4a2a1a', '#1f100c', 1), 10: ('#8e9aa8', '#3a4450', 7)}
STYLE = dict(iris='#d88a1c', iris2='#5a1606', sclera='#ecca98', lip='#4e2428', lip2='#643032', liphi='#a0706a', kohl='#14080a', kohlk=.8, brow='#1c100e', browt=.6, browy=-.02, tilak='none', size=1.22, nose='#1c0f14', mouthw=1.7, tilt=-.09)


def _paint(P, F, k):
    for sd in (1, -1):
        P.c.save(); P.c.scale(sd, 1); ik = k['nose']
        for i in range(3): P.line([(.15 + .02 * i, -.085 - .055 * i), (.26, -.15 - .062 * i, .42, -.15 - .058 * i, .54 + .01 * i, -.04 - .06 * i)], .016 - .003 * i, ik, .8 - .18 * i)      # bags
        for i in range(4): P.line([(.58, .06 - .035 * i), (.64, .08 - .05 * i, .70, .07 - .07 * i, .76, .10 - .11 * i)], .011, ik, .6)                                                        # crow's feet
        for i in range(3): P.line([(.20, .135 + .035 * i), (.30, .205 + .03 * i, .42, .20 + .03 * i, .54, .13 + .03 * i)], .012, ik, .55)                                                  # folds of the upper lid
        P.line([(.26, -.36), (.38, -.46, .46, -.60, .44, -.80)], .022, ik, .85); P.line([(.33, -.40), (.45, -.50, .54, -.62, .54, -.76)], .012, ik, .55)
        P.line([(.07, .10), (.05, .17, .08, .22, .06, .30)], .022, ik, .8); P.line([(.12, -.05), (.10, -.12, .12, -.16, .16, -.2)], .012, ik, .6)
        c = P.c
        import cairo
        for i, (x, y) in enumerate(((.47, .06), (.17, .02), (.45, .0))): P.line([(x, y), (x - .03, y + .012, x - .05, y - .012, x - .085 + .03 * i, y + .006)], .005, '#b8301c', .55 * (F.lid > .2))
        c.restore()
    P.c.save()
    for i in range(3): P.line([(-.46, .40 + .09 * i), (-.2, .46 + .09 * i, .2, .46 + .09 * i, .46, .40 + .09 * i)], .013, k['nose'], .6)
    P.c.restore()


def face(F): return human(F.set(lid=.60 * F.lid, frown=min(1.3, .40 + .80 * F.frown)), STYLE, S=1536, extra=_paint)


KUMBHA = Fig('kumbha', 'kumbha.glsl', PAL, dim=dict(chest=3.7, shx=2.25, shy=1.25, neck=1.55, head=1.50, up=3.5, fore=3.2, hipx=1.05, hipy=-.35, th=3.5, sh=3.3, hand=1.62, foot=1.55), build=dict(chest=1.85, depth=1.85, rib=2.25, waist=2.2, hips=1.75, arm=1.95, leg=1.72, hand=1.0, belly=.6, neck=2.3, shoulder=1.35), hs=[1.2] * 8, face=face, bound=(0, 8, 0, 18), step=.78)

# ------------------------------------------------------------------ poses
_F = dict(lf=(1.75, 1.15, .5), rf=(-1.75, 1.15, .1), lft=(28, 0), rft=(-28, 0), lkn=(.35, 0, 1), rkn=(-.35, 0, 1))
KB_STAND = Pose(pel=(0, 7.5, 0), pelr=(0, 0, 0), cher=(0, 6, 0), hedr=(0, 6, 0), lh=(4.9, 7.3, 1.6), rh=(-4.9, 7.3, 1.6), lel=(.9, .2, -.5), rel=(-.9, .2, -.5), lhand='claw', rhand='claw', lfing=(-.1, -1, .25), rfing=(.1, -1, .25), lpalm=(-1, -.1, .1), rpalm=(1, -.1, .1), **_F)
KB_GRAB = Pose(pel=(0, 6.7, .4), pelr=(-10, 8, 0), cher=(-16, 22, 0), hedr=(14, -4, 0), rh=(-2.4, 7.6, 7.2), rel=(-1, .3, -.2), rhand='claw', rfing=(.15, -.35, .9), rpalm=(.2, -.9, -.2), lh=(5.0, 10.2, -1.6), lel=(.6, -.2, -.8), lhand='claw', lfing=(.4, .2, .5), lpalm=(0, -.3, 1), **{**_F, 'lf': (1.9, 1.15, -1.4), 'rf': (-1.9, 1.15, 2.2)})
KB_SLEEP = Pose(pel=(0, 2.25, 0), pelr=(0, -82, 0), cher=(0, -2, 4), hedr=(22, 16, 8), lh=(5.3, 1.0, -2.8), rh=(-1.4, 5.0, -2.9), lel=(1, .4, .3), rel=(-1, .5, .3), lhand='relax', rhand='relax', lfing=(.6, 0, .6), lpalm=(0, 1, 0), rfing=(.9, .1, -.1), rpalm=(0, -1, 0), lf=(2.2, 1.2, 5.4), rf=(-1.9, 1.3, 6.3), lkn=(.3, 1, 0), rkn=(-.5, 1, 0), lft=(24, -50), rft=(-34, -62))
_SIT = Pose(pel=(0, 2.6, -1.2), pelr=(0, -18, 0), cher=(0, 10, 3), hedr=(8, 8, 4), lh=(5.0, 2.0, 1.6), rh=(-5.2, 1.6, -2.2), lel=(1, .3, -.3), rel=(-1, .3, -.4), lhand='claw', rhand='claw', lfing=(.3, -.5, .8), lpalm=(0, -1, -.3), rfing=(-.5, -.3, -.6), rpalm=(0, -1, 0), lf=(2.4, 1.15, 4.6), rf=(-2.6, 1.15, 4.0), lkn=(.7, 1, .2), rkn=(-.8, 1, .2), lft=(30, -10), rft=(-34, -8))
_CROUCH = Pose(pel=(0, 4.9, -1.0), pelr=(0, 14, 0), cher=(0, 22, 0), hedr=(0, -14, 0), lh=(4.6, 5.0, 3.6), rh=(-4.2, 1.9, 4.2), lel=(1, .4, -.4), rel=(-1, .4, -.2), lhand='claw', rhand='fist', lfing=(-.2, -.5, .8), lpalm=(0, -1, 0), rfing=(.1, -1, .2), rpalm=(0, -.1, -1), lf=(2.5, 1.15, 2.0), rf=(-2.2, 1.1, -2.4), lkn=(.8, .3, 1), rkn=(-.8, 0, 1), lft=(30, 0), rft=(-34, 16))


def _keys(t, K):
    if t <= K[0][0]: return K[0][1]
    for (a, A), (b, B) in zip(K, K[1:]):
        if t <= b: return A.mix(B, (t - a) / (b - a))
    return K[-1][1]


def KB_RISE(t):
    """0 asleep on his back, .3 sitting, .65 one fist on the ground, 1 standing"""
    return _keys(t, [(0., KB_SLEEP), (.30, _SIT), (.65, _CROUCH), (.9, KB_STAND.set(cher=(0, -6, 0), hedr=(0, -8, 0), shrug=(.4, .4))), (1., KB_STAND)])


_HIT = KB_STAND.set(pel=(0, 7.3, -.5), pelr=(0, -10, 0), cher=(8, -20, 4), hedr=(6, -20, 4), lh=(5.6, 13.0, .6), rh=(-5.6, 12.0, 1.2), lhand='open', rhand='open', lfing=(.5, .8, .2), rfing=(-.5, .8, .2), lpalm=(0, 0, 1), rpalm=(0, 0, 1))
_TIP = _HIT.set(pel=(0, 6.2, -3.0), pelr=(4, -42, 0), cher=(4, -16, 3), hedr=(0, 4, 0), lh=(5.8, 12.4, -5.0), rh=(-5.8, 11.4, -4.4), lfing=(.5, .6, -.5), rfing=(-.5, .6, -.5), lf=(1.9, 1.5, 1.2), rf=(-1.9, 1.2, .6), lft=(26, -24), rft=(-26, -18))
_FLAT = Pose(pel=(0, 2.25, -6.0), pelr=(0, -84, 0), cher=(0, -4, 0), hedr=(10, 6, 6), lh=(5.8, 1.2, -11.0), rh=(-5.6, 1.4, -11.8), lel=(.6, .6, .2), rel=(-.6, .6, .2), lhand='open', rhand='relax', lfing=(.7, .1, -.5), rfing=(-.7, .1, -.5), lpalm=(0, 1, 0), rpalm=(0, 1, 0), lf=(2.2, 1.2, .2), rf=(-2.0, 1.3, .8), lkn=(.4, 1, 0), rkn=(-.4, 1, 0), lft=(24, -56), rft=(-30, -62))


def KB_FALL(t):
    """0 standing, .2 struck, .6 tipping over backward, 1 flat on the ground (feet stay where they were)"""
    return _keys(t, [(0., KB_STAND), (.2, _HIT), (.6, _TIP), (1., _FLAT)])


def perches(S):
    """world points on him where small climbers can hang: name -> (point, outward direction)"""
    ch = lambda p, n: (S.chest(p), S.d(np.asarray(n, float) @ S.u['Bc'])); pe = lambda p, n: (S.pelvis(p), S.d(np.asarray(n, float) @ S.u['Bp'])); hd = lambda p, n: (S.head(np.asarray(p, float) * 1.42), S.d(np.asarray(n, float) @ S.u['Bh']))
    return dict(shoulderL=ch((2.9, 2.0, -.2), (0, 1, 0)), shoulderR=ch((-2.9, 2.0, -.2), (0, 1, 0)), breastL=ch((1.3, .4, 1.95), (0, .3, 1)), breastR=ch((-1.3, .4, 1.95), (0, .3, 1)), belly=pe((.3, 1.6, 2.65), (0, 0, 1)), bellyL=pe((1.7, 1.3, 1.9), (.6, 0, .8)), bellyR=pe((-1.7, 1.3, 1.9), (-.6, 0, .8)),
                belt=pe((-.9, -.45, 2.25), (0, 0, 1)), helm=hd((0, 1.25, 0), (0, 1, 0)), hornL=hd((2.2, 1.5, .4), (1, .3, 0)), hornR=hd((-2.2, 1.5, .4), (-1, .3, 0)), elbowL=(S.joint(5) + S.d((0, 1, 0)) * .8 * S.Sc, S.d((0, 1, 0))), elbowR=(S.joint(8) + S.d((0, 1, 0)) * .8 * S.Sc, S.d((0, 1, 0))), wristL=(S.joint(6), S.d((1, 0, 0))), wristR=(S.joint(9), S.d((-1, 0, 0))), kneeL=(S.joint(11) + S.d((0, 0, 1)) * .9 * S.Sc, S.d((0, 0, 1))), kneeR=(S.joint(15) + S.d((0, 0, 1)) * .9 * S.Sc, S.d((0, 0, 1))))


# ------------------------------------------------------------------ the eye that fills the screen
EYE = r'''
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform vec2 res;uniform float fT,eOpen,ePupil,eFlame,eZoom,eRoll,eDark;uniform vec2 eAt,eGaze;uniform vec3 skinA,skinB,irisA,irisB,keyC;
float seg(vec2 p,vec2 a,vec2 b,out float t){vec2 pa=p-a,ba=b-a;t=clamp(dot(pa,ba)/dot(ba,ba),0.,1.);return length(pa-ba*t);}
float loU(float x){float k=x/1.22;return -.36*sqrt(max(0.,1.-k*k))*(1.-.12*k)-.02-.05*x;}
float upU(float x){float k=x/1.24;return .60*pow(max(0.,1.-k*k),.62)*(1.+.18*k)-.02-.05*x;}
float line(float d,float w){return 1.-smoothstep(w*.55,w,abs(d));}
vec3 flame(vec2 q,float s,out float a){q/=s;float u=(q.y+.5)/1.75;float sw=(.16*sin(fT*2.3)+.14*sin(fT*5.1+2.))*u*u;float n=.14*(vn(vec2(q.x*2.,q.y*2.2-fT*3.2))-.5)*u;float x=abs(q.x-sw+n);
  float uu=clamp(u,0.,1.);float w=.62*pow(uu,.55)*pow(1.-uu,.85)*1.15;float d=u<0.||u>1.?.2:(x-w);a=smoothstep(.015,-.05,d);float m=smoothstep(-.02,-.16,d),c=smoothstep(-.10,-.27,d)*smoothstep(.05,.25,uu);
  vec3 col=mix(vec3(.95,.25,.02),vec3(1.,.60,.10),m);col=mix(col,vec3(1.,.92,.62)*1.25,c);return mix(col,vec3(.55,.30,.75),smoothstep(.16,.0,uu)*.45);}
void main(){
  vec2 p=(uv*2.-1.)*vec2(res.x/res.y,1.);p=rot(eRoll)*(p-eAt)/eZoom;
  float x=p.x,y=p.y;float px=2./res.y/eZoom;
  float ins=step(abs(x),1.22);
  float lo=loU(x),up0=upU(x);float op=clamp(eOpen,0.,1.25);float lid=mix(lo+.015,up0,op);
  float sag=.05*(1.-op)*sin(x*2.4);lid+=sag*ins*op*3.;
  vec2 w=vec2(fbm(p*2.3),fbm(p*2.3+7.))-.5;
  // ---- hide
  float n=fbm(p*3.+w),n2=vn(p*26.);
  float bulge=length(vec2(x/1.55,(y-.06)/1.02));
  vec3 base=mix(skinA,skinB,smoothstep(.25,1.25,bulge+.5*(n-.5)));
  float lit=smoothstep(2.1,.15,length(vec2(x+.35,y-.25)))*1.05+.14;
  // the ball of the eye pushes the lid out: shade it round
  float ballY=y-mix(.0,.10,op);float ball=1.-length(vec2(x/1.34,ballY/.86));
  float sh=smoothstep(-.1,.75,ball+.30*(y*.6-x*.45));
  base*=mix(.55,1.28,sh*step(lid-.02,y)+(1.-step(lid-.02,y))*smoothstep(-1.1,.0,y)*.75);
  // wrinkles: rings that follow the almond, broken and bent, plus a fan at both corners
  float ik=0.;float loW=-.40*exp(-x*x*.85)-.02-.05*x,upW=.62*exp(-x*x*.80)-.02-.05*x;
  for(int i=0;i<9;i++){float f=float(i);float g=.075+.088*f+.013*f*f;
    float yu=mix(loW,upW,op*.62+.28)+.02+g*1.06*(.45+.55*exp(-x*x*.35))+(w.x*.10)*(.4+.1*f);
    float wd=.0135*(1.-.05*f)*(.45+.9*vn(vec2(x*2.6+f*7.,f*3.)));float br=smoothstep(.22,.42,vn(vec2(x*1.4+f*13.3,f*5.1)));
    ik=max(ik,line(y-yu,wd)*br*smoothstep(1.75,1.25,abs(x)));
    float yl=loW+.03-g*.92+.04*x*x+(w.y*.10)*(.4+.1*f);ik=max(ik,line(y-yl,wd*1.05)*smoothstep(.20,.44,vn(vec2(x*1.5+f*9.7,f*2.3)))*smoothstep(1.7,1.2,abs(x)));}
  for(int i=0;i<9;i++){float f=float(i)-4.;float t;vec2 a=vec2(1.24,-.10+.045*f),b=vec2(1.95,-.10+.20*f+.10*sin(f*3.));float d=seg(p+w*.10,a,b,t);ik=max(ik,smoothstep(.016*(1.-t)+.003,.0,d)*.95);a.x=-1.24;b.x=-1.9;a.y+=.06;b.y+=.03;d=seg(p+w.yx*.10,a,b,t);ik=max(ik,smoothstep(.016*(1.-t)+.003,.0,d)*.95);}
  // hatch in the hollow under the brow
  float ha=smoothstep(.62,1.05,y+.10*x*x)*(.5+.5*sin((x*.55+y)*88.+6.*n));ik=max(ik,smoothstep(.55,.9,ha)*.55);
  // pores, warts, cracked hide
  vec4 vo=voro(p*10.5+w*1.2);float ck=smoothstep(.07,.015,vo.y)*smoothstep(.52,.74,fbm(p*1.9+4.));ik=max(ik,ck*.55*smoothstep(.85,1.15,bulge));
  float po=smoothstep(.30,.18,length(fract(p*30.+w*3.)-.5))*step(.62,h21(floor(p*30.+w*3.)));base*=1.-.16*po;
  base*=.90+.22*n2*.5+.10*n;
  vec3 col=base*(keyC*lit*1.05+vec3(.055,.045,.085));
  // red raw rim of the lids
  float rim=min(abs(y-lid),abs(y-lo));float rr=smoothstep(.075,.02,rim)*smoothstep(1.27,1.18,abs(x));
  col=mix(col,vec3(.30,.075,.06)*(keyC*lit+.06),rr*.85);
  // ---- eyeball
  float in_=step(lo,y)*step(y,lid)*ins;
  float aa=smoothstep(0.,px*1.6,min(y-lo,lid-y))*ins;
  if(in_>.0){
    vec3 sc=mix(hex(0xe8d49a),hex(0xb98a56),smoothstep(.55,1.2,abs(x+.0)));
    float r0=length(vec2(x/1.2,y/.8));sc*=1.05-.45*r0*r0;
    vec2 c=vec2(eGaze.x*.42,eGaze.y*.22+.06);vec2 q=p-c;float r=length(q),a=atan(q.y,q.x);float R=.475;
    // veins: warped ridges running in from the corners, thinning toward the iris
    float ve=0.;for(int i=0;i<22;i++){float f=float(i),sd=mod(f,2.)<.5?-1.:1.;float u=(1.22-x*sd);float y0=(h11(f*3.7)-.5)*.9;float sl=(h11(f*9.1)-.5)*.35;
      float wob=.16*(fbm(vec2(x*2.6+f*7.,f*3.))-.5)+.05*(vn(vec2(x*11.+f,f*5.))-.5);float yy=mix(y0*.35,y0,smoothstep(0.,.6,u))+sl*u+wob*smoothstep(0.,.25,u)*2.;float len=.30+.42*h11(f*5.3);
      float tp=smoothstep(len,.0,u);ve=max(ve,smoothstep(1.,.35,abs(y-yy)/(.0035+.011*tp))*step(u,len)*step(0.,u)*(.55+.45*tp));
      float u0=len*(.25+.35*h11(f*2.1));float br=u-u0;float y2=yy+sign(h11(f*8.)-.5)*(.45*br+.25*br*br)+.05*(vn(vec2(x*9.+f*3.,f))-.5);ve=max(ve,smoothstep(1.,.35,abs(y-y2)/(.0025+.007*tp))*step(0.,br)*step(u,len*1.15)*.75);}
    ve*=smoothstep(R-.01,R+.12,r);sc=mix(sc,hex(0x9c1a10),ve*.85);sc=mix(sc,hex(0xb0301c),smoothstep(.62,1.22,abs(x))*.50+.10*smoothstep(.3,.8,fbm(p*4.)));
    // corner flesh
    float ca=smoothstep(.20,.12,length((p-vec2(-1.13,.02))*vec2(1.,1.6)));sc=mix(sc,hex(0xa03a30),ca);
    vec3 e=sc*(keyC*.95+.05);
    // iris
    if(r<R+.05){
      float k=r/R;float fb=vn(vec2(a*14.,k*3.))*.55+vn(vec2(a*37.,k*5.+3.))*.30+vn(vec2(a*80.,k*9.))*.15;float fb2=vn(vec2(a*9.+3.,k*9.));
      vec3 ir=mix(irisA,irisB,smoothstep(.40,.98,k+.25*(fb-.5)));ir=mix(ir,hex(0xffd466),smoothstep(.62,.30,k)*.55*smoothstep(.35,.7,fb));ir*=.55+.95*fb;
      ir=mix(ir,irisB*.35,smoothstep(.55,.85,fb2)*smoothstep(.40,.75,k)*.45);
      float pu=mix(.22,.56,ePupil)*(1.+.035*(vn(vec2(a*8.,2.))-.5));
      ir=mix(ir,hex(0x3a1006),smoothstep(pu+.10,pu+.02,k)*.8);ir=mix(ir,vec3(.006,.003,.004),smoothstep(pu+.012,pu-.012,k));
      ir=mix(ir,vec3(.012,.005,.006),smoothstep(.86,.985,k));
      ir*=mix(.75,1.5,smoothstep(.45,-.45,(q.y-.25*q.x)/R));                 // light pooled on the far side of the iris
      e=mix(e,ir*(keyC*1.0+.05),smoothstep(R+px*1.5,R-px*1.5,r));
    }
    // the cornea: flame, its echo, a window of sky
    float fa;vec3 fc=flame(q-vec2(-.10,.02),.30*eFlame+.001,fa);if(eFlame>0.01){e+=vec3(1.,.42,.10)*.05*eFlame*exp(-dot(q-vec2(-.10,.10),q-vec2(-.10,.10))*9.);e=mix(e,fc*1.15,fa*.97);float fb_;vec3 f2=flame((q-vec2(.25,-.23))*vec2(1.,-1.),.085*eFlame+.001,fb_);e=mix(e,f2*.7,fb_*.6);}
    float wn=smoothstep(.02,-.01,length((q-vec2(.20,.24))*vec2(1.,1.35))-.055);e=mix(e,vec3(1.,.95,.84)*1.2,wn*.85);
    // shadow of the lid and the wet line
    e*=mix(.16,1.,smoothstep(.0,.30,lid-y+.05*sin(x*9.)*.3));
    float wet=smoothstep(.030,.012,abs(y-lo-.030))*smoothstep(.2,.8,vn(vec2(x*9.,1.)))*smoothstep(1.15,.8,abs(x));e+=keyC*vec3(1.,.9,.8)*wet*.28;
    col=mix(col,e,aa);
  }
  ik*=1.-smoothstep(0.,.02,min(y-lo,lid-y))*ins*step(.01,op);
  // ---- ink of the lids, lashes
  float cw=smoothstep(1.34,1.10,abs(x));
  float lw=(.030+.020*smoothstep(-1.2,1.2,x))*(.8+.5*vn(vec2(x*5.,3.)));
  ik=max(ik,line(y-lid-.006,lw)*cw);ik=max(ik,line(y-lo+.004,.016*(.7+.6*vn(vec2(x*7.,9.))))*cw*.95);
  ik=max(ik,line(y-(mix(lo,up0,op)+.13*op+.115+.06*(1.-op)),.020*(.6+.7*vn(vec2(x*4.,1.))))*smoothstep(1.30,1.05,abs(x)));
  for(int i=0;i<26;i++){float f=float(i);float lx=-1.12+f*.0895+.03*sin(f*5.);float ly=mix(loU(lx)+.015,upU(lx),op)+.15*op*(1.-op)*sin(lx*2.4);float L=(.17+.13*h11(f*3.1))*(.6+.5*smoothstep(-1.2,.6,lx));float dy=mix(-.75,.62,op);vec2 d=normalize(vec2(lx*.55+.25*(h11(f)-.5),dy));vec2 m=vec2(lx,ly)+d*L*.55+vec2(.015*sign(lx),0.),b=vec2(lx,ly)+d*L+vec2(.05*sign(lx)+.02,mix(-.02,.045,op));
    float t,d1=seg(p,vec2(lx,ly-.004),m,t);float w1=mix(.0150,.010,t);float d2,t2;d2=seg(p,m,b,t2);float w2=mix(.010,.001,t2);ik=max(ik,max(smoothstep(w1+px,w1-px,d1),smoothstep(w2+px,w2-px,d2)));}
  // bristles of the brow across the top
  for(int i=0;i<34;i++){float f=float(i);float bx=-1.9+f*.115+.06*h11(f);float by=1.04+.06*sin(f*2.)-.14*smoothstep(0.,1.6,abs(bx));vec2 a=vec2(bx,by+.12),b=a+vec2(.20+.16*h11(f*7.),-.30-.22*h11(f*3.));float t;float d=seg(p,a,b,t);float w1=mix(.034,.002,t);ik=max(ik,smoothstep(w1+px,w1-px,d));}
  col=mix(col,vec3(.010,.005,.009),clamp(ik,0.,1.)*.96);
  float vg=smoothstep(2.15,.5,length(vec2(x,y*1.25)));col*=mix(1.,vg,eDark);
  o=vec4(max(col,0.),1.);
}
'''


def eye(st, open=1., gaze=(0., 0.), pupil=.35, flame=1., zoom=1., at=(0., 0.), roll=0., key='#ffbe7a', dark=.6, skin=('#8a5f55', '#3a2230'), iris=('#e0901c', '#5a1c08'), t=None):
    """paint the giant's eye over the whole canvas (call between st.clear and st.finish).  open 0 shut .. 1 wide (1.15 startled), gaze -1..1, pupil 0 pin .. 1 huge, flame = size of the flame mirrored in it, zoom / at (screen units, y up, height = 2) / roll frame it"""
    st.paint(EYE, eOpen=float(open), eGaze=tuple(float(v) for v in gaze), ePupil=float(pupil), eFlame=float(flame), eZoom=float(zoom), eAt=tuple(float(v) for v in at), eRoll=math.radians(roll), eDark=float(dark), keyC=hexc(key), skinA=hexc(skin[0]), skinB=hexc(skin[1]), irisA=hexc(iris[0]), irisB=hexc(iris[1]))
