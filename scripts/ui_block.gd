
# =====================================================================
# v0.7 look & motion: fonts, panels that pop in, buttons that press,
# fades between screens, the respawn score card and the end screen.
# =====================================================================
var font_h: Font
var ga := 1.0
var ui_t := 9.0
var seen_state := "-"
var fade := 0.0
var pending_action := ""
var pending_t := 0.0
var pending_big := false
var pressed_r := Rect2()
var pressed_at := -9.0
var btn_i := 0
var intro_t := 9.0
var menu_actors: Array = []
var hud_hp := 100.0
var trail_hp := 100.0
var trail_hold := 0.0
var hud_prev_hp := 100.0
var ammo_pop := 0.0
var last_mag := -1
var peek_t := 0.0
var timer_rect := Rect2()
var cheer := ["", ""]
var me_was_alive := true
var anim_skip := false
var bubble_key := ""
var bubble_since := 0.0
var _sbf := StyleBoxFlat.new()
var leader_now = null
const BIG_ACTIONS := ["play", "again", "restart", "start", "menu", "leave", "to_lobby"]
const CHEERS_LAST := ["Last place is just the starting line.", "Big comebacks start with one kill.", "The match isn't over. Go get them!", "Slow down, aim first, then shoot."]
const TIPS := ["Tip: sit (Down) to shoot steadier.", "Tip: headshots do 60% more damage.", "Tip: grab a health kit before you fight.", "Tip: fly high and shoot down at them."]

func load_fonts() -> void:
	var body = load("res://fonts/InterDisplay-SemiBold.otf")
	var heavy = load("res://fonts/InterDisplay-Black.otf")
	if body != null:
		font = body
	if heavy != null:
		var fv := FontVariation.new()
		fv.base_font = heavy
		fv.variation_transform = Transform2D(Vector2(1.0, 0.2), Vector2(0.0, 1.0), Vector2.ZERO)
		fv.spacing_glyph = 1
		font_h = fv
	else:
		font_h = font

func ease_out(x: float) -> float:
	if anim_skip:
		return 1.0
	x = clampf(x, 0.0, 1.0)
	return 1.0 - pow(1.0 - x, 3.0)

func ease_back(x: float) -> float:
	if anim_skip:
		return 1.0
	x = clampf(x, 0.0, 1.0)
	var c1 := 1.70158
	return 1.0 + (c1 + 1.0) * pow(x - 1.0, 3.0) + c1 * pow(x - 1.0, 2.0)

func txh(s2: String, pos: Vector2, size: float, col: Color, align: int = 0, outline := 0.0) -> void:
	txt(s2, pos, size, col, align, outline, font_h)

func fbox(r: Rect2, col: Color, radius: float, border := Color(0, 0, 0, 0), bw := 0.0, shadow := 0.0) -> void:
	_sbf.bg_color = Color(col, col.a * ga)
	_sbf.set_corner_radius_all(int(radius))
	_sbf.border_color = Color(border, border.a * ga)
	_sbf.set_border_width_all(int(bw))
	_sbf.shadow_size = int(shadow)
	_sbf.shadow_color = Color(0, 0, 0, 0.45 * ga)
	_sbf.shadow_offset = Vector2(0, shadow * 0.3)
	_sbf.anti_aliasing = true
	draw_style_box(_sbf, r)

func circ(pos: Vector2, r: float, col: Color) -> void:
	draw_circle(pos, r, Color(col, col.a * ga))

func vignette(col: Color, edge := 0.3) -> void:
	var clear := Color(col, 0.0)
	var e := sh * edge
	var ex := sw * edge * 0.6
	draw_polygon(PackedVector2Array([Vector2(0, 0), Vector2(sw, 0), Vector2(sw, e), Vector2(0, e)]), PackedColorArray([col, col, clear, clear]))
	draw_polygon(PackedVector2Array([Vector2(0, sh - e), Vector2(sw, sh - e), Vector2(sw, sh), Vector2(0, sh)]), PackedColorArray([clear, clear, col, col]))
	draw_polygon(PackedVector2Array([Vector2(0, 0), Vector2(ex, 0), Vector2(ex, sh), Vector2(0, sh)]), PackedColorArray([col, clear, clear, col]))
	draw_polygon(PackedVector2Array([Vector2(sw - ex, 0), Vector2(sw, 0), Vector2(sw, sh), Vector2(sw - ex, sh)]), PackedColorArray([clear, col, col, clear]))

func draw_crown(c: Vector2, s2: float) -> void:
	var pts := PackedVector2Array([c + Vector2(-s2, s2 * 0.6), c + Vector2(-s2, -s2 * 0.4), c + Vector2(-s2 * 0.5, s2 * 0.05), c + Vector2(0, -s2 * 0.75),
		c + Vector2(s2 * 0.5, s2 * 0.05), c + Vector2(s2, -s2 * 0.4), c + Vector2(s2, s2 * 0.6)])
	var outline := pts.duplicate()
	outline.append(pts[0])
	draw_colored_polygon(pts, Color(1, 0.82, 0.25, ga))
	draw_polyline(outline, Color(0.35, 0.22, 0, 0.9 * ga), maxf(1.0, s2 * 0.18), true)

func current_leader():
	var best = null
	var tie := false
	for p in players:
		if best == null or p.kills > best.kills:
			best = p
			tie = false
		elif p.kills == best.kills:
			tie = true
	if best == null or tie or best.kills < 1:
		return null
	return best

func on_state_change(old: String, new: String) -> void:
	ui_t = 0.0
	if new == "play" and old != "paused":
		intro_t = 9.0 if anim_skip else 0.0
		if not anim_skip:
			view_h = S.view_h * 1.5
			fade = maxf(fade, 0.6)
		me_was_alive = true
		peek_t = 0.0
		last_mag = -1
		hud_hp = S.hp_max
		trail_hp = S.hp_max

func anim_tick(delta: float) -> void:
	anim_skip = shot_at >= 0
	ui_t += delta
	if state != seen_state:
		on_state_change(seen_state, state)
		seen_state = state
	fade = maxf(0.0, fade - delta / 0.4)
	peek_t -= delta
	ammo_pop = maxf(0.0, ammo_pop - delta * 5.0)
	if state == "play" or state == "paused":
		intro_t += delta
	if pending_action != "":
		pending_t -= delta
		if pending_t <= 0:
			var a := pending_action
			pending_action = ""
			do_action(a)
			if pending_big:
				fade = 1.0
	if MENU_STATES.has(state):
		update_actors(minf(delta, 0.05))
		update_parts(minf(delta, 0.05))
	elif not players.is_empty() and my_idx < players.size():
		var me: Player = players[my_idx]
		if me_was_alive and not me.alive:
			cheer = make_cheer(me)
		me_was_alive = me.alive

# a few soldiers flying past behind the menus
func update_actors(dt: float) -> void:
	if menu_actors.is_empty():
		var looks := [["yellow", 0, "ak47"], ["red", 2, "sniper"], ["blue", 1, "rpg"]]
		for i in 3:
			var p := Player.new()
			p.id = 100 + i
			p.actor = true
			p.team = looks[i][0]
			p.color = TEAM_COL[looks[i][1]]
			p.slots = [full_slot(looks[i][2]), null]
			p.alive = true
			menu_actors.append(p)
	var vw := sw / zoom
	var vh := sh / zoom
	for i in menu_actors.size():
		var p: Player = menu_actors[i]
		var spd := 60.0 + i * 22.0
		p.x = cam.x - 140.0 + fposmod(time_s * spd + i * 520.0, vw + 280.0)
		p.y = cam.y + vh * (0.16 + 0.22 * i) + sin(time_s * 0.8 + i * 2.1) * 26.0
		p.vx = spd
		p.on_ground = false
		p.jet_on = true
		p.aim = 0.1 + sin(time_s * 0.6 + i) * 0.18
		animate(p, dt)
		if randf() < 0.5:
			var nz := center(p) + Vector2(-9, 10)
			add_part(nz.x + randf_range(-3, 3), nz.y, randf_range(-20, 20) - spd * 0.3, randf_range(90, 160), 0.5, Color(0.85, 0.85, 0.88, 0.4), 6, -0.02, "smoke", 18)

func draw_top_layers() -> void:
	draw_set_transform_matrix(Transform2D.IDENTITY)
	ga = 1.0
	draw_toast()
	var fa := fade
	if pending_action != "" and pending_big:
		fa = maxf(fa, 1.0 - pending_t / 0.22)
	if fa > 0.001 and not anim_skip:
		draw_rect(Rect2(0, 0, sw, sh), Color(0.02, 0.03, 0.08, clampf(fa, 0.0, 1.0)))

func end_panel() -> void:
	draw_set_transform_matrix(Transform2D.IDENTITY)
	ga = 1.0

# ---------- ranking rows (respawn card, peek, end screen) ----------
func draw_rank_rows(x: float, y: float, w: float, rowh: float, rk: Array, age: float, aw := {}) -> void:
	var lead = current_leader()
	txt("KILLS", Vector2(x + w - 62 * u, y - 6 * u), 9 * u, C_MUTED, 2)
	txt("DEATHS", Vector2(x + w - 8 * u, y - 6 * u), 9 * u, C_MUTED, 2)
	for i in rk.size():
		var p: Player = rk[i]
		var kk := ease_out((age - 0.1 - i * 0.05) / 0.28)
		var ga0 := ga
		ga *= kk
		var rr := Rect2(x + (1.0 - kk) * 24 * u, y + i * rowh, w, rowh - 3 * u)
		var mine := is_me(p)
		if mine:
			fbox(rr, Color(C_ARC, 0.16), 7 * u, Color(C_ARC, 0.55), maxf(1.0, u))
		elif i % 2 == 0:
			fbox(rr, Color(1, 1, 1, 0.035), 7 * u)
		var by := rr.position.y + rowh * 0.62
		txh("%d" % (i + 1), Vector2(rr.position.x + 10 * u, by), 13 * u, C_ARC if i == 0 else C_MUTED)
		circ(Vector2(rr.position.x + 34 * u, by - 4.5 * u), 5 * u, p.color)
		var nx := rr.position.x + 46 * u
		txt(p.pname, Vector2(nx, by), 13 * u, C_ARC if mine else C_INK)
		nx += font.get_string_size(p.pname, 0, -1, int(13 * u)).x + 8 * u
		if p == lead:
			draw_crown(Vector2(nx + 6 * u, by - 5 * u), 6 * u)
			nx += 18 * u
		if aw.has(p):
			var lab: String = aw[p][0]
			var cw := font.get_string_size(lab, 0, -1, int(8 * u)).x + 12 * u
			fbox(Rect2(nx, by - 11 * u, cw, 14 * u), Color(aw[p][1], 0.2), 7 * u, Color(aw[p][1], 0.7), maxf(1.0, u * 0.8))
			txt(lab, Vector2(nx + cw / 2, by - 1 * u), 8 * u, aw[p][1], 1)
		var shown := p.kills
		if not aw.is_empty():
			shown = int(round(p.kills * ease_out((age - 0.3 - i * 0.06) / 0.6)))
		txh(str(shown), Vector2(rr.end.x - 62 * u, by), 14 * u, C_INK, 2)
		txt(str(p.deaths), Vector2(rr.end.x - 8 * u, by), 13 * u, C_MUTED, 2)
		ga = ga0

func team_bar(x: float, y: float, w: float) -> void:
	var ts := team_scores()
	var tot := maxf(1.0, float(ts[0] + ts[1]))
	var bw := w * (0.5 if ts[0] + ts[1] == 0 else ts[0] / tot)
	fbox(Rect2(x, y, w, 8 * u), Color(TEAM_COL[2], 0.85), 4 * u)
	fbox(Rect2(x, y, maxf(bw, 8 * u), 8 * u), Color(TEAM_COL[1], 0.95), 4 * u)
	txh("BLUE %d" % ts[0], Vector2(x, y - 5 * u), 12 * u, TEAM_COL[1])
	txh("%d RED" % ts[1], Vector2(x + w, y - 5 * u), 12 * u, TEAM_COL[2], 2)

func make_cheer(me: Player) -> Array:
	var rk := ranked()
	var pos := rk.find(me)
	var n := rk.size()
	var l1 := ""
	var l2 := ""
	if cfg.mode == "team":
		var ts := team_scores()
		var mine: int = ts[me.side % 2]
		var other: int = ts[1 - me.side % 2]
		if mine > other:
			l1 = "Your team leads by %d. Keep it up!" % (mine - other)
		elif mine == other:
			l1 = "It's tied. Your next kill puts your team ahead."
		else:
			var g := other - mine + 1
			l1 = "Your team needs %d kill%s to take the lead." % [g, "" if g == 1 else "s"]
	elif pos == 0 and me.kills > 0:
		l1 = "You're number 1. Make them chase you."
	elif pos > 0:
		var above: Player = rk[pos - 1]
		var g2: int = maxi(1, above.kills - me.kills + (0 if above.kills == me.kills else 1))
		l1 = "%d kill%s to pass %s" % [g2, "" if g2 == 1 else "s", above.pname]
	else:
		l1 = "Go get the first kill!"
	if me.lstreak >= 2:
		l2 = "Nice run: %d kills in a row." % me.lstreak
	elif pos == n - 1 and n > 2 and cfg.mode != "team":
		l2 = CHEERS_LAST[randi() % CHEERS_LAST.size()]
	else:
		l2 = TIPS[randi() % TIPS.size()]
	return [l1, l2]

func death_line(me: Player) -> Array:
	var k = me.last_hit_by
	if k != null and k != me:
		var how := ""
		if WD.has(me.last_gun):
			how = WD[me.last_gun].name
		else:
			how = {"grenade": "GRENADE", "rpg": "ROCKET", "bomb": "TIME BOMB", "melee": "KNIFE", "shock": "SHOCK"}.get(me.last_gun, "")
		if me.last_head and me.last_cause == "shot":
			how += "  /  HEADSHOT"
		return [k.pname, k.color, how]
	var note: String = {"water": "You drowned", "crush": "A falling rock got you"}.get(me.last_cause, "Your own blast got you")
	return ["", C_INK, note]

func draw_respawn_card(me: Player) -> void:
	var age := S.respawn - me.respawn_t
	var a := ease_out(age / 0.3)
	var k := ease_back((age - 0.05) / 0.4)
	draw_rect(Rect2(0, 0, sw, sh), Color(0.25, 0.0, 0.03, 0.18 * a))
	vignette(Color(0.3, 0.0, 0.04, 0.6 * a), 0.28)
	var rk := ranked()
	var team := cfg.mode == "team"
	var rowh := 23 * u
	var w := minf(sw - 40 * u, 470 * u)
	var h := 84 * u + (26 * u if team else 0.0) + rk.size() * rowh + 54 * u
	h = minf(h, sh - 16 * u)
	var r := Rect2(sw / 2 - w / 2, (sh - h) / 2 + (1.0 - k) * 70 * u, w, h)
	ga = a
	fbox(r, Color(0.06, 0.08, 0.18, 0.93), 16 * u, Color(1, 1, 1, 0.1), maxf(1.0, 1.5 * u), 22 * u)
	fbox(Rect2(r.position + Vector2(2, 2) * u, Vector2(r.size.x - 4 * u, 50 * u)), Color(1, 1, 1, 0.03), 14 * u)
	fbox(Rect2(r.position.x + 24 * u, r.position.y - 2 * u, 64 * u, 4 * u), C_RED, 2 * u)
	var x := r.position.x + 22 * u
	var y := r.position.y
	txh("TAKEN OUT", Vector2(x, y + 36 * u), 22 * u, C_RED, 0, 4 * u)
	var dl := death_line(me)
	if dl[0] != "":
		txt("by", Vector2(x, y + 58 * u), 12 * u, C_MUTED)
		var nx := x + font.get_string_size("by ", 0, -1, int(12 * u)).x
		txt(dl[0], Vector2(nx, y + 58 * u), 12 * u, dl[1])
		nx += font.get_string_size(dl[0], 0, -1, int(12 * u)).x + 8 * u
		txt(dl[2], Vector2(nx, y + 58 * u), 10 * u, C_MUTED)
	else:
		txt(dl[2], Vector2(x, y + 58 * u), 12 * u, C_MUTED)
	# countdown ring
	var cc := Vector2(r.end.x - 42 * u, y + 40 * u)
	draw_arc(cc, 22 * u, 0, TAU, 48, Color(1, 1, 1, 0.12 * ga), 4 * u, true)
	var left := clampf(me.respawn_t / S.respawn, 0.0, 1.0)
	if left > 0.01:
		draw_arc(cc, 22 * u, -PI / 2, -PI / 2 + TAU * left, 48, Color(C_ARC, ga), 4 * u, true)
	txh(str(maxi(1, ceili(me.respawn_t))), cc + Vector2(0, 8 * u), 22 * u, C_INK, 1)
	var ry := y + 92 * u
	if team:
		team_bar(x, y + 92 * u, r.size.x - 44 * u)
		ry += 26 * u
	draw_rank_rows(r.position.x + 14 * u, ry, r.size.x - 28 * u, rowh, rk, age)
	var ck := ease_out((age - 0.45) / 0.35)
	var ga0 := ga
	ga *= ck
	txh(cheer[0], Vector2(x, r.end.y - 30 * u), 14 * u, C_ARC)
	txt(cheer[1], Vector2(x, r.end.y - 12 * u), 11 * u, C_MUTED)
	ga = ga0
	ga = 1.0

func draw_peek() -> void:
	var a := ease_out(minf(3.0 - peek_t, peek_t) / 0.2) if peek_t > 0 else 1.0
	var rk := ranked()
	var rowh := 21 * u
	var w := minf(sw - 40 * u, 380 * u)
	var team := cfg.mode == "team"
	var h := 26 * u + (24 * u if team else 0.0) + rk.size() * rowh + 8 * u
	var r := Rect2(sw / 2 - w / 2, 60 * u - (1.0 - a) * 12 * u, w, h)
	ga = a
	fbox(r, Color(0.05, 0.07, 0.16, 0.88), 12 * u, Color(1, 1, 1, 0.1), maxf(1.0, u), 14 * u)
	var ry := r.position.y + 26 * u
	if team:
		team_bar(r.position.x + 14 * u, r.position.y + 28 * u, w - 28 * u)
		ry += 24 * u
	draw_rank_rows(r.position.x + 10 * u, ry, w - 20 * u, rowh, rk, 9.0)
	ga = 1.0

func awards(rk: Array) -> Dictionary:
	var out := {}
	if not rk.is_empty() and rk[0].kills > 0:
		out[rk[0]] = ["MVP", C_ARC]
	var picks := [["hs", 1, "SHARPSHOOTER", C_CYAN], ["best", 3, "ON FIRE", Color("#ff9a4d")], ["bk", 2, "BOMBER", Color("#ffc061")], ["mk", 1, "KNIFE MASTER", C_PINK]]
	for pk in picks:
		var best = null
		for p in rk:
			if not out.has(p) and p.get(pk[0]) >= pk[1] and (best == null or p.get(pk[0]) > best.get(pk[0])):
				best = p
		if best != null:
			out[best] = [pk[2], pk[3]]
	var few = null
	for p in rk:
		if not out.has(p) and p.kills > 0 and (few == null or p.deaths < few.deaths):
			few = p
	if few != null:
		out[few] = ["SURVIVOR", C_GREEN]
	var most = null
	for p in rk:
		if not out.has(p) and p.deaths > 0 and (most == null or p.deaths > most.deaths):
			most = p
	if most != null:
		out[most] = ["NEVER GAVE UP", Color("#b9a2ff")]
	for p in rk:
		if not out.has(p):
			out[p] = ["FIGHTER", C_MUTED]
	return out

func end_line(rk: Array) -> String:
	var me: Player = players[my_idx]
	if cfg.mode == "team":
		var ts := team_scores()
		var mine: int = ts[me.side % 2]
		var other: int = ts[1 - me.side % 2]
		if mine > other:
			return "Your team won! You got %d kill%s for the team." % [me.kills, "" if me.kills == 1 else "s"]
		if mine == other:
			return "A draw. One more kill would have done it!"
		return "So close. Next match is yours."
	var pos := rk.find(me)
	if pos == 0 and me.kills > 0:
		return "You won! Can you do it again?"
	if pos == rk.size() - 1:
		return "You got %d kill%s. Next match, aim for %d!" % [me.kills, "" if me.kills == 1 else "s", me.kills + 2]
	var g: int = rk[0].kills - me.kills + 1
	return "%d more kill%s and you would have won. Go again!" % [g, "" if g == 1 else "s"]
