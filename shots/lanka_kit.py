"""Lanka on fire as a page that is written on: the city of worlds/lanka with a stage cleared along Hanuman's path, and a fire that starts where his tail passed and spreads from there.
hero(f) = where he is (world); ARR = the moment (seconds) at which the fire reaches each place of the city; every flame of d8 reads it."""
from lau.shot import *
from lau.look import *
from lau.stage import hexc
from worlds import lanka as LK, place
from pathlib import Path

SC = 1.5                                                       # Hanuman's scale in this city
NCL = LK.NC
AW = 2600.                                                     # width of the arrival map
CURL = V(-250., 0., 550.)                                      # centre of the curl he writes


def cell(x, z): return int(math.floor(z / 100)) + NCL // 2, int(math.floor(x / 100)) + NCL // 2


def stage_layout():
    """the city's layout with flat roofs under his feet and open air for the camera"""
    A, B = (q.copy() for q in LK.layout())

    def roof(x, z, top, H, hx=40., hz=40., kind=4):
        k = cell(x, z); A[k] = (kind, hx, H, hz); B[k] = (0., 0., top, .3)
    for x, z, top in ((150, 250, 540), (150, 350, 500), (150, 450, 460), (150, 550, 420)): roof(x, z, top, 60)
    for x in (-50, 50):                                         # the avenue steps down beside him
        for z, top in ((150, 584), (250, 512), (350, 440), (450, 404), (550, 368), (650, 296), (750, 296), (850, 260), (950, 260)): k = cell(x, z); A[k] = (0, 40, 30, 40); B[k][2] = top
    r = np.random.default_rng(8)
    for x in range(-550, -60, 100):                             # the quarter of the curl: one broad terrace of low roofs, courts between them
        for z in range(350, 851, 100):
            kind = int(r.choice([2, 4, 4, 0], p=[.40, .25, .20, .15])); k = cell(x, z); A[k] = (kind, r.uniform(30, 40), 30. if kind == 4 else 60., r.uniform(30, 40)); B[k] = (0, 0, 296. if z > 400 else 404., r.uniform(.1, .9))
    roof(-150, 750, 296, 60); roof(-250, 550, 296, 60); roof(-150, 350, 470, 0, kind=0); roof(-150, 250, 548, 0, kind=0)
    roof(150, 650, 296, 60, kind=4); roof(-150, 650, 296, 60, kind=4)
    for x, z in ((150, 750), (250, 650), (250, 750), (150, 850)): A[cell(x, z)][2] = min(A[cell(x, z)][2], 90.)
    return A, B


_C = {}


def lay():
    if 'A' not in _C: _C['A'], _C['B'] = stage_layout()
    return _C['A'], _C['B']


def roof_y(x, z):
    """height of whatever stands at (x, z): a roof, or the terrace"""
    A, B = lay(); j, i = cell(x, z)
    if not (0 <= i < NCL and 0 <= j < NCL): return 0.
    t, hx, H, hz = A[j, i]; dx, dz, top, s = B[j, i]
    if top < 1: return 0.
    u, v = x - ((i - NCL / 2 + .5) * 100 + dx), z - ((j - NCL / 2 + .5) * 100 + dz); ins = abs(u) < hx and abs(v) < hz
    if max(abs(x), abs(z + 60)) < 165: return 700. if max(abs(x), abs(z + 60)) > 120 else 750.
    if t == 0 or not ins: return float(top)
    if t == 4: return float(top + H + (30 if abs(u) < .6 * hx and abs(v) < .6 * hz else 0))
    if t == 2: return float(top + math.floor(H * .5 / 30 + .5) * 30)
    return float(top + H * .6)


# ------------------------------------------------------------------ his way through the city
LAND = {0: V(46, 656, 136), 12: V(118, 600, 250), 24: V(118, 560, 350), 30: V(118, 520, 446), 42: V(118, 480, 552), 54: V(-118, 356, 748), 66: None, 72: None, 84: V(-218, 356, 550), 90: V(-128, 470.5, 348), 96: V(-84, 700.5, 96), 102: V(-20, 932, 2), 108: V(6.5, 1128, -60)}
R0 = LAND[54] - CURL; PH0, RR0 = math.atan2(R0[2], R0[0]), math.hypot(R0[0], R0[2])


def curl(f):
    """ground point of the curl, f 54..84: a spiral, as a brush ends a stroke"""
    u = clamp((f - 54) / 30.); a = PH0 + math.radians(405) * u; r = 32 + (RR0 - 32) * (1 - u) ** .82; return V(CURL[0] + r * math.cos(a), 356., CURL[2] + r * math.sin(a))


for k in (66, 72): q = curl(k); LAND[k] = V(q[0], 402., q[2])
LF = sorted(LAND)
TOPF = 108; APEX = V(0, 1322, -30); SEA = V(430, 0, 1650)
HOLD = 2                                                       # frames he stays in the crouch of a landing


def hero(f):
    """feet of Hanuman at (float) frame f"""
    if f <= 0: return LAND[0] + V(-6, 0, -18) * (-f)
    if f < TOPF:
        a = max(k for k in LF if k <= f); b = min(k for k in LF if k > f); h = 0 if a == 0 else HOLD; u = clamp((f - a - h) / (b - a - h)); A, B = LAND[a], LAND[b]
        g = 46. if (a, b) == (42, 54) else 26. if b - a == 12 and a < 54 else 12. if b - a == 6 and a < 54 else 30. if a < 84 else 22.
        if 54 <= a < 84: ca, cb = curl(a), curl(b); q = curl(a + (b - a) * u); P = q + (A - ca) * (1 - u) + (B - cb) * u; P[1] = A[1] + (B[1] - A[1]) * u
        else: P = A + (B - A) * u
        if b <= 54: P[1] = A[1] + (B[1] - A[1]) * u ** 2.2
        if b >= 90: P[1] = A[1] + (B[1] - A[1]) * (1 - (1 - u) ** 1.6)
        return P + V(0, 4 * g * u * (1 - u), 0)
    if f < 111: return LAND[108].copy()
    if f < 126: u = (f - 111) / 15.; return lerp(LAND[108], APEX, 1 - (1 - u) ** 2.6) + V(0, 0, 10 * u)
    u = clamp((f - 126) / 24.); A = APEX + V(0, 0, 10); return V(A[0] + SEA[0] * u ** 1.6, A[1] * (1 - u ** 2.2) + 26 * math.sin(math.pi * u) * (1 - u), A[2] + (SEA[2] - A[2]) * u ** 3)


def trail(f):
    """the path a brush behind him takes: the same without the stops"""
    return sum(hero(f + k) * w for k, w in ((-2, .25), (0, .5), (2, .25)))


def heading(f, d=1.5):
    v = hero(f + d) - hero(f - d); return v


# ------------------------------------------------------------------ when the fire reaches a place
def spread(tau, quick, fast=0.):
    """how far the fire has crept from its first mark after tau seconds: a thin stroke in the streets, a leap from tower to tower on the way up"""
    return 14 * np.clip(tau / .16, 0, 1) ** .6 + (12 + 100 * quick) * np.clip(tau - .12, 0, .6) + 84 * fast * np.clip((tau - .03) / .20, 0, 1) + 15 * np.clip(tau - .72, 0, None) + 8 * np.clip(tau - 1.6, 0, None) ** 2


def arrival():
    if 'T' in _C: return _C['T']
    n = 416; g = (np.arange(n) + .5) / n * AW - AW / 2; X, Z = np.meshgrid(g, g); tau = np.linspace(0, 7, 1400); T = 4.45 + np.hypot(X, Z + 60) / 1500. + .25 * np.sin(X * .011 + 1) * np.sin(Z * .013)      # when he springs, the whole city goes up from the palace outward
    for f in np.arange(9, 108, .34):
        p = trail(f); d = np.hypot(X - p[0], Z - p[2]); T = np.minimum(T, f / 24 + np.interp(d, spread(tau, .9 * (1 - smooth(50, 56, f)) + smooth(82, 86, f) * (1 - .6 * smooth(97, 104, f)), smooth(82, 86, f) * (1 - .7 * smooth(98, 104, f))), tau, right=7.))
    _C['T'] = T; return T


def arr(P):
    """arrival time at points (N,3)"""
    T = arrival(); n = len(T); u = np.clip((np.asarray(P)[:, [0, 2]] + AW / 2) / AW * n - .5, 0, n - 1.001); i = u.astype(int); w = u - i; x, z = i[:, 0], i[:, 1]; a, b = w[:, 0], w[:, 1]
    return (T[z, x] * (1 - a) + T[z, x + 1] * a) * (1 - b) + (T[z + 1, x] * (1 - a) + T[z + 1, x + 1] * a) * b


_OLD = 'float burnAt(vec3 p){if(fire<=0.) return 0.;float d=length((p-fireAt)*vec3(1,.7,1));return smoothstep(0.,170.,fire*2700.-d-240.*vn(p.xz*.011+3.));}'
_NEW = 'uniform sampler2D tArr;uniform float fNow,aW,uGlow;float burnAge(vec3 p){return fNow-textureLod(tArr,p.xz/aW+.5,0.).x-.30*(vn(p.xz*.045+3.)-.5)-.10*(vn(vec2(p.x+p.z,p.y)*.06)-.3);}float burnAt(vec3 p){return smoothstep(.0,.55,burnAge(p));}'
_OLD2 = 'void burnPaint(vec3 p,vec3 n,inout Surf s){float b=burnAt(p);if(b<=0.) return;'
_NEW2 = """void burnPaint(vec3 p,vec3 n,inout Surf s){float ag=burnAge(p);
 // the light of the fire on everything near it, before it burns itself
 float glw=exp(min(ag,0.)*4.2)*uGlow;if(glw>.01){float fk=.85+.15*vn(vec2(fT*9.,p.x*.02+p.z*.02));vec3 w=vec3(1.15,.27,.015)*glw*fk;if(s.cls<1.5) emit(s,mix(vec3(dot(s.base,vec3(.33))),s.base,.45)*w*(n.y>.6?.40:.42));else if(s.cls<2.5) s.base*=mix(vec3(1),vec3(1.55,1.02,.62),glw);}
 float b=burnAt(p);if(n.y>.6&&s.cls<1.5){s.base*=.52;s.sh*=.60;}if(b<=0.) return;
 if(n.y>.6&&s.cls<1.5){float cr=fbm(p.xz*.13+vec2(0,-fT*.9)),c2=fbm(p.xz*.045+vec2(fT*.12,-fT*.5));float fr=smoothstep(-.02,.04,ag)*smoothstep(.70,.08,ag);float h=fr*(.45+.9*cr)+(b*smoothstep(.40,.75,c2)*.62)*smoothstep(3.2,.4,ag);
  s.base*=1.-.6*b;s.sh*=1.-.5*b;vec3 e=mix(vec3(.16,.012,.0),vec3(.85,.14,.01),smoothstep(.18,.40,h));e=mix(e,vec3(1.05,.34,.025),smoothstep(.40,.62,h));e=mix(e,vec3(1.35,.78,.17),smoothstep(.66,.9,h));float k=smoothstep(.10,.24,h);if(k>.4){s.cls=4.;s.base=e;s.ink=.12;s.part+=floor(smoothstep(.3,.5,h)*2.)*3.;}return;}"""
_FIX = [('m=U(m,aChhatri(vec3(abs(q.x)-h.x+7.,q.y-H1,abs(q.z)-h.z+7.),6.4));', 'if(abs(B.w-.3)>.001) m=U(m,aChhatri(vec3(abs(q.x)-h.x+7.,q.y-H1,abs(q.z)-h.z+7.),6.4));'),      # his landing roofs have no kiosks on the corners
        ('vec3(0,A.z*.56+17.,0),vec3(A.y+3.4,A.z*.56+17.,A.w+3.4)', 'vec3(0,A.z*.56+17.+(A.x>3.5?44.:0.),0),vec3(A.y+3.4,A.z*.56+17.+(A.x>3.5?44.:0.),A.w+3.4)'),      # the roof pavilions were cut off by their bounding boxes
        ('emit(s,hot*b*(.04+.36*rise*rise));', 'emit(s,hot*b*(.02+.20*rise*rise));'), ('p.y-B.z-A.z*1.12-34.', 'p.y-B.z-A.z*1.12-34.-(A.x>3.5?88.:0.)'),
        ('emit(s,vec3(.6,.25,.06)*.22*pNight);return;}', 'emit(s,vec3(.6,.25,.06)*.035*pNight);return;}'), ('emit(s,vec3(.8,.32,.07)*(.12+.4*exp(-yb*.14))*pNight)', 'emit(s,vec3(.8,.30,.05)*(.015+.26*exp(-yb*.14))*pNight)')]


def src():
    if 's' not in _C:
        s = Path(__file__).resolve().parent.parent.joinpath('worlds/lanka.glsl').read_text()
        for a, b in [(_OLD, _NEW), (_OLD2, _NEW2)] + _FIX:
            if a not in s: raise SystemExit('lanka.glsl changed: lanka_kit must be fitted again: ' + a[:60])
            s = s.replace(a, b)
        _C['s'] = s
    return _C['s']


def tex():
    if 'tl' not in _C:
        A, B = lay(); T = np.zeros((NCL * 2, NCL, 4), 'f4'); T[0::2] = A; T[1::2] = B; t = gl.ctx().texture((NCL, NCL * 2), 4, T.tobytes(), dtype='f4'); t.filter = (0x2600, 0x2600)
        a = arrival().astype('f4'); u = gl.ctx().texture(a.shape[::-1], 1, a.tobytes(), dtype='f4'); u.filter = (0x2601, 0x2601); u.repeat_x = u.repeat_y = False; _C['tl'] = t, u
    return _C['tl']


def hx(a, b, t): a, b = np.array(hexc(a)), np.array(hexc(b)); return tuple(a * (1 - t) + b * t)


SKYA = dict(cZen='#03041a', cMid='#0a1038', cHor='#1c2054', cLow='#060824', cLit='#3a3c78', cCM='#1a1c4a', cSh='#0c0e2c', cInk='#04040f', starAmt=1.)
SKYB = dict(cZen='#05020c', cMid='#16060f', cHor='#541408', cLow='#0c0306', cLit='#8c3014', cCM='#3c1016', cSh='#16060c', cInk='#0a0306', starAmt=.35)
LA = dict(keyCol='#444966', amb='#1a2152', rimCol=(.13, .16, .36), bounceCol=(.20, .07, .02), envT='#3a4cb0', envM='#d89a4a', envB='#c8641e', fogCol='#101848')
LB = dict(keyCol='#a8481c', amb='#2c1230', rimCol=(1.3, .45, .12), bounceCol=(.45, .15, .03), envT='#4a1838', envM='#ff9a40', envB='#ffb44a', fogCol='#340b08')
SEAA, SEAB = ('#1c2860', '#03041a', (.35, .30, .4)), ('#1e0806', '#030104', (1.0, .34, .08))


def blend(A, B, t): dk = 1 - 1.5 * t * (1 - t); return {k: (tuple(dk * np.array(hx(A[k], B[k], t))) if not isinstance(A[k], float) else A[k] * (1 - t) + B[k] * t) for k in A}


def sky(w, **k): return SKY(LK.MOOD['fire']['sky'], **{**blend(SKYA, SKYB, w), **dict(cov=.45, cy0=.02, cy1=.34, sunGlow=0.), **k})


def light(w, **k): return Light(**{**dict(key=tuple(lerp(V(-.55, .6, .5), V(.15, -.12, .8), w)), rim=(.05, .4, -1.), fog=(.00026, 420., .0010, 0.), ink=3., inkCol='#050207', shadow=False), **blend(LA, LB, w), **k})


def city(st, now, w=1., night=1., defs='', glow=1., **u):
    """inside open/close: the city with everything burning that the fire has reached by `now` seconds"""
    W_ = [hx(p, q, w) for p, q in zip(SEAA, SEAB)]; a, b = tex()
    place.draw(st, src(), u=dict(night=float(night), fire=1., fireAt=(0., 0., 0.), doors=0., skyA=W_[0], skyB=W_[1], skyC=W_[2], fNow=float(now), aW=AW, uGlow=float(glow), **u), texs=dict(tLanka=a, tArr=b), defs=defs, sun=0.)


# ------------------------------------------------------------------ flames
def fire_points():
    """(x, y, z, size) of every place a flame can stand: roofs, tower tops, and the stroke itself"""
    if 'fp' not in _C:
        A, B = lay(); keep = dict(LK._C); LK._C.clear(); LK._C.update(A=A, B=B); P = LK.fire_points().copy(); LK._C.clear(); LK._C.update(keep)
        r = np.random.default_rng(5); Q = []
        for f in np.arange(1, 108, .22):
            p = trail(f); s = r.normal(0, 5., 2); y = roof_y(p[0] + s[0], p[2] + s[1])
            if f > 96: y = p[1] - 2
            Q.append((p[0] + s[0], y + .5, p[2] + s[1], r.uniform(9, 17) * (1 + .9 * smooth(82, 88, f)), f / 24 + .10 + .05 * r.uniform()))
        Q = np.array(Q); _C['fp'] = np.vstack([P, Q[:, :4]]); _C['ft'] = np.r_[arr(P), Q[:, 4]]; top = _C['fp'][:, 1] > 1000; _C['ft'][top] = np.maximum(_C['ft'][top], 4.75); _C['fs'] = r.uniform(0, 1, (len(_C['fp']), 5)); _C['ns'] = len(Q)
    return _C['fp'], _C['ft'], _C['fs']


def flames(st, now, cam, n=1100, per=3, gain=(.95, .84, .74), near=36., rise=1., slope=.45):
    """after close: tongues on every burning point in view, the nearest n of them, tall ones stretched upward in world space"""
    F, T, R = fire_points(); age = now - T; c = (F[:, :3] - cam.eye) @ cam.R.T; z = c[:, 2]
    m = (age > 0) & (z > near) & (np.abs(c[:, 0]) * cam.fl < z * 1.9 + 60) & (np.abs(c[:, 1]) * cam.fl < z * 1.25 + 90); i = np.flatnonzero(m)
    if len(i) == 0: return 0
    if len(i) > n: i = i[np.argsort(z[i] / F[i, 3])[:n]]                # biggest on screen first
    b = np.clip(age[i] / (.45 if now < 3.5 else .28), 0, 1); grow = (b * (1.15 - .15 * b)) * (1 + .35 * np.exp(-((age[i] - .55) / .3) ** 2)); P, Sz, Vl, Sd = [], [], [], []
    for k in range(per):
        q = (R[i, k] * 2 - 1)[:, None]; s = F[i, 3] * grow * rise * (1 - .28 * k) * (.75 + .5 * R[i, 2 + k % 2]); j = np.c_[(R[i, 1 + k] - .5), 0 * s, (R[i, 3] - .5)] * F[i, 3:4] * .9 * k; h = np.c_[0 * s, s * 2.1, 0 * s]; P.append(F[i, :3] + j + h * .42); Sz.append(s * .72); Vl.append(h); Sd.append(R[i, k] + .13 * k)
    P, Sz, Vl, Sd = np.vstack(P), np.hstack(Sz), np.vstack(Vl), np.hstack(Sd); o = np.argsort(-((P - cam.eye) ** 2).sum(1)); za = (P[o] - cam.eye) @ cam.R[2]; FX.particles(st, P[o], Sz[o], gain, 'tongue', seed=Sd[o] % 1, vel=Vl[o], alpha=np.clip((za - near) / near, 0, 1), fog=.00016, fogCol=(.16, .03, .012)); return len(o)


def smoke(st, now, cam, n=200, a=.55):
    """after close, before the flames: dark smoke lit from under"""
    F, T, R = fire_points(); age = now - T; c = (F[:, :3] - cam.eye) @ cam.R.T; z = c[:, 2]; m = (age > .4) & (z > 130) & (np.abs(c[:, 0]) * cam.fl < z * 2.0 + 80) & (c[:, 1] * cam.fl < z * 1.2) & (c[:, 1] * cam.fl > -z * 2.2); i = np.flatnonzero(m)
    if len(i) == 0: return
    if len(i) > n: i = i[np.argsort(R[i, 4])[:n]]
    lf = (now * (.30 + .2 * R[i, 0]) + R[i, 1]) % 1.; k = np.clip((age[i] - .4) / .8, 0, 1); s = F[i, 3] * (1.0 + 2.6 * lf) * k; P = F[i, :3] + np.c_[20 * np.sin(R[i, 2] * 40 + lf * 4) * lf + 46 * lf, F[i, 3] * 1.4 + 150 * lf, 14 * np.cos(R[i, 3] * 40 + lf * 3) * lf]
    col = np.array([.30, .060, .020]) * ((1 - lf) ** 2)[:, None] + np.array([.020, .010, .018]); o = np.argsort(-((P - cam.eye) ** 2).sum(1)); FX.particles(st, P[o], s[o], col[o], 'smoke', seed=R[i, 4][o], alpha=(np.minimum(1, lf * 5) * (1 - lf) ** .8 * a * k)[o], rot=0.)


# ------------------------------------------------------------------ the people of the city, very small
def folk():
    if 'folk' in _C: return _C['folk']
    r = np.random.default_rng(12); P, D, Lm = [], [], []
    while len(P) < 460:
        x, z = r.uniform(-640, 330), r.uniform(150, 960); j, i = cell(x, z); A, B = lay(); y = roof_y(x, z)
        if abs(y - B[j, i][2]) > .5 or y < 1: continue
        e = 6.; g = arr(np.array([(x + e, 0, z), (x - e, 0, z), (x, 0, z + e), (x, 0, z - e)])); d = V(g[0] - g[1], 0, g[2] - g[3]); d = nz(d + V(*(r.normal(0, .25) * q for q in (1, 0, 1))) * np.linalg.norm(d)) if np.linalg.norm(d) > 1e-6 else V(1, 0, 0); L = 0.
        while L < 110 and abs(roof_y(x + d[0] * (L + 4), z + d[2] * (L + 4)) - y) < .5: L += 4
        P.append((x, y, z)); D.append(d); Lm.append(L)
    P, D = np.array(P), np.array(D); _C['folk'] = (P, D, np.array(Lm), arr(P), r.uniform(0, 1, (len(P), 3))); return _C['folk']


def folk_at(now):
    P, D, L, T, R = folk(); go = np.clip(now - (T - .75 - .5 * R[:, 0]), 0, None); s = np.minimum(L, (34 + 22 * R[:, 1]) * go); Q = P + D * s[:, None] + D * (2.5 * np.sin(now * 1.7 + R[:, 2] * 40) * (go <= 0))[:, None]; return Q, D, (go > 0) & (s < L - .1), R, T
