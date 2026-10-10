"""Open the artifact folder in headless Chrome, wait for the game, click Start, screenshot."""
import sys, threading, http.server, functools, time
from playwright.sync_api import sync_playwright

ROOT = sys.argv[1]
OUT = sys.argv[2]
handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT)
handler.log_message = lambda *a: None
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 8765), handler)
threading.Thread(target=srv.serve_forever, daemon=True).start()
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/google/chrome/chrome", args=["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
    pg = b.new_page(viewport={"width": 1280, "height": 720})
    logs = []
    pg.on("console", lambda m: logs.append(m.type + ": " + m.text))
    pg.on("pageerror", lambda e: logs.append("pageerror: " + str(e)))
    pg.goto("http://127.0.0.1:8765/index.html")
    for i in range(60):
        time.sleep(1)
        if pg.evaluate("document.getElementById('load').hidden") or not pg.evaluate("document.getElementById('err').hidden"):
            break
    time.sleep(3)
    pg.screenshot(path=OUT + "_menu.png")
    pg.mouse.click(640, 572)
    time.sleep(6)
    pg.keyboard.down("KeyD"); pg.keyboard.down("KeyW"); time.sleep(1.2); pg.keyboard.up("KeyW"); time.sleep(0.6); pg.keyboard.up("KeyD")
    pg.mouse.move(900, 300); pg.mouse.down(); time.sleep(0.8); pg.mouse.up()
    pg.screenshot(path=OUT + "_play.png")
    print("error box:", pg.evaluate("document.getElementById('err').textContent"))
    for l in logs[-15:]:
        print(l[:200])
    b.close()
srv.shutdown()
