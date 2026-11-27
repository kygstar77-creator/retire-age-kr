"""NDG-1 비교 그림 — visual 2026-11-27 (mkcmp_h6.py 꼴). 왼쪽 따라 한 경쟁 장면 = raw/sb 스토리보드 칸(그 초가 든 칸 하나, 영상 안 받음), 오른쪽 우리 장면.
경쟁 칸이 들어 있어 shotcmp/는 커밋하지 않는다(raw/sb도 커밋 안 함).
사용: py -3.12 mkcmp_ndg1.py   → ep/NDG-1/shotcmp/rNN.jpg (파일 있는 줄만, NN = 장면 계획 줄 번호)
"""
import os, re, sys, json, glob, subprocess, imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
EP = os.path.join(WORK, 'research', 'longform', 'ep', 'NDG-1'); PUB = os.path.join(WORK, 'video', 'public'); SB = os.path.join(EP, 'raw', 'sb')
FF = imageio_ffmpeg.get_ffmpeg_exe(); F = ImageFont.truetype(os.path.join(WORK, 'fonts', 'pd700.ttf'), 26)
t = open(os.path.join(EP, 'shot_plan.md'), encoding='utf-8').read()
refs = {}
for l in t.split('# 경쟁 장면', 1)[1].split('# 장면 계획')[0].splitlines():
    m = re.match(r'\| (\d+) \| https://www\.youtube\.com/watch\?v=([\w-]+)&t=(\d+)', l)
    if m: refs[int(m.group(1))] = (m.group(2), int(m.group(3)))
rows = [[c.strip() for c in l.strip().strip('|').split('|')] for l in t.split('# 장면 계획', 1)[1].split('\n# ')[0].splitlines()
        if l.startswith('|') and not re.match(r'\|\s*[-장]', l)]

def sb_tile(vid, sec):
    js = os.path.join(SB, vid + '.json')
    if os.path.exists(js):
        meta = json.load(open(js, encoding='utf-8')); fm = meta['fmt']; c, r = fm['columns'], fm['rows']
        fr = max([f for f in meta['frags'] if f['start'] <= sec], key=lambda f: f['start'])
        k = min(c * r - 1, int((sec - fr['start']) / (fr['dur'] / (c * r))))
        page = Image.open(os.path.join(SB, f"{vid}_{fr['i']:02d}.jpg")).convert('RGB')
        tw, th = page.width // c, page.height // r
        return page.crop(((k % c) * tw, (k // c) * th, (k % c + 1) * tw, (k // c + 1) * th))
    pages = sorted(glob.glob(os.path.join(SB, vid + '_*.jpg')))   # json 없는 영상(ihpmQU33A_g): 페이지를 고르게 나눈 어림
    return None if not pages else Image.open(pages[0]).convert('RGB')

def fit(im, w, h):
    im = im.copy(); im = im.resize((w, int(im.height * w / im.width))) if im.width / im.height > w / h else im.resize((int(im.width * h / im.height), h))
    bg = Image.new('RGB', (w, h), (20, 20, 22)); bg.paste(im, ((w - im.width) // 2, (h - im.height) // 2)); return bg

def main():
    os.makedirs(os.path.join(EP, 'shotcmp'), exist_ok=True); done = []
    for i, r in enumerate(rows, 1):
        fs = [os.path.join(PUB, x.strip()) for x in r[5].split('·') if x.strip()]
        if not fs or not all(os.path.exists(x) for x in fs): print('파일 없음', i, r[5]); continue
        imgs = []
        for f in fs[:2]:
            if f.endswith('.mp4'):
                png = os.path.join(os.environ.get('TEMP', '.'), 'ndg1cmp_' + os.path.basename(f) + '.png')
                subprocess.run([FF, '-y', '-loglevel', 'error', '-ss', '1.5', '-i', f, '-frames:v', '1', png], check=True); f = png
            imgs.append(Image.open(f).convert('RGB'))
        ns = [int(x) for x in re.findall(r'#(\d+)', r[3])][:2]
        tiles = [sb_tile(*refs[n]) for n in ns]
        im = Image.new('RGB', (1920, 600), (250, 250, 248)); d = ImageDraw.Draw(im)
        d.text((20, 14), '경쟁 ' + ' · '.join(f'#{n}' for n in ns) + ' (스토리보드 칸)', font=F, fill=(40, 40, 40))
        d.text((980, 14), f'우리 · {r[0]} — {r[1][:28]}', font=F, fill=(40, 40, 40))
        tiles = [x for x in tiles if x is not None]
        if len(tiles) == 1: im.paste(fit(tiles[0], 940, 530), (10, 56))
        else:
            for k, g in enumerate(tiles): im.paste(fit(g, 466, 530), (10 + k * 474, 56))
        if len(imgs) == 1: im.paste(fit(imgs[0], 940, 530), (970, 56))
        else:
            for k, g in enumerate(imgs): im.paste(fit(g, 466, 530), (970 + k * 474, 56))
        im.save(os.path.join(EP, 'shotcmp', f'r{i:02d}.jpg'), quality=88); done.append(i); print(f'r{i:02d}', r[0], r[5])
    return done

if __name__ == '__main__':
    main()
