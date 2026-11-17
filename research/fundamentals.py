"""Fetch fundamentals from stockanalysis.com (statistics, ratios, financials) -> cache/fund_<T>.json"""
import re, html, json, sys, os, urllib.request
from concurrent.futures import ThreadPoolExecutor
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
def text(url):
    try:
        s = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=40).read().decode("utf-8","replace")
    except Exception as e: return ""
    s = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', s, flags=re.S)
    t = html.unescape(re.sub(r'<[^>]+>', '|', s))
    return re.sub(r'\s*\|[\s|]*', '|', t)
NUM = r'(?:-?[\d.,]+[%BMTK]?|n/a|-)'
def kv(t, k):
    m = re.search(r'\|' + re.escape(k) + r'\|(' + NUM + r')\|', t); return m.group(1) if m else None
def row(t, k, n=6, pct=None):
    for m in re.finditer(r'\|' + re.escape(k) + r'\|(?:[A-Za-z][A-Za-z ()/&-]*\|)?((?:' + NUM + r'\|){2,})', t):
        v = m.group(1).strip('|').split('|')[:n]
        if pct is None or (pct == any('%' in x for x in v)): return v
    return None
def base(tk):
    return f"https://stockanalysis.com/stocks/{tk.lower().replace('.','-')}"
def fetch(tk):
    p = f"cache/fund_{tk}.json"
    if os.path.exists(p): return json.load(open(p))
    st = text(base(tk) + "/statistics/")
    if not st or "PE Ratio" not in st:   # ADRs/foreign listings live under /quote/ on some pages
        st = text(base(tk) + "/statistics/")
    d = {"ticker": tk, "src_stats": base(tk)+"/statistics/", "src_fin": base(tk)+"/financials/", "src_ratios": base(tk)+"/financials/ratios/"}
    for k in ["Market Cap","Enterprise Value","PE Ratio","Forward PE","PS Ratio","EV / EBITDA","Gross Margin","Operating Margin","Profit Margin","FCF Margin",
              "Debt / Equity","Debt / EBITDA","Net Cash","Total Debt","Cash & Cash Equivalents","Return on Invested Capital (ROIC)","Return on Equity (ROE)","Revenue","Net Income","Free Cash Flow","Dividend Yield","Beta (5Y)"]:
        d[k] = kv(st, k)
    fin = text(base(tk) + "/financials/")
    m = re.search(r"\|Fiscal Year\|((?:(?:TTM|FY \d{4})\|){2,})", fin); d["fy"] = m.group(1).strip("|").split("|")[:6] if m else None; d["rev_hist"] = row(fin, "Revenue", pct=False); d["rev_growth"] = row(fin, "Revenue Growth", pct=True)
    d["ni_hist"] = row(fin, "Net Income", pct=False); d["eps_growth"] = row(fin, "EPS Growth", pct=True)
    rat = text(base(tk) + "/financials/ratios/")
    m = re.search(r"\|Fiscal Year\|((?:(?:Current|TTM|FY \d{4})\|){2,})", rat); d["ratio_fy"] = m.group(1).strip("|").split("|")[:6] if m else None; d["pe_hist"] = row(rat, "PE Ratio", 6)
    json.dump(d, open(p, "w"), indent=1); return d
if __name__ == "__main__":
    with ThreadPoolExecutor(4) as ex: res = list(ex.map(fetch, sys.argv[1:]))
    for d in res: print(d["ticker"], d["PE Ratio"], d["Forward PE"], d["Profit Margin"], d["Debt / Equity"], d["rev_growth"][:3] if d["rev_growth"] else None, d["pe_hist"])
