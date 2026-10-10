p = '/home/claude/skysquad/main.gd'
s = open(p).read()
def rep(a, b, count=1):
    global s
    n = s.count(a)
    assert n == count, (n, a[:110])
    s = s.replace(a, b)

rep('Playtest build 0.4', 'Playtest build 0.5')
rep('const VERSION := "0.4"', 'const VERSION := "0.5"')
# ---- slower feel ----
rep('"gravity": 900.0, "max_fall": 540.0, "move_speed": 125.0,', '"gravity": 850.0, "max_fall": 500.0, "move_speed": 105.0,')
rep('"jump_speed": 260.0, "thrust": 1550.0, "max_rise": 270.0,', '"jump_speed": 240.0, "thrust": 1400.0, "max_rise": 240.0,')
rep('"aim_turn": 7.0, "mouse_turn": 16.0,', '"aim_turn": 5.0, "mouse_turn": 10.0,')
# ---- new weapons ----
rep('''	"rpg":     {"name": "ROCKET",''', '''	"smg":     {"name": "SMG",     "dmg": 10.0, "rate": 0.085,"mag": 32, "spare": 128, "reload": 1.6, "spread": 0.08,  "speed": 1250.0, "pellets": 1, "life": 0.6,  "chip": 0.3,  "recoil": 2.5, "push": 0.0,   "snd": "smg", "zooms": [1]},
	"shock":   {"name": "SHOCK",   "dmg": 14.0, "rate": 0.3,  "mag": 20, "spare": 60,  "reload": 1.8, "spread": 0.0,   "speed": 0.0,    "pellets": 1, "life": 0.0,  "chip": 0.0,  "recoil": 2.0, "push": 0.0,   "snd": "shock", "zooms": [1], "special": "shock"},
	"net":     {"name": "NET GUN", "dmg": 5.0,  "rate": 1.2,  "mag": 3,  "spare": 6,   "reload": 2.0, "spread": 0.02,  "speed": 560.0,  "pellets": 1, "life": 1.3,  "chip": 0.0,  "recoil": 5.0, "push": 0.0,   "snd": "net", "zooms": [1], "special": "net"},
	"laser":   {"name": "LASER",   "dmg": 24.0, "rate": 0.4,  "mag": 12, "spare": 36,  "reload": 1.8, "spread": 0.006, "speed": 0.0,    "pellets": 1, "life": 0.0,  "chip": 0.6,  "recoil": 3.0, "push": 0.0,   "snd": "laser", "zooms": [1, 2], "special": "laser"},
	"rpg":     {"name": "ROCKET",''')
rep('''	"flip": {"label": "GRAVITY FLIP", "tip": "Everyone will slowly fall to the ceiling. Up still means fly."},''',
    '''	"flip": {"label": "ANTIGRAVITY FLIP", "tip": "Everyone will slowly fall to the ceiling. Up still means fly."},''')
# pickup pools with new guns and bombs
rep('''	[60, 7, "gun", ["sniper", "rpg"]], [55, 15, "health", []], [64, 15, "grenade", []],
	[42, 20, "gun", ["ak47", "shotgun"]], [78, 20, "gun", ["ak47", "shotgun"]],
	[25, 24, "health", []], [93, 24, "health", []],
	[50, 28, "gun", ["rpg", "ak47"]], [70, 28, "gun", ["rpg", "ak47"]], [61, 24, "gun", ["uzi", "magnum"]],
	[34, 31, "gun", ["shotgun", "sniper"]], [85, 31, "gun", ["shotgun", "sniper"]],
	[20, 34, "gun", ["magnum", "uzi"]], [100, 34, "gun", ["magnum", "uzi"]],
	[13, 18, "grenade", []], [107, 18, "grenade", []],
	[33, 11, "gun", ["ak47", "sniper"]], [87, 11, "gun", ["ak47", "sniper"]],
	[44, -1, "health", []], [76, -1, "health", []], [60, 38, "grenade", []],''', '''	[60, 7, "gun", ["sniper", "rpg", "laser"]], [55, 15, "health", []], [64, 15, "grenade", []],
	[42, 20, "gun", ["ak47", "shotgun", "smg"]], [78, 20, "gun", ["ak47", "shotgun", "smg"]],
	[25, 24, "health", []], [93, 24, "health", []],
	[50, 28, "gun", ["rpg", "ak47", "net"]], [70, 28, "gun", ["rpg", "ak47", "net"]], [61, 24, "gun", ["uzi", "magnum", "shock"]],
	[34, 31, "gun", ["shotgun", "sniper", "laser"]], [85, 31, "gun", ["shotgun", "sniper", "laser"]],
	[20, 34, "gun", ["magnum", "uzi", "smg"]], [100, 34, "gun", ["magnum", "uzi", "smg"]],
	[13, 18, "bomb", []], [107, 18, "bomb", []],
	[33, 11, "gun", ["ak47", "sniper", "shock"]], [87, 11, "gun", ["ak47", "sniper", "net"]],
	[44, -1, "health", []], [76, -1, "health", []], [60, 38, "grenade", []],''')
rep('''	"rusher":    {"react": 0.28, "err": 0.13, "turn": 8.0, "dist": 120.0, "likes": ["shotgun", "uzi"],''', '''	"rusher":    {"react": 0.28, "err": 0.13, "turn": 8.0, "dist": 120.0, "likes": ["shotgun", "uzi", "smg", "shock"],''')
rep('''"likes": ["sniper", "ak47"], "nade": 0.1,''', '''"likes": ["sniper", "ak47", "laser"], "nade": 0.1,''')
rep('''"likes": ["rpg", "shotgun"], "nade": 0.6,''', '''"likes": ["rpg", "shotgun", "net"], "nade": 0.6,''')
# ---- player fields ----
rep('''	var protect_t := 0.0
	var dual_side := 0''', '''	var protect_t := 0.0
	var stun_t := 0.0
	var net_t := 0.0
	var bombs := 0
	var switch_t := 0.0
	var side := 0
	var st := {}
	var near_k = null
	var near_t := -9.0
	var dual_side := 0''')
rep('''"down": false, "pick": "", "zoom": false}''', '''"down": false, "pick": "", "zoom": false, "bomb": false}''')
rep('''	var rocket := false
	var gun := ""

class Grenade:''', '''	var rocket := false
	var net := false
	var gun := ""

class Grenade:''')
rep('''	var fuse := 2.0
	var owner = null

class Part:''', '''	var fuse := 2.0
	var owner = null
	var kind := "frag"
	var stuck := false
	var beep_t := 0.0

class Part:''')
open(p, 'w').write(s)
print("a ok")
