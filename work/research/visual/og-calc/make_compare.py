# 비교판: 위 3줄 = 우리 시안 9장(a·b·c), 아래 줄 = 지금 운영 og v9 + 경쟁 계산기 og 4장(10/1 09:07 curl) — py -3.12 make_compare.py
import os
from PIL import Image, ImageDraw, ImageFont
H = os.path.dirname(os.path.abspath(__file__)); B = os.path.join(H, 'bench')
F = ImageFont.truetype('C:/Windows/Fonts/malgunbd.ttf', 20)
W, Hh = 400, 210
ours = [f'og_{k}_{v}.png' for v in 'abc' for k in ('salary', 'severance', 'unemployment')]
bench = [('운영 v9(지금 3종 공통)', 'og_v9.png'), ('사람인 연봉', 'saramin_salary.img'), ('잡코리아 연봉', 'jobkorea_salary.img'),
         ('데모데이 실수령', 'demoday.img'), ('사람인 실업급여·퇴직금', 'saramin_unemp.img')]
sheet = Image.new('RGB', (20 + 5 * (W + 20), 20 + 3 * (Hh + 50)), '#c9ced6'); d = ImageDraw.Draw(sheet)
def put(im, lab, x, y):
    im = im.convert('RGB'); im.thumbnail((W, Hh)); bg = Image.new('RGB', (W, Hh), '#ffffff'); bg.paste(im, ((W - im.width) // 2, (Hh - im.height) // 2))
    sheet.paste(bg, (x, y + 26)); d.text((x, y), lab, fill='#18191d', font=F)
for i, f in enumerate(ours):
    put(Image.open(os.path.join(H, f)), f.replace('og_', '').replace('.png', ''), 20 + (i % 3) * (W + 20), 20 + (i // 3) * (Hh + 50))
for i, (lab, f) in enumerate(bench):
    put(Image.open(os.path.join(B, f)), lab, 20 + i * (W + 20), 20 + 3 * (Hh + 50))
sheet.save(os.path.join(H, 'compare.png'))
