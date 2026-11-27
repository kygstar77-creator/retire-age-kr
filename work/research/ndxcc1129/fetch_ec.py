# etfcheck 분배 이력(2차) — KODEX 494300·TIGER 486290 2025-03 대조용. 11/27 write.
import sys, re
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(headless=True)
    for c in ['494300','486290']:
        pg=b.new_page(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124')
        pg.goto(f'https://www.etfcheck.co.kr/mobile/etpitem/{c}/dividend',timeout=60000,wait_until='networkidle'); pg.wait_for_timeout(4000)
        t=re.sub(r'\s+',' ',pg.inner_text('body')); open(f'raw/etfcheck_{c}_1127.txt','w',encoding='utf-8').write(pg.url+'\n'+t)
        print(c,len(t)); [print('  ',t[max(0,m.start()-40):m.start()+100]) for m in list(re.finditer(r'2025[.\-]0?3',t))[:3]]
    b.close()
