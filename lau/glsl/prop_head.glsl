#include "sdf.glsl"
uniform vec3 Pb[24],Ps[24];uniform float Pc[24];uniform float pr[16];uniform float fT;
struct Surf{vec3 base,sh,ns;float cls,ink,part,ao,glow;};
void initRig(){}
