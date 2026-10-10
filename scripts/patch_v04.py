import re
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

rep('Playtest build 0.3', 'Playtest build 0.4')
rep('const VERSION := "0.3"', 'const VERSION := "0.4"')
# ---------- feel settings ----------
rep('"gravity": 1050.0, "max_fall": 620.0, "move_speed": 165.0,', '"gravity": 900.0, "max_fall": 540.0, "move_speed": 125.0,')
rep('"jump_speed": 290.0, "thrust": 1850.0, "max_rise": 330.0,', '"jump_speed": 260.0, "thrust": 1550.0, "max_rise": 270.0,')
rep('"fuel_max": 100.0, "fuel_drain": 22.0,', '"fuel_max": 100.0, "fuel_drain": 14.0,')
rep('"aim_turn": 10.0, "view_h": 390.0,', '"aim_turn": 7.0, "mouse_turn": 16.0, "protect": 2.5, "view_h": 390.0,')
rep('	var acc := 1500.0 if p.on_ground else 700.0', '	var acc := 1100.0 if p.on_ground else 520.0')
# AK-47 power
rep('"ak47":    {"name": "AK-47",   "dmg": 13.0, "rate": 0.12, "mag": 30, "spare": 90,  "reload": 1.9, "spread": 0.055, "speed": 1300.0, "pellets": 1, "life": 0.85, "chip": 0.35, "recoil": 3.0,',
    '"ak47":    {"name": "AK-47",   "dmg": 17.0, "rate": 0.11, "mag": 30, "spare": 90,  "reload": 1.9, "spread": 0.045, "speed": 1400.0, "pellets": 1, "life": 0.85, "chip": 0.45, "recoil": 5.0,')
assert '"dmg": 17.0, "rate": 0.11' in s
# ---------- bigger map ----------
rep('const COLS := 80\nconst ROWS := 40', 'const COLS := 120\nconst ROWS := 46\nconst WATER_ROW := 36')
rep('''const ISLANDS := [[6,26,9],[20,24,8],[33,20,14],[52,24,8],[65,26,9],[12,18,7],[60,18,7],[26,14,6],[48,14,6],[37,9,6],[4,11,6],[70,11,6]]
const BRIDGES := [[35,29,12],[16,13,5],[59,13,5]]
const CRATES := [[7,25],[8,25],[72,25],[24,23],[55,23],[39,19],[40,19],[5,10],[74,10]]''',
'''const ISLANDS := [[16,34,8],[30,31,9],[46,28,8],[56,24,10],[66,28,8],[81,31,9],[96,34,8],[22,24,7],[38,20,8],[52,15,7],[61,15,7],[74,20,8],[90,24,7],[10,18,6],[104,18,6],[30,11,6],[84,11,6],[56,7,8]]
const BASES := [[2,30,9],[109,30,9]]
const BRIDGES := [[52,38,17],[11,25,6],[103,25,6]]
const CRATES := [[23,33],[38,30],[81,30],[96,33],[22,23],[96,23],[38,19],[81,19],[10,17],[109,17]]
# pickup spots: [col, row (-1 = ground), type, guns]
const ITEM_SPOTS := [
	[60, 7, "gun", ["sniper", "rpg"]], [55, 15, "health", []], [64, 15, "grenade", []],
	[42, 20, "gun", ["ak47", "shotgun"]], [78, 20, "gun", ["ak47", "shotgun"]],
	[25, 24, "health", []], [93, 24, "health", []],
	[50, 28, "gun", ["rpg", "ak47"]], [70, 28, "gun", ["rpg", "ak47"]], [61, 24, "gun", ["uzi", "magnum"]],
	[34, 31, "gun", ["shotgun", "sniper"]], [85, 31, "gun", ["shotgun", "sniper"]],
	[20, 34, "gun", ["magnum", "uzi"]], [100, 34, "gun", ["magnum", "uzi"]],
	[13, 18, "grenade", []], [107, 18, "grenade", []],
	[33, 11, "gun", ["ak47", "sniper"]], [87, 11, "gun", ["ak47", "sniper"]],
	[44, -1, "health", []], [76, -1, "health", []], [60, 38, "grenade", []],
]''')
rep('''func ground_top(c: int) -> int:
	if c >= 33 and c <= 47:
		return 35
	return 33 - roundi(2.2 * sin(c * 0.13 + 0.5) + 1.2 * sin(c * 0.31))''', '''func ground_top(c: int) -> int:
	if c >= 52 and c <= 68:
		return 42
	return clampi(40 - roundi(2.4 * sin(c * 0.085 + 0.4) + 1.2 * sin(c * 0.21)), 37, 42)''')
rep('''	for pc in [18, 61]:
		for xx in 2:
			for k in 3:
				set_tile(pc + xx, ground_top(pc + xx) - 1 - k, ROCK)
	for xx in 4:
		set_tile(38 + xx, 9, ROCK)''', '''	for pc in [26, 92]:
		for xx in 2:
			for k in 3:
				set_tile(pc + xx, ground_top(pc + xx) - 1 - k, ROCK)
	for xx in 4:
		set_tile(58 + xx, 7, ROCK)
	for bs in BASES:
		for xx in bs[2]:
			set_tile(bs[0] + xx, bs[1], ROCK)
			set_tile(bs[0] + xx, bs[1] + 1, ROCK)''')
rep('''var zones := [
	{"type": "low", "rect": Rect2(30*T, 2*T, 21*T, 12*T), "g": 0.35, "f": 0.5},
	{"type": "heavy", "rect": Rect2(1*T, 14*T, 14*T, 16*T), "g": 1.8, "f": 2.0},
]''', '''var zones := [
	{"type": "low", "rect": Rect2(44*T, 3*T, 32*T, 14*T), "g": 0.35, "f": 0.5},
	{"type": "heavy", "rect": Rect2(80*T, 28*T, 22*T, 12*T), "g": 1.8, "f": 2.0},
]''')
rep('''		var bottom := 35.0 * T
		var tgt := 29.0 * T''', '''		var bottom := 43.0 * T
		var tgt := float(WATER_ROW) * T''')
rep('''		draw_dashed_line(Vector2(T, 29 * T), Vector2(WW - T, 29 * T), Color("#2f7fd8"), 3, 14)
		txt("WATER WILL RISE TO HERE", Vector2(2 * T, 29 * T - 8), 14, Color("#bfe0ff"), 0, 4)''', '''		draw_dashed_line(Vector2(T, WATER_ROW * T), Vector2(WW - T, WATER_ROW * T), Color("#2f7fd8"), 3, 14)
		var lx0: float = clampf(cam.x + 40, T, WW - 300)
		txt("WATER WILL RISE TO HERE", Vector2(lx0, WATER_ROW * T - 8), 14, Color("#bfe0ff"), 0, 4)''')
rep('''			for xx in range(36, 46):
				if tiles[29 * COLS + xx] == WOOD:
					list.append(Vector2i(xx, 29))''', '''			for xx in range(54, 67):
				if tiles[38 * COLS + xx] == WOOD:
					list.append(Vector2i(xx, 38))''')
rep('''		fly = fly or (c.y > 27 * T and randf() < 0.6)''', '''		fly = fly or (c.y > (WATER_ROW - 2) * T and randf() < 0.6)''')
rep('''		cam.y = clampf(16 * T - vh / 2, 0, WH - vh)''', '''		cam.y = clampf(24 * T - vh / 2, 0, WH - vh)''')
# spawn points -> two bases + roam points
cut('func spawn_points() -> Array:', 'func spawn(p: Player) -> void:', '''func base_spots(i: int) -> Array:
	var bs: Array = BASES[i]
	var out := []
	for k in [2, 4, 6]:
		out.append(Vector2((bs[0] + k) * T + 6, bs[1] * T - 44))
	return out

func roam_points() -> Array:
	var out := []
	for isl in ISLANDS:
		out.append(Vector2((isl[0] + isl[2] / 2.0) * T - 10, isl[1] * T - 44))
	for c in [20, 40, 60, 80, 100]:
		out.append(Vector2(c * T + 6, ground_top(c) * T - 44))
	return out

''')
cut('func spawn(p: Player) -> void:', '	p.posture = "stand"', '''func spawn(p: Player) -> void:
	# pick the base farther from enemies (sometimes the other one, to mix it up)
	var far := []
	for i in BASES.size():
		var md := 1e9
		var bc: Vector2 = base_spots(i)[1]
		for o in players:
			if o != p and o.alive:
				md = minf(md, Vector2(o.x - bc.x, o.y - bc.y).length())
		far.append(md)
	var pick := 0 if far[0] >= far[1] else 1
	if randf() < 0.25:
		pick = 1 - pick
	var spots := base_spots(pick)
	spots.shuffle()
	var best = spots[0]
	for sp in spots:
		if not rect_hits(sp.x, sp.y, 20, 42):
			best = sp
			break
	p.protect_t = S.protect
''')
rep('''		var pts := spawn_points()
		b.roam = pts[randi() % pts.size()] + Vector2(10, 20)''', '''		var pts := roam_points()
		b.roam = pts[randi() % pts.size()] + Vector2(10, 20)''')
cut('func make_spawners() -> void:', 'func fill_spawner(s: Spawner) -> void:', '''func make_spawners() -> void:
	spawners.clear()
	for l in ITEM_SPOTS:
		var s := Spawner.new()
		var row: int = l[1] if l[1] >= 0 else ground_top(l[0])
		s.x = l[0] * T + T / 2.0 - 12
		s.y = row * T - 17
		s.type = l[2]
		s.pool = l[3]
		spawners.append(s)
		fill_spawner(s)

''')
open(p, 'w').write(s)
print("map ok")
