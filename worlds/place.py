"""Common to the places: draw(st, 'ayodhya.glsl', ...) = st.world with the places' head and marcher and the light's colours as uniforms."""
from lau.stage import hexc
from lau.rig import nz


def draw(st, src, u=None, texs=None, defs='', shadow=False, sun=1.):
    L = st.light
    st.world(src, u=dict(uAmb=hexc(L.amb), uKey=hexc(L.keyCol), sunSh=float(sun), **{k: (hexc(v) if isinstance(v, str) else v) for k, v in (u or {}).items()}), texs=texs, defs=defs, shadow=shadow, head='place_head.glsl', main='place_main.glsl')
