"""Contact sheet of a rendered shot:  sheet.py a4 [9]  -> qa/sheet_a4.jpg"""
import subprocess
import sys

from common import BIN, contact_sheet, length, save
import numpy as np

name, count = sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 9
total = length(f'out/{name}.mkv')
picks = np.unique(np.linspace(0, total - 1, count).round().astype(int))
raw = subprocess.run([str(BIN / 'ffmpeg'), '-v', 'error', '-i', f'out/{name}.mkv', '-vf', 'scale=640:360', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
clip = np.frombuffer(raw, np.uint8).reshape(-1, 360, 640, 3)
save(f'qa/sheet_{name}.jpg', contact_sheet([clip[i] for i in picks], picks), 88)
