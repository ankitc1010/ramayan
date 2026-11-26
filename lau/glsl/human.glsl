// Skeleton uniforms and body parts in figure space: y up, z forward, x = the figure's LEFT, 1 unit = half a head height.
#include "sdf.glsl"
uniform vec3 J[20];      // 0 pelvis 1 chest 2 neck 3 head 4 shL 5 elL 6 wrL 7 shR 8 elR 9 wrR 10 hipL 11 knL 12 anL 13 toeL 14 hipR 15 knR 16 anR 17 toeR 18 heelL 19 heelR
uniform mat3 Bp,Bc,Bh,BL,BR;   // figure -> local frames: pelvis, chest, head, left hand, right hand
uniform vec4 HF[40];     // finger joints xyz,r : [hand*20 + finger*4 + k]  finger 0 thumb .. 4 little
uniform float B[12];     // build: 0 chest width 1 chest depth 2 rib 3 waist 4 hips 5 arm 6 leg 7 hand 8 bust 9 belly 10 neck 11 shoulder
uniform float jaw;       // mouth opening 0..1 (drops the chin)
uniform float fT;        // seconds, for small living motions
uniform vec3 Wind;       // figure-space wind
vec3 pX,pY,pZ,cX,cY,cZ,hX,hY,hZ;
void initRig(){mat3 a=transpose(Bp),b=transpose(Bc),c=transpose(Bh);pX=a[0];pY=a[1];pZ=a[2];cX=b[0];cY=b[1];cZ=b[2];hX=c[0];hY=c[1];hZ=c[2];}

// ---------------------------------------------------------------- torso
float torsoD(vec3 p){
  vec3 c=Bc*(p-J[1]),h=Bp*(p-J[0]),q=vec3(abs(c.x),c.yz);
  float d=sEll(c-vec3(0,.12,-.04),vec3(1.30*B[0],1.18,.80*B[1]));
  d=smin(d,sCone(q,vec3(.10,1.22,-.14),vec3(1.40*B[11],1.06,-.14),.32,.44),.45);
  float pec=sEll(q-vec3(.56*B[0],.48,.47*B[1]),vec3(.60,.43,.27)); d=smin(d,pec,.18);
  if(B[8]>.01){float bu=sEll(q-vec3(.46,.10,.50*B[1]),vec3(.40,.40,.36)*(.55+.45*B[8]));d=smin(d,bu,.18);}
  vec3 a=J[0]+pY*.20,b=J[1]-cY*.45;float t=segT(p,a,b);vec3 o=p-mix(a,b,t),l=mix(Bp*o,Bc*o,t);
  float w=mix(B[3]*.84,B[2]*.80,smoothstep(0.,1.,t));float wa=(length(l*vec3(1.,1.,1.26))-w)*.80;
  wa-=B[9]*.30*exp(-pow((t-.35)*2.6,2.))*smoothstep(-.2,.8,l.z);
  d=smin(d,wa,.42);
  float pe=sEll(h-vec3(0,-.02,-.04),vec3(.98*B[4],.74,.74)); vec3 g=vec3(abs(h.x)-.42,h.y+.28,h.z+.30); pe=smin(pe,length(g)-.50*B[4],.3);
  d=smin(d,pe,.38);
  // sternum, navel, collar
  d=smax(d,-sCone(c,vec3(0,.95,.86*B[1]),vec3(0,.05,.98*B[1]),.06,.05),.14);
  vec3 nv=mix(Bp*(p-mix(a,b,.42)),Bc*(p-mix(a,b,.42)),.5);d=smax(d,-sEll(nv-vec3(0,0,.70*B[3]),vec3(.06,.09,.12)),.10);
  d=smin(d,sCone(q,vec3(.12,1.16,.44*B[1]),vec3(1.12*B[11],1.34,.08),.05,.05),.12);
  return d;
}
float neckD(vec3 p){
  float d=sCone(p,J[2]-cY*.25,J[3]-hY*.70-hZ*.16,.45*B[10],.385*B[10]);
  vec3 c=Bc*(p-J[2]);vec3 q=vec3(abs(c.x),c.yz);
  return smin(d,sCone(q,vec3(.10,.10,-.10),vec3(.85*B[11],-.36,-.06),.30,.24),.30);
}
// ---------------------------------------------------------------- limbs
float armD(vec3 p,vec3 a,vec3 b,vec3 c,float s){
  float d=length(p-a)-.53*s;
  d=smin(d,sCone(p,a,mix(a,b,.40),.47*s,.43*s),.16);
  d=smin(d,sCone(p,mix(a,b,.30),mix(a,b,.66),.43*s,.40*s),.12);
  d=smin(d,sCone(p,mix(a,b,.55),b,.40*s,.30*s),.14);
  vec3 e=mix(b,c,.30);
  d=smin(d,sCone(p,b,e,.30*s,.375*s),.14);
  return smin(d,sCone(p,e,c,.375*s,.205*s),.14);
}
float legD(vec3 p,vec3 a,vec3 b,vec3 c,float s){
  float d=sCone(p,a,mix(a,b,.45),.76*s,.72*s);
  d=smin(d,sCone(p,mix(a,b,.45),b,.72*s,.44*s),.20);
  d=smin(d,length(p-b)-.44*s,.12);
  vec3 bk=normalize(cross(cross(b-a,c-b)+vec3(1e-3,0,0),c-b)); // rough back of the calf
  vec3 e=mix(b,c,.30);
  d=smin(d,sCone(p,mix(b,c,.06),e,.40*s,.48*s),.14);
  return smin(d,sCone(p,e,c,.48*s,.25*s),.16);
}
float footD(vec3 p,vec3 an,vec3 heel,vec3 toe,float s){
  vec3 f=normalize(toe-heel);
  float d=sCone(p,an,mix(an,heel,.7),.22*s,.24*s);
  d=smin(d,length(p-heel)-.24*s,.14);
  d=smin(d,sCone(p,mix(an,heel,.35)+f*.1,toe-f*.25,.25*s,.17*s),.18);
  d=smin(d,sCone(p,heel,toe-f*.35,.20*s,.21*s),.14);
  vec3 sd=normalize(cross(f,vec3(0,1,.02)));
  for(int i=0;i<5;i++){float k=float(i)-2.;d=smin(d,sCone(p,toe-f*(.30+.02*k*k)+sd*k*.115,toe-f*(.02+.05*abs(k))+sd*k*.125,.085*s,.07*s),.04);}
  return d;
}
float handD(vec3 p,int k){
  vec3 w=k==0?J[6]:J[9];float hs=B[7];
  float bd=length(p-w)-1.95*hs; if(bd>.6) return bd;
  vec3 l=(k==0?BL:BR)*(p-w)/hs;
  float d=sBox(l-vec3(0,.46,0),vec3(.335,.40,.15),.14);
  d=smin(d,sCone(l,vec3(0,-.10,0),vec3(0,.30,0),.185,.25),.16);
  d*=hs;
  for(int f=0;f<5;f++){int i=k*20+f*4;float g=sCone(p,HF[i].xyz,HF[i+1].xyz,HF[i].w,HF[i+1].w);
    g=smin(g,sCone(p,HF[i+1].xyz,HF[i+2].xyz,HF[i+1].w,HF[i+2].w),.03);
    g=smin(g,sCone(p,HF[i+2].xyz,HF[i+3].xyz,HF[i+2].w,HF[i+3].w),.03);
    d=smin(d,g,f==0?.16:.05);}
  return d;
}
// ---------------------------------------------------------------- head
uniform float HS[8];   // 0 jaw width 1 chin 2 nose length 3 nose width 4 cheek 5 brow 6 lips 7 face length
float headBase(vec3 p){
  float jd=jaw*.22;
  float d=sEll(p-vec3(0,.20,-.10),vec3(.76,.84,.87));
  d=smin(d,sEll(p-vec3(0,-.26*HS[7]-jd*.4,.13),vec3(.585*HS[0],.74*HS[7]+jd*.5,.63)),.28);
  vec3 q=vec3(abs(p.x),p.yz);
  d=smin(d,length(q-vec3(.31,-.34,.40))-.255*HS[4],.22);
  d=smin(d,sEll(p-vec3(0,-.90*HS[7]-jd,.43),vec3(.20*HS[1],.15,.18)),.24);
  d=smin(d,sCone(q,vec3(.16,-.86*HS[7]-jd,.34),vec3(.52*HS[0],-.50-jd*.6,-.02),.10,.16),.22);
  return d;
}
float headHuman(vec3 p){
  float d=headBase(p);vec3 q=vec3(abs(p.x),p.yz);
  d=smax(d,-(sEll(q-vec3(.31,.02,.87),vec3(.21,.12,.17))),.16);
  d=smin(d,sCone(q,vec3(.08,.16,.715),vec3(.46,.19,.53),.05*HS[5],.03*HS[5]),.12);
  float nl=HS[2];
  float n=sCone(p,vec3(0,.10,.73),vec3(0,-.26*nl,.885),.050,.070*HS[3]);
  n=smin(n,length(p-vec3(0,-.305*nl,.885))-.074*HS[3],.06);
  n=smin(n,length(q-vec3(.10*HS[3],-.335*nl,.80))-.066*HS[3],.07);
  d=smin(d,n,.10);
  float jd=jaw*.20;
  float l=sCone(q,vec3(0,-.555,.79),vec3(.185,-.575,.675),.045*HS[6],.018);
  l=smin(l,sCone(q,vec3(0,-.640-jd,.775),vec3(.15,-.605-jd,.68),.055*HS[6],.02),.02);
  return smin(d,l,.055);
}
float earsD(vec3 p,float lobe){
  vec3 q=vec3(abs(p.x),p.yz)-vec3(.745,-.06,-.06);if(length(q)>.9) return length(q)-.5;
  q.xz=rot(.25)*q.xz;
  float e=sEll(q-vec3(.02,.06,0),vec3(.07,.21,.14));
  e=smin(e,sEll(q-vec3(.02,-.10-.12*lobe,.02),vec3(.055,.10+.07*lobe,.075)),.10);
  return smax(e,-sEll(q-vec3(.09,.06,.02),vec3(.05,.14,.09)),.04);
}
// ---------------------------------------------------------------- cloth
// wrap of both legs to a fraction of the shin, with pleats; returns distance, writes (u along leg 0..1, v round, w which)
float dhotiD(vec3 p,float hem,float loose,out vec3 loc){
  vec3 hL=J[10],kL=J[11],aL=J[12],hR=J[14],kR=J[15],aR=J[16];
  vec3 eL=mix(kL,aL,hem),eR=mix(kR,aR,hem);
  float sc=loose;
  float tl1=segT(p,hL,kL),tl2=segT(p,kL,eL),tr1=segT(p,hR,kR),tr2=segT(p,kR,eR);
  float l1=length(p-mix(hL,kL,tl1)),l2=length(p-mix(kL,eL,tl2)),r1=length(p-mix(hR,kR,tr1)),r2=length(p-mix(kR,eR,tr2));
  bool left=min(l1,l2)<min(r1,r2);
  vec3 h=left?hL:hR,k=left?kL:kR,e=left?eL:eR;
  vec3 ax=normalize(e-h),sx=normalize(cross(ax,pZ+vec3(1e-3)));vec3 sz=cross(sx,ax);vec3 o=p-h;float ang=atan(dot(o,sx),dot(o,sz));
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
  return max(d,q.y-.52)*.80;
}
// long skirt (saree): hull of hips, knees and feet
float skirtD(vec3 p,float len,out vec3 loc){
  vec3 q=Bp*(p-J[0]);
  vec3 a=J[0]-pY*.1,kn=.5*(J[11]+J[15]),an=.5*(J[12]+J[16]);
  float d=sEll(q-vec3(0,-.10,-.04),vec3(1.08*B[4],.80,.84));
  float f=.0;
  vec3 e=mix(kn,an,len);
  float t1=segT(p,a,kn),t2=segT(p,kn,e);float u=(t1*length(kn-a)+t2*length(e-kn))/(length(kn-a)+length(e-kn)+1e-3);
  vec3 ax=normalize(e-a),sx=normalize(cross(ax,pZ+vec3(1e-3))),sz=cross(sx,ax);vec3 o=p-mix(mix(a,kn,t1),mix(kn,e,t2),step(.999,t1));float ang=atan(dot(o,sx),dot(o,sz));
  loc=vec3(u,ang,0);
  f=(.05*sin(ang*13.+u*3.)+.03*sin(ang*7.-u*5.))*smoothstep(.05,.6,u);
  float sp=.5*length(J[12]-J[16]);
  d=smin(d,sCone(p,J[10],J[11],.86,.78),.5);d=smin(d,sCone(p,J[14],J[15],.86,.78),.5);
  d=smin(d,sCone(p,a,kn,.95,.86),.5);
  d=smin(d,sCone(p,kn,e,.86,1.02),.55);
  d=smin(d,sCone(p,J[11],mix(J[11],J[12],len),.70,.74),.6);d=smin(d,sCone(p,J[15],mix(J[15],J[16],len),.70,.74),.6);
  d-=f;
  float cut=max(dot(p-e,normalize(an-kn)),-1e3);d=smax(d,cut-.03,.04);
  return max(d,q.y-.55)*.78;
}
// tapering tongue of pleats hanging from the belt toward tip
float pleatD(vec3 p,vec3 a,vec3 b,float w0,float w1,out vec2 loc){
  float t=segT(p,a,b);vec3 o=p-mix(a,b,t);vec3 y=normalize(b-a),x=normalize(cross(y,pZ+vec3(1e-3,0,0))),z=cross(x,y);
  vec2 l=vec2(dot(o,x),dot(o,z));float w=mix(w0,w1,t);loc=vec2(t,l.x/w);
  float zg=.05*sin(l.x/w*14.);vec2 q=abs(vec2(l.x,l.y+zg*t))-vec2(w,.06);
  float d=length(max(q,0.))+min(max(q.x,q.y),0.)-.03;
  return max(d,max(-dot(p-a,y)-.1,dot(p-b,y)+.03*sin(l.x/w*9.)))*.8;
}
// ring round a bone
float ringD(vec3 p,vec3 c,vec3 ax,float R,float h,float th){vec3 o=p-c;float y=dot(o,ax);float r=length(o-ax*y);vec2 q=abs(vec2(r-R,y))-vec2(th,h);return length(max(q,0.))+min(max(q.x,q.y),0.)-.02;}

// band of cloth that hugs the torso: td = torsoD(p), chest-space plane normal n through c0, half width w
float sashD(vec3 p,float td,vec3 c0,vec3 n,float w){vec3 c=Bc*(p-J[1])-c0;float s=dot(c,n);return max(abs(td-.055)-.04,abs(s+.03*sin(dot(c,vec3(3.,1.,2.))*3.))-w)*.85;}

// beads (or a solid cord, n<0) that lie on the torso: td = torsoD(p); circle of radius R round ctr in chest xy, front side
float beadsD(vec3 c,float td,vec2 ctr,float R,float r,float n){
  vec2 q=c.xy-ctr;float l=length(q);float rad=l-R;float lift=td-r*.55;
  float back=max(0.,-c.z-.15);
  if(n<0.) return (length(vec2(rad,lift))-r+back)*.8;
  float a=atan(q.x,-q.y),st=TAU/n;a=mod(a+st*.5,st)-st*.5;return (length(vec3(a*l,rad,lift))-r+back)*.8;
}
// hand-drawn anatomy on the skin: returns ink amount 0..1 in chest space
float lineA(float d,float w){return 1.-smoothstep(w*.45,w,abs(d));}
float chestInk(vec3 c){
  if(c.z<0.) return 0.;vec2 q=vec2(abs(c.x),c.y);float k=0.;
  vec2 a=q-vec2(.60,.62);float r=length(a*vec2(.92,1.12));float an=atan(a.x,-a.y);k=max(k,lineA(r-.66,.030*smoothstep(1.9,.2,abs(an-.1)))*step(a.y,.15)*step(.06,q.x));
  k=max(k,lineA(q.x,.018)*step(-.05,q.y)*step(q.y,.62)*.8);
  k=max(k,lineA(q.y-1.22-.10*q.x-.04*sin(q.x*3.),.022)*smoothstep(.10,.20,q.x)*smoothstep(1.15,.7,q.x)*.8);
  k=max(k,smoothstep(.065,.045,length(a-vec2(.10,-.30)))*.55);
  return k;
}
float bellyInk(vec3 h){            // pelvis space: soft folds above the belt
  if(h.z<0.) return 0.;float k=0.;for(int i=0;i<2;i++){float y=.98+.30*float(i);k=max(k,lineA(h.y-y-.10*h.x*h.x,.020)*smoothstep(.62,.30,abs(h.x))*.6);}return k;}
float neckInk(vec3 c){if(c.z<-.1) return 0.;float k=0.;for(int i=0;i<3;i++){float y=1.62+.17*float(i);k=max(k,lineA(c.y-y+.20*c.x*c.x*2.,.016)*smoothstep(.34,.2,abs(c.x))*.55);}return k;}

// wrap of both legs whose folds follow each bone, so it survives kneeling and lunging (loc as dhotiD: u along the leg, angle, which leg)
float legWrapB(vec3 p,vec3 h,vec3 k,vec3 a,float hem,out vec3 loc,out float cut){
  vec3 e=mix(k,a,hem),u1=normalize(k-h),u2=normalize(a-k),axm=normalize(u1+u2);float t1=segT(p,h,k),t2=segT(p,k,a),g=smoothstep(-.7,.7,dot(p-k,axm));
  vec3 o=mix(p-mix(h,k,t1),p-mix(k,a,t2),g),ax=normalize(mix(u1,u2,g)),rf=normalize(pZ*.35+k-.5*(h+a));
  vec3 sx=normalize(cross(ax,rf)),sz=cross(sx,ax);float ang=atan(dot(o,sx),dot(o,sz));float L1=length(k-h),L2=length(e-k),u=clamp((dot(p-h,u1)*(1.-g)+(L1+dot(p-k,u2))*g)/(L1+L2),0.,1.);
  loc=vec3(u,ang,0.);float lg=B[6];float d=smin(sCone(p,h,k,.90*lg,.68*lg),sCone(p,k,e,.68*lg,.72*lg),.25);
  float f=(.044*sin(ang*9.+u*4.)+.018*sin(ang*19.-u*7.))*smoothstep(.15,.65,u);cut=dot(p-e,u2)-(1.-g)*4.;return d-f;}
float dhotiB(vec3 p,float hem,out vec3 loc){
  vec3 l0,l1;float c0,c1;float a=legWrapB(p,J[10],J[11],J[12],hem,l0,c0),b=legWrapB(p,J[14],J[15],J[16],hem,l1,c1);loc=a<b?l0:l1;if(a>=b)loc.z=1.;
  float d=smin(a,b,.42);vec3 q=Bp*(p-J[0]);d=smin(d,sEll(q-vec3(0,-.10,-.02),vec3(1.08*B[4],.90,.92)),.38)-.035;
  d=smax(d,(a<b?c0:c1)-.02,.03);return max(d,q.y-.52-2.5*max(0.,length(q.xz)-1.20))*.80;}
