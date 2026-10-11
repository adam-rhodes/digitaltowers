#!/usr/bin/env python3
"""Compile curated tower data into data/towers.json, towers.geojson, towers.csv. Run on the droplet from /root/dt_site."""
import csv, json, os, sys, datetime, collections
BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
from dt_data_c import TOWERS, S
import dt_entities as E

oa = {}
with open(BASE + "/data/ourairports.csv", newline="", encoding="utf8") as f:
    for r in csv.DictReader(f):
        ic = r.get("ident") or ""
        if len(ic) == 4 and r["type"] != "closed":
            oa[ic] = (float(r["latitude_deg"]), float(r["longitude_deg"]), r.get("iata_code") or "", r.get("elevation_ft") or "")
missing = []
for t in TOWERS:
    ic = t.get("icao") or ""
    if t["lat"] is None:
        if ic in oa: t["lat"], t["lon"] = oa[ic][0], oa[ic][1]
        else: missing.append(t["id"])
    if ic in oa: t["iata"] = oa[ic][2]; t["elev_ft"] = oa[ic][3]
    else: t["iata"] = ""; t["elev_ft"] = ""
if missing: print("NO COORDS:", missing); sys.exit(1)
# jitter co-located markers so both stay clickable
seen = collections.defaultdict(int)
for t in TOWERS:
    k = (round(t["lat"], 3), round(t["lon"], 3)); n = seen[k]; seen[k] += 1
    t["lat"] = round(t["lat"] + n * 0.006, 5); t["lon"] = round(t["lon"] + n * 0.009, 5)
ids = {t["id"] for t in TOWERS}
for t in TOWERS:
    assert not t["controlled_from"] or t["controlled_from"] in ids, (t["id"], t["controlled_from"])
    t["dates"] = [{"d": a, "t": b} for a, b in t["dates"]]
# connections
by = {t["id"]: t for t in TOWERS}
for t in TOWERS:
    c = []
    if t["controlled_from"]:
        h = by[t["controlled_from"]]; c.append({"rel": "controlled from", "id": h["id"], "name": h["name"]})
    if t["kind"] == "rtc":
        for s in TOWERS:
            if s["controlled_from"] == t["id"]: c.append({"rel": "serves", "id": s["id"], "name": s["name"]})
    t["connections"] = c
def count(f): return sum(1 for t in TOWERS if f(t))
meta = {
  "generated": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
  "count": len(TOWERS), "countries": len({t["country"] for t in TOWERS}),
  "by_status": dict(collections.Counter(t["status"] for t in TOWERS)),
  "license": "Compiled facts with source URLs per fact; coordinates from OurAirports (public domain) where an ICAO code exists. Free to reuse with attribution to digitaltowers.org.",
  "note": "Statuses: operational, trial, planned, decommissioned, cancelled, unverified. Confidence: high, medium, low. Hybrid and contingency kinds are not remote towers.",
}
os.makedirs(BASE + "/data", exist_ok=True)
json.dump({"meta": meta, "towers": TOWERS}, open(BASE + "/data/towers.json", "w"), ensure_ascii=False, indent=1)
json.dump({"vendors": E.VENDORS, "ansps": E.ANSPS, "regulators": E.REGULATORS, "programs": E.PROGRAMS, "us_timeline": E.US_TIMELINE, "faa_docs": E.FAA_DOCS}, open(BASE + "/data/entities.json", "w"), ensure_ascii=False, indent=1)
gj = {"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [t["lon"], t["lat"]]},
      "properties": {k: t[k] for k in ("id", "name", "icao", "country", "kind", "status", "conf", "ansp", "controlled_from")} | {"vendors": ", ".join(t["vendors"])}} for t in TOWERS]}
json.dump(gj, open(BASE + "/data/towers.geojson", "w"), ensure_ascii=False)
with open(BASE + "/data/towers.csv", "w", newline="", encoding="utf8") as f:
    w = csv.writer(f); w.writerow(["id", "name", "icao", "country", "kind", "status", "confidence", "vendors", "ansp", "controlled_from", "lat", "lon", "sources"])
    for t in TOWERS:
        w.writerow([t["id"], t["name"], t["icao"], t["country"], t["kind"], t["status"], t["conf"], "; ".join(t["vendors"]), t["ansp"], t["controlled_from"], t["lat"], t["lon"], " ".join(sorted({x["u"] for x in t["facts"]}))])
print("compiled", len(TOWERS), meta["by_status"], "countries", meta["countries"])
