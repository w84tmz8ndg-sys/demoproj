"""Render screen_results.md and portfolio.md from cached data."""
import json, os, glob, statistics, datetime, re
from notes import POS
U = json.load(open("universe.json")); E = json.load(open("ethics.json")) if os.path.exists("ethics.json") else {}
P = json.load(open("portfolio_config.json")) if os.path.exists("portfolio_config.json") else {"holdings": {}}
done = sorted({int(x) for x in open("batches_done.txt").read().split()}) if os.path.exists("batches_done.txt") else []
AUTO = json.load(open("auto_ethics.json")) if os.path.exists("auto_ethics.json") else {}
def num(x):
    if x in (None, "-", "n/a", ""): return None
    x = x.replace(",", "").replace("%", "")
    mult = {"T":1e12, "B":1e9, "M":1e6, "K":1e3}.get(x[-1], 1)
    try: return float(x.rstrip("TBMK")) * mult
    except ValueError: return None
def mc(v): return f"${v/1e12:.2f}T" if v >= 1e12 else f"${v/1e9:.0f}B" if v >= 1e9 else f"${v/1e6:.0f}M"
def shariah(c):
    m, z = c["musaffa"]["status"], c["zoya"]["status"]
    if m == "PASS" and z == "PASS": return "PASS", "Musaffa HALAL + Zoya compliant"
    if "FAIL" in (m, z) or "DOUBTFUL" in (m, z):
        return "FAIL", f"Musaffa {c['musaffa'].get('raw') or m}; Zoya {c['zoya'].get('label') or z}"
    return "UNVERIFIED", f"Musaffa {m}; Zoya {z}"
def quality(t):
    p = f"cache/fund_{t}.json"
    if not os.path.exists(p): return None
    d = json.load(open(p)); fy = d.get("fy") or []
    rev = [num(x) for x in (d.get("rev_hist") or [])]; ni = [num(x) for x in (d.get("ni_hist") or [])]
    # annual columns: index 1.. are FY (most recent first); TTM at 0
    ann_r = [x for x in rev[1:] if x]; ann_n = ni[1:]
    cagr = (ann_r[0]/ann_r[-1])**(1/(len(ann_r)-1))-1 if len(ann_r) >= 3 and ann_r[-1] > 0 else None
    pe_h = [num(x) for x in (d.get("pe_hist") or [])[1:]]; pe_h = [x for x in pe_h if x and 0 < x < 150]
    med = statistics.median(pe_h) if len(pe_h) >= 3 else None
    fpe = num(d.get("Forward PE")); pe = num(d.get("PE Ratio"))
    ref = fpe or pe; val = "n/a"
    if ref and med:
        r = ref/med
        val = "LOW" if r < 0.85 else "FAIR" if r <= 1.15 else "HIGH"
        if ref > 40 and val != "HIGH": val += " vs own history, but HIGH in absolute terms"
    return {"d": d, "cagr": cagr, "ni": ann_n, "ni_trend": ("rising" if ann_n and len(ann_n)>=3 and ann_n[0] and ann_n[-1] and ann_n[0] > ann_n[-1] else "falling/volatile"),
            "med_pe": med, "fpe": fpe, "pe": pe, "val": val, "years": f"{fy[-1]}–{fy[1]}" if len(fy) > 2 else ""}
rows, passers = [], []
for b in done:
    for c0 in U[(b-1)*100:b*100]:
        t = c0["ticker"]; p = f"cache/{t}.json"
        if not os.path.exists(p): rows.append((b, t, c0["name"], "PENDING", "not fetched")); continue
        c = json.load(open(p)); s, sr = shariah(c)
        if s != "PASS": rows.append((b, t, c0["name"], "FAIL" if s=="FAIL" else "UNVERIFIED", f"Shariah: {sr}")); continue
        e = E.get(t)
        if e and e["verdict"] == "EXCLUDE":
            f = e["findings"]; why = "; ".join(sorted({f"({x['label']}) {x['category']}" for x in f}))
            rows.append((b, t, c0["name"], "FAIL", f"Ethics: {why}"))
        elif e and e["verdict"] == "PASS":
            fl = " — open (c) flags" if e["findings"] else ""
            rows.append((b, t, c0["name"], "PASS", f"Shariah pass; ethics manual review pass{fl}")); passers.append((c0, c, e))
        else:
            a = AUTO.get(t)
            if a and a.get("hits"): rows.append((b, t, c0["name"], "FAIL", "Ethics (auto list match, " + "; ".join(a["hits"]) + ")"))
            else: rows.append((b, t, c0["name"], "PENDING-ETHICS", "Shariah pass; no list match; manual ethics review not yet done — not portfolio-eligible"))
now = datetime.date.today().isoformat()
L = [f"# Screen results\n", f"_Last updated {now}. Universe: {len(U)} US-listed common stocks and ADRs (ETFs, funds, warrants, units, rights, preferreds excluded), sorted by market cap, largest first, in batches of 100. Batches completed: {', '.join(map(str,done)) or 'none'} of {-(-len(U)//100)}._\n",
     "_Research for the user's own review — not financial advice._\n",
     "## Method\n",
     "- **Layer 1 — Shariah:** status read from each company's public Musaffa page (`musaffa.com/stock/<T>`) and Zoya page (`zoya.finance/stocks/<t>`) on the fetch date. PASS only if Musaffa = HALAL **and** Zoya = Shariah-compliant. Doubtful/questionable on either = FAIL. Not covered/unreadable = UNVERIFIED (never in the portfolio). Re-check both before acting; ratings change quarterly.",
     "- **Layer 2 — Human rights/ethics:** (1) AFSC Investigate company database (all 252 entries, matched on ticker); (2) Who Profits company database (470 entries, matched on name); (3) BDS movement boycott/divestment target guide; (4) targeted web searches for defense contracts, military-grade product lines, surveillance and forced labour. Labels: **(a) documented**, **(b) campaign-targeted** → exclude; **(c) alleged** → flag only. ESG ratings/funds not used.",
     "- **Defense line used:** a company is excluded for defense if it has a documented direct contract with, or a dedicated product line/offering for, a defense ministry or military (e.g. MIL-PRF/QML-qualified parts, a named DoD contract). Generic commercial products that militaries may also buy are not by themselves exclusionary.",
     "- **PENDING-ETHICS:** passed Shariah and had no automated list match, but no manual web review yet. Not portfolio-eligible until reviewed.\n",
     "## Summary table\n", "| Batch | Ticker | Company | Result | Reason |", "|---|---|---|---|---|"]
for b, t, n, r, why in rows: L.append(f"| {b} | {t} | {n[:45]} | **{r}** | {why} |")
from collections import Counter
cnt = Counter(r[3] for r in rows); L.append(f"\n**Totals:** " + ", ".join(f"{k}: {v}" for k, v in sorted(cnt.items())) + "\n")
L.append("## Excluded on ethics — evidence\n")
for b, t, n, r, why in rows:
    e = E.get(t)
    if r == "FAIL" and e and e["verdict"] == "EXCLUDE":
        L.append(f"**{t} — {n[:50]}**")
        for f in e["findings"]: L.append(f"- ({f['label']}) {f['category']}: {f['text']} Sources: " + ", ".join(f"<{s}>" for s in f["sources"]))
        L.append("")
L.append("## Companies that pass both layers — detail\n")
for c0, c, e in passers:
    t = c0["ticker"]; q = quality(t)
    L.append(f"### {c0['name'].replace(' Common Stock','')} ({t})")
    L.append(f"- **Sector:** {c0['sector']} / {c0['industry']} · **Market cap:** ~{mc(c0['mcap'])}")
    L.append(f"- **Why it passes:** Musaffa {c['musaffa']['raw']} (as of {c['musaffa']['asof']}, <{c['musaffa']['url']}>); Zoya {c['zoya']['label']} (as of {c['zoya']['asof']}, <{c['zoya']['url']}>). Ethics: {e.get('note','')} Sources checked: AFSC Investigate, Who Profits, BDS guide.")
    if q:
        d = q["d"]
        L.append(f"- **Business quality** ({q['years']}, from {d['src_fin']}): revenue CAGR {q['cagr']*100:.1f}%/yr; net income {q['ni_trend']}; operating margin {d['Operating Margin']}, net margin {d['Profit Margin']}; debt/equity {d['Debt / Equity']}, net cash {d['Net Cash']} (negative = net debt); ROIC {d['Return on Invested Capital (ROIC)']}." if q["cagr"] is not None else f"- **Business quality:** operating margin {d['Operating Margin']}, net margin {d['Profit Margin']}, D/E {d['Debt / Equity']}, net cash {d['Net Cash']}.")
        L.append(f"- **Competitive position:** {POS.get(t,'Not yet assessed.')}")
        L.append(f"- **Valuation:** trailing P/E {d['PE Ratio']}, forward P/E {d['Forward PE']}, 5-yr median fiscal-year P/E {q['med_pe']:.1f} → **{q['val']}**. Assumption: forward P/E ÷ own 5-yr median P/E < 0.85 = low, 0.85–1.15 = fair, > 1.15 = high; consensus forward EPS from stockanalysis.com ({d['src_stats']})." if q["med_pe"] else f"- **Valuation:** trailing P/E {d['PE Ratio']}, forward P/E {d['Forward PE']}; insufficient P/E history for comparison.")
    fl = [f for f in e["findings"]]
    L.append("- **Open flags (c) / risks:** " + ("; ".join(f"({f['label']}) {f['text']}" + (" Sources: " + ", ".join(f"<{s}>" for s in f["sources"]) if f["sources"] else " (no specific source located)") for f in fl) if fl else "No (c) flags found.") + "\n")
extra = []
for b in range(max(done)+1, -(-len(U)//100)+1):
    got = [c0 for c0 in U[(b-1)*100:b*100] if os.path.exists(f"cache/{c0['ticker']}.json")]
    if not got: continue
    for c0 in got:
        c = json.load(open(f"cache/{c0['ticker']}.json")); s2, sr = shariah(c)
        a = AUTO.get(c0["ticker"], {})
        if s2 == "PASS":
            r2 = ("FAIL", "Ethics (auto list match: " + "; ".join(a["hits"]) + ")") if a.get("hits") else ("PENDING-ETHICS", "Shariah pass; no list match; manual ethics review not done")
        else: r2 = ("FAIL" if s2 == "FAIL" else "UNVERIFIED", f"Shariah: {sr}")
        extra.append((b, c0["ticker"], c0["name"], r2[0], r2[1]))
if extra:
    L.append(f"## Shariah-only results for batches not yet ethics-reviewed (batches {extra[0][0]}–{extra[-1][0]})\n")
    L.append("_These were fetched automatically. Companies marked PENDING-ETHICS passed both Shariah screeners, but their ethics review is limited to the automated list checks. None of them is eligible for the portfolio._\n")
    L.append("| Batch | Ticker | Company | Result | Reason |"); L.append("|---|---|---|---|---|")
    for b, t, n, r, why in extra: L.append(f"| {b} | {t} | {n[:45]} | **{r}** | {why} |")
    ec = Counter(x[3] for x in extra); L.append("\n**Totals (Shariah-only batches):** " + ", ".join(f"{k}: {v}" for k, v in sorted(ec.items())) + "\n")
open("screen_results.md", "w").write("\n".join(L))
# ---- portfolio ----
H = P["holdings"]; tot = sum(H.values())
pm = [f"# Running portfolio\n", f"_Last updated {now} after batch(es) {', '.join(map(str,done))}. Built only from companies that passed **both** layers and had a manual ethics review. Individual stocks only. Research for review — not financial advice; the user is not relying on it as such._\n",
      "| # | Ticker | Company | Sector | Mkt cap | Weight | Valuation view | Why included |", "|---|---|---|---|---|---|---|---|"]
uidx = {u["ticker"]: u for u in U}; sect = Counter()
for i, (t, w) in enumerate(sorted(H.items(), key=lambda x: -x[1]), 1):
    u = uidx[t]; q = quality(t); sect[P.get("sector_map", {}).get(t, u["sector"])] += w
    pm.append(f"| {i} | {t} | {u['name'].replace(' Common Stock','')[:35]} | {P.get('sector_map',{}).get(t,u['sector'])} | ~{mc(u['mcap'])} | {w:.1f}% | {q['val'] if q else 'n/a'} | {P.get('why',{}).get(t,'')} |")
pm.append(f"\n**Total:** {tot:.1f}%\n\n## Sector mix\n")
for s, w in sect.most_common(): pm.append(f"- {s}: {w:.1f}%")
pm.append("\n" + P.get("commentary", ""))
open("portfolio.md", "w").write("\n".join(pm))
print("rows", len(rows), dict(cnt), "passers", len(passers))
