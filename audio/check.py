"""python audio/check.py : measure the finished soundtrack against the storyboard. Writes pictures and report.txt to qa/audio."""
import sys, importlib
import numpy as np, cv2
from scipy import signal
from core import *
import qa, mix, cues
OUT = ROOT / 'qa' / 'audio'

LAMPS = sorted(set(cues.frames('b2', 'puff')))
# (shot, frame, stems it lives in, what)
NAMED = [('a1', 24, 'sfx', 'spark'), ('a1', 36, 'melodic', 'flame, bell'), ('a2', 0, 'melodic drums', 'theatre'), ('a2', 36, 'melodic sfx', 'prince 1'), ('a2', 90, 'melodic drums sfx', 'toy arrow'), ('a3', 24, 'melodic drums', 'sunrise'), ('a4', 84, 'drums sfx', 'BOW BREAK'),
         ('b1', 0, 'drums', 'coronation'), ('b1', 42, 'melodic', 'first boon'), ('b1', 54, 'melodic', 'second boon'), ('b2', 12, 'sfx', 'crown set down'), *[('b2', f, 'melodic', f'lamp out {i + 1}') for i, f in enumerate(LAMPS) if f == LAMPS[0] or f - LAMPS[i - 1] > 1.5], ('b3', 0, 'drums', 'walk'), *[('b3', f, 'drums', w) for f, w in ((27, 'monsoon'), (54, 'autumn'), (81, 'winter'))],
         ('c1', 36, 'drums', 'deer leaps'), ('c1', 42, 'drums', 'gold eye'), ('c2', 24, 'sfx drums', 'arrow loosed'), ('c2', 30, 'drums', 'deer struck'), ('c3', 18, 'sfx pads drums', 'line takes fire'), *[('c4', 36 + 6 * k, 'drums', f'head {k + 1}') for k in range(10)], ('c4', 78, 'melodic', 'she looks'), ('c4', 90, 'sfx drums', 'line goes out'), ('c5', 0, 'melodic drums', 'unfolds'), ('c5', 24, 'drums sfx', 'earth torn'), ('c6', 60, 'drums sfx', 'wing taken'), ('c6', 72, 'sfx', 'ornament'),
         ('d1', 42, 'melodic sfx', 'spark wakes'), ('d2', 0, 'drums', 'seven begins'), ('d3', 42, 'drums sfx', 'LEAP'), ('d4', 66, 'sfx melodic drums', 'serpent'), ('d5', 48, 'drums sfx', 'lands'), ('d6', 36, 'melodic sfx', 'ring'), ('d7', 30, 'drums sfx', 'fire catches'), ('d7', 66, 'drums sfx', 'ropes burst'), ('d8', 0, 'drums', 'Lanka burns'), ('d8', 126, 'drums', 'pull away'),
         ('e1', 42, 'sfx', 'stone dropped'), ('e1', 60, 'melodic sfx', 'name glows'), ('e1', 84, 'sfx drums', 'surfaces'), *[('e2', 6 * k, 'drums', f'stone {k + 1}') for k in range(0, 16, 3)],
         *[('f1', 12 + 6 * k, 'melodic', f'eye {k + 1}') for k in range(10)], ('f1', 72, 'voice', 'laugh'), ('f2', 36, 'drums sfx', 'CLASH'), ('f3', 12, 'sfx melodic', 'giant eye'), ('f3', 30, 'drums', 'footfall'), ('f3', 48, 'drums', 'footfall'), ('f3', 66, 'drums sfx', 'arrow'), ('f3', 78, 'drums sfx', 'GIANT FALLS'), ('f4', 30, 'sfx drums', 'lightning'), ('f5', 0, 'drums', 'mountain'), ('f6', 12, 'sfx', 'drop'), ('f6', 24, 'melodic', 'one bell'),
         *[('f7', f, 'drums', f'duel {i + 1}') for i, f in enumerate(cues.frames('f7', 'hit')[:9])], ('f9', 0, 'drums sfx', 'RELEASE'), ('f9', 72, 'drums sfx', 'STRIKE'), *[('f10', 12 + 6 * k, 'melodic', f'light {k + 1}') for k in range(9)], ('f10', 78, 'melodic', 'the last light'),
         ('g1', 24, 'melodic sfx', 'jewel'), ('g3', 0, 'drums', 'arrival walk'), ('g4', 84, 'drums melodic', 'LAMPS WRITE THE NAME'), ('g5', 84, 'sfx', 'breath'), ('g5', 90, 'melodic', 'string'), ('g5', 120, 'melodic', 'octave')]


def novelty(x):
    """Spectral flux of log magnitude, 2 ms hop."""
    x = x.mean(1)
    n, h = 768, 96
    f, t, S = signal.stft(x, SR, nperseg=n, noverlap=n - h, nfft=1024, boundary=None, padded=False)
    A = np.abs(S); W = np.log(A + 1e-5 + .002 * A.max())
    return t, np.maximum(W[:, 4:] - W[:, :-4], 0).sum(0) * 1.


def accents(st):
    rows = []
    for s, f, stems, what in NAMED:
        c = sec(fr(s, f)); a = max(0, int((c - .35) * SR)); b = min(TOTAL, int((c + .35) * SR))
        x = sum(st[k][a:b] for k in stems.split())
        t, nv = novelty(x)
        tt = a / SR + t[4:] - .004
        m = abs(tt - c) < .125
        pk, _ = signal.find_peaks(np.r_[0, nv, 0]); pk = pk - 1
        pk = [q for q in pk if m[q] and nv[q] > .45 * (nv * m).max()]           # the strong onsets near by; the nearest of them
        k = min(pk, key=lambda q: abs(tt[q] - c))
        # refine: where the flux first reaches half of that peak
        i = k
        while i > 0 and nv[i] > .5 * nv[k]: i -= 1
        rows.append((s, f, what, (tt[i] - c) * 1000 + 4, nv[k] / (np.median(nv) + 1e-9)))
    return rows


def tuning():
    """Every solo note of 0.3 s or more: sung pitch against the written note, in cents."""
    import voice
    out = []
    for act in ACT0:
        mod = importlib.import_module(f'act_{act.lower()}')
        got = []
        keep = mod.solo, mod.choir
        mod.solo = lambda L, singer, syls, g=1., p=0., **k: got.append((singer, syls, k)); mod.choir = lambda *a, **k: None
        laugh = {n: getattr(mod, n) for n in ('laugh', 'shout') if hasattr(mod, n)}
        for n in laugh: setattr(mod, n, lambda *a, **k: None)
        mod.voice(Part(ACT0[act], ACT0[act] + 1, tail=.1))
        mod.solo, mod.choir = keep
        for n, fn in laugh.items(): setattr(mod, n, fn)
        for singer, syls, k in got:
            y, t0 = singer.sing(syls, **k)
            tt, f, cl = qa.f0track(y, 90, 1100, win=.045, hop=.008); tt = tt + t0
            for nm, nt in syls:
                for a, b, h, fl, v in nt:
                    if b - a < .3 or 'haa' == nm: continue
                    m = (tt > a + .14) & (tt < b - .09) & (cl > .5)
                    if m.sum() > 3: out.append((act, nm, h, float(np.median(1200 * np.log2(f[m] / h)))))
    return out


def curve(out, st):
    W, H = 2000, 620
    im = np.full((H, W, 3), 22, np.uint8)
    Y = lambda l: int(np.clip(20 + (-5 - l) / 45 * (H - 60), 0, H - 1))
    for l in range(-50, 0, 5):
        if l < -4: cv2.line(im, (0, Y(l)), (W, Y(l)), (45, 45, 45), 1); cv2.putText(im, str(l), (4, Y(l) - 3), 0, .4, (130, 130, 130), 1)
    for s in film.START:
        x = int(film.START[s] / film.N * W); cv2.line(im, (x, 0), (x, H - 30), (60, 60, 40) if s[1:] != '1' else (90, 120, 160), 1); cv2.putText(im, s, (x + 2, H - 14), 0, .38, (170, 170, 170), 1)
    def draw(x, col, win):
        l = lu(kpower(x, win, .05)); c = (np.arange(len(l)) * .05 + win / 2) / (TOTAL / SR) * W
        cv2.polylines(im, [np.array([[int(a), Y(max(b, -49.9))] for a, b in zip(c, l)])], False, col, 1, cv2.LINE_AA)
    draw(st['voice'], (120, 200, 120), .4); draw(out, (90, 110, 90), .4); draw(out, (80, 200, 255), 3.)
    cv2.putText(im, 'orange: short-term 3 s   grey: momentary   green: voice stem', (1400, 16), 0, .42, (200, 200, 200), 1)
    cv2.imwrite(str(OUT / 'loudness.png'), im)


def run(out, st):
    OUT.mkdir(parents=True, exist_ok=True)
    L = []
    say = lambda *a: (L.append(' '.join(str(x) for x in a)), print(L[-1], flush=True))
    say(f'length {len(out)} samples = {len(out) / SR:.4f} s (film {film.N / 24:.4f}); sum of stems - soundtrack, max {np.abs(sum(st.values()) - out).max():.1e}')
    say(f'integrated {integrated(out):.2f} LUFS; true peak {20 * np.log10(mix.truepeak(out).max()):.2f} dBTP; DC {out.mean(0)}')
    for a in ACT0: say(f'act {a}: {integrated(out[ACT0[a] * FR:ACT1[a] * FR]):6.1f} LUFS, short-term max {lu(kpower(out[ACT0[a] * FR:ACT1[a] * FR], 3., .1)).max():6.1f}, momentary max {lu(kpower(out[ACT0[a] * FR:ACT1[a] * FR], .4, .05)).max():6.1f}')
    S = abs(np.fft.rfft(out.mean(1))) ** 2; F = np.fft.rfftfreq(len(out), 1 / SR); tot = S.sum()
    say('energy by band %:', {k: round(float(100 * S[(F >= a) & (F < b)].sum() / tot), 2) for k, a, b in (('<30', 0, 30), ('30-120', 30, 120), ('120-400', 120, 400), ('400-2k', 400, 2000), ('2-6k', 2000, 6000), ('6-12k', 6000, 12000), ('>12k', 12000, 24001))})
    mid, sd = out.mean(1), (out[:, 0] - out[:, 1]) / 2; say(f'side/mid {10 * np.log10((sd ** 2).mean() / (mid ** 2).mean()):.1f} dB; below 100 Hz {10 * np.log10((lp(sd, 100, 4) ** 2).mean() / (lp(mid, 100, 4) ** 2).mean()):.1f} dB; L/R correlation {np.corrcoef(out.T)[0, 1]:.2f}')
    rows = accents(st); bad = [r for r in rows if abs(r[3]) > 41.7]
    say(f'accents: {len(rows)} named, max error {max(abs(r[3]) for r in rows):.1f} ms, mean {np.mean([abs(r[3]) for r in rows]):.1f} ms, over one frame: {len(bad)}')
    for r in rows: say(f'   {r[0]:4s} f{r[1]:<4g} {r[2]:22s} {r[3]:+7.1f} ms   strength {r[4]:.0f}x {"<-- LATE/EARLY" if r in bad else ""}')
    pk = {k: np.abs(out[(fr(k, a)) * FR:(fr(k, b)) * FR]).max() for k, a, b in (('a4', 83, 90),)}
    x = out[fr('a1') * FR:fr('b1') * FR]; mo = lu(kpower(x, .05, .01)); say(f'act A: loudest 50 ms at film frame {np.argmax(mo) * .01 * 24 + .6:.1f} (bow break {fr("a4", 84)})')
    for s0, f0, f1 in (('a4', 80, 83.9), ('c7', 73, 84), ('f8', 98.5, 106), ('g5', 167, 168)):
        z = out[int(fr(s0, f0) * FR):int(fr(s0, f1) * FR)]; say(f'silence {s0} f{f0}-{f1}: peak {20 * np.log10(np.abs(z).max() + 1e-9):.0f} dBFS')
    for f, d in CUTS:
        c = int(f * FR); z = np.abs(np.diff(out[c - 400:c + 2000].mean(1))).max(); e = np.abs(np.diff(out[c - 4800:c - 400].mean(1))).max(); say(f'edit at film frame {f:g}: largest step {z:.4f} against {e:.4f} just before')
    tn = tuning(); e = np.array([t[3] for t in tn]); e = e[abs(e) < 300]
    say(f'sung pitch, {len(tn)} solo notes: median {np.median(e):+.1f} cents, mean |error| {np.abs(e).mean():.1f}, 90th percentile {np.percentile(abs(e), 90):.1f}, worst {np.abs(e).max():.0f}')
    import words
    B = signal.butter(3, (300, 3400), 'band', fs=SR, output='sos'); oth = out - st['voice']
    for s0, f0, s1, f1, hi, en in words.LINES:
        a, b = fr(s0, f0) * FR, fr(s1, f1) * FR
        v = signal.sosfilt(B, st['voice'][a:b].mean(1)); o = signal.sosfilt(B, oth[a:b].mean(1)); say(f'voice over the rest, 300-3400 Hz, {hi:34s} {10 * np.log10((v ** 2).mean() / (o ** 2).mean()):+.1f} dB')
    curve(out, st)
    for a in ACT0:
        z = out[ACT0[a] * FR:ACT1[a] * FR]
        qa.spectro(z, OUT / f'act_{a}.png', t0=sec(ACT0[a]), marks=[(sec(film.START[s]), s) for s in film.START], fmax=18000)
    (OUT / 'report.txt').write_text('\n'.join(L) + '\n')
    assert not bad, bad


if __name__ == '__main__':
    st = {s: read_wav(ROOT / 'out' / f'stem_{s}.wav') for s in mix.STEMS}
    run(read_wav(ROOT / 'out' / 'soundtrack.wav'), st)
