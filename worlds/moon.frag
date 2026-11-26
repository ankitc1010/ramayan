// a painted full moon: pale disc, grey-blue seas, a soft ring.  dir (world), R radians, cA lit, cB seas, amt
#include "sky.glsl"
in vec2 uv;out vec4 o;uniform vec2 res;uniform mat3 CamR;uniform float fl,R,amt,glow;uniform vec3 dir,cA,cB,cG;
void main(){vec2 s=(uv*2.-1.)*vec2(res.x/res.y,1.);vec3 d=normalize(transpose(CamR)*vec3(s,fl));vec3 m=normalize(dir),x=normalize(cross(vec3(0,1,0),m)),y=cross(m,x);vec2 q=vec2(dot(d,x),dot(d,y))/sin(R);if(dot(d,m)<0.){o=vec4(0);return;}float r=length(q);
 float w=fbm(q*2.1+vec2(3.,7.)),w2=fbm(q*5.+9.);float sea=smoothstep(.50,.56,w+.12*(w2-.5)-.12*r*r);float sea2=smoothstep(.60,.64,w+.12*(w2-.5)-.12*r*r);vec3 c=mix(cA,cB,sea*.55+sea2*.35);c*=.93+.12*fbm(q*16.);c*=1.-.20*smoothstep(.6,1.,r);float cr=0.;for(int i=0;i<7;i++){vec2 h=h22(vec2(float(i),4.))*1.5-.75;float k=length(q-h)-.03-.05*h21(h);cr+=smoothstep(.012,.0,abs(k))*.35;}c=mix(c,cB,cr*.6);
 c=mix(c,cB*.7,smoothstep(.016,.004,abs(r-.985))*.55);
 float aa=1.5/(res.y*.5*fl*sin(R));float a=smoothstep(1.+aa,1.-aa,r)*amt;float g=exp(-max(r-1.,0.)*2.2)*.55+exp(-max(r-1.,0.)*9.)*.35;vec3 gl=cG*g*glow*(1.-a)*amt;float rg=(smoothstep(.02,.0,abs(r-1.20))+smoothstep(.012,.0,abs(r-1.25)))*.22*glow;gl+=cG*rg*(1.-a);
 o=vec4(c*a+gl,a);}
