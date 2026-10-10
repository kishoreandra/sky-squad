p = '/home/claude/skysquad/main.gd'
s = open(p).read()
def rep(a, b, count=1):
    global s
    n = s.count(a)
    assert n == count, (n, a[:110])
    s = s.replace(a, b)
def cut(start_marker, end_marker, new):
    global s
    i = s.index(start_marker); j = s.index(end_marker, i)
    s = s[:i] + new + s[j:]

# ---- buttons / sticks with options ----
cut('func buttons() -> Array:', 'func _input(event: InputEvent) -> void:', '''func btn_r() -> float:
	return clampf(sh * 0.065, 22 * u, 34 * u) * float(cfg.btn_size)

func stick_rad() -> float:
	return 50.0 * u * float(cfg.stick_size)

func mirror_x(x: float) -> float:
	return sw - x if cfg.left_handed else x

func def_move() -> Vector2:
	return Vector2(mirror_x(100 * u * float(cfg.stick_size) + safe_l + 10 * u), sh - 96 * u)

func def_aim() -> Vector2:
	return Vector2(mirror_x(sw - 200 * u - safe_r), sh - 96 * u)

func buttons() -> Array:
	var names := ["GRENADE", "SWAP", "MELEE", "RELOAD"]
	var ys := [0.30, 0.45, 0.60, 0.75]
	var r := btn_r()
	var bx := mirror_x(sw - safe_r - r - 14 * u)
	var inward := -1.0 if not cfg.left_handed else 1.0
	var out := []
	for i in 4:
		out.append({"n": names[i], "p": Vector2(bx, sh * ys[i]), "r": r})
	if state == "play" and not players.is_empty() and players[0].alive:
		var me: Player = players[0]
		var w = me.slots[me.cur]
		if w != null and WD[w.type].zooms.size() > 1:
			out.append({"n": "ZOOM", "p": Vector2(bx + inward * r * 2.5, sh * 0.30), "r": r * 0.85})
		if me.bombs > 0:
			out.append({"n": "BOMB", "p": Vector2(bx + inward * r * 2.5, sh * 0.47), "r": r * 0.85})
	if cfg.fire_mode == "button":
		var ap := def_aim()
		out.append({"n": "FIRE", "p": Vector2(ap.x, ap.y - stick_rad() - r * 1.9), "r": r * 1.35})
	out.append({"n": "SIT", "p": Vector2(mirror_x(safe_l + r + 14 * u), sh * 0.42), "r": r * 0.85})
	return out

''')
rep('''func _input(event: InputEvent) -> void:
	if event is InputEventScreenTouch:''', '''func _notification(what: int) -> void:
	if what == NOTIFICATION_WM_GO_BACK_REQUEST:
		if state == "play":
			state = "paused"
			jet_player.stop()
		elif state == "paused":
			state = "play"
		elif state == "match_cfg" or state == "ctrl_cfg" or state == "over":
			state = "menu"
		else:
			get_tree().quit()

func _input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo and (event.keycode == KEY_ESCAPE or event.keycode == KEY_P):
		if state == "play":
			state = "paused"
			jet_player.stop()
		elif state == "paused":
			state = "play"
		elif state == "match_cfg" or state == "ctrl_cfg":
			state = "menu"
		return
	if event is InputEventScreenTouch:''')
rep('''		if event.pressed and state != "play":
			menu_tap(event.position)
		elif event.pressed:
			for bb in bubbles:''', '''		if event.pressed and state != "play":
			menu_tap(event.position)
			mouse_down = false
		elif event.pressed and pause_rect.has_point(event.position):
			state = "paused"
			mouse_down = false
			jet_player.stop()
		elif event.pressed:
			for bb in bubbles:''')
rep('''	for bb in bubbles:
		if pos.distance_to(bb.pos) < bb.r + 10 * u:
			pick_request = bb.opt
			return
	for b in buttons():
		if pos.distance_to(b.p) < b.r + 12 * u:
			btn_held[b.n] = id
			return
	if pos.x < sw * 0.5:
		stick_l = {"id": id, "o": pos, "pos": pos}
	else:
		stick_r = {"id": id, "o": pos, "pos": pos}''', '''	if pause_rect.has_point(pos):
		state = "paused"
		jet_player.stop()
		return
	for bb in bubbles:
		if pos.distance_to(bb.pos) < bb.r + 10 * u:
			pick_request = bb.opt
			return
	for b in buttons():
		if pos.distance_to(b.p) < b.r + 12 * u:
			btn_held[b.n] = id
			return
	var fixed: bool = cfg.sticks == "fixed"
	if (pos.x < sw * 0.5) != bool(cfg.left_handed):
		stick_l = {"id": id, "o": def_move() if fixed else pos, "pos": pos}
	else:
		stick_r = {"id": id, "o": def_aim() if fixed else pos, "pos": pos}''')
rep('''func menu_tap(pos: Vector2) -> void:
	if menu_btn.has_point(pos):
		reset_match()
		state = "play"
		stick_l = null
		stick_r = null
		btn_held.clear()''', '''func menu_tap(pos: Vector2) -> void:
	for b in ui_btns:
		if b.r.has_point(pos):
			do_action(b.a)
			return

func do_action(a: String) -> void:
	play("swap", null, -10.0, 0.0)
	stick_l = null
	stick_r = null
	btn_held.clear()
	match a:
		"play", "again", "restart":
			reset_match()
			state = "play"
		"match":
			state = "match_cfg"
		"controls":
			state = "ctrl_cfg"
		"back", "menu":
			state = "menu"
			jet_player.stop()
		"resume":
			state = "play"
		_:
			if a.begins_with("row:"):
				var key_name := a.substr(4)
				for row in MATCH_ROWS + CONTROL_ROWS:
					if row[0] == key_name:
						var vals: Array = row[2]
						var idx := vals.find(cfg[key_name])
						cfg[key_name] = vals[(idx + 1) % vals.size()]
				save_cfg()''')
# human input: sizes, fire button, bomb
rep('''	var shoot := mouse_down and not touch_mode
	var rad := 50.0 * u''', '''	var shoot := mouse_down and not touch_mode
	var rad := stick_rad()''')
rep('''		if d.length() > rad * 0.7:
			shoot = true
		inp.aim = last_touch_aim''', '''		if d.length() > rad * 0.7 and cfg.fire_mode == "auto":
			shoot = true
		inp.aim = last_touch_aim''')
rep('''	inp.mx = mx
	inp.fly = fly
	inp.shoot = shoot''', '''	if btn_held.has("FIRE"):
		shoot = true
	inp.mx = mx
	inp.fly = fly
	inp.shoot = shoot
	inp.bomb = key(KEY_B) or btn_held.has("BOMB")''')
# ---- draw touch with options ----
rep('''func draw_touch() -> void:
	if state != "play":
		return
	var rad := 50.0 * u
	var defs := [[stick_l, Vector2(100 * u + safe_l, sh - 96 * u), "MOVE  /  UP TO FLY"], [stick_r, Vector2(sw - 200 * u - safe_r, sh - 96 * u), "AIM  /  PUSH TO SHOOT"]]
	for d in defs:
		var active: bool = d[0] != null
		var o: Vector2 = d[0].o if active else d[1]
		var pos: Vector2 = d[0].pos if active else d[1]
		var a := 0.85 if active else 0.4''', '''func draw_touch() -> void:
	if state != "play":
		return
	var rad := stick_rad()
	var op: float = float(cfg.opacity)
	var aim_lab := "AIM  /  PUSH TO SHOOT" if cfg.fire_mode == "auto" else "AIM"
	var defs := [[stick_l, def_move(), "MOVE  /  UP TO FLY"], [stick_r, def_aim(), aim_lab]]
	for d in defs:
		var active: bool = d[0] != null
		var o: Vector2 = d[0].o if active else d[1]
		var pos: Vector2 = d[0].pos if active else d[1]
		var a := (0.85 if active else 0.4) * op / 0.7''')
rep('''		draw_circle(o + dv, 22 * u, Color(1, 1, 1, 0.3 * a + 0.15))
		draw_arc(o + dv, 22 * u, 0, TAU, 32, Color(1, 1, 1, a), 1.5 * u, true)''', '''		draw_circle(o + dv, 22 * u * float(cfg.stick_size), Color(1, 1, 1, 0.3 * a + 0.15))
		draw_arc(o + dv, 22 * u * float(cfg.stick_size), 0, TAU, 32, Color(1, 1, 1, a), 1.5 * u, true)''')
rep('''	for b in buttons():
		var held := btn_held.has(b.n)
		draw_circle(b.p, b.r, Color(1, 0.85, 0.29, 0.55) if held else Color(0.04, 0.05, 0.12, 0.45))
		draw_arc(b.p, b.r, 0, TAU, 36, Color(1, 1, 1, 0.6), 1.5 * u, true)
		match b.n:''', '''	for b in buttons():
		var held := btn_held.has(b.n)
		var bg := Color(1, 0.85, 0.29, 0.55) if held else Color(0.04, 0.05, 0.12, 0.45 * op / 0.7)
		if b.n == "FIRE":
			bg = Color(0.95, 0.25, 0.3, 0.75 if held else 0.45 * op / 0.7 + 0.1)
		draw_circle(b.p, b.r, bg)
		draw_arc(b.p, b.r, 0, TAU, 36, Color(1, 1, 1, 0.6 * op / 0.7), 1.5 * u, true)
		match b.n:
			"FIRE":
				txt("FIRE", b.p + Vector2(0, 5 * u), 13 * u, C_INK, 1, 3 * u)
			"BOMB":
				tex_c("timebomb", b.p + Vector2(0, -3 * u), Vector2(20, 15) * u)
				txt("%d" % me.bombs, b.p + Vector2(b.r * 0.55, b.r * 0.7), 11 * u, C_INK, 1, 3 * u)''')
# ---- menus ----
cut('func draw_button(label: String, cx: float, y: float) -> void:', 'func draw_over() -> void:', '''func ui_button(label: String, r: Rect2, action: String, primary := false) -> void:
	rbox(Rect2(r.position + Vector2(0, 3 * u), r.size), Color("#a9811c") if primary else Color(0, 0, 0, 0.35), 10 * u)
	rbox(r, C_ARC if primary else Color(0.22, 0.26, 0.4, 0.95), 10 * u)
	txt(label, r.get_center() + Vector2(0, 6 * u), 16 * u, Color("#2a1f00") if primary else C_INK, 1)
	ui_btns.append({"r": r, "a": action})

func val_name(row: Array) -> String:
	var vals: Array = row[2]
	var idx := vals.find(cfg[row[0]])
	return row[3][idx] if idx >= 0 else str(cfg[row[0]])

func draw_menu() -> void:
	var w := minf(sw - 32 * u, 640 * u)
	var h := minf(sh - 24 * u, 330 * u)
	var r := panel(w, h)
	var x := r.position.x + 26 * u
	var y := r.position.y
	txt("ARC LIGHT STUDIO  /  BUILD " + VERSION, Vector2(x, y + 30 * u), 11 * u, C_CYAN)
	txt("SKY SQUAD", Vector2(x, y + 78 * u), 46 * u, C_ARC, 0, 6 * u)
	var bw := 230 * u
	var bh := 46 * u
	ui_button("PLAY", Rect2(x, y + 104 * u, bw, bh), "play", true)
	ui_button("MATCH SETTINGS", Rect2(x, y + 160 * u, bw, bh), "match")
	ui_button("CONTROLS", Rect2(x, y + 216 * u, bw, bh), "controls")
	var rx := x + bw + 30 * u
	var lines := [
		"THIS MATCH",
		("Teams: Blue vs Red" if cfg.mode == "team" else "Free for all") + "  /  %d bots (%s)" % [cfg.bots, cfg.skill],
		"%d minutes  /  event every %d sec" % [cfg.minutes, cfg.event_every],
		"Antigravity: %s" % ("on" if (cfg.ev_flip or cfg.zones) else "off"),
		"",
		"HOW TO PLAY",
		"Left thumb: move, push up to fly.",
		"Right thumb: aim" + (", push far to shoot." if cfg.fire_mode == "auto" else ", tap FIRE to shoot."),
		"Walk near a gun and tap its bubble to take it.",
		"Keyboard: A/D W S, mouse, E Q Z G B F.",
	]
	for i in lines.size():
		var head: bool = lines[i] == "THIS MATCH" or lines[i] == "HOW TO PLAY"
		txt(lines[i], Vector2(rx, y + 118 * u + i * 19 * u), (10 if head else 12) * u, C_CYAN if head else C_MUTED)

func draw_cfg(title: String, rows: Array) -> void:
	var w := minf(sw - 24 * u, 700 * u)
	var h := minf(sh - 20 * u, 360 * u)
	var r := panel(w, h)
	var x := r.position.x + 22 * u
	var y := r.position.y
	txt(title, Vector2(x, y + 36 * u), 24 * u, C_ARC, 0, 4 * u)
	txt("Tap a value to change it. Saved on this device.", Vector2(r.end.x - 22 * u, y + 34 * u), 10 * u, C_MUTED, 2)
	var per_col := ceili(rows.size() / 2.0)
	var colw := (w - 44 * u - 20 * u) / 2.0
	var rh := minf(34 * u, (h - 130 * u) / per_col)
	for i in rows.size():
		var row: Array = rows[i]
		var cx := x + (i / per_col) * (colw + 20 * u)
		var cy := y + 58 * u + (i % per_col) * rh
		txt(row[1], Vector2(cx, cy + rh * 0.62), 12 * u, C_INK)
		var pr := Rect2(cx + colw * 0.5, cy + rh * 0.12, colw * 0.5, rh * 0.76)
		var on_flag: bool = row[0] in ["ev_flip", "zones"] and cfg[row[0]] == true
		rbox(pr, Color(0.35, 0.18, 0.5, 0.95) if on_flag else Color(0.2, 0.25, 0.42, 0.95), 8 * u)
		txt(val_name(row), pr.get_center() + Vector2(0, 5 * u), 12 * u, C_ARC, 1)
		ui_btns.append({"r": pr, "a": "row:" + row[0]})
	ui_button("BACK", Rect2(r.position.x + w / 2 - 100 * u, r.end.y - 58 * u, 200 * u, 42 * u), "back", true)

func draw_pause() -> void:
	draw_rect(Rect2(0, 0, sw, sh), Color(0.02, 0.03, 0.1, 0.6))
	var r := panel(minf(sw - 32 * u, 340 * u), minf(sh - 24 * u, 270 * u))
	txt("PAUSED", Vector2(r.get_center().x, r.position.y + 42 * u), 26 * u, C_ARC, 1, 4 * u)
	var bx := r.get_center().x - 110 * u
	ui_button("RESUME", Rect2(bx, r.position.y + 66 * u, 220 * u, 44 * u), "resume", true)
	ui_button("RESTART", Rect2(bx, r.position.y + 120 * u, 220 * u, 44 * u), "restart")
	ui_button("MAIN MENU", Rect2(bx, r.position.y + 174 * u, 220 * u, 44 * u), "menu")

''')
rep('''	var rk := ranked()
	txt("MATCH OVER", Vector2(x, y + 28 * u), 11 * u, C_CYAN)
	txt("You win!" if rk[0] == players[0] else "%s wins" % rk[0].pname, Vector2(x, y + 60 * u), 28 * u, C_ARC, 0, 5 * u)''', '''	var rk := ranked()
	txt("MATCH OVER", Vector2(x, y + 28 * u), 11 * u, C_CYAN)
	var title := "You win!" if rk[0] == players[0] else "%s wins" % rk[0].pname
	if cfg.mode == "team":
		var ts := team_scores()
		title = "Draw" if ts[0] == ts[1] else ("Blue team wins %d : %d" % [ts[0], ts[1]] if ts[0] > ts[1] else "Red team wins %d : %d" % [ts[1], ts[0]])
	txt(title, Vector2(x, y + 60 * u), 26 * u, C_ARC, 0, 5 * u)''')
rep('''		var yy := y + 106 * u + i * 22 * u''', '''		var yy := y + 106 * u + i * minf(22 * u, (h - 180 * u) / rk.size())''')
rep('''	draw_button("PLAY AGAIN", sw / 2, r.end.y - 62 * u)''', '''	ui_button("PLAY AGAIN", Rect2(sw / 2 - 210 * u, r.end.y - 60 * u, 200 * u, 44 * u), "again", true)
	ui_button("MENU", Rect2(sw / 2 + 10 * u, r.end.y - 60 * u, 200 * u, 44 * u), "menu")''')
# ---- _draw states ----
rep('''func _draw() -> void:
	draw_set_transform_matrix(Transform2D.IDENTITY)
	var vw := sw / zoom
	var vh := sh / zoom
	if state == "menu":''', '''func _draw() -> void:
	draw_set_transform_matrix(Transform2D.IDENTITY)
	ui_btns.clear()
	var vw := sw / zoom
	var vh := sh / zoom
	var in_menu := state == "menu" or state == "match_cfg" or state == "ctrl_cfg"
	if in_menu:''')
rep('''	if state == "menu":
		draw_set_transform_matrix(Transform2D.IDENTITY)
		draw_menu()
		return''', '''	if in_menu:
		draw_set_transform_matrix(Transform2D.IDENTITY)
		if state == "menu":
			draw_menu()
		elif state == "match_cfg":
			draw_cfg("MATCH SETTINGS", MATCH_ROWS)
		else:
			draw_cfg("CONTROLS", CONTROL_ROWS)
		return''')
rep('''	if state == "over":
		draw_over()''', '''	if state == "over":
		draw_over()
	elif state == "paused":
		draw_pause()''')
rep('''	if touch_mode or OS.has_feature("mobile"):
		draw_touch()''', '''	if touch_mode or OS.has_feature("mobile") or (shot_at >= 0 and touch_mode):
		draw_touch()''')
open(p, 'w').write(s)
print("d ok")
