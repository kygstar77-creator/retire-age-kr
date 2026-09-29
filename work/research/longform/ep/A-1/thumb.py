# A-1 썸네일 — 숫자 1개(분배금 12%) + 짧은 말 1개, 파이어맵 색. 제목 문구 반복 금지(RULES 5장). 숫자는 여는 장면에 그대로 나온다.
import os
from PIL import Image, ImageDraw, ImageFont
EP = os.path.dirname(os.path.abspath(__file__)); FD = os.path.join(EP, '..', '..', '..', '..', 'video', 'public', 'fonts')
B = lambda n: ImageFont.truetype(os.path.join(FD, 'pd700.ttf'), n)
im = Image.new('RGB', (1280, 720), '#101114'); d = ImageDraw.Draw(im)
d.text((80, 70), 'JEPQ', font=B(92), fill='#8b8f98')
d.text((70, 170), '분배금 12%', font=B(210), fill='#ff7a33')
d.rounded_rectangle((80, 470, 1200, 610), radius=28, fill='#1b1c21')
d.text((120, 492), '남은 돈은 SCHD보다 적었다', font=B(80), fill='#f2f3f5')
d.text((1200, 650), '파이어맵', font=B(40), fill='#8b8f98', anchor='rs')
im.save(os.path.join(EP, 'thumb.png')); print('thumb.png')
