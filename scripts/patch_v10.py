"""v1.0 sounds: round-2 picks wired in, plus looping map backgrounds, underwater and torch loops."""
import sys
P = "/home/claude/skysquad/main.gd"
s = open(P).read()

def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        sys.exit(f"expected {count} got {n}: {old[:100]!r}")
    s = s.replace(old, new)

rep('# Sky Squad - Arc Light Studio. Playtest build 0.9', '# Sky Squad - Arc Light Studio. Playtest build 1.0')
rep('const VERSION := "0.9"', 'const VERSION := "1.0"')
rep('''"tink", "ui_ok", "bomb_boom", "jetstart", "locked", "wdrop", "equip2"]:''', '''"tink", "ui_ok", "bomb_boom", "jetstart", "locked", "wdrop", "equip2",
			"jump", "ui_click", "wpick", "ev_water", "ev_rocks", "ev_brk", "ev_flip", "crate", "match_end", "lost_lead", "item_respawn", "low_fuel"]:''')

# loops: background per map, underwater, torch
rep('''	jet_player = AudioStreamPlayer.new()
	jet_player.stream = jet
	jet_player.volume_db = -14
	add_child(jet_player)''', '''	jet_player = AudioStreamPlayer.new()
	jet_player.stream = jet
	jet_player.volume_db = -14
	add_child(jet_player)
	for ln in ["water_loop", "amb_sky", "amb_outpost", "amb_catacombs", "torch_loop"]:
		var st: AudioStreamWAV = load("res://sfx/%s.wav" % ln)
		st.loop_mode = AudioStreamWAV.LOOP_FORWARD
		st.loop_begin = 0
		st.loop_end = st.data.size() / 2
		loops[ln] = st
	for pn in ["amb", "water", "torch"]:
		var ap := AudioStreamPlayer.new()
		ap.volume_db = -80
		add_child(ap)
		loop_players[pn] = ap''')
rep('''var heart_t := 0.0''', '''var loops := {}
var loop_players := {}
var heart_t := 0.0''')

# jump off the ground vs. jet ignition in the air
rep('''			if p.on_ground:
				p.vy = -gsign() * S.jump_speed''', '''			if p.on_ground:
				p.vy = -gsign() * S.jump_speed
				if not was_jet:
					p.jst_t = t
					play("jump", c, -5.0 if is_me(p) else -12.0, 0.05)''')

# menu clicks
rep('''play_l("ui_ok" if BIG_ACTIONS.has(b.a) else "swap", null, -6.0 if BIG_ACTIONS.has(b.a) else -10.0, 0.0)''', '''play_l("ui_ok" if BIG_ACTIONS.has(b.a) else "ui_click", null, -6.0 if BIG_ACTIONS.has(b.a) else -8.0, 0.0)''')

# gun pick up has its own sound; dual plays the equip sound instead
rep('''				apply_pick(p, found, opt)
				me_fx(p, "snd", ["pickup", -6.0])''', '''				apply_pick(p, found, opt)
				if opt != "dual":
					me_fx(p, "snd", ["wpick", -5.0])''')
rep('''				me_fx(p, "snd", ["health" if k.type == "health" else "pickup", -6.0])''', '''				me_fx(p, "snd", ["health" if k.type == "health" else ("wpick" if (k.type == "gun" or k.type == "drop") else "pickup"), -6.0])''')

# event warnings
rep('''	play("warn", null, -10.0, 0.0)''', '''	play({"water": "ev_water", "roof": "ev_rocks", "brk": "ev_brk", "flip": "ev_flip"}.get(ev.name, "warn"), null, -4.0, 0.0)''')

# crates
rep('''	if thp[i] <= 0:
		tiles[i] = EMPTY
		debris((c + 0.5) * T, (r + 0.5) * T, 6, v)''', '''	if thp[i] <= 0:
		tiles[i] = EMPTY
		debris((c + 0.5) * T, (r + 0.5) * T, 6, v)
		if v == CRATE or v == WOOD:
			play("crate", Vector2((c + 0.5) * T, (r + 0.5) * T), -6.0 if v == CRATE else -10.0)''')

# pickups coming back
rep('''			if s.timer <= 0:
				fill_spawner(s)''', '''			if s.timer <= 0:
				fill_spawner(s)
				play("item_respawn", Vector2(s.x, s.y), -10.0)''')

# low fuel, lost the lead, loops
rep('''		fuel_beep_t = 0.45
		play_l("beep", null, -16.0, 0.0)''', '''		fuel_beep_t = 0.7
		play_l("low_fuel", null, -10.0, 0.0)''')
rep('''	if me_lead and not was_leader_me and t > 1.0:
		play_l("crown", null, -7.0, 0.0)
	was_leader_me = me_lead''', '''	if me_lead and not was_leader_me and t > 1.0:
		play_l("crown", null, -7.0, 0.0)
	elif was_leader_me and not me_lead and lead != null:
		play_l("lost_lead", null, -7.0, 0.0)
	was_leader_me = me_lead''')
rep('''func anim_tick(delta: float) -> void:
	anim_skip = shot_at >= 0''', '''func set_loop(pn: String, ln: String, db: float, delta: float) -> void:
	var ap: AudioStreamPlayer = loop_players.get(pn)
	if ap == null:
		return
	if ln == "" or autotest or shot_at >= 0:
		db = -80.0
	elif ap.stream != loops.get(ln):
		ap.stream = loops[ln]
		ap.volume_db = -60.0
	if db > -60.0 and not ap.playing and ap.stream != null:
		ap.play()
	ap.volume_db = move_toward(ap.volume_db, db, 40.0 * delta)
	if ap.volume_db <= -59.0 and db <= -60.0 and ap.playing:
		ap.stop()

func update_loops(delta: float) -> void:
	var playing := state == "play" or state == "paused" or state == "over"
	var amb := {"sky": "amb_sky", "outpost": "amb_outpost", "catacombs": "amb_catacombs"}.get(map_id, "amb_sky")
	set_loop("amb", amb, (-20.0 if playing else -28.0), delta)
	var me = players[my_idx] if (playing and my_idx < players.size()) else null
	set_loop("water", "water_loop", -10.0 if (me != null and me.alive and me.in_water) else -80.0, delta)
	var td := 1e9
	if me != null and map_id == "catacombs":
		var mc := center(me)
		for tp in torches:
			td = minf(td, mc.distance_to(Vector2(tp.x * T + 16, tp.y * T + 10)))
	set_loop("torch", "torch_loop", lerpf(-12.0, -45.0, clampf(td / 420.0, 0.0, 1.0)) if td < 420.0 else -80.0, delta)

func anim_tick(delta: float) -> void:
	anim_skip = shot_at >= 0
	update_loops(delta)''')

# match end
rep('''func on_state_change(old: String, new: String) -> void:
	ui_t = 0.0''', '''func on_state_change(old: String, new: String) -> void:
	ui_t = 0.0
	if new == "over" and old != "over":
		play_l("match_end", null, -4.0, 0.0)''')
open(P, "w").write(s)
print("ok")
