"""v1.2 part 2: replay-based prediction (input numbers echoed by the server)."""
import sys
p='/home/claude/skysquad/main.gd'; s=open(p).read()
def rep(a,b,c=1):
    global s
    if s.count(a)!=c: sys.exit("expected %d got %d: %r" % (c, s.count(a), a[:100]))
    s=s.replace(a,b)
start=s.index("# your own soldier moves at once on your phone")
end=s.index("# ---------- the no-screen room server ----------")
new=open('/home/claude/scripts/predict_block.gd').read()
s=s[:start]+new+s[end:]
rep('''var pred_err := 0.0''','''var pred_err := 0.0
var pred_hist: Array = []
var pred_off := Vector2.ZERO
var in_seq := 0''')
rep('''		var pkt := [i2.mx, i2.fly, i2.shoot, i2.swap, i2.grenade, i2.melee, i2.reload, me.aim, i2.down, i2.pick, i2.zoom, i2.bomb, i2.smoke]''','''		in_seq += 1
		var pkt := [i2.mx, i2.fly, i2.shoot, i2.swap, i2.grenade, i2.melee, i2.reload, me.aim, i2.down, i2.pick, i2.zoom, i2.bomb, i2.smoke, in_seq]''')
rep('''			inp.smoke = a.size() > 12 and bool(a[12])''','''			inp.smoke = a.size() > 12 and bool(a[12])
			if a.size() > 13:
				p.ack = maxi(p.ack, int(a[13]))''')
rep('\tvar svx := 0.0\n','\tvar svx := 0.0\n\tvar ack := 0\n')
rep('''const PF_N := 32''','''const PF_N := 33''')
rep('''			p.hs, p.best, p.mk, p.bk, p.lstreak, p.spin, maxf(p.burn_t, 0.0), p.smokes])''','''			p.hs, p.best, p.mk, p.bk, p.lstreak, p.spin, maxf(p.burn_t, 0.0), p.smokes, p.ack])''')
rep('''		p.smokes = int(pf[o + 31])''','''		p.smokes = int(pf[o + 31])
		if mine and p.alive and was_alive and snaps_got > 1:
			reconcile_me(p, int(pf[o + 32]), fl)
		elif mine:
			pred_hist.clear()
			pred_off = Vector2.ZERO''')
rep('''			p.peer_id = id
			p.remote = true
			p.bot = false
			p.dropped = false''','''			p.peer_id = id
			p.remote = true
			p.bot = false
			p.dropped = false
			p.ack = 0''')
open(p,'w').write(s)
print("ok")
