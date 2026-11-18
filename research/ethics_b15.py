from ethics_lib import *
b = Batch(15)
b.ex("TENB","a","Military software to defense ministries","Tenable software underpins the DoD's Assured Compliance Assessment Solution (ACAS) run by DISA; Army ACAS licence support solicitation (2026).", "https://www.tenable.com/blog/tenable-selected-for-disa-s-acas-vulnerability-management-solution","https://www.highergov.com/contract-opportunity/dliflc-dcsit-tenable-annual-license-support-w911s026ra099-o-8c82e/")
b.ex("MTRN","a","Defense supply chain","Defense sales >$100M for two consecutive years; $65M investment from a defense prime to expand beryllium capacity; aluminium-beryllium castings for F-35 targeting optics (Lockheed Martin).", "https://quantisnow.com/insight/materion-corporation-reports-fourth-quarter-and-full-year-2025-results-provides-6388075","https://businesswire.com/news/home/20140610005135/en/Materion-Corporation-Announces-Supply-Contract-with-Lockheed-Martin-for-Proprietary-AlBeCast%C2%AE-Aluminum-Beryllium-Investment-Castings-for-F-35-Lightning-II-Airborne-Optical-Components")
b.ok("NOVT", flags=[("Possible defense exposure","A company profile lists defense/space manufacturing among capabilities; no defense contract found. Verify.",["https://ghost.bitscale.ai/novanta-inc/"])])
b.ok("EXPO", flags=[("Not fully researched","Engineering/scientific consultancy that may serve government clients; not researched in depth. Verify.",[])])
b.oks("BMI ADPT CSW CRVL HIMS RHI UFPI PAY IPAR FELE STVN ECG HCC MYRG MGNI HTFL UNF AAOI CNR")
b.save()
