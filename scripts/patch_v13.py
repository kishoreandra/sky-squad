"""v1.3: home server mode (one room on one port, for a desktop + playit.gg tunnel); server address may be host:port."""
import sys
P = "/home/claude/skysquad/main.gd"
s = open(P).read()
def rep(a, b, c=1):
    global s
    if s.count(a) != c: sys.exit("expected %d got %d: %r" % (c, s.count(a), a[:120]))
    s = s.replace(a, b)

rep('# Sky Squad - Arc Light Studio. Playtest build 1.2', '# Sky Squad - Arc Light Studio. Playtest build 1.3')
rep('const VERSION := "1.2"', 'const VERSION := "1.3"')
# address with a port = a home server: go straight to its one room
rep('''func mm_query(mode: String, code: String) -> void:
	var host := str(cfg.server).strip_edges()
	var ip := host if host.is_valid_ip_address() else IP.resolve_hostname(host, IP.TYPE_IPV4)''', '''func mm_query(mode: String, code: String) -> void:
	var host := str(cfg.server).strip_edges()
	var direct_port := 0
	if host.contains(":"):
		direct_port = int(host.get_slice(":", 1))
		host = host.get_slice(":", 0)
	var ip := host if host.is_valid_ip_address() else IP.resolve_hostname(host, IP.TYPE_IPV4)''')
rep('''	if recon_left <= 0:
		conn_label = ("Opening room " if mode == "new" else "Joining room ") + mm_code
	state = "connecting"''', '''	if recon_left <= 0:
		conn_label = ("Opening room " if mode == "new" else "Joining room ") + mm_code
	state = "connecting"
	if direct_port > 0:
		mm_mode = ""
		if recon_left <= 0:
			conn_label = "Joining the home server"
		join_game(ip, direct_port)''')
rep('''		if name_entry.length() < 40 and "abcdefghijklmnopqrstuvwxyz0123456789.-".contains(k):''', '''		if name_entry.length() < 48 and "abcdefghijklmnopqrstuvwxyz0123456789.-:".contains(k):''')
rep('''			row = "ZXCVBNM.-"''', '''			row = "ZXCVBNM.-:"''')
rep('''		"server": ["SERVER ADDRESS", "Ask the group admin. Example: 140.238.1.2"]}''', '''		"server": ["SERVER ADDRESS", "Ask the admin. Like 140.238.1.2 or name.ply.gg:12345"]}''')
# lobby title: the server's own room name when it has one (a home server has one room)
rep('''		txh("ROOM  " + room_code, Vector2(x, y + 42 * u), 26 * u, C_ARC, 0, 4 * u)''', '''		if str(lobby_info.get("room", "")) != "":
			room_code = str(lobby_info.room)
		txh("ROOM  " + room_code, Vector2(x, y + 42 * u), 26 * u, C_ARC, 0, 4 * u)''')
# home server: never closes; when everyone leaves, the room goes back to waiting
rep('''				if a2.begins_with("--matchsecs="):''', '''				if a2 == "--stay":
					stay_open = true
				if a2.begins_with("--matchsecs="):''')
rep('''	if lan_players.is_empty():
		idle_t += delta
		if idle_t > 90.0:''', '''	if lan_players.is_empty() and stay_open:
		if state != "lobby":
			print("SERVER everyone left, back to waiting")
			state = "lobby"
			players.clear()
		idle_t = 0.0
	elif lan_players.is_empty():
		idle_t += delta
		if idle_t > 90.0:''')
s += '''
var stay_open := false
'''
open(P, "w").write(s)
print("ok")
