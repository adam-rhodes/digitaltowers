#!/usr/bin/env python3
"""Digital Towers static site generator. Reads data/towers.json, entities.json, news.json, photos.json; writes dist/.
Usage: build.py [--deploy]. Deploy rsyncs dist/ to /var/www/digitaltowers (keeping docs/ and the live ADS-B data)."""
import os, sys, json, html, re, shutil, datetime, subprocess, collections, glob
BASE = os.path.dirname(os.path.abspath(__file__))
DIST = BASE + "/dist"
SITE = "https://digitaltowers.org"
WEB = "/var/www/digitaltowers"
NOW = datetime.datetime.now(datetime.timezone.utc)
def esc(s): return html.escape(str(s if s is not None else ""), quote=True)
def slug(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
def load(p, d=None):
    try: return json.load(open(BASE + "/" + p, encoding="utf8"))
    except Exception: return d
TD = load("data/towers.json"); T = TD["towers"]; META = TD["meta"]
EN = load("data/entities.json")
NEWS = load("data/news.json", []) or []
NSTAT = load("data/news_status.json", {}) or {}
PH = load("data/photos.json", {}) or {}
NO_PHOTO = {"EGPE", "LHBP", "EGDG", "KACY", "ENBO"}
LABEL = {"operational": "Operational", "trial": "Trial", "planned": "Planned", "unverified": "Unverified", "decommissioned": "Decommissioned", "cancelled": "Cancelled"}
KIND = {"remote_tower": "Remote tower", "rtc": "Remote tower centre", "digital_tower": "Digital tower", "hybrid": "Hybrid digital tower", "contingency": "Contingency facility", "test_site": "Test or validation site", "remote_afis": "Remote air-ground service (not air traffic control)"}
BYID = {t["id"]: t for t in T}
def photo(t):
    ic = t.get("icao") or ""
    if ic in NO_PHOTO or ic not in PH: return None
    return PH[ic]
def fdate(d):
    try:
        if len(d) == 10: return datetime.date.fromisoformat(d).strftime("%-d %b %Y")
        if len(d) == 7: return datetime.date.fromisoformat(d + "-01").strftime("%b %Y")
    except Exception: pass
    return d
def host(u):
    m = re.match(r"https?://(?:www\.)?([^/]+)", u); return m.group(1) if m else u

ICON = {
 "home": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 11l9-7 9 7v9a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/></svg>',
 "map": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.2 3 14.8 0 18M12 3c-3 3.2-3 14.8 0 18"/></svg>',
 "list": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M8 6h13M8 12h13M8 18h13"/><circle cx="4" cy="6" r="1"/><circle cx="4" cy="12" r="1"/><circle cx="4" cy="18" r="1"/></svg>',
 "news": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 4h11a2 2 0 0 1 2 2v14H7a2 2 0 0 1-2-2z"/><path d="M18 8h2v10a2 2 0 0 1-2 2M8 8h6M8 12h6M8 16h4"/></svg>',
 "more": '<svg viewBox="0 0 24 24" fill="currentColor"><circle cx="5" cy="12" r="1.8"/><circle cx="12" cy="12" r="1.8"/><circle cx="19" cy="12" r="1.8"/></svg>',
}
LOGO = '<svg viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="9" fill="#151821"/><path d="M11 25l2-12h6l2 12" fill="none" stroke="#7aa7ff" stroke-width="1.8" stroke-linejoin="round"/><path d="M9.5 13h13l-1.5-4h-10z" fill="#5b8dd9"/><path d="M16 9V5.5" stroke="#7aa7ff" stroke-width="1.8" stroke-linecap="round"/></svg>'
NAV = [("Map", "/map/"), ("Towers", "/towers/"), ("Connections", "/connections/"), ("Timeline", "/timeline/"), ("News", "/news/"), ("United States", "/united-states/"), ("Vendors", "/vendors/"), ("About", "/about/")]
TABS = [("Home", "/", "home"), ("Map", "/map/", "map"), ("Towers", "/towers/", "list"), ("News", "/news/", "news"), ("More", "/about/", "more")]
PAGES = []  # (url, lastmod)

def head(title, desc, path, extra="", og_img=None, noindex=False, jsonld=None):
    full = SITE + path
    img = og_img or (SITE + "/assets/og.png")
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><meta name="theme-color" content="#0b0d12">
<link rel="canonical" href="{full}">{'<meta name="robots" content="noindex">' if noindex else '<meta name="robots" content="index,follow,max-image-preview:large">'}
<meta property="og:type" content="website"><meta property="og:site_name" content="Digital Towers"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{full}">
<meta name="twitter:card" content="summary"><link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="alternate" type="application/atom+xml" title="Digital Towers news" href="/feed.xml">
<link rel="stylesheet" href="/assets/site.css?v={VER}">{extra}{('<script type="application/ld+json">' + json.dumps(jsonld, ensure_ascii=False) + '</script>') if jsonld else ''}</head>'''
def top(path):
    def cur(u): return ' aria-current="page"' if (path == u or (u != "/" and path.startswith(u))) else ""
    nav = "".join(f'<a href="{u}"{cur(u)}>{n}</a>' for n, u in NAV)
    return f'<header class="top"><div class="wrap"><a class="brand" href="/">{LOGO}<span>Digital Towers</span></a><nav class="nav" aria-label="Main">{nav}</nav></div></header>'
def tabbar(path):
    def cur(u): return ' aria-current="page"' if (path == u or (u != "/" and path.startswith(u))) else ""
    return '<nav class="tabbar" aria-label="Tabs">' + "".join(f'<a href="{u}"{cur(u)}>{ICON[i]}<span>{n}</span></a>' for n, u, i in TABS) + '</nav>'
def footer():
    return f'''<footer><div class="wrap"><div class="cols2"><div><b style="color:var(--ink)">Digital Towers</b><p style="margin-top:8px;max-width:46ch">An independent reference to remote and digital air traffic control towers, built from public sources only. Not affiliated with, endorsed by, or speaking for the FAA or any other government body. Not for operational use.</p><p class="xs faint">Data built {NOW.strftime("%-d %b %Y %H:%M")} UTC. <a href="/about/">How this is sourced</a></p></div>
<div><h4>Browse</h4><ul><li><a href="/map/">World map</a></li><li><a href="/towers/">All towers</a></li><li><a href="/countries/">Countries</a></li><li><a href="/vendors/">Vendors</a></li><li><a href="/operators/">Service providers</a></li><li><a href="/regulators/">Regulators and standards</a></li><li><a href="/connections/">Connections</a></li><li><a href="/timeline/">Timeline</a></li><li><a href="/coverage/">Coverage and gaps</a></li></ul></div>
<div><h4>Read</h4><ul><li><a href="/news/">News</a> · <a href="/feed.xml">Feed</a></li><li><a href="/united-states/">United States</a></li><li><a href="/what-is-a-digital-tower/">What is a digital tower</a></li><li><a href="/library/">Library</a></li><li><a href="/data/">Data downloads</a></li><li><a href="https://github.com/adam-rhodes/digitaltowers">Source on GitHub</a></li></ul></div></div></div></footer>'''
def page(path, title, desc, body, extra_head="", scripts="", body_class="", noindex=False, jsonld=None, og_img=None, lastmod=None):
    out = head(title, desc, path, extra_head, og_img, noindex, jsonld) + f'<body class="{body_class}">{top(path)}<main id="main">{body}</main>' + ("" if "maponly" in body_class else footer()) + tabbar(path) + scripts + '</body></html>'
    fp = DIST + path + ("index.html" if path.endswith("/") else "")
    os.makedirs(os.path.dirname(fp), exist_ok=True); open(fp, "w", encoding="utf8").write(out)
    if not noindex: PAGES.append((path, lastmod or NOW.strftime("%Y-%m-%d")))

def pill(s): return f'<span class="pill st-{s}">{LABEL[s]}</span>'
def tcard(t, big=False):
    p = photo(t)
    im = f'<div class="im"><img src="/{p["file"]}" alt="" loading="lazy" decoding="async"></div>' if p else f'<div class="im none">{esc(t["icao"] or t["cc"])}</div>'
    return f'<a class="tcard" href="/towers/{t["id"]}/">{im}<div class="tb"><b>{esc(t["name"])}</b><div class="meta"><span>{esc(t["icao"] + " · " if t["icao"] else "")}{esc(t["country"])}</span>{pill(t["status"])}</div></div></a>'
def credit(p, what="Photo of the airport"):
    return f'<p class="credit">{what}: {esc(p["artist"])}, <a href="{esc(p["page"])}" rel="noopener">{esc(p["license"])}</a>, via Wikimedia Commons.</p>'

# ------------------------------------------------------------------ data views
COUNTRIES = collections.OrderedDict()
for t in sorted(T, key=lambda x: x["country"]): COUNTRIES.setdefault(t["country"], []).append(t)
def vendor_of(name):
    for v in EN["vendors"]:
        if name in v["aliases"]: return v
def ansp_of(name):
    if not name: return None
    for a in EN["ansps"]:
        for al in a["aliases"]:
            if name == al or name.startswith(al + " ") or name.startswith(al + "/") : return a
    return None
status_counts = collections.Counter(t["status"] for t in T)
VER = NOW.strftime("%Y%m%d%H%M")

# ------------------------------------------------------------------ pages
def build_assets():
    os.makedirs(DIST + "/assets", exist_ok=True)
    for f, dst in (("dt_site.css", "site.css"), ("dt_map.js", "map.js"), ("dt_site.js", "site.js"), ("conn.js", "conn.js")):
        shutil.copy(BASE + "/" + f, DIST + "/assets/" + dst)
    for f in ("maplibre-gl.js", "maplibre-gl.css", "pmtiles.js"): shutil.copy(BASE + "/vendor/" + f, DIST + "/assets/" + f)
    shutil.copy(BASE + "/vendor/bm/package/dist/basemaps.js", DIST + "/assets/basemaps.js")
    open(DIST + "/assets/favicon.svg", "w").write(LOGO.replace('aria-hidden="true"', 'xmlns="http://www.w3.org/2000/svg"'))
    for d in ("tiles", "fonts", "img"):
        if os.path.isdir(BASE + "/" + d):
            if os.path.exists(DIST + "/" + d): shutil.rmtree(DIST + "/" + d)
            if d == "tiles":
                os.makedirs(DIST + "/tiles"); shutil.copy(BASE + "/tiles/world.pmtiles", DIST + "/tiles/world.pmtiles")
            else: shutil.copytree(BASE + "/" + d, DIST + "/" + d)
    os.makedirs(DIST + "/data", exist_ok=True)
    for f in ("towers.json", "towers.geojson", "towers.csv", "entities.json"): shutil.copy(BASE + "/data/" + f, DIST + "/data/" + f)
    # lightweight og image: solid card (no network)
MAPASSETS = '<link rel="stylesheet" href="/assets/maplibre-gl.css">'
MAPJS = '<script src="/assets/maplibre-gl.js"></script><script src="/assets/pmtiles.js"></script><script src="/assets/basemaps.js"></script><script src="/assets/map.js?v=' + VER + '"></script>'

def build_home():
    ops = status_counts["operational"]
    strip_ids = [("esno", "Örnsköldsvik, Sweden", "Remote operation from 2015, described by Saab as the first airport in the world with remote ATC."),
                 ("eglc", "London City, UK", "Controlled remotely from the NATS centre at Swanwick since 2021."),
                 ("libr", "Brindisi, Italy", "Italy's first remotely managed tower, inaugurated June 2022."),
                 ("levx", "Vigo, Spain", "Spain's first regulator-certified digital tower, reported operating December 2025.")]
    strip = ""
    for i, (tid, ttl, cap) in enumerate(strip_ids):
        t = BYID[tid]; p = photo(t)
        if p: strip += f'<a class="ph" href="/towers/{tid}/"><img src="/{p["file"]}" alt="" decoding="async"><span class="cap"><b>{esc(ttl)}</b><span>{esc(cap)}</span></span></a>'
    latest = NEWS[:5]
    nl = "".join(news_item(n) for n in latest) or '<p class="mute">No published items yet.</p>'
    us = [x for x in EN["us_timeline"] if x[0] >= "2026-04"][-5:]
    ust = "".join(f'<li><span class="d">{fdate(d)}</span><div>{esc(tx)} <a class="xs" href="{esc(u)}" rel="noopener">{esc(host(u))}</a></div></li>' for d, tx, u in reversed(us))
    cc = "".join(f'<a class="chip" href="/countries/{slug(c)}/">{esc(c)} <span class="faint" style="margin-left:6px">{len(v)}</span></a>' for c, v in sorted(COUNTRIES.items(), key=lambda x: -len(x[1]))[:14])
    vcards = ""
    for v in EN["vendors"][:6]:
        n = sum(1 for t in T if any(a in t["vendors"] for a in v["aliases"]))
        vcards += f'<a class="card flat" href="/vendors/{v["id"]}/" style="color:var(--ink)"><h3>{esc(v["name"])}</h3><p class="mute small" style="margin:6px 0 10px">{esc(v["country"])}</p><span class="tag">{n} sites</span></a>'
    body = f'''<div class="wrap"><section class="hero"><div class="eyebrow">Reference</div><h1>Tracking digital and remote towers worldwide.</h1>
<p class="lede">Every fact links to its public source, every site carries a status and a confidence label, and the news below refreshes from public feeds. Coverage is not complete, and unverified sites are marked as such.</p>
<div class="cta"><a class="btn primary" href="/map/">Open the world map</a><a class="btn" href="/towers/">Browse all towers</a><a class="btn" href="/united-states/">United States status</a><a class="btn" href="/connections/">How towers connect</a></div>
<div class="stats"><div class="stat"><b>{len(T)}</b><span>sites mapped</span></div><div class="stat"><b>{ops}</b><span>operational</span></div><div class="stat"><b>{status_counts["trial"]}</b><span>trial</span></div><div class="stat"><b>{status_counts["planned"]}</b><span>planned</span></div><div class="stat"><b>{status_counts.get("unverified",0)}</b><span>unverified</span></div><div class="stat"><b>{META["countries"]}</b><span>countries</span></div></div>
<p class="small mute" style="margin-top:16px;max-width:74ch">{len(T)} sites = {", ".join(str(v) + " " + k for k, v in status_counts.most_common())}. {sum(1 for t in T if t["kind"] in ("remote_tower","rtc","digital_tower","remote_afis"))} are remote towers, centres, digital towers or remote air-ground services; the other {sum(1 for t in T if t["kind"] not in ("remote_tower","rtc","digital_tower","remote_afis"))} are hybrid, contingency or test facilities. <a href="/coverage/">What is not covered</a>.</p><div class="strip">{strip}</div><p class="credit">Photos from Wikimedia Commons under open licences; credits on each tower page.</p></section>
<section class="section"><div class="head"><h2>Latest</h2><a href="/news/">All news</a></div><div class="news">{nl}</div></section>
<section class="section"><div class="head"><h2>United States right now</h2><a href="/united-states/">Full tracker</a></div><div class="card"><ul class="timeline">{ust}</ul></div></section>
<section class="section"><div class="head"><h2>By country</h2><a href="/countries/">All countries</a></div><div style="display:flex;gap:8px;flex-wrap:wrap">{cc}</div></section>
<section class="section"><div class="head"><h2>By vendor</h2><a href="/vendors/">All vendors</a></div><div class="grid g3">{vcards}</div></section>
<section class="section"><div class="card"><h3>How to read the labels</h3><p class="mute" style="margin:8px 0 0;max-width:70ch">Operational means a source states the facility provides air traffic service. Trial means tests or shadow operations without approved service. Planned means announced or funded but not operating. Unverified means reported without a primary source. Decommissioned and cancelled mean the program ended. A design approval is not an operational authorization and is not shown as one. Confidence is high when an operator or regulator source states it, medium when a vendor or press source does, and low when the evidence is old or single-sourced. Hybrid and contingency facilities are listed but kept distinct from remote towers. <a href="/about/">Method and sources</a>.</p></div></section></div>'''
    page("/", "Digital Towers: every remote and digital air traffic tower, sourced", f"A sourced map of {len(T)} remote and digital air traffic control towers in {META['countries']} countries, with status, vendors, providers, connections and a news feed from public sources.", body,
         jsonld={"@context": "https://schema.org", "@graph": [{"@type": "WebSite", "name": "Digital Towers", "url": SITE + "/", "potentialAction": {"@type": "SearchAction", "target": SITE + "/towers/?q={q}", "query-input": "required name=q"}}]})

def news_item(n):
    tags = "".join(f'<span class="tag">{esc(x)}</span>' for x in n["tags"][:4])
    return f'<div class="nitem" data-tags="{esc(" ".join(slug(x) for x in n["tags"]))}"><div class="dt">{fdate(n["date"])}</div><div><a class="t" href="{esc(n["url"])}" rel="noopener" target="_blank">{esc(n["title"])}</a><div class="m"><span>{esc(n["source"])}</span>{tags}</div></div></div>'

def build_news():
    allt = collections.Counter(x for n in NEWS for x in n["tags"])
    chips = "".join(f'<button class="chip" type="button" aria-pressed="false" data-tag="{esc(slug(k))}">{esc(k)} <span class="faint" style="margin-left:6px">{v}</span></button>' for k, v in allt.most_common(18))
    items = "".join(news_item(n) for n in NEWS)
    chk = NSTAT.get("last_run")
    stline = f'Last checked {esc(chk)} UTC across {esc(NSTAT.get("feeds_ok","?"))} of {esc(NSTAT.get("feeds_total","?"))} sources. ' if chk else ""
    body = f'''<div class="wrap" style="padding-top:28px"><h1 style="font-size:clamp(30px,4.5vw,46px)">News</h1><p class="mute" style="max-width:62ch;margin-top:10px">Items from public feeds and press releases about remote and digital towers. {stline}New items wait in a review queue for 24 hours before they appear here, and anything flagged is held for a person to check. Every item links to its original source.</p>
<div id="newsfilter" style="display:flex;gap:6px;flex-wrap:wrap;margin:18px 0">{chips}</div><div class="news">{items}</div>
<p class="small faint" style="margin-top:18px">Feeds: Google News search, Federal Register API, CANSO, NATS, AVweb, Aviation Tech Today, Airport Improvement, plus items added by hand with a source link. <a href="/feed.xml">Atom feed</a>.</p></div>'''
    page("/news/", "Digital tower news | Digital Towers", "Dated, tagged news about remote and digital air traffic control towers, from public feeds, with links to each original source.", body, scripts='<script src="/assets/site.js?v=' + VER + '"></script>')
    # atom
    ent = "".join(f'<entry><title>{esc(n["title"])}</title><link href="{esc(n["url"])}"/><id>{esc(n["url"])}</id><updated>{n["date"]}T12:00:00Z</updated><summary>{esc(n["source"])}</summary></entry>' for n in NEWS[:60])
    open(DIST + "/feed.xml", "w", encoding="utf8").write(f'<?xml version="1.0" encoding="utf-8"?><feed xmlns="http://www.w3.org/2005/Atom"><title>Digital Towers news</title><link href="{SITE}/news/"/><link rel="self" href="{SITE}/feed.xml"/><id>{SITE}/feed.xml</id><updated>{NOW.strftime("%Y-%m-%dT%H:%M:%SZ")}</updated>{ent}</feed>')

def build_directory():
    rows = ""
    for t in sorted(T, key=lambda x: (x["country"], x["name"])):
        vs = "|" + "|".join(t["vendors"]) + "|"
        rows += f'<tr data-s="{t["status"]}" data-c="{esc(t["country"])}" data-v="{esc(vs)}" data-t="{esc((t["name"]+" "+t["icao"]+" "+t["country"]+" "+" ".join(t["vendors"])+" "+t["ansp"]).lower())}"><td><a class="rowlink" href="/towers/{t["id"]}/">{esc(t["name"])}</a><div class="xs faint">{esc(KIND[t["kind"]])}</div></td><td>{esc(t["icao"])}</td><td>{esc(t["country"])}</td><td>{esc(", ".join(t["vendors"]) or "n/a")}</td><td>{pill(t["status"])}</td><td><span class="tag conf-{t["conf"]}">{t["conf"]}</span></td></tr>'
    co = "".join(f'<option>{esc(c)}</option>' for c in COUNTRIES)
    vn = "".join(f'<option>{esc(v["aliases"][0])}</option>' for v in EN["vendors"])
    body = f'''<div class="wrap" style="padding-top:28px"><h1 style="font-size:clamp(30px,4.5vw,46px)">All towers</h1><p class="mute" style="margin-top:10px">{len(T)} sites. Filter by status, country or vendor. <a href="/data/">Download the data</a>. Also: <a href="/connections/">connections</a>, <a href="/timeline/">timeline</a>, <a href="/coverage/">coverage and gaps</a>.</p>
<div class="tools" style="margin-top:18px"><input id="dq" type="search" placeholder="Search name, ICAO code, country, vendor" aria-label="Search towers"><select id="dstatus" aria-label="Status"><option value="">Any status</option>{"".join(f'<option value="{k}">{v}</option>' for k,v in LABEL.items())}</select><select id="dcountry" aria-label="Country"><option value="">Any country</option>{co}</select><select id="dvendor" aria-label="Vendor"><option value="">Any vendor</option>{vn}</select><span id="dcount" class="small mute"></span></div>
<div style="overflow-x:auto"><table class="tbl"><thead><tr><th>Site</th><th>ICAO</th><th>Country</th><th>Vendor</th><th>Status</th><th>Confidence</th></tr></thead><tbody id="dirrows">{rows}</tbody></table></div></div>'''
    page("/towers/", "All remote and digital towers | Digital Towers", f"Directory of {len(T)} remote, digital and hybrid air traffic control tower sites with status, vendor, provider and confidence labels.", body, scripts='<script src="/assets/site.js?v=' + VER + '"></script>')

KIND_BLURB = {"remote_tower": "a remote tower: cameras and sensors at the airport feed controllers who work somewhere else",
              "rtc": "a remote tower centre: the facility where controllers work for one or more airports",
              "digital_tower": "a digital tower: sensor-based tower technology that is not a straight remote tower",
              "hybrid": "a hybrid digital tower: controllers keep the window view and add camera video, so it is not a remote tower",
              "contingency": "a contingency facility: a backup position for use when the main tower is unavailable",
              "test_site": "a test or validation site rather than an operating tower",
              "remote_afis": "a remote aerodrome air-ground (RADIO) service: an officer elsewhere gives advisory information by camera, which is not air traffic control"}
def build_tower(t):
    p = photo(t); path = f"/towers/{t['id']}/"
    hero = f'<div class="thero"><img src="/{p["file"]}" alt="" decoding="async"><div class="in"><div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px">{pill(t["status"])}<span class="tag conf-{t["conf"]}">confidence {t["conf"]}</span></div><h1>{esc(t["name"])}</h1></div></div>{credit(p)}' if p else \
           f'<div class="thero" style="min-height:150px"><div class="in"><div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px">{pill(t["status"])}<span class="tag conf-{t["conf"]}">confidence {t["conf"]}</span></div><h1>{esc(t["name"])}</h1></div></div>'
    facts = "".join(f'<li>{esc(f["t"])}<a class="src" href="{esc(f["u"])}" rel="noopener" target="_blank">{esc(f["u"])}</a></li>' for f in t["facts"])
    tl = "".join(f'<li><span class="d">{esc(fdate(d["d"]))}</span><div>{esc(d["t"])}' + (f' <a class="xs" href="{esc(d["u"])}" rel="noopener" target="_blank">{esc(host(d["u"]))}</a>' if d.get("u") else '') + '</div></li>' for d in sorted(t["dates"], key=lambda x: x["d"]))
    note = f'<div class="note" style="margin-top:16px"><b>Caveat.</b> {esc(t["note"])}</div>' if t["note"] else ""
    if t["status"] in ("unverified",) or t["conf"] == "low":
        note += '<div class="note warn" style="margin-top:12px">The evidence for this entry is old or comes from a single source. Treat the status as unconfirmed.</div>'
    conn = ""
    for c in t["connections"]:
        conn += f'<a class="chip" href="/towers/{c["id"]}/">{esc(c["rel"])}: {esc(c["name"])}</a> '
    v = ""
    for vn in t["vendors"]:
        ve = vendor_of(vn)
        if ve: v += f'<a class="chip" href="/vendors/{ve["id"]}/">{esc(ve["name"])}</a> '
    a = ansp_of(t["ansp"]); av = f'<a class="chip" href="/operators/{a["id"]}/">{esc(a["name"])}</a>' if a else ""
    same = [x for x in COUNTRIES[t["country"]] if x["id"] != t["id"]][:8]
    sm = "".join(f'<a class="chip" href="/towers/{x["id"]}/">{esc(x["name"])}</a> ' for x in same)
    gl = {"i": 0}
    srcs = sorted({f["u"] for f in t["facts"]})
    glance = f'''<div class="card"><h3 style="margin-bottom:12px">At a glance</h3><dl class="kv"><dt>ICAO</dt><dd>{esc(t["icao"] or "n/a")}</dd><dt>Country</dt><dd><a href="/countries/{slug(t["country"])}/">{esc(t["country"])}</a></dd><dt>Type</dt><dd>{esc(KIND[t["kind"]])}</dd><dt>Vendor</dt><dd>{esc(", ".join(t["vendors"]) or "not named in sources")}</dd><dt>Provider</dt><dd>{esc(t["ansp"] or "n/a")}</dd><dt>Status</dt><dd>{LABEL[t["status"]]}</dd>{('<dt>Regulator</dt><dd>' + esc(t["regulator"]) + '</dd>') if t.get("regulator") else ''}{('<dt>Program</dt><dd><a href="/regulators/#' + esc(t["program"]) + '">' + esc(t["program"]) + '</a></dd>') if t.get("program") else ''}<dt>Position</dt><dd>{t["lat"]:.3f}, {t["lon"]:.3f}</dd></dl></div>
<div class="card"><h3 style="margin-bottom:8px">Sources</h3><p class="small mute" style="margin:0">{len(srcs)} public source{"s" if len(srcs)!=1 else ""}: {", ".join(esc(host(s)) for s in srcs)}.</p><p class="small" style="margin:12px 0 0"><a href="https://github.com/adam-rhodes/digitaltowers/issues/new?title={esc("Correction: " + t["name"]).replace(" ", "%20")}&body=Tower%20id%3A%20{t["id"]}%0AWhat%20is%20wrong%3A%20%0APublic%20source%20link%3A%20">Suggest a correction</a></p></div>'''
    body = f'''<div class="wrap"><div class="crumbs"><a href="/towers/">Towers</a> / <a href="/countries/{slug(t["country"])}/">{esc(t["country"])}</a></div>{hero}
<div class="cols"><div><p style="font-size:17px;max-width:62ch;margin-top:6px">{esc(t["name"])} is {KIND_BLURB[t["kind"]]}. {esc(t["facts"][0]["t"]) if t["facts"] else ""}</p>{note}
<h2 id="sources" style="margin:30px 0 12px;font-size:22px">What the sources say</h2><ul class="facts">{facts}</ul>
{('<h2 style="margin:30px 0 12px;font-size:22px">Timeline</h2><div class="card"><ul class="timeline" style="margin:0">' + tl + '</ul></div>') if tl else ''}
<h2 style="margin:30px 0 12px;font-size:22px">Connections</h2><div id="minimap" class="minimap"></div><p class="xs faint" style="margin:8px 0 14px">Lines join each airport to the centre that controls it. Basemap: OpenStreetMap data via Protomaps.</p>
<div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:10px">{conn}{v}{av}</div><p class="small" style="margin:6px 0 14px"><a href="/connections/?focus={t["id"]}">Open in the connections view</a> · <a href="/timeline/?tower={t["id"]}">Timeline for this site</a></p>
{('<p class="xs faint" style="margin:18px 0 8px">Other sites in ' + esc(t["country"]) + '</p><div style="display:flex;gap:6px;flex-wrap:wrap">' + sm + '</div>') if sm else ''}
<p style="margin-top:22px"><a class="btn" href="/map/#{t["id"]}">Show on the world map</a></p></div><div class="side">{glance}</div></div></div>'''
    sc = MAPJS + f'<script>fetch("/data/towers.json?v={VER}").then(function(r){{return r.json()}}).then(function(d){{window.DTMini("{t["id"]}",d.towers)}});</script>'
    ld = {"@context": "https://schema.org", "@type": "Airport", "name": t["name"], "geo": {"@type": "GeoCoordinates", "latitude": t["lat"], "longitude": t["lon"]}, "address": {"@type": "PostalAddress", "addressCountry": t["cc"]}}
    if t["icao"]: ld["icaoCode"] = t["icao"]
    page(path, f'{t["name"]}: {LABEL[t["status"]].lower()} {KIND[t["kind"]].lower()} | Digital Towers', f'{t["name"]} ({t["country"]}): {KIND[t["kind"]].lower()}, {LABEL[t["status"]].lower()}. Vendor {", ".join(t["vendors"]) or "not named"}; provider {t["ansp"] or "n/a"}. Sourced facts, timeline and connections.', body, MAPASSETS, sc, jsonld=ld)

def build_countries():
    cards = "".join(f'<a class="card flat" href="/countries/{slug(c)}/" style="color:var(--ink)"><h3>{esc(c)}</h3><p class="mute small" style="margin:6px 0 0">{len(v)} sites · {sum(1 for x in v if x["status"]=="operational")} operational</p></a>' for c, v in COUNTRIES.items())
    page("/countries/", "Countries with remote and digital towers | Digital Towers", f"{META['countries']} countries with remote, digital or hybrid tower sites, with counts and status.", f'<div class="wrap" style="padding-top:28px"><h1 style="font-size:clamp(30px,4.5vw,46px)">Countries</h1><div class="grid g3" style="margin-top:20px">{cards}</div></div>')
    for c, v in COUNTRIES.items():
        sc = collections.Counter(x["status"] for x in v)
        provs = sorted({x["ansp"] for x in v if x["ansp"]})
        body = f'''<div class="wrap"><div class="crumbs"><a href="/countries/">Countries</a></div><h1 style="margin-top:8px;font-size:clamp(30px,4.5vw,46px)">{esc(c)}</h1><p class="mute" style="max-width:62ch;margin-top:10px">{len(v)} site{"s" if len(v)!=1 else ""}: {", ".join(f"{n} {LABEL[k].lower()}" for k, n in sc.most_common())}. Providers named in sources: {esc(", ".join(provs) or "none")}.</p>
<p style="margin-top:12px"><a class="btn" href="/map/?country={esc(c).replace(" ", "%20")}">Show on the map</a></p><div class="grid g3" style="margin-top:22px">{"".join(tcard(x) for x in v)}</div></div>'''
        page(f"/countries/{slug(c)}/", f"Remote and digital towers in {c} | Digital Towers", f"{len(v)} remote, digital or hybrid tower sites in {c}: {', '.join(x['name'] for x in v[:4])} and more, with status and sources.", body)

def build_entities():
    # vendors
    for kind, key, base, title in (("vendors", "vendors", "/vendors/", "Vendors"), ("operators", "ansps", "/operators/", "Service providers")):
        lst = EN[key]
        def towers_for(e):
            if kind == "vendors": return [t for t in T if any(a in t["vendors"] for a in e["aliases"])]
            return [t for t in T if ansp_of(t["ansp"]) and ansp_of(t["ansp"])["id"] == e["id"]]
        cards = ""
        for e in lst:
            ts = towers_for(e)
            if not ts: continue
            cards += f'<a class="card flat" href="{base}{e["id"]}/" style="color:var(--ink)"><h3>{esc(e["name"])}</h3><p class="mute small" style="margin:6px 0 10px">{esc(e["country"])}</p><p class="small" style="margin:0 0 10px">{esc(e["blurb"])}</p><span class="tag">{len(ts)} sites</span></a>'
        page(base, f"{title} | Digital Towers", f"{title} behind remote and digital towers, with the sites each one is linked to in public sources.", f'<div class="wrap" style="padding-top:28px"><h1 style="font-size:clamp(30px,4.5vw,46px)">{title}</h1><div class="grid g2" style="margin-top:20px">{cards}</div></div>')
        for e in lst:
            ts = towers_for(e)
            if not ts: continue
            sc = collections.Counter(x["status"] for x in ts)
            rel = collections.Counter()
            for x in ts:
                if kind == "vendors":
                    a = ansp_of(x["ansp"]); 
                    if a: rel[(a["name"], "/operators/" + a["id"] + "/")] += 1
                else:
                    for vn in x["vendors"]:
                        ve = vendor_of(vn)
                        if ve: rel[(ve["name"], "/vendors/" + ve["id"] + "/")] += 1
            relh = "".join(f'<a class="chip" href="{u}">{esc(n)} <span class="faint" style="margin-left:6px">{c}</span></a> ' for (n, u), c in rel.most_common())
            body = f'''<div class="wrap"><div class="crumbs"><a href="{base}">{title}</a></div><h1 style="margin-top:8px;font-size:clamp(30px,4.5vw,46px)">{esc(e["name"])}</h1><p class="mute" style="max-width:64ch;margin-top:10px">{esc(e["blurb"])}</p>
<p class="small" style="margin-top:10px">{esc(e["country"])} · <a href="{esc(e["url"])}" rel="noopener" target="_blank">{esc(host(e["url"]))}</a> · {len(ts)} sites: {", ".join(f"{n} {LABEL[k].lower()}" for k, n in sc.most_common())}</p>
{('<p class="xs faint" style="margin:20px 0 8px">' + ("Providers it works with" if kind == "vendors" else "Vendors used") + '</p><div style="display:flex;gap:6px;flex-wrap:wrap">' + relh + '</div>') if relh else ''}
<div class="grid g3" style="margin-top:22px">{"".join(tcard(x) for x in ts)}</div></div>'''
            page(f"{base}{e['id']}/", f"{e['name']}: remote and digital tower sites | Digital Towers", f"{e['name']} ({e['country']}): {len(ts)} remote or digital tower sites linked in public sources. {e['blurb']}", body)
    # regulators + programs
    regs = "".join(f'<div class="card flat" id="{r["id"]}"><h3>{esc(r["name"])}</h3><p class="mute small" style="margin:4px 0 8px">{esc(r["country"])}</p><p class="small" style="margin:0 0 8px">{esc(r["blurb"])}</p><a class="small" href="{esc(r["url"])}" rel="noopener" target="_blank">{esc(host(r["url"]))}</a></div>' for r in EN["regulators"])
    progs = "".join(f'<div class="card flat" id="{p["id"]}"><h3>{esc(p["name"])}</h3><p class="small mute" style="margin:6px 0 8px">{esc(p["blurb"])}</p>' + "".join(f'<a class="chip" href="/towers/{t["id"]}/" style="margin:2px">{esc(t["name"])}</a>' for t in T if t["program"] == p["id"])[:6000] + f'<p class="xs" style="margin:10px 0 0"><a href="{esc(p["url"])}" rel="noopener" target="_blank">Source: {esc(host(p["url"]))}</a></p></div>' for p in EN["programs"])
    page("/regulators/", "Regulators and standards bodies | Digital Towers", "Regulators and standards bodies that shape remote and digital towers: FAA, EUROCAE, EASA, ICAO, IFATCA and CANSO.", f'<div class="wrap" style="padding-top:28px"><h1 style="font-size:clamp(30px,4.5vw,46px)">Regulators and standards</h1><div class="grid g2" style="margin-top:20px">{regs}</div><h2 style="margin:40px 0 14px">Programs</h2><div class="grid g2">{progs}</div></div>')

def build_us():
    ustow = [t for t in T if t["country"] == "United States"]
    tl = "".join(f'<li><span class="d">{fdate(d)}</span><div>{esc(tx)} <a class="xs" href="{esc(u)}" rel="noopener" target="_blank">{esc(host(u))}</a></div></li>' for d, tx, u in reversed(EN["us_timeline"]))
    docs = ""
    for title, d, fn in EN["faa_docs"]:
        if os.path.exists(BASE + "/docs_faa/" + fn): docs += f'<li><a href="/docs/faa/{fn}">{esc(title)}</a> <span class="faint small">{fdate(d)}</span></li>'
    body = f'''<div class="wrap" style="padding-top:28px"><div class="eyebrow">United States</div><h1 style="font-size:clamp(30px,4.5vw,46px)">Where US digital towers stand</h1>
<p class="mute" style="max-width:66ch;margin-top:12px">Built only from public sources, each dated and linked. Last reviewed {NOW.strftime("%-d %B %Y")}.</p>
<div class="grid g3" style="margin-top:22px"><div class="card"><div class="tag">2 Sep 2026</div><h3 style="margin:10px 0 6px">Design approval, with conditions</h3><p class="small mute" style="margin:0">AIP guidance states the FAA granted system design approval to Frequentis USA on 2 September 2026, with conditions. The conditions are not in the sources reviewed. <a href="https://www.faa.gov/airports/aip/guidance_letters/aip_pgl_26_06" rel="noopener" target="_blank">PGL 26-06</a></p></div>
<div class="card"><div class="tag">28 Sep 2026</div><h3 style="margin:10px 0 6px">AIP funding guidance</h3><p class="small mute" style="margin:0">PGL 26-06 says a digital tower with FAA system design approval may be funded at Contract Tower candidates, and that it does not grant operational approval. The sponsor must own, operate and maintain the system.</p></div>
<div class="card"><div class="tag">18 Sep to 19 Oct 2026</div><h3 style="margin:10px 0 6px">FY27 contract tower grants</h3><p class="small mute" style="margin:0">The FAA Contract Tower Competitive Grant Program lists FAA-certified digital towers as eligible; up to $100 million this year. Applications close 19 October 2026. <a href="https://www.faa.gov/iija/airport-infrastructure/fct" rel="noopener" target="_blank">FAA page</a></p></div></div>
<div class="note" style="margin-top:16px"><b>Sources disagree on timing.</b> The FAA page for this program, now titled Digital Tower Systems, was last updated 4 September 2026. It does not list the approval and says the FAA will update it when (and if) it issues one. The earlier Remote Tower Systems page, updated 6 February 2025, said no system was approved. The guidance letter PGL 26-06, dated 28 September 2026, states that the FAA granted Frequentis USA an approval on 2 September 2026, with conditions. We show the approval as that letter words it. <a href="https://www.faa.gov/airports/planning_capacity/non_federal/digital_tower_systems" rel="noopener" target="_blank">FAA page</a></div>
<h2 style="margin:36px 0 14px">US sites</h2><div class="grid g3">{"".join(tcard(t) for t in ustow)}</div>
<h2 style="margin:40px 0 14px">Timeline</h2><div class="card"><ul class="timeline" style="margin:0">{tl}</ul></div>
<h2 style="margin:40px 0 14px">FAA documents (public)</h2><div class="card"><ul style="margin:0;padding-left:18px;display:grid;gap:8px">{docs}</ul><p class="xs faint" style="margin:14px 0 0">Copies of public FAA documents. Latest versions: <a href="https://www.faa.gov/airports/planning_capacity/non_federal/remote_tower_systems" rel="noopener" target="_blank">faa.gov remote tower systems</a>.</p></div></div>'''
    page("/united-states/", "United States digital tower status | Digital Towers", "A dated tracker of the FAA remote and digital tower program: design approval, AIP guidance, contract tower grants, test sites and the history behind them.", body)

def build_static():
    expl = '''<div class="wrap" style="padding-top:28px"><div class="prose"><div class="eyebrow">Explainer</div><h1 style="font-size:clamp(30px,4.5vw,46px)">What is a digital tower?</h1>
<p class="mute" style="margin-top:14px">A remote or digital tower replaces the view from a control tower window with sensors and displays. The FAA describes it as day and night optical cameras plus infrared or thermal cameras, so controller displays can sit away from the airport. <a href="https://www.faa.gov/airports/planning_capacity/non_federal/remote_tower_systems" rel="noopener" target="_blank">FAA</a></p>
<h2>The terms</h2><ul><li><b>Remote tower.</b> Sensors at the airport, controllers somewhere else. Örnsköldsvik in Sweden began H24 remote operation in April 2015.</li><li><b>Remote tower centre.</b> One facility serving one or several airports, for example Bodø in Norway, which Avinor lists as serving 14 airports.</li><li><b>Digital tower.</b> The same sensor-based technology, used with or without a remote location. FAA guidance now uses "digital tower" for what it previously called remote towers.</li><li><b>Hybrid.</b> Controllers keep the window view and add camera video, as planned at Manchester and Farnborough. It is not a remote tower.</li><li><b>Contingency.</b> A backup position for when the main tower is unavailable, such as the Heathrow facility unveiled in 2009.</li></ul>
<h2>Standards</h2><p>In Europe, EUROCAE ED-240A sets minimum performance standards for remote tower optical systems. In the United States the FAA publishes a concept of operations, operational safety assessment, visual requirements and draft technical requirements, and evaluates designs at its Technical Center. See the <a href="/library/">library</a> and the <a href="/united-states/">US tracker</a>.</p>
<h2>What this site does not say</h2><p>It does not say any system is safe or approved for a particular use, and it is not operational information. Status and dates come from the linked public sources and are labelled with a confidence level.</p></div></div>'''
    page("/what-is-a-digital-tower/", "What is a digital tower? | Digital Towers", "Plain definitions of remote tower, remote tower centre, digital tower, hybrid and contingency facilities, with the standards behind them.", expl)
    lib = "".join(f'<li><a href="{u}" rel="noopener" target="_blank">{esc(n)}</a><div class="xs faint">{esc(d)}</div></li>' for n, u, d in [
        ("FAA Remote Tower Systems page", "https://www.faa.gov/airports/planning_capacity/non_federal/remote_tower_systems", "Concept of operations, safety assessment, requirements. Last updated 6 Feb 2025."),
        ("AIP Program Guidance Letter 26-06", "https://www.faa.gov/airports/aip/guidance_letters/aip_pgl_26_06", "28 Sep 2026. Digital airport traffic control tower systems."),
        ("FAA Digital Tower Systems page", "https://www.faa.gov/airports/planning_capacity/non_federal/digital_tower_systems", "Renamed from Remote Tower Systems; last updated 4 Sep 2026."),
        ("FAA Contract Tower Competitive Grant Program", "https://www.faa.gov/iija/airport-infrastructure/fct", "FY27 round open 18 Sep to 19 Oct 2026."),
        ("EUROCAE ED-240A", "https://www.eurocae.net/product/ed-240a-minimum-aviation-system-performance-standards-masps-for-remote-tower-optical-systems", "Minimum aviation system performance standards for remote tower optical systems."),
        ("Avinor remote towers", "https://om.avinor.no/en/aviation-safety/remote-controlled-towers", "Implementation list for the Bodø centre."),
        ("LFV remote tower services", "https://lfv.se/en/services/airport-services/remote-tower-services", "Swedish centres and airports."),
        ("IAA remote towers", "https://www.iaa.ie/air-traffic-management/innovation/remote-towers", "Cork and Shannon trials."),
        ("DFS remote tower centre project (PDF)", "https://eu-lac-app.eu/public/uploads/DFS_Projekt_RTC_20231024_eng.pdf", "Leipzig centre status, October 2023."),
        ("Reason Foundation: FAA reauthorization and remote towers", "https://reason.org/aviation-policy-news/faa-reauthorization-boosts-u-s-remote-towers", "Summary of Section 621, 2024."),
        ("Wikipedia: Remote and virtual tower", "https://en.wikipedia.org/wiki/Remote_and_virtual_tower", "Secondary overview with citations. Used as a lead, not as a sole source for high-confidence entries.")])
    docs = "".join(f'<li><a href="/docs/faa/{fn}">{esc(t)}</a> <span class="faint small">{fdate(d)}</span></li>' for t, d, fn in EN["faa_docs"] if os.path.exists(BASE + "/docs_faa/" + fn))
    page("/library/", "Library | Digital Towers", "Primary documents and references on remote and digital towers: FAA requirements, EUROCAE ED-240A, provider pages and policy summaries.", f'<div class="wrap" style="padding-top:28px"><h1 style="font-size:clamp(30px,4.5vw,46px)">Library</h1><h2 style="margin:26px 0 12px">FAA documents (copies)</h2><div class="card"><ul style="margin:0;padding-left:18px;display:grid;gap:8px">{docs}</ul></div><h2 style="margin:34px 0 12px">References</h2><div class="card"><ul style="margin:0;padding-left:18px;display:grid;gap:12px">{lib}</ul></div></div>')
    credits = "".join(f'<li>{esc(v["artist"])}, <a href="{esc(v["page"])}" rel="noopener">{esc(v["title"])}</a>, {esc(v["license"])} ({esc(k)})</li>' for k, v in sorted(PH.items()) if k not in NO_PHOTO)
    about = f'''<div class="wrap" style="padding-top:28px"><div class="prose"><h1 style="font-size:clamp(30px,4.5vw,46px)">About and method</h1>
<p class="mute" style="margin-top:14px">Digital Towers is an independent reference to remote and digital air traffic control towers. It is built only from public sources. It is not affiliated with, endorsed by, or speaking for the FAA or any other government body, and it is not for operational use.</p>
<h2>How entries are made</h2><ul><li>Every fact on a tower page carries the URL of the public page it came from.</li><li><b>Status</b>: operational, trial, planned, decommissioned, cancelled or unverified. Unverified means the last source we found is old and no go-live notice turned up.</li><li><b>Confidence</b>: high when an operator, regulator or the airport states the fact; medium when a vendor or trade press does; low when the evidence is old, secondary or single-sourced.</li><li>Hybrid and contingency facilities are listed with their own type and are not counted as remote towers in the headline claim.</li><li>Coordinates come from OurAirports (public domain) by ICAO code. Centres without a code are placed approximately and marked.</li></ul>
<h2>News</h2><p>A scheduled job reads public feeds (Google News search, Federal Register API, CANSO, NATS, AVweb, Aviation Tech Today, Airport Improvement), keeps only items that match remote or digital tower terms, removes duplicates, tags them, and puts new ones in a review queue. They publish after 24 hours unless flagged. The FAA website and transportation.gov refuse automated requests from server addresses (even their robots.txt), so FAA coverage comes from the Federal Register API and from Google News searches limited to faa.gov and transportation.gov. The Congress.gov API needs a free key and is not wired yet. Items that look like opinion pieces or use risky wording are held for a person.</p>
<h2>Corrections</h2><p>Use "Suggest a correction" on any tower page, which opens an issue on <a href="https://github.com/adam-rhodes/digitaltowers">GitHub</a> with a public source link.</p>
<h2>Reuse</h2><p>The dataset is free to reuse with attribution to digitaltowers.org: <a href="/data/">downloads</a>. Map data © OpenStreetMap contributors (ODbL), tiles by Protomaps, rendered with MapLibre GL.</p>
<h2>Photo credits</h2><ul class="small mute">{credits}</ul></div></div>'''
    page("/about/", "About and method | Digital Towers", "How Digital Towers is sourced, labelled and updated; limits, corrections, reuse terms and photo credits.", about)
    dl = f'''<div class="wrap" style="padding-top:28px"><div class="prose"><h1 style="font-size:clamp(30px,4.5vw,46px)">Data</h1><p class="mute" style="margin-top:14px">{len(T)} sites, regenerated with the site. Free to reuse with attribution to digitaltowers.org. Statuses and confidence are defined on the <a href="/about/">about page</a>.</p>
<div class="grid g2" style="margin-top:20px"><a class="card flat" href="/data/towers.json" style="color:var(--ink)"><h3>towers.json</h3><p class="small mute" style="margin:6px 0 0">Full records with facts and source URLs.</p></a><a class="card flat" href="/data/towers.csv" style="color:var(--ink)"><h3>towers.csv</h3><p class="small mute" style="margin:6px 0 0">One row per site.</p></a><a class="card flat" href="/data/towers.geojson" style="color:var(--ink)"><h3>towers.geojson</h3><p class="small mute" style="margin:6px 0 0">Points for mapping tools.</p></a><a class="card flat" href="/data/entities.json" style="color:var(--ink)"><h3>entities.json</h3><p class="small mute" style="margin:6px 0 0">Vendors, providers, regulators, programs and the US timeline.</p></a></div></div></div>'''
    page("/data/", "Data downloads | Digital Towers", "Download the Digital Towers dataset as JSON, CSV or GeoJSON.", dl, jsonld={"@context": "https://schema.org", "@type": "Dataset", "name": "Remote and digital air traffic control towers", "description": "Sourced list of remote, digital and hybrid tower sites.", "url": SITE + "/data/", "license": "https://creativecommons.org/licenses/by/4.0/", "distribution": [{"@type": "DataDownload", "encodingFormat": "application/json", "contentUrl": SITE + "/data/towers.json"}, {"@type": "DataDownload", "encodingFormat": "text/csv", "contentUrl": SITE + "/data/towers.csv"}]})

def build_map():
    chips = ""
    body = f'''<div class="mapwrap"><div id="map" aria-label="World map of remote and digital towers"></div>
<aside class="mpanel" aria-label="Tower list"><div class="sheetbar"><button type="button" aria-label="Resize panel" onclick="this.closest('.mpanel').classList.toggle('min')"></button></div><div class="ph1" id="mfilters"><input id="mq" type="search" placeholder="Search {len(T)} towers" aria-label="Search towers"><div class="chips" id="mchips"></div>
<div class="chips"><select id="mcountry" aria-label="Country"><option value="">All countries</option></select><select id="mvendor" aria-label="Vendor"><option value="">All vendors</option></select></div>
<div class="chips" style="align-items:center;justify-content:space-between"><span class="small mute" id="mcount"></span><span><button class="chip" id="mlinks" type="button" aria-pressed="true">Connections</button> <button class="chip" id="mfit" type="button">Reset view</button> <a class="chip" href="/connections/">Connections view</a></span></div></div>
<div class="mlist" id="mlist"></div><div class="mdetail" id="mdetail" hidden></div></aside>
<div class="legend"><span style="--c:#5ed39a"><i></i>Operational</span><span style="--c:#7aa7ff"><i></i>Trial</span><span style="--c:#c4b5fd"><i></i>Planned</span><span style="--c:#9aa2b1"><i></i>Unverified</span><span style="--c:#ff6b6b"><i></i>Decommissioned or cancelled</span><span class="faint">White ring: remote tower centre</span></div></div>'''
    sc = MAPJS + '<script>fetch("/data/towers.json?v=' + VER + '").then(function(r){return r.json()}).then(function(d){DTMap(d.towers)});</script>'
    page("/map/", "World map of remote and digital towers | Digital Towers", f"Interactive map of {len(T)} remote, digital and hybrid air traffic control towers with status, vendor, provider and the connections between airports and centres.", body, MAPASSETS, sc, body_class="maponly")

def build_redirects():
    try: old = [l.strip() for l in open(BASE + "/old/dt_sitemap_urls.txt") if l.strip()]
    except Exception: old = []
    new = {p for p, _ in PAGES}
    idx = {}
    for t in T:
        for k in (t["id"], (t["icao"] or "").lower(), (t["iata"] or "").lower()):
            if k: idx.setdefault(k, t["id"])
    vend = {v["id"] for v in EN["vendors"]}; ops = {a["id"] for a in EN["ansps"]}
    def target(p):
        p = p.replace(SITE, "")
        m = re.match(r"/airports/([^/]+?)(?:\.html)?/?$", p)
        if m and m.group(1) in idx: return f"/towers/{idx[m.group(1)]}/"
        m = re.match(r"/(?:vendors|operators|regulators)/([^/]+?)(?:\.html)?/?$", p)
        if m:
            k = m.group(1).replace("-technologies", "").replace("-collins-aerospace", "").replace("rtx-collins", "frequentis")
            if k in vend: return f"/vendors/{k}/"
            if k in ops: return f"/operators/{k}/"
            if "/regulators/" in p: return "/regulators/"
        m = re.match(r"/([^/]+?)(?:\.html)?/?$", p)
        if m:
            k = m.group(1)
            if k in vend: return f"/vendors/{k}/"
            if k in ops: return f"/operators/{k}/"
        if re.search(r"faa|reauth|cancelled|history|coalition", p): return "/united-states/"
        if re.search(r"map|workstation", p): return "/map/"
        if re.search(r"directory|airports|explore|remote-tower-center|remote-tower-map", p): return "/towers/"
        if re.search(r"standard|library|ed-240|docs", p): return "/library/"
        if re.search(r"what-is|remote-vs|vs-digital|remote-tower|digital-tower", p): return "/what-is-a-digital-tower/"
        if re.search(r"vendor", p): return "/vendors/"
        if re.search(r"operator|regulator|canso|easa|icao|ifatca|eurocae", p): return "/regulators/"
        return "/"
    n = 0
    for u in old:
        p = u.replace(SITE, "")
        if p in new or p in ("/sitemap.xml",): continue
        fp = DIST + p + ("index.html" if p.endswith("/") else "")
        if os.path.exists(fp): continue
        t = target(p)
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        open(fp, "w", encoding="utf8").write(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Moved | Digital Towers</title><meta name="robots" content="noindex"><link rel="canonical" href="{SITE}{t}"><meta http-equiv="refresh" content="0;url={t}"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="stylesheet" href="/assets/site.css"></head><body><main class="wrap" style="padding-top:60px"><p>This page moved to <a href="{t}">{SITE}{t}</a>.</p></main></body></html>')
        n += 1
    return n

def build_misc():
    sm = "".join(f"<url><loc>{SITE}{p}</loc><lastmod>{d}</lastmod></url>" for p, d in sorted(PAGES))
    open(DIST + "/sitemap.xml", "w").write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>')
    open(DIST + "/robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    open(DIST + "/llms.txt", "w").write(f"# Digital Towers\n> Sourced reference to remote and digital air traffic control towers: {len(T)} sites in {META['countries']} countries. Every fact links to a public source.\n\n- Map: {SITE}/map/\n- Towers: {SITE}/towers/\n- Data: {SITE}/data/towers.json\n- United States tracker: {SITE}/united-states/\n- News: {SITE}/news/\n")

def main():
    global DIST
    if os.path.exists(DIST): shutil.rmtree(DIST)
    os.makedirs(DIST)
    build_assets(); build_home(); build_news(); build_directory()
    for t in T: build_tower(t)
    build_countries(); build_entities(); build_us(); build_static(); build_map()
    import dt_views; dt_views.build_all(sys.modules[__name__])
    nred = build_redirects(); build_misc()
    print("built pages", len(PAGES), "redirect stubs", nred, "towers", len(T))
    if "--deploy" in sys.argv: deploy()

def deploy():
    ts = NOW.strftime("%Y%m%dT%H%M%SZ")
    os.makedirs(BASE + "/backups", exist_ok=True)
    subprocess.run(["tar", "czf", f"{BASE}/backups/dt_web_{ts}.tgz", "--exclude=./docs", "--exclude=./data/adsb", "--exclude=./tiles", "-C", WEB, "."], check=False)
    for old in sorted(glob.glob(BASE + "/backups/dt_web_*.tgz"))[:-6]: os.remove(old)
    if os.path.isdir(WEB + "/docs") is False and os.path.isdir(BASE + "/docs_faa"): pass
    ex = ["--exclude=/docs/", "--exclude=/data/adsb/", "--exclude=/data/adsb_uptime.jsonl", "--exclude=/e0266*.txt", "--exclude=/_to_delete/", "--exclude=/adsb_health_probe.py"]
    r = subprocess.run(["rsync", "-a", "--delete"] + ex + [DIST + "/", WEB + "/"])
    print("rsync exit", r.returncode)
    subprocess.run(["chmod", "-R", "a+rX", WEB])
if __name__ == "__main__": main()
