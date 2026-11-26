"""f10 (96): dark.  Ten small flames hang where ten heads were.  Nine go out, one on every pulse (f12 .. f60); the last, in the middle, bows (f66) and goes out (f78).  Gold leaf falls like ash.  No cheering."""
from lau.shot import *

ORDER = [0, 9, 1, 8, 2, 7, 3, 6, 5]                     # outermost first; 4 is the last
OUT = {h: 12 + 6 * i for i, h in enumerate(ORDER)}; OUT[4] = 78

SRC = '''
#include "noise.glsl"
in vec2 uv;out vec4 o;uniform vec2 res;uniform float fT,water;uniform vec4 L[10];uniform vec4 S[10];   // L: x, y (px), height, amount   S: lean, bow, smoke age, seed
vec4 flame(vec2 p,vec4 l,vec4 s,float t){
 vec2 q=p-l.xy;q.y=-q.y;float ht=l.z;if(l.w<=.002) return vec4(0);
 float sw=.05*sin(t*3.1+s.w)+.08*(vn(vec2(t*2.1,s.w))-.5);float y=q.y/ht,x=q.x/(ht*.42);x-=(s.x+sw)*y*y*1.2+s.y*y*1.6;y+=abs(s.y)*.35*y;
 float w=0.;if(y>-.08&&y<1.){float k=(y+.08)/1.08;w=.5*pow(k,.46)*pow(1.-k,.86)*1.46;}float d=abs(x)-w;float b=smoothstep(.03,-.03,d)*step(-.08,y)*step(y,1.);float h=clamp(-d/max(w,.02),0.,1.);
 vec3 c=mix(hex(0xb8240a),hex(0xff7a14),smoothstep(0.,.25,h));c=mix(c,hex(0xffb83a),smoothstep(.2,.45,h));c=mix(c,hex(0xffe7a8)*1.1,smoothstep(.45,.95,h)*smoothstep(.9,.4,y)*smoothstep(-.05,.3,y));c=mix(c,hex(0x2c3a9a)*.8,smoothstep(.18,-.05,y)*.8);
 vec2 g=q-vec2(0,ht*.4);float r=length(g);float gl=exp(-r*r/(ht*ht*.6))*.30+exp(-r/(ht*1.15))*.15;
 return vec4(c*b+hex(0xff8a2c)*gl,b)*l.w;}
void main(){vec2 p=vec2(uv.x*res.x,(1.-uv.y)*res.y);vec3 c=hex(0x050308)*(.6+.5*fbm(uv*vec2(5.,3.)));
 float isW=step(water,p.y);vec2 m=p;if(isW>.5){float dy=p.y-water;m.y=water-dy*1.06;float rp=(vn(vec2(p.x*.010+fT*.25,dy*.06-fT*.7))-.5)*(6.+dy*.10)+(vn(vec2(p.x*.05,dy*.22+fT*1.1))-.5)*(2.+dy*.03);m.x+=rp;m.y+=rp*.25;}
 vec3 a=vec3(0);float cov=0.;for(int i=0;i<10;i++){vec4 f=flame(m,L[i],S[i],fT);a=a*(1.-f.a)+f.rgb;cov=max(cov,f.a);
   float age=S[i].z;if(age>0.){vec2 q=m-L[i].xy;q.y=-q.y;float y=q.y/ (70.+90.*age);if(y>0.&&y<3.2){float wv=26.*(fbm(vec2(y*1.6-age*1.3+S[i].w,S[i].w))-.5)*y+14.*sin(y*3.-age*4.+S[i].w)*y;float w=(5.+16.*y)*(1.+age);float k=exp(-pow((q.x-wv)/w,2.)*2.)*smoothstep(0.,.15,y)*smoothstep(3.2,.8,y)*exp(-age*1.5)*smoothstep(0.,.12,age);a+=hex(0x8a84a0)*k*.22;}}}
 if(isW>.5){float dy=(p.y-water);a*=.42*exp(-dy/420.);c=mix(c,hex(0x080610),.5);}
 c+=a;c+=hex(0x2a1608)*exp(-abs(p.y-water)/3.)*.5;o=vec4(c,1);}
'''


class Shot(ShotBase):
    id = 'f10'; n = 96
    EVENTS = [(f, 'light out', dict(k=i)) for i, f in enumerate(sorted(v for v in OUT.values() if v < 70))] + [(66, 'last light bows', {}), (78, 'last light out', {})]

    def frame(self, f, st):
        st.clear('#000', f=f); t = st.t; push = ease_io(f / 95., 1.4); L, S = [], []; wy = 700.
        for i in range(10):
            k = i - 4.; s = 1 - .055 * abs(k); x = 960 + (k * 168 + (20 if i > 4 else 0)) * (1 + .10 * push) * (1 - .012 * abs(k)); y = 520 + 4.5 * k * k * (1 + .1 * push) - 8 * push; ht = (116 if i == 4 else 92) * s * (1 + .12 * push)
            o = OUT[i]; a = 1 - smooth(o, o + 3, f); fl = 1 + .10 * noise1(t * 7, i) + .06 * noise1(t * 17, i + 20); lean = .10 * noise1(t * 1.3, i + 40); bow = 0.
            if i != 4: lean += .9 * smooth(o - 4, o + 1, f) * (1 if i % 2 else -1); ht *= 1 - .45 * smooth(o - 2, o + 3, f)
            else:
                b = keys(f, [(60, 0.), (74, 1., 'io'), (78, 1.12, 'in'), (82, 1.12)]); bow = -.75 * b; y += 34 * b; ht *= (1 - .42 * b) * (1 - .6 * smooth(77, 81, f)); fl = 1 + (fl - 1) * .4
            L.append((x, y, ht * fl, a)); S.append((lean, bow, max(0., (f - o - 1) / 24.), i * 3.7 + 1.))
        st.paint(SRC, L=np.array(L, 'f4'), S=np.array(S, 'f4'), water=wy)
        live = sum(l[3] for l in L)
        # gold leaf: each flake only shows where a flame still lights it
        r = np.random.default_rng(6); n = 190; p0 = r.uniform(0, 1, (n, 2)); k = r.uniform(.5, 1.3, n); x = p0[:, 0] * 2100 - 90 + 46 * np.sin(t * 1.1 * k + p0[:, 1] * 40); y = np.mod(p0[:, 1] * 1200 + t * 46 * k + 20 * np.sin(t * .8 + p0[:, 0] * 30), 1200) - 60
        P = np.c_[x, y]; lit = np.zeros(n)
        for lx, ly, h, a in L: lit += a * np.exp(-((P[:, 0] - lx) ** 2 + (P[:, 1] - ly + 40) ** 2) / (2 * (150. + h) ** 2))
        al = np.clip(lit * .9 + .05 + .10 * smooth(80, 90, f), 0, 1) * (y < wy + 60); FX.particles(st, P, 3.2 + 5.2 * k, np.array(hexc('#ffc85a')) * (.35 + .9 * np.clip(lit, 0, 1.2))[:, None], 'flake', rot=t * 2.2 * (k - .9) * 3 + p0[:, 0] * 9, seed=p0[:, 0], alpha=al)
        return st.finish(bloom=.50, thr=.85, vig=.6, grain=.017, contrast=1.06, fade=smooth(90, 96, f) * .6)
