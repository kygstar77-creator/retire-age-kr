# 비교판(지금·r19a·r19b) — 눈으로 보기용
import os, sys
from PIL import Image
E = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'longform', 'ep'))
L = sys.argv[2].split(','); W, H = 480, 270
bd = Image.new('RGB', (3 * W, len(L) * H), 'white')
for r, e in enumerate(L):
    for c, k in enumerate(['before_1019', 'r19a', 'r19b']):
        bd.paste(Image.open(os.path.join(E, e, 'thumb_' + k + '.png')).convert('RGB').resize((W, H)), (c * W, r * H))
bd.save(sys.argv[1], quality=85)
