"""v1.8 part B: sit by holding the move stick down (crouching takes less blast damage; a sniper who keeps
holding lies down); no SIT button; real shotgun feel; credits fit the screen."""
import sys
P = "/home/claude/skysquad/main.gd"
s = open(P).read()
ERR = []
def rep(a, b, c=1):
    global s
    if s.count(a) != c:
        ERR.append("expected %d got %d: %r" % (c, s.count(a), a[:120])); return
    s = s.replace(a, b)

# ---------- sit = hold the stick down ----------
rep('''	if inp.down and not pv.get("down", false) and p.on_ground:
		var w0 = p.slots[p.cur]
		if p.posture == "stand":
			set_posture(p, "crouch")
		elif p.posture == "crouch" and w0 != null and w0.type == "sniper":
			set_posture(p, "prone")
		else:
			set_posture(p, "stand")''', '''	# hold down to sit; let go to stand up. A sniper who keeps holding lies down flat.
	var want_post := "stand"
	if inp.down and p.on_ground and not p.in_water:
		p.down_t += dt
		var w0 = p.slots[p.cur]
		want_post = "prone" if (w0 != null and w0.type == "sniper" and p.down_t > 0.6) else "crouch"
	else:
		p.down_t = 0.0
	if p.posture != want_post and (p.on_ground or want_post == "stand"):
		set_posture(p, want_post)''')
rep('\tvar shoot_buf := 0.0\n', '\tvar shoot_buf := 0.0\n\tvar down_t := 0.0\n')
rep('''		if d.y > rad * 0.6 and absf(d.x) < rad * 0.5:
			inp.down = true''', '''		if d.y > rad * 0.55 and absf(d.x) < rad * 0.65:
			inp.down = true''')
rep('''	inp.down = key(KEY_S) or key(KEY_DOWN) or btn_held.has("SIT") or stick_down''', '''	inp.down = key(KEY_S) or key(KEY_DOWN) or stick_down''')
rep('''	out.append({"n": "SIT", "p": Vector2(mirror_x(safe_l + r + 14 * u), sh * 0.42), "r": r * 0.85})
''', '')
rep('''"Left thumb: move, push up to fly.",''', '''"Left thumb: move, up to fly, hold down to sit.",''')
# sitting soldiers take less from blasts
rep('''			var f := clampf((1.0 - d / big) * 1.35, 0.0, 1.0)''', '''			var f := clampf((1.0 - d / big) * 1.35, 0.0, 1.0)
			if p.posture == "crouch":
				f *= 0.55
			elif p.posture == "prone":
				f *= 0.4''')

# ---------- shotgun: a wide close-range blast that hits hard up close and fades with distance ----------
rep('''"shotgun": {"name": "SHOTGUN", "dmg": 14.0, "rate": 0.9,  "mag": 6,  "spare": 18,  "reload": 2.0, "spread": 0.24,  "speed": 1150.0, "pellets": 8, "life": 0.36,''',
    '''"shotgun": {"name": "SHOTGUN", "dmg": 15.0, "rate": 0.85, "mag": 6,  "spare": 18,  "reload": 2.0, "spread": 0.34,  "speed": 1300.0, "pellets": 10, "life": 0.27,''')
rep('''						var head: bool = Vector2(b.x, b.y).distance_to(head_pos(p)) < 9.5
						var dmg: float = b.dmg * (S.headshot if head else 1.0)
						if p.protect_t <= 0:
							p.vx += signf(b.vx) * 25''', '''						var head: bool = Vector2(b.x, b.y).distance_to(head_pos(p)) < 9.5
						var dmg: float = b.dmg * (S.headshot if head else 1.0)
						if b.gun == "shotgun":
							# full power point blank, about a third at the end of its reach
							dmg *= lerpf(1.0, 0.35, clampf(1.0 - b.life / maxf(0.01, b.max_life), 0.0, 1.0))
						if p.protect_t <= 0:
							if b.gun == "shotgun":
								var bd := Vector2(b.vx, b.vy).normalized()
								p.vx += bd.x * 40
								p.vy += bd.y * 22
							else:
								p.vx += signf(b.vx) * 25''')
# look and sound: big blast, smoke, pellets as short streaks, pump action after every shot
rep('''		var fw := 24.0 * (1.3 if gun == "shotgun" else 1.0)
		draw_texture_rect(tex.flash, Rect2(mz.x - 1, mz.y - 7, fw, 14), false)''', '''		var fw := 24.0 * (2.0 if gun == "shotgun" else 1.0)
		var fhh := 14.0 * (1.9 if gun == "shotgun" else 1.0)
		draw_texture_rect(tex.flash, Rect2(mz.x - 1, mz.y - fhh / 2, fw, fhh), false)''')
rep('''		if wt == "ak47" or wt == "sniper":
			add_part(mz.x, mz.y, cos(p.aim) * 30, sin(p.aim) * 30 - 10, 0.5, Color(0.85, 0.85, 0.85, 0.45), 6, -0.02, "smoke", 18)''', '''		if wt == "ak47" or wt == "sniper":
			add_part(mz.x, mz.y, cos(p.aim) * 30, sin(p.aim) * 30 - 10, 0.5, Color(0.85, 0.85, 0.85, 0.45), 6, -0.02, "smoke", 18)
		if wt == "shotgun":
			for k in 4:
				var sa: float = p.aim + randf_range(-0.35, 0.35)
				add_part(mz.x, mz.y, cos(sa) * randf_range(60, 140), sin(sa) * randf_range(60, 140) - 10, 0.6, Color(0.9, 0.88, 0.82, 0.5), 8, -0.03, "smoke", 30)
			for k in 6:
				var ka: float = p.aim + randf_range(-0.4, 0.4)
				add_part(mz.x, mz.y, cos(ka) * randf_range(250, 420), sin(ka) * randf_range(250, 420), 0.12, Color("#ffd27a"), 2.5, 0.0)''')
rep('''			var tl: float = 0.03 if b.gun == "sniper" else 0.016
			draw_line(Vector2(b.x, b.y), Vector2(b.x - b.vx * tl, b.y - b.vy * tl), Color(1, 0.95, 0.7, 0.9), 2.6 if b.gun == "sniper" else 2.0, true)''',
    '''			var tl: float = 0.03 if b.gun == "sniper" else (0.012 if b.gun == "shotgun" else 0.016)
			draw_line(Vector2(b.x, b.y), Vector2(b.x - b.vx * tl, b.y - b.vy * tl), Color(1, 0.88, 0.55, 0.95) if b.gun == "shotgun" else Color(1, 0.95, 0.7, 0.9), 2.6 if (b.gun == "sniper" or b.gun == "shotgun") else 2.0, true)''')
# a firm kick for the shotgun
rep('''		kick -= Vector2(cos(p.aim), sin(p.aim)) * minf(d.recoil * 0.5, 3.0)''', '''		kick -= Vector2(cos(p.aim), sin(p.aim)) * (6.0 if wt == "shotgun" else minf(d.recoil * 0.5, 3.0))''')
# pump action: the front hand pulls the pump back and pushes it forward, with a click
rep('''	var fh := grip if dual else front_hand''', '''	var fh := grip if dual else front_hand
	if gun == "shotgun" and busy == "" and not swim:
		var pk := (t - p.shot_t - 0.22) / 0.32
		if pk > 0.0 and pk < 1.0:
			fh -= dir * sin(pk * PI) * 7.0
			if pk < 0.12 and p.pump_done != p.shot_t:
				p.pump_done = p.shot_t
				play("reload", c, -12.0 if is_me(p) else -18.0, 0.0)''')
rep('\tvar shoot_buf := 0.0\n', '\tvar shoot_buf := 0.0\n\tvar pump_done := -1.0\n')

# ---------- credits: two columns, scaled to fit any screen ----------
i = s.index("const CREDITS := [")
j = s.index('\tui_button("BACK", Rect2(r.end.x - 132 * u, r.end.y - 54 * u, 108 * u, 38 * u), "back")\n', i)
j = j + len('\tui_button("BACK", Rect2(r.end.x - 132 * u, r.end.y - 54 * u, 108 * u, 38 * u), "back")\n')
s = s[:i] + '''const CREDITS_L := [
	["GAME", ""],
	["Sky Squad", "Arc Light Studio"],
	["Design and testing", "Arc Light Studio and friends"],
	["Code, art and music", "Made with Claude (Anthropic)"],
	["MUSIC", ""],
	["Sky Squad Theme", "Original music for this game"],
]
const CREDITS_R := [
	["SOUNDS", ""],
	["Sound effects", "Kenney.nl (CC0)"],
	["More sound effects", "Freedoom project (BSD)"],
	["ENGINE", ""],
	["Godot Engine 4.3", "godotengine.org (MIT)"],
]

func draw_credits() -> void:
	var w := minf(sw - 32 * u, 720 * u)
	var h := minf(sh - 24 * u, 300 * u)
	var r := panel(w, h)
	var x := r.position.x + 26 * u
	var y := r.position.y + 42 * u
	txh("CREDITS", Vector2(x, y), 24 * u, C_ARC, 0, 5 * u)
	txt("Thanks for playing!", Vector2(r.end.x - 26 * u, y - 4 * u), 12 * u, C_MUTED, 2)
	var colw := (w - 52 * u - 24 * u) / 2.0
	for ci in 2:
		var rows: Array = CREDITS_L if ci == 0 else CREDITS_R
		var cx := x + ci * (colw + 24 * u)
		var yy := y + 28 * u
		for i in rows.size():
			var row: Array = rows[i]
			var k2 := ease_out((ui_t - 0.1 - i * 0.04) / 0.3)
			var ga1 := ga
			ga *= k2
			if row[1] == "":
				yy += 8 * u
				txt(row[0], Vector2(cx, yy), 10 * u, C_CYAN)
				yy += 16 * u
			else:
				txt(row[0], Vector2(cx, yy), 12 * u, C_INK)
				txt(row[1], Vector2(cx, yy + 15 * u), 10.5 * u, C_MUTED)
				yy += 34 * u
			ga = ga1
	ui_button("BACK", Rect2(r.end.x - 126 * u, r.end.y - 52 * u, 100 * u, 36 * u), "back")
''' + s[j:]
if ERR:
    print("\n".join(ERR)); sys.exit(1)
open(P, "w").write(s)
print("ok")
