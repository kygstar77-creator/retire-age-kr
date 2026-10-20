# T-1 t1n_c(10/20 09시 visual) — t1n_a에서 알약만 키움(58→100px @1920, 412px에서 약 21px). 흰 작은 줄은 64px로 줄여 위 층 높이 맞춤.
#   이유: 40·50·60세 3명 공통 '무엇의 12배'(알약 168px 안 읽힘, judges.md 07:15). 문구·사진 그대로.
import make_n1020 as m
from PIL import Image, ImageDraw
def make(out, big, pill_size=100, top_size=64, band=160):
    im = m.photo('f_31400388.jpg', y_anchor=0.0); d0 = ImageDraw.Draw(im)
    bs = min(m.fit(d0, t, 210, 'black') for t in big); ls = 1.14
    hb = len(big) * int(bs * ls); y = m.HH - 40 - hb
    im = m.shade(im, max(0, y - 140), m.HH, band); im = m.shade(im, 0, 380, 210, top=True)
    d = ImageDraw.Draw(im)
    d.text((m.X0, 36), m.TOP, font=m.f(top_size, '700'), fill=m.WHITE, stroke_width=3, stroke_fill=m.INK)
    yy = 36 + top_size + 22; ft = m.f(pill_size, '700'); tw = d.textlength(m.PILL, font=ft); ph = int(pill_size * 1.36)
    d.rounded_rectangle((m.X0, yy, m.X0 + tw + 64, yy + ph), 24, fill=m.ORANGE); d.text((m.X0 + 32, yy + ph // 2), m.PILL, font=ft, fill=m.WHITE, anchor='lm')
    for k, t in enumerate(big):
        d.text((m.X0, y - int(bs * 0.12)), t, font=m.f(bs, 'black'), fill=m.WHITE if k == 0 else m.ORANGE, stroke_width=6, stroke_fill=m.INK); y += int(bs * ls)
    im.resize((1280, 720), Image.LANCZOS).save(out); print(out)
make('t1n_c.png', ['10년 중 2년만 거주했으면', '2029년 양도세 약 12배'])
