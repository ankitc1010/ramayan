#include "noise.glsl"
in vec2 uv; out vec4 o; uniform sampler2D tex,tBloom,tZ; uniform vec2 res,gres; uniform float frame,bloom,expo,contrast,satu,vig,grain,paper,ca,flash,fade; uniform vec3 shTint,hiTint,flashCol,fadeCol;
vec3 tone(vec3 x){vec3 k=vec3(.72);vec3 s=k+(1.-k)*(1.-exp(-(x-k)/(1.-k)));return mix(x,s,step(k,x));}
void main(){
 vec2 d=(uv-.5);vec2 off=d*dot(d,d)*ca*.004;
 vec3 c=vec3(texture(tex,uv+off).r,texture(tex,uv).g,texture(tex,uv-off).b);
 c+=texture(tBloom,uv).rgb*bloom;
 c*=expo;
 float l=lum(c);c=mix(vec3(l),c,satu);
 c*=mix(shTint,hiTint,smoothstep(.0,.6,l));
 c=pow(max(c,0.)/.18,vec3(contrast))*.18;
 float v=length(d*vec2(1.05,1.18));c*=1.-vig*smoothstep(.38,.95,v);
 c=tone(c);
 vec2 px=uv*res;
 float pp=fbm(px/2.6)*.55+fbm(px/9.+9.)*.45;c*=1.+(pp-.5)*paper;
 c=pow(mix(pow(max(c,0.),vec3(1./2.2)),pow(max(flashCol,0.),vec3(1./2.2)),flash),vec3(2.2));c=mix(c,fadeCol,fade);      // a flash is mixed as it is seen: a tenth of white on a dark frame is not grey
 vec3 s=pow(max(c,0.),vec3(1./2.2));
 vec2 gp=uv*gres;float g=(h21(gp+frame*17.13)+h21(gp*1.31+frame*7.7)-1.);s+=g*grain*(1.1-.8*lum(s));
 s+=(h21(gp+frame*3.1)-.5)/255.;
 o=vec4(s,1);}
