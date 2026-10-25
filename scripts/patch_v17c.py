"""v1.7 part C: time bomb -> proximity mine; stronger shotgun and grenades; big 12 s smoke."""
import sys
P = "/home/claude/skysquad/main.gd"
s = open(P).read()
ERR = []
def rep(a, b, c=1):
    global s
    if s.count(a) != c:
        ERR.append("expected %d got %d: %r" % (c, s.count(a), a[:120])); return
    s = s.replace(a, b)

# ---------- stronger shotgun and grenades ----------
rep('''"shotgun": {"name": "SHOTGUN", "dmg": 11.0, "rate": 0.95, "mag": 6,  "spare": 18,  "reload": 2.2, "spread": 0.32,  "speed": 1050.0, "pellets": 8, "life": 0.32,''',
    '''"shotgun": {"name": "SHOTGUN", "dmg": 14.0, "rate": 0.9,  "mag": 6,  "spare": 18,  "reload": 2.0, "spread": 0.24,  "speed": 1150.0, "pellets": 8, "life": 0.36,''')
rep('''"grenade_fuse": 2.5, "grenade_radius": 80.0, "grenade_dmg": 80.0,''', '''"grenade_fuse": 2.2, "grenade_radius": 100.0, "grenade_dmg": 105.0,''')
# blasts hurt fully near the middle, then fade out
rep('''		var big := r * 1.4
		if d < big:
			var f := 1.0 - d / big''', '''		var big := r * 1.4
		if d < big:
			var f := clampf((1.0 - d / big) * 1.35, 0.0, 1.0)''')

# ---------- mine: sticks where it lands, arms, explodes when an enemy comes very close ----------
rep('''		if g.kind == "bomb":
			g.beep_t -= dt
			if g.beep_t <= 0:
				g.beep_t = 0.15 + g.fuse * 0.18
				play("beep", Vector2(g.x, g.y), -4.0, 0.0)
			if g.stuck:
				if g.beep_t > 0.9:
					g.beep_t = 0.3
				g.fuse -= dt
				if g.fuse <= 0:
					explode(g.x, g.y, 120.0, 115.0, g.owner, "bomb")
					grenades_list.remove_at(i)
				continue''', '''		if g.kind == "bomb":
			if g.stuck:
				# fuse counts up here: time since it was planted
				g.fuse += dt
				g.beep_t -= dt
				if g.fuse > MINE_ARM:
					var near := mine_target(g)
					if g.beep_t <= 0:
						g.beep_t = 0.25 if near else 1.6
						play("beep", Vector2(g.x, g.y), -6.0 if near else -16.0, 0.0)
					if near or g.fuse > MINE_LIFE:
						explode(g.x, g.y, 120.0, 125.0, g.owner, "bomb")
						grenades_list.remove_at(i)
				continue''')
rep('''				if not g.stuck:
					play("arm", Vector2(g.x, g.y), -2.0, 0.0)
				g.stuck = true
		else:
			g.x = nx''', '''				if not g.stuck:
					plant_mine(g)
				g.stuck = true
		else:
			g.x = nx''')
rep('''				if not g.stuck:
					play("arm", Vector2(g.x, g.y), -2.0, 0.0)
				g.stuck = true
		else:
			g.y = ny''', '''				if not g.stuck:
					plant_mine(g)
				g.stuck = true
		else:
			g.y = ny''')
rep('''		gb.fuse = 4.5
		gb.kind = "bomb"''', '''		gb.fuse = 30.0
		gb.kind = "bomb"''')
rep('''		g.fuse -= dt
		if g.fuse <= 0:
			if g.kind == "smoke":''', '''		if g.kind != "bomb":
			g.fuse -= dt
		if g.fuse <= 0 or (g.kind == "bomb" and (g.y > WH or g.y < 0)):
			if g.kind == "smoke":''')
# drawing the mine: no countdown, a slow blink, faster and a red ring once armed
rep('''			draw_texture_rect(tex.timebomb, Rect2(g.x - 8, g.y - 6, 16, 12), false)
			if sin(time_s * (6.0 + (4.5 - g.fuse) * 3.0)) > 0:
				draw_circle(Vector2(g.x + 4, g.y - 5), 2.0, C_RED)
			txt(str(ceili(g.fuse)), Vector2(g.x, g.y - 10), 11, C_RED, 1, 3)
			continue''', '''			draw_texture_rect(tex.timebomb, Rect2(g.x - 8, g.y - 6, 16, 12), false)
			var armed: bool = g.stuck and g.fuse > MINE_ARM
			if sin(time_s * (9.0 if armed else 3.0)) > 0.2:
				draw_circle(Vector2(g.x + 4, g.y - 5), 2.2, C_RED if armed else C_ARC)
			if armed:
				draw_arc(Vector2(g.x, g.y), MINE_R, 0, TAU, 28, Color(1, 0.25, 0.25, 0.18 + 0.08 * sin(time_s * 4.0)), 1.5, true)
			continue''')
rep('''"bomb": "TIME BOMB"''', '''"bomb": "MINE"''')

# ---------- smoke: 12 seconds, wide, thick, blocks sight ----------
rep('''				clouds.append({"x": g.x, "y": g.y, "t": 7.0, "owner": g.owner})''', '''				clouds.append({"x": g.x, "y": g.y, "t": SMOKE_T, "owner": g.owner})''')
rep('''func cloud_fx(cl: Dictionary, dt: float) -> void:
	var k: float = clampf(cl.t / 1.5, 0.0, 1.0)
	if randf() < dt * 16.0 * k:
		add_part(cl.x + randf_range(-80, 80), cl.y + randf_range(-55, 40), randf_range(-12, 12), randf_range(-14, 4), 2.4, Color(0.62, 0.74, 0.55, 0.55), 40, -0.004, "smoke", 96)''',
'''func cloud_fx(cl: Dictionary, dt: float) -> void:
	# a few drifting wisps on top of the big puffs drawn in draw_clouds
	var k: float = clampf(cl.t / 1.5, 0.0, 1.0)
	if randf() < dt * 6.0 * k:
		var a := randf() * TAU
		add_part(cl.x + cos(a) * SMOKE_R * 0.9, cl.y + sin(a) * SMOKE_R * 0.6, cos(a) * 14.0, sin(a) * 8.0 - 6.0, 2.6, Color(0.7, 0.78, 0.66, 0.35), 50, -0.004, "smoke", 110)''')
rep('''			if center(p).distance_to(Vector2(cl.x, cl.y)) < 105:
				hurt(p, 7.0 * dt, cl.owner, "gas", "smoke")''', '''			if in_cloud(cl, center(p)):
				hurt(p, 4.0 * dt, cl.owner, "gas", "smoke")''')
# bots cannot see through smoke
rep('''		visible = los(eye, center(tg))''', '''		visible = los(eye, center(tg)) and not smoke_blocks(eye, center(tg))''')
# draw the clouds right after the players so soldiers inside are hidden
rep('''	_pm("players")
	draw_set_transform_matrix(wt)
	draw_landing_marker()''', '''	_pm("players")
	draw_set_transform_matrix(wt)
	draw_clouds()
	draw_landing_marker()''')

s += '''
# ================= MINE + SMOKE (v1.7) =================
const MINE_ARM := 0.8
const MINE_LIFE := 90.0
const MINE_R := 46.0
const SMOKE_T := 12.0
const SMOKE_R := 175.0

func plant_mine(g: Grenade) -> void:
	g.fuse = 0.0
	g.vx = 0.0
	g.vy = 0.0
	play("arm", Vector2(g.x, g.y), -2.0, 0.0)
	# each soldier keeps at most 2 mines; the oldest one goes away
	var mine := []
	for o in grenades_list:
		if o.kind == "bomb" and o.stuck and o.owner == g.owner and o != g:
			mine.append(o)
	while mine.size() >= 2:
		grenades_list.erase(mine.pop_front())

func mine_target(g: Grenade) -> bool:
	for p in players:
		if not p.alive or p == g.owner:
			continue
		if g.owner != null and not enemy(p, g.owner):
			continue
		if center(p).distance_to(Vector2(g.x, g.y)) < MINE_R:
			return true
	return false

func cloud_k(cl: Dictionary) -> float:
	var age: float = SMOKE_T - float(cl.t)
	return clampf(age / 0.8, 0.0, 1.0) * clampf(float(cl.t) / 1.8, 0.0, 1.0)

func in_cloud(cl: Dictionary, pt: Vector2) -> bool:
	var r: float = SMOKE_R * (0.45 + 0.55 * clampf((SMOKE_T - float(cl.t)) / 0.8, 0.0, 1.0))
	var d := pt - Vector2(cl.x, cl.y)
	return Vector2(d.x, d.y * 1.4).length() < r * 0.85

func smoke_blocks(a: Vector2, b: Vector2) -> bool:
	for cl in clouds:
		if cloud_k(cl) < 0.5:
			continue
		var c := Vector2(cl.x, cl.y)
		var ab := b - a
		var k := clampf((c - a).dot(ab) / maxf(1.0, ab.length_squared()), 0.0, 1.0)
		if in_cloud(cl, a + ab * k):
			return true
	return false

# big soft puffs that grow out, roll slowly and fade at the end
func draw_clouds() -> void:
	for ci in clouds.size():
		var cl: Dictionary = clouds[ci]
		var k := cloud_k(cl)
		if k <= 0.0:
			continue
		var grow: float = 0.45 + 0.55 * clampf((SMOKE_T - float(cl.t)) / 0.8, 0.0, 1.0)
		var seed := float(int(cl.x * 7.0 + cl.y * 3.0) % 97)
		for j in 16:
			var a := j * 2.39996 + seed
			var rr: float = SMOKE_R * grow * (0.15 + 0.75 * fmod(j * 0.618, 1.0))
			var px: float = cl.x + cos(a + time_s * 0.05) * rr + sin(time_s * 0.4 + j) * 8.0
			var py: float = cl.y + sin(a + time_s * 0.05) * rr * 0.62 + cos(time_s * 0.35 + j * 1.7) * 6.0
			var sz: float = (110.0 + 40.0 * fmod(j * 0.37, 1.0)) * grow
			var shade := 0.62 + 0.14 * fmod(j * 0.53, 1.0)
			draw_set_transform_matrix(cur_wt * Transform2D(time_s * 0.08 * (1.0 if j % 2 == 0 else -1.0) + j, Vector2.ONE, 0.0, Vector2(px, py)))
			draw_texture_rect(tex.smoke, Rect2(-sz / 2, -sz / 2, sz, sz), false, Color(shade, shade + 0.08, shade - 0.02, 0.78 * k))
	draw_set_transform_matrix(cur_wt)
'''
# remember the world transform for helpers that draw in the world
rep('''	var wt := Transform2D(0.0, Vector2(zoom, zoom), 0.0, Vector2(-cam.x * zoom + shk, -cam.y * zoom + shk))
	draw_set_transform_matrix(wt)''', '''	var wt := Transform2D(0.0, Vector2(zoom, zoom), 0.0, Vector2(-cam.x * zoom + shk, -cam.y * zoom + shk))
	cur_wt = wt
	draw_set_transform_matrix(wt)''')
s += "var cur_wt := Transform2D.IDENTITY\n"
if ERR:
    print("\n".join(ERR)); sys.exit(1)
open(P, "w").write(s)
print("ok")
