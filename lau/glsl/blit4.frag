in vec2 uv;layout(location=0) out vec4 a0;layout(location=1) out vec4 a1;layout(location=2) out vec4 a2;layout(location=3) out vec4 a3;
uniform sampler2D g0,g1,g2,g3;uniform vec2 tile;uniform float dist;
void main(){ivec2 q=ivec2(uv*tile);vec4 n=texelFetch(g0,q,0);a1=texelFetch(g1,q,0);a0=vec4(n.xyz,a1.w>.5?n.w-dist:0.);a2=texelFetch(g2,q,0);a3=texelFetch(g3,q,0);}
