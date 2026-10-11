# -*- coding: utf-8 -*-
"""Digital Towers extra views (sites3_1011): connections graph page, approvals and go-lives timeline, coverage page.
Called from dt_build.main() as dt_views.build_all(<dt_build module>)."""
import json, re, collections, datetime

REMOTE_KINDS = ("remote_tower", "rtc", "digital_tower", "remote_afis")

def classify(text):
    s = text.lower()
    if re.search(r"discontinu|cancel|terminat|postpone|fail|abandon|stopped|closed|decommission|ended|ends\b|ends ", s): return "ended"
    if re.search(r"approv|certif|authoris|authoriz|\bsda\b|design approval", s): return "approval"
    if re.search(r"in service|enters? service|go[- ]?live|goes live|switched to|begins|began|starts\b|started|opened|opens\b|inaugurat|unveiled|activated|first (flight|clearance|airport|digital|production|major)|operational|operated from|operating", s): return "golive"
    if re.search(r"contract|order|select|award|agreement|sign|rfp|tender|announce|proposal|request", s): return "contract"
    return "milestone"

def sortkey(d):
    d = str(d)
    return d + "-00-00"[len(d) - 4:] if re.match(r"^\d{4}(-\d{2}){0,2}$", d) else d

def build_all(B):
    build_graph_data(B)
    build_connections(B)
    build_timeline(B)
    build_coverage(B)

# ------------------------------------------------------------------ graph data
def build_graph_data(B):
    T, EN = B.T, B.EN
    prog = {p["id"]: p["name"] for p in EN["programs"]}
    out = []
    for t in T:
        v = []
        for vn in t["vendors"]:
            ve = B.vendor_of(vn)
            v.append([ve["id"], ve["name"]] if ve else [B.slug(vn), vn])
        a = B.ansp_of(t["ansp"])
        p = [a["id"], a["name"]] if a else ([B.slug(t["ansp"]), t["ansp"]] if t["ansp"] else None)
        r = [B.slug(t["regulator"]), t["regulator"]] if t.get("regulator") else None
        g = [t["program"], prog.get(t["program"], t["program"])] if t["program"] else None
        out.append({"id": t["id"], "n": t["name"], "c": t["country"], "s": t["status"], "k": t["kind"], "i": t["icao"], "v": v, "p": p, "r": r, "g": g, "h": t["controlled_from"]})
    import os
    os.makedirs(B.DIST + "/data", exist_ok=True)
    json.dump({"generated": B.NOW.strftime("%Y-%m-%dT%H:%M:%SZ"), "towers": out}, open(B.DIST + "/data/graph.json", "w", encoding="utf8"), ensure_ascii=False, separators=(",", ":"))

# ------------------------------------------------------------------ connections page
def build_connections(B):
    T, esc, pill, KIND, LABEL = B.T, B.esc, B.pill, B.KIND, B.LABEL
    by = B.BYID
    hubs = [t for t in T if t["kind"] == "rtc"]
    cards = ""
    for h in sorted(hubs, key=lambda x: (x["country"], x["name"])):
        sp = [t for t in T if t["controlled_from"] == h["id"]]
        chips = "".join(f'<a class="chip stc st-{s["status"]}" href="/towers/{s["id"]}/" data-c="{esc(s["country"])}" data-s="{s["status"]}"><i></i>{esc(s["name"])}</a> ' for s in sorted(sp, key=lambda x: x["name"]))
        vs = ", ".join(h["vendors"]) or "vendor not named"
        cards += (f'<div class="card flat hubcard" data-c="{esc(h["country"])}" data-s="{h["status"]}" data-v="|{esc("|".join(h["vendors"]))}|">'
                  f'<div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-bottom:6px">{pill(h["status"])}<span class="tag">{len(sp)} airport{"s" if len(sp)!=1 else ""}</span></div>'
                  f'<h3><a href="/towers/{h["id"]}/" style="color:var(--ink)">{esc(h["name"])}</a></h3>'
                  f'<p class="small mute" style="margin:4px 0 10px">{esc(h["country"])} · {esc(h["ansp"] or "provider n/a")} · {esc(vs)}</p>'
                  f'<div class="chiprow">{chips or "<span class=small>No airports linked in sources.</span>"}</div></div>')
    # lists by vendor / provider / program
    def group(keyf, names):
        g = collections.defaultdict(list)
        for t in T:
            for k in keyf(t): g[k].append(t)
        return g
    ven = group(lambda t: [(B.vendor_of(v) or {"id": B.slug(v), "name": v})["id"] for v in t["vendors"]], None)
    vn = {v["id"]: v["name"] for v in B.EN["vendors"]}
    rows_v = ""
    for k, ts in sorted(ven.items(), key=lambda x: -len(x[1])):
        prov = collections.Counter((B.ansp_of(t["ansp"]) or {"name": t["ansp"] or "n/a"})["name"] for t in ts)
        rows_v += f'<li><b><a href="/vendors/{k}/">{esc(vn.get(k, k))}</a></b> <span class="faint small">{len(ts)} sites</span><div class="small mute">Works with: {esc(", ".join(f"{n} ({c})" for n, c in prov.most_common(8)))}</div></li>'
    pn = {a["id"]: a["name"] for a in B.EN["ansps"]}
    pro = group(lambda t: [(B.ansp_of(t["ansp"]) or {"id": ""})["id"]] if B.ansp_of(t["ansp"]) else [], None)
    rows_p = ""
    for k, ts in sorted(pro.items(), key=lambda x: -len(x[1])):
        vv = collections.Counter(v for t in ts for v in t["vendors"])
        rows_p += f'<li><b><a href="/operators/{k}/">{esc(pn.get(k, k))}</a></b> <span class="faint small">{len(ts)} sites</span><div class="small mute">Vendors: {esc(", ".join(f"{n} ({c})" for n, c in vv.most_common(6)) or "not named")}</div></li>'
    rows_g = ""
    for p in B.EN["programs"]:
        ts = [t for t in T if t["program"] == p["id"]]
        if not ts: continue
        rows_g += f'<li><b><a href="/regulators/#{p["id"]}">{esc(p["name"])}</a></b> <span class="faint small">{len(ts)} sites</span><div class="small mute">{esc(p["blurb"])}</div></li>'
    reg = collections.defaultdict(list)
    for t in T:
        if t.get("regulator"): reg[t["regulator"]].append(t)
    rows_r = "".join(f'<li><b>{esc(k)}</b> <span class="faint small">{len(ts)} sites</span><div class="small mute">{esc(", ".join(x["name"] for x in ts[:6]))}{" and more" if len(ts) > 6 else ""}</div></li>' for k, ts in sorted(reg.items(), key=lambda x: -len(x[1])))
    # approvals: entries classified as approval
    appr = []
    for t in T:
        for d in t["dates"]:
            if classify(d["t"]) == "approval": appr.append((d["d"], t, d))
    for d, tx, u in B.EN["us_timeline"]:
        if classify(tx) == "approval": appr.append((d, None, {"d": d, "t": tx, "u": u}))
    appr.sort(key=lambda x: sortkey(x[0]), reverse=True)
    arows = "".join(f'<li><span class="d">{esc(B.fdate(d))}</span><div>{esc(x["t"])} {("<a class=xs href=" + chr(34) + "/towers/" + t["id"] + "/" + chr(34) + ">" + esc(t["name"]) + "</a>") if t else ""} {("<a class=xs href=" + chr(34) + esc(x.get("u")) + chr(34) + " rel=noopener target=_blank>" + esc(B.host(x["u"])) + "</a>") if x.get("u") else ""}</div></li>' for d, t, x in appr[:12])
    co = "".join(f'<option>{esc(c)}</option>' for c in B.COUNTRIES)
    body = f'''<div class="wrap" style="padding-top:28px"><div class="eyebrow">Connections</div><h1 style="font-size:clamp(30px,4.5vw,46px)">How towers connect</h1>
<p class="mute" style="max-width:68ch;margin-top:10px">Who supplies, who runs, who regulates and which airports are controlled from which centre, drawn from the same sourced records as the map. Pick two kinds of party to see how many sites join them, then tap a name or a line to list the sites. <a href="/timeline/">Approvals and go-lives timeline</a>.</p>
<div class="tools ctools" style="margin-top:18px"><label class="sr" for="ca">Left side</label><select id="ca" aria-label="Left side"><option value="vendor">Vendors</option><option value="provider">Providers</option><option value="regulator">Regulators</option><option value="program">Programs</option></select>
<span class="faint">with</span><label class="sr" for="cb">Right side</label><select id="cb" aria-label="Right side"><option value="provider">Providers</option><option value="vendor">Vendors</option><option value="regulator">Regulators</option><option value="program">Programs</option></select>
<label class="sr" for="cc">Country</label><select id="cc" aria-label="Country"><option value="">All countries</option>{co}</select></div>
<div class="chiprow" id="cstat" style="margin-top:10px"></div>
<div class="chiprow" style="margin-top:8px"><button class="chip" id="ckind" type="button" aria-pressed="false">Remote towers and centres only</button><span class="small mute" id="ccount"></span></div>
<div id="cg" class="cg" role="img" aria-label="Lines between the two kinds of party you picked, thicker for more sites"></div>
<div id="cdetail" class="card" style="margin-top:14px"><p class="small mute" style="margin:0">Tap a name or a line above to list the sites it covers.</p></div>
<h2 style="margin:40px 0 6px">Remote tower centres and the airports they control</h2><p class="small mute" style="margin:0 0 14px">Each centre is controlled by one provider; every airport chip opens that airport. <span id="hubcount"></span></p>
<div class="grid g2" id="hubs">{cards}</div>
<div class="grid g2" style="margin-top:36px;align-items:start"><section><h2 style="font-size:22px;margin-bottom:10px">By vendor</h2><div class="card"><ul class="plain">{rows_v}</ul></div></section><section><h2 style="font-size:22px;margin-bottom:10px">By provider</h2><div class="card"><ul class="plain">{rows_p}</ul></div></section></div>
<div class="grid g2" style="margin-top:20px;align-items:start"><section><h2 style="font-size:22px;margin-bottom:10px">Programs</h2><div class="card"><ul class="plain">{rows_g}</ul></div></section><section><h2 style="font-size:22px;margin-bottom:10px">Regulators named in sources</h2><div class="card"><ul class="plain">{rows_r}</ul></div></section></div>
<h2 style="margin:36px 0 10px">Latest approvals</h2><div class="card"><ul class="timeline" style="margin:0">{arows}</ul><p class="small" style="margin:6px 0 0"><a href="/timeline/?type=approval">All approvals</a></p></div>
<p class="xs faint" style="margin-top:20px">An approval on this site is only what a source says was approved, by whom and when. A design approval is not an operational authorization.</p></div>'''
    B.page("/connections/", "How remote and digital towers connect | Digital Towers", "A filterable graph and linked lists of which vendors, providers, regulators and programs connect remote and digital tower sites, and which centres control which airports.", body,
           scripts='<script src="/assets/conn.js?v=' + B.VER + '"></script>')

# ------------------------------------------------------------------ timeline
def build_timeline(B):
    T, esc = B.T, B.esc
    today = B.NOW.strftime("%Y-%m-%d")
    rows = []
    for t in T:
        for d in t["dates"]:
            rows.append((d["d"], d["t"], t, d.get("u") or ""))
    for d, tx, u in B.EN["us_timeline"]:
        rows.append((d, tx, None, u))
    # drop exact duplicates
    seen = set(); uniq = []
    for r in rows:
        k = (r[0], r[1])
        if k in seen: continue
        seen.add(k); uniq.append(r)
    uniq.sort(key=lambda r: sortkey(r[0]), reverse=True)
    items = ""; years = collections.OrderedDict()
    for d, tx, t, u in uniq:
        y = str(d)[:4]
        typ = classify(tx)
        future = sortkey(d) > today + "-00-00"[:0] and sortkey(d) > today
        if future: typ_attr = "scheduled"
        else: typ_attr = typ
        src = (f'<a class="xs" href="{esc(u)}" rel="noopener" target="_blank">{esc(B.host(u))}</a>' if u else (f'<a class="xs" href="/towers/{t["id"]}/#sources">sources on tower page</a>' if t else ""))
        who = f'<a href="/towers/{t["id"]}/">{esc(t["name"])}</a>' if t else '<span class="faint">United States program</span>'
        lab = {"approval": "Approval", "golive": "Go-live", "contract": "Contract or announcement", "ended": "Ended or delayed", "milestone": "Milestone", "scheduled": "Scheduled"}[typ_attr]
        li = (f'<li class="tl" data-type="{typ_attr}" data-c="{esc(t["country"] if t else "United States")}" data-id="{esc(t["id"] if t else "")}"><span class="d">{esc(B.fdate(d))}</span>'
              f'<div><span class="tag tl-{typ_attr}">{lab}</span> {esc(tx)}<div class="xs mute" style="margin-top:3px">{who} · {src}</div></div></li>')
        years.setdefault(y, []).append(li)
    for y, lis in years.items():
        items += f'<h2 class="yr" data-y="{y}" style="margin:28px 0 12px;font-size:22px">{y}</h2><ul class="timeline tlist" style="margin:0">{"".join(lis)}</ul>'
    cs = sorted({t["country"] for t in T} | {"United States"})
    cop = "".join(f'<option>{esc(c)}</option>' for c in cs)
    body = f'''<div class="wrap" style="padding-top:28px"><div class="eyebrow">Timeline</div><h1 style="font-size:clamp(30px,4.5vw,46px)">Approvals and go-lives</h1>
<p class="mute" style="max-width:66ch;margin-top:10px">Every dated event in the records, newest first, each with its source. Future dates are plans, shown as scheduled. The type label is a plain-language guess from the wording of the source, so read the sentence.</p>
<div class="chiprow" id="tlchips" style="margin-top:16px"><button class="chip" type="button" data-type="approval" aria-pressed="false">Approvals</button><button class="chip" type="button" data-type="golive" aria-pressed="false">Go-lives</button><button class="chip" type="button" data-type="contract" aria-pressed="false">Contracts</button><button class="chip" type="button" data-type="ended" aria-pressed="false">Ended or delayed</button><button class="chip" type="button" data-type="scheduled" aria-pressed="false">Scheduled</button></div>
<div class="tools" style="margin-top:10px"><label class="sr" for="tlc">Country</label><select id="tlc" aria-label="Country"><option value="">All countries</option>{cop}</select><span class="small mute" id="tlcount"></span></div>
{items}</div>'''
    B.page("/timeline/", "Approvals and go-lives timeline | Digital Towers", f"{len(uniq)} dated events for remote and digital towers worldwide: approvals, go-lives, contracts, delays and scheduled dates, each linked to its source.", body,
           scripts='<script src="/assets/conn.js?v=' + B.VER + '"></script>')

# ------------------------------------------------------------------ coverage
def build_coverage(B):
    esc = B.esc
    E = B.EN
    cov = ""
    for c in E.get("coverage", []):
        ln = " · ".join(f'<a href="{esc(u)}" rel="noopener" target="_blank">{esc(l)}</a>' for l, u in c["links"])
        cov += f'<div class="card flat"><div class="tag">{esc(c["result"])}</div><h3 style="margin:10px 0 6px">{esc(c["country"])}</h3><p class="small mute" style="margin:0 0 8px">{esc(c["text"])}</p><p class="xs" style="margin:0">{ln}</p></div>'
    rl = "".join(f'<tr><td><b>{esc(a)}</b></td><td>{esc(b)}</td><td>{esc(c)}</td><td><a href="{esc(u)}" rel="noopener" target="_blank">{esc(B.host(u))}</a></td></tr>' for a, b, c, u in E.get("reflists", []))
    unv = [t for t in B.T if t["status"] == "unverified"]
    uv = "".join(f'<li><a href="/towers/{t["id"]}/">{esc(t["name"])}</a> <span class="faint small">{esc(t["country"])}</span><div class="small mute">{esc(t["note"])}</div></li>' for t in unv)
    body = f'''<div class="wrap" style="padding-top:28px"><div class="eyebrow">Coverage</div><h1 style="font-size:clamp(30px,4.5vw,46px)">What is covered, and what is not</h1>
<p class="mute" style="max-width:68ch;margin-top:10px">This map does not claim to be complete. Below are the places checked where nothing verified was found or the finding is not a remote tower, the vendor and provider lists reviewed on 11 October 2026, and the sites still marked unverified.</p>
<h2 style="margin:30px 0 12px">Places checked</h2><div class="grid g2">{cov}</div>
<h2 style="margin:36px 0 12px">Vendor and provider lists reviewed</h2><div class="card" style="overflow-x:auto"><table class="tbl"><thead><tr><th>Who</th><th>List</th><th>What it gave</th><th>Source</th></tr></thead><tbody>{rl}</tbody></table></div>
<h2 style="margin:36px 0 12px">Still unverified ({len(unv)})</h2><div class="card"><ul class="plain">{uv or "<li>None.</li>"}</ul></div>
<p class="small mute" style="margin-top:20px">Know of a site we missed or got wrong? Use "Suggest a correction" on any tower page, with a public source link. <a href="/about/">Method</a>.</p></div>'''
    B.page("/coverage/", "Coverage and gaps | Digital Towers", "Which countries and vendor lists were checked for remote and digital towers, what was found, what was not, and which entries are still unverified.", body)
