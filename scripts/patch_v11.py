"""v1.1: avatars (Locker screen: full looks, helmets, faces, outfits, jetpacks, extras, flame colours), type your own name,
looks shown in game / corpses / menu / lobby and sent over LAN, bots wear random looks. New weapon drop sound."""
import sys
P = "/home/claude/skysquad/main.gd"
s = open(P).read()
AV = open("/home/claude/scripts/av_data.gd").read()

def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        sys.exit(f"expected {count} got {n}: {old[:120]!r}")
    s = s.replace(old, new)

rep('# Sky Squad - Arc Light Studio. Playtest build 1.0', '# Sky Squad - Arc Light Studio. Playtest build 1.1')
rep('const VERSION := "1.0"', 'const VERSION := "1.1"')
rep('const MENU_STATES := ["menu", "match_cfg", "ctrl_cfg", "lan", "lan_join", "ipkey", "connecting", "lobby", "lan_cfg"]',
    'const MENU_STATES := ["menu", "match_cfg", "ctrl_cfg", "lan", "lan_join", "ipkey", "connecting", "lobby", "lan_cfg", "locker", "namekey"]\n' + AV + '''const AV_KEYS := ["h", "f", "o", "j", "x", "fl"]
const AV_DEF := "classic.goggles.army.twin.none.orange"
const AV_BODY_A := Vector2(30.5, 40.5)
const AV_HEAD_A := Vector2(31, 23)
const LK_TABS := [["sets", "LOOKS"], ["h", "HELMET"], ["f", "FACE"], ["o", "OUTFIT"], ["j", "JETPACK"], ["x", "EXTRA"], ["fl", "FLAME"]]
const KB_ROWS := ["1234567890", "QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]''')

# data on players and corpses, saved look
rep('\tvar actor := false\n\tvar jst_t := -9.0\n', '\tvar actor := false\n\tvar look := {}\n\tvar jst_t := -9.0\n')
rep('''	var team := ""
	var t := 0.0
	var face := 1.0''', '''	var team := ""
	var look := {}
	var t := 0.0
	var face := 1.0''')
rep('"name": "", "lan_bots": 2,', '"name": "", "lan_bots": 2, "look": "",')

# textures
rep('''	for g in WD.keys():
		tex["gun_" + g] = load("res://art/gun_%s.png" % g)''', '''	for g in WD.keys():
		tex["gun_" + g] = load("res://art/gun_%s.png" % g)
	for n in AV_RECT.keys():
		tex["av_" + n] = load("res://art/av/%s.png" % n)
	for o in AV_LIST["o"]:
		if o[0] != "army":
			tex["leg_" + o[0]] = load("res://art/av/leg_%s.png" % o[0])
	default_look = parse_look(AV_DEF)''')

# test hooks: open a menu screen, wear a look
rep('''		if a == "--netsize":
			dbg_size = true''', '''		if a == "--netsize":
			dbg_size = true
		if a.begins_with("--state="):
			state = a.substr(8)
		if a.begins_with("--look="):
			cfg.look = a.substr(7)
		if a.begins_with("--lktab="):
			lk_tab = a.substr(8)
		if a.begins_with("--name="):
			cfg.name = a.substr(7)''')

# ---------- players get looks ----------
rep('''	var humans: Array = [{"peer": 1, "name": NAMES[0]}]''', '''	var humans: Array = [{"peer": 1, "name": my_name(), "look": look_str(my_look())}]''')
rep('''		p.team = TEAMS[i]
		p.color = TEAM_COL[i]
		p.bot = not human''', '''		p.team = TEAMS[i]
		p.color = TEAM_COL[i]
		p.look = parse_look(humans[i].get("look", AV_DEF)) if human else random_look()
		p.bot = not human''')
rep('''			p.slots = [full_slot(looks[i][2]), null]
			p.alive = true''', '''			p.slots = [full_slot(looks[i][2]), null]
			p.look = random_look()
			p.alive = true''')
rep('''		pl.append([p.pname, p.team, p.color, p.side, p.bot])''', '''		pl.append([p.pname, p.team, p.color, p.side, p.bot, look_str(plook(p))])''')
rep('''		p.bot = d[4]
		p.slots = [full_slot("uzi"), full_slot("magnum")]''', '''		p.bot = d[4]
		p.look = parse_look(d[5]) if d.size() > 5 else parse_look(AV_DEF)
		p.slots = [full_slot("uzi"), full_slot("magnum")]''')

# LAN hello carries the look; lobby shows it
rep('''func c_hello(nm, ver) -> void:''', '''func c_hello(nm, ver, lk = "") -> void:''')
rep('''	lan_players.append({"peer": id, "name": pick})''', '''	lan_players.append({"peer": id, "name": pick, "look": look_str(parse_look(lk))})''')
rep('''	rpc_id(1, "c_hello", my_name(), VERSION)''', '''	rpc_id(1, "c_hello", my_name(), VERSION, look_str(my_look()))''')
rep('''	lan_players = [{"peer": 1, "name": my_name()}]''', '''	lan_players = [{"peer": 1, "name": my_name(), "look": look_str(my_look())}]''')
rep('''	var info := {"pl": lobby_names(), "mode": cfg.mode,''', '''	var info := {"pl": lobby_names(), "lk": lobby_looks(), "mode": cfg.mode,''')
rep('''func lobby_names() -> Array:''', '''func lobby_looks() -> Array:
	if net_role == "host":
		var out := []
		for lp in lan_players:
			out.append(str(lp.get("look", AV_DEF)))
		return out
	return lobby_info.get("lk", [])

func lobby_names() -> Array:''')
rep('''		circ(Vector2(x + 6 * u, yy - 5 * u), 6 * u, TEAM_COL[i % TEAM_COL.size()])''', '''		var lks := lobby_looks()
		head_icon(parse_look(lks[i]) if i < lks.size() else default_look, Vector2(x + 6 * u, yy - 5 * u), 0.62 * u, TEAM_COL[i % TEAM_COL.size()])''')

# corpses keep the look
rep('''	cp.team = p.team; cp.face = 1.0 if cos(p.aim) >= 0 else -1.0''', '''	cp.team = p.team; cp.face = 1.0 if cos(p.aim) >= 0 else -1.0
	cp.look = plook(p)''')
rep('''		net_fx.append(["c", cp.x, cp.y, cp.vx, cp.vy, cp.spin, cp.team, cp.face])''', '''		net_fx.append(["c", cp.x, cp.y, cp.vx, cp.vy, cp.spin, cp.team, cp.face, look_str(cp.look)])''')
rep('''			cp.face = e[7]
			corpses.append(cp)''', '''			cp.face = e[7]
			cp.look = parse_look(e[8]) if e.size() > 8 else default_look
			corpses.append(cp)''')
rep('''	draw_texture_rect(tex.leg, Rect2(-7, 2, 9, 17), false, Color(0.8, 0.8, 0.8, a))
	draw_texture_rect(tex["torso_" + cp.team], Rect2(-10, -12, 20, 20), false, Color(0.85, 0.85, 0.85, a))
	draw_texture_rect(tex["head_" + cp.team], Rect2(-12, -30, 26, 26), false, Color(0.85, 0.85, 0.85, a))''', '''	var lk: Dictionary = cp.look if not cp.look.is_empty() else default_look
	var tc: Color = TEAM_COL[maxi(0, TEAMS.find(cp.team))]
	var cc := Color(0.85, 0.85, 0.85, a)
	draw_texture_rect(tex[leg_tex(lk)], Rect2(-7, 2, 9, 17), false, Color(0.8, 0.8, 0.8, a))
	av_jet(lk, cc)
	av_torso(lk, tc, cc)
	draw_set_transform_matrix(wt * Transform2D(cp.rot, Vector2(cp.face, gsign()), 0.0, Vector2(cp.x, cp.y)) * Transform2D(0.0, Vector2.ONE, 0.0, Vector2(1, -18)))
	av_head(lk, tc, cc)''')

# ---------- draw the player with their look ----------
rep('''	draw_set_transform_matrix(body)
	if p.jet_on:
		var fl := 16.0 + sin(time_s * 38.0 + p.id) * 4.0 + sin(time_s * 21.0) * 2.0
		for nx in [-12.0, -6.0]:
			draw_texture_rect(tex.glow, Rect2(nx - 6, 9, 12, fl), false, Color(1, 0.62, 0.2, 0.95))
			draw_texture_rect(tex.glow, Rect2(nx - 3.5, 9, 7, fl * 0.6), false, Color(1, 0.95, 0.7, 1))
	draw_leg(body, Vector2(-3, 4), p.leg_b, p.shin_b, Color(0.78, 0.78, 0.78) * tint)
	draw_set_transform_matrix(body)
	draw_texture_rect(tex.jetpack, Rect2(-16, -12, 12, 20), false, tint)''', '''	draw_set_transform_matrix(body)
	var lk := plook(p)
	av_back(lk, tint)
	var fcol = AV_FLAME.get(lk.fl)
	if p.jet_on and fcol != null:
		var fl := 16.0 + sin(time_s * 38.0 + p.id) * 4.0 + sin(time_s * 21.0) * 2.0
		for nx in [-12.0, -6.0]:
			draw_texture_rect(tex.glow, Rect2(nx - 6, 9, 12, fl), false, fcol[0])
			draw_texture_rect(tex.glow, Rect2(nx - 3.5, 9, 7, fl * 0.6), false, fcol[1])
	draw_leg(body, Vector2(-3, 4), p.leg_b, p.shin_b, Color(0.78, 0.78, 0.78) * tint, leg_tex(lk))
	draw_set_transform_matrix(body)
	av_jet(lk, tint)''')
rep('''	var sleeve: Color = p.color.darkened(0.2)''', '''	var sleeve: Color = sleeve_col(p.color, lk).darkened(0.2)''')
rep('''	draw_texture_rect(tex["torso_" + p.team], Rect2(-10, -13, 20, 20), false, tint)
	draw_leg(body, Vector2(3, 4), p.leg_f, p.shin_f, tint)''', '''	av_torso(lk, p.color, tint)
	draw_leg(body, Vector2(3, 4), p.leg_f, p.shin_f, tint, leg_tex(lk))''')
rep('''	draw_texture_rect(tex["head_" + p.team], Rect2(-13, -14, 26, 26), false, tint)''', '''	av_head(lk, p.color, tint)''')
rep('''	draw_line(sh_pt + Vector2(3, 0), fh, p.color * tint, 4.0, true)''', '''	draw_line(sh_pt + Vector2(3, 0), fh, sleeve_col(p.color, lk) * tint, 4.0, true)''')
rep('''	if p.protect_t > 0:
		draw_arc(Vector2(0, -4), 30, 0, TAU, 40''', '''	av_front(lk, tint)
	if p.protect_t > 0:
		draw_arc(Vector2(0, -4), 30, 0, TAU, 40''')
rep('''func draw_leg(base: Transform2D, hip: Vector2, ang: float, shin: float, col: Color) -> void:
	draw_set_transform_matrix(base * Transform2D(ang, Vector2.ONE, 0.0, hip))
	draw_texture_rect_region(tex.leg, Rect2(-4.5, -1, 9, 9.5), Rect2(0, 0, 27, 28.5), col)
	var knee := hip + Vector2(-sin(ang), cos(ang)) * 7.8
	draw_set_transform_matrix(base * Transform2D(shin, Vector2.ONE, 0.0, knee))
	draw_texture_rect_region(tex.leg, Rect2(-4.5, -0.8, 9, 9), Rect2(0, 24, 27, 27), col)''', '''func draw_leg(base: Transform2D, hip: Vector2, ang: float, shin: float, col: Color, tn := "leg") -> void:
	draw_set_transform_matrix(base * Transform2D(ang, Vector2.ONE, 0.0, hip))
	draw_texture_rect_region(tex[tn], Rect2(-4.5, -1, 9, 9.5), Rect2(0, 0, 27, 28.5), col)
	var knee := hip + Vector2(-sin(ang), cos(ang)) * 7.8
	draw_set_transform_matrix(base * Transform2D(shin, Vector2.ONE, 0.0, knee))
	draw_texture_rect_region(tex[tn], Rect2(-4.5, -0.8, 9, 9), Rect2(0, 24, 27, 27), col)''')

# ---------- panel transform is remembered so avatars can be drawn inside panels ----------
rep('''	draw_set_transform_matrix(Transform2D(0.0, Vector2(sc, sc), 0.0, cpos - r.get_center() * sc))
	ga = ease_out(ui_t / 0.2)''', '''	panel_xf = Transform2D(0.0, Vector2(sc, sc), 0.0, cpos - r.get_center() * sc)
	draw_set_transform_matrix(panel_xf)
	ga = ease_out(ui_t / 0.2)''')
rep('''	draw_set_transform_matrix(Transform2D.IDENTITY)
	ui_btns.clear()''', '''	draw_set_transform_matrix(Transform2D.IDENTITY)
	panel_xf = Transform2D.IDENTITY
	ui_btns.clear()''')

# ---------- screens ----------
rep('''			"lan_cfg":
				draw_cfg("MATCH SETTINGS", LAN_ROWS, "lobby_back")''', '''			"lan_cfg":
				draw_cfg("MATCH SETTINGS", LAN_ROWS, "lobby_back")
			"locker":
				draw_locker()
			"namekey":
				draw_namekey()''')
rep('''	ui_button("MATCH SETTINGS", Rect2(x, y + 204 * u, bw, bh), "match")
	ui_button("CONTROLS", Rect2(x, y + 256 * u, bw, bh), "controls")''', '''	ui_button("LOCKER", Rect2(x, y + 204 * u, bw, bh), "locker")
	var hw := (bw - 8 * u) / 2.0
	ui_button("MATCH", Rect2(x, y + 256 * u, hw, bh), "match")
	ui_button("CONTROLS", Rect2(x + hw + 8 * u, y + 256 * u, hw, bh), "controls")
	var ak := ease_back((ui_t - 0.3) / 0.45)
	var ga2 := ga
	ga *= clampf((ui_t - 0.3) / 0.2, 0.0, 1.0) if not anim_skip else 1.0
	var apos := Vector2(r.end.x - 62 * u, y + 58 * u + sin(time_s * 2.0) * 3 * u)
	draw_avatar(my_look(), apos, 1.15 * u * maxf(0.05, ak), TEAM_COL[0])
	txt(my_name(), Vector2(r.end.x - 62 * u, y + 108 * u), 11 * u, C_ARC, 1, 3 * u)
	ga = ga2''')
rep('''	ui_button("NAME: " + my_name(), Rect2(x, y + 188 * u, bw, bh), "name")''', '''	ui_button("NAME & LOOK: " + my_name(), Rect2(x, y + 188 * u, bw, bh), "name")''')

# actions
rep('''			if a.begins_with("row:") or a.begins_with("key:"):''', '''			if a.begins_with("row:") or a.begins_with("key:") or a.begins_with("lk_") or a.begins_with("nk:"):''')
rep('''		"name":
			var i0 := FUN_NAMES.find(my_name())
			cfg.name = FUN_NAMES[(i0 + 1) % FUN_NAMES.size()]
			save_cfg()''', '''		"name":
			lk_back = "lan"
			lk_page = 0
			state = "locker"
		"locker":
			lk_back = "menu"
			lk_page = 0
			state = "locker"
		"lk_done":
			state = lk_back
		"lk_name":
			name_entry = my_name()
			state = "namekey"
		"lk_dice":
			var pool := FUN_NAMES.duplicate()
			pool.erase(name_entry if state == "namekey" else my_name())
			var nn: String = pool[randi() % pool.size()]
			if state == "namekey":
				name_entry = nn
			else:
				cfg.name = nn
				save_cfg()
		"lk_rand":
			cfg.look = look_str(random_look())
			save_cfg()
		"name_ok":
			var nm := name_entry.strip_edges()
			if nm != "":
				cfg.name = nm
				save_cfg()
			state = "locker"
		"name_back":
			state = "locker"''')
rep('''			if a.begins_with("conn:"):
				join_game(a.substr(5))''', '''			if a.begins_with("conn:"):
				join_game(a.substr(5))
			elif a.begins_with("lk_tab:"):
				lk_tab = a.substr(7)
				lk_page = 0
			elif a.begins_with("lk_page:"):
				lk_page += int(a.substr(8))
			elif a.begins_with("lk_pick:"):
				var bits := a.substr(8).split(":")
				if bits[0] == "sets":
					cfg.look = bits[1]
				else:
					var lk := my_look()
					lk[bits[0]] = bits[1]
					cfg.look = look_str(lk)
				save_cfg()
			elif a.begins_with("nk:"):
				name_key(a.substr(3))''')

# back button / keyboard typing for names
rep('''		"lan_cfg":
			do_action("lobby_back")
		"menu":''', '''		"lan_cfg":
			do_action("lobby_back")
		"locker":
			state = lk_back
		"namekey":
			state = "locker"
		"menu":''')
rep('''			if ch != "" and "0123456789.".contains(ch):
				do_action("key:" + ch)
				return''', '''			if ch != "" and "0123456789.".contains(ch):
				do_action("key:" + ch)
				return
		if state == "namekey":
			var ch2 := char(event.unicode) if event.unicode > 0 else ""
			if event.keycode == KEY_BACKSPACE:
				name_key("DEL")
				return
			if event.keycode == KEY_ENTER or event.keycode == KEY_KP_ENTER:
				do_action("name_ok")
				return
			if ch2 != "" and event.keycode != KEY_ESCAPE:
				name_key(ch2, true)
				return''')

# ---------- new code ----------
s += '''
# ================= AVATARS (v1.1) =================
var default_look := {}
var panel_xf := Transform2D.IDENTITY
var lk_tab := "sets"
var lk_page := 0
var lk_back := "menu"
var name_entry := ""

func parse_look(sv) -> Dictionary:
	var parts := str(sv).split(".")
	var d0 := AV_DEF.split(".")
	var out := {}
	for i in AV_KEYS.size():
		var k: String = AV_KEYS[i]
		var v: String = parts[i] if i < parts.size() else d0[i]
		var ok := false
		for it in AV_LIST[k]:
			if it[0] == v:
				ok = true
				break
		out[k] = v if ok else d0[i]
	return out

func look_str(lk: Dictionary) -> String:
	var a := PackedStringArray()
	for k in AV_KEYS:
		a.append(str(lk.get(k, "")))
	return ".".join(a)

func my_look() -> Dictionary:
	return parse_look(cfg.look if str(cfg.look) != "" else AV_DEF)

func plook(p) -> Dictionary:
	return p.look if not p.look.is_empty() else default_look

# bots: mostly one of the full looks, sometimes a wild mix
func random_look() -> Dictionary:
	if randf() < 0.6:
		return parse_look(AV_SETS[randi() % AV_SETS.size()][2])
	var out := {}
	for k in AV_KEYS:
		var arr: Array = AV_LIST[k]
		out[k] = arr[randi() % arr.size()][0]
	if out.fl == "none":
		out.fl = "orange"
	return out

func leg_tex(lk: Dictionary) -> String:
	return "leg" if lk.get("o", "army") == "army" else "leg_" + lk.o

# team games keep team-coloured sleeves so sides stay easy to tell apart
func sleeve_col(team_col: Color, lk: Dictionary) -> Color:
	if lk.get("o", "army") == "army" or cfg.mode == "team":
		return team_col
	return AV_SLEEVE.get(lk.o, team_col)

func av(nm: String, anchor: Vector2, sc: float, off: Vector2, col := Color.WHITE) -> void:
	var r = AV_RECT.get(nm)
	if r == null:
		return
	draw_texture_rect(tex["av_" + nm], Rect2((Vector2(r[0], r[1]) - anchor) * sc + off, Vector2(r[2], r[3]) * sc), false, col)

func av_back(lk: Dictionary, tint: Color) -> void:
	if AV_BACK.has(lk.x):
		av("x_" + lk.x, AV_BODY_A, 1.1, Vector2(0, -3), tint)

func av_jet(lk: Dictionary, tint: Color) -> void:
	av("j_" + lk.j, AV_BODY_A, 1.1, Vector2(-3.5, -3), tint)

func av_torso(lk: Dictionary, team_col: Color, tint: Color) -> void:
	if lk.o == "army":
		av("o_army_shirt", AV_BODY_A, 1.1, Vector2(0, -3), team_col * tint)
		av("o_army", AV_BODY_A, 1.1, Vector2(0, -3), tint)
	else:
		av("o_" + lk.o, AV_BODY_A, 1.1, Vector2(0, -3), tint)
	if lk.x != "none" and not AV_BACK.has(lk.x) and not AV_FRONT.has(lk.x):
		av("x_" + lk.x, AV_BODY_A, 1.1, Vector2(0, -3), tint)

func av_head(lk: Dictionary, team_col: Color, tint: Color) -> void:
	av("face", AV_HEAD_A, 1.05, Vector2.ZERO, tint)
	if not AV_FULL.has(lk.h):
		av("f_" + lk.f, AV_HEAD_A, 1.05, Vector2.ZERO, tint)
	av("h_" + lk.h, AV_HEAD_A, 1.05, Vector2.ZERO, team_col * tint if lk.h == "classic" else tint)

func av_front(lk: Dictionary, tint: Color) -> void:
	if AV_FRONT.has(lk.x):
		av("x_" + lk.x, AV_BODY_A, 1.1, Vector2(0, -3 + sin(time_s * 3.0) * 1.5), tint)

# a standing/flying soldier for menus; pos is the body centre on screen
func draw_avatar(lk: Dictionary, pos: Vector2, sc: float, col: Color, fly := true, gun := "ak47") -> void:
	var a := Color(1, 1, 1, ga)
	var body := panel_xf * Transform2D(0.0, Vector2(sc, sc), 0.0, pos)
	draw_set_transform_matrix(body)
	av_back(lk, a)
	var fc = AV_FLAME.get(lk.fl)
	if fly and fc != null:
		var fl := 15.0 + sin(time_s * 38.0) * 3.0 + sin(time_s * 21.0) * 1.5
		for nx in [-12.0, -6.0]:
			draw_texture_rect(tex.glow, Rect2(nx - 6, 9, 12, fl), false, Color(fc[0], fc[0].a * ga))
			draw_texture_rect(tex.glow, Rect2(nx - 3.5, 9, 7, fl * 0.6), false, Color(fc[1], ga))
	draw_leg(body, Vector2(-3, 4), 0.3, 0.15, Color(0.78, 0.78, 0.78, ga), leg_tex(lk))
	draw_set_transform_matrix(body)
	av_jet(lk, a)
	var sl := sleeve_col(col, lk)
	var sh_pt := Vector2(1, -6)
	var grip := sh_pt + Vector2(7, 1)
	draw_line(sh_pt + Vector2(-2, 0), grip, Color(C_OUT, ga), 6.0, true)
	draw_line(sh_pt + Vector2(-2, 0), grip, Color(sl.darkened(0.2), ga), 4.0, true)
	av_torso(lk, col, a)
	draw_leg(body, Vector2(3, 4), -0.2, 0.05, a, leg_tex(lk))
	draw_set_transform_matrix(body * Transform2D(0.0, Vector2.ONE, 0.0, Vector2(1, -15)))
	av_head(lk, col, a)
	var m: Dictionary = META.GUN[gun]
	var gd: float = S.gun_draw
	draw_set_transform_matrix(body * Transform2D(0.0, Vector2.ONE, 0.0, grip))
	draw_texture_rect(tex["gun_" + gun], Rect2(-m.grip[0] * gd, -m.grip[1] * gd, m.size[0] * gd, m.size[1] * gd), false, a)
	draw_set_transform_matrix(body)
	var fh := grip + Vector2(m.front[0] - m.grip[0], m.front[1] - m.grip[1]) * gd
	draw_line(sh_pt + Vector2(3, 0), fh, Color(C_OUT, ga), 6.0, true)
	draw_line(sh_pt + Vector2(3, 0), fh, Color(sl, ga), 4.0, true)
	draw_texture_rect(tex.hand, Rect2(fh - Vector2(3, 3), Vector2(6, 6)), false, a)
	draw_texture_rect(tex.hand, Rect2(grip - Vector2(3, 3), Vector2(6, 6)), false, a)
	av_front(lk, a)
	draw_set_transform_matrix(panel_xf)

func head_icon(lk: Dictionary, pos: Vector2, sc: float, col: Color) -> void:
	draw_set_transform_matrix(panel_xf * Transform2D(0.0, Vector2(sc, sc), 0.0, pos))
	av_head(lk, col, Color(1, 1, 1, ga))
	draw_set_transform_matrix(panel_xf)

func lk_items(tab: String) -> Array:
	if tab == "sets":
		var out := []
		for st in AV_SETS:
			out.append([st[2], st[1]])
		return out
	return AV_LIST[tab]

# a flat tap target that does not slide in (used for many small keys / tiles)
func flat_btn(r: Rect2, action: String, on := false) -> Rect2:
	ui_btns.append({"r": r, "a": action})
	var rr := r
	if r == pressed_r and time_s - pressed_at < 0.18:
		rr = rr.grow(-3 * u)
	elif not touch_mode and mouse_used and r.has_point(mouse_pos):
		rr.position.y -= 2 * u
	return rr

func draw_dice(c: Vector2, sz: float) -> void:
	fbox(Rect2(c - Vector2(sz, sz) / 2, Vector2(sz, sz)), Color("#f4f6ff"), sz * 0.22, C_OUT, maxf(1.0, sz * 0.06))
	for d in [Vector2(-0.24, -0.24), Vector2(0.24, 0.24), Vector2(0, 0), Vector2(0.24, -0.24), Vector2(-0.24, 0.24)]:
		circ(c + d * sz, sz * 0.09, C_OUT)

func draw_locker() -> void:
	var w := minf(sw - 24 * u, 800 * u)
	var h := minf(sh - 20 * u, 390 * u)
	var r := panel(w, h)
	var x := r.position.x + 22 * u
	var y := r.position.y
	var lk := my_look()
	txh("LOCKER", Vector2(x, y + 38 * u), 24 * u, C_ARC, 0, 4 * u)
	txt("Mix any parts you like. Saved on this phone.", Vector2(r.end.x - 22 * u, y + 34 * u), 10 * u, C_MUTED, 2)
	# left: name and a big preview
	var lw := 206 * u
	var nr := flat_btn(Rect2(x, y + 50 * u, lw - 46 * u, 38 * u), "lk_name")
	fbox(nr, Color(0.02, 0.03, 0.08, 0.9), 9 * u, Color(1, 1, 1, 0.16), maxf(1.0, u))
	txt("NAME", nr.position + Vector2(10 * u, 13 * u), 8 * u, C_CYAN)
	txh(my_name(), nr.position + Vector2(10 * u, 31 * u), 15 * u, C_INK)
	txt("EDIT", Vector2(nr.end.x - 8 * u, nr.position.y + 24 * u), 9 * u, C_ARC, 2)
	var dr := flat_btn(Rect2(x + lw - 40 * u, y + 50 * u, 40 * u, 38 * u), "lk_dice")
	fbox(dr, Color(0.2, 0.25, 0.43), 9 * u, Color(1, 1, 1, 0.13), maxf(1.0, u))
	draw_dice(dr.get_center(), 20 * u)
	var stage := Rect2(x, y + 96 * u, lw, r.end.y - 66 * u - (y + 96 * u))
	fbox(stage, Color(0.13, 0.17, 0.34, 0.9), 14 * u, Color(1, 1, 1, 0.08), maxf(1.0, u))
	fbox(Rect2(stage.position + Vector2(20 * u, stage.size.y - 30 * u), Vector2(stage.size.x - 40 * u, 12 * u)), Color(0, 0, 0, 0.25), 6 * u)
	var sc := minf(stage.size.y / 74.0, stage.size.x / 72.0)
	draw_avatar(lk, stage.get_center() + Vector2(-4 * sc, 4 * sc + sin(time_s * 2.0) * 3 * u), sc, TEAM_COL[0])
	ui_button("SURPRISE ME", Rect2(x, r.end.y - 56 * u, lw, 42 * u), "lk_rand")
	# right: tabs and options
	var rx := x + lw + 18 * u
	var aw := r.end.x - 22 * u - rx
	var tw := (aw - 6 * 5 * u) / 7.0
	for i in LK_TABS.size():
		var tb: Array = LK_TABS[i]
		var on: bool = lk_tab == tb[0]
		var tr := flat_btn(Rect2(rx + i * (tw + 5 * u), y + 50 * u, tw, 34 * u), "lk_tab:" + tb[0])
		fbox(tr, C_ARC if on else Color(0.17, 0.21, 0.38, 0.95), 8 * u, Color(1, 1, 1, 0.12), maxf(1.0, u))
		txh(tb[1], tr.get_center() + Vector2(0, 4 * u), 10 * u, Color("#2a1f00") if on else C_INK, 1)
	var items := lk_items(lk_tab)
	var gy := y + 94 * u
	var gh := r.end.y - 66 * u - gy
	var cols := maxi(3, int(aw / (84 * u)))
	var rows := maxi(1, int(gh / (102 * u)))
	var gap := 7 * u
	var cw := (aw - (cols - 1) * gap) / cols
	var chh := (gh - (rows - 1) * gap) / rows
	var per := cols * rows
	var pages := maxi(1, ceili(items.size() / float(per)))
	lk_page = clampi(lk_page, 0, pages - 1)
	var cur_s := look_str(lk)
	for j in range(lk_page * per, mini(items.size(), (lk_page + 1) * per)):
		var it: Array = items[j]
		var k := j - lk_page * per
		var tr := Rect2(rx + (k % cols) * (cw + gap), gy + (k / cols) * (chh + gap), cw, chh)
		var tl: Dictionary
		var sel: bool
		if lk_tab == "sets":
			tl = parse_look(it[0])
			sel = cur_s == look_str(tl)
		else:
			tl = lk.duplicate()
			tl[lk_tab] = it[0]
			sel = lk[lk_tab] == it[0]
		var ga0 := ga
		ga *= clampf((ui_t - 0.1 - k * 0.025) / 0.2, 0.0, 1.0) if not anim_skip else 1.0
		var rr := flat_btn(tr, "lk_pick:%s:%s" % [lk_tab, it[0]])
		fbox(rr, Color(0.3, 0.25, 0.09, 0.95) if sel else Color(0.11, 0.14, 0.29, 0.95), 10 * u, C_ARC if sel else Color(1, 1, 1, 0.1), (2.0 if sel else 1.0) * maxf(1.0, u))
		var s2 := minf((chh - 22 * u) / 70.0, cw / 66.0)
		draw_avatar(tl, Vector2(rr.get_center().x - 4 * s2, rr.position.y + (chh - 20 * u) / 2.0 + 5 * s2), s2, TEAM_COL[0])
		var lab: String = it[1]
		txt(lab, Vector2(rr.get_center().x, rr.end.y - 7 * u), (8.5 if lab.length() > 13 else 9.5) * u, C_ARC if sel else C_INK, 1, 2 * u)
		ga = ga0
	if pages > 1:
		var py := r.end.y - 54 * u
		var pr := flat_btn(Rect2(r.end.x - 22 * u - 150 * u, py, 44 * u, 38 * u), "lk_page:-1")
		fbox(pr, Color(0.2, 0.25, 0.43, 1.0 if lk_page > 0 else 0.4), 9 * u)
		txh("<", pr.get_center() + Vector2(0, 6 * u), 18 * u, C_INK, 1)
		txt("%d / %d" % [lk_page + 1, pages], Vector2(r.end.x - 22 * u - 75 * u, py + 25 * u), 12 * u, C_MUTED, 1)
		var nx := flat_btn(Rect2(r.end.x - 22 * u - 44 * u, py, 44 * u, 38 * u), "lk_page:1")
		fbox(nx, Color(0.2, 0.25, 0.43, 1.0 if lk_page < pages - 1 else 0.4), 9 * u)
		txh(">", nx.get_center() + Vector2(0, 6 * u), 18 * u, C_INK, 1)
	ui_button("DONE", Rect2(rx, r.end.y - 56 * u, 170 * u, 42 * u), "lk_done", true)

func name_key(k: String, raw := false) -> void:
	if k == "DEL":
		name_entry = name_entry.substr(0, maxi(0, name_entry.length() - 1))
		return
	if k == "SPACE":
		k = " "
	if name_entry.length() >= 12:
		return
	if k == " " and (name_entry == "" or name_entry.ends_with(" ")):
		return
	if not raw:
		k = k.to_upper() if (name_entry == "" or name_entry.ends_with(" ")) else k.to_lower()
	var ok := "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 _-"
	if ok.contains(k):
		name_entry += k

func draw_namekey() -> void:
	var w := minf(sw - 24 * u, 720 * u)
	var h := minf(sh - 20 * u, 370 * u)
	var r := panel(w, h)
	var x := r.position.x + 22 * u
	var y := r.position.y
	var iw := w - 44 * u
	txh("YOUR NAME", Vector2(x, y + 38 * u), 24 * u, C_ARC, 0, 4 * u)
	txt("Up to 12 letters. Everyone sees it over your head.", Vector2(r.end.x - 22 * u, y + 34 * u), 10 * u, C_MUTED, 2)
	var fr := Rect2(x, y + 50 * u, iw - 220 * u, 44 * u)
	fbox(fr, Color(0.02, 0.03, 0.08, 0.9), 9 * u, Color(C_ARC, 0.5), maxf(1.0, 1.5 * u))
	var caret := "|" if fmod(time_s, 1.0) < 0.5 else ""
	txh(name_entry + caret, fr.position + Vector2(14 * u, 31 * u), 22 * u, C_INK)
	txt("%d/12" % name_entry.length(), Vector2(fr.end.x - 10 * u, fr.position.y + 28 * u), 10 * u, C_MUTED, 2)
	var dr := flat_btn(Rect2(fr.end.x + 8 * u, fr.position.y, 44 * u, 44 * u), "lk_dice")
	fbox(dr, Color(0.2, 0.25, 0.43), 9 * u, Color(1, 1, 1, 0.13), maxf(1.0, u))
	draw_dice(dr.get_center(), 22 * u)
	ui_button("SAVE", Rect2(dr.end.x + 8 * u, fr.position.y, r.end.x - 22 * u - dr.end.x - 8 * u, 44 * u), "name_ok", true)
	var ky := y + 104 * u
	var gap := 5 * u
	var kw := (iw - 9 * gap) / 10.0
	var kh := minf(44 * u, (r.end.y - 16 * u - ky - 4 * gap) / 5.0)
	for ri in KB_ROWS.size():
		var row: String = KB_ROWS[ri]
		var x0 := x + (iw - (row.length() * kw + (row.length() - 1) * gap)) / 2.0
		for ci in row.length():
			var kr := flat_btn(Rect2(x0 + ci * (kw + gap), ky + ri * (kh + gap), kw, kh), "nk:" + row[ci])
			fbox(kr, Color(0.17, 0.21, 0.38, 0.95), 8 * u, Color(1, 1, 1, 0.12), maxf(1.0, u))
			txh(row[ci], kr.get_center() + Vector2(0, 6 * u), 16 * u, C_INK, 1)
	var by := ky + 4 * (kh + gap)
	var sp := flat_btn(Rect2(x + kw + gap, by, 6 * kw + 5 * gap, kh), "nk:SPACE")
	fbox(sp, Color(0.17, 0.21, 0.38, 0.95), 8 * u, Color(1, 1, 1, 0.12), maxf(1.0, u))
	txh("SPACE", sp.get_center() + Vector2(0, 5 * u), 12 * u, C_MUTED, 1)
	var dl := flat_btn(Rect2(x + 7 * (kw + gap), by, 2 * kw + gap, kh), "nk:DEL")
	fbox(dl, Color(0.35, 0.14, 0.2, 0.95), 8 * u, Color(1, 1, 1, 0.12), maxf(1.0, u))
	txh("DELETE", dl.get_center() + Vector2(0, 5 * u), 12 * u, C_INK, 1)
	var bk := flat_btn(Rect2(x + 9 * (kw + gap), by, kw, kh), "name_back")
	fbox(bk, Color(0.17, 0.21, 0.38, 0.95), 8 * u, Color(1, 1, 1, 0.12), maxf(1.0, u))
	txh("X", bk.get_center() + Vector2(0, 6 * u), 15 * u, C_MUTED, 1)
'''
open(P, "w").write(s)
print("ok")
# (applied by hand after the patch: "ui" screenshot trigger in shots_tick)
