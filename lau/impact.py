"""Impact frames, speed lines, whips, shock rings, burns, irises: things done to the whole canvas."""
import numpy as np
from . import W, H
from .stage import hexc

_LINES = '''
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform vec2 res,ctr;uniform float seed,inner,amt,dens,ang,par;uniform vec3 col;
void main(){vec2 p=vec2(uv.x*res.x,(1.-uv.y)*res.y);vec2 q=p-ctr;float a,r;if(par>.5){float c=cos(ang),s=sin(ang);vec2 u=vec2(c*q.x+s*q.y,-s*q.x+c*q.y);a=u.y/res.y*6.;r=abs(u.y)/res.y+.35+.15*vn(vec2(u.x*.002+seed,3.));}else{a=atan(q.y,q.x)*3.;r=length(q/vec2(1.,.8))/res.y;}
 float k=0.;for(int i=0;i<3;i++){float f=dens*(1.+float(i)*1.7);float id=floor(a*f);float h=h21(vec2(id,seed+float(i)*9.));float w=fract(a*f)-.5;float L=inner+.55*h;float t=smoothstep(L,L+.35,r);k=max(k,step(.62,h21(vec2(id+3.,seed)))*smoothstep(.5*t,.5*t-.16,abs(w))*step(.001,t));}
 o=vec4(col*k,k)*amt;}
'''


def speedlines(st, at=(W / 2, H / 2), amt=1., col=(0, 0, 0), seed=0, inner=.32, dens=9., parallel=None):
    """radial ink lines toward a point, or parallel ones (parallel = angle in radians)"""
    st.paint(_LINES, 'over', ctr=tuple(map(float, at)), seed=float(seed), inner=float(inner), amt=float(amt), dens=float(dens), ang=float(parallel or 0), par=0. if parallel is None else 1., col=hexc(col))


_FLASH = '''
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform sampler2D tex;uniform vec2 res;uniform float lo,hi,inv,amt;uniform vec3 cA,cB,cC;
void main(){vec3 c=texture(tex,uv).rgb;float l=pow(lum(min(c,vec3(1.5))),.4545);vec2 e=1.5/res;float g=length(vec2(lum(texture(tex,uv+vec2(e.x,0)).rgb)-lum(texture(tex,uv-vec2(e.x,0)).rgb),lum(texture(tex,uv+vec2(0,e.y)).rgb)-lum(texture(tex,uv-vec2(0,e.y)).rgb)));
 l+=.06*(fbm(uv*res/9.)-.5);float a=smoothstep(lo-.01,lo+.01,l),b=smoothstep(hi-.01,hi+.01,l);if(inv>.5){a=1.-a;b=1.-b;}vec3 q=mix(cA,cB,a);q=mix(q,cC,b);q=mix(q,inv>.5?cC:cA,smoothstep(.10,.25,g));o=vec4(mix(c,q,amt),1);}
'''


def inkflash(st, dark='#0a0508', mid='#b3122a', light='#fff3dc', lo=.34, hi=.62, invert=False, amt=1.):
    """the one or two frames of a blow: the picture as a three-colour print"""
    st.post_paint(_FLASH, lo=float(lo), hi=float(hi), inv=1. if invert else 0., amt=float(amt), cA=hexc(dark), cB=hexc(mid), cC=hexc(light))


_BLUR = '''
in vec2 uv;out vec4 o;uniform sampler2D tex;uniform vec2 dir,ctr,res;uniform float zoom,spin;
void main(){vec3 s=vec3(0);float w=0.;for(int i=0;i<24;i++){float k=(float(i)+.5)/24.-.5;vec2 p=uv-dir*k/res;vec2 c=vec2(ctr.x/res.x,1.-ctr.y/res.y);vec2 q=p-c;q.x*=res.x/res.y;float a=spin*k,cs=cos(a),sn=sin(a);q=vec2(cs*q.x-sn*q.y,sn*q.x+cs*q.y)*(1.+zoom*k);q.x/=res.x/res.y;p=c+q;float g=1.-abs(k)*1.2;s+=texture(tex,p).rgb*g;w+=g;}o=vec4(s/w,1);}
'''


def whip(st, dx=0., dy=0.):
    """directional blur in pixels (whip pan, smear)"""
    if abs(dx) + abs(dy) > .5: st.post_paint(_BLUR, dir=(float(dx), float(-dy)), ctr=(W / 2, H / 2), zoom=0., spin=0.)


def zoomblur(st, at=(W / 2, H / 2), amt=.1, spin=0.):
    if abs(amt) + abs(spin) > 1e-3: st.post_paint(_BLUR, dir=(0., 0.), ctr=tuple(map(float, at)), zoom=float(amt), spin=float(spin))


_SHOCK = '''
in vec2 uv;out vec4 o;uniform sampler2D tex;uniform vec2 res,ctr;uniform float rad,wid,amt,sq;
void main(){vec2 p=vec2(uv.x*res.x,(1.-uv.y)*res.y)-ctr;p.y/=sq;float r=length(p);float k=exp(-pow((r-rad)/wid,2.));vec2 n=p/max(r,1.);vec2 d=n*k*amt;o=texture(tex,uv-vec2(d.x,-d.y*sq)/res);o.rgb*=1.+.35*k*sign(amt)*smoothstep(0.,40.,abs(amt));}
'''


def shock(st, at, rad, wid=60., amt=40., squash=1.):
    """refracting ring (pixels)"""
    st.post_paint(_SHOCK, ctr=tuple(map(float, at)), rad=float(rad), wid=float(wid), amt=float(amt), sq=float(squash))


_BURN = '''
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform sampler2D tex,tUnder;uniform vec2 res,ctr;uniform float amt,seed,grain,mode;uniform vec3 edge,under;
void main(){vec2 p=vec2(uv.x*res.x,(1.-uv.y)*res.y);float r=length((p-ctr)/res.y);float n=fbm(p/res.y*6.*grain+seed)*.62+fbm(p/res.y*24.*grain-seed)*.22;float f=(mode>.5?r*.55:0.)+n;float t=amt*(mode>.5?2.0:1.15)-.10;float d=f-t;vec3 c=texture(tex,uv).rgb;vec3 u=mode>1.5?under:texture(tUnder,uv).rgb;
 float hole=smoothstep(.006,-.006,d);float ch=smoothstep(.16,.0,d)*(1.-hole);c=mix(c,vec3(.02,.008,.006),ch*.92);float gl=smoothstep(.030,.004,abs(d-.004));c=mix(c,u,hole);c+=edge*gl*2.2+edge*smoothstep(.09,.0,abs(d))*.35;o=vec4(c,1);}
'''


def burn(st, amt, at=(W / 2, H / 2), seed=0., under=None, col='#000000', radial=True, grain=1., edge='#ff8a24'):
    """the picture burns away from a point (amt 0..1) and shows `under` (texture) or a colour"""
    if amt <= 0: return
    st.post_paint(_BURN, texs=dict(tUnder=under or st._white), ctr=tuple(map(float, at)), amt=float(amt), seed=float(seed), grain=float(grain), mode=2. if under is None else (1. if radial else 0.), edge=hexc(edge), under=hexc(col))


_IRIS = '''
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform vec2 res,ctr;uniform float rad,soft;uniform vec3 col;
void main(){vec2 p=vec2(uv.x*res.x,(1.-uv.y)*res.y)-ctr;float a=atan(p.y,p.x);float r=length(p)+soft*.6*(fbm(vec2(a*2.,3.))-.5);float k=smoothstep(rad-soft,rad+soft,r);o=vec4(col*k,k);}
'''


def iris(st, at, rad, soft=6., col=(0, 0, 0)): st.paint(_IRIS, 'over', ctr=tuple(map(float, at)), rad=float(rad), soft=float(soft), col=hexc(col))


_FROST = '''
in vec2 uv;out vec4 o;uniform sampler2D tex;uniform vec2 res;uniform float amt;
void main(){vec3 s=vec3(0);float w=0.;for(int i=0;i<40;i++){float a=float(i)*2.39996,r=sqrt(float(i)+.5)/6.4;vec2 d=vec2(cos(a),sin(a))*r*amt/res;vec3 c=texture(tex,uv+d).rgb;float k=1.+dot(c,vec3(.6));s+=c*k;w+=k;}o=vec4(s/w,1);}
'''


def defocus(st, px):
    """whole-canvas bokeh blur in pixels (draw sharp things afterwards)"""
    if px > .6: st.post_paint(_FROST, amt=float(px))


_DOF = '''
in vec2 uv;out vec4 o;uniform sampler2D tex,tZ;uniform vec2 res;uniform float focus,range_,maxr;
float coc(float z){return clamp((abs(z-focus)-range_*.35)/range_,0.,1.)*maxr;}
void main(){float z0=texture(tZ,uv).x;float c0=coc(min(z0,5e4));vec3 s=vec3(0);float w=0.;for(int i=0;i<52;i++){float a=float(i)*2.39996,r=sqrt(float(i)+.5)/7.25;vec2 d=vec2(cos(a),sin(a))*r*maxr/res;float z=texture(tZ,uv+d).x;float c=coc(min(z,5e4));float rr=r*maxr;float k=smoothstep(rr-1.5,rr+.5,z<z0?c:min(c,max(c0,.6)));if(i==0)k=1.;vec3 q=texture(tex,uv+d).rgb;k*=1.+.6*dot(q,vec3(.33));s+=q*k;w+=k;}o=vec4(s/w,1);}
'''


def dof(st, focus, rng=10., px=9.):
    """depth of field from the last close(): focus distance, how quickly it falls off, largest blur in px"""
    st.post_paint(_DOF, focus=float(focus), range_=float(rng), maxr=float(px))


_MUL = 'in vec2 uv;out vec4 o;uniform sampler2D tex;uniform vec3 m,a;\nvoid main(){vec3 c=texture(tex,uv).rgb;o=vec4(c*m+a,1);}\n'


def grade(st, mul=(1, 1, 1), add=(0, 0, 0)): st.post_paint(_MUL, m=tuple(hexc(mul)), a=tuple(hexc(add)))
