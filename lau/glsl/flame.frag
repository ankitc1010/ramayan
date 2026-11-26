// one lamp flame, drawn large: pixel position of the wick, height and width in pixels
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform vec2 res,base;uniform float ht,wd,lean,fT,seed,amt,glow,calm;uniform vec3 tint;
void main(){vec2 p=vec2(uv.x*res.x,(1.-uv.y)*res.y)-base;p.y=-p.y;vec2 q=vec2(p.x/wd,p.y/ht);
 float t=fT;float sway=(.06*sin(t*3.1+seed)+.05*sin(t*7.7+seed*2.)+.10*(vn(vec2(t*2.3,seed))-.5))*calm;float fl=1.+(.10*sin(t*9.3+seed)+.14*(vn(vec2(t*6.,seed+4.))-.5))*calm;q.y/=fl;
 q.x-=(lean+sway)*q.y*q.y+.05*calm*sin(q.y*7.-t*11.+seed)*smoothstep(.2,1.,q.y);
 float y=q.y;float w=0.;if(y>-.08&&y<1.){float s=(y+.08)/1.08;w=.5*pow(s,.46)*pow(1.-s,.86)*1.46;}
 float d=abs(q.x)-w;float in_=step(-.08,y)*step(y,1.);float body=smoothstep(.026,-.026,d)*in_;
 float h=clamp(-d/max(w,.02),0.,1.);
 vec3 c=mix(hex(0xc8280a),hex(0xff7a14),smoothstep(.0,.22,h));c=mix(c,hex(0xffb83a),smoothstep(.18,.42,h));c=mix(c,hex(0xffe08a),smoothstep(.40,.72,h)*smoothstep(1.02,.5,y));c=mix(c,hex(0xfff3cc)*1.18,smoothstep(.62,.98,h)*smoothstep(-.02,.30,y)*smoothstep(.86,.42,y));
 float low=smoothstep(.20,-.05,y);c=mix(c,hex(0x2c44b0)*.9,low*.80);c=mix(c,hex(0x2a120c),smoothstep(.13,.02,length((q-vec2(0,.06))*vec2(2.0,1.)))*.6);
 vec2 g=p-vec2(0,ht*.45);float r=length(g/vec2(1.,1.2));float gl=exp(-r*r/(ht*ht*.55))*.40+exp(-r/(ht*1.35))*.20;
 vec3 gc=hex(0xff8a2c)*gl*glow*(.92+.08*fl);
 o=vec4((c*body*1.06*tint+gc*tint*(1.-body*.6))*amt,body*amt*.97);}
