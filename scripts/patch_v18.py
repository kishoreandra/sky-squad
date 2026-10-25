"""v1.8 smoothness: no frame cap judder on phones, smooth distance-based screen shake with a setting,
no hidden self-push when firing, your own shots show at once on a joining phone."""
import sys
P = "/home/claude/skysquad/main.gd"
s = open(P).read()
ERR = []
def rep(a, b, c=1):
    global s
    if s.count(a) != c:
        ERR.append("expected %d got %d: %r" % (c, s.count(a), a[:120])); return
    s = s.replace(a, b)

rep('const VERSION := "1.7"', 'const VERSION := "1.8"')
rep('# Sky Squad - Arc Light Studio. Playtest build 1.7', '# Sky Squad - Arc Light Studio. Playtest build 1.8')

# 1. let the phone run at its own screen rate (a 60 cap on 90/120 Hz screens gives uneven frames)
rep('''	DisplayServer.screen_set_keep_on(true)
	if OS.has_feature("mobile"):
		Engine.max_fps = 60''', '''	DisplayServer.screen_set_keep_on(true)
	DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_ENABLED)''')

# 2. screen shake: smooth wobble, weaker with distance, a setting to turn it down
rep('''	"name": "", "show_fps": false, "music": true,''', '''	"name": "", "show_fps": false, "music": true, "shake": "low",''')
rep('''	["music", "Menu music", [true, false], ["On", "Off"]],''', '''	["shake", "Screen shake", ["low", "full", "off"], ["Low", "Full", "Off"]],
	["music", "Menu music", [true, false], ["On", "Off"]],''')
rep('''	var shk := randf_range(-0.5, 0.5) * shake if shake > 0 else 0.0
	var wt := Transform2D(0.0, Vector2(zoom, zoom), 0.0, Vector2(-cam.x * zoom + shk, -cam.y * zoom + shk))''',
    '''	var sm: float = {"low": 0.45, "full": 1.0, "off": 0.0}.get(cfg.get("shake", "low"), 0.45)
	var shv := Vector2(sin(time_s * 37.0) + 0.5 * sin(time_s * 61.0), cos(time_s * 41.0) + 0.5 * sin(time_s * 53.0 + 1.0)) * 0.33 * shake * sm
	shv += kick * sm
	var wt := Transform2D(0.0, Vector2(zoom, zoom), 0.0, Vector2(-cam.x * zoom + shv.x, -cam.y * zoom + shv.y))''')
rep('''func explode_fx(x: float, y: float, r: float, es := "explosion") -> void:
	shake = maxf(shake, 14.0)''', '''func explode_fx(x: float, y: float, r: float, es := "explosion") -> void:
	# shake only when the blast is near you, and less the further away it is
	var view_c := cam + Vector2(sw, sh) / zoom / 2.0
	var near := clampf(1.0 - Vector2(x, y).distance_to(view_c) / 650.0, 0.0, 1.0)
	shake = maxf(shake, 12.0 * near * near)''')
# your own shot: a small smooth kick back instead of random jitter
rep('''	if is_me(p):
		shake = maxf(shake, d.recoil * (0.9 if wt == "ak47" else 0.5))''', '''	if is_me(p):
		kick -= Vector2(cos(p.aim), sin(p.aim)) * minf(d.recoil * 0.5, 3.0)''')
rep('''	shake = maxf(0.0, shake - dt * 30)''', '''	shake = maxf(0.0, shake - dt * 30)
	kick *= exp(-14.0 * dt)''', 2)

# 3. no hidden push backwards when you fire (the phone could not guess it, so you got pulled back)
rep('''	if d.push > 0 and p.posture == "stand":
		p.vx -= cos(p.aim) * d.push
		p.vy -= sin(p.aim) * d.push * 0.5
	fire_fx(p, w.type, mz)''', '''	fire_fx(p, w.type, mz)''')

# 4. own shots at once on a joining phone; the server's copies of them are not shown twice
rep('''		b.append_array([x.x, x.y, x.vx, x.vy, 1.0 if x.rocket else (2.0 if x.net else (3.0 if x.flame else 0.0)), x.life, x.max_life])''',
    '''		b.append_array([x.x, x.y, x.vx, x.vy, 1.0 if x.rocket else (2.0 if x.net else (3.0 if x.flame else 0.0)), x.life, x.max_life, float(players.find(x.owner))])''')
rep('''	for j in range(0, bb.size(), 7):''', '''	for j in range(0, bb.size(), 8):
		if int(bb[j + 7]) == my_idx and local_shots_on():
			continue''')
rep('''		b.life = bb[j + 5]
		b.max_life = bb[j + 6]
		bullets.append(b)''', '''		b.life = bb[j + 5]
		b.max_life = bb[j + 6]
		bullets.append(b)
	for lb in my_shots:
		bullets.append(lb)''')
rep('''		"f":
			if int(e[1]) < players.size():
				fire_fx(players[e[1]], e[2], e[3])''', '''		"f":
			if int(e[1]) < players.size() and not (int(e[1]) == my_idx and local_shots_on() and LOCAL_GUNS.has(str(e[2]))):
				fire_fx(players[e[1]], e[2], e[3])''')
rep('''	var me: Player = players[my_idx]
	human_input()
	if pick_request != "":
		latch_pick = pick_request''', '''	var me: Player = players[my_idx]
	human_input()
	local_fire(me, dt)
	if pick_request != "":
		latch_pick = pick_request''')

s += '''
# ================= OWN SHOTS ON A JOINING PHONE (v1.8) =================
# The server still decides every hit. This only shows your own flash, sound and bullets the moment you fire.
const LOCAL_GUNS := ["magnum", "uzi", "ak47", "shotgun", "smg", "sniper", "minigun"]
var my_shots: Array = []
var lf_cd := 0.0
var lf_prev := false
var lf_buf := 0.0
var lf_n := 0
var lf_last := -9.0
var kick := Vector2.ZERO

func local_shots_on() -> bool:
	return net_role == "client" and predicting()

func local_fire(me: Player, dt: float) -> void:
	lf_cd -= dt
	for i in range(my_shots.size() - 1, -1, -1):
		var lb: Bullet = my_shots[i]
		if lb.life <= 0.0 or solid_pt(lb.x, lb.y) or lb.x < 0 or lb.x > WW or lb.y < 0 or lb.y > WH or local_hit(lb):
			my_shots.remove_at(i)
			bullets.erase(lb)
	if not local_shots_on() or not me.alive:
		lf_prev = false
		return
	var inp: Dictionary = me.inp
	if inp.shoot and not lf_prev:
		lf_buf = 0.22
	lf_prev = inp.shoot
	lf_buf -= dt
	var w = me.slots[me.cur]
	if w == null or not LOCAL_GUNS.has(w.type) or w.mag <= 0 or me.reload_t > 0 or me.switch_t > 0.06 or me.melee_anim > 0.05 or me.hand_on or me.stun_t > 0 or time_s - me.born_t < 0.5:
		return
	if not (inp.shoot or lf_buf > 0.0) or lf_cd > 0.0:
		return
	if w.type == "minigun" and me.spin < 1.0:
		return
	var d: Dictionary = WD[w.type]
	lf_cd = d.rate * (0.55 if w.get("dual", false) else 1.0)
	lf_buf = 0.0
	var mz := muzzle_pos(me, w.type)
	fire_fx(me, w.type, mz)
	if w.type == "sniper":
		return
	if time_s - lf_last > 0.35:
		lf_n = 0
	lf_last = time_s
	var off: float = SPREAD_PAT[lf_n % SPREAD_PAT.size()]
	lf_n += 1
	var spread_mul := 1.0 if me.on_ground else 1.35
	if me.posture == "crouch":
		spread_mul = 0.6
	elif me.posture == "prone":
		spread_mul = 0.35
	for i in d.pellets:
		var fan: float = (float(i) / (d.pellets - 1) - 0.5 + off * 0.15) if d.pellets > 1 else off
		var a: float = me.aim + fan * d.spread * spread_mul
		var b := Bullet.new()
		var sp: float = d.speed * (1.0 - 0.06 * (i % 3) if d.pellets > 1 else 1.0)
		b.x = mz.x; b.y = mz.y; b.vx = cos(a) * sp; b.vy = sin(a) * sp
		b.life = d.life; b.max_life = d.life; b.gun = w.type
		my_shots.append(b)
		bullets.append(b)

# a shown bullet stops where it meets another soldier
func local_hit(b: Bullet) -> bool:
	for i in players.size():
		if i == my_idx:
			continue
		var o: Player = players[i]
		if o.alive and b.x > o.x and b.x < o.x + o.w and b.y > o.y and b.y < o.y + o.h:
			return true
	return false
'''
if ERR:
    print("\n".join(ERR)); sys.exit(1)
open(P, "w").write(s)
print("ok")
