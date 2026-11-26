// SURASA, mother of serpents: the head.  1 unit = 10 world units at scale 10.  z forward, y up; jaws hinge on the x axis at z = -4.5.
uniform float gape,wet,tongueIn;uniform vec3 TG[14];
uniform sampler2D tFace;
const float ZH=-4.5;const vec3 RA=vec3(6.2,3.7,7.6);
const vec3 EC=vec3(4.25,2.42,1.85),ED=vec3(.72,.46,.52);
vec3 toU(vec3 p){p.z-=ZH;p.yz=rot(-gape*.66)*p.yz;p.z+=ZH;return p;}
vec3 toL(vec3 p){p.z-=ZH;p.yz=rot(gape*.70)*p.yz;p.z+=ZH;return p;}
float flatS(vec3 p){return 1.+.42*smoothstep(-1.,7.,p.z);}
vec2 halfJaw(vec3 p,float sy){       // sy=+1 upper (p.y>0), -1 lower (mirrored so that p.y>0 is the bone side)
  float k=flatS(p);vec3 q=vec3(p.x,p.y*k,p.z);vec3 R=sy>0.?RA:vec3(5.9,2.7,7.3);
  float e=sEll(q,R);float i=sEll(q-vec3(0,-.15,-.10),R*vec3(.80,.72,.82));
  float d=smax(e,-i,.30);d=smax(d,-p.y+.0,.25);
  return vec2(d*.78,-i>e-.12?2.:1.);}
float teeth(vec3 p,float a,float b,float n,float L0,float seed,float lim){   // a row along the ellipse (a,b), pointing to -y
  float ph=atan(p.x/a,p.z/b);if(abs(ph)>lim+.3) return 1e3;float st=TAU/n;float c=floor(ph/st+.5);c=clamp(c,-floor(lim/st),floor(lim/st));float d=1e3;
  for(int k=-1;k<=1;k++){float id=c+float(k);float an=id*st;if(abs(an)>lim) continue;vec3 o=vec3(a*sin(an),0,b*cos(an));float r=h11(id+seed);float fang=exp(-pow((abs(an)-.34)/.13,2.));
    float L=L0*(.55+.35*r+1.15*fang)*(1.-.45*smoothstep(.8,lim,abs(an)));vec3 in_=normalize(vec3(-o.x,0,-o.z));float w=.30+.12*fang;
    vec3 q=p-o;float t=clamp(-q.y/L,0.,1.);vec3 ax=vec3(0,-t*L,0)+in_*.42*L*t*t*.5;float dd=length(q-ax)-w*(1.-t)*(1.+.5*(1.-t)*.4)-.015;d=min(d,dd);}
  return d*.62;}
vec2 map(vec3 p){
  vec3 u=toU(p),l=toL(p);vec3 lm=vec3(l.x,-l.y,l.z);
  vec2 A=halfJaw(u,1.),B=halfJaw(lm,-1.);
  // brow, snout and cheek relief on the upper jaw
  vec3 q=vec3(abs(u.x),u.yz);
  A.x=A.y<1.5?smin(A.x,sCone(q,vec3(1.6,2.7,4.6),vec3(4.9,3.3,.6),.5,.75),.8):A.x;A.x=smin(A.x,sCone(q,vec3(4.9,3.3,.6),vec3(5.6,3.0,-3.4),.75,.35),.7);
  A.x=smin(A.x,sEll(q-vec3(1.05,1.75,6.3),vec3(.95,.75,.95)),.5);A.x=smax(A.x,-sEll(q-vec3(1.25,2.05,6.95),vec3(.34,.30,.50)),.2);
  A.x=smin(A.x,sCone(u,vec3(0,2.35,5.6),vec3(0,3.75,-1.),.4,.55),.9);
  A.x=smin(A.x,sCone(lm*0.+vec3(abs(u.x),u.y,u.z),vec3(6.0,.55,-1.5),vec3(3.6,.55,5.8),.45,.40),.5);                  // upper lip
  B.x=smin(B.x,sCone(vec3(abs(lm.x),lm.yz),vec3(5.7,.50,-1.5),vec3(3.5,.45,5.5),.42,.40),.5);
  vec3 tv=p-vec3(0,-.2,-5.8);float tvd=max(sEll(tv,vec3(4.7,2.9+1.5*gape,3.9)),p.z+3.6);if(-tvd>A.x-.2)A.y=4.;if(-tvd>B.x-.2)B.y=4.;A.x=smax(A.x,-tvd,.2);B.x=smax(B.x,-tvd,.2);
  vec2 m=A.x<B.x?A:B;m.x=smin(A.x,B.x,.25*step(gape,.02)+.02);
  // throat bowl and stretched cheeks
  float rho=length(vec2(p.y,p.z-ZH));float xe=6.0*sqrt(max(.05,1.-pow((rho+ZH)/7.4,2.)));
  float ck=max(abs(abs(p.x)-xe+.35)-.20,rho-2.9-.35*sin(atan(p.y,p.z-ZH)*9.));ck=max(ck,max(u.y-.4,-l.y-.4));
  if(gape>.03){float k2=ck*.7;if(k2<m.x)m.y=13.;m.x=smin(m.x,k2,.35);}
  vec3 tp=p-vec3(0,-.2,-6.2);float bowl=abs(sEll(tp,vec3(5.2,3.4+1.6*gape,4.2)))-.35;bowl=max(bowl,p.z+4.15);float tun=length(vec2(p.x*.85,p.y+.4+.04*(p.z+9.)*(p.z+9.)*.0))-2.1-.15*sin(p.z*2.6);
  float th=max(bowl,-max(tun,p.z+7.));th=min(th,max(abs(tun)-.25,max(p.z+7.6,-p.z-9.2)));th=min(th,max(abs(p.z+9.)-.25,tun-.2));if(th*.85<m.x)m=vec2(th*.85,4.);
  // teeth, gums
  if(m.x>.0){float tt=min(teeth(u,5.25,6.75,54.,1.55,1.,1.95),teeth(u,4.45,5.75,46.,.95,7.,1.8));tt=min(tt,min(teeth(lm,5.0,6.45,52.,1.45,13.,1.95),teeth(lm,4.2,5.5,44.,.85,19.,1.8)));if(tt<m.x)m=vec2(tt,5.);}
  // tongue
  float td=1e3;for(int i=0;i<7;i++){vec3 a=TG[i],b=TG[i+1];float t=segT(p,a,b);vec3 o=p-mix(a,b,t);o.y*=1.9;float r=mix(1.35,.42,(float(i)+t)/7.);td=smin(td,(length(o)-r)*.55,.2);}
  for(int s=0;s<2;s++)for(int i=0;i<2;i++){vec3 a=i==0?TG[7]:TG[8+s*3],b=TG[9+s*3+i-0];if(i==0)b=TG[8+s*3+0];else b=TG[9+s*3];td=smin(td,sCone(p,a,b,i==0?.40:.26,i==0?.26:.05),.06);}
  if(td<m.x)m=vec2(td,6.);
  // eyes with gold rings, horns, forehead jewel
  vec3 ec=q-EC;float ey=max(length(ec)-1.02,-dot(ec,normalize(ED))-.25);m=U(m,vec2(ey,7.));vec3 ed=normalize(ED);float ez=dot(ec,ed);float rr=length(ec-ed*ez);m=U(m,vec2(length(vec2(rr-1.02,ez-.30))-.17,3.));float ea=atan(dot(ec,normalize(cross(ed,vec3(0,1,0)))),ec.y);
  float am=mod(ea,TAU/16.)-TAU/32.;m=U(m,vec2(length(vec3(am*rr,rr-1.32,ez-.22))-.14,8.));
  m=U(m,vec2(min(sCone(q,vec3(3.7,3.9,-1.2),vec3(5.2,5.9,-4.2),.60,.36),sCone(q,vec3(5.2,5.9,-4.2),vec3(5.0,8.6,-5.8),.36,.02))-.015*sin(u.z*11.),9.));
  m=U(m,vec2(min(sCone(q,vec3(5.2,2.2,-3.),vec3(7.2,2.8,-5.6),.42,.22),sCone(q,vec3(7.2,2.8,-5.6),vec3(8.4,4.8,-7.0),.22,.02))-.012*sin(u.z*13.),9.));
  vec3 j=u-vec3(0,3.75,2.0);j.yz=rot(.9)*j.yz;m=U(m,vec2(sEll(j,vec3(1.0,1.35,.42)),3.));m=U(m,vec2(sEll(j-vec3(0,0,.28),vec3(.66,.95,.36)),10.));
  float a2=atan(j.x/1.0,j.y/1.35);float s2=TAU/18.;float m2=mod(a2,s2)-s2*.5;m=U(m,vec2(length(vec3(m2*1.2,length(j.xy/vec2(1.22,1.58))*1.2-1.2,j.z))-.15,8.));
  for(int i=0;i<3;i++){float z=.4-1.5*float(i);m=U(m,vec2(sEll(u-vec3(0,4.15-.02*float(i),z),vec3(.34,.50,.55)),i==1||i==3?11.:3.));}
  return m;
}
vec3 scales(vec2 u){float e=0.,vv=0.,id=0.;float row=floor(u.y);
  for(int k=1;k>=-1;k--){float r=row+float(k);vec2 q=vec2(u.x+.5*mod(r,2.),u.y-r);float c=floor(q.x);q.x=fract(q.x)-.5;float y=q.y-.35;float d=length(vec2(q.x*1.05,max(y,0.)*.78))-.52;if(d<0.&&q.y>-.2){e=d;vv=clamp((q.y+.1)/1.15,0.,1.);id=h21(vec2(c,r));break;}}
  return vec3(e,vv,id);}
void surf(vec3 p,vec3 n,int m,inout Surf s){
  vec3 u=toU(p),l=toL(p);float up=u.y>-.05||p.y>0.?1.:0.;vec3 q=up>.5?u:vec3(l.x,-l.y,l.z);
  float dp=smoothstep(2.,-11.,p.z);
  if(m==1){
    vec2 uv=vec2(atan(q.x,q.y*1.4+1.)*7.6,-q.z*1.9-.4*abs(q.x));vec3 f=scales(uv);float tip=smoothstep(.5,.95,f.y),ed=smoothstep(-.11,-.03,f.x);
    vec3 a=up>.5?Pb[1]:mix(Pb[12],Pb[1],smoothstep(1.6,.4,q.y)*.75);vec3 sh=up>.5?Ps[1]:mix(Ps[12],Ps[1],smoothstep(1.6,.4,q.y)*.75);
    if(up>.5){float nose=smoothstep(3.,7.,q.z);a=mix(a,hex(0x2fa58c),nose*.6);a=mix(a,hex(0x12405e),smoothstep(2.6,4.,q.y)*.8);}
    s.base=mix(a*.72,a*1.18,tip)*(.86+.28*f.z);s.sh=mix(sh*.75,sh*1.15,tip);s.base=mix(s.base,hex(0xe8d27a),smoothstep(-.24,-.17,f.x)*(1.-ed)*.5);s.base=mix(s.base,s.base*.35,ed);s.sh=mix(s.sh,s.sh*.4,ed);
    float lip=smoothstep(.85,.55,q.y)*smoothstep(-.4,.1,q.y);s.base=mix(s.base,hex(0xd8a24a),lip*.0);float lp=smoothstep(.12,.04,abs(q.y-.95-.10*sin(q.z*3.)));s.base=mix(s.base,hex(0xf2cf6a),lp*.75);
    s.cls=8.;s.ink=.9;}
  if(m==2||m==13){                                                            // palate, ribbed and wet
    float rb=sin(q.z*4.2+1.3*abs(q.x)*.35+.4*sin(q.x*2.));float mid=smoothstep(.35,.05,abs(q.x));float k=smoothstep(.2,.8,rb);
    s.base=mix(hex(0xc8484e),hex(0xf09a86),k);s.sh=mix(hex(0x5a0c24),hex(0x8a2438),k);s.base=mix(s.base,hex(0xa83048),mid*.7);
    s.base=mix(s.base,hex(0x180410),dp*.96);s.sh=mix(s.sh,hex(0x0a0208),smoothstep(.0,.6,dp));s.ns=normalize(n+vec3(0,0,.5*cos(q.z*4.2+1.3*abs(q.x)*.35)));s.cls=8.;s.ink=.5;
    if(m==2&&q.y<.5){s.base=mix(hex(0xe8706e),hex(0x180410),dp*.9);}                                     // gums
    if(m==13){float st=sin(atan(p.y,p.z-ZH)*22.);s.base=mix(s.base,hex(0x7a1830),.5*smoothstep(.3,.8,st));}}
  if(m==4){float rb=sin(p.z*5.2+.5*sin(atan(p.x,p.y)*5.));s.base=mix(hex(0x8a2038),hex(0x3a0818),.5+.5*rb);float k=smoothstep(-4.8,-8.2,p.z);s.base=mix(s.base,hex(0x030104),k);s.sh=mix(hex(0x2a0614),hex(0x020103),k);s.cls=1.;if(k>.85){s.cls=4.;s.base=vec3(.0015,.0005,.001);}s.ink=.5*(1.-k);}
  if(m==5){float k=smoothstep(.6,-.9,q.y);s.base=mix(hex(0xd8a860),hex(0xfff6e0),k);s.sh=mix(hex(0x7a4a3a),hex(0x9a8ab0),k);s.cls=8.;s.ink=.85;s.base*=mix(1.,.35,smoothstep(.45,.9,dp));}
  if(m==6){s.base=mix(hex(0xd8344a),hex(0x7a1030),smoothstep(.15,.02,abs(p.x-TG[3].x))*.5);s.sh=hex(0x4a0820);s.base=mix(s.base,hex(0x18040c),smoothstep(.35,.8,dp));s.cls=8.;}
  if(m==7){vec3 c=vec3(abs(u.x),u.yz)-EC;vec3 d=normalize(ED);vec3 ex=normalize(cross(vec3(0,1,0),d)),ey=cross(d,ex);vec2 e=vec2(dot(c,-ex),dot(c,ey))/1.02;e.x=-e.x;vec4 t=texture(tFace,(e/1.1)*.5+.5);vec3 tc=pow(t.rgb/max(t.a,.003),vec3(2.2));s.base=mix(s.base,tc,t.a);s.sh=mix(s.sh,tc*.55,t.a);s.cls=6.;s.ink=.4;}
  if(m==9){s.base*=.82+.25*sin(u.z*9.+.5);s.ink=.9;}
  
  if(m==8||m==10||m==11)s.ink=.7;
  if(wet>0.&&m<2){float dr=smoothstep(.62,.7,fbm(vec2(atan(p.x,p.y)*9.,p.z*.8+fT*1.5)));s.base=mix(s.base,hex(0xeaf6f0),dr*wet*(1.-dp)*.6*step(float(m),1.5));}
}
