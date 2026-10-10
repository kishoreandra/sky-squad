"""Generate Sky Squad v0.2 art with PIL (supersampled for smooth edges).
Writes PNGs into <project>/art and art/meta.gd with gun anchor points."""
import os, sys, math, random, json
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

OUT = os.path.join(sys.argv[1], "art")
os.makedirs(OUT, exist_ok=True)
SS = 4            # supersample factor
OUTLINE = (27, 29, 42, 255)
random.seed(7)
np.random.seed(7)

def canvas(w, h):
    im = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)

def save(im, name, w, h):
    im = im.resize((w, h), Image.LANCZOS)
    im.save(os.path.join(OUT, name + ".png"))
    return im

def sc(pts, k):
    return [(x * k, y * k) for x, y in pts]

def shade(c, f):
    return tuple(max(0, min(255, int(v * f))) for v in c[:3]) + (255,)

def hexc(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (255,)

# ---------------- characters ----------------
# texture scale: 3 tex px per world px
CS = 3
K = CS * SS  # drawing units per world px
TEAM = {
    "yellow": "#f2c230", "blue": "#3fa9f5", "red": "#e8553f",
    "purple": "#9b6bea", "green": "#5cc45a", "orange": "#f08a24",
}
SKIN = hexc("#f1c08f")
SKIN_D = hexc("#d79a68")

def head(team, name):
    W = H = 26
    im, d = canvas(W * CS, H * CS)
    c = hexc(team)
    cx, cy = 13 * K, 14 * K
    r = 10 * K
    ow = int(1.2 * K)
    # face
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SKIN, outline=OUTLINE, width=ow)
    # cheek shadow
    d.pieslice([cx - r + ow, cy - r + ow, cx + r - ow, cy + r - ow], 100, 200, fill=SKIN_D)
    # helmet dome
    hr = 11 * K
    d.chord([cx - hr, cy - hr - 1.5 * K, cx + hr, cy + hr - 1.5 * K], 180, 360, fill=c, outline=OUTLINE, width=ow)
    d.rectangle([cx - hr, cy - 2.2 * K, cx + hr, cy - 0.6 * K], fill=shade(c, 0.72), outline=OUTLINE, width=ow)
    # brim forward
    d.polygon(sc([(13 + 6, 12.4), (13 + 13.5, 12.6), (13 + 12.5, 14), (13 + 6, 14)], K), fill=shade(c, 0.6), outline=OUTLINE)
    # helmet highlight
    d.arc([cx - 8 * K, cy - 10 * K, cx + 4 * K, cy - 1 * K], 200, 260, fill=(255, 255, 255, 140), width=int(1.4 * K))
    # helmet camo dots
    for (dx, dy) in [(-5, -6), (1, -8), (5, -5), (-2, -4)]:
        d.ellipse([cx + (dx - 1.2) * K, cy + (dy - 1) * K, cx + (dx + 1.2) * K, cy + (dy + 1) * K], fill=shade(c, 0.82))
    # goggles strap & lens
    d.rounded_rectangle([cx + 2 * K, cy - 0.2 * K, cx + 9.8 * K, cy + 4.2 * K], radius=1.6 * K, fill=(30, 34, 52, 255), outline=OUTLINE, width=ow)
    d.rounded_rectangle([cx + 3.2 * K, cy + 0.8 * K, cx + 9 * K, cy + 3.3 * K], radius=1 * K, fill=(120, 220, 255, 255))
    d.line([cx + 4 * K, cy + 1.4 * K, cx + 6 * K, cy + 1.4 * K], fill=(255, 255, 255, 220), width=int(0.8 * K))
    # mouth
    d.line([cx + 4.5 * K, cy + 7 * K, cx + 7.5 * K, cy + 6.6 * K], fill=(110, 50, 40, 255), width=int(0.9 * K))
    # chin strap
    d.arc([cx - 9 * K, cy - 9 * K, cx + 9 * K, cy + 9.6 * K], 95, 150, fill=(40, 40, 50, 255), width=int(1.0 * K))
    save(im, name, W * CS, H * CS)

def torso(team, name):
    W, H = 20, 20
    im, d = canvas(W * CS, H * CS)
    c = hexc(team)
    ow = int(1.2 * K)
    # body base (shirt)
    d.rounded_rectangle(sc([(3, 1), (17, 18)], K), radius=4 * K, fill=shade(c, 0.85), outline=OUTLINE, width=ow)
    # vest
    d.rounded_rectangle(sc([(4.2, 3.5), (16, 15.5)], K), radius=3 * K, fill=hexc("#4e5a3a"), outline=OUTLINE, width=int(0.9 * K))
    for px in (6, 11.2):
        d.rounded_rectangle(sc([(px, 7), (px + 3.6, 11.4)], K), radius=0.8 * K, fill=hexc("#5f6d47"), outline=OUTLINE, width=int(0.7 * K))
    # belt
    d.rectangle(sc([(3.4, 14.6), (16.6, 16.6)], K), fill=hexc("#5a3b22"), outline=OUTLINE, width=int(0.7 * K))
    d.rectangle(sc([(9.2, 14.4), (11.4, 16.8)], K), fill=hexc("#c9a640"))
    # collar
    d.polygon(sc([(7, 1.3), (13, 1.3), (10, 4.5)], K), fill=shade(c, 0.65))
    save(im, name, W * CS, H * CS)

def leg(name):
    W, H = 9, 17
    im, d = canvas(W * CS, H * CS)
    ow = int(1.0 * K)
    d.rounded_rectangle(sc([(1.5, 0.5), (7, 12.5)], K), radius=2.2 * K, fill=hexc("#4a4f39"), outline=OUTLINE, width=ow)
    d.line(sc([(4.2, 3), (4.2, 10)], K), fill=hexc("#3b3f2d"), width=int(0.8 * K))
    # boot
    d.rounded_rectangle(sc([(1, 11.5), (8.6, 16.2)], K), radius=1.6 * K, fill=hexc("#2a2523"), outline=OUTLINE, width=ow)
    d.rectangle(sc([(1.4, 15), (8.4, 16)], K), fill=hexc("#151213"))
    save(im, name, W * CS, H * CS)

def jetpack(name):
    W, H = 14, 22
    im, d = canvas(W * CS, H * CS)
    ow = int(1.0 * K)
    for x0 in (1, 7):
        d.rounded_rectangle(sc([(x0, 1), (x0 + 6, 17)], K), radius=3 * K, fill=hexc("#8a96a8"), outline=OUTLINE, width=ow)
        d.rounded_rectangle(sc([(x0 + 1, 2.5), (x0 + 2.4, 14.5)], K), radius=0.7 * K, fill=(230, 236, 245, 200))
        d.polygon(sc([(x0 + 1.2, 17), (x0 + 4.8, 17), (x0 + 5.6, 21), (x0 + 0.4, 21)], K), fill=hexc("#3c4250"), outline=OUTLINE)
    d.rectangle(sc([(2, 7), (12, 9)], K), fill=hexc("#c0392b"), outline=OUTLINE, width=int(0.6 * K))
    save(im, name, W * CS, H * CS)

def hand(name):
    W = H = 6
    im, d = canvas(W * CS, H * CS)
    d.ellipse(sc([(0.6, 0.6), (5.4, 5.4)], K), fill=SKIN, outline=OUTLINE, width=int(0.9 * K))
    save(im, name, W * CS, H * CS)

for tname, tcol in TEAM.items():
    head(tcol, "head_" + tname)
    torso(tcol, "torso_" + tname)
leg("leg")
jetpack("jetpack")
hand("hand")

# ---------------- guns ----------------
GS = 3
GK = GS * SS
META = {}
METAL = hexc("#3a3f4b")
METAL_L = hexc("#5d6474")
METAL_D = hexc("#22252d")
WOOD = hexc("#9a5b2e")
WOOD_L = hexc("#b9763f")
OLIVE = hexc("#5d6b3a")

def gun_canvas(w, h):
    return canvas(w * GS, h * GS)

def P(d, pts, fill, w=1.0):
    d.polygon(sc(pts, GK), fill=fill, outline=OUTLINE, width=int(w * GK))

def R(d, x0, y0, x1, y1, fill, r=0.6, w=0.9):
    d.rounded_rectangle(sc([(x0, y0), (x1, y1)], GK), radius=r * GK, fill=fill, outline=OUTLINE, width=int(w * GK))

def L(d, pts, fill, w):
    d.line(sc(pts, GK), fill=fill, width=int(w * GK))

def gun_shade(im):
    a = np.array(im).astype(np.float32)
    h = a.shape[0]
    grad = np.linspace(1.22, 0.74, h)[:, None]
    a[..., :3] *= grad[..., None]
    # rim light on top edges: opaque pixel whose pixel a few rows above is transparent
    k = max(2, SS * 2)
    alpha = a[..., 3]
    top = np.zeros_like(alpha, dtype=bool)
    top[k:] = (alpha[k:] > 200) & (alpha[:-k] < 40)
    rim = np.zeros_like(top)
    for dy in range(k, int(k * 1.8)):
        rim[dy:] |= top[:-dy] & (alpha[dy:] > 200)
    a[rim, :3] = a[rim, :3] * 0.8 + 255 * 0.2
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGBA")

def gun_save(im, name, W, H, grip, muzzle, front, length):
    im = gun_shade(im)
    save(im, "gun_" + name, W * GS, H * GS)
    META[name] = {"size": [W, H], "grip": grip, "muzzle": muzzle, "front": front, "len": length}

# Magnum / heavy pistol (W 24 x H 14), grip at (6,9)
im, d = gun_canvas(24, 14)
P(d, [(3.5, 6.5), (9, 6.5), (7.4, 13.2), (2.4, 13.2)], hexc("#2b2b30"))
L(d, [(3.5, 9), (7.2, 9)], hexc("#45454c"), 0.6); L(d, [(3.2, 10.6), (6.8, 10.6)], hexc("#45454c"), 0.6)
R(d, 8, 7, 12, 10.5, (0, 0, 0, 0), 1.2, 0.9)
R(d, 2, 3, 22.6, 7.2, hexc("#9aa3b2"), 0.8)
d.rectangle(sc([(9, 3.8), (21.8, 4.6)], GK), fill=hexc("#c7cfdb"))
for x in (3.2, 4.4, 5.6):
    L(d, [(x, 3.6), (x, 6.6)], hexc("#6b7382"), 0.4)
R(d, 20.5, 2.2, 21.8, 3.2, METAL_D, 0.2, 0.4)
d.rectangle(sc([(8.5, 6.2), (22, 7.2)], GK), fill=hexc("#6b7382"))
gun_save(im, "magnum", 24, 14, [6, 9], [22.8, 5], [11, 8], 17)

# Uzi (W 26 x H 18), grip at (9,11)
im, d = gun_canvas(26, 18)
R(d, 7.4, 8, 11.4, 17.4, METAL_D, 0.8)            # magazine through grip
R(d, 3, 3.5, 21, 9.2, METAL, 1.0)                    # body
d.rectangle(sc([(4, 4.4), (20, 5.2)], GK), fill=METAL_L)
R(d, 21, 5, 25.4, 7.2, METAL_D, 0.4, 0.7)            # barrel
L(d, [(3, 6.5), (0.5, 6.5), (0.5, 9.5), (3, 9.5)], METAL_D, 0.9)   # folded stock
R(d, 12, 8.6, 16, 11.4, (0, 0, 0, 0), 1, 0.8)
R(d, 14.5, 2.2, 16, 3.8, METAL_D, 0.3, 0.5)
for x in (13, 15, 17, 19):
    L(d, [(x, 7.2), (x, 8.6)], METAL_D, 0.5)
gun_save(im, "uzi", 26, 18, [9.4, 11], [25.4, 6.1], [18, 8.2], 19)

# AK-47 (W 46 x H 18), grip at (14,11)
im, d = gun_canvas(46, 18)
P(d, [(0.6, 6), (9.5, 5.5), (10.5, 9), (2.5, 12.8), (0.6, 12.6)], WOOD)       # stock
L(d, [(1.8, 7.5), (8.5, 7)], WOOD_L, 0.6)
P(d, [(11.4, 8.2), (15, 8.2), (14, 14.4), (10.8, 14.4)], hexc("#7a4524"))        # pistol grip
P(d, [(17.5, 8.4), (22, 8.4), (24.4, 16.6), (21.4, 17.4), (19.6, 13)], hexc("#a0522d"))   # banana mag
L(d, [(19.6, 10), (22, 15)], hexc("#c0663a"), 0.6)
R(d, 9, 4.2, 26, 9, METAL, 0.6)                                                  # receiver
d.rectangle(sc([(10, 5), (25, 5.8)], GK), fill=METAL_L)
R(d, 26, 5.2, 35, 8.8, WOOD, 0.8)                                                # handguard
L(d, [(27, 6.2), (34, 6.2)], WOOD_L, 0.5)
R(d, 25, 3.2, 34, 4.8, METAL_D, 0.4, 0.6)                                        # gas tube
R(d, 35, 5.6, 44, 7.4, METAL_D, 0.3, 0.7)                                        # barrel
R(d, 43, 5, 45.4, 8, METAL, 0.3, 0.6)                                            # muzzle
P(d, [(39, 5.6), (40.2, 2.8), (41, 2.8), (41.2, 5.6)], METAL_D, 0.5)            # front sight
R(d, 15.5, 8.6, 18.5, 11, (0, 0, 0, 0), 1, 0.7)
for x in (12, 14, 22, 24):                                                      # rivets
    d.ellipse(sc([(x - 0.45, 6.6), (x + 0.45, 7.5)], GK), fill=METAL_L)
for t_ in (0.3, 0.5, 0.7):                                                      # magazine ribs
    L(d, [(18.2 + 3.6 * t_, 9 + 6.5 * t_), (21.2 + 2.4 * t_, 8.8 + 6.8 * t_)], hexc("#7e3f22"), 0.45)
R(d, 11, 2.8, 13.2, 4.4, METAL_D, 0.3, 0.5)                                     # rear sight
P(d, [(43, 4.6), (45.8, 5.2), (45.8, 7.8), (43, 8.4)], hexc("#2b2e36"), 0.6)    # slanted muzzle brake
for x in (28, 30, 32):                                                          # handguard grip lines
    L(d, [(x, 7.6), (x + 1.2, 7.6)], hexc("#6e3d1d"), 0.5)
gun_save(im, "ak47", 46, 18, [13.2, 11], [45.4, 6.5], [30, 7.4], 31)

# Pump shotgun (W 44 x H 15), grip at (12,10)
im, d = gun_canvas(44, 15)
P(d, [(0.5, 4.8), (9.5, 4.5), (11.5, 8.8), (2, 12), (0.5, 11.6)], WOOD)
L(d, [(1.5, 6.4), (9, 6)], WOOD_L, 0.6)
P(d, [(9.5, 7.5), (13, 7.5), (12.8, 12.6), (10, 12.6)], hexc("#7a4524"))
R(d, 9.6, 3.6, 19, 8, hexc("#2c2f37"), 0.6)
R(d, 19, 3.8, 43.4, 5.8, METAL_D, 0.4, 0.7)      # barrel
R(d, 19, 6, 36, 7.8, METAL, 0.4, 0.6)            # tube mag
R(d, 23, 5.4, 32, 9.4, WOOD, 1.2)                # pump
for x in (25, 27, 29):
    L(d, [(x, 6), (x, 8.8)], hexc("#6e3d1d"), 0.5)
R(d, 13, 7.6, 16.5, 10, (0, 0, 0, 0), 1, 0.7)
R(d, 41.6, 3, 42.6, 3.8, METAL_L, 0.2, 0.4)
gun_save(im, "shotgun", 44, 15, [11.6, 10], [43.4, 4.8], [27.5, 7.4], 31)

# Sniper (W 58 x H 18), grip at (15,12)
im, d = gun_canvas(58, 18)
P(d, [(0.5, 6.5), (11, 6.5), (12.5, 9.5), (3.5, 13.5), (0.5, 13.2)], OLIVE)     # stock
P(d, [(3, 6.5), (9, 6.5), (8.5, 5), (4, 5)], hexc("#4d5930"))                   # cheek rest
P(d, [(12.2, 9), (16, 9), (15, 15), (11.6, 15)], hexc("#2a2c26"))
R(d, 11, 6.2, 27, 10, hexc("#3b4128"), 0.6)                                       # body
R(d, 18.6, 9.6, 22, 13.4, METAL_D, 0.5, 0.7)                                      # mag
R(d, 27, 7, 56.6, 8.6, METAL_D, 0.3, 0.7)                                         # barrel
R(d, 54, 6.4, 57.6, 9.2, METAL, 0.3, 0.6)                                         # muzzle brake
R(d, 14, 1.4, 28, 4.6, hexc("#1f2126"), 1.4)                                      # scope
R(d, 12.4, 1, 14.4, 5, hexc("#2c2f37"), 0.6, 0.6)
R(d, 27.6, 0.6, 30, 5.4, hexc("#2c2f37"), 0.6, 0.6)
d.ellipse(sc([(28.2, 1.6), (29.6, 4.4)], GK), fill=(120, 220, 255, 255))
R(d, 17, 4.4, 18.6, 6.4, METAL_D, 0.2, 0.5); R(d, 23, 4.4, 24.6, 6.4, METAL_D, 0.2, 0.5)
L(d, [(36, 8.6), (42, 10.5)], METAL_D, 0.8)                                      # bipod folded
R(d, 16, 9.4, 19, 12, (0, 0, 0, 0), 1, 0.7)
gun_save(im, "sniper", 58, 18, [14.2, 12], [57.6, 7.8], [34, 8.4], 42)

# RPG (W 50 x H 18), grip at (16,12)
im, d = gun_canvas(50, 18)
R(d, 2, 5, 38, 9.4, hexc("#55642f"), 1.6)                       # tube
d.rectangle(sc([(4, 5.8), (36, 6.6)], GK), fill=hexc("#7b8a48"))
R(d, 0.4, 4.4, 4, 10, METAL_D, 0.8, 0.7)                         # rear flare
P(d, [(38, 4), (43, 3.4), (49.4, 7.2), (43, 11), (38, 10.4)], hexc("#6d7a3c"))   # warhead
L(d, [(41, 4.6), (41, 9.8)], hexc("#4c5628"), 0.7)
P(d, [(14, 9.2), (18, 9.2), (17, 15.6), (13.6, 15.6)], hexc("#2a2c26"))
P(d, [(24, 9.2), (27, 9.2), (26.4, 14), (23.6, 14)], hexc("#2a2c26"))
R(d, 19, 1.6, 23, 5, METAL_D, 0.5, 0.6)                          # sight
gun_save(im, "rpg", 50, 18, [15.8, 12], [49.4, 7.2], [25.4, 11], 33)

# ---------------- items ----------------
im, d = canvas(12 * GS, 14 * GS)
d.ellipse(sc([(1.2, 3.4), (10.8, 13.4)], GK), fill=hexc("#5a6b34"), outline=OUTLINE, width=int(0.9 * GK))
for y in (6.6, 9.6):
    d.line(sc([(1.8, y), (10.2, y)], GK), fill=hexc("#45532a"), width=int(0.6 * GK))
d.line(sc([(5.6, 3.6), (5.6, 13)], GK), fill=hexc("#45532a"), width=int(0.6 * GK))
d.rounded_rectangle(sc([(4, 1.4), (8, 4)], GK), radius=0.4 * GK, fill=METAL_L, outline=OUTLINE, width=int(0.6 * GK))
d.ellipse(sc([(7.4, 0.2), (10.4, 3)], GK), outline=hexc("#c9a640"), width=int(0.7 * GK))
d.line(sc([(8, 2), (11, 8)], GK), fill=METAL_L, width=int(0.9 * GK))
save(im, "grenade", 12 * GS, 14 * GS)

im, d = canvas(22 * GS, 18 * GS)
d.rounded_rectangle(sc([(1, 4), (21, 17)], GK), radius=2 * GK, fill=hexc("#f3f3f5"), outline=OUTLINE, width=int(1 * GK))
d.rounded_rectangle(sc([(7.5, 1), (14.5, 5)], GK), radius=1 * GK, outline=OUTLINE, width=int(1 * GK))
d.rectangle(sc([(9.6, 6.5), (12.4, 15)], GK), fill=hexc("#e03a3e"))
d.rectangle(sc([(6.8, 9.3), (15.2, 12.1)], GK), fill=hexc("#e03a3e"))
d.rectangle(sc([(1.6, 14.4), (20.4, 16.4)], GK), fill=hexc("#d8d8de"))
save(im, "medkit", 22 * GS, 18 * GS)

# ---------------- tiles (64 px = 32 world) ----------------
TP = 64
def noise_tex(base, var, speck, seed, size=TP):
    rng = np.random.default_rng(seed)
    n = rng.normal(0, 1, (size // 4, size // 4))
    n = np.kron(n, np.ones((4, 4)))
    n = (n + np.roll(n, 1, 0) + np.roll(n, 1, 1) + np.roll(n, -1, 0)) / 4
    fine = rng.normal(0, 1, (size, size)) * 0.35
    v = n + fine
    arr = np.zeros((size, size, 4), np.uint8)
    for i in range(3):
        arr[..., i] = np.clip(base[i] + v * var, 0, 255)
    arr[..., 3] = 255
    im = Image.fromarray(arr, "RGBA")
    d = ImageDraw.Draw(im)
    rr = random.Random(seed)
    for _ in range(speck):
        x, y, r = rr.uniform(2, size - 2), rr.uniform(2, size - 2), rr.uniform(1.4, 3.4)
        col = rr.choice([(118, 82, 52), (160, 122, 84), (96, 66, 42)])
        d.ellipse([x - r, y - r * 0.8, x + r, y + r * 0.8], fill=col + (255,))
        d.arc([x - r, y - r * 0.8, x + r, y + r * 0.8], 200, 320, fill=(196, 160, 118, 255))
    return im

for i in range(3):
    noise_tex((126, 84, 50), 14, 4, 11 + i).save(os.path.join(OUT, f"dirt{i}.png"))

# grass cap: 32x16 world -> 64x32, blades rise above top
im, d = canvas(TP, 32)
k = SS
d.rectangle([0, 10 * k, TP * k, 22 * k], fill=hexc("#5aa83a"))
d.rectangle([0, 19 * k, TP * k, 23 * k], fill=hexc("#3f7f2a"))
rr = random.Random(3)
for _ in range(70):
    x = rr.uniform(0, TP)
    h = rr.uniform(4, 11)
    col = rr.choice([hexc("#6cc24a"), hexc("#5aa83a"), hexc("#7fd35a")])
    d.polygon([((x - 1.6) * k, 12 * k), ((x + 1.6) * k, 12 * k), ((x + rr.uniform(-2, 2)) * k, (12 - h) * k)], fill=col)
for _ in range(10):
    x = rr.uniform(2, TP - 2)
    d.line([x * k, 18 * k, (x + 3) * k, 20 * k], fill=hexc("#8a5a33"), width=k)
im.resize((TP, 32), Image.LANCZOS).save(os.path.join(OUT, "grass.png"))

# rock / stone blocks
im = noise_tex((112, 116, 124), 10, 0, 50)
d = ImageDraw.Draw(im)
for (x0, y0, x1, y1) in [(0, 0, 38, 30), (38, 0, 64, 30), (0, 30, 22, 64), (22, 30, 64, 64)]:
    d.rectangle([x0 + 1, y0 + 1, x1 - 2, y1 - 2], outline=(78, 82, 92, 255), width=2)
    d.line([x0 + 3, y0 + 3, x1 - 4, y0 + 3], fill=(150, 155, 165, 255), width=2)
im.save(os.path.join(OUT, "rock.png"))

# wood planks
im = Image.new("RGBA", (TP, TP), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
for i, y in enumerate((0, 21, 42)):
    base = [(150, 96, 52), (138, 88, 47), (158, 104, 58)][i]
    d.rectangle([0, y, TP - 1, y + 20], fill=base + (255,), outline=(70, 44, 24, 255), width=2)
    for gx in range(4):
        gy = y + 5 + gx * 4
        d.line([4, gy, TP - 5, gy + random.uniform(-1, 1)], fill=tuple(int(c * 0.86) for c in base) + (255,), width=1)
    for nx in (6, TP - 7):
        d.ellipse([nx - 2, y + 8, nx + 2, y + 12], fill=(60, 60, 66, 255))
im.save(os.path.join(OUT, "wood.png"))

# crate
im, d = canvas(TP, TP)
k = SS
d.rectangle([2 * k, 2 * k, 62 * k, 62 * k], fill=hexc("#b07a42"), outline=hexc("#5a3a1d"), width=4 * k)
for y in (20, 40):
    d.line([4 * k, y * k, 60 * k, y * k], fill=hexc("#8a5a2e"), width=2 * k)
d.line([6 * k, 6 * k, 58 * k, 58 * k], fill=hexc("#7a4e26"), width=7 * k)
d.line([6 * k, 6 * k, 58 * k, 58 * k], fill=hexc("#c58c50"), width=4 * k)
d.rectangle([2 * k, 2 * k, 62 * k, 62 * k], outline=hexc("#5a3a1d"), width=4 * k)
for (x, y) in [(7, 7), (57, 7), (7, 57), (57, 57)]:
    d.ellipse([(x - 2) * k, (y - 2) * k, (x + 2) * k, (y + 2) * k], fill=hexc("#3a3a40"))
im.resize((TP, TP), Image.LANCZOS).save(os.path.join(OUT, "crate.png"))

# cracks
for stage in (1, 2):
    im, d = canvas(TP, TP)
    k = SS
    rr = random.Random(stage * 9)
    lines = 2 if stage == 1 else 5
    for _ in range(lines):
        x, y = rr.uniform(16, 48), rr.uniform(16, 48)
        pts = [(x, y)]
        for _ in range(4):
            x += rr.uniform(-10, 10); y += rr.uniform(-10, 10)
            pts.append((x, y))
        d.line([(a * k, b * k) for a, b in pts], fill=(30, 18, 10, 210), width=int(2.2 * k), joint="curve")
    im.resize((TP, TP), Image.LANCZOS).save(os.path.join(OUT, f"crack{stage}.png"))

# ---------------- background ----------------
def ridge(w, h, base_y, amp, octaves, seed):
    rng = np.random.default_rng(seed)
    xs = np.arange(w)
    y = np.full(w, float(base_y))
    for o in range(octaves):
        f = (o + 1) * 2
        ph = rng.uniform(0, 6.28)
        y -= amp / (o + 1) * (0.5 + 0.5 * np.sin(xs / w * 2 * np.pi * f + ph))
    return y

W_BG = 1024
# far mountains
im = Image.new("RGBA", (W_BG, 360), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
y = ridge(W_BG, 360, 330, 220, 4, 1)
d.polygon([(0, 360)] + [(x, y[x]) for x in range(W_BG)] + [(W_BG - 1, 360)], fill=(128, 160, 196, 255))
y2 = ridge(W_BG, 360, 345, 120, 3, 2)
d.polygon([(0, 360)] + [(x, y2[x]) for x in range(W_BG)] + [(W_BG - 1, 360)], fill=(108, 142, 180, 255))
im = im.filter(ImageFilter.GaussianBlur(0.8))
im.save(os.path.join(OUT, "bg_mountains.png"))

# mid hills with trees
im = Image.new("RGBA", (W_BG, 300), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
y = ridge(W_BG, 300, 300, 160, 3, 5)
d.polygon([(0, 300)] + [(x, y[x] + 40) for x in range(W_BG)] + [(W_BG - 1, 300)], fill=(76, 128, 84, 255))
rr = random.Random(5)
for _ in range(70):
    x = rr.uniform(0, W_BG)
    base = y[int(x) % W_BG] + 44
    h = rr.uniform(26, 56)
    col = rr.choice([(54, 102, 64), (62, 112, 70), (48, 92, 58)])
    for xx in (x, x - W_BG, x + W_BG):
        d.rectangle([xx - 2, base - h * 0.3, xx + 2, base], fill=(70, 52, 40, 255))
        d.polygon([(xx - h * 0.32, base - h * 0.25), (xx + h * 0.32, base - h * 0.25), (xx, base - h)], fill=col + (255,))
im.save(os.path.join(OUT, "bg_hills.png"))

# near hills (darker, bigger)
im = Image.new("RGBA", (W_BG, 260), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
y = ridge(W_BG, 260, 260, 110, 2, 9)
d.polygon([(0, 260)] + [(x, y[x] + 60) for x in range(W_BG)] + [(W_BG - 1, 260)], fill=(56, 98, 62, 255))
for _ in range(40):
    x = rr.uniform(0, W_BG); base = y[int(x) % W_BG] + 64; r = rr.uniform(14, 30)
    for xx in (x, x - W_BG, x + W_BG):
        d.ellipse([xx - r, base - r * 1.6, xx + r, base], fill=(44, 82, 52, 255))
im.save(os.path.join(OUT, "bg_near.png"))

# clouds
for i in range(3):
    im, d = canvas(220, 100)
    rr = random.Random(20 + i)
    k = SS
    for _ in range(9):
        x, yy, r = rr.uniform(50, 170), rr.uniform(46, 66), rr.uniform(22, 38)
        d.ellipse([(x - r) * k, (yy - r) * k, (x + r) * k, (yy + r * 0.8) * k], fill=(255, 255, 255, 235))
    im = im.resize((220, 100), Image.LANCZOS).filter(ImageFilter.GaussianBlur(1.2))
    im.save(os.path.join(OUT, f"cloud{i}.png"))

# ---------------- effects ----------------
def radial(size, stops, name):
    yy, xx = np.mgrid[0:size, 0:size]
    r = np.sqrt((xx - size / 2 + 0.5) ** 2 + (yy - size / 2 + 0.5) ** 2) / (size / 2)
    arr = np.zeros((size, size, 4), np.float32)
    for i in range(len(stops) - 1):
        (p0, c0), (p1, c1) = stops[i], stops[i + 1]
        m = (r >= p0) & (r < p1)
        t = ((r - p0) / (p1 - p0))[m][:, None]
        arr[m] = np.array(c0) * (1 - t) + np.array(c1) * t
    Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA").save(os.path.join(OUT, name + ".png"))

radial(64, [(0, (255, 255, 255, 255)), (0.35, (255, 255, 255, 170)), (1.0, (255, 255, 255, 0)), (2, (255, 255, 255, 0))], "glow")
radial(128, [(0, (255, 250, 220, 255)), (0.25, (255, 214, 90, 255)), (0.55, (255, 120, 30, 220)), (0.85, (180, 50, 20, 90)), (1.0, (120, 40, 20, 0)), (2, (0, 0, 0, 0))], "fireball")

im, d = canvas(64, 64)
rr = random.Random(4)
for _ in range(7):
    x, yy, r = rr.uniform(22, 42), rr.uniform(22, 42), rr.uniform(12, 18)
    d.ellipse([(x - r) * SS, (yy - r) * SS, (x + r) * SS, (yy + r) * SS], fill=(255, 255, 255, 70))
im.resize((64, 64), Image.LANCZOS).filter(ImageFilter.GaussianBlur(2.5)).save(os.path.join(OUT, "smoke.png"))

# muzzle flash, origin at left middle
im, d = canvas(48, 28)
k = SS
d.polygon([(0, 14 * k), (20 * k, 2 * k), (16 * k, 11 * k), (47 * k, 14 * k), (16 * k, 17 * k), (20 * k, 26 * k)], fill=(255, 170, 40, 230))
d.polygon([(0, 14 * k), (14 * k, 7 * k), (12 * k, 12 * k), (32 * k, 14 * k), (12 * k, 16 * k), (14 * k, 21 * k)], fill=(255, 236, 140, 255))
d.ellipse([0, 9 * k, 12 * k, 19 * k], fill=(255, 255, 230, 255))
im.resize((48, 28), Image.LANCZOS).filter(ImageFilter.GaussianBlur(0.6)).save(os.path.join(OUT, "flash.png"))

# ---------------- meta.gd ----------------
with open(os.path.join(OUT, "meta.gd"), "w") as f:
    f.write("# generated by make_art.py\nconst GUN_SCALE := %d\nconst CHAR_SCALE := %d\nconst GUN := %s\n" % (GS, CS, json.dumps(META, indent=1)))

# contact sheet for review
names = sorted(n for n in os.listdir(OUT) if n.endswith(".png"))
sheet = Image.new("RGBA", (1400, 900), (90, 150, 210, 255))
x = y = 8; rowh = 0
for n in names:
    im = Image.open(os.path.join(OUT, n))
    if im.width > 400:
        im = im.resize((400, int(im.height * 400 / im.width)))
    if n.startswith(("head", "torso", "leg", "jet", "hand", "gun_", "grenade", "medkit")):
        im = im.resize((im.width * 2, im.height * 2), Image.LANCZOS)
    if x + im.width > 1392:
        x = 8; y += rowh + 8; rowh = 0
    sheet.alpha_composite(im, (x, y))
    x += im.width + 8; rowh = max(rowh, im.height)
sheet.save(sys.argv[2] if len(sys.argv) > 2 else "/tmp/sheet.png")
print("assets:", len(names))
