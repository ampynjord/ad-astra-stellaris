#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ad Astra - explorateur du contenu vanilla (batiments + technos).

Produit une page HTML autonome : filtres, recherche, tri, et surtout la colonne
de statut qui dit, pour chaque entree, ou elle en est vis-a-vis du mod.
"""
import json
import os

DATA = json.load(open("/tmp/inv.json", encoding="utf-8"))
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "art", "inventaire_stellaris.html")

STATUS_B = {
    "candidate": ("À masquer ?", "Empire normal, aucun prérequis technologique : constructible dès l'Âge de pierre."),
    "covered":   ("Déjà couvert", "Verrouillé par sa techno, elle-même gatée par le mod."),
    "special":   ("Hors sujet", "Empire déchu, succursale, primitif, événement, nature sauvage… inatteignable normalement."),
    "mod":       ("Ad Astra", "Bâtiment d'époque ajouté par le mod."),
}
STATUS_T = {
    "gated":  ("Verrouillée", "Gatée par le mod sur un âge précis."),
    "start":  ("Départ libre", "Techno de départ non gatée par le mod — à vérifier."),
    "free":   ("Non gatée", "Hors périmètre du mod (tier 3+ ou prérequis profonds)."),
    "mod":    ("Ad Astra", "Techno d'époque ajoutée par le mod."),
}

HTML = """<!doctype html>
<html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Ad Astra — inventaire Stellaris 4.4</title>
<style>
:root{
  --bg:#080b18; --panel:#0f1428; --panel2:#141a33; --line:#232b4d;
  --ink:#e8edfb; --muted:#93a3c9; --gold:#e8b451; --gold-hi:#f6d89a;
  --cand:#ff9f4a; --cov:#4ec9a4; --spec:#5f6d97; --mod:#e8b451; --free:#7c88ad;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
  font:14px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
header{padding:26px 28px 18px;border-bottom:1px solid var(--line);
  background:linear-gradient(180deg,#0d1226 0%,transparent 100%)}
h1{margin:0;font:600 22px/1.2 Georgia,"Times New Roman",serif;letter-spacing:.10em;
  color:var(--gold-hi);text-transform:uppercase}
.sub{color:var(--muted);margin-top:6px;font-size:13px}
.wrap{padding:20px 28px 60px;max-width:1500px;margin:0 auto}
.tabs{display:flex;gap:8px;margin:18px 0 16px}
.tab{padding:9px 18px;border:1px solid var(--line);background:var(--panel);
  color:var(--muted);border-radius:8px;cursor:pointer;font-weight:600;font-size:13px}
.tab.on{background:var(--panel2);color:var(--gold-hi);border-color:#3a4570}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin-bottom:16px}
.tile{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:12px 14px}
.tile .n{font:600 24px/1.1 Georgia,serif}
.tile .l{color:var(--muted);font-size:12px;margin-top:3px}
.tile.b-candidate .n{color:var(--cand)} .tile.b-covered .n{color:var(--cov)}
.tile.b-special .n{color:var(--spec)} .tile.b-mod .n{color:var(--mod)}
.tile.b-gated .n{color:var(--cov)} .tile.b-start .n{color:var(--cand)}
.tile.b-free .n{color:var(--free)}
.filters{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:14px}
input[type=search],select{background:var(--panel);border:1px solid var(--line);color:var(--ink);
  padding:8px 11px;border-radius:8px;font-size:13px;outline:none}
input[type=search]{min-width:250px}
input[type=search]:focus,select:focus{border-color:var(--gold)}
.chip{padding:6px 12px;border-radius:20px;border:1px solid var(--line);background:var(--panel);
  color:var(--muted);cursor:pointer;font-size:12px;font-weight:600}
.chip.on{color:#0a0d1a;background:var(--gold);border-color:var(--gold)}
table{width:100%;border-collapse:collapse;font-size:13px}
th{position:sticky;top:0;background:var(--panel2);text-align:left;padding:9px 10px;
  border-bottom:1px solid var(--line);cursor:pointer;color:var(--muted);
  font-size:11px;text-transform:uppercase;letter-spacing:.06em;white-space:nowrap}
th:hover{color:var(--gold-hi)}
td{padding:8px 10px;border-bottom:1px solid #171d38;vertical-align:top}
tr:hover td{background:#111730}
.key{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;color:var(--muted)}
.badge{display:inline-block;padding:2px 9px;border-radius:11px;font-size:11px;font-weight:700;white-space:nowrap}
.s-candidate{background:rgba(255,159,74,.16);color:var(--cand)}
.s-covered{background:rgba(78,201,164,.14);color:var(--cov)}
.s-special{background:rgba(95,109,151,.18);color:var(--spec)}
.s-mod{background:rgba(232,180,81,.16);color:var(--mod)}
.s-gated{background:rgba(78,201,164,.14);color:var(--cov)}
.s-start{background:rgba(255,159,74,.16);color:var(--cand)}
.s-free{background:rgba(124,136,173,.16);color:var(--free)}
.age{color:var(--gold-hi)}
.count{color:var(--muted);font-size:12px;margin:10px 0}
.legend{color:var(--muted);font-size:12px;margin:14px 0 0;line-height:1.7}
.legend b{color:var(--ink)}
.hidden{display:none}
</style></head><body>
<header>
  <h1>Ad Astra — inventaire Stellaris 4.4</h1>
  <div class="sub">Tout le contenu du jeu de base, classé par ce que le mod en fait. __STAMP__</div>
</header>
<div class="wrap">
  <div class="tabs">
    <div class="tab on" data-tab="b">Bâtiments <span id="cb"></span></div>
    <div class="tab" data-tab="t">Technologies <span id="ct"></span></div>
  </div>
  <div id="tiles" class="tiles"></div>
  <div class="filters">
    <input type="search" id="q" placeholder="Rechercher un nom ou une clé…">
    <select id="f1"></select>
    <select id="f2"></select>
    <span id="chips"></span>
  </div>
  <div class="count" id="count"></div>
  <table><thead><tr id="head"></tr></thead><tbody id="body"></tbody></table>
  <div class="legend" id="legend"></div>
</div>
<script>
const DATA = __DATA__;
const META = __META__;
let tab='b', sortCol=null, sortDir=1, status=null;

const COLS={
 b:[['Nom',1],['Clé',0],['Famille',2],['Catégorie',3],['Prérequis',5],['Statut',6]],
 t:[['Nom',1],['Clé',0],['Domaine',2],['Tier',3],['Catégorie',4],['Coût',5],['Âge Ad Astra',6],['Statut',7]]
};
const STATUS={b:META.statusB,t:META.statusT};
const SIDX={b:6,t:7};

function rows(){return tab==='b'?DATA.b:DATA.t}
function tiles(){
  const s={}, idx=SIDX[tab];
  rows().forEach(r=>s[r[idx]]=(s[r[idx]]||0)+1);
  const order=tab==='b'?['candidate','covered','special','mod']:['gated','start','free','mod'];
  document.getElementById('tiles').innerHTML=order.filter(k=>s[k]).map(k=>
    `<div class="tile b-${k}" data-s="${k}"><div class="n">${s[k]}</div>
     <div class="l">${STATUS[tab][k][0]}</div></div>`).join('');
  document.querySelectorAll('.tile').forEach(el=>el.onclick=()=>{
    status = status===el.dataset.s?null:el.dataset.s; draw();});
  document.getElementById('legend').innerHTML=order.map(k=>
    `<div><b>${STATUS[tab][k][0]}</b> — ${STATUS[tab][k][1]}</div>`).join('');
}
function fillFilters(){
  const mk=(sel,idx,label)=>{
    const vals=[...new Set(rows().map(r=>r[idx]).filter(v=>v!==''&&v!==undefined))].sort();
    sel.innerHTML=`<option value="">${label}</option>`+vals.map(v=>
      `<option value="${v}">${idx===6&&tab==='t'?(META.ageFr[v]||v):v}</option>`).join('');
    sel.dataset.idx=idx;
  };
  const f1=document.getElementById('f1'), f2=document.getElementById('f2');
  if(tab==='b'){mk(f1,2,'Toutes les familles');mk(f2,3,'Toutes les catégories');}
  else{mk(f1,2,'Tous les domaines');mk(f2,6,'Tous les âges');}
  f1.value='';f2.value='';
}
function draw(){
  const q=document.getElementById('q').value.toLowerCase();
  const f1=document.getElementById('f1'), f2=document.getElementById('f2');
  const idx=SIDX[tab];
  let rs=rows().filter(r=>{
    if(status&&r[idx]!==status)return false;
    if(f1.value&&String(r[+f1.dataset.idx])!==f1.value)return false;
    if(f2.value&&String(r[+f2.dataset.idx])!==f2.value)return false;
    if(q&&!(String(r[1]).toLowerCase().includes(q)||String(r[0]).toLowerCase().includes(q)))return false;
    return true;});
  if(sortCol!==null){
    rs=rs.slice().sort((a,b)=>{
      const x=a[sortCol],y=b[sortCol];
      return (typeof x==='number'&&typeof y==='number'?x-y:String(x).localeCompare(String(y)))*sortDir;});
  }
  document.getElementById('head').innerHTML=COLS[tab].map((c,i)=>
    `<th data-c="${c[1]}">${c[0]}${sortCol===c[1]?(sortDir>0?' ▲':' ▼'):''}</th>`).join('');
  document.querySelectorAll('#head th').forEach(th=>th.onclick=()=>{
    const c=+th.dataset.c; sortDir=(sortCol===c)?-sortDir:1; sortCol=c; draw();});
  document.getElementById('body').innerHTML=rs.slice(0,900).map(r=>{
    const st=r[idx], b=`<span class="badge s-${st}">${STATUS[tab][st][0]}</span>`;
    if(tab==='b')return `<tr><td>${r[1]}</td><td class="key">${r[0]}</td><td>${r[2]}</td>
      <td>${r[3]||'—'}</td><td class="key">${r[5]||'—'}</td><td>${b}</td></tr>`;
    return `<tr><td>${r[1]}</td><td class="key">${r[0]}</td><td>${r[2]||'—'}</td>
      <td>${r[3]<0?'—':r[3]}</td><td>${r[4]||'—'}</td><td>${r[5]||'—'}</td>
      <td class="age">${r[6]?(META.ageFr[r[6]]||r[6]):'—'}</td><td>${b}</td></tr>`;}).join('');
  document.getElementById('count').textContent=
    `${rs.length} entrée(s)`+(rs.length>900?' — 900 affichées':'')+(status?` · filtre : ${STATUS[tab][status][0]}`:'');
}
document.querySelectorAll('.tab').forEach(el=>el.onclick=()=>{
  document.querySelectorAll('.tab').forEach(t=>t.classList.remove('on'));
  el.classList.add('on'); tab=el.dataset.tab; status=null; sortCol=null;
  fillFilters(); tiles(); draw();});
['q','f1','f2'].forEach(id=>document.getElementById(id).addEventListener('input',draw));
document.getElementById('cb').textContent='('+DATA.b.length+')';
document.getElementById('ct').textContent='('+DATA.t.length+')';
fillFilters(); tiles(); draw();
</script></body></html>"""


def main():
    meta = {"ageFr": DATA["ageFr"], "statusB": STATUS_B, "statusT": STATUS_T}
    html = (HTML.replace("__DATA__", json.dumps({"b": DATA["b"], "t": DATA["t"]},
                                                ensure_ascii=False, separators=(",", ":")))
                .replace("__META__", json.dumps(meta, ensure_ascii=False))
                .replace("__STAMP__", "%d bâtiments · %d technologies"
                         % (len(DATA["b"]), len(DATA["t"]))))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)
    print("ecrit : %s (%.0f Ko)" % (OUT, os.path.getsize(OUT) / 1024))


if __name__ == "__main__":
    main()
