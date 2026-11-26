// marcher of the places: pixel-sized hits, one loop for the normal (short compile), painted sun shadow.  Defines: TMAX STEPS RELAX NOAO SUNSH(steps) SHMAX AOK; BOUND = vec2 bound(o,d) gives (t0,t1)
#ifndef TMAX
#define TMAX 6000.
#endif
#ifndef STEPS
#define STEPS 150
#endif
#ifndef RELAX
#define RELAX .9
#endif
#ifndef SHMAX
#define SHMAX 400.
#endif
#ifndef AOK
#define AOK .9
#endif
in vec2 uv;
layout(location=0) out vec4 g0;layout(location=1) out vec4 g1;layout(location=2) out vec4 g2;layout(location=3) out vec4 g3;
uniform float sunSh;
float sunShadow(vec3 p,vec3 d){
#ifdef SUNSH
  float t=.8,r=1.;for(int i=0;i<SUNSH;i++){float h=map(p+d*t).x;r=min(r,14.*h/t);if(r<.02)return 0.;t+=clamp(h,.8,40.);if(t>SHMAX)break;}return clamp(r,0.,1.);
#else
  return 1.;
#endif
}
void main(){
  vec2 s=(uv*2.-1.)*vec2(res.x/res.y,1.);mat3 C=transpose(CamR);vec3 o=ro,d;if(ortho>0.){d=C[2];o=ro+(C[0]*s.x+C[1]*s.y)*ortho;}else d=normalize(C*vec3(s,fl));
  gRd=d;float px=2./(fl*1080.);float t=.05,t1=TMAX;vec2 m=vec2(0);bool hit=false,flat_=false;
#ifdef BOUND
  vec2 bb=bound(o,d);if(bb.y<bb.x) discard;t=max(t,bb.x);t1=min(t1,bb.y);
#endif
#ifdef SEA0
  float tS=d.y<0.?(SEA0-o.y)/d.y:1e9,pM=M_WATER;vec3 pN=vec3(0,1,0);t1=min(t1,tS);
#define PLANES
#elif defined(PLANES)
  float pM;vec3 pN;float tS=planes(o,d,pM,pN);t1=min(t1,tS);
#endif
  for(int i=min(0,int(fT));i<STEPS;i++){m=map(o+d*t);if(m.x<.32*px*t+.0004&&m.y>.5){hit=true;break;}t+=m.x*RELAX;if(t>t1)break;}
#ifdef PLANES
  if(t>t1&&tS<TMAX*4.&&ortho<=0.){t=tS;m=vec2(0.,pM);hit=true;flat_=true;}
  else
#endif
  if(!hit&&(m.y<.5||m.x>px*t*2.)||t>t1) discard;
  vec3 p=o+d*t;float vz=dot(p-ro,C[2]);gl_FragDepth=clamp(vz/far,0.,1.);if(ortho>0.){g0=vec4(vz);g1=g2=g3=vec4(0);return;}
  gT=t;gPx=px*t;vec3 n=vec3(0);float ao=0.,e=max(.004,.45*gPx),ak=max(AOK,.010*t);
#ifdef NOAO
  const int NS=4;
#else
  const int NS=7;
#endif
  if(flat_){
#ifdef PLANES
  n=pN;
#endif
  }
#ifdef SEA0
  if(!flat_)
#endif
  for(int i=flat_?4:min(0,int(fT));i<NS;i++){bool g=i<4;vec3 k=.57735*(2.*vec3(((i+3)>>1)&1,(i>>1)&1,i&1)-1.);if(i==4) n=normalize(n+1e-9);float q=float(i-3)*ak;float v=map(g?p+k*e:p+n*q).x;if(g) n+=k*v;else ao+=max(0.,q-v)/q;}
  n=normalize(n+1e-9);ao=clamp(1.-ao*.30,0.,1.);
  Surf f;f.base=vec3(.5);f.sh=vec3(.2);f.cls=1.;f.ink=.8;f.part=m.y;f.ns=n;f.ao=1.;f.glow=0.;
  surf(p,n,int(m.y+.5),f);
  bool em=f.cls>3.5&&f.cls<4.5;if(em||f.cls>5.5) ao=1.;
#ifdef SUNSH
  if(sunSh>0.&&!em&&f.cls<5.5&&dot(f.ns,keyDir)>-.1){float k=sunShadow(p+n*max(.25,gPx*1.5),keyDir);k=mix(1.,k,sunSh);vec3 a=f.ns-keyDir*dot(f.ns,keyDir);f.ns=normalize(mix(a-keyDir*.35,f.ns,smoothstep(.30,.62,k))+1e-5);}
#endif
  if(f.cls<1.5&&n.y>.7) f.ink=mix(f.ink,min(f.ink,.18),smoothstep(.55,.30,dot(-d,n)));   // a floor seen edge-on: faint ink, which the shade pass reads as no rim of light
  g0=vec4(n,vz);g1=vec4(f.base*(1.+f.glow),f.cls+clamp(f.ink,0.,.98)*.98);g2=vec4(f.sh,ao*f.ao);g3=vec4(f.ns,objId*64.+mod(f.part,64.));
}
