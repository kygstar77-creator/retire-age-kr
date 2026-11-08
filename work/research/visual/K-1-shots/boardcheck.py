"""K-1 판 PNG를 렌더 화면(1920×1080, 판 82%·위 28px — k1_ds.mp4 170초 실측)에 얹어 bgcheck와 같은 함수로 잰다 — 렌더 전 관문 미리보기.
사용: py -3.12 boardcheck.py [이름 ...]  → 이름 · 가장 큰 글자 % · 글자 줄 · UI 상자 수 (bgcheck ④ 9%↑ · ⑤ 8줄↓ · ⑥ 상자 2개↑ 판이 30% 넘으면 거부)"""
import os, sys, glob
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, WORK)
import bgcheck
BD = os.path.join(WORK, 'video', 'public', 'bg', 'k1', 'board')
def frame(p):
    bg = Image.new('RGB', (1920, 1080), (24, 24, 30)); b = Image.open(p).convert('RGB').resize((1572, 884), Image.LANCZOS)
    bg.paste(b, (176, 28)); return np.array(bg)
def check(p):
    a = frame(p); mh, n = bgcheck.text_lines(a); return mh, n, bgcheck.ui_boxes(a)
if __name__ == '__main__':
    names = sys.argv[1:] or sorted(os.path.basename(x)[:-4] for x in glob.glob(os.path.join(BD, 'k1_*.png')))
    for nm in names:
        mh, n, bx = check(os.path.join(BD, nm + '.png'))
        print(f'{nm:16s} 큰글자 {mh:5.1f}% {"OK" if mh >= 9 else "--"} · 줄 {n:2d} {"OK" if n <= 8 else "--"} · 상자 {bx} {"OK" if bx < 2 else "--"}')
