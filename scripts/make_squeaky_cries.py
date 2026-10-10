"""Sky Squad death cries in the small-cartoon-soldier style (measured from the reference clip:
0.3-0.8 s long, very high squeaky pitch ~550-850 Hz, bright, flat or slightly falling, sudden start and cut).
These are new sounds made from scratch with the voice model in make_reactions.py, not copies."""
import os, sys
import numpy as np

src = open(os.path.join(os.path.dirname(__file__), "make_reactions.py")).read()
exec(src.split("# 1 \"AARGH!\"")[0].replace("OUT = sys.argv[1]", "OUT = sys.argv[1]"))  # voice model + helpers

S = 1.38   # small character: mouth resonances higher than an adult's

def cry(keys, sec, growl=0.15, seed=0, scream=0.45, jitter=0.01):
    x = voice(keys, sec, growl=growl, jitter=jitter, scale=S, seed=seed, scream=scream)
    cut = int(SR * 0.012)
    x[-cut:] *= np.linspace(1, 0, cut)     # sudden stop, like the reference
    return x

def pad(x, after=0.15):
    return np.concatenate([x, np.zeros(int(SR * after))])

def pop(sec=0.08):
    return burst(sec, 900, 6000, 0.008) + thump(sec, 700, 180, 0.012) * 0.8

# 1 "AAH!" flat squeak
k = [(0, "aa", 720, 0.0, 0.1), (0.015, "aa", 760, 1.0, 0.06), (0.32, "aa", 730, 1.0, 0.06), (0.4, "aa", 690, 0.9, 0.08)]
write("01_squeak_aah", pad(cry(k, 0.4, seed=1)))

# 2 "EEE!" high falling
k = [(0, "ee", 880, 0.0, 0.08), (0.015, "ee", 900, 1.0, 0.05), (0.45, "eh", 650, 0.9, 0.06), (0.52, "eh", 600, 0.7, 0.08)]
write("02_squeak_eee", pad(cry(k, 0.52, seed=2, growl=0.05)))

# 3 "OW-ah!" with a voice crack in the middle
k = [(0, "oh", 560, 0.0, 0.1), (0.015, "oh", 580, 1.0, 0.06), (0.16, "aa", 600, 1.0, 0.06), (0.17, "aa", 820, 1.0, 0.06), (0.42, "aa", 780, 0.9, 0.08)]
write("03_ow_crack", pad(cry(k, 0.44, seed=3)))

# 4 "WAAAH" rises, holds, drops at the end (crying)
k = [(0, "oo", 500, 0.0, 0.1), (0.03, "uh", 530, 1.0, 0.06), (0.2, "aa", 650, 1.0, 0.05), (0.55, "aa", 660, 1.0, 0.05), (0.62, "uh", 420, 0.9, 0.1), (0.7, "uh", 380, 0.6, 0.12)]
write("04_waah_cry", pad(cry(k, 0.7, seed=4, growl=0.1)))

# 5 "ACK!" very short
k = [(0, "aa", 820, 0.0, 0.2), (0.01, "aa", 840, 1.0, 0.08), (0.16, "aa", 700, 0.9, 0.12)]
x = cry(k, 0.2, seed=5, scream=0.6)
b = np.zeros(int(SR * 0.35)); place(b, burst(0.02, 2000, 5000, 0.004), 0, 0.4 * np.max(np.abs(x))); place(b, x, 0.012)
write("05_ack_short", b)

# 6 "NYAAA" wobbly whimper
k = [(0, "nn", 620, 0.5, 0.05), (0.05, "nn", 640, 0.6, 0.05), (0.09, "aa", 700, 1.0, 0.05), (0.6, "aa", 600, 0.9, 0.07), (0.7, "uh", 560, 0.6, 0.1)]
x = cry(k, 0.7, seed=6, growl=0.05, jitter=0.004)
x *= 1 + 0.35 * np.sin(2 * np.pi * 9 * np.arange(len(x)) / SR)
write("06_nyaa_whimper", pad(x))

# ---------- the same idea, made better for a bot/toy soldier ----------
# 7 Squeak + poof: cry, then the toy soldier pops into smoke
k = [(0, "aa", 760, 0.0, 0.08), (0.015, "aa", 790, 1.0, 0.05), (0.3, "aa", 700, 0.9, 0.07)]
x = cry(k, 0.32, seed=7)
b = np.zeros(int(SR * 0.85)); place(b, x, 0); place(b, pop(), 0.33, 0.9 * np.max(np.abs(x)))
place(b, burst(0.45, 200, 1500, 0.15), 0.36, 0.35 * np.max(np.abs(x)))
write("07_squeak_poof", b)

# 8 Robo squeak: the cry gets bit-crushed and powers down like a little robot
k = [(0, "ee", 820, 0.0, 0.06), (0.015, "ee", 850, 1.0, 0.04), (0.25, "eh", 760, 1.0, 0.05), (0.6, "uh", 260, 0.8, 0.05)]
x = cry(k, 0.6, seed=8, growl=0.0, scream=0.3)
hold = np.clip((np.arange(len(x)) / len(x) * 9).astype(int), 1, 9)
y = x.copy()
for i in range(len(x)):
    y[i] = x[i - i % hold[i]]
y = np.round(y / np.max(np.abs(y)) * 16) / 16
write("08_robo_squeak", pad(y))

# 9 Squeak + zap: an electric shock cry, then sparks
k = [(0, "aa", 700, 0.0, 0.1), (0.01, "aa", 760, 1.0, 0.08), (0.35, "aa", 720, 0.9, 0.1)]
x = cry(k, 0.38, seed=9, scream=0.55)
x *= 1 + 0.6 * np.sign(np.sin(2 * np.pi * 45 * np.arange(len(x)) / SR)) * 0.5
b = np.zeros(int(SR * 0.8)); place(b, x, 0)
for at in (0.38, 0.45, 0.55, 0.62):
    place(b, burst(0.05, 3000, 8000, 0.01), at, 0.5 * np.max(np.abs(x)))
write("09_squeak_zap", b)

# 10 Squeak flying away: cry with pitch drop and echo, as the body is blown back
k = [(0, "aa", 800, 0.0, 0.08), (0.015, "aa", 820, 1.0, 0.05), (0.5, "aa", 520, 0.8, 0.07), (0.6, "uh", 450, 0.5, 0.1)]
x = cry(k, 0.6, seed=10)
x *= np.linspace(1, 0.5, len(x))
b = np.zeros(int(SR * 1.2)); place(b, x, 0)
for d, g in ((0.16, 0.4), (0.32, 0.22), (0.48, 0.12)):
    place(b, x, d, g)
write("10_squeak_flyaway", b)
print("squeaky cries ok")
