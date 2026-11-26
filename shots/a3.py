"""a3 (72): through the weave of the cloth into the flame (f0-24); its core becomes the rising sun (f24) and Ayodhya opens in full colour; crane up over the city."""
from lau.shot import *
from lau.look import *
from worlds import ayodhya as AY

IN = '''
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform vec2 res;uniform float fT,zoom,u;
void main(){vec2 p=vec2(uv.x*res.x,(1.-uv.y)*res.y)-res*.5;p.y=-p.y;vec2 q=p/zoom;                    // px at the scale a2 ended on
 float ht=390.;vec2 f=vec2(q.x/(ht*.37),(q.y+ht*.46)/ht);float sway=.05*sin(fT*3.1)+.05*(vn(vec2(fT*2.3,1.))-.5);f.x-=sway*f.y*f.y;
 float s=clamp((f.y+.08)/1.08,0.,1.),w=.80*pow(s,.50)*pow(1.-s,.92);float lick=(fbm(vec2(f.y*2.6-fT*1.9,3.+fT*.4))-.5)*.22*s*s;float d=abs(f.x-lick)-w*(1.+.16*(fbm(vec2(f.y*5.-fT*2.6,step(0.,f.x-lick)*9.))-.5));
 float dd=max(0.,length(vec2((f.x-lick)*ht*.37,(f.y-clamp(f.y,.14,.70))*ht))-.34*ht*.37),h=clamp(-d/max(w,.05),0.,1.)*step(-.08,f.y)*step(f.y,1.);
 float glow=exp(-dd/34.)*.50+exp(-dd/150.)*.55+exp(-dd/520.)*.42;vec3 c=mix(hex(0x2a0c04),hex(0xb04a10),smoothstep(.04,.5,glow));c=mix(c,hex(0xffa63c),smoothstep(.34,1.05,glow));c=mix(c,hex(0xffd888),smoothstep(.95,1.5,glow)*.7);
 vec2 fl=vec2(q.x*.034,q.y*.0085-fT*1.5);float n=fbm(fl+vec2(0,.6*fbm(fl*1.9+4.))),n2=fbm(vec2(q.x*.11+3.,q.y*.020-fT*2.8));
 float heat=h*(1.05-.40*smoothstep(.45,1.,f.y))+.30*(n-.5)*smoothstep(.0,.5,h)+.14*(n2-.5);
 vec3 k=mix(hex(0xf0660e),hex(0xff9a22),smoothstep(.05,.24,heat));k=mix(k,hex(0xffc24e),smoothstep(.20,.46,heat));k=mix(k,hex(0xffe39a),smoothstep(.42,.70,heat));k=mix(k,hex(0xfff6da)*1.06,smoothstep(.66,.98,heat));
 float root=smoothstep(.20,-.06,f.y);k=mix(k,mix(hex(0x6a6af0),hex(0xc8b8ff),smoothstep(.3,.9,h)),root*.78*smoothstep(.0,.4,h));
 c=mix(c,k,smoothstep(.0,.16+.20*smoothstep(8.,1.,zoom),h));
 float th=smoothstep(11.,3.2,zoom);vec2 g=p/(4.05*zoom)*1.0;vec2 a=abs(fract(g)-.5);float over=step(.5,fract(floor(g.x)*.5+floor(g.y)*.5));float warp=smoothstep(.46,.30,a.x),weft=smoothstep(.46,.30,a.y);float thr=max(warp*mix(.75,1.,over),weft*mix(1.,.75,over));float hole=(1.-warp)*(1.-weft);
 vec3 cloth=c*(.55+.45*thr*(.8+.2*sin(g.x*6.283*3.)))+hex(0xffc070)*.0;cloth=mix(cloth,c*1.25,hole);c=mix(c,cloth,th*smoothstep(1.4,2.6,zoom));
 float edge=smoothstep(.2,1.,length(p)/res.y);c*=1.-.25*edge*(1.-u);
 c=mix(c,hex(0xfff0c0),smoothstep(.78,1.,u));o=vec4(c,1);}
'''
DISC = '''
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform vec2 res,c;uniform float rad,fT,amt;
void main(){vec2 p=vec2(uv.x*res.x,(1.-uv.y)*res.y)-c;float r=length(p),a=atan(p.y,p.x);float ed=rad*(1.+.035*sin(a*16.+fT*2.)*smoothstep(130.,500.,rad));float k=smoothstep(ed+3.,ed-3.,r);
 vec3 q=mix(hex(0xfff3cc),hex(0xffd272),smoothstep(.72,1.,r/ed));float ring=smoothstep(10.,0.,abs(r-ed-16.))+smoothstep(6.,0.,abs(r-ed-40.));float ray=smoothstep(.0,.4,sin(a*24.-fT))*exp(-(r-ed)/(ed*.55+60.))*step(ed,r);
 vec3 g=hex(0xffb44a)*(exp(-max(0.,r-ed)/(ed*.35+90.))*.75+ray*.55)+hex(0xffe09a)*ring*.8*smoothstep(150.,420.,rad);o=vec4(q*k+g*(1.-k),k)*amt;}
'''


class Shot(ShotBase):
    id = 'a3'; n = 72
    EVENTS = [(0, 'through the cloth', dict(dur=24)), (24, 'sunrise bell', {}), (28, 'birds', dict(dur=44)), (30, 'river', dict(dur=42)), (40, 'temple bell', {})]

    def frame(self, f, st):
        st.clear('#000', f=f); t = st.t
        if f < 24:
            u = f / 23.; z = math.exp(lerp(0., math.log(30.), ease_in(u, 1.7))); st.paint(IN, zoom=float(z), u=float(u)); IM.zoomblur(st, (960, 540), .02 + .05 * u)
            return st.finish(bloom=.35, thr=.95, vig=.35, flash=.85 * (1 - smooth(0, 5, f)), flashCol='#ffdf90')
        u = (f - 24) / 47.; e = ease_io(u, 1.9); sd = nz(V(-.20, .285, -1.))
        eye = lerp(V(-30, 70, 660), V(40, 380, 610), e); at = lerp(eye + sd * 1300, V(-20, 275, -900), ease_io(clamp(u * 1.15), 2.2)); cam = Cam(eye, at, lerp(34, 41, e)); st.cam = cam
        st.paint('sky.frag', **AY.sky('dawn', sunDir=tuple(sd), sunR=.068)); st.open(cam, AY.light('dawn')); AY.draw(st, 'dawn'); AY.trees(st, 'dawn'); st.close()
        AY.birds(st, n=16, at=(-380 + 150 * t, 330 + 20 * t, -420), spread=(260, 60, 160), size=9.)
        near = -1.; x, y, z = cam.project(eye + sd * 4000.)
        rd = lerp(1400, 124, ease_out(clamp((f - 24) / 13.), 2.6)); k = 1 - smooth(35, 41, f)
        if k > 0: st.paint(DISC, 'over', c=(float(x), float(y)), rad=float(rd), amt=float(k))
        return st.finish(bloom=.42, thr=.95, vig=.32, contrast=1.04)
