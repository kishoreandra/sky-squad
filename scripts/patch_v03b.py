import re
p = '/home/claude/skysquad/main.gd'
s = open(p).read()
def rep(a, b, count=1):
    global s
    n = s.count(a)
    assert n == count, (n, a[:90])
    s = s.replace(a, b)

rep('''var menu_btn := Rect2()''', '''var menu_btn := Rect2()
var pick_request := false
var zoom_request := false
var bubble_on := false
var bubble_pos := Vector2.ZERO
var bubble_r := 30.0
var last_delta := 0.016''')
# buttons
rep('''func buttons() -> Array:
	var names := ["GRENADE", "SWAP", "MELEE", "RELOAD"]
	var ys := [0.30, 0.45, 0.60, 0.75]
	var r := clampf(sh * 0.065, 22 * u, 34 * u)
	var out := []
	for i in 4:
		out.append({"n": names[i], "p": Vector2(sw - safe_r - r - 14 * u, sh * ys[i]), "r": r})
	return out''', '''func buttons() -> Array:
	var names := ["GRENADE", "SWAP", "MELEE", "RELOAD"]
	var ys := [0.30, 0.45, 0.60, 0.75]
	var r := clampf(sh * 0.065, 22 * u, 34 * u)
	var bx := sw - safe_r - r - 14 * u
	var out := []
	for i in 4:
		out.append({"n": names[i], "p": Vector2(bx, sh * ys[i]), "r": r})
	if state == "play" and not players.is_empty() and players[0].alive:
		var w = players[0].slots[players[0].cur]
		if w != null and WD[w.type].zooms.size() > 1:
			out.append({"n": "ZOOM", "p": Vector2(bx - r * 2.5, sh * 0.30), "r": r * 0.85})
	out.append({"n": "SIT", "p": Vector2(safe_l + r + 14 * u, sh * 0.42), "r": r * 0.85})
	return out''')
# mouse wheel + bubble click
rep('''	elif event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT:
		mouse_down = event.pressed
		mouse_used = true
		touch_mode = false
		mouse_pos = event.position
		if event.pressed and state != "play":
			menu_tap(event.position)''', '''	elif event is InputEventMouseButton and (event.button_index == MOUSE_BUTTON_WHEEL_UP or event.button_index == MOUSE_BUTTON_WHEEL_DOWN):
		if event.pressed:
			zoom_request = true
	elif event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT:
		mouse_down = event.pressed
		mouse_used = true
		touch_mode = false
		mouse_pos = event.position
		if event.pressed and state != "play":
			menu_tap(event.position)
		elif event.pressed and bubble_on and event.position.distance_to(bubble_pos) < bubble_r + 8 * u:
			pick_request = true
			mouse_down = false''')
rep('''	if state != "play":
		menu_tap(pos)
		return
	for b in buttons():''', '''	if state != "play":
		menu_tap(pos)
		return
	if bubble_on and pos.distance_to(bubble_pos) < bubble_r + 10 * u:
		pick_request = true
		return
	for b in buttons():''')
# human input
rep('''		if d.y < -rad * 0.42:
			fly = true
	var c := center(me)''', '''		if d.y < -rad * 0.42:
			fly = true
		if d.y > rad * 0.6 and absf(d.x) < rad * 0.5:
			inp.down = true
	var c := center(me)''')
rep('''	inp.reload = key(KEY_R) or btn_held.has("RELOAD")''', '''	inp.reload = key(KEY_R) or btn_held.has("RELOAD")
	var stick_down: bool = stick_l != null and (stick_l.pos - stick_l.o).y > rad * 0.6 and absf((stick_l.pos - stick_l.o).x) < rad * 0.5
	inp.down = key(KEY_S) or key(KEY_DOWN) or btn_held.has("SIT") or stick_down
	inp.pick = key(KEY_E) or pick_request
	inp.zoom = key(KEY_Z) or btn_held.has("ZOOM") or zoom_request''')
rep('''	t += dt
	human_input()''', '''	t += dt
	human_input()
	pick_request = false
	zoom_request = false''')
# view + camera
rep('''	var want_view: float = S.view_h
	if state == "play" and not players.is_empty() and players[0].alive:
		var w = players[0].slots[players[0].cur]
		if w != null and w.type == "sniper" and (stick_r != null or mouse_aiming()):
			want_view = S.view_h_scope
	view_h = move_toward(view_h, want_view, delta * 500)''', '''	last_delta = delta
	var want_view: float = S.view_h
	if state == "play" and not players.is_empty() and players[0].alive:
		want_view = S.view_h * ZOOM_MULT[zoom_level(players[0])]
	view_h = lerpf(view_h, want_view, ease_k(4.0, delta))''')
rep('''		var look := Vector2(cos(me.aim), sin(me.aim)) * (90.0 if view_h > S.view_h + 50 else 40.0)''',
    '''		var look := Vector2(cos(me.aim), sin(me.aim)) * (40.0 + (view_h / S.view_h - 1.0) * vw * 0.3)''')
rep('''				cam += (want - cam) * 0.12''', '''				cam += (want - cam) * ease_k(6.0, last_delta)''')
# laser + zoom tag
rep('''		if w2 != null and w2.type == "sniper" and view_h > S.view_h + 50:
			var s0 := w2s(muzzle_pos(me, "sniper"))''', '''		if w2 != null and zoom_level(me) > 1:
			var s0 := w2s(muzzle_pos(me, w2.type))''')
rep('''		gun_icon(w.type, pc + Vector2(-40 * u, -2 * u), 74 * u)''', '''		gun_icon(w.type, pc + Vector2(-40 * u, -2 * u), 74 * u)
		if zoom_level(me) > 1:
			txt("%dX" % zoom_level(me), Vector2(pc.x - 84 * u, pc.y - 10 * u), 11 * u, C_CYAN, 0, 3 * u)
		if me.posture != "stand":
			txt("CRAWLING" if me.posture == "prone" else "SITTING", Vector2(pc.x, pc.y - 30 * u), 10 * u, C_MUTED, 1, 3 * u)''')
# bubble replaces text hint
rep('''	elif state == "play":
		for k in pickups:
			if (k.type == "gun" or k.type == "drop") and overlaps(me, k):
				var auto := false
				for s2 in me.slots:
					if s2 == null or not has_ammo(s2) or (s2.type == k.gun and s2.spare < WD[k.gun].spare * 2):
						auto = true
				if not auto:
					txt("Tap SWAP to pick up the %s" % WD[k.gun].name, Vector2(sw / 2, sh - 80 * u), 13 * u, C_CYAN, 1, 3 * u)
				break''', '''	elif state == "play":
		draw_bubble(me)''')
rep('''func draw_hud() -> void:
	var me: Player = players[0]''', '''func draw_bubble(me: Player) -> void:
	var k = floor_gun(me)
	if k == null or can_auto_take(me, k):
		return
	var r := 30.0 * u * (1.0 + 0.04 * sin(time_s * 5.0))
	var pc := w2s(center(me))
	var pos := Vector2(pc.x, maxf(pc.y - 78 * u, 70 * u))
	draw_colored_polygon(PackedVector2Array([pos + Vector2(-9 * u, r * 0.8), pos + Vector2(9 * u, r * 0.8), pos + Vector2(0, r + 14 * u)]), Color(1, 1, 1, 0.95))
	draw_circle(pos, r + 2 * u, Color(0.1, 0.12, 0.2, 0.9))
	draw_circle(pos, r, Color(1, 1, 1, 0.95))
	gun_icon(k.gun, pos + Vector2(0, -3 * u), r * 1.6)
	txt(WD[k.gun].name, pos + Vector2(0, r * 0.62), 9 * u, Color("#1b1d2a"), 1)
	var hint := "TAP TO SWAP" if touch_mode or OS.has_feature("mobile") else "CLICK OR PRESS E"
	txt(hint, pos + Vector2(0, -r - 8 * u), 10 * u, C_ARC, 1, 3 * u)
	bubble_on = true
	bubble_pos = pos
	bubble_r = r

func draw_hud() -> void:
	bubble_on = false
	var me: Player = players[0]''')
# touch buttons labels
rep('''			_:
				txt(b.n, b.p + Vector2(0, 4 * u), 9 * u, C_INK, 1, 2 * u)''', '''			"ZOOM":
				txt("%dX" % zoom_level(me), b.p + Vector2(0, 2 * u), 14 * u, C_CYAN, 1, 3 * u)
				txt("ZOOM", b.p + Vector2(0, b.r * 0.6), 8 * u, C_INK, 1, 2 * u)
			"SIT":
				var w3 = me.slots[me.cur]
				var lab := "SIT"
				if me.posture == "crouch":
					lab = "LIE" if (w3 != null and w3.type == "sniper") else "STAND"
				elif me.posture == "prone":
					lab = "STAND"
				txt(lab, b.p + Vector2(0, 4 * u), 10 * u, C_INK, 1, 2 * u)
			_:
				txt(b.n, b.p + Vector2(0, 4 * u), 9 * u, C_INK, 1, 2 * u)''')
# menu text
rep('''		"Keyboard: A/D move, W fly, mouse aim + click, G grenade, F melee, Q swap, R reload.",''',
    '''		"Keyboard: A/D move, W fly, S sit, mouse aim + click, E pick up, Q swap, Z zoom, G grenade.",''')
rep('''		"Aim for the head for extra damage. The sniper waits on the top platform.",''',
    '''		"Sit for steadier aim. With the sniper, sit twice to lie down and crawl.",''')

# new draw_player
start = s.index('func draw_player(p: Player, wt: Transform2D) -> void:')
end = s.index('func draw_leg(base: Transform2D')
s = s[:start] + '''func draw_player(p: Player, wt: Transform2D) -> void:
	if not p.alive:
		return
	var c := center(p)
	var face := 1.0 if cos(p.draw_aim) >= 0 else -1.0
	var gs := gsign()
	var base := wt * Transform2D(0.0, Vector2(face, gs), 0.0, c)
	var la := atan2(sin(p.draw_aim) * gs, cos(p.draw_aim) * face)
	var tint := Color(1.6, 1.6, 1.6) if p.flash > 0 else Color.WHITE
	var prone := p.posture == "prone"
	var crouch := p.posture == "crouch"
	var bob := 0.0
	if p.on_ground and not prone:
		bob = sin(time_s * 2.4 + p.id) * 0.5 if absf(p.vx) < 15 else -absf(sin(p.walk)) * 1.2
	var body: Transform2D
	var gun_rot := la
	if prone:
		body = base * Transform2D(PI / 2, Vector2.ONE, 0.0, Vector2(-4, 1))
		gun_rot = la - PI / 2
	else:
		body = base * Transform2D(0.0, Vector2.ONE, 0.0, Vector2(0, (6.0 if crouch else 0.0) + bob))
	gun_rot += 0.5 * p.reload_k
	draw_set_transform_matrix(body)
	if p.jet_on:
		var fl := 16.0 + sin(time_s * 38.0 + p.id) * 4.0 + sin(time_s * 21.0) * 2.0
		for nx in [-12.0, -6.0]:
			draw_texture_rect(tex.glow, Rect2(nx - 6, 9, 12, fl), false, Color(1, 0.62, 0.2, 0.95))
			draw_texture_rect(tex.glow, Rect2(nx - 3.5, 9, 7, fl * 0.6), false, Color(1, 0.95, 0.7, 1))
	draw_leg(body, Vector2(-3, 4), p.leg_b, Color(0.78, 0.78, 0.78) * tint)
	draw_set_transform_matrix(body)
	draw_texture_rect(tex.jetpack, Rect2(-16, -12, 12, 20), false, tint)
	var w = p.slots[p.cur]
	var gun: String = w.type if w != null else "magnum"
	var m: Dictionary = META.GUN[gun]
	var gd: float = S.gun_draw
	var sh_pt := Vector2(1, -6)
	var dir := Vector2(cos(gun_rot), sin(gun_rot))
	var grip := sh_pt + dir * (7.0 - p.recoil)
	var front_hand := grip + (Vector2(m.front[0] - m.grip[0], m.front[1] - m.grip[1]) * gd).rotated(gun_rot)
	var sleeve: Color = p.color.darkened(0.2)
	draw_line(sh_pt + Vector2(-2, 0), grip, C_OUT, 6.0, true)
	draw_line(sh_pt + Vector2(-2, 0), grip, sleeve * tint, 4.0, true)
	draw_texture_rect(tex["torso_" + p.team], Rect2(-10, -13, 20, 20), false, tint)
	draw_leg(body, Vector2(3, 4), p.leg_f, tint)
	var head_rot := clampf(la, -0.5, 0.5) * 0.35 + (-PI / 2 if prone else 0.0)
	draw_set_transform_matrix(body * Transform2D(head_rot, Vector2.ONE, 0.0, Vector2(1, -15)))
	draw_texture_rect(tex["head_" + p.team], Rect2(-13, -14, 26, 26), false, tint)
	draw_set_transform_matrix(body * Transform2D(gun_rot, Vector2.ONE, 0.0, grip))
	var gsz := Vector2(m.size[0], m.size[1]) * gd
	draw_texture_rect(tex["gun_" + gun], Rect2(-m.grip[0] * gd, -m.grip[1] * gd, gsz.x, gsz.y), false, tint)
	if p.muzzle_t > 0 and gun != "rpg":
		var mz := Vector2(m.muzzle[0] - m.grip[0], m.muzzle[1] - m.grip[1]) * gd
		var fw := 24.0 * (1.3 if gun == "shotgun" else 1.0)
		draw_texture_rect(tex.flash, Rect2(mz.x - 1, mz.y - 7, fw, 14), false)
	if p.melee_anim > 0:
		draw_arc(Vector2(6, 0), 30, -0.9, 0.9, 14, Color(1, 1, 1, 0.8), 3, true)
	draw_set_transform_matrix(body)
	draw_line(sh_pt + Vector2(3, 0), front_hand, C_OUT, 6.0, true)
	draw_line(sh_pt + Vector2(3, 0), front_hand, p.color * tint, 4.0, true)
	draw_texture_rect(tex.hand, Rect2(front_hand - Vector2(3, 3), Vector2(6, 6)), false)
	draw_texture_rect(tex.hand, Rect2(grip - Vector2(3, 3), Vector2(6, 6)), false)
	draw_set_transform_matrix(wt)
	var hpos := head_pos(p)
	var ty := hpos.y - 24 if gs > 0 else hpos.y + 34
	if p.bot:
		txt(p.pname, Vector2(c.x, ty), 11, p.color, 1, 3)
		rbox(Rect2(c.x - 15, ty + 3, 30, 5), Color(0, 0, 0, 0.55), 2)
		rbox(Rect2(c.x - 15, ty + 3, 30 * clampf(p.hp / S.hp_max, 0, 1), 5), C_GREEN if p.hp > 40 else C_RED, 2)
	if p.say_t > 0:
		var bw := font.get_string_size(p.say, 0, -1, 11).x + 14
		rbox(Rect2(c.x - bw / 2, ty - 30, bw, 19), Color(1, 1, 1, 0.92), 8)
		txt(p.say, Vector2(c.x, ty - 16), 11, Color("#1b1d2a"), 1)

''' + s[end:]
open(p, 'w').write(s)
print("patched part 2")
