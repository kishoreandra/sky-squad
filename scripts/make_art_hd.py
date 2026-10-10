"""Sky Squad v0.5 art: HD background + HD tiles + new weapons/items. Run after make_art.py."""
import os, sys, json, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

OUT = os.path.join(sys.argv[1], "art")
SS = 4
OUTLINE = (27, 29, 42, 255)
rng = np.random.default_rng(21)
random.seed(21)

def hexc(h, a=255):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (a,)

def canvas(w, h):
    im = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)

def down(im, w, h):
    return im.resize((w, h), Image.LANCZOS)

def sc(pts, k):
    return [(x * k, y * k) for x, y in pts]

def smooth_noise(w, h, scales, seed):
    r = np.random.default_rng(seed)
    acc = np.zeros((h, w), np.float32)
    for s, amp in scales:
        n = r.normal(0, 1, (max(2, h // s), max(2, w // s))).astype(np.float32)
        im = Image.fromarray(((n - n.min()) / (np.ptp(n) + 1e-6) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
        acc += (np.asarray(im, np.float32) / 255 - 0.5) * amp
    return acc

# ---------------- HD tiles (128 px for a 32 world px tile) ----------------
TP = 128
def dirt(seed):
    n = smooth_noise(TP, TP, [(32, 0.5), (12, 0.35), (4, 0.25), (1, 0.12)], seed)
    base = np.array([124, 82, 48], np.float32)
    arr = np.zeros((TP, TP, 4), np.float32)
    for i in range(3):
        arr[..., i] = base[i] * (1 + n * 0.55)
    arr[..., 3] = 255
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA")
    big = im.resize((TP * 2, TP * 2), Image.BICUBIC)
    d = ImageDraw.Draw(big)
    rr = random.Random(seed)
    for _ in range(9):
        x, y, r = rr.uniform(10, TP * 2 - 10), rr.uniform(10, TP * 2 - 10), rr.uniform(4, 10)
        col = rr.choice([(150, 116, 82), (112, 78, 50), (168, 134, 98)])
        d.ellipse([x - r, y - r * 0.75, x + r, y + r * 0.75], fill=col + (255,))
        d.arc([x - r, y - r * 0.75, x + r, y + r * 0.75], 190, 330, fill=(205, 172, 130, 255), width=2)
        d.arc([x - r, y - r * 0.75, x + r, y + r * 0.75], 20, 160, fill=(80, 54, 34, 255), width=2)
    for _ in range(3):  # little roots
        x, y = rr.uniform(20, TP * 2 - 20), rr.uniform(20, TP * 2 - 20)
        pts = [(x, y)]
        for _ in range(4):
            x += rr.uniform(-14, 14); y += rr.uniform(4, 14)
            pts.append((x, y))
        d.line(pts, fill=(88, 60, 38, 200), width=3, joint="curve")
    return big.resize((TP, TP), Image.LANCZOS)

for i in range(3):
    dirt(101 + i).save(os.path.join(OUT, f"dirt{i}.png"))

# grass cap 128x64 (32 x 16 world): band + soft blades
im, d = canvas(TP, 64)
k = SS
d.rectangle([0, 20 * k, TP * k, 44 * k], fill=hexc("#58a83b"))
d.rectangle([0, 38 * k, TP * k, 46 * k], fill=hexc("#3c7d2b"))
rr = random.Random(7)
for _ in range(160):
    x = rr.uniform(-2, TP + 2)
    hgt = rr.uniform(8, 22)
    col = rr.choice([hexc("#6cc24a"), hexc("#5aa83a"), hexc("#82d65c"), hexc("#4f9a35")])
    lean = rr.uniform(-4, 4)
    d.polygon([((x - 2.6) * k, 24 * k), ((x + 2.6) * k, 24 * k), ((x + lean) * k, (24 - hgt) * k)], fill=col)
for _ in range(14):
    x = rr.uniform(4, TP - 4)
    d.ellipse([(x - 2) * k, 30 * k, (x + 2) * k, 34 * k], fill=rr.choice([hexc("#f6e27a"), hexc("#ffffff"), hexc("#f59ab0")]))
d.line([0, 22 * k, TP * k, 22 * k], fill=hexc("#8fe06a", 160), width=2 * k)
g = down(im, TP, 64)
g.save(os.path.join(OUT, "grass.png"))

# rock: bevelled stone blocks
n = smooth_noise(TP, TP, [(16, 0.4), (4, 0.2), (1, 0.08)], 55)
arr = np.zeros((TP, TP, 4), np.float32)
for i, b in enumerate((112, 117, 126)):
    arr[..., i] = b * (1 + n * 0.4)
arr[..., 3] = 255
im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA").resize((TP * 2, TP * 2), Image.BICUBIC)
d = ImageDraw.Draw(im)
for (x0, y0, x1, y1) in [(0, 0, 150, 120), (150, 0, 256, 120), (0, 120, 90, 256), (90, 120, 256, 256)]:
    d.rectangle([x0 + 2, y0 + 2, x1 - 3, y1 - 3], outline=(74, 78, 88, 255), width=5)
    d.line([x0 + 8, y0 + 8, x1 - 9, y0 + 8], fill=(165, 170, 180, 255), width=4)
    d.line([x0 + 8, y0 + 8, x0 + 8, y1 - 9], fill=(150, 155, 165, 255), width=3)
im.resize((TP, TP), Image.LANCZOS).save(os.path.join(OUT, "rock.png"))

# wood planks
im = Image.new("RGBA", (TP * 2, TP * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
for i, y in enumerate((0, 86, 172)):
    base = [(150, 96, 52), (138, 88, 47), (158, 104, 58)][i]
    d.rounded_rectangle([0, y, TP * 2 - 1, y + 82], radius=8, fill=base + (255,), outline=(70, 44, 24, 255), width=5)
    for gx in range(6):
        gy = y + 14 + gx * 11
        d.line([12, gy, TP * 2 - 14, gy + random.uniform(-3, 3)], fill=tuple(int(c * 0.85) for c in base) + (255,), width=2)
    d.line([8, y + 8, TP * 2 - 10, y + 8], fill=tuple(min(255, int(c * 1.2)) for c in base) + (255,), width=3)
    for nx in (22, TP * 2 - 24):
        d.ellipse([nx - 6, y + 34, nx + 6, y + 46], fill=(60, 60, 66, 255))
        d.ellipse([nx - 3, y + 36, nx + 1, y + 40], fill=(140, 140, 150, 255))
im.resize((TP, TP), Image.LANCZOS).save(os.path.join(OUT, "wood.png"))

# crate
im, d = canvas(TP, TP)
k = SS
d.rounded_rectangle([3 * k, 3 * k, 125 * k, 125 * k], radius=6 * k, fill=hexc("#b07a42"), outline=hexc("#5a3a1d"), width=7 * k)
for y in (42, 84):
    d.line([8 * k, y * k, 120 * k, y * k], fill=hexc("#8a5a2e"), width=3 * k)
d.line([12 * k, 12 * k, 116 * k, 116 * k], fill=hexc("#7a4e26"), width=14 * k)
d.line([12 * k, 12 * k, 116 * k, 116 * k], fill=hexc("#c58c50"), width=8 * k)
d.rounded_rectangle([3 * k, 3 * k, 125 * k, 125 * k], radius=6 * k, outline=hexc("#5a3a1d"), width=7 * k)
d.line([10 * k, 10 * k, 118 * k, 10 * k], fill=hexc("#d39a5c"), width=3 * k)
for (x, y) in [(14, 14), (114, 14), (14, 114), (114, 114)]:
    d.ellipse([(x - 4) * k, (y - 4) * k, (x + 4) * k, (y + 4) * k], fill=hexc("#3a3a40"))
down(im, TP, TP).save(os.path.join(OUT, "crate.png"))

for stage in (1, 2):
    im, d = canvas(TP, TP)
    rr = random.Random(stage * 9)
    for _ in range(2 if stage == 1 else 5):
        x, y = rr.uniform(32, 96), rr.uniform(32, 96)
        pts = [(x, y)]
        for _ in range(5):
            x += rr.uniform(-18, 18); y += rr.uniform(-18, 18)
            pts.append((x, y))
        d.line([(a * SS, b * SS) for a, b in pts], fill=(30, 18, 10, 215), width=int(3.5 * SS), joint="curve")
    down(im, TP, TP).save(os.path.join(OUT, f"crack{stage}.png"))

# ---------------- HD background (2048 wide, smooth painted layers) ----------------
W = 2048
def ridge(w, base, amp, octs, seed):
    r = np.random.default_rng(seed)
    xs = np.arange(w)
    y = np.full(w, float(base))
    for o in range(octs):
        f = (o + 1) * 2
        y -= amp / (o + 1) * (0.5 + 0.5 * np.sin(xs / w * 2 * np.pi * f + r.uniform(0, 6.28)))
    return y

def grad_layer(w, h, top_y, c_top, c_bot, haze=None):
    """fill below a ridge with a vertical gradient; returns RGBA array"""
    yy = np.arange(h)[:, None].astype(np.float32)
    t = np.clip((yy - top_y[None, :].min()) / max(1.0, h - top_y.min()), 0, 1)
    col = np.zeros((h, w, 4), np.float32)
    for i in range(3):
        col[..., i] = c_top[i] * (1 - t) + c_bot[i] * t
    mask = yy >= top_y[None, :]
    col[..., 3] = mask * 255.0
    return col

def compose(layers, w, h):
    out = np.zeros((h, w, 4), np.float32)
    for L in layers:
        a = L[..., 3:4] / 255.0
        out[..., :3] = out[..., :3] * (1 - a) + L[..., :3] * a
        out[..., 3:4] = np.maximum(out[..., 3:4], L[..., 3:4])
    return out

def save_arr(arr, name, blur=0.0):
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA")
    if blur:
        im = im.filter(ImageFilter.GaussianBlur(blur))
    im.save(os.path.join(OUT, name + ".png"))

# far mountains with soft snow
H = 700
y1 = ridge(W, 650, 440, 4, 1)
y2 = ridge(W, 680, 260, 3, 2)
far = grad_layer(W, H, y1, (176, 200, 226), (126, 156, 192))
yy = np.arange(H)[:, None]
snow = np.clip(1 - (yy - y1[None, :]) / 70.0, 0, 1) * np.clip((420 - y1[None, :]) / 140.0, 0, 1) * (yy >= y1[None, :])
for i, c in enumerate((240, 246, 252)):
    far[..., i] = far[..., i] * (1 - snow * 0.85) + c * snow * 0.85
near_m = grad_layer(W, H, y2, (150, 178, 210), (110, 140, 178))
save_arr(compose([far, near_m], W, H), "bg_mountains", 1.2)

# mid hills with pine forest
H = 560
y = np.clip(ridge(W, 520, 260, 3, 5), 200, 500)
hills = grad_layer(W, H, y, (110, 160, 112), (66, 112, 74))
im = Image.fromarray(np.clip(hills, 0, 255).astype(np.uint8), "RGBA").resize((W * 2, H * 2), Image.BICUBIC)
d = ImageDraw.Draw(im)
rr = random.Random(5)
for _ in range(150):
    x = rr.uniform(0, W)
    base = (y[int(x) % W] + 10) * 2
    h = rr.uniform(60, 130) * 2
    col = rr.choice([(58, 104, 66), (66, 116, 74), (50, 94, 60), (74, 124, 80)])
    for xx in (x * 2, x * 2 - W * 2, x * 2 + W * 2):
        d.rectangle([xx - 4, base - h * 0.25, xx + 4, base], fill=(76, 58, 44, 255))
        for tier in range(3):
            tw = h * (0.34 - tier * 0.08)
            ty = base - h * (0.2 + tier * 0.25)
            d.polygon([(xx - tw, ty), (xx + tw, ty), (xx, ty - h * 0.42)], fill=col + (255,))
        d.line([xx, base - h, xx - h * 0.12, base - h * 0.62], fill=tuple(min(255, c + 22) for c in col) + (255,), width=3)
im = im.resize((W, H), Image.LANCZOS)
im.save(os.path.join(OUT, "bg_hills.png"))

# near bushes / round trees
H = 480
y = np.clip(ridge(W, 450, 170, 2, 9), 120, 420)
near = grad_layer(W, H, y, (74, 128, 80), (46, 86, 52))
im = Image.fromarray(np.clip(near, 0, 255).astype(np.uint8), "RGBA").resize((W * 2, H * 2), Image.BICUBIC)
d = ImageDraw.Draw(im)
for _ in range(80):
    x = rr.uniform(0, W); base = (y[int(x) % W] + 14) * 2; r = rr.uniform(26, 60) * 2
    for xx in (x * 2, x * 2 - W * 2, x * 2 + W * 2):
        d.ellipse([xx - r, base - r * 1.7, xx + r, base], fill=(52, 96, 58, 255))
        d.ellipse([xx - r * 0.7, base - r * 1.6, xx + r * 0.4, base - r * 0.7], fill=(66, 114, 70, 255))
im.resize((W, H), Image.LANCZOS).save(os.path.join(OUT, "bg_near.png"))

# soft clouds
for i in range(3):
    cw, ch = 520, 220
    im, d = canvas(cw, ch)
    rr2 = random.Random(40 + i)
    for _ in range(14):
        x, yv, r = rr2.uniform(110, cw - 110), rr2.uniform(100, 140), rr2.uniform(48, 86)
        d.ellipse([(x - r) * SS, (yv - r) * SS, (x + r) * SS, (yv + r * 0.75) * SS], fill=(255, 255, 255, 240))
    for _ in range(8):
        x, yv, r = rr2.uniform(130, cw - 130), rr2.uniform(130, 150), rr2.uniform(40, 70)
        d.ellipse([(x - r) * SS, (yv - r * 0.5) * SS, (x + r) * SS, (yv + r * 0.5) * SS], fill=(214, 226, 240, 200))
    im = down(im, cw, ch).filter(ImageFilter.GaussianBlur(2.2))
    im.save(os.path.join(OUT, f"cloud{i}.png"))

# ---------------- new weapons ----------------
GS = 3
GK = GS * SS
METAL = hexc("#3a3f4b"); METAL_L = hexc("#5d6474"); METAL_D = hexc("#22252d")

def P(d, pts, fill, w=1.0):
    d.polygon(sc(pts, GK), fill=fill, outline=OUTLINE, width=int(w * GK))
def R(d, x0, y0, x1, y1, fill, r=0.6, w=0.9):
    d.rounded_rectangle(sc([(x0, y0), (x1, y1)], GK), radius=r * GK, fill=fill, outline=OUTLINE, width=int(w * GK))
def L(d, pts, fill, w):
    d.line(sc(pts, GK), fill=fill, width=int(w * GK))

def gun_shade(im):
    a = np.array(im).astype(np.float32)
    grad = np.linspace(1.2, 0.76, a.shape[0])[:, None]
    a[..., :3] *= grad[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGBA")

meta_path = os.path.join(OUT, "meta.gd")
txt = open(meta_path).read()
GUN = json.loads(txt.split("const GUN := ", 1)[1])

def save_gun(im, name, W_, H_, grip, muzzle, front):
    gun_shade(im).resize((W_ * GS, H_ * GS), Image.LANCZOS).save(os.path.join(OUT, "gun_" + name + ".png"))
    GUN[name] = {"size": [W_, H_], "grip": grip, "muzzle": muzzle, "front": front, "len": int(muzzle[0] - grip[0])}

# SMG (MP5 style)
im, d = canvas(34 * GS, 16 * GS)
L(d, [(1, 5.5), (1, 10.5)], METAL_D, 1.0); L(d, [(1, 5.5), (8, 5.8)], METAL_D, 1.0); L(d, [(1, 10.5), (8, 9.6)], METAL_D, 1.0)
P(d, [(9.6, 8.2), (13, 8.2), (12.2, 14.6), (9.2, 14.6)], hexc("#24262c"))
P(d, [(15, 8.4), (18, 8.4), (19.8, 15.2), (16.8, 15.7)], METAL_D)
R(d, 7, 4, 24, 8.8, METAL, 0.8)
d.rectangle(sc([(9, 3.0), (22, 4.0)], GK), fill=METAL_D)
R(d, 22, 4.6, 29.4, 8.4, hexc("#2c2f37"), 0.8)
for x in (23.5, 25, 26.5, 28):
    L(d, [(x, 5.4), (x, 7.6)], METAL_D, 0.45)
R(d, 29.2, 5.6, 33.4, 7.2, METAL_D, 0.3, 0.7)
R(d, 27.6, 2.6, 28.8, 4.6, METAL_D, 0.2, 0.5)
R(d, 12.6, 8.2, 15.6, 10.6, (0, 0, 0, 0), 1, 0.7)
save_gun(im, "smg", 34, 16, [11, 10], [33.4, 6.4], [25.5, 7.2])

# Shock gun (taser)
im, d = canvas(30 * GS, 16 * GS)
P(d, [(6, 8.6), (11, 8.6), (10.2, 14.6), (6.2, 14.6)], hexc("#24262c"))
R(d, 3, 3.4, 22.5, 9.6, hexc("#f2c230"), 1.6)
for x in (6, 10, 14, 18):
    P(d, [(x, 3.6), (x + 1.6, 3.6), (x - 0.6, 9.4), (x - 2.2, 9.4)], hexc("#22252d"), 0.2)
R(d, 22, 4.4, 26, 8.6, METAL, 0.6)
L(d, [(26, 5), (29.6, 5)], METAL_L, 0.8); L(d, [(26, 8), (29.6, 8)], METAL_L, 0.8)
d.ellipse(sc([(27.2, 5.2), (29.6, 7.8)], GK), fill=hexc("#7fe8ff", 220))
R(d, 8, 1.6, 15, 3.6, hexc("#3a3f4b"), 0.6, 0.6)
d.ellipse(sc([(9, 2), (10.6, 3.2)], GK), fill=hexc("#5ef0ff"))
save_gun(im, "shock", 30, 16, [8.6, 11], [29.6, 6.5], [17, 9.2])

# Net gun
im, d = canvas(36 * GS, 18 * GS)
P(d, [(9.4, 10.6), (13, 10.6), (12.2, 16.8), (9, 16.8)], hexc("#24262c"))
P(d, [(0.8, 6), (8, 5.6), (8.6, 10), (1.6, 11.8)], hexc("#4a5530"))
R(d, 7, 3.6, 30.4, 11.2, hexc("#6b7a3a"), 1.4)
d.rectangle(sc([(9, 4.6), (29, 5.6)], GK), fill=hexc("#8a9a50"))
P(d, [(30, 3.2), (35.6, 1.4), (35.6, 13.6), (30, 11.6)], hexc("#4c5628"))
d.ellipse(sc([(14, 9.4), (21, 16.4)], GK), fill=hexc("#8a6a3a"), outline=OUTLINE, width=int(0.8 * GK))
L(d, [(15, 12.9), (20, 12.9)], hexc("#5c4424"), 0.5); L(d, [(17.5, 10.4), (17.5, 15.4)], hexc("#5c4424"), 0.5)
R(d, 20, 1.6, 24, 3.8, METAL_D, 0.4, 0.6)
save_gun(im, "net", 36, 18, [11, 13], [35.6, 7.5], [24, 10.4])

# Laser gun
im, d = canvas(38 * GS, 16 * GS)
P(d, [(10.4, 9.4), (14, 9.4), (13, 15), (9.8, 15)], hexc("#24262c"))
P(d, [(1.4, 6), (10, 3.2), (30, 3.2), (34.4, 5), (34.4, 8.6), (30, 10.2), (10, 10.2), (1.4, 9)], hexc("#e6ebf2"))
d.rectangle(sc([(10, 3.6), (30, 4.4)], GK), fill=hexc("#ffffff"))
L(d, [(9, 6.8), (31, 6.8)], hexc("#2fd7ff"), 1.3)
for x in (14, 19, 24):
    R(d, x, 5.6, x + 2.6, 8.2, hexc("#7ff4ff"), 0.4, 0.5)
R(d, 34, 5.2, 37.8, 8.4, METAL_D, 0.5, 0.6)
d.ellipse(sc([(36.4, 5.6), (38, 8)], GK), fill=hexc("#7ff4ff"))
R(d, 16, 1.4, 22, 3.4, hexc("#9aa6b6"), 0.5, 0.6)
save_gun(im, "laser", 38, 16, [12, 11], [37.8, 6.8], [24, 9])

# knife (handle at left), 18 x 6 world
im, d = canvas(18 * GS, 6 * GS)
R(d, 0.4, 1.6, 6.4, 4.4, hexc("#2a2523"), 0.8, 0.6)
R(d, 6, 0.6, 7.4, 5.4, METAL, 0.3, 0.5)
P(d, [(7.4, 1.4), (15.6, 1.4), (17.6, 3.0), (15.6, 4.6), (7.4, 4.6)], hexc("#d7dde6"), 0.6)
L(d, [(8, 2.1), (15.4, 2.1)], hexc("#ffffff"), 0.5)
im = down(im, 18 * GS, 6 * GS); im.save(os.path.join(OUT, "knife.png"))

# time bomb, 16 x 12 world
im, d = canvas(16 * GS, 12 * GS)
R(d, 1, 3, 15, 11.4, hexc("#7d8a4a"), 1.2)
L(d, [(5.2, 3), (5.2, 11.4)], hexc("#5c6636"), 0.6); L(d, [(10.8, 3), (10.8, 11.4)], hexc("#5c6636"), 0.6)
R(d, 4, 4.6, 12, 8.6, hexc("#1b1d22"), 0.6, 0.6)
d.rectangle(sc([(5, 5.6), (11, 7.6)], GK), fill=hexc("#ff3b3b"))
L(d, [(3, 3), (5, 0.6), (8, 1.6)], hexc("#e8553f"), 0.6); L(d, [(13, 3), (11, 0.8), (8, 1.6)], hexc("#3fa9f5"), 0.6)
down(im, 16 * GS, 12 * GS).save(os.path.join(OUT, "timebomb.png"))

# net overlay, 36 x 46 world
im, d = canvas(36 * 3, 46 * 3)
k = 3 * SS
for i in range(-6, 12):
    d.line([(i * 6) * k, 0, (i * 6 + 28) * k, 46 * k], fill=(160, 120, 70, 230), width=int(1.1 * k))
    d.line([(i * 6 + 28) * k, 0, (i * 6) * k, 46 * k], fill=(160, 120, 70, 230), width=int(1.1 * k))
d.rectangle([0, 0, 36 * k, 2 * k], fill=(120, 88, 50, 255))
mask = Image.new("L", im.size, 0); ImageDraw.Draw(mask).ellipse([0, 0, im.size[0], im.size[1]], fill=255)
im.putalpha(Image.fromarray(np.minimum(np.array(im)[..., 3], np.array(mask))))
down(im, 36 * 3, 46 * 3).save(os.path.join(OUT, "net_overlay.png"))

with open(meta_path, "w") as f:
    f.write("# generated by make_art.py + make_art_hd.py\nconst GUN_SCALE := 3\nconst CHAR_SCALE := 3\nconst GUN := %s\n" % json.dumps(GUN, indent=1))
print("hd art ok", sorted(GUN.keys()))
