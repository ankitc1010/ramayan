// SITA, and the body, cloth and hand-painting shared with people.glsl (which defines CAST_LIB and includes this file).
// look 0 = bride, 1 = forest, 2 = grove
// ---------------------------------------------------------------- body
float femTorso(vec3 p){
  vec3 c=Bc*(p-J[1]),h=Bp*(p-J[0]),q=vec3(abs(c.x),c.yz);
  float d=sEll(c-vec3(0,-.06,-.07),vec3(1.00*B[0],1.12,.73*B[1]));
  d=smin(d,sCone(q,vec3(.10,1.10,-.16),vec3(1.30*B[11],.90,-.15),.22,.33),.44);
  d=smin(d,sEll(q-vec3(.40*B[0],.03,.44*B[1]),vec3(.40,.43,.40)*(.62+.38*B[8])),.24);
  vec3 a=J[0]+pY*.15,b=J[1]-cY*.50;float t=segT(p,a,b);vec3 o=p-mix(a,b,t),l=mix(Bp*o,Bc*o,t);
  float w=mix(B[3]*.80,B[2]*.76,smoothstep(.1,1.,t));float wa=(length(l*vec3(1.,1.,1.22))-w)*.82;
  wa-=B[9]*.28*exp(-pow((t-.35)*2.6,2.))*smoothstep(-.2,.8,l.z);
  d=smin(d,wa,.46);
  d=smin(d,sEll(h-vec3(0,-.12,-.06),vec3(1.02*B[4],.82,.80)),.42);
  d=smin(d,sCone(q,vec3(.10,1.10,.16),vec3(.95*B[11],1.06,-.02),.04,.04),.14);
  return d;
}
float femNeck(vec3 p){
  float d=sCone(p,J[2]-cY*.35,J[3]-hY*.70-hZ*.17,.40*B[10],.345*B[10]);
  vec3 c=Bc*(p-J[2]);vec3 q=vec3(abs(c.x),c.yz);
  return smin(d,sCone(q,vec3(.08,.02,-.12),vec3(.72*B[11],-.38,-.08),.22,.16),.36);
}
// a foot with a drawn big toe; side +1 left, -1 right
float toesD(vec3 p,vec3 an,vec3 heel,vec3 toe,float s,float side){
  vec3 f=normalize(toe-heel),sd=normalize(cross(f,vec3(0,1,.02)))*side,up=cross(sd,f)*side;
  float d=sCone(p,an,mix(an,heel,.7),.22*s,.24*s);
  d=smin(d,length(p-heel)-.235*s,.14);
  d=smin(d,sCone(p,mix(an,heel,.35)+f*.1,toe-f*.38*s+sd*.06*s,.24*s,.15*s),.18);
  d=smin(d,sCone(p,heel,toe-f*.40*s-sd*.05*s,.19*s,.17*s),.14);
  d=smin(d,sCone(p,toe-f*.36*s+sd*.15*s-up*.04*s,toe-f*.50*s-sd*.17*s-up*.05*s,.135*s,.12*s),.12);
  for(int i=0;i<5;i++){float k=float(i);float x=i==0?.19:.085-.105*(k-1.),l=i==0?.06:.07-.075*(k-1.),r=i==0?.098:.080-.006*k;
    d=smin(d,sCone(p,toe+f*(l-.30)*s+sd*x*s,toe+f*l*s+sd*(x+(i==0?-.01:.0))*s-up*.075*s,r*s*.95,r*s),.035);}
  return d;
}
// ---------------------------------------------------------------- saree: wrapped skirt to the ankles; sinks into a pool when the figure sits on the ground
vec3 hemDir(vec3 kn,vec3 an){vec3 e=normalize(an-kn+vec3(0,-.02,0)),f=J[12]-J[16];float l=length(f);f/=l;float k=dot(e,f);return normalize(e-f*k*smoothstep(.75,.45,abs(k))*smoothstep(.3,1.,l));}   // the hem tilts with the feet
float sariD(vec3 p,float hem,out vec4 loc){     // loc: x = height above the hem, y = angle round the legs, z = pooled, w = 0 waist .. 1 hem
  vec3 hp=J[0]-pY*.05,kn=.5*(J[11]+J[15]),an=.5*(J[12]+J[16]);
  float pool=smoothstep(4.0,2.0,J[0].y);
  vec3 ax=normalize(an-hp);float L=length(an-hp),uu=clamp(dot(p-hp,ax)/L,0.,1.15);
  p-=Wind*uu*uu*.8;
  float tk=segT(p,hp,kn),ta=segT(p,kn,an+normalize(an-kn)*.8);vec3 k1=p-mix(hp,kn,tk),k2=p-mix(kn,an+normalize(an-kn)*.8,ta);
  vec3 sx=normalize(cross(ax,pZ+vec3(1e-3))),sz=cross(sx,ax),o=mix(k1,k2,smoothstep(-.8,.8,dot(p-kn,ax)));float ang=atan(-dot(o,sx),dot(o,sz));
  vec3 q=Bp*(p-J[0]);
  vec3 ed=hemDir(kn,an);
  float dl=smin(sCone(p,J[10],J[11],.60*B[4],.44),sCone(p,J[11],J[12]+ed*.35,.42,.90),.3);
  float dr=smin(sCone(p,J[14],J[15],.60*B[4],.44),sCone(p,J[15],J[16]+ed*.35,.42,.90),.3);
  float ce=smin(sCone(p,hp,kn,.88*B[4],.64),sCone(p,kn,an+ed*.35,.58,1.75),.5);
  float d=smin(smin(dl,dr,.7),ce,.6);
  d=smin(d,sEll(q-vec3(0,-.16,-.06),vec3(1.06*B[4],.92,.88)),.40);
  float front=exp(-ang*ang*5.)*smoothstep(.02,.22,uu);
  float fold=(.045*sin(ang*11.+uu*2.5)+.022*sin(ang*23.-uu*5.))*smoothstep(.10,.75,uu);
  float pl=abs(fract(ang*5.+.25)-.5)*2.;
  fold=mix(fold,(.05+.07*uu)*(pl-.3)+.05,front*(1.-pool));
  d-=fold*(1.-.94*pool);
  float lr=length(q.xz);d=smax(d,q.y-.46-2.5*max(0.,lr-1.15),.04);
  float ph=p.y-.02;
  if(pool>.01){
    vec2 C=.30*J[0].xz+.25*J[11].xz+.25*J[15].xz+.20*an.xz;vec2 e=p.xz-C;float a2=atan(e.x,e.y);
    float rr=1.+.07*sin(a2*5.+.6)+.05*sin(a2*9.)+.02*sin(a2*17.+1.);
    float sp=sEll(vec3(e.x,p.y-.02,e.y),vec3(3.05,.42,2.75)*rr*vec3(1,.9+.35*sin(a2*13.),1));
    d-=.045*pool*sin(a2*10.+1.2*sin(p.y*2.)+.7)*smoothstep(.7,1.9,length(e));
    d=smin(d,sp+(1.-pool)*2.5,.75);d=max(d,-p.y);
    ph=min(ph,mix(9.,(1.-length(e/vec2(3.05,2.75))/rr)*2.6+.02,smoothstep(.75,.25,p.y)));
    ang=mix(ang,a2,step(.5,pool));
  }
  float cut=dot(p-an,ed)-hem;d=smax(d,cut-.05*sin(ang*11.+2.)-8.*pool,.05);
  loc=vec4(pool>.5?ph:-cut,ang,pool,uu);
  return d*.80;
}
// ---------------------------------------------------------------- hands drawn close: x ink of creases and knuckles, y nails, z dyed fingertips.  old 0..1
vec3 handPaint(vec3 p,int k,float old){
  vec3 w=k==0?J[6]:J[9];mat3 M=k==0?BL:BR;float hs=B[7];vec3 l=M*(p-w)/hs;
  if(length(l-vec3(0,.6,0))>1.9||l.y<-.9) return vec3(0);
  mat3 T=transpose(M);float sg=k==0?-1.:1.;vec3 R=vec3(0);float best=1e3,bi=0.,bt=0.,br=1.;vec3 bo=vec3(0),ba=vec3(0,1,0),bp=vec3(0,0,1);int bs=0;float fin=0.;
  for(int f=0;f<5;f++){int i=k*20+f*4;for(int s=0;s<3;s++){vec3 a=HF[i+s].xyz,b=HF[i+s+1].xyz;float t=segT(p,a,b);vec3 o=p-mix(a,b,t);float r=mix(HF[i+s].w,HF[i+s+1].w,t),d=length(o)-r;
    if(d<best){best=d;bt=dot(p-a,normalize(b-a));br=r;bo=o;ba=normalize(b-a);bs=s;fin=length(b-a);vec3 pd=f==0?T*vec3(-.75,.25,.55):cross(T[0],ba)*sg;bp=normalize(pd-ba*dot(pd,ba));bi=float(f);}}}
  if(best<.05*hs){
    float dors=dot(normalize(bo+1e-5),-bp),lat=dot(bo,cross(ba,bp))/br;
    float j0=abs(bt),j1=abs(bt-fin);float near=min(bs==0?9.:j0,bs==2?9.:j1)/hs;
    R.x=max(R.x,lineA(near,.016)*smoothstep(-.1,-.4,dors)*.8);                      // creases inside the fingers
    float kn=near+.012*lat*lat;R.x=max(R.x,max(lineA(kn,.012),lineA(kn-.045,.011)*.8)*smoothstep(.45,.75,dors)*(.55+.45*old));
    if(old>.01) R.x=max(R.x,max(lineA(kn-.09,.010),lineA(abs(lat)-.55,.05)*step(near,.10)*.6)*smoothstep(.2,.6,dors)*old);
    if(bs==2){float y=(bt-fin*.62)/(fin*.46);float e=length(vec2(lat/.70,y>0.?y*.80:y));R.y=smoothstep(1.02,.90,e)*smoothstep(.15,.35,dors);R.x=max(R.x,lineA(e-.98,.10)*smoothstep(.15,.35,dors)*.8);}
    R.z=bs==2?smoothstep(.0,.06*hs,bt-.02+.02*sin(lat*6.)):0.;
  }
  if(l.y<1.0&&best>-.04*hs){
    if(l.z>.03){vec2 q=vec2(l.x,l.y);                                                // the three lines of the palm
      R.x=max(R.x,lineA(length((q-vec2(.36,.22))*vec2(1.,.92))-.36,.016)*step(q.x,.22)*smoothstep(.0,.12,q.y)*.75);
      R.x=max(R.x,lineA(q.y-.50-.20*q.x-.22*q.x*q.x,.014)*smoothstep(-.30,-.22,q.x)*smoothstep(.24,.18,q.x)*.7);
      R.x=max(R.x,lineA(q.y-.66+.16*q.x-.55*q.x*q.x*step(q.x,.1),.014)*smoothstep(-.30,-.26,q.x)*smoothstep(.16,.10,q.x)*.7);
      for(int i=0;i<2;i++)R.x=max(R.x,lineA(l.y+.06+.07*float(i)-.1*q.x*q.x,.012)*smoothstep(.20,.14,abs(q.x))*.6);
      if(old>.01) for(int i=0;i<6;i++){float a=h11(float(i)*3.1)*2.6;vec2 c=vec2(h11(float(i))-.5,h11(float(i)+7.)*1.4)*vec2(.5,.5)+vec2(0,.08);vec2 r=q-c;R.x=max(R.x,lineA(r.x*sin(a)+r.y*cos(a)+.04*sin(r.x*20.),.009)*smoothstep(.13,.05,length(r))*old*.7);}
    } else if(l.z<-.02){
      float ten=1e3;for(int f=0;f<4;f++){vec2 a=vec2(mix(-.12,.12,float(f)/3.),.08),b=vec2(.26-.17*float(f),.70);ten=min(ten,sSeg2(l.xy,a,b));}
      R.x=max(R.x,lineA(ten-.03,.012)*smoothstep(.10,.30,l.y)*smoothstep(.80,.55,l.y)*(.20+.75*old));
      if(old>.01){float w2=sin(l.y*62.+5.*vn(l.xy*7.));R.x=max(R.x,smoothstep(.80,.98,w2)*smoothstep(.42,.60,vn(l.xy*vec2(5.,9.)+3.))*old*.60);
        R.x=max(R.x,lineA(l.x-.08-.10*sin(l.y*6.+1.),.014)*smoothstep(.0,.2,l.y)*smoothstep(.6,.4,l.y)*old*.5);
        for(int i=0;i<4;i++)R.x=max(R.x,lineA(l.y+.10+.085*float(i)+.02*sin(l.x*14.+float(i)),.012)*smoothstep(.26,.12,abs(l.x))*old*.75);}
    }
  }
  return R;
}
// ---------------------------------------------------------------- head: a softer oval than headHuman, with a drawn profile
float femBase(vec3 p){
  float jd=jaw*.22,fl=HS[7];vec3 q=vec3(abs(p.x),p.yz);
  float d=sEll(p-vec3(0,.20,-.10),vec3(.75,.84,.86));
  d=smin(d,sEll(p-vec3(0,-.22*fl-jd*.4,.13),vec3(.56*HS[0],.70*fl+jd*.5,.61)),.26);
  d=smin(d,length(q-vec3(.295,-.27,.42))-.235*HS[4],.22);
  d=smin(d,sEll(p-vec3(0,-.56*fl-jd*.6,.42),vec3(.27,.25,.285)),.20);
  d=smin(d,sEll(p-vec3(0,-.85*fl-jd,.515),vec3(.155*HS[1],.135,.195)),.16);
  d=smin(d,sCone(q,vec3(.13,-.83*fl-jd,.40),vec3(.50*HS[0],-.40-jd*.6,-.04),.085,.15),.20);
  return d;
}
float femHead(vec3 p){
  float d=femBase(p);vec3 q=vec3(abs(p.x),p.yz);float nl=HS[2],jd=jaw*.20;
  d=smax(d,-(sEll(q-vec3(.31,.03,.87),vec3(.21,.12,.16))),.16);
  d=smin(d,sCone(q,vec3(.08,.17,.715),vec3(.44,.21,.54),.05*HS[5],.03*HS[5]),.12);
  float n=sCone(p,vec3(0,.12,.70),vec3(0,-.23*nl,.845),.046,.058*HS[3]);
  n=smin(n,length(p-vec3(0,-.275*nl,.862))-.062*HS[3],.06);
  n=smin(n,length(q-vec3(.088*HS[3],-.315*nl,.785))-.060*HS[3],.07);
  d=smin(d,n,.09);
  d=smin(d,sCone(p,vec3(0,-.36*nl,.725),vec3(0,-.50,.700),.05,.05),.08);
  float l=sCone(q,vec3(0,-.555,.728),vec3(.17,-.580,.655),.042*HS[6],.016);
  l=smin(l,sCone(q,vec3(0,-.645-jd,.715),vec3(.13,-.612-jd,.655),.050*HS[6],.018),.02);
  return smin(d,l,.05);
}
// smooth normals and painted decal on the face; returns how much of the point is head
float facePaint(vec3 p,vec3 n,inout Surf s){
  vec3 h=Bh*(p-J[3]);float isH=smoothstep(-1.14,-1.04,h.y)*step(length(h),1.45);
  if(isH>0.){vec2 k=vec2(1,-1)*.03;vec3 nb=normalize(k.xyy*femBase(h+k.xyy)+k.yyx*femBase(h+k.yyx)+k.yxy*femBase(h+k.yxy)+k.xxx*femBase(h+k.xxx));
    s.ns=normalize(mix(n,transpose(Bh)*nb,.82*isH*smoothstep(-.4,.2,h.z)));
    vec4 d=faceDecal(h);float v=isH*smoothstep(.02,.22,h.z);s.base=mix(s.base,d.rgb,d.a*v);s.sh=mix(s.sh,d.rgb*vec3(.60,.46,.52),d.a*v);
    if(d.a*v>.93&&abs(abs(h.x)-.36)<.30&&abs(h.y-.17)<.25){s.cls=6.;s.ns=n;}}   // eyes stay clear of highlights and cast shadows
  return isH;
}
// woven border: t 0 at the edge .. 1 inside, a = distance along it; 1 gold, 0 ground
float zari(float t,float a){
  float g=max(step(t,.10),max(step(.84,t)*step(t,.94),step(.18,t)*step(t,.23)));
  vec2 f=vec2(fract(a)-.5,(t-.53)*1.35);float dm=abs(f.x)+abs(f.y);g=max(g,step(dm,.40)*step(.16,dm)+step(dm,.08));
  return g;
}
// braid along three bones; returns distance
float braidD(vec3 p,vec3 a,vec3 b,vec3 c,vec3 e,float r0,float r1,float n,out float u){
  float t1=segT(p,a,b),t2=segT(p,b,c),t3=segT(p,c,e);vec3 o1=p-mix(a,b,t1),o2=p-mix(b,c,t2),o3=p-mix(c,e,t3);
  float l1=dot(o1,o1),l2=dot(o2,o2),l3=dot(o3,o3);float L1=length(b-a),L2=length(c-b),L3=length(e-c);vec3 o,ax;
  if(l1<=l2&&l1<=l3){u=t1*L1;o=o1;ax=b-a;}else if(l2<=l3){u=L1+t2*L2;o=o2;ax=c-b;}else{u=L1+L2+t3*L3;o=o3;ax=e-c;}
  float L=L1+L2+L3,v=u/L,r=mix(r0,r1,v);vec3 sx=normalize(cross(ax,cZ+vec3(1e-3,0,0)));float x=dot(o,sx)/r;
  float ph=u/L*n;float ch=abs(sin(PI*(ph-abs(x)*.55+.5*step(0.,x))));
  u=v;return (length(o)-r*(.80+.26*pow(ch,.6)))*.72;
}
uniform int look;        // dress: 0 silk and gold, 1 cotton and jasmine, 2 worn, no jewels, 3 a townswoman
uniform int hairm;       // hair: 0 braid over the right shoulder, 1 loose, 2 low bun
uniform float veil;      // 0 none, 1 over the head, 2 pinned behind the crown
uniform float old;       // age of the hands 0..1
uniform float lamp;      // a lit diya: 1 in both hands, 2 in the right, 3 in the left
#define HEM -.16
float hairline(vec3 h){float ax=abs(h.x);float L=.665-.80*ax*ax;L-=.52*smoothstep(.34,-.02,h.z)*smoothstep(.40,.72,ax);return L-1.25*smoothstep(-.10,-.42,h.z);}
float hairD(vec3 h){
  vec3 q=vec3(abs(h.x),h.yz);
  float d=sEll(h-vec3(0,.185,-.12),vec3(.825,.895,.905));
  d=smin(d,sEll(q-vec3(.60,.05,-.14),vec3(.25,.48,.46)),.20);
  d=smin(d,sEll(h-vec3(0,-.42,-.50),vec3(.50,.56,.42)),.22);
  d+=.035*exp(-h.x*h.x*900.)*smoothstep(.35,.6,h.y)*smoothstep(-.8,-.4,h.z);
  return smax(d,hairline(h)-h.y,.035);
}
vec3 palmAt(int k){mat3 M=k==0?BL:BR;return (k==0?J[6]:J[9])+vec3(0,.62,.16)*B[7]*M;}
vec3 lampAt(){return (lamp<1.5?.5*(palmAt(0)+palmAt(1)):lamp<2.5?palmAt(1):palmAt(0))+vec3(0,lamp<1.5?.18:.24,0)*B[7];}
vec2 lampD(vec3 p){                          // brass bowl, oil, wick and flame
  vec3 o=lampAt();float LS=.50*B[7];
  vec3 q=(p-o)/LS;float bd=length(q-vec3(0,1.,0))-2.3;if(bd>1.5) return vec2(bd*LS,3.);
  float ou=sEll(q-vec3(0,.10,0),vec3(1.0,.60,1.0));float d=max(ou,q.y-.26);d=smax(d,-sEll(q-vec3(0,.30,0),vec3(.88,.56,.88)),.05);
  vec2 m=vec2(d*.8,3.);m=U(m,vec2(sCyl(q-vec3(0,.10,0),.80,.03,.02),21.));m=U(m,vec2(sCap(q,vec3(0,.1,.2),vec3(0,.30,.74),.07),6.));
  vec3 f=q-vec3(0,.36,.76);float sw=.10*sin(fT*7.+J[6].x*3.)+.05*sin(fT*17.+J[6].y);f.x-=sw*f.y*f.y*.6;f.z-=Wind.z*f.y*.4;
  float t=clamp(f.y/1.5,0.,1.);float r=.46*sqrt(t+.03)*pow(1.-t,.9)+.01;float fl=length(vec3(f.x,f.y-t*1.5,f.z))-r;
  m=U(m,vec2(fl*.62,20.));return vec2(m.x*LS,m.y);}
void lampSurf(vec3 p,int m,inout Surf s){
  if(m==20){vec3 o=lampAt();float LS=.50*B[7];float y=(p.y-o.y)/LS-.36;s.base=mix(vec3(2.2,1.5,.75),vec3(2.4,.80,.10),smoothstep(.2,1.3,y));s.ink=0.;s.cls=4.;}
  if(m==21)s.ink=.4;}
float jasmine(vec3 p){float a=atan(p.y,p.x)+p.z*4.;return (length(p)-.068-.016*cos(a*5.))*.8;}
vec2 hairJewels(vec3 h){                    // chain along the parting and the pendant on the forehead
  vec2 m=vec2(1e3,3.);
  if(look==0){
    vec3 c=h-vec3(0,.185,-.12);float a=atan(c.z,c.y),r=length(vec2(c.y/.895,c.z/.905));
    float k=clamp(floor(a/.062+.5),4.,20.)*.062;vec3 b=vec3(0,cos(k)*.905,sin(k)*.915);m=U(m,vec2(length(c-b)-.030,3.));
    vec3 q=h-vec3(0,.565,.742);
    {m=U(m,vec2(sEll(q,vec3(.105,.115,.035)),3.));m=U(m,vec2(sEll(q-vec3(0,.0,.03),vec3(.055,.062,.03)),4.));
      vec3 b2=q-vec3(0,0,.01);float an=atan(b2.y,b2.x);float st=TAU/12.;an=mod(an+st*.5,st)-st*.5;float rr=length(b2.xy);m=U(m,vec2(length(vec3(rr*cos(an)-.118,rr*sin(an),b2.z))-.026,6.));
      m=U(m,vec2(sEll(q-vec3(0,-.155,.015),vec3(.030,.042,.030)),6.));
      // side chains along the hairline to the ears
      vec3 s=vec3(abs(h.x),h.yz);float hl=s.y-hairline(s)-.03;float sh=sEll(h-vec3(0,.185,-.12),vec3(.84,.91,.92));float ch=length(vec2(hl*.8,sh))-.028;ch=max(ch,-(s.z-.02));ch=max(ch,.02-s.x);float bd=.5+.5*sin(s.x*80.);m=U(m,vec2((ch+.010*bd)*.6,3.));}
  } else if(look==1){                        // jasmine over the crown and one flower above the ear
    vec3 g=h-vec3(0,.10,-.12);g.yz=rot(.16)*g.yz;float a=atan(g.x,g.y),st=.135;float k=clamp(floor(a/st+.5),-12.,12.)*st;vec3 b=vec3(sin(k)*.86,cos(k)*.965,.03*sin(k*23.));m=U(m,vec2(jasmine(g-b),6.));
    vec3 f=h-vec3(.80,.20,.16);f.xz=rot(-.75)*f.xz;float an=atan(f.y,f.x),sa=TAU/5.;an=mod(an+sa*.5,sa)-sa*.5;float r=length(f.xy);vec3 e=vec3(r*cos(an)-.115,r*sin(an),f.z-.05*r);m=U(m,vec2(sEll(e,vec3(.12,.075,.035)),11.));m=U(m,vec2(length(f-vec3(0,0,.03))-.05,14.));
  }
  return m;
}
vec2 earJewels(vec3 h){
  vec3 q=vec3(abs(h.x),h.yz)-vec3(.80,-.26,.0);float bd=length(q+vec3(0,.2,0))-.5;if(bd>.35) return vec2(bd,3.);
  if(look==1){vec3 f=q-vec3(.03,-.05,.04);f.xz=rot(-.6)*f.xz;float an=atan(f.y,f.x),sa=TAU/5.;an=mod(an+sa*.5,sa)-sa*.5;float r=length(f.xy);vec2 m=vec2(sEll(vec3(r*cos(an)-.075,r*sin(an),f.z),vec3(.075,.05,.03)),11.);m=U(m,vec2(length(f-vec3(0,0,.03))-.035,14.));
    for(int i=0;i<2;i++)m=U(m,vec2(sEll(q-vec3(.02,-.20-.11*float(i),.02),vec3(.045,.06,.045)),6.));return m;}
  if(look==3){vec2 m=vec2(length(q-vec3(.03,.0,.03))-.07,3.);return U(m,vec2(length(vec2(length(q.xy-vec2(.03,-.13))-.10,q.z-.02))-.022,3.));}
  float st=length(q-vec3(.02,-.02,.03))-.075;vec2 m=vec2(st,3.);m=U(m,vec2(length(q-vec3(.05,-.02,.09))-.035,4.));
  vec3 j=q-vec3(.03,-.27,.02);float r=length(j.xz);float bell=max(abs(length(vec3(j.x,j.y+.08,j.z)/vec3(1,1.15,1))-.155)-.025,-(j.y+.10));m=U(m,vec2(bell*.8,3.));
  m=U(m,vec2(sCap(j,vec3(0,.10,0),vec3(0,.20,0),.025),3.));m=U(m,vec2(sTor(j-vec3(0,-.09,0),.165,.025),3.));
  vec3 b=polar(j-vec3(0,-.145,0),10.,0.);m=U(m,vec2(length(b-vec3(0,0,.155))-.030,6.));m=U(m,vec2(sEll(j-vec3(0,-.16,0),vec3(.05,.07,.05)),4.));
  return m;
}
vec2 necklaces(vec3 p,float td){
  vec3 c=Bc*(p-J[1]);
  if(look==0){
    vec2 m=vec2(beadsD(c,td,vec2(0,1.46),.48,.050,36.),6.);
    m=U(m,vec2(beadsD(c,td,vec2(0,1.46),.575,.040,-1.),3.));m=U(m,vec2(beadsD(c,td,vec2(0,1.46),.655,.066,30.),4.));
    m=U(m,vec2(beadsD(c,td,vec2(0,1.46),.735,.040,50.),3.));
    float a=atan(c.x,-(c.y-1.46));float dr=beadsD(c,td,vec2(0,1.46),.82,.055,30.);m=U(m,vec2(dr,6.));
    vec3 c2=vec3(c.x*1.32,c.yz);m=U(m,vec2(beadsD(c2,td-.02,vec2(0,1.36),1.20,.048,60.)*.8,3.));m=U(m,vec2(beadsD(c2,td-.02,vec2(0,1.36),1.29,.046,64.)*.8,6.));m=U(m,vec2(beadsD(c2,td-.02,vec2(0,1.36),1.375,.040,70.)*.8,3.));
    vec3 pd=vec3(c.x,c.y+.10,td*1.25-.05+max(0.,-c.z*2.));m=U(m,vec2(sEll(pd,vec3(.19,.22,.08)),3.));m=U(m,vec2(sEll(pd-vec3(0,0,.06),vec3(.10,.13,.06)),4.));m=U(m,vec2(sEll(pd-vec3(0,-.26,.02),vec3(.045,.07,.045)),6.));
    return m;}
  if(look==1){float r1=.070,r2=.074;vec2 m=vec2(beadsD(c,td,vec2(0,1.46),.60,r1,30.),6.);vec3 c2=vec3(c.x*1.32,c.yz);m=U(m,vec2(beadsD(c2,td-.02,vec2(0,1.36),1.24,r2,46.)*.8,6.));vec3 pd=vec3(c.x,c.y+.02,td*1.2-.06+max(0.,-c.z*2.));float an=atan(pd.y,pd.x);m=U(m,vec2((length(pd*vec3(1,1,1.4))-.15-.03*cos(an*6.))*.7,11.));m=U(m,vec2(length(pd-vec3(0,0,.10))-.06,14.));return m;}
  if(look==3){vec2 m=vec2(beadsD(c,td,vec2(0,1.46),.58,.050,34.),3.);return U(m,vec2(length(vec3(c.x,c.y-.82,td*1.2-.05+max(0.,-c.z*2.)))-.10,4.));}
  return vec2(beadsD(c,td,vec2(0,1.50),.56,.022,-1.),14.);
}
float hoodD(vec3 p,out float lip){
  vec3 h=Bh*(p-J[3]),c=Bc*(p-J[1]);
  float d=sEll(h-vec3(0,.20,-.16),vec3(.90,.965,.965));
  d=smin(d,sEll(h-vec3(0,-.15,-.30),vec3(.92,.80,.80)),.25);
  vec3 a=J[3]-hZ*.42-hY*.35,b=J[1]+cY*.55-cZ*.42,e=J[0]-pZ*.42+pY*.2,f=J[0]-pZ*.75-pY*2.6+Wind*.6;
  vec3 z=mix(pZ,cZ,smoothstep(-1.,1.,c.y))*.55;vec3 p2=p+z*dot(p-b,cZ),e2=e+z*dot(e-b,cZ),f2=f+z*dot(f-b,cZ);
  d=smin(d,sCone(p,a,b,.72,.80),.40);float bk=smin(sCone(p2,b,e2,1.06,1.16),sCone(p2,e2,f2,1.16,1.42),.4)*.72;d=smin(d,bk,.4);
  d=smin(d,sEll(c-vec3(0,.92,-.22),vec3(1.55*B[11],.42,.50)),.35);
  float ax=atan(c.x,-c.z);d-=(.035*sin(ax*9.+c.y*.6)+.015*sin(ax*19.))*smoothstep(1.2,-.6,c.y);
  // opening: a plane that follows the head above and the back below
  float vb=max(0.,veil-1.);float fr=mix(dot(p-J[1],cZ)+.16+.20*smoothstep(.2,.8,c.y)*smoothstep(1.5,1.,c.y),h.z-(.16+.30*(h.y-.2))+vb*.42,smoothstep(1.2,2.1,c.y));
  lip=-fr;
  d=smax(d,fr,.02);
  vec3 q=Bp*(p-J[0]);d=smax(d,-(q.y+2.4)+.06*sin(ax*9.),.03);
  return d*.78;
}
float blouseD(vec3 p,float td,vec3 c){
  float d=td-.045;vec3 a=J[4],b=J[5],a2=J[7],b2=J[8];
  float s=B[5];d=max(d,-(c.y+.70));
  d=smin(d,smax(sCone(p,a,mix(a,b,.42),.54*s+.06,.44*s+.06),dot(p-mix(a,b,.40),normalize(b-a)),.02),.22);d=smin(d,smax(sCone(p,a2,mix(a2,b2,.42),.54*s+.06,.44*s+.06),dot(p-mix(a2,b2,.40),normalize(b2-a2)),.02),.22);
  float ne=length(vec2(c.x,c.y-1.42)*vec2(.92,1.))-.86;d=smax(d,-ne,.03);
  return d*.9;
}
// the pallu: across the front from the right hip to the left shoulder, then down the back
float palluS(vec3 c){return .80*c.x-.60*c.y-.06;}
float palluE(vec3 c,vec3 q){float w=sin(q.y*1.7);return max(.14+.05*w-.22*smoothstep(0.,-3.,c.y)-c.x,c.x-max(1.02,(.68+.60*c.y)/.80)-.03*w);}
float palluD(vec3 p,float ts,float dsk,vec3 c,vec3 q){
  float wv=.105+.016*sin(palluS(c)*24.),sf=abs(ts-wv)-.035,sb=abs(smin(ts,dsk+.02,.3)-wv)-.035;
  float s=palluS(c);
  float fr=max(abs(s)-.62-.12*smoothstep(.2,-1.4,c.y),-c.z-(veil>.5?.75:.30));fr=max(fr,-q.y+.28);
  if(veil>.5) return max(sf,fr)*.80;
  float bk=max(palluE(c,q),c.z+.10);bk=max(bk,-(q.y+mix(-.1,3.3,smoothstep(2.,4.,J[0].y))+.06*sin(c.x*9.)));bk=max(bk,length(q.xz)-1.75-max(0.,q.y-.6)*3.);
  return min(max(sf,fr),max(sb,bk))*.80;
}
#ifndef CAST_LIB
vec2 map(vec3 p){
  float dh=length(p-J[3]);vec3 c=Bc*(p-J[1]),q=Bp*(p-J[0]);
  float td=femTorso(p),sk=td;
  float ar=min(armD(p,J[4],J[5],J[6],B[5]),armD(p,J[7],J[8],J[9],B[5]));
  sk=smin(sk,ar,.20);
  sk=smin(sk,handD(p,0),.08);sk=smin(sk,handD(p,1),.08);
  float fy=min(length(p-J[12]),length(p-J[16]))-1.9;
  if(fy<sk){float lg=min(sCone(p,J[11],J[12],.40*B[6],.22*B[6]),sCone(p,J[15],J[16],.40*B[6],.22*B[6]));
    lg=smin(lg,toesD(p,J[12],J[18],J[13],.84,1.),.10);lg=smin(lg,toesD(p,J[16],J[19],J[17],.84,-1.),.10);vec3 kn=.5*(J[11]+J[15]),an=.5*(J[12]+J[16]);lg=max(lg,-dot(p-an,hemDir(kn,an))-.35);if(J[0].y>3.)sk=min(sk,lg);}
  sk=smin(sk,femNeck(p),.14);
  vec3 h=Bh*(p-J[3]);if(dh-2.1<sk)sk=smin(sk,smin(femHead(h),earsD(h,.5),.04),.10);
  vec2 m=vec2(sk,1.);
  float ts=smin(td,length(p-J[4])-.56*B[5],.24);
  m=U(m,vec2(blouseD(p,td,c),9.));
  vec4 loc;float ds=sariD(p,HEM,loc),lr=length(q.xz);ds=max(ds,(td-.07-max(0.,.46-q.y)*.75-3.*max(0.,lr-1.05))*.8);m=U(m,vec2(ds,7.));
  float dp=palluD(p,ts,ds,c,q);m=U(m,vec2(dp,8.));float tn=min(td,min(dp/.8+.02,1e3));
  if(look<2){float be=max(max(abs(td-.155)-.05,abs(q.y-.36+.05*cos(q.x*2.))-.085),lr-1.3)*.8;m=U(m,vec2(be,look==0?3.:14.));
    if(look==0){vec3 bq=q-vec3(0,.30,.96);m=U(m,vec2(sEll(bq,vec3(.17,.20,.10)),3.));m=U(m,vec2(sEll(bq-vec3(0,0,.07),vec3(.09,.11,.06)),5.));
      vec3 b=q;b.x-=clamp(floor(b.x/.16+.5),-3.,3.)*.16;float sw=td-.16;m=U(m,vec2(length(vec3(b.x,q.y-.20+.02*abs(q.x),sw))*.8-.045+.0,q.z>.2?6.:3.));}}
  if(dh-3.<m.x){
    if(dh-2.1<m.x){
      m=U(m,vec2(hairD(h)*.92,2.));
      m=U(m,hairJewels(h));if(look!=2)m=U(m,earJewels(h));
      if(look==0){vec3 n=h-vec3(.118,-.338,.822);n.xz=rot(-.45)*n.xz;m=U(m,vec2(length(vec2(length(n.xy)-.050,n.z))-.016,15.));m=U(m,vec2(length(n-vec3(0,-.050,.0))-.024,16.));}
      else if(look==1)m=U(m,vec2(length(h-vec3(.130,-.325,.845))-.026,15.));
    }
    if(veil>.5){float lip;m=U(m,vec2(hoodD(p,lip),10.));}
  } else if(veil>.5&&c.z<.6){float lip;m=U(m,vec2(hoodD(p,lip),10.));}
  m=U(m,necklaces(p,tn));
  if(hairm==0){float u;vec3 a,b,cc,e;{a=J[3]-hX*.42-hY*.62-hZ*.52;b=J[1]-cX*.66+cY*1.34-cZ*.02;cc=J[1]-cX*.56+cY*.20+cZ*.96;e=J[1]-cX*.62-cY*1.75+cZ*.96;}
    float bd=braidD(p,a,b,cc,e,.215,.125,17.,u);m=U(m,vec2(bd,u>.95?14.:2.));
    float k=clamp(floor(u*6.5),1.,5.);float uc=(k+.5)/6.5;vec3 fc=uc<.33?mix(a,b,uc/.33):uc<.62?mix(b,cc,(uc-.33)/.29):mix(cc,e,(uc-.62)/.38);
  } else if(hairm==1){
    vec3 a=J[3]-hZ*.30-hY*.15,b=J[1]-cZ*.58+cY*.75,e=J[1]-cZ*.60-cY*.9,f=J[0]-pZ*.78-pY*.4;
    float ld=sCone(p,a,b,.66,.60);ld=smin(ld,sCone(p,b,e,.58,.50),.3);ld=smin(ld,sCone(p,e,f,.50,.16),.3);
    float an=atan(c.x,-c.z-.1);ld-=(.030*sin(an*13.+c.y*1.3)+.018*sin(an*29.-c.y*2.))*smoothstep(2.4,.6,c.y);ld=smax(ld,c.z-.18-.4*smoothstep(1.2,2.,c.y),.1);
    if(dh<2.4){ld=smax(ld,h.z-.02,.15);}if(veil>.5)ld=max(ld,-c.z-.30);
    for(int s=0;s<2;s++){float sg=s==0?1.:-1.,ln=s==0?.55:1.;vec3 l0=J[3]+hX*.68*sg-hY*.25-hZ*.22,l1=J[1]+cX*.66*sg+cY*1.36-cZ*.06,l2=J[1]+cX*.70*sg+cY*.78+cZ*.56,l3=J[1]+cX*.62*sg-cY*(-.35+1.0*ln)+cZ*.97;
      vec3 w=cX*.035*sin(c.y*5.+sg);float lk=sCone(p+w,l0,l1,.20,.15);lk=smin(lk,sCone(p+w,l1,l2,.15,.12),.22);lk=smin(lk,sCone(p+w,l2,l3,.12,.02),.22);ld=smin(ld,lk-.014*sin(dot(p,cX)*36.+c.y*6.),.10);}
    m=U(m,vec2(ld*.85,2.));
    if(look==2){vec3 g=h-vec3(-.43,.72,.46);g.xz=rot(.75)*g.xz;g.yz=rot(-.62)*g.yz;g.xy=rot(-.35)*g.xy;   // the chudamani
    float jw=sEll(g,vec3(.14,.18,.06));m=U(m,vec2(jw,3.));m=U(m,vec2(sEll(g-vec3(0,0,.05),vec3(.075,.11,.05)),5.));vec3 gb=g;float ga=atan(g.y,g.x),gs=TAU/10.;ga=mod(ga+gs*.5,gs)-gs*.5;float gr=length(g.xy*vec2(1.,.80));m=U(m,vec2(length(vec3(gr*cos(ga)-.155,gr*sin(ga),g.z))-.030,6.));m=U(m,vec2(sEll(g-vec3(0,-.26,0),vec3(.04,.07,.04)),6.));}
  } else if(dh<2.2&&veil<.5){vec3 b=h-vec3(0,-.34,-.98);float r=length(b.xy),bu=sEll(b,vec3(.46,.44,.32))-.018*sin(r*34.+atan(b.y,b.x)*2.);m=U(m,vec2(bu*.85,2.));
    if(look==3){float an=atan(b.y,b.x),sa=TAU/13.;an=mod(an+sa*.5,sa)-sa*.5;m=U(m,vec2(length(vec3(r*cos(an)-.47,r*sin(an),b.z-.04))-.085,6.));}}
  if(look!=2) for(int s=0;s<2;s++){vec3 e0=s==0?J[4]:J[7],e1=s==0?J[5]:J[8],e2=s==0?J[6]:J[9];
    vec3 u=normalize(e1-e0),v=normalize(e2-e1);float L=length(e2-e1);
    if(look!=1){if(look==0)m=U(m,vec2(ringD(p,mix(e0,e1,.50),u,.415*B[5],.075,.03),3.));
      vec3 o=p-e1;float y=dot(o,v)/L;float r=length(o-v*y*L);float k=clamp(floor((y-.70)/.045+.5),look==0?0.:3.,5.);float R=mix(.30,.235,smoothstep(.7,.95,y))*B[5]+.035;
      float bg=length(vec2(r-R,(y-.70-k*.045)*L))-.040;m=U(m,vec2(bg,(k==1.||k==4.)?4.:3.));
      vec3 an=s==0?J[12]:J[16],kn=s==0?J[11]:J[15];m=U(m,vec2(ringD(p,mix(kn,an,1.005),normalize(an-kn),.265*B[6],.05,.035),3.));}
    else{vec3 o=p-mix(e1,e2,.90);float y=dot(o,v);vec3 rr=o-v*y;float r=length(rr);vec3 sx=normalize(cross(v,vec3(.3,.8,.5))),sy=cross(v,sx);float a=atan(dot(rr,sx),dot(rr,sy)),st=TAU/11.;a=mod(a+st*.5,st)-st*.5;
      m=U(m,vec2(length(vec3(r*sin(a),r*cos(a)-.235*B[5]-.06,y))-.082,6.));}}
  if(lamp>.5)m=U(m,lampD(p));
#ifdef EXTRA
  m=U(m,extra(p,h,c,q,td));
#endif
  return m;
}
void surf(vec3 p,vec3 n,int m,inout Surf s){
  vec3 h=Bh*(p-J[3]),c=Bc*(p-J[1]),q=Bp*(p-J[0]);
  vec3 gold=vec3(1.);
  if(m==1){
    float isH=facePaint(p,n,s);
    float ik=neckInk(c)*step(isH,.01)*.8;
    for(int k=0;k<2;k++){vec3 hp=handPaint(p,k,old);ik=max(ik,hp.x*.75);
      vec3 nc=look==2?mix(s.base,hex(0xf2c0a0),.6):mix(s.base,hex(0xc23a3a),.75);s.base=mix(s.base,nc,hp.y);
      if(look==0){s.base=mix(s.base,hex(0xa8301c),hp.z*(1.-hp.y)*.75);s.sh=mix(s.sh,hex(0x5a1414),hp.z*.6);
        vec3 l=(k==0?BL:BR)*(p-(k==0?J[6]:J[9]))/B[7];float r=length(l.xy-vec2(0,.42));if(l.z>.05&&l.z<.4&&l.y<.9&&l.y>0.){float md=max(smoothstep(.15,.135,r),lineA(r-.20,.02));float da=atan(l.y-.42,l.x);md=max(md,smoothstep(.035,.02,abs(r-.255)+.02-.02*cos(da*10.)));s.base=mix(s.base,hex(0xa8301c),md*.8);}}}
    float fo=min(length(p-J[13]),length(p-J[17]));
    if(look==0){float lw=length(p-J[13])<length(p-J[17])?dot(p-J[18],vec3(0,1,0)):dot(p-J[19],vec3(0,1,0));float al=max(smoothstep(.02,-.02,lw),smoothstep(.20,.16,fo))*step(min(length(p-.5*(J[13]+J[18])),length(p-.5*(J[17]+J[19]))),1.5);s.base=mix(s.base,hex(0xc01c2a),al*.85);}
    s.base=mix(s.base,hex(0x7a3a26),ik*.8);s.sh=mix(s.sh,hex(0x4a2018),ik*.8);
  }
  if(m==2){
    vec3 d=h-vec3(0,.18,-.12);float ax=abs(h.x);
    if(length(h)<1.25){float st=atan(d.z+.2,ax+.05)*1.0;float u=atan(d.y-.2,length(vec2(ax,d.z)));float w=sin(st*70.+6.*vn(vec2(st*8.,u*3.)));
      float ln=smoothstep(.80,.97,w)*smoothstep(.0,.15,ax);s.base*=1.-.6*ln;s.ns=normalize(s.ns+.10*w*hX*sign(h.x));float sh=smoothstep(.16,.05,abs(u-.62+.05*sin(st*14.)+.03*w));s.base=mix(s.base,s.base*2.2+hex(0x2a140c)*1.2,sh*.75*(1.-ln));
      float pr=smoothstep(.030,.018,ax)*smoothstep(.30,.5,h.y)*step(-.55,h.z);if(look<2){s.base=mix(s.base,hex(0xc8141c),pr*step(.0,h.z));s.sh=mix(s.sh,hex(0x6a0a12),pr*step(.0,h.z));if(pr>.5&&h.z>0.)s.cls=1.;}
      s.base=mix(s.base,s.sh*.6,pr*(look<2?step(h.z,0.):1.));}
    else if(hairm==1){float w=sin(c.x*38.+3.*sin(c.y*2.)+5.*vn(c.xy*vec2(4.,1.)));s.base*=1.-.5*smoothstep(.75,.97,w);s.ns=normalize(s.ns+.12*w*cX);}
    s.ink=.7;
  }
  bool cloth=m==7||m==8||m==9||m==10;
  if(m==7){vec4 l;sariD(p,HEM,l);float ht=l.x,a=l.y;
    float bw=look==0?.95:look==2?.30:.50;float t=ht/bw;
    if(ht<.06&&l.z<.5&&dot(n,hemDir(.5*(J[11]+J[15]),.5*(J[12]+J[16])))>.5){s.base*=.40;s.sh*=.6;s.ink=.6;return;}
    if(look==0){
      if(t<1.){float g=zari(t,a*28./TAU);if(g>.5){s.cls=2.;s.base=vec3(1.);s.sh=hex(0x805030);}else{s.base=Pb[17];s.sh=Ps[17];}s.ink=.6;}
      else{vec2 g=l.z>.5?p.xz*1.25:vec2(a*22./TAU,ht*1.45);g.x+=.5*mod(floor(g.y),2.);vec2 f=fract(g)-.5;float r=length(f*vec2(1.,1.15)),an=atan(f.x,f.y);float bt=max(step(r,.17+.09*cos(an*4.)),step(abs(r-.30),.018)*0.)*step(.07,r);bt=max(bt,step(r,.045));if(bt>.5&&l.w>.12){s.cls=2.;s.base=vec3(.92);}}
    } else if(t<1.){float st=look!=2?max(step(t,.22),max(step(.36,t)*step(t,.50),step(.86,t))):step(t,.45);s.base=mix(s.base,Pb[18],st*(look==2?.6:.92));s.sh=mix(s.sh,Ps[18],st*.85);}
    else if(look==3){vec2 g=vec2(a*20./TAU,ht*1.5);g.x+=.5*mod(floor(g.y),2.);float dt=step(length(fract(g)-.5),.11);s.base=mix(s.base,Pb[18],dt*.8);}
    if(look==2){float wr=fbm(vec2(a*4.,ht*1.2));s.base*=.86+.24*wr;s.base=mix(s.base,hex(0xa88a5a),smoothstep(.62,.75,wr)*.35);}
    float front=smoothstep(.15,.5,exp(-a*a*5.))*(1.-l.z);float pl=abs(fract(a*5.+.25)-.5)*2.;float gr=front*smoothstep(.34,.10,pl)*smoothstep(.03,.20,l.w);s.base*=1.-.55*gr;s.sh*=1.-.45*gr;s.ink=max(s.ink*.8,.0);
    float fo=sin(a*11.+l.w*2.5);s.base*=1.-.20*smoothstep(.55,.95,-fo)*smoothstep(.1,.6,l.w)*(1.-front);
  }
  if(m==8){float sx=palluS(c);float e=.62-abs(sx);bool back=veil<.5&&c.z<-.10;if(back)e=-palluE(c,q);float al=back?q.y:dot(c.xy,vec2(.60,.80));float endb=back?q.y+3.3:9.;e=min(e,endb*.5);
    float bw=look==0?.24:.14;float t=e/bw;
    if(t<1.&&t>-.5){if(look==0){float g=zari(t,al*2.6);if(g>.5){s.cls=2.;s.base=vec3(1.);}else{s.base=Pb[17];s.sh=Ps[17];}}else{float st=max(step(t,.35),step(.6,t)*step(t,.8));s.base=mix(s.base,Pb[18],st*(look==2?.6:.92));s.sh=mix(s.sh,Ps[18],st*.85);}}
    else if(look==0){vec2 g=vec2(sx,al)*3.4;g.x+=.5*mod(floor(g.y),2.);vec2 f=fract(g)-.5;float an=atan(f.x,f.y);if(length(f)<.17+.06*cos(an*4.)){s.cls=2.;s.base=vec3(.92);}}
    float fl=sin(sx*24.);s.base*=1.-.16*smoothstep(.5,.95,-fl)*(s.cls==2.?0.:1.);s.ink=.75;}
  if(m==9){float nk=length(vec2(c.x,c.y-1.42)*vec2(.92,1.))-.86;float t1=dot(p-mix(J[4],J[5],.40),normalize(J[5]-J[4])),t2=dot(p-mix(J[7],J[8],.40),normalize(J[8]-J[7]));
    float e=min(min(nk,c.y+.70),min(length(p-mix(J[4],J[5],.40))<.5?abs(t1):9.,length(p-mix(J[7],J[8],.40))<.5?abs(t2):9.));
    if(look==0){if(e<.10){s.cls=2.;s.base=vec3(1.);}else{vec2 f=fract(vec2(c.x,c.y)*4.5)-.5;if(length(f)<.10&&abs(c.x)<.8&&c.z>0.){s.cls=2.;s.base=vec3(.9);}}}
    else if(e<.07){s.base=Pb[19];s.sh=Ps[19];}}
  if(m==10){float lip;hoodD(p,lip);float t=lip/.17;vec3 q2=Bp*(p-J[0]);float ht=q2.y+2.4;float al=abs(h.y)<1.4&&length(h)<1.6?atan(h.y,abs(h.x))*1.2:c.y;if(ht/.5<t){t=ht/.5;al=atan(c.x,-c.z-.2)*2.2;}
    if(lip<.022&&ht>.02){s.base*=.55;s.sh*=.7;}
    else if(look!=0){if(t<1.){float st=max(step(t,.35),step(.6,t)*step(t,.8));s.base=mix(s.base,Pb[18],st*.92);s.sh=mix(s.sh,Ps[18],st*.85);}}
    else if(t<1.){float g=zari(t,al*4.);if(g>.5){s.cls=2.;s.base=vec3(1.);}else{s.base=Pb[17];s.sh=Ps[17];}}
    else{vec2 g=length(h)<1.6?vec2(atan(h.x,-h.z)*3.2,h.y*3.):vec2(atan(c.x,-c.z)*3.2,c.y*2.4);g.x+=.5*mod(floor(g.y),2.);vec2 f=fract(g)-.5;if(length(f)<.11){s.cls=2.;s.base=vec3(.95);}}
    s.ink=.8;}
  if(m==15||m==16)s.ink=.35;lampSurf(p,m,s);
#ifdef EXTRA
  extraSurf(p,h,c,q,n,m,s);
#endif
  if(m==6&&look==1){s.ink=.75;s.base*=.92+.10*vn(p.xy*30.);}
}
#endif
