"""Generate Sky Squad sound effects as 16-bit mono WAV files."""
import os, sys, wave
import numpy as np
from scipy.signal import butter, lfilter

OUT = os.path.join(sys.argv[1], "sfx")
os.makedirs(OUT, exist_ok=True)
SR = 22050
rng = np.random.default_rng(1)

def t(sec):
    return np.arange(int(SR * sec)) / SR

def noise(sec):
    return rng.uniform(-1, 1, int(SR * sec))

def lp(x, hz, order=2):
    b, a = butter(order, hz / (SR / 2), "low")
    return lfilter(b, a, x)

def hp(x, hz, order=2):
    b, a = butter(order, hz / (SR / 2), "high")
    return lfilter(b, a, x)

def bp(x, lo, hi):
    b, a = butter(2, [lo / (SR / 2), hi / (SR / 2)], "band")
    return lfilter(b, a, x)

def env(sec, attack, decay):
    tt = t(sec)
    e = np.minimum(1, tt / max(attack, 1e-4)) * np.exp(-tt / decay)
    return e

def thump(sec, f0, f1, decay):
    tt = t(sec)
    f = f1 + (f0 - f1) * np.exp(-tt * 30)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-tt / decay)

def write(name, x, gain=0.9):
    x = x / (np.max(np.abs(x)) + 1e-9) * gain
    x = np.clip(x, -1, 1)
    d = (x * 32767).astype(np.int16)
    with wave.open(os.path.join(OUT, name + ".wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(d.tobytes())

def gunshot(sec, crack_hz, body_hz, decay, thump_f, thump_amt, tail=0.0):
    n = noise(sec)
    crack = hp(n, crack_hz) * env(sec, 0.0005, decay * 0.35)
    body = lp(n, body_hz) * env(sec, 0.001, decay)
    th = thump(sec, thump_f * 2.5, thump_f, decay * 0.8) * thump_amt
    x = crack * 0.7 + body * 1.4 + th
    if tail:
        x += lp(noise(sec), 900) * env(sec, 0.02, tail) * 0.25
    return x

write("magnum", gunshot(0.45, 2500, 1800, 0.08, 90, 1.0, 0.18))
write("uzi", gunshot(0.12, 3000, 2600, 0.03, 140, 0.4), 0.7)
write("ak47", gunshot(0.42, 1700, 1250, 0.09, 72, 1.4, 0.22), 0.95)
write("shotgun", gunshot(0.6, 1500, 900, 0.13, 70, 1.3, 0.25))
write("sniper", gunshot(0.9, 3500, 2000, 0.07, 80, 1.0, 0.45))
# rocket launch whoosh
sec = 0.7
wh = bp(noise(sec), 300, 2400) * env(sec, 0.02, 0.3) + thump(sec, 160, 60, 0.1) * 0.8
write("rpg", wh, 0.8)
# explosion
sec = 1.6
ex = lp(noise(sec), 500, 3) * env(sec, 0.002, 0.45) * 1.5 + thump(sec, 120, 35, 0.35) * 1.2 + hp(noise(sec), 2000) * env(sec, 0.001, 0.05) * 0.4
write("explosion", ex, 0.95)
# jetpack loop (1s, seamless by crossfading)
sec = 1.2
j = lp(noise(sec), 1100, 3) * 0.8 + hp(lp(noise(sec), 5000), 2500) * 0.2
j *= 1 + 0.15 * np.sin(2 * np.pi * 9 * t(sec))
L = int(SR * 1.0); fade = int(SR * 0.2)
loop = j[:L].copy()
loop[:fade] = loop[:fade] * np.linspace(0, 1, fade) + j[L:L + fade] * np.linspace(1, 0, fade)
write("jet", loop, 0.6)
# clicks
def click(sec=0.05, hz=3000):
    return hp(noise(sec), hz) * env(sec, 0.0003, 0.008)
r = np.zeros(int(SR * 0.6)); c1 = click(); c2 = click(0.06, 2000)
r[:len(c1)] += c1; o = int(SR * 0.42); r[o:o + len(c2)] += c2 * 1.2
r[int(SR * 0.2):int(SR * 0.2) + len(c1)] += lp(noise(0.05), 1200) * env(0.05, 0.001, 0.02)
write("reload", r, 0.6)
write("empty", click(0.08, 2500), 0.5)
sw = np.zeros(int(SR * 0.25)); sw[:len(c1)] += c1; o = int(SR * 0.1); sw[o:o + len(c2)] += c2
write("swap", sw, 0.5)
# pickup blip
tt = t(0.22)
f = 600 + 900 * tt / 0.22
write("pickup", np.sin(2 * np.pi * np.cumsum(f) / SR) * env(0.22, 0.005, 0.1), 0.5)
# hit (thud) and headshot (ding)
write("hit", lp(noise(0.12), 700) * env(0.12, 0.001, 0.03) + thump(0.12, 200, 90, 0.04), 0.6)
tt = t(0.4)
write("headshot", (np.sin(2 * np.pi * 1320 * tt) + 0.5 * np.sin(2 * np.pi * 1980 * tt)) * env(0.4, 0.002, 0.12), 0.5)
# throw
write("throw", bp(noise(0.25), 400, 1800) * env(0.25, 0.04, 0.06), 0.4)
# land / step
write("land", lp(noise(0.12), 400) * env(0.12, 0.001, 0.03), 0.5)
# warning siren
tt = t(1.0)
f = 700 + 250 * np.sin(2 * np.pi * 2 * tt)
write("warn", np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.3 * env(1.0, 0.02, 0.8), 0.35)
# crumble
write("crumble", lp(noise(0.8), 350, 3) * env(0.8, 0.05, 0.3) * (1 + 0.6 * rng.uniform(0, 1, int(SR * 0.8))), 0.7)
# melee whoosh
write("melee", bp(noise(0.18), 800, 3000) * env(0.18, 0.03, 0.05), 0.5)
print(sorted(os.listdir(OUT)))

# ---- v0.5 additions ----
write("smg", gunshot(0.16, 2600, 2100, 0.04, 120, 0.6, 0.06), 0.75)
tt = t(0.35)
buzzw = np.sign(np.sin(2 * np.pi * 120 * tt)) * 0.5 + hp(noise(0.35), 3000) * 0.8
buzzw *= (0.6 + 0.4 * rng.uniform(0, 1, len(tt))) * env(0.35, 0.005, 0.18)
write("shock", buzzw, 0.6)
write("net", thump(0.35, 160, 70, 0.08) * 0.8 + bp(noise(0.35), 400, 1500) * env(0.35, 0.01, 0.12), 0.7)
tt = t(0.3)
f = 1800 * np.exp(-tt * 9) + 300
write("laser", (np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.4 * np.sin(4 * np.pi * np.cumsum(f) / SR)) * env(0.3, 0.002, 0.11), 0.55)
tt = t(0.09)
write("beep", np.sin(2 * np.pi * 1900 * tt) * env(0.09, 0.002, 0.04), 0.45)
write("slash", bp(noise(0.22), 1500, 5000) * env(0.22, 0.02, 0.05), 0.55)
# crisper weapon switch: two metal clacks with a short ring
sw = np.zeros(int(SR * 0.22))
c1 = hp(noise(0.03), 2500) * env(0.03, 0.0002, 0.006)
sw[:len(c1)] += c1 * 1.2
o = int(SR * 0.07)
ring = np.sin(2 * np.pi * 2600 * t(0.12)) * env(0.12, 0.001, 0.03) * 0.35
sw[o:o + len(c1)] += c1
sw[o:o + len(ring)] += ring
write("swap", sw, 0.6)
