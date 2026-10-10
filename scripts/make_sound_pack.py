"""Sky Squad sound pack v2, made after measuring the reference clip:
- flying: wide, even hiss (no single pitch), swells in over ~0.2 s, holds while flying
- hand push / boost: short swish 0.15-0.3 s centred near 800-1000 Hz
- guns: sharp hits; automatic fire ~70-120 ms apart
- bombs: big burst with low thump and a ~0.9 s tail
All new sounds made from scratch."""
import os, sys, wave
import numpy as np
from scipy.signal import butter, lfilter

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
SR = 44100
rng = np.random.default_rng(17)
def t(s): return np.arange(int(SR * s)) / SR
def noise(s): return rng.uniform(-1, 1, int(SR * s))
def lp(x, hz, o=2): b, a = butter(o, hz / (SR / 2), "low"); return lfilter(b, a, x)
def hp(x, hz, o=2): b, a = butter(o, hz / (SR / 2), "high"); return lfilter(b, a, x)
def bp(x, lo, hi, o=2): b, a = butter(o, [lo / (SR / 2), hi / (SR / 2)], "band"); return lfilter(b, a, x)
def env(s, a, d): tt = t(s); return np.minimum(1, tt / max(a, 1e-4)) * np.exp(-tt / d)
def thump(s, f0, f1, d): tt = t(s); return np.sin(2 * np.pi * np.cumsum(f1 + (f0 - f1) * np.exp(-tt * 30)) / SR) * np.exp(-tt / d)
def mx(*xs):
    n = max(len(x) for x in xs); out = np.zeros(n)
    for x in xs: out[:len(x)] += x
    return out
def place(b, x, at, g=1.0):
    i = int(SR * at); m = min(len(x), len(b) - i); b[i:i + m] += x[:m] * g
def room(x, amt=0.2, size=1.0):
    out = x.copy()
    for dl, g in ((0.023, 0.5), (0.037, 0.4), (0.053, 0.32), (0.079, 0.24), (0.113, 0.17), (0.167, 0.1)):
        i = int(SR * dl * size); out[i:] += x[:-i] * g * amt * 2
    return out
def write(name, x, gain=0.88):
    x = x / (np.max(np.abs(x)) + 1e-9) * gain
    f = int(SR * 0.01); x[-f:] *= np.linspace(1, 0, f)
    with wave.open(os.path.join(OUT, name + ".wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())

# ---- flying (jetpack) : played while you hold fly. Shown here as a 1.2 s blast ----
def jet(s, rough=0.3, low=0.6, seed=0):
    r = np.random.default_rng(seed)
    n = r.uniform(-1, 1, int(SR * s))
    body = lp(n, 2600, 3) * 1.0 + bp(n, 2500, 7000) * 0.35 + lp(n, 300, 2) * low
    tt = t(s)
    flutter = 1 + rough * np.sin(2 * np.pi * 23 * tt + 2 * np.sin(2 * np.pi * 3 * tt)) * (0.5 + 0.5 * r.random(len(tt)))
    swell = np.minimum(1, tt / 0.2) ** 1.5 * np.minimum(1, (s - tt) / 0.12)
    return body * flutter * swell
write("01_jet_roar", jet(1.2, 0.25, 0.7, 1))
write("02_jet_rocket", jet(1.2, 0.45, 0.35, 2) + bp(noise(1.2), 900, 1300) * 0.25 * np.minimum(1, t(1.2) / 0.2))

# ---- hand push / speed boost swish ----
def swish(s, lo, hi, seed, peak=0.4):
    tt = t(s)
    shape = np.sin(np.pi * np.clip(tt / s, 0, 1)) ** 2 * np.exp(-((tt / s - peak) ** 2) / 0.08)
    sweep = bp(np.random.default_rng(seed).uniform(-1, 1, len(tt)), lo, hi)
    return sweep * shape
b = np.zeros(int(SR * 0.4)); place(b, swish(0.24, 600, 1400, 3), 0)
write("03_push_swish", b)
b = np.zeros(int(SR * 0.5)); place(b, swish(0.3, 500, 2200, 4, 0.3), 0); place(b, swish(0.18, 900, 3000, 5, 0.5), 0.12, 0.6)
write("04_push_double_swish", b)

# ---- sniper ----
def crack(s=0.06):
    return hp(noise(s), 2500) * env(s, 0.0003, 0.008) * 1.2
b = np.zeros(int(SR * 1.4))
place(b, mx(crack(), thump(0.3, 220, 70, 0.07) * 1.2, lp(noise(0.5), 1500) * env(0.5, 0.001, 0.12) * 0.9), 0)
place(b, lp(noise(1.0), 900) * env(1.0, 0.05, 0.35) * 0.25, 0.08)           # long echo across the valley
place(b, bp(noise(0.06), 1500, 4000) * env(0.06, 0.002, 0.015) * 0.3, 0.75)  # bolt click
write("05_sniper_echo", room(b, 0.25, 1.6))
b = np.zeros(int(SR * 1.0))
place(b, mx(crack(0.04) * 1.3, thump(0.25, 300, 90, 0.05), hp(noise(0.25), 800) * env(0.25, 0.001, 0.04)), 0)
place(b, np.sin(2 * np.pi * 2600 * t(0.4)) * env(0.4, 0.001, 0.12) * 0.12, 0.0)   # metallic ring
write("06_sniper_snap", room(b, 0.2, 1.2))

# ---- bombs ----
def boom(s, f0, deep, seed):
    r = np.random.default_rng(seed)
    n = r.uniform(-1, 1, int(SR * s))
    x = lp(n, 900, 3) * env(s, 0.004, 0.32) * 1.4 + thump(s, f0, 38, 0.3) * deep + hp(n, 2000) * env(s, 0.001, 0.05) * 0.5
    for i in r.integers(int(SR * 0.15), int(SR * (s - 0.2)), 18):      # debris rattle
        m = min(400, len(x) - i); x[i:i + m] += r.uniform(-1, 1, m) * np.exp(-np.arange(m) / 60) * 0.15
    return np.tanh(x * 1.5)
write("07_bomb_big", room(boom(1.6, 140, 1.4, 6), 0.3, 1.4))
b = np.zeros(int(SR * 1.5))
place(b, np.sin(2 * np.pi * 1900 * t(0.06)) * env(0.06, 0.001, 0.02) * 0.4, 0)          # last beep of the time bomb
place(b, boom(1.3, 170, 1.0, 7), 0.12)
write("08_bomb_timebomb", room(b, 0.25))

# ---- death (best two from the cries page, re-made here so the pack is complete) ----
import subprocess
src = os.path.join(os.path.dirname(OUT.rstrip("/")), "sq")
for i, (srcname, name) in enumerate((("01_squeak_aah", "09_death_squeak"), ("07_squeak_poof", "10_death_squeak_poof"))):
    p = os.path.join(src, srcname + ".wav")
    if os.path.exists(p):
        w = wave.open(p); d = np.frombuffer(w.readframes(w.getnframes()), np.int16) / 32768
        write(name, d.copy())
print("pack ok", sorted(os.listdir(OUT)))
