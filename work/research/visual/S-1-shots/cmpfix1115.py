# 11/15 17시: s1boards 손 동그라미 고친 5장(r02·r09·r10·r12·r13)의 비교 그림 오른쪽(우리)만 새 판으로 — 왼쪽 경쟁 캡처 그대로(cmpfix1112와 같은 자리 970,56 / 940x530).
from PIL import Image
EP = 'research/longform/ep/S-1/shotcmp'; BD = 'video/public/bg/s1/board'   # work/에서 실행
def fit(im, w, h):
    im = im.copy(); im.thumbnail((w, h)); bg = Image.new('RGB', (w, h), (20, 20, 22)); bg.paste(im, ((w - im.width) // 2, (h - im.height) // 2)); return bg
for r, n in [('r02', 's1_100ju'), ('r09', 's1_top5'), ('r10', 's1_scale_day'), ('r12', 's1_yoy_rows'), ('r13', 's1_scale_month')]:
    p = f'{EP}/{r}.jpg'; im = Image.open(p).convert('RGB'); im.paste(fit(Image.open(f'{BD}/{n}.png').convert('RGB'), 940, 530), (970, 56)); im.save(p, quality=88)
