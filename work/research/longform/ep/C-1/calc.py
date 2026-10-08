# -*- coding: utf-8 -*-
"""C-1 계산 — '3억으로 매달 손에 쥐는 돈 N만원: 배당으로 받는 사람 vs 팔아서 쓰는 사람, 몇 년 버티나'.
숫자는 facts.txt 줄 번호에서 온다. 결과는 calc_out.txt(대본·화면 자막은 이 파일만 본다).

가정(대본·화면에 그대로 밝힌다):
 - 두 사람 모두 같은 미국 대형주 지수(S&P500, 배당 재투자 총수익 지수 ^SP500TR)에 넣었다고 놓는다.
   → 투자 결과는 똑같고 '돈을 꺼내는 방식'만 다르다. 상품 비교가 아니다.
 - 해마다 1월 초에 1년 치를 한 번에 꺼낸다(단순화). 꺼내는 돈은 해마다 같다(물가 반영 안 함).
 - 원화 수익률 = (1+달러 수익률) × (연말 환율 ÷ 전년 연말 환율) − 1 (ECOS 731Y004 말일자료, facts [F2]).
 - 팔아서 쓰는 사람(B): 해외 상장 주식 양도차익 22%(국세 20%+지방 2%), 연 250만원 기본공제(facts [T2]).
   양도차익은 원화 기준 평균 매입가로 계산. 양도소득은 지역 건보료 소득에 안 들어감(facts [H1]).
 - 배당으로 받는 사람(A): 꺼내는 돈 전부가 분배금 — 미국 원천징수 15%(facts [T1]).
   연 분배 1,000만원 넘으면 지역 건보료 소득에 전액 합산: 분배 × 7.19% × (1+0.9448/7.19)(facts [H1]).
   연 2,000만원 넘으면 종합과세·피부양자 탈락 선 — 추가 세금은 다른 소득에 따라 달라 계산 안 함(표시만).
 - 재산분 건보료·다른 소득은 두 사람이 같다고 보고 '더 내는 몫'만 셈.
"""
import json, math, pathlib, datetime as dt

HERE = pathlib.Path(__file__).resolve().parent
RAW = HERE / 'raw'

# [F1] S&P500 총수익 지수 연말 종가 (야후 ^SP500TR 일별, raw/yahoo_SP500TR_1d_20261008.json)
j = json.load(open(RAW / 'yahoo_SP500TR_1d_20261008.json'))['chart']['result'][0]
ye = {}
for t, v in zip(j['timestamp'], j['indicators']['quote'][0]['close']):
    if v:
        ye[dt.datetime.fromtimestamp(t, dt.UTC).year] = v
# [F2] 원/달러 연말(말일자료, ECOS 731Y004)
fx = {int(r['TIME']): float(r['DATA_VALUE']) for r in json.load(open(RAW / 'ecos_731Y004_A_1988_2025.json', encoding='utf-8'))
      if r['ITEM_NAME2'] == '말일자료'}

YEARS = list(range(1989, 2026))          # 꽉 찬 해만(2026은 10월까지라 뺌)
R_USD = {y: ye[y] / ye[y - 1] - 1 for y in YEARS}
R_KRW = {y: (1 + R_USD[y]) * fx[y] / fx[y - 1] - 1 for y in YEARS}


def geo(rs):
    return math.prod(1 + r for r in rs) ** (1 / len(rs)) - 1


G_USD, G_KRW = geo(R_USD.values()), geo(R_KRW.values())

HEALTH = 0.0719 * (1 + 0.9448 / 7.19)   # [H1]
TAX_DIV, TAX_GAIN, DEDUCT = 0.15, 0.22, 2_500_000   # [T1][T2]
LINE1, LINE2 = 10_000_000, 20_000_000


def gross_div(net, health=True):
    """A: 손에 net 쥐려면 분배 얼마. 건보 붙으면 (1−15%−8.13%)."""
    g = net / (1 - TAX_DIV)
    if health and g > LINE1:
        g = net / (1 - TAX_DIV - HEALTH)
    return g


def sell_for(net, value, basis):
    """B: 손에 net 쥐려면 얼마 팔아야 하나 (평균 매입가, 기본공제 250만원). 반환 (판 돈, 세금, 판 만큼 줄어든 매입가)."""
    gain_ratio = max(0.0, 1 - basis / value)
    lo, hi = net, net * 1.5 + DEDUCT
    for _ in range(80):
        s = (lo + hi) / 2
        tax = TAX_GAIN * max(0.0, s * gain_ratio - DEDUCT)
        lo, hi = (s, hi) if s - tax < net else (lo, s)
    s = hi
    return s, TAX_GAIN * max(0.0, s * gain_ratio - DEDUCT), basis * s / value


def run(p0, net_year, returns, mode, tax=True, health=True, cap=100):
    """returns: 해마다 수익률 목록. 고갈되면 그 해(몇 번째 해에 원하는 돈을 다 못 꺼냈나), 아니면 None.
    반환 (고갈 연차 or None, 버틴 해 수, 끝 잔액, 첫해 세금+건보, 첫해 판·받은 세전 금액)."""
    v, basis = p0, p0
    first = None
    for i, r in enumerate(returns[:cap], 1):
        if mode == 'A':
            g = gross_div(net_year, health) if tax else net_year
            cost = g - net_year
        else:
            if tax:
                g, cost, used = sell_for(net_year, v, basis)
            else:
                g, cost, used = net_year, 0.0, basis * net_year / v
            basis -= used if v > 0 else 0
        if first is None:
            first = (cost, g)
        if g > v:
            return i, i - 1, 0, first
        if mode == 'A':
            basis *= (v - g) / v
        v -= g
        v *= 1 + r
        basis = min(basis, v) if mode == 'A' else basis
    return None, min(len(returns), cap), v, first


def eok(x):
    return f'{x / 1e8:.2f}억원'


def won(x):
    return f'{x:,.0f}원'


out = []
w = out.append
w('# C-1 calc_out (calc.py) — 지수 S&P500 총수익(^SP500TR) 1989~2025년 37년 · 원화는 ECOS 연말 환율')
w(f'기하평균 연 수익률: 달러 {G_USD * 100:.2f}% · 원화 {G_KRW * 100:.2f}%  (건보+장기요양 합산율 {HEALTH * 100:.4f}%)')
w('해마다 수익률(달러 / 원화): ' + ' '.join(f'{y}:{R_USD[y] * 100:+.1f}/{R_KRW[y] * 100:+.1f}' for y in YEARS))
worst = sorted(YEARS, key=lambda y: R_KRW[y])[:5]
w('원화 기준 가장 나빴던 해 5개: ' + ', '.join(f'{y} {R_KRW[y] * 100:+.1f}%' for y in worst))

P0S = [100_000_000, 300_000_000, 500_000_000]
NETS = [1_000_000, 1_500_000, 2_000_000, 3_000_000]

w('\n## 1) 평균 수익률이 매년 똑같다고 놓을 때(원화 기하평균) — 고갈 연차 (100년 넘으면 "100년+")')
for p0 in P0S:
    for m in NETS:
        row = []
        for label, kw in [('세금 빼기 전', dict(tax=False)), ('A 배당 세금+건보', dict(mode='A')), ('A 배당 세금만', dict(mode='A', health=False)), ('B 팔기 세금', dict(mode='B'))]:
            mode = kw.pop('mode', 'B')
            k, n, end, first = run(p0, 12 * m, [G_KRW] * 100, mode, **kw)
            row.append(f'{label} {k if k else "100년+"}{"년차" if k else ""}')
        w(f'  {eok(p0)} · 월 {m // 10000}만원: ' + ' | '.join(row))

w('\n## 2) 첫해 영수증 — 손에 쥐는 돈이 같을 때 꺼내는 세전 금액과 빠지는 돈 (3억원, 평균 수익률 경로 첫해)')
for m in NETS:
    net = 12 * m
    gA = gross_div(net)
    hA = gA * HEALTH if gA > LINE1 else 0
    tA = gA * TAX_DIV
    # B 첫해: 산 직후라 차익 0 → 세금 0. 10년 평균 수익 뒤라면? 매입가 대비 평가액 2배 상황도 보여 줌
    s1, c1, _ = sell_for(net, 300_000_000, 300_000_000)
    s2, c2, _ = sell_for(net, 300_000_000, 150_000_000)
    flag = ' [연 2,000만원 넘음: 종합과세·피부양자 탈락 선, 추가세 계산 안 함]' if gA > LINE2 else ''
    w(f'  월 {m // 10000}만원(연 {won(net)}): A 분배 {won(gA)} = 미국 세금 {won(tA)} + 건보 더 냄 {won(hA)}(월 {won(hA / 12)}){flag}'
      f' | B 첫해 판 돈 {won(s1)} 세금 {won(c1)} · 평가액이 산 값의 2배일 때 판 돈 {won(s2)} 세금 {won(c2)}')

w('\n## 3) 실제 연도 순서대로(원화) — 시작한 해별 고갈 연차. 자료가 끝날 때까지 안 떨어지면 "N년 넘게(자료 끝, 남은 돈)"')
for p0 in P0S:
    for m in NETS:
        for mode in ['A', 'B']:
            res = []
            for s in YEARS:
                rs = [R_KRW[y] for y in YEARS if y >= s]
                k, n, end, _ = run(p0, 12 * m, rs, mode)
                res.append((s, k, n, end))
            dep = [(s, k) for s, k, n, e in res if k]
            line = f'  {eok(p0)} · 월 {m // 10000}만원 · {mode}: 고갈된 시작 해 {len(dep)}/{len(res)}'
            if dep:
                fastest = min(dep, key=lambda x: x[1])
                line += f' · 가장 빨리 {fastest[0]}년 시작 → {fastest[1]}년차'
            line += ' · ' + ' '.join(f'{s}:{k if k else str(n) + "+"}' for s, k, n, e in res)
            w(line)

w('\n## 4) 같은 해 시작 비교(3억원) — 고갈 연차 또는 자료 끝 잔액')
for m in [1_500_000, 2_000_000, 3_000_000]:
    for s in [1989, 1995, 2000, 2008, 2009, 2013]:
        rs = [R_KRW[y] for y in YEARS if y >= s]
        rsu = [R_USD[y] for y in YEARS if y >= s]
        parts = []
        for mode in ['A', 'B']:
            k, n, end, _ = run(300_000_000, 12 * m, rs, mode)
            parts.append(f'{mode} ' + (f'{k}년차 바닥' if k else f'{n}년 버팀·2025년 말 {eok(end)}'))
        k, n, end, _ = run(300_000_000, 12 * m, rsu, 'B')
        parts.append('B 환율 뺌(달러 수익률) ' + (f'{k}년차 바닥' if k else f'{n}년 버팀·{eok(end)}'))
        w(f'  월 {m // 10000}만원 · {s}년 시작: ' + ' | '.join(parts))

(HERE / 'calc_out.txt').write_text('\n'.join(out) + '\n', encoding='utf-8')
print('\n'.join(out))


def path(p0, net_year, returns, mode):
    """해마다 연말 잔액 목록(바닥나면 0에서 멈춤)."""
    v, basis, out = p0, p0, []
    for r in returns:
        if mode == 'A':
            g = gross_div(net_year)
        else:
            g, _, used = sell_for(net_year, v, basis)
            basis -= used
        if g > v:
            out.append(0)
            break
        if mode == 'A':
            basis *= (v - g) / v
        v = (v - g) * (1 + r)
        out.append(v)
    return out


out3 = ['\n## 5) 20년 안에 바닥났나 — 20년 치 자료가 있는 시작 해 1989~2006(18개)만 (공정 비교)']
for p0 in P0S:
    for m in NETS:
        cnt = {}
        for mode in ['A', 'B']:
            c = 0
            for s in range(1989, 2007):
                rs = [R_KRW[y] for y in YEARS if y >= s][:20]
                k, *_ = run(p0, 12 * m, rs, mode)
                c += 1 if k else 0
            cnt[mode] = c
        out3.append(f'  {eok(p0)} · 월 {m // 10000}만원: 20년 안에 바닥 — 배당 {cnt["A"]}/18 · 팔기 {cnt["B"]}/18')
out3.append('\n## 6) 해마다 연말 잔액(3억원 · 월 200만원)')
for s in [2000, 2008]:
    rs = [R_KRW[y] for y in YEARS if y >= s]
    for mode in ['A', 'B']:
        pth = path(300_000_000, 24_000_000, rs, mode)
        out3.append(f'  {s}년 시작 {mode}: ' + ' '.join(f'{s + i}:{x / 1e8:.2f}' for i, x in enumerate(pth)))
(HERE / 'calc_out.txt').open('a', encoding='utf-8').write('\n'.join(out3) + '\n')
print('\n'.join(out3))
