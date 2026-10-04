# v3 시안 캡처 + 비교판 (우리 v3 375 | 우리 v2f 375 | 네이버 연봉 | 토스 | 뱅크샐러드 | KRDS)
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
from PIL import Image, ImageDraw, ImageFont
D = Path(__file__).resolve().parent; Q = D.parents[1] / "quality"; R = D.parent
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for tag, vp, sc, scheme in (("375", {"width":375,"height":812}, 2, "light"), ("375-dark", {"width":375,"height":812}, 2, "dark"), ("1280", {"width":1280,"height":800}, 1, "light"), ("320", {"width":320,"height":568}, 2, "light")):
            ctx = await b.new_context(viewport=vp, device_scale_factor=sc, color_scheme=scheme)
            pg = await ctx.new_page(); await pg.goto((D/"preview.html").as_uri()); await pg.wait_for_timeout(1500)
            sw = await pg.evaluate("document.documentElement.scrollWidth")
            await pg.screenshot(path=str(D/f"v3-{tag}.png"))
            if tag == "375": await pg.screenshot(path=str(D/"v3-375-full.png"), full_page=True)
            print(tag, "scrollWidth", sw); await ctx.close()
        await b.close()
asyncio.run(main())
F = ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf", 36)
items = [("우리 v3(레퍼런스 토큰)", D/"v3-375.png"), ("우리 v2f(이전)", Q/"ds-v2"/"v2-salary-375.png"), ("참조: 네이버 연봉", Q/"cap"/"naver-salary-m.png"),
         ("참조: 토스", Q/"cap"/"toss-m.png"), ("참조: 뱅크샐러드", Q/"cap"/"banksalad-m.png")]
ims = []
for _, f in items:
    im = Image.open(f).convert("RGB"); w = 750; h = int(im.height * w / im.width)
    im = im.resize((w, h)).crop((0, 0, w, 1624)); ims.append(im)
pad, top = 40, 70
board = Image.new("RGB", (len(ims)*(750+pad)+pad, 1624+top+pad), (230,230,230)); d = ImageDraw.Draw(board)
for i, ((lab, _), im) in enumerate(zip(items, ims)):
    x = pad + i*(750+pad); board.paste(im, (x, top)); d.text((x, 15), lab, fill=(200,0,0) if i < 2 else (0,0,0), font=F)
board.save(D/"compare-v3.png"); board.resize((board.width//3, board.height//3)).save(D/"compare-v3-small.png"); print(board.size)
