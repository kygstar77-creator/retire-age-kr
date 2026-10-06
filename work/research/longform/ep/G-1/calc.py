# G-1 금 롱폼 계산 — 공개일 기준으로 원자료를 다시 받아 영수증(산 날 4 × 산 길 4)과 세 조각 분해를 낸다.
#   py -3.12 calc.py            → 가장 최근 KRX 거래일 기준
#   py -3.12 calc.py 2026-10-13 → 그 날(또는 그 전 마지막 거래일) 기준 — 공개 전날 다시 돌린다
# 원자료(전부 raw/calc_<기준일>.json에 저장):
#   KRX 금시장 금 1kg 일별 종가 원/g — 네이버 증권 front-api(reutersCode M04020000, 옛 goldDailyQuote 페이지는 10/6 폐지 확인)
#   ACE KRX금현물 ETF 411060.KS 종가 · 금 선물 GC=F(달러/온스) — 야후 차트 API
#   원/달러 매매기준율 — 한국은행 ECOS 731Y001 0000001(일)
# 세금·비용 규칙은 facts.txt [G0] 법 원문 줄. 골드뱅킹은 KB 고시 일시가 확인 필요([G5])라 '어림'으로만 찍는다(대본에 원 단위 금지).
import sys, os, json, math, datetime as dt, time
sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work'); sys.stdout.reconfigure(encoding='utf-8')
import apis
HERE = os.path.dirname(os.path.abspath(__file__)); RAW = os.path.join(HERE, 'raw'); os.makedirs(RAW, exist_ok=True)
M = 10_000_000; OZ = 31.1034768; TAX = 0.154; VAT = 0.10; GB = 0.01   # 골드뱅킹 살 때 +1%·팔 때 -1%(KB 고시 규칙, [G0])
START = '2025-09-01'

def krx_gold():
    out, page = {}, 1
    while page < 40:
        d = apis._j(f'https://m.stock.naver.com/front-api/marketIndex/prices?category=metals&reutersCode=M04020000&page={page}&pageSize=60')
        rows = d.get('result') or []
        if not rows: break
        for r in rows: out[r['localTradedAt'][:10]] = float(r['closePrice'].replace(',', ''))
        if min(out) < START: break
        page += 1; time.sleep(0.3)
    return dict(sorted((k, v) for k, v in out.items() if k >= START))

def yahoo(sym):
    p1 = int(dt.datetime(2025, 8, 25).timestamp()); p2 = int(time.time()) + 86400
    d = apis._j(f'https://query1.finance.yahoo.com/v8/finance/chart/{sym}?period1={p1}&period2={p2}&interval=1d')
    r = d['chart']['result'][0]; tz = r['meta']['gmtoffset']
    out = {}
    for t, c in zip(r['timestamp'], r['indicators']['quote'][0]['close']):
        if c is not None: out[dt.datetime.fromtimestamp(t + tz, dt.timezone.utc).strftime('%Y-%m-%d')] = float(c)
    return out

def ecos_fx(end):
    k = apis.key('ecos')
    d = apis._j(f'https://ecos.bok.or.kr/api/StatisticSearch/{k}/json/kr/1/600/731Y001/D/20250825/{end.replace("-", "")}/0000001')
    return {f"{r['TIME'][:4]}-{r['TIME'][4:6]}-{r['TIME'][6:]}": float(r['DATA_VALUE']) for r in d['StatisticSearch']['row']}

def on_or_before(s, day):
    ks = [k for k in s if k <= day]; return (ks[-1], s[ks[-1]]) if ks else (None, None)

def before(s, day):   # GC=F는 뉴욕 종가 — KRX 15:30 마감 때 알 수 있는 건 전날 뉴욕 종가
    ks = [k for k in s if k < day]; return (ks[-1], s[ks[-1]]) if ks else (None, None)

def back(day, months=0, years=0):
    d = dt.date.fromisoformat(day); y, m = d.year - years, d.month - months
    while m < 1: m += 12; y -= 1
    return dt.date(y, m, min(d.day, 28 if m == 2 else 30 if m in (4, 6, 9, 11) else 31)).isoformat()

krx = krx_gold(); etf = yahoo('411060.KS'); gc = yahoo('GC=F')
asof_req = sys.argv[1] if len(sys.argv) > 1 else max(krx)
fx = ecos_fx(asof_req)
asof, k1 = on_or_before(krx, asof_req)
json.dump({'asof': asof, 'KRX_M04020000_won_per_g': krx, 'ETF_411060': etf, 'GC_F_usd_oz': gc, 'ECOS_731Y001_0000001': fx},
          open(os.path.join(RAW, f'calc_{asof}.json'), 'w', encoding='utf-8'), ensure_ascii=False)

def intl(day):   # 국제 금값을 원화 1g으로(어림): 전날 뉴욕 GC=F 종가 × 그날 ECOS 매매기준율 ÷ 31.1034768
    gd, g = before(gc, day); fd, f = on_or_before(fx, day)
    return g, f, g * f / OZ, gd, fd

win = {k: v for k, v in krx.items() if back(asof, years=1) <= k <= asof}
peak_day = max(win, key=win.get)
days = [('1년 전', on_or_before(krx, back(asof, years=1))[0]), ('1년 고점', peak_day),
        ('3개월 전', on_or_before(krx, back(asof, months=3))[0]), ('1개월 전', on_or_before(krx, back(asof, months=1))[0])]

L = []; P = lambda *a: L.append(' '.join(str(x) for x in a))
P(f'# G-1 calc 기준일 {asof} (요청 {asof_req}) · 실행 {dt.datetime.now():%Y-%m-%d %H:%M} · 원자료 raw/calc_{asof}.json')
P(f'KRX 금 {asof} {k1:,.0f}원/g · 1년 고점 {peak_day} {krx[peak_day]:,.0f}원/g · 고점 대비 {(k1/krx[peak_day]-1)*100:.2f}% · 산 값(고점)으로 돌아가려면 +{(krx[peak_day]/k1-1)*100:.1f}%')
e1d, e1 = on_or_before(etf, asof)
g1, f1, i1, gd1, fd1 = intl(asof)
P(f'ETF 411060 {e1d} {e1:,.0f}원 · GC=F {gd1} {g1:,.2f}달러 · ECOS {fd1} {f1:,.1f}원 · 국제값 원/g 어림 {i1:,.0f} · KRX 웃돈 {(k1/i1-1)*100:.2f}%')
P('')
P('## 영수증 — 1천만원, 산 날 4 × 산 길 4 (팔 때 기준일 값, 증권사 수수료·실물 매입가 차이 별도)')
P('| 산 날 | KRX 금시장 | 금현물 ETF(411060) | 골드뱅킹(어림) | 골드바(부가세 10%) |')
P('|---|---|---|---|---|')
rec = []
for name, d0 in days:
    k0 = krx[d0]; r = k1 / k0
    krx_v = M * r                                           # 부가세 면제(조특법 126조의7①)·양도세 없음(소득세법 94조)
    ed0, e0 = on_or_before(etf, d0); etf_g = M * (e1 / e0 - 1); etf_v = M + etf_g - max(0, etf_g) * TAX   # 이익만 15.4%(어림: 과표기준가 대신 매매차익)
    _, _, i0, gd0, fd0 = intl(d0)
    gb_g = M / (i0 * (1 + GB)) * i1 * (1 - GB) - M; gb_v = M + gb_g - max(0, gb_g) * TAX
    bar_v = M / (1 + VAT) * r                               # 부가세 10% 먼저 빠진 금값 몫이 KRX만큼 움직였다고 본 값(파는 값 차이 별도)
    row = dict(name=name, day=d0, krx0=k0, krx=round(krx_v), krx_pct=(r-1)*100, etf_day=ed0, etf0=e0, etf=round(etf_v),
               etf_pct=(e1/e0-1)*100, gb=round(gb_v), gb_pct=(gb_v/M-1)*100, bar=round(bar_v), bar_pct=(bar_v/M-1)*100,
               gc_day=gd0, fx_day=fd0, intl0=i0)
    rec.append(row)
    P(f"| {name} {d0} ({k0:,.0f}원/g) | {krx_v:,.0f}원 ({(r-1)*100:+.2f}%) | {etf_v:,.0f}원 ({(etf_v/M-1)*100:+.2f}%) | {gb_v:,.0f}원 ({(gb_v/M-1)*100:+.2f}%) | {bar_v:,.0f}원 ({(bar_v/M-1)*100:+.2f}%) |")
P('')
P('## 세 조각 분해 — KRX 금 변화 = 달러 금값 × 환율 × KRX 웃돈 (곱이 정확히 맞음, 막대는 로그 비율로 % 포인트 배분)')
P('| 산 날 | KRX 전체 | 달러 금값(GC=F) | 환율(ECOS) | KRX 웃돈 | 웃돈 그때→지금 | 검산(곱) |')
P('|---|---|---|---|---|---|---|')
for row in rec:
    d0 = row['day']; g0, f0, i0, _, _ = intl(d0)
    a, b = g1 / g0, f1 / f0; c = (k1 / i1) / (row['krx0'] / i0); tot = k1 / row['krx0']
    lt = math.log(tot); share = lambda x: (math.log(x) / lt * (tot - 1) * 100) if lt else 0
    row.update(gold_usd_pct=(a-1)*100, fx_pct=(b-1)*100, prem_pct=(c-1)*100, prem0=(row['krx0']/i0-1)*100, prem1=(k1/i1-1)*100,
               pp=dict(gold=share(a), fx=share(b), prem=share(c)))
    P(f"| {row['name']} {d0} | {(tot-1)*100:+.2f}% | {(a-1)*100:+.2f}% ({share(a):+.1f}%p) | {(b-1)*100:+.2f}% ({share(b):+.1f}%p) | {(c-1)*100:+.2f}% ({share(c):+.1f}%p) | {row['prem0']:+.1f}% → {row['prem1']:+.1f}% | {(a*b*c-1)*100:+.2f}% |")
P('')
P('## 쓰는 법·주의')
P('- 대본 숫자는 이 표만. 제목 677만원·975만원은 2026-10-02 기준 가안 — 기준일이 바뀌면 카피 재심사(titles.md 꼭 지킬 것).')
P('- 국제값은 GC=F(선물, 전날 뉴욕 종가)×ECOS 매매기준율 어림 → 화면에 "어림" 표기. 웃돈은 이 어림 대비라 소수 한 자리까지만 말한다.')
P('- 골드뱅킹 열은 국제값 어림 ±1% 규칙으로 낸 값이라 KB 실제 고시와 다르다([G5]) → 대본에서는 %·원 단위 둘 다 말하지 않고 규칙만.')
P('- ETF 세금은 매매차익 15.4%로 어림(실제는 과표기준가 증가분과 작은 쪽). 손실 구간은 세금 0이라 영향 없음.')
P('- 골드바는 금값 몫이 KRX만큼 움직였다고 본 값. 금은방·은행에 팔 때 받는 값 차이는 빠져 있어 실제로는 더 적다.')
open(os.path.join(HERE, 'calc_out.txt'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
json.dump(dict(asof=asof, krx_now=k1, peak_day=peak_day, peak=krx[peak_day], need_pct=(krx[peak_day]/k1-1)*100, etf_now=e1,
               gc_now=g1, fx_now=f1, intl_now=i1, rows=rec), open(os.path.join(HERE, 'calc.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('\n'.join(L))
