# 11/12 판 사물 그림을 더한 판(n3obj1112 PLAN + n3_seven)이 들어간 shot_plan 줄의 비교 그림 오른쪽(우리 장면)만 새 판으로 바꾼다.
# 경쟁 캡처(왼쪽)는 11/4 scratchpad에서 지워져 mkcmp를 통째로 다시 못 돌림 — 왼쪽 그대로, 오른쪽만(mkcmp와 같은 자리·크기 970,56 / 940x530).
import os, sys, re
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
sys.argv = sys.argv[:1] + ['-']   # mkcmp는 import 때 argv[1](경쟁 폴더)을 읽음 — 쓰지 않음
from mkcmp import plan_rows, ours, fit, EP
from n3obj1112 import PLAN
from PIL import Image
CH = set(PLAN) | {'n3_seven'}
for row in plan_rows():
    cmpf, f = row[6], [x.strip() for x in row[5].split('·')][-1]   # mkcmp와 같은 칸: 6=비교 그림, 5=파일(마지막)
    if not any(n + '.png' in f for n in CH): continue
    p = os.path.join(EP, cmpf.strip('` '))
    if not os.path.exists(p): print('비교 그림 없음', rid); continue
    im = Image.open(p).convert('RGB'); im.paste(fit(ours(f), 940, 530), (970, 56)); im.save(p, quality=88); print('바꿈', os.path.basename(p), f)
