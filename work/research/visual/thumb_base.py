# 공용 썸네일 기본값 (visual 2026-11-26) — benchmark-loop 11/26 지시(longform/thumb-gap-1126.md 3위 '이긴 판이 안 넘어감 두 판째')
#   왜: H-5 o1(11/14 2:0)·SQ-1 p(11/20 2:0)·KOSPI-1 n1(11/20 2:0)에서 이긴 '테두리 약 10px·덮개 걷음·밝은 배경·주제를 싣는 배경'이
#       편마다 따로인 make_*.py로 안 넘어감 — 밝기 중앙값 남 89.5(19~114, 1126 8장) vs 우리 최근 5장 57.
#   make_*.py는 이 파일의 KW(make() 인자)·brighten()·luma()·screen_paste()를 불러 쓴다. 값 바꾸려면 근거(registry C-13·C-14) 한 줄 먼저.
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

# make() 인자 — 캔버스 1920×1080 기준(저장은 1280). sw 15 = 1280에서 약 10px 테두리(C-14 후보, 남 1120 13/13·1126 8/8 테두리·검은 띠)
KW = dict(band=60, tshade=(420, 110), sw=15, tsw=9)
LUMA_TARGET = 90      # 남 1126 롱폼 8장 회색 중앙값 89.5 (640×360, thumb-gap-1126.md 9행과 같은 잼)
GAMMA_MIN = 0.55      # 너무 밝히면 사진이 뿌옇게 떠서 아래 한계


def luma(src):
    """회색 중앙값 — thumb-gap-1126.md와 같은 잼(640×360으로 맞춘 뒤 L 중앙값)."""
    im = src if isinstance(src, Image.Image) else Image.open(src)
    return float(np.median(np.asarray(im.convert('RGB').resize((640, 360), Image.LANCZOS).convert('L'))))


def brighten(im, target=LUMA_TARGET):
    """사진만 감마로 밝힘(글자 그리기 전). 중앙값이 target 넘으면 손대지 않음. 돌려줌: (사진, 감마)."""
    m = luma(im)
    if m >= target: return im, 1.0
    g = max(GAMMA_MIN, np.log(target / 255) / np.log(max(m, 1) / 255))
    a = (np.asarray(im.convert('RGB')).astype(np.float32) / 255) ** g
    return Image.fromarray((a * 255).clip(0, 255).astype(np.uint8)), round(float(g), 3)


def screen_paste(base, chart, quad, keep=None, soft=3):
    """chart를 사진 속 화면·종이(quad: 왼위·오위·오아래·왼아래, base 픽셀)에 원근 맞춰 덮음.
    keep(base와 같은 크기 L 마스크, 255=원래 사진 남김) — 화면 앞을 가리는 손 등."""
    import cv2
    a = np.asarray(base.convert('RGB')).astype(np.float32); s = np.asarray(chart.convert('RGB')); hh, ww = s.shape[:2]
    P = cv2.getPerspectiveTransform(np.float32([[0, 0], [ww, 0], [ww, hh], [0, hh]]), np.float32(quad))
    out = cv2.warpPerspective(s, P, (a.shape[1], a.shape[0])).astype(np.float32)
    m = cv2.warpPerspective(np.full((hh, ww), 255, np.uint8), P, (a.shape[1], a.shape[0]))
    if keep is not None: m = np.minimum(m, 255 - np.asarray(keep))
    m = cv2.GaussianBlur(m, (2 * soft + 1, 2 * soft + 1), 0)[..., None] / 255.0
    return Image.fromarray((a * (1 - m) + out * m).astype(np.uint8))


def skin_mask(base, grow=9):
    """손·팔 살색 마스크(화면 앞 손 남기기용). R>G>B·R 높음·채도 조건, 넓혀서 가장자리 번짐 막음."""
    a = np.asarray(base.convert('RGB')).astype(np.int16); R, G, B = a[..., 0], a[..., 1], a[..., 2]
    m = (R > 95) & (G > 40) & (B > 20) & (R > G + 12) & (R > B + 25) & ((R - np.minimum(G, B)) > 30)
    m &= (G > B + 4) & (G > R * 0.5)   # 화면 속 빨강·분홍 봉(G 낮음·B>G)은 살색에서 뺌 — SQ-1 b2 첫 판에 남은 봉
    im = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(5))
    import cv2   # 가장 큰 덩어리(손)만 — 봉 부스러기 점 빼기
    n, lab, st, _ = cv2.connectedComponentsWithStats((np.asarray(im) > 0).astype(np.uint8))
    if n > 1:
        big = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA])); im = Image.fromarray(((lab == big) * 255).astype(np.uint8))
    return im.filter(ImageFilter.MaxFilter(grow))
