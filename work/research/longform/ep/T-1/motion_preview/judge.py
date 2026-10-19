# T-1 2장 가로식 장면 셋(EqRow) — 제미나이 심사(2026-10-19 motion). ask()는 G-1 judge_asym.py 재사용. 판 board_<k>.png
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); G = os.path.abspath(os.path.join(H, '..', '..', 'G-1', 'motion_preview'))
sys.path.insert(0, G)
exec(open(os.path.join(G, 'judge_asym.py'), encoding='utf-8').read().split('\nQ = ')[0])
D = {
 'ratio': "'같은 해, 세금은 몇 배?'(2줄). 한 줄 식: [1억 4,777만원](수현 씨·공제율 16%·기본공제 250만원) ÷ [1,241만원](정민 씨·공제율 80%·기본공제 2,500만원) = ? → '열두 배 가까이' 말에 주황 11.9배 + 손 동그라미. 아래 '같은 20억 집 · 2029년에 판다면 · 정부안'.",
 'year': "'살았던 한 해의 값'(3줄, 수현 씨 2029년). 식1: [1억 4,777만원](거주 2년) − [1억 3,088만원](거주 3년) = ? → '1,700만원쯤' 말에 주황 '약 1,690만원'(아래 '한 해 더 살면 줄어드는 세금'). 셋째 줄('번 돈이 클수록 한 해의 값도 커집니다')에 검은 카드 '집마다 다름 · 번 돈이 클수록 커짐'. 아래 '2029년 정부안 · 지방세 포함'.",
 'gap': "'햇수 차이 한 해마다 4%p'(3줄, 조건 줄 '거주 2년 이상 · 보유·거주 모두 10년 이하'). 식1 지금 공제율: [보유 40%](10년×4%) + [거주 8%](2년×4%) = 48% → 위 회색 줄로. 식2 낮아지는 폭: [4%p](한 해 차이마다) × [8년](보유 10년 − 거주 2년) = 32%p → 회색 줄로. 식3 2029년 공제율: [48%] − [32%p] = ? → '16%로' 말에 주황 16%.",
}
Q0 = open(os.path.join(H, 'judge_q.txt'), encoding='utf-8').read()
keys = sys.argv[1:] or list(D)
with open(os.path.join(H, 'gemini_row.md'), 'a', encoding='utf-8') as fo:
    for k in keys:
        m, out = ask(Q0.replace('{DESC}', D[k]), [os.path.join(H, f'board_{k}.png')])
        fo.write(f'\n## {k} ({m})\n{out}\n'); print('==', k, m); print(out)
