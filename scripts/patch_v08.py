"""v0.8: three maps (Sky Islands, Outpost, Catacombs) + death yells and pain grunts."""
import re, sys
P = "/home/claude/skysquad/main.gd"
s = open(P).read()

def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        sys.exit(f"expected {count} got {n}: {old[:100]!r}")
    s = s.replace(old, new)

rep('# Sky Squad - Arc Light Studio. Playtest build 0.7', '# Sky Squad - Arc Light Studio. Playtest build 0.8')
rep('const VERSION := "0.7"', 'const VERSION := "0.8"')

# ---------- sounds: death yells for everyone nearby, pain grunts ----------
rep('''"tick", "crown", "spawn"]:''', '''"tick", "crown", "spawn", "die0", "die1", "die2", "ow0", "ow1"]:''')
rep('''	p.hp = 0
	var k = p.last_hit_by''', '''	p.hp = 0
	play("die%d" % (randi() % 3), center(p), 2.0 if is_me(p) else -1.0, 0.06)
	var k = p.last_hit_by''')
rep('''		me_fx(p, "snd", ["death", -2.0])
		k.kills += 1''', '''		k.kills += 1''')
rep('''		me_fx(k, "snd", ["suicide", -4.0])
		me_fx(p, "snd", ["death", -2.0])''', '''		me_fx(k, "snd", ["suicide", -4.0])''')
rep('''		me_fx(p, "snd", ["suicide" if own else "death", -3.0])''', '''		if own:
			me_fx(p, "snd", ["suicide", -5.0])''')
rep('''	p.hp -= amt
	p.last_hit_t = t''', '''	p.hp -= amt
	if p.hp > 0 and amt >= 7.0 and cause != "water" and cause != "gas" and t - p.grunt_t > 0.8:
		p.grunt_t = t
		play("ow%d" % (randi() % 2), center(p), -4.0 if is_me(p) else -9.0, 0.1)
	p.last_hit_t = t''')
rep('\tvar actor := false\n', '\tvar actor := false\n\tvar grunt_t := -9.0\n')

# ---------- map data ----------
rep('const WATER_ROW := 36\n', '')
rep('''	[44, -1, "health", []], [76, -1, "health", []], [60, 38, "grenade", []],''', '''	[44, 30, "health", []], [76, 30, "health", []], [60, 38, "grenade", []],''')
rep('''var zones := [
	{"type": "low", "rect": Rect2(44*T, 3*T, 32*T, 14*T), "g": 0.35, "f": 0.5},
	{"type": "heavy", "rect": Rect2(80*T, 28*T, 22*T, 12*T), "g": 1.8, "f": 2.0},
]''', '''var zones: Array = []
var map_id := "sky"
var bases_v: Array = []
var item_spots: Array = []
var water_row := 36
var roam_pts: Array = []
var surf_runs: Array = []
var torches: Array = []
const MAP_LIST := ["sky", "outpost", "catacombs"]
const MAP_NAMES := {"sky": "Sky Islands", "outpost": "Outpost", "catacombs": "Catacombs", "random": "Random"}
const OUTPOST_SPOTS := [
	[50, 8, "gun", ["sniper", "rpg", "laser", "minigun"]], [59, 9, "health", []],
	[35, 20, "gun", ["ak47", "shotgun", "smg", "flame"]], [84, 20, "gun", ["ak47", "shotgun", "smg", "flame"]],
	[24, 18, "health", []], [95, 18, "health", []],
	[53, 26, "gun", ["uzi", "magnum", "shock", "net"]], [66, 26, "gun", ["smg", "ak47", "rpg"]],
	[55, 32, "grenade", []], [64, 32, "smoke", []],
	[15, 12, "gun", ["sniper", "laser"]], [104, 12, "gun", ["sniper", "laser"]],
	[33, 6, "bomb", []], [86, 6, "bomb", []],
	[42, 30, "gun", ["magnum", "uzi", "smg"]], [78, 30, "gun", ["magnum", "uzi", "minigun"]],
	[30, 30, "smoke", []], [89, 30, "grenade", []],
]
const CATA_SPOTS := [
	[20, 4, "gun", ["sniper", "rpg", "laser", "minigun"]], [100, 4, "gun", ["sniper", "rpg", "laser", "minigun"]],
	[60, 3, "health", []],
	[17, 15, "health", []], [102, 15, "health", []],
	[46, 14, "gun", ["ak47", "shotgun", "smg", "flame"]], [74, 14, "gun", ["ak47", "shotgun", "smg", "flame"]],
	[54, 23, "smoke", []], [66, 23, "grenade", []],
	[26, 31, "gun", ["magnum", "uzi", "shock", "net"]], [94, 31, "gun", ["magnum", "uzi", "smg", "net"]],
	[60, 34, "health", []], [40, 31, "bomb", []], [80, 31, "bomb", []], [11, 31, "grenade", []],
	[70, 31, "smoke", []],
]''')
rep('''	"ev_water": true, "ev_roof": true, "ev_brk": true, "ev_flip": false, "zones": false,''', '''	"ev_water": true, "ev_roof": true, "ev_brk": true, "ev_flip": false, "zones": false, "map": "sky",''')
for rows in ('MATCH_ROWS', 'LAN_ROWS'):
    rep(f'''const {rows} := [
	["mode", "Game mode", ["ffa", "team"], ["Free for all", "Teams"]],''', f'''const {rows} := [
	["map", "Map", ["sky", "outpost", "catacombs", "random"], ["Sky Islands", "Outpost", "Catacombs", "Random"]],
	["mode", "Game mode", ["ffa", "team"], ["Free for all", "Teams"]],''')

# builders
old_gen = s[s.index("func ground_top(c: int) -> int:"):s.index("func solid_at(c: int, r: int) -> bool:")]
new_gen = '''func ground_top(c: int) -> int:
	if c >= 52 and c <= 68:
		return 42
	return clampi(40 - roundi(2.4 * sin(c * 0.085 + 0.4) + 1.2 * sin(c * 0.21)), 37, 42)

func fill(c0: int, r0: int, c1: int, r1: int, v: int) -> void:
	for r in range(r0, r1 + 1):
		for c in range(c0, c1 + 1):
			set_tile(c, r, v)

func carve_ellipse(cx: int, cy: int, rx: int, ry: int) -> void:
	for r in range(cy - ry, cy + ry + 1):
		for c in range(cx - rx, cx + rx + 1):
			var dx := float(c - cx) / rx
			var dy := float(r - cy) / ry
			if dx * dx + dy * dy <= 1.0:
				set_tile(c, r, EMPTY)

func pick_map() -> String:
	if cfg.map == "random" or not MAP_LIST.has(cfg.map):
		return MAP_LIST[randi() % MAP_LIST.size()]
	return cfg.map

func gen_map() -> void:
	tiles = PackedByteArray()
	tiles.resize(COLS * ROWS)
	tiles.fill(0)
	thp = PackedFloat32Array()
	thp.resize(COLS * ROWS)
	for c in COLS:
		for r in [0, ROWS - 1, ROWS - 2]:
			tiles[r * COLS + c] = ROCK
	for r in ROWS:
		tiles[r * COLS] = ROCK
		tiles[r * COLS + COLS - 1] = ROCK
	torches = []
	match map_id:
		"outpost":
			build_outpost()
		"catacombs":
			build_catacombs()
		_:
			build_sky()
	for bs in bases_v:
		for xx in bs[2]:
			set_tile(bs[0] + xx, bs[1], ROCK)
	compute_nav()

func build_sky() -> void:
	bases_v = BASES
	item_spots = ITEM_SPOTS
	water_row = 36
	zones = [
		{"type": "low", "rect": Rect2(44*T, 3*T, 32*T, 14*T), "g": 0.35, "f": 0.5},
		{"type": "heavy", "rect": Rect2(80*T, 28*T, 22*T, 12*T), "g": 1.8, "f": 2.0},
	]
	for c in range(1, COLS - 1):
		for r in range(ground_top(c), ROWS - 2):
			set_tile(c, r, DIRT)
	for isl in ISLANDS:
		for xx in isl[2]:
			set_tile(isl[0] + xx, isl[1], DIRT)
		for xx in range(1, isl[2] - 1):
			set_tile(isl[0] + xx, isl[1] + 1, DIRT)
	for b in BRIDGES:
		for xx in b[2]:
			set_tile(b[0] + xx, b[1], WOOD)
	for pc in [26, 92]:
		for xx in 2:
			for k in 3:
				set_tile(pc + xx, ground_top(pc + xx) - 1 - k, ROCK)
	for xx in 4:
		set_tile(58 + xx, 7, ROCK)
	for bs in BASES:
		for xx in bs[2]:
			set_tile(bs[0] + xx, bs[1] + 1, ROCK)
	for cr in CRATES:
		set_tile(cr[0], cr[1], CRATE)

# desert army base: bunkers at both ends, watchtowers, a two-floor building in the middle
func build_outpost() -> void:
	bases_v = [[2, 31, 9], [109, 31, 9]]
	item_spots = OUTPOST_SPOTS
	water_row = 37
	zones = [
		{"type": "low", "rect": Rect2(44*T, 2*T, 32*T, 20*T), "g": 0.35, "f": 0.5},
		{"type": "heavy", "rect": Rect2(47*T, 32*T, 26*T, 8*T), "g": 1.8, "f": 2.0},
	]
	for c in range(1, COLS - 1):
		var g := 40 - roundi(1.4 * sin(c * 0.07) + 0.7 * sin(c * 0.19 + 1.0))
		fill(c, g, c, ROWS - 3, DIRT)
		fill(c, ROWS - 4, c, ROWS - 3, ROCK)
	# bunkers (spawn on the roof, door on the inner side)
	fill(1, 31, 12, 32, ROCK)
	fill(12, 33, 12, 35, ROCK)
	fill(107, 31, 118, 32, ROCK)
	fill(107, 33, 107, 35, ROCK)
	for c in range(2, 12):
		fill(c, 33, c, 38, EMPTY)
	for c in range(108, 118):
		fill(c, 33, c, 38, EMPTY)
	# watchtowers
	for tx in [22, 92]:
		fill(tx, 22, tx + 5, 22, WOOD)
		fill(tx + 1, 17, tx + 4, 17, WOOD)
		for lx in [tx + 1, tx + 4]:
			for r in range(23, ROWS - 3):
				if solid_at(lx, r):
					break
				set_tile(lx, r, ROCK)
	# the compound
	fill(46, 24, 73, 24, ROCK)
	fill(57, 24, 62, 24, EMPTY)
	fill(46, 25, 46, 41, ROCK)
	fill(73, 25, 73, 41, ROCK)
	fill(46, 35, 46, 39, EMPTY)
	fill(73, 35, 73, 39, EMPTY)
	fill(46, 27, 46, 29, EMPTY)
	fill(73, 27, 73, 29, EMPTY)
	fill(47, 31, 72, 31, WOOD)
	fill(58, 31, 61, 31, EMPTY)
	for c in range(47, 73):
		fill(c, 25, c, 30, EMPTY)
		var g2 := 40 - roundi(1.4 * sin(c * 0.07) + 0.7 * sin(c * 0.19 + 1.0))
		fill(c, 32, c, g2 - 1, EMPTY)
	set_tile(50, 30, CRATE)
	set_tile(69, 30, CRATE)
	# antenna deck and side cover
	fill(54, 11, 65, 11, WOOD)
	fill(32, 28, 40, 28, ROCK)
	set_tile(32, 27, DIRT)
	set_tile(40, 27, DIRT)
	fill(79, 28, 87, 28, ROCK)
	set_tile(79, 27, DIRT)
	set_tile(87, 27, DIRT)
	fill(12, 16, 19, 16, ROCK)
	fill(100, 16, 107, 16, ROCK)
	fill(30, 10, 36, 10, WOOD)
	fill(83, 10, 89, 10, WOOD)
	# sandbag walls and crates on the ground
	for sx in [37, 82]:
		var g3 := surface_below(sx, 30)
		fill(sx, g3 - 2, sx + 1, g3 - 1, DIRT)
	for cx2 in [27, 43, 76, 98]:
		set_tile(cx2, surface_below(cx2, 30) - 1, CRATE)

# underground: tunnels, a great hall with bridges, side chambers and a crypt that floods
func build_catacombs() -> void:
	bases_v = [[3, 25, 9], [108, 25, 9]]
	item_spots = CATA_SPOTS
	water_row = 37
	zones = [
		{"type": "low", "rect": Rect2(40*T, 11*T, 40*T, 10*T), "g": 0.35, "f": 0.5},
		{"type": "heavy", "rect": Rect2(48*T, 33*T, 24*T, 8*T), "g": 1.8, "f": 2.0},
	]
	fill(1, 1, COLS - 2, ROWS - 3, DIRT)
	fill(1, ROWS - 4, COLS - 2, ROWS - 3, ROCK)
	for c in range(3, COLS - 3):
		var top := 5 + roundi(1.2 * sin(c * 0.13))
		var bot := 10 + roundi(1.0 * sin(c * 0.09 + 2.0))
		fill(c, top, c, bot, EMPTY)
	carve_ellipse(15, 20, 12, 6)
	carve_ellipse(105, 20, 12, 6)
	fill(4, 25, 27, 27, DIRT)
	fill(93, 25, 116, 27, DIRT)
	fill(25, 19, 40, 23, EMPTY)
	fill(80, 19, 95, 23, EMPTY)
	carve_ellipse(60, 20, 22, 10)
	for c in range(3, COLS - 3):
		fill(c, 33 + roundi(sin(c * 0.2)), c, 40, EMPTY)
	for sx in [9, 33, 86, 110]:
		fill(sx, 8, sx + 3, 35, EMPTY)
	fill(58, 29, 61, 34, EMPTY)
	fill(44, 22, 76, 22, WOOD)
	fill(57, 22, 63, 22, EMPTY)
	fill(50, 23, 50, 29, ROCK)
	fill(70, 23, 70, 29, ROCK)
	for tx in [20, 45, 74, 98]:
		fill(tx, 39, tx + 2, 40, ROCK)
	set_tile(30, 40, CRATE)
	set_tile(90, 40, CRATE)
	set_tile(55, 21, CRATE)
	set_tile(65, 21, CRATE)
	for bx in [24, 52, 68, 96]:
		fill(bx, 4, bx + 1, 4, ROCK)
	torches = [Vector2(8, 18), Vector2(22, 18), Vector2(98, 18), Vector2(112, 18), Vector2(42, 15), Vector2(78, 15),
		Vector2(54, 26), Vector2(66, 26), Vector2(18, 36), Vector2(52, 36), Vector2(84, 36), Vector2(104, 36),
		Vector2(28, 7), Vector2(60, 7), Vector2(92, 7)]

func surface_below(c: int, hint: int) -> int:
	for r in range(maxi(1, hint), ROWS - 1):
		if solid_at(c, r) and not solid_at(c, r - 1):
			return r
	return ROWS - 3

func roof_start(c: int) -> int:
	for r in range(1, ROWS - 4):
		if not solid_at(c, r) and not solid_at(c + 1, r) and not solid_at(c, r + 1) and not solid_at(c + 1, r + 1):
			return r
	return 1

# places bots can walk to, and floors that the "breaking ground" event can crumble
func compute_nav() -> void:
	roam_pts = []
	for c in range(3, COLS - 3, 4):
		for r in range(3, ROWS - 2):
			if solid_at(c, r) and not solid_at(c, r - 1) and not solid_at(c, r - 2) and not solid_at(c + 1, r - 1) and not solid_at(c + 1, r - 2):
				roam_pts.append(Vector2(c * T + 6, r * T - 44))
	surf_runs = []
	for r in range(2, ROWS - 3):
		var c0 := -1
		for c in range(1, COLS):
			var v := tiles[r * COLS + c] if c < COLS - 1 else 0
			var ok: bool = (v == DIRT or v == WOOD) and not solid_at(c, r - 1)
			if ok and c0 < 0:
				c0 = c
			elif not ok and c0 >= 0:
				if c - c0 >= 6:
					surf_runs.append([c0, r, c - c0])
				c0 = -1

'''
s = s.replace(old_gen, new_gen)

rep('''	var bs: Array = BASES[i]''', '''	var bs: Array = bases_v[i]''')
rep('''func roam_points() -> Array:
	var out := []
	for isl in ISLANDS:
		out.append(Vector2((isl[0] + isl[2] / 2.0) * T - 10, isl[1] * T - 44))
	for c in [20, 40, 60, 80, 100]:
		out.append(Vector2(c * T + 6, ground_top(c) * T - 44))
	return out''', '''func roam_points() -> Array:
	return roam_pts''')
rep('''	for i in BASES.size():
		var md := 1e9''', '''	for i in bases_v.size():
		var md := 1e9''')
rep('''	for l in ITEM_SPOTS:
		var s := Spawner.new()
		var row: int = l[1] if l[1] >= 0 else ground_top(l[0])''', '''	for l in item_spots:
		var s := Spawner.new()
		var row: int = surface_below(l[0], l[1])''')
rep('''(c.y > (WATER_ROW - 2) * T''', '''(c.y > (water_row - 2) * T''')
rep('''		var tgt := float(WATER_ROW) * T''', '''		var tgt := float(water_row) * T''')
rep('''		draw_dashed_line(Vector2(T, WATER_ROW * T), Vector2(WW - T, WATER_ROW * T), Color("#2f7fd8"), 3, 14)''', '''		draw_dashed_line(Vector2(T, water_row * T), Vector2(WW - T, water_row * T), Color("#2f7fd8"), 3, 14)''')
rep('''Vector2(lx0, WATER_ROW * T - 8)''', '''Vector2(lx0, water_row * T - 8)''')

# events adapt to any map
rep('''		var cols := {}
		while cols.size() < 7:
			cols[3 + randi() % (COLS - 8)] = true
		ev.cols = cols.keys()''', '''		var cols := {}
		for tries in 200:
			if cols.size() >= 7:
				break
			var cc := 3 + randi() % (COLS - 8)
			if roof_start(cc) < ROWS - 8:
				cols[cc] = true
		ev.cols = cols.keys()''')
rep('''			var isl: Array = ISLANDS[randi() % ISLANDS.size()]
			var s: int = isl[0] + randi() % maxi(1, isl[2] - 5)
			list = []
			for xx in range(s, s + 6):
				for yy in range(isl[1], isl[1] + 2):''', '''			if surf_runs.is_empty():
				break
			var isl: Array = surf_runs[randi() % surf_runs.size()]
			var s: int = isl[0] + randi() % maxi(1, isl[2] - 5)
			list = []
			for xx in range(s, s + 6):
				for yy in range(isl[1], isl[1] + 2):''')
rep('''			b.y = T
''', '''			b.y = roof_start(b.c) * T
''')
rep('''			var r := 1
			while r < ROWS - 3 and not solid_at(c, r + 2) and not solid_at(c + 1, r + 2):
				r += 1
			var gy: float = (r + 2) * T
			draw_rect(Rect2(c * T, T, 2 * T, gy - T), Color(C_RED, 0.12 if blink else 0.06))''', '''			var rs := roof_start(c)
			var r := rs
			while r < ROWS - 3 and not solid_at(c, r + 2) and not solid_at(c + 1, r + 2):
				r += 1
			var gy: float = (r + 2) * T
			draw_rect(Rect2(c * T, rs * T, 2 * T, gy - rs * T), Color(C_RED, 0.12 if blink else 0.06))''')

# match start picks the map
rep('''func reset_match() -> void:
	gen_map()''', '''func reset_match() -> void:
	map_id = pick_map()
	gen_map()''')

# ---------- textures per map ----------
rep('''"bg_mountains", "bg_hills", "bg_near",''', '''"bg_mountains", "bg_hills", "bg_near",
			"sand0", "sand1", "sand2", "sandcap", "concrete", "bg_out_far", "bg_out_mid", "bg_out_near",
			"cave0", "cave1", "cave2", "moss", "brick", "torch", "bg_cat_far", "bg_cat_mid",''')
rep('''	var shake_set := {}''', '''	var rock_tx: Texture2D = tex.rock
	var dirt_pre := "dirt"
	var cap_tx: Texture2D = tex.grass
	if map_id == "outpost":
		rock_tx = tex.concrete
		dirt_pre = "sand"
		cap_tx = tex.sandcap
	elif map_id == "catacombs":
		rock_tx = tex.brick
		dirt_pre = "cave"
		cap_tx = tex.moss
	var shake_set := {}''')
rep('''			if v == ROCK:
				draw_texture_rect(tex.rock, rect, false)''', '''			if v == ROCK:
				draw_texture_rect(rock_tx, rect, false)''')
rep('''				draw_texture_rect(tex["dirt%d" % ((c * 7 + r * 3) % 3)], rect, false)''', '''				draw_texture_rect(tex["%s%d" % [dirt_pre, (c * 7 + r * 3) % 3]], rect, false)''')
rep('''				draw_texture_rect(tex.grass, Rect2(c * T - 1, r * T - 5, T + 2, 16), false)''', '''				draw_texture_rect(cap_tx, Rect2(c * T - 1, r * T - 5, T + 2, 16), false)
	for tp in torches:
		if tp.x >= c0 - 1 and tp.x <= c1 + 1 and tp.y >= r0 - 2 and tp.y <= r1 + 1:
			var fl := 0.85 + 0.15 * sin(time_s * 13.0 + tp.x) + 0.05 * sin(time_s * 31.0 + tp.y)
			var tc := Vector2(tp.x * T + 16, tp.y * T + 10)
			draw_texture_rect(tex.glow, Rect2(tc - Vector2(70, 70) * fl, Vector2(140, 140) * fl), false, Color(1, 0.62, 0.25, 0.42))
			draw_texture_rect(tex.torch, Rect2(tc - Vector2(8, 20), Vector2(16, 32)), false)''')

old_bg = s[s.index("func draw_bg() -> void:"):s.index("func layer(name: String")]
new_bg = '''func draw_bg() -> void:
	if map_id == "catacombs":
		var t0 := Color("#120e14")
		var t1 := Color("#251c1e")
		draw_polygon(PackedVector2Array([Vector2(0, 0), Vector2(sw, 0), Vector2(sw, sh), Vector2(0, sh)]), PackedColorArray([t0, t0, t1, t1]))
		layer("bg_cat_far", 0.10, 1.02, 0.62, Color("#1a1418"))
		layer("bg_cat_mid", 0.28, 1.04, 0.6, Color("#261e1e"))
		return
	var top := Color("#3a7fca")
	var mid := Color("#7fbbe8")
	var hor := Color("#dcEEF7")
	var sun_col := Color(1, 0.98, 0.88)
	var cloud_col := Color(1, 1, 1, 0.92)
	if map_id == "outpost":
		top = Color("#35477e")
		mid = Color("#d98a5f")
		hor = Color("#f6cf8f")
		sun_col = Color(1, 0.82, 0.55)
		cloud_col = Color(1, 0.8, 0.7, 0.55)
	var my := sh * 0.45
	draw_polygon(PackedVector2Array([Vector2(0, 0), Vector2(sw, 0), Vector2(sw, my), Vector2(0, my)]), PackedColorArray([top, top, mid, mid]))
	draw_polygon(PackedVector2Array([Vector2(0, my), Vector2(sw, my), Vector2(sw, sh), Vector2(0, sh)]), PackedColorArray([mid, mid, hor, hor]))
	var sun := Vector2(sw * 0.78 - cam.x * zoom * 0.02, sh * (0.32 if map_id == "outpost" else 0.2))
	tex_c("glow", sun, Vector2(260, 260) * u * (1.5 if map_id == "outpost" else 1.0), Color(sun_col, 0.7))
	draw_circle(sun, 26 * u * (1.4 if map_id == "outpost" else 1.0), sun_col)
	for i in (3 if map_id == "outpost" else 5):
		var cw := (220.0 + i * 30) * u * 0.9
		var x := fposmod(i * 470.0 + time_s * (6 + i * 2) - cam.x * zoom * 0.08, sw + cw * 2) - cw
		var y := sh * (0.08 + 0.07 * (i % 3)) - cam.y * zoom * 0.03
		draw_texture_rect(tex["cloud%d" % (i % 3)], Rect2(x, y, cw, cw * 0.45), false, cloud_col)
	if map_id == "outpost":
		layer("bg_out_far", 0.10, 0.66, 0.31, Color("#b07054"))
		layer("bg_out_mid", 0.25, 0.80, 0.425, Color("#be925e"))
		layer("bg_out_near", 0.42, 0.93, 0.475, Color("#a0744a"))
		return
	layer("bg_mountains", 0.10, 0.66, 0.31, Color("#7e9cc0"))
	layer("bg_hills", 0.25, 0.80, 0.425, Color("#42724a"))
	layer("bg_near", 0.42, 0.93, 0.475, Color("#2e5434"))

'''
s = s.replace(old_bg, new_bg)

# darker mood underground
rep('''	draw_water()
	draw_set_transform_matrix(Transform2D.IDENTITY)
	ga = 1.0
	draw_hud()''', '''	draw_water()
	draw_set_transform_matrix(Transform2D.IDENTITY)
	ga = 1.0
	if map_id == "catacombs":
		vignette(Color(0, 0, 0, 0.55), 0.28)
	draw_hud()''')

# menu shows the chosen map; LAN carries the map
rep('''		"%d minutes  /  event every %d sec" % [cfg.minutes, cfg.event_every],''', '''		"Map: %s  /  %d min  /  event every %d sec" % [MAP_NAMES.get(cfg.map, "Sky Islands"), cfg.minutes, cfg.event_every],''')
rep('''	return {"idx": idx, "tiles": tiles, "pl": pl, "mode": cfg.mode, "zones": cfg.zones, "mt": match_time}''', '''	return {"idx": idx, "tiles": tiles, "pl": pl, "mode": cfg.mode, "zones": cfg.zones, "mt": match_time, "map": map_id}''')
rep('''	cfg.zones = info.zones
	gen_map()''', '''	cfg.zones = info.zones
	map_id = str(info.get("map", "sky"))
	gen_map()''')
rep('''	var info := {"pl": lobby_names(), "mode": cfg.mode,''', '''	var info := {"pl": lobby_names(), "mode": cfg.mode, "map": cfg.map,''')
rep('''	txt(("Teams: Blue vs Red" if mode == "team" else "Free for all") + "  /  %d min" % mins, Vector2(rx, y + 96 * u), 13 * u, C_INK)''', '''	var mp: String = MAP_NAMES.get(cfg.map if host else str(lobby_info.get("map", "sky")), "Sky Islands")
	txt(mp + "  /  " + ("Teams" if mode == "team" else "Free for all") + "  /  %d min" % mins, Vector2(rx, y + 96 * u), 13 * u, C_INK)''')
open(P, "w").write(s)
print("ok")
s = open(P).read()
s = s.replace('''	for a in args:
		if a == "--lantest-host":''', '''	for a in args:
		if a.begins_with("--map="):
			cfg.map = a.substr(6)
		if a == "--lantest-host":''', 1)
open(P, "w").write(s)
print("map flag ok")
