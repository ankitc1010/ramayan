"""Skies and lights the acts share.  Copy and change: st.paint('sky.frag', **SKY(DAWN, cov=.4))"""
from .stage import hexc, Light

_BASE = dict(cZen='#2c3f7a', cMid='#d9786a', cHor='#ffc776', cLow='#f2a860', sunDir=(-.35, .12, -1.), sunCol='#fff0b8', sunR=.06, sunGlow=1., rays=.6, halo=1., cov=.6, cy0=.06, cy1=.40, cseed=3., cscale=1.5, cdrift=.01, cLit='#ffe2a8', cCM='#e88f7a', cSh='#a0607e', cInk='#3a1a3a', cink=.8, starAmt=0., layers=3.)
DAWN = {}
DAY = dict(cZen='#2f6fb0', cMid='#7cc0d8', cHor='#e6f0d8', cLow='#cfe6d8', sunDir=(.5, .7, -.6), sunCol='#fff6d8', sunR=.045, rays=.25, cLit='#fffdf2', cCM='#d8e8ee', cSh='#8fb4cc', cInk='#3a5a7a')
SAFFRON = dict(cZen='#c8482a', cMid='#ee8a3a', cHor='#ffd27a', cLow='#e89a4a', cLit='#fff0c0', cCM='#f5a860', cSh='#b85a4a', cInk='#4a1a1a')
DUSK = dict(cZen='#1c1a4a', cMid='#8a2f4a', cHor='#f0703a', cLow='#a03a2a', cLit='#ff9a6a', cCM='#a84a5a', cSh='#4a2450', cInk='#1a0c24', rays=.35)
BLOOD = dict(cZen='#1a0818', cMid='#6a1020', cHor='#d8401c', cLow='#5a1018', cLit='#ff6a3a', cCM='#8a1c28', cSh='#3a0a1c', cInk='#0c0408', rays=.3, halo=0.)
NIGHT = dict(cZen='#070a24', cMid='#141c4a', cHor='#2c3a78', cLow='#10163a', sunCol='#dfe8ff', sunGlow=.5, rays=0., halo=.5, cLit='#8fa0d8', cCM='#46568f', cSh='#1f2858', cInk='#05081c', starAmt=1., cov=.35, sunR=.07)
RAIN = dict(cZen='#2a3444', cMid='#4a5868', cHor='#8494a0', cLow='#4a5664', sunGlow=.0, rays=0., halo=0., sunR=0., cov=.9, cLit='#8a9aa6', cCM='#5c6c7a', cSh='#36424f', cInk='#141c26', cink=.6)


def SKY(preset=None, **k):
    """all uniforms of sky.frag, colours resolved"""
    d = {**_BASE, **(preset or {}), **k}
    return {a: (hexc(v) if isinstance(v, str) else v) for a, v in d.items()}


L_DAWN = Light(key=(-.45, .45, .35), keyCol='#ffd9a8', amb='#8f8ac8', rim=(-.4, .3, -.9), rimCol=(1.5, 1.0, .5), bounceCol=(.25, .15, .10), envT='#ffd9b0', envM='#ffb070', envB='#6a4a7a')
L_DAY = Light(key=(.5, .8, .45), keyCol='#fff4dc', amb='#8fa6c8', rim=(-.6, .5, -.6), rimCol=(.5, .55, .6), envT='#ffffff', envM='#ffeccc', envB='#8a9a8a')
L_NIGHT = Light(key=(.4, .8, -.3), keyCol='#8fa4e8', amb='#3a4484', rim=(.5, .5, -.8), rimCol=(.55, .7, 1.2), envT='#8fa4ff', envM='#4a5ab0', envB='#20264f', bounceCol=(.02, .03, .08))
L_FIRE = Light(key=(-.3, -.15, .9), keyCol='#ff9a4a', amb='#4a2a4a', rim=(.7, .4, -.6), rimCol=(1.6, .7, .2), envT='#4a2a5a', envM='#ff8a3a', envB='#ffb04a', bounceCol=(.35, .12, .03))
