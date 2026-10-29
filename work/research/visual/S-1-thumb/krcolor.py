# S-1 c 사진(Pexels 39135247) 차트 색을 한국식으로 — 레드팀 10/29 '초록=상승 외국 차트, 4060은 빨강=상승으로 읽어 거꾸로 보임'.
#   초록 봉·막대 → 빨강, 빨강 봉·막대 → 파랑. 손 둘레는 아주 짙은 빨강만(살색 안 건드림), 화면 밖 붉은 조명(오른쪽 끝)은 그대로.
import numpy as np
from PIL import Image
im = Image.open('photo/hand_point_chart_39135247.jpg').convert('RGB'); im = im.resize((2880, 1920), Image.LANCZOS)
hsv = np.array(im.convert('HSV')).astype(int); h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]   # PIL H 0~255
H, W = h.shape; yy, xx = np.mgrid[0:H, 0:W]
hand = (xx > W * 0.63) & (yy > H * 0.26) & (yy < H * 0.56); keep = xx > W * 0.955   # 손 둘레는 빨강만 더 짙은 것(살색 아님)만 바꿈
green = (h > 60) & (h < 125) & (s > 90) & (v > 60) & ~keep
red = ((h < 9) | (h > 240)) & (s > 140) & (v > 70) & ~keep & (yy < H * 0.62) & (~hand | (s > 200))
h2 = h.copy(); h2[green] = 0; h2[red] = 155    # 파랑 ≈ 218°
s2 = s.copy(); s2[green] = np.maximum(s[green], 190)
out = Image.fromarray(np.stack([h2, s2, v], -1).astype('uint8'), 'HSV').convert('RGB')
out.save('photo/hand_point_chart_39135247_kr.jpg', quality=93); print(green.mean(), red.mean())
