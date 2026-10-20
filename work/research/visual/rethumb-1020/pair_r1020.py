# 11편 짝 비교(C-21): 지금(10/19 pick) vs 새(thumb_r20), 경쟁 5 = textpos-1019/src 잘되는 채널 5장 · 2번 다 이긴 편만 교체 후보
#   py -3.12 pair_r1020.py [편키 ...] → pair/<편>/pair_thumb.md, pair_result.json (읽기만 함, 유튜브 손 안 댐)
import os, sys, json, subprocess, glob
H = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.abspath(os.path.join(H, '..', '..', '..'))
EPD = os.path.join(WORK, 'research', 'longform', 'ep')
D = {d['key']: d for d in json.load(open(os.path.join(H, '..', 'rethumb-1019', 'decisions.json'), encoding='utf-8'))}
sys.path.insert(0, H); import make_r1020 as M
COMP = sorted(glob.glob(os.path.join(H, '..', 'textpos-1019', 'src', '*.jpg')))[:5]
res = {}
for k in (sys.argv[1:] or list(M.EPS)):
    fo = M.EPS[k][0]; cur = os.path.join(EPD, fo, f"thumb_{D[k]['pick']}.png"); new = os.path.join(EPD, fo, 'thumb_r20.png')
    r = subprocess.run(['py', '-3.12', os.path.join(WORK, 'thumbpair.py'), 'thumb', cur, new, *COMP, '--out', os.path.join(H, 'pair', k)], capture_output=True, text=True, encoding='utf-8', errors='replace', env={**os.environ, 'PYTHONIOENCODING': 'utf-8'})
    res[k] = {'exit': r.returncode, 'win': r.returncode == 0, 'err': (r.stderr or '')[-160:] if r.returncode not in (0, 3) else ''}
    print(k, r.returncode, '새판 2승' if r.returncode == 0 else '')
json.dump(res, open(os.path.join(H, 'pair_result.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
