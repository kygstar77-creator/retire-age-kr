# P-1 5장 '519만원 위의 계단' StepCliff — 제미나이 심사(2026-10-13 motion). 판 board_step.png 한 장(줄마다 스틸 15장, 시간 순).
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(H, '..', '..', 'G-1', 'motion_preview')))
import importlib.util
spec = importlib.util.spec_from_file_location('ja', os.path.join(H, '..', '..', 'G-1', 'motion_preview', 'judge_asym.py'))
src = open(spec.origin, encoding='utf-8').read().split('\nQ = ')[0]   # ask()·MODELS만 재사용(질문·실행 부분은 빼고)
exec(src)
Q = open(os.path.join(H, 'judge_step_q.txt'), encoding='utf-8').read()
m, out = ask(Q, [os.path.join(H, 'board_step.png')])
open(os.path.join(H, 'gemini_step.md'), 'w', encoding='utf-8').write(f'## 점수({m})\n{out}\n'); print(m); print(out)
