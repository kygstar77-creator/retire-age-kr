"""D-ETF-1 비교 그림 shotcmp/rNN.jpg — 왼쪽 따라 한 경쟁 장면(유튜브 480p 한 장씩), 오른쪽 우리 장면(Remotion DETF1 스틸 stills/rNN.jpg). visual-designer 2026-10-27 (K-1 mkcmp.py 고침).
사용: py -3.12 mkcmp.py <경쟁 캡처 폴더(cNN_k.jpg)> pick.json  · 경쟁 캡처가 들어 있어 shotcmp/는 커밋하지 않는다."""
import os, re, sys, json
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
EP = os.path.join(WORK, 'research', 'longform', 'ep', 'D-ETF-1'); FONT = os.path.join(WORK, 'fonts', 'pd700.ttf')
comp = sys.argv[1]; pick = json.load(open(sys.argv[2], encoding='utf-8'))
t = open(os.path.join(EP, 'shot_plan.md'), encoding='utf-8').read().split('# 장면 계획', 1)[1]
rows = [[c.strip() for c in l.strip().strip('|').split('|')] for l in t.splitlines() if l.startswith('|') and not re.match(r'\|\s*-', l)][1:]
def box(im, w, h):
    c = im.copy(); c.thumbnail((w, h)); bg = Image.new('RGB', (w, h), (20, 20, 22)); bg.paste(c, ((w - c.width) // 2, (h - c.height) // 2)); return bg
os.makedirs(os.path.join(EP, 'shotcmp'), exist_ok=True); f = ImageFont.truetype(FONT, 24); n = 0
for i, r in enumerate(rows, 1):
    rid = f'r{i:02d}'; refs = re.findall(r'#(\d+)', r[3])
    im = Image.new('RGB', (1920, 600), (250, 250, 248)); d = ImageDraw.Draw(im)
    d.text((20, 14), f'경쟁 #{" · #".join(refs)}', font=f, fill=(40, 40, 40)); d.text((980, 14), f'우리 {rid} · {r[1][:30]}', font=f, fill=(40, 40, 40))
    L = [Image.open(os.path.join(comp, f'c{pick[x]}.jpg')).convert('RGB') for x in refs[:2] if x in pick]
    if len(L) == 1: im.paste(box(L[0], 940, 530), (10, 56))
    elif len(L) >= 2: im.paste(box(L[0], 466, 530), (10, 56)); im.paste(box(L[1], 466, 530), (484, 56))
    O = [Image.open(os.path.join(EP, 'stills', x + '.jpg')).convert('RGB') for x in (rid, rid + 'b') if os.path.exists(os.path.join(EP, 'stills', x + '.jpg'))]
    if len(O) == 1: im.paste(box(O[0], 940, 530), (970, 56))
    else: im.paste(box(O[0], 466, 530), (970, 56)); im.paste(box(O[1], 466, 530), (1444, 56)); d.text((1444, 570), '→ 바로 다음 장면(같은 대본 줄의 답)', font=f, fill=(40, 40, 40))
    im.save(os.path.join(EP, 'shotcmp', rid + '.jpg'), quality=85); n += 1
print(n, 'cmp')
