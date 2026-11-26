// a string of flowers through up to 64 points; even and odd flowers differ; pr[0] = flower radius, pr[1] = count
uniform vec3 G[64];
float flower(vec3 p,vec3 ax,float r,float ph){float y=dot(p,ax);vec3 o=p-ax*y;float l=length(o);vec3 u=normalize(cross(ax,vec3(.31,.95,.12))),v=cross(ax,u);float a=atan(dot(o,u),dot(o,v));
  float pet=.16*abs(sin(a*5.+ph+floor(y/r*2.2+3.)*1.3));return length(vec3(l*.96,y*1.25,0.))-r*(.80+pet*smoothstep(0.,.6,l/r));}
vec2 map(vec3 p){int n=int(pr[1]+.5);float best=1e3;int bi=0;for(int i=0;i<n;i++){float d=dot(p-G[i],p-G[i]);if(d<best){best=d;bi=i;}}
  float d=1e3;float id=0.;for(int k=-1;k<=1;k++){int i=clamp(bi+k,0,n-1);vec3 ax=normalize(G[min(i+1,n-1)]-G[max(i-1,0)]+1e-4);float f=flower(p-G[i],ax,pr[0],float(i)*1.7);if(f<d){d=f;id=float(i);}}
  return vec2(d*.7,11.+mod(id,2.)+(mod(id,9.)>7.5?2.-mod(id,2.):0.));}
void surf(vec3 p,vec3 n,int m,inout Surf s){s.part=float(m);s.ink=.8;float k=smoothstep(.25,.75,vn3(p*9.));s.base*=.86+.26*k;}
