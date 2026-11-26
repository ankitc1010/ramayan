"""Base class of a shot module."""
from .stage import *
from .cam import Cam, orbit
from .rig import Pose, solve, HANDS, V, nz, eul
from .face import Face
from .ease import *
from . import poses as PZ, props as PR, cloth as CL, fx as FX, impact as IM, letters as LT, gl, W, H
from .plates import plate, rgb, poly, smooth_path, ink, blob
from .crowd import Crowd
import numpy as np, math, cairo


class ShotBase:
    id = ''; n = 0
    EVENTS = []                         # [(frame, 'what is heard', {..})] for the sound mix

    def setup(self, st): pass

    def frame(self, f, st): raise NotImplementedError
