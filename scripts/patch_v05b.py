p = '/home/claude/skysquad/main.gd'
s = open(p).read()
def rep(a, b, count=1):
    global s
    n = s.count(a)
    assert n == count, (n, a[:110])
    s = s.replace(a, b)

# ---- settings (saved on device) ----
rep('''var tiles := PackedByteArray()
var thp := PackedFloat32Array()''', '''var cfg := {
	"mode": "ffa", "bots": 5, "skill": "normal", "minutes": 5, "event_every": 60,
	"ev_water": true, "ev_roof": true, "ev_brk": true, "ev_flip": false, "zones": false,
	"fire_mode": "auto", "sticks": "floating", "stick_size": 1.0, "btn_size": 1.0, "opacity": 0.7,
	"left_handed": false, "aim_sens": "medium", "vibration": true, "sound": true,
}
const MATCH_ROWS := [
	["mode", "Game mode", ["ffa", "team"], ["Free for all", "Teams"]],
	["bots", "Bots", [1, 2, 3, 4, 5], ["1", "2", "3", "4", "5"]],
	["skill", "Bot skill", ["easy", "normal", "hard"], ["Easy", "Normal", "Hard"]],
	["minutes", "Match length", [3, 5, 10], ["3 min", "5 min", "10 min"]],
	["event_every", "Map event every", [45, 60, 90], ["45 sec", "60 sec", "90 sec"]],
	["ev_water", "Rising water", [true, false], ["On", "Off"]],
	["ev_roof", "Falling rocks", [true, false], ["On", "Off"]],
	["ev_brk", "Breaking ground", [true, false], ["On", "Off"]],
	["ev_flip", "Antigravity flip", [false, true], ["Off", "On"]],
	["zones", "Gravity zones", [false, true], ["Off", "On"]],
]
const CONTROL_ROWS := [
	["fire_mode", "Shooting", ["auto", "button"], ["Aim stick fires", "Fire button"]],
	["sticks", "Joysticks", ["floating", "fixed"], ["Follow thumb", "Fixed place"]],
	["stick_size", "Joystick size", [0.85, 1.0, 1.2], ["Small", "Medium", "Large"]],
	["btn_size", "Button size", [0.85, 1.0, 1.2], ["Small", "Medium", "Large"]],
	["opacity", "Controls see-through", [0.4, 0.7, 1.0], ["Light", "Medium", "Solid"]],
	["left_handed", "Left-handed", [false, true], ["Off", "On"]],
	["aim_sens", "Aim sensitivity", ["low", "medium", "high"], ["Low", "Medium", "High"]],
	["vibration", "Vibration", [true, false], ["On", "Off"]],
	["sound", "Sound", [true, false], ["On", "Off"]],
]
var ui_btns: Array = []
var match_time := 300.0
var event_every := 60.0
var pause_rect := Rect2()

var tiles := PackedByteArray()
var thp := PackedFloat32Array()''')
rep('''func _ready() -> void:
	randomize()''', '''func load_cfg() -> void:
	var f := ConfigFile.new()
	if f.load("user://settings.cfg") == OK:
		for k in cfg.keys():
			cfg[k] = f.get_value("s", k, cfg[k])
	apply_cfg()

func save_cfg() -> void:
	var f := ConfigFile.new()
	for k in cfg.keys():
		f.set_value("s", k, cfg[k])
	f.save("user://settings.cfg")
	apply_cfg()

func apply_cfg() -> void:
	AudioServer.set_bus_mute(0, not cfg.sound)

func aim_rate(mouse: bool) -> float:
	var m: float = {"low": 0.65, "medium": 1.0, "high": 1.6}.get(cfg.aim_sens, 1.0)
	return (S.mouse_turn if mouse else S.aim_turn) * m

func enemy(a, b) -> bool:
	if a == null or b == null or a == b:
		return false
	return cfg.mode != "team" or a.side != b.side

func make_style(style: String) -> Dictionary:
	var st: Dictionary = STYLES[style].duplicate()
	match cfg.skill:
		"easy":
			st.react += 0.3
			st.err *= 1.7
			st.turn *= 0.7
			st.nade *= 0.6
		"hard":
			st.react = maxf(0.15, st.react - 0.1)
			st.err *= 0.7
			st.turn *= 1.25
	return st

func _ready() -> void:
	randomize()
	load_cfg()''')
rep('''"cloud0", "cloud1", "cloud2", "glow", "fireball", "smoke", "flash", "grenade", "medkit", "leg", "jetpack", "hand"]:''',
    '''"cloud0", "cloud1", "cloud2", "glow", "fireball", "smoke", "flash", "grenade", "medkit", "leg", "jetpack", "hand", "knife", "timebomb", "net_overlay"]:''')
rep('''"throw", "land", "warn", "crumble", "melee"]:''', '''"throw", "land", "warn", "crumble", "melee", "smg", "shock", "net", "laser", "beep", "slash"]:''')
rep('''	if autotest or shot_at >= 0:
		return
	Input.vibrate_handheld(ms)''', '''	if autotest or shot_at >= 0 or not cfg.vibration:
		return
	Input.vibrate_handheld(ms)''')
# zones switch
rep('''func zone_at(px: float, py: float):
	for z in zones:''', '''func zone_at(px: float, py: float):
	if not cfg.zones:
		return null
	for z in zones:''')
rep('''func draw_zones() -> void:
	for z in zones:''', '''func draw_zones() -> void:
	if not cfg.zones:
		return
	for z in zones:''')
# spawn by team
rep('''	var pick := 0 if far[0] >= far[1] else 1
	if randf() < 0.25:
		pick = 1 - pick''', '''	var pick := 0 if far[0] >= far[1] else 1
	if randf() < 0.25:
		pick = 1 - pick
	if cfg.mode == "team":
		pick = p.side''')
# match setup from settings
rep('''	next_event = S.event_every''', '''	match_time = cfg.minutes * 60.0
	event_every = float(cfg.event_every)
	next_event = event_every''')
rep('''	for i in NAMES.size():
		var p := Player.new()
		p.id = i
		p.pname = NAMES[i]
		p.team = TEAMS[i]
		p.color = TEAM_COL[i]
		p.bot = i > 0
		p.style = BOT_STYLE[i]
		p.prev = p.inp.duplicate()
		players.append(p)''', '''	for i in 1 + int(cfg.bots):
		var p := Player.new()
		p.id = i
		p.pname = NAMES[i]
		p.team = TEAMS[i]
		p.color = TEAM_COL[i]
		p.bot = i > 0
		p.style = BOT_STYLE[i]
		p.st = make_style(p.style)
		p.side = i
		if cfg.mode == "team":
			p.side = i % 2
			if i > 0:
				p.team = "blue" if p.side == 0 else "red"
				p.color = TEAM_COL[1] if p.side == 0 else TEAM_COL[2]
		p.prev = p.inp.duplicate()
		players.append(p)''')
rep('''next_event += S.event_every''', '''next_event += event_every''')
rep('''	if ev == null and t >= next_event - S.event_warn and t < S.match_time - S.event_warn:''', '''	if ev == null and t >= next_event - S.event_warn and t < match_time - S.event_warn and not enabled_events().is_empty():''')
rep('''func pick_event() -> String:
	var names := []
	for n in EVENTS.keys():
		if n != last_event:
			names.append(n)
	return names[randi() % names.size()]''', '''func enabled_events() -> Array:
	var out := []
	for n in EVENTS.keys():
		if cfg.get("ev_" + n, true):
			out.append(n)
	return out

func pick_event() -> String:
	var all := enabled_events()
	var names := []
	for n in all:
		if n != last_event:
			names.append(n)
	if names.is_empty():
		names = all
	return names[randi() % names.size()]''')
rep('''	if t >= S.match_time:''', '''	if t >= match_time:''')
rep('''	var left: float = maxf(0.0, S.match_time - t)''', '''	var left: float = maxf(0.0, match_time - t)''')
# ---- friendly fire off in teams ----
rep('''	if p.protect_t > 0 and cause != "water":
		return
	p.hp -= amt''', '''	if p.protect_t > 0 and cause != "water":
		return
	if src != null and src != p and not enemy(src, p):
		return
	p.hp -= amt''')
rep('''		for o in players:
			if o == b or not o.alive:
				continue
			var oc := center(o)
			var d := (oc - c).length()
			var seen: bool''', '''		for o in players:
			if o == b or not o.alive or not enemy(b, o):
				continue
			var oc := center(o)
			var d := (oc - c).length()
			var seen: bool''')
rep('''	var st: Dictionary = STYLES[b.style]
	var c := center(b)
	var eye''', '''	var st: Dictionary = b.st
	var c := center(b)
	var eye''')
rep('''			for p in players:
				if p == b.owner or not p.alive:
					continue
				if in_body(p, Vector2(b.x, b.y)):''', '''			for p in players:
				if p == b.owner or not p.alive or not enemy(b.owner, p):
					continue
				if in_body(p, Vector2(b.x, b.y)):''')
rep('''			if o != p and o.alive and in_body(o, pos):
				victim = o''', '''			if o != p and o.alive and enemy(p, o) and in_body(o, pos):
				victim = o''')
rep('''		for o in players:
			if o == p or not o.alive:
				continue
			var oc := center(o)
			if absf(oc.y - c.y) < 40''', '''		for o in players:
			if o == p or not o.alive or not enemy(p, o):
				continue
			var oc := center(o)
			if absf(oc.y - c.y) < 40''')
# ---- new fire types ----
rep('''	if w.type == "sniper":
		hitscan(p, mz, p.aim + randf_range(-0.5, 0.5) * d.spread * spread_mul, d.dmg, d.chip)
	else:''', '''	var special: String = d.get("special", "")
	if w.type == "sniper":
		hitscan(p, mz, p.aim + randf_range(-0.5, 0.5) * d.spread * spread_mul, d.dmg, d.chip)
	elif special == "laser":
		laser_beam(p, mz, p.aim + randf_range(-0.5, 0.5) * d.spread * spread_mul, d.dmg, d.chip)
	elif special == "shock":
		shock_arc(p, mz, p.aim, d.dmg)
	else:''')
rep('''			b.life = d.life; b.dmg = d.dmg; b.chip = d.chip; b.owner = p; b.rocket = w.type == "rpg"; b.gun = w.type
			bullets.append(b)''', '''			b.life = d.life; b.dmg = d.dmg; b.chip = d.chip; b.owner = p; b.rocket = w.type == "rpg"; b.gun = w.type
			b.net = special == "net"
			bullets.append(b)''')
rep('''	if w.type != "rpg":
		var q := add_part(mz.x''', '''	if w.type != "rpg" and special == "":
		var q := add_part(mz.x''')
rep('''	else:
		for i in 6:
			add_part(mz.x - cos(p.aim) * 40''', '''	elif w.type == "rpg":
		for i in 6:
			add_part(mz.x - cos(p.aim) * 40''')
rep('''	tracers.append({"a": from, "b": end, "t": 0.22})
''', '''	tracers.append({"a": from, "b": end, "t": 0.22, "max": 0.22, "kind": "line"})

func laser_beam(p: Player, from: Vector2, a: float, dmg: float, chip: float) -> void:
	var dir := Vector2(cos(a), sin(a))
	var pos := from
	var seg := from
	var bounces := 0
	for i in 500:
		var prev := pos
		pos += dir * 4.0
		if pos.x < 0 or pos.x > WW or pos.y < 0 or pos.y > WH:
			break
		if solid_pt(pos.x, pos.y):
			damage_tile(floori(pos.x / T), floori(pos.y / T), chip)
			sparks(pos.x, pos.y, Color("#7ff4ff"), 6)
			tracers.append({"a": seg, "b": pos, "t": 0.25, "max": 0.25, "kind": "laser"})
			if bounces >= 1:
				return
			bounces += 1
			if solid_pt(prev.x, pos.y):
				dir.y = -dir.y
			else:
				dir.x = -dir.x
			pos = prev
			seg = pos
			continue
		for o in players:
			if o != p and o.alive and enemy(p, o) and in_body(o, pos):
				var head: bool = pos.distance_to(head_pos(o)) < 9.5
				sparks(pos.x, pos.y, Color("#7ff4ff"), 10)
				play("hit", pos, -8.0)
				hurt(o, dmg * (1.4 if head else 1.0), p, "shot", "laser", head)
				tracers.append({"a": seg, "b": pos, "t": 0.25, "max": 0.25, "kind": "laser"})
				return
	tracers.append({"a": seg, "b": pos, "t": 0.25, "max": 0.25, "kind": "laser"})

func shock_arc(p: Player, from: Vector2, a: float, dmg: float) -> void:
	var best = null
	var bd := 240.0
	for o in players:
		if o != p and o.alive and enemy(p, o):
			var oc := center(o)
			var v := oc - from
			var d := v.length()
			if d < bd and absf(wrapf(v.angle() - a, -PI, PI)) < 0.5 and los(from, oc):
				bd = d
				best = o
	var end := from + Vector2(cos(a), sin(a)) * 200.0
	if best != null:
		end = center(best)
		best.stun_t = 0.9
		hurt(best, dmg, p, "shock", "shock")
		sparks(end.x, end.y, Color("#9ff6ff"), 10)
	else:
		var pos := from
		for i in 50:
			pos += Vector2(cos(a), sin(a)) * 4.0
			if solid_pt(pos.x, pos.y):
				break
		end = pos
		sparks(end.x, end.y, Color("#9ff6ff"), 4)
	tracers.append({"a": from, "b": end, "t": 0.2, "max": 0.2, "kind": "zig"})
''')
# net bullets hit
rep('''					if b.rocket:
						explode(b.x, b.y, S.rocket_radius, S.rocket_dmg, b.owner, "rpg")
					else:
						var head: bool''', '''					if b.rocket:
						explode(b.x, b.y, S.rocket_radius, S.rocket_dmg, b.owner, "rpg")
					elif b.net:
						p.net_t = 3.5
						p.vx *= 0.3
						p.vy *= 0.3
						play("net", Vector2(b.x, b.y), -4.0)
						hurt(p, b.dmg, b.owner, "shot", "net")
					else:
						var head: bool''')
# ---- status effects, bombs, knife, switch, near bubble in update_player ----
rep('''	var post_mul: float = S.crouch_speed if p.posture == "crouch" else (S.crawl_speed if p.posture == "prone" else 1.0)
	var target: float = inp.mx * S.move_speed * (0.55 if p.in_water else 1.0) * post_mul''', '''	var post_mul: float = S.crouch_speed if p.posture == "crouch" else (S.crawl_speed if p.posture == "prone" else 1.0)
	p.stun_t -= dt
	p.net_t -= dt
	if p.net_t > 0 or p.stun_t > 0:
		inp.fly = false
		post_mul *= 0.35 if p.net_t > 0 else 0.15
		if p.stun_t > 0 and randf() < 0.4:
			sparks(c.x + randf_range(-10, 10), c.y + randf_range(-18, 14), Color("#9ff6ff"), 1, 80)
	var target: float = inp.mx * S.move_speed * (0.55 if p.in_water else 1.0) * post_mul''')
rep('''	p.melee_anim -= dt
	p.muzzle_t -= dt''', '''	p.melee_anim -= dt
	p.switch_t -= dt
	p.muzzle_t -= dt''')
rep('''		var stepmax: float = (S.mouse_turn if mouse_aiming() else S.aim_turn) * dt''', '''		var stepmax: float = aim_rate(mouse_aiming()) * dt''')
rep('''	if inp.shoot and w != null and p.reload_t <= 0 and p.fire_cd <= 0:''', '''	if not p.bot:
		near_gun(p)
	if inp.shoot and w != null and p.reload_t <= 0 and p.fire_cd <= 0 and p.stun_t <= 0:''')
rep('''		var found = floor_gun(p)
		if found != null:
			var opts := pickup_opts(p, found)''', '''		var found = floor_gun(p) if p.bot else near_gun(p)
		if found != null:
			var opts := pickup_opts(p, found)''')
rep('''	if inp.swap and not pv.get("swap", false) and p.slots[1 - p.cur] != null:
		p.cur = 1 - p.cur
		p.reload_t = 0.0''', '''	if inp.swap and not pv.get("swap", false) and p.slots[1 - p.cur] != null:
		p.cur = 1 - p.cur
		p.reload_t = 0.0
		p.switch_t = 0.22''')
rep('''		play("throw", c, -8.0)
	if inp.melee and not pv.get("melee", false) and p.melee_cd <= 0:
		p.melee_cd = 0.55
		p.melee_anim = 0.18
		play("melee", c, -8.0)''', '''		play("throw", c, -8.0)
	if inp.bomb and not pv.get("bomb", false) and p.bombs > 0 and p.g_cd <= 0:
		p.bombs -= 1
		p.g_cd = 0.7
		var gb := Grenade.new()
		var spb := shoulder(p)
		gb.x = spb.x; gb.y = spb.y
		gb.vx = cos(p.aim) * 330 + p.vx * 0.3
		gb.vy = sin(p.aim) * 330 + p.vy * 0.2
		gb.fuse = 4.5
		gb.kind = "bomb"
		gb.owner = p
		grenades_list.append(gb)
		play("throw", c, -8.0)
	if inp.melee and not pv.get("melee", false) and p.melee_cd <= 0:
		p.melee_cd = 0.55
		p.melee_anim = 0.28
		play("slash", c, -6.0)''')
rep('''func floor_gun(p: Player):''', '''func near_gun(p: Player):
	var c := center(p)
	var best = null
	var bd := 48.0
	for k in pickups:
		if k.type == "gun" or k.type == "drop":
			var d := Vector2(k.x + k.w / 2.0 - c.x, (k.y + k.h / 2.0 - c.y) * 0.7).length()
			if d < bd:
				bd = d
				best = k
	if best != null:
		p.near_k = best
		p.near_t = t
		return best
	if p.near_k != null and pickups.has(p.near_k) and t - p.near_t < 1.6 and Vector2(p.near_k.x - c.x, p.near_k.y - c.y).length() < 150:
		return p.near_k
	return null

func floor_gun(p: Player):''')
rep('''	if pk.type == "grenade":
		if p.grenades < S.max_grenades:''', '''	if pk.type == "bomb":
		if p.bombs < 2:
			p.bombs += 1
			return true
		return false
	if pk.type == "grenade":
		if p.grenades < S.max_grenades:''')
rep('''	p.grenades = S.start_grenades
	p.reload_t = 0.0''', '''	p.grenades = S.start_grenades
	p.bombs = 0
	p.stun_t = 0.0
	p.net_t = 0.0
	p.reload_t = 0.0''')
# bots throw bombs and choose new weapons
rep('''		if b.grenades > 0 and d < 420 and d > 120 and randf() < dt * st.nade * (1.2 if not visible else 0.35):''', '''		if b.bombs > 0 and d < 260 and randf() < dt * 0.4:
			inp.bomb = true
		if b.grenades > 0 and d < 420 and d > 120 and randf() < dt * st.nade * (1.2 if not visible else 0.35):''')
rep('''	inp.shoot = false
	inp.grenade = false
	inp.melee = false''', '''	inp.shoot = false
	inp.grenade = false
	inp.bomb = false
	inp.melee = false''')
rep('''		if b.goal == null and b.grenades < 2 and b.target == null:
			b.goal = nearest_pickup(b, ["grenade"], 700)''', '''		if b.goal == null and b.grenades < 2 and b.target == null:
			b.goal = nearest_pickup(b, ["grenade", "bomb"], 700)''')
rep('''		var reach := 1000.0 if (w != null and w.type == "sniper") else 760.0''', '''		var reach := 1000.0 if (w != null and w.type == "sniper") else 760.0
		if w != null and w.type == "shock":
			reach = 220.0
		elif w != null and w.type == "net":
			reach = 520.0''')
# ---- time bomb physics ----
rep('''	for i in range(grenades_list.size() - 1, -1, -1):
		var g: Grenade = grenades_list[i]
		var z = zone_at(g.x, g.y)''', '''	for i in range(grenades_list.size() - 1, -1, -1):
		var g: Grenade = grenades_list[i]
		if g.kind == "bomb":
			g.beep_t -= dt
			if g.beep_t <= 0:
				g.beep_t = 0.15 + g.fuse * 0.18
				play("beep", Vector2(g.x, g.y), -4.0, 0.0)
			if g.stuck:
				g.fuse -= dt
				if g.fuse <= 0:
					explode(g.x, g.y, 120.0, 115.0, g.owner, "bomb")
					grenades_list.remove_at(i)
				continue
		var z = zone_at(g.x, g.y)''')
rep('''		var nx := g.x + g.vx * dt
		if solid_pt(nx, g.y):
			g.vx *= -0.4
		else:
			g.x = nx''', '''		var nx := g.x + g.vx * dt
		if solid_pt(nx, g.y):
			g.vx *= -0.4
			if g.kind == "bomb":
				g.stuck = true
		else:
			g.x = nx''')
rep('''		var ny := g.y + g.vy * dt
		if solid_pt(g.x, ny):
			g.vy *= -0.35
			g.vx *= 0.7
		else:
			g.y = ny''', '''		var ny := g.y + g.vy * dt
		if solid_pt(g.x, ny):
			g.vy *= -0.35
			g.vx *= 0.7
			if g.kind == "bomb":
				g.stuck = true
				g.y = floori(ny / T) * T - 5.0 if g.vy <= 0 else g.y
		else:
			g.y = ny''')
open(p, 'w').write(s)
print("b ok")
