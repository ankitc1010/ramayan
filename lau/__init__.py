"""LAU engine: a ray-marched, inked, gold-leafed picture machine.  24 fps, 1920x1080."""
import os
os.environ.setdefault('__EGL_VENDOR_LIBRARY_FILENAMES', '/usr/share/glvnd/egl_vendor.d/10_nvidia.json')
from pathlib import Path
ROOT = str(Path(__file__).resolve().parent.parent)
CACHE = os.path.join(ROOT, 'cache')
os.makedirs(CACHE, exist_ok=True)
W, H, FPS = 1920, 1080, 24
