// THE GOLDEN DEER.  J: 0 pelvis 1 chest 2 neck root 3 neck mid 4 neck top 5 head; legs from 6 (shoulder elbow carpus fetlock hoof / hip stifle hock fetlock hoof): fl fr hl hr; 26..28 tail; 29 withers
uniform vec3 J[40];uniform mat3 Bp,Bc,Bh;uniform vec2 ear;uniform float jaw,burn,dark;uniform vec4 burnAt;uniform vec3 AT[20];
uniform sampler2D tFace;
const float HK=1.16;
const vec3 EC=vec3(.405,.07,.42);                       // eye centre (its left; mirrored)
float limbF(vec3 p,vec3 s,vec3 e,vec3 k,vec3 f,vec3 h){  // fore limb
  float d=sCone(p,s,e,.78,.50);d=smin(d,sCone(p,e,mix(e,k,.5),.45,.27),.28);d=smin(d,sCone(p,mix(e,k,.40),k,.28,.165),.12);d=smin(d,length(p-k)-.185,.08);
  d=smin(d,sCone(p,k,f,.145,.12),.06);d=smin(d,length(p-f)-.185,.08);return smin(d,sCone(p,f,h,.145,.15),.05);}
float limbH(vec3 p,vec3 s,vec3 e,vec3 k,vec3 f,vec3 h){  // hind limb
  float d=sCone(p,s,e,.98,.60);d=smin(d,sCone(p,e,mix(e,k,.5),.56,.33),.30);d=smin(d,sCone(p,mix(e,k,.45),k,.33,.185),.14);d=smin(d,length(p-k)-.215,.08);
  vec3 b=normalize(e-k);d=smin(d,sCone(p,k+normalize(k-f)*.12-vec3(0,0,.10),k-vec3(0,0,.05),.12,.15),.08);
  d=smin(d,sCone(p,k,f,.155,.125),.06);d=smin(d,length(p-f)-.19,.08);return smin(d,sCone(p,f,h,.15,.155),.05);}
float hoofD(vec3 p,vec3 f,vec3 h){vec3 a=normalize(h-f);vec3 c=h+a*.02;float d=sCone(p,c-a*.16,c+a*.02,.19,.235);
  d=smax(d,-(length((p-c-vec3(0,0,.0)).xz*vec2(1.,.12))-.018),.03);return max(d,dot(p-c,a)-.12);}
float antler(vec3 q){float d=1e3;for(int i=0;i<7;i++)d=smin(d,sCone(q,AT[i],AT[i+1],mix(.125,.05,float(i)/7.),mix(.125,.05,float(i+1)/7.)),.05);
  for(int b=0;b<3;b++)for(int i=0;i<3;i++){int k=8+b*4+i;d=smin(d,sCone(q,AT[k],AT[k+1],mix(.085,.025,float(i)/3.),mix(.085,.025,float(i+1)/3.)),.05);}return d;}
vec2 headD(vec3 h){
  vec3 q=vec3(abs(h.x),h.yz);
  float d=sEll(h-vec3(0,.02,-.02),vec3(.54,.54,.66));
  d=smin(d,sCone(h,vec3(0,-.06,.30),vec3(0,-.24,1.40),.43,.235),.22);
  d=smin(d,sEll(q-vec3(.24,-.24,.28),vec3(.22,.34,.42)),.20);
  d=smin(d,sEll(h-vec3(0,-.25,1.50),vec3(.225,.205,.25)),.12);
  float jd=jaw*.30;d=smin(d,sCone(h,vec3(0,-.44,.35),vec3(0,-.52-jd,1.34),.24,.13),.14);
  d=smin(d,sCone(q,vec3(.20,.24,.50),vec3(.48,.26,.10),.10,.10),.14);                       // brow
  d=smax(d,-sEll(q-vec3(.18,-.235,1.69),vec3(.05,.075,.10)),.05);                             // nostril
  d=smax(d,-sCone(q,vec3(.0,-.385-jd*.3,1.66),vec3(.28,-.375-jd*.15,1.12),.018,.012),.04);     // mouth line
  d=smin(d,sEll(q-EC+vec3(.03,0,.0),vec3(.23,.26,.27)),.06);                                  // eyeball
  vec2 m=vec2(d,1.);
  // ears: leaves with a hollow
  for(int s=0;s<2;s++){float sg=s==0?1.:-1.;float e=ear[s];vec3 r=vec3(h.x*sg,h.yz)-vec3(.46,.36,-.22);r.xz=rot(-.35+e*.55)*r.xz;r.xy=rot(-1.12+.14*e)*r.xy;r.yz=rot(-.30+.22*e)*r.yz;
    vec3 l=r-vec3(0,.72,0);float w=.34*smoothstep(-.95,-.1,l.y)*smoothstep(.95,.10,l.y)+.03;float tp=smoothstep(.1,.8,l.y);float en=sEll(vec3(l.x*(1.+.55*tp),l.yz),vec3(.34,.86,.18));
    float hol=sEll(vec3(l.x*(1.+.55*tp),l.y-.02,l.z-.215),vec3(.245,.72,.18));float k=smax(en,-hol,.05);float mt=l.z>-.10&&length(vec2(l.x*(1.+.55*tp),l.y-.02)/vec2(.26,.74))<1.?9.:1.;m=U(m,vec2(k*.85,mt));}
  // antlers with rings and jewels
  if(length(q-vec3(.8,1.7,-.4))<2.5){
    float an=antler(q);an-=.005*sin(q.y*30.);m=U(m,vec2(an*.9,8.));
    m=U(m,vec2(sTor(q-AT[0]-vec3(.03,.06,-.02),.145,.05),3.));
    for(int i=0;i<3;i++){int k=i==0?1:i==1?3:5;vec3 c=AT[k];vec3 ax=normalize(AT[k+1]-AT[k-1]);vec3 o=q-c;float y=dot(o,ax);float rr=length(o-ax*y);m=U(m,vec2(length(vec2(rr-.125,y))-.042,3.));
      m=U(m,vec2(length(q-c-vec3(.03,.0,.155))-.085,i==1?5.:i==0?4.:11.));}
    for(int i=0;i<4;i++){vec3 c=i==0?AT[7]:AT[11+(i-1)*4];m=U(m,vec2(length(q-c)-.075,i==0?4.:6.));}
  }else m=U(m,vec2(length(q-vec3(.8,1.7,-.4))-2.2,8.));
  // forehead jewel on a string of pearls
  vec3 f=h-vec3(0,.40,.50);f.yz=rot(.75)*f.yz;m=U(m,vec2(sEll(f,vec3(.15,.20,.07)),3.));m=U(m,vec2(sEll(f-vec3(0,0,.045),vec3(.095,.14,.06)),4.));
  return m;
}
float torso(vec3 p){
  vec3 c=Bc*(p-J[1]),h=Bp*(p-J[0]);
  float d=sEll(c-vec3(0,-.30,-.10),vec3(.98,1.52,1.45));
  d=smin(d,sEll(c-vec3(0,-.45,.85),vec3(.66,.92,.70)),.45);
  d=smin(d,sEll(c-vec3(0,.62,.05),vec3(.46,.55,1.25)),.45);
  vec3 a=J[1]-vec3(0,.10,0),b=J[0]+vec3(0,.05,0);float t=segT(p,a,b);d=smin(d,length(p-mix(a,b,t))-mix(1.20,.86,smoothstep(0.,1.,t)),.55);
  d=smin(d,sEll(h-vec3(0,.02,-.28),vec3(.98,1.06,1.18)),.5);
  return d;}
vec2 map(vec3 p){
  float d=torso(p);
  d=smin(d,sCone(p,J[2]-vec3(0,.12,0),J[3],.80,.50),.60);d=smin(d,sCone(p,J[3],J[4],.50,.37),.25);
  for(int s=0;s<4;s++){int b=6+5*s;vec3 c=mix(J[b],J[b+4],.5);float R=max(max(distance(c,J[b]),distance(c,J[b+1])),max(distance(c,J[b+2]),distance(c,J[b+3])))+1.25;if(length(p-c)-R>d+.4) continue;if(s<2)d=smin(d,limbF(p,J[b],J[b+1],J[b+2],J[b+3],J[b+4]),.30);else d=smin(d,limbH(p,J[b],J[b+1],J[b+2],J[b+3],J[b+4]),.34);}
  d=smin(d,sCone(p,J[26],J[27],.30,.26),.2);d=smin(d,sCone(p,J[27],J[28],.27,.06),.1);
  vec2 m=vec2(d,1.);
  for(int s=0;s<4;s++){int b=6+5*s;if(length(p-J[b+3])-1.3>m.x) continue;m=U(m,vec2(hoofD(p,J[b+3],J[b+4]),7.));
    vec3 a=normalize(J[b+3]-J[b+2]);vec3 o=p-mix(J[b+2],J[b+3],.80);float y=dot(o,a);float rr=length(o-a*y);m=U(m,vec2(length(vec2(rr-.17,y*.6))-.055,3.));}
  // neck band: pearls, a gold plate and a ruby
  vec3 na=normalize(J[3]-J[2]);vec3 nc=mix(J[2],J[3],.62);vec3 o=p-nc;float y=dot(o,na);vec3 rv=o-na*y;float rr=length(rv);
  if(abs(y)<.7&&rr<1.5){vec3 xx=normalize(cross(na,vec3(0,0,1)+Bc[2]*.0));vec3 zz=cross(xx,na);
    float a=atan(dot(rv,xx),dot(rv,zz));
    m=U(m,vec2(length(vec2(rr-.64,y))-.075,3.));float st=TAU/26.;float am=mod(a,st)-st*.5;m=U(m,vec2(length(vec3(am*rr,rr-.67,y+.16))-.068,6.));m=U(m,vec2(length(vec3(am*rr,rr-.60,y-.16))-.062,6.));
  }
  float dh=length(p-J[5]-(vec3(0,1.3,0))*Bh*1.)-4.1;
  if(dh<m.x){vec2 k=headD(Bh*(p-J[5])/HK);k.x*=HK;m=vec2(k.y==1.?smin(m.x,k.x,.22*step(m.y,1.5)+1e-3):min(m.x,k.x),k.x<m.x?k.y:m.y);}
  return m;
}
float spots(vec3 q,out float ring){   // chital spots in rows; q = trunk coordinates
  vec2 u=vec2(q.z*1.55+.25*sin(q.y*2.),q.y*1.75);u.x+=.5*mod(floor(u.y),2.);vec2 i=floor(u),f=fract(u)-.5;vec2 j=(h22(i+7.3)-.5)*.34;float r=.20+.10*h21(i+3.1);float d=length((f-j)*vec2(.92,1.05))-r;
  ring=smoothstep(.10,.03,abs(d-.02));return smoothstep(.02,-.02,d);}
void surf(vec3 p,vec3 n,int m,inout Surf s){
  vec3 h=Bh*(p-J[5])/HK,c=Bc*(p-J[1]),b=Bp*(p-J[0]);float hd=length(h);
  bool isHead=hd<2.2&&dot(p-J[4],normalize(J[5]-J[4]))>-.6;
  if(m==1){
    s.ink=.85;
    float t=segT(p,J[0],J[1]);vec3 q=mix(b-vec3(0,0,4.0),c,smoothstep(.1,.9,t));vec3 nl=mix(Bp*n,Bc*n,t);
    float hair=sin(q.z*9.+q.y*21.+3.*vn3(q*3.))*.5+.5;
    s.base*=mix(vec3(1.),vec3(1.0,.80,.50),.5*smoothstep(.2,.9,nl.y*.5+.5));                    // richer along the back
    s.base*=.94+.08*hair;
    float dn=1e3;for(int k=0;k<4;k++){int a=6+5*k;dn=min(dn,min(sCap(p,J[a+1],J[a+2],0.),sCap(p,J[a+2],J[a+3],0.)));}
    float low=min(min(J[10].y,J[15].y),min(J[20].y,J[25].y));
    bool leg=dn<.62&&abs(q.x)>-.1&&q.y<-1.25;
    float w=0.;                                                                                // white parts
    float zz=.16*abs(fract(q.z*2.2+.4*vn(q.zy*3.))-.5);
    bool nk=isHead&&h.z<.12;if((!isHead&&!leg)||nk){
      if(!nk)w=max(w,smoothstep(.40,.46,-nl.y+zz*.9-.10*smoothstep(-.6,.2,q.y))*step(q.y,.1));
      w=max(w,smoothstep(.66,.70,nl.z+zz-.25*smoothstep(-.4,.7,q.y))*step(.9,q.z)*step(q.y,.85));
      vec3 nd=normalize(J[3]-J[2]);float nt=dot(p-J[2],nd);
      float front=dot(n,normalize(cross(nd,cross(vec3(0,0,1),nd))));
      if(nt>.2)w=max(w,smoothstep(.50,.56,dot(n,normalize(cross(cross(nd,vec3(0,0,1)*Bh),nd)))+zz));
      vec3 rr=b-vec3(0,.15,-1.1);w=max(w,smoothstep(.0,-.06,length(rr*vec3(1.,.75,1.))-.62-zz)*step(nl.z,-.25));
    }
    if(q.y<-.9)w=max(w,smoothstep(.50,.60,-sign(q.x)*n.x+zz*.5)*smoothstep(.3,.1,-n.z-.4));
    vec3 tl=p-J[27];if(sCap(p,J[26],J[28],.0)<.36&&b.z<-1.2)w=max(w,smoothstep(.1,-.1,dot(n,normalize(cross(vec3(1,0,0),J[28]-J[26])))));
    if(isHead){
      w=max(w,smoothstep(.03,-.03,h.y+.36+.10*h.z*step(h.z,1.)+zz*.3+.9*max(0.,.30-h.z))*step(h.z,1.62));
      w=max(w,smoothstep(.04,.0,abs(h.z-1.36)-.06)*step(h.z,1.5));
      float nose=smoothstep(.02,-.02,length((h-vec3(0,-.16,1.74))*vec3(.95,1.15,1.))-.20);
      s.base=mix(s.base,vec3(1.),0.);if(nose>.5){s.base=Pb[10];s.sh=Ps[10];s.cls=Pc[10];w=0.;}
      float st=smoothstep(.10,.0,abs(h.x)-.05-.06*smoothstep(1.,.3,h.z))*step(.25,h.z)*step(h.z,1.4)*step(0.,h.y+.35);s.base*=mix(vec3(1),vec3(.72,.46,.22),st*.8);
    }
    if(w<.5&&!isHead){float rg;float sp=0.;
      if(!leg){sp=spots(q,rg)*smoothstep(-.95,-.80,q.y)*step(abs(q.x),3.);
        vec3 nd=normalize(J[3]-J[2]);float nt=dot(p-J[2],nd);float fa=step(nt,1.1);sp*=fa;rg*=fa;
        float dors=smoothstep(.16,.10,abs(q.x))*smoothstep(.3,.6,nl.y);
        s.base=mix(s.base,s.base*vec3(.62,.36,.18),max(dors*.8,rg*.55*(1.-sp)*smoothstep(-.95,-.8,q.y)));
        float ds=smoothstep(.02,-.02,length(vec2(abs(q.x)-.24,(fract(q.z*2.2)-.5)/2.2))-.085)*smoothstep(.3,.6,nl.y);sp=max(sp,ds);}
      if(sp>.5){s.base=Pb[6]*1.02;s.sh=Ps[6];s.cls=Pc[6];}
    }
    if(w>.5){s.base=Pb[2]*(.95+.06*hair);s.sh=Ps[2];s.cls=Pc[2];}
    // eye
    if(isHead){float sg=h.x<0.?-1.:1.;vec3 q2=vec3(abs(h.x),h.yz)-EC;vec3 d=normalize(vec3(.84,.14,.46));vec3 ex=normalize(vec3(-.46,.02,.84)),ey=normalize(cross(d,ex));ey*=sign(ey.y);
      vec2 e=vec2(dot(q2,ex),dot(q2,ey))/.40;
      vec3 nn=Bh*n;if(dot(nn*vec3(sg,1,1),d)>.05&&max(abs(e.x),abs(e.y))<1.2){vec4 t=texture(tFace,(e/1.25)*.5+.5);vec3 tc=pow(t.rgb/max(t.a,.003),vec3(2.2));
        if(t.a>.35){s.base=tc;s.sh=tc*vec3(.62,.55,.62);s.cls=6.;s.ink=.25;}}}
  }
  if(m==9){s.base*=.8+.35*vn3(h*8.);}
  if(m==8){s.base*=.85+.25*smoothstep(.2,.8,sin(h.y*34.)*.5+.5);}
  if(m==4||m==5||m==6||m==11)s.ink=.6;
  if(dark>0.){vec3 k=vec3(.04,.02,.03);s.base=mix(s.base,k,dark);s.sh=mix(s.sh,k*.5,dark);if(dark>.5)s.cls=1.;}
  if(burn>0.){
    float nz_=fbm3(p*1.15+3.)*.75+.25*vn3(p*5.);nz_=clamp((nz_-.22)/.56,0.,1.);
    float th=nz_; if(burnAt.w>.5)th=mix(nz_,clamp(length(p-burnAt.xyz)/7.5,0.,1.),.62);
    th=th*.93+.05;float e=th-burn*1.03;
    if(e<0.) discard;
    if(e<.035){s.cls=4.;s.base=mix(vec3(3.2,1.5,.35),vec3(1.6,.28,.03),e/.035);s.ink=0.;}
    else if(e<.10){float k=smoothstep(.10,.035,e);s.base*=mix(vec3(1.),vec3(.22,.10,.06),k);s.sh*=1.-.8*k;}
  }
}
