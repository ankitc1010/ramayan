// a painted ocean: heightfield plus miniature-painting line work
#ifndef SEA_IT
#define SEA_IT 5
#endif
float wv(vec2 p,float t){vec2 q=p+.55*vec2(sin(p.y*.63+t*.4),cos(p.x*.71-t*.3));vec2 w=1.-abs(sin(q));vec2 c=abs(cos(q));w=mix(w,c,w);return pow(1.-pow(w.x*w.y,.65),2.6);}
float seaH(vec2 x,float t,float amp,float fr){float h=0.,a=amp;mat2 m=mat2(1.6,1.2,-1.2,1.6);vec2 p=x*fr;p.x*=.78;for(int i=0;i<SEA_IT;i++){float d=wv(p+vec2(t*.8,t*.35),t)+wv(p*.97-vec2(t*.6,-t*.3)+3.1,t);h+=d*a;p=m*p;a*=.24;t*=1.25;}return h*.62;}
// colours the water at p with normal n: deep, mid, foam ; returns base and shadow
void seaPaint(vec3 p,vec3 n,vec3 rd,float h,float amp,float t,vec3 deep,vec3 mid,vec3 lite,vec3 foam,out vec3 base,out vec3 sh){
  float f=pow(1.-max(0.,dot(n,-rd)),4.);float hh=h/max(amp,1e-3);
  float dist=length(p.xz);
  base=mix(deep,mid,smoothstep(.15,.75,hh+.35*(fbm(p.xz*.35)-.5)));base=mix(base,lite,smoothstep(.85,1.40,hh)*.85);base=mix(base,lite,f*.6);
  float ph=h*2.6/max(amp,.05)+.35*vn(p.xz*1.3);float ln=smoothstep(.10,.03,abs(fract(ph*1.6)-.5))*smoothstep(.2,.6,hh);base=mix(base,deep*.65,ln*.45);
  float fo=smoothstep(1.22,1.34,hh+.30*(fbm(p.xz*2.2+t*.2)-.5)+.14*(vn(p.xz*7.)-.5));base=mix(base,foam,fo);sh=mix(base*vec3(.42,.46,.62),foam*vec3(.62,.70,.85),fo*.6);}
