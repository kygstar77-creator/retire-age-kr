from PIL import Image, ImageDraw, ImageFont
import glob, os
cs = sorted(glob.glob('comp/c_*.jpg')); ours = ['cc1_a.png', 'cc1_b.png', 'cc1_c.png']
F = ImageFont.truetype(r'C:\Windows\Fonts\malgun.ttf', 16)
c = Image.new('RGB', (412 * 4 + 50, (232 + 26) * 2 + 10), 'white'); d = ImageDraw.Draw(c)
for i, p in enumerate(cs + ours):
    x = (i % 4) * 422; y = (i // 4) * 258
    c.paste(Image.open(p).convert('RGB').resize((412, 232)), (x, y + 24))
    d.text((x, y + 2), ('경쟁 ' if p.startswith('comp') else '우리 ') + os.path.basename(p), fill='black', font=F)
c.save('compare.png')
