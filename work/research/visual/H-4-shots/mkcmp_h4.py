"""H-4 비교 그림 shotcmp/rNN.jpg — 왼쪽 따라 한 경쟁 장면(yt-dlp 스트림에서 480p 한 장, 영상 안 받음), 오른쪽 우리 장면. visual-designer 2026-11-09.
K-1 mk1108b.py·mkcmp.py와 같은 꼴. 경쟁 캡처가 들어 있어 shotcmp/는 커밋하지 않는다.
사용: py -3.12 mkcmp_h4.py <경쟁 캡처 폴더(cNN_k.jpg)>  — 장면 계획에서 파일이 이미 있는 줄만 만든다(판·AI는 만든 뒤 다시 돌림).
"""
import os, re, sys, subprocess, imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
EP = os.path.join(WORK, 'research', 'longform', 'ep', 'H-4'); PUB = os.path.join(WORK, 'video', 'public')
FF = imageio_ffmpeg.get_ffmpeg_exe(); F = ImageFont.truetype(os.path.join(WORK, 'fonts', 'pd700.ttf'), 26)
CAP = sys.argv[1]; os.makedirs(os.path.join(EP, 'shotcmp'), exist_ok=True)
t = open(os.path.join(EP, 'shot_plan.md'), encoding='utf-8').read().split('# 장면 계획', 1)[1]
rows = [[c.strip() for c in l.strip().strip('|').split('|')] for l in t.splitlines() if l.startswith('|') and not re.match(r'\|\s*-', l)][1:]
def fit(im, w, h):
    im = im.copy(); im.thumbnail((w, h)); bg = Image.new('RGB', (w, h), (20, 20, 22)); bg.paste(im, ((w - im.width) // 2, (h - im.height) // 2)); return bg
for i, r in enumerate(rows, 1):
    f = os.path.join(PUB, r[5])
    if not os.path.exists(f): continue
    ref = re.findall(r'#(\d+)', r[3])[0]; cap = os.path.join(CAP, f'c{int(ref):02d}_1.jpg')
    if not os.path.exists(cap): print('경쟁 캡처 없음', ref); continue
    if f.endswith('.mp4'):
        png = os.path.join(os.environ.get('TEMP', '.'), 'h4cmp_' + os.path.basename(f) + '.png')
        subprocess.run([FF, '-y', '-loglevel', 'error', '-ss', '2', '-i', f, '-frames:v', '1', png], check=True); f = png
    im = Image.new('RGB', (1920, 600), (250, 250, 248)); d = ImageDraw.Draw(im)
    d.text((20, 14), f'경쟁 #{ref}', font=F, fill=(40, 40, 40)); d.text((980, 14), f'우리 · {r[5]} — {r[2][:30]}', font=F, fill=(40, 40, 40))
    im.paste(fit(Image.open(cap).convert('RGB'), 940, 530), (10, 56)); im.paste(fit(Image.open(f).convert('RGB'), 940, 530), (970, 56))
    out = f'r{i:02d}.jpg'; im.save(os.path.join(EP, 'shotcmp', out), quality=88); print(out, r[0], r[5])
