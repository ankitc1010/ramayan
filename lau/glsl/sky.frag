// general painted sky.  colours: zenith, middle, horizon, below; sun direction (world), size; clouds
#include "sky.glsl"
in vec2 uv;out vec4 o;uniform vec2 res;uniform mat3 CamR;uniform float fl,fT;
uniform vec3 cZen,cMid,cHor,cLow,sunDir,sunCol,cLit,cCM,cSh,cInk;uniform float sunR,sunGlow,rays,cov,cy0,cy1,cseed,cscale,cdrift,cink,starAmt,halo,layers;
void main(){vec2 s=(uv*2.-1.)*vec2(res.x/res.y,1.);vec3 d=normalize(transpose(CamR)*vec3(s,fl));vec2 p=skyUV(d),sp=skyUV(normalize(sunDir));vec2 q=p-sp;if(q.x>PI)q.x-=TAU;if(q.x<-PI)q.x+=TAU;
 float e=p.y;vec3 c=mix(cHor,cMid,smoothstep(0.,.28,e));c=mix(c,cZen,smoothstep(.22,.85,e));c=mix(c,cLow,smoothstep(.0,-.10,e));
 float tx=fbm(uv*vec2(14.,9.)),tw=fbm(uv*vec2(60.,34.));c*=.93+.11*tx+.05*tw;
 float r=length(q);c+=sunCol*(exp(-r*r*18.)*.40+exp(-r*2.6)*.26)*sunGlow;
 float a=atan(q.y,q.x);float ry=smoothstep(-.15,.15,sin(a*18.+fT*.10))*.5+smoothstep(.3,.5,sin(a*7.-fT*.06))*.5;c+=sunCol*ry*rays*exp(-r*1.9)*smoothstep(sunR,sunR*2.2,r)*.5;
 if(starAmt>0.) c=stars(c,p,starAmt*smoothstep(-.02,.2,e),fT);
 float disc=smoothstep(sunR,sunR-.004,r);c=mix(c,sunCol*1.5,disc*step(1e-4,sunR));
 if(halo>0.){float hb=smoothstep(.006,.0,abs(r-sunR*1.35))+smoothstep(.004,.0,abs(r-sunR*1.55));float bead=smoothstep(.010,.004,length(vec2((fract(a*24./TAU)-.5)*TAU/24.*r,r-sunR*1.45)));c=mix(c,sunCol*1.1,clamp(hb+bead,0.,1.)*halo);}
 if(cov>0.){vec2 dr=vec2(fT*cdrift,0.);
  if(layers>2.5) c=cloudLayer(c,p+dr*.35+vec2(7.1,0.),cseed+9.,cov*.9,cy0*.5,cy0*.5+(cy1-cy0)*.35,cscale*2.6,sp+dr*.35+vec2(7.1,0.),mix(cLit,cHor,.55),mix(cCM,cHor,.60),mix(cSh,cHor,.65),mix(cInk,cHor,.4),cink*.5);
  if(layers>1.5) c=cloudLayer(c,p+dr*.6+vec2(4.3,0.),cseed+5.,cov*.95,cy0*.8,cy0+(cy1-cy0)*.62,cscale*1.6,sp+dr*.6+vec2(4.3,0.),mix(cLit,cHor,.32),mix(cCM,cHor,.38),mix(cSh,cHor,.42),mix(cInk,cHor,.2),cink*.7);
  c=cloudLayer(c,p+dr,cseed,cov,cy0,cy1,cscale,sp+dr,cLit,cCM,cSh,cInk,cink);}
 o=vec4(c,1);}
