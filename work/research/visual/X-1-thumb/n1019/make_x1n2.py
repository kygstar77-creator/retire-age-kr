# X-1 x1n_b 고친 판(10/20 17시): 짝 비교 pair1020c에서 두 번 모두 'B 달러 배경 때문에 글자 대비가 낮다'(제미나이) → 문구·사진·자리는 x1n_b 그대로, 큰 글 뒤만 손봄.
#   d: 큰 글 덩어리 뒤 사진을 흐리게(가우스 6)+짙은 그라데이션 강하게(band 110→215), 사진 전체 밝기 0.85

#   상자·판 없음(C-04 그라데이션). py -3.12 make_x1n2.py → ep/X-1/thumb_x1n_d.png, _e.png
import os, sys
from PIL import Image, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'make_x1n.py'), encoding='utf-8').read().split('# a: 큰 글 = 물음')[0]
g = {'__file__': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'make_x1n.py')}; exec(src, g)
_photo = g['photo']
def photo_soft(name, **k):
    im = _photo(name, **k); y0 = int(g['HH'] * 0.50)
    low = im.crop((0, y0, g['W'], g['HH'])).filter(ImageFilter.GaussianBlur(6)); im.paste(low, (0, y0))
    # 흐림 경계가 보이지 않게 위로 220px 섞음
    m = Image.linear_gradient('L').resize((g["W"], 220)); band = im.crop((0, y0 - 220, g["W"], y0)); bl = band.filter(ImageFilter.GaussianBlur(6))
    im.paste(Image.composite(bl, band, m), (0, y0 - 220)); return im
g['photo'] = photo_soft
g['make']('thumb_x1n_d.png', '4275306_6.jpg', 'S&P500에 1억, 산 날만 다르면?', ['작년 10월 +10%', '올 7월 −11%'], '원화 기준', band=215, y_anchor=0.0, zoom=1.1, dark=0.85)
