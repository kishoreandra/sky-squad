extends Node2D
# Sky Squad - Arc Light Studio. Playtest build 1.6
# You vs bots, or LAN play with friends over a phone hotspot. Jetpack fuel, health, real-style guns, breaking map, gravity zones, slow map events.

const META = preload("res://art/meta.gd")
const VERSION := "1.6"
const NET_PORT := 24850
const DISC_PORT := 24851
const FUN_NAMES := ["Blaze", "Rocket", "Shadow", "Viper", "Tiger", "Storm", "Ninja", "Falcon", "Ace", "Bolt", "Rider", "Hawk", "Ghost", "Cobra", "Flash", "Comet"]
const MENU_STATES := ["menu", "match_cfg", "ctrl_cfg", "lan", "lan_join", "ipkey", "connecting", "lobby", "lan_cfg", "locker", "namekey", "online"]
# ---- avatar data (made by make_avatar_layers.py) ----
const AV_RECT := {"face": [19.667, 11.667, 23.0, 23.0], "f_none": [34.0, 21.0, 5.667, 6.0], "f_goggles": [31.667, 21.333, 10.667, 7.0], "f_shades": [31.667, 21.0, 11.0, 6.667], "f_patch": [21.0, 17.333, 20.0, 10.333], "f_scar": [32.0, 19.0, 8.667, 9.0], "f_paint": [28.0, 21.0, 13.667, 9.0], "f_mooch": [32.667, 21.0, 9.667, 10.0], "f_cyber": [30.667, 20.667, 13.0, 7.0], "f_monocle": [33.0, 20.0, 7.0, 13.0], "f_cheeky": [31.0, 21.0, 10.0, 11.667], "h_classic": [18.667, 9.0, 27.0, 15.667], "h_beret": [18.667, 8.667, 21.0, 13.0], "h_bandana": [13.667, 10.0, 29.333, 17.0], "h_ninja": [12.667, 11.0, 30.333, 24.0], "h_pilot": [18.0, 9.0, 26.0, 19.667], "h_astro": [16.667, 8.667, 29.0, 29.0], "h_nvg": [18.667, 9.0, 27.0, 15.667], "h_cowboy": [15.0, 6.667, 33.0, 16.333], "h_cap": [13.667, 9.0, 29.333, 14.667], "h_viking": [15.0, 5.333, 31.0, 19.333], "h_marine": [18.0, 9.667, 26.0, 26.0], "h_turban": [18.0, 7.667, 25.0, 16.333], "h_samurai": [14.667, 1.0, 32.667, 27.0], "h_gasmask": [18.667, 9.0, 27.0, 26.667], "h_robot": [18.667, 3.0, 25.0, 31.667], "h_hoodie": [17.667, 9.0, 25.0, 29.0], "h_pumpkin": [17.667, 8.0, 27.0, 27.667], "h_halo": [18.667, 3.667, 27.0, 21.0], "h_crown": [18.667, 4.333, 27.0, 20.333], "o_army_shirt": [20.667, 29.667, 20.0, 22.0], "o_army": [21.0, 32.0, 18.667, 18.333], "o_desert": [20.667, 29.667, 20.0, 22.0], "o_urban": [20.667, 29.667, 20.0, 22.0], "o_snow": [20.667, 29.667, 20.0, 22.0], "o_ninja": [20.667, 29.667, 20.0, 22.0], "o_jumpsuit": [20.667, 29.667, 20.0, 22.0], "o_hazmat": [20.667, 29.667, 20.0, 22.0], "o_mech": [20.667, 29.667, 20.0, 22.0], "o_hero": [20.667, 29.667, 20.0, 22.0], "o_agent": [20.667, 29.667, 20.0, 22.0], "o_kurta": [20.667, 29.667, 20.0, 22.0], "o_hawaii": [20.667, 29.667, 20.0, 22.0], "o_samurai": [20.667, 29.667, 20.0, 22.0], "o_street": [20.667, 29.667, 20.0, 22.0], "j_twin": [18.0, 29.667, 14.0, 26.0], "j_rocket": [13.667, 24.333, 18.667, 30.667], "j_fan": [12.667, 20.667, 23.0, 31.0], "j_wings": [4.0, 23.0, 26.667, 28.667], "j_barrel": [16.667, 29.667, 15.0, 24.0], "j_butterfly": [5.0, 21.333, 25.667, 30.333], "j_dragon": [11.0, 29.667, 19.667, 29.667], "j_chrome": [17.667, 28.667, 14.333, 24.0], "j_hover": [15.0, 31.667, 18.667, 29.0], "j_fireworks": [15.667, 26.333, 15.0, 26.333], "j_umbrella": [8.667, 12.667, 31.0, 39.0], "x_bandolier": [21.333, 31.333, 17.333, 17.333], "x_cape": [9.0, 30.667, 22.333, 34.667], "x_scarf": [7.0, 28.667, 31.667, 10.333], "x_sword": [11.0, 22.0, 25.667, 40.0], "x_antenna": [11.0, 15.0, 12.667, 34.667], "x_pads": [34.667, 28.667, 9.0, 8.0], "x_tags": [25.0, 34.0, 11.0, 7.667], "x_pet": [1.0, 14.0, 14.0, 12.667], "x_flag": [8.0, 13.0, 13.0, 38.667]}
const AV_LIST := {"h": [["classic", "Combat helmet"], ["beret", "Commando beret"], ["bandana", "Rambo bandana"], ["ninja", "Ninja hood"], ["pilot", "Pilot helmet"], ["astro", "Astronaut bubble"], ["nvg", "Night-vision helmet"], ["cowboy", "Cowboy hat"], ["cap", "Backwards cap"], ["viking", "Viking horns"], ["marine", "Space marine"], ["turban", "Pagdi / turban"], ["samurai", "Samurai kabuto"], ["gasmask", "Gas mask"], ["robot", "Robot head"], ["hoodie", "Street hoodie"], ["pumpkin", "Pumpkin"], ["halo", "Angel halo"], ["crown", "Champion crown"]], "f": [["goggles", "Flight goggles"], ["shades", "Aviator shades"], ["patch", "Eye patch"], ["scar", "Battle scar"], ["paint", "War paint"], ["mooch", "Big mooch"], ["cyber", "Cyber visor"], ["monocle", "Gentleman monocle"], ["cheeky", "Cheeky grin"], ["none", "No glasses"]], "o": [["army", "Army vest"], ["desert", "Desert camo"], ["urban", "Urban grey camo"], ["snow", "Snow camo"], ["ninja", "Shadow ninja"], ["jumpsuit", "Pilot jumpsuit"], ["hazmat", "Hazmat suit"], ["mech", "Mech armour"], ["hero", "Super-hero suit"], ["agent", "Secret agent suit"], ["kurta", "Festive kurta"], ["hawaii", "Beach shirt"], ["samurai", "Samurai armour"], ["street", "Street hoodie"]], "j": [["twin", "Twin tanks"], ["rocket", "Space rocket"], ["fan", "Heli-fan"], ["wings", "Metal wings"], ["barrel", "DIY barrel"], ["butterfly", "Neon butterfly"], ["dragon", "Dragon pack"], ["chrome", "Chrome racer"], ["hover", "Hover rings"], ["fireworks", "Diwali rockets"], ["umbrella", "Umbrella glider"]], "x": [["none", "No extra"], ["bandolier", "Ammo bandolier"], ["cape", "Hero cape"], ["scarf", "Flying scarf"], ["sword", "Katana on back"], ["antenna", "Radio backpack"], ["pads", "Armour pads"], ["tags", "Dog tags"], ["pet", "Drone buddy"], ["flag", "India flag"]], "fl": [["orange", "Fire orange"], ["blue", "Plasma blue"], ["green", "Toxic green"], ["purple", "Void purple"], ["pink", "Candy pink"], ["gold", "Golden"], ["none", "Silent (no flame)"]]}
const AV_SETS := [["commando", "Desert commando", "beret.shades.desert.twin.bandolier.orange"], ["shadow", "Shadow ninja", "ninja.goggles.ninja.dragon.sword.purple"], ["ace", "Sky ace", "pilot.goggles.jumpsuit.chrome.scarf.blue"], ["robo", "Robo trooper", "robot.goggles.mech.hover.pet.blue"], ["maharaja", "Desi hero", "turban.mooch.kurta.fireworks.flag.gold"], ["samurai", "Samurai", "samurai.scar.samurai.dragon.sword.orange"], ["spaceman", "Spaceman", "astro.goggles.snow.rocket.none.blue"], ["toxic", "Toxic squad", "gasmask.goggles.hazmat.barrel.none.green"], ["hero", "Super hero", "classic.cyber.hero.wings.cape.gold"], ["beach", "Holiday mode", "cap.shades.hawaii.umbrella.none.pink"], ["agent", "Secret agent", "classic.monocle.agent.chrome.tags.orange"], ["viking", "Sky viking", "viking.paint.urban.barrel.pads.orange"]]
const AV_FULL := ["astro", "marine", "ninja", "pumpkin", "robot"]
const AV_BACK := ["antenna", "cape", "flag", "scarf", "sword"]
const AV_FRONT := ["pet"]
const AV_FLAME := {"orange": [Color(1.000, 0.620, 0.173, 0.922), Color(1.000, 0.953, 0.690, 1.000)], "blue": [Color(0.247, 0.663, 1.000, 0.922), Color(0.847, 0.953, 1.000, 1.000)], "green": [Color(0.361, 1.000, 0.478, 0.922), Color(0.918, 1.000, 0.847, 1.000)], "purple": [Color(0.722, 0.420, 1.000, 0.922), Color(0.949, 0.878, 1.000, 1.000)], "pink": [Color(1.000, 0.310, 0.690, 0.922), Color(1.000, 0.878, 0.949, 1.000)], "gold": [Color(1.000, 0.847, 0.290, 0.922), Color(1.000, 1.000, 1.000, 1.000)], "none": null}
const AV_SLEEVE := {"desert": Color(0.851, 0.698, 0.478), "urban": Color(0.553, 0.576, 0.612), "snow": Color(0.933, 0.949, 0.969), "ninja": Color(0.122, 0.133, 0.188), "jumpsuit": Color(0.910, 0.416, 0.110), "hazmat": Color(0.949, 0.824, 0.106), "mech": Color(0.725, 0.769, 0.824), "hero": Color(0.184, 0.373, 0.839), "agent": Color(0.106, 0.114, 0.165), "kurta": Color(0.965, 0.937, 0.878), "hawaii": Color(0.145, 0.722, 0.659), "samurai": Color(0.545, 0.118, 0.165), "street": Color(0.231, 0.247, 0.345)}
const AV_KEYS := ["h", "f", "o", "j", "x", "fl"]
const AV_DEF := "classic.goggles.army.twin.none.orange"
const AV_BODY_A := Vector2(30.5, 40.5)
const AV_HEAD_A := Vector2(31, 23)
const LK_TABS := [["sets", "LOOKS"], ["h", "HELMET"], ["f", "FACE"], ["o", "OUTFIT"], ["j", "JETPACK"], ["x", "EXTRA"], ["fl", "FLAME"]]
const KB_ROWS := ["1234567890", "QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]

# ===================== SETTINGS (tune here) =====================
const S := {
	"gravity": 850.0, "max_fall": 500.0, "move_speed": 118.0,
	"jump_speed": 240.0, "thrust": 1400.0, "max_rise": 240.0,
	"fuel_max": 100.0, "fuel_drain": 14.0, "refill_ground": 18.0, "refill_air": 4.0,
	"hp_max": 100.0, "regen_delay": 4.0, "regen_rate": 6.0, "respawn": 3.5,
	"match_time": 300.0, "event_every": 60.0, "event_warn": 8.0, "flip_time": 15.0, "flip_ease": 1.6,
	"water_dps": 6.0, "start_grenades": 3, "max_grenades": 3, "max_bombs": 3, "max_smokes": 3,
	"grenade_fuse": 2.5, "grenade_radius": 80.0, "grenade_dmg": 80.0,
	"rocket_radius": 72.0, "rocket_dmg": 70.0, "pickup_respawn": 15.0,
	"aim_turn": 18.0, "mouse_turn": 30.0, "protect": 2.5, "view_h": 390.0, "headshot": 1.6, "crouch_speed": 0.45, "crawl_speed": 0.3,
	"gun_draw": 0.78,
}
const WD := {
	"magnum":  {"name": "MAGNUM",  "dmg": 26.0, "rate": 0.40, "mag": 7,  "spare": 28,  "reload": 1.3, "spread": 0.02,  "speed": 1250.0, "pellets": 1, "life": 0.8,  "chip": 0.5,  "recoil": 4.0, "push": 0.0,   "snd": "magnum", "zooms": [1]},
	"uzi":     {"name": "UZI",     "dmg": 8.0,  "rate": 0.075,"mag": 30, "spare": 120, "reload": 1.5, "spread": 0.13,  "speed": 1100.0, "pellets": 1, "life": 0.45, "chip": 0.25, "recoil": 2.0, "push": 0.0,   "snd": "uzi", "zooms": [1]},
	"ak47":    {"name": "AK-47",   "dmg": 17.0, "rate": 0.11, "mag": 30, "spare": 90,  "reload": 1.9, "spread": 0.045, "speed": 1400.0, "pellets": 1, "life": 0.85, "chip": 0.45, "recoil": 5.0, "push": 0.0,   "snd": "ak47", "zooms": [1, 2]},
	"shotgun": {"name": "SHOTGUN", "dmg": 11.0, "rate": 0.95, "mag": 6,  "spare": 18,  "reload": 2.2, "spread": 0.32,  "speed": 1050.0, "pellets": 8, "life": 0.32, "chip": 0.4,  "recoil": 7.0, "push": 140.0, "snd": "shotgun", "zooms": [1]},
	"sniper":  {"name": "SNIPER",  "dmg": 75.0, "rate": 1.4,  "mag": 5,  "spare": 15,  "reload": 2.5, "spread": 0.004, "speed": 2600.0, "pellets": 1, "life": 0.9,  "chip": 0.8,  "recoil": 8.0, "push": 60.0,  "snd": "sniper", "zooms": [1, 2, 4, 6]},
	"smg":     {"name": "SMG",     "dmg": 10.0, "rate": 0.085,"mag": 32, "spare": 128, "reload": 1.6, "spread": 0.08,  "speed": 1250.0, "pellets": 1, "life": 0.6,  "chip": 0.3,  "recoil": 2.5, "push": 0.0,   "snd": "smg", "zooms": [1]},
	"shock":   {"name": "SHOCK",   "dmg": 14.0, "rate": 0.3,  "mag": 20, "spare": 60,  "reload": 1.8, "spread": 0.0,   "speed": 0.0,    "pellets": 1, "life": 0.0,  "chip": 0.0,  "recoil": 2.0, "push": 0.0,   "snd": "shock", "zooms": [1], "special": "shock"},
	"net":     {"name": "NET GUN", "dmg": 5.0,  "rate": 1.2,  "mag": 3,  "spare": 6,   "reload": 2.0, "spread": 0.02,  "speed": 560.0,  "pellets": 1, "life": 1.3,  "chip": 0.0,  "recoil": 5.0, "push": 0.0,   "snd": "net", "zooms": [1], "special": "net"},
	"laser":   {"name": "LASER",   "dmg": 24.0, "rate": 0.4,  "mag": 12, "spare": 36,  "reload": 1.8, "spread": 0.006, "speed": 0.0,    "pellets": 1, "life": 0.0,  "chip": 0.6,  "recoil": 3.0, "push": 0.0,   "snd": "laser", "zooms": [1, 2], "special": "laser"},
	"minigun": {"name": "MINIGUN", "dmg": 8.0,  "rate": 0.055,"mag": 120,"spare": 240, "reload": 3.0, "spread": 0.1,   "speed": 1350.0, "pellets": 1, "life": 0.6,  "chip": 0.3,  "recoil": 1.5, "push": 0.0,   "snd": "minigun", "zooms": [1]},
	"flame":   {"name": "FIRE BLAZE", "dmg": 3.0, "rate": 0.06, "mag": 60, "spare": 120, "reload": 2.2, "spread": 0.18,  "speed": 430.0,  "pellets": 1, "life": 0.42, "chip": 0.15, "recoil": 0.5, "push": 0.0,   "snd": "flame", "zooms": [1], "special": "flame"},
	"rpg":     {"name": "ROCKET",  "dmg": 0.0,  "rate": 1.5,  "mag": 1,  "spare": 4,   "reload": 2.0, "spread": 0.01,  "speed": 650.0,  "pellets": 1, "life": 3.0,  "chip": 0.0,  "recoil": 9.0, "push": 90.0,  "snd": "rpg", "zooms": [1, 2]},
}
const EVENTS := {
	"water": {"label": "RISING WATER", "tip": "Water will slowly rise. It hurts, and jetpacks don't work in it."},
	"roof": {"label": "FALLING ROCKS", "tip": "Rocks will drop one by one where you see the red shadows."},
	"brk": {"label": "BREAKING GROUND", "tip": "The shaking ground will crumble away bit by bit."},
	"flip": {"label": "ANTIGRAVITY FLIP", "tip": "Everyone will slowly fall to the ceiling. Up still means fly."},
}
# ================================================================

# in team games, only these can hurt your own teammates
const FF_GUNS := ["bomb", "smoke", "flame", "minigun"]
const ZOOM_MULT := {1: 1.0, 2: 1.35, 4: 1.8, 6: 2.3}
const POSTURE := {"stand": Vector2(20, 42), "crouch": Vector2(20, 32), "prone": Vector2(40, 18)}
const T := 32
const COLS := 120
const ROWS := 46
const WW := COLS * T
const WH := ROWS * T
const EMPTY := 0
const DIRT := 1
const ROCK := 2
const WOOD := 3
const CRATE := 4
const TILE_HP := {1: 8.0, 3: 4.0, 4: 3.0}

# dirt islands [col, row, length] (2 tiles thick), wood bridges [col, row, length]
const ISLANDS := [[16,34,8],[30,31,9],[46,28,8],[56,24,10],[66,28,8],[81,31,9],[96,34,8],[22,24,7],[38,20,8],[52,15,7],[61,15,7],[74,20,8],[90,24,7],[10,18,6],[104,18,6],[30,11,6],[84,11,6],[56,7,8]]
const BASES := [[2,30,9],[109,30,9]]
const BRIDGES := [[52,38,17],[11,25,6],[103,25,6]]
const CRATES := [[23,33],[38,30],[81,30],[96,33],[22,23],[96,23],[38,19],[81,19],[10,17],[109,17]]
# pickup spots: [col, row (-1 = ground), type, guns]
const ITEM_SPOTS := [
	[60, 7, "gun", ["sniper", "rpg", "laser", "minigun"]], [55, 15, "health", []], [64, 15, "grenade", []],
	[42, 20, "gun", ["ak47", "shotgun", "smg", "flame"]], [78, 20, "gun", ["ak47", "shotgun", "smg", "flame"]],
	[38, 20, "smoke", []], [82, 20, "smoke", []],
	[25, 24, "health", []], [93, 24, "health", []],
	[50, 28, "gun", ["rpg", "ak47", "net", "minigun"]], [70, 28, "gun", ["rpg", "ak47", "net", "flame"]], [61, 24, "gun", ["uzi", "magnum", "shock"]],
	[34, 31, "gun", ["shotgun", "sniper", "laser"]], [85, 31, "gun", ["shotgun", "sniper", "laser"]],
	[20, 34, "gun", ["magnum", "uzi", "smg"]], [100, 34, "gun", ["magnum", "uzi", "smg"]],
	[13, 18, "bomb", []], [107, 18, "bomb", []],
	[33, 11, "gun", ["ak47", "sniper", "shock"]], [87, 11, "gun", ["ak47", "sniper", "net"]],
	[44, 30, "health", []], [76, 30, "health", []], [60, 38, "grenade", []],
]

const NAMES := ["You", "Ravi", "Kiran", "Sana", "Arjun", "Meera"]
const TEAMS := ["yellow", "blue", "red", "purple", "green", "orange"]
const TEAM_COL := [Color("#f2c230"), Color("#3fa9f5"), Color("#e8553f"), Color("#9b6bea"), Color("#5cc45a"), Color("#f08a24")]
# bot personalities: reaction (s), aim error (rad), aim turn speed, keep distance, liked guns, grenade use, retreat hp, chat lines
const STYLES := {
	"rusher":    {"react": 0.28, "err": 0.13, "turn": 8.0, "dist": 120.0, "likes": ["shotgun", "uzi", "smg", "shock", "flame"], "nade": 0.25, "retreat": 25.0, "chat": ["Come here!", "Too slow!", "Easy!"]},
	"sniper":    {"react": 0.6, "err": 0.09, "turn": 4.5, "dist": 480.0, "likes": ["sniper", "ak47", "laser"], "nade": 0.1, "retreat": 45.0, "chat": ["Headshot!", "Got you.", "Nice try"]},
	"balanced":  {"react": 0.32, "err": 0.10, "turn": 7.0, "dist": 260.0, "likes": ["ak47", "magnum", "minigun"], "nade": 0.3, "retreat": 35.0, "chat": ["gg", "Next!", "Sorry bro"]},
	"grenadier": {"react": 0.34, "err": 0.12, "turn": 6.5, "dist": 300.0, "likes": ["rpg", "shotgun", "net", "minigun"], "nade": 0.6, "retreat": 35.0, "chat": ["Boom!", "Fire in the hole!", "Hehe"]},
	"cautious":  {"react": 0.30, "err": 0.09, "turn": 7.0, "dist": 340.0, "likes": ["ak47", "sniper"], "nade": 0.35, "retreat": 60.0, "chat": ["Got you", "Stay down", "lol"]},
}
const BOT_STYLE := ["balanced", "rusher", "sniper", "balanced", "grenadier", "cautious"]

const C_INK := Color("#f4f6ff")
const C_MUTED := Color("#b9c2dc")
const C_ARC := Color("#ffd84a")
const C_CYAN := Color("#5ef0ff")
const C_PINK := Color("#ff5ea8")
const C_RED := Color("#ff4d5e")
const C_GREEN := Color("#62e07a")
const C_OUT := Color("#1b1d2a")

class Player:
	var id := 0
	var pname := ""
	var team := "yellow"
	var color := Color.WHITE
	var bot := false
	var actor := false
	var look := {}
	var spawn_set := false
	var shoot_buf := 0.0
	var jit_last := Vector2.ZERO
	var jit_prev := Vector2.ZERO
	var jit_ok := false
	var press_hold := {}
	var sbuf: Array = []
	var fire_lock := false
	var spawn_pt := Vector2.ZERO
	var last_spawn := Vector2.ZERO
	var born_t := -9.0
	var shot_n := 0
	var last_fire_t := -9.0
	var hist: Array = []
	var lat := 0.0
	var uid := ""
	var dropped := false
	var svx := 0.0
	var ack := 0
	var svy := 0.0
	var pfuel := 0.0
	var jst_t := -9.0
	var grunt_t := -9.0
	var spin := 0.0
	var burn_t := 0.0
	var burn_by = null
	var smokes := 0
	var snd_t := -9.0
	var cough_t := -9.0
	var whiz_t := -9.0
	var sizzle_t := -9.0
	var hs := 0
	var best := 0
	var mk := 0
	var bk := 0
	var lstreak := 0
	var remote := false
	var peer_id := 0
	var nx := 0.0
	var ny := 0.0
	var naim := 0.0
	var snap_age := 0.0
	var style := ""
	var w := 20.0
	var h := 42.0
	var x := 0.0
	var y := 0.0
	var vx := 0.0
	var vy := 0.0
	var hp := 100.0
	var fuel := 100.0
	var alive := true
	var respawn_t := 0.0
	var slots: Array = [null, null]
	var cur := 0
	var grenades := 3
	var fire_cd := 0.0
	var reload_t := 0.0
	var melee_cd := 0.0
	var g_cd := 0.0
	var last_hit_t := -9.0
	var last_hit_by = null
	var last_cause := ""
	var last_gun := ""
	var last_head := false
	var kills := 0
	var deaths := 0
	var streak := 0
	var aim := 0.0
	var on_ground := false
	var was_ground := false
	var hit_wall := false
	var in_water := false
	var flash := 0.0
	var jet_on := false
	var walk := 0.0
	var recoil := 0.0
	var muzzle_t := 0.0
	var shot_t := -9.0
	var inp := {"mx": 0.0, "fly": false, "shoot": false, "swap": false, "grenade": false, "melee": false, "reload": false, "aim": 0.0, "down": false, "pick": "", "zoom": false, "bomb": false, "smoke": false}
	var prev := {}
	var melee_anim := 0.0
	var posture := "stand"
	var air_t := 0.0
	var draw_aim := 0.0
	var leg_b := 0.0
	var leg_f := 0.0
	var shin_b := 0.0
	var shin_f := 0.0
	var protect_t := 0.0
	var stun_t := 0.0
	var net_t := 0.0
	var bombs := 0
	var switch_t := 0.0
	var side := 0
	var st := {}
	var near_k = null
	var near_t := -9.0
	var dual_side := 0
	var reload_total := 1.0
	var reload_k := 0.0
	var crouch_roll := 1.0
	var say := ""
	var say_t := 0.0
	# bot brain
	var think_t := 0.0
	var aim_err := 0.0
	var aim_want := 0.0
	var see_t := 0.0
	var strafe := 1.0
	var strafe_t := 0.0
	var saving := false
	var stuck_t := 0.0
	var lx := 0.0
	var ly := 0.0
	var target = null
	var target_pos := Vector2.ZERO
	var target_seen_t := -9.0
	var goal = null
	var roam := Vector2.ZERO
	var roam_t := 0.0
	var burst_t := 0.0
	var pause_t := 0.0
	var dodge_t := 0.0
	var detour := 1.0
	var detour_t := 0.0
	var prog_d := 1e9
	var prog_t := 0.0

class Pickup:
	var type := ""
	var gun := ""
	var ammo = null
	var x := 0.0
	var y := 0.0
	var w := 24.0
	var h := 16.0
	var vx := 0.0
	var vy := 0.0
	var on_ground := false
	var hit_wall := false
	var ttl := 1e9
	var spawner = null

class Spawner:
	var x := 0.0
	var y := 0.0
	var type := ""
	var pool: Array = []
	var timer := 0.0
	var item = null

class Bullet:
	var x := 0.0
	var y := 0.0
	var vx := 0.0
	var vy := 0.0
	var life := 0.0
	var dmg := 0.0
	var chip := 0.0
	var owner = null
	var rocket := false
	var net := false
	var flame := false
	var max_life := 1.0
	var gun := ""
	var ff := 0.0

class Grenade:
	var x := 0.0
	var y := 0.0
	var vx := 0.0
	var vy := 0.0
	var rot := 0.0
	var fuse := 2.0
	var owner = null
	var kind := "frag"
	var stuck := false
	var beep_t := 0.0

class Part:
	var x := 0.0
	var y := 0.0
	var vx := 0.0
	var vy := 0.0
	var life := 0.0
	var max_life := 1.0
	var color := Color.WHITE
	var size := 3.0
	var size1 := 3.0
	var g := 0.0
	var tex := ""
	var rot := 0.0
	var spin := 0.0

class Corpse:
	var x := 0.0
	var y := 0.0
	var vx := 0.0
	var vy := 0.0
	var rot := 0.0
	var spin := 0.0
	var team := ""
	var look := {}
	var t := 0.0
	var face := 1.0

class Block:
	var c := 0
	var y := 0.0
	var vy := 0.0
	var hit := {}

class Ev:
	var name := ""
	var phase := "warn"
	var t := 0.0
	var dur := 0.0
	var cols: Array = []
	var tiles: Array = []
	var spawned := 0

var zones: Array = []
var map_id := "sky"
var bases_v: Array = []
var item_spots: Array = []
var water_row := 36
var roam_pts: Array = []
var surf_runs: Array = []
var torches: Array = []
const MAP_LIST := ["sky", "outpost", "catacombs"]
const MAP_NAMES := {"sky": "Sky Islands", "outpost": "Outpost", "catacombs": "Catacombs", "random": "Random"}
const OUTPOST_SPOTS := [
	[50, 8, "gun", ["sniper", "rpg", "laser", "minigun"]], [59, 9, "health", []],
	[35, 20, "gun", ["ak47", "shotgun", "smg", "flame"]], [84, 20, "gun", ["ak47", "shotgun", "smg", "flame"]],
	[24, 18, "health", []], [95, 18, "health", []],
	[53, 26, "gun", ["uzi", "magnum", "shock", "net"]], [66, 26, "gun", ["smg", "ak47", "rpg"]],
	[55, 32, "grenade", []], [64, 32, "smoke", []],
	[15, 12, "gun", ["sniper", "laser"]], [104, 12, "gun", ["sniper", "laser"]],
	[33, 6, "bomb", []], [86, 6, "bomb", []],
	[42, 30, "gun", ["magnum", "uzi", "smg"]], [78, 30, "gun", ["magnum", "uzi", "minigun"]],
	[30, 30, "smoke", []], [89, 30, "grenade", []],
]
const CATA_SPOTS := [
	[20, 4, "gun", ["sniper", "rpg", "laser", "minigun"]], [100, 4, "gun", ["sniper", "rpg", "laser", "minigun"]],
	[60, 3, "health", []],
	[17, 15, "health", []], [102, 15, "health", []],
	[46, 14, "gun", ["ak47", "shotgun", "smg", "flame"]], [74, 14, "gun", ["ak47", "shotgun", "smg", "flame"]],
	[54, 23, "smoke", []], [66, 23, "grenade", []],
	[26, 31, "gun", ["magnum", "uzi", "shock", "net"]], [94, 31, "gun", ["magnum", "uzi", "smg", "net"]],
	[60, 34, "health", []], [40, 31, "bomb", []], [80, 31, "bomb", []], [11, 31, "grenade", []],
	[70, 31, "smoke", []],
]

var cfg := {
	"mode": "ffa", "bots": 5, "skill": "normal", "minutes": 5, "event_every": 60,
	"ev_water": true, "ev_roof": true, "ev_brk": true, "ev_flip": false, "zones": false, "map": "sky",
	"fire_mode": "auto", "sticks": "floating", "stick_size": 1.0, "btn_size": 1.0, "opacity": 0.7,
	"left_handed": false, "aim_sens": "medium", "vibration": true, "sound": true,
	"name": "", "show_fps": false, "lan_bots": 2, "look": "", "server": "", "uid": "", "my_side": 0,
}
const MATCH_ROWS := [
	["map", "Map", ["sky", "outpost", "catacombs", "random"], ["Sky Islands", "Outpost", "Catacombs", "Random"]],
	["mode", "Game mode", ["ffa", "team"], ["Free for all", "Teams"]],
	["my_side", "Your team (Teams)", [0, 1], ["Blue", "Red"]],
	["bots", "Bots", [1, 2, 3, 4, 5], ["1", "2", "3", "4", "5"]],
	["skill", "Bot skill", ["easy", "normal", "hard"], ["Easy", "Normal", "Hard"]],
	["minutes", "Match length", [3, 5, 10], ["3 min", "5 min", "10 min"]],
	["event_every", "Map event every", [45, 60, 90], ["45 sec", "60 sec", "90 sec"]],
	["ev_water", "Rising water", [true, false], ["On", "Off"]],
	["ev_roof", "Falling rocks", [true, false], ["On", "Off"]],
	["ev_brk", "Breaking ground", [true, false], ["On", "Off"]],
	["ev_flip", "Antigravity flip", [false, true], ["Off", "On"]],
	["zones", "Gravity zones", [false, true], ["Off", "On"]],
]
const LAN_ROWS := [
	["map", "Map", ["sky", "outpost", "catacombs", "random"], ["Sky Islands", "Outpost", "Catacombs", "Random"]],
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
const CONTROL_ROWS := [
	["fire_mode", "Shooting", ["auto", "button"], ["Aim stick fires", "Fire button"]],
	["sticks", "Joysticks", ["floating", "fixed"], ["Follow thumb", "Fixed place"]],
	["stick_size", "Joystick size", [0.85, 1.0, 1.2], ["Small", "Medium", "Large"]],
	["btn_size", "Button size", [0.85, 1.0, 1.2], ["Small", "Medium", "Large"]],
	["opacity", "Controls see-through", [0.4, 0.7, 1.0], ["Light", "Medium", "Solid"]],
	["left_handed", "Left-handed", [false, true], ["Off", "On"]],
	["aim_sens", "Aim sensitivity", ["low", "medium", "high"], ["Low", "Medium", "High"]],
	["vibration", "Vibration", [true, false], ["On", "Off"]],
	["sound", "Sound", [true, false], ["On", "Off"]],
	["show_fps", "Show FPS", [false, true], ["Off", "On"]],
]
var ui_btns: Array = []
var match_time := 300.0
var event_every := 60.0
var pause_rect := Rect2()

var tiles := PackedByteArray()
var thp := PackedFloat32Array()
var state := "menu"
var t := 0.0
var g_dir := 1.0
var g_target := 1.0
var water_y := float(WH)
var next_event := 60.0
var last_event := ""
var ev: Ev = null
var shake := 0.0
var players: Array = []
var bullets: Array = []
var grenades_list: Array = []
var parts: Array = []
var pickups: Array = []
var spawners: Array = []
var blocks: Array = []
var corpses: Array = []
var clouds: Array = []
var feed: Array = []
var big_msg := ""
var big_t := 0.0
var hurt_t := 0.0
var hitmark_t := 0.0

var sw := 1280.0
var sh := 720.0
var u := 1.0
var zoom := 1.0
var view_h := 390.0
var cam := Vector2.ZERO
var safe_l := 0.0
var safe_r := 0.0
var font: Font
var time_s := 0.0
var tex := {}
var snd := {}
var players_pool: Array = []
var jet_player: AudioStreamPlayer

# input
var mouse_pos := Vector2.ZERO
var mouse_down := false
var mouse_used := false
var touch_mode := false
var stick_l = null
var stick_r = null
var btn_held := {}
var last_touch_aim := 0.0
var menu_btn := Rect2()
var pick_request := ""
var bubbles: Array = []
var tracers: Array = []
var last_buzz := -9.0
var zoom_request := false
var bubble_on := false
var bubble_pos := Vector2.ZERO
var bubble_r := 30.0
var last_delta := 0.016

# LAN
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
var feed_sig := ""
var feed_send := 0
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
var dbg_size := false
var lantest_join := ""
var lantest_time := 0.0
var lt_wait := 0.0
var lt_done := 0.0
var lt_moved := 0.0
var lan_shots: Array = []
var shots_quit := false
var shot_wait := 0

# test hooks
var autotest := false
var start_dirt := 0
var explosions := 0
var guns_used := {}
var post_count := {"stand": 0, "crouch": 0, "prone": 0}
var seen_events := {}
var shot_at := -1.0
var shot_name := ""
var shot_frames := 0

func load_cfg() -> void:
	var f := ConfigFile.new()
	if f.load("user://settings.cfg") == OK:
		for k in cfg.keys():
			cfg[k] = f.get_value("s", k, cfg[k])
	apply_cfg()

func save_cfg() -> void:
	var f := ConfigFile.new()
	for k in cfg.keys():
		f.set_value("s", k, cfg[k])
	f.save("user://settings.cfg")
	apply_cfg()

func apply_cfg() -> void:
	AudioServer.set_bus_mute(0, not cfg.sound)

func aim_rate(mouse: bool) -> float:
	var m: float = {"low": 0.65, "medium": 1.0, "high": 1.6}.get(cfg.aim_sens, 1.0)
	return (S.mouse_turn if mouse else S.aim_turn) * m

func enemy(a, b) -> bool:
	if a == null or b == null or a == b:
		return false
	return cfg.mode != "team" or a.side != b.side

func make_style(style: String) -> Dictionary:
	var st: Dictionary = STYLES[style].duplicate()
	match cfg.skill:
		"easy":
			st.react += 0.3
			st.err *= 1.7
			st.turn *= 0.7
			st.nade *= 0.6
		"hard":
			st.react = maxf(0.15, st.react - 0.1)
			st.err *= 0.7
			st.turn *= 1.25
	return st

func _ready() -> void:
	randomize()
	load_cfg()
	font = ThemeDB.fallback_font
	load_fonts()
	DisplayServer.screen_set_keep_on(true)
	if OS.has_feature("mobile"):
		Engine.max_fps = 60
	for n in ["dirt0", "dirt1", "dirt2", "grass", "rock", "wood", "crate", "crack1", "crack2", "bg_mountains", "bg_hills", "bg_near",
			"sand0", "sand1", "sand2", "sandcap", "concrete", "bg_out_far", "bg_out_mid", "bg_out_near",
			"cave0", "cave1", "cave2", "moss", "brick", "torch", "bg_cat_far", "bg_cat_mid",
			"cloud0", "cloud1", "cloud2", "glow", "fireball", "smoke", "flash", "grenade", "medkit", "leg", "jetpack", "hand", "knife", "timebomb", "net_overlay", "smoke_can", "flame"]:
		tex[n] = load("res://art/%s.png" % n)
	for tm in TEAMS:
		tex["head_" + tm] = load("res://art/head_%s.png" % tm)
		tex["torso_" + tm] = load("res://art/torso_%s.png" % tm)
	for g in WD.keys():
		tex["gun_" + g] = load("res://art/gun_%s.png" % g)
	for n in AV_RECT.keys():
		tex["av_" + n] = load("res://art/av/%s.png" % n)
	for o in AV_LIST["o"]:
		if o[0] != "army":
			tex["leg_" + o[0]] = load("res://art/av/leg_%s.png" % o[0])
	default_look = parse_look(AV_DEF)
	if str(cfg.uid) == "":
		cfg.uid = "%08x%08x" % [randi(), randi()]
		save_cfg()
	for n in ["magnum", "uzi", "ak47", "shotgun", "sniper", "rpg", "explosion", "jet", "reload", "empty", "swap", "pickup", "hit", "headshot", "throw", "land", "warn", "crumble", "melee", "smg", "shock", "net", "laser", "beep", "slash",
			"kill", "death", "suicide", "arm", "rack", "hiss", "cough", "spin", "minigun", "flame", "sizzle", "heart", "whiz", "splash", "tick", "crown", "spawn", "die0", "die1", "die2", "ow0", "ow1",
			"tink", "ui_ok", "bomb_boom", "jetstart", "locked", "wdrop", "equip2",
			"jump", "ui_click", "wpick", "ev_water", "ev_rocks", "ev_brk", "ev_flip", "crate", "match_end", "lost_lead", "item_respawn", "low_fuel", "health"]:
		snd[n] = load("res://sfx/%s.wav" % n)
	var jet: AudioStreamWAV = snd.jet
	jet.loop_mode = AudioStreamWAV.LOOP_FORWARD
	jet.loop_begin = 0
	jet.loop_end = jet.data.size() / 2
	for i in 14:
		var a := AudioStreamPlayer.new()
		add_child(a)
		players_pool.append(a)
	jet_player = AudioStreamPlayer.new()
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
		loop_players[pn] = ap
	gen_map()
	cam = Vector2(WW / 2.0 - 400, 8 * T)
	multiplayer.peer_disconnected.connect(_on_peer_gone)
	multiplayer.connected_to_server.connect(_on_connected)
	multiplayer.connection_failed.connect(_on_conn_failed)
	multiplayer.server_disconnected.connect(_on_server_gone)
	var args := OS.get_cmdline_user_args()
	for a in args:
		if a.begins_with("--map="):
			cfg.map = a.substr(6)
		if a == "--lantest-host":
			lantest_host = true
			lantest_time = 45.0
			Engine.max_fps = 60
			cfg.name = "Host"
			cfg.uid = "test-host"
			cfg.lan_bots = 2
			if args.has("--team"):
				cfg.mode = "team"
			host_game()
		if a.begins_with("--lantest-join="):
			lantest_join = a.substr(15)
			lantest_time = 45.0
			Engine.max_fps = 60
			cfg.name = "Tester"
			cfg.uid = "test-tester"
			if lantest_join == "auto":
				state = "lan_join"
			else:
				join_game(lantest_join)
		if a.begins_with("--lanshot="):
			for spec in a.substr(10).split(","):
				lan_shots.append(spec.split(":"))
		if a == "--netsize":
			dbg_size = true
		if a == "--dedicated":
			var dport := 25001
			var droom := "TEST"
			for a2 in args:
				if a2.begins_with("--port="):
					dport = int(a2.substr(7))
				if a2.begins_with("--room="):
					droom = a2.substr(7)
				if a2 == "--stay":
					stay_open = true
				if a2.begins_with("--matchsecs="):
					lantest_time = float(a2.substr(12))
			dedicated_start(dport, droom)
		if a.begins_with("--lag="):
			lag_ms = int(a.substr(6))
		if a.begins_with("--server="):
			cfg.server = a.substr(9)
		if a.begins_with("--online-create"):
			lantest_time = 45.0
			Engine.max_fps = 60
			cfg.name = "Owner"
			cfg.uid = "test-owner"
			lantest_join = "online"
			mm_query("new", a.substr(16) if a.length() > 16 else "TEST1")
		if a.begins_with("--online-join="):
			lantest_time = 45.0
			Engine.max_fps = 60
			cfg.name = "Friend"
			cfg.uid = "test-friend"
			lantest_join = "online"
			mm_query("join", a.substr(14))
		if a == "--drop-test":
			drop_test = true
		if a.begins_with("--hold="):
			lt_hold = float(a.substr(7))
		if a.begins_with("--pick="):
			test_pick = int(a.substr(7))
		if a.begins_with("--state="):
			state = a.substr(8)
		if a.begins_with("--look="):
			cfg.look = a.substr(7)
		if a.begins_with("--lktab="):
			lk_tab = a.substr(8)
		if a.begins_with("--name="):
			cfg.name = a.substr(7)
		if a == "--lockertest":
			for act in ["locker", "lk_tab:h", "lk_pick:h:viking", "lk_pick:fl:pink", "lk_pick:x:cape"]:
				do_action(act)
			print("LT look1=", cfg.look, " state=", state)
			do_action("lk_pick:sets:" + AV_SETS[4][2])
			print("LT look2=", cfg.look)
			do_action("lk_name")
			for i in 20:
				name_key("DEL")
			for k in ["R", "A", "V", "I", "SPACE", "K", "1", "!", "SPACE", "SPACE", "X", "Y", "Z", "W", "Q"]:
				name_key(k)
			print("LT entry=[", name_entry, "]")
			do_action("name_ok")
			print("LT name=", cfg.name, " state=", state, " my_look=", my_look())
			do_action("lk_rand")
			print("LT rand=", cfg.look, " parse_bad=", parse_look("zzz.qq"))
			do_action("lk_done")
			print("LT back=", state)
			get_tree().quit()
		if a == "--shots-quit":
			shots_quit = true
	if args.has("--dumpmap"):
		map_id = pick_map()
		gen_map()
		for r in ROWS:
			var line := ""
			for c in COLS:
				line += [".", "#", "R", "=", "C"][tiles[r * COLS + c]]
			print(line)
		get_tree().quit()
		return
	if args.has("--carrytest"):
		reset_match()
		var me: Player = players[0]
		me.slots = [full_slot("magnum"), full_slot("ak47")]
		me.cur = 0
		var k := make_pickup("gun", me.x, me.y, "sniper")
		pickups.append(k)
		print("holding magnum+ak, sniper options: ", pickup_opts(me, k), " auto-take: ", give_gun(me, "sniper", null))
		apply_pick(me, k, "swap")
		print("after swap: ", me.slots[0].type, " + ", me.slots[1].type, " current=", me.slots[me.cur].type)
		var k2 := make_pickup("gun", me.x, me.y, "magnum")
		pickups.append(k2)
		me.cur = 0
		print("magnum on floor while holding magnum: ", pickup_opts(me, k2))
		apply_pick(me, k2, "dual")
		print("dual magnum: ", me.slots[0].get("dual", false))
		me.slots = [full_slot("uzi"), null]
		print("uzi + empty slot, pick shotgun auto: ", give_gun(me, "shotgun", null), " -> ", me.slots[1].type)
		print("then pick AK auto: ", give_gun(me, "ak47", null))
		me.grenades = 3
		var gp := make_pickup("grenade", 0, 0)
		print("grenades at 3, pick more: ", try_pickup(me, gp), " count ", me.grenades)
		me.bombs = 3
		print("bombs at 3, pick more: ", try_pickup(me, make_pickup("bomb", 0, 0)))
		get_tree().quit()
		return
	if args.has("--rowtest"):
		var bad := 0
		for row in MATCH_ROWS + CONTROL_ROWS + LAN_ROWS:
			var before = cfg[row[0]]
			do_action("row:" + row[0])
			if cfg[row[0]] == before:
				bad += 1
				print("NOT CHANGED: ", row[0])
			do_action("row:" + row[0])
		print("rowtest done, unchanged rows: ", bad)
		get_tree().quit()
		return
	if args.has("--autotest"):
		autotest = true
		cfg.bots = 5
		cfg.ev_flip = true
		cfg.zones = true
		if args.has("--team"):
			cfg.mode = "team"
		reset_match()
		players[my_idx].bot = true
		state = "play"
	for a in args:
		if a.begins_with("--screen="):
			state = a.substr(9)
		if a == "--zoomtest":
			zoom_test = true
			cfg.bots = 0
			reset_match()
			state = "play"
		if a == "--watch":
			reset_match()
			players[my_idx].bot = true
			state = "play"
		if a.begins_with("--shot="):
			var bits: PackedStringArray = a.substr(7).split(":")
			shot_at = float(bits[0])
			shot_name = bits[1]
			touch_mode = bits.size() > 2
			if shot_at > 0:
				reset_match()
				players[my_idx].bot = true
				state = "play"

# ---------------- sound ----------------
func play(name: String, pos = null, vol := 0.0, pitch_var := 0.08) -> void:
	play_l(name, pos, vol, pitch_var)
	if net_role == "host":
		net_fx.append(["s", name, pos, vol])

func play_l(name: String, pos = null, vol := 0.0, pitch_var := 0.08) -> void:
	if autotest or shot_at >= 0:
		return
	var db := vol
	if pos != null:
		var center_w := cam + Vector2(sw, sh) / zoom / 2.0
		var d: float = (pos - center_w).length()
		if d > 1400:
			return
		db -= clampf(d / 1100.0, 0, 1) * 22.0
	for a in players_pool:
		if not a.playing:
			a.stream = snd[name]
			a.volume_db = db
			a.pitch_scale = 1.0 + randf_range(-pitch_var, pitch_var)
			a.play()
			return

# ---------------- map ----------------
func set_tile(c: int, r: int, v: int) -> void:
	if c < 1 or c >= COLS - 1 or r < 1 or r >= ROWS - 1:
		return
	tiles[r * COLS + c] = v
	thp[r * COLS + c] = TILE_HP.get(v, 99.0)
	if net_role == "host":
		tile_dirty[r * COLS + c] = true

func ground_top(c: int) -> int:
	if c >= 52 and c <= 68:
		return 42
	return clampi(40 - roundi(2.4 * sin(c * 0.085 + 0.4) + 1.2 * sin(c * 0.21)), 37, 42)

func fill(c0: int, r0: int, c1: int, r1: int, v: int) -> void:
	for r in range(r0, r1 + 1):
		for c in range(c0, c1 + 1):
			set_tile(c, r, v)

func carve_ellipse(cx: int, cy: int, rx: int, ry: int) -> void:
	for r in range(cy - ry, cy + ry + 1):
		for c in range(cx - rx, cx + rx + 1):
			var dx := float(c - cx) / rx
			var dy := float(r - cy) / ry
			if dx * dx + dy * dy <= 1.0:
				set_tile(c, r, EMPTY)

func pick_map() -> String:
	if cfg.map == "random" or not MAP_LIST.has(cfg.map):
		return MAP_LIST[randi() % MAP_LIST.size()]
	return cfg.map

func gen_map() -> void:
	tiles = PackedByteArray()
	tiles.resize(COLS * ROWS)
	tiles.fill(0)
	thp = PackedFloat32Array()
	thp.resize(COLS * ROWS)
	for c in COLS:
		for r in [0, ROWS - 1, ROWS - 2]:
			tiles[r * COLS + c] = ROCK
	for r in ROWS:
		tiles[r * COLS] = ROCK
		tiles[r * COLS + COLS - 1] = ROCK
	torches = []
	match map_id:
		"outpost":
			build_outpost()
		"catacombs":
			build_catacombs()
		_:
			build_sky()
	for bs in bases_v:
		for xx in bs[2]:
			set_tile(bs[0] + xx, bs[1], ROCK)
	compute_nav()

func build_sky() -> void:
	bases_v = BASES
	item_spots = ITEM_SPOTS
	water_row = 36
	zones = [
		{"type": "low", "rect": Rect2(44*T, 3*T, 32*T, 14*T), "g": 0.35, "f": 0.5},
		{"type": "heavy", "rect": Rect2(80*T, 28*T, 22*T, 12*T), "g": 1.8, "f": 2.0},
	]
	for c in range(1, COLS - 1):
		for r in range(ground_top(c), ROWS - 2):
			set_tile(c, r, DIRT)
	for isl in ISLANDS:
		for xx in isl[2]:
			set_tile(isl[0] + xx, isl[1], DIRT)
		for xx in range(1, isl[2] - 1):
			set_tile(isl[0] + xx, isl[1] + 1, DIRT)
	for b in BRIDGES:
		for xx in b[2]:
			set_tile(b[0] + xx, b[1], WOOD)
	for pc in [26, 92]:
		for xx in 2:
			for k in 3:
				set_tile(pc + xx, ground_top(pc + xx) - 1 - k, ROCK)
	for xx in 4:
		set_tile(58 + xx, 7, ROCK)
	for bs in BASES:
		for xx in bs[2]:
			set_tile(bs[0] + xx, bs[1] + 1, ROCK)
	for cr in CRATES:
		set_tile(cr[0], cr[1], CRATE)

# desert army base: bunkers at both ends, watchtowers, a two-floor building in the middle
func build_outpost() -> void:
	bases_v = [[2, 31, 9], [109, 31, 9]]
	item_spots = OUTPOST_SPOTS
	water_row = 37
	zones = [
		{"type": "low", "rect": Rect2(44*T, 2*T, 32*T, 20*T), "g": 0.35, "f": 0.5},
		{"type": "heavy", "rect": Rect2(47*T, 32*T, 26*T, 8*T), "g": 1.8, "f": 2.0},
	]
	for c in range(1, COLS - 1):
		var g := 40 - roundi(1.4 * sin(c * 0.07) + 0.7 * sin(c * 0.19 + 1.0))
		fill(c, g, c, ROWS - 3, DIRT)
		fill(c, ROWS - 4, c, ROWS - 3, ROCK)
	# bunkers (spawn on the roof, door on the inner side)
	fill(1, 31, 12, 32, ROCK)
	fill(12, 33, 12, 35, ROCK)
	fill(107, 31, 118, 32, ROCK)
	fill(107, 33, 107, 35, ROCK)
	for c in range(2, 12):
		fill(c, 33, c, 38, EMPTY)
	for c in range(108, 118):
		fill(c, 33, c, 38, EMPTY)
	# watchtowers
	for tx in [22, 92]:
		fill(tx, 22, tx + 5, 22, WOOD)
		fill(tx + 1, 17, tx + 4, 17, WOOD)
	# the compound
	fill(46, 24, 73, 24, ROCK)
	fill(57, 24, 62, 24, EMPTY)
	fill(46, 25, 46, 41, ROCK)
	fill(73, 25, 73, 41, ROCK)
	fill(46, 35, 46, 39, EMPTY)
	fill(73, 35, 73, 39, EMPTY)
	fill(46, 27, 46, 29, EMPTY)
	fill(73, 27, 73, 29, EMPTY)
	fill(47, 31, 72, 31, WOOD)
	fill(58, 31, 61, 31, EMPTY)
	for c in range(47, 73):
		fill(c, 25, c, 30, EMPTY)
		var g2 := 40 - roundi(1.4 * sin(c * 0.07) + 0.7 * sin(c * 0.19 + 1.0))
		fill(c, 32, c, g2 - 1, EMPTY)
	set_tile(50, 30, CRATE)
	set_tile(69, 30, CRATE)
	# antenna deck and side cover
	fill(54, 11, 65, 11, WOOD)
	fill(32, 28, 40, 28, ROCK)
	set_tile(32, 27, DIRT)
	set_tile(40, 27, DIRT)
	fill(79, 28, 87, 28, ROCK)
	set_tile(79, 27, DIRT)
	set_tile(87, 27, DIRT)
	fill(12, 16, 19, 16, ROCK)
	fill(100, 16, 107, 16, ROCK)
	fill(30, 10, 36, 10, WOOD)
	fill(83, 10, 89, 10, WOOD)
	# sandbag walls and crates on the ground
	for sx in [37, 82]:
		var g3 := surface_below(sx, 30)
		fill(sx, g3 - 2, sx + 1, g3 - 1, DIRT)
	for cx2 in [27, 43, 76, 98]:
		set_tile(cx2, surface_below(cx2, 30) - 1, CRATE)

# underground: tunnels, a great hall with bridges, side chambers and a crypt that floods
func build_catacombs() -> void:
	bases_v = [[3, 25, 9], [108, 25, 9]]
	item_spots = CATA_SPOTS
	water_row = 37
	zones = [
		{"type": "low", "rect": Rect2(40*T, 11*T, 40*T, 10*T), "g": 0.35, "f": 0.5},
		{"type": "heavy", "rect": Rect2(48*T, 33*T, 24*T, 8*T), "g": 1.8, "f": 2.0},
	]
	fill(1, 1, COLS - 2, ROWS - 3, DIRT)
	fill(1, ROWS - 4, COLS - 2, ROWS - 3, ROCK)
	for c in range(3, COLS - 3):
		var top := 5 + roundi(1.2 * sin(c * 0.13))
		var bot := 10 + roundi(1.0 * sin(c * 0.09 + 2.0))
		fill(c, top, c, bot, EMPTY)
	carve_ellipse(15, 20, 12, 6)
	carve_ellipse(105, 20, 12, 6)
	fill(4, 25, 27, 27, DIRT)
	fill(93, 25, 116, 27, DIRT)
	fill(25, 19, 40, 23, EMPTY)
	fill(80, 19, 95, 23, EMPTY)
	carve_ellipse(60, 20, 22, 10)
	for c in range(3, COLS - 3):
		fill(c, 33 + roundi(sin(c * 0.2)), c, 40, EMPTY)
	for sx in [9, 33, 86, 110]:
		fill(sx, 8, sx + 3, 35, EMPTY)
	fill(58, 29, 61, 34, EMPTY)
	fill(44, 22, 76, 22, WOOD)
	fill(57, 22, 63, 22, EMPTY)
	fill(50, 23, 50, 29, ROCK)
	fill(70, 23, 70, 29, ROCK)
	for tx in [20, 45, 74, 98]:
		fill(tx, 39, tx + 2, 40, ROCK)
	for ac in range(7, 113, 13):   # crypt arches hanging from the ceiling
		if ac < 57 or ac > 63:
			fill(ac, 33, ac + 1, 34, ROCK)
	for st in [16, 40, 58, 80, 104]:   # little stalactites in the top tunnel
		set_tile(st, 5, DIRT)
		set_tile(st, 6, DIRT)
	set_tile(30, 40, CRATE)
	set_tile(90, 40, CRATE)
	set_tile(55, 21, CRATE)
	set_tile(65, 21, CRATE)
	for bx in [24, 52, 68, 96]:
		fill(bx, 4, bx + 1, 4, ROCK)
	torches = [Vector2(8, 18), Vector2(22, 18), Vector2(98, 18), Vector2(112, 18), Vector2(42, 15), Vector2(78, 15),
		Vector2(54, 26), Vector2(66, 26), Vector2(18, 36), Vector2(52, 36), Vector2(84, 36), Vector2(104, 36),
		Vector2(28, 7), Vector2(60, 7), Vector2(92, 7)]

func surface_below(c: int, hint: int) -> int:
	for r in range(maxi(1, hint), ROWS - 1):
		if solid_at(c, r) and not solid_at(c, r - 1):
			return r
	return ROWS - 3

func roof_start(c: int) -> int:
	for r in range(1, ROWS - 4):
		if not solid_at(c, r) and not solid_at(c + 1, r) and not solid_at(c, r + 1) and not solid_at(c + 1, r + 1):
			return r
	return 1

# places bots can walk to, and floors that the "breaking ground" event can crumble
func compute_nav() -> void:
	roam_pts = []
	for c in range(3, COLS - 3, 4):
		for r in range(3, ROWS - 2):
			if solid_at(c, r) and not solid_at(c, r - 1) and not solid_at(c, r - 2) and not solid_at(c + 1, r - 1) and not solid_at(c + 1, r - 2):
				roam_pts.append(Vector2(c * T + 6, r * T - 44))
	surf_runs = []
	for r in range(2, ROWS - 3):
		var c0 := -1
		for c in range(1, COLS):
			var v := tiles[r * COLS + c] if c < COLS - 1 else 0
			var ok: bool = (v == DIRT or v == WOOD) and not solid_at(c, r - 1)
			if ok and c0 < 0:
				c0 = c
			elif not ok and c0 >= 0:
				if c - c0 >= 6:
					surf_runs.append([c0, r, c - c0])
				c0 = -1

func solid_at(c: int, r: int) -> bool:
	if c < 0 or c >= COLS or r < 0 or r >= ROWS:
		return true
	return tiles[r * COLS + c] > 0

func solid_pt(px: float, py: float) -> bool:
	return solid_at(floori(px / T), floori(py / T))

func rect_hits(x: float, y: float, w: float, h: float) -> bool:
	var c0 := floori(x / T)
	var c1 := floori((x + w - 0.002) / T)
	var r0 := floori(y / T)
	var r1 := floori((y + h - 0.002) / T)
	for r in range(r0, r1 + 1):
		for c in range(c0, c1 + 1):
			if solid_at(c, r):
				return true
	return false

func damage_tile(c: int, r: int, amt: float) -> void:
	if c < 1 or c >= COLS - 1 or r < 1 or r >= ROWS - 1:
		return
	var i := r * COLS + c
	var v := tiles[i]
	if v == EMPTY or v == ROCK:
		return
	if v == DIRT and amt < 6:
		amt *= 0.15
	thp[i] -= amt
	if net_role == "host":
		tile_dirty[i] = true
	if thp[i] <= 0:
		tiles[i] = EMPTY
		debris((c + 0.5) * T, (r + 0.5) * T, 6, v)
		if v == CRATE or v == WOOD:
			play("crate", Vector2((c + 0.5) * T, (r + 0.5) * T), -6.0 if v == CRATE else -10.0)

func zone_at(px: float, py: float):
	if not cfg.zones:
		return null
	for z in zones:
		if z.rect.has_point(Vector2(px, py)):
			return z
	return null

func los(a: Vector2, b: Vector2) -> bool:
	var d := (b - a).length()
	var n := ceili(d / 12.0)
	for i in range(1, n):
		var k := float(i) / n
		if solid_pt(a.x + (b.x - a.x) * k, a.y + (b.y - a.y) * k):
			return false
	return true

func gsign() -> float:
	return 1.0 if g_dir >= 0 else -1.0

# ---------------- setup ----------------
func center(p) -> Vector2:
	return Vector2(p.x + p.w / 2.0, p.y + p.h / 2.0)

func new_slot(type: String, mag: int, spare: int) -> Dictionary:
	return {"type": type, "mag": mag, "spare": spare, "zi": 0, "dual": false}

func mag_cap(w) -> int:
	return WD[w.type].mag * (2 if w.get("dual", false) else 1)

func buzz(ms: int) -> void:
	if autotest or shot_at >= 0 or not cfg.vibration:
		return
	Input.vibrate_handheld(ms)

func in_body(o, pos: Vector2) -> bool:
	if pos.x > o.x - 1 and pos.x < o.x + o.w + 1 and pos.y > o.y - 3 and pos.y < o.y + o.h:
		return true
	return pos.distance_to(head_pos(o)) < 9.5

func drop_gun(x: float, y: float, type: String, ammo) -> void:
	for off in [0.0, 36.0, -36.0, 72.0, -72.0, 108.0]:
		var free := true
		for k in pickups:
			if Vector2(k.x - (x + off), k.y - y).length() < 30:
				free = false
				break
		if free and not rect_hits(x + off, y, 24, 16):
			pickups.append(make_pickup("drop", x + off, y, type, ammo))
			return
	pickups.append(make_pickup("drop", x, y, type, ammo))

func zoom_level(p: Player) -> int:
	var w = p.slots[p.cur]
	if w == null:
		return 1
	var zs: Array = WD[w.type].zooms
	return zs[clampi(w.zi, 0, zs.size() - 1)]

func set_posture(p: Player, post: String) -> bool:
	if p.posture == post:
		return true
	var sz: Vector2 = POSTURE[post]
	var nx := p.x + p.w / 2.0 - sz.x / 2.0
	var ny := p.y
	if gsign() > 0:
		ny = p.y + p.h - sz.y
	if rect_hits(nx, ny, sz.x, sz.y):
		return false
	p.x = nx
	p.y = ny
	p.w = sz.x
	p.h = sz.y
	p.posture = post
	return true

func head_pos(p: Player) -> Vector2:
	var c := center(p)
	var face := 1.0 if cos(p.aim) >= 0 else -1.0
	match p.posture:
		"crouch":
			return c + Vector2(1.0 * face, -14.0 * gsign())
		"prone":
			return c + Vector2(11.0 * face, 2.0 * gsign())
	return c + Vector2(1.0 * face, -15.0 * gsign())

func full_slot(type: String) -> Dictionary:
	return new_slot(type, WD[type].mag, WD[type].spare)

func fresh_loadout(p: Player) -> void:
	var primary := "uzi"
	if p.style == "sniper" and p.bot:
		primary = "sniper"
	p.slots = [full_slot(primary), full_slot("magnum")]
	p.cur = 0
	p.grenades = S.start_grenades
	p.bombs = 0
	p.smokes = 0
	p.burn_t = 0.0
	p.spin = 0.0
	p.stun_t = 0.0
	p.net_t = 0.0
	p.reload_t = 0.0

func base_spots(i: int) -> Array:
	var bs: Array = bases_v[i]
	var out := []
	for k in [2, 4, 6]:
		out.append(Vector2((bs[0] + k) * T + 6, bs[1] * T - 44))
	return out

func roam_points() -> Array:
	return roam_pts

# a safe place to land: far from enemies, out of their sight, not where you landed last time,
# picked at random among the best few so nobody can camp it
func pick_spawn(p: Player) -> Vector2:
	var cands := []
	for i in bases_v.size():
		cands.append_array(base_spots(i))
	cands.append_array(roam_pts)
	var own_base := Vector2.ZERO
	var other_base := Vector2.ZERO
	if cfg.mode == "team" and bases_v.size() >= 2:
		own_base = base_spots(p.side % 2)[1]
		other_base = base_spots(1 - p.side % 2)[1]
	var scored := []
	for sp in cands:
		if rect_hits(sp.x, sp.y, 20, 42) or sp.y + 42 > water_y - 24:
			continue
		if cfg.mode == "team" and own_base != other_base and sp.distance_to(own_base) > sp.distance_to(other_base):
			continue
		var c: Vector2 = sp + Vector2(10, 21)
		var md := 1400.0
		var seen := false
		for o in players:
			if o != p and o.alive and enemy(o, p):
				var d := center(o).distance_to(c)
				md = minf(md, d)
				if d < 760 and los(center(o), c):
					seen = true
		var score := md - (520.0 if seen else 0.0) + randf() * 260.0
		if p.last_spawn != Vector2.ZERO and c.distance_to(p.last_spawn) < 240:
			score -= 400.0
		scored.append([score, sp])
	if scored.is_empty():
		return base_spots(0)[1]
	scored.sort_custom(func(a, b): return a[0] > b[0])
	var pick: Vector2 = scored[randi() % mini(3, scored.size())][1]
	p.last_spawn = pick + Vector2(10, 21)
	return pick

func spawn(p: Player) -> void:
	if p.spawn_set and not rect_hits(p.spawn_pt.x, p.spawn_pt.y, 20, 42):
		spawn_at(p, p.spawn_pt)
		return
	spawn_at(p, pick_spawn(p))

func old_spawn_unused(p: Player) -> void:
	# pick the base farther from enemies (sometimes the other one, to mix it up)
	var far := []
	for i in bases_v.size():
		var md := 1e9
		var bc: Vector2 = base_spots(i)[1]
		for o in players:
			if o != p and o.alive:
				md = minf(md, Vector2(o.x - bc.x, o.y - bc.y).length())
		far.append(md)
	var pick := 0 if far[0] >= far[1] else 1
	if randf() < 0.25:
		pick = 1 - pick
	if cfg.mode == "team":
		pick = p.side
	var spots := base_spots(pick)
	spots.shuffle()
	var best = spots[0]
	for sp in spots:
		if not rect_hits(sp.x, sp.y, 20, 42):
			best = sp
			break
	spawn_at(p, best)

func spawn_at(p: Player, best: Vector2) -> void:
	p.spawn_set = false
	p.fire_lock = true
	p.born_t = time_s
	p.protect_t = S.protect
	if t > 0.5:
		play("spawn", Vector2(best.x + 10, best.y + 21), -6.0 if is_me(p) else -12.0, 0.05)
	p.posture = "stand"
	p.w = 20.0
	p.h = 42.0
	p.x = best.x
	p.y = best.y
	p.vx = 0.0
	p.vy = 0.0
	p.hp = S.hp_max
	p.fuel = S.fuel_max
	p.alive = true
	p.last_hit_by = null
	p.last_hit_t = -9.0
	p.target = null
	p.streak = 0
	fresh_loadout(p)

func make_pickup(type: String, x: float, y: float, gun: String = "", ammo = null) -> Pickup:
	var k := Pickup.new()
	k.type = type
	k.gun = gun
	k.ammo = ammo
	k.x = x
	k.y = y
	k.ttl = 20.0 if type == "drop" else 1e9
	return k

func make_spawners() -> void:
	spawners.clear()
	for l in item_spots:
		var s := Spawner.new()
		var row: int = surface_below(l[0], l[1])
		s.x = l[0] * T + T / 2.0 - 12
		s.y = row * T - 17
		s.type = l[2]
		s.pool = l[3]
		spawners.append(s)
		fill_spawner(s)

func fill_spawner(s: Spawner) -> void:
	var g := ""
	if s.type == "gun":
		g = s.pool[randi() % s.pool.size()]
	var pk := make_pickup(s.type, s.x, s.y, g)
	pk.spawner = s
	s.item = pk
	pickups.append(pk)

func reset_match() -> void:
	map_id = pick_map()
	gen_map()
	t = 0.0
	g_dir = 1.0
	g_target = 1.0
	water_y = WH
	match_time = cfg.minutes * 60.0
	if lantest_time > 0:
		match_time = lantest_time
	event_every = float(cfg.event_every)
	next_event = event_every
	last_event = ""
	ev = null
	shake = 0.0
	big_msg = ""
	bullets.clear()
	grenades_list.clear()
	parts.clear()
	pickups.clear()
	blocks.clear()
	corpses.clear()
	clouds.clear()
	feed.clear()
	players.clear()
	var humans: Array = [{"peer": 1, "name": my_name(), "look": look_str(my_look()), "side": int(cfg.my_side)}]
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
		p.look = parse_look(humans[i].get("look", AV_DEF)) if human else random_look()
		p.bot = not human
		p.remote = human and int(humans[i].peer) != 1
		p.peer_id = int(humans[i].peer) if human else 0
		p.style = BOT_STYLE[i]
		p.st = make_style(p.style)
		p.side = i
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
			tp.color = TEAM_COL[1] if tp.side == 0 else TEAM_COL[2]
	my_idx = 99 if dedicated else 0
	for i in players.size():
		if i < humans.size():
			players[i].uid = str(humans[i].get("uid", ""))
	for p in players:
		spawn(p)
	make_spawners()
	start_dirt = tiles.count(DIRT)
	cam = Vector2.ZERO
	tile_dirty.clear()
	net_fx = []

# ---------------- particles ----------------
func add_part(x: float, y: float, vx: float, vy: float, life: float, color: Color, size: float, g: float = 0.0, tx: String = "", size1: float = -1.0) -> Part:
	if parts.size() > 420:
		parts.pop_front()
	var q := Part.new()
	q.x = x; q.y = y; q.vx = vx; q.vy = vy; q.life = life; q.max_life = life; q.color = color
	q.size = size; q.size1 = size if size1 < 0 else size1; q.g = g; q.tex = tx
	q.rot = randf() * TAU
	parts.append(q)
	return q

func debris(x: float, y: float, n: int, kind: int = DIRT) -> void:
	if net_role == "host":
		net_fx.append(["d", x, y, n, kind])
	var cols := [Color("#7e5432"), Color("#9c6a3e"), Color("#5c3c22")]
	if kind == WOOD or kind == CRATE:
		cols = [Color("#a8703c"), Color("#8a5a2e"), Color("#c58c50")]
	for i in n:
		var q := add_part(x + randf_range(-8, 8), y + randf_range(-8, 8), randf_range(-160, 160), randf_range(-220, 40) * gsign(), 0.9 + randf() * 0.5, cols[randi() % 3], 3 + randf() * 4, 1.0)
		q.spin = randf_range(-8, 8)
	add_part(x, y, randf_range(-20, 20), -20 * gsign(), 0.9, Color(0.75, 0.66, 0.55, 0.5), 18, -0.05, "smoke", 34)

func sparks(x: float, y: float, color: Color, n: int, spd := 200.0) -> void:
	if net_role == "host":
		net_fx.append(["k", x, y, color, n, spd])
	for i in n:
		add_part(x, y, randf_range(-spd, spd), randf_range(-spd, spd), 0.18 + randf() * 0.15, color, 2.5)

func blood(x: float, y: float, n: int) -> void:
	if net_role == "host":
		net_fx.append(["b", x, y, n])
	for i in n:
		add_part(x, y, randf_range(-140, 140), randf_range(-160, 60) * gsign(), 0.45 + randf() * 0.3, Color(0.75, 0.08, 0.1, 0.9), 3 + randf() * 2, 0.8)

# ---------------- combat ----------------
func hurt(p: Player, amt: float, src, cause: String, gun := "", head := false) -> void:
	if not p.alive or amt <= 0:
		return
	if p.protect_t > 0 and cause != "water":
		return
	if src != null and src != p and not enemy(src, p) and not FF_GUNS.has(gun):
		return
	p.hp -= amt
	if p.hp > 0 and amt >= 7.0 and cause != "water" and cause != "gas" and t - p.grunt_t > 0.8:
		p.grunt_t = t
		play("ow%d" % (randi() % 2), center(p), -4.0 if is_me(p) else -9.0, 0.1)
	p.last_hit_t = t
	if src != null:
		p.last_hit_by = src
		p.last_gun = gun
	p.last_cause = cause
	p.last_head = head
	p.flash = 0.1
	if p.bot:
		p.dodge_t = 0.6
		if src != null and src != p and (p.target == null or randf() < 0.6):
			p.target = src
			p.target_pos = center(src)
			p.target_seen_t = t
	if cause != "water":
		me_fx(p, "hurt")
		if src != null and src != p:
			me_fx(src, "hit")
	if p.hp <= 0:
		die(p)

func die(p: Player) -> void:
	p.alive = false
	p.respawn_t = S.respawn
	p.deaths += 1
	var was_leader: bool = current_leader() == p and p.kills >= 3
	p.lstreak = p.streak
	p.streak = 0
	p.hp = 0
	play("die%d" % (randi() % 3), center(p), 2.0 if is_me(p) else -1.0, 0.06)
	var k = p.last_hit_by
	var c := center(p)
	blood(c.x, c.y, 14)
	var cp := Corpse.new()
	cp.x = c.x; cp.y = c.y; cp.vx = p.vx * 0.5 + randf_range(-60, 60); cp.vy = -160 * gsign(); cp.spin = randf_range(-5, 5)
	cp.team = p.team; cp.face = 1.0 if cos(p.aim) >= 0 else -1.0
	cp.look = plook(p)
	corpses.append(cp)
	if net_role == "host":
		net_fx.append(["c", cp.x, cp.y, cp.vx, cp.vy, cp.spin, cp.team, cp.face, players.find(p)])
	var entry := {"k": "", "kc": C_INK, "v": p.pname, "vc": p.color, "vi": players.find(p), "gun": "", "head": p.last_head and p.last_cause == "shot", "t": 5.0, "note": ""}
	var team_kill: bool = k != null and k != p and cfg.mode == "team" and k.side == p.side
	if team_kill:
		entry.k = k.pname
		entry.kc = k.color
		entry.gun = p.last_gun
		entry.note = "team kill"
		me_fx(k, "big", "TEAM KILL!")
		me_fx(k, "snd", ["suicide", -4.0])
	elif k != null and k != p:
		me_fx(k, "snd", ["kill", -5.0])
		k.kills += 1
		k.streak += 1
		k.best = maxi(k.best, k.streak)
		if entry.head:
			k.hs += 1
		if p.last_cause == "melee":
			k.mk += 1
		elif p.last_cause == "blast":
			k.bk += 1
		entry.k = k.pname
		entry.kc = k.color
		entry.gun = p.last_gun
		me_fx(k, "buzz", 90)
		me_fx(k, "shake", 7.0)
		if was_leader:
			me_fx(k, "big", "LEADER DOWN!")
		elif entry.head:
			me_fx(k, "big", "HEADSHOT!")
		elif k.streak == 2:
			me_fx(k, "big", "DOUBLE KILL")
		elif k.streak >= 3:
			me_fx(k, "big", "%d KILL STREAK" % k.streak)
		if k.bot and randf() < 0.35:
			var lines: Array = STYLES[k.style].chat
			k.say = lines[randi() % lines.size()]
			k.say_t = 2.2
	else:
		entry.note = {"water": "drowned", "crush": "got crushed", "gas": "choked", "fire": "burned"}.get(p.last_cause, "blew up")
		var own: bool = k == p or (k == null and p.last_cause == "blast")
		if own:
			me_fx(p, "snd", ["suicide", -5.0])
	feed.push_front(entry)
	if feed.size() > 5:
		feed.resize(5)
	var w = p.slots[p.cur]
	if w != null and w.type != "magnum" and w.mag + w.spare > 0:
		drop_gun(c.x - 12, c.y - 8, w.type, {"mag": w.mag, "spare": w.spare})
	me_fx(p, "jetoff")
	me_fx(p, "buzz", 300)

func show_big(s: String) -> void:
	big_msg = s
	big_t = 1.6
	play_l("headshot", null, -6.0, 0.0)

func shoulder(p: Player) -> Vector2:
	var c := center(p)
	var face := 1.0 if cos(p.aim) >= 0 else -1.0
	match p.posture:
		"crouch":
			return c + Vector2(1.0 * face, -5.0 * gsign())
		"prone":
			return c + Vector2(2.0 * face, 2.0 * gsign())
	return c + Vector2(1.0 * face, -6.0 * gsign())

func muzzle_pos(p: Player, gun: String) -> Vector2:
	var m: Dictionary = META.GUN[gun]
	var reach: float = 7.0 + (m.muzzle[0] - m.grip[0]) * S.gun_draw
	return shoulder(p) + Vector2(cos(p.aim), sin(p.aim)) * reach

func fire(p: Player, w: Dictionary) -> void:
	var d: Dictionary = WD[w.type]
	if autotest:
		guns_used[w.type] = guns_used.get(w.type, 0) + 1
	var dual: bool = w.get("dual", false)
	var face := 1.0 if cos(p.aim) >= 0 else -1.0
	var mz := muzzle_pos(p, w.type)
	if dual:
		p.dual_side = 1 - p.dual_side
		if p.dual_side == 1:
			mz += Vector2(-3.0 * face, 3.0 * gsign())
	p.protect_t = 0.0
	# spread follows the same fixed pattern for everyone: the first shot goes where you aim
	if t - p.last_fire_t > 0.35:
		p.shot_n = 0
	var off: float = SPREAD_PAT[p.shot_n % SPREAD_PAT.size()]
	p.shot_n += 1
	p.last_fire_t = t
	var rw := rewind_others(p)
	var spread_mul := 1.0 if p.on_ground else 1.35
	if p.posture == "crouch":
		spread_mul = 0.6
	elif p.posture == "prone":
		spread_mul = 0.35
	if dual:
		spread_mul *= 1.3
	var special: String = d.get("special", "")
	if w.type == "sniper":
		hitscan(p, mz, p.aim + off * d.spread * spread_mul, d.dmg, d.chip)
	elif special == "laser":
		laser_beam(p, mz, p.aim + off * d.spread * spread_mul, d.dmg, d.chip)
	elif special == "shock":
		shock_arc(p, mz, p.aim, d.dmg)
	elif special == "flame":
		for i in 2:
			var fa: float = p.aim + (off * 0.6 + (i - 0.5) * 0.4) * d.spread
			var fb := Bullet.new()
			var fsp: float = d.speed * (1.0 if i == 0 else 0.9)
			fb.x = mz.x
			fb.y = mz.y
			fb.vx = cos(fa) * fsp + p.vx * 0.5
			fb.vy = sin(fa) * fsp + p.vy * 0.5
			fb.life = d.life
			fb.ff = p.lat if p.remote else 0.0
			fb.max_life = fb.life
			fb.dmg = d.dmg
			fb.chip = d.chip
			fb.owner = p
			fb.gun = "flame"
			fb.flame = true
			bullets.append(fb)
	else:
		for i in d.pellets:
			var fan: float = (float(i) / (d.pellets - 1) - 0.5 + off * 0.15) if d.pellets > 1 else off
			var a: float = p.aim + fan * d.spread * spread_mul
			var b := Bullet.new()
			var sp: float = d.speed * (1.0 - 0.06 * (i % 3) if d.pellets > 1 else 1.0)
			b.x = mz.x; b.y = mz.y; b.vx = cos(a) * sp; b.vy = sin(a) * sp
			b.life = d.life; b.dmg = d.dmg; b.chip = d.chip; b.owner = p; b.rocket = w.type == "rpg"; b.gun = w.type
			b.net = special == "net"
			b.ff = p.lat if p.remote else 0.0
			bullets.append(b)
	restore_others(rw)
	if d.push > 0 and p.posture == "stand":
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
	if wt == "flame":
		if t - p.snd_t > 0.3 or t < p.snd_t:
			p.snd_t = t
			play_l("flame", mz, -3.0 if is_me(p) else -7.0, 0.05)
	else:
		play_l(d.snd, mz, (-1.0 if wt == "ak47" else (-6.0 if wt == "minigun" else -4.0)) if is_me(p) else -7.0)
	if is_me(p):
		shake = maxf(shake, d.recoil * (0.9 if wt == "ak47" else 0.5))

func hitscan(p: Player, from: Vector2, a: float, dmg: float, chip: float) -> void:
	var dir := Vector2(cos(a), sin(a))
	var pos := from
	var end := from + dir * 1800.0
	for i in 450:
		pos += dir * 4.0
		if pos.x < 0 or pos.x > WW or pos.y < 0 or pos.y > WH:
			end = pos
			break
		if solid_pt(pos.x, pos.y):
			damage_tile(floori(pos.x / T), floori(pos.y / T), chip)
			sparks(pos.x, pos.y, Color("#ffe8a0"), 6)
			add_part(pos.x, pos.y, 0, -15, 0.5, Color(0.8, 0.7, 0.55, 0.5), 6, 0.0, "smoke", 18)
			end = pos
			break
		var victim = null
		for o in players:
			if o != p and o.alive and enemy(p, o) and in_body(o, pos):
				victim = o
				break
		if victim != null:
			var head: bool = pos.distance_to(head_pos(victim)) < 9.5
			if victim.protect_t <= 0:
				victim.vx += dir.x * 90
			blood(pos.x, pos.y, 8)
			play("hit", pos, -6.0)
			hurt(victim, dmg * (S.headshot if head else 1.0), p, "shot", "sniper", head)
			end = pos
			break
	add_tracer({"a": from, "b": end, "t": 0.22, "max": 0.22, "kind": "line"})

func laser_beam(p: Player, from: Vector2, a: float, dmg: float, chip: float) -> void:
	var dir := Vector2(cos(a), sin(a))
	var pos := from
	var seg := from
	var bounces := 0
	for i in 500:
		var prev := pos
		pos += dir * 4.0
		if pos.x < 0 or pos.x > WW or pos.y < 0 or pos.y > WH:
			break
		if solid_pt(pos.x, pos.y):
			damage_tile(floori(pos.x / T), floori(pos.y / T), chip)
			sparks(pos.x, pos.y, Color("#7ff4ff"), 6)
			add_tracer({"a": seg, "b": pos, "t": 0.25, "max": 0.25, "kind": "laser"})
			if bounces >= 1:
				return
			bounces += 1
			if solid_pt(prev.x, pos.y):
				dir.y = -dir.y
			else:
				dir.x = -dir.x
			pos = prev
			seg = pos
			continue
		for o in players:
			if o != p and o.alive and enemy(p, o) and in_body(o, pos):
				var head: bool = pos.distance_to(head_pos(o)) < 9.5
				sparks(pos.x, pos.y, Color("#7ff4ff"), 10)
				play("hit", pos, -8.0)
				hurt(o, dmg * (1.4 if head else 1.0), p, "shot", "laser", head)
				add_tracer({"a": seg, "b": pos, "t": 0.25, "max": 0.25, "kind": "laser"})
				return
	add_tracer({"a": seg, "b": pos, "t": 0.25, "max": 0.25, "kind": "laser"})

func shock_arc(p: Player, from: Vector2, a: float, dmg: float) -> void:
	var best = null
	var bd := 240.0
	for o in players:
		if o != p and o.alive and enemy(p, o):
			var oc := center(o)
			var v := oc - from
			var d := v.length()
			if d < bd and absf(wrapf(v.angle() - a, -PI, PI)) < 0.5 and los(from, oc):
				bd = d
				best = o
	var end := from + Vector2(cos(a), sin(a)) * 200.0
	if best != null:
		end = center(best)
		if best.protect_t <= 0:
			best.stun_t = 0.9
		hurt(best, dmg, p, "shock", "shock")
		sparks(end.x, end.y, Color("#9ff6ff"), 10)
	else:
		var pos := from
		for i in 50:
			pos += Vector2(cos(a), sin(a)) * 4.0
			if solid_pt(pos.x, pos.y):
				break
		end = pos
		sparks(end.x, end.y, Color("#9ff6ff"), 4)
	add_tracer({"a": from, "b": end, "t": 0.2, "max": 0.2, "kind": "zig"})

func explode(x: float, y: float, r: float, dmg: float, owner, gun: String) -> void:
	var es := "bomb_boom" if gun == "bomb" else "explosion"
	explode_fx(x, y, r, es)
	if net_role == "host":
		net_fx.append(["x", x, y, r, es])
	explosions += 1
	explode_hits(x, y, r, dmg, owner, gun)

func explode_fx(x: float, y: float, r: float, es := "explosion") -> void:
	shake = maxf(shake, 14.0)
	play_l(es, Vector2(x, y), 0.0)
	add_part(x, y, 0, 0, 0.45, Color.WHITE, r * 0.6, 0.0, "fireball", r * 2.2)
	for i in 10:
		var a := randf() * TAU
		add_part(x, y, cos(a) * randf_range(20, 90), sin(a) * randf_range(20, 90) - 30, 1.2 + randf() * 0.6, Color(0.35, 0.33, 0.32, 0.55), 20, -0.04, "smoke", 46)
	for i in 18:
		var a := randf() * TAU
		var s := randf() * 360
		add_part(x, y, cos(a) * s, sin(a) * s, 0.35 + randf() * 0.25, Color("#ffcf5e"), 3, 0.3)

func explode_hits(x: float, y: float, r: float, dmg: float, owner, gun: String) -> void:
	var tr := r * 0.62
	var c0 := floori(x / T)
	var r0 := floori(y / T)
	var n := ceili(tr / T)
	for rr in range(r0 - n, r0 + n + 1):
		for cc in range(c0 - n, c0 + n + 1):
			var dx := (cc + 0.5) * T - x
			var dy := (rr + 0.5) * T - y
			var dd := sqrt(dx * dx + dy * dy)
			if dd < tr:
				damage_tile(cc, rr, 99.0 if dd < tr * 0.55 else 6.0)
	for p in players:
		if not p.alive:
			continue
		var c := center(p)
		var dv := c - Vector2(x, y)
		var d: float = maxf(dv.length(), 1.0)
		var big := r * 1.4
		if d < big:
			var f := 1.0 - d / big
			if p.protect_t <= 0:
				p.vx += dv.x / d * 560 * f
				p.vy += dv.y / d * 560 * f
			hurt(p, dmg * f, owner, "blast", gun)
	for k in pickups:
		if Vector2(k.x - x, k.y - y).length() < r:
			k.vy -= 300 * gsign()

func has_ammo(s) -> bool:
	return s != null and s.mag + s.spare > 0

func start_reload(p: Player) -> void:
	var w = p.slots[p.cur]
	if w == null or p.reload_t > 0:
		return
	var d: Dictionary = WD[w.type]
	if w.mag < mag_cap(w) and w.spare > 0:
		p.reload_t = d.reload * (1.3 if w.get("dual", false) else 1.0)
		p.reload_total = p.reload_t
		me_fx(p, "snd", ["reload", -6.0])

func finish_reload(p: Player) -> void:
	var w = p.slots[p.cur]
	if w == null:
		return
	var take: int = mini(mag_cap(w) - w.mag, w.spare)
	w.mag += take
	w.spare -= take

func give_gun(p: Player, type: String, ammo) -> bool:
	var d: Dictionary = WD[type]
	for s in p.slots:
		if s != null and s.type == type:
			if s.spare >= d.spare * 2:
				return false
			var add: int = (ammo.mag + ammo.spare) if ammo != null else (d.mag + d.spare)
			s.spare = mini(d.spare * 2, s.spare + add)
			return true
	if is_heavy(type) and heavy_slot(p) >= 0:
		return false
	for i in 2:
		if not has_ammo(p.slots[i]):
			p.slots[i] = new_slot(type, ammo.mag, ammo.spare) if ammo != null else full_slot(type)
			if not has_ammo(p.slots[p.cur]):
				p.cur = i
			return true
	return false

func replace_current(p: Player, pk: Pickup) -> void:
	# a heavy gun always replaces the heavy gun you carry (only one heavy at a time)
	var hs := heavy_slot(p)
	if is_heavy(pk.gun) and hs >= 0:
		p.cur = hs
	var old = p.slots[p.cur]
	var c := center(p)
	if has_ammo(old):
		drop_gun(c.x - 12, c.y - 8, old.type, {"mag": old.mag, "spare": old.spare})
		play("wdrop", c, -6.0)
	p.slots[p.cur] = new_slot(pk.gun, pk.ammo.mag, pk.ammo.spare) if pk.ammo != null else full_slot(pk.gun)
	p.reload_t = 0.0
	p.switch_t = 0.22

func overlaps(a, b) -> bool:
	return a.x < b.x + b.w and a.x + a.w > b.x and a.y < b.y + b.h and a.y + a.h > b.y

func remove_pickup(pk: Pickup) -> void:
	pickups.erase(pk)
	if pk.spawner != null:
		pk.spawner.item = null
		pk.spawner.timer = S.pickup_respawn

func try_pickup(p: Player, pk: Pickup) -> bool:
	if pk.type == "health":
		if p.hp < S.hp_max:
			p.hp = minf(S.hp_max, p.hp + 50)
			return true
		return false
	if pk.type == "bomb":
		if p.bombs < S.max_bombs:
			p.bombs += 1
			return true
		return false
	if pk.type == "smoke":
		if p.smokes < S.max_smokes:
			p.smokes += 1
			return true
		return false
	if pk.type == "grenade":
		if p.grenades < S.max_grenades:
			p.grenades = mini(S.max_grenades, p.grenades + 2)
			return true
		return false
	if give_gun(p, pk.gun, pk.ammo):
		return true
	if p.bot:
		var likes: Array = STYLES[p.style].likes
		var c = p.slots[p.cur]
		if likes.has(pk.gun) and (c == null or not likes.has(c.type)):
			replace_current(p, pk)
			return true
	return false

# ---------------- physics ----------------
func move_entity(e, dt: float) -> void:
	e.on_ground = false
	e.hit_wall = false
	var nx: float = e.x + e.vx * dt
	if rect_hits(nx, e.y, e.w, e.h):
		if e.vx > 0:
			nx = floori((nx + e.w) / T) * T - e.w - 0.001
		else:
			nx = (floori(nx / T) + 1) * T + 0.001
		if rect_hits(nx, e.y, e.w, e.h):
			nx = e.x
		e.vx = 0.0
		e.hit_wall = true
	e.x = nx
	var ny: float = e.y + e.vy * dt
	if rect_hits(e.x, ny, e.w, e.h):
		if e.vy > 0:
			ny = floori((ny + e.h) / T) * T - e.h - 0.001
		else:
			ny = (floori(ny / T) + 1) * T + 0.001
		if rect_hits(e.x, ny, e.w, e.h):
			ny = e.y
		if e.vy * gsign() >= 0:
			e.on_ground = true
		e.vy = 0.0
	e.y = ny

func unstick(e) -> void:
	if not rect_hits(e.x, e.y, e.w, e.h):
		return
	for k in range(1, 12):
		var ny: float = e.y - gsign() * k * 8
		if not rect_hits(e.x, ny, e.w, e.h):
			e.y = ny
			return

func update_player(p: Player, dt: float) -> void:
	var inp: Dictionary = p.inp
	var pv: Dictionary = p.prev
	p.say_t -= dt
	if not p.alive:
		p.respawn_t -= dt
		if p.respawn_t <= 0.9 and not p.spawn_set:
			# choose the landing spot now so the camera can glide there before you appear
			p.spawn_pt = pick_spawn(p)
			p.spawn_set = true
			p.x = p.spawn_pt.x
			p.y = p.spawn_pt.y
			p.vx = 0.0
			p.vy = 0.0
		if p.respawn_t <= 0:
			spawn(p)
		p.prev = inp.duplicate()
		return
	unstick(p)
	var c := center(p)
	var z = zone_at(c.x, c.y)
	var gm: float = z.g if z != null else 1.0
	var fm: float = z.f if z != null else 1.0
	var was_water := p.in_water
	p.in_water = c.y > water_y
	if p.in_water and not was_water and t > 0.5:
		play("splash", c, -4.0)
	# sit / crawl
	if inp.down and not pv.get("down", false) and p.on_ground:
		var w0 = p.slots[p.cur]
		if p.posture == "stand":
			set_posture(p, "crouch")
		elif p.posture == "crouch" and w0 != null and w0.type == "sniper":
			set_posture(p, "prone")
		else:
			set_posture(p, "stand")
	if inp.fly and p.posture != "stand":
		if not set_posture(p, "stand"):
			inp.fly = false
	if p.on_ground:
		p.air_t = 0.0
	else:
		p.air_t += dt
		if p.air_t > 0.5 and p.posture != "stand":
			set_posture(p, "stand")
	if p.posture == "prone":
		var wp = p.slots[p.cur]
		if wp == null or wp.type != "sniper":
			set_posture(p, "crouch")
	if p.in_water and p.posture != "stand":
		set_posture(p, "stand")
	c = center(p)
	var post_mul: float = S.crouch_speed if p.posture == "crouch" else (S.crawl_speed if p.posture == "prone" else 1.0)
	p.stun_t -= dt
	p.net_t -= dt
	if p.net_t > 0 or p.stun_t > 0:
		inp.fly = false
		post_mul *= 0.35 if p.net_t > 0 else 0.15
		if p.stun_t > 0 and randf() < 0.4:
			sparks(c.x + randf_range(-10, 10), c.y + randf_range(-18, 14), Color("#9ff6ff"), 1, 80)
	var cw0 = p.slots[p.cur]
	if cw0 != null and cw0.type == "minigun":
		post_mul *= 0.72
	var target: float = inp.mx * S.move_speed * (0.55 if p.in_water else 1.0) * post_mul
	var acc := 2600.0 if p.on_ground else 1500.0
	if target != 0.0 and signf(target) != signf(p.vx):
		acc *= 1.5
	if p.vx < target:
		p.vx = minf(target, p.vx + acc * dt)
	elif p.vx > target:
		p.vx = maxf(target, p.vx - acc * dt)
	var was_jet := p.jet_on
	p.jet_on = false
	if inp.fly:
		if p.in_water:
			p.vy -= g_dir * 1300 * dt
		elif p.fuel > 0:
			if p.on_ground:
				p.vy = -gsign() * S.jump_speed
				if not was_jet:
					p.jst_t = t
					play("jump", c, -5.0 if is_me(p) else -12.0, 0.05)
			p.vy -= g_dir * S.thrust * gm * dt
			p.fuel = maxf(0.0, p.fuel - S.fuel_drain * fm * dt)
			p.jet_on = true
	if p.jet_on and randf() < 0.55:
		var face := 1.0 if cos(p.aim) >= 0 else -1.0
		var nz := c + Vector2(-9 * face, 10 * gsign())
		add_part(nz.x + randf_range(-3, 3), nz.y, randf_range(-20, 20), gsign() * randf_range(90, 160), 0.5, Color(0.85, 0.85, 0.88, 0.45), 6, -0.02, "smoke", 18)
	if p.jet_on and not was_jet and (t - p.jst_t > 0.6 or t < p.jst_t):
		p.jst_t = t
		play("jetstart", c, -8.0 if is_me(p) else -14.0, 0.05)
	if is_me(p):
		if p.jet_on and not was_jet and not autotest and shot_at < 0:
			jet_player.play()
		elif not p.jet_on and was_jet:
			jet_player.stop()
	if not p.jet_on and not p.in_water:
		p.fuel = minf(S.fuel_max, p.fuel + (S.refill_ground if p.on_ground else S.refill_air) * dt)
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
	p.was_ground = p.on_ground
	var fall_speed := p.vy * gsign()
	move_entity(p, dt)
	if p.on_ground and not p.was_ground and fall_speed > 300:
		var fy := p.y + (p.h if gsign() > 0 else 0.0)
		add_part(c.x, fy, -40, -10 * gsign(), 0.5, Color(0.8, 0.72, 0.6, 0.45), 10, 0.0, "smoke", 26)
		add_part(c.x, fy, 40, -10 * gsign(), 0.5, Color(0.8, 0.72, 0.6, 0.45), 10, 0.0, "smoke", 26)
		me_fx(p, "snd", ["land", -10.0])
	if p.on_ground:
		p.walk += absf(p.vx) * dt * (0.05 if p.posture == "stand" else 0.09)
	# weapons
	p.protect_t -= dt
	p.fire_cd -= dt
	p.melee_cd -= dt
	p.g_cd -= dt
	p.flash -= dt
	p.melee_anim -= dt
	p.switch_t -= dt
	p.muzzle_t -= dt
	p.recoil = maxf(0.0, p.recoil - dt * 40)
	if p.bot or p.remote:
		p.aim = inp.aim
	else:
		var diff := wrapf(inp.aim - p.aim, -PI, PI)
		var stepmax: float = aim_rate(mouse_aiming()) * dt
		p.aim = wrapf(p.aim + clampf(diff, -stepmax, stepmax), -PI, PI)
	if p.posture == "prone":
		var face0 := 1.0 if cos(p.aim) >= 0 else -1.0
		var gs0 := gsign()
		var la0 := clampf(atan2(sin(p.aim) * gs0, cos(p.aim) * face0), -0.45, 0.3)
		p.aim = atan2(sin(la0) * gs0, cos(la0) * face0)
	animate(p, dt)
	var w = p.slots[p.cur]
	if p.reload_t > 0:
		p.reload_t -= dt
		if p.reload_t <= 0:
			finish_reload(p)
	if not p.bot:
		near_gun(p)
	var mini: bool = w != null and w.type == "minigun"
	if mini and inp.shoot and p.reload_t <= 0 and p.stun_t <= 0 and w.mag > 0:
		if p.spin <= 0.01:
			play("spin", c, -5.0 if is_me(p) else -9.0)
		p.spin = minf(1.0, p.spin + dt / 0.45)
	else:
		p.spin = maxf(0.0, p.spin - dt / 0.6)
	if not inp.shoot:
		p.fire_lock = false
	if inp.shoot and not pv.get("shoot", false):
		p.shoot_buf = 0.22
	p.shoot_buf -= dt
	var want_fire: bool = (inp.shoot or p.shoot_buf > 0.0) and not p.fire_lock
	if want_fire and w != null and p.reload_t <= 0 and p.fire_cd <= 0 and p.stun_t <= 0 and (not mini or p.spin >= 1.0 or w.mag == 0):
		if w.mag > 0:
			fire(p, w)
			p.shoot_buf = 0.0
			w.mag -= 1
			p.fire_cd = WD[w.type].rate * (0.55 if w.get("dual", false) else 1.0)
			if w.mag == 0:
				start_reload(p)
		elif w.spare > 0:
			start_reload(p)
		else:
			var o = p.slots[1 - p.cur]
			if has_ammo(o):
				p.cur = 1 - p.cur
				p.reload_t = 0.0
			else:
				p.fire_cd = 0.4
				me_fx(p, "snd", ["empty", -6.0])
	if inp.reload and not pv.get("reload", false):
		start_reload(p)
	if inp.pick != "" and pv.get("pick", "") == "":
		var found = floor_gun(p) if p.bot else near_gun(p)
		if found != null:
			var opts := pickup_opts(p, found)
			var opt: String = inp.pick
			if opt == "first":
				opt = opts[0] if opts.size() > 0 else ""
			if opts.has(opt):
				apply_pick(p, found, opt)
				if opt != "dual":
					me_fx(p, "snd", ["wpick", -5.0])
	if inp.swap and not pv.get("swap", false) and p.slots[1 - p.cur] != null:
		p.cur = 1 - p.cur
		p.reload_t = 0.0
		p.switch_t = 0.22
		me_fx(p, "snd", ["swap", -6.0])
	if inp.zoom and not pv.get("zoom", false) and w != null:
		var zs: Array = WD[w.type].zooms
		if zs.size() > 1:
			w.zi = (w.zi + 1) % zs.size()
			me_fx(p, "snd", ["swap", -10.0, 0.0])
	var none_left: bool = (inp.grenade and not pv.get("grenade", false) and p.grenades <= 0) or (inp.bomb and not pv.get("bomb", false) and p.bombs <= 0) or (inp.get("smoke", false) and not pv.get("smoke", false) and p.smokes <= 0)
	if none_left:
		me_fx(p, "snd", ["locked", -6.0])
	if inp.grenade and not pv.get("grenade", false) and p.grenades > 0 and p.g_cd <= 0:
		p.grenades -= 1
		p.g_cd = 0.7
		var g := Grenade.new()
		var sp := shoulder(p)
		g.x = sp.x; g.y = sp.y
		g.vx = cos(p.aim) * 560 + p.vx * 0.4
		g.vy = sin(p.aim) * 560 + p.vy * 0.3
		g.fuse = S.grenade_fuse
		g.owner = p
		grenades_list.append(g)
		play("throw", c, -8.0)
	if inp.bomb and not pv.get("bomb", false) and p.bombs > 0 and p.g_cd <= 0:
		p.bombs -= 1
		p.g_cd = 0.7
		var gb := Grenade.new()
		var spb := shoulder(p)
		gb.x = spb.x; gb.y = spb.y
		gb.vx = cos(p.aim) * 330 + p.vx * 0.3
		gb.vy = sin(p.aim) * 330 + p.vy * 0.2
		gb.fuse = 4.5
		gb.kind = "bomb"
		gb.owner = p
		grenades_list.append(gb)
		play("throw", c, -8.0)
	if inp.get("smoke", false) and not pv.get("smoke", false) and p.smokes > 0 and p.g_cd <= 0:
		p.smokes -= 1
		p.g_cd = 0.7
		var gsm := Grenade.new()
		var spm := shoulder(p)
		gsm.x = spm.x
		gsm.y = spm.y
		gsm.vx = cos(p.aim) * 480 + p.vx * 0.4
		gsm.vy = sin(p.aim) * 480 + p.vy * 0.3
		gsm.fuse = 1.3
		gsm.kind = "smoke"
		gsm.owner = p
		grenades_list.append(gsm)
		play("throw", c, -8.0)
	if p.burn_t > 0:
		p.burn_t -= dt
		if p.in_water:
			p.burn_t = 0.0
		hurt(p, 5.0 * dt, p.burn_by, "fire", "flame")
		if t - p.sizzle_t > 0.7 or t < p.sizzle_t:
			p.sizzle_t = t
			me_fx(p, "snd", ["sizzle", -6.0])
	if inp.melee and not pv.get("melee", false) and p.melee_cd <= 0:
		p.melee_cd = 0.55
		p.melee_anim = 0.28
		play("slash", c, -6.0)
		var dir := 1.0 if cos(p.aim) >= 0 else -1.0
		var rwk := rewind_others(p)
		for o in players:
			if o == p or not o.alive or not enemy(p, o):
				continue
			var oc := center(o)
			if absf(oc.y - c.y) < 40 and (oc.x - c.x) * dir > -6 and (oc.x - c.x) * dir < 54:
				if o.protect_t <= 0:
					o.vx += dir * 360
					o.vy -= gsign() * 140
				hurt(o, 35, p, "melee", "melee")
				blood(oc.x, oc.y, 6)
				play("hit", oc, -4.0)
		restore_others(rwk)
		damage_tile(floori((c.x + dir * 30) / T), floori(c.y / T), 2.0)
	# water and healing
	if p.in_water:
		var src = p.last_hit_by if (p.last_hit_by != null and t - p.last_hit_t < 3) else null
		hurt(p, S.water_dps * dt, src, "water", p.last_gun)
	elif t - p.last_hit_t > S.regen_delay and p.hp < S.hp_max:
		p.hp = minf(S.hp_max, p.hp + S.regen_rate * dt)
	if p.alive:
		for k in pickups.duplicate():
			var human_choice: bool = not p.bot and (k.type == "gun" or k.type == "drop") and not pickup_opts(p, k).is_empty()
			if overlaps(p, k) and not human_choice and try_pickup(p, k):
				remove_pickup(k)
				me_fx(p, "snd", ["health" if k.type == "health" else ("wpick" if (k.type == "gun" or k.type == "drop") else "pickup"), -6.0])
	p.prev = inp.duplicate()

func near_gun(p: Player):
	var c := center(p)
	var best = null
	var bd := 48.0
	for k in pickups:
		if k.type == "gun" or k.type == "drop":
			var d := Vector2(k.x + k.w / 2.0 - c.x, (k.y + k.h / 2.0 - c.y) * 0.7).length()
			if d < bd:
				bd = d
				best = k
	if best != null:
		p.near_k = best
		p.near_t = t
		return best
	if p.near_k != null and pickups.has(p.near_k) and t - p.near_t < 1.6 and Vector2(p.near_k.x - c.x, p.near_k.y - c.y).length() < 150:
		return p.near_k
	return null

func floor_gun(p: Player):
	for k in pickups:
		if (k.type == "gun" or k.type == "drop") and overlaps(p, k):
			return k
	return null

const HEAVY := ["ak47", "shotgun", "sniper", "minigun", "rpg", "flame", "laser"]

func is_heavy(g: String) -> bool:
	return HEAVY.has(g)

# slot index holding a heavy gun with ammo, or -1
func heavy_slot(p: Player) -> int:
	for i in 2:
		var s2 = p.slots[i]
		if s2 != null and has_ammo(s2) and is_heavy(s2.type):
			return i
	return -1

func is_small(g: String) -> bool:
	return g == "magnum" or g == "uzi"

# what a human can choose for the gun on the floor; empty = take it automatically
func pickup_opts(p: Player, k: Pickup) -> Array:
	var cur = p.slots[p.cur]
	if cur != null and cur.type == k.gun:
		if is_small(k.gun) and not cur.get("dual", false):
			return ["dual"]
		return []
	for s2 in p.slots:
		if s2 != null and s2.type == k.gun:
			return []
	if is_heavy(k.gun) and heavy_slot(p) >= 0:
		return ["swap"]
	for s2 in p.slots:
		if s2 == null or not has_ammo(s2):
			return []
	return ["swap", "dual"] if is_small(k.gun) else ["swap"]

func can_auto_take(p: Player, k: Pickup) -> bool:
	return pickup_opts(p, k).is_empty()

func apply_pick(p: Player, k: Pickup, opt: String) -> void:
	if opt == "swap":
		replace_current(p, k)
	elif opt == "dual":
		var cur = p.slots[p.cur]
		if cur == null or cur.type != k.gun:
			replace_current(p, k)
			cur = p.slots[p.cur]
		cur.dual = true
		me_fx(p, "snd", ["equip2", -4.0])
		cur.mag = mag_cap(cur)
		cur.spare += (k.ammo.mag + k.ammo.spare) if k.ammo != null else WD[k.gun].spare
	remove_pickup(k)

func ease_k(rate: float, dt: float) -> float:
	return 1.0 - exp(-rate * dt)

func animate(p: Player, dt: float) -> void:
	p.draw_aim = lerp_angle(p.draw_aim, p.aim, ease_k(22.0, dt))
	var tb := 0.0
	var tf := 0.0
	var sb := 0.0
	var sf := 0.0
	match p.posture:
		"crouch":
			# front knee up, back knee on the ground
			tf = -1.25
			sf = 0.05
			tb = 0.35
			sb = 1.45
		"prone":
			tb = sin(p.walk) * 0.25 * clampf(absf(p.vx) / 25.0, 0, 1)
			tf = -tb
			sb = tb
			sf = tf
		_:
			if p.on_ground:
				var k := clampf(absf(p.vx) / 80.0, 0, 1)
				var ph := p.walk
				tb = -sin(ph) * 0.5 * k
				tf = sin(ph) * 0.5 * k
				sb = tb + maxf(0.0, cos(ph)) * 0.75 * k
				sf = tf + maxf(0.0, -cos(ph)) * 0.75 * k
			else:
				tb = 0.25 + sin(time_s * 2.5 + p.id) * 0.05
				sb = 0.75
				tf = -0.35 + sin(time_s * 2.5 + p.id + 1.0) * 0.05
				sf = 0.1
	var lk := ease_k(12.0, dt)
	p.leg_b = lerpf(p.leg_b, tb, lk)
	p.leg_f = lerpf(p.leg_f, tf, lk)
	p.shin_b = lerpf(p.shin_b, sb, lk)
	p.shin_f = lerpf(p.shin_f, sf, lk)
	p.reload_k = lerpf(p.reload_k, 1.0 if p.reload_t > 0 else 0.0, ease_k(9.0, dt))

# ---------------- bots ----------------
func nearest_pickup(p: Player, types: Array, max_d := 1e9):
	var best = null
	var bd := max_d
	var c := center(p)
	for k in pickups:
		if types.has(k.type):
			var d := Vector2(k.x - c.x, k.y - c.y).length()
			if d < bd:
				bd = d
				best = k
	return best

func bot_think(b: Player, dt: float) -> void:
	var inp: Dictionary = b.inp
	inp.shoot = false
	inp.grenade = false
	inp.bomb = false
	inp.smoke = false
	inp.melee = false
	inp.swap = false
	inp.reload = false
	if not b.alive:
		inp.mx = 0.0
		inp.fly = false
		return
	var st: Dictionary = b.st
	var c := center(b)
	var eye := c + Vector2(0, -12 * gsign())
	b.dodge_t -= dt
	b.think_t -= dt
	if b.think_t <= 0:
		b.think_t = 0.25 + randf() * 0.2
		if randf() < 0.1:
			b.crouch_roll = randf()
		# who can I see or hear?
		var best = null
		var bd := 1e9
		var view: float = 1050.0 if b.style == "sniper" else 820.0
		for o in players:
			if o == b or not o.alive or not enemy(b, o):
				continue
			var oc := center(o)
			var d := (oc - c).length()
			var seen: bool = d < view and los(eye, oc)
			var heard: bool = d < 600 and t - o.shot_t < 1.0
			if seen or heard:
				var score := d * (0.7 if seen else 1.2)
				if o == b.last_hit_by and t - b.last_hit_t < 3:
					score *= 0.5
				if score < bd:
					bd = score
					best = o
		if best != null:
			b.target = best
			b.target_pos = center(best)
			b.target_seen_t = t
		elif b.target != null and (not b.target.alive or t - b.target_seen_t > 4.0):
			b.target = null
		if b.target == null and b.roam_t < 4.0:
			# nobody in sight: go hunting toward the nearest enemy, like a real player would
			var hunt = null
			var hd := 1e9
			for o in players:
				if o.alive and enemy(b, o):
					var dd := (center(o) - c).length()
					if dd < hd:
						hd = dd
						hunt = o
			if hunt != null and randf() < (0.9 if cfg.mode == "team" else 0.6):
				b.roam = center(hunt) + Vector2(randf_range(-120, 120), 0)
				b.roam_t = 3.0 + randf() * 2.0
		b.goal = null
		if b.hp < st.retreat:
			b.goal = nearest_pickup(b, ["health"], 1400)
		var has_big := false
		for s in b.slots:
			if s != null and s.type != "magnum" and has_ammo(s):
				has_big = true
		if b.goal == null and (not has_big or b.target == null):
			var k = null
			if has_big:
				var bestk = null
				var bdk := 800.0
				for pk in pickups:
					if (pk.type == "gun" or pk.type == "drop") and st.likes.has(pk.gun):
						var dk := Vector2(pk.x - c.x, pk.y - c.y).length()
						if dk < bdk:
							bdk = dk
							bestk = pk
				var cur = b.slots[b.cur]
				if bestk != null and (cur == null or not st.likes.has(cur.type)):
					k = bestk
			else:
				k = nearest_pickup(b, ["gun", "drop"], 900)
			b.goal = k
		if b.goal == null and b.grenades < 2 and b.target == null:
			b.goal = nearest_pickup(b, ["grenade", "bomb"], 700)
	# roam when nothing to do
	b.roam_t -= dt
	if b.roam_t <= 0 or c.distance_to(b.roam) < 40:
		var pts := roam_points()
		b.roam = pts[randi() % pts.size()] + Vector2(10, 20)
		b.roam_t = 5.0 + randf() * 4.0
	b.strafe_t -= dt
	if b.strafe_t <= 0:
		b.strafe_t = 0.7 + randf() * 1.2
		b.strafe = -1.0 if randf() < 0.5 else 1.0
	var tg = b.target if (b.target != null and b.target.alive) else null
	var visible := false
	if tg != null:
		visible = los(eye, center(tg))
		if visible:
			b.target_pos = center(tg)
			b.target_seen_t = t
	var gpos := b.roam
	var fighting := false
	if b.goal != null and pickups.has(b.goal):
		gpos = Vector2(b.goal.x + 12, b.goal.y + 8)
	elif tg != null:
		gpos = b.target_pos
		fighting = true
	var dx := gpos.x - c.x
	var keep: float = st.dist
	var w = b.slots[b.cur]
	var reloading: bool = b.reload_t > 0 or (w != null and w.mag == 0)
	if fighting:
		var dist := absf(dx)
		if (b.hp < st.retreat or reloading) and visible:
			inp.mx = -signf(dx)
		elif dist < keep * 0.6:
			inp.mx = -signf(dx) if dx != 0 else b.strafe
		elif dist > keep * 1.4 or not visible:
			inp.mx = signf(dx)
		else:
			inp.mx = b.strafe * 0.6
	else:
		inp.mx = (signf(dx) * (1.0 if absf(dx) > 60 else 0.5)) if absf(dx) > 12 else 0.0
	var rel := (gpos.y - c.y) * gsign()
	var fly := rel < -60 and (not fighting or not visible or rel < -140)
	var front: float = c.x + inp.mx * 22
	if inp.mx != 0 and (solid_pt(front, c.y) or solid_pt(front, c.y + gsign() * 14)):
		fly = true
	if b.in_water or (water_y < WH and c.y > water_y - 120):
		fly = true
	if ev != null and ev.phase == "warn" and ev.name == "water":
		fly = fly or (c.y > (water_row - 2) * T and randf() < 0.6)
	if b.dodge_t > 0 and b.fuel > 30 and randf() < 0.5:
		fly = true
	if b.fuel < 10:
		b.saving = true
	if b.fuel > 60:
		b.saving = false
	if b.saving and not b.in_water and not (inp.mx != 0 and solid_pt(front, c.y)):
		fly = false
	# a platform right above: walk to its nearest edge before flying up
	if fly and not b.in_water and solid_pt(c.x, c.y - gsign() * 40.0):
		if b.detour_t <= 0:
			var row := floori((c.y - gsign() * 40.0) / T)
			var col := floori(c.x / T)
			var dl := 99
			var dr := 99
			for k in range(1, 16):
				if dl == 99 and not solid_at(col - k, row) and not solid_at(col - k, row - int(gsign())):
					dl = k
				if dr == 99 and not solid_at(col + k, row) and not solid_at(col + k, row - int(gsign())):
					dr = k
			b.detour = -1.0 if dl < dr else 1.0
			b.detour_t = 1.0
	if b.detour_t > 0:
		b.detour_t -= dt
		inp.mx = b.detour
		if solid_pt(c.x, c.y - gsign() * 40.0):
			fly = false
	# not getting any closer to where we want to go? pick something else
	b.prog_t -= dt
	if b.prog_t <= 0:
		var gd := (gpos - c).length()
		if gd > b.prog_d - 40.0 and not (fighting and visible):
			b.roam_t = 0.0
			b.goal = null
			b.strafe *= -1
		b.prog_d = gd
		b.prog_t = 2.5
	if Vector2(b.x - b.lx, b.y - b.ly).length() < 0.6:
		b.stuck_t += dt
	else:
		b.stuck_t = 0.0
	b.lx = b.x
	b.ly = b.y
	if b.stuck_t > 1.3:
		b.strafe *= -1
		b.stuck_t = 0.0
		b.roam_t = 0.0
		inp.mx = b.strafe
		fly = true
	# sit or lie down to shoot steadier
	var want_post := "stand"
	if tg != null and visible and b.on_ground and not fly and not b.in_water:
		var tv: Vector2 = b.target_pos - c
		var dd := tv.length()
		if w != null and w.type == "sniper" and b.style == "sniper" and dd > 300 and absf(tv.y) < dd * 0.3:
			want_post = "prone"
		elif (b.style == "cautious" or b.style == "balanced" or b.style == "sniper") and dd > 260 and b.crouch_roll < 0.4:
			want_post = "crouch"
	if want_post != "stand":
		b.stuck_t = 0.0
		inp.mx = 0.0 if want_post == "prone" else inp.mx * 0.5
	if b.posture != want_post:
		if want_post == "prone" and b.posture == "stand":
			set_posture(b, "crouch")
		set_posture(b, want_post)
	inp.fly = fly
	# aiming: turn toward the target like a thumb would, with wobble
	if tg != null:
		var tc: Vector2 = b.target_pos
		var lead := Vector2(tg.vx, tg.vy) * 0.08 if visible else Vector2.ZERO
		b.aim_want = atan2(tc.y + lead.y - c.y, tc.x + lead.x - c.x)
	elif absf(dx) > 12:
		b.aim_want = 0.0 if dx > 0 else PI
	var err_mul := 1.6 if not b.on_ground else 1.0
	b.aim_err = clampf(b.aim_err + randf_range(-0.05, 0.05), -st.err * err_mul, st.err * err_mul)
	var diff := wrapf(b.aim_want - b.aim, -PI, PI)
	var step: float = st.turn * dt
	var new_aim := wrapf(b.aim + clampf(diff, -step, step), -PI, PI)
	var on_target := absf(diff) < 0.25
	inp.aim = new_aim
	if tg != null:
		var d := (b.target_pos - c).length()
		b.see_t = b.see_t + dt if visible else 0.0
		b.burst_t -= dt
		b.pause_t -= dt
		var reach := 1000.0 if (w != null and w.type == "sniper") else 760.0
		if w != null and w.type == "shock":
			reach = 220.0
		elif w != null and w.type == "net":
			reach = 520.0
		if visible and b.see_t > st.react and on_target and d < reach and (tg == null or tg.protect_t <= 0.2):
			if b.pause_t <= 0:
				inp.shoot = true
				if b.burst_t <= -0.5:
					b.burst_t = randf_range(0.4, 1.0)
			if b.burst_t <= 0 and b.burst_t > -0.5 and b.pause_t <= 0:
				b.pause_t = randf_range(0.15, 0.45)
		inp.aim = new_aim + b.aim_err * 0.5
		if d < 48 and visible:
			inp.melee = true
		if b.bombs > 0 and d < 260 and randf() < dt * 0.4:
			inp.bomb = true
		if b.smokes > 0 and d < 320 and randf() < dt * 0.35:
			inp.smoke = true
		if b.grenades > 0 and d < 420 and d > 120 and randf() < dt * st.nade * (1.2 if not visible else 0.35):
			inp.grenade = true
			inp.aim = atan2(b.target_pos.y - c.y - 140 * gsign(), b.target_pos.x - c.x)
	if w != null and not inp.shoot and w.mag < WD[w.type].mag * 0.35 and w.spare > 0:
		inp.reload = true
	if w != null and not has_ammo(w) and has_ammo(b.slots[1 - b.cur]):
		inp.swap = randf() < 0.5
	elif w != null and w.type == "magnum" and has_ammo(b.slots[1 - b.cur]) and randf() < 0.05:
		inp.swap = true

# ---------------- events ----------------
func enabled_events() -> Array:
	var out := []
	for n in EVENTS.keys():
		if cfg.get("ev_" + n, true):
			out.append(n)
	return out

func pick_event() -> String:
	var all := enabled_events()
	var names := []
	for n in all:
		if n != last_event:
			names.append(n)
	if names.is_empty():
		names = all
	return names[randi() % names.size()]

func start_warn() -> void:
	ev = Ev.new()
	ev.name = pick_event()
	ev.phase = "warn"
	ev.t = S.event_warn
	play({"water": "ev_water", "roof": "ev_rocks", "brk": "ev_brk", "flip": "ev_flip"}.get(ev.name, "warn"), null, -4.0, 0.0)
	if ev.name == "roof":
		var cols := {}
		for tries in 200:
			if cols.size() >= 7:
				break
			var cc := 3 + randi() % (COLS - 8)
			if roof_start(cc) < ROWS - 8:
				cols[cc] = true
		ev.cols = cols.keys()
	elif ev.name == "brk":
		var list := []
		for tries in 40:
			if list.size() >= 6:
				break
			if surf_runs.is_empty():
				break
			var isl: Array = surf_runs[randi() % surf_runs.size()]
			var s: int = isl[0] + randi() % maxi(1, isl[2] - 5)
			list = []
			for xx in range(s, s + 6):
				for yy in range(isl[1], isl[1] + 2):
					var v := tiles[yy * COLS + xx]
					if v == DIRT or v == WOOD:
						list.append(Vector2i(xx, yy))
		if list.size() < 6:
			list = []
			for xx in range(54, 67):
				if tiles[38 * COLS + xx] == WOOD:
					list.append(Vector2i(xx, 38))
		list.shuffle()
		ev.tiles = list

func start_active() -> void:
	ev.phase = "active"
	match ev.name:
		"water":
			ev.t = 49.0
		"roof":
			ev.t = 9.0
			ev.spawned = 0
		"brk":
			ev.t = 4.5
			ev.spawned = 0
		"flip":
			ev.t = S.flip_time
			g_target = -1.0
	ev.dur = ev.t

func end_event() -> void:
	if ev.name == "flip":
		g_target = 1.0
		feed.push_front({"k": "", "kc": C_INK, "v": "Gravity is going back to normal", "vc": C_ARC, "gun": "", "head": false, "t": 3.0, "t0": 3.0, "note": ""})
	if ev.name == "water":
		water_y = WH
	last_event = ev.name
	ev = null
	next_event += event_every

func update_events(dt: float) -> void:
	var ease_rate: float = 2.0 / S.flip_ease
	g_dir = move_toward(g_dir, g_target, ease_rate * dt)
	if ev == null and t >= next_event - S.event_warn and t < match_time - S.event_warn and not enabled_events().is_empty():
		start_warn()
	if ev == null:
		return
	ev.t -= dt
	if ev.phase == "warn":
		if ev.t <= 0:
			start_active()
		return
	var el := ev.dur - ev.t
	if ev.name == "water":
		var bottom := 43.0 * T
		var tgt := float(water_row) * T
		var k := 0.0
		if el < 25:
			k = el / 25.0
		elif el < 37:
			k = 1.0
		else:
			k = maxf(0.0, (49.0 - el) / 12.0)
		k = k * k * (3 - 2 * k)
		water_y = bottom - (bottom - tgt) * k
	elif ev.name == "roof":
		while ev.spawned < ev.cols.size() and el > ev.spawned * 1.2:
			var b := Block.new()
			b.c = ev.cols[ev.spawned]
			b.y = roof_start(b.c) * T
			blocks.append(b)
			ev.spawned += 1
	elif ev.name == "brk":
		var per: float = 4.0 / maxf(1.0, ev.tiles.size())
		while ev.spawned < ev.tiles.size() and el > ev.spawned * per:
			var v: Vector2i = ev.tiles[ev.spawned]
			var kind := tiles[v.y * COLS + v.x]
			if kind != EMPTY and kind != ROCK:
				set_tile(v.x, v.y, EMPTY)
				debris((v.x + 0.5) * T, (v.y + 0.5) * T, 8, kind)
				if ev.spawned % 2 == 0:
					play("crumble", Vector2((v.x + 0.5) * T, v.y * T), -6.0)
				shake = maxf(shake, 3.0)
			ev.spawned += 1
	if ev.t <= 0:
		end_event()

func update_blocks(dt: float) -> void:
	for i in range(blocks.size() - 1, -1, -1):
		var b: Block = blocks[i]
		b.vy = minf(520.0, b.vy + 900 * dt)
		var ny := b.y + b.vy * dt
		var box := {"x": b.c * T, "y": ny, "w": 2 * T, "h": 2 * T}
		for p in players:
			if p.alive and not b.hit.has(p) and overlaps(p, box):
				b.hit[p] = true
				hurt(p, 45, null, "crush")
				p.vy += 400
		var row_below := floori((ny + 2 * T) / T)
		if solid_at(b.c, row_below) or solid_at(b.c + 1, row_below) or row_below >= ROWS - 2:
			var r0 := row_below - 2
			for yy in range(r0, r0 + 2):
				for xx in range(b.c, b.c + 2):
					if not solid_at(xx, yy):
						set_tile(xx, yy, DIRT)
			debris(b.c * T + T, row_below * T, 12)
			shake = maxf(shake, 7.0)
			play("crumble", Vector2(b.c * T + T, row_below * T), 0.0)
			for p in players:
				if p.alive:
					unstick(p)
			blocks.remove_at(i)
		else:
			b.y = ny

# ---------------- projectiles and items ----------------
func update_bullets(dt: float) -> void:
	for i in range(bullets.size() - 1, -1, -1):
		var b: Bullet = bullets[i]
		b.life -= dt
		var dead := b.life <= 0
		if b.flame:
			b.vx *= pow(0.2, dt)
			b.vy = b.vy * pow(0.2, dt) - 70.0 * gsign() * dt
		elif not b.rocket and not b.net:
			for hp2 in players:
				if hp2.alive and not hp2.bot and hp2 != b.owner and enemy(b.owner, hp2) and t - hp2.whiz_t > 0.35:
					var hd := Vector2(b.x, b.y).distance_to(head_pos(hp2))
					if hd < 46 and hd > 14:
						hp2.whiz_t = t
						me_fx(hp2, "snd", ["whiz", -7.0])
		var bdt := dt + b.ff
		b.ff = 0.0
		var steps := maxi(3, ceili(Vector2(b.vx, b.vy).length() * bdt / 14.0))
		for s in steps:
			if dead:
				break
			b.x += b.vx * bdt / steps
			b.y += b.vy * bdt / steps
			if b.rocket and randf() < 0.5:
				add_part(b.x, b.y, randf_range(-20, 20), randf_range(-20, 20), 0.7, Color(0.8, 0.8, 0.8, 0.5), 6, -0.03, "smoke", 18)
			if solid_pt(b.x, b.y):
				dead = true
				if b.rocket:
					explode(b.x - b.vx * 0.01, b.y - b.vy * 0.01, S.rocket_radius, S.rocket_dmg, b.owner, "rpg")
				elif b.flame:
					damage_tile(floori(b.x / T), floori(b.y / T), b.chip)
				else:
					damage_tile(floori(b.x / T), floori(b.y / T), b.chip)
					sparks(b.x, b.y, Color("#ffe8a0"), 3)
					add_part(b.x, b.y, 0, -15, 0.35, Color(0.8, 0.7, 0.55, 0.4), 4, 0.0, "smoke", 12)
				break
			for p in players:
				if p == b.owner or not p.alive or not (enemy(b.owner, p) or FF_GUNS.has(b.gun)):
					continue
				if in_body(p, Vector2(b.x, b.y)):
					dead = true
					if b.flame:
						hurt(p, b.dmg, b.owner, "fire", "flame")
						if p.protect_t <= 0:
							p.burn_t = 2.5
							p.burn_by = b.owner
					elif b.rocket:
						explode(b.x, b.y, S.rocket_radius, S.rocket_dmg, b.owner, "rpg")
					elif b.net:
						if p.protect_t <= 0:
							p.net_t = 3.5
							p.vx *= 0.3
							p.vy *= 0.3
						play("net", Vector2(b.x, b.y), -4.0)
						hurt(p, b.dmg, b.owner, "shot", "net")
					else:
						var head: bool = Vector2(b.x, b.y).distance_to(head_pos(p)) < 9.5
						var dmg: float = b.dmg * (S.headshot if head else 1.0)
						if p.protect_t <= 0:
							p.vx += signf(b.vx) * 25
							blood(b.x, b.y, 4)
						else:
							sparks(b.x, b.y, Color("#9ff6ff"), 3)
						play("hit", Vector2(b.x, b.y), -10.0)
						hurt(p, dmg, b.owner, "shot", b.gun, head)
					break
		if b.x < 0 or b.x > WW or b.y < 0 or b.y > WH:
			dead = true
		if dead:
			bullets.remove_at(i)

func update_grenades(dt: float) -> void:
	for i in range(grenades_list.size() - 1, -1, -1):
		var g: Grenade = grenades_list[i]
		if g.kind == "bomb":
			g.beep_t -= dt
			if g.beep_t <= 0:
				g.beep_t = 0.15 + g.fuse * 0.18
				play("beep", Vector2(g.x, g.y), -4.0, 0.0)
			if g.stuck:
				if g.beep_t > 0.9:
					g.beep_t = 0.3
				g.fuse -= dt
				if g.fuse <= 0:
					explode(g.x, g.y, 120.0, 115.0, g.owner, "bomb")
					grenades_list.remove_at(i)
				continue
		var z = zone_at(g.x, g.y)
		g.vy += S.gravity * (z.g if z != null else 1.0) * g_dir * dt
		g.rot += g.vx * dt * 0.05
		if g.y > water_y:
			g.vx *= pow(0.3, dt)
			g.vy *= pow(0.3, dt)
		var nx := g.x + g.vx * dt
		if solid_pt(nx, g.y):
			if absf(g.vx) > 120 and g.kind != "bomb":
				play("tink", Vector2(g.x, g.y), -8.0)
			g.vx *= -0.4
			if g.kind == "bomb":
				if not g.stuck:
					play("arm", Vector2(g.x, g.y), -2.0, 0.0)
				g.stuck = true
		else:
			g.x = nx
		var ny := g.y + g.vy * dt
		if solid_pt(g.x, ny):
			if absf(g.vy) > 140 and g.kind != "bomb":
				play("tink", Vector2(g.x, g.y), -8.0)
			g.vy *= -0.35
			g.vx *= 0.7
			if g.kind == "bomb":
				if not g.stuck:
					play("arm", Vector2(g.x, g.y), -2.0, 0.0)
				g.stuck = true
		else:
			g.y = ny
		g.fuse -= dt
		if g.fuse <= 0:
			if g.kind == "smoke":
				clouds.append({"x": g.x, "y": g.y, "t": 7.0, "owner": g.owner})
				play("hiss", Vector2(g.x, g.y), -1.0)
				grenades_list.remove_at(i)
				continue
			if g.kind == "bomb":
				explode(g.x, g.y, 120.0, 115.0, g.owner, "bomb")
			else:
				explode(g.x, g.y, S.grenade_radius, S.grenade_dmg, g.owner, "grenade")
			grenades_list.remove_at(i)

func cloud_fx(cl: Dictionary, dt: float) -> void:
	var k: float = clampf(cl.t / 1.5, 0.0, 1.0)
	if randf() < dt * 16.0 * k:
		add_part(cl.x + randf_range(-80, 80), cl.y + randf_range(-55, 40), randf_range(-12, 12), randf_range(-14, 4), 2.4, Color(0.62, 0.74, 0.55, 0.55), 40, -0.004, "smoke", 96)

func update_clouds(dt: float) -> void:
	for i in range(clouds.size() - 1, -1, -1):
		var cl: Dictionary = clouds[i]
		cl.t -= dt
		if cl.t <= 0:
			clouds.remove_at(i)
			continue
		cloud_fx(cl, dt)
		for p in players:
			if not p.alive or p == cl.owner:
				continue
			if center(p).distance_to(Vector2(cl.x, cl.y)) < 105:
				hurt(p, 7.0 * dt, cl.owner, "gas", "smoke")
				if t - p.cough_t > 1.3 or t < p.cough_t:
					p.cough_t = t
					me_fx(p, "snd", ["cough", -3.0])
					if not p.bot:
						pass
				p.vx *= pow(0.6, dt)

func update_pickups(dt: float) -> void:
	for i in range(pickups.size() - 1, -1, -1):
		var k: Pickup = pickups[i]
		k.ttl -= dt
		if k.ttl <= 0:
			pickups.remove_at(i)
			continue
		if rect_hits(k.x, k.y, k.w, k.h):
			k.y -= gsign() * T
		k.vy += S.gravity * g_dir * dt * (0.2 if k.y > water_y else 1.0)
		k.vy = clampf(k.vy, -600, 600)
		k.vx *= pow(0.05, dt)
		move_entity(k, dt)
		if k.y > WH or k.y < 0:
			pickups.remove_at(i)
	for s in spawners:
		if s.item == null:
			s.timer -= dt
			if s.timer <= 0:
				fill_spawner(s)
				play("item_respawn", Vector2(s.x, s.y), -10.0)

func update_parts(dt: float) -> void:
	for i in range(parts.size() - 1, -1, -1):
		var q: Part = parts[i]
		q.life -= dt
		if q.life <= 0:
			parts.remove_at(i)
			continue
		q.vy += S.gravity * q.g * g_dir * dt
		q.x += q.vx * dt
		q.y += q.vy * dt
		q.vx *= pow(0.4, dt)
		q.rot += q.spin * dt
	for i in range(corpses.size() - 1, -1, -1):
		var cp: Corpse = corpses[i]
		cp.t += dt
		if cp.t > 3.0:
			corpses.remove_at(i)
			continue
		cp.vy += S.gravity * g_dir * dt
		var nx := cp.x + cp.vx * dt
		if not solid_pt(nx, cp.y):
			cp.x = nx
		else:
			cp.vx = 0
		var ny := cp.y + cp.vy * dt
		if solid_pt(cp.x, ny + 10 * gsign()):
			cp.vy = 0
			cp.vx *= pow(0.02, dt)
			cp.rot = move_toward(cp.rot, -PI / 2 * cp.face, dt * 6)
		else:
			cp.y = ny
			cp.rot += cp.spin * dt

# ---------------- input ----------------
func btn_r() -> float:
	return clampf(sh * 0.065, 22 * u, 34 * u) * float(cfg.btn_size)

func stick_rad() -> float:
	return 50.0 * u * float(cfg.stick_size)

func mirror_x(x: float) -> float:
	return sw - x if cfg.left_handed else x

func def_move() -> Vector2:
	return Vector2(mirror_x(100 * u * float(cfg.stick_size) + safe_l + 10 * u), sh - 96 * u)

func def_aim() -> Vector2:
	return Vector2(mirror_x(sw - 200 * u - safe_r), sh - 96 * u)

func buttons() -> Array:
	var names := ["GRENADE", "SWAP", "MELEE", "RELOAD"]
	var ys := [0.30, 0.45, 0.60, 0.75]
	var r := btn_r()
	var bx := mirror_x(sw - safe_r - r - 14 * u)
	var inward := -1.0 if not cfg.left_handed else 1.0
	var out := []
	for i in 4:
		out.append({"n": names[i], "p": Vector2(bx, sh * ys[i]), "r": r})
	if state == "play" and not players.is_empty() and players[my_idx].alive:
		var me: Player = players[my_idx]
		var w = me.slots[me.cur]
		if w != null and WD[w.type].zooms.size() > 1:
			out.append({"n": "ZOOM", "p": Vector2(bx + inward * r * 2.5, sh * 0.30), "r": r * 0.85})
		if me.bombs > 0:
			out.append({"n": "BOMB", "p": Vector2(bx + inward * r * 2.5, sh * 0.47), "r": r * 0.85})
		if me.smokes > 0:
			out.append({"n": "SMOKE", "p": Vector2(bx + inward * r * 2.5, sh * 0.64), "r": r * 0.85})
	if cfg.fire_mode == "button":
		var ap := def_aim()
		out.append({"n": "FIRE", "p": Vector2(ap.x, ap.y - stick_rad() - r * 1.9), "r": r * 1.35})
	out.append({"n": "SIT", "p": Vector2(mirror_x(safe_l + r + 14 * u), sh * 0.42), "r": r * 0.85})
	return out

func _notification(what: int) -> void:
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
			mm_mode = ""
			state = "online" if online else "lan"
			online = false
			recon_left = 0
		"lan_cfg":
			do_action("lobby_back")
		"locker":
			state = lk_back
		"namekey":
			state = "locker" if key_target == "name" else "online"
		"online":
			state = "lan"
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
		if state == "namekey":
			var ch2 := char(event.unicode) if event.unicode > 0 else ""
			if event.keycode == KEY_BACKSPACE:
				name_key("DEL")
				return
			if event.keycode == KEY_ENTER or event.keycode == KEY_KP_ENTER:
				do_action("name_ok")
				return
			if ch2 != "" and event.keycode != KEY_ESCAPE:
				name_key(ch2, true)
				return
		if event.keycode == KEY_ESCAPE or (event.keycode == KEY_P and (state == "play" or state == "paused")):
			go_back(false)
			return
	if event is InputEventScreenTouch:
		touch_mode = true
		if event.pressed:
			press(event.index, event.position)
		else:
			release(event.index)
	elif event is InputEventScreenDrag:
		if stick_l != null and stick_l.id == event.index:
			stick_l.pos = event.position
		if stick_r != null and stick_r.id == event.index:
			stick_r.pos = event.position
	elif event is InputEventMouseButton and (event.button_index == MOUSE_BUTTON_WHEEL_UP or event.button_index == MOUSE_BUTTON_WHEEL_DOWN):
		if event.pressed:
			zoom_request = true
	elif event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT:
		mouse_down = event.pressed
		mouse_used = true
		touch_mode = false
		mouse_pos = event.position
		if event.pressed and state != "play":
			menu_tap(event.position)
			mouse_down = false
		elif event.pressed and pause_rect.has_point(event.position):
			state = "paused"
			mouse_down = false
			jet_player.stop()
		elif event.pressed and timer_rect.has_point(event.position):
			peek_t = 0.0 if peek_t > 0 else 3.0
			mouse_down = false
		elif event.pressed:
			for bb in bubbles:
				if event.position.distance_to(bb.pos) < bb.r + 8 * u:
					pick_request = bb.opt
					mouse_down = false
	elif event is InputEventMouseMotion:
		mouse_pos = event.position
		mouse_used = true

func press(id: int, pos: Vector2) -> void:
	if state != "play":
		menu_tap(pos)
		return
	if pause_rect.has_point(pos):
		state = "paused"
		jet_player.stop()
		return
	if timer_rect.has_point(pos):
		peek_t = 0.0 if peek_t > 0 else 3.0
		return
	for bb in bubbles:
		if pos.distance_to(bb.pos) < bb.r + 10 * u:
			pick_request = bb.opt
			return
	for b in buttons():
		if pos.distance_to(b.p) < b.r + 12 * u:
			btn_held[b.n] = id
			return
	var fixed: bool = cfg.sticks == "fixed"
	if (pos.x < sw * 0.5) != bool(cfg.left_handed):
		stick_l = {"id": id, "o": def_move() if fixed else pos, "pos": pos}
	else:
		stick_r = {"id": id, "o": def_aim() if fixed else pos, "pos": pos}

func release(id: int) -> void:
	if stick_l != null and stick_l.id == id:
		stick_l = null
	if stick_r != null and stick_r.id == id:
		stick_r = null
	for n in btn_held.keys():
		if btn_held[n] == id:
			btn_held.erase(n)

func menu_tap(pos: Vector2) -> void:
	if pending_action != "":
		return
	for b in ui_btns:
		if b.r.has_point(pos):
			pressed_r = b.r
			pressed_at = time_s
			play_l("ui_ok" if BIG_ACTIONS.has(b.a) else "ui_click", null, -6.0 if BIG_ACTIONS.has(b.a) else -8.0, 0.0)
			var a: String = b.a
			if a.begins_with("row:") or a.begins_with("key:") or a.begins_with("lk_") or a.begins_with("nk:") or a.begins_with("team"):
				do_action(a)
				return
			pending_action = a
			pending_big = BIG_ACTIONS.has(a)
			pending_t = 0.22 if pending_big else 0.1
			return

func do_action(a: String) -> void:
	stick_l = null
	stick_r = null
	btn_held.clear()
	match a:
		"play", "restart":
			reset_match()
			state = "play"
		"again":
			if net_role == "client" and online:
				if is_owner():
					rpc_id(1, "c_start", my_settings())
			elif net_role == "host":
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
			lk_back = "lan"
			lk_page = 0
			state = "locker"
		"locker":
			lk_back = "menu"
			lk_page = 0
			state = "locker"
		"lk_done":
			state = lk_back
		"lk_name":
			key_target = "name"
			name_entry = my_name()
			state = "namekey"
		"lk_dice":
			var pool := FUN_NAMES.duplicate()
			pool.erase(name_entry if state == "namekey" else my_name())
			var nn: String = pool[randi() % pool.size()]
			if state == "namekey":
				name_entry = nn
			else:
				cfg.name = nn
				save_cfg()
		"lk_rand":
			cfg.look = look_str(random_look())
			save_cfg()
		"name_ok":
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
			state = "locker" if key_target == "name" else "online"
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
			if net_role == "client" and online and is_owner():
				rpc_id(1, "c_cfg", my_settings())
		"to_lobby":
			state = "lobby"
			send_lobby(true)
		"leave", "cancel":
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
		"o_share":
			var msg := "Join my Sky Squad room! Code: %s  (Play with friends > Online rooms > Join room)" % room_code
			OS.shell_open("https://wa.me/?text=" + msg.uri_encode())
		"o_start":
			if net_role == "client" and is_owner():
				rpc_id(1, "c_start", my_settings())
		"match":
			state = "match_cfg"
		"controls":
			state = "ctrl_cfg"
		"back", "menu":
			if net_role != "":
				net_close()
			state = "menu"
			jet_player.stop()
		"resume":
			state = "play"
		_:
			if a.begins_with("conn:"):
				join_game(a.substr(5))
			elif a.begins_with("team:"):
				pick_team(int(a.substr(5)))
			elif a == "team_shuffle":
				pick_team(-2)
			elif a.begins_with("lk_tab:"):
				lk_tab = a.substr(7)
				lk_page = 0
			elif a.begins_with("lk_page:"):
				lk_page += int(a.substr(8))
			elif a.begins_with("lk_pick:"):
				var bits := a.substr(8).split(":")
				if bits[0] == "sets":
					cfg.look = bits[1]
				else:
					var lk := my_look()
					lk[bits[0]] = bits[1]
					cfg.look = look_str(lk)
				save_cfg()
			elif a.begins_with("nk:"):
				name_key(a.substr(3))
			elif a.begins_with("key:"):
				var kk := a.substr(4)
				if kk == "DEL":
					ip_entry = ip_entry.substr(0, maxi(0, ip_entry.length() - 1))
				elif ip_entry.length() < 15:
					ip_entry += kk
			if a.begins_with("row:"):
				var key_name := a.substr(4)
				for row in MATCH_ROWS + CONTROL_ROWS + LAN_ROWS:
					if row[0] == key_name:
						var vals: Array = row[2]
						var idx := vals.find(cfg[key_name])
						cfg[key_name] = vals[(idx + 1) % vals.size()]
						break
				save_cfg()

func key(k: Key) -> bool:
	return Input.is_physical_key_pressed(k)

func mouse_aiming() -> bool:
	return mouse_used and not touch_mode

func human_input() -> void:
	var me: Player = players[my_idx]
	var inp: Dictionary = me.inp
	if state != "play":
		for k2 in ["fly", "shoot", "swap", "grenade", "melee", "reload", "down", "zoom", "bomb"]:
			inp[k2] = false
		inp.mx = 0.0
		inp.pick = ""
		return
	var mx := (1.0 if (key(KEY_D) or key(KEY_RIGHT)) else 0.0) - (1.0 if (key(KEY_A) or key(KEY_LEFT)) else 0.0)
	var fly := key(KEY_W) or key(KEY_SPACE) or key(KEY_UP)
	var shoot := mouse_down and not touch_mode
	var rad := stick_rad()
	if stick_l != null:
		var d: Vector2 = stick_l.pos - stick_l.o
		var ax := absf(d.x)
		mx = signf(d.x) * clampf((ax - 5 * u) / (rad * 0.45), 0, 1) if ax > 5 * u else 0.0
		if d.y < -rad * 0.42:
			fly = true
		if d.y > rad * 0.6 and absf(d.x) < rad * 0.5:
			inp.down = true
	var c := center(me)
	if stick_r != null:
		var d: Vector2 = stick_r.pos - stick_r.o
		if d.length() > 10 * u:
			last_touch_aim = atan2(d.y, d.x)
		if d.length() > rad * 0.7 and cfg.fire_mode == "auto":
			# wait until the gun has turned to where the stick points, so the shot goes where you meant
			var cw = me.slots[me.cur]
			var lag := absf(wrapf(last_touch_aim - me.aim, -PI, PI))
			shoot = lag < (0.05 if cw != null and cw.type == "sniper" else 0.3)
		inp.aim = last_touch_aim
	elif mouse_aiming():
		var wpos := cam + mouse_pos / zoom
		inp.aim = atan2(wpos.y - c.y, wpos.x - c.x)
	else:
		inp.aim = last_touch_aim
	if btn_held.has("FIRE"):
		shoot = true
	inp.mx = mx
	inp.fly = fly
	inp.shoot = shoot
	inp.bomb = key(KEY_B) or btn_held.has("BOMB")
	inp.smoke = key(KEY_C) or btn_held.has("SMOKE")
	inp.swap = key(KEY_Q) or btn_held.has("SWAP")
	inp.grenade = key(KEY_G) or btn_held.has("GRENADE")
	inp.melee = key(KEY_F) or btn_held.has("MELEE")
	inp.reload = key(KEY_R) or btn_held.has("RELOAD")
	var stick_down: bool = stick_l != null and (stick_l.pos - stick_l.o).y > rad * 0.6 and absf((stick_l.pos - stick_l.o).x) < rad * 0.5
	inp.down = key(KEY_S) or key(KEY_DOWN) or btn_held.has("SIT") or stick_down
	var pk := pick_request
	if pk == "" and key(KEY_E):
		pk = "first"
	if pk == "" and key(KEY_V):
		pk = "dual"
	inp.pick = pk
	inp.zoom = key(KEY_Z) or btn_held.has("ZOOM") or zoom_request

func shot_pose() -> void:
	var me: Player = players[my_idx]
	for a in OS.get_cmdline_user_args():
		if a.begins_with("--gun="):
			me.slots[me.cur] = full_slot(a.substr(6))
		if a.begins_with("--pose="):
			var pose := a.substr(7)
			if pose != "stand":
				set_posture(me, "crouch")
			if pose == "prone":
				set_posture(me, "prone")
		if a.begins_with("--zoom="):
			me.slots[me.cur].zi = int(a.substr(7))
			view_h = S.view_h * ZOOM_MULT[zoom_level(me)]
		if a == "--bubble":
			pickups.append(make_pickup("gun", me.x, me.y + me.h - 16, "rpg"))
		if a.begins_with("--bubble="):
			pickups.append(make_pickup("gun", me.x, me.y + me.h - 16, a.substr(9)))
		if a == "--dual":
			me.slots[me.cur] = full_slot("uzi")
			me.slots[me.cur].dual = true
		if a == "--snipe":
			me.slots[me.cur] = full_slot("sniper")
			hitscan(me, muzzle_pos(me, "sniper"), 0.15, 1.0, 0.0)
		if a == "--knife":
			me.melee_anim = 0.14
		if a == "--net":
			me.net_t = 2.0
		if a == "--stun":
			me.stun_t = 0.8
		if a == "--laser":
			me.slots[me.cur] = full_slot("laser")
			laser_beam(me, muzzle_pos(me, "laser"), -0.35, 1.0, 0.0)
		if a == "--zap":
			me.slots[me.cur] = full_slot("shock")
			shock_arc(me, muzzle_pos(me, "shock"), 0.1, 1.0)
		if a == "--bombs":
			var gb := Grenade.new()
			gb.x = me.x + 60; gb.y = me.y + me.h - 8; gb.kind = "bomb"; gb.stuck = true; gb.fuse = 3.2; gb.owner = me
			grenades_list.append(gb)
		if a == "--crowd":
			for i in range(1, players.size()):
				var o: Player = players[i]
				o.x = me.x + (i - 3) * 70 + (40 if i >= 3 else 0)
				o.y = me.y - 30 - (i % 2) * 40
				o.vx = 0
				o.vy = 0
				o.alive = true
				o.jet_on = true
				o.aim = PI if o.x > me.x else 0.0
				o.draw_aim = o.aim
		if a == "--pausescreen":
			state = "paused"
		if a == "--overscreen":
			for pp in players:
				pp.hs = randi() % 3
				pp.best = randi() % 4
			state = "over"
		if a == "--peek":
			peek_t = 2.0
		if a == "--flames":
			me.slots[me.cur] = full_slot("flame")
			me.aim = 0.15
			for i in 8:
				fire(me, me.slots[me.cur])
				update_bullets(0.03)
		if a == "--cloud":
			clouds.append({"x": me.x + 170, "y": me.y, "t": 6.0, "owner": me})
			for i in 120:
				update_parts(0.03)
				cloud_fx(clouds[0], 0.03)
		if a == "--burn":
			players[1].burn_t = 2.0
			players[1].x = me.x + 120
			players[1].y = me.y
		if a == "--spin":
			me.slots[me.cur] = full_slot("minigun")
			me.spin = 1.0
			me.muzzle_t = 0.07
		if a == "--dead":
			me.protect_t = 0
			me.last_hit_by = players[1]
			hurt(me, 500, players[1], "shot", "ak47")
		if a == "--landing":
			me.protect_t = 0
			hurt(me, 500, players[1], "shot", "ak47")
			me.respawn_t = 0.45
			update_player(me, 0.01)
			cam = Vector2(me.x - sw / zoom / 2, me.y - sh / zoom / 2)
		if a == "--dropin":
			me.born_t = time_s - 0.18
			me.protect_t = 1.6
	me.aim = 0.15
	me.draw_aim = 0.15
	me.vx = 0
	me.protect_t = 0
	for i in 60:
		animate(me, 1.0 / 30.0)

# ---------------- loop ----------------
func _process(delta: float) -> void:
	var _p0 := Time.get_ticks_usec()
	_process_inner(delta)
	if prof_on:
		prof_proc.append(Time.get_ticks_usec() - _p0)
		prof_frame.append(delta * 1e6)
		if prof_proc.size() >= 300:
			var a := prof_proc.duplicate(); a.sort()
			var b := prof_draw.duplicate(); b.sort()
			var f := prof_frame.duplicate(); f.sort()
			print("PROF process med=%dus p99=%dus | draw med=%dus p99=%dus | frame med=%dus p99=%dus max=%dus | parts=%d bullets=%d" % [a[a.size()/2], a[int(a.size()*0.99)], b[b.size()/2] if b.size() > 0 else 0, b[int(b.size()*0.99)] if b.size() > 0 else 0, f[f.size()/2], f[int(f.size()*0.99)], f[-1], parts.size(), bullets.size()])
			prof_proc.clear(); prof_draw.clear(); prof_frame.clear()

func _process_inner(delta: float) -> void:
	var dt: float = minf(delta, 0.033)
	time_s += delta
	var vs := get_viewport_rect().size
	sw = vs.x
	sh = vs.y
	u = clampf(minf(sw, sh) / 400.0, 1.0, 4.0)
	last_delta = delta
	var want_view: float = S.view_h
	if state == "play" and my_idx < players.size() and players[my_idx].alive:
		want_view = S.view_h * ZOOM_MULT[zoom_level(players[my_idx])]
	view_h = lerpf(view_h, want_view, ease_k(4.0, delta))
	zoom = minf(sh / view_h, sw / (view_h * 1.6))
	if OS.has_feature("mobile"):
		var safe := DisplayServer.get_display_safe_area()
		var scr := DisplayServer.screen_get_size()
		safe_l = maxf(0.0, float(safe.position.x))
		safe_r = maxf(0.0, float(scr.x - safe.end.x))
	anim_tick(delta)
	if dedicated:
		dedicated_tick(delta, dt)
		return
	if shot_at >= 0:
		while state == "play" and t < shot_at:
			update_game(1.0 / 30.0)
		shot_frames += 1
		if shot_frames == 1:
			shot_pose()
		queue_redraw()
		if shot_frames == 4:
			get_viewport().get_texture().get_image().save_png("res://shots/%s.png" % shot_name)
			get_tree().quit()
		return
	net_poll(delta)
	toast_t -= delta
	if state == "connecting" and mm_mode == "":
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
				rtt_s = sp.get_statistic(3) / 1000.0 + lag_ms / 1000.0
	lantest_tick(delta)
	if drop_test and state == "play" and net_role == "client" and t > 12.0 and not drop_done:
		drop_done = true
		print("CLIENT drop test: cutting the connection")
		multiplayer.multiplayer_peer.close()
		start_reconnect()
	shots_tick()
	if net_role != "" and (state == "play" or state == "paused"):
		if net_role == "client":
			update_client(dt)
		else:
			update_game(dt)
	elif state == "play":
		if autotest:
			for i in 40:
				if state == "play":
					update_game(1.0 / 30.0)
					if ev != null:
						seen_events[ev.name] = true
					for pp in players:
						if pp.alive:
							post_count[pp.posture] += 1
		else:
			update_game(dt)
	elif autotest:
		for p in players:
			print("%s (%s) side=%d kills=%d deaths=%d" % [p.pname, p.style, p.side, p.kills, p.deaths])
		print("guns used: ", guns_used, " team scores: ", team_scores())
		print("events seen: ", seen_events.keys(), " dirt left: ", tiles.count(DIRT), " of ", start_dirt, " explosions: ", explosions, " postures: ", post_count, " pickups: ", pickups.size())
		get_tree().quit()
	queue_redraw()

var gunloop_i := -1
func update_game(dt: float) -> void:
	t += dt
	if autotest and OS.get_cmdline_user_args().has("--trace") and fmod(t, 15.0) < dt:
		var line := "t=%d " % int(t)
		for pp in players:
			line += "%s:%d,%d %s tg=%s | " % [pp.pname, int(pp.x / T), int(pp.y / T), "A" if pp.alive else "D", pp.target.pname if pp.target != null else "-"]
		print(line)
	if autotest and OS.get_cmdline_user_args().has("--gunloop") and not players.is_empty():
		var list := ["minigun", "flame", "laser", "shock", "net", "smg", "rpg", "magnum"]
		var gi := int(t / 20.0) % list.size()
		var me0: Player = players[my_idx]
		if gi != gunloop_i and me0.alive:
			gunloop_i = gi
			me0.slots[me0.cur] = full_slot(list[gi])
			me0.bombs = 2
			me0.smokes = 2
		if me0.alive and randf() < dt * 0.6:
			me0.inp.bomb = true
		if me0.alive and randf() < dt * 0.5:
			me0.inp.smoke = true
		if me0.alive and randf() < dt * 0.8:
			me0.inp.melee = true
	if not dedicated:
		human_input()
		if zoom_test:
			zoom_script(dt)
	pick_request = ""
	zoom_request = false
	for p in players:
		if p.bot:
			bot_think(p, dt)
	for p in players:
		if p.remote and not p.press_hold.is_empty():
			for kk in p.press_hold.keys():
				p.inp[kk] = true
			p.press_hold.clear()
	for p in players:
		update_player(p, dt)
	if net_role == "host":
		for p in players:
			p.hist.append(Vector3(t, p.x, p.y))
			while p.hist.size() > 2 and p.hist[0].x < t - 0.4:
				p.hist.pop_front()
	update_bullets(dt)
	update_grenades(dt)
	update_clouds(dt)
	update_blocks(dt)
	update_pickups(dt)
	update_parts(dt)
	update_events(dt)
	for f in feed:
		f.t -= dt
	feed = feed.filter(func(f): return f.t > 0)
	for tr in tracers:
		tr.t -= dt
	tracers = tracers.filter(func(tr): return tr.t > 0)
	shake = maxf(0.0, shake - dt * 30)
	big_t -= dt
	hurt_t -= dt
	hitmark_t -= dt
	if net_role == "host":
		net_host_tick(dt)
		pass
	if t >= match_time:
		state = "over"
		g_dir = 1.0
		g_target = 1.0
		jet_player.stop()
		if net_role == "host":
			send_end()

func team_scores() -> Array:
	var ts := [0, 0]
	for p in players:
		ts[p.side % 2] += p.kills
	return ts

func ranked() -> Array:
	var r := players.duplicate()
	r.sort_custom(func(a, b): return a.kills > b.kills or (a.kills == b.kills and a.deaths < b.deaths))
	return r

# ---------------- drawing helpers ----------------
func txt(s2: String, pos: Vector2, size: float, col: Color, align: int = 0, outline := 0.0, f: Font = null) -> void:
	if f == null:
		f = font
	col.a *= ga
	if col.a <= 0.004:
		return
	var fs := int(size)
	var x := pos.x
	if align != 0:
		var wdt := f.get_string_size(s2, HORIZONTAL_ALIGNMENT_LEFT, -1, fs).x
		x -= wdt / 2.0 if align == 1 else wdt
	if outline > 0:
		draw_string_outline(f, Vector2(x, pos.y), s2, HORIZONTAL_ALIGNMENT_LEFT, -1, fs, int(outline), Color(0, 0, 0, 0.75 * col.a))
	draw_string(f, Vector2(x, pos.y), s2, HORIZONTAL_ALIGNMENT_LEFT, -1, fs, col)

func tex_c(name: String, pos: Vector2, size: Vector2, col := Color.WHITE) -> void:
	draw_texture_rect(tex[name], Rect2(pos - size / 2.0, size), false, col)

var _sb := StyleBoxFlat.new()
func rbox(r: Rect2, col: Color, radius: float) -> void:
	_sb.bg_color = Color(col, col.a * ga)
	_sb.set_corner_radius_all(int(radius))
	_sb.anti_aliasing = true
	draw_style_box(_sb, r)

func gun_icon(gun: String, center_pos: Vector2, max_w: float, col := Color.WHITE) -> void:
	var m: Dictionary = META.GUN[gun]
	var wd: float = m.size[0]
	var ht: float = m.size[1]
	var k := max_w / wd
	tex_c("gun_" + gun, center_pos, Vector2(wd, ht) * k, col)

func w2s(p: Vector2) -> Vector2:
	return (p - cam) * zoom

# ---------------- drawing ----------------
func _draw() -> void:
	if dedicated:
		return
	var _d0 := Time.get_ticks_usec()
	_pm_t = _d0
	_draw_inner()
	_pm("rest")
	if prof_on:
		prof_draw.append(Time.get_ticks_usec() - _d0)
		prof_n += 1
		if prof_n % 300 == 0:
			var o := ""
			for k in prof_sec.keys():
				o += "%s=%dus " % [k, prof_sec[k] / 300]
			print("PROFSEC ", o)
			prof_sec.clear()

func _draw_inner() -> void:
	draw_set_transform_matrix(Transform2D.IDENTITY)
	panel_xf = Transform2D.IDENTITY
	ui_btns.clear()
	var vw := sw / zoom
	var vh := sh / zoom
	var in_menu: bool = MENU_STATES.has(state) or players.is_empty() or my_idx >= players.size()
	if in_menu:
		cam.x = fposmod(time_s * 25.0, WW - vw)
		cam.y = clampf(24 * T - vh / 2, 0, WH - vh)
	elif not players.is_empty():
		var me: Player = players[my_idx]
		var pc := center(me)
		# look a little ahead where you aim; the look-ahead glides on its own, slowly, so flicking
		# the aim never throws the screen around, and you always stay well inside the screen
		var reach: float = 40.0 + (view_h / S.view_h - 1.0) * vw * 0.16
		var look_want := Vector2(cos(me.aim) * reach, sin(me.aim) * reach * 0.5)
		look_want.x = clampf(look_want.x, -vw * 0.2, vw * 0.2)
		look_want.y = clampf(look_want.y, -vh * 0.14, vh * 0.14)
		var jumped: bool = cam_pc != Vector2.ZERO and pc.distance_to(cam_pc) > 300.0
		cam_pc = pc
		if jumped or not me.alive:
			cam_look = look_want
		else:
			cam_look += (look_want - cam_look) * ease_k(2.5, last_delta)
		var look := cam_look
		var tx := (WW - vw) / 2.0 if vw >= WW else clampf(pc.x + look.x - vw / 2.0, 0, WW - vw)
		var ty := (WH - vh) / 2.0 if vh >= WH else clampf(pc.y + look.y - vh / 2.0, 0, WH - vh)
		var want := Vector2(tx, ty)
		if zoom_test:
			zoom_log(me, pc, vw, vh)
		if me.alive:
			if cam == Vector2.ZERO or jumped or shot_at >= 0:
				cam = want
			else:
				cam += (want - cam) * ease_k(6.0, last_delta)
				# never let yourself slip near the edge of the screen
				if vw < WW:
					cam.x = clampf(cam.x, pc.x - vw * 0.82, pc.x - vw * 0.18)
					cam.x = clampf(cam.x, 0, WW - vw)
				if vh < WH:
					cam.y = clampf(cam.y, pc.y - vh * 0.8, pc.y - vh * 0.2)
					cam.y = clampf(cam.y, 0, WH - vh)
		elif me.respawn_t < 0.9:
			cam += (want - cam) * ease_k(5.0, last_delta)
	_pm("pre")
	draw_bg()
	_pm("bg")
	var shk := randf_range(-0.5, 0.5) * shake if shake > 0 else 0.0
	var wt := Transform2D(0.0, Vector2(zoom, zoom), 0.0, Vector2(-cam.x * zoom + shk, -cam.y * zoom + shk))
	draw_set_transform_matrix(wt)
	draw_zones()
	draw_tiles(vw, vh)
	_pm("tiles")
	if in_menu:
		for ac in menu_actors:
			draw_player(ac, wt)
		view_r = Rect2(-100000, -100000, 200000, 200000)
		draw_parts(wt)
		draw_set_transform_matrix(Transform2D.IDENTITY)
		vignette(Color(0.02, 0.03, 0.1, 0.45), 0.3)
		match state:
			"match_cfg":
				draw_cfg("MATCH SETTINGS", MATCH_ROWS)
			"ctrl_cfg":
				draw_cfg("CONTROLS", CONTROL_ROWS)
			"lan":
				draw_lan()
			"lan_join":
				draw_join()
			"online":
				draw_online()
			"ipkey":
				draw_ipkey()
			"connecting":
				draw_connecting()
			"lobby":
				draw_lobby()
			"lan_cfg":
				draw_cfg("MATCH SETTINGS", LAN_ROWS, "lobby_back")
			"locker":
				draw_locker()
			"namekey":
				draw_namekey()
			_:
				draw_menu()
		draw_top_layers()
		return
	leader_now = current_leader()
	view_r = (wt.affine_inverse() * Rect2(Vector2.ZERO, Vector2(sw, sh))).grow(90)
	draw_event_world()
	for k in pickups:
		if view_r.has_point(Vector2(k.x, k.y)):
			draw_pickup(k)
	for b in blocks:
		draw_texture_rect(tex.rock, Rect2(b.c * T, b.y, 2 * T, 2 * T), false)
	for cp in corpses:
		if view_r.has_point(Vector2(cp.x, cp.y)):
			draw_corpse(cp, wt)
	_pm("items")
	draw_set_transform_matrix(wt)
	for p in players:
		draw_player(p, wt)
	_pm("players")
	draw_set_transform_matrix(wt)
	draw_landing_marker()
	draw_set_transform_matrix(wt)
	for b in bullets:
		if not view_r.has_point(Vector2(b.x, b.y)):
			continue
		if b.flame:
			var fage := clampf(1.0 - b.life / maxf(0.05, b.max_life), 0.0, 1.0)
			var fsz := 14.0 + fage * 38.0
			draw_texture_rect(tex.flame, Rect2(b.x - fsz / 2, b.y - fsz / 2, fsz, fsz), false, Color(1, 1 - fage * 0.4, 1 - fage * 0.7, 0.95 - fage * 0.65))
			continue
		if b.net:
			draw_set_transform_matrix(wt * Transform2D(time_s * 9.0, Vector2.ONE, 0.0, Vector2(b.x, b.y)))
			draw_texture_rect(tex.net_overlay, Rect2(-9, -11, 18, 22), false)
			draw_set_transform_matrix(wt)
			continue
		if b.rocket:
			var a := atan2(b.vy, b.vx)
			draw_set_transform_matrix(wt * Transform2D(a, Vector2.ONE, 0.0, Vector2(b.x, b.y)))
			draw_rect(Rect2(-10, -2.5, 14, 5), Color("#6d7a3c"))
			draw_colored_polygon(PackedVector2Array([Vector2(4, -3.5), Vector2(11, 0), Vector2(4, 3.5)]), Color("#55642f"))
			draw_texture_rect(tex.glow, Rect2(-22, -7, 14, 14), false, Color(1, 0.7, 0.3, 0.9))
			draw_set_transform_matrix(wt)
		else:
			var tl: float = 0.03 if b.gun == "sniper" else 0.016
			draw_line(Vector2(b.x, b.y), Vector2(b.x - b.vx * tl, b.y - b.vy * tl), Color(1, 0.95, 0.7, 0.9), 2.6 if b.gun == "sniper" else 2.0, true)
	for g in grenades_list:
		if g.kind == "smoke":
			draw_set_transform_matrix(wt * Transform2D(g.rot, Vector2.ONE, 0.0, Vector2(g.x, g.y)))
			draw_texture_rect(tex.smoke_can, Rect2(-6, -8, 12, 16), false)
			draw_set_transform_matrix(wt)
			continue
		if g.kind == "bomb":
			draw_set_transform_matrix(wt)
			draw_texture_rect(tex.timebomb, Rect2(g.x - 8, g.y - 6, 16, 12), false)
			if sin(time_s * (6.0 + (4.5 - g.fuse) * 3.0)) > 0:
				draw_circle(Vector2(g.x + 4, g.y - 5), 2.0, C_RED)
			txt(str(ceili(g.fuse)), Vector2(g.x, g.y - 10), 11, C_RED, 1, 3)
			continue
		draw_set_transform_matrix(wt * Transform2D(g.rot, Vector2.ONE, 0.0, Vector2(g.x, g.y)))
		draw_texture_rect(tex.grenade, Rect2(-6, -7, 12, 14), false)
		if sin(g.fuse * 18) > 0.3:
			draw_circle(Vector2(2, -6), 1.6, C_RED)
		draw_set_transform_matrix(wt)
	draw_parts(wt)
	for tr in tracers:
		var ta: float = clampf(tr.t / tr.get("max", 0.22), 0, 1)
		match tr.get("kind", "line"):
			"laser":
				draw_line(tr.a, tr.b, Color(0.2, 0.9, 1, 0.35 * ta), 9.0 * ta + 1.0, true)
				draw_line(tr.a, tr.b, Color(0.85, 1, 1, ta), 2.6 * ta + 0.6, true)
			"zig":
				var pts := PackedVector2Array()
				var dv: Vector2 = tr.b - tr.a
				var nrm := Vector2(-dv.y, dv.x).normalized()
				for i in 9:
					var kk := i / 8.0
					var j := 0.0 if (i == 0 or i == 8) else randf_range(-7, 7)
					pts.append(tr.a + dv * kk + nrm * j)
				draw_polyline(pts, Color(0.55, 0.95, 1, 0.8 * ta), 4.0, true)
				draw_polyline(pts, Color(1, 1, 1, ta), 1.6, true)
			_:
				draw_line(tr.a, tr.b, Color(0.85, 0.92, 1, 0.35 * ta), 6.0 * ta + 1.0, true)
				draw_line(tr.a, tr.b, Color(1, 1, 1, 0.95 * ta), 2.2 * ta + 0.6, true)
	draw_water()
	draw_set_transform_matrix(Transform2D.IDENTITY)
	ga = 1.0
	if map_id == "catacombs":
		vignette(Color(0, 0, 0, 0.55), 0.28)
	draw_hud()
	if touch_mode or OS.has_feature("mobile") or (shot_at >= 0 and touch_mode):
		draw_touch()
	if state == "over":
		draw_over()
	elif state == "paused":
		draw_pause()
	draw_top_layers()

func draw_bg() -> void:
	if map_id == "catacombs":
		var t0 := Color("#120e14")
		var t1 := Color("#251c1e")
		draw_polygon(PackedVector2Array([Vector2(0, 0), Vector2(sw, 0), Vector2(sw, sh), Vector2(0, sh)]), PackedColorArray([t0, t0, t1, t1]))
		layer("bg_cat_far", 0.10, 1.02, 0.62, Color("#1a1418"))
		layer("bg_cat_mid", 0.28, 1.04, 0.6, Color("#261e1e"))
		return
	var top := Color("#3a7fca")
	var mid := Color("#7fbbe8")
	var hor := Color("#dcEEF7")
	var sun_col := Color(1, 0.98, 0.88)
	var cloud_col := Color(1, 1, 1, 0.92)
	if map_id == "outpost":
		top = Color("#35477e")
		mid = Color("#d98a5f")
		hor = Color("#f6cf8f")
		sun_col = Color(1, 0.82, 0.55)
		cloud_col = Color(1, 0.8, 0.7, 0.55)
	var my := sh * 0.45
	draw_polygon(PackedVector2Array([Vector2(0, 0), Vector2(sw, 0), Vector2(sw, my), Vector2(0, my)]), PackedColorArray([top, top, mid, mid]))
	draw_polygon(PackedVector2Array([Vector2(0, my), Vector2(sw, my), Vector2(sw, sh), Vector2(0, sh)]), PackedColorArray([mid, mid, hor, hor]))
	var sun := Vector2(sw * 0.78 - cam.x * zoom * 0.02, sh * (0.32 if map_id == "outpost" else 0.2))
	tex_c("glow", sun, Vector2(260, 260) * u * (1.5 if map_id == "outpost" else 1.0), Color(sun_col, 0.7))
	draw_circle(sun, 26 * u * (1.4 if map_id == "outpost" else 1.0), sun_col)
	for i in (3 if map_id == "outpost" else 5):
		var cw := (220.0 + i * 30) * u * 0.9
		var x := fposmod(i * 470.0 + time_s * (6 + i * 2) - cam.x * zoom * 0.08, sw + cw * 2) - cw
		var y := sh * (0.08 + 0.07 * (i % 3)) - cam.y * zoom * 0.03
		draw_texture_rect(tex["cloud%d" % (i % 3)], Rect2(x, y, cw, cw * 0.45), false, cloud_col)
	if map_id == "outpost":
		layer("bg_out_far", 0.10, 0.66, 0.31, Color("#b07054"))
		layer("bg_out_mid", 0.25, 0.80, 0.425, Color("#be925e"))
		layer("bg_out_near", 0.42, 0.93, 0.475, Color("#a0744a"))
		return
	layer("bg_mountains", 0.10, 0.66, 0.31, Color("#7e9cc0"))
	layer("bg_hills", 0.25, 0.80, 0.425, Color("#42724a"))
	layer("bg_near", 0.42, 0.93, 0.475, Color("#2e5434"))

func layer(name: String, par: float, anchor: float, scale: float, fill: Color) -> void:
	var tx: Texture2D = tex[name]
	var k := zoom * scale * 0.9
	var wdt := tx.get_width() * k
	var ht := tx.get_height() * k
	var base := sh * anchor + (WH * 0.55 - cam.y - sh / zoom / 2.0) * zoom * par
	var x := -fposmod(cam.x * zoom * par, wdt)
	while x < sw:
		draw_texture_rect(tx, Rect2(x, base - ht, wdt, ht), false)
		x += wdt
	if base < sh:
		draw_rect(Rect2(0, base - 1, sw, sh - base + 1), fill)

func draw_tiles(vw: float, vh: float) -> void:
	var c0 := maxi(0, floori(cam.x / T) - 1)
	var c1 := mini(COLS - 1, ceili((cam.x + vw) / T) + 1)
	var r0 := maxi(0, floori(cam.y / T) - 1)
	var r1 := mini(ROWS - 1, ceili((cam.y + vh) / T) + 1)
	var rock_tx: Texture2D = tex.rock
	var dirt_pre := "dirt"
	var cap_tx: Texture2D = tex.grass
	if map_id == "outpost":
		rock_tx = tex.concrete
		dirt_pre = "sand"
		cap_tx = tex.sandcap
	elif map_id == "catacombs":
		rock_tx = tex.brick
		dirt_pre = "cave"
		cap_tx = tex.moss
	var shake_set := {}
	if ev != null and ev.phase == "warn" and ev.name == "brk":
		for v in ev.tiles:
			shake_set[v] = true
	for r in range(r0, r1 + 1):
		for c in range(c0, c1 + 1):
			var v := tiles[r * COLS + c]
			if v == EMPTY:
				continue
			var pos := Vector2(c * T, r * T)
			var shaking := shake_set.has(Vector2i(c, r))
			if shaking:
				var amt: float = (1.0 - ev.t / S.event_warn) * 2.5
				pos += Vector2(randf_range(-amt, amt), randf_range(-amt, amt))
			var rect := Rect2(pos, Vector2(T, T))
			var hpk: float = thp[r * COLS + c] / TILE_HP.get(v, 99.0)
			if v == ROCK:
				draw_texture_rect(rock_tx, rect, false)
			elif v == WOOD:
				draw_texture_rect(tex.wood, Rect2(pos + Vector2(0, 2), Vector2(T, T - 6)), false)
			elif v == CRATE:
				draw_texture_rect(tex.crate, rect, false)
			else:
				draw_texture_rect(tex["%s%d" % [dirt_pre, (c * 7 + r * 3) % 3]], rect, false)
				if not solid_at(c, r + 1):
					draw_rect(Rect2(pos.x, pos.y + T - 7, T, 7), Color(0.18, 0.1, 0.05, 0.35))
				if not solid_at(c - 1, r):
					draw_rect(Rect2(pos.x, pos.y, 4, T), Color(0.2, 0.12, 0.06, 0.22))
				if not solid_at(c + 1, r):
					draw_rect(Rect2(pos.x + T - 4, pos.y, 4, T), Color(0.2, 0.12, 0.06, 0.22))
			if v != ROCK:
				if shaking or hpk < 0.4:
					draw_texture_rect(tex.crack2, rect, false)
				elif hpk < 0.75:
					draw_texture_rect(tex.crack1, rect, false)
	# grass caps after all tiles so blades sit on top
	for r in range(r0, r1 + 1):
		for c in range(c0, c1 + 1):
			if tiles[r * COLS + c] == DIRT and not solid_at(c, r - 1):
				draw_texture_rect(cap_tx, Rect2(c * T - 1, r * T - 5, T + 2, 16), false)
	for tp in torches:
		if tp.x >= c0 - 1 and tp.x <= c1 + 1 and tp.y >= r0 - 2 and tp.y <= r1 + 1:
			var fl := 0.85 + 0.15 * sin(time_s * 13.0 + tp.x) + 0.05 * sin(time_s * 31.0 + tp.y)
			var tc := Vector2(tp.x * T + 16, tp.y * T + 10)
			draw_texture_rect(tex.glow, Rect2(tc - Vector2(70, 70) * fl, Vector2(140, 140) * fl), false, Color(1, 0.62, 0.25, 0.42))
			draw_texture_rect(tex.torch, Rect2(tc - Vector2(8, 20), Vector2(16, 32)), false)

func draw_zones() -> void:
	if not cfg.zones:
		return
	for z in zones:
		var low: bool = z.type == "low"
		var r: Rect2 = z.rect
		var col := C_CYAN if low else C_PINK
		draw_rect(r, Color(col, 0.10))
		var corners := [r.position, Vector2(r.end.x, r.position.y), r.end, Vector2(r.position.x, r.end.y), r.position]
		for i in 4:
			draw_dashed_line(corners[i], corners[i + 1], Color(col, 0.7), 2, 10)
		if low:
			for i in 36:
				var px: float = r.position.x + fmod(i * 97.0, r.size.x)
				var py: float = r.end.y - fposmod(time_s * 18 * gsign() + i * 53, r.size.y)
				draw_circle(Vector2(px, py), 2.0 + (i % 3), Color(1, 1, 1, 0.35))
		else:
			for i in 8:
				for j in 7:
					var px: float = r.position.x + 30 + i * 52
					var py: float = r.position.y + fposmod(j * 70 + time_s * 80 * gsign(), r.size.y)
					draw_polyline(PackedVector2Array([Vector2(px - 9, py - 7 * gsign()), Vector2(px, py), Vector2(px + 9, py - 7 * gsign())]), Color(col, 0.3), 3, true)
		var label := "LOW GRAVITY" if low else "HEAVY GRAVITY  2X FUEL"
		rbox(Rect2(r.position + Vector2(6, 6), Vector2(font.get_string_size(label, 0, -1, 12).x + 14, 20)), Color(0.05, 0.06, 0.14, 0.6), 6)
		txt(label, r.position + Vector2(13, 21), 12, col)

func draw_player(p: Player, wt: Transform2D) -> void:
	if not p.alive:
		return
	var c := center(p)
	if net_role == "client" and is_me(p):
		c += pred_off
	var face := 1.0 if cos(p.draw_aim) >= 0 else -1.0
	var gs := gsign()
	var base := wt * Transform2D(0.0, Vector2(face, gs), 0.0, c)
	var la := atan2(sin(p.draw_aim) * gs, cos(p.draw_aim) * face)
	var tint := Color(1.6, 1.6, 1.6) if p.flash > 0 else Color.WHITE
	var bage := time_s - p.born_t
	if bage < 0.6 and bage >= 0.0 and not p.actor:
		draw_drop_beam(c, bage, wt)
		tint.a = clampf(bage / 0.3, 0.15, 1.0)
	var prone := p.posture == "prone"
	var crouch := p.posture == "crouch"
	var bob := 0.0
	if p.on_ground and not prone:
		bob = sin(time_s * 2.4 + p.id) * 0.5 if absf(p.vx) < 15 else -absf(sin(p.walk)) * 1.2
	var body: Transform2D
	var gun_rot := la
	if prone:
		body = base * Transform2D(PI / 2, Vector2.ONE, 0.0, Vector2(-4, 1))
		gun_rot = la - PI / 2
	else:
		body = base * Transform2D(0.0, Vector2.ONE, 0.0, Vector2(0, (1.0 if crouch else 0.0) + bob))
	gun_rot += 0.5 * p.reload_k
	if p.switch_t > 0:
		gun_rot += 1.1 * sin(PI * clampf(p.switch_t / 0.22, 0, 1))
	var mk := clampf(1.0 - p.melee_anim / 0.28, 0, 1) if p.melee_anim > 0 else -1.0
	if mk >= 0:
		gun_rot += 0.7 * sin(mk * PI)
	draw_set_transform_matrix(body)
	var lk := plook(p)
	av_back(lk, tint)
	var fcol = AV_FLAME.get(lk.fl)
	if p.jet_on and fcol != null:
		var fl := 16.0 + sin(time_s * 38.0 + p.id) * 4.0 + sin(time_s * 21.0) * 2.0
		for nx in [-12.0, -6.0]:
			draw_texture_rect(tex.glow, Rect2(nx - 6, 9, 12, fl), false, fcol[0])
			draw_texture_rect(tex.glow, Rect2(nx - 3.5, 9, 7, fl * 0.6), false, fcol[1])
	draw_leg(body, Vector2(-3, 4), p.leg_b, p.shin_b, Color(0.78, 0.78, 0.78) * tint, leg_tex(lk))
	draw_set_transform_matrix(body)
	av_jet(lk, tint)
	var w = p.slots[p.cur]
	var gun: String = w.type if w != null else "magnum"
	var m: Dictionary = META.GUN[gun]
	var gd: float = S.gun_draw
	var sh_pt := Vector2(1, -6)
	var dir := Vector2(cos(gun_rot), sin(gun_rot))
	var grip := sh_pt + dir * (7.0 - p.recoil)
	var front_hand := grip + (Vector2(m.front[0] - m.grip[0], m.front[1] - m.grip[1]) * gd).rotated(gun_rot)
	var sleeve: Color = sleeve_col(p.color, lk).darkened(0.2)
	var dual: bool = w != null and w.get("dual", false)
	var grip2 := sh_pt + Vector2(-3, 3) + dir * (7.0 - p.recoil * 0.5)
	var back_tgt := grip2 if dual else grip
	if p.protect_t > 0:
		tint.a = 0.45 + 0.4 * absf(sin(time_s * 10.0))
	draw_line(sh_pt + Vector2(-2, 0), back_tgt, C_OUT, 6.0, true)
	draw_line(sh_pt + Vector2(-2, 0), back_tgt, sleeve * tint, 4.0, true)
	if dual:
		draw_set_transform_matrix(body * Transform2D(gun_rot, Vector2.ONE, 0.0, grip2))
		var gsz2 := Vector2(m.size[0], m.size[1]) * gd
		draw_texture_rect(tex["gun_" + gun], Rect2(-m.grip[0] * gd, -m.grip[1] * gd, gsz2.x, gsz2.y), false, Color(0.8, 0.8, 0.8) * tint)
		draw_texture_rect(tex.hand, Rect2(-3, -3, 6, 6), false)
		draw_set_transform_matrix(body)
	av_torso(lk, p.color, tint)
	draw_leg(body, Vector2(3, 4), p.leg_f, p.shin_f, tint, leg_tex(lk))
	var head_rot := clampf(la, -0.5, 0.5) * 0.35 + (-PI / 2 if prone else 0.0)
	draw_set_transform_matrix(body * Transform2D(head_rot, Vector2.ONE, 0.0, Vector2(1, -15)))
	av_head(lk, p.color, tint)
	draw_set_transform_matrix(body * Transform2D(gun_rot, Vector2.ONE, 0.0, grip))
	var gsz := Vector2(m.size[0], m.size[1]) * gd
	draw_texture_rect(tex["gun_" + gun], Rect2(-m.grip[0] * gd, -m.grip[1] * gd, gsz.x, gsz.y), false, tint)
	if gun == "minigun" and p.spin > 0.05:
		for bi in 5:
			var by: float = (4.6 + 1.9 * bi - m.grip[1]) * gd
			var fl: float = 0.5 + 0.5 * sin(time_s * 70.0 * p.spin + bi * 1.3)
			draw_line(Vector2((25.0 - m.grip[0]) * gd, by), Vector2((45.0 - m.grip[0]) * gd, by), Color(0.85, 0.88, 0.95, 0.55 * fl * p.spin), 1.2)
	if p.muzzle_t > 0 and gun != "rpg" and not ["laser", "shock", "net", "flame"].has(gun):
		var mz := Vector2(m.muzzle[0] - m.grip[0], m.muzzle[1] - m.grip[1]) * gd
		var fw := 24.0 * (1.3 if gun == "shotgun" else 1.0)
		draw_texture_rect(tex.flash, Rect2(mz.x - 1, mz.y - 7, fw, 14), false)
	if p.muzzle_t > 0 and (gun == "laser" or gun == "shock"):
		var mz2 := Vector2(m.muzzle[0] - m.grip[0], m.muzzle[1] - m.grip[1]) * gd
		draw_texture_rect(tex.glow, Rect2(mz2 - Vector2(8, 8), Vector2(16, 16)), false, Color(0.5, 0.95, 1, 0.9))
	draw_set_transform_matrix(body)
	var fh := grip if dual else front_hand
	var ka := 0.0
	if mk >= 0:
		var e := mk * mk * (3.0 - 2.0 * mk)
		ka = lerpf(-1.7, 0.9, e)
		fh = sh_pt + Vector2(cos(ka), sin(ka)) * 12.0
	draw_line(sh_pt + Vector2(3, 0), fh, C_OUT, 6.0, true)
	draw_line(sh_pt + Vector2(3, 0), fh, sleeve_col(p.color, lk) * tint, 4.0, true)
	draw_texture_rect(tex.hand, Rect2(fh - Vector2(3, 3), Vector2(6, 6)), false)
	draw_texture_rect(tex.hand, Rect2(grip - Vector2(3, 3), Vector2(6, 6)), false)
	if mk >= 0:
		draw_arc(sh_pt, 24, -1.7, ka, 14, Color(1, 1, 1, 0.55 * (1.0 - mk) + 0.15), 4, true)
		draw_set_transform_matrix(body * Transform2D(ka, Vector2.ONE, 0.0, fh))
		draw_texture_rect(tex.knife, Rect2(-3, -3, 18, 6), false)
		draw_set_transform_matrix(body)
	av_front(lk, tint)
	if p.protect_t > 0:
		draw_arc(Vector2(0, -4), 30, 0, TAU, 40, Color(0.5, 0.9, 1.0, 0.25), 2.0, true)
		draw_arc(Vector2(0, -4), 30, -PI / 2, -PI / 2 + TAU * clampf(p.protect_t / S.protect, 0.0, 1.0), 40, Color(0.6, 0.95, 1.0, 0.9), 3.0, true)
		var sa: float = S.protect - p.protect_t
		if sa < 0.5:
			draw_arc(Vector2(0, -4), 30 + sa * 90, 0, TAU, 48, Color(1, 1, 1, (1.0 - sa / 0.5) * 0.8), 3.0, true)
	draw_set_transform_matrix(wt)
	if p.net_t > 0:
		var nsz := Vector2(48, 30) if prone else Vector2(36, 46)
		tex_c("net_overlay", c + Vector2(0, -4 * gs), nsz, Color(1, 1, 1, clampf(p.net_t, 0, 1)))
	if p.burn_t > 0:
		for i in 4:
			var fo := Vector2(sin(time_s * 11.0 + i * 1.7) * 7.0, -6.0 * gs - i * 6.0 * gs + sin(time_s * 17.0 + i) * 3.0)
			var fs2 := 16.0 + 6.0 * sin(time_s * 13.0 + i * 2.0)
			draw_texture_rect(tex.flame, Rect2(c + fo - Vector2(fs2, fs2) / 2, Vector2(fs2, fs2)), false, Color(1, 1, 1, 0.85))
	if p.stun_t > 0:
		for i in 3:
			var zp := PackedVector2Array()
			var ang0 := randf() * TAU
			for j in 6:
				var aa := ang0 + j * 0.5
				zp.append(c + Vector2(cos(aa), sin(aa)) * randf_range(14, 24))
			draw_polyline(zp, Color(0.6, 0.95, 1, 0.85), 1.6, true)
	var hpos := head_pos(p)
	var ty := hpos.y - 24 if gs > 0 else hpos.y + 34
	var tag_col: Color = p.color
	if cfg.mode == "team":
		tag_col = Color("#5ec8ff") if p.side == 0 else Color("#ff6b6b")
	if p.actor:
		return
	if p == leader_now:
		draw_crown(Vector2(c.x, ty - (16 if (not is_me(p) or cfg.mode == "team") else 2)), 7)
	if not is_me(p) or cfg.mode == "team":
		txt(p.pname, Vector2(c.x, ty), 11, tag_col, 1, 3)
		rbox(Rect2(c.x - 15, ty + 3, 30, 5), Color(0, 0, 0, 0.55), 2)
		rbox(Rect2(c.x - 15, ty + 3, 30 * clampf(p.hp / S.hp_max, 0, 1), 5), C_GREEN if p.hp > 40 else C_RED, 2)
	if p.say_t > 0:
		var bw := font.get_string_size(p.say, 0, -1, 11).x + 14
		rbox(Rect2(c.x - bw / 2, ty - 30, bw, 19), Color(1, 1, 1, 0.92), 8)
		txt(p.say, Vector2(c.x, ty - 16), 11, Color("#1b1d2a"), 1)

func draw_leg(base: Transform2D, hip: Vector2, ang: float, shin: float, col: Color, tn := "leg") -> void:
	draw_set_transform_matrix(base * Transform2D(ang, Vector2.ONE, 0.0, hip))
	draw_texture_rect_region(tex[tn], Rect2(-4.5, -1, 9, 9.5), Rect2(0, 0, 27, 28.5), col)
	var knee := hip + Vector2(-sin(ang), cos(ang)) * 7.8
	draw_set_transform_matrix(base * Transform2D(shin, Vector2.ONE, 0.0, knee))
	draw_texture_rect_region(tex[tn], Rect2(-4.5, -0.8, 9, 9), Rect2(0, 24, 27, 27), col)

func draw_corpse(cp: Corpse, wt: Transform2D) -> void:
	var a := 1.0 - clampf((cp.t - 2.2) / 0.8, 0, 1)
	draw_set_transform_matrix(wt * Transform2D(cp.rot, Vector2(cp.face, gsign()), 0.0, Vector2(cp.x, cp.y)))
	var lk: Dictionary = cp.look if not cp.look.is_empty() else default_look
	var tc: Color = TEAM_COL[maxi(0, TEAMS.find(cp.team))]
	var cc := Color(0.85, 0.85, 0.85, a)
	draw_texture_rect(tex[leg_tex(lk)], Rect2(-7, 2, 9, 17), false, Color(0.8, 0.8, 0.8, a))
	av_jet(lk, cc)
	av_torso(lk, tc, cc)
	draw_set_transform_matrix(wt * Transform2D(cp.rot, Vector2(cp.face, gsign()), 0.0, Vector2(cp.x, cp.y)) * Transform2D(0.0, Vector2.ONE, 0.0, Vector2(1, -18)))
	av_head(lk, tc, cc)

func draw_parts(wt: Transform2D) -> void:
	draw_set_transform_matrix(wt)
	for q in parts:
		if not view_r.has_point(Vector2(q.x, q.y)):
			continue
		var k: float = clampf(q.life / q.max_life, 0, 1)
		var col: Color = q.color
		col.a *= k if q.tex != "" else minf(1.0, k * 2.0)
		var sz: float = lerpf(q.size1, q.size, k)
		if q.tex == "":
			if q.spin != 0.0:
				draw_set_transform_matrix(wt * Transform2D(q.rot, Vector2.ONE, 0.0, Vector2(q.x, q.y)))
				draw_rect(Rect2(-sz / 2, -sz / 4, sz, sz / 2), col)
				draw_set_transform_matrix(wt)
			else:
				draw_rect(Rect2(q.x - sz / 2, q.y - sz / 2, sz, sz), col)
		else:
			draw_texture_rect(tex[q.tex], Rect2(q.x - sz / 2, q.y - sz / 2, sz, sz), false, col)

func draw_pickup(k: Pickup) -> void:
	var bob := sin(time_s * 3 + k.x) * 2
	var cpos := Vector2(k.x + k.w / 2, k.y + k.h / 2 + bob)
	tex_c("glow", cpos, Vector2(44, 30), Color(1, 0.95, 0.6, 0.35 + 0.15 * sin(time_s * 4)))
	if k.type == "health":
		tex_c("medkit", cpos, Vector2(22, 18))
		return
	if k.type == "bomb":
		tex_c("timebomb", cpos, Vector2(18, 14))
		txt("TIME BOMB", cpos + Vector2(0, -12), 8, Color.WHITE, 1, 3)
		return
	if k.type == "smoke":
		tex_c("smoke_can", cpos, Vector2(12, 16))
		txt("SMOKE", cpos + Vector2(0, -12), 8, Color.WHITE, 1, 3)
		return
	if k.type == "grenade":
		tex_c("grenade", cpos + Vector2(-5, 0), Vector2(12, 14))
		tex_c("grenade", cpos + Vector2(6, 1), Vector2(12, 14))
		return
	var m: Dictionary = META.GUN[k.gun]
	gun_icon(k.gun, cpos, m.size[0] * S.gun_draw)
	if not (players.size() > 0 and players[my_idx].alive and overlaps(players[my_idx], k)):
		txt(WD[k.gun].name, cpos + Vector2(0, -14), 9, Color.WHITE, 1, 3)

func draw_event_world() -> void:
	if ev == null:
		return
	var blink := sin(time_s * 10) > 0
	if ev.name == "roof" and (ev.phase == "warn" or ev.spawned < ev.cols.size()):
		for i in ev.cols.size():
			if ev.phase == "active" and i < ev.spawned:
				continue
			var c: int = ev.cols[i]
			var rs := roof_start(c)
			var r := rs
			while r < ROWS - 3 and not solid_at(c, r + 2) and not solid_at(c + 1, r + 2):
				r += 1
			var gy: float = (r + 2) * T
			draw_rect(Rect2(c * T, rs * T, 2 * T, gy - rs * T), Color(C_RED, 0.12 if blink else 0.06))
			var rx := T * (0.6 + 0.4 * sin(time_s * 4))
			draw_colored_polygon(ellipse_pts(Vector2(c * T + T, gy - 2), rx, 6), Color(0.6, 0, 0.05, 0.45))
	elif ev.name == "water" and ev.phase == "warn":
		draw_dashed_line(Vector2(T, water_row * T), Vector2(WW - T, water_row * T), Color("#2f7fd8"), 3, 14)
		var lx0: float = clampf(cam.x + 40, T, WW - 300)
		txt("WATER WILL RISE TO HERE", Vector2(lx0, water_row * T - 8), 14, Color("#bfe0ff"), 0, 4)

func ellipse_pts(cpos: Vector2, rx: float, ry: float) -> PackedVector2Array:
	var pts := PackedVector2Array()
	for i in 20:
		var a := TAU * i / 20.0
		pts.append(cpos + Vector2(cos(a) * rx, sin(a) * ry))
	return pts

func draw_water() -> void:
	if water_y >= WH - 2 * T:
		return
	var pts := PackedVector2Array()
	pts.append(Vector2(0, WH))
	var x := 0.0
	while x <= WW:
		pts.append(Vector2(x, water_y + sin(time_s * 2.2 + x * 0.018) * 4 + sin(time_s * 3.1 + x * 0.05) * 1.5))
		x += 24
	pts.append(Vector2(WW, WH))
	draw_colored_polygon(pts, Color(0.16, 0.5, 0.86, 0.5))
	var line := pts.slice(1, pts.size() - 1)
	draw_polyline(line, Color(0.85, 0.95, 1, 0.8), 2.5, true)

func bar(pos: Vector2, w: float, h: float, val: float, col: Color, label: String, trail := -1.0) -> void:
	fbox(Rect2(pos - Vector2(3, 3) * u, Vector2(w, h) + Vector2(6, 6) * u), Color(0.04, 0.05, 0.12, 0.62), 7 * u, Color(1, 1, 1, 0.1), maxf(1.0, u))
	rbox(Rect2(pos, Vector2(w, h)), Color(0, 0, 0, 0.4), 4 * u)
	if trail > val + 0.005:
		rbox(Rect2(pos, Vector2(w * clampf(trail, 0, 1), h)), Color(1, 0.92, 0.85, 0.8), 4 * u)
	if val > 0.01:
		rbox(Rect2(pos, Vector2(w * clampf(val, 0, 1), h)), col, 4 * u)
		rbox(Rect2(pos + Vector2(2 * u, 1.5 * u), Vector2(maxf(0, w * clampf(val, 0, 1) - 4 * u), h * 0.32)), Color(1, 1, 1, 0.28), 3 * u)
	txh(label, pos + Vector2(8 * u, h - 3 * u), 11 * u, Color(1, 1, 1, 0.97), 0, 3 * u)

func draw_bubble(me: Player) -> void:
	var k = near_gun(me)
	if k == null:
		bubble_key = ""
		return
	var opts := pickup_opts(me, k)
	if opts.is_empty():
		return
	var bkey := "%s%d" % [k.gun, int(k.x / 16) * 1000 + int(k.y / 16)]
	if bkey != bubble_key:
		bubble_key = bkey
		bubble_since = time_s
	var r := 28.0 * u * (1.0 + 0.04 * sin(time_s * 5.0)) * maxf(0.05, ease_back((time_s - bubble_since) / 0.25))
	var pc := w2s(center(me))
	var mid := Vector2(pc.x, maxf(pc.y - 80 * u, 70 * u))
	var desk := not (touch_mode or OS.has_feature("mobile"))
	for i in opts.size():
		var opt: String = opts[i]
		var pos := mid + Vector2((i - (opts.size() - 1) / 2.0) * (r * 2.0 + 14 * u), 0)
		draw_colored_polygon(PackedVector2Array([pos + Vector2(-8 * u, r * 0.8), pos + Vector2(8 * u, r * 0.8), pos + Vector2((mid.x - pos.x) * 0.3, r + 14 * u)]), Color(1, 1, 1, 0.95))
		draw_circle(pos, r + 2 * u, Color(0.1, 0.12, 0.2, 0.9))
		draw_circle(pos, r, Color(1, 1, 1, 0.95) if opt == "swap" else Color(1, 0.92, 0.6, 0.97))
		if opt == "dual":
			gun_icon(k.gun, pos + Vector2(-4 * u, -7 * u), r * 1.25)
			gun_icon(k.gun, pos + Vector2(4 * u, 1 * u), r * 1.25)
		else:
			gun_icon(k.gun, pos + Vector2(0, -3 * u), r * 1.55)
		var lab := "DUAL" if opt == "dual" else "SWAP"
		if desk:
			lab += " (" + ("V" if opt == "dual" else "E") + ")"
		txt(lab, pos + Vector2(0, r * 0.66), 9 * u, Color("#1b1d2a"), 1)
		bubbles.append({"pos": pos, "r": r, "opt": opt})
	txt(WD[k.gun].name, mid + Vector2(0, -r - 8 * u), 11 * u, C_ARC, 1, 3 * u)

func draw_hud() -> void:
	bubbles.clear()
	var me: Player = players[my_idx]
	var sx := 38 * u + safe_l
	var sy := 12 * u
	var bw := minf(170 * u, sw * 0.22)
	var dd := last_delta
	if me.hp < hud_prev_hp - 0.5:
		trail_hold = 0.45
	hud_prev_hp = me.hp
	hud_hp = lerpf(hud_hp, me.hp, ease_k(16.0, dd))
	trail_hold -= dd
	if me.hp >= trail_hp:
		trail_hp = me.hp
	elif trail_hold <= 0:
		trail_hp = move_toward(trail_hp, me.hp, 70.0 * dd)
	bar(Vector2(sx, sy), bw, 15 * u, hud_hp / S.hp_max, C_GREEN if me.hp > 40 else C_RED, "%d" % ceili(me.hp), trail_hp / S.hp_max)
	tex_c("medkit", Vector2(sx - 18 * u, sy + 7 * u), Vector2(19, 16) * u)
	bar(Vector2(sx, sy + 24 * u), bw, 12 * u, me.fuel / S.fuel_max, Color("#4fc3ff") if me.fuel > 20 else Color("#ff8a3d"), "JET")
	tex_c("jetpack", Vector2(sx - 18 * u, sy + 30 * u), Vector2(11, 17) * u)
	var c := center(me)
	var z = zone_at(c.x, c.y)
	var fy := sy + 60 * u
	var lx := sx - 26 * u
	if me.alive and me.in_water:
		txt("IN WATER: NO JETPACK, LOSING HEALTH", Vector2(lx, fy), 11 * u, Color("#8fd0ff"), 0, 3 * u)
		fy += 16 * u
	elif me.alive and z != null:
		txt("LOW GRAVITY: FUEL LASTS LONGER" if z.type == "low" else "HEAVY GRAVITY: FUEL BURNS 2X", Vector2(lx, fy), 11 * u, C_CYAN if z.type == "low" else C_PINK, 0, 3 * u)
		fy += 16 * u
	for f in feed:
		var fk := ease_out((float(f.get("t0", 5.0)) - f.t) / 0.25)
		var a := clampf(f.t, 0, 1) * fk
		var x := lx - (1.0 - fk) * 30 * u
		if f.k != "":
			txt(f.k, Vector2(x, fy), 11 * u, Color(f.kc, a), 0, 3 * u)
			x += font.get_string_size(f.k, 0, -1, int(11 * u)).x + 6 * u
			if WD.has(f.gun):
				gun_icon(f.gun, Vector2(x + 14 * u, fy - 4 * u), 28 * u, Color(1, 1, 1, a))
				x += 32 * u
			else:
				var ic: String = {"grenade": "BOOM", "rpg": "BOOM", "bomb": "BOOM", "melee": "KNIFE", "smoke": "GAS"}.get(f.gun, ">")
				txt(ic, Vector2(x, fy), 10 * u, Color(C_ARC, a), 0, 3 * u)
				x += font.get_string_size(ic, 0, -1, int(10 * u)).x + 6 * u
			if f.head:
				txt("HEADSHOT", Vector2(x, fy), 9 * u, Color(C_RED, a), 0, 3 * u)
				x += font.get_string_size("HEADSHOT", 0, -1, int(9 * u)).x + 6 * u
			txt(f.v, Vector2(x, fy), 11 * u, Color(C_RED if f.get("vi", -1) == my_idx else f.vc, a), 0, 3 * u)
		else:
			txt(f.v + (" " + f.note if f.note != "" else ""), Vector2(x, fy), 11 * u, Color(C_RED if f.get("vi", -1) == my_idx else f.vc, a), 0, 3 * u)
		fy += 17 * u
	var left: float = maxf(0.0, match_time - t)
	timer_rect = Rect2(sw / 2 - 56 * u, 8 * u, 112 * u, 44 * u)
	fbox(timer_rect, Color(0.04, 0.05, 0.12, 0.58), 10 * u, Color(1, 1, 1, 0.1), maxf(1.0, u))
	txh("%d:%02d" % [int(left) / 60, int(left) % 60], Vector2(sw / 2, 33 * u), 22 * u, C_RED if left < 10 else C_INK, 1, 3 * u)
	if cfg.mode == "team":
		var ts := team_scores()
		txt("BLUE %d  :  %d RED" % [ts[0], ts[1]], Vector2(sw / 2, 46 * u), 10 * u, C_INK, 1)
	else:
		txt("KILLS %d   DEATHS %d" % [me.kills, me.deaths], Vector2(sw / 2, 46 * u), 9 * u, C_MUTED, 1)
	pause_rect = Rect2(sw / 2 - 98 * u, 12 * u, 34 * u, 34 * u)
	rbox(pause_rect, Color(0.04, 0.05, 0.12, 0.55), 17 * u)
	draw_rect(Rect2(pause_rect.position + Vector2(11 * u, 10 * u), Vector2(4 * u, 14 * u)), C_INK)
	draw_rect(Rect2(pause_rect.position + Vector2(19 * u, 10 * u), Vector2(4 * u, 14 * u)), C_INK)
	var w = me.slots[me.cur]
	if w != null and me.alive:
		var pc := Vector2(sw / 2, sh - 34 * u)
		rbox(Rect2(pc.x - 90 * u, pc.y - 24 * u, 180 * u, 44 * u), Color(0.04, 0.05, 0.12, 0.55), 10 * u)
		gun_icon(w.type, pc + Vector2(-44 * u, -2 * u), 66 * u)
		if zoom_level(me) > 1:
			txt("%dX" % zoom_level(me), Vector2(pc.x - 84 * u, pc.y - 10 * u), 11 * u, C_CYAN, 0, 3 * u)
		if w.get("dual", false):
			txt("x2", Vector2(pc.x - 84 * u, pc.y + 14 * u), 12 * u, C_ARC, 0, 3 * u)
		if me.posture != "stand":
			txt("CRAWLING" if me.posture == "prone" else "SITTING", Vector2(pc.x, pc.y - 30 * u), 10 * u, C_MUTED, 1, 3 * u)
		if last_mag >= 0 and w.mag < last_mag:
			ammo_pop = 1.0
		last_mag = w.mag
		txh("%d" % w.mag, Vector2(pc.x + 38 * u, pc.y + 7 * u), 22 * u * (1.0 + 0.18 * ammo_pop), C_INK.lerp(C_ARC, ammo_pop) if w.mag > 0 else C_RED, 2, 3 * u)
		txt("/ %d" % w.spare, Vector2(pc.x + 42 * u, pc.y + 6 * u), 12 * u, C_MUTED, 0, 3 * u)
		if me.reload_t > 0:
			var k: float = 1.0 - me.reload_t / maxf(0.01, me.reload_total)
			rbox(Rect2(pc.x - 80 * u, pc.y + 12 * u, 160 * u, 4 * u), Color(0, 0, 0, 0.5), 2 * u)
			rbox(Rect2(pc.x - 80 * u, pc.y + 12 * u, 160 * u * k, 4 * u), C_ARC, 2 * u)
			txt("RELOADING", Vector2(pc.x, pc.y - 30 * u), 11 * u, C_ARC, 1, 3 * u)
	if ev != null:
		var info: Dictionary = EVENTS[ev.name]
		var title: String = info.label
		var sub: String = info.tip
		var show := false
		if ev.phase == "warn":
			title = "%s IN %d" % [info.label, ceili(ev.t)]
			show = true
		elif ev.name == "flip":
			sub = "Gravity goes back in %d" % ceili(ev.t)
			show = true
		elif ev.dur - ev.t < 3.0:
			show = true
		if show:
			var bw2: float = minf(sw - 32 * u, 430 * u)
			var by := 60 * u
			rbox(Rect2(sw / 2 - bw2 / 2, by, bw2, 50 * u), Color(0.04, 0.05, 0.12, 0.7), 10 * u)
			txt(title, Vector2(sw / 2, by + 23 * u), 17 * u, C_RED if ev.phase == "warn" else C_ARC, 1, 3 * u)
			txt(sub, Vector2(sw / 2, by + 41 * u), 11 * u, C_INK, 1)
	if big_t > 0 and me.alive:
		var age := 1.6 - big_t
		var bk := ease_back(age / 0.3)
		var a2 := clampf(big_t / 0.45, 0, 1) * clampf(age / 0.08, 0, 1)
		txh(big_msg, Vector2(sw / 2, sh * 0.34), 32 * u * lerpf(1.7, 1.0, bk), Color(C_ARC, a2), 1, 7 * u)
	if intro_t < 2.4 and me.alive:
		var ik := ease_back(intro_t / 0.35)
		var ia := clampf((2.4 - intro_t) / 0.5, 0, 1) * clampf(intro_t / 0.1, 0, 1)
		txh("FIGHT!", Vector2(sw / 2, sh * 0.33), 46 * u * lerpf(1.8, 1.0, ik), Color(C_ARC, ia), 1, 8 * u)
		var goal := "Blue vs Red. Most kills wins." if cfg.mode == "team" else "Most kills in %d:%02d wins." % [int(match_time) / 60, int(match_time) % 60]
		txt(goal, Vector2(sw / 2, sh * 0.33 + 30 * u), 14 * u, Color(C_INK, ia * clampf((intro_t - 0.2) / 0.3, 0, 1)), 1, 4 * u)
	if me.alive and me.protect_t > S.protect - 0.3:
		draw_rect(Rect2(0, 0, sw, sh), Color(1, 1, 1, 0.35 * (me.protect_t - (S.protect - 0.3)) / 0.3))
	if not me.alive:
		draw_respawn_card(me)
	elif state == "play":
		draw_bubble(me)
		if peek_t > 0 or (key(KEY_TAB) and not touch_mode):
			draw_peek()
	if me.alive:
		var cw2 := w2s(shoulder(me) + Vector2(cos(me.aim), sin(me.aim)) * 95.0)
		var cc := C_RED if hitmark_t > 0 else Color(1, 1, 1, 0.85)
		for a3 in [0.0, PI / 2, PI, PI * 1.5]:
			var dv := Vector2(cos(a3), sin(a3))
			draw_line(cw2 + dv * 4 * u, cw2 + dv * 9 * u, cc, 2 * u, true)
		var w2 = me.slots[me.cur]
		if w2 != null and zoom_level(me) > 1:
			var s0 := w2s(muzzle_pos(me, w2.type))
			draw_dashed_line(s0, s0 + Vector2(cos(me.aim), sin(me.aim)) * sw, Color(1, 1, 1, 0.45), 1.4 * u, 8 * u)
	if hurt_t > 0 and me.alive:
		vignette(Color(0.85, 0, 0.05, clampf(hurt_t / 0.35, 0, 1) * 0.42), 0.16)
	elif me.alive and me.hp < 30:
		vignette(Color(0.7, 0, 0.05, 0.16 + 0.08 * sin(time_s * 5.0)), 0.14)

func draw_touch() -> void:
	if state != "play":
		return
	var rad := stick_rad()
	var op: float = float(cfg.opacity)
	var aim_lab := "AIM  /  PUSH TO SHOOT" if cfg.fire_mode == "auto" else "AIM"
	var defs := [[stick_l, def_move(), "MOVE  /  UP TO FLY"], [stick_r, def_aim(), aim_lab]]
	for d in defs:
		var active: bool = d[0] != null
		var o: Vector2 = d[0].o if active else d[1]
		var pos: Vector2 = d[0].pos if active else d[1]
		var a := (0.85 if active else 0.4) * op / 0.7
		draw_circle(o, rad, Color(0.04, 0.05, 0.12, 0.25 * a + 0.05))
		draw_arc(o, rad, 0, TAU, 48, Color(1, 1, 1, a * 0.7), 2 * u, true)
		var dv := pos - o
		if dv.length() > rad:
			dv = dv.normalized() * rad
		draw_circle(o + dv, 22 * u * float(cfg.stick_size), Color(1, 1, 1, 0.3 * a + 0.15))
		draw_arc(o + dv, 22 * u * float(cfg.stick_size), 0, TAU, 32, Color(1, 1, 1, a), 1.5 * u, true)
		if not active:
			txt(d[2], o + Vector2(0, rad + 18 * u), 10 * u, Color(1, 1, 1, 0.75), 1, 3 * u)
	var me: Player = players[my_idx]
	for b in buttons():
		var held := btn_held.has(b.n)
		var bg := Color(1, 0.85, 0.29, 0.55) if held else Color(0.04, 0.05, 0.12, 0.45 * op / 0.7)
		if b.n == "FIRE":
			bg = Color(0.95, 0.25, 0.3, 0.75 if held else 0.45 * op / 0.7 + 0.1)
		var br: float = b.r * (0.9 if held else 1.0)
		draw_circle(b.p, br, bg)
		draw_arc(b.p, br, 0, TAU, 36, Color(1, 1, 1, 0.6 * op / 0.7), 1.5 * u, true)
		match b.n:
			"FIRE":
				txt("FIRE", b.p + Vector2(0, 5 * u), 13 * u, C_INK, 1, 3 * u)
			"SMOKE":
				tex_c("smoke_can", b.p + Vector2(0, -3 * u), Vector2(13, 17) * u)
				txt("%d" % me.smokes, b.p + Vector2(b.r * 0.55, b.r * 0.7), 11 * u, C_INK, 1, 3 * u)
			"BOMB":
				tex_c("timebomb", b.p + Vector2(0, -3 * u), Vector2(20, 15) * u)
				txt("%d" % me.bombs, b.p + Vector2(b.r * 0.55, b.r * 0.7), 11 * u, C_INK, 1, 3 * u)
			"GRENADE":
				tex_c("grenade", b.p + Vector2(0, -3 * u), Vector2(16, 19) * u)
				txt("%d" % me.grenades, b.p + Vector2(b.r * 0.55, b.r * 0.7), 11 * u, C_INK, 1, 3 * u)
			"SWAP":
				var o = me.slots[1 - me.cur]
				if o != null:
					gun_icon(o.type, b.p, b.r * 1.5)
				else:
					txt("SWAP", b.p + Vector2(0, 4 * u), 10 * u, C_INK, 1)
			"ZOOM":
				txt("%dX" % zoom_level(me), b.p + Vector2(0, 2 * u), 14 * u, C_CYAN, 1, 3 * u)
				txt("ZOOM", b.p + Vector2(0, b.r * 0.6), 8 * u, C_INK, 1, 2 * u)
			"SIT":
				var w3 = me.slots[me.cur]
				var lab := "SIT"
				if me.posture == "crouch":
					lab = "LIE" if (w3 != null and w3.type == "sniper") else "STAND"
				elif me.posture == "prone":
					lab = "STAND"
				txt(lab, b.p + Vector2(0, 4 * u), 10 * u, C_INK, 1, 2 * u)
			_:
				txt(b.n, b.p + Vector2(0, 4 * u), 9 * u, C_INK, 1, 2 * u)

func panel(w: float, h: float) -> Rect2:
	var r := Rect2(sw / 2 - w / 2, sh / 2 - h / 2, w, h)
	var k := ease_back(ui_t / 0.34)
	var sc := lerpf(0.9, 1.0, k)
	var cpos := r.get_center() + Vector2(0, (1.0 - k) * 16 * u)
	panel_xf = Transform2D(0.0, Vector2(sc, sc), 0.0, cpos - r.get_center() * sc)
	draw_set_transform_matrix(panel_xf)
	ga = ease_out(ui_t / 0.2)
	btn_i = 0
	fbox(r, Color(0.065, 0.085, 0.2, 0.94), 18 * u, Color(1, 1, 1, 0.11), maxf(1.0, 1.5 * u), 26 * u)
	fbox(Rect2(r.position + Vector2(2, 2) * u, Vector2(r.size.x - 4 * u, minf(r.size.y * 0.4, 120 * u))), Color(1, 1, 1, 0.03), 16 * u)
	fbox(Rect2(r.position.x + 26 * u, r.position.y - 2 * u, 72 * u, 4 * u), C_ARC, 2 * u)
	return r

func ui_button(label: String, r: Rect2, action: String, primary := false) -> void:
	ui_btns.append({"r": r, "a": action})
	var i := btn_i
	btn_i += 1
	var k := ease_out((ui_t - 0.08 - i * 0.045) / 0.26)
	var ga0 := ga
	ga *= k
	var rr := r
	rr.position.x -= (1.0 - k) * 26 * u
	var hover: bool = not touch_mode and mouse_used and r.has_point(mouse_pos) and pending_action == ""
	if r == pressed_r and time_s - pressed_at < 0.18:
		rr = rr.grow(-rr.size.y * 0.06)
	elif hover:
		rr.position.y -= 2 * u
	var base: Color = C_ARC if primary else Color(0.2, 0.25, 0.43)
	if primary:
		var gl := 0.18 + 0.12 * sin(time_s * 3.0)
		fbox(rr.grow(3 * u), Color(0, 0, 0, 0), 13 * u, Color(C_ARC, gl), 2 * u)
	fbox(Rect2(rr.position + Vector2(0, 4 * u), rr.size), base.darkened(0.55) if primary else Color(0, 0, 0, 0.45), 11 * u)
	fbox(rr, base.lightened(0.12 if hover else 0.0), 11 * u, Color(1, 1, 1, 0.4 if primary else 0.13), maxf(1.0, u))
	fbox(Rect2(rr.position + Vector2(3, 2) * u, Vector2(rr.size.x - 6 * u, rr.size.y * 0.46)), Color(1, 1, 1, 0.24 if primary else 0.07), 9 * u)
	var fs := 15 * u if rr.size.y > 36 * u else 13 * u
	txh(label, rr.get_center() + Vector2(0, fs * 0.36), fs, Color("#2a1f00") if primary else C_INK, 1)
	ga = ga0

func val_name(row: Array) -> String:
	var vals: Array = row[2]
	var idx := vals.find(cfg[row[0]])
	return row[3][idx] if idx >= 0 else str(cfg[row[0]])

func draw_menu() -> void:
	var w := minf(sw - 32 * u, 640 * u)
	var h := minf(sh - 24 * u, 330 * u)
	var r := panel(w, h)
	var x := r.position.x + 26 * u
	var y := r.position.y
	txt("ARC LIGHT STUDIO  /  BUILD " + VERSION, Vector2(x, y + 30 * u), 11 * u, C_CYAN)
	txt("Sounds: Kenney.nl (CC0) and the Freedoom project (BSD licence)", Vector2(r.end.x - 20 * u, r.end.y - 12 * u), 8 * u, Color(C_MUTED, 0.7), 2)
	var title := "SKY SQUAD"
	var fs := 50 * u
	var xx := x
	for i in title.length():
		var ch := title[i]
		var k := ease_back((ui_t - 0.12 - i * 0.045) / 0.4)
		var ga0 := ga
		ga *= clampf((ui_t - 0.12 - i * 0.045) / 0.15, 0.0, 1.0) if not anim_skip else 1.0
		txh(ch, Vector2(xx, y + 80 * u - (1.0 - k) * 34 * u), fs, C_ARC, 0, 7 * u)
		ga = ga0
		xx += font_h.get_string_size(ch, HORIZONTAL_ALIGNMENT_LEFT, -1, int(fs)).x
	var bw := 230 * u
	var bh := 44 * u
	ui_button("PLAY VS BOTS", Rect2(x, y + 100 * u, bw, bh), "play", true)
	ui_button("PLAY WITH FRIENDS", Rect2(x, y + 152 * u, bw, bh), "lan", true)
	ui_button("LOCKER", Rect2(x, y + 204 * u, bw, bh), "locker")
	var hw := (bw - 8 * u) / 2.0
	ui_button("MATCH", Rect2(x, y + 256 * u, hw, bh), "match")
	ui_button("CONTROLS", Rect2(x + hw + 8 * u, y + 256 * u, hw, bh), "controls")
	var ak := ease_back((ui_t - 0.3) / 0.45)
	var ga2 := ga
	ga *= clampf((ui_t - 0.3) / 0.2, 0.0, 1.0) if not anim_skip else 1.0
	var apos := Vector2(r.end.x - 62 * u, y + 58 * u + sin(time_s * 2.0) * 3 * u)
	draw_avatar(my_look(), apos, 1.15 * u * maxf(0.05, ak), TEAM_COL[0])
	txt(my_name(), Vector2(r.end.x - 62 * u, y + 108 * u), 11 * u, C_ARC, 1, 3 * u)
	ga = ga2
	var rx := x + bw + 30 * u
	var lines := [
		"THIS MATCH",
		("Teams: Blue vs Red" if cfg.mode == "team" else "Free for all") + "  /  %d bots (%s)" % [cfg.bots, cfg.skill],
		"Map: %s  /  %d min  /  event every %d sec" % [MAP_NAMES.get(cfg.map, "Sky Islands"), cfg.minutes, cfg.event_every],
		"Antigravity: %s" % ("on" if (cfg.ev_flip or cfg.zones) else "off"),
		"",
		"HOW TO PLAY",
		"Left thumb: move, push up to fly.",
		"Right thumb: aim" + (", push far to shoot." if cfg.fire_mode == "auto" else ", tap FIRE to shoot."),
		"Walk near a gun and tap its bubble to take it.",
		"Keyboard: A/D W S, mouse, E Q Z G B C F.",
	]
	for i in lines.size():
		var head: bool = lines[i] == "THIS MATCH" or lines[i] == "HOW TO PLAY"
		var k2 := ease_out((ui_t - 0.2 - i * 0.03) / 0.3)
		var ga1 := ga
		ga *= k2
		txt(lines[i], Vector2(rx + (1.0 - k2) * 14 * u, y + 118 * u + i * 19 * u), (10 if head else 12) * u, C_CYAN if head else C_MUTED)
		ga = ga1

func draw_cfg(title: String, rows: Array, back := "back") -> void:
	var w := minf(sw - 24 * u, 700 * u)
	var h := minf(sh - 20 * u, 360 * u)
	var r := panel(w, h)
	var x := r.position.x + 22 * u
	var y := r.position.y
	txh(title, Vector2(x, y + 38 * u), 24 * u, C_ARC, 0, 4 * u)
	txt("Tap a value to change it. Saved on this device.", Vector2(r.end.x - 22 * u, y + 34 * u), 10 * u, C_MUTED, 2)
	var per_col := ceili(rows.size() / 2.0)
	var colw := (w - 44 * u - 20 * u) / 2.0
	var rh := minf(34 * u, (h - 130 * u) / per_col)
	for i in rows.size():
		var row: Array = rows[i]
		var cx := x + (i / per_col) * (colw + 20 * u)
		var cy := y + 58 * u + (i % per_col) * rh
		txt(row[1], Vector2(cx, cy + rh * 0.62), 12 * u, C_INK)
		var pr := Rect2(cx + colw * 0.5, cy + rh * 0.12, colw * 0.5, rh * 0.76)
		ui_btns.append({"r": pr, "a": "row:" + row[0]})
		var on_flag: bool = row[0] in ["ev_flip", "zones"] and cfg[row[0]] == true
		if pr == pressed_r and time_s - pressed_at < 0.18:
			pr = pr.grow(-2 * u)
		fbox(pr, Color(0.35, 0.18, 0.5, 0.95) if on_flag else Color(0.17, 0.21, 0.38, 0.95), 8 * u, Color(1, 1, 1, 0.12), maxf(1.0, u))
		txh(val_name(row), pr.get_center() + Vector2(0, 5 * u), 12 * u, C_ARC, 1)
	ui_button("BACK", Rect2(r.position.x + w / 2 - 100 * u, r.end.y - 58 * u, 200 * u, 42 * u), back, true)

func draw_pause() -> void:
	draw_rect(Rect2(0, 0, sw, sh), Color(0.02, 0.03, 0.1, 0.6 * ease_out(ui_t / 0.2)))
	var r := panel(minf(sw - 32 * u, 340 * u), minf(sh - 24 * u, 270 * u))
	txh("PAUSED", Vector2(r.get_center().x, r.position.y + 44 * u), 26 * u, C_ARC, 1, 4 * u)
	var bx := r.get_center().x - 110 * u
	if net_role != "":
		txt("The match keeps going for your friends.", Vector2(r.get_center().x, r.position.y + 64 * u), 10 * u, C_MUTED, 1)
		ui_button("RESUME", Rect2(bx, r.position.y + 80 * u, 220 * u, 44 * u), "resume", true)
		ui_button("LEAVE MATCH", Rect2(bx, r.position.y + 140 * u, 220 * u, 44 * u), "leave")
		return
	ui_button("RESUME", Rect2(bx, r.position.y + 66 * u, 220 * u, 44 * u), "resume", true)
	ui_button("RESTART", Rect2(bx, r.position.y + 120 * u, 220 * u, 44 * u), "restart")
	ui_button("MAIN MENU", Rect2(bx, r.position.y + 174 * u, 220 * u, 44 * u), "menu")

func draw_over() -> void:
	draw_rect(Rect2(0, 0, sw, sh), Color(0.02, 0.03, 0.1, 0.62 * ease_out(ui_t / 0.3)))
	var rk := ranked()
	var team: bool = cfg.mode == "team"
	var rowh := minf(25 * u, (minf(sh - 24 * u, 380 * u) - 190 * u) / maxf(1.0, rk.size()))
	var w := minf(sw - 32 * u, 560 * u)
	var h := minf(sh - 24 * u, 190 * u + rk.size() * rowh + (24 * u if team else 0.0))
	var r := panel(w, h)
	var x := r.position.x + 24 * u
	var y := r.position.y
	txt("MATCH OVER", Vector2(x, y + 30 * u), 11 * u, C_CYAN)
	var title := "You win!" if (rk[0] == players[my_idx] and rk[0].kills > 0) else "%s wins" % rk[0].pname
	if team:
		var ts := team_scores()
		title = "Draw" if ts[0] == ts[1] else ("Blue team wins" if ts[0] > ts[1] else "Red team wins")
	var tk := ease_back((ui_t - 0.15) / 0.4)
	var ga0 := ga
	ga *= clampf((ui_t - 0.15) / 0.15, 0.0, 1.0) if not anim_skip else 1.0
	var tsz := 28 * u * lerpf(1.4, 1.0, tk)
	if not team and rk[0].kills > 0:
		draw_crown(Vector2(x + 12 * u, y + 52 * u), 11 * u)
		txh(title, Vector2(x + 32 * u, y + 64 * u), tsz, C_ARC, 0, 5 * u)
	else:
		txh(title, Vector2(x, y + 64 * u), tsz, C_ARC, 0, 5 * u)
	ga = ga0
	var ry := y + 104 * u
	if team:
		team_bar(x, y + 96 * u, w - 48 * u)
		ry += 24 * u
	draw_rank_rows(r.position.x + 14 * u, ry, w - 28 * u, rowh, rk, ui_t, awards(rk))
	var lk := ease_out((ui_t - 0.9) / 0.4)
	var ga1 := ga
	ga *= lk
	txh(end_line(rk), Vector2(r.get_center().x, r.end.y - 72 * u), 13 * u, C_INK, 1)
	ga = ga1
	if net_role == "client" and online and is_owner():
		ui_button("PLAY AGAIN", Rect2(r.get_center().x - 210 * u, r.end.y - 58 * u, 200 * u, 44 * u), "again", true)
		ui_button("LEAVE", Rect2(r.get_center().x + 10 * u, r.end.y - 58 * u, 200 * u, 44 * u), "leave")
		return
	if net_role == "client":
		txt("Waiting for the %s to start the next match..." % ("room leader" if online else "host"), Vector2(r.position.x + 24 * u, r.end.y - 30 * u), 11 * u, C_MUTED)
		ui_button("LEAVE", Rect2(r.end.x - 24 * u - 110 * u, r.end.y - 56 * u, 110 * u, 40 * u), "leave")
		return
	ui_button("PLAY AGAIN", Rect2(r.get_center().x - 210 * u, r.end.y - 58 * u, 200 * u, 44 * u), "again", true)
	if net_role == "host":
		ui_button("LOBBY", Rect2(r.get_center().x + 10 * u, r.end.y - 58 * u, 200 * u, 44 * u), "to_lobby")
	else:
		ui_button("MENU", Rect2(r.get_center().x + 10 * u, r.end.y - 58 * u, 200 * u, 44 * u), "menu")

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
	return {"mx": 0.0, "fly": false, "shoot": false, "swap": false, "grenade": false, "melee": false, "reload": false, "aim": 0.0, "down": false, "pick": "", "zoom": false, "bomb": false, "smoke": false}

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

func lobby_looks() -> Array:
	if net_role == "host":
		var out := []
		for lp in lan_players:
			out.append(str(lp.get("look", AV_DEF)))
		return out
	return lobby_info.get("lk", [])

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
	pe.host.compress(1)  # range coder
	multiplayer.multiplayer_peer = pe
	net_role = "host"
	my_idx = 0
	lan_players = [{"peer": 1, "name": my_name(), "look": look_str(my_look()), "uid": str(cfg.uid)}]
	disc = PacketPeerUDP.new()
	disc.set_broadcast_enabled(true)
	disc.bind(DISC_PORT)
	state = "lobby"

func join_game(ip: String, port := NET_PORT) -> void:
	net_close()
	ip = ip.strip_edges()
	if not ip.is_valid_ip_address():
		toast("That address doesn't look right. Example: 192.168.43.1")
		return
	var pe = ClassDB.instantiate("ENetMultiplayerPeer")
	if pe == null:
		toast("LAN play works in the Android app.")
		return
	var err: int = pe.create_client(ip, port)
	if err != OK:
		toast("Could not join %s" % ip)
		return
	pe.host.compress(1)  # range coder
	var sp = pe.get_peer(1)
	if sp != null:
		sp.set_timeout(32, 4000, 9000)
	multiplayer.multiplayer_peer = pe
	net_role = "client"
	join_ip = ip
	lobby_info = {}
	connect_t = 9.0 if online else 7.0
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
			p.dropped = true
			p.bot = true
			p.style = "balanced"
			p.st = make_style("balanced")
			p.inp = blank_inp()
			p.prev = p.inp.duplicate()
			feed.push_front({"k": "", "kc": C_INK, "v": "%s left. A bot took over." % p.pname, "vc": C_ARC, "gun": "", "head": false, "t": 4.0, "t0": 4.0, "note": ""})
	if gone:
		send_lobby()

func _on_connected() -> void:
	print("NET connected to server")
	recon_left = 0
	rpc_id(1, "c_hello", my_name(), VERSION, look_str(my_look()), str(cfg.uid))
	state = "lobby"

func _on_conn_failed() -> void:
	print("NET connection failed")
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
	toast("Could not join. Are you connected to the host's hotspot?")

func _on_server_gone() -> void:
	print("NET server went away")
	if online and room_code != "":
		start_reconnect()
		return
	net_close()
	state = "lan"
	toast("The host closed the game.")
	if lantest_join != "":
		print("CLIENT: host went away")
		get_tree().quit()

# ---------- messages ----------
@rpc("any_peer", "call_remote", "reliable")
func c_hello(nm, ver, lk = "", cuid = "") -> void:
	if net_role != "host":
		return
	var id := multiplayer.get_remote_sender_id()
	if str(ver) != VERSION:
		rpc_id(id, "s_reject", "Different game version. Install the same Sky Squad on every phone.")
		return
	if dedicated and str(cuid) != "":
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
	lan_players.append({"peer": id, "name": pick, "look": look_str(parse_look(lk)), "uid": str(cuid)})
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
	var info := {"room": room_code, "owner": str(lan_players[0].get("uid", "")) if (dedicated and not lan_players.is_empty()) else "", "pl": lobby_names(), "lk": lobby_looks(), "sd": lobby_sides(), "ud": lobby_uids(), "mode": cfg.mode, "map": cfg.map, "bots": clampi(int(cfg.lan_bots), 0, 6 - lan_players.size()), "skill": cfg.skill, "min": cfg.minutes, "go": go}
	rpc("s_lobby", info)

@rpc("authority", "call_remote", "reliable")
func s_lobby(info) -> void:
	if net_role != "client":
		return
	lobby_info = info
	if online and is_owner() and not cfg_sent:
		cfg_sent = true
		rpc_id(1, "c_cfg", my_settings())
	if state == "connecting" or (info.get("go", false) and (state == "over" or state == "paused")):
		state = "lobby"

func start_lan_match() -> void:
	if net_role != "host":
		return
	if not dedicated and not lan_players.is_empty():
		lan_players[0].name = my_name()
		lan_players[0].look = look_str(my_look())
	reset_match()
	if lantest_host:
		players[0].bot = true
		var lks := []
		for p in players:
			lks.append(p.pname + "=" + look_str(p.look) + " side=" + str(p.side))
		print("LOOKS ", lks)
	state = "play"
	snap_t = 0.0
	for i in players.size():
		var p: Player = players[i]
		if p.remote:
			rpc_id(p.peer_id, "s_start", start_info(i))

func start_info(idx: int) -> Dictionary:
	var pl := []
	for p in players:
		pl.append([p.pname, p.team, p.color, p.side, p.bot, look_str(plook(p))])
	return {"idx": idx, "tiles": tiles, "pl": pl, "mode": cfg.mode, "zones": cfg.zones, "mt": match_time, "map": map_id}

@rpc("authority", "call_remote", "reliable")
func s_start(info) -> void:
	if net_role != "client":
		return
	if stash.is_empty():
		stash = {"mode": cfg.mode, "zones": cfg.zones}
	cfg.mode = info.mode
	cfg.zones = info.zones
	map_id = str(info.get("map", "sky"))
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
	for arr in [bullets, grenades_list, parts, pickups, blocks, corpses, feed, tracers, clouds]:
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
		p.look = parse_look(d[5]) if d.size() > 5 else parse_look(AV_DEF)
		p.slots = [full_slot("uzi"), full_slot("magnum")]
		players.append(p)
	my_idx = int(info.idx)
	cam = Vector2.ZERO
	in_t = 0.0
	snaps_got = 0
	pending_start = true

const PK_TYPES := ["gun", "drop", "health", "grenade", "bomb", "smoke"]
const PF_N := 33

func slot_str(w) -> String:
	if w == null:
		return ""
	return "%s:%d:%d:%d:%d" % [w.type, w.mag, w.spare, w.zi, 1 if w.get("dual", false) else 0]

func slot_from(s2: String):
	if s2 == "":
		return null
	var b := s2.split(":")
	return {"type": b[0], "mag": int(b[1]), "spare": int(b[2]), "zi": int(b[3]), "dual": b[4] == "1"}

func build_snap() -> Dictionary:
	var pf := PackedFloat32Array()
	var ps := PackedStringArray()
	for p in players:
		var fl := (1 if p.alive else 0) | (2 if p.jet_on else 0) | (4 if p.on_ground else 0) | (8 if p.in_water else 0)
		var lh := players.find(p.last_hit_by) if p.last_hit_by != null else -1
		pf.append_array([p.x, p.y, p.vx, p.vy, p.aim, p.hp, p.fuel, fl, p.cur, p.grenades, p.bombs,
			maxf(p.stun_t, 0.0), maxf(p.net_t, 0.0), maxf(p.protect_t, 0.0), maxf(p.reload_t, 0.0), p.reload_total,
			p.kills, p.deaths, p.respawn_t, maxf(p.say_t, 0.0), maxf(p.switch_t, 0.0), maxf(p.melee_anim, 0.0), maxf(p.flash, 0.0), lh,
			p.hs, p.best, p.mk, p.bk, p.lstreak, p.spin, maxf(p.burn_t, 0.0), p.smokes, p.ack])
		ps.append("%s|%s|%s|%s|%s|%s|%d" % [p.posture, slot_str(p.slots[0]), slot_str(p.slots[1]), p.say if p.say_t > 0 else "", p.last_gun, p.last_cause, 1 if p.last_head else 0])
	var b := PackedFloat32Array()
	for x in bullets:
		b.append_array([x.x, x.y, x.vx, x.vy, 1.0 if x.rocket else (2.0 if x.net else (3.0 if x.flame else 0.0)), x.life, x.max_life])
	var g := PackedFloat32Array()
	for x in grenades_list:
		g.append_array([x.x, x.y, x.vx, x.vy, x.rot, x.fuse, {"bomb": 1.0, "smoke": 2.0}.get(x.kind, 0.0), 1.0 if x.stuck else 0.0])
	var guns: Array = WD.keys()
	var k := PackedFloat32Array()
	for x in pickups:
		k.append_array([x.x, x.y, PK_TYPES.find(x.type), guns.find(x.gun)])
	var bl := PackedFloat32Array()
	for x in blocks:
		bl.append_array([x.c, x.y, x.vy])
	var e := []
	if ev != null:
		e = [ev.name, ev.phase, ev.t, ev.dur, ev.spawned, ev.cols, ev.tiles]
	var cl := PackedFloat32Array()
	for x in clouds:
		cl.append_array([x.x, x.y, x.t])
	var d := {"t": t, "wy": water_y, "g": g_dir, "cl": cl, "pf": pf, "ps": ps, "b": b, "gr": g, "bl": bl, "ev": e, "fx": net_fx}
	# pickups only go out for a few updates after they change (and now and then, in case one was lost)
	var ksig := hash(k)
	pk_every -= 1
	if ksig != pk_sig or pk_every <= 0:
		if ksig != pk_sig:
			pk_send = 3
		pk_sig = ksig
		pk_every = 40
		pk_send = maxi(pk_send, 1)
	if pk_send > 0:
		pk_send -= 1
		d["k"] = k
	# the kill list goes out once, safely, when it changes
	var sig := "%d" % feed.size()
	if not feed.is_empty():
		sig += "|%s|%s|%s" % [feed[0].k, feed[0].v, feed[0].note]
	if sig != feed_sig:
		feed_sig = sig
		if net_role == "host":
			rpc("s_feed", feed)
	return d

func net_host_tick(dt: float) -> void:
	snap_t += dt
	if snap_t < SNAP_DT:
		return
	snap_t = minf(snap_t - SNAP_DT, SNAP_DT)
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
	var sn := build_snap()
	if dbg_size:
		var tot := var_to_bytes(sn).size()
		dbg_sizes.append(tot)
		if tot > 1300:
			var parts := {}
			for kk in sn.keys():
				parts[kk] = var_to_bytes(sn[kk]).size()
			print("big snap ", tot, " ", parts)
		if dbg_sizes.size() % 200 == 0:
			var ss := dbg_sizes.duplicate()
			ss.sort()
			print("snap sizes: median=%d p90=%d max=%d" % [ss[ss.size() / 2], ss[int(ss.size() * 0.9)], ss[-1]])
	rpc("s_snap", sn)
	net_fx = []
	snaps_sent += 1
	if snaps_sent % 20 == 0 and multiplayer.multiplayer_peer != null and multiplayer.multiplayer_peer.has_method("get_peer"):
		for p in players:
			if p.remote:
				var sp = multiplayer.multiplayer_peer.get_peer(p.peer_id)
				if sp != null:
					p.lat = clampf(sp.get_statistic(3) / 2000.0 + INTERP + 0.02, 0.0, 0.35)

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
	if lag_ms > 0:
		lag_in.append([time_s + lag_ms / 2000.0, d])
		return
	apply_snap(d)

func apply_snap(d) -> void:
	if net_role != "client" or not (pending_start or state == "play" or state == "paused"):
		return
	snap_wait = 0.0
	var pf: PackedFloat32Array = d.pf
	var ps: PackedStringArray = d.ps
	if ps.size() != players.size() or pf.size() != ps.size() * PF_N:
		return
	snaps_got += 1
	var st: float = d.t
	if absf(st - snap_clock) > 0.3 or snaps_got == 1:
		snap_clock = st
	else:
		snap_clock = lerpf(snap_clock, st, 0.1)
	t = d.t
	water_y = d.wy
	g_dir = d.g
	for i in ps.size():
		var o := i * PF_N
		var bits := ps[i].split("|")
		var p: Player = players[i]
		var was_alive := p.alive
		var mine := i == my_idx and predicting()
		p.nx = pf[o]
		p.ny = pf[o + 1]
		p.svx = pf[o + 2]
		p.svy = pf[o + 3]
		if not mine:
			p.vx = p.svx
			p.vy = p.svy
		p.naim = pf[o + 4]
		p.hp = pf[o + 5]
		p.fuel = pf[o + 6]
		p.pfuel = p.fuel
		var fl := int(pf[o + 7])
		p.alive = (fl & 1) != 0
		if not mine:
			p.jet_on = (fl & 2) != 0
			p.on_ground = (fl & 4) != 0
		p.in_water = (fl & 8) != 0
		p.cur = int(pf[o + 8])
		p.grenades = int(pf[o + 9])
		p.bombs = int(pf[o + 10])
		p.stun_t = pf[o + 11]
		p.net_t = pf[o + 12]
		p.protect_t = pf[o + 13]
		p.reload_t = pf[o + 14]
		p.reload_total = pf[o + 15]
		p.kills = int(pf[o + 16])
		p.deaths = int(pf[o + 17])
		p.respawn_t = pf[o + 18]
		p.say_t = pf[o + 19]
		if pf[o + 20] > p.switch_t + 0.04:
			p.switch_t = pf[o + 20]
		if pf[o + 21] > p.melee_anim + 0.04:
			p.melee_anim = pf[o + 21]
		if pf[o + 22] > p.flash + 0.03:
			p.flash = pf[o + 22]
		var lh := int(pf[o + 23])
		p.last_hit_by = players[lh] if lh >= 0 and lh < players.size() else null
		var post: String = bits[0]
		if post != p.posture and POSTURE.has(post):
			p.posture = post
			var sz: Vector2 = POSTURE[post]
			p.w = sz.x
			p.h = sz.y
		p.slots = [slot_from(bits[1]), slot_from(bits[2])]
		p.say = bits[3] if bits.size() > 3 else ""
		if bits.size() > 6:
			p.last_gun = bits[4]
			p.last_cause = bits[5]
			p.last_head = bits[6] == "1"
		p.hs = int(pf[o + 24])
		p.best = int(pf[o + 25])
		p.mk = int(pf[o + 26])
		p.bk = int(pf[o + 27])
		p.lstreak = int(pf[o + 28])
		p.spin = pf[o + 29]
		p.burn_t = pf[o + 30]
		p.smokes = int(pf[o + 31])
		if not mine:
			if p.alive and not was_alive:
				p.sbuf.clear()
			p.sbuf.append([st, p.nx, p.ny, p.svx, p.svy, p.naim])
			while p.sbuf.size() > 8:
				p.sbuf.pop_front()
		if mine and p.alive and was_alive and snaps_got > 1:
			reconcile_me(p, int(pf[o + 32]), fl)
		elif mine:
			pred_hist.clear()
			pred_off = Vector2.ZERO
		p.snap_age = 0.0
		if p.alive and not was_alive:
			p.born_t = time_s
		if (p.alive and not was_alive) or snaps_got == 1 or (not mine and Vector2(p.x - p.nx, p.y - p.ny).length() > 160):
			p.x = p.nx
			p.y = p.ny
			p.vx = p.svx
			p.vy = p.svy
			if i == my_idx and snaps_got == 1:
				p.aim = p.naim
				last_touch_aim = p.naim
	bullets.clear()
	var bb: PackedFloat32Array = d.b
	for j in range(0, bb.size(), 7):
		var b := Bullet.new()
		b.x = bb[j]
		b.y = bb[j + 1]
		b.vx = bb[j + 2]
		b.vy = bb[j + 3]
		b.rocket = bb[j + 4] == 1.0
		b.net = bb[j + 4] == 2.0
		b.flame = bb[j + 4] == 3.0
		b.life = bb[j + 5]
		b.max_life = bb[j + 6]
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
		g.kind = "bomb" if gg[j + 6] == 1.0 else ("smoke" if gg[j + 6] == 2.0 else "frag")
		g.stuck = gg[j + 7] == 1.0
		grenades_list.append(g)
	if d.has("k"):
		pickups.clear()
		var guns: Array = WD.keys()
		var kk: PackedFloat32Array = d.k
		for j in range(0, kk.size(), 4):
			var gi := int(kk[j + 3])
			pickups.append(make_pickup(PK_TYPES[int(kk[j + 2])], kk[j], kk[j + 1], guns[gi] if gi >= 0 else ""))
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
	if d.has("feed"):
		feed = d.feed
	clouds.clear()
	var cla: PackedFloat32Array = d.get("cl", PackedFloat32Array())
	for j in range(0, cla.size(), 3):
		clouds.append({"x": cla[j], "y": cla[j + 1], "t": cla[j + 2], "owner": null})
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
			explode_fx(e[1], e[2], e[3], e[4] if e.size() > 4 else "explosion")
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
			cp.look = plook(players[int(e[8])]) if (e.size() > 8 and int(e[8]) >= 0 and int(e[8]) < players.size()) else default_look
			corpses.append(cp)
		"m":
			if int(e[1]) == my_idx:
				apply_me_fx(e[2], e[3])

func send_end() -> void:
	var info := {"k": [], "d": [], "hs": [], "best": [], "mk": [], "bk": []}
	for p in players:
		info.k.append(p.kills)
		info.d.append(p.deaths)
		info.hs.append(p.hs)
		info.best.append(p.best)
		info.mk.append(p.mk)
		info.bk.append(p.bk)
	rpc("s_end", info)

@rpc("authority", "call_remote", "reliable")
func s_end(info) -> void:
	if net_role != "client":
		return
	for i in mini(players.size(), info.k.size()):
		players[i].kills = info.k[i]
		players[i].deaths = info.d[i]
		players[i].hs = info.hs[i]
		players[i].best = info.best[i]
		players[i].mk = info.mk[i]
		players[i].bk = info.bk[i]
	state = "over"
	jet_player.stop()
	client_jet = false
	if lantest_join != "" and lt_done == 0.0:
		lt_done = time_s
		var me: Player = players[my_idx]
		print("CLIENT snaps=%d tile_updates=%d players=%d me=%s idx=%d kills=%d deaths=%d moved=%d" % [snaps_got, tiles_got, players.size(), me.pname, my_idx, me.kills, me.deaths, int(lt_moved)])
		print("CLIENT fx: ", fx_count)
		print("CLIENT others jitter=%.2fpx per frame" % (jit_sum / maxf(1.0, jit_n)))
		print("CLIENT prediction: avg_error=%.1fpx hard_corrections=%d rtt=%dms" % [pred_err / maxf(1.0, pred_n), pred_snaps, int(rtt_s * 1000)])

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
			inp.smoke = a.size() > 12 and bool(a[12])
			for kk in EDGE_KEYS:
				if inp.get(kk, false):
					p.press_hold[kk] = true
			if a.size() > 13:
				p.ack = maxi(p.ack, int(a[13]))
			inputs_got += 1
			return

# the joining phone: read controls, send them, and smoothly show what the host sent
func update_client(dt: float) -> void:
	if pending_start or players.is_empty() or my_idx >= players.size():
		return
	if online and state == "play":
		snap_wait += dt
		if snap_wait > 5.0:
			print("NET no updates for 5 seconds")
			start_reconnect()
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
	for kk in EDGE_KEYS:
		if me.inp.get(kk, false):
			in_latch[kk] = true
	snap_clock += dt
	in_t += dt
	if in_t >= 1.0 / 30.0:
		in_t = minf(in_t - 1.0 / 30.0, 0.03)
		var i2: Dictionary = me.inp.duplicate()
		for kk in in_latch.keys():
			i2[kk] = true
		in_latch.clear()
		in_seq += 1
		var pkt := [i2.mx, i2.fly, i2.shoot, i2.swap, i2.grenade, i2.melee, i2.reload, me.aim, i2.down, i2.pick, i2.zoom, i2.bomb, i2.smoke, in_seq]
		if lag_ms > 0:
			lag_out.append([time_s + lag_ms / 2000.0, pkt])
		else:
			rpc_id(1, "c_input", pkt)
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
			p.x = p.nx
			p.y = p.ny
			continue
		if i == my_idx and predicting():
			predict_me(p, dt)
		elif not p.sbuf.is_empty() and not no_glide:
			glide(p)
		else:
			var age := minf(p.snap_age, 0.12)
			var k := ease_k(18.0, dt)
			p.x += (p.nx + p.vx * age - p.x) * k
			p.y += (p.ny + p.vy * age - p.y) * k
		if i != my_idx and p.alive and dt > 0:
			var mv := (Vector2(p.x, p.y) - p.jit_last) / dt
			if p.jit_ok and mv.length() < 1500.0 and dt < 0.05:
				jit_sum += (mv - p.jit_prev).length() * dt
				jit_n += 1
			if glide_log and i == (my_idx + 1) % players.size():
				print("GL %.4f %.4f %.1f %.1f %d %.4f %.1f" % [time_s, snap_clock, p.x, p.y, p.sbuf.size(), (float(p.sbuf[-1][0]) if not p.sbuf.is_empty() else 0.0), mv.length()])
			p.jit_prev = mv
			p.jit_ok = true
			p.jit_last = Vector2(p.x, p.y)
		elif i != my_idx:
			p.jit_ok = false
		if i != my_idx and (p.sbuf.is_empty() or no_glide):
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
	for cl in clouds:
		cl.t -= dt
		cloud_fx(cl, dt)
	for b in bullets:
		if b.flame:
			b.life -= dt
			b.vx *= pow(0.2, dt)
			b.vy = b.vy * pow(0.2, dt) - 70.0 * gsign() * dt
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
	for f in feed:
		f.t -= dt
	feed = feed.filter(func(f): return f.t > 0)
	shake = maxf(0.0, shake - dt * 30)
	big_t -= dt
	hurt_t -= dt
	hitmark_t -= dt

# discovery: the host answers "SKYSQ?" with its name; joiners keep asking around
func net_poll(dt: float) -> void:
	if OS.has_feature("web"):
		return
	mm_poll(dt)
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
	txh("PLAY WITH FRIENDS", Vector2(x, y + 42 * u), 26 * u, C_ARC, 0, 4 * u)
	txt("From anywhere online, or phones close together.", Vector2(x, y + 64 * u), 11 * u, C_MUTED)
	var bw := 230 * u
	var bh := 40 * u
	ui_button("ONLINE ROOMS", Rect2(x, y + 80 * u, bw, bh), "online", true)
	ui_button("HOST (HOTSPOT)", Rect2(x, y + 128 * u, bw, bh), "host")
	ui_button("JOIN (HOTSPOT)", Rect2(x, y + 176 * u, bw, bh), "join")
	ui_button("NAME & LOOK: " + my_name(), Rect2(x, y + 224 * u, bw, bh), "name")
	ui_button("BACK", Rect2(x, y + 272 * u, bw, bh), "back")
	var rx := x + bw + 28 * u
	var lines := [
		"ONLINE ROOMS",
		"Play from anywhere on mobile data or Wi-Fi.",
		"One friend makes a room, others type its code.",
		"",
		"HOTSPOT",
		"1. One phone turns on its Wi-Fi hotspot",
		"    and taps HOST (HOTSPOT).",
		"2. Friends join that hotspot, then tap",
		"    JOIN (HOTSPOT). Same home Wi-Fi works too.",
	]
	for i in lines.size():
		var head: bool = lines[i] == "ONLINE ROOMS" or lines[i] == "HOTSPOT"
		txt(lines[i], Vector2(rx, y + 96 * u + i * 19 * u), (10 if head else 12) * u, C_CYAN if head else C_MUTED)

func draw_join() -> void:
	var w := minf(sw - 32 * u, 600 * u)
	var h := minf(sh - 24 * u, 330 * u)
	var r := panel(w, h)
	var x := r.position.x + 26 * u
	var y := r.position.y
	txh("JOIN A GAME", Vector2(x, y + 42 * u), 26 * u, C_ARC, 0, 4 * u)
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
	txh("TYPE HOST ADDRESS", Vector2(x, y + 40 * u), 22 * u, C_ARC, 0, 4 * u)
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
	if online or mm_mode != "":
		txt(conn_label + dots, Vector2(r.get_center().x, r.position.y + 70 * u), 18 * u, C_INK, 1)
		if recon_left > 0:
			txt("Your bot keeps playing until you are back.", Vector2(r.get_center().x, r.position.y + 96 * u), 11 * u, C_MUTED, 1)
		ui_button("CANCEL", Rect2(r.get_center().x - 90 * u, r.end.y - 66 * u, 180 * u, 44 * u), "cancel")
		return
	txt("Joining " + join_ip + dots, Vector2(r.get_center().x, r.position.y + 70 * u), 18 * u, C_INK, 1)
	ui_button("CANCEL", Rect2(r.get_center().x - 90 * u, r.end.y - 66 * u, 180 * u, 44 * u), "cancel")

func draw_lobby() -> void:
	var w := minf(sw - 32 * u, 660 * u)
	var h := minf(sh - 24 * u, 340 * u)
	var r := panel(w, h)
	var x := r.position.x + 26 * u
	var y := r.position.y
	var host := net_role == "host"
	if online:
		if str(lobby_info.get("room", "")) != "":
			room_code = str(lobby_info.room)
		txh("ROOM  " + room_code, Vector2(x, y + 42 * u), 26 * u, C_ARC, 0, 4 * u)
		var tw2 := font_h.get_string_size("ROOM  " + room_code, HORIZONTAL_ALIGNMENT_LEFT, -1, int(26 * u)).x
		var shr := flat_btn(Rect2(x + tw2 + 16 * u, y + 18 * u, 96 * u, 32 * u), "o_share")
		fbox(shr, Color("#25d366"), 8 * u, Color(1, 1, 1, 0.2), maxf(1.0, u))
		txh("SHARE", shr.get_center() + Vector2(0, 5 * u), 12 * u, Color("#06351a"), 1)
		txt("Tell friends this code. They tap PLAY WITH FRIENDS > ONLINE ROOMS > JOIN ROOM.", Vector2(x, r.end.y - 18 * u), 10 * u, C_CYAN)
	else:
		txh("LOBBY", Vector2(x, y + 42 * u), 26 * u, C_ARC, 0, 4 * u)
		txt("You are hosting" if host else "Joined " + join_ip, Vector2(x + 110 * u, y + 40 * u), 12 * u, C_CYAN)
	var names := lobby_names()
	var lmode: String = cfg.mode if host else str(lobby_info.get("mode", "ffa"))
	if lmode == "team":
		draw_team_columns(x, y, names, host)
	else:
		txt("PLAYERS", Vector2(x, y + 74 * u), 10 * u, C_CYAN)
	for i in (names.size() if lmode != "team" else 0):
		var yy := y + 96 * u + i * 22 * u
		var lks := lobby_looks()
		head_icon(parse_look(lks[i]) if i < lks.size() else default_look, Vector2(x + 6 * u, yy - 5 * u), 0.62 * u, TEAM_COL[i % TEAM_COL.size()])
		var tag := ("  (leader)" if online else "  (host)") if i == 0 else ""
		txt(str(names[i]) + tag, Vector2(x + 20 * u, yy), 15 * u, C_ARC if (host and i == 0) else C_INK)
	var nb: int = clampi(int(cfg.lan_bots), 0, 6 - names.size()) if host else int(lobby_info.get("bots", 0))
	if nb > 0 and lmode != "team":
		txt("+ %d bot%s" % [nb, "s" if nb > 1 else ""], Vector2(x + 20 * u, y + 96 * u + names.size() * 22 * u), 13 * u, C_MUTED)
	var rx := x + 250 * u
	var mode: String = cfg.mode if host else str(lobby_info.get("mode", "ffa"))
	var mins: int = int(cfg.minutes) if host else int(lobby_info.get("min", 5))
	txt("MATCH", Vector2(rx, y + 74 * u), 10 * u, C_CYAN)
	var mp: String = MAP_NAMES.get(cfg.map if host else str(lobby_info.get("map", "sky")), "Sky Islands")
	txt(mp + "  /  " + ("Teams" if mode == "team" else "Free for all") + "  /  %d min" % mins, Vector2(rx, y + 96 * u), 13 * u, C_INK)
	if host:
		var ips := lan_ips()
		txt("Friends: join the hotspot, tap JOIN (HOTSPOT).", Vector2(rx, y + 124 * u), 11 * u, C_MUTED)
		txt("Or type this address:", Vector2(rx, y + 142 * u), 11 * u, C_MUTED)
		txt(", ".join(PackedStringArray(ips.slice(0, 2))) if not ips.is_empty() else "(turn on hotspot or Wi-Fi)", Vector2(rx, y + 166 * u), 18 * u, C_ARC, 0, 3 * u)
		var bw := (r.end.x - 26 * u - rx - 10 * u) / 2.0
		ui_button("START", Rect2(rx, y + 190 * u, bw * 2 + 10 * u, 48 * u), "start", true)
		lobby_row(rx, y + 246 * u, bw * 2 + 10 * u, lmode == "team")
	elif online and is_owner():
		txt("You are the room leader.", Vector2(rx, y + 124 * u), 11 * u, C_MUTED)
		txt("Start when everyone is in. Bots fill empty places.", Vector2(rx, y + 142 * u), 11 * u, C_MUTED)
		var bw2 := (r.end.x - 26 * u - rx - 10 * u) / 2.0
		ui_button("START", Rect2(rx, y + 190 * u, bw2 * 2 + 10 * u, 48 * u), "o_start", true)
		lobby_row(rx, y + 246 * u, bw2 * 2 + 10 * u, lmode == "team")
	else:
		var dots := ".".repeat(int(time_s * 2.0) % 4)
		var lead: String = str(names[0]) if (online and not names.is_empty()) else "the host"
		txt("Waiting for %s to start" % lead + dots, Vector2(rx, y + 140 * u), 14 * u, C_INK)
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
				if lt_wait > 3.0 + lt_hold:
					start_lan_match()
		elif state == "over" and lt_done == 0.0:
			lt_done = time_s
			print("HOST snaps_sent=%d inputs_got=%d" % [snaps_sent, inputs_got])
			for p in players:
				print("  %s bot=%s remote=%s kills=%d deaths=%d" % [p.pname, p.bot, p.remote, p.kills, p.deaths])
		if lt_done > 0 and time_s - lt_done > 4.0:
			get_tree().quit()
	if test_pick >= 0 and net_role == "client" and state == "lobby" and not lobby_info.is_empty():
		print("CLIENT picks team ", test_pick)
		pick_team(test_pick)
		test_pick = -1
	if lantest_join == "auto" and state == "lan_join":
		var fl := found_list()
		if not fl.is_empty():
			lt_wait += dt
			if lt_wait > 3.5:
				print("CLIENT found: ", fl)
				do_action("conn:" + str(fl[0].ip))
	if lantest_join == "online" and state == "lobby" and is_owner() and (lobby_names().size() >= 2 or time_s > 30.0):
		lt_wait += dt
		if lt_wait > 3.0:
			lt_wait = -999.0
			print("CLIENT owner starts the match, players=", lobby_names())
			do_action("o_start")
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
		"now":
			ok = true
		"ui":
			ok = ui_t > 1.3
		"room":
			ok = state == "lobby" and ui_t > 1.5
		_:
			ok = state == "play" and t >= float(trig)
	if not ok:
		shot_wait = 0
		return
	shot_wait += 1
	if shot_wait > 30:
		get_viewport().get_texture().get_image().save_png("res://shots/%s.png" % spec[1])
		print("shot saved: ", spec[1])
		lan_shots.pop_front()
		shot_wait = 0
		if lan_shots.is_empty() and shots_quit:
			get_tree().quit()

# =====================================================================
# v0.7 look & motion: fonts, panels that pop in, buttons that press,
# fades between screens, the respawn score card and the end screen.
# =====================================================================
var font_h: Font
var ga := 1.0
var ui_t := 9.0
var seen_state := "-"
var fade := 0.0
var pending_action := ""
var pending_t := 0.0
var pending_big := false
var pressed_r := Rect2()
var pressed_at := -9.0
var btn_i := 0
var intro_t := 9.0
var menu_actors: Array = []
var hud_hp := 100.0
var trail_hp := 100.0
var trail_hold := 0.0
var hud_prev_hp := 100.0
var ammo_pop := 0.0
var last_mag := -1
var peek_t := 0.0
var timer_rect := Rect2()
var cheer := ["", ""]
var me_was_alive := true
var anim_skip := false
var bubble_key := ""
var bubble_since := 0.0
var _sbf := StyleBoxFlat.new()
var leader_now = null
const BIG_ACTIONS := ["play", "again", "restart", "start", "menu", "leave", "to_lobby"]
const CHEERS_LAST := ["Last place is just the starting line.", "Big comebacks start with one kill.", "The match isn't over. Go get them!", "Slow down, aim first, then shoot."]
const TIPS := ["Tip: sit (Down) to shoot steadier.", "Tip: headshots do 60% more damage.", "Tip: grab a health kit before you fight.", "Tip: fly high and shoot down at them."]

func load_fonts() -> void:
	var body = load("res://fonts/InterDisplay-SemiBold.otf")
	var heavy = load("res://fonts/InterDisplay-Black.otf")
	if body != null:
		font = body
	if heavy != null:
		var fv := FontVariation.new()
		fv.base_font = heavy
		fv.variation_transform = Transform2D(Vector2(1.0, 0.2), Vector2(0.0, 1.0), Vector2.ZERO)
		fv.spacing_glyph = 1
		font_h = fv
	else:
		font_h = font

func ease_out(x: float) -> float:
	if anim_skip:
		return 1.0
	x = clampf(x, 0.0, 1.0)
	return 1.0 - pow(1.0 - x, 3.0)

func ease_back(x: float) -> float:
	if anim_skip:
		return 1.0
	x = clampf(x, 0.0, 1.0)
	var c1 := 1.70158
	return 1.0 + (c1 + 1.0) * pow(x - 1.0, 3.0) + c1 * pow(x - 1.0, 2.0)

func txh(s2: String, pos: Vector2, size: float, col: Color, align: int = 0, outline := 0.0) -> void:
	txt(s2, pos, size, col, align, outline, font_h)

func fbox(r: Rect2, col: Color, radius: float, border := Color(0, 0, 0, 0), bw := 0.0, shadow := 0.0) -> void:
	_sbf.bg_color = Color(col, col.a * ga)
	_sbf.set_corner_radius_all(int(radius))
	_sbf.border_color = Color(border, border.a * ga)
	_sbf.set_border_width_all(int(bw))
	_sbf.shadow_size = int(shadow)
	_sbf.shadow_color = Color(0, 0, 0, 0.45 * ga)
	_sbf.shadow_offset = Vector2(0, shadow * 0.3)
	_sbf.anti_aliasing = true
	draw_style_box(_sbf, r)

func circ(pos: Vector2, r: float, col: Color) -> void:
	draw_circle(pos, r, Color(col, col.a * ga))

func vignette(col: Color, edge := 0.3) -> void:
	var clear := Color(col, 0.0)
	var e := sh * edge
	var ex := sw * edge * 0.6
	draw_polygon(PackedVector2Array([Vector2(0, 0), Vector2(sw, 0), Vector2(sw, e), Vector2(0, e)]), PackedColorArray([col, col, clear, clear]))
	draw_polygon(PackedVector2Array([Vector2(0, sh - e), Vector2(sw, sh - e), Vector2(sw, sh), Vector2(0, sh)]), PackedColorArray([clear, clear, col, col]))
	draw_polygon(PackedVector2Array([Vector2(0, 0), Vector2(ex, 0), Vector2(ex, sh), Vector2(0, sh)]), PackedColorArray([col, clear, clear, col]))
	draw_polygon(PackedVector2Array([Vector2(sw - ex, 0), Vector2(sw, 0), Vector2(sw, sh), Vector2(sw - ex, sh)]), PackedColorArray([clear, col, col, clear]))

func draw_crown(c: Vector2, s2: float) -> void:
	var pts := PackedVector2Array([c + Vector2(-s2, s2 * 0.6), c + Vector2(-s2, -s2 * 0.4), c + Vector2(-s2 * 0.5, s2 * 0.05), c + Vector2(0, -s2 * 0.75),
		c + Vector2(s2 * 0.5, s2 * 0.05), c + Vector2(s2, -s2 * 0.4), c + Vector2(s2, s2 * 0.6)])
	var outline := pts.duplicate()
	outline.append(pts[0])
	draw_colored_polygon(pts, Color(1, 0.82, 0.25, ga))
	draw_polyline(outline, Color(0.35, 0.22, 0, 0.9 * ga), maxf(1.0, s2 * 0.18), true)

func current_leader():
	var best = null
	var tie := false
	for p in players:
		if best == null or p.kills > best.kills:
			best = p
			tie = false
		elif p.kills == best.kills:
			tie = true
	if best == null or tie or best.kills < 1:
		return null
	return best

func on_state_change(old: String, new: String) -> void:
	ui_t = 0.0
	if new == "over" and old != "over":
		play_l("match_end", null, -4.0, 0.0)
	if new == "play" and old != "paused":
		intro_t = 9.0 if anim_skip else 0.0
		if not anim_skip:
			view_h = S.view_h * 1.5
			fade = maxf(fade, 0.6)
		me_was_alive = true
		was_leader_me = false
		last_tick_sec = -1
		play_l("rack", null, -3.0, 0.0)
		peek_t = 0.0
		last_mag = -1
		hud_hp = S.hp_max
		trail_hp = S.hp_max

var loops := {}
var loop_players := {}
var heart_t := 0.0
var fuel_beep_t := 0.0
var last_tick_sec := -1
var was_leader_me := false

func local_sounds(delta: float) -> void:
	if anim_skip or players.is_empty() or my_idx >= players.size() or state != "play":
		return
	var me: Player = players[my_idx]
	heart_t -= delta
	if me.alive and me.hp < 30 and heart_t <= 0:
		heart_t = 0.55 + clampf(me.hp / 30.0, 0.0, 1.0) * 0.4
		play_l("heart", null, -3.0, 0.0)
	fuel_beep_t -= delta
	if me.alive and me.jet_on and me.fuel < 18 and fuel_beep_t <= 0:
		fuel_beep_t = 0.7
		play_l("low_fuel", null, -10.0, 0.0)
	var left := match_time - t
	if left <= 10.0 and left > 0.0:
		var sec := ceili(left)
		if sec != last_tick_sec:
			last_tick_sec = sec
			play_l("tick", null, -8.0 if sec > 3 else -2.0, 0.0)
	var lead = current_leader()
	var me_lead: bool = lead == me
	if me_lead and not was_leader_me and t > 1.0:
		play_l("crown", null, -7.0, 0.0)
	elif was_leader_me and not me_lead and lead != null:
		play_l("lost_lead", null, -7.0, 0.0)
	was_leader_me = me_lead

func set_loop(pn: String, ln: String, db: float, delta: float) -> void:
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
	var amb: String = {"sky": "amb_sky", "outpost": "amb_outpost", "catacombs": "amb_catacombs"}.get(map_id, "amb_sky")
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
	update_loops(delta)
	ui_t += delta
	if state != seen_state:
		on_state_change(seen_state, state)
		seen_state = state
	fade = maxf(0.0, fade - delta / 0.4)
	peek_t -= delta
	ammo_pop = maxf(0.0, ammo_pop - delta * 5.0)
	if state == "play" or state == "paused":
		intro_t += delta
		local_sounds(delta)
	if pending_action != "":
		pending_t -= delta
		if pending_t <= 0:
			var a := pending_action
			pending_action = ""
			do_action(a)
			if pending_big:
				fade = 1.0
	if MENU_STATES.has(state):
		update_actors(minf(delta, 0.05))
		update_parts(minf(delta, 0.05))
	elif not players.is_empty() and my_idx < players.size():
		var me: Player = players[my_idx]
		if me_was_alive and not me.alive:
			cheer = make_cheer(me)
		me_was_alive = me.alive

# a few soldiers flying past behind the menus
func update_actors(dt: float) -> void:
	if menu_actors.is_empty():
		var looks := [["yellow", 0, "ak47"], ["red", 2, "sniper"], ["blue", 1, "rpg"]]
		for i in 3:
			var p := Player.new()
			p.id = 100 + i
			p.actor = true
			p.team = looks[i][0]
			p.color = TEAM_COL[looks[i][1]]
			p.slots = [full_slot(looks[i][2]), null]
			p.look = random_look()
			p.alive = true
			menu_actors.append(p)
	var vw := sw / zoom
	var vh := sh / zoom
	for i in menu_actors.size():
		var p: Player = menu_actors[i]
		var spd := 60.0 + i * 22.0
		p.x = cam.x - 140.0 + fposmod(time_s * spd + i * 520.0, vw + 280.0)
		p.y = cam.y + vh * (0.16 + 0.22 * i) + sin(time_s * 0.8 + i * 2.1) * 26.0
		p.vx = spd
		p.on_ground = false
		p.jet_on = true
		p.aim = 0.1 + sin(time_s * 0.6 + i) * 0.18
		animate(p, dt)
		if randf() < 0.5:
			var nz := center(p) + Vector2(-9, 10)
			add_part(nz.x + randf_range(-3, 3), nz.y, randf_range(-20, 20) - spd * 0.3, randf_range(90, 160), 0.5, Color(0.85, 0.85, 0.88, 0.4), 6, -0.02, "smoke", 18)

func draw_top_layers() -> void:
	if cfg.show_fps:
		draw_set_transform_matrix(Transform2D.IDENTITY)
		txt("%d FPS" % Engine.get_frames_per_second(), Vector2(sw - 10 * u, sh - 8 * u), 11 * u, C_ARC, 2, 3 * u)
	draw_set_transform_matrix(Transform2D.IDENTITY)
	ga = 1.0
	draw_toast()
	var fa := fade
	if pending_action != "" and pending_big:
		fa = maxf(fa, 1.0 - pending_t / 0.22)
	if fa > 0.001 and not anim_skip:
		draw_rect(Rect2(0, 0, sw, sh), Color(0.02, 0.03, 0.08, clampf(fa, 0.0, 1.0)))

func end_panel() -> void:
	draw_set_transform_matrix(Transform2D.IDENTITY)
	ga = 1.0

# ---------- ranking rows (respawn card, peek, end screen) ----------
func draw_rank_rows(x: float, y: float, w: float, rowh: float, rk: Array, age: float, aw := {}) -> void:
	var lead = current_leader()
	txt("KILLS", Vector2(x + w - 62 * u, y - 6 * u), 9 * u, C_MUTED, 2)
	txt("DEATHS", Vector2(x + w - 8 * u, y - 6 * u), 9 * u, C_MUTED, 2)
	for i in rk.size():
		var p: Player = rk[i]
		var kk := ease_out((age - 0.1 - i * 0.05) / 0.28)
		var ga0 := ga
		ga *= kk
		var rr := Rect2(x + (1.0 - kk) * 24 * u, y + i * rowh, w, rowh - 3 * u)
		var mine := is_me(p)
		if mine:
			fbox(rr, Color(C_ARC, 0.16), 7 * u, Color(C_ARC, 0.55), maxf(1.0, u))
		elif i % 2 == 0:
			fbox(rr, Color(1, 1, 1, 0.035), 7 * u)
		var by := rr.position.y + rowh * 0.62
		txh("%d" % (i + 1), Vector2(rr.position.x + 10 * u, by), 13 * u, C_ARC if i == 0 else C_MUTED)
		head_icon(plook(p), Vector2(rr.position.x + 34 * u, by - 4.5 * u), 0.62 * u, p.color)
		var nx := rr.position.x + 46 * u
		txt(p.pname, Vector2(nx, by), 13 * u, C_ARC if mine else C_INK)
		nx += font.get_string_size(p.pname, 0, -1, int(13 * u)).x + 8 * u
		if p == lead:
			draw_crown(Vector2(nx + 6 * u, by - 5 * u), 6 * u)
			nx += 18 * u
		if aw.has(p):
			var lab: String = aw[p][0]
			var cw := font.get_string_size(lab, 0, -1, int(8 * u)).x + 12 * u
			fbox(Rect2(nx, by - 11 * u, cw, 14 * u), Color(aw[p][1], 0.2), 7 * u, Color(aw[p][1], 0.7), maxf(1.0, u * 0.8))
			txt(lab, Vector2(nx + cw / 2, by - 1 * u), 8 * u, aw[p][1], 1)
		var shown := p.kills
		if not aw.is_empty():
			shown = int(round(p.kills * ease_out((age - 0.3 - i * 0.06) / 0.6)))
		txh(str(shown), Vector2(rr.end.x - 62 * u, by), 14 * u, C_INK, 2)
		txt(str(p.deaths), Vector2(rr.end.x - 8 * u, by), 13 * u, C_MUTED, 2)
		ga = ga0

func team_bar(x: float, y: float, w: float) -> void:
	var ts := team_scores()
	var tot := maxf(1.0, float(ts[0] + ts[1]))
	var bw: float = w * (0.5 if ts[0] + ts[1] == 0 else ts[0] / tot)
	fbox(Rect2(x, y, w, 8 * u), Color(TEAM_COL[2], 0.85), 4 * u)
	fbox(Rect2(x, y, maxf(bw, 8 * u), 8 * u), Color(TEAM_COL[1], 0.95), 4 * u)
	txh("BLUE %d" % ts[0], Vector2(x, y - 5 * u), 12 * u, TEAM_COL[1])
	txh("%d RED" % ts[1], Vector2(x + w, y - 5 * u), 12 * u, TEAM_COL[2], 2)

func make_cheer(me: Player) -> Array:
	var rk := ranked()
	var pos := rk.find(me)
	var n := rk.size()
	var l1 := ""
	var l2 := ""
	if cfg.mode == "team":
		var ts := team_scores()
		var mine: int = ts[me.side % 2]
		var other: int = ts[1 - me.side % 2]
		if mine > other:
			l1 = "Your team leads by %d. Keep it up!" % (mine - other)
		elif mine == other:
			l1 = "It's tied. Your next kill puts your team ahead."
		else:
			var g := other - mine + 1
			l1 = "Your team needs %d kill%s to take the lead." % [g, "" if g == 1 else "s"]
	elif pos == 0 and me.kills > 0:
		l1 = "You're number 1. Make them chase you."
	elif pos > 0:
		var above: Player = rk[pos - 1]
		var g2: int = maxi(1, above.kills - me.kills + (0 if above.kills == me.kills else 1))
		l1 = "%d kill%s to pass %s" % [g2, "" if g2 == 1 else "s", above.pname]
	else:
		l1 = "Go get the first kill!"
	if me.lstreak >= 2:
		l2 = "Nice run: %d kills in a row." % me.lstreak
	elif pos == n - 1 and n > 2 and cfg.mode != "team":
		l2 = CHEERS_LAST[randi() % CHEERS_LAST.size()]
	else:
		l2 = TIPS[randi() % TIPS.size()]
	return [l1, l2]

func death_line(me: Player) -> Array:
	var k = me.last_hit_by
	if k != null and k != me:
		var how := ""
		if WD.has(me.last_gun):
			how = WD[me.last_gun].name
		else:
			how = {"grenade": "GRENADE", "rpg": "ROCKET", "bomb": "TIME BOMB", "melee": "KNIFE", "shock": "SHOCK", "smoke": "SMOKE GAS"}.get(me.last_gun, "")
		if me.last_head and me.last_cause == "shot":
			how += "  /  HEADSHOT"
		return [k.pname, k.color, how]
	var note: String = {"water": "You drowned", "crush": "A falling rock got you", "fire": "You burned", "gas": "The gas got you"}.get(me.last_cause, "Your own blast got you")
	return ["", C_INK, note]

func draw_respawn_card(me: Player) -> void:
	var age := S.respawn - me.respawn_t
	var ready_k := clampf(me.respawn_t / 0.9, 0.0, 1.0)
	if ready_k < 1.0:
		var gk := 1.0 - ready_k
		txh("GET READY", Vector2(sw / 2, sh * 0.2), 30 * u * (0.9 + 0.1 * gk), Color(C_ARC, gk), 1, 5 * u)
		txt("You land here", Vector2(sw / 2, sh * 0.2 + 24 * u), 12 * u, Color(C_INK, gk), 1, 3 * u)
	var a := ease_out(age / 0.3) * ready_k
	var k := ease_back((age - 0.05) / 0.4)
	draw_rect(Rect2(0, 0, sw, sh), Color(0.25, 0.0, 0.03, 0.18 * a))
	vignette(Color(0.3, 0.0, 0.04, 0.6 * a), 0.28)
	var rk := ranked()
	var team: bool = cfg.mode == "team"
	var rowh := 23 * u
	var w := minf(sw - 40 * u, 470 * u)
	var h := 84 * u + (26 * u if team else 0.0) + rk.size() * rowh + 54 * u
	h = minf(h, sh - 16 * u)
	var r := Rect2(sw / 2 - w / 2, (sh - h) / 2 + (1.0 - k) * 70 * u, w, h)
	ga = a
	fbox(r, Color(0.06, 0.08, 0.18, 0.93), 16 * u, Color(1, 1, 1, 0.1), maxf(1.0, 1.5 * u), 22 * u)
	fbox(Rect2(r.position + Vector2(2, 2) * u, Vector2(r.size.x - 4 * u, 50 * u)), Color(1, 1, 1, 0.03), 14 * u)
	fbox(Rect2(r.position.x + 24 * u, r.position.y - 2 * u, 64 * u, 4 * u), C_RED, 2 * u)
	var x := r.position.x + 22 * u
	var y := r.position.y
	txh("TAKEN OUT", Vector2(x, y + 36 * u), 22 * u, C_RED, 0, 4 * u)
	var dl := death_line(me)
	if dl[0] != "":
		txt("by", Vector2(x, y + 58 * u), 12 * u, C_MUTED)
		var nx := x + font.get_string_size("by ", 0, -1, int(12 * u)).x
		txt(dl[0], Vector2(nx, y + 58 * u), 12 * u, dl[1])
		nx += font.get_string_size(dl[0], 0, -1, int(12 * u)).x + 8 * u
		txt(dl[2], Vector2(nx, y + 58 * u), 10 * u, C_MUTED)
	else:
		txt(dl[2], Vector2(x, y + 58 * u), 12 * u, C_MUTED)
	# countdown ring
	var cc := Vector2(r.end.x - 42 * u, y + 40 * u)
	draw_arc(cc, 22 * u, 0, TAU, 48, Color(1, 1, 1, 0.12 * ga), 4 * u, true)
	var left := clampf(me.respawn_t / S.respawn, 0.0, 1.0)
	if left > 0.01:
		draw_arc(cc, 22 * u, -PI / 2, -PI / 2 + TAU * left, 48, Color(C_ARC, ga), 4 * u, true)
	txh(str(maxi(1, ceili(me.respawn_t))), cc + Vector2(0, 8 * u), 22 * u, C_INK, 1)
	var ry := y + 92 * u
	if team:
		team_bar(x, y + 92 * u, r.size.x - 44 * u)
		ry += 26 * u
	draw_rank_rows(r.position.x + 14 * u, ry, r.size.x - 28 * u, rowh, rk, age)
	var ck := ease_out((age - 0.45) / 0.35)
	var ga0 := ga
	ga *= ck
	txh(cheer[0], Vector2(x, r.end.y - 30 * u), 14 * u, C_ARC)
	txt(cheer[1], Vector2(x, r.end.y - 12 * u), 11 * u, C_MUTED)
	ga = ga0
	ga = 1.0

func draw_peek() -> void:
	var a := ease_out(minf(3.0 - peek_t, peek_t) / 0.2) if peek_t > 0 else 1.0
	var rk := ranked()
	var rowh := 19 * u
	var w := minf(sw - 40 * u, 300 * u)
	var team: bool = cfg.mode == "team"
	var h := 26 * u + (24 * u if team else 0.0) + rk.size() * rowh + 8 * u
	var r := Rect2(sw - safe_r - w - 12 * u + (1.0 - a) * 24 * u, 60 * u, w, h)
	ga = a
	fbox(r, Color(0.05, 0.07, 0.16, 0.88), 12 * u, Color(1, 1, 1, 0.1), maxf(1.0, u), 14 * u)
	var ry := r.position.y + 26 * u
	if team:
		team_bar(r.position.x + 14 * u, r.position.y + 28 * u, w - 28 * u)
		ry += 24 * u
	draw_rank_rows(r.position.x + 10 * u, ry, w - 20 * u, rowh, rk, 9.0)
	ga = 1.0

func awards(rk: Array) -> Dictionary:
	var out := {}
	if not rk.is_empty() and rk[0].kills > 0:
		out[rk[0]] = ["MVP", C_ARC]
	var picks := [["hs", 1, "SHARPSHOOTER", C_CYAN], ["best", 3, "ON FIRE", Color("#ff9a4d")], ["bk", 2, "BOMBER", Color("#ffc061")], ["mk", 1, "KNIFE MASTER", C_PINK]]
	for pk in picks:
		var best = null
		for p in rk:
			if not out.has(p) and p.get(pk[0]) >= pk[1] and (best == null or p.get(pk[0]) > best.get(pk[0])):
				best = p
		if best != null:
			out[best] = [pk[2], pk[3]]
	var few = null
	for p in rk:
		if not out.has(p) and p.kills > 0 and (few == null or p.deaths < few.deaths):
			few = p
	if few != null:
		out[few] = ["SURVIVOR", C_GREEN]
	var most = null
	for p in rk:
		if not out.has(p) and p.deaths > 0 and (most == null or p.deaths > most.deaths):
			most = p
	if most != null:
		out[most] = ["NEVER GAVE UP", Color("#b9a2ff")]
	for p in rk:
		if not out.has(p):
			out[p] = ["FIGHTER", C_MUTED]
	return out

func end_line(rk: Array) -> String:
	var me: Player = players[my_idx]
	if cfg.mode == "team":
		var ts := team_scores()
		var mine: int = ts[me.side % 2]
		var other: int = ts[1 - me.side % 2]
		if mine > other:
			return "Your team won! You got %d kill%s for the team." % [me.kills, "" if me.kills == 1 else "s"]
		if mine == other:
			return "A draw. One more kill would have done it!"
		return "So close. Next match is yours."
	var pos := rk.find(me)
	if pos == 0 and me.kills > 0:
		return "You won! Can you do it again?"
	if pos == rk.size() - 1:
		return "You got %d kill%s. Next match, aim for %d!" % [me.kills, "" if me.kills == 1 else "s", me.kills + 2]
	var g: int = rk[0].kills - me.kills + 1
	return "%d more kill%s and you would have won. Go again!" % [g, "" if g == 1 else "s"]

# ================= AVATARS (v1.1) =================
var default_look := {}
var panel_xf := Transform2D.IDENTITY
var lk_tab := "sets"
var lk_page := 0
var lk_back := "menu"
var name_entry := ""

func parse_look(sv) -> Dictionary:
	var parts := str(sv).split(".")
	var d0 := AV_DEF.split(".")
	var out := {}
	for i in AV_KEYS.size():
		var k: String = AV_KEYS[i]
		var v: String = parts[i] if i < parts.size() else d0[i]
		var ok := false
		for it in AV_LIST[k]:
			if it[0] == v:
				ok = true
				break
		out[k] = v if ok else d0[i]
	return out

func look_str(lk: Dictionary) -> String:
	var a := PackedStringArray()
	for k in AV_KEYS:
		a.append(str(lk.get(k, "")))
	return ".".join(a)

func my_look() -> Dictionary:
	return parse_look(cfg.look if str(cfg.look) != "" else AV_DEF)

func plook(p) -> Dictionary:
	return p.look if not p.look.is_empty() else default_look

# bots: mostly one of the full looks, sometimes a wild mix
func random_look() -> Dictionary:
	if randf() < 0.6:
		return parse_look(AV_SETS[randi() % AV_SETS.size()][2])
	var out := {}
	for k in AV_KEYS:
		var arr: Array = AV_LIST[k]
		out[k] = arr[randi() % arr.size()][0]
	if out.fl == "none":
		out.fl = "orange"
	return out

func leg_tex(lk: Dictionary) -> String:
	return "leg" if lk.get("o", "army") == "army" else "leg_" + lk.o

# team games keep team-coloured sleeves so sides stay easy to tell apart
func sleeve_col(team_col: Color, lk: Dictionary) -> Color:
	if lk.get("o", "army") == "army" or cfg.mode == "team":
		return team_col
	return AV_SLEEVE.get(lk.o, team_col)

func av(nm: String, anchor: Vector2, sc: float, off: Vector2, col := Color.WHITE) -> void:
	var r = AV_RECT.get(nm)
	if r == null:
		return
	draw_texture_rect(tex["av_" + nm], Rect2((Vector2(r[0], r[1]) - anchor) * sc + off, Vector2(r[2], r[3]) * sc), false, col)

func av_back(lk: Dictionary, tint: Color) -> void:
	if AV_BACK.has(lk.x):
		av("x_" + lk.x, AV_BODY_A, 1.1, Vector2(0, -3), tint)

func av_jet(lk: Dictionary, tint: Color) -> void:
	av("j_" + lk.j, AV_BODY_A, 1.1, Vector2(-3.5, -3), tint)

func av_torso(lk: Dictionary, team_col: Color, tint: Color) -> void:
	if lk.o == "army":
		av("o_army_shirt", AV_BODY_A, 1.1, Vector2(0, -3), team_col * tint)
		av("o_army", AV_BODY_A, 1.1, Vector2(0, -3), tint)
	else:
		av("o_" + lk.o, AV_BODY_A, 1.1, Vector2(0, -3), tint)
	if lk.x != "none" and not AV_BACK.has(lk.x) and not AV_FRONT.has(lk.x):
		av("x_" + lk.x, AV_BODY_A, 1.1, Vector2(0, -3), tint)

func av_head(lk: Dictionary, team_col: Color, tint: Color) -> void:
	av("face", AV_HEAD_A, 1.05, Vector2.ZERO, tint)
	if not AV_FULL.has(lk.h):
		av("f_" + lk.f, AV_HEAD_A, 1.05, Vector2.ZERO, tint)
	av("h_" + lk.h, AV_HEAD_A, 1.05, Vector2.ZERO, team_col * tint if lk.h == "classic" else tint)

func av_front(lk: Dictionary, tint: Color) -> void:
	if AV_FRONT.has(lk.x):
		av("x_" + lk.x, AV_BODY_A, 1.1, Vector2(0, -3 + sin(time_s * 3.0) * 1.5), tint)

# a standing/flying soldier for menus; pos is the body centre on screen
func draw_avatar(lk: Dictionary, pos: Vector2, sc: float, col: Color, fly := true, gun := "ak47") -> void:
	var a := Color(1, 1, 1, ga)
	var body := panel_xf * Transform2D(0.0, Vector2(sc, sc), 0.0, pos)
	draw_set_transform_matrix(body)
	av_back(lk, a)
	var fc = AV_FLAME.get(lk.fl)
	if fly and fc != null:
		var fl := 15.0 + sin(time_s * 38.0) * 3.0 + sin(time_s * 21.0) * 1.5
		for nx in [-12.0, -6.0]:
			draw_texture_rect(tex.glow, Rect2(nx - 6, 9, 12, fl), false, Color(fc[0], fc[0].a * ga))
			draw_texture_rect(tex.glow, Rect2(nx - 3.5, 9, 7, fl * 0.6), false, Color(fc[1], ga))
	draw_leg(body, Vector2(-3, 4), 0.3, 0.15, Color(0.78, 0.78, 0.78, ga), leg_tex(lk))
	draw_set_transform_matrix(body)
	av_jet(lk, a)
	var sl := sleeve_col(col, lk)
	var sh_pt := Vector2(1, -6)
	var grip := sh_pt + Vector2(7, 1)
	draw_line(sh_pt + Vector2(-2, 0), grip, Color(C_OUT, ga), 6.0, true)
	draw_line(sh_pt + Vector2(-2, 0), grip, Color(sl.darkened(0.2), ga), 4.0, true)
	av_torso(lk, col, a)
	draw_leg(body, Vector2(3, 4), -0.2, 0.05, a, leg_tex(lk))
	draw_set_transform_matrix(body * Transform2D(0.0, Vector2.ONE, 0.0, Vector2(1, -15)))
	av_head(lk, col, a)
	var m: Dictionary = META.GUN[gun]
	var gd: float = S.gun_draw
	draw_set_transform_matrix(body * Transform2D(0.0, Vector2.ONE, 0.0, grip))
	draw_texture_rect(tex["gun_" + gun], Rect2(-m.grip[0] * gd, -m.grip[1] * gd, m.size[0] * gd, m.size[1] * gd), false, a)
	draw_set_transform_matrix(body)
	var fh := grip + Vector2(m.front[0] - m.grip[0], m.front[1] - m.grip[1]) * gd
	draw_line(sh_pt + Vector2(3, 0), fh, Color(C_OUT, ga), 6.0, true)
	draw_line(sh_pt + Vector2(3, 0), fh, Color(sl, ga), 4.0, true)
	draw_texture_rect(tex.hand, Rect2(fh - Vector2(3, 3), Vector2(6, 6)), false, a)
	draw_texture_rect(tex.hand, Rect2(grip - Vector2(3, 3), Vector2(6, 6)), false, a)
	av_front(lk, a)
	draw_set_transform_matrix(panel_xf)

func head_icon(lk: Dictionary, pos: Vector2, sc: float, col: Color) -> void:
	draw_set_transform_matrix(panel_xf * Transform2D(0.0, Vector2(sc, sc), 0.0, pos))
	av_head(lk, col, Color(1, 1, 1, ga))
	draw_set_transform_matrix(panel_xf)

func lk_items(tab: String) -> Array:
	if tab == "sets":
		var out := []
		for st in AV_SETS:
			out.append([st[2], st[1]])
		return out
	return AV_LIST[tab]

# a flat tap target that does not slide in (used for many small keys / tiles)
func flat_btn(r: Rect2, action: String, on := false) -> Rect2:
	ui_btns.append({"r": r, "a": action})
	var rr := r
	if r == pressed_r and time_s - pressed_at < 0.18:
		rr = rr.grow(-3 * u)
	elif not touch_mode and mouse_used and r.has_point(mouse_pos):
		rr.position.y -= 2 * u
	return rr

func draw_dice(c: Vector2, sz: float) -> void:
	fbox(Rect2(c - Vector2(sz, sz) / 2, Vector2(sz, sz)), Color("#f4f6ff"), sz * 0.22, C_OUT, maxf(1.0, sz * 0.06))
	for d in [Vector2(-0.24, -0.24), Vector2(0.24, 0.24), Vector2(0, 0), Vector2(0.24, -0.24), Vector2(-0.24, 0.24)]:
		circ(c + d * sz, sz * 0.09, C_OUT)

func draw_locker() -> void:
	var w := minf(sw - 24 * u, 800 * u)
	var h := minf(sh - 20 * u, 390 * u)
	var r := panel(w, h)
	var x := r.position.x + 22 * u
	var y := r.position.y
	var lk := my_look()
	txh("LOCKER", Vector2(x, y + 38 * u), 24 * u, C_ARC, 0, 4 * u)
	txt("Mix any parts you like. Saved on this phone.", Vector2(r.end.x - 22 * u, y + 34 * u), 10 * u, C_MUTED, 2)
	# left: name and a big preview
	var lw := 206 * u
	var nr := flat_btn(Rect2(x, y + 50 * u, lw - 46 * u, 38 * u), "lk_name")
	fbox(nr, Color(0.02, 0.03, 0.08, 0.9), 9 * u, Color(1, 1, 1, 0.16), maxf(1.0, u))
	txt("NAME", nr.position + Vector2(10 * u, 13 * u), 8 * u, C_CYAN)
	txh(my_name(), nr.position + Vector2(10 * u, 31 * u), 15 * u, C_INK)
	txt("EDIT", Vector2(nr.end.x - 8 * u, nr.position.y + 24 * u), 9 * u, C_ARC, 2)
	var dr := flat_btn(Rect2(x + lw - 40 * u, y + 50 * u, 40 * u, 38 * u), "lk_dice")
	fbox(dr, Color(0.2, 0.25, 0.43), 9 * u, Color(1, 1, 1, 0.13), maxf(1.0, u))
	draw_dice(dr.get_center(), 20 * u)
	var stage := Rect2(x, y + 96 * u, lw, r.end.y - 66 * u - (y + 96 * u))
	fbox(stage, Color(0.13, 0.17, 0.34, 0.9), 14 * u, Color(1, 1, 1, 0.08), maxf(1.0, u))
	fbox(Rect2(stage.position + Vector2(20 * u, stage.size.y - 30 * u), Vector2(stage.size.x - 40 * u, 12 * u)), Color(0, 0, 0, 0.25), 6 * u)
	var sc := minf(stage.size.y / 74.0, stage.size.x / 72.0)
	draw_avatar(lk, stage.get_center() + Vector2(-4 * sc, 4 * sc + sin(time_s * 2.0) * 3 * u), sc, TEAM_COL[0])
	if lk_tab == "f" and AV_FULL.has(lk.h):
		txt("Your helmet covers the face.", Vector2(stage.get_center().x, stage.position.y + 18 * u), 9.5 * u, C_MUTED, 1)
		txt("Pick a different helmet to show it.", Vector2(stage.get_center().x, stage.position.y + 31 * u), 9.5 * u, C_MUTED, 1)
	ui_button("SURPRISE ME", Rect2(x, r.end.y - 56 * u, lw, 42 * u), "lk_rand")
	# right: tabs and options
	var rx := x + lw + 18 * u
	var aw := r.end.x - 22 * u - rx
	var tw := (aw - 6 * 5 * u) / 7.0
	for i in LK_TABS.size():
		var tb: Array = LK_TABS[i]
		var on: bool = lk_tab == tb[0]
		var tr := flat_btn(Rect2(rx + i * (tw + 5 * u), y + 50 * u, tw, 34 * u), "lk_tab:" + tb[0])
		fbox(tr, C_ARC if on else Color(0.17, 0.21, 0.38, 0.95), 8 * u, Color(1, 1, 1, 0.12), maxf(1.0, u))
		txh(tb[1], tr.get_center() + Vector2(0, 4 * u), 10 * u, Color("#2a1f00") if on else C_INK, 1)
	var items := lk_items(lk_tab)
	var gy := y + 94 * u
	var gh := r.end.y - 66 * u - gy
	var cols := maxi(3, int(aw / (84 * u)))
	var rows := maxi(1, int(gh / (102 * u)))
	var gap := 7 * u
	var cw := (aw - (cols - 1) * gap) / cols
	var chh := (gh - (rows - 1) * gap) / rows
	var per := cols * rows
	var pages := maxi(1, ceili(items.size() / float(per)))
	lk_page = clampi(lk_page, 0, pages - 1)
	var cur_s := look_str(lk)
	for j in range(lk_page * per, mini(items.size(), (lk_page + 1) * per)):
		var it: Array = items[j]
		var k := j - lk_page * per
		var tr := Rect2(rx + (k % cols) * (cw + gap), gy + (k / cols) * (chh + gap), cw, chh)
		var tl: Dictionary
		var sel: bool
		if lk_tab == "sets":
			tl = parse_look(it[0])
			sel = cur_s == look_str(tl)
		else:
			tl = lk.duplicate()
			tl[lk_tab] = it[0]
			if lk_tab == "f" and AV_FULL.has(tl.h):
				tl.h = "classic"
			sel = lk[lk_tab] == it[0]
		var ga0 := ga
		ga *= clampf((ui_t - 0.1 - k * 0.025) / 0.2, 0.0, 1.0) if not anim_skip else 1.0
		var rr := flat_btn(tr, "lk_pick:%s:%s" % [lk_tab, it[0]])
		fbox(rr, Color(0.3, 0.25, 0.09, 0.95) if sel else Color(0.11, 0.14, 0.29, 0.95), 10 * u, C_ARC if sel else Color(1, 1, 1, 0.1), (2.0 if sel else 1.0) * maxf(1.0, u))
		var s2 := minf((chh - 22 * u) / 70.0, cw / 66.0)
		draw_avatar(tl, Vector2(rr.get_center().x - 4 * s2, rr.position.y + (chh - 20 * u) / 2.0 + 5 * s2), s2, TEAM_COL[0])
		var lab: String = it[1]
		txt(lab, Vector2(rr.get_center().x, rr.end.y - 7 * u), (8.5 if lab.length() > 13 else 9.5) * u, C_ARC if sel else C_INK, 1, 2 * u)
		ga = ga0
	if pages > 1:
		var py := r.end.y - 54 * u
		var pr := flat_btn(Rect2(r.end.x - 22 * u - 150 * u, py, 44 * u, 38 * u), "lk_page:-1")
		fbox(pr, Color(0.2, 0.25, 0.43, 1.0 if lk_page > 0 else 0.4), 9 * u)
		txh("<", pr.get_center() + Vector2(0, 6 * u), 18 * u, C_INK, 1)
		txt("%d / %d" % [lk_page + 1, pages], Vector2(r.end.x - 22 * u - 75 * u, py + 25 * u), 12 * u, C_MUTED, 1)
		var nx := flat_btn(Rect2(r.end.x - 22 * u - 44 * u, py, 44 * u, 38 * u), "lk_page:1")
		fbox(nx, Color(0.2, 0.25, 0.43, 1.0 if lk_page < pages - 1 else 0.4), 9 * u)
		txh(">", nx.get_center() + Vector2(0, 6 * u), 18 * u, C_INK, 1)
	ui_button("DONE", Rect2(rx, r.end.y - 56 * u, 170 * u, 42 * u), "lk_done", true)

func name_key(k: String, raw := false) -> void:
	if k == "DEL":
		name_entry = name_entry.substr(0, maxi(0, name_entry.length() - 1))
		return
	if k == "SPACE":
		k = " "
	if name_entry.length() >= 12 and key_target == "name":
		return
	if k == " " and key_target != "name":
		return
	if k == " " and (name_entry == "" or name_entry.ends_with(" ")):
		return
	if key_target == "room":
		k = k.to_upper()
		if name_entry.length() < 8 and "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789".contains(k):
			name_entry += k
		return
	if key_target == "server":
		k = k.to_lower()
		if name_entry.length() < 48 and "abcdefghijklmnopqrstuvwxyz0123456789.-:".contains(k):
			name_entry += k
		return
	if not raw:
		k = k.to_upper() if (name_entry == "" or name_entry.ends_with(" ")) else k.to_lower()
	var ok := "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 _-"
	if ok.contains(k):
		name_entry += k

func draw_namekey() -> void:
	var w := minf(sw - 24 * u, 720 * u)
	var h := minf(sh - 20 * u, 370 * u)
	var r := panel(w, h)
	var x := r.position.x + 22 * u
	var y := r.position.y
	var iw := w - 44 * u
	var titles := {"name": ["YOUR NAME", "Up to 12 letters. Everyone sees it over your head."],
		"room": ["ROOM CODE", "Type the code your friend got, like TIGER42."],
		"server": ["SERVER ADDRESS", "Ask the admin. Like 140.238.1.2 or name.ply.gg:12345"]}
	var tt: Array = titles.get(key_target, titles.name)
	txh(tt[0], Vector2(x, y + 38 * u), 24 * u, C_ARC, 0, 4 * u)
	txt(tt[1], Vector2(r.end.x - 22 * u, y + 34 * u), 10 * u, C_MUTED, 2)
	var fr := Rect2(x, y + 50 * u, iw - 220 * u, 44 * u)
	fbox(fr, Color(0.02, 0.03, 0.08, 0.9), 9 * u, Color(C_ARC, 0.5), maxf(1.0, 1.5 * u))
	var caret := "|" if fmod(time_s, 1.0) < 0.5 else ""
	txh(name_entry + caret, fr.position + Vector2(14 * u, 31 * u), 22 * u, C_INK)
	if key_target == "name":
		txt("%d/12" % name_entry.length(), Vector2(fr.end.x - 10 * u, fr.position.y + 28 * u), 10 * u, C_MUTED, 2)
		var dr := flat_btn(Rect2(fr.end.x + 8 * u, fr.position.y, 44 * u, 44 * u), "lk_dice")
		fbox(dr, Color(0.2, 0.25, 0.43), 9 * u, Color(1, 1, 1, 0.13), maxf(1.0, u))
		draw_dice(dr.get_center(), 22 * u)
	var okx := fr.end.x + 60 * u
	ui_button({"name": "SAVE", "room": "JOIN", "server": "SAVE"}.get(key_target, "SAVE"), Rect2(okx, fr.position.y, r.end.x - 22 * u - okx, 44 * u), "name_ok", true)
	var ky := y + 104 * u
	var gap := 5 * u
	var kw := (iw - 9 * gap) / 10.0
	var kh := minf(44 * u, (r.end.y - 16 * u - ky - 4 * gap) / 5.0)
	for ri in KB_ROWS.size():
		var row: String = KB_ROWS[ri]
		if ri == 3 and key_target == "server":
			row = "ZXCVBNM.-:"
		var x0 := x + (iw - (row.length() * kw + (row.length() - 1) * gap)) / 2.0
		for ci in row.length():
			var kr := flat_btn(Rect2(x0 + ci * (kw + gap), ky + ri * (kh + gap), kw, kh), "nk:" + row[ci])
			fbox(kr, Color(0.17, 0.21, 0.38, 0.95), 8 * u, Color(1, 1, 1, 0.12), maxf(1.0, u))
			txh(row[ci], kr.get_center() + Vector2(0, 6 * u), 16 * u, C_INK, 1)
	var by := ky + 4 * (kh + gap)
	var sp := flat_btn(Rect2(x, by, 7 * kw + 6 * gap, kh), "nk:SPACE")
	fbox(sp, Color(0.17, 0.21, 0.38, 0.95), 8 * u, Color(1, 1, 1, 0.12), maxf(1.0, u))
	txh("SPACE", sp.get_center() + Vector2(0, 5 * u), 12 * u, C_MUTED, 1)
	var dl := flat_btn(Rect2(x + 7 * (kw + gap), by, 2 * kw + gap, kh), "nk:DEL")
	fbox(dl, Color(0.35, 0.14, 0.2, 0.95), 8 * u, Color(1, 1, 1, 0.12), maxf(1.0, u))
	txh("DELETE", dl.get_center() + Vector2(0, 5 * u), 12 * u, C_INK, 1)
	var bk := flat_btn(Rect2(x + 9 * (kw + gap), by, kw, kh), "name_back")
	fbox(bk, Color(0.17, 0.21, 0.38, 0.95), 8 * u, Color(1, 1, 1, 0.12), maxf(1.0, u))
	txh("X", bk.get_center() + Vector2(0, 6 * u), 15 * u, C_MUTED, 1)

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
var pred_hist: Array = []
var pred_off := Vector2.ZERO
var in_seq := 0
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
	var direct_port := 0
	if host.contains(":"):
		direct_port = int(host.get_slice(":", 1))
		host = host.get_slice(":", 0)
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
	if direct_port > 0:
		mm_mode = ""
		if recon_left <= 0:
			conn_label = "Joining the home server"
		join_game(ip, direct_port)

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
				print("NET room %s is on port %s" % [mm_code, bits[2]])
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

# your own soldier moves at once on your phone. Each server update says where you really were after
# a given input; we start from there and replay the moves the server has not seen yet.
func predict_me(p: Player, dt: float) -> void:
	var inp: Dictionary = p.inp
	predict_step(p, float(inp.mx), bool(inp.fly), dt)
	pred_hist.append([in_seq, float(inp.mx), bool(inp.fly), dt])
	if pred_hist.size() > 180:
		pred_hist.pop_front()
	pred_off *= exp(-10.0 * dt)

func predict_step(p: Player, mx: float, fly_in: bool, dt: float) -> void:
	var c := center(p)
	var z = zone_at(c.x, c.y)
	var gm: float = z.g if z != null else 1.0
	var fm: float = z.f if z != null else 1.0
	var post_mul: float = S.crouch_speed if p.posture == "crouch" else (S.crawl_speed if p.posture == "prone" else 1.0)
	var fly: bool = fly_in and p.posture == "stand"
	if p.net_t > 0 or p.stun_t > 0:
		fly = false
		post_mul *= 0.35 if p.net_t > 0 else 0.15
	var cw0 = p.slots[p.cur]
	if cw0 != null and cw0.type == "minigun":
		post_mul *= 0.72
	var target: float = mx * S.move_speed * (0.55 if p.in_water else 1.0) * post_mul
	var acc := 2600.0 if p.on_ground else 1500.0
	if target != 0.0 and signf(target) != signf(p.vx):
		acc *= 1.5
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
	if not p.jet_on and not p.in_water:
		p.pfuel = minf(S.fuel_max, p.pfuel + (S.refill_ground if p.on_ground else S.refill_air) * dt)
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

# a server update for my own soldier: rewind to it, replay my newer moves, hide small jumps
func reconcile_me(p: Player, ack: int, fl: int) -> void:
	var old := Vector2(p.x, p.y)
	p.x = p.nx
	p.y = p.ny
	p.vx = p.svx
	p.vy = p.svy
	p.on_ground = (fl & 4) != 0
	p.jet_on = (fl & 2) != 0
	p.pfuel = p.fuel
	while not pred_hist.is_empty() and int(pred_hist[0][0]) <= ack:
		pred_hist.pop_front()
	for h in pred_hist:
		predict_step(p, h[1], h[2], h[3])
	var err := Vector2(p.x, p.y) - old
	var el := err.length()
	pred_err += el
	pred_n += 1
	if el > 60.0:
		pred_snaps += 1
		pred_off = Vector2.ZERO
	else:
		pred_off -= err

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
	if lan_players.is_empty() and stay_open:
		if state != "lobby":
			print("SERVER everyone left, back to waiting")
			state = "lobby"
			players.clear()
		idle_t = 0.0
	elif lan_players.is_empty():
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
			p.ack = 0
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

var pk_sig := 0
var pk_send := 0
var pk_every := 0
var dbg_sizes: Array = []

@rpc("authority", "call_remote", "reliable")
func s_feed(f) -> void:
	if net_role == "client" and typeof(f) == TYPE_ARRAY:
		feed = f

var stay_open := false

# ================= FAIR PLAY + RESPAWN (v1.4) =================
const SPREAD_PAT := [0.0, 0.3, -0.28, 0.14, -0.42, 0.4, -0.12, 0.22, -0.36, 0.46, -0.06, 0.32]

# move everyone else back to where this (remote) shooter saw them; returns what to put back
func rewind_others(shooter: Player) -> Array:
	var saved := []
	if not shooter.remote or shooter.lat <= 0.0:
		return saved
	var tt := t - shooter.lat
	for o in players:
		if o == shooter or o.hist.is_empty():
			continue
		var hp: Vector3 = o.hist[0]
		for h in o.hist:
			if h.x <= tt:
				hp = h
			else:
				break
		saved.append([o, o.x, o.y])
		o.x = hp.y
		o.y = hp.z
	return saved

func restore_others(saved: Array) -> void:
	for sv in saved:
		sv[0].x = sv[1]
		sv[0].y = sv[2]

# a beam of light drops the soldier in; everyone sees it for half a second
func draw_drop_beam(c: Vector2, age: float, wt: Transform2D) -> void:
	draw_set_transform_matrix(wt)
	var k := clampf(age / 0.6, 0.0, 1.0)
	var a := 1.0 - k
	var bw := 30.0 * (1.0 - k * 0.7)
	var top := c.y - 420.0 * gsign()
	var foot := c.y + 22.0 * gsign()
	draw_rect(Rect2(c.x - bw / 2, minf(top, foot), bw, absf(foot - top)), Color(0.55, 0.95, 1.0, 0.5 * a))
	draw_rect(Rect2(c.x - bw / 5, minf(top, foot), bw / 2.5, absf(foot - top)), Color(1, 1, 1, 0.9 * a))
	draw_arc(Vector2(c.x, foot), 10.0 + 70.0 * k, 0, TAU, 32, Color(0.6, 0.97, 1.0, 0.8 * a), 3.0, true)
	draw_arc(Vector2(c.x, foot), 4.0 + 40.0 * k, 0, TAU, 24, Color(1, 1, 1, 0.6 * a), 2.0, true)

# while you wait: a pulsing target where you will land (only on your screen)
func draw_landing_marker() -> void:
	if players.is_empty() or my_idx >= players.size() or state != "play":
		return
	var me: Player = players[my_idx]
	if me.alive or me.respawn_t >= 0.9:
		return
	var k := 1.0 - clampf(me.respawn_t / 0.9, 0.0, 1.0)
	var c := Vector2(me.x + 10, me.y + 21)
	var foot := c + Vector2(0, 22 * gsign())
	var pulse := 0.5 + 0.5 * sin(time_s * 10.0)
	draw_arc(foot, 18.0 + 6.0 * pulse, 0, TAU, 32, Color(C_ARC, 0.85 * k), 3.0, true)
	draw_arc(foot, 8.0, 0, TAU, 20, Color(1, 1, 1, 0.7 * k), 2.0, true)
	var ay := c.y - (46.0 + 6.0 * pulse) * gsign()
	draw_colored_polygon(PackedVector2Array([Vector2(c.x - 9, ay), Vector2(c.x + 9, ay), Vector2(c.x, ay + 12 * gsign())]), Color(C_ARC, k))

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
		var my_side: int = plan[mine] if mine >= 0 and mine < plan.size() else -1
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

var test_pick := -1
var lt_hold := 0.0

var prof_on := OS.get_cmdline_user_args().has("--profile")
var prof_proc: Array = []
var prof_draw: Array = []
var prof_frame: Array = []

var _pm_t := 0
var prof_sec := {}
var prof_n := 0
func _pm(nm: String) -> void:
	if not prof_on:
		return
	var n := Time.get_ticks_usec()
	prof_sec[nm] = prof_sec.get(nm, 0) + (n - _pm_t)
	_pm_t = n

# ================= SMOOTH (v1.6) =================
const SNAP_DT := 1.0 / 30.0
const INTERP := 0.1
const EDGE_KEYS := ["shoot", "swap", "grenade", "melee", "reload", "down", "bomb", "smoke", "zoom"]
var in_latch := {}
var snap_clock := 0.0
var jit_sum := 0.0
var jit_n := 0
var glide_log := OS.get_cmdline_user_args().has("--glidelog")
var no_glide := OS.get_cmdline_user_args().has("--noglide")
var view_r := Rect2(-100000, -100000, 200000, 200000)

# show another player a little in the past, gliding between the two updates around that moment
func glide(p: Player) -> void:
	var rt := snap_clock - INTERP
	var buf := p.sbuf
	var a: Array = buf[0]
	if rt <= a[0]:
		p.x = a[1]
		p.y = a[2]
		p.aim = a[5]
		return
	for j in range(buf.size() - 1):
		var s0: Array = buf[j]
		var s1: Array = buf[j + 1]
		if rt >= s0[0] and rt <= s1[0]:
			var k: float = (rt - float(s0[0])) / maxf(0.001, float(s1[0]) - float(s0[0]))
			p.x = lerpf(s0[1], s1[1], k)
			p.y = lerpf(s0[2], s1[2], k)
			p.vx = lerpf(s0[3], s1[3], k)
			p.vy = lerpf(s0[4], s1[4], k)
			p.aim = lerp_angle(s0[5], s1[5], k)
			return
	# no newer update yet: carry on a little along the last known speed
	var l: Array = buf[-1]
	var ex: float = minf(rt - float(l[0]), 0.15)
	p.x = l[1] + l[3] * ex
	p.y = l[2] + l[4] * ex
	p.vx = l[3]
	p.vy = l[4]
	p.aim = l[5]


# ---- test: sniper zoomed, run left/right and flick aim, log the camera ----
var zoom_test := false
var cam_look := Vector2.ZERO
var cam_pc := Vector2.ZERO
var zt_last := Vector2.ZERO
var zt_jumps := 0
var zt_max := 0.0
var zt_out := 0
var zt_edge := 1.0
var zt_n := 0
func zoom_script(dt: float) -> void:
	var me: Player = players[my_idx]
	if not me.alive:
		return
	var w = me.slots[me.cur]
	if w == null or w.type != "sniper":
		me.slots[me.cur] = full_slot("sniper")
		me.slots[me.cur].zi = 3 if not OS.get_cmdline_user_args().has("--z4") else 2
	me.protect_t = 99.0
	var ph := fmod(t, 3.2)
	me.inp.mx = 1.0 if ph < 1.6 else -1.0
	me.inp.fly = fmod(t, 2.0) < 0.5
	# flick the aim stick: forward, back, up-ish, as a player looking around
	var a: float = [0.0, PI, -0.6, PI + 0.5, 0.3][int(t / 0.7) % 5]
	if me.inp.mx < 0:
		a = PI - a
	me.inp.aim = a
	last_touch_aim = a

func zoom_log(me: Player, pc: Vector2, vw: float, vh: float) -> void:
	if t < 1.0:
		zt_last = cam
		return
	var jump := cam.distance_to(zt_last) / maxf(0.001, last_delta) / vw
	zt_last = cam
	zt_n += 1
	zt_max = maxf(zt_max, jump)
	if jump > 1.5:
		zt_jumps += 1
	var sx := (pc.x - cam.x) / vw
	var sy := (pc.y - cam.y) / vh
	var edge := minf(minf(sx, 1.0 - sx), minf(sy, 1.0 - sy))
	zt_edge = minf(zt_edge, edge)
	if edge < 0.08:
		zt_out += 1
	if zt_n % 300 == 0:
		print("ZOOMTEST zoom_level=%d view_h=%.0f gun=%s" % [zoom_level(me), view_h, str(me.slots[me.cur].type if me.slots[me.cur] != null else "none")])
		print("ZOOMTEST frames=%d fast_camera_frames=%d (cam moving >1.5 screens/sec) max=%.1f screens/sec  near_edge_frames=%d closest_to_edge=%.2f" % [zt_n, zt_jumps, zt_max, zt_out, zt_edge])
