"""F, the war: ten eyes up a dark scale, the laugh, the hosts, the giant, the bolt, the mountain, the duel, the last arrow."""
from core import *
from voice import *
from inst import *
from perc import *
import cues

SHREE = (0, 112, 386, 590, 702, 814, 1088)
SHIV = (0, 204, 316, 702, 884)
HAM = (0, 204, 386, 702, 1088)
DARK = "S,, r,, G,, M,, P,, d,, N,, S, r, G,".split()
EYES = range(12, 67, 6)
FLASH = (6, 14, 22, 30, 38, 46)                   # lamp, wedding fire, line, ring, tail, city


def laugh(L, frame, n=9):
    """A male laughing chorus: 'ha' after 'ha', each man in his own throat, pitch falling, breath running out."""
    r = rng('laugh')
    for i in range(n):
        s = Singer('m', float(np.clip(.93 + .03 * r.standard_normal(), .86, 1.)), rd=.62 + .1 * r.random(), breath=.04, vib=(6, 10), jit=.012, shim=.07, drift=20, ring=.3, seed=300 + i)
        t, sy, f = sec(frame) + .02 + (0 if i == 0 else abs(r.normal(0, .02))), [], hz('S,') * r.choice([1, 1, 1.5, 2]) * 2 ** (r.normal(0, 60) / 1200)
        for k in range(8):
            d = .105 + .010 * k + .01 * r.random()
            g = (1 + .25 * np.sin(min(k, 3) / 3 * np.pi)) * 2 ** (-(k ** 1.2) * 1.0 / 12)
            sy.append(('haa' if k % 3 == 0 else 'ha', [(t, t + d * .78, f * g, '', max(.35, 1 - .075 * k))])); t += d + .07
        y, t0 = s.sing(sy, seed=i, attack=.012, release=.08, cons=.5)
        L.add(y, t0, 1 / n ** .5 * r.uniform(.7, 1.1), .9 * (2 * (i + .5) / n - 1))


def shout(L, frame, syl='haa', f='S,', dur=.22, n=10, seed=0, g=1., fall=3.):
    r = rng('shout', frame, seed)
    for i in range(n):
        s = Singer('m', float(np.clip(1 + .04 * r.standard_normal(), .92, 1.1)), rd=.6, breath=.04, vib=(5, 5), drift=15, seed=400 + i)
        h = hz(f) * 2 ** (r.normal(0, 90) / 1200) * r.choice([1, 1, 2]); t = sec(frame) + (0 if i == 0 else abs(r.normal(0, .012)))
        y, t0 = s.sing([(syl, [(t, t + dur * .5, h, '', 1.), (t + dur * .5, t + dur, h * 2 ** (-fall / 12), '', .8)])], seed=seed + i, attack=.02, release=.08)
        L.add(y, t0, g / n ** .5, .9 * (2 * (i + .5) / n - 1))


def voice(P):
    sa = SA / 2
    M = P.layer('dark men', lufs=-22, sends=dict(cathedral=.5, hall=.3), low=55, dry=.75)
    choir(M, lyric("oo=S,:2@.4 oo=S,:4@.5 au=r,:3@.7 aa=S,:2@.9", fr('f1', 0), SA), 'm', 8, seed=1, rd=.95, attack=.8, release=.1, raga=SHREE)
    choir(M, lyric("oo=P,,:6@.5 au=M,,:3@.7 aa=P,,:2@.9", fr('f1', 0), SA), 'm', 6, seed=2, rd=.95, attack=.8, release=.1, raga=SHREE, g=.8)
    choir(M, lyric("aa=S,:6@.9 aa=r,:4@.9 aa=S,:1.5@.8", fr('f3', 0), SA), 'm', 8, seed=3, rd=.8, attack=.4, release=.2, raga=SHREE)
    choir(M, lyric("aa=M,:6@.8 aa=G,:4@.8 aa=M,:1.5@.8", fr('f3', 0), SA), 'm', 6, seed=4, rd=.8, attack=.4, release=.2, raga=SHREE, g=.7)
    L = P.layer('laugh', lufs=-15, sends=dict(cave=.5, hall=.25), low=60, dry=.9); laugh(L, fr('f1', 72), 12)
    H = P.layer('shouts', lufs=-18, sends=dict(open=.5, hall=.3), low=80)
    for k, f in enumerate((0, 12, 24, 30)): shout(H, fr('f2', f), 'ho', 'S', seed=k, g=.6 + .1 * k)
    for k, (f, s) in enumerate(((36, 'haa'), (48, 'haa'), (60, 'he'), (66, 'he'), (72, 'haa'), (84, 'haa'), (90, 'he'))): shout(H, fr('f2', f), s, ('S', 'P')[k % 2], seed=10 + k)
    for k, f in enumerate(cues.frames('f7', 'hit')[:5]): shout(H, fr('f7', f), 'haa', 'S', .16, 6, seed=30 + k, g=.5)
    W = P.layer('war chorus', lufs=-17.5, sends=dict(cathedral=.35, hall=.3), low=75, dry=.85)
    choir(W, lyric("raa=S:1@1 ma=S:1@.95 raa=g:1@1 ma=R:.5@.95+S:.5@.95 | raa=P:1@1 ma=g:1@.95 raa=R:1@1 ma=S:1@.95", fr('f2', 48), sa), 'm', 14, seed=20, rd=.75, attack=.03, raga=SHIV)
    choir(W, lyric("raa=P:1@1 ma=P:1@.95 raa=S':1@1 ma=n:1@.95 | raa=S':1@1 ma=n:1@.95 raa=P:1@1 ma=P:1@.95", fr('f2', 48), sa), 'm', 10, seed=21, rd=.75, attack=.03, raga=SHIV, g=.8)
    choir(W, lyric("aa=P:1.5@.7+D:.75@.85+S':.7@1", fr('f3', 60)), 'f', 10, seed=22, attack=.3, release=.1)
    # f5: the mountain flies
    up = "lau=P:3@.7+D:1@.75 cha=S':1@.8 lii=S':2@.85+D:1@.75 | lau=R':3@.85+S':1@.85 cha=R':1@.9 lii=G':3@.95 | lau=G':2@1+P':1@1+G':1@.95"
    lo = "lau=S:3@.7+P:1@.75 cha=P:1@.8 lii=D:2@.85+P:1@.75 | lau=P:3@.85+D:1@.85 cha=D:1@.9 lii=N:3@.95 | lau=S':2@1+S':1@1+S':1@.95"
    F = P.layer('mountain chorus', lufs=-18, sends=dict(cathedral=.5, hall=.3), low=80, dry=.75)
    choir(F, lyric(up, fr('f5', 0)), 'f', 12, seed=30, attack=.12, release=.9); choir(F, lyric(lo, fr('f5', 0)), 'f', 9, seed=31, attack=.12, release=.9, g=.8)
    choir(F, lyric(up, fr('f5', 0)), 'm', 10, seed=32, octave=-1, attack=.12, release=.9); choir(F, lyric("lau=S,:4@.7 cha=S,:1@.8 lii=m,,:3@.85 | lau=P,:4@.85 cha=P,:1@.9 lii=R,:3@.95 | lau=S,:4@1", fr('f5', 0)), 'm', 10, seed=33, attack=.12, release=.9)
    S = P.layer('lead', lufs=-18, sends=dict(close=.3, hall=.32), low=110, eq=((300, -2, 1.), (3200, 2, 1.2)))
    solo(S, LEAD, lyric("lau=P^:3@.75+D:1@.8 cha=S':1@.8 lii=S':1@.85+R':1@.85+D:1@.8 | lau=R'^:2.5@.9+G':.5@.9+S':1@.85 cha=R':1@.9 lii=G':3@.95 | lau=G':2@1+P':1.2@1+G':.8@.95", fr('f5', 0)), breathin=.8, release=.8)
    # f8: every voice gathers on lau
    A = P.layer('all voices', lufs=-15.5, sends=dict(cathedral=.4, hall=.3), low=75, dry=.85)
    g = fr('f8', 0)
    solo(S, LEAD, lyric("ek=S:1@.5+G:1@.55 lau=P:3@.6+D:1@.6", g + 0), g=.6, breathin=.5, release=.4)
    choir(A, lyric("raa=S:1@.4 ma=S:.5@.4 raa=S:1@.45 raa=S:1@.5 raa=S:.5@.55", g + 22, sa), 'm', 8, seed=39, attack=.05, g=.5)
    for k, (f, d, kd, o, n) in enumerate(((30, 'S', 'm', -1, 8), (38, 'P', 'm', -1, 8), (46, 'S', 'f', 0, 8), (54, 'G', 'f', 0, 8), (60, "P", 'f', 0, 8), (66, 'S', 'm', 0, 8))):
        nx = {'S': 'R', 'P': 'D', 'G': 'P'}[d]; nn = {'S': 'G', 'P': "S'", 'G': "D"}[d]
        L_ = (96 - f) / 6
        a, b, c = L_ - 5, 2.5, 2.6
        choir(A, lyric(f"lau={d}:{max(a, 1):.2f}@.55+{nx}:{b}@.8+{nn}:{c}@1", g + f), kd, n, seed=40 + k, octave=o, attack=.4, release=.04, rd=.85)
    choir(A, lyric("jaa=P':1@.9+S'':1@.9" .replace('jaa', 'aa') + "+S'':1@1", g + 78), 'f', 8, seed=50, attack=.2, release=.04, g=.6, rd=.8)
    R = P.layer('release', lufs=-14.5, sends=dict(cathedral=.5, hall=.25), low=75, dry=.8)
    for k, (d, o, kd, n) in enumerate((("G'", 0, 'f', 8), ("S'", 0, 'f', 8), ("P", 0, 'f', 8), ("S'", -1, 'm', 8), ("P", -1, 'm', 8), ("S", -1, 'm', 8))):
        d2, d3 = {"G'": ("R'", "G'"), "S'": ("S'", "N"), "P": ("P", "P"), "S": ("S", "R")}[d] if True else 0
        choir(R, lyric(f"aa={d}:4@.95+{d2}:4@.95+{d3}:3.9@1 aa={d}:3@.9", fr('f9', 0)), kd, n, seed=60 + k, octave=o, attack=.04, release=.5, rd=.82)


def melodic(P):
    L = P.layer('eyes', lufs=-19, sends=dict(cave=.55), low=28)
    for k, f in enumerate(EYES):
        h = hz(DARK[k]); v = .6 + .04 * k
        L.at(pluck(h, 2.6, 'sarod', v, k), fr('f1', f), v); L.at(pluck(h * 2, 2.2, 'veena', v, 50 + k), fr('f1', f), .5 * v); L.at(gong(h, 2.6, .25, .35 + .05 * k, 20 + k, t60=3.), fr('f1', f), .12 * v, .12 * (k - 4.5))
    B = P.layer('brass', lufs=-17, sends=dict(hall=.45, open=.2), low=42); sa = SA / 2
    horns(B, notes("S,:4@.7", fr('f1', 72), sa=sa), 4, seed=1, attack=.05, release=.3, kind='low', growl=.3)
    horns(B, notes("S:2@.7 r:1@.8 S:1@.8 M:1.5@.9 P:.4@1", fr('f2', 0), sa=sa), 5, seed=2, attack=.03, release=.06)
    horns(B, notes("S':2@1 n:1 P:1 | g:2@1 R:1 S:1 | g:1 P:1", fr('f2', 36), sa=sa), 6, seed=3, attack=.02, release=.1)
    horns(B, notes("S,:2@1 r,:2@1 | S,:2 M,:2 | S,:3", fr('f3', 12), sa=sa * 2), 5, seed=4, attack=.04, release=.2, kind='low', growl=.2)
    horns(B, notes("P:1@.8 D:1@.9 S':2@1", fr('f3', 54), sa=sa), 5, seed=5, attack=.03, release=.06)
    horns(B, notes("P:4@.6 S':4@.7 | D:4@.8 G':4@.9 | S':4@1", fr('f5', 0), sa=sa), 5, seed=6, attack=.2, release=.8, g=.8)
    hits = cues.frames('f7', 'hit')
    for k, f in enumerate(hits):
        nx = hits[k + 1] if k + 1 < len(hits) else 96
        horns(B, [(sec(fr('f7', f)), sec(fr('f7', f + min(5, nx - f - .3))), hz("S r G M P d N S' r' G' M' P' d' N' S'' r'' G'' M''".split()[min(k, 17)], sa), '', 1.)], 4, seed=100 + k, attack=.012, release=.05, g=.9)
    horns(B, notes("S':8@.9 S':4@1 | S':3@.7", fr('f9', 0), sa=sa), 6, seed=7, attack=.02, release=.6)
    horns(B, notes("S:2@.5 R:2@.65 G:2@.8 P:2@.95", fr('f8', 46), sa=sa), 5, seed=8, attack=.2, release=.04)
    C = P.layer('war conch', lufs=-17, sends=dict(open=.55))
    for k, (f, h, p) in enumerate(((0, 220.2, -.5), (5, 293.66, .5), (36, 293.66, 0.), (64, 220.2, .6))): C.at(conch(h, 1.5, k), fr('f2', f), .8, p)
    F = P.layer('flutes', lufs=-23, sends=dict(hall=.5), p=.2)
    bansuri(F, notes("P:1 D:1 S':2 R':2 S':2 | R':1 S':1 R':2 G':4 | P':2 G':2", fr('f5', 0)), seed=1, g=.8)
    bansuri(F, notes("S:1 G:1 P:3 D:1", fr('f8', 6) - 12), seed=2, g=.5)
    S = P.layer('strings plucked', lufs=-23, sends=dict(hall=.35), p=-.2)
    swarmandal(S, "S G P S' G' P' S'' G''", fr('f5', 84), dt=.06, g=.8, seed=3); swarmandal(S, "S, P, S G P S' R' G' P'", fr('f5', 0), dt=.05, g=.6, seed=4)
    line(S, notes("G:.5 P:.5 S':.5 D:.5 P:.5 G:.5", fr('f8', 14)), 'veena', seed=5, g=.8)
    santoor(S, notes("S':.5 P:.5 G:.5 P:.5 D:.5 S':.5", fr('f8', 22)), seed=6, g=.6)
    line(S, notes("S:.5 G:.5 P:.5 N:.5 P:.5 G:.5 R:.5 P:.5 N:.5 P:.5 G:.5 P:.5 N:.5 R':.5", fr('f8', 38)), 'sitar', seed=7, ring=.5)
    santoor(S, notes(" ".join(f"{d}:.25@{.5 + .012 * i:.2f}" for i, d in enumerate("S G P D S' D P G R G P D S' R' S' D G P D S' G' S' D P S' R' G' P' G' R' S' D".split())), fr('f8', 48)), seed=8, hard=.7)
    D = P.layer('one bell', mom=-27, sends=dict(hall=.8)); D.at(bell(hz("S'"), 4.5, 5., .3, 11), fr('f6', 24), .7); D.at(course(hz("G'"), 3, .25, t60=5, seed=12), fr('f6', 24), .4)
    Q = P.layer('ten lights', lufs=-27, sends=dict(hall=.5, cave=.25), low=30)
    for k, f in enumerate(range(12, 61, 6)):
        d = "G, r, S, N,, d,, P,, M,, r,, S,,".split()[k]
        Q.at(pluck(hz(d), 3., 'veena', .6 - .03 * k, 70 + k), fr('f10', f), .9 - .03 * k, .14 * (k - 4)); Q.at(gong(hz(d), 2.5, .2, .15, 40 + k, 3.), fr('f10', f), .05, .14 * (k - 4))
    B2 = P.layer('the last bows', lufs=-27, sends=dict(hall=.7))
    bansuri(B2, notes("P^:1.2@.6 G:.8@.5", fr('f10', 66)), seed=9, breath=.18, g=.45, release=.4)
    B2.at(course(hz('G'), 4., .3, t60=6, seed=13), fr('f10', 78), .8); B2.at(pluck(hz('G,'), 3.5, 'veena', .5, 90), fr('f10', 78), .5)


def drums(P):
    L = P.layer('eyes', lufs=-20, sends=dict(cave=.5), low=26)
    for k, f in enumerate(EYES): L.at(war(40 + .6 * k, round(.5 + .05 * k, 2), k % 4, hard=.2), fr('f1', f), .5 + .05 * k)
    L.at(war(38, 1., 1, hard=.7), fr('f1', 72), 1.)
    for k, f in enumerate((78, 84, 88, 91, 93.5)): L.at(war(44, .6, k % 4, hard=.4), fr('f1', f), .5)
    W = P.layer('war', lufs=-14, sends=dict(open=.45, hall=.15), low=26)
    beat(W, "W...W...W.W.WwWw", fr('f2', 0), 3, 1, seed=1, upto=fr('f2', 36), vel=lambda f: float(np.clip(.55 + .012 * (f - fr('f2')), .4, 1)))
    roll(W, 'o', fr('f2', 12), fr('f2', 36), 2, 1.2, .25, 1., seed=2, g=.5)
    ensemble(W, lambda i: war(38 + 3 * i, 1., i, hard=.9), fr('f2', 36), 6)
    beat(W, "W+.w.W.wwW.wwW.ww", fr('f2', 48), 3, 1, seed=3, width=.2); beat(W, "wwWw", fr('f2', 39), 2.25, 1, seed=4, g=.7)
    beat(W, "N.ooN.o.N.ooNooo", fr('f2', 48), 3, 1, seed=5, width=.6, g=.7); beat(W, "H+hhHhhHhHhhHhhHh", fr('f2', 48), 3, 1, seed=6, width=.5, g=.7)
    G = P.layer('giant', lufs=-15.5, sends=dict(open=.5, hall=.25), low=24)
    beat(G, "W...w...W...w...", fr('f3', 0), 3, 1, seed=7); beat(G, "N..oN..oN.ooNooo", fr('f3', 18), 3, 1, seed=8, g=.6, upto=fr('f3', 66), width=.5)
    for f in (30, 48): ensemble(G, lambda i: war(34 + 3 * i, 1., i, hard=.5), fr('f3', f), 4)
    G.at(war(52, .9, 2, hard=1.), fr('f3', 66), .7); ensemble(G, lambda i: war(32 + 3 * i, 1., i, hard=.8), fr('f3', 78), 7, g=1.5)
    S = P.layer('bolt', mom=-14, sends=dict(open=.5, hall=.3)); ensemble(S, lambda i: war(42 + 4 * i, 1., i, hard=1.), fr('f4', 30), 4); roll(S, 'w', fr('f4', 18), fr('f4', 30), 3, 1.5, .1, .5, seed=9, g=.35)
    M = P.layer('mountain', lufs=-20, sends=dict(hall=.5), low=28)
    for k in range(5): M.at(war(40, .7, k % 4, hard=.3), fr('f5', 24 * k), .8); M.at(war(52, .5, k % 3, hard=.3), fr('f5', 24 * k + 18), .5)
    beat(M, "F.f.f.F.ff F.f.f.F.ff".replace(' ', ''), fr('f5', 48), 3, 1, seed=10, g=.6); roll(M, 'w', fr('f5', 84), fr('f5', 118), 3, 2, .15, .7, seed=11, g=.5)
    D = P.layer('duel', lufs=-14, sends=dict(open=.4, hall=.15), low=26)
    hits = cues.frames('f7', 'hit')
    for k, f in enumerate(hits):
        v = 1.; D.at(war(42 + .8 * k, v, k % 4, hard=.9, dur=1.4), fr('f7', f), 1.); D.at(nagara(1., k % 4, 90 + 4 * k), fr('f7', f), .7); D.at(dhol('dha', 1., k % 4), fr('f7', f), .6)
    beat(D, "h.hhh.hhh.hhh.hh", fr('f7', 0), 3, 2, seed=12, g=.32, width=.6, upto=fr('f7', 94))
    E = P.layer('gather', lufs=-17, sends=dict(hall=.4), low=26)
    beat(E, "W-.....W-.....", fr('f8', 0), 6, 1, seed=13, upto=fr('f8', 46)); beat(E, "F.f-.f.F.f.F.f.", fr('f8', 38), 3, 1, seed=14, g=.5)
    roll(E, 'w', fr('f8', 46), fr('f8', 96), 4, 1., .2, 1., seed=15); roll(E, 'h', fr('f8', 66), fr('f8', 96), 2, 1., .2, 1., seed=16, g=.4)
    for f in (72, 84, 90, 93): E.at(war(40, .9, int(f) % 4, hard=.6), fr('f8', f), .8)
    R = P.layer('release', lufs=-13.5, sends=dict(cathedral=.25, open=.4), low=26)
    ensemble(R, lambda i: war(36 + 3 * i, 1., i, hard=1.), fr('f9', 0), 6, g=1.1)
    beat(R, "W+wwWwwWwWwwWwwWwWwWwWwWw", fr('f9', 0), 3, 1, seed=17, width=.2, upto=fr('f9', 70)); beat(R, "hhhhhhhhhhhhhhhhhhhhhhhh", fr('f9', 0), 3, 1, seed=18, width=.7, g=.4, vel=lambda f: .5 + .5 * (f - fr('f9')) / 72, upto=fr('f9', 70))
    X = P.layer('strike', mom=-9.5, sends=dict(cathedral=.45, hall=.2), low=24)
    ensemble(X, lambda i: war(31 + 3 * i, 1., i, hard=1.), fr('f9', 72), 8); X.at(gong(52, 7, .25, .9, 9), fr('f9', 72), .35); X.at(nagara(1., 1, 70.), fr('f9', 72), .6)


def pads(P):
    L = P.layer('gate', lufs=-24, sends=dict(cave=.5), low=30)
    x = drone(hz('S,') / 2, 4., 1, .6); L.at(fades(x * np.linspace(.4, 1, len(x)), .4, .5), fr('f1', 0)); y = drone(hz('r,'), 2.4, 2, .5); L.at(fades(y, 1., .4), fr('f1', 42), .4)
    strings(L, notes("N:4@.4 r':4@.7 M':4@.95", fr('f1', 24)), 'violin', 6, seed=1, attack=1.5, release=.3, trem=8, g=.5, raga=SHREE)
    W = P.layer('war strings', lufs=-20, sends=dict(hall=.35))
    strings(W, notes(" ".join(f"{d}:.5@{.6 + .02 * i:.2f}" for i, d in enumerate("S S r S S S r S M S r S".split())), fr('f2', 0)), 'cello', 8, seed=2, attack=.02, release=.05, loose=.006)
    for k in (0, 1): strings(W, notes(" ".join(f"{d}:.5@1" for d in "S g P g S g P n S' n P g R g P g".split()[:16 if k == 0 else 4]), fr('f2', 36 + 48 * k)), 'violin', 10, seed=3 + k, attack=.02, release=.04, loose=.006, raga=SHIV)
    strings(W, notes("S,:4@1 S,:2 P,:2 | S,:2@1", fr('f2', 36)), 'cello', 7, seed=6, attack=.03, release=.2)
    strings(W, notes("S,:2@.8 r,:2 S,:2 M,:2 r,:2 S,:3", fr('f3', 0)), 'cello', 8, seed=7, attack=.05, release=.2, trem=7, raga=SHREE); strings(W, notes("r':8@.5 N:3@.6", fr('f3', 12)), 'violin', 7, seed=8, attack=1.5, release=.1, trem=9, g=.5, raga=SHREE); strings(W, notes("P:1@.7 D:1@.8 S':1@.9 G':1@1 P':2@1", fr('f3', 48)), 'violin', 8, seed=9, attack=.05, release=.08)
    strings(W, notes(" ".join(f"{d}:.5@.9" for d in "S r S G S r S M S r S G S r S M P M G r S r G M P d N S' r' S' N d".split()), fr('f7', 0)), 'violin', 10, seed=10, attack=.02, release=.04, loose=.005, raga=SHREE); strings(W, notes("S,:4@.9 r,:4@.9 S,:4@1 M,:4@1", fr('f7', 0)), 'cello', 8, seed=11, attack=.04, release=.1, raga=SHREE)
    H = P.layer('one string', lufs=-27, sends=dict(hall=.7)); strings(H, notes("S'':8.6@.4", fr('f4', 44)), 'violin', 1, seed=12, attack=.25, release=.5, tune=0, loose=0, width=0)
    N = P.layer('storm', lufs=-24, sends=dict(hall=.5)); strings(N, notes("S,:2@.4 r,:2@.6 S,:1@.8", fr('f4', 0)), 'cello', 7, seed=13, attack=.8, release=.06, trem=8, raga=SHREE); strings(N, notes("M:5@.5", fr('f4', 0)), 'violin', 6, seed=14, attack=1., release=.06, trem=9, g=.6)
    F = P.layer('mountain', lufs=-20, sends=dict(hall=.5))
    arp = "S:.5 P:.5 S':.5 P:.5 D:.5 S':.5 G':.5 S':.5 m:.5 D:.5 S':.5 D:.5 m:.5 S':.5 D:.5 S':.5 | P:.5 D:.5 R':.5 D:.5 P:.5 R':.5 D:.5 R':.5 P:.5 N:.5 R':.5 N:.5 G':.5 R':.5 N:.5 R':.5 | S:.5 P:.5 S':.5 G':.5 P':.5 G':.5 S':.5 P:.5"
    strings(F, notes(" ".join(t if t == '|' else f"{t}@{.45 + .5 * i / 41:.2f}" for i, t in enumerate(arp.split())), fr('f5', 0)), 'violin', 9, seed=15, attack=.04, release=.1, loose=.008, p=-.3)
    strings(F, notes("S,:4@.6 D,:1 m,:3@.7 | P,:4@.8 N,:1 G,:3@.9 | S,:4@1", fr('f5', 0)), 'cello', 8, seed=16, attack=.15, release=.8, p=.3); strings(F, notes("S,:8@.6 P,,:8@.8 S,:4@1", fr('f5', 0), sa=SA / 2), 'cello', 5, seed=17, attack=.2, release=.8); strings(F, notes("G':4@.4 S':4@.5 | R':4@.7 N:4@.8 | P':4@1", fr('f5', 0)), 'violin', 8, seed=18, attack=.3, release=.9, p=.4, g=.8)
    M = P.layer('morning', lufs=-27, sends=dict(hall=.7))
    for k, (d, kd, p) in enumerate((("S,:4.5@.4", 'cello', 0), ("P,:4.5@.4", 'cello', .3), ("G:4.5@.35", 'violin', -.4), ("D:2@.3 P:2.5@.35", 'violin', .4))): strings(M, notes(d, fr('f6', 24)), kd, 5, seed=20 + k, p=p, attack=.6, release=.5)
    G = P.layer('gather', lufs=-18, sends=dict(hall=.45), low=30)
    strings(G, notes("S,:8@.4 S,:8@.95", fr('f8', 0)), 'cello', 8, seed=30, attack=1., release=.03, swell=.1); strings(G, notes("S,:8@.4 P,:8@.95", fr('f8', 0), sa=SA / 2), 'cello', 5, seed=31, attack=1., release=.03)
    strings(G, notes("S,:3@.7 r,:1.5@.8 S,:2@.6", fr('f8', 22)), 'cello', 5, seed=32, attack=.1, release=.2, g=.7)
    strings(G, notes("P:2@.4 D:2@.55 S':2@.7 R':1.5@.85 G':1.5@1", fr('f8', 42)), 'violin', 10, seed=33, attack=.5, release=.03, trem=10, p=-.3); strings(G, notes("S:2@.4 P:2@.55 G':2@.7 S'':1@.9 P':2@1", fr('f8', 42)), 'violin', 8, seed=34, attack=.5, release=.03, trem=11, p=.4)
    R = P.layer('release', lufs=-18, sends=dict(hall=.45, cathedral=.2))
    strings(R, notes(" ".join(f"{d}:.5@1" for d in "S G P D S' D P G R P D R' D P R' P G P S' G' P' G' S' P".split()), fr('f9', 0)), 'violin', 10, seed=40, attack=.02, release=.04, loose=.006, p=-.3)
    strings(R, notes("G':4@.95 R':4@.95 G':4@1 S':3@.7", fr('f9', 0)), 'violin', 9, seed=41, attack=.03, release=.6, p=.4); strings(R, notes("S,:4@1 m,:4@1 P,:4@1 S,:3@.7", fr('f9', 0)), 'cello', 8, seed=42, attack=.03, release=.6); strings(R, notes("S,:4@1 S,:4@1 P,,:4@1 S,:3@.7", fr('f9', 0), sa=SA / 2), 'cello', 5, seed=43, attack=.03, release=.6)
