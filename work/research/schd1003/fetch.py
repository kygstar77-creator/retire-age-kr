from playwright.sync_api import sync_playwright
import sys
with sync_playwright() as p:
    b=p.chromium.launch(headless=False,args=["--window-position=-2000,0"]); pg=b.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36")
    pg.goto("https://www.schwabassetmanagement.com/products/schd", timeout=60000); pg.wait_for_timeout(6000)
    t=pg.inner_text("body"); open("schwab.txt","w",encoding="utf-8").write(t)
    b.close()
