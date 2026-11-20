# KOSPI-1 썸네일 11/20 판(visual) — make_kospi1.py 그대로 쓰고 두 곳만 바꿈:
#   ① 큰 글 둘째 줄 '올해만 23번 나왔다' → '2026년 들어 23번'(copywriter 11/20 07:53, A88 상대 시점 막힘)
#   ② 사진 5717791 노트북 화면의 'Bitcoin/BTCUSD' 차트 → (n1) 우리 코스피 2026 일별 종가 선 + -5% 이하 23날 점을 화면에 원근 맞춰 덮음
#      (benchmark-loop '주제를 싣는 배경' 지시, 값 = ep/KOSPI-1/kospi_daily_ecos.json·calc2_out 23일) · (n2) 화면만 흐리게(글자 0)
import os, sys, json
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import cv2
import make_kospi1 as M
O = M.O; EP = os.path.join(M.WORK, 'research', 'longform', 'ep', 'KOSPI-1')
M.BIG = ['코스피 5% 넘게 빠진 날', '2026년 들어 23번']
SRC = 'worried_desk_5717791.jpg'
# 노트북 화면 네 모서리(원본 1880×1253 기준, 눈으로 잡음): 왼위·오위·오아래·왼아래
Q = np.float32([[1136, 356], [1582, 416], [1539, 416+300-2], [1097, 636]])

D = [(k, v) for k, v in json.load(open(os.path.join(EP, 'kospi_daily_ecos.json'), encoding='utf-8')) if k >= '20251230' and k <= '20261113']
pct = [(D[i][0], D[i][1], (D[i][1] / D[i - 1][1] - 1) * 100) for i in range(1, len(D))]
pct = [p for p in pct if p[0] >= '20260101']
DOWN = [p for p in pct if p[2] <= -5]
assert len(DOWN) == 23, len(DOWN)
assert abs(max(p[1] for p in pct) - 9114.55) < 0.01


def chart(w=1100, h=760):
    im = Image.new('RGB', (w, h), (250, 250, 252)); d = ImageDraw.Draw(im)
    vals = [p[1] for p in pct]; lo, hi = min(vals) * 0.95, max(vals) * 1.03
    X = lambda i: 40 + (w - 80) * i / (len(pct) - 1); Y = lambda v: h - 60 - (h - 120) * (v - lo) / (hi - lo)
    for g in range(1, 5): d.line([(40, 60 + g * (h - 120) / 5), (w - 40, 60 + g * (h - 120) / 5)], fill=(225, 228, 235), width=2)
    pts = [(X(i), Y(p[1])) for i, p in enumerate(pct)]
    d.polygon(pts + [(pts[-1][0], h - 60), (pts[0][0], h - 60)], fill=(214, 224, 240))
    d.line(pts, fill=(40, 60, 110), width=7, joint='curve')
    for i, p in enumerate(pct):
        if p[2] <= -5: x, y = pts[i]; d.ellipse((x - 13, y - 13, x + 13, y + 13), fill=M.ORANGE, outline=(255, 255, 255), width=3)
    return im


def warp(base, src):
    a = np.array(base); s = np.array(src); hh, ww = s.shape[:2]
    P = cv2.getPerspectiveTransform(np.float32([[0, 0], [ww, 0], [ww, hh], [0, hh]]), Q)
    out = cv2.warpPerspective(s, P, (a.shape[1], a.shape[0]))
    m = cv2.warpPerspective(np.full((hh, ww), 255, np.uint8), P, (a.shape[1], a.shape[0]))
    m = cv2.GaussianBlur(m, (5, 5), 0)[..., None] / 255.0
    return Image.fromarray((a * (1 - m) + out * m).astype(np.uint8))


def blur_screen(base):
    m = Image.new('L', base.size, 0); ImageDraw.Draw(m).polygon([tuple(p) for p in Q], fill=255)
    m = m.filter(ImageFilter.GaussianBlur(6))
    return Image.composite(base.filter(ImageFilter.GaussianBlur(28)), base, m)


if __name__ == '__main__':
    base = Image.open(os.path.join(M.H, SRC)).convert('RGB')
    warp(base, chart().filter(ImageFilter.GaussianBlur(1.6))).save(os.path.join(M.H, 'worried_desk_kospi_n1.jpg'), quality=95)
    blur_screen(base).save(os.path.join(M.H, 'worried_desk_blur_n2.jpg'), quality=95)
    kw = dict(xa=0.5, band=170, tshade=(400, 150), sw=13, tsw=8)
    M.make('k1_n1.png', 'worried_desk_kospi_n1.jpg', 0.25, **kw)
    M.make('k1_n2.png', 'worried_desk_blur_n2.jpg', 0.25, **kw)
    # n0 = 옛 사진(BTCUSD 화면) + 새 문구 — 사진만 겨루는 기준판(공개 안 함, 화면에 다른 종목 글자)
    M.make('k1_n0.png', SRC, 0.25, **kw)
