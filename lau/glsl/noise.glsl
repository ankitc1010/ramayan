// hashes, value noise, fbm, voronoi
#define PI 3.14159265
#define TAU 6.2831853
float h11(float p){p=fract(p*.1031);p*=p+33.33;p*=p+p;return fract(p);}
float h21(vec2 p){vec3 p3=fract(vec3(p.xyx)*.1031);p3+=dot(p3,p3.yzx+33.33);return fract((p3.x+p3.y)*p3.z);}
vec2 h22(vec2 p){vec3 p3=fract(vec3(p.xyx)*vec3(.1031,.1030,.0973));p3+=dot(p3,p3.yzx+33.33);return fract((p3.xx+p3.yz)*p3.zy);}
float h31(vec3 p3){p3=fract(p3*.1031);p3+=dot(p3,p3.zyx+31.32);return fract((p3.x+p3.y)*p3.z);}
float vn(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*f*(f*(f*6.-15.)+10.);return mix(mix(h21(i),h21(i+vec2(1,0)),f.x),mix(h21(i+vec2(0,1)),h21(i+vec2(1,1)),f.x),f.y);}
float vn3(vec3 p){vec3 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);
 return mix(mix(mix(h31(i),h31(i+vec3(1,0,0)),f.x),mix(h31(i+vec3(0,1,0)),h31(i+vec3(1,1,0)),f.x),f.y),
            mix(mix(h31(i+vec3(0,0,1)),h31(i+vec3(1,0,1)),f.x),mix(h31(i+vec3(0,1,1)),h31(i+vec3(1,1,1)),f.x),f.y),f.z);}
float fbm(vec2 p){float a=.5,s=0.;mat2 m=mat2(.8,.6,-.6,.8);for(int i=0;i<5;i++){s+=a*vn(p);p=m*p*2.03+7.13;a*=.5;}return s;}
float fbm3(vec3 p){float a=.5,s=0.;for(int i=0;i<5;i++){s+=a*vn3(p);p=p*2.03+7.13;a*=.5;}return s;}
float ridge(vec2 p){float a=.5,s=0.;for(int i=0;i<5;i++){float n=1.-abs(2.*vn(p)-1.);s+=a*n*n;p=p*2.07+3.1;a*=.5;}return s;}
// voronoi: x = F1, y = F2-F1 edge, zw = cell hash
vec4 voro(vec2 p){vec2 n=floor(p),f=fract(p);float d1=9.,d2=9.;vec2 id=vec2(0);for(int j=-1;j<=1;j++)for(int i=-1;i<=1;i++){vec2 g=vec2(i,j),o=h22(n+g);float d=length(g+o-f);if(d<d1){d2=d1;d1=d;id=n+g;}else if(d<d2)d2=d;}return vec4(d1,d2-d1,h22(id+17.3));}
float sat(float x){return clamp(x,0.,1.);} vec3 sat(vec3 x){return clamp(x,0.,1.);}
mat2 rot(float a){float c=cos(a),s=sin(a);return mat2(c,-s,s,c);}
vec3 lin(vec3 c){return pow(c,vec3(2.2));}
vec3 hex(int h){return lin(vec3((h>>16)&255,(h>>8)&255,h&255)/255.);}
float lum(vec3 c){return dot(c,vec3(.2126,.7152,.0722));}
