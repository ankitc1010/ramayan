// WAR HORSE (and the donkey-faced demon horse, demon=1).  Joints as in deer.glsl: the same rig, heavier bones.
uniform vec3 J[40];uniform mat3 Bp,Bc,Bh;uniform vec2 ear;uniform float jaw,demon,harness,plain;uniform vec3 clothA,clothB;
uniform sampler2D tFace;
const float HK=1.13;
const vec3 EC=vec3(.425,.14,.62);
float limbF(vec3 p,vec3 s,vec3 e,vec3 k,vec3 f,vec3 h){
  float d=sCone(p,s,e,.95,.60);d=smin(d,sCone(p,e,mix(e,k,.5),.56,.36),.30);d=smin(d,sCone(p,mix(e,k,.42),k,.37,.235),.14);d=smin(d,length(p-k)-.265,.10);
  d=smin(d,sCone(p,k,f,.205,.17),.08);d=smin(d,length(p-f)-.235,.10);d=smin(d,sCone(p,f-normalize(h-f)*.0-vec3(0,0,.10),f-vec3(0,.12,.14),.12,.06),.1);return smin(d,sCone(p,f,h,.19,.21),.06);}
float limbH(vec3 p,vec3 s,vec3 e,vec3 k,vec3 f,vec3 h){
  float d=sCone(p,s,e,1.20,.76);d=smin(d,sCone(p,e,mix(e,k,.5),.70,.44),.34);d=smin(d,sCone(p,mix(e,k,.45),k,.44,.25),.16);d=smin(d,length(p-k)-.285,.10);
  d=smin(d,sCone(p,k+normalize(k-f)*.16-vec3(0,0,.12),k-vec3(0,0,.06),.14,.18),.1);
  d=smin(d,sCone(p,k,f,.225,.18),.08);d=smin(d,length(p-f)-.24,.10);return smin(d,sCone(p,f,h,.195,.215),.06);}
float hoofD(vec3 p,vec3 f,vec3 h){vec3 a=normalize(h-f);return max(sCone(p,h-a*.22,h+a*.06,.22,.325),dot(p-h,a)-.15);}
vec2 headD(vec3 h){
  vec3 q=vec3(abs(h.x),h.yz);
  float d=sEll(h-vec3(0,.02,-.02),vec3(.52,.58,.74));
  float mz=mix(1.,1.22,demon);
  d=smin(d,sCone(h,vec3(0,.02,.40),vec3(0,-.16,1.95),.50,.29*mz),.25);
  d=smin(d,sEll(q-vec3(.24,-.40,.34),vec3(.20,.58,.66)),.22);                       // cheek plate
  d=smin(d,sCone(h,vec3(0,-.62,.7),vec3(0,-.46,1.9),.20,.20),.22);
  d=smin(d,sEll(h-vec3(0,-.21,2.10),vec3(.335,.32,.38)*mz),.16);
  float jd=jaw*.34;d=smin(d,sCone(h,vec3(0,-.55,1.0),vec3(0,-.52-jd,2.06),.18,.17),.14);
  d=smax(d,-sEll(q-vec3(.30,-.10,2.36*mix(1.,1.03,demon)),vec3(.12,.15,.17)),.07);
  d=smax(d,-sCone(q,vec3(0,-.40-jd*.4,2.48),vec3(.36,-.40-jd*.2,1.66),.022+.10*jaw,.016),.05);
  d=smin(d,sCone(q,vec3(.22,.40,.74),vec3(.50,.36,.30),.12,.13),.14);
  d=smin(d,sCone(q,vec3(.34,-.06,.85),vec3(.26,-.12,1.5),.07,.03),.10);              // zygomatic line
  d=smin(d,sEll(q-EC+vec3(.04,0,0),vec3(.20,.23,.24)),.06);
  vec2 m=vec2(d,1.);
  for(int s=0;s<2;s++){float sg=s==0?1.:-1.;float e=ear[s];vec3 r=vec3(h.x*sg,h.yz)-vec3(.26,.48,-.30);r.yz=rot(.15+.9*min(e,0.)*-1.)*r.yz;r.xy=rot(-.32-.35*demon)*r.xy;float ln=mix(.50,.92,demon);
    vec3 l=r-vec3(0,ln,0);float tp=smoothstep(.0,ln,l.y);vec3 lz=vec3(l.x*(1.+.8*tp),l.y,l.z);float k=sEll(lz,vec3(.23,ln,.15));float hol=sEll(lz-vec3(0,0,.17),vec3(.16,ln*.85,.14));k=smax(k,-hol,.04);m=U(m,vec2(k*.8,l.z>-.06&&length(vec2(lz.x/.17,l.y/(ln*.86)))<1.?9.:1.));}
  if(demon>.5){m=U(m,vec2(min(sCone(q,vec3(.14,.48,.40),vec3(.30,1.15,.62),.15,.10),sCone(q,vec3(.30,1.15,.62),vec3(.26,1.7,1.0),.10,.01)),8.));
    if(jaw>.05){float tn=min(length((q-vec3(.12,-.36-jd*.25,2.28)).xz)-.05,1.);}
    vec3 tq=q-vec3(.17,-.36,2.16);tq.y+=0.;m=U(m,vec2(sCone(tq,vec3(0,.05,0),vec3(.02,-.30-jaw*.1,.06),.075,.01),11.));}
  if(harness>.5){
    // bridle: noseband, browband, cheek straps with rosettes, frontal plate
    float nb=abs(length((h.xy-vec2(0,-.20))*vec2(1.,.82))-.415*mix(1.,1.18,demon))-.035;nb=max(nb,abs(h.z-1.55)-.07);m=U(m,vec2(nb*.8,3.));
    float bb=max(abs(sEll(h-vec3(0,.02,.0),vec3(.60,.68,.84)))-.035,abs(h.z-.30-.5*h.y)-.075);bb=max(bb,-h.y-.5);m=U(m,vec2(bb*.8,3.));
    m=U(m,vec2(sCone(q,vec3(.56,-.10,.25),vec3(.42,-.30,1.55),.055,.05),12.));
    m=U(m,vec2(length(q-vec3(.60,-.06,.25))-.14,3.));m=U(m,vec2(length(q-vec3(.68,-.06,.26))-.08,4.));m=U(m,vec2(length(vec2(length((q-vec3(.44,-.34,1.56)).yz)-.14,q.x-.44))-.04,3.));
    vec3 f=h-vec3(0,.44,1.0);f.yz=rot(1.80)*f.yz;m=U(m,vec2(sEll(f,vec3(.19,.50,.07)),3.));m=U(m,vec2(sEll(f-vec3(0,.12,.04),vec3(.09,.13,.06)),4.));m=U(m,vec2(sEll(f-vec3(0,-.20,.04),vec3(.06,.08,.05)),5.));
    m=U(m,vec2(sCone(h,vec3(0,.62,-.02),vec3(0,.98,-.08),.16,.10),3.));m=U(m,vec2(length(h-vec3(0,1.02,-.08))-.15,4.));
  }
  return m;}
float torso(vec3 p){
  vec3 c=Bc*(p-J[1]),h=Bp*(p-J[0]);
  float d=sEll(c-vec3(0,-.34,-.15),vec3(1.22,1.66,1.65));
  vec3 q=vec3(abs(c.x),c.yz);
  d=smin(d,sEll(q-vec3(.50,-.70,1.0),vec3(.66,.78,.66)),.35);                         // breast muscles
  d=smin(d,sEll(c-vec3(0,.80,-.10),vec3(.42,.55,1.2)),.5);                             // withers
  vec3 a=J[1]-vec3(0,.16,0),b=J[0]+vec3(0,-.02,0);float t=segT(p,a,b);d=smin(d,length((p-mix(a,b,t)))-mix(1.46,1.20,smoothstep(0.,1.,t)),.6);
  vec3 hq=vec3(abs(h.x),h.yz);d=smin(d,sEll(hq-vec3(.42,.12,-.30),vec3(.92,1.22,1.36)),.45);
  return d;}
vec2 map(vec3 p){
  float d=torso(p);
  // the arched neck, deep from crest to throat
  vec3 u=normalize(J[3]-J[2]);
  d=smin(d,sCone(p,J[2]-Bc[1]*0.-vec3(0,.25,0),J[3],1.18,.80),.55);d=smin(d,sCone(p,J[2]+vec3(0,.40,-.25),J[3]+vec3(0,.22,-.20),.62,.52),.35);d=smin(d,sCone(p,J[3],J[4],.78,.52),.35);
  for(int s=0;s<4;s++){int b=6+5*s;vec3 c=mix(J[b],J[b+4],.5);float R=max(max(distance(c,J[b]),distance(c,J[b+1])),max(distance(c,J[b+2]),distance(c,J[b+3])))+1.25;if(length(p-c)-R>d+.4) continue;if(s<2)d=smin(d,limbF(p,J[b],J[b+1],J[b+2],J[b+3],J[b+4]),.32);else d=smin(d,limbH(p,J[b],J[b+1],J[b+2],J[b+3],J[b+4]),.38);}
  d=smin(d,sCone(p,J[26],J[27],.30,.20),.2);
  vec2 m=vec2(d,1.);
  for(int s=0;s<4;s++){int b=6+5*s;if(length(p-J[b+3])-1.6>m.x) continue;m=U(m,vec2(hoofD(p,J[b+3],J[b+4]),7.));
    if(harness>.5){vec3 a=normalize(J[b+3]-J[b+2]);vec3 o=p-mix(J[b+2],J[b+3],.80);float y=dot(o,a);float rr=length(o-a*y);m=U(m,vec2(length(vec2(rr-.23,max(abs(y)-.10,0.)))-.06,3.));}}
  if(harness>.5){
    vec3 na=normalize(J[3]-J[2]);vec3 nc=mix(J[2],J[3],.30)-vec3(0,.12,0);vec3 o=p-nc;float y=dot(o,na);vec3 rv=o-na*y;float rr=length(rv);
    if(abs(y)<1.2&&rr<2.2){float a=atan(rv.x,-rv.y);float R=1.17;m=U(m,vec2((length(vec2(rr-R,y))-.13-.03*sin(a*26.))*.8,3.));
      float st=TAU/14.;float am=mod(a+st*.5,st)-st*.5;float fr=step(abs(a),1.9)*1.;m=U(m,vec2(sEll(vec3(am*rr,rr-R-.02,y+.30),vec3(.15,.12,.22))+(1.-fr)*3.,3.));m=U(m,vec2(length(vec3(am*rr,rr-R-.10,y+.30))-.09+(1.-fr)*3.,4.));
      m=U(m,vec2(length(vec3(am*rr,rr-R+.03,y+.62))-.08+(1.-fr)*3.,6.));}
  }
  float dh=length(p-J[5]-vec3(0,.2,.4)*Bh)-3.4;
  if(dh<m.x){vec2 k=headD(Bh*(p-J[5])/HK);k.x*=HK;m=vec2(k.y==1.&&m.y==1.?smin(m.x,k.x,.25):min(m.x,k.x),k.x<m.x?k.y:m.y);}
  return m;
}
void surf(vec3 p,vec3 n,int m,inout Surf s){
  vec3 h=Bh*(p-J[5])/HK,c=Bc*(p-J[1]),b=Bp*(p-J[0]);bool isHead=length(h-vec3(0,0,.6))<2.2&&dot(p-J[4],normalize(J[5]-J[4]))>-.3;
  if(m==1){
    float t=segT(p,J[0],J[1]);vec3 q=mix(b-vec3(0,0,4.3),c,smoothstep(.1,.9,t));vec3 nl=mix(Bp*n,Bc*n,t);
    float dap=smoothstep(.34,.18,voro(q.zy*2.3+q.x*.6).x)*smoothstep(-1.6,.2,q.y+.3*abs(q.z+2.))*(isHead?0.:1.);
    s.base*=1.-.10*(1.-dap)*(1.-demon);s.base*=mix(1.,.55+.6*fbm3(q*1.3),demon);
    float low=1e3;for(int k=0;k<4;k++)low=min(low,sCap(p,J[8+5*k],J[9+5*k],0.));
    s.base=mix(s.base,Pb[10],smoothstep(.55,.2,low)*.75);s.sh=mix(s.sh,Ps[10],smoothstep(.55,.2,low)*.75);
    if(isHead){float mz=smoothstep(1.55,2.2,h.z);s.base=mix(s.base,Pb[10],mz*.85);s.sh=mix(s.sh,Ps[10],mz*.85);
      float nz_=smoothstep(.03,-.03,length((vec3(abs(h.x),h.yz)-vec3(.30,-.10,2.38))*vec3(1.,.8,1.))-.15);s.base=mix(s.base,hex(0x3a1018),nz_);s.sh=mix(s.sh,hex(0x1a060c),nz_);}
    // muscle line work on shoulder, flank and thigh
    float ln=0.;vec3 sp=p-mix(J[6],J[7],.5);
    for(int k=0;k<2;k++){vec3 a=J[6+5*k],e=J[7+5*k];float v=abs(sCap(p,a,e,0.)-.96);ln=max(ln,smoothstep(.05,.015,v)*step(dot(p-a,e-a),.0+9.)*smoothstep(-.1,.4,-(p.z-e.z)+.2));}
    s.base*=1.-.35*ln*(isHead?0.:1.)*step(-1.4,q.y);
    if(harness>.5&&!isHead){
      // breast strap and girth painted as raised bands; a caparison on the back
      float bs=abs(q.y+.35+.12*(q.z-.2)*step(0.,q.z)-.0);float fr=step(-.6,q.z)*step(q.z,3.);
      float k1=smoothstep(.02,-.02,bs-.17)*step(-1.2,q.z)*step(q.z,2.6)*step(dot(p-J[2],normalize(J[3]-J[2])),.7);
      float lgd=min(sCap(p,J[7],J[8],0.),sCap(p,J[12],J[13],0.));float off=step(lgd,.66)*step(q.y,-1.0);float k2=smoothstep(.02,-.02,abs(q.z+1.05)-.16)*step(q.y,.9)*step(-2.2,q.y)*(1.-off);k1*=1.-off;
      float ed=max(smoothstep(.02,-.02,abs(bs-.14)-.03)*k1,smoothstep(.02,-.02,abs(abs(q.z+1.05)-.13)-.03)*k2);
      float st=max(k1,k2);if(st>.5){s.base=mix(clothA,hex(0xffffff),0.);s.sh=clothA*.35;s.cls=8.;s.part=20.;float dd=length(vec2(fract(q.z*2.6)-.5,(bs)*2.6));if(k1>.5&&k2<.5&&dd<.24){s.cls=2.;s.base=vec3(1);}if(ed>.5){s.cls=2.;s.base=vec3(1.05,.95,.75);}}
      float z0=-1.35,z1=-3.55;float drop=-.10-.14*abs(fract((q.z)*1.8)-.5)*2.;float cl=step(q.z,z0)*step(z1,q.z)*step(drop,q.y);
      if(cl>.5){vec2 uv=vec2((q.z-z1)/(z0-z1),(q.y-drop));s.base=clothB;s.sh=clothB*vec3(.35,.28,.4);s.cls=8.;s.part=21.;s.ink=.8;
        float e=min(min(uv.x,1.-uv.x)*2.2,uv.y);if(e<.16){s.cls=2.;s.base=vec3(1.05,.95,.72);}else if(e<.22){s.base=clothA*.6;s.cls=1.;}
        else{vec2 g=vec2(q.z*2.3,q.y*2.3);vec2 f=fract(g)-.5;float a=atan(f.y,f.x);float r=length(f);if(r<.22+.07*cos(a*6.)){s.cls=2.;s.base=vec3(1.,.92,.7);}if(r<.08){s.base=clothA;s.cls=1.;}}}
    }
    if(isHead){float sg=h.x<0.?-1.:1.;vec3 q2=vec3(abs(h.x),h.yz)-EC;vec3 d=normalize(vec3(.90,.10,.38));vec3 ex=normalize(vec3(-.38,-.04,.92)),ey=normalize(cross(d,ex));ey*=sign(ey.y);
      vec2 e=vec2(dot(q2,ex),dot(q2,ey))/.33;vec3 nn=Bh*n;if(dot(nn*vec3(sg,1,1),d)>.05&&max(abs(e.x),abs(e.y))<1.2){vec4 t2=texture(tFace,(e/1.25)*.5+.5);vec3 tc=pow(t2.rgb/max(t2.a,.003),vec3(2.2));
        if(t2.a>.35){s.base=tc;s.sh=tc*vec3(.62,.55,.62);s.cls=6.;s.ink=.25;if(demon>.5&&lum(tc)>.02&&length(e-vec2(0,.02))<.6){s.cls=4.;s.base=vec3(2.2,.5,.08)*smoothstep(.65,.1,length(e));}}}}
  }
  if(m==7){s.base*=.85+.2*sin(p.y*40.);}
  if(m==4||m==5||m==6)s.ink=.6;
}
