"""v0.9: new sound set wired in, one heavy gun at a time (dual small guns ok), max 3 grenades/smokes/time bombs,
weapon drop / dual-equip / no-bullets / locked sounds, grenade bounce, jetpack take-off whoosh."""
import sys
P = "/home/claude/skysquad/main.gd"
s = open(P).read()

def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        sys.exit(f"expected {count} got {n}: {old[:100]!r}")
    s = s.replace(old, new)

rep('# Sky Squad - Arc Light Studio. Playtest build 0.8', '# Sky Squad - Arc Light Studio. Playtest build 0.9')
rep('const VERSION := "0.8"', 'const VERSION := "0.9"')
rep('\tvar actor := false\n', '\tvar actor := false\n\tvar jst_t := -9.0\n')
rep('"start_grenades": 3, "max_grenades": 5,', '"start_grenades": 3, "max_grenades": 3, "max_bombs": 3, "max_smokes": 3,')
rep('''		if p.bombs < 2:''', '''		if p.bombs < S.max_bombs:''')
rep('''		if p.smokes < 2:''', '''		if p.smokes < S.max_smokes:''')
rep('''"die0", "die1", "die2", "ow0", "ow1"]:''', '''"die0", "die1", "die2", "ow0", "ow1",
			"tink", "ui_ok", "bomb_boom", "jetstart", "locked", "wdrop", "equip2"]:''')

# ---- one heavy gun at a time ----
rep('''func is_small(g: String) -> bool:''', '''const HEAVY := ["ak47", "shotgun", "sniper", "minigun", "rpg", "flame", "laser"]

func is_heavy(g: String) -> bool:
	return HEAVY.has(g)

# slot index holding a heavy gun with ammo, or -1
func heavy_slot(p: Player) -> int:
	for i in 2:
		var s2 = p.slots[i]
		if s2 != null and has_ammo(s2) and is_heavy(s2.type):
			return i
	return -1

func is_small(g: String) -> bool:''')
rep('''	for s2 in p.slots:
		if s2 == null or not has_ammo(s2):
			return []
	return ["swap", "dual"] if is_small(k.gun) else ["swap"]''', '''	if is_heavy(k.gun) and heavy_slot(p) >= 0:
		return ["swap"]
	for s2 in p.slots:
		if s2 == null or not has_ammo(s2):
			return []
	return ["swap", "dual"] if is_small(k.gun) else ["swap"]''')
rep('''	for i in 2:
		if not has_ammo(p.slots[i]):
			p.slots[i] = new_slot(type, ammo.mag, ammo.spare) if ammo != null else full_slot(type)''', '''	if is_heavy(type) and heavy_slot(p) >= 0:
		return false
	for i in 2:
		if not has_ammo(p.slots[i]):
			p.slots[i] = new_slot(type, ammo.mag, ammo.spare) if ammo != null else full_slot(type)''')
rep('''func replace_current(p: Player, pk: Pickup) -> void:
	var old = p.slots[p.cur]
	var c := center(p)
	if has_ammo(old):
		drop_gun(c.x - 12, c.y - 8, old.type, {"mag": old.mag, "spare": old.spare})
	p.slots[p.cur] = new_slot(pk.gun, pk.ammo.mag, pk.ammo.spare) if pk.ammo != null else full_slot(pk.gun)
	p.reload_t = 0.0''', '''func replace_current(p: Player, pk: Pickup) -> void:
	# a heavy gun always replaces the heavy gun you carry (only one heavy at a time)
	var hs := heavy_slot(p)
	if is_heavy(pk.gun) and hs >= 0:
		p.cur = hs
	var old = p.slots[p.cur]
	var c := center(p)
	if has_ammo(old):
		drop_gun(c.x - 12, c.y - 8, old.type, {"mag": old.mag, "spare": old.spare})
		play("wdrop", c, -6.0)
	p.slots[p.cur] = new_slot(pk.gun, pk.ammo.mag, pk.ammo.spare) if pk.ammo != null else full_slot(pk.gun)
	p.reload_t = 0.0
	p.switch_t = 0.22''')
rep('''		cur.dual = true
		cur.mag = mag_cap(cur)''', '''		cur.dual = true
		me_fx(p, "snd", ["equip2", -4.0])
		cur.mag = mag_cap(cur)''')

# ---- health has its own pickup sound ----
rep('''			if overlaps(p, k) and not human_choice and try_pickup(p, k):
				remove_pickup(k)
				me_fx(p, "snd", ["pickup", -6.0])''', '''			if overlaps(p, k) and not human_choice and try_pickup(p, k):
				remove_pickup(k)
				me_fx(p, "snd", ["health" if k.type == "health" else "pickup", -6.0])''')

# ---- no grenades / bombs / smokes left: locked sound ----
rep('''	if inp.grenade and not pv.get("grenade", false) and p.grenades > 0 and p.g_cd <= 0:''', '''	var none_left: bool = (inp.grenade and not pv.get("grenade", false) and p.grenades <= 0) or (inp.bomb and not pv.get("bomb", false) and p.bombs <= 0) or (inp.get("smoke", false) and not pv.get("smoke", false) and p.smokes <= 0)
	if none_left:
		me_fx(p, "snd", ["locked", -6.0])
	if inp.grenade and not pv.get("grenade", false) and p.grenades > 0 and p.g_cd <= 0:''')

# ---- jetpack take-off whoosh ----
rep('''	if is_me(p):
		if p.jet_on and not was_jet and not autotest and shot_at < 0:
			jet_player.play()''', '''	if p.jet_on and not was_jet and (t - p.jst_t > 0.6 or t < p.jst_t):
		p.jst_t = t
		play("jetstart", c, -8.0 if is_me(p) else -14.0, 0.05)
	if is_me(p):
		if p.jet_on and not was_jet and not autotest and shot_at < 0:
			jet_player.play()''')

# ---- grenade bounce tink ----
rep('''			g.vx *= -0.4''', '''			if absf(g.vx) > 120 and g.kind != "bomb":
				play("tink", Vector2(g.x, g.y), -8.0)
			g.vx *= -0.4''')
rep('''			g.vy *= -0.35''', '''			if absf(g.vy) > 140 and g.kind != "bomb":
				play("tink", Vector2(g.x, g.y), -8.0)
			g.vy *= -0.35''')

# ---- time bomb has its own boom ----
rep('''func explode(x: float, y: float, r: float, dmg: float, owner, gun: String) -> void:
	explode_fx(x, y, r)
	if net_role == "host":
		net_fx.append(["x", x, y, r])''', '''func explode(x: float, y: float, r: float, dmg: float, owner, gun: String) -> void:
	var es := "bomb_boom" if gun == "bomb" else "explosion"
	explode_fx(x, y, r, es)
	if net_role == "host":
		net_fx.append(["x", x, y, r, es])''')
rep('''func explode_fx(x: float, y: float, r: float) -> void:
	shake = maxf(shake, 14.0)
	play_l("explosion", Vector2(x, y), 0.0)''', '''func explode_fx(x: float, y: float, r: float, es := "explosion") -> void:
	shake = maxf(shake, 14.0)
	play_l(es, Vector2(x, y), 0.0)''')
rep('''			explode_fx(e[1], e[2], e[3])''', '''			explode_fx(e[1], e[2], e[3], e[4] if e.size() > 4 else "explosion")''')

# ---- menu: confirm sound for big moves ----
rep('''			pressed_at = time_s
			play_l("swap", null, -10.0, 0.0)''', '''			pressed_at = time_s
			play_l("ui_ok" if BIG_ACTIONS.has(b.a) else "swap", null, -6.0 if BIG_ACTIONS.has(b.a) else -10.0, 0.0)''')
open(P, "w").write(s)
print("ok")
