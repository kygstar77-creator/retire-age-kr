"""심사관에게 줄 자료 judge_brief.json — 줄마다 대본·따라 한 경쟁 장면 설명·우리 장면 종류·비교 그림 경로. visual 10/29 (P-3)."""
import json, re, sys, os
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); EP = os.path.join(HERE, '..', '..', 'longform', 'ep', 'P-3')
t = open(os.path.join(EP, 'shot_plan.md'), encoding='utf-8').read(); refs = {}
for l in t.split('# 경쟁 장면', 1)[1].split('# 장면 계획')[0].splitlines():
    m = re.match(r'\| (\d+) \| (\S+) \| ([^|]+)\| ([^|]+)\|', l)
    if m: refs[m.group(1)] = f"{m.group(3).strip()}: {m.group(4).strip()}"
rows = [[c.strip() for c in l.strip().strip('|').split('|')] for l in t.split('# 장면 계획', 1)[1].splitlines() if l.startswith('|') and not re.match(r'\|\s*[-장]', l)]
only = set(sys.argv[1:]); out = []
for i, r in enumerate(rows, 1):
    rid = f'r{i:02d}'
    if only and rid not in only: continue
    out.append({'r': rid, '장': r[0], '대본 줄': r[1], '우리 장면(구상 칸)': r[2], '경쟁': [f'#{x} ' + refs.get(x, '') for x in re.findall(r'#(\d+)', r[3])],
                '비교 그림': os.path.abspath(os.path.join(EP, 'shotcmp', rid + '.jpg')).replace(os.sep, '/')})
json.dump(out, open(os.path.join(HERE, 'judge_brief.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1); print(len(out))
