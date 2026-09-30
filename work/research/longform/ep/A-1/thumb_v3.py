# A-1 썸네일 v2 (2026-09-30 23시, 순돌이)
# 사장님 지적: 첫 썸네일(어두운 글자판)이 채널에서 잘된 틀과 달랐다. 잘된 틀은 흰 고양이·매달린 간판·밝은 배경·큰 한글 2덩이.
# 또 길이 표시가 글자를 가렸다. 제미나이 이미지(무료 한도 429)와 ChatGPT 이미지(스꾸와 같은 한도)는 쓸 수 없었다.
# 그래서 우리 채널의 잘된 썸네일(zhTjJwy1mwQ, 1,971회, 우리 자산)의 고양이와 SCHD 간판을 살리고, 왼쪽 간판을 JEPQ로 다시 그렸다.
# 아래 글자도 새로 얹었다. 오른쪽 아래(길이 표시 자리)는 비운다.
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
EP = os.path.dirname(os.path.abspath(__file__)); FD = os.path.join(EP, '..', '..', '..', '..', 'video', 'public', 'fonts')
B = lambda n: ImageFont.truetype(os.path.join(FD, 'pd700.ttf'), n)
im = Image.open(os.path.join(EP, 'ref_winner.jpg')).convert('RGB').resize((1280, 720)); d = ImageDraw.Draw(im)
# 왼쪽 간판(QQQM)을 JEPQ로: 나무 느낌 주황 판
d.rounded_rectangle((0, 182, 458, 420), radius=10, fill='#c9791d', outline='#8a4f10', width=10)
for y in range(200, 410, 18): d.line((10, y, 448, y + 4), fill='#d48a2c', width=3)
f = B(150); w = d.textlength('JEPQ', font=f)
for dx, dy in [(4, 5)]: d.text(((458 - w) / 2 + dx, 215 + dy), 'JEPQ', font=f, fill='#6b3a08')
d.text(((458 - w) / 2, 215), 'JEPQ', font=f, fill='#fff6ea')
# 아래 옛 글자 덮기: 부드러운 어두운 띠
band = Image.new('RGBA', (1280, 225), (21, 22, 26, 255))
im.paste(band, (0, 495), band)
def outline(xy, t, f, fill):
    x, y = xy
    for dx in range(-6, 7, 3):
        for dy in range(-6, 7, 3): d.text((x + dx, y + dy), t, font=f, fill='#000000')
    d.text(xy, t, font=f, fill=fill)
outline((40, 506), '분배금 12% vs 배당 성장', B(80), '#ffd200')
outline((40, 592), '1억, 1년 뒤 승자는?', B(100), '#ffffff')   # 오른쪽 아래 x>960, y>600 비움
im.save(os.path.join(EP, 'thumb_v3.png'), quality=95)
im.resize((320, 180)).save(os.path.join(EP, 'thumb_v3_small.png')); print('ok')
