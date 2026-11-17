from ethics_lib import *
b = Batch(14)
b.ex("BB","a","Military software to defense ministries","Pentagon Force Protection Agency AtHoc contract; BlackBerry UEM on DoDIN Approved Products List and DISA STIG-approved; US Air Force selected BlackBerry Spark.", "https://mobilesyrup.com/2016/06/06/blackberry-signs-new-1-year-secure-alert-systems-contract-with-pentagon/","https://www.executivegov.com/articles/usaf-selects-blackberry-spark-to-support-uem-and-ues-john-chen-quoted")
b.ex("ENS","a","Defense supply chain","Precision Power Solutions segment supplies military vehicles, soldier power, munitions and defense programs; management calls EnerSys 'the largest supplier to the U.S. military' (batteries).", "https://s206.q4cdn.com/482396552/files/doc_news/EnerSys-Announces-Segment-Realignment-2026.pdf","https://www.fool.com/earnings/call-transcripts/2026/05/21/enersys-ens-q4-2026-earnings-transcript/")
b.ex("DOX","b","Campaign-targeted","The Palestinian BDS National Committee campaigned against Amdocs (urging Telkom South Africa not to contract with it). No documented occupation/military contract found.", "https://bdsmovement.net/ar/node/11452")
b.ok("LSTR", flags=[("Defense freight demand","Q2 2026 call cites aerospace and defense among drivers of heavy-haul freight; no DoD contract found. Flagged.",["https://www.marketbeat.com/instant-alerts/landstar-system-q2-earnings-call-highlights-2026-07-28/"])])
b.oks("LPX ALGM INSW WFG MMSI TREX SNDR LQDA PI SKY SXT CVCO WHD SITE TVTX MXL GOLF RELY LAUR RXO SYNA BLLN")
b.save()
