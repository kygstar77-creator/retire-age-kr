"""K-1 AI 실사 마무리 — 고른 시드 + 알아볼 수 없는 가짜 글자 자리 흐리기. visual-designer 2026-10-26.
원본 bg/k1/ai_raw/(gen_k1.py, RealVisXL V5.0 이 PC) → bg/k1/ai/<장면>.png (1344x768)."""
import os
from PIL import Image, ImageFilter, ImageDraw, ImageEnhance
HERE = os.path.dirname(os.path.abspath(__file__))
BG = os.path.abspath(os.path.join(HERE, '..', '..', '..', 'video', 'public', 'bg', 'k1'))
def blur_box(im, box, r):
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle(box, 30, fill=255); m = m.filter(ImageFilter.GaussianBlur(14))
    return Image.composite(im.filter(ImageFilter.GaussianBlur(r)), im, m)
def patch(im, box, src_xy):
    x0, y0, x1, y1 = box; c = im.crop((src_xy[0], src_xy[1], src_xy[0] + x1 - x0, src_xy[1] + y1 - y0))
    m = Image.new('L', c.size, 0); ImageDraw.Draw(m).rectangle((20, 20, c.width - 1, c.height - 20), fill=255); m = m.filter(ImageFilter.GaussianBlur(14))
    im.paste(c, (x0, y0), m); return im
def blur_except(im, keep, r):
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).ellipse(keep, fill=255); m = m.filter(ImageFilter.GaussianBlur(40))
    return Image.composite(im, im.filter(ImageFilter.GaussianBlur(r)), m)
J = {
 'phone_tea':    ('phone_tea2_s53.png', lambda im: im),  # 3차: 받침 위 가짜 휴대폰·덮은 자국 '못함' → 다시 뽑음(식탁에 찻잔·휴대폰만)
 'bank_ticket':  ('bank_ticket_s13.png', lambda im: blur_box(im, (690, 315, 940, 465), 6)),
 'calendar_hand':('calendar_hand_s12.png', lambda im: blur_except(im, (-260, 420, 400, 1000), 10)),
 'phone_scroll': ('phone_scroll_s12.png', lambda im: ImageEnhance.Brightness(blur_box(im, (450, 80, 685, 495), 9)).enhance(1.55)),
 'passbook':     ('passbook3_s42.png', lambda im: im),  # 3차: 장부책·흐린 책자 '못함' → 손가락 얹은 글자 없는 연파랑 통장
 'dusk_table':   ('dusk3_s43.png', lambda im: im),  # 3차: 외국 집·동남아풍 '못함' → 흰 아파트 단지 해 질 녘 식탁
 'keys_envelope':('keys2_s23.png', lambda im: blur_box(im, (330, 240, 960, 620), 4)),  # 열쇠 머리 가짜 글자 흐림
}
if __name__ == '__main__':
    import sys
    os.makedirs(os.path.join(BG, 'ai'), exist_ok=True)
    for k in ([a for a in sys.argv[1:] if a != '--over'] or ([] if '--over' in sys.argv else J)):
        src, fn = J[k]; p = os.path.join(BG, 'ai_raw', src)
        if not os.path.exists(p): print('없음', src); continue
        fn(Image.open(p).convert('RGB')).save(os.path.join(BG, 'ai', k + '.png')); print(k, '<-', src)

# 화면에 얹힐 글자까지 넣은 '마지막 모습'(비교·검수용 — 실제 글자는 PD가 Remotion에서 같은 말로 얹는다). 10/27 3차 심사 '사진만으론 대본 줄이 안 읽힘' 반영.
from PIL import ImageFont
FB = os.path.abspath(os.path.join(HERE, '..', '..', '..', 'fonts', 'NotoSansKR-Black.ttf'))
def over(src, lines, out, y=0.5):
    im = Image.open(os.path.join(BG, 'ai', src)).convert('RGB'); W, H = im.size
    g = Image.new('L', (W, H), 0); gd = ImageDraw.Draw(g)
    for k in range(H): gd.line([(0, k), (W, k)], fill=int(120 * max(0, 1 - abs(k / H - y) / 0.35)))
    im = Image.composite(Image.new('RGB', (W, H), (0, 0, 0)), im, g); d = ImageDraw.Draw(im)
    f = ImageFont.truetype(FB, 86); f.set_variation_by_axes([900])
    for i, (s, col) in enumerate(lines):
        d.text((W // 2, int(H * y) + (i - (len(lines) - 1) / 2) * 112), s, font=f, fill=col, anchor='mm', stroke_width=6, stroke_fill=(0, 0, 0))
    im.save(os.path.join(BG, 'ai', out)); print(out)
OVER = {
 'passbook_over': ('passbook.png', [('내 예금 이자는', (255, 255, 255)), ('얼마나 따라왔나', (255, 90, 0))], 0.5),
 'phone_tea_over': ('phone_tea.png', [('정기예금 1억원', (255, 255, 255)), ('다음 달 만기', (255, 90, 0))], 0.4),
}
if __name__ == '__main__' and '--over' in sys.argv:
    for k, (s, l, y) in OVER.items(): over(s, l, k + '.png', y)
