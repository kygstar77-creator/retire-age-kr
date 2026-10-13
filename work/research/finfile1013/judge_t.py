# finfile1013 제목 후보 심사(제미나이 2회씩). 사용: py -3.12 judge_t.py "제목1" "제목2"...
import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
sys.argv = [sys.argv[0], 'file'] + ['__T__' + t for t in sys.argv[1:]]
import importlib.util
src = open(os.path.join(H, 'judge_c.py'), encoding='utf-8').read().split("raw = []")[0]
exec(src)
raw = []
for t0 in [a[5:] for a in sys.argv[2:]]:
    tp2 = tp.replace('"' + title + '"', '"' + t0 + '"')
    for i in (1, 2):
        t = ask([{'text': tp2}]); raw.append(f'[제목후보 {t0} {i}]\n' + t); m = re.search(r'점수[^0-9]{0,20}(\d+(?:\.\d+)?)', t); print(t0, i, m.group(1) if m else t[:100])
open(os.path.join(H, 'judge_title_raw.md'), 'a', encoding='utf-8').write('\n---\n'.join(raw) + '\n===\n')
