"""python audio/make.py            render what changed, mix, write out/*.wav and dist/lau.en.srt
   python audio/make.py --all      ignore the cache
   python audio/make.py --qa       also measure (qa/audio)
   python audio/make.py A F        only re-render these acts, then mix"""
import sys, os, time, pathlib, hashlib, ast, importlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import core
from core import *
import multiprocessing as mp

HERE = pathlib.Path(__file__).resolve().parent
CACHE = HERE / 'cache'
LIBS = dict(voice=('core', 'voice'), melodic=('core', 'voice', 'inst'), drums=('core', 'inst', 'perc'), pads=('core', 'voice', 'inst'), sfx=('core', 'sfx', 'perc', 'inst'))


def digest(act, stem):
    import cues
    h = hashlib.sha1()
    for m in LIBS[stem]: h.update((HERE / f'{m}.py').read_bytes())
    if stem == 'sfx': h.update(repr(cues.act_cues(act)).encode())
    else:
        tree = ast.parse((HERE / f'act_{act.lower()}.py').read_text())
        for n in tree.body:
            if isinstance(n, ast.FunctionDef) and n.name in LIBS and n.name != stem: continue
            h.update(ast.dump(n).encode())
        for a, s, k in (('F', 'f7', 'hit'), ('B', 'b2', 'puff')):              # where the music follows the shots
            if a == act: h.update(repr(cues.frames(s, k)).encode())
    h.update(repr((ACT0[act], ACT1[act], TOTAL)).encode())
    return h.hexdigest()[:16]


def render(job):
    act, stem, path = job
    t = time.time()
    if stem == 'sfx':
        import cues
        x, info = cues.stem(act)
        s0 = ACT0[act] * FR
    else:
        mod = importlib.import_module(f'act_{act.lower()}')
        P = Part(ACT0[act], ACT1[act], pre=24)
        getattr(mod, stem)(P)
        x, info = P.finish()
        s0 = P.s0
    for old in CACHE.glob(f'{act}_{stem}_*.npz'): old.unlink()
    np.savez(path, x=x, s0=s0)
    return act, stem, round(time.time() - t, 1), info


def warm():
    import voice, inst, perc, sfx, mix
    voice.warm(); inst.flute_cal(); inst.bow_cal('violin'); inst.bow_cal('cello'); inst.pluck(200, .1); inst.conch(dur=.3)
    inst.brass_note([(0, .2, 200, '', 1)]); perc.war(); sfx.whoosh(2000, rng(1)); modal(np.ones(1) * 100, np.ones(1), np.ones(1), np.zeros(1), 10, np.ones(10)); modal(np.ones(1) * 100, np.ones(1), np.ones(1), np.zeros(1), 10, np.ones(1))
    mix.smooth_ar(np.ones(4), 1., 1.); mix._release(np.ones(4), .1)
    for k in ROOMS: room_ir(k)


def main(argv):
    t0 = time.time()
    CACHE.mkdir(exist_ok=True)
    acts = [a for a in argv if a in ACT0] or list(ACT0)
    warm()
    jobs, have = [], {}
    for stem in ('voice', 'pads', 'melodic', 'sfx', 'drums'):
        for act in ACT0:
            if stem != 'sfx' and not (HERE / f'act_{act.lower()}.py').exists(): continue
            p = CACHE / f'{act}_{stem}_{digest(act, stem)}.npz'
            have[act, stem] = p
            if not p.exists() or ('--all' in argv and act in acts): jobs.append((act, stem, str(p)))
    if jobs:
        with mp.get_context('fork').Pool(min(12, len(jobs)), maxtasksperchild=4) as pool:
            for act, stem, dt, info in pool.imap_unordered(render, jobs, chunksize=1): print(f'{act} {stem:8s} {dt:6.1f}s  {info}', flush=True)
    print(f'rendered {len(jobs)} parts in {time.time() - t0:.0f}s', flush=True)
    import mix, words
    stems = {s: np.zeros((TOTAL, 2)) for s in mix.STEMS}
    for (act, stem), p in have.items():
        d = np.load(p); x, s0 = d['x'], int(d['s0'])
        n = min(len(x), TOTAL - s0); stems[stem][s0:s0 + n] += x[:n]
    st, out, rep = mix.master(stems)
    (ROOT / 'out').mkdir(exist_ok=True); (ROOT / 'dist').mkdir(exist_ok=True)
    write_wav(ROOT / 'out' / 'soundtrack.wav', out)
    for s in mix.STEMS: write_wav(ROOT / 'out' / f'stem_{s}.wav', st[s])
    words.srt(ROOT / 'dist' / 'lau.en.srt')
    for f, t, m, g in rep['riding']:
        if abs(g) > 9: print(f'   riding: film frame {f:.0f} wanted {t}, was {m}, gain {g}')
    print(f'mix: {integrated(out):.2f} LUFS, master gain {rep["gain"]:.1f} dB, deepest limiting {rep["limit"]:.1f} dB, {time.time() - t0:.0f}s in all')
    if '--qa' in argv:
        import check; check.run(out, st)


if __name__ == '__main__': main(sys.argv[1:])
