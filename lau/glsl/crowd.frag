in vec2 tuv;flat in float sc;flat in float fid;flat in float flp;in vec3 vt;in float vz0;in vec3 wp;
layout(location=0) out vec4 g0;layout(location=1) out vec4 g1;layout(location=2) out vec4 g2;layout(location=3) out vec4 g3;
uniform sampler2D a0,a1,a2,a3;uniform float objId,far,ortho;uniform mat3 CamR;
void main(){ivec2 q=ivec2(tuv*vec2(textureSize(a1,0)));vec4 A=texelFetch(a1,q,0);if(A.w<.5) discard;vec4 N=texelFetch(a0,q,0),S=texelFetch(a2,q,0),Q=texelFetch(a3,q,0);
 float vz=vz0+N.w*sc;gl_FragDepth=clamp(vz/far,0.,1.);vec3 fx=vec3(flp,1,1);
 float cl=floor(A.w);vec3 t=cl<1.5||cl>4.5?vt:mix(vec3(1),vt,.25);
 g0=vec4(transpose(CamR)*(N.xyz*fx),vz);g1=vec4(A.rgb*t,A.w);g2=vec4(S.rgb*t,S.w);g3=vec4(transpose(CamR)*(Q.xyz*fx),(objId+mod(fid,97.))*64.+mod(Q.w,64.));}
