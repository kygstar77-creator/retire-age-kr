# mixreset1016 — 2021년 10월 3억 30년 원리금균등 5년 고정 뒤 남은 25년을 새 금리로 다시 계산
import sys, json, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
sys.stdout.reconfigure(encoding='utf-8')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import apis
ecos = apis.ecos('121Y006', 'M', '202101', '202609', 'BECBLA0302', n=80)
fin = [x for x in apis.finlife('mortgage') if x['담보'] == '아파트' and x['상환방식'] == '분할상환방식'
       and x['금리유형'] == '변동금리' and any(b in (x['은행'] or '') for b in ['국민', '신한', '하나', '우리', '농협'])]
json.dump({'ecos_121Y006_BECBLA0302': ecos, 'finlife_mortgage_var_split_apt': fin}, open('raw.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
E = {t: float(v) for t, v, _ in ecos}

def pmt(P, r, n):
    i = r / 12; return P * i / (1 - (1 + i) ** -n)

P = 300_000_000; r0 = E['202110'] / 100
m0 = pmt(P, r0, 360); B = P
for _ in range(60): B = B * (1 + r0 / 12) - m0
print(f'2021-10 평균 {r0*100:.2f}% · 월 {m0:,.0f}원 · 5년 뒤 남은 원금 {B:,.0f}원')
print(f'2026-08 평균 {E["202608"]:.2f}% (최근 공표월 {ecos[-1][0]})')
rows = [('2021년 10월 그대로', r0)]
rows.append(('2026년 8월 새 주담대 평균', E['202608'] / 100))
for x in sorted(fin, key=lambda x: float(x['대출최저'])):
    rows.append((f"{x['은행']} 변동 최저", float(x['대출최저']) / 100))
lo = min(float(x['대출최저']) for x in fin); hi = max(float(x['대출최고']) for x in fin)
rows += [('5대 은행 변동 최저', lo / 100), ('5대 은행 변동 최고', hi / 100)]
for name, r in rows:
    m = pmt(B, r, 300)
    print(f'{name:22s} {r*100:.2f}% 월 {m:,.0f}원 · 차이 {m-m0:+,.0f}원 · 1년 {(m-m0)*12:+,.0f}원')
for x in fin: print(x['은행'], x['상품'].replace('\n', ''), x['대출최저'], x['대출최고'], x['공시월'])
print('--- 빌린 달별(5년 뒤 그달 평균으로 다시 계산, 2026-10은 아직 공표 전이라 최근 8월 값)')
for ym, ym5 in [('202101', '202601'), ('202104', '202604'), ('202107', '202607'), ('202110', '202608')]:
    r = E[ym] / 100; rN = E[ym5] / 100; m = pmt(P, r, 360); b = P
    for _ in range(60): b = b * (1 + r / 12) - m
    mm = pmt(b, rN, 300)
    print(f'{ym} {E[ym]:.2f}% -> {ym5} {E[ym5]:.2f}% 월 {m:,.0f} 남은 {b:,.0f} 새 {mm:,.0f} 차이 {mm-m:+,.0f}')
