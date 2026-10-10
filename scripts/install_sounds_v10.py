"""Round 2 picks into skysquad/sfx. Loops get their ends cross-faded so they repeat without a click."""
import shutil, wave
import numpy as np
SFX = "/home/claude/skysquad/sfx/"
V3 = "/tmp/claude-0/pv3/"
picks = {"jump": ("A", "jump"), "empty_gun": ("A", "empty"), "empty_throw": ("A", "locked"), "ui_click": ("B", "ui_click"),
         "spawn": ("D", "spawn"), "splash": ("C", "splash"), "crumble": ("C", "crumble"), "hit": ("A", "hit"),
         "weapon_pick": ("C", "wpick"), "weapon_equip_dual": ("B", "equip2"), "ev_water": ("B", "ev_water"),
         "ev_rocks": ("C", "ev_rocks"), "ev_ground": ("B", "ev_brk"), "ev_flip": ("B", "ev_flip"), "crate_break": ("A", "crate"),
         "match_start": ("A", "rack"), "match_end": ("B", "match_end"), "tick": ("C", "tick"), "leader": ("A", "crown"),
         "lost_lead": ("A", "lost_lead"), "item_respawn": ("A", "item_respawn"), "heartbeat": ("A", "heart"), "low_fuel": ("B", "low_fuel")}
for snd, (opt, name) in picks.items():
    shutil.copy(f"{V3}{snd}__{opt}.wav", SFX + name + ".wav")

def loop(src, dst, xf=0.4, gain=0.9):
    w = wave.open(src); sr = w.getframerate()
    d = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float64) / 32768
    n = int(sr * xf)
    body = d[:-n].copy()
    body[:n] = body[:n] * np.linspace(0, 1, n) + d[-n:] * np.linspace(1, 0, n)
    body = body / (np.max(np.abs(body)) + 1e-9) * gain
    with wave.open(SFX + dst + ".wav", "wb") as o:
        o.setnchannels(1); o.setsampwidth(2); o.setframerate(sr)
        o.writeframes((body * 32767).astype(np.int16).tobytes())
loop(V3 + "water_loop__A.wav", "water_loop", 0.3)
loop(V3 + "amb_sky__A.wav", "amb_sky", 0.5)
loop(V3 + "amb_outpost__B.wav", "amb_outpost", 0.5)
loop(V3 + "amb_cata__B.wav", "amb_catacombs", 0.5)
loop(V3 + "torch__A.wav", "torch_loop", 0.3)
print("round 2 installed")
