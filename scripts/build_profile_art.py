"""Builds the animated SVGs used by profile/README.md (banner + system map, light and dark).

    python scripts/build_profile_art.py path/to/bsg-mark-tight.png

The ring mark is embedded as a data URI because GitHub renders README SVGs through
<img>, which blocks external references. Edit the NODES/EDGES below and re-run.
"""
import base64
from html import escape
import math
import random
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "profile" / "assets"

THEMES = {
    "dark": dict(
        bg="#111311", ink="#EEF2EA", sub="#99A293", faint="#D9E021", faint_op=0.07,
        accent="#D9E021", accent_text="#D9E021", node="#191C18", node_line="#2C3129",
        engine_line="#D9E021", glow_op=0.10, edge_op=0.55, tag="#C9CFC4",
    ),
    "light": dict(
        bg="#F7FAF7", ink="#1A1A1A", sub="#5B6357", faint="#1A1A1A", faint_op=0.05,
        accent="#7F8C00", accent_text="#5F6B00", node="#FFFFFF", node_line="#DCE1D8",
        engine_line="#1A1A1A", glow_op=0.0, edge_op=0.6, tag="#3A3D38",
    ),
}

SANS = "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif"
MONO = "'Cascadia Code', SFMono-Regular, Consolas, 'Liberation Mono', Menlo, monospace"


def tree_rings(cx, cy, n, r0, step, seed):
    """Slightly wobbly concentric circles, like growth rings."""
    rnd = random.Random(seed)
    paths = []
    for i in range(n):
        r = r0 + i * step
        phase = [rnd.uniform(0, 2 * math.pi) for _ in range(3)]
        amp = [rnd.uniform(0.6, 2.2) for _ in range(3)]
        pts = []
        for k in range(73):
            a = 2 * math.pi * k / 72
            rr = r + sum(amp[j] * math.sin((j + 2) * a + phase[j]) for j in range(3))
            pts.append(f"{cx + rr * math.cos(a):.1f},{cy + rr * math.sin(a):.1f}")
        paths.append("M" + " L".join(pts) + "Z")
    return paths


def banner(t, mark):
    rings = tree_rings(1190, 40, 14, 40, 26, seed=7)
    ring_paths = "\n".join(
        f'<path d="{d}" fill="none" stroke="{t["faint"]}" stroke-opacity="{t["faint_op"] * (1.6 - i / 14):.3f}" stroke-width="1.2"/>'
        for i, d in enumerate(rings)
    )
    tagline = "> we build the reporting the off-the-shelf tools don't"
    tag_w = 640
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 340" width="1280" height="340" role="img" aria-label="Blended Services Group — maintenance, projects, landscaping and tree services, Melbourne">
<defs>
  <radialGradient id="glow" cx="50%" cy="50%" r="50%">
    <stop offset="0" stop-color="{t["accent"]}" stop-opacity="{t["glow_op"]}"/>
    <stop offset="1" stop-color="{t["accent"]}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="sweep" x1="0" x2="1">
    <stop offset="0" stop-color="{t["accent"]}" stop-opacity="0"/>
    <stop offset=".5" stop-color="{t["accent"]}" stop-opacity=".9"/>
    <stop offset="1" stop-color="{t["accent"]}" stop-opacity="0"/>
  </linearGradient>
  <clipPath id="type"><rect x="350" y="218" height="34" width="0">
    <animate attributeName="width" from="0" to="{tag_w + 4}" begin="0.6s" dur="2.6s" fill="freeze"/>
  </rect></clipPath>
</defs>
<rect width="1280" height="340" fill="{t["bg"]}"/>
<g>{ring_paths}
  <animateTransform attributeName="transform" type="rotate" values="0 1190 40;3 1190 40;0 1190 40" dur="24s" repeatCount="indefinite"/>
</g>
<circle cx="184" cy="170" r="150" fill="url(#glow)">
  <animate attributeName="r" values="135;160;135" dur="6s" repeatCount="indefinite"/>
</circle>
<image href="{mark}" x="69" y="55" width="230" height="230">
  <animateTransform attributeName="transform" type="rotate" from="0 184 170" to="360 184 170" dur="90s" repeatCount="indefinite"/>
</image>
<text x="350" y="140" font-family="{SANS}" font-size="60" font-weight="700" fill="{t["ink"]}" letter-spacing="-0.5">Blended Services Group</text>
<text x="352" y="182" font-family="{SANS}" font-size="15" font-weight="600" fill="{t["accent_text"]}" letter-spacing="3.5">MAINTENANCE · PROJECTS · LANDSCAPING · TREE SERVICES</text>
<g clip-path="url(#type)">
  <text x="350" y="242" font-family="{MONO}" font-size="19" fill="{t["tag"]}" textLength="{tag_w}" lengthAdjust="spacing">{tagline.replace("'", "&#8217;")}</text>
</g>
<rect y="225" width="10" height="22" fill="{t["accent"]}" x="350">
  <animate attributeName="x" from="350" to="{350 + tag_w + 8}" begin="0.6s" dur="2.6s" fill="freeze"/>
  <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1.05s" repeatCount="indefinite"/>
</rect>
<text x="352" y="294" font-family="{SANS}" font-size="13" fill="{t["sub"]}" letter-spacing="1.5">MELBOURNE  ·  INTERNAL ENGINEERING  ·  TYPESCRIPT · NEXT.JS · PYTHON · SQLITE · AZURE</text>
<rect x="0" y="337" width="1280" height="3" fill="{t["accent"]}" fill-opacity=".18"/>
<rect x="-260" y="337" width="260" height="3" fill="url(#sweep)">
  <animate attributeName="x" from="-260" to="1280" dur="7s" repeatCount="indefinite"/>
</rect>
</svg>'''


# --- system map ---------------------------------------------------------------
SRC_X, SRC_W = 40, 290
ENG_X, ENG_W = 490, 300
OUT_X, OUT_W = 950, 290

SOURCES = [  # (key, title, sub)
    ("aroflo", "AroFlo", "jobs · quotes · invoices · timesheets"),
    ("xero", "Xero", "payments · leave"),
    ("tp", "TreePlotter", "council tree inventories"),
    ("fs", "ForeStree", "watering & maintenance records"),
    ("m365", "Microsoft 365", "SharePoint lists · mail"),
]
ENGINES = [
    ("conn", "AroFlo Connector", "Next.js · SQLite · Azure App Service", "refreshes through the working day", 130),
    ("pipe", "Maintenance pipeline", "Python · headless browser · Azure", "nightly chain, done before the crews start", 330),
]
OUTPUTS = [
    ("pm", "PM dashboards & My Day", "per-manager workload and triage", "conn"),
    ("wall", "Office wallboards", "live on the TVs", "conn"),
    ("wip", "Daily WIP & gross profit", "by division, against budget", "conn"),
    ("rep", "Daily maintenance & planting reports", "emailed every morning", "pipe"),
    ("inv", "Council invoicing packs", "built from source, not by hand", "pipe"),
    ("board", "Workforce board", "who's where, today", "pipe"),
]
EDGES_IN = [("aroflo", "conn"), ("xero", "conn"), ("aroflo", "pipe"), ("tp", "pipe"), ("fs", "pipe"), ("m365", "pipe")]

SRC_H, SRC_GAP, OUT_H, OUT_GAP, ENG_H, TOP = 70, 24, 62, 16, 150, 80


def system_map(t, mark):
    src_y = {k: TOP + i * (SRC_H + SRC_GAP) for i, (k, *_) in enumerate(SOURCES)}
    out_y = {k: TOP + i * (OUT_H + OUT_GAP) for i, (k, *_) in enumerate(OUTPUTS)}
    eng_y = {k: y for k, *_, y in ENGINES}
    parts = []

    for x, label in ((SRC_X, "SOURCES"), (ENG_X, "ENGINES"), (OUT_X, "OUTPUTS")):
        parts.append(f'<text x="{x + 2}" y="52" font-family="{SANS}" font-size="12" font-weight="700" letter-spacing="3" fill="{t["accent_text"]}">{label}</text>')

    edges = [(SRC_X + SRC_W, src_y[s] + SRC_H / 2, ENG_X, eng_y[e] + ENG_H / 2) for s, e in EDGES_IN]
    edges += [(ENG_X + ENG_W, eng_y[e] + ENG_H / 2, OUT_X, out_y[o] + OUT_H / 2) for o, *_, e in OUTPUTS]
    for i, (x1, y1, x2, y2) in enumerate(edges):
        mx = (x1 + x2) / 2
        d = f"M{x1},{y1:.0f} C{mx},{y1:.0f} {mx},{y2:.0f} {x2},{y2:.0f}"
        parts.append(f'<path id="e{i}" d="{d}" fill="none" stroke="{t["accent"]}" stroke-opacity="{t["edge_op"]}" stroke-width="1.6" stroke-dasharray="4 7">'
                     f'<animate attributeName="stroke-dashoffset" from="22" to="0" dur="1.4s" repeatCount="indefinite"/></path>')
        parts.append(f'<circle r="3.5" fill="{t["accent"]}"><animateMotion dur="3.2s" begin="{(i * 0.37) % 3.2:.2f}s" repeatCount="indefinite"><mpath href="#e{i}"/></animateMotion></circle>')

    def node(x, y, w, h, title, sub, line, title_size=17):
        return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{t["node"]}" stroke="{line}" stroke-width="1.2"/>'
                f'<text x="{x + 20}" y="{y + h / 2 - 3}" font-family="{SANS}" font-size="{title_size}" font-weight="600" fill="{t["ink"]}">{escape(title)}</text>'
                f'<text x="{x + 20}" y="{y + h / 2 + 18}" font-family="{SANS}" font-size="13" fill="{t["sub"]}">{escape(sub)}</text>')

    for k, title, sub in SOURCES:
        parts.append(node(SRC_X, src_y[k], SRC_W, SRC_H, title, sub, t["node_line"]))
    for k, title, sub, _ in OUTPUTS:
        parts.append(node(OUT_X, out_y[k], OUT_W, OUT_H, title, sub, t["node_line"], 15))
    for k, title, stack, blurb, y in ENGINES:
        parts.append(
            f'<rect x="{ENG_X}" y="{y}" width="{ENG_W}" height="{ENG_H}" rx="16" fill="{t["node"]}" stroke="{t["engine_line"]}" stroke-width="1.6"/>'
            f'<use href="#mark" x="{ENG_X + 22}" y="{y + 26}" width="34" height="34"/>'
            f'<text x="{ENG_X + 68}" y="{y + 50}" font-family="{SANS}" font-size="21" font-weight="700" fill="{t["ink"]}">{title}</text>'
            f'<text x="{ENG_X + 24}" y="{y + 92}" font-family="{MONO}" font-size="12.5" fill="{t["accent_text"]}">{stack}</text>'
            f'<text x="{ENG_X + 24}" y="{y + 120}" font-family="{SANS}" font-size="13.5" fill="{t["sub"]}">{blurb}</text>')

    body = "\n".join(parts)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 580" width="1280" height="580" role="img" aria-label="System map: AroFlo, Xero, TreePlotter, ForeStree and Microsoft 365 feed the AroFlo Connector and the maintenance pipeline, which produce dashboards, wallboards, WIP, daily reports, council invoicing packs and the workforce board">
<defs><symbol id="mark" viewBox="0 0 253 256"><image href="{mark}" width="253" height="256"/></symbol></defs>
<rect width="1280" height="580" rx="18" fill="{t["bg"]}"/>
{body}
</svg>'''


def main():
    mark_png = Path(sys.argv[1]).read_bytes()
    mark = "data:image/png;base64," + base64.b64encode(mark_png).decode()
    OUT.mkdir(parents=True, exist_ok=True)
    for name, t in THEMES.items():
        (OUT / f"banner-{name}.svg").write_text(banner(t, mark), encoding="utf-8")
        (OUT / f"system-map-{name}.svg").write_text(system_map(t, mark), encoding="utf-8")
    print("wrote", sorted(p.name for p in OUT.iterdir()))


if __name__ == "__main__":
    main()
