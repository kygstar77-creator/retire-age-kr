"""P-3 AI 실사 마무리 — 고른 시드 + 알아볼 수 없는 가짜 글자 자리 흐리기. visual-designer 2026-10-29 (K-1-shots/ai_finish.py 꼴).
원본 bg/p3/ai_raw/(C:/Users/강영준/Documents/tools/localgen/p3/gen_p3.py, RealVisXL V5.0 이 PC) → bg/p3/ai/<장면>.png (1344x768).
r24 calendar_nov는 AI 3장 모두 가짜 날짜·이상한 손 → 종이 달력 판 p3_calendar_nov(p3boards.py)로 바꿈."""
import os
from PIL import Image, ImageFilter, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
BG = os.path.abspath(os.path.join(HERE, '..', '..', '..', 'video', 'public', 'bg', 'p3'))
def blur_box(im, box, r):
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle(box, 30, fill=255); m = m.filter(ImageFilter.GaussianBlur(14))
    return Image.composite(im.filter(ImageFilter.GaussianBlur(r)), im, m)
J = {
 'notice_magnifier': ('notice2_s22.png', lambda im: blur_box(im, (0, 0, 560, 230), 9)),  # 1차 3장 돋보기 없음 → notice2. 왼쪽 위 펼친 책 가짜 글자 흐림
 'tea_bill_steam':   ('tea_bill2_s22.png', lambda im: im),  # 1차 3장 고지서 없음 → tea_bill2(접힌 종이·김)
}
if __name__ == '__main__':
    os.makedirs(os.path.join(BG, 'ai'), exist_ok=True)
    for k, (src, fn) in J.items():
        fn(Image.open(os.path.join(BG, 'ai_raw', src)).convert('RGB')).save(os.path.join(BG, 'ai', k + '.png')); print(k)
