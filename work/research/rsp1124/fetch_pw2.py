# 11/24 올리기 전 확인: SPY 보유 종목 xlsx·인베스코 RSP 페이지를 chromium으로 다시 받기
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); c=b.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"); pg=c.new_page()
    r=c.request.get("https://www.ssga.com/us/en/intermediary/library-content/products/fund-data/etfs/us/holdings-daily-us-en-spy.xlsx",timeout=60000)
    open("raw/spy_holdings_1124.xlsx","wb").write(r.body()); print("spy",r.status,len(r.body()))
    pg.goto("https://www.invesco.com/us/en/etf/sp-500-equal-weight-rsp.html",timeout=60000,wait_until="domcontentloaded"); pg.wait_for_timeout(9000)
    open("raw/invesco_rsp_1124.txt","w",encoding="utf-8").write(pg.inner_text("body")); print("inv ok")
    b.close()
