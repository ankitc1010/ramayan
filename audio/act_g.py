"""G, home: six beats, Bhoopali, the theme complete; every house, every heart; a child; a breath; one string."""
from core import *
from voice import *
from inst import *
from perc import *

ONE = "ghar=S:1@.75 ghar=R:1@.8 lau=G:2.5@.85+P:.5@.85+G:1@.85 | man=P:1@.85 man=D:1@.88 lau=P:1.5@.88+D:.5@.85+P:.5@.8+G:1.5@.8"
TWO = "ghar=D:1@.85 ghar=S':1@.9 lau=R':2.5@.95+G':.5@.95+R':.5@.9+S':.5@.9 | man=G':1@.95 man=R':1@.95 lau=S':2@.95+R':1@.9+S':1@.9 | lau=D:2@.85+S':1@.85+D:1@.85+P:2@.8"
HOME = "ek=S:1@.75+G:1@.8 lau=P^:3@.9+D:1@.9 cha=S':1@.92 lii=R':1.5@.95+S':.5@.92+D:1@.9 ghar=S':1@.95 aa=R':2@.98+S':.5@.98+R':.5@1 ii=G':5.6@1"


def voice(P):
    L = P.layer('lead', lufs=-18.5, sends=dict(close=.3, hall=.27), low=110, eq=((300, -2, 1.), (3200, 2, 1.2)))
    solo(L, LEAD, lyric(ONE, fr('g2', 0)), g=1.15, breathin=1., release=.4)
    solo(L, LEAD, lyric("hum=P:1@.5+D:.5@.5+P:.5@.5+G:2@.5", fr('g2', 72)), release=.4, g=.4)
    solo(L, LEAD, lyric(TWO, fr('g3', 0)), breathin=.8, release=.3)
    solo(L, LEAD, lyric(HOME, fr('g4', 0)), breathin=.8, release=.9)
    C = P.layer('chorus', lufs=-18.5, sends=dict(cathedral=.45, hall=.35), low=85, dry=.78)
    choir(C, lyric("oo=G:4@.5 oo=G:2@.5 | oo=m:3@.55 oo=R:3@.55 | oo=G:4@.5", fr('g2', 0)), 'f', 8, seed=1, attack=.5, release=.6, g=.45, rd=1.5); choir(C, lyric("oo=S:4@.5 oo=D,:2@.5 | oo=D,:3@.55 oo=P,:3@.55 | oo=S:4@.5", fr('g2', 0)), 'm', 8, seed=2, octave=0, attack=.5, release=.6, g=.4, rd=1.4)
    lo = "ghar=m:1@.85 ghar=m:1@.9 lau=P:2.5@.95+N:.5@.95+P:1@.9 | man=S':1@.95 man=P:1@.95 lau=D:2@.95+P:2@.9 | lau=m:2@.85+m:1@.85+m:1@.85+R:2@.8"
    choir(C, lyric(TWO, fr('g3', 0)), 'f', 14, seed=3, attack=.08, release=.3); choir(C, lyric(lo, fr('g3', 0)), 'f', 8, seed=4, attack=.08, release=.3, g=.8)
    choir(C, lyric(TWO, fr('g3', 0)), 'm', 10, seed=5, octave=-1, attack=.08, release=.3, g=.8); choir(C, lyric("ghar=m,:1@.85 ghar=m,:1@.9 lau=P,:4@.95 | man=D,:1@.95 man=P,:1@.95 lau=m,:2@.95+P,:2@.9 | lau=m,:4@.85+P,:2@.8", fr('g3', 0)), 'm', 10, seed=6, attack=.08, release=.3, g=.8)
    choir(C, lyric("_:2 lau=S':3@.8+S':1@.8 cha=S':1@.85 lii=D:3@.85 ghar=D:1@.9 aa=R':3@.95 ii=P':5.8@1", fr('g4', 0)), 'f', 8, seed=7, attack=.15, release=1., g=.8)
    choir(C, lyric(HOME, fr('g4', 0)), 'f', 12, seed=8, attack=.1, release=1.); choir(C, lyric("_:2 lau=G:3@.85+m:1@.85 cha=m:1@.9 lii=m:3@.9 ghar=m:1@.95 aa=P:3@.98 ii=S':5.8@1", fr('g4', 0)), 'f', 8, seed=9, attack=.12, release=1., g=.8)
    choir(C, lyric(HOME, fr('g4', 0)), 'm', 12, seed=10, octave=-1, attack=.1, release=1., g=.9); choir(C, lyric("_:2 lau=S,:3@.85+m,:1@.85 cha=m,:1@.9 lii=D,:3@.9 ghar=m,:1@.95 aa=P,:3@.98 ii=S,:5.8@1", fr('g4', 0)), 'm', 10, seed=11, attack=.12, release=1.); choir(C, lyric("_:14 ii=P,:5.8@1", fr('g4', 0)), 'm', 8, seed=12, attack=.1, release=1., g=.8)
    K = P.layer('child', lufs=-23, sends=dict(close=.3, hall=.3), low=150)
    solo(K, CHILD, lyric("ek=S:1@.6+G:1@.65 lau=P:2.5@.7+D:1@.65+P:1@.65+G:2.4@.55", fr('g5', 18)), breathin=.6, release=.5)


def melodic(P):
    T = P.layer('tanpura', lufs=-30, sends=dict(hall=.25)); tanpura(T, fr('g1', 0), fr('g5', 66), g=1.)
    Z = P.layer('last string', mom=-24, sends=dict(hall=.35), low=50)
    from inst import _tanpura_string, body
    Z.at(body(_tanpura_string(hz('S,'), 1, 6.5), 'gourd'), fr('g5', 90), 1.); Z.at(body(_tanpura_string(hz('S'), 0, 6.5), 'gourd'), fr('g5', 120), .75)
    L = P.layer('bansuri', lufs=-22, sends=dict(hall=.45), p=.2)
    bansuri(L, notes("_:2 S:1 G:1 P^:3 D:1 P:1 G:2 R:1", fr('g1', 0)), seed=1, g=1., breath=.12)
    bansuri(L, notes("_:12 S':.5 R':.5 G':1 R':.5 S':.5 D:1", fr('g2', 0)), seed=2, g=.8)
    bansuri(L, notes("_:4 S':.5 D:.5 P:1 _:4 G':.5 R':.5 S':1 _:2 P:1 D:1 S':2", fr('g3', 0)), seed=3, g=.6)
    bansuri(L, notes("_:14 G':.5 P':.5 S'':1.5 P':.5 G':1 R':.5 S':1.5", fr('g4', 0)), seed=4, g=.6)
    V = P.layer('veena', lufs=-24, sends=dict(close=.2, hall=.3), p=-.2, low=45)
    line(V, notes("S,:3 P,:3 D,:3 P,:3", fr('g1', 0)), 'veena', seed=5, ring=1.2, g=.7)
    line(V, notes("S,:1 P,:1 S:1 G:1 S:1 P,:1 | m,,:1 D,:1 S:1 P,,:1 R,:1 P,:1 | S,:1 P,:1 S:1 P,:1", fr('g2', 0)), 'veena', seed=6, ring=.8)
    line(V, notes("m,,:1 D,:1 S:1 P,,:1 R,:1 P,:1 | D,,:1 P,:1 D,:1 m,,:1 D,:1 S:1 | m,,:1 D,:1 S:1 P,,:1 R,:1 P,:1", fr('g3', 0)), 'veena', seed=7, ring=.8)
    line(V, notes("S,:1 P,:1 S:1 G:1 S:1 m,,:1 m,:1 D,:1 m,:1 D,,:1 m,,:1 P,,:1 R,:1 P,:1 S,:1 P,:1 S:1 G:1 P:1 S':1", fr('g4', 0)), 'veena', seed=8, ring=1.)
    S = P.layer('santoor', lufs=-25, sends=dict(hall=.45), p=-.3)
    arp = lambda c: " ".join(f"{d}:.5@{.8 if i % 2 == 0 else .55}" for i, d in enumerate(c.split()))
    santoor(S, notes(arp("S G P S' P G S P G S' P G D S' m' S' D m P R' P' R' N P S G P S' P G S P"), fr('g2', 0)), seed=9, g=.8)
    santoor(S, notes(arp("m D S' m' S' D P N R' P' R' N D S' G' D' G' S' m D S' m' S' D m D S' m' S' D P N R' P' R' N"), fr('g3', 0)), seed=10)
    santoor(S, notes(arp("S G P S' P G S P G S' m D S' m' S' D m D D S' G' S' m D P N R' P' R' N"), fr('g4', 0)), seed=11)
    swarmandal(S, "S, P, S R G P D S' R' G' P' S''", fr('g4', 84), dt=.05, g=1.2, seed=12); swarmandal(S, "S R G P D S' R' G'", fr('g3', 0) - 4, dt=.03, g=.7, seed=13)
    B = P.layer('bells', lufs=-27, sends=dict(hall=.7, cathedral=.2))
    B.at(bell(hz("P'"), 3., 3.5, .2, 1), fr('g1', 24), .4)
    for k, (f, d) in enumerate(((84, "S'"), (90, "P'"), (96, "G'"), (102, "S''"), (108, "P'"))): B.at(bell(hz(d), 4, 4.5, .35, 2 + k), fr('g4', f), (1., .5, .45, .4, .3)[k], (0, -.5, .5, -.3, .3)[k])
    B.at(bell(hz("S"), 5, 6, .3, 8), fr('g4', 84), .9)
    for k in range(4): B.at(bell(hz(("S'", "P'", "G'", "R'")[k]), 2.5, 3, .25, 20 + k), fr('g3', (0, 36, 60, 84)[k]), .35)
    H = P.layer('horns', lufs=-21, sends=dict(hall=.5)); horns(H, notes("P:3@.6 N:1.5 P:1.5 | S':2@.7 D:2 P:2 | m:4@.7 P:2", fr('g3', 0), sa=SA / 2), 4, seed=14, attack=.15, release=.3, g=.8); horns(H, notes("_:2 S:4@.6 m:4@.7 m:1@.75 P:3@.85 S':5.5@.95", fr('g4', 0), sa=SA / 2), 4, seed=15, attack=.12, release=.8)


def drums(P):
    L = P.layer('tabla', lufs=-24, sends=dict(close=.4, hall=.2), p=.1)
    beat(L, "X-.d-.D-.G-.d-.D-.", fr('g2', 0), 3, 2, seed=1, width=.08); beat(L, "X.Dtd.G.", fr('g2', 72), 3, 1, seed=2, width=.08)
    beat(L, "X.Y-.D.G.d-.Dt-", fr('g3', 0), 3, 3, seed=3, width=.08); beat(L, "X.Y-.D.G.d-.Dt-", fr('g4', 0), 3, 2, seed=4, width=.08); beat(L, "X.DtDtXtDtDt", fr('g4', 72), 3, 1, seed=5, width=.08, upto=fr('g4', 84)); beat(L, "X...D-...Y-...d-..", fr('g4', 84), 3, 1, seed=6, width=.08)
    D = P.layer('dholak', lufs=-24, sends=dict(open=.3, hall=.2), p=-.15)
    beat(D, "M.n-c-n.u.n-c-nc-", fr('g3', 0), 3, 3, seed=7); beat(D, "M.n-c-n.u.n-c-nc-", fr('g4', 0), 3, 2, seed=8)
    J = P.layer('manjira', lufs=-35, sends=dict(hall=.4), p=.35); beat(J, "j-.J-.J-.", fr('g2', 48), 6, 1, seed=9, upto=fr('g3')); beat(J, "jJ-J-jJ-J-", fr('g3', 0), 6, 3, seed=10); beat(J, "jJ-J-jJ-J-", fr('g4', 0), 6, 2, seed=11)
    W = P.layer('deep', lufs=-23, sends=dict(hall=.5), low=28)
    for s, f, v in (('g3', 0, .6), ('g3', 36, .5), ('g3', 72, .55), ('g4', 0, .5), ('g4', 36, .6), ('g4', 60, .65)): W.at(war(42, v, 1, hard=.2), fr(s, f), v)
    roll(W, 'w', fr('g4', 62), fr('g4', 84), 3, 1.5, .1, .7, seed=12, g=.5); ensemble(W, lambda i: war(40 + 3 * i, .9, i, hard=.35), fr('g4', 84), 4, g=1.2); W.at(gong(73.4, 6, .5, .35, 3), fr('g4', 84), .12)


def pads(P):
    L = P.layer('strings', lufs=-23, sends=dict(hall=.55))
    strings(L, notes("_:3 S,:4@.3 D,:3@.35 P,:2@.35", fr('g1', 0)), 'cello', 5, seed=1, attack=.6, release=.5); strings(L, notes("_:4 G:3@.2 R:3@.25 N,:2@.25", fr('g1', 0)), 'violin', 4, seed=2, attack=.7, release=.5, g=.7)
    for k, (d, kd, p, g) in enumerate((("G:4@.4 G:2 m:3@.45 R:3 G:4@.45", 'violin', -.4, .7), ("S:4@.4 D,:2 D,:3 N,:3 S:4", 'violin', .4, .6), ("P,:4@.4 P,:2 m,:3 P,:3 P,:4", 'cello', .2, .7), ("S,:4@.45 D,,:2 m,,:3 P,,:3 S,:4", 'cello', 0, .9))): strings(L, notes(d, fr('g2', 0)), kd, 6, seed=3 + k, p=p, g=g, attack=.35, release=.4)
    for k, (d, kd, p, g) in enumerate((("D:2@.7 R':4@.75 G':2@.75 S':4@.75 D:4@.75 P:2@.7", 'violin', -.4, 1.), ("m:2@.7 P:4 D:2 m:4 m:4 R:2", 'violin', .4, .8), ("S:2@.7 N,:4 S:2 S:4 D,:4 N,:2", 'cello', .25, .8), ("m,:2@.7 P,,:4 D,,:2 m,:4 m,:4 P,,:2", 'cello', 0, 1.))): strings(L, notes(d, fr('g3', 0)), kd, 7, seed=10 + k, p=p, g=g, attack=.12, release=.3)
    for k, (d, kd, p, g) in enumerate((("G:2@.6 P:3@.7 D:1 S':4@.8 S':1 R':3@.9 G':6@1", 'violin', -.4, 1.), ("S:2@.6 G:3@.7 m:1 m:4@.8 m:1 N:3@.9 P:6@.95", 'violin', .4, .8), ("P,:2@.6 S:3@.7 D,:1 D,:4@.8 D,:1 R:3@.9 S:6@.95", 'cello', .25, .8), ("S,:5@.6 m,,:1 m,,:2 D,,:2@.8 m,,:1 P,,:3@.9 S,:6@1", 'cello', 0, 1.), ("_:10 S':1@.6 P':3@.7 P':6@.8", 'violin', 0, .6))): strings(L, notes(d, fr('g4', 0)), kd, 8, seed=20 + k, p=p, g=g, attack=.12, release=1.2)
    strings(L, notes("S,:6@.6", fr('g4', 84), sa=SA / 2), 'cello', 5, seed=30, attack=.1, release=1.2)
    strings(L, notes("_:1 S,:6@.18 P,:5@.15", fr('g5', 6)), 'cello', 3, seed=31, attack=.8, release=.8, g=.8)
