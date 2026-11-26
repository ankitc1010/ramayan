# The LAU engine, for anyone drawing a character, a place or a shot

Run everything from the repository root with `./.mm/env/bin/python`. Python draws; the GPU does the work. A frame takes 0.2 to 0.6 s, so look often.

Rules of the film: no image files, no fonts, no samples, no network, no downloaded assets, no generative models. Everything on screen is code in this repository. All work is original. Never copy code from another project.

## The picture

A frame is a canvas (`st.C`, linear light) built in passes. Shots draw in 1920x1080 picture pixels (`st.wd`, `st.ht`) whatever the output size; the stage has `st.k` output pixels per picture pixel (2 for 3840x2160), so the canvas is `st.pw` x `st.ph`. Anything sized to the canvas uses those: a texture you copy the canvas into is `(st.pw, st.ph)`, a viewport onto `st.C` is `(0, 0, st.pw, st.ph)`, the depth of the last `close()` per picture pixel is `st.depth()`. `tools/scale.py <shot>` draws a shot at 1x and 2x and shows what moved.

```python
from lau.shot import *
from chars import rama

class Shot(ShotBase):
    id = 'e0'; n = 96
    EVENTS = [(42, 'stone drops', {})]          # (frame, what is heard): the sound mix reads this

    def setup(self, st):                        # once: crowds, plates, simulations
        ...
    def frame(self, f, st):                     # any frame on its own, deterministic, no state carried from frame to frame
        st.clear('#000000', f=f)                # always first; sets st.t = f/24
        cam = Cam((7, 4.6, 27), (0, 8.6, 0), 34)     # eye, target, vertical fov (degrees), roll=
        st.cam = cam                                  # needed before paint() uses the camera
        st.paint('sky.frag', **SKY)                   # full-screen shader, 2-D or camera-aware
        st.open(cam, Light(...))                      # 3-D G-buffer (4K, supersampled)
        S = st.fig(rama.EXILE, PZ.archer(1.), at=(0, 0, 0), yaw=28, face=Face(frown=.4))
        st.world(GLSL, u=dict(...))                   # ray-marched scenery
        st.mesh(*CL.strip(...), kind=1, col=(...))    # cloth, ropes, banners
        st.close()                                    # shade, ink, composite; after this effects are depth-tested against it
        FX.flame(st, tip, 1.5); FX.drift(...)         # fire, sparks, petals
        st.vector(lambda c: ...)                      # cairo overlay, 1920x1080, y down
        return st.finish(bloom=.5)                    # uint8 image
```

You may call `open/close` several times for layers (each composites over the canvas; effects test against the latest one).

Look at your work:

```bash
./.mm/env/bin/python tools/still.py a4 0 40 84            # qa/a4/f0040.jpg
./.mm/env/bin/python tools/still.py a4 --strip 0:108:12   # contact sheet qa/a4/sheet.jpg
./.mm/env/bin/python tools/still.py a4 84 --crop 700,300,700,500
./.mm/env/bin/python tools/render.py a4                   # out/a4.mkv  (--scale 2: out/x2/a4.mkv)
./.mm/env/bin/python tools/scale.py a4                    # the same frames at 1x and 2x, qa/scale/
```

## Units and axes

World: y up, right handed. A figure faces **+z**; its own **left is +x** (screen right when it faces the camera). `yaw` turns it to its left (yaw=90 faces +x). One unit = half a head; an adult is about 15.5 units tall, eye height about 13.8, chest 11.3, hip 8.3. Feet at y=0. `scale` scales a figure.

## Figures (`lau/stage.py`, `lau/rig.py`, `lau/poses.py`)

`st.fig(fig, pose, at=, yaw=, pitch=, roll=, scale=, face=, u={...})` draws and returns `S` (Solved): `S.palm('L')`, `S.head((x,y,z))`, `S.chest(...)`, `S.pelvis(...)` give world points; `S.joint(i)` gives joints (0 pelvis 1 chest 2 neck 3 head 4/5/6 left shoulder/elbow/wrist 7/8/9 right 10..13 left hip/knee/ankle/toe 14..17 right). `S.hand('R', (x,y,z))` gives a direction of the hand frame (x thumb side, y fingers, z out of the palm). `draw=False` only solves.

`Pose` (all in degrees and figure units): `pel` pelvis position, `pelr/cher/hedr` = (yaw, pitch, roll) of pelvis, chest (relative), head (relative); pitch > 0 bows forward, yaw > 0 turns to its left, roll > 0 leans to its left. `lh/rh` wrist targets in figure space (IK), `lel/rel` elbow directions, `lhand/rhand` hand shapes (`rig.HANDS`: open relax fist grip hold point two draw anjali abhaya cup claw flat pinch katak), `lfing/rfing` finger direction, `lpalm/rpalm` palm direction, `lf/rf` ankle targets (standing = y .75), `lkn/rkn` knee directions, `lft/rft` foot (yaw, pitch). `pose.set(...)` copies with changes, `a.mix(b, t)` blends, `keys(f, [(0, A), (12, B, 'back'), (20, C)])` animates poses, faces, numbers or tuples. Library: `PZ.STAND CONTRA archer(draw) walk(phase) run(phase) KNEEL BOW_DOWN ANJALI SIT BLESS`. Build your own poses; check them from the shot camera.

`Face(lid, gx, gy, brow, frown, sad, smile, mouth, teeth, tear, squint, pupil, glow, spark)`: `spark=1` puts a flame in the eyes.

Acting: hold poses, move between them fast, overshoot and settle. Animate figures on twos (`on2(f)`) and the camera on ones. Every move has anticipation and follow-through. Ribbons, hair, sashes lag behind (`CL.lag` takes the anchor as a function of time).

## Props and cloth

`PR.bow_and_arrow(st, S, side='L', arrow=True)` strings a bow between the two hands and returns (nock, tip, aim). `PR.BOW ARROW GADA SWORD RING DIYA SANDAL SPEAR QUIVER STONE CROWN`, placed with `st.fig(PR.GADA, M=PR.place(origin, y_axis, z_axis, scale))`.
`CL.lag(anchor_fn, t, n, length, wind=, grav=, wave=)` then `CL.strip(points, widths, up=, n=40)` gives a mesh for `st.mesh(..., kind=0 plain 1 border 2 dots 4 banner 6 feather 7 checks, col=(base, shadow, accent), cls=8)`. `CL.tube(points, radii)` is a rope or tail, `CL.sheet(fn)` any surface. `st.mesh(kind=3, texs=dict(tCard=tex), cls=6, ink=0)` puts a painted plate in 3-D.

## Inserts: one arm

`chars/armonly.py`: `ARM` is a single arm and hand for close shots (palm lines, nails, knuckles). `ARM.variant(pal={1: SKIN['sita']}, u=dict(side=1, band=1, old=0.))`. `place_hand(S, 'R', at, fingers_dir, palm_dir, scale, anchor='palm'|'wrist'|'tip1')` returns the matrix that puts the palm or a fingertip exactly on a point. `u=dict(fore=1.)` leaves out the upper arm. See shots/e1.py.

## Worked shots

`shots/a1.py` (lamp, point light, sparks), `shots/a2.py` (2-D theatre with cairo layers fed to a shader), `shots/e1.py` (insert, under water, sea surface, three set-ups in one shot).

## Scenery

`st.world(src, u=, defs=)`: `src` is GLSL (file in `worlds/` or literal) with `vec2 map(vec3 p)` = (distance, material) and `void surf(vec3 p, vec3 n, int m, inout Surf s)` setting `s.base s.sh` (linear; use `hex(0xrrggbb)`), `s.cls`, `s.ink` (0..1 line weight; below .25 also means "floor": no rim light), `s.part`. `#include "sdf.glsl"` helpers are already in: sEll sCap sCone sTor sBox sCyl smin smax polar rot vn fbm fbm3 voro h21. `fT` is seconds, `ro` the eye, `CamR` the camera rows. Tune with `#define TMAX 600.`, `STEPS`, `RELAX`, `EPS`, `NOAO`. Keep maps cheap: cull with bounding distances, use domain repetition.
Classes: 1 matte (skin, cloth, stone) 2 gold leaf 3 gem 4 emissive 5 hair/fur 6 flat painted 7 dark steel 8 silk/wet.
`sky.frag` (all its uniforms must be given; see `SKY` in `lau/look.py`), `sea.glsl` (seaH, seaPaint). `lau/glsl/noise.glsl` for 2-D painting. `plate(key, w, h, fn)` caches a cairo painting (`ink`, `blob`, `smooth_path` help); draw it flat with `st.plate(tex, x, y, scale)` or in 3-D with `st.mesh(kind=3)`.

## Light

`Light(key=dir, keyCol, amb, rim=dir, rimCol, bounceCol, envT, envM, envB, pts=[(xyz, radius, rgb)], shadow=True, edge, soft, fogCol, fog=(density, start, height falloff, base y), ink=3.2, inkCol, inkRef)`. Directions point toward the light. Colours are hex strings or linear tuples (tuples may exceed 1). `pts` are flames (up to 12). `envT/M/B` are what gold reflects from above, level and below. `inkRef` = world size of the figure unit (set it to `scale` when figures are drawn very large or small). Presets in `lau/look.py`.

## Effects (`lau/fx.py`, `lau/impact.py`)

`FX.flame(st, at, h)` lamp flame (world point + world height, or pixel point + pixels). `FX.ribbon(st, P, width, mode='fire'|'light'|'smoke'|'brush'|'wind'|'gold'|'bolt')` along world or pixel points. `FX.particles` (kinds ember streak petal leaf ash glint smoke tongue rain feather ring dot spark flake drop lamp), `FX.embers`, `FX.burst`, `FX.drift`. A wall of fire = many `tongue` particles.
`IM.speedlines inkflash whip zoomblur shock burn iris defocus dof grade`. Use `inkflash` for one or two frames at a blow, never longer.

`LT.draw(c, 'ram'|'lau'|'ramayan', x, y, h, upto=)` writes Devanagari with a reed pen; `LT.points('ram', spacing)` gives points along the strokes.

## Crowds

`Crowd(st, [(fig, pose, face, yaw), ...], px=360, pitch=camera pitch)` in `setup`, then `cr.draw(pos, scale=, tile=, flip=, tint=)` between open and close. Bake 4 to 8 run or walk phases and step `tile` with time.

## Taste

* Indian mural and miniature painting, staged like the best cel animation. Flat strong shapes, ink, gold that glints, ornament used in bands against calm areas. Strong silhouettes. One light idea per shot.
* Every shot has one picture you would print. Compose it first (thirds, diagonals, framing shapes in the foreground), then move the camera through it.
* Colour script: A amber and dawn rose-gold. B vermilion dusk then seasons. C emerald and gold turning to blood and indigo, ending in blue-grey rain. D rain blue, then saffron sky and turquoise sea, then indigo night and gold, then fire on black. E teal, white, vermilion. F ochre dust and crimson, violet night, then black and gold. G deep indigo and ten thousand warm lamps.
* Depth: something near the lens, the subject, something far. Let things overlap the frame edge.
* Reverence. Rama, Sita, Lakshmana and Hanuman are always dignified; nothing comic, nothing gory (no blood; struck things burst into gold leaf, feathers, sparks, petals).
* Check every frame range you animate with a strip. Look for popping, sliding feet, clipped limbs, hands through props, bent-backward knees, figures floating or sunk, dead backgrounds, empty frames, flicker.

## The cast, quick reference

Sheets in qa/cast_*. Each file's docstring and module-level names have the rest.

**Rama** `chars/rama.py`: PRINCE (crown), BAREHEAD, EXILE, LAKSHMANA, LAKSHMANA_PRINCE. **One arm** `chars/armonly.py`: ARM, HANUMAN_ARM, SKIN, place_hand. **Garlands** `chars/garland.py`: string(st, points, r, 'marigold'|'rose'|'jasmine').
**Sita** `chars/sita.py`: BRIDE, FOREST, GROVE; S_STAND S_WALK(ph) S_GARLAND S_SIT S_PALM S_LOOKUP S_HEART S_STEP; `fit(pose)` adapts lau.poses to her height. Uniforms `look hairm veil lamp old`. Skirt pools when the pelvis is low; keep her ground at y=0. `Wind` (figure space) moves hem and veil.
**People** `chars/people.py`: KAIKEYI (KAIKEYI_EYES for eyes only), DASHARATHA, BHARATA, SAGE, MENDICANT (`u=dict(staff=0., bowl=0.)`), KAUSHALYA, CITIZEN_M[0..2], CITIZEN_F[0..2], CHILD, CHILD_B and `*_LAMP` versions holding a lit diya; `lit(fig, hands)`, `flame(S, hands)` (world point; add your own point light). P_LAMP P_WAVE P_BOW P_NAMASTE P_WALK(ph) P_STAFF P_GIVE D_KING B_SANDALS K_TWO F_LAMP F_WAVE F_NAMASTE F_STAND C_STAND C_LAMP C_WAVE child_pose(p).
**Hanuman** `chars/hanuman.py`: HANUMAN, HANUMAN_CU (face-filling close-ups), `VFace(lidL=, lidR=)`; H_STAND H_ANJALI H_BOW H_KNEEL_PALM H_CROUCH H_LEAP H_FLY (right arm ahead, reads at yaw about -70) H_FLY_L (left arm ahead, reads at yaw 70 to 90) H_FLY2 H_CARRY (left palm up) H_LAND H_PERCH H_BOUND H_ROAR H_RUN(ph) H_WALK(ph) H_SWING(t); `mirror(pose)`, `fit(pose)`; `P = tail(st, S, t, style='calm'|'fly'|'whip'|'up', length=13, wrap=0, path=None|displacement(t), vel=, ground='auto'|y|None)` inside open/close returns 72 world points; `tail_fire(st, P, t, a, b, k, scale)` after close; `sash(st, S, t, wind, vel)`; `gada(st, S, side)`.
**Vanaras** `chars/vanara.py`: KINDS (7), SUGRIVA, ANGADA; `arm(fig, hold, tailw)` hold 0 none 1 rock 2 tree 3 club 4 big stone overhead; V_STAND V_RUN V_CHARGE V_WALK V_CHEER V_THROW(t) V_CARRY V_CARRY_WALK V_CLIMB V_CLIMB2. qa/cast_vanara/crowd.py shows 28 crowd tiles.
**Ravana** `chars/ravana.py` as RV: `RV.fig(st, pose, at=, yaw=, scale=, fan=0..1, arms=0..1, alive=, eyeglow=, lids=, mouths=, navel=, spread=, face=, u=)` (arrays of ten; head 0 is screen-left when he faces us, 4 is the main head); RV.HEAD one loose head; RV.heads(S, fan, spread), RV.eye_points(S, fan), RV.cape(st, S, t), RV.hold(st, S, PR.SWORD); poses R_STAND R_EASE R_LOOM R_THRONE R_LAUGH R_STRUCK R_ARCHER(draw) R_SWORD(t); shadow: RV.silhouette(colour) as the light, **RV.SHADOW layout, RV.shadow_tex(...).
**Rakshasas** `chars/rakshasa.py` as RK: KINDS, SPEARMAN SWORDSMAN HORN_SPEAR, `.variant(u=dict(hold=0..4, shield=0|1))`; K_RUN K_STAB K_GUARD K_FALL K_DOWN K_SHOOT K_CROWD; MARICHA (M_CRY, M_FALLING, face CRY, uniform gild 1..0), INDRAJIT (I_STAND, RK.serpent_bow). **Kumbhakarna** `chars/kumbha.py` as KB: KUMBHA, KB_SLEEP KB_RISE(t) KB_STAND KB_GRAB KB_FALL(t), perches(S), `KB.eye(st, open=, gaze=, flame=, ...)` full-screen eye. Use `scale=12` with Light inkRef=12; draw tiny climbers in a second open/close with inkRef 1.
**Deer** `chars/deer.py`: draw(st, pose, at, yaw, face=, burn=, burn_at=); STAND ALERT look graze step(ph) run(ph) leap(t) struck(t); leaf(st, S, t). **Jatayu** `chars/jatayu.py`: draw(st, pose, at/M, face=, parts=); GLIDE flap(ph) glide dive(t) brake(t) strike(t) wing_lost(t) lying; shed(st, S, t). **Surasa** `chars/serpent.py`: draw(st, gape, at, yaw, scale=10, neck=[points], hood=); rise(t); inkRef about 10. **Horses** `chars/horse.py`; **chariots and Pushpaka** `chars/vehicles.py`: C = chariot(st, 'rama'|'ravana', at, yaw, t, speed, horses=4) then st.fig(..., M=C.stand); P = pushpaka(st, at, yaw, scale=6, mood=0|1, lamps=, glow=) with P.deck, P.lamps(); inkRef about 6. **Birds** `chars/birds.py`: flock, vee, swarm, specks, peacock, squirrel.
Meshes (wings, tails, banners) cast no shadow and cannot be baked into a Crowd. `st.mesh` kind 2 and 7 need `u=dict(rep=(a, b, 0, 0))`. Texture unit 15 is taken by Ravana.

## Places

`worlds/ayodhya.py` as AY: sky(mood), light(mood), draw, trees, lamps, birds, ground(x, z), lamp_points(); moods dawn, day, dusk, night. `worlds/lanka.py`: see its docstring (moon wide, rooftops, fire, far view, gate). `worlds/flora.py`: tree(st, kind, at, height, season), scatter, frame (foreground leaves), many kinds. `worlds/palace.py`, `worlds/forest.py`: halls and forests. `worlds/arch.glsl`, `worlds/orn.glsl` for your own sets; `worlds/place.py` draws a world file with sun shadows. Sheets in qa/places.

## Places: cameras and traps

Always draw a place with its own module's `draw(...)`, never `st.world('ayodhya.glsl')`. Draw the world first in each open(). `st.open(..., far=20000)` for far views (default 4000 drops the rest). `inkRef`: 1 to 3 at figure scale, 4 on Lanka's rooftops, 8 to 14 for wide city views, 30 for the far island.
Tested cameras (eye -> target, fov): a4 hall (0,24,150)->(0,36,-240) 44, dais top y=9 at z -216..-300. b2 gate (0,9,-40)->(0,46,-430) 46. b3 forest track (x,12,74)->(x,15,0) 36 with walkers on z=0 toward +x; FO.track, FO.near, FO.drift, FO.wipe. b4 hut (34,9,62)->(4,13,4) 38, hearth flame at (16,1.5,20). c3 c4 clearing (0,15,100)->(0,20,0) 40, `line=` draws the ring of fire, the rock face for the shadow is z < -46. c7 rain (-26,9,70)->(4,13,0) 38. d5 Lanka (-500,120,3300)->(0,420,0) 34 then (-470,420,1060)->(40,620,0) 46. d6 grove (34,12,74)->(2,24,0) 38, seat top y=2. d7 hall (-12,20,120)->(4,40,-240) 44. d8 roofs (-330,460,800)->(60,500,100) 52 and (-740,560,560)->(-100,520,100) 50, ending (0,130,6200)->(0,240,0) 34 with fire=1, rise=2.2. f1 gate, mood dark, (50,292,1500)->(0,345,1100) 44, arch 84 wide 126 high, sill (0,260,1190). g3 street (4,66,-150)->(0,150,-500) 50, ghats (150,62,-40)->(-200,56,-110) 48, fill=.7. g4 rise (0,820,700)->(0,330,-560) 48 then (0,1500,900)->(0,190,-620) 46, fill .36 to .10.
Lanka fire: `P, S, Q = LK.fires(fire, at, cam, n=, per=, rise=, near=)` then `FX.particles(st, P, S, (.95,.86,.80), 'tongue', seed=Q)`; raise `near` (default 90) for a racing camera. `LK.path(n)` gives roof landing points, `LK.ground(x, z)` heights, `AY.ground(x, z)` heights in Ayodhya.
