// VANARAS: the anatomy of hanuman.glsl in plain dress, cheap enough to bake by the dozen.
// look: 0 warrior 1 langur 2 youth 3 bear 4 king 5 prince;  orn bits: 1 headband 2 bone necklace 4 armbands 8 bead garland;  hold: 0 nothing 1 rock in the right hand 2 tree 3 club 4 stone on both hands
#define VANARA_LIB
#include "hanuman.glsl"
uniform int look,orn,hold;uniform float tailW,tailL;      // tailW: phase of the tail's wave 0..1;  tailL: its length, 0 = none
#define ON(b) ((orn&(b))!=0)
vec3 palmAt(int k){return (k==0?J[6]:J[9])+(vec3(0.,.62,.20)*B[7])*(k==0?BL:BR);}
vec4 TP[10];vec3 hO,hX_,hY_,hZ_;                   // tail joints and the frame of the thing held: found once per pixel, before the march
void vInit(){
  initRig();dhE=look>=3?.56:.22;
  vec3 a=J[0]-pZ*.72+pY*.05,dr=normalize(-pZ-pY*.30);TP[0]=vec4(a,.25);float sg=tailL/9.;
  for(int i=0;i<9;i++){float u=float(i)/8.;float e=radians(mix(-40.,92.,smoothstep(.0,.62,u))-34.*smoothstep(.72,1.,u)+9.*u*sin(tailW*TAU-u*4.));float az=.55*u*sin(tailW*TAU-u*3.3)+.25*sin(u*3.);
    vec3 t=vec3(sin(az)*cos(e),sin(e),-cos(az)*cos(e));t=normalize(mix(dr,t,smoothstep(0.,.25,u)));a+=t*sg;a.y=max(a.y,.32);TP[i+1]=vec4(a,i==8?.09:mix(.25,.17,u)+(i==7?.07:0.));}
  if(hold==1) hO=palmAt(1)+(vec3(0.,.25,.72)*B[7])*BR;else if(hold==4) hO=.5*(palmAt(0)+palmAt(1))+normalize(vec3(0,1,0)*.8+.2*cY)*1.05;else hO=palmAt(1)+(vec3(0,0,.12)*B[7])*BR;
  mat3 q=transpose(BR);hY_=q[0];hZ_=q[2];hX_=cross(hZ_,hY_);
}
#define initRig vInit
float tailD(vec3 p){
  if(tailL<.01) return 1e3;float bd=length(p-TP[5].xyz)-.62*tailL;if(bd>.6) return bd;
  float d=1e3;for(int i=0;i<9;i++) d=smin(d,sCone(p,TP[i].xyz,TP[i+1].xyz,TP[i].w,TP[i+1].w),.10);return d;
}
vec2 band(vec3 h){                                 // a knotted strip of cloth round the brow
  vec3 c=h-vec3(0,.52,-.10);c.yz=rot(.10)*c.yz;c.xz/=vec2(.97,1.03);float r=length(c.xz);float d=max(abs(r-.835)-.03,abs(c.y+.012*sin(atan(c.x,c.z)*9.))-.095)-.015;
  vec3 k=c-vec3(0,-.02,-.92);d=min(d,length(k)-.12);vec3 q=vec3(abs(k.x),k.yz);d=min(d,max(sCone(q,vec3(.02,0,0),vec3(.26,-.85,-.22),.05,.12),-1e3));return vec2(d*.9,8.);}
vec2 crown(vec3 p){                                // leaf crown of the kings: look 4 five tall leaves over a dome, look 5 a diadem
  float bd=length(p-vec3(0,.95,0))-1.35;if(bd>.5) return vec2(bd,3.);
  vec3 c=p-vec3(0,.12,-.10);c.yz=rot(.10)*c.yz;c.xz/=vec2(.99,1.05);float r=length(c.xz);
  float d=max(abs(r-.83)-.04,abs(c.y-.52)-.085)-.02;d=min(d,sTor(c-vec3(0,.42,0),.84,.04));
  vec3 g=polar(c,20.,0.);float gem=sEll(g-vec3(0,.53,.885),vec3(.06,.06,.04));
  if(look==4){
    vec3 q=polar(c,9.,0.)-vec3(0,.80,.80);q.yz=rot(-.14)*q.yz;float lf=max(length(vec2(abs(q.x)+.30,q.y-.02))-.52,abs(q.z)-.03)-.02;d=min(d,max(lf,-max(length(vec2(abs(q.x)+.30,q.y-.02))-.44,.02-q.z))*.9);gem=min(gem,sEll(q-vec3(0,.02,.05),vec3(.07,.11,.04)));
    d=min(d,max(sEll(c-vec3(0,.56,0),vec3(.74,.66,.74)),-c.y+.56));d=min(d,length(c-vec3(0,1.28,0))-.15);d=min(d,sCone(c,vec3(0,1.36,0),vec3(0,1.62,0),.08,.01));}
  else{vec3 f=c-vec3(0,.78,.80);f.yz=rot(-.18)*f.yz;float v=length(vec2(abs(f.x)+.34,f.y))-.62;d=min(d,max(max(v,abs(f.z)-.035)-.02,-max(v+.08,.02-f.z)));gem=min(gem,sEll(f-vec3(0,-.05,.06),vec3(.10,.16,.05)));
    vec3 q=vec3(abs(c.x),c.yz)-vec3(.52,.66,.60);q.xz=rot(-.75)*q.xz;d=min(d,max(length(vec2(abs(q.x)+.26,q.y))-.40,abs(q.z)-.03)-.02);}
  return U(vec2(d*.95,3.),vec2(gem,4.));}
vec2 held(vec3 p){
  if(hold==0) return vec2(1e3,9.);
  vec3 q=p-hO;
  if(hold==1||hold==4){float R=hold==1?.95:1.75;float bd=length(q)-R*1.25;if(bd>.5) return vec2(bd,10.);
    q.xy=rot(.5)*q.xy;q.yz=rot(.7)*q.yz;float d=sBox(q,vec3(.82,.66,.72)*R,.34*R);d=smax(d,dot(q,vec3(.738,.527,-.422))-.72*R,.1*R);d=smax(d,dot(q,vec3(-.508,.609,.609))-.74*R,.1*R);return vec2(d*.9,10.);}
  q=vec3(dot(q,hX_),dot(q,hY_),dot(q,hZ_));
  if(hold==3){float d=sCone(q,vec3(0,-1.1,0),vec3(0,2.4,0),.15,.30);d=smin(d,sCone(q,vec3(0,2.2,0),vec3(0,3.6,0),.32,.46),.3);vec3 k=polar(q,5.,0.);d=smin(d,length(vec3(k.x,q.y-2.7,k.z-.36))-.13,.1);return vec2(smin(d,length(vec3(k.x,q.y-3.4,k.z-.42))-.13,.1),9.);}
  float bd=sCap(q,vec3(0,-1.6,0),vec3(0,5.4,0),1.9);if(bd>.6) return vec2(bd,9.);
  float d=sCone(q,vec3(0,-1.6,0),vec3(.15,3.6,0),.26,.17);d=smin(d,sCone(q,vec3(.05,2.,0),vec3(1.1,4.0,.4),.16,.08),.15);d=smin(d,sCone(q,vec3(.05,2.6,0),vec3(-.9,4.5,-.3),.15,.07),.15);
  float l=sEll(q-vec3(.1,4.5,0),vec3(1.05,.95,.95));l=smin(l,sEll(q-vec3(1.25,4.1,.4),vec3(.80,.62,.72)),.15);l=smin(l,sEll(q-vec3(-1.0,4.7,-.3),vec3(.85,.68,.75)),.15);
  l-=.16*abs(sin(q.x*5.+q.y*2.)*sin(q.y*5.3-q.z*3.))-.02;
  return U(vec2(d,9.),vec2(l*.75,15.));
}
vec2 map(vec3 p){
  float td=hTorso(p),sk=hLimbs(p,td);sk=smin(sk,hNeck(p),.20);sk=smin(sk,hTufts(p),.09);sk=smin(sk,tailD(p),.16);
  vec2 m=vec2(sk,1.);
  float dh=length(p-J[3]);
  if(dh-2.6*HS[0]<m.x){vec3 h=Hd(p);float S=HS[0];
    float hd=vHead(h)*S,ru=vRuff(h)*S;vec2 e=vEars(h);
    if(look!=4){vec3 hq=vec3(abs(h.x),h.yz);float cr=lockD(hq,vec3(.02,.80,.36),vec3(.04,1.10,.06),vec3(.02,1.30,-.28),.15);cr=min(cr,lockD(hq,vec3(.17,.78,.22),vec3(.22,1.03,-.10),vec3(.21,1.13,-.48),.15));cr=min(cr,lockD(hq,vec3(.33,.70,.08),vec3(.42,.90,-.20),vec3(.45,.94,-.58),.15));ru=smin(ru,cr*S,.06);}
    m=U(m,vec2(hd,12.));m=U(m,vec2(ru,2.));m=U(m,vec2(e.x*S,13.));
    if(ON(1)){vec2 k=band(h);m=U(m,vec2(k.x*S,k.y));}
    if(look>=4){vec2 k=crown(h);m=U(m,vec2(k.x*S,k.y));k=ringKundala(h);m=U(m,vec2(k.x*S,k.y));}}
  if(td<.7){vec3 c=Bc*(p-J[1]);
    if(ON(2)){m=U(m,vec2(beadsD(c,td,vec2(0,1.62),1.05,.085,30.),6.));float a=atan(c.x,-(c.y-1.62));for(int i=-2;i<=2;i++){float x=float(i)*.26;vec2 o=vec2(0,1.62)+1.14*vec2(sin(x),-cos(x));vec2 t=o+.40*vec2(sin(x),-cos(x));vec3 pq=vec3(c.xy,td-.03);m=U(m,vec2(max(sCone(pq,vec3(o,0),vec3(t,0),.085,.015),-c.z),6.));}}
    if(ON(8)){m=U(m,vec2(beadsD(c,td,vec2(0,1.55),1.45,.10,40.),9.));}
    if(look>=4){m=U(m,vec2(beadsD(c,td,vec2(0,1.66),1.02,.075,-1.),3.));m=U(m,vec2(beadsD(c,td,vec2(0,1.66),1.20,.060,44.),3.));m=U(m,vec2(max(beadsD(c,td,vec2(0,1.60),1.95,.075,56.),abs(c.x)-1.32),look==4?3.:6.));vec3 pd=c-vec3(0,-.36,0);m=U(m,vec2(max(sEll(vec3(pd.xy,td-.05),vec3(.20,.25,.13)),-c.z),4.));}}
  vec3 loc;m=U(m,vec2(dhoti(p,loc),7.));
  vec3 q=Bp*(p-J[0]);
  if(length(q)-2.6<m.x){float be=ringD(vec3(q.x,q.y-.46,q.z*1.14),vec3(0),vec3(0,1,0),1.03*B[3]+.10+.30*B[9]*smoothstep(-.4,.8,q.z),.11,.06);m=U(m,vec2(be*.8,look>=4?3.:9.));}
  for(int s=0;s<2;s++){vec3 a=J[0]+pY*.36+pZ*(s==0?.96+.4*B[9]:-.92),kn=.5*(J[11]+J[15]);vec3 dn=normalize(mix(normalize(kn-J[0]),-pY,.35)-(s==1?pZ*.25:vec3(0)));float ln=look>=3?2.3:(s==0?2.2:1.9);vec3 b=a+dn*ln+pZ*(s==0?.24:-.3)+Wind*.5;vec2 pl;
    if((s==0||look<3)&&length(p-mix(a,b,.5))-1.8<m.x) m=U(m,vec2(pleatD(p,a,b,.26,.40,pl),8.));}
  if(ON(4)||look>=4) for(int s=0;s<2;s++){vec3 e0=s==0?J[4]:J[7],e1=s==0?J[5]:J[8],e2=s==0?J[6]:J[9];vec3 u=normalize(e1-e0),v=normalize(e2-e1);
    m=U(m,vec2(ringD(p,mix(e0,e1,.42),u,.49*B[5],look>=4?.13:.07,.04),look>=4?3.:9.));m=U(m,vec2(ringD(p,mix(e1,e2,.86),v,.275*B[5],look>=4?.17:.10,.03),look>=4?3.:9.));
    if(look>=4){vec3 l0=s==0?J[11]:J[15],l1=s==0?J[12]:J[16];vec3 w=normalize(l1-l0),o=p-mix(l0,l1,.9);float y=dot(o,w);m=U(m,vec2(length(vec2(length(o-w*y)-.33*B[6],y))-.09,3.));}}
  m=U(m,held(p));
  // Never run (look is 0..5).  NVIDIA inlines a whole shader of this size at each of the nine map() calls: 15 s to compile and twice the time per frame.  Past a size limit it keeps real calls.
  if(look==77) for(int i=0;i<6;i++){vec3 q=p+float(i);m=U(m,crown(q));m=U(m,vec2(vRuff(q),2.));m=U(m,vec2(hLimbs(q,1.),2.));}
  return m;
}
void surf(vec3 p,vec3 n,int m,inout Surf s){
  if(m==1){bodySurf(p,n,s);vec3 c=Bc*(p-J[1]);
    if(look==3&&c.z>0.){float v=abs(length(vec2(c.x,c.y-1.35)*vec2(1.,.85))-1.15);float k=smoothstep(.17,.11,v+.10*vn(c.xy*vec2(9.,3.)))*step(c.y,1.1);s.base=mix(s.base,hex(0xe9cf9a),k);s.sh=mix(s.sh,hex(0x8a6a50),k);}}
  if(m==12) headSurf(p,n,s);
  if(m==2) ruffSurf(p,n,s);
  if(m==13) earSurf(p,n,s);
  if(m==7){vec3 loc;dhoti(p,loc);float u=loc.x,a=loc.y,e=dhE;float bd=smoothstep(e-.10,e-.09,u);if(look<3) bd*=.0;
    s.base=mix(s.base,Pb[16],bd);s.sh=mix(s.sh,Ps[16],bd);if(look>=4){float ln=step(.5,fract(u*46.))*step(e-.13,u)*step(u,e-.06);s.base=mix(s.base,hex(0xffe08a),ln*.8);}
    float fl=sin(a*8.+u*4.);s.base*=1.-.20*smoothstep(.5,.95,-fl)*smoothstep(.0,.2,u);s.ink=.8;}
  if(m==8){vec3 q=Bp*(p-J[0]);float st=step(.6,fract(q.y*2.2));s.base=mix(s.base,Pb[16],st*.55);s.ink=.85;}
  if(m==9){float g=vn(vec2(atan(p.x,p.z)*6.,p.y*9.));s.base*=.82+.36*g;}
  if(m==10){float c=fbm3(p*2.2);s.base*=.75+.5*c;s.base=mix(s.base,s.sh*.8,smoothstep(.05,.02,abs(vn3(p*1.7)-.5))*.6);}
  if(m==15){vec4 v=voro((p.xy+p.zy*.6)*4.2);s.base=mix(s.base*.72,s.base*1.25,v.z);s.base=mix(s.base,s.sh*.6,smoothstep(.10,.03,v.y)*.8);s.ns=normalize(n+vec3(v.z-.5,v.w-.5,0.)*.8);}
}
