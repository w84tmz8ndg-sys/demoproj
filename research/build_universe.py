"""Build the screening universe: US-listed common stocks, sorted by market cap (largest first)."""
import json, re
etf, test = set(), set()
for fn, symcol, etfcol, testcol in [("nasdaqlisted.txt",0,6,3),("otherlisted.txt",0,4,6)]:
    for line in open(fn).read().splitlines()[1:]:
        p = line.split("|")
        if len(p) < 7: continue
        if p[etfcol]=="Y": etf.add(p[symcol])
        if p[testcol]=="Y": test.add(p[symcol])
sec = {r[2]: (r[0], r[3]) for r in json.load(open("sec_tickers.json"))["data"]}  # ticker -> (cik, exch)
bad = re.compile(r"\b(warrants?|units?|rights?|preferred|pfd|notes? due|debentures?|depositary shares? represent(ing)? (a )?(1/|fraction)|perpetual|subordinated|trust preferred|fund|etf|etn|baby bond)\b", re.I)
rows = json.load(open("screener.json"))["data"]["rows"]
out = []
for r in rows:
    s = r["symbol"].strip()
    if s in etf or s in test or "^" in s or "/" in s: continue
    if bad.search(r["name"]): continue
    try: mc = float(r["marketCap"] or 0)
    except ValueError: mc = 0
    if mc <= 0: continue
    out.append({"ticker": s, "name": r["name"], "sector": r["sector"] or "n/a", "industry": r["industry"] or "n/a",
                "country": r["country"], "mcap": mc, "price": r["lastsale"], "cik": sec.get(s.replace(".","-"), (None,))[0]})
out.sort(key=lambda x: -x["mcap"])
json.dump(out, open("universe.json","w"), indent=0)
print(len(rows), "rows ->", len(out), "common stocks; batches:", -(-len(out)//100))
