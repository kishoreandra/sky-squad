"""Sky Squad v0.7 sounds: kill/death/suicide, bomb arming, gun rack at start, gas hiss + cough,
minigun spin + fire, flamethrower, burning, heartbeat, bullet whizz, splash, last-seconds tick, crown chime, respawn."""
import os, sys, wave
import numpy as np
from scipy.signal import butter, lfilter

OUT = os.path.join(sys.argv[1], "sfx")
SR = 22050
rng = np.random.default_rng(7)

def t(sec): return np.arange(int(SR * sec)) / SR
def noise(sec): return rng.uniform(-1, 1, int(SR * sec))
def lp(x, hz, o=2):
    b, a = butter(o, hz / (SR / 2), "low"); return lfilter(b, a, x)
def hp(x, hz, o=2):
    b, a = butter(o, hz / (SR / 2), "high"); return lfilter(b, a, x)
def bp(x, lo, hi):
    b, a = butter(2, [lo / (SR / 2), hi / (SR / 2)], "band"); return lfilter(b, a, x)
def env(sec, att, dec):
    tt = t(sec); return np.minimum(1, tt / max(att, 1e-4)) * np.exp(-tt / dec)
def tone(sec, f, dec, att=0.002):
    tt = t(sec); return np.sin(2 * np.pi * f * tt) * env(sec, att, dec)
def sweep(sec, f0, f1):
    tt = t(sec); f = f0 + (f1 - f0) * tt / sec
    return np.sin(2 * np.pi * np.cumsum(f) / SR)
def thump(sec, f0, f1, dec):
    tt = t(sec); f = f1 + (f0 - f1) * np.exp(-tt * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / dec)
def place(buf, x, at):
    i = int(SR * at); n = min(len(x), len(buf) - i); buf[i:i + n] += x[:n]; return buf
def write(name, x, gain=0.9):
    x = x / (np.max(np.abs(x)) + 1e-9) * gain
    d = (np.clip(x, -1, 1) * 32767).astype(np.int16)
    with wave.open(os.path.join(OUT, name + ".wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(d.tobytes())

# kill confirm (killer hears): bright double "ting" over a soft punch
b = np.zeros(int(SR * 0.6))
place(b, thump(0.2, 180, 70, 0.05) * 0.8, 0)
place(b, (tone(0.4, 1568, 0.12) + 0.4 * tone(0.4, 3136, 0.06)) * 0.6, 0.02)
place(b, (tone(0.45, 2093, 0.16) + 0.3 * tone(0.45, 4186, 0.07)) * 0.6, 0.11)
write("kill", b, 0.7)

# death (the one killed hears): heavy heartbeat thud + muffled ringing ear
b = np.zeros(int(SR * 1.4))
place(b, thump(0.35, 110, 40, 0.12) * 1.2, 0)
place(b, lp(noise(0.3), 300) * env(0.3, 0.002, 0.06), 0)
ring = np.sin(2 * np.pi * 3100 * t(1.3)) * env(1.3, 0.05, 0.5) * 0.18
place(b, ring, 0.05)
place(b, thump(0.3, 90, 40, 0.1) * 0.7, 0.32)
write("death", b, 0.75)

# suicide: "womp womp" - two sad falling muted horn notes
def horn(sec, f0, f1):
    s = sweep(sec, f0, f1)
    s = np.tanh(2.2 * s) * env(sec, 0.03, sec * 0.7)
    return lp(s, 1200)
b = np.zeros(int(SR * 1.3))
place(b, horn(0.38, 233, 220), 0)
place(b, horn(0.8, 220, 160), 0.42)
write("suicide", b, 0.6)

# time bomb armed: switch click then three rising chirps
b = np.zeros(int(SR * 0.55))
place(b, hp(noise(0.02), 2500) * env(0.02, 0.0002, 0.004), 0)
for i, f in enumerate((1400, 1800, 2400)):
    place(b, tone(0.07, f, 0.03) * 0.7, 0.08 + i * 0.12)
write("arm", b, 0.55)

# match start: rifle charging handle pulled back and slammed forward
b = np.zeros(int(SR * 0.6))
place(b, bp(noise(0.12), 900, 4000) * env(0.12, 0.005, 0.03) * 0.7, 0)
place(b, hp(noise(0.03), 2000) * env(0.03, 0.0002, 0.006), 0.1)
place(b, hp(noise(0.1), 1500) * env(0.1, 0.0002, 0.01) + thump(0.1, 400, 180, 0.02) * 0.6, 0.3)
place(b, tone(0.15, 2900, 0.03) * 0.15, 0.31)
write("rack", b, 0.7)

# gas release hiss
sec = 1.6
h = hp(noise(sec), 2500) * env(sec, 0.02, 0.55) + bp(noise(sec), 600, 2000) * env(sec, 0.01, 0.2) * 0.4
write("hiss", h, 0.5)

# cough (two hacking bursts)
b = np.zeros(int(SR * 0.6))
for at, g in ((0, 1.0), (0.22, 0.8)):
    c = bp(noise(0.16), 250, 1600) * env(0.16, 0.004, 0.05) * g
    c += np.sin(2 * np.pi * 160 * t(0.16)) * env(0.16, 0.004, 0.04) * 0.4 * g
    place(b, c, at)
write("cough", b, 0.6)

# minigun barrels spinning up (motor whine rising)
sec = 0.55
tt = t(sec)
f = 90 + 380 * (tt / sec) ** 0.7
ph = np.cumsum(f) / SR
whir = (np.sign(np.sin(2 * np.pi * ph * 6)) * 0.3 + np.sin(2 * np.pi * ph)) * np.minimum(1, tt / 0.1)
whir = lp(whir, 2400) + bp(noise(sec), 1500, 4000) * 0.15
write("spin", whir, 0.5)

# minigun shot: short, tight, buzzy
def gunshot(sec, crack_hz, body_hz, decay, tf, ta):
    n = noise(sec)
    return hp(n, crack_hz) * env(sec, 0.0005, decay * 0.35) * 0.7 + lp(n, body_hz) * env(sec, 0.001, decay) * 1.4 + thump(sec, tf * 2.5, tf, decay * 0.8) * ta
write("minigun", gunshot(0.09, 2800, 2400, 0.022, 110, 0.6), 0.6)

# flamethrower roar burst
sec = 0.42
r = lp(noise(sec), 700, 3) * env(sec, 0.03, 0.18) * 1.4 + bp(noise(sec), 1500, 5000) * env(sec, 0.02, 0.1) * 0.3
crack = np.zeros(len(r))
for i in rng.integers(0, len(r) - 200, 10):
    crack[i:i + 60] += rng.uniform(-1, 1, 60) * np.exp(-np.arange(60) / 12)
write("flame", r + crack * 0.25, 0.7)

# burning on you: crackle + sizzle
sec = 0.7
sz = hp(noise(sec), 4000) * env(sec, 0.05, 0.3) * 0.5
cr = np.zeros(int(SR * sec))
for i in rng.integers(0, len(cr) - 200, 22):
    cr[i:i + 80] += rng.uniform(-1, 1, 80) * np.exp(-np.arange(80) / 15)
write("sizzle", sz + cr * 0.6, 0.45)

# heartbeat (lub-dub) for low health
b = np.zeros(int(SR * 0.7))
place(b, thump(0.18, 70, 45, 0.06), 0)
place(b, thump(0.16, 60, 40, 0.05) * 0.7, 0.2)
write("heart", lp(b, 200), 0.8)

# bullet whizz past your head
sec = 0.22
tt = t(sec)
f = 2600 * np.exp(-tt * 8) + 500
wz = bp(noise(sec), 1200, 6000) * np.sin(np.pi * np.clip(tt / sec, 0, 1)) ** 2
wz += np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * tt / sec) ** 2 * 0.25
write("whiz", wz, 0.45)

# water splash
sec = 0.6
sp = bp(noise(sec), 400, 3500) * env(sec, 0.005, 0.15) + hp(noise(sec), 3000) * env(sec, 0.02, 0.25) * 0.3
write("splash", sp, 0.55)

# last seconds clock tick
write("tick", hp(noise(0.04), 1800) * env(0.04, 0.0003, 0.008) + tone(0.04, 1200, 0.01) * 0.4, 0.45)

# you took the lead: soft rising three-note chime
b = np.zeros(int(SR * 0.8))
for i, f in enumerate((784, 988, 1319)):
    place(b, (tone(0.5, f, 0.2) + 0.3 * tone(0.5, f * 2, 0.1)) * 0.5, i * 0.09)
write("crown", b, 0.5)

# respawn: airy whoosh in
sec = 0.5
tt = t(sec)
wh = bp(noise(sec), 500, 3000) * np.sin(np.pi * tt / sec) ** 2 + sweep(sec, 300, 900) * np.sin(np.pi * tt / sec) ** 2 * 0.15
write("spawn", wh, 0.45)
print("v07 sfx ok")
