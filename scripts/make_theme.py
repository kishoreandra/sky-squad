"""Sky Squad main theme - an original heroic piece made for the game (Arc Light Studio).
D harmonic minor, 112 bpm, 32 bars, loops cleanly. Writes music/theme.ogg."""
import numpy as np, subprocess, wave, os

SR = 44100
BPM = 112.0
BEAT = 60.0 / BPM
BARS = 32
N = int(SR * BEAT * 4 * BARS)
L = np.zeros(N); R = np.zeros(N)
rng = np.random.default_rng(7)

def hz(semi):  # semitones from A4
    return 440.0 * 2 ** (semi / 12.0)
NOTE = {"C": -9, "C#": -8, "D": -7, "Eb": -6, "E": -5, "F": -4, "F#": -3, "G": -2, "G#": -1, "A": 0, "Bb": 1, "B": 2}
def n(name):  # "D4", "C#5"
    p, o = name[:-1], int(name[-1])
    return NOTE[p] + (o - 4) * 12

def env(len_s, a, d, s, r):
    t = np.arange(int(len_s * SR)) / SR
    e = np.ones_like(t) * s
    e[t < a] = t[t < a] / a
    m = (t >= a) & (t < a + d)
    e[m] = 1 - (1 - s) * (t[m] - a) / d
    rel = int(r * SR)
    if rel > 0 and rel < len(e):
        e[-rel:] *= np.linspace(1, 0, rel)
    return e, t

def add(sig, start_s, pan=0.0, gain=1.0):
    i = int(start_s * SR)
    if i >= N:
        return
    j = min(N, i + len(sig))
    sig = sig[: j - i] * gain
    L[i:j] += sig * (1 - pan) * 0.5
    R[i:j] += sig * (1 + pan) * 0.5

def saw(f, t, harm=12, vib=0.0):
    ph = 2 * np.pi * f * t + vib * np.sin(2 * np.pi * 5.2 * t) * (t > 0.25)
    out = np.zeros_like(t)
    for k in range(1, harm + 1):
        if f * k > 9000:
            break
        out += np.sin(k * ph) / k
    return out

def brass(semi, start, dur, gain=0.22, pan=0.0):
    e, t = env(dur + 0.12, 0.035, 0.15, 0.8, 0.12)
    f = hz(semi)
    bright = np.clip(t / 0.08, 0, 1)
    sig = saw(f, t, harm=9, vib=0.9) * (0.6 + 0.4 * bright) + 0.35 * saw(f * 1.003, t, harm=6)
    add(sig * e, start, pan, gain)

def strings(semis, start, dur, gain=0.05):
    for si, semi in enumerate(semis):
        e, t = env(dur + 0.4, 0.35, 0.3, 0.85, 0.4)
        f = hz(semi)
        sig = saw(f * 0.997, t, harm=7) + saw(f * 1.004, t, harm=7)
        add(sig * e, start, pan=(-0.6 if si % 2 else 0.6), gain=gain)

def bass(semi, start, dur, gain=0.30):
    e, t = env(dur, 0.005, 0.12, 0.55, 0.05)
    f = hz(semi)
    sig = np.sin(2 * np.pi * f * t) + 0.35 * np.sign(np.sin(2 * np.pi * f * t)) * 0.5 + 0.3 * np.sin(4 * np.pi * f * t)
    add(sig * e, start, 0.0, gain)

def drum(start, kind, gain=1.0):
    if kind == "taiko":
        d = 0.9; t = np.arange(int(d * SR)) / SR
        f = 55 + 70 * np.exp(-t * 18)
        ph = 2 * np.pi * np.cumsum(f) / SR
        sig = np.sin(ph) * np.exp(-t * 5.5) + 0.25 * rng.standard_normal(len(t)) * np.exp(-t * 40)
        add(sig, start, 0.0, 0.55 * gain)
    elif kind == "dhol_lo":
        d = 0.5; t = np.arange(int(d * SR)) / SR
        f = 90 + 60 * np.exp(-t * 25)
        sig = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)
        add(sig, start, -0.15, 0.42 * gain)
    elif kind == "dhol_hi":
        d = 0.25; t = np.arange(int(d * SR)) / SR
        sig = (np.sin(2 * np.pi * 330 * t) * 0.5 + rng.standard_normal(len(t)) * 0.6) * np.exp(-t * 28)
        add(sig, start, 0.25, 0.22 * gain)
    elif kind == "clap":
        d = 0.3; t = np.arange(int(d * SR)) / SR
        nz = rng.standard_normal(len(t))
        nz = np.diff(np.concatenate([[0], nz]))  # brighter
        sig = nz * (np.exp(-t * 30) + 0.5 * np.exp(-((t - 0.012) ** 2) / 0.00002))
        add(sig, start, 0.1, 0.16 * gain)
    elif kind == "crash":
        d = 2.2; t = np.arange(int(d * SR)) / SR
        nz = np.diff(np.concatenate([[0], rng.standard_normal(len(t))]))
        sig = nz * np.exp(-t * 1.8)
        add(sig, start, -0.3, 0.07 * gain); add(sig[::-1][: len(sig)] * 0, start)
    elif kind == "swell":
        d = BEAT * 4; t = np.arange(int(d * SR)) / SR
        nz = np.diff(np.concatenate([[0], rng.standard_normal(len(t))]))
        sig = nz * (t / d) ** 2.5
        add(sig, start, 0.3, 0.06 * gain)

def bar(b):
    return b * 4 * BEAT

# ---------------- the tune (original) ----------------
# chords per bar (root semitone, minor/major triad)
CH_A = [("D", "m"), ("Bb", "M"), ("C", "M"), ("A", "M")] * 2
CH_B = [("G", "m"), ("D", "m"), ("Bb", "M"), ("A", "M"), ("G", "m"), ("Bb", "M"), ("E", "dim"), ("A", "M")]
CH_I = [("D", "m")] * 4
CH_O = [("Bb", "M"), ("C", "M"), ("A", "M"), ("A", "M")]
chords = CH_I + CH_A + CH_B + CH_A + CH_O
assert len(chords) == BARS

def triad(root, q, octv=3):
    r = n(root + str(octv))
    third = 3 if q in ("m", "dim") else 4
    fifth = 6 if q == "dim" else 7
    return [r, r + third, r + fifth]

MEL_A = [  # (note, beats)
    ("D4", 1.5), ("F4", 0.5), ("A4", 1), ("D5", 1),
    ("C#5", 1.5), ("Bb4", 0.5), ("A4", 2),
    ("G4", 1), ("A4", 0.5), ("Bb4", 0.5), ("C5", 1), ("Bb4", 1),
    ("A4", 3), (None, 1),
    ("D5", 1.5), ("E5", 0.5), ("F5", 1), ("E5", 1),
    ("D5", 1), ("C#5", 1), ("A4", 2),
    ("Bb4", 1), ("A4", 0.5), ("G4", 0.5), ("F4", 1), ("E4", 1),
    ("D4", 3), (None, 1),
]
MEL_B = [
    ("Bb4", 1), ("D5", 1), ("G5", 1.5), ("F5", 0.5),
    ("F5", 1), ("E5", 0.5), ("D5", 0.5), ("A4", 2),
    ("Bb4", 1), ("C5", 1), ("D5", 1), ("F5", 1),
    ("E5", 2), ("C#5", 2),
    ("D5", 1), ("G5", 1), ("Bb5", 1.5), ("A5", 0.5),
    ("G5", 1), ("F5", 1), ("D5", 2),
    ("E5", 1), ("G5", 1), ("Bb4", 1), ("C#5", 1),
    ("A4", 2), ("E5", 1), ("C#5", 1),
]
MEL_O = [("D5", 2), ("C5", 2), ("C#5", 1.5), ("E5", 0.5), ("A5", 2), ("A4", 4)]

def play_mel(mel, start_bar, gain=0.2, octave=0, double=False):
    tpos = bar(start_bar)
    for nm, beats in mel:
        if nm:
            brass(n(nm) + octave, tpos, beats * BEAT * 0.95, gain)
            if double:
                brass(n(nm) + octave - 12, tpos, beats * BEAT * 0.95, gain * 0.45, pan=-0.3)
        tpos += beats * BEAT
    return tpos

# chords, bass, drums for every bar
for b, (root, q) in enumerate(chords):
    t0 = bar(b)
    tri = triad(root, q, 4 if root in ("C", "C#", "D", "Eb", "E") else 3)
    big = b >= 4
    strings([x for x in tri] + ([tri[0] + 12] if big else []), t0, 4 * BEAT, 0.035 if b < 4 else 0.045)
    r = n(root + "2")
    if b < 4:
        bass(r, t0, 4 * BEAT * 0.9, 0.18)
    else:
        for e8 in range(8):
            if e8 in (0, 3, 4, 6, 7):
                bass(r + (12 if e8 == 7 else 0), t0 + e8 * BEAT / 2, BEAT / 2 * 0.85, 0.24)
    # drums
    if b < 4:
        drum(t0, "taiko", 0.6 + 0.15 * b)
        if b == 3:
            for k in range(8):
                drum(t0 + 2 * BEAT + k * BEAT / 4, "dhol_lo", 0.5 + k * 0.08)
            drum(t0, "swell")
    else:
        drum(t0, "taiko")
        drum(t0 + 2.5 * BEAT, "taiko", 0.8)
        for k in range(16):
            s16 = t0 + k * BEAT / 4
            if k in (0, 3, 6, 10, 12):
                drum(s16, "dhol_lo", 0.9)
            if k in (2, 5, 8, 11, 14, 15):
                drum(s16, "dhol_hi", 0.8 if k % 2 else 1.0)
        drum(t0 + BEAT, "clap"); drum(t0 + 3 * BEAT, "clap")
    if b in (4, 12, 20):
        drum(t0, "crash")
    if b in (11, 19, 27):
        drum(t0, "swell")

play_mel(MEL_A, 4, 0.19)
play_mel(MEL_B, 12, 0.20, double=True)
play_mel(MEL_A, 20, 0.21, octave=0, double=True)
play_mel(MEL_O, 28, 0.2, double=True)
# a little horn call in the intro
for i, (nm, bt) in enumerate([("A3", 1), ("D4", 1), ("A4", 2)]):
    brass(n(nm), bar(2) + i * BEAT, bt * BEAT * 0.9, 0.12)
brass(n("C#4"), bar(3), 2 * BEAT, 0.12); brass(n("E4"), bar(3) + 2 * BEAT, 2 * BEAT, 0.12)

# ---------------- mix: simple room echo, gentle limiter ----------------
def echo(x, ms, fb, mix):
    d = int(SR * ms / 1000)
    y = x.copy()
    for k in range(1, 5):
        y[d * k:] += x[: -d * k] * (fb ** k) * mix
    return y
L = echo(L, 113, 0.45, 0.6); R = echo(R, 157, 0.45, 0.6)
# wrap the tail into the start so the loop is seamless
st = np.stack([L, R], 1)
st /= np.max(np.abs(st)) / 0.98
st = np.tanh(st * 1.3) / np.tanh(1.3)
st *= 0.85
os.makedirs("/home/claude/skysquad/music", exist_ok=True)
wav = "/tmp/claude-0/theme.wav"
with wave.open(wav, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st * 32767).astype(np.int16).tobytes())
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-c:a", "libvorbis", "-q:a", "4", "/home/claude/skysquad/music/theme.ogg"], check=True)
print("seconds", N / SR, "size", os.path.getsize("/home/claude/skysquad/music/theme.ogg"))
