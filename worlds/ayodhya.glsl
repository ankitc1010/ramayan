// AYODHYA on the Sarayu.  x right along the bank, river z > 0 (water y = 0), the city climbs toward -z.  People are 15.5 tall.
// ghats z 0..-95 (20 steps, up to y = 48), promenade y = 48 to z = -140, then 8 tiers of 120 each 36 higher, avenue |x| < 34 up the axis, great palace on the top tier (y = 300) at z = -1180.
// Uniforms (see ayodhya.py): night 0..1, fill (how far lamp light floods the stone, .3 from high above), boats[8] (x, z, yaw, size), skyA skyB skyC (what the water mirrors: horizon, above, sun light), tCity (layout texture).
// Cameras: dawn crane (0,70,760)->(0,300,700) looking at (0,170,-900), fov 38; ghats (150,62,-70)->(−300,56,−90); street (6,62,-150)->(0,110,-700); from above (0,1500,700)->(0,100,-600)
#define TMAX 5200.
#ifndef STEPS
#define STEPS 190
#endif
#ifndef SUNSH
#define SUNSH 22
#endif
#define SHMAX 420.
#define BOUND
#define SEA0 0.
#define AOK 1.6
#include "arch.glsl"
#include "paint.glsl"
uniform sampler2D tCity;uniform float night,fill;uniform vec4 boats[8];uniform vec3 skyA,skyB,skyC;
const float CW=120.,CD=120.,Z0=-140.,TIER=36.,GH=48.,TOP=300.;const int NC=44,NR=14;
vec2 bound(vec3 o,vec3 d){float t0=0.,t1=TMAX;float ty=(900.-o.y)/d.y,tb=(-1.-o.y)/d.y;if(o.y>900.){if(d.y>=0.) return vec2(1,0);t0=max(t0,ty);}else if(d.y>0.) t1=min(t1,ty);if(d.y<0.) t1=min(t1,tb+2.);return vec2(t0,t1);}
float tierY(float r){return GH+TIER*clamp(r,0.,7.);}
struct Cell{vec4 A,B;vec3 q;float top,e;};
vec4 tcA(ivec2 ij){return ij.x<0||ij.x>=NC||ij.y<0||ij.y>=NR?vec4(0):texelFetch(tCity,ivec2(ij.x,ij.y*2),0);}
vec4 tcB(ivec2 ij){return ij.x<0||ij.x>=NC||ij.y<0||ij.y>=NR?vec4(0):texelFetch(tCity,ivec2(ij.x,ij.y*2+1),0);}
float rectD(ivec2 ij,vec3 p){vec4 A=tcA(ij);if(A.x<.5) return 60.;vec4 B=tcB(ij);float g=A.x>2.5&&A.x<3.5?7.6:2.2;vec2 c=vec2((float(ij.x)-float(NC/2)+.5)*CW,Z0-(float(ij.y)+.5)*CD)+B.xy;vec3 q=vec3(abs(p.x-c.x)-A.y-g,p.y-tierY(float(ij.y))-A.z*1.35-26.,abs(p.z-c.y)-A.w-g);return max(length(max(q,0.)),1.2);}
Cell cellAt(vec3 p,bool near){Cell c;float r=floor((Z0-p.z)/CD),k=floor(p.x/CW);c.top=tierY(r);vec2 ctr=vec2((k+.5)*CW,Z0-(r+.5)*CD);vec2 f=p.xz-ctr;ivec2 ij=ivec2(int(k)+NC/2,int(r));c.A=tcA(ij);c.B=tcB(ij);
 c.q=p-vec3(ctr.x+c.B.x,c.top,ctr.y+c.B.y);c.e=60.;if(near){ivec2 d=ivec2(f.x>0.?1:-1,f.y>0.?-1:1);c.e=min(60.,min(rectD(ij+ivec2(d.x,0),p),min(rectD(ij+ivec2(0,d.y),p),rectD(ij+d,p))));}
 return c;}
float fhOf(vec4 B){return B.z;}
vec2 chh4(vec3 q,vec2 h,float s){return aChhatri(vec3(abs(q.x)-h.x,q.y,abs(q.z)-h.y),s);}
vec2 bld(vec3 q,vec4 A,vec4 B){float t=A.x;vec3 h=vec3(A.y,A.z,A.w);float fh=B.z;vec2 m;
 if(t<1.5){m=vec2(aBlock(q,h,fh),M_WALL);vec3 r=q-vec3(0,h.y,0);if(r.y>-4.){m=U(m,vec2(aParapet(r,h.xz+.6,4.2,4.2),M_TRIM));m=U(m,chh4(r,h.xz-6.5,6.2));m=U(m,aDome(r-vec3(0,5.,0),min(h.x,h.z)*.42));m=U(m,vec2(max(aOct(r.xz)-min(h.x,h.z)*.48,abs(r.y-3.)-3.),M_WALL));}}
 else if(t<2.5){m=aShikhara(q+vec3(0,0,h.z*.30),h.x*.62,h.y);vec3 r=q-vec3(0,0,h.z*.52);float y=h.y*.26;float b=aBlock(r,vec3(h.x*.46,y,h.z*.42),y);float py=sBox(r-vec3(0,y+2.,0),vec3(h.x*.46,2.,h.z*.42)*(1.-.0*q.y),.1);float k=clamp((r.y-y)/(h.y*.16),0.,1.);float st=floor(k*4.)/4.;py=max(max(abs(r.x)-h.x*.46*(1.-st*.8),abs(r.z)-h.z*.42*(1.-st*.8)),max(y-r.y,r.y-y-h.y*.16))*.7;m=U(m,vec2(min(b,py),M_WALL));m=U(m,vec2(aFinial(r-vec3(0,y+h.y*.16,0),h.y*.07),M_GOLD));m=U(m,vec2(aBlock(q,vec3(h.x,4.,h.z),4.),M_STEP));float fp=sCyl(q-vec3(0,h.y*1.06,-h.z*.30),.28,h.y*.09,.01);vec3 fq=q-vec3(0,h.y*1.11,-h.z*.30);float wv=.8*sin(fq.x*.35-fT*4.+B.w*9.)*clamp(fq.x*.2,0.,1.);float fl2=max(abs(fq.z-wv)-.12,max(abs(fq.y)-2.6*(1.-fq.x/16.),max(-fq.x,fq.x-16.)))*.6;m=U(m,vec2(fp,M_GOLD));m=U(m,vec2(fl2,M_CLOTH));}
 else if(t<3.5){float H1=floor(h.y*.62/fh+.5)*fh;vec3 a=q-vec3(0,0,h.z*.36);m=vec2(aBlock(a,vec3(h.x,H1,h.z*.64),fh),M_WALL);vec3 b=q+vec3(h.x*.22*sign(B.w-.5),0,h.z*.45);m=U(m,vec2(aBlock(b,vec3(h.x*.72,h.y,h.z*.52),fh),M_WALL));m=U(m,vec2(aParapet(a-vec3(0,H1,0),vec2(h.x,h.z*.64)+.6,3.4,3.6),M_TRIM));m=U(m,vec2(aParapet(b-vec3(0,h.y,0),vec2(h.x*.72,h.z*.52)+.6,3.4,3.6),M_TRIM));m=U(m,aChhatri(b-vec3(0,h.y,0),8.));vec3 c=a-vec3(0,0,h.z*.64);c.x=abs(c.x)-h.x*.5;m=U(m,aJharokha(c-vec3(0,fh*1.18,0),fh*.26));m=U(m,aChhatri(vec3(abs(a.x)-h.x+6.,a.y-H1,a.z-h.z*.64+6.),4.8));}
 else if(t<4.5){float H1=h.y*.46;m=vec2(aBlock(q,vec3(h.x,H1,h.z),fh),M_WALL);vec3 r=q-vec3(0,H1,0);if(r.y>-4.){m=U(m,vec2(aParapet(r,h.xz+.6,4.2,4.2),M_TRIM));float R=min(h.x,h.z)*.66;m=U(m,vec2(max(aOct(r.xz)-R*1.06,abs(r.y-R*.24)-R*.24),M_WALL));m=U(m,aDome(r-vec3(0,R*.42,0),R));m=U(m,chh4(r,h.xz-7.5,7.));}}
 else if(t<5.5){m=vec2(aBlock(q,vec3(h.x,h.y,h.x),fh),M_WALL);m=U(m,aChhatri(q-vec3(0,h.y,0),h.x*.95));m=U(m,vec2(aBlock(q,vec3(h.x*1.7,fh,h.x*1.7),fh),M_WALL));}
 else {m=vec2(aBlock(q,vec3(h.x,5.,h.z),5.),M_STEP);m=U(m,aChhatri(q-vec3(0,5.,0),h.y*.22));}
 return m;}
vec2 city(vec3 p){if(p.z>Z0+14.) return vec2(max(p.z-Z0-8.,1.),0.);Cell c=cellAt(p,true);vec2 m=vec2(c.e,0.);float over=p.y-TOP-250.;
 if(c.A.x>.5){float Hb=c.B.w>=0.?c.A.z*1.35+26.:0.;float bb=sBox(c.q-vec3(0,Hb*.5,0),vec3(c.A.y+3.2,Hb*.5,c.A.w+3.2),0.);vec2 b=bb>7.?vec2(bb+1.,0.):bld(c.q,c.A,c.B);m=U(m,b);}
 m.x=max(m.x,over);return m;}
// the great palace on the hill
const vec3 PAL=vec3(0.,TOP,-1190.);const float PS=1.5;
vec2 palace(vec3 p){vec3 q=p-PAL;float bb=sBox(q-vec3(0,320,0),vec3(540,345,190),0.);if(bb>20.) return vec2(bb,0.);q/=PS;vec3 a=vec3(abs(q.x),q.yz);
 vec2 m=vec2(aBlock(q,vec3(250,74,84),37.),M_WALL);m=U(m,vec2(aBlock(q,vec3(168,148,66),37.),M_WALL));m=U(m,vec2(aBlock(q,vec3(92,222,52),37.),M_WALL));m=U(m,vec2(sBox(q-vec3(0,6,0),vec3(345,6,118),.3),M_STEP));
 m=U(m,vec2(aParapet(q-vec3(0,74,0),vec2(251,85),6.,6.),M_TRIM));m=U(m,vec2(aParapet(q-vec3(0,148,0),vec2(169,67),6.,6.),M_TRIM));m=U(m,vec2(aParapet(q-vec3(0,222,0),vec2(93,53),6.,6.),M_TRIM));
 m=U(m,vec2(max(aOct(q.xz)-56.,abs(q.y-234.)-16.),M_WALL));m=U(m,vec2(aDome(q-vec3(0,248,0),56.).x,M_GOLD));
 m=U(m,aDome(a-vec3(130,156,0),34.));m=U(m,vec2(max(aOct(a.xz-vec2(130,0))-36.,abs(a.y-154.)-10.),M_WALL));m=U(m,aChhatri(vec3(abs(a.x-209.)-32.,a.y-74.,abs(a.z)-72.),13.));m=U(m,aChhatri(vec3(a.x-158.,a.y-148.,abs(a.z)-56.),13.));m=U(m,aChhatri(vec3(a.x-80.,a.y-222.,abs(a.z)-40.),13.));
 m=U(m,aShikhara(a-vec3(306,0,0),34.,262.));m=U(m,aShikhara(a-vec3(222,74,0),18.,110.));m.x*=PS;return m;}
vec2 paras(vec3 p){if(p.z>6.||p.z<-92.||p.y>34.+max(0.,-p.z)*.5) return vec2(max(p.y-34.+min(0.,p.z*.5),3.),0.);vec2 c=vec2(46.,30.);vec2 id=floor(p.xz/c);vec2 f=p.xz-(id+.5)*c;vec2 e=c*.5-abs(f);float bd=min(e.x,e.y)+3.;vec2 h=h22(id+5.);float xb=id.x*46.+23.;xb-=300.*round(xb/300.);if(h.x<.60||abs(p.x)<70.||abs(xb)<48.&&id.y<-.5) return vec2(bd,0.);vec2 ctr=(id+.5)*c+(h22(id+9.)-.5)*vec2(18.,8.);float g=clamp((floor(-ctr.y/4.75)+1.)*2.4,0.,48.);vec3 q=vec3(p.x-ctr.x,p.y-g,p.z-ctr.y);float R=8.+4.*h.y,H=12.+4.*h.y;float l=length(q.xz);float y=q.y-H+l*l*.035+.25*abs(sin(atan(q.x,q.z)*6.))*smoothstep(R*.6,R,l);float d=max(abs(y)-.22,l-R)*.75;float p_=sCyl(q-vec3(0,H*.5,0),.28,H*.5+1.2,.02);return U(U(vec2(d,M_CLOTH),vec2(p_,M_WOOD)),vec2(bd,0.));}
vec2 ghat(vec3 p){vec2 s=vec2(p.z,p.y);float d;if(p.z>-90.||p.y<GH+3.) d=aStairs(s,2.4,4.75);else d=p.y-GH;d=max(d,p.y-GH);vec2 m=vec2(d,M_STEP);
 // central landing and side bastions with pavilions
 float xr=p.x-300.*round(p.x/300.);vec3 q=vec3(xr,p.y,p.z+58.);if(abs(p.x)>150.){float b=max(aOct(q.xz)-19.,p.y-GH-.5);b=min(b,max(aOct(q.xz)-20.5,abs(p.y-GH+1.5)-1.));m=U(m,vec2(b,M_WALL));m=U(m,aChhatri(q-vec3(0,GH,0),12.));}
 float xs=p.x-150.-300.*round((p.x-150.)/300.);if(abs(p.x)>100.) m=U(m,aShikhara(vec3(xs,p.y-12.,p.z+26.),5.2,44.));
 // lamp pillars on either side of the axis
 vec3 l=vec3(abs(p.x)-46.,p.y-GH,p.z+104.);m=U(m,aDeepa(l,44.,5.5));
 m=U(m,paras(p));float ba=max(aBaluster(vec3(p.x,p.y-GH,p.z+97.),4000.,4.2,2.6),52.-abs(p.x));m=U(m,vec2(ba,M_TRIM));return m;}
vec2 terr(vec3 p){float d=aStairs(vec2(p.z-Z0-CD*0.,p.y-GH+TIER*1.),TIER,CD);float r=floor((Z0-p.z)/CD);d=p.z>Z0?max(p.y-GH,0.)+0.:d;if(p.z>Z0){float a=p.y-GH;float b=p.z-(Z0-CD);d=p.y<GH+TIER?min(max(a,0.),b):max(a,0.);}d=max(d,p.y-TOP);vec2 m=vec2(d,M_GROUND);
 // stairs of the avenue
 if(abs(p.x)<42.&&p.z<Z0&&r<7.){float zb=Z0-(r+1.)*CD;float top=tierY(r);vec2 s=vec2(p.z-zb-64.8,p.y-top);float st=max(aStairs(s,2.,3.6),abs(p.x)-30.);st=max(st,p.y-top-TIER);float wing=max(max(abs(abs(p.x)-32.5)-2.5,abs(p.z-zb-32.)-34.),p.y-top-TIER*clamp((zb+68.-p.z)/68.,.12,1.)-3.);m=U(m,U(vec2(st,M_STEP),vec2(wing*.8,M_WALL)));}
 return m;}
vec2 gate(vec3 p){vec3 q=p-vec3(0,GH,-132.);float bb=sBox(q-vec3(0,40,0),vec3(60,48,16),0.);if(bb>10.) return vec2(bb,0.);vec3 a=vec3(abs(q.x),q.yz);float op=oArch(q.xy,24.,30.,4.);float b=sBox(q-vec3(0,33,0),vec3(44,33,9),.2);b=max(b,-max(op,abs(q.z)-12.));b=min(b,sBox(q-vec3(0,67,0),vec3(47,1.4,12),.2));b=min(b,sBox(q-vec3(0,64,0),vec3(45.5,1.,10.5),.2));vec2 m=vec2(b,M_WALL);m=U(m,vec2(aBlock(a-vec3(44,0,0),vec3(9,78,12),26.),M_WALL));m=U(m,vec2(aParapet(q-vec3(0,68,0),vec2(37,10),4.,4.),M_TRIM));m=U(m,aChhatri(a-vec3(44,78,0),9.));m=U(m,aChhatri(vec3(abs(q.x)-15.,q.y-68.,q.z),7.));m=U(m,aChhatri(q-vec3(0,68,0),10.));return m;}
vec2 boat(vec3 p){vec2 m=vec2(1e4,0.);for(int i=0;i<8;i++){vec4 b=boats[i];if(b.w<.1) continue;vec3 q=p-vec3(b.x,.25*sin(fT*1.3+b.x),b.y);float bb=length(q-vec3(0,6,0)*b.w)-34.*b.w;if(bb>6.){m=U(m,vec2(bb,0.));continue;}q.xz=rot(b.z)*q.xz;q/=b.w;float k=abs(q.x)/24.;float up=k*k*9.+k*k*k*k*5.;float w=5.2*(1.-k*k*.92);float y=q.y-up;float hull=max(length(vec2(q.z*.95,(y-1.8)*1.0))-w-.2,y-2.0);hull=max(hull,-max(length(vec2(q.z,y-2.2))-w+.8,-1.6-y*0.));hull=max(hull,abs(q.x)-26.);
  float cab=sBox(q-vec3(-2,6.,0),vec3(7.5,.35,3.8),.1);cab=max(abs(q.y-6.8+.10*q.z*q.z)-.35,max(abs(q.x+2.)-8.6,abs(q.z)-4.6))*.8;float po=sCyl(vec3(abs(q.x+2.)-7.5,q.y-3.8,abs(q.z)-3.6),.28,3.,.02);float mast=sCyl(q-vec3(9,14,0),.3,13.,.02);float bill=3.4*(1.-pow(abs(q.y-15.)/10.5,2.));float sx=q.x-9.-bill*.0;float sail=max(abs(q.z-bill*(1.-pow(abs(q.x-9.)/9.,2.)))-.18,max(abs(q.y-15.)-9.,abs(q.x-9.)-8.5+.16*abs(q.y-7.)))*.55;
  vec2 b2=U(vec2(hull*.7,M_WOOD),vec2(min(cab,9e3),M_CLOTH));b2=U(b2,vec2(min(po,mast),M_WOOD));if(mod(float(i),2.)<.5) b2=U(b2,vec2(sail,M_CLOTH));b2.x*=b.w;m=U(m,b2);}return m;}
vec2 map(vec3 p){vec2 m=vec2(60.,0.);if(p.z<14.){m=U(m,p.z>Z0-2.?ghat(p):terr(p));if(p.z>Z0-30.&&p.z<-95.) m=U(m,terr(vec3(p.x,p.y,min(p.z,Z0-.01))).x<0.?m:m);}else m=U(m,vec2(p.z-9.,0.));
 if(p.z<40.) m=U(m,gate(p));
 m=U(m,city(p));if(p.z<-900.) m=U(m,palace(p));else m=U(m,vec2(max(p.z+990.,8.),0.));
 if(p.z>-12.) m=U(m,boat(p));return m;}
void hueOf(float h,out vec3 w,out vec3 sh,out vec3 tr){if(h<.5){w=hex(0xf8ecd8);sh=hex(0xb295b4);tr=hex(0xd2754e);}else if(h<1.5){w=hex(0xf0c0a4);sh=hex(0xae7a96);tr=hex(0xa8433c);}else if(h<2.5){w=hex(0xf3d8a0);sh=hex(0xb48a86);tr=hex(0xb8642c);}else if(h<3.5){w=hex(0xe29c80);sh=hex(0x9a6280);tr=hex(0x7e2c34);}else{w=hex(0xe6dcea);sh=hex(0x968cbe);tr=hex(0x4a5a9a);}}
void wallOf(inout Surf s,vec3 n,vec3 q,vec3 h,float fh,float bay,float hue,float seed){vec3 w,sh,tr;hueOf(hue,w,sh,tr);if(n.y>.6){pPave(s,q.xz,vec2(5.),mix(w,hex(0xf0dcc0),.4),sh,.4);if(pNight>0.) emit(s,pLamp*w*.10*pNight);return;}if(n.y<-.5){s.base=w*.8;s.sh=sh;if(pNight>0.) emit(s,pLamp*w*.4*pNight);return;}
 bool zf=abs(n.z)>abs(n.x);float W=zf?h.x:h.z;vec3 tn=zf?vec3(1,0,0):vec3(0,0,1);vec2 u=vec2(zf?q.x:q.z,q.y);float out_=zf?abs(q.z)-h.z:abs(q.x)-h.x;if(out_>.45||q.y>h.y){s.base=mix(w,vec3(1),.22);s.sh=sh;oAA=gPx/1.5;s.base=mix(s.base,tr,oBead(vec2(u.x/1.5,fract(q.y/fh+.026)*fh/1.5))*.35*pLod(1.5)*step(q.y,h.y));s.ink=.5;if(pNight>0.) emit(s,pLamp*w*.55*pNight);return;}
 pFacade(s,n,tn,u,W,h.y,fh,bay,w,sh,tr,seed);}
vec3 waterCol(vec3 p,vec3 r){vec3 c=mix(skyA,skyB,smoothstep(0.,.5,r.y));float g=max(dot(normalize(r*vec3(1,1,1)),keyDir),0.);return c+skyC*(pow(g,60.)*1.6+pow(g,9.)*.35);}
// the heavy painters run once, at the end: branches only note what to paint (keeps compile time down)
int jK=0;vec3 jQ,jH,jA,jB,jC;vec4 jP;
void W_(vec3 q,vec3 h,float fh,float bay,float hue,float seed){jK=1;jQ=q;jH=h;jP=vec4(fh,bay,hue,seed);}
void D_(vec3 q,float r,vec3 a,vec3 b,vec3 c,float st){jK=2;jQ=q;jA=a;jB=b;jC=c;jP=vec4(r,st,0,0);}
void S_(vec3 q,float w,float h,vec3 a,vec3 b,vec3 c){jK=3;jQ=q;jA=a;jB=b;jC=c;jP=vec4(w,h,0,0);}
void surfC0(vec3 p,vec3 n,int m,inout Surf s){pNight=night;pLamp*=fill;
 if(m==2){s.cls=2.;s.base=vec3(1.04,1.,.96);s.sh=vec3(.5);s.ink=.7;return;}
 if(m==7){s.base=hex(0x8a4a2c)*(.85+.3*vn(p.xz*vec2(.4,3.)));s.sh=hex(0x4a2430);oAA=gPx;s.base=mix(s.base,hex(0xe8b04a),oL(p.y-2.6,.3)*.0);return;}
 if(m==9&&p.z<0.&&p.z>-95.){vec2 c=vec2(46.,30.);vec2 id=floor(p.xz/c);vec2 ctr=(id+.5)*c+(h22(id+9.)-.5)*vec2(18.,8.);vec2 q=p.xz-ctr;float a=atan(q.x,q.y);float k=step(.5,fract(a*6./TAU));float hh=h21(id+2.);vec3 A_=hh<.4?hex(0xd23c26):hh<.7?hex(0xe88a24):hex(0x2c6a78);s.base=mix(A_,hex(0xfbeed2),k);s.sh=mix(A_*.45,hex(0xb894a8),k);if(n.y<0.){s.base*=.7;}if(night>0.) emit(s,pLamp*s.base*.4*night);return;}
 if(m==9){float k=p.z>-12.?step(.5,fract(p.y*.22)):step(.5,fract(p.x*.1));s.base=mix(hex(0xd8442a),hex(0xf6d488),k);s.sh=mix(hex(0x8a2434),hex(0xb08078),k);if(p.z>-12.){s.base=mix(hex(0xfbeed2),hex(0xdb7a3a),k*.85);s.sh=mix(hex(0xb894a0),hex(0x8a4a50),k);}s.ink=.6;return;}
 if(p.z>Z0+.2&&p.z<18.){ // ghats and promenade
  if(m==4){vec2 q=n.y>.5?p.xz:p.xy;pPave(s,q,n.y>.5?vec2(16.,4.75):vec2(16.,2.4),hex(0xefd6b4),hex(0xa8809a),.5);float wet=smoothstep(9.,1.,p.y+2.*vn(p.xz*.1));s.base=mix(s.base,hex(0xa8755e),wet*.6);float st_=floor(-p.z/4.75-.01);if(n.y<.5){s.base*=.90;if(mod(st_,5.)>3.5){float k=step(.5,fract(p.x/9.));s.base=mix(hex(0xc2482e),hex(0xfaf0da),k);s.sh=mix(hex(0x7c2c44),hex(0xb49ab4),k);}}else if(mod(st_,5.)>3.5) s.base=mix(s.base,hex(0xfaecd2),.6);s.ink=.7*stepInk(4.75,2.4);
   if(night>0.){float row=floor(-p.z/4.75);float u=abs(fract(p.x/7.+.37*row)-.5)*7.;float w2=fract(-p.z/4.75)*4.75-1.2;float g=exp(-u*u*.16-(n.y>.5?w2*w2*.10:(p.y-floor(p.y/2.4)*2.4)*.35));emit(s,pLamp*hex(0xefd6b4)*(.40*g+.012)*night*(.8+.4*h21(vec2(floor(p.x/7.+.37*row),row))));}return;}
  vec3 w,sh,tr;hueOf(0.,w,sh,tr);float xr=p.x-300.*round(p.x/300.);float xs=p.x-150.-300.*round((p.x-150.)/300.);
  if(abs(p.x)>100.&&abs(xs)<9.&&p.z>-40.){S_(vec3(xs,p.y-12.,p.z+26.),5.2,44.,hex(0xf0c0a4),hex(0xa87492),hex(0xa8433c));return;}
  vec3 bq=vec3(xr,p.y,p.z+58.);if(abs(p.x)>150.&&p.z>-92.&&p.z<-30.){if(m==3){D_(bq-vec3(0,GH+26.6,0),10.3,hex(0xf3d8a0),hex(0xb48a86),hex(0xc0502e),0.);return;}if(p.y>GH+.6){s.base=w;s.sh=sh;if(night>0.) emit(s,pLamp*w*.35*night);return;}float a=atan(bq.x,bq.z);s.base=hex(0xf0c0a4);s.sh=hex(0xae7a96);oAA=gPx/5.;float yy=(GH-4.-p.y)/5.;if(yy>0.&&yy<1.)s.base=mix(s.base,tr,oLotus(vec2(a*20./5.,1.-yy))*pLod(4.));pPave(s,vec2(a*19.,p.y),vec2(9.,4.),s.base,s.sh,.35);if(night>0.) emit(s,pLamp*s.base*.5*exp(-(GH-p.y)*.1)*night);return;}
  vec3 gq=p-vec3(0,GH,-132.);if(m==3){if(abs(gq.x)>36.) D_(vec3(abs(gq.x)-44.,gq.y-78.-20.,gq.z),7.7,hex(0xf8ecd8),hex(0xb295b4),hex(0xc0502e),1.);else if(abs(gq.x)>8.5) D_(vec3(abs(gq.x)-15.,gq.y-68.-15.5,gq.z),6.,hex(0xf3d8a0),hex(0xb48a86),hex(0xc0502e),0.);else D_(gq-vec3(0,68.+22.2,0),8.6,hex(0xf8ecd8),hex(0xb295b4),hex(0xc0502e),1.);return;}
  if(m==8){s.base=hex(0xf8e2c4);s.sh=hex(0xb08a9c);s.ink=.6;if(night>0.) emit(s,pLamp*.22*night*w);return;}
  if(n.y>.6&&p.y<GH+.6&&p.z<-95.){pPave(s,p.xz,vec2(9.),hex(0xe6c8a2),hex(0x9a7890),.45);s.ink=.18;if(night>0.) emit(s,pLamp*s.base*.10*night);return;}
  if(abs(gq.x)<56.&&abs(gq.z)<24.&&gq.y<110.){vec3 rw=hex(0xe8a68a),rs=hex(0x9c6684);if(abs(gq.x)>34.7&&gq.y<79.){W_(vec3(abs(gq.x)-44.,gq.yz),vec3(9,78,12),26.,12.,3.,2.);return;}s.base=rw;s.sh=rs;oAA=gPx;float d=oArch(gq.xy,24.,30.,4.);if(abs(n.z)>.6&&gq.y<64.){s.base=mix(s.base,hex(0xf8ecd8),oE(abs(d-2.2)-1.6));s.base=mix(s.base,hex(0x8e2c30),oE(abs(d-2.2)-.5));float L=length(vec2(abs(gq.x)-29.,gq.y-52.));oAA=gPx/5.;s.base=mix(s.base,mix(hex(0x8e2c30),hex(0xf8ecd8),oLotusM(vec2(abs(gq.x)-29.,gq.y-52.)/5.)),oE((L-5.)/5.));oAA=gPx/3.;float by=(gq.y-57.)/3.4;if(by>0.&&by<1.) s.base=mix(hex(0x8e2c30),hex(0xf8dca8),oVine(vec2(gq.x/4.5,by)));if(d>4.6&&gq.y<55.){oAA=gPx/5.;s.base=mix(s.base,hex(0xf2c4a4),.8*oDiaper(gq.xy/5.)*pLod(5.));}}
   if(night>0.) emit(s,pLamp*rw*(.12+.24*exp(-gq.y*.06))*night);return;}
  s.base=w;s.sh=sh;if(night>0.) emit(s,pLamp*w*.2*night);return;}
 if(p.z<-990.&&p.z>-1380.&&abs(p.x)<540.&&p.y>TOP+.5){vec3 q=(p-PAL)/PS;gPx/=PS;vec3 a=vec3(abs(q.x),q.yz);vec3 w,sh,tr;hueOf(0.,w,sh,tr);
  if(m==3){if(a.x<60.&&q.y>240.) {D_(q-vec3(0,248,0),56.,hex(0xfdf0dc),hex(0xb898b8),hex(0xd08a2c),1.);}else if(abs(a.x-130.)<37.&&q.y>150.&&abs(q.z)<37.) D_(a-vec3(130,156,0),34.,hex(0xf6d0b8),hex(0xae7a96),hex(0xb04a3a),0.);else{s.base=hex(0xf3d8a0);s.sh=hex(0xb48a86);}return;}
  if(m==4||m==8){s.base=hex(0xf6e0c4);s.sh=hex(0xb08a9c);if(m==4&&abs(n.y)<.5){oAA=gPx/10.;s.base=mix(s.base,tr,oLotus(vec2(p.x/10.,q.y/12.))*.7);}if(night>0.) emit(s,pLamp*.3*night*s.base);return;}
  if(a.x>258.&&q.y>12.){S_(a-vec3(306,0,0),34.,262.,hex(0xf3d0a8),hex(0xb08494),hex(0xb8542e));return;}
  if(a.x>198.&&a.x<246.&&abs(q.z)<24.&&q.y>75.){S_(a-vec3(222,74,0),18.,110.,hex(0xf8e4c8),hex(0xb08494),hex(0xb8542e));return;}if(q.y>222.5||(a.x>170.&&q.y>75.)||(a.x>94.&&q.y>149.)){s.base=w;s.sh=sh;if(night>0.) emit(s,pLamp*w*.4*night);return;}
  vec3 h=q.y>148.5?vec3(92,222,52):q.y>74.5?vec3(168,148,66):vec3(250,74,84);if(a.x<h.x+2.2&&abs(q.z)<h.z+2.2) W_(q,h,37.,22.,q.y>148.5?0.:q.y>74.5?1.:0.,3.);else{s.base=w;s.sh=sh;}
  return;}
 Cell c=cellAt(p,false);vec4 A=c.A,B=c.B;float seed=abs(B.w);float hue=floor(seed*97.);hue=mod(hue,5.);seed=fract(seed*13.7);vec3 w,sh,tr;hueOf(hue,w,sh,tr);vec3 q=c.q;
 if(m==10){ // ground and terrace walls
  if(n.y>.5&&(p.z<-1820.||abs(p.x)>2640.)){float f_=step(.5,vn(floor(p.xz/90.)));s.base=mix(hex(0x6a8a48),hex(0xb8b060),f_)*.8;s.sh=s.base*vec3(.5,.45,.7);s.base*=1.-.7*night;s.sh*=1.-.6*night;s.ink=.1;s.cls=6.;return;}
  if(n.y>.5){pPave(s,p.xz,vec2(9.,9.),hex(0xe6c8a2),hex(0x9a7890),.45);s.ink=.3;if(abs(p.x)<30.){oAA=gPx/30.;float z=fract(p.z/30.)-.5;s.base=mix(hex(0xf0dab8),hex(0xc8885e),oLotusM(vec2(p.x/13.,z*30./13.))*.6*pLod(14.));s.base=mix(s.base,hex(0xb06048),oL(abs(p.x)-26.,.7));}if(night>0.){float u=exp(-abs(abs(p.x)-30.)*.12);emit(s,pLamp*hex(0xe6c8a2)*(.06+.30*u)*night);}}
  else{float yb=mod(p.y-GH,TIER);pPave(s,p.xy,vec2(8.,4.),hex(0xe8b898),hex(0x986888),.4);oAA=gPx/4.;float by=(yb-TIER+5.)/4.;if(by>0.&&by<1.) s.base=mix(hex(0xb05a44),hex(0xf8e0b8),oLotus(vec2(p.x/4.,by)));float nx=(fract(p.x/20.)-.5)*20.;oAA=gPx;float d=oArch(vec2(nx,yb-2.),5.,6.,3.);s.base=mix(s.base,hex(0xf8dcc0),oE(abs(d-.6)-.5)*pLod(6.));if(d<0.&&by<0.){s.base=mix(s.base,hex(0x5a3048),pLod(8.));s.sh=mix(s.sh,hex(0x3a2038),pLod(8.));if(night>.3){s.base=mix(s.base,pLamp*(.3+.8*exp(-yb*.3)),pLod(6.));s.cls=4.;s.ink=.2;}}if(night>0.&&s.cls<2.) emit(s,pLamp*hex(0xe8b898)*(.10+.5*exp(-(TIER-yb)*.3))*night);}
  return;}
 if(abs(p.x)<36.2&&m==1){pPave(s,abs(n.x)>.5?p.zy:p.xy,vec2(7.,3.),hex(0xf2d2b0),hex(0xa27c94),.4);if(night>0.) emit(s,pLamp*hex(0xf2d2b0)*.35*night);return;}
 vec3 h=vec3(A.y,A.z,A.w);float fh=max(B.z,8.);
 if(m==4){if(abs(p.x)<30.5) s.ink=.7*stepInk(3.6,2.);pPave(s,n.y>.5?q.xz:q.xy,vec2(6.,3.),hex(0xeed4b4),hex(0xa07c94),.4);if(night>0.) emit(s,pLamp*.15*night);return;}
 if(m==8){s.base=mix(w,vec3(1),.15);s.sh=sh;s.ink=.6*pLod(1.6)+.1;if(night>0.) emit(s,pLamp*w*.28*night);return;}
 if(A.x<1.5){if(m==3){vec3 r=q-vec3(0,h.y,0);float R=min(h.x,h.z)*.42;if(length(r.xz)<R*1.15) D_(r-vec3(0,5,0),R,hue==1.||hue==3.?hex(0xf8ecd8):hex(0xf0c8a8),sh,tr,seed*3.);else{s.base=hue<2.?hex(0xf3d8a0):hex(0xf8ecd8);s.sh=sh;}return;}if(q.y>h.y+.2){s.base=w;s.sh=sh;if(night>0.) emit(s,pLamp*w*.35*night);return;}W_(q,h,fh,15.,hue,seed);return;}
 if(A.x<2.5){if(q.z<h.z*.02||q.y>h.y*.45) S_(q+vec3(0,0,h.z*.3),h.x*.62,h.y,mix(w,hex(0xf0c8a0),.4),sh,tr);else{vec3 r=q-vec3(0,0,h.z*.52);W_(r,vec3(h.x*.46,h.y*.26,h.z*.42),h.y*.26,h.x*.3,hue,seed);}return;}
 if(A.x<3.5){if(m==3){s.base=hex(0xf3d8a0);s.sh=sh;return;}float H1=floor(h.y*.62/fh+.5)*fh;vec3 a=q-vec3(0,0,h.z*.36);vec3 b=q+vec3(h.x*.22*sign(B.w-.5),0,h.z*.45);if(a.z<h.z*.64+1.&&a.z>-h.z*.66&&a.y<H1+1.) W_(a,vec3(h.x,H1,h.z*.64),fh,13.,hue,seed);else if(b.z>-h.z*.55&&b.z<h.z*.54&&b.y<h.y+1.&&abs(b.x)<h.x*.74) W_(b,vec3(h.x*.72,h.y,h.z*.52),fh,13.,hue,seed+.3);else{s.base=mix(w,vec3(1),.2);s.sh=sh;if(m==8) s.base=tr;if(night>0.) emit(s,pLamp*w*.5*night);}return;}
 if(A.x<4.5){float H1=h.y*.46;float R=min(h.x,h.z)*.66;vec3 r=q-vec3(0,H1,0);if(m==3){if(length(r.xz)<R*1.1) D_(r-vec3(0,R*.42,0),R,mix(w,vec3(1),.35),sh,tr,floor(seed*3.));else{s.base=w;s.sh=sh;}return;}if(q.y>H1+.2){s.base=w;s.sh=sh;if(length(r.xz)<R*1.2){float an=atan(r.x,r.z);oAA=gPx;float d=oArch(vec2((fract(an*16./TAU)-.5)*R*.39,r.y-R*.05),R*.11,R*.18,3.);s.base=mix(s.base,tr,oE(d));if(night>.3&&d<0.){s.cls=4.;s.base=pLamp;}}if(night>0.&&s.cls<2.) emit(s,pLamp*w*.35*night);return;}W_(q,vec3(h.x,H1,h.z),fh,16.,hue,seed);return;}
 if(A.x<5.5){if(m==3||q.y>h.y+.5){s.base=m==3?hex(0xf3d8a0):w;s.sh=sh;if(night>0.) emit(s,pLamp*w*.3*night);return;}if(abs(q.x)>h.x+1.8||abs(q.z)>h.x+1.8) W_(q,vec3(h.x*1.7,fh,h.x*1.7),fh,12.,hue,seed);else W_(q,vec3(h.x,h.y,h.x),fh,10.,hue,seed);return;}
 s.base=m==3?hex(0xf8ecd8):w;s.sh=sh;if(night>0.) emit(s,pLamp*w*.35*night);}
void surfC(vec3 p,vec3 n,int m,inout Surf s){jK=0;surfC0(p,n,m,s);if(jK==1) wallOf(s,n,jQ,jH,jP.x,jP.y,jP.z,jP.w);else if(jK==2) pDome(s,jQ,jP.x,jA,jB,jC,jP.y);else if(jK==3) pSpire(s,jQ,jP.x,jP.y,jA,jB,jC);}
void surf(vec3 p,vec3 n,int m,inout Surf s){
 bool wa=m==5,hit=false;vec3 q=p,nn=n,r=gRd,rd0=gRd,c=vec3(0);int mm=m;vec2 wv=vec2(0);float gp=gPx,k=smoothstep(900.,60.,gT),tt=0.;
 // the river: mirror with a painter's broken edges, woven lines near
 if(wa){wv=vec2(fbm(p.xz*vec2(.022,.06)+vec2(fT*.10,0))-.5,fbm(p.xz*vec2(.03,.10)+vec2(7.,fT*.16))-.5);float sm=(vn(p.xz*vec2(.16,.55)+vec2(fT*.5,fT*.2))-.5)*pLod(5.);
  vec3 wn=normalize(vec3((wv.x*.05+sm*.02),1.,wv.y*.13+sm*.05));r=reflect(gRd,wn);r.y=abs(r.y)+.004;c=waterCol(p,r);
  vec3 o=p+vec3(0,.3,0);float t=1.+gT*.004;vec2 h=vec2(0);for(int i=min(0,int(fT));i<60;i++){h=map(o+r*t);if(h.x<.0025*t+.02&&h.y>.5){hit=true;break;}t+=h.x;if(t>2600.||(o+r*t).y>900.)break;}
  if(hit){q=o+r*t;tt=t;mm=int(h.y+.5);gPx=max(gPx*2.,.5);float e=.4+.002*t;nn=vec3(0);for(int i=min(0,int(fT));i<3;i++){vec3 x=vec3(i==0,i==1,i==2);nn+=x*(map(q+x*e).x-h.x);}nn=normalize(nn+1e-5);gRd=r;}}
 Surf f=s;f.ns=nn;f.ink=wa?0.:f.ink;if(!wa||hit) surfC(q,nn,mm,f);gRd=rd0;gPx=gp;if(!wa){s=f;return;}
 if(hit){vec3 lit=f.cls>3.5&&f.cls<4.5?f.base:f.cls>1.5&&f.cls<2.5?hex(0xf0b848)*(uKey*.6+uAmb*.6):mix(f.sh*uAmb,f.base*uKey,smoothstep(.44,.50,dot(nn,keyDir)*.5+.5));float fg=1.-exp(-(gT+tt)*.00042);lit=mix(lit,skyA,fg*.8*(1.-night*.6));c=mix(lit,c,.16);}
 float fr=pow(1.-max(0.,-gRd.y),3.);vec3 deep=mix(skyB*.5,hex(0x22a0a4)*(uKey*.30+uAmb*.9),.85)*.62;c=mix(deep,c,clamp(.28+.36*fr,0.,1.));
 float st=fbm(p.xz*vec2(.018,.14)+vec2(fT*.06,fT*.10));float ln=smoothstep(.045,.02,abs(st-.5))*pLod(9.);c=mix(c,c*.72,ln*.6*k);float l2=smoothstep(.03,.01,abs(st-.60))*pLod(9.);c=mix(c,c*1.25+skyA*.12,l2*.7*k);
 oAA=gPx/26.;float ww=oWater(vec2(p.x/26.+wv.x*1.2,p.z/11.+wv.y*2.))*smoothstep(420.,90.,gT);c=mix(c,c*.70,ww*.55);
 if(night>0.){float g=exp(-max(0.,p.z)*.018);c+=pLamp*g*.05*night;}
 // divide out the class-6 light so the painted colour arrives as painted
 s.cls=6.;s.base=c/max(mix(uAmb,uKey,.55),vec3(.004));s.sh=s.base;s.ink=0.;s.part=1.;s.ns=vec3(0,1,0);}
