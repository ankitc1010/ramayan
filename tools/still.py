"""Look at a shot.
    still.py a4 10 40                 full pictures, qa/a4/f0010.jpg ...
    still.py a4 --strip 0:108:9       a contact sheet of a range, qa/a4/sheet.jpg  (--sheet does the same for listed frames, --cols N)
    still.py a4 84 --crop 700,300,700,500    also cut out a 1:1 detail
    --ss 1 is faster and rougher; --k 2 draws at 3840x2160; --out DIR puts the pictures elsewhere"""
import argparse
from time import perf_counter

from common import Runner, contact_sheet, save


def options():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('shot')
    p.add_argument('frame', nargs='*', type=int)
    p.add_argument('--strip', metavar='FROM:TO:STEP')
    p.add_argument('--sheet', action='store_true')
    p.add_argument('--cols', type=int, default=3)
    p.add_argument('--crop', metavar='X,Y,W,H', action='append', default=[])
    p.add_argument('--ss', type=int, default=2)
    p.add_argument('--k', type=int, default=1)
    p.add_argument('--scale', type=float, default=1.0)
    p.add_argument('--out')
    return p.parse_args()


def main():
    o = options()
    wanted = o.frame + (list(range(*map(int, o.strip.split(':')))) if o.strip else [])
    folder = o.out or f'qa/{o.shot}'
    began = perf_counter()
    shot = Runner(o.shot, o.ss, o.k)
    print(f'ready in {perf_counter() - began:.1f}s')
    kept = []
    for f in wanted:
        began = perf_counter()
        picture = shot[f]
        print(f, f'{perf_counter() - began:.2f}s')
        for k, box in enumerate(o.crop):
            x, y, w, h = map(int, box.split(','))
            save(f'{folder}/f{f:04d}_c{k}.jpg', picture[y:y + h, x:x + w], 94)
        if o.strip or o.sheet:
            kept.append(picture)
        else:
            if o.scale != 1:
                import cv2
                picture = cv2.resize(picture, None, fx=o.scale, fy=o.scale, interpolation=cv2.INTER_AREA)
            save(f'{folder}/f{f:04d}.jpg', picture)
    if kept:
        save(f'{folder}/sheet.jpg', contact_sheet(kept, wanted, o.cols), 88)


main()
