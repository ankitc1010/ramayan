// The brass lamp (nilavilakku) of a1, a2 and g5.  Dish centre at the origin, rim radius 3.2 at y=0.62; the burning wick's tip is at WICK = (3.05, 0.92, 0).  Cloth screen at z = clothZ.
#define TMAX 90.
#define STEPS 120
#define RELAX .8
uniform float clothZ,glowW,glowL;
const vec3 WICK=vec3(3.05,.92,0.);
float dish(vec3 p){
  vec3 q=p;float a=atan(q.z,q.x);float sp=exp(-a*a*7.);               // spout toward +x
  float r=length(q.xz)/(1.+.13*sp*smoothstep(1.5,3.4,length(q.xz)));
  float prof=.055*r*r-.02;                                             // bowl
  float shell=abs(q.y-prof)-.10;
  float d=max(shell*.72,r-3.2);
  d=smin(d,length(vec2(r-3.2,q.y-.58))-.14,.10);                       // rolled rim
  float pet=abs(sin(a*12.));float band=length(vec2(r-2.55,(q.y-.18)*.8))-.20-.05*pet;d=smin(d,band,.06);
  return d;}
vec2 map(vec3 p){
  float bd=length(p-vec3(0,1.,0))-6.5;vec2 m=vec2(1e3,0.);
  if(bd<1.){
    m=vec2(dish(p),2.);
    float r=length(p.xz),a=atan(p.z,p.x);
    // foot and stem
    float st=length(p.xz)-(.42+.16*sin(p.y*3.1)+.10*smoothstep(-1.,-3.,p.y));st=max(st,p.y-.0);m=U(m,vec2(st*.7,2.));
    // central finial: stacked rings, a lotus bud
    float fi=r-(.46-.10*p.y+.13*sin(p.y*6.2));fi=max(fi,max(-p.y,p.y-2.3));m=U(m,vec2(fi*.6,2.));
    vec3 l=p-vec3(0,2.75,0);float lb=sEll(l,vec3(.52,.70,.52));float pt=abs(sin(a*4.+.4));lb-=.06*pt*smoothstep(.7,-.4,l.y);m=U(m,vec2(lb*.8,2.));
    m=U(m,vec2(length(p-vec3(0,3.55,0))-.16,2.));
    // beads round the rim
    vec3 b=polar(p,44.,0.);m=U(m,vec2(length(b-vec3(0,.36,3.16))-.115,2.));
    // oil
    float oil=max(abs(p.y-.40)-.02,r-2.95);m=U(m,vec2(oil,3.));
    // wick: cotton rope from the oil over the lip
    vec3 w0=vec3(.6,.36,.25),w1=vec3(2.0,.47,.05),w2=WICK;float tw=.02*sin(p.x*22.+atan(p.y-.5,p.z)*2.);
    float wk=sCone(p,w0,w1,.13,.135);wk=smin(wk,sCone(p,w1,w2,.135,.105),.06)-tw;m=U(m,vec2(wk*.8,4.));
  } else m.x=bd;
  float fold=.35*sin(p.x*.55)+.18*sin(p.x*1.3+1.);float cl=p.z-clothZ-fold*.35;m=U(m,vec2(cl*.8,5.));
  return m;}
void surf(vec3 p,vec3 n,int m,inout Surf s){
  float a=atan(p.z,p.x),r=length(p.xz);
  if(m==2){s.cls=2.;s.base=hex(0xf2c27a);s.sh=hex(0x3a1408);
    float g=0.;g=max(g,smoothstep(.05,.02,abs(fract(r*2.2)-.5))*step(r,3.)*.5);float pt=abs(fract(a*24./TAU)-.5);g=max(g,smoothstep(.07,.03,abs(pt-.5*smoothstep(1.2,2.4,r)))*step(1.2,r)*step(r,2.4));
    s.base*=1.-.55*g;s.ink=.75;}
  if(m==3){s.cls=4.;s.ink=.5;vec3 rd=normalize(p-ro);vec3 nn=normalize(vec3(.015*sin(p.x*7.+fT*1.3)+.012*sin(p.z*9.-fT),1.,.015*sin(p.z*8.+fT*1.1)));vec3 rf=reflect(rd,nn);
    vec2 wx=vec2(2.05,-.2);float tt=dot(wx-p.xz,rf.xz)/max(dot(rf.xz,rf.xz),1e-3);vec3 q=p+rf*max(tt,0.);float dx=length(q.xz-wx);float hy=q.y-WICK.y;float fl_=smoothstep(.36,.05,dx)*smoothstep(-.1,.3,hy)*smoothstep(2.4,1.0,hy);
    float gl=exp(-dx*dx*.35)*.55;float edge=smoothstep(2.4,2.95,r);s.base=(hex(0x3a1404)*(.25+gl*1.2)+hex(0xc8641a)*gl*.35+hex(0xffc86a)*fl_*1.1+hex(0xa85a18)*edge*.25)*glowL;}
  if(m==4){float ch=smoothstep(.55,.0,length(p-WICK));s.base=mix(hex(0xf3e7cd),hex(0x1c120e),ch);s.sh=s.base*.4;s.glow=0.;
    float em=smoothstep(.34,.02,length(p-WICK-vec3(.02,.04,0)))*glowW;if(em>.02){s.cls=4.;s.base=mix(s.base*.25,hex(0xff5a1c)*1.6,em);}s.ink=.6;}
  if(m==5){float wv=.5+.5*sin(p.x*26.)*sin(p.y*26.);s.base=hex(0xd8b88a)*(.86+.14*wv);s.sh=hex(0x1a0c08);s.ink=0.;s.ns=normalize(n+vec3(.25*cos(p.x*.55),0,0));}
}
