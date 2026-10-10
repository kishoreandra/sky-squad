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
	var acc := 1100.0 if p.on_ground else 520.0
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

