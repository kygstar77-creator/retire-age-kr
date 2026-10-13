# -*- coding: utf-8 -*-
"""C-2(N1 시범) 계산 — C-1 calc.py의 '팔아 쓰기(B)' 규칙만 그대로 쓴다(배당 쪽 A는 전제 불가능이라 뺌, replan_1012).
가상 인물 1명: 1998년 1월 3억원을 S&P500 총수익 지수에 넣고 해마다 1월 초 1년 치를 팔아 씀(세금 22%·공제 250만원 반영).
결과는 calc_n1_out.txt — 대본 숫자는 이 파일에서만."""
import sys, io, contextlib, pathlib
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'C-1'))
with contextlib.redirect_stdout(io.StringIO()):
    import calc as C   # C-1 calc_out.txt를 같은 값으로 다시 씀(결정적)
out = []
w = out.append
P0 = 300_000_000
def path_detail(p0, net_year, start, R):
    v, basis, rows = p0, p0, []
    for y in [y for y in C.YEARS if y >= start]:
        g, tax, used = C.sell_for(net_year, v, basis)
        if g > v:
            rows.append((y, v, None, tax)); break
        basis -= used
        v_after = (v - g) * (1 + R[y])
        rows.append((y, v, v_after, tax)); v = v_after
    return rows
w('# C-2 calc_n1_out (calc_n1.py) — 팔아 쓰기만 · 3억원 · 원화(ECOS 연말 환율) · S&P500 총수익 ^SP500TR')
for m in [200, 150]:
    for s in [1997, 1998, 2003]:
        rows = path_detail(P0, m * 120000, s, C.R_KRW)
        last = rows[-1]
        end = '바닥 ' + f'{last[0]}년(시작 {len(rows)}년차, 1월에 남은 돈 {last[1]/1e8:.2f}억원 < 1년 치)' if last[2] is None else f'2025년 말 {last[2]/1e8:.2f}억원 남음'
        w(f'\n## 월 {m}만원 · {s}년 1월 시작 → {end}')
        w('  해: 1월 남은 돈(억) → 꺼낸 뒤 그해 수익률 → 연말(억) · 그해 세금(만원)')
        for y, v0, v1, tax in rows:
            w(f'  {y}: {v0/1e8:.2f} → {C.R_KRW[y]*100:+.1f}% → ' + (f'{v1/1e8:.2f}' if v1 is not None else '못 꺼냄') + f' · 세금 {tax/1e4:.0f}')
# 총 꺼낸 돈(손에 쥔 돈) — 1998 월200
rows = path_detail(P0, 24_000_000, 1998, C.R_KRW)
n = sum(1 for r in rows if r[2] is not None)
w(f'\n## 1998 월200: 다 꺼낸 해 {n}번 · 손에 쥔 돈 합 {n*2400/10000:.2f}억원 · 마지막 해 남은 돈 {rows[-1][1]/1e4:,.0f}만원')
w(f'## 환율(ECOS 연말): 1997 {C.fx[1997]:,.1f} · 1998 {C.fx[1998]:,.1f} · 2007 {C.fx[2007]:,.1f} · 2008 {C.fx[2008]:,.1f}')
(HERE / 'calc_n1_out.txt').write_text('\n'.join(out) + '\n', encoding='utf-8')
print('\n'.join(out))

# 2) 줄였다면 — 1998년 시작, 월 200만원으로 꺼내다 어느 해부터 월 X만원으로 줄임(같은 규칙)
o2 = ['\n## 줄였다면 — 1998년 1월 시작 · 처음 월 200만원 → 그 해부터 줄임']
def run_switch(start, m1, m2, cut_year, R):
    v, basis = P0, P0
    for y in [y for y in C.YEARS if y >= start]:
        net = (m1 if y < cut_year else m2) * 120000
        g, tax, used = C.sell_for(net, v, basis)
        if g > v:
            return f'{y}년 바닥(시작 {y - start + 1}년차)'
        basis -= used
        v = (v - g) * (1 + R[y])
    return f'2025년 말 {v/1e8:.2f}억원 남음'
for cut in [2001, 2003]:
    for m2 in [150, 120, 100]:
        o2.append(f'  {cut}년부터 월 {m2}만원: ' + run_switch(1998, 200, m2, cut, C.R_KRW))
# 3) 시작 해 전부(3억·월 200만원·팔아 쓰기) — calc_out 3절 B 줄과 같은 값인지 대조
o2.append('\n## 시작 해별(3억·월 200만원·팔아 쓰기, 원화) — 바닥난 해만')
bad = []
for s in range(1989, 2026):
    k, n, end, _ = C.run(P0, 24_000_000, [C.R_KRW[y] for y in C.YEARS if y >= s], 'B')
    if k: bad.append(f'{s}년 시작 {k}년차')
o2.append('  ' + ' · '.join(bad) + f' (총 {len(bad)}/37)')
for m in [100, 150, 300]:
    c = sum(1 for s in range(1989, 2026) if C.run(P0, m * 120000, [C.R_KRW[y] for y in C.YEARS if y >= s], 'B')[0])
    o2.append(f'  월 {m}만원: 바닥난 시작 해 {c}/37')
(HERE / 'calc_n1_out.txt').open('a', encoding='utf-8').write('\n'.join(o2) + '\n')
