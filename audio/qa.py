"""Measurements and pictures of sound. Nothing here makes sound."""
import numpy as np, cv2, pathlib
from scipy import signal
from core import SR, FR, sec, lu, kpower, integrated, ROOT
OUT = ROOT / 'qa' / 'audio'


def spectro(x, path, t0=0., fmax=20000, w=1600, h=620, marks=(), floor=-95, log=True, win=2048):
    """Spectrogram picture (log frequency), with optional vertical marks [(second, label)]."""
    x = x.mean(1) if x.ndim == 2 else x
    hop = max(64, len(x) // w)
    f, t, S = signal.stft(x, SR, nperseg=win, noverlap=win - min(hop, win // 2), boundary=None, padded=False)
    D = 20 * np.log10(abs(S) + 1e-9)
    yy = np.geomspace(40, fmax, h)[::-1] if log else np.linspace(0, fmax, h)[::-1]
    D = D[np.clip(np.round(yy / f[1]).astype(int), 0, len(f) - 1)]
    D = cv2.resize(D, (w, h), interpolation=cv2.INTER_AREA)
    img = cv2.applyColorMap((np.clip((D - floor) / (-15 - floor), 0, 1) * 255).astype(np.uint8), cv2.COLORMAP_INFERNO)
    for g in (100, 200, 500, 1000, 2000, 5000, 10000):
        if g < fmax:
            k = int(np.argmin(abs(yy - g))); img[k, ::6] = (120, 120, 120); cv2.putText(img, str(g), (2, k - 2), 0, .4, (200, 200, 200), 1)
    for s, lab in marks:
        c = int((s - t0) / (len(x) / SR) * w)
        if 0 <= c < w: img[:, c] = img[:, c] // 2 + 60; cv2.putText(img, lab, (c + 2, 12), 0, .4, (120, 255, 120), 1)
    pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(path), img)


def f0track(x, fmin=80, fmax=1200, win=.05, hop=.01):
    """Autocorrelation pitch track with parabolic refinement: (time, hz, clarity)."""
    n, h = int(win * SR), int(hop * SR)
    out = []
    w = np.hanning(n)
    m = 2 * n
    for i in range(0, len(x) - n, h):
        s = x[i:i + n] - x[i:i + n].mean()
        s = s * w
        R = np.fft.irfft(abs(np.fft.rfft(s, m)) ** 2, m)[:n]
        W = np.fft.irfft(abs(np.fft.rfft(w, m)) ** 2, m)[:n]
        r = R / (R[0] + 1e-12) / (W / W[0])
        a, b = int(SR / fmax), min(int(SR / fmin), n * 2 // 3)
        pk, _ = signal.find_peaks(r[a:b])
        if not len(pk): out.append((i / SR + win / 2, 0, 0)); continue
        mx = r[a:b][pk].max()
        k = pk[r[a:b][pk] > .92 * mx][0] + a
        y0, y1, y2 = r[k - 1:k + 2]
        d = .5 * (y0 - y2) / (y0 - 2 * y1 + y2 + 1e-12)
        out.append((i / SR + win / 2, SR / (k + d), mx))
    return np.array(out).T
