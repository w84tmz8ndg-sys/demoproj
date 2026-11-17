"""Fetch Musaffa + Zoya Shariah status and SEC SIC code for a batch of 100 tickers. Results cached in cache/<TICKER>.json."""
import json, re, sys, os, time, html, datetime, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
def get(url, ua=UA, tries=3):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": ua})
            with urllib.request.urlopen(req, timeout=40) as r: return r.status, r.read().decode("utf-8","replace")
        except urllib.error.HTTPError as e:
            if e.code == 404: return 404, ""
            if e.code in (429,500,502,503) and i < tries-1: time.sleep(5*(i+1)); continue
            return e.code, ""
        except Exception as e:
            if i < tries-1: time.sleep(3*(i+1)); continue
            return 0, str(e)
def musaffa(t):
    url = f"https://musaffa.com/stock/{t.replace('.','-')}/"
    code, body = get(url)
    m = re.search(r'is classified as (NOT HALAL|HALAL|DOUBTFUL|NOT COVERED|[A-Z ]+?) by Musaffa', body)
    asof = re.search(r'As of ([A-Za-z]+ \d{4})', body)
    st = {"HALAL":"PASS","NOT HALAL":"FAIL","DOUBTFUL":"DOUBTFUL"}.get(m.group(1), m.group(1)) if m else ("NOT LISTED" if code==404 else "UNVERIFIED")
    return {"status": st, "raw": m.group(1) if m else None, "asof": asof.group(1) if asof else None, "url": url, "http": code}
def zoya(t):
    url = f"https://zoya.finance/stocks/{t.lower().replace('.','-')}"
    code, body = get(url)
    h = re.search(r'stock is&nbsp;<a[^>]*>([^<]+)</a>', body)
    faq = re.search(r'"text": "(As of [^"]*?\((?:[^)]*)\) is [^"]*)"', body) or re.search(r'content="((?:Yes\. |No\. )?As of [^"]*)" name="description"', body)
    raw = html.unescape(faq.group(1)) if faq else None
    label = html.unescape(h.group(1)).strip() if h else None
    st = "NOT LISTED" if code == 404 else "UNVERIFIED"
    probe = (label or raw or "").lower()
    if probe:
        if re.search(r"not shariah-compliant|non-compliant|not halal", probe): st = "FAIL"
        elif re.search(r"questionable|doubtful|cannot yet confirm|under review", probe): st = "DOUBTFUL"
        elif re.search(r"shariah-compliant", probe): st = "PASS"
    asof = re.search(r'As of ([A-Za-z]+ \d+, \d{4})', raw or "")
    return {"status": st, "label": label, "raw": raw, "asof": asof.group(1) if asof else None, "url": url, "http": code}
def sic(cik):
    if not cik: return None
    code, body = get(f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=10-K&dateb=&owner=include&count=1&output=atom", ua="ResearchScript contact@example.org")
    m = re.search(r'<assigned-sic>(\d+)</assigned-sic>.*?<assigned-sic-desc>([^<]*)', body, re.S)
    return {"code": m.group(1), "desc": html.unescape(m.group(2))} if m else None
def work(c):
    p = f"cache/{c['ticker']}.json"
    if os.path.exists(p) and not os.environ.get("REFRESH"):
        d = json.load(open(p))
        if d["musaffa"]["status"] not in ("UNVERIFIED",) and d["zoya"]["status"] not in ("UNVERIFIED",): return d
    d = dict(c); d["musaffa"] = musaffa(c["ticker"]); d["zoya"] = zoya(c["ticker"]); d["sic"] = None
    d["fetched"] = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    json.dump(d, open(p,"w"), indent=1); return d
if __name__ == "__main__":
    u = json.load(open("universe.json"))
    for b in [int(x) for x in sys.argv[1:]]:
        chunk = u[(b-1)*100:b*100]
        with ThreadPoolExecutor(4) as ex: res = list(ex.map(work, chunk))
        from collections import Counter
        print(f"batch {b}: musaffa {dict(Counter(r['musaffa']['status'] for r in res))} zoya {dict(Counter(r['zoya']['status'] for r in res))}", flush=True)
