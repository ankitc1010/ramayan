#include "human.glsl"
uniform vec3 Pb[24],Ps[24];uniform float Pc[24];   // palette: base, shadow, class per material
uniform sampler2D tFace;                           // painted face, front projection
uniform vec4 faceBox;                              // x0,y0,x1,y1 of the decal in head space
struct Surf{vec3 base,sh,ns;float cls,ink,part,ao,glow;};
// classes: 1 matte 2 gold 3 gem 4 emissive 5 hair 6 flat painted 7 dark metal 8 silk
vec4 faceDecal(vec3 h){vec2 t=(h.xy-faceBox.xy)/(faceBox.zw-faceBox.xy);if(t.x<0.||t.y<0.||t.x>1.||t.y>1.) return vec4(0);vec4 d=texture(tFace,t);d.rgb=pow(d.rgb/max(d.a,.003),vec3(2.2));return d;}
