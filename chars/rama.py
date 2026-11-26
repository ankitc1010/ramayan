"""Rama: the prince (look 0) and the exile (look 1)."""
from lau.stage import Fig
from lau.face import human, Face
BLUE = ('#4f7fb0', '#27406f', 1)
PAL = {1: BLUE, 2: ('#1d1826', '#0c0a14', 5), 3: ('#ffffff', '#805030', 2), 4: ('#b3122a', '#54081c', 3), 5: ('#0f7a58', '#063a34', 3), 6: ('#f5ead2', '#b79a8c', 1), 7: ('#eeb02f', '#a85a1c', 8), 8: ('#c42a2a', '#6a0f22', 1), 9: ('#6b3416', '#2e130a', 1), 10: ('#8e9aa8', '#3a4450', 7), 11: ('#fff0d8', '#d08a7a', 1), 12: ('#7a4a22', '#3a1e0c', 1)}


def face(F): return human(F, dict(skinsh='#1c2c58'))


PRINCE = Fig('rama', 'rama.glsl', PAL, face=face, u=dict(look=0))
BAREHEAD = PRINCE.variant(u=dict(nocrown=1.))          # the prince before the crown
EXILE = PRINCE.variant(pal={7: ('#d9772a', '#7e3516', 1), 8: ('#a8481c', '#5a2010', 1)}, u=dict(look=1))

# Lakshmana: the same exile's dress in white and red, wheat-gold skin
LAKSHMANA = PRINCE.variant(pal={1: ('#d9a066', '#86502f', 1), 2: ('#2a1a14', '#120a0a', 5), 7: ('#efe6d2', '#9a7f86', 1), 8: ('#b5303a', '#5c1220', 1)}, u=dict(look=1), face=lambda F: human(F, dict(skinsh='#6a3a20', nose='#5a2c18', lip='#a8483c', lip2='#c0604c', tilak='line', browt=1.15)))
LAKSHMANA_PRINCE = LAKSHMANA.variant(pal={7: ('#f2f0e4', '#9a8fa0', 8)}, u=dict(look=0))
