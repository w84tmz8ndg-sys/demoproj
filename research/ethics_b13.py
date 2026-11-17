from ethics_lib import *
b = Batch(13)
b.ex("CVLT","a","Military software to defense ministries","DoD-wide ESI agreement for Commvault (N66001-25-A-0054, to 2029); Defense Health Agency and Air Force licence orders.", "https://static.carahsoft.com/concrete/files/1317/5328/8015/Carahsoft_ESI_Reference_External_Guide_-_Commvault.pdf","https://samsearch.co/gov-explore/federal/commvault-software/HT001525FE053")
b.ex("PEGA","a","Military software to defense ministries","US Army sole-source 10-year IDIQ for Pega software and services (up to $419M).", "https://www.govconwire.com/articles/pegasystems-419m-army-enterprise-software-contract")
b.ex("BOX","a","Military software to defense ministries","DISA DoD Impact Level 4 authorization; Defense Contract Management Agency selected Box (2020).", "https://businesswire.com/news/home/20170426005517/en/Box-Announces-Department-of-Defense-Level-4-Authorization-and-Launches-Box-KeySafe-for-Government","https://www.businesswire.com/news/home/20201216005374/en/Defense-Contract-Management-Agency-Selects-Box-for-Cloud-Content-Management/")
b.ex("NPO","a","Defense supply chain","Advanced Surface Technologies segment serves 'critical applications in the space, aerospace, and defense markets'; aerospace ~8% of sales (2025 annual report).", "https://s203.q4cdn.com/627297643/files/doc_financials/AR/EnPro_AnnualReport25_Final.pdf")
b.oks("CTVA CAI MIRM MIDD CRUS OLLI VAL POWL LFST BCPC BRZE")
b.save()
