p = '/home/claude/skysquad/main.gd'
s = open(p).read()
def rep(a, b, count=1):
    global s
    n = s.count(a)
    assert n == count, (n, a[:100])
    s = s.replace(a, b)
def cut(start_marker, end_marker, new):
    global s
    i = s.index(start_marker); j = s.index(end_marker, i)
    s = s[:i] + new + s[j:]

# ---------- player fields / input ----------
rep('''	var leg_b := 0.0
	var leg_f := 0.0''', '''	var leg_b := 0.0
	var leg_f := 0.0
	var shin_b := 0.0
	var shin_f := 0.0
	var protect_t := 0.0
	var dual_side := 0
	var reload_total := 1.0''')
rep('"down": false, "pick": false, "zoom": false}', '"down": false, "pick": "", "zoom": false}')
rep('''var pick_request := false''', '''var pick_request := ""
var bubbles: Array = []
var tracers: Array = []
var last_buzz := -9.0''')
rep('"crouch": Vector2(20, 30)', '"crouch": Vector2(20, 32)')
rep('''			return c + Vector2(1.0 * face, -9.0 * gsign())''', '''			return c + Vector2(1.0 * face, -14.0 * gsign())''')
rep('''			return c + Vector2(1.0 * face, 0.0)
		"prone":''', '''			return c + Vector2(1.0 * face, -5.0 * gsign())
		"prone":''')
rep('''	return {"type": type, "mag": mag, "spare": spare, "zi": 0}''', '''	return {"type": type, "mag": mag, "spare": spare, "zi": 0, "dual": false}

func mag_cap(w) -> int:
	return WD[w.type].mag * (2 if w.get("dual", false) else 1)

func buzz(ms: int) -> void:
	if autotest or shot_at >= 0:
		return
	Input.vibrate_handheld(ms)

func in_body(o, pos: Vector2) -> bool:
	if pos.x > o.x - 1 and pos.x < o.x + o.w + 1 and pos.y > o.y - 3 and pos.y < o.y + o.h:
		return true
	return pos.distance_to(head_pos(o)) < 9.5

func drop_gun(x: float, y: float, type: String, ammo) -> void:
	for off in [0.0, 36.0, -36.0, 72.0, -72.0, 108.0]:
		var free := true
		for k in pickups:
			if Vector2(k.x - (x + off), k.y - y).length() < 30:
				free = false
				break
		if free and not rect_hits(x + off, y, 24, 16):
			pickups.append(make_pickup("drop", x + off, y, type, ammo))
			return
	pickups.append(make_pickup("drop", x, y, type, ammo))''')

# ---------- hurt / die ----------
rep('''	if not p.alive or amt <= 0:
		return
	p.hp -= amt''', '''	if not p.alive or amt <= 0:
		return
	if p.protect_t > 0 and cause != "water":
		return
	p.hp -= amt''')
rep('''	if p == players[0] and cause != "water":
		hurt_t = 0.35''', '''	if p == players[0] and cause != "water":
		hurt_t = 0.35
		if t - last_buzz > 0.15:
			last_buzz = t
			buzz(25)''')
rep('''	var entry := {"k": "", "kc": C_INK, "v": p.pname, "vc": p.color,''', '''	var entry := {"k": "", "kc": C_INK, "v": p.pname, "vc": C_RED if p == players[0] else p.color,''')
rep('''		if k == players[0]:
			if entry.head:''', '''		if k == players[0]:
			buzz(90)
			shake = maxf(shake, 7.0)
			if entry.head:''')
rep('''	if w != null and w.type != "magnum" and w.mag + w.spare > 0:
		pickups.append(make_pickup("drop", c.x - 12, c.y - 8, w.type, {"mag": w.mag, "spare": w.spare}))
	if p == players[0]:
		jet_player.stop()''', '''	if w != null and w.type != "magnum" and w.mag + w.spare > 0:
		drop_gun(c.x - 12, c.y - 8, w.type, {"mag": w.mag, "spare": w.spare})
	if p == players[0]:
		jet_player.stop()
		buzz(300)''')

# ---------- fire: instant sniper, dual, AK punch ----------
cut('func fire(p: Player, w: Dictionary) -> void:', 'func explode(', '''func fire(p: Player, w: Dictionary) -> void:
	var d: Dictionary = WD[w.type]
	var dual: bool = w.get("dual", false)
	var face := 1.0 if cos(p.aim) >= 0 else -1.0
	var mz := muzzle_pos(p, w.type)
	if dual:
		p.dual_side = 1 - p.dual_side
		if p.dual_side == 1:
			mz += Vector2(-3.0 * face, 3.0 * gsign())
	p.protect_t = 0.0
	var spread_mul := 1.0 if p.on_ground else 1.35
	if p.posture == "crouch":
		spread_mul = 0.6
	elif p.posture == "prone":
		spread_mul = 0.35
	if dual:
		spread_mul *= 1.3
	if w.type == "sniper":
		hitscan(p, mz, p.aim + randf_range(-0.5, 0.5) * d.spread * spread_mul, d.dmg, d.chip)
	else:
		for i in d.pellets:
			var a: float = p.aim + randf_range(-0.5, 0.5) * d.spread * spread_mul
			var b := Bullet.new()
			var sp: float = d.speed * (randf_range(0.85, 1.15) if d.pellets > 1 else 1.0)
			b.x = mz.x; b.y = mz.y; b.vx = cos(a) * sp; b.vy = sin(a) * sp
			b.life = d.life; b.dmg = d.dmg; b.chip = d.chip; b.owner = p; b.rocket = w.type == "rpg"; b.gun = w.type
			bullets.append(b)
	p.recoil = d.recoil
	p.muzzle_t = 0.07
	p.shot_t = t
	if d.push > 0 and p.posture == "stand":
		p.vx -= cos(p.aim) * d.push
		p.vy -= sin(p.aim) * d.push * 0.5
	if w.type != "rpg":
		var q := add_part(mz.x - cos(p.aim) * 14, mz.y - sin(p.aim) * 14, -cos(p.aim) * 40 + randf_range(-30, 30), -120 * gsign() + randf_range(-30, 0), 0.7, Color("#d9b24a"), 2.6, 1.0)
		q.spin = randf_range(-14, 14)
		if w.type == "ak47" or w.type == "sniper":
			add_part(mz.x, mz.y, cos(p.aim) * 30, sin(p.aim) * 30 - 10, 0.5, Color(0.85, 0.85, 0.85, 0.45), 6, -0.02, "smoke", 18)
	else:
		for i in 6:
			add_part(mz.x - cos(p.aim) * 40, mz.y - sin(p.aim) * 40, -cos(p.aim) * 120 + randf_range(-40, 40), -sin(p.aim) * 120 + randf_range(-40, 40), 0.8, Color(0.8, 0.8, 0.8, 0.6), 10, -0.05, "smoke", 26)
	play(d.snd, mz, (-1.0 if w.type == "ak47" else -4.0) if p == players[0] else -6.0)
	if p == players[0]:
		shake = maxf(shake, d.recoil * (0.9 if w.type == "ak47" else 0.5))

func hitscan(p: Player, from: Vector2, a: float, dmg: float, chip: float) -> void:
	var dir := Vector2(cos(a), sin(a))
	var pos := from
	var end := from + dir * 1800.0
	for i in 450:
		pos += dir * 4.0
		if pos.x < 0 or pos.x > WW or pos.y < 0 or pos.y > WH:
			end = pos
			break
		if solid_pt(pos.x, pos.y):
			damage_tile(floori(pos.x / T), floori(pos.y / T), chip)
			sparks(pos.x, pos.y, Color("#ffe8a0"), 6)
			add_part(pos.x, pos.y, 0, -15, 0.5, Color(0.8, 0.7, 0.55, 0.5), 6, 0.0, "smoke", 18)
			end = pos
			break
		var victim = null
		for o in players:
			if o != p and o.alive and in_body(o, pos):
				victim = o
				break
		if victim != null:
			var head: bool = pos.distance_to(head_pos(victim)) < 9.5
			victim.vx += dir.x * 90
			blood(pos.x, pos.y, 8)
			play("hit", pos, -6.0)
			hurt(victim, dmg * (S.headshot if head else 1.0), p, "shot", "sniper", head)
			end = pos
			break
	tracers.append({"a": from, "b": end, "t": 0.22})

''')
# ---------- reload with dual ----------
rep('''	var d: Dictionary = WD[w.type]
	if w.mag < d.mag and w.spare > 0:
		p.reload_t = d.reload
		if p == players[0]:''', '''	var d: Dictionary = WD[w.type]
	if w.mag < mag_cap(w) and w.spare > 0:
		p.reload_t = d.reload * (1.3 if w.get("dual", false) else 1.0)
		p.reload_total = p.reload_t
		if p == players[0]:''')
rep('''	var d: Dictionary = WD[w.type]
	var take: int = mini(d.mag - w.mag, w.spare)''', '''	var take: int = mini(mag_cap(w) - w.mag, w.spare)''')
rep('''			p.fire_cd = WD[w.type].rate
''', '''			p.fire_cd = WD[w.type].rate * (0.55 if w.get("dual", false) else 1.0)
''')
rep('''		pickups.append(make_pickup("drop", c.x - 12, c.y - 8, old.type, {"mag": old.mag, "spare": old.spare}))''',
    '''		drop_gun(c.x - 12, c.y - 8, old.type, {"mag": old.mag, "spare": old.spare})''')
# sit and fire: stay seated
rep('''		if p.air_t > 0.25 and p.posture != "stand":''', '''		if p.air_t > 0.5 and p.posture != "stand":''')
# protection timer
rep('''	p.fire_cd -= dt
	p.melee_cd -= dt''', '''	p.protect_t -= dt
	p.fire_cd -= dt
	p.melee_cd -= dt''')
# aim smoothing also for mouse
rep('''	if p.bot or mouse_aiming():
		p.aim = inp.aim
	else:
		var diff := wrapf(inp.aim - p.aim, -PI, PI)
		var stepmax: float = S.aim_turn * dt''', '''	if p.bot:
		p.aim = inp.aim
	else:
		var diff := wrapf(inp.aim - p.aim, -PI, PI)
		var stepmax: float = (S.mouse_turn if mouse_aiming() else S.aim_turn) * dt''')
# pick options
rep('''	if inp.pick and not pv.get("pick", false):
		var found = floor_gun(p)
		if found != null:
			if not give_gun(p, found.gun, found.ammo):
				replace_current(p, found)
			remove_pickup(found)
			if p == players[0]:
				play("pickup", null, -6.0)''', '''	if inp.pick != "" and pv.get("pick", "") == "":
		var found = floor_gun(p)
		if found != null:
			var opts := pickup_opts(p, found)
			var opt: String = inp.pick
			if opt == "first":
				opt = opts[0] if opts.size() > 0 else ""
			if opts.has(opt):
				apply_pick(p, found, opt)
				if p == players[0]:
					play("pickup", null, -6.0)''')
rep('''		for k in pickups.duplicate():
			if overlaps(p, k) and try_pickup(p, k):''', '''		for k in pickups.duplicate():
			var human_choice: bool = not p.bot and (k.type == "gun" or k.type == "drop") and not pickup_opts(p, k).is_empty()
			if overlaps(p, k) and not human_choice and try_pickup(p, k):''')
rep('''func can_auto_take(p: Player, k: Pickup) -> bool:
	for s2 in p.slots:
		if s2 == null or not has_ammo(s2) or (s2.type == k.gun and s2.spare < WD[k.gun].spare * 2):
			return true
	return false''', '''func is_small(g: String) -> bool:
	return g == "magnum" or g == "uzi"

# what a human can choose for the gun on the floor; empty = take it automatically
func pickup_opts(p: Player, k: Pickup) -> Array:
	var cur = p.slots[p.cur]
	if cur != null and cur.type == k.gun:
		if is_small(k.gun) and not cur.get("dual", false):
			return ["dual"]
		return []
	for s2 in p.slots:
		if s2 != null and s2.type == k.gun:
			return []
	for s2 in p.slots:
		if s2 == null or not has_ammo(s2):
			return []
	return ["swap", "dual"] if is_small(k.gun) else ["swap"]

func can_auto_take(p: Player, k: Pickup) -> bool:
	return pickup_opts(p, k).is_empty()

func apply_pick(p: Player, k: Pickup, opt: String) -> void:
	if opt == "swap":
		replace_current(p, k)
	elif opt == "dual":
		var cur = p.slots[p.cur]
		if cur == null or cur.type != k.gun:
			replace_current(p, k)
			cur = p.slots[p.cur]
		cur.dual = true
		cur.mag = mag_cap(cur)
		cur.spare += (k.ammo.mag + k.ammo.spare) if k.ammo != null else WD[k.gun].spare
	remove_pickup(k)''')
# two-part legs
rep('''	var tb := 0.0
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
	p.leg_f = lerpf(p.leg_f, tf, ease_k(14.0, dt))''', '''	var tb := 0.0
	var tf := 0.0
	var sb := 0.0
	var sf := 0.0
	match p.posture:
		"crouch":
			# front knee up, back knee on the ground
			tf = -1.25
			sf = 0.05
			tb = 0.35
			sb = 1.45
		"prone":
			tb = sin(p.walk) * 0.25 * clampf(absf(p.vx) / 25.0, 0, 1)
			tf = -tb
			sb = tb
			sf = tf
		_:
			if p.on_ground:
				var k := clampf(absf(p.vx) / 80.0, 0, 1)
				var ph := p.walk
				tb = -sin(ph) * 0.5 * k
				tf = sin(ph) * 0.5 * k
				sb = tb + maxf(0.0, cos(ph)) * 0.75 * k
				sf = tf + maxf(0.0, -cos(ph)) * 0.75 * k
			else:
				tb = 0.25 + sin(time_s * 2.5 + p.id) * 0.05
				sb = 0.75
				tf = -0.35 + sin(time_s * 2.5 + p.id + 1.0) * 0.05
				sf = 0.1
	var lk := ease_k(12.0, dt)
	p.leg_b = lerpf(p.leg_b, tb, lk)
	p.leg_f = lerpf(p.leg_f, tf, lk)
	p.shin_b = lerpf(p.shin_b, sb, lk)
	p.shin_f = lerpf(p.shin_f, sf, lk)''')
rep('''func draw_leg(base: Transform2D, hip: Vector2, ang: float, col: Color) -> void:
	draw_set_transform_matrix(base * Transform2D(ang, Vector2.ONE, 0.0, hip))
	draw_texture_rect(tex.leg, Rect2(-4.5, -1, 9, 17), false, col)''', '''func draw_leg(base: Transform2D, hip: Vector2, ang: float, shin: float, col: Color) -> void:
	draw_set_transform_matrix(base * Transform2D(ang, Vector2.ONE, 0.0, hip))
	draw_texture_rect_region(tex.leg, Rect2(-4.5, -1, 9, 9.5), Rect2(0, 0, 27, 28.5), col)
	var knee := hip + Vector2(-sin(ang), cos(ang)) * 7.8
	draw_set_transform_matrix(base * Transform2D(shin, Vector2.ONE, 0.0, knee))
	draw_texture_rect_region(tex.leg, Rect2(-4.5, -0.8, 9, 9), Rect2(0, 24, 27, 27), col)''')
rep('''	draw_leg(body, Vector2(-3, 4), p.leg_b, Color(0.78, 0.78, 0.78) * tint)''', '''	draw_leg(body, Vector2(-3, 4), p.leg_b, p.shin_b, Color(0.78, 0.78, 0.78) * tint)''')
rep('''	draw_leg(body, Vector2(3, 4), p.leg_f, tint)''', '''	draw_leg(body, Vector2(3, 4), p.leg_f, p.shin_f, tint)''')
rep('''Vector2(0, (6.0 if crouch else 0.0) + bob))''', '''Vector2(0, (1.0 if crouch else 0.0) + bob))''')
# dual pistols drawing + spawn shield
rep('''	var sleeve: Color = p.color.darkened(0.2)
	draw_line(sh_pt + Vector2(-2, 0), grip, C_OUT, 6.0, true)
	draw_line(sh_pt + Vector2(-2, 0), grip, sleeve * tint, 4.0, true)''', '''	var sleeve: Color = p.color.darkened(0.2)
	var dual: bool = w != null and w.get("dual", false)
	var grip2 := sh_pt + Vector2(-3, 3) + dir * (7.0 - p.recoil * 0.5)
	var back_tgt := grip2 if dual else grip
	if p.protect_t > 0:
		tint.a = 0.45 + 0.4 * absf(sin(time_s * 10.0))
	draw_line(sh_pt + Vector2(-2, 0), back_tgt, C_OUT, 6.0, true)
	draw_line(sh_pt + Vector2(-2, 0), back_tgt, sleeve * tint, 4.0, true)
	if dual:
		draw_set_transform_matrix(body * Transform2D(gun_rot, Vector2.ONE, 0.0, grip2))
		var gsz2 := Vector2(m.size[0], m.size[1]) * gd
		draw_texture_rect(tex["gun_" + gun], Rect2(-m.grip[0] * gd, -m.grip[1] * gd, gsz2.x, gsz2.y), false, Color(0.8, 0.8, 0.8) * tint)
		draw_texture_rect(tex.hand, Rect2(-3, -3, 6, 6), false)
		draw_set_transform_matrix(body)''')
rep('''	draw_line(sh_pt + Vector2(3, 0), front_hand, C_OUT, 6.0, true)
	draw_line(sh_pt + Vector2(3, 0), front_hand, p.color * tint, 4.0, true)
	draw_texture_rect(tex.hand, Rect2(front_hand - Vector2(3, 3), Vector2(6, 6)), false)
	draw_texture_rect(tex.hand, Rect2(grip - Vector2(3, 3), Vector2(6, 6)), false)''', '''	var fh := grip if dual else front_hand
	draw_line(sh_pt + Vector2(3, 0), fh, C_OUT, 6.0, true)
	draw_line(sh_pt + Vector2(3, 0), fh, p.color * tint, 4.0, true)
	draw_texture_rect(tex.hand, Rect2(fh - Vector2(3, 3), Vector2(6, 6)), false)
	draw_texture_rect(tex.hand, Rect2(grip - Vector2(3, 3), Vector2(6, 6)), false)
	if p.protect_t > 0:
		draw_arc(Vector2(0, -4), 30, 0, TAU, 40, Color(0.5, 0.9, 1.0, 0.5), 2.0, true)''')
# bullets use body+head hit test
rep('''				if b.x > p.x - 1 and b.x < p.x + p.w + 1 and b.y > p.y - 3 and b.y < p.y + p.h:''', '''				if in_body(p, Vector2(b.x, b.y)):''')
# tracers update + draw
rep('''	for f in feed:
		f.t -= dt
	feed = feed.filter(func(f): return f.t > 0)''', '''	for f in feed:
		f.t -= dt
	feed = feed.filter(func(f): return f.t > 0)
	for tr in tracers:
		tr.t -= dt
	tracers = tracers.filter(func(tr): return tr.t > 0)''')
rep('''	draw_parts(wt)
	draw_water()''', '''	draw_parts(wt)
	for tr in tracers:
		var ta: float = clampf(tr.t / 0.22, 0, 1)
		draw_line(tr.a, tr.b, Color(1, 0.75, 0.3, 0.35 * ta), 6.0 * ta + 1.0, true)
		draw_line(tr.a, tr.b, Color(1, 1, 0.92, 0.95 * ta), 2.2 * ta + 0.6, true)
	draw_water()''')
# bubble input
rep('''		elif event.pressed and bubble_on and event.position.distance_to(bubble_pos) < bubble_r + 8 * u:
			pick_request = true
			mouse_down = false''', '''		elif event.pressed:
			for bb in bubbles:
				if event.position.distance_to(bb.pos) < bb.r + 8 * u:
					pick_request = bb.opt
					mouse_down = false''')
rep('''	if bubble_on and pos.distance_to(bubble_pos) < bubble_r + 10 * u:
		pick_request = true
		return''', '''	for bb in bubbles:
		if pos.distance_to(bb.pos) < bb.r + 10 * u:
			pick_request = bb.opt
			return''')
rep('''	inp.pick = key(KEY_E) or pick_request''', '''	var pk := pick_request
	if pk == "" and key(KEY_E):
		pk = "first"
	if pk == "" and key(KEY_V):
		pk = "dual"
	inp.pick = pk''')
rep('''	pick_request = false
	zoom_request = false''', '''	pick_request = ""
	zoom_request = false''')
cut('func draw_bubble(me: Player) -> void:', 'func draw_hud() -> void:', '''func draw_bubble(me: Player) -> void:
	var k = floor_gun(me)
	if k == null:
		return
	var opts := pickup_opts(me, k)
	if opts.is_empty():
		return
	var r := 28.0 * u * (1.0 + 0.04 * sin(time_s * 5.0))
	var pc := w2s(center(me))
	var mid := Vector2(pc.x, maxf(pc.y - 80 * u, 70 * u))
	var desk := not (touch_mode or OS.has_feature("mobile"))
	for i in opts.size():
		var opt: String = opts[i]
		var pos := mid + Vector2((i - (opts.size() - 1) / 2.0) * (r * 2.0 + 14 * u), 0)
		draw_colored_polygon(PackedVector2Array([pos + Vector2(-8 * u, r * 0.8), pos + Vector2(8 * u, r * 0.8), pos + Vector2((mid.x - pos.x) * 0.3, r + 14 * u)]), Color(1, 1, 1, 0.95))
		draw_circle(pos, r + 2 * u, Color(0.1, 0.12, 0.2, 0.9))
		draw_circle(pos, r, Color(1, 1, 1, 0.95) if opt == "swap" else Color(1, 0.92, 0.6, 0.97))
		if opt == "dual":
			gun_icon(k.gun, pos + Vector2(-4 * u, -7 * u), r * 1.25)
			gun_icon(k.gun, pos + Vector2(4 * u, 1 * u), r * 1.25)
		else:
			gun_icon(k.gun, pos + Vector2(0, -3 * u), r * 1.55)
		var lab := "DUAL" if opt == "dual" else "SWAP"
		if desk:
			lab += " (" + ("V" if opt == "dual" else "E") + ")"
		txt(lab, pos + Vector2(0, r * 0.66), 9 * u, Color("#1b1d2a"), 1)
		bubbles.append({"pos": pos, "r": r, "opt": opt})
	txt(WD[k.gun].name, mid + Vector2(0, -r - 8 * u), 11 * u, C_ARC, 1, 3 * u)

''')
rep('''func draw_hud() -> void:
	bubble_on = false''', '''func draw_hud() -> void:
	bubbles.clear()''')
# reload bar + dual tag
rep('''			var k: float = 1.0 - me.reload_t / WD[w.type].reload''', '''			var k: float = 1.0 - me.reload_t / maxf(0.01, me.reload_total)''')
rep('''		if zoom_level(me) > 1:
			txt("%dX" % zoom_level(me), Vector2(pc.x - 84 * u, pc.y - 10 * u), 11 * u, C_CYAN, 0, 3 * u)''', '''		if zoom_level(me) > 1:
			txt("%dX" % zoom_level(me), Vector2(pc.x - 84 * u, pc.y - 10 * u), 11 * u, C_CYAN, 0, 3 * u)
		if w.get("dual", false):
			txt("x2", Vector2(pc.x - 84 * u, pc.y + 14 * u), 12 * u, C_ARC, 0, 3 * u)''')
# red death screen
rep('''		txt("Back in %d" % ceili(me.respawn_t), Vector2(sw / 2, sh * 0.45), 26 * u, C_INK, 1, 5 * u)''', '''		draw_rect(Rect2(0, 0, sw, sh), Color(0.6, 0, 0.05, 0.16))
		txt("YOU WERE TAKEN OUT", Vector2(sw / 2, sh * 0.38), 28 * u, C_RED, 1, 6 * u)
		txt("Back in %d" % ceili(me.respawn_t), Vector2(sw / 2, sh * 0.45), 20 * u, C_RED, 1, 5 * u)''')
open(p, 'w').write(s)
print("patch b ok")
