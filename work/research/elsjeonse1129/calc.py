# elsjeonse1129 — 잠실엘스 전세 새 계약 vs 갱신 (국토부 실거래, raw/11710_*)
#   py -3.12 work/research/elsjeonse1129/calc.py > calc_out_1127.txt
import json, glob, os, sys, statistics as st, collections
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
def num(s): return int((s or '0').replace(',', '') or 0)
def ym(r): return int(r['dealYear']) * 100 + int(r['dealMonth'])
rent, trade = [], []
for f in glob.glob(os.path.join(HERE, 'raw', '11710_*_rent.json')):
    rent += [r for r in json.load(open(f, encoding='utf-8')) if r['aptNm'] == '잠실엘스']
for f in glob.glob(os.path.join(HERE, 'raw', '11710_*_trade.json')):
    trade += [r for r in json.load(open(f, encoding='utf-8')) if r['aptNm'] == '잠실엘스']
def band(r, lo, hi): return lo <= float(r['excluUseAr']) < hi
def med(v): return st.median(v) if v else None
def q(v):
    v = sorted(v); n = len(v)
    return (v[n // 4], v[(3 * n) // 4]) if n >= 4 else (None, None)
W0, W1 = 202512, 202611   # 최근 12개월 계약
for name, lo, hi in (('84㎡대(80~86)', 80, 86), ('59㎡대(59~60)', 59, 61)):
    print(f'\n===== {name} · 계약 {W0}~{W1}')
    R = [r for r in rent if band(r, lo, hi) and W0 <= ym(r) <= W1]
    J = [r for r in R if num(r['monthlyRent']) == 0]
    print('전월세', len(R), '순수 전세', len(J), '월세 낀 것', len(R) - len(J))
    for ct in ('신규', '갱신', ''):
        v = [num(r['deposit']) for r in J if r['contractType'] == ct]
        print(f'  {ct or "빈칸"}: {len(v)}건 가운데 {med(v)} 만원 · 사분위 {q(v)} · 최저 {min(v) if v else None} 최고 {max(v) if v else None}')
    new = [num(r['deposit']) for r in J if r['contractType'] == '신규']
    ren = [num(r['deposit']) for r in J if r['contractType'] == '갱신']
    if new and ren: print(f'  차이(신규-갱신 가운데) {med(new) - med(ren)} 만원 · 비율 {med(new) / med(ren):.3f}')
    # 갱신: 종전 보증금 대비
    G = [r for r in J if r['contractType'] == '갱신' and num(r['preDeposit']) > 0 and num(r['preMonthlyRent']) == 0]
    rate = [(num(r['deposit']) / num(r['preDeposit']) - 1) * 100 for r in G]
    print(f'  갱신 중 종전 전세 있음 {len(G)}건 · 올린 비율 가운데 {med(rate):.2f}%' if rate else '  갱신 종전 없음')
    if rate:
        print('    5% 이하', sum(1 for x in rate if x <= 5.0001), '· 5% 초과', sum(1 for x in rate if x > 5.0001), '· 그대로(0%)', sum(1 for x in rate if abs(x) < 0.001), '· 내림', sum(1 for x in rate if x < -0.001))
        print('    종전 가운데', med([num(r['preDeposit']) for r in G]), '→ 새 가운데', med([num(r['deposit']) for r in G]))
    for u in ('사용', '미사용', ''):
        g = [r for r in G if r['useRRRight'] == u]
        rr = [(num(r['deposit']) / num(r['preDeposit']) - 1) * 100 for r in g]
        if g: print(f'    갱신요구권 {u or "빈칸"}: {len(g)}건 올린 비율 가운데 {med(rr):.2f}% · 새 보증금 가운데 {med([num(r["deposit"]) for r in g])} · 5% 초과 {sum(1 for x in rr if x > 5.0001)}')
    # 반기별 신규·갱신 가운데
    for a, b, lab in ((202512, 202605, '25.12~26.5'), (202606, 202611, '26.6~26.11')):
        n = [num(r['deposit']) for r in J if r['contractType'] == '신규' and a <= ym(r) <= b]
        g = [num(r['deposit']) for r in J if r['contractType'] == '갱신' and a <= ym(r) <= b]
        print(f'  {lab}: 신규 {len(n)}건 {med(n)} · 갱신 {len(g)}건 {med(g)}')
    # 1년 전 같은 반기
    n0 = [num(r['deposit']) for r in rent if band(r, lo, hi) and num(r['monthlyRent']) == 0 and r['contractType'] == '신규' and 202506 <= ym(r) <= 202511]
    print(f'  (25.6~25.11 신규 {len(n0)}건 {med(n0)})')
    # 매매
    T = [num(r['dealAmount']) for r in trade if band(r, lo, hi) and W0 <= ym(r) <= W1 and not r.get('cdealType')]
    T2 = [num(r['dealAmount']) for r in trade if band(r, lo, hi) and 202606 <= ym(r) <= W1 and not r.get('cdealType')]
    print(f'  매매(해제 뺌) {len(T)}건 가운데 {med(T)} · 26.6~11 {len(T2)}건 가운데 {med(T2)}')
    if T and new: print(f'  전세가율 신규/매매 {med(new) / med(T) * 100:.1f}% · 갱신/매매 {med(ren) / med(T) * 100:.1f}%')
    if T2:
        n2 = [num(r['deposit']) for r in J if r['contractType'] == '신규' and 202606 <= ym(r) <= W1]
        print(f'  26.6~11 신규/매매 {med(n2) / med(T2) * 100:.1f}%')
# 해제 건수
print('\n해제 매매(84)', sum(1 for r in trade if band(r, 80, 86) and W0 <= ym(r) <= W1 and r.get('cdealType')))
print('계약기간 예', collections.Counter(r['contractTerm'] for r in rent if W0 <= ym(r) <= W1).most_common(4))
# --- §E 대조용: 경쟁 1(307720)의 '10~11월 신규 중위값' 같은 창 · 월별 신규/갱신 가운데(84)
print('\n§E 84㎡대 10~11월 신규 가운데')
for a, b in ((202510, 202511), (202610, 202611)):
    v = [num(r['deposit']) for r in rent if band(r, 80, 86) and num(r['monthlyRent']) == 0 and r['contractType'] == '신규' and a <= ym(r) <= b]
    print(f'  {a}~{b}: {len(v)}건 {med(v)}')
print('§F 84㎡대 반기 신규 가운데 · 갱신 가운데 · 차이')
for a, b, lab in ((202506, 202511, '25.6~25.11'), (202512, 202605, '25.12~26.5'), (202606, 202611, '26.6~26.11')):
    n = [num(r['deposit']) for r in rent if band(r, 80, 86) and num(r['monthlyRent']) == 0 and r['contractType'] == '신규' and a <= ym(r) <= b]
    g = [num(r['deposit']) for r in rent if band(r, 80, 86) and num(r['monthlyRent']) == 0 and r['contractType'] == '갱신' and a <= ym(r) <= b]
    print(f'  {lab}: 신규 {len(n)} {med(n)} · 갱신 {len(g)} {med(g)} · 차이 {med(n) - med(g)}')
print('§G 84 갱신요구권 표시 없는 갱신 중 5% 초과 41건 올린 금액 가운데')
G = [r for r in rent if band(r, 80, 86) and W0 <= ym(r) <= W1 and num(r['monthlyRent']) == 0 and r['contractType'] == '갱신' and num(r['preDeposit']) > 0 and num(r['preMonthlyRent']) == 0]
up = [num(r['deposit']) - num(r['preDeposit']) for r in G if (num(r['deposit']) / num(r['preDeposit']) - 1) * 100 > 5.0001]
print('  ', len(up), '건 올린 금액 가운데', med(up), '최대', max(up))
us = [num(r['deposit']) - num(r['preDeposit']) for r in G if r['useRRRight'] == '사용']
print('   요구권 사용 86건 올린 금액 가운데', med(us))
