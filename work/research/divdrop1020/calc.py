# 코스피가 하루 3% 넘게 빠진 날, 고배당 ETF는 얼마나 빠졌나 (네이버 fchart 일봉 종가)
import re, pathlib, statistics as st
R = pathlib.Path(__file__).parent / "raw"
CODES = {"KOSPI": "코스피", "069500": "KODEX 200", "161510": "PLUS 고배당주",
         "279530": "KODEX 고배당주", "104530": "KIWOOM 코리아고배당", "211560": "TIGER 배당성장"}

def load(c):
    t = (R / f"{c}.xml").read_bytes().decode("euc-kr", "ignore")
    out = {}
    for d, o, h, l, cl, v in re.findall(r'data="(\d+)\|([\d.]+)\|([\d.]+)\|([\d.]+)\|([\d.]+)\|(\d+)"', t):
        out[d] = float(cl)
    return out

px = {c: load(c) for c in CODES}
days = sorted(px["KOSPI"])
print("기간", days[0], "~", days[-1], len(days), "거래일")
rows = []
for i in range(1, len(days)):
    d, p = days[i], days[i - 1]
    k = px["KOSPI"][d] / px["KOSPI"][p] - 1
    if k <= -0.03:
        r = {"d": d, "KOSPI": k}
        for c in CODES:
            if c == "KOSPI": continue
            a, b = px[c].get(d), px[c].get(p)
            r[c] = (a / b - 1) if a and b else None
        rows.append(r)
print("코스피 -3% 이하인 날", len(rows))
hdr = ["날짜"] + list(CODES.values())
print(" | ".join(hdr))
for r in rows:
    print(r["d"], " | ".join(f"{r[c]*100:+.2f}%" if r[c] is not None else "-" for c in CODES))
print("--- 평균 / 가운데 / KODEX 200보다 덜 빠진 날")
for c in CODES:
    v = [r[c] for r in rows if r[c] is not None]
    less = sum(1 for r in rows if r[c] is not None and r[c] > r["069500"]) if c not in ("KOSPI", "069500") else "-"
    print(CODES[c], f"평균 {st.mean(v)*100:+.2f}% 가운데 {st.median(v)*100:+.2f}%", f"덜빠짐 {less}/{len(v)}")
# 같은 기간 전체 수익(가격만)
print("--- 기간 전체 가격 변화(분배금 뺌)")
for c in CODES:
    ds = sorted(px[c]); print(CODES[c], ds[0], f"{(px[c][ds[-1]]/px[c][ds[0]]-1)*100:+.1f}%")

# 오른 날(코스피 +3% 이상)
up = []
for i in range(1, len(days)):
    d, p = days[i], days[i - 1]
    k = px["KOSPI"][d] / px["KOSPI"][p] - 1
    if k >= 0.03:
        up.append({c: (px[c][d] / px[c][p] - 1) if px[c].get(d) and px[c].get(p) else None for c in CODES})
print("--- 코스피 +3% 이상인 날", len(up))
for c in CODES:
    v = [r[c] for r in up if r[c] is not None]
    print(CODES[c], f"평균 {st.mean(v)*100:+.2f}% 가운데 {st.median(v)*100:+.2f}%")

# 분배금(야후 events=div, 배당락일 기준) 더한 총수익 — 재투자 안 함, 단순 합
import json, datetime
print("--- 분배금 더한 기간 수익(재투자 없이 단순 합, 세전)")
for c in ("069500", "161510", "279530"):
    y = json.load(open(R / f"y_{c}.json"))["chart"]["result"][0]
    dv = y.get("events", {}).get("dividends", {})
    s, e = days[0], days[-1]
    tot = sum(v["amount"] for k, v in dv.items()
              if s < datetime.datetime.fromtimestamp(int(k), datetime.UTC).strftime("%Y%m%d") <= e)
    p0, p1 = px[c][s], px[c][e]
    print(CODES[c], f"시작 {p0:,.0f} 끝 {p1:,.0f} 분배금 합 {tot:,.0f}원",
          f"가격 {(p1/p0-1)*100:+.1f}% 분배금 {tot/p0*100:+.1f}%p 합 {((p1+tot)/p0-1)*100:+.1f}%",
          f"1천만원이면 {1e7*(p1+tot)/p0:,.0f}원")

# 그림용 결과
res = {"ndrop": len(rows), "nup": len(up),
       "drop": {c: st.mean([r[c] for r in rows if r[c] is not None]) for c in CODES},
       "upm": {c: st.mean([r[c] for r in up if r[c] is not None]) for c in CODES},
       "today": rows[-1] if rows and rows[-1]["d"] == days[-1] else None, "tot": {}}
for c in ("069500", "161510", "279530"):
    y = json.load(open(R / f"y_{c}.json"))["chart"]["result"][0]
    dv = y.get("events", {}).get("dividends", {})
    s, e = days[0], days[-1]
    tot = sum(v["amount"] for k, v in dv.items()
              if s < datetime.datetime.fromtimestamp(int(k), datetime.UTC).strftime("%Y%m%d") <= e)
    res["tot"][c] = 1e7 * (px[c][e] + tot) / px[c][s]
json.dump(res, open(pathlib.Path(__file__).parent / "results.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
