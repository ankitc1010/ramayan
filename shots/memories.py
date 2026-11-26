"""Frames of other shots, kept as small pictures: f9's tunnel is hung with them.  A picture is rendered once and cached until its shot file changes."""
import hashlib
import importlib
import os

import cv2
import numpy as np

from lau import CACHE, ROOT, gl

PICK = [('a1', 58), ('a2', 84), ('a3', 60), ('a4', 92), ('a5', 34), ('b1', 24), ('b3', 30), ('c1', 30), ('c3', 26), ('c4', 72), ('c6', 26), ('c7', 45), ('d1', 62), ('d3', 62), ('d4', 57), ('d5', 62), ('d6', 64), ('d7', 46), ('d8', 121),
        ('d8', 155), ('e1', 62), ('e2', 66), ('f1', 90), ('f2', 33), ('f3', 63), ('f4', 74), ('f5', 30), ('f6', 26), ('f7', 84)]          # in the order they were lived
SIZE = (960, 540)


def picture(name, frame, st):
    path = os.path.join(ROOT, 'shots', name + '.py')
    if not os.path.exists(path):
        return None
    stamp = hashlib.md5(open(path, 'rb').read()).hexdigest()[:10]
    kept = os.path.join(CACHE, f'mem_{name}_{frame}_{SIZE[0]}_{stamp}.npy')
    if os.path.exists(kept):
        return np.load(kept)
    try:
        shot = importlib.import_module('shots.' + name).Shot()
        shot.setup(st)
        small = cv2.resize(shot.frame(frame, st), SIZE, interpolation=cv2.INTER_AREA)
    except Exception as why:
        print('no memory of', name, repr(why)[:120])
        return None
    np.save(kept, small)
    return small


def wall(st):
    """a texture array of every picture that exists"""
    have = [p for p in (picture(n, f, st) for n, f in PICK) if p is not None]
    data = np.concatenate([p[::-1].tobytes() and np.frombuffer(np.ascontiguousarray(p[::-1]).tobytes(), np.uint8) for p in have])
    t = gl.ctx().texture_array((SIZE[0], SIZE[1], len(have)), 3, data.tobytes(), alignment=1)
    t.build_mipmaps()
    t.filter = (gl.mgl.LINEAR_MIPMAP_LINEAR, gl.mgl.LINEAR)
    t.repeat_x = t.repeat_y = False
    t.anisotropy = 8.
    return t, len(have)
