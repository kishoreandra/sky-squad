"""v1.7 part E: original menu theme (loops on menus, fades in matches) + Music setting + Credits screen."""
import sys
P = "/home/claude/skysquad/main.gd"
s = open(P).read()
ERR = []
def rep(a, b, c=1):
    global s
    if s.count(a) != c:
        ERR.append("expected %d got %d: %r" % (c, s.count(a), a[:120])); return
    s = s.replace(a, b)

rep('''const MENU_STATES := ["menu", "match_cfg", "ctrl_cfg", "lan", "lan_join", "ipkey", "connecting", "lobby", "lan_cfg", "locker", "namekey", "online"]''',
    '''const MENU_STATES := ["menu", "match_cfg", "ctrl_cfg", "lan", "lan_join", "ipkey", "connecting", "lobby", "lan_cfg", "locker", "namekey", "online", "credits"]''')
rep('''	"name": "", "show_fps": false,''', '''	"name": "", "show_fps": false, "music": true,''')
rep('''	["show_fps", "Show FPS", [false, true], ["Off", "On"]],''', '''	["music", "Menu music", [true, false], ["On", "Off"]],
	["show_fps", "Show FPS", [false, true], ["Off", "On"]],''')
rep('''	for pn in ["amb", "water", "torch"]:''', '''	music_player = AudioStreamPlayer.new()
	var mst: AudioStreamOggVorbis = load("res://music/theme.ogg")
	if mst != null:
		mst.loop = true
		music_player.stream = mst
	music_player.volume_db = -80.0
	add_child(music_player)
	for pn in ["amb", "water", "torch"]:''')
rep('''	anim_tick(delta)
	if dedicated:''', '''	anim_tick(delta)
	music_tick(delta)
	if dedicated:''')
# menu: credits button + line
rep('''	txt("Sounds: Kenney.nl (CC0) and the Freedoom project (BSD licence)", Vector2(r.end.x - 20 * u, r.end.y - 12 * u), 8 * u, Color(C_MUTED, 0.7), 2)''',
    '''	ui_button("CREDITS", Rect2(r.end.x - 112 * u, r.end.y - 48 * u, 92 * u, 34 * u), "credits")''')
rep('''		"controls":
			state = "ctrl_cfg"''', '''		"controls":
			state = "ctrl_cfg"
		"credits":
			state = "credits"''')
rep('''			"ctrl_cfg":
				draw_cfg("CONTROLS", CONTROL_ROWS)''', '''			"ctrl_cfg":
				draw_cfg("CONTROLS", CONTROL_ROWS)
			"credits":
				draw_credits()''')
rep('''		"match_cfg", "ctrl_cfg", "lan":''', '''		"match_cfg", "ctrl_cfg", "lan", "credits":''')
rep('''	"Keyboard: A/D W S, mouse, E Q Z G B C F.",''', '''	"Keyboard: A/D W S, mouse, E Q Z G F, 1-3 pick throw, Shift hand.",''')
s += '''
# ================= MUSIC + CREDITS (v1.7) =================
var music_player: AudioStreamPlayer
var music_vol := -80.0

# the theme plays on the menus and lobby, and fades away once a match starts
func music_tick(delta: float) -> void:
	if music_player == null or music_player.stream == null or dedicated or autotest:
		return
	var want := -9.0 if (bool(cfg.get("music", true)) and cfg.sound and MENU_STATES.has(state)) else -80.0
	music_vol = move_toward(music_vol, want, delta * (40.0 if want > music_vol else 30.0))
	music_player.volume_db = music_vol
	if music_vol > -79.0 and not music_player.playing:
		music_player.play()
	elif music_vol <= -79.5 and music_player.playing:
		music_player.stop()

const CREDITS := [
	["GAME", ""],
	["Sky Squad", "Arc Light Studio"],
	["Design and testing", "Arc Light Studio and friends"],
	["Code, art and music", "Made with Claude (Anthropic)"],
	["MUSIC", ""],
	["Sky Squad Theme", "Original music made for this game"],
	["SOUNDS", ""],
	["Sound effects", "Kenney.nl (CC0)"],
	["More sound effects", "The Freedoom project (BSD licence)"],
	["ENGINE", ""],
	["Godot Engine 4.3", "godotengine.org (MIT licence)"],
	["", ""],
	["Thanks for playing!", ""],
]

func draw_credits() -> void:
	var w := minf(sw - 32 * u, 560 * u)
	var h := minf(sh - 24 * u, 340 * u)
	var r := panel(w, h)
	var x := r.position.x + 28 * u
	var y := r.position.y + 44 * u
	txh("CREDITS", Vector2(x, y), 26 * u, C_ARC, 0, 5 * u)
	y += 30 * u
	for i in CREDITS.size():
		var row: Array = CREDITS[i]
		var k2 := ease_out((ui_t - 0.1 - i * 0.03) / 0.3)
		var ga1 := ga
		ga *= k2
		if row[1] == "" and row[0] != "" and row[0] == row[0].to_upper():
			y += 6 * u
			txt(row[0], Vector2(x, y), 10 * u, C_CYAN)
		else:
			txt(row[0], Vector2(x, y), 12 * u, C_INK)
			txt(row[1], Vector2(r.end.x - 28 * u, y), 12 * u, C_MUTED, 2)
		ga = ga1
		y += 18 * u
	ui_button("BACK", Rect2(r.end.x - 132 * u, r.end.y - 54 * u, 108 * u, 38 * u), "back")
'''
if ERR:
    print("\n".join(ERR)); sys.exit(1)
open(P, "w").write(s)
print("ok")
