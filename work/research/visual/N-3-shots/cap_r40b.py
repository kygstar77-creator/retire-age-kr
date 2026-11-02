import sys, os
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')
O = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cap')
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 412, 'height': 900}, device_scale_factor=3)
    pg.goto('https://firemap.kr/calc/salary', wait_until='networkidle'); pg.wait_for_timeout(1000)
    pg.get_by_role('button', name='연봉').first.click(); pg.wait_for_timeout(800)
    pg.screenshot(path=os.path.join(O, 'r40_sheet.png'))
    for el in pg.query_selector_all('input, button'):
        if el.is_visible(): print(el.evaluate("e => [e.tagName, e.type, e.getAttribute('aria-label'), e.placeholder, e.value, (e.innerText||'').slice(0,30)].join(' | ')"))
    print(pg.url)
    b.close()
