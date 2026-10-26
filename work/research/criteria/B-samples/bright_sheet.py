# 밝기 시트(10/26 motion): 경쟁 25편·우리 12편을 밝기(Y) 순으로 한 장에 — 편마다 1/3·2/3 지점 2장, 위 글자 = 밝기
#   py -3.12 bright_sheet.py <out.png>
import sys, os, json, subprocess
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); FF = os.path.join(HERE, 'media', 'bin', 'ffmpeg.exe')
TW, TH = 72, 128
def rows(fn, d):
    return [(json.loads(l), d) for l in open(os.path.join(HERE, 'res', fn), encoding='utf-8') if l.strip() and l.strip() != 'null']
items = rows('bright_comp_1026.jsonl', 'media') + rows('bright_ours_1026.jsonl', 'media/ours1026')
items.sort(key=lambda t: t[0]['Y'])
def grab(p, n):
    out = []
    for frac in (1 / 3, 2 / 3):
        r = subprocess.run([FF, '-v', 'error', '-ss', str(max(0, int(n * frac))), '-i', p, '-frames:v', '1', '-vf', f'scale={TW}:{TH}', '-pix_fmt', 'rgb24', '-f', 'rawvideo', '-'], capture_output=True)
        out.append(Image.frombytes('RGB', (TW, TH), r.stdout[:TW * TH * 3]) if len(r.stdout) >= TW * TH * 3 else Image.new('RGB', (TW, TH), 'gray'))
    return out
font = ImageFont.truetype('C:/Windows/Fonts/malgunbd.ttf', 13)
cols = 13; cw = TW * 2 + 6; ch = TH + 22
rowsn = (len(items) + cols - 1) // cols
sheet = Image.new('RGB', (cols * cw + 6, rowsn * ch + 34), 'white')
d = ImageDraw.Draw(sheet)
d.text((6, 6), '쇼츠 밝기(편 칸 밝기 중앙 Y, 어두운 순) · 파랑=경쟁 25편 중앙 85 · 주황=우리 12편 중앙 50 · 2026-10-26', fill='black', font=font)
for i, (m, sub) in enumerate(items):
    x, y = 6 + (i % cols) * cw, 30 + (i // cols) * ch
    ours = 'ours' in sub
    for k, im in enumerate(grab(os.path.join(HERE, sub, m['file']), m['n'])): sheet.paste(im, (x + k * TW, y + 18))
    d.rectangle([x - 2, y + 16, x + TW * 2 + 1, y + 18 + TH + 1], outline=(230, 120, 0) if ours else (40, 90, 200), width=2)
    vid = m['file'].split('_', 1)[1][:5]
    d.text((x, y), f"{'우리' if ours else '남'} {vid} {m['Y']:.0f}", fill=(200, 90, 0) if ours else (30, 70, 170), font=font)
sheet.save(sys.argv[1]); print(sys.argv[1], sheet.size)
