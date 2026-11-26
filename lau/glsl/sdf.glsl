#include "noise.glsl"
float smin(float a,float b,float k){float h=max(k-abs(a-b),0.)/k;return min(a,b)-h*h*k*.25;}
float smax(float a,float b,float k){return -smin(-a,-b,k);}
float sEll(vec3 p,vec3 r){float k0=length(p/r),k1=length(p/(r*r));return k0*(k0-1.)/max(k1,1e-4);}
float sCap(vec3 p,vec3 a,vec3 b,float r){vec3 pa=p-a,ba=b-a;float h=clamp(dot(pa,ba)/dot(ba,ba),0.,1.);return length(pa-ba*h)-r;}
float sCone(vec3 p,vec3 a,vec3 b,float r1,float r2){vec3 pa=p-a,ba=b-a;float h=clamp(dot(pa,ba)/dot(ba,ba),0.,1.);return length(pa-ba*h)-mix(r1,r2,h);}
float sTor(vec3 p,float R,float r){return length(vec2(length(p.xz)-R,p.y))-r;}
float sBox(vec3 p,vec3 b,float r){vec3 q=abs(p)-b+r;return length(max(q,0.))+min(max(q.x,max(q.y,q.z)),0.)-r;}
float sCyl(vec3 p,float R,float h,float r){vec2 d=abs(vec2(length(p.xz),p.y))-vec2(R,h)+r;return min(max(d.x,d.y),0.)+length(max(d,0.))-r;}
float sSeg2(vec2 p,vec2 a,vec2 b){vec2 pa=p-a,ba=b-a;return length(pa-ba*clamp(dot(pa,ba)/dot(ba,ba),0.,1.));}
vec2 U(vec2 a,vec2 b){return a.x<b.x?a:b;}
float segT(vec3 p,vec3 a,vec3 b){vec3 ba=b-a;return clamp(dot(p-a,ba)/dot(ba,ba),0.,1.);}
// polar repetition about y: returns p rotated into the nearest of n sectors
vec3 polar(vec3 p,float n,float off){float a=atan(p.x,p.z),s=TAU/n;a=mod(a+off+s*.5,s)-s*.5;float r=length(p.xz);return vec3(sin(a)*r,p.y,cos(a)*r);}
float polarId(vec3 p,float n,float off){return floor((atan(p.x,p.z)+off+PI/n)/(TAU/n));}
