in vec2 uv; layout(location=0) out vec4 o; layout(location=1) out vec4 oz;
uniform sampler2D tex,g0,g1; uniform vec2 sres; uniform float ss;
void main(){vec4 s=vec4(0);float z=1e5;int n=int(ss+.5);vec2 base=floor(uv*sres/ss)*ss;
 for(int j=0;j<n;j++)for(int i=0;i<n;i++){ivec2 q=ivec2(base)+ivec2(i,j);vec4 c=texelFetch(tex,q,0);c.rgb=min(c.rgb,vec3(6.));s+=c;if(texelFetch(g1,q,0).w>.5) z=min(z,texelFetch(g0,q,0).w);}
 o=s/float(n*n);oz=vec4(z,0,0,1);}
