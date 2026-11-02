# N-3 r40 — 연봉 4,000만(기본) → +1000만 = 5,000만, 시트 닫고 첫 화면 캡처(412px·3배)
import sys, os
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')
O = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cap')
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 412, 'height': 900}, device_scale_factor=3)
    pg.goto('https://firemap.kr/calc/salary', wait_until='networkidle'); pg.wait_for_timeout(1000)
    pg.get_by_role('button', name='연봉').first.click(); pg.wait_for_timeout(600)
    pg.get_by_role('button', name='+1000만').first.click(); pg.wait_for_timeout(600)
    pg.get_by_role('button', name='닫기').first.click(); pg.wait_for_timeout(800)
    pg.screenshot(path=os.path.join(O, 'r40_5000.png'))
    print(pg.inner_text('main')[:900] if pg.query_selector('main') else pg.inner_text('body')[:900])
    b.close()
