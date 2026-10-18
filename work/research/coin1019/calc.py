# coin1019 계산 — 업비트 일봉 종가(원) · 소득세법 37조⑤·64조의3②·시행령 88조
import json
def close(f, d):
    for c in json.load(open(f, encoding='utf-8')):
        if c['candle_date_time_kst'].startswith(d): return c['trade_price']
b23 = close('raw/up_BTC_2023.json', '2023-10-18')
b25 = close('raw/up_BTC_2025.json', '2025-10-18')
now = close('raw/up_BTC_now.json', '2026-10-17')
tax = lambda gain: max(gain - 2_500_000, 0) * 0.22
out = []
P = lambda *a: out.append(' '.join(str(x) for x in a))
P('BTC 종가 2023-10-18', b23, '· 2025-10-18', b25, '· 2026-10-17', now)
for name, buy in (('A 3년 전', b23), ('B 1년 전', b25)):
    qty = 10_000_000 / buy
    val = qty * now
    P(f'{name} 1천만원 → 수량 {qty:.5f} · 10/17 평가 {val:,.0f} · 손익 {val-1e7:,.0f} ({(val/1e7-1)*100:.1f}%)')
    base = max(val, 1e7)   # 연말 값=10/17 값이라 가정할 때 인정 취득가
    P(f'  인정 취득가(연말 값=10/17 값 가정) {base:,.0f} · 그 값에 팔면 과세 이익 0')
    if val > 1e7:
        P(f'  만약 실제 취득가(1천만)로 셈하면 세금 {tax(val-1e7):,.0f}')
    P(f'  2027년에 1천만원 되돌아와 팔면 과세 이익 {max(1e7-base,0):,.0f}')
P('2027년 이후 이익 1천만원 한 해 세금', f'{tax(1e7):,.0f}', '· 두 해 500만씩', f'{2*tax(5e6):,.0f}', '· 차', f'{tax(1e7)-2*tax(5e6):,.0f}')
P('손실 이월 없음: 2027 -500만, 2028 +1,000만 → 2028 세금', f'{tax(1e7):,.0f}', '· 합쳐 셀 수 있었다면', f'{tax(5e6):,.0f}')
P('같은 해 비트코인 +1,000만·이더리움 -500만 → 합쳐 500만 → 세금', f'{tax(5e6):,.0f}')
P('250만원 이하 이익 세금 0 · 이익 300만이면', f'{tax(3e6):,.0f}')
open('calc_out.txt', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('\n'.join(out))
