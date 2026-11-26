in vec2 uv; out vec4 o; uniform sampler2D tex; uniform vec4 tint; uniform float srgb; uniform mat3 M; uniform float blurLod;
void main(){vec2 t=(M*vec3(uv,1)).xy;if(t.x<0.||t.y<0.||t.x>1.||t.y>1.){o=vec4(0);return;}vec4 c=blurLod>0.?textureLod(tex,t,blurLod):texture(tex,t);if(srgb>.5){vec3 k=c.rgb/max(c.a,1e-4);k=pow(max(k,0.),vec3(2.2));c.rgb=k*c.a;}o=c*vec4(tint.rgb*tint.a,tint.a);}
