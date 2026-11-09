"""롱폼 판 PNG 렌더 전 검사(공용) — 판을 렌더 화면(1920×1080, 판 82%·위 28px — K-1 k1_ds.mp4 실측)에 얹어 bgcheck와 같은 함수로 잰다.
visual-designer 2026-11-09, research/visual/K-1-shots/boardcheck.py를 편 이름 인자로 넓힘.
사용: py -3.12 work/boardcheck.py <편 폴더 이름: k1|h4|p3|n3 …> [판 이름 ...]
→ 이름 · 가장 큰 글자 % · 글자 줄 · UI 상자 수 (bgcheck ④ 9%↑ · ⑤ 8줄↓ · ⑥ 상자 2개↑ 판이 30% 넘으면 거부). 하나라도 '--'면 종료 코드 1."""
import os, sys, glob
import numpy as np
from PIL import Image
WORK = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, WORK)
import bgcheck
def frame(p):
    bg = Image.new('RGB', (1920, 1080), (24, 24, 30)); b = Image.open(p).convert('RGB').resize((1572, 884), Image.LANCZOS)
    bg.paste(b, (176, 28)); return np.array(bg)
def check(p):
    a = frame(p); mh, n = bgcheck.text_lines(a); return mh, n, bgcheck.ui_boxes(a)
if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')
    ep = sys.argv[1]; BD = os.path.join(WORK, 'video', 'public', 'bg', ep, 'board')
    names = sys.argv[2:] or sorted(os.path.basename(x)[:-4] for x in glob.glob(os.path.join(BD, '*.png')))
    bad = 0
    for nm in names:
        mh, n, bx = check(os.path.join(BD, nm + '.png')); ok = mh >= 9 and n <= 8 and bx < 2; bad += not ok
        print(f'{nm:16s} 큰글자 {mh:5.1f}% {"OK" if mh >= 9 else "--"} · 줄 {n:2d} {"OK" if n <= 8 else "--"} · 상자 {bx} {"OK" if bx < 2 else "--"}')
    print(f'{len(names)}장 중 걸림 {bad}'); sys.exit(1 if bad else 0)
