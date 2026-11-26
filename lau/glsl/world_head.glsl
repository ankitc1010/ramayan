#include "sdf.glsl"
struct Surf{vec3 base,sh,ns;float cls,ink,part,ao,glow;};
uniform float fT;uniform vec3 keyDir,ro;uniform mat3 CamR;   // ro = eye, CamR rows = right, up, forward
