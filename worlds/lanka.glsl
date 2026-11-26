// LANKA: golden city on a three-peaked rock in the sea.  Origin = middle of the island, sea y = 0, people 15.5.
// rock radius 820 at the sea flaring to 1180 at the rim (y = 180): the bowl of a lamp; rampart on the rim; city cells of 100 climb three peaks: middle (0,-60) to y = 720, left (-560,60) 500, right (580,0) 460.
// front gate at (0,180,1150) facing +z, sea stair from (0,0,1560) up to it.
// Uniforms (lanka.py): night, fire 0..1 (spreads from fireAt), doors 0 open..1 shut, moonDir, skyA skyB skyC for the sea, tLanka layout.
#define TMAX 9000.
#ifndef STEPS
#define STEPS 220
#endif
#define BOUND
#define SEA0 0.
#define AOK 1.6
#include "arch.glsl"
#include "paint.glsl"
uniform sampler2D tLanka;uniform float night,fire,doors;uniform vec3 fireAt,skyA,skyB,skyC;
const float CW=100.;const int NC=24;const float RIM=260.,PK0=640.,PK1=550.,PK2=510.;
vec2 bound(vec3 o,vec3 d){float t0=0.,t1=TMAX;float ty=(1500.-o.y)/d.y,tb=(-1.-o.y)/d.y;if(o.y>1500.){if(d.y>=0.) return vec2(1,0);t0=max(t0,ty);}else if(d.y>0.) t1=min(t1,ty);if(d.y<0.) t1=min(t1,tb+2.);
 vec2 dd=d.xz;float a=dot(dd,dd),b=dot(o.xz,dd),c=dot(o.xz,o.xz)-1600.*1600.;float h=b*b-a*c;bool sea=d.y<0.;if(!sea){if(h<0.) return vec2(1,0);h=sqrt(h);t0=max(t0,(-b-h)/a);t1=min(t1,(-b+h)/a);}return vec2(t0,t1);}
float burnAt(vec3 p){if(fire<=0.) return 0.;float d=length((p-fireAt)*vec3(1,.7,1));return smoothstep(0.,170.,fire*2700.-d-240.*vn(p.xz*.011+3.));}
vec4 tc(ivec2 ij,int k){return ij.x<0||ij.x>=NC||ij.y<0||ij.y>=NC?vec4(0,0,0,0):texelFetch(tLanka,ivec2(ij.x,ij.y*2+k),0);}
// A = (type, hx, H, hz)  B = (dx, dz, top, seed)
vec2 bld(vec3 q,vec4 A,vec4 B){float t=A.x;vec3 h=vec3(A.y,A.z,A.w);vec2 m;
 if(t<1.5){m=aGopura(q,h.x,h.z,h.y,floor(5.+h.y/46.));}
 else if(t<2.5){float H1=floor(h.y*.5/30.+.5)*30.;m=vec2(aBlock(q,vec3(h.x,H1,h.z),30.),M_WALL);vec3 r=q-vec3(0,H1,0);if(r.y>-4.){float R=min(h.x,h.z)*.70;m=U(m,vec2(aParapet(r,h.xz+.6,4.,4.4),M_TRIM));m=U(m,vec2(max(aOct(r.xz)-R*1.05,abs(r.y-R*.22)-R*.22),M_WALL));m=U(m,aDome(r-vec3(0,R*.40,0),R));m=U(m,aChhatri(vec3(abs(r.x)-h.x+6.5,r.y,abs(r.z)-h.z+6.5),6.));}}
 else if(t<3.5){m=aShikhara(q,h.x*.62,h.y);m=U(m,vec2(aBlock(q,vec3(h.x,10.,h.z),10.),M_STEP));vec3 c=vec3(abs(q.x)-h.x*.8,q.y-10.,abs(q.z)-h.z*.8);m=U(m,aShikhara(c,h.x*.15,h.y*.34));}
 else{float H1=h.y;m=vec2(aBlock(q,vec3(h.x,H1,h.z),30.),M_WALL);m=U(m,vec2(aBlock(q,vec3(h.x*.6,H1+30.,h.z*.6),30.),M_WALL));m=U(m,vec2(aParapet(q-vec3(0,H1,0),h.xz+.6,4.,4.4),M_TRIM));m=U(m,aChhatri(q-vec3(0,H1+30.,0),min(h.x,h.z)*.52));m=U(m,aChhatri(vec3(abs(q.x)-h.x+7.,q.y-H1,abs(q.z)-h.z+7.),6.4));}
 return m;}
float nbr(ivec2 ij,vec3 p){vec4 B=tc(ij,1);if(B.z<1.) return 50.;vec4 A=tc(ij,0);vec2 c=(vec2(ij)-float(NC/2)+.5)*CW;float d=sBox(vec3(p.x-c.x,p.y-(B.z+RIM-5.)*.5,p.z-c.y),vec3(CW*.5,(B.z-RIM+5.)*.5,CW*.5),0.);if(A.x>.5){vec3 q=vec3(abs(p.x-c.x-B.x)-A.y-3.4,p.y-B.z-A.z*1.12-34.,abs(p.z-c.y-B.y)-A.w-3.4);float e=max(length(max(q,0.)),1.2);d=min(d,e);}return d;}
vec2 city(vec3 p){vec2 k=floor(p.xz/CW);ivec2 ij=ivec2(k)+NC/2;vec2 f=p.xz-(k+.5)*CW;vec4 A=tc(ij,0),B=tc(ij,1);vec2 m=vec2(50.,0.);
 if(B.z>1.) m=U(m,vec2(max(p.y-B.z,RIM-5.-p.y),M_GROUND));
 ivec2 d=ivec2(f.x>0.?1:-1,f.y>0.?1:-1);ivec2 n1=ij+ivec2(d.x,0),n2=ij+ivec2(0,d.y),n3=ij+d;
 float a=tc(n1,1).z,b=tc(n2,1).z;m=U(m,vec2(nbr(n1,p),0.));m=U(m,vec2(nbr(n2,p),0.));m=U(m,vec2(nbr(n3,p),0.));
 // walls of the higher neighbours are real surfaces
 if(a>B.z) m=U(m,vec2(max(CW*.5-abs(f.x),max(p.y-a,RIM-5.-p.y)),M_STEP));if(b>B.z) m=U(m,vec2(max(CW*.5-abs(f.y),max(p.y-b,RIM-5.-p.y)),M_STEP));
 if(A.x>.5){vec3 q=p-vec3((k.x+.5)*CW+B.x,B.z,(k.y+.5)*CW+B.y);float bb=sBox(q-vec3(0,A.z*.56+17.,0),vec3(A.y+3.4,A.z*.56+17.,A.w+3.4),0.);
  if(bb>7.) m=U(m,vec2(bb+1.,0.));else{float bu=burnAt(p);if(bu>0.){q.xz+=bu*vec2(sin(q.y*.07+B.w*9.),cos(q.y*.06+B.w*7.))*2.2*smoothstep(0.,60.,q.y);q.y*=1.+.10*bu*smoothstep(20.,140.,q.y);}vec2 b2=bld(q,A,B);m=U(m,vec2(b2.x*(1.-.12*bu),b2.y));}}
 return m;}
float rimR(float a){return 1180.+26.*sin(a*5.+1.)+18.*sin(a*9.);}
vec2 rock(vec3 p){float l=length(p.xz),a=atan(p.x,p.z);float yk=clamp(p.y/RIM,0.,1.);float R=mix(930.,rimR(a),pow(yk,.8));float d=(l-R)*.74;d=max(d,p.y-RIM);if(d<110.&&p.y<RIM+2.){float u=a*1100./58.;vec4 v=voro(vec2(u,p.y/210.+.35*sin(u*.7)));vec4 v2=voro(vec2(u*2.7+4.,p.y/70.));float w=v.x*84.+v2.x*24.-20.+14.*abs(fract(p.y/44.+.4*v.z)-.5);float k=smoothstep(RIM,RIM-30.,p.y);d=max((d+(w-18.)*k)*.62,p.y-RIM);}return vec2(d,M_ROCK);}
vec2 skerry(vec3 p){float l=length(p.xz);if(p.y>95.||l<860.||l>1250.) return vec2(max(p.y-60.,max(l-1200.,max(900.-l,6.))),0.);float a=atan(p.x,p.z);float s=TAU/34.;float id=floor(a/s);float aa=a-(id+.5)*s;vec2 h=h22(vec2(id,3.));vec3 q=vec3(aa*l-(h.x-.5)*70.,p.y,l-960.-120.*h.y);float H=26.+70.*h.x*h.x;float k=clamp(q.y/H,0.,1.);float r=(22.+26.*h.y)*(1.-k*.85);float d=max(aOct(rot(h.x*6.)*q.xz+vec2(q.y*.15,0.))-r,q.y-H)*.7;if(p.z>0.&&abs(p.x)<140.) d=40.;return U(vec2(d-2.,M_ROCK),vec2(max(abs(s*l*.5-abs(aa*l)),3.)+3.,0.));}
vec2 rampart(vec3 p){float l=length(p.xz);float a=atan(p.x,p.z);float R=rimR(a)-24.;float b=abs(l-R)-40.;if(p.y<RIM-30.||p.y>RIM+170.||b>40.) return vec2(max(max(b,RIM-30.-p.y),p.y-RIM-170.)+6.,0.);
 float n=44.,s=TAU/n;float id=floor(a/s+.5);float aa=a-id*s;vec3 q=vec3(sin(aa)*l,p.y-RIM+6.,cos(aa)*l-R);float w=aRampart(vec3(aa*R,q.y,l-R),1e4,62.,8.,9.);float tw=aTower(vec3(q.x,q.y,q.z),25.,94.,9.);if(p.z>0.&&abs(p.x)<140.){tw=1e4;w=max(w,92.-abs(p.x));}vec2 m=vec2(min(w,tw),M_COL);
 if(mod(id,2.)<.5&&tw<1e3) m=U(m,aDome(vec3(q.x,q.y-94.,q.z),19.));return m;}
// the great gate
const vec3 GP=vec3(0.,RIM,1140.);
vec2 gate(vec3 p){vec3 q=p-GP;float bb=sBox(q-vec3(0,150,10),vec3(190,170,90),0.);if(bb>14.) return vec2(bb,0.);vec3 a=vec3(abs(q.x),q.yz);
 float op=oArch(q.xy,42.,78.,5.);float b=sBox(q-vec3(0,74,0),vec3(96,74,46),.3);b=max(b,-max(op,q.z*0.-60.-0.));
 float inner=max(op,-(q.z+34.));b=sBox(q-vec3(0,74,0),vec3(96,74,46),.3);b=max(b,-max(op,-34.-q.z));
 float rec=oArch(q.xy,54.,82.,5.);b=max(b,-max(rec,40.-q.z));
 vec2 m=vec2(b,M_COL);m=U(m,aGopura(q-vec3(0,146,0),92.,40.,190.,7.));
 m=U(m,vec2(aTower(a-vec3(128,-4,6),40.,178.,11.),M_COL));m=U(m,aDome(a-vec3(128,174,6),32.));
 float ca=min(sBox(q-vec3(0,146,0),vec3(101,4.,51),.3),sBox(q-vec3(0,139,0),vec3(98,2.,48),.3));m=U(m,vec2(ca,M_GOLD));
 // doors
 if(doors>.01){float x=abs(q.x)-42.*(1.-doors);float dr=max(abs(q.z-28.)-2.5,max(op+.5,-x));vec2 g=vec2(abs(q.x),q.y);vec2 c=g-vec2(7.5,9.)-15.*round((g-vec2(7.5,9.))/15.);float bo=length(vec3(c,q.z-30.5))-2.2;bo=max(bo,max(op+4.,-x));m=U(m,U(vec2(dr,M_DARK),vec2(bo,M_GOLD)));}
 // guardian lamps
 m=U(m,aDeepa(a-vec3(74,0,64),52.,7.));return m;}
vec2 stair(vec3 p){vec3 q=p-vec3(0,0,1180.);float bb=sBox(q-vec3(0,135,180),vec3(96,150,210),0.);if(bb>12.) return vec2(bb,0.);float d=max(aStairs(vec2(q.z-378.,q.y),6.,8.72),abs(q.x)-60.);d=max(d,max(q.y-RIM,-q.z-70.));float sl=q.y-RIM*clamp((378.-q.z)/378.,0.,1.);float w=max(max(abs(abs(q.x)-68.)-9.,sl*.85-14.),max(q.z-386.,-q.z-70.));vec3 l=vec3(abs(q.x)-68.,q.y-RIM*clamp((378.-q.z)/378.,0.,1.)-14.,q.z-63.*round((q.z)/63.));l.y=q.y-RIM*clamp((378.-63.*round(q.z/63.))/378.,0.,1.)-12.;float f=max(aFinial(l,16.),max(q.z-380.,-q.z));return U(vec2(min(d,w),M_STEP),vec2(f,M_GOLD));}
// Ravana's palace on the middle peak, smaller crowns on the other two
vec2 crown(vec3 p){vec2 m=vec2(1e4,0.);vec3 q=p-vec3(0,0,-60);float bb=sBox(q-vec3(0,PK0+310.,0),vec3(190,340,190),0.);if(bb<16.){vec3 c=q-vec3(0,PK0,0);vec3 a=vec3(abs(c.x),c.y,abs(c.z));m=vec2(aBlock(c,vec3(165,60,165),30.),M_WALL);m=U(m,vec2(aBlock(c,vec3(120,110,120),36.6),M_WALL));m=U(m,vec2(aParapet(c-vec3(0,60,0),vec2(166),6.,6.),M_TRIM));m=U(m,vec2(aParapet(c-vec3(0,110,0),vec2(121),6.,6.),M_TRIM));m=U(m,aGopura(c-vec3(0,108,0),86.,76.,400.,11.));m=U(m,aGopura(a-vec3(138,58,0),24.,30.,150.,6.));m=U(m,aGopura(vec3(a.z,a.y,a.x)-vec3(138,58,0),24.,30.,150.,6.));m=U(m,aShikhara(a-vec3(134,58,134),22.,170.));m=U(m,aDome(a-vec3(98,112,98),19.));}else m=U(m,vec2(bb,0.));
 vec3 l=p-vec3(-560,PK1,60);bb=sBox(l-vec3(0,150,0),vec3(100,190,100),0.);if(bb<16.){m=U(m,vec2(aBlock(l,vec3(80,40,80),40.),M_WALL));m=U(m,aShikhara(l-vec3(0,38,0),50.,280.));m=U(m,aShikhara(vec3(abs(l.x)-64.,l.y-38.,abs(l.z)-64.),13.,104.));}else m=U(m,vec2(bb,0.));
 vec3 r=p-vec3(580,PK2,0);bb=sBox(r-vec3(0,150,0),vec3(110,190,110),0.);if(bb<16.){m=U(m,vec2(aBlock(r,vec3(90,60,90),30.),M_WALL));m=U(m,vec2(aParapet(r-vec3(0,60,0),vec2(91),5.,5.),M_TRIM));m=U(m,vec2(max(aOct(r.xz)-62.,abs(r.y-74.)-18.),M_WALL));m=U(m,aDome(r-vec3(0,90,0),60.));m=U(m,aChhatri(vec3(abs(r.x)-74.,r.y-60.,abs(r.z)-74.),14.));}else m=U(m,vec2(bb,0.));return m;}
vec2 map(vec3 p){vec2 m=vec2(90.,0.);float l=length(p.xz);if(l>1620.) return U(m,vec2(l-1590.,0.));m=U(m,rock(p));m=U(m,skerry(p));
 m=U(m,rampart(p));if(l<1290.){if(p.y>RIM-60.) m=U(m,city(p));else m=U(m,vec2(max(RIM-p.y,8.),0.));if(p.y>420.) m=U(m,crown(p));else m=U(m,vec2(max(500.-p.y,20.),0.));}else m=U(m,vec2(max(l-1250.,8.),0.));
 if(p.z>900.){m=U(m,gate(p));m=U(m,stair(p));}return m;}
const int cStone=0x4b3340;
void gold(inout Surf s,vec3 tint){s.cls=2.;s.base=tint;s.sh=tint*.5;s.ink=.7;}
void pGop(inout Surf s,vec3 n,vec3 q,float w,float d,float h,float N,float seed){float y0=h*.16,y1=h*.82;float t=clamp((q.y-y0)/(y1-y0),0.,1.);float k=floor(t*N),f=fract(t*N);float st=(y1-y0)/N;
 gold(s,vec3(1.05,.92,.80));if(q.y>y1||n.y>.55){gold(s,vec3(1.1,1.,.9));return;}
 bool zf=abs(n.z)>abs(n.x);float u=zf?q.x:q.z;if(q.y<y0){oAA=gPx;vec3 w_=hex(cStone),sh=hex(0x2a1c30);s.cls=1.;s.base=w_;s.sh=sh;float dd=oArch(vec2(u,q.y),w*.16,h*.07,4.);if(zf&&dd<0.){s.base=hex(0x1a0c10);s.sh=hex(0x100810);s.part+=20.;if(pNight>0.||fire>0.){s.cls=4.;s.base=vec3(1.1,.42,.08)*(.35+.6*exp(-q.y/(h*.06)))*mix(.25,1.,max(pNight*pNight,fire));s.ink=.3;}}else if(abs(dd-1.4)<1.1) gold(s,vec3(1));else{oAA=gPx/5.;float by=(y0-6.-q.y)/5.;if(by>0.&&by<1.&&oLotus(vec2(u/5.,1.-by))>.4) gold(s,vec3(1));}return;}
 if(f>.62){gold(s,vec3(1.15,1.02,.88));return;}
 float per=w*.18;float x=(fract(u/per)-.5)*per;vec2 id=vec2(floor(u/per),k+seed*17.);oAA=gPx;float dd=oArch(vec2(x,(f-.06)*st),per*.22,st*.26,2.);float lod=pLod(per*.4);gold(s,vec3(.80,.56,.42));
 if(dd<0.){float hh=h21(id);if(hh<.45*max(pNight,step(.01,fire))){s.cls=4.;s.base=mix(vec3(.9,.34,.06),vec3(1.5,.75,.2),smoothstep(0.,-per*.2,dd))*(.5+hh);s.ink=.2;}else{s.cls=1.;s.base=hex(0x3a1c1c);s.sh=hex(0x1c0e18);}if(lod<.5&&s.cls<4.) gold(s,vec3(.62,.42,.32));s.part+=20.;}
 else if(abs(dd-.8)<.6) gold(s,vec3(1.2,1.1,.95));}
void wallL(inout Surf s,vec3 n,vec3 q,vec3 h,float fh,float seed){vec3 w=mix(hex(cStone),hex(0x5c3a3c),step(.5,seed)),sh=hex(0x2c1e38),tr=hex(0xd89a38);if(n.y>.6){pPave(s,q.xz,vec2(6.),w*1.15,sh,.5);emit(s,vec3(.5,.22,.06)*.10*pNight);return;}if(n.y<-.5){s.base=w;s.sh=sh;return;}bool zf=abs(n.z)>abs(n.x);float W=zf?h.x:h.z;vec3 tn=zf?vec3(1,0,0):vec3(0,0,1);float out_=zf?abs(q.z)-h.z:abs(q.x)-h.x;if(out_>.45||q.y>h.y){gold(s,vec3(1.05,.98,.9));return;}pFacade(s,n,tn,vec2(zf?q.x:q.z,q.y),W,h.y,fh,17.,w,sh,tr,seed);}
int jK=0;vec3 jQ,jH,jN;vec4 jP;float jS;
void W_(vec3 q,vec3 h,float fh,float seed){jK=1;jQ=q;jH=h;jP=vec4(fh,seed,0,0);}
void G_(vec3 n,vec3 q,float w,float d,float h,float N,float seed){jK=2;jN=n;jQ=q;jP=vec4(w,d,h,N);jS=seed;}
void surfL0(vec3 p,vec3 n,int m,inout Surf s){pNight=night;pLamp=vec3(1.0,.42,.10)*.8;float l=length(p.xz);
 if(m==2||m==3){gold(s,vec3(1.08,1.,.92));if(m==3){float a=atan(n.x,n.z);s.base*=.86+.2*step(.5,fract(a*16./TAU));}return;}
 if(m==6){if(n.y>.8&&p.y>RIM-1.){pPave(s,p.xz,vec2(12.),hex(0x5c4448),hex(0x30223a),.5);s.ink=.3;return;}vec3 c=mix(hex(0x46384a),hex(0x8a7078),smoothstep(-.1,.8,n.y+.6*(fbm(vec2(p.x+p.z,p.y)*.03)-.5)));float sl=fbm(vec2(atan(p.x,p.z)*60.,p.y*.05));c*=.75+.5*sl;s.base=c;s.sh=hex(0x2c2640)*(.7+.5*sl);float wet=smoothstep(26.,4.,p.y);s.base*=1.-.5*wet;s.ink=.3;if(p.y<3.5+2.5*vn(p.xz*.06+fT)) {s.base=mix(s.base,hex(0xc8d4ee),.55);s.sh=mix(s.sh,hex(0x7080b0),.55);}emit(s,vec3(.55,.20,.05)*.07*pNight*smoothstep(90.,RIM,p.y));return;}
 if(m==13){vec3 w=hex(0x4f3642),sh=hex(0x2a1d34);float a=atan(p.x,p.z);vec2 u=vec2(a*1160.,p.y-RIM);if(n.y>.5){s.base=w*1.1;s.sh=sh;return;}pPave(s,u,vec2(13.,7.),w,sh,.6);oAA=gPx/8.;float by=(u.y-40.)/8.;if(by>0.&&by<1.&&oLotus(vec2(u.x/8.,by))>.45) gold(s,vec3(1));if(abs(u.y-38.)<1.||abs(u.y-50.)<1.||u.y>57.) gold(s,vec3(1.02,.95,.85));
  vec3 q=p-GP;if(abs(q.x)<100.&&abs(q.z)<60.){s.cls=1.;pPave(s,q.xy,vec2(16.,9.),w*1.05,sh,.6);oAA=gPx;float d=oArch(q.xy,42.,78.,5.),d2=oArch(q.xy,54.,82.,5.);if(abs(n.z)>.5){if(abs(d2-4.)<3.) gold(s,vec3(1.1));if(d2>9.&&d2<11.) gold(s,vec3(.9));oAA=gPx/8.;if(d2>13.&&q.y<128.&&abs(q.x)<92.&&oDiaper(q.xy/14.)>.5) gold(s,vec3(.95,.85,.7));float by2=(q.y-128.)/9.;if(by2>0.&&by2<1.){s.base=hex(0x5a1418);s.sh=hex(0x2c0a1c);if(oVine(vec2(q.x/10.,by2))>.5) gold(s,vec3(1.1));}float M=length(vec2(abs(q.x)-70.,q.y-112.));if(M<15.){oAA=gPx/14.;float c=oSun(vec2(abs(q.x)-70.,q.y-112.)/14.);gold(s,c>.5?vec3(1.15):vec3(.5,.3,.25));}}
   if(d<.6&&q.z<38.){s.cls=1.;s.base=hex(0x170d16);s.sh=hex(0x0a0610);s.ink=.3;return;}}
  else if(length(vec2(abs(q.x)-128.,q.z-6.))<50.&&q.y<185.){float a2=atan(abs(q.x)-128.,q.z-6.);s.cls=1.;pPave(s,vec2(a2*40.,q.y),vec2(14.,8.),w,sh,.6);oAA=gPx/10.;for(int i=0;i<2;i++){float yy=(q.y-50.-70.*float(i))/10.;if(yy>0.&&yy<1.&&oLotus(vec2(a2*4.,yy))>.45) gold(s,vec3(1));if(abs(yy*10.+2.)<1.||abs(yy*10.-12.)<1.) gold(s,vec3(1));}if(q.y>165.) gold(s,vec3(1.05));}
  emit(s,pLamp*.10*pNight*exp(-abs(u.y-34.)*.06));return;}
 if(m==12){vec3 q=p-GP;vec2 g=vec2(abs(q.x),q.y);s.base=hex(0x3a1a16);s.sh=hex(0x1c0c14);vec2 c=abs(g-15.*round(g/15.));if(min(c.x,c.y)<1.1) gold(s,vec3(.8,.62,.45));s.ink=.8;return;}
 vec3 gq=p-GP;if(gq.z>-62.&&abs(gq.x)<100.&&gq.y>147.&&l>1000.){G_(n,gq-vec3(0,146,0),92.,40.,190.,7.,.3);return;}
 if(m==4&&p.z>1105.&&abs(p.x)<96.){vec3 c=mix(hex(0x6a4c4a),hex(0x4a3440),step(60.5,abs(p.x)));pPave(s,n.y>.5?p.xz:p.xy,vec2(18.,6.3),c,hex(0x2c2038),.5);if(abs(p.x)<60.5) s.ink=.7*stepInk(8.7,6.);if(abs(p.x)>60.5&&n.y>.4&&abs(abs(p.x)-68.)>6.5) gold(s,vec3(1));emit(s,pLamp*.04*pNight);return;}
 // crowns
 vec3 c=p-vec3(0,PK0,-60);if(abs(c.x)<172.&&abs(c.z)<172.&&c.y>.5){vec3 a=vec3(abs(c.x),c.y,abs(c.z));if(a.x>108.&&a.z>108.&&c.y>59.){gold(s,vec3(1.1,1.,.9));return;}if(c.y>109.5&&m!=8){if(a.x<90.&&a.z<80.){G_(n,c-vec3(0,108,0),86.,76.,400.,11.,.7);return;}}if(c.y>59.5&&(a.x>121.||a.z>121.)&&m!=8){if(a.x>a.z) G_(n,vec3(a.x-138.,c.y-58.,c.z),24.,30.,150.,6.,.2);else G_(vec3(n.z,n.y,n.x),vec3(a.z-138.,c.y-58.,c.x),24.,30.,150.,6.,.2);return;}if(m==8||c.y>110.5){gold(s,vec3(1));return;}W_(c,c.y>60.5?vec3(120,110,120):vec3(165,60,165),c.y>60.5?36.6:30.,.3);return;}
 vec3 L=p-vec3(-560,PK1,60);if(abs(L.x)<100.&&abs(L.z)<100.&&L.y>.5){if(L.y>40.5) gold(s,vec3(1.08,.96,.84));else W_(L,vec3(80,40,80),40.,.6);if(L.y>40.5&&n.y<.5){float k=fract(L.y*.12);if(k<.3) s.base*=.72;}return;}
 vec3 R=p-vec3(580,PK2,0);if(abs(R.x)<110.&&abs(R.z)<110.&&R.y>.5){if(m==8||R.y>60.5) gold(s,vec3(1.05,.95,.85));else W_(R,vec3(90,60,90),30.,.4);return;}
 vec2 k=floor(p.xz/CW);ivec2 ij=ivec2(k)+NC/2;vec4 A=tc(ij,0),B=tc(ij,1);vec3 q=p-vec3((k.x+.5)*CW+B.x,B.z,(k.y+.5)*CW+B.y);float seed=B.w;vec3 h=vec3(A.y,A.z,A.w);
 if(m==10||m==4&&!(A.x>2.5&&A.x<3.5&&q.y>.2)){if(n.y>.5){pPave(s,p.xz,vec2(10.),hex(0x6a4e4a),hex(0x33243c),.5);s.ink=.3;emit(s,vec3(.6,.25,.06)*.22*pNight);return;}
  vec3 w=hex(0x56393e),sh=hex(0x2c1e36);float u=abs(n.x)>.5?p.z:p.x;float yb=mod(p.y,36.);pPave(s,vec2(u,p.y),vec2(12.,6.),w,sh,.6);if(yb>32.5) gold(s,vec3(1));else{float x=(fract(u/20.)-.5)*20.;oAA=gPx;float d=oArch(vec2(x,yb-4.),5.5,11.,3.);if(abs(d-1.)<.7) gold(s,vec3(.95,.85,.7));else if(d<0.){float hh=h21(vec2(floor(u/20.),floor(p.y/36.)+seed));s.part+=20.;s.base=hex(0x22121a);s.sh=hex(0x140a14);if(hh<.45*max(pNight,step(.01,fire))){s.cls=4.;s.base=vec3(1.2,.5,.10)*(.4+hh)*(.4+.8*exp(-(yb-4.)*.14));s.ink=.2;}}}
  if(s.cls<1.5) emit(s,vec3(.8,.32,.07)*(.12+.4*exp(-yb*.14))*pNight);return;}
 if(m==8){gold(s,vec3(1.02,.94,.85));return;}
 if(A.x<1.5){G_(n,q,h.x,h.z,h.y,floor(5.+h.y/46.),seed);return;}
 if(A.x<2.5){float H1=floor(h.y*.5/30.+.5)*30.;if(q.y>H1+.3){gold(s,vec3(.98,.86,.74));if(length(q.xz)<min(h.x,h.z)*.8){float an=atan(q.x,q.z);float f=fract(an*12./TAU)-.5;if(abs(f)<.22&&n.y<.4){s.cls=4.;s.base=vec3(1.2,.5,.1)*max(pNight,.2);}}return;}W_(q,vec3(h.x,H1,h.z),30.,seed);return;}
 if(A.x<3.5){gold(s,vec3(1.04,.9,.78));if(q.y<h.y*.22&&q.y>10.){float u=abs(n.z)>abs(n.x)?q.x:q.z;oAA=gPx;float d=oArch(vec2(u,q.y-12.),h.x*.2,h.y*.07,3.);if(d<0.){s.cls=4.;s.base=vec3(1.1,.45,.1)*(.2+.8*pNight);s.part+=20.;s.ink=.3;}}else{float f=fract(q.y/(h.y*.02)*.5);if(f<.35&&n.y<.6) s.base*=.66;}return;}
 if(q.y>h.y+.4&&(abs(q.x)>h.x*.62||abs(q.z)>h.z*.62||q.y>h.y+30.4)){gold(s,vec3(1,.9,.8));return;}if(q.y>h.y+.2) W_(q,vec3(h.x*.6,h.y+30.,h.z*.6),30.,seed);else W_(q,h,30.,seed);}
void surfL(vec3 p,vec3 n,int m,inout Surf s){jK=0;surfL0(p,n,m,s);if(jK==1) wallL(s,n,jQ,jH,jP.x,jP.y);else if(jK==2) pGop(s,jN,jQ,jP.x,jP.y,jP.z,jP.w,jS);}
void burnPaint(vec3 p,vec3 n,inout Surf s){float b=burnAt(p);if(b<=0.) return;float t=fT;float u=abs(n.x)>abs(n.z)?p.z:p.x;
 // flicker from below, char, molten gold that runs down in threads
 float fl_=fbm(vec2(u*.05,p.y*.035-t*1.6));float rise=smoothstep(.35,.75,fl_);float col=floor(u/5.);float hh=h21(vec2(col,3.));float run=fract(p.y/(70.+60.*hh)+t*(.16+.2*hh)+hh*9.);float th=smoothstep(.36,.14,abs(fract(u/5.)-.5+.12*sin(p.y*.2+hh*6.)))*smoothstep(0.,.10,run)*smoothstep(.75,.35,run)*step(.45,hh)*step(n.y,.7);
 vec3 hot=mix(vec3(.85,.14,.01),vec3(1.5,.62,.10),fl_);if(s.cls>1.5&&s.cls<2.5){s.base*=mix(vec3(1),vec3(1.25,.80,.50),b);if(th*b>.35){s.cls=4.;s.base=mix(vec3(1.5,.5,.06),vec3(2.1,1.5,.5),smoothstep(.4,1.,th));s.ink=.25;s.part+=12.;}else{float gl=smoothstep(.50,.72,fl_)*b;if(gl>.5){s.cls=4.;s.base=hot*.55;s.ink=.3;}}}
 else if(s.cls<1.5){s.base*=1.-.55*b;s.sh*=1.-.45*b;emit(s,hot*b*(.04+.36*rise*rise));}
 else if(s.cls>3.5&&s.cls<4.5){s.base=mix(s.base,vec3(1.7,.72,.12)*(.8+.5*fl_),b);}}
void surf(vec3 p,vec3 n,int m,inout Surf s){
 bool wa=m==5,hit=false;vec3 q=p,nn=n,r=gRd,rd0=gRd,c=vec3(0);int mm=m;vec2 wv=vec2(0);float gp=gPx;
 if(wa){wv=vec2(fbm(p.xz*vec2(.006,.016)+vec2(fT*.06,0))-.5,fbm(p.xz*vec2(.010,.030)+vec2(7.,fT*.10))-.5);float near=pLod(14.);vec2 w2=vec2(vn(p.xz*.06+fT*.4)-.5,vn(p.xz*vec2(.07,.2)-fT*.5)-.5)*near;
  vec3 wn=normalize(vec3(wv.x*.05+w2.x*.05,1.,wv.y*.11+w2.y*.11));r=reflect(gRd,wn);r.y=abs(r.y)+.004;c=mix(skyA,skyB,smoothstep(0.,.45,r.y));float g=max(dot(r,keyDir),0.);vec2 az=normalize(r.xz+1e-5),ka=normalize(keyDir.xz+1e-5);float path=pow(max(dot(az,ka),0.),90.);c+=skyC*(pow(g,120.)*1.2+path*.5*(.3+.7*smoothstep(.45,.7,fbm(p.xz*vec2(.02,.12)+vec2(0,fT*.2)))));
  vec3 o=p+vec3(0,.5,0);float t=2.+gT*.004,tE=0.;vec2 h=vec2(0);float a_=dot(r.xz,r.xz),b_=dot(o.xz,r.xz),c_=dot(o.xz,o.xz)-1500.*1500.,d_=b_*b_-a_*c_;if(d_>0.){d_=sqrt(d_);t=max(t,(-b_-d_)/a_);tE=min((-b_+d_)/a_,(1500.-o.y)/r.y);}
  for(int i=min(0,int(fT));i<(t<tE?56:0);i++){h=map(o+r*t);if(h.x<.0025*t+.02&&h.y>.5){hit=true;break;}t+=h.x;if(t>tE)break;}
  if(hit){q=o+r*t;mm=int(h.y+.5);gPx=max(gPx*2.,1.);float e=.6+.002*t;nn=vec3(0);for(int i=min(0,int(fT));i<3;i++){vec3 k=vec3(i==0,i==1,i==2);nn+=k*(map(q+k*e).x-h.x);}nn=normalize(nn+1e-5);gRd=r;}}
 Surf f=s;f.ns=nn;f.ink=wa?0.:f.ink;
 if(!wa||hit){surfL(q,nn,mm,f);if(mm!=6&&!(mm==4&&q.z>1100.)) burnPaint(q,nn,f);else if(fire>0.&&mm==6) emit(f,vec3(.9,.22,.03)*burnAt(q)*.35*smoothstep(90.,RIM,q.y));}
 gRd=rd0;gPx=gp;if(!wa){s=f;return;}
 if(hit){vec3 lit=f.cls>3.5&&f.cls<4.5?f.base:f.cls>1.5&&f.cls<2.5?hex(0xe0a03c)*f.base*(uKey*.55+uAmb*.6+vec3(.10,.05,.015)+burnAt(q)*vec3(.7,.25,.04)):mix(f.sh*uAmb,f.base*uKey,smoothstep(.44,.50,dot(nn,keyDir)*.5+.5));c=mix(lit,c,.12);}
 float fr=pow(1.-max(0.,-gRd.y),3.);vec3 deep=skyB*.5;c=mix(deep,c,clamp(.35+.65*fr,0.,1.));
 float st=fbm(p.xz*vec2(.010,.05)+vec2(fT*.05,fT*.08));float ln=smoothstep(.04,.015,abs(st-.5))*pLod(24.);c=mix(c,c*.55,ln*.7);float l2=smoothstep(.026,.008,abs(st-.6))*pLod(20.);c+=(skyA*.22+c*.3)*l2*.6;
 oAA=gPx/60.;float ww=oWater(vec2(p.x/60.+wv.x*1.2,p.z/26.+wv.y*2.))*smoothstep(1300.,200.,gT);c=mix(c,c*.6,ww*.6);
 s.cls=6.;s.base=c/max(mix(uAmb,uKey,.55),vec3(.004));s.sh=s.base;s.ink=0.;s.part=1.;s.ns=vec3(0,1,0);}
