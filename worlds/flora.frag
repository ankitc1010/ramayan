// painted cards: flat class 6, own ink, colour gradient from foot to crown, haze toward a colour
in vec2 vuv;in vec3 wp;flat in vec4 vt;in float hy;flat in float fid;
layout(location=0) out vec4 g0;layout(location=1) out vec4 g1;layout(location=2) out vec4 g2;layout(location=3) out vec4 g3;
uniform sampler2D tCard;uniform vec3 ro,hazeCol,footCol;uniform mat3 CamR;uniform float far,objId,cutoff,cls,foot,ortho,inkw;
void main(){vec4 t=texture(tCard,vuv);if(t.a<cutoff) discard;vec3 f=transpose(CamR)[2];float vz=dot(wp-ro,f);if(vz<.2) discard;gl_FragDepth=clamp(vz/far,0.,1.);
 vec3 c=pow(t.rgb/max(t.a,.01),vec3(2.2))*vt.rgb;c=mix(c,footCol,foot*smoothstep(.45,0.,hy));c=mix(c,hazeCol,vt.a);vec3 n=normalize(ro-wp);
 g0=vec4(n,vz);g1=vec4(c,cls+inkw*.98);g2=vec4(c*.5,1);g3=vec4(n,objId*64.+mod(fid,60.));}
