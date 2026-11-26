// RAKSHASAS.  KIND 0 tusked, 1 horned, 2 archer, 3 hulk, 4 Maricha, 5 Indrajit.  SBOW = the serpent bow on its own.
#ifndef KIND
#define KIND 0
#endif
#ifdef SBOW
float gW;
float limbS(vec3 p,out float u,out vec3 q){q=vec3(p.x,abs(p.y),p.z);float L=pr[1],pl=clamp((pr[0]-1.0)/3.,0.,1.2);float d=1e3;u=0.;vec3 a=vec3(0);
  for(int i=1;i<=13;i++){float k=float(i)/13.;vec3 b=vec3(0,L*k*(1.-.10*pl*k),-(.95+.95*pl)*k*k+.62*sin(k*PI*.98)*(.65-.35*pl)+.40*smoothstep(.78,1.,k)+.16*sin(k*22.)*k*(1.-k)*2.);
    float r=.23*(1.-.50*k)+.05*sin(k*PI);float t=segT(q,a,b);float dd=length(q-mix(a,b,t))-r;if(dd<d){d=dd;u=k-(1.-t)/13.;}a=b;}
  return d;}
vec3 tipS(){float L=pr[1],pl=clamp((pr[0]-1.0)/3.,0.,1.2);return vec3(0,L*(1.-.10*pl),-(.95+.95*pl)+.62*sin(PI*.98)*(.65-.35*pl)+.40);}
vec2 map(vec3 p){float u;vec3 q;float d=limbS(p,u,q);vec2 m=vec2(d-.012*sin(u*130.),9.);
  m=U(m,vec2(sCap(q,vec3(0),vec3(0,.55,0),.22),12.));m=U(m,vec2(sTor(q-vec3(0,.62,.05),.22,.08),3.));
  vec3 t=tipS();vec3 h=q-t-vec3(0,.10,.10);h.yz=rot(.5)*h.yz;                      // a hooded head at each tip
  float hd=sEll(h-vec3(0,.20,0),vec3(.46*smoothstep(-.5,.3,h.y+.1)+.05,.42,.12));hd=smin(hd,sEll(h-vec3(0,.62,.08),vec3(.17,.24,.15)),.12);m=U(m,vec2(hd*.8,9.));
  m=U(m,vec2(length(vec3(abs(h.x)-.10,h.y-.66,h.z-.19))-.055,4.));m=U(m,vec2(sEll(h-vec3(0,.34,.13),vec3(.11,.14,.06)),5.));m=U(m,vec2(sCone(h,vec3(0,.84,.10),vec3(0,1.12,.22),.03,.012),4.));
  m=U(m,vec2(sCap(q,t,vec3(0,0,-pr[0]),.026),13.));return m;}
void surf(vec3 p,vec3 n,int m,inout Surf s){if(m==9){float u;vec3 q;limbS(p,u,q);vec2 g=vec2(u*34.,atan(q.x,n.z)*3.);g.y+=.5*mod(floor(g.x),2.);vec2 f=fract(g)-.5;float l=length(f*vec2(1.,.9));s.base*=.62+.55*smoothstep(.55,.2,l);s.base=mix(s.base,hex(0xd8c25a),smoothstep(.9,1.,sin(u*40.))*.7);}}
#else
uniform int hold,shield;            // hold 0 nothing 1 spear 2 sword 3 club 4 bow (left hand, string to the right) ; shield 1 on the left forearm
uniform float gild;                 // Maricha: how much of the golden deer is still on him
// ---------------------------------------------------------------- weapons, grip at the origin, +y up
vec2 rkWeapon(vec3 w,int kd){
  vec2 m=vec2(1e3,10.);
  if(kd==1){m=vec2(sCap(w,vec3(0,-4.2,0),vec3(0,4.6,0),.095),11.);vec3 q=w-vec3(0,5.5,0);float wd=.40*smoothstep(1.1,-.3,q.y)*smoothstep(-1.,-.5,q.y);vec2 e=abs(q.xz)-vec2(wd,.07);m=U(m,vec2(max(length(max(e,0.))+min(max(e.x,e.y),0.),abs(q.y)-1.05)*.6,10.));m=U(m,vec2(length(w-vec3(0,4.4,0))-.22,3.));m=U(m,vec2(sEll(w-vec3(0,4.0,0),vec3(.24,.34,.24)),8.));}
  else if(kd==2){m=vec2(sCap(w,vec3(0,-.6,0),vec3(0,.4,0),.15),9.);m=U(m,vec2(length(w-vec3(0,-.75,0))-.22,3.));m=U(m,vec2(sBox(w-vec3(0,.52,0),vec3(.58,.11,.18),.08),3.));vec3 q=w;q.x-=.075*q.y*q.y*.5;float wd=mix(.22,.52,smoothstep(.8,4.2,q.y))*smoothstep(5.0,4.2,q.y);vec2 e=abs(q.xz)-vec2(wd,.055);m=U(m,vec2(max(length(max(e,0.))+min(max(e.x,e.y),0.),abs(q.y-2.7)-2.2)*.6,10.));}
  else if(kd==3){float r=mix(.16,.62,smoothstep(.2,3.4,w.y));float d=max(length(w.xz)-r,max(1.0-w.y,w.y-3.75))-.06;d=min(d,sCap(w,vec3(0,-1.,0),vec3(0,1.6,0),.17));m=vec2(d*.8,11.);for(int i=0;i<3;i++){float y=1.9+.75*float(i);vec3 b=polar(vec3(w.x,w.y-y,w.z),6.,float(i)*.5);float R=mix(.16,.62,smoothstep(.2,3.4,y));m=U(m,vec2(sCone(b,vec3(0,0,R-.05),vec3(0,.05,R+.36),.13,.02),10.));}m=U(m,vec2(sTor(w-vec3(0,1.45,0),.40,.10),3.));m=U(m,vec2(length(w-vec3(0,-1.,0))-.24,3.));}
  return m;
}
// ---------------------------------------------------------------- heads
float rkSkull(vec3 h){
  float d=headHuman(h);vec3 q=vec3(abs(h.x),h.yz);
#if KIND<4
  d=smin(d,sCone(q,vec3(.06,.19,.76),vec3(.52,.24,.52),.10,.07),.10);                  // brow shelf
  d=smin(d,sEll(h-vec3(0,-.27,.86),vec3(.20,.13,.14)),.10);                            // broad nose
  d=smin(d,sEll(h-vec3(0,-.86-jaw*.2,.48),vec3(.46,.20,.28)),.16);                     // underhung jaw
  d=smax(d,-sEll(q-vec3(.11,-.36,.98),vec3(.055,.05,.10)),.03);
#elif KIND==4
  d=smin(d,sCone(q,vec3(.06,.19,.75),vec3(.50,.28,.52),.085,.05),.10);
  d=smax(d,-sEll(q-vec3(.52,-.48,.46),vec3(.16,.30,.22)),.16);                          // hollow cheeks
#endif
  return d;
}
vec2 rkHead(vec3 h){
  vec3 q=vec3(abs(h.x),h.yz);
  float sk=rkSkull(h);
  if(sk>2.2) return vec2(sk-1.3,1.);
  sk=smin(sk,earsD(h,.2),.04);
#if KIND!=5
  sk=smin(sk,sCone(q,vec3(.76,.04,-.06),vec3(1.16,.44,-.30),.13,.02),.08);
#endif
  vec2 m=vec2(sk,1.);
#if KIND==0
  m=U(m,vec2(smin(sCone(q,vec3(.23,-.68-jaw*.2,.72),vec3(.33,-.46,.84),.075,.062),sCone(q,vec3(.33,-.46,.84),vec3(.30,-.22,.87),.062,.010),.08),6.));
  vec3 c=h-vec3(0,.06,-.10);float hp=sEll(c,vec3(.86,1.06,.95));hp=max(hp,-(h.y-.36+.55*smoothstep(.15,-.5,h.z)));m=U(m,vec2(hp,5.));
  vec3 cr=h-vec3(0,.36,-.08);m=U(m,vec2(max(abs(length(cr.xz/vec2(.95,1.05))-.80)-.05,abs(cr.y-.04*0.)-.11)-.02,3.));vec3 b=polar(cr,10.,0.);m=U(m,vec2(length(b-vec3(0,0,.86))-.085,4.));
  m=U(m,vec2(sCone(h,vec3(0,.90,-.12),vec3(0,1.35,-.14),.26,.16),3.));
  vec3 k=h-vec3(0,1.45,-.18);float an=atan(k.x,k.z);float tk=sCone(k,vec3(0,0,0),vec3(0,.50,-.28),.20,.34);tk=smin(tk,sCone(k,vec3(0,.50,-.28),vec3(0,.25,-1.1),.34,.10),.25)-.03*sin(an*9.+k.y*4.);m=U(m,vec2(tk*.85,2.));
#elif KIND==1
  m=U(m,vec2(sCone(q,vec3(.19,-.64-jaw*.2,.76),vec3(.22,-.40,.86),.06,.012),6.));
  {float hd=1e3;vec3 a=vec3(.44,.70,.16);float an=0.;for(int i=1;i<=7;i++){float k=float(i)/7.;vec3 b=vec3(.44+1.0*sin(k*2.1)*.9,.70+.35*k+.95*k*k,.16-.55*sin(k*2.6)+.75*k*k);float r=.22*(1.-.86*k);hd=min(hd,sCone(q,a,b,.22*(1.-.86*(k-1./7.)),r));a=b;}hd-=.02*sin(length(q-vec3(.4,.6,.3))*26.);m=U(m,vec2(hd*.85,6.));}
  float mane=sEll(h-vec3(0,.10,-.22),vec3(.98,1.0,.92));mane=smin(mane,sEll(h-vec3(0,-.55,-.50),vec3(.95,1.05,.50)),.3);mane=smax(mane,h.z-.26+.55*smoothstep(.5,-.2,h.y),.1);float ma=atan(h.x,h.z+.2);mane-=.09*sin(ma*11.+h.y*3.)+.03*sin(ma*25.-h.y*9.);m=U(m,vec2(mane*.7,2.));
  m=U(m,vec2(max(abs(length(vec3(h.x/.95,h.y-.50+.1*h.z,(h.z+.08)/1.05).xz)-.83)-.04,max(abs(h.y-.50+.10*h.z)-.09,.18-h.z))-.02,3.));m=U(m,vec2(sEll(h-vec3(0,.46,.84),vec3(.14,.17,.07)),4.));
#elif KIND==2
  float hr=sEll(h-vec3(0,.16,-.14),vec3(.81,.88,.88));hr=smax(hr,-(h.y-.40+.60*smoothstep(.2,-.6,h.z)),.06);hr-=.016*sin(atan(h.x,h.z)*30.);m=U(m,vec2(hr,2.));
  vec3 k=h-vec3(0,1.02,-.30);float tk=sCone(k,vec3(0,0,0),vec3(0,.35,-.25),.17,.22);tk=smin(tk,sCone(k,vec3(0,.35,-.25),vec3(0,-.6,-.95),.22,.17),.2);tk=smin(tk,sCone(k,vec3(0,-.6,-.95),vec3(.1,-2.2,-.75),.17,.05),.2)-.02*sin(k.y*9.);m=U(m,vec2(tk*.85,2.));
  m=U(m,vec2(sTor(k-vec3(0,.02,0),.19,.07),3.));
  m=U(m,vec2(max(abs(length(vec2(h.x/.96,(h.z+.08)/1.06))-.80)-.035,abs(h.y-.40-.04*cos(atan(h.x,h.z)*2.))-.075)-.02,8.));
  m=U(m,vec2(sCone(q,vec3(.14,-.62-jaw*.2,.78),vec3(.16,-.46,.84),.045,.01),6.));
#elif KIND==3
  m=U(m,vec2(sCone(q,vec3(.30,-.74-jaw*.2,.66),vec3(.42,-.36,.80),.10,.015),6.));
  m=U(m,vec2(sCone(q,vec3(.34,.74,.30),vec3(.62,1.24,.36),.18,.02),6.));
  float mo=max(abs(h.x)-.10-.03*sin(h.y*18.+h.z*14.),sEll(h-vec3(0,.16,-.10),vec3(.8,1.12,1.06)));mo=max(mo,max(-h.z*.9-h.y-.3,.66-h.y-step(h.z,.2)*9.));m=U(m,vec2(mo*.8,2.));
  m=U(m,vec2(length(vec2(length((h-vec3(0,-.46,.94)).xy)-.12,h.z-.94))-.035,3.));
#elif KIND==4
  {float hd=1e3;vec3 a=vec3(.30,.74,.26);for(int i=1;i<=6;i++){float k=float(i)/6.;float tw=k*9.;vec3 b=vec3(.30+.55*k+.10*cos(tw),.74+1.65*k,.26-.45*k+.10*sin(tw));hd=min(hd,sCone(q,a,b,.14*(1.-.8*(k-1./6.)),.14*(1.-.8*k)));a=b;}hd-=.02*sin(q.y*34.);if(h.x>0.)hd=max(hd,h.y-1.50-.45*(h.x-.5));m=U(m,vec2(hd*.85,6.));}
  float hr=sEll(h-vec3(0,.12,-.30),vec3(.86,.92,.82));hr=smax(hr,h.z-.10,.08);float ha=atan(h.x,h.z+.25);float lk=length(h.xz-vec2(0,-.28))-(.78+.30*smoothstep(.2,-1.6,h.y));lk=max(lk,max(h.y-.3,-(h.y+1.75+.5*sin(ha*13.)*sin(ha*5.))));lk=max(lk,h.z-.02+.22*smoothstep(-.4,-1.4,h.y)*0.);hr=smin(hr,lk,.1)-.07*sin(ha*17.+h.y*2.+sin(h.y*5.));m=U(m,vec2(hr*.62,2.));
  m=U(m,vec2(sCone(q,vec3(.15,-.60,.78),vec3(.16,-.72,.80),.04,.01),6.));
  m=U(m,vec2(length(vec2(length((h-vec3(.84,-.46,-.02)).xy)-.17,h.z+.02))-.035,3.));
#elif KIND==5
  vec3 o=h-vec3(0,0,-.24);float aa=atan(o.x,-o.z);float hr=sEll(h-vec3(0,.14,-.18),vec3(.82,.90,.88));hr=smax(hr,-(h.y-.50+.75*smoothstep(.25,-.4,h.z)),.08);
  float rp=.76+.26*smoothstep(0.,-1.7,h.y)-.22*smoothstep(-2.2,-3.3,h.y);float cu=max(length(o.xz*vec2(1.,1.08))-rp-.025*cos(aa*15.+sin(h.y*2.))-.012*cos(aa*41.),max(h.y-.2,-(h.y+3.0+.25*abs(sin(aa*5.)))));cu=smax(cu,o.z-.06-.10*smoothstep(-.6,-1.6,h.y),.1);hr=smin(hr,cu*.8,.08);m=U(m,vec2(hr*.9,2.));
  // a diadem of five cobra hoods
  vec3 c=h-vec3(0,.52,-.08);c.xz/=vec2(.96,1.06);float r=length(c.xz);float dd=max(abs(r-.81)-.04,abs(c.y)-.10)-.02;dd=min(dd,sTor(c-vec3(0,.11,0),.82,.04));dd=min(dd,sTor(c-vec3(0,-.11,0),.82,.04));
  float gm=1e3;for(int i=0;i<3;i++){float f=float(i);vec3 k=vec3(abs(h.x),h.yz);float an=f*.52;k=vec3(cos(an)*k.x-sin(an)*(k.z+.08),k.y-.62,sin(an)*k.x+cos(an)*(k.z+.08)-.84+.03*f);float H=(1.-.20*f);k/=H;k.yz=rot(-.14)*k.yz;
    float w=.10+.34*smoothstep(-.05,.55,k.y)*smoothstep(1.02,.62,k.y);vec2 hv=vec2(abs(k.x)-w,abs(k.z+.10*k.x*k.x)-.045);float hd=length(max(hv,0.))+min(max(hv.x,hv.y),0.)-.03;hd=max(hd,abs(k.y-.40)-.50);hd=smin(hd*.75,sCone(k,vec3(0,.72,.02),vec3(0,.90,.20),.10,.075),.10);dd=min(dd,hd*H*.8);gm=min(gm,(sEll(k-vec3(0,.52,.09),vec3(.085,.13,.05)))*H);gm=min(gm,(length(vec3(abs(k.x)-.07,k.y-.92,k.z-.22))-.032)*H);}
  m=U(m,vec2(dd*.9,3.));m=U(m,vec2(gm,4.));{vec3 bd=polar(c,20.,0.);m=U(m,vec2(sEll(bd-vec3(0,0,.85),vec3(.06,.06,.045)),4.));}
  vec3 e=q-vec3(.82,-.60,-.02);m=U(m,vec2(length(vec2(length(e.yz)-.24,e.x))-.05,3.));m=U(m,vec2(length(e-vec3(0,-.02,0))-.10,4.));
#endif
  return m;
}
// ---------------------------------------------------------------- body
#if KIND==5
float rDhoti(vec3 p,float hem,float loose,out vec3 loc){
  vec3 hL=J[10],kL=J[11],aL=J[12],hR=J[14],kR=J[15],aR=J[16];
  vec3 eL=mix(kL,aL,hem),eR=mix(kR,aR,hem);
  float sc=loose;
  float tl1=segT(p,hL,kL),tl2=segT(p,kL,eL),tr1=segT(p,hR,kR),tr2=segT(p,kR,eR);
  float l1=length(p-mix(hL,kL,tl1)),l2=length(p-mix(kL,eL,tl2)),r1=length(p-mix(hR,kR,tr1)),r2=length(p-mix(kR,eR,tr2));
  bool left=min(l1,l2)<min(r1,r2);
  vec3 h=left?hL:hR,k=left?kL:kR,e=left?eL:eR;
  vec3 ax=normalize(e-h),sx=normalize(cross(ax,pZ+vec3(1e-3)));vec3 sz=cross(sx,ax);vec3 o=p-mix(mix(h,k,left?tl1:tr1),mix(k,e,left?tl2:tr2),smoothstep(-.4,.4,left?l1-l2:r1-r2));float ang=atan(dot(o,sx),dot(o,sz));
  float ul=length(k-h),v=(min(l1,l2)<l1+1e-5&&left||!left)?0.:0.;
  float s1=left?tl1:tr1,s2=left?tl2:tr2;float u=(s1*ul+s2*length(e-k))/(ul+length(e-k));
  loc=vec3(u,ang,left?0.:1.);
  float fold=.040*sin(ang*9.+u*5.)+.016*sin(ang*21.-u*9.);fold*=smoothstep(.12,.60,u);
  float lg=B[6];float dl=sCone(p,hL,kL,.90*lg*sc,.70*lg*sc);dl=smin(dl,sCone(p,kL,eL,.70*lg*sc,.70*lg*sc),.25);
  float dr=sCone(p,hR,kR,.90*lg*sc,.70*lg*sc);dr=smin(dr,sCone(p,kR,eR,.70*lg*sc,.70*lg*sc),.25);
  float d=smin(dl,dr,.45);
  vec3 q=Bp*(p-J[0]);float hp=sEll(q-vec3(0,-.10,-.02),vec3(1.10*B[4],.78,.86));
  d=smin(d,hp,.40)-fold-.03;
  // open the hem: cut by the plane of the hem end
  float cut=left?dot(p-eL,normalize(aL-kL)):dot(p-eR,normalize(aR-kR));
  d=smax(d,cut-.02,.03);
  return max(d,q.y-.52-2.2*smoothstep(1.0,1.9,q.z))*.80;
}
#endif
// short kilt of leather strips, cut square across each thigh
float kiltD(vec3 p,out vec3 loc){
  vec3 hL=J[10],kL=mix(J[10],J[11],.86),hR=J[14],kR=mix(J[14],J[15],.86);float lg=B[6];
  float tl=segT(p,hL,kL),tr=segT(p,hR,kR);float dl=length(p-mix(hL,kL,tl)),dr=length(p-mix(hR,kR,tr));bool lf=dl<dr;
  vec3 a=lf?hL:hR,b=lf?kL:kR;vec3 ax=normalize(b-a),sx=normalize(cross(ax,pZ+vec3(1e-3))),sz=cross(sx,ax);vec3 o=p-a;float ang=atan(dot(o,sx),dot(o,sz));loc=vec3(lf?tl:tr,ang,0);
  float d=smin(dl-mix(.92,1.02,tl)*lg,dr-mix(.92,1.02,tr)*lg,.40);
  vec3 q=Bp*(p-J[0]);d=smin(d,sEll(q-vec3(0,-.10,-.02),vec3(1.10*B[4],.78,.88)),.40);
  d-=.030*abs(sin(ang*7.))*smoothstep(.1,.7,loc.x);
  float cut=dot(p-b,ax)+.16*abs(sin(ang*7.+1.57));d=smax(d,cut,.03);
  return max(d,q.y-.52-2.*smoothstep(1.,1.8,q.z))*.78;
}
vec2 map(vec3 p){
  float td=torsoD(p),sk=td;
#if KIND==4
  {vec3 c=Bc*(p-J[1]);vec3 q=vec3(abs(c.x),c.yz);float rb=sin((c.y+.30*q.x+.2)*9.5);sk+=.045*rb*smoothstep(.12,.35,q.x)*smoothstep(1.3,.9,q.x)*smoothstep(.75,.4,c.y)*smoothstep(-1.4,-1.,c.y);}
#endif
  sk=smin(sk,armD(p,J[4],J[5],J[6],B[5]),.22);sk=smin(sk,armD(p,J[7],J[8],J[9],B[5]),.22);
  sk=smin(sk,handD(p,0),.10);sk=smin(sk,handD(p,1),.10);
  float lg=min(legD(p,J[10],J[11],J[12],B[6]),legD(p,J[14],J[15],J[16],B[6]));
  lg=smin(lg,min(footD(p,J[12],J[18],J[13],B[6]),footD(p,J[16],J[19],J[17],B[6])),.10);
  sk=smin(sk,lg,.2);sk=smin(sk,neckD(p),.14);
  vec2 m=vec2(sk,1.);
  float hs=B[10]*0.+HSC;
  {vec3 h=Bh*(p-J[3])/hs;float hb=length(h-vec3(0,.35,-.2))-2.6;if(hb>.5) m=U(m,vec2(hb*hs+.1,1.));else{vec2 r=rkHead(h);r.x*=hs;if(r.y<1.5) m=vec2(smin(m.x,r.x,.06),m.y);else m=U(m,r);}}
  vec3 c=Bc*(p-J[1]);vec3 qc=vec3(abs(c.x),c.yz);
#if KIND<4
  // lamellar cuirass, bronze edges, boss
  float bot=-(c.y+1.02+.10*abs(sin(qc.x*6.))),top=c.y-.96-.46*smoothstep(.3,1.4,qc.x)+.18*smoothstep(.6,0.,qc.x);
  float arm=qc.x>.9?-(length(vec3((qc.x-1.75)*.75,qc.y-.75,qc.z+.10))-.86):-9.;float ed=max(max(bot,top),arm);
  float cu=max(abs(td-.06)-.045,ed);
  if(cu<.15){float row=fract(c.y*2.6);cu-=.030*row*step(c.y,.75);}
  m=U(m,vec2(cu*.85,5.));m=U(m,vec2((length(vec2(td-.10,ed+.02))-.07)*.85,3.));
  vec3 bo=c-vec3(0,.32,.98*B[1]+.10);m=U(m,vec2(sEll(bo,vec3(.40,.40,.16)),3.));m=U(m,vec2(sTor(bo.xzy,.40,.06),3.));m=U(m,vec2(sEll(bo-vec3(0,0,.12),vec3(.17,.17,.12)),4.));
  m=U(m,vec2(beadsD(c,td-.06,vec2(0,1.66),.85,.085,22.),6.));
  // shoulder plates
  for(int s=0;s<2;s++){vec3 e0=s==0?J[4]:J[7],e1=s==0?J[5]:J[8],e2=s==0?J[6]:J[9];vec3 u=normalize(e1-e0),v=normalize(e2-e1);vec3 o=p-e0;float ou=dot(o,u);
    if(length(o)<1.9){float pd=abs(length(o)-.53*B[5]-.10)-.05;pd=max(pd,ou-.30);vec3 ci=Bc*o;pd=max(pd,-(ci.x*(s==0?1.:-1.)+.50));float l2=abs(length(o-u*ou)-.49*B[5]-.08)-.045;l2=max(l2,abs(ou-.52)-.22);m=U(m,vec2(min(pd,l2)*.8,5.));m=U(m,vec2(length(vec2(ou-.74,length(o-u*ou)-.49*B[5]-.09))-.06,3.));
      vec3 sp=normalize((s==0?cX:-cX)*.75+cY*.7);m=U(m,vec2(sCone(o,sp*(.53*B[5]+.05),sp*(.53*B[5]+.55),.20,.02),3.));}
    m=U(m,vec2(ringD(p,mix(e1,e2,.68),v,.295*B[5],.36,.04),5.));m=U(m,vec2(min(ringD(p,mix(e1,e2,.52),v,.345*B[5],.05,.05),ringD(p,mix(e1,e2,.84),v,.255*B[5],.05,.05)),3.));
    vec3 l0=s==0?J[11]:J[15],l1=s==0?J[12]:J[16];vec3 ld=normalize(l1-l0);vec3 lo=p-mix(l0,l1,.5);float ly=dot(lo,ld);float lr=length(lo-ld*ly);float gr=max(lr-(.47-.075*ly)*B[6]-.06,abs(ly)-1.15);m=U(m,vec2(gr*.85,5.));m=U(m,vec2(length(vec2(abs(ly)-1.12,lr-(.47-.075*ly)*B[6]-.02))-.065,3.));
  }
  vec3 loc;float dt=kiltD(p,loc);m=U(m,vec2(dt,7.));
  vec3 q=Bp*(p-J[0]);vec3 qb=vec3(q.x,q.y-.50,q.z*1.18);m=U(m,vec2(ringD(qb,vec3(0),vec3(0,1,0),1.04*B[4],.17,.06)*.85,9.));m=U(m,vec2(ringD(qb,vec3(0,.20,0),vec3(0,1,0),1.06*B[4],.04,.06)*.85,3.));
  vec3 bu=q-vec3(0,.48,.94*B[4]);m=U(m,vec2(sEll(bu,vec3(.32,.30,.16)),3.));
  {vec3 bl=vec3(abs(abs(q.x)-.62)-.31,q.y-.02,0.);float bz=q.z-.92*B[4]+.35*q.x*q.x*.5;m=U(m,vec2(sEll(vec3(bl.x,q.y-.08,bz),vec3(.13,.17,.13)),3.));}
  vec3 a=J[0]+pY*.45+pZ*.92*B[4],kn=.5*(J[11]+J[15]);vec2 pl;float dp=pleatD(p,a,kn+pZ*.75-pY*.1+Wind*.4,.26,.46,pl);m=U(m,vec2(dp,8.));
#elif KIND==4
  vec3 loc;float dt=dhotiD(p,-.10,1.05,loc);float rg=dot(p-mix(J[11],J[12],.0),-pY)+.35*sin(loc.y*5.)+.2*sin(loc.y*13.);dt=max(dt,rg*.6-.05);m=U(m,vec2(dt*.8,7.));
  vec3 q=Bp*(p-J[0]);m=U(m,vec2(ringD(vec3(q.x,q.y-.50,q.z*1.2),vec3(0),vec3(0,1,0),.98*B[4],.08,.06)*.85,9.));
  m=U(m,vec2(beadsD(c,td,vec2(0,1.55),.92,.075,26.),6.));
  m=U(m,vec2(sashD(p,td,vec3(0,.15,0),normalize(vec3(.62,.78,0.)),.20+.10*sin(c.x*9.)),8.));
#else
  // dark plate with emerald scales, serpents coiled on the arms
  float bot=-(c.y+.95+.45*(1.-smoothstep(0.,1.2,qc.x))),top=c.y-.96-.46*smoothstep(.3,1.4,qc.x)+.34*smoothstep(.6,0.,qc.x);
  float arm=qc.x>.9?-(length(vec3((qc.x-1.62)*.75,qc.y-.75,qc.z+.10))-.78):-9.;float ed=max(max(bot,top),arm);
  float cu=max(abs(td-.06)-.045,ed);if(cu<.15){vec2 g=vec2(c.x*4.6,c.y*5.2);g.x+=.5*mod(floor(g.y),2.);vec2 f=fract(g)-vec2(.5,.95);cu-=.035*smoothstep(.75,.3,length(f*vec2(1.,.8)));}
  m=U(m,vec2(cu*.82,5.));m=U(m,vec2((length(vec2(td-.10,ed+.02))-.06)*.85,3.));
  vec3 bo=c-vec3(0,.30,.92*B[1]+.10);m=U(m,vec2(sEll(bo,vec3(.17,.24,.12)),4.));m=U(m,vec2(length(vec2(length(bo.xy*vec2(1.25,.92))-.26,bo.z))-.05,3.));
  m=U(m,vec2(beadsD(c,td-.06,vec2(0,1.62),.80,.065,34.),4.));m=U(m,vec2(beadsD(c,td-.06,vec2(0,1.62),1.0,.085,-1.),3.));
  for(int s=0;s<2;s++){vec3 e0=s==0?J[4]:J[7],e1=s==0?J[5]:J[8],e2=s==0?J[6]:J[9];vec3 u=normalize(e1-e0),v=normalize(e2-e1);
    vec3 o=p-e0;if(length(o)<1.7){float ou=dot(o,u);float pd=abs(length(o)-.53*B[5]-.08)-.045;pd=max(pd,ou-.36+.10*abs(sin(atan(dot(o,cZ),dot(o,cY))*4.)));vec3 ci=Bc*o;pd=max(pd,-(ci.x*(s==0?1.:-1.)+.48));m=U(m,vec2(pd*.8,5.));vec3 sp=normalize((s==0?cX:-cX)*.7+cY*.6+cZ*.3);m=U(m,vec2(length(o-sp*(.53*B[5]+.14))-.15,4.));}
    vec3 ao=p-mix(e0,e1,.60);float ay=dot(ao,u);vec3 ar=ao-u*ay;vec3 xx=normalize(cross(u,cZ+.01)),zz=cross(xx,u);float an=atan(dot(ar,xx),dot(ar,zz));float coil=length(vec2(length(ar)-.40*B[5]-.03,(mod(ay-an/TAU*.30+.15,.30)-.15)))-.085;coil=max(coil,abs(ay)-.50);m=U(m,vec2(coil*.8,3.));
    m=U(m,vec2(ringD(p,mix(e1,e2,.72),v,.28*B[5],.34,.03),5.));m=U(m,vec2(min(ringD(p,mix(e1,e2,.56),v,.33*B[5],.04,.05),ringD(p,mix(e1,e2,.88),v,.24*B[5],.04,.05)),3.));
    vec3 l0=s==0?J[11]:J[15],l1=s==0?J[12]:J[16];m=U(m,vec2(ringD(p,mix(l0,l1,.95),normalize(l1-l0),.28*B[6],.07,.05),3.));}
  vec3 loc;float dt=rDhoti(p,.74,1.03,loc);m=U(m,vec2(dt,7.));
  vec3 q=Bp*(p-J[0]);vec3 qb=vec3(q.x,q.y-.50,q.z*1.20);m=U(m,vec2(ringD(qb,vec3(0),vec3(0,1,0),1.0*B[4],.14,.05)*.85,5.));m=U(m,vec2(ringD(qb,vec3(0,-.16,0),vec3(0,1,0),1.02*B[4],.04,.06)*.85,3.));m=U(m,vec2(sEll(q-vec3(0,.48,.90),vec3(.26,.24,.14)),3.));m=U(m,vec2(sEll(q-vec3(0,.48,1.0),vec3(.12,.13,.10)),4.));
  vec3 a=J[0]+pY*.45+pZ*.86,kn=.5*(J[11]+J[15]);vec3 b=mix(kn,.5*(J[12]+J[16]),.45)+pZ*.95+Wind*.5;vec2 pl;float dp=pleatD(p,a,b,.20,.44,pl);m=U(m,vec2(dp,8.));
  // quiver
  vec3 qv=c-vec3(-.55,.35,-1.12);qv.xy=rot(.42)*qv.xy;float qr=length(qv.xz);m=U(m,vec2(max(qr-.30-.05*qv.y,abs(qv.y)-1.35)*.9,9.));m=U(m,vec2(min(sTor(qv-vec3(0,1.3,0),.37,.07),sTor(qv+vec3(0,1.2,0),.27,.07)),3.));{vec3 ar=qv-vec3(0,1.9,0);float st=TAU/5.,an=atan(ar.x,ar.z);an=mod(an,st)-st*.5;ar=vec3(sin(an),0,cos(an))*length(ar.xz)+vec3(0,ar.y,0);m=U(m,vec2(sBox(ar-vec3(0,0,.16),vec3(.03,.36,.10),.02),8.));}
#endif
#if KIND==2
  {vec3 qv=c-vec3(-.55,.30,-1.10);qv.xy=rot(.42)*qv.xy;float qr=length(qv.xz);m=U(m,vec2(max(qr-.32-.05*qv.y,abs(qv.y)-1.35)*.9,9.));m=U(m,vec2(min(sTor(qv-vec3(0,1.3,0),.39,.07),sTor(qv+vec3(0,1.2,0),.29,.07)),3.));vec3 ar=qv-vec3(0,1.9,0);float st=TAU/5.,an=atan(ar.x,ar.z);an=mod(an,st)-st*.5;ar=vec3(sin(an),0,cos(an))*length(ar.xz)+vec3(0,ar.y,0);m=U(m,vec2(sBox(ar-vec3(0,0,.18),vec3(.03,.36,.12),.02),6.));}
#endif
#if KIND<4
  float hz=B[7];
  if(hold>0&&hold<4){vec3 w=BR*(p-J[9]);w=vec3(w.y-.60*hz,w.x,w.z-.27*hz);float wb=sCap(w,vec3(0,-4.2,0),vec3(0,6.,0),1.0);m=U(m,wb>.5?vec2(wb,10.):rkWeapon(w,hold));}
  if(hold==4){vec3 w=BL*(p-J[6]);w=vec3(w.y-.60*hz,w.x,w.z-.27*hz);float k=clamp(abs(w.y)/3.6,0.,1.);float xc=.0-1.15*k*k+.45*sin(PI*k);float d=max(length(vec2(w.x-xc,w.z))-mix(.16,.08,k),abs(w.y)-3.6)*.66;m=U(m,vec2(d,11.));
    vec3 tp=vec3(-1.15,3.6,0);vec3 rh=BL*(J[9]+transpose(BR)*vec3(0,.8,.3)*hz-J[6]);rh=vec3(rh.y-.60*hz,rh.x,rh.z-.27*hz);if(length(rh)>5.5||rh.x>-.8) rh=vec3(-1.15,0,0);m=U(m,vec2(min(sCap(w,tp,rh,.03),sCap(w,vec3(tp.x,-tp.y,0),rh,.03)),6.));}
  if(shield==1){vec3 w=BL*(p-mix(J[5],J[6],.80));w=vec3(w.x,w.y,-w.z-.62);float r=length(w.xy);float dm=w.z-.34*(1.-r*r/2.6);m=U(m,vec2(max(abs(dm)-.07,r-1.62)*.8,12.));m=U(m,vec2(length(vec2(r-1.62,w.z+.0))-.11,3.));m=U(m,vec2(length(vec2(r-.95,dm-.05))-.06,3.));m=U(m,vec2(sEll(w-vec3(0,0,.38),vec3(.36,.36,.24)),3.));m=U(m,vec2(sCone(w,vec3(0,0,.5),vec3(0,0,.95),.16,.02),10.));vec3 b=polar(w.xzy,8.,.39);m=U(m,vec2(length(b-vec3(0,.17,1.3))-.11,3.));}
#endif
  return m;
}
void surf(vec3 p,vec3 n,int m,inout Surf s){
  vec3 h=Bh*(p-J[3])/HSC;vec3 c=Bc*(p-J[1]);
  if(m==1){
    float isH=smoothstep(-1.12,-1.02,h.y)*step(length(h),1.6)*smoothstep(.12,.04,rkSkull(h));
    if(isH>0.){vec2 k=vec2(1,-1)*.03;vec3 nb=normalize(k.xyy*headBase(h+k.xyy)+k.yyx*headBase(h+k.yyx)+k.yxy*headBase(h+k.yxy)+k.xxx*headBase(h+k.xxx));
      s.ns=normalize(mix(n,transpose(Bh)*nb,.60*isH*smoothstep(-.4,.2,h.z)));
      vec4 d=faceDecal(h);float v=isH*smoothstep(.02,.22,h.z);s.base=mix(s.base,d.rgb,d.a*v);s.sh=mix(s.sh,d.rgb*vec3(.48,.42,.55),d.a*v);s.ao*=1.-.2*smoothstep(.3,.8,d.a)*v;}
    float ik=max(chestInk(c),max(neckInk(c)*step(isH,.01),bellyInk(Bp*(p-J[0]))))*(1.-isH);s.base=mix(s.base,s.sh*.55,ik*.75);s.sh*=1.-.45*ik;
#if KIND<4
    float sp=smoothstep(.62,.72,vn3(p*3.1))*(1.-isH);s.base*=1.-.16*sp;
#endif
#if KIND==4
    {float g=vn3(p*1.15+3.)*.62+vn3(p*3.3)*.28+vn3(p*9.)*.10;float th=1.12-gild*1.15;float q=g-th-.30*isH*smoothstep(.2,.5,h.z);if(q>0.&&gild>0.){s.cls=2.;s.base=hex(0xffe0a8);s.sh=hex(0x805030);s.ink=.8;s.ao*=.9;}else if(gild>0.&&gild<1.&&q>-.035){s.cls=4.;s.ink=0.;s.base=mix(hex(0xff5a10),hex(0xffe080),smoothstep(-.035,0.,q))*(1.3+.6*sin(fT*13.+p.y*5.));}
     else {float rb=sin((c.y+.30*abs(c.x)+.2)*9.5);float rl=smoothstep(.55,.95,-rb)*smoothstep(.12,.35,abs(c.x))*smoothstep(1.2,.8,abs(c.x))*smoothstep(.8,.4,c.y)*smoothstep(-1.4,-1.,c.y)*step(0.,c.z)*(1.-isH);s.base*=1.-.40*rl;s.sh*=1.-.4*rl;}}
#endif
  }
  if(m==2){float st=sin(h.x*31.*sign(h.x)+h.y*16.+6.*vn3(h*3.));s.base*=1.+.45*smoothstep(.6,1.,st);}
#if KIND<4
  if(m==5){if(c.y<1.1&&c.y>-1.3&&length(p-J[4])>1.25*B[5]&&length(p-J[7])>1.25*B[5]&&abs(c.x)<1.6*B[0]){float a=atan(c.x,c.z)*7.;float row=c.y*2.6;float f=fract(row);a+=.5*mod(floor(row),2.);float ln=smoothstep(.06,.02,abs(fract(a)-.5)-.0*f)*step(c.y,.75);float lw=smoothstep(.14,.05,f)*step(c.y,.75);s.base*=1.-.55*max(ln,lw);float rv=smoothstep(.10,.06,length(vec2(fract(a+.5)-.5,(f-.62)*.9)))*step(c.y,.75);s.base=mix(s.base,hex(0xb07a3a),rv);}}
  if(m==7){vec3 loc;kiltD(p,loc);float a=loc.y*7./PI;float f=abs(fract(a)-.5);float ln=smoothstep(.43,.48,f);s.base*=1.-.6*ln;s.sh*=1.-.5*ln;float st=smoothstep(.12,.08,length(vec2((fract(a)-.5)*.9,fract(loc.x*4.+.3)-.5)));s.base=mix(s.base,hex(0xc08a3e),st);s.ink=.85;}
  if(m==12){vec3 w=BL*(p-mix(J[5],J[6],.80));float r=length(w.xy),a=atan(w.x,w.y);float pt=step(0.,sin(a*8.+r*5.));s.base=mix(s.base,s.sh*1.4,pt*step(1.02,r)*.75);float ln=smoothstep(.04,.02,abs(r-.62));s.base=mix(s.base,hex(0xd8a03a),ln);}
  if(m==6){s.base*=.85+.2*smoothstep(-.6,.6,sin(h.y*24.+h.x*6.));}
  if(m==8) s.base*=.93+.1*sin(h.x*9.);
#elif KIND==4
  if(m==7||m==8){float w=vn3(p*vec3(6.,1.,6.));s.base*=.75+.5*w;s.sh*=.75+.5*w;s.ink=.85;}
#elif KIND==5
  if(m==5){float g=smoothstep(.5,.9,vn(c.xy*3.));s.base=mix(s.base,hex(0x1f6a5c),.35*g);}
  if(m==7){vec3 loc;rDhoti(p,.74,1.03,loc);float u=loc.x,a=loc.y;float bd=smoothstep(.84,.86,u);s.base=mix(s.base,hex(0xb88a3a),bd);s.sh=mix(s.sh,hex(0x4a3018),bd);float w=sin(u*26.+sin(a*2.)*2.0);float ln=smoothstep(.93,.99,w)*(1.-bd);s.base=mix(s.base,hex(0xb8a24a),ln*.8);vec2 z=vec2(fract(a*1.91)-.5,(u-.93)*9.);float sr=abs(z.y-.28*sin(z.x*TAU))-.07;s.base=mix(s.base,hex(0x12302c),smoothstep(.03,-.02,sr)*bd);float fl=sin(a*9.+u*5.);s.base*=1.-.2*smoothstep(.55,.95,-fl)*smoothstep(.1,.5,u);s.ink=.8;}
#endif
}
#endif
