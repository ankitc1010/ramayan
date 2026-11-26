// G-buffer -> inked, gold-leafed, toon-lit picture (premultiplied linear rgb + coverage)
#include "noise.glsl"
in vec2 uv; layout(location=0) out vec4 o;
uniform sampler2D g0,g1,g2,g3,tSh;
uniform vec2 res;uniform vec3 ro;uniform mat3 CamR;uniform float fl,far;
uniform vec3 keyDir,keyCol,ambCol,rimDir,rimCol,bounceDir,bounceCol,envT,envM,envB,fogCol,inkCol;
uniform vec4 fog;                   // density, start, height falloff, base height
uniform int nPt;uniform vec4 ptPos[12],ptCol[12];
uniform mat4 shM;uniform float shOn,shFar,inkW,inkRef,toonEdge,toonSoft,pig,fT,hiAmt,stip,air;
float shadowAt(vec3 P,vec3 n){
  if(shOn<.5) return 1.;
  vec4 q=shM*vec4(P+n*.26*inkRef,1);vec2 c=q.xy*.5+.5;if(c.x<.0||c.y<0.||c.x>1.||c.y>1.) return 1.;
  float s=0.;vec2 px=1./vec2(textureSize(tSh,0));
  for(int j=-2;j<=2;j++)for(int i=-2;i<=2;i++){float d=texture(tSh,c+vec2(i,j)*px*1.6).x;s+=(d<=0.||d>q.z-.34*inkRef)?1.:0.;}
  return smoothstep(.30,.70,s/25.);
}
void main(){
  vec4 N=texture(g0,uv),A=texture(g1,uv),S=texture(g2,uv),Q=texture(g3,uv);
  float ssc=res.y/1080.;vec2 px=uv*res/ssc;vec2 asp=vec2(res.x/res.y,1.);
  mat3 C=transpose(CamR);vec2 sc=(uv*2.-1.)*asp;vec3 rd=normalize(C*vec3(sc,fl));
  float cls=floor(A.w),w0=fract(A.w)/.98;vec3 col=vec3(0);float cov=0.;
  vec3 P=ro+rd*(N.w/max(dot(rd,C[2]),1e-3));
  float tx=fbm(px/6.5),tx2=fbm(px/85.+3.);
  if(cls>.5){
    cov=1.;vec3 n=N.xyz,ns=normalize(Q.xyz+1e-5);vec3 base=A.rgb,sh=S.rgb;float ao=S.w;
    float dif=dot(ns,keyDir)*.5+.5+(tx-.5)*.06*pig;
    float shd=shadowAt(P,n);
    float k=smoothstep(toonEdge-toonSoft,toonEdge+toonSoft,dif*mix(.80,1.,ao))*shd;
    vec3 kc=mix(vec3(lum(keyCol)),keyCol,.66);vec3 lit=mix(base*kc,vec3(lum(base))*keyCol,.10),dark=sh*ambCol;
    dark*=mix(.80,1.,smoothstep(.08,.42,dif));
    vec3 c=mix(dark,lit,k);
    vec3 rc=CamR*reflect(rd,n);                       // reflection in camera axes
    float fr=pow(1.-max(0.,dot(-rd,n)),3.);
    vec3 Lg=ambCol*.62+keyCol*(.25+.55*k);
    vec3 pl=vec3(0);float pk=0.;
    for(int i=0;i<nPt;i++){vec3 d=ptPos[i].xyz-P;float r=length(d);d/=r;float f=1./(1.+r*r/(ptPos[i].w*ptPos[i].w));float nl=dot(ns,d)*.5+.5;float st=smoothstep(.42,.60,nl)*.75+.25*nl;pl+=ptCol[i].rgb*f*st;pk=max(pk,f*st);}
    if(cls<1.5||cls>7.5){                              // skin, cloth, silk
      float k2=smoothstep(.78,.86,dif*ao+.03*(tx2-.5))*k;c=mix(c,mix(base,vec3(1.),.20)*keyCol*1.16,k2*hiAmt*(cls>7.5?.45:1.));
      // stippled terminator, the mural painter's shading
      float band=smoothstep(toonEdge+.16,toonEdge-.02,dif)*k;float dots=smoothstep(.36,.26,length(fract(px/5.)-.5)+.25*vn(px/9.));c=mix(c,dark,band*dots*stip);
      c=mix(c,dark,smoothstep(.46,.95,1.-abs(dot(rd,n)))*.34*air);
      c+=mix(base,vec3(lum(base))*1.25,.36)*pl;
      if(cls>7.5){float e=rc.y*.8+rc.x*.35;c+=base*keyCol*(smoothstep(.30,.42,e)-smoothstep(.50,.66,e))*.20*k;}
    } else if(cls<2.5){                                // gold leaf
      float e=rc.y*.62+rc.x*.28;float bands=smoothstep(-.35,-.25,e)*.45+smoothstep(.05,.12,e)*.60+smoothstep(.55,.62,e)*1.3;
      vec3 g=mix(hex(0x55260a),hex(0xc9862a),smoothstep(0.,.5,bands));g=mix(g,hex(0xf4cf6a),smoothstep(.5,1.05,bands));g=mix(g,hex(0xfff6cf)*1.6,smoothstep(1.3,2.2,bands));
      vec3 env=mix(envB,envM,smoothstep(-.7,.0,rc.y));env=mix(env,envT,smoothstep(.1,.8,rc.y));
      c=g*base*1.55*mix(vec3(lum(Lg)),Lg,.75)*env*mix(.55,1.,ao);
      c+=g*pl*.9; float sp=smoothstep(.93,.985,dot(reflect(rd,n),keyDir));c+=keyCol*sp*.9*shd;
      c+=g*pow(pk,2.)*smoothstep(.75,.95,max(rc.y,-rc.x))*.5;
    } else if(cls<3.5){                                // gems
      c=mix(sh,base,smoothstep(.2,.9,dif))*Lg+base*pl*1.2;vec3 r=reflect(rd,n);c+=keyCol*pow(max(0.,dot(r,keyDir)),28.)*1.4+base*.6*Lg*fr;c+=pl*pow(max(0.,dot(n,-rd)),8.)*.25;
    } else if(cls<4.5){ c=base; }                      // emissive
    else if(cls<5.5){                                  // hair and fur
      float hb=smoothstep(.10,.0,abs(dot(CamR*ns,vec3(-.25,.92,.0))-.62+.10*vn(px/7.)))*.8;c+=base*keyCol*hb*k*1.2+base*pl*1.2;
    } else if(cls<6.5){ c=base*mix(ambCol,keyCol,.55)+base*pl*.8; }   // painted cards
    else {                                             // blackened steel
      float e=rc.y*.7+rc.x*.2;float b2=smoothstep(-.2,-.1,e)*.35+smoothstep(.2,.26,e)*.5+smoothstep(.6,.66,e)*1.2;c=base*Lg*(.35+b2)+base*pl+keyCol*smoothstep(.95,.99,dot(reflect(rd,n),keyDir))*.6;}
    if(cls<3.5||cls>4.5){
      float frs=pow(1.-max(0.,dot(-rd,ns)),3.);float rim=smoothstep(.30,.50,frs*max(0.,dot(ns,rimDir)*.9+.35));c+=rimCol*rim*(cls>5.5&&cls<6.5?0.:1.)*mix(.4,1.,ao)*smoothstep(.22,.52,w0);   // floors and water (faint ink) take no rim
      if(cls<1.5||cls>4.5) c+=base*bounceCol*max(0.,dot(ns,bounceDir));
      c*=1.-.07*pig+.14*pig*tx2+.07*pig*(tx-.5);
    }
    col=c;
  }
  // ---- ink
  float rmax=inkW*ssc*(.72+.56*fbm(px/70.+Q.w*.37));
  float ink=0.;float mz=1e6;
  for(int i=0;i<14;i++){float an=(float(i)+.5*h21(px))*.4488;vec2 dir=vec2(cos(an),sin(an));
    for(int j=1;j<=3;j++){float r=rmax*float(j)/3.;vec2 u2=uv+dir*r/res;
      vec4 N2=texture(g0,u2),A2=texture(g1,u2),Q2=texture(g3,u2);float c2=floor(A2.w);if(c2<.5&&cls<.5) continue;
      float w2=fract(A2.w)/.98;bool sameId=abs(Q2.w-Q.w)<.4;float e=0.,lim=1.;
      float za=cls>.5?N.w:1e6,zb=c2>.5?N2.w:1e6;float near=min(za,zb);
      if(!sameId||(c2<.5)!=(cls<.5)){bool obj=abs(floor(Q2.w/64.)-floor(Q.w/64.))>.5||c2<.5||cls<.5;e=za<zb?w0:w2;lim=obj?1.:.72;}
      else{vec2 s2=(u2*2.-1.)*asp;vec3 r2=normalize(C*vec3(s2,fl));vec3 P2=ro+r2*(N2.w/max(dot(r2,C[2]),1e-3));float dp=abs(dot(P2-P,N.xyz));float th=.16*inkRef;e=smoothstep(th,th*1.8,dp)*w0;lim=.80;float dn=1.-dot(N2.xyz,N.xyz);float cr=smoothstep(.42,.95,dn)*w0*.85;if(cr>e){e=cr;lim=.58;}}
      float wz=clamp(inkRef*14./near,.22,1.25);                    // far things get thinner lines
      float fall=smoothstep(lim*wz,lim*wz*.62,float(j)/3.-.16);
      if(e*fall>ink){ink=e*fall;} mz=min(mz,near);
    }}
  ink=smoothstep(.12,.70,ink);
  float fogA=0.;
  if(cls>.5||ink>.0){float z=min(cls>.5?N.w:1e6,ink>0.?mz:1e6);float yy=P.y;fogA=1.-exp(-max(0.,z-fog.y)*fog.x*exp(-max(0.,(cls>.5?yy:0.)-fog.w)*fog.z));}
  vec3 ic=mix(inkCol,fogCol,fogA*.85);
  col=mix(col,fogCol,fogA*step(.5,cls)*(cls>3.5&&cls<4.5?.4:1.));
  if(cls>3.5&&cls<4.5) ink*=.0+w0;
  o=vec4(mix(col*cov,ic,ink),max(cov,ink));
}
