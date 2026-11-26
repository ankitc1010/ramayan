// RAVANA.  ten heads (uniform fan), twenty arms (uniform arms).  Define HEADONLY for one loose head on its own (figure origin = centre of the skull).
uniform float fan,arms,armT,navel,hair,spread,mantle,armTop;      // armTop: angle of the highest arm (radians, 1.3 = nearly upright); hair: 1 long locks on the main head; spread: width of the row; mantle: 1 the gold collar under the row
uniform float alive[10],eyeglow[10],lids[10],mouths[10];   // per head, 0 = his far right .. 4 = main .. 9 = his far left
uniform sampler2D tCells;                                  // expression cells for the nine lesser heads
#define MAINH 4
#define S0 1.30
vec3 rX,rY,rZ;vec4 aT[18];                                     // per arm and side: cos, sin, length, how far out
vec4 hP[10];vec2 hC[10];float hE[10];float gJ=0.;      // row frame, head centre+scale in it, cos/sin of its outward turn, how far it is out
void initRav(){
  initRig();
  rZ=normalize(mix(cZ,hZ,.55));rX=normalize(mix(cX,hX,.40));rY=normalize(cross(rZ,rX)+.0001);rX=cross(rY,rZ);
  for(int i=0;i<9;i++)for(int s=0;s<2;s++){float f=float(i),e=smoothstep(0.,1.,clamp(arms*1.6-.6*f/8.,0.,1.));float a=armTop-(armTop+1.10)*f/8.-.95*(1.-e)+.045*sin(armT*1.7+f*1.1+(s==0?0.:1.3))*e;aT[i*2+s]=vec4(cos(a),sin(a),mix(.05,1.,e)*(mod(f,2.)<.5?1.14:1.0),e);}
  float xr=0.,xl=0.,pr=S0,pl=S0;
  for(int n=0;n<=5;n++){
    for(int s=0;s<2;s++){
      int k=s==0?MAINH-n:MAINH+n;if(k<0||(n==0&&s==1)) continue;
      float sc=n==0?S0:(s==0?1.08-.085*float(n):1.06-.083*float(n));
      if(n>0){if(s==0){xr+=.785*spread*(pr+sc);pr=sc;}else{xl+=.725*spread*(pl+sc);pl=sc;}}
      float e=n==0?1.:1.-pow(1.-clamp(fan*1.35-.07*float(n),0.,1.),2.2);
      float x=n==0?0.:(s==0?-xr:xl);
      float a=x==0.?0.:sign(x)*(.05+.080*float(n))*e;
      float f=float(n);
      hE[k]=e;hP[k]=vec4(x*e,(.04+.02*f-.020*f*f)*e-.25*step(.5,f)*(1.-e),-.22*f*e-.34*step(.5,f),sc*mix(.55,1.,e));hC[k]=vec2(cos(a),sin(a));
    }}
}
// figure space -> local (unit) space of head k
vec3 toHead(vec3 p,int k){
#ifdef HEADONLY
  return p;
#endif
  if(k==MAINH) return Bh*(p-J[3])/S0;
  vec3 o=p-J[3];o=vec3(dot(o,rX),dot(o,rY),dot(o,rZ))-hP[k].xyz;vec2 c=hC[k];
  return vec3(c.x*o.x-c.y*o.z,o.y,c.y*o.x+c.x*o.z)/hP[k].w;
}
float headSc(int k){
#ifdef HEADONLY
  return 1.;
#endif
  return k==MAINH?S0:hP[k].w;}
// ---------------------------------------------------------------- one head
float rBase(vec3 p,float jw){
  float jd=jw*.24;vec3 q=vec3(abs(p.x),p.yz);
  float d=sEll(p-vec3(0,.20,-.10),vec3(.79,.84,.88));
  d=smin(d,sEll(p-vec3(0,-.30-jd*.4,.11),vec3(.70,.78+jd*.5,.64)),.26);
  d=smin(d,length(q-vec3(.37,-.30,.39))-.27,.18);
  d=smin(d,sEll(p-vec3(0,-.98-jd,.42),vec3(.30,.17,.20)),.20);
  return smin(d,sCone(q,vec3(.20,-.96-jd,.34),vec3(.65,-.52-jd*.6,-.04),.12,.20),.18);
}
float rFace(vec3 p,float jw){
  float d=rBase(p,jw);vec3 q=vec3(abs(p.x),p.yz);float jd=jw*.22;
  d=smax(d,-sEll(q-vec3(.32,.01,.89),vec3(.22,.12,.17)),.14);
  d=smin(d,sCone(q,vec3(.10,.185,.735),vec3(.50,.27,.53),.085,.055),.12);            // brow ridge
  float n=sCone(p,vec3(0,.13,.73),vec3(0,-.06,.88),.060,.085);n=smin(n,sCone(p,vec3(0,-.06,.88),vec3(0,-.30,.905),.080,.095),.06);
  n=smin(n,length(q-vec3(.125,-.335,.80))-.090,.06);
  d=smin(d,n,.15);
  d=smax(d,-sCone(q,vec3(.185,-.41,.80),vec3(.34,-.62,.60),.02,.03),.10);             // fold beside the mouth
  float l=sCone(q,vec3(0,-.565,.80),vec3(.21,-.585,.68),.055,.02);
  l=smin(l,sCone(q,vec3(0,-.655-jd,.775),vec3(.17,-.62-jd,.68),.070,.025),.02);
  return smin(d,l,.05);
}
float stache(vec3 p){
  vec3 q=vec3(abs(p.x),p.yz);
  float d=sCone(q,vec3(.035,-.430,.885),vec3(.22,-.475,.83),.045,.088);
  d=smin(d,sCone(q,vec3(.22,-.475,.83),vec3(.45,-.43,.715),.088,.076),.05);
  d=smin(d,sCone(q,vec3(.45,-.43,.715),vec3(.625,-.29,.60),.076,.054),.05);
  d=smin(d,sCone(q,vec3(.625,-.29,.60),vec3(.71,-.09,.54),.054,.032),.05);
  d=smin(d,sCone(q,vec3(.71,-.09,.54),vec3(.67,.04,.55),.032,.010),.04);
  return d-.009*sin(q.x*9.+q.y*52.-q.x*q.x*30.);
}
vec2 rCrown(vec3 p){
  vec3 c=p-vec3(0,.21,-.10);c.xz/=vec2(.97,1.06);float r=length(c.xz),a=atan(c.x,c.z);
  if(r>1.6) return vec2(r-1.25,3.);
  float d=max(abs(r-.83)-.05,abs(c.y-.60)-.14)-.02;                                    // band
  d=min(d,sTor(c-vec3(0,.44,0),.845,.052));d=min(d,sTor(c-vec3(0,.77,0),.83,.046));
  vec3 g=polar(c,18.,0.);float gem=sEll(g-vec3(0,.605,.895),vec3(.075,.085,.05)),gem2;
  vec3 b=polar(c,18.,PI/18.);gem2=length(b-vec3(0,.605,.895))-.042;
  // three bells, each with a lip of petals
  float y=c.y-.80;
  float s=smoothstep(0.,1.9,y);float t=clamp(y,0.,1.95)/.65;float fr=fract(t),ti=floor(t);
  float prof=(.74-.185*ti)*(1.-.30*fr*fr)-.02;prof=min(prof,.80);prof=mix(prof,.09,smoothstep(1.72,2.0,y));
  float bell=max(r-prof,max(-y-.05,y-2.0))*.55;bell-=.016*cos(a*(22.-5.*min(ti,2.)))*smoothstep(1.9,1.4,y);d=min(d,bell);
  for(int i=0;i<3;i++){float f=float(i);vec3 q=polar(c,12.-2.*f,f*.26)-vec3(0,.90+.65*f,.79-.185*f);q.yz=rot(-.22)*q.yz;float pt=sEll(q,vec3(.17-.02*f,.22,.05));pt=max(pt,-sEll(q-vec3(0,0,.05),vec3(.10,.15,.04)));d=min(d,pt);gem2=min(gem2,length(q-vec3(0,-.03,.015))-.055);
    d=min(d,sTor(c-vec3(0,.80+.65*f,0),.77-.185*f,.05));}
  d=min(d,sTor(c-vec3(0,2.76,0),.17,.06));d=min(d,sEll(c-vec3(0,2.92,0),vec3(.15,.17,.15)));d=min(d,sCone(c,vec3(0,3.0,0),vec3(0,3.42,0),.085,.012));
  gem=min(gem,length(c-vec3(0,2.92,.10))-.095);
  // flame-shaped plates: one over the brow, one over each ear
  vec3 f=p-vec3(0,1.27,.83);f.yz=rot(-.16)*f.yz;float sz=1.;vec3 f2=vec3(abs(p.x),p.yz)-vec3(.90,1.02,-.06);f2.xz=vec2(-f2.z,f2.x);f2.yz=rot(-.34)*f2.yz;f2/=.86;
  if(length(f2)<length(f)){f=f2;sz=.86;}
  float fx=abs(f.x),lf=length(vec2(fx/.40,(f.y+.10)/.46))-1.;lf=min(lf,max(fx-.20*(1.-smoothstep(.1,.92,f.y)),abs(f.y-.35)-.55)/.40)*.36;
  float pl=max(lf,abs(f.z+.10*fx)-.055)*.8;pl=max(pl,-max(lf+.085,-f.z-.02));
  pl=min(pl,max(abs(lf+.04)-.028,abs(f.z-.035)-.045)*.8);d=min(d,pl*sz);
  gem=min(gem,sEll(f-vec3(0,-.06,.04),vec3(.13,.19,.09))*sz);gem2=min(gem2,(length(f-vec3(0,.36,.03))-.065)*sz);
  {float st=TAU/14.,aa=atan(fx,f.y+.10),al=mod(aa+st*.5,st)-st*.5,rr=length(vec2(fx/.40,(f.y+.10)/.46))*.4;if(f.y<.22) gem2=min(gem2,length(vec3(sin(al)*rr,cos(al)*rr-.255,f.z-.02))*sz-.034);}
  return U(U(vec2(d,3.),vec2(gem,4.)),vec2(gem2,6.));
}
vec2 rEarring(vec3 h){vec3 q=vec3(abs(h.x),h.yz)-vec3(.84,-.64,.0);float bd=length(q)-.62;if(bd>.3) return vec2(bd,3.);
  float d=length(vec2(length(q.zy-vec2(0,0))-.235,q.x))-.078;vec3 b=polar(q.yxz,10.,0.);d=min(d,length(b-vec3(0,0,.335))-.055);
  d=min(d,sEll(q-vec3(0,-.46,0),vec3(.10,.13,.10)));return U(vec2(d,3.),U(vec2(sEll(q,vec3(.09,.13,.13)),4.),vec2(length(q-vec3(0,-.63,0))-.065,6.)));}
// whole head in unit space; main = the one with long hair
vec2 headMap(vec3 h,float jw,bool mn){
  float sk=rFace(h,jw);
  if(sk>1.2) {vec2 cr=rCrown(h);return U(vec2(sk-.9,1.),cr);}
  sk=smin(sk,earsD(h,1.6),.04);
  vec2 m=vec2(sk,1.);
  float hr=sEll(h-vec3(0,.08,-.30),vec3(.85,.90,.84));hr=smax(hr,-(h.y+.85+.35*h.z),.1);hr=smax(hr,h.z-.10,.08);
  vec3 q=vec3(abs(h.x),h.yz);
  // side whiskers along the jaw
  float bs=rBase(h,jw);float ww=mix(.05,.25,smoothstep(-.62,.5,h.y));float wh=max(bs-.035-.012*sin(h.y*40.+h.z*18.),max(abs(h.z-.06+.10*h.y)-ww-.02*sin(h.y*23.),max(h.y-.85,-h.y-.60)));wh=max(wh,.40-q.x);
  hr=min(hr,wh*.8);
  if(mn&&hair>.0){vec3 o=h-vec3(0,0,-.26);float aa=atan(o.x,-o.z),y=h.y;float r=length(o.xz*vec2(1.,1.06));float rp=.80+.30*smoothstep(.0,-1.5,y)-.10*smoothstep(-1.7,-2.4,y);
    float wv=aa+.07*sin(y*3.2);float lob=cos(wv*13.);float cu=max(r-rp-.045*lob-.016*cos(wv*39.),max(y-.2,-(y+2.05+.22*abs(sin(wv*6.5))-.10*cos(wv*3.))));
    cu=smax(cu,o.z-.12-.16*smoothstep(-.6,-1.6,y)+.10*smoothstep(-.2,.2,y),.10);hr=smin(hr,cu*.75,.06);}
  m=U(m,vec2(hr*.85,2.));
  m=U(m,vec2(stache(h)*.9,17.));
  m=U(m,rCrown(h));
  return U(m,rEarring(h));
}
// rough hull of a head in unit space: chin to crown tip, earrings
float headHull(vec3 h){return min(sCap(h,vec3(0,-.35,0),vec3(0,.8,-.05),1.24),sCone(h,vec3(0,1.1,0),vec3(0,3.45,0),1.12,.35));}
float jawOf(int k){return k==MAINH?max(jaw,mouths[k]):mouths[k];}
#ifndef HEADONLY
// nearest heads
void nearHeads(vec3 p,out ivec3 id,out vec3 bd){
  id=ivec3(MAINH,-1,-1);bd=vec3(1e3);
  vec3 o=p-J[3];float ox=dot(o,rX);
  for(int k=0;k<10;k++){
    if(k!=MAINH&&fan<=0.) continue;
    float a=k==MAINH&&alive[k]>.99?1.:alive[k];if(hE[k]<.004||a<.02) continue;
    float s=headSc(k);
    if(k!=MAINH&&abs(ox-hP[k].x)-1.26*s>bd.z) continue;
    vec3 h=toHead(p,k);
    float d=headHull(a<.99?(h-vec3(0,-1.,0))/a+vec3(0,-1.,0):h)*s*a;
    if(d<bd.x){bd=vec3(d,bd.xy);id=ivec3(k,id.xy);}else if(d<bd.y){bd=vec3(bd.x,d,bd.y);id=ivec3(id.x,k,id.y);}else if(d<bd.z){bd.z=d;id.z=k;}
  }
}
vec2 headsMap(vec3 p,float cur){
  ivec3 id;vec3 bd;nearHeads(p,id,bd);vec2 m=vec2(1e3,1.);
  for(int j=0;j<3;j++){
    if(id[j]<0||bd[j]>min(m.x,cur)) break;
    if(bd[j]>.35){m=U(m,vec2(bd[j],1.));continue;}
    int k=id[j];float a=min(alive[k],1.);vec3 h=toHead(p,k);if(a<.99) h=(h-vec3(0,-1.,0))/a+vec3(0,-1.,0);
    vec2 r=headMap(h,jawOf(k),k==MAINH);r.x*=headSc(k)*a;m=U(m,r);
  }
  return m;
}
// the shared mass that carries the row: necks, torcs, and a gold mantle
vec2 rowMap(vec3 p,float cur){
  vec2 m=vec2(1e3,1.);float lb=1e3;vec3 o=p-J[3];o=vec3(dot(o,rX),dot(o,rY),dot(o,rZ));
  for(int k=0;k<10;k++){
    float e=hE[k];if(e<.004) continue;
    vec3 c=hP[k].xyz;float s=hP[k].w;
    if(abs(o.x-c.x)>1.6&&k!=MAINH&&mantle>.5){lb=min(lb,abs(o.x-c.x)-.8);continue;}
    if(k==MAINH){
      if(alive[k]<.98){vec3 nx=normalize(J[3]-J[2]),t=mix(J[2],J[3],.34);m=U(m,vec2(sEll(Bc*(p-t),vec3(.56,.20,.52)),12.));m=U(m,vec2(ringD(p,t-nx*.22,nx,.62,.10,.06),3.));}
      continue;}
    vec3 top=c+vec3(0,-.62*s,-.14*s),bot=vec3(c.x*.97,c.y-1.16*s,c.z-.22*s);
    float nk=sCone(o,bot,top,.60*s,.43*s);if(mantle<.5){vec3 el=vec3(c.x*.84,bot.y-.75,c.z-.3),rt=vec3(c.x*.30,-2.9,-.5);nk=smin(nk,sCone(o,el,bot,.50*s,.50*s),.3);nk=smin(nk,sCone(o,rt,el,.75,.48*s),.4);}
    if(alive[k]<.98) nk=max(nk,dot(o-mix(bot,top,.55),normalize(top-bot)));
    m=vec2(m.y<1.5?smin(m.x,nk,.12):min(m.x,nk),nk<m.x?1.:m.y);
    vec3 ax=normalize(top-bot),cc=mix(bot,top,.36);
    m=U(m,vec2(ringD(o,cc,ax,.56*s,.09*s,.05),3.));m=U(m,vec2(ringD(o,cc-ax*.17*s,ax,.60*s,.045*s,.05),4.));
    if(alive[k]<.98){vec3 f=o-mix(bot,top,.58);f-=ax*dot(f,ax)*.0;m=U(m,vec2(length(f-ax*dot(f,ax)*-.6)-.41*s,12.));}
  }
  m=U(m,vec2(lb,3.));
  if(fan>0.&&mantle>.5){
    float ax=abs(o.x),w=max(-hP[0].x,hP[9].x)+.62,gw=smoothstep(.0,.45,hE[9]);
    float u=clamp(ax/w,0.,1.2);float zc=-.22-.18*ax;float top=-1.28+.085*ax,hgt=mix(1.15,.50,u)*mix(.15,1.,gw);
    float lob=.11*abs(sin(ax*2.35));
    float flare=.18*(1.-u);                                           // the rim leans forward like a dish
    float yy=o.y-(top-hgt*.5),zz=o.z-zc-flare*(yy/hgt+.5)-.10*smoothstep(.3,-.5,yy/hgt);
    vec2 b=abs(vec2(yy,zz))-vec2(hgt*.5,.34-.14*u);
    float pl=length(max(b,0.))+min(max(b.x,b.y),0.)-.06;pl=max(pl,ax-w+.35*abs(yy));if(gw<.02) pl=1e2;
    pl=max(pl,top-hgt-.02+lob-o.y);
    if(pl<.16) pl-=.022*(.5+.5*cos(ax*9.4))*smoothstep(.5,.3,abs(yy/hgt))*step(0.,zz);
    m=U(m,vec2(pl*.72,15.));
    float ft=.34-.14*u;
    if(gw>.02) m=U(m,vec2(length(vec2(o.y-top-.03,zz-ft*.6))-.075+max(0.,ax-w)*1.,3.));
    float cx=.70,xi=(floor(ax/cx)+.5)*cx;if(xi<w-.25&&gw>.98){float ui=xi/w,hi=mix(1.15,.50,ui),k=1.-.35*ui;vec3 g=vec3(ax-xi,o.y-(-1.28+.085*xi-hi*.45),o.z-(-.22-.18*xi)-.18*(1.-ui)*.5-(.34-.14*ui)-.06);m=U(m,vec2(sEll(g,vec3(.15,.18,.10)*k),4.));m=U(m,vec2(length(vec2(length(g.xy*vec2(1.,.87))-.20*k,g.z))-.045,3.));
      float lb=.11*abs(sin(xi*2.35));vec3 dr=vec3(ax-xi,o.y-(-1.28+.085*xi-hi+lb-.12),o.z-(-.22-.18*xi)-.06);m=U(m,vec2(sEll(dr,vec3(.09,.20,.09)*k),6.));}
    float lo=o.y-(top-hgt-.02+lob);if(gw>.02) m=U(m,vec2(length(vec2(lo,zz-.02))-.075+max(0.,ax-w+.1),3.));
  }
  return m;
}
// ---------------------------------------------------------------- the wheel of arms
int weapon(int i,bool left){int L[9]=int[9](0,7,4,1,3,6,8,2,5);int R[9]=int[9](2,0,1,4,6,3,0,8,5);return left?L[i]:R[i];}
vec2 weaponMap(vec3 w,int kd){            // grip at the origin, business end +y, +x away from the body's middle
  vec2 m;
  if(kd==0){m=vec2(sCap(w,vec3(0,-.5,0),vec3(0,.4,0),.13),11.);m=U(m,vec2(length(w-vec3(0,-.62,0))-.2,3.));m=U(m,vec2(sBox(w-vec3(0,.5,0),vec3(.55,.10,.17),.08),3.));
    vec3 q=w;q.x-=.06*q.y*q.y*.5;float wd=mix(.22,.40,smoothstep(.8,3.2,q.y))*smoothstep(4.5,3.5,q.y);vec2 e=abs(q.xz)-vec2(wd,.05);float d=length(max(e,0.))+min(max(e.x,e.y),0.);m=U(m,vec2(max(d,abs(q.y-2.45)-1.95)*.6,10.));}
  else if(kd==1){m=vec2(sCap(w,vec3(0,-1.1,0),vec3(0,2.2,0),.15),11.);m=U(m,vec2(length(w-vec3(0,-1.25,0))-.24,3.));vec3 q=w-vec3(0,2.95,0);float a=atan(q.x,q.z);m=U(m,vec2((length(q*vec3(1,.9,1))-.88-.08*cos(a*8.)*smoothstep(.9,.2,abs(q.y)))*.8,3.));m=U(m,vec2(sTor(q,.93,.09),4.));m=U(m,vec2(sCone(q,vec3(0,.85,0),vec3(0,1.45,0),.2,.03),3.));}
  else if(kd==2){m=vec2(sCap(w,vec3(0,-2.4,0),vec3(0,2.6,0),.085),11.);vec3 q=w-vec3(0,3.4,0);float wd=.36*smoothstep(1.,-.3,q.y)*smoothstep(-1.,-.5,q.y);vec2 e=abs(q.xz)-vec2(wd,.06);m=U(m,vec2(max(length(max(e,0.))+min(max(e.x,e.y),0.),abs(q.y)-.98)*.6,10.));m=U(m,vec2(length(w-vec3(0,2.45,0))-.18,3.));}
  else if(kd==3){float k=clamp(abs(w.y)/2.5,0.,1.);float xc=-1.0*k*k+.35*sin(PI*k);float d=max(length(vec2(w.x-xc,w.z))-mix(.16,.075,k),abs(w.y)-2.5)*.66;m=vec2(d,11.);m=U(m,vec2(length(vec3(w.x+1.0,abs(w.y)-2.5,w.z))-.15,3.));m=U(m,vec2(sCap(w,vec3(-1.0,-2.45,0),vec3(-1.0,2.45,0),.028),6.));m=U(m,vec2(sCap(w,vec3(0,-.5,0),vec3(0,.5,0),.19),3.));m=U(m,vec2(length(vec3(w.x-.22,abs(w.y)-.85,w.z))-.2,3.));}
  else if(kd==4){vec3 q=w-vec3(0,1.35,0);float r=length(q.xy),a=atan(q.x,q.y);m=vec2(max(abs(r-.78)-.17,abs(q.z)-.07)*.9,3.);vec3 s=q;float st=TAU/16.,aa=mod(a+st*.5,st)-st*.5;m=U(m,vec2(max(sEll(vec3(sin(aa)*r,cos(aa)*r-.98,q.z),vec3(.12,.26,.06)),abs(q.z)-.05),10.));m=U(m,vec2(length(q)-.2,4.));st=TAU/8.;aa=mod(a,st)-st*.5;m=U(m,vec2(sCap(vec3(sin(aa)*r,cos(aa)*r,q.z),vec3(0),vec3(0,.75,0),.055),3.));m=U(m,vec2(sCone(w,vec3(0,.3,0),vec3(0,1.1,0),.12,.09),13.));}
  else if(kd==5){vec3 q=w-vec3(.1,.1,.42);float r=length(q.xy);float dm=q.z-.30*(1.-r*r/1.5);m=vec2(max(abs(dm)-.06,r-1.22)*.8,16.);m=U(m,vec2(length(vec2(r-1.22,q.z+.0))-.10,3.));m=U(m,vec2(length(vec2(r-.70,dm-.05))-.05,3.));m=U(m,vec2(sEll(q-vec3(0,0,.34),vec3(.27,.27,.2)),3.));vec3 b=polar(q.xzy,8.,.39);m=U(m,vec2(length(b-vec3(0,.16,.95))-.10,4.));}
  else if(kd==6){m=vec2(sCap(w,vec3(0,-1.3,0),vec3(0,2.5,0),.12),11.);vec3 q=w-vec3(.40,2.0,0);float bl=max(length(q.xy)-.98,-(length(vec2(q.x+.22,abs(q.y)-.78))-.56));bl=max(bl,-.45-q.x);bl=max(bl,abs(q.z)-.10+.07*smoothstep(.2,.9,length(q.xy)));m=U(m,vec2(bl*.8,10.));m=U(m,vec2(sBox(w-vec3(.05,2.0,0),vec3(.26,.30,.18),.08),3.));m=U(m,vec2(sCone(w,vec3(0,2.5,0),vec3(0,3.0,0),.14,.02),3.));}
  else if(kd==7){m=vec2(sCap(w,vec3(0,-2.2,0),vec3(0,2.5,0),.09),11.);vec3 q=vec3(abs(w.x),w.y-2.5,w.z);float pr=sCone(q,vec3(0,0,0),vec3(0,1.6,0),.11,.02);pr=min(pr,sCap(q,vec3(0,.1,0),vec3(.46,.28,0),.085));pr=min(pr,sCone(q,vec3(.46,.28,0),vec3(.40,1.28,0),.10,.02));m=U(m,vec2(pr,3.));m=U(m,vec2(length(w-vec3(0,2.4,0))-.17,4.));}
  else {m=vec2(1e3,13.);}
  return m;
}
float gArm=0.;
vec2 armsMap(vec3 p,float cur){
  vec3 c=Bc*(p-J[1]);bool lf=c.x>0.;vec3 q=vec3(abs(c.x),c.yz)-vec3(1.35*B[11],.80,-1.45);q.z+=.13*length(q.xy);
  float slab=max(max(length(q.xy)-10.8,abs(q.z+.1)-2.1),0.);if(slab>.8||slab>cur) return vec2(max(slab,.02)*.9,13.);
  float b1=1e3,b2=1e3;int i1=-1,i2=-1,sd=lf?0:1;
  for(int i=0;i<9;i++){
    vec4 T=aT[i*2+sd];if(T.w<.015) continue;float f=float(i);vec2 k=T.xy;float L=T.z,zo=mod(f,2.)<.5?.0:-.62;
    vec3 l=vec3(dot(q.xy,k),dot(q.xy,vec2(-k.y,k.x)),q.z-zo)/L;if((abs(l.y-.65)-2.95)*L>b2) continue;int kd=weapon(i,lf);
    float bd=sCap(l,vec3(.2,-.1,0),vec3(5.2,.5,.2),.82);
    float hw=kd==3?2.75:1.45;bd=min(bd,kd==3||kd==2?length(l-vec3(5.4,.7,.5))-2.8:1e3);
    bd=min(bd,sCap(l,vec3(5.2,.6,.4),vec3(kd==5||kd==8?5.8:9.2,kd==5||kd==8?.8:2.2,.4),kd==5?1.5:1.25));
    bd*=L;
    if(bd<b1){b2=b1;i2=i1;b1=bd;i1=i;}else if(bd<b2){b2=bd;i2=i;}
  }
  vec2 m=vec2(1e3,13.);
  for(int j=0;j<2;j++){
    int i=j==0?i1:i2;float bd=j==0?b1:b2;if(i<0||bd>min(m.x,cur)) break;
    if(bd>.30){m=U(m,vec2(bd,13.));continue;}
    float f=float(i);float zo=mod(f,2.)<.5?.0:-.62;vec2 k=aT[i*2+sd].xy;float L=aT[i*2+sd].z;vec3 l=vec3(dot(q.xy,k),dot(q.xy,vec2(-k.y,k.x)),q.z-zo)/L;
    vec3 E=vec3(2.75,-.28,-.12),W=vec3(4.95,.48,.30),A=vec3(.15,0,0);
    float d=sCone(l,A,mix(A,E,.4),.60,.56);d=smin(d,sCone(l,mix(A,E,.4),E,.56,.38),.14);vec3 mm=mix(E,W,.3);d=smin(d,sCone(l,E,mm,.37,.45),.14);d=smin(d,sCone(l,mm,W,.45,.25),.14);
    vec3 fw=normalize(W-E);int kd=weapon(i,lf);vec3 w=l-(W+fw*.46);
    vec2 r;
    if(kd==8){ // open palm
      vec3 o=w;o.xy=mat2(fw.x,-fw.y,fw.y,fw.x)*o.xy;o.xy=vec2(o.x,o.y);float pm=sBox(o-vec3(.05,0,0),vec3(.42,.40,.15),.13);vec3 fg=o-vec3(.42,0,0);float id=clamp(floor(fg.y/.2+.5),-1.5,1.5);id=clamp(floor(fg.y/.2)+.5,-1.5,1.5);fg.y-=id*.2;pm=smin(pm,sCone(fg,vec3(0),vec3(.62-.08*abs(id),id*.03,.02),.105,.085),.05);pm=smin(pm,sCone(o,vec3(-.1,.35,.05),vec3(.30,.66,.15),.13,.09),.08);d=smin(d,pm,.1);r=vec2(d,13.);}
    else{
      vec3 o=w;float fs=sBox(o,vec3(.36,.38,.32),.20);float kn=abs(fract(o.y*5.2+.5)-.5);fs+=.03*smoothstep(.30,.5,kn)*step(0.,o.z);fs=smin(fs,sCone(o,vec3(-.1,-.15,.26),vec3(.22,.18,.36),.12,.10),.05);d=smin(d,fs,.10);
      r=vec2(d,13.);
      // turn the weapon so its point looks away from the hub and upward
      float tl=kd==3?.10:(kd==4?1.10:1.15);vec2 ax=kd==4?vec2(.45,.89):(kd==3?vec2(.0,1.):vec2(cos(.34),sin(.34)));
      vec3 ww=vec3(w.x*ax.y-w.y*ax.x,w.x*ax.x+w.y*ax.y,w.z);if(kd==6)ww.x=-ww.x;
      r=U(r,weaponMap(ww,kd));
    }
    vec3 a1=mix(A,E,.50),an=normalize(E-A);r=U(r,vec2(ringD(l,a1,an,.50,.14,.04),3.));r=U(r,vec2(length(l-a1-vec3(0,0,.56))-.12,4.));
    r=U(r,vec2(ringD(l,mix(E,W,.86),fw,.30,.18,.04),3.));
    r.x*=L*.95;m=U(m,r);
  }
  // round gold hub behind the shoulder
  float hb=sEll(q-vec3(.05,.1,.42),vec3(1.0,1.0,.95));m=U(m,vec2(hb,13.));
  return m;
}
// ---------------------------------------------------------------- body
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
float chestPat(vec3 c){          // hammered ornament of the breastplate, as a height
  float k=0.;vec2 q=vec2(abs(c.x),c.y);
  float r=length(q-vec2(0,.18)),a=atan(q.x,q.y-.18);
  k+=.5+.5*cos(a*16.);k*=smoothstep(.62,.56,r)*smoothstep(.22,.28,r);
  k+=smoothstep(.05,.02,abs(r-.70));
  vec2 p2=q-vec2(.98,.40);float r2=length(p2),a2=atan(p2.x,p2.y);k+=smoothstep(.045,.015,abs(r2-.34))+smoothstep(.07,.03,abs(r2-.20+.05*cos(a2*8.)));
  vec2 g=vec2(q.x*4.2,q.y*4.2+.5*floor(q.x*4.2));
  float sc=0.;{vec2 u=vec2(c.x*3.4,c.y*4.6);u.x+=.5*mod(floor(u.y),2.);vec2 f=fract(u)-vec2(.5,1.);sc=smoothstep(.62,.50,length(f*vec2(1.,.9)))*.55;}
  return k+sc*step(.80,r)*step(.42,r2);
}
vec2 armourMap(vec3 p,float td){
  vec3 c=Bc*(p-J[1]);vec3 q=vec3(abs(c.x),c.yz);
  float bot=-(c.y+.62+.42*(1.-smoothstep(0.,1.2,q.x))-.10*abs(sin(q.x*3.2)));
  float top=c.y-.98-.42*smoothstep(.35,1.5,q.x)+.26*smoothstep(.7,.0,q.x);
  float arm=length(vec2(q.y-1.02,q.z+.16))-.86+.0;arm=q.x>1.0?-(length(vec3((q.x-1.95)*.75,q.y-.72,q.z+.10))-.98):-9.;
  float ed=max(max(bot,top),arm);
  float sh=max(abs(td-.07)-.05,ed);
  if(sh<.18) sh-=.030*chestPat(c)*smoothstep(.0,-.18,ed)*step(0.,c.z);
  vec2 m=vec2(sh*.85,9.);
  float rim=length(vec2(td-.12,ed+.03))-.075;m=U(m,vec2(rim*.85,3.));
  vec3 md=c-vec3(0,.18,1.06*B[1]);m=U(m,vec2(sEll(md,vec3(.21,.23,.12)),4.));m=U(m,vec2(sTor(md.xzy,.25,.055),3.));
  return m;
}
vec2 map(vec3 p){
  vec2 m=vec2(1e3,1.);
  // hulls: upper body, legs, each arm
  float hub=sCap(p,J[0]+pY*.2,J[2]-cY*.4,2.55);hub=min(hub,sCap(p,J[4],J[7],1.2));
  float td=1e3;
  if(hub<.5){
    td=torsoD(p);float nd=neckD(p);if(alive[MAINH]<.98) nd=smax(nd,dot(p-mix(J[2],J[3],.34),normalize(J[3]-J[2])),.06);m=vec2(smin(td,nd,.16),1.);
  }else m=vec2(hub,1.);
  float ab=min(min(sCap(p,J[4],J[5],.95),sCap(p,J[5],J[6],.85)),min(sCap(p,J[7],J[8],.95),sCap(p,J[8],J[9],.85)));
  ab=min(ab,min(length(p-J[6]),length(p-J[9]))-2.3);
  if(ab<.4){
    float a=min(armD(p,J[4],J[5],J[6],B[5]),armD(p,J[7],J[8],J[9],B[5]));a=smin(a,min(handD(p,0),handD(p,1)),.10);
    m.x=smin(m.x,a,.22);
    for(int s=0;s<2;s++){vec3 e0=s==0?J[4]:J[7],e1=s==0?J[5]:J[8],e2=s==0?J[6]:J[9];vec3 u=normalize(e1-e0),v=normalize(e2-e1);
      vec3 ac=mix(e0,e1,.60);m=U(m,vec2(ringD(p,ac,u,.405*B[5],.15,.05),3.));vec3 fo=normalize(cross(u,s==0?cZ:-cZ)+cZ*.2);
      m=U(m,vec2(length(p-ac-normalize(cZ+(s==0?cX:-cX)*.9)*.46*B[5])-.14,4.));
      m=U(m,vec2(ringD(p,mix(e1,e2,.80),v,.27*B[5],.30,.04),9.));m=U(m,vec2(ringD(p,mix(e1,e2,.64),v,.335*B[5],.05,.05),3.));m=U(m,vec2(ringD(p,mix(e1,e2,.93),v,.235*B[5],.05,.06),3.));
      // shoulder plates: three lames
      vec3 o=p-e0;float ou=dot(o,u);float bd=length(o)-1.5;
      if(bd<.3){vec3 cs=Bc*o;cs.x*=s==0?1.:-1.;vec3 ot=normalize((s==0?cX:-cX)*.62+cY*.62+cZ*.48);
        vec3 pa=normalize((s==0?cX:-cX)*.80+cY*.60);float py=dot(o,pa);vec3 pr=o-pa*py;float R=.53*B[5]+.06;float an=atan(dot(pr,cZ),dot(pr,cross(pa,cZ)));
        float lay=1e3;
        for(int i=0;i<3;i++){float f=float(i);float lim=.48-.36*f;float w=.045*abs(sin(an*(5.+f)));float sh=abs(length(o-pa*(.02-.10*f))-R-.02-.055*(2.-f)*.0-.05*f*.0-.04*(1.-f))-.035;sh=max(sh,lim-py-w);sh=max(sh,py-lim-.62);lay=min(lay,sh);
          float rm=length(vec2(length(o-pa*(.02-.10*f))-R-.04*(1.-f)-.03,py-lim+w-.02))-.045;m=U(m,vec2(rm*.8,3.));}
        lay=max(lay,-cs.x-.62);m=U(m,vec2(lay*.75,9.));
        m=U(m,vec2(sEll(vec3(dot(o-pa*(R+.06),cZ),py-R-.06,dot(o-pa*(R+.06),cross(pa,cZ))),vec3(.26,.14,.26)),4.));m=U(m,vec2(length(vec2(length(pr)-.30,py-R+.0))-.065,3.));
        float ou=dot(o,u);float l2=abs(length(o-u*ou)-.48*B[5]-.05+.05*ou)-.04;l2=max(l2,abs(ou-.78)-.20);m=U(m,vec2(l2*.8,9.));m=U(m,vec2(length(vec2(ou-.99,length(o-u*ou)-.48*B[5]-.03+.05*ou))-.055,3.));}
    }
  }else m=U(m,vec2(ab,1.));
  if(hub<.5){
    m=U(m,vec2(sashD(p,td,vec3(0,-1.25,0),normalize(vec3(.50,.86,0.)),.22),8.));
    m=U(m,armourMap(p,td));
    vec3 c=Bc*(p-J[1]);
    m=U(m,vec2(beadsD(c,td-.12,vec2(0,1.78),.78,.085,36.),6.));
    m=U(m,vec2(beadsD(c,td-.12,vec2(0,1.78),1.02,.115,-1.),3.));m=U(m,vec2(beadsD(c,td-.14,vec2(0,1.78),1.02,.10,30.),4.));
    m=U(m,vec2(beadsD(c,td-.12,vec2(0,1.78),1.22,.065,52.),6.));
    m=U(m,vec2(beadsD(c,td-.05,vec2(0,1.95),3.02,.085,84.),3.));
    m=U(m,vec2(sEll(c-vec3(0,-1.22,1.02*B[1]),vec3(.2,.25,.14)),4.));
  }
  float dh=length(p-J[3])-1.5*S0;
  float far=sCap(p,J[3],J[3]+hY*3.8,1.6);
  if(fan<=0.){
    if(far<min(m.x,.5)+1.6){float a=alive[MAINH];vec2 r;float fb=sCap(p,J[3]-hY*(hair>0.?2.2:.5),J[3]+hY*3.6,1.9);
      if(fb>.4) r=vec2(fb,1.);
      else if(a>=.99){vec3 h=toHead(p,MAINH);r=headMap(h,jawOf(MAINH),true);r.x*=S0;}
      else{r=headsMap(p,m.x);vec2 e=rowMap(p,m.x);r=U(r,e);}
      if(r.y<1.5&&m.y<1.5) m=vec2(smin(m.x,r.x,.04),1.);else m=U(m,r);}
    else m=U(m,vec2(far-.35,1.));
  }else{
    vec3 o=p-J[3];o=vec3(dot(o,rX),dot(o,rY),dot(o,rZ));float bb=sBox(o-vec3(0,.9,-.9),vec3(1.2+6.0*max(1.,spread),3.9,2.2),.3);
    if(bb>.6) m=U(m,vec2(bb,1.));
    else{vec2 r=headsMap(p,m.x),e=rowMap(p,m.x);
      if(e.y<1.5&&m.y<1.5) m=vec2(smin(m.x,e.x,.22),1.);else m=U(m,e);
      if(r.y<1.5&&m.y<1.5) m=vec2(smin(m.x,r.x,.04),1.);else m=U(m,r);}
  }
  if(arms>0.){vec2 r=armsMap(p,m.x);if(r.y>12.5&&r.y<13.5&&m.y<1.5&&r.x<.3&&m.x<.3) m=vec2(smin(m.x,r.x,.2),m.x<r.x?1.:13.);else m=U(m,r);}
  // legs and cloth
  float lb=min(min(sCap(p,J[10],J[11],1.6),sCap(p,J[11],J[12],1.5)),min(sCap(p,J[14],J[15],1.6),sCap(p,J[15],J[16],1.5)));lb=min(lb,min(sCap(p,J[12],J[13],.7),sCap(p,J[16],J[17],.7)));lb=min(lb,length(p-J[0])-2.1);
  lb=min(lb,sCap(p,J[0],.5*(J[12]+J[16]),1.7));
  if(lb>.5) return U(m,vec2(lb,7.));
  float lg=min(sCone(p,J[11],J[12],.42*B[6],.27*B[6]),sCone(p,J[15],J[16],.42*B[6],.27*B[6]));lg=min(lg,min(sCone(p,J[11],mix(J[11],J[12],.3),.42*B[6],.50*B[6]),sCone(p,J[15],mix(J[15],J[16],.3),.42*B[6],.50*B[6])));
  lg=smin(lg,footD(p,J[12],J[18],J[13],B[6]),.12);lg=smin(lg,footD(p,J[16],J[19],J[17],B[6]),.12);
  m=U(m,vec2(lg,1.));
  for(int s=0;s<2;s++){vec3 l0=s==0?J[11]:J[15],l1=s==0?J[12]:J[16];vec3 ld=normalize(l1-l0);
    m=U(m,vec2(ringD(p,mix(l0,l1,.97),ld,.31*B[6],.06,.06),3.));m=U(m,vec2(ringD(p,mix(l0,l1,.90),ld,.32*B[6],.05,.05),6.));}
  vec3 loc;float dt=rDhoti(p,.80,1.10,loc);m=U(m,vec2(dt,7.));
  vec3 q=Bp*(p-J[0]);vec3 qb=vec3(q.x,q.y-.46,q.z*1.16);
  m=U(m,vec2(ringD(qb,vec3(0),vec3(0,1,0),1.22*B[4],.20,.06)*.85,9.));m=U(m,vec2(min(ringD(qb,vec3(0,.23,0),vec3(0,1,0),1.24*B[4],.05,.07),ringD(qb,vec3(0,-.23,0),vec3(0,1,0),1.24*B[4],.05,.07))*.85,3.));
  vec3 bq=q-vec3(0,.46,1.28);m=U(m,vec2(sEll(bq,vec3(.40,.40,.22)),3.));m=U(m,vec2(sEll(bq-vec3(0,0,.18),vec3(.20,.22,.12)),4.));
  vec3 bg=polar(qb,14.,PI/14.);m=U(m,vec2(length(bg-vec3(0,0,1.27*B[4]))-.11,4.));
  // swags of beads over the thighs
  {float ax=abs(q.x);for(int i=0;i<2;i++){float f=float(i);float yy=.10-.30*f-(.55+.22*f)*sin(clamp((ax-.15)/(1.35),0.,1.)*PI);float dd=length(vec2(q.y-yy,dt-.03))-.065;dd=max(dd,ax-1.5);dd=max(dd,-q.z-.2);m=U(m,vec2((dd-.02*cos(ax*34.))*.6,f<.5?3.:6.));}}
  vec3 a=J[0]+pY*.30+pZ*1.22,kn=.5*(J[11]+J[15]);vec3 b=mix(kn,.5*(J[12]+J[16]),.42)+pZ*1.1+Wind*.5;b=mix(b,kn+pY*.75+pZ*.9,smoothstep(2.2,3.2,dot(kn-J[0],pZ)));vec2 pl;float dp=pleatD(p,a,b,.34,.62,pl);m=U(m,vec2(dp+9.*smoothstep(2.5,3.2,dot(kn-J[0],pZ)),8.));
  return m;
}
#else
vec2 map(vec3 p){vec2 m=headMap(p,max(jaw,mouths[MAINH]),false);vec3 f=p-vec3(0,-.92,-.16);m=U(m,vec2(sCone(p,vec3(0,-.3,-.16),vec3(0,-.92,-.16),.45,.46),1.));m=U(m,vec2(sEll(f-vec3(0,-.06,0),vec3(.43,.16,.43)),12.));m=U(m,vec2(ringD(p,vec3(0,-.80,-.16),vec3(0,1,0),.50,.07,.05),3.));return m;}
#endif
// ---------------------------------------------------------------- paint
vec4 cellTex(vec2 t,float col,float row){vec4 d=textureLod(tCells,(vec2(col,row)+clamp(t,.004,.996))/vec2(5.,4.),0.);d.rgb=pow(d.rgb/max(d.a,.003),vec3(2.2));return d;}
void skinHead(vec3 p,vec3 n,vec3 h,int k,mat3 H2F,inout Surf s){
  float jw=max(k==MAINH?jaw:0.,mouths[k]);
  float isH=smoothstep(-1.22,-1.12,h.y)*step(length(h),1.7);isH*=smoothstep(.10,.03,rFace(h,jw));if(isH<=0.) return;
  vec2 e=vec2(1,-1)*.03;vec3 nb=normalize(e.xyy*rBase(h+e.xyy,jw)+e.yyx*rBase(h+e.yyx,jw)+e.yxy*rBase(h+e.yxy,jw)+e.xxx*rBase(h+e.xxx,jw));
  s.ns=normalize(mix(n,H2F*nb,.62*isH*smoothstep(-.4,.2,h.z)));
  vec2 t=(h.xy-faceBox.xy)/(faceBox.zw-faceBox.xy);
  bool own=k==MAINH&&lids[k]>.985&&mouths[k]<.02;
  float lc=floor(clamp(lids[k],0.,1.)*4.+.5),mc=floor(clamp(mouths[k],0.,1.)*2.+.5);
  vec4 d=own?faceDecal(h):(all(greaterThan(t,vec2(0)))&&all(lessThan(t,vec2(1)))?cellTex(t,lc,3.-mc):vec4(0));
  float v=isH*smoothstep(.02,.22,h.z);
  s.base=mix(s.base,d.rgb,d.a*v);s.sh=mix(s.sh,d.rgb*vec3(.46,.40,.62),d.a*v);s.ao*=1.-.22*smoothstep(.3,.8,d.a)*v;
  float eg=eyeglow[k];
  if(eg>.2&&jw>.2&&h.z>.2&&d.a>.6&&lum(d.rgb)<.02&&abs(h.x)<.30&&h.y<-.56&&h.y>-.64-.25*jw){s.cls=4.;s.ink=0.;s.base=mix(hex(0xb02a06),hex(0xff9a30),smoothstep(-.60-.24*jw,-.60,h.y))*eg*(.5+.7*jw);}      // fire in the throat of a laughing head whose eyes burn
  if(eg>.01&&h.z>.2){vec4 g=cellTex(t,lc,0.);if(g.a*eg>.12){s.cls=4.;s.ink=0.;s.base=g.rgb*(.25+1.9*eg)+d.rgb*(1.-eg)*.3;}}
}
void surf(vec3 p,vec3 n,int m,inout Surf s){
#ifdef HEADONLY
  if(m==1) skinHead(p,n,p,MAINH,mat3(1),s);
  vec3 h=p;int k=MAINH;
#else
  ivec3 id;vec3 bd;nearHeads(p,id,bd);int k=id.x;
  vec3 h=toHead(p,k);
  if(m==1){
    if(bd.x<.02){
      float a=min(alive[k],1.);vec3 hh=a<.99?(h-vec3(0,-1.,0))/a+vec3(0,-1.,0):h;
      mat3 M;if(k==MAINH) M=transpose(Bh);else{vec2 c=hC[k];M=mat3(rX,rY,rZ)*mat3(c.x,0,-c.y,0,1,0,c.y,0,c.x);}
      skinHead(p,n,hh,k,M,s);}
    vec3 c=Bc*(p-J[1]);float far=step(1.2,length(p-J[3])/S0);
    float ik=max(neckInk(c),bellyInk(Bp*(p-J[0])))*far;s.base=mix(s.base,s.sh*.6,ik*.8);s.sh*=1.-.5*ik;
    if(navel>.01){vec3 q=Bp*(p-J[0]);float r=length(vec2(q.x,q.y-1.38));if(q.z>0.&&r<.42*navel){float g=smoothstep(.42*navel,.05,r);s.cls=4.;s.ink=0.;s.base=mix(hex(0xd8501a),hex(0xfff2b0),g*g)*(1.+3.*navel*g);}}
  }
  if((m==1||m==2||m==3||m==4||m==6||m==17)&&bd.x<.05) s.part+=float(k-(k/2)*2)*24.+(k==MAINH?0.:24.*0.);
  if(m==13){vec3 c=Bc*(p-J[1]);vec3 q=vec3(abs(c.x),c.yz)-vec3(1.35*B[11],.80,-.95);float a=atan(q.y,q.x);s.part=24.+mod(floor((a+.2)/((armTop+1.10)/8.)),2.)*8.;float r=length(q.xy);s.base*=mix(.62,1.,smoothstep(.8,4.,r));s.sh*=mix(.62,1.,smoothstep(.8,4.,r));}
  if(m==7){vec3 loc;rDhoti(p,.80,1.10,loc);float u=loc.x,a=loc.y;vec3 hp=loc.z<.5?J[10]:J[14],he=loc.z<.5?mix(J[11],J[12],.8):mix(J[15],J[16],.8);float u2=dot(p-hp,he-hp)/dot(he-hp,he-hp);
    float bdr=smoothstep(.80,.815,u);s.base=mix(s.base,hex(0xd9962a),bdr);s.sh=mix(s.sh,hex(0x6a3212),bdr);
    float ln=step(.5,fract(u*54.))*step(.775,u)*step(u,.835);s.base=mix(s.base,hex(0x7a0f1a),ln);
    vec2 z=vec2(fract(a*2.228)-.5,(u-.90)*9.);float lt=abs(length(z*vec2(1.,.7))-.30)-.06;s.base=mix(s.base,hex(0x8a1420),smoothstep(.02,-.02,lt)*bdr);
    vec2 g=vec2(a*1.592,u2*11.);g.x+=.5*mod(floor(g.y),2.);vec2 f=fract(g)-.5;float pt=length(f*vec2(1.,1.25));float an=atan(f.x,f.y);
    float bl=smoothstep(.04,.0,pt-.20-.06*cos(an*6.))*(1.-smoothstep(.0,.03,.09-pt))*(1.-bdr)*step(.10,u);s.base=mix(s.base,hex(0xe2a53a),bl*.9);s.sh=mix(s.sh,hex(0x7a3a14),bl*.9);
    float fl=sin(a*9.+u*5.);s.base*=1.-.22*smoothstep(.55,.95,-fl)*smoothstep(.1,.5,u);s.ink=.8;}
  if(m==8){vec3 c=Bc*(p-J[1]);vec3 q=Bp*(p-J[0]);if(q.y<.4){float u=-q.y;float e=smoothstep(3.9,3.95,u);s.base*=.94+.10*sin(q.x*26.);float bb=step(.42,fract(u*.9))*step(fract(u*.9),.58);s.base=mix(s.base,hex(0xe0a034),bb*.85);}else{float w=dot(c-vec3(0,-1.25,0),normalize(vec3(.50,.86,0.)));s.base=mix(s.base,hex(0xe0a034),smoothstep(.14,.16,abs(w)));}}
#endif
  if(m==2||m==17){float st=sin(h.y*34.+h.x*9.*sign(h.x)+6.*vn3(h*4.));s.base*=1.+.35*smoothstep(.6,1.,st);if(m==2&&h.z<.1){float aa=atan(h.x,-(h.z+.26))+.07*sin(h.y*3.2);float g=smoothstep(.75,.98,cos(aa*39.+sin(h.y*5.)))*smoothstep(.15,.6,vn(vec2(aa*9.,h.y*1.3)));s.base=mix(s.base,hex(0x4a3a5c),g*.8);s.ink=.7;}}
  if(m==12){float fl=.75+.25*sin(fT*9.+p.x*7.)+.25*vn3(p*5.+vec3(0,-fT*3.,0));float g=smoothstep(.2,.9,dot(n,normalize(vec3(.1,.8,.6)))*.5+.5);s.base=mix(hex(0xa02406),hex(0xffa838),g)*(.55+.75*fl)+hex(0xffd070)*.5*smoothstep(.55,.9,vn3(p*4.+vec3(0,-fT*2.,0)));s.ink=.0;}
  if(m==9) s.ink=.75;
#ifndef HEADONLY
  if(m==15){s.ink=.75;vec3 o=p-J[3];o=vec3(dot(o,rX),dot(o,rY),dot(o,rZ));float ax=abs(o.x),w=6.75;float u=ax/w,hg=mix(1.15,.50,u);float yy=(o.y-(-1.28+.085*ax-hg*.5))/hg;vec2 z=vec2(fract(ax/.70)-.5,yy);float r=length(z*vec2(1.,1.25));float ln=smoothstep(.035,.015,abs(r-.40))+smoothstep(.05,.02,abs(abs(yy)-.40));float pt=smoothstep(.05,.0,abs(length(vec2(abs(z.x)-.5,yy+.1))-.16));s.base*=1.-.55*clamp(ln+pt*.8,0.,1.);}
  if(m==12){}
#endif
}
#define initRig initRav
