"""What the command-line tools share: finding the project, running one shot, writing video, laying out contact sheets."""
import importlib
import os
import subprocess
import sys
import threading
from pathlib import Path
from queue import Queue

HOME = Path(__file__).resolve().parent.parent
os.chdir(HOME)
if str(HOME) not in sys.path:
    sys.path.insert(0, str(HOME))

import numpy as np  # noqa: E402

BIN = HOME / '.mm/env/bin'
SIZE = (1920, 1080)
TAGGED = 'scale=out_color_matrix=bt709:out_range=tv,setparams=range=tv:colorspace=bt709:color_primaries=bt709:color_trc=bt709'
BT709 = ['-color_range', 'tv', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709']


def shot_file(name, k=1):
    """where a shot's video lives; each output scale keeps its own"""
    return Path('out', f'{name}.mkv') if k == 1 else Path('out', f'x{k}', f'{name}.mkv')


class Runner:
    """one shot on its own stage; runner[f] is the finished frame f, k times SIZE"""

    def __init__(self, name, ss=2, k=1):
        from lau.stage import Stage
        self.shot = importlib.import_module(f'shots.{name}').Shot()
        self.stage = Stage(ss, k=k)
        self.size = (SIZE[0] * k, SIZE[1] * k)
        self.shot.setup(self.stage)

    def __getitem__(self, f):
        picture = self.shot.frame(f, self.stage)
        if picture.shape != (self.size[1], self.size[0], 3):
            raise ValueError(f'frame {f} has shape {picture.shape}')
        return picture


class VideoFile:
    """with VideoFile(path) as v: v.add(frame).  Encoding runs beside the renderer; the file appears only when it is complete."""

    def __init__(self, path, quality=7, size=SIZE):
        self.path, self.part = Path(path), Path(str(path) + '.part.mkv')
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.command = [str(BIN / 'ffmpeg'), '-v', 'error', '-y', '-f', 'rawvideo', '-pixel_format', 'rgb24', '-video_size', '%dx%d' % size, '-framerate', '24', '-i', 'pipe:0',
                        '-vf', TAGGED, '-c:v', 'libx264', '-preset', 'veryfast', '-crf', str(quality), '-pix_fmt', 'yuv444p', *BT709, str(self.part)]

    def __enter__(self):
        self.process = subprocess.Popen(self.command, stdin=subprocess.PIPE)
        self.frames = Queue(maxsize=6)
        self.writer = threading.Thread(target=self._drain, daemon=True)
        self.writer.start()
        return self

    def _drain(self):
        while (frame := self.frames.get()) is not None:
            self.process.stdin.write(frame)

    def add(self, picture):
        self.frames.put(picture.tobytes())

    def __exit__(self, kind, *rest):
        self.frames.put(None)
        self.writer.join()
        self.process.stdin.close()
        if self.process.wait() == 0 and kind is None:
            self.part.replace(self.path)
        else:
            self.part.unlink(missing_ok=True)


def length(path):
    """number of video frames in a file, 0 when there is none"""
    if not Path(path).exists():
        return 0
    probe = subprocess.run([str(BIN / 'ffprobe'), '-v', 'error', '-select_streams', 'v:0', '-count_packets', '-print_format', 'default=nw=1:nk=1', '-show_entries', 'stream=nb_read_packets', str(path)], capture_output=True, text=True)
    digits = ''.join(ch for ch in probe.stdout if ch.isdigit())
    return int(digits or 0)


def contact_sheet(pictures, labels, columns=3, width=640):
    """RGB pictures laid out in a grid, each with its frame number"""
    import cv2
    height = width * SIZE[1] // SIZE[0]
    rows = -(-len(pictures) // columns)
    page = np.zeros((rows * height, columns * width, 3), np.uint8)
    for k, (picture, label) in enumerate(zip(pictures, labels)):
        y, x = divmod(k, columns)
        cell = cv2.resize(picture, (width, height), interpolation=cv2.INTER_AREA)
        cv2.putText(cell, str(label), (10, height - 12), cv2.FONT_HERSHEY_SIMPLEX, .6, (255, 240, 0), 2, cv2.LINE_AA)
        page[y * height:(y + 1) * height, x * width:(x + 1) * width] = cell
    return page


def save(path, picture, quality=91):
    import cv2
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(path), picture[..., ::-1], [cv2.IMWRITE_JPEG_QUALITY, quality])
    print(path)
