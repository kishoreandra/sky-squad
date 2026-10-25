"""v1.7 part B: one action at a time in the soldier's animation."""
import sys
P = "/home/claude/skysquad/main.gd"
s = open(P).read()
ERR = []
def rep(a, b, c=1):
    global s
    if s.count(a) != c:
        ERR.append("expected %d got %d: %r" % (c, s.count(a), a[:120])); return
    s = s.replace(a, b)

# gun pose: melee wins, then swap, then reload; never a mix of all three
rep('''	gun_rot += 0.5 * p.reload_k
	if p.switch_t > 0:
		gun_rot += 1.1 * sin(PI * clampf(p.switch_t / 0.22, 0, 1))
	var mk := clampf(1.0 - p.melee_anim / 0.28, 0, 1) if p.melee_anim > 0 else -1.0
	if mk >= 0:
		gun_rot += 0.7 * sin(mk * PI)''', '''	var mk := clampf(1.0 - p.melee_anim / 0.28, 0, 1) if p.melee_anim > 0 else -1.0
	var busy := "melee" if mk >= 0 else ("swap" if p.switch_t > 0 else ("reload" if p.reload_k > 0.01 else ""))
	if busy == "melee":
		gun_rot += 0.7 * sin(mk * PI)
	elif busy == "swap":
		gun_rot += 1.1 * sin(PI * clampf(p.switch_t / 0.22, 0, 1))
	elif busy == "reload":
		gun_rot += 0.5 * p.reload_k''')
rep('''	if p.muzzle_t > 0 and gun != "rpg" and not ["laser", "shock", "net", "flame"].has(gun):''',
    '''	if p.muzzle_t > 0 and busy == "" and gun != "rpg" and not ["laser", "shock", "net", "flame"].has(gun):''')
# respawn: fade in through the drop beam first, then a calm shield glow (no hard flicker on top)
rep('''	if p.protect_t > 0:
		tint.a = 0.45 + 0.4 * absf(sin(time_s * 10.0))''', '''	if p.protect_t > 0 and bage >= 0.6:
		tint.a = 0.8 + 0.2 * sin(time_s * 6.0)''')
rep('''	if p.protect_t > 0:
		draw_arc(Vector2(0, -4), 30, 0, TAU, 40, Color(0.5, 0.9, 1.0, 0.25), 2.0, true)''', '''	if p.protect_t > 0 and (bage >= 0.45 or bage < 0.0 or p.actor):
		draw_arc(Vector2(0, -4), 30, 0, TAU, 40, Color(0.5, 0.9, 1.0, 0.25), 2.0, true)''')
# no shooting in the middle of a gun swap or a knife swing; no shooting while still dropping in
rep('''	if want_fire and w != null and p.reload_t <= 0''', '''	if p.melee_anim > 0.05 or p.switch_t > 0.06 or t - p.born_srv < 0.45:
		want_fire = false
	if want_fire and w != null and p.reload_t <= 0''')
rep('\tvar shoot_buf := 0.0\n', '\tvar shoot_buf := 0.0\n\tvar born_srv := -9.0\n')
if ERR:
    print("\n".join(ERR)); sys.exit(1)
open(P, "w").write(s)
print("ok")
