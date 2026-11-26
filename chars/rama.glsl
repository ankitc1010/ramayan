// RAMA.  look 0 = prince (crown, gold), 1 = exile (matted hair, beads, ochre cloth)
uniform int look;uniform float nocrown;   // nocrown 1 = the prince bareheaded
vec2 kirita(vec3 p){                       // tall tiered crown
  vec3 c=p-vec3(0,.0,-.08);c.xz/=vec2(.95,1.05);float r=length(c.xz),a=atan(c.x,c.z);
  float d=max(abs(r-.80)-.045,abs(c.y-.60)-.115)-.02;
  d=min(d,sTor(c-vec3(0,.48,0),.815,.045));d=min(d,sTor(c-vec3(0,.73,0),.80,.040));
  vec3 g=polar(c,28.,0.);float gem=sEll(g-vec3(0,.605,.86),vec3(.05,.065,.04));
  vec3 q=polar(c,12.,0.)-vec3(0,.90,.80);q.yz=rot(-.16)*q.yz;float pet=sEll(q,vec3(.19,.24,.05));d=min(d,max(pet,-(sEll(q-vec3(0,-.02,.045),vec3(.11,.15,.04)))));
  float gem2=sEll(q-vec3(0,-.02,.02),vec3(.06,.09,.04));
  float y=c.y-.78;float prof=.70-.36*y-.10*sin(y*9.5)*step(0.,y);prof=max(prof,.10);
  float cone=max(r-prof,max(-y,y-1.28))*.72;cone-=.02*cos(a*16.)*smoothstep(1.3,.1,y);d=min(d,cone);
  d=min(d,length(c-vec3(0,2.16,0))-.13);d=min(d,sEll(c-vec3(0,2.34,0),vec3(.06,.18,.06)));
  vec3 f=p-vec3(0,.98,.80);f.yz=rot(-.20)*f.yz;float pl=sEll(f,vec3(.27,.42,.07));pl=max(pl,-sEll(f-vec3(0,0,.07),vec3(.19,.32,.05)));d=min(d,pl);
  gem=min(gem,sEll(f-vec3(0,-.03,.04),vec3(.10,.17,.06)));
  for(int i=0;i<7;i++){float t=float(i)/6.*4.6-2.3+1.5708;gem2=min(gem2,length(f-vec3(cos(t)*.23,sin(t)*.36,.05))-.032);}
  return U(U(vec2(d,3.),vec2(gem,4.)),vec2(gem2,5.));
}
vec2 kundala(vec3 h){vec3 q=vec3(abs(h.x),h.yz)-vec3(.80,-.62,-.02);float bd=length(q)-.42;if(bd>.3) return vec2(bd,3.);
  float d=length(vec2(length(q.xy)-.19,q.z))-.055;vec3 b=polar(q.xzy,12.,0.);d=min(d,length(b-vec3(0,0,.27))-.042);
  return U(vec2(d,3.),vec2(length(q)-.10,4.));}
vec2 jata(vec3 h){                          // piled matted hair with beads
  float d=sEll(h-vec3(0,.24,-.14),vec3(.80,.84,.86));
  d=smax(d,-(h.y-.46+.42*smoothstep(.2,-.7,h.z)-.10*abs(h.x)),.10);      // hairline
  float a=atan(h.x,h.z+.1);d-=.016*sin(a*26.+h.y*5.);
  vec3 b=h-vec3(0,1.22,-.28);b.yz=rot(.28)*b.yz;float r=length(b.xz),ab=atan(b.x,b.z);
  float bun=length(vec2(r-.17,b.y+.20))-.25;bun=smin(bun,length(vec2(r-.12,b.y-.13))-.21,.05);bun=smin(bun,length(b-vec3(0,.40,0))-.17,.05);bun-=.022*sin(ab*9.+b.y*16.);
  d=smin(d,bun,.12);
  vec3 q=vec3(abs(h.x),h.yz);float lk=sCone(q,vec3(.70,.12,-.12),vec3(.80,-1.30,-.42),.15,.12);lk=smin(lk,sCone(q,vec3(.52,-.2,-.60),vec3(.66,-1.75,-.62),.32,.22),.22);lk-=.022*sin(h.y*13.+q.x*15.+q.z*6.);
  d=min(d,lk);
  vec2 m=vec2(d*.9,2.);
  vec3 p1=polar(b-vec3(0,-.02,0),14.,0.);m=U(m,vec2(length(p1-vec3(0,0,.36))-.062,9.));
  vec3 p2=polar(b-vec3(0,-.40,0),18.,0.);m=U(m,vec2(length(p2-vec3(0,0,.42))-.058,9.));
  vec3 fl=b-vec3(.20,.02,.36);float ft=atan(fl.y,fl.x);m=U(m,vec2(max(length(fl)-.15*(.75+.25*cos(ft*5.)),abs(fl.z)-.05),11.));
  return m;
}
vec2 necklaces(vec3 p,float td){
  vec3 c=Bc*(p-J[1]);
  if(look==0){
    vec2 m=vec2(beadsD(c,td,vec2(0,1.62),.60,.060,40.),6.);
    float d2=beadsD(c,td,vec2(0,1.62),.92,.085,-1.);m=U(m,vec2(d2,3.));
    m=U(m,vec2(beadsD(c,td,vec2(0,1.62),.92,.075,30.)-.0,4.));m=U(m,vec2(beadsD(c,td,vec2(0,1.62),1.10,.055,44.),3.));m=U(m,vec2(beadsD(c,td,vec2(0,1.62),1.22,.048,44.),6.));
    m=U(m,vec2(beadsD(c,td,vec2(0,1.62),1.95,.065,64.),6.));
    vec3 pd=c-vec3(0,-.34,.96*B[1]);m=U(m,vec2(sEll(pd,vec3(.22,.28,.10)),3.));m=U(m,vec2(sEll(pd-vec3(0,0,.07),vec3(.12,.17,.07)),5.));
    return m;}
  vec2 m=vec2(beadsD(c,td,vec2(0,1.55),.78,.082,30.),9.);
  m=U(m,vec2(beadsD(c,td,vec2(0,1.55),1.42,.090,44.),9.));
  m=U(m,vec2(length(c-vec3(0,.10,1.02*B[1]))-.15,9.));return m;
}
vec2 garland(vec3 p){return vec2(1e3,0.);}
vec2 map(vec3 p){
  float dh=length(p-J[3]);
  float td=torsoD(p),sk=td;
  sk=smin(sk,armD(p,J[4],J[5],J[6],B[5]),.22);sk=smin(sk,armD(p,J[7],J[8],J[9],B[5]),.22);
  sk=smin(sk,handD(p,0),.10);sk=smin(sk,handD(p,1),.10);
  float lg=min(legD(p,J[10],J[11],J[12],B[6]),legD(p,J[14],J[15],J[16],B[6]));
  lg=smin(lg,footD(p,J[12],J[18],J[13],B[6]),.10);lg=smin(lg,footD(p,J[16],J[19],J[17],B[6]),.10);
  sk=smin(sk,lg,.2);sk=smin(sk,neckD(p),.14);
  if(dh-2.9<sk){vec3 h=Bh*(p-J[3]);sk=smin(sk,smin(headHuman(h),earsD(h,1.),.04),.10);}
  vec2 m=vec2(sk,1.);
  m=U(m,vec2(sashD(p,td,vec3(0,.15,0),normalize(vec3(.62,.78,0.)),look==0?.26:.30),8.));
  if(dh-2.9<m.x){vec3 h=Bh*(p-J[3]);
    if(look==0){float hair=sEll(h-vec3(0,.10,-.30),vec3(.83,.88,.82));hair=smax(hair,-(h.y+.75+.4*h.z),.1);hair=smax(hair,h.z-.16,.1);
      vec3 hq=vec3(abs(h.x),h.yz);float lock=sCone(hq,vec3(.74,.2,.02),vec3(.86,-1.3,-.35),.10,.12);lock=smin(lock,sCone(hq,vec3(.6,-.2,-.5),vec3(.75,-1.7,-.55),.34,.26),.2);lock+=.018*sin(h.y*26.+hq.x*22.);
      if(nocrown>.5){float tp=sEll(h-vec3(0,.26,-.14),vec3(.80,.84,.86));tp=smax(tp,-(h.y-.50+.42*smoothstep(.2,-.7,h.z)-.06*abs(h.x)),.10);tp-=.012*sin(atan(h.x,h.z+.1)*30.+h.y*6.);hair=min(hair,tp);}m=U(m,vec2(min(hair,lock)*.9,2.));if(nocrown<.5)m=U(m,kirita(h));}
    else m=U(m,jata(h));
    m=U(m,kundala(h));}
  m=U(m,necklaces(p,td));
  vec3 loc;float dt=dhotiB(p,look==0?.72:.30,loc);m=U(m,vec2(dt,7.));
  // belt and front pleats
  vec3 q=Bp*(p-J[0]);float be=ringD(vec3(q.x,q.y-.50,q.z*1.22),vec3(0),vec3(0,1,0),.98*B[4],.13,.05);m=U(m,vec2(be*.85,look==0?3.:8.));
  if(look==0){vec3 bq=q-vec3(0,.48,.86);m=U(m,vec2(length(bq)-.16,4.));m=U(m,vec2(sTor(bq.xzy,.19,.05),3.));}
  vec3 a=J[0]+pY*.45+pZ*.86,kn=.5*(J[11]+J[15]);vec3 b=mix(kn,.5*(J[12]+J[16]),look==0?.45:.05)+pZ*.95+Wind*.5;vec2 pl;float dp=pleatD(p,a,b,.22,look==0?.50:.36,pl);m=U(m,vec2(dp,8.));
  // armlets, bracelets, anklets
  for(int s=0;s<2;s++){vec3 e0=s==0?J[4]:J[7],e1=s==0?J[5]:J[8],e2=s==0?J[6]:J[9];vec3 u=normalize(e1-e0),v=normalize(e2-e1);
    float r1=ringD(p,mix(e0,e1,.46),u,.385*B[5],look==0?.12:.06,.04);m=U(m,vec2(r1,look==0?3.:9.));
    float r2=ringD(p,mix(e1,e2,.88),v,.235*B[5],look==0?.16:.07,.035);m=U(m,vec2(r2,look==0?3.:9.));
    vec3 l0=s==0?J[11]:J[15],l1=s==0?J[12]:J[16];if(look==0)m=U(m,vec2(ringD(p,mix(l0,l1,.95),normalize(l1-l0),.28*B[6],.07,.05),3.));}
  return m;
}
void surf(vec3 p,vec3 n,int m,inout Surf s){
  vec3 h=Bh*(p-J[3]);
  if(m==1){
    float isH=smoothstep(-1.12,-1.02,h.y)*step(length(h),1.45);
    if(isH>0.){vec2 k=vec2(1,-1)*.03;vec3 nb=normalize(k.xyy*headBase(h+k.xyy)+k.yyx*headBase(h+k.yyx)+k.yxy*headBase(h+k.yxy)+k.xxx*headBase(h+k.xxx));
      s.ns=normalize(mix(n,transpose(Bh)*nb,.78*isH*smoothstep(-.4,.2,h.z)));
      vec4 d=faceDecal(h);float v=isH*smoothstep(.02,.22,h.z);s.base=mix(s.base,d.rgb,d.a*v);s.sh=mix(s.sh,d.rgb*vec3(.50,.45,.62),d.a*v);
      if(d.a*v>.93&&abs(abs(h.x)-.35)<.30&&abs(h.y-.15)<.24){s.cls=6.;s.ns=n;}}
    vec3 c=Bc*(p-J[1]);float ik=max(chestInk(c),max(neckInk(c)*step(isH,.01),bellyInk(Bp*(p-J[0]))))*(1.-isH);s.base=mix(s.base,hex(0x17254a),ik*.8);s.sh=mix(s.sh,hex(0x0c1330),ik*.8);
  }
  if(m==7){vec3 loc;dhotiB(p,look==0?.72:.30,loc);float u=loc.x,a=loc.y;
    float bd=smoothstep(.86,.88,u);vec3 gold=look==0?hex(0xd98a1c):hex(0x8a3a16);s.base=mix(s.base,look==0?hex(0xb3202a):hex(0xc96a24),bd);s.sh=mix(s.sh,look==0?hex(0x5a0c1c):hex(0x6a2a16),bd);
    float ln=step(.5,fract(u*60.))*step(.84,u)*step(u,.90);s.base=mix(s.base,hex(0xf2c24a),ln*(look==0?1.:.4));
    if(look==0){vec2 g=vec2(a*5.,u*16.);vec2 f=fract(g)-.5;float dot_=smoothstep(.20,.16,length(f*vec2(1.,1.3)))*step(u,.82)*step(.12,u);s.base=mix(s.base,hex(0xc2571a),dot_*.75);}
    float fl=sin(a*9.+u*5.);s.base*=1.-.18*smoothstep(.55,.95,-fl)*smoothstep(.1,.5,u);s.ink=.8;}
  if(m==8){s.base*=.92+.12*sin(h.x*9.);}
  if(m==11) s.ink=.7;
}
