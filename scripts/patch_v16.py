"""v1.6 smoothness: faster aim, snappier movement, no lost taps (fire buffer + tap latching), 30 updates a second,
smooth other players (render a little in the past and glide between updates), smooth bullets on joining phones,
off-screen culling, 60 fps on phones, Show FPS option."""
import sys
P = "/home/claude/skysquad/main.gd"
s = open(P).read()
ERR = []
def rep(a, b, c=1):
    global s
    if s.count(a) != c:
        ERR.append("expected %d got %d: %r" % (c, s.count(a), a[:120])); return
    s = s.replace(a, b)

rep('# Sky Squad - Arc Light Studio. Playtest build 1.5', '# Sky Squad - Arc Light Studio. Playtest build 1.6')
rep('const VERSION := "1.5"', 'const VERSION := "1.6"')

# ---------- aim + movement feel ----------
rep('"aim_turn": 5.0, "mouse_turn": 10.0,', '"aim_turn": 18.0, "mouse_turn": 30.0,')
rep('"move_speed": 105.0,', '"move_speed": 118.0,')
rep('''	var acc := 1100.0 if p.on_ground else 520.0''', '''	var acc := 2600.0 if p.on_ground else 1500.0
	if target != 0.0 and signf(target) != signf(p.vx):
		acc *= 1.5''', 2)
rep('''		mx = signf(d.x) * clampf((ax - 8 * u) / (rad * 0.75), 0, 1) if ax > 8 * u else 0.0''', '''		mx = signf(d.x) * clampf((ax - 5 * u) / (rad * 0.45), 0, 1) if ax > 5 * u else 0.0''')

# ---------- a tap always fires: buffer it until the gun is ready ----------
rep('\tvar spawn_set := false\n', '\tvar spawn_set := false\n\tvar shoot_buf := 0.0\n\tvar press_hold := {}\n\tvar sbuf: Array = []\n')
rep('''	if not inp.shoot:
		p.fire_lock = false
	if inp.shoot and not p.fire_lock and w != null''', '''	if not inp.shoot:
		p.fire_lock = false
	if inp.shoot and not pv.get("shoot", false):
		p.shoot_buf = 0.22
	p.shoot_buf -= dt
	var want_fire: bool = (inp.shoot or p.shoot_buf > 0.0) and not p.fire_lock
	if want_fire and w != null''')
rep('''		if w.mag > 0:
			fire(p, w)
			w.mag -= 1''', '''		if w.mag > 0:
			fire(p, w)
			p.shoot_buf = 0.0
			w.mag -= 1''')
# server: two input packets in one frame must not swallow a tap
rep('''			inp.smoke = a.size() > 12 and bool(a[12])
			if a.size() > 13:''', '''			inp.smoke = a.size() > 12 and bool(a[12])
			for kk in EDGE_KEYS:
				if inp.get(kk, false):
					p.press_hold[kk] = true
			if a.size() > 13:''')
rep('''	for p in players:
		update_player(p, dt)
	if net_role == "host":''', '''	for p in players:
		if p.remote and not p.press_hold.is_empty():
			for kk in p.press_hold.keys():
				p.inp[kk] = true
			p.press_hold.clear()
	for p in players:
		update_player(p, dt)
	if net_role == "host":''')
# joining phone: a tap between two sends is still sent
rep('''	in_t += dt
	if in_t >= 1.0 / 30.0:
		in_t = minf(in_t - 1.0 / 30.0, 0.03)
		var i2: Dictionary = me.inp''', '''	for kk in EDGE_KEYS:
		if me.inp.get(kk, false):
			in_latch[kk] = true
	in_t += dt
	if in_t >= 1.0 / 30.0:
		in_t = minf(in_t - 1.0 / 30.0, 0.03)
		var i2: Dictionary = me.inp.duplicate()
		for kk in in_latch.keys():
			i2[kk] = true
		in_latch.clear()''')

# ---------- 30 updates a second ----------
rep('''	if snap_t < 0.05:''', '''	if snap_t < SNAP_DT:''')
rep('''	snap_t = minf(snap_t - 0.05, 0.05)''', '''	snap_t = minf(snap_t - SNAP_DT, SNAP_DT)''')
# lag compensation: include the small delay the joining phone uses to glide between updates
rep('''					p.lat = clampf(sp.get_statistic(3) / 2000.0 + 0.03, 0.0, 0.25)''', '''					p.lat = clampf(sp.get_statistic(3) / 2000.0 + INTERP + 0.02, 0.0, 0.35)''')

# ---------- smooth others on joining phones ----------
rep('''	snaps_got += 1
	t = d.t''', '''	snaps_got += 1
	var st: float = d.t
	if absf(st - snap_clock) > 0.3 or snaps_got == 1:
		snap_clock = st
	else:
		snap_clock = lerpf(snap_clock, st, 0.1)
	t = d.t''')
rep('''		p.smokes = int(pf[o + 31])''', '''		p.smokes = int(pf[o + 31])
		if not mine:
			if p.alive and not was_alive:
				p.sbuf.clear()
			p.sbuf.append([st, p.nx, p.ny, p.svx, p.svy, p.naim])
			while p.sbuf.size() > 8:
				p.sbuf.pop_front()''')
rep('''		if i == my_idx and predicting():
			predict_me(p, dt)
		else:
			var age := minf(p.snap_age, 0.12)
			var k := ease_k(18.0, dt)
			p.x += (p.nx + p.vx * age - p.x) * k
			p.y += (p.ny + p.vy * age - p.y) * k
		if i != my_idx:
			p.aim = lerp_angle(p.aim, p.naim, ease_k(16.0, dt))''', '''		if i == my_idx and predicting():
			predict_me(p, dt)
		elif not p.sbuf.is_empty():
			glide(p)
		else:
			var age := minf(p.snap_age, 0.12)
			var k := ease_k(18.0, dt)
			p.x += (p.nx + p.vx * age - p.x) * k
			p.y += (p.ny + p.vy * age - p.y) * k
		if i != my_idx and p.sbuf.is_empty():
			p.aim = lerp_angle(p.aim, p.naim, ease_k(16.0, dt))''')
rep('''	in_t += dt
	if in_t >= 1.0 / 30.0:''', '''	snap_clock += dt
	in_t += dt
	if in_t >= 1.0 / 30.0:''')
# ---------- draw less: skip what is off screen; parts cap ----------
rep('''	if parts.size() > 650:''', '''	if parts.size() > 420:''')
rep('''	leader_now = current_leader()
	draw_event_world()
	for k in pickups:
		draw_pickup(k)''', '''	leader_now = current_leader()
	view_r = (wt.affine_inverse() * Rect2(Vector2.ZERO, Vector2(sw, sh))).grow(90)
	draw_event_world()
	for k in pickups:
		if view_r.has_point(Vector2(k.x, k.y)):
			draw_pickup(k)''')
rep('''	for cp in corpses:
		draw_corpse(cp, wt)''', '''	for cp in corpses:
		if view_r.has_point(Vector2(cp.x, cp.y)):
			draw_corpse(cp, wt)''')
rep('''	draw_landing_marker()
	draw_set_transform_matrix(wt)
	for b in bullets:
		if b.flame:''', '''	draw_landing_marker()
	draw_set_transform_matrix(wt)
	for b in bullets:
		if not view_r.has_point(Vector2(b.x, b.y)):
			continue
		if b.flame:''')
rep('''	for q in parts:
		var k: float = clampf(q.life / q.max_life, 0, 1)''', '''	for q in parts:
		if not view_r.has_point(Vector2(q.x, q.y)):
			continue
		var k: float = clampf(q.life / q.max_life, 0, 1)''')

# ---------- 60 fps on phones, FPS readout ----------
rep('''	DisplayServer.screen_set_keep_on(true)''', '''	DisplayServer.screen_set_keep_on(true)
	if OS.has_feature("mobile"):
		Engine.max_fps = 60''')
rep('''	"name": "", "lan_bots": 2,''', '''	"name": "", "show_fps": false, "lan_bots": 2,''')
rep('''	["sound", "Sound", [true, false], ["On", "Off"]],
]''', '''	["sound", "Sound", [true, false], ["On", "Off"]],
	["show_fps", "Show FPS", [false, true], ["Off", "On"]],
]''')
rep('''func draw_top_layers() -> void:''', '''func draw_top_layers() -> void:
	if cfg.show_fps:
		draw_set_transform_matrix(Transform2D.IDENTITY)
		txt("%d FPS" % Engine.get_frames_per_second(), Vector2(sw - 10 * u, sh - 8 * u), 11 * u, C_ARC, 2, 3 * u)''')

s += '''
# ================= SMOOTH (v1.6) =================
const SNAP_DT := 1.0 / 30.0
const INTERP := 0.1
const EDGE_KEYS := ["shoot", "swap", "grenade", "melee", "reload", "down", "bomb", "smoke", "zoom"]
var in_latch := {}
var snap_clock := 0.0
var view_r := Rect2(-100000, -100000, 200000, 200000)

# show another player a little in the past, gliding between the two updates around that moment
func glide(p: Player) -> void:
	var rt := snap_clock - INTERP
	var buf := p.sbuf
	var a: Array = buf[0]
	if rt <= a[0]:
		p.x = a[1]
		p.y = a[2]
		p.aim = a[5]
		return
	for j in range(buf.size() - 1):
		var s0: Array = buf[j]
		var s1: Array = buf[j + 1]
		if rt >= s0[0] and rt <= s1[0]:
			var k := (rt - s0[0]) / maxf(0.001, s1[0] - s0[0])
			p.x = lerpf(s0[1], s1[1], k)
			p.y = lerpf(s0[2], s1[2], k)
			p.vx = lerpf(s0[3], s1[3], k)
			p.vy = lerpf(s0[4], s1[4], k)
			p.aim = lerp_angle(s0[5], s1[5], k)
			return
	# no newer update yet: carry on a little along the last known speed
	var l: Array = buf[-1]
	var ex := minf(rt - l[0], 0.15)
	p.x = l[1] + l[3] * ex
	p.y = l[2] + l[4] * ex
	p.vx = l[3]
	p.vy = l[4]
	p.aim = l[5]

'''
if ERR:
    print("\n".join(ERR)); sys.exit(1)
open(P, "w").write(s)
print("ok")
