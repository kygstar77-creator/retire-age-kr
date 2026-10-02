# ds-v2·Stitch 비교·허브 시안 캡처 (firemap-designer 10/2)
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
D = Path(__file__).resolve().parent; G = D.parent.parent / "global-calcs"
JOBS = [
 (D/"preview.html", "", D/"v2-salary", True),
 (D/"claude-stitch-prompt.html", "", D/"stitch-claude", True),
 (G/"preview.html", "", G/"hub-now", True),
 (G/"preview.html", "?state=checked", G/"hub-checked", True),
]
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for f, q, out, both in JOBS:
            url = f.as_uri() + q
            for tag, vp, scale, scheme in (("375", {"width":375,"height":812}, 2, "light"), ("375-dark", {"width":375,"height":812}, 2, "dark"), ("1280", {"width":1280,"height":800}, 1, "light"), ("320", {"width":320,"height":568}, 2, "light")):
                ctx = await b.new_context(viewport=vp, device_scale_factor=scale, color_scheme=scheme)
                pg = await ctx.new_page(); await pg.goto(url); await pg.wait_for_timeout(1200)
                sw = await pg.evaluate("document.documentElement.scrollWidth")
                await pg.screenshot(path=f"{out}-{tag}.png")
                if tag == "375": await pg.screenshot(path=f"{out}-{tag}-full.png", full_page=True)
                print(out.name, tag, "scrollWidth", sw)
                await ctx.close()
        await b.close()
asyncio.run(main())
