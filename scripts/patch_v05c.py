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

# fix bomb landing line + in-flight fuse
rep('''				g.y = floori(ny / T) * T - 5.0 if g.vy <= 0 else g.y
''', '')
rep('''			explode(g.x, g.y, S.grenade_radius, S.grenade_dmg, g.owner, "grenade")
			grenades_list.remove_at(i)''', '''			if g.kind == "bomb":
				explode(g.x, g.y, 120.0, 115.0, g.owner, "bomb")
			else:
				explode(g.x, g.y, S.grenade_radius, S.grenade_dmg, g.owner, "grenade")
			grenades_list.remove_at(i)''')
# ---- sky + HD layers ----
rep('''	var pts := PackedVector2Array([Vector2(0, 0), Vector2(sw, 0), Vector2(sw, sh), Vector2(0, sh)])
	var top := Color("#4c98d8")
	var hor := Color("#cfe6f2")
	draw_polygon(pts, PackedColorArray([top, top, hor, hor]))''', '''	var top := Color("#3a7fca")
	var mid := Color("#7fbbe8")
	var hor := Color("#dcEEF7")
	var my := sh * 0.45
	draw_polygon(PackedVector2Array([Vector2(0, 0), Vector2(sw, 0), Vector2(sw, my), Vector2(0, my)]), PackedColorArray([top, top, mid, mid]))
	draw_polygon(PackedVector2Array([Vector2(0, my), Vector2(sw, my), Vector2(sw, sh), Vector2(0, sh)]), PackedColorArray([mid, mid, hor, hor]))''')
rep('''	layer("bg_mountains", 0.10, 0.66, 0.62, Color("#6c8eb4"))
	layer("bg_hills", 0.25, 0.80, 0.85, Color("#4c8054"))
	layer("bg_near", 0.42, 0.93, 0.95, Color("#38623e"))''', '''	layer("bg_mountains", 0.10, 0.66, 0.31, Color("#7e9cc0"))
	layer("bg_hills", 0.25, 0.80, 0.425, Color("#42724a"))
	layer("bg_near", 0.42, 0.93, 0.475, Color("#2e5434"))''')
# ---- world draws: net bullets, bombs, tracers ----
rep('''	for b in bullets:
		if b.rocket:''', '''	for b in bullets:
		if b.net:
			draw_set_transform_matrix(wt * Transform2D(time_s * 9.0, Vector2.ONE, 0.0, Vector2(b.x, b.y)))
			draw_texture_rect(tex.net_overlay, Rect2(-9, -11, 18, 22), false)
			draw_set_transform_matrix(wt)
			continue
		if b.rocket:''')
rep('''	for g in grenades_list:
		draw_set_transform_matrix(wt * Transform2D(g.rot, Vector2.ONE, 0.0, Vector2(g.x, g.y)))''', '''	for g in grenades_list:
		if g.kind == "bomb":
			draw_set_transform_matrix(wt)
			draw_texture_rect(tex.timebomb, Rect2(g.x - 8, g.y - 6, 16, 12), false)
			if sin(time_s * (6.0 + (4.5 - g.fuse) * 3.0)) > 0:
				draw_circle(Vector2(g.x + 4, g.y - 5), 2.0, C_RED)
			txt(str(ceili(g.fuse)), Vector2(g.x, g.y - 10), 11, C_RED, 1, 3)
			continue
		draw_set_transform_matrix(wt * Transform2D(g.rot, Vector2.ONE, 0.0, Vector2(g.x, g.y)))''')
rep('''	for tr in tracers:
		var ta: float = clampf(tr.t / 0.22, 0, 1)
		draw_line(tr.a, tr.b, Color(1, 0.75, 0.3, 0.35 * ta), 6.0 * ta + 1.0, true)
		draw_line(tr.a, tr.b, Color(1, 1, 0.92, 0.95 * ta), 2.2 * ta + 0.6, true)''', '''	for tr in tracers:
		var ta: float = clampf(tr.t / tr.get("max", 0.22), 0, 1)
		match tr.get("kind", "line"):
			"laser":
				draw_line(tr.a, tr.b, Color(0.2, 0.9, 1, 0.35 * ta), 9.0 * ta + 1.0, true)
				draw_line(tr.a, tr.b, Color(0.85, 1, 1, ta), 2.6 * ta + 0.6, true)
			"zig":
				var pts := PackedVector2Array()
				var dv: Vector2 = tr.b - tr.a
				var nrm := Vector2(-dv.y, dv.x).normalized()
				for i in 9:
					var kk := i / 8.0
					var j := 0.0 if (i == 0 or i == 8) else randf_range(-7, 7)
					pts.append(tr.a + dv * kk + nrm * j)
				draw_polyline(pts, Color(0.55, 0.95, 1, 0.8 * ta), 4.0, true)
				draw_polyline(pts, Color(1, 1, 1, ta), 1.6, true)
			_:
				draw_line(tr.a, tr.b, Color(0.85, 0.92, 1, 0.35 * ta), 6.0 * ta + 1.0, true)
				draw_line(tr.a, tr.b, Color(1, 1, 1, 0.95 * ta), 2.2 * ta + 0.6, true)''')
# ---- player drawing: switch dip, knife, net, stun, team tags ----
rep('''	gun_rot += 0.5 * p.reload_k
	draw_set_transform_matrix(body)''', '''	gun_rot += 0.5 * p.reload_k
	if p.switch_t > 0:
		gun_rot += 1.1 * sin(PI * clampf(p.switch_t / 0.22, 0, 1))
	var mk := clampf(1.0 - p.melee_anim / 0.28, 0, 1) if p.melee_anim > 0 else -1.0
	if mk >= 0:
		gun_rot += 0.7 * sin(mk * PI)
	draw_set_transform_matrix(body)''')
rep('''	if p.muzzle_t > 0 and gun != "rpg":''', '''	if p.muzzle_t > 0 and gun != "rpg" and not ["laser", "shock", "net"].has(gun):''')
rep('''	if p.melee_anim > 0:
		draw_arc(Vector2(6, 0), 30, -0.9, 0.9, 14, Color(1, 1, 1, 0.8), 3, true)
	draw_set_transform_matrix(body)
	var fh := grip if dual else front_hand''', '''	if p.muzzle_t > 0 and (gun == "laser" or gun == "shock"):
		var mz2 := Vector2(m.muzzle[0] - m.grip[0], m.muzzle[1] - m.grip[1]) * gd
		draw_texture_rect(tex.glow, Rect2(mz2 - Vector2(8, 8), Vector2(16, 16)), false, Color(0.5, 0.95, 1, 0.9))
	draw_set_transform_matrix(body)
	var fh := grip if dual else front_hand
	var ka := 0.0
	if mk >= 0:
		var e := mk * mk * (3.0 - 2.0 * mk)
		ka = lerpf(-1.7, 0.9, e)
		fh = sh_pt + Vector2(cos(ka), sin(ka)) * 12.0''')
rep('''	draw_texture_rect(tex.hand, Rect2(fh - Vector2(3, 3), Vector2(6, 6)), false)
	draw_texture_rect(tex.hand, Rect2(grip - Vector2(3, 3), Vector2(6, 6)), false)''', '''	draw_texture_rect(tex.hand, Rect2(fh - Vector2(3, 3), Vector2(6, 6)), false)
	draw_texture_rect(tex.hand, Rect2(grip - Vector2(3, 3), Vector2(6, 6)), false)
	if mk >= 0:
		draw_arc(sh_pt, 24, -1.7, ka, 14, Color(1, 1, 1, 0.55 * (1.0 - mk) + 0.15), 4, true)
		draw_set_transform_matrix(body * Transform2D(ka, Vector2.ONE, 0.0, fh))
		draw_texture_rect(tex.knife, Rect2(-3, -3, 18, 6), false)
		draw_set_transform_matrix(body)''')
rep('''	draw_set_transform_matrix(wt)
	var hpos := head_pos(p)
	var ty := hpos.y - 24 if gs > 0 else hpos.y + 34
	if p.bot:
		txt(p.pname, Vector2(c.x, ty), 11, p.color, 1, 3)''', '''	draw_set_transform_matrix(wt)
	if p.net_t > 0:
		var nsz := Vector2(48, 30) if prone else Vector2(36, 46)
		tex_c("net_overlay", c + Vector2(0, -4 * gs), nsz, Color(1, 1, 1, clampf(p.net_t, 0, 1)))
	if p.stun_t > 0:
		for i in 3:
			var zp := PackedVector2Array()
			var ang0 := randf() * TAU
			for j in 6:
				var aa := ang0 + j * 0.5
				zp.append(c + Vector2(cos(aa), sin(aa)) * randf_range(14, 24))
			draw_polyline(zp, Color(0.6, 0.95, 1, 0.85), 1.6, true)
	var hpos := head_pos(p)
	var ty := hpos.y - 24 if gs > 0 else hpos.y + 34
	var tag_col: Color = p.color
	if cfg.mode == "team":
		tag_col = Color("#5ec8ff") if p.side == 0 else Color("#ff6b6b")
	if p.bot or cfg.mode == "team":
		txt(p.pname, Vector2(c.x, ty), 11, tag_col, 1, 3)''')
rep('''	if k.type == "grenade":
		tex_c("grenade", cpos + Vector2(-5, 0), Vector2(12, 14))''', '''	if k.type == "bomb":
		tex_c("timebomb", cpos, Vector2(18, 14))
		txt("TIME BOMB", cpos + Vector2(0, -12), 8, Color.WHITE, 1, 3)
		return
	if k.type == "grenade":
		tex_c("grenade", cpos + Vector2(-5, 0), Vector2(12, 14))''')
# bubble: near guns
rep('''func draw_bubble(me: Player) -> void:
	var k = floor_gun(me)''', '''func draw_bubble(me: Player) -> void:
	var k = near_gun(me)''')
rep('''				var ic: String = {"grenade": "BOOM", "rpg": "BOOM", "melee": "HIT"}.get(f.gun, ">")''', '''				var ic: String = {"grenade": "BOOM", "rpg": "BOOM", "bomb": "BOOM", "melee": "KNIFE"}.get(f.gun, ">")''')
# white sniper line
rep('''			draw_line(s0, s0 + Vector2(cos(me.aim), sin(me.aim)) * sw, Color(1, 0.1, 0.1, 0.45), 1.2 * u, true)''', '''			draw_dashed_line(s0, s0 + Vector2(cos(me.aim), sin(me.aim)) * sw, Color(1, 1, 1, 0.45), 1.4 * u, 8 * u)''')
# team score in timer box + pause button
rep('''	txt("KILLS %d   DEATHS %d" % [me.kills, me.deaths], Vector2(sw / 2, 46 * u), 9 * u, C_MUTED, 1)''', '''	if cfg.mode == "team":
		var ts := team_scores()
		txt("BLUE %d  :  %d RED" % [ts[0], ts[1]], Vector2(sw / 2, 46 * u), 10 * u, C_INK, 1)
	else:
		txt("KILLS %d   DEATHS %d" % [me.kills, me.deaths], Vector2(sw / 2, 46 * u), 9 * u, C_MUTED, 1)
	pause_rect = Rect2(sw / 2 - 98 * u, 12 * u, 34 * u, 34 * u)
	rbox(pause_rect, Color(0.04, 0.05, 0.12, 0.55), 17 * u)
	draw_rect(Rect2(pause_rect.position + Vector2(11 * u, 10 * u), Vector2(4 * u, 14 * u)), C_INK)
	draw_rect(Rect2(pause_rect.position + Vector2(19 * u, 10 * u), Vector2(4 * u, 14 * u)), C_INK)''')
rep('''func ranked() -> Array:''', '''func team_scores() -> Array:
	var ts := [0, 0]
	for p in players:
		ts[p.side % 2] += p.kills
	return ts

func ranked() -> Array:''')
open(p, 'w').write(s)
print("c ok")
