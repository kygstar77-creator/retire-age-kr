"""K-1 비교 그림 shotcmp/rNN.jpg — 왼쪽 따라 한 경쟁 장면(360~480p 한 장씩), 오른쪽 우리 장면. visual-designer 2026-10-26.
사용: py -3.12 mkcmp.py <경쟁 캡처 폴더(cNN_k.jpg)> [pick.json]
pick.json = {"경쟁#": k 또는 "NN_k"} — 고른 캡처(0·1·2, 없으면 1). 쪼개기 시각이 ±20초 어긋나 옆 구간 캡처가 맞으면 "02_0"처럼 파일을 직접 적는다.
경쟁 캡처가 들어 있어 shotcmp/는 커밋하지 않는다(H-3과 같음).
"""
import os, re, sys, json, subprocess
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
EP = os.path.join(WORK, 'research', 'longform', 'ep', 'K-1')
PUB = os.path.join(WORK, 'video', 'public')
FF = os.path.join(WORK, 'video', 'node_modules', '@remotion', 'compositor-win32-x64-msvc', 'ffmpeg.exe')
FONT = os.path.join(WORK, 'fonts', 'pd700.ttf')
comp = sys.argv[1]; pick = json.load(open(sys.argv[2], encoding='utf-8')) if len(sys.argv) > 2 else {}

def plan_rows():
    t = open(os.path.join(EP, 'shot_plan.md'), encoding='utf-8').read()
    sec = t.split('# 장면 계획', 1)[1]
    rows = [[c.strip() for c in l.strip().strip('|').split('|')] for l in sec.splitlines() if l.startswith('|') and not re.match(r'\|\s*-', l)][1:]
    return rows

def ours(path):
    p = os.path.join(PUB, path)
    if p.endswith('.mp4'):
        png = os.path.join(os.environ.get('TEMP', '.'), 'k1cmp_' + os.path.basename(p) + '.png')
        subprocess.run([FF, '-y', '-loglevel', 'error', '-ss', '2', '-i', p, '-frames:v', '1', png]); p = png
    return Image.open(p).convert('RGB')

def fit(im, w, h):
    im = im.copy(); im.thumbnail((w, h)); bg = Image.new('RGB', (w, h), (20, 20, 22)); bg.paste(im, ((w - im.width) // 2, (h - im.height) // 2)); return bg

def main():
    os.makedirs(os.path.join(EP, 'shotcmp'), exist_ok=True); f = ImageFont.truetype(FONT, 26); done = []
    for r in plan_rows():
        cmpf, ourf, refs = r[6], [f.strip() for f in r[5].split('·')][-1], re.findall(r'#(\d+)', r[3])   # 파일이 둘이면 마지막(글자 얹은 마지막 모습)과 견줌
        im = Image.new('RGB', (1920, 600), (250, 250, 248)); d = ImageDraw.Draw(im)
        d.text((20, 14), f'경쟁 #{" · #".join(refs)}', font=f, fill=(40, 40, 40)); d.text((980, 14), f'우리 · {r[0]} · {r[1][:34]}', font=f, fill=(40, 40, 40))
        L = []
        for n in refs[:2]:
            k = pick.get(n, 1); p = os.path.join(comp, f'c{k}.jpg' if isinstance(k, str) else f'c{int(n):02d}_{k}.jpg')
            if os.path.exists(p): L.append(Image.open(p).convert('RGB'))
        if len(L) == 1: im.paste(fit(L[0], 940, 530), (10, 56))
        elif len(L) == 2: im.paste(fit(L[0], 466, 530), (10, 56)); im.paste(fit(L[1], 466, 530), (484, 56))
        try: im.paste(fit(ours(ourf), 940, 530), (970, 56))
        except Exception as e: print('ours 없음', ourf, e); continue
        im.save(os.path.join(EP, cmpf), quality=88); done.append(cmpf)
    print(len(done), 'cmp')

if __name__ == '__main__':
    main()
