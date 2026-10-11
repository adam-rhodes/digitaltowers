#!/usr/bin/env python3
"""Writes /root/dt_site/data/news_verify.json: evidence that the 24 h hold promotes. Run once after the first scheduled run past the hold (cron one-shot).
Reads news_status.json, news_promotions.jsonl, news.json and the live page https://digitaltowers.org/news/."""
import json, datetime, urllib.request, os
D = "/root/dt_site/data/"
st = json.load(open(D + "news_status.json")); pub = json.load(open(D + "news.json"))
promos = [json.loads(l) for l in open(D + "news_promotions.jsonl")] if os.path.exists(D + "news_promotions.jsonl") else []
page = urllib.request.urlopen(urllib.request.Request("https://digitaltowers.org/news/", headers={"User-Agent": "dt-verify"}), timeout=30).read().decode("utf8", "ignore")
on_page = [p["title"] for p in promos if p["title"][:40] in page.replace("&amp;", "&").replace("&#39;", "'")]
out = {"checked_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "last_run": st.get("last_run"), "promoted_last_run": st.get("promoted"), "promotion_records": len(promos),
       "published_total": len(pub), "queue_len": st.get("queue_len"), "held_flagged": st.get("held_flagged"), "promoted_titles_on_live_page": len(on_page),
       "result": "PROMOTION OBSERVED" if promos and on_page else "NO PROMOTION OBSERVED YET", "sample": promos[-3:]}
json.dump(out, open(D + "news_verify.json", "w"), ensure_ascii=False, indent=1); print(json.dumps(out, ensure_ascii=False)[:800])
