# 11/12 n3obj1112 걸린 판(상자 2↑)에 같은 뜻 다른 그림을 차례로 대 보고, boardcheck 기준(상자 1↓)을 넘는 첫 그림을 고른다. 그림을 감지기에 맞춰 고치지 않는다.
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, HERE); sys.path.insert(0, WORK)
import n3obj1112 as N, boardcheck as BC, k1boards as K
from PIL import Image
TRY = {'n3_4760': ['receipt', 'calculator', 'coins'], 'n3_8020': ['calendar', 'coins', 'bankbook'],
       'n3_leak_q': ['receipt', 'bill', 'coins'], 'n3_nontax': ['receipt', 'bill', 'coins', 'scale'],
       'n3_sameformula': ['calculator', 'flow', 'scale'], 'n3_taxsteps': ['bill', 'receipt', 'calculator', 'coins']}
for n, cands in TRY.items():
    base = Image.open(os.path.join(N.BASE, n + '.png')).convert('RGB'); sp = N.find_spot(N.ink_mask(base))
    for o in cands:
        im = base.copy(); K.obj(im, o, sp[0], sp[1], sp[2], rot=3); p = os.path.join(N.D, n + '.png'); im.save(p)
        mh, ln, bx = BC.check(p); print(n, o, 'boxes', bx, flush=True)
        if bx <= 1: break
    else: print(n, '— 통과 그림 없음, base로 되돌림'); base.save(os.path.join(N.D, n + '.png'))
