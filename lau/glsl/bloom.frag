in vec2 uv; out vec4 o; uniform sampler2D tex; uniform vec2 px; uniform int mode; uniform float thr,amt;
void main(){
 if(mode==0){vec3 s=vec3(0);float w=0.;for(int j=-1;j<=1;j++)for(int i=-1;i<=1;i++){vec3 c=texture(tex,uv+vec2(i,j)*px).rgb;float l=dot(c,vec3(.2126,.7152,.0722));float k=1./(1.+l);s+=c*k;w+=k;}s/=w;float l=max(s.r,max(s.g,s.b));float b=max(0.,l-thr);b=b*b/(b+.25);o=vec4(s*b/max(l,1e-4),1);}
 else if(mode==1){vec3 s=texture(tex,uv).rgb*4.;for(int i=0;i<4;i++){vec2 d=vec2(i<2?-1:1,(i&1)==0?-1:1);s+=texture(tex,uv+d*px).rgb;}o=vec4(s/8.,1);}
 else {vec3 s=vec3(0);s+=texture(tex,uv+vec2(-1,0)*px*2.).rgb+texture(tex,uv+vec2(1,0)*px*2.).rgb+texture(tex,uv+vec2(0,1)*px*2.).rgb+texture(tex,uv+vec2(0,-1)*px*2.).rgb;s+=2.*(texture(tex,uv+px).rgb+texture(tex,uv-px).rgb+texture(tex,uv+px*vec2(1,-1)).rgb+texture(tex,uv+px*vec2(-1,1)).rgb);o=vec4(s/12.*amt,1);}
}
