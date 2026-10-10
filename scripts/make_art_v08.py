"""Sky Squad v0.8 art for the new maps.
Outpost (desert army base): sand tiles, sand edge, concrete blocks, sandbags, desert mesas/dunes background.
Catacombs (under the ground): cave soil, moss edge, stone bricks, torch, dark cave-wall background with arches."""
import os, sys, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

OUT = os.path.join(sys.argv[1], "art")
SS = 4
TP = 128

def smooth_noise(w, h, scales, seed):
    r = np.random.default_rng(seed)
    acc = np.zeros((h, w), np.float32)
    for s, amp in scales:
        n = r.normal(0, 1, (max(2, h // s), max(2, w // s))).astype(np.float32)
        im = Image.fromarray(((n - n.min()) / (np.ptp(n) + 1e-6) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
        acc += (np.asarray(im, np.float32) / 255 - 0.5) * amp
    return acc

def tinted(base, seed, amt=0.5, scales=None):
    n = smooth_noise(TP, TP, scales or [(32, 0.5), (12, 0.35), (4, 0.25), (1, 0.12)], seed)
    arr = np.zeros((TP, TP, 4), np.float32)
    for i in range(3):
        arr[..., i] = base[i] * (1 + n * amt)
    arr[..., 3] = 255
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA")

def save(im, name):
    im.save(os.path.join(OUT, name + ".png"))

# ---------- OUTPOST ----------
for i in range(3):
    im = tinted((214, 178, 120), 300 + i, 0.32).resize((TP * 2, TP * 2), Image.BICUBIC)
    d = ImageDraw.Draw(im)
    rr = random.Random(300 + i)
    for _ in range(7):   # wind ripples
        y = rr.uniform(20, 236); x = rr.uniform(0, 120)
        d.arc([x, y, x + rr.uniform(60, 140), y + 18], 200, 340, fill=(236, 206, 150, 255), width=3)
        d.arc([x, y + 3, x + rr.uniform(60, 140), y + 21], 200, 340, fill=(176, 140, 88, 255), width=2)
    for _ in range(10):  # pebbles
        x, y, r = rr.uniform(8, 248), rr.uniform(8, 248), rr.uniform(3, 7)
        d.ellipse([x - r, y - r * 0.7, x + r, y + r * 0.7], fill=rr.choice([(170, 140, 100), (190, 160, 118), (150, 120, 86)]) + (255,))
    save(im.resize((TP, TP), Image.LANCZOS), f"sand{i}")

# sand edge cap (replaces grass): light crest with a few dry tufts
im = Image.new("RGBA", (TP * SS, 64 * SS), (0, 0, 0, 0)); d = ImageDraw.Draw(im); k = SS
d.rectangle([0, 22 * k, TP * k, 40 * k], fill=(232, 202, 146, 255))
d.rectangle([0, 34 * k, TP * k, 42 * k], fill=(200, 166, 108, 255))
d.line([0, 23 * k, TP * k, 23 * k], fill=(250, 230, 186, 255), width=2 * k)
rr = random.Random(31)
for _ in range(10):
    x = rr.uniform(4, TP - 4)
    for j in range(5):
        a = -1.2 + j * 0.6
        d.line([x * k, 23 * k, (x + np.sin(a) * 9) * k, (23 - np.cos(a) * rr.uniform(6, 12)) * k], fill=(160, 140, 80, 255), width=int(1.4 * k))
save(im.resize((TP, 64), Image.LANCZOS), "sandcap")

# concrete block (bunker walls): smooth grey slab with seams and bolts
n = smooth_noise(TP, TP, [(24, 0.3), (6, 0.15), (1, 0.08)], 77)
arr = np.zeros((TP, TP, 4), np.float32)
for i, b in enumerate((150, 148, 140)):
    arr[..., i] = b * (1 + n * 0.35)
arr[..., 3] = 255
im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA").resize((TP * 2, TP * 2), Image.BICUBIC)
d = ImageDraw.Draw(im)
d.rectangle([2, 2, 253, 253], outline=(92, 92, 88, 255), width=6)
d.line([10, 10, 245, 10], fill=(190, 190, 184, 255), width=4)
d.line([10, 10, 10, 245], fill=(176, 176, 170, 255), width=3)
d.line([0, 128, 256, 128], fill=(110, 110, 104, 255), width=3)
for x, y in ((26, 26), (230, 26), (26, 230), (230, 230)):
    d.ellipse([x - 6, y - 6, x + 6, y + 6], fill=(96, 96, 92, 255)); d.ellipse([x - 3, y - 4, x + 1, y], fill=(200, 200, 196, 255))
rr = random.Random(5)
for _ in range(3):
    x, y = rr.uniform(40, 216), rr.uniform(40, 216)
    d.line([x, y, x + rr.uniform(-30, 30), y + rr.uniform(10, 30)], fill=(105, 105, 100, 255), width=2)
save(im.resize((TP, TP), Image.LANCZOS), "concrete")

W = 2048
def ridge(w, base, amp, octs, seed):
    r = np.random.default_rng(seed)
    xs = np.arange(w); y = np.full(w, float(base))
    for o in range(octs):
        f = (o + 1) * 2
        y -= amp / (o + 1) * (0.5 + 0.5 * np.sin(xs / w * 2 * np.pi * f + r.uniform(0, 6.28)))
    return y

def layer(w, h, top, c_top, c_bot):
    yy = np.arange(h)[:, None].astype(np.float32)
    t = np.clip((yy - top.min()) / max(1.0, h - top.min()), 0, 1)
    col = np.zeros((h, w, 4), np.float32)
    for i in range(3):
        col[..., i] = c_top[i] * (1 - t) + c_bot[i] * t
    col[..., 3] = (yy >= top[None, :]) * 255.0
    return col

def to_im(arr, blur=0.0):
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA")
    return im.filter(ImageFilter.GaussianBlur(blur)) if blur else im

# far mesas: flat-topped cliffs
H = 700
xs = np.arange(W)
top = np.full(W, 690.0)
rr = random.Random(8)
x = 0
while x < W:
    wdt = rr.uniform(160, 380); hgt = rr.uniform(200, 380)
    l, r_ = int(x), int(min(W, x + wdt))
    for xi in range(l, r_):
        k = (xi - l) / max(1, r_ - l)
        edge = min(1.0, k / 0.12, (1 - k) / 0.12)
        top[xi] = min(top[xi], 690 - hgt * edge ** 0.5)
    x += wdt + rr.uniform(40, 200)
top = np.convolve(np.pad(top, 6, mode="wrap"), np.ones(13) / 13, mode="valid")
far = layer(W, H, top, (214, 150, 112), (176, 112, 86))
yy = np.arange(H)[:, None]
for band in range(4):   # rock strata
    y0 = top[None, :] + 40 + band * 60
    m = (np.abs(yy - y0) < 6) * (yy >= top[None, :])
    for i, c in enumerate((196, 132, 98)):
        far[..., i] = far[..., i] * (1 - m * 0.5) + c * m * 0.5
to_im(far, 1.0).save(os.path.join(OUT, "bg_out_far.png"))

# dunes
H = 560
y = np.clip(ridge(W, 520, 200, 3, 15), 220, 520)
dunes = layer(W, H, y, (226, 182, 124), (190, 146, 94))
im = to_im(dunes).resize((W * 2, H * 2), Image.BICUBIC)
d = ImageDraw.Draw(im)
rr = random.Random(9)
for _ in range(22):   # cactus + poles
    x = rr.uniform(0, W); base = (y[int(x) % W] + 8) * 2; h = rr.uniform(50, 110) * 2
    for xx in (x * 2, x * 2 - W * 2, x * 2 + W * 2):
        if rr.random() < 0.6:
            d.rounded_rectangle([xx - 9, base - h, xx + 9, base], radius=9, fill=(104, 132, 76, 255))
            d.rounded_rectangle([xx - 34, base - h * 0.6, xx - 22, base - h * 0.3], radius=6, fill=(104, 132, 76, 255))
            d.rectangle([xx - 30, base - h * 0.36, xx - 9, base - h * 0.3], fill=(104, 132, 76, 255))
        else:
            d.rectangle([xx - 3, base - h * 1.4, xx + 3, base], fill=(96, 74, 56, 255))
            d.line([xx - 30, base - h * 1.3, xx + 30, base - h * 1.3], fill=(96, 74, 56, 255), width=4)
im.resize((W, H), Image.LANCZOS).save(os.path.join(OUT, "bg_out_mid.png"))

# near: fence, tents and barrels silhouettes
H = 480
y = np.clip(ridge(W, 455, 90, 2, 19), 300, 440)
near = layer(W, H, y, (196, 150, 98), (160, 116, 72))
im = to_im(near).resize((W * 2, H * 2), Image.BICUBIC)
d = ImageDraw.Draw(im)
for x in range(0, W * 2, 90):   # wire fence
    base = y[(x // 2) % W] * 2 + 10
    d.rectangle([x - 4, base - 120, x + 4, base], fill=(110, 86, 62, 255))
for x in range(0, W * 2, 4):
    base = y[(x // 2) % W] * 2 + 10
    for hh in (100, 70, 40):
        if (x // 4) % 2 == 0:
            d.point((x, base - hh), fill=(90, 80, 70, 255))
rr = random.Random(21)
for _ in range(6):
    x = rr.uniform(100, W * 2 - 300); base = y[int(x // 2) % W] * 2 + 10
    d.polygon([(x, base), (x + 260, base), (x + 130, base - 150)], fill=(126, 120, 74, 255))
    d.polygon([(x + 100, base), (x + 160, base), (x + 130, base - 90)], fill=(70, 66, 40, 255))
im.resize((W, H), Image.LANCZOS).save(os.path.join(OUT, "bg_out_near.png"))

# ---------- CATACOMBS ----------
for i in range(3):
    im = tinted((86, 70, 62), 500 + i, 0.6).resize((TP * 2, TP * 2), Image.BICUBIC)
    d = ImageDraw.Draw(im)
    rr = random.Random(500 + i)
    for _ in range(10):   # embedded stones
        x, y, r = rr.uniform(10, 246), rr.uniform(10, 246), rr.uniform(6, 14)
        c = rr.choice([(112, 104, 98), (96, 88, 84), (128, 118, 108)])
        d.ellipse([x - r, y - r * 0.8, x + r, y + r * 0.8], fill=c + (255,))
        d.arc([x - r, y - r * 0.8, x + r, y + r * 0.8], 190, 330, fill=(150, 140, 130, 255), width=2)
    if i == 2:   # a little bone
        d.line([90, 150, 150, 130], fill=(214, 204, 180, 255), width=8)
        for (bx, by) in ((90, 150), (150, 130)):
            d.ellipse([bx - 8, by - 9, bx + 2, by + 1], fill=(214, 204, 180, 255)); d.ellipse([bx - 4, by - 2, bx + 6, by + 8], fill=(214, 204, 180, 255))
    save(im.resize((TP, TP), Image.LANCZOS), f"cave{i}")

# moss edge cap
im = Image.new("RGBA", (TP * SS, 64 * SS), (0, 0, 0, 0)); d = ImageDraw.Draw(im); k = SS
d.rectangle([0, 22 * k, TP * k, 36 * k], fill=(70, 98, 60, 255))
rr = random.Random(41)
for _ in range(60):
    x = rr.uniform(0, TP); r = rr.uniform(3, 7)
    d.ellipse([(x - r) * k, (24 - r) * k, (x + r) * k, (24 + r) * k], fill=rr.choice([(86, 120, 70), (64, 92, 56), (100, 136, 80)]) + (255,))
for _ in range(8):   # hanging strands
    x = rr.uniform(4, TP - 4)
    d.line([x * k, 34 * k, x * k, (34 + rr.uniform(4, 12)) * k], fill=(64, 92, 56, 255), width=int(1.5 * k))
save(im.resize((TP, 64), Image.LANCZOS), "moss")

# stone brick (unbreakable)
n = smooth_noise(TP, TP, [(16, 0.35), (4, 0.2), (1, 0.1)], 88)
arr = np.zeros((TP, TP, 4), np.float32)
for i, b in enumerate((104, 98, 96)):
    arr[..., i] = b * (1 + n * 0.45)
arr[..., 3] = 255
im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA").resize((TP * 2, TP * 2), Image.BICUBIC)
d = ImageDraw.Draw(im)
for row, y0 in enumerate((0, 86, 172)):
    off = 0 if row % 2 == 0 else 64
    for x0 in range(-128 + off, 256, 128):
        d.rectangle([x0 + 3, y0 + 3, x0 + 125, y0 + 82], outline=(56, 52, 52, 255), width=5)
        d.line([x0 + 9, y0 + 9, x0 + 119, y0 + 9], fill=(140, 134, 128, 255), width=3)
save(im.resize((TP, TP), Image.LANCZOS), "brick")

# torch sprite 16 x 32 world (48 x 96 px): iron holder + flame
im = Image.new("RGBA", (48 * SS, 96 * SS), (0, 0, 0, 0)); d = ImageDraw.Draw(im); k = SS
d.polygon([(16 * k, 54 * k), (32 * k, 54 * k), (28 * k, 70 * k), (20 * k, 70 * k)], fill=(60, 56, 54, 255))
d.rectangle([22 * k, 68 * k, 26 * k, 92 * k], fill=(88, 64, 44, 255))
for r_, c in ((16, (255, 140, 40, 200)), (11, (255, 196, 80, 230)), (6, (255, 246, 190, 255))):
    d.ellipse([(24 - r_ * 0.7) * k, (48 - r_ * 1.6) * k, (24 + r_ * 0.7) * k, (54) * k], fill=c)
save(im.resize((48, 96), Image.LANCZOS), "torch")

# cave background: far wall with arches, mid pillars with skull niches
H = 760
yy = np.arange(H)[:, None].astype(np.float32)
nw = smooth_noise(W // 4, H // 4, [(24, 0.6), (8, 0.3), (2, 0.15)], 61)
nw = np.asarray(Image.fromarray(((nw - nw.min()) / np.ptp(nw) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC), np.float32) / 255
far = np.zeros((H, W, 4), np.float32)
for i, (a, b) in enumerate(((44, 30), (40, 28), (46, 34))):
    far[..., i] = a * (0.7 + 0.6 * nw) * (1 - 0.25 * yy / H) + b * 0.0
far[..., 3] = 255
im = to_im(far).resize((W * 2, H * 2), Image.BICUBIC)
d = ImageDraw.Draw(im)
for x in range(0, W * 2, 520):   # big arches
    d.rectangle([x + 60, 500, x + 460, 1520], fill=(26, 22, 26, 255))
    d.ellipse([x + 60, 300, x + 460, 700], fill=(26, 22, 26, 255))
    d.arc([x + 50, 290, x + 470, 710], 180, 360, fill=(70, 62, 60, 255), width=22)
    d.rectangle([x + 30, 500, x + 70, 1520], fill=(66, 58, 56, 255))
    d.rectangle([x + 450, 500, x + 490, 1520], fill=(66, 58, 56, 255))
im.resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(1.5)).save(os.path.join(OUT, "bg_cat_far.png"))

H = 600
mid = np.zeros((H, W, 4), np.float32)
im = Image.fromarray(mid.astype(np.uint8), "RGBA").resize((W * 2, H * 2))
d = ImageDraw.Draw(im)
rr = random.Random(77)
for x in range(0, W * 2, 300):
    pw = rr.uniform(70, 110)
    d.rectangle([x, 0, x + pw, H * 2], fill=(52, 46, 46, 255))
    d.rectangle([x + 6, 0, x + 14, H * 2], fill=(74, 66, 64, 255))
    for yv in range(160, H * 2, 260):   # niches with skulls
        nx = x + pw + 60
        d.rounded_rectangle([nx, yv, nx + 110, yv + 90], radius=20, fill=(20, 18, 22, 255))
        d.ellipse([nx + 35, yv + 30, nx + 75, yv + 70], fill=(150, 142, 126, 255))
        d.ellipse([nx + 43, yv + 42, nx + 52, yv + 52], fill=(20, 18, 22, 255)); d.ellipse([nx + 58, yv + 42, nx + 67, yv + 52], fill=(20, 18, 22, 255))
d.rectangle([0, H * 2 - 140, W * 2, H * 2], fill=(38, 32, 32, 255))
im.resize((W, H), Image.LANCZOS).save(os.path.join(OUT, "bg_cat_mid.png"))
print("v08 art ok")
