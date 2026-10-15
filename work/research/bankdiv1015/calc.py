# bankdiv1015 계산 — KRX 종가(야후 15:30, 다음 prevClosingPrice와 10/14 일치) · DART 2025 주당배당금 · 2026 분기배당
import json
y = json.load(open('src/yahoo.json', encoding='utf-8'))
d25 = {'KB금융': 4367, '신한지주': 2590, '하나금융지주': 4105, '우리금융지주': 1360, 'BNK금융지주': 735}
d26 = {'KB금융': [1143, 1155], '신한지주': [740, 740], '하나금융지주': [1145, 1155], '우리금융지주': [220, 220], 'BNK금융지주': [150, 150]}
M = 10_000_000
for n in d25:
    c = y[n]['close']; now, prev = c['10-15'], c['10-14']
    sh = int(M // now); div = sh * d25[n]; net = round(div * (1 - 0.154))
    print(f'{n}: 10/14 {prev:,.0f} → 10/15 {now:,.0f} ({(now/prev-1)*100:+.2f}%) | 2025 DPS {d25[n]:,} → 수익률 {d25[n]/now*100:.2f}% (어제 종가면 {d25[n]/prev*100:.2f}%)'
          f' | 1천만원 {sh}주(남는 돈 {M-sh*now:,.0f}) 배당 {div:,} 세후(15.4%) {net:,} 월 {net/12:,.0f} | 2026 1·2분기 {sum(d26[n]):,}원 ({d26[n]})')
