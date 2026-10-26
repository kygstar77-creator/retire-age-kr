"""심사관 JSON(judgeN_*.json) → ep/K-1/shot_plan.md '품질 판정' 칸. 사용: py -3.12 fill_plan.py <표시> judge1_a.json judge1_b.json
표시 예: '심사관 1차(새 Agent, 10/27 00시)'. 이미 같음·나음인 줄은 새 판정이 있을 때만 바꾼다."""
import sys, json, re, os
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.abspath(os.path.join(HERE, '..', '..', 'longform', 'ep', 'K-1', 'shot_plan.md'))
tag = sys.argv[1]; J = {}
for f in sys.argv[2:]:
    for x in json.load(open(os.path.join(HERE, f), encoding='utf-8')): J[x['r']] = x
t = open(P, encoding='utf-8').read(); out = []
for l in t.splitlines():
    m = re.search(r'\| shotcmp/(r\d\d)\.jpg \|', l)
    if m and m.group(1) in J:
        x = J[m.group(1)]; cells = l.rstrip().rstrip('|').split('|')
        txt = f"{x['verdict']} — {x['reason']}" + (f" 고칠 점: {x['fix']}" if x['verdict'] == '못함' and x.get('fix') else '') + f" [{tag}]"
        cells[-1] = ' ' + txt.replace('|', '/') + ' '; l = '|'.join(cells) + '|'
    out.append(l)
open(P, 'w', encoding='utf-8').write('\n'.join(out) + '\n')
from collections import Counter
print(Counter(x['verdict'] for x in J.values()))
