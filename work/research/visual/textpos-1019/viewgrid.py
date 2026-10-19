# 눈으로 보기용 판: 3x3 = 9장, 장당 480x270, 1/3 안내선(얇은 빨강 점선)
import sys, os, json
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
rows = json.load(open(os.path.join(HERE, 'data.json'), encoding='utf-8'))['rows']
OUT = os.path.join(sys.argv[1]); os.makedirs(OUT, exist_ok=True)
W, H, HD = 480, 270, 22
font = ImageFont.truetype('C:/Windows/Fonts/malgun.ttf', 15)
for b in range(0, len(rows), 9):
    sheet = Image.new('RGB', (W*3, (H+HD)*3), 'white'); d = ImageDraw.Draw(sheet)
    for i, r in enumerate(rows[b:b+9]):
        x, y = (i % 3) * W, (i // 3) * (H + HD)
        im = Image.open(os.path.join(HERE, 'src', r['id'] + '.jpg')).convert('RGB').resize((W, H))
        g = ImageDraw.Draw(im)
        for k in (1, 2):
            for t in range(0, W, 8): g.line([(t, H*k//3), (t+3, H*k//3)], fill=(255, 0, 0))
            for t in range(0, H, 8): g.line([(W*k//3, t), (W*k//3, t+3)], fill=(255, 0, 0))
        sheet.paste(im, (x, y + HD))
        d.text((x + 4, y + 2), f"#{b+i:02d} {r['channel']} {r['id']}", fill='black', font=font)
    sheet.save(os.path.join(OUT, f'view_{b//9:02d}.jpg'), quality=88)
print('ok')
