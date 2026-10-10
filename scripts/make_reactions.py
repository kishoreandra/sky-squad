"""Death reaction voices for Sky Squad, built with a voice model:
vocal cords (pulse train with shake and roughness) -> mouth shape (moving resonances between vowels)
-> lips, plus breath and consonant noises. Every keyframe is (time, sound, pitch Hz, loudness, breath)."""
import os, sys, wave
import numpy as np
from scipy.signal import lfilter, butter

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
SR = 44100
rng = np.random.default_rng(5)

V = {   # formant freqs (F1..F4) for a man's voice
    "aa": (730, 1090, 2440, 3400), "uh": (640, 1190, 2390, 3300), "oh": (570, 840, 2410, 3300),
    "oo": (320, 870, 2240, 3200), "eh": (530, 1840, 2480, 3500), "ee": (290, 2290, 3010, 3600),
    "nn": (260, 1700, 2600, 3300), "hh": (700, 1200, 2500, 3400), "ng": (280, 2200, 2800, 3400),
}
BW = (90, 110, 160, 220)
GAIN = (1.0, 0.55, 0.28, 0.12)

def smooth_noise(n, rate, seed):
    r = np.random.default_rng(seed)
    pts = r.standard_normal(int(n / SR * rate) + 3)
    return np.interp(np.arange(n) / SR * rate, np.arange(len(pts)), pts)

def interp_keys(keys, n, idx):
    times = np.array([k[0] for k in keys])
    vals = np.array([k[idx] for k in keys], float)
    return np.interp(np.arange(n) / SR, times, vals)

def voice(keys, sec, growl=0.0, jitter=0.012, scale=1.0, seed=0, scream=0.0):
    n = int(SR * sec)
    f0 = interp_keys(keys, n, 2)
    f0 = f0 * (1 + jitter * smooth_noise(n, 30, seed)) * (1 + 0.006 * np.sin(2 * np.pi * 5.2 * np.arange(n) / SR))
    amp = interp_keys(keys, n, 3)
    breath = interp_keys(keys, n, 4)
    ph = np.cumsum(f0) / SR
    p = ph % 1.0
    flow = np.where(p < 0.42, 0.5 * (1 - np.cos(np.pi * p / 0.42)), np.where(p < 0.58, np.cos(np.pi / 2 * (p - 0.42) / 0.16), 0.0))
    exc = np.diff(flow, prepend=0.0) * 40
    period = np.floor(ph).astype(int)
    exc *= 1 + growl * np.where(period % 2 == 0, 0.6, -0.6) * (0.5 + 0.5 * smooth_noise(n, 8, seed + 1))
    exc *= 1 + 0.12 * smooth_noise(n, 40, seed + 2)
    asp = rng.uniform(-1, 1, n) * (0.35 + 0.65 * (p < 0.5))
    src = exc * amp + asp * breath
    # mouth: time-varying resonances, block by block with carried filter state
    names = [k[1] for k in keys]
    times = np.array([k[0] for k in keys])
    F = np.zeros((n, 4))
    tt = np.arange(n) / SR
    for j in range(4):
        F[:, j] = np.interp(tt, times, [V[nm][j] * scale for nm in names])
    out = np.zeros(n)
    B = 256
    for j in range(4):
        zi = np.zeros(2)
        y = np.zeros(n)
        for i in range(0, n, B):
            f = F[min(i + B // 2, n - 1), j]
            bw = BW[j] * (1.4 if scream else 1.0)
            r = np.exp(-np.pi * bw / SR)
            a = [1.0, -2 * r * np.cos(2 * np.pi * f / SR), r * r]
            y[i:i + B], zi = lfilter([1 - r], a, src[i:i + B], zi=zi)
        out += y * GAIN[j]
    out = np.diff(out, prepend=0.0) * 8          # lips
    b, a = butter(2, 90 / (SR / 2), "high")
    out = lfilter(b, a, out)
    if scream:
        out = np.tanh(out / (np.max(np.abs(out)) + 1e-9) * (1 + 3 * scream))
    return out

def burst(sec, lo, hi, dec):
    b, a = butter(2, [lo / (SR / 2), hi / (SR / 2)], "band")
    tt = np.arange(int(SR * sec)) / SR
    return lfilter(b, a, rng.uniform(-1, 1, len(tt))) * np.exp(-tt / dec)

def thump(sec, f0, f1, dec):
    tt = np.arange(int(SR * sec)) / SR
    f = f1 + (f0 - f1) * np.exp(-tt * 25)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / dec)

def room(x, amt=0.18):
    out = x.copy()
    for d, g in ((0.019, 0.5), (0.029, 0.4), (0.043, 0.3), (0.061, 0.22), (0.089, 0.15)):
        i = int(SR * d); out[i:] += x[:-i] * g * amt * 2
    return out

def place(buf, x, at, g=1.0):
    i = int(SR * at); m = min(len(x), len(buf) - i)
    buf[i:i + m] += x[:m] * g

def norm(x): return x / (np.max(np.abs(x)) + 1e-9)

def write(name, x, gain=0.9):
    x = norm(x) * gain
    fade = int(SR * 0.01); x[-fade:] *= np.linspace(1, 0, fade)
    d = (np.clip(x, -1, 1) * 32767).astype(np.int16)
    with wave.open(os.path.join(OUT, name + ".wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(d.tobytes())

# 1 "AARGH!" - shot, angry pained yell, rough and falling
k = [(0, "hh", 150, 0.0, 0.4), (0.04, "aa", 175, 1.0, 0.15), (0.25, "aa", 205, 1.0, 0.12), (0.55, "aa", 160, 0.9, 0.15), (0.75, "uh", 115, 0.5, 0.2), (0.85, "uh", 95, 0.0, 0.1)]
write("01_aargh", room(voice(k, 0.88, growl=0.55, seed=1, scream=0.5)))

# 2 "UGH!" - short gut punch grunt, quick like Mini Militia
k = [(0, "uh", 140, 0.0, 0.3), (0.015, "uh", 150, 1.0, 0.1), (0.12, "uh", 120, 0.8, 0.15), (0.2, "uh", 100, 0.0, 0.25)]
b = np.zeros(int(SR * 0.32)); place(b, voice(k, 0.22, growl=0.6, seed=2, scream=0.2), 0.0); place(b, burst(0.03, 1500, 4000, 0.006), 0.19, 0.06)
write("02_ugh", room(b, 0.1))

# 3 "NOOO!" - desperate, rising then falling
k = [(0, "nn", 170, 0.5, 0.05), (0.09, "nn", 185, 0.6, 0.05), (0.15, "oh", 210, 1.0, 0.08), (0.45, "oh", 235, 1.0, 0.1), (0.85, "oo", 150, 0.7, 0.15), (1.05, "oo", 120, 0.0, 0.1)]
write("03_nooo", room(voice(k, 1.08, growl=0.25, seed=3, scream=0.35), 0.25))

# 4 "OOF!" - air knocked out of the chest, with breath
k = [(0, "oo", 160, 0.0, 0.5), (0.02, "oo", 165, 1.0, 0.25), (0.11, "uh", 130, 0.6, 0.3), (0.17, "hh", 110, 0.0, 0.6), (0.3, "hh", 100, 0.0, 0.0)]
b = voice(k, 0.32, growl=0.3, seed=4)
place(b, thump(0.2, 140, 60, 0.05), 0.0, 0.25 * np.max(np.abs(b)))
write("04_oof", room(b, 0.1))

# 5 "AAH!" - sharp, short cry, higher voice
k = [(0, "hh", 230, 0.0, 0.4), (0.02, "aa", 260, 1.0, 0.1), (0.18, "aa", 285, 1.0, 0.1), (0.38, "uh", 200, 0.4, 0.2), (0.45, "uh", 170, 0.0, 0.1)]
write("05_aah_short", room(voice(k, 0.47, growl=0.2, seed=5, scream=0.4)))

# 6 "AH! ...uhh" - hit, then slowly collapsing groan
b = np.zeros(int(SR * 1.3))
k1 = [(0, "hh", 190, 0.0, 0.4), (0.02, "aa", 215, 1.0, 0.1), (0.14, "aa", 190, 0.7, 0.15), (0.2, "aa", 170, 0.0, 0.2)]
k2 = [(0, "uh", 120, 0.0, 0.3), (0.08, "uh", 115, 0.7, 0.35), (0.5, "oh", 95, 0.5, 0.4), (0.8, "oh", 80, 0.0, 0.3)]
place(b, voice(k1, 0.22, growl=0.4, seed=6, scream=0.3), 0.0)
place(b, voice(k2, 0.82, growl=0.7, jitter=0.03, seed=7), 0.36, 0.7)
place(b, thump(0.3, 110, 45, 0.08), 1.0, 0.25)
write("06_ah_collapse", room(b, 0.2))

# 7 Gasp and choke - sharp breath in, then a strangled "khh-ahh"
b = np.zeros(int(SR * 0.9))
tt = np.arange(int(SR * 0.22)) / SR
gasp = burst(0.22, 900, 5000, 0.5) * np.sin(np.pi * tt / 0.22) ** 2
place(b, gasp, 0.0, 0.5)
place(b, burst(0.04, 1200, 3500, 0.01), 0.25, 0.6)
k = [(0, "aa", 160, 0.6, 0.4), (0.15, "aa", 140, 0.8, 0.4), (0.4, "uh", 100, 0.0, 0.3)]
place(b, voice(k, 0.45, growl=0.9, jitter=0.05, seed=8), 0.28, 1.0)
write("07_gasp_choke", room(b, 0.15))

# 8 Long falling scream - "AAAAaaah" dropping away
k = [(0, "hh", 260, 0.0, 0.4), (0.04, "aa", 300, 1.0, 0.1), (0.3, "aa", 320, 1.0, 0.1), (1.0, "aa", 210, 0.8, 0.12), (1.4, "uh", 150, 0.0, 0.1)]
x = voice(k, 1.45, growl=0.2, seed=9, scream=0.6)
x *= np.linspace(1, 0.35, len(x))   # moving away
write("08_falling_scream", room(x, 0.35))

# 9 Comic "WAH-wah-wooo" - cartoon fall-over voice
k = [(0, "oo", 220, 0.0, 0.05), (0.03, "aa", 230, 1.0, 0.05), (0.18, "uh", 200, 0.9, 0.05), (0.26, "aa", 210, 1.0, 0.05), (0.4, "uh", 180, 0.9, 0.05),
     (0.48, "oo", 190, 1.0, 0.05), (0.95, "oo", 110, 0.9, 0.05), (1.05, "oo", 100, 0.0, 0.05)]
x = voice(k, 1.08, growl=0.0, jitter=0.004, seed=10)
place(x, thump(0.25, 160, 60, 0.06), 0.96, 0.4 * np.max(np.abs(x)))
write("09_comic_wahwah", room(x, 0.2))

# 10 Bullet impact + "UGH" + body hits the floor
b = np.zeros(int(SR * 1.0))
place(b, burst(0.08, 300, 2500, 0.012) + thump(0.08, 260, 90, 0.02), 0.0, 0.5)
k = [(0, "uh", 150, 0.0, 0.3), (0.015, "uh", 165, 1.0, 0.12), (0.16, "oh", 120, 0.7, 0.2), (0.26, "oh", 100, 0.0, 0.2)]
place(b, voice(k, 0.28, growl=0.6, seed=11, scream=0.25), 0.04)
place(b, thump(0.3, 120, 45, 0.07) + burst(0.3, 100, 900, 0.03) * 0.5, 0.55, 0.6)
place(b, thump(0.2, 100, 45, 0.05), 0.68, 0.3)
write("10_hit_ugh_fall", room(b, 0.12))
print("reactions ok")
