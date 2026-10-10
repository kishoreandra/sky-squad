"""Short original kill music clips (1-2.5 s) for Sky Squad. Each one is made from scratch with numpy."""
import os, sys, wave
import numpy as np
from scipy.signal import butter, lfilter

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
SR = 44100
rng = np.random.default_rng(3)

def t(sec): return np.arange(int(SR * sec)) / SR
def mtof(m): return 440.0 * 2 ** ((m - 69) / 12)
def env(sec, a=0.005, d=0.3, s=0.0):
    tt = t(sec); return np.minimum(1, tt / a) * (s + (1 - s) * np.exp(-tt / d))
def lp(x, hz, o=2):
    b, a = butter(o, min(hz, SR / 2 - 100) / (SR / 2), "low"); return lfilter(b, a, x)
def hp(x, hz, o=2):
    b, a = butter(o, hz / (SR / 2), "high"); return lfilter(b, a, x)
def bp(x, lo, hi):
    b, a = butter(2, [lo / (SR / 2), hi / (SR / 2)], "band"); return lfilter(b, a, x)
def noise(sec): return rng.uniform(-1, 1, int(SR * sec))
def saw(f, sec, detune=0.0):
    tt = t(sec); out = np.zeros_like(tt)
    for d in (-detune, 0, detune):
        out += 2 * ((tt * f * (1 + d)) % 1) - 1
    return out / 3
def sq(f, sec, duty=0.5): return np.where((t(sec) * f) % 1 < duty, 1.0, -1.0)
def sine(f, sec): return np.sin(2 * np.pi * f * t(sec))
def tri(f, sec): return 2 * np.abs(2 * ((t(sec) * f) % 1) - 1) - 1
def place(buf, x, at, g=1.0):
    i = int(SR * at); n = min(len(x), len(buf) - i)
    if n > 0: buf[i:i + n] += x[:n] * g
def kick(sec=0.4, f0=150, f1=45):
    tt = t(sec); f = f1 + (f0 - f1) * np.exp(-tt * 28)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / 0.16)
def snare(sec=0.3):
    return hp(noise(sec), 1500) * env(sec, 0.001, 0.07) * 0.8 + sine(190, sec) * env(sec, 0.001, 0.05) * 0.5
def hat(sec=0.08): return hp(noise(sec), 7000) * env(sec, 0.0005, 0.02)
def crash(sec=1.6): return hp(noise(sec), 4000) * env(sec, 0.002, 0.5) * 0.5
def reverb(x, amt=0.25):
    out = x.copy()
    for d, g in ((0.031, 0.5), (0.047, 0.4), (0.071, 0.33), (0.113, 0.25), (0.167, 0.18)):
        i = int(SR * d); out[i:] += x[:-i] * g * amt * 2
    return out
def write(name, x, gain=0.85):
    x = x / (np.max(np.abs(x)) + 1e-9) * gain
    d = (np.clip(x, -1, 1) * 32767).astype(np.int16)
    with wave.open(os.path.join(OUT, name + ".wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(d.tobytes())

# 1 Arcade Level-Up: fast chiptune arpeggio up to a held note
b = np.zeros(int(SR * 1.3))
for i, m in enumerate([72, 76, 79, 84, 88]):
    place(b, sq(mtof(m), 0.09, 0.25) * env(0.09, 0.002, 0.2, 0.6), i * 0.065, 0.5)
place(b, (sq(mtof(91), 0.7, 0.25) * 0.5 + sq(mtof(79), 0.7, 0.5) * 0.25) * env(0.7, 0.002, 0.35), 0.33)
write("01_arcade_levelup", lp(b, 9000))

# 2 Brass Stab: big synth-brass chord hit with a drum, short and punchy
b = np.zeros(int(SR * 1.6))
ch = sum(saw(mtof(m), 1.2, 0.006) for m in [55, 62, 67, 70, 74])
filt_env = 1800 + 4000 * np.exp(-t(1.2) / 0.15)
brass = np.zeros_like(ch)
for i in range(0, len(ch), 512):   # moving filter, block by block
    seg = ch[max(0, i - 2048):i + 512]
    brass[i:i + 512] = lp(seg, float(filt_env[min(i, len(filt_env) - 1)]))[-len(brass[i:i + 512]):]
place(b, brass * env(1.2, 0.01, 0.45), 0.0, 0.7)
place(b, kick(0.5, 120, 40), 0.0, 1.0)
place(b, crash(1.4), 0.0, 0.35)
write("02_brass_stab", reverb(b, 0.3))

# 3 Rock Riff: two distorted power-chord hits (palm-muted then open)
def guitar(m, sec):
    x = saw(mtof(m), sec, 0.003) + saw(mtof(m + 7), sec, 0.003) + 0.6 * saw(mtof(m + 12), sec, 0.003)
    x = np.tanh(x * 6)
    return lp(x, 3500) * env(sec, 0.003, sec * 0.5, 0.2)
b = np.zeros(int(SR * 1.8))
for at in (0.0, 0.12, 0.24):
    place(b, guitar(40, 0.11) * env(0.11, 0.002, 0.04), at, 0.7)
place(b, guitar(43, 1.3), 0.38, 0.9)
place(b, kick(), 0.0); place(b, kick(), 0.24); place(b, snare(), 0.38); place(b, crash(), 0.38, 0.6)
write("03_rock_riff", reverb(b, 0.2))

# 4 Victory Fanfare: trumpet-like da-da-daaa
def horn(m, sec):
    f = mtof(m) * (1 + 0.004 * np.sin(2 * np.pi * 5.5 * t(sec)) * np.clip(t(sec) / 0.2, 0, 1))
    ph = np.cumsum(f) / SR
    x = sum((1.0 / k) * np.sin(2 * np.pi * ph * k) for k in range(1, 9))
    return lp(np.tanh(x * 1.5), 4000) * env(sec, 0.02, sec * 0.8, 0.5)
b = np.zeros(int(SR * 1.8))
place(b, horn(67, 0.13), 0.0); place(b, horn(67, 0.13), 0.15); place(b, horn(72, 1.0) + 0.6 * horn(76, 1.0), 0.3)
place(b, kick(0.5, 100, 40), 0.3, 0.8); place(b, crash(1.3), 0.3, 0.3)
write("04_victory_fanfare", reverb(b, 0.35))

# 5 Bass Drop: riser whoosh into a deep 808 boom
b = np.zeros(int(SR * 2.0))
rise = bp(noise(0.5), 800, 6000) * np.linspace(0, 1, int(SR * 0.5)) ** 2
place(b, rise, 0.0, 0.5)
place(b, sine(mtof(36), 1.4) * env(1.4, 0.005, 0.6) * (1 + 0.3 * np.tanh(4 * sine(mtof(36), 1.4))), 0.5)
place(b, kick(0.6, 180, 40), 0.5, 1.2)
place(b, crash(1.2), 0.5, 0.25)
write("05_bass_drop", np.tanh(b * 1.3))

# 6 Orchestra Hit: dark, dramatic minor stab + timpani roll
b = np.zeros(int(SR * 1.8))
strings = sum(saw(mtof(m), 1.4, 0.008) for m in [50, 57, 62, 65, 69, 74])
place(b, lp(strings, 3000) * env(1.4, 0.008, 0.5), 0.0, 0.6)
for i in range(6):
    place(b, kick(0.35, 90, 55) * 0.5, 0.35 + i * 0.07, 0.6 - i * 0.07)
place(b, kick(0.8, 110, 45), 0.0, 1.0)
place(b, crash(1.6), 0.0, 0.4)
write("06_orchestra_hit", reverb(b, 0.45))

# 7 Dhol Celebration: Indian dhol beat - bass "dha", sharp "ta", fast roll, final big hit
def dha(sec=0.35): return kick(sec, 130, 70) * 0.9 + bp(noise(sec), 200, 900) * env(sec, 0.002, 0.05) * 0.4
def ta(sec=0.15): return bp(noise(sec), 1800, 6000) * env(sec, 0.001, 0.03) + sine(780, sec) * env(sec, 0.001, 0.04) * 0.5
b = np.zeros(int(SR * 1.9))
pattern = [(0.0, "D"), (0.14, "t"), (0.21, "t"), (0.28, "D"), (0.42, "t"), (0.49, "D"), (0.56, "t"), (0.6, "t"), (0.64, "t"), (0.68, "t"), (0.72, "t"), (0.8, "D")]
for at, k in pattern:
    place(b, dha() if k == "D" else ta(), at, 1.0 if k == "D" else 0.7)
place(b, dha(0.7) * 1.3, 0.8)
place(b, (tri(mtof(74), 0.6) + 0.5 * tri(mtof(79), 0.6)) * env(0.6, 0.01, 0.3) * 0.25, 0.8)  # little shehnai-like note
write("07_dhol_celebration", reverb(b, 0.2))

# 8 Coin Combo: sparkly bell cascade down then up, light and happy
def bell(m, sec):
    f = mtof(m)
    return (sine(f, sec) + 0.5 * sine(f * 2.76, sec) * env(sec, 0.001, 0.12) + 0.25 * sine(f * 5.4, sec) * env(sec, 0.001, 0.05)) * env(sec, 0.001, 0.35)
b = np.zeros(int(SR * 1.5))
for i, m in enumerate([84, 88, 91, 96, 91, 96, 100]):
    place(b, bell(m, 0.6), i * 0.07, 0.45)
write("08_coin_combo", reverb(b, 0.4))

# 9 Trap Hit: fast hi-hat roll, snare clap and a sliding 808
b = np.zeros(int(SR * 2.0))
for i in range(12):
    place(b, hat(), i * 0.035, 0.5 + i * 0.03)
place(b, snare(0.4), 0.42, 1.0)
place(b, hp(noise(0.25), 1000) * env(0.25, 0.001, 0.05), 0.42, 0.6)
tt = t(1.3); f = mtof(38) * (1.5 - 0.5 * np.clip(tt / 0.15, 0, 1))
place(b, np.tanh(2 * np.sin(2 * np.pi * np.cumsum(f) / SR)) * env(1.3, 0.005, 0.5), 0.42, 0.9)
write("09_trap_hit", b)

# 10 Spy Sting: sneaky surf-guitar twang, cool and short
b = np.zeros(int(SR * 1.7))
def twang(m, sec):
    x = saw(mtof(m), sec, 0.002) * env(sec, 0.002, 0.3)
    return lp(np.tanh(x * 3), 2500) * (1 + 0.3 * np.sin(2 * np.pi * 7 * t(sec)))
for i, m in enumerate([52, 55, 58, 59]):
    place(b, twang(m, 0.18), i * 0.1, 0.6)
place(b, twang(64, 1.1), 0.42, 0.9)
place(b, twang(70, 1.1), 0.42, 0.4)
place(b, snare(0.3), 0.42, 0.4)
write("10_spy_sting", reverb(b, 0.4))
print("made", sorted(os.listdir(OUT)))
