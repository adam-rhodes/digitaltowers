#!/usr/bin/env python3
"""Digital Towers news pipeline. Reads public feeds, filters to remote/digital tower items, dedupes, tags, queues new items
for 24 hours, then publishes them unless flagged. Files in /root/dt_site/data:
  news.json (published), news_queue.json (review queue), news_flags.json (hold/ban lists a person edits), news_status.json (last run).
Run: fetch_news.py   (cron every 4 hours, then dt_build.py --deploy)"""
import json, os, re, sys, hashlib, datetime, urllib.request, urllib.parse, email.utils, html, xml.etree.ElementTree as ET, fcntl
BASE = "/root/dt_site"; D = BASE + "/data/"
UA = {"User-Agent": "Mozilla/5.0 (compatible; DigitalTowersBot/1.0; +https://digitaltowers.org/about/)"}
NOW = datetime.datetime.now(datetime.timezone.utc)
HOLD_HOURS = 24
KW = re.compile(r"(remote|digital|virtual)[ -](air[ -]traffic[ -])?(control[ -])?tower|remote air traffic|digital air traffic|remote tower|digital tower|multiple remote tower|virtual tower|remote and digital tower", re.I)
RISKY = re.compile(r"\b(crash|crashed|killed|dies|died|fatal|lawsuit|sued|collision|near[- ]miss|incident|investigation|outage|hack|breach)\b", re.I)
FEEDS = [
 ("Google News: digital or remote tower", "https://news.google.com/rss/search?q=%22digital+tower%22+OR+%22remote+tower%22+airport+when%3A30d&hl=en-US&gl=US&ceid=US:en", "rss", False),
 ("Google News: FAA remote tower", "https://news.google.com/rss/search?q=FAA+%22remote+tower%22+OR+%22digital+tower%22+when%3A30d&hl=en-US&gl=US&ceid=US:en", "rss", False),
 ("Google News: remote tower Europe", "https://news.google.com/rss/search?q=%22remote+tower%22+OR+%22digital+tower%22+Saab+OR+Frequentis+OR+Kongsberg+OR+Indra+OR+Searidge+when%3A30d&hl=en-GB&gl=GB&ceid=GB:en", "rss", False),
 ("Federal Register: remote tower", "https://www.federalregister.gov/api/v1/documents.json?conditions%5Bterm%5D=%22remote+tower%22&order=newest&per_page=15", "fedreg", False),
 ("Federal Register: digital tower", "https://www.federalregister.gov/api/v1/documents.json?conditions%5Bterm%5D=%22digital+tower%22&order=newest&per_page=15", "fedreg", False),
 ("CANSO", "https://canso.org/feed/", "rss", True),
 ("NATS", "https://www.nats.aero/feed/", "rss", True),
 ("AVweb", "https://www.avweb.com/feed/", "rss", True),
 ("Aviation Tech Today", "https://www.aviationtoday.com/feed/", "rss", True),
 ("Airport Improvement", "https://airportimprovement.com/rss", "rss", True),
]
COUNTRIES = ["United States","Norway","Sweden","Finland","Denmark","Germany","United Kingdom","Ireland","Netherlands","Belgium","France","Spain","Italy","Switzerland","Austria","Hungary","Poland","Romania","Estonia","Latvia","Lithuania","Canada","Brazil","Australia","New Zealand","Singapore","Hong Kong","Japan","India","Saudi Arabia","Iceland","Greenland"]
CMAP = {"U.S.": "United States", "US ": "United States", "FAA": "United States", "UK ": "United Kingdom", "British": "United Kingdom", "German": "Germany", "Swedish": "Sweden", "Norwegian": "Norway", "Finnish": "Finland", "Danish": "Denmark", "French": "France", "Spanish": "Spain", "Italian": "Italy", "Dutch": "Netherlands", "Swiss": "Switzerland", "Irish": "Ireland", "Polish": "Poland", "Canadian": "Canada", "Australian": "Australia", "Saudi": "Saudi Arabia", "Brazilian": "Brazil", "Hungarian": "Hungary", "Estonian": "Estonia"}
ORGS = ["Saab","Frequentis","Kongsberg","Indra","Searidge","Adacel","FerroNATS","Avinor","LFV","NATS","DFS","HungaroControl","Naviair","Fintraffic","EANS","PANSA","ENAV","DSNA","skyguide","NAV CANADA","Airservices","FAA","EASA","ICAO","EUROCAE","CANSO","Congress"]
TOPICS = [("Procurement", r"contract|order|selects|selected|awarded|tender|rfp|wins|procure"), ("Policy", r"bill|congress|rule|regulat|policy|guidance|reauthori|legislat|senate|house "), ("Funding", r"fund|grant|aip|\$\d"), ("Operations", r"opens|opened|live|operational|first|inaugurat|goes|launch|commission"), ("Safety", r"safety|certif|approval|approved|standard")]
def log(*a): print(datetime.datetime.utcnow().strftime("%H:%M:%S"), *a, flush=True)
def load(f, d):
    try: return json.load(open(D + f, encoding="utf8"))
    except Exception: return d
def save(f, o): json.dump(o, open(D + f + ".tmp", "w", encoding="utf8"), ensure_ascii=False, indent=1); os.replace(D + f + ".tmp", D + f)
def get(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=25).read()
def norm(u):
    p = urllib.parse.urlsplit(u); q = [(k, v) for k, v in urllib.parse.parse_qsl(p.query) if not k.startswith("utm_")]
    return urllib.parse.urlunsplit((p.scheme, p.netloc.lower(), p.path.rstrip("/"), urllib.parse.urlencode(q), ""))
def tkey(t): return re.sub(r"[^a-z0-9]", "", re.sub(r"\s+-\s+[^-]+$", "", t.lower()))[:70]
def strip(s): return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s or ""))).strip()
def parse_rss(b, src):
    out = []
    root = ET.fromstring(b)
    for it in list(root.iter("item")) + list(root.iter("{http://www.w3.org/2005/Atom}entry")):
        g = lambda n: (it.findtext(n) or it.findtext("{http://www.w3.org/2005/Atom}" + n) or "")
        title = strip(g("title")); link = g("link")
        if not link:
            l = it.find("{http://www.w3.org/2005/Atom}link"); link = l.get("href") if l is not None else ""
        pd = g("pubDate") or g("published") or g("updated")
        try: dt = email.utils.parsedate_to_datetime(pd) if "," in pd else datetime.datetime.fromisoformat(pd.replace("Z", "+00:00"))
        except Exception: dt = NOW
        s = it.find("source"); source = (s.text if s is not None and s.text else src)
        summ = strip(g("description") or g("summary") or g("{http://purl.org/rss/1.0/modules/content/}encoded"))
        out.append({"title": title, "url": link.strip(), "date": dt.astimezone(datetime.timezone.utc).strftime("%Y-%m-%d"), "source": source, "summary": summ[:400]})
    return out
def parse_fedreg(b):
    out = []
    for r in json.loads(b).get("results", []):
        out.append({"title": r["title"], "url": r["html_url"], "date": r["publication_date"], "source": "Federal Register (" + ", ".join(a.get("name", "") for a in r.get("agencies", [])[:1]) + ")", "summary": strip(r.get("abstract") or "")[:400]})
    return out
def tag(n):
    text = n["title"] + " " + n["summary"]; tags = []
    for c in COUNTRIES:
        if re.search(r"\b" + re.escape(c) + r"\b", text) and c not in tags: tags.append(c)
    for k, v in CMAP.items():
        if k in text and v not in tags: tags.append(v)
    for o in ORGS:
        if re.search(r"\b" + re.escape(o) + r"\b", text) and o not in tags: tags.append(o)
    for t, rx in TOPICS:
        if re.search(rx, text, re.I): tags.append(t)
    return tags[:8] or ["General"]
def main():
    lk = open(BASE + "/data/.news.lock", "w")
    try: fcntl.flock(lk, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError: log("already running"); return
    pub = load("news.json", []); queue = load("news_queue.json", []); flags = load("news_flags.json", {"hold": [], "ban": []})
    seen_url = {norm(n["url"]) for n in pub + queue}; seen_t = {tkey(n["title"]) for n in pub + queue}
    ok = 0; status = []; added = 0
    for name, url, kind, filt in FEEDS:
        try:
            b = get(url); items = parse_fedreg(b) if kind == "fedreg" else parse_rss(b, name); ok += 1
            n0 = len(items)
            def okitem(i):
                t = i["title"] + " " + i["summary"]
                if not (i["url"] and i["title"]): return False
                if kind == "fedreg": return True
                if KW.search(t): return True
                if "Google" in name: return bool(re.search(r"\btower", t, re.I) and re.search(r"remote|digital|virtual", t, re.I) and re.search(r"air traffic|airport|atc|aviation", t, re.I))
                return False
            items = [i for i in items if okitem(i)]
            new = 0
            for i in items:
                nu, tk = norm(i["url"]), tkey(i["title"])
                if nu in seen_url or tk in seen_t: continue
                try:
                    if (NOW.date() - datetime.date.fromisoformat(i["date"])).days > 120: continue
                except Exception: pass
                seen_url.add(nu); seen_t.add(tk)
                i["id"] = hashlib.sha1(nu.encode()).hexdigest()[:12]; i["tags"] = tag(i); i["feed"] = name
                i["first_seen"] = NOW.strftime("%Y-%m-%dT%H:%M:%SZ"); i["publish_after"] = (NOW + datetime.timedelta(hours=HOLD_HOURS)).strftime("%Y-%m-%dT%H:%M:%SZ")
                i["flag"] = "risky wording: check before publishing" if RISKY.search(i["title"]) else None
                queue.append(i); new += 1; added += 1
            status.append({"feed": name, "ok": True, "items": n0, "matched": len(items), "new": new}); log(name, "items", n0, "matched", len(items), "new", new)
        except Exception as e:
            status.append({"feed": name, "ok": False, "error": str(e)[:100]}); log(name, "ERROR", e)
    # promote
    keep = []; promoted = 0
    hold = [h.lower() for h in flags.get("hold", [])]; ban = [b.lower() for b in flags.get("ban", [])]
    for q in queue:
        blob = (q["url"] + " " + q["title"] + " " + q["id"]).lower()
        if any(b in blob for b in ban): continue
        if any(h in blob for h in hold): q["flag"] = q.get("flag") or "held by editor"
        if not q.get("flag") and q["publish_after"] <= NOW.strftime("%Y-%m-%dT%H:%M:%SZ"):
            pub.append({k: q[k] for k in ("id", "title", "url", "source", "date", "tags")}); promoted += 1
        else: keep.append(q)
    pub.sort(key=lambda n: n["date"], reverse=True)
    save("news.json", pub); save("news_queue.json", keep)
    save("news_status.json", {"last_run": NOW.strftime("%Y-%m-%d %H:%M"), "feeds_ok": ok, "feeds_total": len(FEEDS), "added_to_queue": added, "promoted": promoted, "queue_len": len(keep), "published_total": len(pub), "feeds": status})
    log("done: queued", added, "promoted", promoted, "queue", len(keep), "published", len(pub))
if __name__ == "__main__": main()
