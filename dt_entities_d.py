# -*- coding: utf-8 -*-
# Entities added in sites3_1011: providers, vendors, regulators, programs, US timeline items, coverage notes, vendor list sweep.
import dt_entities as E

E.VENDORS += [
 dict(id="oki", name="OKI", aliases=["OKI"], country="Japan", url="https://www.oki.com/jp/press/2022/02/z21090.html",
  blurb="Japanese electronics company. Supplied the RVA-19 remote tower device the Japan Civil Aviation Bureau uses for remote air-ground service at Amami."),
]
E.ANSPS += [
 dict(id="romatsa", name="ROMATSA", aliases=["ROMATSA"], country="Romania", url="https://romatsa.ro/en/a/evenimente/premiera-in-romania:-dirijarea-prin-tehnologia-remote-tower",
  blurb="Romanian air traffic services administration. Controls Brașov-Ghimbav from its centre in Arad, about 450 km away."),
 dict(id="rlp", name="ŘLP ČR", aliases=["ŘLP ČR"], country="Czech Republic", url="https://zdopravy.cz/virtualni-vez-provoz-na-letisti-v-budejovicich-se-bude-ridit-na-dalku-z-ostravy-172109/",
  blurb="Czech state air navigation provider. Has said it plans a remote tower at Mošnov near Ostrava to control České Budějovice."),
 dict(id="skeyes", name="skeyes", aliases=["skeyes"], country="Belgium", url="https://annualreport.skeyes.be/en/innovation/digital-towers",
  blurb="Belgian air navigation service provider. Building a digital tower centre in Namur for Liège and Charleroi, due 2027."),
 dict(id="airwaysnz", name="Airways New Zealand", aliases=["Airways New Zealand"], country="New Zealand", url="https://www.airways.co.nz/media-centre/media-statements/airways-unveils-future-digital-air-traffic-control-tower",
  blurb="New Zealand's air navigation service provider. Trialled a prototype digital tower at Auckland in 2017 and awarded Frequentis the Invercargill contract in 2019."),
 dict(id="jcab", name="Japan Civil Aviation Bureau", aliases=["JCAB"], country="Japan", url="https://www.mlit.go.jp/koku/",
  blurb="Japan's civil aviation authority. Runs the remote air-ground service at Amami from Naha."),
 dict(id="qcaa", name="Qatar Civil Aviation Authority", aliases=["Qatar CAA"], country="Qatar", url="https://www.caa.gov.qa",
  blurb="Qatar's civil aviation authority and air navigation service provider. Adopted a hybrid digital tower model at Hamad International."),
 dict(id="caac", name="CAAC", aliases=["CAAC", "Xinjiang Airport Group"], country="China", url="https://www.icao.int/sites/default/files/APAC/Meetings/2024/2024%20SURICG-9/4-Information%20Papers/IP07_CHN-AI.7-Trial-Application-of-Remote-Tower-Optical-System-Technology-in-Civil-Aviation-Industry-of-China.pdf",
  blurb="Civil Aviation Administration of China. Has run remote tower optical system trials at Chizhou and Xinyuan Nalati."),
]
E.REGULATORS += [
 dict(id="casa", name="CASA", country="Australia", url="https://australianaviation.com.au/2026/02/navy-and-airservices-test-western-sydneys-digital-tower/", blurb="Civil Aviation Safety Authority of Australia. Reviewing the Western Sydney digital tower safety cases as of February 2026."),
 dict(id="qcaa-reg", name="Qatar CAA", country="Qatar", url="https://backend.ainonline.com/aviation-news/aerospace/2025-12-01/hamad-international-activates-virtual-tower-qatar", blurb="Adopted the hybrid digital tower model at Hamad International."),
 dict(id="caac-reg", name="CAAC", country="China", url="https://www.icao.int/sites/default/files/APAC/Meetings/2024/2024%20SURICG-9/4-Information%20Papers/IP07_CHN-AI.7-Trial-Application-of-Remote-Tower-Optical-System-Technology-in-Civil-Aviation-Industry-of-China.pdf", blurb="Began the experimental phase for remote tower optical systems in 2021."),
]
E.PROGRAMS += [
 dict(id="lvnl-centralised", name="LVNL Centralised Base (remote towers)", url="https://jaarverslag.lvnl.nl/jaarverslag-2025/veiligheid/projectportfolio-overige-projecten", blurb="Groningen and Maastricht Aachen to be run from Schiphol-Oost. Postponed since 2022 per LVNL's 2025 annual report."),
 dict(id="skeyes-namur", name="skeyes digital towers (Namur)", url="https://annualreport.skeyes.be/en/innovation/digital-towers", blurb="Namur centre for Liège and Charleroi, operational in 2027; test centre opened May 2024."),
 dict(id="airservices-das", name="Airservices Digital Aerodrome Services", url="https://www.airservicesaustralia.com/airservices-australia-launches-nations-first-purpose-built-digital-air-traffic-control-service-at-western-sydney-international-airport", blurb="Alice Springs trial (2011 to 2012), Sydney prototype (2019), and the Western Sydney digital tower."),
]
E.US_TIMELINE += [
 ("2026-09-04", "FAA Digital Tower Systems page last updated. It says the FAA is renaming Remote Tower to Digital Tower, is evaluating designs at the Technical Center and will update the page when (and if) it issues a System Design Approval. At our 11 Oct 2026 review it did not list the 2 Sep approval that PGL 26-06 describes.", "https://www.faa.gov/airports/planning_capacity/non_federal/digital_tower_systems"),
]
E.US_TIMELINE.sort(key=lambda x: x[0])

# Places checked where no verified remote tower exists, or where the finding is not a remote tower.
E.COVERAGE = [
 dict(country="Austria", result="No remote or digital tower found",
  text="Austro Control's pages and trade coverage reviewed on 11 October 2026 mention no remote or digital tower. Frequentis is headquartered in Austria, but its Austrian reference in the sources reviewed is a conventional tower (Salzburg, 2014).",
  links=[("Salzburg tower (Frequentis, 2014)", "https://www.atc-network.com/atc-news/new-austro-control-tower-in-salzburg-technical-solutions-from-frequentis-support-operations"), ("Austro Control overview", "https://en.wikipedia.org/wiki/Austro_Control")]),
 dict(country="United Arab Emirates (Abu Dhabi)", result="No remote tower found",
  text="Abu Dhabi Airports adopted Frequentis's Advanced Automated Tower concept, which puts tower information on one screen inside the tower. Frequentis's page names no remote digital tower at Abu Dhabi. No UAE remote tower announcement was found.",
  links=[("Frequentis: Abu Dhabi Advanced Automated Tower", "https://www.frequentis.com/en/node/4360")]),
 dict(country="Czech Republic", result="Planned only (added)",
  text="ŘLP has said it plans a remote tower at Mošnov to control České Budějovice. A later report says construction had not started. Both sites are listed as planned with low confidence.",
  links=[("Zdopravy.cz, Aug 2023", "https://zdopravy.cz/virtualni-vez-provoz-na-letisti-v-budejovicich-se-bude-ridit-na-dalku-z-ostravy-172109/"), ("Zdopravy.cz, later report", "https://zdopravy.cz/nova-era-rizeni-letadel-virtualni-vez-budou-mit-i-v-polsku-pripravy-bezi-take-u-nas-256221/")]),
 dict(country="Japan", result="Remote air-ground service only (added)",
  text="Amami has had a remote RADIO (aerodrome air-ground) service run from Naha since October 2021. That is not remote air traffic control, so it is typed separately. The Japan Civil Aviation Bureau's remote tower work in the sources reviewed is research.",
  links=[("OKI press release", "https://www.oki.com/jp/press/2022/02/z21090.html"), ("WING, July 2021", "https://www.jwing.net/news/40463")]),
 dict(country="India", result="Study only",
  text="An undated trade report says the Airports Authority of India was studying remote towers with the regulator and that Saab and Searidge were in talks. No installation or contract was found.",
  links=[("International Airport Review", "https://www.internationalairportreview.com/news/74028/remote-air-traffic-control-india/")]),
 dict(country="South Korea", result="Not a remote tower",
  text="Incheon's digital apron tower is an apron control system integrated with the existing physical tower. A fully digital remote tower for Terminal 3 is described as under consideration, with no date.",
  links=[("ICAO information paper, 2024", "https://www.icao.int/sites/default/files/APAC/Meetings/2024/2024%20AOP-SG-8/4-Information%20Papers/IP10-AI7-ROK_Digital-Apron-Tower-Transforming-Airport-Operations.pdf")]),
 dict(country="China", result="Trials only (added)",
  text="Two trials are listed: Xinyuan Nalati (2020) and Chizhou (2021 onward). No operational remote tower control service was found.",
  links=[("Aviation Week, May 2020", "https://ngstage.aviationweek.com/air-transport/safety-ops-regulation/china-trials-remote-tower-operations-xinjiang"), ("ICAO information paper, 2024", "https://www.icao.int/sites/default/files/APAC/Meetings/2024/2024%20SURICG-9/4-Information%20Papers/IP07_CHN-AI.7-Trial-Application-of-Remote-Tower-Optical-System-Technology-in-Civil-Aviation-Industry-of-China.pdf")]),
]

# Vendor and provider reference lists reviewed on 11 October 2026 and what each gave.
E.REFLISTS = [
 ("Frequentis", "Remote digital tower focus page", "Gives only totals (12 customers at 16 airports) and no names, so the total cannot be reconciled with this map.", "https://www.frequentis.com/en/air-traffic-management/focus-areas/remote-digital-tower"),
 ("NATS and Searidge", "NATS digital towers page", "Lists London City, Farnborough, Manchester, Miquelon and Saint-Pierre, Vigo, Hamad, Heathrow, Hong Kong and a Paris Orly logo. Hamad and Miquelon were added; Orly has no described tower.", "https://www.nats.aero/our-solutions/digital-towers/"),
 ("Saab", "Press releases 2024 and 2026", "Stockholm-Västerås (start 1 January 2028) and the skeyes Belgium test centre. Belgium added.", "https://www.saab.com/newsroom/press-releases/2026/saab-is-digitalizing-stockholm-vasteras-airport-with-remote-air-traffic-control-services"),
 ("Indra", "AlUla and Fintraffic releases", "Both already on the map; AlUla operating remotely from Jeddah per Indra's 11 Feb 2026 release.", "https://www.indragroup.com/cms-content/2026/02/260211-PR-Indra-AI-UIa-Digital-Tower-1.pdf"),
 ("Kongsberg", "Menorca and DAATS", "Menorca re-checked and shown as cancelled (reported). Kingston unchanged.", "https://www.kongsberg.com/news/news-archive/20202/spains-menorca-airport-to-operate-with-kongsbergs-remote-tower-system/"),
 ("Thales", "TopSky-ATC remote tower release", "A product extension with HungaroControl and Searidge as partners; no operating airport found.", "https://www.thalesgroup.com/en/news-centre/press-releases/thales-extends-topsky-atc-remote-tower-and-signs-partnerships"),
 ("Avinor, LFV, DFS, HungaroControl, skyguide", "Provider pages", "Already on the map. skyguide's Geneva plan (Sept 2022) names no vendor and no date.", "https://www.worldradio.ch/news/bitesize-news/airport-control-tower-to-go-virtual"),
 ("NAV CANADA and Kongsberg Geospatial", "DAATS program", "Kingston only; no other site found.", "https://www.kongsberggeospatial.com/news/nav-canada-selects-kongsberg-geospatial-as-the-technology-partner-to-equip-digital-aerodrome-air-traffic-services-daats-program"),
 ("Airservices Australia", "Western Sydney, Sydney, Alice Springs", "Western Sydney updated; Sydney 2019 prototype and Alice Springs 2011 to 2012 trial added.", "https://www.airservicesaustralia.com/airservices-australia-launches-nations-first-purpose-built-digital-air-traffic-control-service-at-western-sydney-international-airport"),
 ("CAAS and Changi", "NATS release on the prototype", "Prototype awarded; no operating service found. Entry unchanged.", "https://www.nats.aero/news/nats-wins-major-smart-digital-tower-contract-changi-airport/"),
 ("DECEA Brazil", "Santa Cruz installation", "Santa Cruz airbase, October 2019; no second site found.", "https://www.aviationpros.com/airport-business/airport-infrastructure-operations/airport-technology/communications/press-release/21111194/frequentis-usa-inc-brazil-implements-south-americas-first-remote-air-traffic-control-tower-with-frequentis"),
 ("FAA", "Digital Tower Systems page and PGL 26-06", "Page updated 4 Sep 2026 and renamed to Digital Tower Systems; PGL 26-06 confirms the Frequentis USA design approval of 2 Sep 2026.", "https://www.faa.gov/airports/planning_capacity/non_federal/digital_tower_systems"),
]
