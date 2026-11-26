"""LAU (लौ) : the Ramayana as one flame.  The timeline and the storyboard.
24 fps.  The pulse is 6 frames (a quarter second) all through; the bar changes: acts A B C G = 6 pulses (36 f), act D = 7 pulses (42 f), acts E F = 8 pulses (48 f)."""
PULSE = 6
ACTS = dict(A=('दीप  the lamp', 36), B=('वन  the forest', 36), C=('माया  the golden deer', 36), D=('हनुमान  the carrier', 42), E=('सेतु  the bridge', 48), F=('युद्ध  the war', 48), G=('दीपावली  the row of lamps', 36))
# (id, frames, what happens, where the flame is)
BOARD = [
    ('a1', 72, 'Black. One breath. A spark falls on a wick (f24); the flame stands up (f36). Extreme close: brass lamp dish, oil, wick; first light crawls over the brass. Slow pull back.', 'lamp'),
    ('a2', 108, 'Shadow theatre seen from the audience: a glowing cloth, the flame a hot spot behind it. Perforated leather puppets on rods: King Dasharatha and the sacred fire (f0), four small princes rise (f36), the eldest draws a toy bow and shoots across the cloth (f72, release f90).', 'behind the cloth'),
    ('a3', 72, 'Push through the cloth into the flame (f0-24); its core becomes the rising sun (f24) and the painted world opens in full colour: Ayodhya at dawn on the Sarayu, domes, flags, ghats, boats, birds. Crane up.', 'becomes the sun'),
    ('a4', 108, "Mithila. Shiva's bow, huge, on its stand; rows of crowned kings. The prince lifts it with one hand (f0-30), close on the grip and the string (f30-54), draws to the ear (f54-84), and it BREAKS (f84): print-frame flash, shock ring, petals.", 'glint on the bow'),
    ('a5', 72, 'Sita raises the garland across the wedding fire; their eyes meet (f30); the garland comes down over the lens (f60-72).', 'the wedding fire'),
    ('b1', 72, 'Coronation. A crown descends toward Rama, gold and drums. f36: it stops. Colour drains. In the dark above, two kohl-rimmed eyes open (Kaikeyi); one finger rises (f42), then two (f54): two boons. The crown goes back up.', 'glint in her eyes'),
    ('b2', 72, 'The crown is set down on a stone floor (thunk f12). Bare feet turn and go. Low, wide: three silhouettes walk out through a vast gate into a red dusk, and behind them the hall lamps go out one by one (f36-66). Dark.', 'lamps go out'),
    ('b3', 108, 'Fourteen years in one tracking shot: Rama, Sita, Lakshmana walk in profile through painted forests; tree trunks wipe the seasons: spring f0, monsoon f27, autumn f54, winter f81. Deer, peacocks, a river.', 'sun through leaves'),
    ('b4', 36, 'Panchavati at night. A leaf hut, a small cooking fire, three faces lit by it, fireflies. Peace.', 'cooking fire'),
    ('c1', 60, 'A golden deer steps through shafts of light, looks at us, leaps (f36) in an arc of gold dust. Sita sees it: gold in her eyes (f42-60).', 'gold'),
    ('c2', 60, 'Rama runs and shoots (release f24). The deer is struck (f30): its gold skin bursts into leaf and the demon Maricha is under it, crying out in Rama\'s voice (f36-60).', 'gold leaf burns off'),
    ('c3', 48, "Lakshmana's arrow point scratches a line in the earth before the hut; on f18 the line takes fire and runs round; he goes (f36).", 'the line of fire'),
    ('c4', 96, 'A humble mendicant with a bowl stands at the burning line. The fire throws his shadow up the rock behind him, and the shadow tells the truth: it swells, grows ten heads (one per beat from f36) and twenty arms. Sita has not looked up. She does (f78). Her foot crosses; the line goes out (f90).', 'line of fire, goes out'),
    ('c5', 60, 'Ravana unfolds: ten heads fan open (f0-18). He takes the very ground she stands on: earth, hut and all rip loose (f24) and rise into a red sky behind his flying chariot.', 'red sky'),
    ('c6', 96, 'Out of the sun the old vulture Jatayu falls on him (f0-24), wings as wide as the frame; talons, sword; on f60 the blade takes a wing. Feathers. Sita lets an ornament fall (f72): a spark dropping away to the forest below.', 'falling jewel spark'),
    ('c7', 84, 'The hut place, empty. Rain. Cold ash, one thread of smoke from the dead fire. Rama on his knees, Lakshmana behind. Blue-grey, almost no colour. The smoke thread ends (f72). Silence.', 'out'),
    ('d1', 84, 'A rainy hill. Two palms: Rama\'s hand lays a ring in Hanuman\'s great hand (f24). Deep in the ruby a spark wakes (f42). Hanuman\'s lowered eyes open with the spark in them (f54-84).', 'spark in the ruby'),
    ('d2', 84, 'On the shore mountain he remembers what he is. He grows: camera climbs from his feet past the treetops, past clouds, to his face; tiny vanaras cheer far below.', 'ring on his hand'),
    ('d3', 84, 'The crouch (f0-30): rock cracks, trees bend inward. The LEAP (f42): the peak bursts, smear, shock rings, trees torn after him like arrows.', 'sun behind him'),
    ('d4', 126, 'Flight. Camera swings round him over a turquoise ocean; he skims spray, bursts through clouds (f42), a serpent mouth as big as a harbour rises (f66); he shrinks, darts in and out between the teeth (f84), and a golden glimmer shows on the far edge of the sea.', 'glimmer of Lanka'),
    ('d5', 84, 'Night. Lanka: a city of gold on a three-peaked rock, under an enormous moon. A small shape lands on a parapet (f48) and lifts its head.', 'gold city lights'),
    ('d6', 84, 'The ashoka grove. Sita under the red-flowering tree, cold moonlight, guards asleep. The ring drops from the leaves into her palm (f36); the spark lights her face warm, the first warm light since the rain.', 'the ring lights her face'),
    ('d7', 84, "Ravana's hall. Hanuman bound, tail wrapped in oiled cloth. A torch touches it (f30). Fire runs up the tail; he opens one eye, smiles (f48); ropes burst (f66).", 'on his tail'),
    ('d8', 168, 'Lanka burning, one long take: he bounds roof to roof, the tail a brush writing fire across the city; camera flies beside, under, over; gold towers run like wax. Last 42 f: pull far back over black water; the burning island is a lamp, the city its flame.', 'the whole city'),
    ('e1', 96, 'A stone. A wet vermilion finger writes राम on it (f0-36). It is dropped (f42), sinks through green water, the name glows (f60), it stops, rises, breaks the surface, floats (f84).', 'the name glows'),
    ('e2', 96, 'The bridge builds itself under a flying camera: stones rain in on every pulse, each with the name; the army marches behind; a squirrel carries a pebble; ahead, Lanka on the horizon.', 'names glow'),
    ('f1', 96, 'Lanka\'s gate in darkness. Ravana\'s ten pairs of eyes open one by one, one on every half beat (f12, 18, 24 ... 66); fires behind; all ten mouths laugh (f72).', 'fire in ten pairs of eyes'),
    ('f2', 96, 'The two hosts run at each other and meet (f36). Vanaras with trees and rocks, rakshasas with steel; a storm of arrows crossing arrows; camera travels down the line of the collision.', 'burning arrows'),
    ('f3', 96, 'Kumbhakarna. An eye as big as a house opens (f12). He stands up out of the dust, vanaras hang on him like ants. One arrow from Rama, bright (f66). He falls like a mountain (f78 impact).', 'arrow of light'),
    ('f4', 96, 'Night. Indrajit hidden in cloud; a serpent of lightning (f30) strikes Lakshmana down. Sound goes. Rama catches him. All colour sinks; a lamp in Rama\'s camp gutters.', 'guttering'),
    ('f5', 120, 'Hanuman flies with a whole mountain on his palm, herbs glowing on it like lamps, across a huge moon, over rivers and sleeping India; dawn begins behind him.', 'glowing herbs'),
    ('f6', 48, 'A drop from a glowing leaf falls on Lakshmana\'s lips (f12). His eyes open (f24). Sunrise.', 'the drop, the sunrise'),
    ('f7', 96, 'The duel. Two chariots circle. Arrow, head falls, head grows again: f12, f24, f36, f42, f48 ... faster; ten heads wheel like a burning discus.', 'burning heads'),
    ('f8', 120, 'Rama kneels into the last draw. Every flame of the film streams in to the arrow point: lamp, wedding fire, line, ring, tail, city. Close on his eye with the flame in it (f72). String creaks. Silence (f96-120).', 'on the arrow point'),
    ('f9', 96, 'Release (f0). The arrow flies through everything the film has shown, a tunnel of painted memories; it strikes the navel (f72). White.', 'the arrow is the flame'),
    ('f10', 96, 'Dark. Ten small lights hang where ten heads were. They go out one by one (f12, 18 ... 66). The last one bows before it dies (f78). Gold leaf falls like ash. No cheering.', 'ten lights go out'),
    ('g1', 72, 'Sita and Rama, a lamp between them. He gives back the jewel (f24). Their eyes; two reflections of one flame.', 'one lamp between two faces'),
    ('g2', 96, 'The flower chariot Pushpaka carries them home over the night map of India: sea, bridge, rivers; below it lamps wake in village after village, a river of light following them.', 'villages'),
    ('g3', 108, 'Ayodhya. Bharata, with the sandals on the throne, lifts his eyes. An old mother raises a lamp. Streets of people; they arrive: Rama, Sita, Lakshmana, Hanuman walk through light.', 'every hand'),
    ('g4', 120, 'Camera rises from the ghats: lamps on the water, on steps, roofs, streets; higher; the lamps of the whole city together write राम (clear by f84). Hold.', 'ten thousand lamps'),
    ('g5', 168, 'The lamp of the beginning, the cloth behind it. An old hand guides a child\'s: a new small wick is lit at the flame (f30-48). The small flame comes to us, close. Breath (f84): out. Black. लौ is written in embers (f90-120), holds, and fades (f144-168).', 'passed on'),
]
from itertools import accumulate

LEN = {row[0]: row[1] for row in BOARD}
START = dict(zip(LEN, accumulate(LEN.values(), initial=0)))
SHOTS = [(name, START[name], LEN[name]) for name in LEN]
BRIEF = {row[0]: row[2] for row in BOARD}
N = sum(LEN.values())


def where(frame):
    """the shot on screen at a film frame, and the frame inside it"""
    name = max((s for s in START if START[s] <= frame), key=START.get)
    return name, frame - START[name]


if N != 3738:
    raise SystemExit(f'the soundtrack is cut to 3738 frames but the storyboard adds up to {N}')
