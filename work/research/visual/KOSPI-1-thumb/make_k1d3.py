# KOSPI-1 k1_d3 (copywriter 2026-11-23 — 관문 11:30 막힘 풀기) — k1_d2 글자 그대로, 사진만 손 사진(hands_phone_32219704)으로.
#   이유: k1_d2 1초 시험 3차 권유 '약간~예' 3/3, 원인 '머리 감싼 사람' 3/3(copy/kospi1/titles.md '3차-24'). 휴대폰·노트북 화면은 흐림(오르는 화살표·차트가 권유로 읽히지 않게).
import os, sys
from PIL import Image, ImageDraw, ImageFilter
sys.stdout.reconfigure(encoding='utf-8')
O = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, O)
import make_kospi1 as M
src = Image.open(os.path.join(M.H, 'hands_phone_32219704.jpg')).convert('RGB')
blur = src.filter(ImageFilter.GaussianBlur(28)); m = Image.new('L', src.size, 0); d = ImageDraw.Draw(m)
d.polygon([(500, 640), (830, 320), (1070, 560), (720, 860)], fill=255)          # 휴대폰 화면
d.polygon([(1290, 400), (1690, 0), (1880, 0), (1880, 1000), (1720, 1000)], fill=255)  # 노트북 화면
m = m.filter(ImageFilter.GaussianBlur(12))
Image.composite(blur, src, m).save(os.path.join(M.H, 'hands_phone_blur_d3.jpg'), quality=95)
M.BIG = ['코스피 5% 넘게 빠진 날', '2026년 들어 24번']
M.make('k1_d3.png', 'hands_phone_blur_d3.jpg', 0.2, band=190, tshade=(400, 160), sw=13, tsw=8)
