import sys
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page()
    for n in ('1910','1964','1908'):
        pg.goto(f'https://www.plusetf.co.kr/insight/report/detail?n={n}', wait_until='networkidle', timeout=60000); pg.wait_for_timeout(1500)
        t=pg.inner_text('body'); open(f'raw/report_{n}.txt','w',encoding='utf-8').write(t)
        i=t.find('[PLUS'); print(n, t[i:i+120].replace('\n',' '))
    b.close()
