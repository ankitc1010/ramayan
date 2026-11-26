// JATAYU, body without wings and tail (those are feather meshes).  Figure space: z forward (flight), y up, origin between the shoulders.
// NK[6] neck curve to the skull, NR radii; LG[32+] legs: per leg hip knee ankle foot, then 4 toes x 4 points
uniform mat3 Bh;uniform vec3 NK[6];uniform vec3 HD;uniform vec3 LG[40];uniform float jaw,brow,dust;
uniform sampler2D tFace;
const vec3 EC=vec3(.80,.22,.62);
float bodyD(vec3 p){
  float d=sEll(p-vec3(0,-.25,.6),vec3(2.35,2.45,3.9));
  d=smin(d,sEll(p-vec3(0,.05,-3.2),vec3(1.75,1.55,3.2)),1.2);
  d=smin(d,sEll(vec3(abs(p.x)-1.75,p.y-.75,p.z-1.2),vec3(1.0,1.0,1.7)),.8);
  d=smin(d,sEll(p-vec3(0,-.75,2.2),vec3(1.5,1.9,2.2)),.8);
  return d;}
float neckD(vec3 p,out float t){float d=1e3;t=0.;for(int i=0;i<5;i++){float u=segT(p,NK[i],NK[i+1]);float k=(float(i)+u)/5.;float r=mix(1.32,.80,smoothstep(0.,.85,k));float e=length(p-mix(NK[i],NK[i+1],u))-r;if(e<d)t=k;d=smin(d,e,.18);}
  return d;}
vec2 beakD(vec3 h){
  vec3 q=vec3(abs(h.x),h.yz);
  // upper mandible: a deep curved hook
  float u=clamp((h.z-.9)/2.15,0.,1.2);float cy=-.06-.02*u-.62*pow(max(u-.28,0.),2.1);float hgt=mix(.44,.16,smoothstep(0.,1.05,u));float wid=mix(.40,.13,smoothstep(0.,1.,u));
  float d=length(vec2(q.x/wid,(h.y-cy)/hgt))-1.;d*=min(wid,hgt)*.8;d=max(d,max(.75-h.z,h.z-2.95));
  d=min(d,sCone(h,vec3(0,-.46,2.72),vec3(0,-1.12,2.80),.25,.04));d=smin(d,sCone(h,vec3(0,-.30,2.35),vec3(0,-.55,2.78),.30,.22),.2);
  d=smin(d,sEll(h-vec3(0,.06,1.05),vec3(.44,.42,.42)),.12);                // cere
  d=smax(d,-sEll(q-vec3(.40,.10,1.32),vec3(.08,.07,.16)),.04);
  float jd=jaw*.62;vec3 l=h-vec3(0,-.36,.55);l.yz=rot(-jd)*l.yz;float lo=sCone(l,vec3(0,-.06,.2),vec3(0,-.14,1.95),.30,.10);lo=max(lo,l.y-.03);
  vec2 m=vec2(d,3.+8.);m=U(m,vec2(lo*.9,12.));
  if(jaw>.02)m=U(m,vec2(sCone(l,vec3(0,.02,.2),vec3(0,.10,1.5),.13,.05),10.));
  return m;}
vec2 headD(vec3 h){
  vec3 q=vec3(abs(h.x),h.yz);
  float d=sEll(h-vec3(0,.08,-.05),vec3(.95,.92,1.18));
  d=smin(d,sEll(h-vec3(0,-.14,.75),vec3(.62,.55,.62)),.3);
  d=smin(d,sEll(q-vec3(.50,-.42,.15),vec3(.36,.42,.62)),.25);               // cheek and jowl
  d=smax(d,-sEll(q-vec3(.92,.18,.70),vec3(.30,.26,.36)),.18);
  d=smin(d,sCone(q,vec3(.34,.62,1.02),vec3(.98,.58,.15),.13,.15),.14);       // the brow ridge
  d=smin(d,sEll(q-EC+vec3(.10,.0,.0),vec3(.27,.29,.30)),.05);
  d-=.016*sin(h.z*16.+h.y*9.)*smoothstep(.4,-.6,h.y+.5*h.z);
  vec2 m=vec2(d,1.);m=U(m,beakD(h));
  // white tufts: brows, crown and beard
  float w=sCone(q,vec3(.62,.80,.62),vec3(1.10,.96,-.45),.14,.02);w=smin(w,sCone(q,vec3(.72,.72,.45),vec3(1.22,.74,-.55),.11,.02),.05);
  for(int i=0;i<4;i++){float k=float(i);w=min(w,sCone(q,vec3(.06+.14*k,.92-.06*k*k*.4,-.1),vec3(.10+.26*k,1.18-.10*k,-1.35+.12*k),.15,.02));}
  for(int i=0;i<3;i++){float k=float(i);w=min(w,sCone(q,vec3(.06+.12*k,-.58,.75-.18*k),vec3(.04+.10*k,-1.42+.14*k,.55-.35*k),.13,.02));}
  w+=.012*sin(h.z*26.+h.x*18.);
  return U(m,vec2(w*.9,2.));}
vec2 legsD(vec3 p){
  vec2 m=vec2(1e3,5.);
  for(int s=0;s<2;s++){int b=20*s;vec3 hp=LG[b],kn=LG[b+1],an=LG[b+2],ft=LG[b+3];
    float bd=length(p-mix(hp,ft,.55))-length(hp-ft)*.6-2.6;if(bd>m.x) continue;
    float th=sCone(p,hp,kn,1.25,.95);th=smin(th,sCone(p,kn,mix(kn,an,.62),.95,.42),.4);th-=.05*sin(dot(p,vec3(2.,6.,3.)))*.6;m=U(m,vec2(th*.9,4.));
    float sh=sCone(p,mix(kn,an,.5),an,.34,.30);sh=smin(sh,sCone(p,an,ft,.30,.34),.12);
    for(int t=0;t<4;t++){int k=b+4+t*4;sh=smin(sh,sCone(p,LG[k],LG[k+1],.28,.25),.1);sh=smin(sh,sCone(p,LG[k+1],LG[k+2],.25,.21),.06);
      vec3 a=LG[k+2],c=LG[k+3];vec3 md=mix(a,c,.5)+.26*normalize(cross(cross(c-a,LG[k+1]-a),c-a)+1e-4)*-1.;float cl=sCone(p,a,md,.185,.13);cl=min(cl,sCone(p,md,c,.13,.015));m=U(m,vec2(cl,7.));}
    m=U(m,vec2(sh,5.));
    vec3 ax=normalize(ft-an);vec3 o=p-mix(an,ft,.45);float y=dot(o,ax);m=U(m,vec2(length(vec2(length(o-ax*y)-.36,y*.5))-.09,3.));}
  return m;}
vec2 map(vec3 p){
  vec2 m=vec2(bodyD(p)*.95,4.);
  float t;float nd=neckD(p,t);
  nd-=.035*sin(t*62.+1.5*sin(atan(p.x,p.y-1.)*2.))*smoothstep(.12,.3,t);
  if(nd<m.x)m=vec2(nd,1.);
  // torque
  vec3 ax=normalize(NK[1]-NK[0]);vec3 o=p-NK[0]-ax*.95;float y=dot(o,ax);vec3 rv=o-ax*y;float rr=length(rv);
  if(abs(y)<1.2){float a=atan(rv.x,-rv.y);m=U(m,vec2((length(vec2(rr-1.48,y))-.20-.035*sin(a*34.+y*12.))*.8,3.));
    float st=TAU/16.;float am=mod(a+st*.5,st)-st*.5;m=U(m,vec2(length(vec3(am*rr,rr-1.50,y-.30))-.11,6.));
    float st2=TAU/10.;float ab=mod(a+st2*.5,st2)-st2*.5;float fr=step(abs(a),1.3);vec3 pd=vec3(ab*rr,rr-1.62,y+.0);m=U(m,vec2(sEll(pd-vec3(0,.16,.02),vec3(.17,.26,.15))+(1.-fr)*2.,3.));m=U(m,vec2(length(pd-vec3(0,.22,.14))-.11+(1.-fr)*2.,abs(ab-a)<.02?8.:9.));}
  float dh=length(p-HD)-3.4;if(dh<m.x){vec2 k=headD(Bh*(p-HD));m=vec2(k.y==1.&&m.y==1.?smin(m.x,k.x,.3):min(m.x,k.x),k.x<m.x?k.y:m.y);}
  float lb=min(length(p-LG[2]),length(p-LG[22]))-6.;if(lb<m.x)m=U(m,legsD(p));
  return m;}
// rows of scales: x across, y along (tips toward +y).  returns edge shade, v = 0..1 along the scale, id
vec3 scales(vec2 u){vec2 best=vec2(9.);float e=0.,vv=0.,id=0.;float row=floor(u.y);
  for(int k=1;k>=-1;k--){float r=row+float(k);vec2 q=vec2(u.x+.5*mod(r,2.),u.y-r);float c=floor(q.x);q.x=fract(q.x)-.5;float y=q.y-.35;float d=length(vec2(q.x*1.05,max(y,0.)*.78))-.52;if(d<0.&&q.y>-.2){e=d;vv=clamp((q.y+.1)/1.15,0.,1.);id=h21(vec2(c,r));break;}}
  return vec3(e,vv,id);}
void surf(vec3 p,vec3 n,int m,inout Surf s){
  vec3 h=Bh*(p-HD);
  if(m==4){                                                                   // feathered body
    bool leg=min(length(p-LG[2]),length(p-LG[22]))<3.2&&p.y<-1.2;
    vec2 uv=vec2(atan(p.x,p.y+.2)*3.4,-p.z*1.35+.25*sin(p.x*3.));if(leg)uv=vec2(atan(p.x-sign(p.x)*1.2,p.z-LG[1].z)*2.6,-p.y*1.6);
    vec3 f=scales(uv);float tip=smoothstep(.55,.95,f.y);float ed=smoothstep(-.10,-.02,f.x);
    float back=smoothstep(-.2,.6,n.y);vec3 a=mix(Pb[13],Pb[4],back);vec3 b=mix(Ps[13],Ps[4],back);
    a*=.86+.28*f.z;s.base=mix(a*.72,a*1.12,tip);s.sh=mix(b*.8,b*1.1,tip);
    float q=abs(fract(uv.x+.5*mod(floor(uv.y),2.))-.5);
    s.base=mix(s.base,s.base*.42,ed);s.sh=mix(s.sh,s.sh*.5,ed);s.base=mix(s.base,hex(0xf6dca0),smoothstep(-.20,-.15,f.x)*(1.-ed)*.55);
    float vent=smoothstep(.55,.85,-n.y);s.ink=.8;
  }
  if(m==1){
    float wr=0.;float isH=smoothstep(1.75,1.3,length(h-vec3(0,0,.2)));
    float t;neckD(p,t);float f=abs(fract(t*9.+.5+.22*sin(atan(p.x,p.y-1.)*3.)+.3*vn3(p*1.5))-.5);wr=smoothstep(.09,.03,f)*smoothstep(.10,.25,t)*(1.-isH)*.75;
    float w2=smoothstep(.10,.02,abs(fract(h.z*2.2+h.y*1.6+.5*vn3(h*2.))-.5))*isH*smoothstep(.1,-.5,h.y)*smoothstep(1.,.5,h.z)*.5;wr=max(wr,w2);
    s.base=mix(s.base,hex(0xb8685a),smoothstep(.2,.9,fbm3(p*.9))*.55);s.base=mix(s.base,hex(0xc9505a),smoothstep(.35,.0,length(vec3(abs(h.x),h.yz)-vec3(.75,-.05,.55)))*.5);
    s.base=mix(s.base,hex(0xe2c6b4),smoothstep(.5,.9,h.y)*isH*.6);
    s.base=mix(s.base,hex(0x4a1c26),wr);s.sh=mix(s.sh,hex(0x260c18),wr);
    float sg=h.x<0.?-1.:1.;vec3 q=vec3(abs(h.x),h.yz)-EC;vec3 d=normalize(vec3(.86,.04,.50));vec3 ex=normalize(vec3(-.50,.0,.86)),ey=normalize(cross(d,ex));ey*=sign(ey.y);
    vec2 e=vec2(dot(q,ex),dot(q,ey))/.46;vec3 nn=Bh*n;
    if(dot(nn*vec3(sg,1,1),d)>.02&&max(abs(e.x),abs(e.y))<1.45&&isH>.2){vec4 tx=texture(tFace,(e/1.5)*.5+.5);vec3 tc=pow(tx.rgb/max(tx.a,.003),vec3(2.2));float k=smoothstep(.2,.5,tx.a);if(k>0.){s.base=mix(s.base,tc,k);s.sh=mix(s.sh,tc*vec3(.6,.5,.6),k);if(k>.6){s.cls=6.;s.ink=.3;}}}
  }
  if(m==11||m==12){float k=smoothstep(1.2,2.6,h.z);s.base=mix(hex(0xe8b04a),hex(0x3a2a2e),k);s.sh=mix(hex(0x8a4a1c),hex(0x14101a),k);s.cls=8.;float g=smoothstep(1.28,1.18,h.z);s.base=mix(s.base,hex(0xc8746a),g*.9);s.sh=mix(s.sh,hex(0x7a3038),g*.9);
    float st=sin(h.z*16.+h.y*6.);s.base*=.95+.07*st;}
  if(m==2){float k=sin(h.z*22.+h.y*17.+h.x*13.);s.base*=.93+.08*k;s.ink=.6;}
  if(m==5){float b=abs(fract(dot(p,vec3(.3,2.6,1.4)))-.5);s.base*=mix(.6,1.,smoothstep(.04,.12,b));s.ink=.85;}
  if(m==6||m==8||m==9)s.ink=.6;
  if(dust>0.){s.base=mix(s.base,vec3(lum(s.base))*vec3(1.,.93,.86),dust*.6);}
}
