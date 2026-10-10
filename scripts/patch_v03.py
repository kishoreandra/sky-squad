import sys
p = '/home/claude/skysquad/main.gd'
s = open(p).read()
def rep(a, b, count=1):
    global s
    n = s.count(a)
    assert n == count, (n, a[:80])
    s = s.replace(a, b)

rep('# Sky Squad - Arc Light Studio. Playtest build 0.2', '# Sky Squad - Arc Light Studio. Playtest build 0.3')
rep('const VERSION := "0.2"', 'const VERSION := "0.3"')
rep('"aim_turn": 13.0, "view_h": 390.0, "view_h_scope": 600.0, "headshot": 1.6,',
    '"aim_turn": 10.0, "view_h": 390.0, "headshot": 1.6, "crouch_speed": 0.45, "crawl_speed": 0.3,')
# zoom levels per gun
rep('"snd": "magnum"}', '"snd": "magnum", "zooms": [1]}')
rep('"snd": "uzi"}', '"snd": "uzi", "zooms": [1]}')
rep('"snd": "ak47"}', '"snd": "ak47", "zooms": [1, 2]}')
rep('"snd": "shotgun"}', '"snd": "shotgun", "zooms": [1]}')
rep('"snd": "sniper"}', '"snd": "sniper", "zooms": [1, 2, 4, 6]}')
rep('"snd": "rpg"}', '"snd": "rpg", "zooms": [1, 2]}')
rep('''const T := 32
''', '''const ZOOM_MULT := {1: 1.0, 2: 1.35, 4: 1.8, 6: 2.3}
const POSTURE := {"stand": Vector2(20, 42), "crouch": Vector2(20, 30), "prone": Vector2(40, 18)}
const T := 32
''')
# player fields
rep('''	var melee_anim := 0.0
	var say := ""''', '''	var melee_anim := 0.0
	var posture := "stand"
	var air_t := 0.0
	var draw_aim := 0.0
	var leg_b := 0.0
	var leg_f := 0.0
	var reload_k := 0.0
	var crouch_roll := 1.0
	var say := ""''')
rep('''var inp := {"mx": 0.0, "fly": false, "shoot": false, "swap": false, "grenade": false, "melee": false, "reload": false, "aim": 0.0}''',
    '''var inp := {"mx": 0.0, "fly": false, "shoot": false, "swap": false, "grenade": false, "melee": false, "reload": false, "aim": 0.0, "down": false, "pick": false, "zoom": false}''')
rep('''func new_slot(type: String, mag: int, spare: int) -> Dictionary:
	return {"type": type, "mag": mag, "spare": spare}''', '''func new_slot(type: String, mag: int, spare: int) -> Dictionary:
	return {"type": type, "mag": mag, "spare": spare, "zi": 0}

func zoom_level(p: Player) -> int:
	var w = p.slots[p.cur]
	if w == null:
		return 1
	var zs: Array = WD[w.type].zooms
	return zs[clampi(w.zi, 0, zs.size() - 1)]

func set_posture(p: Player, post: String) -> bool:
	if p.posture == post:
		return true
	var sz: Vector2 = POSTURE[post]
	var nx := p.x + p.w / 2.0 - sz.x / 2.0
	var ny := p.y
	if gsign() > 0:
		ny = p.y + p.h - sz.y
	if rect_hits(nx, ny, sz.x, sz.y):
		return false
	p.x = nx
	p.y = ny
	p.w = sz.x
	p.h = sz.y
	p.posture = post
	return true

func head_pos(p: Player) -> Vector2:
	var c := center(p)
	var face := 1.0 if cos(p.aim) >= 0 else -1.0
	match p.posture:
		"crouch":
			return c + Vector2(1.0 * face, -9.0 * gsign())
		"prone":
			return c + Vector2(11.0 * face, 2.0 * gsign())
	return c + Vector2(1.0 * face, -15.0 * gsign())''')
# spawn resets posture
rep('''	p.x = best.x
	p.y = best.y
	p.vx = 0.0
	p.vy = 0.0
	p.hp = S.hp_max''', '''	p.posture = "stand"
	p.w = 20.0
	p.h = 42.0
	p.x = best.x
	p.y = best.y
	p.vx = 0.0
	p.vy = 0.0
	p.hp = S.hp_max''')
# shoulder by posture
rep('''func shoulder(p: Player) -> Vector2:
	var c := center(p)
	var face := 1.0 if cos(p.aim) >= 0 else -1.0
	return c + Vector2(1.0 * face, -6.0 * gsign())''', '''func shoulder(p: Player) -> Vector2:
	var c := center(p)
	var face := 1.0 if cos(p.aim) >= 0 else -1.0
	match p.posture:
		"crouch":
			return c + Vector2(1.0 * face, 0.0)
		"prone":
			return c + Vector2(2.0 * face, 2.0 * gsign())
	return c + Vector2(1.0 * face, -6.0 * gsign())''')
rep('''	var spread_mul := 1.0 if p.on_ground else 1.35''', '''	var spread_mul := 1.0 if p.on_ground else 1.35
	if p.posture == "crouch":
		spread_mul = 0.6
	elif p.posture == "prone":
		spread_mul = 0.35''')
# headshot detection by head point
rep('''						var head: bool = (b.y - p.y) < 13 if gsign() > 0 else (p.y + p.h - b.y) < 13''',
    '''						var head: bool = Vector2(b.x, b.y).distance_to(head_pos(p)) < 9.5''')
# movement: postures
rep('''	p.in_water = c.y > water_y
	var target: float = inp.mx * S.move_speed * (0.55 if p.in_water else 1.0)''', '''	p.in_water = c.y > water_y
	# sit / crawl
	if inp.down and not pv.get("down", false) and p.on_ground:
		var w0 = p.slots[p.cur]
		if p.posture == "stand":
			set_posture(p, "crouch")
		elif p.posture == "crouch" and w0 != null and w0.type == "sniper":
			set_posture(p, "prone")
		else:
			set_posture(p, "stand")
	if inp.fly and p.posture != "stand":
		if not set_posture(p, "stand"):
			inp.fly = false
	if p.on_ground:
		p.air_t = 0.0
	else:
		p.air_t += dt
		if p.air_t > 0.25 and p.posture != "stand":
			set_posture(p, "stand")
	if p.posture == "prone":
		var wp = p.slots[p.cur]
		if wp == null or wp.type != "sniper":
			set_posture(p, "crouch")
	if p.in_water and p.posture != "stand":
		set_posture(p, "stand")
	c = center(p)
	var post_mul: float = S.crouch_speed if p.posture == "crouch" else (S.crawl_speed if p.posture == "prone" else 1.0)
	var target: float = inp.mx * S.move_speed * (0.55 if p.in_water else 1.0) * post_mul''')
# walk cycle slower and aim smoothing / prone clamp / anim smoothing
rep('''	if p.on_ground:
		p.walk += absf(p.vx) * dt * 0.075''', '''	if p.on_ground:
		p.walk += absf(p.vx) * dt * (0.05 if p.posture == "stand" else 0.09)''')
rep('''		p.aim = wrapf(p.aim + clampf(diff, -stepmax, stepmax), -PI, PI)
	var w = p.slots[p.cur]''', '''		p.aim = wrapf(p.aim + clampf(diff, -stepmax, stepmax), -PI, PI)
	if p.posture == "prone":
		var face0 := 1.0 if cos(p.aim) >= 0 else -1.0
		var gs0 := gsign()
		var la0 := clampf(atan2(sin(p.aim) * gs0, cos(p.aim) * face0), -0.45, 0.3)
		p.aim = atan2(sin(la0) * gs0, cos(la0) * face0)
	animate(p, dt)
	var w = p.slots[p.cur]''')
# swap: only swap guns; pick: take the gun on the floor; zoom: cycle
rep('''	if inp.swap and not pv.get("swap", false):
		var found: Pickup = null
		for k in pickups:
			if (k.type == "gun" or k.type == "drop") and overlaps(p, k):
				found = k
				break
		if found != null:
			if not give_gun(p, found.gun, found.ammo):
				replace_current(p, found)
			remove_pickup(found)
			if p == players[0]:
				play("pickup", null, -6.0)
		elif p.slots[1 - p.cur] != null:
			p.cur = 1 - p.cur
			p.reload_t = 0.0
			if p == players[0]:
				play("swap", null, -6.0)''', '''	if inp.pick and not pv.get("pick", false):
		var found = floor_gun(p)
		if found != null:
			if not give_gun(p, found.gun, found.ammo):
				replace_current(p, found)
			remove_pickup(found)
			if p == players[0]:
				play("pickup", null, -6.0)
	if inp.swap and not pv.get("swap", false) and p.slots[1 - p.cur] != null:
		p.cur = 1 - p.cur
		p.reload_t = 0.0
		if p == players[0]:
			play("swap", null, -6.0)
	if inp.zoom and not pv.get("zoom", false) and w != null:
		var zs: Array = WD[w.type].zooms
		if zs.size() > 1:
			w.zi = (w.zi + 1) % zs.size()
			if p == players[0]:
				play("swap", null, -10.0, 0.0)''')
# helper functions inserted before bots section
rep('''# ---------------- bots ----------------''', '''func floor_gun(p: Player):
	for k in pickups:
		if (k.type == "gun" or k.type == "drop") and overlaps(p, k):
			return k
	return null

func can_auto_take(p: Player, k: Pickup) -> bool:
	for s2 in p.slots:
		if s2 == null or not has_ammo(s2) or (s2.type == k.gun and s2.spare < WD[k.gun].spare * 2):
			return true
	return false

func ease_k(rate: float, dt: float) -> float:
	return 1.0 - exp(-rate * dt)

func animate(p: Player, dt: float) -> void:
	p.draw_aim = lerp_angle(p.draw_aim, p.aim, ease_k(22.0, dt))
	var tb := 0.0
	var tf := 0.0
	match p.posture:
		"crouch":
			tb = 1.35
			tf = -0.95
		"prone":
			tb = sin(p.walk) * 0.28 * clampf(absf(p.vx) / 30.0, 0, 1)
			tf = -tb
		_:
			if p.on_ground:
				var swing := sin(p.walk) * 0.55 * clampf(absf(p.vx) / 90.0, 0, 1)
				tb = -swing
				tf = swing
			else:
				tb = -0.22 + sin(time_s * 3.0 + p.id) * 0.06
				tf = 0.32 + sin(time_s * 3.0 + p.id + 1.0) * 0.06
	p.leg_b = lerpf(p.leg_b, tb, ease_k(14.0, dt))
	p.leg_f = lerpf(p.leg_f, tf, ease_k(14.0, dt))
	p.reload_k = lerpf(p.reload_k, 1.0 if p.reload_t > 0 else 0.0, ease_k(9.0, dt))

# ---------------- bots ----------------''')
# bot posture
rep('''	if b.stuck_t > 1.3:
		b.strafe *= -1
		b.stuck_t = 0.0
		b.roam_t = 0.0
		inp.mx = b.strafe
		fly = true
	inp.fly = fly''', '''	if b.stuck_t > 1.3:
		b.strafe *= -1
		b.stuck_t = 0.0
		b.roam_t = 0.0
		inp.mx = b.strafe
		fly = true
	# sit or lie down to shoot steadier
	var want_post := "stand"
	if tg != null and visible and b.on_ground and not fly and not b.in_water:
		var tv: Vector2 = b.target_pos - c
		var dd := tv.length()
		if w != null and w.type == "sniper" and b.style == "sniper" and dd > 300 and absf(tv.y) < dd * 0.3:
			want_post = "prone"
		elif (b.style == "cautious" or b.style == "balanced" or b.style == "sniper") and dd > 260 and b.crouch_roll < 0.4:
			want_post = "crouch"
	if want_post != "stand":
		b.stuck_t = 0.0
		inp.mx = 0.0 if want_post == "prone" else inp.mx * 0.5
	if b.posture != want_post:
		if want_post == "prone" and b.posture == "stand":
			set_posture(b, "crouch")
		set_posture(b, want_post)
	inp.fly = fly''')
rep('''		b.think_t = 0.25 + randf() * 0.2''', '''		b.think_t = 0.25 + randf() * 0.2
		if randf() < 0.1:
			b.crouch_roll = randf()''')
open(p, 'w').write(s)
print("patched part 1")
