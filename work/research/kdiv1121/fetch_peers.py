# 같은 갈래 1차: 미래에셋 TIGER 은행고배당플러스TOP10(466940)·삼성 KODEX 고배당주(279530) 상품 페이지 분배금 — 한 번씩만
import sys, json
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')
J={}
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page()
    def on(r):
        if 'divid' in r.url.lower() or 'distrib' in r.url.lower():
            try: J[r.url]=r.text()
            except Exception: pass
    pg.on('response', on)
    for name,url in [('tiger466940','https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7466940009'),
                     ('kodex279530','https://www.samsungfund.com/etf/product/view.do?id=2ETF96')]:
        try:
            pg.goto(url, wait_until='networkidle', timeout=60000); pg.wait_for_timeout(3000)
            for t in ('분배금','분배'):
                try: pg.get_by_text(t, exact=True).first.click(timeout=3000); pg.wait_for_timeout(2500); break
                except Exception: pass
            t=pg.inner_text('body'); open(f'raw/{name}.txt','w',encoding='utf-8').write(t)
            print(name, len(t), t.count('분배'))
        except Exception as e: print(name,'ERR',e)
    json.dump(J,open('raw/peers_api.json','w',encoding='utf-8'),ensure_ascii=False)
    b.close()
print(list(J)[:6])
