# 2차(16:5x): 심사(제미나이 6~7.5·Claude 심사관 6) 공통 — 110px에서 '무슨 87.5%인지' 안 읽힘, 흰 바탕이 경쟁과 섞임
#   → 진한 남색 카드 + "전세가율" 큰 글자 + 숫자 노랑, 도장 뺌, 출처 줄은 작게 남김(근거)
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
V = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'visual', 'cafe-covers-1002'); sys.path.insert(0, V)
import make_covers as MC
from playwright.sync_api import sync_playwright
MC.HTML = (MC.HTML.replace('background:#F7F8FA', 'background:#0F1B3D').replace('.stamp{', '.stamp{display:none;')
           .replace('color:#6B7280', 'color:#A5B4D4').replace('top:196px', 'top:96px'))
Y, Wt = '#FFD43B', '#FFFFFF'
MC.COV['b10danji1003'] = dict(stamp='',
    rows=[('서울에서 가장 높은 단지', 100, Wt, 't'), ('전세가율', 190, Y, 't'), ('87.5|%', 400, Y, 'num'), ('매매가와 차이 6,600만원', 92, Wt, 't')],
    src='2026년 7~9월 국토부 실거래 · 도봉구 신동아아파트2 80㎡대', keep_orig=False,
    check=['87.5%', '6,600만원', '신동아아파트2', '전세가율', '7~9월'])
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1080}); MC.make('b10danji1003', pg); b.close()
