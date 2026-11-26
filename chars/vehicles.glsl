// KIND 0 Rama's chariot, 1 Ravana's chariot (origin on the ground under the axle, +z forward), 2 Pushpaka (origin at the deck, +z = prow, 1 unit = 6 world units)
uniform float wheel,canopy,mood,lamps,glow;
#ifndef KIND
#define KIND 0
#endif
#if KIND<2
const float WR=5.0,FL=6.6;
float spokeD(vec2 p,float n,float r0,float r1,float w){float a=atan(p.x,p.y),s=TAU/n;a=mod(a+s*.5,s)-s*.5;float r=length(p);vec2 q=vec2(sin(a)*r,cos(a)*r);float t=clamp((q.y-r0)/(r1-r0),0.,1.);
  return length(vec2(max(abs(q.x)-w*(1.+.7*exp(-pow((t-.5)*5.,2.))),0.),q.y-mix(r0,r1,t)));}
vec2 wheelD(vec3 p){                       // axis x, centre at the origin, outside = +x
  float r=length(p.yz);if(max(r-WR-.6,abs(p.x)-1.9)>.6) return vec2(max(r-WR-.6,abs(p.x)-1.9),3.);
  vec2 q=rot(wheel)*p.zy;float ri=max(abs(r-WR+.42)-.40,abs(p.x)-.48)-.06;vec2 m=vec2(ri,9.);
  m=U(m,vec2(max(abs(r-WR+.02)-.12,abs(p.x)-.36)-.04,3.));m=U(m,vec2(length(vec2(abs(r-WR+.42)-.44,abs(p.x)-.46))-.10,3.));
  float sp=spokeD(q,KIND==0?16.:12.,1.0,WR-.7,.13);m=U(m,vec2(length(vec2(sp,max(abs(p.x)-.16,0.)))-.10,3.));
  float a=atan(q.x,q.y);
#if KIND==0
  float pet=r-1.75-.35*abs(cos(a*8.));m=U(m,vec2(max(pet,abs(p.x)-.26)*.7,3.));float pet2=r-1.15-.22*abs(sin(a*8.));m=U(m,vec2(max(pet2,abs(p.x)-.42)*.7,4.));
#else
  float as=mod(a+PI/12.,TAU/6.)-TAU/12.;vec2 bl=vec2(sin(as)*r,cos(as)*r);float bd=max(abs(bl.x)-.42*smoothstep(3.6,1.2,bl.y),abs(p.x)-.10);bd=max(bd,abs(bl.y-2.2)-1.5);m=U(m,vec2(bd*.6,7.));float pet2=r-1.35-.15*abs(sin(a*6.));m=U(m,vec2(max(pet2,abs(p.x)-.46)*.7,4.));
#endif
  float hub=max(length(p.yz)-.85+.12*abs(p.x),abs(p.x)-1.1);m=U(m,vec2(hub,3.));m=U(m,vec2(sCone(vec3(p.x,p.yz),vec3(1.0,0,0),vec3(KIND==0?1.75:2.9,0,0),.48,KIND==0?.18:.02),KIND==0?3.:7.));
  float st=mod(a+PI/16.,TAU/16.)-TAU/32.;m=U(m,vec2(length(vec3(st*r,r-WR+.42,abs(p.x)-.52))-.13,6.));
  return m;}
vec2 map(vec3 p){
  vec3 q=vec3(abs(p.x),p.yz);
  vec2 m=wheelD(q-vec3(6.1,WR,0));
  // axle, floor, lotus skirt
  m=U(m,vec2(sCap(q,vec3(0,WR,0),vec3(5.4,WR,0),.42),9.));
  float fl=sBox(p-vec3(0,FL-.25,-.4),vec3(4.5,.30,5.6),.2);m=U(m,vec2(fl,9.));
  m=U(m,vec2(sBox(p-vec3(0,FL-.28,-.4),vec3(4.75,.16,5.85),.12),3.));
  {vec3 c=vec3(p.x/4.5,p.y,(p.z+.4)/5.6);float a=atan(c.x,c.z),n=22.;float s=TAU/n,id=floor(a/s+.5);float am=a-id*s;float R=length(c.xz);vec3 l=vec3(am*4.9,p.y-FL+1.05,(R-1.)*4.9+.10+.30*(p.y-FL+1.));float w=.62*sqrt(max(.02,1.-pow((l.y-.2)/1.0,2.)));float pd=sEll(l,vec3(.66,.95,.24));if(l.y<.0)pd=max(pd,abs(l.x)-.62*smoothstep(-.95,.15,l.y));m=U(m,vec2(max(pd,p.y-FL+.35)*.62,10.));}
  // body: a curved wall open behind
  {vec2 c=vec2(p.x,p.z+.2);vec2 k=vec2(p.x/4.25,(p.z+.2)/5.2);float R=length(k);float el=(R-1.)*4.3*.86;float hgt=FL+mix(2.2,5.0,smoothstep(-2.5,4.2,p.z))+.35*smoothstep(3.6,5.2,p.z);
    el-=.35*smoothstep(FL,hgt,p.y)*smoothstep(-2.,4.,p.z);
    float wall=max(max(abs(el)-.17,max(p.y-hgt,FL-p.y)),-p.z-3.6);m=U(m,vec2(wall*.8,11.));
    float rim=length(vec2(el,p.y-hgt))-.26;rim=max(rim,-p.z-3.7);m=U(m,vec2(rim*.75,3.));
    float b1=length(vec2(max(abs(el)-.2,0.),abs(p.y-FL-.45)-.0))-.14;m=U(m,vec2(max(b1,-p.z-3.6)*.8,3.));
    float a=atan(k.x,k.y);float n=26.;float am=mod(a+PI/n,TAU/n)-PI/n;m=U(m,vec2(max(length(vec3(am*4.7,el-.18,p.y-hgt+.62))-.15,-p.z-3.4)*.8,6.));
    float n2=14.;float a3=mod(a+PI/n2,TAU/n2)-PI/n2;vec3 rz=vec3(a3*4.7,p.y-mix(FL+.5,hgt,.48),el-.12);float fl2=length(rz.xy)-.62-.14*cos(atan(rz.y,rz.x)*8.);m=U(m,vec2(max(max(fl2,abs(rz.z)-.17),-p.z-3.2)*.6,3.));m=U(m,vec2(max(length(rz-vec3(0,0,.14))-.24,-p.z-3.2)*.8,KIND==0?5.:4.));}
  // corner posts
  m=U(m,vec2(sCap(q,vec3(3.2,FL,-3.7),vec3(3.2,FL+3.4,-3.7),.22),3.));m=U(m,vec2(length(q-vec3(3.2,FL+3.7,-3.7))-.40,4.));
  // the pole to the yoke
  {float u=clamp((p.z-4.)/19.,0.,1.);vec3 c=vec3(0,FL-1.0+4.2*u*u+.9*sin(u*PI),p.z);m=U(m,vec2(max(length(p-c)-mix(.42,.26,u),max(4.-p.z,p.z-23.))*.85,9.));m=U(m,vec2(length(vec3(p.x,p.y-FL-3.2,p.z-23.1))-.55,3.));
   float br=mod(p.z,3.)-1.5;m=U(m,vec2(max(max(length(p.xy-c.xy)-mix(.50,.34,u),abs(br)-.2),max(5.-p.z,p.z-22.)),3.));}
  // figurehead on the front wall
  {vec3 f=p-vec3(0,FL+5.1,5.3);vec3 g=vec3(abs(f.x),f.yz);
#if KIND==0
   float b=sEll(f-vec3(0,-.6,.15),vec3(.75,1.1,.6));b=smin(b,sEll(f-vec3(0,.75,.35),vec3(.50,.55,.55)),.3);b=smin(b,sCone(f,vec3(0,.72,.75),vec3(0,.35,1.35),.26,.05),.1);
   for(int i=0;i<6;i++){float k=float(i);vec3 l=g-vec3(.35,-.05-.10*k,.05);l.xz=rot(.30)*l.xz;l.xy=rot(-.55-.24*k)*l.xy;float h=2.0-.14*k;b=min(b,sEll(l-vec3(0,h,-.05*k),vec3(.30,h,.10))*.9);}m=U(m,vec2(b*.85,3.));m=U(m,vec2(length(g-vec3(.30,.92,.70))-.12,4.));m=U(m,vec2(length(f-vec3(0,-.45,.75))-.24,5.));
#else
   float b=sEll(f-vec3(0,-.1,.2),vec3(1.25,1.2,.75));b=smin(b,sCone(g,vec3(.25,.55,.85),vec3(1.1,.75,.5),.20,.16),.2);b=smin(b,sEll(f-vec3(0,-.10,.95),vec3(.36,.30,.34)),.15);b=smax(b,-sEll(f-vec3(0,-.78,.85),vec3(.75,.30,.5)),.1);
   for(int i=0;i<6;i++){float a=(float(i)/5.-.5)*2.6;b=min(b,sCone(f,vec3(sin(a)*1.1,cos(a)*1.0,-.1),vec3(sin(a)*2.1,cos(a)*1.9+.2,-.5),.30,.03));}m=U(m,vec2(b*.8,3.));
   m=U(m,vec2(length(g-vec3(.48,.28,.86))-.20,12.));m=U(m,vec2(min(sCone(g,vec3(.42,-.62,.95),vec3(.40,-1.15,1.0),.11,.01),sCone(g,vec3(.16,-.60,1.02),vec3(.15,-.86,1.05),.07,.01)),13.));
   m=U(m,vec2(min(sCone(g,vec3(.9,.8,.1),vec3(1.9,1.6,.2),.28,.18),sCone(g,vec3(1.9,1.6,.2),vec3(1.75,2.9,.5),.18,.01)),7.));
#endif
  }
  // umbrella of state on a tall pole, and the banner staff
  if(canopy>.5){vec3 o=vec3(0,0,-4.8);m=U(m,vec2(sCap(p,o+vec3(0,FL,0),o+vec3(0,24.,0),.15),3.));
    vec3 c=p-o-vec3(0,21.6,0);float r=length(c.xz),a=atan(c.x,c.z);
#if KIND==0
    float d=sEll(c,vec3(6.2,2.7,6.2));d=max(abs(d)-.10,-c.y-.25-.22*abs(sin(a*12.)));d-=.06*abs(sin(a*12.))*0.;m=U(m,vec2(d*.7,14.));m=U(m,vec2(max(abs(r-6.15)-.14,abs(c.y+.05)-.16),3.));
    float n=36.;float am=mod(a+PI/n,TAU/n)-PI/n;m=U(m,vec2(length(vec3(am*6.15,c.y+.62,r-6.15))-.17,6.));m=U(m,vec2(length(vec3(am*6.15,(c.y+.95)*.6,r-6.15))-.12,3.));
    m=U(m,vec2(sEll(c-vec3(0,3.0,0),vec3(.55,.7,.55)),3.));m=U(m,vec2(sCone(c,vec3(0,3.5,0),vec3(0,4.6,0),.22,.03),3.));
#else
    for(int i=0;i<3;i++){float k=float(i);vec3 e=c-vec3(0,1.9*k,0);float R=5.9-1.6*k;float y=e.y;float prof=r-R*(1.-.62*smoothstep(0.,1.7,y))-.5*exp(-y*3.5)*step(0.,y);float d=max(prof,max(-y,y-1.7));d=max(d,-(prof+.25));m=U(m,vec2(d*.55,14.));m=U(m,vec2(length(vec2(r-R-.45,y-.02))-.14,3.));float n=24.-5.*k;float am=mod(a+PI/n,TAU/n)-PI/n;m=U(m,vec2(sCone(vec3(am*R,y,r-R-.45),vec3(0),vec3(0,-.75,.1),.13,.01),i==0?4.:3.));}
    m=U(m,vec2(sCone(c,vec3(0,5.4,0),vec3(0,8.2,0),.5,.02),3.));m=U(m,vec2(length(c-vec3(0,5.6,0))-.55,4.));
#endif
  }
  m=U(m,vec2(sCap(p,vec3(3.6,FL,-5.2),vec3(3.6,28.5,-5.2),.11),3.));m=U(m,vec2(sEll(p-vec3(3.6,28.9,-5.2),vec3(.35,.6,.35)),3.));
  return m;}
#else
// ------------------------------------------------------------------ the flower chariot
float petal(vec3 l,float w,float h,float th){      // local: x across, y up the petal (0..h), z outward normal
  float t=clamp(l.y/h,0.,1.);float ww=w*pow(sin(PI*min(t*.83+.17,1.)),.70);float z=l.z-.26*h*t*t+.35*(l.x*l.x)/max(w,.1);
  return max(max(abs(l.x)-ww,abs(z)-th),max(-l.y,l.y-h))*.62-.015;}
vec2 tier(vec3 p,float n,float R,float y0,float w,float h,float tilt,float off,float mat){   // ring of petals; p already squashed in z
  float a=atan(p.x,p.z)+off,s=TAU/n;float id=floor(a/s+.5);a-=id*s;float r=length(p.xz);vec3 l=vec3(sin(a)*r,p.y-y0,cos(a)*r-R);l.yz=rot(tilt)*l.yz;return vec2(petal(l,w,h,.055),mat);}
float ogee(vec3 p,float R){                        // onion dome on y>=0
  float r=length(p.xz),y=p.y/R;float pr=y<0.?1.:1.06*sqrt(max(0.,1.-pow((y-.28)/1.02,2.)));float tip=.42*exp(-(y-.72)*3.0);pr=mix(pr,min(pr,tip),smoothstep(.70,.98,y));
  float a=atan(p.x,p.z);float d=r-R*pr-.025*R*abs(cos(a*8.));return max(max(d,-p.y),p.y-R*1.75)*.55;}
vec2 finial(vec3 p,float s){vec2 m=vec2(length(p)-.20*s,3.);m=U(m,vec2(length(p-vec3(0,.27*s,0))-.13*s,4.));m=U(m,vec2(sCone(p,vec3(0,.3*s,0),vec3(0,.85*s,0),.09*s,.01),3.));return m;}
vec2 chhatri(vec3 p,float s){                      // a small domed pavilion, base at y=0
  p/=s;vec3 q=vec3(abs(p.x),p.y,abs(p.z));if(q.z>q.x)q.xz=q.zx;
  vec2 m=vec2(sBox(p-vec3(0,.08,0),vec3(.80,.10,.80),.03),11.);
  vec3 c=vec3(abs(p.x)-.58,p.y,abs(p.z)-.58);float pl=length(c.xz)-.085-.03*cos(p.y*14.);m=U(m,vec2(max(pl,abs(p.y-.72)-.60)*.9,3.));
  m=U(m,vec2(sBox(p-vec3(0,1.38,0),vec3(.82,.10,.82),.04),11.));m=U(m,vec2(sBox(p-vec3(0,1.30,0),vec3(.98,.035,.98),.03),3.));
  float o=ogee(p-vec3(0,1.48,0),.66);m=U(m,vec2(o,10.));vec2 f=finial(p-vec3(0,2.62,0),.5);m=U(m,f);
  m=U(m,vec2(length(p-vec3(0,.95,0))-.17,12.));m.x*=s;return m;}
vec2 map(vec3 p){
  vec3 q=vec3(abs(p.x),p.yz);vec3 sp=vec3(p.x,p.y,p.z/1.72);float r=length(sp.xz),a=atan(sp.x,sp.z);
  vec2 m=vec2(1e3,0.);
  float bd=max(r-5.9,max(-p.y-4.2,p.y-2.4));
  if(bd<.8){
    // hull: a shallow bowl, three tiers of petals above, two hanging below
    float bowl=sEll(sp-vec3(0,.15,0),vec3(4.3,2.1,4.3));bowl=max(bowl,p.y-.15);m=vec2(bowl,9.);
    m=U(m,tier(sp,18.,3.45,-.95,.92,2.75,.60,0.,13.));
    m=U(m,tier(sp,18.,3.72,-.55,.88,2.20,.26,PI/18.,14.));
    m=U(m,tier(sp,18.,3.88,-.15,.62,1.20,-.02,0.,10.));
    vec3 dn=vec3(sp.x,-sp.y,sp.z);
    m=U(m,tier(dn,18.,3.30,.50,.80,1.70,1.10,PI/18.,14.));m=U(m,tier(dn,14.,2.45,1.10,.72,1.55,.95,0.,13.));m=U(m,tier(dn,10.,1.45,1.60,.58,1.30,.70,PI/10.,14.));
    float bud=sEll(sp-vec3(0,-2.2,0),vec3(.95,1.15,.95))-.05*cos(a*10.);m=U(m,vec2(bud*.8,3.));vec2 fk=finial(vec3(p.x,-p.y-3.35,p.z/1.72),1.1);m=U(m,fk);
    // bands, beads, lamps and bells round the waist
    float rb=length(vec2(r-4.05,p.y+.22));m=U(m,vec2((rb-.16)*.9,3.));
    float n=44.;float am=mod(a+PI/n,TAU/n)-PI/n;m=U(m,vec2(length(vec3(am*4.1,p.y+.02,r-4.10))-.115,6.));
    float n2=22.;float a2=mod(a,TAU/n2)-PI/n2;m=U(m,vec2(length(vec3(a2*4.1,p.y+.55,r-4.22))-.12,12.));m=U(m,vec2(sCone(vec3(a2*4.1,p.y,r-4.20),vec3(0,-.25,0),vec3(0,-.48,0),.05,.10),3.));
    float deck=max(r-3.95,abs(p.y-.18)-.07);m=U(m,vec2(deck,11.));
    float rail=max(abs(r-3.72)-.05,abs(p.y-.72)-.06);m=U(m,vec2(rail,3.));float n3=56.;float a3=mod(a+PI/n3,TAU/n3)-PI/n3;m=U(m,vec2(max(length(vec2(a3*3.72,r-3.72))-.055,abs(p.y-.45)-.28)*.9,3.));
  } else m=vec2(bd,9.);
  // prow: a hamsa's neck and head ; stern: a fan of tail leaves
  float pb=length(p-vec3(0,2.6,8.0))-4.1;if(pb<m.x){
    float d=1e3;vec3 A0=vec3(0,-.5,5.9);for(int i=1;i<=10;i++){float u=float(i)/10.;vec3 b=vec3(0,-.5+5.2*u+.35*sin(u*5.),5.9+3.3*sin(u*2.05)-1.15*u*u+.75*pow(u,6.));d=smin(d,sCone(p,A0,b,mix(.74,.20,sqrt(u-.1)),mix(.74,.20,sqrt(u))),.08);A0=b;}
    d=smin(d,sEll(p-A0-vec3(0,.06,.16),vec3(.25,.27,.40)),.12);m=U(m,vec2(d-.012*cos(p.y*20.+p.z*8.),15.));
    vec3 hb=p-A0-vec3(0,.02,.48);float bk=sCone(hb,vec3(0),vec3(0,-.26,.62),.145,.03);m=U(m,vec2(bk,16.));vec3 he=vec3(abs(p.x),p.yz)-A0-vec3(.20,.12,.26);m=U(m,vec2(length(he)-.075,20.));
    for(int i=0;i<4;i++){float k=float(i);m=U(m,vec2(sCone(vec3(abs(p.x),p.yz)-A0,vec3(.03*k,.22,.05-.12*k),vec3(.06+.10*k,.95-.10*k,-.35-.22*k),.075,.015),i==0?3.:16.));}
    vec3 to=p-vec3(0,2.6,8.95);to.yz=rot(.22)*to.yz;m=U(m,vec2(length(vec2(length(to.xz)-.50,to.y))-.10,3.));float at=atan(to.x,to.z);float am2=mod(at+PI/12.,TAU/12.)-PI/12.;m=U(m,vec2(length(vec3(am2*.55,to.y+.17,length(to.xz)-.55))-.095,6.));m=U(m,vec2(length(to-vec3(0,-.42,.62))-.17,4.));}
  float tb=length(p-vec3(0,2.2,-7.6))-3.4;if(tb<m.x){for(int i=0;i<4;i++){float k=float(i);vec3 l=q-vec3(.30*k,.2,-6.3);l.xy=rot(.26*k)*l.xy;l.z=-l.z;l.yz=rot(.50+.05*k)*l.yz;float h=4.4-.5*k;m=U(m,vec2(petal(l,.62,h,.06),i%2==0?13.:14.));m=U(m,vec2(length(l-vec3(0,h*.72,.46*h*.52))-.16,i%2==0?4.:5.));}}
  // palace: plinth, hall, upper hall, dome, side halls, four pavilions, gate
  float hb=sBox(p-vec3(0,4.2,-.4),vec3(3.2,4.4,5.4),0.);if(hb<m.x){
    vec3 c=p-vec3(0,0,-.4);vec3 g=vec3(abs(c.x),c.y,abs(c.z));
    m=U(m,vec2(sBox(c-vec3(0,.45,0),vec3(2.35,.28,4.1),.06),11.));m=U(m,vec2(sBox(c-vec3(0,.74,0),vec3(2.5,.07,4.25),.04),3.));
    float hall=sBox(c-vec3(0,1.85,0),vec3(1.65,1.1,3.1),.05);m=U(m,vec2(hall,17.));
    // a colonnade round the hall
    float zz=clamp(floor(g.z/.78+.5),0.,4.)*.78;vec3 pc=vec3(g.x-2.15,c.y,g.z-zz-.0);float pl=length(pc.xz)-.115-.035*cos((c.y-1.8)*9.)*smoothstep(.2,.9,abs(c.y-1.85));float xx=clamp(floor(g.x/.86+.5),0.,2.)*.86;vec3 pd=vec3(g.x-xx,c.y,g.z-3.65);float pl2=length(pd.xz)-.115-.035*cos((c.y-1.8)*9.)*smoothstep(.2,.9,abs(c.y-1.85));
    m=U(m,vec2(max(min(pl,pl2),abs(c.y-1.85)-1.10)*.9,3.));
    vec3 e=c-vec3(0,3.02,0);float ev=sBox(e-vec3(0,.02+.0,0),vec3(2.55,.10,4.15),.05);m=U(m,vec2(ev,11.));m=U(m,vec2(sBox(e-vec3(0,-.12,0),vec3(2.72,.05,4.30),.03),3.));
    {float ex=mod(g.z+.17,.34)-.17;float hh=max(length(vec3(g.x-2.66,e.y+.32,ex))-.075,g.z-4.2);float ez=mod(g.x+.17,.34)-.17;float h2=max(length(vec3(ez,e.y+.32,g.z-4.24))-.075,g.x-2.6);m=U(m,vec2(min(hh,h2)*.8,12.));}
    {float ex=mod(g.z+.28,.56)-.28;float pt=max(petal(vec3(ex,e.y-.10,g.x-2.45),.25,.62,.05),g.z-4.0);float ez=mod(g.x+.28,.56)-.28;pt=min(pt,max(petal(vec3(ez,e.y-.10,g.z-4.05),.25,.62,.05),g.x-2.4));m=U(m,vec2(pt,13.));}
    // upper hall and the great dome
    vec3 u=c-vec3(0,3.12,0);float up=max(max(g.x,g.z*.94)*1.-1.45,abs(u.y-.75)-.75);up=max(up,(g.x+g.z)*.7071-1.75);m=U(m,vec2(up*.9,18.));
    vec3 k=polar(u,8.,0.);float cp=length(vec2(abs(k.x)-.62,k.z-1.58))-.095;m=U(m,vec2(max(cp,abs(u.y-.75)-.8)*.9,3.));
    m=U(m,vec2(max(length(u.xz)-1.95,abs(u.y-1.58)-.09),11.));m=U(m,vec2(length(vec2(length(u.xz)-1.98,u.y-1.48))-.09,3.));
    m=U(m,tier(u-vec3(0,1.60,0),14.,1.62,.0,.36,.72,-.45,0.,13.));
    float og=ogee(u-vec3(0,1.75,0),1.62);m=U(m,vec2(og,10.));vec2 f=finial(u-vec3(0,4.55,0),1.15);m=U(m,f);
    // four pavilions on the roof corners, two on the long axis ends
    m=U(m,chhatri(vec3(g.x-1.72,c.y-3.12,g.z-3.15),.92));m=U(m,chhatri(vec3(g.x,c.y-3.12,g.z-3.2),.0+1.15));
    // gate arch toward the prow
    vec3 t=p-vec3(0,0,4.15);float ar=max(abs(length(vec2(t.x,max(t.y-1.9,0.)))-.95)-.16,abs(t.z)-.2);ar=max(ar,-t.y+.3);m=U(m,vec2(ar,3.));vec2 ft=finial(t-vec3(0,3.2,0),.8);m=U(m,ft);m=U(m,vec2(length(t-vec3(0,2.62,0))-.18,12.));
  }
  return m;}
#endif
float jali(vec2 u){vec2 f=abs(fract(u)-.5);return min(abs(f.x+f.y-.5),min(abs(f.x-.0),abs(f.y-.0)));}
void surf(vec3 p,vec3 n,int m,inout Surf s){
#if KIND<2
  if(m==9){float g=sin(p.z*18.+3.*vn3(p*2.))*.05;s.base*=1.+g;if(p.y>6.&&n.y>.7){float pl=abs(fract(p.x*.9)-.5);s.base*=.8+.25*smoothstep(.02,.06,.5-pl);}}
  if(m==11){vec2 k=vec2(p.x/4.25,(p.z+.2)/5.2);float a=atan(k.x,k.y);float y=p.y-6.6;vec2 u=vec2(a*6.5,y*1.15);
    u*=1.25;vec2 f=abs(fract(vec2(u.x+u.y,u.x-u.y)*.5)-.5);float l=min(f.x,f.y);vec2 ce=fract(vec2(u.x+u.y,u.x-u.y)*.5)-.5;float dt=length(ce);
    if(l<.045){s.base=vec3(1.,.93,.72);s.sh=s.base*.4;s.cls=2.;}else if(dt<.16+.04*cos(atan(ce.y,ce.x)*4.)){s.base=KIND==0?hex(0xc8323a):hex(0x8a1018);s.cls=8.;if(dt<.06){s.cls=2.;s.base=vec3(1.);}}s.ink=.8;}
  if(m==14){vec3 c=p-vec3(0,21.6,-4.8);float a=atan(c.x,c.z),r=length(c.xz);
#if KIND==0
    float st=smoothstep(.06,.0,abs(abs(sin(a*12.))-.0));float rg=smoothstep(.10,.04,abs(r-5.0))+smoothstep(.10,.04,abs(r-4.5));float dt=smoothstep(.2,.16,length(vec2(fract(a*36./TAU)-.5,(r-4.75)*1.2)));if(rg>.5){s.cls=2.;s.base=vec3(1);}else{s.base=mix(s.base,hex(0xc8323a),max(dt,smoothstep(5.15,5.2,r)*.9));s.base*=.92+.08*cos(a*24.);}
#else
    float z=sin(a*20.)*.5+.5;s.base=mix(s.base,hex(0x7a0c18),smoothstep(.45,.55,z));float y=mod(c.y,1.9);if(y<.28){s.cls=2.;s.base=vec3(.95,.75,.5);}
#endif
  }
  if(m==10){float y=p.y-6.6+1.05;s.base*=.75+.4*smoothstep(-.9,.8,y);}
  if(m==12){s.base=vec3(3.2,.9,.15)*1.3;s.cls=4.;s.ink=.6;}
  if(m==4||m==5||m==6)s.ink=.6;
#else
  vec3 sp=vec3(p.x,p.y,p.z/1.72);float a=atan(sp.x,sp.z),r=length(sp.xz);
  vec3 g2=mix(vec3(1.),vec3(.62,.40,.34),mood);
  vec3 lampc=mix(vec3(3.4,1.9,.62),vec3(3.2,.42,.08),mood)*lamps;
  if(m==13||m==14){float k=smoothstep(3.1,5.2,r);if(p.y>2.6)k=.6;vec3 c0=m==13?hex(0xffd2cc):hex(0xfff0e0),c1=m==13?hex(0xe2557c):hex(0xf08aa0);vec3 d0=m==13?hex(0x3a1020):hex(0x1c1420),d1=m==13?hex(0x8a1420):hex(0x5a0c18);
    s.base=mix(mix(c0,c1,k),mix(d0,d1,k),mood);s.sh=s.base*mix(vec3(.42,.30,.48),vec3(.3),mood);float v=sin(a*16.*9.);s.base*=.95+.06*v;s.cls=8.;s.ink=.9;}
  if(m==10){float y=p.y;float rb=abs(sin(atan(p.x,p.z+.4)*8.));s.base*=g2;}
  if(m==3){s.base*=mix(vec3(1.),vec3(.95,.66,.48),mood);}
  if(m==9){s.base=mix(s.base,hex(0x2a1018),mood);vec2 u=vec2(a*14.,p.y*4.);float f=smoothstep(.14,.06,abs(sin(u.x)*.5+.5-fract(u.y)));if(f>.5){s.cls=2.;s.base=vec3(1.,.9,.7)*g2;}vec2 lu=vec2(a*(p.y>-1.35?11.:7.),(p.y+.3)*2.1);vec2 lf=fract(lu)-.5;float ld=length(lf*vec2(1.6,1.));if(ld<.20){s.cls=4.;s.base=lampc*.8;s.ink=.2;}else if(ld<.27){s.cls=2.;s.base=vec3(1.);}}
  if(m==11){s.base=mix(s.base,hex(0x241820),mood);s.sh=mix(s.sh,hex(0x0c080e),mood);if(n.y>.8&&p.y<.4){float ck=mod(floor(p.x*2.5)+floor(p.z*2.5),2.);s.base=mix(s.base,mix(hex(0xb8483a),hex(0x3a0c14),mood),ck*.6);}
    float fr=abs(fract((abs(n.x)>abs(n.z)?p.z:p.x)*3.)-.5);if(abs(n.y)<.5&&fr<.16){s.cls=2.;s.base=vec3(1.,.9,.7)*g2;}}
  if(m==17||m==18){                                   // walls with lit jali windows
    float x=abs(n.x)>abs(n.z)?p.z+.4:p.x;float bay=m==17?.78:.9;float f=mod(x+bay*.5*step(1.,float(m-16))*0.,bay)-bay*.5;if(m==17)f=mod(x+.39,.78)-.39;float y0=m==17?1.75:3.85;vec2 w=vec2(f,p.y-y0);float hw=m==17?.24:.26,hh=.52;
    float arch=max(abs(w.x)-hw,max(-w.y-hh,length(vec2(w.x,max(w.y-.22,0.))*vec2(1.,.75))-hw));
    if(abs(n.y)<.4&&arch<0.){float j=jali(w*7.);float b=smoothstep(.04,.09,j);s.cls=4.;s.base=lampc*mix(.10,1.,b)*(.55+.45*smoothstep(.5,-.4,w.y));s.ink=0.;}
    else if(abs(n.y)<.4&&arch<.07){s.cls=2.;s.base=vec3(1.,.9,.7)*g2;}
    else{s.base=mix(s.base,hex(0x2a1c26),mood);s.sh=mix(s.sh,hex(0x100a12),mood);float dd=length(vec2(f,fract((p.y-y0)*3.)-.5)-vec2(0));if(abs(p.y-y0)>.62){float q=abs(fract(x*5.)-.5);if(q<.2){s.cls=2.;s.base=vec3(1.,.9,.7)*g2;}}}
    s.ink=.7;}
  if(glow>0.&&s.cls!=4.&&m!=12){float r2=length(sp.xz);float pr=1.15*exp(-pow((p.y-2.45)/.85,2.))*smoothstep(3.6,2.2,abs(p.x))+1.05*exp(-pow((p.y+.55)/1.15,2.))*smoothstep(2.6,4.0,r2)+.55*exp(-pow((p.y-4.1)/.7,2.))+.30*smoothstep(-.2,.6,-n.y)*step(p.y,0.)+.34;
    vec3 w=mix(vec3(1.,.52,.16),vec3(1.,.16,.05),mood)*glow*lamps*pr;if(s.cls<2.5&&s.cls>1.5)s.base*=(vec3(1.)+glow*lamps*pr*mix(vec3(13.,6.4,.7),vec3(9.,1.2,.2),mood))*mix(vec3(1.),vec3(1.,.80,.22),min(glow,1.)*.9);else{s.sh+=s.base*w*2.8;s.base+=s.base*w*1.5;}}
  if(m==12){s.cls=4.;s.base=lampc*1.15;s.ink=.25;}
  if(m==20){s.base=mix(hex(0x1a0c10),vec3(2.4,.4,.05),mood);s.cls=mood>.5?4.:8.;s.ink=.6;}
  if(m==15){s.base=mix(s.base,hex(0x2c2230),mood);s.sh=mix(s.sh,hex(0x100a14),mood);vec2 u=vec2(atan(p.x,p.z-7.4)*2.4,-p.y*3.4);float e=0.,id=0.;float row=floor(u.y);
    for(int k=1;k>=-1;k--){float rr=row+float(k);vec2 f=vec2(u.x*2.2+.5*mod(rr,2.),u.y-rr);f.x=fract(f.x)-.5;float y=f.y-.35;float d=length(vec2(f.x*1.05,max(y,0.)*.78))-.52;if(d<0.&&f.y>-.2){e=d;break;}}
    float hk=smoothstep(4.35,4.1,p.y);s.base=mix(s.base,mix(hex(0xd8a24a),hex(0x6a1c14),mood),smoothstep(-.12,-.04,e)*hk);s.base=mix(s.base,mix(hex(0xffd8c8),hex(0x5a2420),mood),smoothstep(-.34,-.5,e)*hk*.5);
    float g=abs(p.y-4.22)-.09;if(g<0.){s.cls=2.;s.base=vec3(1.);}
    vec3 eq=vec3(abs(p.x),p.yz)-vec3(.2,4.97+.02,9.0);float hd=length(vec2(eq.z*.8,eq.y*1.4));if(hd<.0){s.base=hex(0x1a0c10);}}
  if(m==16){s.base=mix(s.base,hex(0x8a2018),mood);}
  if(m==4||m==5||m==6)s.ink=.5;
#endif
}
