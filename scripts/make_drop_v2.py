"""Weapon drop sounds, take 2: a sharp metal crack when the gun hits the ground, then it bounces
(hits come faster and softer, like a real object settling), with a ring from the metal body.
Ideas from shooters: IGI (sharp metallic crack), Counter-Strike (clanky bounce), PUBG (heavy thud),
Call of Duty (rattle and slide)."""
import os, sys
here = os.path.dirname(__file__)
src = open(os.path.join(here, "make_pack_v2.py")).read()
exec(src.split("# ================= DEATH CRIES")[0])

def modal(s, freqs, decays, amps, seed):
    r = np.random.default_rng(seed); tt = t(s); out = np.zeros(len(tt))
    for f, d, a in zip(freqs, decays, amps):
        f2 = f * r.uniform(0.97, 1.03)
        out += np.sin(2 * np.pi * f2 * tt + r.uniform(0, 6.28)) * np.exp(-tt / d) * a
    return out

def impact(strength, metal, seed, body=(950, 2380, 4150, 6300, 8100), wood=False):
    r = np.random.default_rng(seed)
    s = 0.6
    hit = hp(r.uniform(-1, 1, int(SR * 0.012)), 2500) * np.exp(-np.arange(int(SR * 0.012)) / (SR * 0.0015))
    ring = modal(s, [f * r.uniform(0.95, 1.05) for f in body], [0.09, 0.06, 0.045, 0.03, 0.02], [0.5, 0.8, 0.6, 0.4, 0.25], seed) * metal
    thud = thump(0.12, 260, 110, 0.02) * (0.9 if wood else 0.6)
    return mix((hit, 0, 1.6), (ring, 0, 0.6), (thud, 0, 1.0)) * strength

def bounce_seq(first_gap, n, decay, metal, seed, body=(950, 2380, 4150, 6300, 8100)):
    parts, at, g, gap = [], 0.0, 1.0, first_gap
    for i in range(n):
        parts.append((impact(g, metal * (0.7 + 0.3 * g), seed + i, body), at, 1.0))
        at += gap; gap *= 0.62; g *= decay
    return parts

def slide(s, seed):
    r = np.random.default_rng(seed)
    return bp(r.uniform(-1, 1, int(SR * s)), 1500, 6000) * np.linspace(1, 0, int(SR * s)) ** 1.5

# 1 IGI-style: one hard metallic crack, short bounce, settles
save("weapon_drop", "A", "IGI-style metal crack + settle", room(mix(*bounce_seq(0.11, 4, 0.45, 1.0, 1)), 0.15, 0.8))
# 2 Counter-Strike-style: clanky, more bounces, brighter
save("weapon_drop", "B", "Clanky bounce (CS-style)", room(mix(*bounce_seq(0.14, 6, 0.6, 1.3, 11, (1300, 3100, 5200, 7400, 9000))), 0.12, 0.8))
# 3 PUBG-style: heavy rifle thud, low ring, little bounce
save("weapon_drop", "C", "Heavy rifle thud (PUBG-style)", room(mix((impact(1.0, 0.5, 21, (420, 1150, 2300, 3700, 5100)), 0, 1.0), (thump(0.25, 140, 55, 0.07), 0, 1.0), (impact(0.35, 0.5, 22, (420, 1150, 2300, 3700, 5100)), 0.09, 1.0)), 0.15, 0.9))
# 4 Call of Duty-style: crack, rattle of loose parts, slide on concrete
save("weapon_drop", "D", "Crack + rattle + slide (COD-style)", room(mix(*bounce_seq(0.08, 3, 0.5, 1.0, 31), (slide(0.35, 32), 0.12, 0.35), *[(impact(0.12, 1.2, 40 + i, (2600, 4400, 6900, 8800, 10000)), 0.05 + i * 0.03, 1.0) for i in range(5)]), 0.12, 0.8))
# 5 Pistol skitter: small, light, quick tumbling
save("weapon_drop", "E", "Pistol skitter", room(mix(*bounce_seq(0.07, 5, 0.55, 1.1, 51, (1700, 3900, 6100, 8300, 9800)), (slide(0.2, 52), 0.15, 0.25)), 0.1, 0.6))
# 6 Real recording base (Freedoom metal) made sharper, with a crack on top
metal_rec = excite(fd("dsmetal"), 0.35)
save("weapon_drop", "F", "Recorded metal clang + crack", room(mix((trim(pitch(metal_rec, 4), 0.4), 0, 1.0), (impact(0.9, 1.0, 61), 0, 1.0), (impact(0.3, 1.0, 62), 0.1, 1.0)), 0.12, 0.8))

json.dump(LIST, open(os.path.join(OUT, "list.json"), "w"))
print(len(LIST))
