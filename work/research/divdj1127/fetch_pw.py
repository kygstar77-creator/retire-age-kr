# 운용사 상품 페이지(자바스크립트로 그림)를 Playwright로 읽어 글자만 남긴다. 11/26 write.
import sys, re
from playwright.sync_api import sync_playwright
P = {
 'tiger': 'https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7458730009',

  'ace': 'https://www.funetf.co.kr/product/etf/view/KR7402970008',
}
with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    for k, u in P.items():
        pg = b.new_page(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124')
        try:
            pg.goto(u, timeout=40000, wait_until='networkidle')
        except Exception as e:
            print(k, 'goto', repr(e)[:80])
        pg.wait_for_timeout(3000)
        t = re.sub(r'\s+', ' ', pg.inner_text('body'))
        open(f'raw/{k}_pw_1127.txt', 'w', encoding='utf-8').write(pg.url + '\n' + t)
        print('==', k, pg.url, len(t))
        for w in ['총보수', '기준일', '분배금 지급']:
            m = re.search(w, t)
            if m: print(' ', w, ':', t[max(0, m.start()-40):m.start()+200])
    b.close()
