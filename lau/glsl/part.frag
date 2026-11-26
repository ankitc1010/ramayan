#include "noise.glsl"
in vec2 vq;in vec4 vc;in float vz;flat in float kind,seed;out vec4 o;
uniform sampler2D tZ;uniform vec2 res;uniform float fT,soft,fogD;uniform vec3 fogC;uniform int space;
// 0 ember 1 streak 2 petal 3 leaf 4 ash 5 star glint 6 smoke puff 7 flame tongue 8 rain 9 feather 10 ring 11 hard dot 12 spark cross 13 gold leaf flake 14 drop 15 lamp point
void main(){
 vec2 q=vq;float r=length(q),al=0.;vec3 c=vc.rgb;float add=0.;int k=int(kind+.5);
 if(k==0){al=exp(-r*r*5.)*smoothstep(1.,.6,r);c=mix(c,vec3(1.2,1.1,.8),exp(-r*r*18.));add=.75;}
 else if(k==1){float w=1.-abs(q.x);float e=smoothstep(-1.,.6,q.y)*smoothstep(1.,.9,q.y);al=pow(max(w,0.),1.6)*e;add=.6;}
 else if(k==2){q.x*=1.7;float d=length(q-vec2(0,.1*q.y))-.8+.25*smoothstep(.2,.9,q.y)*abs(sin(atan(q.x,q.y)));al=smoothstep(.06,-.02,d);c*=.75+.35*smoothstep(-.8,.8,q.y)-.25*smoothstep(.06,.0,abs(q.x))*step(q.y,.5);c=mix(c,vc.rgb*.35,smoothstep(-.14,-.02,d));}
 else if(k==3){float w=.42*sin((q.y*.5+.5)*PI);float d=abs(q.x)-w;al=smoothstep(.05,-.01,d)*step(abs(q.y),1.);c=mix(c,vc.rgb*.45,smoothstep(-.10,-.0,d)+smoothstep(.05,.0,abs(q.x)));}
 else if(k==4){float n=vn(q*2.5+seed*31.);al=smoothstep(.72,.5,r+.4*(n-.5));}
 else if(k==5){al=exp(-r*r*14.)+.5*exp(-abs(q.x)*26.-abs(q.y)*4.)+.5*exp(-abs(q.y)*26.-abs(q.x)*4.);al*=smoothstep(1.,.5,r);add=.9;}
 else if(k==6){float n=fbm(q*1.6+seed*17.+vec2(0,-fT*.25));float d=r+.55*(n-.5);al=smoothstep(.82,.70,d);float sh=smoothstep(-.2,.35,dot(normalize(vec3(q,.8)),normalize(vec3(-.5,.7,.5)))+.5*(n-.5));c=mix(c*.62,c*1.08,sh);c=mix(c*.45,c,smoothstep(.80,.66,d));}
 else if(k==7){vec2 p=q;p.y=p.y*.5+.5;float t=fT*1.7+seed*13.;float n=fbm(vec2(p.x*1.8+seed*7.,p.y*1.7-t*1.5));float n2=fbm(vec2(p.x*4.2-seed*3.,p.y*3.6-t*2.7));
   p.x+=(n-.5)*1.0*p.y+.24*sin(p.y*5.-t*6.+seed*9.)*p.y;float w=.50*pow(max(1.-p.y,0.),.85)*smoothstep(-.02,.20,p.y)+.015;float d=(abs(p.x)-w*(.55+.75*n2))/max(w,.05);
   float e=smoothstep(.09,-.05,d)*step(p.y,1.);float h=-d*.85+.30*(1.-p.y)+.22*(n-.5);
   vec3 f=vc.rgb*vec3(.30,.035,.015);f=mix(f,vc.rgb*vec3(.78,.13,.025),smoothstep(.06,.14,h));f=mix(f,vc.rgb*vec3(1.05,.34,.05),smoothstep(.34,.42,h));f=mix(f,vc.rgb*vec3(1.18,.66,.13),smoothstep(.68,.76,h));f=mix(f,vc.rgb*vec3(1.3,1.06,.52),smoothstep(1.0,1.08,h));c=f;al=e*smoothstep(0.,.06,p.y);add=.16;}
 else if(k==8){al=smoothstep(1.,.0,abs(q.x))*smoothstep(-1.,-.2,q.y)*smoothstep(1.,.8,q.y);add=.2;}
 else if(k==9){float w=.26*sin((q.y*.5+.5)*PI)*(1.-.2*q.y);float b=sin((q.y*16.+abs(q.x)*30.));float d=abs(q.x)-w+.04*b;al=smoothstep(.03,-.01,d);c=mix(c,vc.rgb*.35,smoothstep(.05,.0,abs(q.x))+smoothstep(-.07,.0,d)*.8);c*=.9+.12*b;}
 else if(k==10){al=smoothstep(.12,.0,abs(r-.82))*(.6+.4*vn(vec2(atan(q.y,q.x)*6.,seed)));add=.6;}
 else if(k==11){al=smoothstep(1.,.86,r);}
 else if(k==12){float a=atan(q.y,q.x);float sp=pow(abs(cos(a*3.+seed*6.)),22.)+.6*pow(abs(cos(a*5.+seed*3.)),40.);al=smoothstep(1.,.0,r/(.22+.85*sp));al*=al;add=.9;}
 else if(k==13){float d=max(abs(q.x),abs(q.y))-.7+.3*vn(q*3.+seed*9.);al=smoothstep(.05,-.02,d);float g=smoothstep(.35,.6,sin(fT*7.+seed*40.+q.x*2.));c=mix(c*.6,c*1.9,g);add=.2*g;}
 else if(k==14){q.y*=.8;float d=length(q-vec2(0,-.2))-.55+.5*smoothstep(-.2,.9,q.y)*.9;al=smoothstep(.05,-.05,d);c=mix(c*.55,c*1.4,smoothstep(.3,.0,length(q-vec2(-.18,-.3))));}
 else{float f=exp(-r*r*26.);al=f+.30*exp(-r*r*4.)*smoothstep(1.,.5,r);c=mix(c,vec3(1.4,1.25,.9),f);add=.9;}
 al*=vc.a;
 if(space==0){float z=texelFetch(tZ,ivec2(gl_FragCoord.xy),0).x;al*=soft>0.?smoothstep(0.,soft,z-vz):step(vz,z);float fg=1.-exp(-vz*fogD);c=mix(c,fogC,fg*(1.-add));if(add>.5)al*=1.-.7*fg;}
 if(al<.002) discard;
 o=vec4(c*al,al*(1.-add));
}
