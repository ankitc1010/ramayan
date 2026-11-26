#include "noise.glsl"
in vec4 vuv;in float vz;out vec4 o;uniform sampler2D tZ;uniform float fT,seed,amt,soft;uniform int mode,space;uniform vec3 colA,colB;
// u = along 0..1, v = across -1..1, z = half width in px, w = length in widths.  mode 0 fire 1 light 2 smoke 3 ink brush 4 water/wind 5 gold thread 6 lightning core
void main(){float u=vuv.x,v=vuv.y,L=vuv.w;vec3 c=colA;float al=0.,add=0.;
 if(mode==0){float t=fT*2.2;float n=fbm(vec2(u*L*1.1-t*1.6+seed,v*1.3+seed*3.)),n2=fbm(vec2(u*L*2.6-t*3.1,v*2.8-seed));float w=(.42+.62*n)*(1.-.15*u)*smoothstep(1.,.80,u)*smoothstep(0.,.02,u);float d=abs(v)-w*(.70+.55*n2);al=smoothstep(.06,-.04,d);float h=(w-abs(v))/max(w,.05)+.35*(n2-.5)+.25*(1.-u);
  c=colA*vec3(.36,.045,.018);c=mix(c,colA*vec3(.85,.15,.03),smoothstep(.08,.16,h));c=mix(c,colA*vec3(1.1,.38,.06),smoothstep(.34,.42,h));c=mix(c,colA*vec3(1.25,.76,.18),smoothstep(.66,.74,h));c=mix(c,colA*vec3(1.4,1.2,.7),smoothstep(.98,1.06,h));add=.22;}
 else if(mode==1){float g=exp(-v*v*9.),k=exp(-v*v*90.);al=g*.55+k;c=mix(colA,colB,k);al*=smoothstep(0.,.12,u)*smoothstep(1.,.97,u);add=.9;}
 else if(mode==2){float n=fbm(vec2(u*L*.9-fT*.6+seed,v*1.1+seed));float d=abs(v)-(.35+.75*n)*smoothstep(0.,.08,u);al=smoothstep(.08,-.12,d)*smoothstep(1.,.55,u)*.85;c=mix(colB,colA,smoothstep(-.4,.6,v+n-.5));}
 else if(mode==3){float n=fbm(vec2(u*L*.35+seed,v*9.+seed*5.));float dry=smoothstep(.50,.62,n+.45*(1.-smoothstep(.15,.95,u)));float ed=abs(v)-.86+.22*fbm(vec2(u*L*2.+seed,v+3.));al=smoothstep(.05,-.04,ed)*dry*smoothstep(0.,.015,u);}
 else if(mode==4){float n=fbm(vec2(u*L*.5-fT*2.+seed,v*3.));al=smoothstep(.45,.6,n)*(1.-abs(v))*smoothstep(0.,.2,u)*smoothstep(1.,.5,u);add=.2;}
 else if(mode==5){al=smoothstep(1.,.75,abs(v));float g=smoothstep(.3,.8,sin(u*L*2.-fT*5.));c=mix(colA,colB,g);add=.15;}
 else {float k=exp(-v*v*40.),g=exp(-v*v*5.);al=k+.35*g;c=mix(colA,colB,k);add=.95;}
 if(space==0){float z=texelFetch(tZ,ivec2(gl_FragCoord.xy),0).x;al*=soft>0.?smoothstep(0.,soft,z-vz):step(vz,z+.02);}
 al*=amt;if(al<.003) discard;o=vec4(c*al,al*(1.-add));}
