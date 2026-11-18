from ethics_lib import *
b = Batch(21); b.oks("ETON GRC CRCT AMR TILE LMAT CERT GIC BLBD INSP DFIN", LIGHT_NOTE); b.save()
b = Batch(22)
b.ok("OMCL", flags=[("Possible military health sales","Pharmacy-automation vendor whose customers likely include military hospitals; not researched. Verify.",[])])
b.oks("INVX AEHR ALG ADEA NRP PRLB WGS HUBG HLIO PDFS", LIGHT_NOTE); b.save()
b = Batch(23)
b.ok("LQDT", flags=[("DoD surplus-sales contracts","Historically ran surplus-property sales for the Defense Logistics Agency; current status not researched. Verify.",[])])
b.oks("XPRO PRCT SHLS PLPC ARLO INNV STAA RVLV", LIGHT_NOTE); b.save()
