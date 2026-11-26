// painted skies: gradient, sun with mural rays, scalloped clouds with contour ink, stars
#include "noise.glsl"
float F1(vec2 p){vec2 n=floor(p),f=fract(p);float d=9.;for(int j=-1;j<=1;j++)for(int i=-1;i<=1;i++){vec2 g=vec2(i,j),o=h22(n+g)*.8+.1;vec2 r=g+o-f;d=min(d,dot(r,r));}return sqrt(d);}
float puff(vec2 p){return (1.-F1(p))*.56+(1.-F1(p*2.13+3.7))*.28+(1.-F1(p*4.37+9.1))*.16;}
// mural clouds: a scalloped bank (union of discs) with the painter's concentric contour lines.  p in radians; cov 0..1 fills the band y0..y1; sc = how small the scallops are
float cloudTop(float x,float seed,float cov,float y0,float y1,float sc){float a=fbm(vec2(x*.50*sc+seed*1.7,seed*3.1)),b=fbm(vec2(x*1.9*sc+seed,seed*.7));return y0+(y1-y0)*smoothstep(.80-cov*.72,1.0-cov*.40,a*.78+b*.36);}
float smin2(float a,float b,float k){float h=max(k-abs(a-b),0.)/k;return min(a,b)-h*h*k*.25;}
float cloudSDF(vec2 p,float seed,float cov,float y0,float y1,float sc,out float tp){
  float cs=.120/sc;float xi=floor(p.x/cs);float d=1e3;tp=y0;float wsum=0.;
  for(int i=-2;i<=2;i++){float id=xi+float(i);vec2 h=h22(vec2(id,seed*7.3));vec2 g=h22(vec2(id+.5,seed*3.1));float cx=(id+.5+(h.x-.5)*.5)*cs;
    float top=cloudTop(cx,seed,cov,y0,y1,sc);float w=exp(-pow((p.x-cx)/cs,2.)*1.6);tp+=w*(top-y0);wsum+=w;if(top<y0+cs*.30) continue;
    float ht=top-y0;float r1=cs*(.36+.34*h.y);r1=min(r1,ht*.8+cs*.1);
    d=min(d,length(p-vec2(cx,top-r1))-r1);
    d=min(d,length(p-vec2(cx+cs*(.52*(g.x-.5)+.30),top-r1*1.75))-r1*(.72+.3*g.y));
    d=min(d,length(p-vec2(cx-cs*.36,top-r1*2.0-cs*.1*g.y))-r1*(.80+.25*g.x));
}
  tp=y0+(tp-y0)/max(wsum,.2);
  float cur=max(p.y-(tp-cs*.62),y0+cs*.34-tp);d=smin2(d,cur*.8,cs*.22);
  float bt=y0-p.y+.10*cs*sin(p.x/cs*2.3+seed)+.05*cs*sin(p.x/cs*5.1);return max(d,bt);}
vec3 cloudLayer(vec3 c,vec2 p,float seed,float cov,float y0,float y1,float sc,vec2 sun,vec3 lit,vec3 mid,vec3 sh,vec3 ink,float ik){
  float cs=.120/sc;if(p.y<y0-cs*.4||p.y>y1+cs*1.2) return c;
  vec2 wp=p+(vec2(vn(p*sc*30.+seed),vn(p*sc*30.+7.))-.5)*.010/sc+(vec2(vn(p*sc*95.),vn(p*sc*95.+7.))-.5)*.0035/sc;
  float tp;float d=cloudSDF(wp,seed,cov,y0,y1,sc,tp);float aa=.0011;if(d>aa*4.) return c;
  vec2 s=normalize(sun-p+1e-4);float e=.006/sc;float t2;float dl=cloudSDF(wp+s*.022/sc,seed,cov,y0,y1,sc,t2);float ds=cloudSDF(wp+vec2(0,.05)/sc,seed,cov,y0,y1,sc,t2);
  float near=exp(-length(sun-p)*1.35);
  float u=-d*sc;                                               // depth inside, in scallop units
  float hy=smoothstep(y0-.02,tp,p.y);
  float tone=hy*.95+.16*(fbm(p*sc*vec2(9.,14.)+seed)-.5)+near*.22;
  vec3 q=mix(sh,mid,smoothstep(.12,.55,tone));q=mix(q,lit,smoothstep(.52,.95,tone));
  q=mix(q,lit*1.06,smoothstep(.030,.004,u)*smoothstep(-.2,.6,hy)*.75);                  // light along the rim
  float facing=smoothstep(.000,.018,dl-d)  ;q=mix(q,lit*1.12,facing*smoothstep(.034,.012,u)*(.35+.65*near));
  q=mix(q,mix(sh,mid,.35),smoothstep(.0,.05,ds-d<0.?0.:0.)*.0);
  float pr=.55+.45*smoothstep(.25,.65,vn(p*sc*22.+seed));
  float l1=smoothstep(.0036,.0012,abs(u-.016))*.62,l2=smoothstep(.0032,.0010,abs(u-.034))*.48,l3=smoothstep(.0030,.0009,abs(u-.058))*.34,l4=smoothstep(.0028,.0008,abs(u-.090))*.22;
  q=mix(q,ink,(l1+l2+l3+l4)*ik*pr*smoothstep(cs*1.9,cs*.5,tp-p.y));
  q*=.95+.09*fbm(p*sc*34.);
  float line=smoothstep(.0052,.0020,abs(u-.0018)/1.);
  float foot=smoothstep(y0-.01,y0+cs*.75,p.y+cs*.35*(fbm(p*sc*vec2(5.,18.)+seed)-.5));
  float a=smoothstep(aa,-aa,d)*foot;
  c=mix(c,q,a);return mix(c,ink,line*ik*pr*foot*.85);}
vec3 stars(vec3 c,vec2 p,float amt,float t){vec2 g=p*46.;vec2 i=floor(g);vec2 h=h22(i);float k=step(.80,h21(i+7.));float r=length(fract(g)-.15-.7*h);float s=k*smoothstep(.09*(.4+h.x),.0,r)*(.65+.35*sin(t*2.+h.y*40.));return c+s*amt*mix(vec3(1.,.86,.6),vec3(.8,.9,1.),h.x);}
vec2 skyUV(vec3 d){return vec2(atan(d.x,-d.z),asin(clamp(d.y,-1.,1.)));}
