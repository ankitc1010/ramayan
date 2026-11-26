# लौ (LAU)

The *Ramayana* as one flame: a 155-second animated film drawn, animated, scored and sung entirely in code.
3840×2160 (drawn natively, not upscaled; 1920×1080 also builds), 24 fps, 3,738 frames, 41 shots.

लौ is the flame of a lamp. In Hindi it is also the word for devotion, for being held by someone the way a wick holds fire. The film follows one flame. It is lit behind a shadow-puppet cloth and becomes the sun over Ayodhya and the wedding fire. It is the line Lakshmana draws, the spark in the ring Hanuman carries over the sea, the fire on his tail and the burning of Lanka. Rama's last arrow gathers it. It comes home as ten thousand lamps that write राम from above, and it is passed, wick to wick, to a child.

No image models, no image files, no samples, no text-to-speech, no fonts on screen. The picture is Python and GLSL on one GPU (moderngl, numpy, pycairo, opencv). The sound is Python (numpy, scipy, numba).

## Build

An NVIDIA GPU with EGL (made on an RTX 2060 SUPER), Linux, conda. From this directory:

```bash
conda create -y -p .mm/env -c conda-forge --override-channels python=3.12 numpy opencv pycairo scipy pillow numba ffmpeg moderngl scikit-image
./.mm/env/bin/python audio/make.py                                    # sound, out/soundtrack.wav
./.mm/env/bin/python tools/film.py --scale 2 --jobs 1                 # picture at 3840x2160, one file per shot in out/x2/
./.mm/env/bin/python tools/film.py --scale 2 --join --codec x265      # dist/lau.2160p.x265.mp4, 10-bit HEVC
./.mm/env/bin/python tools/film.py --jobs 1 && ./.mm/env/bin/python tools/film.py --join   # or 1920x1080 H.264, dist/lau.mp4
```

One job at a time: on an 8 GB card three 4K jobs fill the GPU, and on the machine this was made on that ended in a reboot.

One frame: `./.mm/env/bin/python tools/still.py d3 46`, which writes `qa/d3/f0046.jpg`.

## What is where

| Path | What it does |
|---|---|
| `film.py` | the timeline and the storyboard |
| `lau/` | the engine: ray-marched inked figures, gold leaf, skies, seas, cloth, crowds, fire, print-frame flashes, reed-pen Devanagari |
| `chars/` | the cast: one GLSL body and one Python file of poses and faces each |
| `worlds/` | cities, halls, forests, painted trees, ornament, the lamp |
| `shots/` | the 41 shots, one module each |
| `audio/` | score, voices, instruments, effects, mix |
| `tools/` | stills, strips, renders, the film checker, the originality checker |
| `ENGINE.md`, `SHOTS.md` | how to draw something new |

## Credits and source

The *Ramayana* belongs to everyone. All drawing, music and words here are original code. The idea of a whole film in code came from [don-film](https://github.com/ChetasLua/don-film) by ChetasLua; no code from it is used (`tools/overlap.py` checks).

## License

MIT, see [LICENSE](LICENSE).
