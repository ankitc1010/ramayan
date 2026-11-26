"""E, the bridge: a work song in eight. Every stone is a drum; one name sinks, and will not stay down."""
from core import *
from voice import *
from inst import *
from perc import *


def under(b):
    """Everything between the splash and the surfacing is heard through water; it opens as the stone comes up."""
    a, c = fr('e1', 42) * FR, fr('e1', 84) * FR
    s0 = (ACT0['E'] - 24) * FR
    t = np.arange(len(b)) + s0
    f = np.interp(t, [a - 400, a + 900, fr('e1', 72) * FR, c - FR, c], [18000, 260, 380, 1500, 18000])
    i, j = a - 400 - s0, c + 2000 - s0
    out = b.copy()
    for k in (0, 1):
        y = sweep(sweep(b[i - 4800:j, k], f[i - 4800:j], .8, 'low'), f[i - 4800:j], .7, 'low')[4800:]
        w = np.ones(len(y)); w[:200] = np.linspace(0, 1, 200); w[-1500:] = np.linspace(1, 0, 1500)
        out[i:j, k] = y * w * np.interp(t[i:j], [a, c - 2 * FR, c], [1.5, 1.5, 1.]) + out[i:j, k] * (1 - w)
    return out


def voice(P):
    M = P.layer('men', lufs=-16, sends=dict(open=.35, cathedral=.22), low=75, fx=under, dry=.9)
    sa = SA / 2
    choir(M, lyric("raam=S:1.5@0.82+R:.5@0.82 naam=S:2@0.82 raam=S:1.5@0.87+G:.5@0.87 naam=R:2@0.82 | raam=G:2@0.92 naam=R:2@0.92 raam=G:1@1.00+P:1@1.00", fr('e1', 0), sa), 'm', 12, seed=1, rd=1.05, attack=.05)
    choir(M, lyric("raam=S:2@0.82 naam=S,:2@0.82 raam=S:2@0.87 naam=P,:2@0.82 | raam=S:2@0.92 naam=R:2@0.92 raam=S:1@1.00+R:1@1.00", fr('e1', 0), sa), 'm', 8, seed=2, rd=1.05, attack=.05, g=.7)
    choir(M, lyric("naam=P:2@1", fr('e1', 84), sa), 'm', 10, seed=3, attack=.03, rd=.85)
    resp = "_:4 raam=S':1.5@1+R':.5@1 naam=S':2@1 | _:4 raam=G':1@1+R':1@1 naam=S':2@1"
    choir(M, lyric(resp, fr('e2', 0), sa), 'm', 14, seed=4, rd=.85, attack=.03); choir(M, lyric("_:4 raam=P:2@1 naam=P:2@1 | _:4 raam=S':1@1+P:1@1 naam=P:2@1", fr('e2', 0), sa), 'm', 8, seed=5, rd=.85, attack=.03, g=.8)
    choir(M, lyric(resp, fr('e2', 0), SA), 'f', 8, seed=6, rd=.95, attack=.03, g=.75)
    L = P.layer('call', lufs=-18, sends=dict(close=.2, hall=.25, open=.2), low=90, fx=under, eq=((2800, 2, 1.2),))
    solo(L, LEADM, lyric("raam=S':2@1 naam=S':1@.95+D:1@.9 _:4 | raam=S':.5@1+R':.5@1+G':1@1 naam=R':1@.95+S':1@.9", fr('e2', 0), sa), release=.2)
    solo(L, LEAD, lyric("_:4 raam=S':1@.8+P:1@.8 naam=D:2@.75", fr('e2', 48)), release=.3, g=.6)


def melodic(P):
    L = P.layer('flute', lufs=-23, sends=dict(open=.4), p=.3, fx=under)
    bansuri(L, notes("S':1 R':.5 S':.5 D:1 P:1 | G:.5 P:.5 D:1 S':2 | S':.5 D:.5 P:1 G:1 P:1", fr('e1', 0)), seed=1, g=.6)
    bansuri(L, notes("G':.5 R':.5 S':1 R':.5 S':.5 D:1 | S':.5 R':.5 G':1 P':2 | G':.5 R':.5 S':1 D:.5 S':.5 R':1 | G':1 P':1 S'':2", fr('e2', 0)), seed=2, raga=(0, 204, 386, 702, 884), flutter=.2)
    S = P.layer('strum', lufs=-23, sends=dict(close=.3, open=.2), p=-.3, fx=under)
    line(S, notes(" ".join("S:.5 P:.5 S':.5 P:.5 D:.5 P:.5 G:.5 P:.5".split() * 3), fr('e1', 0), sa=SA), 'sarod', seed=3, ring=.35)
    line(S, notes(" ".join("S:.5 P:.5 S':.5 P:.5 D:.5 P:.5 G:.5 P:.5 m:.5 D:.5 S':.5 D:.5 S:.5 P:.5 S':.5 P:.5".split() * 2), fr('e2', 0), sa=SA), 'sarod', seed=4, ring=.35)
    B = P.layer('bass', lufs=-21, sends=dict(close=.3), low=38, fx=under)
    line(B, notes("S,:1.5 S,:.5 P,:2 | S,:1.5 S,:.5 D,,:2 | S,:1.5 S,:.5 P,:1.5", fr('e1', 0)), 'veena', seed=5, ring=.6); line(B, notes("S,:1.5 S,:.5 P,:1 S,:1 | m,,:1.5 m,,:.5 S,:2 | S,:1.5 S,:.5 D,,:2 | m,,:1 P,,:1 S,:2", fr('e2', 0)), 'veena', seed=6, ring=.6)
    G = P.layer('glow', mom=-27, sends=dict(cave=.8)); G.at(bell(hz("S'"), 3.5, 4, .2, 3), fr('e1', 60), .5); swarmandal(G, "S G P S' G'", fr('e1', 61), dt=.07, g=.4, seed=4)
    H = P.layer('open', lufs=-19, sends=dict(hall=.4)); horns(H, notes("P:2@1", fr('e1', 84), sa=SA / 2), 4, seed=7, attack=.02, release=.1)
    horns(H, notes("S':4@.8 m:2@.7 S':2@.8 | S':4@.85 m:1@.8 P:1@.85 S':2@.9", fr('e2', 0), sa=SA / 2), 4, seed=8, attack=.05, release=.15, g=.8)


def drums(P):
    L = P.layer('stones', lufs=-17, sends=dict(open=.4), fx=under)
    beat(L, "S...T...S..TT...", fr('e1', 0), 3, 2, seed=1, width=.5, upto=fr('e1', 82))
    for k in range(16):
        f = fr('e2', 6 * k)
        L.at(stone((190, 300, 230, 360)[k % 4] * (1 + .03 * (k % 3)), 1. if k % 2 == 0 else .75, k % 6, .9 if k % 2 == 0 else .4), f, 1. if k % 2 == 0 else .7, (-.6, .4, -.2, .7, -.4, .1, .6, -.7)[k % 8])
    beat(L, "..T.T.TT..T.TTT.", fr('e2', 0), 3, 2, seed=2, g=.4, width=.8)
    D = P.layer('dholak', lufs=-19, sends=dict(close=.3, open=.2), p=.1, fx=under)
    beat(D, "M.nnu.ncm.nnM.nc", fr('e1', 0), 3, 2, seed=3, upto=fr('e1', 82)); beat(D, "M+.nnu.ncM.nnMnnc", fr('e2', 0), 3, 2, seed=4); beat(D, "H...h.h.H.h.H.hh", fr('e2', 0), 3, 2, seed=5, g=.8, width=.4)
    C = P.layer('claps', lufs=-25, sends=dict(open=.5), fx=under); beat(C, "..C...C.", fr('e1', 0), 6, 1, seed=6, width=.8, upto=fr('e1', 42)); beat(C, "..C...C.", fr('e2', 0), 6, 2, seed=7, width=.8); beat(C, "..C...C.", fr('e2', 0), 6, 2, seed=8, width=.8, human=.012)
    W = P.layer('war', lufs=-20, sends=dict(open=.4)); W.at(war(44, .95, 1), fr('e1', 84), 1.); W.at(dhol('dha', 1.), fr('e1', 84), .6); roll(W, 'w', fr('e1', 86), fr('e2', 0), 3, 2, .5, .9, seed=9, g=.5); beat(W, "W...w...W..w.w..", fr('e2', 0), 3, 2, seed=10, g=.9)
    J = P.layer('manjira', lufs=-33, sends=dict(open=.3), p=.4, fx=under); beat(J, "jJJJ", fr('e2', 0), 6, 4, seed=11); beat(J, "jJJJ", fr('e1', 0), 6, 3, seed=12, g=.6)


def pads(P):
    L = P.layer('strings', lufs=-23, sends=dict(hall=.4), fx=under)
    strings(L, notes("S,:4@.6 S,:4@.6 | S,:3@.6 P,:2@.8", fr('e1', 0)), 'cello', 6, seed=1, attack=.1, release=.2)
    strings(L, notes("G:4@.5 P:3@.5 | G:3@.4 R:4@.5", fr('e1', 0)), 'violin', 5, seed=2, attack=.3, release=.3, g=.7)
    strings(L, notes("G':2@.9 D:1@.9 S':1@.9 | D:2@.9 S':2@.95 | G':2@.95 R':1 S':1 | D:1@1 N:1@1 S':2@1", fr('e2', 0)), 'violin', 8, seed=3, attack=.03, release=.2)
    strings(L, notes("S,:4@.9 m,:2 S,:2 | S,:2 D,:2 m,:1 P,:1 S,:2", fr('e2', 0)), 'cello', 7, seed=4, attack=.04, release=.2)
    strings(L, notes("P:4@.7 D:2 P:2 | P:4@.8 D:1 N:1 P:2", fr('e2', 0)), 'violin', 6, seed=5, attack=.1, release=.3, p=.4, g=.8)
    U = P.layer('deep', lufs=-26, sends=dict(cave=.6), low=30); e = drone(hz('S,') / 2, 1.9, 3, .35); U.at(fades(e, .15, .4), fr('e1', 43))
