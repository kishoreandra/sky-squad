"""Put the user's round-1 sound picks (and safe defaults for the new hooks) into skysquad/sfx."""
import os, sys, shutil, wave
here = os.path.dirname(__file__)
src = open(os.path.join(here, "make_pack_v2.py")).read()
sys.argv = [sys.argv[0], "/tmp/claude-0/install_tmp"]
exec(src.split("# ================= DEATH CRIES")[0])
import re as _re
flame = fd("dsflame"); pistol = fd("dspistol"); rx = fd("dsrxplod")
for _name in ("jet", "whoosh", "gun", "boom"):
    _m = _re.search(r"\ndef " + _name + r"\(.*?(?=\nsave\()", src, _re.S)
    exec(_m.group(0))

SFX = "/home/claude/skysquad/sfx/"
V2 = "/tmp/claude-0/pv2/"
V3 = "/tmp/claude-0/pv3/"
def put(name, x, gain=0.9):
    x = x / (np.max(np.abs(x)) + 1e-9) * gain
    with wave.open(SFX + name + ".wav", "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())
def cp(srcfile, name):
    shutil.copy(srcfile, SFX + name + ".wav")

picks = {"death": "B", "hurt": "A", "magnum": "A", "uzi": "B", "ak47": "B", "smg": "B", "shotgun": "A", "sniper": "A",
         "rpg": "A", "laser": "B", "shock": "B", "net": "A", "flame": "B", "explosion": "B", "land": "A", "reload": "B",
         "swap": "A", "pickup": "A", "health": "A", "melee": "A", "grenade_throw": "A", "bounce": "A", "ui_confirm": "A"}
game_name = {"death": ["die0", "die1", "die2"], "hurt": ["ow0", "ow1"], "melee": ["slash"], "grenade_throw": ["throw"],
             "bounce": ["tink"], "ui_confirm": ["ui_ok"]}
for snd, opt in picks.items():
    for gname in game_name.get(snd, [snd]):
        cp(V2 + f"{snd}__{opt}.wav", gname)

# minigun: the picked "burst" is 6 shots; the game plays one per shot, so one shot of the same recipe
put("minigun", gun(pistol, 4, 0.08, 3200, 110, 0.08, 0.05, sub_g=0.5))
# time bomb: the picked clip is beep-beep-BOOM; the game beeps on its own, so only the boom
put("bomb_boom", boom(rx, -4, 1.8, 40, 1.4))
# jetpack: same recipe as the pick, made as a seamless loop (no fade in/out, cross-faded ends)
L = 2.0
raw = jet(L + 0.3, 0.8, 0.6, 1)
body = raw[int(SR * 0.2):int(SR * (0.2 + L))].copy()
tail = raw[int(SR * (0.2 + L)):int(SR * (0.2 + L + 0.1))]
fade = len(tail)
body[:fade] = body[:fade] * np.linspace(0, 1, fade) + tail * np.linspace(1, 0, fade)
put("jet", body, 0.8)
# hand push swish = the "whoosh" when you take off with the jetpack
cp(V2 + "push__B.wav", "jetstart")
# defaults for the new hooks until round 2 picks arrive
cp(V3 + "empty_gun__A.wav", "empty")
cp(V3 + "empty_throw__A.wav", "locked")
cp(V3 + "weapon_drop__A.wav", "wdrop")
cp(V3 + "weapon_equip_dual__A.wav", "equip2")
print("installed")
