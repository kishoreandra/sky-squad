"""Sky Squad sound pack v2: real recordings (Kenney = CC0, Freedoom = BSD licence, credits kept)
cleaned up, brought to 44.1 kHz and layered with extra crack / boom / air layers so they sound
full and modern. Writes options per sound: <sound>__<option>.wav and a list file."""
import os, sys, json, subprocess, wave
import numpy as np
from scipy.signal import butter, lfilter, resample_poly

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
SR = 44100
FD = "/home/claude/snd/freedoom/sounds/"
KF = "/home/claude/kenneynl/starter-kit-fps/sounds/"
KP = "/home/claude/snd/Starter-Kit-3D-Platformer/"
KI = "/home/claude/snd/kenney-interface-sounds/"
KR = "/home/claude/snd/Starter-Kit-Racing/"
rng = np.random.default_rng(23)

def find(base, name):
    for root, _, files in os.walk(base):
        for f in files:
            if f == name:
                return os.path.join(root, f)
    raise FileNotFoundError(base + name)

def load(path):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
    x = np.frombuffer(raw, np.float32).astype(np.float64)
    x = x - np.mean(x[: min(len(x), 2000)])
    return x / (np.max(np.abs(x)) + 1e-9)

def fd(name): return clean(load(FD + name + ".wav"))
def kfps(name): return load(KF + name + ".ogg")

def lp(x, hz, o=2): b, a = butter(o, min(hz, SR / 2 - 200) / (SR / 2), "low"); return lfilter(b, a, x)
def hp(x, hz, o=2): b, a = butter(o, hz / (SR / 2), "high"); return lfilter(b, a, x)
def bp(x, lo, hi, o=2): b, a = butter(o, [lo / (SR / 2), hi / (SR / 2)], "band"); return lfilter(b, a, x)
def t(s): return np.arange(int(SR * s)) / SR
def noise(s): return rng.uniform(-1, 1, int(SR * s))
def env(s, a, d): tt = t(s); return np.minimum(1, tt / max(a, 1e-4)) * np.exp(-tt / d)
def thump(s, f0, f1, d): tt = t(s); return np.sin(2 * np.pi * np.cumsum(f1 + (f0 - f1) * np.exp(-tt * 30)) / SR) * np.exp(-tt / d)

def clean(x):
    """remove 8-bit hiss in the quiet parts and the dull low-res top end"""
    e = np.convolve(np.abs(x), np.ones(441) / 441, mode="same")
    gate = np.clip((e - 0.02) / 0.05, 0, 1)
    x = x * (0.15 + 0.85 * gate)
    return lp(x, 9000, 4)

def excite(x, amt=0.35, hz=3500):
    """adds new bright detail above the old recording's limit (harmonic exciter)"""
    h = hp(x, hz)
    return x + np.tanh(h * 4) * amt

def pitch(x, semis):
    """speed up / slow down (changes pitch and length together, like a sped-up tape)"""
    k = 2 ** (semis / 12)
    up, down = int(round(1000 / k)), 1000
    return resample_poly(x, up, down)

def est_f0(x):
    out = []
    for i in range(0, len(x) - 1300, 660):
        s2 = x[i:i + 1300]; s2 = s2 - s2.mean()
        if np.sqrt((s2 ** 2).mean()) < 0.05: continue
        c = np.correlate(s2, s2, "full")[len(s2) - 1:]; lo, hi = int(SR / 1200), int(SR / 70)
        j = lo + np.argmax(c[lo:hi])
        if c[j] > 0.3 * c[0]: out.append(SR / j)
    return float(np.median(out)) if out else 200.0

def to_pitch(x, target):
    semis = float(np.clip(12 * np.log2(target / est_f0(x)), 3, 15))
    return pitch(x, semis)

def trim(x, sec):
    n = int(SR * sec)
    y = x[:n].copy()
    f = min(len(y), int(SR * 0.01)); y[-f:] *= np.linspace(1, 0, f)
    return y

def mix(*parts):
    n = max(len(p) + int(SR * at) for p, at, g in parts)
    out = np.zeros(n)
    for p, at, g in parts:
        i = int(SR * at); out[i:i + len(p)] += p * g
    return out

def room(x, amt=0.18, size=1.0):
    out = np.concatenate([x, np.zeros(int(SR * 0.25 * size))])
    for dl, g in ((0.021, 0.5), (0.033, 0.42), (0.049, 0.33), (0.071, 0.25), (0.103, 0.18), (0.151, 0.12)):
        i = int(SR * dl * size); out[i:i + len(x)] += x * g * amt * 2
    return out

def comp(x, drive=1.6):
    return np.tanh(x / (np.max(np.abs(x)) + 1e-9) * drive)

LIST = []
def save(sound, option, label, x, gain=0.9):
    x = x / (np.max(np.abs(x)) + 1e-9) * gain
    f = int(SR * 0.006); x[-f:] *= np.linspace(1, 0, f)
    name = f"{sound}__{option}"
    with wave.open(os.path.join(OUT, name + ".wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())
    LIST.append({"sound": sound, "option": option, "label": label, "file": name})

def crack(s=0.05, hz=2500): return hp(noise(s), hz) * env(s, 0.0003, 0.007)

# ================= DEATH CRIES (Mini Militia style: real cry, sped up high, sudden stop) =================
src = {"a": fd("dspldeth"), "b": fd("dspdiehi"), "c": fd("dspodth2"), "d": fd("dspodth3"), "e": fd("dsplpain"), "f": fd("dspopain")}
save("death", "A", "High squeaky cry", trim(excite(to_pitch(src["a"], 680), 0.25), 0.55))
save("death", "B", "Short sharp scream", trim(excite(to_pitch(src["b"], 640), 0.25), 0.5))
save("death", "C", "Growly yelp", trim(excite(to_pitch(src["c"], 600), 0.25), 0.5))
save("death", "D", "Squeak + poof", mix((trim(excite(to_pitch(src["e"], 700), 0.25), 0.4), 0, 1.0),
                                       (lp(noise(0.45), 1500) * env(0.45, 0.01, 0.12), 0.4, 0.35), (crack(0.03, 1500), 0.4, 0.5)))
save("death", "E", "Low crying wail", trim(excite(to_pitch(src["d"], 560), 0.25), 0.6))

# ================= HURT GRUNTS =================
save("hurt", "A", "Quick 'uh!'", trim(excite(to_pitch(fd("dsoof"), 520), 0.2), 0.22))
save("hurt", "B", "Short 'ow'", trim(excite(to_pitch(fd("dsouch"), 520), 0.2), 0.28))
save("hurt", "C", "Squeaky 'eh!'", trim(excite(to_pitch(src["f"], 600), 0.2), 0.22))

# ================= GUNS =================
pistol, shot, dshot, rl, plasma = fd("dspistol"), fd("dsshotgn"), fd("dsdshtgn"), fd("dsrlaunc"), fd("dsplasma")
blaster, rep = kfps("blaster"), kfps("blaster_repeater")
def gun(body, semis, bodylen, crack_hz, sub_f, tail, room_amt, crack_g=0.9, sub_g=0.8):
    b = trim(excite(pitch(body, semis), 0.3), bodylen)
    return room(mix((b, 0, 1.0), (crack(0.05, crack_hz), 0, crack_g), (thump(0.25, sub_f * 2.5, sub_f, 0.06), 0, sub_g),
                    (lp(noise(tail), 1200) * env(tail, 0.002, tail * 0.3), 0, 0.35)), room_amt)
save("magnum", "A", "Heavy pistol", gun(pistol, -3, 0.35, 2500, 75, 0.5, 0.2))
save("magnum", "B", "Big revolver boom", gun(pistol, -5, 0.45, 2000, 60, 0.8, 0.28, sub_g=1.1))
save("uzi", "A", "Light rapid snap", gun(pistol, 3, 0.12, 3500, 110, 0.15, 0.08, sub_g=0.5))
save("uzi", "B", "Buzzy small gun", gun(rep, 0, 0.12, 3000, 120, 0.15, 0.06, sub_g=0.4))
save("ak47", "A", "Punchy rifle", gun(pistol, -1, 0.3, 2200, 70, 0.45, 0.2, sub_g=1.2))
save("ak47", "B", "Rifle with crack", gun(shot, 4, 0.25, 3000, 80, 0.4, 0.18, crack_g=1.2))
save("smg", "A", "Tight SMG", gun(pistol, 2, 0.15, 3200, 100, 0.2, 0.1, sub_g=0.6))
save("smg", "B", "Hollow SMG", gun(dshot, 6, 0.14, 2800, 100, 0.2, 0.1, sub_g=0.6))
save("shotgun", "A", "Real shotgun", gun(shot, 0, 0.8, 1800, 60, 0.9, 0.28, sub_g=1.2))
save("shotgun", "B", "Shotgun + pump", mix((gun(shot, -1, 0.6, 1800, 60, 0.8, 0.25, sub_g=1.2), 0, 1.0), (excite(fd("dssgcock"), 0.3), 0.45, 0.6)))
save("shotgun", "C", "Double-barrel blast", gun(dshot, -2, 0.6, 1800, 55, 0.9, 0.3, sub_g=1.3))
save("sniper", "A", "Sniper crack + echo", mix((gun(pistol, -6, 0.4, 2500, 55, 1.4, 0.45, crack_g=1.5, sub_g=1.2), 0, 1.0), (excite(fd("dssgcock"), 0.3), 0.8, 0.35)))
save("sniper", "B", "Sharp supersonic snap", gun(shot, 3, 0.3, 4000, 70, 1.2, 0.5, crack_g=1.8))
save("minigun", "A", "Minigun burst", mix(*[(gun(pistol, 4, 0.08, 3200, 110, 0.08, 0.05, sub_g=0.5), i * 0.055, 1.0) for i in range(6)]))
save("minigun", "B", "Spin-up whine", mix((lp(np.sin(2 * np.pi * np.cumsum(np.linspace(80, 420, int(SR * 0.5))) / SR) * 0.6 + bp(noise(0.5), 1500, 4000) * 0.2, 2500) * np.linspace(0.2, 1, int(SR * 0.5)), 0, 1.0)))
save("rpg", "A", "Rocket launch whoosh", room(mix((excite(rl, 0.3), 0, 1.0), (thump(0.3, 150, 50, 0.08), 0, 0.8)), 0.2))
save("rpg", "B", "Heavy launch + hiss", room(mix((excite(pitch(rl, -2), 0.3), 0, 1.0), (bp(noise(1.0), 800, 5000) * env(1.0, 0.05, 0.35), 0.05, 0.4), (thump(0.3, 130, 45, 0.1), 0, 1.0)), 0.25))
save("laser", "A", "Energy zap", room(mix((trim(excite(pitch(plasma, 2), 0.4), 0.35), 0, 1.0), (crack(0.03, 4000), 0, 0.5)), 0.15))
save("laser", "B", "Blaster bolt", room(trim(blaster, 0.6), 0.12))
save("shock", "A", "Electric shock", mix((trim(excite(pitch(plasma, -4), 0.5), 0.45), 0, 1.0), (np.sign(np.sin(2 * np.pi * 120 * t(0.4))) * env(0.4, 0.005, 0.15) * 0.25, 0, 1.0)))
save("shock", "B", "Crackling taser", mix(*[(crack(0.03, 3000) * 0.8, i * 0.035 + rng.uniform(0, 0.01), 1.0) for i in range(10)], (trim(excite(plasma, 0.4), 0.3), 0, 0.5)))
save("net", "A", "Net launcher thump", room(mix((thump(0.3, 180, 70, 0.07), 0, 1.0), (trim(excite(fd("dsslop"), 0.3), 0.35), 0.02, 0.7)), 0.15))
save("flame", "A", "Flamethrower roar", trim(excite(fd("dsflame"), 0.3), 0.6))
save("flame", "B", "Fire burst", mix((trim(excite(pitch(fd("dsflamst"), -2), 0.3), 0.6), 0, 1.0), (lp(noise(0.5), 700) * env(0.5, 0.03, 0.2), 0, 0.6)))

# ================= EXPLOSIONS =================
rx, bx, fx = fd("dsrxplod"), fd("dsbarexp"), fd("dsfirxpl")
def boom(body, semis, length, sub_f, sub_g, debris=True):
    b = trim(excite(pitch(body, semis), 0.25), length)
    parts = [(b, 0, 1.0), (thump(1.0, sub_f * 3, sub_f, 0.35), 0, sub_g), (crack(0.08, 1500), 0, 0.8)]
    if debris:
        for i in range(14):
            parts.append((bp(noise(0.05), 1500, 6000) * env(0.05, 0.001, 0.01), rng.uniform(0.15, length * 0.8), 0.25))
    return room(comp(mix(*parts), 1.4), 0.25, 1.4)
save("explosion", "A", "Big blast + debris", boom(rx, -2, 1.8, 45, 1.3))
save("explosion", "B", "Punchy grenade", boom(bx, 0, 1.0, 55, 1.1))
save("explosion", "C", "Fiery boom", boom(fx, -3, 1.2, 50, 1.2, False))
save("timebomb", "A", "Beep beep... BOOM", mix((np.sin(2 * np.pi * 1900 * t(0.07)) * env(0.07, 0.001, 0.03) * 0.5, 0, 1.0),
                                              (np.sin(2 * np.pi * 1900 * t(0.07)) * env(0.07, 0.001, 0.03) * 0.5, 0.15, 1.0),
                                              (boom(rx, -4, 1.8, 40, 1.4), 0.3, 1.0)))

# ================= MOVEMENT =================
flame = fd("dsflame")
def jet(sec, g_flame, g_air, seed):
    r = np.random.default_rng(seed)
    loop = np.tile(lp(flame, 4000), int(sec / (len(flame) / SR)) + 2)[: int(SR * sec)]
    air = lp(r.uniform(-1, 1, int(SR * sec)), 3000, 3) + bp(r.uniform(-1, 1, int(SR * sec)), 3000, 8000) * 0.3
    tt = t(sec)
    sw = np.minimum(1, tt / 0.18) ** 1.4 * np.minimum(1, (sec - tt) / 0.12)
    return (loop * g_flame + air * g_air) * sw * (1 + 0.15 * np.sin(2 * np.pi * 19 * tt))
save("jetpack", "A", "Jet roar (fire + air)", jet(1.4, 0.8, 0.6, 1))
save("jetpack", "B", "Airy thrust", jet(1.4, 0.35, 1.0, 2))
def whoosh(sec, lo, hi, seed):
    tt = t(sec)
    shape = np.sin(np.pi * np.clip(tt / sec, 0, 1)) ** 2
    f = np.linspace(lo, hi, len(tt))
    n = np.random.default_rng(seed).uniform(-1, 1, len(tt))
    out = np.zeros(len(tt))
    for i in range(0, len(tt), 512):   # moving band = real whoosh movement
        seg = n[max(0, i - 1024):i + 512]
        out[i:i + 512] = bp(seg, f[i] * 0.6, f[i] * 1.4)[-len(out[i:i + 512]):]
    return out * shape
save("push", "A", "Fast whoosh", whoosh(0.28, 600, 2000, 3))
save("push", "B", "Swish + cloth", mix((whoosh(0.25, 900, 2600, 4), 0, 1.0), (trim(excite(fd("dsskeswg"), 0.3), 0.3), 0, 0.5)))
save("jump", "A", "Jump", load(find(KP, "jump.ogg")))
save("land", "A", "Land thud", mix((load(KF + "land.ogg"), 0, 1.0), (thump(0.15, 120, 60, 0.04), 0, 0.5)))

# ================= WEAPON HANDLING =================
save("reload", "A", "Mag out, mag in", mix((excite(fd("dsdbopn"), 0.3), 0, 1.0), (excite(fd("dsdbload"), 0.3), 0.3, 1.0), (excite(fd("dsdbcls"), 0.3), 0.6, 1.0)))
save("reload", "B", "Pump rack", excite(fd("dssgcock"), 0.3))
save("swap", "A", "Weapon switch", load(KF + "weapon_change.ogg"))
save("swap", "B", "Metal clack", excite(fd("dswpnup"), 0.3))
save("empty", "A", "Dry click", trim(excite(fd("dsnoway"), 0.3), 0.25))
save("pickup", "A", "Gun pickup", excite(fd("dswpnup"), 0.3))
save("pickup", "B", "Item pickup", excite(fd("dsitemup"), 0.3))
save("health", "A", "Health up", excite(fd("dsgetpow"), 0.3))
save("melee", "A", "Knife slash + hit", mix((whoosh(0.18, 1500, 4000, 6), 0, 0.8), (excite(fd("dspunch"), 0.3), 0.08, 1.0)))
save("melee", "B", "Heavy punch", excite(fd("dspunch"), 0.3))
save("grenade_throw", "A", "Throw swish", trim(excite(fd("dsskeswg"), 0.3), 0.4))
save("bounce", "A", "Grenade tink", excite(fd("dstink"), 0.3))
save("spawn", "A", "Teleport in", trim(excite(fd("dstelept"), 0.3), 1.0))

# ================= MAP / EVENTS / UI =================
save("splash", "A", "Water splash", trim(excite(fd("dsslop"), 0.3), 0.8))
save("crumble", "A", "Ground breaks", load(find(KP, "break.ogg")))
save("hit", "A", "Bullet hits body", mix((excite(fd("dspunch"), 0.2), 0, 0.6), (thump(0.12, 200, 90, 0.03), 0, 0.6)))
save("ui_click", "A", "Button click", load(find(KI, "click_001.wav")))
save("ui_confirm", "A", "Confirm / start", load(find(KI, "confirmation_001.wav")))
save("kill", "A", "Kill confirm ping", load(find(KI, "confirmation_002.wav")))
save("kill", "B", "Glass ding", load(find(KI, "glass_001.wav")))

json.dump(LIST, open(os.path.join(OUT, "list.json"), "w"), indent=0)
print(len(LIST), "clips")
