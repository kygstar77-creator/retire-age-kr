# 시안 미리보기 판(1280 축소 640 + 168 실제 크기) — py -3.12 peek.py p1a,p1b,p1c [out.png]
import sys, os
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__)); EP = os.path.join(H, '..', '..', 'longform', 'ep', 'P-1')
ks = sys.argv[1].split(','); out = sys.argv[2] if len(sys.argv) > 2 else 'peek.png'
b = Image.new('RGB', (660 * len(ks), 480), 'white')
for i, k in enumerate(ks):
    b.paste(Image.open(os.path.join(EP, f'thumb_{k}.png')).resize((640, 360)), (i * 660, 0))
    b.paste(Image.open(os.path.join(H, f'{k}_168.png')), (i * 660, 376))
b.save(os.path.join(H, out))
