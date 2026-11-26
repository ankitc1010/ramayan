"""The whole film.
    film.py                     render every shot that is missing or has the wrong length (--jobs N at a time)
    film.py --only a1,d4        render these again
    film.py --all               render everything again
    film.py --join              join the shots and out/soundtrack.wav into dist/lau.mp4  (--silent leaves the sound out)
    --scale 2                   all of the above at 3840x2160: shots in out/x2/, the film in dist/lau.2160p.<codec>.mp4
    --codec x265                join as 10-bit HEVC instead of 8-bit H.264"""
import argparse
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from common import BIN, BT709, SIZE, TAGGED, length, shot_file
import film

CODECS = {
    'x264': dict(crf='18', args='-pix_fmt yuv420p -c:v libx264 -profile:v high -preset slow -x264-params keyint=48:aq-mode=3'),
    'x265': dict(crf='22', args='-pix_fmt yuv420p10le -c:v libx265 -profile:v main10 -preset slow -tag:v hvc1 -x265-params keyint=48:min-keyint=24:aq-mode=3:colorprim=bt709:transfer=bt709:colormatrix=bt709:range=limited:log-level=error'),
}


def render(name, k):
    done = subprocess.run([str(BIN / 'python'), 'tools/render.py', name, '--scale', str(k)], capture_output=True, text=True)
    good = done.returncode == 0
    print(done.stdout.strip().splitlines()[-1] if good and done.stdout.strip() else f'{name} FAILED\n' + done.stderr[-1200:], flush=True)
    return good


def choose(o):
    built = [s for s in film.LEN if Path(f'shots/{s}.py').exists()]
    if o.only:
        return o.only.split(',')
    return built if o.all else [s for s in built if length(shot_file(s, o.scale)) != film.LEN[s]]


def join(o):
    short = {s: length(shot_file(s, o.scale)) for s in film.LEN if length(shot_file(s, o.scale)) != film.LEN[s]}
    if short:
        sys.exit(f'cannot join, wrong or missing: {short}')
    reel_list = Path(shot_file('reel', o.scale).with_suffix('.txt'))
    reel_list.write_text('\n'.join(f"file '{shot_file(s, o.scale).resolve()}'" for s in film.LEN))
    reel = ['-f', 'concat', '-safe', '0', '-i', str(reel_list)]
    sound = [] if o.silent else ['-i', 'out/soundtrack.wav']
    words = ['-i', 'dist/lau.en.srt'] if sound and Path('dist/lau.en.srt').exists() else []
    tracks = (sound and '-map 1:a:0 -c:a aac -b:a 320k'.split()) + (words and '-map 2:s:0 -c:s mov_text -metadata:s:s:0 language=eng -disposition:s:0 0'.split())
    codec = CODECS[o.codec]
    picture = ['-map', '0:v:0', '-vf', TAGGED, '-r', '24', *codec['args'].split(), '-crf', o.crf or codec['crf'], *BT709]
    out = o.out or ('dist/lau.mp4' if o.scale == 1 and o.codec == 'x264' else f'dist/lau.{SIZE[1] * o.scale}p.{o.codec}.mp4')
    Path(out).parent.mkdir(exist_ok=True)
    made = subprocess.run([str(BIN / 'ffmpeg'), '-v', 'error', '-y', *reel, *sound, *words, *picture, *tracks, '-movflags', '+faststart', out])
    if made.returncode:
        sys.exit('ffmpeg could not join the film')
    print(out, length(out), 'frames')


p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
p.add_argument('--only')
p.add_argument('--all', action='store_true')
p.add_argument('--jobs', type=int, default=3)
p.add_argument('--join', action='store_true')
p.add_argument('--silent', action='store_true')
p.add_argument('--scale', type=int, default=1)
p.add_argument('--codec', choices=list(CODECS), default='x264')
p.add_argument('--crf')
p.add_argument('--out')
o = p.parse_args()
if o.only or not o.join:
    with ThreadPoolExecutor(o.jobs) as pool:
        if not all(pool.map(lambda s: render(s, o.scale), choose(o))):
            sys.exit(1)
if o.join:
    join(o)
