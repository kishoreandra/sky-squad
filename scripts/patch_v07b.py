"""v0.7 part B: HD look, motion, respawn score card, new end screen."""
import re, sys
P = "/home/claude/skysquad/main.gd"
s = open(P).read()

def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        sys.exit(f"expected {count} got {n}: {old[:90]!r}")
    s = s.replace(old, new)

def func_span(name):
    a = s.index("\nfunc " + name + "(") + 1
    b = s.index("\nfunc ", a + 5) + 1
    return a, b

def replace_func(name, new):
    global s
    a, b = func_span(name)
    s = s[:a] + new.strip("\n") + "\n\n" + s[b:]

# fonts
rep('\tfont = ThemeDB.fallback_font\n', '\tfont = ThemeDB.fallback_font\n\tload_fonts()\n')

# txt / rbox respect global alpha + optional font
replace_func("txt", '''func txt(s2: String, pos: Vector2, size: float, col: Color, align: int = 0, outline := 0.0, f: Font = null) -> void:
	if f == null:
		f = font
	col.a *= ga
	if col.a <= 0.004:
		return
	var fs := int(size)
	var x := pos.x
	if align != 0:
		var wdt := f.get_string_size(s2, HORIZONTAL_ALIGNMENT_LEFT, -1, fs).x
		x -= wdt / 2.0 if align == 1 else wdt
	if outline > 0:
		draw_string_outline(f, Vector2(x, pos.y), s2, HORIZONTAL_ALIGNMENT_LEFT, -1, fs, int(outline), Color(0, 0, 0, 0.75 * col.a))
	draw_string(f, Vector2(x, pos.y), s2, HORIZONTAL_ALIGNMENT_LEFT, -1, fs, col)''')
rep('''func rbox(r: Rect2, col: Color, radius: float) -> void:
	_sb.bg_color = col''', '''func rbox(r: Rect2, col: Color, radius: float) -> void:
	_sb.bg_color = Color(col, col.a * ga)''')

replace_func("panel", '''func panel(w: float, h: float) -> Rect2:
	var r := Rect2(sw / 2 - w / 2, sh / 2 - h / 2, w, h)
	var k := ease_back(ui_t / 0.34)
	var sc := lerpf(0.9, 1.0, k)
	var cpos := r.get_center() + Vector2(0, (1.0 - k) * 16 * u)
	draw_set_transform_matrix(Transform2D(0.0, Vector2(sc, sc), 0.0, cpos - r.get_center() * sc))
	ga = ease_out(ui_t / 0.2)
	btn_i = 0
	fbox(r, Color(0.065, 0.085, 0.2, 0.94), 18 * u, Color(1, 1, 1, 0.11), maxf(1.0, 1.5 * u), 26 * u)
	fbox(Rect2(r.position + Vector2(2, 2) * u, Vector2(r.size.x - 4 * u, minf(r.size.y * 0.4, 120 * u))), Color(1, 1, 1, 0.03), 16 * u)
	fbox(Rect2(r.position.x + 26 * u, r.position.y - 2 * u, 72 * u, 4 * u), C_ARC, 2 * u)
	return r''')

replace_func("ui_button", '''func ui_button(label: String, r: Rect2, action: String, primary := false) -> void:
	ui_btns.append({"r": r, "a": action})
	var i := btn_i
	btn_i += 1
	var k := ease_out((ui_t - 0.08 - i * 0.045) / 0.26)
	var ga0 := ga
	ga *= k
	var rr := r
	rr.position.x -= (1.0 - k) * 26 * u
	var hover: bool = not touch_mode and mouse_used and r.has_point(mouse_pos) and pending_action == ""
	if r == pressed_r and time_s - pressed_at < 0.18:
		rr = rr.grow(-rr.size.y * 0.06)
	elif hover:
		rr.position.y -= 2 * u
	var base: Color = C_ARC if primary else Color(0.2, 0.25, 0.43)
	if primary:
		var gl := 0.18 + 0.12 * sin(time_s * 3.0)
		fbox(rr.grow(3 * u), Color(0, 0, 0, 0), 13 * u, Color(C_ARC, gl), 2 * u)
	fbox(Rect2(rr.position + Vector2(0, 4 * u), rr.size), base.darkened(0.55) if primary else Color(0, 0, 0, 0.45), 11 * u)
	fbox(rr, base.lightened(0.12 if hover else 0.0), 11 * u, Color(1, 1, 1, 0.4 if primary else 0.13), maxf(1.0, u))
	fbox(Rect2(rr.position + Vector2(3, 2) * u, Vector2(rr.size.x - 6 * u, rr.size.y * 0.46)), Color(1, 1, 1, 0.24 if primary else 0.07), 9 * u)
	var fs := 15 * u if rr.size.y > 36 * u else 13 * u
	txh(label, rr.get_center() + Vector2(0, fs * 0.36), fs, Color("#2a1f00") if primary else C_INK, 1)
	ga = ga0''')

replace_func("draw_menu", '''func draw_menu() -> void:
	var w := minf(sw - 32 * u, 640 * u)
	var h := minf(sh - 24 * u, 330 * u)
	var r := panel(w, h)
	var x := r.position.x + 26 * u
	var y := r.position.y
	txt("ARC LIGHT STUDIO  /  BUILD " + VERSION, Vector2(x, y + 30 * u), 11 * u, C_CYAN)
	var title := "SKY SQUAD"
	var fs := 50 * u
	var xx := x
	for i in title.length():
		var ch := title[i]
		var k := ease_back((ui_t - 0.12 - i * 0.045) / 0.4)
		var ga0 := ga
		ga *= clampf((ui_t - 0.12 - i * 0.045) / 0.15, 0.0, 1.0) if not anim_skip else 1.0
		txh(ch, Vector2(xx, y + 80 * u - (1.0 - k) * 34 * u), fs, C_ARC, 0, 7 * u)
		ga = ga0
		xx += font_h.get_string_size(ch, HORIZONTAL_ALIGNMENT_LEFT, -1, int(fs)).x
	var bw := 230 * u
	var bh := 44 * u
	ui_button("PLAY VS BOTS", Rect2(x, y + 100 * u, bw, bh), "play", true)
	ui_button("PLAY WITH FRIENDS", Rect2(x, y + 152 * u, bw, bh), "lan", true)
	ui_button("MATCH SETTINGS", Rect2(x, y + 204 * u, bw, bh), "match")
	ui_button("CONTROLS", Rect2(x, y + 256 * u, bw, bh), "controls")
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
		var k2 := ease_out((ui_t - 0.2 - i * 0.03) / 0.3)
		var ga1 := ga
		ga *= k2
		txt(lines[i], Vector2(rx + (1.0 - k2) * 14 * u, y + 118 * u + i * 19 * u), (10 if head else 12) * u, C_CYAN if head else C_MUTED)
		ga = ga1''')

rep('''	txt(title, Vector2(x, y + 36 * u), 24 * u, C_ARC, 0, 4 * u)
	txt("Tap a value to change it. Saved on this device."''', '''	txh(title, Vector2(x, y + 38 * u), 24 * u, C_ARC, 0, 4 * u)
	txt("Tap a value to change it. Saved on this device."''')
rep('''		rbox(pr, Color(0.35, 0.18, 0.5, 0.95) if on_flag else Color(0.2, 0.25, 0.42, 0.95), 8 * u)
		txt(val_name(row), pr.get_center() + Vector2(0, 5 * u), 12 * u, C_ARC, 1)''', '''		if pr == pressed_r and time_s - pressed_at < 0.18:
			pr = pr.grow(-2 * u)
		fbox(pr, Color(0.35, 0.18, 0.5, 0.95) if on_flag else Color(0.17, 0.21, 0.38, 0.95), 8 * u, Color(1, 1, 1, 0.12), maxf(1.0, u))
		txh(val_name(row), pr.get_center() + Vector2(0, 5 * u), 12 * u, C_ARC, 1)''')
# the hit rect must stay the unshrunk one
rep('''		var pr := Rect2(cx + colw * 0.5, cy + rh * 0.12, colw * 0.5, rh * 0.76)''', '''		var pr := Rect2(cx + colw * 0.5, cy + rh * 0.12, colw * 0.5, rh * 0.76)
		ui_btns.append({"r": pr, "a": "row:" + row[0]})''')
rep('''		txh(val_name(row), pr.get_center() + Vector2(0, 5 * u), 12 * u, C_ARC, 1)
		ui_btns.append({"r": pr, "a": "row:" + row[0]})''', '''		txh(val_name(row), pr.get_center() + Vector2(0, 5 * u), 12 * u, C_ARC, 1)''')

replace_func("draw_pause", '''func draw_pause() -> void:
	draw_rect(Rect2(0, 0, sw, sh), Color(0.02, 0.03, 0.1, 0.6 * ease_out(ui_t / 0.2)))
	var r := panel(minf(sw - 32 * u, 340 * u), minf(sh - 24 * u, 270 * u))
	txh("PAUSED", Vector2(r.get_center().x, r.position.y + 44 * u), 26 * u, C_ARC, 1, 4 * u)
	var bx := r.get_center().x - 110 * u
	if net_role != "":
		txt("The match keeps going for your friends.", Vector2(r.get_center().x, r.position.y + 64 * u), 10 * u, C_MUTED, 1)
		ui_button("RESUME", Rect2(bx, r.position.y + 80 * u, 220 * u, 44 * u), "resume", true)
		ui_button("LEAVE MATCH", Rect2(bx, r.position.y + 140 * u, 220 * u, 44 * u), "leave")
		return
	ui_button("RESUME", Rect2(bx, r.position.y + 66 * u, 220 * u, 44 * u), "resume", true)
	ui_button("RESTART", Rect2(bx, r.position.y + 120 * u, 220 * u, 44 * u), "restart")
	ui_button("MAIN MENU", Rect2(bx, r.position.y + 174 * u, 220 * u, 44 * u), "menu")''')

replace_func("draw_over", '''func draw_over() -> void:
	draw_rect(Rect2(0, 0, sw, sh), Color(0.02, 0.03, 0.1, 0.62 * ease_out(ui_t / 0.3)))
	var rk := ranked()
	var team := cfg.mode == "team"
	var rowh := minf(25 * u, (minf(sh - 24 * u, 380 * u) - 190 * u) / maxf(1.0, rk.size()))
	var w := minf(sw - 32 * u, 560 * u)
	var h := minf(sh - 24 * u, 190 * u + rk.size() * rowh + (24 * u if team else 0.0))
	var r := panel(w, h)
	var x := r.position.x + 24 * u
	var y := r.position.y
	txt("MATCH OVER", Vector2(x, y + 30 * u), 11 * u, C_CYAN)
	var title := "You win!" if (rk[0] == players[my_idx] and rk[0].kills > 0) else "%s wins" % rk[0].pname
	if team:
		var ts := team_scores()
		title = "Draw" if ts[0] == ts[1] else ("Blue team wins" if ts[0] > ts[1] else "Red team wins")
	var tk := ease_back((ui_t - 0.15) / 0.4)
	var ga0 := ga
	ga *= clampf((ui_t - 0.15) / 0.15, 0.0, 1.0) if not anim_skip else 1.0
	var tsz := 28 * u * lerpf(1.4, 1.0, tk)
	if not team and rk[0].kills > 0:
		draw_crown(Vector2(x + 12 * u, y + 52 * u), 11 * u)
		txh(title, Vector2(x + 32 * u, y + 64 * u), tsz, C_ARC, 0, 5 * u)
	else:
		txh(title, Vector2(x, y + 64 * u), tsz, C_ARC, 0, 5 * u)
	ga = ga0
	var ry := y + 104 * u
	if team:
		team_bar(x, y + 96 * u, w - 48 * u)
		ry += 24 * u
	draw_rank_rows(r.position.x + 14 * u, ry, w - 28 * u, rowh, rk, ui_t, awards(rk))
	var lk := ease_out((ui_t - 0.9) / 0.4)
	var ga1 := ga
	ga *= lk
	txh(end_line(rk), Vector2(r.get_center().x, r.end.y - 72 * u), 13 * u, C_INK, 1)
	ga = ga1
	if net_role == "client":
		txt("Waiting for the host to start the next match...", Vector2(r.position.x + 24 * u, r.end.y - 30 * u), 11 * u, C_MUTED)
		ui_button("LEAVE", Rect2(r.end.x - 24 * u - 110 * u, r.end.y - 56 * u, 110 * u, 40 * u), "leave")
		return
	ui_button("PLAY AGAIN", Rect2(r.get_center().x - 210 * u, r.end.y - 58 * u, 200 * u, 44 * u), "again", true)
	if net_role == "host":
		ui_button("LOBBY", Rect2(r.get_center().x + 10 * u, r.end.y - 58 * u, 200 * u, 44 * u), "to_lobby")
	else:
		ui_button("MENU", Rect2(r.get_center().x + 10 * u, r.end.y - 58 * u, 200 * u, 44 * u), "menu")''')

# HUD bar with damage trail
replace_func("bar", '''func bar(pos: Vector2, w: float, h: float, val: float, col: Color, label: String, trail := -1.0) -> void:
	fbox(Rect2(pos - Vector2(3, 3) * u, Vector2(w, h) + Vector2(6, 6) * u), Color(0.04, 0.05, 0.12, 0.62), 7 * u, Color(1, 1, 1, 0.1), maxf(1.0, u))
	rbox(Rect2(pos, Vector2(w, h)), Color(0, 0, 0, 0.4), 4 * u)
	if trail > val + 0.005:
		rbox(Rect2(pos, Vector2(w * clampf(trail, 0, 1), h)), Color(1, 0.92, 0.85, 0.8), 4 * u)
	if val > 0.01:
		rbox(Rect2(pos, Vector2(w * clampf(val, 0, 1), h)), col, 4 * u)
		rbox(Rect2(pos + Vector2(2 * u, 1.5 * u), Vector2(maxf(0, w * clampf(val, 0, 1) - 4 * u), h * 0.32)), Color(1, 1, 1, 0.28), 3 * u)
	txh(label, pos + Vector2(8 * u, h - 3 * u), 11 * u, Color(1, 1, 1, 0.97), 0, 3 * u)''')

# HUD changes
rep('''	bar(Vector2(sx, sy), bw, 15 * u, me.hp / S.hp_max, C_GREEN if me.hp > 40 else C_RED, "%d" % ceili(me.hp))''', '''	var dd := last_delta
	if me.hp < hud_prev_hp - 0.5:
		trail_hold = 0.45
	hud_prev_hp = me.hp
	hud_hp = lerpf(hud_hp, me.hp, ease_k(16.0, dd))
	trail_hold -= dd
	if me.hp >= trail_hp:
		trail_hp = me.hp
	elif trail_hold <= 0:
		trail_hp = move_toward(trail_hp, me.hp, 70.0 * dd)
	bar(Vector2(sx, sy), bw, 15 * u, hud_hp / S.hp_max, C_GREEN if me.hp > 40 else C_RED, "%d" % ceili(me.hp), trail_hp / S.hp_max)''')
rep('''	for f in feed:
		var a := clampf(f.t, 0, 1)
		var x := lx''', '''	for f in feed:
		var fk := ease_out((float(f.get("t0", 5.0)) - f.t) / 0.25)
		var a := clampf(f.t, 0, 1) * fk
		var x := lx - (1.0 - fk) * 30 * u''')
rep('''	rbox(Rect2(sw / 2 - 56 * u, 8 * u, 112 * u, 44 * u), Color(0.04, 0.05, 0.12, 0.55), 10 * u)
	txt("%d:%02d" % [int(left) / 60, int(left) % 60], Vector2(sw / 2, 32 * u), 22 * u, C_INK, 1, 3 * u)''', '''	timer_rect = Rect2(sw / 2 - 56 * u, 8 * u, 112 * u, 44 * u)
	fbox(timer_rect, Color(0.04, 0.05, 0.12, 0.58), 10 * u, Color(1, 1, 1, 0.1), maxf(1.0, u))
	txh("%d:%02d" % [int(left) / 60, int(left) % 60], Vector2(sw / 2, 33 * u), 22 * u, C_RED if left < 10 else C_INK, 1, 3 * u)''')
rep('''	var rk := ranked()
	var bx := sw - safe_r - 112 * u
	rbox(Rect2(bx - 8 * u, 8 * u, 112 * u, (rk.size() * 15 + 8) * u), Color(0.04, 0.05, 0.12, 0.5), 8 * u)
	for i in rk.size():
		var yy := 22 * u + i * 15 * u
		draw_circle(Vector2(bx + 2 * u, yy - 4 * u), 4 * u, rk[i].color)
		txt(rk[i].pname, Vector2(bx + 10 * u, yy), 11 * u, C_ARC if is_me(rk[i]) else (C_INK if rk[i].bot else C_CYAN), 0, 2 * u)
		txt(str(rk[i].kills), Vector2(bx + 94 * u, yy), 11 * u, C_INK, 2, 2 * u)
''', '')
rep('''		txt("%d" % w.mag, Vector2(pc.x + 32 * u, pc.y + 6 * u), 22 * u, C_INK if w.mag > 0 else C_RED, 2, 3 * u)''', '''		if last_mag >= 0 and w.mag < last_mag:
			ammo_pop = 1.0
		last_mag = w.mag
		txh("%d" % w.mag, Vector2(pc.x + 32 * u, pc.y + 7 * u), 22 * u * (1.0 + 0.18 * ammo_pop), C_INK.lerp(C_ARC, ammo_pop) if w.mag > 0 else C_RED, 2, 3 * u)''')
rep('''	if big_t > 0:
		var a2 := clampf(big_t, 0, 1)
		var s := 1.0 + maxf(0, big_t - 1.3) * 1.5
		txt(big_msg, Vector2(sw / 2, sh * 0.36), 30 * u * s, Color(C_ARC, a2), 1, 6 * u)
	if not me.alive:
		draw_rect(Rect2(0, 0, sw, sh), Color(0.6, 0, 0.05, 0.16))
		txt("YOU WERE TAKEN OUT", Vector2(sw / 2, sh * 0.38), 28 * u, C_RED, 1, 6 * u)
		txt("Back in %d" % ceili(me.respawn_t), Vector2(sw / 2, sh * 0.45), 20 * u, C_RED, 1, 5 * u)
		if me.last_hit_by != null and me.last_hit_by != me:
			txt("by %s" % me.last_hit_by.pname, Vector2(sw / 2, sh * 0.45 + 24 * u), 14 * u, C_RED, 1, 3 * u)
	elif state == "play":
		draw_bubble(me)''', '''	if big_t > 0 and me.alive:
		var age := 1.6 - big_t
		var bk := ease_back(age / 0.3)
		var a2 := clampf(big_t / 0.45, 0, 1) * clampf(age / 0.08, 0, 1)
		txh(big_msg, Vector2(sw / 2, sh * 0.34), 32 * u * lerpf(1.7, 1.0, bk), Color(C_ARC, a2), 1, 7 * u)
	if intro_t < 2.4 and me.alive:
		var ik := ease_back(intro_t / 0.35)
		var ia := clampf((2.4 - intro_t) / 0.5, 0, 1) * clampf(intro_t / 0.1, 0, 1)
		txh("FIGHT!", Vector2(sw / 2, sh * 0.33), 46 * u * lerpf(1.8, 1.0, ik), Color(C_ARC, ia), 1, 8 * u)
		var goal := "Blue vs Red. Most kills wins." if cfg.mode == "team" else "Most kills in %d:%02d wins." % [int(match_time) / 60, int(match_time) % 60]
		txt(goal, Vector2(sw / 2, sh * 0.33 + 30 * u), 14 * u, Color(C_INK, ia * clampf((intro_t - 0.2) / 0.3, 0, 1)), 1, 4 * u)
	if me.alive and me.protect_t > S.protect - 0.3:
		draw_rect(Rect2(0, 0, sw, sh), Color(1, 1, 1, 0.35 * (me.protect_t - (S.protect - 0.3)) / 0.3))
	if not me.alive:
		draw_respawn_card(me)
	elif state == "play":
		draw_bubble(me)
		if peek_t > 0 or (key(KEY_TAB) and not touch_mode):
			draw_peek()''')
rep('''	if hurt_t > 0:
		var a4 := clampf(hurt_t / 0.35, 0, 1) * 0.35
		var e := 26 * u
		draw_rect(Rect2(0, 0, sw, e), Color(0.9, 0, 0, a4))
		draw_rect(Rect2(0, sh - e, sw, e), Color(0.9, 0, 0, a4))
		draw_rect(Rect2(0, 0, e, sh), Color(0.9, 0, 0, a4))
		draw_rect(Rect2(sw - e, 0, e, sh), Color(0.9, 0, 0, a4))''', '''	if hurt_t > 0 and me.alive:
		vignette(Color(0.85, 0, 0.05, clampf(hurt_t / 0.35, 0, 1) * 0.42), 0.16)
	elif me.alive and me.hp < 30:
		vignette(Color(0.7, 0, 0.05, 0.16 + 0.08 * sin(time_s * 5.0)), 0.14)''')

# bubble pops in
rep('''	var r := 28.0 * u * (1.0 + 0.04 * sin(time_s * 5.0))''', '''	var bkey := "%s%d" % [k.gun, int(k.x / 16) * 1000 + int(k.y / 16)]
	if bkey != bubble_key:
		bubble_key = bkey
		bubble_since = time_s
	var r := 28.0 * u * (1.0 + 0.04 * sin(time_s * 5.0)) * maxf(0.05, ease_back((time_s - bubble_since) / 0.25))''')
rep('''	var k = near_gun(me)
	if k == null:
		return''', '''	var k = near_gun(me)
	if k == null:
		bubble_key = ""
		return''')

# players: crown over the leader, spawn ring, no tags on menu actors
rep('''	if p.protect_t > 0:
		draw_arc(Vector2(0, -4), 30, 0, TAU, 40, Color(0.5, 0.9, 1.0, 0.5), 2.0, true)''', '''	if p.protect_t > 0:
		draw_arc(Vector2(0, -4), 30, 0, TAU, 40, Color(0.5, 0.9, 1.0, 0.5), 2.0, true)
		var sa: float = S.protect - p.protect_t
		if sa < 0.5:
			draw_arc(Vector2(0, -4), 30 + sa * 90, 0, TAU, 48, Color(1, 1, 1, (1.0 - sa / 0.5) * 0.8), 3.0, true)''')
rep('''	if not is_me(p) or cfg.mode == "team":
		txt(p.pname''', '''	if p.actor:
		return
	if p == leader_now:
		draw_crown(Vector2(c.x, ty - (16 if (not is_me(p) or cfg.mode == "team") else 2)), 7)
	if not is_me(p) or cfg.mode == "team":
		txt(p.pname''')

# _draw: actors in menus, reset transforms, top layers (toast + fades)
rep('''	draw_zones()
	draw_tiles(vw, vh)
	if in_menu:
		draw_set_transform_matrix(Transform2D.IDENTITY)
		match state:''', '''	draw_zones()
	draw_tiles(vw, vh)
	if in_menu:
		for ac in menu_actors:
			draw_player(ac, wt)
		draw_parts(wt)
		draw_set_transform_matrix(Transform2D.IDENTITY)
		vignette(Color(0.02, 0.03, 0.1, 0.45), 0.3)
		match state:''')
rep('''			_:
				draw_menu()
		draw_toast()
		return''', '''			_:
				draw_menu()
		draw_top_layers()
		return''')
rep('''	if state == "over":
		draw_over()
	elif state == "paused":
		draw_pause()
	draw_toast()''', '''	if state == "over":
		draw_over()
	elif state == "paused":
		draw_pause()
	draw_top_layers()''')
rep('''	draw_event_world()
	for k in pickups:''', '''	leader_now = current_leader()
	draw_event_world()
	for k in pickups:''')
rep('''	draw_set_transform_matrix(Transform2D.IDENTITY)
	draw_hud()''', '''	draw_set_transform_matrix(Transform2D.IDENTITY)
	ga = 1.0
	draw_hud()''')

# touch buttons squash when held
rep('''		draw_circle(b.p, b.r, bg)
		draw_arc(b.p, b.r, 0, TAU, 36''', '''		var br: float = b.r * (0.9 if held else 1.0)
		draw_circle(b.p, br, bg)
		draw_arc(b.p, br, 0, TAU, 36''')

# lobby dots respect fade
rep('''		draw_circle(Vector2(x + 6 * u, yy - 5 * u), 6 * u, TEAM_COL[i % TEAM_COL.size()])''', '''		circ(Vector2(x + 6 * u, yy - 5 * u), 6 * u, TEAM_COL[i % TEAM_COL.size()])''')
# headings on LAN screens use the game font
for t in ['"PLAY WITH FRIENDS", Vector2(x, y + 42 * u), 26 * u', '"JOIN A GAME", Vector2(x, y + 42 * u), 26 * u', '"TYPE HOST ADDRESS", Vector2(x, y + 40 * u), 22 * u', '"LOBBY", Vector2(x, y + 42 * u), 26 * u']:
    rep('txt(' + t, 'txh(' + t)

s += open("/home/claude/scripts/ui_block.gd").read()
open(P, "w").write(s)
print("ok")
