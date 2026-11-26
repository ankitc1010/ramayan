"""python tools/check.py [shot ...] [--scale 2]  Reads out/<shot>.mkv (out/x2/ at --scale 2) and reports: frame count against the timeline, black or blank stretches, frozen stretches, single-frame flashes, flicker (A-B-A), clipped whites.
Exit code 1 when a shot is missing, has the wrong length, or is blank where the storyboard does not say so."""
import sys, os, subprocess
from common import HOME, shot_file
import numpy as np, film as FM
B = '.mm/env/bin/'; W, H = 192, 108
DARK_OK = {'a1', 'b2', 'c7', 'f10', 'g5', 'f1', 'b1', 'd1', 'f4', 'f8'}; FREEZE_OK = {'f10': 14, 'g5': 14, 'c7': 14, 'f8': 10}


def load(s):
    r = subprocess.run([B + 'ffmpeg', '-v', 'error', '-i', str(shot_file(s, K)), '-vf', f'scale={W}:{H}:flags=area', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True)
    return np.frombuffer(r.stdout, np.uint8).reshape(-1, H, W, 3).astype(np.float32) / 255


def runs(m):
    out, a = [], None
    for i, v in enumerate(list(m) + [False]):
        if v and a is None: a = i
        if not v and a is not None: out.append((a, i - 1)); a = None
    return out


ARGS = sys.argv[1:]; K = 1
if '--scale' in ARGS: i = ARGS.index('--scale'); K = int(ARGS[i + 1]); del ARGS[i:i + 2]
bad = 0
for s, st, n in FM.SHOTS:
    if ARGS and s not in ARGS: continue
    if not os.path.exists(shot_file(s, K)): print(f'{s:4s} MISSING'); bad = 1; continue
    x = load(s); msg = []
    if len(x) != n: msg.append(f'LENGTH {len(x)} != {n}'); bad = 1
    lum = x.mean((1, 2, 3)); sd = x.std((1, 2, 3)); d = np.abs(np.diff(x, axis=0)).mean((1, 2, 3))
    for a, b in runs(sd < .006):
        if b - a >= 2 and s not in DARK_OK: msg.append(f'blank {a}-{b}'); bad = 1
        elif b - a >= 2: msg.append(f'(blank {a}-{b}, allowed)')
    lim = FREEZE_OK.get(s, 5)
    for a, b in runs(d < .0016):
        if b - a >= lim: msg.append(f'still {a}-{b + 1}')
    e = np.abs(x[2:] - x[:-2]).mean((1, 2, 3)); fl = [i + 1 for i in range(len(e)) if d[i] > .05 and d[i + 1] > .05 and e[i] < .35 * min(d[i], d[i + 1])]
    if fl: msg.append('flash/flicker at ' + ','.join(map(str, fl)))
    cut = [i + 1 for i in range(len(d)) if d[i] > .16]
    if cut: msg.append('jumps at ' + ','.join(map(str, cut)))
    hot = (x.min(-1) > .985).mean((1, 2)); q = runs(hot > .45)
    if q: msg.append('white ' + ' '.join(f'{a}-{b}' for a, b in q))
    print(f'{s:4s} {len(x):4d}f  lum {lum.min():.2f}..{lum.max():.2f}  motion {np.median(d):.4f}  ' + ('; '.join(msg) or 'ok'))
sys.exit(bad)
