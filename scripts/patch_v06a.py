"""v0.6 part A: LAN plumbing inside the game logic (me_fx, fx recording, tile diffs, players[my_idx])."""
import re, sys
P = "/home/claude/skysquad/main.gd"
s = open(P).read()

def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        sys.exit(f"expected {count} got {n}: {old[:80]!r}")
    s = s.replace(old, new)

rep('# Sky Squad - Arc Light Studio. Playtest build 0.5\n# You vs 5 bots.', '# Sky Squad - Arc Light Studio. Playtest build 0.6\n# You vs bots, or LAN play with friends over a phone hotspot.')
rep('const VERSION := "0.5"', 'const VERSION := "0.6"\nconst NET_PORT := 24850\nconst DISC_PORT := 24851\nconst FUN_NAMES := ["Blaze", "Rocket", "Shadow", "Viper", "Tiger", "Storm", "Ninja", "Falcon", "Ace", "Bolt", "Rider", "Hawk", "Ghost", "Cobra", "Flash", "Comet"]\nconst MENU_STATES := ["menu", "match_cfg", "ctrl_cfg", "lan", "lan_join", "ipkey", "connecting", "lobby", "lan_cfg"]')

# player fields
rep('\tvar bot := false\n\tvar style := ""', '\tvar bot := false\n\tvar remote := false\n\tvar peer_id := 0\n\tvar nx := 0.0\n\tvar ny := 0.0\n\tvar naim := 0.0\n\tvar snap_age := 0.0\n\tvar style := ""')

# cfg
rep('"left_handed": false, "aim_sens": "medium", "vibration": true, "sound": true,\n}',
    '"left_handed": false, "aim_sens": "medium", "vibration": true, "sound": true,\n\t"name": "", "lan_bots": 2,\n}')
rep('const CONTROL_ROWS := [', '''const LAN_ROWS := [
	["mode", "Game mode", ["ffa", "team"], ["Free for all", "Teams"]],
	["lan_bots", "Bots", [0, 1, 2, 3, 4], ["None", "1", "2", "3", "4"]],
	["skill", "Bot skill", ["easy", "normal", "hard"], ["Easy", "Normal", "Hard"]],
	["minutes", "Match length", [3, 5, 10], ["3 min", "5 min", "10 min"]],
	["event_every", "Map event every", [45, 60, 90], ["45 sec", "60 sec", "90 sec"]],
	["ev_water", "Rising water", [true, false], ["On", "Off"]],
	["ev_roof", "Falling rocks", [true, false], ["On", "Off"]],
	["ev_brk", "Breaking ground", [true, false], ["On", "Off"]],
	["ev_flip", "Antigravity flip", [false, true], ["Off", "On"]],
	["zones", "Gravity zones", [false, true], ["Off", "On"]],
]
const CONTROL_ROWS := [''')

# net vars
rep('# test hooks\nvar autotest := false', '''# LAN
var net_role := ""
var my_idx := 0
var lan_players: Array = []
var lobby_info := {}
var disc: PacketPeerUDP = null
var probe: PacketPeerUDP = null
var probe_t := 0.0
var found_hosts := {}
var ip_entry := ""
var join_ip := ""
var connect_t := 0.0
var net_fx: Array = []
var tile_dirty := {}
var snap_t := 0.0
var in_t := 0.0
var stash := {}
var pending_start := false
var client_jet := false
var latch_pick := ""
var latch_pick_t := 0.0
var latch_zoom_t := 0.0
var toast_msg := ""
var toast_t := 0.0
var snaps_got := 0
var snaps_sent := 0
var inputs_got := 0
var tiles_got := 0
var fx_count := {}
var lantest_host := false
var lantest_join := ""
var lantest_time := 0.0
var lt_wait := 0.0
var lt_done := 0.0
var lt_moved := 0.0
var lan_shots: Array = []
var shots_quit := false
var shot_wait := 0

# test hooks
var autotest := false''')

# sound: local play + recorded play
rep('''func play(name: String, pos = null, vol := 0.0, pitch_var := 0.08) -> void:
	if autotest or shot_at >= 0:''', '''func play(name: String, pos = null, vol := 0.0, pitch_var := 0.08) -> void:
	play_l(name, pos, vol, pitch_var)
	if net_role == "host":
		net_fx.append(["s", name, pos, vol])

func play_l(name: String, pos = null, vol := 0.0, pitch_var := 0.08) -> void:
	if autotest or shot_at >= 0:''')

# tile diffs
rep('''	tiles[r * COLS + c] = v
	thp[r * COLS + c] = TILE_HP.get(v, 99.0)''', '''	tiles[r * COLS + c] = v
	thp[r * COLS + c] = TILE_HP.get(v, 99.0)
	if net_role == "host":
		tile_dirty[r * COLS + c] = true''')
rep('''	thp[i] -= amt
	if thp[i] <= 0:''', '''	thp[i] -= amt
	if net_role == "host":
		tile_dirty[i] = true
	if thp[i] <= 0:''')
rep('''				tiles[v.y * COLS + v.x] = EMPTY
				debris(''', '''				set_tile(v.x, v.y, EMPTY)
				debris(''')

# particle helpers record themselves
rep('''func debris(x: float, y: float, n: int, kind: int = DIRT) -> void:
''', '''func debris(x: float, y: float, n: int, kind: int = DIRT) -> void:
	if net_role == "host":
		net_fx.append(["d", x, y, n, kind])
''')
rep('''func sparks(x: float, y: float, color: Color, n: int, spd := 200.0) -> void:
''', '''func sparks(x: float, y: float, color: Color, n: int, spd := 200.0) -> void:
	if net_role == "host":
		net_fx.append(["k", x, y, color, n, spd])
''')
rep('''func blood(x: float, y: float, n: int) -> void:
''', '''func blood(x: float, y: float, n: int) -> void:
	if net_role == "host":
		net_fx.append(["b", x, y, n])
''')

# hurt feedback goes to whoever is that player
rep('''	if p == players[0] and cause != "water":
		hurt_t = 0.35
		if t - last_buzz > 0.15:
			last_buzz = t
			buzz(25)
	if src == players[0] and p != players[0] and cause != "water":
		hitmark_t = 0.15''', '''	if cause != "water":
		me_fx(p, "hurt")
		if src != null and src != p:
			me_fx(src, "hit")''')

# die
rep('"vc": C_RED if p == players[0] else p.color,', '"vc": p.color, "vi": players.find(p),')
rep('''	corpses.append(cp)
''', '''	corpses.append(cp)
	if net_role == "host":
		net_fx.append(["c", cp.x, cp.y, cp.vx, cp.vy, cp.spin, cp.team, cp.face])
''')
rep('''		if k == players[0]:
			buzz(90)
			shake = maxf(shake, 7.0)
			if entry.head:
				show_big("HEADSHOT!")
			elif k.streak == 2:
				show_big("DOUBLE KILL")
			elif k.streak >= 3:
				show_big("%d KILL STREAK" % k.streak)''', '''		me_fx(k, "buzz", 90)
		me_fx(k, "shake", 7.0)
		if entry.head:
			me_fx(k, "big", "HEADSHOT!")
		elif k.streak == 2:
			me_fx(k, "big", "DOUBLE KILL")
		elif k.streak >= 3:
			me_fx(k, "big", "%d KILL STREAK" % k.streak)''')
rep('''	if p == players[0]:
		jet_player.stop()
		buzz(300)''', '''	me_fx(p, "jetoff")
	me_fx(p, "buzz", 300)''')
rep('''	play("headshot", null, -6.0, 0.0)''', '''	play_l("headshot", null, -6.0, 0.0)''')

# fire effects split out so clients can replay them
old_tail = s[s.index('\tp.recoil = d.recoil\n\tp.muzzle_t = 0.07'):s.index('func hitscan(')]
new_tail = '''	if d.push > 0 and p.posture == "stand":
		p.vx -= cos(p.aim) * d.push
		p.vy -= sin(p.aim) * d.push * 0.5
	fire_fx(p, w.type, mz)
	if net_role == "host":
		net_fx.append(["f", players.find(p), w.type, mz])

func fire_fx(p: Player, wt: String, mz: Vector2) -> void:
	var d: Dictionary = WD[wt]
	var special: String = d.get("special", "")
	p.recoil = d.recoil
	p.muzzle_t = 0.07
	p.shot_t = t
	if wt != "rpg" and special == "":
		var q := add_part(mz.x - cos(p.aim) * 14, mz.y - sin(p.aim) * 14, -cos(p.aim) * 40 + randf_range(-30, 30), -120 * gsign() + randf_range(-30, 0), 0.7, Color("#d9b24a"), 2.6, 1.0)
		q.spin = randf_range(-14, 14)
		if wt == "ak47" or wt == "sniper":
			add_part(mz.x, mz.y, cos(p.aim) * 30, sin(p.aim) * 30 - 10, 0.5, Color(0.85, 0.85, 0.85, 0.45), 6, -0.02, "smoke", 18)
	elif wt == "rpg":
		for i in 6:
			add_part(mz.x - cos(p.aim) * 40, mz.y - sin(p.aim) * 40, -cos(p.aim) * 120 + randf_range(-40, 40), -sin(p.aim) * 120 + randf_range(-40, 40), 0.8, Color(0.8, 0.8, 0.8, 0.6), 10, -0.05, "smoke", 26)
	play_l(d.snd, mz, (-1.0 if wt == "ak47" else -4.0) if is_me(p) else -6.0)
	if is_me(p):
		shake = maxf(shake, d.recoil * (0.9 if wt == "ak47" else 0.5))

'''
s = s.replace(old_tail, new_tail)

rep('tracers.append({', 'add_tracer({', 5)

# explode: visuals split out
rep('''func explode(x: float, y: float, r: float, dmg: float, owner, gun: String) -> void:
	shake = maxf(shake, 14.0)
	play("explosion", Vector2(x, y), 0.0)''', '''func explode(x: float, y: float, r: float, dmg: float, owner, gun: String) -> void:
	explode_fx(x, y, r)
	if net_role == "host":
		net_fx.append(["x", x, y, r])
	explosions += 1
	explode_hits(x, y, r, dmg, owner, gun)

func explode_fx(x: float, y: float, r: float) -> void:
	shake = maxf(shake, 14.0)
	play_l("explosion", Vector2(x, y), 0.0)''')
rep('''		add_part(x, y, cos(a) * s, sin(a) * s, 0.35 + randf() * 0.25, Color("#ffcf5e"), 3, 0.3)
	explosions += 1
''', '''		add_part(x, y, cos(a) * s, sin(a) * s, 0.35 + randf() * 0.25, Color("#ffcf5e"), 3, 0.3)

func explode_hits(x: float, y: float, r: float, dmg: float, owner, gun: String) -> void:
''')

# personal sounds -> me_fx
s, n = re.subn(r'(\t+)if p == players\[0\]:\n\t+play\("(\w+)", null, (-?[\d.]+)((?:, [\d.]+)?)\)', r'\1me_fx(p, "snd", ["\2", \3\4])', s)
print("personal sounds:", n)
rep('''	if p == players[0]:
		if p.jet_on and not was_jet''', '''	if is_me(p):
		if p.jet_on and not was_jet''')
rep('''	if p.bot:
		p.aim = inp.aim''', '''	if p.bot or p.remote:
		p.aim = inp.aim''')

# drawing: who is "me"
rep('	if p.bot or cfg.mode == "team":\n\t\ttxt(p.pname', '	if not is_me(p) or cfg.mode == "team":\n\t\ttxt(p.pname')
rep('C_INK if rk[i].bot else C_ARC, 0, 2 * u)', 'C_ARC if is_me(rk[i]) else (C_INK if rk[i].bot else C_CYAN), 0, 2 * u)')
rep('var col: Color = C_ARC if not rk[i].bot else C_INK', 'var col: Color = C_ARC if is_me(rk[i]) else (C_INK if rk[i].bot else C_CYAN)')
rep('Color(f.vc, a)', 'Color(C_RED if f.get("vi", -1) == my_idx else f.vc, a)', 2)

# reset_match builds humans (LAN) + bots
rep('''	match_time = cfg.minutes * 60.0''', '''	match_time = cfg.minutes * 60.0
	if lantest_time > 0:
		match_time = lantest_time''')
old = s[s.index('\tfor i in 1 + int(cfg.bots):'):s.index('\tfor p in players:\n\t\tspawn(p)')]
new = '''	var humans: Array = [{"peer": 1, "name": NAMES[0]}]
	var nbots := int(cfg.bots)
	if net_role == "host":
		humans = lan_players
		nbots = clampi(int(cfg.lan_bots), 0, 6 - humans.size())
	var bot_names := []
	for nm in NAMES.slice(1) + ["Dev", "Asha", "Vikram"]:
		var used := false
		for hm in humans:
			if hm.name == nm:
				used = true
		if not used:
			bot_names.append(nm)
	for i in humans.size() + nbots:
		var p := Player.new()
		var human := i < humans.size()
		p.id = i
		p.pname = humans[i].name if human else bot_names[i - humans.size()]
		p.team = TEAMS[i]
		p.color = TEAM_COL[i]
		p.bot = not human
		p.remote = human and int(humans[i].peer) != 1
		p.peer_id = int(humans[i].peer) if human else 0
		p.style = BOT_STYLE[i]
		p.st = make_style(p.style)
		p.side = i
		if cfg.mode == "team":
			p.side = i % 2
			if i > 0 or net_role == "host":
				p.team = "blue" if p.side == 0 else "red"
				p.color = TEAM_COL[1] if p.side == 0 else TEAM_COL[2]
		p.prev = p.inp.duplicate()
		players.append(p)
	my_idx = 0
'''
s = s.replace(old, new)
rep('''	start_dirt = tiles.count(DIRT)
	cam = Vector2.ZERO''', '''	start_dirt = tiles.count(DIRT)
	cam = Vector2.ZERO
	tile_dirty.clear()
	net_fx = []''')

n0 = s.count("players[0]")
s = s.replace("players[0]", "players[my_idx]")
print("players[0] replaced:", n0)
open(P, "w").write(s)
