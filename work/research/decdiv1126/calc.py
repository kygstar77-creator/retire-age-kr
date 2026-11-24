# 야후 배당 기록(raw/yahoo_*.json)으로 작년 12월 배당·1년 배당·지금 종가를 센다 → calc_out.txt
import json, datetime as dt, os
T = ['JEPI', 'JEPQ', 'SCHD', 'DGRO', 'VYM', 'VIG', 'VOO']
out = []
for t in T:
    j = json.load(open(f'raw/yahoo_{t}.json', encoding='utf-8'))['chart']['result'][0]
    ts = j['timestamp']; cl = j['indicators']['quote'][0]['close']
    last = max(i for i, c in enumerate(cl) if c is not None)
    d_last = dt.datetime.utcfromtimestamp(ts[last]).date(); px = cl[last]
    divs = sorted((dt.datetime.utcfromtimestamp(int(k)).date(), v['amount']) for k, v in j.get('events', {}).get('dividends', {}).items())
    y25 = [(d, a) for d, a in divs if d.year == 2025]
    dec25 = [(d, a) for d, a in y25 if d.month == 12]
    y26 = [(d, a) for d, a in divs if d.year == 2026]
    s25 = sum(a for _, a in y25); sdec = sum(a for _, a in dec25)
    # 지난 12개월(마지막 종가일 기준) 배당 합
    ttm = sum(a for d, a in divs if (d_last - d).days < 365)
    out.append(f"{t} | 마지막 종가 {d_last} {px:.2f}달러 | 2025년 배당 {len(y25)}번 합 {s25:.4f} | 2025년 12월 배당락 {[(str(d), round(a,4)) for d,a in dec25]} 합 {sdec:.4f} = 1년의 {sdec/s25*100:.1f}% | 2026년 지금까지 {len(y26)}번 {[(str(d), round(a,4)) for d,a in y26]} | 지난 12개월 합 {ttm:.4f} → 종가 대비 {ttm/px*100:.2f}% | 1,000만원(환율 1,460원 가정 아님 — 달러 1만 달러) 어치 {10000/px:.1f}주 x 작년 12월 {sdec:.4f} = {10000/px*sdec:.1f}달러")
open('calc_out.txt', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('\n'.join(out))
