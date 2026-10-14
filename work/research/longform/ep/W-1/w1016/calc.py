# -*- coding: utf-8 -*-
"""W-1 2화 숫자 — 수요일 10/14 마감 기준 (youtube-loop 2026-10-15)
코스피·환율·SPY = core_out.txt(weekcore.py 2026-10-16 --cut 2026-10-14) 그대로 읽음.
여기서 더하는 것: 삼성전자 100주(다음 금융 = KRX 정규장 종가), SK하이닉스 하루 등락, 삼성 자사주 취득결과(DART 20261012000421),
SK하이닉스 IR 일정(DART 20261014800385), 미국 9월 CPI(BLS API CUUR0000SA0·부문 / FRED CPIAUCNS·CPIAUCSL·CPILFESL).
사용: py -3.12 calc.py  → calc_out.txt"""
import json, csv, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(H, 'raw')
out = []
def p(k, v): out.append(f'{k} = {v}')

# 0. core_out(코스피·환율·SPY)
for line in open(os.path.join(H, 'core_out.txt'), encoding='utf-8'):
    if line.startswith('['): out.append(line.rstrip('\n'))

# 1. 삼성전자 100주 · 하이닉스 (다음 금융 일별 = KRX 정규장 종가)
def daum(code):
    return {r['date'][:10]: r['tradePrice'] for r in json.load(open(os.path.join(R, f'daum_{code}.json'), encoding='utf-8'))['data']}
S = daum('A005930'); X = daum('A000660')
s0, s1 = S['2026-10-08'], S['2026-10-14']
p('[A1] 삼성전자 종가 2026-10-08(원)', int(s0)); p('[A2] 삼성전자 종가 2026-10-14(원)', int(s1))
p('[A3] 삼성전자 주간(%)', round((s1 / s0 - 1) * 100, 2)); p('[A4] 100주 평가액 차이(원)', int((s1 - s0) * 100))
p('[A5] 100주 평가액 2026-10-08 → 2026-10-14(원)', f'{int(s0*100):,} → {int(s1*100):,}')
for d in ['2026-10-12', '2026-10-13', '2026-10-14']: p(f'[A6] 삼성전자 종가 {d}', int(S[d]))
x0, x1 = X['2026-10-08'], X['2026-10-14']
p('[H1] SK하이닉스 종가 2026-10-08 → 2026-10-14(원)', f'{int(x0):,} → {int(x1):,}'); p('[H2] SK하이닉스 주간(%)', round((x1 / x0 - 1) * 100, 2))
p('[H4] SK하이닉스 종가 10/12·10/13(원)', f"{int(X['2026-10-12']):,} · {int(X['2026-10-13']):,}"); p('[H3] SK하이닉스 10/13 하루(%)', round((X['2026-10-13'] / X['2026-10-12'] - 1) * 100, 2))

# 2. 삼성 자사주 취득결과보고서
t = open(os.path.join(R, 'dart_20261012000421.xml'), 'rb').read().decode('utf-8', 'ignore')
t = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', t))
m = re.search(r'계 - ([\d,]+) ([\d,]+) ([\d,]+) ([\d,]+)', t)
qty, avg, tot = int(m.group(2).replace(',', '')), int(m.group(3).replace(',', '')), int(m.group(4).replace(',', ''))
p('[B1] 자사주 취득기간(체결일)', '2026-08-24 ~ 2026-10-06 (주요사항보고서 2026-08-21)')
p('[B2] 취득 수량(주)', f'{qty:,}'); p('[B3] 1주당 취득가액 평균(원, 수수료 제외)', f'{avg:,}'); p('[B4] 취득가액 총액(원)', f'{tot:,}')
p('[B5] 10/14 종가 vs 평균 취득가(%)', round((s1 / avg - 1) * 100, 2))
p('[B6] 평균 취득가로 100주(원)', f'{avg*100:,}'); p('[B7] 10/14 종가로 100주(원)', f'{int(s1*100):,}')
own = re.search(r'보통주식 ([\d,]+) ([\d.]+) ([\d,]+) 0 0 0', t)
p('[B8] 취득 후 자기주식 보통주(주·%, 2026-10-12 현재)', f'{own.group(1)} · {own.group(2)}%'); p('[B12] 자기주식 전체 장부가 ÷ 주식 수(원, 수수료 포함 장부금액)', round(int(own.group(3).replace(',', '')) * 1e6 / int(own.group(1).replace(',', ''))))
days = re.findall(r'2026년 (\d\d)월 (\d\d)일 보통주식 ([\d,]+) ([\d,]+) ([\d,]+)', t)
lo = min(days, key=lambda d: int(d[4].replace(',', ''))); hi = max(days, key=lambda d: int(d[4].replace(',', '')))
p('[B9] 취득 거래일 수', len(days)); p('[B11] 하루 평균단가가 10/14 종가 이하인 날 수', sum(int(d[4].replace(',', '')) <= s1 for d in days)); p('[B10] 하루 평균단가 최저·최고(원)', f'{lo[0]}/{lo[1]} {lo[4]} · {hi[0]}/{hi[1]} {hi[4]}')

# 3. 하이닉스 IR
p('[I1] SK하이닉스 3분기 경영실적 발표(컨퍼런스콜)', '2026-10-28 09:00 (DART 20261014800385, 결정 2026-10-14)')

# 4. 미국 9월 CPI
F = {r['observation_date']: r for r in csv.DictReader(open(os.path.join(R, 'fred_cpi.csv'), encoding='utf-8'))}
g = lambda d, k: float(F[d][k])
p('[C1] CPI(CPIAUCNS) 2025-09 → 2026-09', f"{F['2025-09-01']['CPIAUCNS']} → {F['2026-09-01']['CPIAUCNS']}")
p('[C2] 1년 상승률(%, 비계절조정)', round((g('2026-09-01', 'CPIAUCNS') / g('2025-09-01', 'CPIAUCNS') - 1) * 100, 1))
p('[C3] 8월 1년 상승률(%)', round((g('2026-08-01', 'CPIAUCNS') / g('2025-08-01', 'CPIAUCNS') - 1) * 100, 1))
p('[C4] 전월 대비(%, 계절조정 CPIAUCSL)', round((g('2026-09-01', 'CPIAUCSL') / g('2026-08-01', 'CPIAUCSL') - 1) * 100, 1))
CO = {(x['year'], x['period']): float(x['value']) for x in json.load(open(os.path.join(R, 'bls_core.json'), encoding='utf-8'))['Results']['series'][0]['data'] if x['value'] not in ('-', '')}
p('[C5] 식품·에너지 뺀 근원 1년 상승률(%, 비계절조정 BLS CUUR0000SA0L1E 2025-09 → 2026-09)', f"{CO[('2025','M09')]} → {CO[('2026','M09')]} · {round((CO[('2026','M09')] / CO[('2025','M09')] - 1) * 100, 1)}")
B = json.load(open(os.path.join(R, 'bls_parts.json'), encoding='utf-8'))
nm = {'CUUR0000SETB01': '[C6] 휘발유', 'CUUR0000SA0E': '[C7] 에너지', 'CUUR0000SAF1': '[C8] 식품', 'CUUR0000SAH1': '[C9] 주거'}
for s in B['Results']['series']:
    if s['seriesID'] not in nm: continue
    v = {(x['year'], x['period']): float(x['value']) for x in s['data'] if x['value'] not in ('-', '')}
    p(f"{nm[s['seriesID']]} 1년 상승률(%, 비계절조정 {s['seriesID']})", round((v[('2026', 'M09')] / v[('2025', 'M09')] - 1) * 100, 1))
p('[C10] 발표', '미국 노동통계국(BLS) 2026-10-14 08:30 미 동부 = 한국 21:30 · 수치는 BLS API·FRED 2026-10-15 04:4x 조회')

# 5. 다음 주 일정 (1화 calc_out [G2][G3] 재사용 — 각 기관 일정표)
p('[G2] 한국은행 금통위', '2026-10-22'); p('[G3] FOMC', '2026-10-27~28')

# 5-1. 두 주 이어서(1화 기준일 10/2) · SPY 발표 날 하루
EC = json.load(open(os.path.join(R, 'ecos_d_20261016.json'), encoding='utf-8'))['data']['802Y001']; KO = dict((t, v) for t, v in EC)
two = KO['20261014'] / KO['20261002'] - 1
p('[D5] 코스피 10/2 → 10/14(%)', round(two * 100, 2)); p('[D6] 같은 1천만원 두 주 이어서 차이(원)', round(10_000_000 * two)); p('[D7] 1화 −539,440 + 2화 차이 단순 합(원)', -539440 + round(10_000_000 * (KO['20261014'] / KO['20261008'] - 1)))
j = json.load(open(os.path.join(R, 'yh_SPY.json')))['chart']['result'][0]; tz = j['meta']['gmtoffset']
import datetime as _dt
spy = {_dt.datetime.fromtimestamp(t + tz, _dt.UTC).strftime('%Y-%m-%d'): v for t, v in zip(j['timestamp'], j['indicators']['quote'][0]['close']) if v}
p('[F6] SPY 10/13 → 10/14 종가', f"{spy['2026-10-13']:.2f} → {spy['2026-10-14']:.2f} ({(spy['2026-10-14']/spy['2026-10-13']-1)*100:.2f}%)")
p('[F7] yh_SPY 받은 시각(야후 regularMarketTime, 한국)', _dt.datetime.fromtimestamp(j['meta']['regularMarketTime']).strftime('%Y-%m-%d %H:%M'))

# 5-2. 1화 비교(../calc_out.txt 그대로) · 1년 전 3분기 배당 결의일
for l in open(os.path.join(H, '..', 'calc_out.txt'), encoding='utf-8'):
    if l.startswith(('[D3]', '[D4]', '[F2]', '[F5]', '[G5]')): out.append('[1화] ' + l.rstrip())
# 6. 셋 나란히(반올림 말용)
k = {l.split(' = ')[0]: l.split(' = ')[1] for l in out}
p('[S1] 삼성 100주 만원', round(int((s1 - s0) * 100) / 1e4))
p('[S2] 코스피 1천만원 만원', k['[S4] 코스피 1천만원 차이 만원(반올림)'])
p('[S3] 미국 1만달러 원화 만원(소수 1)', round(int(k['[F5] 원화 차이(원)']) / 1e4, 1))
k = {l.split(' = ')[0]: l.split(' = ')[1] for l in out}
base3 = s0 * 100 + 10_000_000 + int(k['[F3] 1만 달러 SPY 원화 2026-10-08(원)'])
d3 = int((s1 - s0) * 100) + int(k['[D4] 코스피 그대로 1천만원 차이(원)']) + int(k['[F5] 원화 차이(원)'])
p('[S5] 세 칸 모두(100주+1천만원+1만달러) 10/8 평가액 → 차이(원·%)', f'{int(base3):,} → {d3:,} ({d3 / base3 * 100:.2f}%)')
open(os.path.join(H, 'calc_out.txt'), 'w', encoding='utf-8').write('# W-1 2화 calc_out (calc.py)\n' + '\n'.join(out) + '\n')
print('\n'.join(out))
