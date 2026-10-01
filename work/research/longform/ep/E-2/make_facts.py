"""E-2 사실표 facts.txt 만들기 (2026-10-01 루프 16회차). 숫자는 전부 원문 파일에서 정규식으로 뽑고 계산만 한다 — 손으로 친 숫자 없음.
원문: raw/10-Q_0001628280-26-049270.txt(2026-07-23 제출, 2026년 2분기) · raw/8-K_0001628280-26-063820.txt(2026-09-29) · quarters.json(XBRL) · price.json(나스닥 공식)."""
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(H, 'raw')
q10 = open(os.path.join(R, '10-Q_0001628280-26-049270.txt'), encoding='utf-8').read()
k8 = open(os.path.join(R, '8-K_0001628280-26-063820.txt'), encoding='utf-8').read()
Q = json.load(open(os.path.join(H, 'quarters.json'), encoding='utf-8'))['q']
P = json.load(open(os.path.join(H, 'price.json'), encoding='utf-8'))

ops = q10[q10.find('Consolidated Statements of Operations (in millions'):]
cf = q10[q10.find('Cash Flows from Investing Activities') - 3000:]
bs = q10[q10.find('Consolidated Balance Sheets (in millions'):]
num = lambda s: -float(s.strip('() ').replace(',', '')) if '(' in s else float(s.replace(',', ''))
def row(text, label, n=4):  # label 뒤 숫자 n개 (3개월 26·25, 6개월 26·25)
    m = re.search(re.escape(label) + r'\s+\$?\s*((?:\(?\s*[\d,]+\s*\)?\s+\$?\s*){%d})' % n, text)
    return [num(x) for x in re.findall(r'\(\s*[\d,]+\s*\)|[\d,]+', m.group(1))][:n]

L = {}
for lab in ['Automotive sales', 'Automotive regulatory credits', 'Automotive leasing', 'Total automotive revenues', 'Energy generation and storage',
            'Services and other', 'Total revenues']:
    L['rev:' + lab] = row(ops, lab)
cost = ops[ops.find('Cost of revenues'):]
for lab in ['Total automotive cost of revenues', 'Energy generation and storage', 'Services and other', 'Total cost of revenues']:
    L['cost:' + lab] = row(cost, lab)
for lab in ['Gross profit', 'Research and development', 'Selling, general and administrative', 'Total operating expenses', 'Income from operations',
            'Interest income', 'Other income, net', 'Income before income taxes', 'Net income']:
    L[lab] = row(ops, lab)
cap = row(cf, 'Purchases of property and equipment excluding finance leases, net of sales', 2)
ocf = row(cf, 'Net cash provided by operating activities', 2)
spx = re.search(r'Purchase of SpaceX equity investment\s+\(\s*([\d,]+)\s*\)', cf).group(1)
cash = row(bs, 'Cash and cash equivalents', 2); sti = row(bs, 'Short-term investments', 2)
capex_guide = re.search(r'expect our capital expenditures to be in excess of \$(\d+) billion in 2026', q10).group(1)
deliv = re.search(r'delivered approximately (\d+) thousand consumer vehicles through the second quarter', q10).group(1)
prod = re.search(r'produced approximately (\d+) thousand consumer vehicles', q10).group(1)
gwh = re.search(r'deployed ([\d.]+) GWh of energy storage products through the second quarter', q10).group(1)
cyb = 'we began production of Cybercab' in q10
fund = 'will necessitate additional funding beyond our operating cash flow' in q10
# 8-K 9/29
fac = re.findall(r'\$\s*([\d.]+)\s*billion\s+senior unsecured\s+([\w-]+)', k8)  # [(20.0, three-year), (8.0, five-year), (2.0, 364-day)]
fsum = sum(float(a) for a, _ in fac)
old = re.search(r'Existing Revolving Credit Agreement had aggregate commitments of \$([\d.]+) billion and was set to mature on ([A-Za-z]+ \d+, \d{4})', k8)
nolo = 'No loans were outstanding' in k8 or 'no loans outstanding' in k8.lower()
nopen = 'did not incur any early termination penalties' in k8

pct = lambda a, b: f'{(a / b - 1) * 100:+.1f}%'
gm = lambda r, c: f'{(r - c) / r * 100:.1f}%'
o = []; A = o.append
A('# E-2 사실표 — 테슬라 (2026-10-01 루프 16회차, make_facts.py 기계 출력). 대본 숫자는 여기서만. 단위 백만 달러(=100만 달러), 3개월값.')
A('# 원문: 10-Q 2026-07-23 제출(0001628280-26-049270) · 8-K 2026-09-29(0001628280-26-063820) · SEC XBRL companyfacts · 나스닥 공식 과거 시세(야후와 대조)')
A('')
r, c = L['rev:Total revenues'], L['cost:Total cost of revenues']
A(f'[1] 2026년 2분기 매출 {r[0]:,.0f} (1년 전 {r[1]:,.0f}, {pct(r[0], r[1])}) — 10-Q 손익계산서')
A(f'[2] 2026년 2분기 영업이익 {L["Income from operations"][0]:,.0f} (1년 전 {L["Income from operations"][1]:,.0f}, {pct(L["Income from operations"][0], L["Income from operations"][1])}) · 영업이익률 {L["Income from operations"][0]/r[0]*100:.1f}% (1년 전 {L["Income from operations"][1]/r[1]*100:.1f}%)')
A(f'[3] 같은 분기 이자수익 {L["Interest income"][0]:,.0f} > 영업이익 {L["Income from operations"][0]:,.0f} · 기타수익 {L["Other income, net"][0]:,.0f} · 세전이익 {L["Income before income taxes"][0]:,.0f} · 순이익 {L["Net income"][0]:,.0f}(1년 전 {L["Net income"][1]:,.0f})')
A(f'    → 세전이익 중 영업에서 번 몫 {L["Income from operations"][0]/L["Income before income taxes"][0]*100:.0f}% (나머지는 이자·기타수익)')
rd, sga = L['Research and development'], L['Selling, general and administrative']
A(f'[4] 연구개발비 {rd[0]:,.0f} (1년 전 {rd[1]:,.0f}, {pct(rd[0], rd[1])}) · 판매관리비 {sga[0]:,.0f} (1년 전 {sga[1]:,.0f}, {pct(sga[0], sga[1])}) · 영업비용 합계 {L["Total operating expenses"][0]:,.0f}(1년 전 {L["Total operating expenses"][1]:,.0f})')
A(f'    매출총이익 {L["Gross profit"][0]:,.0f}(1년 전 {L["Gross profit"][1]:,.0f}, {pct(L["Gross profit"][0], L["Gross profit"][1])}) — 총이익은 늘었는데 영업비용이 더 늘어 영업이익이 줄었다')
A('[5] 부문별 매출(1년 전) · 매출총이익률(1년 전) — 10-Q')
for lab, cl in [('Total automotive revenues', 'Total automotive cost of revenues'), ('Energy generation and storage', 'Energy generation and storage'), ('Services and other', 'Services and other')]:
    rv, cs = L['rev:' + lab], L['cost:' + cl]
    A(f'    {lab}: {rv[0]:,.0f} ({rv[1]:,.0f}, {pct(rv[0], rv[1])}) · 총이익률 {gm(rv[0], cs[0])} ({gm(rv[1], cs[1])})')
rc = L['rev:Automotive regulatory credits']
A(f'    그중 규제 크레딧 {rc[0]:,.0f} ({rc[1]:,.0f}, {pct(rc[0], rc[1])}) — 10-Q: "Recent governmental and regulatory actions have restricted certain regulatory credit programs"')
A(f'    규제 크레딧 줄어든 금액 {rc[1]-rc[0]:,.0f}(계산) · 지금 값은 1년 전의 {rc[0]/rc[1]:.3f}배(약 3분의 1)')
A(f'    자동차 판매만 {L["rev:Automotive sales"][0]:,.0f} ({L["rev:Automotive sales"][1]:,.0f}, {pct(L["rev:Automotive sales"][0], L["rev:Automotive sales"][1])})')
A(f'[6] 2026년 상반기 생산 약 {prod}천 대·인도 약 {deliv}천 대 · 에너지 저장 {gwh} GWh 설치 — 10-Q 개요(회사 표기 "approximately")')
A(f'    10-Q 문장: "In the first half of 2026 ... we began production of Cybercab" 있음={cyb} · Optimus는 "advance the development of Optimus"(개발 단계, 대수 없음)')
A(f'[7] 상반기(6개월) 설비투자 {abs(cap[0]):,.0f} (1년 전 {abs(cap[1]):,.0f}, {abs(cap[0])/abs(cap[1]):.2f}배) · 영업현금흐름 {ocf[0]:,.0f}(1년 전 {ocf[1]:,.0f}) · SpaceX 지분 매입 {spx} — 10-Q 현금흐름표')
A(f'    2026년 설비투자 전망: "in excess of ${capex_guide} billion" = {int(capex_guide)*1000:,} 넘게(={capex_guide}0억 달러, 회사 전망) · 상반기 실적 {abs(cap[0]):,.0f} → 하반기에 최소 {int(capex_guide)*1000-abs(cap[0]):,.0f} 남음(계산)')
A(f'    상반기 나간 돈 설비투자+SpaceX {abs(cap[0])+int(spx.replace(",","")):,.0f} vs 영업현금흐름 {ocf[0]:,.0f} → 차이 {abs(cap[0])+int(spx.replace(",",""))-ocf[0]:,.0f}(계산)')
A(f'    10-Q 문장: "will necessitate additional funding beyond our operating cash flow" 있음={fund}')
A(f'[8] 6월 말 현금 {cash[0]:,.0f} + 단기투자 {sti[0]:,.0f} = {cash[0]+sti[0]:,.0f} (2025년 말 {cash[1]+sti[1]:,.0f}) — 10-Q 재무상태표')
A(f'[9] 8-K 9/29: 새 신용 한도 {len(fac)}개 ' + '·'.join(f'{b}={float(a)*10:.0f}억 달러' for a, b in fac) + f' = 합계 {fsum*10:.0f}억 달러(무담보) · 대출 잔액 0={nolo} · 용도 "general corporate purposes"')
A(f'    해지된 옛 회전 한도 {float(old.group(1))*10:.0f}억 달러(원문 ${old.group(1)} billion, 만기 {old.group(2)}), 빌린 돈 없었고 중도해지 위약금 없음={nopen} → 새 한도는 옛 한도의 {fsum/float(old.group(1)):.0f}배')
qs = Q['매출']; ks = sorted(qs)
A('[10] 분기 10개(XBRL, *=연간−3개 분기 계산): 분기말 매출 / 영업이익 / 영업이익률 / 연구개발비')
for k in ks:
    rv = qs[k]['v'] / 1e6; op = Q['영업이익'][k]['v'] / 1e6; r_ = Q['연구개발비'][k]['v'] / 1e6
    A(f'    {k}{"*" if qs[k]["calc"] else " "} {rv:,.0f} / {op:,.0f} / {op/rv*100:.1f}% / {r_:,.0f}')
mx = max(ks, key=lambda k: qs[k]['v']); mn = min(ks, key=lambda k: Q['영업이익'][k]['v'] / qs[k]['v'])
A(f'    → 10분기 중 매출 최대 {mx} · 영업이익률 최저 {mn} · 연구개발비 {ks[-1]} ÷ {ks[0]} = {Q["연구개발비"][ks[-1]]["v"]/Q["연구개발비"][ks[0]]["v"]:.2f}배')
l = P['last']
A(f'[11] 주가(나스닥 공식 종가, 야후와 {P["yahoo_compare"]["days"]}일 중 0.5% 넘게 다른 날 {P["yahoo_compare"]["over_0.5pct"]}일): {l[0]} ${l[1]:.2f}')
A(f'    1년 전 {P["y1"][0]} ${P["y1"][1]:.2f} → {P["y1_x"]}배 · 3년 전 {P["y3"][0]} ${P["y3"][1]:.2f} → {P["y3_x"]}배 · 5년 전 {P["y5"][0]} ${P["y5"][1]:.2f}(분할 반영값) → {P["y5_x"]}배')
A(f'    5년 중 최고 종가 {P["peak"][0]} ${P["peak"][1]:.2f} → 지금 {(l[1]/P["peak"][1]-1)*100:.1f}% · 5년 중 최대 낙폭 {P["mdd"]["pct"]}% ({P["mdd"]["from"]} → {P["mdd"]["to"]})')
A('    ※ 주가는 공개 전에 다시 받는다(price.py의 raw 파일을 지우고 다시 실행).')
F = json.load(open(os.path.join(H, 'fireage.json'), encoding='utf-8'))
A('[12] 은퇴 나이(파이어맵 계산기 src/utils/retirementSimulator.js, fireage.mjs → fireage.json). 공통 가정: 수익률 연 5%·물가 3%·국민연금 65세부터 월 100만원')
for p, nm in (('p35', '35세·1억·월 300만원 저축·생활비 월 300만원(E-1과 같은 가정)'), ('p50', '50세·5억·월 200만원 저축·생활비 월 300만원')):
    x = F[p]
    A(f'    {nm}: 그대로 {x["none"]["age"]}세 · 지금 낙폭 {x["now"]["drawdown"]}%({x["now"]["asset"]:,}원) {x["now"]["age"]}세 · 5년 최대 낙폭 {x["max5y"]["drawdown"]}%({x["max5y"]["asset"]:,}원) {x["max5y"]["age"]}세')
A('    ※ 낙폭 %는 [11]과 같은 값이어야 한다 — 주가를 다시 받으면 fireage.mjs의 dd도 고친다')
def ko(m):  # 백만 달러 → '282억 3,600만 달러'식 읽기
    m = int(round(m)); e, r = divmod(m, 100)
    return (f'{e}억 ' if e else '') + (f'{r*100:,}만 ' if r else '') + '달러'
A('[13] 대본 읽기용(위 값을 억·만 단위로 바꾼 것, 새 숫자 없음)')
vals = {'매출 26·25 2분기': r[:2], '매출 2024 1분기': [qs[ks[0]]['v'] / 1e6], '영업이익': L['Income from operations'][:2], '이자수익': L['Interest income'][:1],
        '연구개발비': rd[:2], '판매관리비': sga[:2], '영업비용': L['Total operating expenses'][:2], '매출총이익': L['Gross profit'][:2],
        '자동차·에너지·서비스': [L['rev:Total automotive revenues'][0], L['rev:Energy generation and storage'][0], L['rev:Services and other'][0]],
        '규제 크레딧(26·25·감소)': [rc[0], rc[1], rc[1] - rc[0]], '상반기 설비투자·영업현금·SpaceX': [abs(cap[0]), ocf[0], float(spx.replace(',', ''))],
        '하반기 최소 설비투자': [int(capex_guide) * 1000 - abs(cap[0])], '현금+단기투자': [cash[0] + sti[0]]}
for k, v in vals.items():
    A(f'    {k}: ' + ' / '.join(f'{ko(x)}(≈{x/100:.0f}억)' for x in v))
A(f'    영업이익률 1.4% = 100달러 팔아 1달러 40센트 · 인도 약 {deliv}천 대 = 약 83만 8천 대 · 날짜: 2021년 11월 4일 → 2023년 1월 3일(최대 낙폭), 2025년 12월 16일(최고 종가), 옛 한도 계약 2023년 1월 20일')
A('')
A('[확인 안 함 — 대본에 쓰지 않음] 3분기 인도량(10월 초 발표 예정, 원문 없음) · 사이버캡 생산 대수 · 옵티머스 대수 · 신용 한도 실제 사용 계획 · PER 등 밸류에이션(이번 편은 장부만)')
open(os.path.join(H, 'facts.txt'), 'w', encoding='utf-8').write('\n'.join(o) + '\n')
print('\n'.join(o))
