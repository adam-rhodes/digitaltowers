# -*- coding: utf-8 -*-
from dt_data_b import S, F, T, TOWERS

# ---------------- FINLAND, ESTONIA, BALTICS, POLAND, ROMANIA ----------------
T(id="vantaa-rtc", name="Fintraffic Remote Tower Centre Vantaa", icao="EFHK", country="Finland", cc="FI", kind="rtc", status="planned", vendors=["Indra"], ansp="Fintraffic ANS", program="fintraffic-rtc",
  dates=[("2026-06-25","Indra announces deployment of the multi-airport centre")], lat=60.3172, lon=24.9633,
  facts=[F("Indra and Fintraffic announced a digital remote tower centre near Helsinki where each controller can manage up to three airports from one workstation.", "fintraffic")], conf="high")
for sid, nm, ic in [("efma","Mariehamn Airport","EFMA"),("eftu","Turku Airport","EFTU"),("efva","Vaasa Airport","EFVA"),("efkt","Kittilä Airport","EFKT"),("efiv","Ivalo Airport","EFIV"),("efks","Kuusamo Airport","EFKS"),("efou","Oulu Airport","EFOU")]:
    T(id=sid, name=nm, icao=ic, country="Finland", cc="FI", kind="remote_tower", status="planned", vendors=["Indra"], ansp="Fintraffic ANS", controlled_from="vantaa-rtc", program="fintraffic-rtc",
      facts=[F("One of seven airports covered by the Vantaa multi-airport centre announced on 25 June 2026; no schedule is given.", "fintraffic")], conf="medium")
T(id="tallinn-rtc", name="EANS Remote Tower Centre Tallinn", icao="EETN", country="Estonia", cc="EE", kind="rtc", status="operational", vendors=["Adacel"], ansp="EANS", program="",
  dates=[("2016","EANS starts the remote tower project with Cybernetica"),("2022-02-24","Cybernetica sells its ATM remote tower technology; Adacel takes over")],
  facts=[F("The centre is at the Tallinn ATCC; Tartu was the first airport served from it, from April 2023.", "eans")], conf="high")
T(id="eetu", name="Tartu Airport", icao="EETU", country="Estonia", cc="EE", kind="remote_tower", status="operational", vendors=["Adacel"], ansp="EANS", controlled_from="tallinn-rtc",
  dates=[("2023-04","First airport served from the Tallinn centre")], facts=[F("Tartu received air traffic services from the Remote Tower Centre starting April 2023.", "eans")], conf="high")
for sid, nm, ic in [("eeke","Kuressaare Airport","EEKE"),("eepu","Pärnu Airport","EEPU"),("eeka","Kärdla Airport","EEKA")]:
    T(id=sid, name=nm, icao=ic, country="Estonia", cc="EE", kind="remote_tower", status="planned", vendors=["Adacel"], ansp="EANS", controlled_from="tallinn-rtc",
      facts=[F("EANS planned to digitise all four regional Estonian airports (Tartu, Kuressaare, Pärnu, Kärdla).", "eans")], conf="low", note="Current status not confirmed.")
T(id="eyvi", name="Vilnius Airport", icao="EYVI", country="Lithuania", cc="LT", kind="remote_tower", status="planned", vendors=["Saab"], ansp="Oro Navigacija",
  dates=[("2025-04-04","Order reported")], facts=[F("Saab received an order from Oro Navigacija for a digital air traffic control tower at Vilnius, reported 4 April 2025; no operation date stated.", "vilnius")], conf="medium")
T(id="epmo", name="Warsaw Modlin Airport", icao="EPMO", country="Poland", cc="PL", kind="remote_tower", status="planned", vendors=["Saab"], ansp="PANSA",
  dates=[("2025-07-10","Saab Digital Tower selected")], facts=[F("PANSA selected Saab's Digital Tower Suite with an operations centre at PANSA premises in Warsaw; first Polish airport run from a digital tower.", "modlin")], conf="high")
T(id="lrbv", name="Brașov-Ghimbav International Airport", icao="LRBV", country="Romania", cc="RO", kind="remote_tower", status="operational", vendors=["Saab"], ansp="Brașov airport",
  dates=[("2023-06-15","Flights began under remote air traffic control")],
  facts=[F("Wikipedia, citing Romanian press, says flights began on 15 June 2023 with a fully remote tower.", "wiki"), F("Saab received the order for a digital tower in Romania in 2022.", "saab_ro")], conf="medium")
T(id="lrar", name="Arad International Airport", icao="LRAR", country="Romania", cc="RO", kind="remote_tower", status="unverified", vendors=["Saab"], ansp="",
  controlled_from="lrbv", facts=[F("Wikipedia lists Arad as a remote operating site about 400 km from Brașov-Ghimbav.", "wiki")], conf="low", note="Single secondary source; not independently confirmed.")

# ---------------- SOUTHERN EUROPE ----------------
T(id="levx", name="Vigo Airport", icao="LEVX", country="Spain", cc="ES", kind="remote_tower", status="operational", vendors=["Searidge", "FerroNATS"], ansp="Aena",
  dates=[("2020-11","Aena selects Searidge and FerroNATS"),("2025-06","Operations planned to launch"),("2025-12-10","Reported operational; early operations in low-traffic hours with a conventional controller on standby")],
  facts=[F("Searidge reports Spain's first regulator-certified digital control tower operating at Vigo, with the operations centre in a separate building next to the airport.", "vigo"),
         F("CAPA reported in March 2025 that operations were due to launch in June 2025.", "vigo_cap")], conf="high")
T(id="lemh", name="Menorca Airport", icao="LEMH", country="Spain", cc="ES", kind="remote_tower", status="unverified", vendors=["Kongsberg"], ansp="Aena",
  facts=[F("Kongsberg was selected to supply its remote tower system for Menorca, with delivery stated as 2021; the remote location is not stated.", "menorca")], conf="low", note="No go-live notice found.")
T(id="lfbo-rtc", name="DSNA Remote Tower Centre Toulouse", icao="LFBO", country="France", cc="FR", kind="rtc", status="planned", vendors=["Frequentis"], ansp="DSNA",
  dates=[("2022-06","DSNA selects Frequentis smartVISION")], facts=[F("The centre at Toulouse-Blagnac was planned to later handle four more airport towers.", "tours")], conf="medium", note="Operational status not confirmed.")
T(id="lfot", name="Tours Val de Loire Airport", icao="LFOT", country="France", cc="FR", kind="remote_tower", status="unverified", vendors=["Frequentis"], ansp="DSNA", controlled_from="lfbo-rtc",
  dates=[("2022-06","Selected; first tower due to go live end of 2023")],
  facts=[F("Frequentis supplies the system; Tours is more than 500 km from Toulouse and was due to go live at the end of 2023.", "tours"),
         F("French press in December 2022 said the remote tower was planned for installation in 2024.", "tours_fr")], conf="low", note="Schedules conflict; no go-live notice found.")
T(id="libr", name="Brindisi Airport", icao="LIBR", country="Italy", cc="IT", kind="remote_tower", status="operational", vendors=[], ansp="ENAV",
  dates=[("2022-06-13","Inaugurated")], facts=[F("ENAV inaugurated Italy's first remotely managed control tower on 13 June 2022.", "enav")], conf="high", note="The hardware vendor is not named in the ENAV release.")
T(id="lsgg", name="Geneva Airport", icao="LSGG", country="Switzerland", cc="CH", kind="remote_tower", status="planned", vendors=[], ansp="skyguide",
  dates=[("2022-09-21","Reported plan to replace the 1980s tower")], facts=[F("Skyguide plans to replace the tower with a remote tower, initially on site.", "geneva")], conf="low", note="Plan reported in 2022; current status not confirmed.")

# ---------------- AMERICAS ----------------
T(id="cygk", name="Kingston Airport (Ontario)", icao="CYGK", country="Canada", cc="CA", kind="digital_tower", status="planned", vendors=["Kongsberg"], ansp="NAV CANADA", program="daats",
  dates=[("2024-06-24","Kongsberg Geospatial framework contract announced")],
  facts=[F("Kingston is the first digital facility in NAV CANADA's DAATS programme; a Kingston hub serving other communities could follow in four to six years.", "daats")], conf="high")
T(id="sbsc", name="Santa Cruz Air Base", icao="SBSC", country="Brazil", cc="BR", kind="remote_tower", status="operational", vendors=["Frequentis"], ansp="DECEA",
  dates=[("2019-10-18","smartVISION system installed")], facts=[F("Frequentis and DECEA installed the first remote tower in South America at the Santa Cruz air base in October 2019.", "brazil")], conf="medium",
  note="Ongoing operation since 2019 not re-verified.")
T(id="kjyo", name="Leesburg Executive Airport", icao="KJYO", country="United States", cc="US", kind="remote_tower", status="decommissioned", vendors=["Saab"], ansp="FAA (non-federal)", program="faa-rts",
  dates=[("2015-06","Test in summer 2015"),("2018","Remote tower air traffic services began"),("2023-06","FAA discontinued the remote tower program")],
  facts=[F("The town says air traffic control has been provided since 2018 through the FAA remote tower program (nearly 80,000 operations a year) and that the FAA discontinued the program in June 2023.", "jyo_town"),
         F("A temporary tower is in place; the permanent tower is estimated to finish in spring 2029.", "jyo_town"),
         F("Saab stopped being the provider after the FAA changed certification standards.", "reason23")], conf="high")
T(id="kfnl", name="Northern Colorado Regional Airport", icao="KFNL", country="United States", cc="US", kind="remote_tower", status="decommissioned", vendors=["Searidge"], ansp="FAA / Colorado DOT", program="faa-rts",
  dates=[("2015-10-01","Selected as FAA test site"),("2023","FAA terminated the project after the vendor left")],
  facts=[F("Colorado DOT says the FAA terminated the Loveland project in late 2023 after the vendor opted not to continue; the project began in 2013.", "cdot"),
         F("A mobile tower with contract controllers operates at the airport; the airport commission kept a digital tower option open in 2023.", "bizwest")], conf="high")
T(id="kbow", name="Bartow Executive Airport (Digital Tower Operations Center)", icao="KBOW", country="United States", cc="US", kind="remote_tower", status="trial", vendors=["Frequentis"], ansp="FDOT / airport", program="faa-rts",
  controlled_from="", dates=[("2025","Frequentis installation (project March 2023 to November 2025)"),("2026-01","Active control testing planned"),("2026-07","Full services targeted")],
  facts=[F("Installed at Bartow; active control testing was slated for January 2026 and full air traffic control services were targeted for July 2026.", "bow_ai"),
         F("Frequentis reports its X10 voice system went live there; the CANSO story is dated 12 March 2026.", "bow_x10")], conf="high",
  note="The FAA states that no remote tower system was approved for the NAS as of its February 2025 page. See the United States program page for the September 2026 design approval.")
T(id="kgif", name="Winter Haven Regional Airport", icao="KGIF", country="United States", cc="US", kind="remote_tower", status="planned", vendors=["Frequentis"], ansp="FDOT / airport", controlled_from="kbow", program="faa-rts",
  dates=[("2026-07","Control testing for Winter Haven scheduled to begin")],
  facts=[F("Winter Haven is intended to be operated from the Bartow centre; Florida DOT is funding the system and officials hoped for approval in 2026.", "ain_wh"), F("Control testing for Winter Haven was scheduled to begin in July 2026.", "bow_ai")], conf="medium")
T(id="kacy", name="FAA William J. Hughes Technical Center (Atlantic City)", icao="KACY", country="United States", cc="US", kind="test_site", status="trial", vendors=["Frequentis"], ansp="FAA", program="faa-rts",
  facts=[F("The FAA evaluates remote tower systems at the Technical Center and selected RTX-Frequentis for system design approval evaluation and operational testing.", "ain_wh"), F("The FAA states that manufacturers submit designs which it evaluates at the Technical Center.", "faa_rts")], conf="high")
T(id="kjnx", name="Johnston Regional Airport", icao="KJNX", country="United States", cc="US", kind="remote_tower", status="planned", vendors=[], ansp="Airport authority", program="faa-rts",
  dates=[("2025-10-27","Local reporting on a digital tower plan")], facts=[F("The airport has FAA approval for a traditional tower but hopes the FAA approves digital towers; the director estimates a digital tower at about half the cost.", "wral")], conf="medium", note="No vendor named in the cited report.")

# ---------------- MIDDLE EAST, ASIA-PACIFIC ----------------
T(id="oeao", name="AlUla International Airport", icao="OEAO", country="Saudi Arabia", cc="SA", kind="remote_tower", status="operational", vendors=["Indra"], ansp="SANS",
  dates=[("2026-02-11","Reported operating fully remotely")], facts=[F("Indra and SANS say the airport operates fully remotely from a control centre about 550 km away in Jeddah, the first in the Middle East.", "alula")], conf="high")
T(id="ysws", name="Western Sydney International Airport", icao="YSWS", lat=-33.8844, lon=150.7340, country="Australia", cc="AU", kind="remote_tower", status="trial", vendors=["Frequentis"], ansp="Airservices Australia",
  dates=[("2024-03-05","Airservices announces the digital tower")],
  facts=[F("Over 20 cameras at the airport feed a Digital Aerodrome Service at Eastern Creek; CDC and Frequentis Australasia work with Airservices.", "wsi"),
         F("A July 2026 Frequentis article describes the digital work positions as in use.", "frq_munich")], conf="medium", note="Airport opening date and ATC go-live not confirmed here.")
T(id="vhhh", name="Hong Kong International Airport (digital tower and apron)", icao="VHHH", country="Hong Kong", cc="HK", kind="digital_tower", status="operational", vendors=["Searidge"], ansp="Airport Authority Hong Kong / CAD",
  dates=[("2022-06-22","Phase one passed acceptance testing")], facts=[F("Searidge reports a combined digital apron and tower platform with over 240 camera sensors; phase one passed acceptance and reliability testing in June 2022.", "hk")], conf="medium",
  note="A digital facility that augments the tower; not a remote tower.")
T(id="wsss", name="Singapore Changi Airport (smart digital tower prototype)", icao="WSSS", country="Singapore", cc="SG", kind="test_site", status="trial", vendors=["Searidge"], ansp="CAAS",
  facts=[F("NATS built a smart digital tower prototype for CAAS as a 22-month trial, with Searidge, ST Engineering and HungaroControl involved.", "changi")], conf="medium", note="Trial dates are not given in the source; later outcome not confirmed.")
T(id="nzaa", name="Auckland Airport (digital tower contingency)", icao="NZAA", country="New Zealand", cc="NZ", kind="contingency", status="unverified", vendors=["Frequentis"], ansp="Airways New Zealand",
  dates=[("2019-08-22","Frequentis announces the system")], facts=[F("Frequentis said its Digital Tower System would initially be used as a back-up contingency system.", "auckland")], conf="low")
