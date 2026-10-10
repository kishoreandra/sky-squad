"""v1.2: online rooms (room codes, a no-screen server per room), owner starts/sets the match, reconnect after a drop,
client-side prediction for your own movement, fake-lag test switch."""
import sys
P = "/home/claude/skysquad/main.gd"
s = open(P).read()

def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        sys.exit(f"expected {count} got {n}: {old[:140]!r}")
    s = s.replace(old, new)

rep('# Sky Squad - Arc Light Studio. Playtest build 1.1', '# Sky Squad - Arc Light Studio. Playtest build 1.2')
rep('const VERSION := "1.1"', 'const VERSION := "1.2"')
rep('"lan_cfg", "locker", "namekey"]', '"lan_cfg", "locker", "namekey", "online"]')
rep('"name": "", "lan_bots": 2, "look": "",', '"name": "", "lan_bots": 2, "look": "", "server": "", "uid": "",')
rep('\tvar actor := false\n\tvar look := {}\n', '\tvar actor := false\n\tvar look := {}\n\tvar uid := ""\n\tvar dropped := false\n\tvar svx := 0.0\n\tvar svy := 0.0\n\tvar pfuel := 0.0\n')

# ---------- start-up switches ----------
rep('''		if a.begins_with("--state="):''', '''		if a == "--dedicated":
			var dport := 25001
			var droom := "TEST"
			for a2 in args:
				if a2.begins_with("--port="):
					dport = int(a2.substr(7))
				if a2.begins_with("--room="):
					droom = a2.substr(7)
			dedicated_start(dport, droom)
		if a.begins_with("--lag="):
			lag_ms = int(a.substr(6))
		if a.begins_with("--server="):
			cfg.server = a.substr(9)
		if a.begins_with("--online-create"):
			lantest_time = 45.0
			Engine.max_fps = 60
			cfg.name = "Owner"
			lantest_join = "online"
			mm_query("new", a.substr(16) if a.length() > 16 else "TEST1")
		if a.begins_with("--online-join="):
			lantest_time = 45.0
			Engine.max_fps = 60
			cfg.name = "Friend"
			lantest_join = "online"
			mm_query("join", a.substr(14))
		if a == "--drop-test":
			drop_test = true
		if a.begins_with("--state="):''')

# every install gets its own id (used to put you back in your seat after a drop)
rep('''	default_look = parse_look(AV_DEF)''', '''	default_look = parse_look(AV_DEF)
	if str(cfg.uid) == "":
		cfg.uid = "%08x%08x" % [randi(), randi()]
		save_cfg()''')

# ---------- process loop: no-screen server ----------
rep('''	if shot_at >= 0:
		while state == "play" and t < shot_at:''', '''	if dedicated:
		dedicated_tick(delta, dt)
		return
	if shot_at >= 0:
		while state == "play" and t < shot_at:''')
rep('''	if state == "play" and not players.is_empty() and players[my_idx].alive:
		want_view = S.view_h * ZOOM_MULT[zoom_level(players[my_idx])]''', '''	if state == "play" and my_idx < players.size() and players[my_idx].alive:
		want_view = S.view_h * ZOOM_MULT[zoom_level(players[my_idx])]''')
rep('''	human_input()
	pick_request = ""
	zoom_request = false
	for p in players:
		if p.bot:
			bot_think(p, dt)''', '''	if not dedicated:
		human_input()
	pick_request = ""
	zoom_request = false
	for p in players:
		if p.bot:
			bot_think(p, dt)''')
rep('''func _draw() -> void:
	draw_set_transform_matrix(Transform2D.IDENTITY)''', '''func _draw() -> void:
	if dedicated:
		return
	draw_set_transform_matrix(Transform2D.IDENTITY)''')
rep('''	my_idx = 0
	for p in players:
		spawn(p)''', '''	my_idx = 99 if dedicated else 0
	for i in players.size():
		if i < humans.size():
			players[i].uid = str(humans[i].get("uid", ""))
	for p in players:
		spawn(p)''')
rep('''	lan_players[0].name = my_name()
	lan_players[0].look = look_str(my_look())
	reset_match()''', '''	if not dedicated and not lan_players.is_empty():
		lan_players[0].name = my_name()
		lan_players[0].look = look_str(my_look())
	reset_match()''')
rep('''	lan_players = [{"peer": 1, "name": my_name(), "look": look_str(my_look())}]''', '''	lan_players = [{"peer": 1, "name": my_name(), "look": look_str(my_look()), "uid": str(cfg.uid)}]''')

# ---------- hello: uid, rejoin ----------
rep('''func c_hello(nm, ver, lk = "") -> void:''', '''func c_hello(nm, ver, lk = "", cuid = "") -> void:''')
rep('''	if not ["lobby", "lan_cfg", "over"].has(state):
		rpc_id(id, "s_reject", "A match is running. Try again when it ends.")
		return''', '''	if dedicated and str(cuid) != "":
		# same phone coming back: take its old seat
		for j in range(lan_players.size() - 1, -1, -1):
			if str(lan_players[j].get("uid", "")) == str(cuid) and int(lan_players[j].peer) != id:
				var oldp := int(lan_players[j].peer)
				lan_players.remove_at(j)
				for p in players:
					if p.remote and p.peer_id == oldp:
						p.peer_id = -1
				multiplayer.multiplayer_peer.disconnect_peer(oldp)
		if state == "play" and try_rejoin(id, str(cuid), lk):
			return
	if not ["lobby", "lan_cfg", "over"].has(state):
		rpc_id(id, "s_reject", "A match is running. Try again when it ends.")
		return''')
rep('''	lan_players.append({"peer": id, "name": pick, "look": look_str(parse_look(lk))})''', '''	lan_players.append({"peer": id, "name": pick, "look": look_str(parse_look(lk)), "uid": str(cuid)})''')
rep('''	rpc_id(1, "c_hello", my_name(), VERSION, look_str(my_look()))''', '''	rpc_id(1, "c_hello", my_name(), VERSION, look_str(my_look()), str(cfg.uid))''')
rep('''		if p.remote and p.peer_id == id:
			p.remote = false
			p.bot = true''', '''		if p.remote and p.peer_id == id:
			p.remote = false
			p.dropped = true
			p.bot = true''')
rep('''	var info := {"pl": lobby_names(), "lk": lobby_looks(), "mode": cfg.mode,''', '''	var info := {"room": room_code, "owner": str(lan_players[0].get("uid", "")) if (dedicated and not lan_players.is_empty()) else "", "pl": lobby_names(), "lk": lobby_looks(), "mode": cfg.mode,''')
rep('''	lobby_info = info
	if state == "connecting" or''', '''	lobby_info = info
	if online and is_owner() and not cfg_sent:
		cfg_sent = true
		rpc_id(1, "c_cfg", my_settings())
	if state == "connecting" or''')

# ---------- client: prediction + reconnect watchdog ----------
rep('''@rpc("authority", "call_remote", "unreliable_ordered", 1)
func s_snap(d) -> void:
	if net_role != "client" or not (pending_start or state == "play" or state == "paused"):
		return''', '''@rpc("authority", "call_remote", "unreliable_ordered", 1)
func s_snap(d) -> void:
	if lag_ms > 0:
		lag_in.append([time_s + lag_ms / 2000.0, d])
		return
	apply_snap(d)

func apply_snap(d) -> void:
	if net_role != "client" or not (pending_start or state == "play" or state == "paused"):
		return
	snap_wait = 0.0''')
rep('''		p.nx = pf[o]
		p.ny = pf[o + 1]
		p.vx = pf[o + 2]
		p.vy = pf[o + 3]''', '''		var mine := i == my_idx and predicting()
		p.nx = pf[o]
		p.ny = pf[o + 1]
		p.svx = pf[o + 2]
		p.svy = pf[o + 3]
		if not mine:
			p.vx = p.svx
			p.vy = p.svy''')
rep('''		p.alive = (fl & 1) != 0
		p.jet_on = (fl & 2) != 0
		p.on_ground = (fl & 4) != 0
		p.in_water = (fl & 8) != 0''', '''		p.alive = (fl & 1) != 0
		if not mine:
			p.jet_on = (fl & 2) != 0
			p.on_ground = (fl & 4) != 0
		p.in_water = (fl & 8) != 0''')
rep('''		p.fuel = pf[o + 6]''', '''		p.fuel = pf[o + 6]
		p.pfuel = p.fuel''')
rep('''		if (p.alive and not was_alive) or snaps_got == 1 or Vector2(p.x - p.nx, p.y - p.ny).length() > 160:
			p.x = p.nx
			p.y = p.ny''', '''		if (p.alive and not was_alive) or snaps_got == 1 or (not mine and Vector2(p.x - p.nx, p.y - p.ny).length() > 160):
			p.x = p.nx
			p.y = p.ny
			p.vx = p.svx
			p.vy = p.svy''')
rep('''		var age := minf(p.snap_age, 0.12)
		var k := ease_k(18.0, dt)
		p.x += (p.nx + p.vx * age - p.x) * k
		p.y += (p.ny + p.vy * age - p.y) * k''', '''		if i == my_idx and predicting():
			predict_me(p, dt)
		else:
			var age := minf(p.snap_age, 0.12)
			var k := ease_k(18.0, dt)
			p.x += (p.nx + p.vx * age - p.x) * k
			p.y += (p.ny + p.vy * age - p.y) * k''')
rep('''		rpc_id(1, "c_input", [i2.mx, i2.fly, i2.shoot, i2.swap, i2.grenade, i2.melee, i2.reload, me.aim, i2.down, i2.pick, i2.zoom, i2.bomb, i2.smoke])''', '''		var pkt := [i2.mx, i2.fly, i2.shoot, i2.swap, i2.grenade, i2.melee, i2.reload, me.aim, i2.down, i2.pick, i2.zoom, i2.bomb, i2.smoke]
		if lag_ms > 0:
			lag_out.append([time_s + lag_ms / 2000.0, pkt])
		else:
			rpc_id(1, "c_input", pkt)''')
rep('''func update_client(dt: float) -> void:
	if pending_start or players.is_empty() or my_idx >= players.size():
		return''', '''func update_client(dt: float) -> void:
	if pending_start or players.is_empty() or my_idx >= players.size():
		return
	if online and state == "play":
		snap_wait += dt
		if snap_wait > 5.0:
			start_reconnect()
			return''')

# connection drops / failures while online
rep('''func _on_conn_failed() -> void:
	net_close()
	state = "lan_join"
	toast("Could not join. Are you connected to the host's hotspot?")''', '''func _on_conn_failed() -> void:
	net_close()
	if online:
		if recon_left > 0:
			start_reconnect()
			return
		online = false
		state = "online"
		toast("Could not reach the room. Check your internet and try again.")
		return
	state = "lan_join"
	toast("Could not join. Are you connected to the host's hotspot?")''')
rep('''func _on_server_gone() -> void:
	net_close()
	state = "lan"
	toast("The host closed the game.")''', '''func _on_server_gone() -> void:
	if online and room_code != "":
		start_reconnect()
		return
	net_close()
	state = "lan"
	toast("The host closed the game.")''')
rep('''	if state == "connecting":
		connect_t -= delta
		if connect_t <= 0:
			_on_conn_failed()''', '''	if state == "connecting" and mm_mode == "":
		connect_t -= delta
		if connect_t <= 0:
			_on_conn_failed()
	lag_tick()
	if online and net_role == "client" and multiplayer.multiplayer_peer != null and multiplayer.multiplayer_peer.has_method("get_peer"):
		rtt_t -= delta
		if rtt_t <= 0:
			rtt_t = 1.0
			var sp = multiplayer.multiplayer_peer.get_peer(1)
			if sp != null:
				rtt_s = sp.get_statistic(3) / 1000.0 + lag_ms / 1000.0''')
rep('''	var err: int = pe.create_client(ip, NET_PORT)
	if err != OK:
		toast("Could not join %s" % ip)
		return
	pe.host.compress(1)  # range coder''', '''	var err: int = pe.create_client(ip, port)
	if err != OK:
		toast("Could not join %s" % ip)
		return
	pe.host.compress(1)  # range coder
	var sp = pe.get_peer(1)
	if sp != null:
		sp.set_timeout(32, 4000, 9000)''')
rep('''func join_game(ip: String) -> void:''', '''func join_game(ip: String, port := NET_PORT) -> void:''')
rep('''	connect_t = 7.0
	state = "connecting"''', '''	connect_t = 9.0 if online else 7.0
	state = "connecting"''')

# ---------- actions ----------
rep('''		"leave", "cancel":
			net_close()
			state = "lan"''', '''		"leave", "cancel":
			net_close()
			mm_mode = ""
			state = "online" if online else "lan"
			online = false
			recon_left = 0
		"online":
			if OS.has_feature("web"):
				toast("Online rooms work in the app, not in the browser.")
			else:
				state = "online"
		"o_create":
			if str(cfg.server).strip_edges() == "":
				toast("Set the server address first (tap CHANGE).")
			else:
				mm_query("new", make_code())
		"o_join":
			if str(cfg.server).strip_edges() == "":
				toast("Set the server address first (tap CHANGE).")
			else:
				key_target = "room"
				name_entry = ""
				state = "namekey"
		"o_server":
			key_target = "server"
			name_entry = str(cfg.server)
			state = "namekey"
		"o_start":
			if net_role == "client" and is_owner():
				rpc_id(1, "c_start", my_settings())''')
rep('''		"again":
			if net_role == "host":
				start_lan_match()''', '''		"again":
			if net_role == "client" and online:
				if is_owner():
					rpc_id(1, "c_start", my_settings())
			elif net_role == "host":
				start_lan_match()''')
rep('''		"lobby_back":
			state = "lobby"
			send_lobby()''', '''		"lobby_back":
			state = "lobby"
			send_lobby()
			if net_role == "client" and online and is_owner():
				rpc_id(1, "c_cfg", my_settings())''')
rep('''		"lk_name":
			name_entry = my_name()
			state = "namekey"''', '''		"lk_name":
			key_target = "name"
			name_entry = my_name()
			state = "namekey"''')
rep('''		"name_ok":
			var nm := name_entry.strip_edges()
			if nm != "":
				cfg.name = nm
				save_cfg()
			state = "locker"
		"name_back":
			state = "locker"''', '''		"name_ok":
			var nm := name_entry.strip_edges()
			if key_target == "room":
				if nm.length() < 4:
					toast("Room codes have at least 4 letters, like TIGER42.")
				else:
					mm_query("join", nm)
				return
			if key_target == "server":
				cfg.server = nm.to_lower()
				save_cfg()
				state = "online"
				return
			if nm != "":
				cfg.name = nm
				save_cfg()
			state = "locker"
		"name_back":
			state = "locker" if key_target == "name" else "online"''')
rep('''		"namekey":
			state = "locker"''', '''		"namekey":
			state = "locker" if key_target == "name" else "online"
		"online":
			state = "lan"''')
rep('''		"connecting", "lobby":
			net_close()
			state = "lan"''', '''		"connecting", "lobby":
			net_close()
			mm_mode = ""
			state = "online" if online else "lan"
			online = false
			recon_left = 0''')

# typing rules per field
rep('''	if not raw:
		k = k.to_upper() if (name_entry == "" or name_entry.ends_with(" ")) else k.to_lower()
	var ok := "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 _-"
	if ok.contains(k):
		name_entry += k''', '''	if key_target == "room":
		k = k.to_upper()
		if name_entry.length() < 8 and "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789".contains(k):
			name_entry += k
		return
	if key_target == "server":
		k = k.to_lower()
		if name_entry.length() < 40 and "abcdefghijklmnopqrstuvwxyz0123456789.-".contains(k):
			name_entry += k
		return
	if not raw:
		k = k.to_upper() if (name_entry == "" or name_entry.ends_with(" ")) else k.to_lower()
	var ok := "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 _-"
	if ok.contains(k):
		name_entry += k''')
rep('''	if name_entry.length() >= 12:
		return
	if k == " " and''', '''	if name_entry.length() >= 12 and key_target == "name":
		return
	if k == " " and key_target != "name":
		return
	if k == " " and''')
rep('''	txh("YOUR NAME", Vector2(x, y + 38 * u), 24 * u, C_ARC, 0, 4 * u)
	txt("Up to 12 letters. Everyone sees it over your head.", Vector2(r.end.x - 22 * u, y + 34 * u), 10 * u, C_MUTED, 2)''', '''	var titles := {"name": ["YOUR NAME", "Up to 12 letters. Everyone sees it over your head."],
		"room": ["ROOM CODE", "Type the code your friend got, like TIGER42."],
		"server": ["SERVER ADDRESS", "Ask the group admin. Example: 140.238.1.2"]}
	var tt: Array = titles.get(key_target, titles.name)
	txh(tt[0], Vector2(x, y + 38 * u), 24 * u, C_ARC, 0, 4 * u)
	txt(tt[1], Vector2(r.end.x - 22 * u, y + 34 * u), 10 * u, C_MUTED, 2)''')
rep('''	txt("%d/12" % name_entry.length(), Vector2(fr.end.x - 10 * u, fr.position.y + 28 * u), 10 * u, C_MUTED, 2)
	var dr := flat_btn(Rect2(fr.end.x + 8 * u, fr.position.y, 44 * u, 44 * u), "lk_dice")
	fbox(dr, Color(0.2, 0.25, 0.43), 9 * u, Color(1, 1, 1, 0.13), maxf(1.0, u))
	draw_dice(dr.get_center(), 22 * u)
	ui_button("SAVE", Rect2(dr.end.x + 8 * u, fr.position.y, r.end.x - 22 * u - dr.end.x - 8 * u, 44 * u), "name_ok", true)''', '''	if key_target == "name":
		txt("%d/12" % name_entry.length(), Vector2(fr.end.x - 10 * u, fr.position.y + 28 * u), 10 * u, C_MUTED, 2)
		var dr := flat_btn(Rect2(fr.end.x + 8 * u, fr.position.y, 44 * u, 44 * u), "lk_dice")
		fbox(dr, Color(0.2, 0.25, 0.43), 9 * u, Color(1, 1, 1, 0.13), maxf(1.0, u))
		draw_dice(dr.get_center(), 22 * u)
	var okx := fr.end.x + 60 * u
	ui_button({"name": "SAVE", "room": "JOIN", "server": "SAVE"}.get(key_target, "SAVE"), Rect2(okx, fr.position.y, r.end.x - 22 * u - okx, 44 * u), "name_ok", true)''')
rep('''	for ri in KB_ROWS.size():
		var row: String = KB_ROWS[ri]''', '''	for ri in KB_ROWS.size():
		var row: String = KB_ROWS[ri]
		if ri == 3 and key_target == "server":
			row = "ZXCVBNM.-"''')

# ---------- screens ----------
rep('''	txh("PLAY WITH FRIENDS", Vector2(x, y + 42 * u), 26 * u, C_ARC, 0, 4 * u)
	txt("Phones close together. No internet needed.", Vector2(x, y + 64 * u), 11 * u, C_MUTED)
	var bw := 230 * u
	var bh := 44 * u
	ui_button("HOST A GAME", Rect2(x, y + 84 * u, bw, bh), "host", true)
	ui_button("JOIN A GAME", Rect2(x, y + 136 * u, bw, bh), "join", true)
	ui_button("NAME & LOOK: " + my_name(), Rect2(x, y + 188 * u, bw, bh), "name")
	ui_button("BACK", Rect2(x, y + 240 * u, bw, bh), "back")''', '''	txh("PLAY WITH FRIENDS", Vector2(x, y + 42 * u), 26 * u, C_ARC, 0, 4 * u)
	txt("From anywhere online, or phones close together.", Vector2(x, y + 64 * u), 11 * u, C_MUTED)
	var bw := 230 * u
	var bh := 40 * u
	ui_button("ONLINE ROOMS", Rect2(x, y + 80 * u, bw, bh), "online", true)
	ui_button("HOST (HOTSPOT)", Rect2(x, y + 128 * u, bw, bh), "host")
	ui_button("JOIN (HOTSPOT)", Rect2(x, y + 176 * u, bw, bh), "join")
	ui_button("NAME & LOOK: " + my_name(), Rect2(x, y + 224 * u, bw, bh), "name")
	ui_button("BACK", Rect2(x, y + 272 * u, bw, bh), "back")''')
rep('''		"HOW IT WORKS",
		"1. One phone turns on its Wi-Fi hotspot",
		"    and taps HOST A GAME.",
		"2. Friends connect to that hotspot,",
		"    then tap JOIN A GAME.",
		"3. The host taps START. Bots fill the",
		"    empty places (up to 6 players).",
		"",
		"Same home Wi-Fi works too.",
		"Tap NAME to change your name.",''', '''		"ONLINE ROOMS",
		"Play from anywhere on mobile data or Wi-Fi.",
		"One friend makes a room, others type its code.",
		"",
		"HOTSPOT",
		"1. One phone turns on its Wi-Fi hotspot",
		"    and taps HOST (HOTSPOT).",
		"2. Friends join that hotspot, then tap",
		"    JOIN (HOTSPOT). Same home Wi-Fi works too.",''')
rep('''		var head: bool = i == 0
		txt(lines[i], Vector2(rx, y + 100 * u + i * 19 * u), (10 if head else 12) * u, C_CYAN if head else C_MUTED)''', '''		var head: bool = lines[i] == "ONLINE ROOMS" or lines[i] == "HOTSPOT"
		txt(lines[i], Vector2(rx, y + 96 * u + i * 19 * u), (10 if head else 12) * u, C_CYAN if head else C_MUTED)''')
rep('''			"lan_join":
				draw_join()''', '''			"lan_join":
				draw_join()
			"online":
				draw_online()''')
rep('''	var dots := ".".repeat(int(time_s * 2.0) % 4)
	txt("Joining " + join_ip + dots,''', '''	var dots := ".".repeat(int(time_s * 2.0) % 4)
	if online or mm_mode != "":
		txt(conn_label + dots, Vector2(r.get_center().x, r.position.y + 70 * u), 18 * u, C_INK, 1)
		if recon_left > 0:
			txt("Your bot keeps playing until you are back.", Vector2(r.get_center().x, r.position.y + 96 * u), 11 * u, C_MUTED, 1)
		ui_button("CANCEL", Rect2(r.get_center().x - 90 * u, r.end.y - 66 * u, 180 * u, 44 * u), "cancel")
		return
	txt("Joining " + join_ip + dots,''')
rep('''	var host := net_role == "host"
	txh("LOBBY", Vector2(x, y + 42 * u), 26 * u, C_ARC, 0, 4 * u)
	txt("You are hosting" if host else "Joined " + join_ip, Vector2(x + 110 * u, y + 40 * u), 12 * u, C_CYAN)''', '''	var host := net_role == "host"
	if online:
		txh("ROOM  " + room_code, Vector2(x, y + 42 * u), 26 * u, C_ARC, 0, 4 * u)
		txt("Tell friends this code. They tap ONLINE ROOMS, then JOIN ROOM.", Vector2(x, y + 62 * u), 10 * u, C_CYAN)
	else:
		txh("LOBBY", Vector2(x, y + 42 * u), 26 * u, C_ARC, 0, 4 * u)
		txt("You are hosting" if host else "Joined " + join_ip, Vector2(x + 110 * u, y + 40 * u), 12 * u, C_CYAN)''')
rep('''		var tag := "  (host)" if i == 0 else ""''', '''		var tag := ("  (leader)" if online else "  (host)") if i == 0 else ""''')
rep('''	else:
		var dots := ".".repeat(int(time_s * 2.0) % 4)
		txt("Waiting for the host to start" + dots, Vector2(rx, y + 140 * u), 14 * u, C_INK)
		ui_button("LEAVE", Rect2(rx, y + 246 * u, 160 * u, 42 * u), "leave")''', '''	elif online and is_owner():
		txt("You are the room leader.", Vector2(rx, y + 124 * u), 11 * u, C_MUTED)
		txt("Start when everyone is in. Bots fill empty places.", Vector2(rx, y + 142 * u), 11 * u, C_MUTED)
		var bw2 := (r.end.x - 26 * u - rx - 10 * u) / 2.0
		ui_button("START", Rect2(rx, y + 190 * u, bw2 * 2 + 10 * u, 48 * u), "o_start", true)
		ui_button("SETTINGS", Rect2(rx, y + 246 * u, bw2, 42 * u), "lan_cfg")
		ui_button("LEAVE", Rect2(rx + bw2 + 10 * u, y + 246 * u, bw2, 42 * u), "leave")
	else:
		var dots := ".".repeat(int(time_s * 2.0) % 4)
		var lead: String = str(names[0]) if (online and not names.is_empty()) else "the host"
		txt("Waiting for %s to start" % lead + dots, Vector2(rx, y + 140 * u), 14 * u, C_INK)
		ui_button("LEAVE", Rect2(rx, y + 246 * u, 160 * u, 42 * u), "leave")''')
rep('''	if net_role == "client":
		txt("Waiting for the host to start the next match...", Vector2(r.position.x + 24 * u, r.end.y - 30 * u), 11 * u, C_MUTED)''', '''	if net_role == "client" and online and is_owner():
		ui_button("PLAY AGAIN", Rect2(r.get_center().x - 210 * u, r.end.y - 58 * u, 200 * u, 44 * u), "again", true)
		ui_button("LEAVE", Rect2(r.get_center().x + 10 * u, r.end.y - 58 * u, 200 * u, 44 * u), "leave")
		return
	if net_role == "client":
		txt("Waiting for the %s to start the next match..." % ("room leader" if online else "host"), Vector2(r.position.x + 24 * u, r.end.y - 30 * u), 11 * u, C_MUTED)''')

# room-finder replies, polled with the rest of the network
rep('''func net_poll(dt: float) -> void:
	if OS.has_feature("web"):
		return''', '''func net_poll(dt: float) -> void:
	if OS.has_feature("web"):
		return
	mm_poll(dt)''')

# drop test: client cuts its own connection once mid-match to prove rejoin works
rep('''	lantest_tick(delta)''', '''	lantest_tick(delta)
	if drop_test and state == "play" and net_role == "client" and t > 12.0 and not drop_done:
		drop_done = true
		print("CLIENT drop test: cutting the connection")
		multiplayer.multiplayer_peer.close()
		start_reconnect()''')

s += '''
# ================= ONLINE ROOMS (v1.2) =================
const MM_PORT := 24870
const CODE_WORDS := ["TIGER", "HAWK", "COBRA", "STORM", "BLAZE", "VIPER", "ROCKET", "NINJA", "COMET", "BOLT", "FALCON", "GHOST", "SHARK", "LION", "EAGLE", "RHINO"]
var dedicated := false
var room_code := ""
var online := false
var mm: PacketPeerUDP = null
var mm_mode := ""
var mm_code := ""
var mm_ip := ""
var mm_t := 0.0
var mm_tries := 0
var conn_label := ""
var key_target := "name"
var idle_t := 0.0
var recon_left := 0
var snap_wait := 0.0
var rtt_s := 0.0
var rtt_t := 0.0
var lag_ms := 0
var lag_in: Array = []
var lag_out: Array = []
var cfg_sent := false
var drop_test := false
var drop_done := false
var pred_err := 0.0
var pred_n := 0
var pred_snaps := 0

func make_code() -> String:
	return CODE_WORDS[randi() % CODE_WORDS.size()] + str(10 + randi() % 90)

func is_owner() -> bool:
	return str(lobby_info.get("owner", "")) != "" and str(lobby_info.get("owner", "")) == str(cfg.uid)

func my_settings() -> Dictionary:
	var out := {}
	for row in LAN_ROWS:
		out[row[0]] = cfg[row[0]]
	return out

func predicting() -> bool:
	return net_role == "client"

# ask the room finder on the server which port the room lives on
func mm_query(mode: String, code: String) -> void:
	var host := str(cfg.server).strip_edges()
	var ip := host if host.is_valid_ip_address() else IP.resolve_hostname(host, IP.TYPE_IPV4)
	if ip == "":
		toast("Can't find the server. Check the address.")
		state = "online"
		return
	mm_ip = ip
	mm_mode = mode
	mm_code = code.to_upper()
	mm_tries = 0
	mm_t = 0.0
	if mm == null:
		mm = PacketPeerUDP.new()
		mm.bind(0)
	online = true
	room_code = mm_code
	cfg_sent = false
	if recon_left <= 0:
		conn_label = ("Opening room " if mode == "new" else "Joining room ") + mm_code
	state = "connecting"

func mm_poll(dt: float) -> void:
	if mm == null or mm_mode == "":
		return
	mm_t -= dt
	if mm_t <= 0:
		mm_t = 0.6
		mm_tries += 1
		if mm_tries > 10:
			mm_mode = ""
			if recon_left > 0:
				start_reconnect()
				return
			online = false
			state = "online"
			toast("The server is not answering. Is it switched on?")
			return
		mm.set_dest_address(mm_ip, MM_PORT)
		mm.put_packet(("SKYROOM?|%s|%s|%s" % [mm_mode, mm_code, VERSION]).to_utf8_buffer())
	while mm.get_available_packet_count() > 0:
		var bits := mm.get_packet().get_string_from_utf8().split("|")
		if bits.size() < 4 or bits[0] != "SKYROOM!" or bits[1] != mm_code:
			continue
		mm_mode = ""
		match bits[3]:
			"ok":
				join_game(mm_ip, int(bits[2]))
			"none":
				online = false
				state = "online"
				toast("No room called %s. Check the code with your friend." % mm_code)
			"full":
				online = false
				state = "online"
				toast("The server is busy. Try again in a few minutes.")
			"old":
				online = false
				state = "online"
				toast("The server has a different version. Update Sky Squad.")
			_:
				online = false
				state = "online"
				toast("The server said no (%s)." % bits[3])
		return

# lost the room mid-game: try to get back in a few times
func start_reconnect() -> void:
	if recon_left <= 0:
		recon_left = 4
	recon_left -= 1
	var code := room_code
	net_close()
	online = true
	room_code = code
	if recon_left <= 0:
		online = false
		state = "online"
		toast("Lost the connection to room %s." % code)
		return
	conn_label = "Connection lost. Getting you back into " + code
	print("CLIENT reconnecting to ", code)
	mm_query("join", code)

func lag_tick() -> void:
	if lag_ms <= 0:
		return
	while not lag_in.is_empty() and lag_in[0][0] <= time_s:
		apply_snap(lag_in.pop_front()[1])
	while not lag_out.is_empty() and lag_out[0][0] <= time_s:
		var pk = lag_out.pop_front()[1]
		if net_role == "client":
			rpc_id(1, "c_input", pk)

# your own soldier moves at once on your phone; the server's word gently pulls it back if they differ
func predict_me(p: Player, dt: float) -> void:
	var inp: Dictionary = p.inp
	var c := center(p)
	var z = zone_at(c.x, c.y)
	var gm: float = z.g if z != null else 1.0
	var fm: float = z.f if z != null else 1.0
	var post_mul: float = S.crouch_speed if p.posture == "crouch" else (S.crawl_speed if p.posture == "prone" else 1.0)
	var fly: bool = inp.fly and p.posture == "stand"
	if p.net_t > 0 or p.stun_t > 0:
		fly = false
		post_mul *= 0.35 if p.net_t > 0 else 0.15
	var cw0 = p.slots[p.cur]
	if cw0 != null and cw0.type == "minigun":
		post_mul *= 0.72
	var target: float = inp.mx * S.move_speed * (0.55 if p.in_water else 1.0) * post_mul
	var acc := 1100.0 if p.on_ground else 520.0
	if p.vx < target:
		p.vx = minf(target, p.vx + acc * dt)
	elif p.vx > target:
		p.vx = maxf(target, p.vx - acc * dt)
	p.jet_on = false
	if fly:
		if p.in_water:
			p.vy -= g_dir * 1300 * dt
		elif p.pfuel > 0:
			if p.on_ground:
				p.vy = -gsign() * S.jump_speed
			p.vy -= g_dir * S.thrust * gm * dt
			p.pfuel = maxf(0.0, p.pfuel - S.fuel_drain * fm * dt)
			p.jet_on = true
	p.vy += S.gravity * gm * g_dir * dt * (0.3 if p.in_water else 1.0)
	if p.in_water:
		p.vx *= pow(0.3, dt)
		p.vy *= pow(0.2, dt)
	var fall: float = 200.0 if p.in_water else S.max_fall
	if p.vy * gsign() > fall:
		p.vy = fall * gsign()
	if -p.vy * gsign() > S.max_rise and p.jet_on:
		p.vy = -S.max_rise * gsign()
	p.vx = clampf(p.vx, -700, 700)
	move_entity(p, dt)
	# where the server says we are, moved forward by the time its message took to arrive
	var lat := clampf(rtt_s * 0.5, 0.0, 0.3)
	var tgt := Vector2(p.nx, p.ny) + Vector2(p.svx, p.svy) * minf(p.snap_age + lat, 0.35)
	var err := tgt - Vector2(p.x, p.y)
	var el := err.length()
	pred_err += el
	pred_n += 1
	if el > 150.0:
		p.x = tgt.x
		p.y = tgt.y
		p.vx = p.svx
		p.vy = p.svy
		pred_snaps += 1
	elif el > 2.0:
		var kk := ease_k(5.0 if el > 50.0 else 2.5, dt)
		var ox := p.x
		var oy := p.y
		p.x += err.x * kk
		p.y += err.y * kk
		if rect_hits(p.x, p.y, p.w, p.h):
			p.x = ox
			p.y = oy

# ---------- the no-screen room server ----------
func dedicated_start(port: int, code: String) -> void:
	dedicated = true
	room_code = code
	Engine.max_fps = 60
	var pe = ClassDB.instantiate("ENetMultiplayerPeer")
	if pe == null or pe.create_server(port, 8) != OK:
		print("SERVER could not open port ", port)
		get_tree().quit(1)
		return
	pe.host.compress(1)
	multiplayer.multiplayer_peer = pe
	net_role = "host"
	my_idx = 99
	lan_players = []
	state = "lobby"
	print("SERVER room %s ready on port %d (version %s)" % [code, port, VERSION])

func dedicated_tick(delta: float, dt: float) -> void:
	time_s += delta
	if state == "play":
		update_game(dt)
	if lan_players.is_empty():
		idle_t += delta
		if idle_t > 90.0:
			print("SERVER room %s empty, closing" % room_code)
			get_tree().quit()
	else:
		idle_t = 0.0
	if state == "over":
		for p in players:
			p.inp = blank_inp()

func try_rejoin(id: int, cuid: String, lk) -> bool:
	for i in players.size():
		var p: Player = players[i]
		if p.uid == cuid and (p.dropped or p.remote):
			p.peer_id = id
			p.remote = true
			p.bot = false
			p.dropped = false
			p.inp = blank_inp()
			p.prev = p.inp.duplicate()
			lan_players.append({"peer": id, "name": p.pname, "look": look_str(p.look), "uid": cuid})
			rpc_id(id, "s_start", start_info(i))
			feed.push_front({"k": "", "kc": C_INK, "v": "%s is back!" % p.pname, "vc": C_ARC, "gun": "", "head": false, "t": 4.0, "t0": 4.0, "note": ""})
			print("SERVER %s rejoined" % p.pname)
			return true
	return false

func apply_settings(st) -> void:
	if typeof(st) != TYPE_DICTIONARY:
		return
	for row in LAN_ROWS:
		if st.has(row[0]) and (row[2] as Array).has(st[row[0]]):
			cfg[row[0]] = st[row[0]]

func sender_is_owner() -> bool:
	return dedicated and not lan_players.is_empty() and int(lan_players[0].peer) == multiplayer.get_remote_sender_id()

@rpc("any_peer", "call_remote", "reliable")
func c_cfg(st) -> void:
	if not sender_is_owner():
		return
	apply_settings(st)
	send_lobby()

@rpc("any_peer", "call_remote", "reliable")
func c_start(st) -> void:
	if not sender_is_owner() or not ["lobby", "lan_cfg", "over"].has(state):
		return
	apply_settings(st)
	print("SERVER room %s: match starting with %d players" % [room_code, lan_players.size()])
	send_lobby(true)
	start_lan_match()

func draw_online() -> void:
	var w := minf(sw - 32 * u, 640 * u)
	var h := minf(sh - 24 * u, 330 * u)
	var r := panel(w, h)
	var x := r.position.x + 26 * u
	var y := r.position.y
	txh("ONLINE ROOMS", Vector2(x, y + 42 * u), 26 * u, C_ARC, 0, 4 * u)
	txt("Play with friends anywhere, on mobile data or Wi-Fi.", Vector2(x, y + 64 * u), 11 * u, C_MUTED)
	var bw := 230 * u
	var bh := 44 * u
	ui_button("CREATE ROOM", Rect2(x, y + 84 * u, bw, bh), "o_create", true)
	ui_button("JOIN ROOM", Rect2(x, y + 136 * u, bw, bh), "o_join", true)
	ui_button("BACK", Rect2(x, y + 240 * u, bw, bh), "to_lan")
	var sr := flat_btn(Rect2(x, y + 188 * u, bw, bh), "o_server")
	fbox(sr, Color(0.02, 0.03, 0.08, 0.9), 9 * u, Color(1, 1, 1, 0.16), maxf(1.0, u))
	txt("SERVER", sr.position + Vector2(10 * u, 14 * u), 8 * u, C_CYAN)
	var sv := str(cfg.server)
	txt(sv if sv != "" else "not set", sr.position + Vector2(10 * u, 33 * u), 13 * u, C_INK if sv != "" else C_MUTED)
	txt("CHANGE", Vector2(sr.end.x - 8 * u, sr.position.y + 27 * u), 9 * u, C_ARC, 2)
	var rx := x + bw + 28 * u
	var lines := [
		"HOW IT WORKS",
		"1. One friend taps CREATE ROOM.",
		"2. The game shows a code, like TIGER42.",
		"    Send it on WhatsApp.",
		"3. Friends tap JOIN ROOM and type it.",
		"4. The room leader taps START.",
		"",
		"If your internet drops, the game puts",
		"you back in your seat. A bot covers you.",
	]
	for i in lines.size():
		var head: bool = i == 0
		txt(lines[i], Vector2(rx, y + 100 * u + i * 19 * u), (10 if head else 12) * u, C_CYAN if head else C_MUTED)
'''

# lantest end print: add prediction numbers
rep('''		print("CLIENT fx: ", fx_count)''', '''		print("CLIENT fx: ", fx_count)
		print("CLIENT prediction: avg_error=%.1fpx hard_corrections=%d rtt=%dms" % [pred_err / maxf(1.0, pred_n), pred_snaps, int(rtt_s * 1000)])''')
rep('''	if lantest_join != "" and lt_done > 0 and time_s - lt_done > 3.0:
		get_tree().quit()''', '''	if lantest_join == "online" and state == "lobby" and is_owner() and (lobby_names().size() >= 2 or time_s > 30.0):
		lt_wait += dt
		if lt_wait > 3.0:
			lt_wait = -999.0
			print("CLIENT owner starts the match, players=", lobby_names())
			do_action("o_start")
	if lantest_join != "" and lt_done > 0 and time_s - lt_done > 3.0:
		get_tree().quit()''')
rep('''func _on_connected() -> void:''', '''func _on_connected() -> void:
	recon_left = 0''')
rep('''				if a2.begins_with("--room="):
					droom = a2.substr(7)''', '''				if a2.begins_with("--room="):
					droom = a2.substr(7)
				if a2.begins_with("--matchsecs="):
					lantest_time = float(a2.substr(12))''')
open(P, "w").write(s)
print("ok")
