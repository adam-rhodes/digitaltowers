# -*- coding: utf-8 -*-
# Digital Towers dataset, part D (sites3_1011, 2026-10-11): new towers, resolutions of the 8 unverified entries, fresh vendor sweep.
# Every fact carries a source URL. Dates may carry a third element: a key into S (their own source).
from dt_data_c import S, F, T, TOWERS

S.update(
 saab_alice="https://www.saab.com/newsroom/press-releases/2011/saab-and-airservices-australia-sign-contract-to-conduct-remote-atm-tower-trial",
 frq_au18="https://www.frequentis.com/sites/default/files/news/2018-11/AustralianAviation_FrequentisArticle2018_11.pdf",
 canso_syd="https://canso.org/airservices-australia-selects-searidge-for-digital-aerodrome-services-program/",
 as_wsi24="https://www.airservicesaustralia.com/airservices-australia-launches-nations-first-purpose-built-digital-air-traffic-control-service-at-western-sydney-international-airport",
 ausav_wsi26="https://australianaviation.com.au/2026/02/navy-and-airservices-test-western-sydneys-digital-tower/",
 td_wsi24="https://traveldaily.com.au/?p=396447",
 oki_amami="https://www.oki.com/jp/press/2022/02/z21090.html",
 jwing="https://www.jwing.net/news/40463",
 zd_cb23="https://zdopravy.cz/virtualni-vez-provoz-na-letisti-v-budejovicich-se-bude-ridit-na-dalku-z-ostravy-172109/",
 zd_poland="https://zdopravy.cz/nova-era-rizeni-letadel-virtualni-vez-budou-mit-i-v-polsku-pripravy-bezi-take-u-nas-256221/",
 aeroweb_cb22="https://www.aeroweb.cz/clanky/7831-letiste-ceske-budejovice-se-docka-rozsireni-provozu-pomuze-rlp",
 saab_ro22="https://www.saab.com/newsroom/press-releases/2022/saab-receives-order-for-a-digital-tower-in-romania",
 romatsa="https://romatsa.ro/en/a/evenimente/premiera-in-romania:-dirijarea-prin-tehnologia-remote-tower",
 ro_outage="https://romania.europalibera.org/a/aeroport-brasov-ghimbav-defectiune-turn-virtual/33084366.html",
 lvnl_ar25="https://jaarverslag.lvnl.nl/jaarverslag-2025/veiligheid/projectportfolio-overige-projecten",
 groningen2="https://www.groningenairport.nl/en/sustainability-innovation/project-portfolio/remote-tower",
 naviair_poc="https://www.frequentis.com/en/pr/first-integrated-digital-tower-denmark-completes-proof-concept-testing-frequentis-dfs-aerosense",
 menorca_info26="https://www.menorca.info/menorca/local/2026/09/16/2709357/gobierno-aprueba-plan-inversiones-del-aeropuerto-menorca-torre-control.html",
 vigoe_menorca="https://vigoe.es/vigo/local/surgen-dudas-sobre-la-futura-torre-de-control-remota-de-peinador-tras-el-precedente-fallido-de-menorca",
 kong_menorca="https://www.kongsberg.com/news/news-archive/20202/spains-menorca-airport-to-operate-with-kongsbergs-remote-tower-system/",
 tours_jt="https://www.lejournaltoulousain.fr/occitanie/haute-garonne/toulouse/tour-controle-aeroport-tours-delocalisee-toulouse-blagnac-188517/",
 sncta="https://www.sncta.fr/news/comtec-cda-projet-rtc-blagnac-crash-ou-remise-de-gaz-29552",
 auck17="https://www.internationalairportreview.com/news/40553/auckland-trials-digital-air-traffic-control/",
 airways_unveil="https://www.airways.co.nz/media-centre/media-statements/airways-unveils-future-digital-air-traffic-control-tower",
 airways_inv="https://www.airways.co.nz/media-centre/media-statements/invercargill-gets-nzs-first-digital-air-traffic-control-tower",
 inv19="https://www.airport-technology.com/news/frequentis-invercargill-airport/",
 skeyes_ar="https://annualreport.skeyes.be/en/innovation/digital-towers",
 saab_be24="https://www.saab.com/newsroom/press-releases/2024/saab-technology-in-new-digital-air-traffic-test-centre-in-belgium",
 ain_hamad="https://backend.ainonline.com/aviation-news/aerospace/2025-12-01/hamad-international-activates-virtual-tower-qatar",
 nats_dt="https://www.nats.aero/our-solutions/digital-towers/",
 greenland="https://www.airport-technology.com/contractors/traffic/frequentis/pressreleases/frequentis-digital-tower-solution-greenland/",
 frq_baires="https://www.frequentis.com/en/pr/frequentis-deploy-south-americas-first-remote-virtual-tower-buenos-aires-international-airport",
 icao_chn="https://www.icao.int/sites/default/files/APAC/Meetings/2024/2024%20SURICG-9/4-Information%20Papers/IP07_CHN-AI.7-Trial-Application-of-Remote-Tower-Optical-System-Technology-in-Civil-Aviation-Industry-of-China.pdf",
 avweek_xj="https://ngstage.aviationweek.com/air-transport/safety-ops-regulation/china-trials-remote-tower-operations-xinjiang",
 indra_alula="https://www.indragroup.com/cms-content/2026/02/260211-PR-Indra-AI-UIa-Digital-Tower-1.pdf",
 mq_searidge="https://militaryaerospace.com/commercial-aerospace/article/14228780/french-ansp-selects-searidge-remote-tower-for-remote-management-of-miquelon-airport",
 mq_aerot="https://www.aerotelegraph.com/wenn-im-kontrollturm-niemand-sitzt-remote-tower-miquelon",
 saab_vas26="https://www.saab.com/newsroom/press-releases/2026/saab-is-digitalizing-stockholm-vasteras-airport-with-remote-air-traffic-control-services",
 changi_nats="https://www.nats.aero/news/nats-wins-major-smart-digital-tower-contract-changi-airport/",
 geneva22="https://www.worldradio.ch/news/bitesize-news/airport-control-tower-to-go-virtual",
 brazil19="https://www.aviationpros.com/airport-business/airport-infrastructure-operations/airport-technology/communications/press-release/21111194/frequentis-usa-inc-brazil-implements-south-americas-first-remote-air-traffic-control-tower-with-frequentis",
 faa_dt="https://www.faa.gov/airports/planning_capacity/non_federal/digital_tower_systems",
 pgl2606="https://www.faa.gov/airports/aip/guidance_letters/aip_pgl_26_06",
 frq_ref="https://www.frequentis.com/en/air-traffic-management/focus-areas/remote-digital-tower",
 india17="https://www.internationalairportreview.com/news/74028/remote-air-traffic-control-india/",
 incheon="https://www.icao.int/sites/default/files/APAC/Meetings/2024/2024%20AOP-SG-8/4-Information%20Papers/IP10-AI7-ROK_Digital-Apron-Tower-Transforming-Airport-Operations.pdf",
 frq_adac="https://www.frequentis.com/en/node/4360",
 austro_sbg="https://www.atc-network.com/atc-news/new-austro-control-tower-in-salzburg-technical-solutions-from-frequentis-support-operations",
)

def find(i):
    for t in TOWERS:
        if t["id"] == i: return t
    raise KeyError(i)

def P(i, facts=None, dates=None, **kw):
    """Patch an existing tower. facts/dates are appended; other keywords replace fields."""
    t = find(i)
    for k, v in kw.items(): t[k] = v
    for f in facts or []: t["facts"].append(F(*f))
    for d in dates or []: t["dates"].append(tuple(d))
    return t

# ============ RESOLUTION OF THE 8 UNVERIFIED ENTRIES ============
# 1 Groningen
P("ehgg", status="planned", conf="low", program="lvnl-centralised",
  note="Two primary sources disagree. The airport's project page says the project is complete (December 2024) and that traffic is run from Schiphol Oost. LVNL's 2025 annual report says the programme has been postponed since 2022 and that a simulator and test environment was commissioned at Schiphol-Oost in 2025. We follow the operator report and show the site as planned.",
  facts=[("LVNL's 2025 annual report says the Centralised Base programme (Groningen and Maastricht Aachen) has been postponed since 2022 because of capacity and permit delays; further rollout follows full introduction of the iTEC-based centre automation system.", "lvnl_ar25"),
         ("The airport's own project page says 'This project is complete and will not be updated further' and that air traffic is controlled from the Remote Tower Centre at Schiphol Oost.", "groningen2")])
# 2 Schiphol RTC
P("schiphol-rtc", status="trial", conf="medium", program="lvnl-centralised",
  note="The 2025 milestone was a remote tower simulator and test environment. The sources do not describe live traffic being handled from here. Location is approximate.",
  facts=[("LVNL's 2025 annual report says a remote tower simulator and test environment was commissioned at Schiphol-Oost in 2025; it does not call it a live remote tower centre.", "lvnl_ar25")],
  dates=[("2025", "Remote tower simulator and test environment commissioned at Schiphol-Oost", "lvnl_ar25")])
# 3 Maastricht
P("ehbk", status="planned", conf="medium", program="lvnl-centralised",
  note="Postponed since 2022 according to LVNL.",
  facts=[("LVNL's 2025 annual report lists the Centralised Base programme as postponed since 2022; Maastricht Aachen is one of its two airports.", "lvnl_ar25")],
  dates=[("2022", "Centralised Base programme postponed (capacity and permit delays)", "lvnl_ar25")])
# 4 Billund
P("ekbi", status="planned", conf="low", note="Proof of concept done at Frequentis premises; no go-live notice found as of 11 October 2026.",
  facts=[("Naviair's integrated digital tower and approach solution completed proof-of-concept testing at Frequentis in Austria; the initial remote tower centre is to be at Billund airport. No go-live date is given.", "naviair_poc")])
# 5 Arad -> it is the control centre, not a remote airport
P("lrar", name="ROMATSA Arad control centre (remote tower hub)", kind="rtc", status="operational", conf="high", ansp="ROMATSA", vendors=["Saab"], lat=46.1766, lon=21.2620,
  note="Plotted at Arad airport; the building within the airport is not specified in the sources.",
  facts=[("ROMATSA says air traffic services for Brașov-Ghimbav are provided from Arad, almost 450 km away, from four working positions and a panoramic screen.", "romatsa"),
         ("Saab's February 2022 order includes a linked control room at the ROMATSA air traffic control centre in Arad.", "saab_ro22")])
find("lrar")["facts"] = [f for f in find("lrar")["facts"] if f["u"] != S["wiki"]]
P("lrbv", ansp="ROMATSA", conf="high", controlled_from="lrar", status="operational", regulator="",
  dates=[("2022-02-08", "Saab receives order for the digital tower (customer: UTI-led consortium; ROMATSA operates the service)", "saab_ro22"),
         ("2023-06-15", "Remote air traffic service begins; first flight lands at Brașov", "romatsa"),
         ("2024-08-18", "Camera feeds to Arad fail for about three hours; airspace around Brașov closed that evening, service restored about 22:30", "ro_outage")],
  facts=[("ROMATSA says the first flight under the remote tower service landed at Brașov-Ghimbav at 08:10 on 15 June, controlled from Arad.", "romatsa"),
         ("Romanian press reported the airport as the only one in Romania with remote air traffic control; a fault on 18 August 2024 suspended service for a few hours.", "ro_outage")])
# 6 Menorca
P("lemh", status="cancelled", conf="medium", vendors=["Kongsberg"],
  note="Spanish press describes the virtual tower as a failure and the physical tower is still in use. No official cancellation notice was found, so this is reported, not confirmed by Aena.",
  facts=[("Menorca.info, 16 September 2026, refers to the 'failure of the virtual system' and reports that the 2027 to 2031 investment plan includes no new tower; the existing tower is still in use.", "menorca_info26"),
         ("Vigoe.es, 2 April 2025, calls Menorca a 'failed precedent' and says Menorca ended up abandoning the remote tower system.", "vigoe_menorca")],
  dates=[("2020-10", "Kongsberg selected to supply the remote tower system (delivery expected 2021)", "kong_menorca")])
# 7 Tours
P("lfot", status="planned", conf="low",
  note="Schedules slipped: first end of 2023, then 2024. A union (SNCTA) said the project was stalled in March 2023. No go-live notice found as of 11 October 2026.",
  facts=[("Le Journal Toulousain, 13 December 2022: Tours to be controlled from Toulouse-Blagnac from 2024, with Frequentis supplying the visualisation.", "tours_jt"),
         ("The air traffic controllers' union SNCTA, 1 March 2023, called the Blagnac remote tower centre project stalled and asked for a pause.", "sncta")])
# 8 Auckland
P("nzaa", status="trial", conf="low",
  note="A prototype was shown in 2017 and was not handling live traffic. Frequentis said in 2019 that its system would initially serve as a contingency backup. No later notice found.",
  facts=[("Airways New Zealand and Frequentis began trialling a prototype digital tower at Auckland on 30 November 2017; the prototype was not used to manage live traffic.", "auck17")],
  dates=[("2017-11-30", "Prototype digital tower trial announced at Auckland", "auck17")])

# ============ UPDATES TO EXISTING ENTRIES ============
P("esow", dates=[("2026-09-21", "Saab announces a 15-year service contract for remote ATC at Stockholm-Västerås", "saab_vas26"), ("2028-01-01", "Planned start of remote service from Sundsvall", "saab_vas26")],
  facts=[("Saab's 21 September 2026 release gives a 15-year agreement, a camera tower and digital workstation, and a start date of 1 January 2028 with traffic controlled from its Remote Tower Center in Sundsvall.", "saab_vas26")], conf="high")
P("ysws", ansp="Airservices Australia", regulator="CASA", controlled_from="eastern-creek-dac",
  dates=[("2024-03-05", "Airservices announces a purpose-built digital aerodrome service for Western Sydney", "as_wsi24"), ("2026-02-12", "Navy helicopter flight calibrates and validates the camera feeds; CASA reviewing safety cases", "ausav_wsi26")],
  facts=[("Airservices says the airport will have no traditional tower and will be monitored by more than 20 cameras feeding a digital aerodrome service centre at Eastern Creek; partners are CDC and Frequentis Australasia.", "as_wsi24"),
         ("Australian Aviation, 12 February 2026: not yet operational, CASA is reviewing the safety cases, and Airservices aims to bring it online in July (about 25 cameras on a 45 m mast).", "ausav_wsi26")])
P("levx", regulator="AESA (Spain)")
P("cygk", regulator="Transport Canada")

# ============ NEW HUBS ============
T(id="eastern-creek-dac", name="Airservices Digital Aerodrome Service centre, Eastern Creek", icao="", country="Australia", cc="AU", kind="rtc", status="trial", vendors=["Frequentis"], ansp="Airservices Australia", regulator="CASA", program="airservices-das",
  lat=-33.8010, lon=150.8560, conf="medium", note="Location approximate (suburb of Eastern Creek).",
  dates=[("2024-03-05", "Centre announced for Western Sydney", "as_wsi24")],
  facts=[F("Airservices says air traffic services for Western Sydney will be provided from a digital aerodrome service centre at Eastern Creek.", "as_wsi24"), F("Australian Aviation, February 2026, says the digital tower is not yet operational and is expected to open with the airport in 2026.", "ausav_wsi26")])
T(id="adelaide-atc", name="Airservices Adelaide centre (2012 remote tower trial hub)", icao="", country="Australia", cc="AU", kind="rtc", status="cancelled", vendors=["Saab"], ansp="Airservices Australia", program="airservices-das",
  lat=-34.9462, lon=138.5306, conf="medium", note="Plotted at Adelaide airport; the exact facility is not specified in the sources.",
  facts=[F("The Saab and Airservices trial was to control aircraft at Alice Springs remotely from the Airservices facility in Adelaide, more than 1,500 km away.", "saab_alice")])
T(id="yssy", name="Sydney Airport (digital tower prototype)", icao="YSSY", country="Australia", cc="AU", kind="test_site", status="trial", vendors=["Searidge"], ansp="Airservices Australia", program="airservices-das",
  dates=[("2019-11-15", "Airservices selects Searidge for a prototype digital tower at Sydney", "canso_syd")], conf="low",
  note="The sources describe a prototype and an evaluation, not a service. No later notice found.",
  facts=[F("CANSO, 15 November 2019: Airservices selected Searidge to deliver a prototype 4K display with a wide view of a Sydney runway, as a first step toward possible contingency use and use at other aerodromes.", "canso_syd"), F("The Define stage was due to finish by March 2020.", "canso_syd")])
T(id="ybas", name="Alice Springs Airport (2012 remote tower trial)", icao="YBAS", country="Australia", cc="AU", kind="remote_tower", status="cancelled", vendors=["Saab"], ansp="Airservices Australia", controlled_from="adelaide-atc", program="airservices-das",
  dates=[("2011-06-01", "Saab and Airservices sign contract for a remote tower trial controlled from Adelaide", "saab_alice"), ("2012", "Trial run; network capability judged inadequate for a service", "frq_au18")], conf="medium",
  note="A trial that ended without a service, not a decommissioned operating tower.",
  facts=[F("Saab's 1 June 2011 release says Airservices staff would control Alice Springs from Adelaide during the trial, with no change to existing ATC arrangements.", "saab_alice"),
         F("Airservices' executive said in a 2018 article that the trial exposed weaknesses in the data network and 'network capability was not adequate to provide an air traffic control service' at the time.", "frq_au18")])

T(id="mosnov-rtc", name="ŘLP planned remote tower centre, Mošnov (Ostrava)", icao="", country="Czech Republic", cc="CZ", kind="rtc", status="planned", conf="low", ansp="ŘLP ČR", program="",
  lat=49.6963, lon=18.1111, note="Planned. In August 2023 the ŘLP chief said it should open in two to three years; a later report says construction had not started and an operational concept was still being drafted. No vendor is named.",
  dates=[("2023-08-19", "ŘLP chief says remote tower in Ostrava targeted within two to three years", "zd_cb23")],
  facts=[F("ŘLP, the Czech air navigation provider, plans a remote tower at Mošnov near Ostrava to control České Budějovice, which could later serve other regional airports.", "zd_cb23"),
         F("A later Zdopravy.cz report says the stated deadline had passed, construction had not started at either site, and an operational concept and cost-benefit analysis come first. A floor of the Mošnov control tower was reserved in 2016.", "zd_poland")])
T(id="lkcs", name="České Budějovice Airport", icao="LKCS", country="Czech Republic", cc="CZ", kind="remote_tower", status="planned", conf="low", ansp="ŘLP ČR", controlled_from="mosnov-rtc",
  lat=48.9458, lon=14.4272, note="Planned only. No vendor named and no approval or contract found.",
  dates=[("2022-09-01", "ŘLP confirms it is considering a remote tower for the airport", "aeroweb_cb22")],
  facts=[F("Aeroweb.cz, 1 September 2022: ŘLP was considering a remote virtual tower for České Budějovice within three to four years; no vendor is named.", "aeroweb_cb22"),
         F("Zdopravy.cz, 19 August 2023: all traffic including taxiing and parking would be controlled from Ostrava, probably starting as an on-request service.", "zd_cb23")])

T(id="rjka", name="Amami Airport (remote aerodrome air-ground service)", icao="RJKA", country="Japan", cc="JP", kind="remote_afis", status="operational", conf="high", vendors=["OKI"], ansp="JCAB", regulator="JCAB", program="",
  lat=28.4306, lon=129.7125, note="This is a remote aerodrome air-ground (RADIO) service from Naha, not remote air traffic control. Japan has no remote tower providing control service in the sources reviewed.",
  dates=[("2021-10-01", "Remote RADIO operation from Naha begins (Japan's first)", "oki_amami"), ("2022-02-28", "OKI announces delivery of the RVA-19 system to the Civil Aviation Bureau", "oki_amami")],
  facts=[F("OKI says Amami began remote RADIO operation on 1 October 2021, with a flight information officer at Naha Airport providing air-ground service through its RVA-19 remote tower device.", "oki_amami"),
         F("A July 2021 trade report describes Japan's remote tower work as research at the Electronic Navigation Research Institute, with a small remote air-ground system serving some low-traffic airports.", "jwing")])

T(id="namur-dtc", name="skeyes digital tower control centre, Namur", icao="", country="Belgium", cc="BE", kind="rtc", status="planned", vendors=["Saab"], ansp="skeyes", program="skeyes-namur", conf="high",
  lat=50.4674, lon=4.8720, note="Plotted at Namur; exact site approximate.",
  dates=[("2025", "Building completed", "skeyes_ar"), ("2027", "Planned to become operational (equipped in 2026)", "skeyes_ar")],
  facts=[F("skeyes says the Namur building was completed in 2025, will be further equipped in 2026 and become operational in 2027; Liège and Charleroi will be controlled from it.", "skeyes_ar")])
T(id="ebci", name="Charleroi Airport", icao="EBCI", country="Belgium", cc="BE", kind="remote_tower", status="planned", vendors=["Saab"], ansp="skeyes", controlled_from="namur-dtc", program="skeyes-namur", conf="high",
  lat=50.4592, lon=4.4538, facts=[F("Charleroi and Liège are the first skeyes airports to get digital towers, controlled from Namur from 2027.", "skeyes_ar")])
T(id="eblg", name="Liège Airport", icao="EBLG", country="Belgium", cc="BE", kind="remote_tower", status="planned", vendors=["Saab"], ansp="skeyes", controlled_from="namur-dtc", program="skeyes-namur", conf="high",
  lat=50.6374, lon=5.4432, facts=[F("Charleroi and Liège are the first skeyes airports to get digital towers, controlled from Namur from 2027.", "skeyes_ar")])
T(id="ebbr-dttc", name="skeyes Digital Tower Test Centre, Steenokkerzeel", icao="", country="Belgium", cc="BE", kind="test_site", status="trial", vendors=["Saab"], ansp="skeyes", program="skeyes-namur", conf="high",
  lat=50.9040, lon=4.4900, note="Plotted near Brussels Airport; exact site approximate.",
  dates=[("2024-05-31", "Digital Tower Test Centre unveiled", "saab_be24")],
  facts=[F("Saab's 31 May 2024 release says skeyes unveiled a Digital Tower Test Centre in Steenokkerzeel, a prototype for the Namur centre, built on Saab's Remote Tower solution, for training controllers.", "saab_be24")])

T(id="othh", name="Hamad International Airport (hybrid virtual tower)", icao="OTHH", lat=25.2731, lon=51.6081, country="Qatar", cc="QA", kind="hybrid", status="operational", vendors=["Searidge"], ansp="Qatar CAA", regulator="Qatar CAA", conf="medium",
  dates=[("2025-12-01", "Searidge and AIN report the virtual tower in operational service", "ain_hamad")],
  facts=[F("AIN, 1 December 2025: Hamad's virtual tower, built on Searidge's Chorus platform, 'has entered operational service' under a hybrid model adopted by the Qatar CAA; two positions are in the main tower and two in the backup and approach training centre.", "ain_hamad"),
         F("NATS lists Hamad as a certified hybrid digital tower and the first large-scale digital tower certified by safety regulators in the Middle East.", "nats_dt")])
T(id="bgqq", name="Qaqortoq Airport (new, local digital tower)", icao="", country="Greenland", cc="GL", kind="digital_tower", status="planned", vendors=["Frequentis"], ansp="", conf="low",
  lat=60.7164, lon=-46.0297, note="Plotted at Qaqortoq town; exact site approximate. Frequentis says similar systems are already in place at Nuuk and Ilulissat, but gives no dates, so those are not listed here.",
  facts=[F("Frequentis was awarded a contract (via the construction firm COMSA) for a Local Digital Tower at the new Qaqortoq airport; it describes a vision of centralised control from Nuuk.", "greenland")])
T(id="nznv", name="Invercargill Airport", icao="NZNV", country="New Zealand", cc="NZ", kind="remote_tower", status="unverified", vendors=["Frequentis"], ansp="Airways New Zealand", conf="low",
  lat=-46.4124, lon=168.3129, note="Contract awarded in 2019 with go-live expected in 2020. No go-live notice found.",
  dates=[("2019-02-27", "Airways awards Frequentis the contract for the first New Zealand digital tower", "inv19")],
  facts=[F("Airways New Zealand awarded Frequentis a contract for a remotely operated digital tower at Invercargill; controllers would start at the airfield and later move to a hub, with operation expected by 2020.", "inv19")])
T(id="saez", name="Buenos Aires Ezeiza International Airport", icao="SAEZ", country="Argentina", cc="AR", kind="remote_tower", status="planned", vendors=["Frequentis"], ansp="", conf="low",
  lat=-34.8222, lon=-58.5358, note="Vendor page only; customer and dates not stated. Treat as unconfirmed.",
  facts=[F("Frequentis says Ezeiza will receive an airport camera system as a first step toward what it calls South America's first remote virtual tower, with tower control to follow completion of a new tower.", "frq_baires")])
T(id="zsjh", name="Chizhou Jiuhuashan Airport (remote tower trial)", icao="ZSJH", country="China", cc="CN", kind="remote_tower", status="trial", conf="medium", ansp="CAAC", regulator="CAAC",
  lat=30.7403, lon=117.6856, note="A trial under the CAAC. The paper does not name a vendor.",
  dates=[("2021-09", "Remote tower optical system installed", "icao_chn")],
  facts=[F("A Chinese paper to ICAO describes a remote tower optical system installed at Chizhou in September 2021 and operated from the Anhui ATC Bureau about 180 km away; trial operations, with full remote service planned after trial and transition phases.", "icao_chn")])
T(id="zwnl", name="Xinyuan Nalati Airport (remote tower trial)", icao="ZWNL", country="China", cc="CN", kind="remote_tower", status="trial", conf="low", ansp="Xinjiang Airport Group", regulator="CAAC",
  lat=43.4318, lon=83.3786, note="One report, May 2020; no later notice found.",
  dates=[("2020-05-22", "China Express flight controlled remotely from Urumqi in what Aviation Week called China's first remote tower operation", "avweek_xj")],
  facts=[F("Aviation Week, 22 May 2020: a China Express Airlines flight was controlled remotely from the Xinjiang Airport Group's centre in Urumqi, 385 km away, at Xinyuan Nalati.", "avweek_xj")])
T(id="lfvm", name="Miquelon Airport (remote from Saint-Pierre)", icao="LFVM", country="France", cc="FR", kind="remote_tower", status="unverified", vendors=["Searidge"], ansp="DSNA", conf="low",
  lat=47.0958, lon=-56.3803, note="Selected in 2016. NATS lists a Miquelon and Saint-Pierre digital tower as a reference, while a union document calls earlier French attempts failures. Neither gives a service date.",
  dates=[("2016-03-09", "DSNA selects Searidge's remote tower for Miquelon, to be controlled from Saint-Pierre", "mq_searidge")],
  facts=[F("DSNA selected Searidge in March 2016 to remote Miquelon from Saint-Pierre, about 40 km away; cameras to be installed at Miquelon.", "mq_searidge"),
         F("NATS's digital tower page lists Miquelon and Saint-Pierre as a digital tower where controllers manage both airfields remotely from one location; no date is given.", "nats_dt")])


# ============ MORE FACTS FROM THE VENDOR AND PROVIDER SWEEP ============
P("lsgg", facts=[("skyguide said in September 2022 that Geneva's tower would close in favour of a virtual tower that would initially stay on site; no vendor or date is given.", "geneva22")],
  dates=[("2022-09-21", "skyguide plans a virtual tower for Geneva (vendor and date not stated)", "geneva22")])
P("sbsc", facts=[("Frequentis reported on 21 October 2019 that its smartVISION remote tower was installed at Santa Cruz in six months for DECEA's CISCEA, calling it the first in South America to provide actual remote ATC services.", "brazil19")],
  dates=[("2019-10-21", "Frequentis reports the remote tower installed at Santa Cruz", "brazil19")])
P("wsss", facts=[("NATS was awarded the CAAS contract for a smart digital tower prototype at Changi (a 22-month project with Searidge cameras; HungaroControl and ST Engineering also named); the release gives no go-live.", "changi_nats")])
P("kbow", facts=[("The FAA's Digital Tower Systems page (renamed from Remote Tower Systems, last updated 4 September 2026) says the FAA is evaluating designs at the Technical Center and will update it when (and if) it issues a System Design Approval.", "faa_dt")])
