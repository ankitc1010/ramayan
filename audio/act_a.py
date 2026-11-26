"""A, the lamp: darkness, tanpura, alap; the shadow theatre; sunrise in Bhoopali; the bow; the wedding."""
from core import *
from voice import *
from inst import *
from perc import *
import perc

TOY = ("S:.5 R:.5 G:1 P:.5 G:.5 R:1 S:.5 R:.5 D,:1 | S:1 R:1 G:1 P:1 D:.5 P:.5 G:.5 R:.5 | S:.5 R:.5 G:.5 P:.5 D:.5 S':.5")


def voice(P):
    L = P.layer('lead', lufs=-19, sends=dict(close=.3, hall=.27), low=110, eq=((300, -2, 1.), (3200, 2, 1.2)))
    solo(L, LEAD, lyric("hum=D,:1.5@.5+S:1.5@.55+R:1@.5+G~:3@.6+R:1@.5+S:3@.45", fr('a2', 8)), g=.75, release=.4)
    solo(L, LEAD, lyric("ek=S:1@.75+G:1@.85 lau=P^:3+D:1 ja=P:1 lii=G:2+R:1+G:2.2@.85", fr('a3', 12)), breathin=1., release=.35)
    solo(L, LEAD, lyric("ek=S:1@.6+G:1@.65 lau=P^:1.5@.72+D:.5@.7+S':1@.75 mi=D:.5@.7 lii=P:1@.65+G:1@.6+R:.5@.55+S:1.2@.5", fr('a5', 18)), breathin=.8, release=.3, g=.8)
    C = P.layer('chorus', lufs=-23, sends=dict(cathedral=.5, hall=.3), low=140, dry=.75)
    up = fr('a3', 24)
    for k, ln in enumerate(("aa=P:4.3@.9+D:1@.8+P:4@.6", "aa=G:5.3@.9+R:1@.8+G:3@.6", "aa=S:4.3@.9+D,:1@.8+S:4@.6")): choir(C, lyric(ln, up - 1), 'f', 5, seed=k, attack=.25, release=.6)
    choir(C, lyric("aa=S:4.3@.9+D,:2@.8+S:3@.6", up - 1), 'm', 6, seed=9, octave=-1, attack=.25, release=.6)
    choir(C, lyric("aa=S,:6@.25+S,:5@.6+P,:3@.95", fr('a4', 0)), 'm', 8, seed=11, attack=1.6, release=.05, g=1.1)
    choir(C, lyric("aa=R:3@.4+G:3@.6+M:2@.85+P:2@1", fr('a4', 18)), 'f', 6, seed=12, attack=1.2, release=.05, g=.8)


def melodic(P):
    r = rng('a')
    L = P.layer('tanpura', lufs=-31, sends=dict(hall=.25))
    tanpura(L, 36, 320, g=1., r=r); tanpura(L, 358, 426, g=.9, start=1)
    L = P.layer('bloom', mom=-25, sends=dict(hall=.6))
    swarmandal(L, "S P D S' R' G' P' S''", 36, dt=.055, g=.8, seed=3)
    L.at(bell(1174.7, 4, 4, .2, 1), 36, .28)
    L.at(course(587.33, 3.5, .4, t60=5, seed=8), 36, .9)
    L = P.layer('bansuri', lufs=-24, sends=dict(hall=.5))
    bansuri(L, notes("D,:.7 S:2.3 R:.6 G~:3.2 R:1 S:2.4", 44), seed=1, breath=.12)
    bansuri(L, notes("_:3 S:1 R:1 G:1 P~:4 D:1 P:2 G:2", fr('a2', 60) - 6), g=.5, seed=2)
    bansuri(L, notes("S':2 D:1 S':1 R':2 S':2 D:1 P:3", fr('a3', 26)), g=.55, seed=3)
    bansuri(L, notes("G:1 R:.5 G:.5 P:1", fr('a5', 0)), g=.5, seed=4)
    B = P.layer('sunrise', mom=-21, sends=dict(hall=.6)); B.at(bell(587.33, 4.5, 5, .5, 4), fr('a3', 24), 1.); B.at(course(587.33, 3, .7, seed=9), fr('a3', 24), .8); B.at(course(440.5, 3, .7, seed=10), fr('a3', 24), .6)
    L = P.layer('toy', lufs=-25, sends=dict(theatre=.5), p=-.15)
    line(L, notes(TOY, fr('a2', 0)), 'toy', seed=1, ring=.5)
    line(L, notes("S':.5 P:.25 G:.25 R:.5 S:1.5", fr('a2', 90)), 'toy', seed=2, ring=.6, human=.0)
    santoor(L, notes(TOY, fr('a2', 0), sa=SA * 2), g=.18, seed=4, hard=.3, p=.35, ring=.7)
    L = P.layer('veena', lufs=-25, sends=dict(hall=.4), p=.12)
    line(L, notes("S,:2 P,:1 D,:1 | S:2 D,:1 P,:1", fr('a3', 24)), 'veena', seed=5, g=.8)
    line(L, notes("S:1 P,:1 D,:1 | D,:1 S:1 R:1 G:1 | S:1.5 P,:1.5", fr('a5', 0)), 'veena', seed=6, g=.75)
    S = P.layer('santoor', lufs=-27, sends=dict(hall=.5), p=-.2)
    santoor(S, notes("S':.5 P:.5 D:.5 S':.5 R':.5 S':.5 G':.5 R':.5 S':.5 D:.5 P:.5 D:.5 S':.5 D:.5 P:.5 G:.5", fr('a3', 24)), seed=7, hard=.5)
    santoor(S, notes("G:1 P:1 S':1 | D:.5 P:.5 G:1 R:1", fr('a5', 30)), seed=8, hard=.35, g=.7)
    swarmandal(S, "S R G P D S' R' G' P'", fr('a3', 21), dt=.014, g=1.1, seed=9)
    swarmandal(S, "S R G P D S' R' G'", fr('a5', 58), dt=.05, g=.6, seed=10)


def drums(P):
    L = P.layer('theatre drums', lufs=-25, sends=dict(theatre=.6), p=.1)
    beat(L, "M.n-c-n.u.n-c-nc-", fr('a2', 0), 3, 2, seed=1)
    beat(L, "M.ncn.u.ncnc M.......", fr('a2', 72), 3, 1, seed=2, upto=fr('a2', 90))
    L.at(dholak('dum', 1., 1), fr('a2', 90), 1.); L.at(dholak('na', 1., 1), fr('a2', 90), .8)
    M = P.layer('manjira', lufs=-36, sends=dict(theatre=.5), p=.3)
    beat(M, "j-...J-.j-...J-.", fr('a2', 0), 3, 1, seed=3); beat(M, "j-.J-.J-.", fr('a2', 36), 6, 1, seed=4)
    B = P.layer('pakhawaj', lufs=-20, sends=dict(stone=.5), p=-.05)
    up = lambda f: np.clip(.45 + .55 * (f - fr('a4')) / 78, .4, 1)
    beat(B, "P..q..g.qK..", fr('a4', 0), 3, 1, seed=5, vel=up)
    beat(B, "P.qKg.P.qKgq", fr('a4', 36), 3, 1, seed=6, vel=up, upto=fr('a4', 72))
    roll(B, 'P', fr('a4', 60), fr('a4', 78), 2, 1, .6, 1., g=.8, seed=7)
    W = P.layer('war', lufs=-23, sends=dict(hall=.5))
    for k, f in enumerate((0, 18, 36, 48, 60, 66, 72, 75)): W.at(war(46, round(.35 + .6 * f / 78, 2), k % 3), fr('a4', f), .4 + .6 * f / 78)
    W.at(war(40, .9, 1, hard=.5), fr('a3', 24), .9)
    X = P.layer('break', mom=-11.5, sends=dict(cathedral=.35, hall=.3))
    X.at(war(38, 1., 0, hard=1., rim=1.), fr('a4', 84)); X.at(gong(58, 6, .25, .8, 2), fr('a4', 84), .25); X.at(nagara(1., 1, 70.), fr('a4', 84), .6)


def pads(P):
    L = P.layer('strings', lufs=-23, sends=dict(hall=.55), eq=((300, -1.5, 1.),))
    f = fr('a3', 4)
    for k, (d, g) in enumerate((("S,", .9), ("P,", .7), ("S", .6), ("G", .5))):
        strings(L, notes(f"{d}:3.4@.35", f), 'cello' if "," in d else 'violin', 5, g=g, p=(-.4, .3, -.2, .5)[k], seed=k, attack=.7, release=.2, width=.4)
    up = fr('a3', 24)
    strings(L, notes("G':4@.9 D:1 S':3@.85 D:2@.7 P:1.5@.5", up - 1), 'violin', 8, g=1., p=-.4, seed=10, attack=.06, swell=.3)
    strings(L, notes("P:4@.9 D:2@.8 P:3@.6", up - 1), 'violin', 6, g=.7, p=.3, seed=11, attack=.06)
    strings(L, notes("S:3@.9 D,:3@.8 P,:3@.6", up - 1), 'cello', 5, g=.8, p=.4, seed=12, attack=.06)
    strings(L, notes("S,:3@.9 D,:3@.8 S,:3@.6", up - 1, sa=SA / 2), 'cello', 4, g=.9, p=.1, seed=13, attack=.06)
    T = P.layer('tension', lufs=-22, sends=dict(hall=.5))
    strings(T, notes("S:6@.2 S:3@.4 R:2@.6 G:2@.8", fr('a4', 0)), 'violin', 8, g=.8, p=-.3, seed=20, attack=1.2, release=.03, trem=9)
    strings(T, notes("P,:6@.25 D,:3@.5 N,:2@.7 S:2@.95", fr('a4', 0)), 'cello', 6, g=.9, p=.3, seed=21, attack=1., release=.03, trem=8)
    strings(T, notes("S,:13@.5", fr('a4', 0), sa=SA / 2), 'cello', 5, g=1., p=0, seed=22, attack=1.5, release=.03, swell=.8)
    horns(T, notes("S,:3@.5 P,:3@.65 S:3@.8 R:2@.95", fr('a4', 12)), 4, g=.5, seed=23, attack=.5, release=.04)
    E = P.layer('tender', lufs=-25, sends=dict(hall=.6))
    for k, (seq, kd, p, g) in enumerate((("G:5@.5 D:3@.6 D:2.5@.6 P:1.5@.5", 'violin', -.4, .7), ("P:5@.5 G:3@.6 m:2.5@.6 N:1.5@.5", 'violin', .4, .6), ("S:5@.5 D,:3@.6 m,:2.5@.6 P,:1.5@.5", 'cello', .2, .8))):
        strings(E, notes(seq, fr('a5', 0)), kd, 6, g=g, p=p, seed=30 + k, attack=.4, release=.4)
