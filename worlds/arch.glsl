// architecture: distance functions.  Foot at y = 0, centred in x and z, unless said.  v2 results are (distance, material)
#include "orn.glsl"
#define M_WALL 1.
#define M_GOLD 2.
#define M_DOME 3.
#define M_STEP 4.
#define M_WATER 5.
#define M_ROCK 6.
#define M_WOOD 7.
#define M_TRIM 8.
#define M_CLOTH 9.
#define M_GROUND 10.
#define M_LAMP 11.
#define M_DARK 12.
#define M_COL 13.
float aBox2(vec2 q,vec2 b){q=abs(q)-b;return length(max(q,0.))+min(max(q.x,q.y),0.);}
float aOct(vec2 p){p=abs(p);return max(max(p.x,p.y),(p.x+p.y)*.70711);}
// pot-and-foliage column: stepped plinth, fluted shaft with ring bands, bell and lotus capital, square abacus
float aColumn(vec3 p,float h,float r){float l=length(p.xz),y=p.y;float d=max(aOct(p.xz)-r*1.75,abs(y-r*.35)-r*.35);d=min(d,max(l-r*(1.45-.22*smoothstep(r*.7,r*1.5,y)),abs(y-r*1.1)-r*.45));
 float sh=r*(.95-.14*smoothstep(0.,h,y));float yb=h-y;float bell=r*.70*smoothstep(r*3.0,r*1.15,yb)*smoothstep(r*.55,r*1.1,yb);float e=l-sh-bell-r*.10*smoothstep(r*.34,r*.28,abs(yb-r*3.3))-r*.12*smoothstep(r*.30,r*.22,abs(y-h*.42));
 if(e<r*.5){float a=atan(p.x,p.z);float fl=smoothstep(r*1.6,r*2.2,y)*smoothstep(r*3.6,r*4.0,yb)*smoothstep(r*.32,r*.5,abs(y-h*.42));e+=r*.07*fl*(abs(sin(a*8.))-.2);e-=r*.06*abs(sin(a*6.))*smoothstep(r*2.6,r*1.2,yb)*smoothstep(r*.5,r*1.,yb);}
 d=min(d,max(e*.82,abs(y-h*.5)-h*.5+r*.4));d=min(d,max(l-r*(1.0+.5*smoothstep(r*1.0,r*.35,yb)),abs(yb-r*.7)-r*.34));d=min(d,max(max(abs(p.x),abs(p.z))-r*1.75,abs(yb-r*.22)-r*.22));return d;}
// ogee dome of radius r on a short drum, with lotus collar and finial; total height about 2.5 r
float aDomeBody(vec3 p,float r){float l=length(p.xz);float a=r*.0;float b=sEll(p-vec3(0,.66*r,0),vec3(r,.72*r,r));float k=clamp((p.y-1.05*r)/(.75*r),0.,1.);float c=(l-mix(.60*r,.03*r,pow(k,.55)))*.80;c=max(c,abs(p.y-1.42*r)-.38*r);b=smin(b,c,.18*r);b=max(b,.10*r-p.y);return min(b,max(l-.86*r,abs(p.y-.12*r)-.14*r));}
float aFinial(vec3 p,float s){float d=length(p-vec3(0,.10*s,0))-.16*s;d=min(d,sEll(p-vec3(0,.36*s,0),vec3(.11,.12,.11)*s));d=min(d,length(p-vec3(0,.56*s,0))-.07*s);return min(d,sCone(p,vec3(0,.5*s,0),vec3(0,1.*s,0),.035*s,.006*s));}
vec2 aDome(vec3 p,float r){float f=aFinial(p-vec3(0,1.76*r,0),r*.72);f=min(f,max(abs(length(p.xz)-.90*r)-.06*r,abs(p.y-.27*r)-.045*r));return U(vec2(aDomeBody(p,r),M_DOME),vec2(f,M_GOLD));}
// pavilion: plinth, four columns, wide eave, dome.  s = half width of the plinth; height about 4.4 s
vec2 aChhatri(vec3 p,float s){float bb=length(p-vec3(0,2.1*s,0))-2.7*s;if(bb>s*1.2) return vec2(bb,M_DOME);vec3 q=vec3(abs(p.x),p.y,abs(p.z));float d=sBox(p-vec3(0,.14*s,0),vec3(s,.14*s,s),.02*s);float c=sCyl(q-vec3(.74*s,1.1*s,.74*s),.115*s,.95*s,.02*s);c=min(c,sBox(q-vec3(.74*s,.40*s,.74*s),vec3(.17,.14,.17)*s,.02*s));c=min(c,sBox(q-vec3(.74*s,1.86*s,.74*s),vec3(.20,.12,.20)*s,.02*s));
 float rl=max(sBox(p-vec3(0,.50*s,0),vec3(.84,.20,.84)*s,.0),-sBox(p-vec3(0,.5*s,0),vec3(.76,.6,.76)*s,0.));d=min(d,rl);
 float e=sBox(p-vec3(0,2.06*s,0),vec3(.90,.14,.90)*s,.01*s);float ev=max(abs(p.y-2.2*s+.10*max(q.x,q.z))-.05*s,max(q.x,q.z)-1.22*s)*.95;d=min(d,min(c,min(e,ev)));vec2 m=aDome(p-vec3(0,2.22*s,0),.86*s);return U(vec2(d,M_WALL),m);}
// stepped plinth block with cornice slabs every fh, pierced parapet.  h = half width, height, half depth
float aBlock(vec3 p,vec3 h,float fh){float d=sBox(p-vec3(0,h.y*.5,0),vec3(h.x,h.y*.5,h.z),.15);float k=clamp(round(p.y/fh),1.,floor(h.y/fh+.01));vec3 q=vec3(p.x,p.y-k*fh,p.z);d=min(d,sBox(q,vec3(h.x+1.7,.75,h.z+1.7),.1));d=min(d,sBox(q-vec3(0,-1.6,0),vec3(h.x+.8,.6,h.z+.8),.1));return min(d,sBox(p-vec3(0,1.2,0),vec3(h.x+1.5,1.2,h.z+1.5),.1));}
float aParapet(vec3 p,vec2 h,float ht,float per){vec2 q=abs(p.xz)-h;float o=max(q.x,q.y);float w=abs(o)-.7;bool xf=q.x>q.y;float u=xf?p.z:p.x;float k=abs(fract(u/per)-.5)*2.;float top=ht*(.45+.55*smoothstep(.95,.35,k)*(1.-.35*smoothstep(.5,.0,k)*0.));return max(w,max(p.y-top,-p.y-.6))*.75;}
float aSpire0(vec3 p,float w,float h){float m=max(abs(p.x),abs(p.z));float y=clamp(p.y/(h*.86),0.,1.);float d=max(m-w*(1.-.82*pow(y,1.6)),max(-p.y,p.y-h*.86))*.75;return min(d,sEll(p-vec3(0,h*.9,0),vec3(w*.34,h*.05,w*.34)));}
// curved (nagara) spire on its sanctum: w half width, h total height
vec2 aShikhara(vec3 p,float w,float h){vec3 q=vec3(abs(p.x),p.y,abs(p.z));float m=max(q.x,q.z),n=min(q.x,q.z);float y=clamp((p.y-.22*h)/(.60*h),0.,1.);float r=w*(1.-.80*pow(y,1.55));float rib=r*(step(n,r*.30)*.14+step(n,r*.62)*.09);float ring=.018*w*abs(sin(p.y*PI/(h*.020)));
 float b=max(m-r-rib+ring*step(.22*h,p.y),max(-p.y,p.y-.82*h))*.72;float l=length(p.xz);float a=atan(p.x,p.z);float am=sEll(p-vec3(0,.855*h,0),vec3(.36*w,.030*h,.36*w)*(1.+.05*cos(a*20.)));b=min(b,max(l-.20*w,abs(p.y-.83*h)-.03*h));b=min(b,sBox(p-vec3(0,.10*h,0),vec3(w*1.18,.012*h,w*1.18),.1));b=min(b,sBox(p-vec3(0,.215*h,0),vec3(w*1.22,.010*h,w*1.22),.1));b=min(b,sBox(p-vec3(0,.02*h,0),vec3(w*1.35,.02*h,w*1.35),.1));
 vec3 g=vec3(q.x,p.y,q.z);if(g.z>g.x) g=g.zyx;g-=vec3(w*.98,.22*h,0);float tur=aSpire0(g,w*.30,h*.34);b=min(b,tur);float f=aFinial(p-vec3(0,.885*h,0),.115*h);return U(vec2(min(b,am),M_WALL),vec2(min(am-.0,f),M_GOLD));}
// stepped (dravida) gate tower: half width w, half depth d, height h, n storeys; barrel roof with a row of finials; a doorway is painted or carved by the caller
vec2 aGopura(vec3 p,float w,float d,float h,float n){float y0=h*.16,y1=h*.82;float t=clamp((p.y-y0)/(y1-y0),0.,1.);float k=floor(t*n),f=fract(t*n);float s=1.-.60*(k/n)-.0;vec2 hw=vec2(w,d)*s;vec2 q=abs(p.xz);float o=max(q.x-hw.x,q.y-hw.y);float co=.055*w*s*(smoothstep(.62,.70,f)-smoothstep(.84,.95,f));float u=q.x-hw.x>q.y-hw.y?p.z:p.x;float per=w*.18;float pil=.018*w*smoothstep(.30,.36,abs(fract(u/per)-.5))*step(f,.62);
 float sl=o-co*step(y0,p.y)-pil;float b=max(sl,max(-p.y,p.y-y1))*.70;b=min(b,max(max(q.x-w*1.06,q.y-d*1.06),abs(p.y-y0)-.012*h));b=min(b,max(max(q.x-w*1.05,q.y-d*1.05),abs(p.y-.01*h)-.02*h));
 vec2 tp=vec2(w,d)*.42;float r=tp.y*1.10;float bar=max(length(vec2(p.z,p.y-y1-.02*h))-r,q.x-tp.x*1.08);bar=max(bar,y1-p.y);float rib=.0;float an=max(length(vec2(p.z,p.y-y1-.02*h))-r*1.16,abs(q.x-tp.x*1.08)-.03*w);bar=min(bar,max(an,y1-p.y));vec3 fp=vec3(p.x-clamp(round(p.x/(tp.x*.5)),-2.,2.)*tp.x*.5,p.y-y1-.02*h-r*.94,p.z);float fn=aFinial(fp,h*.075);return U(U(vec2(b,M_WALL),vec2(bar*.9,M_DOME)),vec2(fn,M_GOLD));}
// wall running along x from -L to L: height h, half thickness t, merlons of period per
float aRampart(vec3 p,float L,float h,float t,float per){float x=abs(p.x)-L;float b=max(x,max(abs(p.z)-t-.06*max(0.,h*.5-p.y),p.y-h));b=min(b,max(x,max(abs(p.z)-t*1.12,abs(p.y-h)-.025*h)));float k=abs(fract(p.x/per)-.5)*per;float mh=h+per*.55*(1.-smoothstep(per*.26,per*.40,k))+per*.22*(1.-smoothstep(0.,per*.26,k));float m=max(x,max(abs(p.z-t*.8)-t*.14,max(p.y-mh,h-.2-p.y)))*.6;return max(min(b,m),-p.y);}
float aTower(vec3 p,float r,float h,float per){float l=length(p.xz);float R=r*(1.10-.16*smoothstep(0.,h,p.y));float d=max(l-R,p.y-h);d=min(d,max(l-R*1.10,abs(p.y-h*.93)-h*.02));float a=atan(p.x,p.z)*r;float k=abs(fract(a/per)-.5)*per;float mh=h+per*.6*(1.-smoothstep(per*.24,per*.38,k));return max(min(d,max(abs(l-R*.95)-r*.08,p.y-mh)*.6),-p.y);}
// gateway of two posts and n curved cross beams with rolled ends; w half span, h height of the lowest beam
vec2 aTorana(vec3 p,float w,float h,float t){vec3 q=vec3(abs(p.x),p.y,p.z);float d=sBox(q-vec3(w,h*.5,0),vec3(t,h*.5,t),.05*t);d=min(d,sBox(q-vec3(w,h*.06,0),vec3(t*1.5,h*.06,t*1.5),.05*t));d=min(d,sBox(q-vec3(w,h*.98,0),vec3(t*1.5,h*.03,t*1.5),.05*t));d=min(d,sBox(q-vec3(w,h*1.30,0),vec3(t*.8,h*.32,t*.8),.05*t));float k=clamp(round((p.y-h*1.10)/(h*.24)),0.,2.);float yc=h*1.10+k*h*.24+.10*h*(1.-q.x*q.x/(w*w*2.2));float L=w*(1.75-.16*k);float b=max(abs(p.y-yc)-h*.055,max(abs(p.z)-t*.62,q.x-L))*.85;vec2 e=vec2(q.x-L+h*.02,p.y-yc+.0);float ro_=max(length(e)-h*.085,abs(p.z)-t*.72);d=min(d,min(b,ro_));float f=aFinial(q-vec3(w*.0,h*1.10+2.*h*.24+.155*h,0),h*.34);f=min(f,aFinial(q-vec3(w,h*1.62,0),h*.22));return U(vec2(d,M_WALL),vec2(f,M_GOLD));}
// staircase rising toward -z from z = 0: rise and run of a step
float aStairs(vec2 q,float rise,float run){float u=-q.x;float i=floor(u/run);float top=(i+1.)*rise;float a=q.y-top;float b=(i+1.)*run-u;float nx=top+rise-q.y;float d=a;if(nx>0.) d=min(d,b);if(u<0.) d=length(vec2(-u,max(q.y-rise,0.)));return d*.95;}
// bell-roofed (bangla) balcony on a wall at z = 0, projecting to +z: half width w
vec2 aJharokha(vec3 p,float w){float bb=sBox(p-vec3(0,1.3*w,.4*w),vec3(1.3*w,2.2*w,.8*w),0.);if(bb>w) return vec2(bb,M_TRIM);vec3 q=vec3(abs(p.x),p.yz);float d=sBox(p-vec3(0,.35*w,.35*w),vec3(w,.35*w,.38*w),.03*w);float br=max(q.z-.75*w*clamp((p.y+.7*w)/(.7*w),0.,1.),max(abs(p.y+.35*w)-.35*w,abs(q.x-.6*w)-.10*w));br=max(br,-q.z);d=min(d,br*.7);d=min(d,sCyl(q-vec3(.84*w,1.2*w,.62*w),.08*w,.6*w,.01));d=min(d,sBox(p-vec3(0,-.02*w,.38*w),vec3(1.08*w,.06*w,.46*w),.02*w));
 float yc=1.86*w-.30*w*q.x*q.x/(w*w);float rf=max(abs(p.y-yc)-.07*w,max(q.x-1.22*w,abs(p.z-.4*w)-.52*w))*.85;float dm=max(length(vec2(p.y-yc+.15*w,(p.z-.36*w)*.75))-.42*w,max(q.x-1.02*w,yc-p.y))*.75;vec2 f=vec2(aFinial(p-vec3(0,2.14*w,.36*w),.55*w),M_GOLD);return U(U(vec2(d,M_WALL),vec2(min(rf,dm),M_TRIM)),f);}
float aBaluster(vec3 p,float L,float h,float per){float x=abs(p.x)-L;float d=max(x,max(abs(p.z)-.10*h,min(abs(p.y-h*.95)-.06*h,abs(p.y-h*.08)-.08*h)));float u=p.x-per*round(p.x/per);float r=.10*h*(1.+.8*smoothstep(.30,.0,abs(p.y/h-.42)));return min(d,max(max(length(vec2(u,p.z))-r,abs(p.y-h*.5)-h*.45),x)*.8);}
// tall many-tiered lamp pillar; n dishes
vec2 aDeepa(vec3 p,float h,float r){float l=length(p.xz);float d=max(aOct(p.xz)-r*1.1,abs(p.y-.02*h)-.03*h);d=min(d,max(l-r*.22*(1.-.3*p.y/h),abs(p.y-h*.5)-h*.5));float k=clamp(round((p.y-.2*h)/(.16*h)),0.,4.);float yy=p.y-.2*h-k*.16*h;float R=r*(1.-.15*k);d=min(d,max(l-R*(.55+.45*smoothstep(-.02*h,.015*h,yy)),abs(yy)-.018*h)*.8);return U(vec2(d,M_GOLD),vec2(aFinial(p-vec3(0,.98*h,0),.10*h),M_GOLD));}
float aFlagpole(vec3 p,float h){return min(sCyl(p-vec3(0,h*.5,0),.35,h*.5,.02),length(p-vec3(0,h,0))-.8);}
