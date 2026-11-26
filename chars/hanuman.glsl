// HANUMAN, and the anatomy every vanara shares (vanara.glsl includes this file with VANARA_LIB defined, which leaves out map() and surf()).
// HS: 0 head scale 1 muzzle length 2 muzzle width 3 ruff length 4 ear size 5 brow 6 beard 7 nose width
#define Hd(p) (Bh*((p)-J[3])/HS[0])
float gs(float x){return exp(-x*x);}
// ---------------------------------------------------------------- body
float hTorso(vec3 p){
  vec3 c=Bc*(p-J[1]),h=Bp*(p-J[0]),q=vec3(abs(c.x),c.yz);float W=B[0],D=B[1];
  float d=sEll(c-vec3(0,.10,-.06),vec3(1.46*W,1.28,.94*D));
  vec3 l=q-vec3(.98*W,-.42,-.22*D);l.xy=rot(-.30)*l.xy;d=smin(d,sEll(l,vec3(.60*W,1.70,.58*D)),.40);
  d=smin(d,sCone(q,vec3(.10,1.66,-.30),vec3(1.70*B[11],1.00,-.16),.50,.52),.46);
  vec3 a=J[0]+pY*.10,b=J[1]-cY*.35;float t=segT(p,a,b);vec3 o=p-mix(a,b,t),w=mix(Bp*o,Bc*o,smoothstep(0.,1.,t));
  float r=mix(B[3]*1.10,B[2]*1.30,smoothstep(.10,1.,t))+.10*gs((t-.0)/.22);
  float wa=(length(w*vec3(1.,1.,1.20))-r)*.82;
  float fr=smoothstep(.35,.75,w.z/r);
  wa-=B[9]*.62*gs((t-.40)/.42)*smoothstep(-.5,.9,w.z/r);
  float ab=(1.-min(B[9]*1.4,1.))*fr;                              // the wall of the belly
  wa+=ab*(.060*gs(w.x/.075)*smoothstep(-.1,.2,t)+.050*smoothstep(.62,.50,abs(w.x))*(gs((t-.30)/.045)+gs((t-.56)/.045)+gs((t-.82)/.05))+.05*gs((abs(w.x)-.62)/.09));
  d=smin(d,wa,.34);
  float pe=sEll(h-vec3(0,-.04,-.04),vec3(1.06*B[4],.80,.84));vec3 g=vec3(abs(h.x)-.44,h.y+.30,h.z+.34);pe=smin(pe,length(g)-.54*B[4],.3);
  d=smin(d,pe,.36);
  vec3 pc=q-vec3(.76*W,.50,.60*D);pc.xy=rot(.16)*pc.xy;d=smin(d,sEll(pc,vec3(.80*W,.58,.44)),.13);
  d=smax(d,-sCone(c,vec3(0,1.02,1.02*D),vec3(0,.02,1.14*D),.09,.07),.16);
  d=smin(d,sCone(q,vec3(.14,1.24,.46*D),vec3(1.30*B[11],1.40,.08),.075,.07),.16);
  return d;
}
float hNeck(vec3 p){
  vec3 c=Bc*(p-J[2]);vec3 q=vec3(abs(c.x),c.yz);
  float d=sCone(p,J[2]-cY*.45,J[3]-hY*.55*HS[0]-hZ*.20,.66*B[10],.60*B[10]);
  return smin(d,sCone(q,vec3(.26,.20,-.26),vec3(1.15*B[11],-.36,-.10),.44,.30),.34);
}
vec3 armF(vec3 a,vec3 b,vec3 c){return normalize((a+c)*.5-b+cZ*.14+vec3(1e-4));}
vec3 legK(vec3 a,vec3 b,vec3 c){return normalize(b-(a+c)*.5+pZ*.16+vec3(1e-4));}
float hArm(vec3 p,vec3 a,vec3 b,vec3 c,float s){
  float bd=min(sCap(p,a,b,.70*s),sCap(p,b,c,.52*s));if(bd>.6) return bd;
  vec3 f=armF(a,b,c);vec3 u=normalize(b-a);f=normalize(f-u*dot(f,u)*.6);
  float d=sCone(p,a-u*.02,mix(a,b,.34),.545*s,.46*s);                                                   // deltoid
  d=smin(d,sCone(p,mix(a,b,.2),b,.43*s,.33*s),.14);
  d=smin(d,sCone(p,mix(a,b,.46)+f*.20*s,mix(a,b,.68)+f*.18*s,.32*s,.27*s),.09);                        // biceps
  d=smin(d,sCone(p,mix(a,b,.36)-f*.19*s,mix(a,b,.66)-f*.14*s,.33*s,.25*s),.09);                        // triceps
  vec3 e=mix(b,c,.28);
  float k=sCone(p,b,e,.33*s,.43*s);k=smin(k,sCone(p,e,mix(b,c,.62),.43*s,.31*s),.12);k=smin(k,sCone(p,mix(b,c,.55),c,.33*s,.225*s),.14);
  return smin(d,k,.09);
}
float hLeg(vec3 p,vec3 a,vec3 b,vec3 c,float s){
  float bd=min(sCap(p,a,b,.92*s),sCap(p,b,c,.66*s));if(bd>.6) return bd;
  vec3 k=legK(a,b,c),u=normalize(b-a),v=normalize(c-b);vec3 k1=normalize(k-u*dot(k,u)*.8),k2=normalize(k-v*dot(k,v)*.9);
  float d=sCone(p,a,mix(a,b,.45),.69*s,.69*s);
  d=smin(d,sCone(p,mix(a,b,.42),b,.68*s,.40*s),.16);
  d=smin(d,sCone(p,mix(a,b,.28)+k1*.16*s,mix(a,b,.74)+k1*.15*s,.58*s,.33*s),.16);                      // quadriceps
  d=smin(d,length(p-b-k2*.07*s)-.39*s,.10);
  d=smin(d,sCone(p,b,c,.40*s,.27*s),.16);
  d=smin(d,sCone(p,mix(b,c,.18)-k2*.19*s,mix(b,c,.42)-k2*.16*s,.42*s,.31*s),.20);                      // calf
  return d;
}
float hFoot(vec3 p,vec3 an,vec3 heel,vec3 toe,float s,float inner){
  float bd=sCap(p,heel,toe,.62*s);if(bd>.5) return bd;
  vec3 f=normalize(toe-heel),u=normalize(an-mix(heel,toe,.2));u=normalize(u-f*dot(u,f));vec3 sd=cross(f,u)*inner;
  float d=sCone(p,an,mix(an,heel,.75),.24*s,.27*s);
  d=smin(d,length(p-heel)-.265*s,.16);
  d=smin(d,sCone(p,mix(an,heel,.30)+f*.14,toe-f*.46*s+u*.05,.27*s,.22*s),.22);
  d=smin(d,sCone(p,heel,toe-f*.46*s-sd*.10*s,.22*s,.22*s),.16);
  d=smin(d,sCone(p,heel+f*.5*s,toe-f*.50*s+sd*.15*s,.20*s,.21*s),.16);
  for(int i=0;i<5;i++){float k=float(i);float x=.295-.150*k;float big=i==0?1.:0.;
    d=smin(d,sCone(p,toe-f*(.50+.04*k)*s+sd*(x+.02*big)*s,toe+f*(.06-.085*k+.02*big)*s+sd*(x+.05*big)*s-u*.06*s,(.115+.030*big)*s,(.080+.030*big)*s),.045);}
  return d;
}
float hLimbs(vec3 p,float d){
  float A=B[5],L=B[6];
  d=smin(d,hArm(p,J[4],J[5],J[6],A),.22);d=smin(d,hArm(p,J[7],J[8],J[9],A),.22);
  d=smin(d,handD(p,0),.12);d=smin(d,handD(p,1),.12);
  float g=min(hLeg(p,J[10],J[11],J[12],L),hLeg(p,J[14],J[15],J[16],L));
  g=smin(g,hFoot(p,J[12],J[18],J[13],L,1.),.12);g=smin(g,hFoot(p,J[16],J[19],J[17],L,-1.),.12);
  return smin(d,g,.22);
}
// pointed locks that break the outline: elbows, calves, shoulders
float hTufts(vec3 p){
  float d=1e3;
  for(int s=0;s<2;s++){vec3 a=s==0?J[4]:J[7],b=s==0?J[5]:J[8],c=s==0?J[6]:J[9];float A=B[5];
    float bd=length(p-mix(b,c,.2))-1.3*A;if(bd<d){if(bd>.5) d=min(d,bd);else{vec3 f=armF(a,b,c);vec3 v=normalize(c-b);f=normalize(f-v*dot(f,v));vec3 x=cross(v,f);
      for(int i=0;i<3;i++){float k=float(i);vec3 o=mix(b,c,.10+.16*k)-f*.28*A+x*(k-1.)*.10*A;d=smin(d,sCone(p,o,o-f*.22*A-v*(.36+.06*k)*A,.17*A,.012),.06);}}}
    vec3 k0=s==0?J[10]:J[14],k1=s==0?J[11]:J[15],k2=s==0?J[12]:J[16];float L=B[6];
    float bl=length(p-mix(k1,k2,.5))-1.4*L;if(bl<d){if(bl>.5) d=min(d,bl);else{vec3 k=legK(k0,k1,k2);vec3 v=normalize(k2-k1);k=normalize(k-v*dot(k,v));vec3 x=cross(v,k);
      for(int i=0;i<2;i++){float j=float(i);vec3 o=mix(k1,k2,.44+.20*j)-k*.22*L+x*(j-.5)*.16*L;d=smin(d,sCone(p,o,o-k*.20*L+v*.48*L,.18*L,.012),.06);}}}
  }
  return d;
}
// ---------------------------------------------------------------- head
float vHeadBase(vec3 p){
  float jd=jaw*.26,mz=HS[1],mw=HS[2];vec3 q=vec3(abs(p.x),p.yz);
  float d=sEll(p-vec3(0,.22,-.12),vec3(.80,.82,.86));
  d=smin(d,length(q-vec3(.45,-.16,.34))-.33,.22);
  d=smin(d,sEll(p-vec3(0,-.44,.46+.12*mz),vec3(.55*mw,.40,.54*mz)),.22);
  d=smin(d,sEll(p-vec3(0,-.80-jd,.36+.10*mz),vec3(.48*mw,.26,.48*mz)),.14);
  d=smin(d,sCone(q,vec3(.18,-.86-jd,.20),vec3(.58,-.42-jd*.5,-.10),.18,.26),.24);
  return d;
}
float vHead(vec3 p){
  float jd=jaw*.26,mz=HS[1];vec3 q=vec3(abs(p.x),p.yz);float zf=.46+.66*mz;                          // zf: front of the muzzle
  float d=vHeadBase(p);
  d=smax(d,-sEll(q-vec3(.34,.00,.92),vec3(.27,.16,.22)),.16);                                       // eye hollows
  d=smin(d,sCone(q,vec3(.04,.235,.74),vec3(.54,.225,.50),.125*HS[5],.095*HS[5]),.13);                  // brow
  float n=sCone(p,vec3(0,.12,.74),vec3(0,-.16,zf-.16),.085,.105);
  n=smin(n,sEll(p-vec3(0,-.235,zf-.11),vec3(.20*HS[7],.095,.11)),.08);
  n=smin(n,length(q-vec3(.155*HS[7],-.265,zf-.17))-.088,.06);
  n=smax(n,-sEll(q-vec3(.085*HS[7],-.325,zf-.03),vec3(.052,.036,.08)),.03);
  d=smin(d,n,.10);
  float mo=-.635+.10*q.x*q.x;                                                                          // the lips meet
  d+=(.034*gs((p.y-mo+jd*.3)/.030)-.030*gs((p.y-mo-.085)/.07)-.036*gs((p.y-mo+.10+jd*.7)/.06))*smoothstep(.50*HS[2],.34*HS[2],q.x)*smoothstep(.45,.75,p.z)*(1.-.85*min(1.,jaw*2.5));
  return d*.90;
}
// cheek ruff and nape: layers of locks round the face, swept back and down
float lockD(vec3 q,vec3 a,vec3 b,vec3 c,float r){return smin(sCone(q,a,b,r,r*.72),sCone(q,b,c,r*.72,.012),r*.5);}
float vRuff(vec3 p){
  float bd=length((p-vec3(0,-.40,-.25))*vec3(.80,.72,.85))-1.25-.3*HS[3];if(bd>.7) return bd;
  vec3 q=vec3(abs(p.x),p.yz);float L=HS[3],jd=jaw*.20;
  float far_=min(sCone(q,vec3(.62,.30,-.20),vec3(.70,-.50,-.30),.22,.34),sCone(q,vec3(.70,-.50,-.25),vec3(0,-1.04,.0),.34,.40));far_=min(far_,sEll(p-vec3(0,-.15,-.50),vec3(.90,1.20,.60)));if(far_>.62+.25*L) return far_-.50-.2*L;
  float d=sCone(q,vec3(.62,.30,-.14),vec3(.66,-.58,-.12),.22,.30);
  d=smin(d,sCone(q,vec3(.64,-.5,-.1),vec3(.14,-1.04-jd,.16),.28,.20),.2);
  for(int i=0;i<7;i++){float t=float(i)/6.;float a=mix(1.80,.06,t);                                       // temple .. chin
    vec2 o=vec2(sin(a)*.82,-.24-cos(a)*.80-jd*smoothstep(.5,1.,t));vec2 dr=normalize(vec2(sin(a)*1.1,-cos(a)*.75-.42));
    float l=L*(.40+.14*sin(t*11.+1.))*(i==6?.35+.95*HS[6]:1.);vec2 cv=vec2(0,-.10*l);
    d=smin(d,lockD(q,vec3(o*.88,.16-.04*t),vec3(o+dr*l*.45,-.04+.10*t),vec3(o+dr*l+cv,-.14+.24*t),.17),.040);}
  for(int i=0;i<6;i++){float t=float(i)/5.;float a=mix(1.62,.22,t);
    vec2 o=vec2(sin(a)*.84,-.26-cos(a)*.80-jd*smoothstep(.5,1.,t));vec2 dr=normalize(vec2(sin(a)*1.1,-cos(a)*.6-.65));float l=L*(.56-.12*t);
    d=smin(d,lockD(q,vec3(o*.90,-.14-.05*t),vec3(o+dr*l*.45,-.34+.1*t),vec3(o+dr*l-vec2(0,.10*l),-.50+.24*t),.20),.045);}
  float nk=sEll(p-vec3(0,.06,-.36),vec3(.86,.98,.66));                                                // nape
  for(int j=0;j<2;j++)for(int i=0;i<4;i++){float fi=float(i),fj=float(j);float x=.11+.215*fi-.08*fj;vec3 o=vec3(x,-.42-.45*fj+.05*fi,-.86+.14*fi*fi*.35+.06*fj);
    nk=smin(nk,lockD(q,o,o+vec3(.05+.03*fi,-.34,-.10),o+vec3(.09+.07*fi,-.66-.10*fj*L+.05*fi,-.22),.20),.05);}
  return smin(d,nk,.10)*.95;
}
vec2 vEars(vec3 p){                           // y: 1 inside the shell
  vec3 q=vec3(abs(p.x),p.yz)-vec3(.97,.16,-.10);float bd=length(q)-.5*HS[4];if(bd>.4) return vec2(bd,0);
  q/=HS[4];q.xz=rot(.62)*q.xz;q.xy=rot(.16)*q.xy;
  float e=sEll(q,vec3(.33,.36,.115));float in_=sEll(q-vec3(.03,-.01,.12),vec3(.22,.25,.115));
  float d=smax(e,-in_,.05);d=smin(d,sEll(q-vec3(.02,-.02,-.01),vec3(.16,.18,.05)),.05);
  return vec2(d*HS[4],smoothstep(.05,.0,in_)*step(-.06,q.z));
}
vec2 ringKundala(vec3 p){
  vec3 q=vec3(abs(p.x),p.yz)-vec3(1.10+.10*(HS[4]-1.),-.44,.04);float bd=length(q)-.40;if(bd>.3) return vec2(bd,3.);
  q.xz=rot(.45)*q.xz;float d=length(vec2(length(q.xy)-.205,q.z))-.058;vec3 b=polar(q.xzy,10.,0.);d=min(d,length(b-vec3(0,0,.275))-.043);
  return U(vec2(d,3.),vec2(length(q-vec3(0,-.205,.0))-.095,4.));
}
// ---------------------------------------------------------------- fur drawn on the surface
// short tapering strokes scattered in a bone's own space so that they ride with it.  x: ink 0..1, y: signed tilt of the hair, z: tone
vec3 furS(vec3 p,vec3 n,vec3 F,float cell,float wd){
  F=normalize(F-n*dot(F,n)+1e-4);vec3 X=cross(n,F),g=p/cell,ip=floor(g);float ink=0.,tl=0.,tn=0.;
  for(int k=-1;k<=1;k++)for(int j=-1;j<=1;j++)for(int i=-1;i<=1;i++){
    vec3 id=ip+vec3(i,j,k);float r=h31(id);vec3 o=g-id-vec3(r,h31(id+17.3),h31(id+41.7));
    if(abs(dot(o,n))>.5) continue;float a=dot(o,F),L=.38+.42*fract(r*7.3),u=a/L*.5+.5;if(u<0.||u>1.) continue;
    float x=abs(dot(o,X)+(fract(r*13.7)-.5)*.9*a*a);float tp=min(u*5.,1.)*(1.-u)*1.6;
    ink=max(ink,(1.-smoothstep(wd*.45*tp,wd*tp+.01,x))*step(.10,fract(r*5.1)));
    float w2=(1.-smoothstep(.02,.20*(1.-u)+.06,x));tl+=(fract(r*3.7)-.5)*w2;tn=max(tn,w2*fract(r*9.1));}
  return vec3(ink,tl,tn);
}
struct FB{float d;vec3 lp,ln,F;mat3 M;};
void fbone(inout FB b,vec3 p,vec3 n,vec3 a,vec3 c,vec3 f,float r){
  float d=length(p-mix(a,c,segT(p,a,c)))-r;if(d>b.d) return;vec3 y=normalize(a-c);vec3 z=normalize(f-y*dot(f,y)),x=cross(y,z);mat3 M=transpose(mat3(x,y,z));
  b.d=d;b.M=M;b.lp=M*(p-a)+a.x*0.;b.ln=M*n;b.F=vec3(0,-1,0);
}
FB furBone(vec3 p,vec3 n){
  FB b;vec3 c=Bc*(p-J[1]);b.d=sEll(c-vec3(0,-.5,0),vec3(1.6*B[0],2.6,1.1))+.0;b.lp=c;b.ln=Bc*n;b.M=Bc;b.F=normalize(vec3(sign(c.x)*.35*smoothstep(0.,.8,abs(c.x)),-1.,0.));
  float A=B[5],L=B[6];vec3 fl=armF(J[4],J[5],J[6]),fr=armF(J[7],J[8],J[9]),kl=legK(J[10],J[11],J[12]),kr=legK(J[14],J[15],J[16]);
  fbone(b,p,n,J[4],J[5],fl,.62*A);fbone(b,p,n,J[5],J[6],fl,.40*A);fbone(b,p,n,J[7],J[8],fr,.62*A);fbone(b,p,n,J[8],J[9],fr,.40*A);
  fbone(b,p,n,J[10],J[11],kl,.72*L);fbone(b,p,n,J[11],J[12],kl,.44*L);fbone(b,p,n,J[14],J[15],kr,.72*L);fbone(b,p,n,J[15],J[16],kr,.44*L);
  return b;
}
// bare palms and fingers, soles and toes: 0 fur .. 1 skin;  crease = ink of palm lines and nails
float handSkin(vec3 p,out float crease,out float nail){
  crease=0.;nail=0.;float sk=0.;
  for(int k=0;k<2;k++){vec3 w=k==0?J[6]:J[9];float hs=B[7];if(length(p-w)>2.1*hs||handD(p,k)>.07) continue;vec3 l=(k==0?BL:BR)*(p-w)/hs;
    float jag=.10*abs(fract(l.x*4.2)-.5)+.05*vn(l.xy*9.);
    float m=max(l.z*2.2+.10+min(0.,l.y-.02)*.8,l.y-.66);m=max(m,abs(l.x)*1.4-.50+max(0.,l.y-.25)*.4);m=min(m,l.y*2.+.40);
    sk=max(sk,smoothstep(-.01,.03,m-jag));
    if(l.z>.05&&l.y<.95){vec2 q=l.xy;
      crease=max(crease,lineA(length(q-vec2(.42,.30))-.40-.05*q.y,.016)*step(q.x,.22)*step(.02,q.y)*step(q.y,.66));
      crease=max(crease,lineA(q.y-.52+.16*q.x-.10*q.x*q.x,.015)*step(-.26,q.x)*step(q.x,.20));
      crease=max(crease,lineA(q.y-.66-.22*q.x*q.x+.10*q.x,.015)*step(-.30,q.x)*step(q.x,.16));}
    for(int f=0;f<5;f++){int i=k*20+f*4;vec3 a=HF[i+2].xyz,b=HF[i+3].xyz,ax=normalize(b-a);vec3 o=p-b;float r=HF[i+3].w;
      vec3 bk=f==0?normalize(cross(ax,cross(ax,(k==0?transpose(BL):transpose(BR))*vec3(.55,0,.8)))):normalize(cross(ax,cross(ax,(transpose(k==0?BL:BR))*vec3(0,.0,1.)+ax*.4)));
      float up=dot(o,bk),al=dot(o,ax);vec3 x=o-bk*up-ax*al;float sdw=length(x);
      if(up>r*.30){float e=max(sdw-r*.72,max(abs(al+r*.20)-r*.95,0.)-r*.02);float ee=length(vec2(sdw/(r*.74),max(abs(al+.2*r)-r*.3,0.)/(r*.70)));nail=max(nail,smoothstep(1.02,.90,ee));crease=max(crease,smoothstep(.16,.04,abs(ee-1.))*.9);}
      for(int j=1;j<3;j++){vec3 jn=HF[i+j].xyz,dx=normalize(HF[i+j+1].xyz-HF[i+j-1].xyz);vec3 oj=p-jn;float rj=HF[i+j].w;if(length(oj)<rj*1.25&&dot(oj,bk)<-rj*.2) crease=max(crease,lineA(dot(oj,dx),rj*.16)*.8);}}
  }
  return sk;
}
float footSkin(vec3 p,out float nail){
  float sk=0.;nail=0.;
  for(int k=0;k<2;k++){vec3 an=k==0?J[12]:J[16],he=k==0?J[18]:J[19],to=k==0?J[13]:J[17];float s=B[6];if(length(p-mix(he,to,.5))>1.9*s||hFoot(p,an,he,to,s,k==0?1.:-1.)>.07) continue;
    vec3 f=normalize(to-he),u=normalize(an-mix(he,to,.2));u=normalize(u-f*dot(u,f));vec3 sd=cross(f,u)*(k==0?1.:-1.);
    vec3 o=p-to;float x=dot(o,sd)/s,y=dot(o,u)/s,z=dot(o,f)/s;
    float m=max(-y-.06-max(0.,-z-1.2)*.1,z+.34);sk=max(sk,smoothstep(-.02,.04,m-.10*abs(fract(x*5.)-.5)));
    for(int i=0;i<5;i++){float fk=float(i),big=i==0?1.:0.;vec3 c=to+f*(.06-.085*fk+.02*big)*s+sd*(.295-.150*fk+.05*big)*s-u*.06*s;float r=(.080+.030*big)*s;vec3 q=p-c;float up=dot(q,u);
      if(up>r*.35){float ee=length(vec2(dot(q,sd)/(r*.66),(dot(q,f)+r*.05)/(r*.80)));nail=max(nail,smoothstep(1.02,.9,ee));}}}
  return sk;
}
// short dhoti of red cloth drawn tight round the thighs
float dhE=.56;                                // how far down the thigh it reaches
float dhoti(vec3 p,out vec3 loc){
  vec3 q=Bp*(p-J[0]);loc=vec3(0);
  float bd=length(q-vec3(0,-.7,0))-3.4;if(bd>.6) return bd;
  float L=B[6];vec3 aL=J[10],kL=J[11],aR=J[14],kR=J[15];float tl=segT(p,aL,kL),tr=segT(p,aR,kR);float dl=length(p-mix(aL,kL,tl)),dr=length(p-mix(aR,kR,tr));bool lf=dl<dr;
  vec3 h=lf?aL:aR,k=lf?kL:kR,ax=normalize(k-h),z=normalize(pZ-ax*dot(pZ,ax)+1e-3),x=cross(ax,z),o=p-h;float an=atan(dot(o,x),dot(o,z)),u=dot(o,ax)/length(k-h);
  loc=vec3(u,an,lf?0.:1.);
  float fo=.040*sin(an*8.+u*4.)*smoothstep(.0,.45,u)+.016*sin(an*19.-u*9.)*smoothstep(.1,.5,u);
  vec3 kk=lf?legK(J[10],J[11],J[12]):legK(J[14],J[15],J[16]);kk=normalize(kk-ax*dot(kk,ax)*.8);
  float e=dhE;float d1=sCone(p,aL,mix(aL,kL,e),.77*L,.84*L),d2=sCone(p,aR,mix(aR,kR,e),.77*L,.84*L);
  float d=min(d1,d2);d=smin(d,sCone(p,mix(h,k,.22)+kk*.15*L,mix(h,k,e)+kk*.17*L,.70*L,.70*L),.2);
    d=smin(d,sEll(q-vec3(0,-.16,-.06),vec3(1.15*B[4],.92,.98)),.34)-fo-.02;
  d=smax(d,(u-e)*length(k-h)-.02*sin(an*8.+1.),.03);
  return max(d,q.y-.50-max(0.,u-.06)*7.)*.82;
}
void fur(inout Surf s,vec3 lp,vec3 n,vec3 ln,vec3 F,mat3 M,float cell,float amt){
  vec3 f=furS(lp,ln,F,cell,.075);float cl=smoothstep(.35,.65,vn3(lp*1.3+3.));
  s.ns=normalize(n+transpose(M)*(normalize(F-ln*dot(F,ln)+1e-4)*f.y*.75));
  s.base=mix(s.base,s.base*vec3(1.10,1.10,1.0),f.z*.5*amt);s.base=mix(s.base,s.sh*1.35,f.x*(.22+.60*cl)*amt);s.sh=mix(s.sh,s.sh*.50,f.x*(.3+.6*cl)*amt);
}
#ifdef VANARA_LIB
#define HAIRLINE (.56+.05*cos(h.x*9.))
#else
#define HAIRLINE .85           // under the crown
#endif
void bodySurf(vec3 p,vec3 n,inout Surf s){
    s.part=1.;FB b=furBone(p,n);vec3 c=Bc*(p-J[1]),pl=Bp*(p-J[0]);
    float jg=.16*vn(b.lp.xy*vec2(7.,2.))+.10*vn(b.lp.zy*vec2(8.,2.5));
    float fr=smoothstep(.15,.55,c.z)*smoothstep(1.55,1.1,c.y);float lt=smoothstep(.0,.07,(.92-.10*c.y-abs(c.x)*(.80+.12*c.y))+jg-.12)*fr*step(-3.1,c.y);
    if(dot(c,c)>9.) lt=0.;
    float arm=min(length(p-mix(J[5],J[6],segT(p,J[5],J[6]))),length(p-mix(J[8],J[9],segT(p,J[8],J[9]))));lt*=smoothstep(.65,.9,arm);
    s.base=mix(s.base,Pb[14],lt);s.sh=mix(s.sh,Ps[14],lt);
    fur(s,b.lp,n,b.ln,b.F,b.M,.235,mix(1.,.5,lt));
    float cr,nl,nl2;float sk=handSkin(p,cr,nl);float fs=footSkin(p,nl2);sk=max(sk,fs);nl=max(nl,nl2);
    s.base=mix(s.base,Pb[11],sk);s.sh=mix(s.sh,Ps[11],sk);s.ns=normalize(mix(s.ns,n,sk));
    s.base=mix(s.base,hex(0xf7d0a8),nl*.8);s.sh=mix(s.sh,hex(0xa8605a),nl*.8);s.base=mix(s.base,hex(0x5c1420),cr*sk*.85);s.sh=mix(s.sh,hex(0x34081a),cr*sk*.85);
    if(sk>.5) s.part=14.;
    if(c.z>0.&&sk<.5&&arm>.75){vec2 q=vec2(abs(c.x),c.y);float k=0.;
      vec2 a=q-vec2(.78,.60);float r=length(a*vec2(.86,1.08)),an=atan(a.x,-a.y);k=max(k,lineA(r-.66,.050*smoothstep(2.0,.1,abs(an-.15)))*step(a.y,.2)*step(.05,q.x));
      k=max(k,lineA(q.x,.026)*step(-.02,q.y)*step(q.y,.70));
      k=max(k,lineA(q.y-1.28-.10*q.x-.04*sin(q.x*3.),.026)*smoothstep(.12,.24,q.x)*smoothstep(1.35,.8,q.x)*.8);
      vec3 a0=J[0]+pY*.10,b0=J[1]-cY*.35;float t=segT(p,a0,b0);vec3 o=p-mix(a0,b0,t);float x=mix(dot(o,pX),dot(o,cX),t);
      float ab=0.;ab=max(ab,lineA(x,.026)*step(.02,t)*step(t,.97));for(int i=0;i<3;i++){float y=.30+.26*float(i);ab=max(ab,lineA(t-y-.10*x*x,.010)*smoothstep(.60,.40,abs(x)));}
      ab=max(ab,lineA(abs(x)-.66-.12*(t-.5),.022)*smoothstep(.95,.7,t)*step(.05,t)*.8);
      k=max(k,ab*smoothstep(.2,.6,c.z)*step(c.y,-.2)*(1.-min(1.,B[9]*1.6)));
      s.base=mix(s.base,s.sh*.55,k*.85);s.sh=mix(s.sh,s.sh*.35,k*.85);}
  }
void headSurf(vec3 p,vec3 n,inout Surf s){vec3 h=Hd(p);
    s.part=1.;vec3 ln=Bh*n;
    vec2 k=vec2(1,-1)*.03;vec3 nb=normalize(k.xyy*vHeadBase(h+k.xyy)+k.yyx*vHeadBase(h+k.yyx)+k.yxy*vHeadBase(h+k.yxy)+k.xxx*vHeadBase(h+k.xxx));
    float ax=abs(h.x);
    float an=atan(ax,-h.y-.2);float jg=.085*abs(fract(an*4.6+.35*sin(an*5.))-.5)*2.+.05*abs(fract(an*9.7)-.5)-.02;
    float fm=min(.80-.085*smoothstep(-.35,-.05,h.y)-.02*smoothstep(.1,.5,h.y)-ax,h.y+1.06+jaw*.26)-jg*.8;fm=min(min(fm,h.z-.20-.16*smoothstep(-.3,-.9,h.y)-jg),HAIRLINE-h.y-jg);
    float face=smoothstep(.0,.022,fm);
    vec3 F=normalize(vec3(h.x*1.3,h.y*.5-.25,-1.));
    float ck=smoothstep(.30,.0,h.y+.12*vn(h.yz*9.));s.base=mix(Pb[1],Pb[2],ck);s.sh=mix(Ps[1],Ps[2],ck);if(face<.995) fur(s,h,n,ln,F,Bh,.115,1.);
    s.base=mix(s.base,Pb[11],face);s.sh=mix(s.sh,Ps[11],face);
    s.ns=normalize(mix(s.ns,normalize(mix(n,transpose(Bh)*nb,.84)),face));
    if(face>.5) s.part=15.;
    vec4 d=faceDecal(h);float v=face*smoothstep(.05,.25,h.z);s.base=mix(s.base,d.rgb,d.a*v);s.sh=mix(s.sh,d.rgb*vec3(.50,.42,.55),d.a*v);if(d.a*v>.5&&lum(d.rgb)<.05) s.cls=5.;
  }
void ruffSurf(vec3 p,vec3 n,inout Surf s){vec3 h=Hd(p);vec3 ln=Bh*n;vec2 rd=vec2(h.x,h.y+.2);vec3 F=normalize(vec3(rd*vec2(1.,.8)-vec2(0,.5),-.9));
    float bk=max(smoothstep(-.25,-.6,h.z),smoothstep(.40,.62,h.y));s.base=mix(s.base,Pb[1],bk);s.sh=mix(s.sh,Ps[1],bk);
    fur(s,h,n,ln,F,Bh,.14,1.);s.ink=.75;s.part=1.;}
void earSurf(vec3 p,vec3 n,inout Surf s){vec3 h=Hd(p);vec2 e=vEars(h);if(e.y>.5){s.base=Pb[11]*.85;s.sh=Ps[11];}else{vec3 ln=Bh*n;s.base=Pb[1];s.sh=Ps[1];fur(s,h,n,ln,vec3(sign(h.x)*.7,.4,-.6),Bh,.12,.8);}}
#ifndef VANARA_LIB
// ================================================================ HANUMAN
vec2 mukut(vec3 p){                              // a low, round, lobed crown
  float bd=length(p-vec3(0,1.0,0))-1.45;if(bd>.5) return vec2(bd,3.);
  vec3 c=p-vec3(0,.16,-.11);c.yz=rot(.12)*c.yz;c.xz/=vec2(.99,1.05);float r=length(c.xz),a=atan(c.x,c.z);
  float d=max(abs(r-.83)-.045,abs(c.y-.57)-.105)-.02;
  d=min(d,sTor(c-vec3(0,.455,0),.845,.045));d=min(d,sTor(c-vec3(0,.69,0),.84,.042));
  vec3 g=polar(c,26.,0.);float gem=sEll(g-vec3(0,.572,.885),vec3(.052,.062,.04));
  float lob=abs(sin(a*7.));vec3 dm=c-vec3(0,.66,0);float dome=sEll(dm,vec3(.80,.58,.80));dome=max(dome,-dm.y)-.030*sqrt(lob)*smoothstep(.72,.30,dm.y);d=min(d,dome*.8);
  vec3 q=polar(c,14.,0.)-vec3(0,.83,.79);q.yz=rot(-.36)*q.yz;float pet=sEll(q,vec3(.155,.19,.05));d=min(d,max(pet,-sEll(q-vec3(0,-.02,.05),vec3(.095,.13,.045))));
  float gem2=sEll(q-vec3(0,-.02,.02),vec3(.05,.075,.04));
  d=min(d,sTor(c-vec3(0,1.17,0),.36,.055));d=min(d,sEll(c-vec3(0,1.31,0),vec3(.29,.17,.29)));d=min(d,sTor(c-vec3(0,1.45,0),.14,.035));d=min(d,sEll(c-vec3(0,1.55,0),vec3(.115,.105,.115)));d=min(d,sCone(c,vec3(0,1.60,0),vec3(0,1.78,0),.06,.008));
  vec3 f=p-vec3(0,1.02,.84);f.yz=rot(-.24)*f.yz;float ed=length(vec2(abs(f.x)+.10*max(0.,f.y)*1.,f.y*.80));
  float pl=sEll(f,vec3(.31,.42,.07));pl=max(pl,-sEll(f-vec3(0,0,.07),vec3(.225,.325,.05)));d=min(d,pl);
  gem=min(gem,sEll(f-vec3(0,-.05,.05),vec3(.115,.165,.06)));d=min(d,sTor((f-vec3(0,-.05,.03)).xzy*vec3(1.,1.,.72),.145,.028));
  for(int i=0;i<7;i++){float t=float(i)/6.*4.4-2.2+1.5708;gem2=min(gem2,length(f-vec3(cos(t)*.265,sin(t)*.36,.045))-.034);}
  vec3 w=vec3(abs(p.x),p.yz)-vec3(.86,.92,.10);w.xz=rot(-1.15)*w.xz;d=min(d,max(sEll(w,vec3(.20,.31,.06)),-sEll(w-vec3(0,0,.06),vec3(.13,.23,.045))));gem=min(gem,sEll(w-vec3(0,-.02,.03),vec3(.07,.11,.05)));
  return U(U(vec2(d*.95,3.),vec2(gem,4.)),vec2(gem2,5.));
}
vec2 ornaments(vec3 p,float td){
  vec3 c=Bc*(p-J[1]);vec2 m=vec2(1e3,3.);
  if(td<.7){
    m=U(m,vec2(beadsD(c,td,vec2(0,1.72),.80,.070,38.),6.));
    m=U(m,vec2(beadsD(c,td,vec2(0,1.72),1.10,.080,-1.),3.));m=U(m,vec2(beadsD(c,td,vec2(0,1.72),1.10,.075,32.)-.005,4.));m=U(m,vec2(beadsD(c,td,vec2(0,1.72),1.30,.060,48.),3.));
    m=U(m,vec2(beadsD(c,td,vec2(0,1.62),2.10,.080,58.),3.));
    float pt=td-.03;vec3 pd=c-vec3(0,-.48,0);m=U(m,vec2(max(length(vec2(length(pd.xy*vec2(1.,.82))-.17,pt))-.07,-c.z),3.));m=U(m,vec2(max(sEll(vec3(pd.xy,pt-.02),vec3(.16,.20,.10)),-c.z),4.));
    for(int i=-2;i<=2;i++){float x=float(i)*.16;m=U(m,vec2(max(sEll(vec3(c.x-x,c.y+.80-.06*abs(float(i)),pt),vec3(.055,.10,.06)),-c.z),3.));}
    vec3 n=normalize(vec3(-.62,.78,0.));m=U(m,vec2((length(vec2(dot(c-vec3(.0,.05,0),n)+.035*sin(c.y*2.),td-.01))-.042)*.9,9.));
  }
  return m;
}
vec2 map(vec3 p){
  float td=hTorso(p),sk=hLimbs(p,td);sk=smin(sk,hNeck(p),.20);sk=smin(sk,hTufts(p),.09);
  vec2 m=vec2(sk,1.);
  float dh=length(p-J[3]);
  if(dh-2.6*HS[0]<m.x){vec3 h=Hd(p);float S=HS[0];
    float hd=vHead(h)*S;vec2 e=vEars(h);float ru=vRuff(h)*S;
    m=U(m,vec2(hd,12.));m=U(m,vec2(ru,2.));m=U(m,vec2(e.x*S,13.));
    vec2 k=mukut(h);m=U(m,vec2(k.x*S,k.y));k=ringKundala(h);m=U(m,vec2(k.x*S,k.y));}
  m=U(m,ornaments(p,td));
  vec3 loc;m=U(m,vec2(dhoti(p,loc),7.));
  vec3 q=Bp*(p-J[0]);
  float bq=length(q-vec3(0,.2,0))-2.4;
  if(bq<m.x){
    float be=ringD(vec3(q.x,q.y-.50,q.z*1.14),vec3(0),vec3(0,1,0),1.03*B[3]+.06,.15,.07);m=U(m,vec2(be*.85,3.));
    vec3 rq=vec3(q.x,q.y-.50,q.z*1.14);vec3 pb=polar(rq,22.,0.);m=U(m,vec2(length(pb-vec3(0,0,1.03*B[3]+.15))-.085,4.));
    vec3 b=q-vec3(0,.50,1.02);m=U(m,vec2(max(length(b.xy)-.30,abs(b.z)-.09)-.03,3.));m=U(m,vec2(sTor(b.xzy-vec3(0,.09,0),.235,.045),3.));m=U(m,vec2(sEll(b-vec3(0,0,.10),vec3(.14,.14,.10)),4.));
    vec3 pz=polar(vec3(q.x,q.y,q.z*1.10),18.,0.);m=U(m,vec2(length(pz-vec3(0,.20-.04*0.,1.17))-.07,3.));
  }
  vec3 a=J[0]+pY*.36+pZ*.98,kn=.5*(J[11]+J[15]);vec3 dn=normalize(mix(normalize(kn-J[0]),-pY,.35));vec3 b=a+dn*2.35+pZ*.22+Wind*.5;vec2 pl;
  if(length(p-mix(a,b,.5))-1.9<m.x){float dp=pleatD(p,a,b,.24,.42,pl);m=U(m,vec2(dp,8.));}
  for(int s=0;s<2;s++){vec3 e0=s==0?J[4]:J[7],e1=s==0?J[5]:J[8],e2=s==0?J[6]:J[9];float A=B[5];
    if(length(p-e1)-3.2<m.x){vec3 u=normalize(e1-e0),v=normalize(e2-e1);vec3 f=armF(e0,e1,e2);
      vec3 ac=mix(e0,e1,.40);float r1=ringD(p,ac,u,.50*A,.11,.05);m=U(m,vec2(r1,3.));
      vec3 ox=p-ac;float y=dot(ox,u);vec3 rr=normalize(normalize(ac-J[1]-u*dot(ac-J[1],u))+cZ*.6);rr=normalize(rr-u*dot(rr,u));vec3 pq=ox-rr*(.52*A);float px=dot(pq,cross(u,rr));float pr_=dot(pq,rr);
      m=U(m,vec2(sEll(vec3(px,y+.06*smoothstep(-.3,.3,y),pr_+.06),vec3(.29,.38,.13)),3.));m=U(m,vec2(sEll(vec3(px,y+.04,pr_-.05),vec3(.12,.17,.08)),4.));
      float r2=ringD(p,mix(e1,e2,.86),v,.275*A,.19,.035);m=U(m,vec2(r2,3.));vec3 bc=mix(e1,e2,.86);m=U(m,vec2(ringD(p,bc-v*.21,v,.30*A,.03,.05),3.));m=U(m,vec2(ringD(p,bc+v*.21,v,.275*A,.03,.05),3.));}
    vec3 l0=s==0?J[11]:J[15],l1=s==0?J[12]:J[16];
    if(length(p-l1)-1.6<m.x){vec3 v=normalize(l1-l0);vec3 bc=mix(l0,l1,.90);vec3 o=p-bc;float y=dot(o,v);m=U(m,vec2(length(vec2(length(o-v*y)-.33*B[6],y))-.095,3.));m=U(m,vec2(length(vec2(length(o-v*y)-.31*B[6],y+.16))-.06,3.));vec3 x0=normalize(cross(v,vec3(.3,.1,1.))),z0=cross(v,x0);vec3 pp=polar(vec3(dot(o,x0),y-.13,dot(o,z0)),12.,0.);m=U(m,vec2(length(pp-vec3(0,0,.34*B[6]))-.075,3.));}}
  return m;
}
void surf(vec3 p,vec3 n,int m,inout Surf s){
  if(m==1) bodySurf(p,n,s);
  if(m==12) headSurf(p,n,s);
  if(m==2) ruffSurf(p,n,s);
  if(m==13) earSurf(p,n,s);
  if(m==7){vec3 loc;dhoti(p,loc);float u=loc.x,a=loc.y;float bd=smoothstep(.435,.445,u);
    s.base=mix(s.base,hex(0xe8a42c),bd);s.sh=mix(s.sh,hex(0x8a4214),bd);
    float ln=step(.5,fract(u*50.))*step(.415,u)*step(u,.46);s.base=mix(s.base,hex(0xffe08a),ln*.8);
    vec2 f=fract(vec2(a*3.82,(u-.505)*14.+.5))-.5;s.base=mix(s.base,hex(0xb0182a),smoothstep(.34,.26,length(f*vec2(1.,.8)))*step(.465,u)*step(u,.545));
    vec2 g=fract(vec2(a*2.9,u*9.))-.5;s.base=mix(s.base,hex(0xf0a83a),smoothstep(.17,.12,length(g*vec2(1.,1.4)))*step(u,.405)*step(.02,u)*.8);
    float fl=sin(a*8.+u*4.);s.base*=1.-.20*smoothstep(.5,.95,-fl)*smoothstep(.05,.3,u);s.ink=.8;}
  if(m==8){vec3 a=J[0]+pY*.36+pZ*.98,kn=.5*(J[11]+J[15]);vec3 dn=normalize(mix(normalize(kn-J[0]),-pY,.35));vec3 b=a+dn*2.35+pZ*.22+Wind*.5;vec2 pl;pleatD(p,a,b,.24,.42,pl);
    float bd=smoothstep(.80,.815,pl.x);s.base=mix(s.base,hex(0xe8a42c),bd);s.sh=mix(s.sh,hex(0x8a4214),bd);float ln=step(.5,fract(pl.x*40.))*step(.77,pl.x)*step(pl.x,.83);s.base=mix(s.base,hex(0xffe08a),ln);
    s.base*=1.-.16*smoothstep(.3,.9,sin(pl.y*14.+1.6));}
}
#endif
