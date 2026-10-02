# 디자인 품질 프로젝트 1단계: 운영 화면·비교 화면 375px 첫 화면 캡처
import sys, asyncio
from pathlib import Path
from urllib.parse import quote
from playwright.async_api import async_playwright
OUT = Path(__file__).parent / "cap"
OURS = {
 "home": "https://firemap.kr/?fm_internal=1",
 "salary": "https://firemap.kr/calc/salary?fm_internal=1",
 "severance": "https://firemap.kr/calc/severance?fm_internal=1",
 "unemp": "https://firemap.kr/calc/unemployment-benefit?fm_internal=1",
 "guide": "https://firemap.kr/guide/?fm_internal=1",
 # 10/2 designer: 빠진 도구 6개(sitemap.xml 기준)
 "dividend": "https://firemap.kr/dividend?fm_internal=1",
 "pension": "https://firemap.kr/pension?fm_internal=1",
 "health": "https://firemap.kr/health-insurance?fm_internal=1",
 "tax": "https://firemap.kr/tax?fm_internal=1",
 "firetype": "https://firemap.kr/firetype?fm_internal=1",
 "ranking": "https://firemap.kr/ranking?fm_internal=1",
}
ONLY = set(sys.argv[1:])
REF = {
 "naver-salary": "https://m.search.naver.com/search.naver?query=" + quote("연봉계산기"),
 "naver-severance": "https://m.search.naver.com/search.naver?query=" + quote("퇴직금계산기"),
 "naver-unemp": "https://m.search.naver.com/search.naver?query=" + quote("실업급여계산기"),
 "toss": "https://toss.im/",
 "banksalad": "https://www.banksalad.com/",
 "calcnet": "https://www.calculator.net/retirement-calculator.html",
}
UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for group in (OURS, REF):
            for k, u in group.items():
                if ONLY and k not in ONLY: continue
                for name, vp, ua, mob in (("m", {"width":375,"height":812}, UA, True), ("d", {"width":1440,"height":900}, None, False)):
                    ctx = await b.new_context(viewport=vp, user_agent=ua, is_mobile=mob, device_scale_factor=2 if mob else 1, locale="ko-KR")
                    pg = await ctx.new_page()
                    try:
                        await pg.goto(u, wait_until="load", timeout=45000)
                    except Exception as e:
                        print("warn", k, name, str(e)[:80])
                    await pg.wait_for_timeout(1500)
                    await pg.screenshot(path=str(OUT / f"{k}-{name}.png"))
                    if mob:
                        await pg.screenshot(path=str(OUT / f"{k}-{name}-full.png"), full_page=True)
                    await ctx.close()
                print("ok", k)
        await b.close()
asyncio.run(main())
