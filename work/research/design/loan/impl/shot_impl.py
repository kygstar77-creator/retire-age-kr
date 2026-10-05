# 대출 v1 구현본 캡처(dev 서버 #loan) — 375·320·다크·1280, 넘침·버튼 아래끝 잼
import asyncio, sys
from pathlib import Path
from playwright.async_api import async_playwright
D = Path(__file__).resolve().parent
BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5191"
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for tag, vp, sc, scheme in (("375", {"width":375,"height":812}, 2, "light"), ("375-dark", {"width":375,"height":812}, 2, "dark"), ("1280", {"width":1280,"height":800}, 1, "light"), ("320", {"width":320,"height":568}, 2, "light")):
            ctx = await b.new_context(viewport=vp, device_scale_factor=sc, color_scheme=scheme)
            pg = await ctx.new_page(); errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            await pg.goto(BASE + "/?fm_internal=1#loan", wait_until="domcontentloaded", timeout=120000); await pg.wait_for_timeout(4000)
            sw = await pg.evaluate("document.documentElement.scrollWidth")
            cta = await pg.evaluate("(()=>{const b=[...document.querySelectorAll('button')].find(x=>x.textContent.includes('몇 살에 은퇴'));return b?b.getBoundingClientRect().bottom:-1})()")
            txt = await pg.evaluate("(document.querySelector('.ds-loan')||document.body).innerText.slice(0,300)")
            await pg.screenshot(path=str(D/f"impl-{tag}.png"))
            if tag == "375": await pg.screenshot(path=str(D/"impl-375-full.png"), full_page=True)
            print(tag, "scrollWidth", sw, "cta bottom", round(cta), "errors", errs[:2]); print(txt.replace("\n"," | ")[:300]); await ctx.close()
        await b.close()
asyncio.run(main())
