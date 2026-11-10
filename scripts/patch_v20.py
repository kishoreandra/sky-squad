"""v2.0: aim in sync, dual only for the same gun, quiet mine, easier easy bots, longer throws while paddling,
one switchable throw icon, net empties the jetpack, three new maps."""
import sys
P = "/home/claude/sky-squad/main.gd"
s = open(P).read()
ERR = []
def rep(a, b, c=1):
    global s
    if s.count(a) != c:
        ERR.append("expected %d got %d: %r" % (c, s.count(a), a[:120])); return
    s = s.replace(a, b)

rep('const VERSION := "1.9"', 'const VERSION := "2.0"')
rep('# Sky Squad - Arc Light Studio. Playtest build 1.9', '# Sky Squad - Arc Light Studio. Playtest build 2.0')

# 1. aim: the gun points exactly where your stick or mouse points, the moment you move it
rep('''	if p.bot or p.remote:
		p.aim = inp.aim
	else:
		var diff := wrapf(inp.aim - p.aim, -PI, PI)
		var stepmax: float = aim_rate(mouse_aiming()) * dt
		p.aim = wrapf(p.aim + clampf(diff, -stepmax, stepmax), -PI, PI)''', '''	p.aim = wrapf(float(inp.aim), -PI, PI)''')
rep('''	p.draw_aim = lerp_angle(p.draw_aim, p.aim, ease_k(22.0, dt))''', '''	# your own soldier is drawn exactly at the aim; others are smoothed a touch
	p.draw_aim = p.aim if (is_me(p) or p.bot) else lerp_angle(p.draw_aim, p.aim, ease_k(30.0, dt))''')
rep('''			shoot = lag < (0.05 if cw != null and cw.type == "sniper" else 0.3)''', '''			shoot = lag < 0.3''')

# 2. dual guns only when the gun on the floor is the same as one you carry
rep('''	return ["swap", "dual"] if is_small(k.gun) else ["swap"]''', '''	return ["swap"]''')
rep('''	elif opt == "dual":
		var cur = p.slots[p.cur]
		if cur == null or cur.type != k.gun:
			replace_current(p, k)
			cur = p.slots[p.cur]
		cur.dual = true''', '''	elif opt == "dual":
		var cur = p.slots[p.cur]
		if cur == null or cur.type != k.gun:
			return
		cur.dual = true''')

# 3. mine: only a tiny dim blink, no big warning ring
rep('''			var armed: bool = g.stuck and g.fuse > MINE_ARM
			if sin(time_s * (9.0 if armed else 3.0)) > 0.2:
				draw_circle(Vector2(g.x + 4, g.y - 5), 2.2, C_RED if armed else C_ARC)
			if armed:
				draw_arc(Vector2(g.x, g.y), MINE_R, 0, TAU, 28, Color(1, 0.25, 0.25, 0.18 + 0.08 * sin(time_s * 4.0)), 1.5, true)
			continue''', '''			var armed: bool = g.stuck and g.fuse > MINE_ARM
			if sin(time_s * (2.5 if armed else 3.0)) > 0.75:
				draw_circle(Vector2(g.x + 4, g.y - 5), 1.4, Color(1, 0.3, 0.3, 0.7) if armed else C_ARC)
			continue''')

# 4. bots: easy is really easy now, normal a little gentler
rep('''		"easy":
			st.react += 0.3
			st.err *= 1.7
			st.turn *= 0.7
			st.nade *= 0.6''', '''		"easy":
			st.react += 0.6
			st.err *= 2.6
			st.turn *= 0.5
			st.nade *= 0.3
			st["lead"] = 0.0
			st["pause"] = 2.2
			st["reach"] = 0.65
			st["extras"] = 0.3
		"normal":
			st.react += 0.12
			st.err *= 1.25
			st["pause"] = 1.3
			st["reach"] = 0.85''')
rep('''		var lead := Vector2(tg.vx, tg.vy) * 0.08 if visible else Vector2.ZERO''', '''		var lead := Vector2(tg.vx, tg.vy) * 0.08 * float(st.get("lead", 1.0)) if visible else Vector2.ZERO''')
rep('''		var reach := 1000.0 if (w != null and w.type == "sniper") else 760.0''', '''		var reach := (1000.0 if (w != null and w.type == "sniper") else 760.0) * float(st.get("reach", 1.0))''')
rep('''			if b.burst_t <= 0 and b.burst_t > -0.5 and b.pause_t <= 0:
				b.pause_t = randf_range(0.15, 0.45)''', '''			if b.burst_t <= 0 and b.burst_t > -0.5 and b.pause_t <= 0:
				b.pause_t = randf_range(0.15, 0.45) * float(st.get("pause", 1.0))''')
rep('''		if b.bombs > 0 and d < 260 and randf() < dt * 0.4:
			inp.bomb = true
		if b.smokes > 0 and d < 320 and randf() < dt * 0.35:''', '''		if b.bombs > 0 and d < 260 and randf() < dt * 0.4 * float(st.get("extras", 1.0)):
			inp.bomb = true
		if b.smokes > 0 and d < 320 and randf() < dt * 0.35 * float(st.get("extras", 1.0)):''')

# 5. throwing while paddling with your hands: allowed, and it goes further
rep('''	if p.hand_on:
		do_frag = false
		do_mine = false
		do_smoke = false
''', '''	var tm := 1.3 if p.hand_on else 1.0
''')
rep('''		g.vx = cos(p.aim) * 560 + p.vx * 0.4
		g.vy = sin(p.aim) * 560 + p.vy * 0.3''', '''		g.vx = cos(p.aim) * 560 * tm + p.vx * 0.4 * tm
		g.vy = sin(p.aim) * 560 * tm + p.vy * 0.3''')
rep('''		gb.vx = cos(p.aim) * 330 + p.vx * 0.3
		gb.vy = sin(p.aim) * 330 + p.vy * 0.2''', '''		gb.vx = cos(p.aim) * 330 * tm + p.vx * 0.3 * tm
		gb.vy = sin(p.aim) * 330 * tm + p.vy * 0.2''')
rep('''		gsm.vx = cos(p.aim) * 480 + p.vx * 0.4
		gsm.vy = sin(p.aim) * 480 + p.vy * 0.3''', '''		gsm.vx = cos(p.aim) * 480 * tm + p.vx * 0.4 * tm
		gsm.vy = sin(p.aim) * 480 * tm + p.vy * 0.3''')

# 6. one small switch icon beside the throw button; tap it to go to the next kind you have
rep('''		for kk in 3:
			out.append({"n": "TK%d" % kk, "p": Vector2(bx + inward * r * 1.95, sh * 0.30 + (kk - 1) * r * 1.3), "r": r * 0.6})''', '''		if kinds_held(me) > 1:
			out.append({"n": "TKS", "p": Vector2(bx + inward * r * 1.7, sh * 0.30 - r * 0.55), "r": r * 0.55})''')
rep('''			if b.n.begins_with("TK"):
				my_tk = int(b.n.substr(2))
				return''', '''			if b.n == "TKS":
				my_tk = next_kind(me, my_tk)
				play_ui("click")
				return''')
rep('''			"TK0", "TK1", "TK2":
				var kk2 := int(b.n.substr(2))
				var on: bool = pick_kind(me, my_tk) == kk2
				var cnt := kind_count(me, kk2)
				if on:
					draw_arc(b.p, b.r + 2 * u, 0, TAU, 32, C_ARC, 2.5 * u, true)
				var tcol := Color(1, 1, 1, 1.0 if cnt > 0 else 0.3)
				tex_c(THROW_TEX[kk2][0], b.p + Vector2(0, -1 * u), THROW_TEX[kk2][1] * u * 0.7, tcol)
				txt("%d" % cnt, b.p + Vector2(b.r * 0.7, b.r * 0.75), 9 * u, C_INK if cnt > 0 else C_MUTED, 1, 2 * u)''', '''			"TKS":
				# shows the next kind you would switch to, with a little turn arrow
				var nk := next_kind(me, my_tk)
				tex_c(THROW_TEX[nk][0], b.p + Vector2(-1 * u, 0), THROW_TEX[nk][1] * u * 0.6)
				draw_arc(b.p, b.r - 3 * u, -2.4, 1.6, 18, C_ARC, 2 * u, true)
				var tip := b.p + Vector2(cos(1.6), sin(1.6)) * (b.r - 3 * u)
				draw_colored_polygon(PackedVector2Array([tip + Vector2(-4, -1) * u, tip + Vector2(3, -3) * u, tip + Vector2(1, 4) * u]), C_ARC)''')
rep('''	for kk in 3:
		if key([KEY_1, KEY_2, KEY_3][kk]):
			my_tk = kk''', '''	for kk in 3:
		if key([KEY_1, KEY_2, KEY_3][kk]):
			my_tk = kk
	if key(KEY_T) and not tk_key:
		my_tk = next_kind(me, my_tk)
	tk_key = key(KEY_T)''')

# 7. net: the jetpack is emptied and stays empty while the net holds you, so you drop to the ground
rep('''							p.net_t = 3.5''', '''							p.net_t = 3.5
							p.fuel = 0.0''')
rep('''		p.fuel = minf(S.fuel_max, p.fuel + (S.refill_ground if p.on_ground else S.refill_air) * dt)''', '''		if p.net_t <= 0:
			p.fuel = minf(S.fuel_max, p.fuel + (S.refill_ground if p.on_ground else S.refill_air) * dt)
		else:
			p.fuel = 0.0''')
rep('''		p.pfuel = minf(S.fuel_max, p.pfuel + (S.refill_ground if p.on_ground else S.refill_air) * dt)''', '''		p.pfuel = minf(S.fuel_max, p.pfuel + (S.refill_ground if p.on_ground else S.refill_air) * dt) if p.net_t <= 0 else 0.0''')

# 8. three new maps
rep('''const MAP_LIST := ["sky", "outpost", "catacombs"]
const MAP_NAMES := {"sky": "Sky Islands", "outpost": "Outpost", "catacombs": "Catacombs", "random": "Random"}''',
    '''const MAP_LIST := ["sky", "outpost", "catacombs", "towers", "canyon", "ruins"]
const MAP_NAMES := {"sky": "Sky Islands", "outpost": "Outpost", "catacombs": "Catacombs", "towers": "Twin Towers", "canyon": "Red Canyon", "ruins": "Jungle Ruins", "random": "Random"}
const MAP_THEME := {"towers": "outpost", "canyon": "outpost", "ruins": "sky"}''')
rep('''	["map", "Map", ["sky", "outpost", "catacombs", "random"], ["Sky Islands", "Outpost", "Catacombs", "Random"]],''',
    '''	["map", "Map", ["sky", "outpost", "catacombs", "towers", "canyon", "ruins", "random"], ["Sky Islands", "Outpost", "Catacombs", "Twin Towers", "Red Canyon", "Jungle Ruins", "Random"]],''', 2)
rep('''		"catacombs":
			build_catacombs()
		_:
			build_sky()''', '''		"catacombs":
			build_catacombs()
		"towers":
			build_towers()
		"canyon":
			build_canyon()
		"ruins":
			build_ruins()
		_:
			build_sky()''')
# the look of a map (sky, sand or cave) follows its theme
for a in ['if map_id == "catacombs":', 'map_id == "outpost"', 'elif map_id == "catacombs":']:
    pass
s = s.replace('map_id == "outpost"', 'map_theme() == "outpost"').replace('map_id == "catacombs"', 'map_theme() == "catacombs"')
rep('''"catacombs": "amb_catacombs"}.get(map_id, "amb_sky")''', '''"catacombs": "amb_catacombs"}.get(map_theme(), "amb_sky")''')

s += '''
# ================= v2.0 helpers =================
var tk_key := false

func kinds_held(p: Player) -> int:
	var n := 0
	for k in 3:
		if kind_count(p, k) > 0:
			n += 1
	return n

func next_kind(p: Player, cur: int) -> int:
	cur = pick_kind(p, cur)
	for i in range(1, 4):
		var k := (cur + i) % 3
		if kind_count(p, k) > 0:
			return k
	return cur

func map_theme() -> String:
	return MAP_THEME.get(map_id, map_id)

# --- Twin Towers: two tall towers with floors, a sky bridge, a street and a tunnel under it ---
func build_towers() -> void:
	bases_v = [[2, 33, 8], [110, 33, 8]]
	water_row = 38
	zones = [{"type": "low", "rect": Rect2(48*T, 2*T, 24*T, 14*T), "g": 0.35, "f": 0.5}]
	for c in range(1, COLS - 1):
		fill(c, 39, c, ROWS - 3, DIRT)
	fill(1, ROWS - 4, COLS - 2, ROWS - 3, ROCK)
	# tunnel under the street
	fill(30, 41, 89, 42, EMPTY)
	fill(30, 39, 31, 40, EMPTY)
	fill(88, 39, 89, 40, EMPTY)
	for tx in [28, 80]:
		# tower walls with doors and window gaps
		fill(tx, 10, tx, 38, ROCK)
		fill(tx + 11, 10, tx + 11, 38, ROCK)
		for fy in [32, 26, 20, 14, 10]:
			fill(tx, fy, tx + 11, fy, ROCK)
		for fy in [32, 26, 20, 14]:
			fill(tx + 4, fy, tx + 7, fy, EMPTY)   # stair gap in each floor
		fill(tx, 34, tx, 37, EMPTY)
		fill(tx + 11, 34, tx + 11, 37, EMPTY)
		fill(tx, 22, tx, 24, EMPTY)
		fill(tx + 11, 16, tx + 11, 18, EMPTY)
		fill(tx, 16, tx, 18, EMPTY)
		fill(tx + 11, 22, tx + 11, 24, EMPTY)
		set_tile(tx + 2, 31, CRATE)
		set_tile(tx + 9, 25, CRATE)
	# sky bridge between the towers and small roofs at the sides
	fill(40, 20, 79, 20, WOOD)
	fill(57, 20, 62, 20, EMPTY)
	fill(52, 9, 67, 9, WOOD)
	fill(12, 26, 20, 26, ROCK)
	fill(99, 26, 107, 26, ROCK)
	fill(13, 15, 19, 15, WOOD)
	fill(100, 15, 106, 15, WOOD)
	# street cover
	for cx2 in [46, 52, 67, 73]:
		set_tile(cx2, 38, CRATE)
	fill(58, 37, 61, 38, ROCK)
	item_spots = [
		[60, 8, "gun", ["sniper", "rpg", "laser", "minigun"]], [59, 36, "health", []],
		[33, 31, "gun", ["ak47", "shotgun", "smg"]], [85, 31, "gun", ["ak47", "shotgun", "smg"]],
		[33, 13, "gun", ["sniper", "laser"]], [85, 13, "gun", ["sniper", "laser"]],
		[48, 19, "gun", ["uzi", "magnum", "shock", "net"]], [71, 19, "gun", ["flame", "net", "rpg"]],
		[16, 25, "health", []], [103, 25, "health", []],
		[45, 40, "grenade", []], [74, 40, "bomb", []], [60, 40, "smoke", []],
		[16, 14, "gun", ["uzi", "shotgun"]], [103, 14, "gun", ["smg", "shotgun"]],
	]

# --- Red Canyon: two mesas, a deep canyon with a rope bridge, caves in the walls ---
func build_canyon() -> void:
	bases_v = [[3, 18, 9], [108, 18, 9]]
	water_row = 40
	zones = [{"type": "heavy", "rect": Rect2(46*T, 30*T, 28*T, 10*T), "g": 1.8, "f": 2.0}]
	for c in range(1, COLS - 1):
		var top: int
		if c < 40:
			top = 19 + roundi(1.2 * sin(c * 0.2))
		elif c > 79:
			top = 19 + roundi(1.2 * sin(c * 0.17 + 1.0))
		else:
			var k := absf(c - 59.5) / 20.0
			top = 41 - roundi((1.0 - k * k) * 0.0 + k * k * 22.0)
		fill(c, top, c, ROWS - 3, DIRT)
	fill(1, ROWS - 4, COLS - 2, ROWS - 3, ROCK)
	# caves in the canyon walls and inside the mesas
	carve_ellipse(30, 27, 7, 3)
	carve_ellipse(89, 27, 7, 3)
	fill(36, 26, 44, 28, EMPTY)
	fill(75, 26, 83, 28, EMPTY)
	carve_ellipse(14, 30, 8, 3)
	carve_ellipse(105, 30, 8, 3)
	fill(13, 20, 15, 28, EMPTY)
	fill(104, 20, 106, 28, EMPTY)
	# rope bridge across the canyon and floating rock steps
	fill(40, 18, 79, 18, WOOD)
	fill(58, 18, 61, 18, EMPTY)
	fill(50, 30, 54, 30, ROCK)
	fill(65, 30, 69, 30, ROCK)
	fill(57, 24, 62, 24, ROCK)
	# rock pillars on the mesas
	for px in [24, 95]:
		fill(px, 14, px + 1, 18, ROCK)
	fill(20, 10, 28, 10, WOOD)
	fill(91, 10, 99, 10, WOOD)
	for cx2 in [10, 35, 84, 109]:
		set_tile(cx2, surface_below(cx2, 10) - 1, CRATE)
	item_spots = [
		[59, 22, "gun", ["sniper", "rpg", "laser", "minigun"]], [59, 38, "health", []],
		[24, 9, "gun", ["sniper", "laser"]], [95, 9, "gun", ["sniper", "laser"]],
		[30, 27, "gun", ["ak47", "shotgun", "smg", "flame"]], [89, 27, "gun", ["ak47", "shotgun", "smg", "flame"]],
		[52, 29, "grenade", []], [67, 29, "bomb", []],
		[14, 29, "health", []], [105, 29, "health", []],
		[45, 17, "gun", ["uzi", "magnum", "shock", "net"]], [74, 17, "gun", ["uzi", "magnum", "shock", "net"]],
		[59, 17, "smoke", []],
	]

# --- Jungle Ruins: a stepped temple in the middle, broken stone arches, a river below ---
func build_ruins() -> void:
	bases_v = [[2, 30, 9], [109, 30, 9]]
	water_row = 36
	zones = [{"type": "low", "rect": Rect2(46*T, 2*T, 28*T, 12*T), "g": 0.35, "f": 0.5}]
	for c in range(1, COLS - 1):
		var g := 35 + roundi(1.5 * sin(c * 0.09) + 0.8 * sin(c * 0.23 + 2.0))
		if c > 33 and c < 44 or c > 75 and c < 86:
			g = 40   # river beds
		fill(c, g, c, ROWS - 3, DIRT)
	fill(1, ROWS - 4, COLS - 2, ROWS - 3, ROCK)
	for bs in [[2, 30, 9], [109, 30, 9]]:
		fill(bs[0], bs[1] + 1, bs[0] + bs[2] - 1, 34, ROCK)
	# stepped temple
	var steps := [[44, 75, 34], [47, 72, 30], [50, 69, 26], [53, 66, 22], [56, 63, 18]]
	for st in steps:
		fill(st[0], st[2], st[1], st[2], ROCK)
		fill(st[0], st[2] + 1, st[0], 34, ROCK)
		fill(st[1], st[2] + 1, st[1], 34, ROCK)
	for st in steps:
		fill(st[0] + 1, st[2] + 1, st[1] - 1, st[2] + 2, EMPTY)
	fill(57, 13, 62, 13, ROCK)
	fill(59, 14, 60, 17, EMPTY)
	fill(44, 31, 44, 33, EMPTY)
	fill(75, 31, 75, 33, EMPTY)
	# broken arches and tree platforms
	for ax in [18, 96]:
		fill(ax, 22, ax + 7, 22, ROCK)
		fill(ax, 23, ax, 30, ROCK)
		fill(ax + 7, 23, ax + 7, 27, ROCK)
	fill(30, 16, 37, 16, WOOD)
	fill(82, 16, 89, 16, WOOD)
	fill(8, 15, 14, 15, WOOD)
	fill(105, 15, 111, 15, WOOD)
	# log bridges over the rivers
	fill(34, 35, 43, 35, WOOD)
	fill(76, 35, 85, 35, WOOD)
	for cx2 in [26, 49, 70, 93]:
		set_tile(cx2, surface_below(cx2, 25) - 1, CRATE)
	item_spots = [
		[59, 12, "gun", ["sniper", "rpg", "laser", "minigun"]], [59, 21, "health", []],
		[48, 29, "gun", ["ak47", "shotgun", "smg"]], [71, 29, "gun", ["ak47", "shotgun", "smg"]],
		[21, 21, "gun", ["sniper", "laser"]], [99, 21, "gun", ["sniper", "laser"]],
		[33, 15, "gun", ["uzi", "magnum", "shock", "net"]], [86, 15, "gun", ["flame", "net", "rpg"]],
		[38, 39, "health", []], [80, 39, "health", []],
		[11, 14, "grenade", []], [108, 14, "smoke", []], [59, 33, "bomb", []],
	]
'''
if ERR:
    print("\n".join(ERR)); sys.exit(1)
open(P, "w").write(s)
print("ok")
