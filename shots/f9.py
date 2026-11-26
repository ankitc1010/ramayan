"""f9 (96): release (f0).  The arrow flies down a tunnel hung with everything the film has shown (f6-64) and strikes (f72).  White."""
from lau.shot import *
from lau.look import *
from chars import rama
from . import memories
from .f8 import BG

TUNNEL = '''
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform vec2 res,bend;uniform float fT,z0,roll,heat,end_,gap;uniform int nImg;uniform sampler2DArray tM;
const float F=1.22,HW=.90,HH=.506,B=.075;
void main(){
 vec2 p=(uv*2.-1.)*vec2(res.x/res.y,1.)-bend;p=rot(roll)*p;float r=length(p)+1e-4,a=atan(p.y,p.x);vec3 rd=vec3(p/F,1.),col=vec3(0);float T=1.;
 float first=floor((z0+.30)/gap)+1.;
 for(int i=0;i<22;i++){                                                     // near to far: pictures on a spiral, each turned a little to the path
  float k=first+float(i);if(k<0.||k>=float(nImg)||T<.01)continue;float zk=k*gap-z0;
  float th=k*2.39996+.6;vec2 dir=vec2(cos(th),sin(th));vec3 C=vec3(dir*vec2(1.42,1.04),zk);
  vec3 X=normalize(vec3(1,0,-dir.x*.55)),Y=normalize(vec3(0,1,-dir.y*.55)),N=normalize(cross(X,Y));float t=dot(C,N)/dot(rd,N);if(t<.22)continue;
  vec3 Q=rd*t-C;vec2 q=vec2(dot(Q,X),dot(Q,Y));float px=t/(F*res.y*.5),d=max(abs(q.x)-HW,abs(q.y)-HH),cov=smoothstep(px,-px,d-B);
  float halo=exp(-max(d-B,0.)/.16)*(1.-cov);
  if(cov>0.){
   float lod=log2(max(1.,px/(2.*HW)*960.));vec3 c=pow(textureLod(tM,vec3(clamp(q/vec2(2.*HW,2.*HH)+.5,0.,1.),k),lod).rgb,vec3(2.2))*1.12;
   // the painted border of a miniature: red band, gold lines, a row of gold seeds
   float b=smoothstep(-px,px,d);vec2 e=abs(q)-vec2(HW,HH);float along=e.x>e.y?q.y:q.x;vec3 band=mix(hex(0x7a0f16),hex(0x4a0712),smoothstep(0.,B,d));
   float seed=length(vec2(abs(fract(along*14.)-.5)/14.,d-B*.5));band=mix(band,hex(0xf2b64a),smoothstep(.011+px,.011-px,seed));
   float ln=min(abs(d-.006),abs(d-B+.008))-.0045;band=mix(band,hex(0xffd37a)*(.75+.35*sin(a*5.+fT*4.+zk*2.)),smoothstep(px,-px,ln));
   c=mix(c,band,b);
   float near=exp(-zk*.13);c*=mix(vec3(.30,.15,.08),vec3(1.),near);c+=hex(0xff8a30)*(1.-near)*.10*heat;c*=1.+.5*smoothstep(1.7,.6,zk);
   col+=T*cov*c;}
  T*=(1.-cov)*(1.-.62*halo);}
 // what is behind them: a dark warm well, dust of gold, and the light the arrow is going to
 float z=z0+1.2/r;vec3 bg=mix(hex(0x1c0714),hex(0x471014),fbm(vec2(a*3.,z*.9)));vec2 g=vec2(a*14.,z*5.),gi=floor(g);float dot_=smoothstep(.22,.0,length(fract(g)-.5-.5*(vec2(h21(gi),h21(gi+7.))-.5)))*step(.80,h21(gi+3.));bg+=hex(0xffb04a)*dot_*.8*smoothstep(.0,.25,r);
 bg*=.35+.65*smoothstep(0.,.9,r);col+=T*bg;
 float beam=smoothstep(.55,1.,vn(vec2(a*30.,z*.28-fT*1.6)))*smoothstep(.06,.7,r);col+=hex(0xffb870)*beam*.16;
 col*=1.-.80*end_*smoothstep(1.9,.35,r);col+=hex(0x4a0a08)*end_*smoothstep(1.4,.1,r)*.5;float g2=1.+1.6*end_;                 // the dark closes in, the point stays
 col=mix(col,hex(0xff8426),exp(-r*r*30./g2)*.85);col=mix(col,hex(0xfff2cf)*1.5,exp(-r*r*190./g2));col+=hex(0xff9a44)*exp(-r*4.2)*.34*heat;o=vec4(col,1);}
'''


class Shot(ShotBase):
    id = 'f9'; n = 96
    EVENTS = [(0, 'release', {}), (6, 'arrow tunnel', dict(dur=60)), (60, 'arrow nears', {}), (72, 'arrow strikes', {}), (80, 'white', dict(dur=16))]

    def setup(self, st):
        self.wall, self.nimg = memories.wall(st)

    def frame(self, f, st):
        st.clear('#000', f=f)
        if f < 6: return self.release(f, st, st.t)
        if f < 64: return self.tunnel(f, st, st.t)
        return self.strike(f, st, st.t)

    def release(self, f, st, t):
        cam = Cam(V(14, 7.5, 24), V(7.5, 11.6, 0), 34, roll=-9); st.cam = cam; P = PZ.archer(keys(f, [(0, 1.06), (1, .4, 'snap'), (3, .3)])).set(hedr=(72, 2, -2)); S = st.fig(rama.EXILE, P, yaw=26, draw=False); nk = S.palm('R', .22, .95, .34); g = S.palm('L', 0, .62, .30); aim = nz(g - nk)
        x, y, z = cam.project(g); st.paint(BG, sun=(float(x), float(y)), heat=1.6, silent=0.)
        L = Light(key=(.75, .3, .45), keyCol=(1.5, .85, .4), amb=(.14, .08, .12), rim=(-.6, .5, -.6), rimCol=(1.4, .5, .2), pts=[(g, 5., (1.6, .8, .3))], envT='#ffb060', envM='#d8601c', envB='#3a0f1c', ink=3.6)
        st.open(cam, L); S = st.fig(rama.EXILE, P, yaw=26, face=Face(frown=.7, squint=.2, smile=-.2, teeth=.3)); PR.bow_and_arrow(st, S, half=5.2, arrow=f < 1, release=1. if f > 0 else 0.); st.close()
        if f >= 1:
            a = g + aim * (6 + 22 * f); FX.ribbon(st, np.array([g + aim * 1., a]), np.array([.9, .25]), 'fire', (1.2, 1., .7), seed=2); FX.ribbon(st, np.array([g, a]), .30, 'light', '#ffb050', '#fff6dc'); FX.burst(st, 60, g, f / 24., speed=26, grav=0, size=.10, seed=3, spread=(1, 1, 1), life=.5)
        IM.zoomblur(st, (float(x), float(y)), .05 * f)
        if f == 1: IM.inkflash(st, '#1a0408', '#ff8a2c', '#fff6dc', lo=.25, hi=.52)
        return st.finish(bloom=.7, vig=.4, flash=.35 * (f == 2) + .12 * max(0, f - 3), flashCol='#fff0d0')

    def tunnel(self, f, st, t):
        u = (f - 6) / 58.; gap = .95; z = -1.9 + (self.nimg * gap + 1.2) * (.30 * u + .70 * u ** 1.75); roll = .16 * math.sin(u * 4.2) - .10 * u; bend = (.12 * math.sin(u * 6.) * (1 - u), .08 * math.cos(u * 5.) * (1 - u))
        fl = 1 + .10 * noise1(t * 13, 2)
        st.paint(TUNNEL, z0=float(z), roll=float(roll), heat=float(fl), end_=float(smooth(56, 64, f)), bend=bend, gap=gap, nImg=int(self.nimg), texs=dict(tM=self.wall))
        IM.zoomblur(st, (960 + bend[0] * 540, 540 - bend[1] * 540), .006 + .034 * u * u)
        # the arrow itself, seen from behind and above, with its long fire
        cam = Cam(V(.6, 2.1, 7.6), V(bend[0] * 5, .6 + bend[1] * 5, -20), 40, roll=-math.degrees(roll) * .25); st.cam = cam; bob = V(.10 * math.sin(t * 9), .08 * math.cos(t * 11), 0); tip = V(0, -.15, -3.4) + bob; aim = V(0, .0, -1.)
        L = Light(key=(0, .5, .8), keyCol=(1.0, .62, .30), amb=(.25, .12, .08), rim=(0, 1, -.6), rimCol=(1.6, .9, .4), envT='#ffc070', envM='#ff8a3a', envB='#6a1c10', pts=[(tip, 2.5, (1.4, .7, .25))], shadow=False, ink=3.0, inkRef=.5)
        st.open(cam, L); st.fig(PR.arrow_of(4.2, 1.3), M=PR.place(tip - aim * 4.2, V(math.sin(t * 7), math.cos(t * 7), 0), aim, 1.)); st.close()
        for i in range(4):
            q = np.linspace(0, 1, 34); ph = t * 12 + i * 1.57; c = tip[None] + V(0, 0, 1)[None] * (q * 7.0)[:, None]; w = (.03 + .16 * q)[:, None]; off = np.c_[np.cos(q * 9 - ph), np.sin(q * 9 - ph), np.zeros(34)] * w
            FX.ribbon(st, c + off, np.interp(q, [0, .12, .6, 1], [.02, .10, .13, .03]), 'fire', (1., .85, .6), seed=i * 4. + 1, amt=.9)
        FX.flame(st, tip + V(0, 0, 0), .8, seed=1.3, glow=.9, lean=0., calm=1.6)
        r = np.random.default_rng(4); n = 120; a = r.uniform(0, 6.28, n); rr = r.uniform(.9, 3.4, n); zz = -30 + np.mod(r.uniform(0, 31, n) + t * 46, 31); FX.particles(st, np.c_[np.cos(a) * rr, np.sin(a) * rr, zz], .035, '#ffc070', 'streak', vel=np.tile([0, 0, 1.6 + 1.6 * u], (n, 1)), alpha=.8)
        return st.finish(bloom=.55, thr=.9, vig=.5, contrast=1.08, flash=.6 * (1 - smooth(6, 9, f)), flashCol='#fff0d0')

    def strike(self, f, st, t):
        from chars import ravana as RV
        u = (f - 64) / 8.; hit = f >= 72
        cam = Cam(V(1.0, 8.6, 33 - 2.5 * min(u, 1.6)), V(0, 12.6, 0), 36, roll=-4 + 3 * min(u, 1)); st.cam = cam
        st.paint('sky.frag', **SKY(BLOOD, sunDir=(.0, .22, -1), sunR=.22, sunCol='#ff5a24', sunGlow=1.3, rays=.8, cov=.5, cy0=.0, cy1=.3))
        L = Light(key=(-.9, .25, .3), keyCol=(1.1, .55, .25), amb=(.05, .02, .05), rim=(.5, .4, -.8), rimCol=(2.0, .6, .2), envT='#ff7a3a', envM='#b8301c', envB='#2a0a14', shadow=False, ink=3.6, pts=[(V(0, 9.0, 3.), 4., (2.2, 1.2, .5))] if hit else [])
        st.open(cam, L); S = RV.fig(st, RV.R_STRUCK if hit else RV.R_EASE, fan=1., arms=1., navel=1. if hit else .25, eyeglow=.0 if hit else .5, mouths=.8 if hit else .2, face=Face(mouth=.8, sad=.5, lid=1.1) if hit else Face(frown=.9, smile=-.4, mouth=.15, teeth=.5)); RV.cape(st, S, t, wind=(-.35, .05, -1.6)); st.close()
        nav = S.pelvis((0, 1.38, 1.3))
        if not hit:
            tip = lerp(V(-44, 14, 16), nav, ease_in(u, 1.25)); d = nz(nav - V(-44, 14, 16)); FX.ribbon(st, np.array([tip - d * 26, tip - d * 12, tip]), np.array([.1, 1.3, .25]), 'fire', (1.2, 1., .7), seed=2); FX.ribbon(st, np.array([tip - d * 30, tip]), .35, 'light', '#ffb050', '#fff6dc'); FX.particles(st, tip[None], 3.0, '#ffd890', 'spark')
            k = math.exp(-(f - 64) / 2.2); x, y, _ = cam.project(nav); FX.particles(st, np.array([nav, nav]), np.array([1.4 + 11 * k, .8 + 5 * k]), '#ffe2a8', 'spark', alpha=.45 + .55 * k)          # the same light the tunnel ended on
            IM.zoomblur(st, (float(x), float(y)), .05 * k)
            return st.finish(bloom=.6 + .4 * k, vig=.5 + .25 * k, contrast=1.1)
        x, y, z = cam.project(nav); a = (f - 72) / 24.
        if f in (72, 74):                                                                  # two frames of print: the king, the line, the point of light
            FX.ribbon(st, np.array([nav - V(60, -3, -10), nav]), np.array([.2, 1.0]), 'light', '#ffffff', '#ffffff'); FX.particles(st, nav[None], 4.5, '#ffffff', 'spark'); IM.speedlines(st, (float(x), float(y)), .9, col=(.02, .01, .01), seed=f, inner=.42, dens=6); IM.inkflash(st, '#12040a', '#ff7a24', '#fff6dc', lo=.16, hi=.46, invert=f == 74)
            return st.finish(bloom=.2, vig=.2)
        FX.particles(st, nav[None], 7 + 60 * a, '#fff0c8', 'spark', alpha=1.); FX.burst(st, 160, nav, a, speed=34, grav=6, size=.22, seed=4, col='#ffd27a', kind='flake', life=1.2); FX.burst(st, 90, nav, a, speed=44, grav=0, size=.14, seed=5)
        IM.zoomblur(st, (float(x), float(y)), .06 + .5 * a); IM.shock(st, (float(x), float(y)), 60 + 2400 * a, 120, 60)
        return st.finish(bloom=.9, vig=.3, flash=smooth(74, 82, f), flashCol='#fff8e8')
