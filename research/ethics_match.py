"""Automated ethics list matching: Who Profits DB names + BDS guide text. Manual review is still required."""
import json, re, sys
wp = json.load(open("sources/whoprofits_companies.json"))
bds = open("sources/bds_guide.txt").read()
STOP = {"inc","corp","corporation","company","co","the","plc","ltd","limited","holdings","holding","group","sa","se","ag","nv","n.v.","common","stock","class","a","b","ordinary","shares","american","depositary","ads","incorporated","technologies","international","(the)","(de)","new"}
def key(name):
    w = [x for x in re.sub(r"[^a-z0-9& ]"," ",name.lower()).split() if x not in STOP]
    return " ".join(w[:2]) if w else ""
def core(name):
    w = [x for x in re.sub(r"[^a-z0-9& ]"," ",name.lower()).split() if x not in STOP]
    return w[0] if w else ""
def match(name):
    k, c = key(name), core(name)
    hits = []
    for _id,(n,url) in wp.items():
        nk = key(n)
        if k and (nk == k or (len(c) > 3 and nk.split()[:1] == [c])): hits.append(("whoprofits", n, url))
    if len(c) > 3 and re.search(r"\b"+re.escape(c)+r"\b", bds, re.I):
        ctx = re.search(r".{0,80}\b"+re.escape(c)+r"\b.{0,120}", bds, re.I|re.S).group(0).replace("\n"," ")
        hits.append(("bds", c, ctx))
    return hits
if __name__ == "__main__":
    for t in sys.argv[1:]:
        d = json.load(open(f"cache/{t}.json"))
        for h in match(d["name"]): print(t, "|", h[0], "|", h[1], "|", h[2][:200])
