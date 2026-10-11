#!/usr/bin/env python3
"""sites3_1011 patcher for /root/dt_site. Idempotent: skips a patch whose marker is already present. Asserts every old string exists."""
import sys, re
B = "/root/dt_site/"
def rep(path, pairs):
    s = open(B + path, encoding="utf8").read()
    for old, new, marker in pairs:
        if marker and marker in s: print("skip", path, marker[:40]); continue
        assert old in s, (path, old[:80])
        assert s.count(old) == 1, (path, "not unique", old[:80])
        s = s.replace(old, new)
        print("patched", path, (marker or old)[:50])
    open(B + path, "w", encoding="utf8").write(s)

# ---------------- dt_compile.py
rep("dt_compile.py", [
 ("from dt_data_c import TOWERS, S", "from dt_data_d import TOWERS, S", "from dt_data_d import"),
 ("import dt_entities as E\n", "import dt_entities as E\nimport dt_entities_d\n", "import dt_entities_d"),
 ('    t["dates"] = [{"d": a, "t": b} for a, b in t["dates"]]\n',
  '    t["dates"] = [({"d": x[0], "t": x[1], "u": S[x[2]]} if len(x) > 2 else {"d": x[0], "t": x[1]}) for x in t["dates"]]\n', '"u": S[x[2]]'),
 ("# connections\n",
  '''# photos (credit per ICAO) so the map panel can show one
_NOPH = {"EGPE", "LHBP", "EGDG", "KACY", "ENBO"}
try: _ph = json.load(open(BASE + "/data/photos.json", encoding="utf8"))
except Exception: _ph = {}
for t in TOWERS:
    p = _ph.get(t.get("icao") or "")
    t["photo"] = ({"file": p["file"], "artist": p["artist"], "license": p["license"], "page": p["page"]} if p and (t.get("icao") not in _NOPH) else None)
# connections
''', "_NOPH"),
 ('"note": "Statuses:', '"by_kind": dict(collections.Counter(t["kind"] for t in TOWERS)), "note": "Statuses:', '"by_kind"'),
 ('"us_timeline": E.US_TIMELINE, "faa_docs": E.FAA_DOCS}', '"us_timeline": E.US_TIMELINE, "faa_docs": E.FAA_DOCS, "coverage": E.COVERAGE, "reflists": E.REFLISTS}', '"coverage": E.COVERAGE'),
])

# ---------------- dt_build.py
rep("dt_build.py", [
 ('"test_site": "Test or validation site"}', '"test_site": "Test or validation site", "remote_afis": "Remote air-ground service (not air traffic control)"}', '"remote_afis": "Remote air-ground'),
 ('"test_site": "a test or validation site rather than an operating tower"}', '"test_site": "a test or validation site rather than an operating tower",\n              "remote_afis": "a remote aerodrome air-ground (RADIO) service: an officer elsewhere gives advisory information by camera, which is not air traffic control"}', '"remote_afis": "a remote aerodrome'),
 ('NAV = [("Map", "/map/"), ("Towers", "/towers/"), ("News", "/news/"), ("United States", "/united-states/"), ("Vendors", "/vendors/"), ("About", "/about/")]',
  'NAV = [("Map", "/map/"), ("Towers", "/towers/"), ("Connections", "/connections/"), ("Timeline", "/timeline/"), ("News", "/news/"), ("United States", "/united-states/"), ("Vendors", "/vendors/"), ("About", "/about/")]', '("Connections", "/connections/")'),
 ('<li><a href="/regulators/">Regulators and standards</a></li></ul></div>', '<li><a href="/regulators/">Regulators and standards</a></li><li><a href="/connections/">Connections</a></li><li><a href="/timeline/">Timeline</a></li><li><a href="/coverage/">Coverage and gaps</a></li></ul></div>', '/coverage/">Coverage'),
 ('(("dt_site.css", "site.css"), ("dt_map.js", "map.js"), ("dt_site.js", "site.js"))', '(("dt_site.css", "site.css"), ("dt_map.js", "map.js"), ("dt_site.js", "site.js"), ("conn.js", "conn.js"))', '"conn.js"'),
 ('<div class="strip">{strip}</div>',
  '<p class="small mute" style="margin-top:16px;max-width:74ch">{len(T)} sites = ' + '{", ".join(str(v) + " " + k for k, v in status_counts.most_common())}. {sum(1 for t in T if t["kind"] in ("remote_tower","rtc","digital_tower","remote_afis"))} are remote towers, centres, digital towers or remote air-ground services; the other {sum(1 for t in T if t["kind"] not in ("remote_tower","rtc","digital_tower","remote_afis"))} are hybrid, contingency or test facilities. <a href="/coverage/">What is not covered</a>.</p><div class="strip">{strip}</div>', 'What is not covered'),
 ('<a class="btn" href="/united-states/">United States status</a></div>', '<a class="btn" href="/united-states/">United States status</a><a class="btn" href="/connections/">How towers connect</a></div>', 'How towers connect'),
 ('{len(T)} sites. Filter by status, country or vendor. <a href="/data/">Download the data</a>.</p>', '{len(T)} sites. Filter by status, country or vendor. <a href="/data/">Download the data</a>. Also: <a href="/connections/">connections</a>, <a href="/timeline/">timeline</a>, <a href="/coverage/">coverage and gaps</a>.</p>', 'coverage and gaps</a>.</p>'),
 ('<h2 style="margin:30px 0 12px;font-size:22px">What the sources say</h2>', '<h2 id="sources" style="margin:30px 0 12px;font-size:22px">What the sources say</h2>', 'id="sources"'),
 ('''tl = "".join(f'<li><span class="d">{esc(fdate(d["d"]))}</span><div>{esc(d["t"])}</div></li>' for d in sorted(t["dates"], key=lambda x: x["d"]))''',
  '''tl = "".join(f'<li><span class="d">{esc(fdate(d["d"]))}</span><div>{esc(d["t"])}' + (f' <a class="xs" href="{esc(d["u"])}" rel="noopener" target="_blank">{esc(host(d["u"]))}</a>' if d.get("u") else '') + '</div></li>' for d in sorted(t["dates"], key=lambda x: x["d"]))''', 'if d.get("u") else'),
 ('<dt>Status</dt><dd>{LABEL[t["status"]]}</dd>', '''<dt>Status</dt><dd>{LABEL[t["status"]]}</dd>{('<dt>Regulator</dt><dd>' + esc(t["regulator"]) + '</dd>') if t.get("regulator") else ''}{('<dt>Program</dt><dd><a href="/regulators/#' + esc(t["program"]) + '">' + esc(t["program"]) + '</a></dd>') if t.get("program") else ''}''', "<dt>Regulator</dt>"),
 ('{conn}{v}{av}</div>', '{conn}{v}{av}</div><p class="small" style="margin:6px 0 14px"><a href="/connections/?focus={t["id"]}">Open in the connections view</a> · <a href="/timeline/?tower={t["id"]}">Timeline for this site</a></p>', 'Open in the connections view'),
 ('<div class="note" style="margin-top:16px"><b>Sources disagree on timing.</b> The FAA Remote Tower Systems page, last updated 6 February 2025, says no remote tower system is approved for the NAS and lists no design approval. The September 2026 guidance letter postdates it. Both are linked below.</div>',
  '<div class="note" style="margin-top:16px"><b>Sources disagree on timing.</b> The FAA page for this program, now titled Digital Tower Systems, was last updated 4 September 2026. It does not list the approval and says the FAA will update it when (and if) it issues one. The earlier Remote Tower Systems page, updated 6 February 2025, said no system was approved. The guidance letter PGL 26-06, dated 28 September 2026, states that the FAA granted Frequentis USA an approval on 2 September 2026, with conditions. We show the approval as that letter words it. <a href="https://www.faa.gov/airports/planning_capacity/non_federal/digital_tower_systems" rel="noopener" target="_blank">FAA page</a></div>', 'now titled Digital Tower Systems'),
 ('The FAA newsroom feed blocks automated readers, and the Congress.gov API needs a free key, so neither is wired yet.',
  'The FAA website and transportation.gov refuse automated requests from server addresses (even their robots.txt), so FAA coverage comes from the Federal Register API and from Google News searches limited to faa.gov and transportation.gov. The Congress.gov API needs a free key and is not wired yet. Items that look like opinion pieces or use risky wording are held for a person.', 'Federal Register API and from Google News'),
 ('("FAA Contract Tower Competitive Grant Program",', '("FAA Digital Tower Systems page", "https://www.faa.gov/airports/planning_capacity/non_federal/digital_tower_systems", "Renamed from Remote Tower Systems; last updated 4 Sep 2026."),\n        ("FAA Contract Tower Competitive Grant Program",', 'FAA Digital Tower Systems page'),
 ('<button class="chip" id="mfit" type="button">Reset view</button></span>', '<button class="chip" id="mfit" type="button">Reset view</button> <a class="chip" href="/connections/">Connections view</a></span>', 'Connections view'),
 ('    build_countries(); build_entities(); build_us(); build_static(); build_map()\n', '    build_countries(); build_entities(); build_us(); build_static(); build_map()\n    import dt_views; dt_views.build_all(sys.modules[__name__])\n', 'dt_views.build_all'),
])

# ---------------- dt_map.js
rep("dt_map.js", [
 ("""'<button class="chip" type="button" id="mback">All towers</button><h2>'+esc(t.name)+'</h2><p><span class="pill st-'+t.status+'">'+LABEL[t.status]+'</span> <span class="tag conf-'+t.conf+'">confidence '+t.conf+'</span></p>'""",
  """'<button class="chip" type="button" id="mback">All towers</button><h2>'+esc(t.name)+'</h2><p><span class="pill st-'+t.status+'">'+LABEL[t.status]+'</span> <span class="tag conf-'+t.conf+'">confidence '+t.conf+'</span></p>'+ph""", "+ph"),
 ("    detail.innerHTML='<button", """    var ph=t.photo?'<div class="mphoto"><img src="/'+esc(t.photo.file)+'" alt="" loading="lazy"><div class="cr">Photo: '+esc(t.photo.artist)+', <a href="'+esc(t.photo.page)+'" rel="noopener" target="_blank">'+esc(t.photo.license)+'</a>, via Wikimedia Commons</div></div>':'<div class="mphoto"><div class="ph0">'+esc(t.icao||t.country)+'</div><div class="cr">No openly licensed photo found yet.</div></div>';
    detail.innerHTML='<button""", "var ph=t.photo"),
 ("""'<p style="margin-top:16px"><a class="btn primary" href="/towers/'+esc(t.id)+'/">Open full page</a></p>'""", """'<p style="margin-top:16px"><a class="btn primary" href="/towers/'+esc(t.id)+'/">Open full page</a> <a class="btn" href="/connections/?focus='+esc(t.id)+'">Connections</a></p>'""", "Connections</a></p>"),
])

# ---------------- css
css = open(B + "dt_site.css", encoding="utf8").read()
if "sites3_1011: connections" not in css:
    css += open(B + "css_add.css", encoding="utf8").read()
    open(B + "dt_site.css", "w", encoding="utf8").write(css); print("css appended")
print("patch ok")
