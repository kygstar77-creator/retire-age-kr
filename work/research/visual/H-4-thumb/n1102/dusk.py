# 광명 실물 사진(gm_complex_wm)을 어둡게·푸르게만 바꿈(합성·지우기 없음) — b(밤 사진)가 짝 비교에서 이긴 이유 '어두운 배경에 글자 대비'를 광명 사진으로
import os
from PIL import Image, ImageEnhance
H = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'photo')
im = Image.open(os.path.join(H, 'gm_complex_wm.jpg')).convert('RGB')
im = ImageEnhance.Contrast(ImageEnhance.Brightness(im).enhance(0.62)).enhance(1.25)
r, g, b = im.split(); im = Image.merge('RGB', (r.point(lambda v: v * 0.9), g.point(lambda v: v * 0.97), b.point(lambda v: min(255, v * 1.08))))
im.save(os.path.join(H, 'gm_complex_wm_dusk.jpg'), quality=92)
