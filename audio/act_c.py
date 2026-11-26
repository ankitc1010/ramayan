"""C, the golden deer: Yaman shimmer, the chase, the line of fire, Shree rising head by head, earth, wings, rain."""
from core import *
from voice import *
from inst import *
from perc import *

SHREE = (0, 112, 386, 590, 702, 814, 1088)
SHIV = (0, 204, 316, 702, 884)


def voice(P):
    L = P.layer('rain voice', lufs=-25, sends=dict(close=.2, hall=.5, cathedral=.2), low=110, eq=((3200, 1.5, 1.2),))
    soft = Singer('f', 1., rd=1.75, breath=.045, vib=(4.9, 20), glide=1.5, seed=21)
    solo(L, soft, lyric("lau=P:1.5@.5+D:.5@.45+P:1@.5 bu=g~:1@.45 jhii=R:1.5@.42+S:2@.36", fr('c7', 12)), breathin=1.2, release=.5, raga=SHIV)
    C = P.layer('cry', mom=-24, sends=dict(cave=.7, open=.5), dry=.35, low=150, high=4200)
    solo(C, Singer('m', 1.02, rd=.75, breath=.03, vib=(5.5, 40), glide=2.2, seed=22), lyric("haa=D:.6@1+P:1.2@.95+g:.8@.75+S:1.2@.5", fr('c2', 36)), release=.5)
    C = P.layer('far cry', mom=-31, sends=dict(cave=1., open=.8), dry=.15, low=200, high=2600)
    solo(C, Singer('m', 1.02, rd=.75, breath=.03, vib=(5.5, 40), glide=2.2, seed=24), lyric("haa=P:1.2@.9+g:.7@.8+S:1.4@.5", fr('c3', 33)), release=.5)
    M = P.layer('shree men', lufs=-21, sends=dict(cathedral=.6, hall=.3), low=60, dry=.7)
    f = fr('c4', 0)
    choir(M, lyric("oo=S,:5@.4 oo=S,:5@.5 au=r,:3@.7 aa=r,:2@.9", f + 2), 'm', 8, seed=1, attack=1.2, release=.1, raga=SHREE)
    choir(M, lyric("oo=P,:5@.3 oo=P,:5@.5 au=d,:3@.7 aa=d,:2@.9", f + 2, sa=SA), 'm', 6, seed=2, attack=1.2, release=.1, raga=SHREE, g=.8)
    choir(M, lyric("aa=M:3@.5+P:3@.7+N:1.7@1", f + 48), 'f', 6, seed=3, attack=1., release=.1, g=.5, raga=SHREE)
    choir(M, lyric("haa=S,:3@1+r,:1@1 haa=M,:4@1+S,:2@.8", fr('c5', 0)), 'm', 10, seed=4, attack=.05, release=.5, rd=.75, raga=SHREE)
    choir(M, lyric("haa=S:1@1 haa=S:1@1 haa=r:2@1 haa=M:2@1", fr('c6', 24)), 'm', 8, seed=5, octave=-1, attack=.03, release=.1, rd=.7, g=.6, raga=SHREE)


def melodic(P):
    L = P.layer('deer', lufs=-21, sends=dict(hall=.55), p=-.1)
    up = "N, R G M D N R' G' M' G' R' N D M G R".split(); dn = "G' N D M G M D N R' N D N R' G' M' D'".split()
    f = fr('c1', 0)
    for k in range(40):
        d = (up if k < 16 else dn if k < 32 else up)[k % 16]; t = f + 1.5 * k
        if t >= fr('c1', 60): break
        L.at(course(hz(d), 1.6, .5 + .2 * (k % 4 == 0), seed=k, t60=2.2), t, (.9 if k % 4 == 0 else .5) * (.6 + .4 * min(1, k / 16)), -.35 + .7 * ((k * 5) % 8) / 8)
    swarmandal(L, "N, R G M D N R' G' M' D' N'", fr('c1', 36), dt=.022, g=1.2, seed=2, ring=2.5)
    L.at(bell(hz("N'"), 3, 3, .6, 5), fr('c1', 42), .7)
    V = P.layer('deer sitar', lufs=-24, sends=dict(hall=.4), p=.25)
    line(V, notes("N,:1 R:.5 G~:2 M:.5 G:1 R:1 | G:1 Mv:.5 Dv:1.5 N~:2", fr('c1', 0)), 'sitar', seed=3, ring=1.)
    B = P.layer('fall', lufs=-20, sends=dict(hall=.6, open=.3), low=180)
    t0, t1 = fr('c6', 60), fr('c6', 96)                                                                            # one long falling note
    bansuri(B, [(sec(t0), sec(t0 + 4), hz("S''"), '', 1.), (sec(t0 + 4), sec(t0 + 9), hz("N'"), '', .9), (sec(t0 + 9), sec(t0 + 14), hz("P'"), '', .85), (sec(t0 + 14), sec(t0 + 20), hz("M'"), '', .8), (sec(t0 + 20), sec(t0 + 27), hz("r'"), '', .7), (sec(t0 + 27), sec(t1 + 2), hz("S'"), '~', .55)], glide=4., seed=1, release=.5)
    H = P.layer('brass', lufs=-18, sends=dict(hall=.5), low=45)
    for k, d in enumerate("S, r, G, M, P, d, N, S r M".split()):                                                    # ten heads fan open
        horns(H, [(sec(fr('c5', 2 * k)), sec(fr('c5', 23)), hz(d) / 1, '', .5 + .05 * k)], 2, g=.6, p=.14 * (k - 4.5), seed=30 + k, attack=.02, release=.06)
    horns(H, notes("S,:4@1 r,:2@.9", fr('c5', 24), sa=SA / 2), 5, g=1.2, seed=45, attack=.02, release=.4, kind='low', growl=.25)
    horns(H, notes("S:.5 S:.5 r:1 S:.5 S:.5 M:1 r:1 S:1", fr('c6', 24), sa=SA / 2), 4, g=.9, seed=46, attack=.02, release=.1, growl=.15)
    K = P.layer('chase', lufs=-20, sends=dict(close=.4, hall=.2), p=.2)
    line(K, notes(" ".join(f"{d}:.5" for d in "S S r S G S M G P M G r S r G M".split()), fr('c2', 0)), 'sarod', seed=50, ring=.25)
    X = P.layer('she looks', mom=-27, sends=dict(hall=.8)); X.at(bell(hz("r''"), 2.5, 2.5, .2, 9), fr('c4', 78), .6)
    Y = P.layer('rain veena', lufs=-29, sends=dict(hall=.5), p=-.2)
    line(Y, notes("S,:3 P,:2 g,:2 R,:2 S,:3", fr('c7', 6)), 'veena', seed=60, ring=1.6)
    Z = P.layer('gold burst', mom=-22, sends=dict(hall=.5)); swarmandal(Z, "S'' P' M' G' r' S' N P M G r S", fr('c2', 30), dt=.03, seed=61, ring=1.5)


def drums(P):
    L = P.layer('chase', lufs=-19, sends=dict(open=.35))
    beat(L, "M.ncn.M.n.cn", fr('c2', 0), 2, 1, seed=1); beat(L, "F.f.F.ff.f.f", fr('c2', 0), 2, 1, seed=2, g=.8, p=.3)
    beat(L, "M.nn", fr('c2', 24), 1.5, 1, seed=3)
    roll(L, 'm', fr('c2', 12), fr('c2', 24), 2, 1, .4, .9, seed=4)
    Z = P.layer('leap', mom=-25, sends=dict(hall=.5)); Z.at(frame('doum', v=.8, jingle=1.), fr('c1', 36)); Z.at(manjira(3300, .9, 1., 1), fr('c1', 36), .3); Z.at(manjira(3700, .9, 1., 2), fr('c1', 42), .25)
    X = P.layer('struck', mom=-14, sends=dict(open=.4, hall=.3)); X.at(war(48, 1., 1, hard=.8), fr('c2', 30)); X.at(dhol('dha', 1.), fr('c2', 24), .5)
    G = P.layer('ten heads', lufs=-17, sends=dict(cave=.45, hall=.3), low=26)
    for k in range(10):
        f = fr('c4', 36 + 6 * k); v = .5 + .05 * k
        G.at(war(44 - k * .4, round(v, 2), k % 4, hard=.35), f, v); G.at(gong(58 + 1.3 * k, 3., .3, .4 + .05 * k, k), f, .10 + .016 * k, .12 * (k - 4.5))
    E = P.layer('earth', lufs=-14.5, sends=dict(open=.4, hall=.35), low=26)
    for k in range(10): E.at(nagara(round(.5 + .05 * k, 2), k % 4, 80 + 7 * k), fr('c5', 2 * k), .4 + .05 * k, .12 * (k - 4.5))
    ensemble(E, lambda i: war(40 + 3 * i, 1., i, hard=.8), fr('c5', 24), 5); roll(E, 'w', fr('c5', 28), fr('c5', 60), 3, 2, .6, .9, seed=6, g=.7)
    F = P.layer('fight', lufs=-15, sends=dict(open=.4))
    beat(F, "W+.w.ww W.w.ww", fr('c6', 24), 3, 1, seed=7); beat(F, "H.hhB.HhhHhh", fr('c6', 24), 3, 1, seed=8, g=.8, width=.3)
    roll(F, 'w', fr('c6', 6), fr('c6', 24), 3, 1.5, .2, .9, seed=9, g=.7)
    F.at(war(40, 1., 2, hard=1.), fr('c6', 60), 1.2)
    S = P.layer('line', mom=-18, sends=dict(open=.4)); S.at(war(50, .9, 1, hard=.8), fr('c3', 18)); S.at(frame('tek', v=1.), fr('c3', 18), .7); S.at(war(42, .5, 2, hard=.1), fr('c4', 90), 1.1)


def pads(P):
    L = P.layer('gold air', lufs=-28, sends=dict(hall=.7))
    strings(L, notes("N:6@.4 R':4@.5", fr('c1', 0)), 'violin', 6, seed=1, p=-.4, attack=.5, release=.4); strings(L, notes("G':6@.35 M':4@.45", fr('c1', 0)), 'violin', 5, seed=2, p=.4, attack=.6, release=.4); strings(L, notes("N,:6@.4 G:4@.45", fr('c1', 0)), 'cello', 4, seed=3, attack=.5, release=.4)
    L = P.layer('run', lufs=-22, sends=dict(hall=.35))
    strings(L, notes(" ".join(f"{d}:.5@{v}" for d, v in zip("S r S G S r S M S r S G P M G r".split(), [.9, .6] * 8)), fr('c2', 0)), 'violin', 8, seed=4, attack=.02, release=.06, loose=.006)
    strings(L, notes("S,:5@.5 S,:5@.35", fr('c2', 0)), 'cello', 6, seed=5, attack=.05, release=.4, g=.8)
    strings(L, notes("r:1@.4 r:3.5@.3", fr('c2', 33)), 'violin', 5, seed=6, attack=.4, release=.4, g=.5, trem=8)
    B = P.layer('line of fire', lufs=-21, sends=dict(hall=.45))
    strings(B, notes("S,:3@.45 r,:2.9@.95 G,:1.1@.7 r,:1@.5", fr('c3', 0)), 'cello', 8, seed=7, attack=.15, release=.3, raga=SHREE)
    strings(B, notes("M:.7@.9 P:.7@.9 d:.8@.85 N:.8@.75 S':2@.5", fr('c3', 18)), 'violin', 8, seed=8, attack=.02, release=.4, trem=11, g=.8, raga=SHREE)
    W = P.layer('shree', lufs=-20, sends=dict(hall=.5, cathedral=.3), low=32)
    f = fr('c4', 0)
    for k, (d, kd, p, g) in enumerate((("S,:15.1@.9", 'cello', 0, 1.), ("r:6@.3 r:9.1@.9", 'violin', -.5, .6), ("P,:6@.3 M,:9.1@.9", 'cello', .4, .8), ("N:9@.25 d:3@.6 N:3.1@.95", 'violin', .5, .5))):
        strings(W, notes(d, f), kd, 6, seed=20 + k, p=p, g=g, attack=3.2, release=.05, trem=7 if kd == 'violin' else 0, raga=SHREE)
    e = drone(hz('S,') / 2, 4.2, 5, .7); e *= np.linspace(.1, 1, len(e)) ** 1.5; W.at(fades(e[:ns(sec(91.5))], .5, .05), f, 1.4)
    R = P.layer('red sky', lufs=-21, sends=dict(hall=.5))
    strings(R, notes("S':4@.9 r':2@.9", fr('c5', 24)), 'violin', 8, seed=30, attack=.02, release=.3, trem=10, p=-.3); strings(R, notes("M:4@.9 P:2@.9", fr('c5', 24)), 'violin', 6, seed=31, attack=.02, release=.3, trem=9, p=.4); strings(R, notes("S,:4@1 r,:2@1", fr('c5', 24)), 'cello', 6, seed=32, attack=.02, release=.3)
    strings(R, notes("P:.5 M:.5 G:.5 M:.5 P:.5 d:.5 N:.5 S':.5 r':.5 S':.5 N:.5 d:.5 " + "S' N d P M G r S N, S r G ".replace(' ', ':.25 ').strip() + " M:3@.7", fr('c6', 0)), 'violin', 8, seed=33, attack=.02, release=.05, loose=.007, raga=SHREE)
    strings(R, notes("S,:4@.8 S,:6@.9", fr('c6', 0)), 'cello', 6, seed=34, attack=.3, release=.04)
    N = P.layer('rain', lufs=-29, sends=dict(hall=.7))
    strings(N, notes("S:3@.35 g:3@.4 R:3@.35 S:1.5@.25", fr('c7', 4)), 'cello', 2, seed=40, attack=.6, release=.6, raga=SHIV, tune=3); strings(N, notes("g:3@.2 P:3@.25 P:3@.2 g:2@.15", fr('c7', 4)), 'violin', 2, seed=41, attack=.8, release=.6, g=.6, raga=SHIV, tune=3)
