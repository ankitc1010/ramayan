// the figure pass: ray-march map() inside a bounding sphere and write the G-buffer.  Needs map(), surf() from a character.
in vec2 uv;
layout(location=0) out vec4 g0;   // normal xyz, view depth
layout(location=1) out vec4 g1;   // base rgb, class + ink weight fraction
layout(location=2) out vec4 g2;   // shadow rgb, ao
layout(location=3) out vec4 g3;   // shading normal xyz, id
uniform vec2 res;uniform vec3 ro;uniform mat3 CamR;uniform float fl,far,ortho,objId,Sc,stepK,bake;uniform mat4 Mi,Mf;uniform vec4 bnd;
vec3 nrm(vec3 p,float e){vec2 k=vec2(1,-1)*e;return normalize(k.xyy*map(p+k.xyy).x+k.yyx*map(p+k.yyx).x+k.yxy*map(p+k.yxy).x+k.xxx*map(p+k.xxx).x);}
void main(){
  vec2 s=(uv*2.-1.)*vec2(res.x/res.y,1.);mat3 C=transpose(CamR);
  vec3 rw=ro,dw; if(ortho>0.){dw=C[2];rw=ro+(C[0]*s.x+C[1]*s.y)*ortho;}else dw=normalize(C*vec3(s,fl));
  vec3 o=(Mi*vec4(rw,1)).xyz,d=normalize(mat3(Mi)*dw);
  vec3 oc=o-bnd.xyz;float b=dot(oc,d),c=dot(oc,oc)-bnd.w*bnd.w,h=b*b-c;if(h<0.) discard;h=sqrt(h);
  float t=max(-b-h,.02),t1=-b+h;if(t1<0.) discard;
  initRig();
  vec2 m=vec2(0);bool hit=false;float eps=ortho>0.&&bake<.5?.004:.0008;
  for(int i=0;i<130;i++){m=map(o+d*t);if(m.x<eps*max(t,1.)){hit=true;break;}t+=m.x*stepK;if(t>t1)break;}
  if(!hit) discard;
  vec3 p=o+d*t;vec3 pw=(Mf*vec4(p,1)).xyz;float vz=dot(pw-ro,C[2]);
  if(vz<.01) discard;
  gl_FragDepth=clamp(vz/far,0.,1.);
  if(ortho>0.&&bake<.5){g0=vec4(vz);g1=g2=g3=vec4(0);return;}
  vec3 n=nrm(p,.0035);
  Surf f;f.base=Pb[int(m.y+.5)];f.sh=Ps[int(m.y+.5)];f.cls=Pc[int(m.y+.5)];f.ink=.9;f.part=m.y;f.ns=n;f.ao=1.;f.glow=0.;
  surf(p,n,int(m.y+.5),f);
  float ao=0.;for(int i=1;i<=4;i++){float q=float(i)*.085;ao+=max(0.,q-map(p+n*q).x)/q;}
  ao=clamp(1.-ao*.26,0.,1.)*f.ao;
  mat3 Mr=mat3(Mf)/Sc;
  g0=vec4(normalize(Mr*n),vz);g1=vec4(f.base*(1.+f.glow),f.cls+clamp(f.ink,0.,.98)*.98);g2=vec4(f.sh,ao);g3=vec4(normalize(Mr*f.ns),objId*64.+f.part);
}
