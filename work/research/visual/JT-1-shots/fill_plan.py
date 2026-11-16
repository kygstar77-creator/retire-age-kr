"""JT-1 shot_plan.md 장면 계획 표의 '비교 그림'·'품질 판정' 칸 채우기 — visual 2026-11-16.
judge.json = {"r01": ["같음", "이유", (줄마다 심사관·시각, 없으면 인자)], ...} (만든 사람이 아닌 새 심사관 Agent 답을 그대로 옮김). 사용: py -3.12 fill_plan.py judge.json "새 심사관 Agent 11/16 HH:MM"
"""
import json, re, sys, os
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, '..', '..', 'longform', 'ep', 'JT-1', 'shot_plan.md')
J = json.load(open(sys.argv[1], encoding='utf-8')); who = sys.argv[2]
head, rest = open(P, encoding='utf-8').read().split('# 장면 계획', 1)
lines = rest.split('\n'); i = 0
for k, l in enumerate(lines):
    if l.startswith('|') and not re.match(r'\|\s*[-장]', l):
        i += 1; rid = f'r{i:02d}'; c = l.strip().strip('|').split('|')
        c = [x.strip() for x in c] + [''] * (8 - len(c))
        v, why = J[rid][:2]; w = J[rid][2] if len(J[rid]) > 2 else who
        c[6] = f'shotcmp/{rid}.jpg'; c[7] = f'{v} — {w}({why})'
        lines[k] = '| ' + ' | '.join(c[:8]) + ' |'
open(P, 'w', encoding='utf-8', newline='\n').write(head + '# 장면 계획' + '\n'.join(lines)); print(i, '줄')
