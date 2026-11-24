#!/usr/bin/env python3
"""Generate docs/index.html from addons.json: every addon on one page, grouped by category."""
import html, json, pathlib
from collections import defaultdict

root = pathlib.Path(__file__).resolve().parent.parent
data = json.loads((root / "addons.json").read_text(encoding="utf-8"))
esc = lambda s: html.escape(str(s or ""), quote=True)
groups = defaultdict(list)
for a in data["addons"]:
    groups[a["category"]].append(a)

def card(a):
    ok = a["status"] == "published"
    proj = esc(a["blobProject"])
    links = (f'<a href="https://blob.build/project/{proj}/{esc(a["channel"])}">Blob Builds</a>'
             f'<a href="https://pack.drakescraft.cl/builds/">Mirror</a>') if ok else '<span class="wait">not published yet</span>'
    author = esc(a.get("author") or "DrakesCraft Labs")
    q = esc((a["name"] + " " + a["description"] + " " + author + " " + a["category"]).lower())
    return (f'<article class="card" data-q="{q}"><h3>{esc(a["name"])}</h3><p>{esc(a["description"])}</p>'
            f'<div class="meta"><span class="v">MC {esc(data["minecraft"])}</span><span>by {author}</span></div>'
            f'<div class="links">{links}<a href="https://github.com/SlimefunNewHorizons/{esc(a["repo"])}">Source</a></div></article>')

order = sorted(groups, key=lambda c: (c in ("Drakes Suite", "Libraries & Core", "Multiverse (by Chagui68)"), c))
sections = []
for c in order:
    items = sorted(groups[c], key=lambda x: x["name"].lower())
    sections.append(f'<section data-cat="1"><h2>{esc(c)} <small>{len(items)}</small></h2><div class="grid">' + "".join(card(i) for i in items) + "</div></section>")
total = len(data["addons"])
page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Slimefun 6 addons for Minecraft {esc(data['minecraft'])}</title>
<style>
:root{{color-scheme:dark}}*{{box-sizing:border-box}}body{{margin:0;font:15px system-ui,sans-serif;background:#0b0f17;color:#e6edf6}}
main{{max-width:1100px;margin:0 auto;padding:28px 20px 60px}}h1{{margin:0 0 4px}}p.lead{{color:#9fb0c5;margin:0}}
input{{width:100%;padding:11px 13px;margin:18px 0 6px;border-radius:9px;border:1px solid #2a3a50;background:#111826;color:inherit;font-size:15px}}
h2{{margin:28px 0 12px;font-size:1.15rem;color:#7dd3fc}}h2 small{{color:#6b7f99;font-weight:400;margin-left:6px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px}}
.card{{background:#101826;border:1px solid #1d2a3d;border-radius:12px;padding:14px;display:flex;flex-direction:column;gap:8px;min-width:0}}
.card h3{{margin:0;font-size:1rem;overflow-wrap:anywhere}}.card p{{margin:0;color:#aab8cb;font-size:.88rem;line-height:1.45;flex:1}}
.meta{{display:flex;gap:10px;flex-wrap:wrap;color:#6b7f99;font-size:.8rem}}.v{{color:#4ade80}}
.links{{display:flex;gap:12px;flex-wrap:wrap;font-size:.88rem}}a{{color:#7dd3fc;text-decoration:none}}a:hover{{text-decoration:underline}}.wait{{color:#fbbf24}}
</style></head><body><main>
<h1>Slimefun 6 addons</h1>
<p class="lead">{total} addons maintained by DrakesCraft Labs and running on Minecraft {esc(data['minecraft'])}. Every build passes the ABI gate before it is published. Builds mirror: <a href="https://pack.drakescraft.cl/builds/">pack.drakescraft.cl/builds</a> · Maven: <a href="https://maven.drakescraft.cl">maven.drakescraft.cl</a></p>
<input id="q" placeholder="Search addons..." autofocus>
{"".join(sections)}
<script>q.oninput=()=>{{const v=q.value.toLowerCase();document.querySelectorAll('.card').forEach(c=>c.hidden=!c.dataset.q.includes(v));document.querySelectorAll('section').forEach(s=>s.hidden=![...s.querySelectorAll('.card')].some(c=>!c.hidden))}}</script>
</main></body></html>"""
(root / "docs").mkdir(exist_ok=True)
(root / "docs" / "index.html").write_text(page, encoding="utf-8")
print("addons", total, "categories", len(groups))
