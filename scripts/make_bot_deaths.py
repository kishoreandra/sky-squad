"""Bot / toy-soldier death sounds for Sky Squad: no human voices. Short, punchy, game-like."""
import os, sys, wave
import numpy as np
from scipy.signal import butter, lfilter

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
SR = 44100
rng = np.random.default_rng(9)

def t(s): return np.arange(int(SR * s)) / SR
def env(s, a=0.003, d=0.2): tt = t(s); return np.minimum(1, tt / a) * np.exp(-tt / d)
def noise(s): return rng.uniform(-1, 1, int(SR * s))
def lp(x, hz, o=2): b, a = butter(o, min(hz, 20000) / (SR / 2), "low"); return lfilter(b, a, x)
def hp(x, hz, o=2): b, a = butter(o, hz / (SR / 2), "high"); return lfilter(b, a, x)
def bp(x, lo, hi): b, a = butter(2, [lo / (SR / 2), hi / (SR / 2)], "band"); return lfilter(b, a, x)
def osc(freq, kind="sin"):
    ph = np.cumsum(freq) / SR
    if kind == "sq": return np.where(ph % 1 < 0.5, 1.0, -1.0)
    if kind == "saw": return 2 * (ph % 1) - 1
    if kind == "tri": return 2 * np.abs(2 * (ph % 1) - 1) - 1
    return np.sin(2 * np.pi * ph)
def glide(s, f0, f1, curve=1.0):
    k = np.linspace(0, 1, int(SR * s)) ** curve
    return f0 * (f1 / f0) ** k
def thump(s, f0, f1, d): tt = t(s); return np.sin(2 * np.pi * np.cumsum(f1 + (f0 - f1) * np.exp(-tt * 30)) / SR) * np.exp(-tt / d)
def place(b, x, at, g=1.0):
    i = int(SR * at); m = min(len(x), len(b) - i); b[i:i + m] += x[:m] * g
def crush(x, bits=5, hold=6):
    x = np.repeat(x[::hold], hold)[:len(x)]
    q = 2 ** bits; return np.round(x * q) / q
def write(name, x, gain=0.88):
    x = x / (np.max(np.abs(x)) + 1e-9) * gain
    f = int(SR * 0.008); x[-f:] *= np.linspace(1, 0, f)
    with wave.open(os.path.join(OUT, name + ".wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())

# 1 Power down: bot's motor whine slides down and switches off with a click
s = 0.85
f = glide(s, 900, 60, 0.6)
x = (osc(f, "saw") * 0.6 + osc(f * 2.01, "sin") * 0.3) * np.linspace(1, 0.2, len(f))
x = lp(x, 3000)
b = np.zeros(int(SR * 1.0)); place(b, x, 0); place(b, hp(noise(0.02), 2000) * env(0.02, 0.0005, 0.004), 0.86, 0.6)
write("01_power_down", b)

# 2 Glitch out: chopped digital stutter, then cut to silence
b = np.zeros(int(SR * 0.7))
base = osc(glide(0.5, 440, 180), "sq") * 0.5 + noise(0.5) * 0.2
for i, at in enumerate([0, 0.06, 0.1, 0.16, 0.19, 0.25, 0.27, 0.33]):
    seg = crush(base[int(at * SR):int((at + 0.04) * SR)], bits=4 - i % 3 + 2, hold=4 + i * 2)
    place(b, seg, at, 1 - i * 0.08)
place(b, thump(0.15, 200, 60, 0.04), 0.4, 0.6)
write("02_glitch_out", b)

# 3 Robot "UGH": a grunt that is clearly a machine (ring-modulated, buzzy, no human voice)
s = 0.32
f = glide(s, 170, 95)
buzz = osc(f, "saw")
x = bp(buzz, 300, 1400) * osc(np.full(len(f), 55.0)) * env(s, 0.008, 0.12)
x = crush(x, 6, 3)
write("03_robo_ugh", lp(x, 5000))

# 4 Spark and clank: electric zap, then metal parts hitting the floor
b = np.zeros(int(SR * 1.0))
zap = (np.sign(osc(np.full(int(SR * 0.18), 110.0))) * 0.4 + hp(noise(0.18), 3000)) * env(0.18, 0.002, 0.07)
place(b, zap, 0)
for at, fr in ((0.3, 1800), (0.42, 2400), (0.5, 1500), (0.62, 2100)):
    tt = t(0.25)
    clank = sum(np.sin(2 * np.pi * fr * m * tt) * np.exp(-tt / (0.05 / m)) for m in (1, 2.4, 3.9)) * 0.3
    place(b, clank, at, 0.8)
place(b, thump(0.2, 140, 60, 0.05), 0.3, 0.6)
write("04_spark_clank", b)

# 5 Toy squeak: a doodle soldier's tiny high "eep!" (rubber-toy chirp)
s = 0.22
f = np.concatenate([glide(0.06, 900, 1600), glide(0.16, 1600, 700, 0.7)])
x = osc(f, "tri") * np.concatenate([np.linspace(0, 1, int(SR * 0.02)), np.ones(len(f) - int(SR * 0.02))]) * np.exp(-t(len(f) / SR) / 0.12)
b = np.zeros(int(SR * 0.45)); place(b, x, 0); place(b, thump(0.12, 300, 120, 0.03), 0.22, 0.4)
write("05_toy_squeak", b)

# 6 Pop and poof: balloon pop then a puff of smoke
b = np.zeros(int(SR * 0.7))
place(b, hp(noise(0.06), 1000) * env(0.06, 0.0003, 0.006) + thump(0.06, 900, 200, 0.01), 0, 1.0)
place(b, lp(noise(0.5), 1200) * env(0.5, 0.03, 0.15), 0.03, 0.5)
write("06_pop_poof", b)

# 7 Overload: warning beeps speed up, then a small electric burst
b = np.zeros(int(SR * 1.0))
at = 0.0
for i, gap in enumerate([0.16, 0.12, 0.09, 0.07, 0.05]):
    place(b, osc(np.full(int(SR * 0.04), 1800.0 + i * 150), "sq") * env(0.04, 0.001, 0.02) * 0.4, at)
    at += gap
place(b, lp(noise(0.4), 2500) * env(0.4, 0.002, 0.12) + thump(0.4, 160, 50, 0.08), at, 1.0)
place(b, (hp(noise(0.3), 3000) * env(0.3, 0.001, 0.08)), at, 0.4)
write("07_overload", b)

# 8 Rubber splat: squishy cartoon "bloop" as the doodle goes flat
s = 0.4
f = glide(s, 420, 90, 0.5)
x = osc(f) * env(s, 0.004, 0.14) + bp(noise(s), 200, 900) * env(s, 0.002, 0.05) * 0.6
b = np.zeros(int(SR * 0.55)); place(b, x, 0); place(b, thump(0.15, 180, 70, 0.04), 0.06, 0.6)
write("08_rubber_splat", b)

# 9 Tape stop: the soldier's own sound "winds down" like a machine running out of power
s = 0.7
f = glide(s, 330, 25, 2.0)
x = (osc(f, "saw") + 0.5 * osc(f * 1.5, "saw")) * np.linspace(1, 0.4, len(f))
x = lp(x, 2200) + lp(noise(s), 500) * 0.15 * np.linspace(0.3, 1, len(f))
write("09_wind_down", x)

# 10 Retro game-over: 8-bit falling notes, very short
b = np.zeros(int(SR * 0.75))
for i, m in enumerate([76, 72, 67, 60]):
    fr = 440 * 2 ** ((m - 69) / 12)
    place(b, osc(np.full(int(SR * 0.12), fr), "sq") * env(0.12, 0.002, 0.08) * 0.4, i * 0.1)
place(b, osc(glide(0.3, 262, 130), "sq") * env(0.3, 0.002, 0.15) * 0.4, 0.4)
write("10_retro_gameover", lp(b, 7000))

# 11 Sad bot beeps: two-tone falling "boo-doo" chirps, a little cute
b = np.zeros(int(SR * 0.8))
place(b, osc(glide(0.18, 1200, 800)) * env(0.18, 0.005, 0.1), 0)
place(b, osc(glide(0.35, 900, 350, 0.6)) * env(0.35, 0.005, 0.2) * (1 + 0.3 * osc(np.full(int(SR * 0.35), 18.0))), 0.22)
write("11_sad_bot_beeps", b)

# 12 Shatter: crystal armor breaks into sparkles
b = np.zeros(int(SR * 0.9))
place(b, hp(noise(0.08), 2500) * env(0.08, 0.0005, 0.02) + thump(0.08, 500, 150, 0.015), 0, 1.0)
for i in range(14):
    fr = rng.uniform(2500, 6000); tt = t(0.2)
    place(b, np.sin(2 * np.pi * fr * tt) * np.exp(-tt / 0.04) * 0.35, 0.03 + rng.uniform(0, 0.5))
write("12_shatter", b)
print("bot deaths ok")
