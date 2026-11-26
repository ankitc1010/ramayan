"""Prove that a shot draws the same picture at every output scale.
    scale.py a2 b1                    frames of each shot at 1x and 2x; the 2x picture, shrunk to 1x, is compared with the 1x one
    scale.py --all --at 4             every shot, 4 frames each spread over the shot (default 3)
    scale.py dump DIR --scale 1 a2    only write raw frames, DIR/<shot>_<frame>.npy
    scale.py same DIR a2              this code's 1x frames against a dump, bit for bit
Pictures go to qa/scale/ (1x | 2x shrunk | difference x4), numbers to qa/scale/report.txt."""
import argparse
import subprocess
import sys
from pathlib import Path

import numpy as np

from common import BIN, HOME, save
import film


def frames_of(shot, at):
    n = film.LEN[shot]
    return sorted({round(i * (n - 1) / max(at - 1, 1)) for i in range(at)})


def dump(folder, scale, shots, at):
    from common import Runner
    Path(folder).mkdir(parents=True, exist_ok=True)
    for shot in shots:
        runner = Runner(shot, 2, scale) if scale != 1 else Runner(shot, 2)
        for f in frames_of(shot, at):
            np.save(f'{folder}/{shot}_{f}.npy', runner[f])
        print(shot, 'dumped', flush=True)


def run_dump(folder, scale, shots, at):
    """each shot in its own process, so one shot's GPU state never leaks into the next"""
    for shot in shots:
        done = subprocess.run([str(BIN / 'python'), __file__, 'dump', folder, '--scale', str(scale), '--at', str(at), shot], cwd=HOME, capture_output=True, text=True)
        if done.returncode:
            print(shot, 'FAILED', done.stderr[-1500:], flush=True)


def soften(a):
    import cv2
    return cv2.GaussianBlur(a.astype(np.float32), (0, 0), 1.6)


def compare(one, two, shots, at, out='qa/scale'):
    """worst = 99.9th percentile of the blurred difference, in 8-bit levels; grain and edge sharpness blur away, a moved or missing thing does not"""
    import cv2
    Path(out).mkdir(parents=True, exist_ok=True)
    lines = []
    for shot in shots:
        for f in frames_of(shot, at):
            a, b = Path(f'{one}/{shot}_{f}.npy'), Path(f'{two}/{shot}_{f}.npy')
            if not (a.exists() and b.exists()):
                lines.append(f'{shot} {f:4d}  missing'); continue
            a, b = np.load(a), np.load(b)
            if b.shape != a.shape:
                b = cv2.resize(b, (a.shape[1], a.shape[0]), interpolation=cv2.INTER_AREA)
            d = np.abs(soften(a) - soften(b)).max(2)
            worst, mean = float(np.percentile(d, 99.9)), float(d.mean())
            lines.append(f'{shot} {f:4d}  mean {mean:5.2f}  worst {worst:6.2f}')
            save(f'{out}/{shot}_{f:04d}.jpg', np.hstack([a, b, np.clip(d * 4, 0, 255).astype(np.uint8)[..., None].repeat(3, 2)])[::2, ::2], 85)
    Path(f'{out}/report.txt').write_text('\n'.join(lines) + '\n')
    print('\n'.join(lines))


def same(folder, shots, at):
    from common import Runner
    for shot in shots:
        runner = Runner(shot, 2)
        for f in frames_of(shot, at):
            kept = np.load(f'{folder}/{shot}_{f}.npy'); now = runner[f]
            changed = int((kept != now).any(2).sum())
            print(f'{shot} {f:4d}  {"same" if changed == 0 else f"{changed} pixels differ, max {int(np.abs(kept.astype(int) - now).max())}"}', flush=True)


p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
p.add_argument('words', nargs='*')
p.add_argument('--all', action='store_true')
p.add_argument('--at', type=int, default=3)
p.add_argument('--scale', type=int, default=2)
o = p.parse_intermixed_args()
verb = o.words[0] if o.words and o.words[0] in ('dump', 'same') else 'check'
rest = o.words[1:] if verb != 'check' else o.words
if verb == 'dump':
    dump(rest[0], o.scale, rest[1:] or list(film.LEN), o.at)
elif verb == 'same':
    same(rest[0], rest[1:] or list(film.LEN), o.at)
else:
    shots = list(film.LEN) if o.all else rest
    if not shots:
        sys.exit('name the shots, or --all')
    for k in (1, o.scale):
        run_dump(f'cache/scale/x{k}', k, shots, o.at)
    compare('cache/scale/x1', f'cache/scale/x{o.scale}', shots, o.at)
