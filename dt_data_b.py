# -*- coding: utf-8 -*-
from dt_data_a import S, F, T, TOWERS

# ---------------- UNITED KINGDOM ----------------
T(id="swanwick-dtc", name="NATS Swanwick Digital Tower Centre", icao="", country="United Kingdom", cc="GB", kind="rtc", status="operational", vendors=["Saab"], ansp="NATS",
  program="", lat=50.8737, lon=-1.2473, facts=[F("London City is controlled remotely from the NATS centre at Swanwick.", "wiki")], conf="medium",
  note="Plotted at Swanwick; exact building location approximate.")
T(id="eglc", name="London City Airport", icao="EGLC", country="United Kingdom", cc="GB", kind="remote_tower", status="operational", vendors=["Saab"], ansp="NATS",
  controlled_from="swanwick-dtc", dates=[("2021","Switched to remote ATC (first major airport)")],
  facts=[F("Reuters reported the move to remote air traffic control in April 2021.", "reuters_lcy"), F("Saab names London City as a customer of its digital tower.", "saab_navy")], conf="high")
T(id="egtc", name="Cranfield Airport", icao="EGTC", country="United Kingdom", cc="GB", kind="remote_tower", status="operational", vendors=["Saab"], ansp="Cranfield University",
  dates=[("2018-12-13","Digital ATC centre opened (first in the UK)")],
  facts=[F("Wikipedia, citing Cranfield University, gives 13 December 2018 as the opening date of the UK's first digital air traffic control centre.", "wiki"), F("Airport Technology feature on the Cranfield digital tower.", "airporttech_cran")], conf="medium")
T(id="egll", name="Heathrow Virtual Contingency Facility", icao="EGLL", country="United Kingdom", cc="GB", kind="contingency", status="operational", vendors=["Searidge"], ansp="NATS",
  dates=[("2009","Contingency facility unveiled")],
  facts=[F("NATS unveiled the world's first approved remote ATC contingency facility in 2009.", "nats_vcf"), F("NATS and Searidge run a Digital Tower Laboratory in the Heathrow tower.", "nats_chasm")], conf="medium")
for sid, nm, ic, la, lo in [("egdo","RNAS Predannack","EGDO",50.0003,-5.2272),("egdr","RNAS Culdrose","EGDR",50.0859,-5.2557)]:
    T(id=sid, name=nm, icao=ic, lat=la, lon=lo, country="United Kingdom", cc="GB", kind="remote_tower", status="operational", vendors=["Saab"], ansp="Royal Navy",
      dates=[("2021-02","Saab order for Predannack announced"),("2025-02-19","Support and maintenance contract concluded")],
      facts=[F("Saab signed to provide a digital air traffic control solution at Predannack, announced 25 February 2021.", "saab_navy"),
             F("A three-year, GBP 710,000 support contract for the remote tower equipment at Predannack and Culdrose was concluded 19 February 2025.", "navy_tender")],
      conf="medium", note="In-service status is inferred from the 2025 support contract.")
T(id="egcc", name="Manchester Airport (hybrid digital tower)", icao="EGCC", country="United Kingdom", cc="GB", kind="hybrid", status="planned", vendors=["Searidge"], ansp="NATS",
  dates=[("2025-02-26","Announced"),("2026","Digital apron management due to go live")],
  facts=[F("Hybrid digital control tower with camera arrays on Terminal 2 piers; the release says the apron system is due to go live in 2026.", "mcr")], conf="medium",
  note="Hybrid means controllers keep the window view and add video; it is not a remote tower. Go-live not confirmed.")
T(id="eglf", name="Farnborough Airport (hybrid digital tower)", icao="EGLF", country="United Kingdom", cc="GB", kind="hybrid", status="planned", vendors=["Searidge"], ansp="NATS",
  dates=[("2023-10-03","Announced")], facts=[F("Hybrid digital working position, described as a digital extension of the existing tower.", "far")], conf="medium",
  note="Hybrid, not a remote tower. No go-live confirmation found.")
T(id="egpe", name="Inverness (HIAL Combined Surveillance Centre)", icao="EGPE", country="United Kingdom", cc="GB", kind="rtc", status="cancelled", vendors=[], ansp="HIAL",
  dates=[("2022-08-24","Project cancelled")], 
  facts=[F("HIAL planned to move air traffic services for Dundee, Sumburgh, Kirkwall and Stornoway into Inverness; the project of about GBP 34 million was cancelled on 24 August 2022.", "wiki"),
         F("HIAL's 2021 guide describes the plan for remote and digital towers in the north of Scotland.", "hial")], conf="medium")

# ---------------- GERMANY ----------------
T(id="leipzig-rtc", name="DFS Remote Tower Control Center Leipzig", icao="EDDP", country="Germany", cc="DE", kind="rtc", status="operational", vendors=["Frequentis"], ansp="DFS",
  program="dfs-rtc", dates=[("2018-12-04","First remote landing clearance (Saarbrücken)")],
  facts=[F("As of October 2023 the Leipzig centre connected Saarbrücken, Erfurt and Dresden.", "dfs_rtc"), F("DFS signed with Frequentis for remote tower technology.", "dfs_frq")], conf="high")
T(id="eddr", name="Saarbrücken Airport", icao="EDDR", country="Germany", cc="DE", kind="remote_tower", status="operational", vendors=["Frequentis"], ansp="DFS", controlled_from="leipzig-rtc", program="dfs-rtc",
  dates=[("2018-12-04","Remote operation began; about 450 km from Leipzig")], facts=[F("Operational since 4 December 2018, when a Luxair flight was the first aircraft controlled remotely from Leipzig.", "dfs_rtc")], conf="high")
T(id="edde", name="Erfurt-Weimar Airport", icao="EDDE", country="Germany", cc="DE", kind="remote_tower", status="operational", vendors=["Frequentis"], ansp="DFS", controlled_from="leipzig-rtc", program="dfs-rtc",
  dates=[("2022-04-28","Remote operation began")], facts=[F("Operational since 28 April 2022, about 110 km from Leipzig.", "dfs_rtc")], conf="high")
T(id="eddc", name="Dresden Airport", icao="EDDC", country="Germany", cc="DE", kind="remote_tower", status="trial", vendors=["Frequentis"], ansp="DFS", controlled_from="leipzig-rtc", program="dfs-rtc",
  dates=[("2023-10","Validation under way")], facts=[F("In October 2023 the new system's implementation was almost complete, with validations planned for 2024.", "dfs_rtc")], conf="medium",
  note="Whether it moved to operation after 2024 is not confirmed here.")
T(id="braunschweig-rtc", name="DFS Aviation Services Remote Tower Center Niedersachsen", icao="EDVE", country="Germany", cc="DE", kind="rtc", status="operational", vendors=["Frequentis"], ansp="DFS Aviation Services",
  program="dfs-rtc", dates=[("2024-11-28","Opening ceremony")],
  facts=[F("Opened 28 November 2024 with capacity for six airports; operated with Frequentis DFS Aerosense and ESPA.", "dfs_bs")], conf="high")
T(id="edve", name="Braunschweig-Wolfsburg Airport", icao="EDVE", country="Germany", cc="DE", kind="remote_tower", status="operational", vendors=["Frequentis"], ansp="DFS Aviation Services", controlled_from="braunschweig-rtc", program="dfs-rtc",
  dates=[("2024-11","Services partly provided from the centre")], facts=[F("In the November 2024 operational introduction phase, services were already partly provided from the centre.", "dfs_bs")], conf="medium", lat=52.3192, lon=10.5561)
T(id="edwe", name="Emden Airport", icao="EDWE", country="Germany", cc="DE", kind="remote_tower", status="planned", vendors=["Frequentis"], ansp="DFS Aviation Services", controlled_from="braunschweig-rtc", program="dfs-rtc",
  facts=[F("DFS said in November 2024 that Emden would be connected in the following months, the first integration of an AFIS into a remote tower centre.", "dfs_bs")], conf="medium",
  note="Wikipedia lists Emden as served from Braunschweig since 2024; the DFS release says planned. Unresolved.")
T(id="eddm", name="Munich Airport (validation virtual tower)", icao="EDDM", country="Germany", cc="DE", kind="test_site", status="trial", vendors=["Frequentis"], ansp="DFS",
  dates=[("2026-07-30","Reported as being installed and tested under real conditions")],
  facts=[F("A validation system is being installed and tested as a virtual tower during the tower renovation (Frequentis DFS Aerosense).", "frq_munich")], conf="medium")
T(id="etin", name="Garrison Katterbach (US Army)", icao="ETIN", country="Germany", cc="DE", kind="digital_tower", status="operational", vendors=["Frequentis"], ansp="US Army", program="",
  dates=[("2025-06-05","Reported live and operational")],
  facts=[F("The US Department of Defense and Frequentis Defense said their first digital air traffic control tower was live and operational at Garrison Katterbach, Germany.", "katterbach")], conf="high")

# ---------------- HUNGARY, IRELAND, NETHERLANDS, DENMARK ----------------
T(id="lhbp", name="Budapest Ferenc Liszt International Airport", icao="LHBP", country="Hungary", cc="HU", kind="remote_tower", status="operational", vendors=["Indra"], ansp="HungaroControl",
  dates=[("2017","Remote tower operations launched"),("2023-03","New Indra modular remote tower centre in factory acceptance")],
  facts=[F("HungaroControl was operationally certified to provide tower services using a remote tower; operations launched in 2017 and the remote facility took over during a physical-tower upgrade.", "hc19"),
         F("Indra is supplying a modular integrated remote tower centre; live operations were expected in 2024.", "hc_indra")], conf="medium",
  note="The vendor of the 2017 system is not named in the cited release. The Indra system is a separate, newer deployment. Current status of the Indra system is not confirmed here.")
T(id="dublin-atcc", name="IAA Dublin ATC Centre (remote tower hub)", icao="EIDW", country="Ireland", cc="IE", kind="rtc", status="trial", vendors=["Saab"], ansp="IAA", program="sesar",
  dates=[("2016-06","Remote tower trials began")], facts=[F("The IAA plans to provide air movements and surface control for Cork and Shannon from the Dublin centre; trials began in June 2016.", "iaa")], conf="medium")
for sid, nm, ic in [("eick","Cork Airport","EICK"),("einn","Shannon Airport","EINN")]:
    T(id=sid, name=nm, icao=ic, country="Ireland", cc="IE", kind="remote_tower", status="trial", vendors=["Saab"], ansp="IAA", controlled_from="dublin-atcc", program="sesar",
      dates=[("2016-06","Multiple remote tower trial from Dublin"),("2023-01","SESAR grant announced for a demonstration")],
      facts=[F("IAA page dated 30 January 2023 announces a SESAR demonstration grant; no go-live date is given and European regulatory approval is still needed.", "iaa")], conf="medium")
T(id="ehgg", name="Groningen Airport Eelde", icao="EHGG", country="Netherlands", cc="NL", kind="remote_tower", status="unverified", vendors=["Saab"], ansp="LVNL",
  controlled_from="schiphol-rtc", dates=[("2019-12","SDATS contract"),("2024-12","Airport project page marks the project complete")],
  facts=[F("LVNL chose Saab Digital Air Traffic Solutions for Groningen and Maastricht Aachen; service was planned from the end of 2021.", "lvnl"),
         F("The airport's project page lists May 2018 to December 2024 and says air traffic control is run remotely from the Remote Tower Centre at Schiphol Oost.", "groningen")], conf="low",
  note="No go-live notice found.")
T(id="schiphol-rtc", name="LVNL Remote Tower Centre (Schiphol Oost)", icao="", country="Netherlands", cc="NL", kind="rtc", status="unverified", vendors=["Saab"], ansp="LVNL", lat=52.3050, lon=4.8000,
  facts=[F("Named on the Groningen project page as the location from which Groningen is run remotely.", "groningen")], conf="low", note="Location approximate.")
T(id="ehbk", name="Maastricht Aachen Airport", icao="EHBK", country="Netherlands", cc="NL", kind="remote_tower", status="unverified", vendors=["Saab"], ansp="LVNL", controlled_from="schiphol-rtc",
  facts=[F("Named in the December 2019 LVNL contract with Saab; current status not confirmed.", "lvnl")], conf="low")
T(id="ekbi", name="Billund Airport", icao="EKBI", country="Denmark", cc="DK", kind="remote_tower", status="unverified", vendors=["Frequentis"], ansp="Naviair",
  dates=[("2020-02","Naviair selects integrated remote tower and approach centre")],
  facts=[F("Naviair chose Frequentis DFS Aerosense for an integrated remote digital tower with approach automation, Billund first; centre expected operational in 2022.", "naviair")], conf="low",
  note="No go-live notice found.")
