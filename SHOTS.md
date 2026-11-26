# Making a shot

Read ENGINE.md first, then the shots that are already finished: `shots/a1.py`, `a2.py`, `e1.py`, `f8.py`, `f10.py`, `g5.py`. They set the standard. The storyboard is `film.BOARD`; the number of frames, and every frame it names, is a promise to the soundtrack.

## The contract

* One module per shot, `shots/<id>.py`, with `class Shot(ShotBase)`, `id`, `n` equal to `film.LEN[id]`, `EVENTS`, `setup(st)`, `frame(f, st)`. A helper module `shots/<act>_kit.py` is fine when several shots share a set.
* `frame(f, st)` depends on nothing but `f` and what `setup` built. Frames are rendered out of order.
* `EVENTS = [(frame, 'name', {...})]` lists everything that should be heard, in plain words, on the exact frame it is seen (footstep, hit, splash, wing beat, cloth, crowd, fire ...). Use `dict(dur=frames)` for things that last.
* Write only your own shot files, and `qa/<id>/` for pictures. Do not edit `lau/`, `tools/`, `film.py`, `chars/`, `worlds/`, `audio/` or other people's shots. If something there is wrong or missing, work around it in your file and say so in your report.
* Under about 1 s per frame; `setup` under about 40 s.

## How to work

1. Read the storyboard line and the notes you were given. Decide the one picture you would print. Block it: where is the camera, what is near, what is far, where is the light, where does the eye go.
2. Build that picture as a single frame and look at it at full size (`tools/still.py <id> <f>`, then open the jpg with Read). Do not animate until it is good.
3. Animate: anticipation, action, follow-through, settle. Figures on twos with `on2(f)`, camera on ones. Motion arcs, not straight lines. Cloth, hair, tails and ribbons lag. Something alive in the background (leaves, dust, birds, banners, embers, water).
4. Check strips of every moving range (`--strip 0:96:6`, then `--strip a:b:1` round the fast actions). Look at them. Fix popping, sliding feet, floating or sunk figures, hands through props, backward knees, clipped limbs, props detached from hands, faces turned away at the moment that matters, flicker, dead backgrounds, empty frames.
5. Check cuts: your first frame must read in a quarter of a second; your last frame must hand over to the next shot (a shape, a light, a direction).
6. `tools/render.py <id>`, then `tools/check.py <id>`, then `tools/scale.py <id>` (the film is delivered at 3840x2160, so the shot must draw the same picture at 2x), then `tools/sheet.py <id> 12` and look at the sheet once more.

## What makes it good

* Composition before effects. Big shapes, clear silhouette, one focal point, light on it. If the frame is muddled, remove things.
* The camera always has an intention: it pushes toward, pulls away, follows, or waits. No drifting for its own sake. Use long lenses (fov 16 to 24) for faces, wide and low (40 to 55) for giants and action.
* Faces: light the eyes. Aim `gx, gy` where the character is looking. Change expression on a beat, not continuously.
* Give every shot one light idea and one colour idea from the act's script (see ENGINE.md, Taste). Dark shots still need a readable bright shape.
* Effects support the beat. One `IM.inkflash` of one or two frames, at the hit, at most.
* Ornament frames calm: bands, halos, borders against flat colour.
* Reverence: no comedy at the expense of Rama, Sita, Lakshmana, Hanuman; no blood.
* The flame is in every shot that the storyboard says it is. It is the thread; make it findable.
* Exposure: check that nothing large is blown to flat white or crushed to flat black unless the storyboard says so. Warm light on Rama's blue skin should glow, not turn green.
