#include "noise.glsl"
in vec3 vp,vn_;in vec2 vuv;
layout(location=0) out vec4 g0;layout(location=1) out vec4 g1;layout(location=2) out vec4 g2;layout(location=3) out vec4 g3;
uniform vec3 ro;uniform mat3 CamR;uniform float far,objId,cls,inkw,part,ortho,fT;uniform int kind;uniform vec3 cA,cB,cC;uniform sampler2D tCard;uniform vec4 rep;uniform float cutoff;
// kind 0 plain  1 border stripes both edges  2 border + dots  3 textured card (tCard)  4 banner with sun disc  5 leaf scales 6 feather  7 checks
void main(){
  vec3 n=normalize(vn_);vec3 v=vp-ro;if(dot(n,v)>0.) n=-n;vec3 f=transpose(CamR)[2];float vz=dot(v,f);gl_FragDepth=clamp(vz/far,0.,1.);
  vec3 b=cA,s=cB;vec2 u=vuv;float k=abs(u.y-.5)*2.;
  if(kind==1||kind==2){float e=smoothstep(.70,.74,k);b=mix(b,cC,e);float ln=step(.80,k)*step(k,.86);b=mix(b,cA*.5,ln);}
  if(kind==2){vec2 g=fract(vec2(u.x*rep.x,u.y*rep.y))-.5;b=mix(b,cC,smoothstep(.22,.17,length(g))*step(k,.66));}
  if(kind==3){vec4 t=texture(tCard,u);if(t.a<max(cutoff,.02)) discard;b=pow(t.rgb/max(t.a,.01),vec3(2.2))*cA;s=b*cB;}
  if(kind==4){float d=length((u-vec2(.42,.5))*vec2(1.6,1.));b=mix(b,cC,smoothstep(.27,.25,d));float a=atan(u.y-.5,(u.x-.42)*1.6);b=mix(b,cC,smoothstep(.40,.38,d)*step(.30,d)*step(.2,sin(a*14.)));b=mix(b,cC,step(.86,k));}
  if(kind==6){float q=abs(u.y-.5);float bar=sin((u.x*38.+q*26.));b=mix(b,cC,smoothstep(.2,.6,bar)*.5);b=mix(b,s,smoothstep(.03,.0,q));}
  if(kind==7){vec2 g=step(.5,fract(u*rep.xy));b=mix(b,cC,abs(g.x-g.y));}
  float w=sin(u.x*23.+u.y*5.)*.5+.5;if(kind<3) b*=.93+.10*w;
  g0=vec4(n,vz);g1=vec4(b,cls+clamp(inkw,0.,.98)*.98);g2=vec4(s,1);g3=vec4(n,objId*64.+part);
}
