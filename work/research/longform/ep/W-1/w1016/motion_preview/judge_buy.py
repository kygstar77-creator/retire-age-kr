# W-1 2화 2장 BuybackDays — 제미나이 심사(2026-10-15 motion). 판 board_buy.png(줄마다 스틸 2장, 시간 순). ask()는 G-1 judge_asym.py 재사용.
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); G = os.path.abspath(os.path.join(H, '..', '..', '..', 'G-1', 'motion_preview'))
sys.path.insert(0, G)
src = open(os.path.join(G, 'judge_asym.py'), encoding='utf-8').read().split('\nQ = ')[0]
exec(src)
Q = open(os.path.join(H, 'judge_buy_q.txt'), encoding='utf-8').read()
m, out = ask(Q, [os.path.join(H, 'board_buy.png')])
open(os.path.join(H, 'gemini_buy.md'), 'w', encoding='utf-8').write(f'## 점수({m})\n{out}\n'); print(m); print(out)
