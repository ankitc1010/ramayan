#version 430
// instanced standing cards.  a = (width, height, flip, phase)  b = (anchor x 0..1, anchor y 0..1 from below, yaw or 99 = face camera, lean)
in vec2 q;in vec3 pos;in vec4 a;in vec4 b;in vec4 tint;
uniform vec3 ro;uniform mat3 CamR;uniform float fl,far,fT,wind,upright;uniform vec2 res;
out vec2 vuv;out vec3 wp;flat out vec4 vt;out float hy;flat out float fid;
void main(){vec2 l=vec2((q.x-b.x)*a.x,(q.y-b.y)*a.y);float h=max(0.,q.y-b.y);
 l.x*=a.z;l.x+=b.w*l.y+wind*a.y*.020*h*h*(sin(fT*1.1+a.w)+.5*sin(fT*2.3+a.w*2.7+q.x*2.));
 vec3 R;if(b.z<50.){R=vec3(cos(b.z),0,-sin(b.z));}else{vec3 v=pos-ro;v.y=0.;if(dot(v,v)<1e-4)v=vec3(0,0,-1);v=normalize(v);R=normalize(vec3(-v.z,0,v.x));}
 vec3 U=mix(vec3(CamR[0][1],CamR[1][1],CamR[2][1]),vec3(0,1,0),upright);
 vec3 w=pos+R*l.x+U*l.y;wp=w;vec3 c=CamR*(w-ro);vuv=q;vt=tint;hy=h;fid=float(gl_InstanceID);
 gl_Position=vec4(c.x*fl*res.y/res.x,c.y*fl,(c.z/far*2.-1.)*c.z,c.z);}
