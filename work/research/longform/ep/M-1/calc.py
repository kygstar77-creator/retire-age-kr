# -*- coding: utf-8 -*-
"""M-1 거꾸로 계산 — '세후·건보료 뒤 매달 M원을 받으려면 지금 얼마를 넣어야 하나'.
숫자는 전부 facts.txt 줄 번호에서 온다. 결과는 calc_out.txt(대본·화면 자막이 이 파일만 본다).

가정(대본·화면에 그대로 밝힌다):
 - 지난 12회 실제 분배금이 앞으로도 같다고 놓은 계산이다(앞으로 같다는 뜻 아님).
 - 해외 직투(SCHD·JEPQ): 미국 원천징수 15%, 국내 추가 0(분리과세 한도 안, facts [T1]).
 - 국내 상장(ACE): 배당소득세 15.4%를 분배금 전체에 매김(과세표준이 분배금보다 작을 수 있으나 ACE 과세표준 공시는 확인 안 함 → 세금을 크게 잡은 쪽).
 - 건보료: 지역가입자, 금융소득(세전) 연 1,000만원 넘으면 전액이 소득에 들어감 → 연 금융소득 × 7.19% × (1+0.9448/7.19) (facts [H1], D-1 [1][3][6]). 재산분·다른 소득은 같다고 보고 '더 내는 몫'만 셈.
 - 연 금융소득 2,000만원(종합과세·피부양자 탈락 선)을 넘는 칸은 표시만 하고 추가 세금은 계산하지 않는다(다른 소득에 따라 달라짐).
 - 해외 상품의 원금·분배를 같은 환율로 바꾸면 비율은 환율과 무관(분배율 = 달러 분배 ÷ 달러 가격).
"""
import pathlib

HERE = pathlib.Path(__file__).resolve().parent

# facts.txt
P = {
    # 이름: (지난 12회 분배 합, 가장 적은 달 1회, 최근 종가, 횟수/년, 세율, 단위)
    'SCHD': (1.0541, None, 32.72, 4, 0.15, '달러'),      # [S1][S2]
    'JEPQ': (6.88454, 0.46572, 61.04, 12, 0.15, '달러'),  # [J1][J2]
    'ACE 미국배당다우존스': (441, 21, 14330, 12, 0.154, '원'),  # [K1][K2]
}
HEALTH = 0.0719 * (1 + 0.9448 / 7.19)   # 건보+장기요양, 연 금융소득에 곱함 (D-1 [1][3])
LINE1, LINE2 = 10_000_000, 20_000_000
TARGETS = [1_000_000, 2_000_000, 3_000_000]


def gross_needed(monthly_net, tax):
    """세후·건보 뒤 매달 monthly_net 받으려면 필요한 연 세전 분배금."""
    g = 12 * monthly_net / (1 - tax)
    if g <= LINE1:
        return g, False
    return 12 * monthly_net / (1 - tax - HEALTH), True


def won(x):
    return f'{x:,.0f}원'


def eok(x):
    return f'{x / 1e8:.2f}억원'


out = []
w = out.append
w(f'# M-1 calc_out (calc.py) — 건보+장기요양 합산율 {HEALTH * 100:.4f}%')
for name, (dist, mn, price, n, tax, unit) in P.items():
    y = dist / price
    w(f'\n## {name} — 지난 12개월 분배 {dist}{unit} ÷ 종가 {price}{unit} = 분배율 {y * 100:.2f}% · 세율 {tax * 100:.1f}% · 연 {n}회')
    # 건보 안 붙는 최대 월 세후 수령
    cap = LINE1 * (1 - tax) / 12
    w(f'  건보 안 붙는 최대(연 세전 1,000만원): 월 세후 {won(cap)} · 필요 원금 {eok(LINE1 / y)}')
    for m in TARGETS:
        g, h = gross_needed(m, tax)
        need = g / y
        flag = []
        if h:
            flag.append(f'건보 더 냄 연 {won(g * HEALTH)}(월 {won(g * HEALTH / 12)})')
        if g > LINE2:
            flag.append('연 2,000만원 넘음 → 종합과세·피부양자 탈락 선(추가세 계산 안 함)')
        line = f'  월 {m // 10000}만원: 연 세전 분배 {won(g)} → 필요 원금 {eok(need)}'
        if mn and n == 12:
            ratio = (mn * 12) / dist
            line += f' · 가장 적은 달 기준이면 {eok(need / ratio)}(×{1 / ratio:.2f})'
        w(line + ('  [' + ' · '.join(flag) + ']' if flag else ''))
    if n == 4:
        w(f'  ※ 분기 1회 — 매달이 아님: 월{TARGETS[0] // 10000}만원이면 3달마다 세후 {won(TARGETS[0] * 3)}씩 들어와 나눠 써야 함')

(HERE / 'calc_out.txt').write_text('\n'.join(out) + '\n', encoding='utf-8')
print('\n'.join(out))

# 같은 1년(2025-10-02 → 2026-10-02) 총수익 — 원화, 분배 재투자 안 함, 분배는 끝날 환율로 바꿈(근사, facts [X1])
FX0, FX1 = 1406.0, 1359.6   # ECOS 731Y001 (R-1 facts [10])
TR = {'SCHD': (27.34, 32.72, 1.0541, True), 'JEPQ': (57.29, 61.04, 6.88454, True),
      'ACE 미국배당다우존스': (12460, 14330, 441, False)}
out2 = ['\n## 1년 총수익(원화, 1억 넣었다면)']
for name, (p0, p1, d, usd) in TR.items():
    a, b = (FX0, FX1) if usd else (1, 1)
    start, end, dv = p0 * a, p1 * b, d * b
    r_price, r_tot = end / start - 1, (end + dv) / start - 1
    out2.append(f'  {name}: 가격 {r_price * 100:+.2f}% · 분배 {dv / start * 100:.2f}% · 합 {r_tot * 100:+.2f}% → 1억이 {won(1e8 * (1 + r_tot))}(세전)')
(HERE / 'calc_out.txt').open('a', encoding='utf-8').write('\n'.join(out2) + '\n')
print('\n'.join(out2))
