# 미래에셋 TIGER 상품 상세 렌더 뒤 분배금 현황·총보수 받기(329200·182480), 2026-11-22 write-b
import re,sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright
for code,isin in [('329200','KR7329200003'),('182480','KR7182480007')]:
    U=f'https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund={isin}'
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page()
        pg.goto(U,timeout=60000); pg.wait_for_load_state('networkidle',timeout=60000); pg.wait_for_timeout(5000)
        t=pg.inner_text('body'); open(f'raw/tiger_{code}_1122.txt','w',encoding='utf-8').write(t)
        print('==',code,len(t))
        for k in ['총보수','분배금','기준일','순자산']:
            for m in list(re.finditer(k,t))[:2]:
                print(k,'|',t[max(0,m.start()-60):m.start()+200].replace('\n',' / '))
        b.close()
