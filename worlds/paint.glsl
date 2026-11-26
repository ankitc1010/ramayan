// painted walls, domes, spires, water for the places (needs place_head + arch.glsl).  pNight 0..1 lights windows and ledges
float pNight=0.;vec3 pLamp=vec3(1.15,.46,.10);                // colour of lamp light
float pLod(float size){return smoothstep(.42,.12,gPx/size);}   // 1 near, 0 when a thing of this size is a few pixels
float stepInk(float run,float rise){return smoothstep(1.5,7.,run*abs(gRd.y)/gPx)*smoothstep(1.5,5.,rise/gPx);}   // thin slivers of tread take no line
vec3 mixh(int a,int b,float t){return mix(hex(a),hex(b),t);}
// a wall: q = (along, up from the foot), W half width, H height, fh storey, bay = wanted bay width, tn = unit vector along the wall.  seed picks lit windows
void pFacade(inout Surf s,vec3 n,vec3 tn,vec2 q,float W,float H,float fh,float bay,vec3 wall,vec3 wsh,vec3 trim,float seed){
  float lod=pLod(bay*.5),lod2=pLod(fh*.12);s.base=wall;s.sh=wsh;s.ink=.8*mix(.25,1.,lod);
  float fl_=floor(q.y/fh),y=q.y-fl_*fh;float W2=W*.95,nb=max(1.,round(2.*W2/bay)),bw=2.*W2/nb,id=floor((q.x+W2)/bw),x=(fract((q.x+W2)/bw)-.5)*bw;
  bool inB=abs(q.x)<W2;vec2 hh=h22(vec2(id+fl_*17.+seed*31.,fl_+seed));
  // broad gouache variation between storeys and a foot that is warmer
  s.base*=.95+.09*vn(q*.05+seed*9.);
  float ww=min(bw*.30,fh*.22),sill=fh*.17,hs=fh*.34;
  if(inB&&lod>.01&&q.y<H-1.){
    vec2 w0=vec2(x,y-sill);oAA=gPx;float d=oArch(w0,ww,hs,3.);
    float panel=max(abs(x)-bw*.42,abs(y-fh*.47)-fh*.37);s.base=mix(s.base,mix(wall,trim,.30),oE(panel)*lod*.75);s.sh=mix(s.sh,mix(wsh,trim*.6,.3),oE(panel)*lod*.75);
    float ln=oL(panel+.0,.16)*pLod(1.6);s.base=mix(s.base,trim,ln);
    float fr=oE(abs(d-.75)-.55);s.base=mix(s.base,mix(trim,vec3(1.,.95,.85),.0),fr*lod);s.sh=mix(s.sh,trim*.55,fr*lod);
    if(d<0.){
      vec2 off=vec2(dot(gRd,tn),gRd.y)/max(-dot(gRd,n),.12)*2.2;float d2=oArch(w0+off,ww,hs,3.);float lit=step(hh.x,.62)*pNight;
      vec3 deep=mix(mix(wsh,hex(0x6a3450),.62)*.62,hex(0x3c2240),hh.y*.8);if(pNight>.3) deep=mix(deep,hex(0x1c1026),pNight*.7);vec3 c=deep;
      if(d2>0.) c=mix(wall,wsh,.65)*.62;
      else{float jal=oJaliSq((w0+off)/ (ww*.36));bool low=w0.y<hs*.55;if(low&&hh.y>.35) c=mix(deep,wall*.75,jal*pLod(1.2));else if(hh.y>.75){float cur=smoothstep(.0,.05,abs(x)-ww*.45*(.6+.4*w0.y/hs));c=mix(deep,mix(hex(0x9a2a24),hex(0x2c5a50),step(.88,hh.y)),cur);}}
      s.base=mix(s.base,c,lod);s.sh=mix(s.sh,c*.8,lod);s.part+=20.;
      if(lit>0.&&d2<0.){float g=exp(-length(w0-vec2(0,hs*.35))/(ww*1.6));bool low=w0.y<hs*.55&&hh.y>.35;float jal=oJaliSq((w0+off)/(ww*.36));vec3 e=mix(vec3(.75,.16,.02),vec3(1.55,.80,.20),smoothstep(.1,.8,g))*(.60+.55*hh.y);e+=vec3(.5,.42,.2)*smoothstep(.75,1.,g);if(low) e*=mix(1.,.16,jal*pLod(1.2));else{float mu=oE(abs(x)-.10)+oE(abs(w0.y-hs*1.02)-.12);e*=1.-.7*clamp(mu,0.,1.)*pLod(1.);}if(lit>.5){s.cls=4.;s.base=mix(s.base,e,lod);s.ink=.35;}else emit(s,e*lit*lod);}
    }
  } else if(q.y<H-1.&&lod<.5&&inB) {s.base=mix(s.base,mix(wall,hex(0x5a3a50),.22),1.-2.*lod);}
  // far windows still twinkle at night
  if(pNight>0.&&inB){float fw=step(hh.x,.62)*smoothstep(ww*1.2,ww*.5,abs(x))*step(sill,y)*step(y,sill+hs*1.6);if(fw*(1.-lod)*pNight>.45){s.cls=4.;s.base=vec3(1.0,.36,.06)*(.6+.5*hh.y);s.ink=.1;}}
  // bands under each ledge
  float by=(fh-y-2.1)/3.2;if(by>0.&&by<1.&&q.y<H){oAA=gPx/3.2;float b=oLotus(vec2(q.x/3.2,by));s.base=mix(s.base,mix(trim,wall,1.-b),pLod(3.));s.base=mix(s.base,trim*.9,oL((by-.02)*3.2,.14));s.part+=10.;s.ink*=.6;}
  if(q.y<5.&&q.y>0.){oAA=gPx/4.6;float b=oLotusFill(vec2(q.x/3.0,1.-q.y/4.6));s.base=mix(s.base,mix(trim*.8,wall,b),pLod(4.)*.8);}
  // corner pilasters
  float cp=oE(abs(abs(q.x)-W+1.4)-1.2);s.base=mix(s.base,mix(wall,vec3(1),.3),cp*lod2*.6);
  // light of the rows of lamps on the ledges, below and above
  if(pNight>0.&&s.cls<3.5){float g=exp(-y/(fh*.15))*1.0+.45*exp(-(fh-y)/(fh*.10));g*=.75+.4*sin(q.x*.70+seed);emit(s,pLamp*wall*g*.46*pNight);}
}
// lamp flames painted on an edge: u along the edge, v above it
void pLampRow(inout Surf s,vec2 u,float per,float size,float k){float id=floor(u.x/per);vec2 f=vec2((fract(u.x/per)-.5)*per,u.y);f.x+=.03*size*sin(fT*9.+id*7.);float w=size*.34*sqrt(max(0.,sin(PI*clamp(pow(clamp(f.y/size,0.,1.),.62),0.,1.))));float d=max(abs(f.x)-w,max(-f.y,f.y-size));oAA=gPx;float c=oE(d);if(c>.3&&k>.02){s.cls=4.;s.base=mix(vec3(2.2,.75,.12),vec3(2.4,2.0,1.1),smoothstep(0.,-.12*size,d))*k;s.ink=0.;}}
// onion dome: p local to the dome's foot, r radius
void pDome(inout Surf s,vec3 p,float r,vec3 c,vec3 sh,vec3 trim,float style){s.base=c;s.sh=sh;float a=atan(p.x,p.z),y=p.y/r;float lod=pLod(r*.14);s.ink=.85;
  oAA=gPx/(r*.39);float N=16.;vec2 u=vec2(a*N/TAU,(y-.30)/.34);if(u.y>0.&&u.y<1.){float b=oLotus(u);s.base=mix(s.base,trim,b*lod*.85);s.sh=mix(s.sh,trim*.55,b*lod*.85);}
  if(style<.5){float g=abs(fract(a*N/TAU)-.5);float w=.05;s.base=mix(s.base,mix(c,sh,.5),oE((abs(g-.5)-w)*TAU*length(p.xz)/N/r*2.)*.0+smoothstep(.10,.0,.5-g)*lod*.55*step(.62,y));}
  else if(style<1.5){oAA=gPx/(r*.2);float b=oDiaper(vec2(a*N*1.5/TAU,y*4.2));s.base=mix(s.base,trim,b*lod*.6*smoothstep(.62,.7,y)*smoothstep(1.35,1.2,y));}
  else {float k=step(.5,fract(a*N*.5/TAU+y*.9));s.base=mix(s.base,mix(c,trim,.45),k*lod*.7*smoothstep(.62,.7,y));}
  s.base=mix(s.base,trim,oL(y-.29,.02)*lod);s.base=mix(s.base,mix(hex(0xf0c050),c,.2),smoothstep(1.28,1.34,y)*.8);}
void pSpire(inout Surf s,vec3 p,float w,float h,vec3 c,vec3 sh,vec3 trim){s.base=c;s.sh=sh;float y=p.y/h;float lod=pLod(h*.020);float k=abs(fract(p.y/(h*.02))-.5)*2.;s.base=mix(s.base,mix(c,sh,.75),smoothstep(.55,.95,k)*lod*step(.22,y));s.sh=mix(s.sh,sh*.6,smoothstep(.55,.95,k)*lod*step(.22,y));
  float m=min(abs(p.x),abs(p.z));oAA=gPx/(w*.25);float nich=fract(p.y/(h*.06));if(y>.24&&m<w*.2){float b=oE(oPet(vec2(m/(w*.25),nich-.1),.42,.75));s.base=mix(s.base,trim,b*lod*.8);}
  if(y<.21&&y>.02){oAA=gPx;vec2 u=vec2(abs(p.x)>abs(p.z)?p.z:p.x,p.y-h*.03);float d=oArch(u,w*.34,h*.07,3.);float fr=oE(abs(d-.5)-.5);s.base=mix(s.base,trim,fr);if(d<0.){s.base=hex(0x2a1420);s.sh=hex(0x1a0c18);s.part+=20.;if(pNight>.5){s.cls=4.;s.base=pLamp*(.5+.7*exp(-length(u)/(w*.4)));s.ink=.3;}}}
  if(pNight>0.){float g=exp(-fract(y*9.)*4.)*step(y,.8);emit(s,pLamp*c*g*.30*pNight);}}
void pPlain(inout Surf s,vec3 c,vec3 sh){s.base=c;s.sh=sh;}
// stone paving with courses
void pPave(inout Surf s,vec2 q,vec2 sz,vec3 c,vec3 sh,float amt){float r=floor(q.y/sz.y);q.x+=.5*sz.x*mod(r,2.);vec2 id=floor(q/sz),f=(fract(q/sz)-.5)*sz;float h=h21(id);oAA=gPx;float e=oE(min(abs(abs(f.x)-sz.x*.5),abs(abs(f.y)-sz.y*.5))-.06)*pLod(min(sz.x,sz.y)*.5);s.base=c*(1.+.16*(h-.5)*pLod(sz.x));s.sh=sh*(1.+.2*(h-.5)*pLod(sz.x));s.base=mix(s.base,sh,e*amt);}
