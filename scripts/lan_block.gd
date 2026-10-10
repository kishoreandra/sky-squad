
# =====================================================================
# LAN play: one phone hosts (runs the whole game), friends join and
# send their controls; the host sends back what is happening 20x a second.
# =====================================================================
func is_me(p) -> bool:
	return p != null and my_idx < players.size() and players[my_idx] == p

func me_fx(p, kind: String, a = 0) -> void:
	if p == null:
		return
	if is_me(p):
		apply_me_fx(kind, a)
	elif net_role == "host" and p.remote:
		net_fx.append(["m", players.find(p), kind, a])

func apply_me_fx(kind: String, a) -> void:
	match kind:
		"hurt":
			hurt_t = 0.35
			if t - last_buzz > 0.15:
				last_buzz = t
				buzz(25)
		"hit":
			hitmark_t = 0.15
		"buzz":
			buzz(int(a))
		"shake":
			shake = maxf(shake, float(a))
		"big":
			show_big(str(a))
		"snd":
			play_l(a[0], null, a[1], a[2] if a.size() > 2 else 0.08)
		"jetoff":
			jet_player.stop()

func add_tracer(tr: Dictionary) -> void:
	tracers.append(tr)
	if net_role == "host":
		net_fx.append(["t", tr.a, tr.b, tr.max, tr.kind])

func my_name() -> String:
	if str(cfg.name) == "":
		cfg.name = FUN_NAMES[randi() % FUN_NAMES.size()]
		save_cfg()
	return str(cfg.name)

func toast(msg: String) -> void:
	toast_msg = msg
	toast_t = 4.0

func blank_inp() -> Dictionary:
	return {"mx": 0.0, "fly": false, "shoot": false, "swap": false, "grenade": false, "melee": false, "reload": false, "aim": 0.0, "down": false, "pick": "", "zoom": false, "bomb": false}

func lan_ips() -> Array:
	var out := []
	for a in IP.get_local_addresses():
		var ip := str(a)
		if ip.contains(":") or ip.begins_with("127.") or ip.begins_with("169.254."):
			continue
		out.append(ip)
	out.sort_custom(func(x, y): return int(x.begins_with("192.168.")) > int(y.begins_with("192.168.")))
	return out

# where to ask "is anyone hosting?": broadcast, the hotspot phone (x.x.x.1), and this phone
func probe_targets() -> Array:
	var out := ["255.255.255.255", "127.0.0.1", "192.168.43.1"]
	for ip in lan_ips():
		var b: PackedStringArray = str(ip).split(".")
		if b.size() == 4:
			var pre := "%s.%s.%s." % [b[0], b[1], b[2]]
			for last in ["255", "1"]:
				if not out.has(pre + last) and pre + last != ip:
					out.append(pre + last)
	return out

func found_list() -> Array:
	var out := []
	for k in found_hosts.keys():
		if time_s - found_hosts[k].seen < 3.5:
			out.append(found_hosts[k])
	return out

func lobby_names() -> Array:
	if net_role == "host":
		var out := []
		for lp in lan_players:
			out.append(lp.name)
		return out
	return lobby_info.get("pl", [])

func host_game() -> void:
	net_close()
	var pe = ClassDB.instantiate("ENetMultiplayerPeer")
	if pe == null:
		toast("LAN play works in the Android app.")
		return
	var err: int = pe.create_server(NET_PORT, 7)
	if err != OK:
		toast("Could not start hosting. Close other copies of the game and try again.")
		return
	multiplayer.multiplayer_peer = pe
	net_role = "host"
	my_idx = 0
	lan_players = [{"peer": 1, "name": my_name()}]
	disc = PacketPeerUDP.new()
	disc.set_broadcast_enabled(true)
	disc.bind(DISC_PORT)
	state = "lobby"

func join_game(ip: String) -> void:
	net_close()
	ip = ip.strip_edges()
	if not ip.is_valid_ip_address():
		toast("That address doesn't look right. Example: 192.168.43.1")
		return
	var pe = ClassDB.instantiate("ENetMultiplayerPeer")
	if pe == null:
		toast("LAN play works in the Android app.")
		return
	var err: int = pe.create_client(ip, NET_PORT)
	if err != OK:
		toast("Could not join %s" % ip)
		return
	multiplayer.multiplayer_peer = pe
	net_role = "client"
	join_ip = ip
	lobby_info = {}
	connect_t = 7.0
	state = "connecting"

func net_close() -> void:
	if net_role != "" and multiplayer.multiplayer_peer != null:
		multiplayer.multiplayer_peer.close()
	multiplayer.multiplayer_peer = OfflineMultiplayerPeer.new()
	if disc != null:
		disc.close()
		disc = null
	if not stash.is_empty():
		cfg.mode = stash.mode
		cfg.zones = stash.zones
		stash = {}
	net_role = ""
	lan_players = []
	my_idx = 0
	pending_start = false
	net_fx = []
	tile_dirty.clear()
	if jet_player != null:
		jet_player.stop()

func _on_peer_gone(id: int) -> void:
	if net_role != "host":
		return
	var gone := false
	for i in range(lan_players.size() - 1, -1, -1):
		if int(lan_players[i].peer) == id:
			lan_players.remove_at(i)
			gone = true
	for p in players:
		if p.remote and p.peer_id == id:
			p.remote = false
			p.bot = true
			p.style = "balanced"
			p.st = make_style("balanced")
			p.inp = blank_inp()
			p.prev = p.inp.duplicate()
			feed.push_front({"k": "", "kc": C_INK, "v": "%s left. A bot took over." % p.pname, "vc": C_ARC, "gun": "", "head": false, "t": 4.0, "note": ""})
	if gone:
		send_lobby()

func _on_connected() -> void:
	rpc_id(1, "c_hello", my_name(), VERSION)
	state = "lobby"

func _on_conn_failed() -> void:
	net_close()
	state = "lan_join"
	toast("Could not join. Are you connected to the host's hotspot?")

func _on_server_gone() -> void:
	net_close()
	state = "lan"
	toast("The host closed the game.")
	if lantest_join != "":
		print("CLIENT: host went away")
		get_tree().quit()

# ---------- messages ----------
@rpc("any_peer", "call_remote", "reliable")
func c_hello(nm, ver) -> void:
	if net_role != "host":
		return
	var id := multiplayer.get_remote_sender_id()
	if str(ver) != VERSION:
		rpc_id(id, "s_reject", "Different game version. Install the same Sky Squad on every phone.")
		return
	if not ["lobby", "lan_cfg", "over"].has(state):
		rpc_id(id, "s_reject", "A match is running. Try again when it ends.")
		return
	if lan_players.size() >= 6:
		rpc_id(id, "s_reject", "This game is full (6 players).")
		return
	var base := str(nm).substr(0, 12)
	var pick := base
	var n := 2
	while lobby_names().has(pick):
		pick = "%s%d" % [base, n]
		n += 1
	lan_players.append({"peer": id, "name": pick})
	play_l("pickup", null, -6.0)
	send_lobby()

@rpc("authority", "call_remote", "reliable")
func s_reject(msg) -> void:
	net_close()
	state = "lan"
	toast(str(msg))

func send_lobby(go := false) -> void:
	if net_role != "host":
		return
	var info := {"pl": lobby_names(), "mode": cfg.mode, "bots": clampi(int(cfg.lan_bots), 0, 6 - lan_players.size()), "skill": cfg.skill, "min": cfg.minutes, "go": go}
	rpc("s_lobby", info)

@rpc("authority", "call_remote", "reliable")
func s_lobby(info) -> void:
	if net_role != "client":
		return
	lobby_info = info
	if state == "connecting" or (info.get("go", false) and (state == "over" or state == "paused")):
		state = "lobby"

func start_lan_match() -> void:
	if net_role != "host":
		return
	reset_match()
	if lantest_host:
		players[0].bot = true
	state = "play"
	snap_t = 0.0
	for i in players.size():
		var p: Player = players[i]
		if p.remote:
			rpc_id(p.peer_id, "s_start", start_info(i))

func start_info(idx: int) -> Dictionary:
	var pl := []
	for p in players:
		pl.append([p.pname, p.team, p.color, p.side, p.bot])
	return {"idx": idx, "tiles": tiles, "pl": pl, "mode": cfg.mode, "zones": cfg.zones, "mt": match_time}

@rpc("authority", "call_remote", "reliable")
func s_start(info) -> void:
	if net_role != "client":
		return
	if stash.is_empty():
		stash = {"mode": cfg.mode, "zones": cfg.zones}
	cfg.mode = info.mode
	cfg.zones = info.zones
	gen_map()
	tiles = info.tiles
	for i in tiles.size():
		thp[i] = TILE_HP.get(tiles[i], 99.0)
	t = 0.0
	g_dir = 1.0
	g_target = 1.0
	water_y = WH
	ev = null
	shake = 0.0
	big_t = 0.0
	match_time = info.mt
	for arr in [bullets, grenades_list, parts, pickups, blocks, corpses, feed, tracers]:
		arr.clear()
	players.clear()
	var pl: Array = info.pl
	for i in pl.size():
		var d: Array = pl[i]
		var p := Player.new()
		p.id = i
		p.pname = d[0]
		p.team = d[1]
		p.color = d[2]
		p.side = d[3]
		p.bot = d[4]
		p.slots = [full_slot("uzi"), full_slot("magnum")]
		players.append(p)
	my_idx = int(info.idx)
	cam = Vector2.ZERO
	in_t = 0.0
	snaps_got = 0
	pending_start = true

func slot_enc(w) -> Array:
	if w == null:
		return []
	return [w.type, w.mag, w.spare, w.zi, w.get("dual", false)]

func slot_dec(a):
	if a == null or a.size() < 5:
		return null
	return {"type": a[0], "mag": a[1], "spare": a[2], "zi": a[3], "dual": a[4]}

func build_snap() -> Dictionary:
	var pl := []
	for p in players:
		var fl := (1 if p.alive else 0) | (2 if p.jet_on else 0) | (4 if p.on_ground else 0) | (8 if p.in_water else 0)
		pl.append([p.x, p.y, p.vx, p.vy, p.aim, p.hp, p.fuel, fl, p.posture, p.cur, [slot_enc(p.slots[0]), slot_enc(p.slots[1])],
			p.grenades, p.bombs, maxf(p.stun_t, 0.0), maxf(p.net_t, 0.0), maxf(p.protect_t, 0.0), maxf(p.reload_t, 0.0), p.reload_total,
			p.kills, p.deaths, p.respawn_t, p.say if p.say_t > 0 else "", maxf(p.say_t, 0.0), maxf(p.switch_t, 0.0), maxf(p.melee_anim, 0.0), maxf(p.flash, 0.0),
			players.find(p.last_hit_by) if p.last_hit_by != null else -1])
	var b := PackedFloat32Array()
	for x in bullets:
		b.append_array([x.x, x.y, x.vx, x.vy, 1.0 if x.rocket else (2.0 if x.net else 0.0)])
	var g := PackedFloat32Array()
	for x in grenades_list:
		g.append_array([x.x, x.y, x.vx, x.vy, x.rot, x.fuse, 1.0 if x.kind == "bomb" else 0.0, 1.0 if x.stuck else 0.0])
	var k := []
	for x in pickups:
		k.append([x.type, x.gun, x.x, x.y])
	var bl := PackedFloat32Array()
	for x in blocks:
		bl.append_array([x.c, x.y, x.vy])
	var e := []
	if ev != null:
		e = [ev.name, ev.phase, ev.t, ev.dur, ev.spawned, ev.cols, ev.tiles]
	return {"t": t, "wy": water_y, "g": g_dir, "pl": pl, "b": b, "gr": g, "k": k, "bl": bl, "ev": e, "feed": feed, "fx": net_fx}

func net_host_tick(dt: float) -> void:
	snap_t += dt
	if snap_t < 0.05:
		return
	snap_t = 0.0
	if not tile_dirty.is_empty():
		var idx := PackedInt32Array()
		var vals := PackedByteArray()
		var hps := PackedFloat32Array()
		for i in tile_dirty.keys():
			idx.append(i)
			vals.append(tiles[i])
			hps.append(thp[i])
		tile_dirty.clear()
		rpc("s_tiles", idx, vals, hps)
	rpc("s_snap", build_snap())
	net_fx = []
	snaps_sent += 1

@rpc("authority", "call_remote", "reliable")
func s_tiles(idx, vals, hps) -> void:
	if net_role != "client" or tiles.size() != COLS * ROWS:
		return
	for j in idx.size():
		tiles[idx[j]] = vals[j]
		thp[idx[j]] = hps[j]
	tiles_got += idx.size()

@rpc("authority", "call_remote", "unreliable_ordered", 1)
func s_snap(d) -> void:
	if net_role != "client" or not (pending_start or state == "play" or state == "paused"):
		return
	var pl: Array = d.pl
	if pl.size() != players.size():
		return
	snaps_got += 1
	t = d.t
	water_y = d.wy
	g_dir = d.g
	for i in pl.size():
		var a: Array = pl[i]
		var p: Player = players[i]
		var was_alive := p.alive
		p.nx = a[0]
		p.ny = a[1]
		p.vx = a[2]
		p.vy = a[3]
		p.naim = a[4]
		p.hp = a[5]
		p.fuel = a[6]
		var fl := int(a[7])
		p.alive = (fl & 1) != 0
		p.jet_on = (fl & 2) != 0
		p.on_ground = (fl & 4) != 0
		p.in_water = (fl & 8) != 0
		var post: String = a[8]
		if post != p.posture:
			p.posture = post
			var sz: Vector2 = POSTURE[post]
			p.w = sz.x
			p.h = sz.y
		p.cur = a[9]
		p.slots = [slot_dec(a[10][0]), slot_dec(a[10][1])]
		p.grenades = a[11]
		p.bombs = a[12]
		p.stun_t = a[13]
		p.net_t = a[14]
		p.protect_t = a[15]
		p.reload_t = a[16]
		p.reload_total = a[17]
		p.kills = a[18]
		p.deaths = a[19]
		p.respawn_t = a[20]
		p.say = a[21]
		p.say_t = a[22]
		if a[23] > p.switch_t + 0.04:
			p.switch_t = a[23]
		if a[24] > p.melee_anim + 0.04:
			p.melee_anim = a[24]
		if a[25] > p.flash + 0.03:
			p.flash = a[25]
		var lh := int(a[26])
		p.last_hit_by = players[lh] if lh >= 0 and lh < players.size() else null
		p.snap_age = 0.0
		if (p.alive and not was_alive) or snaps_got == 1 or Vector2(p.x - p.nx, p.y - p.ny).length() > 160:
			p.x = p.nx
			p.y = p.ny
			if i == my_idx and snaps_got == 1:
				p.aim = p.naim
				last_touch_aim = p.naim
	bullets.clear()
	var bb: PackedFloat32Array = d.b
	for j in range(0, bb.size(), 5):
		var b := Bullet.new()
		b.x = bb[j]
		b.y = bb[j + 1]
		b.vx = bb[j + 2]
		b.vy = bb[j + 3]
		b.rocket = bb[j + 4] == 1.0
		b.net = bb[j + 4] == 2.0
		bullets.append(b)
	grenades_list.clear()
	var gg: PackedFloat32Array = d.gr
	for j in range(0, gg.size(), 8):
		var g := Grenade.new()
		g.x = gg[j]
		g.y = gg[j + 1]
		g.vx = gg[j + 2]
		g.vy = gg[j + 3]
		g.rot = gg[j + 4]
		g.fuse = gg[j + 5]
		g.kind = "bomb" if gg[j + 6] == 1.0 else "frag"
		g.stuck = gg[j + 7] == 1.0
		grenades_list.append(g)
	pickups.clear()
	for kd in d.k:
		pickups.append(make_pickup(kd[0], kd[2], kd[3], kd[1]))
	blocks.clear()
	var bl: PackedFloat32Array = d.bl
	for j in range(0, bl.size(), 3):
		var blk := Block.new()
		blk.c = int(bl[j])
		blk.y = bl[j + 1]
		blk.vy = bl[j + 2]
		blocks.append(blk)
	var e: Array = d.ev
	if e.is_empty():
		ev = null
	else:
		if ev == null:
			ev = Ev.new()
		ev.name = e[0]
		ev.phase = e[1]
		ev.t = e[2]
		ev.dur = e[3]
		ev.spawned = e[4]
		ev.cols = e[5]
		ev.tiles = e[6]
	feed = d.feed
	for fx in d.fx:
		apply_fx(fx)
	if pending_start:
		pending_start = false
		state = "play"

func apply_fx(e: Array) -> void:
	var kind := str(e[0])
	fx_count[kind] = fx_count.get(kind, 0) + 1
	match kind:
		"s":
			play_l(e[1], e[2], e[3])
		"d":
			debris(e[1], e[2], e[3], e[4])
		"k":
			sparks(e[1], e[2], e[3], e[4], e[5])
		"b":
			blood(e[1], e[2], e[3])
		"x":
			explode_fx(e[1], e[2], e[3])
		"f":
			if int(e[1]) < players.size():
				fire_fx(players[e[1]], e[2], e[3])
		"t":
			tracers.append({"a": e[1], "b": e[2], "t": e[3], "max": e[3], "kind": e[4]})
		"c":
			var cp := Corpse.new()
			cp.x = e[1]
			cp.y = e[2]
			cp.vx = e[3]
			cp.vy = e[4]
			cp.spin = e[5]
			cp.team = e[6]
			cp.face = e[7]
			corpses.append(cp)
		"m":
			if int(e[1]) == my_idx:
				apply_me_fx(e[2], e[3])

func send_end() -> void:
	var k := []
	var dd := []
	for p in players:
		k.append(p.kills)
		dd.append(p.deaths)
	rpc("s_end", {"k": k, "d": dd})

@rpc("authority", "call_remote", "reliable")
func s_end(info) -> void:
	if net_role != "client":
		return
	for i in mini(players.size(), info.k.size()):
		players[i].kills = info.k[i]
		players[i].deaths = info.d[i]
	state = "over"
	jet_player.stop()
	client_jet = false
	if lantest_join != "" and lt_done == 0.0:
		lt_done = time_s
		var me: Player = players[my_idx]
		print("CLIENT snaps=%d tile_updates=%d players=%d me=%s idx=%d kills=%d deaths=%d moved=%d" % [snaps_got, tiles_got, players.size(), me.pname, my_idx, me.kills, me.deaths, int(lt_moved)])
		print("CLIENT fx: ", fx_count)

@rpc("any_peer", "call_remote", "unreliable_ordered", 1)
func c_input(a) -> void:
	if net_role != "host" or typeof(a) != TYPE_ARRAY or a.size() < 12:
		return
	var id := multiplayer.get_remote_sender_id()
	for p in players:
		if p.remote and p.peer_id == id:
			var inp: Dictionary = p.inp
			inp.mx = clampf(float(a[0]), -1.0, 1.0)
			inp.fly = bool(a[1])
			inp.shoot = bool(a[2])
			inp.swap = bool(a[3])
			inp.grenade = bool(a[4])
			inp.melee = bool(a[5])
			inp.reload = bool(a[6])
			inp.aim = float(a[7])
			inp.down = bool(a[8])
			inp.pick = str(a[9])
			inp.zoom = bool(a[10])
			inp.bomb = bool(a[11])
			inputs_got += 1
			return

# the joining phone: read controls, send them, and smoothly show what the host sent
func update_client(dt: float) -> void:
	if pending_start or players.is_empty() or my_idx >= players.size():
		return
	var me: Player = players[my_idx]
	human_input()
	if pick_request != "":
		latch_pick = pick_request
		latch_pick_t = 0.25
	if zoom_request:
		latch_zoom_t = 0.15
	pick_request = ""
	zoom_request = false
	latch_pick_t -= dt
	latch_zoom_t -= dt
	if latch_pick_t > 0 and me.inp.pick == "":
		me.inp.pick = latch_pick
	if latch_zoom_t > 0:
		me.inp.zoom = true
	if lantest_join != "":
		test_input(me)
	if me.alive:
		var diff := wrapf(me.inp.aim - me.aim, -PI, PI)
		var stepmax: float = aim_rate(mouse_aiming()) * dt
		me.aim = wrapf(me.aim + clampf(diff, -stepmax, stepmax), -PI, PI)
	in_t += dt
	if in_t >= 1.0 / 30.0:
		in_t = 0.0
		var i2: Dictionary = me.inp
		rpc_id(1, "c_input", [i2.mx, i2.fly, i2.shoot, i2.swap, i2.grenade, i2.melee, i2.reload, me.aim, i2.down, i2.pick, i2.zoom, i2.bomb])
	var old_me := Vector2(me.x, me.y)
	for i in players.size():
		var p: Player = players[i]
		p.snap_age += dt
		p.say_t -= dt
		p.muzzle_t -= dt
		p.flash -= dt
		p.melee_anim -= dt
		p.switch_t -= dt
		p.protect_t -= dt
		p.respawn_t -= dt
		p.stun_t -= dt
		p.net_t -= dt
		p.reload_t = maxf(0.0, p.reload_t - dt)
		p.recoil = maxf(0.0, p.recoil - dt * 40)
		if not p.alive:
			continue
		var age := minf(p.snap_age, 0.12)
		var k := ease_k(18.0, dt)
		p.x += (p.nx + p.vx * age - p.x) * k
		p.y += (p.ny + p.vy * age - p.y) * k
		if i != my_idx:
			p.aim = lerp_angle(p.aim, p.naim, ease_k(16.0, dt))
		if p.on_ground:
			p.walk += absf(p.vx) * dt * (0.05 if p.posture == "stand" else 0.09)
		animate(p, dt)
		if p.jet_on and randf() < 0.55:
			var c := center(p)
			var face := 1.0 if cos(p.aim) >= 0 else -1.0
			var nz := c + Vector2(-9 * face, 10 * gsign())
			add_part(nz.x + randf_range(-3, 3), nz.y, randf_range(-20, 20), gsign() * randf_range(90, 160), 0.5, Color(0.85, 0.85, 0.88, 0.45), 6, -0.02, "smoke", 18)
	lt_moved += Vector2(me.x, me.y).distance_to(old_me)
	if me.alive and me.jet_on and not client_jet and lantest_join == "":
		jet_player.play()
	elif client_jet and not (me.alive and me.jet_on):
		jet_player.stop()
	client_jet = me.alive and me.jet_on
	for b in bullets:
		b.x += b.vx * dt
		b.y += b.vy * dt
		if b.rocket and randf() < 0.5:
			add_part(b.x, b.y, randf_range(-20, 20), randf_range(-20, 20), 0.7, Color(0.8, 0.8, 0.8, 0.5), 6, -0.03, "smoke", 18)
	for g in grenades_list:
		g.fuse -= dt
		if not g.stuck:
			g.x += g.vx * dt
			g.y += g.vy * dt
			g.rot += g.vx * dt * 0.05
	for blk in blocks:
		blk.y += blk.vy * dt
	update_parts(dt)
	for tr in tracers:
		tr.t -= dt
	tracers = tracers.filter(func(tr): return tr.t > 0)
	shake = maxf(0.0, shake - dt * 30)
	big_t -= dt
	hurt_t -= dt
	hitmark_t -= dt

# discovery: the host answers "SKYSQ?" with its name; joiners keep asking around
func net_poll(dt: float) -> void:
	if OS.has_feature("web"):
		return
	if net_role == "host" and disc != null:
		while disc.get_available_packet_count() > 0:
			var data := disc.get_packet()
			var ip := disc.get_packet_ip()
			var port := disc.get_packet_port()
			if data.get_string_from_utf8() == "SKYSQ?" and ip != "":
				var st := "lobby" if ["lobby", "lan_cfg", "over"].has(state) else "playing"
				disc.set_dest_address(ip, port)
				disc.put_packet(("SKYSQ!|%s|%d|%s|%s" % [my_name(), lan_players.size(), st, VERSION]).to_utf8_buffer())
	if state == "lan_join":
		if probe == null:
			probe = PacketPeerUDP.new()
			probe.set_broadcast_enabled(true)
			probe.bind(0)
		probe_t -= dt
		if probe_t <= 0:
			probe_t = 0.8
			for addr in probe_targets():
				probe.set_dest_address(addr, DISC_PORT)
				probe.put_packet("SKYSQ?".to_utf8_buffer())
		while probe.get_available_packet_count() > 0:
			var msg := probe.get_packet().get_string_from_utf8()
			var ip2 := probe.get_packet_ip()
			var bits := msg.split("|")
			if bits.size() >= 5 and bits[0] == "SKYSQ!":
				var key := bits[1]
				var old = found_hosts.get(key)
				if old != null and not str(old.ip).begins_with("127.") and ip2.begins_with("127."):
					ip2 = old.ip
				found_hosts[key] = {"ip": ip2, "name": bits[1], "n": int(bits[2]), "st": bits[3], "ver": bits[4], "seen": time_s}
	elif probe != null:
		probe.close()
		probe = null

# ---------- LAN screens ----------
func draw_toast() -> void:
	if toast_t <= 0:
		return
	var a := clampf(toast_t, 0, 1)
	var tw := font.get_string_size(toast_msg, 0, -1, int(13 * u)).x + 30 * u
	var r := Rect2(sw / 2 - tw / 2, sh - 64 * u, tw, 34 * u)
	rbox(r, Color(0.55, 0.08, 0.16, 0.92 * a), 10 * u)
	txt(toast_msg, Vector2(sw / 2, r.position.y + 22 * u), 13 * u, Color(1, 1, 1, a), 1)

func draw_lan() -> void:
	var w := minf(sw - 32 * u, 640 * u)
	var h := minf(sh - 24 * u, 330 * u)
	var r := panel(w, h)
	var x := r.position.x + 26 * u
	var y := r.position.y
	txt("PLAY WITH FRIENDS", Vector2(x, y + 42 * u), 26 * u, C_ARC, 0, 4 * u)
	txt("Phones close together. No internet needed.", Vector2(x, y + 64 * u), 11 * u, C_MUTED)
	var bw := 230 * u
	var bh := 44 * u
	ui_button("HOST A GAME", Rect2(x, y + 84 * u, bw, bh), "host", true)
	ui_button("JOIN A GAME", Rect2(x, y + 136 * u, bw, bh), "join", true)
	ui_button("NAME: " + my_name(), Rect2(x, y + 188 * u, bw, bh), "name")
	ui_button("BACK", Rect2(x, y + 240 * u, bw, bh), "back")
	var rx := x + bw + 28 * u
	var lines := [
		"HOW IT WORKS",
		"1. One phone turns on its Wi-Fi hotspot",
		"    and taps HOST A GAME.",
		"2. Friends connect to that hotspot,",
		"    then tap JOIN A GAME.",
		"3. The host taps START. Bots fill the",
		"    empty places (up to 6 players).",
		"",
		"Same home Wi-Fi works too.",
		"Tap NAME to change your name.",
	]
	for i in lines.size():
		var head: bool = i == 0
		txt(lines[i], Vector2(rx, y + 100 * u + i * 19 * u), (10 if head else 12) * u, C_CYAN if head else C_MUTED)

func draw_join() -> void:
	var w := minf(sw - 32 * u, 600 * u)
	var h := minf(sh - 24 * u, 330 * u)
	var r := panel(w, h)
	var x := r.position.x + 26 * u
	var y := r.position.y
	txt("JOIN A GAME", Vector2(x, y + 42 * u), 26 * u, C_ARC, 0, 4 * u)
	var list := found_list()
	var dots := ".".repeat(int(time_s * 2.0) % 4)
	if list.is_empty():
		txt("Looking for games" + dots, Vector2(x, y + 92 * u), 16 * u, C_INK)
		txt("1. Connect this phone to the host's Wi-Fi hotspot.", Vector2(x, y + 124 * u), 12 * u, C_MUTED)
		txt("2. The host must be on the LOBBY screen.", Vector2(x, y + 144 * u), 12 * u, C_MUTED)
		txt("Can't find it? Tap TYPE ADDRESS and enter the", Vector2(x, y + 176 * u), 12 * u, C_MUTED)
		txt("number shown on the host's LOBBY screen.", Vector2(x, y + 196 * u), 12 * u, C_MUTED)
	else:
		txt("Tap a game to join" + dots, Vector2(x, y + 70 * u), 12 * u, C_MUTED)
		for i in mini(list.size(), 3):
			var hg: Dictionary = list[i]
			var lab := "%s's game   %d/6" % [hg.name, hg.n]
			if hg.ver != VERSION:
				lab += "   (needs update)"
			elif hg.st == "playing":
				lab += "   (playing now)"
			ui_button(lab, Rect2(x, y + (84 + i * 52) * u, w - 52 * u, 44 * u), "conn:" + str(hg.ip), i == 0)
	ui_button("TYPE ADDRESS", Rect2(x, r.end.y - 58 * u, 200 * u, 42 * u), "ipkey")
	ui_button("BACK", Rect2(r.end.x - 26 * u - 150 * u, r.end.y - 58 * u, 150 * u, 42 * u), "to_lan")

func draw_ipkey() -> void:
	var w := minf(sw - 32 * u, 540 * u)
	var h := minf(sh - 24 * u, 330 * u)
	var r := panel(w, h)
	var x := r.position.x + 26 * u
	var y := r.position.y
	txt("TYPE HOST ADDRESS", Vector2(x, y + 40 * u), 22 * u, C_ARC, 0, 4 * u)
	txt("The host can see it on their LOBBY screen.", Vector2(x, y + 60 * u), 11 * u, C_MUTED)
	var fr := Rect2(x, y + 72 * u, 236 * u, 40 * u)
	rbox(fr, Color(0.02, 0.03, 0.08, 0.9), 8 * u)
	var caret := "|" if fmod(time_s, 1.0) < 0.5 else ""
	txt(ip_entry + caret, fr.position + Vector2(12 * u, 27 * u), 20 * u, C_INK)
	var keys := [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"], [".", "0", "DEL"]]
	var kw := 74 * u
	var kh := 42 * u
	for rr in keys.size():
		for cc in 3:
			var kname: String = keys[rr][cc]
			ui_button(kname, Rect2(x + cc * (kw + 7 * u), y + 120 * u + rr * (kh + 6 * u), kw, kh), "key:" + kname)
	var rx := x + 3 * (kw + 7 * u) + 18 * u
	var bw2 := r.end.x - 26 * u - rx
	ui_button("JOIN", Rect2(rx, y + 120 * u, bw2, 90 * u), "ipjoin", true)
	ui_button("BACK", Rect2(rx, y + 216 * u, bw2, 42 * u), "join")

func draw_connecting() -> void:
	var r := panel(minf(sw - 32 * u, 420 * u), minf(sh - 24 * u, 200 * u))
	var dots := ".".repeat(int(time_s * 2.0) % 4)
	txt("Joining " + join_ip + dots, Vector2(r.get_center().x, r.position.y + 70 * u), 18 * u, C_INK, 1)
	ui_button("CANCEL", Rect2(r.get_center().x - 90 * u, r.end.y - 66 * u, 180 * u, 44 * u), "cancel")

func draw_lobby() -> void:
	var w := minf(sw - 32 * u, 660 * u)
	var h := minf(sh - 24 * u, 340 * u)
	var r := panel(w, h)
	var x := r.position.x + 26 * u
	var y := r.position.y
	var host := net_role == "host"
	txt("LOBBY", Vector2(x, y + 42 * u), 26 * u, C_ARC, 0, 4 * u)
	txt("You are hosting" if host else "Joined " + join_ip, Vector2(x + 110 * u, y + 40 * u), 12 * u, C_CYAN)
	var names := lobby_names()
	txt("PLAYERS", Vector2(x, y + 74 * u), 10 * u, C_CYAN)
	for i in names.size():
		var yy := y + 96 * u + i * 22 * u
		draw_circle(Vector2(x + 6 * u, yy - 5 * u), 6 * u, TEAM_COL[i % TEAM_COL.size()])
		var tag := "  (host)" if i == 0 else ""
		txt(str(names[i]) + tag, Vector2(x + 20 * u, yy), 15 * u, C_ARC if (host and i == 0) else C_INK)
	var nb: int = clampi(int(cfg.lan_bots), 0, 6 - names.size()) if host else int(lobby_info.get("bots", 0))
	if nb > 0:
		txt("+ %d bot%s" % [nb, "s" if nb > 1 else ""], Vector2(x + 20 * u, y + 96 * u + names.size() * 22 * u), 13 * u, C_MUTED)
	var rx := x + 250 * u
	var mode: String = cfg.mode if host else str(lobby_info.get("mode", "ffa"))
	var mins: int = int(cfg.minutes) if host else int(lobby_info.get("min", 5))
	txt("MATCH", Vector2(rx, y + 74 * u), 10 * u, C_CYAN)
	txt(("Teams: Blue vs Red" if mode == "team" else "Free for all") + "  /  %d min" % mins, Vector2(rx, y + 96 * u), 13 * u, C_INK)
	if host:
		var ips := lan_ips()
		txt("Friends: join the hotspot, tap JOIN A GAME.", Vector2(rx, y + 124 * u), 11 * u, C_MUTED)
		txt("Or type this address:", Vector2(rx, y + 142 * u), 11 * u, C_MUTED)
		txt(", ".join(PackedStringArray(ips.slice(0, 2))) if not ips.is_empty() else "(turn on hotspot or Wi-Fi)", Vector2(rx, y + 166 * u), 18 * u, C_ARC, 0, 3 * u)
		var bw := (r.end.x - 26 * u - rx - 10 * u) / 2.0
		ui_button("START", Rect2(rx, y + 190 * u, bw * 2 + 10 * u, 48 * u), "start", true)
		ui_button("SETTINGS", Rect2(rx, y + 246 * u, bw, 42 * u), "lan_cfg")
		ui_button("LEAVE", Rect2(rx + bw + 10 * u, y + 246 * u, bw, 42 * u), "leave")
	else:
		var dots := ".".repeat(int(time_s * 2.0) % 4)
		txt("Waiting for the host to start" + dots, Vector2(rx, y + 140 * u), 14 * u, C_INK)
		ui_button("LEAVE", Rect2(rx, y + 246 * u, 160 * u, 42 * u), "leave")

# ---------- LAN test hooks (two copies on one computer) ----------
func test_input(me: Player) -> void:
	var best = null
	var bd := 1e9
	var c := center(me)
	for o in players:
		if o != me and o.alive and enemy(me, o):
			var d := center(o).distance_to(c)
			if d < bd:
				bd = d
				best = o
	var inp: Dictionary = me.inp
	if best != null:
		var oc := center(best)
		inp.aim = atan2(oc.y - c.y, oc.x - c.x)
		inp.shoot = bd < 650
		inp.mx = signf(oc.x - c.x) if bd > 180 else 0.0
	inp.fly = fmod(time_s, 3.0) < 1.1
	inp.swap = fmod(time_s, 9.0) < 0.1
	inp.grenade = fmod(time_s, 7.0) < 0.1
	inp.pick = "first" if fmod(time_s, 5.0) < 0.3 else ""

func lantest_tick(dt: float) -> void:
	if lantest_host:
		if state == "lobby":
			if lan_players.size() >= 2 or time_s > 40.0:
				lt_wait += dt
				if lt_wait > 3.0:
					start_lan_match()
		elif state == "over" and lt_done == 0.0:
			lt_done = time_s
			print("HOST snaps_sent=%d inputs_got=%d" % [snaps_sent, inputs_got])
			for p in players:
				print("  %s bot=%s remote=%s kills=%d deaths=%d" % [p.pname, p.bot, p.remote, p.kills, p.deaths])
		if lt_done > 0 and time_s - lt_done > 4.0:
			get_tree().quit()
	if lantest_join == "auto" and state == "lan_join":
		var fl := found_list()
		if not fl.is_empty():
			lt_wait += dt
			if lt_wait > 3.5:
				print("CLIENT found: ", fl)
				do_action("conn:" + str(fl[0].ip))
	if lantest_join != "" and lt_done > 0 and time_s - lt_done > 3.0:
		get_tree().quit()

func shots_tick() -> void:
	if lan_shots.is_empty():
		return
	var spec: Array = lan_shots[0]
	var trig := str(spec[0])
	var ok := false
	match trig:
		"lobby":
			ok = state == "lobby" and lobby_names().size() >= 2
		"join":
			ok = state == "lan_join" and not found_list().is_empty()
		"over":
			ok = state == "over"
		_:
			ok = state == "play" and t >= float(trig)
	if not ok:
		shot_wait = 0
		return
	shot_wait += 1
	if shot_wait > 12:
		get_viewport().get_texture().get_image().save_png("res://shots/%s.png" % spec[1])
		print("shot saved: ", spec[1])
		lan_shots.pop_front()
		shot_wait = 0
		if lan_shots.is_empty() and shots_quit:
			get_tree().quit()
