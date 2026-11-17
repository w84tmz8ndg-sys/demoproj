"""Automated ethics list screen for Shariah double-passers without a manual review. Output: auto_ethics.json"""
import json, re, os, glob
U = json.load(open("universe.json")); E = json.load(open("ethics.json"))
afsc = json.load(open("sources/afsc_companies.json")); wp = json.load(open("sources/whoprofits_companies.json"))
bds = open("sources/bds_guide.txt").read()
STOP = set("inc corp corporation company co the plc ltd limited holdings holding group sa se ag nv common stock class a b c ordinary shares share american depositary ads adr incorporated international new de llc lp sponsored each representing one".split())
def words(n): return [w for w in re.sub(r"[^a-z0-9 ]", " ", n.lower()).split() if w not in STOP]
wpk = {}
for _id, (n, url) in wp.items():
    w = words(re.sub(r"[֐-׿\"]+", " ", re.sub(r"\(.*?\)", " ", n)))
    if w: wpk.setdefault(" ".join(w[:2]), []).append((n.strip(), url))
afsc_t = {t: v for v in afsc.values() for t in v["tickers"]}
DEF_IND = re.compile(r"military|ordnance|aerospace|defense|guided missile|tanks", re.I)
STATIC = {  # (label, reason, source)
 "GEO": ("a", "Private prison operator", "https://www.geogroup.com/"),
 "CXW": ("a", "Private prison operator (CoreCivic)", "https://www.corecivic.com/"),
 "AXON": ("a", "Surveillance/weapons tech (Tasers, body cameras, police surveillance) sold to state security", "https://investor.axon.com/"),
}
out = {}
for c0 in U:
    t = c0["ticker"]; p = f"cache/{t}.json"
    if t in E or not os.path.exists(p): continue
    c = json.load(open(p))
    if not (c["musaffa"]["status"] == "PASS" and c["zoya"]["status"] == "PASS"): continue
    hits, src = [], []
    if t in afsc_t: hits.append(f"(a) AFSC Investigate: {', '.join(afsc_t[t]['tags']) or 'listed'}"); src.append(afsc_t[t]["url"])
    w = words(c0["name"]); k = " ".join(w[:2])
    if k in wpk and len(k) > 3: hits.append(f"(a) Who Profits: {wpk[k][0][0]}"); src.append(wpk[k][0][1])
    if w and len(w[0]) > 4 and w[0] not in {"global","american","united","first","national","general","energy","health","capital","digital","pacific","world"}:
        nm = " ".join(w[:2]) if len(w) > 1 else w[0]
        if re.search(r"\b" + re.escape(nm) + r"\b", bds, re.I): hits.append(f"(b) BDS guide mentions '{nm}'"); src.append("https://bdsmovement.net/Guide-to-BDS-Boycott")
    if DEF_IND.search(c0["industry"]): hits.append(f"(a?) defense-related industry classification '{c0['industry']}' — verify")
    if t in STATIC: l, r, s = STATIC[t]; hits.append(f"({l}) {r}"); src.append(s)
    out[t] = {"hits": hits, "sources": src}
json.dump(out, open("auto_ethics.json", "w"), indent=1)
print(len(out), "double-passers auto-screened;", sum(1 for v in out.values() if v["hits"]), "with hits")
for t, v in out.items():
    if v["hits"]: print(t, v["hits"])
