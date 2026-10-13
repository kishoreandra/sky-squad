"""v1.4: fair play + clear respawn.
- respawn: many safe spawn points (far from enemies, out of their sight, not the same place twice), the camera
  glides to where you will land, a beam drops you in, the shield shows how long it lasts
- every weapon behaves the same for everyone: fixed spread pattern (no lucky shots), fixed shotgun fan,
  fixed flame, same starting guns for everyone
- lag compensation: shots from players on slower internet are checked against what they saw"""
import sys
P = "/home/claude/skysquad/main.gd"
s = open(P).read()
def rep(a, b, c=1):
    global s
    if s.count(a) != c: sys.exit("expected %d got %d: %r" % (c, s.count(a), a[:120]))
    s = s.replace(a, b)

rep('# Sky Squad - Arc Light Studio. Playtest build 1.3', '# Sky Squad - Arc Light Studio. Playtest build 1.4')
rep('const VERSION := "1.3"', 'const VERSION := "1.4"')
rep('\tvar actor := false\n\tvar look := {}\n', '\tvar actor := false\n\tvar look := {}\n\tvar spawn_set := false\n\tvar spawn_pt := Vector2.ZERO\n\tvar last_spawn := Vector2.ZERO\n\tvar born_t := -9.0\n\tvar shot_n := 0\n\tvar last_fire_t := -9.0\n\tvar hist: Array = []\n\tvar lat := 0.0\n')
rep('''	var max_life := 1.0
	var gun := ""

class Grenade:''', '''	var max_life := 1.0
	var gun := ""
	var ff := 0.0

class Grenade:''')

# ---------- respawn: choose the landing spot early, then drop in ----------
rep('''func spawn(p: Player) -> void:
	# pick the base farther from enemies (sometimes the other one, to mix it up)
	var far := []''', '''# a safe place to land: far from enemies, out of their sight, not where you landed last time,
# picked at random among the best few so nobody can camp it
func pick_spawn(p: Player) -> Vector2:
	var cands := []
	for i in bases_v.size():
		cands.append_array(base_spots(i))
	cands.append_array(roam_pts)
	var own_base := Vector2.ZERO
	var other_base := Vector2.ZERO
	if cfg.mode == "team" and bases_v.size() >= 2:
		own_base = base_spots(p.side % 2)[1]
		other_base = base_spots(1 - p.side % 2)[1]
	var scored := []
	for sp in cands:
		if rect_hits(sp.x, sp.y, 20, 42) or sp.y + 42 > water_y - 24:
			continue
		if cfg.mode == "team" and own_base != other_base and sp.distance_to(own_base) > sp.distance_to(other_base):
			continue
		var c: Vector2 = sp + Vector2(10, 21)
		var md := 1400.0
		var seen := false
		for o in players:
			if o != p and o.alive and enemy(o, p):
				var d := center(o).distance_to(c)
				md = minf(md, d)
				if d < 760 and los(center(o), c):
					seen = true
		var score := md - (520.0 if seen else 0.0) + randf() * 260.0
		if p.last_spawn != Vector2.ZERO and c.distance_to(p.last_spawn) < 240:
			score -= 400.0
		scored.append([score, sp])
	if scored.is_empty():
		return base_spots(0)[1]
	scored.sort_custom(func(a, b): return a[0] > b[0])
	var pick: Vector2 = scored[randi() % mini(3, scored.size())][1]
	p.last_spawn = pick + Vector2(10, 21)
	return pick

func spawn(p: Player) -> void:
	if p.spawn_set and not rect_hits(p.spawn_pt.x, p.spawn_pt.y, 20, 42):
		spawn_at(p, p.spawn_pt)
		return
	spawn_at(p, pick_spawn(p))

func old_spawn_unused(p: Player) -> void:
	# pick the base farther from enemies (sometimes the other one, to mix it up)
	var far := []''')
rep('''	p.protect_t = S.protect
	if t > 0.5:
		me_fx(p, "snd", ["spawn", -8.0])''', '''	spawn_at(p, best)

func spawn_at(p: Player, best: Vector2) -> void:
	p.spawn_set = false
	p.born_t = time_s
	p.protect_t = S.protect
	if t > 0.5:
		play("spawn", Vector2(best.x + 10, best.y + 21), -6.0 if is_me(p) else -12.0, 0.05)''')
rep('''	if not p.alive:
		p.respawn_t -= dt
		if p.respawn_t <= 0:
			spawn(p)''', '''	if not p.alive:
		p.respawn_t -= dt
		if p.respawn_t <= 0.9 and not p.spawn_set:
			# choose the landing spot now so the camera can glide there before you appear
			p.spawn_pt = pick_spawn(p)
			p.spawn_set = true
			p.x = p.spawn_pt.x
			p.y = p.spawn_pt.y
			p.vx = 0.0
			p.vy = 0.0
		if p.respawn_t <= 0:
			spawn(p)''')
# camera glides to the landing spot in the last moment of the respawn wait
rep('''		if me.alive:
			if cam == Vector2.ZERO or cam.distance_to(want) > 500 or shot_at >= 0:
				cam = want
			else:
				cam += (want - cam) * ease_k(6.0, last_delta)''', '''		if me.alive:
			if cam == Vector2.ZERO or cam.distance_to(want) > 500 or shot_at >= 0:
				cam = want
			else:
				cam += (want - cam) * ease_k(6.0, last_delta)
		elif me.respawn_t < 0.9:
			cam += (want - cam) * ease_k(5.0, last_delta)''')
# joining phones: a dead player's position is where they will land
rep('''		p.recoil = maxf(0.0, p.recoil - dt * 40)
		if not p.alive:
			continue
		if i == my_idx and predicting():''', '''		p.recoil = maxf(0.0, p.recoil - dt * 40)
		if not p.alive:
			p.x = p.nx
			p.y = p.ny
			continue
		if i == my_idx and predicting():''')
rep('''		if (p.alive and not was_alive) or snaps_got == 1 or (not mine''', '''		if p.alive and not was_alive:
			p.born_t = time_s
		if (p.alive and not was_alive) or snaps_got == 1 or (not mine''')
# the respawn card fades away so you can see where you land
rep('''func draw_respawn_card(me: Player) -> void:
	var age := S.respawn - me.respawn_t
	var a := ease_out(age / 0.3)''', '''func draw_respawn_card(me: Player) -> void:
	var age := S.respawn - me.respawn_t
	var ready_k := clampf(me.respawn_t / 0.9, 0.0, 1.0)
	if ready_k < 1.0:
		var gk := 1.0 - ready_k
		txh("GET READY", Vector2(sw / 2, sh * 0.2), 30 * u * (0.9 + 0.1 * gk), Color(C_ARC, gk), 1, 5 * u)
		txt("You land here", Vector2(sw / 2, sh * 0.2 + 24 * u), 12 * u, Color(C_INK, gk), 1, 3 * u)
	var a := ease_out(age / 0.3) * ready_k''')
# landing marker (only you see it), then the beam everyone sees
rep('''	draw_set_transform_matrix(wt)
	for p in players:
		draw_player(p, wt)
	draw_set_transform_matrix(wt)''', '''	draw_set_transform_matrix(wt)
	for p in players:
		draw_player(p, wt)
	draw_set_transform_matrix(wt)
	draw_landing_marker()
	draw_set_transform_matrix(wt)''')
rep('''	var tint := Color(1.6, 1.6, 1.6) if p.flash > 0 else Color.WHITE''', '''	var tint := Color(1.6, 1.6, 1.6) if p.flash > 0 else Color.WHITE
	var bage := time_s - p.born_t
	if bage < 0.6 and bage >= 0.0 and not p.actor:
		draw_drop_beam(c, bage, wt)
		tint.a = clampf(bage / 0.3, 0.15, 1.0)''')
# shield shows how long it has left
rep('''		draw_arc(Vector2(0, -4), 30, 0, TAU, 40, Color(0.5, 0.9, 1.0, 0.5), 2.0, true)''', '''		draw_arc(Vector2(0, -4), 30, 0, TAU, 40, Color(0.5, 0.9, 1.0, 0.25), 2.0, true)
		draw_arc(Vector2(0, -4), 30, -PI / 2, -PI / 2 + TAU * clampf(p.protect_t / S.protect, 0.0, 1.0), 40, Color(0.6, 0.95, 1.0, 0.9), 3.0, true)''')

# ---------- same weapon, same result for everyone ----------
rep('''	var r := randf()
	var primary := "uzi" if r < 0.5 else ("ak47" if r < 0.8 else "shotgun")
	if p.style == "sniper" and p.bot:''', '''	var primary := "uzi"
	if p.style == "sniper" and p.bot:''')
rep('''	p.protect_t = 0.0
	var spread_mul := 1.0 if p.on_ground else 1.35''', '''	p.protect_t = 0.0
	# spread follows the same fixed pattern for everyone: the first shot goes where you aim
	if t - p.last_fire_t > 0.35:
		p.shot_n = 0
	var off: float = SPREAD_PAT[p.shot_n % SPREAD_PAT.size()]
	p.shot_n += 1
	p.last_fire_t = t
	var rw := rewind_others(p)
	var spread_mul := 1.0 if p.on_ground else 1.35''')
rep('''		hitscan(p, mz, p.aim + randf_range(-0.5, 0.5) * d.spread * spread_mul, d.dmg, d.chip)''', '''		hitscan(p, mz, p.aim + off * d.spread * spread_mul, d.dmg, d.chip)''')
rep('''		laser_beam(p, mz, p.aim + randf_range(-0.5, 0.5) * d.spread * spread_mul, d.dmg, d.chip)''', '''		laser_beam(p, mz, p.aim + off * d.spread * spread_mul, d.dmg, d.chip)''')
rep('''			var fa: float = p.aim + randf_range(-0.5, 0.5) * d.spread
			var fb := Bullet.new()
			var fsp: float = d.speed * randf_range(0.8, 1.15)''', '''			var fa: float = p.aim + (off * 0.6 + (i - 0.5) * 0.4) * d.spread
			var fb := Bullet.new()
			var fsp: float = d.speed * (1.0 if i == 0 else 0.9)''')
rep('''			fb.life = d.life * randf_range(0.8, 1.1)''', '''			fb.life = d.life
			fb.ff = p.lat if p.remote else 0.0''')
rep('''			var a: float = p.aim + randf_range(-0.5, 0.5) * d.spread * spread_mul
			var b := Bullet.new()
			var sp: float = d.speed * (randf_range(0.85, 1.15) if d.pellets > 1 else 1.0)''', '''			var fan: float = (float(i) / (d.pellets - 1) - 0.5 + off * 0.15) if d.pellets > 1 else off
			var a: float = p.aim + fan * d.spread * spread_mul
			var b := Bullet.new()
			var sp: float = d.speed * (1.0 - 0.06 * (i % 3) if d.pellets > 1 else 1.0)''')
rep('''			b.net = special == "net"
			bullets.append(b)''', '''			b.net = special == "net"
			b.ff = p.lat if p.remote else 0.0
			bullets.append(b)''')
rep('''	if d.push > 0 and p.posture == "stand":
		p.vx -= cos(p.aim) * d.push''', '''	restore_others(rw)
	if d.push > 0 and p.posture == "stand":
		p.vx -= cos(p.aim) * d.push''')
# knife: judged against what the attacker saw too
rep('''		var dir := 1.0 if cos(p.aim) >= 0 else -1.0
		for o in players:
			if o == p or not o.alive or not enemy(p, o):
				continue''', '''		var dir := 1.0 if cos(p.aim) >= 0 else -1.0
		var rwk := rewind_others(p)
		for o in players:
			if o == p or not o.alive or not enemy(p, o):
				continue''')
rep('''		damage_tile(floori((c.x + dir * 30) / T), floori(c.y / T), 2.0)''', '''		restore_others(rwk)
		damage_tile(floori((c.x + dir * 30) / T), floori(c.y / T), 2.0)''')
# bullets from slow-internet players catch up the time their message took
rep('''		var steps := 3
		for s in steps:
			if dead:
				break
			b.x += b.vx * dt / steps
			b.y += b.vy * dt / steps''', '''		var bdt := dt + b.ff
		b.ff = 0.0
		var steps := maxi(3, ceili(Vector2(b.vx, b.vy).length() * bdt / 14.0))
		for s in steps:
			if dead:
				break
			b.x += b.vx * bdt / steps
			b.y += b.vy * bdt / steps''')
# server keeps a short history of where everyone was, and each player's delay
rep('''	for p in players:
		update_player(p, dt)
	update_bullets(dt)''', '''	for p in players:
		update_player(p, dt)
	if net_role == "host":
		for p in players:
			p.hist.append(Vector3(t, p.x, p.y))
			while p.hist.size() > 2 and p.hist[0].x < t - 0.4:
				p.hist.pop_front()
	update_bullets(dt)''')
rep('''	snaps_sent += 1''', '''	snaps_sent += 1
	if snaps_sent % 20 == 0 and multiplayer.multiplayer_peer != null and multiplayer.multiplayer_peer.has_method("get_peer"):
		for p in players:
			if p.remote:
				var sp = multiplayer.multiplayer_peer.get_peer(p.peer_id)
				if sp != null:
					p.lat = clampf(sp.get_statistic(3) / 2000.0 + 0.03, 0.0, 0.25)''')

s += '''
# ================= FAIR PLAY + RESPAWN (v1.4) =================
const SPREAD_PAT := [0.0, 0.3, -0.28, 0.14, -0.42, 0.4, -0.12, 0.22, -0.36, 0.46, -0.06, 0.32]

# move everyone else back to where this (remote) shooter saw them; returns what to put back
func rewind_others(shooter: Player) -> Array:
	var saved := []
	if not shooter.remote or shooter.lat <= 0.0:
		return saved
	var tt := t - shooter.lat
	for o in players:
		if o == shooter or o.hist.is_empty():
			continue
		var hp: Vector3 = o.hist[0]
		for h in o.hist:
			if h.x <= tt:
				hp = h
			else:
				break
		saved.append([o, o.x, o.y])
		o.x = hp.y
		o.y = hp.z
	return saved

func restore_others(saved: Array) -> void:
	for sv in saved:
		sv[0].x = sv[1]
		sv[0].y = sv[2]

# a beam of light drops the soldier in; everyone sees it for half a second
func draw_drop_beam(c: Vector2, age: float, wt: Transform2D) -> void:
	draw_set_transform_matrix(wt)
	var k := clampf(age / 0.6, 0.0, 1.0)
	var a := 1.0 - k
	var bw := 30.0 * (1.0 - k * 0.7)
	var top := c.y - 420.0 * gsign()
	var foot := c.y + 22.0 * gsign()
	draw_rect(Rect2(c.x - bw / 2, minf(top, foot), bw, absf(foot - top)), Color(0.55, 0.95, 1.0, 0.28 * a))
	draw_rect(Rect2(c.x - bw / 5, minf(top, foot), bw / 2.5, absf(foot - top)), Color(1, 1, 1, 0.55 * a))
	draw_arc(Vector2(c.x, foot), 10.0 + 70.0 * k, 0, TAU, 32, Color(0.6, 0.97, 1.0, 0.8 * a), 3.0, true)
	draw_arc(Vector2(c.x, foot), 4.0 + 40.0 * k, 0, TAU, 24, Color(1, 1, 1, 0.6 * a), 2.0, true)

# while you wait: a pulsing target where you will land (only on your screen)
func draw_landing_marker() -> void:
	if players.is_empty() or my_idx >= players.size() or state != "play":
		return
	var me: Player = players[my_idx]
	if me.alive or me.respawn_t >= 0.9:
		return
	var k := 1.0 - clampf(me.respawn_t / 0.9, 0.0, 1.0)
	var c := Vector2(me.x + 10, me.y + 21)
	var foot := c + Vector2(0, 22 * gsign())
	var pulse := 0.5 + 0.5 * sin(time_s * 10.0)
	draw_arc(foot, 18.0 + 6.0 * pulse, 0, TAU, 32, Color(C_ARC, 0.85 * k), 3.0, true)
	draw_arc(foot, 8.0, 0, TAU, 20, Color(1, 1, 1, 0.7 * k), 2.0, true)
	var ay := c.y - (46.0 + 6.0 * pulse) * gsign()
	draw_colored_polygon(PackedVector2Array([Vector2(c.x - 9, ay), Vector2(c.x + 9, ay), Vector2(c.x, ay + 12 * gsign())]), Color(C_ARC, k))
'''
open(P, "w").write(s)
print("ok")
