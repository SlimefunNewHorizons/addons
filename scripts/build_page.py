#!/usr/bin/env python3
"""Generate docs/index.html from addons.json (single page listing every addon)."""
import html, json, pathlib

root = pathlib.Path(__file__).resolve().parent.parent
data = json.loads((root / "addons.json").read_text(encoding="utf-8"))
rows = []
for a in sorted(data["addons"], key=lambda x: x["name"].lower()):
    name = html.escape(a["name"])
    proj = html.escape(a["blobProject"], quote=True)
    repo = html.escape(a["repo"], quote=True)
    author = html.escape(a.get("author") or "DrakesCraft Labs")
    ok = a["status"] == "published"
    blob = f'<a href="https://blob.build/project/{proj}/{a["channel"]}">Blob Builds</a>' if ok else "pending"
    portal = f'<a href="https://pack.drakescraft.cl/builds/">Portal</a>' if ok else ""
    src = f'<a href="https://github.com/SlimefunNewHorizons/{repo}">Source</a>'
    badge = '<span class="ok">26.2</span>' if ok else '<span class="wait">pending</span>'
    rows.append(f'<tr data-q="{html.escape((a["name"]+" "+author).lower(), quote=True)}"><td>{name}</td><td>{badge}</td><td>{author}</td><td>{blob}</td><td>{portal}</td><td>{src}</td></tr>')
page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Slimefun 6 addons for Minecraft {data['minecraft']}</title>
<style>
:root{{color-scheme:dark}}body{{margin:0;font:15px system-ui,sans-serif;background:#0b0f17;color:#e6edf6}}
main{{max-width:1000px;margin:0 auto;padding:24px}}h1{{margin:0 0 4px}}p{{color:#9fb0c5}}
input{{width:100%;box-sizing:border-box;padding:10px 12px;margin:14px 0;border-radius:8px;border:1px solid #2a3a50;background:#111826;color:inherit}}
table{{width:100%;border-collapse:collapse}}th,td{{text-align:left;padding:8px 10px;border-bottom:1px solid #1d2a3d}}a{{color:#7dd3fc}}
.ok{{color:#4ade80}}.wait{{color:#fbbf24}}
</style></head><body><main>
<h1>Slimefun 6 addons</h1>
<p>{len(rows)} addons maintained by DrakesCraft Labs and running on Minecraft {data['minecraft']}. Every build passes the ABI gate before it is published.</p>
<input id="q" placeholder="Search addons..." autofocus>
<table><thead><tr><th>Addon</th><th>Version</th><th>Author</th><th>Download</th><th>Mirror</th><th>Source</th></tr></thead><tbody id="t">
{chr(10).join(rows)}
</tbody></table>
<script>q.oninput=()=>{{const v=q.value.toLowerCase();for(const r of t.rows)r.hidden=!r.dataset.q.includes(v)}}</script>
</main></body></html>"""
(root / "docs").mkdir(exist_ok=True)
(root / "docs" / "index.html").write_text(page, encoding="utf-8")
print("rows", len(rows))
