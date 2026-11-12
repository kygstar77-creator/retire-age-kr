# H-4 올리기 전 확인(11/12) — 실거래 다시 받아 raw/rt_1112에 두고, calc.py·calc_renew.py를 그 자료로 다시 돌려 calc_out과 비교
#   py -3.12 work/research/longform/ep/H-4/check/recheck_1112.py
import os, sys, json, subprocess
sys.stdout.reconfigure(encoding='utf-8')
EP = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); NEW = os.path.join(EP, 'raw', 'rt_1112'); os.makedirs(NEW, exist_ok=True)
sys.path.insert(0, os.path.normpath(os.path.join(EP, '..', '..', '..', '..')))
import rtmolit
OLD = os.path.join(EP, 'raw', 'rt')
for f in sorted(os.listdir(OLD)):
    lawd, ym, kind = f[:-5].split('_')
    p = os.path.join(NEW, f)
    if os.path.exists(p): continue
    json.dump(rtmolit.fetch(kind, lawd, ym), open(p, 'w', encoding='utf-8'), ensure_ascii=False)
print('fetched', len(os.listdir(NEW)))
for name in ('calc.py', 'calc_renew.py'):
    src = open(os.path.join(EP, name), encoding='utf-8').read().replace("os.path.join(HERE, 'raw', 'rt')", repr(NEW))
    g = {'__file__': os.path.join(EP, name), '__name__': '__main__'}
    out = os.path.join(EP, 'check', name.replace('.py', '_out_1112.txt'))
    so = sys.stdout; sys.stdout = open(out, 'w', encoding='utf-8')
    try: exec(compile(src, name, 'exec'), g)
    finally: sys.stdout.close(); sys.stdout = so
    print('wrote', out)
