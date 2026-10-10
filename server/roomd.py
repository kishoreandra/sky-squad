#!/usr/bin/env python3
"""Sky Squad room finder. Phones ask "where is room TIGER42?" on UDP port 24870.
Each room is its own copy of the game running with no screen, on its own UDP port (25001-25040).
Rooms close themselves when everyone has left for 90 seconds.

  python3 roomd.py --godot ./godot --pack ./skysquad.pck --version 1.2
"""
import argparse, os, re, socket, subprocess, sys, time

ap = argparse.ArgumentParser()
ap.add_argument("--godot", required=True, help="path to the Godot program")
ap.add_argument("--pack", required=True, help="path to skysquad.pck")
ap.add_argument("--version", required=True, help="game version the server runs, e.g. 1.2")
ap.add_argument("--port", type=int, default=24870)
ap.add_argument("--first-room-port", type=int, default=25001)
ap.add_argument("--max-rooms", type=int, default=12)
ap.add_argument("--extra", default="", help="extra switches passed to every room (for tests)")
a = ap.parse_args()

CODE = re.compile(r"^[A-Z0-9]{4,8}$")
rooms = {}          # code -> {"port": int, "proc": Popen, "start": float}

def log(*m):
    print(time.strftime("%H:%M:%S"), *m, flush=True)

def clean():
    for code in list(rooms):
        if rooms[code]["proc"].poll() is not None:
            log("room", code, "closed")
            del rooms[code]

def free_port():
    used = {r["port"] for r in rooms.values()}
    for p in range(a.first_room_port, a.first_room_port + a.max_rooms):
        if p not in used:
            return p
    return None

def open_room(code):
    port = free_port()
    if port is None:
        return None
    cmd = [a.godot, "--headless", "--main-pack", a.pack, "--", "--dedicated", f"--port={port}", f"--room={code}"]
    cmd += a.extra.split() if a.extra else []
    logf = open(os.path.join(os.path.dirname(os.path.abspath(a.pack)), f"room-{code}.log"), "w")
    proc = subprocess.Popen(cmd, stdout=logf, stderr=subprocess.STDOUT)
    rooms[code] = {"port": port, "proc": proc, "start": time.time()}
    log("room", code, "opened on port", port)
    return port

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", a.port))
log(f"Sky Squad room finder v{a.version} listening on UDP {a.port}")
while True:
    data, addr = sock.recvfrom(512)
    try:
        bits = data.decode("utf-8", "replace").split("|")
        if len(bits) != 4 or bits[0] != "SKYROOM?":
            continue
        mode, code, ver = bits[1], bits[2].upper(), bits[3]
        if not CODE.match(code):
            continue
        clean()
        if ver != a.version:
            status, port = "old", 0
        elif code in rooms:
            status, port = "ok", rooms[code]["port"]
        elif mode == "join":
            status, port = "none", 0
        else:
            port = open_room(code)
            status = "ok" if port else "full"
            port = port or 0
        sock.sendto(f"SKYROOM!|{code}|{port}|{status}".encode(), addr)
    except Exception as e:  # never let one bad packet stop the server
        log("error:", e)
