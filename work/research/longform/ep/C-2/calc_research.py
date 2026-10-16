# -*- coding: utf-8 -*-
"""C-2 자료조사 '우리만' 계산 (2026-10-17 C-2 자료조사 담당) — research.md ④칸 숫자는 이 출력(calc_research_out.txt)에서만.
규칙은 calc_n1.py와 같다(C-1 calc.py sell_for·run: 1월 초 1년 치 한 번에 팔기, 해외 상장 양도세 22%·연 250만원 공제, 물가 반영 안 함).
새로 받은 원자료(2026-10-16 23:5x 한국은행 ECOS API, raw/에 저장):
  raw/ecos_731Y004_M_1995_2025_1016.json  원/달러 매매기준율 말일자료(월)
  raw/ecos_731Y004_A_1995_2025_1016.json  같은 표(연) — C-1 raw와 1996·1997·1998·2002·2007·2008·2025 값 대조
  raw/ecos_121Y002_BEABAA2113_M_1016.json 예금은행 정기예금(1~2년 미만) 신규취급액 가중평균금리(월)
"""
import sys, io, json, math, contextlib, pathlib, datetime as dt
sys.stdout.reconfigure(encoding='utf-8')
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'C-1'))
with contextlib.redirect_stdout(io.StringIO()):
    import calc as C
RAW = HERE / 'raw'
P0, NET = 300_000_000, 24_000_000
out = []; w = out.append
w('# C-2 calc_research_out (calc_research.py) — 3억원 · 월 200만원(연 2,400만원) · 원화')

# 0) 원자료 대조: ECOS 연말 환율(오늘 받은 값) ↔ C-1 raw(10/8 받은 값)
fa = {int(r['TIME']): float(r['DATA_VALUE']) for r in json.load(open(RAW / 'ecos_731Y004_A_1995_2025_1016.json', encoding='utf-8'))}
diff = [y for y in fa if y in C.fx and abs(fa[y] - C.fx[y]) > 0.05]
w(f'\n## 0) ECOS 연말 환율 재수신 대조: {len([y for y in fa if y in C.fx])}개 해 비교, 다른 해 {len(diff)}개 {diff}')
w('  ' + ' · '.join(f'{y} {fa[y]:,.1f}' for y in (1996, 1997, 1998, 2002, 2007, 2008, 2011, 2025)))

# 1) 인출률
w(f'\n## 1) 인출률: 월 200만원 = 3억의 연 {NET / P0 * 100:.1f}% · 월 100만원 = 연 {12_000_000 / P0 * 100:.1f}% (4% 규칙과 같은 비율)')

# 2) 그냥 뒀다면(꺼내지 않음) — 1998년 1월 3억 → 2025년 말
v = P0 * math.prod(1 + C.R_KRW[y] for y in C.YEARS if y >= 1998)
w(f'\n## 2) 1998년 1월 3억을 한 푼도 안 꺼냈다면 2025년 말 {v / 1e8:.2f}억원 (세금 0 — 안 팔았으니) · 원화 연평균 {(v / P0) ** (1 / 28) * 100 - 100:.1f}% (28년)')
v03 = P0 * math.prod(1 + C.R_KRW[y] for y in C.YEARS if y >= 2003)
w(f'   2003년 1월 3억 안 꺼냈다면 2025년 말 {v03 / 1e8:.2f}억원 · 원화 연평균 {(v03 / P0) ** (1 / 23) * 100 - 100:.1f}% (23년)')
g98 = math.prod(1 + C.R_KRW[y] for y in range(1998, 2011)) ** (1 / 13) - 1
w(f'   정우 씨가 돈을 꺼낸 13년(1998~2010) 원화 연평균 {g98 * 100:.1f}% — 꺼내는 비율 8.0%보다 낮음')
g98u = math.prod(1 + C.R_USD[y] for y in range(1998, 2011)) ** (1 / 13) - 1
w(f'   같은 13년 달러 연평균 {g98u * 100:.1f}%')

# 3) 금고(수익 0%)에 넣고 같은 규칙
n0 = P0 // NET
w(f'\n## 3) 수익 0%(금고)라면: 1월마다 2,400만원 다 꺼낸 해 {n0}번 → {1998 + n0}년 1월 바닥(남은 돈 {(P0 - n0 * NET) / 1e4:,.0f}만원) · 정우 씨 S&P500 13번(2011년 1월 바닥) — 차이 {13 - n0}년')

# 4) 정기예금(한국은행 실제 금리)에 넣고 같은 규칙 — 1월 신규 1년 정기예금 금리를 그해 이자율로, 이자소득세 15.4%(지금 세율로 통일)
dep = {r['TIME']: float(r['DATA_VALUE']) for r in json.load(open(RAW / 'ecos_121Y002_BEABAA2113_M_1016.json', encoding='utf-8'))}
def dep_rate(y):
    k = f'{y}01'
    return dep[k] / 100 if k in dep else dep[f'{y}07'] / 100   # 1996은 7월부터만 있음
def deposit_path(start):
    v = P0; rows = []
    for y in range(start, 2026):
        if NET > v: return y, rows
        v -= NET
        r = dep_rate(y) * (1 - 0.154)
        v *= 1 + r; rows.append((y, r, v))
    return None, rows
b, rows = deposit_path(1998)
w(f'\n## 4) 정기예금(1~2년 미만, 1월 신규 금리, 세후 ×0.846) 1998년 1월 시작 → ' + (f'{b}년 1월 바닥(시작 {b - 1997}년차)' if b else f'2025년 말 {rows[-1][2] / 1e8:.2f}억원'))
w('  ' + ' · '.join(f'{y} 세후 {r * 100:.2f}% 연말 {v / 1e8:.2f}억' for y, r, v in rows))
for s in (1997, 2003):
    b2, r2 = deposit_path(s)
    w(f'  정기예금 {s}년 1월 시작 → ' + (f'{b2}년 1월 바닥(시작 {b2 - s + 1}년차)' if b2 else f'2025년 말 {r2[-1][2] / 1e8:.2f}억원'))

# 5) 매달 팔았다면(월말 지수·월말 환율) — 세금은 해마다 차익을 모아 이듬해 5월에 계좌에서 냄(250만원 공제)
j = json.load(open(HERE.parent / 'C-1' / 'raw' / 'yahoo_SP500TR_1d_20261008.json'))['chart']['result'][0]
me = {}
for t, x in zip(j['timestamp'], j['indicators']['quote'][0]['close']):
    if x:
        d = dt.datetime.fromtimestamp(t, dt.UTC); me[(d.year, d.month)] = x
fm = {(int(r['TIME'][:4]), int(r['TIME'][4:])): float(r['DATA_VALUE']) for r in json.load(open(RAW / 'ecos_731Y004_M_1995_2025_1016.json', encoding='utf-8'))}
months = [(y, m) for y in range(1988, 2026) for m in range(1, 13)]
def krw(ym): return me[ym] * fm[ym]
def monthly_path(start_year, net_m=2_000_000):
    prev = (start_year - 1, 12)
    units = P0 / krw(prev); basis = P0; gains = {}; owed = 0.0
    for ym in [x for x in months if x >= (start_year, 1)]:
        if ym not in me or ym not in fm: continue
        price = krw(prev)                       # 달 초 = 전달 말 값으로 판다
        need = net_m + (owed if ym[1] == 5 else 0)
        if ym[1] == 5: owed = 0.0
        val = units * price
        if need > val: return ym
        sell_units = need / price
        g = need - basis * sell_units / units   # 판 금액 − 판 만큼의 평균 매입가
        basis -= basis * sell_units / units; units -= sell_units
        gains[ym[0]] = gains.get(ym[0], 0) + g
        if ym[1] == 12:
            owed = 0.22 * max(0.0, gains.get(ym[0], 0) - 2_500_000)
        prev = ym
    return None
mb = monthly_path(1998)
w(f'\n## 5) 매달 1일 200만원씩 팔았다면(월말 지수·월말 환율, 세금은 이듬해 5월) 1998년 시작 → ' + (f'{mb[0]}년 {mb[1]}월 바닥' if mb else '2025년 말까지 남음'))
mcnt = [s for s in range(1996, 2026) if monthly_path(s)]   # 월말 환율 받은 구간이 1995-12부터
acnt = [s for s in range(1996, 2026) if C.run(P0, NET, [C.R_KRW[y] for y in C.YEARS if y >= s], 'B')[0]]
w(f'   같은 30개 시작 해(1996~2025) 중 바닥 — 매달 팔기 {len(mcnt)}개: ' + ' · '.join(str(s) for s in mcnt) + f' / 1월 한 번에 팔기 {len(acnt)}개: ' + ' · '.join(str(s) for s in acnt))

# 6) 국내 상장 S&P500 ETF로 했다면 — 판 이익이 배당소득(15.4%, 공제 없음), 그해 판 이익 1,000만원 넘으면 건보료(전액 × 합산율) 같은 해에 냄(단순화)
HEALTH = C.HEALTH
def sell_kr(net, value, basis):
    gr = max(0.0, 1 - basis / value); lo, hi = net, net * 1.6
    for _ in range(80):
        s = (lo + hi) / 2; gain = s * gr
        cost = 0.154 * gain + (HEALTH * gain if gain > 10_000_000 else 0)
        lo, hi = (s, hi) if s - cost < net else (lo, s)
    s = hi; gain = s * gr
    return s, 0.154 * gain + (HEALTH * gain if gain > 10_000_000 else 0), basis * s / value
def run_kr(start, net=NET):
    v, basis = P0, P0
    for i, y in enumerate([y for y in C.YEARS if y >= start], 1):
        g, cost, used = sell_kr(net, v, basis)
        if g > v: return i
        basis -= used; v = (v - g) * (1 + C.R_KRW[y])
    return None
kb = [s for s in range(1989, 2026) if run_kr(s)]
w(f'\n## 6) 국내 상장 ETF 과세(판 이익 15.4%·공제 없음·1,000만원 넘으면 건보료) · 월 200만원 · 시작 해 37개 중 바닥 {len(kb)}개: ' + ' · '.join(f'{s}({run_kr(s)}년차)' for s in kb))
w(f'   1998년 시작 → {1997 + run_kr(1998)}년 1월 바닥(해외 상장 22% 규칙과 같은 해인지 대조)')
def end_val(start, kr):
    v, basis = P0, P0
    for y in [y for y in C.YEARS if y >= start]:
        g, cost, used = (sell_kr if kr else C.sell_for)(NET, v, basis)
        if g > v: return None
        basis -= used; v = (v - g) * (1 + C.R_KRW[y])
    return v
for s in (1997, 2003):
    a, b_ = end_val(s, False), end_val(s, True)
    w(f'   {s}년 시작 2025년 말: 해외 상장 {a / 1e8:.2f}억 · 국내 상장 {b_ / 1e8:.2f}억 (차이 {(a - b_) / 1e8:.2f}억)')

# 7) '평생'은 얼마나 — 2024년 생명표(국가데이터처 2025-12-03 발표) 60세 기대여명 남 23.7년 · 여 28.4년
for label, yrs in (('남 60세 기대여명 23.7년 → 24번 꺼내기', 24), ('여 60세 기대여명 28.4년 → 29번 꺼내기', 29)):
    obs = [s for s in range(1989, 2026) if s + yrs - 1 <= 2025]
    for m in (100, 150, 200):
        ok = [s for s in obs if not (lambda k: k and k <= yrs)(C.run(P0, m * 120000, [C.R_KRW[y] for y in C.YEARS if y >= s], 'B')[0])]
        w(f'\n## 7) {label} · 월 {m}만원: 끝까지 볼 수 있는 시작 해 {len(obs)}개({obs[0]}~{obs[-1]}) 중 {len(ok)}개가 버팀, 못 버틴 해 ' + ', '.join(str(s) for s in obs if s not in ok))
(HERE / 'calc_research_out.txt').write_text('\n'.join(out) + '\n', encoding='utf-8')
print('\n'.join(out))

# 8) 그래서 — '1월에 통장이 처음 넣은 3억보다 적으면 그해만 월 100만원' 규칙(가드레일). 시청자 한 사람: 3억·월 200만원
o8 = []
def guard(start, line=P0, low=12_000_000, high=NET):
    v, basis, got, cut = P0, P0, 0, 0
    for y in [y for y in C.YEARS if y >= start]:
        net = low if v < line else high
        cut += net == low
        g, tax, used = C.sell_for(net, v, basis)
        if g > v: return y, got, cut, None
        basis -= used; got += net; v = (v - g) * (1 + C.R_KRW[y])
    return None, got, cut, v
for line_ratio in (1.0, 0.8):
    res = {s: guard(s, P0 * line_ratio) for s in range(1989, 2026)}
    bad = [s for s, r in res.items() if r[0]]
    o8.append(f'\n## 8) 규칙: 1월 통장이 {line_ratio * 3:.1f}억 아래면 그해 월 100만원(아니면 200만원) · 37명 중 바닥 {len(bad)}명 ' + ' · '.join(map(str, bad)))
    for s in (1998, 2003, 1997):
        b, got, cut, end = res[s]
        o8.append(f'   {s}년 시작: ' + (f'{b}년 바닥' if b else f'2025년 말 {end / 1e8:.2f}억원 남음') + f' · 손에 쥔 돈 {got / 1e8:.2f}억원 · 줄인 해 {cut}번')
# 비교: 줄이지 않은 정우 씨 손에 쥔 돈 3.12억(13번)
(HERE / 'calc_research_out.txt').open('a', encoding='utf-8').write('\n'.join(o8) + '\n')
print('\n'.join(o8))

# 9) 대본 1장 '왜 1억 7천까지밖에' — 1998년 시작 정우 씨 2003년 1월 꺼낸 뒤 남은 돈
v, basis = P0, P0
for y in [y for y in C.YEARS if y >= 1998]:
    g, tax, used = C.sell_for(NET, v, basis)
    basis -= used
    if y == 2003:
        line9 = f'\n## 9) 정우 씨 2003년 1월: 꺼내기 전 {v / 1e8:.2f}억 → 꺼낸 뒤 {(v - g) / 1e8:.2f}억원 → 원화 {C.R_KRW[y] * 100:+.1f}% → 연말 {(v - g) * (1 + C.R_KRW[y]) / 1e8:.2f}억원'
        break
    v = (v - g) * (1 + C.R_KRW[y])
(HERE / 'calc_research_out.txt').open('a', encoding='utf-8').write(line9 + '\n'); print(line9)
