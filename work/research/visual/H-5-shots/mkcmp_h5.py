"""H-5 비교 그림 shotcmp/rNN.jpg — 왼쪽 따라 한 경쟁 장면(yt-dlp 480p 스트림에서 그 초 한 장, 영상 안 받음), 오른쪽 우리 장면. visual-designer 2026-11-17 (mkcmp_jt1.py 복사).
H-4 mkcmp_h4.py와 같은 꼴. 경쟁 캡처가 들어 있어 shotcmp/·cap/은 커밋하지 않는다.
경쟁 번호가 둘이면 두 장을 왼쪽에 위아래로.
사용: py -3.12 mkcmp_s1.py cap   → cap/cNN.jpg (경쟁 장면 표 주소의 &t=초)
      py -3.12 mkcmp_s1.py cmp   → ep/S-1/shotcmp/rNN.jpg (파일 있는 줄만)
"""
import os, re, sys, subprocess, imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
EP = os.path.join(WORK, 'research', 'longform', 'ep', 'H-5'); PUB = os.path.join(WORK, 'video', 'public')
CAP = os.path.join(HERE, 'cap'); FF = imageio_ffmpeg.get_ffmpeg_exe(); F = ImageFont.truetype(os.path.join(WORK, 'fonts', 'pd700.ttf'), 26)
t = open(os.path.join(EP, 'shot_plan.md'), encoding='utf-8').read()
refs = {}
for l in t.split('# 경쟁 장면', 1)[1].split('# 장면 계획')[0].splitlines():
    m = re.match(r'\| (\d+) \| (https://www\.youtube\.com/watch\?v=([\w-]+)&t=(\d+))', l)
    if m: refs[int(m.group(1))] = (m.group(3), int(m.group(4)))
rows = [[c.strip() for c in l.strip().strip('|').split('|')] for l in t.split('# 장면 계획', 1)[1].split('\n# ')[0].splitlines()
        if l.startswith('|') and not re.match(r'\|\s*[-장]', l)]

def cap():
    os.makedirs(CAP, exist_ok=True)
    need = sorted({int(x) for r in rows for x in re.findall(r'(\d+)', r[3])})
    urls = {}
    for n in need:
        vid, sec = refs[n]; out = os.path.join(CAP, f'c{n:02d}.jpg')
        if os.path.exists(out): continue
        if vid not in urls:
            urls[vid] = subprocess.run([sys.executable, '-m', 'yt_dlp', '-q', '--js-runtimes', 'node', '-f', 'best[height<=480]/bv*[height<=480]', '-g',
                                        f'https://www.youtube.com/watch?v={vid}'], capture_output=True, text=True).stdout.strip().splitlines()[0]
        subprocess.run([FF, '-y', '-loglevel', 'error', '-ss', str(sec + 1), '-i', urls[vid], '-frames:v', '1', out], check=True); print('cap', n, vid, sec)

def fit(im, w, h):
    im = im.copy(); im.thumbnail((w, h)); bg = Image.new('RGB', (w, h), (20, 20, 22)); bg.paste(im, ((w - im.width) // 2, (h - im.height) // 2)); return bg

def cmp():
    os.makedirs(os.path.join(EP, 'shotcmp'), exist_ok=True)
    for i, r in enumerate(rows, 1):
        fs = [os.path.join(PUB, x.strip()) for x in r[5].split('·') if x.strip()]
        fs = sorted(fs, key=lambda x: not x.endswith('.mp4'))[:2]   # 실사 있으면 실사 먼저, 판은 둘째
        if not all(os.path.exists(x) for x in fs): print('파일 없음', i, r[5]); continue
        imgs = []
        for f in fs:
            if f.endswith('.mp4'):
                png = os.path.join(os.environ.get('TEMP', '.'), 'h5cmp_' + os.path.basename(f) + '.png')
                subprocess.run([FF, '-y', '-loglevel', 'error', '-ss', '1.5', '-i', f, '-frames:v', '1', png], check=True); f = png
            imgs.append(Image.open(f).convert('RGB'))
        ns = [int(x) for x in re.findall(r'(\d+)', r[3])][:2]
        im = Image.new('RGB', (1920, 600), (250, 250, 248)); d = ImageDraw.Draw(im)
        d.text((20, 14), '경쟁 ' + ' · '.join(f'#{n}' for n in ns), font=F, fill=(40, 40, 40))
        d.text((980, 14), f'우리 · {r[0]} — {r[2][:30]}', font=F, fill=(40, 40, 40))
        if len(ns) == 1: im.paste(fit(Image.open(os.path.join(CAP, f'c{ns[0]:02d}.jpg')).convert('RGB'), 940, 530), (10, 56))
        else:
            for k, n in enumerate(ns): im.paste(fit(Image.open(os.path.join(CAP, f'c{n:02d}.jpg')).convert('RGB'), 466, 530), (10 + k * 474, 56))
        if len(imgs) == 1: im.paste(fit(imgs[0], 940, 530), (970, 56))
        else:
            for k, g in enumerate(imgs): im.paste(fit(g, 466, 530), (970 + k * 474, 56))
        im.save(os.path.join(EP, 'shotcmp', f'r{i:02d}.jpg'), quality=88); print(f'r{i:02d}', r[0], r[5])

if __name__ == '__main__':
    {'cap': cap, 'cmp': cmp}[sys.argv[1]]()
