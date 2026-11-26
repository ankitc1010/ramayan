#version 430
in vec3 ip;in vec3 in_;in vec2 iuv;out vec3 vp,vn_;out vec2 vuv;uniform vec3 ro;uniform mat3 CamR;uniform float fl,far;uniform vec2 res;
void main(){vec3 c=CamR*(ip-ro);vp=ip;vn_=in_;vuv=iuv;gl_Position=vec4(c.x*fl*res.y/res.x,c.y*fl,(c.z/far*2.-1.)*c.z,c.z);}
