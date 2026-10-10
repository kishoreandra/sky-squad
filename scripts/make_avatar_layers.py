"""Game art for the Locker: every avatar part as its own see-through layer (3 px per world px), cropped,
plus recoloured leg strips per outfit. Writes skysquad/art/av/*.png and scripts/av_data.gd (consts for main.gd)."""
import os, sys, json
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = "/home/claude/skysquad/art/av"
os.makedirs(OUT, exist_ok=True)
for f in os.listdir(OUT):
    if f.endswith(".png"):
        os.remove(os.path.join(OUT, f))
sys.argv = [sys.argv[0], "/tmp/claude-0/avatars_unused"]
src = open(os.path.join(HERE, "make_avatars.py")).read()
src = src.replace("PX = 4 ", "PX = 3 ").split("LIST = []")[0]
g = {"__name__": "avlayers"}
exec(src, g)
K, W, H, PX, Pen, hx, shade = g["K"], g["W"], g["H"], g["PX"], g["Pen"], g["hx"], g["shade"]

RECTS = {}

def layer(name, fn):
    im = Image.new("RGBA", (W * K, H * K), (0, 0, 0, 0))
    pn = Pen(ImageDraw.Draw(im))
    fn(pn)
    im = im.resize((W * PX, H * PX), Image.LANCZOS)
    a = np.array(im)[:, :, 3]
    ys, xs = np.nonzero(a > 3)
    if len(xs) == 0:
        return
    x0, x1 = max(0, xs.min() - 2), min(W * PX, xs.max() + 3)
    y0, y1 = max(0, ys.min() - 2), min(H * PX, ys.max() + 3)
    im.crop((x0, y0, x1, y1)).save(os.path.join(OUT, name + ".png"))
    RECTS[name] = [round(x0 / PX, 3), round(y0 / PX, 3), round((x1 - x0) / PX, 3), round((y1 - y0) / PX, 3)]

WHITE = hx("#ffffff")
# head: skin + plain eye, face items, helmets (classic is white so the game can tint it with the team colour)
layer("face", lambda pn: g["face"](pn))
layer("f_none", g["eye"])
for k, fn in g["FACES"].items():
    layer("f_" + k, fn)
for k, fn in g["HELMETS"].items():
    if k == "classic":
        layer("h_classic", lambda pn: g["helmet_classic"](pn, WHITE))
    elif k == "astro":
        layer("h_astro", g["h_astro"])
    else:
        layer("h_" + k, fn)
# outfits: army splits into a tintable shirt + the vest on top
def army_shirt(pn): pn.r(22, 31, 39, 50, hx("#d9d9d9"), 4)
def army_vest(pn):
    pn.r(23.4, 33.5, 37.8, 47.5, hx("#4e5a3a"), 3, 0.9)
    for px in (25.5, 31.2):
        pn.r(px, 37, px + 4, 41.6, hx("#5f6d47"), 0.8, 0.7)
    pn.r(22.4, 46.4, 38.6, 48.6, hx("#5a3b22"), 0.3, 0.7)
    pn.r(29.4, 46.2, 31.8, 48.8, hx("#c9a640"), 0.2, 0.4)
layer("o_army_shirt", army_shirt)
layer("o_army", army_vest)
for k, o in g["OUTFITS"].items():
    if k != "army":
        layer("o_" + k, o["draw"])
for k, fn in g["JETS"].items():
    layer("j_" + k, fn)
EX = dict(g["EXTRAS"])
EX["pads"] = lambda pn: pn.e(36, 30, 42, 35, hx("#3a4250"), 0.9)   # shoulder pad only: legs move in game
for k, fn in EX.items():
    layer("x_" + k, fn)

# legs: recolour the game's leg strip for each outfit (pants + boots)
leg = np.array(Image.open("/home/claude/skysquad/art/leg.png").convert("RGBA")).astype(np.float64)
PANTS0, BOOT0 = np.array([74, 79, 57.0]), np.array([42, 37, 35.0])
def lum(c): return c[..., 0] * 0.3 + c[..., 1] * 0.59 + c[..., 2] * 0.11
rgb = leg[:, :, :3]
d_p = np.linalg.norm(rgb - PANTS0, axis=2)
d_b = np.linalg.norm(rgb - BOOT0, axis=2)
d_o = np.minimum(np.linalg.norm(rgb - np.array([23, 25, 40.0]), axis=2), np.linalg.norm(rgb - np.array([29, 31, 44.0]), axis=2))
LEG_DEF = (hx("#4a4f39"), hx("#2a2523"))
for k, o in g["OUTFITS"].items():
    if k == "army":
        continue
    pc = np.array(o.get("pants", LEG_DEF[0])[:3], np.float64)
    bc = np.array(o.get("boots", LEG_DEF[1])[:3], np.float64)
    out = leg.copy()
    pm = (d_p < d_b) & (d_p < d_o) & (d_p < 60)
    rows = np.arange(leg.shape[0])[:, None] * np.ones((1, leg.shape[1]))
    bm = (rows >= 36) & (rows <= 45) & (d_b < 30) & ~pm
    pm = pm & (rows < 36)
    fp = (lum(rgb) / lum(PANTS0))[..., None]
    fb = (lum(rgb) / lum(BOOT0))[..., None]
    out[:, :, :3] = np.where(pm[..., None], np.clip(pc * fp, 0, 255), out[:, :, :3])
    out[:, :, :3] = np.where(bm[..., None], np.clip(bc * fb, 0, 255), out[:, :, :3])
    Image.fromarray(out.astype(np.uint8)).save(os.path.join(OUT, "leg_" + k + ".png"))

def c2g(c):
    if c is None:
        return "null"
    return "[%s, %s]" % (cf(c[0]), cf(c[1]))
def cf(c): return "Color(%.3f, %.3f, %.3f, %.3f)" % tuple(v / 255 for v in c[:4])
def col(c): return "Color(%.3f, %.3f, %.3f)" % tuple(v / 255 for v in c[:3])

# lists for the Locker (order = how tiles appear)
def short(s): return s.replace(" (now)", "").replace(" (Halloween)", "").replace("Big mooch (moustache)", "Big mooch").replace(" + visor", "").replace("Back flag (India)", "India flag")
L = {"h": [[k, short(g["HELMET_LABEL"][k])] for k in g["HELMETS"]],
     "f": [[k, short(g["FACE_LABEL"][k])] for k in g["FACES"]] + [["none", "No glasses"]],
     "o": [[k, short(o["label"])] for k, o in g["OUTFITS"].items()],
     "j": [[k, short(g["JET_LABEL"][k])] for k in g["JETS"]],
     "x": [["none", "No extra"]] + [[k, short(g["EXTRA_LABEL"][k])] for k in EX],
     "fl": [[k, short(g["FLAME_LABEL"][k])] for k in g["FLAMES"]]}
full = open(os.path.join(HERE, "make_avatars.py")).read()
SRC_SETS = {}
exec("SETS = {" + full.split("SETS = {")[1].split("\n}\n")[0] + "\n}", {}, SRC_SETS)
DEF = {"helmet": "classic", "face": "goggles", "outfit": "army", "jet": "twin", "extra": None, "flame": "orange"}
sets = []
for k, (lab, sel) in SRC_SETS["SETS"].items():
    s = dict(DEF); s.update(sel)
    sets.append([k, lab, "%s.%s.%s.%s.%s.%s" % (s["helmet"], s["face"], s["outfit"], s["jet"], s["extra"] or "none", s["flame"])])

with open(os.path.join(HERE, "av_data.gd"), "w") as f:
    f.write("# ---- avatar data (made by make_avatar_layers.py) ----\n")
    f.write("const AV_RECT := " + json.dumps(RECTS) + "\n")
    f.write("const AV_LIST := " + json.dumps(L) + "\n")
    f.write("const AV_SETS := " + json.dumps(sets) + "\n")
    f.write("const AV_FULL := " + json.dumps(sorted(g["FULL_HELMETS"])) + "\n")
    f.write("const AV_BACK := " + json.dumps(sorted(g["BACK_EXTRAS"])) + "\n")
    f.write("const AV_FRONT := " + json.dumps(sorted(g["FRONT_EXTRAS"])) + "\n")
    f.write("const AV_FLAME := {" + ", ".join('"%s": %s' % (k, c2g(v)) for k, v in g["FLAMES"].items()) + "}\n")
    f.write("const AV_SLEEVE := {" + ", ".join('"%s": %s' % (k, col(o["sleeve"])) for k, o in g["OUTFITS"].items() if "sleeve" in o) + "}\n")
print(len(RECTS), "layers,", len(sets), "sets")
