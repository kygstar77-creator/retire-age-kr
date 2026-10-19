# 휴대폰 목록 크기(가로 168px) 판 — 큰 글 자리별로 묶고, 우리 13편(rethumb-1019 공개본)·H-2 시험판을 옆에 둔다.
#   python sheet.py → contact_168.png
import os, sys, json, glob
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from ann import A
VIS = os.path.dirname(HERE); EP = os.path.join(VIS, '..', 'longform', 'ep')
rows = json.load(open(os.path.join(HERE, 'data.json'), encoding='utf-8'))['rows']
TW, TH, CAP, GAP, PER = 168, 95, 16, 8, 10
font = ImageFont.truetype('C:/Windows/Fonts/malgun.ttf', 11); hfont = ImageFont.truetype('C:/Windows/Fonts/malgunbd.ttf', 17)
ORDER = ['아래-넓게', '아래-왼쪽', '아래-가운데', '가운데-왼쪽', '가운데-넓게', '위-오른쪽']
groups = [(f'경쟁 · 큰 글 {p} ({sum(1 for i in A if A[i]["pos"] == p)}장)',
           [(os.path.join(HERE, 'src', r['id'] + '.jpg'), f"{r['channel'][:6]} {r['ratio']:.2f}배") for i, r in enumerate(rows) if A[i]['pos'] == p]) for p in ORDER]
groups.append(('경쟁 · 큰 글 위-왼쪽 (0장)', []))
ours = sorted(glob.glob(os.path.join(VIS, 'rethumb-1019', 'ytimg_after', '*.jpg')))
groups.append((f'우리 · 10/19 새 썸네일 13편 (전부 위-왼쪽)', [(p, os.path.basename(p)[:11]) for p in ours]))
groups.append(('H-2 · 지금 h2f4 / 시험판 a·b(큰 글 아래) / 대조 c(위-왼쪽)',
               [(os.path.join(EP, 'H-2', 'thumb_h2f4.png'), '지금 h2f4'), (os.path.join(HERE, 'h2tp_a.png'), 'h2tp_a 아래'),
                (os.path.join(HERE, 'h2tp_b.png'), 'h2tp_b 아래'), (os.path.join(HERE, 'h2tp_c.png'), 'h2tp_c 위-왼쪽')]))
height = 10
for t, items in groups: height += 28 + max(1, -(-len(items) // PER)) * (TH + CAP + GAP)
W = PER * (TW + GAP) + GAP
sheet = Image.new('RGB', (W, height), (245, 245, 245)); d = ImageDraw.Draw(sheet); y = 10
for t, items in groups:
    d.text((GAP, y), t, font=hfont, fill=(20, 20, 20)); y += 28
    if not items: d.text((GAP, y + 30), '없음', font=hfont, fill=(150, 150, 150))
    for k, (p, cap) in enumerate(items):
        x = GAP + (k % PER) * (TW + GAP); yy = y + (k // PER) * (TH + CAP + GAP)
        im = Image.open(p).convert('RGB').resize((TW, TH), Image.LANCZOS); sheet.paste(im, (x, yy))
        d.text((x, yy + TH + 1), cap, font=font, fill=(60, 60, 60))
    y += max(1, -(-len(items) // PER)) * (TH + CAP + GAP)
out = os.path.join(HERE, 'contact_168.png'); sheet.save(out); print(out, sheet.size)
