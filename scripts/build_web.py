"""Turn Godot's web export into an artifact-ready folder: split the 35 MB wasm into parts
and write a page that rejoins them while loading."""
import json, os, re, shutil, sys

SRC = sys.argv[1]          # godot web export folder (index.html, index.js, index.wasm, index.pck)
OUT = sys.argv[2]          # artifact folder
VERSION = sys.argv[3] if len(sys.argv) > 3 else "0.2"
PART = 12 * 1024 * 1024

shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(OUT)
wasm = open(os.path.join(SRC, "index.wasm"), "rb").read()
parts = []
for i in range(0, len(wasm), PART):
    name = f"engine{len(parts)}.wasm"
    open(os.path.join(OUT, name), "wb").write(wasm[i:i + PART])
    parts.append(name)
shutil.copy(os.path.join(SRC, "index.pck"), os.path.join(OUT, "game.wasm"))
shutil.copy(os.path.join(SRC, "index.js"), os.path.join(OUT, "index.js"))
shutil.copy(os.path.join(SRC, "index.audio.worklet.js"), os.path.join(OUT, "index.audio.worklet.js"))

html = open(os.path.join(SRC, "index.html")).read()
cfg = json.loads(re.search(r"GODOT_CONFIG = (\{.*?\});", html).group(1))
cfg["ensureCrossOriginIsolationHeaders"] = False
cfg["fileSizes"] = {"index.pck": os.path.getsize(os.path.join(OUT, "game.wasm")), "index.wasm": len(wasm)}
cfg["canvasResizePolicy"] = 2

page = """<title>Sky Squad</title>
<style>
/* Full-screen game canvas with a loading card. Single dark arcade look. */
:root{--bg:#0a0c22;--panel:#141842;--line:#2b3170;--ink:#eef0ff;--muted:#a3a9db;--arc:#ffd84a;--red:#ff6b7f;color-scheme:dark}
html,body{height:100%;margin:0;background:var(--bg);color:var(--ink);overflow:hidden;font-family:system-ui,-apple-system,'Segoe UI',sans-serif;touch-action:none;-webkit-user-select:none;user-select:none}
#canvas{position:fixed;left:0;top:env(safe-area-inset-top,0px);width:100%;height:calc(100% - env(safe-area-inset-top,0px) - env(safe-area-inset-bottom,0px));display:block;outline:none}
#load{position:fixed;inset:0;display:flex;align-items:center;justify-content:center;padding:16px;background:var(--bg)}
.card{width:100%;max-width:420px;background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:22px 20px;display:flex;flex-direction:column;gap:12px;box-sizing:border-box}
.eyebrow{font-size:12px;letter-spacing:.14em;color:#5ef0ff;font-weight:600;text-transform:uppercase}
h1{margin:0;font-size:36px;color:var(--arc);letter-spacing:.02em}
.bar{height:10px;background:#0a0c22;border-radius:6px;overflow:hidden}
.bar i{display:block;height:100%;width:0;background:var(--arc);transition:width .2s}
p{margin:0;font-size:14px;line-height:1.5;color:var(--muted)}
#err{color:var(--red)}
[hidden]{display:none!important}
</style>
<canvas id="canvas" tabindex="0">Your browser can't run this game.</canvas>
<div id="load"><div class="card">
  <div class="eyebrow">Arc Light Studio &middot; Build __VER__</div>
  <h1>SKY SQUAD</h1>
  <div class="bar"><i id="fill"></i></div>
  <p id="msg">Loading the game (about 36 MB, first time only takes a bit)...</p>
  <p id="err" hidden></p>
  <p>Keyboard: A/D move, W or Space fly, mouse to aim and shoot, G grenade, F melee, Q swap, R reload. On a phone, turn it sideways and use your thumbs.</p>
</div></div>
<script>
const PARTS=__PARTS__;
const realFetch=window.fetch.bind(window);
window.fetch=async(input,init)=>{
  const url=typeof input==='string'?input:(input&&input.url)||'';
  if(url.endsWith('index.wasm')){
    const bufs=await Promise.all(PARTS.map(p=>realFetch(p).then(r=>{if(!r.ok)throw new Error('Could not load '+p+' ('+r.status+')');return r.arrayBuffer();})));
    const blob=new Blob(bufs,{type:'application/wasm'});
    return new Response(blob,{status:200,headers:{'Content-Type':'application/wasm','Content-Length':String(blob.size)}});
  }
  if(url.endsWith('index.pck'))return realFetch("game.wasm",init);
  return realFetch(input,init);
};
</script>
<script src="index.js"></script>
<script>
const GODOT_CONFIG=__CFG__;
const fill=document.getElementById('fill'),msg=document.getElementById('msg'),err=document.getElementById('err');
function fail(e){err.hidden=false;err.textContent='The game could not start: '+(e&&e.message?e.message:e)+'. Try reloading the page.';msg.hidden=true;document.getElementById('load').hidden=false;}
try{
  const engine=new Engine(GODOT_CONFIG);
  let shown=false;
  const show=()=>{if(shown)return;shown=true;document.getElementById('load').hidden=true;document.getElementById('canvas').focus();};
  engine.startGame({
    onProgress:(cur,total)=>{if(total>0){fill.style.width=Math.round(cur/total*100)+'%';if(cur>=total){msg.textContent='Starting...';setTimeout(show,1500);}}},
    onPrint:(...a)=>{console.log(...a);if(String(a[0]).startsWith('Godot Engine'))setTimeout(show,300);}
  }).then(show).catch(fail);
}catch(e){fail(e);}
</script>
"""
page = page.replace("__PARTS__", json.dumps(parts)).replace("__CFG__", json.dumps(cfg)).replace("__VER__", VERSION)
open(os.path.join(OUT, "index.html"), "w").write(page)
print("parts", parts, "pck", cfg["fileSizes"]["index.pck"])
