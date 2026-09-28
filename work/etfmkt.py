# [ETF 시황](카페 12시 코너) 재료 뽑기. 네이버 증권 ETF 시세 한 번 받아 오른 것·내린 것·거래대금 상위를 찍는다.
# 사용: py -3.12 work/etfmkt.py [저장폴더]  → 폴더에 snap.json(원자료+코스피·코스닥)을 남긴다.
# 2026-09-28: 코너를 처음 쓸 때 도구가 없어 회차 안에서 손으로 짰다. 매일 쓰는 코너라 도구로 뺐다.
# 장중에 돌리면 장중 값이다. 글에 기준 시각을 반드시 적는다.
import sys, os, json, datetime, requests
sys.stdout.reconfigure(encoding='utf-8')
H = {"User-Agent": "Mozilla/5.0 Chrome/129.0", "Referer": "https://finance.naver.com/sise/etf.naver"}
out = sys.argv[1] if len(sys.argv) > 1 else '.'
os.makedirs(out, exist_ok=True)
d = requests.get("https://finance.naver.com/api/sise/etfItemList.nhn?etfType=0&targetColumn=market_sum&sortOrder=desc", headers=H, timeout=30).json()
idx = {}
for code in ("KOSPI", "KOSDAQ"):
    x = requests.get(f"https://polling.finance.naver.com/api/realtime/domestic/index/{code}", headers=H, timeout=30).json()["datas"][0]
    idx[code] = {k: x.get(k) for k in ("closePrice", "fluctuationsRatio", "marketStatus", "localTradedAt")}
ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
json.dump({"ts": ts, "etf": d, "index": idx}, open(os.path.join(out, "snap.json"), "w", encoding="utf-8"), ensure_ascii=False)
L = d["result"]["etfItemList"]
print(f"[{ts}] 코스피 {idx['KOSPI']['closePrice']} {idx['KOSPI']['fluctuationsRatio']}% · 코스닥 {idx['KOSDAQ']['closePrice']} {idx['KOSDAQ']['fluctuationsRatio']}% · 장 {idx['KOSPI']['marketStatus']}")
print(f"ETF {len(L)}개 · 상승 {sum(x['changeRate'] > 0 for x in L)} · 하락 {sum(x['changeRate'] < 0 for x in L)}")
act = [x for x in L if x["amonut"] >= 100]   # 거래대금 1억원(=100백만) 미만은 뺀다 — 몇 주 거래로 튄 값이 순위를 차지한다
inv = lambda x: '인버스' in x['itemname']
for name, src, key, rev in [("상승(거래대금 1억 이상)", act, 'changeRate', True),
                            ("상승 — 인버스 제외", [x for x in act if not inv(x)], 'changeRate', True),
                            ("하락(거래대금 1억 이상)", act, 'changeRate', False),
                            ("거래대금", L, 'amonut', True)]:
    print(f"== {name}")
    for x in sorted(src, key=lambda x: x[key], reverse=rev)[:8]:
        print(f"  {x['itemcode']} {x['itemname']} {x['nowVal']:,}원 {x['changeRate']:+.2f}% 거래대금 {x['amonut']/100:,.0f}억")
