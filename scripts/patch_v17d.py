"""v1.7 part D: one THROW button (grenade / mine / smoke, tap the icons to switch);
HAND button: swing your arms in the air to fly faster sideways."""
import sys
P = "/home/claude/skysquad/main.gd"
s = open(P).read()
ERR = []
def rep(a, b, c=1):
    global s
    if s.count(a) != c:
        ERR.append("expected %d got %d: %r" % (c, s.count(a), a[:120])); return
    s = s.replace(a, b)

# ---------- input fields ----------
rep('''"zoom": false, "bomb": false, "smoke": false}''', '''"zoom": false, "bomb": false, "smoke": false, "tk": 0, "hand": false}''', 2)
rep('\tvar shoot_buf := 0.0\n', '\tvar shoot_buf := 0.0\n\tvar hand_on := false\n\tvar hand_k := 0.0\n\tvar tk := 0\n')

# ---------- server: one throw button, the kind you picked; empty kinds are skipped ----------
rep('''	var none_left: bool = (inp.grenade and not pv.get("grenade", false) and p.grenades <= 0) or (inp.bomb and not pv.get("bomb", false) and p.bombs <= 0) or (inp.get("smoke", false) and not pv.get("smoke", false) and p.smokes <= 0)''',
'''	var thr: bool = inp.grenade and not pv.get("grenade", false)
	p.tk = pick_kind(p, int(inp.get("tk", 0)))
	var do_frag: bool = thr and p.tk == 0
	var do_mine: bool = (thr and p.tk == 1) or (inp.bomb and not pv.get("bomb", false))
	var do_smoke: bool = (thr and p.tk == 2) or (inp.get("smoke", false) and not pv.get("smoke", false))
	if p.hand_on:
		do_frag = false
		do_mine = false
		do_smoke = false
	var none_left: bool = (thr and p.grenades + p.bombs + p.smokes <= 0) or (inp.bomb and not pv.get("bomb", false) and p.bombs <= 0) or (inp.get("smoke", false) and not pv.get("smoke", false) and p.smokes <= 0)''')
rep('''	if inp.grenade and not pv.get("grenade", false) and p.grenades > 0 and p.g_cd <= 0:''', '''	if do_frag and p.grenades > 0 and p.g_cd <= 0:''')
rep('''	if inp.bomb and not pv.get("bomb", false) and p.bombs > 0 and p.g_cd <= 0:''', '''	if do_mine and p.bombs > 0 and p.g_cd <= 0:''')
rep('''	if inp.get("smoke", false) and not pv.get("smoke", false) and p.smokes > 0 and p.g_cd <= 0:''', '''	if do_smoke and p.smokes > 0 and p.g_cd <= 0:''')

# ---------- hand: faster in the air, arms swing, no shooting meanwhile ----------
rep('''	var target: float = inp.mx * S.move_speed * (0.55 if p.in_water else 1.0) * post_mul
	var acc := 2600.0 if p.on_ground else 1500.0''', '''	var target: float = inp.mx * S.move_speed * (0.55 if p.in_water else 1.0) * post_mul
	var acc := 2600.0 if p.on_ground else 1500.0
	p.hand_on = hand_ok(p, bool(inp.get("hand", false)))
	if p.hand_on:
		target *= HAND_SPEED
		acc *= 1.3''')
rep('''func predict_step(p: Player, mx: float, fly_in: bool, dt: float) -> void:''', '''func predict_step(p: Player, mx: float, fly_in: bool, dt: float, hand := false) -> void:''')
rep('''	var target: float = mx * S.move_speed * (0.55 if p.in_water else 1.0) * post_mul
	var acc := 2600.0 if p.on_ground else 1500.0''', '''	var target: float = mx * S.move_speed * (0.55 if p.in_water else 1.0) * post_mul
	var acc := 2600.0 if p.on_ground else 1500.0
	p.hand_on = hand_ok(p, hand)
	if p.hand_on:
		target *= HAND_SPEED
		acc *= 1.3''')
rep('''	predict_step(p, float(inp.mx), bool(inp.fly), dt)
	pred_hist.append([in_seq, float(inp.mx), bool(inp.fly), dt])''', '''	predict_step(p, float(inp.mx), bool(inp.fly), dt, bool(inp.get("hand", false)))
	pred_hist.append([in_seq, float(inp.mx), bool(inp.fly), dt, bool(inp.get("hand", false))])''')
rep('''		predict_step(p, h[1], h[2], h[3])''', '''		predict_step(p, h[1], h[2], h[3], h[4] if h.size() > 4 else false)''')
rep('''	if p.melee_anim > 0.05 or p.switch_t > 0.06 or t - p.born_srv < 0.45:''', '''	if p.melee_anim > 0.05 or p.switch_t > 0.06 or t - p.born_srv < 0.45 or p.hand_on:''')
rep('''	animate(p, dt)
	var w = p.slots[p.cur]''', '''	animate(p, dt)
	p.hand_k = move_toward(p.hand_k, 1.0 if p.hand_on else 0.0, dt * 7.0)
	var w = p.slots[p.cur]''')

# ---------- network: picked kind and hand go in the input packet; others see your arms swing ----------
rep('''i2.bomb, i2.smoke, in_seq]''', '''i2.bomb, i2.smoke, in_seq, int(i2.get("tk", 0)), bool(i2.get("hand", false))]''')
rep('''			if a.size() > 13:
				p.ack = maxi(p.ack, int(a[13]))''', '''			if a.size() > 13:
				p.ack = maxi(p.ack, int(a[13]))
			inp.tk = clampi(int(a[14]), 0, 2) if a.size() > 14 else 0
			inp.hand = a.size() > 15 and bool(a[15])''')
rep('''		var fl := (1 if p.alive else 0) | (2 if p.jet_on else 0) | (4 if p.on_ground else 0) | (8 if p.in_water else 0)''',
    '''		var fl := (1 if p.alive else 0) | (2 if p.jet_on else 0) | (4 if p.on_ground else 0) | (8 if p.in_water else 0) | (16 if p.hand_on else 0)''')
rep('''		if not mine:
			p.jet_on = (fl & 2) != 0
			p.on_ground = (fl & 4) != 0''', '''		if not mine:
			p.jet_on = (fl & 2) != 0
			p.on_ground = (fl & 4) != 0
			p.hand_on = (fl & 16) != 0''')

# ---------- phone controls ----------
rep('''	inp.grenade = key(KEY_G) or btn_held.has("GRENADE")''', '''	inp.grenade = key(KEY_G) or btn_held.has("GRENADE")
	for kk in 3:
		if key([KEY_1, KEY_2, KEY_3][kk]):
			my_tk = kk
	my_tk = pick_kind(me, my_tk)
	inp.tk = my_tk
	inp.hand = key(KEY_SHIFT) or btn_held.has("HAND")''')
rep('''		if me.bombs > 0:
			out.append({"n": "BOMB", "p": Vector2(bx + inward * r * 2.5, sh * 0.47), "r": r * 0.85})
		if me.smokes > 0:
			out.append({"n": "SMOKE", "p": Vector2(bx + inward * r * 2.5, sh * 0.64), "r": r * 0.85})''', '''		# the three throwables next to the THROW button: tap one to pick it
		for kk in 3:
			out.append({"n": "TK%d" % kk, "p": Vector2(bx + inward * r * 1.95, sh * 0.30 + (kk - 1) * r * 1.3 + (r * 2.2 if WD[w.type].zooms.size() > 1 and w != null else 0.0)), "r": r * 0.6})''')
rep('''	out.append({"n": "SIT", "p": Vector2(mirror_x(safe_l + r + 14 * u), sh * 0.42), "r": r * 0.85})''', '''	out.append({"n": "SIT", "p": Vector2(mirror_x(safe_l + r + 14 * u), sh * 0.42), "r": r * 0.85})
	out.append({"n": "HAND", "p": Vector2(mirror_x(safe_l + r + 14 * u), sh * 0.26), "r": r * 0.85})''')
rep('''	for b in buttons():
		if pos.distance_to(b.p) < b.r + 12 * u:
			btn_held[b.n] = id
			return''', '''	for b in buttons():
		if pos.distance_to(b.p) < b.r + (6 if b.n.begins_with("TK") else 12) * u:
			if b.n.begins_with("TK"):
				my_tk = int(b.n.substr(2))
				return
			btn_held[b.n] = id
			return''')
rep('''			"GRENADE":
				tex_c("grenade", b.p + Vector2(0, -3 * u), Vector2(16, 19) * u)
				txt("%d" % me.grenades, b.p + Vector2(b.r * 0.55, b.r * 0.7), 11 * u, C_INK, 1, 3 * u)''', '''			"GRENADE":
				var kk := pick_kind(me, my_tk)
				tex_c(THROW_TEX[kk][0], b.p + Vector2(0, -3 * u), THROW_TEX[kk][1] * u)
				txt("%d" % kind_count(me, kk), b.p + Vector2(b.r * 0.55, b.r * 0.7), 11 * u, C_INK, 1, 3 * u)
			"TK0", "TK1", "TK2":
				var kk2 := int(b.n.substr(2))
				var on: bool = pick_kind(me, my_tk) == kk2
				var cnt := kind_count(me, kk2)
				if on:
					draw_arc(b.p, b.r + 2 * u, 0, TAU, 32, C_ARC, 2.5 * u, true)
				var tcol := Color(1, 1, 1, 1.0 if cnt > 0 else 0.3)
				tex_c(THROW_TEX[kk2][0], b.p + Vector2(0, -1 * u), THROW_TEX[kk2][1] * u * 0.7, tcol)
				txt("%d" % cnt, b.p + Vector2(b.r * 0.7, b.r * 0.75), 9 * u, C_INK if cnt > 0 else C_MUTED, 1, 2 * u)
			"HAND":
				var sw2 := sin(time_s * 10.0) * 0.5 if btn_held.has("HAND") else 0.0
				for hs in [-1.0, 1.0]:
					var ang := -PI / 2 + hs * (0.55 + sw2 * hs)
					draw_line(b.p + Vector2(0, 4 * u), b.p + Vector2(0, 4 * u) + Vector2(cos(ang), sin(ang)) * 11 * u, C_INK, 3 * u, true)
					draw_circle(b.p + Vector2(0, 4 * u) + Vector2(cos(ang), sin(ang)) * 12 * u, 3 * u, C_INK)
				txt("HAND", b.p + Vector2(0, b.r * 0.75), 8 * u, C_INK, 1, 2 * u)''')

# ---------- drawing the arms swinging ----------
rep('''	else:
		body = base * Transform2D(0.0, Vector2.ONE, 0.0, Vector2(0, (1.0 if crouch else 0.0) + bob))''', '''	else:
		var lean := p.hand_k * 0.3 * clampf(p.vx / 120.0, -1.0, 1.0) * face
		body = base * Transform2D(lean, Vector2.ONE, 0.0, Vector2(0, (1.0 if crouch else 0.0) + bob))''')
rep('''	var back_tgt := grip2 if dual else grip''', '''	var back_tgt := grip2 if dual else grip
	var swim := p.hand_k > 0.3
	var sw_ph := time_s * 13.0 + p.id
	if swim:
		# arms paddle through the air, one forward while the other goes back
		var a1 := -0.4 + sin(sw_ph) * 1.4
		back_tgt = sh_pt + Vector2(-2, 0) + Vector2(cos(a1), sin(a1)) * 12.0''')
rep('''	if dual:
		draw_set_transform_matrix(body * Transform2D(gun_rot, Vector2.ONE, 0.0, grip2))''', '''	if swim:
		draw_texture_rect(tex.hand, Rect2(back_tgt - Vector2(3, 3), Vector2(6, 6)), false)
	if dual and not swim:
		draw_set_transform_matrix(body * Transform2D(gun_rot, Vector2.ONE, 0.0, grip2))''')
rep('''	draw_texture_rect(tex["gun_" + gun], Rect2(-m.grip[0] * gd, -m.grip[1] * gd, gsz.x, gsz.y), false, tint)
	if gun == "minigun" and p.spin > 0.05:''', '''	if not swim:
		draw_texture_rect(tex["gun_" + gun], Rect2(-m.grip[0] * gd, -m.grip[1] * gd, gsz.x, gsz.y), false, tint)
	if gun == "minigun" and p.spin > 0.05 and not swim:''')
rep('''		fh = sh_pt + Vector2(cos(ka), sin(ka)) * 12.0
	draw_line(sh_pt + Vector2(3, 0), fh, C_OUT, 6.0, true)''', '''		fh = sh_pt + Vector2(cos(ka), sin(ka)) * 12.0
	if swim:
		var a2 := -0.4 - sin(sw_ph) * 1.4
		fh = sh_pt + Vector2(3, 0) + Vector2(cos(a2), sin(a2)) * 12.0
	draw_line(sh_pt + Vector2(3, 0), fh, C_OUT, 6.0, true)''')
rep('''	draw_texture_rect(tex.hand, Rect2(grip - Vector2(3, 3), Vector2(6, 6)), false)
	if mk >= 0:''', '''	if not swim:
		draw_texture_rect(tex.hand, Rect2(grip - Vector2(3, 3), Vector2(6, 6)), false)
	if mk >= 0:''')

s += '''
# ================= THROW + HAND (v1.7) =================
const HAND_SPEED := 1.45
const THROW_TEX := [["grenade", Vector2(16, 19)], ["timebomb", Vector2(20, 15)], ["smoke_can", Vector2(13, 17)]]
var my_tk := 0

func kind_count(p: Player, k: int) -> int:
	return [p.grenades, p.bombs, p.smokes][clampi(k, 0, 2)]

# the kind you picked, or the next one you still have
func pick_kind(p: Player, want: int) -> int:
	want = clampi(want, 0, 2)
	for i in 3:
		var k := (want + i) % 3
		if kind_count(p, k) > 0:
			return k
	return want

func hand_ok(p: Player, want: bool) -> bool:
	return want and not p.on_ground and not p.in_water and p.posture == "stand" and p.net_t <= 0 and p.stun_t <= 0
'''
if ERR:
    print("\n".join(ERR)); sys.exit(1)
open(P, "w").write(s)
print("ok")
