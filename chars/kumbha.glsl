// KUMBHAKARNA: a hill of a giant.  Figure units as for everyone; the shot scales him (12x).
#define HSC 1.42
float kBase(vec3 p){
  float jd=jaw*.26;vec3 q=vec3(abs(p.x),p.yz);
  float d=sEll(p-vec3(0,.16,-.10),vec3(.80,.82,.88));
  d=smin(d,sEll(p-vec3(0,-.36-jd*.4,.10),vec3(.86,.70+jd*.5,.64)),.28);
  d=smin(d,sEll(q-vec3(.50,-.46-jd*.3,.36),vec3(.34,.36,.34)),.16);            // hanging cheeks
  d=smin(d,sEll(p-vec3(0,-.96-jd,.36),vec3(.46,.20,.30)),.18);
  return smin(d,sEll(p-vec3(0,-1.14-jd*.7,.10),vec3(.74,.24,.46)),.10);         // second chin
}
float kFace(vec3 p){
  float d=kBase(p);vec3 q=vec3(abs(p.x),p.yz);float jd=jaw*.24;
  d=smax(d,-sEll(q-vec3(.33,.0,.92),vec3(.24,.13,.18)),.14);
  d=smin(d,sCone(q,vec3(.06,.20,.78),vec3(.56,.25,.52),.12,.08),.12);
  d=smin(d,sEll(q-vec3(.33,-.14,.76),vec3(.22,.05,.07)),.06);                  // bags under the eyes
  float n=sCone(p,vec3(0,.10,.76),vec3(0,-.24,.93),.085,.155);n=smin(n,length(q-vec3(.19,-.32,.82))-.135,.07);d=smin(d,n,.09);
  d=smax(d,-sEll(q-vec3(.13,-.43,.95),vec3(.06,.05,.10)),.03);
  d=smax(d,-sCone(q,vec3(.27,-.40,.78),vec3(.48,-.72,.54),.02,.03),.10);
  float l=sCone(q,vec3(0,-.575,.80),vec3(.32,-.60,.66),.055,.03);l=smin(l,sCone(q,vec3(0,-.69-jd,.80),vec3(.28,-.65-jd,.66),.085,.04),.02);
  return smin(d,l,.05);
}
vec2 helm(vec3 h){
  vec3 q=vec3(abs(h.x),h.yz);vec3 c=h-vec3(0,.44,-.10);float r=length(c.xz/vec2(.97,1.05)),a=atan(c.x,c.z);
  float d=sEll(c-vec3(0,.04,0),vec3(.92,.86,.97));d=max(d,-(c.y-.0+.42*smoothstep(.1,-.6,h.z)));
  d=min(d,max(abs(r-.90)-.07,abs(c.y-.02+.0)-.15)-.02);d=min(d,sTor(c-vec3(0,.19,0),.90,.055));d=min(d,sTor(c-vec3(0,-.14,0),.93,.055));
  for(int i=0;i<3;i++){float f=float(i);vec3 k=polar(c,12.-2.*f,f*.3);float y=.30+.24*f,R=.90*sqrt(max(0.,1.-pow((y-.04)/.86,2.)));d=min(d,length(k-vec3(0,y,R+.02))-.055);}
  float rb=max(abs(r),0.);d=min(d,max(abs(q.x)-.075-.0,abs(length(c-vec3(0,.04,0))-.95)-.06+step(c.y,.0)*9.));
  d=min(d,sCone(c,vec3(0,.86,0),vec3(0,1.42,0),.20,.02));d=min(d,sTor(c-vec3(0,.90,0),.24,.08));
  // ear guards and a nasal leaf
  vec3 e=q-vec3(.90,-.10,-.12);e.xz=rot(.25)*e.xz;d=min(d,max(sEll(e,vec3(.12,.46,.34)),e.y-.3));d=min(d,sTor((e-vec3(.06,-.02,0)).yxz,.20,.05));
  vec3 f=h-vec3(0,.66,.86);f.yz=rot(-.12)*f.yz;d=min(d,max(max(abs(f.x)-.36*(1.-smoothstep(-.1,.62,f.y))-.02,abs(f.z)-.06),abs(f.y-.18)-.42)*.8);
  vec2 m=vec2(d*.9,3.);
  m=U(m,vec2(sEll(f-vec3(0,.12,.06),vec3(.14,.17,.10)),4.));vec3 g=polar(c,14.,PI/14.);m=U(m,vec2(sEll(g-vec3(0,.02,.95),vec3(.085,.085,.06)),4.));m=U(m,vec2(length(e-vec3(.10,-.02,0))-.12,4.));
  // great bull horns
  float hd=1e3,hb=1e3;vec3 p0=vec3(.70,.66,-.10);
  for(int i=1;i<=8;i++){float k=float(i)/8.;vec3 p1=vec3(.70+1.75*sin(k*2.0)*.95,.66+.15*k+1.75*k*k,-.10+.55*sin(k*2.6)-.1*k);float r0=.34*(1.-.93*(k-.125)),r1=.34*(1.-.93*k);float s=sCone(q,p0,p1,r0,r1);hd=min(hd,s);if(i==2||i==5)hb=min(hb,ringD(q,p1,normalize(p1-p0),r1+.02,.10,.05));p0=p1;}
  hd-=.022*sin(length(q-vec3(.7,.5,-.1))*17.);
  m=U(m,vec2(hd*.8,6.));return U(m,vec2(hb,3.));
}
vec2 kHead(vec3 h){
  vec3 q=vec3(abs(h.x),h.yz);float sk=kFace(h);
  if(sk>3.) return vec2(sk-2.3,1.);
  sk=smin(sk,earsD(h,1.8),.04);vec2 m=vec2(sk,1.);
  m=U(m,vec2(smin(sCone(q,vec3(.33,-.76-jaw*.24,.68),vec3(.50,-.56,.76),.105,.085),sCone(q,vec3(.50,-.56,.76),vec3(.56,-.24,.72),.085,.012),.10),6.));
  // brows like thatch, and a two-forked beard in bone rings
  float br=sCone(q,vec3(.08,.17,.88),vec3(.40,.31,.80),.075,.090);br=smin(br,sCone(q,vec3(.40,.31,.80),vec3(.84,.16,.54),.090,.02),.08)-.022*sin(q.x*42.+h.y*26.);m=U(m,vec2(br*.8,2.));
  float bd=sEll(h-vec3(0,-1.22-jaw*.26,.34),vec3(.86,.52,.50));bd=max(bd,-(h.y+.98+jaw*.26-.45*q.x*q.x+.0)*-1.+0.);bd=smin(bd,sCone(q,vec3(.30,-1.35-jaw*.26,.55),vec3(.40,-2.25-jaw*.2,1.42),.40,.13),.16);bd=smin(bd,sCone(q,vec3(.62,-.50,.30),vec3(.46,-1.15-jaw*.2,.36),.13,.22),.16);
  bd-=.030*sin(h.x*24.+sin(h.y*6.)*2.)+.012*sin(h.x*61.+h.y*9.);m=U(m,vec2(bd*.75,2.));
  m=U(m,vec2(ringD(q,vec3(.375,-2.0-jaw*.2,1.18),normalize(vec3(.1,-.90,.87)),.22,.10,.06),6.));
  float hr=sEll(h-vec3(0,-.30,-.46),vec3(.88,1.0,.60));hr=smax(hr,h.z+.02,.1)-.045*sin(atan(h.x,h.z)*13.+h.y*4.);m=U(m,vec2(hr*.8,2.));
  vec3 e=q-vec3(.92,-.78,-.06);m=U(m,vec2(length(vec2(length(e.yz)-.26,e.x))-.075,6.));
  return U(m,helm(h));
}
float bellyD(vec3 p){vec3 h=Bp*(p-J[0]);return sEll(h-vec3(0,1.30,.85),vec3(2.80,2.40,2.55));}
float hull(vec3 p){
  float td=torsoD(p);
  float d=smin(td,bellyD(p),.55);
  vec3 c=Bc*(p-J[1]);vec3 q=vec3(abs(c.x),c.yz);
  d=smin(d,sEll(q-vec3(.95,.10,1.30),vec3(1.0,.70,.62)),.16);                  // heavy breast
  d=smin(d,sEll(c-vec3(0,1.20,-.75),vec3(2.9,1.0,1.15)),.45);                   // hump of the shoulders
  vec3 h=Bp*(p-J[0]);d=smax(d,-sEll(h-vec3(0,1.05,3.40),vec3(.18,.22,.30)),.12);
  return d;
}
vec2 bell(vec3 b,float s){b/=s;float r=length(b.xz);float prof=.20+.16*smoothstep(.1,-.42,b.y)+.06*smoothstep(-.32,-.46,b.y);float d=max(r-prof,max(b.y-.20,-b.y-.46));d=smax(d,length(b-vec3(0,.02,0))-.52,.1);return U(vec2(d*s*.8,3.),vec2((length(b-vec3(0,-.50,0))-.11)*s,9.));}
vec2 map(vec3 p){
  float hub=length(p-mix(J[0],J[1],.5))-4.6,td=1e3;vec2 m=vec2(hub,1.);
  if(hub<.6){td=hull(p);m.x=smin(td,neckD(p),.2);}
  float ab=min(min(sCap(p,J[4],J[5],1.45),sCap(p,J[5],J[6],1.25)),min(sCap(p,J[7],J[8],1.45),sCap(p,J[8],J[9],1.25)));ab=min(ab,min(length(p-J[6]),length(p-J[9]))-3.2);bool arm=ab<.5;
  if(arm){float a=min(armD(p,J[4],J[5],J[6],B[5]),armD(p,J[7],J[8],J[9],B[5]));a=smin(a,min(handD(p,0),handD(p,1)),.14);m.x=smin(m.x,a,.30);}else m=U(m,vec2(ab,1.));
  float lb=min(min(sCap(p,J[10],J[11],2.0),sCap(p,J[11],J[12],1.5)),min(sCap(p,J[14],J[15],2.0),sCap(p,J[15],J[16],1.5)));lb=min(lb,min(sCap(p,J[12],J[13],.9),sCap(p,J[16],J[17],.9)));lb=min(lb,length(p-J[0])-3.4);lb=min(lb,sCap(p,J[0],.5*(J[12]+J[16])+pZ*1.5,1.9));bool low=lb<.5;
  if(low){float lg=min(legD(p,J[10],J[11],J[12],B[6]),legD(p,J[14],J[15],J[16],B[6]));lg=smin(lg,min(footD(p,J[12],J[18],J[13],B[6]),footD(p,J[16],J[19],J[17],B[6])),.14);m.x=smin(m.x,lg,.25);}else m=U(m,vec2(lb,1.));
  float nb=sCap(p,J[2],J[3],1.5);if(hub>=.6){if(nb<.5) m.x=smin(m.x,neckD(p),.2);else m=U(m,vec2(nb,1.));}
  {vec3 h=Bh*(p-J[3])/HSC;float hb=length(h-vec3(0,.2,0))-3.2;if(hb>.4) m=U(m,vec2(hb*HSC+.1,1.));else{vec2 r=kHead(h);r.x*=HSC;if(r.y<1.5) m=vec2(smin(m.x,r.x,.08),m.y);else m=U(m,r);}}
  vec3 c=Bc*(p-J[1]);
  if(hub<.6){
  // harness crossed on the chest, gold bosses
  float s1=dot(c-vec3(0,.05,0),normalize(vec3(.62,.78,0.))),s2=dot(c-vec3(0,.05,0),normalize(vec3(-.62,.78,0.)));
  float up=max(c.y-1.5,-1.75-c.y);
  float st=max(abs(td-.05)-.06,min(max(abs(s1)-.24,up),max(abs(s2)-.24,up)));m=U(m,vec2(st*.8,9.));
  {float lo=min(abs(abs(s1)-.21),abs(abs(s2)-.21));m=U(m,vec2(max(length(vec2(lo,td-.11))-.04,up)*.8,3.));}
  vec3 bo=c-vec3(0,.05,0);bo.z-=1.36;m=U(m,vec2(max(length(bo.xy)-.56,abs(td-.10)-.12)*.8,3.));m=U(m,vec2(max(abs(length(bo.xy)-.56)-.05,abs(td-.17)-.07)*.8,3.));m=U(m,vec2(length(vec3(bo.xy,(td-.16)*1.6))-.26,4.));{float an=atan(bo.x,bo.y),sg=TAU/10.;an=mod(an+sg*.5,sg)-sg*.5;float r=length(bo.xy);m=U(m,vec2(length(vec3(sin(an)*r,cos(an)*r-.42,td-.22))-.06,6.));}
  // necklace of tusks
  {vec2 q=c.xy-vec2(0,2.25);float l=length(q);float a=atan(q.x,-q.y),sg=TAU/26.;float ia=floor(a/sg+.5);float af=a-ia*sg;float lift=td-.16;vec3 t=vec3(af*l,l-1.95,lift);float tk=sCone(t,vec3(0,-.12,0),vec3(0,.52,.02),.13,.02);tk=max(tk,-c.z*.8-.1);m=U(m,vec2(tk*.75,6.));m=U(m,vec2((length(vec2(l-1.80,td-.08))-.10+max(0.,-c.z-.2))*.8,9.));}
  }
  // arm rings of bone and gold, wrist guards, ankle bells
  for(int s=0;s<2;s++){if(arm){vec3 e0=s==0?J[4]:J[7],e1=s==0?J[5]:J[8],e2=s==0?J[6]:J[9];vec3 u=normalize(e1-e0),v=normalize(e2-e1);
    m=U(m,vec2(ringD(p,mix(e0,e1,.56),u,.42*B[5],.20,.05),3.));m=U(m,vec2(min(ringD(p,mix(e0,e1,.44),u,.44*B[5],.07,.07),ringD(p,mix(e0,e1,.68),u,.42*B[5],.07,.07)),6.));
    vec3 w=p-mix(e1,e2,.74);float wy=dot(w,v);vec3 wr=w-v*wy;m=U(m,vec2(ringD(p,mix(e1,e2,.74),v,.29*B[5],.42,.05),9.));m=U(m,vec2(min(ringD(p,mix(e1,e2,.60),v,.34*B[5],.06,.06),ringD(p,mix(e1,e2,.88),v,.25*B[5],.06,.06)),3.));
    vec3 sx=normalize(cross(v,cZ+.01)),sz=cross(sx,v);float an=atan(dot(wr,sx),dot(wr,sz)),sg=TAU/8.;an=mod(an,sg)-sg*.5;float r=length(wr);m=U(m,vec2(sCone(vec3(sin(an)*r,wy,cos(an)*r),vec3(0,0,.27*B[5]),vec3(0,-.05,.27*B[5]+.34),.10,.015),3.));
    }if(!low) continue;vec3 l0=s==0?J[11]:J[15],l1=s==0?J[12]:J[16];vec3 ld=normalize(l1-l0);vec3 ac=mix(l0,l1,.90);m=U(m,vec2(ringD(p,ac,ld,.31*B[6],.08,.07),9.));
    vec3 o=p-ac;float oy=dot(o,-ld);vec3 ox=normalize(cross(ld,pZ+.01)),oz=cross(ox,ld);vec3 ol=o+ld*oy;vec3 pk=vec3(dot(ol,ox),oy,dot(ol,oz));vec3 b=polar(pk,9.,0.)-vec3(0,-.10,.31*B[6]+.12);if(length(b)<.9) m=U(m,bell(b,.42));
    m=U(m,vec2(ringD(p,mix(l0,l1,.10),ld,.47*B[6],.22,.05),3.));}
  if(!low) return m;
  // hide about the loins, belt of bells
  vec3 loc;float dt;
  {vec3 hL=J[10],kL=mix(J[10],J[11],.92),hR=J[14],kR=mix(J[14],J[15],.92);float tl=segT(p,hL,kL),tr=segT(p,hR,kR);float dl=length(p-mix(hL,kL,tl)),dr=length(p-mix(hR,kR,tr));bool lf=dl<dr;vec3 a=lf?hL:hR,b=lf?kL:kR;vec3 ax=normalize(b-a),sx=normalize(cross(ax,pZ+vec3(1e-3))),sz=cross(sx,ax);vec3 o=p-a;float ang=atan(dot(o,sx),dot(o,sz));loc=vec3(lf?tl:tr,ang,0.);
    dt=smin(dl-mix(.70,1.06,tl)*B[6],dr-mix(.70,1.06,tr)*B[6],.6);vec3 q=Bp*(p-J[0]);dt=smin(dt,sEll(q-vec3(0,-.20,.05),vec3(1.95,1.0,1.80)),.5)-.035*sin(ang*9.+loc.x*4.)*loc.x;float cut=dot(p-b,ax)+.22*sin(ang*5.)+.12*sin(ang*13.);dt=smax(dt,cut,.04);dt=max(dt,q.y-.10-2.*smoothstep(2.2,3.0,q.z)+.45*smoothstep(.6,1.8,q.z))*.75;}
  m=U(m,vec2(dt,7.));
  vec3 q=Bp*(p-J[0]);float by=q.y+.15+.55*smoothstep(.2,1.9,q.z);vec3 qb=vec3(q.x,by,q.z*1.06-.06);float hug=min(td,dt);float lim=length(q)-3.4;m=U(m,vec2(max(max(abs(hug-.08)-.09,abs(by)-.22),lim)*.7,9.));m=U(m,vec2(max(length(vec2(abs(by)-.24,hug-.17))-.08,lim)*.7,3.));
  {vec3 b=polar(vec3(qb.x,qb.y,qb.z*(q.z<0.?1.12:1.)),18.,0.)-vec3(0,-.36,2.13);if(length(b)<1.3) m=U(m,bell(b,.78));}
  {vec3 b=q-vec3(0,-.66,2.10);m=U(m,vec2(sEll(b,vec3(.62,.60,.26)),3.));m=U(m,vec2(sEll(b-vec3(0,.04,.22),vec3(.28,.26,.14)),4.));vec3 bq=vec3(abs(b.x),b.yz);m=U(m,vec2(sCone(bq,vec3(.40,.20,.10),vec3(.86,.62,.18),.16,.03),6.));}
  vec3 a=J[0]-pY*.95+pZ*2.0,kn=.5*(J[11]+J[15]);vec3 b=mix(kn,.5*(J[12]+J[16]),.15)+pZ*1.5+Wind*.5;vec2 pl;m=U(m,vec2(pleatD(p,a,b,.55,.95,pl),8.));
  return m;
}
void surf(vec3 p,vec3 n,int m,inout Surf s){
  vec3 h=Bh*(p-J[3])/HSC;vec3 c=Bc*(p-J[1]);
  if(m==1){
    float isH=smoothstep(-1.35,-1.2,h.y)*step(length(h),1.8)*smoothstep(.12,.04,kFace(h));
    float w=1.;
    if(isH>0.){vec2 k=vec2(1,-1)*.03;vec3 nb=normalize(k.xyy*kBase(h+k.xyy)+k.yyx*kBase(h+k.yyx)+k.yxy*kBase(h+k.yxy)+k.xxx*kBase(h+k.xxx));
      s.ns=normalize(mix(n,transpose(Bh)*nb,.45*isH*smoothstep(-.4,.2,h.z)));
      vec4 d=faceDecal(h);float v=isH*smoothstep(.02,.22,h.z);s.base=mix(s.base,d.rgb,d.a*v);s.sh=mix(s.sh,d.rgb*vec3(.48,.42,.55),d.a*v);s.ao*=1.-.2*smoothstep(.3,.8,d.a)*v;w=1.-d.a*v;}
    // folded hide: cracks, warts, pale belly
    vec3 l=Bp*(p-J[0]);float cr=abs(vn3(p*1.7+2.*vn3(p*.8))-.5);float k1=smoothstep(.030,.006,cr)*smoothstep(.35,.6,vn3(p*.7+9.));float cr2=abs(vn3(p*4.6+7.)-.5);float k2=smoothstep(.045,.01,cr2)*smoothstep(.55,.75,vn3(p*1.1));
    float bl=smoothstep(.30,-.10,bellyD(p))*smoothstep(.5,1.6,l.z)*(1.-isH);s.base=mix(s.base,s.base*1.35+.012,bl*.6);
    s.base*=1.-.10*smoothstep(.45,.75,vn3(p*.9));
    float ik=max(k1,k2*.7)*w;vec3 b=vec3(abs(c.x),c.yz);
    ik=max(ik,max(neckInk(c)*step(isH,.01),(1.-isH)*smoothstep(.06,.02,abs(length((b.xy-vec2(.95,.18))*vec2(.9,1.2))-.80))*step(b.y,.0)*step(.5,c.z)));
    for(int i=0;i<3;i++){float y=.15+.46*float(i);ik=max(ik,smoothstep(.04,.01,abs(l.y-y-.10*l.x*l.x*.4-.05*vn(l.xy*3.)))*smoothstep(2.0,1.1,abs(l.x))*step(1.2,l.z)*.55*(1.-isH));}
    s.base=mix(s.base,s.sh*.65,ik*.8);s.sh*=1.-.5*ik;
  }
  if(m==2){float st=sin(h.x*41.*sign(h.x)+h.y*12.+6.*vn3(h*4.));s.base*=1.+.5*smoothstep(.6,1.,st);}
  if(m==6){float g=vn3(p*vec3(2.,7.,2.));s.base*=.82+.3*g;s.sh*=.8+.3*g;}
  if(m==7){vec3 l=Bp*(p-J[0]);float w=sin(l.y*4.2+2.2*vn(l.xz*1.6)+1.2*sin(l.x*2.));float st=smoothstep(.45,.65,w);s.base=mix(s.base,hex(0x1c120e),st*.85);s.sh=mix(s.sh,hex(0x0c0808),st*.85);float fr=vn3(p*vec3(9.,2.,9.));s.base*=.8+.35*fr;s.ink=.85;}
  if(m==8){vec3 l=Bp*(p-J[0]);float bb=step(.35,fract(l.y*.8))*step(fract(l.y*.8),.50);s.base=mix(s.base,hex(0xd8a23a),bb);s.base*=.93+.1*sin(l.x*20.);}
  if(m==9){float g=vn3(p*4.);s.base*=.8+.35*g;}
}
