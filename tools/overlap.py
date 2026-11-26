"""python tools/overlap.py <other repo>  Originality check: code lines (40+ characters, whitespace removed) that also occur in another repository, and shared 14-token runs."""
import sys, os, re, glob
from pathlib import Path
ROOT = str(Path(__file__).resolve().parent.parent); other = sys.argv[1]


def files(r): return [p for e in ('py', 'mjs', 'js', 'glsl', 'frag', 'vert') for p in glob.glob(os.path.join(r, '**', '*.' + e), recursive=True) if '/.mm/' not in p and '/.git/' not in p and '/cache/' not in p]


def lines(r):
    out = {}
    for p in files(r):
        for i, l in enumerate(open(p, errors='ignore')):
            k = re.sub(r'\s+', '', l)
            if len(k) >= 40: out.setdefault(k, f'{os.path.relpath(p, r)}:{i + 1}')
    return out


def grams(r, n=14):
    out = {}
    for p in files(r):
        t = re.findall(r'[A-Za-z_]\w*|\d+\.?\d*|\S', open(p, errors='ignore').read())
        for i in range(len(t) - n): out.setdefault(' '.join(t[i:i + n]), os.path.relpath(p, r))
    return out


a, b = lines(ROOT), lines(other); s = [k for k in a if k in b]; print('lines here', len(a), 'there', len(b), 'shared', len(s))
for k in s[:40]: print('  ', a[k], '|', b[k], '|', k[:110])
g, h = grams(ROOT), grams(other); q = [k for k in g if k in h]; print('14-token runs here', len(g), 'shared', len(q))
by = {}
for k in q: by.setdefault((g[k], h[k]), []).append(k)
for (mine, theirs), runs in sorted(by.items(), key=lambda kv: -len(kv[1]))[:60]: print(f'  {len(runs):4d}  {mine} | {theirs} | {runs[len(runs) // 2][:130]}')
