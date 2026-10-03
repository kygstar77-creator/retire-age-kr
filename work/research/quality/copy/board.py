# 카페 제목·쇼츠 제목 비교판 — 우리 제목 | 같은 주제 경쟁 상위 3 (scorecard-2026-10, copywriter)
import json, re
from PIL import Image, ImageDraw, ImageFont
R = 'C:/Users/강영준/Documents/GitHub/retire-age-kr/work/research/'
F = 'C:/Windows/Fonts/malgun.ttf'; FB = 'C:/Windows/Fonts/malgunbd.ttf'
def comp(path, col):
    out = []
    for ln in open(R + path, encoding='utf-8'):
        c = [x.strip() for x in ln.strip().strip('|').split('|')]
        if len(c) > col and re.fullmatch(r'\d+', c[0]) and len(out) < 3:
            out.append(re.sub(r'\*\*', '', c[col])[:60])
    if not out:  # 표 없는 compare.md는 따옴표 속 제목
        out = [t for t in re.findall(r"'([^']{12,60})'", open(R + path, encoding='utf-8').read()) if '?' in t or '아파트' in t][:3]
    return out
hy = json.load(open(R + 'cardshorts/e1_hynix_dd.json', encoding='utf-8'))['yt_title']
rows = []
for d in ['nps1002', 'garak0929', 'b10danji1003', 'offimkt_ic0929', 'pibu1003']:
    rows.append((d + ' (카페)', open(R + d + '/pkg/title.txt', encoding='utf-8').read().strip(), comp(d + '/compare.md', 1)))
rows.append(('e1_hynix_dd (쇼츠)', hy, comp('cardshorts/e1_hynix_dd/compete.md', 7)))
W, H = 1400, 70 + 150 * len(rows)
im = Image.new('RGB', (W, H), 'white'); g = ImageDraw.Draw(im)
f1, f2, f3 = ImageFont.truetype(FB, 26), ImageFont.truetype(F, 20), ImageFont.truetype(F, 17)
g.text((24, 18), '제목 비교판 2026-10-03 — 굵은 글씨 = 우리 공개 제목 · 회색 = 같은 주제 경쟁 상위 3', font=f2, fill='#111')
y = 60
for name, ours, cs in rows:
    g.line((24, y, W - 24, y), fill='#ddd')
    g.text((24, y + 10), name, font=f3, fill='#E8590C')
    g.text((24, y + 34), ours, font=f1, fill='#111')
    for i, c in enumerate(cs):
        g.text((44, y + 74 + i * 24), f'{i+1}. {c}', font=f3, fill='#777')
    y += 150
im.save(R + 'quality/copy/board-2026-10-03.png')
small = im.resize((700, H // 2)); small.save(R + 'quality/copy/board-2026-10-03-small.png')
json.dump([{'item': n, 'ours': o, 'comp': c} for n, o, c in rows], open(R + 'quality/copy/board-2026-10-03.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', len(rows))
