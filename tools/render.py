"""Render one shot to out/<shot>.mkv:  render.py a4 [--range 20:60] [--out other.mkv] [--ss 2] [--scale 2, 3840x2160 into out/x2/]"""
import argparse
import sys
from time import perf_counter

from common import Runner, VideoFile, shot_file
import film

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('shot')
p.add_argument('--range', default='')
p.add_argument('--out')
p.add_argument('--ss', type=int, default=2)
p.add_argument('--scale', type=int, default=1)
o = p.parse_args()

began = perf_counter()
runner = Runner(o.shot, o.ss, o.scale)
if runner.shot.n != film.LEN[o.shot]:
    sys.exit(f'{o.shot} says {runner.shot.n} frames, the storyboard says {film.LEN[o.shot]}')
first, last = (int(v) for v in o.range.split(':')) if o.range else (0, runner.shot.n)
path = o.out or shot_file(o.shot, o.scale)
with VideoFile(path, size=runner.size) as video:
    for f in range(first, last):
        video.add(runner[f])
print(f'{path}: {last - first} frames in {perf_counter() - began:.0f}s')
