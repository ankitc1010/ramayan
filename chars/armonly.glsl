// one arm and hand, for inserts.  side 0 left, 1 right ; band 0 none 1 gold bangles 2 beads
uniform int side,band;uniform float old,fur,fore;uniform vec3 furB,furS;
vec2 map(vec3 p){
  vec3 a=side==0?J[4]:J[7],b=side==0?J[5]:J[8],c=side==0?J[6]:J[9];
  float fa;if(fore>.5){vec3 e=mix(b,c,.30);fa=smin(sCone(p,b,e,.30*B[5],.375*B[5]),sCone(p,e,c,.375*B[5],.205*B[5]),.14);}else fa=armD(p,a,b,c,B[5]);float d=smin(fa,handD(p,side),.10);vec2 m=vec2(d,1.);
  vec3 v=normalize(c-b);
  if(band==1){for(int i=0;i<3;i++)m=U(m,vec2(ringD(p,mix(b,c,.78+.065*float(i)),v,.245*B[5],.035,.04),3.));}
  if(band==2)m=U(m,vec2(ringD(p,mix(b,c,.88),v,.235*B[5],.07,.035),9.));
  return m;}
void surf(vec3 p,vec3 n,int m,inout Surf s){
  if(m!=1) return;
  vec3 w=side==0?J[6]:J[9];mat3 M=side==0?BL:BR;vec3 l=M*(p-w)/B[7];
  if(fur>.5){float e=l.y+.30+.16*fbm(l.xz*6.+l.y*2.)+.5*smoothstep(.0,.25,-l.z)*(-.62);float f=smoothstep(.02,-.06,e);vec3 c3=normalize((side==0?J[6]:J[9])-(side==0?J[5]:J[8]));float u=dot(p-w,c3),a=atan(l.x,l.z);float st=smoothstep(.50,.68,vn(vec2(a*16.+.6*vn(vec2(u*4.,a*3.)),u*3.2)));vec3 fb=mix(furB,furB*.62,st*.8);s.base=mix(s.base,fb,f);s.sh=mix(s.sh,furS,f);if(f>.5){s.ink=.9;return;}}
  // palm lines and knuckle creases
  float k=0.;
  if(l.z>.05&&l.y>-.1&&l.y<1.){k=max(k,lineA(l.y-.62-.22*l.x+.10*sin(l.x*5.),.018)*step(abs(l.x),.28));k=max(k,lineA(l.y-.46+.30*l.x,.016)*step(abs(l.x),.24)*.8);k=max(k,lineA(length(l.xy-vec2(.36,.22))-.30,.018)*step(.05,l.y)*.9);}
  if(l.z<-.05){for(int i=0;i<4;i++){vec2 q=l.xy-vec2(-.26+.17*float(i),.80);k=max(k,lineA(length(q*vec2(1.,1.5))-.06,.014)*step(q.y,.02)*.7);}}
  if(l.y>.82){float u=fract((l.y-.82)*2.6);k=max(k,smoothstep(.06,.0,abs(u-.5))*.35*(.6+old));}
  if(old>.0){float wr=fbm(l.xy*vec2(9.,26.)+l.z*7.);k=max(k,smoothstep(.56,.66,wr)*.55*old);k=max(k,smoothstep(.05,.0,abs(sin(l.x*11.+2.*vn(l.xy*3.))))*step(l.z,-.05)*step(l.y,.8)*.35*old);}
  vec3 nail=vec3(0);for(int f=0;f<5;f++){vec4 t=HF[side*20+f*4+3],t2=HF[side*20+f*4+2];vec3 ax=normalize(t.xyz-t2.xyz),o=p-t.xyz;vec3 bk=-normalize(transpose(M)[2]);float e=length(vec3(dot(o,ax)*.8-.015,0,length(o-ax*dot(o,ax)-bk*dot(o,bk))));if(dot(o,bk)>.012&&e<t.w*.85){s.base=mix(s.base,s.base*1.18+vec3(.06,.03,.03),.8);k=max(k,smoothstep(.16,.02,abs(e/(t.w*.85)-.95))*.5);}}
  s.base=mix(s.base,s.sh*.45,k);s.sh=mix(s.sh,s.sh*.4,k);}
