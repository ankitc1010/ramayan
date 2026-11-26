"""D, the carrier: seven beats, 3+2+2, in Hamsadhwani (S R G P N); one drop to a burning city."""
from core import *
from voice import *
from inst import *
from perc import *

HAM = (0, 204, 386, 702, 1088)
RAMA = lambda a, b, c, v=.8: f"raa={a}:2@{v} ma={a}:1@{v * .85:.2f} raa={b}:1@{v} ma={b}:1@{v * .85:.2f} raa={c}:1@{v} ma={c}:1@{v * .85:.2f}"
OST = "S:.5 G:.5 P:.5 N:.5 P:.5 G:.5 | R:.5 P:.5 N:.5 P:.5 | G:.5 P:.5 N:.5 R':.5"
F0 = fr('d1')


def bar(k): return F0 + 42 * k


def voice(P):
    L = P.layer('lead', lufs=-20, sends=dict(close=.3, hall=.32), low=110, eq=((300, -2, 1.), (3200, 2, 1.2)))
    solo(L, Singer('f', 1., rd=1.5, breath=.035, vib=(5., 22), glide=1.5, seed=31), lyric("lau=S:1@.45+G:1@.5 jaa=P:1@.55 gii=N^:1.6@.6+P:1@.5", fr('d1', 48)), breathin=.7, release=.3, g=.7, raga=HAM)
    solo(L, LEAD, lyric("si=G:1@.5 yaa=P:1@.55+D:.5@.55+P:2.5~@.55".replace("2.5~", "2.5"), fr('d6', 8)), breathin=.7, release=.4, g=.75)
    solo(L, LEAD, lyric("lau=P^:1@.6+D:1@.6+S':2@.65+D:1@.55+P:1@.5", fr('d6', 44)), breathin=.6, release=.5, g=.8)
    M = P.layer('men', lufs=-17.5, sends=dict(cathedral=.4, hall=.35), low=75, dry=.8)
    sa = SA / 2
    choir(M, lyric(RAMA('S', 'S', 'S', .45), bar(2), sa), 'm', 12, seed=1, rd=1.5, attack=.05)
    choir(M, lyric(RAMA('S', 'S', 'R', .6), bar(3), sa), 'm', 12, seed=2, rd=1.3, attack=.05)
    choir(M, lyric(RAMA('P', 'P', 'P', .6), bar(3), sa), 'm', 8, seed=3, rd=1.3, attack=.05, g=.8)
    choir(M, lyric("raa=S:2@.7 ma=S:1@.6 raa=R:1@.75 ma=R:1@.7 raa=G:1@.85", bar(4), sa), 'm', 12, seed=4, rd=1.1, attack=.05)
    choir(M, lyric("raa=P:2@.7 ma=P:1@.6 raa=P:1@.75 ma=N:1@.7 raa=N:1@.85", bar(4), sa), 'm', 8, seed=5, rd=1.1, attack=.05, g=.8)
    for k, (a, b, c) in enumerate((("S'", "S'", "N"), ("S'", "N", "S'"), ("G'", "R'", "S'"))):
        choir(M, lyric(RAMA(a, b, c, 1.), bar(5 + k), sa), 'm', 12, seed=6 + k, rd=.85, attack=.03)
        choir(M, lyric(RAMA('S', 'P', 'P', 1.), bar(5 + k), sa), 'm', 8, seed=16 + k, rd=.85, attack=.03, g=.8)
    W = P.layer('women', lufs=-18, sends=dict(cathedral=.4, hall=.35), low=150, dry=.8)
    choir(W, lyric("raa=P:2@.6 ma=N:1@.6 raa=S':2@.8 ma=R':1@.85", bar(4)), 'f', 8, seed=20, attack=.2)
    choir(W, lyric("raa=G':3@1 ma=R':1@.9 raa=S':1@.95 ma=R':1@.9 raa=N:1@.9 | ma=S':2@.95 raa=R':1@.95 ma=S':1@.9 raa=N:1@.9 ma=P:1@.85 raa=N:1@.85 | ma=R':3@.95 raa=G':2@1 ma=S':2@.9", bar(5)), 'f', 10, seed=21, rd=.95, attack=.04)
    choir(W, lyric("raa=P:3@1 ma=P:1@.9 raa=G:1@.95 ma=P:1@.9 raa=P:1@.9 | ma=G:2@.95 raa=P:1@.95 ma=G:1@.9 raa=P:1@.9 ma=R:1@.85 raa=P:1@.85 | ma=P:3@.95 raa=P:2@1 ma=G:2@.9", bar(5)), 'f', 8, seed=22, rd=.95, attack=.04, g=.8)
    K = P.layer('chuckle', mom=-27, sends=dict(cave=.6, hall=.3), low=55, high=2600, dry=.6)
    s1, t, sy = Singer('m', .84, rd=.7, breath=.05, vib=(6, 8), jit=.012, shim=.06, drift=15, ring=.2, seed=77), sec(fr('d7', 8)), []
    for k in range(5): sy.append(('ha', [(t, t + .12, hz('S,,') * 1.5 * 2 ** (-k * .7 / 12), '', .8 - .09 * k)])); t += .19
    y, t0 = s1.sing(sy, seed=7, attack=.02, release=.1, cons=.3); K.add(y, t0, 1., 0.)
    X = P.layer('jali', lufs=-14.5, sends=dict(cathedral=.42, hall=.3), low=85, dry=.85)
    up = "ja=P:1@1 lii=S':2@1 ja=N:1@1 lii=S':1@1 _:2 | lau=G':2@1+R':1@1 ja=R':1@1 lii=S':3@1 | ja=S':1@1 lii=R':2@1 ja=R':1@1 lii=G':1@1 lau=R':1@1+G':1@1 | "
    lo = "ja=G:1@1 lii=P:2@1 ja=P:1@1 lii=P:1@1 _:2 | lau=S':2@1+N:1@1 ja=N:1@1 lii=P:3@1 | ja=P:.5@1 lii=N:2.5@1 ja=N:.5@1 lii=S':1.5@1 lau=N:1@1+S':1@1 | "
    choir(X, lyric(up, fr('d8', 0)), 'f', 12, seed=30, rd=.85, attack=.03, release=.12); choir(X, lyric(lo, fr('d8', 0)), 'f', 8, seed=31, rd=.85, attack=.03, release=.12, g=.8)
    choir(X, lyric(up, fr('d8', 0)), 'm', 12, seed=32, octave=-1, rd=.75, attack=.03, release=.12); choir(X, lyric(lo, fr('d8', 0)), 'm', 8, seed=33, octave=-1, rd=.75, attack=.03, release=.12, g=.8)
    for k, (d, o, kd, n) in enumerate((("S'", 0, 'f', 8), ("P", 0, 'f', 6), ("G", 0, 'f', 5), ("S", -1, 'm', 8), ("P", -1, 'm', 6))):
        choir(X, lyric(f"lau={d}:6.5@.75", fr('d8', 126)), kd, n, seed=40 + k, octave=o, attack=.12, release=1.2, g=.75)


def melodic(P):
    L = P.layer('spark', mom=-30, sends=dict(hall=.7)); L.at(course(hz("P'"), 3, .3, t60=5, seed=1), fr('d1', 42), 1.); L.at(bell(hz("N'"), 3, 3, .15, 2), fr('d1', 42), .2)
    L = P.layer('flight flute', lufs=-19, sends=dict(hall=.4), p=.25)
    bansuri(L, notes("S':.5 R':.5 G':1 R':.5 S':.5 | N:.5 S':.5 R':1 | P:1 N:1 | S':.5 N:.5 P:1 G:1 | P:.5 N:.5 S':1 | R':2", bar(6)), seed=3, flutter=.2, raga=HAM)
    bansuri(L, notes(" ".join(f"{d}:.25" for d in "S' R' G' P' G' R' S' N S' R' S' N P N P G P N S' R'".split()), fr('d4', 84)), seed=4, glide=.5, raga=HAM)
    bansuri(L, notes("S':.33 R':.33 G'^:1.3 P':1", fr('d7', 47)), seed=5, g=.8, flutter=.4, raga=HAM)
    K = P.layer('sitar flight', lufs=-22, sends=dict(close=.3, hall=.25), p=-.3)
    for k in (5, 6): line(K, notes(OST, bar(k) if k > 5 else bar(5), sa=SA), 'sitar', seed=6 + k, ring=.5)
    line(K, notes(OST, bar(8) - 0, sa=SA), 'sitar', seed=15, ring=.5, g=.8)
    B = P.layer('brass', lufs=-18, sends=dict(hall=.45), low=45)
    horns(B, notes("S:2@.5 R:1@.55 G:1@.65 P:1@.75 N:1@.9", bar(4), sa=SA / 2), 4, seed=20, attack=.15, release=.06)
    horns(B, notes("S':3@1 N:2@.9 P:2@.9 | S':2@.9 R':1@.9 S':2@.9 P:2@.9 | G':3@1 R':2@.95 S':2@.9", bar(5), sa=SA / 2), 5, seed=21, attack=.02, release=.12)
    horns(B, notes("S,:3@1 r,:1@1", fr('d4', 66)), 4, seed=22, attack=.05, release=.2, kind='low', growl=.35)
    horns(B, notes("S:3@1 P:2@.95 N:2@.95 | S':3@1 N:2@.95 P:2@.95 | R':3@1 S':2@.95 G':2@1", fr('d8', 0), sa=SA / 2), 5, seed=23, attack=.02, release=.12)
    V = P.layer('veena', lufs=-25, sends=dict(hall=.45), p=-.15)
    line(V, notes("_:3 P,:3 S:2 | R~:2 G:3 Rv:1 S:2", fr('d5', 12)), 'veena', seed=30, ring=2., g=.7)
    line(V, notes("S:1.5 G:1.5 P:2 | S:1.5 R:.5 G:1 | S':1 P:2 | G:1 Rv:1 S:2", fr('d6', 0)), 'veena', seed=31, ring=1.8, g=.8)
    X = P.layer('ring', mom=-25, sends=dict(hall=.7)); X.at(bell(hz("G'"), 3.5, 4, .25, 7), fr('d6', 36), .5); swarmandal(X, "S G P S' G' P'", fr('d6', 37), dt=.06, g=.5, seed=8)
    G = P.layer('glimmer', mom=-23, sends=dict(hall=.6)); swarmandal(G, "S' R' G' P' N' S'' R''", fr('d4', 108), dt=.05, g=.8, seed=9)
    T = P.layer('tanpura', lufs=-33, sends=dict(hall=.3)); tanpura(T, fr('d5', 10), fr('d6', 76))
    C = P.layer('conch', lufs=-18, sends=dict(open=.5), p=.3); C.at(conch(293.66, 1.6, 3), fr('d3', 42)); C.at(conch(220.2, 1.6, 4), fr('d3', 48), .6, -.4); C.at(conch(293.66, 1.8, 5), fr('d8', 0), .8)


def drums(P):
    up = lambda f: float(np.clip(.35 + .6 * (f - bar(2)) / 130, .35, 1))
    L = P.layer('frames', lufs=-20, sends=dict(open=.4, hall=.2))
    beat(L, "F.f-.f.F.f.F.f-f-", bar(2), 3, 2, seed=1, vel=up, width=.4); beat(L, "F.f.ffF.ffF.ff", bar(2), 3, 2, seed=2, vel=lambda f: up(f) * .7, p=.4, width=.3)
    beat(L, "FfffffFfffFf", bar(4), 3, 1, seed=3, vel=up, width=.4)
    roll(L, 'w', bar(4), fr('d3', 36), 3, 1.2, .25, 1., seed=4)
    W = P.layer('leap', mom=-13, sends=dict(cathedral=.3, hall=.3), low=26); ensemble(W, lambda i: war(38 + 3 * i, 1., i, hard=.9), fr('d3', 42), 6); W.at(gong(64, 5, .2, .9, 4), fr('d3', 42), .2)
    B = P.layer('flight', lufs=-17, sends=dict(open=.45))
    beat(B, "W+.w.w.W.w.W.ww", bar(5), 3, 3, seed=5, width=.15); beat(B, "H+.hhB.H.hhHhhh", bar(5), 3, 3, seed=6, g=.9, width=.4); beat(B, "j.J.J.j.J.j.J.", bar(5), 3, 3, seed=7, g=.22, p=.4)
    ensemble(B, lambda i: war(36 + 4 * i, 1., i, hard=.9), fr('d4', 66), 4, g=1.3); B.at(gong(60, 3, .2, .7, 5), fr('d4', 66), .2)
    beat(B, "W..w.wW.w.WwWw", fr('d4', 66), 1.5, 1, seed=8, g=.8)
    N = P.layer('night', mom=-30, sends=dict(hall=.6)); N.at(frame('doum', v=.6), fr('d5', 48)); N.at(frame('doum', v=.4, var=1), fr('d5', 66), .5)
    H = P.layer('hall', lufs=-23, sends=dict(stone=.5), low=28)
    beat(H, "W-.....w-...w-...", fr('d7', 0), 3, 1, seed=9, upto=fr('d7', 42)); beat(H, "W..w..W.w.W.w.", fr('d7', 42), 3, 1, seed=10, upto=fr('d7', 66)); beat(H, "F.f.f.F.f.F.f.", fr('d7', 30), 3, 1, seed=11, g=.6, upto=fr('d7', 64))
    X = P.layer('bursts', mom=-18, sends=dict(stone=.5)); X.at(war(52, .8, 1, hard=.6), fr('d7', 30), .6); X.at(war(42, 1., 2, hard=.9), fr('d7', 66)); X.at(dhol('dha', 1., 1), fr('d7', 66), .7)
    roll(X, 'h', fr('d7', 69), fr('d8', 0), 3, 1.5, .4, 1., seed=12, g=.5)
    D = P.layer('fire', lufs=-14.5, sends=dict(open=.45))
    beat(D, "W+.wwW.W.wwW.ww", fr('d8', 0), 3, 3, seed=13, width=.15); beat(D, "H+hhHhhHhhhHhHh", fr('d8', 0), 3, 3, seed=14, width=.5, g=.9); beat(D, "N.o.ooN.ooN.oo", fr('d8', 0), 3, 3, seed=15, width=.6, g=.7); beat(D, "C.....C...C...", fr('d8', 0), 3, 3, seed=16, g=.5, width=.8); beat(D, "j.J.J.j.J.j.J.", fr('d8', 0), 3, 3, seed=17, g=.25, p=-.4)
    D.at(war(40, 1., 3, hard=.8), fr('d8', 126), 1.); D.at(gong(60, 6, .4, .6, 6), fr('d8', 126), .15)


def pads(P):
    L = P.layer('wake', lufs=-31, sends=dict(hall=.6), low=30)
    e = drone(hz('S,') / 2, 2.2, 1, .4); L.at(fades(e, .5, .5), fr('d1', 42)); strings(L, notes("S':3@.15 S':3@.25", fr('d1', 46)), 'violin', 3, seed=2, g=.6, attack=1., release=.4)
    S = P.layer('ostinato', lufs=-20, sends=dict(hall=.35))
    for k, v in ((2, .35), (3, .55), (4, .75)): strings(S, notes(" ".join(x if x == '|' else x + f"@{v}" for x in OST.split()), bar(k)) if k < 4 else notes(" ".join(x if x == '|' else x + f"@{v}" for x in OST.split()[:12]), bar(4)), 'cello' if k < 4 else 'violin', 8, seed=3 + k, attack=.03, release=.04, loose=.006, g=v)
    for k in (5, 6, 7): strings(S, notes(" ".join(x if x == '|' else x + "@.95" for x in OST.split()), bar(k)), 'violin', 8, seed=3 + k, attack=.02, release=.04, loose=.006, p=-.3); strings(S, notes(" ".join(x if x == '|' else x + "@.9" for x in OST.split()), bar(k), sa=SA / 2), 'cello', 6, seed=13 + k, attack=.02, release=.04, loose=.006, p=.35)
    H = P.layer('soar', lufs=-19, sends=dict(hall=.5))
    strings(H, notes("G':3@1 R':1 S':1 R':1 N:1 | S':2 R':1 S':1 N:1 P:1 N:1 | R':3 G':2 S':2 | N:1 P':2@.8 N':2@.7 S'':2@.5", bar(5), sa=SA), 'violin', 8, seed=20, attack=.05, release=.3, swell=.15, raga=HAM)
    strings(H, notes("S,:3@1 P,,:2 N,,:2 | S,:2 G,:3 P,:2 | R,:3 P,:2 S,:2 | S,:4@.8 P,:3@.6", bar(5)), 'cello', 8, seed=21, attack=.04, release=.3)
    strings(H, notes("S,:3@.9 S,:4@.9 | S,:3@.9 S,:4@.9 | P,,:3@.9 S,:4@.9 | S,:7@.6", bar(5), sa=SA / 2), 'cello', 5, seed=22, attack=.04, release=.4)
    N = P.layer('night', lufs=-28, sends=dict(hall=.7))
    strings(N, notes("P':6@.2 N':8@.25", fr('d5', 4)), 'violin', 4, seed=30, p=-.4, attack=1.2, release=1.2); strings(N, notes("S,:7@.4 P,,:7@.4", fr('d5', 4)), 'cello', 5, seed=31, attack=1., release=1.); strings(N, notes("R:7@.22 G:7@.25", fr('d5', 4)), 'violin', 4, seed=32, p=.4, attack=1.2, release=1.2)
    G = P.layer('warm', lufs=-27, sends=dict(hall=.6))
    strings(G, notes("S,:6@.35 S,:4@.55 D,,:4@.5", fr('d6', 0)), 'cello', 6, seed=40, attack=.8, release=.8); strings(G, notes("G:4@.5 G:4@.45", fr('d6', 36)), 'violin', 6, seed=41, p=-.3, attack=.3, release=.8); strings(G, notes("P:4@.5 R:4@.45", fr('d6', 36)), 'violin', 5, seed=42, p=.3, attack=.3, release=.8)
    C = P.layer('court', lufs=-23, sends=dict(stone=.4, hall=.3), low=35)
    strings(C, notes("S,:.5@.6 _:.5 S,:.5 _:.5 r,:.5 _:.5 S,:.5 _:.5 S,:.5 _:.5 M,:.5 _:.5 P,:.5 _:.5 " * 1, fr('d7', 0)), 'cello', 8, seed=50, attack=.02, release=.05, loose=.006); strings(C, notes("S,:.5@.8 S,:.5 r,:.5 S,:.5 M,:.5 S,:.5 P,:.5 S,:.5", fr('d7', 42)), 'cello', 8, seed=51, attack=.02, release=.05, loose=.006)
    strings(C, notes("S:3@.4 r:3@.65 P:1@.8", fr('d7', 30)), 'violin', 8, seed=52, attack=.05, release=.1, trem=10, g=.7); strings(C, notes(" ".join(f"{d}:.25@{.6 + .05 * i:.2f}" for i, d in enumerate("S R G P N S' R' G'".split())), fr('d7', 72)), 'violin', 8, seed=53, attack=.02, release=.05, loose=.005)
    Q = P.layer('blaze', lufs=-18, sends=dict(hall=.45))
    for k in range(3): strings(Q, notes(" ".join(x if x == '|' else x + "@1" for x in OST.split()), fr('d8', 42 * k)), 'violin', 8, seed=60 + k, attack=.02, release=.04, loose=.006, p=-.3); strings(Q, notes(" ".join(x if x == '|' else x + "@.95" for x in OST.split()), fr('d8', 42 * k), sa=SA / 2), 'cello', 6, seed=70 + k, attack=.02, release=.04, loose=.006, p=.3)
    strings(Q, notes("S':3@1 S':2 N:2 | G':3 R':1 S':3 | R':3 R':2 G':2", fr('d8', 0), sa=SA * 2), 'violin', 8, seed=80, attack=.03, release=.2, g=.6)
    for k, (d, kd, g) in enumerate((("S'", 'violin', .8), ("P", 'violin', .7), ("G", 'violin', .6), ("S,", 'cello', 1.), ("P,", 'cello', .8))): strings(Q, notes(f"{d}:6.5@.5", fr('d8', 126)), kd, 6, seed=90 + k, attack=.15, release=1.2, g=g, p=(-.4, .4, 0, .2, -.2)[k])
    strings(Q, notes("S,:6.5@.6", fr('d8', 126), sa=SA / 2), 'cello', 5, seed=99, attack=.15, release=1.2)
