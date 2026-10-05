# X-V1·X-CN-1 v3 로컬 캡처 (firemap-venture-builder 10/5) — 375 첫 화면·375 입력 뒤·1280, 측정 요청은 막는다
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
D = Path(__file__).parent; R = D.parent; V = R.parent / "ventures"
UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
SHOTS = [  # (출력, 파일, 폭, 높이, 입력)
 (R/"uk-pay/v3/xv1-375.png", V/"uk-pay/site/index.html", 375, 812, None),
 (R/"uk-pay/v3/xv1-375-60k.png", V/"uk-pay/site/index.html", 375, 812, "60000"),
 (R/"uk-pay/v3/xv1-1280.png", V/"uk-pay/site/index.html", 1280, 800, "60000"),
 (R/"x-cn-1/v3/xcn1-375.png", V/"x-cn-1/site/hanneunggeom/index.html", 375, 812, None),
 (R/"x-cn-1/v3/xcn1-1280.png", V/"x-cn-1/site/hanneunggeom/index.html", 1280, 800, None),
]
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for out, f, w, h, val in SHOTS:
            ctx = await b.new_context(viewport={"width": w, "height": h}, device_scale_factor=2, user_agent=UA if w < 500 else None, locale="ko-KR")
            pg = await ctx.new_page(); errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            await pg.route("**/*supabase*/**", lambda r: r.abort())
            await pg.goto(f.as_uri() + "?fm_internal=1"); await pg.wait_for_timeout(600)
            if val:
                await pg.fill("#sal", val); await pg.dispatch_event("#sal", "input"); await pg.wait_for_timeout(300)
            m = await pg.evaluate("""() => { const q = s => document.querySelector(s), r = s => q(s) ? Math.round(q(s).getBoundingClientRect().bottom) : null;
              return {over: document.documentElement.scrollWidth - innerWidth, h1: q('h1') ? Math.round(q('h1').getBoundingClientRect().height) : null,
                      cta: r('#cta') ?? r('#ics'), tblhead: r('thead'), body: document.body.scrollHeight}; }""")
            out.parent.mkdir(parents=True, exist_ok=True)
            await pg.screenshot(path=str(out)); print(out.name, m, "errors", errs)
            await ctx.close()
        await b.close()
asyncio.run(main())
