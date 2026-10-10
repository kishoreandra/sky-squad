"""v0.7 part A: match stats (headshots, streaks, knife/blast kills), leader crown logic, sync over LAN, state-change hooks."""
import sys
P = "/home/claude/skysquad/main.gd"
s = open(P).read()

def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        sys.exit(f"expected {count} got {n}: {old[:90]!r}")
    s = s.replace(old, new)

rep('# Sky Squad - Arc Light Studio. Playtest build 0.6', '# Sky Squad - Arc Light Studio. Playtest build 0.7')
rep('const VERSION := "0.6"', 'const VERSION := "0.7"')
rep('\tvar bot := false\n\tvar remote := false', '\tvar bot := false\n\tvar actor := false\n\tvar hs := 0\n\tvar best := 0\n\tvar mk := 0\n\tvar bk := 0\n\tvar lstreak := 0\n\tvar remote := false')

# stats + leader down
rep('''	p.deaths += 1
	p.streak = 0
	p.hp = 0
	var k = p.last_hit_by''', '''	p.deaths += 1
	var was_leader: bool = current_leader() == p and p.kills >= 3
	p.lstreak = p.streak
	p.streak = 0
	p.hp = 0
	var k = p.last_hit_by''')
rep('''		k.kills += 1
		k.streak += 1
		entry.k = k.pname''', '''		k.kills += 1
		k.streak += 1
		k.best = maxi(k.best, k.streak)
		if entry.head:
			k.hs += 1
		if p.last_cause == "melee":
			k.mk += 1
		elif p.last_cause == "blast":
			k.bk += 1
		entry.k = k.pname''')
rep('''		if entry.head:
			me_fx(k, "big", "HEADSHOT!")''', '''		if was_leader:
			me_fx(k, "big", "LEADER DOWN!")
		elif entry.head:
			me_fx(k, "big", "HEADSHOT!")''')
rep('''			feed.push_front({"k": "", "kc": C_INK, "v": "%s left. A bot took over." % p.pname, "vc": C_ARC, "gun": "", "head": false, "t": 4.0, "note": ""})''',
    '''			feed.push_front({"k": "", "kc": C_INK, "v": "%s left. A bot took over." % p.pname, "vc": C_ARC, "gun": "", "head": false, "t": 4.0, "t0": 4.0, "note": ""})''')
rep('''"vc": C_ARC, "gun": "", "head": false, "t": 3.0, "note": ""})''', '''"vc": C_ARC, "gun": "", "head": false, "t": 3.0, "t0": 3.0, "note": ""})''')

# LAN sync of the new numbers
rep('const PF_N := 24', 'const PF_N := 29')
rep('''p.kills, p.deaths, p.respawn_t, maxf(p.say_t, 0.0), maxf(p.switch_t, 0.0), maxf(p.melee_anim, 0.0), maxf(p.flash, 0.0), lh])
		ps.append("%s|%s|%s|%s" % [p.posture, slot_str(p.slots[0]), slot_str(p.slots[1]), p.say if p.say_t > 0 else ""])''',
    '''p.kills, p.deaths, p.respawn_t, maxf(p.say_t, 0.0), maxf(p.switch_t, 0.0), maxf(p.melee_anim, 0.0), maxf(p.flash, 0.0), lh,
			p.hs, p.best, p.mk, p.bk, p.lstreak])
		ps.append("%s|%s|%s|%s|%s|%s|%d" % [p.posture, slot_str(p.slots[0]), slot_str(p.slots[1]), p.say if p.say_t > 0 else "", p.last_gun, p.last_cause, 1 if p.last_head else 0])''')
rep('''		p.say = bits[3] if bits.size() > 3 else ""''', '''		p.say = bits[3] if bits.size() > 3 else ""
		if bits.size() > 6:
			p.last_gun = bits[4]
			p.last_cause = bits[5]
			p.last_head = bits[6] == "1"
		p.hs = int(pf[o + 24])
		p.best = int(pf[o + 25])
		p.mk = int(pf[o + 26])
		p.bk = int(pf[o + 27])
		p.lstreak = int(pf[o + 28])''')
rep('''	var k := []
	var dd := []
	for p in players:
		k.append(p.kills)
		dd.append(p.deaths)
	rpc("s_end", {"k": k, "d": dd})''', '''	var info := {"k": [], "d": [], "hs": [], "best": [], "mk": [], "bk": []}
	for p in players:
		info.k.append(p.kills)
		info.d.append(p.deaths)
		info.hs.append(p.hs)
		info.best.append(p.best)
		info.mk.append(p.mk)
		info.bk.append(p.bk)
	rpc("s_end", info)''')
rep('''		players[i].kills = info.k[i]
		players[i].deaths = info.d[i]''', '''		players[i].kills = info.k[i]
		players[i].deaths = info.d[i]
		players[i].hs = info.hs[i]
		players[i].best = info.best[i]
		players[i].mk = info.mk[i]
		players[i].bk = info.bk[i]''')

# clicks: press feel + fade before big moves
rep('''func menu_tap(pos: Vector2) -> void:
	for b in ui_btns:
		if b.r.has_point(pos):
			do_action(b.a)
			return

func do_action(a: String) -> void:
	play("swap", null, -10.0, 0.0)
''', '''func menu_tap(pos: Vector2) -> void:
	if pending_action != "":
		return
	for b in ui_btns:
		if b.r.has_point(pos):
			pressed_r = b.r
			pressed_at = time_s
			play_l("swap", null, -10.0, 0.0)
			var a: String = b.a
			if a.begins_with("row:") or a.begins_with("key:"):
				do_action(a)
				return
			pending_action = a
			pending_big = BIG_ACTIONS.has(a)
			pending_t = 0.22 if pending_big else 0.1
			return

func do_action(a: String) -> void:
''')

# tap the timer to peek at scores
rep('''	if pause_rect.has_point(pos):
		state = "paused"
		jet_player.stop()
		return
	for bb in bubbles:
		if pos.distance_to(bb.pos) < bb.r + 10 * u:''', '''	if pause_rect.has_point(pos):
		state = "paused"
		jet_player.stop()
		return
	if timer_rect.has_point(pos):
		peek_t = 0.0 if peek_t > 0 else 3.0
		return
	for bb in bubbles:
		if pos.distance_to(bb.pos) < bb.r + 10 * u:''')
rep('''		elif event.pressed and pause_rect.has_point(event.position):
			state = "paused"
			mouse_down = false
			jet_player.stop()''', '''		elif event.pressed and pause_rect.has_point(event.position):
			state = "paused"
			mouse_down = false
			jet_player.stop()
		elif event.pressed and timer_rect.has_point(event.position):
			peek_t = 0.0 if peek_t > 0 else 3.0
			mouse_down = false''')

# process: timers, state changes, pending action, menu actors
rep('''	if shot_at >= 0:
		while state == "play" and t < shot_at:''', '''	anim_tick(delta)
	if shot_at >= 0:
		while state == "play" and t < shot_at:''')
rep('''	if shot_wait > 12:''', '''	if shot_wait > 30:''')
open(P, "w").write(s)
print("ok")
