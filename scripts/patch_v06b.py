"""v0.6 part B: networking (ENet host/client, discovery), client view, LAN menus, test hooks."""
import sys
P = "/home/claude/skysquad/main.gd"
s = open(P).read()

def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        sys.exit(f"expected {count} got {n}: {old[:90]!r}")
    s = s.replace(old, new)

# ---------- _ready: signals + test flags ----------
rep('''	var args := OS.get_cmdline_user_args()
	if args.has("--autotest"):''', '''	multiplayer.peer_disconnected.connect(_on_peer_gone)
	multiplayer.connected_to_server.connect(_on_connected)
	multiplayer.connection_failed.connect(_on_conn_failed)
	multiplayer.server_disconnected.connect(_on_server_gone)
	var args := OS.get_cmdline_user_args()
	for a in args:
		if a == "--lantest-host":
			lantest_host = true
			lantest_time = 45.0
			Engine.max_fps = 60
			cfg.name = "Host"
			cfg.lan_bots = 2
			host_game()
		if a.begins_with("--lantest-join="):
			lantest_join = a.substr(15)
			lantest_time = 45.0
			Engine.max_fps = 60
			cfg.name = "Tester"
			if lantest_join == "auto":
				state = "lan_join"
			else:
				join_game(lantest_join)
		if a.begins_with("--lanshot="):
			for spec in a.substr(10).split(","):
				lan_shots.append(spec.split(":"))
		if a == "--shots-quit":
			shots_quit = true
	if args.has("--autotest"):''')

# ---------- go back / Esc ----------
old = s[s.index('func _notification(what: int) -> void:'):s.index('	if event is InputEventScreenTouch:')]
new = '''func _notification(what: int) -> void:
	if what == NOTIFICATION_WM_GO_BACK_REQUEST:
		go_back(true)

func go_back(can_quit: bool) -> void:
	match state:
		"play":
			state = "paused"
			jet_player.stop()
		"paused":
			state = "play"
		"match_cfg", "ctrl_cfg", "lan":
			state = "menu"
		"over":
			if net_role == "":
				state = "menu"
		"lan_join":
			state = "lan"
		"ipkey":
			state = "lan_join"
		"connecting", "lobby":
			net_close()
			state = "lan"
		"lan_cfg":
			do_action("lobby_back")
		"menu":
			if can_quit:
				get_tree().quit()

func _input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		if state == "ipkey":
			var ch := char(event.unicode) if event.unicode > 0 else ""
			if event.keycode == KEY_BACKSPACE:
				do_action("key:DEL")
				return
			if event.keycode == KEY_ENTER or event.keycode == KEY_KP_ENTER:
				do_action("ipjoin")
				return
			if ch != "" and "0123456789.".contains(ch):
				do_action("key:" + ch)
				return
		if event.keycode == KEY_ESCAPE or (event.keycode == KEY_P and (state == "play" or state == "paused")):
			go_back(false)
			return
'''
s = s.replace(old, new)

# ---------- actions ----------
rep('''		"play", "again", "restart":
			reset_match()
			state = "play"''', '''		"play", "restart":
			reset_match()
			state = "play"
		"again":
			if net_role == "host":
				start_lan_match()
			else:
				reset_match()
				state = "play"
		"lan":
			if OS.has_feature("web"):
				toast("LAN play works in the Android app, not in the browser.")
			else:
				state = "lan"
		"name":
			var i0 := FUN_NAMES.find(my_name())
			cfg.name = FUN_NAMES[(i0 + 1) % FUN_NAMES.size()]
			save_cfg()
		"host":
			host_game()
		"join":
			found_hosts.clear()
			state = "lan_join"
		"to_lan":
			state = "lan"
		"ipkey":
			if ip_entry == "":
				var ips := lan_ips()
				if ips.size() > 0:
					var b: PackedStringArray = str(ips[0]).split(".")
					ip_entry = "%s.%s.%s.1" % [b[0], b[1], b[2]]
			state = "ipkey"
		"ipjoin":
			join_game(ip_entry)
		"start":
			start_lan_match()
		"lan_cfg":
			state = "lan_cfg"
		"lobby_back":
			state = "lobby"
			send_lobby()
		"to_lobby":
			state = "lobby"
			send_lobby(true)
		"leave", "cancel":
			net_close()
			state = "lan"''')
rep('''		"back", "menu":
			state = "menu"
			jet_player.stop()''', '''		"back", "menu":
			if net_role != "":
				net_close()
			state = "menu"
			jet_player.stop()''')
rep('''			if a.begins_with("row:"):
				var key_name := a.substr(4)
				for row in MATCH_ROWS + CONTROL_ROWS:''', '''			if a.begins_with("conn:"):
				join_game(a.substr(5))
			elif a.begins_with("key:"):
				var kk := a.substr(4)
				if kk == "DEL":
					ip_entry = ip_entry.substr(0, maxi(0, ip_entry.length() - 1))
				elif ip_entry.length() < 15:
					ip_entry += kk
			if a.begins_with("row:"):
				var key_name := a.substr(4)
				for row in MATCH_ROWS + CONTROL_ROWS + LAN_ROWS:''')
rep('''					cfg[key_name] = vals[(idx + 1) % vals.size()]''', '''					cfg[key_name] = vals[(idx + 1) % vals.size()]
					break''')

# ---------- human input: idle when not playing ----------
rep('''	var me: Player = players[my_idx]
	var inp: Dictionary = me.inp
	var mx :=''', '''	var me: Player = players[my_idx]
	var inp: Dictionary = me.inp
	if state != "play":
		for k2 in ["fly", "shoot", "swap", "grenade", "melee", "reload", "down", "zoom", "bomb"]:
			inp[k2] = false
		inp.mx = 0.0
		inp.pick = ""
		return
	var mx :=''')

# ---------- process loop ----------
rep('''	if state == "play":
		if autotest:
			for i in 40:''', '''	net_poll(delta)
	toast_t -= delta
	if state == "connecting":
		connect_t -= delta
		if connect_t <= 0:
			_on_conn_failed()
	lantest_tick(delta)
	shots_tick()
	if net_role != "" and (state == "play" or state == "paused"):
		if net_role == "client":
			update_client(dt)
		else:
			update_game(dt)
	elif state == "play":
		if autotest:
			for i in 40:''')
rep('''	if t >= match_time:
		state = "over"
		g_dir = 1.0
		g_target = 1.0
		jet_player.stop()''', '''	if net_role == "host":
		net_host_tick(dt)
	if t >= match_time:
		state = "over"
		g_dir = 1.0
		g_target = 1.0
		jet_player.stop()
		if net_role == "host":
			send_end()''')

# ---------- drawing dispatch ----------
rep('''	var in_menu := state == "menu" or state == "match_cfg" or state == "ctrl_cfg"''', '''	var in_menu: bool = MENU_STATES.has(state) or players.is_empty() or my_idx >= players.size()''')
rep('''		if state == "menu":
			draw_menu()
		elif state == "match_cfg":
			draw_cfg("MATCH SETTINGS", MATCH_ROWS)
		else:
			draw_cfg("CONTROLS", CONTROL_ROWS)
		return''', '''		match state:
			"match_cfg":
				draw_cfg("MATCH SETTINGS", MATCH_ROWS)
			"ctrl_cfg":
				draw_cfg("CONTROLS", CONTROL_ROWS)
			"lan":
				draw_lan()
			"lan_join":
				draw_join()
			"ipkey":
				draw_ipkey()
			"connecting":
				draw_connecting()
			"lobby":
				draw_lobby()
			"lan_cfg":
				draw_cfg("MATCH SETTINGS", LAN_ROWS, "lobby_back")
			_:
				draw_menu()
		draw_toast()
		return''')
rep('''	if state == "over":
		draw_over()
	elif state == "paused":
		draw_pause()''', '''	if state == "over":
		draw_over()
	elif state == "paused":
		draw_pause()
	draw_toast()''')

# menu buttons
rep('''	ui_button("PLAY", Rect2(x, y + 104 * u, bw, bh), "play", true)
	ui_button("MATCH SETTINGS", Rect2(x, y + 160 * u, bw, bh), "match")
	ui_button("CONTROLS", Rect2(x, y + 216 * u, bw, bh), "controls")''', '''	bh = 44 * u
	ui_button("PLAY VS BOTS", Rect2(x, y + 98 * u, bw, bh), "play", true)
	ui_button("PLAY WITH FRIENDS", Rect2(x, y + 150 * u, bw, bh), "lan", true)
	ui_button("MATCH SETTINGS", Rect2(x, y + 202 * u, bw, bh), "match")
	ui_button("CONTROLS", Rect2(x, y + 254 * u, bw, bh), "controls")''')

# cfg back action
rep('func draw_cfg(title: String, rows: Array) -> void:', 'func draw_cfg(title: String, rows: Array, back := "back") -> void:')
rep('''	ui_button("BACK", Rect2(r.position.x + w / 2 - 100 * u, r.end.y - 58 * u, 200 * u, 42 * u), "back", true)''',
    '''	ui_button("BACK", Rect2(r.position.x + w / 2 - 100 * u, r.end.y - 58 * u, 200 * u, 42 * u), back, true)''')

# pause in LAN
rep('''	txt("PAUSED", Vector2(r.get_center().x, r.position.y + 42 * u), 26 * u, C_ARC, 1, 4 * u)
	var bx := r.get_center().x - 110 * u''', '''	txt("PAUSED", Vector2(r.get_center().x, r.position.y + 42 * u), 26 * u, C_ARC, 1, 4 * u)
	var bx := r.get_center().x - 110 * u
	if net_role != "":
		txt("The match keeps going for your friends.", Vector2(r.get_center().x, r.position.y + 62 * u), 10 * u, C_MUTED, 1)
		ui_button("RESUME", Rect2(bx, r.position.y + 80 * u, 220 * u, 44 * u), "resume", true)
		ui_button("LEAVE MATCH", Rect2(bx, r.position.y + 140 * u, 220 * u, 44 * u), "leave")
		return''')

# over in LAN
rep('''	ui_button("PLAY AGAIN", Rect2(sw / 2 - 210 * u, r.end.y - 60 * u, 200 * u, 44 * u), "again", true)
	ui_button("MENU", Rect2(sw / 2 + 10 * u, r.end.y - 60 * u, 200 * u, 44 * u), "menu")''', '''	if net_role == "client":
		txt("Waiting for the host to start the next match...", Vector2(sw / 2 - 30 * u, r.end.y - 32 * u), 11 * u, C_MUTED, 1)
		ui_button("LEAVE", Rect2(r.end.x - 24 * u - 110 * u, r.end.y - 58 * u, 110 * u, 40 * u), "leave")
		return
	ui_button("PLAY AGAIN", Rect2(sw / 2 - 210 * u, r.end.y - 60 * u, 200 * u, 44 * u), "again", true)
	if net_role == "host":
		ui_button("LOBBY", Rect2(sw / 2 + 10 * u, r.end.y - 60 * u, 200 * u, 44 * u), "to_lobby")
	else:
		ui_button("MENU", Rect2(sw / 2 + 10 * u, r.end.y - 60 * u, 200 * u, 44 * u), "menu")''')

s += open("/home/claude/scripts/lan_block.gd").read()
open(P, "w").write(s)
print("ok")
