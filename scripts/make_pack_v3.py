"""Sky Squad sound pack v3: more and better options for the sounds not picked yet,
plus new map and game sounds. Same sources and tools as v2 (Kenney CC0, Freedoom BSD)."""
import os, sys, json
here = os.path.dirname(__file__)
src = open(os.path.join(here, "make_pack_v2.py")).read()
exec(src.split("# ================= DEATH CRIES")[0])   # helpers, loaders, save()
import re as _re
flame = fd("dsflame")
for _name in ("jet", "whoosh"):
    _m = _re.search(r"\ndef " + _name + r"\(.*?(?=\nsave\()", src, _re.S)
    exec(_m.group(0))

KM = "/home/claude/snd/Starter-Kit-Match-3/"
KC = "/home/claude/snd/Starter-Kit-City-Builder/"
KU = "/home/claude/snd/kenney-ui-audio/"
def ki(n): return load(find(KI, n + ".wav"))
def ku(n): return load(find(KU, n + ".wav"))
def ko(base, n): return load(find(base, n + ".ogg"))
def sweep_sin(s, f0, f1, curve=1.0):
    k = np.linspace(0, 1, int(SR * s)) ** curve
    return np.sin(2 * np.pi * np.cumsum(f0 * (f1 / f0) ** k) / SR)
def tone(s, f, d=0.15, a=0.002): return np.sin(2 * np.pi * f * t(s)) * env(s, a, d)
def bell(s, f, d=0.4):
    return (tone(s, f, d) + 0.5 * tone(s, f * 2.76, d * 0.4) + 0.25 * tone(s, f * 5.4, d * 0.2))
def whoosh_fast(s, lo, hi, seed=0): return whoosh(s, lo, hi, seed)

# ---------- JUMP (old one was not good) ----------
save("jump", "A", "Jetpack kick-off puff", mix((whoosh(0.22, 400, 1600, 11), 0, 0.9), (thump(0.12, 160, 80, 0.03), 0, 0.5), (bp(noise(0.08), 2000, 6000) * env(0.08, 0.001, 0.02), 0, 0.3)))
save("jump", "B", "Boot scuff + hop", mix((ko(KF, "jump_a"), 0, 1.0), (thump(0.1, 140, 70, 0.025), 0, 0.4)))
save("jump", "C", "Soft hop", ko(KF, "jump_b"))
save("jump", "D", "Grunt hop (tiny 'hup')", mix((trim(excite(to_pitch(fd("dsoof"), 600), 0.2), 0.12), 0, 0.6), (ko(KF, "jump_c"), 0, 0.8)))
save("jump", "E", "Springy boost", mix((sweep_sin(0.18, 300, 900) * env(0.18, 0.003, 0.08), 0, 0.5), (whoosh(0.2, 600, 2000, 12), 0, 0.7)))

# ---------- OUT OF AMMO: no bullets / no bombs ----------
def click(s=0.02, hz=3000): return hp(noise(s), hz) * env(s, 0.0002, 0.003)
save("empty_gun", "A", "Dry trigger click-click", mix((click(), 0, 1.0), (click(0.02, 2200), 0.09, 0.8)))
save("empty_gun", "B", "Hammer on empty", mix((click(0.03, 1800), 0, 1.0), (tone(0.08, 2900, 0.02), 0, 0.2), (thump(0.05, 400, 200, 0.01), 0, 0.3)))
save("empty_gun", "C", "Switch click", trim(excite(fd("dsswtchn"), 0.3), 0.2))
save("empty_gun", "D", "Light tick", ki("tick_001"))
save("empty_throw", "A", "Locked buzz (no bombs)", ki("error_004"))
save("empty_throw", "B", "Low 'nope' blip", mix((tone(0.09, 330, 0.05), 0, 0.6), (tone(0.12, 220, 0.07), 0.1, 0.6)))
save("empty_throw", "C", "Padlock clack", mix((excite(fd("dsswtchx"), 0.3), 0, 1.0), (tone(0.15, 180, 0.05), 0.02, 0.3)))
save("empty_throw", "D", "Glitch denied", ki("glitch_002"))

# ---------- WEAPON DROP / PICK / EQUIP ----------
metal = excite(fd("dsmetal"), 0.3)
save("weapon_drop", "A", "Gun clatters on ground", mix((trim(pitch(metal, 3), 0.35), 0, 1.0), (thump(0.1, 200, 90, 0.03), 0, 0.5), (trim(pitch(metal, 7), 0.2), 0.12, 0.4)))
save("weapon_drop", "B", "Heavy thud + rattle", mix((thump(0.2, 140, 60, 0.05), 0, 0.9), (trim(pitch(metal, -2), 0.3), 0.02, 0.6)))
save("weapon_drop", "C", "Toss and slide", mix((whoosh(0.15, 500, 1500, 13), 0, 0.5), (trim(pitch(metal, 5), 0.3), 0.12, 0.8), (bp(noise(0.25), 600, 3000) * env(0.25, 0.01, 0.08), 0.18, 0.3)))
save("weapon_pick", "A", "Grab + cock (picked before)", excite(fd("dswpnup"), 0.3))
save("weapon_pick", "B", "Quick grab", mix((whoosh(0.12, 800, 2500, 14), 0, 0.6), (click(0.03, 2000), 0.08, 1.0), (click(0.02, 2800), 0.14, 0.7)))
save("weapon_pick", "C", "Bolt rack grab", excite(pitch(fd("dssgcock"), 2), 0.3))
save("weapon_equip_dual", "A", "Second gun: double cock", mix((excite(pitch(fd("dssgcock"), 5), 0.3), 0, 1.0), (excite(pitch(fd("dssgcock"), 7), 0.3), 0.22, 0.9)))
save("weapon_equip_dual", "B", "Twin slide racks", mix((excite(fd("dsdbload"), 0.3), 0, 1.0), (excite(pitch(fd("dsdbcls"), 3), 0.3), 0.18, 1.0), (bell(0.3, 1400, 0.1), 0.3, 0.15)))
save("weapon_equip_dual", "C", "Spin + click (cowboy)", mix((whoosh(0.3, 900, 2500, 15), 0, 0.6), (click(0.03, 2200), 0.28, 1.0), (click(0.03, 2600), 0.36, 1.0)))

# ---------- MENUS ----------
save("ui_click", "A", "Soft tap", ki("click_002"))
save("ui_click", "B", "Crisp click", ku("click3"))
save("ui_click", "C", "Toggle switch", ki("toggle_002"))
save("ui_click", "D", "Select blip", ki("select_003"))
save("ui_click", "E", "Military switch", trim(excite(fd("dsswtchn"), 0.3), 0.2))
save("ui_confirm", "A", "Confirm (picked before)", ki("confirmation_001"))

# ---------- KILL CONFIRM (only the killer hears) ----------
save("kill", "A", "Bright ping", ki("confirmation_002"))
save("kill", "B", "Coin + punch", mix((ko(KP, "coin"), 0, 0.8), (thump(0.15, 180, 70, 0.04), 0, 0.6)))
save("kill", "C", "Match ding", ko(KM, "tile-match"))
save("kill", "D", "Hitmarker tick-tick", mix((click(0.02, 3500), 0, 1.0), (tone(0.06, 3200, 0.015), 0, 0.3), (click(0.02, 3500), 0.07, 1.0), (tone(0.06, 3600, 0.015), 0.07, 0.3)))
save("kill", "E", "Bell + bass", mix((bell(0.6, 1568, 0.3), 0, 0.5), (thump(0.3, 120, 50, 0.08), 0, 0.8)))
save("kill", "F", "Glass ding", ki("glass_001"))

# ---------- RESPAWN ----------
save("spawn", "A", "Teleport in", trim(excite(fd("dstelept"), 0.3), 1.0))
save("spawn", "B", "Drop-pod land", mix((whoosh(0.4, 300, 1500, 16), 0, 0.7), (thump(0.3, 150, 50, 0.07), 0.35, 1.0), (bp(noise(0.3), 300, 2000) * env(0.3, 0.005, 0.08), 0.35, 0.4)))
save("spawn", "C", "Shield power-up", mix((sweep_sin(0.6, 200, 1200, 0.7) * env(0.6, 0.02, 0.35), 0, 0.5), (bell(0.6, 1760, 0.25), 0.45, 0.3)))
save("spawn", "D", "Jetpack ignition", mix((excite(fd("dspstart"), 0.3), 0, 0.7), (jet(0.6, 0.6, 0.6, 5), 0.15, 0.6)))
save("spawn", "E", "Digital appear", ki("maximize_006"))

# ---------- WATER ----------
slop = excite(fd("dsslop"), 0.3)
def bubbles(s, n=10, seed=0):
    r = np.random.default_rng(seed); out = np.zeros(int(SR * s))
    for _ in range(n):
        f0 = r.uniform(500, 1400); d = r.uniform(0.03, 0.07); at = r.uniform(0, s - 0.1)
        b = sweep_sin(d, f0, f0 * 1.8) * env(d, 0.002, d * 0.5)
        i = int(at * SR); out[i:i + len(b)] += b * r.uniform(0.3, 0.8)
    return out
save("splash", "A", "Big splash", trim(slop, 0.8))
save("splash", "B", "Splash + bubbles", mix((trim(pitch(slop, 2), 0.5), 0, 1.0), (bubbles(0.8, 12, 1), 0.15, 0.4)))
save("splash", "C", "Dive in (plunge)", mix((thump(0.2, 200, 70, 0.06), 0, 0.7), (lp(noise(0.5), 1500) * env(0.5, 0.005, 0.15), 0, 0.8), (bubbles(0.7, 8, 2), 0.2, 0.5)))
save("water_loop", "A", "Under water muffle (while in water)", mix((lp(noise(1.5), 400) * 0.7, 0, 1.0), (bubbles(1.5, 10, 3), 0, 0.25)))

# ---------- MAP BREAKING ----------
brk = ko(KP, "break")
stone = excite(fd("dsstnmov"), 0.3)
save("crumble", "A", "Rocks crumble (Kenney)", brk)
save("crumble", "B", "Stone grinding", trim(stone, 1.0))
save("crumble", "C", "Crack + rubble rain", mix((crack(0.06, 1200), 0, 1.0), (thump(0.3, 120, 45, 0.08), 0, 0.8), *[(bp(noise(0.06), 800, 4000) * env(0.06, 0.002, 0.015), 0.1 + i * 0.05 + rng.uniform(0, 0.03), 0.4) for i in range(12)]))
save("crumble", "D", "Deep earth rumble", mix((lp(noise(1.2), 180, 3) * env(1.2, 0.2, 0.5) * 2.5, 0, 1.0), (brk, 0.5, 0.5)))
save("crate_break", "A", "Wood crate smash", mix((excite(fd("dspunch"), 0.3), 0, 0.6), (brk, 0, 0.8), (bp(noise(0.3), 600, 3000) * env(0.3, 0.002, 0.06), 0.03, 0.4)))
save("crate_break", "B", "Planks snap", mix(*[(bp(noise(0.05), 1000, 5000) * env(0.05, 0.001, 0.012), i * 0.04, 1.0 - i * 0.15) for i in range(5)], (thump(0.15, 180, 80, 0.04), 0, 0.6)))

# ---------- BULLET HITS ----------
save("hit", "A", "Body thump", mix((excite(fd("dspunch"), 0.2), 0, 0.6), (thump(0.12, 200, 90, 0.03), 0, 0.6)))
save("hit", "B", "Armour ping", mix((bell(0.25, 2200, 0.06), 0, 0.4), (click(0.02, 2500), 0, 0.8)))
save("hit", "C", "Sharp slap", mix((hp(noise(0.06), 1200) * env(0.06, 0.0005, 0.012), 0, 1.0), (thump(0.08, 300, 120, 0.02), 0, 0.5)))
save("hit", "D", "Kenney hurt blip", ko(KF, "enemy_hurt"))
save("headshot", "A", "Helmet clank", mix((bell(0.35, 1500, 0.08), 0, 0.5), (crack(0.03, 2000), 0, 0.8), (thump(0.1, 250, 100, 0.03), 0, 0.5)))
save("headshot", "B", "Bright ding", mix((bell(0.5, 2093, 0.2), 0, 0.7), (bell(0.5, 3136, 0.12), 0.0, 0.3)))

# ---------- MAP EVENTS ----------
def siren(s, lo, hi, rate):
    tt = t(s); f = lo + (hi - lo) * (0.5 + 0.5 * np.sin(2 * np.pi * rate * tt))
    x = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.4 + np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.6
    return lp(x, 3000) * np.minimum(1, tt / 0.1) * np.minimum(1, (s - tt) / 0.2)
save("ev_water", "A", "Flood siren", siren(1.6, 500, 900, 1.2))
save("ev_water", "B", "Radio alert + gushing", mix((excite(fd("dsradio"), 0.3), 0, 0.8), (lp(noise(1.4), 900) * np.minimum(1, t(1.4) / 0.6) * 0.7, 0.2, 1.0), (bubbles(1.2, 14, 4), 0.3, 0.4)))
save("ev_water", "C", "Deep horn", mix((lp(np.sign(np.sin(2 * np.pi * 110 * t(1.4))), 900) * np.minimum(1, t(1.4) / 0.05) * np.minimum(1, (1.4 - t(1.4)) / 0.3), 0, 0.6), (lp(np.sign(np.sin(2 * np.pi * 165 * t(1.4))), 900) * np.minimum(1, t(1.4) / 0.05) * np.minimum(1, (1.4 - t(1.4)) / 0.3), 0, 0.4)))
save("ev_rocks", "A", "Ceiling rumble", mix((lp(noise(1.6), 200, 3) * np.minimum(1, t(1.6) / 0.4) * 3, 0, 1.0), *[(bp(noise(0.05), 800, 4000) * env(0.05, 0.002, 0.015), 0.3 + i * 0.1, 0.3) for i in range(10)]))
save("ev_rocks", "B", "Stone grind warning", trim(pitch(stone, -3), 1.4))
save("ev_rocks", "C", "Alarm bell + rumble", mix((bell(1.2, 880, 0.4), 0, 0.4), (bell(1.2, 880, 0.4), 0.4, 0.35), (lp(noise(1.6), 200, 3) * np.minimum(1, t(1.6) / 0.4) * 2.5, 0, 1.0)))
save("ev_ground", "A", "Cracking earth", mix(*[(crack(0.05, 900) * 0.8, i * 0.12 + rng.uniform(0, 0.05), 1.0) for i in range(8)], (lp(noise(1.2), 250) * 1.5 * env(1.2, 0.2, 0.6), 0, 1.0)))
save("ev_ground", "B", "Creak and groan", mix((trim(excite(pitch(fd("dsdoropn"), -7), 0.3), 1.2), 0, 1.0), (lp(noise(1.2), 250) * env(1.2, 0.2, 0.6), 0, 0.8)))
save("ev_flip", "A", "Gravity warp (reverse whoosh)", mix((whoosh(1.0, 2500, 300, 17)[::-1].copy(), 0, 0.8), (sweep_sin(1.0, 600, 120, 0.5) * env(1.0, 0.1, 0.6), 0, 0.5)))
save("ev_flip", "B", "Sci-fi warble", mix((np.sin(2 * np.pi * np.cumsum(500 + 300 * np.sin(2 * np.pi * 7 * t(1.2))) / SR) * env(1.2, 0.05, 0.6), 0, 0.6), (ki("glitch_004"), 0.0, 0.5)))
save("ev_flip", "C", "Deep pulse", mix(*[(thump(0.3, 90, 40, 0.1), i * 0.3, 1.0 - i * 0.15) for i in range(4)], (sweep_sin(1.2, 200, 800, 1.5) * env(1.2, 0.3, 0.8), 0, 0.3)))

# ---------- MATCH FLOW ----------
def whistle(s, f=2400):
    tt = t(s); x = np.sin(2 * np.pi * np.cumsum(f * (1 + 0.02 * np.sin(2 * np.pi * 28 * tt))) / SR)
    return (x + bp(noise(s), f * 0.8, f * 1.2) * 0.4) * np.minimum(1, tt / 0.02) * np.minimum(1, (s - tt) / 0.05)
save("match_start", "A", "Gun rack + horn", mix((excite(fd("dssgcock"), 0.3), 0, 0.8), (lp(np.sign(np.sin(2 * np.pi * 220 * t(0.8))), 2000) * np.minimum(1, (0.8 - t(0.8)) / 0.15), 0.45, 0.5)))
save("match_start", "B", "Whistle blast", whistle(0.7))
save("match_start", "C", "3-2-1 beeps + go", mix((tone(0.12, 880, 0.06), 0, 0.6), (tone(0.12, 880, 0.06), 0.35, 0.6), (tone(0.12, 880, 0.06), 0.7, 0.6), (tone(0.5, 1760, 0.25), 1.05, 0.8)))
save("match_start", "D", "Confirm chime", ki("confirmation_003"))
save("match_end", "A", "Long whistle", mix((whistle(0.25), 0, 1.0), (whistle(0.25), 0.35, 1.0), (whistle(0.9), 0.7, 1.0)))
save("match_end", "B", "Victory sting", mix((bell(0.7, 784, 0.3), 0, 0.5), (bell(0.7, 988, 0.3), 0.12, 0.5), (bell(1.0, 1319, 0.45), 0.24, 0.6)))
save("match_end", "C", "Bong", ki("bong_001"))
save("tick", "A", "Clock tick", ki("tick_002"))
save("tick", "B", "Wood block", mix((bp(noise(0.04), 1500, 3000) * env(0.04, 0.0005, 0.01), 0, 1.0), (tone(0.05, 1200, 0.01), 0, 0.5)))
save("tick", "C", "Beep", tone(0.08, 1500, 0.03))
save("leader", "A", "You took the lead (rising chime)", mix((bell(0.5, 784, 0.2), 0, 0.5), (bell(0.5, 988, 0.2), 0.09, 0.5), (bell(0.7, 1319, 0.3), 0.18, 0.6)))
save("leader", "B", "Crown coin", mix((ko(KP, "coin"), 0, 1.0), (bell(0.5, 2093, 0.2), 0.08, 0.3)))
save("lost_lead", "A", "Lost the lead (falling)", mix((bell(0.4, 988, 0.15), 0, 0.5), (bell(0.6, 784, 0.25), 0.12, 0.5)))
save("item_respawn", "A", "Item appears (Freedoom)", excite(fd("dsitmbk"), 0.3))
save("item_respawn", "B", "Sparkle pop", mix(*[(bell(0.2, f, 0.06), i * 0.04, 0.3) for i, f in enumerate([1568, 2093, 2637, 3136])]))
save("heartbeat", "A", "Heartbeat (low health)", mix((thump(0.2, 70, 45, 0.06), 0, 1.0), (thump(0.2, 60, 40, 0.05), 0.2, 0.7)))
save("low_fuel", "A", "Fuel warning beeps", mix((tone(0.06, 1200, 0.03), 0, 0.5), (tone(0.06, 1200, 0.03), 0.12, 0.5)))
save("low_fuel", "B", "Engine sputter", mix(*[(trim(jet(0.12, 0.8, 0.4, 20 + i), 0.12), i * 0.18, 0.8) for i in range(3)]))

# ---------- MAP AMBIENCE (quiet loops under the game) ----------
def wind(s, lo, hi, seed, gust=0.4):
    r = np.random.default_rng(seed); n = r.uniform(-1, 1, int(SR * s))
    g = 0.6 + gust * np.sin(2 * np.pi * 0.25 * t(s)) + 0.2 * np.sin(2 * np.pi * 0.11 * t(s) + 1)
    return bp(n, lo, hi) * g
def drips(s, n, seed):
    r = np.random.default_rng(seed); out = np.zeros(int(SR * s))
    for _ in range(n):
        f0 = r.uniform(900, 2200); b = sweep_sin(0.05, f0, f0 * 1.6) * env(0.05, 0.001, 0.015)
        i = int(r.uniform(0, s - 0.1) * SR); out[i:i + len(b)] += b * r.uniform(0.3, 1.0)
    return room(out, 0.5, 2.5)[:int(SR * s)]
save("amb_sky", "A", "Sky Islands: high wind", wind(4.0, 200, 1200, 30), 0.5)
save("amb_sky", "B", "Sky Islands: breeze + birds", mix((wind(4.0, 300, 900, 31, 0.2), 0, 0.6), *[(sweep_sin(0.12, 2500, 3600) * env(0.12, 0.01, 0.05), 0.5 + i * 0.9 + rng.uniform(0, 0.3), 0.15) for i in range(4)]), 0.5)
save("amb_outpost", "A", "Outpost: desert wind + flag", mix((wind(4.0, 150, 700, 32, 0.5), 0, 0.8), (bp(noise(4.0), 1500, 3000) * (0.5 + 0.5 * np.sin(2 * np.pi * 6 * t(4.0))) * 0.1, 0, 1.0)), 0.5)
save("amb_outpost", "B", "Outpost: generator hum", mix((lp(np.sign(np.sin(2 * np.pi * 50 * t(4.0))), 300) * 0.4, 0, 1.0), (wind(4.0, 200, 800, 33, 0.3), 0, 0.5)), 0.5)
save("amb_cata", "A", "Catacombs: drips + low hum", mix((drips(4.0, 9, 34), 0, 1.0), (lp(noise(4.0), 120, 3) * 1.5, 0, 0.6)), 0.5)
save("amb_cata", "B", "Catacombs: eerie wind in tunnels", mix((wind(4.0, 150, 500, 35, 0.6), 0, 0.7), (np.sin(2 * np.pi * np.cumsum(220 + 15 * np.sin(2 * np.pi * 0.3 * t(4.0))) / SR) * 0.05, 0, 1.0), (drips(4.0, 4, 36), 0, 0.6)), 0.5)
save("torch", "A", "Torch crackle (near torches)", mix((trim(fd("dsflame"), 1.0) * 0.3, 0, 1.0), *[(bp(noise(0.02), 2000, 6000) * env(0.02, 0.001, 0.004), rng.uniform(0, 1.5), 0.4) for i in range(18)]), 0.5)

json.dump(LIST, open(os.path.join(OUT, "list.json"), "w"), indent=0)
print(len(LIST), "clips")
