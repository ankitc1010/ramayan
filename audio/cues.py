"""What is heard, shot by shot.  DEFAULT is the storyboard.  If shots/<id>.py carries EVENTS = [(frame, text, {params})],
each event is matched to an effect (params['sfx'], else the words of the text; see sfx.find) and replaces the default
one-shots of that effect in that shot; defaults of other effects stay.  params: db (level trim), pan, n (length in frames),
room ({name: amount}), mute=True (drop the effect from this shot), and anything the effect itself reads."""
import ast, importlib
from core import ROOT, Part, rng, sec, fr, db, momentary_max, pan as panned, ACT0, ACT1, ns
import numpy as np
import film

def E(frame, name, /, **p): return frame, name, p

DUEL = [12, 24, 36, 42, 48, 54, 60, 64, 68, 72, 75, 78, 81, 84, 87, 90, 92, 94]

DEFAULT = dict(
    a1=[E(3, 'breath'), E(24, 'spark'), E(36, 'flame_up', size=.35), E(38, 'lamp', n=60)],
    a2=[E(0, 'lamp', n=108, db=2), E(0, 'flame_up', size=.8, db=-4)] + [E(f, 'clack', f=q, pan=x, db=d) for f, q, x, d in ((3, 700, .3, 0), (9, 620, .25, -4), (18, 760, .35, -3), (36, 820, -.5, 0), (40, 880, -.25, -1), (44, 940, 0, -1), (48, 1010, .25, 0), (60, 820, -.4, -3), (72, 700, -.5, 0), (92, 900, .5, -3), (99, 760, .4, -4))]
       + [E(72, 'creak', dur=.72, f=640, db=-6, r0=18, r1=60), E(90, 'loose', f=240, db=-5, size=.5), E(26, 'cloth'), E(100, 'cloth')],
    a3=[E(22, 'whoom', dur=.9), E(24, 'river', n=50, db=3), E(26, 'birds', n=46, k=6, db=5), E(30, 'boat', n=40), E(40, 'ring', f=1568, db=-7)],
    a4=[E(0, 'crowd', n=80, voices=30, b=.15), E(0, 'giant_grow', dur=1.25, db=-5), E(30, 'ring', f=1318, db=-8), E(54, 'creak', dur=1.22, f=210, r0=12, r1=95, db=4), E(84, 'bow_break'), E(88, 'petals', dur=1.2, db=-2)],
    a5=[E(0, 'fire', n=72, size=.7, db=-7), E(0, 'birds', n=70, k=2, db=-6), E(60, 'cloth', db=2), E(62, 'petals', dur=1.)],
    b1=[E(0, 'crowd', n=36, voices=40, excite=.4, b=.03, db=4), E(42, 'whoosh', dur=.5, db=-10, lo=120, hi=700), E(54, 'whoosh', dur=.5, db=-9, lo=120, hi=700), E(60, 'ring', f=932, db=-9)],
    b2=[E(12, 'crown')] + [E(f, 'foot', pan=.1 * (-1) ** k, db=1) for k, f in enumerate((20, 28, 36, 44, 52))] + [E(26, 'gate', db=-6)] + [E(f, 'puff', pan=x) for f, x in zip((36, 42, 48, 54, 60, 66), (-.6, .6, -.4, .4, -.2, .1))],
    b3=[E(0, 'birds', n=27, k=7, a=.1, db=7), E(0, 'river', n=40, db=4), E(27, 'rain', n=28, dens=1.4, a=.03, b=.25, db=6), E(29, 'thunder', near=.2, db=-7), E(54, 'leaves', n=28, db=7), E(80, 'wind', n=30, lo=350, hi=1500, whistle=.25, db=3)]
       + [E(f, 'whoosh', dur=.4, peak=.5, db=-5, pan0=.9, pan1=-.9) for f in (27, 54, 81)] + [E(f, 'foot', on=o, db=0) for f, o in [(3 + 6 * k, ('stone', 'wet', 'leaves', 'leaves')[min(3, (3 + 6 * k) // 27)]) for k in range(17)]],
    b4=[E(0, 'crickets', n=40, db=6), E(0, 'fire', n=40, size=.6, db=-2)],
    c1=[E(0, 'birds', n=40, k=4, db=-3), E(0, 'gold', n=34, db=-5)] + [E(f, 'ring', f=q, db=-8) for f, q in ((4, 2093), (14, 2349), (24, 2637))] + [E(36, 'gold', dur=1.3, db=2), E(36, 'whoosh', dur=.6, db=-2), E(44, 'gold', dur=.6)],
    c2=[E(0, 'steps', n=20, every=3, on='leaves', db=1), E(4, 'creak', dur=.8, f=380, db=-4), E(24, 'loose'), E(30, 'hit', db=0), E(32, 'fire', n=28, size=1.6, db=2), E(32, 'leaves', n=24, db=2)],
    c3=[E(0, 'write', dur=.75, db=8), E(18, 'flame_up', size=1.2, db=2), E(18, 'fire_run', dur=1.), E(20, 'fire', n=28, size=1.2)] + [E(f, 'foot', on='leaves', db=1) for f in (36, 42, 47)],
    c4=[E(0, 'fire', n=92, size=1.4, db=1, b=.1), E(36, 'giant_grow', dur=2.2, db=0), E(90, 'puff', db=6)],
    c5=[E(f, 'steel', f=q, db=-7) for f, q in zip(range(0, 20, 2), range(420, 820, 40))] + [E(24, 'earth_tear', dur=1.4), E(30, 'rumble', n=40, db=3), E(30, 'wind_rush', n=34)],
    c6=[E(0, 'wind_rush', n=80, db=-1), E(22, 'whoosh', dur=1.2, peak=.8, lo=90, hi=1600, db=5), E(24, 'wings', dur=1.5, every=9), E(32, 'steel'), E(42, 'steel', f=900), E(51, 'steel', f=640), E(60, 'steel', f=1180, db=6), E(60, 'hit', db=-2), E(62, 'feathers', n=34, db=2), E(72, 'ring', f=2637, db=2), E(78, 'ring', f=2637, db=-5), E(84, 'ring', f=2637, db=-9)],
    c7=[E(0, 'rain', n=74, dens=.9, a=.6, b=1.4, db=4), E(6, 'ash_hiss', n=62, db=2), E(10, 'drop', db=-6, f=820), E(41, 'drop', db=-5, f=900)],
    d1=[E(0, 'rain', n=84, dens=.55, a=1., b=1., db=-5), E(6, 'drop', f=760, db=2), E(24, 'ring_skin', db=0), E(42, 'spark', db=1), E(42, 'gold', dur=.8, db=-6), E(48, 'heartbeat', n=36, every=12)],
    d2=[E(0, 'giant_grow', dur=3.2, db=2), E(0, 'waves', n=40, db=-3), E(20, 'wind_rush', n=64, db=-3), E(50, 'crowd', n=34, pitch=1.5, excite=.6, db=0), E(66, 'whoosh', dur=.8, db=-2)],
    d3=[E(0, 'rumble', n=42, f=80, db=2, a=1.), E(8, 'crack', db=-5), E(18, 'crack', db=-3), E(27, 'crack', db=-1), E(34, 'crack', db=0), E(42, 'leap_blast'), E(46, 'wind_rush', n=40, db=2)],
    d4=[E(0, 'wind_rush', n=126), E(14, 'splash', db=-5), E(22, 'splash', db=-3), E(30, 'splash', db=-6), E(42, 'whoosh', dur=.8, db=2), E(64, 'splash', size=3, db=3), E(66, 'roar', dur=1.4), E(84, 'whoosh', dur=.4, db=3), E(91, 'whoosh', dur=.4, db=2, pan0=.8, pan1=-.8), E(96, 'splash', db=-2), E(108, 'gold', dur=.8)],
    d5=[E(0, 'night_city', n=84), E(0, 'waves', n=84, period=4., db=-6), E(48, 'foot', db=5), E(48, 'hit', db=-13, size=.6), E(56, 'cloth', db=2)],
    d6=[E(0, 'crickets', n=84, db=2), E(0, 'wind', n=84, lo=150, hi=420, db=-3), E(26, 'leaves', n=12, db=-3), E(36, 'ring_skin', db=1), E(38, 'gold', dur=1.2, db=-4)],
    d7=[E(0, 'crowd', n=70, voices=24, pitch=.75, db=0), E(30, 'flame_up', size=1.6, db=4), E(32, 'fire_run', dur=1.1, db=-1), E(34, 'fire', n=56, size=2., db=2), E(66, 'rope', db=3), E(66, 'hit', db=-4), E(68, 'whoosh', dur=.7, db=2)],
    d8=[E(0, 'fire', n=130, size=5., db=6, a=.1, b=1.), E(0, 'wind_rush', n=124, db=-2)] + [E(f, 'hit', db=-5) for f in (10, 31, 52, 73, 94)] + [E(f, 'flame_up', size=3, db=3) for f in (12, 33, 54, 75, 96)] + [E(f, 'whoosh', dur=.8, db=2) for f in (22, 43, 64, 85)] + [E(60, 'crack', size=2), E(106, 'crack', size=3, db=2), E(126, 'far_fire', n=54), E(128, 'waves', n=44, period=3.4, db=-5)],
    e1=[E(0, 'waves', n=44, db=-1, b=.2), E(2, 'write', dur=1.4, db=4), E(40, 'whoosh', dur=.5, db=-5), E(42, 'splash', size=1.6, db=1), E(43, 'underwater', n=39), E(60, 'gold', dur=.8, db=-3), E(84, 'splash', size=1.3, db=2), E(82, 'waves', n=16)],
    e2=[E(0, 'waves', n=96), E(0, 'march', n=96, db=-1), E(0, 'crowd', n=96, pitch=1.25, db=-3)] + [E(f, 'stone_drop', pan=x, db=d) for f, x, d in [(6 * k, (-.7, .5, -.2, .8, -.5, .2, .7, -.8)[k % 8], (1, -4, -2, -4)[k % 4]) for k in range(16)]] + [E(58, 'squirrel'), E(64, 'stone_drop', f=900, big=0, db=-8)],
    f1=[E(0, 'rumble', n=96, f=70, db=-2), E(0, 'fire', n=96, size=3., db=-1), E(2, 'gate', db=-3), E(72, 'flame_up', size=4, db=2)] + [E(f, 'eye_open', pan=.12 * (k - 4.5)) for k, f in enumerate(range(12, 67, 6))],
    f2=[E(0, 'march', n=38, every=3, db=6), E(0, 'crowd', n=96, voices=40, excite=.8, db=6), E(36, 'clash'), E(40, 'arrow_storm', n=56), E(0, 'arrow_storm', n=36, db=-4)] + [E(f, 'steel', db=-2, pan=x) for f, x in ((44, -.6), (51, .5), (57, -.2), (66, .7), (72, -.7), (81, .3), (87, -.4))] + [E(60, 'hit', db=-5), E(78, 'hit', db=-5)],
    f3=[E(0, 'rumble', n=80, db=1), E(12, 'eye_open', db=3), E(14, 'roar', f=44, dur=1.7, db=-2), E(30, 'footfall', db=-2), E(48, 'footfall', db=0), E(20, 'giant_grow', dur=2, db=2), E(62, 'roar', f=52, dur=.7, db=-4), E(66, 'loose', db=3), E(66, 'arrow_fly', dur=.5, db=4), E(72, 'hit', db=-3), E(78, 'giant_fall')],
    f4=[E(0, 'wind', n=34, db=2), E(0, 'thunder', db=-7, near=.1), E(16, 'thunder', db=-5, near=.2), E(30, 'lightning'), E(48, 'heartbeat', n=48, every=18, db=3), E(62, 'lamp', n=34, db=-1)],
    f5=[E(0, 'mountain_wind', n=120, db=1), E(0, 'rumble', n=120, f=70, db=-3), E(0, 'gold', n=60, db=-8), E(84, 'birds', n=40, k=5)],
    f6=[E(12, 'drop', f=980, db=3), E(24, 'gold', dur=1., db=-8), E(22, 'birds', n=26, k=4, db=-2)],
    f7=[E(0, 'chariot', n=94, db=2), E(0, 'wind_rush', n=94, db=-3), E(0, 'fire', n=94, size=3, db=1)] + [E(f, 'hit', db=-1) for f in DUEL] + [E(max(0, f - 3), 'loose', db=-5, pan=.5 * (-1) ** k) for k, f in enumerate(DUEL[:9])],
    f8=[E(f, 'fire_run', dur=.8, db=d) for f, d in ((4, -8), (18, -7), (32, -5), (46, -4), (60, -3), (74, -1))] + [E(36, 'creak', dur=2.4, f=240, r0=10, r1=60, db=2), E(98, 'creak', dur=.85, f=300, r0=9, r1=26, db=-5)],
    f9=[E(0, 'loose', db=8, size=2), E(0, 'tunnel', n=72), E(72, 'giant_fall', db=1), E(72, 'lightning', db=-3)] + [E(f, 'whoosh', dur=.45, db=2, pan0=x, pan1=-x) for f, x in ((10, .8), (20, -.8), (30, .8), (38, -.8), (46, .8), (53, -.8), (60, .8), (66, -.8))],
    f10=[E(f, 'puff', db=-4, pan=.1 * (k - 4.5)) for k, f in enumerate(range(12, 61, 6))] + [E(78, 'puff', db=-1), E(0, 'ash_hiss', n=96, db=-6)],
    g1=[E(0, 'lamp', n=72, db=5), E(24, 'ring', f=2093, db=-4), E(24, 'cloth', db=-3)],
    g2=[E(0, 'wind', n=96, lo=220, hi=700, db=-3), E(0, 'lamps', n=96, rate=9, curve=.55, db=4), E(0, 'ring', f=1760, db=-9), E(48, 'ring', f=1975, db=-10)],
    g3=[E(0, 'lamp', n=40), E(12, 'cloth'), E(30, 'crowd', n=78, voices=44, excite=.35, pitch=1.1, db=4), E(40, 'lamps', n=60, db=2), E(56, 'petals', dur=2., db=3)] + [E(f, 'ring', f=1568, db=-7) for f in (48, 60, 72, 84, 96)],
    g4=[E(0, 'river', n=120), E(0, 'lamps', n=110, rate=22, curve=.8, db=5), E(0, 'crowd', n=100, voices=30, db=-5), E(84, 'gold', dur=1.2, db=1)],
    g5=[E(0, 'lamp', n=84, db=3, b=.06), E(36, 'spark', db=-6), E(42, 'flame_up', size=.25, db=-4), E(10, 'cloth', db=-3), E(84, 'breath_out'), E(90, 'embers', n=40)],
)


# what the shots call things, where the words alone would mislead; None = carried by the music, or by a storyboard default
ALIAS = {'theatre begins': 'flame_up', 'ghee on the fire': 'flame_up', 'spark falls': None, 'stone rises': None, 'last stroke': None, 'white': None, 'silence': None, 'title done': None,
         'wick to wick': 'spark', 'flame comes near': None, 'last light bows': None, ('g5', 'breath'): None, ('f8', 'eye'): None, 'point burns': 'fire', 'eyes meet': None, 'eyes open': None, 'eye opens': None, ('f1', 'eyes open'): 'eye_open', ('f3', 'eye opens'): 'eye_open',
         'everything stops': None, 'coronation drums': None, 'conch': None, 'first boon': None, 'second boon': None, 'crown goes up': None, 'crown metal': 'ring', 'the word reads': None, 'camera rises': None,
         'ring on palm': 'ring_skin', 'fist closes': 'cloth', 'hand withdraws': 'cloth', 'tear': None, 'two breaths': 'breath', 'fire bursts up': 'flame_up', 'a head slides out of the shadow': None, 'twenty arms open': 'whoosh', 'she looks up': None, 'flames shiver': None, 'bowl falls': 'crown',
         ('g2', 'flower chariot overhead'): 'wind', ('g2', 'bells on the chariot'): 'temple_bell', 'bow lifted': None, 'hand on bow': None, 'string hum': None, 'eyes lift': None, 'look down': None, 'ten mouths laugh': None, 'arms and weapons unfold': 'steel', 'through the cloth': 'cloth'}
# the same, shot by shot: a name, or (name, params) where the effect needs a colour or a level of its own
BY_SHOT = dict(
    b4={'quiet words': None, 'she laughs softly': ('breath', dict(db=-3))},
    c1={'jewels chime': ('ring', dict(f=2349, db=-8)), 'it looks at us': None, 'hooves gather': ('hoof', dict(k=4)), 'leap': ('whoosh', dict(n=14, db=-2)), 'she sees it': None},
    c2={'deer bounds': ('hoof', dict(k=2)), 'arrow drawn from quiver': 'cloth', 'arrow flight': ('arrow_fly', dict(n=8, db=-4)), 'the stolen cry': None, 'wood darkens': ('wind', dict(n=14, db=-2))},
    c3={'he looks at her': None, 'far cry': None},
    c4={'ten pairs of eyes kindle': ('eye_open', dict(db=-2)), 'bare foot on earth': ('foot', dict(on='leaves'))},
    c5={'first accent': ('whoom', dict(n=8, db=-3)), 'second accent, arms': ('whoom', dict(n=8, db=-2)), 'third accent, ten heads': ('whoom', dict(n=8, db=0)), 'he breathes': None, 'the earth cracks': ('crack', dict(size=2, db=1)),
        'stones and roots tear': ('crack', dict(size=3, db=-1)), 'the ground comes loose': 'rumble', 'flying chariot passes over': ('whoosh', dict(n=20, lo=80, hi=900, db=1)), 'the sky swallows them': ('whoosh', dict(n=12, db=-4))},
    c6={'far cry of an old bird': ('bird_cry', {}), 'beak on the dome': ('steel', dict(f=900, db=1)), 'Ravana slides back': ('whoosh', dict(n=10, lo=90, hi=900)), 'the blade passes': ('steel', dict(f=1180, db=6)), 'wings open like sails': ('wings', dict(n=12)), 'wing beat': ('wings', dict(n=8)), 'wing buffet': ('wings', dict(n=8, db=3)), 'feathers': ('feathers', dict(n=28, db=-2)), 'ornaments let go': ('ring', dict(f=2637, db=5)),
        'small bells falling away': ('ring', dict(f=3136, db=-3)), 'five heads turn up': None, 'jewels on rock': ('ring', dict(f=2093, db=-5))},
    c7={'wet footstep': ('foot', dict(on='wet', db=1)), 'he stops': None, 'knee on wet earth': ('foot', dict(on='wet', db=3)), 'hand closes on earth': ('foot', dict(on='wet', db=-2))},
    d3={'giant crouches': 'rumble', 'mountain bursts': ('earth_tear', dict(db=-4)), 'whip': ('whoosh', dict(n=8, db=-2)), 'boulders': ('crack', dict(size=3)), 'passes overhead': ('whoosh', dict(n=16, lo=70, hi=1200, db=3)), 'tree falls away': ('leaves', dict(n=12, db=1))},
    d4={'joyful cry': None, 'hand cuts water': ('splash', dict(db=-5)), 'calm': None, 'water pours': ('splash', dict(size=3, db=2)), 'shrinks': None, 'jaws clap': ('hit', dict(size=2.5, db=-3)), 'glimmer': 'gold'},
    d5={'still sea at night': 'waves', 'look down': None},
    d6={'guards breathe': None, 'leaf falls': ('leaves', dict(n=8, db=-6)), 'ring falls': None, 'ring in palm': 'ring_skin', 'eyes see': None, 'looks up': None},
    d7={'ravana chuckles': None, 'silence falls': None, 'small smile': None, 'leap over the lens': ('whoosh', dict(n=16, db=2)), 'guards thrown back': ('hit', dict(db=-6)), 'window breaks': 'shatter'},
    d8={'lattice bursts': 'shatter', 'tail fire': ('fire', dict(n=130)), 'fire stroke': 'fire_run', 'wall of fire': ('flame_up', dict(size=5, db=5)), 'land on roof': 'hit', 'leap': 'whoosh', 'great leap': ('whoosh', dict(n=20, lo=90, hi=2000, db=4)), 'under the bridge': 'whoosh', 'camera up': 'whoosh', 'land on terrace': 'hit', 'towers catch': 'flame_up', 'land on palace': 'hit', 'land on tower': 'hit',
        'land on the top': ('hit', dict(size=2, db=-3)), 'spring': 'whoosh', 'city goes up': ('flame_up', dict(size=5, db=5)), 'hang': None, 'hiss in the sea': ('splash', dict(db=-5))},
    e2={'work song': 'crowd', 'names run to Lanka': ('gold', dict(n=14)), 'bridge complete': None},
    f1={'host roars out': ('crowd', dict(n=18, pitch=.75, excite=1., voices=44, a=.1, db=8))},
    f2={'two hosts run': 'march', 'war drums': None, 'dust wall': ('whoom', dict(n=14, db=-1)), 'mace breaks shield': ('steel', dict(f=520, db=1)), 'tree sweeps two away': 'hit', 'club on helm': ('steel', dict(f=760, db=0)), 'rock bursts': 'hit', 'camera whip': ('whoosh', dict(n=8, db=-3)), 'arrows meet': ('ring', dict(f=2794, db=-9))},
    f3={'eye widens': ('eye_open', dict(db=-3)), 'giant hand sweeps': ('whoosh', dict(n=12, lo=60, hi=700, db=3)), 'sun goes out': ('whoom', dict(n=12, db=-2)), 'giant falls': ('whoosh', dict(n=10, lo=60, hi=500, db=2)), 'giant hits the ground': 'giant_fall', 'ground wave': ('earth_tear', dict(db=-6)), 'dust swallows': ('wind', dict(n=12, db=2))},
    f4={'bow drops, muffled': ('clack', dict(f=240, db=-4)), 'second bow drops, muffled': ('clack', dict(f=210, db=-4)), 'he is caught': 'cloth', 'hiss falling': ('arrow_fly', dict(n=6, db=-2))},
    f5={'waterfalls in the air': ('river', dict(n=60, db=4)), 'conch far off': None, 'herbs blaze': ('gold', dict(n=8))},
    f6={'drop swells': None, 'eyes open, breath': 'breath', 'hand closes on hand': 'cloth', 'sunrise swell': None},
    f7={'two chariots gallop': ('chariot', dict(n=94)), 'chariots pass': ('whoosh', dict(n=12, lo=90, hi=1400, db=1)), 'hoof': ('hoof', dict(k=4, db=2)), 'wheel': None, 'glare': ('eye_open', dict(db=-3)), 'head grows again': ('flame_up', dict(n=6, size=.6, db=-5))},
    g3={'quiet hall': None, 'head lifts': 'cloth'},
)
ALIAS.update({(shot, text): a for shot, names in BY_SHOT.items() for text, a in names.items()})
ALIAS.update(hoof='hoof')
LOUD = -20          # an effect this loud or louder, where the storyboard does not have it, is held to -26 unless the event names it (sfx=...)


def read_events(shot):
    """EVENTS of shots/<shot>.py: parsed as a literal when possible, else by importing the module. Never raises."""
    path = ROOT / 'shots' / f'{shot}.py'
    if not path.exists(): return []
    ev = None
    try:
        for node in ast.walk(ast.parse(path.read_text())):
            if isinstance(node, ast.Assign) and any(getattr(t, 'id', '') == 'EVENTS' for t in node.targets): ev = ast.literal_eval(node.value)
    except Exception: ev = None
    if ev is None and 'EVENTS' in path.read_text():
        try:
            m = importlib.import_module(f'shots.{shot}')
            ev = next((c.EVENTS for c in vars(m).values() if isinstance(c, type) and c.__dict__.get('EVENTS')), [])
        except Exception as x:
            print(f'cues: {shot}: EVENTS not readable ({x!r}), using the storyboard'); ev = []
    out = []
    for e in ev or []:
        try:
            p = dict(e[2]) if len(e) > 2 and e[2] else {}
            if 'dur' in p: p['n'] = p.pop('dur')          # the shots count in frames
            if p.pop('soft', 0): p['db'] = p.get('db', 0) - 3
            out.append((float(e[0]), str(e[1]), p))
        except Exception: print(f'cues: {shot}: skipped {e!r}')
    return out


def cues(shot):
    """Merged cue list of a shot: [(frame, effect, params)]."""
    import sfx
    base = [c for c in DEFAULT.get(shot, [])]
    new, drop = [], set()
    for f, text, p in read_events(shot):
        a = ALIAS.get((shot, text), ALIAS.get(text, ''))
        if a is None: continue
        a, give = a if isinstance(a, tuple) else (a, {})
        key = p.get('sfx') or a or sfx.find(text)
        if key not in sfx.REG:
            print(f'cues: {shot} f{f:g}: no effect for {text!r}'); continue
        known = any(b[1] == key for b in base)
        drop.add(key)
        if p.get('mute'): continue
        q = dict(min((b for b in base if b[1] == key), key=lambda b: abs(b[0] - f), default=(0, 0, {}))[2])
        if 'n' not in p and key == 'heartbeat': q['n'] = 4
        if not known: q['db'] = min(-4, -26 - sfx.REG[key]['level']) if 'sfx' not in p else 0
        q.update({k: v for k, v in p.items() if k != 'sfx'}); q.update(give); new.append((f, key, q))
    for i, (f, key, q) in enumerate(new):
        later = [g for g, k, _ in new if k == key and g > f]
        if 'n' in q: q['n'] = max(2, min([q['n'], film.LEN[shot] - f + 2] + [g - f for g in later]))
    return sorted([b for b in base if b[1] not in drop] + new, key=lambda c: (c[0], c[1]))


def frames(shot, key): return [f for f, k, p in cues(shot) if k == key]


def act_cues(act): return [(s, f, k, p) for s in film.START if ACT0[act] <= film.START[s] < ACT1[act] for f, k, p in cues(s)]


def stem(act):
    """Render all effects of one act."""
    import sfx
    P = Part(ACT0[act], ACT1[act])
    layers = {}
    for i, (s, f, k, p) in enumerate(act_cues(act)):
        e = sfx.REG[k]
        room = p.get('room', e['room'])
        x = e['fn'](p, rng(s, f, k, i))
        off = 0.
        if isinstance(x, tuple): x, off = x
        x = np.asarray(x, dtype=float)
        x = x * db(e['level'] + p.get('db', 0) - momentary_max(x))
        key = tuple(sorted(room.items()))
        if key not in layers: layers[key] = P.layer(str(key), sends=dict(key), low=28)
        if x.ndim == 1: x = panned(x, p.get('pan', 0.))
        elif p.get('pan'): x = x * np.array([min(1, 1 - p['pan']), min(1, 1 + p['pan'])])
        m = ns(.0015); x[-m:] *= np.linspace(1, 0, m)[:, None]
        layers[key].add(x, sec(fr(s, f)) - off)
    return P.finish()
