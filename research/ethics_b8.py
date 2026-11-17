from ethics_lib import *
b = Batch(8)
b.ex("LOGI","a","Military supplier (Israel)","AFSC: the Israeli military uses Logitech gaming controllers to fly drones (Gaza).", AF+"logitech")
b.ex("COKE","b","Campaign-targeted brand","Largest US bottler of Coca-Cola products; the Coca-Cola brand is a BDS 'organic boycott target' and its Israeli licensee operates in a settlement (AFSC). COKE itself has no documented Israeli operations — excluded as (b) on the brand, conservatively.", BDS, AF+"coca-cola")
b.ex("DOCU","a","Military software to defense ministries","DISA granted DocuSign a DoD Impact Level 4 provisional authorization (2021), maintained since; onboarded to DoD's DISN.", "https://docusign.com/blog/docusign-achieves-dod-impact-level-4-provisional-authorization")
b.ex("DT","a","Military software to defense ministries","DoD Enterprise Software Initiative (ESI) agreement for Dynatrace via Carahsoft.", "https://static.carahsoft.com/concrete/files/6917/8351/7245/Carahsoft_ESI_Reference_External_Guide_-_Dynatrace.pdf")
b.ok("TRMB", flags=[("Possible defense/GPS sales","Trimble positioning products are used by government and possibly defense customers; no defense contract located in this search. Verify.",[])])
b.oks("BBIO MANH LECO BURL ICLR GKOS MTZ AVY EHC TOL BSY AHR NXT RPM SNN PEN RDY WSO")
b.save()
