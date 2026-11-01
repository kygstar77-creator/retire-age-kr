# 비교판 compare.png — 우리 e·f + 경쟁 5(412px)
import glob, os
from PIL import Image, ImageDraw, ImageFont
O = os.path.dirname(os.path.abspath(__file__))
fs = [os.path.join(O, 'w3n_e.png'), os.path.join(O, 'w3n_f.png')] + sorted(glob.glob(os.path.join(O, 'comp', '*.jpg')))
W, H = 412, 232; b = Image.new('RGB', (4 * W + 30, 2 * (H + 24)), 'white'); d = ImageDraw.Draw(b); F = ImageFont.truetype(r'C:\Windows\Fonts\malgun.ttf', 14)
for i, f in enumerate(fs):
    x = (i % 4) * (W + 10); y = (i // 4) * (H + 24); b.paste(Image.open(f).convert('RGB').resize((W, H)), (x, y)); d.text((x + 2, y + H + 2), os.path.basename(f), fill='black', font=F)
b.save(os.path.join(O, 'compare.png'))
