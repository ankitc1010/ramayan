// KIND 0 bow, 1 arrow, 2 gada, 3 sword, 4 ring, 5 lamp (diya), 6 sandal, 7 spear, 8 conch, 9 quiver, 10 stone, 11 crown on its own
#ifndef KIND
#define KIND 0
#endif
#if KIND==0
// bow: grip at the origin, limbs along y, arrow flies +z.  pr[0] = pull distance behind the grip, pr[1] = half length
float limb(vec3 p,out float u){vec3 q=vec3(p.x,abs(p.y),p.z);float L=pr[1],pl=clamp((pr[0]-1.0)/3.,0.,1.2);float d=1e3;u=0.;vec3 a=vec3(0);
  for(int i=1;i<=11;i++){float k=float(i)/11.;vec3 b=vec3(0,L*k*(1.-.10*pl*k),-(.95+.95*pl)*k*k+.62*sin(k*PI*.98)*(.65-.35*pl)+.40*smoothstep(.78,1.,k));
    float r=mix(.17,.085,k);float t=segT(q,a,b);float dd=length(q-mix(a,b,t))-r;if(dd<d){d=dd;u=k-(1.-t)/11.;}a=b;}
  return d;}
vec3 tipP(){float L=pr[1],pl=clamp((pr[0]-1.0)/3.,0.,1.2);return vec3(0,L*(1.-.10*pl),-(.95+.95*pl)+.62*sin(PI*.98)*(.65-.35*pl)+.40);}
vec2 map(vec3 p){float u;vec3 q=vec3(p.x,abs(p.y),p.z);float d=limb(p,u);
  vec2 m=vec2(d,9.);
  float grip=sCap(q,vec3(0),vec3(0,.55,0),.20);m=U(m,vec2(grip,12.));
  m=U(m,vec2(length(q-vec3(0,.66,.06))-.25,3.));
  float rg=abs(fract(u*5.+.5)-.5)*2.;if(u>.12)m=U(m,vec2(max(d-.045,.0+(.80-rg)*.0+ (rg<.86?.04:-.02)),3.));
  vec3 t=tipP();m=U(m,vec2(sEll(q-t-vec3(0,.06,.05),vec3(.13,.30,.13)),3.));m=U(m,vec2(length(q-t-vec3(0,.40,.08))-.11,4.));
  if(abs(pr[2])>.5){float j=.10*sin(p.x*31.+p.z*23.)+.07*sin(p.z*57.);m.x=max(m.x,-sign(pr[2])*p.y+.12+j);return m;}      // pr[2] = +1 / -1: the broken upper / lower half, no string
  vec3 nk=vec3(0,0,-pr[0]);m=U(m,vec2(sCap(q,t,nk,max(.028,pr[3])),13.));return m;}
#elif KIND==1
// arrow: nock at the origin, points +z, length pr[0]; pr[1] = head size ; pr[2] fire
vec2 map(vec3 p){float L=pr[0];vec2 m=vec2(sCap(p,vec3(0),vec3(0,0,L-.3),.052),9.);
  vec3 q=p-vec3(0,0,L);float hs=pr[1];float w=.22*hs*smoothstep(.10,-.45,q.z/hs)*smoothstep(-.95,-.55,q.z/hs);vec2 e=abs(q.xy)-vec2(w,.035*hs),e2=abs(q.yx)-vec2(w*.8,.035*hs);float hd=min(length(max(e,0.))+min(max(e.x,e.y),0.),length(max(e2,0.))+min(max(e2.x,e2.y),0.));hd=max(hd,max(q.z-.03*hs,-q.z-.97*hs));m=U(m,vec2(hd*.6,10.));
  m=U(m,vec2(sCap(p,vec3(0,0,L-1.*hs),vec3(0,0,L-.7*hs),.085),3.));
  for(int i=0;i<3;i++){float a=float(i)*2.0944+.5;vec3 r=p;r.xy=rot(a)*r.xy;float h=.26*smoothstep(0.,.25,r.z)*smoothstep(1.15,.8,r.z);vec2 f=abs(vec2(r.x,r.y-.05))-vec2(.018,h);float fd=max(length(max(f,0.))+min(max(f.x,f.y),0.),abs(r.z-.6)-.55);m=U(m,vec2(fd*.7,11.));}
  return m;}
#elif KIND==2
// gada: grip at the origin, head toward +y
vec2 map(vec3 p){vec2 m=vec2(sCap(p,vec3(0,-1.6,0),vec3(0,3.6,0),.17),9.);m=U(m,vec2(length(p-vec3(0,-1.8,0))-.32,3.));
  vec3 q=p-vec3(0,4.7,0);float a=atan(q.x,q.z);float s=length(q*vec3(1.,.92,1.))-1.22-.10*cos(a*8.)*smoothstep(1.25,.3,abs(q.y));m=U(m,vec2(s*.8,3.));
  m=U(m,vec2(sTor(q,1.28,.12),3.));vec3 g=polar(q,8.,.39);m=U(m,vec2(length(g-vec3(0,0,1.32))-.19,4.));
  m=U(m,vec2(sEll(p-vec3(0,6.15,0),vec3(.28,.55,.28)),3.));m=U(m,vec2(sTor(p-vec3(0,3.45,0),.36,.12),3.));m=U(m,vec2(sTor(p-vec3(0,5.85,0),.42,.10),3.));return m;}
#elif KIND==3
// sword (curved khadga): grip at the origin, blade toward +y
vec2 map(vec3 p){vec2 m=vec2(sCap(p,vec3(0,-.55,0),vec3(0,.45,0),.15),12.);m=U(m,vec2(length(p-vec3(0,-.75,0))-.22,3.));m=U(m,vec2(sBox(p-vec3(0,.55,0),vec3(.62,.10,.18),.08),3.));
  vec3 q=p;q.x-=.055*q.y*q.y*.5;float w=mix(.26,.44,smoothstep(1.,4.4,q.y))*smoothstep(5.6,4.5,q.y);vec2 e=abs(q.xz)-vec2(w,.05);float d=length(max(e,0.))+min(max(e.x,e.y),0.);d=max(d,abs(q.y-3.05)-2.45);m=U(m,vec2(d*.6,10.));return m;}
#elif KIND==4
// ring with a ruby, axis z, radius 1
vec2 map(vec3 p){float a=atan(p.x,p.y);float d=length(vec2(length(p.xy)-1.,p.z))-.17-.025*cos(a*24.);vec2 m=vec2(d*.9,3.);vec3 q=p-vec3(0,1.28,0);m=U(m,vec2(sEll(q,vec3(.46,.20,.40)),3.));m=U(m,vec2(sEll(q-vec3(0,.17,0),vec3(.31,.22,.27)),4.));
  vec3 b=polar(q,10.,0.);m=U(m,vec2(length(b-vec3(0,.10,.40))-.075,3.));return m;}
#elif KIND==5
// clay/brass diya: rim radius 1, spout toward +x
vec2 map(vec3 p){vec3 q=p;q.x-=.35*smoothstep(.2,1.4,q.x);q.z*=1.+.45*smoothstep(.3,1.3,p.x);float o=sEll(q-vec3(0,.10,0),vec3(1.05,.62,1.0));float in_=sEll(q-vec3(0,.28,0),vec3(.92,.58,.86));float d=max(o,p.y-.28);d=smax(d,-in_,.05);
  vec2 m=vec2(d*.8,3.);m=U(m,vec2(max(abs(length(p.xz)-.52)-.05,abs(p.y+.45)-.08)-.02,3.));
  float oil=max(sEll(q-vec3(0,.28,0),vec3(.90,.56,.84)),abs(p.y-.12)-.02);m=U(m,vec2(oil,14.));m=U(m,vec2(sCap(p,vec3(.2,.12,0),vec3(1.28,.34,0),.075),6.));return m;}
#elif KIND==6
// wooden sandal (paduka), toe +z
vec2 map(vec3 p){float w=.40+.10*smoothstep(-.9,.6,p.z);vec2 e=vec2(length(vec2(max(abs(p.x)-w+.3,0.),max(abs(p.z)-1.05,0.)))-.3,abs(p.y)-.10);float d=length(max(e,0.))+min(max(e.x,e.y),0.)-.04;vec2 m=vec2(d,9.);
  m=U(m,vec2(sBox(p-vec3(0,-.28,.55),vec3(.36,.20,.14),.05),9.));m=U(m,vec2(sBox(p-vec3(0,-.28,-.65),vec3(.36,.20,.16),.05),9.));m=U(m,vec2(sCap(p,vec3(0,.1,.72),vec3(0,.42,.72),.06),3.));m=U(m,vec2(length(p-vec3(0,.52,.72))-.14,3.));return m;}
#elif KIND==7
// spear along y
vec2 map(vec3 p){vec2 m=vec2(sCap(p,vec3(0,-5.,0),vec3(0,5.,0),.085),9.);vec3 q=p-vec3(0,5.9,0);float w=.34*smoothstep(1.,-.35,q.y)*smoothstep(-1.,-.55,q.y);vec2 e=abs(q.xz)-vec2(w,.06);float d=max(length(max(e,0.))+min(max(e.x,e.y),0.),abs(q.y)-.98);m=U(m,vec2(d*.6,10.));m=U(m,vec2(length(p-vec3(0,4.85,0))-.18,3.));return m;}
#elif KIND==9
// quiver: opening +y, length 4, with arrow fletchings
vec2 map(vec3 p){float r=length(p.xz);float d=max(r-mix(.38,.56,smoothstep(-2.2,2.,p.y)),abs(p.y)-2.2);vec2 m=vec2(d*.9,12.);m=U(m,vec2(sTor(p-vec3(0,2.1,0),.55,.10),3.));m=U(m,vec2(sTor(p-vec3(0,0,0),.50,.07),3.));m=U(m,vec2(sTor(p-vec3(0,-2.1,0),.40,.10),3.));
  for(int i=0;i<5;i++){float a=float(i)*1.2566;vec3 q=p-vec3(cos(a)*.28,2.9+.2*sin(float(i)*3.),sin(a)*.28);m=U(m,vec2(sCap(q,vec3(0,-1.,0),vec3(0,.5,0),.05),9.));m=U(m,vec2(sBox(q-vec3(0,.25,0),vec3(.16,.36,.03),.02),11.));m=U(m,vec2(sBox(q-vec3(0,.25,0),vec3(.03,.36,.16),.02),11.));}return m;}
#elif KIND==10
vec2 map(vec3 p){float d=sBox(p,vec3(1.35,.75,.95),.25);d-=.10*fbm3(p*1.7)+.05*vn3(p*5.);return vec2((d+.06)*.8,9.);}
#elif KIND==11
vec2 map(vec3 h){vec3 c=h;float r=length(c.xz),a=atan(c.x,c.z);float d=max(abs(r-.80)-.045,abs(c.y)-.115)-.02;d=min(d,sTor(c-vec3(0,-.12,0),.815,.045));d=min(d,sTor(c-vec3(0,.13,0),.80,.040));
  vec3 g=polar(c,28.,0.);float gem=sEll(g-vec3(0,0,.86),vec3(.05,.065,.04));vec3 q=polar(c,12.,0.)-vec3(0,.30,.80);q.yz=rot(-.16)*q.yz;float pet=sEll(q,vec3(.19,.24,.05));d=min(d,max(pet,-(sEll(q-vec3(0,-.02,.045),vec3(.11,.15,.04)))));float gem2=sEll(q-vec3(0,-.02,.02),vec3(.06,.09,.04));
  float y=c.y-.18;float prof=max(.70-.36*y-.10*sin(y*9.5)*step(0.,y),.10);float cone=max(abs(r-prof+.05)-.05,max(-y,y-1.28))*.72;cone-=.02*cos(a*16.)*smoothstep(1.3,.1,y);d=min(d,cone);d=min(d,length(c-vec3(0,1.56,0))-.13);d=min(d,sEll(c-vec3(0,1.74,0),vec3(.06,.18,.06)));
  vec3 f=h-vec3(0,.38,.86);f.yz=rot(-.20)*f.yz;float pl=sEll(f,vec3(.27,.42,.07));pl=max(pl,-sEll(f-vec3(0,0,.07),vec3(.19,.32,.05)));d=min(d,pl);gem=min(gem,sEll(f-vec3(0,-.03,.04),vec3(.10,.17,.06)));return U(U(vec2(d,3.),vec2(gem,4.)),vec2(gem2,5.));}
#else
vec2 map(vec3 p){return vec2(length(p)-1.,9.);}
#endif
void surf(vec3 p,vec3 n,int m,inout Surf s){
#if KIND==10
  float v=fbm3(p*2.3);s.base*=.75+.5*v;s.sh*=.75+.5*v;
#endif
  if(m==9){float g=sin(p.x*40.+6.*vn3(p*3.))*.06;s.base*=1.+g;}
}
