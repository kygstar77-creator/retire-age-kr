# P-3 가로식 장면 셋(EqRow plain) — 제미나이 심사(2026-10-27 motion). ask()는 G-1 judge_asym.py 재사용. 판 board_<k>.png
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); G = os.path.abspath(os.path.join(H, '..', '..', 'G-1', 'motion_preview'))
sys.path.insert(0, G)
exec(open(os.path.join(G, 'judge_asym.py'), encoding='utf-8').read().split('\nQ = ')[0])
D = {
 'calc': "'고지서 한 달은 얼마?'(7줄, 연금 한 달 167만원·재산 0). 식1 건강보험료: 167만원(연금 한 달) × 절반(보험료 매길 땐) × 7.19%(보험료율) = ? → '6만원 정도' 말에 주황 '약 6만원'(아래 60,037원) → 회색 줄로. 식2: 6만원 × 13.14%(장기요양) = ? → '약 8천원'(7,889원). 식3 고지서 한 달: 6만원 + 8천원 = ? → '6만 8천원쯤'에 '약 6만 8천원'(67,926원). 아래 '재산 0 가정 · 2026년 요율 · 소득분만'.",
 'rise': "'아무것도 안 해도 넘는 자리'(5줄). 식1: 165만원(올해) × 1.021(물가만큼 2.1%) = ? → '168만원 남짓'(연 2,022만원 · 기준 위). 식2 그다음 해부터 한 해: 약 6만 8천원(매달) × 12달 = ? → '80만원 넘음'(822,252원). 식3: 164만원 × 1.021 = 167.4만원(연 2,009만원 · 기준 위), 끝에 큰 먹 글자 '163만원이면 연 1,997만원 · 기준 아래' + 주황 밑줄. 아래 '가정 — 내년 인상률은 2027년 1월 발표 · 올해처럼 2.1%'.",
 'mix': "'1천만원을 넘으면 전부'(4줄). 식: 1,000만원(국민연금) + 1,100만원(이자·배당 전부) = ? → 2,100만원(기준 2,000만원 위), '매달 11만원쯤' 말에 큰 먹 글자 '탈락 · 매달 약 11만원' + 주황 밑줄. 아래 '이자·배당 1천만원 넘으면 전부 더함 · 재산 0 · 소득분만'.",
}
Q0 = open(os.path.join(H, 'judge_q.txt'), encoding='utf-8').read()
keys = sys.argv[1:] or list(D)
with open(os.path.join(H, 'gemini_row.md'), 'a', encoding='utf-8') as fo:
    for k in keys:
        m, out = ask(Q0.replace('{DESC}', D[k]), [os.path.join(H, f'board_{k}.png')])
        fo.write(f'\n## {k} ({m})\n{out}\n'); print('==', k, m); print(out)
