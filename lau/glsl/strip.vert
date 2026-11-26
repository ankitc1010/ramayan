#version 430
in vec3 ip;in vec4 iuv;out vec4 vuv;out float vz;uniform vec3 ro;uniform mat3 CamR;uniform float fl;uniform vec2 res;uniform int space;
void main(){vuv=iuv;if(space==1){vz=0.;gl_Position=vec4(ip.x/res.x*2.-1.,1.-ip.y/res.y*2.,0,1);return;}
 vec3 c=CamR*(ip-ro);vz=c.z;gl_Position=c.z<.05?vec4(2,2,2,1):vec4(c.x*fl*res.y/res.x,c.y*fl,0,c.z);}
