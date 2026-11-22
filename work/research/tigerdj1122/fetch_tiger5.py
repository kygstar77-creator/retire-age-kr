# 미래에셋 TIGER 458730 상세 — XHR 응답에서 총보수 찾기(audit 11/21 21:14), 2026-11-22 15시
import re
from playwright.sync_api import sync_playwright
U = 'https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7458730008'
hits = []
def on_resp(r):
    try:
        if r.request.resource_type in ('xhr', 'fetch', 'document'):
            t = r.text()
            if '보수' in t or 'fee' in t.lower():
                hits.append((r.url, t))
    except Exception: pass
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(locale='ko-KR')
    pg.on('response', on_resp)
    pg.goto(U, timeout=60000); pg.wait_for_timeout(15000)
    t = pg.inner_text('body')
    open('raw/tiger_page_1122.txt', 'w', encoding='utf-8').write(t)
    i = t.find('총보수'); print('BODY', repr(t[i:i+60]))
    b.close()
for u, t in hits:
    for m in re.finditer(r'총보수', t):
        s = re.sub(r'<[^>]+>', ' ', t[m.start():m.start()+400]); print(u[:100], '|', re.sub(r'\s+', ' ', s)[:160]); break
