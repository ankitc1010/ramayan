#version 430
in vec2 q;in vec3 pos;in vec4 a;in vec4 tint;   // a: scale, tile, flip, lean
uniform vec3 ro;uniform mat3 CamR;uniform float fl,far;uniform vec2 res;uniform vec4 box;uniform vec2 grid;uniform float upright;
out vec2 tuv;flat out float sc;flat out float fid;flat out float flp;out vec3 vt;out float vz0;out vec3 wp;
void main(){float h=box.w-box.y;vec2 l=vec2(mix(box.x,box.z,q.x*.5+.5),mix(box.y,box.w,q.y*.5+.5))*a.x;float f=a.z;l.x*=f;l.x+=a.w*l.y;
 vec3 R=vec3(CamR[0][0],CamR[1][0],CamR[2][0]),Uv=mix(vec3(CamR[0][1],CamR[1][1],CamR[2][1]),vec3(0,1,0),upright);vec3 w=pos+R*l.x+Uv*l.y;wp=w;vec3 c=CamR*(w-ro);vec3 c0=CamR*(pos+Uv*(h*.5*a.x)-ro);vz0=c.z;
 float t=a.y;vec2 cell=vec2(mod(t,grid.x),floor(t/grid.x));tuv=(cell+q*.5+.5)/grid;sc=a.x;fid=float(gl_InstanceID);flp=f;vt=tint.rgb;
 gl_Position=c.z<.05?vec4(2,2,2,1):vec4(c.x*fl*res.y/res.x,c.y*fl,(c.z/far*2.-1.)*c.z,c.z);}
