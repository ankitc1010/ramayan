"""g4 (120): from the ghats the camera rises over the lamps of Ayodhya until it looks down on the sleeping city, and the lamps of the whole city write राम (f84).
The lamps of the word lie where the last camera's rays meet the city (water, steps, streets, roofs), so from below they are only lamps."""
from lau.shot import *
from lau.look import *
from .g_kit import *

RISE = (8, 94)                                                 # the climb
UNIT, X0, Y0 = 800., 298., 150.                                # the word on the last picture: letter height, left end and head line (pixels)
HOLD = 98                                                      # frame whose camera the word is written for


def camera(f):
    u = ease_io((f - RISE[0]) / (RISE[1] - RISE[0]), 2.3); d = smooth(84, 119, f); lo = f / 24.
    y = 13. * (1960. / 13.) ** u + 45 * d; pitch = lerp(5., -79.5, ease_io(u, 1.35)); z = lerp(250., 20., smooth(0, 1, u)); x = lerp(-36., 0., u)
    eye = V(x, y + 1.5 * lo * (1 - u), z - 5 * lo * (1 - u)); a = math.radians(pitch)
    return Cam(eye, eye + V(.10 * (1 - u), math.sin(a), -math.cos(a)) * 100, lerp(44, 40, u), roll=1.5 * math.sin(math.pi * u))


POOL = '''
in vec2 uv;out vec4 o;uniform sampler2D tex,tW;uniform vec2 res;uniform mat3 A;uniform float amt,t;
void main(){vec3 c=texture(tex,uv).rgb;vec2 p=vec2(uv.x*res.x,(1.-uv.y)*res.y);vec2 q=(A*vec3(p,1)).xy/res;q.y=1.-q.y;float g=textureLod(tW,q,4.6).a*.9+textureLod(tW,q,6.2).a*.8;if(min(q.x,q.y)<0.||max(q.x,q.y)>1.)g=0.;g*=amt;
 float l=dot(c,vec3(.3,.5,.2));o=vec4(c+vec3(1.,.50,.16)*g*(l*2.6+.010),1);}
'''


CUP = PR.DIYA.variant(pal={3: ('#4a7a3a', '#1c3420', 1), 6: ('#f7efdc', '#a08070', 1), 14: ('#b0621c', '#4a1c0c', 3)})


class Shot(ShotBase):
    id = 'g4'; n = 120
    EVENTS = [(0, 'river lamps', dict(dur=40)), (0, 'crowd far', dict(dur=60)), (8, 'camera rises', dict(dur=76)), (40, 'wind high', dict(dur=80)), (84, 'the word reads', {}), (96, 'temple bell', dict(soft=1)), (110, 'one lamp', {})]

    def light(self, hi):
        return AY.light('night', inkRef=lerp(5., 14., hi), keyCol=tuple(lerp(np.array(hexc('#3e4c96')), np.array(hexc('#182258')), hi)), amb=tuple(lerp(np.array(hexc('#2a3270')), np.array(hexc('#0f163e')), hi)), rimCol=tuple(np.array([.22, .24, .45]) * (1 - .8 * hi)), fog=(.00036 * (1 - hi), 300., .0016, 0.))

    def setup(self, st):
        # the city as the last camera sees it: a depth map, on which the word is laid
        cam = camera(HOLD); st.clear('#000', f=HOLD); st.open(cam, self.light(1.), far=8000.); city(st, 0., .1, trees=0); st.close()
        D = st.depth()
        S, w = LT.strokes('ram', 160); r = np.random.default_rng(11); nib = np.array([math.cos(math.radians(-47)), math.sin(math.radians(-47))]); Q = []
        for s in S:
            L = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(s, axis=0), axis=1))])
            for k, off in enumerate((-.052, -.018, .018, .052)):
                n = int(L[-1] / .030); q = np.linspace(0, L[-1], n) + (k % 2) * .015; Q.append(np.c_[np.interp(q, L, s[:, 0]), np.interp(q, L, s[:, 1])] + nib * off)
        Q = np.vstack(Q) * UNIT + [X0, Y0] + r.normal(0, 2.2, (sum(len(q) for q in Q), 2))
        z = D[np.clip(Q[:, 1], 0, H - 1).astype(int), np.clip(Q[:, 0], 0, W - 1).astype(int)]
        d = np.array([cam.ray(*q) for q in Q]); P = cam.eye + d * ((z - 5.) / (d @ cam.R[2]))[:, None]
        self.word = P; self.m = len(P); self.wet = P[:, 1] < 8.
        # three lamps of the river that are still on their way: the last of each lower stroke
        self.late = []
        for x in (.50, .77, 1.54):
            c = np.array([x * UNIT + X0, .90 * UNIT + Y0]); self.late.append(int(np.argmin(((Q - c) ** 2).sum(1) + 1e6 * ~self.wet)))
        self.Q = Q
        self.one = int(np.argmin(((Q - [1265, 572]) ** 2).sum(1)))
        sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); LT.draw(cairo.Context(sf), 'ram', X0, Y0, UNIT, w=.16); sf.flush(); self.tw = gl.tex_from(np.ndarray((H, W, 4), np.uint8, sf.get_data()).copy())
        self.lamps = AY.lamp_points(); g = np.random.default_rng(3); self.keep = g.uniform(0, 1, len(self.lamps))
        g = np.random.default_rng(5); n = 260; self.water = np.c_[g.uniform(-700, 700, n), np.full(n, .9), 8 + 330 * g.uniform(0, 1, n) ** 1.4]
        T = people_tiles(False); self.cr = Crowd(st, [(a, b, c, yw) for yw in (-22, 14) for a, b, c in T], px=260, pitch=2.); self.off = np.array([flame_offset(a, b, yw) for yw in (-22, 14) for a, b, c in T])
        n = 320; x = np.r_[g.uniform(-330, 330, n)]; st_ = g.integers(1, 19, n); z = -st_ * 4.75 + 2.4; self.folk = np.c_[x, AY.ground(x, z), z]; self.tile = g.integers(0, 16, n)

        self.cups = [(-27, 34, 1.15, 20), (-9, 52, 1.0, 120), (6, 30, 1.2, -40), (21, 46, 1.1, 200), (-40, 66, 1.1, 60), (34, 74, 1.2, 10), (-17, 82, 1.1, 80)]

    def frame(self, f, st):
        st.clear('#05071e', f=f); t = st.t; cam = camera(f); st.cam = cam
        u = ease_io((f - RISE[0]) / (RISE[1] - RISE[0]), 2.3); hi = smooth(.25, .95, u); dark = smooth(.35, 1., u)
        if cam.R[2][1] > -.75: st.paint('sky.frag', **AY.sky('night', sunGlow=0.))
        st.open(cam, self.light(hi), far=8000.); city(st, 1 - .95 * dark, lerp(.38, .14, smooth(0, .7, u)), trees=1 - dark, tall=1 - smooth(.56, .70, u), tint=tuple(np.array([.9, .8, .75]) * (1 - .55 * dark)))
        small = 1 - smooth(.56, .68, u)
        if small > .05: self.cr.draw(self.folk, scale=small, upright=1 - .4 * smooth(.3, .55, u), tile=self.tile, tint=tuple(np.array([2.1, 1.55, 1.15]) * (1 - .85 * dark)))
        near = []
        if u < .35:
            M = np.eye(4); L = st.light
            for k, (x, dz, sc, yw) in enumerate(self.cups):
                at = V(x + 2.2 * t * (1 if k % 2 else -.6) + .3 * math.sin(t * 1.1 + k), .35 + .12 * math.sin(t * 1.7 + k * 2), 250 - dz); M[:3, :3] = eul(yw + 10 * t, 3 * math.sin(t * 1.3 + k), 3 * math.cos(t * 1.1 + k)) * sc; M[:3, 3] = at; near.append((at + M[:3, :3] @ V(1.30, .42, 0), sc)); st.fig(CUP, M=M.copy())
            L.pts = [(p + V(0, 1.2, 0), 3.2, (.42, .20, .07)) for p, _ in near][:10]
        st.close(); amber(st, .9)
        # the lamps that are not the word
        rest = np.clip(1.25 - 1.22 * dark - .25 * self.keep, .0, 1.) * (1 - .0 * dark); rest = np.maximum(rest, (.085 * (self.keep < .22)))
        glows(st, self.lamps, 1.1, lerp(1.5, 1.2, dark), rest, gain=1.5)
        drift = np.array([t * 5., 0, 0]); glows(st, self.water + drift * np.random.default_rng(6).uniform(.4, 1.4, (len(self.water), 1)), 1.1, 1.5, 1 - .93 * dark)
        if u < .5: glows(st, self.folk + self.off[self.tile], .8, 1.6, 1.)
        # the word
        P = self.word.copy()
        for k, i in enumerate(self.late):
            a = 1 - smooth(72, 108 + 3 * k, f); P[i] += V((90 + 30 * k) * a * (1 if k != 1 else -1), 0, (120 + 25 * k) * a) + V(3 * math.sin(t * 1.3 + k), 0, 2 * math.cos(t * 1.1 + k)) * a
        bob = self.wet[:, None] * np.c_[.8 * np.sin(t * 1.4 + np.arange(self.m)), np.zeros(self.m), .6 * np.cos(t * 1.1 + np.arange(self.m) * 2)]; P = P + bob
        s = 1 + .38 * np.sin(np.arange(self.m) * 2.399); up = smooth(.55, .9, u)
        if up > 0:                                                                    # the light of the word lies on the roofs
            q = cam.project(self.word)[:, :2]; A, *_ = np.linalg.lstsq(np.c_[q, np.ones(self.m)], np.c_[self.Q, np.ones(self.m)], rcond=None); st.post_paint(POOL, texs=dict(tW=self.tw), A=A.T, amt=float(smooth(.74, .97, u)), t=t)
        glows(st, P, 1.1, lerp(1.5, 6.2, hi) * s, 1 - .8 * up, col='#ff9a3a', gain=1.8, tw=.22)
        if up > 0:                                                                    # nothing hides them from straight above
            q = cam.project(P)[:, :2]; ph = np.arange(self.m) * 1.7; tw = .80 + .20 * np.sin(t * 2.6 + ph) * np.sin(t * 1.7 + ph * 2.1) + .06 * np.sin(t * 11 + ph * 3)
            if f >= 104: near_ = np.linalg.norm(q - q[self.one], axis=1); tw = tw * np.clip((lerp(1500, 0, ease_io((f - 104) / 15., 1.4)) - near_) / 260. + 1, 0, 1) ** 1.5
            FX.particles(st, q, 34., '#ff7a1e', 'ember', alpha=.045 * up * tw, seed=ph % 1); FX.particles(st, q, 14.5 * s, np.array(hexc('#ff8a2a')) * 2.3, 'lamp', alpha=up * tw, seed=ph % 1)
        self.reflect(st, t, 1 - dark)
        for k, (p, sc) in enumerate(near):
            x, y, z = cam.project(p)
            if z > 4 and -80 < x < 2000 and y < 1250:
                FX.ribbon(st, np.array([p * [1, 0, 1] + V(0, .05, 0) + V(0, 0, q) for q in np.linspace(.6, 7, 12)]) + np.c_[.35 * np.sin(np.arange(12) * 1.3 + t * 5 + k), np.zeros(12), np.zeros(12)], np.linspace(.42, .06, 12) * sc, 'light', '#ff8a2a', '#ffd890', amt=.28); FX.flame(st, p, 1.7 * sc, seed=k * 2.1, glow=.8, calm=1.)
        if f >= 104:
            k = self.one; x, y, _ = cam.project(P[k]); IM.iris(st, (float(x), float(y)), lerp(1350, 20, ease_io((f - 104) / 15., 1.5)), lerp(900, 210, smooth(104, 119, f)), col=hexc('#020208')); e = smooth(112, 118, f)
            FX.particles(st, np.array([[x, y]]), 70 + 60 * e, '#ff7a1e', 'ember', alpha=.30 * e); FX.particles(st, np.array([[x, y]]), 22 + 10 * e, np.array(hexc('#ff8a2a')) * 2.3, 'lamp', alpha=e)
        return st.finish(bloom=lerp(.6, .5, hi), thr=.9, vig=.42, contrast=1.06, satu=1.05)

    def reflect(self, st, t, amt):
        """the lights lie on the river as broken streaks while we are low"""
        if amt < .05 or st.cam.eye[1] > 500: return
        g = np.random.default_rng(9); A = self.lamps; A = A[np.abs(A[:, 0]) < 900]; A = A[g.permutation(len(A))[:2200]]; n2 = len(A); e = st.cam.eye; k = e[1] / (e[1] + A[:, 1]); Q = e + (A * [1, -1, 1] - e) * k[:, None]
        w = np.sin(t * g.uniform(2, 5, n2) + g.uniform(0, 6.28, n2)); Q[:, 0] += w * 1.5; Q[:, 1] = .15; z = ((Q - e) @ st.cam.R.T)[:, 2]; m = (Q[:, 2] > 3) & (z > 5); Q, w, z = Q[m], w[m], z[m]; p2 = st.cam.fl * 540 / z
        FX.particles(st, Q, 1.7 / p2, np.array(hexc('#ff9a3a')) * 1.3, 'ember', vel=np.c_[0 * w, (34 + 18 * w) / p2, 0 * w], alpha=amt * (.30 + .25 * w))
