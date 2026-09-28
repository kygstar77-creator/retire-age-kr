import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright
U={"kodex":"https://www.samsungfund.com/etf/product/view.do?id=2ETFE4",
   "tiger":"https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7360750004"}
with sync_playwright() as p:
    b=p.chromium.launch()
    for k,u in U.items():
        pg=b.new_page(); pg.goto(u,timeout=60000); pg.wait_for_timeout(6000)
        t=pg.inner_text("body"); open(f"raw/{k}.txt","w",encoding="utf-8").write(t)
        print(k,len(t))
    b.close()
