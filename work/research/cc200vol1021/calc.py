# KODEX 200타겟위클리커버드콜(498400) vs KODEX 200(069500): 큰 날 등락·누적 (네이버 fchart 일봉 종가 + 분배금)
# 분배금: 498400은 삼성자산운용 공식(raw/divid.json) 금액, 배당락일은 야후(raw/y*.json, 기준일 하루 전 영업일과 일치)
import re, json, pathlib, statistics as st, datetime as D, sys
sys.stdout.reconfigure(encoding='utf-8')
R = pathlib.Path(__file__).parent / "raw"
def load(c):
    t = (R / f"{c}.xml").read_bytes().decode("euc-kr", "ignore")
    return {d: float(cl) for d, o, h, l, cl, v in re.findall(r'data="(\d+)\|([\d.]+)\|([\d.]+)\|([\d.]+)\|([\d.]+)\|(\d+)"', t)}
def divs(c):
    r = json.load(open(R / f"y{c}.json"))['chart']['result'][0]
    out = {}
    for k, v in r.get('events', {}).get('dividends', {}).items():
        d = D.datetime.fromtimestamp(int(k), D.UTC).astimezone(D.timezone(D.timedelta(hours=9))).strftime('%Y%m%d')
        out[d] = v['amount']
    return out
CC, K = "498400", "069500"
px = {c: load(c) for c in (CC, K, "KOSPI")}
dv = {c: divs(c) for c in (CC, K)}
# 공식 금액 대조
off = {x['basicD']: float(x['dividA']) for x in json.load(open(R / 'divid.json', encoding='utf-8'))['dividList']}
print("공식 분배금 건수", len(off), "합", sum(off.values()), "야후 합", sum(v for d, v in dv[CC].items()))
days = sorted(d for d in px[CC] if d in px[K])
print("기간", days[0], "~", days[-1], len(days), "거래일")
def ret(c, d, p):
    return (px[c][d] + dv[c].get(d, 0)) / px[c][p] - 1
rows = []
for i in range(1, len(days)):
    d, p = days[i], days[i-1]
    rows.append((d, ret(K, d, p), ret(CC, d, p), d in dv[CC] or d in dv[K]))
for th in (0.03, 0.04):
    up = [r for r in rows if r[1] >= th]; dn = [r for r in rows if r[1] <= -th]
    for name, L in (("오른 날", up), ("내린 날", dn)):
        kk = st.mean(r[1] for r in L); cc = st.mean(r[2] for r in L)
        less = sum(1 for r in L if abs(r[2]) < abs(r[1]))
        print(f"KODEX200 ±{th*100:.0f}% {name} {len(L)}일 · KODEX200 평균 {kk*100:+.2f}% · 커버드콜 평균 {cc*100:+.2f}% · 비율 {cc/kk*100:.0f}% · 커버드콜이 덜 움직인 날 {less}/{len(L)} · 배당락 낀 날 {sum(r[3] for r in L)}")
print("--- ±4% 날 목록")
for r in rows:
    if abs(r[1]) >= 0.04: print(r[0], f"{r[1]*100:+.2f}%", f"{r[2]*100:+.2f}%", "배당락" if r[3] else "")
# 누적: 1천만원, 첫 거래일 종가에 사서 분배금은 현금으로 받음(재투자 안 함)
def grow(c, a, b, won=10_000_000):
    n = won / px[c][a]
    cash = sum(v for d, v in dv[c].items() if a < d <= b) * n
    return n * px[c][b], cash
for a, b, lab in ((days[0], days[-1], "상장 다음날~오늘"), ([d for d in days if d >= '20260102'][0], days[-1], "올해 첫 거래일~오늘"),
                  ([d for d in days if d >= '20251021'][0], days[-1], "1년 전~오늘")):
    for c, nm in ((K, "KODEX 200"), (CC, "커버드콜")):
        v, cash = grow(c, a, b)
        print(lab, a, b, nm, f"평가 {v:,.0f} 분배금 {cash:,.0f} 합 {v+cash:,.0f} ({(v+cash)/1e7*100-100:+.1f}%)")
# 최근 12개월 분배금
last12 = [(d, v) for d, v in off.items() if d > '20251015']
print("최근 12회 분배금 합", sum(v for d, v in last12), len(last12), "오늘 종가", px[CC][days[-1]], f"{sum(v for d,v in last12)/px[CC][days[-1]]*100:.2f}%")
tax = {x['basicD']: float(x['taxDividA']) for x in json.load(open(R / 'divid.json', encoding='utf-8'))['dividList']}
print("10월 과세표준", tax['20261015'], "/", off['20261015'], " 직전 11회 과세표준 합", sum(tax[d] for d, v in last12 if d != '20261015'))
# 올해 월별: KODEX 200 월간 수익 vs 커버드콜
print("--- 오늘(10/21) 줄", [ (r[0], f"{r[1]*100:+.2f}%", f"{r[2]*100:+.2f}%") for r in rows if r[0]=='20261021'])
print("--- 차이 큰 날(커버드콜이 덜 오른 폭 상위 3)", sorted(((r[1]-r[2])*100, r[0]) for r in rows if r[1] >= 0.03)[-3:])
print("--- 급락 42일 중 커버드콜이 더 빠진 날", [(r[0], f"{r[1]*100:+.2f}", f"{r[2]*100:+.2f}") for r in rows if r[1] <= -0.03 and r[2] < r[1]])
n = int(10_000_000 // px[CC][days[-1]])
print("1천만원 오늘 종가", px[CC][days[-1]], "주", n, "10월 분배금", n*281, "10월 세금", round(n*105*0.154), "9월 분배금", n*300, "9월 세금", round(n*2*0.154))
up = [r for r in rows if r[1] >= 0.03]; dn = [r for r in rows if r[1] <= -0.03]
print("급락날 평균 차이 %p", round((st.mean(r[2] for r in dn) - st.mean(r[1] for r in dn))*100, 2), "급등날 평균 차이 %p", round((st.mean(r[1] for r in up) - st.mean(r[2] for r in up))*100, 2))
print("주당 프리미엄 목표 15%/52주", round(15/52, 2))
