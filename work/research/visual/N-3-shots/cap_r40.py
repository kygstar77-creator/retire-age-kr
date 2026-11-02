# N-3 r40 '내 숫자 넣기' — firemap.kr/calc/salary 실제 화면(우리 사이트) 1단계: 입력 칸 구조 보기
import sys, os
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')
O = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cap')
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 412, 'height': 900}, device_scale_factor=3)
    pg.goto('https://firemap.kr/calc/salary', wait_until='networkidle'); pg.wait_for_timeout(1500)
    pg.screenshot(path=os.path.join(O, 'r40_raw.png'), full_page=True)
    for el in pg.query_selector_all('input, select, button'):
        print(el.evaluate("e => [e.tagName, e.type, e.id, e.name, e.getAttribute('aria-label'), e.placeholder, e.value, (e.innerText||'').slice(0,30)].join(' | ')"))
    b.close()
