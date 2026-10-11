#!/usr/bin/env python3
"""Fetch one openly licensed lead photo per tower from Wikimedia Commons (via Wikidata ICAO -> English Wikipedia lead image).
Accepts CC0, public domain, CC BY, CC BY-SA only. Writes img/towers/<icao>.jpg and data/photos.json (credit per ICAO)."""
import json, os, re, sys, urllib.request, urllib.parse, html, time
BASE = "/root/dt_site"
UA = {"User-Agent": "DigitalTowersBot/1.0 (https://digitaltowers.org/about/; reference site, low volume)"}
def get(url, tries=3):
    for i in range(tries):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40).read()
        except Exception as e:
            time.sleep(2 + i * 2); err = e
    raise err
towers = json.load(open(BASE + "/data/towers.json"))["towers"]
codes = sorted({t["icao"] for t in towers if t.get("icao")})
q = 'SELECT ?c ?a WHERE { VALUES ?c {%s} ?i wdt:P239 ?c . ?a schema:about ?i ; schema:isPartOf <https://en.wikipedia.org/> . }' % " ".join('"%s"' % c for c in codes)
d = json.loads(get("https://query.wikidata.org/sparql?format=json&query=" + urllib.parse.quote(q)))
title = {}
for b in d["results"]["bindings"]:
    title[b["c"]["value"]] = urllib.parse.unquote(b["a"]["value"].rsplit("/", 1)[1]).replace("_", " ")
print("wikipedia titles", len(title), "of", len(codes))
# lead image names
img = {}
tl = list(title.items())
for i in range(0, len(tl), 40):
    chunk = tl[i:i + 40]
    u = "https://en.wikipedia.org/w/api.php?" + urllib.parse.urlencode({"action": "query", "format": "json", "prop": "pageimages", "piprop": "name", "redirects": 1, "titles": "|".join(t for _, t in chunk)})
    r = json.loads(get(u))["query"]
    redir = {x["from"]: x["to"] for x in r.get("redirects", [])}
    norm = {x["from"]: x["to"] for x in r.get("normalized", [])}
    bytitle = {p["title"]: p.get("pageimage") for p in r["pages"].values()}
    for c, t in chunk:
        t2 = redir.get(norm.get(t, t), norm.get(t, t))
        if bytitle.get(t2): img[c] = bytitle[t2]
print("lead images", len(img))
# commons license check + download
ok = {}
names = sorted(set(img.values()))
info = {}
for i in range(0, len(names), 40):
    chunk = names[i:i + 40]
    u = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({"action": "query", "format": "json", "prop": "imageinfo", "iiprop": "url|size|extmetadata", "iiurlwidth": 1280, "titles": "|".join("File:" + n for n in chunk)})
    r = json.loads(get(u))["query"]
    for p in r["pages"].values():
        if "imageinfo" in p: info[p["title"][5:].replace(" ", "_")] = p["imageinfo"][0]
os.makedirs(BASE + "/img/towers", exist_ok=True)
good = ("cc0", "public domain", "cc by", "cc-by", "pd")
out = {}
for c, n in img.items():
    ii = info.get(n.replace(" ", "_"))
    if not ii: continue
    m = ii["extmetadata"]; lic = (m.get("LicenseShortName", {}).get("value") or "").strip()
    ll = lic.lower()
    if not (ll.startswith("cc by") or ll.startswith("cc0") or "public domain" in ll or ll.startswith("pd")): continue
    if "nc" in ll.split() or "-nc" in ll or "nd" in ll.split(): continue
    if ii["width"] < ii["height"] * 1.1: continue  # landscape only
    art = re.sub(r"<[^>]+>", "", html.unescape(m.get("Artist", {}).get("value", "") or "")).strip()[:80]
    dst = BASE + "/img/towers/%s.jpg" % c.lower()
    try:
        data = get(ii.get("thumburl") or ii["url"])
        open(dst, "wb").write(data)
    except Exception as e:
        print("dl fail", c, e); continue
    out[c] = {"file": "img/towers/%s.jpg" % c.lower(), "title": n.replace("_", " "), "artist": art or "Unknown author", "license": lic, "page": ii.get("descriptionurl"), "w": ii.get("thumbwidth"), "h": ii.get("thumbheight")}
json.dump(out, open(BASE + "/data/photos.json", "w"), indent=1, ensure_ascii=False)
print("photos saved", len(out))
for c, v in sorted(out.items()): print(c, "|", v["title"][:60], "|", v["license"], "|", v["artist"][:30])
