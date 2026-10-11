# -*- coding: utf-8 -*-
# Digital Towers dataset, part A: sources and Europe-north. Every fact carries a source URL. Compiled 2026-10-11 from public sources.
S = dict(
 wiki="https://en.wikipedia.org/wiki/Remote_and_virtual_tower",
 avinor="https://om.avinor.no/en/aviation-safety/remote-controlled-towers",
 kong25="https://www.kongsberg.com/news/stories/2025/5/remote-towers-a-new-standard-for-air-traffic-management/",
 kong7="https://kongsberg.com/kda/news/news-archive/2024/kongsberg-to-deliver-remote-towers-to-seven-new-norwegian-airports",
 canso_indra="https://canso.org/the-worlds-largest-remote-tower-centre-operates-with-tower-and-communication-systems-from-indra/",
 ntb_bodo="https://kommunikasjon.ntb.no/pressemelding/verdens-storste-fjernstyrte-tarnsenter-apnet-i-bodo?publisherId=17421123&releaseId=17894324",
 lfv="https://lfv.se/en/services/airport-services/remote-tower-services",
 vasteras="https://defence-industry.eu/saab-wins-15-year-stockholm-vasteras-airport-contract-to-expand-remote-air-traffic-control-operations-from-sundsvall/",
 saab_navy="https://ukdefencejournal.org.uk/royal-navy-order-digital-towers-from-saab/",
 navy_tender="https://www.find-tender.service.gov.uk/Notice/005940-2025",
 ain_lfv="https://ainonline.com/aviation-news/air-transport/2015-04-22/swedens-lfv-inaugurates-first-remote-tower-operations",
 reuters_lcy="https://www.reuters.com/world/uk/ground-control-out-remote-control-london-city-airport-2021-04-29/",
 nats_vcf="https://www.nats.aero/news/worlds-first-approved-remote-atc-contingency-facility-unveiled/",
 nats_chasm="https://www.nats.aero/news/elevate/april-22/crossing-the-chasm-how-digital-towers-joined-the-mainstream/",
 mcr="https://www.nats.aero/news/manchester-airport-partners-with-nats-and-searidge-technologies-for-digital-transformation/",
 far="https://www.nats.aero/news/farnborough-airport-goes-digital-with-nats-and-searidge-technologies/",
 airporttech_cran="https://www.airport-technology.com/features/cranfield-digital-atc-tower/",
 hial="https://www.hial.co.uk/downloads/file/326/guide-to-remote-digital-towers-april-2021-hial-plots-its-path-to-a-digital-future-for-air-traffic-services-in-the-north-of-scotland",
 dfs_rtc="https://eu-lac-app.eu/public/uploads/DFS_Projekt_RTC_20231024_eng.pdf",
 dfs_bs="https://dfs-as.aero/dfs-aviation-services-eroeffnet-remote-tower-center-niedersachsen-in-braunschweig/",
 dfs_frq="https://www.internationalairportreview.com/news/19736/dfs-signs-contract-with-frequentis-to-install-remote-tower-technology",
 frq_munich="https://www.boerse-online.de/dpa-afx/irw-news-dr-reuter-investor-relations-von-sydney-bis-muenchen-wie-frequentis-mit-digitalen-flugtowern-weltweit-neue-standards-fuer-die-zivile-und-militaerische-infrastruktur-setzt-541645.html",
 katterbach="https://aerospaceglobalnews.com/news/frequentis-cooperates-with-us-dod-on-installation-of-digital-tower/",
 hc19="https://en.hungarocontrol.hu/press-room/news/remote-tower-technology-continues-to-bolster-service-continuity-in-Hungary",
 hc_indra="https://www.indragroup.com/en/news/indra-implementing-worlds-advanced-digital-remote-tower-hungarocontrol-budapest-airport",
 iaa="https://www.iaa.ie/air-traffic-management/innovation/remote-towers",
 lvnl="https://www.internationalairportreview.com/news/108966/sdats-contract-build-remote-towers",
 groningen="https://www.groningenairport.nl/en/sustainability/project-portfolio/remote-tower",
 naviair="https://canso.org/denmarks-naviair-to-tackle-airspace-efficiency-and-service-provision-with-integrated-remote-tower-and-approach-centre-from-frequentis-dfs-aerosense/",
 fintraffic="https://www.indragroup.com/cms-content/2026/06/260625-PR-Indra-digital-multiairport-tower-Fintraffic.pdf",
 eans="https://eans.ee/en/tegevused/arendustegevused/remote-tower",
 vilnius="https://www.nordicdefencesector.com/article/saab-receives-order-for-digital-air-traffic-control-tower-fo?lang=en",
 modlin="https://www.saab.com/newsroom/press-releases/2025/saabs-next-generation-digital-tower-selected-for-warsaw-modlin-airport-in-poland",
 saab_ro="https://www.saab.com/newsroom/press-releases/2022/saab-receives-order-for-a-digital-tower-in-romania",
 vigo="https://www.atc-network.com/atc-news/searidge-technologies/searidge-powers-spains-first-regulator-certified-digital-control-tower-at-vigo-airport",
 vigo_cap="https://centreforaviation.com/news/vigo-airport-to-launch-digital-control-tower-operations-in-jun-2025-1306697",
 menorca="https://www.kongsberg.com/news/news-archive/20202/spains-menorca-airport-to-operate-with-kongsbergs-remote-tower-system/",
 tours="https://canso.org/france-selects-frequentis-remote-digital-tower/",
 tours_fr="https://www.presse-citron.net/pour-la-premiere-fois-en-france-un-aeroport-va-etre-controle-a-distance/",
 enav="https://www.enav.it/en/node/17451",
 geneva="https://worldradio.ch/news/bitesize-news/airport-control-tower-to-go-virtual",
 daats="https://www.kongsberggeospatial.com/news/nav-canada-selects-kongsberg-geospatial-as-the-technology-partner-to-equip-digital-aerodrome-air-traffic-services-daats-program",
 brazil="https://canso.org/?p=11248",
 wsi="https://www.australianflying.com.au/latest/western-sydney-to-get-digital-tower",
 hk="https://www.atc-network.com/atc-news/searidge-technologies/industrys-largest-digital-tower-to-go-operational-in-hong-kong",
 changi="https://www.nats.aero/news/nats-wins-major-smart-digital-tower-contract-changi-airport/",
 auckland="https://www.frequentis.com/sites/default/files/pr/2019-08/20190822_FREQUENTIS_digitalTower_Auckland_IR_EN.pdf",
 alula="https://www.indragroup.com/en/news/al-ula-saudi-arabia-becomes-the-middle-easts-first-airport-to-be-operated-remotely-powered-by-sans-and-indras-digital-tower",
 jyo_town="https://www.leesburgva.gov/departments/capital-projects/current-projects/airport-projects/airport-air-traffic-control-tower",
 reason23="https://reason.org/aviation-policy-news/aviation-policy-news-another-u-s-remote-tower-project-loses-its-provider/",
 cdot="https://www.codot.gov/business/consultants/advertised-projects/2026/statewide-project-specific-digital-airport-traffic-control-tower-project-management-services/cdot-aero-digital-tower-program-management-sow_acc.pdf",
 bizwest="https://bizwest.com/?p=373279",
 ain_wh="https://backend.ainonline.com/aviation-news/2025-08-27/faa-tests-while-winter-haven-preps-remote-tower",
 bow_ai="https://airportimprovement.com/article/bartow-executive-redefines-air-traffic-control-with-digital-tower-and-onsite-controller-training/",
 bow_x10="https://canso.org/?p=117565",
 wral="https://www.wral.com/news/investigates/local-airport-johnston-regional-remote-tower-initiative-smithfield-october-2025/",
 faa_rts="https://www.faa.gov/airports/planning_capacity/non_federal/remote_tower_systems",
 pgl="https://www.faa.gov/airports/aip/guidance_letters/aip_pgl_26_06",
 fct="https://www.faa.gov/iija/airport-infrastructure/fct",
 citizen="https://citizenportal.ai/articles/10446362/colorado/executive/governors-office/governors-boards-and-commissions/colorado-aeronautical-board/division-says-digitaltower-guidance-issued-faa-system-approval-boosts-fct-eligibility-prospects",
 gar="https://globalairspaceradar.com/stories/digital-towers-in-the-nas-coming-soon/",
)

def F(t, k): return {"t": t, "u": S[k]}

TOWERS = []
def T(**kw):
    kw.setdefault("vendors", []); kw.setdefault("ansp", ""); kw.setdefault("controlled_from", "")
    kw.setdefault("program", ""); kw.setdefault("regulator", ""); kw.setdefault("dates", []); kw.setdefault("facts", [])
    kw.setdefault("conf", "medium"); kw.setdefault("note", ""); kw.setdefault("lat", None); kw.setdefault("lon", None)
    TOWERS.append(kw)

# ---------------- NORWAY (Avinor) ----------------
T(id="bodo-rtc", name="Bodø Remote Towers Centre", icao="ENBO", country="Norway", cc="NO", kind="rtc", status="operational",
  vendors=["Kongsberg", "Indra"], ansp="Avinor", program="ninox", regulator="Norwegian CAA",
  dates=[("2019-10", "First digital tower (Røst) in service"), ("2025-04", "14 airports operated from the centre")],
  facts=[F("Avinor lists 14 airports in operational service from the Bodø digital towers centre.", "avinor"),
         F("Kongsberg reports 14 airports managed from the Bodø centre as of April 2025, with seven more scheduled within two to three years.", "kong25"),
         F("A standalone digital tower for the new Bodø Airport is planned for 2029.", "kong7"),
         F("Avinor and Kongsberg signed the NINOX programme agreement in 2015.", "kong25")],
  conf="high", note="Avinor describes Kongsberg Defence & Aerospace and Indra as suppliers for the first service at Røst.")
NO_OP = [("enrs","Røst","ENRS","2019-10"),("enss","Vardø","ENSS","2020-10"),("enhk","Hasvik","ENHK","2020-11"),("enbv","Berlevåg","ENBV","2020-11"),
 ("enro","Røros","ENRO","2022-06"),("enmh","Mehamn","ENMH","2022-06"),("enrm","Rørvik","ENRM","2022-09"),("ennm","Namsos","ENNM","2022-09"),
 ("ensh","Svolvær","ENSH","2023-01"),("ensg","Sogndal","ENSG","2023-02"),("enfd","Førde","ENFD","2023-02"),("enml","Molde","ENML","2025-04"),
 ("enlk","Leknes","ENLK","2025-04"),("enst","Sandnessjøen","ENST","2025-04")]
for sid, nm, ic, dt in NO_OP:
    T(id=sid, name=nm+" Airport", icao=ic, country="Norway", cc="NO", kind="remote_tower", status="operational", vendors=["Kongsberg","Indra"],
      ansp="Avinor", controlled_from="bodo-rtc", program="ninox", dates=[(dt,"Digital tower in service (Avinor implementation list)")],
      facts=[F("Listed by Avinor as an airport in operational service from Bodø; in-service month "+dt+".", "avinor")], conf="high")
NO_PL = [("enbs","Båtsfjord","ENBS"),("envd","Vadsø","ENVD"),("ensr","Sørkjosen","ENSR"),("ensd","Sandane","ENSD"),("enms","Mosjøen","ENMS"),("enov","Ørsta-Volda","ENOV")]
for sid, nm, ic in NO_PL:
    T(id=sid, name=nm+" Airport", icao=ic, country="Norway", cc="NO", kind="remote_tower", status="planned", vendors=["Kongsberg"],
      ansp="Avinor", controlled_from="bodo-rtc", program="ninox", dates=[("2027","Planned operation from Bodø (Kongsberg delivery due 2027)")],
      facts=[F("Avinor's board decided in February 2024 to move this tower to the Bodø centre; Kongsberg delivers sensors for operation from 2027.", "kong7"),
             F("Avinor lists it in phase 2, planned for 2026 or 2027.", "avinor")], conf="high")
T(id="enra-new", name="Mo i Rana Airport (new airport)", icao="ENRA", country="Norway", cc="NO", kind="remote_tower", status="planned", vendors=["Kongsberg"],
  ansp="Avinor", controlled_from="bodo-rtc", program="ninox", dates=[("2027","Planned completion spring 2027")],
  facts=[F("The new Mo i Rana airport is to be operated from Bodø, with completion planned for spring 2027.", "avinor"),
         F("Kongsberg delivers the remote tower infrastructure for the new airport in 2027.", "kong7")], conf="high")
T(id="enbo-new", name="New Bodø Airport (local digital tower)", icao="ENBO", country="Norway", cc="NO", kind="digital_tower", status="planned", vendors=["Kongsberg"],
  ansp="Avinor", program="ninox", dates=[("2029","Delivery due 2029")], lat=67.2692, lon=14.3653,
  facts=[F("A separate installation for the new Bodø Airport is due in 2029.", "kong7"),
         F("Avinor says the new Bodø and Kirkenes airports will have local digital tower solutions rather than operation from the centre.", "avinor")], conf="high",
  note="Plotted at the existing Bodø airport; the new airport site is nearby.")
T(id="enkr", name="Kirkenes Airport", icao="ENKR", country="Norway", cc="NO", kind="digital_tower", status="planned", vendors=[],
  ansp="Avinor", program="ninox", facts=[F("Avinor says Kirkenes will have a local digital tower solution.", "avinor")], conf="medium")

# ---------------- SWEDEN (LFV) ----------------
T(id="sundsvall-rtc", name="LFV Remote Tower Centre Sundsvall", icao="ESNN", country="Sweden", cc="SE", kind="rtc", status="operational", vendors=["Saab"], ansp="LFV",
  program="lfv-rtc", dates=[("2015-04","H24 remote operation began at Örnsköldsvik")],
  facts=[F("The Sundsvall centre serves Sundsvall-Timrå, Sälen, Örnsköldsvik and Linköping; Stockholm-Västerås is to be the fifth.", "vasteras"),
         F("LFV's page says the Sundsvall centre serves Örnsköldsvik over 150 km away.", "lfv")], conf="high")
T(id="esno", name="Örnsköldsvik Airport", icao="ESNO", country="Sweden", cc="SE", kind="remote_tower", status="operational", vendors=["Saab"], ansp="LFV",
  controlled_from="sundsvall-rtc", program="lfv-rtc", dates=[("2014-10","Operational approval"),("2015-04","H24 remote operation began")],
  facts=[F("LFV reports operational approval by the end of October 2014 and H24 operation from April 2015.", "lfv"),
         F("Saab describes Örnsköldsvik as the first airport in the world with remote air traffic control.", "saab_navy"),
         F("AIN reported the inauguration of LFV's first remote tower operations in April 2015.", "ain_lfv")], conf="high")
T(id="esnn", name="Sundsvall-Timrå Airport", icao="ESNN", country="Sweden", cc="SE", kind="remote_tower", status="operational", vendors=["Saab"], ansp="LFV",
  controlled_from="sundsvall-rtc", program="lfv-rtc", facts=[F("Named among the airports served from the Sundsvall centre.", "vasteras")], conf="medium",
  note="Plotted slightly offset from the centre marker, which shares the airport coordinates.", lat=62.5281, lon=17.4439)
T(id="esks", name="Scandinavian Mountains Airport (Sälen)", icao="ESKS", country="Sweden", cc="SE", kind="remote_tower", status="operational", vendors=["Saab"], ansp="LFV",
  controlled_from="sundsvall-rtc", program="lfv-rtc", dates=[("2019-12","Opened without a conventional tower")],
  facts=[F("Opened in December 2019 with no traditional tower; run from Sundsvall.", "wiki"), F("Named among the airports served from Sundsvall.", "vasteras")], conf="medium")
T(id="essl", name="Linköping City Airport", icao="ESSL", country="Sweden", cc="SE", kind="remote_tower", status="operational", vendors=["Saab"], ansp="LFV",
  controlled_from="sundsvall-rtc", program="lfv-rtc", facts=[F("Named among the airports served from the Sundsvall centre.", "vasteras")], conf="medium")
T(id="stockholm-rtc", name="LFV Remote Tower Centre Stockholm", icao="ESSA", country="Sweden", cc="SE", kind="rtc", status="operational", vendors=["Saab"], ansp="LFV",
  program="lfv-rtc", dates=[("2021-06-01","Centre opened")], lat=59.6519, lon=17.9186,
  facts=[F("RTC Stockholm opened on 1 June 2021 and serves some Swedavia airports.", "lfv")], conf="medium", note="Exact centre location not stated; plotted at Arlanda.")
for sid, nm, ic, st, dt, c in [("esnq","Kiruna Airport","ESNQ","operational","2021","medium"),("esnz","Åre Östersund Airport","ESNZ","operational","2021-12-01","medium"),
                               ("esnu","Umeå Airport","ESNU","planned","","low"),("esms","Malmö Airport","ESMS","planned","","low")]:
    T(id=sid, name=nm, icao=ic, country="Sweden", cc="SE", kind="remote_tower", status=st, vendors=["Saab"], ansp="LFV", controlled_from="stockholm-rtc", program="lfv-rtc",
      dates=([(dt,"Connected to RTC Stockholm")] if dt else []),
      facts=[F("LFV lists it as served from RTC Stockholm." + (" Kiruna was the first airport connected." if ic=="ESNQ" else "") + (" Umeå and Malmö are described as the two remaining airports, with no connection date given." if st=="planned" else ""), "lfv")], conf=c)
T(id="esow", name="Stockholm-Västerås Airport", icao="ESOW", country="Sweden", cc="SE", kind="remote_tower", status="planned", vendors=["Saab"], ansp="Saab (service contract)",
  controlled_from="sundsvall-rtc", program="lfv-rtc", dates=[("2026-09-22","Contract announced"),("2028-01-01","Agreement takes effect")],
  facts=[F("Saab won a 15-year contract to install and operate remote air traffic control services; announced 22 September 2026, effective 1 January 2028.", "vasteras")], conf="high")
