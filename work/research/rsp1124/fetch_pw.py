# 자바스크립트로 그리는 운용사 화면을 Playwright chromium으로 읽어 글자만 저장
import sys
from playwright.sync_api import sync_playwright
pages={"tiger_488500":"https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7488500000","tiger_360750":"https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7360750004",
}
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(user_agent="Mozilla/5.0")
    for k,u in pages.items():
        try:
            pg.goto(u,timeout=60000,wait_until="domcontentloaded"); pg.wait_for_timeout(9000)
            open(f"raw/{k}.txt","w",encoding="utf-8").write(pg.inner_text("body")); print(k,"ok")
        except Exception as e: print(k,"fail",e)
    b.close()
