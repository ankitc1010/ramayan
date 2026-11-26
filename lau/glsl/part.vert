#version 430
in vec2 q;in vec3 pos;in vec4 a;in vec4 col;in vec3 vel;
uniform vec3 ro;uniform mat3 CamR;uniform float fl,far;uniform vec2 res;uniform int space;
out vec2 vq;out vec4 vc;out float vz;flat out float kind,seed;out vec2 spx;
void main(){vq=q;vc=col;kind=a.z;seed=a.w;
 if(space==1){vec2 p=pos.xy;vz=0.;if(length(vel.xy)>1e-4){vec2 d=normalize(vel.xy),n=vec2(-d.y,d.x);p+=vel.xy*.5*q.y+n*q.x*a.x;}else{float c=cos(a.y),s=sin(a.y);p+=vec2(c*q.x-s*q.y,s*q.x+c*q.y)*a.x;}
  gl_Position=vec4(p.x/res.x*2.-1.,1.-p.y/res.y*2.,0,1);spx=p;return;}
 vec3 c=CamR*(pos-ro);
 if(length(vel)>1e-5){vec3 cv=CamR*vel;vec3 c0=c-cv*.5,c1=c+cv*.5;c0.z=max(c0.z,.05);c1.z=max(c1.z,.05);vec3 cc=mix(c0,c1,q.y*.5+.5);vec2 d=c1.xy/c1.z-c0.xy/c0.z;d=length(d)>1e-6?normalize(d):vec2(0,1);cc.xy+=vec2(-d.y,d.x)*q.x*a.x;c=cc;}
 else{float k=cos(a.y),s=sin(a.y);c.xy+=vec2(k*q.x-s*q.y,s*q.x+k*q.y)*a.x;}
 vz=c.z;gl_Position=c.z<.05?vec4(2,2,2,1):vec4(c.x*fl*res.y/res.x,c.y*fl,0,c.z);spx=vec2(0);
}
