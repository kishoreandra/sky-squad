"""Sky Squad v0.8 voices: death yells (3 kinds) and short pain grunts (2 kinds), made with a simple voice model
(buzzing vocal cords shaped by mouth resonances), plus a rough growl so they sound like a soldier, not a beep."""
import os, sys, wave
import numpy as np
from scipy.signal import lfilter, butter

OUT = os.path.join(sys.argv[1], "sfx")
SR = 22050
rng = np.random.default_rng(11)

def write(name, x, gain=0.9):
    x = x / (np.max(np.abs(x)) + 1e-9) * gain
    d = (np.clip(x, -1, 1) * 32767).astype(np.int16)
    with wave.open(os.path.join(OUT, name + ".wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(d.tobytes())

def resonator(x, f, bw):
    r = np.exp(-np.pi * bw / SR)
    th = 2 * np.pi * f / SR
    a = [1, -2 * r * np.cos(th), r * r]
    return lfilter([1 - r], a, x)

def voice(sec, f0_curve, formants, growl=0.5, breath=0.15, seed=0):
    r = np.random.default_rng(seed)
    n = int(SR * sec)
    tt = np.arange(n) / SR
    f0 = f0_curve(tt / sec) * (1 + 0.012 * r.standard_normal(n).cumsum() / np.sqrt(np.arange(1, n + 1)))
    ph = np.cumsum(f0) / SR
    saw = 2 * (ph % 1.0) - 1                                   # glottal buzz
    pulse = np.tanh(3 * saw) - 0.6 * saw
    sub = np.sin(2 * np.pi * ph * 0.5)                         # subharmonic = rough growl
    am = 1 + growl * (0.5 + 0.5 * np.sin(2 * np.pi * 33 * tt + r.uniform(0, 6))) * (0.6 + 0.4 * r.random(n))
    src = (pulse + growl * 0.35 * sub) * am + breath * r.uniform(-1, 1, n)
    out = np.zeros(n)
    for (f, bw, g) in formants:
        out += resonator(src, f, bw) * g
    b, a = butter(2, 120 / (SR / 2), "high")
    return lfilter(b, a, out)

def env(n, att, rel):
    e = np.ones(n)
    a = int(SR * att); rl = int(SR * rel)
    e[:a] = np.linspace(0, 1, a) ** 0.6
    e[-rl:] *= np.linspace(1, 0, rl) ** 1.5
    return e

AA = [(760, 90, 1.0), (1180, 110, 0.6), (2550, 170, 0.25), (3400, 250, 0.1)]   # "aaa"
UH = [(620, 90, 1.0), (1050, 110, 0.55), (2450, 170, 0.22), (3300, 250, 0.1)]  # "uhh"
OH = [(520, 80, 1.0), (880, 100, 0.6), (2400, 160, 0.2), (3200, 250, 0.08)]    # "ohh"

def yell(sec, f_start, f_peak, f_end, formants, growl, seed):
    def curve(k):
        up = np.clip(k / 0.18, 0, 1)
        down = np.clip((k - 0.18) / 0.82, 0, 1)
        return np.where(k < 0.18, f_start + (f_peak - f_start) * up, f_peak + (f_end - f_peak) * down ** 1.3)
    v = voice(sec, curve, formants, growl=growl, seed=seed)
    v = np.tanh(v / (np.max(np.abs(v)) + 1e-9) * 2.2)        # strained, shouted
    return v * env(len(v), 0.035, sec * 0.45)

write("die0", yell(0.75, 190, 250, 120, AA, 0.55, 1), 0.85)   # "AAARGH"
write("die1", yell(0.62, 220, 280, 140, UH, 0.7, 2), 0.85)    # "UUHHH"
write("die2", yell(0.9, 170, 230, 95, OH, 0.5, 3), 0.85)      # long "OHHH" falling
def grunt(sec, f, formants, seed):
    v = voice(sec, lambda k: f * (1.05 - 0.25 * k), formants, growl=0.8, breath=0.25, seed=seed)
    v = np.tanh(v / (np.max(np.abs(v)) + 1e-9) * 2.0)
    return v * env(len(v), 0.012, sec * 0.6)
write("ow0", grunt(0.17, 170, UH, 4), 0.6)   # "uh!"
write("ow1", grunt(0.2, 150, OH, 5), 0.6)    # "oof"
print("v08 voices ok")
