// HALLS.  #define HALL 0 Mithila assembly (a4) | 1 Ayodhya coronation (b1 b2) | 2 Ravana (d7).   x across, z along the nave, floor y = 0, people 15.5.
// nave |x| < 62, columns every 48 along z at x = +-62 and +-112, ceiling y = 96, side walls x = +-156.
// 0: dais at z -216..-300 (top y 9), sun wall behind; open pillared depth toward +z.   Camera (0,26,120)->(0,34,-240), fov 40
// 1: gate at z = -430 (opening 46 wide each side, 118 high) on the sky; dais with throne at z +110..+180 (top y 9, facing -z); lamp stands at x = +-34 every 48, uniform lamps = how many of the 2*9 are lit, counted from the gate (0..18, fraction = dimming); dusk 0..1 red light through the gate.
// 2: dais at z -216; serpent columns, braziers at x = +-34.   Uniforms: lamps, dusk, lit (0..1 all lamps, halls 0 and 2)
#define TMAX 1500.
#define STEPS 150
#define AOK 1.2
#ifndef HALL
#define HALL 0
#endif
#include "arch.glsl"
#include "paint.glsl"
uniform float lamps,dusk,lit;
const float BZ=48.,CX=62.,CX2=112.,CH=96.,WX=156.,GZ=-430.;
#if HALL==1
const float ZA=GZ,ZB=250.;
#else
const float ZA=-330.,ZB=420.;
#endif
#define PLANES
float planes(vec3 o,vec3 d,out float mat,out vec3 n){float t=1e9;mat=M_GROUND;n=vec3(0,1,0);if(d.y<0.) t=-o.y/d.y;
 float c=d.y>0.?(CH-o.y)/d.y:1e9,w=abs(d.x)>1e-6?(sign(d.x)*WX-o.x)/d.x:1e9;
#if HALL==1
 if(o.z+d.z*c<GZ) c=1e9;if(o.z+d.z*w<GZ) w=1e9;
#endif
 if(c<t&&c>0.){t=c;mat=M_TRIM;n=vec3(0,-1,0);}if(w<t&&w>0.){t=w;mat=M_WALL;n=vec3(-sign(d.x),0,0);}return t>0.?t:1e9;}
float lampLit(float k,float side){ // stands from the gate: k = 0..8, side 0/1
 float id=k*2.+side;
#ifdef LAMPREV
 id=17.-id;
#endif
 return clamp(lamps-id,0.,1.);}
float serp(vec3 p,float h,float r){float l=length(p.xz),a=atan(p.x,p.z);float d=l-r*.72;float pitch=r*3.4;float ph=(a/TAU+p.y/pitch);float f=(fract(ph)-.5)*pitch*.72;float tube=length(vec2(l-r*.95,f))-r*.52;d=min(d,tube*.70);d=max(d,abs(p.y-h*.5)-h*.5);return d;}
vec2 col(vec3 p,float r){
#if HALL==2
 float l=length(p.xz);if(l>r*4.) return vec2(l-r*2.8,M_COL);vec2 m=vec2(serp(p-vec3(0,r*1.2,0),CH-r*4.,r*1.15),M_COL);m=U(m,vec2(max(aOct(p.xz)-r*2.1,p.y-r*1.2),M_DARK));
 // spread hoods
 vec3 q=p-vec3(0,CH-r*3.6,0);q=polar(q,4.,0.);float hd=sEll(q-vec3(0,r*.4,r*1.35),vec3(r*1.25,r*1.9,r*.42));hd=max(hd,-sEll(q-vec3(0,r*.4,r*2.0),vec3(r*.95,r*1.5,r*.42)));float he=sEll(q-vec3(0,r*.9,r*2.0),vec3(r*.34,r*.5,r*.62));m=U(m,vec2(min(hd,he)*.8,M_GOLD));m=U(m,vec2(sBox(p-vec3(0,CH-r*1.1,0),vec3(r*2.,r*1.1,r*2.),.2),M_DARK));return m;
#else
 float l=max(abs(p.x),abs(p.z));if(l>r*4.) return vec2(l-r*2.,M_COL);return vec2(aColumn(p,CH-10.,r),M_COL);
#endif
}
vec2 map(vec3 p){vec2 m=vec2(40.,0.);float ax=abs(p.x);vec3 q=vec3(ax,p.y,p.z);float zr=p.z-BZ*round(p.z/BZ);float zc=clamp(p.z,ZA,ZB);
 if(p.z>ZA-40.||HALL!=1){

 m=U(m,col(vec3(ax-CX,p.y,zr),4.6));m=U(m,col(vec3(ax-CX2,p.y,zr),4.0));
 // arcades along the nave, and beams across
 if(p.y>34.){vec2 u=vec2(abs(zr)-BZ*.5,p.y);float op=oArch(vec2(BZ*.5-abs(zr)-0.,p.y),18.6,50.,4.);op=oArch(vec2(abs(abs(zr)-BZ*.5),p.y),18.6,50.,4.);float sl=max(abs(ax-CX)-2.4,max(46.-p.y,-op));sl=min(sl,max(abs(ax-CX)-3.2,abs(p.y-84.)-1.2));m=U(m,vec2(sl*.9,M_STEP));
  float bm=max(abs(zr)-2.6,max(86.-p.y,ax-WX));float op2=oArch(vec2(ax-87.,p.y),19.,50.,4.);float sb=max(abs(zr)-2.0,max(max(46.-p.y,CX-ax),max(ax-CX2,-op2)));m=U(m,vec2(min(bm,sb*.9),M_STEP));}
 }else m=U(m,vec2(max(ax-400.,40.),0.));
 // hanging lamps and banners
#if HALL==0
 {float zl=p.z-BZ*.5;zl=zl-BZ*round(zl/BZ);vec3 l=vec3(p.x,p.y-64.,zl);float ch=max(length(l.xz)-.22,max(-l.y,l.y-32.));float ds=max(length(vec2(length(l.xz)-3.4,l.y+.6))-1.0,-9.);ds=min(ds,sEll(l-vec3(0,-1.4,0),vec3(3.6,1.5,3.6)));ds=min(ds,aFinial(vec3(l.x,-l.y-2.4,l.z),3.));vec3 c2=vec3(abs(l.x)-2.6,l.y-4.,abs(l.z)-2.6);m=U(m,vec2(min(ds,ch)*.8,M_GOLD));}
 {float wv=.7*sin(p.y*.18+p.z*.2-fT*1.2)*smoothstep(84.,40.,p.y);float b=max(abs(ax-CX+5.4+wv)-.18,max(abs(zr)-4.2,max(38.+1.6*abs(zr)*.6-p.y,p.y-82.)));m=U(m,vec2(b*.7,M_CLOTH));}
#endif
#if HALL!=1
 // dais, throne wall
 {float d=sBox(p-vec3(0,0,-262),vec3(58,9,46),.3);d=min(d,sBox(p-vec3(0,0,-262),vec3(63,6,51),.3));d=min(d,sBox(p-vec3(0,0,-262),vec3(68,3,56),.3));m=U(m,vec2(d,M_STEP));float w=p.z+318.;float ni=oArch(vec2(p.x,p.y-9.),40.,38.,5.);w=min(w,9e3);w=max(p.z-ZA-12.,-max(ni,-p.z+ZA));m=U(m,vec2(w,M_WALL));}
#endif
#if HALL==2
 {float zl=p.z-BZ*.5;zl=zl-BZ*round(zl/BZ);vec3 l=vec3(ax-34.,p.y,zl);float bz=max(length(l.xz)-3.*(.7+.5*smoothstep(0.,12.,l.y)*smoothstep(0.,14.,l.y)),abs(l.y-7.)-7.);bz=min(bz,max(abs(length(l.xz)-4.6)-.5,abs(l.y-13.6)-1.2));if(p.z>-200.&&p.z<200.) m=U(m,vec2(bz*.8,M_GOLD));}
#endif
#if HALL==1
 {// gate wall
  float op=oArch(vec2(p.x,p.y),38.,46.,5.);float w=max(abs(p.z-GZ)-9.,max(-op,p.y-240.));w=max(w,ax-400.);float rec=oArch(vec2(p.x,p.y),46.,46.,5.);w=max(w,-max(rec,GZ+6.-p.z));m=U(m,vec2(w,M_WALL));
  // door leaves thrown open outward
  float dl=max(abs(ax-40.)-1.6,max(abs(p.z-GZ+38.)-30.,p.y-84.));m=U(m,vec2(dl,M_WOOD));
  // lamp stands
  float k=clamp(round((p.z-GZ-46.)/BZ),0.,8.);vec3 l=vec3(ax-34.,p.y,p.z-GZ-46.-k*BZ);m=U(m,vec2(aDeepa(l,34.,4.6).x,M_LAMP));
  // throne end
  float d=sBox(p-vec3(0,0,150),vec3(52,9,38),.3);d=min(d,sBox(p-vec3(0,0,150),vec3(57,6,43),.3));d=min(d,sBox(p-vec3(0,0,150),vec3(62,3,48),.3));m=U(m,vec2(d,M_STEP));float bw=ZB-30.-p.z;float ni=oArch(vec2(p.x,p.y-9.),36.,32.,5.);bw=max(bw,-max(ni,p.z-ZB+8.));bw=max(bw,-400.);m=U(m,vec2(bw,M_WALL));
  vec3 t=vec3(ax,p.y-9.,p.z-168.);float th=sBox(t-vec3(0,3.2,0),vec3(9,.9,7.5),.3);th=min(th,sBox(vec3(t.x-7.4,t.y-1.4,abs(t.z)-5.8),vec3(1.,1.8,1.),.3));float bk=max(abs(t.z-7.4)-.8,-1e3);float bs=oArch(vec2(t.x,t.y-2.),9.4,13.,4.);bk=max(bk,bs);th=min(th,bk);m=U(m,vec2(th,M_GOLD));float cu=sBox(t-vec3(0,4.8,-.4),vec3(8.2,.9,6.6),.8);m=U(m,vec2(cu,M_CLOTH));
  vec2 cp=aChhatri(vec3(t.x,t.y+.6,t.z)/1.0,18.);}
#endif
 return m;}
vec3 fl1,fl2,wa1,wa2,tr1,cl1;
vec3 lampGlow(vec3 p){vec3 g=vec3(0);
#if HALL==1
 for(int s=0;s<2;s++)for(int j=-1;j<=1;j++){float k=round((p.z-GZ-46.)/BZ)+float(j);if(k<0.||k>8.) continue;float L=lampLit(k,float(s));vec3 d=p-vec3(s==0?-34.:34.,27.,GZ+46.+k*BZ);float r=length(d);g+=vec3(1.15,.44,.10)*L/(1.+r*r/200.);}
#elif HALL==0
 for(int j=-1;j<=1;j++){float zl=(round((p.z-BZ*.5)/BZ)+float(j))*BZ+BZ*.5;vec3 d=p-vec3(0,66.,zl);float r=length(d);g+=vec3(.75,.36,.10)*lit/(1.+r*r/700.);}
#else
 for(int s=0;s<2;s++)for(int j=-1;j<=1;j++){float zl=(round((p.z-BZ*.5)/BZ)+float(j))*BZ+BZ*.5;if(abs(zl)>200.) continue;vec3 d=p-vec3(s==0?-34.:34.,20.,zl);float r=length(d);g+=vec3(1.5,.28,.04)*lit*(.85+.15*sin(fT*9.+zl+float(s)*2.))/(1.+r*r/420.);}
#endif
 return g;}
void gold(inout Surf s,vec3 t){s.cls=2.;s.base=t;s.sh=t*.5;s.ink=.75;}
void floorP(vec3 p,inout Surf s){vec2 q=p.xz;s.base=fl1;s.sh=fl2;s.ink=.3;float ax=abs(p.x);
 // nave carpet of medallions
 float per=96.;float z=(fract((q.y+48.)/per)-.5)*per;float r=length(vec2(q.x,z));oAA=gPx/30.;
 if(ax<56.){pPave(s,q,vec2(24.),fl1,fl2,.35);oAA=gPx/30.;float M=oLotusM(vec2(q.x,z)/30.);if(r<30.) {s.base=mix(tr1,wa1,M);s.sh=mix(tr1*.4,wa2,M);}s.base=mix(s.base,cl1,oL((r-33.)/30.,.04));s.base=mix(s.base,cl1,oL((r-36.)/30.,.012));
  vec2 c=vec2(ax-50.,0.);oAA=gPx/9.;float by=(ax-44.)/9.;if(by>0.&&by<1.){float v=oVine(vec2(q.y/9.,by));s.base=mix(cl1,wa1,v);s.sh=mix(cl1*.45,wa2,v);}if(abs(ax-43.)<.6||abs(ax-54.)<.6) s.base=tr1;
  oAA=gPx/14.;vec2 cq=vec2(ax-32.,abs(z)-36.);if(r>38.&&ax<42.){float f=oFlorets(vec2(q.x,z)/14.);s.base=mix(s.base,cl1,f*.6);}
 }else if(ax<WX){pPave(s,q,vec2(18.),fl1*.9,fl2,.4);oAA=gPx/18.;s.base=mix(s.base,cl1,oDiaper(q/36.)*.45);}}
void surf0(vec3 p,vec3 n,int m,inout Surf s){pNight=1.;float ax=abs(p.x);
#if HALL==0
 fl1=hex(0xeed2a4);fl2=hex(0x9a6a5c);wa1=hex(0xf6e2bc);wa2=hex(0xa87a72);tr1=hex(0xa83a2c);cl1=hex(0x2f5a58);
#elif HALL==1
 fl1=hex(0xc87a50);fl2=hex(0x5a2c34);wa1=hex(0xe8b884);wa2=hex(0x7a4450);tr1=hex(0x8a2024);cl1=hex(0x5a1a24);
#else
 fl1=hex(0x2c2026);fl2=hex(0x140c14);wa1=hex(0x3a2a30);wa2=hex(0x180e18);tr1=hex(0x521014);cl1=hex(0x8a5a24);
#endif
 float zr=p.z-BZ*round(p.z/BZ);
 if(m==10){
#if HALL==1
  if(p.z<GZ-10.){pPave(s,p.xz,vec2(26.),hex(0xb06a50),hex(0x5a2c38),.4);return;}
#endif
  floorP(p,s);}
 else if(m==2||m==11){gold(s,vec3(1.05,.98,.9));
#if HALL==1
  if(m==2&&p.z>165.&&n.z<-.5){float bs=oArch(vec2(p.x,p.y-11.),9.4,13.,4.);oAA=gPx/2.2;if(bs<-1.6){s.cls=1.;s.base=mix(hex(0x9a1c22),hex(0xf0b84a),oDiaper(p.xy/3.2)*.8);s.sh=hex(0x4a0c1c);s.part+=20.;}}
#endif
 }
 else if(m==9){float y=p.y;s.base=hex(0xc2341f);s.sh=hex(0x6a1424);
#if HALL==0
  float k=mod(round(p.z/BZ),3.);if(k<.5){s.base=hex(0xe08a1e);s.sh=hex(0x8a4020);}else if(k<1.5){s.base=hex(0x2c6a62);s.sh=hex(0x14363e);}oAA=gPx/3.4;vec2 c=vec2(zr,y-62.)/3.4;float sn=oSun(c);s.base=mix(s.base,hex(0xf8dca0),sn);if(abs(zr)>3.4||y<41.) s.base=mix(s.base,hex(0xf8dca0),.85);oAA=gPx/2.;float b=oBead(vec2(y/2.,(abs(zr)-2.6)/.8));if(abs(zr)>2.6&&abs(zr)<3.4) s.base=mix(s.base,hex(0xf8dca0),b);
#else
  oAA=gPx/2.4;s.base=mix(s.base,hex(0xf0c060),oDiaper(p.xz/2.4)*.8);
#endif
 }
 else if(m==13){float rr=ax<87.?4.6:4.0;vec3 q=vec3(ax-(ax<87.?CX:CX2),p.y,zr);float a=atan(q.x,q.z);
#if HALL==2
  float u=(a/TAU+(p.y-4.6*1.2)/(rr*1.15*3.4));float f=abs(fract(u)-.5);oAA=gPx/1.4;float sc=oScale(vec2(a*rr*1.6,u*9.));s.base=hex(0x241a22);s.sh=hex(0x0e080e);if(f<.30){if(f<.13){gold(s,vec3(.85,.72,.6)*(1.-.35*sc));}else{gold(s,vec3(.66,.50,.40)*(1.-.45*sc));}}
#else
  float yb=CH-10.-p.y;s.base=wa1;s.sh=wa2;if(p.y<rr*1.6||yb<rr*.5){s.base=mix(wa1,tr1,.75);s.sh=mix(wa2,tr1*.35,.75);}else if(yb<rr*3.){gold(s,vec3(1.02,.95,.85));oAA=gPx/3.;}else if(abs(yb-rr*3.3)<rr*.36||abs(p.y-(CH-10.)*.42)<rr*.32||abs(p.y-rr*1.9)<rr*.22) gold(s,vec3(1.));else{oAA=gPx/2.2;if(abs(p.y-(CH-10.)*.42)<rr*1.5){float v=oButa(vec2(a*rr*1.02/1.6,p.y/4.));s.base=mix(s.base,tr1,v);}else if(p.y>(CH-10.)*.46){s.base=mix(s.base,tr1,.55*oE(abs(fract(a*8./TAU+p.y*.05)-.5)*2.-.45)*pLod(1.));}}
#endif
 }
 else if(m==4){ // arches, dais
  if(p.y<9.5&&n.y<.5){oAA=gPx/3.;float by=fract(p.y/3.);s.base=mix(wa1,tr1,oLotus(vec2((abs(n.z)>.5?p.x:p.z)/3.,by))*pLod(2.));s.sh=mix(wa2,tr1*.4,.3);if(by>.9) gold(s,vec3(1));
#if HALL==2
   s.base*=.8;
#endif
  }else if(p.y<9.5){oAA=gPx/12.;s.base=mix(cl1,tr1,.3);s.sh=s.base*.4;float v=oDiaper(p.xz/12.);s.base=mix(s.base,hex(0xe8b860),v*.8);}
  else{bool zf=abs(n.x)>.5;vec2 u=zf?vec2(zr,p.y):vec2(ax-87.,p.y);float op=zf?oArch(vec2(abs(abs(zr)-BZ*.5),p.y),18.6,50.,4.):oArch(vec2(ax-87.,p.y),19.,50.,4.);s.base=wa1;s.sh=wa2;oAA=gPx;if(abs(op-1.5)<1.) gold(s,vec3(1));else if(p.y>82.&&p.y<86.) gold(s,vec3(.95,.88,.78));else if(p.y>86.){oAA=gPx/8.;float v=oVine(vec2((zf?p.z:p.x)/8.,(p.y-86.)/10.));s.base=mix(tr1,wa1,v);s.sh=mix(tr1*.4,wa2,v);}else{vec2 c=zf?vec2(abs(zr),p.y-74.):vec2(abs(ax-87.)-19.,p.y-74.);oAA=gPx/5.;float L=length(c);if(L<5.){float v=oLotusM(c/5.);s.base=mix(tr1,hex(0xf0c878),v);s.sh=s.base*.45;}else{oAA=gPx/6.;s.base=mix(s.base,cl1,oDiaper(u/6.)*.4*pLod(3.));}}}}
 else if(m==8){s.base=mix(tr1,wa1,.25);s.sh=s.base*.45;vec2 q=vec2(p.x,zr);vec2 g=vec2(mod(p.x+12.,24.)-12.,mod(p.z+12.,24.)-12.);oAA=gPx/10.;float L=length(g);s.base=mix(s.base,hex(0xe8b45c),oLotusM(g/10.)*step(L,10.));if(max(abs(g.x),abs(g.y))>11.) gold(s,vec3(.9));s.ink=.4;}
 else if(m==7){vec2 u=vec2(p.z-GZ,p.y);s.base=hex(0x6a2a1e);s.sh=hex(0x2c1018);vec2 c=abs(u-10.*round(u/10.));if(min(c.x,c.y)<.8) gold(s,vec3(.9));else if(length(c-5.)<1.6) gold(s,vec3(1.1));}
 else if(m==12){s.base=wa1;s.sh=wa2;if(abs(n.y)>.5) s.base*=1.2;}
 else{ // walls
  s.base=wa1;s.sh=wa2;
  if(ax>WX-1.){float y=p.y;pPave(s,vec2(p.z,y),vec2(16.,8.),wa1*.85,wa2*.9,.4);float zc2=abs(zr);float op=oArch(vec2(zr,y-16.),15.,34.,4.);oAA=gPx;if(abs(op-1.6)<1.2) gold(s,vec3(1));if(op<0.){oAA=gPx/5.;float j=oJali(vec2(zr,y)/5.);
#if HALL==0
   vec3 sky=mix(vec3(1.15,.66,.26),vec3(.8,.46,.30),smoothstep(16.,70.,y));s.base=mix(sky*lit,wa2*.7,j);if(j<.5){s.cls=4.;s.ink=.15;}
#elif HALL==1
   vec3 sky=mix(vec3(1.2,.30,.10),vec3(.45,.10,.16),smoothstep(16.,70.,y))*dusk;s.base=mix(sky,wa2*.4,j);if(j<.5){s.cls=4.;s.ink=.15;}
#else
   s.base=mix(hex(0x0c060a),hex(0x2a1a20),j);if(j<.5){s.cls=4.;s.base=vec3(.55,.06,.02)*smoothstep(70.,10.,y)*lit;s.ink=.15;}
#endif
   s.part+=20.;}else if(y>74.){oAA=gPx/10.;float by=(y-76.)/10.;if(by>0.&&by<1.){float v=oLotus(vec2(p.z/10.,by));s.base=mix(tr1,wa1,v);s.sh=s.base*.45;}}}
#if HALL==1
  else if(p.z<GZ+60.){float op=oArch(p.xy,38.,46.,5.),r2=oArch(p.xy,46.,46.,5.);oAA=gPx;s.base=mix(wa1,tr1,.2);if(abs(n.z)>.5){if(abs(r2-3.)<2.2) gold(s,vec3(1.1));else if(r2>7.&&r2<15.){oAA=gPx/8.;float v=oLotus(vec2(atan(p.x,p.y-46.)*7.,(r2-7.)/8.));s.base=mix(tr1,hex(0xf0c878),v);s.sh=s.base*.4;}else if(r2>15.){oAA=gPx/16.;float v=oButa(p.xy/16.);s.base=mix(s.base,tr1,v*.7);}else if(op>0.){oAA=gPx/6.;s.base=mix(tr1,wa1,oFlorets(p.xy/6.));}}}
  else if(p.z>ZB-40.){float ni=oArch(vec2(p.x,p.y-9.),36.,32.,5.);oAA=gPx;s.base=mix(tr1,wa1,.15);s.sh=s.base*.4;if(abs(ni-2.)<1.6) gold(s,vec3(1.1));else if(ni<0.){vec2 c=vec2(p.x,p.y-42.);oAA=gPx/29.;float sn=oSun(c/29.);s.base=hex(0x1e2a5a);s.sh=hex(0x101434);if(sn>.5) gold(s,vec3(1.1));else{oAA=gPx/10.;s.base=mix(s.base,hex(0xc89a4a),oFlorets(p.xy/10.)*.8);}}else{oAA=gPx/14.;s.base=mix(s.base,hex(0xe8b860),oDiaper(p.xy/14.)*.22);}}
#else
  else{float ni=oArch(vec2(p.x,p.y-9.),40.,38.,5.);oAA=gPx;if(p.z<ZA+6.){vec2 c=vec2(p.x,p.y-42.);oAA=gPx/30.;
#if HALL==0
   float sn=oSun(c/30.);s.base=hex(0x2f5a66);s.sh=hex(0x1c3648);if(length(c)<30.&&sn>.5) gold(s,vec3(1.15));else{oAA=gPx/10.;s.base=mix(s.base,hex(0xe8c070),oFlorets(p.xy/10.)*.8);}
#else
   s.base=hex(0x1c0a0e);s.sh=hex(0x0c0408);float a=atan(c.x,c.y+14.),l=length(c+vec2(0,14.));float fl_=l-36.-9.*pow(1.-abs(fract(a*4.2+.12*l)-.5)*2.,1.4);if(abs(a)<1.8&&fl_<0.&&fl_>-4.) gold(s,vec3(1.1));else if(abs(a)<1.8&&fl_<-4.&&l>24.){oAA=gPx/4.;s.base=mix(hex(0x5a0e0c),hex(0xd8742a),oScale(vec2(a*12.,fl_/4.)));emit(s,vec3(.5,.06,.01)*lit);}
#endif
   }else if(abs(ni-2.)<1.6) gold(s,vec3(1.1));else{s.base=mix(wa1,tr1,.3);oAA=gPx/14.;s.base=mix(s.base,cl1,oDiaper(p.xy/14.)*.5);}}
#endif
 }
 if(s.cls<1.5||s.cls>7.5){vec3 g=lampGlow(p);float w=.35+.65*smoothstep(-.3,.6,dot(n,normalize(vec3(-sign(p.x)*.6,.4,.3))));emit(s,s.base*g*w*.62);
#if HALL==1
  // the dusk that lies along the floor, and catches what faces the gate
  float dz=max(p.z-GZ,0.);float spread=46.+dz*.16;float lane=smoothstep(spread,spread*.8,ax)*exp(-dz*.0034);if(m==10&&p.z>GZ) emit(s,hex(0xff4a1c)*.42*dusk*lane*s.base);else if(p.z>GZ&&n.z<-.1) emit(s,hex(0xff5a24)*.55*dusk*s.base*(-n.z)*exp(-dz*.0034)*smoothstep(spread+50.,spread-6.,ax));
#endif
 }else if(s.cls<2.5){vec3 g=lampGlow(p);s.base*=.55+1.0*min(vec3(1.4),g*vec3(1.,1.4,2.6));
#if HALL==1
  s.base*=mix(1.,.6+.6*exp(-max(p.z-GZ,0.)*.004),1.);
#endif
 }}
void surf(vec3 p,vec3 n,int m,inout Surf s){
 bool fl=m==10&&p.y<.5,hit=false;vec3 q=p,nn=n,rd0=gRd,c=vec3(0);int mm=m;float gp=gPx;Surf f0=s;
 surf0(p,n,m,s);
#ifdef POLISH
 if(fl&&s.cls<1.5){vec2 w=vec2(vn(p.xz*.22)-.5,vn(p.xz*.22+9.)-.5)*.012;vec3 r=reflect(gRd,normalize(vec3(w.x,1.,w.y)));r.y=abs(r.y);vec3 o=p+vec3(0,.1,0);float t=.5;vec2 h=vec2(0);for(int i=min(0,int(fT));i<44;i++){h=map(o+r*t);if(h.x<.004*t+.02){hit=true;break;}t+=h.x;if(t>700.)break;}
  if(hit&&t>1.){q=o+r*t;vec3 g=lampGlow(q);int k=int(h.y+.5);vec3 b=k==2||k==11?vec3(.75,.45,.12):k==8?tr1*.4:k==9?tr1:k==1&&abs(q.x)>WX-2.?mix(wa1*.5,vec3(1.2,.7,.35)*(HALL==0?lit:HALL==1?dusk*.5:.1),step(oArch(vec2(q.z-BZ*round(q.z/BZ),q.y-16.),15.,34.,4.),0.)):wa1*.8;vec3 e=b*(uAmb*.5+uKey*.12+min(g,vec3(HALL==2?.25:.7)));float fr=pow(1.-max(0.,-gRd.y),4.);emit(s,e*mix(.16,.75,fr));}
  else if(!hit){
#if HALL==1
   float fr=pow(1.-max(0.,-gRd.y),4.);emit(s,hex(0xff5a24)*dusk*mix(.06,.8,fr));
#endif
  }}
#endif
}
