"""Sky Squad v0.7 art: minigun ("wheel machine gun"), flamethrower ("fire blaze gun"), smoke grenade."""
import os, sys, json
import numpy as np
from PIL import Image, ImageDraw

OUT = os.path.join(sys.argv[1], "art")
SS = 4
GS = 3
GK = GS * SS
OUTLINE = (27, 29, 42, 255)

def hexc(h, a=255):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (a,)

def canvas(w, h):
    im = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)

def sc(pts, k):
    return [(x * k, y * k) for x, y in pts]

def P(d, pts, fill, w=1.0):
    d.polygon(sc(pts, GK), fill=fill, outline=OUTLINE, width=int(w * GK))
def R(d, x0, y0, x1, y1, fill, r=0.6, w=0.9):
    d.rounded_rectangle(sc([(x0, y0), (x1, y1)], GK), radius=r * GK, fill=fill, outline=OUTLINE, width=int(w * GK))
def L(d, pts, fill, w):
    d.line(sc(pts, GK), fill=fill, width=int(w * GK))
def E(d, x0, y0, x1, y1, fill, w=0.8):
    d.ellipse(sc([(x0, y0), (x1, y1)], GK), fill=fill, outline=OUTLINE, width=int(w * GK))

METAL = hexc("#3a3f4b"); METAL_L = hexc("#5d6474"); METAL_D = hexc("#22252d")

def gun_shade(im):
    a = np.array(im).astype(np.float32)
    grad = np.linspace(1.2, 0.76, a.shape[0])[:, None]
    a[..., :3] *= grad[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGBA")

meta_path = os.path.join(OUT, "meta.gd")
GUN = json.loads(open(meta_path).read().split("const GUN := ", 1)[1])

def save_gun(im, name, W_, H_, grip, muzzle, front):
    gun_shade(im).resize((W_ * GS, H_ * GS), Image.LANCZOS).save(os.path.join(OUT, "gun_" + name + ".png"))
    GUN[name] = {"size": [W_, H_], "grip": grip, "muzzle": muzzle, "front": front, "len": int(muzzle[0] - grip[0])}

# Minigun: big motor box, ammo drum, six spinning barrels in a cluster
im, d = canvas(46 * GS, 20 * GS)
P(d, [(9, 12), (13, 12), (12.4, 18.6), (8.6, 18.6)], hexc("#24262c"))          # rear grip
E(d, 1, 9.6, 10.4, 19.4, hexc("#5a6236"))                                     # ammo drum
L(d, [(3, 14.5), (8.4, 14.5)], hexc("#3f4526"), 0.6)
R(d, 7, 4, 22, 13, METAL, 1.4)                                                 # motor housing
d.rectangle(sc([(9, 5), (20, 6.2)], GK), fill=METAL_L)
for x in (10, 13, 16, 19):
    L(d, [(x, 7.6), (x, 11.2)], METAL_D, 0.5)
R(d, 14.5, 1.2, 20, 4.2, METAL_D, 0.6, 0.6)                                    # carry handle
R(d, 21, 3.6, 25.2, 13.4, hexc("#2c2f37"), 0.8)                                # front clamp
for i, y in enumerate((4.6, 6.6, 8.6, 10.6, 12.2)):
    col = METAL_L if i % 2 == 0 else METAL
    R(d, 24.6, y - 0.8, 45.2, y + 0.8, col, 0.4, 0.45)                          # barrels
R(d, 33, 3.2, 35, 13.6, METAL_D, 0.4, 0.6)                                     # barrel ring
R(d, 42.6, 3.2, 44.2, 13.6, METAL_D, 0.4, 0.6)
P(d, [(17, 13), (20.4, 13), (21.6, 18.4), (18.4, 18.8)], METAL_D)              # front grip
save_gun(im, "minigun", 46, 20, [11, 15], [45.2, 8.4], [19.6, 16])

# Flamethrower: fuel tank under, long nozzle with pilot flame
im, d = canvas(42 * GS, 18 * GS)
P(d, [(8, 9.6), (11.6, 9.6), (10.8, 16.4), (7.6, 16.4)], hexc("#24262c"))
R(d, 2, 4.6, 26, 9.8, hexc("#8d2f22"), 1.2)                                    # red body
d.rectangle(sc([(4, 5.4), (24, 6.4)], GK), fill=hexc("#c4553e"))
L(d, [(6, 8.4), (22, 8.4)], hexc("#5e1c14"), 0.5)
E(d, 13, 9.2, 23, 17.4, hexc("#e8a52c"))                                       # fuel tank
L(d, [(14.6, 13.3), (21.4, 13.3)], hexc("#9b6a14"), 0.6)
L(d, [(18, 9.6), (18, 17)], hexc("#9b6a14"), 0.4)
R(d, 25.4, 5.4, 39, 8.8, METAL, 0.6)                                           # nozzle
R(d, 38.4, 4.4, 41.6, 9.8, METAL_D, 0.5, 0.6)
R(d, 29, 3.2, 31.6, 11, METAL_D, 0.4, 0.5)                                     # heat shield ring
d.ellipse(sc([(40.2, 1.6), (42, 4.4)], GK), fill=hexc("#5ec8ff", 230))         # blue pilot flame
P(d, [(20, 9.8), (23.4, 9.8), (24.4, 15.6), (21.2, 16)], METAL_D)              # front grip
save_gun(im, "flame", 42, 18, [9.6, 12.6], [41.6, 7.1], [22.4, 13.4])

# Smoke grenade canister 12 x 16
im, d = canvas(12 * GS, 16 * GS)
R(d, 2, 4, 10, 15.4, hexc("#7a8a7e"), 1.0)
d.rectangle(sc([(2.6, 7.2), (9.4, 9.6)], GK), fill=hexc("#cfd8c9"))
R(d, 4, 1.4, 8, 4.4, METAL_D, 0.4, 0.6)
L(d, [(8, 2.4), (10.6, 0.8)], METAL_L, 0.7)
for x in (3.4, 5.2, 7.0, 8.8):
    d.ellipse(sc([(x - 0.35, 12.4), (x + 0.35, 13.1)], GK), fill=hexc("#2a2d33"))
im.resize((12 * GS, 16 * GS), Image.LANCZOS).save(os.path.join(OUT, "smoke_can.png"))

# Flame puff sprite (soft orange) 32x32
yy, xx = np.mgrid[0:96, 0:96]
r = np.sqrt((xx - 48) ** 2 + (yy - 48) ** 2) / 48
a = np.clip(1 - r, 0, 1) ** 1.6
img = np.zeros((96, 96, 4), np.uint8)
img[..., 0] = 255
img[..., 1] = np.clip(120 + 135 * (1 - r) ** 2, 0, 255).astype(np.uint8)
img[..., 2] = np.clip(40 + 160 * np.clip(1 - r * 2.2, 0, 1), 0, 255).astype(np.uint8)
img[..., 3] = (a * 255).astype(np.uint8)
Image.fromarray(img, "RGBA").save(os.path.join(OUT, "flame.png"))

with open(meta_path, "w") as f:
    f.write("# generated by make_art.py + make_art_hd.py + make_art_v07.py\nconst GUN_SCALE := 3\nconst CHAR_SCALE := 3\nconst GUN := %s\n" % json.dumps(GUN, indent=1))
print("v07 art ok", sorted(GUN.keys()))
