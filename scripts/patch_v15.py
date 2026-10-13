"""v1.5: pick your team in the lobby (Blue / Red, like Mini Militia); host or room leader can shuffle;
bots fill the smaller team; vs-bots games get a 'Your team' setting."""
import sys
P = "/home/claude/skysquad/main.gd"
s = open(P).read()
def rep(a, b, c=1):
    global s
    if s.count(a) != c: sys.exit("expected %d got %d: %r" % (c, s.count(a), a[:120]))
    s = s.replace(a, b)

rep('# Sky Squad - Arc Light Studio. Playtest build 1.4', '# Sky Squad - Arc Light Studio. Playtest build 1.5')
rep('const VERSION := "1.4"', 'const VERSION := "1.5"')
rep('"server": "", "uid": "",', '"server": "", "uid": "", "my_side": 0,')
rep('''	["mode", "Game mode", ["ffa", "team"], ["Free for all", "Teams"]],
	["bots", "Bots"''', '''	["mode", "Game mode", ["ffa", "team"], ["Free for all", "Teams"]],
	["my_side", "Your team (Teams)", [0, 1], ["Blue", "Red"]],
	["bots", "Bots"''')

# ---------- match setup: sides from the lobby, bots balance ----------
rep('''	var humans: Array = [{"peer": 1, "name": my_name(), "look": look_str(my_look())}]''', '''	var humans: Array = [{"peer": 1, "name": my_name(), "look": look_str(my_look()), "side": int(cfg.my_side)}]''')
rep('''		p.side = i
		if cfg.mode == "team":
			p.side = i % 2
			if i > 0 or net_role == "host":
				p.team = "blue" if p.side == 0 else "red"
				p.color = TEAM_COL[1] if p.side == 0 else TEAM_COL[2]
		p.prev = p.inp.duplicate()
		players.append(p)''', '''		p.side = i
		p.prev = p.inp.duplicate()
		players.append(p)
	if cfg.mode == "team":
		var sides := []
		for hm in humans:
			sides.append(int(hm.get("side", -1)))
		var plan := team_plan(sides, nbots)
		for i in players.size():
			var tp: Player = players[i]
			tp.side = plan[i]
			tp.team = "blue" if tp.side == 0 else "red"
			tp.color = TEAM_COL[1] if tp.side == 0 else TEAM_COL[2]''')

# ---------- lobby info carries each player's pick ----------
rep('''"pl": lobby_names(), "lk": lobby_looks(), "mode": cfg.mode,''', '''"pl": lobby_names(), "lk": lobby_looks(), "sd": lobby_sides(), "ud": lobby_uids(), "mode": cfg.mode,''')

# ---------- lobby screen ----------
rep('''	var names := lobby_names()
	txt("PLAYERS", Vector2(x, y + 74 * u), 10 * u, C_CYAN)
	for i in names.size():''', '''	var names := lobby_names()
	var lmode: String = cfg.mode if host else str(lobby_info.get("mode", "ffa"))
	if lmode == "team":
		draw_team_columns(x, y, names, host)
	else:
		txt("PLAYERS", Vector2(x, y + 74 * u), 10 * u, C_CYAN)
	for i in (names.size() if lmode != "team" else 0):''')
rep('''	var nb: int = clampi(int(cfg.lan_bots), 0, 6 - names.size()) if host else int(lobby_info.get("bots", 0))
	if nb > 0:''', '''	var nb: int = clampi(int(cfg.lan_bots), 0, 6 - names.size()) if host else int(lobby_info.get("bots", 0))
	if nb > 0 and lmode != "team":''')
rep('''		ui_button("START", Rect2(rx, y + 190 * u, bw * 2 + 10 * u, 48 * u), "start", true)
		ui_button("SETTINGS", Rect2(rx, y + 246 * u, bw, 42 * u), "lan_cfg")
		ui_button("LEAVE", Rect2(rx + bw + 10 * u, y + 246 * u, bw, 42 * u), "leave")''', '''		ui_button("START", Rect2(rx, y + 190 * u, bw * 2 + 10 * u, 48 * u), "start", true)
		lobby_row(rx, y + 246 * u, bw * 2 + 10 * u, lmode == "team")''')
rep('''		ui_button("START", Rect2(rx, y + 190 * u, bw2 * 2 + 10 * u, 48 * u), "o_start", true)
		ui_button("SETTINGS", Rect2(rx, y + 246 * u, bw2, 42 * u), "lan_cfg")
		ui_button("LEAVE", Rect2(rx + bw2 + 10 * u, y + 246 * u, bw2, 42 * u), "leave")''', '''		ui_button("START", Rect2(rx, y + 190 * u, bw2 * 2 + 10 * u, 48 * u), "o_start", true)
		lobby_row(rx, y + 246 * u, bw2 * 2 + 10 * u, lmode == "team")''')

# ---------- actions ----------
rep('''			if a.begins_with("row:") or a.begins_with("key:") or a.begins_with("lk_") or a.begins_with("nk:"):''', '''			if a.begins_with("row:") or a.begins_with("key:") or a.begins_with("lk_") or a.begins_with("nk:") or a.begins_with("team"):''')
rep('''			elif a.begins_with("lk_tab:"):''', '''			elif a.begins_with("team:"):
				pick_team(int(a.substr(5)))
			elif a == "team_shuffle":
				pick_team(-2)
			elif a.begins_with("lk_tab:"):''')

s += '''
# ================= TEAM PICKING (v1.5) =================
# sides people picked (-1 = no pick yet) -> final side for every human, then for every bot.
# Players without a pick and the bots go to the smaller team.
func team_plan(sides: Array, nbots: int) -> Array:
	var out := []
	var cnt := [0, 0]
	for sd in sides:
		var v := int(sd)
		if v == 0 or v == 1:
			cnt[v] += 1
	for sd in sides:
		var v := int(sd)
		if v != 0 and v != 1:
			v = 0 if cnt[0] <= cnt[1] else 1
			cnt[v] += 1
		out.append(v)
	for i in nbots:
		var v := 0 if cnt[0] <= cnt[1] else 1
		cnt[v] += 1
		out.append(v)
	return out

func lobby_sides() -> Array:
	if net_role == "host":
		var out := []
		for lp in lan_players:
			out.append(int(lp.get("side", -1)))
		return out
	return lobby_info.get("sd", [])

func lobby_uids() -> Array:
	if net_role == "host":
		var out := []
		for lp in lan_players:
			out.append(str(lp.get("uid", "")))
		return out
	return lobby_info.get("ud", [])

func my_lobby_index() -> int:
	return lobby_uids().find(str(cfg.uid))

func shuffle_teams() -> void:
	var idx := range(lan_players.size())
	idx.shuffle()
	for k in idx.size():
		lan_players[idx[k]].side = k % 2

# tap JOIN BLUE / JOIN RED / SHUFFLE
func pick_team(side: int) -> void:
	if net_role == "host" and not dedicated:
		if side == -2:
			shuffle_teams()
		elif not lan_players.is_empty():
			lan_players[0].side = side
		send_lobby()
	elif net_role == "client":
		rpc_id(1, "c_team", side)

@rpc("any_peer", "call_remote", "reliable")
func c_team(side) -> void:
	if net_role != "host" or not ["lobby", "lan_cfg", "over"].has(state):
		return
	var id := multiplayer.get_remote_sender_id()
	var sd := int(side)
	if sd == -2:
		if sender_is_owner():
			shuffle_teams()
	elif sd == 0 or sd == 1:
		for lp in lan_players:
			if int(lp.peer) == id:
				lp.side = sd
	send_lobby()

func draw_team_columns(x: float, y: float, names: Array, host: bool) -> void:
	var sides := lobby_sides()
	var lks := lobby_looks()
	var picks := []
	for i in names.size():
		picks.append(int(sides[i]) if i < sides.size() else -1)
	var nb: int = clampi(int(cfg.lan_bots), 0, 6 - names.size()) if host else int(lobby_info.get("bots", 0))
	var plan := team_plan(picks, nb)
	var mine := my_lobby_index()
	var colw := 116 * u
	var heads := [["BLUE", TEAM_COL[1]], ["RED", TEAM_COL[2]]]
	for side in 2:
		var cx := x + side * (colw + 8 * u)
		fbox(Rect2(cx - 6 * u, y + 60 * u, colw, 172 * u), Color(heads[side][1], 0.1), 10 * u, Color(heads[side][1], 0.5), maxf(1.0, u))
		txh(heads[side][0], Vector2(cx + 4 * u, y + 80 * u), 13 * u, heads[side][1])
		var row := 0
		for i in names.size():
			if plan[i] != side:
				continue
			var yy := y + 104 * u + row * 21 * u
			head_icon(parse_look(lks[i]) if i < lks.size() else default_look, Vector2(cx + 8 * u, yy - 5 * u), 0.55 * u, heads[side][1])
			var nm := str(names[i])
			if nm.length() > 10:
				nm = nm.substr(0, 9) + "."
			txt(nm + (" (you)" if i == mine else ""), Vector2(cx + 20 * u, yy), 12 * u, C_ARC if i == mine else (C_INK if picks[i] >= 0 else C_MUTED))
			row += 1
		var bots := 0
		for j in range(names.size(), plan.size()):
			if plan[j] == side:
				bots += 1
		if bots > 0:
			txt("+ %d bot%s" % [bots, "s" if bots > 1 else ""], Vector2(cx + 20 * u, y + 104 * u + row * 21 * u), 11 * u, C_MUTED)
		var my_side := plan[mine] if mine >= 0 and mine < plan.size() else -1
		var br := flat_btn(Rect2(cx - 6 * u, y + 240 * u, colw, 40 * u), "team:%d" % side)
		var on: bool = my_side == side and mine >= 0 and picks[mine] == side
		fbox(br, heads[side][1] if on else Color(heads[side][1], 0.35), 10 * u, Color(1, 1, 1, 0.25 if on else 0.12), maxf(1.0, u))
		txh(("YOUR TEAM" if on else "JOIN " + heads[side][0]), br.get_center() + Vector2(0, 5 * u), 12 * u, Color.WHITE, 1)

# SETTINGS / (SHUFFLE) / LEAVE under the START button
func lobby_row(rx: float, ry: float, wtot: float, teams: bool) -> void:
	if teams:
		var bw := (wtot - 16 * u) / 3.0
		ui_button("SETTINGS", Rect2(rx, ry, bw, 42 * u), "lan_cfg")
		ui_button("SHUFFLE", Rect2(rx + bw + 8 * u, ry, bw, 42 * u), "team_shuffle")
		ui_button("LEAVE", Rect2(rx + 2 * (bw + 8 * u), ry, bw, 42 * u), "leave")
	else:
		var bw2 := (wtot - 10 * u) / 2.0
		ui_button("SETTINGS", Rect2(rx, ry, bw2, 42 * u), "lan_cfg")
		ui_button("LEAVE", Rect2(rx + bw2 + 10 * u, ry, bw2, 42 * u), "leave")
'''
open(P, "w").write(s)
print("ok")
