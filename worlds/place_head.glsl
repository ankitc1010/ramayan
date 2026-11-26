// head of every place: the engine's world head plus the view ray, the size of a pixel, and painted light that does not need a lamp
#include "sdf.glsl"
struct Surf{vec3 base,sh,ns;float cls,ink,part,ao,glow;};
uniform vec2 res;uniform vec3 ro,keyDir;uniform mat3 CamR;uniform float fl,far,ortho,objId,fT;
uniform vec3 uAmb,uKey;                                    // ambient and key colour of the stage light (linear), set by worlds/place.py
vec3 gRd;float gT,gPx;                                      // view ray, distance, world size of one 1080p pixel at the hit
// light that a matte surface gives off by itself (lamp glow on a wall, fire light): survives the light's colours
void emit(inout Surf s,vec3 e){s.sh+=e/max(uAmb,vec3(.004));vec3 k=max(mix(vec3(dot(uKey,vec3(.2126,.7152,.0722))),uKey,.66),vec3(.004)),a=e/(.9*k),b=uKey/(9.*k);const vec3 Y=vec3(.2126,.7152,.0722);s.base+=a-b*dot(a,Y)/(1.+dot(b,Y));}
