"""v1.7 part A: no grabbing guns through walls."""
import sys
P = "/home/claude/skysquad/main.gd"
s = open(P).read()
ERR = []
def rep(a, b, c=1):
    global s
    if s.count(a) != c:
        ERR.append("expected %d got %d: %r" % (c, s.count(a), a[:120])); return
    s = s.replace(a, b)

rep('''			var d := Vector2(k.x + k.w / 2.0 - c.x, (k.y + k.h / 2.0 - c.y) * 0.7).length()
			if d < bd:''', '''			var d := Vector2(k.x + k.w / 2.0 - c.x, (k.y + k.h / 2.0 - c.y) * 0.7).length()
			if d < bd and reach_ok(c, k):''')
rep('''	if p.near_k != null and pickups.has(p.near_k) and t - p.near_t < 1.6 and Vector2(p.near_k.x - c.x, p.near_k.y - c.y).length() < 150:''',
    '''	if p.near_k != null and pickups.has(p.near_k) and t - p.near_t < 0.4 and Vector2(p.near_k.x - c.x, p.near_k.y - c.y).length() < 70 and reach_ok(c, p.near_k):''')
rep('''			if overlaps(p, k) and not human_choice and try_pickup(p, k):''', '''			if overlaps(p, k) and not human_choice and reach_ok(center(p), k) and try_pickup(p, k):''')
# a dropped gun never goes inside a wall or to the other side of one
rep('''		if free and not rect_hits(x + off, y, 24, 16):''', '''		if free and not rect_hits(x + off, y, 24, 16) and los(Vector2(x, y + 8), Vector2(x + off + 12, y + 8)):''')
rep('''			pickups.append(make_pickup("drop", x + off, y, type, ammo))
			return
	pickups.append(make_pickup("drop", x, y, type, ammo))''', '''			pickups.append(make_pickup("drop", x + off, y, type, ammo))
			return
	var yy := y
	for _i in 12:
		if not rect_hits(x, yy, 24, 16):
			break
		yy -= gsign() * T * 0.5
	pickups.append(make_pickup("drop", x, yy, type, ammo))''')
s += '''
# you can only take an item you can actually reach: not inside a wall and not behind one
func reach_ok(c: Vector2, k: Pickup) -> bool:
	if rect_hits(k.x + 3, k.y + 3, k.w - 6, k.h - 6):
		return false
	return los(c, Vector2(k.x + k.w / 2.0, k.y + k.h / 2.0))
'''
if ERR:
    print("\n".join(ERR)); sys.exit(1)
open(P, "w").write(s)
print("ok")
