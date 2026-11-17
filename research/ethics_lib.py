import json, os
WP = "https://www.whoprofits.org/companies/company/"; AF = "https://investigate.afsc.org/company/"; BDS = "https://bdsmovement.net/Guide-to-BDS-Boycott"
DEFAULT_NOTE = "No documented or campaign-targeted involvement found in AFSC Investigate, Who Profits, or the BDS target guide; targeted web search found none."
class Batch:
    def __init__(s, n): s.n, s.R = n, {}
    def ex(s, t, label, cat, text, *src): s.R.setdefault(t, {"verdict": "EXCLUDE", "findings": []})["findings"].append({"label": label, "category": cat, "text": text, "sources": list(src)})
    def ok(s, t, note=DEFAULT_NOTE, flags=()): s.R[t] = {"verdict": "PASS", "note": note, "findings": [{"label": "c", "category": c, "text": x, "sources": list(y)} for c, x, y in flags]}
    def oks(s, tickers, note=DEFAULT_NOTE):
        for t in tickers.split(): s.ok(t, note)
    def save(s):
        db = json.load(open("ethics.json")) if os.path.exists("ethics.json") else {}
        for t, v in s.R.items(): v["batch"] = s.n; v["review"] = "manual"; db[t] = v
        json.dump(db, open("ethics.json", "w"), indent=1)
        print(f"batch {s.n}: {len(s.R)} reviewed, {sum(v['verdict']=='PASS' for v in s.R.values())} pass")
