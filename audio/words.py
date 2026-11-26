"""The song: what is sung, where, and the English subtitles."""
from core import fr, sec

# (shot, frame from, shot, frame to, sung, English)
LINES = [
    ('a3', 10, 'a4', 2, 'ek lau jalī', 'One flame was lit.'),
    ('a5', 16, 'b1', 0, 'ek lau milī', 'One flame met another.'),
    ('b3', 0, 'b3', 105, 'van chalī, van chalī, sang chalī', 'To the forest it went, to the forest. Together it went.'),
    ('c7', 10, 'c7', 70, 'lau bujhī', 'The flame went out.'),
    ('d1', 46, 'd2', 0, 'lau jāgī', 'The flame woke.'),
    ('d2', 6, 'd4', 108, 'Rāma, Rāma, Rāma', 'Rama, Rama, Rama.'),
    ('d6', 4, 'd6', 80, 'siyā, lau', 'Sita, the flame.'),
    ('d8', 0, 'd8', 126, 'jalī! jalī! lau jalī!', 'Alight! Alight! The flame is alight!'),
    ('e1', 4, 'e2', 94, 'Rām nām, Rām nām', "Rama's name, Rama's name."),
    ('f5', 4, 'f5', 116, 'lau chalī, lau chalī', 'The flame set out, the flame set out.'),
    ('f8', 48, 'f8', 95, 'lau', 'Flame.'),
    ('g2', 0, 'g3', 106, 'ghar ghar lau, man man lau', 'In every house a flame, in every heart a flame.'),
    ('g4', 0, 'g4', 118, 'ek lau chalī, ghar āī', 'One flame set out, and is home.'),
    ('g5', 16, 'g5', 78, 'ek lau', 'One flame.'),
]


def stamp(t): return f'{int(t // 3600):02d}:{int(t // 60) % 60:02d}:{int(t) % 60:02d},{int(round((t % 1) * 1000)) % 1000:03d}'


def srt(path):
    out = []
    for i, (s0, f0, s1, f1, hi, en) in enumerate(LINES, 1):
        out.append(f'{i}\n{stamp(sec(fr(s0, f0)))} --> {stamp(sec(fr(s1, f1)))}\n{en}\n')
    path.write_text('\n'.join(out))
