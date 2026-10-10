"""Sky Squad avatar ideas: renders the game's chibi soldier wearing each helmet / face item / outfit /
jetpack / extra / flame colour, one card per option, so the user can pick. Output: PNGs + list.json"""
import os, sys, json, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
SS = 3
PX = 4                      # final pixels per world pixel
K = SS * PX
W, H = 66, 74               # card in world px
OL = (27, 29, 42, 255)
def hx(h, a=255):
    h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (a,)
def shade(c, f): return tuple(max(0, min(255, int(v * f))) for v in c[:3]) + (c[3] if len(c) > 3 else 255,)
SKIN, SKIN_D = hx("#f1c08f"), hx("#d79a68")
TEAM = hx("#f2c230")

class Pen:
    def __init__(self, d): self.d = d
    def p(self, pts, fill, w=1.0, ol=True):
        self.d.polygon([(x * K, y * K) for x, y in pts], fill=fill, outline=OL if ol else None, width=int(w * K) if ol else 0)
    def e(self, x0, y0, x1, y1, fill, w=1.0, ol=True):
        self.d.ellipse([x0 * K, y0 * K, x1 * K, y1 * K], fill=fill, outline=OL if ol else None, width=int(w * K) if ol else 0)
    def r(self, x0, y0, x1, y1, fill, rad=1.0, w=1.0, ol=True):
        self.d.rounded_rectangle([x0 * K, y0 * K, x1 * K, y1 * K], radius=rad * K, fill=fill, outline=OL if ol else None, width=int(w * K) if ol else 0)
    def l(self, pts, fill, w=1.0):
        self.d.line([(x * K, y * K) for x, y in pts], fill=fill, width=max(1, int(w * K)), joint="curve")
    def ch(self, x0, y0, x1, y1, a0, a1, fill, w=1.0):
        self.d.chord([x0 * K, y0 * K, x1 * K, y1 * K], a0, a1, fill=fill, outline=OL, width=int(w * K))
    def arc(self, x0, y0, x1, y1, a0, a1, fill, w=1.0):
        self.d.arc([x0 * K, y0 * K, x1 * K, y1 * K], a0, a1, fill=fill, width=max(1, int(w * K)))

HX, HY, HR = 31, 23, 10          # head centre / radius
# ---------------- base parts ----------------
def flame(pn, col):
    if col is None: return
    c1, c2 = col
    for x in (22.5, 27.5):
        pn.p([(x - 2.4, 53), (x + 2.4, 53), (x + 0.6, 66), (x - 0.6, 66)], c1, ol=False)
        pn.p([(x - 1.2, 53), (x + 1.2, 53), (x + 0.2, 60), (x - 0.2, 60)], c2, ol=False)

def jet_twin(pn):
    for x0 in (19.5, 24.5):
        pn.r(x0, 31, x0 + 6, 51, hx("#8a96a8"), 2.6)
        pn.r(x0 + 1, 32.5, x0 + 2.2, 48, hx("#e6ecf5", 200), 0.6, ol=False)
        pn.p([(x0 + 1, 51), (x0 + 5, 51), (x0 + 5.8, 54), (x0 + 0.2, 54)], hx("#3c4250"))
    pn.r(20, 38, 30, 40, hx("#c0392b"), 0.4, 0.6)

def legs(pn, pants=hx("#4a4f39"), boots=hx("#2a2523"), extra=None):
    for x0 in (24, 31):
        pn.r(x0, 48, x0 + 5.5, 61, pants, 2)
        pn.r(x0 - 0.5, 59.5, x0 + 7, 64.5, boots, 1.5)
    if extra: extra(pn)

def torso_base(pn, shirt, vest=hx("#4e5a3a"), pocket=hx("#5f6d47"), belt=hx("#5a3b22"), buckle=hx("#c9a640"), detail=None):
    pn.r(22, 31, 39, 50, shirt, 4)
    if vest is not None:
        pn.r(23.4, 33.5, 37.8, 47.5, vest, 3, 0.9)
        for px in (25.5, 31.2):
            pn.r(px, 37, px + 4, 41.6, pocket, 0.8, 0.7)
    if belt is not None:
        pn.r(22.4, 46.4, 38.6, 48.6, belt, 0.3, 0.7)
        pn.r(29.4, 46.2, 31.8, 48.8, buckle, 0.2, 0.4)
    if detail: detail(pn)

def face(pn, skin=SKIN):
    pn.e(HX - HR, HY - HR, HX + HR, HY + HR, skin, 1.2)
    pn.d.pieslice([(HX - HR + 1.2) * K, (HY - HR + 1.2) * K, (HX + HR - 1.2) * K, (HY + HR - 1.2) * K], 100, 200, fill=shade(skin, 0.86))
    pn.l([(HX + 4.5, HY + 7), (HX + 7.5, HY + 6.6)], hx("#6e3228"), 0.9)

def eye(pn):
    pn.e(HX + 4, HY - 0.5, HX + 7, HY + 2.5, hx("#ffffff"), 0.6)
    pn.e(HX + 5.4, HY + 0.3, HX + 6.9, HY + 1.8, hx("#1b1d2a"), 0.1, ol=False)

def goggles(pn):
    pn.r(HX + 2, HY - 0.2, HX + 9.8, HY + 4.2, hx("#1e2234"), 1.6, 1.2)
    pn.r(HX + 3.2, HY + 0.8, HX + 9, HY + 3.3, hx("#78dcff"), 1, ol=False)
    pn.l([(HX + 4, HY + 1.4), (HX + 6, HY + 1.4)], hx("#ffffff", 220), 0.8)

def helmet_classic(pn, c=TEAM):
    pn.ch(HX - 11, HY - 12.5, HX + 11, HY + 9.5, 180, 360, c, 1.2)
    pn.r(HX - 11, HY - 2.2, HX + 11, HY - 0.6, shade(c, 0.72), 0.2, 1.0)
    pn.p([(HX + 6, HY - 1.6), (HX + 13.5, HY - 1.4), (HX + 12.5, HY), (HX + 6, HY)], shade(c, 0.6))
    pn.arc(HX - 8, HY - 10, HX + 4, HY - 1, 200, 260, hx("#ffffff", 140), 1.4)
    for dx, dy in [(-5, -6), (1, -8), (5, -5), (-2, -4)]:
        pn.e(HX + dx - 1.2, HY + dy - 1, HX + dx + 1.2, HY + dy + 1, shade(c, 0.82), ol=False)

def arm_gun(pn, sleeve):
    pn.l([(33, 37), (43, 39)], OL, 3.0); pn.l([(33, 37), (43, 39)], sleeve, 2.0)
    # simple rifle
    pn.r(38, 36.2, 55, 39.6, hx("#3a3f4b"), 0.6, 0.8)
    pn.r(55, 37, 60, 38.6, hx("#22252d"), 0.3, 0.6)
    pn.p([(44, 39.4), (47, 39.4), (46.2, 44.5), (43.6, 44.5)], hx("#22252d"), 0.6)
    pn.p([(34, 37), (39, 36.5), (39, 40), (35, 41)], hx("#6b4a2b"), 0.6)
    pn.e(41.5, 37.6, 44.5, 40.6, SKIN, 0.7)

# ---------------- a full character with chosen parts ----------------
DEF = {"helmet": "classic", "face": "goggles", "outfit": "army", "jet": "twin", "extra": None, "flame": "orange"}

def render(sel, name, label_bg=None):
    im = Image.new("RGBA", (W * K, H * K), (0, 0, 0, 0))
    d = ImageDraw.Draw(im); pn = Pen(d)
    pn.e(18, 66, 46, 70, hx("#000000", 60), ol=False)
    s = dict(DEF); s.update(sel)
    o = OUTFITS[s["outfit"]]
    if s["extra"] in BACK_EXTRAS: EXTRAS[s["extra"]](pn)
    flame(pn, FLAMES[s["flame"]])
    JETS[s["jet"]](pn)
    legs(pn, o.get("pants", hx("#4a4f39")), o.get("boots", hx("#2a2523")), o.get("legx"))
    o["draw"](pn)
    if s["extra"] and s["extra"] not in BACK_EXTRAS: EXTRAS[s["extra"]](pn)
    face(pn, o.get("skin", SKIN))
    if s["helmet"] not in FULL_HELMETS:
        FACES[s["face"]](pn)
    HELMETS[s["helmet"]](pn)
    arm_gun(pn, o.get("sleeve", shade(TEAM, 0.85)))
    if s["extra"] in FRONT_EXTRAS: EXTRAS[s["extra"]](pn)
    im = im.resize((W * PX, H * PX), Image.LANCZOS)
    im.save(os.path.join(OUT, name + ".png"))

# ================= HELMETS / HEADGEAR =================
def h_beret(pn):
    pn.e(HX - 11, HY - 13, HX + 7, HY - 3, hx("#7a1f2b"), 1.1)
    pn.e(HX - 9, HY - 6.5, HX + 6, HY - 3.2, shade(hx("#7a1f2b"), 0.75), 0.8)
    pn.e(HX - 3, HY - 10, HX + 0, HY - 7, hx("#f2c230"), 0.6)
def h_bandana(pn):
    pn.ch(HX - 10.5, HY - 11.5, HX + 10.5, HY + 6, 180, 360, hx("#d6303a"), 1.1)
    for dx, dy in [(-5, -6), (0, -8), (4, -5), (-2, -3.5)]:
        pn.e(HX + dx - 0.9, HY + dy - 0.9, HX + dx + 0.9, HY + dy + 0.9, hx("#ffffff"), ol=False)
    pn.p([(HX - 9, HY - 3), (HX - 16, HY - 1), (HX - 15, HY + 3), (HX - 9, HY - 1)], hx("#d6303a"), 0.9)
def h_ninja(pn):
    pn.e(HX - HR - 0.5, HY - HR - 0.5, HX + HR + 0.5, HY + HR + 0.5, hx("#1f2230"), 1.2)
    pn.r(HX - 1, HY - 1.5, HX + 10, HY + 3.5, SKIN, 1.5, 0.8)
    pn.e(HX + 4.5, HY - 0.3, HX + 7.5, HY + 2.3, hx("#ffffff"), 0.5); pn.e(HX + 5.8, HY + 0.4, HX + 7.2, HY + 1.8, OL, ol=False)
    pn.p([(HX - 9, HY - 2), (HX - 17, HY - 4), (HX - 16, HY + 0), (HX - 9, HY + 1)], hx("#c0392b"), 0.8)
def h_pilot(pn):
    pn.ch(HX - 11.5, HY - 12.5, HX + 11.5, HY + 11, 160, 380, hx("#e8edf5"), 1.2)
    pn.r(HX + 1, HY - 3, HX + 11.5, HY + 3.5, hx("#ff9a3c"), 2.2, 1.0)
    pn.r(HX + 2.3, HY - 2, HX + 10.5, HY + 0.5, hx("#ffe0b0", 180), 1.2, ol=False)
    pn.l([(HX - 6, HY - 12), (HX - 4, HY + 4)], hx("#c0392b"), 1.6)
def h_astro(pn):
    pn.e(HX - 13, HY - 13, HX + 13, HY + 13, hx("#bfe8ff", 90), 1.2)
    pn.arc(HX - 10, HY - 11, HX + 6, HY + 2, 200, 270, hx("#ffffff", 220), 1.6)
    pn.r(HX - 9, HY + 10, HX + 9, HY + 13, hx("#d0d6e0"), 1.2, 0.9)
def h_nvg(pn):
    helmet_classic(pn, hx("#5b6b3a"))
    pn.r(HX + 2, HY - 9, HX + 7, HY - 4, hx("#2b2f38"), 0.8, 0.8)
    for y in (-8.5, -6.2):
        pn.r(HX + 6.5, HY + y, HX + 11, HY + y + 2, hx("#2b2f38"), 0.6, 0.6)
        pn.e(HX + 10.2, HY + y + 0.2, HX + 11.4, HY + y + 1.8, hx("#4cff7a"), ol=False)
def h_cowboy(pn):
    pn.e(HX - 15, HY - 6, HX + 16, HY - 1.5, hx("#7a4a24"), 1.1)
    pn.r(HX - 8, HY - 15, HX + 9, HY - 3.5, hx("#8c5a2e"), 4, 1.1)
    pn.r(HX - 8, HY - 6.5, HX + 9, HY - 4.5, hx("#2a1c12"), 0.2, 0.6)
def h_cap(pn):
    pn.ch(HX - 10.5, HY - 12, HX + 10.5, HY + 6, 180, 360, hx("#2f6fd6"), 1.1)
    pn.p([(HX - 9, HY - 3), (HX - 16, HY - 2.2), (HX - 15.5, HY - 0.6), (HX - 9, HY - 1)], hx("#1d4fa3"), 0.9)
    pn.e(HX - 1, HY - 12.5, HX + 1, HY - 10.8, hx("#ffffff"), 0.5)
def h_viking(pn):
    helmet_classic(pn, hx("#9aa3ad"))
    pn.p([(HX - 9, HY - 7), (HX - 15, HY - 15), (HX - 12.5, HY - 17), (HX - 7, HY - 9)], hx("#f2ead8"), 0.9)
    pn.p([(HX + 8, HY - 7), (HX + 14, HY - 15), (HX + 11.5, HY - 17), (HX + 6, HY - 9)], hx("#f2ead8"), 0.9)
def h_marine(pn):
    pn.e(HX - 11.5, HY - 12, HX + 11.5, HY + 11, hx("#2f7d4a"), 1.2)
    pn.p([(HX + 1, HY - 1), (HX + 11.5, HY - 2), (HX + 11, HY + 4), (HX + 2, HY + 3)], hx("#ffb020"), 1.0)
    pn.r(HX - 4, HY + 5, HX + 6, HY + 10, hx("#22553a"), 1.2, 0.8)
    for y in (6.2, 8.2): pn.l([(HX - 2, HY + y), (HX + 4, HY + y)], hx("#13311f"), 0.6)
def h_turban(pn):
    pn.e(HX - 11.5, HY - 14, HX + 10.5, HY - 0.5, hx("#f08a24"), 1.1)
    for i in range(4):
        pn.arc(HX - 10 + i * 0.4, HY - 13 + i * 3, HX + 9.5, HY - 1 + i * 0.5, 190, 340, shade(hx("#f08a24"), 0.75), 0.9)
    pn.e(HX + 4, HY - 9, HX + 7, HY - 6, hx("#e8202a"), 0.6)
    pn.l([(HX + 5.5, HY - 9), (HX + 7, HY - 13)], hx("#ffffff"), 0.8)
def h_samurai(pn):
    pn.ch(HX - 12, HY - 12.5, HX + 12, HY + 10, 180, 360, hx("#2a2a35"), 1.2)
    pn.p([(HX - 13, HY - 2), (HX - 15, HY + 4), (HX - 9, HY), (HX + 9, HY), (HX + 15, HY + 4), (HX + 13, HY - 2)], hx("#8b1e2a"), 1.0)
    pn.p([(HX - 1, HY - 12), (HX - 7, HY - 21), (HX - 4, HY - 21), (HX, HY - 14), (HX + 4, HY - 21), (HX + 7, HY - 21), (HX + 1, HY - 12)], hx("#d4a72c"), 0.8)
def h_gasmask(pn):
    helmet_classic(pn, hx("#4e5a3a"))
    pn.r(HX + 0.5, HY - 1.5, HX + 10.5, HY + 9, hx("#3a3f46"), 3, 1.0)
    pn.e(HX + 4, HY - 0.5, HX + 9, HY + 3.5, hx("#7fd0d8"), 0.7)
    pn.e(HX + 6, HY + 5, HX + 12.5, HY + 11, hx("#5d6470"), 0.9)
    for i in range(3): pn.l([(HX + 7.5 + i * 1.5, HY + 6), (HX + 7.5 + i * 1.5, HY + 10)], hx("#2b2f36"), 0.5)
def h_robot(pn):
    pn.r(HX - 11, HY - 11, HX + 11, HY + 10, hx("#b9c4d2"), 3, 1.2)
    pn.r(HX + 0.5, HY - 3, HX + 10, HY + 3.5, hx("#16202e"), 1.5, 0.8)
    pn.r(HX + 2, HY - 1.5, HX + 9, HY + 1.5, hx("#ff4d5e"), 0.8, ol=False)
    pn.l([(HX - 2, HY - 11), (HX - 3, HY - 17)], OL, 0.8); pn.e(HX - 4.5, HY - 19, HX - 1.5, HY - 16, hx("#ffd84a"), 0.6)
    for y in (5, 7): pn.l([(HX + 2, HY + y), (HX + 8, HY + y)], hx("#7a8696"), 0.6)
def h_hoodie(pn):
    pn.ch(HX - 12, HY - 12.5, HX + 11.5, HY + 11.5, 95, 335, hx("#3b3f58"), 1.2)
    pn.arc(HX - 9.5, HY - 10, HX + 9.5, HY + 9.5, 120, 320, hx("#555a78"), 1.2)
    pn.l([(HX - 2, HY + 9), (HX - 3, HY + 14)], hx("#e6e8f2"), 0.7)
def h_pumpkin(pn):
    pn.e(HX - 12, HY - 11, HX + 12, HY + 11, hx("#f07a1a"), 1.2)
    for dx in (-6, 0, 6): pn.arc(HX + dx - 5, HY - 11, HX + dx + 5, HY + 11, 270, 450, shade(hx("#f07a1a"), 0.75), 0.8)
    pn.p([(HX + 3, HY - 3), (HX + 6, HY - 6), (HX + 8, HY - 2)], hx("#2a1608"), 0.3)
    pn.p([(HX + 1, HY + 4), (HX + 10, HY + 4), (HX + 8, HY + 7), (HX + 3, HY + 7)], hx("#2a1608"), 0.3)
    pn.r(HX - 1, HY - 14, HX + 1.5, HY - 10, hx("#4a6a2a"), 0.5, 0.6)
def h_halo(pn):
    helmet_classic(pn, hx("#f6f0d8"))
    pn.e(HX - 8, HY - 18, HX + 8, HY - 14, hx("#ffe066", 0), 0.0, ol=False)
    pn.d.ellipse([(HX - 8) * K, (HY - 18) * K, (HX + 8) * K, (HY - 14) * K], outline=hx("#ffd84a"), width=int(1.6 * K))
def h_crown(pn):
    helmet_classic(pn)
    pn.p([(HX - 7, HY - 10), (HX - 7, HY - 17), (HX - 3.5, HY - 13), (HX, HY - 18), (HX + 3.5, HY - 13), (HX + 7, HY - 17), (HX + 7, HY - 10)], hx("#ffcc33"), 0.9)
    for dx in (-3.5, 0, 3.5): pn.e(HX + dx - 0.9, HY - 12.5, HX + dx + 0.9, HY - 10.7, hx("#e8202a"), ol=False)

FULL_HELMETS = {"ninja", "astro", "marine", "robot", "pumpkin"}
HELMETS = {"classic": helmet_classic, "beret": h_beret, "bandana": h_bandana, "ninja": h_ninja, "pilot": h_pilot,
           "astro": lambda pn: (goggles(pn), h_astro(pn)), "nvg": h_nvg, "cowboy": h_cowboy, "cap": h_cap,
           "viking": h_viking, "marine": h_marine, "turban": h_turban, "samurai": h_samurai, "gasmask": h_gasmask,
           "robot": h_robot, "hoodie": h_hoodie, "pumpkin": h_pumpkin, "halo": h_halo, "crown": h_crown}
HELMET_LABEL = {"classic": "Combat helmet (now)", "beret": "Commando beret", "bandana": "Rambo bandana", "ninja": "Ninja hood",
                "pilot": "Pilot helmet + visor", "astro": "Astronaut bubble", "nvg": "Night-vision helmet", "cowboy": "Cowboy hat",
                "cap": "Backwards cap", "viking": "Viking horns", "marine": "Space marine", "turban": "Pagdi / turban",
                "samurai": "Samurai kabuto", "gasmask": "Gas mask", "robot": "Robot head", "hoodie": "Street hoodie",
                "pumpkin": "Pumpkin (Halloween)", "halo": "Angel halo", "crown": "Champion crown"}

# ================= FACE / EYEWEAR =================
def f_shades(pn):
    pn.r(HX + 2, HY - 0.5, HX + 10, HY + 3, hx("#14161f"), 1.2, 0.9); pn.l([(HX + 3, HY + 0.3), (HX + 5, HY + 0.3)], hx("#ffffff", 180), 0.6)
def f_patch(pn):
    eye(pn); pn.e(HX + 3.8, HY - 0.8, HX + 7.6, HY + 3, hx("#14161f"), 0.6); pn.l([(HX - 9, HY - 4), (HX + 9, HY + 1)], hx("#14161f"), 0.7)
def f_scar(pn):
    eye(pn); pn.l([(HX + 2, HY - 3), (HX + 8, HY + 4)], hx("#b04a40"), 0.8)
    for i in range(3): pn.l([(HX + 3 + i * 2, HY - 1 + i * 2), (HX + 4.5 + i * 2, HY - 2.2 + i * 2)], hx("#b04a40"), 0.5)
def f_paint(pn):
    eye(pn)
    for y in (3.5, 5.5): pn.l([(HX - 2, HY + y), (HX + 9, HY + y)], hx("#2e3a2a"), 0.9)
def f_mooch(pn):
    eye(pn); pn.p([(HX + 3, HY + 5), (HX + 6, HY + 4.2), (HX + 9.5, HY + 5), (HX + 10.5, HY + 3.6), (HX + 9, HY + 6.4), (HX + 6, HY + 5.6), (HX + 3.5, HY + 6.6)], hx("#2a1a10"), 0.4)
def f_cyber(pn):
    pn.r(HX + 1, HY - 1, HX + 11, HY + 3, hx("#ff3ea5"), 1.4, 0.9); pn.l([(HX + 2, HY + 0.4), (HX + 10, HY + 0.4)], hx("#ffffff", 200), 0.5)
def f_monocle(pn):
    eye(pn); pn.d.ellipse([(HX + 3.4) * K, (HY - 1.4) * K, (HX + 7.6) * K, (HY + 3.2) * K], outline=hx("#d4a72c"), width=int(0.8 * K))
    pn.l([(HX + 5.5, HY + 3.2), (HX + 4, HY + 9)], hx("#d4a72c"), 0.4)
def f_cheeky(pn):
    eye(pn); pn.e(HX + 1, HY + 3.5, HX + 4, HY + 5.5, hx("#ff8a8a", 160), ol=False)
    pn.arc(HX + 4, HY + 4, HX + 9, HY + 8, 10, 160, hx("#6e3228"), 0.8)
FACES = {"goggles": goggles, "shades": f_shades, "patch": f_patch, "scar": f_scar, "paint": f_paint, "mooch": f_mooch, "cyber": f_cyber, "monocle": f_monocle, "cheeky": f_cheeky}
FACE_LABEL = {"goggles": "Flight goggles (now)", "shades": "Aviator shades", "patch": "Eye patch", "scar": "Battle scar",
              "paint": "War paint", "mooch": "Big mooch (moustache)", "cyber": "Cyber visor", "monocle": "Gentleman monocle", "cheeky": "Cheeky grin"}

# ================= OUTFITS =================
def camo(base, spots, seed):
    def det(pn):
        r = random.Random(seed)
        for _ in range(9):
            x, y = r.uniform(23.5, 37), r.uniform(32.5, 46)
            pn.e(x - 1.8, y - 1.2, x + 1.8, y + 1.2, r.choice(spots), ol=False)
    return det
def o_army(pn): torso_base(pn, shade(TEAM, 0.85))
def o_desert(pn): torso_base(pn, hx("#d9b27a"), hx("#c49a5e"), hx("#b5884d"), detail=camo(0, [hx("#a87b45"), hx("#e8cfa0")], 1))
def o_urban(pn): torso_base(pn, hx("#8d939c"), hx("#6c727b"), hx("#5b6068"), detail=camo(0, [hx("#4a4f57"), hx("#b5bac2")], 2))
def o_snow(pn): torso_base(pn, hx("#eef2f7"), hx("#d8dee8"), hx("#c5ccd8"), hx("#7a8696"), detail=camo(0, [hx("#b8c2d0"), hx("#ffffff")], 3))
def o_ninja(pn):
    torso_base(pn, hx("#1f2230"), None, belt=hx("#c0392b"), buckle=hx("#c0392b"))
    pn.l([(24, 33), (37, 46)], hx("#30344a"), 1.2)
def o_jumpsuit(pn):
    torso_base(pn, hx("#e86a1c"), None, belt=hx("#2b2f38"), buckle=hx("#9aa3ad"))
    pn.l([(30.5, 32), (30.5, 46)], hx("#b04e12"), 0.6); pn.r(32.5, 34, 37, 37, hx("#2f6fd6"), 0.4, 0.5)
def o_hazmat(pn):
    torso_base(pn, hx("#f2d21b"), None, belt=hx("#2b2f38"), buckle=hx("#2b2f38"))
    pn.e(27.5, 36, 33.5, 42, hx("#2b2f38"), 0.4)
    for a in (90, 210, 330):
        x = 30.5 + 2 * math.cos(math.radians(a)); y = 39 + 2 * math.sin(math.radians(a))
        pn.e(x - 1, y - 1, x + 1, y + 1, hx("#f2d21b"), ol=False)
def o_mech(pn):
    torso_base(pn, hx("#b9c4d2"), hx("#8e9bae"), hx("#6f7c90"), hx("#3a4250"), hx("#ff4d5e"))
    pn.e(28.5, 37, 32.5, 41, hx("#5ef0ff"), 0.6)
def o_hero(pn):
    torso_base(pn, hx("#2f5fd6"), None, belt=hx("#ffd84a"), buckle=hx("#e8202a"))
    pn.p([(27, 36), (34, 36), (30.5, 42)], hx("#ffd84a"), 0.6)
def o_agent(pn):
    torso_base(pn, hx("#1b1d2a"), None, belt=None)
    pn.p([(27.5, 31.5), (33.5, 31.5), (31.5, 45), (29.5, 45)], hx("#ffffff"), 0.5)
    pn.p([(30, 32.5), (31, 32.5), (31.3, 40), (30.5, 41.5), (29.7, 40)], hx("#c0392b"), 0.3)
def o_kurta(pn):
    torso_base(pn, hx("#f6efe0"), None, belt=None)
    pn.l([(30.5, 32), (30.5, 40)], hx("#d4a72c"), 0.7)
    for y in (34, 36.5, 39): pn.e(29.9, y - 0.6, 31.1, y + 0.6, hx("#d4a72c"), ol=False)
    pn.r(22, 46, 39, 50, hx("#f6efe0"), 1.5, 0.9)
    pn.p([(22.2, 48.5), (38.8, 48.5), (38.8, 49.5), (22.2, 49.5)], hx("#e86a1c"), ol=False)
def o_hawaii(pn):
    torso_base(pn, hx("#25b8a8"), None, belt=hx("#5a3b22"))
    r = random.Random(9)
    for _ in range(7):
        x, y = r.uniform(24, 37), r.uniform(33, 45)
        for a in range(0, 360, 72):
            pn.e(x + math.cos(math.radians(a)) - 0.8, y + math.sin(math.radians(a)) - 0.8, x + math.cos(math.radians(a)) + 0.8, y + math.sin(math.radians(a)) + 0.8, hx("#ff6fa8"), ol=False)
def o_samurai(pn):
    torso_base(pn, hx("#2a2a35"), hx("#8b1e2a"), hx("#6d1620"), hx("#d4a72c"), hx("#2a2a35"))
    for y in (36, 39, 42): pn.l([(24, y), (37, y)], hx("#d4a72c"), 0.5)
def o_street(pn):
    torso_base(pn, hx("#3b3f58"), None, belt=None)
    pn.r(25, 41, 36, 46, hx("#30344a"), 1, 0.6)
    pn.l([(29, 31), (28.5, 36)], hx("#e6e8f2"), 0.5); pn.l([(32, 31), (32.5, 36)], hx("#e6e8f2"), 0.5)
OUTFITS = {
    "army": {"draw": o_army, "label": "Army vest (now)"},
    "desert": {"draw": o_desert, "label": "Desert camo", "pants": hx("#c49a5e"), "boots": hx("#6b4a2b"), "sleeve": hx("#d9b27a")},
    "urban": {"draw": o_urban, "label": "Urban grey camo", "pants": hx("#6c727b"), "sleeve": hx("#8d939c")},
    "snow": {"draw": o_snow, "label": "Snow camo", "pants": hx("#d8dee8"), "boots": hx("#5b6573"), "sleeve": hx("#eef2f7")},
    "ninja": {"draw": o_ninja, "label": "Shadow ninja", "pants": hx("#1f2230"), "boots": hx("#14161f"), "sleeve": hx("#1f2230")},
    "jumpsuit": {"draw": o_jumpsuit, "label": "Pilot jumpsuit", "pants": hx("#e86a1c"), "sleeve": hx("#e86a1c")},
    "hazmat": {"draw": o_hazmat, "label": "Hazmat suit", "pants": hx("#f2d21b"), "boots": hx("#2b2f38"), "sleeve": hx("#f2d21b")},
    "mech": {"draw": o_mech, "label": "Mech armour", "pants": hx("#8e9bae"), "boots": hx("#3a4250"), "sleeve": hx("#b9c4d2")},
    "hero": {"draw": o_hero, "label": "Super-hero suit", "pants": hx("#2f5fd6"), "boots": hx("#e8202a"), "sleeve": hx("#2f5fd6")},
    "agent": {"draw": o_agent, "label": "Secret agent suit", "pants": hx("#1b1d2a"), "boots": hx("#0e0f16"), "sleeve": hx("#1b1d2a")},
    "kurta": {"draw": o_kurta, "label": "Festive kurta", "pants": hx("#f6efe0"), "boots": hx("#8c5a2e"), "sleeve": hx("#f6efe0")},
    "hawaii": {"draw": o_hawaii, "label": "Beach shirt", "pants": hx("#e8d6b0"), "boots": hx("#5a3b22"), "sleeve": hx("#25b8a8")},
    "samurai": {"draw": o_samurai, "label": "Samurai armour", "pants": hx("#2a2a35"), "boots": hx("#14161f"), "sleeve": hx("#8b1e2a")},
    "street": {"draw": o_street, "label": "Street hoodie", "pants": hx("#2d3a5c"), "boots": hx("#e6e8f2"), "sleeve": hx("#3b3f58")},
}

# ================= JETPACKS =================
def j_rocket(pn):
    pn.r(19, 29, 28, 52, hx("#d6d9e0"), 4, 1.0); pn.p([(19, 33), (23.5, 25), (28, 33)], hx("#e8202a"), 0.9)
    pn.e(21, 36, 26, 41, hx("#5ec8ff"), 0.7); pn.p([(18, 46), (15, 54), (20, 51)], hx("#e8202a"), 0.8); pn.p([(29, 46), (31, 54), (27, 51)], hx("#e8202a"), 0.8)
def j_fan(pn):
    pn.r(19, 33, 29, 50, hx("#5d6474"), 2, 1.0)
    pn.e(14, 22, 34, 28, hx("#cfd6e0", 160), 0.8); pn.l([(24, 25), (24, 33)], OL, 1.0); pn.e(22.5, 23.5, 25.5, 26.5, hx("#ffd84a"), 0.6)
def j_wings(pn):
    pn.p([(26, 34), (8, 24), (6, 30), (12, 33), (5, 37), (13, 39), (8, 44), (25, 42)], hx("#c9d2de"), 0.9)
    for y in (29, 34, 39): pn.l([(24, 37), (9, y + 1)], hx("#8e9bae"), 0.5)
    pn.r(22, 33, 29, 50, hx("#6f7c90"), 2, 0.9)
def j_barrel(pn):
    pn.r(18, 31, 30, 52, hx("#8b5a2b"), 2.5, 1.0)
    for y in (35, 46): pn.r(18, y, 30, y + 1.5, hx("#55575f"), 0.3, 0.6)
    pn.l([(21, 32), (21, 51)], hx("#6d4420"), 0.6); pn.l([(27, 32), (27, 51)], hx("#6d4420"), 0.6)
def j_butterfly(pn):
    for top, col in ((True, hx("#ff4fd8", 210)), (False, hx("#4fe0ff", 210))):
        if top: pn.p([(27, 36), (12, 22), (6, 30), (14, 37)], col, 0.8)
        else: pn.p([(27, 38), (10, 42), (12, 50), (22, 45)], col, 0.8)
    pn.r(23, 33, 29, 50, hx("#30344a"), 2, 0.9)
def j_dragon(pn):
    pn.r(19, 31, 29, 51, hx("#2f7d4a"), 3, 1.0)
    for y in (33, 37, 41, 45): pn.p([(19, y), (15, y + 2), (19, y + 3)], hx("#ffd84a"), 0.6)
    pn.p([(22, 51), (17, 58), (12, 57), (19, 50)], hx("#2f7d4a"), 0.8)
def j_chrome(pn):
    for x0 in (19, 24.5):
        pn.r(x0, 30, x0 + 6, 51, hx("#e8edf5"), 3, 1.0)
        pn.r(x0 + 1, 31.5, x0 + 2.4, 48, hx("#ffffff"), 0.6, ol=False)
        pn.r(x0 + 3.5, 31.5, x0 + 5, 48, hx("#a4afbf"), 0.6, ol=False)
    pn.r(20, 39, 30, 41, hx("#2b2f38"), 0.3, 0.6)
def j_hover(pn):
    pn.r(20, 33, 29, 50, hx("#30344a"), 2, 0.9)
    for y in (52, 56):
        pn.d.ellipse([16 * K, y * K, 32 * K, (y + 3) * K], outline=hx("#5ef0ff"), width=int(1.2 * K))
def j_fireworks(pn):
    for i, x0 in enumerate((17, 21, 25)):
        col = [hx("#e8202a"), hx("#2f6fd6"), hx("#5cc45a")][i]
        pn.r(x0, 31 + i, x0 + 4, 51, col, 1, 0.8); pn.p([(x0, 31 + i), (x0 + 2, 27 + i), (x0 + 4, 31 + i)], hx("#ffd84a"), 0.6)
def j_umbrella(pn):
    pn.r(21, 34, 28, 50, hx("#5d6474"), 2, 0.9)
    pn.ch(10, 14, 38, 34, 180, 360, hx("#e8202a"), 1.0)
    for x in (17, 24, 31): pn.l([(24, 24), (x, 24)], shade(hx("#e8202a"), 0.7), 0.5)
    pn.l([(24, 24), (24, 35)], OL, 0.8)
JETS = {"twin": jet_twin, "rocket": j_rocket, "fan": j_fan, "wings": j_wings, "barrel": j_barrel, "butterfly": j_butterfly,
        "dragon": j_dragon, "chrome": j_chrome, "hover": j_hover, "fireworks": j_fireworks, "umbrella": j_umbrella}
JET_LABEL = {"twin": "Twin tanks (now)", "rocket": "Space rocket", "fan": "Heli-fan", "wings": "Metal wings", "barrel": "DIY barrel",
             "butterfly": "Neon butterfly", "dragon": "Dragon pack", "chrome": "Chrome racer", "hover": "Hover rings",
             "fireworks": "Diwali rockets", "umbrella": "Umbrella glider"}

# ================= EXTRAS =================
def x_bandolier(pn):
    pn.l([(23, 33), (37, 47)], hx("#5a3b22"), 2.0)
    for i in range(6):
        x, y = 24.5 + i * 2.2, 34.5 + i * 2.1; pn.r(x - 0.6, y - 1.6, x + 0.6, y + 0.6, hx("#d4a72c"), 0.3, 0.3)
def x_cape(pn): pn.p([(22, 32), (10, 60), (20, 64), (30, 34)], hx("#c0392b"), 1.0)
def x_scarf(pn):
    pn.r(25, 30, 37, 33.5, hx("#e8202a"), 1.2, 0.8); pn.p([(25, 31), (11, 34), (13, 36), (8, 38), (25, 34)], hx("#e8202a"), 0.8)
def x_sword(pn):
    pn.l([(13, 60), (34, 26)], hx("#cfd6e0"), 1.6); pn.l([(30, 32), (35, 23)], hx("#3a2a1a"), 1.8); pn.l([(28, 30), (33, 33)], hx("#d4a72c"), 1.2)
def x_antenna(pn):
    pn.r(15, 34, 22, 48, hx("#4e5a3a"), 1.2, 0.8); pn.l([(17, 34), (13, 18)], OL, 0.6); pn.e(12, 16.5, 14, 18.5, hx("#ff4d5e"), ol=False)
def x_pads(pn):
    pn.e(36, 30, 42, 35, hx("#3a4250"), 0.9); pn.r(23.5, 54, 29.5, 57, hx("#3a4250"), 0.8, 0.7); pn.r(30.5, 54, 36.5, 57, hx("#3a4250"), 0.8, 0.7)
def x_tags(pn):
    pn.arc(26, 29, 35, 38, 20, 160, hx("#c8ccd4"), 0.5); pn.r(29.5, 37, 31.5, 40, hx("#c8ccd4"), 0.4, 0.4)
def x_pet(pn):
    pn.e(4, 18, 12, 25, hx("#b9c4d2"), 0.8); pn.e(8, 20, 11, 23, hx("#5ef0ff"), 0.5)
    pn.l([(4, 18), (2, 15)], OL, 0.5); pn.l([(12, 18), (14, 15)], OL, 0.5)
def x_flag(pn):
    pn.l([(19, 50), (19, 14)], hx("#6b4a2b"), 0.8)
    for i, c in enumerate(["#ff9933", "#ffffff", "#138808"]): pn.r(9, 14 + i * 2.5, 19, 16.5 + i * 2.5, hx(c), 0, 0.3)
    pn.e(13, 16.4, 15, 18.4, hx("#000080", 0), 0.0, ol=False); pn.d.ellipse([13.2 * K, 16.6 * K, 14.8 * K, 18.2 * K], outline=hx("#000080"), width=max(1, int(0.3 * K)))
EXTRAS = {"bandolier": x_bandolier, "cape": x_cape, "scarf": x_scarf, "sword": x_sword, "antenna": x_antenna,
          "pads": x_pads, "tags": x_tags, "pet": x_pet, "flag": x_flag}
BACK_EXTRAS = {"cape", "scarf", "sword", "antenna", "flag"}
FRONT_EXTRAS = {"pet"}
EXTRA_LABEL = {"bandolier": "Ammo bandolier", "cape": "Hero cape", "scarf": "Flying scarf", "sword": "Katana on back",
               "antenna": "Radio backpack", "pads": "Armour pads", "tags": "Dog tags", "pet": "Drone buddy", "flag": "Back flag (India)"}

# ================= JET FLAME COLOURS =================
FLAMES = {"orange": (hx("#ff9e2c", 235), hx("#fff3b0")), "blue": (hx("#3fa9ff", 235), hx("#d8f3ff")), "green": (hx("#5cff7a", 235), hx("#eaffd8")),
          "purple": (hx("#b86bff", 235), hx("#f2e0ff")), "pink": (hx("#ff4fb0", 235), hx("#ffe0f2")), "gold": (hx("#ffd84a", 235), hx("#ffffff")),
          "none": None}
FLAME_LABEL = {"orange": "Fire orange (now)", "blue": "Plasma blue", "green": "Toxic green", "purple": "Void purple", "pink": "Candy pink", "gold": "Golden", "none": "Silent (no flame)"}

LIST = []
def add(cat, key, label, sel):
    name = f"{cat}__{key}"; render(sel, name); LIST.append({"cat": cat, "key": key, "label": label, "file": name})
for k in HELMETS: add("helmet", k, HELMET_LABEL[k], {"helmet": k})
for k in FACES: add("face", k, FACE_LABEL[k], {"face": k})
for k in OUTFITS: add("outfit", k, OUTFITS[k]["label"], {"outfit": k})
for k in JETS: add("jetpack", k, JET_LABEL[k], {"jet": k})
for k in EXTRAS: add("extra", k, EXTRA_LABEL[k], {"extra": k})
for k in FLAMES: add("flame", k, FLAME_LABEL[k], {"flame": k})
# full looks: a few complete sets to show how parts combine
SETS = {
    "commando": ("Desert commando", {"helmet": "beret", "face": "shades", "outfit": "desert", "extra": "bandolier"}),
    "shadow": ("Shadow ninja", {"helmet": "ninja", "outfit": "ninja", "jet": "dragon", "extra": "sword", "flame": "purple"}),
    "ace": ("Sky ace", {"helmet": "pilot", "outfit": "jumpsuit", "jet": "chrome", "extra": "scarf", "flame": "blue"}),
    "robo": ("Robo trooper", {"helmet": "robot", "outfit": "mech", "jet": "hover", "extra": "pet", "flame": "blue"}),
    "maharaja": ("Desi hero", {"helmet": "turban", "face": "mooch", "outfit": "kurta", "jet": "fireworks", "extra": "flag", "flame": "gold"}),
    "samurai": ("Samurai", {"helmet": "samurai", "face": "scar", "outfit": "samurai", "jet": "dragon", "extra": "sword"}),
    "spaceman": ("Spaceman", {"helmet": "astro", "outfit": "snow", "jet": "rocket", "flame": "blue"}),
    "toxic": ("Toxic squad", {"helmet": "gasmask", "outfit": "hazmat", "jet": "barrel", "flame": "green"}),
    "hero": ("Super hero", {"helmet": "classic", "face": "cyber", "outfit": "hero", "jet": "wings", "extra": "cape", "flame": "gold"}),
    "beach": ("Holiday mode", {"helmet": "cap", "face": "shades", "outfit": "hawaii", "jet": "umbrella", "flame": "pink"}),
    "agent": ("Secret agent", {"helmet": "classic", "face": "monocle", "outfit": "agent", "jet": "chrome", "extra": "tags"}),
    "viking": ("Sky viking", {"helmet": "viking", "face": "paint", "outfit": "urban", "jet": "barrel", "extra": "pads"}),
}
for k, (lab, sel) in SETS.items(): add("set", k, lab, sel)
json.dump(LIST, open(os.path.join(OUT, "list.json"), "w"))
print(len(LIST), "cards")
