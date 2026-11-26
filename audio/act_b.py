"""B, the forest: coronation cut dead; two boons; the walk out; fourteen years as one walking song; a lullaby."""
from core import *
from voice import *
from inst import *
from perc import *
import cues

SONG = "van=S:1+R:1 cha=G:1 lii=P^:2+G:1 | van=D:1+P:1 cha=G:1 lii=R:2+S:1 | sang=G:1+P:1 cha=D:1 lii=P:1+G:.5+R:.5+S:1"


def voice(P):
    L = P.layer('lead', lufs=-19, sends=dict(close=.3, hall=.25), low=110, eq=((300, -2, 1.), (3200, 2, 1.2)))
    solo(L, LEAD, lyric(SONG, fr('b3', 0)), breathin=.7, release=.3)
    solo(L, LEAD, lyric("hum=P:1@.45+D:.5@.45+P:.5@.45+G~:2@.5+R:.7@.4+S:1.6@.35", fr('b4', 2)), release=.5, g=.95)
    C = P.layer('men', lufs=-27, sends=dict(cathedral=.5, hall=.3), low=90, dry=.7)
    choir(C, lyric("oo=S:6@.8", fr('b1', 0) - 1), 'm', 6, seed=1, attack=.12, release=.05)
    choir(C, lyric("oo=P,:4@.5+d,:3@.5+P,:4@.35", fr('b2', 10), sa=SA), 'm', 6, seed=2, attack=.6, release=.8, g=.5)
    choir(C, lyric("sang=G:1+P:1 cha=D:1 lii=P:1+G:.5+R:.5+S:1", fr('b3', 72)), 'm', 5, seed=3, octave=-1, g=.7)


def melodic(P):
    L = P.layer('conch', lufs=-19, sends=dict(stone=.5), p=-.3)
    L.at(conch(220.2, 1.5, 1), fr('b1', 0)); L.at(conch(293.66, 1.3, 2), fr('b1', 6), .7, .4)
    L = P.layer('fanfare', lufs=-20, sends=dict(stone=.5))
    horns(L, notes("S:1 P:1 S':1 P:.5 S':.5 G':2", fr('b1', 0), sa=SA / 2), 5, seed=3, attack=.03, release=.04)
    L = P.layer('boons', mom=-24, sends=dict(hall=.6, stone=.3))
    for f, d, s in ((42, 'S,', 1), (54, 'r,', 2)):
        L.at(pluck(hz(d), 3.2, 'veena', 1., s), fr('b1', f)); L.at(bell(hz(d) * 2, 3., 3., .25, s), fr('b1', f), .18); L.at(pluck(hz(d) / 2, 3., 'sarod', 1., s + 5), fr('b1', f), .7)
    L = P.layer('bass', lufs=-25, sends=dict(stone=.4), low=40)
    for k, d in enumerate("S, S, P,, S, d,, d,, P,, P,, r, S, P,, S,".split()):
        L.at(pluck(hz(d), 1.4, 'sarod', .8, k), fr('b2', 6 * k), (1., .6)[k % 2] * (1 - .03 * k), .0)
    L = P.layer('lamps out', lufs=-25, sends=dict(stone=.6))
    outs = sorted(set(cues.frames('b2', 'puff')))
    down = "S' n d P g r".split() if len(outs) <= 8 else "S'' n' d' P' m' g' r' S' n d P m g r S n, d, P, m, g, r, S,".split()
    for k, f in enumerate(outs):                                                                                   # one lamp, one small fall
        drop = lambda t, q=k: 2 ** (-(3 + q % 3) * np.clip((t - .07) / .28, 0, 1) ** .8 / 12)
        L.at(pluck(hz(down[min(k, len(down) - 1)]), 1.0, 'veena', .7, 20 + k, drop), fr('b2', f), .95 - .01 * k, .7 * (-1) ** k * (1 - k / len(outs)))
    L = P.layer('bansuri', lufs=-23, sends=dict(hall=.45), p=.2)
    bansuri(L, notes("S:1 R:1 G:1 P:1.5", fr('b3', 0), sa=SA * 2), g=.6, seed=1)                                    # spring, above
    bansuri(L, notes("_:4.5 P,:.5 D,:1 P,:1.5 R:1.5", fr('b3', 0)), g=.8, seed=2, breath=.16)                          # monsoon, low and wet
    bansuri(L, notes("_:9 G:.5 P:.5 G:1 R:1 S:1.5", fr('b3', 0)), g=.6, seed=3)
    bansuri(L, notes("G:2 R:1 S:2.5", fr('b4', 2)), g=.5, seed=4)
    L = P.layer('santoor', lufs=-25, sends=dict(hall=.4), p=-.25)
    santoor(L, notes("S':.5 G':.5 P':.5 G':.5 R':.5 P':.5 S':.5 D:.5 S'.5".replace("S'.5", "S':.5"), fr('b3', 0)), seed=5, hard=.6)         # spring
    swarmandal(L, "P' G' R' S' D P G R S", fr('b3', 27), dt=.05, g=1.1, seed=6)
    santoor(L, notes("_:4.5 S':.75 P:.75 D:.75 P:.75 G:.75 R:.75", fr('b3', 0)), seed=7, hard=.3, g=.5)
    K = P.layer('autumn', lufs=-26, sends=dict(theatre=.3), p=.3)
    line(K, notes("_:9 S:.5 R:.5 G:.5 P:.5 D:.5 P:.5 G:.5 R:.5 G:.5", fr('b3', 0)), 'toy', seed=8, ring=.5)
    W = P.layer('winter', lufs=-27, sends=dict(hall=.8), p=0)
    for k, (f, d) in enumerate(((81, "S''"), (84, "P'"), (87, "R''"), (90, "S''"), (93, "D'"), (96, "P'"), (99, "G'"), (102, "S''"), (105, "P'"))): W.at(bell(hz(d), 1.8, 2., .15, k), fr('b3', f), .5 + .2 * (k % 3), .5 * (-1) ** k)
    V = P.layer('walking bass', lufs=-24, sends=dict(close=.4), low=45)
    line(V, notes("S,:1 P,:1 S:1 S,:1 D,:1 P,:1 | D,,:1 P,:1 D,:1 m,,:1 D,,:1 R,:1 | P,,:1 R,:1 P,:1 S,:1 P,:1 S,:1", fr('b3', 0)), 'veena', seed=9, ring=.5)
    L = P.layer('tanpura', lufs=-32, sends=dict(hall=.2))
    tanpura(L, fr('b3', 0), fr('b4', 34), g=1.)
    L = P.layer('lullaby', lufs=-28, sends=dict(hall=.4), p=-.2)
    line(L, notes("S:1 G:.5 P:.5 G:1 S:1 G:.5 R:.5 S:1.5", fr('b4', 0)), 'veena', seed=11, ring=1.2, g=.8)


def drums(P):
    L = P.layer('coronation', lufs=-17, sends=dict(stone=.45))
    beat(L, "N+.ooN.o.No oo".replace(' ', ''), fr('b1', 0), 3, 1, seed=1, width=.4); beat(L, "H+.hhB.H.hhhh", fr('b1', 0), 3, 1, seed=2, width=.3)
    beat(L, "W.....W..W.W", fr('b1', 0), 3, 1, seed=3); beat(L, "j.J.j.J.j.J.", fr('b1', 0), 3, 1, seed=4, g=.35)
    L = P.layer('boons', mom=-25, sends=dict(hall=.5))
    for f in (42, 54): L.at(war(40, .5, 1), fr('b1', f), .8)
    L = P.layer('heart', lufs=-29, sends=dict(stone=.3))
    for k in range(6): L.at(war(44, .42, k % 3, hard=.1), fr('b2', 12 * k), .9); L.at(war(44, .25, k % 2, hard=.1), fr('b2', 12 * k + 6), .5)
    L = P.layer('tabla', lufs=-24, sends=dict(close=.4, hall=.15), p=.1)
    beat(L, "X.Y-.D.G.d-.Dt-", fr('b3', 0), 3, 2, seed=5, width=.08)
    beat(L, "X.Y-.D.G.Dt-DtX.....", fr('b3', 72), 3, 1, seed=6, width=.08, upto=fr('b4', 1))
    for f, q in ((27, 'doum'), (54, 'tek'), (81, 'doum')): L.at(frame(q, v=1., jingle=.5), fr('b3', f), 1.1); L.at(bayan('ge', v=1., bend=.5), fr('b3', f), .9)
    J = P.layer('manjira', lufs=-36, sends=dict(hall=.3), p=.35)
    beat(J, "j-.J-.J-.", fr('b3', 0), 6, 2, seed=7, upto=fr('b3', 80)); beat(J, "j-.J-.J-.", fr('b3', 72), 6, 1, seed=8)


def pads(P):
    L = P.layer('drone', lufs=-27, sends=dict(hall=.5, stone=.3), low=30)
    n = 36 / 24 + 2.6
    x = drone(hz('S,') / 2, n, 1, .5); y = drone(hz('P,') / 2, n, 2, .35); z = drone(hz('r,'), 1.6, 3, .3)
    e = lambda q: fades(q, .05, 1.2)
    L.at(e(x), fr('b1', 36)); L.at(e(y), fr('b1', 42), .45, .3); L.at(e(z), fr('b1', 54), .22, -.3)
    L = P.layer('dusk', lufs=-27, sends=dict(hall=.6))
    strings(L, notes("P,:2@.5 d,:2@.55 P,:2@.5 m,:2@.5 g,:1.5@.5 r,:1.5@.45 S,:1.5@.4", fr('b2', 0)), 'cello', 6, seed=1, attack=.4, release=.5, raga=(0, 112, 316, 498, 702, 814, 1018))
    strings(L, notes("S,:6@.4 m,,:3@.4 S,:3@.4", fr('b2', 0)), 'cello', 4, seed=2, attack=.5, release=.6, g=.8)
    L = P.layer('seasons', lufs=-27, sends=dict(hall=.5))
    for k, (a, b, c) in enumerate((("G:9@.5 S:3@.5 G:3@.6 P:1 G:2@.5", 'violin', -.4), ("P:6@.5 D:3 m:3@.5 R:3@.6 P:3@.5", 'violin', .4), ("S:6@.5 D,:3 m,:3@.5 P,:3@.6 S:3@.5", 'cello', .1))):
        strings(L, notes(a, fr('b3', 0)), b, 6, seed=10 + k, p=c, attack=.25, release=.5)
    strings(L, notes("_:13.5 P':4.5@.22", fr('b3', 0)), 'violin', 4, seed=14, g=.5, p=0, attack=.1, release=.4)
    N = P.layer('night', lufs=-31, sends=dict(hall=.6))
    strings(N, notes("S,:6@.35", fr('b4', 0)), 'cello', 4, seed=20, attack=.4, release=.8); strings(N, notes("G:3@.3 P:3@.3", fr('b4', 0)), 'violin', 4, seed=21, attack=.5, release=.8, g=.6)
