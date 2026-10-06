# nhis_prop_b v3 첫 프레임만 그리기(firemap-shorts 10/7 07:1x) — 답 먼저 큰 글자
import sys, os, json, copy
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(H, '..', '..', '..', '..'))
import cardshort as C
from PIL import Image, ImageDraw
spec = json.load(open(os.path.join(H, '..', '..', sys.argv[1]), encoding='utf-8'))
c = spec['cards'][0]
probe = Image.new('RGB', (C.W, C.H)); bottom = C.draw_card(ImageDraw.Draw(probe), spec, c, 99, C.CARD_TOP)
off = max(0, (C.SAFE_B - bottom) // 2)
C.card_image(spec, c, 0, off).save(os.path.join(H, sys.argv[2]))
print('bottom', bottom, 'off', off)
