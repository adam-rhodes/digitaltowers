# -*- coding: utf-8 -*-
"""Digital Towers "Future state" section (fut1011). Hypothetical, illustrative scenarios built only from public data.
Called from dt_build.main() as dt_future.build_all(<dt_build module>). Data: data/future/*.json (built off-droplet by build_future)."""
import json, os, shutil, collections, html

DISC = "Hypothetical. Illustrative. Not a recommendation of any authority."
TIERS = {
 "1": ("Tier 1", "Full remote tower service", "#ffb347", "Air traffic control from a remote centre for extended hours or around the clock."),
 "2": ("Tier 2", "Part-time remote tower", "#4fd1c5", "Remote air traffic control in busy periods, advisory service the rest of the day."),
 "3": ("Tier 3", "Remote advisory (AFIS-like)", "#f472b6", "Remote flight information and traffic advisories. Not air traffic control."),
 "4": ("Tier 4", "Surface awareness only", "#9aa2b1", "Cameras and surveillance feeds that give an operator or pilots a picture. No separation service."),
 "X": ("Hub", "Large hub: augment or keep as is", "#556070", "Too large for the simple remote model. Digital augmentation or contingency use only."),
}
CLS = {"R": "Remote or digital tower already listed on this site", "T": "Staffed tower today", "S": "No tower, scheduled passenger service", "G": "No tower, traffic above threshold", "P": "No tower, infrastructure proxy (no traffic figure)", "I": "No tower, isolated airfield"}

def n(x):
    try: return f"{int(round(x)):,}"
    except Exception: return "n/a"
def short(x):
    x = float(x or 0)
    if x >= 1e9: return f"{x/1e9:.1f} billion"
    if x >= 1e6: return f"{x/1e6:.1f} million"
    if x >= 1e3: return f"{x/1e3:.0f} thousand"
    return f"{int(x)}"

def build_all(B):
    base = B.BASE
    src = base + "/data/future"
    if not os.path.isdir(src): return
    SUMM = json.load(open(src + "/summary.json", encoding="utf8"))
    TH = SUMM["thresholds"]; CS = SUMM["countries"]; SCOPE = SUMM["scope"]
    os.makedirs(B.DIST + "/data/future", exist_ok=True)
    for f in os.listdir(src):
        if f.endswith(".json") or f.endswith(".csv"): shutil.copy(src + "/" + f, B.DIST + "/data/future/" + f)
    shutil.copy(base + "/dt_future.css", B.DIST + "/assets/future.css")
    shutil.copy(base + "/dt_future.js", B.DIST + "/assets/future.js")
    esc = B.esc
    names = {t["cc"]: t["country"] for t in B.T}; names.setdefault("IN", "India")
    for cc in SCOPE: names.setdefault(cc, CS[cc]["name"])
    slugs = {cc: B.slug(names[cc]) for cc in SCOPE}
    order = sorted(SCOPE, key=lambda c: names[c])
    HEAD = f'<link rel="stylesheet" href="/assets/future.css?v={B.VER}">'
    def banner(): return f'<div class="note fut-banner"><b>{DISC}</b> Every number here comes from a stated rule applied to public data. It describes a what-if, not a plan, forecast or advice to any country, airport or authority.</div>'
    def subnav(cur):
        items = [("/future/", "Overview"), ("/future/map/", "World view"), ("/future/countries/", "Countries"), ("/future/market/", "Market and use cases"), ("/future/method/", "Method")]
        return '<div class="subnav">' + "".join(f'<a class="chip" href="{u}"' + (' aria-pressed="true"' if u == cur else "") + f'>{t}</a>' for u, t in items) + '</div>'
    # ------------------------------------------------ world totals
    def tot(key_fn): return sum(key_fn(CS[c]) for c in CS)
    W = dict(
        countries=len(CS), assessed=tot(lambda s: s["assessed"]),
        gap=tot(lambda s: s["gap_n"]), tow=tot(lambda s: s["tower_elig"]), ctr=tot(lambda s: s["centers"]),
        t4=tot(lambda s: s["tier4"]),
        g1=tot(lambda s: s["tier_gap"]["1"]), g2=tot(lambda s: s["tier_gap"]["2"]), g3=tot(lambda s: s["tier_gap"]["3"]),
        x=tot(lambda s: s["tier_tower"]["X"]), tw=tot(lambda s: s["cls"]["T"]), remote=tot(lambda s: s["cls"]["R"]),
        gapb=tot(lambda s: s["gap_traffic_basis"]),
        scope_assessed=sum(CS[c]["assessed"] for c in SCOPE), scope_gap=sum(CS[c]["gap_n"] for c in SCOPE),
    )
    # ------------------------------------------------ overview
    def tiles(items):
        return '<div class="stats">' + "".join(f'<div class="stat"><b>{v}</b><span>{l}</span></div>' for v, l in items) + '</div>'
    cards = ""
    for cc in order:
        s = CS[cc]
        cards += (f'<a class="card flat" href="/future/countries/{slugs[cc]}/" style="color:var(--ink)"><h3>{esc(names[cc])}</h3>'
                  f'<p class="mute small" style="margin:6px 0 10px">{n(s["assessed"])} airports assessed</p>'
                  f'<p class="small" style="margin:0"><b>{n(s["gap_n"])}</b> without a tower meet a threshold · <b>{n(s["tower_elig"])}</b> towered candidates · <b>{n(s["centers"])}</b> hypothetical centres</p></a>')
    body = f'''<div class="wrap" style="padding-top:28px"><div class="eyebrow">Future state</div><h1 style="font-size:clamp(30px,4.5vw,50px);max-width:22ch">What digital towers could enable, country by country</h1>
<p class="lede mute" style="max-width:64ch;margin-top:14px;font-size:17px">Remote and digital towers do more than copy a tower window. They let one team serve many airports, extend service hours, and give airports that have no air traffic service today a way to get one. This section applies simple, published rules to public airport data to show where that could matter, how service could be tiered, and where shared centres could sit.</p>
{banner()}
{subnav("/future/")}
{tiles([(n(W["assessed"]), "airports assessed worldwide"), (n(W["gap"]), "without a tower that meet a tier 1 to 3 rule"), (n(W["tow"]), "towered airports that fit tier 1 to 3"), (n(W["ctr"]), "hypothetical centres"), (str(len(SCOPE)), "country pages")])}
<div class="cta" style="display:flex;gap:10px;flex-wrap:wrap;margin-top:22px"><a class="btn primary" href="/future/map/">Open the world view</a><a class="btn" href="/future/countries/">Browse countries</a><a class="btn" href="/future/market/">Market and use cases</a><a class="btn" href="/future/method/">Read the method</a></div>
<section class="section"><div class="head"><h2>How it works in four steps</h2></div><div class="grid g4">
<div class="card flat"><div class="tag">1</div><h3 style="margin:10px 0 6px">Classify</h3><p class="small mute" style="margin:0">Every public airport with a runway of {TH["assess_rwy_m"]} m or more, or scheduled service, or a tower, is put in one class: already remote, towered, scheduled without a tower, busy without a tower, infrastructure proxy, or isolated.</p></div>
<div class="card flat"><div class="tag">2</div><h3 style="margin:10px 0 6px">Tier</h3><p class="small mute" style="margin:0">A traffic rule suggests one of four service tiers, from full remote tower service down to surface awareness only. Large hubs are left alone.</p></div>
<div class="card flat"><div class="tag">3</div><h3 style="margin:10px 0 6px">Cluster</h3><p class="small mute" style="margin:0">Airports are grouped around existing air traffic facilities, within {TH["center_radius_km"]} km and about one time zone, up to a stated workload per centre.</p></div>
<div class="card flat"><div class="tag">4</div><h3 style="margin:10px 0 6px">Measure the gap</h3><p class="small mute" style="margin:0">Traffic and people near airports that have no tower today, from national statistics and GeoNames city populations. Missing data is stated, not filled in.</p></div></div></section>
<section class="section"><div class="head"><h2>Countries</h2><a href="/future/countries/">All countries</a></div><div class="grid g3">{cards}</div></section>
<section class="section"><div class="card"><h3>Read this before using any number</h3><ul class="plain small mute" style="margin-top:10px"><li>Tiers are suggestions from a rule, not assessments of any airport. Real decisions need a safety case, a regulator, and local knowledge this section does not have.</li><li>Where a country has no public airport traffic table loaded here, tiers rest on runway length, airport size class and the scheduled-service flag. Each country page says which.</li><li>"Towered" means the airport has a tower radio frequency in OurAirports or a tower flag in the FAA forecast. That is not proof of staffed hours.</li><li>The people figures count only cities of 15,000 or more (GeoNames), so rural populations are missed.</li></ul><p class="small" style="margin:12px 0 0"><a href="/future/method/">Full method, every threshold and source</a></p></div></section></div>'''
    B.page("/future/", "Future state: what digital towers could enable | Digital Towers", "A hypothetical, sourced view of which airports have no tower today, what remote service tier could suit them, and where shared remote tower centres could sit, in " + str(len(SCOPE)) + " countries.", body, HEAD)
    # ------------------------------------------------ method
    th = TH
    def row(a, b, c): return f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>"
    thr = "".join([
        row("Airport is assessed", f"Type small, medium or large; not closed; not military by name; and scheduled service, or a tower, or a runway of {th['assess_rwy_m']} m or more. United States: only airports in the FAA forecast, or with scheduled service or a tower.", "OurAirports; FAA Terminal Area Forecast"),
        row("Tier 1 (staffed tower today)", f"{n(th['t1_ops_tower'])} or more movements a year, or {n(th['t1_pax_tower'])} or more passengers", "National traffic tables"),
        row("Tier 2 (staffed tower today)", f"{n(th['t2_ops_tower'])} or more movements, or {n(th['t2_pax_tower'])} or more passengers", ""),
        row("Tier 3 (staffed tower today)", "Traffic known and below the tier 2 level", ""),
        row("Hub, left alone", f"{n(th['big_ops'])} or more movements, or {n(th['big_pax'])} or more passengers", ""),
        row("Tier 1 (no tower, scheduled service)", f"{n(th['t1_pax_sched'])} or more passengers, or {n(th['t1_ops_nontower'])} or more movements", ""),
        row("Tier 2 (no tower, scheduled service)", f"{n(th['t2_pax_sched'])} or more passengers, or {n(th['t2_ops_nontower'])} or more movements", ""),
        row("Tier 3 (no tower, scheduled service)", "Below the tier 2 level", ""),
        row("Tier 1 / Tier 2 (no tower, no scheduled service)", f"{n(th['t1_ops_nontower'])} or more movements is tier 1; {n(th['t2_ops_nontower'])} or more movements is tier 2", "Needs a movements figure (United States forecast, UK, Australia, part of Canada)"),
        row("Tier 3 by infrastructure proxy", f"No tower, no traffic figure, paved runway of {n(th['proxy_rwy_m'])} m or more, and {n(th['proxy_pop25'])} or more people within 25 km", "OurAirports; GeoNames"),
        row("Tier 4, isolated", f"No tower, runway of {th['iso_rwy_m']} m or more, and no other reference airport within {th['iso_km']} km (reference = scheduled service, a tower, or a paved runway of {n(th['iso_ref_rwy_m'])} m or more)", "OurAirports"),
        row("Unknown traffic, staffed tower", "Large airport class is a hub; medium is tier 1; small is tier 2", "Size class from OurAirports"),
        row("Unknown traffic, scheduled service, no tower", "Medium or large class is tier 2; small is tier 3", ""),
        row("Hypothetical centre", f"Up to {th['center_cap_units']:g} workload units (tier 1 = {th['unit_t1']:g}, tier 2 = {th['unit_t2']:g}, tier 3 = {th['unit_t3']:g}); airports within {th['center_radius_km']} km and {th['center_dlon']} degrees of longitude of the centre; same country", "Greedy placement, existing facilities first"),
        row("People gap", f"People in cities of 15,000 or more within {th['gap_pop_km']} km of an airport, each city counted once", "GeoNames cities15000"),
    ])
    srcrows = ""
    for cc in order:
        ss = SUMM["countries"][cc]
        j = json.load(open(src + f"/c_{cc.lower()}.json", encoding="utf8"))
        links = "<br>".join(f'<a href="{esc(x["url"])}" rel="noopener" target="_blank">{esc(x["label"])}</a>' for x in j["sources"]) or "None loaded. Tiers use runway, size class and scheduled-service flag only."
        srcrows += f'<tr><td><a href="/future/countries/{slugs[cc]}/">{esc(names[cc])}</a></td><td class="small">{links}</td></tr>'
    body = f'''<div class="wrap" style="padding-top:28px"><div class="crumbs"><a href="/future/">Future state</a> / Method</div><h1 style="margin-top:8px;font-size:clamp(30px,4.5vw,46px)">Method</h1>
<p class="mute" style="max-width:68ch;margin-top:10px">Everything on the Future state pages follows from the rules on this page and the public data named here. Nothing is estimated by hand, and no document or data from any government or company that is not public was used.</p>{banner()}{subnav("/future/method/")}
<div class="prose" style="max-width:76ch;margin-top:8px"><h2>1. Airport classes</h2>
<p>Each assessed airport gets the first class that fits.</p>
<ul><li><b>Remote or digital, already listed (R).</b> Matches an operational, trial or planned site in the <a href="/towers/">tower dataset</a> by ICAO code.</li><li><b>Staffed tower today (T).</b> Has a tower frequency in OurAirports, or the tower flag in the FAA forecast for US airports. This is a proxy: it does not prove the tower is staffed all day, and OurAirports frequency lists are incomplete in some countries.</li><li><b>No tower, scheduled passenger service (S).</b> The OurAirports scheduled-service flag.</li><li><b>No tower, traffic above threshold (G).</b> A movements or passenger figure at or above the tier 2 level.</li><li><b>No tower, infrastructure proxy (P).</b> No traffic figure exists in the loaded tables, but the runway and nearby population suggest a busy airfield.</li><li><b>No tower, isolated (I).</b> Far from every other reference airport. This is a distance proxy for remote, medical or island access. No road, medical or ferry data was used.</li><li><b>Below threshold (N).</b> Assessed but not a candidate. Counted, not mapped.</li></ul>
<h2>2. Suggested service tiers</h2>
<div class="grid g2" style="margin:14px 0">{"".join(f'<div class="card flat tiercard" style="--c:{TIERS[k][2]}"><div class="tag" style="color:var(--c)">{TIERS[k][0]}</div><h3 style="margin:8px 0 6px">{TIERS[k][1]}</h3><p class="small mute" style="margin:0">{TIERS[k][3]}</p></div>' for k in "1234X")}</div>
<h2>3. Every threshold</h2></div>
<div class="card" style="overflow-x:auto;margin-top:6px"><table class="tbl"><thead><tr><th>Rule</th><th>Value</th><th>Input</th></tr></thead><tbody>{thr}</tbody></table></div>
<div class="prose" style="max-width:76ch"><h2>4. Where hypothetical centres go</h2>
<p>Within each country, the airports in tiers 1 to 3 (not hubs, not already remote) are grouped. Candidate sites are airports with a staffed tower today and a medium or large size class, plus operating, trial or planned remote tower centres from this site's dataset. A greedy search picks the site that can take the most workload within {th['center_radius_km']} km, prefers existing remote tower centres and then existing staffed facilities, and repeats until every airport is placed. If no existing site is in range, the airport itself becomes a "new site", which is penalised so it is used last. Centres never cross a national border. Workload units are an illustration of shared capacity, not a staffing analysis.</p>
<h2>5. Data inputs</h2>
<ul><li><b>Airports, runways, frequencies:</b> <a href="https://ourairports.com/data/" rel="noopener">OurAirports open data</a> (public domain), pulled 11 October 2026.</li><li><b>Populations:</b> GeoNames cities of 15,000 or more (CC BY 4.0); national population from the World Bank (SP.POP.TOTL, 2024).</li><li><b>Existing remote and digital towers:</b> the <a href="/data/">dataset on this site</a>, every row with its own sources.</li><li><b>Traffic:</b> per country, below. Where a table is missing, tiers fall back on infrastructure, and the country page says so.</li></ul>
<h2>6. What this is not</h2>
<ul><li>It is not a recommendation to any authority, airport or air navigation service provider.</li><li>It is not a business case. There are no costs, benefits or demand forecasts here.</li><li>It does not know local terrain, weather, airspace, labour agreements, safety history or politics.</li><li>Tiers can be wrong for any single airport. Use the airport list as a starting question, not an answer.</li></ul>
<h2>7. Traffic sources by country</h2></div>
<div class="card" style="overflow-x:auto"><table class="tbl"><thead><tr><th>Country</th><th>Public traffic data used</th></tr></thead><tbody>{srcrows}</tbody></table></div>
<p class="small mute" style="margin-top:14px">Data downloads: <a href="/data/future/summary.json">summary.json</a> · <a href="/data/future/airports.csv">airports.csv</a> (every candidate airport in the country-page countries, with class, tier and reason) · <a href="/data/future/world_points.json">world_points.json</a> · <a href="/data/future/world_centers.json">world_centers.json</a>. Free to reuse with attribution to digitaltowers.org.</p></div>'''
    B.page("/future/method/", "Method: classes, tiers, thresholds and sources | Digital Towers", "How airports are classified, how a service tier is suggested, how hypothetical remote tower centres are placed, with every threshold and input source. Hypothetical and illustrative.", body, HEAD)
    # ------------------------------------------------ countries index
    rows = ""
    for cc in order:
        s = CS[cc]
        rows += f'<tr><td><a class="rowlink" href="/future/countries/{slugs[cc]}/">{esc(names[cc])}</a></td><td>{n(s["assessed"])}</td><td>{n(s["gap_n"])}</td><td>{n(s["tower_elig"])}</td><td>{n(s["tier4"])}</td><td>{n(s["centers"])}</td><td>{short(s["people"]["gap"])}</td></tr>'
    body = f'''<div class="wrap" style="padding-top:28px"><div class="crumbs"><a href="/future/">Future state</a> / Countries</div><h1 style="margin-top:8px;font-size:clamp(30px,4.5vw,46px)">Countries</h1>{banner()}{subnav("/future/countries/")}
<div class="card" style="overflow-x:auto;margin-top:10px"><table class="tbl"><thead><tr><th>Country</th><th>Assessed</th><th>No tower, tier 1 to 3</th><th>Towered, tier 1 to 3</th><th>Tier 4</th><th>Centres</th><th>People near gap</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="small mute" style="margin-top:12px">Countries are those already on this site plus India. "People near gap" counts people in cities of 15,000 or more within {TH["gap_pop_km"]} km of an airport without a tower that meets a tier 1 to 3 rule.</p></div>'''
    B.page("/future/countries/", "Future state by country | Digital Towers", "Hypothetical remote tower tiers, candidate airports and centres for " + str(len(SCOPE)) + " countries.", body, HEAD)
    # ------------------------------------------------ country pages
    GUIDE = [("EASA ED Decision 2023/005/R, guidance material on remote aerodrome air traffic services", "https://www.easa.europa.eu/en/document-library/agency-decisions/ed-decision-2023005r"),
             ("UK CAA: remote aerodrome air traffic services (CAP 670 and approval policy)", "https://www.caa.co.uk/commercial-industry/airspace/communication-navigation-and-surveillance/remote-towers/"),
             ("EUROCAE ED-240A, minimum performance standards for remote tower optical systems", "https://www.eurocae.net/product/ed-240a-minimum-aviation-system-performance-standards-masps-for-remote-tower-optical-systems"),
             ("FAA Digital Tower Systems page", "https://www.faa.gov/airports/planning_capacity/non_federal/digital_tower_systems"),
             ("FAA AIP Program Guidance Letter 26-06 (design approval is not operational approval)", "https://www.faa.gov/airports/aip/guidance_letters/aip_pgl_26_06"),
             ("ICAO Doc 4444, PANS-ATM, the procedures that remote services must still meet", "https://www.icao.int/publications/pages/publication.aspx?docnum=4444")]
    def responsible(cc, nm, regs):
        reg = (" The regulator named in this site's records for " + esc(nm) + ": " + esc(", ".join(regs)) + ".") if regs else " This site's records name no regulator for " + esc(nm) + " yet; the national supervisory authority would decide."
        items = [
         ("Safety case and regulator approval", "Each service needs its own safety case and approval before it carries traffic. A design approval for equipment is a different step from permission to run a service." + reg),
         ("Controller workforce and training", "Remote work changes the job: new displays, new failure modes, and new competence checks. A plan would cover who moves, who trains, how existing controllers choose, and what happens to current staff and their conditions."),
         ("Communications and surveillance", "Radio, video and surveillance links must meet the latency and quality the safety case assumes. Tier 1 and 2 airports need reliable cameras, redundant links and a surveillance picture for traffic that radar or ADS-B cannot see from the ground."),
         ("Contingency and redundancy", "Every centre needs a fallback: a second path for data, a backup position, and a rule for what the airport does when a link fails (hold, divert, revert to advisory). Centres that serve many airports need a plan for losing all of them at once."),
         ("Cybersecurity", "A centre is a single high-value target. It needs the same protections as other air traffic systems: segmented networks, supply-chain checks, logging, and tested recovery."),
         ("Community and labour engagement", "Airports, airlines, pilots, unions, local governments and neighbours should be in the process before decisions, not after. Jobs can move away from small airports, and that is a real cost to a community.")]
        lis = "".join(f'<div class="card flat"><h3>{t}</h3><p class="small mute" style="margin:8px 0 0">{x}</p></div>' for t, x in items)
        gl = "".join(f'<li><a href="{u}" rel="noopener" target="_blank">{esc(t)}</a></li>' for t, u in GUIDE)
        return f'<section class="section"><div class="head"><h2>Responsible implementation</h2></div><p class="small mute" style="max-width:70ch">A tier on this page is a starting question. These are the topics any real plan would need to answer. Public guidance:</p><ul class="small" style="margin:8px 0 16px;padding-left:18px;display:grid;gap:6px">{gl}</ul><div class="grid g2">{lis}</div></section>'
    regs_by = collections.defaultdict(list)
    for t in B.T:
        if t.get("regulator") and t["regulator"] not in regs_by[t["cc"]]: regs_by[t["cc"]].append(t["regulator"])
    for cc in order:
        s = CS[cc]; j = json.load(open(src + f"/c_{cc.lower()}.json", encoding="utf8")); nm = names[cc]
        g = s["tier_gap"]; tt = s["tier_tower"]; pe = s["people"]
        has_today = any(t["cc"] == cc for t in B.T)
        cov = "no national traffic table loaded" if not j["sources"] else f'{len(j["sources"])} public traffic source{"s" if len(j["sources"]) != 1 else ""} loaded'
        basis = s["gap_traffic_basis"]
        dq = (f'<b>Data quality.</b> {basis} of the {s["gap_n"]} airports without a tower that meet a rule have a traffic figure; the rest are placed by runway, size class and scheduled-service flag only.' if s["gap_n"] else "No airport without a tower met a tier 1 to 3 rule.")
        if not j["sources"]: dq += " No public national airport traffic table was loaded for this country, so every tier here is an infrastructure proxy."
        else: dq += " " + " ".join(esc(x["note"]) for x in j["sources"] if x.get("note"))
        what = []
        if s["gap_n"]: what.append(f'<li><b>Service where there is none.</b> {n(s["gap_n"])} airports have no tower but meet a traffic or infrastructure rule. Remote service could give them separation or advisory service they cannot justify as a conventional tower.' + (f' About {short(pe["gap_notower"])} people live within {TH["gap_pop_km"]} km of one of them and of no towered airport.' if pe["gap_notower"] else "") + '</li>')
        if s["tower_elig"]: what.append(f'<li><b>Fewer, shared positions.</b> {n(s["tower_elig"])} towered airports fit tiers 1 to 3. Serving some of them from {n(s["centers"])} shared centres could change how towers are staffed, equipped and replaced when they age.</li>')
        if s["centers"]: what.append(f'<li><b>Different working pattern.</b> A centre of about {s["centers_avg"]:g} airports lets part-time airports share a controller across the day, and lets busy periods at different airports fall on different positions.</li>')
        if s["tier4"]: what.append(f'<li><b>Awareness for isolated fields.</b> {n(s["tier4"])} isolated airfields could get surface awareness (cameras and surveillance) without any air traffic service.</li>')
        if s["cls"]["R"]: what.append(f'<li><b>Already moving.</b> {n(s["cls"]["R"])} airports here are listed on this site as remote or digital (operational, trial or planned). <a href="/countries/{slugs[cc]}/">See them</a>.</li>')
        if not what: what.append("<li>Little to add under these rules.</li>")
        tierrows = "".join(f'<tr><td><span class="dot" style="background:{TIERS[k][2]}"></span>{TIERS[k][0]}: {TIERS[k][1]}</td><td>{n(g.get(k, 0)) if k in g else "n/a"}</td><td>{n(tt.get(k, 0)) if k in tt else "n/a"}</td></tr>' for k in "123") + f'<tr><td><span class="dot" style="background:{TIERS["4"][2]}"></span>Tier 4: Surface awareness only</td><td>{n(s["tier4"])}</td><td>n/a</td></tr><tr><td><span class="dot" style="background:{TIERS["X"][2]}"></span>Large hub, left alone</td><td>n/a</td><td>{n(tt["X"])}</td></tr>'
        ctrrows = "".join(f'<tr><td>{esc(c["site"])}<div class="xs faint">{esc(c["kind"])}</div></td><td>{c["n"]}</td><td>{c["t1"]} / {c["t2"]} / {c["t3"]}</td><td>{c["maxd"]} km</td></tr>' for c in j["centers"][:60])
        more = f'<p class="xs faint" style="margin:8px 0 0">First 60 of {len(j["centers"])} centres shown. All are in the data file.</p>' if len(j["centers"]) > 60 else ""
        top = [x for x in j["airports"] if x["cls"] in ("S", "G", "P") and x["tier"] in ("1", "2", "3")][:15]
        static = "".join(f'<tr><td>{esc(x["n"])}<div class="xs faint">{esc(x["id"])} · {esc(x["m"])}</div></td><td>{TIERS[x["tier"]][0]}</td><td>{esc(CLS[x["cls"]])}</td><td>{n(x["pax"]) if x["pax"] is not None else "n/a"}</td><td>{n(x["ops"]) if x["ops"] is not None else "n/a"}</td></tr>' for x in top)
        body = f'''<div class="wrap" style="padding-top:28px"><div class="crumbs"><a href="/future/">Future state</a> / <a href="/future/countries/">Countries</a></div><h1 style="margin-top:8px;font-size:clamp(30px,4.5vw,46px)">{esc(nm)}: a hypothetical future state</h1>
<p class="mute" style="max-width:68ch;margin-top:10px">{n(s["assessed"])} airports assessed. {n(s["gap_n"])} have no tower and meet a tier 1 to 3 rule ({n(g["1"])} / {n(g["2"])} / {n(g["3"])}). {n(s["tower_elig"])} towered airports fit tiers 1 to 3. A hypothetical set of {n(s["centers"])} centres covers them. {cov.capitalize()}.</p>{banner()}
{tiles([(n(s["assessed"]), "airports assessed"), (n(s["gap_n"]), "no tower, tier 1 to 3"), (n(s["tower_elig"]), "towered, tier 1 to 3"), (n(s["tier4"]), "isolated, tier 4"), (n(s["centers"]), "hypothetical centres"), (short(pe["gap"]), "people near a gap airport")])}
<div class="fmapwrap"><div id="fmap" class="fmap" aria-label="Map of candidate airports and hypothetical centres in {esc(nm)}"></div><div class="legend2" id="flegend"></div></div>
<p class="xs faint" style="margin:8px 0 0">Orange, teal, pink and grey dots are suggested tiers. Hollow rings are towered airports that fit a tier. White-ringed orange dots are hypothetical centres. Green outlined dots are remote or digital towers already listed on this site. Basemap: OpenStreetMap data via Protomaps.</p>
<section class="section"><div class="head"><h2>What it could enable</h2></div><ul class="plain small" style="max-width:74ch;gap:10px">{"".join(what)}</ul></section>
<section class="section"><div class="head"><h2>The gap in numbers</h2></div><div class="grid g2" style="align-items:start"><div class="card" style="overflow-x:auto"><table class="tbl"><thead><tr><th>Tier</th><th>No tower today</th><th>Towered today</th></tr></thead><tbody>{tierrows}</tbody></table></div>
<div class="card"><dl class="kv"><dt>Traffic on gap airports</dt><dd>{short(s["gap_pax"])} passengers ({s["gap_pax_n"]} airports with a figure){(", " + short(s["gap_ops"]) + " movements (" + str(s["gap_ops_n"]) + " airports)") if s["gap_ops"] else ""}</dd><dt>Population</dt><dd>{short(s["pop"]) if s["pop"] else "n/a"} (World Bank 2024)</dd><dt>People in cities of 15,000+</dt><dd>{short(pe["cities_pop"])}</dd><dt>Within {TH["gap_pop_km"]} km of a gap airport</dt><dd>{short(pe["gap"])}</dd><dt>... and of no towered airport</dt><dd>{short(pe["gap_notower"])}</dd><dt>Near only an isolated airfield</dt><dd>{short(pe.get("iso", 0))}</dd><dt>Airports with air-ground service already</dt><dd>{n(s["afis_gap"])} of the gap airports have an AFIS-type frequency listed</dd></dl></div></div>
<div class="note" style="margin-top:14px">{dq}</div></section>
<section class="section"><div class="head"><h2>Candidate airports</h2><span class="small mute" id="fcount"></span></div>
<div class="tools"><input id="fq" type="search" placeholder="Search name or code" aria-label="Search airports"><select id="ftier" aria-label="Tier"><option value="">Any tier</option><option value="1">Tier 1</option><option value="2">Tier 2</option><option value="3">Tier 3</option><option value="4">Tier 4</option><option value="X">Hub</option></select><select id="fcls" aria-label="Class"><option value="">Any class</option><option value="gap">No tower, tier 1 to 3</option><option value="T">Staffed tower today</option><option value="R">Already remote or digital</option><option value="I">Isolated</option></select></div>
<div class="card" style="overflow-x:auto;margin-top:10px"><table class="tbl" id="ftable"><thead><tr><th>Airport</th><th>Tier</th><th>Class</th><th>Passengers</th><th>Movements</th><th>Centre</th></tr></thead><tbody id="frows">{static}</tbody></table></div><div id="fmore" style="margin-top:10px"></div></section>
<section class="section"><div class="head"><h2>Hypothetical centres</h2></div><div class="card" style="overflow-x:auto"><table class="tbl"><thead><tr><th>Centre site</th><th>Airports</th><th>Tier 1 / 2 / 3</th><th>Farthest</th></tr></thead><tbody>{ctrrows or '<tr><td colspan="4">No centres needed under these rules.</td></tr>'}</tbody></table></div>{more}</section>
{responsible(cc, nm, regs_by.get(cc, []))}
<section class="section"><div class="head"><h2>Sources</h2></div><div class="card"><ul class="small" style="margin:0;padding-left:18px;display:grid;gap:8px"><li><a href="https://ourairports.com/data/" rel="noopener">OurAirports</a>: airports, runways, frequencies.</li><li>GeoNames cities of 15,000 or more; World Bank population.</li>{"".join(f'<li><a href="{esc(x["url"])}" rel="noopener" target="_blank">{esc(x["label"])}</a></li>' for x in j["sources"])}</ul>
{('<p class="small" style="margin:12px 0 0">Towers already listed for ' + esc(nm) + ': <a href="/countries/' + slugs[cc] + '/">remote and digital sites in ' + esc(nm) + '</a>.</p>') if has_today else '<p class="small mute" style="margin:12px 0 0">No remote or digital towers are listed for this country on this site yet.</p>'}
<p class="small" style="margin:8px 0 0"><a href="/future/method/">Method and thresholds</a> · <a href="/data/future/c_{cc.lower()}.json">This country as JSON</a></p></div></section></div>'''
        sc = (MAPJS(B) + f'<script src="/assets/future.js?v={B.VER}"></script><script>DTFutureCountry("{cc.lower()}",{json.dumps(nm)});</script>')
        B.page(f"/future/countries/{slugs[cc]}/", f"{nm}: hypothetical remote tower future state | Digital Towers", f"{nm}: {n(s['gap_n'])} airports without a tower meet a remote service threshold, {n(s['tower_elig'])} towered airports fit a tier, and {n(s['centers'])} hypothetical centres could serve them. Illustrative only.", body, B.MAPASSETS + HEAD, sc)
    # ------------------------------------------------ world map
    scope_js = json.dumps({cc: {"s": slugs[cc], "n": names[cc]} for cc in SCOPE})
    allnames = json.dumps({cc: CS[cc]["name"] for cc in CS})
    body = f'''<div class="mapwrap"><div id="fwmap" aria-label="World map: today and possible future"></div>
<aside class="mpanel" aria-label="Controls"><div class="sheetbar"><button type="button" aria-label="Resize panel" onclick="this.closest('.mpanel').classList.toggle('min')"></button></div>
<div class="ph1" id="fctl"><div class="seg" role="group" aria-label="View"><button type="button" id="vtoday" aria-pressed="false">Today</button><button type="button" id="vfuture" aria-pressed="true">Possible future</button></div>
<p class="xs faint" style="margin:10px 0 0"><b>{DISC}</b></p>
<div id="fday" hidden><p class="small mute" style="margin:12px 0 0">Existing remote and digital towers from the <a href="/towers/">dataset</a>. Colour is status.</p></div>
<div id="ffut"><div class="chips" id="ftiers"></div><div class="chips" style="margin-top:8px"><button class="chip" id="fgap" aria-pressed="true" type="button">No tower today</button><button class="chip" id="ftow" aria-pressed="true" type="button">Towered candidates</button><button class="chip" id="fctr" aria-pressed="true" type="button">Centres</button></div>
<div class="chips"><select id="fcountry" aria-label="Country"><option value="">World</option></select></div></div>
<p class="small mute" id="fcount2" style="margin:10px 0 0"></p></div>
<div class="mlist" id="fdetail" style="padding:12px 14px"><p class="small mute">Tap a dot for details. <a href="/future/countries/">Country pages</a> · <a href="/future/market/">Market view</a> · <a href="/future/method/">Method</a></p></div></aside>
<div class="legend" id="flegend2"></div></div>'''
    sc = MAPJS(B) + f'<script src="/assets/future.js?v={B.VER}"></script><script>DTFutureWorld({scope_js},{allnames});</script>'
    B.page("/future/map/", "World view: today and possible future | Digital Towers", "Toggle between existing remote and digital towers and a hypothetical future state with suggested service tiers and shared centres. Illustrative only.", body, B.MAPASSETS + HEAD, sc, body_class="maponly")
    # ------------------------------------------------ market
    regs = collections.OrderedDict()
    for cc, s in CS.items():
        r = regs.setdefault(s["region"] or "Other", dict(assessed=0, g1=0, g2=0, g3=0, t1=0, t2=0, t3=0, x=0, t4=0, ctr=0, basis=0, gap=0, pax=0, ppl=0, nct=0))
        r["assessed"] += s["assessed"]; r["g1"] += s["tier_gap"]["1"]; r["g2"] += s["tier_gap"]["2"]; r["g3"] += s["tier_gap"]["3"]
        r["t1"] += s["tier_tower"]["1"]; r["t2"] += s["tier_tower"]["2"]; r["t3"] += s["tier_tower"]["3"]; r["x"] += s["tier_tower"]["X"]; r["t4"] += s["tier4"]; r["ctr"] += s["centers"]
        r["basis"] += s["gap_traffic_basis"]; r["gap"] += s["gap_n"]; r["pax"] += s["gap_pax"]; r["ppl"] += s["people"]["gap"]
    rr = ""
    for k, r in sorted(regs.items(), key=lambda x: -x[1]["gap"]):
        if r["assessed"] == 0: continue
        rr += f'<tr><td>{esc(k)}</td><td>{n(r["assessed"])}</td><td>{n(r["g1"])}</td><td>{n(r["g2"])}</td><td>{n(r["g3"])}</td><td>{n(r["t1"])}</td><td>{n(r["t2"])}</td><td>{n(r["t3"])}</td><td>{n(r["t4"])}</td><td>{n(r["x"])}</td><td>{n(r["ctr"])}</td><td>{round(100*r["basis"]/r["gap"]) if r["gap"] else 0}%</td></tr>'
    mx = max((CS[c]["gap_n"] + CS[c]["tower_elig"]) for c in CS) or 1
    top = sorted(CS, key=lambda c: -(CS[c]["gap_n"] + CS[c]["tower_elig"]))[:15]
    bars = "".join(f'<div class="barrow"><span class="bl">{esc(CS[c]["name"])}</span><span class="bar"><i style="width:{100*CS[c]["gap_n"]/mx:.1f}%;background:#ffb347"></i><i style="width:{100*CS[c]["tower_elig"]/mx:.1f}%;background:#4fd1c5"></i></span><span class="bv">{n(CS[c]["gap_n"])} / {n(CS[c]["tower_elig"])}</span></div>' for c in top)
    # existing market today
    stc = collections.Counter(t["status"] for t in B.T if t["kind"] in ("remote_tower", "rtc", "digital_tower", "remote_afis"))
    gp = sum(CS[c]["gap_n"] for c in CS)
    uc = [
     ("Regional airports with scheduled service and no tower", f"{n(sum(CS[c]['cls']['S'] for c in CS))} airports worldwide have scheduled service and no tower under this method. Many already run on radio advisory service. Remote service is one way to add traffic separation or longer hours where the volume justifies it."),
     ("Replacing or consolidating ageing towers", f"{n(W['tow'])} staffed-tower airports fit tiers 1 to 3. A tower that needs replacement is a decision point where a remote or digital option can be weighed against a new building."),
     ("Part-time and shoulder-hour coverage", f"{n(W['g2'])} airports without a tower fit tier 2. Part-time remote service matches airports with a few busy hours and long quiet ones."),
     ("Island, remote and medical access", f"{n(W['t4'])} isolated airfields fit tier 4. Cameras and surveillance feeds could give operators and pilots a picture, without claiming any air traffic service. The isolation test is distance only, not a medical or road study."),
     ("Contingency for existing towers", f"{n(W['x'])} large hubs are left alone. For those, digital tower technology is more likely to appear as a backup or an added view than as a replacement."),
     ("Training, simulation and trials", "Every tier needs controller training and human-in-the-loop trials. That work is not counted here, and the airport counts say nothing about it.")]
    ucs = "".join(f'<div class="card flat"><h3>{t}</h3><p class="small mute" style="margin:8px 0 0">{x}</p></div>' for t, x in uc)
    body = f'''<div class="wrap" style="padding-top:28px"><div class="crumbs"><a href="/future/">Future state</a> / Market and use cases</div><h1 style="margin-top:8px;font-size:clamp(30px,4.5vw,46px)">Market and use cases</h1>
<p class="mute" style="max-width:68ch;margin-top:10px">Counts of airports by suggested tier and region, from the method on the <a href="/future/method/">method page</a>. These are counts of places a rule flags, not demand, revenue or a forecast of what any country will buy.</p>{banner()}{subnav("/future/market/")}
{tiles([(n(W["assessed"]), "airports assessed"), (n(W["gap"]), "no tower, tier 1 to 3"), (n(W["tow"]), "towered, tier 1 to 3"), (n(W["t4"]), "isolated, tier 4"), (n(W["ctr"]), "hypothetical centres")])}
<section class="section"><div class="head"><h2>By region and tier</h2></div><div class="card" style="overflow-x:auto"><table class="tbl"><thead><tr><th>Region</th><th>Assessed</th><th>No tower T1</th><th>T2</th><th>T3</th><th>Towered T1</th><th>T2</th><th>T3</th><th>Tier 4</th><th>Hubs</th><th>Centres</th><th>Gap with a traffic figure</th></tr></thead><tbody>{rr}</tbody></table></div>
<p class="xs faint" style="margin-top:8px">T1, T2, T3 = tiers 1, 2, 3. "Gap with a traffic figure" is the share of no-tower airports that met a rule using a real passenger or movement number. The rest were placed by runway and size class, so treat those counts as weaker.</p></section>
<section class="section"><div class="head"><h2>Where the counts are largest</h2></div><div class="card"><p class="xs faint" style="margin:0 0 12px"><i class="dot" style="background:#ffb347"></i>No tower, tier 1 to 3 &nbsp; <i class="dot" style="background:#4fd1c5"></i>Towered, tier 1 to 3</p>{bars}</div></section>
<section class="section"><div class="head"><h2>Use cases</h2></div><div class="grid g2">{ucs}</div></section>
<section class="section"><div class="head"><h2>Where it stands today</h2></div><div class="card"><p class="small mute" style="margin:0 0 8px">On this site, {stc.get("operational", 0)} remote or digital tower sites are operational, {stc.get("trial", 0)} are in trial and {stc.get("planned", 0)} are planned, in {B.META["countries"]} countries. The method flags {n(gp)} airports without a tower. The distance between those two numbers is the point of this section, but it is not a market size: most flagged airports will never justify a remote tower.</p><p class="small" style="margin:0"><a href="/future/map/">See both on one map</a></p></div></section>
<section class="section"><div class="head"><h2>Honest caveats</h2></div><div class="card"><ul class="plain small mute"><li><b>Traffic data is uneven.</b> {n(W["scope_assessed"])} of the {n(W["assessed"])} assessed airports are in the {len(SCOPE)} country-page countries. The other countries use only OurAirports (runway, size class, scheduled flag) and no national traffic table.</li><li><b>US movements are estimates.</b> For airports without a tower the FAA forecast uses estimated operations. Some are high.</li><li><b>Tower presence is a proxy.</b> A tower frequency in OurAirports does not prove staffed hours, and frequency lists are incomplete in some countries, which can hide towers and overstate the gap.</li><li><b>Some figures are secondary.</b> India, Japan and Canada use ranked lists compiled on Wikipedia from national agencies; airports outside the lists have no figure.</li><li><b>Australia's open file ends in 2020</b>, so 2019 figures are used.</li><li><b>Thresholds are choices.</b> Change them and the counts change. They are on the method page so you can see how.</li><li><b>Not every gap should be filled.</b> A radio-advised airfield can be safe and economical as it is.</li></ul></div></section></div>'''
    B.page("/future/market/", "Market and use cases for digital towers | Digital Towers", "Counts of airports by suggested remote tower tier and region, use cases, and honest caveats. Hypothetical and illustrative.", body, HEAD)
    # airports.csv download
    import csv
    out = open(B.DIST + "/data/future/airports.csv", "w", newline="", encoding="utf8"); w = csv.writer(out)
    w.writerow(["country", "code", "name", "municipality", "lat", "lon", "class", "tier", "passengers", "movements", "traffic_source", "traffic_year", "centre", "reason"])
    for cc in SCOPE:
        j = json.load(open(src + f"/c_{cc.lower()}.json", encoding="utf8"))
        cn_ = {i: c for i, c in enumerate(j["centers"])}
        for x in j["airports"]:
            w.writerow([cc, x["id"], x["n"], x["m"], x["la"], x["lo"], x["cls"], x["tier"], x["pax"] if x["pax"] is not None else "", x["ops"] if x["ops"] is not None else "", x["ts"], x["ty"] or "", cn_[x["c"]]["id"] if x["c"] >= 0 else "", x["rs"]])
    out.close()

def MAPJS(B):
    return '<script src="/assets/maplibre-gl.js"></script><script src="/assets/pmtiles.js"></script><script src="/assets/basemaps.js"></script>'
