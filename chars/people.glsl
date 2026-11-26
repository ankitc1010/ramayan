// THE PEOPLE.  KIND 0 = women (Sita's body and saree with the extras below), 1 = men and children.
// uniforms beside Sita's: crownk, beard, hairk, robe, shawl, staff, bowl (see people.py)
#ifndef KIND
#define KIND 0
#endif
#if KIND==0
// ================================================================ women
uniform float crownk;                        // 1 = Kaikeyi's tiara
#define EXTRA
vec2 tiara(vec3 p){                          // p in head space: tall, pointed, jewelled, swept back
  vec3 c=p-vec3(0,.10,-.10);c.yz=rot(-.14)*c.yz;vec3 e=vec3(c.x/.97,c.y,c.z/1.04);float r=length(e.xz),a=atan(e.x,e.z);
  float d=max(abs(r-.825)-.035,abs(c.y-.50-.03*cos(a*2.))-.085)-.015;
  vec3 g=polar(e,26.,0.);float gem=sEll(g-vec3(0,.50,.875),vec3(.045,.055,.035));
  float w=exp(-a*a*.62);float top=.60+w*(.62+.34*pow(abs(cos(a*3.5)),3.)*1.);
  float y=(c.y-.56)/max(top-.56,.05);float R=.83-.16*clamp(y,0.,1.)*clamp(y,0.,1.)+.06*clamp(y,0.,1.);
  float body=max(abs(r-R)-.032,max(c.y-top,.54-c.y))*.62;
  float ho=length(vec2(sin(a*3.5)*.30,(c.y-.60-w*.30)*1.1))-.10*w;body=max(body,-max(ho,r-2.)*.6);
  d=min(d,body);
  vec3 f=e-vec3(0,1.02,.80);vec3 f2=f;f.yz=rot(-.06)*f.yz;float pl=sEll(f,vec3(.20,.44,.07));d=min(d,pl);
  gem=min(gem,sEll(f-vec3(0,-.06,.05),vec3(.10,.19,.06)));
  float vg=1e3;for(int i=0;i<9;i++){float t=float(i)/8.*TAU;vg=min(vg,length(f-vec3(cos(t)*.165,sin(t)*.36,.045))-.030);}
  vec3 q=vec3(abs(f2.x),f2.yz);vg=min(vg,sEll(q-vec3(.33,-.10,-.055),vec3(.065,.11,.06)));vg=min(vg,sEll(q-vec3(.57,-.22,-.21),vec3(.05,.085,.06)));
  d=min(d,length(f2-vec3(0,.50,.01))-.07);d=min(d,sEll(f2-vec3(0,.60,.01),vec3(.035,.11,.035)));
  float pd=sEll(p-vec3(0,.50,.775),vec3(.05,.09,.04));vg=min(vg,pd);
  return U(U(vec2(d,3.),vec2(gem,22.)),vec2(vg,23.));
}
vec2 extra(vec3 p,vec3 h,vec3 c,vec3 q,float td){
  vec2 m=vec2(1e3,0.);if(crownk>.5){float b=length(h-vec3(0,.9,0))-1.5;if(b<.4)m=tiara(h);else m=vec2(b,3.);}
  return m;
}
void extraSurf(vec3 p,vec3 h,vec3 c,vec3 q,vec3 n,int m,inout Surf s){
  if(m==3&&crownk>.5&&h.y>.62&&length(h)<3.){                                      // engraving on the tiara
    vec3 e=h-vec3(0,.10,-.10);e.yz=rot(-.14)*e.yz;float a=atan(e.x/.97,e.z/1.04),y=e.y;float k=0.;
    vec2 f=vec2(a*3.5,(y-.80)*3.2);vec2 g=vec2(abs(fract(f.x/PI+.5)-.5)*2.,f.y);float r=length(g-vec2(.0,.1));k=max(k,lineA(r-.42,.07));k=max(k,lineA(r-.62,.04));k=max(k,lineA(length(g-vec2(.72,.75))-.24,.06));k=max(k,smoothstep(.13,.10,length(g-vec2(0.,.1))));
    k=max(k,lineA(y-.625,.02));s.base*=1.-.62*k;s.ink=.8;}
  if(m==22||m==23)s.ink=.7;
}
#else
#define CAST_LIB
#endif
#include "sita.glsl"
#if KIND>0
// ================================================================ men and children
uniform float beard;                         // 0 none .. length in units
uniform int hairk;                           // 0 matted knot, 1 crown, 2 turban, 3 bun, 4 cropped with a side knot
uniform float robe;                          // hem: 0..1 = dhoti to that part of the shin, 2 = long wrapped robe
uniform int shawl;                           // 0 sash across, 1 over both shoulders, 2 wide, one shoulder bare, 3 none
uniform int tunic;                           // 1 = sewn tunic with short sleeves, 2 = long sleeves
uniform float beads;                         // 1 rudraksha, 2 gold of a king
uniform float staff,bowl;
uniform float kid;                           // 1 = a child
float kidTorso(vec3 p){                      // a child's torso
  vec3 c=Bc*(p-J[1]),h=Bp*(p-J[0]),q=vec3(abs(c.x),c.yz);
  float d=sEll(c-vec3(0,-.05,-.03),vec3(.74,.72,.56));
  d=smin(d,sCone(q,vec3(.08,.60,-.06),vec3(.62,.52,-.06),.16,.24),.3);
  vec3 a=J[0]+pY*.1,b=J[1]-cY*.2;float t=segT(p,a,b);vec3 o=p-mix(a,b,t),l=mix(Bp*o,Bc*o,t);
  d=smin(d,(length(l*vec3(1,1,1.16))-mix(.66,.60,t))*.85,.35);
  d=smin(d,sEll(h-vec3(0,-.02,.10),vec3(.64,.52,.60)),.3);
  return smin(d,sEll(h-vec3(0,-.10,-.06),vec3(.70,.52,.58)),.3);
}
float bodyD(vec3 p){return kid>.5?kidTorso(p):torsoD(p);}
float bodyNeck(vec3 p){return kid>.5?sCone(p,J[2]-cY*.2,J[3]-hY*.6-hZ*.12,.27,.25):neckD(p);}
// wrap of both legs, with the folds measured round each bone so that bent knees stay clean
#define HZ (kid>.5?.72:1.)
float legWrap(vec3 p,vec3 h,vec3 k,vec3 a,float hem,out vec3 loc,out float cut){
  vec3 e=mix(k,a,hem),u1=normalize(k-h),u2=normalize(a-k),axm=normalize(u1+u2);float t1=segT(p,h,k),t2=segT(p,k,a),g=smoothstep(-.7,.7,dot(p-k,axm));
  vec3 o=mix(p-mix(h,k,t1),p-mix(k,a,t2),g),ax=normalize(mix(u1,u2,g)),rf=normalize(pZ*.35+k-.5*(h+a));
  vec3 sx=normalize(cross(ax,rf)),sz=cross(sx,ax);float ang=atan(dot(o,sx),dot(o,sz));float L1=length(k-h),L2=length(e-k),u=clamp((dot(p-h,u1)*(1.-g)+(L1+dot(p-k,u2))*g)/(L1+L2),0.,1.);
  loc=vec3(u,ang,0.);float lg=B[6];float d=smin(sCone(p,h,k,.88*lg,.64*lg),sCone(p,k,e,.64*lg,.70*lg),.25);
  float f=(.042*sin(ang*9.+u*4.)+.018*sin(ang*19.-u*7.))*smoothstep(.15,.65,u)*HZ;cut=dot(p-e,u2);return d-f;
}
float dhoti2(vec3 p,float hem,out vec3 loc){
  vec3 l0,l1;float c0,c1;float a=legWrap(p,J[10],J[11],J[12],hem,l0,c0),b=legWrap(p,J[14],J[15],J[16],hem,l1,c1);loc=a<b?l0:l1;if(a>=b)loc.z=1.;
  float d=smin(a,b,.40*HZ);vec3 q=Bp*(p-J[0]);d=smin(d,sEll(q-vec3(0,-.10,-.02),vec3(1.06*B[4],.92,.94)*vec3(1,HZ,HZ*1.05)),.36)-.03;
  d=smax(d,(a<b?c0:c1)-.02,.03);return max(d,q.y-.50-2.5*max(0.,length(q.xz)-1.15*HZ))*.80;
}
vec2 hairs(vec3 h,float dh){
  vec3 q=vec3(abs(h.x),h.yz);float a=atan(h.x,h.z+.1);vec2 m=vec2(1e3,2.);
  float L=.60-.55*q.x*q.x-.45*smoothstep(.30,-.02,h.z)*smoothstep(.40,.72,q.x)-1.20*smoothstep(-.10,-.45,h.z);
  if(hairk==1){                              // long hair under the crown
    float d=sEll(h-vec3(0,.08,-.26),vec3(.83,.88,.84));d=smax(d,h.z-.10,.1);d=smax(d,-(h.y+.85),.1);
    float lk=sCone(q,vec3(.62,-.2,-.42),vec3(.70,-1.45,-.50),.32,.20);d=smin(d,lk,.2)-.014*sin(h.x*22.+h.y*4.);m=vec2(d*.9,2.);
    vec3 c=h-vec3(0,.02,-.08);c.xz/=vec2(.95,1.05);float r=length(c.xz),an=atan(c.x,c.z);
    float k=max(abs(r-.80)-.045,abs(c.y-.60)-.125)-.02;k=min(k,sTor(c-vec3(0,.46,0),.82,.045));k=min(k,sTor(c-vec3(0,.74,0),.80,.04));
    vec3 g=polar(c,22.,0.);float gem=sEll(g-vec3(0,.60,.86),vec3(.055,.07,.04));
    vec3 pt=polar(c,10.,0.)-vec3(0,.92,.79);pt.yz=rot(-.12)*pt.yz;k=min(k,sEll(pt,vec3(.22,.30,.05)));gem=min(gem,sEll(pt-vec3(0,-.02,.04),vec3(.07,.11,.04)));
    float y=c.y-.80;float dome=sEll(c-vec3(0,.82,0),vec3(.70,.72,.70))-.02*cos(an*14.);dome=max(dome,-y);k=min(k,dome*.8);
    k=min(k,length(c-vec3(0,1.60,0))-.12);k=min(k,sEll(c-vec3(0,1.76,0),vec3(.06,.15,.06)));
    return U(U(m,vec2(k*.9,3.)),vec2(gem,4.));}
  if(hairk==2){                              // turban
    float d=sEll(h-vec3(0,.10,-.26),vec3(.80,.82,.78));d=smax(d,h.z-.02,.1);d=smax(d,-(h.y+.62),.1);m=vec2(d*.9,2.);
    vec3 c=h-vec3(0,.56,-.10);c.yz=rot(.10)*c.yz;float w=sEll(c,vec3(.96,.50,1.0));w=smin(w,sEll(c-vec3(.12,.24,0),vec3(.62,.42,.70)),.2);w=max(w,-(h.y-.30+.10*q.x));
    float an=atan(c.x,c.z);float f=c.y*.8+.30*sin(an+.6);w-=.035*abs(sin(f*17.));
    m=U(m,vec2(w*.85,12.));m=U(m,vec2(sEll(c-vec3(.42,.24,.80),vec3(.12,.13,.10)),14.));return m;}
  float d=sEll(h-vec3(0,.21,-.13),vec3(.80,.86,.88));
  if(hairk==4){                              // a child's crop with a knot
    L=.50-.18*abs(sin(h.x*9.))*.6-.35*q.x*q.x-.52*smoothstep(.36,.0,h.z)*smoothstep(.40,.72,q.x)-.75*smoothstep(-.10,-.45,h.z);
    d-=.020*sin(a*18.+h.y*3.);d=smax(d,L-h.y,.06);
    vec3 b=h-vec3(0,1.12,-.22);float kn=sEll(b,vec3(.26,.24,.26))-.02*sin(atan(b.x,b.z)*8.+b.y*9.);d=smin(d,kn,.10);m=vec2(d*.88,2.);
    return U(m,vec2(sTor(b-vec3(0,-.17,0),.20,.055),14.));}
  d-=.014*sin(a*26.+h.y*5.);d=smax(d,L-h.y,.08);
  if(hairk==3){vec3 b=h-vec3(0,.10,-1.02);float bu=sEll(b,vec3(.30,.32,.24))-.02*sin(atan(b.y,b.x)*7.);return vec2(smin(d,bu,.08)*.88,2.);}
  vec3 b=h-vec3(0,1.22,-.26);b.yz=rot(.25)*b.yz;float r=length(b.xz),ab=atan(b.x,b.z);   // jata
  float bun=length(vec2(r-.18,b.y+.20))-.25;bun=smin(bun,length(vec2(r-.13,b.y-.12))-.21,.05);bun=smin(bun,length(b-vec3(0,.38,0))-.17,.05);bun-=.022*sin(ab*9.+b.y*16.);
  d=smin(d,bun,.12);
  float lk=sCone(q,vec3(.52,-.2,-.58),vec3(.62,-1.55,-.62),.32,.20);lk-=.022*sin(h.y*13.+q.x*15.+q.z*6.);m=vec2(min(d,lk)*.88,2.);
  vec3 p2=polar(b-vec3(0,-.38,0),18.,0.);return U(m,vec2(length(p2-vec3(0,0,.43))-.060,9.));
}
float beardD(vec3 p,vec3 h){
  vec3 q=vec3(abs(h.x),h.yz);float jd=jaw*.2;
  vec3 tip=mix(J[3]+hY*(-.95-beard)+hZ*(.62+.10*beard),J[1]+cY*(1.75-beard)+cZ*1.08,smoothstep(.5,1.4,beard));
  vec3 ba=J[3]-hY*(.80+jd)+hZ*.40,bm=mix(ba,tip,.50)+hZ*.05+hX*.04;float d=smin(sCone(p,ba,bm,.40,.33),sCone(p,bm,tip+hX*.06*sin(fT*1.5),.33,.045),.22);
  d=smin(d,sCone(q,vec3(.16,-.78-jd,.40),vec3(.60*HS[0],-.22,.02),.22,.13),.16);
  d=smin(d,sEll(q-vec3(.34,-.58-jd*.5,.40),vec3(.17,.17,.22)),.14);
  float st=sin(h.x*30.+4.*sin(h.y*3.+h.x*5.));d-=.016*st*smoothstep(-.5,-.9,h.y);
  d=smax(d,-sEll(h-vec3(0,-.60-jd*.6,.86),vec3(.19,.075+jd*.5,.30)),.05);
  float mo=smin(sCone(q,vec3(.03,-.475,.765),vec3(.22,-.535,.70),.055,.055),sCone(q,vec3(.22,-.535,.70),vec3(.37,-.66,.54),.055,.02),.06);
  return min(d,mo-.006*sin(h.x*60.));
}
float tunicD(vec3 p,float td,vec3 q){
  float s=B[5],k=kid>.5?.80:1.;float d=td-.05;vec3 a=J[4],b=J[5],a2=J[7],b2=J[8];float e=.52;
  d=max(d,-(q.y-.25));float s1=sCone(p,a,mix(a,b,e+.02),.53*s+.05,.45*s+.05),s2=sCone(p,a2,mix(a2,b2,e+.02),.53*s+.05,.45*s+.05);
  if(tunic<2){s1=smax(s1,dot(p-mix(a,b,e),normalize(b-a)),.02);s2=smax(s2,dot(p-mix(a2,b2,e),normalize(b2-a2)),.02);}
  d=smin(d,s1,.2*k);d=smin(d,s2,.2*k);
  if(tunic==2){vec3 w=J[6],w2=J[9];d=smin(d,sCone(p,mix(a,b,e),b,.45*s+.05,.37*s+.05),.1);d=smin(d,smax(sCone(p,b,mix(b,w,.90),.40*s+.05,.27*s+.06),dot(p-mix(b,w,.86),normalize(w-b)),.02),.1);d=smin(d,sCone(p,mix(a2,b2,e),b2,.45*s+.05,.37*s+.05),.1);d=smin(d,smax(sCone(p,b2,mix(b2,w2,.90),.40*s+.05,.27*s+.06),dot(p-mix(b2,w2,.86),normalize(w2-b2)),.02),.1);
    }
  vec3 c=Bc*(p-J[1]);float ne=length(vec2(c.x,c.y-(kid>.5?.86:1.52)))-(kid>.5?.36:.62);d=smax(d,-ne,.03);
  return d*.9;
}
float shawlE(vec3 c){                        // signed distance of the shawl's region, chest space
  if(shawl==1){float f=abs(abs(c.x)-.92*B[11]-.06*c.y)-.34;float b=max(-(c.y+2.2),abs(c.x)-1.24*B[11]);return c.z>0.?f:max(min(f,b),-9.);}
  if(shawl==2){float s=.78*c.x-.62*c.y+.05;return abs(s)-.95;}
  return 1e3;
}
vec2 map(vec3 p){
  float dh=length(p-J[3]);vec3 c=Bc*(p-J[1]),q=Bp*(p-J[0]),h=Bh*(p-J[3]);
  float td=bodyD(p),sk=smax(td,.12-q.y,.05);
  sk=smin(sk,armD(p,J[4],J[5],J[6],B[5]),.20);sk=smin(sk,armD(p,J[7],J[8],J[9],B[5]),.20);
  sk=smin(sk,handD(p,0),.09);sk=smin(sk,handD(p,1),.09);
  float lg=min(sCone(p,J[11],mix(J[11],J[12],.3),.42*B[6],.47*B[6]),sCone(p,J[15],mix(J[15],J[16],.3),.42*B[6],.47*B[6]));
  lg=min(lg,min(sCone(p,mix(J[11],J[12],.3),J[12],.47*B[6],.24*B[6]),sCone(p,mix(J[15],J[16],.3),J[16],.47*B[6],.24*B[6])));
  float fs=kid>.5?.62:.95;lg=smin(lg,toesD(p,J[12],J[18],J[13],fs,1.),.10);lg=smin(lg,toesD(p,J[16],J[19],J[17],fs,-1.),.10);
  if(robe>1.5){lg=max(lg,-dot(p-.5*(J[12]+J[16]),hemDir(.5*(J[11]+J[15]),.5*(J[12]+J[16])))-.35);if(J[0].y<3.)lg=1e3;}
  sk=min(sk,lg);
  sk=smin(sk,bodyNeck(p),.14);if(dh-2.1<sk)sk=smin(sk,smin(femHead(h),earsD(h,.6),.04),.10);
  vec2 m=vec2(sk,1.);
  float ts=smin(td,min(length(p-J[4]),length(p-J[7]))-.50*B[5],.24);
  float tc=td;
  if(tunic>0){float t=tunicD(p,td,q);m=U(m,vec2(t,9.));tc=min(td,t);}
  if(robe>1.5){vec4 l;float ds=sariD(p,HEM,l);ds=max(ds,(td-.07-max(0.,.46-q.y)*.75-3.*max(0.,length(q.xz)-1.05))*.8);m=U(m,vec2(ds,7.));}
  else{vec3 l;m=U(m,vec2(dhoti2(p,robe,l),7.));}
  float be=max(abs(td-(robe>1.5?.15:.12))-.055,abs(q.y-.42)-.11)*.8;m=U(m,vec2(be,robe>1.5&&beads>1.5?3.:8.));
  if(robe<1.5){vec3 a=J[0]+pY*.40+pZ*(kid>.5?.78:1.0),kn=.5*(J[11]+J[15]);vec3 b=mix(kn,.5*(J[12]+J[16]),robe*.55)+pZ*(kid>.5?.74:1.0)+Wind*.5;vec2 pl;m=U(m,vec2(pleatD(p,a,b,.16,kid>.5?.26:.40,pl),8.));}
  if(shawl==0)m=U(m,vec2(sashD(p,tc-.03,vec3(0,.15,0),normalize(vec3(.62,.78,0.)),.30),8.));
  else if(shawl<3){float sh=abs(min(ts,tunic>0?tc:1e3)-.10-.014*sin(shawl==1?c.x*26.:(.78*c.x-.62*c.y)*20.))-.035;sh=max(sh,shawlE(c));sh=max(sh,-(q.y-(shawl==1?.55:.30)));m=U(m,vec2(sh*.8,8.));}
  if(dh-2.6<m.x){m=U(m,hairs(h,dh));}
  if(beard>0.&&dh-2.6-beard<m.x)m=U(m,vec2(beardD(p,h)*.82,2.));
  if(beads>1.5){m=U(m,vec2(beadsD(c,tc-.02,vec2(0,1.62),.72,.065,40.),6.));m=U(m,vec2(beadsD(c,tc-.02,vec2(0,1.62),.90,.075,30.),3.));m=U(m,vec2(beadsD(c,tc-.02,vec2(0,1.62),1.06,.060,44.),4.));vec3 c2=vec3(c.x*1.2,c.yz);m=U(m,vec2(beadsD(c2,tc-.03,vec2(0,1.62),1.75,.065,64.)*.85,3.));
    vec3 pd=vec3(c.x,c.y+.16,(tc*1.2-.08)+max(0.,-c.z*2.));m=U(m,vec2(sEll(pd,vec3(.20,.24,.10)),3.));m=U(m,vec2(sEll(pd-vec3(0,0,.07),vec3(.11,.14,.06)),4.));
    vec3 e=vec3(abs(h.x),h.yz)-vec3(.79,-.46,-.02);m=U(m,vec2(length(vec2(length(e.xy)-.13,e.z))-.045,3.));m=U(m,vec2(length(e)-.07,4.));}
  else if(beads>.5){m=U(m,vec2(beadsD(c,tc-.04,vec2(0,1.55),.78,.082,30.),9+13.));m=U(m,vec2(beadsD(c,tc-.04,vec2(0,1.55),1.45,.088,46.),22.));}
  if(beads>0.)for(int s=0;s<2;s++){vec3 e0=s==0?J[4]:J[7],e1=s==0?J[5]:J[8],e2=s==0?J[6]:J[9];vec3 u=normalize(e1-e0),v=normalize(e2-e1);
    m=U(m,vec2(ringD(p,mix(e1,e2,.90),v,.235*B[5]+(tunic==2?.06:0.),beads>1.5?.15:.05,.04),beads>1.5?3.:22.));if(tunic==0)m=U(m,vec2(ringD(p,mix(e0,e1,.46),u,.40*B[5],beads>1.5?.12:.05,.04),beads>1.5?3.:22.));}
  if(staff>.5){vec3 g=palmAt(1);vec3 dn=normalize(vec3(g.x*.06,-1,.04));vec3 a=g-dn*4.6,b=g+dn*g.y;float w=.035*sin(p.y*2.1)+.02*sin(p.y*5.3);float t=segT(p,a,b);float d=length(p-mix(a,b,t)-vec3(w,0,w*.6))-.135-.02*sin(p.y*3.7);vec3 o=p-a;d=smin(d,length(vec2(length(o.xy-vec2(.0,.12))-.18,o.z))-.09,.12);m=U(m,vec2(d*.85,13.));
    for(int i=0;i<3;i++)m=U(m,vec2(length(p-a-vec3(.22,-.25-.16*float(i),.10))-.075,22.));}
  if(bowl>.5){vec3 b=(p-palmAt(0)-vec3(0,.44,0))/.72;float d=sEll(b-vec3(0,.12,0),vec3(1.,.82,1.));d=max(d,b.y-.34);d=smax(d,-sEll(b-vec3(0,.28,0),vec3(.86,.74,.86)),.05);m=U(m,vec2(d*.55,13.));m=U(m,vec2(sEll(b-vec3(0,-.08,0),vec3(.80,.32,.80))*.6,21.));}
  if(lamp>.5)m=U(m,lampD(p));
  return m;
}
void surf(vec3 p,vec3 n,int m,inout Surf s){
  vec3 h=Bh*(p-J[3]),c=Bc*(p-J[1]),q=Bp*(p-J[0]);
  if(m==1){
    float isH=facePaint(p,n,s);float ik=0.;
    if(kid<.5&&tunic==0)ik=max(chestInk(c),bellyInk(q))*(1.-isH)*.8;ik=max(ik,neckInk(c)*step(isH,.01)*.7);
    for(int k=0;k<2;k++){vec3 hp=handPaint(p,k,old);ik=max(ik,hp.x*.8);s.base=mix(s.base,mix(s.base,hex(0xf6d8c0),.55),hp.y);
      if(old>.01){vec3 e=k==0?J[5]:J[8],w=k==0?J[6]:J[9];float L=length(w-e),t=dot(p-e,w-e)/L/L;vec3 o=p-mix(e,w,t);if(t>.2&&t<1.02&&length(o)<.6){vec3 sx=normalize(cross(w-e,vec3(.2,.1,1)));float an=atan(dot(o,sx),dot(o,normalize(cross(sx,w-e))));
          float v=sin(an*3.+3.*vn(vec2(t*9.,float(k))));ik=max(ik,lineA(v,.07)*.30*old*smoothstep(.2,.5,t));float cr=sin(t*120.+3.*vn(vec2(an*3.,t*8.)));ik=max(ik,smoothstep(.90,1.,cr)*smoothstep(.52,.68,vn(vec2(an*2.2,t*13.)))*.55*old*smoothstep(.55,.9,t));}}}
    s.base=mix(s.base,s.sh*.62,ik*.85);s.sh=mix(s.sh,s.sh*.45,ik*.8);
  }
  if(m==2){float w=sin(atan(h.x,h.z+.1)*52.+5.*vn(h.xy*vec2(4.,2.)));if(h.y<-.45)w=sin(h.x*38.+4.*sin(h.y*3.+h.x*4.));float ln=smoothstep(.70,.97,w);s.base=mix(s.base,s.sh,ln*.8);s.ns=normalize(s.ns+.12*w*hX);s.ink=.75;}
  if(m==7){float u,a,ht;if(robe>1.5){vec4 l;sariD(p,HEM,l);u=l.w;a=l.y;ht=l.x;}else{vec3 l;dhoti2(p,robe,l);u=l.x;a=l.y;ht=(1.-u)*(kid>.5?3.5:7.);}
    float bw=beads>1.5?.80:.42,t=ht/bw;if(robe>1.5&&ht<.06&&dot(n,hemDir(.5*(J[11]+J[15]),.5*(J[12]+J[16])))>.5){s.base*=.40;s.sh*=.6;s.ink=.6;return;}
    if(t<1.){if(beads>1.5){if(zari(t,a*26./TAU)>.5){s.cls=2.;s.base=vec3(1);}else{s.base=Pb[17];s.sh=Ps[17];}}else{float st=max(step(t,.30),step(.5,t)*step(t,.66));s.base=mix(s.base,Pb[18],st*.9);s.sh=mix(s.sh,Ps[18],st*.85);}}
    else if(beads>1.5){vec2 g=vec2(a*18./TAU,ht*1.2);g.x+=.5*mod(floor(g.y),2.);vec2 f=fract(g)-.5;float an=atan(f.x,f.y);if(length(f)<.14+.05*cos(an*4.)){s.cls=2.;s.base=vec3(.9);}}
    float fl=sin(a*9.+u*5.);s.base*=1.-.22*smoothstep(.5,.95,-fl)*smoothstep(.08,.5,u)*(s.cls==2.?0.:1.);s.ink=.8;}
  if(m==8){float e=-shawlE(c);if(shawl==1||shawl==2){float t=e/.16;if(t<1.&&t>-.2){if(beads>1.5){s.cls=2.;s.base=vec3(1);}else{float st=step(.30,t)*step(t,.75);s.base=mix(s.base,Pb[18],st*.9);s.sh=mix(s.sh,Ps[18],st*.85);}}float fl=sin(shawl==1?c.x*26.:(.78*c.x-.62*c.y)*20.);s.base*=1.-.18*smoothstep(.4,.95,-fl)*(s.cls==2.?0.:1.);}}
  if(m==9){float ne=length(vec2(c.x,c.y-(kid>.5?.86:1.52)))-(kid>.5?.36:.62);float e=c.z>0.?ne:9.;float ht=q.y-.25;e=min(e,ht);
    vec3 a=J[4],b=J[5],a2=J[7],b2=J[8];if(tunic==1){float t1=dot(p-mix(a,b,.52),normalize(b-a)),t2=dot(p-mix(a2,b2,.52),normalize(b2-a2));float rr=.5*B[5]+.12;if(length(p-mix(a,b,.52))<rr)e=min(e,abs(t1));if(length(p-mix(a2,b2,.52))<rr)e=min(e,abs(t2));}
    if(e<(kid>.5?.07:.10)){if(beads>1.5){s.cls=2.;s.base=vec3(1);}else{s.base=Pb[19];s.sh=Ps[19];}}
    else if(beads>1.5&&abs(c.x)<1.2){vec2 f=fract(vec2(c.x,c.y)*2.6+vec2(.5*mod(floor(c.y*2.6),2.),0.))-.5;if(length(f)<.10){s.cls=2.;s.base=vec3(.9);}}}
  if(m==12){s.ink=.8;float f=(h.y-.56)*.8+.30*sin(atan(h.x,h.z)+.6);s.base*=.86+.18*abs(sin(f*17.));}
  if(m==13){s.base*=.8+.35*vn(vec2(p.y*2.,atan(p.x,p.z)*6.));}
  if(m==22)s.ink=.7;
  lampSurf(p,m,s);
}
#endif
