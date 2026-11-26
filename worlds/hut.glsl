// PANCHAVATI.  a leaf hut (parnashala) at the origin, door to +z, ridge along x, 30 wide, 22 deep, eave 13, ridge 27; a cooking hearth at (16,0,20); a rock face behind at z < -46 (the wall for c4's shadow, about 120 wide, 70 high).
// ground: gentle earth y = gy(x,z) near 0 (flat within 40 of the hut).  Uniforms: fireK 0..1 (hearth glow), tone (0 dry, 1 wet), gA gB (earth lit, shade), seasonal tint leafA leafB.  DEFINE NOHUT for a bare clearing, NOROCK without the rock face.
#define TMAX 900.
#define STEPS 130
#define AOK .8
#define SUNSH 18
#define SHMAX 120.
#include "arch.glsl"
#include "paint.glsl"
uniform float fireK,tone,line,lineR;uniform vec3 gA,gB,leafA,leafB,rockA,rockB;
float gy(vec2 q){float r=length(q-vec2(0,10.));float k=smoothstep(46.,150.,r);return k*(3.*(vn(q*.016)-.35)*2.+5.*smoothstep(.45,.8,vn(q*.009+4.)))-.0;}
vec2 hut(vec3 p){float bb=sBox(p-vec3(0,14,0),vec3(24,16,19),0.);if(bb>4.) return vec2(bb,0.);vec3 q=vec3(abs(p.x),p.y,p.z);
 float yl=27.-abs(p.z)*.86-.035*p.x*p.x*.3;float sag=.5*sin(p.x*.5+p.z*.3);float th=abs(p.y-yl-sag*.4)*.75-.75;float roof=max(th,max(q.x-19.+.25*sin(p.z*3.)+.5*vn(vec2(p.z*2.,1.)),abs(p.z)-17.-.6*vn(vec2(p.x*1.6,3.))));
 float lay=fract((abs(p.z)+.4*vn(p.xz*.8))/2.6);roof-=.30*(1.-lay)+.25*abs(sin(p.x*2.2+floor(abs(p.z)/2.6)*1.7));vec2 m=vec2(roof*.6,M_DOME);
 float wall=max(max(q.x-14.6,abs(p.z)-10.6),p.y-yl);wall=max(wall,-max(q.x-13.8,abs(p.z)-9.8));float dr=oArchR(p.xy,4.2,8.6);wall=max(wall,-max(dr,-p.z));float wv=.12*abs(sin(p.y*1.9+3.14*step(.5,fract(p.x*.22))));m=U(m,vec2(wall-wv,M_WALL));
 float po=length(vec2(q.x-14.8,abs(p.z)-12.6))-.55-.08*sin(p.y*1.4);po=max(po,max(-p.y,p.y-yl));float p2=max(length(vec2(q.x-5.2,p.z-12.8))-.45,max(-p.y,p.y-16.5));float be=length(vec2(p.y-13.6,abs(p.z)-12.8))-.45;be=max(be,q.x-19.);float rd=max(length(vec2(p.y-26.9,p.z))-.6,q.x-20.5);m=U(m,vec2(min(min(po,p2),min(be,rd)),M_WOOD));
 float pl=sBox(p-vec3(0,.5,2.),vec3(18,.6,15.5),.4);return U(m,vec2(pl,M_STEP));}
vec2 rockf(vec3 p){float d0=p.z+46.;if(d0>30.||abs(p.x)>170.) return vec2(max(d0-20.,abs(p.x)-150.)*.5+4.,0.);vec4 v=voro(p.xy*vec2(.030,.018)+vec2(.2,p.z*.004));float h=62.+22.*vn(vec2(p.x*.02,2.))-.0035*p.x*p.x;float d=p.z+52.-9.*v.x-5.*vn(p.xy*.06)+max(0.,p.y-h*.7)*.35;d=max(d,p.y-h-10.*v.z);return vec2(d*.62,M_ROCK);}
vec2 hearth(vec3 p){vec3 q=p-vec3(16,0,20);float bb=length(q)-9.;if(bb>3.) return vec2(bb,0.);float a=atan(q.x,q.z);float s=TAU/9.;float i=floor(a/s);float aa=a-(i+.5)*s;float l=length(q.xz);vec3 r=vec3(sin(aa)*l,q.y-.5,cos(aa)*l-3.4);float st=sEll(r,vec3(1.15,.95+.3*h11(i),.95));float lg=sCap(q,vec3(-2.6,.5,-.6),vec3(2.2,1.6,.5),.42);lg=min(lg,sCap(q,vec3(1.6,.5,-2.),vec3(-.8,1.7,1.4),.38));lg=min(lg,sCap(q,vec3(.3,.4,2.4),vec3(.1,1.9,-1.2),.40));return U(vec2(st,M_ROCK),vec2(lg,M_WOOD));}
vec2 map(vec3 p){float g=gy(p.xz);vec2 m=vec2((p.y-g-.12*vn(p.xz*.5))*.85,M_GROUND);
#ifndef NOHUT
 m=U(m,hut(p));m=U(m,hearth(p));
#endif
#ifndef NOROCK
 m=U(m,rockf(p));
#endif
 return m;}
void surf(vec3 p,vec3 n,int m,inout Surf s){
 vec3 fp=vec3(16,3.5,20);vec3 fd=fp-p;float fr=length(fd);float fg=fireK/(1.+fr*fr/150.)*(.9+.1*sin(fT*11.)*sin(fT*7.3));vec3 fire_=vec3(1.0,.36,.07)*min(fg,.75)*(.25+.75*smoothstep(-.25,.5,dot(n,fd/max(fr,.1))));
 if(m==10){float t=fbm(p.xz*.06),t2=vn(p.xz*.6);s.base=mix(gA,gB,smoothstep(.35,.62,t)*.55);s.base*=.92+.14*t2;s.sh=gB*.5;s.ink=.25;
  // brushed tufts and pebbles of the miniature painter
  vec2 c=floor(p.xz/5.),f=fract(p.xz/5.)-.5;vec2 h=h22(c);vec2 o=f-(h-.5)*.7;oAA=gPx/5.;float tu=0.;for(int i=-1;i<=1;i++){vec2 q=o-vec2(float(i)*.07,0.);q.x-=float(i)*.25*(-q.y);tu=max(tu,oE(max(abs(q.x)-.022*(1.+q.y*3.),max(-q.y-.16,q.y-.02))));}s.base=mix(s.base,mix(leafB,leafA,h.x),tu*step(.45,h.y)*pLod(1.2)*step(28.,length(p.xz-vec2(0,8.))));
  float pb=oE(length(o*vec2(1.,1.5))-.05-.05*h.x);s.base=mix(s.base,rockA,pb*step(h.y,.14)*pLod(1.));
  float path=smoothstep(9.,5.5,abs(p.x-4.*sin(p.z*.03)))*smoothstep(8.,18.,p.z);s.base=mix(s.base,mix(gA,vec3(1.,.9,.75),.35),path*.6);
  s.base=mix(s.base,s.base*.55,tone*.8);float pud=smoothstep(.62,.66,vn(p.xz*.05+3.))*tone;if(pud>.5){s.base=mix(uAmb,uKey,.3)*.8+vec3(.02);s.sh=s.base*.6;s.cls=8.;}
  if(line>0.){float L=length(p.xz-vec2(0.,4.));float a=atan(p.x,p.z-4.)/TAU+.5;float w=abs(L-lineR+.5*(vn(vec2(a*40.,1.))-.5))-.35;if(w<0.){s.base=vec3(.05,.02,.02);s.sh=s.base;if(a<line){s.cls=4.;s.base=vec3(2.2,.9,.2);s.ink=0.;}}if(a<line) emit(s,vec3(1.2,.4,.07)*.8*exp(-abs(L-lineR)*.22));}
 }
 else if(m==3){vec2 u=vec2(p.x,p.z);float row=floor((abs(p.z)+.4*vn(p.xz*.8))/2.6),lay=fract((abs(p.z)+.4*vn(p.xz*.8))/2.6);float id=floor(p.x*.55+row*.5);float h=h21(vec2(id,row+step(0.,p.z)*40.));vec3 c=mix(leafB,leafA,.25+.75*h);float f=fract(p.x*.55+row*.5)-.5;c=mix(c,leafB*.5,smoothstep(.07,.02,abs(f))*.7);c*=1.1-.35*lay;s.base=c;s.sh=c*vec3(.40,.36,.48);s.ink=.55;s.base*=1.-.35*tone;}
 else if(m==1){float k=step(.5,fract(p.x*.22+p.z*.22));float b=.5+.5*sin(p.y*1.9+3.14*k);s.base=mix(hex(0x9a6a3c),hex(0xdcae6c),b);s.sh=s.base*vec3(.42,.34,.42);s.ink=.6;if(abs(p.x)<14.&&abs(p.z)<10.){s.base*=.5;s.base+=0.;emit(s,vec3(.8,.3,.06)*.22*fireK*smoothstep(13.,2.,p.y));}s.base*=1.-.3*tone;}
 else if(m==7){s.base=hex(0x7a4e32)*(.85+.3*vn(p.xy*vec2(3.,.6)));s.sh=s.base*vec3(.4,.34,.45);if(length(p.xz-vec2(16,20))<5.&&fireK>0.) emit(s,vec3(1.4,.4,.06)*fireK*.8*smoothstep(.4,.7,vn(p.xz*2.+fT)));}
 else if(m==4){s.base=mix(gA,hex(0xe8c090),.4);s.sh=gB*.5;}
 else{vec4 v=voro(p.xy*vec2(.030,.018)+vec2(.2,p.z*.004));float t=fbm(vec2(p.x*.05,p.y*.02)+4.);s.base=mix(rockB,rockA,smoothstep(.25,.7,t+.25*n.y+.2*v.z));s.sh=rockB*.45;float cr=fbm(vec2(p.x*.11+p.y*.02,p.y*.035));s.base=mix(s.base,rockB*.6,smoothstep(.035,.012,abs(cr-.5))*.7);float ms=smoothstep(.5,.75,n.y+.5*(vn(p.xy*.08)-.4));s.base=mix(s.base,leafB*1.1,ms*.7);if(p.z>0.){s.base=rockA*.6;}s.base*=1.-.4*tone;}
 if(fireK>0.&&s.cls!=4.) emit(s,s.base*fire_);}
