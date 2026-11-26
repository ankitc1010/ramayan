"""Cameras.  y up, right handed."""
import numpy as np, math
from . import W, H
V = lambda *a: np.array(a, float)


class Cam:
    def __init__(self, eye, at, fov=32., roll=0., up=(0, 1, 0)):
        self.eye = np.asarray(eye, float); self.at = np.asarray(at, float); f = self.at - self.eye; f /= np.linalg.norm(f)
        up = np.asarray(up, float)
        if abs(f @ up) > .9995: up = V(0, 0, -1.) if f[1] < 0 else V(0, 0, 1.)
        r = np.cross(f, up); r /= np.linalg.norm(r); u = np.cross(r, f)
        if roll: c, s = math.cos(math.radians(roll)), math.sin(math.radians(roll)); r, u = r * c + u * s, u * c - r * s
        self.R = np.stack([r, u, f]); self.fl = 1 / math.tan(math.radians(fov) / 2); self.fov = fov

    def project(self, P):
        """world point(s) -> pixel x, y (y down) and depth"""
        c = (np.asarray(P, float) - self.eye) @ self.R.T; z = np.maximum(c[..., 2], 1e-3)
        return np.stack([W / 2 + c[..., 0] / z * self.fl * H / 2, H / 2 - c[..., 1] / z * self.fl * H / 2, c[..., 2]], -1)

    def px(self, P):
        """pixels per world unit at P"""
        z = max(1e-3, float(((np.asarray(P, float) - self.eye) @ self.R.T)[2])); return self.fl * H / 2 / z

    def ray(self, x, y):
        s = V((x / W * 2 - 1) * W / H, 1 - y / H * 2, self.fl); d = s @ self.R; return d / np.linalg.norm(d)

    def u(self): return dict(ro=tuple(self.eye), CamR=self.R, fl=self.fl)


def orbit(at, dist, yaw, pitch, **k):
    """camera on a sphere round `at`; yaw 0 looks along -z (sees a figure that faces +z from the front)"""
    a, b = math.radians(yaw), math.radians(pitch); at = np.asarray(at, float)
    return Cam(at + dist * V(math.sin(a) * math.cos(b), math.sin(b), math.cos(a) * math.cos(b)), at, **k)
