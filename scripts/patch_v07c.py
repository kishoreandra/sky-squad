"""v0.7 part C: minigun, fire blaze gun, smoke gas grenade, team-damage rules, and the new sound design."""
import sys
P = "/home/claude/skysquad/main.gd"
s = open(P).read()

def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        sys.exit(f"expected {count} got {n}: {old[:100]!r}")
    s = s.replace(old, new)

# ---------- weapons ----------
rep('''	"rpg":     {"name": "ROCKET",''', '''	"minigun": {"name": "MINIGUN", "dmg": 8.0,  "rate": 0.055,"mag": 120,"spare": 240, "reload": 3.0, "spread": 0.1,   "speed": 1350.0, "pellets": 1, "life": 0.6,  "chip": 0.3,  "recoil": 1.5, "push": 0.0,   "snd": "minigun", "zooms": [1]},
	"flame":   {"name": "FIRE BLAZE", "dmg": 3.0, "rate": 0.06, "mag": 60, "spare": 120, "reload": 2.2, "spread": 0.18,  "speed": 430.0,  "pellets": 1, "life": 0.42, "chip": 0.15, "recoil": 0.5, "push": 0.0,   "snd": "flame", "zooms": [1], "special": "flame"},
	"rpg":     {"name": "ROCKET",''')
rep('''const ZOOM_MULT :=''', '''# in team games, only these can hurt your own teammates
const FF_GUNS := ["bomb", "smoke", "flame", "minigun"]
const ZOOM_MULT :=''')
rep('''	[60, 7, "gun", ["sniper", "rpg", "laser"]],''', '''	[60, 7, "gun", ["sniper", "rpg", "laser", "minigun"]],''')
rep('''	[42, 20, "gun", ["ak47", "shotgun", "smg"]], [78, 20, "gun", ["ak47", "shotgun", "smg"]],''', '''	[42, 20, "gun", ["ak47", "shotgun", "smg", "flame"]], [78, 20, "gun", ["ak47", "shotgun", "smg", "flame"]],
	[38, 20, "smoke", []], [82, 20, "smoke", []],''')
rep('''	[50, 28, "gun", ["rpg", "ak47", "net"]], [70, 28, "gun", ["rpg", "ak47", "net"]],''', '''	[50, 28, "gun", ["rpg", "ak47", "net", "minigun"]], [70, 28, "gun", ["rpg", "ak47", "net", "flame"]],''')
rep('''"likes": ["shotgun", "uzi", "smg", "shock"]''', '''"likes": ["shotgun", "uzi", "smg", "shock", "flame"]''')
rep('''"likes": ["rpg", "shotgun", "net"]''', '''"likes": ["rpg", "shotgun", "net", "minigun"]''')
rep('''"likes": ["ak47", "magnum"]''', '''"likes": ["ak47", "magnum", "minigun"]''')

# player + bullet fields
rep('\tvar actor := false\n', '\tvar actor := false\n\tvar spin := 0.0\n\tvar burn_t := 0.0\n\tvar burn_by = null\n\tvar smokes := 0\n\tvar snd_t := -9.0\n\tvar cough_t := -9.0\n\tvar whiz_t := -9.0\n\tvar sizzle_t := -9.0\n')
rep('''"pick": "", "zoom": false, "bomb": false}
	var prev := {}''', '''"pick": "", "zoom": false, "bomb": false, "smoke": false}
	var prev := {}''')
rep('''	var net := false
	var gun := ""
''', '''	var net := false
	var flame := false
	var max_life := 1.0
	var gun := ""
''')
rep('''"down": false, "pick": "", "zoom": false, "bomb": false}''', '''"down": false, "pick": "", "zoom": false, "bomb": false, "smoke": false}''')
rep('var corpses: Array = []\n', 'var corpses: Array = []\nvar clouds: Array = []\n')
rep('''	p.bombs = 0
	p.stun_t = 0.0''', '''	p.bombs = 0
	p.smokes = 0
	p.burn_t = 0.0
	p.spin = 0.0
	p.stun_t = 0.0''')
rep('''	corpses.clear()
	feed.clear()
	players.clear()''', '''	corpses.clear()
	clouds.clear()
	feed.clear()
	players.clear()''')
rep('''	for arr in [bullets, grenades_list, parts, pickups, blocks, corpses, feed, tracers]:''', '''	for arr in [bullets, grenades_list, parts, pickups, blocks, corpses, feed, tracers, clouds]:''')

# textures + sounds
rep('''"hand", "knife", "timebomb", "net_overlay"]:''', '''"hand", "knife", "timebomb", "net_overlay", "smoke", "flame"]:''')
rep('''"laser", "beep", "slash"]:''', '''"laser", "beep", "slash",
			"kill", "death", "suicide", "arm", "rack", "hiss", "cough", "spin", "minigun", "flame", "sizzle", "heart", "whiz", "splash", "tick", "crown", "spawn"]:''')

# team damage rule
rep('''	if src != null and src != p and not enemy(src, p):
		return''', '''	if src != null and src != p and not enemy(src, p) and not FF_GUNS.has(gun):
		return''')

# deaths: kill / death / suicide / team-kill sounds (only the two people involved hear them)
rep('''	if k != null and k != p:
		k.kills += 1''', '''	var team_kill: bool = k != null and k != p and cfg.mode == "team" and k.side == p.side
	if team_kill:
		entry.k = k.pname
		entry.kc = k.color
		entry.gun = p.last_gun
		entry.note = "team kill"
		me_fx(k, "big", "TEAM KILL!")
		me_fx(k, "snd", ["suicide", -4.0])
		me_fx(p, "snd", ["death", -2.0])
	elif k != null and k != p:
		me_fx(k, "snd", ["kill", -5.0])
		me_fx(p, "snd", ["death", -2.0])
		k.kills += 1''')
rep('''	else:
		entry.note = {"water": "drowned", "crush": "got crushed"}.get(p.last_cause, "blew up")''', '''	else:
		entry.note = {"water": "drowned", "crush": "got crushed", "gas": "choked", "fire": "burned"}.get(p.last_cause, "blew up")
		var own: bool = k == p or (k == null and p.last_cause == "blast")
		me_fx(p, "snd", ["suicide" if own else "death", -3.0])''')

# respawn whoosh (not at match start, the gun rack plays then)
rep('''	p.protect_t = S.protect
	p.posture = "stand"''', '''	p.protect_t = S.protect
	if t > 0.5:
		me_fx(p, "snd", ["spawn", -8.0])
	p.posture = "stand"''')

# fire: flame stream
rep('''	elif special == "shock":
		shock_arc(p, mz, p.aim, d.dmg)
	else:''', '''	elif special == "shock":
		shock_arc(p, mz, p.aim, d.dmg)
	elif special == "flame":
		for i in 2:
			var fa: float = p.aim + randf_range(-0.5, 0.5) * d.spread
			var fb := Bullet.new()
			var fsp: float = d.speed * randf_range(0.8, 1.15)
			fb.x = mz.x
			fb.y = mz.y
			fb.vx = cos(fa) * fsp + p.vx * 0.5
			fb.vy = sin(fa) * fsp + p.vy * 0.5
			fb.life = d.life * randf_range(0.8, 1.1)
			fb.max_life = fb.life
			fb.dmg = d.dmg
			fb.chip = d.chip
			fb.owner = p
			fb.gun = "flame"
			fb.flame = true
			bullets.append(fb)
	else:''')
rep('''	play_l(d.snd, mz, (-1.0 if wt == "ak47" else -4.0) if is_me(p) else -6.0)''', '''	if wt == "flame":
		if t - p.snd_t > 0.3 or t < p.snd_t:
			p.snd_t = t
			play_l("flame", mz, -3.0 if is_me(p) else -7.0, 0.05)
	else:
		play_l(d.snd, mz, (-1.0 if wt == "ak47" else (-6.0 if wt == "minigun" else -4.0)) if is_me(p) else -7.0)''')

# update_player: minigun spin-up, heavy walk, smoke throw, burning, splash
rep('''	var target: float = inp.mx * S.move_speed * (0.55 if p.in_water else 1.0) * post_mul''', '''	var cw0 = p.slots[p.cur]
	if cw0 != null and cw0.type == "minigun":
		post_mul *= 0.72
	var target: float = inp.mx * S.move_speed * (0.55 if p.in_water else 1.0) * post_mul''')
rep('''	p.in_water = c.y > water_y''', '''	var was_water := p.in_water
	p.in_water = c.y > water_y
	if p.in_water and not was_water and t > 0.5:
		play("splash", c, -4.0)''')
rep('''	if inp.shoot and w != null and p.reload_t <= 0 and p.fire_cd <= 0 and p.stun_t <= 0:''', '''	var mini: bool = w != null and w.type == "minigun"
	if mini and inp.shoot and p.reload_t <= 0 and p.stun_t <= 0 and w.mag > 0:
		if p.spin <= 0.01:
			play("spin", c, -5.0 if is_me(p) else -9.0)
		p.spin = minf(1.0, p.spin + dt / 0.45)
	else:
		p.spin = maxf(0.0, p.spin - dt / 0.6)
	if inp.shoot and w != null and p.reload_t <= 0 and p.fire_cd <= 0 and p.stun_t <= 0 and (not mini or p.spin >= 1.0 or w.mag == 0):''')
rep('''	if inp.melee and not pv.get("melee", false) and p.melee_cd <= 0:''', '''	if inp.get("smoke", false) and not pv.get("smoke", false) and p.smokes > 0 and p.g_cd <= 0:
		p.smokes -= 1
		p.g_cd = 0.7
		var gsm := Grenade.new()
		var spm := shoulder(p)
		gsm.x = spm.x
		gsm.y = spm.y
		gsm.vx = cos(p.aim) * 480 + p.vx * 0.4
		gsm.vy = sin(p.aim) * 480 + p.vy * 0.3
		gsm.fuse = 1.3
		gsm.kind = "smoke"
		gsm.owner = p
		grenades_list.append(gsm)
		play("throw", c, -8.0)
	if p.burn_t > 0:
		p.burn_t -= dt
		if p.in_water:
			p.burn_t = 0.0
		hurt(p, 5.0 * dt, p.burn_by, "fire", "flame")
		if t - p.sizzle_t > 0.7 or t < p.sizzle_t:
			p.sizzle_t = t
			me_fx(p, "snd", ["sizzle", -6.0])
	if inp.melee and not pv.get("melee", false) and p.melee_cd <= 0:''')

# pickups
rep('''	if pk.type == "grenade":
		if p.grenades < S.max_grenades:''', '''	if pk.type == "smoke":
		if p.smokes < 2:
			p.smokes += 1
			return true
		return false
	if pk.type == "grenade":
		if p.grenades < S.max_grenades:''')
rep('''	if k.type == "grenade":
		tex_c("grenade", cpos + Vector2(-5, 0), Vector2(12, 14))''', '''	if k.type == "smoke":
		tex_c("smoke", cpos, Vector2(12, 16))
		txt("SMOKE", cpos + Vector2(0, -12), 8, Color.WHITE, 1, 3)
		return
	if k.type == "grenade":
		tex_c("grenade", cpos + Vector2(-5, 0), Vector2(12, 14))''')

# bullets: flames drift and burn; minigun and flames can hit teammates; near-miss whizz
rep('''		b.life -= dt
		var dead := b.life <= 0
		var steps := 3''', '''		b.life -= dt
		var dead := b.life <= 0
		if b.flame:
			b.vx *= pow(0.2, dt)
			b.vy = b.vy * pow(0.2, dt) - 70.0 * gsign() * dt
		elif not b.rocket and not b.net:
			for hp2 in players:
				if hp2.alive and not hp2.bot and hp2 != b.owner and enemy(b.owner, hp2) and t - hp2.whiz_t > 0.35:
					var hd := Vector2(b.x, b.y).distance_to(head_pos(hp2))
					if hd < 46 and hd > 14:
						hp2.whiz_t = t
						me_fx(hp2, "snd", ["whiz", -7.0])
		var steps := 3''')
rep('''				if b.rocket:
					explode(b.x - b.vx * 0.01, b.y - b.vy * 0.01, S.rocket_radius, S.rocket_dmg, b.owner, "rpg")
				else:
					damage_tile''', '''				if b.rocket:
					explode(b.x - b.vx * 0.01, b.y - b.vy * 0.01, S.rocket_radius, S.rocket_dmg, b.owner, "rpg")
				elif b.flame:
					damage_tile(floori(b.x / T), floori(b.y / T), b.chip)
				else:
					damage_tile''')
rep('''				if p == b.owner or not p.alive or not enemy(b.owner, p):
					continue
				if in_body(p, Vector2(b.x, b.y)):
					dead = true
					if b.rocket:''', '''				if p == b.owner or not p.alive or not (enemy(b.owner, p) or FF_GUNS.has(b.gun)):
					continue
				if in_body(p, Vector2(b.x, b.y)):
					dead = true
					if b.flame:
						hurt(p, b.dmg, b.owner, "fire", "flame")
						if p.protect_t <= 0:
							p.burn_t = 2.5
							p.burn_by = b.owner
					elif b.rocket:''')

# grenades: bomb arming chirp, smoke canister releases gas
rep('''			if g.stuck:
				g.fuse -= dt''', '''			if g.stuck:
				if g.beep_t > 0.9:
					g.beep_t = 0.3
				g.fuse -= dt''')
s = s.replace('''			g.vx *= -0.4
			if g.kind == "bomb":
				g.stuck = true''', '''			g.vx *= -0.4
			if g.kind == "bomb":
				if not g.stuck:
					play("arm", Vector2(g.x, g.y), -2.0, 0.0)
				g.stuck = true''')
s = s.replace('''			g.vy *= -0.35
			g.vx *= 0.7
			if g.kind == "bomb":
				g.stuck = true''', '''			g.vy *= -0.35
			g.vx *= 0.7
			if g.kind == "bomb":
				if not g.stuck:
					play("arm", Vector2(g.x, g.y), -2.0, 0.0)
				g.stuck = true''')
rep('''		if g.fuse <= 0:
			if g.kind == "bomb":
				explode(g.x, g.y, 120.0, 115.0, g.owner, "bomb")''', '''		if g.fuse <= 0:
			if g.kind == "smoke":
				clouds.append({"x": g.x, "y": g.y, "t": 7.0, "owner": g.owner})
				play("hiss", Vector2(g.x, g.y), -1.0)
				grenades_list.remove_at(i)
				continue
			if g.kind == "bomb":
				explode(g.x, g.y, 120.0, 115.0, g.owner, "bomb")''')
rep('''func update_pickups(dt: float) -> void:''', '''func cloud_fx(cl: Dictionary, dt: float) -> void:
	var k: float = clampf(cl.t / 1.5, 0.0, 1.0)
	if randf() < dt * 16.0 * k:
		add_part(cl.x + randf_range(-80, 80), cl.y + randf_range(-55, 40), randf_range(-12, 12), randf_range(-14, 4), 2.4, Color(0.7, 0.78, 0.66, 0.42), 40, -0.004, "smoke", 96)

func update_clouds(dt: float) -> void:
	for i in range(clouds.size() - 1, -1, -1):
		var cl: Dictionary = clouds[i]
		cl.t -= dt
		if cl.t <= 0:
			clouds.remove_at(i)
			continue
		cloud_fx(cl, dt)
		for p in players:
			if not p.alive or p == cl.owner:
				continue
			if center(p).distance_to(Vector2(cl.x, cl.y)) < 105:
				hurt(p, 7.0 * dt, cl.owner, "gas", "smoke")
				if t - p.cough_t > 1.3 or t < p.cough_t:
					p.cough_t = t
					me_fx(p, "snd", ["cough", -3.0])
					if not p.bot:
						pass
				p.vx *= pow(0.6, dt)

func update_pickups(dt: float) -> void:''')
rep('''	update_grenades(dt)
	update_blocks(dt)''', '''	update_grenades(dt)
	update_clouds(dt)
	update_blocks(dt)''')

# drawing: flames, smoke canister, burning players, minigun barrels blur
rep('''	for b in bullets:
		if b.net:''', '''	for b in bullets:
		if b.flame:
			var fage := clampf(1.0 - b.life / maxf(0.05, b.max_life), 0.0, 1.0)
			var fsz := 10.0 + fage * 32.0
			draw_texture_rect(tex.flame, Rect2(b.x - fsz / 2, b.y - fsz / 2, fsz, fsz), false, Color(1, 1 - fage * 0.4, 1 - fage * 0.7, 0.95 - fage * 0.65))
			continue
		if b.net:''')
rep('''	for g in grenades_list:
		if g.kind == "bomb":''', '''	for g in grenades_list:
		if g.kind == "smoke":
			draw_set_transform_matrix(wt * Transform2D(g.rot, Vector2.ONE, 0.0, Vector2(g.x, g.y)))
			draw_texture_rect(tex.smoke, Rect2(-6, -8, 12, 16), false)
			draw_set_transform_matrix(wt)
			continue
		if g.kind == "bomb":''')
rep('''	if p.stun_t > 0:
		for i in 3:''', '''	if p.burn_t > 0:
		for i in 4:
			var fo := Vector2(sin(time_s * 11.0 + i * 1.7) * 7.0, -6.0 * gs - i * 6.0 * gs + sin(time_s * 17.0 + i) * 3.0)
			var fs2 := 16.0 + 6.0 * sin(time_s * 13.0 + i * 2.0)
			draw_texture_rect(tex.flame, Rect2(c + fo - Vector2(fs2, fs2) / 2, Vector2(fs2, fs2)), false, Color(1, 1, 1, 0.85))
	if p.stun_t > 0:
		for i in 3:''')
rep('''	if p.muzzle_t > 0 and gun != "rpg" and not ["laser", "shock", "net"].has(gun):''', '''	if gun == "minigun" and p.spin > 0.05:
		for bi in 5:
			var by: float = (4.6 + 1.9 * bi - m.grip[1]) * gd
			var fl: float = 0.5 + 0.5 * sin(time_s * 70.0 * p.spin + bi * 1.3)
			draw_line(Vector2((25.0 - m.grip[0]) * gd, by), Vector2((45.0 - m.grip[0]) * gd, by), Color(0.85, 0.88, 0.95, 0.55 * fl * p.spin), 1.2)
	if p.muzzle_t > 0 and gun != "rpg" and not ["laser", "shock", "net", "flame"].has(gun):''')

# kill feed / death card words
rep('''{"grenade": "BOOM", "rpg": "BOOM", "bomb": "BOOM", "melee": "KNIFE"}''', '''{"grenade": "BOOM", "rpg": "BOOM", "bomb": "BOOM", "melee": "KNIFE", "smoke": "GAS"}''')
rep('''{"grenade": "GRENADE", "rpg": "ROCKET", "bomb": "TIME BOMB", "melee": "KNIFE", "shock": "SHOCK"}''', '''{"grenade": "GRENADE", "rpg": "ROCKET", "bomb": "TIME BOMB", "melee": "KNIFE", "shock": "SHOCK", "smoke": "SMOKE GAS"}''')
rep('''	var note: String = {"water": "You drowned", "crush": "A falling rock got you"}.get(me.last_cause, "Your own blast got you")''', '''	var note: String = {"water": "You drowned", "crush": "A falling rock got you", "fire": "You burned", "gas": "The gas got you"}.get(me.last_cause, "Your own blast got you")''')

# controls: smoke key + button
rep('''	inp.bomb = key(KEY_B) or btn_held.has("BOMB")''', '''	inp.bomb = key(KEY_B) or btn_held.has("BOMB")
	inp.smoke = key(KEY_C) or btn_held.has("SMOKE")''')
rep('''		if me.bombs > 0:
			out.append({"n": "BOMB", "p": Vector2(bx + inward * r * 2.5, sh * 0.47), "r": r * 0.85})''', '''		if me.bombs > 0:
			out.append({"n": "BOMB", "p": Vector2(bx + inward * r * 2.5, sh * 0.47), "r": r * 0.85})
		if me.smokes > 0:
			out.append({"n": "SMOKE", "p": Vector2(bx + inward * r * 2.5, sh * 0.64), "r": r * 0.85})''')
rep('''			"BOMB":
				tex_c("timebomb", b.p + Vector2(0, -3 * u), Vector2(20, 15) * u)''', '''			"SMOKE":
				tex_c("smoke", b.p + Vector2(0, -3 * u), Vector2(13, 17) * u)
				txt("%d" % me.smokes, b.p + Vector2(b.r * 0.55, b.r * 0.7), 11 * u, C_INK, 1, 3 * u)
			"BOMB":
				tex_c("timebomb", b.p + Vector2(0, -3 * u), Vector2(20, 15) * u)''')
rep('''"Keyboard: A/D W S, mouse, E Q Z G B F."''', '''"Keyboard: A/D W S, mouse, E Q Z G B C F."''')

# bots throw smoke sometimes
rep('''	inp.grenade = false
	inp.bomb = false
	inp.melee = false''', '''	inp.grenade = false
	inp.bomb = false
	inp.smoke = false
	inp.melee = false''')
rep('''		if b.bombs > 0 and d < 260 and randf() < dt * 0.4:
			inp.bomb = true''', '''		if b.bombs > 0 and d < 260 and randf() < dt * 0.4:
			inp.bomb = true
		if b.smokes > 0 and d < 320 and randf() < dt * 0.35:
			inp.smoke = true''')

# ---------- LAN sync ----------
rep('''			inp.bomb = bool(a[11])''', '''			inp.bomb = bool(a[11])
			inp.smoke = a.size() > 12 and bool(a[12])''')
rep('''i2.down, i2.pick, i2.zoom, i2.bomb])''', '''i2.down, i2.pick, i2.zoom, i2.bomb, i2.smoke])''')
rep('const PF_N := 29', 'const PF_N := 32')
rep('''			p.hs, p.best, p.mk, p.bk, p.lstreak])''', '''			p.hs, p.best, p.mk, p.bk, p.lstreak, p.spin, maxf(p.burn_t, 0.0), p.smokes])''')
rep('''		p.lstreak = int(pf[o + 28])''', '''		p.lstreak = int(pf[o + 28])
		p.spin = pf[o + 29]
		p.burn_t = pf[o + 30]
		p.smokes = int(pf[o + 31])''')
rep('''		b.append_array([x.x, x.y, x.vx, x.vy, 1.0 if x.rocket else (2.0 if x.net else 0.0)])''', '''		b.append_array([x.x, x.y, x.vx, x.vy, 1.0 if x.rocket else (2.0 if x.net else (3.0 if x.flame else 0.0)), x.life, x.max_life])''')
rep('''	for j in range(0, bb.size(), 5):''', '''	for j in range(0, bb.size(), 7):''')
rep('''		b.net = bb[j + 4] == 2.0
		bullets.append(b)''', '''		b.net = bb[j + 4] == 2.0
		b.flame = bb[j + 4] == 3.0
		b.life = bb[j + 5]
		b.max_life = bb[j + 6]
		bullets.append(b)''')
rep('''1.0 if x.kind == "bomb" else 0.0, 1.0 if x.stuck else 0.0])''', '''{"bomb": 1.0, "smoke": 2.0}.get(x.kind, 0.0), 1.0 if x.stuck else 0.0])''')
rep('''		g.kind = "bomb" if gg[j + 6] == 1.0 else "frag"''', '''		g.kind = "bomb" if gg[j + 6] == 1.0 else ("smoke" if gg[j + 6] == 2.0 else "frag")''')
rep('''	var d := {"t": t, "wy": water_y, "g": g_dir, "pf": pf,''', '''	var cl := PackedFloat32Array()
	for x in clouds:
		cl.append_array([x.x, x.y, x.t])
	var d := {"t": t, "wy": water_y, "g": g_dir, "cl": cl, "pf": pf,''')
rep('''	if d.has("feed"):
		feed = d.feed''', '''	if d.has("feed"):
		feed = d.feed
	clouds.clear()
	var cla: PackedFloat32Array = d.get("cl", PackedFloat32Array())
	for j in range(0, cla.size(), 3):
		clouds.append({"x": cla[j], "y": cla[j + 1], "t": cla[j + 2], "owner": null})''')
rep('const PK_TYPES := ["gun", "drop", "health", "grenade", "bomb"]', 'const PK_TYPES := ["gun", "drop", "health", "grenade", "bomb", "smoke"]')
# client: move flames, gas puffs
rep('''	for b in bullets:
		b.x += b.vx * dt
		b.y += b.vy * dt''', '''	for cl in clouds:
		cl.t -= dt
		cloud_fx(cl, dt)
	for b in bullets:
		if b.flame:
			b.life -= dt
			b.vx *= pow(0.2, dt)
			b.vy = b.vy * pow(0.2, dt) - 70.0 * gsign() * dt
		b.x += b.vx * dt
		b.y += b.vy * dt''')

# ---------- sounds that live only on your own phone ----------
rep('''func anim_tick(delta: float) -> void:''', '''var heart_t := 0.0
var fuel_beep_t := 0.0
var last_tick_sec := -1
var was_leader_me := false

func local_sounds(delta: float) -> void:
	if anim_skip or players.is_empty() or my_idx >= players.size() or state != "play":
		return
	var me: Player = players[my_idx]
	heart_t -= delta
	if me.alive and me.hp < 30 and heart_t <= 0:
		heart_t = 0.55 + clampf(me.hp / 30.0, 0.0, 1.0) * 0.4
		play_l("heart", null, -3.0, 0.0)
	fuel_beep_t -= delta
	if me.alive and me.jet_on and me.fuel < 18 and fuel_beep_t <= 0:
		fuel_beep_t = 0.45
		play_l("beep", null, -16.0, 0.0)
	var left := match_time - t
	if left <= 10.0 and left > 0.0:
		var sec := ceili(left)
		if sec != last_tick_sec:
			last_tick_sec = sec
			play_l("tick", null, -8.0 if sec > 3 else -2.0, 0.0)
	var lead = current_leader()
	var me_lead: bool = lead == me
	if me_lead and not was_leader_me and t > 1.0:
		play_l("crown", null, -7.0, 0.0)
	was_leader_me = me_lead

func anim_tick(delta: float) -> void:''')
rep('''	if state == "play" or state == "paused":
		intro_t += delta''', '''	if state == "play" or state == "paused":
		intro_t += delta
		local_sounds(delta)''')
rep('''		me_was_alive = true
		peek_t = 0.0''', '''		me_was_alive = true
		was_leader_me = false
		last_tick_sec = -1
		play_l("rack", null, -3.0, 0.0)
		peek_t = 0.0''')

open(P, "w").write(s)
print("ok")
