# 대출 계산기 경쟁 375 첫 화면 캡처 (firemap-designer 10/5) — py -3.12 cap.py
import asyncio, sys
from pathlib import Path
from playwright.async_api import async_playwright
D = Path(__file__).parent / "cap"
UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
LIVE = {
 "naver": "https://m.search.naver.com/search.naver?query=%EB%8C%80%EC%B6%9C%EC%9D%B4%EC%9E%90%EA%B3%84%EC%82%B0%EA%B8%B0",
 "budongsan": "https://xn--989a00af8jnslv3dba.com/loan",
 "finda": "https://finda.co.kr/calculator/debt-repayment",
 "kb": "https://omoney.kbstar.com/quics?page=C016613",
 "fss": "https://fine.fss.or.kr/fine/fnctip/lonCalc/view.do?menuNo=900017",
 "kinfa": "https://www.kinfa.or.kr/financialProduct/learnMorePopup.do",
}
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={"width": 375, "height": 812}, device_scale_factor=2, user_agent=UA, locale="ko-KR")
        for k, u in LIVE.items():
            if len(sys.argv) > 1 and k not in sys.argv[1:]: continue
            pg = await ctx.new_page()
            try:
                r = await pg.goto(u, wait_until=("load" if k=="budongsan" else "networkidle"), timeout=45000); await pg.wait_for_timeout(2000)
                await pg.screenshot(path=str(D / f"{k}-375.png"))
                sw = await pg.evaluate("document.documentElement.scrollWidth")
                print("ok", k, r.status if r else None, pg.url[:90], "scrollWidth", sw)
            except Exception as e: print("fail", k, str(e)[:120])
            await pg.close()
        await b.close()
asyncio.run(main())
