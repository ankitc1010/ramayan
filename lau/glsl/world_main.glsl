// world pass: the shot supplies map(p) (vec2 distance, material) and surf().  Optional defines: TMAX, STEPS, RELAX, EPS, NOAO
#ifndef TMAX
#define TMAX 400.
#endif
#ifndef STEPS
#define STEPS 140
#endif
#ifndef RELAX
#define RELAX .85
#endif
#ifndef EPS
#define EPS .0008
#endif
in vec2 uv;
layout(location=0) out vec4 g0;layout(location=1) out vec4 g1;layout(location=2) out vec4 g2;layout(location=3) out vec4 g3;
uniform vec2 res;uniform float fl,far,ortho,objId;
vec3 nrmW(vec3 p,float e){vec2 k=vec2(1,-1)*e;return normalize(k.xyy*map(p+k.xyy).x+k.yyx*map(p+k.yyx).x+k.yxy*map(p+k.yxy).x+k.xxx*map(p+k.xxx).x);}
void main(){
  vec2 s=(uv*2.-1.)*vec2(res.x/res.y,1.);mat3 C=transpose(CamR);vec3 o=ro,d;if(ortho>0.){d=C[2];o=ro+(C[0]*s.x+C[1]*s.y)*ortho;}else d=normalize(C*vec3(s,fl));
  float t=.05;vec2 m=vec2(0);bool hit=false;
  for(int i=0;i<STEPS;i++){m=map(o+d*t);if(m.x<EPS*max(t,1.)){hit=true;break;}t+=m.x*RELAX;if(t>TMAX)break;}
  if(!hit) discard;
  vec3 p=o+d*t;float vz=dot(p-ro,C[2]);gl_FragDepth=clamp(vz/far,0.,1.);if(ortho>0.){g0=vec4(vz);g1=g2=g3=vec4(0);return;}
  vec3 n=nrmW(p,max(.003,.0012*t));Surf f;f.base=vec3(.5);f.sh=vec3(.2);f.cls=1.;f.ink=.8;f.part=m.y;f.ns=n;f.ao=1.;f.glow=0.;
  surf(p,n,int(m.y+.5),f);
  float ao=1.;
#ifndef NOAO
  ao=0.;float k=max(.10,.012*t);for(int i=1;i<=4;i++){float q=float(i)*k;ao+=max(0.,q-map(p+n*q).x)/q;}ao=clamp(1.-ao*.24,0.,1.);
#endif
  g0=vec4(n,vz);g1=vec4(f.base*(1.+f.glow),f.cls+clamp(f.ink,0.,.98)*.98);g2=vec4(f.sh,ao*f.ao);g3=vec4(f.ns,objId*64.+f.part);
}
