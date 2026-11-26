// painted ornament.  Every function: coverage 0..1 at uv.  Borders: x runs along the band (one motif per unit), y 0..1 across it.  Fields: one motif per unit square.  Medallions: centred, radius 1.
// Set oAA (size of a pixel in the same units) before calling; when the motif is smaller than a few pixels it fades to its mean tone, so nothing shimmers.
float oAA=.01;
float oE(float d){return smoothstep(oAA*.75,-oAA*.75,d);}                                  // edge of a signed distance (inside < 0)
float oL(float d,float w){return oE(abs(d)-w);}                                            // a line of half width w
float oF(float c,float mean){return mix(c,mean,smoothstep(.10,.34,oAA));}                  // level of detail
float oPet(vec2 p,float w,float h){p.x=abs(p.x);float y=p.y/h;float b=w*sqrt(max(0.,sin(PI*clamp(pow(clamp(y,0.,1.),.82),0.,1.))))*(1.-.18*y);return max(p.x-b,max(-p.y,p.y-h));}   // upright petal, foot at 0
float oEll(vec2 p,vec2 r){float k=length(p/r);return (k-1.)*min(r.x,r.y);}
float oSpiral(vec2 p,float r,float w){float a=atan(p.y,p.x),l=length(p);float k=fract(a/TAU-l/r*1.6+.25)-.5;return max(abs(k)*r*.62-w*(1.-.35*l/r),l-r);}
// ---- bands
float oLotus(vec2 u){float i=floor(u.x);vec2 f=vec2(fract(u.x)-.5,u.y);float d=oPet(f,.40,.92);vec2 g=vec2(fract(u.x+.5)-.5,u.y);float b=oPet(g,.30,.70);float c=oE(d)-oE(oPet(f-vec2(0,.10),.25,.66))*.0;
 float line=oL(d,.035),in_=oE(oPet(f-vec2(0,.06),.22,.62));float back=oL(b,.03)*(1.-oE(d));float vein=oE(abs(f.x)-.016)*in_*step(u.y,.56);
 return oF(clamp(line+back+in_*.75-vein,0.,1.)*step(0.,u.y)*step(u.y,1.),.45);}
float oLotusFill(vec2 u){vec2 f=vec2(fract(u.x)-.5,u.y);return oF(oE(oPet(f,.42,.95)),.6);}
float oBead(vec2 u){vec2 f=vec2(fract(u.x)-.5,u.y-.5);return oF(oE(length(f)-.34),.36);}
float oWave(vec2 u){float y=.5+.26*sin(u.x*TAU);float d=abs(u.y-y)-.07;vec2 f=vec2(fract(u.x)-.25,u.y-.36),g=vec2(fract(u.x)-.75,u.y-.64);return oF(clamp(oE(d)+oE(length(f)-.11)+oE(length(g)-.11),0.,1.),.32);}
float oVine(vec2 u){float x=u.x*.5;float s=sin(x*TAU);float y=.5+.24*s;float st=oE(abs(u.y-y)/sqrt(1.+pow(.75*cos(x*TAU),2.))-.035);float k=fract(x)-.5,sg=k<0.?1.:-1.;vec2 c=vec2((abs(k)-.25)*2.,(u.y-.5)*sg+.18);
 float sp=oE(oSpiral(c*vec2(1.,1.)*rot(.6),.26,.030));float fl=0.;vec2 q=c;float a=atan(q.y,q.x),l=length(q);fl=oE(l-.105*(1.+.35*cos(a*5.)));
 float lf=0.;for(int i=0;i<2;i++){float o=float(i)*2.-1.;vec2 b=c-vec2(o*.34,.16);b=rot(o*.9+.2)*b;lf=max(lf,oE(oPet(b+vec2(0,.13),.075,.26)));}
 return oF(clamp(st+sp+fl+lf,0.,1.),.34);}
float oKey(vec2 u){vec2 f=vec2(fract(u.x),u.y);float d=min(max(abs(f.x-.5)-.36,abs(f.y-.5)-.36),9.);float c=oL(d,.05)+oL(max(abs(f.x-.5)-.18,abs(f.y-.5)-.18),.05);return oF(clamp(c,0.,1.),.35);}
float oMerlon(vec2 u){vec2 f=vec2(fract(u.x)-.5,u.y);float w=.40;float d=max(abs(f.x)-w,f.y-.50);float t=length(vec2(abs(f.x)+.18,f.y-.5))-.585;d=min(d,max(t,.5-f.y));return oE(max(d,-f.y));}
float oRope(vec2 u){float k=fract(u.x+u.y*.8)-.5;return oF(oE(abs(k)-.3)*oE(abs(u.y-.5)-.42),.5);}
float oLeafBand(vec2 u){float i=floor(u.x);vec2 f=vec2(fract(u.x)-.5,u.y-.5);f=rot(.75)*f;float d=oEll(f,vec2(.17,.46));return oF(oE(d)-.8*oE(max(d+.05,abs(f.x)-.02)),.4);}
// ---- fields
float oDiaper(vec2 u){vec2 f=fract(u)-.5;float a=atan(f.y,f.x),l=length(f);float q=oE(l-.30*(.42+.58*abs(cos(a*2.))));vec2 g=fract(u+.5)-.5;float b=oE(length(g)-.075);float x=oE(abs(abs(f.x)+abs(f.y)-.5)-.022);return oF(clamp(q-oE(l-.06)+b+x*.9,0.,1.),.28);}
float oButa(vec2 u){u.x+=.5*mod(floor(u.y),2.);vec2 f=fract(u)-.5;float a=0.;f.y+=.04;vec2 p=f;p.x-=.16*smoothstep(.05,.35,f.y)*1.;float r=.23*smoothstep(.42,-.12,p.y);float d=max(length(vec2(p.x,min(p.y+.06,0.)))-.22,-9.);d=min(length(p+vec2(0,.10))-.20,max(abs(p.x)-r*.86,max(-.10-p.y,p.y-.36)));
 float c=oL(d,.022)+oE(d+.075);vec2 q=p+vec2(0,.11);float at=atan(q.y,q.x);c-=oE(length(q)-.075*(1.+.3*cos(at*6.)));return oF(clamp(c,0.,1.),.22);}
float oFlorets(vec2 u){u.x+=.5*mod(floor(u.y),2.);vec2 f=fract(u)-.5;float a=atan(f.y,f.x);float l=length(f);return oF(clamp(oE(l-.22*(.65+.35*cos(a*6.)))-oE(l-.06)+oE(abs(f.x)-.018)*step(f.y,-.1)*step(-.46,f.y),0.,1.),.18);}
// lattices: 1 = stone, 0 = hole
float oJali(vec2 u){vec2 r=vec2(1,1.7320508);vec2 a=mod(u,r)-r*.5,b=mod(u-r*.5,r)-r*.5;vec2 g=dot(a,a)<dot(b,b)?a:b;vec2 q=abs(g);float h=max(q.x,dot(q,vec2(.5,.8660254)));float s=max(min(h-.30,9.),-1.);float an=atan(g.y,g.x);float st=length(g)-.335*(1.-.13*cos(an*6.));return oF(1.-oE(st)+.0*s,.62);}
float oJaliSq(vec2 u){vec2 f=fract(u)-.5;float d=max(abs(f.x),abs(f.y))-.32;float e=(abs(f.x)+abs(f.y))-.46;float st=min(d,9.);st=max(d,e);vec2 g=fract(u+.5)-.5;float k=abs(g.x)+abs(g.y)-.13;return oF(clamp(1.-oE(st)-oE(k),0.,1.),.55);}
float oScale(vec2 u){float r=floor(u.y);u.x+=.5*mod(r,2.);vec2 f=vec2(fract(u.x)-.5,fract(u.y));float d=length(f-vec2(0,0.))-.5;float c=oL(d+.02,.045);f.y-=1.;vec2 g=vec2(fract(u.x+.5)-.5,f.y);return oF(clamp(c+oL(length(g)-.48,.045)*step(d,-.0),0.,1.),.3);}
// woven water of the miniatures: basket arcs
float oWater(vec2 u){float s=0.;for(int i=0;i<2;i++){vec2 v=u+float(i)*vec2(.5,.31);vec2 f=vec2(fract(v.x)-.5,fract(v.y));float a=abs(f.y-.30-.30*cos(f.x*PI));s+=oE(a-.05*(1.-1.6*abs(f.x)));}return oF(clamp(s,0.,1.),.16);}
// ---- medallions
float oLotusM(vec2 p){float l=length(p),a=atan(p.y,p.x);float c=0.;for(int i=0;i<3;i++){float n=i==0?16.:i==1?12.:8.;float R=i==0?1.:i==1?.72:.44;float k=abs(fract(a*n/TAU+(i==1?.5:0.))-.5)*2.;float ed=R*(1.-.22*pow(k,1.6));float d=l-ed;float v=i==0?.55:i==1?.8:.62;c=mix(c,v,oE(d));c=mix(c,1.,oL(d+.012,.018));c=mix(c,.2,oE(abs(k-1.)*l*PI/n-.010)*oE(d)*step(R*.45,l));}
 c=mix(c,1.,oE(l-.17));c=mix(c,.25,oL(l-.17,.02));return c*oE(l-1.);}
float oSun(vec2 p){float l=length(p),a=atan(p.y,p.x);float r=abs(fract(a*16./TAU)-.5)*2.;float d=l-mix(1.,.66,r);float w=abs(fract(a*16./TAU+.5)-.5)*2.;float d2=l-mix(.86,.62,w);float c=oE(min(d,d2));c-=oL(l-.60,.025);c-=oL(l-.50,.015);float m=oE(length(p-vec2(0,.02))-.40)*0.;return clamp(c-m,0.,1.);}
float oWheel(vec2 p){float l=length(p),a=atan(p.y,p.x);float c=oE(abs(l-.88)-.10)+oE(l-.20)-oE(l-.07);float k=abs(fract(a*12./TAU)-.5)*TAU/12.*l;float sp=oE(k-.035-.05*smoothstep(.25,.8,l)*smoothstep(.8,.6,l))*step(.18,l)*step(l,.82);float b=oE(length(vec2((fract(a*24./TAU)-.5)*TAU/24.*.88,l-.88))-.045);return clamp(max(c,sp)-b,0.,1.);}
float oConch(vec2 p){p=rot(.38)*p;float y=p.y;float wb=.50*pow(max(0.,1.-pow(max(0.,(.18-y)/1.12),1.25)),.75);float b=y<.18?abs(p.x+.06*(.18-y))-wb:length(vec2(p.x,(y-.18)*1.25))-.50;b=max(b,-.94-y);float k=clamp((y-.42)/.48,0.,1.);float sp=max(abs(p.x+.02)-.30*(1.-k)*(1.+.14*abs(sin(k*9.4))),max(.40-y,y-.90));float d=min(b,sp);float c=oE(d);
 float sl=abs(p.x-.10-.16*sin((y+.75)*1.9))-.020-.035*smoothstep(-.8,.0,y);c-=.85*oE(max(sl,abs(y+.30)-.46));for(int i=0;i<3;i++){float r=.30+.0*float(i);float yy=.44-.17*float(i);c-=.8*oE(abs(y-yy-.13*(1.-p.x*p.x*5.))-.014)*c*step(abs(p.x),.47);}c-=.8*oE(length(p-vec2(-.16,-.12))-.035);return clamp(c,0.,1.);}
float oEyeM(vec2 p){float d=max(length(p-vec2(0,.55))-.95,length(p+vec2(0,.55))-.95);return clamp(oL(d,.04)+oE(length(p)-.26)-oE(length(p-vec2(.06,.07))-.06),0.,1.);}
// ---- 2-D architecture (signed distances): opening of half width w, springing at height hs, n lobes a side; foot at y = 0
float oArch(vec2 p,float w,float hs,float n){p.x=abs(p.x);float R=w*1.34;vec2 c=vec2(w-R,hs);vec2 q=p-c;float amax=acos(clamp((R-w)/R,-1.,1.));float a=atan(q.y,q.x);float lob=w*.105*(1.-abs(sin(n*PI*clamp(a/amax,0.,1.))));float d=p.y<hs?p.x-w+w*.105*smoothstep(hs-w*.2,hs,p.y):length(q)-R+lob;d=max(d,-p.y);float og=p.x-.16*w*pow(clamp((hs+w*1.16-p.y)/(w*.36),0.,1.),1.6);og=max(og,max(p.y-hs-w*1.16,hs+w*.6-p.y));return min(d,og);}
float oArchR(vec2 p,float w,float hs){p.x=abs(p.x);float d=p.y<hs?p.x-w:length(p-vec2(0,hs))-w;return max(d,-p.y);}
