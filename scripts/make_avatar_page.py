"""Avatar picker page: every option as a card, grouped by category, multi-pick, copy picks."""
import base64, json, sys
src, out = sys.argv[1], sys.argv[2]
L = json.load(open(f"{src}/list.json"))
for it in L:
    it["img"] = "data:image/png;base64," + base64.b64encode(open(f"{src}/{it['file']}.png", "rb").read()).decode()
CATS = [("set", "Full looks", "Complete characters, ready to wear. Pick any you'd like as presets."),
        ("helmet", "Helmets & hats", "What sits on the head."),
        ("face", "Face", "Eyes, masks and marks."),
        ("outfit", "Outfits", "Body and legs."),
        ("jetpack", "Jetpacks", "What's on the back."),
        ("extra", "Extras", "Little add-ons that show off."),
        ("flame", "Jet flame colour", "The colour of your jet fire.")]
html = """<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sky Squad Locker</title>
<style>
:root{--bg:#0f1426;--card:#18203a;--line:#2a3558;--txt:#eef1fb;--mut:#9aa6c8;--gold:#ffc83d;--goldt:#2a2000}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#0f1426}}
:root[data-theme="dark"]{--bg:#0f1426}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--txt);font:15px/1.45 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;padding:0 16px 110px}
.wrap{max-width:1100px;margin:0 auto}
h1{font-size:30px;margin:28px 0 4px;letter-spacing:-.5px}h1 span{color:var(--gold)}
.lead{color:var(--mut);margin:0 0 8px}
h2{font-size:20px;margin:34px 0 2px}h2 small{color:var(--mut);font-weight:500;font-size:13px;margin-left:8px}
.sub{color:var(--mut);font-size:13px;margin:0 0 12px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px}
.c{background:var(--card);border:2px solid var(--line);border-radius:14px;padding:8px 8px 10px;cursor:pointer;transition:transform .15s,border-color .15s;text-align:center;user-select:none}
.c:hover{transform:translateY(-2px)}
.c img{width:100%;aspect-ratio:264/296;image-rendering:auto;display:block;border-radius:10px;background:radial-gradient(circle at 50% 40%,#26315a,#151b33)}
.c b{display:block;font-size:13px;margin-top:6px;font-weight:600}
.c i{display:block;font-style:normal;font-size:11px;color:var(--mut)}
.c.on{border-color:#ffc83d;background:#2a2a24;box-shadow:0 0 0 3px rgba(255,200,61,.3)}
.c.on b::after{content:" ✓";color:var(--gold)}
.bar{position:fixed;left:0;right:0;bottom:0;background:rgba(10,14,28,.96);border-top:1px solid var(--line);padding:12px 16px}
.bar .in{max-width:1100px;margin:0 auto;display:flex;gap:12px;align-items:center}
#sum{flex:1;font-size:13px;color:var(--mut);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
button{background:var(--gold);color:var(--goldt);border:0;border-radius:10px;padding:11px 18px;font-weight:700;font-size:14px;cursor:pointer}
button.ghost{background:transparent;color:var(--mut);border:1px solid var(--line)}
</style></head><body><div class="wrap">
<h1>Sky Squad <span>Locker</span></h1>
<p class="lead">Avatar options for the game. Tap every card you like (pick as many as you want in each group), then press <b>Copy my picks</b> and paste it to me. Everything you pick becomes something players can equip in a new Locker screen, and other players see your look in LAN games.</p>
<div id="root"></div></div>
<div class="bar"><div class="in"><div id="sum">Nothing picked yet</div><button class="ghost" id="clr">Clear</button><button id="cp">Copy my picks</button></div></div>
<script>
const L=__L__, CATS=__C__;
const picked=new Set();
const root=document.getElementById('root');
for(const [cat,title,sub] of CATS){
  const items=L.filter(x=>x.cat===cat); if(!items.length) continue;
  const h=document.createElement('h2'); h.innerHTML=title+'<small>'+items.length+' options</small>'; root.appendChild(h);
  const p=document.createElement('p'); p.className='sub'; p.textContent=sub; root.appendChild(p);
  const g=document.createElement('div'); g.className='grid'; root.appendChild(g);
  for(const it of items){
    const c=document.createElement('div'); c.className='c';
    const id=cat+':'+it.key;
    c.innerHTML='<img alt="" src="'+it.img+'"><b></b><i></i>';
    c.querySelector('b').textContent=it.label; c.querySelector('i').textContent=it.key;
    c.onclick=()=>{picked.has(id)?picked.delete(id):picked.add(id);c.classList.toggle('on');upd();};
    g.appendChild(c);
  }
}
function text(){
  const parts=[];
  for(const [cat,title] of CATS){const ks=[...picked].filter(x=>x.startsWith(cat+':')).map(x=>x.split(':')[1]); if(ks.length) parts.push(title+': '+ks.join(', '));}
  return parts.length?'My avatar picks: '+parts.join(' / '):'';
}
function upd(){document.getElementById('sum').textContent=picked.size?picked.size+' picked — '+text().replace('My avatar picks: ',''):'Nothing picked yet';}
document.getElementById('cp').onclick=async()=>{const t=text(); if(!t) return; try{await navigator.clipboard.writeText(t);}catch(e){const a=document.createElement('textarea');a.value=t;document.body.appendChild(a);a.select();try{document.execCommand('copy')}catch(_){};a.remove();} const b=document.getElementById('cp'); b.textContent='Copied!'; setTimeout(()=>b.textContent='Copy my picks',1400);};
document.getElementById('clr').onclick=()=>{picked.clear();document.querySelectorAll('.c.on').forEach(c=>c.classList.remove('on'));upd();};
</script></body></html>"""
html = html.replace("__L__", json.dumps(L)).replace("__C__", json.dumps(CATS))
open(out, "w").write(html)
print(len(html))
